#!/usr/bin/env python3
"""Probe EQ through the builder bank's entry: does its verdict name the equal-clock arm?

Run from sw/builder. Reads test_builder.py's `for fn in (...)` run list, runs
every ROM-clock entry exactly as main() does (bank globals, bank SKIPPED) with a
planted equal-clock shape beside the tracked ones, and prints main()'s verdict.
Exit 0 only when the verdict names the arm.
"""
import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
import test_builder as bank  # noqa: E402
import test_clock_contract  # noqa: E402

loops = [node for node in ast.walk(ast.parse(Path("test_builder.py").read_text()))
         if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and node.target.id == "fn"]
names = [node.id for node in ast.walk(loops[0].iter) if isinstance(node, ast.Name)]
entries = [name for name in names if "rom_clock" in name and "ledger" not in name]
print("bank ROM-clock entries:", entries)


def equal_clocks(cfg: dict) -> None:
    """Plant sys_clk_hz == milan_clk_hz."""
    cfg["board"]["constraints"]["sys_clk_hz"] = cfg["board"]["constraints"]["milan_clk_hz"]


equal = bank._variant(bank.CONFIGS["ax7101_1x1_tdm8"], equal_clocks)
test_clock_contract.CONFIGS = [*test_clock_contract.CONFIGS, equal]
try:
    for name in entries:
        fn = getattr(bank, name, None) or getattr(test_clock_contract, name)
        print(f"{name}:")
        fn()
finally:
    equal.unlink()
verdict = (f"ALL GATES PASS EXCEPT {len(bank.SKIPPED)} NOT RUN" if bank.SKIPPED else "ALL GATES PASS")
for gate, why, _kind in bank.SKIPPED:
    print(f"  - [{gate}] {why}")
print(verdict)
sys.exit(0 if any(equal.stem in why for _gate, why, _kind in bank.SKIPPED) else 1)
