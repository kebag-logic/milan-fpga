"""R226: every tracked Markdown page, classified by the base and head engines.

Usage: python3 -B r226_pages.py BASE_CLONE HEAD_CLONE OUT.json

For each population (the tracked *.md of the base tree and of the head tree),
each engine (base scripts, head scripts) computes blocks(), line_kinds(),
headings(), refusals(), owns() and generated_block() on the text the shipped
generator reads (Path.read_text). Engines run in separate processes.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

WORKER = r'''
import hashlib, json, subprocess, sys
from pathlib import Path
scripts, tree = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(scripts))
import gen_toc as g
files = subprocess.run(["git", "-C", str(tree), "ls-files", "-z", "*.md"], capture_output=True,
                       text=True, check=True).stdout.split("\0")
out = {}
for rel in sorted(f for f in files if f):
    p = tree / rel
    text = p.read_text()
    raw = p.read_bytes()
    rec = {"blocks": g.blocks(text), "kinds": g.line_kinds(text), "headings": g.headings(text),
           "refusals": g.refusals(text), "owns": g.owns(rel, text),
           "generated_block": g.generated_block(text, rel), "has_cr_bytes": b"\r" in raw}
    out[rel] = hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=True).encode()).hexdigest()
    out[rel + "#detail"] = {"n_headings": len(rec["headings"]), "provenance": rec["generated_block"] is not None,
                            "refused": bool(rec["refusals"]), "owns": rec["owns"], "cr": rec["has_cr_bytes"],
                            "html_lines": rec["blocks"].count(g.HTML), "fence_lines": rec["blocks"].count(g.FENCE)}
json.dump(out, sys.stdout)
'''


def run(scripts: Path, tree: Path) -> dict:
    res = subprocess.run([sys.executable, "-B", "-c", WORKER, str(scripts), str(tree)],
                         capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def main() -> None:
    base, head, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    result = {}
    for pop_name, pop in (("base-pages", base), ("head-pages", head)):
        for eng_name, eng in (("base-engine", base / "scripts"), ("head-engine", head / "scripts")):
            result[f"{pop_name}/{eng_name}"] = run(eng, pop)
    summary = {}
    for pop in ("base-pages", "head-pages"):
        b, h = result[f"{pop}/base-engine"], result[f"{pop}/head-engine"]
        pages = [k for k in b if not k.endswith("#detail")]
        diff = [k for k in pages if b[k] != h.get(k)]
        det = [b[k + "#detail"] for k in pages]
        summary[pop] = {"pages": len(pages), "engine_disagreements": diff,
                        "provenance_pages": sum(d["provenance"] for d in det),
                        "refused_pages": [k for k in pages if b[k + "#detail"]["refused"]],
                        "cr_pages": [k for k in pages if b[k + "#detail"]["cr"]],
                        "pages_with_html_lines": sum(1 for d in det if d["html_lines"]),
                        "pages_with_fence_lines": sum(1 for d in det if d["fence_lines"]),
                        "owned_pages": sum(d["owns"] for d in det)}
    bp = result["base-pages/head-engine"]
    hp = result["head-pages/head-engine"]
    summary["pages_whose_head_engine_record_differs_between_populations"] = sorted(
        k for k in set(bp) | set(hp) if not k.endswith("#detail") and bp.get(k) != hp.get(k))
    out.write_text(json.dumps({"summary": summary, "records": result}, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
