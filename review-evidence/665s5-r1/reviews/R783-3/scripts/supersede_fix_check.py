#!/usr/bin/env python3
"""Does the required outcome hold? In memory: the self-test's `another path` case given a row of another path in the
table's own group, then the path term dropped from the rule. Nothing in TREE is written.

usage: supersede_fix_check.py TREE
"""
import sys, types
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
H = tree / 'tb/verilator/ctrl_service_hooks'
sys.path.insert(0, str(H)); sys.dont_write_bytecode = True
RULE = "(x['group'], x['path'], x['interface']) == (by, *r['path'])"
DROPPED = "(x['group'], x['interface']) == (by, r['path'][1])"
CASE = "got = graded_with({'acmp-disc': [dict(lost, path=['acmp.bind_rx', 1])], 'hooks-disc-aging': [again]})"
FIXED = "got = graded_with({'acmp-disc': [lost], 'hooks-disc-aging': [dict(again, path=['acmp.entity_available', 1])]})"
import hooks  # noqa: E402
def run_with(rule, case):
    p = H / 'run.py'; src = p.read_text(); assert src.count(RULE) == 1
    m = types.ModuleType('run'); m.__file__ = str(p); sys.modules['run'] = m
    exec(compile(src.replace(RULE, rule), str(p), 'exec'), m.__dict__)
    p = H / 'hooks_selftest.py'; src = p.read_text(); assert src.count(CASE) == 1
    s = types.ModuleType('st'); s.__file__ = str(p); sys.modules['st'] = s
    exec(compile(src.replace(CASE, case), str(p), 'exec'), s.__dict__)
    return {k: v[:70] for k, v in s.run_checks().items() if v}
print('head case, head rule:', run_with(RULE, CASE))
print('head case, path term dropped:', run_with(DROPPED, CASE))
print('reaching case, head rule:', run_with(RULE, FIXED))
print('reaching case, path term dropped:', run_with(DROPPED, FIXED))
