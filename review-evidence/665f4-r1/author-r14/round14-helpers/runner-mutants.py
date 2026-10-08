import importlib.util, io, contextlib, json, pathlib, sys, tempfile
root=pathlib.Path('/scratch')
source=pathlib.Path('/candidate/scripts/act_ci.py').read_text()
entry='    (\n        "third_party/lwSRP",\n        "third_party/lwSRP",\n        "https://github.com/kebag-logic/lwSRP.git",\n    ),\n'
plants=[
 ('missing-trusted-entry',entry,'','the trusted manifest includes exactly the five approved entries'),
 ('missing-materialization','if name != "external"','if name not in ("external", "third_party/lwSRP")','materialization fetches all four public pins'),
 ('ignore-manifest-equality','if actual != expected:','if False:','candidate that drops lwSRP is refused before fetch'),
 ('ignore-manifest-addition','if actual != expected:','if False:','candidate that adds another lwSRP is refused before fetch'),
 ('ignore-duplicate-key','if key in actual:','if False:','candidate that duplicates lwSRP is refused before fetch'),
 ('ignore-url-change','if actual != expected:','if False:','candidate that redirects lwSRP is refused before fetch'),
 ('ignore-gitlink-omission','if actual_gitlinks != expected_gitlinks or len(gitlinks) != len(actual_gitlinks):','if False:','candidate that drops lwSRP gitlink is refused before fetch'),
 ('ignore-gitlink-addition','if actual_gitlinks != expected_gitlinks or len(gitlinks) != len(actual_gitlinks):','if False:','candidate that adds lwSRP gitlink is refused before fetch'),
]
results=[]
for index,(name,old,new,needle) in enumerate([('baseline','','','')]+plants):
 if old: assert source.count(old)==1,(name,source.count(old))
 path=root/(name+'.py');path.write_text(source.replace(old,new,1) if old else source)
 spec=importlib.util.spec_from_file_location('manifest_probe',path)
 mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
 tally=mod.SelftestTally();log=io.StringIO();error=None
 with contextlib.redirect_stdout(log),tempfile.TemporaryDirectory(dir=root) as tmp:
  try:
   fixture=mod.selftest_git_fixture(pathlib.Path(tmp),mod.selftest_fixture().pr)
   mod.selftest_submodule_manifest(tally,fixture)
  except mod.Refusal as exc:
   error=str(exc)
 text=log.getvalue();(root/(name+'.log')).write_text(text+(error or ''))
 passed=tally.failures==0 and error is None if name=='baseline' else ('FAIL '+needle) in text
 results.append(dict(name=name,passed=passed,failures=tally.failures,exception=error))
 print(json.dumps(results[-1]),flush=True)
(root/'mutation-results.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(item['passed'] for item in results)
