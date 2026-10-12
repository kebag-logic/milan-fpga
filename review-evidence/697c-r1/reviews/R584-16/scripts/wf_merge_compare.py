#!/usr/bin/env python3
"""Compare rtl-fast.yml jobs across merge base, lane parent, dev parent and head.

Usage: wf_merge_compare.py <repo> <base> <lane> <dev> <head>
Prints, per job, which side it comes from and whether the head equals that
side (modulo the tsn-c-stack fetch the lane adds to every firmware job), and
the aggregate's needs/env/loop sets.
"""
import re
import subprocess
import sys

import yaml

WF = ".github/workflows/rtl-fast.yml"


def load(repo, rev):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{WF}"],
                          check=True, capture_output=True, text=True).stdout
    return yaml.safe_load(text), text


def norm(job):
    """Drop the lane's tsn-c-stack addition so dev jobs compare to dev."""
    s = yaml.safe_dump(job, sort_keys=True)
    return s.replace(" third_party/tsn-c-stack", "")


def main():
    repo, base, lane, dev, head = sys.argv[1:6]
    docs = {n: load(repo, r)[0] for n, r in
            (("base", base), ("lane", lane), ("dev", dev), ("head", head))}
    jobs = {n: d["jobs"] for n, d in docs.items()}
    names = sorted(set().union(*[set(j) for j in jobs.values()]))
    bad = 0
    # top-level keys other than jobs
    for k in sorted(set(docs["head"]) | set(docs["lane"]) | set(docs["dev"]), key=str):
        if k == "jobs":
            continue
        h, l, d, b = (docs[x].get(k) for x in ("head", "lane", "dev", "base"))
        exp = l if l != b else d
        ok = h == exp
        print(f"TOP {k!s:12} head==expected:{ok}")
        bad += not ok
    for n in names:
        present = {k: n in v for k, v in jobs.items()}
        if not present["head"]:
            print(f"JOB {n:28} MISSING AT HEAD present={present}")
            bad += 1
            continue
        h = jobs["head"][n]
        res = []
        for side in ("lane", "dev"):
            if present[side]:
                res.append(f"{side}:{'eq' if h == jobs[side][n] else ('eq-modulo-tsn' if norm(h) == norm(jobs[side][n]) else 'DIFF')}")
        b_eq = present["base"] and h == jobs["base"][n]
        print(f"JOB {n:28} {' '.join(res)} base:{'eq' if b_eq else ('n/a' if not present['base'] else 'diff')}"
              f" timeout={h.get('timeout-minutes')} needs={h.get('needs')}")
    # firmware jobs fetch tsn-c-stack
    for n, j in jobs["head"].items():
        for st in j.get("steps", []):
            run = st.get("run", "") or ""
            if "submodule update" in run and n.startswith("firmware"):
                print(f"FETCH {n:26} tsn-c-stack:{'third_party/tsn-c-stack' in run}")
    # aggregate
    for n, j in jobs["head"].items():
        if isinstance(j.get("needs"), list) and len(j["needs"]) > 4:
            env = set(j.get("env", {}) or {})
            for st in j.get("steps", []):
                env |= set((st.get("env") or {}))
                run = st.get("run", "") or ""
                loop = re.findall(r'"([a-z0-9-]+):\$', run)
                if loop:
                    print(f"AGG {n} loop={loop}")
            print(f"AGG {n} needs={j['needs']}")
            print(f"AGG {n} env={sorted(env)}")
            for side in ("lane", "dev", "base"):
                if n in jobs[side]:
                    print(f"AGG {n} {side}-needs={jobs[side][n]['needs']}")
            fw_jobs = [k for k in jobs["head"] if k.startswith("firmware")]
            missing = [k for k in fw_jobs if k not in j["needs"]]
            print(f"AGG {n} firmware jobs missing from needs: {missing}")
    print("BAD", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
