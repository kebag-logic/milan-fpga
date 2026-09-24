"""AC4: classify every tracked page under the base walk and the new walk; enumerate differences."""
import importlib.util, json, subprocess, sys
from pathlib import Path
repo = Path(sys.argv[1]); base_scripts = Path(sys.argv[2]); tree = Path(sys.argv[3]) if len(sys.argv) > 3 else repo
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
sys.path.insert(0, str(repo / "scripts"))
new = load("gen_toc_new", repo / "scripts/gen_toc.py")
old = load("gen_toc_old", base_scripts / "gen_toc.py")
out = subprocess.run(["git", "-C", str(tree), "ls-files", "-z", "*.md"], capture_output=True, text=True, check=True).stdout
pages = sorted(p for p in out.split("\0") if p and (tree / p).is_file())
report, fields_diff = {}, {}
for p in pages:
    text = (tree / p).read_text()
    diffs = {}
    for field, fn in (("refusals", lambda m: m.refusals(text)), ("blocks", lambda m: m.blocks(text)),
                      ("line_kinds", lambda m: m.line_kinds(text)), ("headings", lambda m: m.headings(text)),
                      ("plan", lambda m: m.plan(text)), ("existing", lambda m: m.existing(text)),
                      ("owns", lambda m: m.owns(p, text)), ("generated_block", lambda m: m.generated_block(text, p))):
        a, b = fn(old), fn(new)
        if a != b:
            if field in ("blocks", "line_kinds"):
                rows = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
                diffs[field] = rows
            elif field == "headings":
                diffs[field] = {"old_only": [h for h in a if h not in b], "new_only": [h for h in b if h not in a]}
            else:
                diffs[field] = {"old": a, "new": b}
            fields_diff[field] = fields_diff.get(field, 0) + 1
    if diffs:
        report[p] = diffs
print(json.dumps({"pages": len(pages), "differing_pages": len(report), "fields": fields_diff}, indent=1))
for p, d in report.items():
    print("==", p)
    for f, v in d.items():
        if f in ("blocks", "line_kinds"):
            lines = (tree / p).read_text().split("\n")
            print(f"  {f}: {len(v)} line(s):", ", ".join(f"{i}:{x}->{y}" for i, x, y in v[:6]), "..." if len(v) > 6 else "")
        else:
            print(f"  {f}:", json.dumps(v, ensure_ascii=False)[:600])
if len(sys.argv) > 4:
    Path(sys.argv[4]).write_text(json.dumps(report, indent=1, ensure_ascii=False))
