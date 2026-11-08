# SPDX-License-Identifier: MIT
# usage: cand_plants.py TREE WORK CANDIDATES_JSON EXCLUDE_FILTER [NAME...]
# For each candidate plant {name, path, old, new}: copies TREE (src, include, tests, CMake files) to WORK/NAME,
# applies the plant (old must occur once), builds acmp_tests, then runs the whole binary and the binary with
# EXCLUDE_FILTER excluded. Prints one line per plant: name, full-suite rc and failing tests, rc without the excluded
# tests. TREE is never modified.
import json, shutil, subprocess, sys
from pathlib import Path
tree, work, cands, exclude = Path(sys.argv[1]), Path(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text()), sys.argv[4]
only = set(sys.argv[5:])
for p in cands:
    if only and p['name'] not in only:
        continue
    d = work / p['name']
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(tree, d / 'tree', ignore=shutil.ignore_patterns('.git', 'build*', '__pycache__'))
    f = d / 'tree' / p['path']
    t = f.read_text()
    assert t.count(p['old']) == 1, (p['name'], t.count(p['old']))
    f.write_text(t.replace(p['old'], p['new']))
    subprocess.run(['cmake', '-S', d / 'tree', '-B', d / 'build', '-DCMAKE_BUILD_TYPE=Debug'], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['cmake', '--build', d / 'build', '--target', 'acmp_tests', '-j8'], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    full = subprocess.run([d / 'build/acmp_tests'], capture_output=True, text=True)
    (d / 'full.txt').write_text(full.stdout + full.stderr)
    failed = sorted({l.split()[3] for l in full.stdout.splitlines() if l.startswith('[  FAILED  ]') and len(l.split()) > 3
                     and '.' in l.split()[3]})
    rest = subprocess.run([d / 'build/acmp_tests', '--gtest_filter=-' + exclude], capture_output=True, text=True)
    (d / 'without.txt').write_text(rest.stdout + rest.stderr)
    total = [l for l in rest.stdout.splitlines() if l.startswith('[==========]') and 'ran' in l]
    print(p['name'], '| full rc', full.returncode, '| failing', ','.join(failed) or '-', '| without rc', rest.returncode,
          '|', total[-1] if total else '?', flush=True)
