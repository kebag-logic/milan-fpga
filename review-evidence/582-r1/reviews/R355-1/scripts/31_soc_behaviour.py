#!/usr/bin/env python3
"""Reviewer probe: the real milan_soc.py main() on product and documented argv.

Usage: 31_soc_behaviour.py <tree> <label>
Runs main() up to the first platform step (the front-end routing check, which
follows every argument refusal) and records REFUSED (argparse exit 2, with the
message class) or ACCEPTED. Nothing is elaborated or written.
"""
import contextlib
import io
import sys
from pathlib import Path
from unittest.mock import patch

TREE = Path(sys.argv[1]).resolve(); LABEL = sys.argv[2]
sys.path.insert(0, str(TREE / "sw/builder")); sys.path.insert(0, str(TREE / "sw/litex"))
import endstation_builder as eb  # noqa: E402
import milan_soc  # noqa: E402


class Boundary(Exception):
    pass


def run(argv):
    err = io.StringIO()
    with patch.object(sys, "argv", ["milan_soc.py", *argv]), contextlib.redirect_stderr(err), \
            contextlib.redirect_stdout(io.StringIO()), \
            patch.object(milan_soc.board_audio_routing, "assert_front_end_routed", side_effect=Boundary):
        try:
            milan_soc.main()
        except Boundary:
            return "ACCEPTED", ""
        except SystemExit as exc:
            last = err.getvalue().strip().splitlines()[-1:] or [""]
            return f"REFUSED rc={exc.code}", last[0][:150]
    return "RETURNED", ""


def replace(argv, opt, value):
    out = list(argv)
    if opt in out:
        i = out.index(opt)
        if value is None:
            del out[i:i + 2]
        else:
            out[i + 1] = value
    elif value is not None:
        out += [opt, value]
    return out


cases = []
for path in sorted((TREE / "configs").glob("endstation_*.yaml")):
    argv = eb.emit_soc_argv(eb.load_config(path))
    n = path.stem
    cases.append((f"{n} configured argv", argv, "ACCEPTED"))
    for v in ("100e6", "80e6", "49999999", "50000001", "25e6"):
        cases.append((f"{n} product argv --milan-clk-freq {v}", replace(argv, "--milan-clk-freq", v), "REFUSED"))
    cases.append((f"{n} product argv without --milan-clk-freq (system fallback)", replace(argv, "--milan-clk-freq", None), "REFUSED"))
    cases.append((f"{n} product argv --milan-clk-freq 0 (disabled domain)", replace(argv, "--milan-clk-freq", "0"), "REFUSED"))
    cases.append((f"{n} product argv + --no-milan", [a for a in argv if a != "--fabric-gptp"] + ["--no-milan"], "ACCEPTED"))
    cases.append((f"{n} product argv + --no-milan at 100e6", [a for a in replace(argv, "--milan-clk-freq", "100e6") if a != "--fabric-gptp"] + ["--no-milan"], "REFUSED"))
    cases.append((f"{n} product argv --sys 50e6 no milan domain", replace(replace(argv, "--milan-clk-freq", None), "--sys-clk-freq", "50e6"), "ACCEPTED"))
    cases.append((f"{n} product argv duplicate --milan-clk-freq 100e6 last", argv + ["--milan-clk-freq", "100e6"], "REFUSED"))
    cases.append((f"{n} product argv duplicate --milan-clk-freq 50e6 last after 100e6", replace(argv, "--milan-clk-freq", "100e6") + ["--milan-clk-freq", "50e6"], "ACCEPTED"))
# The usage block at the head of milan_soc.py.
for argv in ([], ["--full"], ["--with-mac"], ["--no-milan"],
             ["--software-profile", "baremetal", "--cpu", "vexiiriscv", "--xlen", "32", "--with-spiflash", "--flashboot", "baremetal"]):
    cases.append(("header usage: milan_soc.py " + " ".join(argv), argv, "record"))
    cases.append(("header usage + --milan-clk-freq 50e6: " + " ".join(argv), argv + ["--milan-clk-freq", "50e6"], "record"))
bad = 0
for name, argv, expect in cases:
    got, msg = run(argv)
    ok = expect == "record" or (got.startswith(expect) and (expect != "REFUSED" or "baremetal clock:" in msg))
    bad += not ok
    print(f"[{LABEL}] {'ok ' if ok else 'BAD'} {got:<16} {name} :: {msg}")
print(f"[{LABEL}] {len(cases)} cases, {bad} unexpected")
sys.exit(1 if bad else 0)
