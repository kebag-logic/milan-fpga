#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""split_mutants.py - the split leg's planted defects, each caught by the check it names (#665 F-INT PR 2).

Each arm plants one defect into a copy of one source of the split placement's
control path (the datapath's split branch, KL_mbx_cdc, its window or
KL_ctrl_split), builds the split leg through its own recipe (make build-split
with the copy in place of the source: DP_SRC, CDC_SRC, CDCW_SRC or CTLS_SRC)
into a directory of its own, and runs it. The arm is caught when the run
fails and prints FAIL beside the label of the check the arm names. A clean
build must pass first, so a bench that fails for another reason fails here.

    python3 split_mutants.py            # every arm
    python3 split_mutants.py --list
    python3 split_mutants.py --only NAME
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE.parents[2] / "hdl"
DP = RTL / "milan/milan_datapath.sv"
CDC = RTL / "milan/mailbox/KL_mbx_cdc.sv"
CDCW = RTL / "milan/mailbox/KL_mbx_cdc_window.sv"
CTLS = RTL / "milan/KL_ctrl_split.sv"
VAR = {DP: "DP_SRC", CDC: "CDC_SRC", CDCW: "CDCW_SRC", CTLS: "CTLS_SRC"}

#: (name, the source, its line as tracked, the planted line, the label of the check that must fail)
ARMS = (
    ("a class-D consumer on a G tie-off", DP,
     "    assign pp_cd_acmp_declaring_w     = i_ctl_pub_da_gate[ACMP_SRC_C-1:0];",
     "    assign pp_cd_acmp_declaring_w     = '0;",
     "[PUB] DA_GATE.OPEN reaches the talker's declaration predicate"),
    ("the licence on its ACTIVE term alone", DP,
     "    assign pp_cd_srp_sr_admitted_w    = i_ctl_pub_licence[ACMP_SRC_C-1:0];",
     "    assign pp_cd_srp_sr_admitted_w    = '0;",
     "[PUB] ...and its admitted term"),
    ("a stream_id taken without SID_VALID", DP,
     "          i_ctl_pub_sid_valid[k] ? i_ctl_pub_sid[64*k +: 64] : 64'd0;",
     "          i_ctl_pub_sid[64*k +: 64];",
     "[PUB] a stream_id without SID_VALID never reaches the listener"),
    ("a publication that never crosses again", CDC,
     "    else if (pub_send_r) pub_send_r <= ~pub_rcv_w;",
     "    else if (pub_send_r) pub_send_r <= 1'b1;",
     "[PUB] the stream_id reaches the listener once SID_VALID is set, within 60 mailbox cycles"),
    ("a setting taken before its commit", CDC,
     "    else if (fw_take_p_w) fw_r <= fw_bus_w;",
     "    else                  fw_r <= fw_bus_w;",
     "[FACE] a setting not committed does not reach the datapath"),
    ("a commit never acknowledged", CDC,
     "  cdc_pulse u_fw_ack (.src_clk(dp_clk_i), .src_rst_n(dp_rst_n), .src_pulse(fw_take_p_w),",
     "  cdc_pulse u_fw_ack (.src_clk(dp_clk_i), .src_rst_n(dp_rst_n), .src_pulse(1'b0),",
     "[FACE] the commit is acknowledged within MBX_FACE_ACK_CYCLES"),
    ("a setting on the wrong datapath port", DP,
     "    assign pp_aecp_clk_src_index_w = i_ctl_clk_src_index;",
     "    assign pp_aecp_clk_src_index_w = i_ctl_cur_config;",
     "[FACE] F_CLOCK.SOURCE_INDEX reaches the media clock's selector"),
    ("an answer under another tag", CDCW,
     "    .src_clk(dp_clk_i), .src_rst_n(dp_rst_n), .src_in({tag_r, ans_r}), .src_send(out_send_r),",
     "    .src_clk(dp_clk_i), .src_rst_n(dp_rst_n), .src_in({~tag_r, ans_r}), .src_send(out_send_r),",
     "[WIN] CTR closes DONE, not TIMEOUT"),
    ("an answer taken while the datapath waits", CDCW,
     "          end else if (!d_wait_i) begin",
     "          end else begin",
     "[WIN] ...and that word is not the empty one"),
    ("a tap that hands out the media subtypes", CTLS,
     "  assign accept_w = ((etype_w == ET_1722_C)\n                     && ((subtype_w == ST_ADP_C) || (subtype_w == ST_AECP_C)\n"
     "                         || (subtype_w == ST_ACMP_C) || (subtype_w == ST_MAAP_C)))",
     "  assign accept_w = (etype_w == ET_1722_C)",
     "[RX] ...and the tap hands out no frame"),
    ("a serializer that drops a frame's last byte", CTLS,
     "  assign rx_last_o  = ser_busy_r & ser_last_r & (ser_idx_r == ser_top_w);",
     "  assign rx_last_o  = ser_busy_r & ser_last_r & (ser_idx_r == ser_top_w - 3'd1);",
     "[RX] its record's length is the frame's"),
    ("a packer that reverses the lanes", CTLS,
     "        txp_data_r[8*txp_idx_r +: 8] <= tx_data_i;",
     "        txp_data_r[8*(3'd7 - txp_idx_r) +: 8] <= tx_data_i;",
     "[TX] ...byte for byte"),
    ("the LINK level held low", CDC,
     "      ev_hold_r <= {d_link_up_i, ev_pend_r[EV_W_C-2:0] | ev_new_w[EV_W_C-2:0]};",
     "      ev_hold_r <= {1'b0, ev_pend_r[EV_W_C-2:0] | ev_new_w[EV_W_C-2:0]};",
     "[LINK] the datapath's effective link reaches LINK.UP"),
)


def build_and_run(mdir: Path, overrides: dict[str, Path]) -> tuple[int, str]:
    """make build-split into mdir with the overrides, then run the leg: (rc, output)."""
    args = ["make", "-s", "--no-print-directory", "-C", str(HERE), "build-split", f"SPLIT_MDIR={mdir}"]
    args += [f"{var}={path}" for var, path in overrides.items()]
    built = subprocess.run(args, capture_output=True, text=True, env=dict(os.environ))
    if built.returncode:
        return -1, built.stdout[-3000:] + built.stderr[-3000:]
    ran = subprocess.run([str(mdir / "Vmilan_dp_split")], capture_output=True, text=True, cwd=HERE, timeout=1800)
    return ran.returncode, ran.stdout + ran.stderr


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    if args.list:
        print("\n".join(name for name, *_ in ARMS))
        return 0
    arms = [a for a in ARMS if args.only in (None, a[0])]
    if not arms:
        print(f"no arm named {args.only!r}")
        return 2
    work = Path(tempfile.mkdtemp(prefix="split-mutants-", dir=HERE))
    bad = 0
    try:
        rc, out = build_and_run(work / "clean", {})
        if rc != 0 or "failures: 0" not in out:
            print(f"FAIL control: the tracked sources must pass the split leg (rc {rc})\n{out[-2000:]}")
            return 1
        print("ok   control: the tracked sources pass the split leg")
        for name, src, old, new, label in arms:
            text = src.read_text()
            if text.count(old) != 1:
                print(f"FAIL {name}: its anchor is not in {src.name} once")
                bad += 1
                continue
            copy = work / name.replace(" ", "_").replace("'", "") / src.name
            copy.parent.mkdir(parents=True)
            copy.write_text(text.replace(old, new))
            rc, out = build_and_run(copy.parent / "obj", {VAR[src]: copy})
            caught = rc > 0 and any(line.startswith(f"FAIL {label}") for line in out.splitlines())
            print(f"{'ok  ' if caught else 'FAIL'} {name}: {'caught by ' + label if caught else f'rc {rc}, not caught by {label}'}")
            if not caught:
                print("\n".join(line for line in out.splitlines() if line.startswith("FAIL") or "error" in line)[:2000])
            bad += not caught
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"split mutants: {len(arms) - bad} of {len(arms)} caught by the check each names")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
