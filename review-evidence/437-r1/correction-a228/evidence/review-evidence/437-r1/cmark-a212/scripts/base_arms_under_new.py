"""Score every base-era arm (dev 759da623 tables) with the new walk; list those it answers differently."""
import importlib.util, json, sys, types
from pathlib import Path
repo, base = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "scripts"))
import gen_toc as new
# Load the base tables against the NEW walk: they import names from `gen_toc`.
# Constants the base tables import that the new walk deleted are supplied from the base module.
spec = importlib.util.spec_from_file_location("gen_toc_base", base / "gen_toc.py"); old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
shim = types.ModuleType("gen_toc")
for k in dir(old): setattr(shim, k, getattr(old, k))
for k in ("blocks", "headings", "line_kinds", "generated_block", "existing", "plan", "refusals", "refusal_notes", "TEXT", "FENCE", "COMMENT", "CODE", "HTML"):
    setattr(shim, k, getattr(new, k))
sys.modules["gen_toc"] = shim
sys.path.insert(0, str(base))
for m in ("gen_toc_cases", "gen_toc_closer_cases", "gen_toc_guards"):
    sys.modules.pop(m, None)
cases = importlib.util.module_from_spec(importlib.util.spec_from_file_location("gen_toc_cases", base / "gen_toc_cases.py"))
sys.modules["gen_toc_guards"] = importlib.util.module_from_spec(importlib.util.spec_from_file_location("gen_toc_guards", base / "gen_toc_guards.py"))
sys.modules["gen_toc_guards"].__spec__.loader.exec_module(sys.modules["gen_toc_guards"])
cases.__spec__.loader.exec_module(cases)
closers = importlib.util.module_from_spec(importlib.util.spec_from_file_location("gen_toc_closer_cases", base / "gen_toc_closer_cases.py")); closers.__spec__.loader.exec_module(closers)
fams = {"walk": cases.walk_arms(), "tag": cases.tag_arms(), "heading": cases.heading_arms(), "predecessor": cases.predecessor_arms(),
        "provenance": cases.provenance_arms(), "refusal": cases.refusal_arms(), "I440": closers.closer_arms()}
changed, total = [], 0
for fam, arms in fams.items():
    for name, page, holds in arms:
        total += 1
        ok = holds(new.blocks(page)) if fam in ("walk", "tag", "I440") else holds(page)
        if not ok:
            changed.append({"family": fam, "name": name, "page": page})
print(total, "base-era page arms;", len(changed), "answered differently by the renderer")
fixture = {s["page"] for s in json.loads((repo / "scripts/gen_toc_shapes.json").read_text())["shapes"]}
missing = [c for c in changed if c["page"] not in fixture]
print("pages missing from the fixture:", len(missing))
json.dump(changed, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
from collections import Counter; print(Counter(c["family"] for c in changed))
