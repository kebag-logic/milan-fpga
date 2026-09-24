#!/usr/bin/env python3
"""Base walk vs head walk over every tracked Markdown page (acceptance 4).

Usage: compare_tree.py <repo> <base-rev> <out.json> [<tree-rev>]
With <tree-rev>, the pages are read from that revision (git ls-tree/git
show) instead of the working tree.
Loads gen_toc.py from <base-rev> (git show, temp dir) and from the checkout,
and for every `git ls-files '*.md'` page at the checkout records: owns(),
refusals, blocks(), line_kinds(), headings(), plan(), existing() span and
separator, and generated_block(). Prints every page on which any differs.
"""
import importlib.util, json, subprocess, sys, tempfile
from pathlib import Path

repo, base_rev, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
tree_rev = sys.argv[4] if len(sys.argv) > 4 else None
sys.path.insert(0, str(repo / "scripts"))
import gen_toc as head  # noqa: E402
tmp = Path(tempfile.mkdtemp(prefix="basewalk."))
(tmp / "gen_toc.py").write_bytes(subprocess.run(
    ["git", "-C", str(repo), "show", f"{base_rev}:scripts/gen_toc.py"],
    capture_output=True, check=True).stdout)
spec = importlib.util.spec_from_file_location("gen_toc_base", tmp / "gen_toc.py")
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)

def view(m, rel, text):
    ex = m.existing(text)
    gb = m.generated_block(text, rel)
    return {"owns": m.owns(rel, text), "refusals": m.refusals(text),
            "blocks": m.blocks(text), "line_kinds": m.line_kinds(text),
            "headings": [list(h) for h in m.headings(text)],
            "plan": None if m.plan(text) is None else [list(h) for h in m.plan(text)],
            "existing_span": [ex[1], ex[2], ex[3]],
            "generated_block": None if gb is None else [gb[0], gb[1]]}

if tree_rev:
    files = [f for f in subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "-z", "--name-only", tree_rev],
             capture_output=True, text=True, check=True).stdout.split("\0") if f.endswith(".md")]
else:
    files = subprocess.run(["git", "-C", str(repo), "ls-files", "-z", "*.md"],
                           capture_output=True, text=True, check=True).stdout.split("\0")
report, summary = [], {"pages": 0, "any_diff": 0}
for rel in sorted(f for f in files if f):
    if tree_rev:
        text = subprocess.run(["git", "-C", str(repo), "show", f"{tree_rev}:{rel}"],
                              capture_output=True, check=True).stdout.decode("utf-8")
    else:
        p = repo / rel
        if not p.is_file():
            continue
        text = p.read_text()
    summary["pages"] += 1
    b, h = view(base, rel, text), view(head, rel, text)
    diffs = sorted(k for k in b if b[k] != h[k])
    if diffs:
        summary["any_diff"] += 1
        for k in diffs:
            summary[k] = summary.get(k, 0) + 1
        entry = {"page": rel, "fields": diffs}
        if "blocks" in diffs or "line_kinds" in diffs:
            entry["lines"] = [[i + 1, b["line_kinds"][i], h["line_kinds"][i], text.split("\n")[i][:100]]
                              for i in range(len(b["line_kinds"])) if b["line_kinds"][i] != h["line_kinds"][i]
                              or b["blocks"][i] != h["blocks"][i]]
        if "headings" in diffs:
            entry["headings_base"], entry["headings_head"] = b["headings"], h["headings"]
        for k in ("plan", "existing_span", "generated_block", "owns", "refusals"):
            if k in diffs:
                entry[k] = {"base": b[k], "head": h[k]}
        report.append(entry)
out.write_text(json.dumps({"summary": summary, "pages": report}, indent=1))
print(json.dumps(summary))
for e in report:
    print("==", e["page"], e["fields"])
    for ln in e.get("lines", [])[:12]:
        print("   line", ln)
    if len(e.get("lines", [])) > 12:
        print("   ...", len(e["lines"]), "lines")
    if "headings" in e["fields"]:
        bs = {tuple(x) for x in e["headings_base"]}; hs = {tuple(x) for x in e["headings_head"]}
        print("   headings added:", sorted(hs - bs), "removed:", sorted(bs - hs))
