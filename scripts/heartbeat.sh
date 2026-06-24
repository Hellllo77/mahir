#!/usr/bin/env bash
# Posts a heartbeat to the bridge every N seconds to assert agent liveness.
#
# Usage:
#   ./scripts/heartbeat.sh --for quinn-pm-command-center-hq --interval 30

set -euo pipefail

BRIDGE="${BRIDGE_URL:-http://127.0.0.1:8767}"
AGENT=""
INTERVAL=30

while [[ $# -gt 0 ]]; do
  case "$1" in
    --for) AGENT="$2"; shift 2 ;;
    --interval) INTERVAL="$2"; shift 2 ;;
    --bridge) BRIDGE="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

if [[ -z "$AGENT" ]]; then
  echo "Usage: $0 --for <agent> [--interval seconds]"
  exit 2
fi

echo "[heartbeat] agent=$AGENT interval=${INTERVAL}s bridge=$BRIDGE"

while true; do
  curl -sf -X POST "$BRIDGE/heartbeat" \
    -H "Content-Type: application/json" \
    -d "{\"agent\": \"$AGENT\"}" >/dev/null 2>&1 || true
  sleep "$INTERVAL"
done
