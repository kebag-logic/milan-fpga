#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #530/#551 streaming licence in milan_dp: prove the checks can fail.

sim_crf_licence.cpp (the obj_crflic leg) asserts on the shipping AX 1x1 TDM8
shape that nothing is emitted while the processor declares and admits a
Stream Output that no Listener Ready has reached, and that the CRF licence
and the AAF gate require ACTIVE AND the real grant on every cycle. Before #530
all three consumers read the processor's raw admission verdict, which rises
at DECLARE_TALKER. So the real milan_datapath is mutated back, one consumer
at a time, and the SAME leg is rebuilt through the Makefile's own recipe
(`make crflic-build` with DP_SRC and CRFLIC_MDIR overridden, and PP_DIR for a
processor mutant) and run. Each mutant must make the leg FAIL by its OWN
verdict (a `[FAIL]` line or a tally with failures, read by
scripts/suite_tally.py), and the named check must be among the failures; a
crash or an abort is not a catch. The positive control
is the clean leg (obj_crflic, which `make crflic-mutants` builds and runs
first), re-run here.

#774 adds one control on two legs: every talker source given talker 0's
TSpec MaxFrameSize, the integration before #774, which declared the AAF
number for the CRF Media Clock Output. It must fail the [TSPEC] grading on
obj_crflic (AX 1x1 TDM8) and on obj_tspec8 (AX 8x8, `make tspec8-build`
with TSPEC8_MDIR overridden), each beside its own clean control.

#851 adds one control on the processor side, for processor #214's rule that
each MRPDU carries each attribute value at most once (the leg's [ONEVEC]
section, IEEE 802.1Q-2022 10.7.7, 10.7.5.13 c)). It is planted in a COPY of
the processor's hdl/ tree, built through the same recipe with PP_DIR
overridden, and must fail "no DUT MRPDU carries one attribute value in two
VectorAttributes". At #851 it tied the SRP encoder's value search to a miss,
so every second hand-over of a pending value appended an entry, as the
encoder did before #214. Since processor #216 each Applicant decides one
message per tx! and each round's drain waits for its tx!, so no value is
handed over twice in one window and that arm alone survives (#883). It now
removes both layers, as the processor's own push-twice-encoder-appends arm
does: the encoder's intake takes every push twice, and the encoder appends.

#883 adds four processor controls of the same kind, for processor #216 (the
leg's [MRPAPP] and [MVRPLA] sections, #860 and #857). They plant the
processor's own arms for its #216 defects, each the behaviour before #216: the
Domain declared at LINK_UP in AN, so it sends one New (IEEE 802.1Q-2018 Table
10-3); a VID's first join in AN, one New; every VID Join encoded JoinIn
whatever its Registrar (10.7.6.3); and an MVRP drain that needs a pending VID,
so with nothing declared no LeaveAll goes out (10.7.9, Table 10-5). Each must
fail its named check.

The other half of #530's failing arms, the protocol processor at its previous
pin 424c688f, needs a second processor checkout and is not run here; the
leg's README records how it was run and what it reported.

What bounds a run. This driver sets no host-time deadline (rule 8's
wall-clock ratchet, scripts/test_evidence.budget item 4). The leg is
cycle-bounded by construction: every phase runs to a fixed cycle target, the
AXI4-Lite BFM gives up after 2048 cycles per handshake, and no loop waits on
a DUT output without a cycle bound, so a mutant ends at the same cycle as
the clean leg. This is an explicit campaign outside the sweep
(docs/testing/TESTING.md), so run by hand nothing but the cycle bound limits
a run; the SIGTERM handler turns a kill into an exit that removes the
temporary directory.

Usage: make -C tb/verilator/milan_dp crflic-mutants
       (or python3 crflic_mutants.py from tb/verilator/milan_dp)
Exit 0 = every mutant was caught and both clean legs still pass.
"""

import re
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DP_RTL = HERE / "../../../hdl/milan/milan_datapath.sv"
PP_HDL = HERE / "../../../protocol-processor/hdl"
#: leg -> (its build target, the objdir variable, the clean objdir, the executable)
LEGS = {
    "crflic": ("crflic-build", "CRFLIC_MDIR", HERE / "obj_crflic", "Vmilan_dp_crflic"),
    "tspec8": ("tspec8-build", "TSPEC8_MDIR", HERE / "obj_tspec8", "Vmilan_dp_tspec8"),
}
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

# (name, the exact source fragment, its replacement, the check it must fail)
MUTATIONS = [
    ("every gate reads the raw verdict",
     "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
     "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];",
     "  assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];",
     "the CRF licence never opened (every cycle sampled)"),
    ("the CRF licence alone reads the raw verdict",
     "                           lwsrp_stream_gate[SRP_TALKERS_C-1];",
     "                           pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1];",
     "the CRF licence equals ACTIVE[CRF] AND real grant"),
    ("the AAF source 0 gate alone reads the raw verdict",
     "                   (~cfg_lwsrp_enable | lwsrp_stream_gate[0])));",
     "                   (~cfg_lwsrp_enable | pp_cd_srp_sr_admitted_w[0])));",
     "the AAF gate never opened"),
    ("every gate drops the real grant",
     "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
     "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];",
     "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0];",
     "refused CRF licence never opened"),
    ("the CRF licence alone drops the real grant",
     "                           lwsrp_stream_gate[SRP_TALKERS_C-1];",
     "                           pp_cd_srp_active_w[SRP_TALKERS_C-1];",
     "refused CRF licence never opened"),
    ("the AAF source 0 gate alone drops the real grant",
     "                   (~cfg_lwsrp_enable | lwsrp_stream_gate[0])));",
     "                   (~cfg_lwsrp_enable | pp_cd_srp_active_w[0])));",
     "refused AAF gate never opened"),
]

#: #774: (name, fragment, replacement, the check it must fail, the leg)
TALKER0_TSPEC = (
    "      .cfg_tspec_max_frame_i (pp_src_maxf_w),",
    "      .cfg_tspec_max_frame_i ({ACMP_SRC_C{tctx_maxf_w[0]}}),",
    "CRF TSpec MaxFrameSize is Milan v1.2 Table 4.4's 28 + 1")
TSPEC_MUTATIONS = [
    ("every source declares talker 0's TSpec on the 1x1", *TALKER0_TSPEC, "crflic"),
    ("every source declares talker 0's TSpec on the 8x8", *TALKER0_TSPEC, "tspec8"),
]

#: the SRP top's intake of the five producers, verbatim at the pin
PP_INTAKE = ("  assign dom_ev_ready_w  = enc_ev_ready_w && dom_ev_valid_w;\n"
             "  assign vlan_ev_ready_w = enc_ev_ready_w && !dom_ev_valid_w\n")
#: ...and the intake taking every push twice (the processor's push-twice arm)
PP_INTAKE_TWICE = ("  logic dup_r;\n"
                   "  always_ff @(posedge clk_i) begin : push_twice\n"
                   "    if (!rst_n) dup_r <= 1'b0;\n"
                   "    else if (enc_ev_valid_w && enc_ev_ready_w) dup_r <= !dup_r;\n"
                   "  end\n"
                   "  assign dom_ev_ready_w  = dup_r && enc_ev_ready_w && dom_ev_valid_w;\n"
                   "  assign vlan_ev_ready_w = dup_r && enc_ev_ready_w && !dom_ev_valid_w\n")
PP_INTAKE_TK = "  assign tk_ev_ready_w   = enc_ev_ready_w && !dom_ev_valid_w\n"
PP_INTAKE_LS = "  assign ls_ev_ready_w   = enc_ev_ready_w && !dom_ev_valid_w\n"

#: #851, processor #214, and #883, processor #216: (name, [(the file under the
#: processor's hdl/, the exact fragment, its replacement), ...], the check it
#: must fail), each on the 1x1 leg
PP_MUTATIONS = [
    ("the intake takes every push twice and the SRP encoder never merges (before processor #214)",
     [("srp/KL_srp_top.sv", PP_INTAKE, PP_INTAKE_TWICE),
      ("srp/KL_srp_top.sv", PP_INTAKE_TK, PP_INTAKE_TK.replace("= enc_ev", "= dup_r && enc_ev")),
      ("srp/KL_srp_top.sv", PP_INTAKE_LS, PP_INTAKE_LS.replace("= enc_ev", "= dup_r && enc_ev")),
      ("srp/KL_srp_encoder.sv",
       "  assign sr_hit_w    = sr_cont_w && (q_key_w == sr_key_r);",
       "  assign sr_hit_w    = 1'b0;")],
     "no DUT MRPDU carries one attribute value in two VectorAttributes"),
    ("LINK_UP declares the Domain in AN, so one New goes out (before processor #216)",
     [("srp/KL_srp_domain.sv",
       "        app_r      <= SRP_AP_VN_C;\n        declared_r <= 1'b1;\n",
       "        app_r      <= SRP_AP_AN_C;\n        declared_r <= 1'b1;\n")],
     "MSRP Domain {class A, 3, VID 2}: message 2 is New again (AN tx!: sN)"),
    ("a VID's first join enters AN, so one New goes out (before processor #216)",
     [("srp/KL_srp_vlan.sv",
       "      2'd0:    one_nx_w = srp_app_next(one_st_w, SRP_AE_NEW_C, reg_nx_w[one_ix_w], p2p_i);",
       "      2'd0:    one_nx_w = SRP_AP_AN_C;")],
     "MVRP VID 2: message 2 is New again (AN tx!: sN)"),
    ("every VID Join is JoinIn whatever its Registrar (before processor #216)",
     [("srp/KL_srp_vlan.sv",
       "    wmsg_w = srp_app_msg(app_ev_w[widx_r], wla_r, reg_nx_w[widx_r]);",
       "    wmsg_w = srp_app_msg(app_ev_w[widx_r], wla_r, 1'b1);")],
     "no MVRP JoinIn in the whole run: no VID was ever registered (10.7.6.3)"),
    ("an MVRP drain needs a pending VID, so nothing declared sends no LeaveAll (before processor #216)",
     [("srp/KL_srp_encoder.sv",
       "                 && ((cnt_mvrp_r != '0) || la_pend_r[1] || leaveall_i[1]);",
       "                 && (cnt_mvrp_r != '0);")],
     "MVRP, nothing declared: at least two LeaveAll MRPDUs after the withdrawal"),
]


def build(rtl_path: Path, mdir: Path, leg: str = "crflic", pp_dir: Path | None = None) -> Path | None:
    """Build `leg` against `rtl_path` (and the processor tree `pp_dir`, when
    given) through the suite's own recipe; the executable, or None when the
    recipe failed or left none."""
    target, mdir_var, _, exe_name = LEGS[leg]
    pp = [f"PP_DIR={pp_dir}"] if pp_dir else []
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), target, f"DP_SRC={rtl_path}",
         f"{mdir_var}={mdir}", *pp],
        capture_output=True, text=True, check=False)
    exe = mdir / exe_name
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_leg(exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one run of the leg, with no host deadline: the leg is
    cycle-bounded (module docstring)."""
    out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True,
                         text=True, check=False)
    return out.returncode, out.stdout + out.stderr


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


def run_mutant(src: str, mutation: tuple[str, ...], work: Path) -> bool:
    """Plant one mutation, build and run its leg; True when it was caught."""
    name, pattern, replacement, breaks = mutation[:4]
    leg = mutation[4] if len(mutation) > 4 else "crflic"
    if src.count(pattern) != 1:
        print(f"[FAIL] mutation {name!r}: its pattern appears {src.count(pattern)} "
              f"time(s) in {DP_RTL.name}, expected exactly 1. The RTL moved and this "
              f"mutant is no longer mutating anything - fix the pattern, do not delete the arm.")
        return False
    tag = re.sub(r"[^A-Za-z0-9]+", "_", name)
    mpath = work / f"milan_datapath_{tag}.sv"
    mpath.write_text(src.replace(pattern, replacement))
    exe = build(mpath, work / f"obj_{tag}", leg)
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the leg")
        return False
    answer = verdict(*run_leg(exe), breaks)
    if answer == "caught":
        print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The leg does not prove \"{breaks}\".")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def run_pp_mutant(mutation: tuple, work: Path) -> bool:
    """Plant one mutation's edits in a copy of the processor's hdl/ tree, build
    the 1x1 leg against it and the real datapath, and run it; True when caught."""
    name, edits, breaks = mutation
    texts: dict[str, str] = {}
    for rel, pattern, replacement in edits:
        src = texts.get(rel, (PP_HDL / rel).read_text())
        if src.count(pattern) != 1:
            print(f"[FAIL] mutation {name!r}: a pattern appears {src.count(pattern)} "
                  f"time(s) in {rel}, expected exactly 1. The processor moved and this "
                  f"mutant is no longer mutating anything - fix the pattern, do not delete the arm.")
            return False
        texts[rel] = src.replace(pattern, replacement)
    tag = re.sub(r"[^A-Za-z0-9]+", "_", name)[:60]
    pp_dir = work / f"pp_hdl_{tag}"
    shutil.copytree(PP_HDL, pp_dir)
    for rel, text in texts.items():
        (pp_dir / rel).write_text(text)
    exe = build(DP_RTL, work / f"obj_{tag}", "crflic", pp_dir)
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the leg")
        return False
    answer = verdict(*run_leg(exe), breaks)
    if answer == "caught":
        print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The leg does not prove \"{breaks}\".")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived."""
    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    src = DP_RTL.read_text()
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="crflic-mutants-") as td:
        work = Path(td)
        for leg, (_, _, clean_mdir, exe_name) in LEGS.items():
            clean = clean_mdir / exe_name
            exe = clean if clean.is_file() else build(DP_RTL, work / f"obj_clean_{leg}", leg)
            answer = verdict(*run_leg(exe), None) if exe else "did not compile"
            if answer == "pass":
                passes += 1
                print(f"[PASS] the unmutated gateware still passes the obj_{leg} leg")
            else:
                fails += 1
                print(f"[FAIL] the unmutated gateware does NOT pass obj_{leg} ({answer}) - "
                      f"every mutant result on it is meaningless")
        for mutation in MUTATIONS + TSPEC_MUTATIONS:
            if run_mutant(src, mutation, work):
                passes += 1
            else:
                fails += 1
        for mutation in PP_MUTATIONS:
            if run_pp_mutant(mutation, work):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
