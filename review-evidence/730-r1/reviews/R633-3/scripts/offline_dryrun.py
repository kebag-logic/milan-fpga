"""Print the actual dry-run path with inert external boundaries; sandbox only."""
import importlib.util,pathlib,sys
root=pathlib.Path(sys.argv[1]).resolve()
spec=importlib.util.spec_from_file_location('reviewed_runner',root/'scripts/act_ci.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
f=m.selftest_fixture();run=m.ValidatedRun(f.pr,f.repository,f.base)
for slot in (0,3):
 rc,text=m.dry_run_transcript(run,'rtl-full',m.ReplaySlot(slot),root)
 print(f'OFFLINE DRY RUN slot={slot}, rc={rc}; synthetic PR/head, inert external boundaries')
 print(text,end='')
 assert rc==0
 expected=range(20*slot+4,20*slot+20,4)
 assert all(f'--cpuset-cpus={c}-{c+3}' in text for c in expected)
