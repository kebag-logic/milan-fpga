#!/usr/bin/env python3
"""Run the builder bank's own run list in time-boxed sequential chunks.

The bank (sw/builder/test_builder.py) outlasts one foreground call here, so
this driver reads the bank's `for fn in (...)` run list from the file itself
(AST, never a copied list), runs gates from index START in order until the
time budget is spent, and records per-gate timing, the SKIPPED ledger rows
added and the index to resume from. Aggregation across chunks yields the
bank's verdict line.

Usage: bank_chunks.py <tree> <start> <budget-seconds> <state.json> [bank flags...]
BANK_REVIEWER_SKIP=name,name records those gates as REVIEWER NOT RUN (a gate
that alone outlasts one foreground call) instead of running them.
Exit 0 if every gate run in this chunk passed; 1 on the first failure.
"""
from __future__ import annotations

import ast
import json
import os
import sys
import time
import traceback
from pathlib import Path


def run_list(bank: Path) -> list[str]:
    tree = ast.parse(bank.read_text())
    main = [n for n in tree.body if isinstance(n, ast.If)
            and isinstance(n.test, ast.Compare) and getattr(n.test.left, "id", "") == "__name__"]
    loops = [n for n in ast.walk(main[-1]) if isinstance(n, ast.For)
             and isinstance(n.target, ast.Name) and n.target.id == "fn"]
    assert len(loops) == 1
    return [e.id for e in loops[0].iter.elts]


def main() -> int:
    tree, start, budget, state = Path(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), Path(sys.argv[4])
    flags = sys.argv[5:]
    bank = tree / "sw/builder/test_builder.py"
    names = run_list(bank)
    sys.argv = [str(bank), *flags]
    sys.path.insert(0, str(tree / "sw/builder"))
    import test_builder as tb  # noqa: E402
    from test_declarations import test_declaration_contracts  # noqa: E402
    import test_clock_contract as tcc  # noqa: E402
    extra = dict(test_declaration_contracts=test_declaration_contracts)
    for n in ("test_baremetal_clock_contract", "test_builder_clock_source", "test_extra_sweep_clocks",
              "test_extra_sweep_invocation", "test_sim_clock", "test_tap_clock_docs"):
        extra[n] = getattr(tcc, n)
    t0 = time.time()
    record = json.loads(state.read_text()) if state.exists() else dict(gates=[], skipped=[], total=len(names))
    i = start
    rc = 0
    while i < len(names):
        if time.time() - t0 > budget and i > start:
            break
        name = names[i]
        if name in os.environ.get("BANK_REVIEWER_SKIP", "").split(","):
            print(f"{name}: REVIEWER NOT RUN (outlasts one foreground call)", flush=True)
            record["gates"].append(dict(index=i, name=name, ok=None, seconds=0))
            i += 1
            record["next"] = i
            state.write_text(json.dumps(record, indent=1))
            continue
        fn = getattr(tb, name, None) or extra[name]
        before = len(tb.SKIPPED)
        g0 = time.time()
        print(f"{name}:", flush=True)
        try:
            fn()
            ok = True
        except BaseException:  # noqa: BLE001 - a gate failure ends the chunk
            traceback.print_exc()
            ok = False
        sys.stdout.flush()
        record["gates"].append(dict(index=i, name=name, ok=ok, seconds=round(time.time() - g0, 1)))
        record["skipped"] += [list(s) for s in tb.SKIPPED[before:]]
        i += 1
        record["next"] = i
        state.write_text(json.dumps(record, indent=1))
        if not ok:
            rc = 1
            break
    record["next"] = i
    state.write_text(json.dumps(record, indent=1))
    print(f"CHUNK start={start} next={i} of {len(names)} rc={rc} elapsed={time.time() - t0:.0f}s", flush=True)
    if i >= len(names) and rc == 0:
        failed = [g for g in record["gates"] if g["ok"] is False]
        reviewer_skipped = [g["name"] for g in record["gates"] if g["ok"] is None]
        ran = sorted({g["index"] for g in record["gates"]})
        assert ran == list(range(len(names))), "not every gate ran exactly once"
        sk = record["skipped"]
        if failed:
            print(f"FAILED GATES: {failed}")
            return 1
        if sk:
            print(f"\n{len(sk)} GATE ARM(S) DID NOT RUN - this verdict does not cover them:")
            for gate, why, _kind in sk:
                print(f"  - [{gate}] {why}")
            print(f"ALL GATES PASS EXCEPT {len(sk)} NOT RUN")
        else:
            print("ALL GATES PASS")
        if reviewer_skipped:
            print(f"REVIEWER NOT RUN (not covered by this verdict): {reviewer_skipped}")
        if "--require-elaboration" in flags:
            return tb._require_elaboration_verdict([tuple(s) for s in sk])
    return rc


if __name__ == "__main__":
    sys.exit(main())
