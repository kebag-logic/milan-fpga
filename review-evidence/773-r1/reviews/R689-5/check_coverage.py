#!/usr/bin/env python3
"""Check a signed local-CI manifest's coverage map against workflow definitions.

Usage: python3 -I check_coverage.py <repo> <manifest.json> <hosted_jobs.json> <hosted_merge_ref.json>

Run from any directory; reads workflow files with `git show <rev>:<path>` in <repo>.
Prints one line per check and exits non-zero if any check fails.
"""
import json
import subprocess
import sys

import yaml

repo, manifest_path, jobs_path, mref_path = sys.argv[1:5]
m = json.load(open(manifest_path))
hosted = json.load(open(jobs_path))
mref = json.load(open(mref_path))
cov = m["execution"]["coverage"]
act = m["execution"]["act"]["jobs"]
subj = m["subject"]
WF = {"docs": "docs.yml", "elaborate": "elaborate.yml", "rtl-fast": "rtl-fast.yml", "rtl": "rtl.yml"}
fails = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (f" ({detail})" if detail else ""))
    if not cond:
        fails.append(name)


def load(rev, f):
    return subprocess.check_output(["git", "-C", repo, "show", f"{rev}:.github/workflows/{f}"])


def legs(job, wname):
    """Expand a job's act leg names: '<workflow>/<name>-<k>' for matrix jobs."""
    mat = (job.get("strategy") or {}).get("matrix")
    if not mat:
        return None
    shards, total = mat["shard"], mat["total"]
    assert len(total) == 1
    tmpl = job["name"]
    out = []
    for k, s in enumerate(shards, 1):
        n = tmpl.replace("${{ matrix.shard }}", str(s)).replace("${{ matrix.total }}", str(total[0]))
        out.append(n if wname is None else f"{wname}/{n}-{k}")
    return out


import hashlib

for side, rev in (("head", subj["head"]), ("candidate", subj["candidate"])):
    for wf, f in WF.items():
        h = hashlib.sha256(load(rev, f)).hexdigest()
        check(f"definitions.{side}.{f} equals git {rev[:8]}", m["definitions"][side][f] == h, h[:12])

check("subject.candidate tree", subprocess.check_output(["git", "-C", repo, "rev-parse", subj["candidate"] + "^{tree}"]).decode().strip() == subj["candidate_tree"])
check("subject.head tree", subprocess.check_output(["git", "-C", repo, "rev-parse", subj["head"] + "^{tree}"]).decode().strip() == subj["head_tree"])
check("subject.candidate_parent is candidate^1", subprocess.check_output(["git", "-C", repo, "rev-parse", subj["candidate"] + "^1"]).decode().strip() == subj["candidate_parent"])

head_wf = {wf: yaml.safe_load(load(subj["head"], f)) for wf, f in WF.items()}
cand_wf = {wf: yaml.safe_load(load(subj["candidate"], f)) for wf, f in WF.items()}

expected = {f"{wf}/{jid}" for wf, w in head_wf.items() for jid in w["jobs"]}
expected_c = {f"{wf}/{jid}" for wf, w in cand_wf.items() for jid in w["jobs"]}
check("candidate and head define the same job ids", expected == expected_c)
check("coverage keys == every job id of the four workflows", set(cov) == expected,
      f"{len(cov)} keys, {len(expected)} jobs; missing={sorted(expected - set(cov))} extra={sorted(set(cov) - expected)}")
check("every coverage entry ok is true", all(v.get("ok") is True for v in cov.values()))

used_act = set()
for key, v in sorted(cov.items()):
    wf, jid = key.split("/", 1)
    w = head_wf[wf]
    wname = w["name"]
    job = w["jobs"][jid]
    disp = job.get("name") or jid
    if v["by"] == "act":
        exp_legs = legs(job, wname)
        if exp_legs:
            got = v.get("act_jobs", [])
            check(f"{key}: matrix lists all its act legs", sorted(got) == sorted(exp_legs), f"{len(got)}/{len(exp_legs)}")
            names = got
        else:
            names = [v["act_job"]]
            check(f"{key}: act_job names this job", v["act_job"] == f"{wname}/{disp}", v["act_job"])
        for n in names:
            check(f"{key}: act result {n} is success", act.get(n) == "success", str(act.get(n)))
            used_act.add(n)
    elif v["by"] == "not-run":
        check(f"{key}: named not-run reason", bool(v.get("reason")))
        n = f"{wname}/{disp}"
        check(f"{key}: act shows {n} skipped", act.get(n) == "skipped", str(act.get(n)))
        used_act.add(n)
    else:
        check(f"{key}: by is act or not-run", False, v["by"])

check("every act job is mapped by exactly one coverage entry", used_act == set(act), f"unmapped={sorted(set(act) - used_act)}")

# candidate matrix for rtl/verilator-shards
cm = cov["rtl/verilator-shards"]["candidate_matrix"]
cand_legs = legs(cand_wf["rtl"]["jobs"]["verilator-shards"], None)
names = [leg["name"] for leg in cm["legs"]]
check("candidate_matrix legs == candidate rtl.yml legs, each once", sorted(names) == sorted(cand_legs) and len(set(names)) == len(names), f"{len(names)} legs vs {len(cand_legs)}")
hj = {j["name"]: j for j in hosted}
for leg in cm["legs"]:
    j = hj.get(leg["name"])
    check(f"hosted {leg['name']}: job id and conclusion match", j is not None and j["id"] == leg["job_id"] and j["conclusion"] == leg["conclusion"] == "success" and j["run_attempt"] == 1,
          f"{leg['job_id']}")
check("run URL is 40152466723", cm["run"].endswith("/actions/runs/40152466723"))
check("hosted run has no other Verilator shard job", sum(1 for j in hosted if j["name"].startswith("Verilator shard ")) == 17)
check("merge ref tree == candidate tree", mref["tree"] == subj["candidate_tree"], mref["tree"][:12])
check("merge ref parents == (candidate_parent, head)", mref["parents"] == [subj["candidate_parent"], subj["head"]])
phys = [j for j in hosted if j["name"] == "Physical gPTP (nightly and manual)"]
check("hosted Physical gPTP skipped too", len(phys) == 1 and phys[0]["conclusion"] == "skipped")
print("RESULT", "PASS" if not fails else f"FAIL {len(fails)}")
sys.exit(1 if fails else 0)
