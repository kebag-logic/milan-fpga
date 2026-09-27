#!/usr/bin/env python3
"""Re-apply, outside the builder bank, the two gate-1b datapath pins the PR
edits (sw/builder/test_builder.py reference_census for media_rebase_p_w /
mcr_restart_p_w and direct_initializer for mcr_restart_p_w) to the head
datapath and to each reviewer probe's mutated copy. The pin logic is copied
from test_builder.py at the reviewed head; this is a reproduction of two
assertions, not a run of the bank.

Usage: static_pin_probe.py <head milan_datapath.sv> <mutated copy>...
"""
import re
import sys

EXPECTED_RHS = ("crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) "
                "| crf_mr_toggle_p_w)")
CENSUS = {"media_rebase_p_w": 2, "mcr_restart_p_w": 2}


def blank_comments(text):
    text = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def check(path):
    src = blank_comments(open(path).read())
    problems = []
    for name, count in CENSUS.items():
        found = len(re.findall(rf"\b{re.escape(name)}\b", src))
        if found != count:
            problems.append(f"census {name}: {found} != {count}")
    m = list(re.finditer(r"(?m)^[ \t]*wire[ \t]+mcr_restart_p_w[ \t]*=[ \t]*(?P<value>[^;]+);", src))
    if len(m) != 1:
        problems.append(f"initializer count {len(m)}")
    elif re.sub(r"\s+", "", m[0].group("value")) != re.sub(r"\s+", "", EXPECTED_RHS):
        problems.append("initializer RHS differs: " + " ".join(m[0].group("value").split()))
    return problems


rc = 0
for i, p in enumerate(sys.argv[1:]):
    probs = check(p)
    verdict = ("ACCEPTED" if not probs else "REJECTED")
    if i == 0 and probs:
        rc = 1
    print(f"{verdict:9} {p}")
    for q in probs:
        print(f"          {q}")
sys.exit(rc)
