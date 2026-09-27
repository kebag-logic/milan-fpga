#!/usr/bin/env python3
"""Reviewer-owned mutation probes for #582 at the exact head.

Usage: 30_mutants.py <pristine-head-copy> <work-copy> [python-with-migen]
Each mutant replaces exactly one source span in a disposable copy, runs the
named test command, records KILLED (nonzero) or SURVIVED (zero), and restores
the pristine bytes before the next mutant.
"""
import filecmp
import json
import shutil
import subprocess
import sys
from pathlib import Path

HEAD, WORK = Path(sys.argv[1]), Path(sys.argv[2])
PY = sys.argv[3] if len(sys.argv) > 3 else sys.executable
B = "sw/builder/endstation_builder.py"
S = "sw/litex/milan_soc.py"
W = "sw/litex/sweep_extra.sh"
M = "sw/litex/test_pp_mem_bridge.py"
BUILDER_T = [PY, "-c", "import sys; sys.path.insert(0,'sw/builder'); import test_clock_contract as t; t.test_baremetal_clock_contract()"]
SOC_T = [PY, "-c", "import sys; sys.path.insert(0,'sw/builder'); import test_clock_contract as t; t.test_soc_clock_contract()"]
SWEEP_T = [PY, "-c", "import sys; sys.path.insert(0,'sw/builder'); import test_clock_contract as t; t.test_extra_sweep_clocks()"]
PPM_T = [PY, "test_pp_mem_bridge.py"]
GUARD = 'if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:'
SGUARD = "if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:"
IMPORT_B = "from tb.verilator.nvm_capture_cpu.recipe import CPU_HZ as BAREMETAL_CLK_HZ  # noqa: E402"
IMPORT_S = "from tb.verilator.nvm_capture_cpu.recipe import CPU_HZ as BAREMETAL_CLK_HZ"
MUTANTS = [
    # id, file, old, new, test, cwd
    # Controls: an identity replacement must leave every test green.
    ("C0 control builder test", B, GUARD, GUARD, BUILDER_T, "."),
    ("C1 control SoC test", S, SGUARD, SGUARD, SOC_T, "."),
    ("C2 control sweep test", W, "  clocks=$(clock_options)", "  clocks=$(clock_options)", SWEEP_T, "."),
    ("C3 control memory-bridge test", M, "    for path in paths:\n        clocks", "    for path in paths:\n        clocks", PPM_T, "sw/litex"),
    ("B1 builder guard reads sys_clk_hz", B, GUARD, 'if cons["sys_clk_hz"] != BAREMETAL_CLK_HZ:', BUILDER_T, "."),
    ("B2 builder guard tolerates +-1 kHz", B, GUARD, 'if abs(cons["milan_clk_hz"] - BAREMETAL_CLK_HZ) > 1000:', BUILDER_T, "."),
    ("B3 builder guard only for flashboot baremetal", B, GUARD, 'if cons["flashboot"] == "baremetal" and cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:', BUILDER_T, "."),
    ("B4 builder refusal drops the contract citation", B, '"(docs/integration/BAREMETAL_FIRMWARE.md build contract)")', '"(see docs)")', BUILDER_T, "."),
    ("B5 builder mirrors the literal instead of importing", B, IMPORT_B, "BAREMETAL_CLK_HZ = 50_000_000", BUILDER_T, "."),
    ("B6 builder guard only below 60 MHz window", B, GUARD, 'if not 40_000_000 <= cons["milan_clk_hz"] <= 60_000_000 or cons["milan_clk_hz"] in (49_999_999, 50_000_001):', BUILDER_T, "."),
    ("S1 SoC guard exempts --no-milan", S, SGUARD, "if not args.no_milan and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:", SOC_T, "."),
    ("S2 SoC guard exempts --full product argv", S, SGUARD, "if not args.full and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:", SOC_T, "."),
    ("S3 SoC guard exempts the arty board", S, SGUARD, 'if args.board != "arty" and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:', SOC_T, "."),
    ("S4 SoC guard exempts --with-spiflash", S, SGUARD, "if not args.with_spiflash and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:", SOC_T, "."),
    ("S5 SoC guard only when --build", S, SGUARD, "if args.build and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:", SOC_T, "."),
    ("S6 SoC guard ignores sys fallback", S, SGUARD, "if args.milan_clk_freq and args.milan_clk_freq != BAREMETAL_CLK_HZ:", SOC_T, "."),
    ("S7 SoC mirrors the literal instead of importing", S, IMPORT_S, "BAREMETAL_CLK_HZ = 50_000_000", SOC_T, "."),
    ("W1 sweep falls back to a literal clock", W, "  clocks=$(clock_options)", '  clocks=$(clock_options || echo "--sys-clk-freq 100e6 --milan-clk-freq 50e6")', SWEEP_T, "."),
    ("W2 sweep ignores SWEEP_CFG", W, 'CFG="${SWEEP_CFG:-configs/endstation_arty_4x4.yaml}"', 'CFG="configs/endstation_arty_4x4.yaml"', SWEEP_T, "."),
    ("W3 sweep drops the board check", W, 'if cfg["board_target"] != sys.argv[3]:', "if False:", SWEEP_T, "."),
    ("P1 precedence loop drops configured pairs", M, "for name, sys_hz, milan_hz in configured_clock_pairs() + HISTORICAL_CLOCK_PAIRS:", "for name, sys_hz, milan_hz in HISTORICAL_CLOCK_PAIRS:", PPM_T, "sw/litex"),
    ("P2 configured pairs keep only the first config", M, "    for path in paths:\n        clocks", "    for path in paths[:1]:\n        clocks", PPM_T, "sw/litex"),
]


def restore() -> None:
    for rel in (B, S, W, M):
        shutil.copyfile(HEAD / rel, WORK / rel)
        shutil.copymode(HEAD / rel, WORK / rel)
        assert filecmp.cmp(HEAD / rel, WORK / rel, shallow=False)


results = []
for mid, rel, old, new, cmd, cwd in MUTANTS:
    restore()
    text = (WORK / rel).read_text()
    count = text.count(old)
    if count != 1:
        results.append(dict(mutant=mid, status="NOT-APPLIED", occurrences=count))
        print(f"NOT-APPLIED {mid}: {count} occurrences")
        continue
    (WORK / rel).write_text(text.replace(old, new))
    proc = subprocess.run(cmd, cwd=WORK / cwd, capture_output=True, text=True, timeout=900)
    tail = (proc.stdout + proc.stderr).strip().splitlines()[-1:] or [""]
    status = "KILLED" if proc.returncode else "SURVIVED"
    if mid.startswith("C"):
        status = "CONTROL-PASS" if proc.returncode == 0 else "CONTROL-FAIL"
    results.append(dict(mutant=mid, status=status, returncode=proc.returncode, last_line=tail[0][:200]))
    print(f"{status} {mid}: rc {proc.returncode}; {tail[0][:160]}")
restore()
print("RESTORED: work copy sources equal the pristine head copy")
print(json.dumps(results, indent=1))
