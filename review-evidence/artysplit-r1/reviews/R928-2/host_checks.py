"""Focused console and MII tests and their planted defects."""
import concurrent.futures
import json
from pathlib import Path
import sys

source, packet = map(Path, sys.argv[1:3])
sys.path.insert(0, str(source / 'sw/firmware/ctrl/test'))
import ctrl_build
import ctrl_mutants
import fw_gtest
import plat_arms

out = packet / 'scratch/host'
out.mkdir(parents=True, exist_ok=True)

def arm(item):
    name, fn = item
    tree = ctrl_build.Tree(ctrl_build.CTRL, out / name, out / (name+'-reuse'), fw_gtest.Build(jobs=4))
    result = fn(tree)
    (packet / ('host-'+name+'.log')).write_text(result.log)
    (packet / ('host-'+name+'.rc')).write_text(str(result.rc)+'\n')
    print(name, result.rc, flush=True)
    return dict(name=name, rc=result.rc)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(arm, [('console', plat_arms.arm_plat),
                                 ('mii', lambda t: plat_arms.arm_platboot(t, 1, mii=True))]))
ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if m.name.startswith(('mii-', 'plat-lat-')))
# Only the focused table's named tests are in scope; no claim of whole-suite mutation coverage.
ctrl_mutants.unnamed_tests = lambda: []
failed = ctrl_mutants.campaign(out / 'mutants', out / 'reuse', 8)
results.append(dict(name='focused-plants', count=len(ctrl_mutants.MUTANTS), failures=failed))
(packet / 'host-results.json').write_text(json.dumps(results, indent=2)+'\n')
raise SystemExit(bool(failed) or any(r.get('rc', 0) for r in results))
