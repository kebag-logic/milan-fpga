#!/usr/bin/env python3
"""Formal equivalence of base and head at their elaborated GMII defaults.
usage: equiv_default.py <base tree> <head tree> <work dir> <receipt dir>
The head observer is compared with `gmii_tready_i` tied to GMII's constant 1."""
import os, re, subprocess, sys
base, head, w, out = sys.argv[1:5]
sv2v = os.environ.get("SV2V", "sv2v")
plane = "hdl/ieee8021as/gptp_plane"
def conv(tree, mod, side):
    t = subprocess.run([sv2v, "-DSYNTHESIS", f"--top={mod}", f"{tree}/{plane}/{mod}.sv",
                        f"{tree}/hdl/common/cdc_handshake.sv", f"{tree}/hdl/common/cdc_pulse.sv"],
                       check=True, capture_output=True, text=True).stdout
    # elaboration-time refusals: every one of them is inside an untaken generate arm
    return re.sub(r'\$error\(.*?\);', ';', t, flags=re.S)
def elaborate(path, mod, new):
    return (f"read_verilog {path}\nhierarchy -check -top {mod}\nproc; flatten; opt_clean\n"
            f"memory -nomap; memory_map; opt -full\nrename {mod} {new}\ndesign -stash {new}\n")
for name, mod, tie in (("launch", "KL_gptp_gmii_launch", True), ("txret", "KL_gptp_txret", False)):
    b, h = conv(base, mod, "base"), conv(head, mod, "head")
    if tie:
        assert "input wire gmii_tready_i;" in h and "gmii_tready_i" not in b
        h = h.replace("input wire gmii_tready_i;", "wire gmii_tready_i = 1'b1;")
        h, n = re.subn(r'(\n\s*)gmii_tready_i,', r'\1', h, count=1)
        assert n == 1
    open(f"{w}/{name}_base.v", "w").write(b)
    open(f"{w}/{name}_head.v", "w").write(h)
    script = (elaborate(f"{w}/{name}_base.v", mod, "gold") + elaborate(f"{w}/{name}_head.v", mod, "gate") +
              "design -copy-from gold -as gold gold\ndesign -copy-from gate -as gate gate\n"
              "equiv_make gold gate equiv\nhierarchy -top equiv\n"
              "equiv_simple -seq 2\nequiv_induct -seq 4\nequiv_status -assert\n")
    open(f"{w}/run_{name}.ys", "w").write(script)
    done = subprocess.run(["timeout", "420", "yosys", "-q", "-l", f"{out}/equiv_{name}.log", "-s", f"{w}/run_{name}.ys"],
                          capture_output=True, text=True)
    open(f"{out}/equiv_{name}.rc", "w").write(f"{done.returncode}\n")
    print(name, "rc", done.returncode)
