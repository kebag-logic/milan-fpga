#!/usr/bin/env python3
"""Arm-independence variants of the round-2 head harness (reviewer probe).

Each variant is a git-archive export of the head with one or more of the new
inactive-direction arms deleted from tb/verilator/engine/sim_main.cpp, so a
mutant run shows which arm still catches the defect on its own.

  no_idle:        delete the idle Sync-timeout arm (keep idle GM change)
  no_idle_no_gm:  delete the idle Sync-timeout and idle GM-change arms

Usage: python3 make_arm_variants.py <clone> <out-root>
Then:  python3 probe_mutants.py --tree <out-root>/<variant> --work <w> \
           --set reviewer --only R01,R06 --jobs 2
"""
import io
import subprocess
import sys
import tarfile
from pathlib import Path

HEAD = "4a897e44243d39945df763d00b96049363a58e78"

IDLE = '''    run_svc(800000); // 400 ms exceeds the 375 ms Sync receipt watch
    expect("slew: idle timeout clears sync-ok", dut->pub_flags_o & FL_SYNCOK, 0);
    expect("slew: idle timeout stays asCapable", dut->pub_flags_o & FL_ASCAP, FL_ASCAP);
    expect("slew: idle timeout stays inactive", dut->phc_slew_active_o, 0);
    expect("slew: idle timeout has no level edge", slew_edges.size(), idle_edges);
    expect("slew: idle timeout leaves the rate alone", adj_seen.size(), idle_rates);
    slew_probe("slew: in-band pair after idle timeout stays inactive", 0, false);
    slew_probe("slew: second pair after idle timeout stays inactive", 100, false);
'''
GM = '''    announce(0x7506, 100, GMID + 2, 0, PEER_CID);
    expect("slew: idle GM change selects the new identity", dut->pub_gm_id_o, GMID + 2);
    expect("slew: idle GM change clears sync-ok", dut->pub_flags_o & FL_SYNCOK, 0);
    expect("slew: idle GM change stays slave", dut->pub_flags_o & FL_AMGM, 0);
    expect("slew: idle GM change stays inactive", dut->phc_slew_active_o, 0);
    expect("slew: idle GM change has no level edge", slew_edges.size(), idle_edges);
    slew_probe("slew: in-band pair after idle GM change stays inactive", -100, false);
    slew_probe("slew: second pair after idle GM change stays inactive", 0, false);
'''
KEEP_ANNOUNCE = '''    announce(0x7506, 100, GMID + 2, 0, PEER_CID);
    (void)idle_rates;
'''

VARIANTS = {
    "no_idle": [(IDLE, "    (void)idle_rates;\n")],
    # keep the identity change itself so later announces keep their meaning,
    # but drop every check and the in-band pairs behind it
    "no_idle_no_gm": [(IDLE, ""), (GM, KEEP_ANNOUNCE)],
}


def main() -> int:
    clone, root = Path(sys.argv[1]), Path(sys.argv[2])
    data = subprocess.run(["git", "-C", str(clone), "archive", HEAD],
                          check=True, capture_output=True).stdout
    for name, edits in VARIANTS.items():
        out = root / name
        out.mkdir(parents=True, exist_ok=False)
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            tf.extractall(out, filter="data")
        p = out / "tb/verilator/engine/sim_main.cpp"
        s = p.read_text()
        for old, new in edits:
            assert s.count(old) == 1, (name, old[:60])
            s = s.replace(old, new)
        p.write_text(s)
        print(f"variant ready: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
