#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""One planted defect per rule of the USB network path and the status LEDs.

WHY THIS EXISTS. A green suite and a suite that cannot go red look the same
from the outside. Each control below plants ONE defect in a copy of the RTL,
builds the harness against the copy, and requires the named check to fail.
The tree itself is never written, so nothing has to be restored.

Each control names the harness line it must break (a substring of the FAIL
line), so a control caught by an unrelated check is reported as not caught.

Usage:
    python3 mutants.py              # every control
    python3 mutants.py --list       # name them
    python3 mutants.py NAME ...     # only these
Environment: MUTANT_DIR, the scratch directory (default: a temporary one).

Exit 0 = every control was caught by its named check; 1 = one was not.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE.parent.parent.parent / "hdl" / "usbnet"
PKG, RXC, TXI, ARB, TAP, LED = ("KL_usbnet_pkg.sv", "KL_usbnet_rx_copy.sv", "KL_usbnet_tx_inject.sv",
                                "KL_usbnet_tx_arb.sv", "KL_usbnet_tap.sv", "KL_status_leds.sv")

# (name, harness, file, old, new, the FAIL text that must appear)
CONTROLS = [
    # ---- the receive copy, one per class --------------------------------------------------
    ("rx_host_unicast_kept", "tap", PKG,
     "return (h.dst == host) ? RXV_HOST : RXV_UNICAST;", "return RXV_UNICAST;",
     "unicast to the computer: copied=0"),
    ("rx_other_unicast_copied", "tap", PKG,
     "return (h.dst == host) ? RXV_HOST : RXV_UNICAST;", "return RXV_HOST;",
     "unicast to the device: copied=1"),
    ("rx_group_not_copied", "tap", PKG,
     "    return RXV_GROUP;\n  endfunction", "    return RXV_UNICAST;\n  endfunction",
     "broadcast ARP: copied=0"),
    ("rx_link_local_copied", "tap", PKG,
     "    if (is_link_local(h.dst))                       return RXV_LINKLOCAL;\n", "",
     "gPTP link-local: copied=1"),
    ("mrp_block_not_reserved", "tap", PKG,
     " || (a[47:4] == 44'h0180C200002)", "",
     "MVRP: copied=1"),
    ("link_local_block_too_wide", "tap", PKG,
     "return (a[47:4] == 44'h0180C200000)", "return (a[47:8] == 40'h0180C20000)",
     "01-80-C2-00-00-10 is not link-local: copied=0"),
    ("rx_tagged_stream_copied", "tap", PKG,
     "if (is_tagged(h)) return (h.itype == ETH_AVTP_C) && !h.o18[7];",
     "if (is_tagged(h)) return 1'b0;",
     "tagged AAF stream: copied=1"),
    ("stream_is_only_aaf", "tap", PKG,
     "return (h.etype == ETH_AVTP_C) && !h.o14[7];", "return (h.etype == ETH_AVTP_C) && h.o14 == 8'h02;",
     "experimental stream 0x7F: copied=1"),
    ("stream_includes_control", "tap", PKG,
     "return (h.etype == ETH_AVTP_C) && !h.o14[7];", "return (h.etype == ETH_AVTP_C);",
     "ADP multicast: copied=0"),
    ("rx_stream_before_host_order", "tap", PKG,
     "    if (is_stream(h))                               return RXV_STREAM;\n    if (!is_group(h.dst))",
     "    if (!is_group(h.dst))",
     "CVF stream unicast to the computer: copied=1"),
    ("rx_no_host_still_copies", "tap", PKG,
     "    if (!host_ok)                                   return RXV_OFF;\n", "",
     "attached=0: broadcast ARP: copied=1"),
    ("rx_double_tag_read", "tap", PKG,
     "return is_tagged(h) && ((h.itype == ETH_CTAG_C) || (h.itype == ETH_STAG_C));",
     "return 1'b0;", "attached=1: double tag: copied=1"),
    ("rx_full_overwrites", "tap", RXC,
     "wire         room_w  = (start_w - rd_ptr_r) != (AW_C+1)'(DEPTH_P);",
     "wire         room_w  = 1'b1;", "a full buffer drops whole frames"),
    ("rx_odd_pad_stale", "tap", RXC,
     "if (words_r == 11'd1 && olen_r[0]) m_data_o[15:8] = 8'h00;", "",
     "records toward the computer are well formed"),
    ("rx_rollback_missing", "tap", RXC,
     "wire [AW_C:0] start_w = in_frame_r ? wr_cur_r : wr_ptr_r;",
     "wire [AW_C:0] start_w = wr_cur_r;",
     "is octet-exact"),
    # ---- the transmit drops ---------------------------------------------------------------
    ("tx_source_unchecked", "tap", PKG,
     "if (!host_ok || h.src != host)                  return TXV_SOURCE;",
     "if (!host_ok)                                   return TXV_SOURCE;",
     "foreign source: verdict 0"),
    ("tx_link_local_passes", "tap", PKG,
     "    if (is_link_local(h.dst))                       return TXV_LINKLOCAL;\n", "",
     "gPTP: verdict"),
    ("tx_stream_passes", "tap", PKG,
     "    if (is_stream(h))                               return TXV_STREAM;\n    //!", "    //!",
     "untagged AAF: verdict 0"),
    ("tx_priority_unchecked", "tap", PKG,
     "if (is_tagged(h) && h.o14[7:5] > 3'd1)", "if (1'b0)",
     "tagged priority 3: verdict 0"),
    ("tx_background_refused", "tap", PKG,
     "if (is_tagged(h) && h.o14[7:5] > 3'd1)", "if (is_tagged(h) && h.o14[7:5] > 3'd0)",
     "tagged background: verdict 4"),
    ("tx_double_tag_passes", "tap", PKG,
     "    if (is_unreadable_tag(h))                       return TXV_SHAPE;\n", "",
     "double tag: verdict 0"),
    ("tx_too_long_passes", "tap", TXI,
     "if (rlen_w < 12'd14 || rlen_w > 12'(MAX_LEN_P)) begin", "if (rlen_w < 12'd14) begin",
     "too long: verdict"),
    ("tx_unknown_record_not_skipped", "tap", TXI,
     "              pst_r <= (rlen_w == 12'd0) ? P_HDR : P_SKIP;\n            end\n          endcase",
     "              pst_r <= P_HDR;\n            end\n          endcase",
     "one verdict per frame record"),
    ("host_universal_accepted", "tap", PKG,
     "return !a[40] && a[41];", "return !a[40];",
     "a universally administered address is refused"),
    ("host_timeout_ignored", "tap", TXI,
     "assign host_fresh_o = host_ok_o && (ms_r < 16'(HOST_TIMEOUT_MS_P));",
     "assign host_fresh_o = host_ok_o;",
     "a stale host record drops LD1"),
    ("usb_ok_ignores_superspeed", "tap", TAP,
     "&& host_fresh_w && host_state_o[0];", "&& host_fresh_w;",
     "LD1 input needs SuperSpeed"),
    ("usb_ok_ignores_bus", "tap", TAP,
     "assign usb_ok_o = bus_alive_i && host_ok_o", "assign usb_ok_o = host_ok_o",
     "LD1 input needs the bus clock"),
    # ---- the rate limit -------------------------------------------------------------------
    ("rate_four_times", "tap", TXI,
     "tok_r + TOK_W_C'(INC_C)", "tok_r + TOK_W_C'(4 * INC_C)",
     "the steady rate stays at the limit"),
    ("rate_cost_without_overhead", "tap", TXI,
     "+ 12'd24;", "+ 12'd0;",
     "the steady rate stays at the limit"),
    ("rate_too_slow", "tap", TXI,
     "tok_r + TOK_W_C'(INC_C)", "tok_r + TOK_W_C'(INC_C / 2)",
     "the limiter does not throttle below it"),
    # ---- best effort only -----------------------------------------------------------------
    ("arb_injection_outranks", "tap", ARB,
     "wire grant_lo_w = (ast_r == A_IDLE) && !hi_valid_i && lo_valid_i",
     "wire grant_lo_w = (ast_r == A_IDLE) && lo_valid_i",
     "the datapath wins every arbitration"),
    ("arb_mac_not_empty", "tap", ARB,
     "&& (out_r == '0) && answered_w;", "&& answered_w;",
     "no injected frame shared the MAC with a datapath frame"),
    ("arb_no_wait_for_end", "tap", ARB,
     "        A_WAIT: if (answered_w) ast_r <= A_IDLE;", "        A_WAIT: ast_r <= A_IDLE;",
     "no injected frame shared the MAC with a datapath frame"),
    ("arb_end_not_masked", "tap", ARB,
     "      if (ack_r != req_sync_r[1]) ack_r <= req_sync_r[1];\n      else                        tgl_r <= ~tgl_r;",
     "      if (ack_r != req_sync_r[1]) ack_r <= req_sync_r[1];\n      tgl_r <= ~tgl_r;",
     "the frame-end toggle counts the datapath frames only"),
    ("arb_inject_enable_ignored", "tap", ARB,
     "&& lo_valid_i && inject_en_i", "&& lo_valid_i",
     "inject_en_i low holds the computer's frames"),
    ("inject_gap_in_frame", "tap", TXI,
     "  assign m_valid_o = send_r;", "  assign m_valid_o = send_r && div_r[0];",
     "no gap inside a frame"),
    # ---- the LEDs, one per rule -----------------------------------------------------------
    ("ld0_ignores_link", "leds", LED,
     "usb_ok_i, link_up_i && !off_w};", "usb_ok_i, !off_w};",
     "all off: LD0"),
    ("ld0_no_blink", "leds", LED,
     "wire off_w = blink_r > MS_W_C'(BLINK_ON_MS_P);", "wire off_w = 1'b0;",
     "one frame: LD0 off for"),
    ("ld0_no_hold", "leds", LED,
     "    end else if (blink_r == '0) begin",
     "    end else if (blink_r <= MS_W_C'(BLINK_ON_MS_P)) begin",
     "a frame inside the 60 ms hold does not blink"),
    ("ld0_blinks_link_down", "leds", LED,
     "if (act_i && link_up_i) blink_r", "if (act_i) blink_r",
     "link back: LD0 on at once"),
    ("ld1_from_wrong_input", "leds", LED,
     "{stat_i[1], stat_i[0], usb_ok_i,", "{stat_i[1], stat_i[0], stat_i[0],",
     "LD1 alone"),
    ("ld2_ld3_swapped", "leds", LED,
     "{stat_i[1], stat_i[0], usb_ok_i,", "{stat_i[0], stat_i[1], usb_ok_i,",
     "LD2 alone"),
    ("led_full_duty", "leds", LED,
     "assign led_o   = state_o & {4{pwm_r < PWM_BITS_P'(DUTY_P)}};", "assign led_o   = state_o;",
     "link: LD0 lit"),
]


def run(name, harness, fname, old, new, want, scratch):
    work = scratch / name
    rtl = work / "rtl"
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(RTL, rtl)
    src = (rtl / fname).read_text()
    n = src.count(old)
    if n != 1:
        return f"NOT APPLIED ({n} matches of the planted text)"
    (rtl / fname).write_text(src.replace(old, new))
    (work / "obj" / harness).mkdir(parents=True, exist_ok=True)
    p = subprocess.run(["make", "-C", str(HERE), harness, f"RTL={rtl}", f"OBJ={work / 'obj'}"],
                       capture_output=True, text=True)
    out = p.stdout + p.stderr
    fails = [l for l in out.splitlines() if l.startswith("FAIL ") and ".cpp:" in l]
    if p.returncode == 0:
        return "NOT CAUGHT (the harness passed)"
    if not fails:
        return "NOT CAUGHT (the build failed, no check ran):\n" + out[-800:]
    if not any(want in l for l in fails):
        return "CAUGHT BY ANOTHER CHECK:\n    " + "\n    ".join(fails[:4])
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    if a.list:
        for c in CONTROLS:
            print(f"{c[0]:34s} {c[1]:5s} {c[2]}")
        return 0
    sel = [c for c in CONTROLS if not a.names or c[0] in a.names]
    scratch = Path(os.environ.get("MUTANT_DIR") or tempfile.mkdtemp(prefix="usbnet-mut-"))
    bad = 0
    for c in sel:
        r = run(*c, scratch)
        print(f"{'caught' if r is None else 'MISSED'}  {c[0]}" + ("" if r is None else f": {r}"), flush=True)
        bad += r is not None
    print(f"{len(sel) - bad} of {len(sel)} controls caught by their named check")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
