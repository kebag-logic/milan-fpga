#!/usr/bin/env python3
"""R354-2: documented milan_soc.py usages, as written and with the stated
required options, run through main() up to the platform boundary; plus an
AST comparison of every argparse default between two revisions.

Usage (from the repository root, LiteX interpreter):
  soc_usage_probe.py <base-rev>
"""
import ast
import contextlib
import io
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/litex"))
sys.path.insert(0, str(ROOT / "sw/builder"))
import milan_soc  # noqa: E402
import endstation_builder as eb  # noqa: E402

CLOCK = str(eb.BAREMETAL_CLK_HZ)
GEN = ["--entity-gen-dir", "configs/generated/endstation_ax7101_1x1_tdm8"]


class BeforePlatform(Exception):
    pass


def outcome(argv):
    err = io.StringIO()
    with patch.object(sys, "argv", ["milan_soc.py", *argv]), contextlib.redirect_stderr(err), \
            patch.object(milan_soc.board_audio_routing, "assert_front_end_routed", side_effect=BeforePlatform):
        try:
            milan_soc.main()
        except BeforePlatform:
            return "REACHES-PLATFORM", ""
        except SystemExit as exc:
            return f"EXIT-{exc.code}", err.getvalue().strip().splitlines()[-1][:200]
    return "RETURNED", ""


def documented_usages():
    """Parse the header usage lines ('#   ./milan_soc.py ...' plus continuations)."""
    lines = (ROOT / "sw/litex/milan_soc.py").read_text().splitlines()[:40]
    usages, pending = [], None
    for line in lines:
        body = line[1:].strip() if line.startswith("#") else ""
        if pending is not None:
            pending += " " + body.split("#")[0].rstrip("\\ ").strip()
            if not body.endswith("\\"):
                usages.append(pending.split())
                pending = None
            continue
        if body.startswith("./milan_soc.py"):
            code = body.split("#")[0].strip()
            if code.endswith("\\"):
                pending = code.rstrip("\\ ")
            else:
                usages.append(code.split())
    return [u[1:] for u in usages]


def defaults(source: str) -> dict:
    out = {}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "add_argument":
            names = [a.value for a in node.args if isinstance(a, ast.Constant)]
            kw = {k.arg: ast.unparse(k.value) for k in node.keywords if k.arg != "help"}
            out[tuple(names)] = kw
    return out


failures = 0
for argv in documented_usages():
    as_written = outcome(argv)
    required = ["--sys-clk-freq", CLOCK] if "--no-milan" in argv else ["--milan-clk-freq", CLOCK]
    with_required = outcome(argv + required + ([] if "--no-milan" in argv else GEN))
    print(f"usage {' '.join(argv) or '(none)'}")
    print(f"   as written: {as_written[0]} {as_written[1]}")
    print(f"   + required: {with_required[0]} {with_required[1]}")
    if as_written[0] == "EXIT-2" and "baremetal clock:" not in as_written[1]:
        failures += 1
    if with_required[0] != "REACHES-PLATFORM":
        failures += 1

base = subprocess.run(["git", "show", f"{sys.argv[1]}:sw/litex/milan_soc.py"], capture_output=True,
                      text=True, check=True).stdout
head = (ROOT / "sw/litex/milan_soc.py").read_text()
db, dh = defaults(base), defaults(head)
changed = {k: (db.get(k), dh.get(k)) for k in set(db) | set(dh) if db.get(k) != dh.get(k)}
print(f"argparse options: base {len(db)}, head {len(dh)}; non-help keyword differences: {changed or 'none'}")
failures += bool(changed)
print(f"failures={failures}")
sys.exit(1 if failures else 0)
