import json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]);output=pathlib.Path(sys.argv[2]);base='483a133ed08867ea0d300d2b4a027b5b48a4282f';head='f01f237d4b48c7b1ed59c80aca51430901791624'
def tree(rev):
 rows=subprocess.check_output(['rtk','proxy','git','-C',str(root),'ls-tree','-rz',rev]).split(b'\0');result={}
 for row in rows:
  if row:
   meta,path=row.split(b'\t');result[path.decode()]=meta.decode()
 return result
before,after=tree(base),tree(head)
changed={p:{'base':before.get(p),'head':after.get(p)} for p in sorted(before.keys()|after.keys()) if before.get(p)!=after.get(p)}
assert set(changed)=={'scripts/ci_events.py','docs/testing/CI_WORKFLOWS.md'}
result={'base':base,'head':head,'diff':changed,'base_entries':len(before),'head_entries':len(after),'unchanged_selected':{p:v for p,v in after.items() if before.get(p)==v and (p.startswith('.github/workflows/') or p.endswith('.budget') or '160000' in v or p=='scripts/act_ci.py')},'all_other_entries_equal':True}
output.write_text(json.dumps(result,indent=2)+'\n');print('PASS: only the two authorized files differ; other entries, modes and gitlinks equal')
