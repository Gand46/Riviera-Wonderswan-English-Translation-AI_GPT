#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ "$#" -lt 1 ]; then
  echo "Usage: ./BUILD.command CLEAN_JP_ROM [OUTPUT_ROM]"
  exit 2
fi
python3 build.py "$@"
