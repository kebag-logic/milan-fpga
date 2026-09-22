#!/usr/bin/env python3
"""[R238] the five documented withholding forms, end to end through the gate.

Each base page carries the em-dash heading in one of the five forms the head
documents as omitted; the head page shows it as an ATX heading with the
generated Contents block. CONTRIBUTING 6.1 (head) says their copied labels
receive no exemption, and GitHub renders every one as a heading: the
documented answer is `refused` where the renderer alone would say `exempt`.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_render as probes  # noqa: E402

EM = "—"
ROWS = [("G01 equals setext", f"Old {EM} heading\n===\n"),
        ("G02 hyphen setext", f"Old {EM} heading\n---\n"),
        ("G03 single hyphen setext", f"Old {EM} heading\n-\n"),
        ("G04 quoted heading", "> ## Old\n"),
        ("G05 list heading", "- item\n\n  ## Old\n")]


def main() -> int:
    shapes = probes.OUT / "receipts" / "e2e-family-two-shapes.json"
    shapes.write_text(json.dumps([{"id": i, "page": p} for i, p in ROWS], ensure_ascii=False))
    out = probes.OUT / "receipts" / "e2e-family-two-head.json"
    subprocess.run([sys.executable, "-B", str(probes.OUT / "scripts" / "e2e_gate_worker.py"),
                    str(probes.SCRATCH / "clone-head" / "scripts"), str(shapes), str(out)],
                   check=True)
    cache = probes.load_cache()
    lines = ["id | GitHub renders the base heading | head gate label decision"]
    for r in json.loads(out.read_text()):
        shown = [s for _, s in probes.rendered_headings(
            probes.render(r["base_page"], cache)["response"])]
        refused = sum("mirrors no heading" in f for f in r["findings"])
        decision = "exempt" if (r["exempt"], refused) == (1, 0) else \
            "refused" if (r["exempt"], refused) == (0, 1) else f"{r['exempt']}/{refused}"
        lines.append(f"{r['id']} | {f'Old {EM} heading' in shown} | {decision}")
    (probes.OUT / "receipts" / "e2e-family-two.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
