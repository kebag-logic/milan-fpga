#!/usr/bin/env python3
"""Run the six new copy/fill plants in disposable trees, four workers maximum."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import sys
root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(root/'sw/firmware/ctrl/test'))
import ctrl_build as b
import ctrl_mutants as m
names = {'mem-copy-bulk-drops-a-word', 'mem-copy-rest-halfword-dropped',
         'mem-copy-rest-byte-dropped', 'mem-set-bulk-drops-a-word',
         'mem-set-rest-steps-overlap', 'mem-set-rest-halfword-dropped'}
mutants = [x for x in m.MUTANTS if x.name in names]
assert len(mutants) == 6
renamed = tuple('-D'+s+'=ctrl_mem_'+s for s in ('memcpy','memmove','memset','memcmp'))
def run(mutant):
    out = packet/'scratch/memory-mutants'/mutant.name
    src = out/'src'
    shutil.copytree(b.CTRL, src, dirs_exist_ok=True)
    target = src/mutant.path
    old = target.read_text()
    assert mutant.old in old
    target.write_text(old.replace(mutant.old, mutant.new, 1))
    tree = b.Tree(src, out/'build', b.PP/'tb/adp_engine', b.fw_gtest.Build(jobs=1))
    objs = b.compile_c(tree, b.sources(tree, ('plat/ctrl_mem.c',)), 'mem', renamed)
    tests = b.compile_tests(tree, ('test_ctrl_mem.cpp',), 'tests')
    result = b.execute('memory', b.link(tree, 'memory', objs+tests))
    (packet/(mutant.name+'.log')).write_text(result.log)
    caught = result.rc != 0 and mutant.test in result.log and mutant.needle in result.log
    print(mutant.name, 'CAUGHT' if caught else 'FAILED', flush=True)
    return caught
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, mutants))
print(sum(results), 'of', len(results), 'caught')
sys.exit(0 if all(results) else 1)
