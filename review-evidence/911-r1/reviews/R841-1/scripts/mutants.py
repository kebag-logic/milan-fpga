#!/usr/bin/env python3
"""Reviewer mutation probes (#911), run in a disposable copy of the tree.

usage: mutants.py <tree copy> <litex python>
Each mutant replaces one exact text (it must occur once), runs the gates
named for it, records each gate's rc and last line, and restores the file.
A mutant is KILLED when at least one of its gates exits non-zero.
"""
import subprocess
import sys
from pathlib import Path

TREE, LITEX_PY = Path(sys.argv[1]), sys.argv[2]
GATE_1E = ["python3", "sw/builder/test_builder.py", "--gates",
           "test_qspi_owner_transition_completed_write_prefixes"]
TIMING = ["python3", "sw/builder/test_timing_grade.py", LITEX_PY]
VARIANTS = ["python3", "scripts/board_variants.py"]

MUTANTS = [
    ("K1 flash-pair dumps the live QSPI before proving the board", "sw/litex/deploy.sh",
     '    prove_board "$target_layout" "$target_bit" "$tmp" || exit 2\n\n'
     '    echo "[deploy] prove live QSPI bitstream on serial $SERIAL ($dump_bytes B)"\n'
     '    run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -o 0 --dump-flash \\\n'
     '        --file-size "$dump_bytes" "$live"\n',
     '\n    echo "[deploy] prove live QSPI bitstream on serial $SERIAL ($dump_bytes B)"\n'
     '    run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -o 0 --dump-flash \\\n'
     '        --file-size "$dump_bytes" "$live"\n'
     '    prove_board "$target_layout" "$target_bit" "$tmp" || exit 2\n',
     [GATE_1E]),
    ("K2 die check compares the family only", "sw/litex/qspi_owner_transition.py",
     "    if detected != _die(part):", "    if detected[:4] != _die(part)[:4]:", [GATE_1E]),
    ("K3 two disagreeing JEDEC forms accepted (first wins)", "sw/litex/qspi_owner_transition.py",
     "    if len(ids) != 1:", "    if not ids:", [GATE_1E]),
    ("K4 several FPGA models on the chain accepted", "sw/litex/qspi_owner_transition.py",
     "    if len(models) != 1:", "    if not models:", [GATE_1E]),
    ("K5 flash-images writes before proving the board", "sw/litex/deploy.sh",
     '    prove_board "$layout" "$bit" "$tmp" || exit 2\n    write_prepared_images "$rows"\n',
     '    write_prepared_images "$rows"\n    prove_board "$layout" "$bit" "$tmp" || exit 2\n',
     [GATE_1E]),
    ("K6 layout_for grows the slot but leaves the AEM at 0x400000", "sw/litex/flash_map.py",
     '            "aem": dict(layout["aem"], offset=slot)}', '            "aem": dict(layout["aem"])}',
     [TIMING, VARIANTS]),
    ("K7 layout_from_soch reverts to the fixed 4 MiB bitstream budget", "sw/litex/layout_from_soch.py",
     '"addr": 0x0, "budget": aem["offset"]})', '"addr": 0x0, "budget": 0x40_0000})',
     # test_timing_grade.py never reads layout_from_soch.py (no reference to it),
     # and needs a git checkout this disposable copy lacks.
     [GATE_1E, VARIANTS]),
    ("K8 the 200T recipe's programmer part reverts to the 100T", "sw/litex/build.sh",
     "ax7a200t)     echo \"$AX_FTDI ft232    xc7a200tfbg484 boot",
     "ax7a200t)     echo \"$AX_FTDI ft232    xc7a100tfgg484 boot", [GATE_1E]),
    ("K9 the deploy bitstream budget is capped at the AX7101's 4 MiB", "sw/litex/qspi_owner_transition.py",
     '    budget = bit_rows[0].get("budget", bit_rows[0].get("size"))\n',
     '    budget = min(bit_rows[0].get("budget", bit_rows[0].get("size")), 0x40_0000)\n',
     [GATE_1E]),
]
if len(sys.argv) > 3:   # run only the named mutants, e.g. K7,K9
    MUTANTS = [m for m in MUTANTS if m[0].split()[0] in sys.argv[3].split(",")]


def main() -> int:
    survived = 0
    for label, rel, old, new, gates in MUTANTS:
        path = TREE / rel
        original = path.read_text(encoding="utf-8")
        if original.count(old) != 1:
            print(f"SETUP-ERROR {label}: anchor occurs {original.count(old)} times")
            return 2
        path.write_text(original.replace(old, new), encoding="utf-8")
        results = []
        try:
            for gate in gates:
                r = subprocess.run(gate, cwd=TREE, text=True, capture_output=True, timeout=900)
                tail = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()]
                hit = [l for l in tail if "AssertionError" in l or "FAIL" in l or "accepted" in l]
                results.append((Path(gate[1]).name, r.returncode, (hit or tail or [""])[-1][:220]))
        finally:
            path.write_text(original, encoding="utf-8")
        killed = any(rc != 0 for _, rc, _ in results)
        survived += not killed
        print(f"{'KILLED  ' if killed else 'SURVIVED'} {label}")
        for name, rc, line in results:
            print(f"    {name} rc={rc}: {line}")
    print(f"{len(MUTANTS) - survived} killed, {survived} survived")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
