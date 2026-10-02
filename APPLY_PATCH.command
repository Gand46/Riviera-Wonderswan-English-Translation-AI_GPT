#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ "$#" -ne 2 ]; then
  echo "Usage: ./APPLY_PATCH.command CLEAN_JP_ROM OUTPUT_ROM"
  exit 2
fi
python3 apply_patch.py "$1" "$2"
