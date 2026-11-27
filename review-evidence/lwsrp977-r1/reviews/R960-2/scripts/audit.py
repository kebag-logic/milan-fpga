#!/usr/bin/env python3
"""Audit downloaded public evidence and exact checkout; no source writes.
Usage: python3 -B scripts/audit.py CHECKOUT PACKET
Public downloads belong under PACKET/scratch/public; hashes use MANIFEST.json.
"""
import collections, hashlib, importlib.util, json, os, pathlib, re, stat, subprocess, sys
sys.dont_write_bytecode = True
repo, packet = [pathlib.Path(x).resolve() for x in sys.argv[1:3]]
out = packet/"receipts"
public = packet/"scratch/public"
def git(*args):
    return subprocess.check_output(["git",*args],cwd=repo)
def module(name):
    spec=importlib.util.spec_from_file_location(name,repo/"tests"/(name+".py"))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def save(name,d):
    (out/name).write_text(json.dumps(d,indent=2)+"\n")
m=json.loads((public/"MANIFEST.json").read_text())
hashes=[]
for row in m:
    p=public/row["file"]
    if p.is_file():
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        hashes.append({**row,"actual_sha256":actual,"match":actual==row["published_sha256"]})
assert all(x["match"] for x in hashes)
save("public-hashes.json",hashes)
cr=module("check_reversals");cd=module("check_differential")
gates=public/"author-r2/receipts/gates"
reversals=[]
for p in sorted(gates.glob("*.summary.json")):
    d=json.loads(p.read_text())
    expected=[c[0] for c in cr.CASES if cr.selection(c[0],d["scale"],d["end_station"]) is None]
    log=p.with_name(p.name.replace(".summary.json",".log")).read_text()
    killed=re.findall(r"^KILLED (\S+)$",log,re.M)
    skips=re.findall(r"^SKIP ([^:]+):",log,re.M)
    ok=(d["listed"]==len(cr.CASES) and d["selected"]==expected and
        set(d["results"])==set(expected) and len(killed)==len(expected) and
        set(killed)==set(expected) and set(skips)==set(d["skipped"]) and
        len(skips)==len(d["skipped"]) and d["failures"]==0 and
        all(v=="killed" for v in d["results"].values()))
    reversals.append({"file":p.name,"milan":d["milan"],"scale":d["scale"],"end_station":d["end_station"],
                      "listed":d["listed"],"selected":len(expected),"killed":len(killed),
                      "skipped":len(skips),"reconciled":ok})
assert all(x["reconciled"] for x in reversals)
diffs=[]
for p in sorted(gates.glob("*.differential.json")):
    d=json.loads(p.read_text()); expected={x[0] for x in cd.MUTANTS}|{cd.LEAN_READ[0]}
    assert set(d["killed"])==expected and len(d["killed"])==39 and not d["problems"]
    assert len(cd.MUTANTS)==38 and len(d["rows"])==22
    assert all(r["identical"]+r["excused"]==r["seeds"]==200 for r in d["rows"])
    diffs.append({"file":p.name,"base":d["base"],"milan":d["milan"],"killed":len(d["killed"]),
                  "mutation_inventory":len(cd.MUTANTS),"problems":d["problems"],
                  "rows":d["rows"]})
units=(gates/"units.log").read_text()
unit_lines=[x for x in units.splitlines() if ": unit rc=" in x]
assert len(unit_lines)==18 and all("unit rc=0 ctest rc=0" in x for x in unit_lines)
save("evidence-audit.json",{"public_files_verified":len(hashes),"reversals":reversals,
    "differential":diffs,"unit_runs":unit_lines,
    "count_control_tail":(public/"author-r2/receipts/probes/reversal-count-plant.log").read_text().splitlines()[-3:],
    "named_failures":(public/"author-r2/receipts/named-failures.txt").read_text()})
anchors=[]
for doc in ["README.md",*git("ls-files","doc/*.md").decode().splitlines()]:
    try: old=git("show","73007b48:"+doc).decode()
    except subprocess.CalledProcessError: continue
    new=(repo/doc).read_text()
    pattern=r"\[([^\]]+)\]\(([^)#]+)#L(\d+)\)"
    before=collections.defaultdict(list)
    for label,path,line in re.findall(pattern,old): before[(label,path)].append(int(line))
    for label,path,line in re.findall(pattern,new):
        if not before[(label,path)]: continue
        prior=before[(label,path)].pop(0);line=int(line)
        if prior==line: continue
        target=os.path.normpath(os.path.join(os.path.dirname(doc),path))
        oldline=git("show","73007b48:"+target).decode().splitlines()[prior-1]
        newline=(repo/target).read_text().splitlines()[line-1]
        anchors.append({"doc":doc,"label":label,"target":target,"old":prior,"new":line,
                        "same_target_text":oldline==newline,"target_text":newline})
save("anchors.json",anchors)
assert all(x["same_target_text"] for x in anchors)
entries=[]
for item in git("ls-tree","-rz","--full-tree","HEAD").split(b"\0"):
    if not item:continue
    meta,path=item.split(b"\t",1); mode,kind,blob=meta.decode().split(); path=path.decode()
    if kind=="commit":
        entries.append({"path":path,"mode":mode,"blob":blob,"gitlink":True});continue
    p=repo/path
    data=os.readlink(p).encode() if p.is_symlink() else p.read_bytes()
    actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    actual_mode="120000" if p.is_symlink() else ("100755" if p.stat().st_mode & stat.S_IXUSR else "100644")
    entries.append({"path":path,"mode":mode,"blob":blob,"actual_blob":actual,"actual_mode":actual_mode,
                    "match":actual==blob and actual_mode==mode})
tracked_pycs=git("ls-files","*.pyc").decode().splitlines()
added=git("diff","73007b48..HEAD","--","src").decode().splitlines()
suspect=[x for x in added if x.startswith("+") and not x.startswith("+++") and
         re.search(r"\b(?:R\d{3}|A\d{3}|B\d{2})\b|issuecomment-|review round|/home/|/srv/|/data/",x)]
integrity={"head":git("rev-parse","HEAD").decode().strip(),"tree":git("rev-parse","HEAD^{tree}").decode().strip(),
           "entries":entries,"gitlinks":[x for x in entries if x.get("gitlink")],
           "index_diff":git("diff","--cached","--raw","HEAD").decode(),
           "worktree_diff":git("diff","--raw","HEAD").decode(),
           "status":git("status","--porcelain=v1","--untracked-files=all").decode(),
           "tracked_pycs":tracked_pycs,"source_comment_scan_hits":suspect}
save("integrity.json",integrity)
assert integrity["head"]=="50a2106483141fcd7d1b20654bcf0803e7c3020a"
assert integrity["tree"]=="74f0d3e54480d8c841c66d0958a2b3a9fe20d789"
assert all(x.get("match",True) for x in entries)
assert not any(integrity[k] for k in ("gitlinks","index_diff","worktree_diff","status","tracked_pycs","source_comment_scan_hits"))
print("Public files verified:",len(hashes))
print("Reversal selections reconciled:",len(reversals))
print("Differential summaries reconciled:",len(diffs),"with 38 ordinary plants plus one sanitizer control")
print("Unit configurations reconciled:",len(unit_lines))
print("Moved anchors preserve target text:",len(anchors))
print("Tracked bytes/modes verified:",len(entries),"; index/worktree clean; no gitlinks or tracked bytecode")
