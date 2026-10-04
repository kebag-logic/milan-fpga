#!/usr/bin/env python3
"""Check that each armq_* control in tb/pp_top/acmp_mutants.py plants a top byte-identical
to the one R462-1's lockstep_armq/gen.py control of the same defect plants.

usage: edit_identity.py TREE GEN_PY
TREE is an exported tree holding hdl/top/protocol_processor_top.sv and tb/pp_top/acmp_mutants.py.
Prints one line per pair with both digests; exits 1 on any difference or refused edit.
"""
import hashlib
import importlib.util
import sys
from pathlib import Path

PAIRS = {
    "armq_read_tail": "read_tail",
    "armq_head_stuck": "head_stuck",
    "armq_ring_of_three": "ring_of_three",
    "armq_write_at_head": "wr_at_head",
    "armq_write_at_mid": "wr_at_mid",
    "armq_write_refused": "write_refused",
    "armq_write_wrap_hi": "wr_wrap_hi",
    "armq_full_pop_refuses": "full_pop_refuses",
    "armq_drop_skip_sat": "drop_skip_sat",
}


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    tree, gen_py = Path(sys.argv[1]), Path(sys.argv[2])
    top_rel = "hdl/top/protocol_processor_top.sv"
    top = (tree / top_rel).read_text()
    am = load("acmp_mutants", tree / "tb/pp_top/acmp_mutants.py")
    gen = load("gen", gen_py)
    by_name = {m.name: m for m in am.MUTANTS if m.name.startswith("armq_")}
    bad = 0
    if sorted(by_name) != sorted(PAIRS):
        print(f"armq_ arms in acmp_mutants.py: {sorted(by_name)}")
        bad += 1
    for arm, ctl in PAIRS.items():
        m = by_name[arm]
        a = top
        for path, old, new in m.edits:
            assert path.endswith(top_rel), (arm, path)
            assert a.count(old) == 1, (arm, a.count(old))
            a = a.replace(old, new, 1)
        old, new = gen.MUTANTS[ctl]
        assert top.count(old) == 1, (ctl, top.count(old))
        b = top.replace(old, new, 1)
        da, db = hashlib.sha256(a.encode()).hexdigest(), hashlib.sha256(b.encode()).hexdigest()
        same = da == db and a != top
        bad += 0 if same else 1
        print(f"{arm:24s} {ctl:18s} {'IDENTICAL' if same else 'DIFFERENT'} {da[:16]} {db[:16]} "
              f"checks={list(m.checks)}")
    print(f"{len(PAIRS) - bad if bad <= len(PAIRS) else 0} of {len(PAIRS)} identical")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
