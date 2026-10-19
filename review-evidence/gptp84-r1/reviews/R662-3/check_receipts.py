#!/usr/bin/env python3
"""Audit named mutation receipts and apply adoption patches in disposable files."""
import ast
import base64
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
ev = packet / "evidence/author-r2/receipts/round2"
syntax = ast.parse((root / "tb/verilator/engine/mutants.py").read_text())
env = {"GENERATOR": "ucode/gen_gptp_ucode.py", "P1_PREFIX": "p1 255 "}
node = next(n.value for n in syntax.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "MUTATIONS" for t in n.targets))
mutations = eval(compile(ast.Expression(node), "mutations", "eval"), {"__builtins__": {}}, env)
assert len(mutations) == 72
named = 0
for i, (name, file, old, new, breaks) in enumerate(mutations):
    assert (root / "hdl" / file).read_text().count(old) == 1, name
    log = (ev / f"lane-head-2022d363/engine-mutants/mut-{i // 3}.log").read_text()
    end = log.index('[PASS] mutant caught: ' + name + ' - breaks')
    start = log.rfind('[PASS]', 0, end)
    section = log[start:end]
    if breaks.startswith(("#82 ", "#84 ", "#85 ", "p1 255 ")):
        for label in breaks.split(" | "):
            assert any(line.startswith('FAIL ' + label + ' ') for line in section.splitlines()), (name, label)
            named += 1
for i in range(24):
    log = (ev / f"lane-head-2022d363/engine-mutants/mut-{i}.log").read_text()
    assert '[PASS] the unmutated engine still passes the harness' in log
    assert '4 checks: 4 PASS, 0 FAIL' in log
print(f"72/72 source mutation patterns unique; 72 caught receipts; 24 positive controls; {named} mandatory named failures verified.")

base = "e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f"
files = ['tb/verilator/gptp_shadow/sim_main.cpp', 'tb/verilator/milan_dp/sim_gptp.cpp', 'tb/verilator/milan_dp/sim_ax1x1gptp.cpp']
scratch = packet / "scratch/adoption"
scratch.mkdir(parents=True, exist_ok=True)
for name in files:
    saved = packet / "authorities" / name
    if not saved.exists():
        data = json.loads(subprocess.check_output(['gh', 'api', f'repos/kebag-logic/milan-fpga/contents/{name}?ref={base}']))
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(base64.b64decode(data['content']))
    dest = scratch / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(saved, dest)
patches = ['parent-adoption-gptp_shadow-85.patch', 'parent-adoption-milan_dp-85.patch', 'parent-adoption-milan_dp-82.patch', 'parent-adoption-milan_dp_gptp-84.patch']
for name in patches:
    path = packet / "evidence/author-r3" / name
    subprocess.run(['git', 'apply', '--check', str(path)], cwd=scratch, check=True)
    subprocess.run(['git', 'apply', str(path)], cwd=scratch, check=True)
    print('Applies in order: ' + name + '; sha256=' + hashlib.sha256(path.read_bytes()).hexdigest())
for name in files:
    print('Adopted file: ' + name + '; sha256=' + hashlib.sha256((scratch / name).read_bytes()).hexdigest())

saved = packet / "public/parent-base-tree.json"
if not saved.exists():
    saved.write_bytes(subprocess.check_output(['gh','api',f'repos/kebag-logic/milan-fpga/git/trees/{base}?recursive=1']))
tree = json.loads(saved.read_text())['tree']
links = {x['path']: x['sha'] for x in tree if x['mode'] == '160000'}
links['gptp-processor'] = '2022d363fc622f6bbf4c312239fc3db741b4d29a'
snapshots = (ev / 'snapshots.txt').read_text().split('## submodules of the adoption E checkouts')[1]
for path, oid in sorted(links.items()):
    assert oid + ' ' + path + ' ' in snapshots, path
    print('Author adoption dependency matches public base plus donor advance: ' + path + '=' + oid)
print(f'{len(links)} recorded adoption gitlinks checked. This is receipt validation, not a manager bank execution.')

def strip_comments(src):
    return re.sub(r'\s+', '', re.sub(r'/\*.*?\*/|//[^\n]*', '', src, flags=re.S))
current = (root / 'hdl/top/KL_gptp_engine.sv').read_text()
old = subprocess.check_output(['git','-C',str(root),'show','43acfbcc:hdl/top/KL_gptp_engine.sv']).decode()
def declaration(src):
    return strip_comments(src[src.index('module KL_gptp_engine'):src.index(');', src.index('module KL_gptp_engine')) + 2])
assert declaration(current) == declaration(old)
print('Public module declaration, ports and parameters unchanged from 43acfbcc after comment removal.')
