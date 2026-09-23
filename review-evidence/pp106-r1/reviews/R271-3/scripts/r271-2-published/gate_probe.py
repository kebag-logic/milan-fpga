#!/usr/bin/env python3
"""Discriminating probe checks for the decoder's once-per-MRPDU LeaveAll gate.

Adds three reviewer-owned checks (G1 to G3) to a disposable export's
tb/srp_decoder/sim_main.cpp, plants one mutant from mutants.py (or none), and
runs srp_decoder only. The export is never the clone. Expected strobe
timelines are hand-written constants from 802.1Q-2014 §10.8.1.2 framing and
the once-per-MRPDU rule of docs 10 §6.5, as in the suite itself:

  G1 [L LA JoinIn] [Domain LA n=2] [L LA JoinMt]   -> L3 E3 L4 E4 E4 E3
     (the Listener gate stays closed across another type's message)
  G2 one Listener message [LA JoinIn] [JoinIn] [LA JoinMt] -> L3 E3 E3 E3
     (an unflagged vector does not re-open the gate)
  G3 a Listener-only LeaveAll MRPDU padded to the 46-octet minimum payload,
     fed twice                                     -> L3, then L3 again
     (the gate re-arms after a padded, well-formed MRPDU)

usage: gate_probe.py <clone> <rev> <scratch-dir> <receipt> [mutant-id ...]
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mutants  # noqa: E402  (same directory)

PROBE_DECL = "  void the_gate_re_arms_after_a_malformed_mrpdu();\n"
PROBE_CALL = "  the_gate_re_arms_after_a_malformed_mrpdu();\n\n  printf("
PROBE_BODY = r'''
void SrpDecoderSuite::reviewer_gate_probes() {
  // G1: [L LA JoinIn] [Domain LA n=2] [L LA JoinMt]
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 3); P8(p, 8); P16(p, 14);
  P16(p, 0x2001); P64(p, SIDB + 0x1D0); P8(p, 36); P8(p, 0x80);
  P16(p, 0);
  P8(p, 4); P8(p, 4); P16(p, 9);
  P16(p, 0x2002); P8(p, 5); P8(p, 2); P16(p, 2); P8(p, 126);
  P16(p, 0);
  P8(p, 3); P8(p, 8); P16(p, 14);
  P16(p, 0x2001); P64(p, SIDB + 0x1E0); P8(p, 108); P8(p, 0x80);
  P16(p, 0); P16(p, 0);
  h.feed(p, true);
  check_marks("G1 Listener gate stays closed across a Domain message",
              {{'L', kListener}, {'E', kListener}, {'L', kDomain}, {'E', kDomain},
               {'E', kDomain}, {'E', kListener}});
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "G1 done ok");

  // G2: one Listener message [LA JoinIn] [JoinIn] [LA JoinMt]
  h.clear();
  p.clear();
  P8(p, 0);
  P8(p, 3); P8(p, 8); P16(p, 38);
  P16(p, 0x2001); P64(p, SIDB + 0x2D0); P8(p, 36); P8(p, 0x80);
  P16(p, 0x0001); P64(p, SIDB + 0x2E0); P8(p, 36); P8(p, 0x80);
  P16(p, 0x2001); P64(p, SIDB + 0x2F0); P8(p, 108); P8(p, 0x80);
  P16(p, 0); P16(p, 0);
  h.feed(p, true);
  check_marks("G2 an unflagged vector does not re-open the gate",
              {{'L', kListener}, {'E', kListener}, {'E', kListener}, {'E', kListener}});
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "G2 done ok");

  // G3: padded Listener-only LeaveAll MRPDU (19 octets + 27 pad = 46), twice
  std::vector<uint8_t> q;
  P8(q, 0);
  P8(q, 3); P8(q, 8); P16(q, 12);
  P16(q, 0x2000); P64(q, 0);
  P16(q, 0); P16(q, 0);
  while (q.size() < 46) P8(q, 0);
  for (int n = 0; n < 2; ++n) {
    h.clear();
    h.feed(q, true);
    check_marks(n == 0 ? "G3 padded MRPDU 0" : "G3 padded MRPDU 1 (gate re-armed)",
                {{'L', kListener}});
    CHECK(h.dones.size() == 1 && h.dones[0].ok, "G3 padded MRPDU %d done ok", n);
  }
}

int SrpDecoderSuite::run() {'''


def add_probes(tree: pathlib.Path) -> None:
    """Insert the G1-G3 member into the export's decoder suite, exactly once."""
    path = tree / "tb/srp_decoder/sim_main.cpp"
    text = path.read_text()
    for old in (PROBE_DECL, PROBE_CALL, "\nint SrpDecoderSuite::run() {"):
        if text.count(old) != 1:
            raise ValueError(f"probe anchor matched {text.count(old)} times")
    text = text.replace(PROBE_DECL, PROBE_DECL + "  void reviewer_gate_probes();\n", 1)
    text = text.replace(PROBE_CALL,
                        "  the_gate_re_arms_after_a_malformed_mrpdu();\n"
                        "  reviewer_gate_probes();\n\n  printf(", 1)
    text = text.replace("\nint SrpDecoderSuite::run() {", PROBE_BODY, 1)
    path.write_text(text)


def main() -> int:
    """Run the probe checks against each requested mutant; write a receipt."""
    clone, rev, scratch, receipt = sys.argv[1:5]
    ids = sys.argv[5:] or ["K0", "K5", "K6", "K7", "K8"]
    lines = [f"# gate probes G1-G3 at {rev}", ""]
    for mid in ids:
        desc, edits = mutants.MUTANTS[mid]
        tree = pathlib.Path(scratch) / f"probe-{mid}"
        mutants.export(clone, rev, tree)
        lines.append(f"## {mid}: {desc}")
        lines += ["planted " + s for s in mutants.plant(tree, edits)]
        add_probes(tree)
        suite, status, tally, fails = mutants.run_suite(tree, "srp_decoder")
        lines.append(f"{status} {suite} ({tally})")
        log = (tree / "srp_decoder.log").read_text().splitlines()
        lines += ["    " + ln for ln in log
                  if ln.startswith("FAIL") or ln.startswith("  got") or ln.startswith("  want")]
        lines.append("")
        print(f"{mid}: {status} {tally}", flush=True)
    pathlib.Path(receipt).write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
