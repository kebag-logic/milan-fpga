#!/usr/bin/env python3
"""Build disposable probe copies of the gptp_shadow suite for PR #1016 round 2.

Usage: python3 -I make_probes.py <repo-at-exact-head> <probe-root> <old-generator-file>

Each probe is a copy of the files `make run` reads (hdl/, gptp-processor/hdl,
third_party/verilog-axis/rtl, tb/common, tb/verilator/gptp_shadow),
with at most one plant.
Every probe also prints each graded pair's offsets (instrumentation only;
no check is changed). The source checkout is only read.
"""
import shutil
import sys
from pathlib import Path

REPO, ROOT, OLDGEN = (Path(a) for a in sys.argv[1:4])
SM = "tb/verilator/gptp_shadow/sim_main.cpp"
BK = "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
GEN = "gptp-processor/hdl/ucode/gen_gptp_ucode.py"
GRADED = "    gm_pair(m, D_NOM - used_delay(d) + kGradedOffsetNs);\n"
BANK = "        pub_offset_o    <= pub_offset_raw_w;\n"
INSTR_OLD = "    const int32_t after = static_cast<int32_t>(dut->pub_offset_o);\n"
INSTR_NEW = INSTR_OLD + (
    '    std::printf("PROBE %s before=%d after=%d delta=%d\\n", tag.c_str(), '
    "before, after, after - before);\n")

PROBES = {
    "p0_instr": [],
    "p1_stale_bank": [(BK, BANK, "        pub_offset_o    <= pub_offset_o;\n")],
    "p2_unsent": [(SM, GRADED, "")],
    "p3_oldgen": ["OLDGEN"],
    "p4_stale_on_negative": [(BK, BANK,
        "        pub_offset_o    <= pub_pdelay_raw_w[31] ? pub_offset_o : pub_offset_raw_w;\n")],
    "p5_wrong_sign": [(SM, GRADED,
        "    gm_pair(m, D_NOM - used_delay(d) - kGradedOffsetNs);\n")],
    "p6_used_as_zero": [(SM, GRADED,
        "    gm_pair(m, D_NOM - (d < 0 ? 0 : used_delay(d)) + kGradedOffsetNs);\n")],
}


def sub(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    assert text.count(old) == 1, (path, old)
    path.write_text(text.replace(old, new))


def main() -> int:
    for name, plants in PROBES.items():
        d = ROOT / name
        assert not d.exists(), f"{d} exists; use a fresh probe root"
        (d / "tb/verilator").mkdir(parents=True)
        shutil.copytree(REPO / "hdl", d / "hdl", symlinks=True)
        shutil.copytree(REPO / "gptp-processor/hdl", d / "gptp-processor/hdl", symlinks=True)
        shutil.copytree(REPO / "third_party/verilog-axis/rtl",
                        d / "third_party/verilog-axis/rtl", symlinks=True)
        shutil.copytree(REPO / "tb/common", d / "tb/common", symlinks=True)
        shutil.copytree(REPO / "tb/verilator/gptp_shadow", d / "tb/verilator/gptp_shadow",
                        symlinks=True,
                        ignore=shutil.ignore_patterns("obj_dir", "gptp_ucode.hex", "__pycache__"))
        sub(d / SM, INSTR_OLD, INSTR_NEW)
        for plant in plants:
            if plant == "OLDGEN":
                shutil.copyfile(OLDGEN, d / GEN)
            else:
                sub(d / plant[0], plant[1], plant[2])
        print("probe", name, "planted", len(plants))
    return 0


if __name__ == "__main__":
    sys.exit(main())
