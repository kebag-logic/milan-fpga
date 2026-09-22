"""R226 probe: dump (family, name, fixture) for every gen_toc arm in a tree."""
import hashlib, json, sys
from pathlib import Path
scripts = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(scripts))
import gen_toc
sys.modules.setdefault("gen_toc", gen_toc)
import gen_toc_cases as cases
fams = {"walk": cases.walk_arms(), "tag": cases.tag_arms(), "guard": cases.guard_arms(),
        "heading": cases.heading_arms(), "predecessor": cases.predecessor_arms(),
        "provenance": cases.provenance_arms(), "refusal": cases.refusal_arms()}
try:
    import gen_toc_closer_cases as closers
    fams["I440"] = closers.closer_arms()
except ImportError:
    pass
rows = []
for fam, arms in fams.items():
    for arm in arms:
        name, text = arm[0], arm[1]
        rows.append({"family": fam, "name": name,
                     "text_sha256": hashlib.sha256(repr(text).encode()).hexdigest()})
json.dump({"counts": {f: len(a) for f, a in fams.items()}, "total": len(rows), "rows": rows},
          sys.stdout, indent=1)
