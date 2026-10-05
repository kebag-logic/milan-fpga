#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""mutants.py - planted RTL defects the packet-mailbox suite must catch (#665 lane F0).

Each arm copies hdl/milan/mailbox to a scratch directory, writes ONE defect
into the copy (a substitution that must occur exactly once), builds the
suite's harness against the copy with the Makefile's own recipe (read through
`make print-vflags`, never restated here) through the adapter the arm names,
runs it, and requires the run to complete with exit 1 and a `[FAIL]` line
naming the arm's check. A positive control, the unmodified RTL through both
adapters, runs first. The tree is never written: every build directory is
under the scratch root.

Usage:
    python3 tb/verilator/mbx/mutants.py [--jobs N] [--keep DIR]
    python3 tb/verilator/mbx/mutants.py --quick   # the suite's default arm: one defect per leaf

--quick runs QUICK only and no controls: the default `make` runs it after
run-wb and run-axil, which are its positive controls.

Exit 0 = every arm caught by its named check and both controls green;
1 = an arm escaped or a control failed; 2 = a fixture did not apply.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE.parents[2] / "hdl" / "milan" / "mailbox"
RTL_FILES = ("KL_mbx_pkg.sv", "KL_mbx_ring.sv", "KL_mbx_rx.sv", "KL_mbx_tx.sv", "KL_mbx_evt.sv", "KL_mbx.sv",
             "KL_mbx_wb.sv", "KL_mbx_axil.sv")


@dataclass(frozen=True)
class Arm:
    """One planted defect: file, substitution, the adapter build, the check that must fail."""

    name: str
    path: str
    old: str
    new: str
    host: int
    needle: str


ARMS = (
    Arm("rx-msg-type-ignored", "KL_mbx_rx.sv", "if (MBX_TERM_MASK_TBL_C[j][{1'b0, msg_r}]) begin", "if (1'b1) begin",
        0, "F2 ENTITY_DISCOVER for another entity, and AVAILABLE or DEPARTING"),
    Arm("rx-eq-own-is-eq-zero", "KL_mbx_rx.sv", "MBX_TEST_EQ_OWN_C:        if (field_ok && eqown_r[j])",
        "MBX_TEST_EQ_OWN_C:        if (field_ok && eqzero_r[j])", 0, "F2 ENTITY_DISCOVER for this entity passes"),
    Arm("rx-field-length-unchecked", "KL_mbx_rx.sv", "MBX_TEST_EQ_ZERO_C:       if (field_ok && eqzero_r[j])",
        "MBX_TEST_EQ_ZERO_C:       if (eqzero_r[j])", 0, "F2 a DISCOVER truncated"),
    Arm("rx-writes-past-free-space", "KL_mbx_rx.sv", "+ 32'd2 < 32'(free_w))", "+ 32'd2 < 32'(free_w) + 32'd64)",
        0, "D0 every unread record survives"),
    Arm("rx-bucket-never-drains", "KL_mbx_rx.sv",
        "      if (commit_w && ch_r == MBX_CH_W_C'(c)) tokens = tokens - 9'd1;\n", "", 0,
        "T0 the frames past it count in RATE_DROP"),
    Arm("rx-lanes-big-endian", "KL_mbx_rx.sv", "(5'd8 * 5'(lane_r))", "(5'd8 * (5'd3 - 5'(lane_r)))", 0,
        "F1 frame byte k is ring word"),
    Arm("rx-subtype-ignored", "KL_mbx_rx.sv",
        "(MBX_CH_HAS_SUBTYPE_TBL_C[c] == 0 || rx_data_i == 8'(MBX_CH_SUBTYPE_TBL_C[c]))", "1'b1", 0,
        "C0 ACMP to this talker or this listener passes"),
    Arm("tx-reserved-word-unchecked", "KL_mbx_tx.sv", "if (w0_ok_w && rd_data_i == 32'd0) begin",
        "if (w0_ok_w) begin", 0, "X1 a malformed TX record counts once in TX_ERR"),
    Arm("tx-refusal-no-flush", "KL_mbx_tx.sv", "tail_r[ch_r] <= tx_head_words_i[16*ch_r +: 16];",
        "tail_r[ch_r] <= tail_r[ch_r];", 0, "X1 and flushes the ring to TX_HEAD"),
    Arm("tx-fixed-priority", "KL_mbx_tx.sv", "c = (int'(last_ch_r) + k) % int'(MBX_N_CH_C);", "c = k - 1;", 0,
        "X0 round-robin"),
    Arm("evt-rearm-keeps-tag", "KL_mbx_evt.sv", "          tag_r[SW_C'(tmr_slot_i)] <= tmr_tag_i;\n", "", 0,
        "M1 a re-armed slot expires once, with the second arm's tag"),
    Arm("evt-cancel-arms", "KL_mbx_evt.sv", "armed_r[SW_C'(tmr_slot_i)] <= (32'(tmr_op_i) == MBX_TMR_OP_ARM_C);",
        "armed_r[SW_C'(tmr_slot_i)] <= 1'b1;", 0, "M0 no event by +4 ms"),
    Arm("evt-tick-count-lost", "KL_mbx_evt.sv", "tick_cnt_r <= tick_cnt_r + 16'd1;", "tick_cnt_r <= 16'd1;", 0,
        "K1 carrying every tick"),
    Arm("top-tick-always-enabled", "KL_mbx.sv", ".tick_en_i         (tick_ctl_r[MBX_TICK_CTL_EN_LSB_C]),",
        ".tick_en_i         (1'b1),", 0, "K0 no TICK while TICK_CTL.EN is clear"),
    Arm("top-gm-hi-live", "KL_mbx.sv", "mbx_place_f(32'(gm_hi_snap_r[0]),",
        "mbx_place_f(32'(gm_id_i[64*0 + 32 +: 32]),",
        0, "G0 GM_HI reads the snapshot"),
    Arm("top-partial-strobe-accepted", "KL_mbx.sv",
        "assign wr_w      = host_req_i && host_we_i && (host_be_i == 4'hF);",
        "assign wr_w      = host_req_i && host_we_i;", 0, "R2 a write with a partial strobe leaves the register"),
    Arm("top-irq-ignores-enable", "KL_mbx.sv", ") & irq_enable_r);", ") & 32'hFFFF_FFFF);", 0,
        "R2 a cause that is not enabled leaves the line low"),
    Arm("rx-maap-empty-count-overlaps", "KL_mbx_rx.sv", "overlap  = (field_r[j][15:0] != 16'd0) && (maap_count_i",
        "overlap  = (maap_count_i", 0, "C2 MAAP PROBE/DEFEND/ANNOUNCE overlapping this range pass"),
    Arm("rx-drop-uncounted", "KL_mbx_rx.sv", "drop_r[c] != 16'hFFFF) drop_r[c] <= drop_r[c] + 16'd1;",
        "drop_r[c] != 16'hFFFF) drop_r[c] <= drop_r[c];", 0, "D0 a frame the free space cannot hold counts in RX_DROP"),
    Arm("rx-refill-slow", "KL_mbx_rx.sv", "+ 32'd1 >= MBX_CH_RATE_REFILL_MS_TBL_C[c]);",
        "+ 32'd1 >= 2 * MBX_CH_RATE_REFILL_MS_TBL_C[c]);", 0, "T1 one refill period buys exactly one more frame"),
    Arm("tx-lanes-reversed", "KL_mbx_tx.sv", "assign tx_data_o  = pw_r[8*lane_r +: 8];",
        "assign tx_data_o  = pw_r[8*(2'd3 - lane_r) +: 8];", 0, "X0 the first frame leaves byte for byte"),
    Arm("evt-link-never-posts", "KL_mbx_evt.sv", "if (!any_w && link_up_i[i] != posted_up_r[i]) begin",
        "if (1'b0) begin", 0, "E0 a link rise posts a LINK event"),
    Arm("evt-gm-domain-dropped", "KL_mbx_evt.sv",
        "w3_w = 32'(gptp_domain_i[8*src_if_w +: 8]) << MBX_EV_GM_W3_DOMAIN_LSB_C;", "w3_w = '0;", 0,
        "E1 GM DOMAIN"),
    Arm("evt-expires-late", "KL_mbx_evt.sv", "$signed(now_ms_i - dl_r[scan_r]) >= 0",
        "$signed(now_ms_i - dl_r[scan_r]) > 0",
        0, "M0 slot 3 expires at its deadline"),
    Arm("top-irq-enable-unmasked", "KL_mbx.sv",
        "if (wr_w && off_w == AW2_C'(MBX_REG_IRQ_ENABLE_C)) irq_enable_r <= host_wdata_i & (",
        "if (wr_w && off_w == AW2_C'(MBX_REG_IRQ_ENABLE_C)) irq_enable_r <= host_wdata_i | (", 0,
        "R1 IRQ_ENABLE keeps RX[7:0], EVT and ERR only"),
    Arm("rx-closed-channel-stores", "KL_mbx_rx.sv", "hit_r      <= cls_hit_w && open_i[cls_ch_w];",
        "hit_r      <= cls_hit_w;", 0, "F0 a closed channel stores nothing"),
    Arm("rx-second-ethertype-ignored", "KL_mbx_rx.sv",
        "|| ethertype == 16'(MBX_CH_ETHERTYPE1_TBL_C[c]))", ")", 0,
        "C3 every MSRP and MVRP PDU reaches the SRP ring"),
    Arm("evt-only-exact-deadline", "KL_mbx_evt.sv", "$signed(now_ms_i - dl_r[scan_r]) >= 0",
        "now_ms_i == dl_r[scan_r]", 0, "M2 a deadline already past expires at once"),
    Arm("wb-address-shifted", "KL_mbx_wb.sv", "assign host_addr_o  = wb_adr_i[MBX_ADDR_W_C-1:0];",
        "assign host_addr_o  = {wb_adr_i[MBX_ADDR_W_C-2:0], 1'b0};", 0, "R0 CAPS.N_CH"),
    Arm("axil-read-uses-write-address", "KL_mbx_axil.sv",
        "assign host_addr_o  = go_wr_w ? aw_addr_r : ar_addr_r;", "assign host_addr_o  = aw_addr_r;", 1,
        "R0 CAPS.N_CH"),
    # The two combinational READYs of the adapter this one replaced: AR
    # yielding to a write offered in the same cycle, and AW waiting for W.
    Arm("axil-arready-follows-awvalid", "KL_mbx_axil.sv", "assign s_arready_o  = !ar_full_r;",
        "assign s_arready_o  = !ar_full_r && !s_awvalid_i;", 1, "A0 no AXI4-Lite output followed"),
    Arm("axil-awready-waits-for-wvalid", "KL_mbx_axil.sv", "assign s_awready_o  = !aw_full_r;",
        "assign s_awready_o  = !aw_full_r && s_wvalid_i;", 1, "A0 no AXI4-Lite output followed"),
    Arm("axil-write-without-w", "KL_mbx_axil.sv", "assign wr_ok_w = aw_full_r && w_full_r && !bvalid_r && !busy_r;",
        "assign wr_ok_w = aw_full_r && !bvalid_r && !busy_r;", 1, "A1 and no B answers it before its W"),
    Arm("axil-write-ignores-b-slot", "KL_mbx_axil.sv",
        "assign wr_ok_w = aw_full_r && w_full_r && !bvalid_r && !busy_r;",
        "assign wr_ok_w = aw_full_r && w_full_r && !busy_r;", 1, "A4 each write is answered by exactly one B"),
    Arm("axil-b-dropped-without-bready", "KL_mbx_axil.sv", "else if (s_bready_i) bvalid_r <= 1'b0;",
        "else bvalid_r <= 1'b0;", 1, "A4 BVALID holds for 10 clocks"),
    Arm("axil-r-dropped-without-rready", "KL_mbx_axil.sv",
        "end else if (s_rready_i) begin\n        rvalid_r <= 1'b0;", "end else begin\n        rvalid_r <= 1'b0;", 1,
        "A5 RVALID holds for 10 clocks"),
    Arm("axil-rdata-follows-port", "KL_mbx_axil.sv", "assign s_rdata_o    = rdata_r;",
        "assign s_rdata_o    = host_rdata_i;", 1, "A5 RDATA and RRESP hold with it"),
    Arm("axil-read-before-write", "KL_mbx_axil.sv", "assign go_rd_w = rd_ok_w && !wr_ok_w;",
        "assign go_rd_w = rd_ok_w;", 1, "A3 the read answers its own address"),
    Arm("axil-reset-keeps-aw", "KL_mbx_axil.sv", "      aw_full_r <= 1'b0;\n      aw_addr_r <= '0;\n",
        "      aw_addr_r <= '0;\n", 1, "A6 an AW taken before a reset is forgotten"),
)


#: One defect per leaf and one in the skeleton: the arm the suite's default target runs.
QUICK = ("rx-lanes-big-endian", "tx-refusal-no-flush", "evt-tick-count-lost", "top-partial-strobe-accepted")


def recipe() -> list[str]:
    """The Makefile's verilator command, one word per line."""
    res = subprocess.run(["make", "-s", "--no-print-directory", "print-vflags"], cwd=HERE, capture_output=True,
                         text=True, check=True)
    return [w for w in res.stdout.splitlines() if w]


def build_and_run(rtl_dir: Path, work: Path, host: int) -> tuple[int, str]:
    """Build the suite against rtl_dir through one adapter and run it."""
    work.mkdir(parents=True, exist_ok=True)
    argv = recipe() + [f"-GHOST_P={host}", "--Mdir", str(work / "obj"), "-j", "4",
                       *[str(rtl_dir / f) for f in RTL_FILES], "tb_mbx_top.sv", "sim_main.cpp", "-o", "Vmbx"]
    built = subprocess.run(argv, cwd=HERE, capture_output=True, text=True, check=False)
    if built.returncode != 0:
        return 2, built.stdout + built.stderr
    ran = subprocess.run([str(work / "obj" / "Vmbx"), str(host)], capture_output=True, text=True, check=False)
    return ran.returncode, ran.stdout + ran.stderr


def plant(arm: Arm, root: Path) -> Path:
    """A copy of the RTL with the arm's defect written into it."""
    copy = root / arm.name / "rtl"
    shutil.copytree(RTL, copy)
    target = copy / arm.path
    text = target.read_text(encoding="utf-8")
    if text.count(arm.old) != 1:
        raise ValueError(f"{arm.name}: fixture occurs {text.count(arm.old)} times in {arm.path}")
    target.write_text(text.replace(arm.old, arm.new), encoding="utf-8")
    return copy


def run_arm(arm: Arm, root: Path) -> tuple[Arm, bool, str]:
    """One arm's verdict and its first failing line."""
    rc, log = build_and_run(plant(arm, root), root / arm.name, arm.host)
    fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
    caught = rc == 1 and any(arm.needle in ln for ln in fails)
    detail = fails[0] if fails else (log.strip().splitlines() or ["no output"])[-1]
    return arm, caught, f"{len(fails)} check(s) failed; first: {detail}"


def main(argv: list[str] | None = None) -> int:
    """Controls first, then every arm."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--jobs", type=int, default=4, help="arms built and run at once")
    ap.add_argument("--keep", type=Path, help="keep the scratch builds here")
    ap.add_argument("--quick", action="store_true", help="QUICK arms only, no controls (the default make)")
    args = ap.parse_args(argv)
    arms = tuple(a for a in ARMS if a.name in QUICK) if args.quick else ARMS
    with tempfile.TemporaryDirectory(prefix="mbx-mutants-") as tmp:
        root = args.keep.resolve() if args.keep else Path(tmp)
        bad = 0
        for host in () if args.quick else (0, 1):
            rc, log = build_and_run(RTL, root / f"control-{host}", host)
            tally = [ln for ln in log.splitlines() if "checks:" in ln]
            verdict = tally[-1] if tally else log[-200:]
            print(f"[{'ok' if rc == 0 else 'FAIL'}] positive control, host {host}: {verdict}")
            bad += rc != 0
        try:
            with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
                results = list(pool.map(lambda a: run_arm(a, root), arms))
        except ValueError as exc:
            print(f"REFUSED: {exc}")
            return 2
        for arm, caught, detail in results:
            print(f"[{'ok' if caught else 'ESCAPED'}] {arm.name}: {detail}")
            bad += not caught
        print(f"mbx mutants: {sum(c for _a, c, _d in results)} of {len(arms)} caught")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
