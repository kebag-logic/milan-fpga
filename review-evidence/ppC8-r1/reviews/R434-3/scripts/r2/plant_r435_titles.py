#!/usr/bin/env python3
"""Reviewer re-creation, from the titles of the other round-1 review's F4
survivor table only (not its script), of each weakening on the round-2 code.
Usage: plant_r435_titles.py <head-tree> <work-dir> <name>"""
import sys, pathlib, importlib.util
here = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("plant_r2", here / "plant_r2.py")
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
R, L = base.R, base.L
base.PLANTS.clear()
base.PLANTS.update({
 "T-cap45":         (R, "FORMATS_MAX = 46 ", "FORMATS_MAX = 45 "),
 "T-rates7":        (R, "RATES_MAX = 8 ", "RATES_MAX = 7 "),
 "T-crf-ge1":       (R, "            if at_input[stream] != 1:", "            if at_input[stream] < 1:"),
 "T-aaf-ge1":       (R, "            if total != 1:", "            if total < 1:"),
 "T-waiver-anytype": (L, "if finding.check != self.check or (cfg, dtype) != self.where[:2]:", "if finding.check != self.check or cfg != self.where[0]:"),
 "T-waiver-anycfg": (L, "if finding.check != self.check or (cfg, dtype) != self.where[:2]:", "if finding.check != self.check or dtype != self.where[1]:"),
 "T-entity-cfg":    (R, "        if cfg != 0:\n            ctx.bad(\"entity-count\"", "        if False:\n            ctx.bad(\"entity-count\""),
 "T-iface-subset":  (R, "            seen = first.setdefault(port, (cfg, index))\n            if seen[1] != index:", "            seen = first.setdefault(port, (cfg, index))\n            if seen[1] != index and index in ctx.of(seen[0], D.AVB_INTERFACE) and False:"),
})
sys.argv = [sys.argv[0]] + sys.argv[1:]
exec(compile(open(here / "plant_r2.py").read().split("if __name__")[1].split(":", 1)[1].replace("\n    ", "\n"), "main", "exec"), {**base.__dict__, "PLANTS": base.PLANTS})
