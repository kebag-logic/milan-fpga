#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for #948's depacketizer frame boundaries: sim_depkt.cpp's checks can fail.

sim_depkt.cpp holds, on KL_aaf_rx_depacketizer alone at four inputs, that each
PDU an input accepted reaches it as one frame of ceil(length/8) beats with
tlast on the last, for every payload length, and that a frame short of its
payload is dropped whole and counted. Each defect below breaks one of those;
the depacketizer is mutated one defect at a time and the SAME harness is
rebuilt through the Makefile's own recipe (`make depkt-build` with DEPKT_SRC
and DT_MDIR overridden, no payload lead). Each mutant must make the harness
FAIL by its own verdict, with the named check among the failures; a crash or
an abort is not a catch. The positive control is the unmutated depacketizer,
rebuilt here.

What bounds a run: the harness is cycle-bounded by construction, and the
host-time bound is the sweep's per-suite guard in scripts/run_all_suites.sh.

Usage: make -C tb/verilator/avtp_rxmon   (or python3 depkt_mutants.py from there)
Exit 0 = every mutant was caught and the clean harness still passes.
"""

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lockstep_mutants import failed_checks, plant, verdict  # noqa: E402

SRC = HERE / "../../../hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv"
EXE_NAME = "Vdepkt"

# (name, [(the ONE text it replaces, its replacement)], the check it must fail)
MUTATIONS = [
    ("a tail left in the hold: the frame's last word is popped with the beat before it, so the pass ends and "
     "the read side resynchronises without the final beat (the #948 frame-boundary defect)",
     [("  wire keep_w      = ff_last && (remain_r > 16'd8) &&\n"
       "                     (remain_r <= 16'd8 + 16'(k_w));\n",
       "  wire keep_w      = 1'b0;\n")],
     "[DT1] a 65-octet payload: 9 beats, tlast on the last"),
    ("a tail left in the hold behind a C-VLAN tag is sized for an untagged frame",
     [("                     (remain_r <= 16'd8 + 16'(k_w));\n",
       "                     (remain_r <= 16'd10);\n")],
     "[DT2] cases whose every output frame is whole, in order, under its index"),
    ("a frame short of its payload is committed and read out in part",
     [("          if (fw_good_w && !wshort_w) wc_r <= wp_r + 1'b1;\n",
       "          if (fw_good_w) wc_r <= wp_r + 1'b1;\n"),
      ("        rq_com_r[fate_e_w] <= !wdrop_w && !wshort_w;\n",
       "        rq_com_r[fate_e_w] <= !wdrop_w;\n"),
      ("        rq_drp_r[fate_e_w] <= wdrop_w || wshort_w;\n",
       "        rq_drp_r[fate_e_w] <= wdrop_w;\n")],
     "[DT3] 192 octets, 40 short, inputs 3: ...each its beats, its tlast, its index and its bytes, in order"),
    ("a frame short of its payload is dropped but counted for none of its accepting inputs",
     [("        rq_drp_r[fate_e_w] <= wdrop_w || wshort_w;\n",
       "        rq_drp_r[fate_e_w] <= wdrop_w;\n")],
     "[DT3] 192 octets, 1 short, inputs 3: drop_p_o names each short frame's accepting inputs"),
    ("drops_o leaves out a frame short of its payload",
     [("  wire           ovf_w   = tl_w && (wdrop_w || trunc_w);\n",
       "  wire           ovf_w   = tl_w && wdrop_w;\n")],
     "[DT3] 192 octets, 1 short, inputs 3: drops_o counts each short frame"),
    ("the length check reads a tagged frame's data_len where an untagged frame carries it",
     [("  wire  [15:0] wlen_w    = wvlan_r ? {w_tdata_w[55:48], w_tdata_w[63:56]}\n",
       "  wire  [15:0] wlen_w    = 1'b0    ? {w_tdata_w[55:48], w_tdata_w[63:56]}\n")],
     "[DT2] cases whose every output frame is whole, in order, under its index"),
    ("the length check takes a short last beat for a full one",
     [("  wire         wshort_w  = (wowe_r > 17'(wkeep_n_w));\n",
       "  wire         wshort_w  = (wowe_r > 17'd8);\n")],
     "[DT3] 192 octets, 1 short, inputs 3: output frames, one per accepting input"),
    ("the store's write side takes the tap as it comes, so a frame of ten beats or fewer ends before its enqueue "
     "pulse (the #948 short-frame defect)",
     [("  wire        in_acc    = dv_r[ENQ_LAT_C-1];\n", "  wire        in_acc    = tap_acc_w;\n"),
      ("  wire [63:0] w_tdata_w = dd_r[ENQ_LAT_C-1];\n", "  wire [63:0] w_tdata_w = s_tdata_i;\n"),
      ("  wire [7:0]  w_tkeep_w = dk_r[ENQ_LAT_C-1];\n", "  wire [7:0]  w_tkeep_w = s_tkeep_i;\n"),
      ("  wire        w_tlast_w = dl_r[ENQ_LAT_C-1];\n", "  wire        w_tlast_w = s_tlast_i;\n")],
     "[DT4] cases whose every output frame is whole, in order, under its index"),
    ("a pulse is taken only while its frame is still on the tap, so one after a nine- or ten-beat frame's tlast "
     "is lost",
     [("        if (s_tlast_i)     tbc_r <= '0;\n",
       "        if (s_tlast_i)     tbc_r <= '0;\n        if (s_tlast_i)     taw_r <= 1'b0;\n")],
     "[DT4] cases whose every output frame is whole, in order, under its index"),
    ("the verdict at the stored eighth beat misses a pulse that lands in that same cycle",
     [("  wire        q7_w      = tq_r || enq_tap_w;\n", "  wire        q7_w      = tq_r;\n")],
     "[DT4] the 1-channel 48 kHz Base PDU (a 62-octet frame): one output frame"),
    ("the write side runs two cycles behind the tap, one short of the enqueue pulse's latency",
     [("  localparam int ENQ_LAT_C = 3;\n", "  localparam int ENQ_LAT_C = 2;\n")],
     "[DT4] the 1-channel 48 kHz Base PDU (a 62-octet frame): one output frame"),
]


def build(src: Path, mdir: Path) -> Path | None:
    """Build the harness against `src` through the suite's own recipe; the executable, or None."""
    out = subprocess.run(["make", "-s", "-C", str(HERE), "depkt-build", f"DEPKT_SRC={src}", f"DT_MDIR={mdir}",
                          "DT_LEAD=0"], capture_output=True, text=True, check=False)
    exe = mdir / EXE_NAME
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_harness(exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one run, with no host deadline: the harness is cycle-bounded."""
    out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True, text=True, check=False)
    return out.returncode, out.stdout + out.stderr


def run_mutant(mutation: tuple[str, list[tuple[str, str]], str], work: Path, index: int) -> bool:
    """Plant one mutation, build and run the harness; True when it was caught."""
    name, edits, breaks = mutation
    text = plant(SRC.read_text(), edits, name, SRC.name)
    if text is None:
        return False
    mpath = work / f"m{index}_{SRC.name}"
    mpath.write_text(text)
    exe = build(mpath, work / f"obj_m{index}")
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build proves nothing")
        return False
    rc, out = run_harness(exe)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        broke = failed_checks(out)
        print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
        print(f"    it broke {len(broke)} check(s); first: {broke[0] if broke else '-'}")
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
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="rxmon-depkt-mutants-") as td:
        work = Path(td)
        exe = build(SRC.resolve(), work / "obj_clean")
        answer = verdict(*run_harness(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated depacketizer still passes its frame-boundary contract")
        else:
            fails += 1
            print(f"[FAIL] the unmutated depacketizer does NOT pass ({answer}) - every mutant result is meaningless")
        for index, mutation in enumerate(MUTATIONS):
            if run_mutant(mutation, work, index):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
