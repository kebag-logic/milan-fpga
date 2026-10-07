#!/usr/bin/env python3
"""R532-8 reviewer probe: plant one defect into a scratch copy of the exact-head
control tree and run the SRP-composition suites that compile it.

usage: probe_mutants.py REPO LWSRP WORK NAME
REPO is an exported copy of the head (its test helpers are imported from it),
LWSRP the pinned lwSRP checkout, WORK a disposable directory. Prints one line
per suite and interface count; exit 0 = every run passed (the plant ESCAPED),
1 = at least one run failed (the plant was CAUGHT), 2 = refusal.
"""
import shutil, sys
sys.dont_write_bytecode = True
from pathlib import Path

PLANTS = {
    # The new SRP pass bound's terms (srp/srp_bounds.h, new in the merge), understated.
    "srp-poll-drops-tx": ("srp/srp_bounds.h", "(MBX_N_IF * (4u + 2u * SRP_MBX_TX_MAX))",
                          "(MBX_N_IF * (4u + 0u * SRP_MBX_TX_MAX))"),
    "srp-pass-drops-rx-and-poll": ("srp/srp_bounds.h",
                                   "CTRL_LOOP_RX_PER_PASS * (SRP_MBX_RX_RECORD_MAX + SRP_MBX_RX_MAX) + SRP_MBX_POLL_MAX)",
                                   "0u)"),
    "srp-rx-max-zero": ("srp/srp_bounds.h", "#define SRP_MBX_RX_MAX 2u", "#define SRP_MBX_RX_MAX 0u"),
    "srp-event-max-zero": ("srp/srp_bounds.h", "#define SRP_MBX_EVENT_MAX 1u", "#define SRP_MBX_EVENT_MAX 0u"),
    # The attach's conditional ACMP bit and tick enable.
    "attach-acmp-always": ("app/ctrl_app_srp.c", "if (app->loop.rx[MBX_CH_ACMP].fn) {", "if (1) {"),
    "attach-no-tick": ("app/ctrl_app_srp.c", "mbx_tick_enable(true);", "mbx_tick_enable(false);"),
    # Control: the unmodified tree must pass every suite.
    "control-none": ("app/ctrl_app_srp.c", "", ""),
}
SUITES = ("test_acmp_mbx.cpp", "srp_app.cpp")


def main() -> int:
    repo, lwsrp, work, name = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
    sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
    import fw_gtest
    from ctrl_build import Tree, Refusal
    from srp_arms import arm_srp
    path, old, new = PLANTS[name]
    src = work / "ctrl"
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(repo / "sw/firmware/ctrl", src)
    target = src / path
    text = target.read_text()
    if old:
        if text.count(old) != 1:
            print(f"REFUSED {name}: {text.count(old)} planting sites"); return 2
        target.write_text(text.replace(old, new))
    failed = False
    build = fw_gtest.Build(jobs=4)
    for suite in SUITES:
        for interfaces in (1, 2):
            try:
                result = arm_srp(Tree(src, work / "build", work / "reuse", build), lwsrp, interfaces, test=suite)
            except Refusal as error:
                print(f"{name} {suite} IF={interfaces}: REFUSED (build) {str(error)[:300]}"); failed = True; continue
            first = next((l.strip() for l in result.log.splitlines() if "[FAIL]" in l or "Failure" in l), "")
            print(f"{name} {suite} IF={interfaces}: {'FAIL' if result.rc else 'pass'} {first[:200]}")
            failed |= bool(result.rc)
    print(f"{name}: {'CAUGHT' if failed else 'ESCAPED'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
