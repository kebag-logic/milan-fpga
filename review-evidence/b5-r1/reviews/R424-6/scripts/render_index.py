"""Render docs/findings/README.md at three revisions with the pinned cmark-gfm
lock and report the index table's body-row count, each row's link target, and
whether the target exists in that revision's tree. Usage:
  render_index.py <repo> <rev>...
"""
import subprocess, sys, html5lib, cmarkgfm
from cmarkgfm.cmark import Options
repo, revs = sys.argv[1], sys.argv[2:]
def git(*a): return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout
for rev in revs:
    src = git("show", f"{rev}:docs/findings/README.md")
    doc = html5lib.parse(cmarkgfm.github_flavored_markdown_to_html(src, options=Options.CMARK_OPT_UNSAFE), namespaceHTMLElements=False)
    tables = doc.findall(".//table")
    rows = tables[0].findall("./tbody/tr") if tables else []
    tree = set(git("ls-tree", "-r", "--name-only", rev, "docs").split())
    print(f"== {rev} tables={len(tables)} body_rows={len(rows)}")
    targets = []
    for tr in rows:
        cells = tr.findall("./td")
        a = cells[0].find(".//a")
        href = a.get("href") if a is not None else None
        path = None
        if href and not href.startswith("http"):
            import posixpath
            path = posixpath.normpath(posixpath.join("docs/findings", href.split("#")[0]))
        ok = path in tree if path else None
        targets.append(href)
        print(f"  cells={len(cells)} href={href} exists={ok}")
    dup = {t for t in targets if targets.count(t) > 1}
    print(f"  duplicate_targets={sorted(dup)}")
