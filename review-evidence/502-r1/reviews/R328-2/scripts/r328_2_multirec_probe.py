#!/usr/bin/env python3
"""R328-2 probe: a two-record map command refused at its SECOND record.

Usage: r328_2_multirec_probe.py <tree> <outdir> [<milan_datapath.sv> <label>]

Derives tb/verilator/pp_shadow/r328_2_probe_main.cpp in the DISPOSABLE <tree>
from the head's sim_main.cpp (no reviewed file is edited), inserting the
probe before the final reset control, and runs the dynamic-output leg
(`make run-pending CPP=...`). An optional datapath copy replaces
hdl/milan/milan_datapath.sv in the source list only.

From a durable baseline:
  Q1 input: record 0 claims cluster key 0 (stream 0/ch 0); record 1 names the
     same key with a different channel, so validation refuses record 1
     (BAD_ARGUMENTS) after record 0's claim exists. Nothing is written.
  Q2 output: record 0 claims stream 0/ch 0 at cluster 0; record 1 names the
     same key with cluster 1, refused the same way.
Each must answer status 7, leave the map empty and leave pending clear.
This is the only reachable situation in which a claimed, changed key is
presented on a non-phase-5 beat (the abort, phase 3).
"""
import subprocess
import sys
from pathlib import Path

HOOK = '        pending_boot(7);\n        pending_report("K reset", 0, 0, 0);\n'

PROBE = r'''
    void r328_2_probe() {
        printf("[R328-2] two-record command refused at record 1 (reviewer-derived)\n");
        for (uint16_t type : {uint16_t{0x000e}, uint16_t{0x000f}}) {
            pending_boot(6);
            std::vector<uint8_t> map(24, 0);
            put16be(map.data(), type);
            put16be(map.data() + 4, 2);                 // two records
            // record 0: stream 0 / channel 0 / cluster 0 / cc 0 (all zero)
            if (type == 0x000e) put16be(map.data() + 18, 1);  // rec 1: channel 1, same cluster
            else                put16be(map.data() + 20, 1);  // rec 1: same stream/ch, cluster 1
            pending_command(0x002c, map, static_cast<uint16_t>(0x7000 + type), 7);
            pending_map_value(type, 0, static_cast<uint16_t>(0x7010 + type));
            printf("  [R328-2-obs] type 0x%x phase-5 records %u marks %u storage changes %u "
                   "PP_STAT[11] %u\n", type, pending.maps, pending.marks, pending.changes,
                   (axi_read(A_PP_STAT) >> 11) & 1u);
            pending_report(type == 0x000e ? "R328-2 Q1 input refused at record 1"
                                          : "R328-2 Q2 output refused at record 1", 0, 0, 0);
        }
    }
'''


def main():
    tree = Path(sys.argv[1]).resolve()
    outdir = Path(sys.argv[2]).resolve()
    dp = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
    label = sys.argv[4] if len(sys.argv) > 4 else "shipping"
    tb = tree / "tb/verilator/pp_shadow"
    src = (tb / "sim_main.cpp").read_text()
    anchor = "    void grade_pending_live_writes() {\n"
    if src.count(HOOK) != 1 or src.count(anchor) != 1:
        sys.exit("REFUSED: probe anchors changed")
    probe = src.replace(HOOK, "        r328_2_probe();\n" + HOOK).replace(anchor, PROBE + anchor)
    (tb / "r328_2_probe_main.cpp").write_text(probe)
    (outdir / "build").mkdir(parents=True, exist_ok=True)
    cmd = ["make", "run-pending", f"PENDING_BUILD_DIR={outdir / 'build' / label}",
           "CPP=r328_2_probe_main.cpp"]
    if dp is not None:
        listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"], cwd=tb,
                                 check=True, capture_output=True, text=True).stdout.split()
        ship = (tree / "hdl/milan/milan_datapath.sv").resolve()
        srcs = [(tb / p).resolve() for p in listing]
        assert srcs.count(ship) == 1
        cmd.append("DP_SRCS=" + " ".join(str(dp if p == ship else p) for p in srcs))
    log = outdir / f"probe.{label}.log"
    with log.open("w") as fh:
        rc = subprocess.run(cmd, cwd=tb, stdout=fh, stderr=subprocess.STDOUT).returncode
    text = log.read_text(errors="replace")
    for line in text.splitlines():
        if "R328-2" in line or "[FAIL]" in line or line.startswith(("pp_shadow:", "RESULT")):
            print(line)
    print(f"{label}: rc={rc}")


if __name__ == "__main__":
    main()
