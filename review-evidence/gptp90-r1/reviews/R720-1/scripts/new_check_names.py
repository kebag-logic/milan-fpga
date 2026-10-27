#!/usr/bin/env python3
"""List the engine check names the PR adds or rewrites, and whether a named
author control (mutants.py `breaks`) or the author coverage map names each.

Usage: new_check_names.py BASE_TREE HEAD_TREE COVERAGE_MAP_MD
Names are taken from string literals passed to expect()/slew_probe()/
expect_policy_pair() and from snprintf templates, expanded over the tag
tables the harness uses (Failure tags, LossShape tags, s39 tags).
"""
import importlib.util
import re
import sys
from pathlib import Path

base, head, cov = map(Path, sys.argv[1:4])

LIT = re.compile(r'(?:expect|slew_probe|expect_policy_pair)\(\s*"((?:[^"\\]|\\.)*)"', re.S)
SNP = re.compile(r'snprintf\(n, sizeof n,\s*((?:"(?:[^"\\]|\\.)*"\s*)+)', re.S)
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')

TAGS89 = ["first grandmaster", "Sync stops", "no Follow_Up",
          "Follow_Up after the next Sync", "Follow_Up with the next sequenceId"]
TAGS90 = ["#90 no response", "#90 no follow-up", "#91 duplicated response",
          "#91 three responses"]


def names(src: str) -> set[str]:
    out = set(m.group(1) for m in LIT.finditer(src))
    for m in SNP.finditer(src):
        t = "".join(STR.findall(m.group(1)))
        if "%llu" in t:
            out |= {t.replace("%s", g).replace("%llu", str(k))
                    for g in TAGS90 for k in range(1, 7)}
        elif t.startswith("#89 %s"):
            out |= {t.replace("%s", g) for g in TAGS89}
        elif t.startswith("%s"):
            out |= {t.replace("%s", g) for g in TAGS90}
        else:
            out.add(t)
    return out


b = names((base / "tb/verilator/engine/sim_main.cpp").read_text())
h = names((head / "tb/verilator/engine/sim_main.cpp").read_text())
new = sorted(h - b)
spec = importlib.util.spec_from_file_location(
    "m", head / "tb/verilator/engine/mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
named = set()
for mu in m.MUTATIONS:
    named |= set(mu[4].split(" | "))
covtext = cov.read_text()
covered = set(re.findall(r"^\| (.+?) \| (.+?) \|$", covtext, re.M))
covnames = {c[0] for c in covered if c[1].strip()}
print(f"new or rewritten check names (static): {len(new)}")
for n in new:
    tag = ("NAMED" if n in named else "") + (" MAP" if n in covnames else "")
    print(f"{tag or 'NONE':10s} {n}")
