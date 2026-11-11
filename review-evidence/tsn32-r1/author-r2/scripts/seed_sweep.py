#!/usr/bin/env python3
"""Run AcmpWalk at many seeds against the head's core and planted copies (scratch evidence, not a gate).

usage: seed_sweep.py TREE OUT SEEDS
The test's fixed seed is replaced by one read from WALK_SEED; each plant is the campaign's own entry.
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

tree, out, seeds = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
test = (tree / 'tests/test_acmp_walk.cpp').read_text()
anchor = 'Rng rng{0x9E3779B9u};'
assert test.count(anchor) == 1
test = test.replace(anchor, 'Rng rng{static_cast<std::uint32_t>(std::strtoul(std::getenv("WALK_SEED"), nullptr, 0))};')
test = test.replace('#include <array>', '#include <array>\n#include <cstdlib>')
(out / 'walk_seeded.cpp').write_text(test)
flags = ['-DACMP_MAX_SINKS=33u', '-fsanitize=shift,undefined', '-fno-sanitize-recover=shift,undefined']
pc = lambda *o: subprocess.check_output(['pkg-config', *o, 'gmock', 'gtest'], text=True).split()
subprocess.run(['g++', '-std=c++20', '-O1', *flags, '-I' + str(tree / 'include'), '-I' + str(tree / 'examples'),
                '-I' + str(tree / 'tests'), *pc('--cflags'), '-c', str(out / 'walk_seeded.cpp'), '-o', str(out / 'walk.o')], check=True)
subprocess.run(['g++', '-std=c++20', '-O1', *pc('--cflags'), '-c', str(tree / 'tests/main.cpp'), '-o', str(out / 'main.o')], check=True)
plants = {m['name']: m for m in json.loads((tree / 'tests/mutations.json').read_text()) if m['name'].startswith('walk-')}
source = (tree / 'src/acmp.c').read_text()
variants = {'head': source}
for name, m in plants.items():
    assert source.count(m['old']) == 1, name
    variants[name] = source.replace(m['old'], m['new'])

def build(item):
    name, text = item
    d = out / name
    d.mkdir(exist_ok=True)
    (d / 'acmp.c').write_text(text)
    subprocess.run(['gcc', '-std=c11', '-O1', *flags, '-DNDEBUG', '-DCTRL_REENTRY_ASSERT', '-I' + str(tree / 'include'),
                    '-c', str(d / 'acmp.c'), '-o', str(d / 'acmp.o')], check=True)
    subprocess.run(['g++', str(d / 'acmp.o'), str(out / 'walk.o'), str(out / 'main.o'), '-fsanitize=shift,undefined',
                    *pc('--libs'), '-o', str(d / 'walk')], check=True)
    caught = {}
    for size in ('OneSink', 'EightSinks', 'ThirtyTwoSinks', 'ThirtyThreeSinks'):
        hits = []
        for seed in range(1, seeds + 1):
            env = dict(os.environ, WALK_SEED=str(0x9E3779B9 + seed * 0x10001))
            r = subprocess.run([str(d / 'walk'), '--gtest_filter=AcmpWalk.' + size + '*'], env=env,
                               capture_output=True, text=True, timeout=300)
            text = r.stdout
            hits.append({'rc': r.returncode, 'trace': "full walk's calls" in text,
                         'sink': 'no sink marked' in text, 'interface': 'no interface marked' in text,
                         'reach': 'the random entries' in text or 'owed probe its timer' in text})
        caught[size] = {k: sum(h[k] for h in hits) for k in ('trace', 'sink', 'interface', 'reach')}
        caught[size]['failed'] = sum(h['rc'] != 0 for h in hits)
    return name, caught

with ThreadPoolExecutor(max_workers=12) as pool:
    results = dict(pool.map(build, variants.items()))
(out / 'results.json').write_text(json.dumps({'seeds': seeds, 'results': results}, indent=1) + '\n')
for name, c in results.items():
    print(name, json.dumps(c))
