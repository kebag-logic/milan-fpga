#!/usr/bin/env python3
"""Reviewer mutation probes for PR #619 items 1-4 and 6 (no LiteX needed).

Each mutant replaces exactly one occurrence of a source span in the probe
copy, runs the named check, restores the original bytes and records whether
the check went red (killed). A control run of each check on the unmutated
tree must be green first.

Usage: mutants.py <probe-tree> <out.jsonl> [ID ...]
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

CC = "sw/builder/test_clock_contract.py"
TD = "sw/builder/test_declarations.py"
EB = "sw/builder/endstation_builder.py"
MK = "tb/verilator/milan_dp/Makefile"
CPP = "tb/verilator/milan_dp/sim_ax1x1gptp.cpp"
SX = "sw/litex/sweep_extra.sh"
TB = "sw/builder/test_builder.py"


def call(fn: str, module: str = "test_clock_contract") -> list[str]:
    return ["python3", "-B", "-c",
            f"import sys; sys.path.insert(0, 'sw/builder'); import {module} as m; m.{fn}()"]


CHECKS = {
    "sim_clock": call("test_sim_clock"),
    "sweep_invocation": call("test_extra_sweep_invocation"),
    "sweep_clocks": call("test_extra_sweep_clocks"),
    "builder_clock_source": call("test_builder_clock_source"),
    "declarations": ["python3", "-B", TD],
    "mac_shape": call("test_mac_shape_contract", "test_declarations"),
    "hex_shape": call("test_hex_shape_contract", "test_declarations"),
    "rom_skip_ledger": ["python3", "-B", "-c",
                        "import sys; sys.argv=['x']; sys.path.insert(0,'sw/builder'); "
                        "import test_builder as t; t.test_rom_clock_skip_reaches_the_ledger()"],
}

# (id, item, file, old, new, checks that must go red)
MUTANTS = [
    ("I1-M1", 1, MK, "AX_GPTP_HZ := $(shell python3 -I -c 'import runpy, sys; print(runpy.run_path(sys.argv[1])[\"CPU_HZ\"])' $(CLOCK_RECIPE))",
     "AX_GPTP_HZ := 50000000", ["sim_clock"]),
    ("I1-M2", 1, CPP, "constexpr uint64_t kHz = MILAN_CLK_HZ_TB;", "constexpr uint64_t kHz = 50000000;", ["sim_clock"]),
    ("I1-M3", 1, MK, "\t  -CFLAGS \"-DMILAN_CLK_HZ_TB=$(AX_GPTP_HZ) -Wall -Wextra\" \\\n", "", ["sim_clock"]),
    ("I1-M4", 1, MK, "ifneq ($(.SHELLSTATUS),0)\n$(error $(CLOCK_RECIPE) did not yield CPU_HZ; the AX 1x1 simulation clock could not be derived)\nendif\n",
     "", ["sim_clock"]),
    ("I1-M5", 1, MK, "python3 $< --clk-hz $(AX_GPTP_HZ) --mac", "python3 $< --clk-hz 50000000 --mac", ["sim_clock"]),
    ("I1-M6", 1, CPP, "milan::tb::GptpLaunchObserver observer{kPeriodNs};", "milan::tb::GptpLaunchObserver observer{20};", ["sim_clock"]),
    ("I2-BASE", 2, SX, None, "BASE", ["sweep_invocation"]),
    ("I2-M1", 2, SX, '      "--entity-gen-dir", gen, sep="\\n")', '      sep="\\n")', ["sweep_clocks", "sweep_invocation"]),
    ("I2-M2", 2, SX, "      -*) usage \"unknown option $arg\";;\n", "", ["sweep_invocation"]),
    ("I2-M3", 2, SX, "    if built != gen:\n", "    if False:\n", ["sweep_invocation"]),
    ("I2-M4", 2, SX, "  export PATH=\"$HOME/litex-milan/venv/bin:$PATH\"\n  case", "  case", ["sweep_invocation"]),
    ("I2-M5", 2, SX, "  [ -n \"$TAG\" ] || usage \"empty tag\"\n", "", ["sweep_invocation"]),
    ("I2-M6", 2, SX, "if sys.argv[4] == \"0\":", "if False:", ["sweep_invocation"]),
    ("I3-B5", 3, EB, 'BAREMETAL_CLK_HZ = runpy.run_path(ROOT / "tb/verilator/nvm_capture_cpu/recipe.py")["CPU_HZ"]\nsys.path.insert(0, str(ROOT))\n',
     "BAREMETAL_CLK_HZ = 50_000_000\nsys.path.insert(0, str(ROOT))\n", ["builder_clock_source"]),
    ("I3-NS", 3, EB, 'BAREMETAL_CLK_HZ = runpy.run_path(ROOT / "tb/verilator/nvm_capture_cpu/recipe.py")["CPU_HZ"]\nsys.path.insert(0, str(ROOT))\n',
     "sys.path.insert(0, str(ROOT))\nfrom tb.verilator.nvm_capture_cpu.recipe import CPU_HZ as BAREMETAL_CLK_HZ  # noqa: E402\n",
     ["builder_clock_source"]),
    ("I4-M1", 4, CC, '                skip("clock contract", f"{path.stem}: system-clock ROM control not applicable, "\n',
     '                _print_skip("clock contract", f"{path.stem}: system-clock ROM control not applicable, "\n', ["rom_skip_ledger"]),
    ("I4-M2", 4, TB, "    test_gptp_rom_clock(skip=skip)\n", "    test_gptp_rom_clock()\n", ["rom_skip_ledger"]),
    ("I6-SIGN", 6, EB, 'HEX_TEXT = re.compile(r"(?:0[xX])?', 'HEX_TEXT = re.compile(r"[+-]?(?:0[xX])?', ["mac_shape", "hex_shape"]),
    ("I6-WS", 6, EB, "    match = HEX_TEXT.fullmatch(v)\n", "    match = HEX_TEXT.fullmatch(v.strip())\n", ["hex_shape"]),
    ("I6-WSMAC", 6, EB, "    text = HEX_TEXT.fullmatch(v)\n", "    text = HEX_TEXT.fullmatch(v.strip())\n", ["mac_shape"]),
    ("I6-DBLUS", 6, EB, "(?:_?[0-9A-Fa-f])*)", "(?:_*[0-9A-Fa-f])*)", ["mac_shape", "hex_shape"]),
    ("I6-TRAILUS", 6, EB, "(?:_?[0-9A-Fa-f])*)", "(?:_?[0-9A-Fa-f])*_?)", ["mac_shape", "hex_shape"]),
    ("I6-LEADUS", 6, EB, 'HEX_TEXT = re.compile(r"(?:0[xX])?(', 'HEX_TEXT = re.compile(r"(?:0[xX])?_?(', ["mac_shape", "hex_shape"]),
    ("I6-WIDTH", 6, EB, "    if len(digits) > bits // 4:\n", "    if int(digits, 16) >> bits:\n", ["hex_shape"]),
    ("I6-NOWIDTH", 6, EB, "    if len(digits) > bits // 4:\n", "    if False:\n", ["hex_shape"]),
    ("I6-MIXSEP", 6, EB, r"(?:\1[0-9A-Fa-f]{2}){4}", r"(?:[:-][0-9A-Fa-f]{2}){4}", ["mac_shape"]),
    ("I6-UNPAD", 6, EB, r'MAC_OCTETS = re.compile(r"[0-9A-Fa-f]{2}([:-])[0-9A-Fa-f]{2}(?:\1[0-9A-Fa-f]{2}){4}")',
     r'MAC_OCTETS = re.compile(r"[0-9A-Fa-f]{1,2}([:-])[0-9A-Fa-f]{1,2}(?:\1[0-9A-Fa-f]{1,2}){4}")', ["mac_shape"]),
    ("I6-MACCOUNT", 6, EB, "    if len(digits) != MAC48_MAX.bit_length() // 4:\n", "    if not 0 < len(digits) <= MAC48_MAX.bit_length() // 4:\n", ["mac_shape"]),
    ("I6-OLDMAC", 6, EB, "        digits = text[1].replace(\"_\", \"\")\n    else:\n        digits = \"\"\n",
     "        digits = text[1].replace(\"_\", \"\")\n    else:\n        digits = v.replace(\":\", \"\").replace(\"-\", \"\").replace(\"_\", \"\").zfill(12)\n",
     ["mac_shape"]),
    ("I6-ZERO", 6, EB, "    if not n:\n        raise ConfigError(f\"{ctx}: {v!r} is the all-zero MAC-48\")\n", "", ["declarations"]),
    ("I6-UNICODE", 6, EB, 'HEX_TEXT = re.compile(r"(?:0[xX])?([0-9A-Fa-f](?:_?[0-9A-Fa-f])*)")',
     'HEX_TEXT = re.compile(r"(?:0[xX])?([0-9A-Fa-f\\u0660-\\u0669](?:_?[0-9A-Fa-f\\u0660-\\u0669])*)")', ["hex_shape"]),
    ("I6-PREFIXOCT", 6, EB, r'MAC_OCTETS = re.compile(r"[0-9A-Fa-f]{2}', r'MAC_OCTETS = re.compile(r"(?:0x)?[0-9A-Fa-f]{2}', ["mac_shape"]),
    ("I6-DMACWIDE", 6, EB, "    dmac = _hex_text(s[\"stream_dmac_base\"], MAC48_MAX.bit_length(),", "    dmac = _hex_text(s[\"stream_dmac_base\"], EUI64_MAX.bit_length(),", ["hex_shape"]),
    ("I6-OUIWIDE", 6, EB, '    oui = _declared_uint(ent["vendor_oui"], 24, "entity.vendor_oui")', '    oui = _declared_uint(ent["vendor_oui"], 32, "entity.vendor_oui")', ["hex_shape"]),
]


def run(tree: Path, check: str) -> tuple[int, str]:
    r = subprocess.run(CHECKS[check], cwd=tree, text=True, capture_output=True, timeout=900)
    tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
    return r.returncode, tail[0][:300]


def main() -> int:
    tree, out = Path(sys.argv[1]), Path(sys.argv[2])
    only = set(sys.argv[3:])
    mutants = [m for m in MUTANTS if not only or m[0] in only]
    rows, bad = [], 0
    with out.open("w") as log:
        for check in sorted({c for m in mutants for c in m[5]}):
            rc, tail = run(tree, check)
            row = dict(kind="control", check=check, rc=rc, tail=tail, ok=rc == 0)
            bad += rc != 0
            log.write(json.dumps(row) + "\n"); log.flush()
            print(f"CONTROL {check}: rc={rc} {'PASS' if rc == 0 else 'FAIL'}")
        for mid, item, rel, old, new, checks in mutants:
            path = tree / rel
            original = path.read_bytes()
            try:
                if new == "BASE":
                    mutated = subprocess.run(["git", "-C", str(tree), "show", f"eaa88a32:{rel}"],
                                             capture_output=True, check=True).stdout
                else:
                    text = original.decode()
                    assert text.count(old) == 1, f"{mid}: span occurs {text.count(old)} times"
                    mutated = text.replace(old, new).encode()
                path.write_bytes(mutated)
                for check in checks:
                    t0 = time.time()
                    rc, tail = run(tree, check)
                    killed = rc != 0
                    row = dict(kind="mutant", id=mid, item=item, file=rel, check=check, rc=rc,
                               killed=killed, seconds=round(time.time() - t0, 1), tail=tail)
                    log.write(json.dumps(row) + "\n"); log.flush()
                    print(f"{mid} ({rel}) vs {check}: rc={rc} {'KILLED' if killed else 'SURVIVED'} | {tail}")
            finally:
                path.write_bytes(original)
    print(f"controls failing: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
