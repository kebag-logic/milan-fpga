#!/usr/bin/env python3
"""Independent focused PP stale-number reproduction; no source changes.

Run: rtk proxy python3 independent_pp.py CHECKOUT OUTPUT_DIRECTORY
Uses the unmodified driver and native tools. The local Python shim changes
only generated ucode.hex; a labelled fault arm freezes just the ROM digest.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

SHIM = r'''
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
args = sys.argv[1:]
real = os.environ['R247_REAL_PYTHON']
folder = Path(os.environ['R247_ARTIFACTS'])
name = Path(args[0]).name if args else ''
def event(data):
    with (folder / 'events.jsonl').open('a') as f: f.write(json.dumps(data) + '\n')
if name in ('gen_ltn_rom.py', 'gen_ucode.py', 'gen_gptp_ucode.py'):
    p = subprocess.run([real, *args])
    if p.returncode: sys.exit(p.returncode)
    dest = Path(args[args.index('-o') + 1])
    if dest.name == 'ucode.hex' and os.environ.get('R247_CHANGE') == '1':
        dest.write_bytes(b'INVALID_ROM_DATA\n')
    shutil.copyfile(dest, folder / dest.name)
    event({'generator': name, 'image': dest.name, 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()})
    sys.exit(0)
if name == 'result_cache.py':
    if args[1] == 'rom-digest':
        p = subprocess.run([real, *args], capture_output=True, text=True)
        value = os.environ.get('R247_FROZEN_DIGEST', p.stdout.strip())
        event({'operation':'rom-digest', 'actual':p.stdout.strip(), 'effective':value, 'exit':p.returncode})
        sys.stdout.write(value + '\n'); sys.stderr.write(p.stderr); sys.exit(p.returncode)
    if args[1] in ('lookup', 'store'):
        fields = dict(zip(args[2::2], args[3::2]))
        staged = Path(fields['--sv2v-file'])
        shutil.copyfile(staged, folder / staged.name)
        event({'operation':args[1], 'fields':fields, 'sv2v_sha256':hashlib.sha256(staged.read_bytes()).hexdigest()})
if args and args[0] == '-' and len(args) == 2 and args[1].endswith('.stat.json'):
    stat = Path(args[1])
    if stat.exists():
        shutil.copyfile(stat, folder / stat.name)
        verilog = stat.with_name(stat.name.replace('.stat.json', '.v'))
        shutil.copyfile(verilog, folder / verilog.name)
os.execv(real, [real, *args])
'''

def inventory(path):
    return {str(p.relative_to(path)): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mode & 0o777)
            for p in path.rglob('*') if p.is_file()}

def identities(row, op):
    answer = []
    for event in row['events']:
        if event.get('operation') == op:
            fields = dict(event['fields'])
            for flag in ('--dir', '--seed', '--sv2v-file', '--cells', '--stat-json'):
                fields.pop(flag, None)
            fields['sv2v_sha256'] = event['sv2v_sha256']
            answer.append(fields)
    return answer

def main():
    root, work = map(lambda s: Path(s).resolve(), sys.argv[1:])
    work.mkdir(parents=True)
    bindir = work / 'bin'; bindir.mkdir()
    shim = bindir / 'python3'; shim.write_text('#!' + sys.executable + '\n' + SHIM); shim.chmod(0o755)
    head = work / 'head'
    rows = []
    def run(label, flags, change=False, frozen=None):
        folder = work / label; folder.mkdir()
        env = dict(os.environ, PATH=str(bindir) + ':' + os.environ['PATH'],
                   R247_REAL_PYTHON=sys.executable, R247_ARTIFACTS=str(folder),
                   R247_CHANGE=str(int(change)), PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='1')
        if frozen: env['R247_FROZEN_DIGEST'] = frozen
        cmd = ['rtk', 'proxy', 'bash', str(root / 'syn/yosys/run.sh'), '--top', 'KL_pp_shadow',
               '--no-structural', '--results', str(folder / 'results'), *flags]
        start = time.monotonic()
        with (folder / 'stdout').open('w') as stdout, (folder / 'stderr').open('w') as stderr:
            proc = subprocess.run(cmd, cwd=root, env=env, stdout=stdout, stderr=stderr)
        output = (folder / 'stdout').read_text() + (folder / 'stderr').read_text()
        match = re.search(r'\[PASS\]\s+KL_pp_shadow\s+cells=(\d+)', output)
        row = {'label':label, 'command':cmd, 'changed':change, 'frozen':frozen, 'exit':proc.returncode,
               'seconds':round(time.monotonic()-start,3), 'cells':int(match[1]) if match else None,
               'hit':'(result cache)' in output,
               'events':[json.loads(line) for line in (folder/'events.jsonl').read_text().splitlines()]}
        (folder / 'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
        rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k not in ('command','events')}), flush=True)
        assert row['exit'] == 0 and row['cells'] is not None, output
        return row
    cold = run('01-cold', ['--cache',str(head)])
    assert not cold['hit'] and identities(cold,'lookup') == identities(cold,'store')
    warm = run('02-warm', ['--cache',str(head)])
    assert warm['hit'] and warm['cells']==cold['cells']
    seed = work / 'seed'; shutil.copytree(head, seed)
    for p in [seed, *seed.rglob('*')]: p.chmod(p.stat().st_mode & ~0o222)
    before = inventory(seed)
    seeded = run('03-seed', ['--cache-seed',str(seed)])
    assert seeded['hit'] and seeded['cells']==cold['cells']
    frozen = identities(cold,'lookup')[0]['--rom-sha256']
    mutant = run('04-fault-frozen-digest', ['--cache-seed',str(seed)], True, frozen)
    assert mutant['hit'] and mutant['cells']==cold['cells']
    changed = run('05-changed', ['--cache',str(head),'--cache-seed',str(seed)], True)
    assert not changed['hit'] and changed['cells'] != cold['cells']
    assert identities(changed,'lookup') == identities(changed,'store')
    left, right = identities(cold,'lookup')[0], identities(changed,'lookup')[0]
    assert {k for k in left if left[k]!=right[k]} == {'--rom-sha256'}
    changed_warm = run('06-changed-warm', ['--cache',str(head),'--cache-seed',str(seed)], True)
    assert changed_warm['hit'] and changed_warm['cells']==changed['cells']
    uncached = run('07-changed-uncached', [], True)
    assert not uncached['hit'] and uncached['cells']==changed['cells']
    assert inventory(seed)==before
    for label in ('01-cold','05-changed','07-changed-uncached'):
        row = next(r for r in rows if r['label']==label)
        assert json.loads((work/label/'KL_pp_shadow.stat.json').read_text())['design']['num_cells']==row['cells']
    assert (work/'05-changed/KL_pp_shadow.v').read_bytes()==(work/'07-changed-uncached/KL_pp_shadow.v').read_bytes()
    assert (work/'01-cold/KL_pp_shadow.v').read_bytes()==(work/'05-changed/KL_pp_shadow.v').read_bytes()
    for label in ('02-warm','03-seed'):
        assert (work/label/'results/top-KL_pp_shadow.result').read_bytes()==(work/'01-cold/results/top-KL_pp_shadow.result').read_bytes()
    for label in ('06-changed-warm','07-changed-uncached'):
        assert (work/label/'results/top-KL_pp_shadow.result').read_bytes()==(work/'05-changed/results/top-KL_pp_shadow.result').read_bytes()
    (work/'complete.json').write_text(json.dumps({'result':'PASS','rows':rows,'readonly_seed_unchanged':True},indent=2)+'\n')

if __name__ == '__main__': main()
