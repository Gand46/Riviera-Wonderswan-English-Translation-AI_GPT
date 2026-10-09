#!/usr/bin/env python3
"""Portable bounded RC6/RC7 credit replay; requires user-provided Mesen/ROMs."""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, os, subprocess, time

def main():
    script_dir = Path(__file__).resolve().parent
    root = script_dir.parents[1]
    p = argparse.ArgumentParser()
    p.add_argument('--base-rom', type=Path, required=True)
    p.add_argument('--target-rom', type=Path, required=True)
    p.add_argument('--emulator', type=Path, required=True)
    p.add_argument('--state', type=Path, default=root/'validation/S460/final_routes/final_route0_full/chunk2/checkpoint_02000.mss')
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    state, em, out_root = a.state.resolve(), a.emulator.resolve(), a.out.resolve()
    def run(job):
        version, rom_path, expected = job
        rom = rom_path.resolve()
        digest = hashlib.sha256(rom.read_bytes()).hexdigest()
        assert digest == expected, version+' ROM mismatch'
        out = out_root/version
        out.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, QA_OUT=str(out), QA_STATE=str(state))
        lib = Path('/usr/lib/x86_64-linux-gnu/libstdc++.so.6')
        if os.name == 'posix' and lib.exists():
            env['LD_PRELOAD'] = str(lib)
        cmd = [str(em), '--testRunner', '--timeout=40', '--enableStdout',
               '--doNotSaveSettings', '--debug.scriptWindow.allowIoOsAccess=true',
               str(script_dir/'credit_qa.lua'), str(rom)]
        start = time.monotonic()
        with (out/'mesen.log').open('w') as log:
            rc = subprocess.run(cmd, cwd=em.parent, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=50).returncode
        report = {'version': version, 'exit': rc, 'seconds': time.monotonic()-start,
                  'rom_sha256': digest, 'source_state_sha256': hashlib.sha256(state.read_bytes()).hexdigest(),
                  'command': cmd, 'access_method': 'SAVESTATE',
                  'source_origin': 'S460 synthetic ending', 'rom_writes': 0}
        (out/'RUN.json').write_text(json.dumps(report, indent=2)+'\n')
        return report
    jobs = [('S462_RC6_build', a.base_rom, 'b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204'),
            ('S463_RC7', a.target_rom, '933cfcd5ea40f0f1d960338e78dc60ead6d8e5c280ea28bc69007f55ed2cc7aa')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        reports = list(pool.map(run, jobs))
    (out_root/'CREDIT_RUNS.json').write_text(json.dumps(reports, indent=2)+'\n')
    print(json.dumps(reports, indent=2))
    assert all(r['exit'] == 0 for r in reports)

if __name__ == '__main__':
    main()
