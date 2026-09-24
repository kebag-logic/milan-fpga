"""Run the actual licence scenario against two temporary RTL mutations.

Usage: python3 bdd_mutants.py <repository> <evidence-directory>
No other reader/build may use the datapath while this probe runs.
Only the gate assignment changes; its exact original bytes are restored.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
datapath = root / 'hdl/milan/milan_datapath.sv'
original = datapath.read_bytes()
source = original.decode()
pattern = ('  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n'
           '                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];')
assert source.count(pattern) == 1
command = ['behave', '--no-capture', '-f', 'plain', '-n', 'the stream gate requires',
           'features/milan_streaming_licence.feature']

def scenario(name):
    result = subprocess.run(command, cwd=root / 'tests', capture_output=True,
                            text=True, timeout=300, check=False)
    text = result.stdout + result.stderr
    (out / (name + '.log')).write_text(text)
    print(name, 'rc', result.returncode)
    return result.returncode, text

try:
    rc, log = scenario('bdd_clean_before')
    assert rc == 0 and '1 scenario passed' in log
    for name, term in [('bdd_active_only', 'pp_cd_srp_active_w'),
                       ('bdd_raw_grant_only', 'pp_cd_srp_sr_admitted_w')]:
        replacement = '  assign lwsrp_stream_gate = ' + term + '[SRP_TALKERS_C-1:0];'
        datapath.write_text(source.replace(pattern, replacement))
        rc, log = scenario(name)
        assert rc == 1, log
        assert ('ASSERT FAILED: lwsrp_stream_gate must be ACTIVE AND '
                'the per-source real grant and nothing else') in log, log
        assert '0 scenarios passed, 1 failed' in log, log
        print('CAUGHT: exact gate-composition assertion')
finally:
    datapath.write_bytes(original)
assert datapath.read_bytes() == original
rc, log = scenario('bdd_clean_after')
assert rc == 0 and '1 scenario passed' in log
print('PASS: both mutants fail the actual scenario; clean controls pass; RTL restored')
