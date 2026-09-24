#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer fault/mutation probes for processor PR #115 (issue #113).

Each variant is extracted fresh from the exact reviewed commit with
`git archive`, edited in a disposable tree, built with the GI bench target
(`make gsi-build`) and run with `--gsi-internal-only`. Nothing in the source
checkout is modified. One JSON line per variant is appended to
<out>/probes.jsonl; build and run transcripts are kept alongside.

Usage:
  r310_probes.py --repo <clone> --commit <sha> --work <scratch> --out <dir>
                 --verilator <path> [--cpus 0-7] VARIANT [VARIANT ...]
"""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

TOP = "hdl/top/protocol_processor_top.sv"
SRP = "hdl/srp/KL_srp_listener_fsm.sv"
GI = "tb/pp_top/gsi_internal.hpp"
CMP = "evt_tk_latency_chg_o[s] <= (lat_r[s] != evt_acc_latency_i);"

# Reviewer test additions: single-bit transitions at both ends of the word,
# explicit same-write coalescing with a FailureInformation change and with an
# Advertise<->Failed swap, and a wire check that a latency-only change does
# not re-declare the Listener attribute.
GI_ANCHOR = "    io.gsi_fold_latency = false;\n  }\n"
GI_EXTRA = r'''    // ---- R310 probe additions (not part of the reviewed head) ----
    latency_refresh(0, 0x80000000, 0xFFFFFFFF, true);   // bit 31 only
    latency_refresh(1, 0x7FFFFFFF, 0x80000000, true);   // bit 31 only
    latency_refresh(0, 0x80000001, 0x7FFFFFFF, true);   // bit 0 only
    latency_refresh(1, 0x7FFF7FFF, 0x80000001, true);   // bit 15 only
    r310_coalesce(1, 23, BRIDGE1 ^ 0x00FF, true, 0x00C0FFEE,
                  "R310 COALESCE-FAIL+LAT");
    r310_coalesce(1, 11, BRIDGE1, true, 0x7FFF7FFF,
                  "R310 COALESCE-FAIL-RESTORE");
    r310_coalesce(0, 7, BRIDGE0, true, 0x01020304,
                  "R310 COALESCE-SWAP-TO-FAILED+LAT");
    r310_coalesce(0, 0, 0, false, 0x05060708,
                  "R310 COALESCE-SWAP-TO-ADV+LAT");
    io.q_msrp.clear();
    attribute(0, 0, 0, false, EV_JOININ, 0x0A0B0C0D);
    CHECK(listener_news(0, 600) == 0,
          "R310 LATENCY wire: a latency-only change sends no Listener New");
    {
      const auto uns = input_uns(0, 0);
      CHECK(uns.size() == 1, "R310 LATENCY wire: exactly one unsolicited, got %zu",
            uns.size());
      if (!uns.empty())
        check_frame(uns[0], "R310 LATENCY-WIRE", 0, 3, 0, 0, 0, true, true,
                    false, 0x0A0B0C0D);
    }
    CHECK(input_uns(1, 50).empty() && io.q_aecp.empty(),
          "R310 LATENCY wire: nothing else pushed");
'''
GI_HELPER_ANCHOR = "  void latency_changes() {\n"
GI_HELPER = r'''  void r310_coalesce(unsigned sink, uint8_t code, uint64_t bridge,
                     bool failed, uint32_t latency, const char* tag) {
    attribute(sink, code, bridge, failed, EV_JOININ, latency);
    const auto uns = input_uns(sink, 100);
    CHECK(uns.size() == 1, "%s: exactly one unsolicited response, got %zu",
          tag, uns.size());
    const auto pushed = uns.empty() ? std::vector<uint8_t>{} : uns[0];
    check_frame(pushed, tag, sink, 3, 0, code, bridge, true, true, false,
                latency);
    check_frame(query(sink), tag, sink, 3, 0, code, bridge, false, true,
                false, latency);
    CHECK(input_uns(sink ^ 1, 100).empty() && io.q_aecp.empty(),
          "%s: no other or duplicate response", tag);
  }

'''

VARIANTS = {
    # name: (list of (file, old, new, count), expected FAIL prefix or "" for PASS,
    #        apply reviewer test additions?)
    "golden": ([], "", False),
    "golden-plus": ([], "", True),
    "trigger-removed": ([(TOP, " || srp_evt_tk_latency_chg_w[k]", "", 1)],
                        "GI LATENCY-CHANGE: exactly one unsolicited response", False),
    "always-pulse": ([(SRP, CMP, "evt_tk_latency_chg_o[s] <= 1'b1;", 1)],
                     "GI LATENCY-SAME: unchanged refresh sends no response", False),
    "wrong-sink": ([(TOP, "|| srp_evt_tk_latency_chg_w[k];",
                     "|| srp_evt_tk_latency_chg_w[k ^ 1];", 1)],
                   "GI LATENCY-CHANGE: exactly one unsolicited response", False),
    "broadcast": ([(TOP, "|| srp_evt_tk_latency_chg_w[k];",
                    "|| (|srp_evt_tk_latency_chg_w);", 1)],
                  "GI LATENCY-OTHER", False),
    "cmp-low3": ([(SRP, CMP, "evt_tk_latency_chg_o[s] <= "
                   "(lat_r[s][2:0] != evt_acc_latency_i[2:0]);", 1)], None, False),
    "cmp-high2": ([(SRP, CMP, "evt_tk_latency_chg_o[s] <= "
                    "(lat_r[s][31:30] != evt_acc_latency_i[31:30]);", 1)], None, False),
    "cmp-no-bit31": ([(SRP, CMP, "evt_tk_latency_chg_o[s] <= "
                       "(lat_r[s][30:0] != evt_acc_latency_i[30:0]);", 1)], None, False),
    "cmp-low3-plus": ([(SRP, CMP, "evt_tk_latency_chg_o[s] <= "
                        "(lat_r[s][2:0] != evt_acc_latency_i[2:0]);", 1)],
                      "GI LATENCY-CHANGE: exactly one unsolicited response", True),
    "cmp-high2-plus": ([(SRP, CMP, "evt_tk_latency_chg_o[s] <= "
                         "(lat_r[s][31:30] != evt_acc_latency_i[31:30]);", 1)],
                       "GI LATENCY-CHANGE: exactly one unsolicited response", True),
    "cmp-no-bit31-plus": ([(SRP, CMP, "evt_tk_latency_chg_o[s] <= "
                            "(lat_r[s][30:0] != evt_acc_latency_i[30:0]);", 1)],
                          "GI LATENCY-CHANGE: exactly one unsolicited response", True),
    "cmp-low16": ([(SRP, CMP, "evt_tk_latency_chg_o[s] <= "
                    "(lat_r[s][15:0] != evt_acc_latency_i[15:0]);", 1)], None, False),
    "cmp-low16-plus": ([(SRP, CMP, "evt_tk_latency_chg_o[s] <= "
                         "(lat_r[s][15:0] != evt_acc_latency_i[15:0]);", 1)],
                       "GI LATENCY-CHANGE: exactly one unsolicited response", True),
}


def sh(cmd, cwd, log, cpus):
    with open(log, "w") as stream:
        return subprocess.run(["taskset", "-c", cpus] + cmd, cwd=cwd, stdout=stream,
                              stderr=subprocess.STDOUT, check=False,
                              timeout=1500).returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--cpus", default="0-7")
    ap.add_argument("variants", nargs="+")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(["git", "-C", str(a.repo), "rev-parse", a.commit + "^{commit}"],
                          capture_output=True, text=True, check=True).stdout.strip()
    for name in a.variants:
        edits, expected, plus = VARIANTS[name]
        tree = a.work / name
        if tree.exists():
            shutil.rmtree(tree)
        tree.mkdir(parents=True)
        arc = subprocess.run(["git", "-C", str(a.repo), "archive", head, "hdl",
                              "tb/common", "tb/pp_top"], capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", str(tree)], input=arc.stdout, check=True)
        for fname, old, new, count in edits:
            p = tree / fname
            text = p.read_text()
            if text.count(old) != count:
                raise SystemExit(f"{name}: {fname} has {text.count(old)} sites, want {count}")
            p.write_text(text.replace(old, new))
        if plus:
            p = tree / GI
            text = p.read_text()
            assert text.count(GI_ANCHOR) == 1 and text.count(GI_HELPER_ANCHOR) == 1
            text = text.replace(GI_ANCHOR, GI_EXTRA + GI_ANCHOR)
            text = text.replace(GI_HELPER_ANCHOR, GI_HELPER + GI_HELPER_ANCHOR)
            p.write_text(text)
        bench = tree / "tb/pp_top"
        brc = sh(["make", "gsi-build", "VERILATOR=" + a.verilator], bench,
                 a.out / f"{name}-build.log", a.cpus)
        rrc = None
        fails, tally = [], ""
        if brc == 0:
            rlog = a.out / f"{name}-run.log"
            rrc = sh(["./obj_dir/Vpp_top_sim", "--gsi-internal-only"], bench, rlog, a.cpus)
            lines = rlog.read_text(errors="replace").splitlines()
            fails = [l for l in lines if l.startswith("FAIL: ")]
            tally = next((l for l in lines if l.startswith("[build default,")), "")
        if expected is None:
            verdict = "SURVIVES" if (rrc == 0 and not fails and tally) else "KILLED"
        elif expected == "":
            verdict = "PASS" if (rrc == 0 and not fails and tally) else "UNEXPECTED"
        else:
            named = [l for l in fails if l.startswith("FAIL: " + expected)]
            verdict = "KILLED-BY-NAMED" if (brc == 0 and tally and named) else "UNEXPECTED"
        rec = {"variant": name, "commit": head, "edits": [e[:3] for e in edits],
               "reviewer_test_additions": plus, "build_rc": brc, "run_rc": rrc,
               "tally": tally, "n_fail_lines": len(fails), "first_fails": fails[:6],
               "expected": expected, "verdict": verdict}
        with open(a.out / "probes.jsonl", "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)
        shutil.rmtree(tree / "tb/pp_top/obj_dir", ignore_errors=True)


if __name__ == "__main__":
    main()
