#!/usr/bin/env python3
"""Dump milan_soc.py's argparse surface without running main's body.

Usage: python3 cli_dump.py <repo-root>
Prints, per option: dest, default, action type, choices, and help text, then
the full --help rendering. argparse.ArgumentParser.parse_args is patched to
record the parser and stop, so no SoC is elaborated.
"""
import argparse
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(root, "sw/litex"))
os.environ["COLUMNS"] = "100"


class Stop(Exception):
    pass


captured = {}


def fake_parse(self, *a, **k):
    captured["ap"] = self
    raise Stop


argparse.ArgumentParser.parse_args = fake_parse
sys.argv = ["milan_soc.py"]
import milan_soc  # noqa: E402

try:
    milan_soc.main()
except Stop:
    pass
ap = captured["ap"]
for act in ap._actions:
    print(f"OPT {act.dest} default={act.default!r} type={type(act).__name__} "
          f"choices={act.choices!r} help={act.help!r}")
print("----- --help -----")
print(ap.format_help())
