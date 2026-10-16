"""Lane B19 round 2: the ten software-grandmaster edges re-derived from the hashed raws; no bench access.

usage: r2_gm.py <raw-root> <packet-root>              writes round2/gm-steps-r2.{json,md}; rc 1 on any FAIL
       r2_gm.py <raw-root> <packet-root> --selftest   planted controls only; rc 1 unless every control behaves

Inputs: <raw-root>/gmNN/{events,console,controller}.jsonl and <packet-root>/bench/gmNN/analysis.json
(wire `tu` and `mr` history, counters) with <packet-root>/summary/gm-steps.json (the round-1 grades).

Timestamp convention (#387 item 4, #621 item 3). A console sample is timed at its command-send
time t on the build-box clock, in seconds after the software-grandmaster start; its words were read
between t and the command's completion. An edge first shown by sample k therefore happened in
(t[k-1], end[k]], and is reported at t[k]. Assertion and clear come from the complete transition
history of the run, not from a window chosen around the PHC step: "tu set" is the first sample of
the edge window with `tu` 1 that follows a sample with `tu` 0; "steady clear" is the first sample
from which sync 1, asCapable 1 and `tu` 0 hold for 2 s. Wire episodes are the DUT's CRF PDUs with
`tu=1` on the tap clock (one PDU each 2 ms), and are kept apart from the sampled console edges.
Command-completion times are reported only as the upper end of each interval.

The controller-poll arm: every DUT GET_AVB_INFO poll in the edge window must read AS_CAPABLE 1.
A poll that did not answer is counted separately, never as asCapable.
"""
from pathlib import Path
import copy, json, re, sys

SPLIT, LO, HI = 27.0, -9.0, 200.0
STEADY = 2.0
RUNS = [f"gm{i:02d}" for i in range(1, 6)]


def load(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def samples(console, t0):
    out = []
    for r in console:
        if r["cmd"] != "milan_status":
            continue
        d = dict(re.findall(r"(\w+)=([a-zA-Z0-9_]+)", r["raw"]))
        if "SYNC" in d and "TU" in d:
            out.append(dict(t=r["t"] - t0, end=r["end"] - t0, sync=d["SYNC"], asc=d["ASCAPABLE"], tu=d["TU"], pdelay=int(d["PDELAY_NS"])))
    return out


def tu_edges(s, lo, hi):
    """Assertion and steady clear in [lo, hi) from the complete history s (each sample keeps its index)."""
    rise = next((k for k in range(1, len(s)) if lo <= s[k]["t"] < hi and s[k]["tu"] == "1" and s[k - 1]["tu"] == "0"), None)
    rises = sum(1 for k in range(1, len(s)) if lo <= s[k]["t"] < hi and s[k]["tu"] == "1" and s[k - 1]["tu"] == "0")
    clear = None
    if rise is not None:
        for k in range(rise + 1, len(s)):
            ok = lambda x: x["sync"] == "1" and x["asc"] == "1" and x["tu"] == "0"
            if ok(s[k]) and all(ok(x) for x in s[k:] if x["t"] < s[k]["t"] + STEADY) and s[-1]["t"] >= s[k]["t"] + STEADY:
                clear = k
                break
    iv = lambda k: None if k is None else dict(t=round(s[k]["t"], 3), interval=[round(s[k - 1]["t"], 3), round(s[k]["end"], 3)])
    last1 = None
    if rise is not None:
        last1 = max(k for k in range(rise, len(s)) if s[k]["tu"] == "1" and all(x["tu"] == "1" for x in s[rise:k + 1]))
    episode = None if rise is None else [round(s[last1]["t"] - s[rise]["t"], 3), round(s[last1 + 1]["end"] - s[rise - 1]["t"], 3)]
    return dict(rises=rises, tu_set=iv(rise), steady_clear=iv(clear), console_episode_bounds_s=episode,
                steady_after_set_s=round(s[clear]["t"] - s[rise]["t"], 3) if rise is not None and clear is not None else None)


def poll_arm(ctrl, t0, co, lo, hi):
    p = [r for r in ctrl if r.get("role") == "dut" and r.get("what") == "avb" and lo <= r["t"] - co - t0 < hi]
    ok = [r for r in p if r["response"].get("status") == "SUCCESS"]
    asc0 = [round(r["t"] - co - t0, 3) for r in ok if r["response"]["decoded"].get("as_capable") != 1]
    pd = [r["response"]["decoded"]["pdelay_ns"] for r in ok]
    return dict(polls=len(p), answered=len(ok), unanswered=len(p) - len(ok), ascapable0=len(asc0), ascapable0_at=asc0,
                pdelay_ns=[min(pd), max(pd)] if pd else None)


def wire_episode(tr, lo, hi):
    """The DUT CRF `tu=1` episodes starting in [lo, hi): rise and fall on the tap clock."""
    eps = []
    for (t, v), nxt in zip(tr, tr[1:] + [[None, None]]):
        if v == 1 and lo <= t < hi:
            eps.append([t, nxt[0], round(nxt[0] - t, 3) if nxt[0] is not None else None])
    return eps


def run(raw, pkt, name, round1):
    ev, con, ctrl = load(raw / name / "events.jsonl"), load(raw / name / "console.jsonl"), load(raw / name / "controller.jsonl")
    t0 = next(e["t"] for e in ev if e["kind"] == "gm-start")
    c = min((e for e in ev if e["kind"] == "clock" and e["role"] == "controller"), key=lambda e: e["t1"] - e["t0"])
    co = c["remote"] - (c["t0"] + c["t1"]) / 2
    a = json.loads((pkt / "bench" / name / "analysis.json").read_text())
    s = samples(con, t0)
    rows = []
    for edge, (lo, hi) in (("takeover", (LO, SPLIT)), ("release", (SPLIT, HI))):
        r1 = next(x for x in round1 if x["run"] == name and x["edge"] == edge)
        te = tu_edges(s, lo, hi)
        pa = poll_arm(ctrl, t0, co, lo, hi)
        win = [x for x in s if lo <= x["t"] < hi]
        g = dict(r1["grade"])
        g["one_tu"] = g["one_tu"] and te["rises"] == 1
        g["no_ascapable_loss"] = sum(x["asc"] != "1" for x in win) == 0 and pa["ascapable0"] == 0
        rows.append(dict(run=name, edge=edge, tu=te, console_samples=len(win), console_ascapable0=sum(x["asc"] != "1" for x in win),
                         console_pdelay_ns=[min(x["pdelay"] for x in win), max(x["pdelay"] for x in win)], polls=pa,
                         wire_tu_episodes=wire_episode(a["wire"]["dut"]["tu"], lo, hi),
                         wire_tu1_first_last=next((p["crf"]["dut"]["tu1_span"] for p in a.get("per_step", []) if lo <= p["step"]["bracket"][1] < hi), None),
                         round1=dict(tu_set=r1["tu_set"], tu_steady_clear=r1["tu_steady_clear"]), grade=g, pass_=all(g.values())))
    totals = dict(console_samples=len(s), console_ascapable0=sum(x["asc"] != "1" for x in s),
                  console_pdelay_ns=[min(x["pdelay"] for x in s), max(x["pdelay"] for x in s)], polls=poll_arm(ctrl, t0, co, -1e9, 1e9))
    return rows, s, totals


def main():
    raw, pkt = Path(sys.argv[1]), Path(sys.argv[2])
    round1 = json.loads((pkt / "summary" / "gm-steps.json").read_text())["edges"]
    if sys.argv[3:] == ["--selftest"]:
        return selftest(raw, pkt, round1)
    rows, tot = [], []
    for name in RUNS:
        r, _, t = run(raw, pkt, name, round1)
        rows += r
        tot.append(t)
    P = lambda k: sum(r["polls"][k] for r in rows)
    ep = [e[2] for r in rows for e in r["wire_tu_episodes"]]
    sp = [round(r["wire_tu1_first_last"][1] - r["wire_tu1_first_last"][0], 3) for r in rows]
    cb = [r["tu"]["console_episode_bounds_s"] for r in rows]
    st = [r["tu"]["steady_after_set_s"] for r in rows]
    res = dict(edges=len(rows), passed=sum(r["pass_"] for r in rows),
               derivations=dict(console_samples=sum(r["console_samples"] for r in rows), console_ascapable0=sum(r["console_ascapable0"] for r in rows),
                                dut_polls=P("polls"), dut_polls_unanswered=P("unanswered"), dut_polls_ascapable0=P("ascapable0"),
                                console_pdelay_ns=[min(r["console_pdelay_ns"][0] for r in rows), max(r["console_pdelay_ns"][1] for r in rows)],
                                poll_pdelay_ns=[min(r["polls"]["pdelay_ns"][0] for r in rows), max(r["polls"]["pdelay_ns"][1] for r in rows)],
                                steady_after_set_s=[min(st), max(st)], wire_tu_rise_to_fall_s=[min(ep), max(ep)],
                                wire_tu1_first_to_last_pdu_s=[min(sp), max(sp)],
                                console_tu_episode_bounds_s=[min(x[0] for x in cb), max(x[1] for x in cb)],
                                runs=dict(console_samples=sum(t["console_samples"] for t in tot), console_ascapable0=sum(t["console_ascapable0"] for t in tot),
                                          console_pdelay_ns=[min(t["console_pdelay_ns"][0] for t in tot), max(t["console_pdelay_ns"][1] for t in tot)],
                                          dut_polls=sum(t["polls"]["polls"] for t in tot), dut_polls_unanswered=sum(t["polls"]["unanswered"] for t in tot),
                                          dut_polls_ascapable0=sum(t["polls"]["ascapable0"] for t in tot),
                                          poll_pdelay_ns=[min(t["polls"]["pdelay_ns"][0] for t in tot), max(t["polls"]["pdelay_ns"][1] for t in tot)]),
                                tu_set_changed=[(r["run"], r["edge"], r["round1"]["tu_set"], r["tu"]["tu_set"]["t"]) for r in rows
                                                if r["round1"]["tu_set"] != r["tu"]["tu_set"]["t"]],
                                steady_clear_shift_s=sorted({round(r["round1"]["tu_steady_clear"] - r["tu"]["steady_clear"]["t"], 3) for r in rows})),
               rows=rows)
    md = ["| Run | Edge | `tu` set (s) | its interval (s) | steady clear (s) | its interval (s) | steady after set (s) | wire `tu=1`, first to last PDU (s) | asCapable 0: samples / polls | Grade |",
          "|---|---|---:|---|---:|---|---:|---:|---|---|"]
    for r in rows:
        t = r["tu"]
        md.append(f"| {r['run'][-1]} | {r['edge']} | {t['tu_set']['t']:.3f} | {t['tu_set']['interval'][0]:.3f} to {t['tu_set']['interval'][1]:.3f} | "
                  f"{t['steady_clear']['t']:.3f} | {t['steady_clear']['interval'][0]:.3f} to {t['steady_clear']['interval'][1]:.3f} | {t['steady_after_set_s']:.3f} | "
                  f"{r['wire_tu1_first_last'][1] - r['wire_tu1_first_last'][0]:.3f} | {r['console_ascapable0']} of {r['console_samples']} / {r['polls']['ascapable0']} of {r['polls']['polls']} | "
                  f"{'PASS' if r['pass_'] else 'FAIL'} |")
    (pkt / "round2").mkdir(exist_ok=True)
    (pkt / "round2" / "gm-steps-r2.json").write_text(json.dumps(res, indent=1) + "\n")
    (pkt / "round2" / "gm-steps-r2.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    print(json.dumps(res["derivations"], indent=1))
    print(f"edges {res['edges']}, PASS {res['passed']}")
    return 0 if res["passed"] == res["edges"] else 1


def selftest(raw, pkt, round1):
    checks = []
    rows, s, _ = run(raw, pkt, "gm01", round1)
    # 1. A planted controller poll with asCapable 0 must fail its edge.
    ev, con, ctrl = load(raw / "gm01" / "events.jsonl"), load(raw / "gm01" / "console.jsonl"), load(raw / "gm01" / "controller.jsonl")
    t0 = next(e["t"] for e in ev if e["kind"] == "gm-start")
    c = min((e for e in ev if e["kind"] == "clock" and e["role"] == "controller"), key=lambda e: e["t1"] - e["t0"])
    co = c["remote"] - (c["t0"] + c["t1"]) / 2
    mut = copy.deepcopy(ctrl)
    k = next(i for i, r in enumerate(mut) if r.get("role") == "dut" and r.get("what") == "avb" and r["t"] - co - t0 > 10)
    mut[k]["response"]["decoded"]["as_capable"] = 0
    pa = poll_arm(mut, t0, co, LO, SPLIT)
    checks.append(("planted DUT poll with asCapable 0 in the takeover window", "FAIL" if pa["ascapable0"] else "PASS", "FAIL"))
    pa = poll_arm(mut, t0, co, SPLIT, HI)
    checks.append(("the same planted poll does not leak into the release window", "FAIL" if pa["ascapable0"] else "PASS", "PASS"))
    mut = copy.deepcopy(ctrl)
    mut[k]["response"] = dict(status="TIMEOUT")
    pa = poll_arm(mut, t0, co, LO, SPLIT)
    checks.append(("an unanswered poll is counted as unanswered, not as asCapable 0", "FAIL" if pa["ascapable0"] else ("PASS" if pa["unanswered"] == 1 else "FAIL"), "PASS"))
    # 2. Boundary control: a rounded PHC-step bracket that starts one sample after the `tu` rise must
    #    not drop the first asserted sample. The round-1 method searched from the bracket start.
    syn = [dict(t=0.25 * i, end=0.25 * i + 0.032, sync="1", asc="1", tu="0", pdelay=380) for i in range(40)]
    for i in (12, 13):
        syn[i]["tu"] = "1"
    bracket_start = syn[13]["t"]
    got = tu_edges(syn, 0.0, 9.0)["tu_set"]["t"]
    old = next(x["t"] for x in syn if x["t"] >= bracket_start and x["tu"] == "1")
    checks.append(("first asserted sample one sample before the step bracket is kept", "PASS" if got == syn[12]["t"] else "FAIL", "PASS"))
    checks.append(("the round-1 search from the bracket start drops it (the control can fail)", "PASS" if old == syn[12]["t"] else "FAIL", "FAIL"))
    # 3. A rise exactly at the window split belongs to the later window only.
    syn2 = [dict(t=-1 + 0.25 * i, end=-1 + 0.25 * i + 0.032, sync="1", asc="1", tu="0", pdelay=380) for i in range(200)]
    k27 = next(i for i, x in enumerate(syn2) if x["t"] == SPLIT)
    syn2[k27]["tu"] = "1"
    a, b = tu_edges(syn2, LO, SPLIT), tu_edges(syn2, SPLIT, HI)
    checks.append(("rise at exactly 27 s counts in the release window, not the takeover", "PASS" if (a["rises"], b["rises"]) == (0, 1) else "FAIL", "PASS"))
    # 4. A second console `tu` episode in one window fails the one-tu grade.
    syn3 = copy.deepcopy(syn)
    syn3[20]["tu"] = "1"
    checks.append(("a second console tu episode in the window", "PASS" if tu_edges(syn3, 0.0, 9.0)["rises"] == 1 else "FAIL", "FAIL"))
    # 5. Steady clear needs 2 s: a relapse 1.5 s after the first clear sample moves it.
    syn4 = copy.deepcopy(syn)
    syn4[20]["asc"] = "0"
    sc = tu_edges(syn4, 0.0, 9.0)["steady_clear"]["t"]
    checks.append(("steady clear skips a clear run broken within 2 s", "PASS" if sc == syn4[21]["t"] else "FAIL", "PASS"))
    # 6. The real gm01 takeover reproduces the health history's first `tu` 1 sample.
    h = json.loads((pkt / "bench" / "gm01" / "analysis.json").read_text())["health"]
    first_h = next(t for t, v in h if v.endswith("tu1") and LO <= t < SPLIT)
    checks.append(("gm01 takeover tu set equals the analysis health history", "PASS" if abs(rows[0]["tu"]["tu_set"]["t"] - first_h) < 0.0015 else "FAIL", "PASS"))
    bad = 0
    for label, got, want in checks:
        print(f"{'ok ' if got == want else 'BAD'} {want:4} got {got:4}  {label}")
        bad += got != want
    print(f"selftest: {len(checks) - bad} of {len(checks)} controls behave")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
