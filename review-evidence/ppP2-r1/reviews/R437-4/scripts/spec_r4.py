# R437-4 independent probes on round 4's tests (run through probe.py).
#  W10, W11, W12, W15: owed_left_r narrowed to 10, 11, 12 and 15 bits. At the
#      suite's MAX_PAYLOAD_P = 1024 a READ owes at most 1,024 payload bytes, so
#      W11 and wider fit it there; only a build at a larger MAX_PAYLOAD_P (the
#      randomized harness, at 65,527) can grade 11 to 15 bits.
#  B14: the owed command's kind taken without the request states, so a READ
#      granted late is not drained at all (the late-grant branch, under-drain).
#  B15: the drain not bounded by the count (round 2's drain): over-drain in
#      every branch.
#  LEGAL: the head under the seven legal device models at 20, 21, 37, 100,
#      1,000 and 4,096; the head's randomized harness at further bounds.
DECL = "  logic       [15:0] owed_left_r;   // ...as many as it still owes"
RDST = ("  assign rd_st_w  = (state_r == S_RHREQ) || (state_r == S_RHCOLL)\n"
        "                  || (state_r == S_RHWAIT) || (state_r == S_RPREQ)\n"
        "                  || (state_r == S_RPPUMP) || (state_r == S_RPWAIT);\n")
DRAIN = "  assign drain_w = owed_r && owed_rd_r && (owed_left_r != 16'd0);\n"
PROBES = {
    "base": [],
    "W10_count_ten_bits": [("RTL", DECL, "  logic        [9:0] owed_left_r;   // ...as many as it still owes")],
    "W11_count_eleven_bits": [("RTL", DECL, "  logic       [10:0] owed_left_r;   // ...as many as it still owes")],
    "W12_count_twelve_bits": [("RTL", DECL, "  logic       [11:0] owed_left_r;   // ...as many as it still owes")],
    "W15_count_fifteen_bits": [("RTL", DECL, "  logic       [14:0] owed_left_r;   // ...as many as it still owes")],
    "B14_late_grant_not_a_read": [("RTL", RDST,
        "  assign rd_st_w  = (state_r == S_RHCOLL)\n"
        "                  || (state_r == S_RHWAIT)\n"
        "                  || (state_r == S_RPPUMP) || (state_r == S_RPWAIT);\n")],
    "B15_drain_unbounded": [("RTL", DRAIN, "  assign drain_w = owed_r && owed_rd_r;\n")],
}
LEGAL = ("pristine", "half-page", "page-buffered NOR", "lazy erase", "lazy erase + page-buffered",
         "coincident completion", "unsolicited completion")
RUNS = []
for p in PROBES:
    if p == "base":
        continue
    for t in (100, 37, 20):
        RUNS.append((p, "pristine", t))
    for t in (1, 3, 37):
        RUNS.append(("FZ:" + p, "pristine", t))
for m in LEGAL:
    for t in (20, 21, 37, 100, 1000, 4096):
        RUNS.append(("base", m, t))
for t in (1, 2, 3, 5, 19, 37, 100):
    RUNS.append(("FZ:base", "pristine", t))
PROBES.update({"FZ:" + k: v for k, v in list(PROBES.items())})
