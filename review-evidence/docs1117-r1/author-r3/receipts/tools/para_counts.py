"""Word count of every prose block (paragraph or whole list item, with its
continuation lines) that contains a line added since <base>.  Words are
counted with check_doc_style's own normalisation and WORD expression.
usage: <repo> <base> <limit> <page>...   exit 1 if any block exceeds <limit>"""
import re, subprocess, sys
from pathlib import Path
repo, base, limit, pages = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4:]
sys.path.insert(0, str(repo / "scripts"))
import check_doc_style as c
LIST = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s+")
over = 0
for p in pages:
    d = subprocess.run(["git", "-C", str(repo), "diff", "-U0", base, "--", p], capture_output=True, text=True, check=True).stdout
    added = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", d, re.M):
        s, n = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
        added |= set(range(s, s + n))
    blocks, cur, fenced = [], None, False
    for no, raw in enumerate((repo / p).read_text().splitlines(), 1):
        st = raw.strip()
        if st.startswith(("```", "~~~")):
            fenced = not fenced; cur = None; continue
        if fenced or not st or st.startswith(("#", "|", ">", "<!--")):
            cur = None; continue
        if LIST.match(raw) or cur is None:
            cur = [no, [LIST.sub("", raw).strip()], "item" if LIST.match(raw) else "para"]
            blocks.append(cur)
        else:
            cur[1].append(st)
    print(f"## {p}")
    for start, lines, kind in blocks:
        span = set(range(start, start + len(lines)))
        if not span & added:
            continue
        words = len(c.WORD.findall(c.normalized_prose(" ".join(lines))))
        flag = "OVER" if words > limit else "ok"
        over += words > limit
        print(f"{p}:{start}-{start+len(lines)-1} {kind} {words} words {flag} :: {' '.join(lines)[:70]}")
print(f"blocks over {limit} words: {over}")
sys.exit(1 if over else 0)
