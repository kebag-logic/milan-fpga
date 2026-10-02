#!/usr/bin/env python3
"""R420-2 reviewer probes for PR #139 (lane C6) at 88e0bf82: disposable, never committed.

Each probe copies hdl/, tb/common/ and tb/pp_top/ of an exported head tree into a
private directory, applies exact-once text edits (an RTL defect and/or one extra
reviewer bench function appended to section ID), builds the third pp_top build
(EN_IDENTIFY_NOTIF_P = 1) and runs it. The verdict lists the FAIL lines and the
[P]/[i] information lines. The exported tree is never modified.

Usage: python3 r420_probes.py --head DIR --work DIR --out DIR [--only NAME ...]
"""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

NTFY = "hdl/aecp/KL_aecp_notify.sv"
BENCH = "tb/pp_top/notify_phases.hpp"

# one extra function in IdentifyPhase, called last in section ID's run()
PROBE_FN = r'''
  //! R420-2 reviewer probe (not part of the suite)
  void r420_probe() {
    // RP1: a short press, then a second press 50 ms after the burst's third
    // frame left, held 300 ms (the WAITING path, not the in-burst latch)
    size_t from = seen.size();
    press(true);
    wait_idents(from, 1);
    press(false);
    wait_idents(from, 3);
    const auto v3 = idents(from);
    if (v3.size() == 3) {
      const uint64_t t3 = v3[2].t;
      while (io.t < t3 + uint64_t(50L * MS_CYC)) tick();
      press(true);
      run_ms(300);
      press(false);
      run_ms(1500);
      const auto v = idents(from);
      printf("  [P] RP1: frames %zu", v.size());
      if (v.size() >= 4) printf(", third->fourth %ld clocks", long(v[3].t - v[2].t));
      printf("\n");
      CHECK(v.size() == 6, "RP1a: a second press 50 ms after a burst sends a "
            "second burst (%zu frames)", v.size());
      if (v.size() >= 4)
        CHECK(long(v[3].t - v[2].t) >= BURST, "RP1b: the second burst starts at "
              "least T-IDENT-BURST after the third frame (%ld clocks)",
              long(v[3].t - v[2].t));
    }
    // RP2: an 80 ms press that starts 20 ms after a burst's third frame left
    run_ms(1200);
    from = seen.size();
    press(true);
    wait_idents(from, 1);
    press(false);
    wait_idents(from, 3);
    const auto w3 = idents(from);
    if (w3.size() == 3) {
      const uint64_t t3 = w3[2].t;
      while (io.t < t3 + uint64_t(20L * MS_CYC)) tick();
      press(true);
      run_ms(80);
      press(false);
      run_ms(1500);
      printf("  [P] RP2: an 80 ms press 20 ms after the third frame left: %zu "
             "frames after it\n", idents(from).size() - 3);
    }
  }
'''
RUN_OLD = "    a_tx_stall_mid_burst_never_bunches_it();\n  }\n};\n"
RUN_NEW = "    a_tx_stall_mid_burst_never_bunches_it();\n    r420_probe();\n  }\n};\n"
FN_ANCHOR = "  void a_tx_stall_mid_burst_never_bunches_it() {\n"
WITH_PROBE = ((BENCH, FN_ANCHOR, PROBE_FN + FN_ANCHOR), (BENCH, RUN_OLD, RUN_NEW))


SWEEP_FN = r"""
  //! R420-2 reviewer sweeps (not part of the suite): the R420-1 / R421-1 shapes
  void r420_sweeps() {
    // RS1: the MAC stalled right after frame 1 or frame 2, for several lengths
    static constexpr long STALLS[] = {100, 200, 250, 320, 400};
    long rs1_min = 1L << 40;
    int rs1_bursts = 0;
    for (int after = 1; after <= 2; ++after) {
      for (const long ms : STALLS) {
        const size_t from = seen.size();
        press(true);
        wait_idents(from, 1);
        press(false);
        if (after == 2) wait_idents(from, 2);
        stall_mac(ms);
        run_ms(1500);
        const auto v = idents(from);
        if (v.size() != 3) { printf("  [P] RS1: after frame %d, %ld ms: %zu frames\n", after, ms, v.size()); continue; }
        ++rs1_bursts;
        printf("  [P] RS1: stall %ld ms after frame %d: gaps %ld and %ld\n", ms, after, gap_of(v, 0), gap_of(v, 1));
        rs1_min = std::min({rs1_min, gap_of(v, 0), gap_of(v, 1)});
      }
    }
    CHECK(rs1_bursts == 10, "RS1a: ten stalled presses, ten bursts of three (%d)", rs1_bursts);
    CHECK(rs1_min >= BURST, "RS1b: no gap under T-IDENT-BURST across the stall sweep (min %ld)", rs1_min);
    // RS2: a 15-row SET_NAME fan-out fed across frame 2's deadline, 31 offsets
    int ok = 0;
    for (unsigned k = 0; k < 15; ++k)
      ok += register_controller(FAN_MAC + k, FAN_EID + k, uint16_t(0x7B00 + k)) ? 1 : 0;
    CHECK(ok == 15, "RS2: fifteen controllers registered (%d)", ok);
    long rs2_min = 1L << 40;
    long rs2_max12 = 0;
    int rs2_bursts = 0;
    for (int i = 0; i <= 30; ++i) {
      const long off = BURST - 1500 + 50L * i;
      char text[32];
      snprintf(text, sizeof text, "Sweep %d", i);
      const auto body = clock_domain_name(text);
      const size_t from = seen.size();
      press(true);
      wait_idents(from, 1);
      press(false);
      if (idents(from).empty()) break;
      const uint64_t t1 = idents(from)[0].t;
      while (io.t < t1 + uint64_t(off)) tick();
      feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, uint16_t(0x7C00 + i),
                      AEM_SET_NAME, body));
      run_ms(1500);
      const auto v = idents(from);
      if (v.size() != 3) continue;
      ++rs2_bursts;
      rs2_min = std::min({rs2_min, gap_of(v, 0), gap_of(v, 1)});
      rs2_max12 = std::max(rs2_max12, gap_of(v, 0));
    }
    printf("  [P] RS2: %d bursts; smallest gap %ld, largest 1->2 %ld clocks\n", rs2_bursts, rs2_min, rs2_max12);
    CHECK(rs2_bursts == 31, "RS2a: 31 bursts of three (%d)", rs2_bursts);
    CHECK(rs2_min >= BURST, "RS2b: no gap under T-IDENT-BURST across the fan-out sweep (min %ld)", rs2_min);
    CHECK(rs2_max12 > BURST + SLACK, "RS2c: the sweep did delay frame 2 (largest 1->2 %ld)", rs2_max12);
  }
"""
RUN_NEW_SWEEP = "    a_tx_stall_mid_burst_never_bunches_it();\n    r420_sweeps();\n  }\n};\n"
WITH_SWEEPS = ((BENCH, FN_ANCHOR, SWEEP_FN + FN_ANCHOR), (BENCH, RUN_OLD, RUN_NEW_SWEEP))

WAIT_OLD = "          I_WAIT: if (btn_q2_r && !gap_r) begin\n"
HOLD_OLD = "            end else if ((rel_r || fired_r || exp_r_w) && !gap_r) begin\n"
DL_OLD = "    assign id_arm_deadline_w = armb_r ? now_ms_i + 32'(IDENT_BURST_MS_C + 1)\n"

PROBES = {
    # the head itself with the reviewer bench function
    "head_with_probe": WITH_PROBE,
    # the head with the R420-1 / R421-1 shaped sweeps
    "head_with_sweeps": WITH_SWEEPS,
    # the WAITING start alone ignores the running gap (HOLD keeps it)
    "wait_ignores_gap": ((NTFY, WAIT_OLD, "          I_WAIT: if (btn_q2_r) begin\n"),),
    "wait_ignores_gap_with_probe": ((NTFY, WAIT_OLD, "          I_WAIT: if (btn_q2_r) begin\n"),)
                                   + WITH_PROBE,
    # the HOLD start alone ignores the running gap (WAITING keeps it)
    "hold_ignores_gap": ((NTFY, HOLD_OLD,
                          "            end else if (rel_r || fired_r || exp_r_w) begin\n"),),
    # the BURST deadline one tick short: due at the 150th boundary, not the 151st
    "burst_deadline_one_tick_short": ((NTFY, DL_OLD,
                                       "    assign id_arm_deadline_w = armb_r ? now_ms_i + "
                                       "32'(IDENT_BURST_MS_C)\n"),),
}

TALLY = re.compile(r"\[build identify[^\]]*\] (\d+) checks, (\d+) failures")


def plant(tree: Path, edits) -> str:
    for rel, old, new in edits:
        path = tree / rel
        text = path.read_text()
        if text.count(old) != 1:
            return f"{rel}: anchor occurs {text.count(old)} times"
        path.write_text(text.replace(old, new, 1))
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--head", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--verilator", default="verilator")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    head, work, out = Path(a.head), Path(a.work), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, edits in PROBES.items():
        if a.only and name not in a.only:
            continue
        tree = work / name
        shutil.rmtree(tree, ignore_errors=True)
        skip = shutil.ignore_patterns("obj*", "*.hex", "__pycache__")
        for d in ("hdl", "tb/common", "tb/pp_top"):
            shutil.copytree(head / d, tree / d, ignore=skip)
        refusal = plant(tree, edits)
        log = out / f"{name}.log"
        if refusal:
            rows.append({"probe": name, "verdict": "REFUSED", "reason": refusal})
            continue
        with log.open("w") as s:
            b = subprocess.run(["make", "identify-build", "VERILATOR=" + a.verilator],
                               cwd=tree / "tb/pp_top", stdout=s, stderr=subprocess.STDOUT).returncode
            r = subprocess.run(["./obj_idn/Vpp_top_idn"], cwd=tree / "tb/pp_top", stdout=s,
                               stderr=subprocess.STDOUT).returncode if b == 0 else None
        text = log.read_text(errors="replace")
        m = TALLY.search(text)
        fails = [ln[6:] for ln in text.splitlines() if ln.startswith("FAIL: ")]
        info = [ln.strip() for ln in text.splitlines() if "[P]" in ln]
        rows.append({"probe": name, "build_rc": b, "run_rc": r,
                     "tally": m.group(0) if m else None, "failing_checks": fails, "probe_info": info})
        print(json.dumps(rows[-1]))
        shutil.rmtree(tree, ignore_errors=True)
    (out / "probes.json").write_text(json.dumps(rows, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
