#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys

if len(sys.argv) != 3:
    raise SystemExit("Uso: python3 apply_patch.py ROM_JP_LIMPIA.wsc SALIDA_RC5.wsc")
root=Path(__file__).resolve().parent
vendor=root/'sources/Riviera_S457_FULL_SOURCE/scripts/vendor'
sys.path.insert(0,str(vendor))
from ws_patch_tools import bps

source_path=Path(sys.argv[1]);output_path=Path(sys.argv[2])
source=source_path.read_bytes()
source_sha=hashlib.sha256(source).hexdigest()
expected_source='62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921'
expected_target='2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf'
if source_sha!=expected_source:raise SystemExit(f'ROM fuente incorrecta: {source_sha}')
patch=(root/'patches/Riviera_EN_v0.114_S461_RC5_CUMULATIVE_FROM_JP.bps').read_bytes()
target=bps.apply(source,patch)
target_sha=hashlib.sha256(target).hexdigest()
if target_sha!=expected_target:raise SystemExit(f'Salida inesperada: {target_sha}')
output_path.parent.mkdir(parents=True,exist_ok=True);output_path.write_bytes(target)
print('OK',target_sha)
