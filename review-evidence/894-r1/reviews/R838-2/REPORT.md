[R838] NEGATIVE - exact head 8a3791e44533d6b1cc26d486d0b18e7d83470dc1

R838-2 independently applied Conformance, RTL, Robustness, Tests and Docs. Two MAJOR findings and one MINOR remain open. The reproduced model passes its stated 1x1/1if bounds, but the join-interval grader can omit late intervals, and the map rewrite retains quadratic work on an adversarial, legal-length command. Neither probe establishes an observed target-CPU deadline violation.

The reviewed tree is `3387d98b5f115d86cbb60ac303d5271d697e4584`. The review reconstructed the repository contract, documentation map, frozen issue scope and public rulings before examining the requested `66f713267f201d1a00d7f711e04b3a996d804dee..8a3791e4` diff and history. Delta work was assessed against `12180198b087d4cfdd531d0de5d3753211b35616`, accounting for the imported #810 base `cec88385` and merge `ccb47e39`. The independent verdict and five-lens ledger were written before consulting either prior review. No private author material or other current-round report was used.

**Authority and evidence.** The controlling decisions are [6844175391](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6844175391), [6845846512](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6845846512), [6848507008](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6848507008), [6857835707](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6857835707), the [contingent ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6858269025), and its [130 ms amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874). These amend project budgets associated with Milan v1.2 4.2.7.1.1/Table 4.3, IEEE 802.1Q-2018 10.6/10.7.11, and IEEE 1722.1-2021 9.3.2.6. Evidence examined includes the [published author-r7 packet](https://github.com/kebag-logic/milan-fpga/tree/6f321a998afb177721373be74100a0d84b199ab5/review-evidence/894-r1/author-r7), its root manifest, and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867318907). Packet-relative paths below refer to that archive unless prefixed `checks/`, which identifies this review's receipts.

**R838-2-F1 — MAJOR — Conformance, Robustness, Tests, Docs — late join intervals disappear from the gate.**

- Artifact: `tb/verilator/ctrl_service_budget/mrpdu_grade.py:25,41`; `join_grade.py:30,49`; `run.py:171`. Reproduction: `probe_join.py`, `checks/join_horizon.log`.
- Authority/evidence: contingent item 4 requires the join gate to catch intervals outside 180–240 ms. `join_grade.released()` delegates to `mrpdu_grade.released()`, which searches only 100 ms after the timer callback. Its comment claims a late build becomes an over-budget row, never no row. The probe supplies two MSRP commits for one participant, a join expiry between them, a corresponding build and work pass, and no competing timer or empty intervening build. Intervals of 191 ms pass; 241 and 289 ms fail. At 291 and 500 ms, the result is `count=0, over=[]`: the late build is outside the horizon. The run-level failure list consumes `over`, so this interval supplies no failure. The horizon also affects the timer-to-MRPDU rows.
- Impact: a sufficiently delayed build can evade both checks. The reported 52 intervals and existing planted defect do not establish that every late interval is detected. This is a grader false negative, not evidence that real firmware produced a 291 ms interval.
- Required outcome: distinguish a completed empty build from a late, absent or unresolved build; do not silently classify an unobserved build beyond a finite horizon as no obligation. Preserve the legitimate idle-timer case described by the corrected definition.
- Verification: add controls spanning the horizon, including a late eventual commit and an unresolved pending obligation, while retaining empty-build/idle-request exclusions. The supplied 291/500 ms cases must no longer disappear. Recheck published interval receipts with the corrected gate.

**R838-2-F2 — MAJOR — Conformance, RTL, Robustness, Tests, Docs — the map rewrite retains a quadratic collision path.**

- Artifact: `sw/firmware/ctrl/aecp/aecp_maps.c:127,162,340`; `tb/verilator/ctrl_service_budget/long_notice.py:9`; `rows_tiers.py:127`. Reproduction: `probe_maps.py`, `checks/map_probe.log`.
- Authority/evidence: ruling 6848507008 requires #904's single decode and O(n) duplicate/conflict checking without rescans, with behavior preserved. `match()` linearly scans the occupied run from a hash of the destination key. Distinct input mappings sharing a destination key occupy successively longer runs. ADD stops on a conflict; REMOVE first builds the complete table. A disposable copy counted loop iterations on REMOVE commands with distinct stream indices and the same input destination: **36, 136, 528 and 2,016** for 8, 16, 32 and 63 mappings, exactly n(n+1)/2. The 63-mapping command is 550 bytes and within the legal-length envelope. It is rejected BAD_ARGUMENTS, but table construction precedes rejection. This is not #903's oversized-command case.
- Impact: decoding each row once does not establish linear duplicate/conflict work. The published largest-notice group repeats one mapping, so it does not exercise this collision family. Its 89,126-cycle record maximum, stated at 940 us after padding, cannot by itself establish the maximum over this newly identified path. No target-cycle measurement of the collision case was made here; this report does not claim it exceeds 940 us or puts txL over 50 ms.
- Required outcome: satisfy the ruled bounded-work requirement for rejected as well as accepted legal-length commands, preserving status, validation precedence, duplicate-removal multiplicity and atomicity. Include adversarial collisions in cost evidence. A different complexity contract requires a public scope decision.
- Verification: retain the existing definition test unchanged; add maximum-length collision/conflict cases that detect repeated rescanning. Re-measure affected record costs with the required padding and recompute affected rows. The existing **4,000-edit definition test** and restored-output ownership test both pass alongside this probe; semantic success does not clear the complexity defect.

**R838-2-F3 — MINOR — Conformance, Docs — numeric timing contracts disagree with the amended build.**

- Artifacts: `docs/reference/FR_NFR.md:415`; `sw/firmware/ctrl/aecp/README.md:120`; `docs/design/MAILBOX_SPLIT.md:390`.
- Authority/evidence: FR_NFR's new paragraph correctly derives 50 ms from 240 minus the armed 190 ms, but its SRP table still states **40 ms**, derives that from **200 ms**, promises commit within 40 ms, and states a periodic interval of **960–1040 ms**. The header derives 50 ms and describes 1000 ±50 ms. The AECP README states the last queued notice's bound as **125 ms**, while the amendment and code hold 130 ms. MAILBOX_SPLIT states the one-interface slice as **0.8 ms**, while the built slice is 900 us. This retains the cause of both earlier stale-slice findings, although the old 1.05 ms text was replaced.
- Impact: a reader following the authoritative table or interface description obtains a different contract from the ruling and executable model. These are numeric/clause claims, not wording-only residue.
- Required outcome: reconcile these statements with the scoped current exceptions, keeping historical measurements explicitly historical. Cite the contingent ruling/amendment where FR_NFR changes; distinguish the original 20 ms measurement target from amended every-source budgets rather than silently extending exceptions.
- Verification: compare amended prose with `CTRL_LOOP_JOIN_CS`, `CTRL_LOOP_TX_BOUND_MS`, `AECP_QUEUED_MS`, `CTRL_LOOP_SLICE_US`, and the exact-head model. Re-review Docs and Conformance at the corrected head.

**R838-2-R1 — RESIDUE — Docs — new source comments identify review rounds or issue-comment IDs.**

- Artifacts: under `sw/firmware/ctrl/`, `aecp/aecp_mbx.h:44,58` and `loop/ctrl_loop.h:265,330`; under `tb/verilator/ctrl_service_budget/`, `flip_grade.py:180`, `join_grade.py:3`, `load_grade.py:235`, `notice_window.py:61`, `paced_rows.py:3,35`, `queued_bound.py:3,4`, `rows_tiers.py:114`, `run.py:190`, `selftest_polls.py:251`, `tier1_rows.py:32,213`.
- Authority/evidence: these additions since the previously reviewed head contain `issuecomment-6858269025`, `issuecomment-6862465874`, or “round 5”. The owner's comment rule permits issue/requirement IDs and behavior/reason, but excludes those identifiers. Assertion strings and pre-existing #746 residue are excluded from this finding.
- Impact: wording violates the convention; the cited behavior and calculations need not change.
- Exact fix: replace `#894's contingent ruling issuecomment-6858269025` with `#894's contingent ruling of 2026-11-13`, and the amendment identifier with `#894's amendment of 2026-11-13`; remove `on round 5`, retaining date, item, #904/#908 and requirement references. Apply equivalent replacements to wrapped phrases.
- Verification: scan added comments/docstrings; executable text, measurements and clause claims remain unchanged. Non-blocking residue.

**R838-2-R2 — RESIDUE — Docs — the handoff points final rows at an earlier receipt.**

- Artifact: `author-r7/HANDOFF-r7.md`, section 0, opening receipt reference.
- Evidence/impact: it names `receipts/model/rows-1x1-final.txt`, whose header identifies `2953091` and whose rows precede the 725 us restatement (last 117.19; txL 49.70). The handoff's actual final figures are correct and supported by another exact-head receipt.
- Exact fix: change that prose reference to `receipts/gates/lane-flip_check_1x1.txt`. Preserve the historical receipt/header. No measurement, figure, verdict or clause claim changes.
- Verification: the replacement receipt names `8a3791e4` and prints last 125.84 and txL 49.99. Non-blocking residue.

**Earlier findings, resolved or retained at this head.** Sources: [R838-1](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6840525113) and [R837-1](https://github.com/kebag-logic/milan-fpga/pull/902#issuecomment-6840357283), read after the independent pass.

| Prior finding | Disposition and cause-level evidence |
|---|---|
| R838-1 F1: missing other tier-1 rows | Resolved. `tier1_rows.py`, `rows_tiers.CHANNEL_ROWS`, and `flip_grade.channel_controls` cover ACMP/ADP/MAAP at the authorized 30 ms bounds. Reproduced rows and missing-channel controls pass. |
| R837-1-1: legal notices exceed 128-byte slots | Resolved at its original cause. Slots now hold 552 bytes; `QueuedBurst.ABurstOfTheLargestLegalNoticesIsQueued`, the slot-size control, `long_notice.py`, R4L and txL cover the legal envelope. R4L's 240 ms exception and large-notice charge are public decisions. F2 is a distinct cost-path defect. |
| R838-1 F2 / R837-1-2: unruled MRPDU bound/lost proof | Implementation/scope cause resolved: public decisions establish the 50 ms derivation, `ctrl_loop.c:203` restores the compile-time comparison, and tx/txL are every-source rows. Documentation remains open as F3; F1 separately limits the interval gate. |
| R838-1 F3: longer notice forgotten after queue drains | Resolved. `test_aecp.cpp:1723`, `Queued.AfterTheQueuesLastNoticeTheLongerOneIsStillOwed`, exercises a pending longer notice and coincident lock expiry. Independently ran the unchanged test and exact removed-`a->notify` mutant: baseline passes; mutant fails at “and runs no lock expiry beside it”. `checks/prior_owed.log`. |
| R838-1 F4: ordinary round retains `round_one` | Resolved. `test_port_loop.cpp:1674`, L28, leaves THE DRAIN pending so a later whole pass cannot hide the error. Baseline passes; deleting the ordinary-pass clear fails its named assertion. `checks/prior_round.log`. |
| R838-1 F5 / R837-1-3: stale slice | Retained as F3. The text changed numerically but still disagrees with the built slice. |
| R838-1 F6: other tier-1 channels described as serialized | Resolved. `MAILBOX_SPLIT.md:388` now says each its due, then one per channel in turn; `ctrl_loop.c` implements that rotating sweep. The replacement published PR body does not repeat the old claim. |
| R838-1 F7 / R837-1-5: unconditional Domain/VLAN invariant | Resolved. `srp/README.md:240` allows the intervening ordinary pass and conditions licensing on `vlan_sent`; `srp_mbx.cpp:1598` tests the gap; `srp_transmit_mutants.py` plants premature licensing. `srp_mbx.c` preserves the guard and resume/reset behavior. |
| R837-1-4 / R838-1 S5: 8x8/2if called undecided | Resolved. Current descriptions name the decision/#872 and report rather than hold the rows. The newly reported 1,550 us build is expressly refuted, not claimed to pass. |
| R838-1 RS1 / R837-1-6: old round identifiers | Original instances resolved by dated decision references. New instances are R1; earlier cleanup does not cover later comments. |

**Optional findings retained for one author pass.** Each is SUGGESTION and does not prevent clean coverage on its own.

| ID / lenses / artifact | Authority/evidence and impact | Optional outcome and verification |
|---|---|---|
| R838-2-S1; Docs; `aecp/README.md`, owed-queue ordering (prior R838 S1) | A later controller's response can precede an earlier command's queued notice. Applying that later-arriving notice can cache the older value. The public ordering decision permits this; no new protocol violation is asserted. | State the accepted consequence beside the rules; illustrate two controllers editing the same field and compare response/notice order. |
| R838-2-S2; RTL; `aecp.c:708` (prior R838 S2) | The drain still resets `counter_event`, already reset by the command header. The earlier round identified the redundant defensive assignment; the delta does not make removal necessary. | Keep with a guard rationale, or remove if the invariant is demonstrated; run queue/retry tests. |
| R838-2-S3; Tests; `tests/steps/aecp_owed_notice_steps.py` (prior R838 S3 / R837-1-8) | The scenario layer remains an offline model pinned by strings. Native `Queued.*` supplies execution evidence, so this is not a missing acceptance test. | Drive a compiled implementation from a scenario; a behavioral mutation should fail without changing an anchor. |
| R838-2-S4; Tests; `long_notice.py`, `datapath-events` measurements (prior R838 S4) | Earlier datapath estimates rested on 8/16 instances. Current summaries add reruns but not a full per-term maximum/sample inventory. Largest-notice inputs repeat equal mappings; the blocking collision issue is F2. | Publish per-term counts/maxima and broaden adversarial inputs; verify maxima against raw records and the padded table. |
| R838-2-S5; Tests; `rows_tiers.py:686` (prior R837-1-7) | `least_margin` scores an unsolved row -1, potentially above a solved row missing by more than its bound. It does not alter the current passing 1x1 selection. | Rank unsolved rows below solved candidates; add a mixed solved/unsolved ordering control before using this optimization at another point. |

**Results by focus area.** The independent 1x1/1if rows match `receipts/gates/lane-flip_check_1x1.txt`. `checks/flip.log` and `checks/model_audit.json` record the results and complete model inputs.

| Row | Model W, ms | Current bound, ms |
|---|---:|---:|
| R4 | 12.82 | 20 |
| R4L | 158.34 | 240 |
| ACMP | 28.35 | 30 |
| ADP | 26.76 | 30 |
| MAAP | 26.88 | 30 |
| First notice | 14.50 | 20 |
| R5 | 72.71 | 90 |
| R6 | 68.62 | 90 |
| Last notice | 125.84 | 130 |
| tx | 29.78 | 50 |
| txL | 49.99 | 50 |

The model includes channel bursts/refills, timer/TICK/GM sources, coalesced datapath events, polls, owed items, retained retries, builds, rounds and aged steps. Channel and dropped-source controls were exercised: **555/555 flip, 969/969 tier, 25/25 load controls** pass independently. Load is **0.513** at the pin and **0.509** in the second column, both below 0.70 (`checks/load.log`). The model selects **900 us**, **P=6**, **19 cs**. `CTRL_LOOP_TX_BOUND_MS` derives from `240 - 10 * CTRL_LOOP_JOIN_CS`; the queue bound rounds up to the next 5 ms under the amendment, giving 130 ms. These results do not clear F1/F2.

Cost padding was checked on exposed maxima: largest record 89,126 cycles -> **940 us**; largest notice 34,359 -> **365 us**; #908 send 4,744 -> **50 us**; decline 1,589 -> **20 us**; historical base maximum 19,159 -> **205 us**; SRP build of one 68,951 -> **725 us**. Datapath 31.96/29.06/23.33 us becomes 35/35/25 us. Conversions use maximum ×1.05, rounded up to 5 us (`audit_model.py`). At 8x8, 6,134/1,550 cycles give send/decline 65/20 us; 147,613 gives the reported 1,550 us build.

Unchanged cost assessments carry forward where dependencies are unchanged; imported #810 increases were read against the merged tables and attribution. **I do not certify a newly established maximum-plus-5% for every term at this source head.** Published exact-head summaries report failures and selected maxima, not a complete maximum inventory. No STATED failure proves measured cost <= stated cost, which alone is weaker than measured cost ×1.05 <= stated cost. The arithmetic checks validate the exposed maxima; F2 identifies an unmeasured adversarial path. The displayed 0.01 ms txL margin remains conditional on the cost basis and occurrence model, not a hardware guarantee.

For #908, `acmp_mbx.c:111–187`, the stack's owed-send path and `poll_grade.py` support separating send, declined offers and accepted record handling. A kept command blocks later ring takes; redelivery follows an actual send and offers the kept command first. This supplies **two declines per send plus one** in a window. Accepted handling is charged once to its record; nested offer spans are removed from send/base. The published exact-head redeliver-every-poll plant is caught with **316 declines versus 25 for 12 sends**. Native acceptance receipts and source comparison support behavior neutrality of the accounting change.

Base attribution separates the register-read change (**2 cycles**), hot-list placement (**203 cycles**), and approximately 4,400 remaining cycles associated with cache layout after KLJ3 stage growth. Attribution profiles/layouts support that explanation. Placement cuts reduced base but raised other costs; the runtime placement change was reverted (`77a2da0b` / `5013dbc1`). No retained behavioral cut is inferred from rejected experiments; the charge stays 205 us.

THE PACE uses `aecp_mbx.c`'s ready callback before `ctrl_loop.c` takes a record: the head stays in the ring, and subtraction is wrap-safe. `aecp_maps.c` stamps checked edits from the current core clock. Queue-full/zero-storage behavior, response-before-own-notice, FIFO recipients, longer-notice fallback, reset during resumed SRP builds, and ordinary/whole-pass transitions were inspected. Public pace controls and reproduced R4L support the intended 240 ms envelope, subject to F2's cost gap.

The join summaries in `receipts/gates/harness-head-builds.txt` report **52 intervals over 14 runs, 185.668–190.025 ms** (1x1: 188.036–190.025 ms). This includes the deliberate ACMP plant run; it is not 14 independent clean campaigns. The join over-bound control is present and reported caught in public self-test evidence. F1 demonstrates an escaping case. No bench capture was provided; physical calibration was not run.

The image ledger (`receipts/images/every-image-final.txt`, built at `11c586a8`) carries across a final delta confined to tests: fixture 1x1/1if **40.5**, 1x1/2if **41.5**, 8x8/1if **54.0**, 8x8/2if **59.0** RAMB36; platform **42.5, 43.5, 56.0, 60.0**, respectively. The 59.0 fixture uses ruling 6844175391's fallback; platform is <=60.5 and the other points <=56. Exact-head harness plan lines corroborate exercised fixtures. These are image-plan receipts, not fresh synthesis or physical-fit results.

8x8/1if remains **reported, not held**: derived load 0.698 against the separate 0.75 ceiling, with its per-point slice not built. 8x8/2if's **1,550 us build** exceeds the retained 1,300 us slice/1,215 us statement and is explicitly reported as refuted, as authorized for this round. Neither is counted as a passing 1x1 gate.

**Execution and provenance.**

- Independent runs: `run_checks.py` (six concurrent lightweight checks); `probe_maps.py` (three native tests, including unchanged definition/ownership tests); `probe_prior.py` (two campaigns concurrently, at most twelve compile jobs, each baseline then mutant); `audit_model.py`; `verify_evidence.py`. Foreground processes supervised all runs. Builds/mutations stayed in disposable `scratch/` copies. No source fix was made.
- Public receipts: four sweep shards report **65 suites, 2,713,040 checks, zero failures**; local workflow reproduction reports **139 executed steps, zero bad, 226 not run**. The lane summary distinguishes expected nonzero reporting gates. Source evidence is the author's exact-head set. Earlier `11c586a8` test failures are not represented as passing that head; final receipts and test fixes were inspected.
- All **121 author-r7 entries** match the root manifest's `published_sha256`, including two declared redactions (`checks/evidence_integrity.log`). The original author index is not substituted for the publication manifest. Archive commit: `6f321a998afb177721373be74100a0d84b199ab5`; tree: `c6e54150d35c10f3ce8e48ba22a9031a737e9062`. Signature status is `N`: hashes were verified, not a cryptographic signer. No separate detached signature was supplied in the inspected packet.
- Final verification compares index tree with HEAD and independently hashes tracked bytes and executable/symlink modes: all **1,619 main-tree blobs** agree. Required submodules agree in head, index and tracked bytes: gptp `135afd04`, protocol processor `a9e84b66`, lwSRP `08ee86e8`, TSN stack `715589c1`, verilog-axis `48ff7a7e`. The optional uninitialized `external` gitlink is preserved. No source edits require restoration.

**Reviewer-owned completion ledger.** UNCLEAN means an open finding, not an omitted lens. All five were applied, including the imported mailbox read/ACK/write-publication changes and firmware dependencies. No clean coverage is carried over changed dependencies.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2, F3 | #894 rulings; FR_NFR 3.4.1; `tier1_rows.py`, `rows_tiers.py`, `paced_rows.py`, `join_grade.py`; `aecp_maps.c`; flip/load | R838-2, applied; no clean coverage claimed | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |
| RTL | UNCLEAN: F2 | `hdl/milan/mailbox/KL_mbx.sv`, `KL_mbx_dma.sv`, `KL_mbx_rx.sv`: registered reads, held ACK and published head; `ctrl_loop.c`; `aecp.c`, `aecp_mbx.c`, `aecp_maps.c`; `acmp_mbx.c`; `srp_mbx.c` resume/reset/licensing | R838-2, applied; no clean coverage claimed | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |
| Robustness | UNCLEAN: F1, F2 | legal-length conflicting REMOVE; late-join probe; ready/queue/full/zero-storage paths; reset/wrap arithmetic; prior defect probes | R838-2, applied; no clean coverage claimed | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |
| Tests | UNCLEAN: F1, F2 | unchanged map definition; L28/owed-notice mutants; 555/969/25 model controls; native/harness receipts; join horizon and collision probes | R838-2, applied; no clean coverage claimed | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |
| Docs | UNCLEAN: F1, F2, F3 | grader no-missing-row assertion; map single-pass claim; FR_NFR table; AECP/SRP READMEs; MAILBOX_SPLIT; SPLIT_CONTROL_MEMORY; PR body, handoff, manifest/receipts | R838-2, applied; no clean coverage claimed | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |

**Limits and pending manager duties.** No full parent, protocol-processor, gPTP, synthesis or builder bank was run by this reviewer. The scoped pinned simulator was not invoked; no identity claim is made. No hosted/act acceptance is supplied; skipped contexts are not executions. There is **no manager source bank at this exact head**. The manager owns current-dev merge-candidate builder/native validation and publication, hosted/act disposition, merge authorization, and post-merge containment. Source receipts do not substitute for candidate validation against live dev. Physical calibration is NOT RUN; field skips and image plans are not hardware proof. Original full standards were not independently re-obtained during this round; clause interpretation follows frozen public rulings and linked repository authorities, with contradictions recorded above.

F1–F3 require correction and re-review at the resulting head before their lenses become clean. R1/R2 belong on the residue checklist. #908 retains the duty to restore the original 125 ms/20 cs/40 ms budgets; separate shape and bench obligations remain pending public work. This report neither merges nor publishes anything to GitHub.

R838-2 FINISHED
