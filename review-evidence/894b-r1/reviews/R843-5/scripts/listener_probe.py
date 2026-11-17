#!/usr/bin/env python3
"""Reviewer probe for SRP's Listener copies (#930) at an exact head.

usage: listener_probe.py CLONE OUT MODE [JOBS [NAME]]
  MODE arms        run srp_listeners.cpp at 1x1/1if and 8x8/1if (srp_arms.listener_arms), unmodified
  MODE plants-1x1  plant the reviewer's own extra defects (EXTRA) at 1x1/1if, one interface
  MODE plants-8x8  plant them at 8x8/1if, one interface

Each defect is a one-site edit of srp/srp_mbx.c in a disposable copy under OUT (srp_mutants.campaign copies
sw/firmware/ctrl); none touches the clone. A defect is caught only when the named differential test fails with its
own diagnostic words (srp_mutants.caught). The defects marked equivalent are expected to escape: they change no
behaviour the adapter can show, and are planted to state that, not to hold the test to them.
"""
import sys
from pathlib import Path

clone, out, mode = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))

import srp_mutants  # noqa: E402
import srp_arms  # noqa: E402
import srp_listener_mutants as L  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402

LWSRP = clone / "third_party/lwSRP"
TEST, NEEDLE = L.TEST, L.NEEDLE
DISPATCH = L.DISPATCH
PRESENCE = L.PRESENCE
LEFT = "        listener(ctx,port,value,MSRP_LISTENER_DECL_IGNORE,false);\n"


def d(name, old, new, equivalent=False):
    return (srp_mutants.Defect("reviewer-" + name, TEST, old, new, NEEDLE, suite=L.SUITE), equivalent)


EXTRA = (
    # the observer copies a Talker's Registrar change as a Listener's presence when its StreamID is a source's
    d("dispatch-any-type", DISPATCH, DISPATCH.replace("t->attr_type == MSRP_ATTR_TYPE_LISTENER && ", "")),
    # MVRP's slot: its attribute type 1 is never MSRP's Listener type 3, so the slot test changes nothing
    d("dispatch-any-slot", DISPATCH, DISPATCH.replace("slot == 0u && ", ""), equivalent=True),
    # every Listener Registrar change counted as presence, a departure into MT too
    d("presence-always", PRESENCE, PRESENCE.replace("t->reg_to != MRP_REG_STATE_MT", "true")),
    # only departures copied: an arrival leaves presence to the next walk
    d("arrival-dropped", DISPATCH, DISPATCH.replace("t->reg_from != t->reg_to", "t->reg_to == MRP_REG_STATE_MT")),
    # a Listener's Leave indication no longer copies its declaration
    d("leave-not-copied", LEFT, "        (void)ctx; (void)port; (void)value;\n"),
    # Ready Failed copied as not ready by the indication alone (the walk still counts it)
    d("indication-readyfailed-dropped",
      "                               declaration == MSRP_LISTENER_DECL_READY_FAILED;\n",
      "                               false;\n"),
    # the walk's own copy of what a Listener registers (registrations), which round 12's retarget left unplanted:
    # Asking Failed counted as ready, and Ready Failed as not ready, at the walk alone
    d("walk-asking-is-ready", "i->registered[n] = v[8] == 2 || v[8] == 3;",
      "i->registered[n] = v[8] == 1 || v[8] == 2 || v[8] == 3;"),
    d("walk-readyfailed-ignored", "i->registered[n] = v[8] == 2 || v[8] == 3;", "i->registered[n] = v[8] == 2;"),
)


def main():
    out.mkdir(parents=True, exist_ok=True)
    if mode == "arms":
        tree = Tree(CTRL, out / "build", out / "reuse", fw_gtest.Build(jobs=jobs))
        bad = 0
        for o in srp_arms.listener_arms(tree, LWSRP):
            name = o.arm
            print(f"[arm] {name}: rc={o.rc}", flush=True)
            (out / (str(name).replace('/', '_') + ".log")).write_text(o.log)
            tail = [x for x in o.log.splitlines() if "PASS" in x or "FAIL" in x or "tests" in x.lower()][-6:]
            print("\n".join("    " + x for x in tail), flush=True)
            bad |= o.rc != 0
        print("RESULT:", "FAIL" if bad else "PASS", flush=True)
        return 1 if bad else 0
    entity = {"plants-1x1": "", "plants-8x8": L.ENTITY}[mode]
    verdicts = []
    only = sys.argv[5] if len(sys.argv) > 5 else ""
    for defect, equivalent in EXTRA:
        if only and defect.name != "reviewer-" + only:
            continue
        srp_mutants.DEFECTS = (defect,)
        escaped = srp_mutants.campaign(out / defect.name, LWSRP, jobs, 1, entity)
        expect = "escape (equivalent)" if equivalent else "caught"
        got = "escaped" if escaped else "caught"
        ok = (got == "escaped") == equivalent
        verdicts.append(ok)
        print(f"[{'as-expected' if ok else 'UNEXPECTED'}] {defect.name} at {mode}: {got}, expected {expect}",
              flush=True)
    print("RESULT:", "PASS" if all(verdicts) else "FAIL", flush=True)
    return 0 if all(verdicts) else 1


if __name__ == "__main__":
    sys.exit(main())
