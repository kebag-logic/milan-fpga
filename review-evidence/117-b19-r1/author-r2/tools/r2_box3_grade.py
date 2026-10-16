"""Lane B19 round 2: grade every box 3 transition edge against the stated time-base model; no bench access.

usage: r2_box3_grade.py <packet-root>              grade; writes round2/box3-grade.{json,md}; rc 1 on any FAIL
       r2_box3_grade.py <packet-root> --selftest   planted controls only; rc 1 unless every control behaves

Inputs: bench/cycleNN/correlation.json (sample brackets at the PHC read, wire times, both on the tap
clock) and round2/box3-model.json (r2_box3_model.py: d_lo, d_hi, u per action).

Criterion (#117 box 3, REQ-PTP-07): a sample's publication words were read at r = p - d - e, with
d in [d_lo, d_hi] and |e| <= u. An edge observed between sample a (old value) and sample b (new
value) happened in (r_a, r_b]. Its wire cause c must lie in that interval for EVERY admissible d
and e, with no processing allowance:
  lower margin  c - (a - d_lo + u_a)  > 0    the cause is after the last read that still showed the old value
  upper margin  (b - d_hi - u_b) - c >= 0    the cause is not after the first read that showed the new value
The first `tu=1` CRF PDU is an effect of the CLKV_STAT[0] rise, not a cause: it may follow the
rise by up to one PDU period, so its upper margin adds 2 ms (500 PDU/s).

Graded edges per cycle: sync loss (cause: the switch's last Sync + 0.375 s, the sync receipt
timeout of docs/design/GM_LOSS_RECOVERY.md "Recovery bound"), grandmaster loss (last Announce +
3 s, the announce receipt timeout), asCapable return (the DUT's second completed Pdelay exchange),
grandmaster return (the switch's Announce the DUT adopted: the last one at or before the latest
admissible read of the first sample naming the switch), and in cycles 1 to 3 the first `tu=1` CRF
PDU. That is 27 edges. asCapable loss and `tu` clear have no single wire instant as cause and
are reported as ranges under the same model.
"""
from pathlib import Path
import copy, json, sys

SWITCH, DUT = "3cc0c6fffefe0210", "020000fffe000001"
SYNC_TO, ANN_TO, PDU = 0.375, 3.0, 0.002
NEAR = 0.025


def u_of(m, how):
    return m["u_phc_s"] if how == "phc" else m["u_cal_s"]


def grade_edge(kind, br, c, m, effect=False):
    a, b = br["last_before"], br["first_after"]
    ua, ub = u_of(m, br["how"][0]), u_of(m, br["how"][1])
    lo = c - (a - m["d_lo_s"] + ua)
    hi = (b - m["d_hi_s"] - ub) - c + (PDU if effect else 0.0)
    ok = lo > 0 and hi >= 0
    return dict(edge=kind, cause_s=round(c, 4), last_before_s=a, first_after_s=b, how=br["how"],
                lower_margin_ms=round(1e3 * lo, 2), upper_margin_ms=round(1e3 * hi, 2),
                d0_lower_ms=round(1e3 * (c - a), 2), d0_upper_ms=round(1e3 * (b - c), 2),
                verdict="PASS" if ok else "FAIL", near=min(lo, hi) < NEAR)


def cycle_edges(i, c, m):
    E, W = c["edges"], c["wire"]
    first = lambda f, to: next(e for e in E[f] if str(e["to"]) == str(to))
    last = lambda f, to: [e for e in E[f] if str(e["to"]) == str(to)][-1]
    out = []
    sb = first("sync", 0)
    out.append(grade_edge("sync loss", sb, W["switch_last_sync"] + SYNC_TO, m))
    out.append(grade_edge("grandmaster loss", first("gm", DUT), W["switch_last_announce"] + ANN_TO, m))
    out.append(grade_edge("asCapable return", last("asCapable", 1), W["dut_completed_pdelay_after_return"][1], m))
    gb = last("gm", SWITCH)
    latest = gb["first_after"] - m["d_lo_s"] + u_of(m, gb["how"][1])
    acc = [x[0] for x in W["switch_announces_after_return"] if x[0] <= latest]
    out.append(grade_edge("grandmaster return", gb, acc[-1] if acc else float("inf"), m))
    if i <= 3:
        crf = next(x for x in W["crf_tu_edges"] if x["to"] == 1)
        out.append(grade_edge("first tu=1 CRF PDU", first("tu", 1), crf["first_after"], m, effect=True))
    same = all(first(f, v)["last_before"] == sb["last_before"] for f, v in (("tu", 1), ("holdover", 1)))
    for e in out:
        e["cycle"] = i
    ranges = dict(cycle=i, sync_tu_holdover_same_bracket=same)
    ab = first("asCapable", 0)
    ranges["asCapable_loss_after_last_resp_s"] = [round(ab["last_before"] - m["d_hi_s"] - u_of(m, ab["how"][0]) - W["switch_last_pdelay_resp"], 3),
                                                  round(ab["first_after"] - m["d_lo_s"] + u_of(m, ab["how"][1]) - W["switch_last_pdelay_resp"], 3)]
    tb = last("tu", 0)
    # tu clear follows the adoption commit; its holdover is bounded by the two brackets.
    ranges["holdover_after_adoption_s"] = [round((tb["last_before"] - m["d_hi_s"]) - (gb["first_after"] - m["d_lo_s"]), 3),
                                           round((tb["first_after"] - m["d_lo_s"]) - (gb["last_before"] - m["d_hi_s"]), 3)]
    ranges["holdover_at_least_0_25_consistent"] = ranges["holdover_after_adoption_s"][1] >= 0.25
    gm_first = (gb["first_after"] - m["d_hi_s"] - u_of(m, gb["how"][1]), gb["first_after"] - m["d_lo_s"] + u_of(m, gb["how"][1]))
    ranges["gm_return_first_read_after_announce_s"] = [round(gm_first[0] - acc[-1], 3), round(gm_first[1] - acc[-1], 3)] if acc else None
    ranges["sync_loss_reads_after_last_sync_s"] = [round(sb["last_before"] - m["d_hi_s"] - W["switch_last_sync"], 3),
                                                   round(sb["first_after"] - m["d_lo_s"] - W["switch_last_sync"], 3)]
    g0 = first("gm", DUT)
    ranges["gm_loss_reads_after_last_announce_s"] = [round(g0["last_before"] - m["d_hi_s"] - W["switch_last_announce"], 3),
                                                     round(g0["first_after"] - m["d_lo_s"] - W["switch_last_announce"], 3)]
    return out, ranges


def grade(pkt):
    model = json.loads((pkt / "round2" / "box3-model.json").read_text())
    edges, ranges = [], []
    for i in range(1, 7):
        name = f"cycle{i:02d}"
        c = json.loads((pkt / "bench" / name / "correlation.json").read_text())
        e, r = cycle_edges(i, c, model["actions"][name])
        edges += e
        ranges.append(r)
    return model, edges, ranges


def selftest(pkt):
    """Planted controls on copies of cycle 3: each must give the stated verdict."""
    model = json.loads((pkt / "round2" / "box3-model.json").read_text())
    m = model["actions"]["cycle03"]
    base = json.loads((pkt / "bench" / "cycle03" / "correlation.json").read_text())
    br = next(e for e in base["edges"]["sync"] if str(e["to"]) == "0")
    lo_edge = br["last_before"] - m["d_lo_s"] + m["u_phc_s"]
    hi_edge = br["first_after"] - m["d_hi_s"] - m["u_phc_s"]
    checks = []
    us = 1e-6
    for label, c, want in (("cause 1 us after the latest old read", lo_edge + us, "PASS"),
                           ("cause 1 us before the latest old read", lo_edge - us, "FAIL"),
                           ("cause 1 us before the earliest new read", hi_edge - us, "PASS"),
                           ("cause 1 us after the earliest new read", hi_edge + us, "FAIL"),
                           ("cause inside at d = 0 but after the earliest new read under the model", br["first_after"] - 1e-3, "FAIL"),
                           ("cause 5 ms before the last old PHC read, which the offset moves inside", br["last_before"] - 5e-3, "PASS")):
        checks.append((label, grade_edge("planted", br, c, m)["verdict"], want))
    for label, c, want in (("effect PDU 1 us inside one PDU period after the earliest new read", hi_edge + PDU - us, "PASS"),
                           ("effect PDU 1 us beyond one PDU period", hi_edge + PDU + us, "FAIL")):
        checks.append((label, grade_edge("planted", br, c, m, effect=True)["verdict"], want))
    # Planted wire causes in the real input, each moved just past its own margin, must turn the grade to FAIL.
    real, _ = cycle_edges(3, base, m)
    marg = {x["edge"]: x for x in real}
    mut = copy.deepcopy(base)
    mut["wire"]["switch_last_announce"] += marg["grandmaster loss"]["upper_margin_ms"] / 1e3 + 1e-4
    e, _ = cycle_edges(3, mut, m)
    checks.append(("cycle 3 last Announce moved 0.1 ms past its upper margin", next(x for x in e if x["edge"] == "grandmaster loss")["verdict"], "FAIL"))
    mut = copy.deepcopy(base)
    mut["wire"]["dut_completed_pdelay_after_return"][1] -= marg["asCapable return"]["lower_margin_ms"] / 1e3 + 1e-4
    e, _ = cycle_edges(3, mut, m)
    checks.append(("cycle 3 second Pdelay exchange moved 0.1 ms past its lower margin", next(x for x in e if x["edge"] == "asCapable return")["verdict"], "FAIL"))
    mut = copy.deepcopy(base)
    mut["wire"]["switch_last_sync"] += marg["sync loss"]["upper_margin_ms"] / 1e3 + 1e-4
    e, _ = cycle_edges(3, mut, m)
    checks.append(("cycle 3 last Sync moved 0.1 ms past its upper margin", next(x for x in e if x["edge"] == "sync loss")["verdict"], "FAIL"))
    mut = copy.deepcopy(base)
    for x in mut["wire"]["crf_tu_edges"]:
        if x["to"] == 1:
            x["first_after"] = br["last_before"] - 0.020
    e, _ = cycle_edges(3, mut, m)
    checks.append(("cycle 3 first tu=1 PDU planted before the bracket", next(x for x in e if x["edge"] == "first tu=1 CRF PDU")["verdict"], "FAIL"))
    tight = copy.deepcopy(m)
    tight["d_lo_s"] = 0.0
    e, _ = cycle_edges(3, base, tight)
    checks.append(("cycle 3 with no read-to-PHC offset (d_lo = 0): the grandmaster return fails", next(x for x in e if x["edge"] == "grandmaster return")["verdict"], "FAIL"))
    bad = 0
    for label, got, want in checks:
        print(f"{'ok ' if got == want else 'BAD'} {want:4} got {got:4}  {label}")
        bad += got != want
    print(f"selftest: {len(checks) - bad} of {len(checks)} controls behave")
    return 1 if bad else 0


def main():
    pkt = Path(sys.argv[1])
    if sys.argv[2:] == ["--selftest"]:
        return selftest(pkt)
    model, edges, ranges = grade(pkt)
    fails = [e for e in edges if e["verdict"] == "FAIL"]
    near = sorted((e for e in edges if e["near"]), key=lambda e: min(e["lower_margin_ms"], e["upper_margin_ms"]))
    res = dict(criterion="cause in (r_a, r_b] for every admissible d and e; first tu=1 PDU may trail by one PDU period",
               edges_graded=len(edges), passed=len(edges) - len(fails), failed=len(fails),
               verdict="PASS" if not fails else "FAIL", edges=edges, near_boundary=[(e["cycle"], e["edge"]) for e in near], ranges=ranges)
    rows = ["| Cycle | Edge | Cause (s) | Bracket at the PHC read (s) | Placement | Lower margin (ms) | Upper margin (ms) | Margins at d = 0 (ms) | Grade |",
            "|---:|---|---:|---|---|---:|---:|---|---|"]
    for e in edges:
        rows.append(f"| {e['cycle']} | {e['edge']} | {e['cause_s']:.4f} | {e['last_before_s']:.4f} to {e['first_after_s']:.4f} | "
                    f"{'/'.join(e['how'])} | {e['lower_margin_ms']:.2f} | {e['upper_margin_ms']:.2f} | "
                    f"{e['d0_lower_ms']:.1f} / {e['d0_upper_ms']:.1f} | {e['verdict']}{' (near)' if e['near'] else ''} |")
    md = "\n".join(rows) + f"\n\n{res['passed']} of {res['edges_graded']} edges PASS; {len(near)} lie within 25 ms of a bracket boundary.\n"
    (pkt / "round2" / "box3-grade.json").write_text(json.dumps(res, indent=1) + "\n")
    (pkt / "round2" / "box3-grade.md").write_text(md)
    print(md)
    for r in ranges:
        print(json.dumps(r))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
