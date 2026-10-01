#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (R419-2): is a GET_STREAM_INFO served inside a
GET_DYNAMIC_INFO serialized against an ACMP step of the same sink, as the
stand-alone GET_STREAM_INFO is (HZ6)?

The classifier comment (protocol_processor_top.sv, hz_classify banner) says a
GET_DYNAMIC_INFO takes the NONE key because "no ACMP step writes a field
either serves". A GET_STREAM_INFO record of a STREAM_INPUT reads the
listener's binding record, which ACMP listener steps write.

Adds arms to section HZ of a SCRATCH copy of tb/pp_top/sim_main.cpp (never the
reviewed checkout) and runs --hazards-only.

  R419-G0  control: a stand-alone GET_STREAM_INFO STREAM_INPUT 1 waits for a
           held ACMP UNBIND_RX of sink 1 (what HZ6 grades).
  R419-G1  a GET_DYNAMIC_INFO carrying one GET_STREAM_INFO record for
           STREAM_INPUT 1, beside the same held UNBIND_RX: printed as
           admitted beside or waited; answer status printed.
  R419-G2  the same GET_DYNAMIC_INFO beside a held GET_RX_STATE (two reads,
           control).

Usage: probe_gdi_stream_info.py <scratch tree root> <verilator>
"""
import pathlib
import subprocess
import sys

ANCHOR = ("    hz12_a_stream_named_by_another_class_conflicts_with_its_read();\n"
          "  }\n")

PROBE = r'''
  //! one GET_DYNAMIC_INFO record: GET_STREAM_INFO of {ty, ix}
  static std::vector<uint8_t> gdi_stri(uint16_t ty, uint16_t ix) {
    std::vector<uint8_t> r(8, 0);
    putbe(&r[0], 4, 2);                        // four bytes of command data
    putbe(&r[6], 0x000F, 2);                   // GET_STREAM_INFO
    const auto d = ti(ty, ix);
    r.insert(r.end(), d.begin(), d.end());
    return r;
  }
  //! like beside_or_after, but only REPORTS the relation
  void r419_relation(uint8_t msg, uint16_t uid, uint16_t op,
                     const std::vector<uint8_t>& pl, const char* what) {
    const Held a = hold_acmp(msg, uid);
    const uint16_t s = seq++;
    (void)send_aecp(0, op, pl, s);
    io.idle(500);
    const auto* b = aecp_adm_after(a.adm);
    const bool held_now = io.d->dbg_acmp_sb_active_o != 0;
    const bool beside = b != nullptr && held_now;
    const long refused = io.hz_aecp_refused;
    const unsigned cls = b ? b->cls : 99u;
    const unsigned key = b ? b->key : 0u;
    release_mac();
    long first = -1;
    const auto r = aecp_answer(s, 40, &first);
    printf("%s: %s (ACMP still held %d, refused %ld clocks, class %u key 0x%04x)"
           ", answer status %d, %zu bytes\n", what,
           beside ? "ADMITTED BESIDE" : "WAITED", int(held_now), refused, cls,
           key, status(r), r.size());
  }
  void r419_gdi_probe() {
    r419_relation(8, 1, 0x000F, ti(DT_SI, 1),
        "R419-G0 stand-alone GET_STREAM_INFO STREAM_INPUT 1 vs a held UNBIND_RX of sink 1");
    r419_relation(8, 1, 0x004B, gdi_stri(DT_SI, 1),
        "R419-G1 GET_DYNAMIC_INFO{GET_STREAM_INFO STREAM_INPUT 1} vs a held UNBIND_RX of sink 1");
    r419_relation(10, 1, 0x004B, gdi_stri(DT_SI, 1),
        "R419-G2 GET_DYNAMIC_INFO{GET_STREAM_INFO STREAM_INPUT 1} vs a held GET_RX_STATE of sink 1");
  }
'''


def main() -> int:
    root = pathlib.Path(sys.argv[1])
    verilator = sys.argv[2]
    sim = root / "tb/pp_top/sim_main.cpp"
    text = sim.read_text()
    if text.count(ANCHOR) != 1:
        print("anchor not unique", file=sys.stderr)
        return 2
    text = text.replace(ANCHOR,
                        "    hz12_a_stream_named_by_another_class_conflicts_"
                        "with_its_read();\n    r419_gdi_probe();\n  }\n" + PROBE,
                        1)
    sim.write_text(text)
    tb = root / "tb/pp_top"
    subprocess.run(["make", "gsi-build", f"VERILATOR={verilator}"], cwd=tb,
                   check=True, stdout=subprocess.DEVNULL)
    r = subprocess.run(["./obj_dir/Vpp_top_sim", "--hazards-only"], cwd=tb,
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
