#!/usr/bin/env python3
"""Reviewer-planted defects on the cuts of PR #939 (issue #927), none of which
the PR's own campaigns plant. Each plant edits a copy of one tracked source
(read from the tree's HEAD, so a probed working tree is not picked up), builds
the named suite with that copy through the suite's own override variable, and
records whether the suite fails. A plant that changes nothing visible is
reported ESCAPED, never hidden.

usage: reviewer_plants.py <tree-root> <work-dir> <plant-name|all>
"""
import subprocess
import sys
from pathlib import Path

METER = "hdl/ieee1722/crf/KL_aaf_clock_meter.sv"
DMA = "hdl/milan/mailbox/KL_mbx_dma.sv"
DP = "hdl/milan/milan_datapath.sv"

PLANTS = {
    # the group-end PDU-0 timestamp one PDU early: the new subtraction's constant
    "meter-pc-ts0-one-pdu-off": (METER, "          pc_ts0_r  <= grp_ref_r - 32'(GRP_LAST_NS_C);\n",
                                 "          pc_ts0_r  <= grp_ref_r - 32'(GRP_NS_C);\n", "meter"),
    # the group-end PDU-0 timestamp taken as the reference itself, no subtraction
    "meter-pc-ts0-unsubtracted": (METER, "          pc_ts0_r  <= grp_ref_r - 32'(GRP_LAST_NS_C);\n",
                                  "          pc_ts0_r  <= grp_ref_r;\n", "meter"),
    # the start's load of the ring address omitted: a move starts at the last move's word
    "dma-ring-addr-not-loaded-at-start": (DMA, "              ring_addr_r <= ring_word(ring_base_i, ring_mask_i, ring_index_i);\n",
                                          "", "dma"),
    # the ring address not advanced on the transmit (to-ring) branch alone
    "dma-ring-addr-stuck-to-ring": (DMA, "          if (hold_r) begin\n            index_r     <= index_r + 16'd1;\n"
                                    "            ring_addr_r <= ring_addr_next_w;\n          end\n",
                                    "          if (hold_r) begin\n            index_r     <= index_r + 16'd1;\n"
                                    "          end\n", "dma"),
    # the all-fabric build given the split's registered encode: its map restore
    # changes the record while req stays high
    "dp-allfabric-encode-registered": (DP, "    assign amap_edit_out_enc_w = amap_edit_out_encode(amap_edit_co_w,\n"
                                       "                                                      pp_amap_edit_desc_index_w);\n",
                                       "    logic [13:0] af_enc_q;\n"
                                       "    always_ff @(posedge axis_clk) af_enc_q <= amap_edit_out_encode(amap_edit_co_w,\n"
                                       "                                                      pp_amap_edit_desc_index_w);\n"
                                       "    assign amap_edit_out_enc_w = af_enc_q;\n", "maprec8+dynmap"),
}


def sh(cmd, cwd, log):
    log.write(f"$ {' '.join(map(str, cmd))}\n")
    log.flush()
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log.write(r.stdout[-20000:])
    log.write(f"\n# rc={r.returncode}\n")
    log.flush()
    return r.returncode, r.stdout


def plant(root: Path, work: Path, name: str) -> str:
    rel, old, new, suite = PLANTS[name]
    text = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{rel}"], check=True,
                          capture_output=True, text=True).stdout
    if text.count(old) != 1:
        return f"FIXTURE {name}: anchor found {text.count(old)} times"
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    copy = d / Path(rel).name
    copy.write_text(text.replace(old, new))
    verdicts = []
    with open(d / "plant.log", "w") as log:
        if suite == "meter":
            tb = root / "tb/verilator/aaf_clock_meter"
            rc, _ = sh(["make", "-s", "-C", str(tb), "build", f"METER_RTL={copy}", f"MDIR={d / 'obj'}"], tb, log)
            if rc:
                return f"BUILD {name}"
            rc1, o1 = sh([str(d / "obj" / "Vmeter_sim")], tb, log)
            rc, _ = sh(["make", "-s", "-C", str(tb), "servo-build", f"METER_RTL={copy}",
                        f"SERVO_MDIR={d / 'objs'}"], tb, log)
            if rc:
                return f"BUILD {name} (servo)"
            rc2, o2 = sh([str(d / "objs" / "Vservo_sim")], tb, log)
            fails = [ln for ln in (o1 + o2).splitlines() if ln.startswith("FAIL") or "[FAIL]" in ln]
            verdicts.append((rc1 != 0 or rc2 != 0, fails))
        elif suite == "dma":
            tb = root / "tb/verilator/mbx"
            flags = subprocess.run(["make", "-s", "-C", str(tb), "print-dma-vflags"], check=True,
                                   capture_output=True, text=True).stdout.split("\n")
            flags = [f for f in flags if f]
            pkg = root / "hdl/milan/mailbox/KL_mbx_pkg.sv"
            rc, _ = sh([*flags, "--Mdir", str(d / "obj"), str(pkg), str(copy), str(tb / "dma_main.cpp"),
                        "-o", "Vmbx_dma"], tb, log)
            if rc:
                return f"BUILD {name}"
            rc1, o1 = sh([str(d / "obj" / "Vmbx_dma")], tb, log)
            fails = [ln for ln in o1.splitlines() if "[FAIL]" in ln]
            verdicts.append((rc1 != 0, fails))
        else:
            tb = root / "tb/verilator/milan_dp"
            for leg, mvar, exe in (("maprec8", "MAPREC8_MDIR", "Vmilan_dp_maprec8"),
                                   ("dynmap", "DYNMAP_MDIR", "Vmilan_dp_dynmap")):
                rc, _ = sh(["make", "-s", "-C", str(tb), f"{leg}-build", f"DP_SRC={copy}",
                            f"{mvar}={d / ('obj_' + leg)}"], tb, log)
                if rc:
                    return f"BUILD {name} ({leg})"
                rcx, ox = sh([str(d / ("obj_" + leg) / exe)], tb, log)
                fails = [ln for ln in ox.splitlines() if ln.startswith("FAIL") or "[FAIL]" in ln]
                verdicts.append((rcx != 0, fails))
    caught = any(v for v, _ in verdicts)
    first = [f for _, fl in verdicts for f in fl][:3]
    return f"{'caught' if caught else 'ESCAPED'} {name}: {first}"


def main() -> int:
    root, work, which = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    names = list(PLANTS) if which == "all" else [which]
    bad = 0
    for n in names:
        line = plant(root, work, n)
        print(line, flush=True)
        bad += not line.startswith("caught")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
