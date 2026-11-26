#!/usr/bin/env python3
"""Read-only packet audit. Usage: audit_packet.py SOURCE PACKET_ROOT."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

source, packet = map(lambda s: Path(s).resolve(), sys.argv[1:])
head = '079c4fa1514be460949ddc28ae3277ea1873cb48'
tree = 'be2122cbd487361b4ed8a99ff283565c1bec3eb2'
evidence = 'e2d4a1d3ca42c07812cb2112446eb6b8c73120ef'

def git(*args, root=source):
    return subprocess.check_output(['git', '-C', str(root), *args])

def sha(data):
    return hashlib.sha256(data).hexdigest()

def bytes_and_index(root, revision):
    entries = git('ls-tree', '-rz', '--full-tree', revision, root=root).split(b'\0')
    index = {}
    for row in git('ls-files', '--stage', '-z', root=root).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, oid, stage = meta.split()
            assert stage == b'0', path
            index[path] = (mode, oid)
    files, links = 0, {}
    expected = {}
    for row in entries:
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid = meta.split()
        expected[name] = (mode, oid)
        path = root / os.fsdecode(name)
        if kind == b'commit':
            links[os.fsdecode(name)] = oid.decode()
            continue
        st = path.lstat()
        actual_mode = b'120000' if stat.S_ISLNK(st.st_mode) else (b'100755' if st.st_mode & 0o111 else b'100644')
        data = os.fsencode(os.readlink(path)) if stat.S_ISLNK(st.st_mode) else path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest().encode()
        assert (actual_mode, actual) == (mode, oid), name
        files += 1
    assert index == expected, 'index differs from exact tree'
    print(f'BYTES {root.name if root != source else "source"}: {files} blobs, modes and index equal {revision}')
    return links

assert git('rev-parse', 'HEAD').decode().strip() == head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == tree
links = bytes_and_index(source, head)
for name in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis', 'third_party/tsn-c-stack', 'third_party/lwSRP'):
    sub = source / name
    assert (sub / '.git').exists() and not sub.is_symlink()
    assert git('rev-parse', 'HEAD', root=sub).decode().strip() == links[name]
    bytes_and_index(sub, links[name])
    print(f'GITLINK {name} {links[name]}')

changed = git('diff', '--name-only', '85569e24', head).decode().splitlines()
assert changed == ['sw/firmware/ctrl_nvm/nvm_store.h']
before = git('show', '85569e24:sw/firmware/ctrl_nvm/nvm_store.h')
after = (source / changed[0]).read_bytes()
strip_comments = lambda b: re.sub(rb'/\*.*?\*/|//[^\n]*', b'', b, flags=re.S)
assert strip_comments(before) == strip_comments(after)
print('DELTA one file; comment-stripped bytes identical; no executable or gitlink delta')

for round_name in ('p1win-r1', 'p1win-r2'):
    root = packet / 'scratch/review-evidence' / round_name
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    count = 0
    for row in manifest:
        if not row['file'].startswith('author/'):
            continue
        data = (root / row['file']).read_bytes()
        assert sha(data) == row['published_sha256'], row['file']
        committed = git('show', f'{evidence}:review-evidence/{round_name}/{row["file"]}')
        assert committed == data, row['file']
        count += 1
    print(f'PACKET {round_name}: {count} author files match published SHA256 and pinned commit')
root = packet / 'scratch/review-evidence/p1win-r2/author'
for line in (root / 'MANIFEST.txt').read_text().splitlines():
    digest, filename = line.split(None, 1)
    assert sha((root / filename.strip()).read_bytes()) == digest
print('AUTHOR MANIFEST all entries match')
print('SIGNATURE: archive commit has no signature; integrity verified by immutable commit and SHA256, not signer authentication')
gates = sorted((root / 'receipts').glob('gate-*.txt'))
for gate in gates:
    text = gate.read_text()
    assert text.startswith(f'head {head} tree {tree} status-entries 0')
    assert 'rc 0 status-entries 0' in text or ('rc=0' in text and 'status-entries after 0' in text)
print(f'GATE RECEIPTS {len(gates)} exact-head clean-checkout records with successful exits')

sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
sys.path.insert(0, str(source / 'scripts'))
import bind_save
import egress_ledger
import run

for point in ('1x1', '8x8-1if'):
    prefix = root / 'full-run' / point
    ident = prefix.with_name(point + '-identity.txt').read_text()
    assert f'head {head}\ntree {tree}\nstatus entries 0' in ident
    assert 'rc 0\nstatus entries after 0' in ident
    data = prefix.with_name(point + '-results.json').read_bytes()
    table = prefix.with_name(point + '-table.md').read_bytes()
    assert sha(data) in ident and sha(table) in ident
    d = json.loads(data)
    assert run.counts(d['results']) == d['counts']
    assert run.table(d['results'], point, d['clock']['label']).strip() == table.decode().strip()
    print(f'TABLE {point}: regenerated table and counts match published results')
    assert f'sha256 native/Vsim {d["build"]}' in ident
    assert f'build.json executable_sha256 {d["build"]}' in ident
    assert len(d['results']) == len({r['group'] for r in d['results']}) == 113
    assert not d['refusals'] and not d['save_misses'] and not d['notice_misses']
    assert not bind_save.late(d['results'])
    probes = [(g['group'], p) for g in d['results'] for p in g['probes'] if p['status'] == 'measured']
    misses = [(g,p) for g,p in probes if not p['within_budget']]
    assert len(misses) == 7 and all(g == 'backlog-owed' for g,p in misses)
    print(f'RUN {point}: 113 unique groups; {len(probes)} measurements; seven held-egress misses; no refusals or save misses')
    for family in ('acmp', 'notify', 'srp'):
        selected = [p['ms'] for g,p in probes if g != 'backlog-owed' and p['family'] == family]
        print(f'FAMILY {point} {family} max_ms={max(selected):.5f}')
    over = [(g['group'],g['passes']['share']['over'],g['passes']['worst']['ms']) for g in d['results'] if g['passes']['share']['over']]
    print(f'SHARE {point}: {over}')
    print('FIRMWARE', point, re.search(r'sha256 image/ctrl_app.elf (\w+)', ident)[1])
    print(f'STEPS {point}: pass_max_ms={max(g["passes"]["steps"]["ms"] for g in d["results"]):.5f}, store_max_ms={max(g["passes"]["steps"]["store_ms"] for g in d["results"]):.5f}')
    for g in d['results']:
        if g.get('bind') and g['group'] in ('save-bind','save-bind-burst','save-bind-in-capture'):
            b=g['bind']
            print(f'BIND {point} {g["group"]} max_ms={b["worst_ms"]} saves={b["saves"]} erases={b["erases"]}')
        if g['group'] in ('save-flight','save-burst'):
            print(f'OTHER {point} {g["group"]} max_ms={g["burst"]["worst_ms"]}')
    if point == '8x8-1if':
        instances = [dict(group=g, probe=p['probe'], status=p.get('status'), ms=p.get('ms'), exact=True,
                          within_budget=p.get('within_budget', True), budget_ms=p.get('budget_ms'),
                          never=bool(p.get('starved') or p.get('unanswered'))) for g,p in probes]
        assert not egress_ledger.findings(instances, point)
        print('EGRESS all seven rows within unchanged ledger')

for shape, expected in (('1x1',8),('8x8',36)):
    text = (root / 'board' / f'summary-{shape}.txt').read_text()
    rows = re.findall(r'sink (\d+): power off ([\d.]+) s.*?idle at the bind (True|False).*?durable by ([\d.]+) s \(bracket ([\d.]+) s\).*?durable ([\d.]+) s before it.*?(PASS|FAIL)', text)
    assert len(rows) == expected
    assert all(idle == 'True' and float(durable) < .8 and float(durable) < float(off) and float(margin) >= .25 and verdict == 'PASS' for _,off,idle,durable,width,margin,verdict in rows)
    print(f'BOARD {shape}: {expected} cut rows internally consistent; no bracket <=10 ms; summaries only, no raw acquisition or deployed-image identity in these files')
print('AUDIT PASS (evidence integrity and consistency; not a hardware or merge verdict)')
