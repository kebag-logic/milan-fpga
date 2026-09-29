"""Emit the findings-page tables for lane B2 from summary/summary.json and the packet.

Every number in a generated table is read from the analyses; nothing is typed.
usage: b2_pages.py  (writes summary/page-*.md)
"""
import json
from pathlib import Path

p = Path(__file__).resolve().parent.parent
s = json.loads((p / "summary" / "summary.json").read_text())
raw = {r["path"]: r for r in json.loads((p / "RAW-ARTIFACTS.json").read_text())["files"]}
out = {}


def f(x, n=6):
    return "-" if x is None else f"{x:.{n}f}"


def tx(path, mt):
    for line in path.read_text().splitlines():
        r = json.loads(line)
        if r.get("kind") == "transaction" and r["mt"] == mt:
            return r


rows = ["| Bind | Unbound before, s | Pre-bind tap, s | DUT LeaveAll PDUs / target TA declarations in it | First probe status | First DUT TA, s | First bridge MRPDU, s | Bridge Listener Ready, s | First valid PDU, s | Result |",
        "|---|---|---|---|---|---|---|---|---|---|"]
for b in s["binds"]:
    k = b["bind"]
    hold = "more than 1,800 (lane B1's restore)" if k == 1 else f"{tx(p / 'bind' / f'bind-{k}' / 'bind.jsonl', 6)['start'] - tx(p / 'bind' / f'unbind-{k - 1}' / 'unbind.jsonl', 8)['end']:.1f}"
    status = {0: "SUCCESS"}.get(b["probe_status"], str(b["probe_status"]))
    mr = f(b["first_bridge_mrpdu_s"]) + (", LeaveAll" if b["first_bridge_mrpdu_leaveall"] else ", Listener New")
    rows.append(f"| {k} | {hold} | {b['pre_window_s']:.3f} | {b['pre_dut_leaveall_pdus']} / {b['pre_target_ta_declarations']} | {status} | "
                f"{f(b['first_dut_ta_s'])} ({b['first_dut_ta_event']}) | {mr} | {f(b['first_bridge_ready_s'])} | {f(b['latency_s'])} | {b['result']} |")
out["binds"] = rows

rows = ["| Unbind | After bind response, s | Bridge Listener Lv, s | Last PDU, s | PDUs after Lv + 2 ms | DUT TA Lv, s | Quiet after TA Lv, s | START / STOP |",
        "|---|---|---|---|---|---|---|---|"]
for b in s["binds"]:
    u = b["unbind"]
    if not u:
        continue
    k = b["bind"]
    gap = tx(p / "bind" / f"unbind-{k}" / "unbind.jsonl", 8)["start"] - tx(p / "bind" / f"bind-{k}" / "bind.jsonl", 6)["end"]
    rows.append(f"| {k} | {gap:.1f} | {f(u['lv_s'])} | {f(u['last_pdu_s'])} | {u['pdus_after_lv_plus_period']} | {f(u['dut_ta_lv_s'], 3)} | {u['settle_s']:.1f} | +{u['start_stop_delta'][0]} / +{u['start_stop_delta'][1]} |")
out["unbinds"] = rows

r = s["restart"]
rows = ["| Population | Count | Below 1 s | Min, s | Median, s | p95, s | Max, s |", "|---|---|---|---|---|---|---|",
        f"| Demonstrated restarts | {r['demonstrated']} | {r['below_1s']} | {f(r['min'])} | {f(r['median'])} | {f(r['p95'])} | {f(r['max'])} |"]
for key, label in (("held", "DUT Talker Advertise held through the hold"), ("withdrawn", "DUT Talker Advertise withdrawn in the hold")):
    t = r["by_ta_in_hold"][key]
    rows.append(f"| {label} | {t['n']} | {t['n']} | {f(t['min'])} | {f(t['median'])} | - | {f(t['max'])} |")
out["distribution"] = rows

fit = r["fit"]
out["growth"] = ["| First ten median, s | Last ten median, s | Slope, s per cycle | 95% slope interval, s per cycle | Residual df |", "|---|---|---|---|---|",
                 f"| {f(r['first_ten_median'])} | {f(r['last_ten_median'])} | {fit['slope']:+.9f} | [{fit['ci'][0]:+.9f}, {fit['ci'][1]:+.9f}] | {fit['df']} |"]
rows = ["| Cycles | Demonstrated restarts | Median, s | Max, s | Combined MSRP PDUs/s |", "|---|---|---|---|---|"]
for b in s["blocks"]:
    rows.append(f"| {b['block']} | {b['demonstrated']} | {f(b['median'])} | {f(b['max'])} | {b['msrp_pdus_per_s']:.3f} |")
out["blocks"] = rows

rows = ["| Cycle | Own LeaveAll minus bridge Lv, s | Registrar at Lv | Stop |", "|---|---|---|---|"]
for n in s["stop"]["near_own_leaveall"]:
    rows.append(f"| {n['cycle']} | {n['own_la_minus_lv_s']:+.6f} | {n['registrar']} | {n['stop']} |")
out["near"] = rows

rows = ["| Cycle | Bridge Lv after disconnect, s | Registrar at Lv | Last PDU minus Lv, ms | Hold PDUs | START / STOP | DUT TA declared in hold | Restart, s | #608 stop | #75 restart |",
        "|---|---|---|---|---|---|---|---|---|---|"]
for c in s["cycles"]:
    stop = "PASS" if c["stop_class"] == "stop within one PDU" else ("LV window, no stop" if c["registrar_class"] == "LV" else "FAIL")
    rows.append(f"| {c['cycle']} | {f(c['lv_s'])} | {c['registrar_class']} | {c['last_pdu_after_lv_s'] * 1000:+.3f} | {c['hold_pdus']} | "
                f"+{c['start_stop_delta'][0]} / +{c['start_stop_delta'][1]} | {'yes' if c['ta_in_hold'] else 'no'} | {f(c['restart_s']) if c['demonstrated'] else 'none: no stop'} | {stop} | {c['restart_75']} |")
out["cycles"] = rows


def rawrows(names):
    rr = ["| Capture identifier | Bytes | SHA-256 |", "|---|---|---|"]
    for nm in names:
        x = raw[nm + "/tap.pcap"]
        rr.append(f"| `{x['path']}` | {x['size']} | `{x['sha256']}` |")
    return rr


out["raw-binds"] = rawrows(["baseline"] + [f"{m}-{k}" for k in range(1, 6) for m in ("bind", "unbind") if (m, k) != ("unbind", 5)] + ["unbind-restore", "final"])
out["raw-cycles"] = rawrows([f"cycle-{n:03d}" for n in range(1, 101)])
for k, v in out.items():
    (p / "summary" / f"page-{k}.md").write_text("\n".join(v) + "\n")
print({k: len(v) - 2 for k, v in out.items()})
