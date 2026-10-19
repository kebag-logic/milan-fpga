#!/usr/bin/env python3
"""Independently reconcile the public round-3 packet. Run fetch_public.py first."""
import collections, hashlib, json, os, pathlib, re, shutil, subprocess, sys
P = pathlib.Path(__file__).resolve().parents[1]
PUB = P / "scratch/public"
R = PUB / "author-r3/receipts"
S = R / "round3/scripts"
OUT = P / "receipts"
TMP = P / "scratch/replay"
TMP.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(TMP)
M = {r["file"]: r for r in json.loads((OUT / "public-manifest.json").read_text())}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args, stem, expected=0):
    r = subprocess.run([sys.executable, "-I", "-B", *map(str,args)], capture_output=True)
    (OUT/f"{stem}.log").write_bytes(r.stdout+r.stderr)
    (OUT/f"{stem}.rc").write_text(str(r.returncode)+"\n")
    assert r.returncode == expected, (stem,r.returncode,r.stderr[-500:])
    return r.stdout.decode()
# The saved pre-publication round-2 index must match every retained original digest.
kept=[];directory=None
for l in (R/"round3/INDEX-round2.md").read_text().splitlines():
    if l.startswith("## "): directory=l[3:-1] if l.endswith("/") else None
    if directory is not None and (m:=re.match(r"\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|",l)):
        rel=(pathlib.Path(directory)/m[1]).as_posix()
        row=M[f"author-r3/receipts/{rel}"]
        assert row["original_sha256"]==m[3],rel
        assert digest(R/rel)==row["published_sha256"],rel
        kept.append(rel)
assert len(kept)==1475
# Index hashes use pre-publication bytes; reconcile redacted files through the manifest.
listed={};directory=None
for l in (R/"INDEX.md").read_text().splitlines():
    if l.startswith("## "): directory=l[3:-1] if l.endswith("/") else None
    if directory is not None and (m:=re.match(r"\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|",l)):
        rel=(pathlib.Path(directory)/m[1]).as_posix();listed[rel]=m[3]
        assert M[f"author-r3/receipts/{rel}"]["original_sha256"]==m[3],rel
actual={p.relative_to(R).as_posix() for p in R.rglob("*") if p.is_file() and p.name!="INDEX.md"}
assert actual==set(listed),(len(actual),len(listed),actual-set(listed))
(OUT/"preservation-index.json").write_text(json.dumps({"saved_index_original_digests_match":len(kept),"publication_hashes_verified":True,"new_index_files":len(listed),"new_index_complete":True,"publication_redactions_reconciled":True},indent=2)+"\n")
# Inputs: original digests in receipt, published hashes at the immutable commit.
input_hashes={l.split(None,2)[2]:l.split()[0] for l in (R/"round3/inputs.sha256").read_text().splitlines()}
def original_dir(label):
    return R/"head-campaigns/out" if label=="r1b/head" else R/label/"campaigns/out"
def record_file(label,c):
    for f in [original_dir(label)/c/"results.json", R/"round3/records"/label/c/"results.json"]:
        if f.exists(): return f
    return None
def fail_id(s):
    return re.search(r"(?:\[[^\]]*\]\s*)?([A-Za-z][A-Za-z0-9_.-]*)",s)[1]
prepared={};extract_checks=0
def prepare(label,c):
    global extract_checks
    key=(label,c)
    if key in prepared:return prepared[key]
    f=record_file(label,c)
    assert f is not None,key
    assert input_hashes[f"{label}/{c}/results.json"]==M[f.relative_to(PUB).as_posix()]["original_sha256"],key
    dest=TMP/"inputs"/label/c;dest.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(f,dest/"results.json")
    rows=json.loads(f.read_text());logs={}
    if c=="aecp_dispatch":
        extract=R/"round3/records"/label/c/"fail-lines.txt"
        for line in extract.read_text().splitlines():
            if line.startswith("== "): name=line[3:];assert name not in logs;logs[name]=[]
            else: assert line.startswith("FAIL:");logs[name].append(line)
        for name,lines in logs.items():
            (dest/name).write_text("\n".join(lines)+("\n" if lines else ""))
            full=original_dir(label)/c/name
            if full.exists():
                assert [l for l in full.read_text().splitlines() if l.startswith("FAIL:")]==lines
                extract_checks+=1
    groups=({}, {})
    for row in rows:
        if c=="aecp_dispatch":
            name=row["arm"];is_mutant="patch" in row
            assert is_mutant != name.startswith("control ")
            logfile=name+".log" if is_mutant else "control-"+name.removeprefix("control ")+".log"
            fails=[x[5:].strip() for x in logs[logfile]]
            if is_mutant: assert len(fails)==row["failures"] and row["rc"]!=0 and row["named"]>0
            else: assert row["rc"]==0
        elif c=="name_state":
            name=row["name"];is_mutant=name!="golden"
            assert row["build_rc"]==0 and all(x["completed"] for x in row["runs"])
            fails=[f for r in row["runs"] for f in r["failures"]]
        else:
            name=row["mutant"];is_mutant=bool(row["named_checks"])
            assert is_mutant != name.startswith("golden-")
            assert row["build_rc"]==0 and row["completed"] and not row["missing"]
            fails=row["failing_checks"]
        assert row["verdict"]==("KILLED" if is_mutant else "PASS")
        assert bool(fails)==is_mutant
        target=groups[0 if is_mutant else 1];assert name not in target
        target[name]=(row["verdict"],tuple(sorted(fail_id(x) for x in fails)))
    prepared[key]=(dest,groups)
    return prepared[key]
def diff(a,b):
    common=set(a)&set(b);changed=sorted(n for n in common if a[n]!=b[n])
    return {"unchanged":len(common)-len(changed),"changed":changed,"added":sorted(b.keys()-a.keys()),"removed":sorted(a.keys()-b.keys())}
results=[]
for f in sorted((R/"round3/compare").rglob("*.json")):
    claim=json.loads(f.read_text());c=claim["campaign"];txt=f.with_suffix(".txt").read_text()
    labels=re.search(r"records: base (\S+), head (\S+)",txt).groups()
    assert f.with_suffix(".rc").read_text().strip()=="0"
    if c=="acmp":
        # Full ACMP result records exceed the public size cap. Use the explicitly
        # named JSON-line campaign roster for population, never filesystem logs.
        groups=[]
        for label in labels:
            log=R/"head-campaigns/acmp.log" if label=="r1b/head" else R/label/"campaigns/acmp.log"
            rows=[json.loads(l) for l in log.read_text().splitlines() if l.startswith("{")]
            mut={r["mutant"]:r["verdict"] for r in rows if not r["mutant"].startswith("golden-")}
            bas={r["mutant"]:r["verdict"] for r in rows if r["mutant"].startswith("golden-")}
            assert set(mut.values())=={"KILLED"} and set(bas.values())=={"PASS"}
            assert all(not r.get("missing") for r in rows)
            groups.append((mut,bas))
        (bm,bb),(hm,hb)=groups
        coverage="explicit campaign roster/verdicts; full failure-ID records omitted by public size cap"
    else:
        (b,(bm,bb)),(h,(hm,hb))=[prepare(label,c) for label in labels]
        got=TMP/f.name
        replay=run([S/"r3_failsets.py",c,b,h,"--json",got],"replay-"+f.parent.name+"-"+f.stem)
        parsed=json.loads(got.read_text())
        adjusted=dict(claim)
        for side,d in [("base",b),("head",h)]:adjusted[f"{side}_sha256"]=digest(d/"results.json")
        assert parsed==adjusted,f
        expected=txt.replace(f"records: base {labels[0]}, head {labels[1]}\n","")
        for side in ["base","head"]:expected=expected.replace(claim[f"{side}_sha256"],adjusted[f"{side}_sha256"])
        assert replay==expected,f
        coverage="complete comparison replay and independent failure-ID/verdict reconciliation"
    independent={"base_mutants":len(bm),"head_mutants":len(hm),"base_baselines":len(bb),"head_baselines":len(hb),"mutants":diff(bm,hm),"baselines":diff(bb,hb),"baselines_clean_at_both":len(set(bb)&set(hb))}
    for k,v in independent.items():assert claim[k]==v,(f,k,v,claim[k])
    for side,label in zip(["base","head"],labels):assert claim[f"{side}_sha256"]==input_hashes[f"{label}/{c}/results.json"]
    assert "MUTANTS: {} unchanged".format(claim["mutants"]["unchanged"]) in txt
    assert "BASELINES (not mutants):" in txt
    results.append({"comparison":f.relative_to(R).as_posix(),"coverage":coverage,**independent})
(OUT/"comparisons-audit.json").write_text(json.dumps({"comparisons":results,"raw_dispatch_extracts_crosschecked":extract_checks},indent=2)+"\n")
# The previous reviewer audit is executed byte-for-byte unchanged against author-r3.
audit=TMP/"prior-audit";audit.mkdir(exist_ok=True)
shutil.copyfile(PUB/"reviews/R668-2/audit_evidence.py",audit/"audit_evidence.py")
(audit/"receipts").mkdir(exist_ok=True)
if not (audit/"receipts/public").exists(): (audit/"receipts/public").symlink_to(R/"round2",target_is_directory=True)
run([audit/"audit_evidence.py"],"prior-audit-replay")
assert (audit/"evidence-audit.json").read_bytes()==(PUB/"reviews/R668-2/evidence-audit.json").read_bytes()
shutil.copyfile(audit/"evidence-audit.json",OUT/"evidence-audit-replayed.json")
run([S/"r3_reconcile.py",audit/"evidence-audit.json",PUB/"reviews/R668-2/evidence-audit.json",R/"round3/compare/round2"],"reconcile")
run([S/"r3_oldrows.py",R],"old-rows")
run([S/"r3_failsets_selftest.py",S/"r3_failsets.py",R/"round2/scripts/r1c_failsets.py"],"comparison-selftest")
# Extra reviewer probe: all five campaign baseline-only rosters, with an unrelated
# failing log present on both sides, must still yield zero mutants.
for c in ["notify","d3","acmp","aecp_dispatch","name_state"]:
    b=TMP/"baseline-only"/c;b.mkdir(parents=True,exist_ok=True)
    if c=="acmp": rows=[{"mutant":"golden-control","named_checks":[],"failing_checks":[],"verdict":"PASS"}]
    else:
        d,_=prepare("round2/base",c);raw=json.loads((d/"results.json").read_text())
        rows=[r for r in raw if r["verdict"]=="PASS"]
        if c=="aecp_dispatch":
            for r in rows:(b/("control-"+r["arm"].removeprefix("control ")+".log")).write_text("")
    (b/"results.json").write_text(json.dumps(rows));(b/"unlisted-failing.log").write_text("FAIL: XX1 unrelated\n")
    text=run([S/"r3_failsets.py",c,b,b],"baseline-only-"+c)
    assert "MUTANTS: 0 unchanged, 0 changed, 0 added, 0 removed" in text
# Reproduce the four planted comparison-script failures in disposable scratch.
plants=TMP/"plants"
run([S/"r3_plant.py",S/"r3_failsets.py",plants],"plant-comparison-controls")
for f in sorted(plants.glob("*.py")):
    run([S/"r3_failsets_selftest.py",f],"mutant-"+f.stem,expected=1)
# Regenerate the preservation map into a disposable receipt-shaped tree.
mapped=TMP/"mapped"
for section in ["round2/compare","r1c/compare","round3/compare"]:
    dest=mapped/section;dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():dest.symlink_to(R/section,target_is_directory=True)
run([S/"r3_supersedes.py",mapped],"supersedes-replay")
assert (mapped/"round3/SUPERSEDES.md").read_bytes()==(R/"round3/SUPERSEDES.md").read_bytes()
# Preserve the exact prior script as an independently re-runnable publication receipt.
shutil.copyfile(PUB/"reviews/R668-2/audit_evidence.py",P/"scripts/audit_evidence.py")
print(f"PASS: {len(results)} comparisons reconciled (13 complete replays; 3 ACMP roster/verdict checks); {len(kept)} retained original digests match saved index; index {len(listed)} files; prior audit byte-identical; selftest and five baseline-only/stray-log probes pass")
