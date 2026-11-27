"""Reviewer probe: the console (lat) and MII PHY host arms at the checkout given as argv[1], then every
mii-* and plat-lat-* mutant of ctrl_mutants.py, planted in copies under argv[2]. The checkout is never edited."""
import hashlib, json, sys
from pathlib import Path
ROOT, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'sw/firmware/ctrl/test'))
import ctrl_build, ctrl_mutants, fw_gtest, plat_arms
before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ctrl_build.CTRL / 'plat').glob('*.c')}
tree = ctrl_build.Tree(ctrl_build.CTRL, OUT / 'clean', OUT / 'reuse', fw_gtest.Build(jobs=16))
rec = []
for name, arm in [('console', plat_arms.arm_plat), ('mii', lambda t: plat_arms.arm_platboot(t, 1, mii=True))]:
    o = arm(tree)
    (OUT / (name + '.log')).write_text(o.log)
    print('ARM', name, 'rc', o.rc, flush=True)
    rec.append(dict(arm=name, rc=o.rc))
ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if m.name.startswith(('mii-', 'plat-lat-')))
ctrl_mutants.unnamed_tests = lambda: []
print('MUTANTS', len(ctrl_mutants.MUTANTS), [m.name for m in ctrl_mutants.MUTANTS], flush=True)
failed = ctrl_mutants.campaign(OUT / 'mutants', OUT / 'reuse', 16)
after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ctrl_build.CTRL / 'plat').glob('*.c')}
rec.append(dict(mutants=len(ctrl_mutants.MUTANTS), escaped_any=failed, checkout_plat_sources_unchanged=before == after))
print(json.dumps(rec))
raise SystemExit(1 if failed or any(r.get('rc') for r in rec) or before != after else 0)
