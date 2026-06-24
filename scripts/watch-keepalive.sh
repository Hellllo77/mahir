#!/bin/bash
# watch-keepalive.sh — restarts watch.sh whenever it exits + progress-ping sidecar.
# Quinn task-24 (CLASS-3 monitor-process-death fix, 2026-05-31).
# Quinn task-progress-ping (Tier-1 mid-task-liveness, 2026-06-01) — Felix-6.7hr-class.
#
# Failure classes addressed:
#   1. Class-3 monitor-process-death: watch.sh dies (SIGTERM, OOM, crash) and the
#      Monitor task ends without restarting it. heartbeat.sh keeps posting alive →
#      silent inbound-zombie. This wrapper SEPARATELY respawns watch.sh on death
#      with 2s backoff.
#   2. Mid-task-freeze: the agent's main Claude Code loop is blocked (long wait, deep
#      thinking, hung tool) but is mid-task. The PROGRESS-PING sidecar runs as an
#      OS-level background loop INSIDE this supervisor — it reads
#      <agent-folder>/current_task.json and pings the bridge when the task is stale
#      (>5min) but still-open WORK_START on the bridge. Pings every ~3min until task
#      completes or the file goes stale-and-no-longer-on-bridge.
#
# Usage (drop-in replacement for watch.sh in Monitor commands):
#   Monitor(description="Bridge messages to <agent>",
#           command="../../scripts/watch-keepalive.sh --for <agent> --bridge http://127.0.0.1:8895 --poll 8",
#           persistent=true, timeout_ms=3600000)
#
# All args pass through verbatim to watch.sh.

set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WATCH="$SCRIPT_DIR/watch.sh"

if [[ ! -x "$WATCH" ]]; then
  echo "[watch-keepalive] FATAL: $WATCH not executable" >&2
  exit 1
fi

# Self-dedupe: kill any other watch-keepalive supervising the same --for slug
# so a re-arm cycle does not stack supervisors. Pattern matches watch.sh dedupe.
AGENT=""
BRIDGE="http://127.0.0.1:8895"
for ((i=1; i<=$#; i++)); do
  if [[ "${!i}" == "--for" ]]; then
    j=$((i+1))
    AGENT="${!j}"
  fi
  if [[ "${!i}" == "--bridge" ]]; then
    j=$((i+1))
    BRIDGE="${!j}"
  fi
done

if [[ -n "$AGENT" ]]; then
  SELF_PID=$$
  for pid in $(pgrep -f "/watch-keepalive.sh --for $AGENT"); do
    if [[ "$pid" != "$SELF_PID" ]]; then
      echo "[watch-keepalive] killing duplicate supervisor pid=$pid (self-dedupe, agent=$AGENT)" >&2
      kill -TERM "$pid" 2>/dev/null || true
    fi
  done
  sleep 1
fi

echo "[watch-keepalive] supervising watch.sh for agent=$AGENT pid=$$ at $(date '+%F %T')" >&2

# File-based heartbeat (proxy idx 687 residual): touch on each iteration so
# fleet-watchdog can detect "Monitor task itself died" — the case where this
# whole wrapper goes away. No bridge noise. /tmp/ is local-only.
HEARTBEAT_FILE="/tmp/watch-keepalive-heartbeat-${AGENT:-unknown}"
touch "$HEARTBEAT_FILE" 2>/dev/null || true

# ─────────────────────────────────────────────────────────────────────────────
# PROGRESS-PING SIDECAR (Quinn task-progress-ping, idx 1220)
# Runs as a background loop in this supervisor process, so it pings the bridge
# EVEN WHEN the agent's main Claude Code loop is blocked (the whole point).
# Contract with agent-side writer (Sage-defined current_task.json, to-be-confirmed):
#   PATH:   <CCC_ROOT>/agents/<slug>/current_task.json
#   FIELDS: task_id (string), last_updated_at (ISO-8601 UTC), summary (1-line, optional)
#   LIFE:   agent writes on WORK_START; updates last_updated_at + summary on substantive progress;
#           deletes (or leaves stale) on WORK_COMPLETE.
# Sidecar policy:
#   - Poll file every 30s.
#   - If file missing → skip (no ping).
#   - If age(last_updated_at) ≤ 5min → skip (agent fresh).
#   - If age > 5min AND task_id has matching open WORK_START on bridge AND no matching
#     WORK_COMPLETE → emit PROGRESS_PING advisory. Rate-limit: at most one ping per
#     ~3min per task to avoid bridge spam.
# Caveats:
#   - Sidecar uses 'kind: advisory' (works for any specialist with advisory in
#     kinds_allowed). Body starts with literal "PROGRESS_PING task-XXX:".
#   - The whole loop is wrapped in a tolerant pipe — any parsing failure (malformed
#     JSON, missing field) silently skips that cycle. Never crashes the supervisor.
PROGRESS_PIDS=()
if [[ -n "$AGENT" ]]; then
  CCC_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
  TASK_FILE="$CCC_ROOT/agents/$AGENT/current_task.json"

  (
    STALENESS=300       # 5 min — task considered "no fresh update"
    PING_INTERVAL=180   # 3 min — minimum gap between pings for the same task
    last_ping_at=0
    last_ping_task=""

    while true; do
      sleep 30
      [[ ! -f "$TASK_FILE" ]] && continue

      # Parse with python (tolerant — silent skip on bad JSON / missing fields).
      parsed=$(python3 - "$TASK_FILE" <<'PY' 2>/dev/null
import json, sys
from datetime import datetime, timezone
try:
    d = json.load(open(sys.argv[1]))
    tid = d.get("task_id", "")
    lua = d.get("last_updated_at", "")
    summary = d.get("summary", "no fresh update")
    dt = datetime.fromisoformat(lua.replace("Z", "+00:00"))
    age = int((datetime.now(timezone.utc) - dt).total_seconds())
    print(f"{tid}\t{age}\t{summary}")
except Exception:
    pass
PY
)
      [[ -z "$parsed" ]] && continue
      task_id=$(printf '%s' "$parsed" | awk -F'\t' '{print $1}')
      age=$(printf '%s' "$parsed" | awk -F'\t' '{print $2}')
      summary=$(printf '%s' "$parsed" | awk -F'\t' '{print $3}')

      [[ -z "$task_id" || -z "$age" ]] && continue
      [[ "$age" -lt "$STALENESS" ]] && continue

      now=$(date +%s)
      if [[ "$last_ping_task" == "$task_id" ]] && [[ $((now - last_ping_at)) -lt "$PING_INTERVAL" ]]; then
        continue
      fi

      # Verify task still open on bridge: agent has posted WORK_START $task_id
      # but no WORK_COMPLETE $task_id. Query messages.json (legacy endpoint OK for inspection).
      open_state=$(curl -sf --max-time 4 "$BRIDGE/messages.json" 2>/dev/null \
        | python3 -c "
import json, sys
try:
    msgs = json.load(sys.stdin)
except Exception:
    print('skip'); sys.exit()
started = False
completed = False
for m in msgs:
    if m.get('from') != '$AGENT':
        continue
    body = m.get('body','')
    if 'WORK_START $task_id' in body:
        started = True
    if 'WORK_COMPLETE $task_id' in body:
        completed = True
print('open' if (started and not completed) else 'closed')
" 2>/dev/null)
      [[ "$open_state" != "open" ]] && continue

      # Emit the ping. kind=advisory, body starts with PROGRESS_PING marker.
      body_safe=$(printf 'PROGRESS_PING %s: %s (mid-task age=%ss; sidecar — agent main loop may be blocked)' "$task_id" "$summary" "$age" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))")
      curl -sf --max-time 4 -X POST "$BRIDGE/post" \
        -H "Content-Type: application/json" \
        -d "{\"from\":\"$AGENT\",\"to\":\"quinn-pm-command-center-hq\",\"kind\":\"advisory\",\"body\":$body_safe}" \
        > /dev/null 2>&1

      last_ping_at=$now
      last_ping_task="$task_id"
      echo "[watch-keepalive] PROGRESS_PING fired for $AGENT task=$task_id age=${age}s" >&2
    done
  ) &
  PROGRESS_PID=$!
  PROGRESS_PIDS+=("$PROGRESS_PID")
  echo "[watch-keepalive] started progress-ping sidecar pid=$PROGRESS_PID task_file=$TASK_FILE" >&2
fi

# Clean up sidecars on supervisor exit. ${...:-} guards `set -u` on empty array.
trap 'for p in "${PROGRESS_PIDS[@]:-}"; do [[ -n "$p" ]] && kill "$p" 2>/dev/null || true; done' EXIT

while true; do
  touch "$HEARTBEAT_FILE" 2>/dev/null || true
  "$WATCH" "$@"
  rc=$?
  echo "[watch-keepalive] watch.sh exited rc=$rc at $(date '+%F %T'), restart in 2s" >&2
  sleep 2
done
