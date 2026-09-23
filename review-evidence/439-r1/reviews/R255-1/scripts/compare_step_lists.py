#!/usr/bin/env python3
"""Reviewer-owned: base vs head recorded step lists must differ only by the
added `run` records of the 38 scoped steps (issue 439). Also compares the
other public tables the change must not alter.
Usage: python3 compare_step_lists.py <base-root> <head-root>"""
import importlib.util
import pathlib
import sys


def load(root, name):
    spec = importlib.util.spec_from_file_location(name, pathlib.Path(root) / "scripts/ci_events.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


b, h = load(sys.argv[1], "base_ce"), load(sys.argv[2], "head_ce")
problems, added = [], 0
for table in ("RTL_SEQUENCE_PINS", "CARRIER_STEP_LISTS", "STEP_LISTS"):
    bt, ht = getattr(b, table), getattr(h, table)
    if set(bt) != set(ht):
        problems.append(f"{table} keys differ: {set(bt) ^ set(ht)}")
        continue
    for k in bt:
        if len(bt[k]) != len(ht[k]):
            problems.append(f"{table}{k} length differs")
            continue
        for i, (x, y) in enumerate(zip(bt[k], ht[k])):
            y2 = {kk: vv for kk, vv in y.items() if kk != "run" or "run" in x}
            if x != y2:
                problems.append(f"{table}{k}[{i}] non-run difference")
            if table == "RTL_SEQUENCE_PINS" and "run" in y and "run" not in x:
                added += 1
for name in ("ENV_FILE_WRITERS", "AGGREGATE_SCRIPTS", "CANONICAL_OWNERSHIP_SCRIPT",
             "SV2V_INSTALL", "OOC_SH_SELFTEST", "PHYSICAL_GPTP_CONTRACT",
             "CANONICAL_DEFAULT_BRANCH_SCRIPT", "FAST_VERDICT_ENV"):
    if getattr(b, name) != getattr(h, name):
        problems.append(f"{name} differs")
same_norm = all(b.normalize_script(s) == h.normalize_script(s) for s in (
    "a  b\\\n c\n\n# x\t y", "x y", "p\r\nq"))
print(f"run_records_added={added} normalize_script_same_on_samples={same_norm}")
print("problems=" + repr(problems))
sys.exit(0 if not problems and added == 38 and same_norm else 1)
