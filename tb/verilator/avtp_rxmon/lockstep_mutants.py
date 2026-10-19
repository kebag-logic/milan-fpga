#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the avtp_rxmon lockstep leg (#640 M6): prove its hazard checks can fail.

sim_lockstep.cpp runs the shipping KL_avtp_rx_monitor_ctx beside the
pre-change reference and grades four read-modify-write hazards of the
counter contexts with their own oracles: same-stream back-to-back updates
([H1]), an update colliding with a read ([H2]), every sink answering its own
GET_COUNTERS row ([GC]) and a reset during an update ([H4]). Each defect below
is the one its case exists for: a lost increment, a torn read, a wrong stream
index and a missed reset. The rest are #762's STREAM_INTERRUPTED rules
([SI]): a silence that unlocks without counting, a sequence gap that does not
count, an unbind that counts, an unbind that erases a silence already expired
(the walk's consume race), a stopped input's silence that counts, and a STOP
sampled at the walk instead of at the expiry. Each #762 defect is planted in
the engine AND in the reference copy, so the lockstep comparison cannot see it
and only the harness's own count oracle can fail. The real engine is mutated
one defect at a time, the SAME harness is rebuilt through the Makefile's own
recipe (`make lockstep-build` with RXMON_SRC, REF_SRC and LS_MDIR overridden)
at both shapes (N=1 and N=8), and both binaries run. Each mutant must make the harness FAIL by its
OWN verdict (a `[FAIL]` line or a tally with failures, read by
scripts/suite_tally.py), and the named check must be among the failures; a
crash or an abort is not a catch. The positive control is the clean pair
`make lockstep` just built (obj_ls1, obj_ls8), re-run here; a binary older
than any input of its recipe is stale and is rebuilt instead of graded.

What bounds a run. This driver sets no host-time deadline (rule 8's
wall-clock ratchet, scripts/test_evidence.budget item 4). The harness is
cycle-bounded by construction: every case steps a fixed number of cycles and
every wait on a DUT output carries a cycle bound, so a mutant ends within the
clean harness's cycle count. The host-time bound is the sweep's per-suite
guard in scripts/run_all_suites.sh; the SIGTERM handler turns that kill into
an exit that removes the temporary directory.

Usage: make -C tb/verilator/avtp_rxmon   (or python3 lockstep_mutants.py from there)
Exit 0 = every mutant was caught and the clean harness still passes.
"""

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
REF = HERE / "reference/KL_avtp_rx_monitor_ctx_ref.sv"
CLEAN_MDIR = HERE / "obj_ls"
#: every input of the clean recipe (the Makefile's LSSRCS and the harness,
#: and the Makefile itself): a clean binary older than any of them is stale
CLEAN_INPUTS = [RTL, REF,
                HERE / "avtp_rxmon_lockstep_wrap.sv", HERE / "sim_lockstep.cpp",
                HERE / "Makefile"]
EXE_NAME = "Vavtp_rxmon_lockstep"
SHAPES = ("1", "8")
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the GET_COUNTERS mirror's write port, as the engine writes it
MIRROR_WRITE = """  always_ff @(posedge clk_i) begin : mirror_wr
    if (cntw_hit_w)
      cnt_mirror_r[MIRW_C'(32'(ram_waddr_w[AW_C-1:5]) * 16 + 32'(cntw_col_w))]
        <= ram_wdata_w;
  end : mirror_wr"""

#: the #762 silence mark, as both modules write it
SI_MARK = "            if (bound_i[s] && !bind_fall_i[s] && !stopped_i[s])\n"
#: the unbind's unlock request, as both modules write it
UNBIND_UNLOCK = "        if (bind_fall_i[s] && locked_sh_r[s]) sil_pend_r[s] <= 1'b1;\n"
#: one boundary-sweep check, of either event
BOUNDARY = "boundary ({}, idle): after the expiry the silence counts once, on or before it never"

# (name, [(the ONE text it replaces, its replacement), ...], the check it must
# fail, whether the reference copy gets the same edits)
MUTATIONS = [
    ("lost increment: a pulse that lands on a queued dispatch drops out of the queue count",
     [("        default : ;                     //! 2'b11 (one in, one out) holds it",
       "        2'b11   : pq_cnt_r <= pq_cnt_r - 2'd1;\n        default : ;")],
     "[H1] STREAM_INTERRUPTED moved by exactly one per accepted gap PDU", False),
    ("torn read: the mirror takes a write's high half one cycle after its low half",
     [(MIRROR_WRITE,
       """  logic              tear_v_r;
  logic [MIRW_C-1:0] tear_a_r;
  logic [15:0]       tear_hi_r;
  always_ff @(posedge clk_i) begin : mirror_wr
    tear_v_r  <= cntw_hit_w;
    tear_a_r  <= MIRW_C'(32'(ram_waddr_w[AW_C-1:5]) * 16 + 32'(cntw_col_w));
    tear_hi_r <= ram_wdata_w[31:16];
    if (cntw_hit_w)
      cnt_mirror_r[MIRW_C'(32'(ram_waddr_w[AW_C-1:5]) * 16 + 32'(cntw_col_w))][15:0]
        <= ram_wdata_w[15:0];
    if (tear_v_r) cnt_mirror_r[tear_a_r][31:16] <= tear_hi_r;
  end : mirror_wr""")],
     "[H2] GET_COUNTERS read identical to the reference in every cycle of the update window", False),
    ("wrong stream index: the GET_COUNTERS read ignores the sink",
     [("      default : diag_q_o = cnt_mirror_r[MIRW_C'(32'(diag_ridx_w) * 16\n"
       "                                                + 32'(diag_col_i))];",
       "      default : diag_q_o = cnt_mirror_r[MIRW_C'(32'(diag_col_i))];")],
     "[GC] every sink answers its own row and column (seeded signatures)", False),
    ("missed reset: the bundle queue's count survives a reset",
     [("      pq_cnt_r    <= '0;\n      pq_wp_r     <= '0;", "      pq_wp_r     <= '0;")],
     "[H4] no bundle queued before a reset is served after it", False),
    ("silence: the watchdog's unlock is never marked an interruption (#762)",
     [(SI_MARK, "            if (1'b0)\n")],
     "[SI] a silence that unlocks a bound stream counts STREAM_INTERRUPTED once", True),
    ("gap: a sequence gap of two lost PDUs no longer interrupts (#762)",
     [("              | ((seq_mm_w && lost_w >= 8'(INTERRUPT_MIN_LOST_C))",
       "              | ((1'b0 && lost_w >= 8'(INTERRUPT_MIN_LOST_C))")],
     "[SI] a sequence gap of two lost PDUs counts STREAM_INTERRUPTED once", True),
    ("unbind: an unbind's unlock is counted as an interruption (#762)",
     [(UNBIND_UNLOCK, UNBIND_UNLOCK + "        if (bind_fall_i[s] && locked_sh_r[s]) sil_si_r[s] <= 1'b1;\n")],
     "[SI] an unbind of a locked stream counts no STREAM_INTERRUPTED", True),
    ("consume race: an unbind erases a silence already expired, before its walk counts it (#762)",
     [(UNBIND_UNLOCK, UNBIND_UNLOCK + "        if (bind_fall_i[s]) sil_si_r[s] <= 1'b0;\n")],
     BOUNDARY.format("an unbind"), True),
    ("stopped: a stopped input's silence is marked an interruption (#762)",
     [(SI_MARK, "            if (bound_i[s] && !bind_fall_i[s])\n")],
     "[SI] a stopped input's silence unlocks it but counts no STREAM_INTERRUPTED", True),
    ("stop at the walk: the stopped state is read when the walk counts, not at the expiry (#762)",
     [(SI_MARK, "            if (bound_i[s] && !bind_fall_i[s])\n"),
      ("                if (sil_si_r[ev_s_r]) begin",
       "                if (sil_si_r[ev_s_r] && !stopped_i[ev_s_r]) begin")],
     BOUNDARY.format("a STOP"), True),
]


def build(rtl_path: Path, mdir: Path, ref_path: Path = REF) -> list[Path] | None:
    """Build the harness at both shapes against `rtl_path` (and `ref_path`)
    through the suite's own recipe; the executables, or None when the recipe
    failed or left none."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "lockstep-build", f"RXMON_SRC={rtl_path}",
         f"REF_SRC={ref_path}", f"LS_MDIR={mdir}"],
        capture_output=True, text=True, check=False)
    exes = [Path(f"{mdir}{shape}") / EXE_NAME for shape in SHAPES]
    if out.returncode != 0 or not all(exe.is_file() for exe in exes):
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exes


def is_fresh(exes: list[Path]) -> bool:
    """True when every executable exists and is no older than any recipe input."""
    return all(exe.is_file() and all(exe.stat().st_mtime >= src.stat().st_mtime
                                     for src in CLEAN_INPUTS) for exe in exes)


def run_harness(exes: list[Path]) -> tuple[int, str]:
    """(worst rc, joined stdout) of one run of each shape, with no host
    deadline: the harness is cycle-bounded (module docstring)."""
    rcs, outs = [], []
    for exe in exes:
        out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True,
                             text=True, check=False)
        rcs.append(out.returncode)
        outs.append(out.stdout + out.stderr)
    worst = next((rc for rc in rcs if rc != 0), 0)
    return worst, "\n".join(outs)


def failed_checks(out: str) -> list[str]:
    """The names of the checks the harness printed as failed, in order."""
    return [line.strip()[len("[FAIL]"):].split(" got=")[0].strip()
            for line in out.splitlines() if line.strip().startswith("[FAIL]")]


def verdict(rc: int, out: str, must_fail: str | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        if must_fail and not any(line.strip().startswith("[FAIL]") and must_fail in line
                                 for line in out.splitlines()):
            return f"failed, but not the named check ({must_fail!r})"
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def plant(text: str, edits: list[tuple[str, str]], name: str, where: str) -> str | None:
    """`text` with every edit applied, or None (reported) when an anchor is not unique."""
    for pattern, replacement in edits:
        if text.count(pattern) != 1:
            print(f"[FAIL] mutation {name!r}: its pattern appears {text.count(pattern)} "
                  f"time(s) in {where}, expected exactly 1. The RTL moved and this "
                  f"mutant is no longer mutating anything - fix the pattern, do not delete the arm.")
            return None
        text = text.replace(pattern, replacement)
    return text


def run_mutant(src: str, ref: str,
               mutation: tuple[str, list[tuple[str, str]], str, bool], work: Path) -> bool:
    """Plant one mutation, build and run the harness; True when it was caught."""
    name, edits, breaks, both = mutation
    tag = name.split(":")[0].replace(" ", "_")
    mutated = plant(src, edits, name, RTL.name)
    if mutated is None:
        return False
    mpath = work / f"KL_avtp_rx_monitor_ctx_{tag}.sv"
    mpath.write_text(mutated)
    rpath = REF
    if both:
        mutated_ref = plant(ref, edits, name, REF.name)
        if mutated_ref is None:
            return False
        rpath = work / f"KL_avtp_rx_monitor_ctx_ref_{tag}.sv"
        rpath.write_text(mutated_ref)
    exes = build(mpath, work / f"obj_{tag}", rpath)
    if exes is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the harness")
        return False
    rc, out = run_harness(exes)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        broke = failed_checks(out)
        where = " (planted in the engine and the reference)" if both else ""
        print(f"[PASS] mutant caught{where}: {name} - breaks \"{breaks}\"")
        print(f"    it broke {len(broke)} check(s): {'; '.join(broke)}")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The harness does not prove \"{breaks}\".")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived."""
    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    src = RTL.read_text()
    ref = REF.read_text()
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="rxmon-lockstep-mutants-") as td:
        work = Path(td)
        exes: list[Path] | None = [Path(f"{CLEAN_MDIR}{shape}") / EXE_NAME for shape in SHAPES]
        if not is_fresh(exes):
            print(f"[INFO] {CLEAN_MDIR.name}1/{CLEAN_MDIR.name}8 are missing or older than "
                  f"their sources: the positive control is rebuilt")
            exes = build(RTL, work / "obj_clean")
        answer = verdict(*run_harness(exes), None) if exes else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated context engine still passes the lockstep harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated context engine does NOT pass ({answer}) - every "
                  f"mutant result is meaningless")
        for mutation in MUTATIONS:
            if run_mutant(src, ref, mutation, work):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
