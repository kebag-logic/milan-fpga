#!/usr/bin/env python3
"""Reviewer probe C for FPGA-gPTP #75 / PR #76 round 2 (reconciliation).

Exports the exact head and adds one directed scenario to
tb/verilator/engine/sim_main.cpp, after the round-2 idle GM-change arm, while
the level is inactive and the port is an ordinary tracking slave:

  C: Pdelay responses go bad on the wire until asCapable drops, capability
     recovers through good exchanges, the same GM is announced, and two
     in-band pairs are consumed. The level must stay low with no edge.

Usage: python3 make_probe_tree_r2.py <clone> <out-dir>
Then:  PATH=<verilator dir>:$PATH python3 probe_mutants.py --tree <out-dir> \
           --work <scratch> --set control
       PATH=<verilator dir>:$PATH python3 probe_r2.py --tree <out-dir> \
           --work <scratch> --set reviewer --jobs 2
"""
import io
import subprocess
import sys
import tarfile
from pathlib import Path

HEAD = "4a897e44243d39945df763d00b96049363a58e78"

C_AFTER = ('    slew_probe("slew: second pair after idle GM change stays inactive",'
           ' 0, false);\n')
C_ADD = '''    // [R305 probe C] asCapable loss and recovery while inactive
    {
      const size_t c_edges = slew_edges.size();
      pd_mode = PD_FAR;
      expect("r305c: bad delay drops asCapable while inactive",
             wait_flags(FL_ASCAP, 0, 2500000), 1);
      expect("r305c: inactive asCapable loss stays inactive", dut->phc_slew_active_o, 0);
      printf("R305C flags after loss: 0x%x\\n", dut->pub_flags_o);
      pd_mode = PD_NORMAL;
      expect("r305c: capability recovers",
             wait_flags(FL_ASCAP, FL_ASCAP, 5000000), 1);
      printf("R305C flags after recovery: 0x%x\\n", dut->pub_flags_o);
      announce(0x75C0, 100, GMID + 2, 0, PEER_CID);
      expect("r305c: slave again after recovery", dut->pub_flags_o & FL_AMGM, 0);
      expect("r305c: recovery leaves the level low", dut->phc_slew_active_o, 0);
      expect("r305c: loss and recovery make no level edge", slew_edges.size(), c_edges);
      slew_probe("r305c: in-band pair after asCapable recovery stays inactive",
                 0, false, false, true);
      slew_probe("r305c: second in-band pair after recovery stays inactive", 0, false);
    }
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
    assert s.count(C_AFTER) == 1, C_AFTER
    p.write_text(s.replace(C_AFTER, C_AFTER + C_ADD))
    print(f"probe tree ready: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
