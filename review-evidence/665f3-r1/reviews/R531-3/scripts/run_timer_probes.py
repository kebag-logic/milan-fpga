import pathlib,sys
root=pathlib.Path(sys.argv[1]).resolve(); p=pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_build as b, fw_gtest
t=b.Tree(b.CTRL,p/'scratch/timer-probes',p/'scratch/native/reuse',fw_gtest.Build(jobs=4))
o=b.compile_c(t,[b.CTRL/'acmp/acmp.c'],'core')
o+=fw_gtest.compile_tests(t.build,b.includes(t),[p/'scripts/independent_timers.cpp'],t.out/'tests')
r=b.execute('independent-timers',b.link(t,'timer-probes',o))
(p/'receipts/independent-timers.log').write_text(r.log)
(p/'receipts/independent-timers.rc').write_text(str(r.rc)+'\n')
print(r.log)
sys.exit(r.rc)
