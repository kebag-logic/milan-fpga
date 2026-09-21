import importlib.util,sys,os,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent
tmp=Path(os.environ['REVIEW_TMP'])
spec=importlib.util.spec_from_file_location('review_builder',root/'sw/builder/test_builder.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
m.OUT=tmp/'builder-out';m.OUT.mkdir(exist_ok=True)
for name in sys.argv[1:] or ['test_baremetal_profile_contract','test_boot_policy_follows_the_declaration']:
 print('RUN',name,flush=True);getattr(m,name)();print('PASS',name,flush=True)
print('FOCUSED_SKIPS',json.dumps(m.SKIPPED),flush=True)
