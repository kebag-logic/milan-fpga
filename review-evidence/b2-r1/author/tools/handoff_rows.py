"""Regenerate the per-bind and per-cycle tables in HANDOFF.md from the analyses.

usage: handoff_rows.py
"""
import json, re
from pathlib import Path
p = Path(__file__).resolve().parent.parent
h = p / "HANDOFF.md"


def f(x, n=6):
    return "-" if x is None else f"{x:.{n}f}"


rows = ["| Bind | Fresh (pre-window s, DUT LeaveAll PDUs, target TA declarations) | First probe status | First DUT TA (s) | First bridge MRPDU (s) | Bridge Listener Ready (s) | First valid PDU (s) | Unbind after: bridge Lv / last PDU / DUT TA Lv (s) | Result |",
        "|---|---|---|---|---|---|---|---|---|"]
for d in sorted((p / "bind").glob("bind-[0-9]*/analysis.json"), key=lambda x: int(x.parent.name.split("-")[1])):
    a = json.loads(d.read_text())
    k = d.parent.name.split("-")[1]
    u = p / "bind" / ("unbind-" + k) / "analysis.json"
    un = "-"
    if u.exists():
        b = json.loads(u.read_text())
        un = f"{f(b['bridge_listener_lv_after_response_s'])} / {f(b['last_valid_pdu_after_response_s'])} / {f(b['dut_ta_lv_after_response_s'], 3)} ({b['result']})"
    bm = a["first_bridge_mrpdu"]
    rows.append(f"| {k} | {a['fresh']} ({a['pre_window_s']:.1f}, {a['pre_dut_leaveall_pdus']}, {a['pre_dut_target_ta_declarations']}) | {a['first_probe_response_status']} | "
                f"{f(a['first_dut_ta']['after_response_s'])} | {f(bm['after_response_s'])}{' LeaveAll' if bm['leaveall'] else ''} | "
                f"{f(a['first_bridge_ready']['after_response_s'])} | {f(a['latency_s'])} | {un} | {a['result']} |")
crow = ["| Cycle | Bridge Lv after disconnect (s) | Registrar at Lv | Last PDU after Lv (s) | PDUs after Lv + 2 ms | Settled hold PDUs | START/STOP delta | TA declared in hold | Restart (s) | #608 stop | #75 restart |",
        "|---|---|---|---|---|---|---|---|---|---|---|"]
for d in sorted((p / "cycles").glob("cycle-[0-9]*/analysis.json")):
    a = json.loads(d.read_text())
    stop = a["stop_608"] if a["stop_608"] in ("PASS", "FAIL", "NO-LV") else "LV-WINDOW"
    crow.append(f"| {d.parent.name.split('-')[1]} | {f(a.get('bridge_lv_after_disconnect_s'))} | {a.get('registrar_at_lv', '-')} | {f(a.get('last_pdu_after_lv_s'))} | "
                f"{a.get('pdus_after_lv_plus_period', '-')} | {a['settled_pdus']} | {a['dut_out1_start_stop_delta'][0]}/{a['dut_out1_start_stop_delta'][1]} | "
                f"{'yes' if a['dut_ta_declarations_in_hold'] else 'no'} | {f(a['restart_s'])} | {stop} | {a['restart_75']} |")
t = h.read_text()
t = re.sub(r"(<!-- binds:start -->\n).*?(<!-- binds:end -->)", lambda m: m[1] + "\n".join(rows) + "\n" + m[2], t, flags=re.S)
t = re.sub(r"(<!-- cycles:start -->\n).*?(<!-- cycles:end -->)", lambda m: m[1] + "\n".join(crow) + "\n" + m[2], t, flags=re.S)
h.write_text(t)
print(len(rows) - 2, "bind rows,", len(crow) - 2, "cycle rows")
