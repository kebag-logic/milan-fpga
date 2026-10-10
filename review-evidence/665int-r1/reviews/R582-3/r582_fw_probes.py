#!/usr/bin/env python3
"""r582_fw_probes.py - R582-3 disposable firmware plants beyond the author's tables.

Usage: r582_fw_probes.py <checkout> <lwsrp> <scratch-root>

Each plant edits a COPY of <checkout>/sw/firmware/ctrl (the gate's own plant()
copies it), builds the named arm(s) or the full srp_mbx.cpp suite with the
gate's own builders, and prints every [FAIL] line. A control run of each arm
kind, unplanted, comes first. Nothing in <checkout> is written.
"""
import sys
from pathlib import Path

checkout, lwsrp, root = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import shutil  # noqa: E402

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Outcome, Refusal, Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

assert CTRL == checkout / "sw/firmware/ctrl", CTRL
build = fw_gtest.Build(jobs=4)
reuse = root / "reuse"
cut_reuse(reuse)
ARMS = {"acmp": ctrl_arms.arm_acmp, "unit": ctrl_arms.arm_unit, "model": ctrl_arms.arm_model,
        "acmpif2": ctrl_arms.arm_acmpif2}


def fails(o: Outcome) -> list[str]:
    return [ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln]


def report(name: str, outs: list[Outcome], expect: str) -> None:
    f = [x for o in outs for x in fails(o)]
    rcs = ",".join(f"{o.arm}={o.rc}" for o in outs)
    hit = [x for x in f if expect and expect in x]
    verdict = "CONTROL-CLEAN" if not expect and not f and all(o.rc == 0 for o in outs) else \
        "CONTROL-DIRTY" if not expect else "CAUGHT" if hit else "ESCAPED" if not f else "CAUGHT-ELSEWHERE"
    print(f"[{verdict}] {name} (rc {rcs}): {len(f)} failing check(s)", flush=True)
    for x in (hit or f)[:3]:
        print(f"    {x[:220]}", flush=True)


CTRL_PLANTS = (
    (Mutant("r582-unbind-keeps-started", "acmp/acmp.c",
            "\ts->started = false;\n\ts->probing = ACMP_PROBING_DISABLED;",
            "\ts->probing = ACMP_PROBING_DISABLED;", "acmp", "", ""), ("acmp",), "A31"),
    (Mutant("r582-adapter-sid-valid-always", "acmp/acmp_mbx.c",
            "(void)mbx_pub_sink_binding(interface, sink, bound, started, stream_id != 0u);",
            "(void)mbx_pub_sink_binding(interface, sink, bound, started, true);", "acmp", "", ""),
     ("acmp", "acmpif2"), "B1"),
    (Mutant("r582-driver-started-on-sid-valid", "mbx/mbx.c",
            "mbx_place(started ? 1u : 0u, MBX_BINDING_STARTED_LSB, MBX_BINDING_STARTED_WIDTH)",
            "mbx_place(started ? 1u : 0u, MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH)",
            "unit", "", ""), ("unit",), "D14"),
    (Mutant("r582-restore-started-dropped", "acmp/acmp.c",
            "\t\ts->started = (payload[0] & BIND_STARTED) != 0u;", "\t\ts->started = false;", "acmp", "", ""),
     ("acmp",), "A31Restored"),
    (Mutant("r582-model-started-from-bound", "host/mbx_model.c",
            "out->started[k] = mbx_field(binding, MBX_BINDING_STARTED_LSB, MBX_BINDING_STARTED_WIDTH) != 0u;",
            "out->started[k] = mbx_field(binding, MBX_BINDING_BOUND_LSB, MBX_BINDING_BOUND_WIDTH) != 0u;",
            "model", "", ""), ("model", "acmp"), "Publication"),
)

SRP_PLANTS = (
    ("r582-withdraw-on-interface-0", "    withdraw_declared(i->index);\n    msrp_app_destroy",
     "    withdraw_declared(0u);\n    msrp_app_destroy", "PubTalkerDecl"),
    ("r582-declarations-cleared-at-adoption", "    (void)declare_sources(i);\n    i->domain_owed = false;",
     "    (void)declare_sources(i);\n    withdraw_declared(i->index);\n    i->domain_owed = false;", "Pub"),
    ("r582-declarations-published-to-interface-0", "    (void)mbx_pub_talker_decl(i->index,declared);",
     "    (void)mbx_pub_talker_decl(0u,declared);", "PubTalkerDecl"),
)

print("== controls (unplanted)", flush=True)
ctl = Tree(CTRL, root / "control" / "build", reuse, build)
report("control acmp/unit/model/acmpif2", [ARMS[a](ctl) for a in ARMS], "")
report("control srp_mbx.cpp at two interfaces", [srp_arms.arm_srp(ctl, lwsrp, 2)], "")

print("== ctrl plants", flush=True)
for m, arms, expect in CTRL_PLANTS:
    try:
        tree = Tree(ctrl_mutants.plant(m, root), root / "work" / "build", reuse, build)
        report(m.name, [ARMS[a](tree) for a in arms], expect)
    except Refusal as exc:
        print(f"[REFUSED] {m.name}: {exc}", flush=True)

print("== SRP plants (full srp_mbx.cpp suite, two interfaces)", flush=True)
for name, old, new, expect in SRP_PLANTS:
    work = root / "srpwork" / "ctrl"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(CTRL, work, ignore=shutil.ignore_patterns("__pycache__"))
    t = work / "srp/srp_mbx.c"
    s = t.read_text()
    if s.count(old) != 1:
        print(f"[REFUSED] {name}: fixture occurs {s.count(old)} times", flush=True)
        continue
    t.write_text(s.replace(old, new))
    try:
        report(name, [srp_arms.arm_srp(Tree(work, root / "srpwork" / "build", reuse, build), lwsrp, 2)], expect)
    except Refusal as exc:
        print(f"[REFUSED] {name}: {exc}", flush=True)
shutil.rmtree(root / "work", ignore_errors=True)
shutil.rmtree(root / "srpwork", ignore_errors=True)
print("probes done", flush=True)
