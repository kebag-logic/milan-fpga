[R625] NEGATIVE - exact head 35e332b6be3de2b36c4aec0f1d0bc9f390447b74

Round R625-2, external independent review of issue #629 / PR #725.
Tree: `870785667820e5cae10f060bbd48d0b524db4aeb`.
Comparison: `c20c85bd..35e332b6be3de2b36c4aec0f1d0bc9f390447b74`.

All five lenses were applied independently. The four prior MINOR findings
and both prior wording residues are resolved. One additional MINOR numerical
discrepancy remains. It changes no bench conclusion and alleges no DUT defect,
but the round's requirement that every figure match its receipt remains unmet.
Conformance, Tests and Docs are therefore UNCLEAN.

The four commits change only the findings page and its index. No RTL,
firmware, executable test, configuration, generated image or gitlink changes.
The measured image is dev `5603c353`, distinct from this documentation head.

**Scope and evidence**

Reconstructed from `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, the
[issue contract](https://github.com/kebag-logic/milan-fpga/issues/629),
the [B16 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187),
the [B16b ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835),
the [B16c clock exception](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090),
and the [round-2 scope](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119316763).
Technical authorities include `REQUIREMENTS.md`, FR-CLK-03/04 at
`docs/reference/FR_NFR.md:252`, the media-clock design's clause findings and
bench cases, and the register map's slip, meter and servo fields.

Evidence paths below refer to `author-r2/` in the immutable
[published packet](https://github.com/kebag-logic/milan-fpga/tree/7affd6015fd3bb56ef0fbd37499be3c6f188d9b3/review-evidence/629-b16-r1).
All 499 publication hashes, 62 cited evidence hash/size rows and 40 raw-inventory
rows check. Inventory equality verifies citations, not unavailable raw bytes.
No private author material or other reviewer's packet was read. The independent
verdict and ledger were written before reading the two prior public findings
comments. Their subsequent reconciliation is recorded below.

**R625-2-F1 - MINOR - Conformance, Tests, Docs**

Artifact: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3189`.

Finding: the B16c attribution table says point (a) is at **-123.98 dB median
on both tones in both cases**. B-CRF's 9,973 Hz value is **-123.9703 dB**,
which rounds to **-123.97 dB**. The detailed table at line 3071 already gives
the correct -123.97 dB.

Authority/evidence: round-2 item 1 requires every figure to equal its receipt.
`summary/bcrf/a-peer-tap.json`, channel 1, `tone_9973.median.thdn_db`, is
-123.9703. Independent recomputation of the published per-block median agrees;
see `receipt-audit.json`, `remaining_figure_discrepancy` and `point_medians`.

Impact: the aggregate attribution row disagrees with its receipt and its own
detailed table by 0.01 dB at the displayed precision. This does not reverse
the path-floor result, but it is a numerical claim rather than wording-only
RESIDUE under the owner's rule.

Required outcome: preserve the four measured medians. An exact replacement
for the evidence cell is: "At (a), medians are -123.98/-123.97 dB for B-CRF
and -123.98/-123.98 dB for B-AAF (997/9,973 Hz); every worst block is
-123.93 dB."

Verification: compare that row against `summary/{bcrf,baaf}/a-peer-tap.json`
and the detailed table. Re-run the receipt arithmetic after correction.

**R625-2-S1 - SUGGESTION - Docs**

Artifacts: `tools/census_cmp.py`, `restore/census-*.jsonl`, and the findings'
census descriptions. Retains R625-1-S1 / R624-1-S1 as optional.

Authority/evidence: each 46-entry census contains a header and 45 reads.
The published statement "45 of 46 entries equal" is true under that definition.
Impact: readers may mistake entries for device reads. Optional outcome:
use "44 of 45 reads equal" when excluding the header. Verification:
exclude only the `type=start` row before comparing. This suggestion does
not prevent clean lens coverage.

**Prior public findings, explicitly dispositioned at this head**

Read the [R624-1 findings](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119236428)
and [R625-1 findings](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119311570)
only after the independent pass. There were no formal reviews or inline comments
in the inspected public inventory. No current-round review report was consulted.

| Prior item | Disposition and evidence |
|---|---|
| R625-1-F1, Conformance/Tests/Docs | RESOLVED. Findings at lines 2782, 2800 and 3201, index line 15 and the live PR body keep 131 at (c), demonstrate 23 within the 34.1136-second overlap, and label the other 108 as inferred upstream. Counts independently reproduced from block inventory and both alignments. |
| R625-1-F2, Tests/Docs; R624-1-S2 | RESOLVED. Two public poll traces and reduced receipts expose extrema and every slip transition with servo states. Source receipt contains the meter levels and neutral state comparisons. Raw hashes and extraction procedures are published at line 3340. All 1,420 trace rows were decoded; twelve source-read hash bindings checked. Private source reads/map were not regenerated. |
| R625-1-F3, Conformance/Tests/Docs; R624-1-F1 | RESOLVED for all three original figures. B0 floor medians are -123.98/-123.95 dB; degraded runs split at block 45; recording begins about 06:38:05.2, 26 seconds after binding, including the two-second playback lead. `r2/b0-2-receipt.json` reproduced byte-for-byte. The separate F1 above concerns a different B16c figure. |
| R625-1-F4, Conformance/Tests/Docs; R624-1-F2 | RESOLVED. Lines 3145-3154 state all four B6 terms for both following cases. Three are met; timed ratio is NOT RUN with no decision replacing it. Acceptance, limits, index and PR body preserve that qualification. |
| R625-1-R1 / R624-1-R1, Docs | RESOLVED. The live PR title exactly matches the previously requested title, distinguishing graded B0 from the following cases at the floor. |
| R625-1-R2 / R624-1-R2, Docs | RESOLVED. Method, counter header and counter discussion identify the first mark 20 seconds after the set, about six seconds before recording. Events give 20.019/20.016 seconds after setting and 6.005/6.004 seconds before recording for B-CRF/B-AAF. |
| R625-1-S1 / R624-1-S1, Docs | RETAINED OPTIONAL as S1 above. |

**Results by lens**

Conformance is UNCLEAN solely for F1. Checked the frozen STOP/resume decisions,
format adaptation, one selected source, permitted exception and restore.
`summary/loop2/acmp-peer-tap.json` shows two unanswered CONNECT_TX commands
200.015 ms apart. Both loopback runs have fourteen listener polls with zero
received frames and no media lock; the external captures are zero. B16b
correctly stops before circular following. B16c has all eight source sets
read back successfully in controller responses: peer INTERNAL, DUT CRF/AAF,
DUT INTERNAL, then peer CRF. All nine runs' final records equal their starts.
Every lane census and the full B16-start to B16c-end census have 45/46 equal
entries, with only live propagation delay changed. The INTERNAL mismatch
control remains NOT RUN and #629 remains open.

[R625] PASS RTL - complete two-file diff; `docs/overview/ARCHITECTURE.md:72`;
`docs/reference/REGISTER_MAP.md:1870`, `:2076`, `:2139`; public poll traces -
checked the ownership and decoding of the measured interfaces. Source indices
0/1/2, servo state 4, signed 1/16-ppm trim, rates at 512 units/ppm, and
`0x001e0007` agree with the authorities. No implementation change or new RTL
execution is claimed. Both window traces decode to 596 LOCKED polls; trim
is -6.125 to -6.000 ppm. B-AAF shows enabled/locked/rate-valid, zero history
restarts and 30 ns maximum timestamp deviation.

[R625] PASS Robustness - `runs/{loop1,loop2,b0}/events.jsonl`,
`runs/{bcrf,baaf}/ctl.jsonl`, `restore/census-*.jsonl`,
`tools/run_b16c.py`, `controls/b16c-dryrun-*.json` and wrapper deadline receipt -
examined unsuccessful loopback, busy-capture exclusion, refused set, absent
lock, controller loss, deadline teardown and restoration order. The eight
published dry-run outcomes were inspected, not re-executed. The empty B0
incident capture is ungraded. Independent synthetic reduction probes reject
altered raw bytes, expose a post-lock slip, and adjust attribution when tap
coverage shrinks. Actual traces contain five pre-set IDLE slip steps per case,
then one/two ACQUIRE steps; none after observed LOCKED. No new bench action ran.

Tests is UNCLEAN for F1's test-result claim. Independent arithmetic verifies
the 20 detailed point-table THD+N rows, all six output grades and overlaps.
B0 has 169 floor and 131 degraded blocks; 23 degraded blocks are wholly in
the common overlap, 108 beyond it. Both following cases have 300/300 floor
blocks, no reported discontinuity, and median -123.98/-123.97 dB at (c).
Direct comparisons cover 34.2-34.3 seconds of each 300-second following run.
The reduced traces reproduce extrema and slip brackets to their published
time precision. Both source-clock restores and the full binding restore
are checked against controller/census records. DUT clock counters move
22/21 to 24/23; peer counters 6/5 to 8/7; both DUT outputs' MEDIA_RESET
counts move 0 to 4. These are receipt checks, not fresh hardware measurements.

Docs is UNCLEAN solely for F1. Examined both changed pages, PR body, gate
receipts, hash tables, source attribution and extraction instructions.
The source routing and clock changes are attributed outside the lane.
Measured overlap and later inference remain distinct in all three public
summaries. The reduced receipts use neutral roles and disclose their private
raw/map limitation. Added prose preserves peer/capture anonymity and host-path
privacy. Documentation checks pass; no normative requirement or compliance
status is silently promoted.

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | Issue/rulings; FR-CLK-03/04; findings:3189; B6 criterion; loopback decode; clock responses and final states | R625-2 applied; no clean coverage | 35e332b6be3de2b36c4aec0f1d0bc9f390447b74 |
| RTL | CLEAN | Complete diff; architecture:72; register map:1870, :2076, :2139; both raw-word poll traces; required gitlinks | R625-2 | 35e332b6be3de2b36c4aec0f1d0bc9f390447b74 |
| Robustness | CLEAN | Failure/incident events; run teardown; eight published dry-run outcomes; deadline receipt; restoration responses; independent fault probes | R625-2 | 35e332b6be3de2b36c4aec0f1d0bc9f390447b74 |
| Tests | UNCLEAN: F1 | Published point/grade/alignment JSON; numerical tables; poll traces; source reduction; controls and probes | R625-2 applied; no clean coverage | 35e332b6be3de2b36c4aec0f1d0bc9f390447b74 |
| Docs | UNCLEAN: F1 | Findings and index; live PR body/title; all new hash rows; extraction procedures; documentation checks | R625-2 applied; no clean coverage | 35e332b6be3de2b36c4aec0f1d0bc9f390447b74 |

**Executed checks and reproducibility**

Scripts accept repository, public evidence and output locations as arguments.
All temporary copies and dependencies stay under packet `scratch/`.
Independent checks ran concurrently inside a waited foreground process,
at most four children, with numerical-library threads limited to one.

| Check | Result / receipt |
|---|---|
| `audit_receipts.py` | PASS for receipt consistency; `receipt-audit.json` separately identifies F1 |
| Published alignment controls | 6/6 PASS, byte-equal to published result; `checks/alignment-controls.json` |
| Published tap/presence controls | 8/8 PASS, byte-equal; `checks/tap-controls.json` |
| Published synthetic tone/slip/drift controls | 20/20 PASS, byte-equal; `checks/grade-controls.json` |
| B0 receipt regeneration | Byte-equal; `checks/b0-recomputed.json` |
| `probe_reductions.py` | 5/5 PASS; `reduction-probes.json`: overlap boundary, signed-word decode, raw-hash refusal, post-lock slip/summary mismatch, source value/hash extraction |
| Seven focused documentation/whitespace checks | Final rc 0; `checks/results.json`, `checks/results-retry.json`, per-check logs and rc files |
| `verify_checkout.py` | PASS; `checkout-integrity.json`: 1,291 candidate blobs and 880 required-submodule blobs, modes and indexes equal their pinned trees |

Three renderer-dependent checks initially exited 2 because the reviewer
driver resolved the disposable environment's executable symlink. Keeping
the environment launcher path fixed that setup error; only those three
checks were repeated. Initial exit statuses remain in `checks/results.json`;
per-check logs/rc files show the final attempt. This was not a source failure.

The author's `gates/r2/results.json` names the exact reviewed head and has
14 successful entries, including two environment-version checks. A copy is
`author-gates.json`. These are the published source validation receipts;
there is no manager source-bank run at this head, and none is inferred.
Hosted checks were not polled in this round; their acceptance and the local
workflow replica remain the manager's duties. A skipped context is not an
executed suite or hardware proof.

**Real limits and pending manager duties**

No hardware access, private captures, source edits, commits, remote writes,
full parent/processor/synthesis/builder banks or local workflow replica ran.
No simulator was invoked. The raw audio/tap captures and full poll files
remain privately retained and hash-listed. Poll extrema were reconstructed
from public raw-word traces; source measurements were checked against their
neutral receipt and hash inventory, with synthetic extraction controls.
Private source classification cannot be independently verified here.

There is one 300-second run per following case on one DUT/reference-peer
pair. Direct sample equality covers only the tap overlap. The timed ratio
and INTERNAL mismatch control were NOT RUN. Physical calibration was NOT RUN;
printed precision, field skips and desk controls provide no calibrated
hardware or release-campaign proof. #645 and the remaining #629 acceptance
stay open. This findings-only review does not close them.

The manager must publish this packet, correct F1, obtain independent re-review
of the affected lenses and both required positive reviews, and ensure no
review remains in flight. S1 stays optional; both prior residues are resolved.
This verdict is not merge authorization.

Source-head validation remains separate from final current-dev candidate
validation. At the merge turn, the manager must combine the corrected reviewed
lane (source base `c20c85bd`) with then-current dev (provided tip
`c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`), execute the required builder and
native banks, link exact-candidate receipts, judge hosted/local-replica evidence,
and perform post-merge containment after an authorized merge. This report
supplies no candidate-bank result.

R625-2 FINISHED
