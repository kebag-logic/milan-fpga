#!/usr/bin/env python3
"""Independently re-derive the Step 3 per-cycle table of the #117 findings page.

Usage: step3.py <bench-a202 dir> [cycle numbers...]

Timebase (reviewer's own construction from the published raw files):
  * clock-before/after.jsonl give remote-minus-build-box offsets for the
    capture server, the controller host and the power-strip host; each is
    interpolated linearly in time between the two brackets.
  * t0 = T_OFF_CMD from powerstrip.txt (power-strip host clock) minus that
    host's offset, i.e. the off command on the build-box clock.
  * Console samples carry the command send time on the build-box clock.
  * Tap records: capture-server time = linear fit of (pcap host time minus tap
    time) minima per 5 s tap bin; then minus the capture-server offset.
  * Controller-host watcher times minus the controller-host offset.
All results are seconds after t0. A console transition is reported at the
first sample that shows it (the later of the two bracketing samples).
"""
import json, os, re, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import condec, tapdec

SW_ID = "3cc0c6fffefe0210"
DUT_ID = "020000fffe000001"
HOSTS = {"server": "ubuntu-server", "ctl": "pw1", "ps": "-pi"}


def offsets(cdir):
    res = {}
    for fn in ("clock-before.jsonl", "clock-after.jsonl"):
        for line in open(os.path.join(cdir, fn)):
            j = json.loads(line)
            for k, pat in HOSTS.items():
                if j["host"].endswith(pat) or pat in j["host"]:
                    res.setdefault(k, []).append((j["local_t"], j["offset_s"]))
    def f(k):
        (ta, oa), (tb, ob) = sorted(res[k])
        return lambda t: oa + (ob - oa) * (t - ta) / (tb - ta)
    return {k: f(k) for k in res}, res


def powerstrip(cdir):
    d = {}
    for line in open(os.path.join(cdir, "powerstrip.txt")):
        for m in re.finditer(r"(T_[A-Z_]+) ([0-9.]+)", line):
            d[m.group(1)] = float(m.group(2))
    return d


def tap_timeline(path):
    recs, stats = tapdec.load(path)
    bins = {}
    for r in recs:
        k = r["tap_ns"] // 5_000_000_000
        v = r["host_ns"] - r["tap_ns"]
        if k not in bins or v < bins[k][1]:
            bins[k] = (r["tap_ns"], v)
    xs = [x for x, _ in bins.values()]
    ys = [y for _, y in bins.values()]
    mx, my = st.fmean(xs), st.fmean(ys)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    resid = max(abs(y - (a + b * x)) for x, y in zip(xs, ys))
    for r in recs:
        r["srv"] = (r["tap_ns"] + a + b * r["tap_ns"]) / 1e9
    return recs, stats, resid / 1e6, len(bins)


def main():
    base = sys.argv[1]
    cycles = [int(x) for x in sys.argv[2:]] or [1, 2, 3, 4, 5, 6]
    table = []
    for n in cycles:
        cdir = os.path.join(base, "bench", f"cycle{n}")
        off, raw = offsets(cdir)
        ps = powerstrip(cdir)
        t0 = ps["T_OFF_CMD"] - off["ps"](ps["T_OFF_CMD"])
        ton = ps["T_ON_CMD"] - off["ps"](ps["T_ON_CMD"])
        R = lambda t: t - t0
        # ---------------- console
        con = condec.parse(os.path.join(cdir, "console.txt"))
        ms = [r for r in con if r["cmd"] == "milan_status" and r.get("ok")]
        mem = {}
        for r in con:
            if "addr" in r:
                mem.setdefault(r["addr"], []).append((R(r["t"]), r["word"]))
        S = []
        for r in ms:
            f = r["fields"]
            cs = int(f["CLKV_STAT"], 16)
            S.append(dict(t=R(r["t"]), gm=f["GPTP_GM"], par=f["GPTP_PARENT"], sync=int(f["SYNC"]),
                          asc=int(f["ASCAPABLE"]), tu=int(f["TU"]), hold=(cs >> 3) & 1, cs=cs,
                          gen=int(f["AS_PATH_GEN"]), cnt=int(f["AS_PATH_COUNT"]), pd=int(f["PDELAY_NS"])))
        good = lambda s: s["gm"] == SW_ID and s["sync"] == 1 and s["asc"] == 1 and s["tu"] == 0
        gaps = [b["t"] - a["t"] for a, b in zip(S, S[1:])]
        pre = [s for s in S if s["t"] < 0]

        def first(pred, after=0.0):
            for s in S:
                if s["t"] > after and pred(s):
                    return s
            return None
        sync0 = first(lambda s: s["sync"] == 0)
        gmself = first(lambda s: s["gm"] == DUT_ID)
        asc0 = first(lambda s: s["asc"] == 0)
        asc1 = first(lambda s: s["asc"] == 1, asc0["t"])
        gmsw = first(lambda s: s["gm"] == SW_ID, gmself["t"])
        idx = None
        for i in range(len(S) - 1, -1, -1):
            if not good(S[i]):
                idx = i + 1
                break
        allgood = S[idx]
        tu1 = first(lambda s: s["tu"] == 1)
        hold_loss = [s["t"] for s in S if s["hold"] and s["t"] < gmself["t"]]
        hold_ret = [s["t"] for s in S if s["hold"] and s["t"] > gmsw["t"] - 0.2]
        tuclr = first(lambda s: s["tu"] == 0, gmsw["t"] - 0.01)
        synret = first(lambda s: s["sync"] == 1, gmsw["t"] - 0.2)
        gens = sorted({(s["gen"], s["cnt"]) for s in S})
        pars = all(s["par"] == s["gm"] for s in S)
        # ---------------- tap
        tp = os.path.join(cdir, f"tap-c{n}.pcap")
        recs, tstats, resid, nb = tap_timeline(tp)
        for r in recs:
            r["t"] = R(r["srv"] - off["server"](r["srv"]))
        p2 = [r for r in recs if r["port"] == 2]
        p3 = [r for r in recs if r["port"] == 3]
        allg = [(b["t"] - a["t"], a["t"], b["t"]) for a, b in zip(recs, recs[1:])]
        dark = max(allg)
        sw_last = max(r["t"] for r in p2 if r["t"] < dark[2])
        sw_first = min(r["t"] for r in p2 if r["t"] >= dark[2])
        any_first = dark[2]
        ptp2 = [r for r in p2 if r["kind"] == "ptp"]
        last = lambda mt: max(r["t"] for r in ptp2 if r["mt"] == mt and r["t"] < dark[2])
        firstm = lambda mt: min(r["t"] for r in ptp2 if r["mt"] == mt and r["t"] >= dark[2])
        ann_after = sorted(r["t"] for r in ptp2 if r["mt"] == 0xB and r["t"] >= dark[2])
        sw_ann1, sw_sync1 = firstm(0xB), firstm(0)
        dut_master = [r for r in p3 if r["kind"] == "ptp" and r["mt"] in (0, 8, 0xB) and r["t"] >= dark[2]]
        dut_ann = [(round(r["t"], 2), r.get("gm"), r.get("p1")) for r in dut_master if r["mt"] == 0xB]
        sw_ann_fields = {(r["gm"], r["p1"], tuple(r["path"] or [])) for r in ptp2 if r["mt"] == 0xB}
        rec_ann = allgood["t"] - sw_ann1
        rec_first = allgood["t"] - min(sw_ann1, sw_sync1)
        # which Announce the DUT adopted: the first switch Announce at or before GM=switch sample
        adopted = max(t for t in ann_after if t <= gmsw["t"])
        # ---------------- CRF (bound cycles)
        crf = [r for r in p3 if r["kind"] == "crf"]
        crfinfo = None
        if crf:
            pre_dark = [r for r in crf if r["t"] < dark[2]]
            post = [r for r in crf if r["t"] >= dark[2]]
            tu1c = [r for r in pre_dark if r["tu"] == 1]
            crfinfo = dict(first_tu1=round(tu1c[0]["t"], 3) if tu1c else None, n_tu1=len(tu1c),
                           last_pre=round(pre_dark[-1]["t"], 3) if pre_dark else None,
                           first_post=round(post[0]["t"], 3) if post else None,
                           post_tu1=sum(r["tu"] for r in post), post_n=len(post),
                           pre_tu0_before_loss=sum(1 for r in pre_dark if r["tu"] == 0))
        # ---------------- console CSR words
        ep = sorted({w for _, w in mem.get(0x90000720, [])})
        lg = mem.get(0x90000774, [])
        lg_drop = next((t for t, w in lg if t > 0 and w == 0x03), None)
        lg_back = next((t for t, w in lg if lg_drop and t > lg_drop and w == 0x83), None)
        tuc = mem.get(0x90000780, [])
        tuc_delta = tuc[-1][1] - tuc[0][1] if tuc else None
        crft = mem.get(0x90000750, [])
        lic = [(round(t, 2), hex(w)) for (t, w), (_, pw) in zip(crft[1:], crft) if w != pw] if crft else []
        # ---------------- controller host
        wat = [json.loads(l) for l in open(os.path.join(cdir, "pw1-watch.jsonl"))]
        car = [(w["t"], w["value"]) for w in wat if w.get("type") == "carrier"]
        car_rel = [(round(R(t - off["ctl"](t)), 2), v) for t, v in car]
        row = dict(cycle=n, off_for=round(ps["T_ON_CMD"] - ps["T_OFF_CMD"], 2),
                   sync0=round(sync0["t"], 2), gmself=round(gmself["t"], 2), asc0=round(asc0["t"], 2),
                   sw_first=round(sw_first, 2), sw_ann1=round(sw_ann1, 2), sw_sync1=round(sw_sync1, 2),
                   asc1=round(asc1["t"], 2), gmsw=round(gmsw["t"], 2), allgood=round(allgood["t"], 2),
                   rec=round(rec_ann, 3), rec_first=round(rec_first, 3))
        table.append(row)
        print(f"===== cycle {n}")
        print("  offsets (remote minus build box, before/after):",
              {k: [round(o, 6) for _, o in sorted(v)] for k, v in raw.items()})
        print(f"  t0(build-box) {t0:.3f}; on at {R(ton):.3f}; off_for {row['off_for']}")
        print(f"  console samples {len(S)} (pre-off {len(pre)} all-good {sum(1 for s in pre if good(s))}); "
              f"max gap {max(gaps):.3f}; RST_EPOCH {ep}")
        print(f"  sync0/tu1 {sync0['t']:.2f} (tu1 first {tu1['t']:.2f}); gm=self {gmself['t']:.2f}; asc0 {asc0['t']:.2f}; "
              f"asc1 {asc1['t']:.2f}; gm=switch {gmsw['t']:.2f}; all-good {allgood['t']:.2f} (prev good? {good(S[idx - 1])})")
        print(f"  holdover samples at loss: {len(hold_loss)} span {[round(x, 2) for x in hold_loss[:1] + hold_loss[-1:]]}; "
              f"at return: {len(hold_ret)} {[round(x, 2) for x in hold_ret[:1] + hold_ret[-1:]]}; "
              f"sync back {synret['t']:.2f}; tu clear {tuclr['t']:.2f} ({tuclr['t'] - gmsw['t']:.2f} after adoption sample)")
        print(f"  path (gen,count) seen {gens}; parent==gm in all samples {pars}")
        print(f"  tap: tapped {tstats['tapped']} host-only {tstats['host_only']} bins {nb} fit resid max {resid:.2f} ms")
        print(f"  tap: switch last Sync {last(0):.2f} last Announce {last(0xB):.2f} last Pdelay_Resp {last(3):.2f} "
              f"last frame {sw_last:.2f}; dark {dark[1]:.2f} -> {dark[2]:.2f} (first any {any_first:.2f})")
        print(f"  tap: switch first frame {sw_first:.2f} first Announce {sw_ann1:.2f} first Sync {sw_sync1:.2f}; "
              f"announces after return {[round(t, 3) for t in ann_after[:3]]}")
        print(f"  tap: switch Announce fields {sw_ann_fields}")
        print(f"  DUT master msgs after return: {len(dut_master)} (Sync {sum(1 for r in dut_master if r['mt'] == 0)}, "
              f"FU {sum(1 for r in dut_master if r['mt'] == 8)}), Announce {dut_ann}")
        print(f"  adopted Announce at {adopted:.3f}; GM=switch sample {gmsw['t']:.3f} (delta {gmsw['t'] - adopted:.3f})")
        print(f"  loss edges vs wire: sync0-lastSync {sync0['t'] - last(0):.2f}; gmself-lastAnn {gmself['t'] - last(0xB):.2f}; "
              f"asc0-lastPdResp {asc0['t'] - last(3):.2f}")
        print(f"  RECOVERY all-good - first Announce = {rec_ann:.3f}; vs first of Announce/Sync = {rec_first:.3f}; "
              f"on->all-good {allgood['t'] - R(ton):.2f}; swfirst->all-good {allgood['t'] - sw_first:.2f}")
        print(f"  LINKG_STAT 0x03 at {lg_drop}, back 0x83 at {lg_back}; CLKV_TUCNT delta {tuc_delta}")
        print(f"  carrier (controller host): {car_rel}")
        if crfinfo:
            print(f"  CRF: {crfinfo}; CRFT_CTRL changes {lic}")
            cc = mem.get(0x77C)
    print("\n===== table (seconds after the off command)")
    keys = list(table[0].keys())
    print(" | ".join(keys))
    for r in table:
        print(" | ".join(str(r[k]) for k in keys))
    print(f"recovery range {min(r['rec'] for r in table)} .. {max(r['rec'] for r in table)}; bound 5 s: "
          f"{'ALL PASS' if all(r['rec'] < 5 for r in table) else 'FAIL'}")


if __name__ == "__main__":
    main()
