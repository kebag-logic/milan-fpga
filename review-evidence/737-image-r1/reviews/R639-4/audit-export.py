#!/usr/bin/env python3
"""Independently examine authenticated layer populations and CPU tree bytes."""
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
work = packet / 'scratch/image'
pins = json.loads((root / 'ci/image/sources.lock.json').read_text())
lock = json.loads((root / 'ci/image/image.lock.json').read_text())
expected = {}
placements = {'VexiiRiscv': ''}
rows = [r for r in pins['sources'] if r['tool'] == 'VexiiRiscv' or r.get('parent')]
while rows:
    ready = [r for r in rows if r['tool'] == 'VexiiRiscv' or r['parent'] in placements]
    if not ready:
        break  # Other tool families own the remaining recursive source rows.
    for row in ready:
        prefix = '' if row['tool'] == 'VexiiRiscv' else (placements[row['parent']] + '/' + row['path']).strip('/')
        placements[row['tool']] = prefix
        with tarfile.open(work / 'context' / row['filename']) as archive:
            for member in archive:
                if not (member.isfile() or member.issym()):
                    continue
                name = member.name.partition('/')[2]
                if not name:
                    continue
                path = (prefix + '/' + name).lstrip('/')
                data = archive.extractfile(member).read() if member.isfile() else member.linkname.encode()
                expected[path] = dict(kind='file' if member.isfile() else 'symlink',
                                      executable=bool(member.mode & 0o111),
                                      sha256=hashlib.sha256(data).hexdigest())
        rows.remove(row)

# Reproduce the committed CPU patch independently with Git, without any identity.
patch = root / 'sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch'
cpu_file = 'src/main/scala/vexiiriscv/soc/litex/Soc.scala'
cpu_row = next(r for r in pins['sources'] if r['tool'] == 'VexiiRiscv')
replay = packet / 'scratch/cpu-replay'
target = replay / 'pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv' / cpu_file
target.parent.mkdir(parents=True, exist_ok=True)
with tarfile.open(work / 'context' / cpu_row['filename']) as archive:
    member = next(m for m in archive if m.name.partition('/')[2] == cpu_file)
    target.write_bytes(archive.extractfile(member).read())
subprocess.run(['git', 'apply', str(patch)], cwd=replay, check=True)
expected[cpu_file]['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()

prefix = 'opt/python/lib/python3.12/site-packages/pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv/'
actual = {}
layers = []
all_counts = collections.Counter()
with tarfile.open(work / 'image-a.tar') as image:
    for index, record in enumerate([*lock['base_layers'], *lock['layers']]):
        counts = collections.Counter()
        roots = collections.Counter()
        with image.extractfile('blobs/' + record['oci_digest'].replace(':', '/')) as stream:
            with tarfile.open(fileobj=stream, mode='r|*') as archive:
                for member in archive:
                    name = member.name.removeprefix('./')
                    assert not any(name == p or name.startswith(p + '/') for p in ('build','recipe','inputs'))
                    counts['members'] += 1
                    if member.isfile(): counts['regular'] += 1
                    roots['/'.join(name.split('/')[:2])] += 1
                    if name in ('opt/ci-image/smoke.py', 'opt/ci-image/sources.lock.json'):
                        data = archive.extractfile(member).read()
                        assert data == (root / 'ci/image' / Path(name).name).read_bytes()
                    if name.startswith(prefix) and (member.isfile() or member.issym()):
                        data = archive.extractfile(member).read() if member.isfile() else member.linkname.encode()
                        actual[name[len(prefix):]] = dict(kind='file' if member.isfile() else 'symlink',
                                                       executable=bool(member.mode & 0o111),
                                                       sha256=hashlib.sha256(data).hexdigest())
        all_counts.update(counts)
        layers.append(dict(index=index, tool=record.get('tool','base'), **counts,
                           roots=dict(sorted(roots.items()))))
assert actual == expected, dict(missing=sorted(expected.keys()-actual.keys()),
                               extra=sorted(actual.keys()-expected.keys()),
                               changed=[k for k in expected.keys() & actual.keys() if expected[k]!=actual[k]])
result = dict(counts=dict(all_counts), layers=layers, cpu_sources=len(placements),
              cpu_members=len(actual), cpu_exact_bytes_links_execute_bits=True,
              embedded_smoke_and_source_lock_equal_head=True, build_context_roots_absent=True)
(packet / 'export-population.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='layers'},indent=2))
