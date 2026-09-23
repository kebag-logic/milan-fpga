#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable decoder probe for two edges of the once-per-MRPDU LeaveAll gate
that no suite at fc155c3c exercises. It appends one reviewer test method to a
COPY of tb/srp_decoder/sim_main.cpp inside each given tree (never the review
clone), then builds and runs srp_decoder there.

  U  the layout docs 10 section 6.5 processes in DLSDU order: a vector of type T
     WITHOUT LeaveAllEvent ahead of the first vector of T WITH it, in one
     message, across messages, and for MVRP. Documented result: the unflagged
     vector's events, THEN the lane, then the flagged vector's events.
  A  re-arm after a tolerance discard: an MRPDU that strobes the Listener lane
     and is then malformed, followed by a well-formed Listener LeaveAll MRPDU,
     must strobe the lane again.

Usage: 06_decoder_probe.py <verilator> <out.txt> <tree>...
"""
import pathlib
import re
import subprocess
import sys

PROBE = r'''
// ==== reviewer probe (not part of the PR) ================================
void SrpDecoderSuite::reviewer_probe_gate_edges() {
  // U1: [Listener: v1 LA=0 JoinIn, v2 LA=1 JoinIn] in ONE message
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 3); P8(p, 8); P16(p, 26);
  P16(p, 0x0001); P64(p, SIDB + 0xD00); P8(p, 36); P8(p, 0x80);
  P16(p, 0x2001); P64(p, SIDB + 0xE00); P8(p, 36); P8(p, 0x80);
  P16(p, 0); P16(p, 0);
  h.feed(p, true);
  check_marks("U1 one message", {{'E', kListener}, {'L', kListener}, {'E', kListener}});
  // U2: [Listener LA=0 JoinIn][Domain LA=1 n=1][Listener LA=1 JoinMt]
  h.clear();
  std::vector<uint8_t> q;
  P8(q, 0);
  P8(q, 3); P8(q, 8); P16(q, 14);
  P16(q, 0x0001); P64(q, SIDB + 0xF00); P8(q, 36); P8(q, 0x80);
  P16(q, 0);
  P8(q, 4); P8(q, 4); P16(q, 9);
  P16(q, 0x2001); P8(q, 6); P8(q, 3); P16(q, 2); P8(q, 36);
  P16(q, 0);
  P8(q, 3); P8(q, 8); P16(q, 14);
  P16(q, 0x2001); P64(q, SIDB + 0xF00); P8(q, 108); P8(q, 0x80);
  P16(q, 0); P16(q, 0);
  h.feed(q, true);
  check_marks("U2 across messages", {{'E', kListener}, {'L', kDomain}, {'E', kDomain},
                                     {'L', kListener}, {'E', kListener}});
  // U3: MVRP [VID LA=0 n=1][VID LA=1 n=1]
  h.clear();
  std::vector<uint8_t> r;
  P8(r, 0);
  P8(r, 1); P8(r, 2);
  P16(r, 0x0001); P16(r, 5); P8(r, 36);
  P16(r, 0x2001); P16(r, 9); P8(r, 36);
  P16(r, 0); P16(r, 0);
  h.feed(r, false);
  check_marks("U3 MVRP", {{'E', 1}, {'M', 1}, {'E', 1}});
  // A1: Listener LA strobed, then the MRPDU truncates mid-FirstValue
  h.clear();
  std::vector<uint8_t> a;
  P8(a, 0);
  P8(a, 3); P8(a, 8); P16(a, 14);
  P16(a, 0x2001); P8(a, 0x00); P8(a, 0x11); P8(a, 0x22);   // 3 of 8 FirstValue bytes
  h.feed(a, true);
  CHECK(h.dones.size() == 1 && h.dones[0].mal, "A1 truncated MRPDU is malformed");
  check_marks("A1 lane before the bad field", {{'L', kListener}});
  // A2: the next, well-formed Listener LeaveAll MRPDU strobes the lane again
  h.clear();
  std::vector<uint8_t> b;
  P8(b, 0);
  P8(b, 3); P8(b, 8); P16(b, 12);
  P16(b, 0x2000); P64(b, 0);
  P16(b, 0); P16(b, 0);
  h.feed(b, true);
  check_marks("A2 re-armed after a malformed MRPDU", {{'L', kListener}});
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "A2 done ok");
  // A3: bad AttributeLength after a flagged Listener vector, then a good one
  h.clear();
  std::vector<uint8_t> c;
  P8(c, 0);
  P8(c, 3); P8(c, 8); P16(c, 14);
  P16(c, 0x2001); P64(c, SIDB + 0xA10); P8(c, 36); P8(c, 0x80);
  P16(c, 0);
  P8(c, 4); P8(c, 5);                           // Domain with AttributeLength 5: bad
  P16(c, 0); P16(c, 0); P16(c, 0);
  h.feed(c, true);
  CHECK(h.dones.size() == 1 && h.dones[0].mal, "A3 bad AttributeLength is malformed");
  h.clear();
  h.feed(b, true);
  check_marks("A3 re-armed after a discarded MRPDU", {{'L', kListener}});
}
'''


def patch(sim: pathlib.Path):
    s = sim.read_text()
    if "reviewer_probe_gate_edges" in s:
        return
    s = s.replace("  void check_marks(const char* tag, const std::vector<Mark>& want);\n",
                  "  void check_marks(const char* tag, const std::vector<Mark>& want);\n"
                  "  void reviewer_probe_gate_edges();\n", 1)
    s = s.replace("\nint SrpDecoderSuite::run() {", PROBE + "\nint SrpDecoderSuite::run() {", 1)
    s = s.replace("  a_type_leaves_all_once_per_mrpdu();\n",
                  "  a_type_leaves_all_once_per_mrpdu();\n  reviewer_probe_gate_edges();\n", 1)
    assert s.count("reviewer_probe_gate_edges") == 3, "probe insertion failed"
    sim.write_text(s)


def main():
    vl, out = sys.argv[1], pathlib.Path(sys.argv[2])
    lines = []
    for t in sys.argv[3:]:
        tree = pathlib.Path(t)
        d = tree / "tb" / "srp_decoder"
        patch(d / "sim_main.cpp")
        subprocess.run(["make", "clean"], cwd=d, capture_output=True)
        p = subprocess.run(["make", "VERILATOR=%s" % vl], cwd=d, capture_output=True, text=True)
        log = p.stdout + p.stderr
        (tree / "probe_srp_decoder.log").write_text(log)
        tally = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL", log)
        fails = [ln for ln in log.splitlines()
                 if ln.startswith("FAIL:") and (" U" in ln[5:8] or " A" in ln[5:8])]
        lines.append("%s: %s" % (tree.name, tally[-1] if tally else "NO TALLY rc=%d" % p.returncode))
        lines += ["    " + f for f in fails]
        for ln in log.splitlines():
            if ln.strip().startswith(("got :", "want:")):
                lines.append("      " + ln.strip())
    out.write_text("\n".join(lines) + "\n")
    print(out.read_text(), end="")


if __name__ == "__main__":
    main()
