#!/usr/bin/env bash
# Polls the bridge for messages addressed to a specific agent.
# Uses GET /messages?for=<agent>&since=<idx> — ADR-001a server-side filter.
# Client-side to-field matching removed; server returns only the addressed slice.
#
# Usage:
#   ./scripts/watch.sh --for quinn-pm-command-center-hq --poll 4
#   ./scripts/watch.sh --for quinn-pm-command-center-hq --kinds task,question --poll 4

set -euo pipefail

BRIDGE="${BRIDGE_URL:-http://127.0.0.1:8767}"
AGENT=""
# Quinn dispatch 2026-05-30: default poll bumped 4s → 8s to halve bridge load
# (15 agents @ 4s on single-thread FastAPI is borderline). 8s coordination
# latency is acceptable. Callers with explicit `--poll N` override this.
POLL=8
KINDS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --for) AGENT="$2"; shift 2 ;;
    --poll) POLL="$2"; shift 2 ;;
    --bridge) BRIDGE="$2"; shift 2 ;;
    --kinds) KINDS="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

if [[ -z "$AGENT" ]]; then
  echo "Usage: $0 --for <agent> [--poll seconds] [--bridge url] [--kinds csv]"
  exit 2
fi

# Self-dedupe (Quinn dispatch 2026-05-30 systemic-fix): kill any existing
# watch.sh peers for this agent before we settle in. Prevents re-arm cycles
# from stacking duplicate pollers (proxy observed 36 procs/agent earlier).
# Matches by exact `--for $AGENT` token so agents with prefix overlap don't
# clobber each other. Excludes self ($$ stable across subshells).
SELF_PID=$$
for pid in $(pgrep -f "/watch.sh --for $AGENT"); do
  if [[ "$pid" != "$SELF_PID" ]]; then
    echo "[watch] killing duplicate watch.sh pid=$pid (self-dedupe, agent=$AGENT)" >&2
    kill -TERM "$pid" 2>/dev/null || true
  fi
done
# Brief grace for SIGTERM to land + give any racing twin its dedupe window.
sleep 1

# Initial cursor — task-1c204723 #73 cursor-resilience.
# Bridge-restart resilience: if a persisted cursor exists from a prior wake of
# this same agent's watch.sh, prefer it over current head so messages that
# arrived during the outage are caught up via since=<persisted> (not skipped).
# Three branches:
#   (a) persisted file exists + integer + <= current head    → resume + catch up
#   (b) persisted file exists + integer + > current head     → rotation occurred,
#                                                              resync to head
#   (c) no file (fresh start) or unreadable                  → current head
# Falls back to -1 only if bridge is unreachable (preserves prior behaviour).
# Uses legacy /messages.json (grandfathered for inspection per ADR-001a §5).
CURSOR_FILE="/tmp/watch_cursor_${AGENT}"
HEAD_IDX=$(curl -sf "$BRIDGE/messages.json" \
       | python3 -c "import json,sys; m=json.load(sys.stdin); print(m[-1]['index'] if m else -1)" 2>/dev/null \
       || echo -1)

if [[ -f "$CURSOR_FILE" ]]; then
  PERSISTED=$(cat "$CURSOR_FILE" 2>/dev/null | head -1 | tr -d '[:space:]')
  if [[ "$PERSISTED" =~ ^-?[0-9]+$ ]]; then
    if [[ "$HEAD_IDX" =~ ^[0-9]+$ ]] && [[ "$PERSISTED" -gt "$HEAD_IDX" ]]; then
      LAST="$HEAD_IDX"
      echo "[watch] cursor-resilience: persisted=$PERSISTED > head=$HEAD_IDX — rotation detected, resync to head" >&2
    else
      LAST="$PERSISTED"
      echo "[watch] cursor-resilience: resuming from persisted=$PERSISTED (head=$HEAD_IDX); will catch up gap via since=" >&2
    fi
  else
    LAST="$HEAD_IDX"
  fi
else
  LAST="$HEAD_IDX"
fi

echo "[watch] bridge=$BRIDGE target=$AGENT starting_at_index=$LAST poll=${POLL}s"

# Build server-side filter URL (ADR-001a)
BASE_URL="$BRIDGE/messages?for=$AGENT"
if [[ -n "$KINDS" ]]; then
  BASE_URL="$BASE_URL&kinds=$KINDS"
fi

# File-based liveness heartbeat (proxy idx 704 fix): touched at the START of every
# poll iteration so the mtime reflects actual polling liveness, not just respawn
# events. fleet-watchdog reads this file's mtime to detect Class-3 monitor-process
# death. If the loop wedges OR the process dies, mtime stops advancing → stale →
# advisory. The wrapper-level touch in watch-keepalive.sh covers the initial-
# spawn gap; this per-poll touch is the steady-state signal.
HEARTBEAT_FILE="/tmp/watch-keepalive-heartbeat-${AGENT}"

# Fix-B (Quinn task-a55dfef3, 2026-06-01): per-agent cohort decorrelation jitter.
# When the fleet receives a broadcast (to="all"/"broadcast") or an @all message, all
# 15 agents' watch.shes pick it up on their next poll. Without jitter, the 15 polls
# all complete within the same ~1s window (poll synchronization from a common spawn
# time) → 15 simultaneous Monitor notifications → 15 simultaneous Claude inference
# calls → server-side "temporarily limiting requests" rate-limit → freeze class.
# A one-shot startup jitter (uniform in [0, POLL)) decorrelates the cohort across
# the poll window — same total inference volume, ~8x lower simultaneous peak.
# Zero semantic change; ~half-poll-interval avg added to the worst-case inbox-to-
# inference latency, which is acceptable for fleet coordination (≤ 4s on POLL=8s).
sleep $((RANDOM % POLL))

while true; do
  touch "$HEARTBEAT_FILE" 2>/dev/null || true
  RESP=$(curl -sf "$BASE_URL&since=$LAST" || echo "[]")
  python3 - "$AGENT" "$LAST" <<'PY' "$RESP" || true
import json, sys
agent = sys.argv[1]
last = int(sys.argv[2])
raw = sys.argv[3] if len(sys.argv) > 3 else "[]"
try:
    msgs = json.loads(raw)
except Exception:
    msgs = []
new_last = last
for m in msgs:
    idx = m.get("index", -1)
    if idx <= last:
        continue
    new_last = max(new_last, idx)
    print(f"NEW_MSG [{m.get('ts','')}] <{m.get('from','?')}>: {m.get('body','')}", flush=True)
open("/tmp/watch_cursor_" + agent, "w").write(str(new_last))
PY
  if [[ -f "/tmp/watch_cursor_$AGENT" ]]; then
    LAST=$(cat "/tmp/watch_cursor_$AGENT")
  fi

  # Backlog #5a: detect bridge rotation. After rotation, indexes restart at 0,
  # so head_index = message_count_active - 1. If head < LAST, the cursor is now
  # ahead of the bridge head and we're permanently blind. Resync to -1.
  # Only probe on empty response to avoid extra traffic during active phases.
  if [[ "$RESP" == "[]" || -z "$RESP" ]]; then
    HEAD=$(curl -sf "$BRIDGE/health" \
           | python3 -c "import json,sys; h=json.load(sys.stdin); print(h.get('message_count_active',0)-1)" 2>/dev/null \
           || echo -1)
    # Atlas idx 1075 fix: reject HEAD=-1 (health-failure sentinel from line 104 fallback).
    # Previous regex `^-?[0-9]+$` accepted -1, so a transient /health blip (e.g. bridge
    # restart) was misread as rotation → cursor reset to -1 → next poll replayed entire
    # history as notifications (fleet-wide replay storm on every bridge restart). Tightened
    # to `^[0-9]+$` so only non-negative HEAD values are considered; real rotations have
    # HEAD>=0 (e.g. 4 after reset), health failures stay -1 and are correctly ignored.
    if [[ "$HEAD" =~ ^[0-9]+$ ]] && [[ "$LAST" -gt 0 ]] && [[ "$HEAD" -lt "$LAST" ]]; then
      echo "[watch] bridge rotation detected — head=$HEAD prev_cursor=$LAST; resyncing cursor to -1 + re-arming" >&2
      LAST=-1
      echo "-1" > "/tmp/watch_cursor_$AGENT"
    fi
  fi

  sleep "$POLL"
done
