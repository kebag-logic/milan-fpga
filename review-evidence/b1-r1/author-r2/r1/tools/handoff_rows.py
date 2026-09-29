"""Refresh the step-3 per-cycle table in HANDOFF.md from bench/cycleNN/check.txt."""
import json, re
from pathlib import Path
P = Path(__file__).resolve().parent.parent
rows = []
for f in sorted(P.glob("bench/cycle*/check.txt")):
    lines = f.read_text().splitlines()
    r = json.loads(lines[0])
    md, mu = r["mac_down"] or {}, r["mac_up"] or {}
    rows.append("| %s | %.2f | %s (%s) | %s-%s / %s-%s | %s | %s / %s | %s |" % (
        r["cycle"][-2:], r["off_s"], r["link_down_up"], r["link_counters"], md.get("last_up_before"),
        md.get("first_down"), mu.get("last_down_before"), mu.get("first_up"), r["recovery_s"],
        "both recovered" if lines[1] == "RECOVERED" else "NOT recovered",
        "held" if r["bindings"]["all_connected"] else "LOST", lines[1]))
s = (P / "HANDOFF.md").read_text()
head = "| Cycle | OFF (s) | LINK_DOWN / LINK_UP delta | MAC_STATUS down / up | gPTP recovery (s) | Streams / bindings | Result |\n|---|---|---|---|---|---|---|\n"
start = s.index(head) + len(head)
end = s.index("\n## Per-step table")
s = s[:start] + "\n".join(rows) + "\n" + s[end:]
(P / "HANDOFF.md").write_text(s)
print("\n".join(rows))
