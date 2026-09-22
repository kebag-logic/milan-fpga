#!/usr/bin/env python3
"""[R238] drive the shipped em-dash gate end to end at base and at head.

For each selected probe, the exact BASE page the fixture commits is also put
to GitHub's renderer (cached with the probes), so the expected verdict is the
renderer's answer on that exact page: no rendered `Old <U+2014> heading` on
the base page means the copied label must be REFUSED (1 finding, 0 exempt);
a rendered one means it must be EXEMPT (0 findings, 1 exempt).
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_render as probes  # noqa: E402

OUT = probes.OUT
SELECT = ("A01", "A04", "A07", "B01", "B03", "C01", "C04", "C05", "C06",
          "C07", "C08", "D01", "D02", "D03", "D04", "P01", "P02")


def main() -> int:
    rows = [{"id": n, "page": t} for n, t in probes.SHAPES
            if n.split(" ", 1)[0] in SELECT]
    shapes = OUT / "receipts" / "e2e-shapes.json"
    shapes.write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    outcome = {}
    for rev in ("base", "head"):
        out = OUT / "receipts" / f"e2e-{rev}.json"
        proc = subprocess.run([sys.executable, "-B",
                               str(OUT / "scripts" / "e2e_gate_worker.py"),
                               str(probes.SCRATCH / f"clone-{rev}" / "scripts"),
                               str(shapes), str(out)], capture_output=True, text=True)
        if proc.returncode:
            print(proc.stdout, proc.stderr)
            return 2
        outcome[rev] = json.loads(out.read_text())
    cache = probes.load_cache()
    # Only the Contents LABEL decision is scored: exempt, or refused with
    # `mirrors no heading`. An `added heading` finding is this fixture's own
    # diff alignment (git pairs the heading line differently per page) and
    # is listed separately, never scored.
    lines = ["id | renderer shows Old on exact base page | expected label | "
             "base gate label | head gate label | other findings base/head"]
    for b, h in zip(outcome["base"], outcome["head"]):
        got = probes.render(b["base_page"], cache)
        shown = [s for _, s in probes.rendered_headings(got["response"])]
        visible = "Old — heading" in shown
        expected = "exempt" if visible else "refused"

        def decision(r):
            refused = sum("mirrors no heading" in f for f in r["findings"])
            if (r["exempt"], refused) == (1, 0):
                got_label = "exempt"
            elif (r["exempt"], refused) == (0, 1):
                got_label = "refused"
            else:
                got_label = f"exempt={r['exempt']},refused={refused}"
            return f"{got_label} {'ok' if got_label == expected else 'WRONG'}"

        def other(r):
            return sum("mirrors no heading" not in f for f in r["findings"])
        lines.append(f"{b['id']} | {visible} | {expected} | {decision(b)} | "
                     f"{decision(h)} | {other(b)}/{other(h)}")
    (OUT / "receipts" / "e2e-table.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
