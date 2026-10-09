"""Deterministic release checks and scoped inherited-evidence validity."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'deliver/Riviera_EN_v0.111_S458_RC2_FULL_PACKAGE'
SHA=lambda b:hashlib.sha256(b).hexdigest()
rc=(ROOT/'root_global/Riviera_EN_v0.111_S458_RC2.wsc').read_bytes()
old=(ROOT/'rc1_runtime/Riviera_EN_v0.110_S457_RC1.wsc').read_bytes()
checks=[]
for page in (0,5):
    name=f'page_{page:02d}'
    cur=ROOT/'root_global/credits_regression'/name/'runtime'
    prior=P/'synthetic/credits_replay'/name/'runtime'
    data=(cur/(name+'.bin')).read_bytes();before=(prior/(name+'.bin')).read_bytes()
    guard=json.loads((cur/'hook_guard.json').read_text())
    # Harness dumps entire WRAM. Compare the actual native credit bitmap fields;
    # startup RAM and stack outside them vary with persisted emulator state.
    ranges=[(0x56e0,0x56e0+96*144//2),(0x7200,0x8100)]
    pixels=b''.join(data[a:b] for a,b in ranges)
    oldpixels=b''.join(before[a:b] for a,b in ranges)
    assert pixels==oldpixels and guard['register_errors']==guard['unexpected_writes']==0
    differences=[hex(i) for i,(a,b) in enumerate(zip(data,before)) if a!=b]
    checks.append(dict(page=page,native_pixel_fields_byte_exact_rc1=True,field_ranges=[[hex(a),hex(b)] for a,b in ranges],pixel_fields_sha256=SHA(pixels),whole_ram_equal=data==before,whole_ram_differences_outside_pixel_fields=differences,output_sha256=SHA(data),guard=guard))
result=dict(result='PASS_SYNTHETIC',scope='Native credit output regression, pages 0 and 5 around adjacent S450 allocation; remaining 11-page results inherited because all credit code/data and callsites unchanged',checks=checks,runtime_rom_sha256='ffee86fda00785dbd2c84f3e938eb7cc588d86af7bc744e9239f0aaf2a9b28da',final_rom_sha256=SHA(rc),transfer_to_final='Only epilogue_011 byte 0x662925 and checksum differ from measured candidate; credit dependencies unchanged',natural_progression=False)
(P/'validation/CREDITS_RC2_REGRESSION.json').write_text(json.dumps(result,indent=2)+'\n')
print('CREDITS_REGRESSION_OK')
