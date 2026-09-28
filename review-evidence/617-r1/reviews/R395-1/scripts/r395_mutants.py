#!/usr/bin/env python3
"""Reviewer-authored mutants for PR #618 (issue #617), round R395-1.

Each mutant edits a COPY of hdl/ieee1722/aaf/KL_chan_map_capture.sv (every
pattern must occur exactly once) and is run against:
  - the capture_coherence junction harness (full scenario list), built through
    the suite's own Makefile with CMAP_SRC/MDIR overridden;
  - the chmap_capture harness (lane A four-pair frame, lane B one-pair frame),
    built from an untracked probe copy of the suite directory with SRCS
    overridden (the netlist leg is not run for mutants).
The tree's tracked files are never written.

Usage: r395_mutants.py <clone> <workdir> <outdir>
"""
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    ("RM1 frame length ignored: close on the bucket's last pair (N_TDM_PAIRS_C-1), not TDM_FRAME_PAIRS_P-1",
     [("(32'(tdm_pair_slot_i) == TDM_FRAME_PAIRS_P - 1);",
       "(32'(tdm_pair_slot_i) == N_TDM_PAIRS_C - 1);"),
      ("(t == int'(TDM_FRAME_PAIRS_P) - 1) ? tdm_pair_w",
       "(t == int'(N_TDM_PAIRS_C) - 1) ? tdm_pair_w")]),
    ("RM2 frame closed by the second-to-last pair",
     [("(32'(tdm_pair_slot_i) == TDM_FRAME_PAIRS_P - 1);",
       "(32'(tdm_pair_slot_i) == TDM_FRAME_PAIRS_P - 2);"),
      ("(t == int'(TDM_FRAME_PAIRS_P) - 1) ? tdm_pair_w",
       "(t == int'(TDM_FRAME_PAIRS_P) - 2) ? tdm_pair_w")]),
    ("RM3 walk snapshot one cycle late (on slot 0's inject edge)",
     [("wire tdm_snap_w = (st_r == CM_POP_S) && (32'(pop_idx_r) == LB_PAIRS_C);",
       "wire tdm_snap_w = (st_r == CM_STEP_S) && (slot_r == '0);")]),
    ("RM4 closing pair not bypassed: FRAME copies STAGE only (last pair one frame old)",
     [("(t == int'(TDM_FRAME_PAIRS_P) - 1) ? tdm_pair_w",
       "1'b0 ? tdm_pair_w")]),
]


def run(cmd, cwd, log):
    with open(log, "w") as fh:
        rc = subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT, check=False).returncode
        fh.write(f"\nrc={rc}\n")
    return rc


def verdict(log: Path, rc: int) -> str:
    text = log.read_text()
    fails = [l.strip() for l in text.splitlines() if "[FAIL]" in l or "[FAIL " in l or l.strip().startswith("[FAIL")]
    tally = [l.strip() for l in text.splitlines() if "failures" in l]
    return f"rc={rc} fail_lines={len(fails)} tally={tally[-2:] if tally else 'none'}"


def main() -> int:
    clone, work, out = (Path(a).resolve() for a in sys.argv[1:4])
    rtl = clone / "hdl/ieee1722/aaf/KL_chan_map_capture.sv"
    cc = clone / "tb/verilator/capture_coherence"
    chm_src = clone / "tb/verilator/chmap_capture"
    chm = clone / "tb/verilator/r395_probe_chmap"
    if chm.exists():
        shutil.rmtree(chm)
    shutil.copytree(chm_src, chm, ignore=shutil.ignore_patterns("obj_dir", "obj_net"))
    out.mkdir(parents=True, exist_ok=True)
    summary = []
    for i, (name, edits) in enumerate(MUTANTS, 1):
        src = rtl.read_text()
        for pat, rep in edits:
            n = src.count(pat)
            if n != 1:
                summary.append(f"{name}: pattern count {n} != 1 - NOT APPLIED")
                break
            src = src.replace(pat, rep)
        else:
            d = work / f"rm{i}"
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)
            m = d / "KL_chan_map_capture.sv"
            m.write_text(src)
            (out / f"rm{i}.diff").write_text(subprocess.run(
                ["diff", "-u", str(rtl), str(m)], capture_output=True, text=True).stdout)
            jlog = out / f"rm{i}-junction.log"
            #: the suite's "run" target prefixes ./ to MDIR, so build through the
            #: recipe and run the executable here
            jrc = run(["bash", "-c", f"make build CMAP_SRC={m} MDIR={d / 'obj_j'} && "
                       f"{d / 'obj_j' / 'Vcoherence_sim'}"], cc, jlog)
            shutil.rmtree(chm / "obj_dir", ignore_errors=True)
            srcs = (f"{m} ../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv "
                    "../../../hdl/ieee1722/aaf/KL_tone_gen.sv chmap_wrap.sv")
            clog = out / f"rm{i}-chmap_capture.log"
            crc = run(["bash", "-c", f"make obj_dir/Vchmap_wrap SRCS='{srcs}' && ./obj_dir/Vchmap_wrap"], chm, clog)
            summary.append(f"{name}\n    junction: {verdict(jlog, jrc)}\n    chmap_capture: {verdict(clog, crc)}")
    shutil.rmtree(chm)
    text = "\n".join(summary) + "\n"
    (out / "SUMMARY.txt").write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
