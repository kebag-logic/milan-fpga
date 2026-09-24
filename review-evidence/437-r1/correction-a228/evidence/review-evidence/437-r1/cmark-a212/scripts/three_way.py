"""Base walk vs renderer walk vs GitHub, over recorded pages (rendered.json style)."""
import importlib.util, json, sys
from pathlib import Path
repo, base, data = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(repo / "scripts"))
import gen_toc as new, gen_toc_renderer as r
spec = importlib.util.spec_from_file_location("gen_toc_base", base / "gen_toc.py"); old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
def norm(level, text): return (level, " ".join(old.strip_md(text).split()))
rows = json.loads(data.read_text())
stats = {"agree_both": 0, "fixed": 0, "regressed": 0, "wrong_both": 0}
detail = []
for s in rows:
    gh = r.headings_of(s["response_bytes"])
    gh_n = [norm(l, t) for l, t in gh if not (l == 2 and t == "Footnotes" and 'sr-only' in s["response_bytes"])]
    base_h = [norm(l, raw) for l, raw, _ in old.headings(s["page"])]
    new_h = [norm(l, t) for l, t in new.rendered_headings(s["page"])]
    b_ok, n_ok = base_h == gh_n, new_h == gh_n
    k = "agree_both" if b_ok and n_ok else "fixed" if n_ok else "regressed" if b_ok else "wrong_both"
    stats[k] += 1
    if k != "agree_both":
        detail.append({"class": k, "set": s.get("set"), "name": s.get("name"), "page": s["page"], "github": gh_n, "base": base_h, "new": new_h})
print(json.dumps(stats))
for d in detail:
    if d["class"] in ("regressed", "wrong_both"):
        print(d["class"], d["set"], d["name"], repr(d["page"])[:120], d["github"], d["base"], d["new"])
if len(sys.argv) > 4:
    Path(sys.argv[4]).write_text(json.dumps({"stats": stats, "detail": detail}, indent=1, ensure_ascii=False))
