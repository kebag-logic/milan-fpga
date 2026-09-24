#!/usr/bin/env python3
"""Reviewer probes on the obj_crflic leg (disposable; never committed).

Each variant copies the head leg source, applies one text patch, builds it
through the suite's own `make crflic-build` recipe in a scratch COPY of the
clone and runs it. Usage:

  python3 probe_variants.py <scratch-copy-of-clone> <receipts-dir> <variant>...

Variants:
  fixedla10000  the switch sends its own LeaveAll on a FIXED 10.0 s period
                from boot, independent of the DUT's LeaveAll (the PR's
                unmodelled switch); expect every [C] check to hold.
  fixedla12500  the same at 12.5 s.
  fixedla3300   a fast 3.3 s switch LeaveAll period, sweeping its phase
                against the DUT's 10-15 s timer.
  earlyready    the switch declares Listener Ready for the CRF stream at the
                start of [A], before the DUT declares: exercises the stated
                optimistic-window corner and prints how many cycles ACTIVE
                leads the raw admission verdict. [A] checks are EXPECTED to
                fail in this variant (a Listener Ready exists).
Needs VERILATOR in the environment; VERILATOR_JOBS is forced to 8.
"""
import os
import subprocess
import sys
from pathlib import Path

LEG = "tb/verilator/milan_dp/sim_crf_licence.cpp"

SWITCH_TIMER = (
    "    const uint64_t gen = ++bridge_la_gen;\n"
    "    at(cyc + ms(9990), [this, gen] { bridge_send_leave_all(gen); });\n")
BOOT_CALL = "    boot();\n    const uint64_t t0 = phase_a();\n"
REPORT = "    grade_invariants();\n"


def fixed(period_ms: int):
    def patch(src: str) -> str:
        assert src.count(SWITCH_TIMER) == 1 and src.count(BOOT_CALL) == 1
        src = src.replace(SWITCH_TIMER, "")
        sched = (f"    for (int k = 1; k <= 60; k++)\n"
                 f"        at(cyc + ms({period_ms}ull * static_cast<uint64_t>(k)),"
                 f" [this] {{ bridge_send_leave_all(bridge_la_gen); }});\n")
        return src.replace(BOOT_CALL, "    boot();\n" + sched
                           + "    const uint64_t t0 = phase_a();\n")
    return patch


def early_ready(src: str) -> str:
    anchor = "    probe(kUidCrf);\n    probe(kUidAaf);\n    run_until(t0 + ms(3900));\n"
    assert src.count(anchor) == 1 and src.count(REPORT) == 1
    src = src.replace(anchor, "    bridge_declare(kUidCrf, 0, 2);\n" + anchor)
    extra = (
        "    {\n"
        "        const uint64_t a = active[kUidCrf].first_rise;\n"
        "        const uint64_t r = admitted[kUidCrf].first_rise;\n"
        "        const uint64_t p = crf_pdus.empty() ? kNever : crf_pdus.front().cyc;\n"
        "        long before = 0;\n"
        "        for (const StreamPdu& q : crf_pdus) if (q.cyc < r) before++;\n"
        "        printf(\"[PROBE] earlyready: ACTIVE first rise cyc %llu, raw admitted first rise cyc %llu,\"\n"
        "               \" lead %lld cycles; licence first rise %llu; first CRF PDU cyc %llu;\"\n"
        "               \" PDUs before raw admission %ld\\n\",\n"
        "               (unsigned long long)a, (unsigned long long)r,\n"
        "               (long long)r - (long long)a, (unsigned long long)licence.first_rise,\n"
        "               (unsigned long long)p, before);\n"
        "    }\n")
    return src.replace(REPORT, REPORT + extra)


VARIANTS = {
    "fixedla10000": fixed(10000),
    "fixedla12500": fixed(12500),
    "fixedla3300": fixed(3300),
    "earlyready": early_ready,
}


def main() -> int:
    copy, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, VERILATOR_JOBS="8")
    leg = copy / LEG
    pristine = (copy / LEG).with_suffix(".cpp.pristine")
    if not pristine.exists():
        pristine.write_bytes(leg.read_bytes())
    base = pristine.read_text()
    rc_all = 0
    for name in sys.argv[3:]:
        leg.write_text(VARIANTS[name](base))
        mdir = f"obj_probe_{name}"
        b = subprocess.run(["make", "-s", "-C", str(copy / "tb/verilator/milan_dp"),
                            "crflic-build", f"CRFLIC_MDIR={mdir}"],
                           env=env, capture_output=True, text=True, check=False)
        log = out / f"probe_{name}.log"
        if b.returncode != 0:
            log.write_text(b.stdout + b.stderr + f"\nBUILD rc={b.returncode}\n")
            rc_all = 1
            continue
        r = subprocess.run([str(copy / "tb/verilator/milan_dp" / mdir / "Vmilan_dp_crflic")],
                           cwd=str(copy / "tb/verilator/milan_dp"),
                           capture_output=True, text=True, check=False)
        log.write_text(r.stdout + r.stderr + f"\nrc={r.returncode}\n")
    leg.write_bytes(pristine.read_bytes())
    return rc_all


if __name__ == "__main__":
    sys.exit(main())
