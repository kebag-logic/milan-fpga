#!/usr/bin/env python3
"""Prove parent retention and shared mutation/measurement inventories."""
import ast, json, os, pathlib, subprocess, tempfile
ROOT=pathlib.Path.cwd()
ENV=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
HEAD="33b311f5213f1fb8b47916ace9b8d872538a90e4"
PARENT="64e62816ad21791f6df3657fadb935aec5555881"
SOURCE="708e5634f28e6e5a19236a9b0a9a543c3622e52d"
BASE="910f338db"
def git(*args): return subprocess.check_output(["git",*args],env=ENV,stderr=subprocess.DEVNULL)
def paths(a,b): return set(git("diff","--name-only",a,b).decode().splitlines())
def blob(rev,path): return git("show",rev+":"+path).decode()
assert git("rev-parse","HEAD").decode().strip()==HEAD
assert git("rev-parse","HEAD^{tree}").decode().strip()=="52b4e42eca3d57c74ede894a9452dcad0af42862"
assert git("rev-parse",PARENT+"^{tree}")==git("rev-parse","09f1841bd2c6a9dea8eb1994d887f7386ca4f62d^{tree}")
ours=paths(BASE,SOURCE); theirs=paths(BASE,PARENT); overlap=ours & theirs
print("PR paths:",len(ours),"predecessor paths:",len(theirs))
print("Overlap:",json.dumps(sorted(overlap),indent=2))
expected={"sw/firmware/ctrl/README.md","sw/firmware/ctrl/mbx/mbx.h","sw/firmware/ctrl/test/ctrl_mutants.py","sw/firmware/gtest/README.md","sw/firmware/gtest/coverage.ratchet"}
assert overlap==expected
assert paths(PARENT,HEAD)==ours
for rev,files in ((SOURCE,ours-theirs),(PARENT,theirs-ours)):
 for path in files: assert git("ls-tree",rev,path)==git("ls-tree",HEAD,path),path
print("All unshared entries preserve their owning source blob and mode.")
for path in sorted(overlap):
 with tempfile.TemporaryDirectory() as tmp:
  names=[]
  for n,rev in enumerate((PARENT,BASE,SOURCE)):
   f=pathlib.Path(tmp)/str(n);f.write_text(blob(rev,path));names.append(str(f))
  r=subprocess.run(["git","merge-file","-p",*names],capture_output=True)
  assert r.returncode==0,(path,r.returncode)
  assert r.stdout==git("show",HEAD+":"+path),path
 print("Raw three-way merge exactly retained:",path)
def arms(rev):
 tree=ast.parse(blob(rev,"sw/firmware/ctrl/test/ctrl_mutants.py"))
 values=next(n.value.elts for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="MUTANTS" for t in n.targets))
 result={v.args[0].value:ast.dump(v,include_attributes=False) for v in values}
 assert len(result)==len(values)
 return result
sets={rev:arms(rev) for rev in (BASE,PARENT,SOURCE,HEAD)}
for rev in (PARENT,SOURCE):
 for name,value in sets[rev].items(): assert sets[HEAD][name]==value,(rev,name)
assert set(sets[HEAD])==set(sets[PARENT])|set(sets[SOURCE])
print("Mutation inventories:",json.dumps({k:len(v) for k,v in sets.items()}))
print("Source-only mutations:",sorted(set(sets[SOURCE])-set(sets[BASE])))
print("Predecessor-only mutations:",sorted(set(sets[PARENT])-set(sets[BASE])))
print("Every mutation definition from both parents survives exactly.")
def ratchet(rev):return dict(line.split("  ",1) for line in blob(rev,"sw/firmware/gtest/coverage.ratchet").splitlines() if line and not line.startswith("#"))
r0=ratchet(BASE); rp=ratchet(PARENT); rs=ratchet(SOURCE); rh=ratchet(HEAD)
for key in rh:
 expected=rs[key] if rs[key]!=r0[key] else rp[key]
 assert rh[key]==expected,key
 print("Ratchet:",key,rh[key])
h=blob(HEAD,"sw/firmware/ctrl/mbx/mbx.h")
assert all(t in h for t in ("mbx_filter_set_own_mac","mbx_filter_mismatch","No synchronous callbacks"))
for pattern in (".github/workflows","scripts/ci_events.py","scripts/ci_scope.py","scripts/ci_rv32_sdk.py","scripts/run_all_suites.sh","sw/firmware/gtest/fw_rv32.py","sw/firmware/gtest/rv32_include/assert.h"):
 assert not git("diff",SOURCE,HEAD,"--",pattern),pattern
 print("Unchanged from reviewed source:",pattern)
for pattern in ("hdl","protocol-processor","gptp-processor","third_party/verilog-axis","sw/mailbox"):
 assert not git("diff",PARENT,HEAD,"--",pattern),pattern
 print("Unchanged from predecessor:",pattern)
print("PASS composition retention and inventories")
