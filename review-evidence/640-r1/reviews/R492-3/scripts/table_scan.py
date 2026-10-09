"""Render a Markdown page at a git revision with the pinned cmark-gfm and
report every table: its source line, header, body-row count and first-cell
texts of the last body row, plus every source table line that is directly
followed by a non-blank, non-pipe line (a prose line GFM folds into the
table; an HTML comment line starts its own block and is not folded). Usage: python3 -I table_scan.py <repo> <rev> <path> [<path>...]"""
import subprocess
import sys

import cmarkgfm
import html5lib
from cmarkgfm.cmark import Options


def scan(repo, rev, path):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout
    lines = text.split("\n")
    folded = []
    in_fence = False
    for i, line in enumerate(lines[:-1]):
        if line.startswith("```"):
            in_fence = not in_fence
        if in_fence:
            continue
        nxt = lines[i + 1]
        if line.startswith("|") and nxt.strip() and not nxt.startswith("|") \
                and not nxt.startswith("```") and not nxt.startswith("<!--"):
            folded.append((i + 1, nxt))
    html = cmarkgfm.github_flavored_markdown_to_html(
        text, options=Options.CMARK_OPT_SOURCEPOS | Options.CMARK_OPT_UNSAFE)
    doc = html5lib.parse(html, namespaceHTMLElements=False)
    tables = doc.findall(".//table")
    print(f"{rev[:12]} {path}: {len(tables)} rendered table(s), "
          f"{len(folded)} source table line(s) followed by unseparated prose")
    for line_no, nxt in folded:
        print(f"  FOLDED after line {line_no}: {nxt!r}")
    for t in tables:
        pos = t.get("data-sourcepos", "?")
        head = [("".join(c.itertext())).strip() for c in t.findall("./thead/tr/th")]
        rows = t.findall("./tbody/tr")
        last = [("".join(c.itertext())).strip() for c in rows[-1]] if rows else []
        print(f"  table @{pos} cols={len(head)} body_rows={len(rows)} "
              f"head={head[:2]} last_row_first_cell={last[:1]}")
    # Paragraph check for the M3 basis prose.
    paras = ["".join(p.itertext()).strip() for p in doc.findall(".//p")]
    hit = [p for p in paras if p.startswith("That displaces about 3,380 LUTs.")]
    print(f"  paragraph_starting_'That displaces about 3,380 LUTs.'={len(hit)}")
    return len(folded)


def main():
    repo, rev, paths = sys.argv[1], sys.argv[2], sys.argv[3:]
    total = sum(scan(repo, rev, p) for p in paths)
    print(f"TOTAL folded={total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
