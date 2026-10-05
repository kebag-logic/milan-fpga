#!/usr/bin/env python3
"""Plant only additional test stimulus in an isolated exact-head source copy."""
import argparse
import os
from pathlib import Path
import subprocess
import tarfile

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
a = p.parse_args()
packet = a.packet.resolve()
tree = packet / 'scratch/expanded'
tree.mkdir(parents=True, exist_ok=True)
with tarfile.open(packet / 'scratch/source.tar') as t:
    t.extractall(tree, filter='data')
f = tree / 'tb/srp_stream_fsms/sim_main.cpp'
text = f.read_text()
needle = '  void expiry_and_received_event_follow_table_10_4();'
assert text.count(needle) == 1
text = text.replace(needle, needle + '\n  void review_expanded_events();')
needle = 'int SrpStreamFsmsSuite::run() {'
assert text.count(needle) == 1
snippet = (packet / 'scripts/expanded_events.cpp').read_text()
text = text.replace(needle, snippet + '\n' + needle + '\n  review_expanded_events();')
f.write_text(text)
env = os.environ.copy()
env.update(VERILATOR=str(packet / 'scratch/bounded-simulator'),
           TMPDIR=str(packet / 'scratch'), MAKEFLAGS='-j16')
with (packet / 'receipts/expanded-events.log').open('w') as log:
    result = subprocess.run(['make', '-j16', '-C', 'tb/srp_stream_fsms', 'RUN_ARGS=suite'],
                            cwd=tree, env=env, stdout=log, stderr=subprocess.STDOUT)
(packet / 'receipts/expanded-events.rc').write_text(str(result.returncode) + '\n')
print('Expanded event probe rc=' + str(result.returncode))
raise SystemExit(result.returncode)
