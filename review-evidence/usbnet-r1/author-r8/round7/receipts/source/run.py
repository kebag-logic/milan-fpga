import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path('$LANES/usbnet-1011')
SCRATCH = Path('$VALIDATION_STORAGE/usbnet-a855/round7')
PACKET = Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
PRIOR = PACKET.parent.parent / 'round5/receipts'
HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
MODE = sys.argv[1]
results = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(label, command, cwd=ROOT):
    assert shutil.disk_usage('/data').free >= 18_000_000_000
    assert int(subprocess.check_output(['du', '-s', '-B1', '$VALIDATION_STORAGE/usbnet-a855']).split()[0]) < 25_000_000_000
    started = time.monotonic()
    print('RUN', label, flush=True)
    log = PACKET / (label + '.log')
    with log.open('w') as stream:
        rc = subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT).returncode
    row = dict(label=label, command=command, cwd=str(cwd), head=HEAD, rc=rc,
               elapsed_seconds=time.monotonic()-started, log=log.name, sha256=sha(log))
    results.append(row)
    (PACKET / (MODE+'-commands.json')).write_text(json.dumps(results, indent=2)+'\n')
    print('RESULT', label, rc, flush=True)
    if rc:
        print(log.read_text()[-4000:], flush=True)
        raise SystemExit(rc)


if MODE in ('gates', 'gate45'):
    if MODE == 'gate45':
        os.environ['PATH'] = str(SCRATCH/'markdown-venv/bin')+':'+os.environ['PATH']
    import yaml
    workflow = ROOT / '.github/workflows/docs.yml'
    steps = yaml.safe_load(workflow.read_text())['jobs']['docs-gates-0']['steps']
    gates = [s for s in steps if s.get('id') in ('gate_31', 'gate_45')]
    assert len(gates) == 2
    (PACKET/'ci-gate-definitions.json').write_text(json.dumps(dict(workflow=str(workflow), sha256=sha(workflow), gates=gates), indent=2)+'\n')
    if MODE == 'gate45':
        gates = [s for s in gates if s['id'] == 'gate_45']
    for step in gates:
        run(step['id'], ['bash', '--noprofile', '--norc', '-eo', 'pipefail', '-c', step['run']])
elif MODE == 'setup':
    shutil.copy2(PACKET/'gate_45.log',PACKET/'gate_45-missing-dependency.log')
    run('markdown-venv', ['python3','-m','venv','--system-site-packages',str(SCRATCH/'markdown-venv')])
    run('markdown-install', [str(SCRATCH/'markdown-venv/bin/python3'),'-m','pip','install','--require-hashes','-r','tools/markdown/requirements.txt'])
elif MODE == 'usbnet':
    run('usbnet', ['make', '-C', 'tb/verilator/usbnet', 'OBJ='+str(SCRATCH/'usbnet'), 'JOBS=4'])
elif MODE == 'plants':
    os.environ['MUTANT_DIR'] = str(SCRATCH/'plants')
    run('plants', ['python3', '-B', 'tb/verilator/usbnet/mutants.py'])
    rows = []
    for path in sorted((SCRATCH/'plants').glob('*/run.log')):
        target = PACKET/'plants'/(path.parent.name+'.log')
        shutil.copy2(path, target)
        rows.append(dict(name=path.parent.name, log=str(target.relative_to(PACKET)), sha256=sha(target)))
    assert len(rows) == 72
    (PACKET/'plants/manifest.json').write_text(json.dumps(rows, indent=2)+'\n')
elif MODE == 'firmware':
    old_rows = json.loads((PACKET.parent.parent / 'round6/receipts/firmware-identity.json').read_text())
    rows = []
    for old in old_rows:
        recipe, tag = old['recipe'], old['tree']
        root = ROOT if tag == 'candidate' else SCRATCH/'baseline'
        out = SCRATCH/'product'/tag/recipe
        out.mkdir(parents=True, exist_ok=True)
        old_out = '$VALIDATION_STORAGE/usbnet-a855/round6/product/'+tag+'/'+recipe
        command = [a.replace(old_out,str(out)).replace('$VALIDATION_STORAGE/usbnet-a855/round5/baseline',str(root)).replace(str(ROOT),str(root)) for a in old['command']]
        generator = [a.replace(old_out,str(out)) for a in old['generator']]
        run('firmware-'+tag+'-'+recipe+'-map', generator, root)
        run('firmware-'+tag+'-'+recipe, command, root)
        hashes = {name:sha(out/name) for name in ('ctrl_app.elf','ctrl_plat_map_gen.h')}
        assert 'CTRL_PLAT_LEDS' not in (out/'ctrl_plat_map_gen.h').read_text()
        dest = PACKET/'firmware'/tag/recipe
        dest.mkdir(parents=True, exist_ok=True)
        for name in hashes:
            shutil.copy2(out/name,dest/name)
        rows.append(dict(recipe=recipe,tree=tag,head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),hashes=hashes,command=command,generator=generator))
        (PACKET/'firmware-identity.json').write_text(json.dumps(rows,indent=2)+'\n')
    for recipe in ('arty','ax7101','ax8x8'):
        for name in ('ctrl_app.elf','ctrl_plat_map_gen.h'):
            assert (PACKET/'firmware/candidate'/recipe/name).read_bytes() == (PACKET/'firmware/baseline'/recipe/name).read_bytes()
        print('CANDIDATE/BASELINE IDENTICAL', recipe, flush=True)
elif MODE == 'netlist':
    import difflib
    import re
    old = Path('$VALIDATION_STORAGE/usbnet-a855/round5/route/gen-final')
    command = json.loads(old.with_suffix('.command.json').read_text())
    assert '--build' not in command
    command[command.index('--output-dir')+1] = str(SCRATCH/'netlist')
    command[command.index('--ctrl-firmware')+1] = str(SCRATCH/'product/candidate/arty/ctrl_app.elf')
    run('netlist-generation',command)
    def normalized(text):
        pattern = r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/'
        return '\n'.join(line.rstrip() for line in re.sub(pattern,lambda m: m[0] if m[0].startswith('"') else '',text).splitlines() if line.strip())
    rows=[]
    for rel in ['gateware/digilent_arty.v','gateware/digilent_arty.xdc']:
        before,after = old/rel,SCRATCH/'netlist'/rel
        a,b=before.read_text(),after.read_text()
        (PACKET/(before.name+'.diff')).write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='round5/'+rel,tofile='round6/'+rel)))
        eq=normalized(a)==normalized(b) if rel.endswith('.v') else a==b
        rows.append(dict(file=rel,before_sha256=sha(before),after_sha256=sha(after),byte_identical=a==b,logic_identical=eq,normalized_sha256=hashlib.sha256(normalized(b).encode()).hexdigest()))
        assert eq, rel
    old_init={str(p.relative_to(old)):sha(p) for p in (old/'gateware').glob('*.init')}
    new_init={str(p.relative_to(SCRATCH/'netlist')):sha(p) for p in (SCRATCH/'netlist/gateware').glob('*.init')}
    assert old_init and old_init==new_init,(old_init,new_init)
    (PACKET/'netlist-identity.json').write_text(json.dumps(dict(head=HEAD,comparison='ddda29e1e28ec5b1a58786a750fd1f21b8f6c0d0',files=rows,initialization=old_init,reroute_required=False),indent=2)+'\n')
    print('NETLIST AND INITIALIZATION IDENTICAL',flush=True)
else:
    raise SystemExit('unknown mode')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip() == HEAD
# The measured input hashes bind the ongoing verification-only edits.
print('PASS', MODE, HEAD, datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
