#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 3 ]]; then
  echo "Usage: $0 /path/to/Mesen /path/to/rom.wsc /path/to/script.lua [timeout]" >&2
  exit 2
fi
MESEN=$(realpath "$1")
ROM=$(realpath "$2")
LUA=$(realpath "$3")
TIMEOUT=${4:-30}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
source "$ROOT/scripts/mesen_runtime_env.sh"
DIR=$(dirname "$MESEN")
[[ -f "$DIR/settings.json" ]] || printf '{}\n' > "$DIR/settings.json"
cd "$DIR"
exec "$MESEN" --testRunner "--timeout=$TIMEOUT" --enableStdout --doNotSaveSettings \
  --debug.scriptWindow.allowIoOsAccess=true \
  "$LUA" "$ROM"
