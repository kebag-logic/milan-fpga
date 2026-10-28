#!/usr/bin/env python3
"""Insert a reviewer probe at the end of phase 42 in <tree>'s harness: the
sync-ok fall is carried by a commit (sampled at pub_commit_o) naming the
priority1 255 grandmaster, and usable Sync resumed afterwards raises sync-ok
again with that grandmaster still elected. Prints are prefixed R719P3."""
import sys
from pathlib import Path
f = Path(sys.argv[1]) / "tb/verilator/engine/sim_main.cpp"
t = f.read_text()
anchor = ("               (dut->pub_flags_o & (3 | FL_SYNCOK)) == FL_PRESENT, 1);\n  }\n")
assert t.count(anchor) == 1
probe = anchor[:-4] + r"""    {
      bool fall_committed = false;
      for (size_t i = c0; i < commit_snaps.size(); i++)
        if (commit_snaps[i].gm == G255 &&
            (commit_snaps[i].flags & (3 | FL_SYNCOK)) == FL_PRESENT &&
            commit_snaps[i].cyc <= cyc) {
          fall_committed = true;
          std::printf("R719P3 first commit carrying the fall: %llu cycles after c0 window, flags=%x\n",
                      (unsigned long long)(commit_snaps[i].cyc), commit_snaps[i].flags);
          break;
        }
      const size_t c1 = commit_snaps.size();
      for (int k = 0; k < 8; k++)
        s39_interval(SyncShape::usable, 250000, false, 1000, S255);
      bool rise_committed = false;
      for (size_t i = c1; i < commit_snaps.size(); i++)
        if (commit_snaps[i].gm == G255 && (commit_snaps[i].flags & FL_SYNCOK)) rise_committed = true;
      std::printf("R719P3 after 1 s of resumed usable Sync flags=%x gm=%016llx\n",
                  dut->pub_flags_o, (unsigned long long)dut->pub_gm_id_o);
      expect("R719P3 the sync-ok fall is committed", fall_committed, 1);
      expect("R719P3 resumed usable Sync raises sync-ok again with the peer elected",
             rise_committed && dut->pub_gm_id_o == G255 &&
                 (dut->pub_flags_o & (3 | FL_SYNCOK)) == (FL_PRESENT | FL_SYNCOK), 1);
    }
  }
"""
f.write_text(t.replace(anchor, probe))
print("probe inserted")
