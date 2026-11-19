#!/usr/bin/env python3
"""Read-only delta and public receipt audit. Run from the candidate checkout."""
import ast, collections, difflib, hashlib, json, os, pathlib, re, subprocess
OUT = pathlib.Path(__file__).resolve().parent
ARCHIVE = "af70bbe3ceb299a0c65826df70c8bea492f28e0d"
OLD = "0d1eb8e4c5821e9431097950882659f2083d96ba"
HEAD = "f09d82e05270bdd77e07f7fc2e14d064c1123be8"
PREFIX = "review-evidence/951-r1/"
def git(*args):
    return subprocess.check_output(["git", *args], env={**os.environ, "GIT_NO_REPLACE_OBJECTS":"1"})
def blob(rev, path):
    return git("show", rev+":"+path)
def receipt(path):
    return blob(ARCHIVE, PREFIX+path).decode()
assert git("rev-parse","HEAD").decode().strip()==HEAD
assert git("rev-parse","HEAD^{tree}").decode().strip()=="13ff87928a0c2b9448475c2725c4f18fbc76f1dc"
manifest=json.loads(blob(ARCHIVE,PREFIX+"MANIFEST.json"))
checked=0
for row in manifest:
    if not row["file"].startswith(("author-r1/","author-r2/")): continue
    data=blob(ARCHIVE,PREFIX+row["file"])
    assert hashlib.sha256(data).hexdigest()==row["published_sha256"],row["file"]
    checked+=1
print("Published author packet hashes verified:",checked)
commit=git("cat-file","commit",ARCHIVE)
print("Archive commit signature:", "present" if b"\ngpgsig " in commit else "ABSENT; hash integrity only, not cryptographic signer authentication")
changes=git("diff","--name-only",OLD,HEAD).decode().splitlines()
print("Delta files:",len(changes))
cpaths=["sw/firmware/ctrl/srp/srp_mbx.c","sw/firmware/ctrl/test/srp_gate.hpp","sw/firmware/ctrl/test/srp_talker.cpp"]
pypath="tb/verilator/ctrl_service_budget/talker_notice.py"
assert set(changes)==set(cpaths+[pypath,"docs/design/MAILBOX_SPLIT.md","docs/design/SPLIT_CONTROL_MEMORY.md","sw/firmware/ctrl/srp/README.md","tb/verilator/ctrl_service_budget/README.md"])
for path in cpaths:
    a,b=blob(OLD,path).splitlines(),blob(HEAD,path).splitlines()
    assert len(a)==len(b),path
    changed=[(x,y) for x,y in zip(a,b) if x!=y]
    assert all(x.lstrip().startswith(b"//") and y.lstrip().startswith(b"//") for x,y in changed),path
    assert all(not x.rstrip().endswith(b"\\") and not y.rstrip().endswith(b"\\") for x,y in changed),path
    print("Only whole-line comments; equal line counts:",path,len(a),"changed",len(changed))
a,b=[ast.parse(blob(r,pypath)) for r in (OLD,HEAD)]
assert isinstance(a.body[0],ast.Expr) and isinstance(a.body[0].value,ast.Constant)
assert isinstance(b.body[0],ast.Expr) and isinstance(b.body[0].value,ast.Constant)
assert "nominal longest LeaveAll" in b.body[0].value.value
a.body.pop(0); b.body.pop(0)
assert ast.dump(a)==ast.dump(b)
print("Python AST identical after removing module docstring")
assert not git("diff",OLD,HEAD,"--","hdl",".gitmodules","scripts","third_party","protocol-processor","gptp-processor","sw/firmware/ctrl/test/srp_talker_mutants.py","sw/firmware/ctrl/test/srp_mutants.py")
print("RTL, interfaces, build drivers, mutations and gitlinks unchanged")
for name, count, pattern in [
    ("budget-hashes.txt",12,r"^(\S+ \S+) ([0-9a-f]{64})$"),
    ("platform-and-fixture-hashes.txt",8,r"^([0-9a-f]{64}) (\S+)$")]:
    t=receipt("author-r2/receipts/images/"+name)
    pairs=re.findall(pattern,t,re.M)
    assert len(pairs)==2*count
    assert pairs[:count]==pairs[count:]
    print("Published image hash pairs identical:",name,count)
for name in ("e7b0272b","f09d82e0"):
    t=receipt("author-r2/receipts/gates/"+name+"/docs-workflow-steps.txt")
    rows=re.findall(r"^(\d+)-.*? rc=(\d+) ",t,re.M)
    assert len(rows)==104 and [int(x[0]) for x in rows]==list(range(104))
    assert all(rc=="0" for _,rc in rows)
    assert "tracked files changed after the steps: 0" in t
    print("Published selected docs steps:",name,"104/104 rc=0; tracked changes=0")
deltas=collections.Counter()
rows=[]
for row in manifest:
    path=row["file"]
    if not (path.startswith("author-r1/receipts/images/pairs/") and path.endswith(".imgdiff.txt")): continue
    t=receipt(path)
    found={}
    for line in t.splitlines():
        m=re.match(r"  (\.\w+) (\w+) addr (0x[0-9a-f]+) size (0x[0-9a-f]+) \| \.\w+ \w+ addr (0x[0-9a-f]+) size (0x[0-9a-f]+)",line)
        if m:
            section,kind,aa,ss,bb,tt=m.groups()
            found[section]=(int(aa,16),int(bb,16),int(ss,16),int(tt,16))
    assert found[".text"][3]-found[".text"][2]==4,path
    ro=found[".rodata"]; shift=ro[1]-ro[0]; deltas[shift]+=1
    assert ro[2]==ro[3]
    for sec in (".data",".bss",".stack"):
        aa,bb,ss,tt=found[sec]; assert aa==bb and ss==tt,(path,sec)
    if "/platform-" in path: assert shift==0
    assert "inputs that differ by sha256: 1 of" in t and "srp_mbx.o" in t
    rel=receipt(path.replace(".imgdiff.txt",".relink.txt"))
    assert rel.count("loadable bytes EQUAL")==2
    rows.append((path.rsplit("/",1)[1],shift))
assert deltas=={0:13,8:7},deltas
print("Independent count from 20 original pair receipts: .rodata shifts",dict(deltas))
print("All 20 pairs: .text size +4; .data/.bss/.stack address and size unchanged; all 4 platform .rodata shifts zero")
for path,shift in rows: print(path,"rodata_shift",shift)
for row in manifest:
    path=row["file"]
    if path.startswith("author-r2/receipts/tests/") and path.endswith(".log"):
        t=receipt(path)
        m=re.search(r"\[  PASSED  \] (\d+) tests",t)
        assert m and int(m[1]) in (16,9) and "[  FAILED  ]" not in t
        print("Published focused test:",path.rsplit("/",1)[1],m[1],"passed")
print("AUDIT PASS")

