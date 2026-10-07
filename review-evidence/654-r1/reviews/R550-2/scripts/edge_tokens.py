#!/usr/bin/env python3
"""Record CLI and constructor outcomes for boundary --l2-bytes values.

Usage: edge_tokens.py TREE
CPU setup, SoCCore construction and the front-end routing check are replaced by a
sentinel, so "setup" means every refusal was passed and nothing was generated.
"""
import contextlib
import io
import json
import sys
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/litex"))
import milan_soc
from litex.soc.cores.cpu.naxriscv import NaxRiscv
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv


class SetupStarted(Exception):
    pass


def guarded(fn):
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink), \
         patch.object(VexiiRiscv, "args_read", side_effect=SetupStarted), \
         patch.object(NaxRiscv, "args_read", side_effect=SetupStarted), \
         patch.object(milan_soc.SoCCore, "__init__", side_effect=SetupStarted), \
         patch.object(milan_soc.board_audio_routing, "assert_front_end_routed", side_effect=SetupStarted):
        try:
            fn()
        except SetupStarted:
            return {"kind": "setup"}
        except SystemExit as exc:
            return {"kind": "exit", "rc": exc.code, "reason": sink.getvalue().strip().splitlines()[-1]}
        except ValueError as exc:
            return {"kind": "refused", "reason": str(exc)}
        except Exception as exc:  # noqa: BLE001 - recorded as a crash, graded below
            return {"kind": "crash", "type": type(exc).__name__, "reason": str(exc)}
    return {"kind": "completed"}


def cli(token):
    argv = ["milan_soc.py", "--no-milan", "--sys-clk-freq=50000000", "--l2-bytes=" + token]

    def go():
        with patch.object(sys, "argv", argv):
            milan_soc.main()
    return guarded(go)


ZERO = ["0", "0.0", "-0", "-0.0", "+0", "0e-400", "0E+999999", " 0 ", "0_0", "000"]
WHOLE_NONZERO = ["8192", "8192.0", "8.192e3", "1E+999999", "1_000", "4096.000"]
FRACTIONAL = ["1e-400", "-1e-400", "1e-12", "0.5", "4096.0000000000000000000000001",
              "-1", "-8192", "nan", "-nan", "snan", "inf", "-Infinity", "invalid", "", "0x10"]
rows, bad = [], []
for group, tokens, expect in (("zero", ZERO, "setup"),
                              ("whole-nonzero", WHOLE_NONZERO, "without a data cache"),
                              ("fractional/invalid", FRACTIONAL, "whole number")):
    for token in tokens:
        out = cli(token)
        ok = out["kind"] == "setup" if expect == "setup" else (
            out["kind"] == "exit" and out["rc"] == 2 and expect in out["reason"])
        rows.append({"surface": "cli", "group": group, "token": token, "ok": ok, **out})
        if not ok:
            bad.append(("cli", token))

CONSTRUCTOR = [
    ("vexiiriscv", Decimal("1e-400"), "whole number"), ("vexiiriscv", Decimal("-0"), "setup"),
    ("vexiiriscv", Decimal("sNaN"), "whole number"), ("vexiiriscv", Decimal("NaN"), "whole number"),
    ("vexiiriscv", 0, "setup"), ("vexiiriscv", 0.0, "setup"), ("vexiiriscv", None, "setup"),
    ("vexiiriscv", 1e-300, "whole number"), ("vexiiriscv", -0.0, "setup"),
    ("naxriscv", Decimal("-0"), "keeps its nonzero default"), ("naxriscv", 0.0, "keeps its nonzero default"),
    ("naxriscv", Decimal("8192"), "setup"), ("naxriscv", 8192.0, "setup"),
    ("naxriscv", Decimal("1e-400"), "whole number"), ("naxriscv", float("-inf"), "whole number"),
    ("vexii", 0, "unsupported CPU"), ("VexiiRiscv", None, "unsupported CPU"),
    (" naxriscv", 0, "unsupported CPU"), (42, None, "unsupported CPU"),
]
for cpu, l2, expect in CONSTRUCTOR:
    out = guarded(lambda: milan_soc.MilanSoC(None, 50000000, xlen=32, with_milan=False, cpu=cpu, l2_bytes=l2))
    ok = out["kind"] == "setup" if expect == "setup" else (out["kind"] == "refused" and expect in out["reason"])
    rows.append({"surface": "constructor", "cpu": repr(cpu), "l2_bytes": repr(l2), "ok": ok, **out})
    if not ok:
        bad.append(("constructor", repr(cpu), repr(l2)))
print(json.dumps(rows, indent=1))
print("UNEXPECTED:", bad)
sys.exit(1 if bad else 0)
