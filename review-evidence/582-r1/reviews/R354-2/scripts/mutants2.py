#!/usr/bin/env python3
"""R354-2 disposable kill-tests for PR #596 (issue #582) at 77998f14.

Usage: mutants2.py <repo> <python-with-litex> [mutant-id ...]

Round-1 mutants M01-M21 are rerun at the new head (same substitutions; M21
now judged by the new bank ROM test). M22 is the system-clock-fed ROM mutant
(the external round-1 probe 36). S1-S4 and B3 are this reviewer's own
implementations of the external round-1 guard narrowings, written from their
published descriptions. M23-M31 target round-2 changes. C* are identity
controls: the same harness with no semantic change must pass (rc 0).

Each mutant applies one exact substitution (asserted to match exactly once),
runs the named focused test, records rc and tail, restores the file with
`git checkout -- <file>`, and asserts a clean tree. KILLED = test rc != 0.
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
CS = "scripts/ci_scope.py"
CW = "docs/testing/CI_WORKFLOWS.md"


def fn(module: str, name: str, cwd: str):
    return ([PY, "-c", f"import {module} as t; t.{name}()"], cwd)


CC = ([PY, "test_clock_contract.py", "--soc"], "sw/builder")
CC_SOC = fn("test_clock_contract", "test_soc_clock_contract", "sw/builder")
CC_BUILD = fn("test_clock_contract", "test_baremetal_clock_contract", "sw/builder")
CC_ROM = fn("test_clock_contract", "test_gptp_rom_clock", "sw/builder")
CC_SWEEP = fn("test_clock_contract", "test_extra_sweep_clocks", "sw/builder")
CC_TAPS = fn("test_clock_contract", "test_tap_clock_docs", "sw/builder")
PAIRS = fn("test_pp_mem_bridge", "test_configured_clock_pairs", "sw/litex")
ROM1B = ([PY, str(Path(__file__).resolve().parent / "rom_clock_probe.py")], "sw/builder")
SCOPE = ([PY, "scripts/ci_scope.py", "--selftest"], ".")
SOLDOC = ([PY, "scripts/check_solution_docs.py"], ".")

GUARD = "if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:"
BGUARD = 'if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:'
ROMARG = '             "--clk-hz", str(cfg["constraints"]["milan_clk_hz"])],'
PAIRLINE = 'pairs.append((path.stem, clocks["sys_clk_hz"], clocks["milan_clk_hz"]))'
NORM = 'clocks = eb.load_config(path)["constraints"]'
SWEEPC = 'c = cfg["constraints"]'

MUTANTS = [
    ("C1-control-builder-identity", B, BGUARD, BGUARD, CC),
    ("C2-control-soc-identity", S, GUARD, GUARD, CC_SOC),
    ("C3-control-pairs-identity", M, NORM, NORM, PAIRS),
    ("C4-control-sweep-identity", X, SWEEPC, SWEEPC, CC_SWEEP),
    ("C5-control-rom-identity", B, ROMARG, ROMARG, CC_ROM),
    ("M01-builder-guard-removed", B, BGUARD, "if False:", CC_BUILD),
    ("M02-builder-guard-ceiling", B, BGUARD, 'if cons["milan_clk_hz"] > BAREMETAL_CLK_HZ:', CC_BUILD),
    ("M03-builder-guard-floor", B, BGUARD, 'if cons["milan_clk_hz"] < BAREMETAL_CLK_HZ:', CC_BUILD),
    ("M04-builder-message-unnamed", B,
     'f"baremetal clock: milan_clk_hz must be', 'f"clock: milan_clk_hz must be', CC_BUILD),
    ("M05-builder-scala-message-narrowed", B,
     'no scala_args overrides")', 'no cache/prefetch scala_args")', CC_BUILD),
    ("M06-soc-guard-removed", S, GUARD, "if False:", CC_SOC),
    ("M07-soc-ignores-system-fallback", S, GUARD,
     "if args.milan_clk_freq and args.milan_clk_freq != BAREMETAL_CLK_HZ:", CC_SOC),
    ("M08-soc-guard-ceiling", S, GUARD,
     "if (args.milan_clk_freq or args.sys_clk_freq) > BAREMETAL_CLK_HZ:", CC_SOC),
    ("M09-soc-message-unnamed", S,
     'ap.error(f"baremetal clock: effective', 'ap.error(f"clock: effective', CC_SOC),
    ("M10-soc-checks-system-only", S, GUARD,
     "if args.sys_clk_freq != BAREMETAL_CLK_HZ and not args.milan_clk_freq:", CC_SOC),
    ("M11-recipe-clock-100mhz", R, "CPU_HZ = 50_000_000", "CPU_HZ = 100_000_000", CC_BUILD),
    ("M12-sweep-hardcoded-pair", X, "clocks=$(clock_options)",
     'clocks="--sys-clk-freq 100000000 --milan-clk-freq 50000000"', CC_SWEEP),
    ("M13-sweep-swallows-config-failure", X, "clocks=$(clock_options)",
     "clocks=$(clock_options) || true", CC_SWEEP),
    ("M14-sweep-board-check-removed", X, 'if cfg["board_target"] != sys.argv[3]:', "if False:", CC_SWEEP),
    ("M15-sweep-ignores-SWEEP_CFG", X, 'CFG="${SWEEP_CFG:-configs/endstation_arty_4x4.yaml}"',
     'CFG="configs/endstation_arty_4x4.yaml"', CC_SWEEP),
    ("M16-pairs-swapped", M, PAIRLINE,
     'pairs.append((path.stem, clocks["milan_clk_hz"], clocks["sys_clk_hz"]))', PAIRS),
    ("M17-pairs-first-only", M, "    return pairs\n", "    return pairs[:1]\n", PAIRS),
    ("M18-pairs-milan-copied-to-sys", M, PAIRLINE,
     'pairs.append((path.stem, clocks["milan_clk_hz"], clocks["milan_clk_hz"]))', PAIRS),
    ("M19-tap-doc-old-10ns", T, "| `endstation_ax7101_1x1_tdm8` | 50000000 | 20 | present |",
     "| `endstation_ax7101_1x1_tdm8` | 50000000 | 10 | present |", CC_TAPS),
    ("M20-tap-doc-8x8-unpruned", T, "| `endstation_ax7101_8x8` | 50000000 | 20 | pruned |",
     "| `endstation_ax7101_8x8` | 50000000 | 20 | present |", CC_TAPS),
    # Round-1 F2 survivor, now judged by the new bank test and the whole file.
    ("M21-rom-clock-not-forwarded", B, ROMARG, "             ],", CC_ROM),
    ("M21b-rom-clock-not-forwarded-cc", B, ROMARG, "             ],", CC),
    ("M21d-rom-clock-not-forwarded-gate1b-replica", B, ROMARG, "             ],", ROM1B),
    # External round-1 probe 36: the system clock fed to the generator.
    ("M22-rom-clock-is-sys", B, ROMARG,
     '             "--clk-hz", str(cfg["constraints"]["sys_clk_hz"])],', CC_ROM),
    ("M22b-rom-clock-is-sys-cc", B, ROMARG,
     '             "--clk-hz", str(cfg["constraints"]["sys_clk_hz"])],', CC),
    # This reviewer's implementations of the external S1-S4 and B3.
    ("S1-soc-guard-exempts-no-milan", S, GUARD,
     "if not args.no_milan and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:", CC_SOC),
    ("S2-soc-guard-exempts-full", S, GUARD,
     "if not args.full and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:", CC_SOC),
    ("S3-soc-guard-exempts-arty", S, GUARD,
     "if args.board != 'arty' and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:", CC_SOC),
    ("S4-soc-guard-exempts-spiflash", S, GUARD,
     "if not args.with_spiflash and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:", CC_SOC),
    ("B3-builder-guard-baremetal-flash-only", B, BGUARD,
     'if cons["flashboot"] == "baremetal" and cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:', CC_BUILD),
    # Round-2 item 6: the pair and sweep derivations must use normalized clocks.
    ("M23-pairs-raw-yaml", M, NORM,
     'clocks = yaml.safe_load(path.read_text())["board"]["constraints"]', PAIRS),
    ("M24-pairs-raw-yaml-wrong-default", M, NORM,
     'clocks = dict(yaml.safe_load(path.read_text())["board"]["constraints"]); '
     'clocks.setdefault("sys_clk_hz", clocks["milan_clk_hz"])', PAIRS),
    ("M25-sweep-omitted-sys-uses-milan", X, SWEEPC,
     'c = dict(cfg["constraints"]); import yaml; '
     'r = yaml.safe_load(open(Path(sys.argv[1]) / sys.argv[2]))["board"]["constraints"]; '
     'c["sys_clk_hz"] = r.get("sys_clk_hz", c["milan_clk_hz"])', CC_SWEEP),
    # Round-2 item 3: the product argv must carry the configured Milan clock.
    ("M26-builder-argv-drops-milan-clock", B,
     'opts += ["--milan-clk-freq", _freq(c["milan_clk_hz"])]', "pass", CC_SOC),
    # Round-2 item 1: the tap page registration.
    ("M27-scope-page-unregistered", CS, '    "docs/AAF_LATENCY_TAPS.md",\n', "", SCOPE),
    ("M28-scope-case-says-docs-only", CS, '(["docs/AAF_LATENCY_TAPS.md"], True),',
     '(["docs/AAF_LATENCY_TAPS.md"], False),', SCOPE),
    ("M29-ci-workflows-row-removed", CW,
     "| `sw/builder/test_clock_contract.py`: [AAF_LATENCY_TAPS.md](../AAF_LATENCY_TAPS.md) | `elaborate`, "
     "through `test_builder.py` | yes, through the same builder bank |\n", "", SCOPE),
    # Second commit: the solution-docs arm must still detect a changed default.
    ("M30-soc-system-default-80mhz", S, 'ap.add_argument("--sys-clk-freq", default=100e6,',
     'ap.add_argument("--sys-clk-freq", default=80e6,', SOLDOC),
    # Round-2 item 3: the no-Milan refusal via the system clock only.
    ("M31-soc-no-milan-checks-milan-only", S, GUARD,
     "if (args.milan_clk_freq or (0 if args.no_milan else args.sys_clk_freq)) != BAREMETAL_CLK_HZ "
     "and not (args.no_milan and not args.milan_clk_freq):", CC_SOC),
]


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True,
                          capture_output=True, text=True).stdout


def main() -> int:
    assert git("status", "--porcelain").strip() == "", "tree not clean before probes"
    survivors = []
    for mid, rel, old, new, (cmd, cwd) in MUTANTS:
        if ONLY and mid not in ONLY:
            continue
        path = REPO / rel
        text = path.read_text()
        assert text.count(old) == 1, f"{mid}: anchor matches {text.count(old)} times"
        path.write_text(text.replace(old, new))
        try:
            proc = subprocess.run(cmd, cwd=REPO / cwd, capture_output=True, text=True, timeout=3600)
        finally:
            git("checkout", "--", rel)
        assert git("status", "--porcelain").strip() == "", f"{mid}: restore failed"
        tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
        control = mid.startswith("C")
        if control:
            verdict = "CONTROL-PASS" if proc.returncode == 0 else "CONTROL-FAIL"
        else:
            verdict = "KILLED" if proc.returncode != 0 else "SURVIVED"
        if verdict in ("SURVIVED", "CONTROL-FAIL"):
            survivors.append(mid)
        print(f"{mid}: {verdict} rc={proc.returncode} test={' '.join(cmd[1:])[:80]}")
        for line in tail:
            print(f"    | {line[:220]}")
        sys.stdout.flush()
    print(f"unexpected={survivors}")
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
