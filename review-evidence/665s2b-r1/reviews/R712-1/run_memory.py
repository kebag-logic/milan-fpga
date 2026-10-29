#!/usr/bin/env python3
"""Execute the submitted memory tests and their mutations without the full bank."""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent/'scratch/memory'
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_build as b
import ctrl_mutants as m
tree=b.Tree(b.CTRL,out,b.PP/'tb/adp_engine')
renamed=tuple('-D'+s+'=ctrl_mem_'+s for s in ('memcpy','memmove','memset','memcmp'))
objs=b.compile_c(tree,b.sources(tree,('plat/ctrl_mem.c',)),'mem',renamed)
tests=b.compile_tests(tree,('test_ctrl_mem.cpp',),'tests')
result=b.execute('memory',b.link(tree,'memory',objs+tests))
print(result.log)
sys.exit(result.rc)
