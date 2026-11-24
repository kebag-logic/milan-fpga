#!/usr/bin/env python3
"""Run a clean parent and an isolated replacement-invalidation fault, concurrently."""
import argparse
import concurrent.futures
import json
import os
import re
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('checkout', type=Path)
p.add_argument('packet', type=Path)
p.add_argument('simulator', type=Path)
p.add_argument('--integration',action='store_true')
p.add_argument('--missing-talker',action='store_true')
a = p.parse_args()
root, packet = a.checkout.resolve(), a.packet.resolve()
scratch = packet / 'scratch/parent-probe'
scratch.mkdir(parents=True, exist_ok=True)
source = (root / 'hdl/milan/milan_datapath.sv').read_text()
old = 'else invalidate_r <= edit_change_w || direct_change_w || restore_change_w;'
new = '''else invalidate_r <= (edit_change_w
        && !(amap_in_store_r[amap_edit_in_key_w*8 + 7]
             && amap_edit_iclaim_word_r[amap_edit_in_key_w*8 + 7]))
        || direct_change_w || restore_change_w;'''
if a.integration:
    new = old.replace('edit_change_w', "1'b0")
if a.missing_talker:
    old = '.stream_en_i (aaf_stream_en_w),'
    new = ".stream_en_i (aaf_stream_en_w & N_STREAMS'(8'h7f)),"
assert source.count(old) == 1
faultdir=scratch/('missing-talker-fault' if a.missing_talker else
                  'integration-fault' if a.integration else 'replacement-fault')
faultdir.mkdir(exist_ok=True)
fault = faultdir / 'milan_datapath.sv'
fault.write_text(source.replace(old, new))
env = dict(os.environ, VERILATOR=str(a.simulator.resolve()), VERILATOR_JOBS='8',
           PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch))

def run(case):
    name, shape, plant = case
    command = [sys.executable, str(root/'tb/verilator/input_loopback_dp/run.py'),
               '--shape', str(shape), '--work', str(scratch/name)]
    if plant:
        command += ['--dp-source', str(fault)]
    raw = scratch / (name + '.log')
    with raw.open('w') as sink:
        result = subprocess.run(command, cwd=root, env=env, stdout=sink,
                                stderr=subprocess.STDOUT, timeout=600)
    text = raw.read_text().replace(str(root), '$CHECKOUT').replace(str(packet), '$PACKET')
    text = text.replace(str(a.simulator.resolve()), '$SIMULATOR')
    text = re.sub(r'/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff',
                  '$SIMULATOR_ROOT', text)
    (packet/'receipts'/f'{name}.log').write_text(text)
    (packet/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
    return dict(case=name, shape=shape, fault=plant, exit=result.returncode,
                runtime_pass='RESULT: PASS' in text,
                built=(scratch/name/'obj/parent_loopback').is_file())

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    cases=([('parent-control1',1,False),('parent-invalidation-fault8',8,True)] if a.integration
           else [('parent-control8',8,False),('parent-replacement-fault8',8,True)])
    if a.missing_talker:
        cases=[('parent-missing-talker7',8,True)]
    results = list(pool.map(run, cases))
name='integration-probe.json' if a.integration else 'parent-probe.json'
if a.missing_talker: name='missing-talker-probe.json'
(packet/'receipts'/name).write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results, indent=2))
