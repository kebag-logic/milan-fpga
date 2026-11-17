"""Render CONTRIBUTING.md with the pinned cmark-gfm, list heading ids GitHub would give, check the
same-page and cross-page #23-batched-merges links, and extract every mermaid block to files.
usage: anchor_and_mermaid.py <repo> <outdir>"""
import re, sys, pathlib, unicodedata
repo, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
def slug(h):  # GitHub heading anchor rule: lowercase, drop punctuation except - and _, spaces to -
    h = re.sub(r"<[^>]+>", "", h).strip().lower()
    return re.sub(r"\s", "-", "".join(c for c in h if c.isalnum() or c in " -_"))
src = (repo / "CONTRIBUTING.md").read_text()
heads = [slug(m.group(2)) for m in re.finditer(r"^(#{1,6})\s+(.*)$", src, re.M)]
print("CONTRIBUTING heading slug 23-batched-merges present:", "23-batched-merges" in heads, "count", heads.count("23-batched-merges"))
import cmarkgfm
html = cmarkgfm.github_flavored_markdown_to_html(src)
print("rendered heading text '2.3 Batched merges' present:", ">2.3 Batched merges<" in html)
for f in ["CONTRIBUTING.md", "AGENTS.md", "docs/testing/CI_WORKFLOWS.md"]:
    t = (repo / f).read_text()
    for m in re.finditer(r"\]\(([^)]*#23-batched-merges)\)", t):
        line = t[:m.start()].count("\n") + 1
        target = m.group(1).split("#")[0]
        resolved = (repo / f).parent.joinpath(target).resolve() if target else (repo / f).resolve()
        print(f"{f}:{line} -> {m.group(1)} : file {'OK' if resolved == (repo/'CONTRIBUTING.md').resolve() else 'WRONG '+str(resolved)}")
n = 0
for m in re.finditer(r"^```mermaid\n(.*?)^```", src, re.M | re.S):
    n += 1; (out / f"contributing-mermaid-{n}.mmd").write_text(m.group(1))
    print(f"mermaid block {n} at line {src[:m.start()].count(chr(10))+1}, {m.group(1).count(chr(10))} lines")
