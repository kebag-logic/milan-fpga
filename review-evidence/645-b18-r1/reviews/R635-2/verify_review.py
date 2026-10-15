#!/usr/bin/env python3
"""Read-only replay of the #645 documentation review from published Git objects.

Usage: python3 verify_review.py /path/to/candidate
The candidate object database must contain the published evidence revision.
No bench access, source edits, external commands from the packet, or builds.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from datetime import datetime, timezone

REPO = Path(sys.argv[1]).resolve()
HEAD = 'b3f7a696713a96b42265e08a8c3a04a430b7b5ed'
PREV = '480c5e916f8bf711c47e1985ba3efe2b2471bdda'
BASE = '9ef717727e6fdac11ee7f01672fefae948452343'
EVIDENCE = '1a86b31dd03c479a196ece2b532d2141279be4d1'
PROVENANCE = 'bbc53aabb02a1654812ba2eaa1642f5e36e69ce0'
PACKET = 'review-evidence/645-b18-r1/'
PAGE = 'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], env=env)

def blob(path, revision=EVIDENCE):
    return git('show', revision + ':' + PACKET + path)

def text(path, revision=EVIDENCE):
    return blob(path, revision).decode()

def data(path):
    return json.loads(blob(path))

def jl(path):
    return [json.loads(line) for line in text(path).splitlines() if line.startswith('{')]

def ok(label):
    print('PASS:', label)

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == '57d505ff2fcb01a2f51f631c9784701f41716e8f'
for rev in (BASE, PREV):
    assert git('diff', '--name-only', rev, HEAD).decode().splitlines() == [PAGE]
git('diff', '--check', BASE, HEAD)
ok('exact head/tree; base and previous-head deltas each touch only the findings page')

# Compare every tracked index record and actual blob byte/mode to the head tree.
tree = {}
for item in git('ls-tree', '-rz', HEAD).split(b'\0'):
    if item:
        meta, path = item.split(b'\t', 1)
        mode, kind, oid = meta.split()
        tree[path] = (mode, oid)
index = {}
for item in git('ls-files', '--stage', '-z').split(b'\0'):
    if item:
        meta, path = item.split(b'\t', 1)
        mode, oid, stage = meta.split()
        assert stage == b'0' and path not in index
        index[path] = (mode, oid)
assert tree == index
blobs = links = 0
for path, (mode, oid) in tree.items():
    if mode == b'160000':
        links += 1
        print('GITLINK:', path.decode(), oid.decode())
        continue
    f = REPO / os.fsdecode(path)
    st = f.lstat()
    if mode == b'120000':
        assert stat.S_ISLNK(st.st_mode)
        raw = os.fsencode(os.readlink(f))
    else:
        assert stat.S_ISREG(st.st_mode)
        assert bool(st.st_mode & 0o111) == (mode == b'100755')
        raw = f.read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest().encode() == oid, path
    blobs += 1
ok(f'{blobs} tracked blob bytes/modes and entire index verified; {links} gitlinks match head')

manifest = data('MANIFEST.json')
checked = 0
for row in manifest:
    if row['file'].startswith(('author/', 'author-r2/', 'manager-provenance/')):
        assert hashlib.sha256(blob(row['file'])).hexdigest() == row['published_sha256'], row['file']
        checked += 1
ok(f'{checked} author/provenance published manifest hashes; reviewer reports excluded')
names = git('ls-tree', '-r', '--name-only', EVIDENCE, PACKET + 'manager-provenance/').decode().splitlines()
for name in names:
    rel = name[len(PACKET):]
    assert blob(rel) == blob(rel, PROVENANCE)
ok(f'{len(names)} provenance files equal the page-linked evidence commit')
original_names = git('ls-tree', '-r', '--name-only', EVIDENCE, PACKET + 'author/').decode().splitlines()
for name in original_names:
    rel = name[len(PACKET):]
    assert blob(rel) == blob(rel, '2e913519')
ok(f'{len(original_names)} original author files equal the page-named packet location')

p = data('manager-provenance/provenance.json')
l = data('manager-provenance/flashboot_layout.json')
assert p['source']['dev_merge'] == BASE
assert BASE in text('manager-provenance/01-clone.status')
assert git('rev-parse', BASE+'^{tree}').decode().strip() in text('manager-provenance/01-clone.status')
assert 'PR #742' in git('show', '-s', '--format=%s', BASE).decode()
bit = '4b5a391af524cb3b490099381c0fd9e3275383fc51c163a75fb78cdb054ffcca'
aem = '4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d'
assert p['build']['bitstream_sha256'] == bit and p['build']['bitstream_bytes'] == 3825992
assert p['build']['aem_desc_sha256'] == l['aem_image_sha256'] == aem
assert p['build']['aem_desc_bytes'] == l['aem_image_bytes'] == 7512
assert l['aem_image_crc32'] == int('5ba355eb', 16)
flash = text('manager-provenance/flash.log')
assert hashlib.sha256(blob('manager-provenance/flash.log')).hexdigest() == 'a1539c67fc8c6490034332976024248decf3046fdc8da72a9c867762e09d9d46'
tokens = ['2026-10-15T18:42:24Z', '[deploy] write+verify aem', '[deploy] write+verify bitstream',
          'FLASH_RC=0', 'POWERCYCLE_RC=0', 'FALLBACK 0      Normal configuration',
          'FALLBACK 1      Normal configuration', '=== done 2026-10-15T18:44:49Z']
positions = [flash.index(t) for t in tokens]
assert positions == sorted(positions)
assert flash.count('Verifying write (May take time)') == 2
console = text('manager-provenance/console-after-flash.log')
for s in p['cold_boot_console']:
    assert s in console
page = git('show', HEAD+':'+PAGE).decode()
for s in (bit, aem, PROVENANCE, 'no read on\nthe device distinguishes the two images'):
    assert s in page
ok('source/tree -> manager-recorded file hashes -> layout AEM hash/CRC -> ordered verified writes -> cold boot/no fallback -> boot line')
print('LIMIT: bitstream binary absent; its full-file hash is manager-attested. Layout payload hash is a separate hash.')
identity = jl('author/identity/identity-verdict.txt')
assert len(identity) == 11 and all(x['result'] == 'PASS' for x in identity)
assert 'LOCK 2026-10-15T18:50:11.845Z' in text('author/identity/lock-window.txt')
ok('11 identity checks after the recorded cold boot; continuity uses the public manager statement')

digest = ''
for i in range(1, 11):
    cycle = f'c{i:02d}'
    path = 'author/cycles/' + cycle + '/poll.jsonl'
    digest += hashlib.sha256(blob(path)).hexdigest() + '  cycles/' + cycle + '/poll.jsonl\n'
    polls = jl(path)
    events = jl('author/cycles/' + cycle + '/events.jsonl')
    summary = data('author/summary/' + cycle + '.json')
    bind = next(x['t_bind_local'] for x in events if x['kind'] == 'bind-time')
    assert bind == summary['bind_local']
    assert len(polls) == 80 and [x['n'] for x in polls] == list(range(80))
    assert all(int(x['words']['0x8d4'], 16) == int(x['words']['0x8d8'], 16) == 0 for x in polls)
    assert all(len(x['words']) == 8 for x in polls)
    for x in events:
        if x['kind'] in ('bind', 'unbind'):
            assert x['status'] == 0
        if x['kind'] == 'state':
            assert x['clk_dut'] == 0 and x['clk_peer'] == 1
        if x['kind'] == 'counters':
            def words(key):
                payload = bytes.fromhex(x['payloads'][key])
                return [int.from_bytes(payload[j:j+4], 'big') for j in range(8, 136, 4)]
            si, avb = words('dut-0x0005-0'), words('dut-0x0009-0')
            assert si[0] == avb[0] == 1
            assert all(si[j] == 0 for j in (1, 2, 3, 4, 5, 7, 8, 9, 10))
    # The first-poll start and last-poll end are the published observation bounds.
    first, last = polls[0]['t0'] - bind, polls[-1]['t1'] - bind
    assert f'{last:.2f}' in next(line for line in page.splitlines() if line.startswith('| '+cycle+' |') and 'Held' in line)
    print(f'COUNTERS: {cycle} polls=80 SLIP_LB=0 SLIP_TDM=0 first={first:.6f}s last={last:.6f}s states=0/1')
assert digest.encode() == blob('author/summary/counter-logs.sha256')
assert hashlib.sha256(digest.encode()).hexdigest() == '2c5e8d6ff8220cb16a9a3d0535279dfd7f04b5642c9aee2d9f97cdefcd939bdb'
for when in ('start', 'end'):
    raw = text('author/restore/dut-' + when + '.txt')
    m = re.search(r'^0x900008d4\s+((?:[0-9a-f]{2} ){4})', raw, re.M)
    assert int.from_bytes(bytes.fromhex(m.group(1)), 'little') == 0
assert '18:59:58.137Z' in text('author/restore/baseline-end-lock.txt')
ok('800 polls, both baselines, cumulative-counter joins and raw-counter digest; c01/c10 tails covered by later zero reads')
ok('20 raw counter payloads: DUT MEDIA_LOCKED and LINK_UP remain 1; named DUT error counters remain 0')
for name in ('table', 'compare'):
    rows = [s for s in text('author/summary/'+name+'.md').splitlines() if s.startswith('| c')]
    assert len(rows) == 10 and all(row in page for row in rows)
ok('both unchanged tables match the published summaries, 20 rows')
gates = text('author-r2/gates/gates-r2.txt')
assert HEAD in gates and gates.count('rc=0') == 7
assert '338 added line(s)' in gates
ok('author seven-gate receipt names the exact head and 338 added lines')
print('LIMIT: no new bench run, capture replay, physical calibration, source bank or merge-candidate bank performed.')
