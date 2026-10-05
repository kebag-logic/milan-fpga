#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: the bare-metal saved-state store of #665 lane F1, on the host, per shape.

WHAT IT RUNS. sw/firmware/ctrl_nvm is portable C11 with no heap: the KLJ2
codec, the store (the boot restore and the write-back) and two flash ports.
For every shipped shape (configs/endstation_*.yaml) the builder fixes the
shape and the identity, the store is compiled against the same constants
sw/litex/milan_soc.py publishes for the shipping writer, and the scenario
runner (test/nvm_test.c) drives it over the host flash model directly and
over the on-chip LiteSPI port on a model of the command master. The checks
(nvm_checks.py, nvm_checks_write.py) grade the boot path with valid, absent,
torn, corrupted and wrong-version slots, read faults at every boot read, and
the binding and D3 restore walks; the write path's commit, its A/B atomicity
and DR2a/DR2b/DR2c/DR5 rules, the console included; a power cut inside every
media effect of a commit; the time base under PHC steps and the counter's
wrap; a command master that stalls; the service bound; and the round trip
against the recorded vectors of tb/verilator/nvm_backend. Every byte and
every verdict is compared with scripts/nvm_klj2.py, the reference codec.

THE RV32 ARM (nvm_rv32.py) cross-compiles the store and the LiteSPI port
freestanding for RV32I and reports their static sizes per shape. Without a
compiler it is SKIPPED, visibly; --require-rv32 refuses instead.

NEGATIVE CONTROLS. --self-test plants every defect of nvm_mutants.py into a
copy of the tree, one at a time, at the shipping 1x1 shape, and requires each
check the defect names to fail. Every check is named by at least one defect.

Usage:
    python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py
    python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
    python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --config configs/endstation_ax7101_8x8.yaml

Exit 0 = every check passed (and every planted defect reddened); 1 = a
finding; 2 = refused (the bench could not be built, or no RV32 compiler under
--require-rv32).
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import nvm_mutants                                                      # noqa: E402
import nvm_rv32                                                         # noqa: E402
from nvm_bench import (ROOT, TREE, VECTOR_IDENT, Bench, Refusal,        # noqa: E402
                       ShapeInputs, make_bench, shape_inputs)
from nvm_checks import BOOT_CHECKS, BOOT_PORTS                          # noqa: E402
from nvm_checks_write import WRITE_CHECKS, WRITE_PORTS, table_exists    # noqa: E402

CHECKS: dict[str, Callable[[Bench, str], list[str]]] = {**BOOT_CHECKS, **WRITE_CHECKS}
PORTS = {**BOOT_PORTS, **WRITE_PORTS}
SELF_TEST_SHAPE = "endstation_ax7101_1x1_tdm8"


def bench_for(inputs: ShapeInputs, work: Path, tree: Path = TREE) -> Bench:
    """The store compiled for one shape, and under the recorded vectors'
    identity too where tb/verilator/nvm_backend records a vector of it."""
    b = make_bench(inputs, work / "store", tree)
    if table_exists(inputs.cfg.stem):
        b.vector = make_bench(inputs, work / "vector", tree, VECTOR_IDENT)
    return b


def grade(b: Bench, names: list[str]) -> dict[str, list[str]]:
    """Run the named checks on every port each one runs on."""
    out = {}
    for name in names:
        found = []
        for port in PORTS[name]:
            found += [f"{port or 'model'}: {x}" for x in CHECKS[name](b, port)]
        out[name] = found
    return out


def rv32_arm(inputs: ShapeInputs, work: Path, require: bool) -> list[str]:
    """The RV32I freestanding build of one shape, and its sizes."""
    cc = nvm_rv32.compiler()
    if cc is None:
        if require:
            raise Refusal("no RV32 compiler (the pinned SDK's riscv32-linux-gcc or a bare-metal one)")
        print(f"  rv32: SKIPPED for {inputs.cfg.stem}: no RV32 compiler; --require-rv32 refuses")
        return []
    found, sizes = nvm_rv32.build(TREE, work / "rv32", work / "store" / "gen", cc)
    if sizes:
        print(f"  rv32: text={sizes['text']} data={sizes['data']} bss={sizes['bss']} "
              f"stage={sizes.get('nvm_stage')} payload={sizes.get('nvm_payload')} "
              f"chunk={sizes.get('nvm_chunk')} store={sizes.get('nvm')} "
              f"clock={sizes.get('ls_ticks', 0) + sizes.get('ls_tick_last', 0)} (bytes)")
    return found


def self_test(inputs: ShapeInputs, work: Path) -> list[str]:
    """Plant every defect; each check it names must fail."""
    found = [f"self-test: no defect names the check {n}"
             for n in nvm_mutants.unnamed_checks(list(CHECKS))]
    for m in nvm_mutants.MUTANTS:
        tree = work / m.name / "tree"
        nvm_mutants.plant(m, tree)
        b = bench_for(inputs, work / m.name, tree)
        result = grade(b, list(m.kills))
        alive = nvm_mutants.survivors(m, result)
        if alive:
            found.append(f"self-test: {m.name} was NOT caught by {', '.join(alive)}")
        else:
            first = next(x for k in m.kills for x in result[k])
            print(f"  self-test OK: {m.name:<26} caught by {', '.join(m.kills)}; first: {first[:110]}")
    return found


def run_shape(cfg: Path, work: Path, args: argparse.Namespace) -> tuple[list[str], ShapeInputs]:
    """Every check (or the ones asked for) and the RV32 arm for one shape."""
    inputs = shape_inputs(cfg, work)
    b = bench_for(inputs, work)
    names = args.check or list(CHECKS)
    result = grade(b, names)
    findings = [f"{cfg.stem}: {name}: {x}" for name in names for x in result[name]]
    bad = sum(1 for name in names if result[name])
    print(f"{cfg.stem:<28} records={len(b.frames):3d} image={len(b.assemble(b.frames, 0)):5d} B "
          f"checks={len(names)} failed={bad} runs={b.runs + (b.vector.runs if b.vector else 0)}")
    findings += [f"{cfg.stem}: {x}" for x in rv32_arm(inputs, work, args.require_rv32)]
    return findings, inputs


def main() -> int:
    """Grade every shipped shape; with --self-test, the planted defects too."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--config", action="append", type=Path,
                    help="configs to grade (default: every configs/endstation_*.yaml)")
    ap.add_argument("--check", action="append", choices=list(CHECKS),
                    help="run only these checks")
    ap.add_argument("--self-test", action="store_true",
                    help="also plant every defect and require its named checks to fail")
    ap.add_argument("--require-rv32", action="store_true",
                    help="refuse, rather than skip, when no RV32 compiler is present")
    args = ap.parse_args()
    cfgs = args.config or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    findings: list[str] = []
    try:
        with tempfile.TemporaryDirectory(prefix="ctrl-nvm.") as tmp:
            inputs_by_stem = {}
            for cfg in cfgs:
                got, inputs = run_shape(cfg, Path(tmp) / cfg.stem, args)
                findings += got
                inputs_by_stem[cfg.stem] = inputs
            if args.self_test and not findings:
                target = inputs_by_stem.get(SELF_TEST_SHAPE) or next(iter(inputs_by_stem.values()))
                findings += self_test(target, Path(tmp) / "self-test")
    except Refusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    for x in findings:
        print(f"FINDING: {x}")
    if findings:
        return 1
    print(f"saved-state store gate (#665 F1): OK across {len(cfgs)} shape(s), {len(CHECKS)} checks"
          + (f", and all {len(nvm_mutants.MUTANTS)} planted defects reddened" if args.self_test else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
