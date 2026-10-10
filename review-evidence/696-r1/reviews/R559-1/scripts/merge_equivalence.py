#!/usr/bin/env python3
"""PR #706 merge checks: the lane's diff over dev 8b61b709 (at the merge) equals its diff over
base 6aa25dec (at the pre-merge lane head), ignoring only index and hunk-header lines; the merge
needed no conflict resolution (empty remerge diff); gitlinks are unchanged across all four commits;
the two post-merge commits touch only the record and the two docs pages."""
import subprocess, sys
repo = sys.argv[1]
BASE, LANE, DEV, MERGE, REC, HEAD = ("6aa25dec977c6ad78bf4ff6275de47fb81d0c246", "39571196045ddcc881f9ad0957742537175441d6",
    "8b61b70902f3ebf118e56967277e2686731081bd", "0df486370990fddf9b60096be2f2371150692a10",
    "e6f00121a5c6be8a786bd7cbd3411c1d80dd8a73", "030eb98a12685a2ca41cf8d785bb0eb69dc32a98")
g = lambda *a: subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout
ok = True
parents = g("rev-list", "--parents", "-n1", MERGE).split()[1:]
print("merge parents:", parents, "expected", [LANE, DEV]); ok &= parents == [LANE, DEV]
print("base is ancestor of dev:", subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", BASE, DEV]).returncode == 0)
strip = lambda t: [l for l in t.splitlines() if not l.startswith(("index ", "@@"))]
a = g("diff", "--no-ext-diff", "--no-textconv", BASE, LANE); b = g("diff", "--no-ext-diff", "--no-textconv", DEV, MERGE)
fa = sorted(g("diff", "--name-only", BASE, LANE).split()); fb = sorted(g("diff", "--name-only", DEV, MERGE).split())
print("lane files over base:", len(fa), "over dev:", len(fb), "same set:", fa == fb); ok &= fa == fb
eq = strip(a) == strip(b); print("diff bodies equal (index/@@ lines ignored):", eq, len(strip(a)), "lines"); ok &= eq
rm = g("show", "--remerge-diff", "--format=", MERGE).strip(); print("remerge diff empty:", rm == ""); ok &= rm == ""
for c in (BASE, LANE, DEV, MERGE, HEAD):
    print(c[:10], " ".join(l.split()[2][:10] + ":" + l.split()[3] for l in g("ls-tree", c).splitlines() if l.split()[1] == "commit"))
links = {c: [l for l in g("ls-tree", c).splitlines() if l.split()[1] == "commit"] for c in (BASE, LANE, DEV, MERGE, HEAD)}
same = len({tuple(v) for v in links.values()}) == 1; print("gitlinks identical:", same); ok &= same
r = g("diff", "--name-only", MERGE, REC).split(); d = g("diff", "--name-only", REC, HEAD).split()
print("record commit files:", r); ok &= r == ["syn/ooc/pp_resource_baseline.json"]
print("docs commit files:", d); ok &= sorted(d) == ["docs/design/AREA_BUDGET.md", "docs/findings/234_PP_SHADOW_AREA_BASELINE.md"]
print("HEAD parent chain:", g("rev-list", "--parents", "-n1", HEAD).split()[1:], g("rev-list", "--parents", "-n1", REC).split()[1:])
print("RESULT:", "PASS" if ok else "FAIL"); raise SystemExit(0 if ok else 1)
