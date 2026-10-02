#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ "$#" -lt 1 ]; then
  echo "Uso: ./BUILD.command ROM_JP_LIMPIA.wsc [SALIDA_RC5.wsc]"
  exit 2
fi
output="${2:-build/Riviera_EN_v0.114_S461_RC5.wsc}"
exec python3 build_rc5.py "$1" --out "$output"
