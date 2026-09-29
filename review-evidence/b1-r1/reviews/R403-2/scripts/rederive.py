#!/usr/bin/env python3
"""Independently re-derive the PR #620 findings-page tables and ranges from the
archived per-action analyses (bench/<action>/analysis.json), and compare them
with the tables written in the two pages.

This is reviewer code: it does not import or execute the author's summary or
check scripts. It reads only the archived analysis.json files, which are the
author's extraction from raw captures that are NOT in the archive; so this
proves internal consistency of page <- analysis, not analysis <- raw.

usage: rederive.py <repo-checkout> <extracted-packet-dir>/author
Prints every comparison; exit 1 if any page cell disagrees.
"""
import json
import re
import sys
from pathlib import Path

repo, author = Path(sys.argv[1]), Path(sys.argv[2])
A = lambda n: json.loads((author / "bench" / n / "analysis.json").read_text())
bad = []


def table(page, header_start):
    rows, on = [], False
    for line in (repo / page).read_text().splitlines():
        if line.startswith(header_start):
            on = True
            continue
        if on:
            if not line.startswith("|"):
                break
            if line.startswith("|---"):
                continue
            rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows


NUM = re.compile(r"[-+]?\d+(?:\.\d+)?")


def display_equal(p, m):
    """Equal up to one unit in the last displayed decimal (half-up vs float rounding)."""
    if NUM.sub("#", p) != NUM.sub("#", m):
        return False
    a, b = NUM.findall(p), NUM.findall(m)
    return all(x == y if "." not in x else abs(float(x) - float(y)) <= 10 ** -len(x.split(".")[1]) + 1e-9
               for x, y in zip(a, b))


def cmp(label, page_val, mine):
    exact = page_val == mine
    ok = exact or (len(page_val) == len(mine) and all(display_equal(p, m) for p, m in zip(page_val, mine)))
    tag = "OK  " if exact else ("OK~ " if ok else "DIFF")
    print(tag + f" {label}: page={page_val!r} rederived={mine!r}")
    if not ok:
        bad.append(label)


def f2(x):
    return "%.2f" % x


def rng(vals, fmt="%.2f"):
    return (fmt % min(vals)) + "-" + (fmt % max(vals))


# ---------------------------------------------------------------- cycles
P1 = "docs/findings/599_394_E1_LINK_CYCLES.md"
rows = table(P1, "| Cycle | OFF |")
cyc = {}
for i in range(1, 11):
    a = A("cycle%02d" % i)
    lk = a["link_counters"]["dut:counter-9-0"]
    md, mu = a["mac_link_down"], a["mac_link_up"]
    w = a["wire"]
    lic = a["crf_ctrl"]
    off = next(t for t, v in lic if t > 0 and v == "0x3")
    on = next(t for t, v in lic if t > off and v == "0x3002e3")
    fd, fp = w["dut"]["first_valid_after_on"], w["peer"]["first_valid_after_on"]
    cyc[i] = a
    mine = [str(i), f2(a["off_hold_s"]), f"{f2(md['last_up_before'])}-{f2(md['first_down'])}",
            f"{f2(mu['last_down_before'])}-{f2(mu['first_up'])}",
            f"+{lk['end_LINK_DOWN'] - lk['LINK_DOWN']} / +{lk['end_LINK_UP'] - lk['LINK_UP']}",
            f2(a["first_gm"]), "%.3f" % a["gptp_recovery_s"], f"{f2(fd)} / {f2(fp)}",
            f"{f2(fd - mu['first_up'])} / {f2(fp - mu['first_up'])}", f"{f2(off)} / {f2(on)}",
            "held" if a["bindings"]["all_connected"] else "NOT HELD"]
    cmp(f"cycle {i} row", rows[i - 1], mine)

C = [cyc[i] for i in range(1, 11)]
print("\n-- cycle bullets and counters --")
print("MAC down bracket span", rng([c["mac_link_down"]["last_up_before"] for c in C] + [c["mac_link_down"]["first_down"] for c in C]))
print("MAC down minus last far frame (first_down - last_far)", rng([c["mac_link_down"]["first_down"] - c["last_far_frame_before_on"] for c in C]))
print("MAC down minus last far frame (last_up - last_far)", rng([c["mac_link_down"]["last_up_before"] - c["last_far_frame_before_on"] for c in C]))
print("MAC up bracket span", rng([c["mac_link_up"]["last_down_before"] for c in C] + [c["mac_link_up"]["first_up"] for c in C]))
print("wire return minus MAC up first_up", rng([c["first_wire_return"] - c["mac_link_up"]["first_up"] for c in C]))
print("wire return minus MAC up last_down_before", rng([c["first_wire_return"] - c["mac_link_up"]["last_down_before"] for c in C]))
print("gPTP recovery", rng([c["gptp_recovery_s"] for c in C], "%.3f"))
print("gPTP steady_from == recovered_at every cycle", all(c["gptp_steady_from"] == c["gptp_recovered_at"] for c in C))
print("first GM kind", sorted([c["first_gm_kind"] for c in C]))
ml = [v for c in C for v in c["media_locked_at"].values()]
print("MEDIA_LOCKED again", rng(ml), "none missing:", None not in ml)
print("servo LOCKED again", rng([c["servo_locked_at"] for c in C]))
print("first PDU after wire return DUT", rng([c["wire"]["dut"]["first_valid_after_wire_return_s"] for c in C]))
print("first PDU after wire return peer", rng([c["wire"]["peer"]["first_valid_after_wire_return_s"] for c in C]))
print("post PDUs >100 both ways every cycle", all(c["wire"][r]["post_pdus"] > 100 for c in C for r in ("dut", "peer")))
print("post max gap", max(c["wire"][r]["post_max_gap_s"] for c in C for r in ("dut", "peer")))
print("post tu1 PDUs", [c["wire"]["dut"]["post_tu1"] + c["wire"]["peer"]["post_tu1"] for c in C])
st = [s["phc_minus_wall_delta_s"] for c in C for s in c["phc_discontinuities"] if abs(s["phc_minus_wall_delta_s"]) > 0.1]
print("GM-return PHC steps", len(st), rng(st, "%.1f"))
print("console max gap", max(c["max_console_gap_s"] for c in C))
print("reset epochs", sorted({e for c in C for e in c["reset_epochs"]}))
print("DUT mr changes per cycle", [len(c["wire"]["dut"]["mr"]) - 1 for c in C])
print("DUT mr change minus MAC down first_down", [round(c["wire"]["dut"]["mr"][1][0] - c["mac_link_down"]["first_down"], 3) for c in C if len(c["wire"]["dut"]["mr"]) > 1])
print("peer mr changes per cycle", [len(c["wire"]["peer"]["mr"]) - 1 for c in C])
print("MAC_STATUS values per cycle", sorted({tuple(c["mac_status_values"]) for c in C}), "up value", sorted({c["mac_link_up"]["value"] for c in C}))
print("link_status CSR mirrors MAC_STATUS values", all([v for _, v in c["mac_status"]] == [v for _, v in c["link_status_csr"]] for c in C))
print("link_status CSR lag behind MAC_STATUS (s)", rng([b[0] - a[0] for c in C for a, b in zip(c["mac_status"], c["link_status_csr"])], "%.3f"))
print("far frames during OFF after 5 s", [c["far_frames_during_off_after_5s"] for c in C])
print("carrier down/up", [[t for t, v in c["carrier"]][1:] for c in C])
ce1, ce10 = C[0]["counter_endpoints"], C[-1]["counter_endpoints"]
for key, idx in [("dut:counter-9-0", ("0", "1", "5")), ("dut:counter-5-1", ("0", "1")), ("dut:counter-6-1", ("0", "1")),
                 ("dut:counter-36-0", ("0", "1")), ("peer:counter-9-0", ("0", "1", "5"))]:
    print(f"{key} first(cycle01)", {k: ce1[key]["first"][k] for k in idx}, "last(cycle10)", {k: ce10[key]["last"][k] for k in idx})
print("per-cycle deltas LINK_UP/LINK_DOWN/GM_CHANGED", [(c["counter_endpoints"]["dut:counter-9-0"]["delta"]["0"], c["counter_endpoints"]["dut:counter-9-0"]["delta"]["1"], c["counter_endpoints"]["dut:counter-9-0"]["delta"]["5"]) for c in C])
print("per-cycle DUT listener LOCKED/UNLOCKED deltas", [(c["counter_endpoints"]["dut:counter-5-1"]["delta"]["0"], c["counter_endpoints"]["dut:counter-5-1"]["delta"]["1"]) for c in C])
print("per-cycle peer listener LOCKED/UNLOCKED deltas", [(c["counter_endpoints"]["peer:counter-5-8"]["delta"]["0"], c["counter_endpoints"]["peer:counter-5-8"]["delta"]["1"]) for c in C])
print("counter continuity cycle(n).last == cycle(n+1).first (dut 9-0, 5-1, 36-0)",
      all(C[i]["counter_endpoints"][k]["last"] == C[i + 1]["counter_endpoints"][k]["first"] for i in range(9) for k in ("dut:counter-9-0", "dut:counter-5-1", "dut:counter-36-0")))

bp = A("bmsr-proof")
print("\n-- link-drop proof --")
for k in ("mac_status", "link_status_csr", "linkg_stat", "carrier", "last_far_frame_before_on", "far_frames_during_off_after_5s",
          "first_wire_return", "first_gm", "first_gm_kind", "gptp_recovered_at", "gptp_recovery_s", "reset_epochs", "peer_available_index",
          "health", "gm", "bindings", "off_hold_s"):
    print(k, json.dumps(bp[k]))
print("LINK counters", bp["link_counters"]["dut:counter-9-0"])

# ---------------------------------------------------------------- steps
P2 = "docs/findings/387_SOFTWARE_GM_STEP.md"
srows = table(P2, "| Run | Edge | DUT PHC step |")
rrows = table(P2, "| Run | Takeover Announce |")
print("\n-- steps --")
k = 0
extra = []
for i in range(1, 6):
    a = A("gm%02d" % i)
    real = [s for s in a["phc_discontinuities"] if abs(s["phc_minus_wall_delta_s"]) > 0.005]
    flags = [s for s in a["phc_discontinuities"] if abs(s["phc_minus_wall_delta_s"]) <= 0.005]
    extra.append((i, flags))
    assert len(real) == 2, (i, real)
    wj, fj = a["dut_phc_wire_jumps"], a["far_time_jumps"]
    assert len(wj) == 2 and len(fj) == 2, (i, wj, fj)
    health = a["health"]
    dut_tu = a["wire"]["dut"]["tu"]
    servo = a["servo"]
    for e, s in enumerate(real):
        lo = s["bracket"][0] - 1.0
        hi = real[1]["bracket"][0] - 1.0 if e == 0 else 1e9
        ps = next(p for p in a["per_step"] if p["step"]["bracket"] == s["bracket"])
        clear = ps["tu_steady_clear"]
        eps = sum(1 for t, v in dut_tu if v == 1 and lo <= t <= min(hi, s["bracket"][1] + 15))
        a0 = next(t for t, v in health if t >= s["bracket"][0] and "asc0" in v)
        a1 = next(t for t, v in health if t > a0 and "asc1" in v)
        mr_d = sum(1 for t, v in a["wire"]["dut"]["mr"][1:] if lo <= t <= hi)
        mr_p = sum(1 for t, v in a["wire"]["peer"]["mr"][1:] if lo <= t <= hi)

        def cdelta(key, idx):
            tr = a["counter_transitions"][key]
            before = [v for t, v in tr if t < lo]
            inwin = [v for t, v in tr if t <= min(hi, s["bracket"][1] + 15)]
            return inwin[-1][idx] - (before[-1] if before else inwin[0])[idx]
        pre = [x[1]["discards"] for x in servo if x[0] < lo]
        win = [x[1]["discards"] for x in servo if lo <= x[0] <= min(hi, s["bracket"][1] + 15)]
        states = sorted({x[1]["state"] for x in servo})
        mine = [str(i), "takeover" if e == 0 else "release", "%+.3f ms" % (wj[e]["delta_s"] * 1e3),
                "%+.3f ms" % (fj[e]["delta_s"] * 1e3), f"{f2(ps['tu_first_set'])} / {f2(clear)}",
                f"{f2(clear - s['bracket'][1])}-{f2(clear - s['bracket'][0])}", str(eps), f"{f2(a0)}-{f2(a1)}",
                f"{mr_d} / {mr_p}", f"+{cdelta('dut:counter-6-1', '2')} / +{cdelta('dut:counter-5-1', '4')}",
                f"+{cdelta('dut:counter-5-1', '1')} / +{cdelta('peer:counter-5-8', '1')}",
                f"{'LOCKED' if states == [4] else states}; {pre[-1] if pre else win[0]} to {win[-1]}"]
        cmp(f"gm{i} {mine[1]} row", srows[k], mine)
        print(f"   console step {s['phc_minus_wall_delta_s']*1e3:+.3f} ms; wire-vs-console {abs(s['phc_minus_wall_delta_s']-wj[e]['delta_s'])*1e3:.3f} ms;"
              f" step at +{s['bracket'][0]:.2f}..{s['bracket'][1]:.2f}; asCapable lost {a0 - s['bracket'][1]:.2f}-{a0 - s['bracket'][0]:.2f} s after step, for {a1 - a0:.3f} s;"
              f" crf max gap dut/peer {ps['crf']['dut']['max_gap_s']}/{ps['crf']['peer']['max_gap_s']}; peer tu1 {ps['crf']['peer']['tu1']};"
              f" DUT listener MEDIA_LOCKED delta {cdelta('dut:counter-5-1', '0')}, peer MEDIA_RESET delta {cdelta('peer:counter-5-8', '4')}")
        k += 1
    d = {kk: v["delta"] for kk, v in a["counter_endpoints"].items()}
    ann = a["announce_gm"]
    tk = next(t for t, v in ann if v[0] != "3cc0c6fffefe0210")
    rl = next(t for t, v in ann if t > tk and v[0] == "3cc0c6fffefe0210")
    mine = [str(i), f2(tk), f2(rl), f"{a['clkv_tucnt_first_last'][0]} to {a['clkv_tucnt_first_last'][1]}",
            "+%d" % d["dut:counter-9-0"]["5"], "+%d / +%d" % (d["dut:counter-36-0"]["0"], d["dut:counter-36-0"]["1"]),
            "+%d / +%d / +%d" % (d["dut:counter-5-1"]["5"], d["dut:counter-5-1"]["9"], d["dut:counter-5-1"]["10"]),
            "%d / %d" % (a["wire"]["dut"]["tu_counts"]["1"], a["wire"]["peer"]["tu_counts"]["1"]),
            "%d ms" % round(max(a["wire"]["dut"]["max_gap_s"], a["wire"]["peer"]["max_gap_s"]) * 1e3)]
    cmp(f"gm{i} run row", rrows[i - 1], mine)
    shown = [[t, [v[0] if v[0] in ("3cc0c6fffefe0210", "020000fffe000001") else "<software-GM>", v[1], v[2]]] for t, v in ann]
    print(f"   announce GM changes {json.dumps(shown)}; crf_ctrl {a['crf_ctrl']}; servo states {sorted({x[1]['state'] for x in a['servo']})};"
          f" bindings {a['bindings']}; reset epochs {a['reset_epochs']}; mac {a['mac_status']}; console gap {a['max_console_gap_s']:.3f};"
          f" peer tu1 on wire {a['wire']['peer']['tu_counts']['1']}; peer listener TIMESTAMP_UNCERTAIN delta {d['peer:counter-5-8']['5']};"
          f" DUT talker TIMESTAMP_UNCERTAIN delta {d['dut:counter-6-1']['3']}")
print("non-step console flags", extra)
print("\nDIFFS:", bad if bad else "none")
sys.exit(1 if bad else 0)
