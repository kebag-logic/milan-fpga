#!/usr/bin/env python3
"""R354-1 bypass probes for the bare-metal clock refusals (issue #582).

Usage (LiteX interpreter): bypass_probe.py <repo>
Runs the real builder and the real milan_soc.main() (stopped at the platform
boundary by the PR's own harness) on inputs the PR's tests do not list.
Prints ACCEPT/REFUSE per case; exits non-zero if any expectation fails.
"""
import copy
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(REPO / "sw/builder"))
sys.path.insert(0, str(REPO / "sw/litex"))
import yaml  # noqa: E402
import endstation_builder as eb  # noqa: E402
import test_clock_contract as tcc  # noqa: E402
import milan_soc  # noqa: E402

bad = 0


def expect(label: str, ok: bool, detail: str = "") -> None:
    global bad
    bad += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {label} {detail}")


# ---- SoC CLI: forms the PR's table does not list -------------------------
frag = eb.emit_soc_argv(eb.load_config(REPO / "configs/endstation_ax7101_1x1_tdm8.yaml"))
soc_cases = [
    ("equals form 100e6", ["--milan-clk-freq=100e6"], True),
    ("repeated option, last wins 100e6", ["--milan-clk-freq", "50e6", "--milan-clk-freq", "100e6"], True),
    ("repeated option, last wins 50e6", ["--milan-clk-freq", "100e6", "--milan-clk-freq", "50e6"], False),
    ("build.sh EXTRA appended after shipping argv", frag + ["--milan-clk-freq", "100e6"], True),
    ("build.sh EXTRA system clock only (Milan domain kept)", frag + ["--sys-clk-freq", "90e6"], False),
    ("disabled domain at 100 MHz system", ["--sys-clk-freq", "100e6", "--milan-clk-freq", "0"], True),
    ("negative zero falls back to system 100 MHz", ["--milan-clk-freq", "-0"], True),
    ("no Milan datapath, CPU on 50 MHz domain", ["--no-milan", "--milan-clk-freq", "50e6"], False),
    ("no Milan datapath, CPU on 100 MHz system", ["--no-milan"], True),
    ("sub-hertz above contract", ["--milan-clk-freq", "50000000.5"], True),
]
for label, argv, refused in soc_cases:
    try:
        tcc._soc_clock_case(milan_soc, argv, refused)
        expect(f"SoC {label}", True, "REFUSE" if refused else "ACCEPT")
    except AssertionError as exc:
        expect(f"SoC {label}", False, f"expected {'REFUSE' if refused else 'ACCEPT'}: {str(exc)[:160]}")

# ---- Builder: value forms the PR's table does not list -------------------
raw0 = yaml.safe_load((REPO / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
with tempfile.TemporaryDirectory() as tmp:
    td = Path(tmp)
    for label, value, accepted in (("string 100000000", "100000000", False),
                                   ("float 1e8", 1e8, False),
                                   ("bool true", True, False),
                                   ("string 50000000", "50000000", True),
                                   ("float 50000000.9 (int-normalised)", 50000000.9, True)):
        raw = copy.deepcopy(raw0)
        raw["board"]["constraints"]["milan_clk_hz"] = value
        p = td / "c.yaml"
        p.write_text(yaml.safe_dump(raw))
        try:
            cfg = eb.load_config(p)
            argv = eb.emit_soc_argv(cfg)
            got = argv[argv.index("--milan-clk-freq") + 1]
            expect(f"builder {label}", accepted, f"ACCEPT emits --milan-clk-freq {got}")
        except eb.ConfigError as exc:
            expect(f"builder {label}", not accepted, f"REFUSE {str(exc)[:120]}")

    # A valid configuration that omits the optional sys_clk_hz (board default).
    raw = copy.deepcopy(raw0)
    del raw["board"]["constraints"]["sys_clk_hz"]
    cdir = td / "configs"
    cdir.mkdir()
    p = cdir / "endstation_nosys.yaml"
    p.write_text(yaml.safe_dump(raw))
    cfg = eb.load_config(p)
    print(f"info builder accepts omitted sys_clk_hz -> {cfg['constraints']['sys_clk_hz']}")
    import test_pp_mem_bridge as tpm  # noqa: E402
    from unittest.mock import patch
    with patch.dict(tpm.configured_clock_pairs.__globals__, HERE=td / "sw/litex"):
        try:
            print("info configured_clock_pairs ->", tpm.configured_clock_pairs())
        except Exception as exc:  # noqa: BLE001
            print(f"info configured_clock_pairs raises {type(exc).__name__}: {exc}")
    env = dict(os.environ, SWEEP_CFG=str(p))
    r = subprocess.run(["bash", str(REPO / "sw/litex/sweep_extra.sh"), "ax7101", "t", "--dry-run"],
                       capture_output=True, text=True, cwd="/")
    print(f"info sweep_extra (cwd=/) omitted sys_clk_hz rc={r.returncode}: "
          f"{' '.join(r.stdout.split()[3:9]) or r.stderr.strip()[:160]}")
    r = subprocess.run(["bash", str(REPO / "sw/litex/sweep_extra.sh"), "ax7101", "t", "--dry-run"],
                       capture_output=True, text=True, cwd="/", env=env)
    print(f"info sweep_extra (cwd=/) SWEEP_CFG=omitted-sys rc={r.returncode}: "
          f"{' '.join(r.stdout.split()[3:9]) or r.stderr.strip()[:160]}")

print(f"bypass probe failures={bad}")
sys.exit(1 if bad else 0)
