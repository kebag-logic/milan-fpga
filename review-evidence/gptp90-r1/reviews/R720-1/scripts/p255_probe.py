#!/usr/bin/env python3
"""Plant a reviewer-only observation phase at the end of the engine suite's
priority1-255 pass of TREE (a disposable copy): a better peer whose
grandmaster also has priority1 255 (802.1AS-2011 gmPresent FALSE) keeps
announcing every second and never sends Sync. Prints the published flags
and grandmaster after each Announce. Usage: p255_probe.py TREE"""
import sys
from pathlib import Path
f = Path(sys.argv[1]) / "tb/verilator/engine/sim_main.cpp"
s = f.read_text()
anchor = ("    end_every_peer_path_with_thisclock();\n  }\n\n"
          "  //! The shipping passes")
assert s.count(anchor) == 1
probe = '''
  void r720_p255_peer_without_sync() {
    pd_mode = PD_NORMAL;
    const bool m = wait_flags(FL_AMGM | FL_ASCAP, FL_AMGM | FL_ASCAP,
                              12000000ull);
    printf("R720 start master=%d flags=%x\\n", m,
           static_cast<unsigned>(dut->pub_flags_o));
    const uint64_t G = 0x0000000000000101ull, S = 0x0000000000000102ull;
    // one usable Sync/Follow_Up pair from S while master: at head it
    // clears any aged mark an earlier phase left, so the peer below is
    // judged on its own (at base a master ignores it)
    sync_pair(0x9200, phc() + 1000, phc() + 1000, S);
    run_svc(20000);
    printf("R720 after pair: flags=%x\\n",
           static_cast<unsigned>(dut->pub_flags_o));
    for (int k = 0; k < 6; k++) {
      announce(static_cast<uint16_t>(0x9100 + k), 255, G, 0, S);
      printf("R720 announce %d: flags=%x gm=%016llx\\n", k,
             static_cast<unsigned>(dut->pub_flags_o),
             static_cast<unsigned long long>(dut->pub_gm_id_o));
      run_svc(2000000);
      printf("R720 +1s %d: flags=%x gm=%016llx\\n", k,
             static_cast<unsigned>(dut->pub_flags_o),
             static_cast<unsigned long long>(dut->pub_gm_id_o));
    }
  }
'''
s = s.replace(anchor, "    end_every_peer_path_with_thisclock();\n"
              "    r720_p255_peer_without_sync();\n  }\n" + probe +
              "\n  //! The shipping passes")
f.write_text(s)
print("planted")
