#!/usr/bin/env python3
"""Reproduce the focused offset controls in disposable, registered clones."""
import concurrent.futures
import os
from pathlib import Path
import re
import subprocess
import sys

PACKET = Path(__file__).resolve().parent
HEAD = 'e5d8a71b6fa90352eca72314c7bd2275a1b20285'
HARNESS = Path('tb/verilator/gptp_shadow/sim_main.cpp')
BANK = Path('hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv')

def cmd(argv, cwd, log):
    result = subprocess.run(argv, cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
    return result.returncode

def replace(path, old, new):
    text = path.read_text()
    assert text.count(old) == 1, (path, old, text.count(old))
    path.write_text(text.replace(old, new))

def run_arm(source, simulator, name):
    work = PACKET / 'scratch' / name
    receipt = PACKET / 'receipts' / (name + '.log')
    with receipt.open('w') as log:
        assert cmd(['git', 'clone', '--quiet', '--shared', '--no-checkout', str(source), str(work)], source, log) == 0
        assert cmd(['git', 'checkout', '--quiet', '--detach', HEAD], work, log) == 0
        for sub in ('gptp-processor', 'third_party/verilog-axis'):
            assert cmd(['git', 'config', 'submodule.' + sub + '.url', str(source / sub)], work, log) == 0
        assert cmd(['git', '-c', 'protocol.file.allow=always', 'submodule', 'update', '--init', 'gptp-processor', 'third_party/verilog-axis'], work, log) == 0
        originals = {path: (work / path).read_bytes() for path in (HARNESS, BANK)}
        try:
            replace(work / HARNESS, '    const int32_t after = static_cast<int32_t>(dut->pub_offset_o);\n',
                    '    const int32_t after = static_cast<int32_t>(dut->pub_offset_o);\n'
                    '    printf("OFFSET delay=%lld before=%d after=%d delta=%lld\\n", static_cast<long long>(d), before, after, static_cast<long long>(after) - before);\n')
            pair = '    gm_pair(m, D_NOM - used_delay(d) + kGradedOffsetNs);\n'
            if name == 'unsent-pair':
                replace(work / HARNESS, pair, '')
            elif name == 'stale-bank':
                replace(work / BANK, '        pub_offset_o    <= pub_offset_raw_w;\n', '        pub_offset_o    <= pub_offset_o;\n')
            elif name == 'unsent-follow-up':
                replace(work / HARNESS, '  void gm_pair(const ModelGm &m, int64_t extra_ns = 0) {\n',
                        '  bool omit_graded_follow_up = false;\n  void gm_pair(const ModelGm &m, int64_t extra_ns = 0) {\n')
                replace(work / HARNESS, '    Frame g = follow_up(seq, origin + static_cast<uint64_t>(D_NOM + extra_ns));\n    send_wide(g.b);\n',
                        '    Frame g = follow_up(seq, origin + static_cast<uint64_t>(D_NOM + extra_ns));\n    if (!omit_graded_follow_up) send_wide(g.b);\n')
                replace(work / HARNESS, pair, '    omit_graded_follow_up = true;\n' + pair + '    omit_graded_follow_up = false;\n')
            assert cmd([simulator, '--version'], work, log) == 0
            status = cmd(['make', '-j16', 'run', 'VERILATOR=' + simulator, 'VERILATOR_JOBS=4'], work / HARNESS.parent, log)
            (PACKET / 'receipts' / (name + '.rc')).write_text(str(status) + '\n')
        finally:
            for path, data in originals.items():
                (work / path).write_bytes(data)
    text = receipt.read_text()
    tally = re.findall(r'^(\d+) checks: (\d+) PASS, (\d+) FAIL$', text, re.M)
    assert tally, (name, 'no completed tally')
    if name == 'clean':
        assert status == 0 and tally[-1] == ('490', '490', '0'), (name, status, tally)
    else:
        assert status != 0 and int(tally[-1][2]) > 0, (name, status, tally)
        for delay in (-3, -80, -81, -263, -801, -5000000):
            for check in ('the graded Follow_Up is used: its offset is fresh', 'its offset uses the delay floored at -800 ns'):
                assert f'FAIL #109 {delay} ns: {check}' in text, (name, delay, check)
    return name + ': ' + str(tally[-1]) + ', rc=' + str(status)

def main():
    source = Path(sys.argv[1]).resolve()
    simulator = str(Path(sys.argv[2]).resolve())
    (PACKET / 'receipts').mkdir(exist_ok=True)
    (PACKET / 'scratch').mkdir(exist_ok=True)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run_arm, source, simulator, name) for name in
                   ('clean', 'unsent-pair', 'stale-bank', 'unsent-follow-up')]
        results = [future.result() for future in futures]
    (PACKET / 'receipts' / 'probe-summary.txt').write_text('\n'.join(results) + '\n')
    print('\n'.join(results))

if __name__ == '__main__':
    main()
