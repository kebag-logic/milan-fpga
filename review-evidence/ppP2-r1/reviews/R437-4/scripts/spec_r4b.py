# R437-4 probes of the randomized harness itself (FZ10's reach) and of the two
# broken-device models at further bounds (run through probe.py).
#  H1: babble never abandons at a header byte or a terminal (round 3's draw).
#  H2: no READ of the largest payload is abandoned (one_widest not called).
#  H3: no long record is drawn (long_payload returns at most 24 bytes).
#  Each must fail FZ10 (a branch unexercised) while the port is the head's.
#  BROKEN: the head under the short-read and silent models at 20, 100 and
#  4,096: every RW check must pass (the service checks are expected to fail).
PROBES = {
    "base": [],
    "FZ:H1_babble_payload_only": [("FUZZ",
        "  if (u() < 0.5) {                              // ...or as often a header byte (1-8), the\n",
        "  if (false) {                                  // ...or as often a header byte (1-8), the\n")],
    "FZ:H2_no_widest": [("FUZZ", "    one_widest(good);\n", "")],
    "FZ:H3_no_long_records": [("FUZZ",
        "  return size_t(u() < 0.5 ? top : rnd(std::min(25, top), top));",
        "  return size_t(rnd(0, std::min(24, top)));")],
}
RUNS = [(p, "pristine", t) for p in PROBES if p.startswith("FZ:") for t in (3, 37)]
for m in ("short read", "silent"):
    for t in (20, 100, 4096):
        RUNS.append(("base", m, t))
