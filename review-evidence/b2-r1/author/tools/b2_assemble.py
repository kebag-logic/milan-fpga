"""Fill the two findings-page templates from summary/page-*.md and summary.json.

usage: b2_assemble.py <lane_worktree>
"""
import json, sys
from pathlib import Path
p = Path(__file__).resolve().parent.parent
w = Path(sys.argv[1]) / "docs" / "findings"
s = json.loads((p / "summary" / "summary.json").read_text())
frag = {x.stem[len("page-"):]: x.read_text().rstrip("\n") for x in (p / "summary").glob("page-*.md")}
st = s["stop"]
red = st["redeclaration_after_leaveall"]
lo, hi = st["last_pdu_after_lv_stopped"]
cl = st["registrar_classes"]
frag["inference"] = "\n\n".join([
    f"The bridge re-declared the stream within {red['max_delay_s']:.3f} s of every Listener-type LeaveAll seen while registered.",
    f"That covers {red['observed']} LeaveAlls: {red['by_sender']['DUT']} own and {red['by_sender']['bridge']} from the bridge; none went unanswered.",
    f"Every capture holds at least {st['min_window_before_lv_s']:.3f} s before its `Lv`.",
    "So an `Lv` with no LeaveAll in its capture came long after the last re-declaration."])
frag["stop_within"] = str(st["within_one_pdu"])
frag["lv_range"] = f"{st['lv_after_disconnect'][0]:.6f}-{st['lv_after_disconnect'][1]:.6f}"
frag["last_after_lv"] = f"between {-lo * 1000:.3f} ms before and {hi * 1000:.3f} ms after"
frag["last_after_disc"] = f"{st['last_pdu_after_disconnect_stopped'][0]:.6f}-{st['last_pdu_after_disconnect_stopped'][2]:.6f} s, median {st['last_pdu_after_disconnect_stopped'][1]:.6f} s,"
frag["classes"] = f"{cl.get('IN (observed)', 0)} IN observed, {cl.get('IN (inferred)', 0)} IN inferred and {cl.get('LV', 0)} LV"
frag["ss_start"], frag["ss_stop"] = str(st["start_stop_sum"][0]), str(st["start_stop_sum"][1])
import hashlib
TOOLS = [("b2_action.py", "acquisition: one locked capture and controller action"), ("run_action.sh", "bench-lock wrapper for one action"),
         ("series.sh", "cycle series, one lock window per cycle"), ("identity_locked.sh", "identity readback and UART grader under the lock"),
         ("b2_analyze.py", "offline replay of one capture"), ("b2_summary.py", "distributions, growth and stop classes"),
         ("b2_pages.py", "page tables from the summary"), ("b2_assemble.py", "page assembly from the tables"),
         ("aecp_identity.py", "ENTITY and CONFIGURATION byte comparison"), ("b2_reconnect.py", "controller transactions for the one pair"),
         ("b2_controller.py", "controller reads; PR #604 copy, import renamed"), ("avdecc_ro.py", "raw AVDECC reader, unchanged from PR #604"),
         ("capture.py", "bounded tap capture, unchanged from PR #604"), ("console_read.py", "read-only console reader, unchanged from PR #604"),
         ("wire_summary.py", "tap decoder, unchanged from PR #604"), ("expected_crc.py", "reference CRC table, unchanged from PR #604"),
         ("census_compare.py", "census comparison, unchanged from PR #620")]
rows = ["| Tool | Role | SHA-256 |", "|---|---|---|"]
for n, role in TOOLS:
    rows.append(f"| `{n}` | {role} | `{hashlib.sha256((p / 'tools' / n).read_bytes()).hexdigest()}` |")
grader = Path(sys.argv[1]) / "scripts" / "baremetal_uart_smoke.py"
rows.append(f"| [UART grader](../../scripts/baremetal_uart_smoke.py) at `13eda870` | identity and restore | `{hashlib.sha256(grader.read_bytes()).hexdigest()}` |")
frag["tools"] = "\n".join(rows)
(p / "summary" / "page-tools.md").write_text(frag["tools"] + "\n")
for name, tmpl in (("606_FIRST_BIND_MEASUREMENT.md", "page-606.template.md"), ("608_75_WITHDRAWAL_AND_RESTART.md", "page-608.template.md")):
    text = (p / "summary" / tmpl).read_text()
    for k, v in frag.items():
        text = text.replace("{{" + k + "}}", v)
    assert "{{" not in text, [l for l in text.splitlines() if "{{" in l]
    (w / name).write_text(text)
    print(name, len(text.splitlines()), "lines")
