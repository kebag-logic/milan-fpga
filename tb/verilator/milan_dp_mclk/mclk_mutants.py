#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The #629 root leg and its named mutants, run as one pool.

docs/design/MEDIA_CLOCK_FOLLOWING.md's test plan names, for every
milan_datapath row, the defect its check must catch. This driver proves each
one: the clean leg (sim_mclk.cpp's legs A, B and C, the build `make mclk-build`
left in obj_mclk) must pass, and each mutant must make its short leg FAIL by
its OWN verdict, with the named check among the failures. A crash, an abort or
a failure of some other check is not a catch.

ONE ELABORATION FOR SIXTEEN MUTANTS (mutant schemata). Sixteen rebuilds of
the whole datapath do not fit the suite's 1800 s guard beside the leg itself.
So every mutation is planted once, into copies of milan_datapath.sv,
KL_aaf_clock_meter.sv and milan_csr.sv, each guarded by a selector the run
sets with `+MCLK_MUT=<id>`: with id 0 the copies are the tracked RTL, and with
id k exactly mutant k is live. Each copy reads the plusarg into its own
`mclk_mut_r` in an initial block, so no port or hierarchy changes. The copies
are elaborated through the suite's own recipe (`make mclk-build` with the
MUT_*_SRC overrides, which the Makefile SUBSTITUTES in the source list, so a
mutant cannot fall back to the tracked file). The schemata build's own clean
control is every short mode at id 0, which must pass.

THE POOL. The clean legs and every short run are independent processes; they
run SIM_JOBS at a time (default 4, the hosted runner's cores), so the
campaign shares the suite's wall clock instead of following it. Only the clean
legs' output enters the log in full: their tallies are the suite's. A mutant
run's output never does, because its [FAIL] lines are the expected result.

What bounds a livelocking mutant. Every mode of sim_mclk.cpp is bounded in
simulated time, never by a DUT output, so a run ends whatever the gateware
does. The host-time bound is the sweep's per-suite guard.

Usage: python3 mclk_mutants.py   (run from tb/verilator/milan_dp_mclk)
Exit 0 = the clean legs pass and every mutant was caught.
"""

import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl"
CLEAN_EXE = HERE / "obj_mclk/Vmilan_dp_mclk"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the three files the schemata plant into: (path, the Makefile override)
SOURCES = {
    "dp": (RTL / "milan/milan_datapath.sv", "MUT_DP_SRC"),
    "meter": (RTL / "ieee1722/crf/KL_aaf_clock_meter.sv", "MUT_AAFM_SRC"),
    "csr": (RTL / "common/csr/milan_csr.sv", "MUT_CSR_SRC"),
}

#: where each copy declares its selector: (file, the unique line it goes
#: before, ahead of every planted site in that file)
SELECTOR_ANCHOR = {
    "dp": '  `include "gen/adp_shape_defaults.svh"\n',
    "meter": "  wire               en_w = en_i;\n",
    "csr": "  localparam logic [ADDR_WIDTH-1:0] A_AAFM_STAT",
}
SELECTOR = ("  //! #629 mutant schemata (tb/verilator/milan_dp_mclk/mclk_mutants.py)\n"
            "  int unsigned mclk_mut_r;\n"
            "  initial begin\n"
            "    if (!$value$plusargs(\"MCLK_MUT=%d\", mclk_mut_r)) mclk_mut_r = 0;\n"
            "  end\n")


@dataclass(frozen=True)
class Edit:
    """One planted site: `pattern` must appear exactly once in the file."""

    source: str
    pattern: str
    replacement: str


@dataclass(frozen=True)
class Mutant:
    """One named defect: its selector id, the short leg, the check it breaks."""

    mid: int
    name: str
    mode: str
    breaks: str


EDITS = [
    Edit("dp", "      aaf_clk_selected_r <= aaf_sel_w;\n",
         "      aaf_clk_selected_r <= aaf_sel_w && (mclk_mut_r != 1);\n"),
    Edit("dp", "      follow_sel_r       <= aaf_sel_w ||\n",
         "      follow_sel_r       <= (aaf_sel_w && (mclk_mut_r != 1)) ||\n"),
    Edit("dp", "(aaf_clk_selected_r ? aafm_locked_w : crf_locked_w)",
         "((aaf_clk_selected_r && mclk_mut_r != 2) ? aafm_locked_w : crf_locked_w)"),
    Edit("dp", "ref_rate_w   = aaf_clk_selected_r ? aafm_rate_w : crf_rate_w;",
         "ref_rate_w   = (aaf_clk_selected_r && mclk_mut_r != 2) ? aafm_rate_w : crf_rate_w;"),
    Edit("dp", "ref_rate_valid_w = aaf_clk_selected_r ? aafm_rate_valid_w",
         "ref_rate_valid_w = (aaf_clk_selected_r && mclk_mut_r != 2) ? aafm_rate_valid_w"),
    Edit("dp", "  wire        mga_sel_w = int_clk_selected_r | follow_sel_r;",
         "  wire        mga_sel_w = (int_clk_selected_r && mclk_mut_r != 3) | follow_sel_r;"),
    Edit("dp", "crf_locked_w) && !ref_src_chg_w;",
         "crf_locked_w) && (!ref_src_chg_w || mclk_mut_r == 4);"),
    Edit("meter", "        mr_seeded_r  <= 1'b0;\n",
         "        if (mclk_mut_r != 5) mr_seeded_r  <= 1'b0;\n"),
    Edit("dp", "  wire mcr_restart_p_w /* verilator public_flat_rd */ =\n",
         "  logic aafm_lk_q_r;\n"
         "  always_ff @(posedge axis_clk) aafm_lk_q_r <= aafm_locked_w;\n"
         "  wire mcr_restart_p_w /* verilator public_flat_rd */ =\n"),
    Edit("dp", "       | aafm_disrupt_p_w | aafm_mr_toggle_p_w;",
         "       | ((mclk_mut_r == 6) ? (aafm_lk_q_r & ~aafm_locked_w)"
         " : (aafm_disrupt_p_w & (mclk_mut_r != 8))) | aafm_mr_toggle_p_w;"),
    Edit("dp", "      .en_i          (aaf_clk_selected_r),",
         "      .en_i          (aaf_clk_selected_r || mclk_mut_r == 7),"),
    Edit("meter", "(match_idx_i == follow_idx_i)",
         "(match_idx_i == follow_idx_i || mclk_mut_r == 9)"),
    Edit("dp", "  wire ctr_mclk_lock_w = ~clkv_tu_w & (~follow_sel_r | mcsrv_locked_w);",
         "  wire ctr_mclk_lock_w = ~clkv_tu_w & (~follow_sel_r | (mclk_mut_r == 10)"
         " | ((mclk_mut_r == 11) ? (aaf_clk_selected_r ? aafm_locked_w : crf_locked_w)"
         " : mcsrv_locked_w));"),
    Edit("meter", "        if (s2_gap_r)                              settle_r <= '0;\n",
         "        if (s2_gap_r) begin settle_r <= '0;"
         " if (mclk_mut_r == 12) locked_o <= 1'b0; end\n"),
    Edit("csr", "(rd_addr_q == A_AAFM_STAT) ||",
         "((rd_addr_q == A_AAFM_STAT) && mclk_mut_r != 13) ||"),
    Edit("csr", "(rd_addr_q == A_AAFM_RATE) ||",
         "((rd_addr_q == A_AAFM_RATE) && mclk_mut_r != 13) ||"),
    Edit("dp", "      .tu_i          (avtprx_tu_bit),",
         "      .tu_i          ((mclk_mut_r == 15) ? avtprx_tv_bit : avtprx_tu_bit),"),
    Edit("meter", "wire lock_clr_w  = en_rise_w || en_fall_w || idx_chg_w || !en_w;",
         "wire lock_clr_w  = en_rise_w || en_fall_w || (idx_chg_w && mclk_mut_r != 16) || !en_w;"),
    Edit("dp", "      if (pp_aecp_clk_src_index_w == 16'(k)) begin\n",
         "      if (pp_aecp_clk_src_index_w == 16'(k)"
         " && !(mclk_mut_r == 14 && k == AEM_N_CLKSRC_C - 1)) begin\n"),
]

MUTANTS = [
    Mutant(1, "the decode kept as the CRF-only compare", "select",
           "AAF0: the servo leaves IDLE once the meter locks"),
    Mutant(2, "the reference mux stuck on KL_crf_rx", "refmux",
           "AAF0: the trim holds until the meter's rate validates"),
    Mutant(3, "the aligner left disengaged at INTERNAL (no A2-a)", "internal",
           "INTERNAL: the packet grid holds the physical grid's rate"),
    Mutant(4, "the one-cycle unlocked presentation removed (W2)", "w2",
           "W2: the switch onto a locked CRF passes HOLDOVER"),
    Mutant(5, "no re-seed on a change of the followed listener", "switch",
           "switch: no request pulse at any switch"),
    Mutant(6, "the meter's raw lock-fall edge wired as the disruption", "switch",
           "switch: no request pulse at any switch"),
    Mutant(7, "the meter's enable tied high", "dwell",
           "(iii) INTERNAL dwell: AAF0's mr toggle raises no request"),
    Mutant(8, "disrupt_p not ORed into the request", "aafloss",
           "AAF loss: one request at the meter's timeout"),
    Mutant(9, "the echo ungated (the meter's listener compare ignored)", "echo",
           "echo: the unfollowed AAF1's toggle raises no request"),
    Mutant(10, "C0's level (~tu only)", "select",
           "C1: UNLOCKED moves at the switch onto AAF0"),
    Mutant(11, "C2's level (the reference lock)", "select",
           "C1: LOCKED holds until the servo reads LOCKED"),
    Mutant(12, "the meter's held lock cleared on a sequence gap", "loss",
           "loss leg: the servo stays LOCKED through single lost PDUs"),
    Mutant(13, "the read-window terms missing", "csr",
           "CSR: AAFM_STAT reads the meter's status word"),
    Mutant(14, "the decode table one source short (the previous shape's)", "switch",
           "switch: AAF1 decodes as listener 1 and the meter follows it"),
    Mutant(15, "tu taken from the tv net (the CRF wiring)", "tu",
           "tu: the followed talker's tu edge restarts the meter's history"),
    Mutant(16, "a change of the followed listener keeping a held lock", "silent",
           "switch (iv): the meter's lock clears at the switch"),
]


#: simulated seconds each short leg runs, so the pool starts the long ones
#: first and the short ones fill in behind them
MODE_SECONDS = {"loss": 9.0, "internal": 4.1, "refmux": 3.2, "aafloss": 0.4,
                "switch": 0.4, "silent": 0.3, "echo": 0.2, "dwell": 0.2, "tu": 0.1}


def plant(work: Path) -> dict[str, Path] | str:
    """Write the three schemata copies, or say which edit no longer applies."""
    texts = {key: path.read_text() for key, (path, _) in SOURCES.items()}
    for key, anchor in SELECTOR_ANCHOR.items():
        if texts[key].count(anchor) != 1:
            return f"the selector anchor {anchor.strip()!r} is not unique in {key}"
        texts[key] = texts[key].replace(anchor, SELECTOR + anchor)
    for e in EDITS:
        n = texts[e.source].count(e.pattern)
        if n != 1:
            return (f"{e.pattern.strip()!r} appears {n} time(s) in {e.source}, "
                    "expected exactly 1: the RTL moved, fix the pattern")
        texts[e.source] = texts[e.source].replace(e.pattern, e.replacement)
    out = {}
    for key, (path, _) in SOURCES.items():
        out[key] = work / path.name
        out[key].write_text(texts[key])
    return out


def build(copies: dict[str, Path], mdir: Path) -> Path | None:
    """Elaborate the schemata through the suite's own recipe."""
    args = ["make", "-s", "-C", str(HERE), "mclk-build", f"MCLK_MDIR={mdir}"]
    args += [f"{SOURCES[k][1]}={p}" for k, p in copies.items()]
    out = subprocess.run(args, capture_output=True, text=True, check=False)
    exe = mdir / "Vmilan_dp_mclk"
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-3000:])
        sys.stdout.write(out.stderr[-3000:])
        return None
    return exe


def run_leg(exe: Path, mode: str, mid: int) -> tuple[int, str]:
    """(rc, output) of one run, waited for with no host deadline."""
    args = [str(exe), f"--{mode}", f"+MCLK_MUT={mid}"]
    proc = subprocess.run(args, cwd=str(HERE), capture_output=True, text=True,
                          check=False)
    return proc.returncode, proc.stdout + proc.stderr


def verdict(rc: int, out: str, must_fail: str | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        named = any(line.strip().startswith("[FAIL]") and must_fail in line
                    for line in out.splitlines()) if must_fail else True
        if not named:
            return f"failed, but not the named check ({must_fail!r})"
        return "caught"
    return f"exited {rc} with no harness verdict - a crash is not a catch"


def jobs() -> int:
    """How many runs share the host at once."""
    raw = os.environ.get("SIM_JOBS", "4")
    return max(1, int(raw)) if raw.isdigit() else 4


def main() -> int:
    """Run the clean legs, the schemata's controls and every mutant."""
    passes = 0
    fails = 0
    if not CLEAN_EXE.is_file():
        print(f"[FAIL] the clean leg {CLEAN_EXE.name} is not built (make mclk-build)")
        return 1
    with tempfile.TemporaryDirectory(prefix="mclk-mutants-") as td:
        work = Path(td)
        copies = plant(work)
        if isinstance(copies, str):
            print(f"[FAIL] the schemata cannot be planted: {copies}")
            return 1
        exe = build(copies, work / "obj_mclk_mut")
        if exe is None:
            print("[FAIL] the schemata did not compile; no mutant proves anything")
            return 1
        modes = sorted({m.mode for m in MUTANTS})
        short = [("control", exe, mode, 0) for mode in modes]
        short += [("mutant", exe, m.mode, m.mid) for m in MUTANTS]
        short.sort(key=lambda r: -MODE_SECONDS.get(r[2], 0.1))
        runs = [("leg", CLEAN_EXE, leg, 0) for leg in ("a", "c", "b")] + short
        with ThreadPoolExecutor(max_workers=jobs()) as pool:
            results = list(pool.map(lambda r: run_leg(r[1], r[2], r[3]), runs))
    by_mid = {m.mid: m for m in MUTANTS}
    for (kind, _, mode, mid), (rc, out) in zip(runs, results):
        if kind == "leg":
            print(f"======== the clean leg {mode.upper()} ========")
            sys.stdout.write(out)
            ok = verdict(rc, out, None) == "pass"
            passes, fails = (passes + 1, fails) if ok else (passes, fails + 1)
            continue
        if kind == "control":
            answer = verdict(rc, out, None)
            ok = answer == "pass"
            print(f"[{'PASS' if ok else 'FAIL'}] the schemata at id 0 pass the "
                  f"--{mode} leg" + ("" if ok else f" ({answer}): every mutant "
                                     "result in that mode is meaningless"))
        else:
            m = by_mid[mid]
            answer = verdict(rc, out, m.breaks)
            ok = answer == "caught"
            print(f"[{'PASS' if ok else 'FAIL'}] mutant {mid} "
                  f"({m.name}, --{mode}): {answer}; breaks \"{m.breaks}\"")
        passes, fails = (passes + 1, fails) if ok else (passes, fails + 1)
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
