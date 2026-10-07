#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe for PR #690 round 3: the published SRP plants and independent plants.

Usage: probe_srp.py --repo <checkout at the head> --out <scratch dir> --workers N
                    [--author] [--reviewer] [--baseline]

--author   replays every plant in sw/firmware/ctrl/test/srp_mutants.py at IF=2 and
           requires its named test to catch it (the lane's own predicate).
--reviewer plants the reviewer's own defects at the round-3 change sites and runs the
           WHOLE srp_mbx.cpp suite at IF=1 and IF=2, recording every failing test.
--baseline runs the unmodified srp_mbx.cpp suite at IF=1 and IF=2.
Each plant edits a private copy of sw/firmware/ctrl; the checkout is never written.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

# (name, old text, new text, intent). old must occur exactly once in srp/srp_mbx.c.
REVIEWER = [
    ("RP1-drop-vlan-requested-inheritance",
     "replacement.vlan_requested |= r->vlan_requested;", "(void)0;",
     "R533-2-F1: replacement forgets that the shared VID was already requested"),
    ("RP2-drop-vlan-sent-inheritance",
     "replacement.vlan_sent |= r->vlan_sent;", "(void)0;",
     "R533-2-F1: replacement forgets the committed VID, so a retained Ready must wait or leave"),
    ("RP3-declared-only-from-replaced-slot",
     "replacement.declared |= r->declared;", "if (r == s) { replacement.declared |= r->declared; }",
     "R533-2-F1: a new shared binding does not inherit the Applicant held by another slot"),
    ("RP4-judge-without-replacement",
     "    const struct srp_sink old = *s;\n    *s = replacement;\n    if (old.bound) {",
     "    const struct srp_sink old = *s;\n    s->bound = false;\n    if (old.bound) {",
     "R533-2-F1: withdrawal judged before the replacement joins the set (replacement then lost)"),
    ("RP5-withdraw-domain-vid-on-unbind",
     "if (old.vid != i->domain.vid && !has_sink(i,&old,false))", "if (!has_sink(i,&old,false))",
     "R532-2-F3: the last binding on the Domain VID withdraws the Domain's own VLAN"),
    ("RP6-attach-assumes-up",
     "m->ifs[n].link = mbx_link_up(n);", "m->ifs[n].link = true;",
     "R532-2-F1: attach assumes up instead of reading the level"),
    ("RP7-poll-edge-not-seen",
     "            i->link = link;\n            i->link_seen = true;", "            i->link = link;",
     "R532-2-F1: a poll-observed edge does not mark the link as seen"),
    ("RP8-poll-up-edge-without-reset",
     "            reset_interface(i);\n            i->link = link;",
     "            if (!link) { reset_interface(i); }\n            i->link = link;",
     "R532-2-F1: a poll-observed up edge keeps the down-period participants"),
    ("RP9-vlan-inheritance-any-vid",
     "            if (r->vid == vid) {", "            if (true) {",
     "R533-2-F1: replacement inherits another VID's committed membership (Milan 4.3.2)"),
    ("RP10-declared-inheritance-any-stream",
     "            if (memcmp(r->stream_id.bytes,identity->bytes,8) == 0) {", "            if (true) {",
     "R533-2-F1: replacement inherits another StreamID's Applicant"),
    ("RP11-unbind-shared-vid-while-bound",
     "if (old.vid != i->domain.vid && !has_sink(i,&old,false))", "if (old.vid != i->domain.vid)",
     "R532-2-F3: a VID still used by another binding is withdrawn"),
    ("RP12-poll-reconcile-skips-down-edge",
     "        if (i->link != link) {", "        if (!i->link && link) {",
     "R532-2-F1: only the up edge is reconciled from the level"),
]


def setup(repo: Path):
    sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
    sys.path.insert(0, str(repo / "sw/firmware/gtest"))
    import ctrl_build, fw_gtest, srp_arms, srp_mutants  # noqa: E401
    return ctrl_build, fw_gtest, srp_arms, srp_mutants


FAIL = re.compile(r"^\[FAIL\] ([A-Za-z0-9_.]+):", re.M)
GFAIL = re.compile(r"^\[  FAILED  \] ([A-Za-z0-9_.]+)", re.M)
PASSED = re.compile(r"^\[  PASSED  \] (\d+) test", re.M)


def failing(log: str) -> list[str]:
    return sorted(set(FAIL.findall(log)) | set(GFAIL.findall(log)))


def one(job):
    kind, repo, out, name, old, new, ifs, test, needle = job
    repo, out = Path(repo), Path(out)
    ctrl_build, fw_gtest, srp_arms, srp_mutants = setup(repo)
    work = out / "work" / name
    src = work / "ctrl"
    if src.exists():
        shutil.rmtree(work)
    shutil.copytree(repo / "sw/firmware/ctrl", src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    path = src / (job_path := "srp/srp_mbx.c")
    if old is not None:
        text = path.read_text()
        n = text.count(old)
        if n != 1:
            return {"name": name, "kind": kind, "error": f"{n} planting sites"}
        path.write_text(text.replace(old, new))
    rows = []
    for nif in ifs:
        build = fw_gtest.Build(jobs=2)
        tree = ctrl_build.Tree(src, work / f"build{nif}", work / f"reuse{nif}", build)
        sel = ("srp_mbx.cpp", "Srp." + test) if test else "srp_mbx.cpp"
        try:
            res = srp_arms.arm_srp(tree, repo / "third_party/lwSRP", nif, test=sel)
        except ctrl_build.Refusal as e:
            rows.append({"if": nif, "refusal": str(e)[:2000]})
            continue
        (out / "logs").mkdir(parents=True, exist_ok=True)
        (out / "logs" / f"{name}-if{nif}.log").write_text(res.log)
        row = {"if": nif, "rc": res.rc, "failing": failing(res.log)}
        m = PASSED.search(res.log)
        row["passed"] = int(m.group(1)) if m else None
        if kind == "author":
            row["caught"] = srp_mutants.caught("Srp." + test if "." not in test else test, needle, res)
        rows.append(row)
    shutil.rmtree(work, ignore_errors=True)
    return {"name": name, "kind": kind, "rows": rows}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--author", action="store_true")
    ap.add_argument("--reviewer", action="store_true")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    repo, out = a.repo.resolve(), a.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    _, _, _, srp_mutants = setup(repo)
    jobs = []
    if a.baseline:
        jobs.append(("baseline", str(repo), str(out), "baseline", None, None, (1, 2), "", ""))
    if a.reviewer:
        for name, old, new, _ in REVIEWER:
            jobs.append(("reviewer", str(repo), str(out), name, old, new, (1, 2), "", ""))
    if a.author:
        for d in srp_mutants.DEFECTS:
            if d.path != "srp/srp_mbx.c" or d.suite != "srp_mbx.cpp" or d.debug:
                jobs.append(("author-skip", str(repo), str(out), d.name, None, None, (), "", ""))
                continue
            jobs.append(("author", str(repo), str(out), d.name, d.old, d.new, (2,), d.test, d.needle))
    if a.only:
        keep = set(a.only.split(","))
        jobs = [j for j in jobs if j[3] in keep]
    results = []
    with ProcessPoolExecutor(a.workers) as pool:
        for r in pool.map(one, jobs):
            results.append(r)
            print(json.dumps(r), flush=True)
    tag = "-".join(k for k, v in (("baseline", a.baseline), ("reviewer", a.reviewer), ("author", a.author)) if v)
    (out / f"results-{tag or 'only'}.json").write_text(json.dumps(results, indent=1))
    shutil.rmtree(out / "work", ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
