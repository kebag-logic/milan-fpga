#!/usr/bin/env python3
"""Lane B17 round 2: check the printed figures against the raw counter logs (offline, read-only).

usage: check_b17_page.py <packet_dir> <findings_page.md> [<pr_body.md>]
  1. Recomputes, independently of summ_b17.py, every poll cell of the slips table from cycles/cNN/poll.jsonl
     and the bind's instant in cycles/cNN/events.jsonl, each rounded once (the bind's UTC instant truncated),
     and compares it with the page's row, cell by cell.
  2. The page's slips table equals summary/table.md, and its bind-priming table equals summary/priming.md.
  3. Each lane figure from summary/figures.json that the section prints appears in the section.
  4. With a PR body: each of its table rows equals the matching cells of summary/table.md.
Prints one line per check and "mismatches: N"; rc 0 only when N is 0.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

P, page = Path(sys.argv[1]), Path(sys.argv[2]).read_text()
start = page.index("## Dev 5603c353, 2026-10-15: lane B17")
end = page.find("\n## ", start + 10)
sec = page[start:end if end > 0 else None]
flat = " ".join(sec.split())  # prose with its line breaks folded
bad = 0


def check(ok, what):
    global bad
    bad += not ok
    print(("ok   " if ok else "FAIL ") + what)


def cells(line):
    return [x.strip() for x in line.strip().strip("|").split("|")]


rows = {cells(x)[0]: cells(x) for x in sec.splitlines() if x.startswith("| c") and len(cells(x)) == 10}
for cdir in sorted((P / "cycles").glob("c[0-9][0-9]")):
    c = cdir.name
    ev = [json.loads(x) for x in open(cdir / "events.jsonl") if x.startswith("{")]
    tb = next(e for e in ev if e["kind"] == "bind-time")["t_bind_local"]
    po = sorted((json.loads(x) for x in open(cdir / "poll.jsonl") if x.startswith("{")), key=lambda x: x["n"])
    lb = [int(x["words"]["0x8d4"], 16) for x in po]
    ch = [i for i in range(1, len(po)) if lb[i] != lb[i - 1]]
    slip = "; ".join(f"{po[i - 1]['t0'] - tb:.2f} to {po[i]['t1'] - tb:.2f}, +{(lb[i] & 0xFFFF) - (lb[i - 1] & 0xFFFF)} dups, "
                     f"{(lb[i] >> 16) - (lb[i - 1] >> 16)} skips" for i in ch) or "none"
    want = {1: datetime.fromtimestamp(tb, timezone.utc).strftime("%H:%M:%S.%f")[:-3],
            3: f"{len(po)}, {po[0]['t0'] - tb:+.2f} to {po[-1]['t1'] - tb:+.2f}",
            4: f"{lb[0] & 0xFFFF} to {lb[-1] & 0xFFFF}", 5: slip}
    got = rows.get(c)
    check(got is not None, f"{c}: row present on the page")
    if got:
        for i, w in want.items():
            check(got[i] == w, f"{c}: cell {i} page '{got[i]}' raw '{w}'")

tbl = [x for x in sec.splitlines() if x.startswith("| c") and len(cells(x)) == 10]
check(tbl == open(P / "summary" / "table.md").read().splitlines()[2:], "slips table equals summary/table.md")
pm = open(P / "summary" / "priming.md").read().splitlines()
check(sec.count("\n".join(pm) + "\n") == 1, "bind-priming table equals summary/priming.md")

f = json.load(open(P / "summary" / "figures.json"))["figures"]
for key in ("slip_after_bind_s", "slip_interval_width_s", "polls_left_after_slip_s", "last_poll_min_s", "prefill_exit_by_s",
            "converged_later_by_s", "fill_from_exit", "first_pdu_ms", "rates_vs_gptp_ppm", "delta_ppm", "rate_interval_min_s",
            "rate_interval_min_at_resolution_s", "rate_slips_expected_max"):
    check(f[key] in flat, f"figure {key} '{f[key]}' printed")
for key, sub in (("bursts_after_slip", "last_poll"), ("long_polls", "after_unbind_s"), ("long_polls", "after_bind_s"),
                 ("long_polls", "took_s"), ("long_polls", "others_took_max_s")):
    check(f[key][sub] in flat, f"figure {key}.{sub} '{f[key][sub]}' printed")
check(f["peak_after_slip_us"]["last_poll"].split(" to ")[1] in flat, "after-slip peak to the last poll printed")
check(f["peer_stream_after_unbind_s"]["c08"] in flat and f["peer_stream_last_before_bind_s"]["c08"].lstrip("-") in flat, "c08 peer stream figures printed")
check(f["prefill_exit_brackets"]["c05"].strip("(]").replace(", ", " to ") in flat, "c05 prefill bracket printed")
check(f["peer_stream_after_unbind_s"]["c05"] in flat, "the other nine cycles' least peer-stream tail printed")

if len(sys.argv) > 3:
    ref = {cells(x)[0]: cells(x) for x in open(P / "summary" / "table.md").read().splitlines()[2:]}
    for x in Path(sys.argv[3]).read_text().splitlines():
        if x.startswith("| c"):
            g, r = cells(x), ref[cells(x)[0]]
            want = [r[0], r[1], r[2], r[4], r[5].replace(", 0 skips", ""), r[7], r[8]]
            check(g == want, f"PR body {g[0]}: {g} against {want}")

print(f"mismatches: {bad}")
sys.exit(1 if bad else 0)
