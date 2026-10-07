#!/usr/bin/env python3
"""[R530] R530-3: build sw/firmware/ctrl/acmp/acmp.c of tree ROOT with one gtest probe file and run it.
usage: run_r530_probes.py ROOT WORKDIR TESTFILE.cpp TAG   (exit = the test binary's)"""
import pathlib, sys
root, work, test, tag = (pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(),
                         pathlib.Path(sys.argv[3]).resolve(), sys.argv[4])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_build as b, fw_gtest  # noqa: E402
t = b.Tree(b.CTRL, work / 'build', work / 'reuse', fw_gtest.Build(jobs=2))
o = b.compile_c(t, [b.CTRL / 'acmp/acmp.c'], 'core')
o += fw_gtest.compile_tests(t.build, b.includes(t), [test], t.out / 'tests')
r = b.execute(tag, b.link(t, tag, o))
print(r.log)
sys.exit(r.rc)
