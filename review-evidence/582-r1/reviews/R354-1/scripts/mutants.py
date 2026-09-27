#!/usr/bin/env python3
"""R354-1 disposable kill-tests for PR #596 (issue #582).

Usage: mutants.py <repo> <python-with-litex> [mutant-id ...]

Each mutant applies one exact text substitution (asserted to match exactly
once), runs the focused test named for it, records rc and the tail, then
restores the file with `git checkout -- <file>`. A mutant is KILLED when the
focused test exits non-zero. Tree cleanliness is asserted after every mutant.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
PY = sys.argv[2]
ONLY = set(sys.argv[3:])

B = "sw/builder/endstation_builder.py"
S = "sw/litex/milan_soc.py"
R = "tb/verilator/nvm_capture_cpu/recipe.py"
X = "sw/litex/sweep_extra.sh"
M = "sw/litex/test_pp_mem_bridge.py"
T = "docs/AAF_LATENCY_TAPS.md"

CC = ([PY, "test_clock_contract.py"], "sw/builder")
CC_SOC = ([PY, "-c", "import test_clock_contract as t; t.test_soc_clock_contract()"], "sw/builder")
CC_BUILD = ([PY, "-c", "import test_clock_contract as t; t.test_baremetal_clock_contract()"], "sw/builder")
CC_SWEEP = ([PY, "-c", "import test_clock_contract as t; t.test_extra_sweep_clocks()"], "sw/builder")
CC_TAPS = ([PY, "-c", "import test_clock_contract as t; t.test_tap_clock_docs()"], "sw/builder")
PAIRS = ([PY, "-c", "import test_pp_mem_bridge as t; t.test_configured_clock_pairs()"], "sw/litex")
ROM1B = ([PY, str(Path(__file__).resolve().parent / "rom_clock_probe.py")], "sw/builder")

MUTANTS = [
    ("M01-builder-guard-removed", B,
     'if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:', 'if False:', CC_BUILD),
    ("M02-builder-guard-ceiling", B,
     'if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:', 'if cons["milan_clk_hz"] > BAREMETAL_CLK_HZ:', CC_BUILD),
    ("M03-builder-guard-floor", B,
     'if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:', 'if cons["milan_clk_hz"] < BAREMETAL_CLK_HZ:', CC_BUILD),
    ("M04-builder-message-unnamed", B,
     'f"baremetal clock: milan_clk_hz must be', 'f"clock: milan_clk_hz must be', CC_BUILD),
    ("M05-builder-scala-message-narrowed", B,
     'no scala_args overrides")', 'no cache/prefetch scala_args")', CC_BUILD),
    ("M06-soc-guard-removed", S,
     "if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:", "if False:", CC_SOC),
    ("M07-soc-ignores-system-fallback", S,
     "if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:",
     "if args.milan_clk_freq and args.milan_clk_freq != BAREMETAL_CLK_HZ:", CC_SOC),
    ("M08-soc-guard-ceiling", S,
     "if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:",
     "if (args.milan_clk_freq or args.sys_clk_freq) > BAREMETAL_CLK_HZ:", CC_SOC),
    ("M09-soc-message-unnamed", S,
     'ap.error(f"baremetal clock: effective', 'ap.error(f"clock: effective', CC_SOC),
    ("M10-soc-checks-system-only", S,
     "if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:",
     "if args.sys_clk_freq != BAREMETAL_CLK_HZ and not args.milan_clk_freq:", CC_SOC),
    ("M11-recipe-clock-100mhz", R,
     "CPU_HZ = 50_000_000", "CPU_HZ = 100_000_000", CC_BUILD),
    ("M12-sweep-hardcoded-pair", X,
     "clocks=$(clock_options)", 'clocks="--sys-clk-freq 100000000 --milan-clk-freq 50000000"', CC_SWEEP),
    ("M13-sweep-swallows-config-failure", X,
     "clocks=$(clock_options)", "clocks=$(clock_options) || true", CC_SWEEP),
    ("M14-sweep-board-check-removed", X,
     'if cfg["board_target"] != sys.argv[3]:', 'if False:', CC_SWEEP),
    ("M15-sweep-ignores-SWEEP_CFG", X,
     'CFG="${SWEEP_CFG:-configs/endstation_arty_4x4.yaml}"', 'CFG="configs/endstation_arty_4x4.yaml"', CC_SWEEP),
    ("M16-pairs-swapped", M,
     'pairs.append((path.stem, clocks["sys_clk_hz"], clocks["milan_clk_hz"]))',
     'pairs.append((path.stem, clocks["milan_clk_hz"], clocks["sys_clk_hz"]))', PAIRS),
    ("M17-pairs-first-only", M,
     "    return pairs\n", "    return pairs[:1]\n", PAIRS),
    ("M18-pairs-milan-copied-to-sys", M,
     'pairs.append((path.stem, clocks["sys_clk_hz"], clocks["milan_clk_hz"]))',
     'pairs.append((path.stem, clocks["milan_clk_hz"], clocks["milan_clk_hz"]))', PAIRS),
    ("M19-tap-doc-old-10ns", T,
     "| `endstation_ax7101_1x1_tdm8` | 50000000 | 20 | present |",
     "| `endstation_ax7101_1x1_tdm8` | 50000000 | 10 | present |", CC_TAPS),
    ("M20-tap-doc-8x8-unpruned", T,
     "| `endstation_ax7101_8x8` | 50000000 | 20 | pruned |",
     "| `endstation_ax7101_8x8` | 50000000 | 20 | present |", CC_TAPS),
    # Coverage probe, not a kill claim by the author: the gPTP ROM's clock
    # input after the 80 MHz variant became a refusal.
    ("M21-rom-clock-not-forwarded", B,
     '             "--clk-hz", str(cfg["constraints"]["milan_clk_hz"])],',
     '             ],', ROM1B),
    ("M21b-rom-clock-not-forwarded-cc", B,
     '             "--clk-hz", str(cfg["constraints"]["milan_clk_hz"])],',
     '             ],', CC),
    ("M21c-rom-clock-not-forwarded-capture-gate", B,
     '             "--clk-hz", str(cfg["constraints"]["milan_clk_hz"])],',
     '             ],', ([PY, "scripts/check_nvm_capture.py"], ".")),
]


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True,
                          capture_output=True, text=True).stdout


def main() -> int:
    assert git("status", "--porcelain").strip() == "", "tree not clean before probes"
    survivors = 0
    for mid, rel, old, new, (cmd, cwd) in MUTANTS:
        if ONLY and mid not in ONLY:
            continue
        path = REPO / rel
        text = path.read_text()
        assert text.count(old) == 1, f"{mid}: anchor matches {text.count(old)} times"
        path.write_text(text.replace(old, new))
        try:
            proc = subprocess.run(cmd, cwd=REPO / cwd, capture_output=True, text=True,
                                  timeout=3600)
        finally:
            git("checkout", "--", rel)
        assert git("status", "--porcelain").strip() == "", f"{mid}: restore failed"
        tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
        verdict = "KILLED" if proc.returncode != 0 else "SURVIVED"
        survivors += verdict == "SURVIVED"
        print(f"{mid}: {verdict} rc={proc.returncode} test={' '.join(cmd[1:])[:70]}")
        for line in tail:
            print(f"    | {line[:220]}")
        sys.stdout.flush()
    print(f"survivors={survivors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
