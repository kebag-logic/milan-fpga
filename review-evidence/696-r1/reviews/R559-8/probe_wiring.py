#!/usr/bin/env python3
"""Build disposable integration wiring faults and require named rejections."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--compiler', required=True, type=Path)
    parser.add_argument('--jobs', type=int, default=3)
    args = parser.parse_args()
    assert 1 <= args.jobs <= 3
    root = args.source.resolve()
    packet = Path(__file__).resolve().parent
    work = packet / 'scratch' / 'wiring-probes'
    work.mkdir(exist_ok=True)
    env = dict(os.environ, TMPDIR=str(packet / 'scratch'), VERILATOR=str(args.compiler), VERILATOR_JOBS='2', PYTHONDONTWRITEBYTECODE='1')
    original = (root / 'hdl/milan/milan_datapath.sv').read_text()
    suite = root / 'tb/verilator/maap'
    listed = subprocess.check_output(['make', '-s', '--no-print-directory', '-C', str(root / 'tb/verilator/milan_dp'), 'print-srcs'], env=env, text=True).strip()
    target = '../../../hdl/milan/milan_datapath.sv'
    assert listed.split().count(target) == 1
    probes = [
        ('drop-link', '    .port_operational_i (eff_link_w),\n', '', 'M5 datapath: link return starts four fresh PROBEs'),
        ('tie-link-high', '.port_operational_i (eff_link_w)', ".port_operational_i (1'b1)", 'M5 datapath: link return starts four fresh PROBEs'),
        ('drop-clock', '    .realtime_ns_i     (ptp_now_w[31:0]),\n', '', 'M3 datapath: real-time clock changes probe intervals'),
    ]
    def run(probe):
        name, before, after, check = probe
        assert original.count(before) == 1
        rtl = work / (name + '.sv')
        rtl.write_text(original.replace(before, after))
        mdir = work / ('obj_' + name)
        argv = ['make', '-j16', '-f', 'integration.mk', 'build', f'DP_MDIR={mdir}',
                'VERILATOR_JOBS=2', f'VERILATOR={args.compiler}', 'SRCS=' + listed.replace(target, str(rtl))]
        with (packet / ('wiring-' + name + '-build.log')).open('w') as log:
            result = subprocess.run(argv, cwd=suite, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
        build_rc = result.returncode
        run_rc = None
        output = ''
        if build_rc == 0:
            result = subprocess.run([str(mdir / 'maap_integration')], cwd=mdir, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
            run_rc, output = result.returncode, result.stdout
        (packet / ('wiring-' + name + '-run.log')).write_text(output)
        killed = build_rc == 0 and run_rc == 1 and '[FAIL] ' + check in output
        row = {'probe': name, 'build_rc': build_rc, 'run_rc': run_rc, 'required_check': check, 'killed': killed}
        print(json.dumps(row), flush=True)
        return row
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rows = list(pool.map(run, probes))
    (packet / 'wiring-results.json').write_text(json.dumps(rows, indent=2) + '\n')
    return int(any(not row['killed'] for row in rows))

if __name__ == '__main__':
    raise SystemExit(main())
