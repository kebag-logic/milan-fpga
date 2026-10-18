#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the engine suite: prove its checks are load-bearing.

Why this exists. `sim_main.cpp` grades the whole plane through its wire and
publish faces, and the arms that repair FPGA-gPTP #31 - the accepted-beat
result face, the message-scoped lost arm, the retained Pdelay pairing
context and the three admission gates - are exactly the kind of behaviour a
harness can appear to check without checking. A suite whose assertions never
fail is indistinguishable from a suite that asserts nothing, and the defect
this round repairs was invisible to a green suite for that reason.

So the real engine RTL and the real micro-code generator are mutated, one
defect at a time, and the SAME harness is run against each mutant. Every
mutant must make it FAIL. The unmutated build must still PASS, without which
the arm would be satisfied by a harness that fails on everything.

"Caught" means the harness's own tally says so; see tb/mutation_verdict.py
for why a non-zero exit alone is not a catch. Everything is staged into a
temporary directory, so nothing is written into the tree.

Cost note, recorded rather than hidden: micro-code mutants reuse one build of
the unmutated RTL, because a generator change moves only the ROM image the
simulation reads at start-up. RTL mutants are built individually.

What this arm deliberately does NOT list, recorded rather than hidden,
because the value of a mutation arm is also the map of what it cannot reach.
Removing the reset-backed read gate on the pending-pair cell alone survives
every check, and that survival is a property of the design rather than a gap
in the harness: the cell is read in only two places, and a new Pdelay_Req
clears it at its commit point before any post-reset timestamp result can
match a claim. The gate is kept because it is the second half of a stated
rule that pairs it with the t1 validity beside it, whose own removal IS
caught below; it is defence in depth with no reachable arm, not a checked
behaviour. Closing that would need a reachable state, not another mutant.

The lapse hook's asCapable term is also defence in depth. Removing only
that term survives: Sync pairs cannot be consumed while incapable, and
the 375 ms Sync receipt watch clears sync-ok before capability can recover
through two good Pdelay exchanges at 1 s cadence. Only mastership disarms
that watch, and mastership retires the qualifier itself. This is a
reachability argument from the current policy, not an executed proof;
revisit it if the timer or capability recovery rules change.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HDL = (HERE / "../../../hdl").resolve()
sys.path.insert(0, str((HERE / "../../").resolve()))

from mutation_verdict import verdict  # noqa: E402

#: the RTL the suite builds, in the order the Makefile lists it
RTL_SOURCES = (
    "ucpu/gptp_ucpu_pkg.sv",
    "ucpu/KL_gptp_ucpu.sv",
    "wire/KL_gptp_rx_parser.sv",
    "wire/KL_gptp_tx_slot.sv",
    "common/KL_gptp_timer.sv",
    "top/KL_gptp_engine.sv",
)
GENERATOR = "ucode/gen_gptp_ucode.py"
#: the shipping arguments of this suite's image, as tb/verilator/engine/Makefile
GENARGS = ("--clk-hz", "2000000", "--cease-ms", "3000")

VFLAGS = [
    "--cc", "--exe", "--build", "-j", "4", "--top-module", "KL_gptp_engine",
    "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
    "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
    "-GUCODE_HEX_P=\"gptp_ucode.hex\"", "-GCLK_HZ_P=2000000",
]

#: (name, file under hdl/, pattern, replacement, the property it should break)
MUTATIONS = [
    # ---- #75: the policy level must cover the entire affected interval ----
    ("slew level tied low", "top/KL_gptp_engine.sv",
     "      // gather: atomic millisecond snapshot",
     "      phc_slew_active_o <= 1'b0; // injected tied-low output\n"
     "      // gather: atomic millisecond snapshot",
     "slew: policy decision starts at +101 ns"),
    ("slew clears at the first in-band pair", GENERATOR,
     "    p.emit(\"MOVE\", rd=RB, ra=0, imm=3)                       # reload, then -1",
     "    p.emit(\"MOVE\", rd=RB, ra=0, imm=2)                       # early completion",
     "slew: first in-band pair cannot clear"),
    ("slew clears before the replacement rate", "top/KL_gptp_engine.sv",
     "                if (st_wdata_w[1:0] != 2'd0)\n"
     "                  phc_slew_active_o <= 1'b1;",
     "                phc_slew_active_o <= (st_wdata_w[1:0] != 2'd0);",
     "slew: no clear precedes the replacement rate"),
    ("slew idle lapse arms qualification", "top/KL_gptp_engine.sv",
     "                if (phc_slew_active_o &&\n",
     "                if (1'b1 &&\n",
     "slew: in-band pair after idle timeout stays inactive"),
    ("slew idle asCapable loss arms qualification", "top/KL_gptp_engine.sv",
     "                if (phc_slew_active_o &&\n"
     "                    (!st_wdata_w[2] || !st_wdata_w[3]))\n",
     "                if ((phc_slew_active_o && !st_wdata_w[3]) ||\n"
     "                    !st_wdata_w[2])\n",
     "slew: in-band pair after asCapable recovery stays inactive"),
    ("slew mastership keeps qualification", "top/KL_gptp_engine.sv",
     "                phc_slew_left_r   <= 2'd0;\n"
     "                phc_slew_active_o <= 1'b0;\n",
     "                phc_slew_active_o <= 1'b0;\n",
     "slew: in-band return from GM stays inactive"),
    # ---- the result face: acceptance, and what acceptance protects -------
    ("result face always ready", "top/KL_gptp_engine.sv",
     "assign txts_ready_o  = !txts_pend_r && rst_n;",
     "assign txts_ready_o  = 1'b1;",
     "a result already owed to the micro-code cannot be replaced by a "
     "later one"),
    ("result value taken without an accepted beat", "top/KL_gptp_engine.sv",
     "if (txts_accept_w)          txts_r <= txts_ns_i;",
     "if (txts_valid_i)          txts_r <= txts_ns_i;",
     "the accepted result keeps its own timestamp until its dispatch"),
    ("result tag taken without an accepted beat", "top/KL_gptp_engine.sv",
     "if (txts_accept_w) begin",
     "if (txts_valid_i) begin",
     "the accepted result keeps its own tag and outcome until its dispatch"),
    # ---- reset-backed validity of the pairing cells ----------------------
    ("recorded t1 survives reset", "top/KL_gptp_engine.sv",
     "        else if ((st_addr_w[5:0] == 6'd37) && !t1v_valid_r)\n"
     "          st_rd_mux_w = 64'd0;\n",
     "",
     "a t1 measured before a reset cannot pair with a later Follow_Up"),
    # ---- the byte face, which decides how many frames were sent ----------
    ("byte face advances without ready", "wire/KL_gptp_tx_slot.sv",
     "      end else if (tx_ready_i) begin",
     "      end else begin",
     "a stalled byte, including the final one, waits for an accepted "
     "transfer"),
    # ---- the lost arm, and its scope -------------------------------------
    ("lost t1 fabricates a time and a companion", GENERATOR,
     "    p.label(\"t1\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_T1V, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)\n"
     "    p.emit(\"END\")\n",
     "    p.label(\"t1\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)\n"
     "    p.emit(\"BR\", label=LB[\"TXT1OK\"])\n",
     "a lost result writes no time and completes no exchange"),
    ("lost Sync cancels the requester exchange", GENERATOR,
     "    p.label(\"sync\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)\n"
     "    p.emit(\"END\")                      # no SYNCFU: there is no "
     "origin time\n",
     "    p.label(\"sync\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_T1V, fmt=FMT_Q)\n"
     "    p.emit(\"END\")\n",
     "a lost Sync result retires the Sync claim and nothing else"),
    ("lost response cancels the requester exchange", GENERATOR,
     "    p.label(\"resp\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_TXQ_RESP, fmt=FMT_Q)\n"
     "    p.emit(\"END\")                      # no RFU: there is no t3 to "
     "carry\n",
     "    p.label(\"resp\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_TXQ_RESP, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)\n"
     "    p.emit(\"END\")\n",
     "a lost Pdelay_Resp result retires the response claim and nothing "
     "else"),
    # ---- the retained pairing context -------------------------------------
    ("a later response re-arms the frozen pair", GENERATOR,
     "    p.emit(\"RDST\", rd=RU, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)\n"
     "    p.emit(\"CMP\", ra=RU, rb=0, fmt=FMT_D, imm=0)\n"
     "    p.emit(\"BRS\", cnd=BRS_Z, label=\"arm_go\")\n"
     "    p.emit(\"BR\", label=\"multi\")                                   "
     "# frozen\n"
     "    p.label(\"arm_go\")\n",
     "    p.label(\"arm_go\")\n",
     "a complete pair keeps its own identity and operands until its t1"),
    ("the tail runs before its own t1", GENERATOR,
     "    p.emit(\"RDST\", rd=RT, imm=RG_SCR | S_T1V, fmt=FMT_Q)\n"
     "    p.emit(\"CMP\", ra=RT, rb=0, fmt=FMT_D, imm=1)\n"
     "    p.emit(\"BRS\", cnd=BRS_Z, label=\"t1_here\")\n"
     "    p.emit(\"WRST\", ra=RC, imm=RG_SCR | S_T3, fmt=FMT_Q)\n"
     "    p.emit(\"MOVE\", rd=RT, ra=0, imm=1)\n"
     "    p.emit(\"WRST\", ra=RT, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)\n"
     "    p.emit(\"END\")\n"
     "    p.label(\"t1_here\")\n",
     "    p.label(\"t1_here\")\n",
     "a delay is computed from this exchange's own t1, never a "
     "predecessor's"),
    ("a new request leaves the old pair live", GENERATOR,
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_T1V, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)\n"
     "    p.emit(\"RDST\", rd=RA, imm=RG_SCR | S_MYSEQ, fmt=FMT_Q)\n",
     "    p.emit(\"RDST\", rd=RA, imm=RG_SCR | S_MYSEQ, fmt=FMT_Q)\n",
     "a superseded exchange cannot pair with the new request's t1"),
    # ---- the three admission gates, one arm each --------------------------
    ("credit gate removed from the Pdelay_Req leg", GENERATOR,
     "    e_credit_gate(p, \"beat_off\")\n",
     "",
     "a Pdelay_Req beat is postponed while the transmit path has no "
     "credit"),
    ("credit gate removed from the Sync leg", GENERATOR,
     "    e_flag_gate(p, FL_ASCAP_C, FL_ASCAP_C, \"ac\", \"skip\")\n"
     "    e_credit_gate(p, \"skip\")\n"
     "    p.emit(\"RDST\", rd=RB, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)\n",
     "    e_flag_gate(p, FL_ASCAP_C, FL_ASCAP_C, \"ac\", \"skip\")\n"
     "    p.emit(\"RDST\", rd=RB, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)\n",
     "a Sync beat is postponed while the transmit path has no credit"),
    ("credit gate removed from the Announce leg", GENERATOR,
     "    e_flag_gate(p, FL_ASCAP_C, FL_ASCAP_C, \"ac\", \"skip\")\n"
     "    e_credit_gate(p, \"skip\")\n"
     "    p.emit(\"RDST\", rd=RA, imm=RG_SCR | S_ASEQ, fmt=FMT_Q)\n",
     "    e_flag_gate(p, FL_ASCAP_C, FL_ASCAP_C, \"ac\", \"skip\")\n"
     "    p.emit(\"RDST\", rd=RA, imm=RG_SCR | S_ASEQ, fmt=FMT_Q)\n",
     "an Announce beat is postponed while the transmit path has no credit"),
    # ---- the #68 step-versus-slew policy, one arm per rule -----------------
    ("every pair uses the locked threshold", GENERATOR,
     "    p.emit(\"RDST\", rd=RB, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n",
     "    p.emit(\"MOVE\", rd=RB, ra=0,"
     " imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C)\n",
     "a link-up pair steps over 20 us"),
    ("every pair uses the link-up threshold", GENERATOR,
     "    p.emit(\"MOVE\", rd=RT, ra=0,"
     " imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C)\n",
     "    p.emit(\"MOVE\", rd=RT, ra=0, imm=0)\n",
     "a locked pair slews up to 100 us"),
    ("exactly the threshold steps", GENERATOR,
     "    p.emit(\"ALU\", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=1)\n"
     "    p.emit(\"MD\", rd=RU, ra=RW, rb=RB, cnd=MD_DIVU)\n",
     "    p.emit(\"ALU\", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=0)\n"
     "    p.emit(\"MD\", rd=RU, ra=RW, rb=RB, cnd=MD_DIVU)\n",
     "an offset of exactly 20 us, or 100 us once locked, slews"),
    ("the step arm is unreachable", GENERATOR,
     "    p.emit(\"BRS\", cnd=BRS_Z, label=\"sv_slew\")\n",
     "    p.emit(\"BR\", label=\"sv_slew\")\n",
     "an offset over the threshold steps"),
    # word-neutral, because the BTCA leg fills its gap and one more word is
    # a packing refusal, not a mutant: the unlock takes the slot of the
    # Sync-cadence disarm, which disarms nothing for a plane that is
    # already a slave (18c's), and elsewhere leaves a cadence whose own
    # master gate sends nothing
    ("a grandmaster change unlocks the servo", GENERATOR,
     "    p.emit(\"WRST\", ra=0, imm=RG_TMR | 1, fmt=FMT_Q)        "
     "# sync TX off\n",
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n",
     "the servo stays locked across a grandmaster identity change"),
    # only an asCapable rise re-arms the link-up (the manager's ruling on
    # #68): each of these two re-adds a retired re-arm
    ("a receipt timeout unlocks the servo", GENERATOR,
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C)\n",
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n",
     "the servo stays locked across a Sync receipt timeout"),
    ("becoming grandmaster unlocks the servo", GENERATOR,
     "    e_flags(p, andm=FL_ASCAP_C, orm=FL_PRESENT_C | FL_AMGM_C)\n",
     "    e_flags(p, andm=FL_ASCAP_C, orm=FL_PRESENT_C | FL_AMGM_C)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n",
     "the servo stays locked across a return from mastership"),
    ("the locked threshold is 200 us", GENERATOR,
     "    p.emit(\"MOVE\", rd=RT, ra=0,"
     " imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C)\n",
     "    p.emit(\"MOVE\", rd=RT, ra=0,"
     " imm=2 * STEP_LOCKED_NS_C - STEP_LINKUP_NS_C)\n",
     "a locked pair steps over 100 us, after a receipt timeout too"),
    ("asCapable's rise keeps the lock", GENERATOR,
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)"
     "  # rose: link-up\n",
     "",
     "the first pair after asCapable rises, or after a reset, is a link-up"),
    ("becoming grandmaster keeps sync-ok", GENERATOR,
     "    e_flags(p, andm=FL_ASCAP_C, orm=FL_PRESENT_C | FL_AMGM_C)\n",
     "    e_flags(p, andm=FL_ASCAP_C | FL_SYNCOK_C,"
     " orm=FL_PRESENT_C | FL_AMGM_C)\n",
     "becoming grandmaster clears the sync-ok verdict"),
    ("the whole trim is not clamped", GENERATOR,
     "    e_sat(p, RT, RUNTIME[\"ilim\"], \"sv_a\")                    "
     "# +-200 ppm\n",
     "",
     "the written trim never leaves +-200 ppm"),
    ("the trim clamp is one unit wider than the envelope", GENERATOR,
     "    e_sat(p, RT, RUNTIME[\"ilim\"], \"sv_a\")",
     "    e_sat(p, RT, RUNTIME[\"ilim\"] + 1, \"sv_a\")",
     "the written trim never leaves the envelope the consumer derives"),
    ("the integrator is not clamped", GENERATOR,
     "    e_sat(p, RC, RUNTIME[\"ilim\"], \"sv_i\")                    "
     "# +-ILIM\n",
     "",
     "the integrator stays within +-200 ppm"),
    # ---- #82: thisClock and {thisClock} until a peer is elected ----------
    # Each control lists, after "#82 ", every named check it must fail.
    ("boot publication restored to zero", "top/KL_gptp_engine.sv",
     "  assign pub_gm_id_o     = pub_gm_self_w ? local_gm_id_w : pub_gm_r;\n"
     "  assign pub_parent_id_o = pub_parent_r;\n"
     "  assign pub_flags_o     = pub_flags_r;\n"
     "  assign pub_pdelay_ns_o = pub_pdelay_r;\n"
     "  assign pub_offset_o    = pub_offset_r;\n"
     "  assign pub_annq_o      = pub_annq_r;\n"
     "  assign pub_path_count_o = pub_gm_self_w ? {3'd0, local_clock_valid_r}\n",
     "  assign pub_gm_id_o     = pub_gm_r;\n"
     "  assign pub_parent_id_o = pub_parent_r;\n"
     "  assign pub_flags_o     = pub_flags_r;\n"
     "  assign pub_pdelay_ns_o = pub_pdelay_r;\n"
     "  assign pub_offset_o    = pub_offset_r;\n"
     "  assign pub_annq_o      = pub_annq_r;\n"
     "  assign pub_path_count_o = pub_gm_self_w ? 4'd0\n",
     "#82 cold boot: first commit names thisClock"
     " | #82 cold boot: first commit path is {thisClock}"
     " | #82 warm reset: first commit names thisClock"
     " | #82 warm reset: first commit path is {thisClock}"),
    ("no engine commit after reset", "top/KL_gptp_engine.sv",
     "  assign pub_commit_o     = ucpu_commit_w || boot_pub_commit_r;",
     "  assign pub_commit_o     = ucpu_commit_w;",
     "#82 cold boot: a commit lands with the first beat"
     " | #82 warm reset: a commit follows the release at once"),
    ("thisClock hides an elected peer", "top/KL_gptp_engine.sv",
     "  wire        pub_gm_self_w = (pub_gm_r == 64'd0);",
     "  wire        pub_gm_self_w = local_clock_valid_r;",
     "#82 peer wins: its commit names the peer GM"),
    ("an elected peer keeps the self path", "top/KL_gptp_engine.sv",
     "  assign pub_path_count_o = pub_gm_self_w ? {3'd0, local_clock_valid_r}",
     "  assign pub_path_count_o = local_clock_valid_r ? 4'd1",
     "#82 peer wins: its commit carries the peer path"),
    ("becoming grandmaster keeps the departed GM", GENERATOR,
     "    p.emit(\"WRST\", ra=RC, imm=RG_PUB | 0, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=RC, imm=RG_PUB | 1, fmt=FMT_Q)\n",
     "    p.emit(\"WRST\", ra=RC, imm=RG_PUB | 1, fmt=FMT_Q)\n",
     "#82 peer leaves: the mastership commit names thisClock"),
    ("becoming grandmaster keeps the departed path", GENERATOR,
     "    p.emit(\"WRST\", ra=RT, imm=RG_PUB | 6, fmt=FMT_Q)",
     "    p.emit(\"WRST\", ra=0, imm=RG_PUB | 6, fmt=FMT_Q)",
     "#82 peer leaves: the mastership commit path is {thisClock}"),
]


def stage(work: Path, tag: str,
          mutate: tuple[str, str, str] | None = None) -> Path:
    """A directory holding the RTL and the generator, with at most one
    mutated. Nothing outside the returned directory is written."""
    srcdir = work / f"src_{tag}"
    for name in RTL_SOURCES + (GENERATOR,):
        target = srcdir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        text = (HDL / name).read_text(encoding="utf-8")
        if mutate is not None and mutate[0] == name:
            text = text.replace(mutate[1], mutate[2])
        target.write_text(text, encoding="utf-8")
    return srcdir


def generate_image(srcdir: Path, rundir: Path) -> bool:
    """Write the suite's ROM image from `srcdir`'s generator. False when the
    generator refuses, which for a packing failure is a real answer."""
    rundir.mkdir(parents=True, exist_ok=True)
    out = subprocess.run(
        [sys.executable, str(srcdir / GENERATOR), *GENARGS,
         "-o", str(rundir / "gptp_ucode.hex")],
        capture_output=True, text=True)
    return out.returncode == 0 and (rundir / "gptp_ucode.hex").is_file()


def build(srcdir: Path, work: Path, tag: str) -> Path | None:
    """Build the harness against the RTL in `srcdir`; the exe, or None."""
    mdir = work / f"obj_{tag}"
    exe_name = f"Vengine_{tag}"
    out = subprocess.run(
        ["verilator", *VFLAGS, "--Mdir", str(mdir),
         "-CFLAGS", f"-std=c++17 -O2 -I{HERE} -Wall -Wextra",
         *[str(srcdir / s) for s in RTL_SOURCES],
         str(HERE / "sim_main.cpp"), "-o", exe_name],
        capture_output=True, text=True)
    exe = mdir / exe_name
    if out.returncode != 0 or not exe.is_file():
        return None
    return exe


def run_harness(exe: Path, rundir: Path) -> tuple[int, str]:
    """(rc, output) of one harness run, reading its image from `rundir`.

    No host deadline: every wait in sim_main.cpp is bounded in DUT cycles and
    reports its own timeout as a failed check, so a mutant that wedges the
    plane still returns a verdict.
    """
    out = subprocess.run([str(exe)], cwd=str(rundir),
                         capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr


def main() -> int:
    """Run the control and every mutant, and report the arm's exit status.

    0 when the unmutated sources pass and every mutant is caught; 1 when any
    mutant survived, failed to build, or no longer matches its pattern, each
    printed with the property it was defending.
    """
    passes = fails = 0
    with tempfile.TemporaryDirectory(prefix="engine-mutants-") as td:
        work = Path(td)

        # -- positive control: the real sources must still pass -------------
        clean_src = stage(work, "clean")
        clean_run = work / "run_clean"
        clean_exe = build(clean_src, work, "clean")
        if clean_exe is None or not generate_image(clean_src, clean_run):
            print("[FAIL] the unmutated sources did not build; every mutant "
                  "result below would be meaningless")
            return 1
        answer = verdict(*run_harness(clean_exe, clean_run))
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated engine still passes the harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated engine does NOT pass ({answer}) - "
                  f"every mutant result below is meaningless")

        # -- each mutant must be caught --------------------------------------
        for name, fname, pattern, replacement, breaks in MUTATIONS:
            src = (HDL / fname).read_text(encoding="utf-8")
            if src.count(pattern) != 1:
                fails += 1
                print(f"[FAIL] mutation {name!r}: its pattern appears "
                      f"{src.count(pattern)} time(s) in {fname}, expected "
                      f"exactly 1. The source moved and this mutant is no "
                      f"longer mutating anything - fix the pattern, do not "
                      f"delete the arm.")
                continue
            tag = "".join(c if c.isalnum() else "_" for c in name)
            srcdir = stage(work, tag, (fname, pattern, replacement))
            rundir = work / f"run_{tag}"
            if not generate_image(srcdir, rundir):
                fails += 1
                print(f"[FAIL] mutation {name!r}: the generator refused its "
                      f"image, so this mutant proves nothing about the "
                      f"harness")
                continue
            if fname == GENERATOR:
                exe = clean_exe          # only the ROM image differs
            else:
                exe = build(srcdir, work, tag)
            if exe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not build; a mutant that "
                      f"cannot build proves nothing about the harness")
                continue
            rc, output = run_harness(exe, rundir)
            answer = verdict(rc, output)
            # #75 controls must fail their specific behavioral check; an
            # unrelated existing failure cannot stand in for that evidence.
            if breaks.startswith("slew:") and answer == "caught":
                named = [line for line in output.splitlines()
                         if line.startswith("FAIL ") and breaks in line]
                if not named:
                    answer = "missed its named check"
                else:
                    print(named[0])
            # #82 controls must fail every check they name, for the same
            # reason: each of those checks needs its own failing defect.
            if breaks.startswith("#82 ") and answer == "caught":
                failed = [line for line in output.splitlines()
                          if line.startswith("FAIL ")]
                missed = [want for want in breaks.split(" | ")
                          if not any(want in line for line in failed)]
                if missed:
                    answer = ("missed its named check(s): "
                              + "; ".join(missed))
                else:
                    for want in breaks.split(" | "):
                        print(next(line for line in failed if want in line))
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
            elif answer == "pass":
                fails += 1
                print(f"[FAIL] mutant SURVIVED: {name}. The harness does not "
                      f"prove \"{breaks}\".")
            else:
                fails += 1
                print(f"[FAIL] mutant {name!r} {answer}")

    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
