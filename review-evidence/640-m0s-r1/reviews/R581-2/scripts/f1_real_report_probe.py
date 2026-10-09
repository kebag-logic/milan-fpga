#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent F1 probe: the head gate's default (unmarked) selection on a real accepted route hierarchy report.

Usage: f1_real_report_probe.py <repo-checkout> <real baseline_hierarchy.rpt> <work-dir>

Builds the gate self-test's synthetic route measurement, records it as a private baseline, then swaps in the
published route-1x1 hierarchy report and plants population faults in it. For every case it runs `check`,
`record --write` and the printed `record`, and reports the exit status, whether each expected role is named,
and whether the private baseline bytes changed. The repository's own baseline is never touched.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

repo, real, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_resource_gate_selftest as st  # noqa: E402

MODULES = {"wrapper": "KL_pp_shadow", "adp": "KL_adp_engine", "acmp-listener": "KL_pp_acmp_listener",
           "acmp-talker": "KL_acmp_talker", "srp": "KL_srp_top", "maap": "KL_maap", "processor-maap": "KL_pp_maap",
           "aecp": "KL_aecp_engine", "notify": "KL_aecp_notify", "mailbox": "KL_mbx", "gptp": "KL_gptp_shadow"}

work.mkdir(parents=True, exist_ok=True)
entry = st.recorded(work / "rec", "route")
folder = st.fresh(work / "rec", "route")  # the recorded paths live under arm/
original_fixture = (folder / "baseline_hierarchy.rpt").read_text()
# As the gate's own --fuzz does: zero the recorded input digest so a changed report reaches judge().
entry["record"]["inputs_sha256"] = "0" * 64
baseline = work / "baseline.json"
baseline.write_text(json.dumps({"endpoints": {"route-1x1": entry}}))
pristine = baseline.read_bytes()
digest = hashlib.sha256(pristine).hexdigest()

text = real.read_text()


def module_lines(module):
    return [line for line in text.splitlines(keepends=True)
            if len(line.split("|")) == 12 and line.split("|")[2].strip() == module
            and not line.split("|")[1].strip().startswith("(")]


def drop(src, modules):
    """Remove each row whose module column is one of modules (own rows too), leaving the rest."""
    return "".join(line for line in src.splitlines(keepends=True)
                   if not (len(line.split("|")) == 12 and line.split("|")[2].strip() in modules))


def dup(src, module):
    line = module_lines(module)[0]
    copy = line.replace(line.split("|")[1], line.split("|")[1].replace(line.split("|")[1].strip(), "probe_dup"), 1)
    return src + copy


def rename(src, module, new):
    return src.replace(f" {module} |", f" {new} |")


def add_row(src, module):
    return src + f"|   probe_{module} | {module} | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |\n"


removed = ("KL_adp_engine", "KL_pp_acmp_listener", "KL_acmp_talker", "KL_srp_top", "KL_maap")
cases = [
    ("C0 real accepted route-1x1, unchanged", text, ()),
    ("C1 SRP removed", drop(text, {"KL_srp_top"}), ("srp",)),
    ("C2 wrapper-retaining F0-F4, no marker", drop(text, set(removed)), ("adp", "acmp-listener", "acmp-talker",
                                                                         "srp", "maap")),
    ("C3 ADP duplicated", dup(text, "KL_adp_engine"), ("adp",)),
    ("C4 talker module renamed (misplaced identity)", rename(text, "KL_acmp_talker", "KL_acmp_talker_x"),
     ("acmp-talker",)),
    ("C5 mailbox present", add_row(text, "KL_mbx"), ("mailbox",)),
    ("C6 processor MAAP present", add_row(text, "KL_pp_maap"), ("processor-maap",)),
    ("C7 gPTP plane removed", drop(text, {"KL_gptp_shadow"}), ("gptp",)),
    ("C8 AECP and notify removed", drop(text, {"KL_aecp_engine", "KL_aecp_notify"}), ("aecp", "notify")),
    ("C9 every role removed but wrapper", drop(text, set(MODULES.values()) - {"KL_pp_shadow"}),
     ("adp", "acmp-listener", "acmp-talker", "srp", "maap", "aecp", "notify", "gptp")),
    ("C10 specialised module names", re.sub(r" (KL_[a-z_]+) \|", lambda m: f" {m[1]}__parameterized3 |"
                                            if m[1] in MODULES.values() else m[0], text), ()),
]
report = folder / "baseline_hierarchy.rpt"
failures = 0
for label, body, roles in cases:
    report.write_text(body)
    out = []
    for command in (("check",), ("record", "--write"), ("record",)):
        baseline.write_bytes(pristine)  # each command starts from the private pristine baseline
        status, lines = st.cli(*command, folder, "--endpoint", "route-1x1", "--baseline", baseline)
        joined = " ".join(lines)
        named = {role: f"{role} ({MODULES[role]})" in joined for role in roles}
        changed = hashlib.sha256(baseline.read_bytes()).hexdigest() != digest
        out.append((" ".join(command), status, named, changed, lines[-1][:160] if lines else ""))
        printing = command == ("record",)
        expected = (0 if printing else 2) if roles else None
        if roles:  # a wrong population: refused by name (printing excepted, as documented), baseline untouched
            ok = not changed and status == expected and (printing or all(named.values()))
        else:  # a valid population: accepted; only record --write may (and does) rewrite the private baseline
            ok = status == 0 and "wrong placement" not in joined and changed == (command == ("record", "--write"))
        failures += not ok
        print(f"{'OK  ' if ok else 'FAIL'} {label} | {' '.join(command)} | exit {status} | named {named} | "
              f"baseline changed {changed} | {out[-1][4]}")
report.write_text(original_fixture)
print(f"f1 real-report probe: {len(cases)} cases x 3 commands, {failures} failures")
sys.exit(1 if failures else 0)
