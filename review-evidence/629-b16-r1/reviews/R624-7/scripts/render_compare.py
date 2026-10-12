#!/usr/bin/env python3
"""R624-7: render the findings page at two commits with the pinned renderer (GitHub options) and compare the
visible text of every block before lane B16's round 7 subsection, HTML comments removed from the older render.
usage: <renderer python> -I render_compare.py <old page> <new page> <out.json>"""
import json, re, sys
import cmarkgfm, html5lib
from cmarkgfm.cmark import Options
old, new, out = sys.argv[1:4]
def blocks(path):
    t = open(path, encoding="utf-8").read()
    t = t[:t.index("### B16, round 7: no markup")] if "### B16, round 7: no markup" in t else t
    h = cmarkgfm.github_flavored_markdown_to_html(t, options=Options.CMARK_OPT_UNSAFE)
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    return [b for b in re.split(r"\n+", h) if b.strip()]
a, b = blocks(old), blocks(new)
diff = [(i, x[:200], y[:200]) for i, (x, y) in enumerate(zip(a, b)) if x != y]
res = dict(old_blocks=len(a), new_blocks=len(b), differing=len(diff), first=diff[:12])
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(dict(old_blocks=len(a), new_blocks=len(b), differing=len(diff))))
for d in diff[:12]:
    print(d[0], "\n  OLD", d[1], "\n  NEW", d[2])
