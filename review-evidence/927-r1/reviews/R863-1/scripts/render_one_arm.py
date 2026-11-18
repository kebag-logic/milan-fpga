#!/usr/bin/env python3
"""Run named arms of tb/verilator/milan_dp_render/tdm8_render_mutants.py only,
in the given tree, through the campaign's own run_mutations (its build recipe,
its legs, its verdict). The clean legs must already be built in the tree
(make tdm8render-build tdm8render-multi-build). Prints every [FAIL] line each
mutated leg emitted, so the checks that caught it are visible.

usage: render_one_arm.py <tree-root> <arm name>...
"""
import sys
import tempfile
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1])
    names = sys.argv[2:]
    here = root / "tb/verilator/milan_dp_render"
    sys.path.insert(0, str(here))
    import tdm8_render_mutants as m  # noqa: E402  (the tree's own campaign)
    m.MUTATIONS = [a for a in m.MUTATIONS if a[0] in names]
    if len(m.MUTATIONS) != len(names):
        print("FIXTURE: arms not found:", names, [a[0] for a in m.MUTATIONS])
        return 2
    real = m.run_leg

    def run_leg(exe, mode):
        rc, out = real(exe, mode)
        fails = [ln for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
        print(f"leg rc {rc}; {len(fails)} [FAIL] line(s):", flush=True)
        for ln in fails[:20]:
            print("   ", ln[:300], flush=True)
        return rc, out

    m.run_leg = run_leg
    with tempfile.TemporaryDirectory(prefix="r863-one-arm-") as td:
        p, f = m.run_mutations(Path(td))
    print(f"arms: {p} caught, {f} not caught", flush=True)
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
