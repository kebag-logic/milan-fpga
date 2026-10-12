#!/usr/bin/env python3
"""Lane B16, round 2: a reduced, public receipt of one B16c case's console poll.

usage: r2_poll_b16c.py <poll-run.jsonl> <events.jsonl> <out-receipt.json> <out-trace.tsv>

The raw poll (console_poll_b8.py's output, kept outside the packet) is checked first against the
size and SHA-256 the case's own events.jsonl recorded for it; on a mismatch nothing is written and
the exit status is 2. Then, from the raw poll and the published events.jsonl:

1. The published poll-summary is recomputed from the raw poll with run_b16c.py's own rule (a poll
   belongs to a span when it starts at or after the span's start and ends at or before its end)
   and compared field by field: `matches_published_summary`.
2. Each poll is decoded with docs/reference/REGISTER_MAP.md: MCSRV_STAT (0x8F8) [2:0] state and
   [31:16] signed trim in 1/16 ppm; CRF_CTRL (0x738) [31] the CRF sink's lock; CRF_RATE (0x748)
   and AAFM_RATE (0x8E4) signed, 512 units per ppm; AAFM_STAT (0x8E0); SLIP_LB (0x8D4) and
   SLIP_TDM (0x8D8) [15:0] dups, [31:16] skips.
3. Finer spans are cut at the case's steps: the poll's start, the peer's set, the binds, the DUT's
   set, the first LOCKED poll after it, the window's start and end, the restore and the poll's end.
   Per span: polls, servo states, MCSRV_STAT[15:0] values, and the minimum and maximum of the trim,
   the CRF rate, the AAF rate (only where AAFM_STAT[1], rate valid, reads 1), SLIP_LB and SLIP_TDM.
   A poll that straddles a step is counted in neither span and listed under `straddling`.
4. Every change of SLIP_LB between two consecutive polls, with the times of both polls against
   the DUT's set and against the binds, both polls' servo states, and the span of the later poll.

Times are CLOCK_MONOTONIC_RAW, as the poll and the run tool recorded them. The bind time, which
events.jsonl gives in realtime only, is mapped to it by the median realtime-to-raw offset of the
polls. The trace (one row per poll: its number, its start against the DUT's set, its length and
the eight raw words) lets the extrema be checked without the raw file. Nothing here is private.
"""
import hashlib
import json
import statistics
import sys
from pathlib import Path

STATES = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}
WORDS = ("0x8f8", "0x8e0", "0x8e4", "0x8d4", "0x8d8", "0x8dc", "0x738", "0x748")


def s16(v):
    return v - 0x10000 if v & 0x8000 else v


def s32(v):
    return v - 0x100000000 if v & 0x80000000 else v


def decode(w):
    g = {k: (int(v, 16) if v else None) for k, v in w.items()}
    if any(g.get(k) is None for k in WORDS):
        return None
    st = g["0x8f8"]
    return dict(state=STATES.get(st & 7, str(st & 7)), mcsrv_lo=f"{st & 0xffff:04x}", trim_ppm=s16(st >> 16) / 16,
                crf_locked=(g["0x738"] >> 31) & 1, crf_rate_ppm=s32(g["0x748"]) / 512,
                aafm_stat=f"{g['0x8e0']:08x}", aafm_rate_valid=(g["0x8e0"] >> 1) & 1,
                aafm_rate_ppm=s32(g["0x8e4"]) / 512,
                slip_lb_dups=g["0x8d4"] & 0xffff, slip_lb_skips=g["0x8d4"] >> 16,
                slip_tdm_dups=g["0x8d8"] & 0xffff, slip_tdm_skips=g["0x8d8"] >> 16)


def rng(vals):
    vals = [v for v in vals if v is not None]
    return [min(vals), max(vals)] if vals else None


def published_rule(rows, spans):
    """run_b16c.py's Poll.summary, unchanged in substance."""
    out = {}
    for tag, (a, b) in spans.items():
        rs = [r for r in rows if r["raw0"] >= a and (b is None or r["raw1"] <= b)]
        st = {}
        for r in rs:
            k = STATES.get(r.get("servo_state"), str(r.get("servo_state")))
            st[k] = st.get(k, 0) + 1
        words = sorted({k for r in rs for k in (r.get("words") or {})})
        first = {k: next((r["words"].get(k) for r in rs if (r.get("words") or {}).get(k)), None) for k in words}
        last = {k: next((r["words"].get(k) for r in reversed(rs) if (r.get("words") or {}).get(k)), None) for k in words}
        distinct = {k: len({r["words"].get(k) for r in rs if (r.get("words") or {}).get(k)}) for k in words}
        out[tag] = dict(polls=len(rs), servo=st, first=first, last=last, distinct=distinct,
                        failed=sum(1 for r in rs if any(v is None for v in (r.get("words") or {}).values())))
    return out


def main() -> int:
    poll_p, ev_p, out_json, out_tsv = map(Path, sys.argv[1:5])
    raw = poll_p.read_bytes()
    sha, size = hashlib.sha256(raw).hexdigest(), len(raw)
    events = [json.loads(line) for line in ev_p.read_text().splitlines() if line.strip()]
    rec = next((e for e in events if e.get("kind") == "raw" and e.get("file") == "poll-run.jsonl"), None)
    if not rec or rec.get("sha256") != sha or rec.get("bytes") != size:
        print(f"MISMATCH: {poll_p.name} {size} {sha} against the run's record {rec}", file=sys.stderr)
        return 2
    rows = [json.loads(line) for line in raw.decode().splitlines() if line.startswith("{")]
    summ = next(e for e in events if e.get("kind") == "poll-summary")
    m = summ["marks_raw"]

    # 1. the published summary, recomputed with its own rule and spans
    pts = sorted(m.items(), key=lambda kv: kv[1])
    spans0 = {f"{a}..{b}": (ta, tb) for (a, ta), (b, tb) in zip(pts, pts[1:])}
    spans0[f"{pts[-1][0]}..poll-end"] = (pts[-1][1], None)
    again = published_rule(rows, spans0)
    matches = again == summ["spans"]

    # 2. decode; the realtime-to-raw offset for the binds
    off = statistics.median(r["raw0"] - r["t0"] * 1e9 for r in rows)
    binds = [e["t"] for e in events if e.get("kind") == "bind"]
    t_bind = int(max(binds) * 1e9 + off)
    t_set = m["dut-set"]
    dec = [(r, decode(r.get("words") or {})) for r in rows]
    after = [r for r, d in dec if r["raw0"] >= t_set]
    k_lock = next(k for k, r in enumerate(after) if r.get("servo_state") == 4)
    first_locked = after[k_lock]
    servo_ev = next((e for e in events if e.get("kind") == "servo-state"), None)

    # 3. finer spans
    cuts = [("poll-start", m["poll-start"]), ("peer-set", m["peer-set"]), ("binds", t_bind), ("dut-set", t_set),
            ("first-locked-poll", first_locked["raw0"]), ("window-start", m["window-start"]),
            ("window-end", m["window-end"]), ("restored", m["restored"]), ("poll-end", None)]
    spans, straddling, bounds = {}, [], {}
    for (a, ta), (b, tb) in zip(cuts, cuts[1:]):
        bounds[f"{a}..{b}"] = (ta, tb)
        rs = [(r, d) for r, d in dec if r["raw0"] >= ta and (tb is None or r["raw1"] <= tb)]
        ds = [d for _, d in rs if d]
        st, lo = {}, {}
        for d in ds:
            st[d["state"]] = st.get(d["state"], 0) + 1
            lo[d["mcsrv_lo"]] = lo.get(d["mcsrv_lo"], 0) + 1
        spans[f"{a}..{b}"] = dict(
            from_s=round((ta - t_set) / 1e9, 3), to_s=None if tb is None else round((tb - t_set) / 1e9, 3),
            polls=len(rs), failed=len(rs) - len(ds), servo=st, mcsrv_stat_lo16=lo,
            trim_ppm=rng(d["trim_ppm"] for d in ds),
            crf_locked=sum(d["crf_locked"] for d in ds), crf_rate_ppm=rng(d["crf_rate_ppm"] for d in ds),
            aafm_stat=sorted({d["aafm_stat"] for d in ds}),
            aafm_rate_ppm_valid=rng(d["aafm_rate_ppm"] for d in ds if d["aafm_rate_valid"]),
            slip_lb_dups=rng(d["slip_lb_dups"] for d in ds), slip_lb_skips=rng(d["slip_lb_skips"] for d in ds),
            slip_tdm_dups=rng(d["slip_tdm_dups"] for d in ds), slip_tdm_skips=rng(d["slip_tdm_skips"] for d in ds))
        if tb is not None:
            straddling += [dict(poll=r["n"], step=b, from_s=round((r["raw0"] - t_set) / 1e9, 3),
                                to_s=round((r["raw1"] - t_set) / 1e9, 3))
                           for r, _ in dec if r["raw0"] < tb < r["raw1"]]

    def span_of(r):
        return next((k for k, (ta, tb) in bounds.items() if r["raw0"] >= ta and (tb is None or r["raw1"] <= tb)),
                    "straddling")

    # 4. SLIP_LB transitions
    steps, prev = [], None
    for r, d in dec:
        if not d:
            continue
        if prev and (d["slip_lb_dups"], d["slip_lb_skips"]) != (prev[1]["slip_lb_dups"], prev[1]["slip_lb_skips"]):
            p = prev[0]
            steps.append(dict(polls=[p["n"], r["n"]],
                              after_set_s=[round((p["raw0"] - t_set) / 1e9, 3), round((r["raw1"] - t_set) / 1e9, 3)],
                              after_binds_s=[round((p["raw0"] - t_bind) / 1e9, 3), round((r["raw1"] - t_bind) / 1e9, 3)],
                              dups=[prev[1]["slip_lb_dups"], d["slip_lb_dups"]],
                              skips=[prev[1]["slip_lb_skips"], d["slip_lb_skips"]],
                              servo=[prev[1]["state"], d["state"]], span=span_of(r)))
        prev = (r, d)

    receipt = dict(
        tool="r2_poll_b16c.py", raw=dict(file=poll_p.name, bytes=size, sha256=sha),
        events=dict(file=ev_p.name, sha256=hashlib.sha256(ev_p.read_bytes()).hexdigest()),
        polls=len(rows), failed=sum(1 for _, d in dec if d is None),
        matches_published_summary=matches,
        marks_after_set_s={k: round((v - t_set) / 1e9, 3) for k, v in m.items()} | {"binds": round((t_bind - t_set) / 1e9, 3)},
        locked=dict(first_locked_poll=first_locked["n"],
                    recomputed_s=[round((after[k_lock - 1]["raw1"] - t_set) / 1e9, 3) if k_lock else 0.0,
                                  round((first_locked["raw1"] - t_set) / 1e9, 3)],
                    published=None if not servo_ev else [servo_ev.get("s_lo"), servo_ev.get("s_hi")]),
        spans=spans, straddling=straddling, slip_lb_steps=steps)
    out_json.write_text(json.dumps(receipt, indent=1) + "\n")
    with open(out_tsv, "w") as f:
        f.write("n\tstart_after_set_s\tlength_ms\t" + "\t".join(WORDS) + "\n")
        for r in rows:
            w = r.get("words") or {}
            f.write(f"{r['n']}\t{(r['raw0'] - t_set) / 1e9:.3f}\t{(r['raw1'] - r['raw0']) / 1e6:.1f}\t"
                    + "\t".join(w.get(k) or "-" for k in WORDS) + "\n")
    print(json.dumps(dict(raw=sha[:12], matches_published_summary=matches, steps=len(steps),
                          locked=receipt["locked"])))
    return 0 if matches else 1


if __name__ == "__main__":
    sys.exit(main())
