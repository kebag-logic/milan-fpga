#!/usr/bin/env python3
"""Merge a gate leg's runs (results, results-<part>, results-<helper>, ...) into one results directory: for each of the leg's
groups, the script and the log of a run whose log is finished (has SUMMARY); refuse a group with none, or a group whose
scripts differ between runs. usage: merge_leg.py BUILD_DIR OUT GROUP,GROUP,..."""
import filecmp, shutil, sys
from pathlib import Path

build, out, groups = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3].split(',')
out.mkdir(parents=True, exist_ok=True)
# this round's legs run their first group in the build's own run (results-build), so it is merged with the rest
runs = sorted(d for d in build.glob('results*') if d.is_dir() and 'niced-stopped' not in d.name and d != out)
missing, chosen = [], {}
for g in groups:
    done = [d for d in runs if (d / f'{g}.log').exists() and 'SUMMARY' in (d / f'{g}.log').read_text(errors='replace')]
    if not done:
        missing.append(g)
        continue
    scripts = [d / f'{g}.txt' for d in done]
    if any(not filecmp.cmp(scripts[0], s, shallow=False) for s in scripts[1:]):
        sys.exit(f'REFUSED {g}: its scripts differ between {[d.name for d in done]}')
    d = done[0]
    shutil.copy2(d / f'{g}.txt', out / f'{g}.txt')
    shutil.copy2(d / f'{g}.log', out / f'{g}.log')
    chosen[g] = d.name
for g, d in sorted(chosen.items()):
    print(f'{g} {d}')
if missing:
    sys.exit(f'MISSING {len(missing)}: {",".join(missing)}')
print(f'merged {len(chosen)} groups')
