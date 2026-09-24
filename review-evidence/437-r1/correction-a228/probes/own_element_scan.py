"""For each _OWN_ELEMENT kind, the pages whose block labels or line kinds
change when that kind is dropped.  Usage: own_element_scan.py <repo> <pages.json>..."""
import json, subprocess, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "scripts"))
import gen_toc as g, gen_toc_renderer as r
pages = []
for f in sys.argv[2:]:
    d = json.load(open(f))
    rows = d["shapes"] if isinstance(d, dict) else d
    pages += [(f"{Path(f).name}:{x.get('name', i) if isinstance(x, dict) else i}", x["page"] if isinstance(x, dict) else x) for i, x in enumerate(rows)]
tracked = subprocess.run(["git", "-C", str(repo), "ls-files", "*.md"], capture_output=True, text=True).stdout.split()
pages += [(p, (repo / p).read_text()) for p in tracked if (repo / p).is_file()]
extra = {"partial list": "<span>\n<!--\n\n- a\n- b <!-- x -->\n- c\n",
         "partial quote": "<span>\n<!--\n\n> a <!-- x -->\n>\n> b\n"}
pages += list(extra.items())
full = r._OWN_ELEMENT
def answer(page):
    g._page.cache_clear()
    return g.blocks(page), g.line_kinds(page)
base = {name: answer(page) for name, page in pages}
for drop in full:
    r._OWN_ELEMENT = tuple(k for k in full if k != drop)
    changed = [name for name, page in pages if answer(page) != base[name]]
    print(f"drop {drop:15}: {len(changed)} of {len(pages)} pages change", changed[:6])
r._OWN_ELEMENT = full
