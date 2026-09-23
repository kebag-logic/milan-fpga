#!/usr/bin/env python3
"""Classify every arm page of the families present at base 88e9276b (walk,
tag, guard, heading, predecessor, provenance, refusal, I440) and of the
A172 I437 family under the base, a172 and working-tree walks; report every
page whose blocks() or headings() differ between walks.

Usage: prior_arms.py OUT.json
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_way import LANE, REVS, load  # noqa: E402


def arm_pages(rev: str) -> dict[str, list[str]]:
    """Arm pages per family, read from the case tables at REV."""
    with tempfile.TemporaryDirectory(prefix="a184.arms.") as d:
        for f in ("gen_toc.py", "gen_toc_cases.py", "gen_toc_closer_cases.py", "gen_toc_guards.py",
                  "gen_toc_container_cases.py"):
            try:
                src = subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:scripts/{f}"], check=True,
                                     capture_output=True, text=True).stdout
            except subprocess.CalledProcessError:
                continue
            (Path(d) / f).write_text(src)
        code = ("import json,sys; sys.path.insert(0, '.'); import gen_toc; "
                "import gen_toc_cases as c, gen_toc_closer_cases as k; fam = {"
                "'walk': c.walk_arms(), 'tag': c.tag_arms(), 'guard': c.guard_arms(), "
                "'heading': c.heading_arms(), 'predecessor': c.predecessor_arms(), "
                "'provenance': c.provenance_arms(), 'refusal': c.refusal_arms(), 'I440': k.closer_arms()}\n"
                "try:\n import gen_toc_container_cases as i; fam['I437'] = i.container_arms()\n"
                "except ImportError: pass\n"
                "print(json.dumps({n: [a[1] for a in arms] for n, arms in fam.items()}))")
        out = subprocess.run([sys.executable, "-B", "-c", code], cwd=d, check=True, capture_output=True, text=True)
        return json.loads(out.stdout)


def main() -> int:
    fams = {"base": arm_pages(REVS["base"]), "a172": arm_pages(REVS["a172"])}
    with tempfile.TemporaryDirectory(prefix="a184.walks.") as tmp:
        walks = {n: load(n, r, Path(tmp)) for n, r in REVS.items()}
        report = {"counts": {k: {f: len(v) for f, v in fam.items()} for k, fam in fams.items()}, "diffs": []}
        pages = {(src, fam, i): p for src, famd in fams.items() for fam, ps in famd.items()
                 for i, p in enumerate(ps)}
        for (src, fam, i), page in pages.items():
            res = {n: (mod.blocks(page), mod.headings(page)) for n, (mod, _) in walks.items()}
            if not (res["base"] == res["a172"] == res["head"]):
                changed = [n for n in ("a172", "head") if res[n] != res["base"]]
                head_vs_a172 = res["head"] != res["a172"]
                report["diffs"].append({"source": src, "family": fam, "index": i, "page": page,
                                        "differs_from_base": changed, "head_differs_from_a172": head_vs_a172})
    report["unique_pages"] = len(set(pages.values()))
    report["head_differs_from_a172"] = [d for d in report["diffs"] if d["head_differs_from_a172"]]
    Path(sys.argv[1]).write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps(report["counts"]), "unique pages", report["unique_pages"])
    by = {}
    for d in report["diffs"]:
        key = (d["source"], d["family"], tuple(d["differs_from_base"]))
        by[key] = by.get(key, 0) + 1
    print("pages differing from the base walk:", by)
    print("pages where head differs from a172:", len(report["head_differs_from_a172"]))
    for d in report["head_differs_from_a172"][:20]:
        print("  ", d["source"], d["family"], repr(d["page"])[:120])
    return 0


if __name__ == "__main__":
    sys.exit(main())
