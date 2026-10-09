#!/usr/bin/env python3
import io,json,pathlib,re,subprocess,sys,tarfile
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve(); work=packet/"scratch/full-assertion-probe"; tree=work/"tree"; tree.mkdir(parents=True,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(["git","-C",str(root),"archive","HEAD"]))) as t: t.extractall(tree,filter="data")
f=tree/"tests/test_port.cpp"; text=f.read_text(); text=text.replace("TEST(ExamplePort, DefersExpiryAndRetainsBlockedOutput) {","TEST(ExamplePort, DefersExpiryAndRetainsBlockedOutput) {\n    GTEST_ASSERT_LT(1, 2);",1); f.write_text(text)
commands=[("comments",[sys.executable,"scripts/check_comments.py"]),("needles",[sys.executable,"scripts/needle_audit.py","--selftest"]),("configure",["cmake","-S",str(tree),"-B",str(work/"build"),"-DCMAKE_BUILD_TYPE=Debug"]),("build",["cmake","--build",str(work/"build"),"--target","port_tests","-j16"]),("run",[str(work/"build/port_tests"),"--gtest_output=xml:"+str(work/"port.xml")])]
rows=[]
for name,cmd in commands:
 r=subprocess.run(cmd,cwd=tree,capture_output=True,text=True); (work/(name+".log")).write_text(r.stdout+r.stderr); rows.append({"step":name,"rc":r.returncode}); print(name,r.returncode,flush=True)
 if r.returncode: break
result={"source_head":subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip(),"addition":"GTEST_ASSERT_LT(1, 2);","path":"tests/test_port.cpp:9","steps":rows}
(packet/"receipts/full-assertion-probe.json").write_text(json.dumps(result,indent=2)+"\n")
assert len(rows)==5 and all(x["rc"]==0 for x in rows)
