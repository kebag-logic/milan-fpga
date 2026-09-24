#!/usr/bin/env python3
"""Build the reviewer's disposable probe tree for FPGA-gPTP #75 finding F1.

Exports the exact head from a clone with `git archive`, then adds two directed
scenarios to tb/verilator/engine/sim_main.cpp (see receipts/r305_probe_harness.diff):
  A: a Sync lapse while the level is inactive, then two in-band pairs -> inactive
  B: correction, mastership, return to slave, two in-band pairs -> inactive

Usage: python3 make_probe_tree.py <clone> <out-dir>
Then:  PATH=<verilator dir>:$PATH python3 probe_mutants.py --tree <out-dir> \
           --work <scratch> --set control
       PATH=<verilator dir>:$PATH python3 probe_mutants.py --tree <out-dir> \
           --work <scratch> --set reviewer --only R01,R02,R06 --jobs 3
"""
import io
import subprocess
import sys
import tarfile
from pathlib import Path

HEAD = "49d23b20fcad15a3c03554476d8b8c9116b3b375"

A_AFTER = '    slew_probe("slew: two fresh pairs complete after timeout", 0, false);\n'
A_ADD = '''    // [R305 probe A] a Sync lapse while inactive must not arm tracking
    run_svc(800000);
    expect("r305: inactive lapse clears sync-ok", dut->pub_flags_o & FL_SYNCOK, 0);
    expect("r305: inactive lapse stays inactive", dut->phc_slew_active_o, 0);
    slew_probe("r305: tracking after an inactive Sync lapse stays inactive", 0, false);
    slew_probe("r305: second tracking pair after lapse stays inactive", 0, false);
'''
B_AFTER = '    expect("slew: no clear precedes the replacement rate", slew_early_clears, 0);\n'
B_ADD = '''    // [R305 probe B] return to slave duty with an in-band first pair
    slew_probe("r305: correction before mastership", -5000, true);
    announce(0x7506, 250, GMID, 0, PEER_CID);
    expect("r305: degraded parent returns to GM", dut->pub_flags_o & FL_AMGM, FL_AMGM);
    expect("r305: mastership retires", dut->phc_slew_active_o, 0);
    run_svc(250000);
    announce(0x7507, 100, GMID, 0, PEER_CID);
    expect("r305: slave again", dut->pub_flags_o & FL_AMGM, 0);
    slew_probe("r305: in-band return pair stays inactive", 0, false);
    slew_probe("r305: second in-band return pair stays inactive", 0, false);
'''


def main() -> int:
    clone, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    data = subprocess.run(["git", "-C", str(clone), "archive", HEAD],
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        tf.extractall(out, filter="data")
    p = out / "tb/verilator/engine/sim_main.cpp"
    s = p.read_text()
    for anchor, add in ((A_AFTER, A_ADD), (B_AFTER, B_ADD)):
        assert s.count(anchor) == 1, anchor
        s = s.replace(anchor, anchor + add)
    p.write_text(s)
    print(f"probe tree ready: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
