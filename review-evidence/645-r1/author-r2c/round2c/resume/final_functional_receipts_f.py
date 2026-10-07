"""Collect the merged-head functional gate receipts into the handoff packet.

Every functional gate ran at the final merge content (f6bd415f) in
functional/merged-gates-f; the vendor parser ran in the lane tree (vendor-f). Logs over 200 KB stay in scratch
with size and SHA-256; a labelled tail is retained instead.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

w = Path(__file__).resolve().parents[1]
repo = Path('$LANES/645-ring-slip')
k = w / 'functional/merged-gates-f'
earlier = w / 'functional/merged-gates-k'
out = Path.home() / 'milan-fpga-management/2026-09-23/645-a531/round2c/full-gates'
assert (k / 'all.rc').read_text().strip() == '0'
commands = json.loads((k / 'commands.json').read_text())
expected = {'sweep-0', 'sweep-1', 'physical', 'builder', 'source-controls', 'wire-controls', 'render-pullin', 'render-boundary', 'portability'}
assert {row['name'] for row in commands} == expected, {row['name'] for row in commands}
assert all(row['rc'] == 0 and not row['resource_interruption'] for row in commands)
shard1 = []
out.mkdir(exist_ok=True, parents=True)
inventory = []
sources = [(k, p) for p in sorted(k.rglob('*')) if p.is_file()]
pullin = w / 'functional/tree/tb/verilator/milan_dp_render/obj_pullin'
sources += [(pullin.parent, p) for p in sorted(pullin.glob('pullin_*.log'))]
for base, path in sources:
    relative = Path(base.name) / path.relative_to(base) if base != k else path.relative_to(base)
    if base == earlier and path.name == 'commands.json':
        relative = Path('merged-gates-k/commands.json')
    data = path.read_bytes()
    row = dict(path=str(path.relative_to(w)), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    target = out / relative
    target.parent.mkdir(exist_ok=True, parents=True)
    if len(data) <= 200000:
        kept = data.decode(errors='replace').replace(str(Path.home()), '$HOME').encode()
        assert len(kept) <= 200000
        target.write_bytes(kept)
        row['retained_sha256'] = hashlib.sha256(kept).hexdigest()
    elif path.suffix == '.log':
        with path.open('rb') as stream:
            stream.seek(max(0, len(data) - 60000))
            tail = stream.read().decode(errors='replace').split('\n', 1)[-1]
        kept = ('EXCERPT: final portion only; original size and hash are in the inventory.\n'
                + tail).replace(str(Path.home()), '$HOME').encode()
        target.with_suffix('.tail.txt').write_bytes(kept)
        row['excerpt'] = str(target.with_suffix('.tail.txt').relative_to(out))
        row['excerpt_sha256'] = hashlib.sha256(kept).hexdigest()
    inventory.append(row)
for index in range(0, len(inventory), 100):
    payload = json.dumps(inventory[index:index + 100], indent=2).replace(str(Path.home()), '$HOME') + '\n'
    assert len(payload.encode()) <= 200000
    (out / f'artifact-inventory-{index // 100:02d}.json').write_text(payload)
shards = []
for name, log in [('sweep-0', k / 'sweep-0.log'), ('sweep-1', k / 'sweep-1.log'), ('physical', k / 'physical.log')]:
    text = log.read_text()
    row = re.findall(r'^suites: (\d+)   passed: (\d+)   failed: (\d+)   timed out: (\d+)$', text, re.M)
    tally = re.findall(r'^checks: (\d+)   in-suite failures: (\d+)$', text, re.M)
    assert len(row) == 1 and len(tally) == 1, name
    suites, passed, failed, timed_out = map(int, row[0])
    checks, failures = map(int, tally[0])
    assert suites == passed and failed == timed_out == failures == 0
    shards.append(dict(name=name, suites=suites, checks=checks, failures=0, rc=0))
head = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
summary = dict(
    result='PASS', rc=0, commands=commands + shard1, shards=shards,
    default_suites=sum(r['suites'] for r in shards if r['name'] != 'physical'),
    default_checks=sum(r['checks'] for r in shards if r['name'] != 'physical'),
    render_pullin_phases=len(list(pullin.glob('pullin_*.log'))),
    export_content='f6bd415f for every command (three source exports, blob-identical: ../resume/export-identity-f6bd415f.json)',
    vendor_parser='../vendor-f/ (lane tree at f6bd415f, under the shared lock)',
    current_head=head,
    builder_note='Builder rc 0 with one arm not run for a recorded reason: gate 11 needs an Arty mf48 build tree that is not on this host.',
    note='Original non-piped commands, return codes and peak service memory are retained. '
         'Large logs stay in external scratch with size and SHA-256.')
(out / 'summary.json').write_text(json.dumps(summary, indent=2).replace(str(Path.home()), '$HOME') + '\n')
print(json.dumps(dict(result='PASS', shards=shards, head=head), indent=2))
