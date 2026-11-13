#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned planted-defect probes of SRP's Talker declarations (beyond the lane's own plant table).

Each probe edits a copy of sw/firmware/ctrl (never the checkout), then runs the lane's Talker suites through the
repository's own arm builder: srp_talker.cpp at 1x1/1if and 8x8/2if, and test_acmp_mbx.cpp's SrpGate.* at 8x8/2if and
1x1/1if. A probe is KILLED when any arm fails, SURVIVED when every arm passes. Usage:
  probe_talker.py REPO OUT [PROBE ...]
"""
import shutil
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(REPO / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(REPO / "sw/firmware/gtest"))
from ctrl_build import CTRL, ROOT, Tree  # noqa: E402
import fw_gtest  # noqa: E402
from srp_arms import arm_srp  # noqa: E402

SRP = "srp/srp_mbx.c"
APP = "app/ctrl_app_srp.c"
PROBES = {
    # the control: no edit, every arm must pass
    "baseline-unplanted": (SRP, "#define SRP_JOIN_CS 20u\n", "#define SRP_JOIN_CS 20u\n"),
    # srp_mbx_gate records a change but owes no pass: the declaration waits for some later transmit opportunity
    "gate-owes-no-pass": (SRP, "            i->sources_owed = true;\n            hold(i);\n        }\n    }\n",
                          "            i->sources_owed = true;\n        }\n    }\n"),
    # the hold-off's end owes no pass: the changed destination waits for some later transmit opportunity
    "hold-off-end-owes-no-pass": (SRP, "                    i->sources_owed = true;\n                    hold(i);\n",
                                  "                    i->sources_owed = true;\n"),
    # the hold-off counted as exactly two LeaveAllTime periods from the Leave's request, no JoinTime/transmit margin
    "hold-off-margin-dropped": (SRP, "#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)",
                                "#define SRP_REDECLARE_CS (2u * 1000u)"),
    # the hold-off one centisecond short of two LeaveAllTime periods from the request
    "hold-off-1999": (SRP, "#define SRP_REDECLARE_CS (2u * 1000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)",
                      "#define SRP_REDECLARE_CS (1999u)"),
    # every interface fed interface 0's gate: a source would be declared on an interface that is not its own
    "feed-interface-0-everywhere": (APP, "app->maap.published_gate[interface],app->maap.ifs[interface].core.base);",
                                    "app->maap.published_gate[0],app->maap.ifs[0].core.base);"),
    # a reset forgets what the destroyed participants declared
    "reset-forgets-talkers": (SRP, "    i->msrp = NULL; i->mvrp = NULL; i->domain_owed = false;\n",
                              "    i->msrp = NULL; i->mvrp = NULL; i->domain_owed = false; i->talkers = 0u;\n"),
    # a declared source keeps its readdressed mark
    "readdressed-kept": (SRP, "                i->readdressed &= ~bit;\n", ""),
}
ARMS = (("srp_talker.cpp", "*", 1, None), ("srp_talker.cpp", "*", 2, "endstation_ax7101_8x8"),
        ("test_acmp_mbx.cpp", "SrpGate.*", 2, "endstation_ax7101_8x8"), ("test_acmp_mbx.cpp", "SrpGate.*", 1, None))


def run(name: str) -> str:
    path, old, new = PROBES[name]
    work = OUT / name
    src = work / "ctrl"
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    target = src / path
    text = target.read_text()
    if text.count(old) != 1:
        return f"REFUSED {name}: {text.count(old)} planting sites"
    target.write_text(text.replace(old, new))
    lwsrp = REPO / "third_party/lwSRP"
    verdicts = []
    for suite, flt, nif, cfg in ARMS:
        extra = {"config": ROOT / "configs" / (cfg + ".yaml")} if cfg else {}
        tree = Tree(src, work / "build", work / "reuse", fw_gtest.Build(jobs=2))
        res = arm_srp(tree, lwsrp, nif, test=(suite, flt), **extra)
        label = f"{suite}:{flt}@if{nif}{'-' + cfg if cfg else '-1x1'}"
        (OUT / f"{name}.{label.replace(':', '_').replace('*', 'all')}.log").write_text(res.log)
        fails = [ln.strip() for ln in res.log.splitlines() if ln.strip().startswith("[FAIL]")]
        verdicts.append(f"{label} rc={res.rc} fails={len(fails)} {fails[:3]}")
    killed = any("rc=0" not in v for v in verdicts)
    return f"{'KILLED' if killed else 'SURVIVED'} {name}\n  " + "\n  ".join(verdicts)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for probe in sys.argv[3:] or PROBES:
        print(run(probe), flush=True)
