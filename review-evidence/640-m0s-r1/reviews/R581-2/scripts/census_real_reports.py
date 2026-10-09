#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent control-role census of published Vivado hierarchy reports.

Usage: census_real_reports.py <repo-checkout> <reports-root>
Each <reports-root>/<NN>/ holds baseline_hierarchy.rpt and a SOURCE line.
For each report, prints the design, state, an independent count per role
(module column, exact name or __parameterizedN, own rows excluded) and the
verdict of the head's pp_placement.all_fabric_problems() on the same file.
"""
import re
import sys
from pathlib import Path

repo, root = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_placement  # noqa: E402

ROLES = {"wrapper": "KL_pp_shadow", "adp": "KL_adp_engine", "acmp-listener": "KL_pp_acmp_listener",
         "acmp-talker": "KL_acmp_talker", "srp": "KL_srp_top", "maap": "KL_maap", "processor-maap": "KL_pp_maap",
         "aecp": "KL_aecp_engine", "notify": "KL_aecp_notify", "mailbox": "KL_mbx", "gptp": "KL_gptp_shadow"}
assert ROLES == pp_placement.MODULES, "role table drifted from the head"

for folder in sorted(p for p in root.iterdir() if p.is_dir()):
    text = (folder / "baseline_hierarchy.rpt").read_text()
    design = re.search(r"\| Design\s+: (\S+)", text)[1]
    state = re.search(r"\| Design State : (.+)", text)[1].strip()
    counts = dict.fromkeys(ROLES, 0)
    for line in text.splitlines():
        cells = line.split("|")
        if len(cells) != 12:
            continue
        instance, module = cells[1].strip(), cells[2].strip()
        if instance.startswith("(") or module == "Module":
            continue
        for role, name in ROLES.items():
            if module == name or re.fullmatch(re.escape(name) + r"__parameterized\d+", module):
                counts[role] += 1
    gate = pp_placement.all_fabric_problems(folder)
    source = (folder / "SOURCE").read_text().strip()
    print(f"{folder.name} design={design} state={state!r} counts={counts} "
          f"head_problems={len(gate)} {gate} :: {source}")
