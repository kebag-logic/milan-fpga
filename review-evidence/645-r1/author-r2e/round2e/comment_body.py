"""Prepare the authorized issue handoff from completed result records."""
import json
from pathlib import Path

w = Path(__file__).resolve().parent
assert (w / "vendor.rc").read_text().strip() == "0"
audit = json.loads((w / "final-audit.json").read_text())
area = json.loads((w / "area-ooc/comparison.json").read_text())
resources = json.loads((w / "resource-summary.json").read_text())
timing = json.loads((w / "timing-summary.json").read_text())
assert audit["clean"] and not audit["active_jobs"]
assert area["rc"] == timing["rc"] == 0
assert all(row.get("rc") == 0 for row in resources["rows"])
lut, ff = area["combined_delta"]["Slice LUTs"], area["combined_delta"]["Slice Registers"]
text = f"""[A531] REVIEW READY — Round 2e

Commit: `{audit['head']}`

Merged dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240` with `--no-ff` as `9a0d68e2016c0385171107277721aa187ce19674`. The merge is automatic, with no conflict resolutions. Processor pin is `2ad2f845dd583f8310075fa2380cb60a04fd091a`; the other pins remain `5dce647a` and `48ff7a7e`. R474-3-R1/R2 are fixed in the mutation-driver docstring and TESTING.md: the complete twelve controls, including all four capture controls, are documented. No RTL was authored in this round. Both new commits have one-line subjects and no body or trailers.

Shared infrastructure triggered the full validation set. Credited commands returned 0, with the assignment's explicit #657 comparison below:

- `scripts/run_all_suites.sh` shards `0/2` and `1/2`: **61/61 suites, 2,185,760 checks, zero failures**. The `--physical-gptp` leg passes **197 checks**; both wire recentres declare and observe -5 events, with dup/skip counters unchanged.
- follow_ring default passes; **12/12 controls caught**, small pulls **10/10**, four controller clock rates. Capture ring: **785 behavioral + 20 netlist checks**, zero failures.
- Arrival campaign `--jobs 16`: **128/128**, byte-identical logs to Round 2d. All 384 post-settle windows have zero slip; minimum empty/full margins **2.17344 / 2.23488 ticks**. Quiet reader: **128 phases / 512 windows, peak 1 axis cycle against band 2**.
- Standalone INTERNAL pull-in: **32/32**, byte-identical to Round 2d; **28 on-law, four ambiguity-band cases not gradable**. All have one recentre and zero post-settle slip. Four 56-us cases have one pre-settle slip, unchanged from Round 2d.
- `make -j16 tdm8render-pullin PULLIN_JOBS=16`: **18/18 phases, 558 checks**, all gradable, no slip during the pull or after settling. `tdm8render-law-boundary LAW_BOUNDARY_JOBS=16`: **81/81 over 564 windows**, largest walk **3 cycles** against the stated bound of 5.
- Firmware unit/NVM/RV32/coverage/image checks pass. Four `--slice K/4 --jobs 4` campaigns catch **469/469** controls exactly once. Specification suite: **14 features / 404 scenarios / 1,968 steps**. Builder passes gate 23h and **5/5** missing-patch controls; build-environment simulations **5/5**, controls **10/10**. GMII fixture: **1,036 comparisons**, **6/6** structure controls; good/bad placement fixture passes.
- Portability **58/58**, tied-input and tap-purity checks pass; vendor front-end has zero findings; source/documentation gates **28/28**.

**#657:** `tdm8render-mutants` gives dev **28/32**, candidate **30/34**, both rc 2. Every shared outcome and all four failing lines match. The candidate's clean pull-in and missing-settle controls add two passes. No merged-suite regression is observed; the full mutation gate is not claimed clean.

Shipping timing sweep, worst setup / hold in ns:

| Directive | Setup | Hold | Full IOB | Disposition |
|---|---:|---:|---|---|
| ExtraPostPlacementOpt | +0.057 | +0.024 | 21 PASS / 1 INERT / 0 FAIL | Meets margin |
| AltSpreadLogic_high | +0.066 | +0.024 | 21 PASS / 1 INERT / 0 FAIL | **Kept** |
| ExtraTimingOpt | +0.011 | +0.036 | 21 PASS / 1 INERT / 0 FAIL | Below +0.030; not selected |

All twelve corner reports have zero TNS/THS and failing endpoints. All nine GMII RX registers pack into ILOGIC in every row. Each implementation, constraint check and manifest returns 0; critical warnings: zero. This passes the #691 best-image ruling. Kept bitstream SHA-256: `7b0c5eead7a68221c47e1f16077ec8ddbc3ca3631a033ff3e5e9235881c09977` (3,825,992 bytes).

`pp_resource_gate.py check` against the recorded baseline:

| Endpoint | Baseline LUT / FF | Candidate LUT / FF | Result |
|---|---|---|---|
"""
for row in resources["rows"]:
    b, c = row["baseline"], row["candidate"]
    text += f'| {row["endpoint"]} | {b["LUT"]:,} / {b["FF"]:,} | {c["LUT"]:,} / {c["FF"]:,} | PASS, rc 0 |\n'
text += f"""
The route endpoint uses its recorded ExtraPostPlacementOpt recipe, has no routing errors, and uses 15,754 slices versus 15,734 (+20). No baseline was changed. Fresh own-area OOC delta versus dev is **+{lut} LUT / +{ff} FF**, within **120 / 120**.

The optional external TSN field campaigns were skipped because their generator is absent. Builder gate 11's historical Arty calibration arm was NOT RUN because its report is absent. These are not credited; hardware and bench campaigns remain outside this assignment. Failed setup and interrupted partitioning attempts are retained separately from the complete passing runs.

HANDOFF.md and PR-BODY.md retain earlier rounds and now contain Round 2e results, reproduction commands, traces, classification, options and recommendation. The packet records sizes and SHA-256 for large artifacts and contains no file over 200 KB. The tree and dependencies are clean; all jobs have ended; peak service memory was {int(audit['memory']['memory.peak']) / 1e9:.3f} GB, below 17 GB. No STOP condition was triggered. Ready for independent review at the commit above.
"""
(w / "review-ready.md").write_text(text)
print("Prepared issue handoff:", len(text.encode()), "bytes")
