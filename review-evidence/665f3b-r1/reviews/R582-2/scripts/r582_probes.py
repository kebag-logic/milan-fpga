#!/usr/bin/env python3
"""Reviewer-owned disposable plants on the F3b round-2 DA_GATE code.

Each plant is applied to a copy of sw/firmware/ctrl (the campaign's own
`plant`), never to the checkout. A plant is KILLED when any check of any
listed arm fails; SURVIVED when every arm still passes. Usage:
    python3 r582_probes.py <checkout> <work dir> [jobs]
"""
from __future__ import annotations

import sys
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path[:0] = [str(checkout / "sw/firmware/ctrl/test"), str(checkout / "sw/firmware/gtest")]

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import Outcome, Refusal, Tree  # noqa: E402

M = ctrl_mutants.Mutant
MAAP = "maap/maap_mbx.c"
ARMS = ("acmp", "acmpif2", "maap", "maap_if2")
PLANTS = (
    M("r582-allocation-filter-removed", MAAP, "valid && s < count && demand", "valid && (s < count || 1) && demand",
      "maap", "", ""),
    M("r582-interface-filter-removed", MAAP, "m->acmp->cfg.source_interface[s] == interface && valid",
      "(m->acmp->cfg.source_interface[s] == interface || 1) && valid", "maap", "", ""),
    M("r582-maap-validity-removed", MAAP, "valid && s < count && demand", "s < count && demand",
      "maap", "", ""),
    M("r582-event-refresh-removed", MAAP, "i->armed = false;\n\t\t\trefresh_demand(m);",
      "i->armed = false;", "maap", "", ""),
    M("r582-rx-refresh-removed", MAAP, "refresh_demand(m);\n\tmaap_rx(", "maap_rx(", "maap", "", ""),
    M("r582-link-refresh-removed", MAAP, "i->link = ev->link_up;\n\t\t\trefresh_demand(m);",
      "i->link = ev->link_up;", "maap", "", ""),
    M("r582-poll-refresh-removed", MAAP, "bool owed = false;\n\trefresh_demand(m);", "bool owed = false;",
      "maap", "", ""),
    M("r582-range-cache-not-updated", MAAP,
      "m->published_gate[interface] = declaring(m, interface, count, valid);\n"
      "\t(void)mbx_pub_da_gate(interface, m->published_gate[interface]);",
      "(void)mbx_pub_da_gate(interface, declaring(m, interface, count, valid));", "maap", "", ""),
    M("r582-poll-writes-before-maap-poll", MAAP,
      "\t\towed = maap_poll(&m->ifs[k].core) || owed;\n\t\tconst struct maap *core = &m->ifs[k].core;\n"
      "\t\tuint32_t gate = declaring(m, k, core->count, core->valid);",
      "\t\tconst struct maap *core = &m->ifs[k].core;\n"
      "\t\tuint32_t gate = declaring(m, k, core->count, core->valid);\n"
      "\t\towed = maap_poll(&m->ifs[k].core) || owed;", "maap", "", ""),
    M("r582-demand-not-cleared", MAAP, "\tm->demand = 0u;\n\tif (m->acmp != NULL) {",
      "\tif (m->acmp != NULL) {", "maap", "", ""),
)

arms = {name: getattr(ctrl_arms, f"arm_{name}") for name in ARMS}
build = fw_gtest.Build(jobs=jobs)
reuse = work / "reuse"
survived = 0
for m in PLANTS:
    ctrl, stack = ctrl_mutants.plant(m, work)
    tree = Tree(ctrl, work / "work" / "build", reuse, build, stack)
    failing = []
    for name, arm in arms.items():
        try:
            outcome = arm(tree)
        except Refusal as exc:
            outcome = Outcome(name, 2, f"refused: {exc}")
        lines = [ln.strip() for ln in outcome.log.splitlines() if "[FAIL]" in ln]
        if outcome.rc != 0:
            failing.append(f"{name} rc={outcome.rc} first={lines[0] if lines else outcome.log[-300:]!r}")
    verdict = "KILLED" if failing else "SURVIVED"
    survived += not failing
    print(f"[{verdict}] {m.name}", flush=True)
    for f in failing:
        print(f"    {f}", flush=True)
print(f"r582 probes: {len(PLANTS) - survived} killed, {survived} survived of {len(PLANTS)}")
