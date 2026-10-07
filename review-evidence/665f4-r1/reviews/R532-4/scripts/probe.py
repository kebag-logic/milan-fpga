#!/usr/bin/env python3
"""R532-4 probes: baseline SRP suites and reviewer-planted defects.

Usage (from anywhere; REPO is the reviewed checkout, LWSRP the pinned lwSRP):
  probe.py REPO LWSRP OUT baseline SUITE IF [debug]
  probe.py REPO LWSRP OUT plant NAME IF
Plants are applied to a disposable copy of sw/firmware/ctrl under OUT; the
reviewed checkout is never written. Exit 0 = probe ran (verdict in the log).
"""
import shutil
import sys
from pathlib import Path

REPO, LWSRP, OUT = (Path(a).resolve() for a in sys.argv[1:4])
MODE = sys.argv[4]
sys.path[:0] = [str(REPO / "sw/firmware/ctrl/test"), str(REPO / "sw/firmware/gtest")]
from ctrl_build import CTRL, Tree, Refusal  # noqa: E402
import fw_gtest  # noqa: E402
from srp_arms import arm_srp  # noqa: E402
from srp_mutants import caught, DEFECTS  # noqa: E402

C = "srp/srp_mbx.c"
# Reviewer-chosen plants, independent of the lane's mutant list.
OWN = {
    # F1: inherit the shared Applicant only from a binding with the same destination.
    "R-same-dest-only": (C, "if (memcmp(r->stream_id.bytes,identity->bytes,8) == 0) {",
                         "if (memcmp(r->stream_id.bytes,identity->bytes,8) == 0 && memcmp(r->dest_mac,dest_mac,6) == 0) {",
                         "JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves", "d.event"),
    # F1: inheritance keyed on VID instead of StreamID.
    "R-inherit-by-vid": (C, "if (memcmp(r->stream_id.bytes,identity->bytes,8) == 0) {",
                         "if (r->vid == vid) {",
                         "ReboundStreamCannotInheritAnotherStreamsReady", "ready"),
    # F1: one slot order only (inherit from lower-numbered slots).
    "R-lower-slot-only": (C, "including several accepted binds before the next service pass.\n"
                             "        for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {",
                          "including several accepted binds before the next service pass.\n"
                          "        for (unsigned k = 0; k < sink; ++k) {",
                          "JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves", "d.event"),
    # F1: the mirror order (inherit from higher-numbered slots only).
    "R-higher-slot-only": (C, "including several accepted binds before the next service pass.\n"
                              "        for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {",
                           "including several accepted binds before the next service pass.\n"
                           "        for (unsigned k = sink + 1u; k < CTRL_SRP_SINKS; ++k) {",
                           "JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves", "d.event"),
    # F2: guard hard-coded to the startup SR class VID instead of the current Domain.
    "R-guard-startup-vid": (C, "if (old.vid != i->domain.vid && !has_sink(i,&old,false))",
                            "if (old.vid != 2 && !has_sink(i,&old,false))",
                            "FinalDomainVidUnbindKeepsSrClassMembership", "d.event"),
    # F2: guard uses the pending Domain rather than the committed one.
    "R-guard-next-domain": (C, "if (old.vid != i->domain.vid && !has_sink(i,&old,false))",
                            "if (old.vid != i->next_domain.vid && !has_sink(i,&old,false))",
                            "FinalDomainVidUnbindKeepsSrClassMembership", "d.event"),
}
for d in DEFECTS:
    OWN.setdefault("L-" + d.name, (d.path, d.old, d.new, d.test, d.needle))


def run(src: Path, iface: int, suite: str, flt: str, debug: bool, out: Path):
    tree = Tree(src, out / "build", out / "reuse", fw_gtest.Build(jobs=2))
    return arm_srp(tree, LWSRP, iface, debug=debug, test=(suite, flt))


if MODE == "baseline":
    suite, iface = sys.argv[5], int(sys.argv[6])
    debug = len(sys.argv) > 7 and sys.argv[7] == "debug"
    out = OUT / f"base-{suite}-if{iface}{'-debug' if debug else ''}"
    r = run(CTRL, iface, suite, "*", debug, out)
    print(r.log)
    print(f"BASELINE {suite} IF={iface} debug={debug} rc={r.rc}")
elif MODE in ("plant", "plantnamed"):
    # plantnamed runs only the named test, as the lane campaign does; plant
    # runs the whole suite so collateral catches are visible too.
    name, iface = sys.argv[5], int(sys.argv[6])
    path, old, new, test, needle = OWN[name]
    out = OUT / f"plant-{name}-if{iface}"
    src = out / "ctrl"
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    text = (src / path).read_text()
    if text.count(old) != 1:
        print(f"PLANT {name} REFUSED: {text.count(old)} sites")
        sys.exit(2)
    (src / path).write_text(text.replace(old, new))
    try:
        r = run(src, iface, "srp_mbx.cpp", "Srp." + test if MODE == "plantnamed" else "*", False, out)
    except Refusal as e:
        print(f"PLANT {name} IF={iface} REFUSED (build): {e}")
        sys.exit(2)
    print(r.log)
    failed = sorted({ln.strip()[7:].split(":")[0] for ln in r.log.splitlines()
                     if ln.strip().startswith("[FAIL] Srp.")})
    named = caught("Srp." + test, needle, r)
    print(f"PLANT {name} IF={iface} rc={r.rc} named={'CAUGHT' if named else 'ESCAPED'} "
          f"test={test} needle={needle} failing={failed}")
else:
    sys.exit(f"unknown mode {MODE}")
