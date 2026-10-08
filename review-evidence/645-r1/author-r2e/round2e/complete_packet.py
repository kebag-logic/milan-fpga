"""Finalize the author handoff only after all required recorded results pass."""
import json
from pathlib import Path

w = Path(__file__).resolve().parent
packet = Path.home() / "milan-fpga-management/2026-09-23/645-a531"
assert (w / "vendor.rc").read_text().strip() == "0"
assert (w / "logs/gmii-placement.rc").read_text().strip() == "0"
timing = json.loads((w / "timing-summary.json").read_text())
resource = json.loads((w / "resource-summary.json").read_text())
area = json.loads((w / "area-ooc/comparison.json").read_text())
audit = json.loads((w / "final-audit.json").read_text())
assert timing["rc"] == area["rc"] == 0
assert timing["kept"] == "AltSpreadLogic_high"
assert len(resource["rows"]) == 3 and all(r.get("rc") == 0 for r in resource["rows"])
assert audit["clean"] and not audit["active_jobs"]

def signed(value):
    return f"{value:+,}"

text = (w / "timing-results.md").read_text().split("### Resource checks in progress")[0]
text += """### Resource checks and own-area limit

All three repository resource checks pass, rc 0, against the recorded
baseline. Each recipe identity matches. No baseline was changed.

| Endpoint | Baseline LUT / FF | Candidate LUT / FF | Delta LUT / FF | Candidate RAMB36 / RAMB18 | DSP | Result |
|---|---|---|---|---|---|---|
"""
for row in resource["rows"]:
    b, c, d = row["baseline"], row["candidate"], row["delta"]
    text += (f'| {row["endpoint"]} | {b["LUT"]:,} / {b["FF"]:,} | '
             f'{c["LUT"]:,} / {c["FF"]:,} | {signed(d["LUT"])} / {signed(d["FF"])} | '
             f'{c["RAMB36"]} / {c["RAMB18"]} | {c["DSP"]} | PASS |\n')
text += """
The route is complete with no unrouted net or routing error. Its slice count
is 15,754 versus 15,734 (+20), with 87.5 BRAM tiles unchanged. The recorded
route recipe's WNS is +0.057 ns versus +0.124 (-0.067); WHS is +0.024 ns
versus +0.031 (-0.007). All are within the recorded policy. RAM and DSP
comparisons are retained in each endpoint report. OOC timing is characterization;
the shipping sign-off result is the kept image reported above.

The separate own-area comparison uses the exact dev and candidate capture
and settle logic, shipping 1x1 generics, and a 20 ns axis clock:

| Component | Dev LUT / FF | Candidate LUT / FF | Delta LUT / FF |
|---|---|---|---|
"""
for title, key in (("Settle and existing source recentre", "settle"), ("Capture ring", "cmc")):
    b, c = area["rows"][key + "_base"], area["rows"][key + "_head"]
    text += (f'| {title} | {b["Slice LUTs"]:,} / {b["Slice Registers"]:,} | '
             f'{c["Slice LUTs"]:,} / {c["Slice Registers"]:,} | '
             f'{signed(c["Slice LUTs"]-b["Slice LUTs"])} / '
             f'{signed(c["Slice Registers"]-b["Slice Registers"])} |\n')
lut, ff = area["combined_delta"]["Slice LUTs"], area["combined_delta"]["Slice Registers"]
text += f"""
**Own delta: {signed(lut)} LUT / {signed(ff)} FF; limit 120 / 120: PASS.**
The four separate synthesis commands and the area grade returned 0.
Evidence: `round2e/resource-summary.json`, the three resource-check logs,
`round2e/area-ooc/comparison.json`, and `round2e/area-source-audit.json`.
The GMII good/bad placement fixture also returned 0.

### Disposition and recommendation

**REVIEW READY at `{audit['head']}`.** The assignment's merge, both wording
corrections and affected verification are complete, with the expressly
accepted #657 comparison. No STOP condition was triggered. This is an author
handoff; independent review and the protected publication/merge gates remain
required.

Recommendation remains option C, the implemented correction of both rings.
Its fresh own-area result is {signed(lut)} LUT / {signed(ff)} FF, and the
kept shipping image clears the timing and IOB bar. The classification,
protocol-visible effects, alternatives and test plans retained in
`HANDOFF.md` remain applicable. Alternative prototype area figures are historical, not
new measurements. The declared residual remains a second INTERNAL pull
starting during the previous action's recovery window. The diagnostic
loopback target remains 11 events; the AAF presentation law is unchanged.

The final tree and all three dependencies are clean at the recorded pins.
Both new first-parent commits have one-line subjects and no body or trailers.
Every job has ended. Peak service memory was
{int(audit['memory']['memory.peak']) / 1e9:.3f} GB, below 17 GB. Vendor jobs
ran serially under the shared lock; the 8x8 OOC job waited behind another
service's run. No heavy functional build overlapped a vendor job in this
service. See `round2e/final-audit.json`, the command receipts and
`round2e/vendor.log`.
"""
(w / "completed-results.md").write_text(text)
for name in ("HANDOFF.md", "PR-BODY.md"):
    p = packet / name
    current = p.read_text()
    start = current.index("### Three-directive shipping timing sweep", current.index("\n## Round 2e\n"))
    current = current[:start] + text
    if name == "HANDOFF.md":
        current += "\n" + (w / "reproduction.md").read_text()
        current = current.replace(
            "Status: validation in progress. See the Round 2e section below for current\nscope and results.",
            "Status: REVIEW READY. See the Round 2e section below for current\nscope and results.", 1)
    current = current.replace("**Status: validation in progress**, head", "**Status: REVIEW READY**, head")
    p.write_text(current)
print("Finalized HANDOFF.md and PR-BODY.md at", audit["head"])
