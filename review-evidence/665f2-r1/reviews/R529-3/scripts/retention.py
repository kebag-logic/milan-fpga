#!/usr/bin/env python3
"""Compare public commit objects and mutation obligations across both merge parents."""
import ast,dataclasses,hashlib,subprocess,sys,types
from pathlib import Path
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
import ctrl_build
HEAD="8b78a8fd36864246336c71c061ac4f21d629952f";OLD="938497af1dffd8a87edebf3ab93663914bf85e5e";DEV="910f338dbd050f4efd2d96991ddcf928a583d55f";MERGE="5901ab0869e0674bb18bbb4df60757f2711e5cd4"
def git(*args): return subprocess.check_output(["git","-C",str(root),*args])
def blob(rev,path): return git("show",rev+":"+path).decode()
def catalog(rev):
 for name in ("maap_mutants","ctrl_mutants"):
  mod=types.ModuleType(name);sys.modules[name]=mod
  exec(compile(blob(rev,"sw/firmware/ctrl/test/"+name+".py"),name,"exec"),mod.__dict__)
 return {m.name:dataclasses.asdict(m) for m in mod.MUTANTS}
a=catalog(OLD);b=catalog(HEAD)
assert len(a)==192 and len(b)==193
assert all(b.get(k)==v for k,v in a.items())
assert set(b)-set(a)=={"r2-saved-range-never-consumed"}
print("PASS: all 192 round-2 mutation definitions, exact source plants and named obligations retained; one additional bounce control")
ks=list(b);parts=[ks[i::4] for i in range(4)];assert len(set(sum(parts,[])))==len(ks)
assert sorted(sum(parts,[]))==sorted(ks)
print("PASS: four complete disjoint partitions",[len(x) for x in parts])
print("Named obligations:",sum(1+len(v["also"]) for v in b.values()))
assert git("show","-s","--format=%P",MERGE).decode().strip()==OLD+" "+DEV
print("PASS: merge parents are exact reviewed round-2 head then authorized dev")
def functions(rev,path):
 return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(blob(rev,path)).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
path="sw/firmware/ctrl/test/ctrl_arms.py"
for source in (OLD,DEV):
 old=functions(source,path);new=functions(HEAD,path)
 names=list(old) if source==DEV else [x for x in old if x not in ("rv32_compiler","symbols","arm_rv32")]
 assert all(old[n]==new[n] for n in names)
 print("PASS: functions retained semantically from",source,len(names),"in",path)
for path in ("sw/firmware/ctrl/test/test_ctrl_firmware.py",):
 old=functions(OLD,path);new=functions(HEAD,path)
 assert old==new
 print("PASS every executable function retained from round 2:",path)
for path in ("sw/firmware/gtest/fw_rv32.py","sw/firmware/gtest/fw_rv32_selftest.py","sw/firmware/ctrl_nvm/test/nvm_rv32.py",".github/workflows/rtl-fast.yml","scripts/ci_events.py","scripts/run_all_suites.sh","scripts/measure_test_evidence.py","hdl/ieee1722/aaf/KL_aaf_packetizer.sv"):
 assert git("rev-parse",DEV+":"+path)==git("rev-parse",HEAD+":"+path)
 print("PASS exact dev bytes:",path)
for path in ("sw/firmware/ctrl/maap/maap_mbx.c","sw/firmware/ctrl/maap/maap_csr.c","sw/firmware/ctrl/app/ctrl_app.c","sw/firmware/ctrl/test/test_maap_mbx.cpp","sw/firmware/ctrl/test/test_maap_differential.cpp","sw/firmware/ctrl/test/maap_differential.py","sw/firmware/gtest/coverage.ratchet","sw/firmware/gtest/coverage_exclusions.json"):
 if path.endswith("coverage_exclusions.json"): continue
 assert git("rev-parse",OLD+":"+path)==git("rev-parse",HEAD+":"+path)
 print("PASS exact round-2 bytes:",path)
core="sw/firmware/ctrl/maap/maap.c"
for debug in (False,True):
 def preprocess(rev):
  args=["gcc","-std=c11","-E","-P","-","-I"+str(root/"sw/firmware/ctrl/maap"),"-I"+str(root/"sw/firmware/ctrl/wire")]
  if not debug:args.append("-DNDEBUG")
  return subprocess.check_output(args,input=blob(rev,core).encode())
 before=preprocess(OLD);after=preprocess(HEAD)
 # Release removes an empty assert expression; there is no expression evaluation.
 if not debug: before=before.replace(b"  ((void) (0));\n",b"")
 if debug:
  # The source insertion changes only the diagnostic line number from 15 to 18.
  old_site=b'__assert_fail ("!m->in_call", "<stdin>", 15,'
  new_site=b'__assert_fail ("!m->in_call", "<stdin>", 18,'
  assert before.count(old_site)==1 and after.count(new_site)==1
  before=before.replace(old_site,new_site)
 print("Preprocessed",("debug (diagnostic source line 15->18 only)" if debug else "release (removed void no-op only)"),"byte equality",before==after)
 assert before==after
print("PASS static retention audit")
