#!/usr/bin/env python3
"""Resolve every relative link (and anchor) in the lines a commit range adds
under docs/findings. Anchors are GitHub-style slugs of the headings the
pinned cmark-gfm renders. usage: anchor_check.py <repo> <old> <new>"""
import html, re, subprocess, sys
from pathlib import Path
import cmarkgfm
repo, old, new = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
diff = subprocess.run(['git', '-C', str(repo), 'diff', '-U0', f'{old}..{new}', '--', 'docs/findings'],
                      capture_output=True, text=True, check=True).stdout
def slugs(path):
    h = cmarkgfm.github_flavored_markdown_to_html(path.read_text(), options=cmarkgfm.Options.CMARK_OPT_UNSAFE)
    out, seen = set(), {}
    for m in re.finditer(r'<h[1-6][^>]*>(.*?)</h[1-6]>', h, re.S):
        t = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip().lower()
        s = re.sub(r'[^\w\- ]', '', t).replace(' ', '-')
        k = seen.get(s, 0); seen[s] = k + 1
        out.add(s if k == 0 else f'{s}-{k}')
    return out
cur, bad, n = None, 0, 0
for line in diff.splitlines():
    if line.startswith('+++ b/'): cur = Path(line[6:]); continue
    if not line.startswith('+') or line.startswith('+++'): continue
    for tgt in re.findall(r'\]\(([^)\s]+)\)', line):
        if re.match(r'https?:', tgt): continue
        n += 1
        f, _, anc = tgt.partition('#')
        p = (repo / cur.parent / f).resolve() if f else (repo / cur)
        ok = p.exists() and (not anc or anc in slugs(p))
        bad += not ok
        print(f'{cur}: {tgt} -> {"OK" if ok else "BROKEN"}')
print(f'{n} relative links, {bad} broken'); sys.exit(1 if bad else 0)
