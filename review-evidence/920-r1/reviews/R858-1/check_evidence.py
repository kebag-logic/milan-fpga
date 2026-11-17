#!/usr/bin/env python3
"""Check selected published receipts from archive 4a3e37f8 without running banks.

Arguments: directory containing author-r1 and author-r2; packet directory.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

evidence, packet = map(Path, sys.argv[1:])
manifest = json.loads((packet / 'receipts/public-evidence-manifest.json').read_text())
errors = []
for entry in manifest['selected']:
    data = (evidence / entry['file']).read_bytes()
    if hashlib.sha256(data).hexdigest() != entry['published_sha256']:
        errors.append('hash mismatch: ' + entry['file'])

def read(path):
    return (evidence / path).read_text()

def require(condition, text):
    if not condition:
        errors.append(text)

head = 'bd252db1d73511307c0ecb78470f0d15d0c3ea9b'
suite_names = []
checks = 0
for shard in range(4):
    prefix = f'author-r2/receipts/sweep-bd252db1/shard-{shard}'
    run = json.loads(read(prefix + '-results.json'))
    require(run['head'] == head, f'shard {shard}: wrong head')
    require(all(r['exit_code'] == 0 for r in run['results']), f'shard {shard}: nonzero exit')
    summary = read(prefix + '-summary.txt')
    counts = re.search(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)', summary)
    total, passed, failed, timed = map(int, counts.groups())
    require(total == passed and failed == timed == 0, f'shard {shard}: incomplete sweep')
    names = re.findall(r'^PASS\s+(\S+)', summary, re.M)
    require(len(names) == total, f'shard {shard}: suite tally differs')
    suite_names += names
    count, failures = map(int, re.search(r'checks: (\d+)\s+in-suite failures: (\d+)', summary).groups())
    checks += count
    require(failures == 0, f'shard {shard}: in-suite failures')
require(len(suite_names) == len(set(suite_names)) == 65, 'suite selection is not 65 distinct passes')
require(checks == 2713040, 'suite check tally differs')

timing = {}
budgets = {}
for point, groups, passes in (('1x1', 98, 132926), ('8x8-1if', 97, 231039)):
    saves = read(f'author-r2/receipts/harness/save-groups-{point}.txt')
    timing[point] = [line for line in saves.splitlines() if line.startswith('BURST ')]
    require(len(timing[point]) == 2 and all(line.endswith('within') for line in timing[point]), point + ': save target')
    grade = read(f'author-r2/receipts/harness/regrade-{point}.txt')
    expected = f'{groups} groups graded, 0 refusals, 7 budget misses'
    require(expected in grade and f'0 of {passes} work passes over' in grade, point + ': budget tally')
    sources = json.loads(read(f'author-r2/receipts/harness/sources-{point}.json'))
    require(len(sources) == groups, point + ': group source count')
    budgets[point] = {'groups': groups, 'refusals': 0, 'over_share': 0,
                      'work_passes': passes, 'recorded_held_egress_misses': 7}

def roms(path):
    found = {}
    for line in read(path).splitlines():
        m = re.match(r'(\S+): rc (\d+) rom (\d+) in (\d+), sram (\d+) in (\d+), tiles ([0-9.]+)', line)
        name, rc, rom, rom_cap, ram, ram_cap, tiles = m.groups()
        rc, rom, rom_cap, ram, ram_cap = map(int, (rc, rom, rom_cap, ram, ram_cap))
        require(rc == 0 and rom <= rom_cap and ram <= ram_cap, name + ': memory entry exceeded')
        found[name] = {'rom': rom, 'rom_cap': rom_cap, 'sram': ram, 'sram_cap': ram_cap, 'tiles': float(tiles)}
    return found

base = roms('author-r2/receipts/merge/rom-per-image-dev-70f4056f.txt')
merged = roms('author-r2/receipts/merge/rom-per-image-merge-d66b4045.txt')
require(len(base) == len(merged) == 8 and base.keys() == merged.keys(), 'ROM image set differs')
for name, values in merged.items():
    values['rom_growth'] = values['rom'] - base[name]['rom']
    require(296 <= values['rom_growth'] <= 304, name + ': growth outside stated range')

print(json.dumps({'archive': manifest['archive'], 'selected_hashes_checked': len(manifest['selected']),
                  'sweep': {'head': head, 'suites': len(suite_names), 'checks': checks},
                  'save_lines': timing, 'budgets': budgets, 'images': merged, 'errors': errors}, indent=2))
raise SystemExit(bool(errors))
