#!/usr/bin/env python3
"""Focused review probes. Run from the reviewed clone; all disposable trees stay in packet/scratch."""
import concurrent.futures, hashlib, importlib.util, json, os, pathlib, subprocess, sys, tarfile, io, time
OUT=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path.cwd()
SCRATCH=OUT/"scratch"
def run(name,cmd,cwd=ROOT,expected=0):
    cached=OUT/(name+".rc.json")
    if cached.exists():
        row=json.loads(cached.read_text())
        assert row["command"]==cmd and row["rc"]==expected
        return row
    start=time.monotonic()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(SCRATCH))
    p=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=570)
    (OUT/(name+".log")).write_bytes(p.stdout)
    row=dict(name=name,command=cmd,rc=p.returncode,expected=expected,seconds=round(time.monotonic()-start,3))
    (OUT/(name+".rc.json")).write_text(json.dumps(row,indent=2)+"\n")
    assert p.returncode==expected,row
    return row
def archive(rev,label):
    if (SCRATCH/label/"AGENTS.md").exists():return SCRATCH/label
    dest=SCRATCH/label;dest.mkdir(exist_ok=True)
    data=subprocess.check_output(["git","archive",rev],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(data)) as t:t.extractall(dest,filter="data")
    return dest
old=archive("9acb9b82","old-nosub")
fixed=archive("c413d33a","fixed-nosub")
head=archive("HEAD","head-nosub")
jobs=[
 ("old-list",["python3","sw/builder/test_builder.py","--list"],old,2),
 ("fixed-list",["python3","sw/builder/test_builder.py","--list"],fixed,0),
 ("head-list",["python3","sw/builder/test_builder.py","--list"],head,0),
 ("fixed-planner",["python3","scripts/suite_shards.py","--selftest"],fixed,0),
 ("head-planner",["python3","scripts/suite_shards.py","--selftest"],ROOT,0),
 ("head-evidence-selftest",["python3","scripts/measure_test_evidence.py","--selftest"],ROOT,0),
 ("head-suite-workflows",["python3","scripts/ci_suite_workflows.py","--check"],ROOT,0),
 ("head-gate-workflows",["python3","scripts/ci_gate_workflows.py","--check"],ROOT,0),
 ("head-builder-focused",["python3","sw/builder/test_input_loopback.py"],ROOT,0),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows=list(pool.map(lambda a:run(*a),jobs))
baseline=SCRATCH/"public-packet/author-r6/receipts/repro--list-7bfae19-sub.json.txt"
a=(OUT/"fixed-list.log").read_bytes(); b=baseline.read_bytes()
# Published receipts prepend a source-binding header; compare exact payload bytes.
b=b[b.index(b'["test_soc_option_refusals"'):]
assert a==b
assert a==(OUT/"head-list.log").read_bytes()
inventory=json.loads(a)
print("inventory matches published prior-submodule inventory byte-for-byte",hashlib.sha256(a).hexdigest())
print("inventory type",type(inventory).__name__,"entries",len(inventory))
for label,cwd,n in [("fixed",fixed,19),("head",ROOT,27)]:
    union=[]
    for i in range(n):
        rows.append(run(f"{label}-shard-{i}",["python3","scripts/suite_shards.py","--suite-root","tb/verilator","--ci-pieces","--shard",f"{i}/{n}"],cwd))
        union.extend((OUT/f"{label}-shard-{i}.log").read_text().split())
    assert len(union)==len(set(union)),(label,"duplicate selections")
    for name in ("input_loopback","input_loopback_dp"):assert union.count(name)==1
    print(label,"all",n,"listings pass; unique selections",len(union))
sys.path.insert(0,str(ROOT/"scripts"))
import measure_test_evidence as evidence
driver=(ROOT/"scripts/run_all_suites.sh").read_text()
assert not evidence.runner_contract(driver)
for name in ("input_loopback","input_loopback_dp"):
    line=next(l for l in driver.splitlines(True) if l.strip().startswith(name+")"))
    assert evidence.runner_contract(driver.replace(line,"")),(name,"deletion escaped")
    assert evidence.runner_contract(driver.replace(line,line.replace(":-300",":-301"))),(name,"budget mutation escaped")
    print(name,"timeout deletion and 301-second mutation rejected")
(OUT/"probe-results.json").write_text(json.dumps(rows,indent=2)+"\n")
print("PASS focused probes")

