[R678] NEGATIVE - exact head ee5ece607816a1bfc834bd51734b703a8aab8e46

External independent review, round R678-3, PR #770, issues #632 and #764. Tree: `5505182fe6e444e736f1f10b4388621342b820d5`.

Three findings remain: one substantial execution-evidence gap and two documentation defects. There is also one nonblocking source-comment residue item. No new implementation defect was established in the reviewed delta. All five lenses were applied; Tests and Docs remain UNCLEAN. This is not merge authorization.

## Scope and authority

The review examined the 31 commits after `2ff30f0dc5e89be46f8103272883885e8553f4b8`, with the complete `e26f1816..ee5ece60` diff and history as context. Unchanged code retains its prior result only where the delta leaves its dependencies unchanged. Replacing the render stage changes the dependencies of the shipping render and GM-step harnesses.

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, public issue contracts and decisions, requirements and interface authorities, then implementation and executable evidence. Prior public findings were reconciled after the independent implementation pass. No current peer report, private author material or management source bank was used.

The binding decisions examined were the [round-3 assignment](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306591168), [processor option (b)](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6312625146), [build-now decision](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6309219099), [block-RAM decision](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6309313685), [round-4 assignment](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6316458183), [2 ms sizing decision](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6320453361), and [AAF-exact ruling](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6320617745). The [round-4](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6331675159) and [round-5](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6338815326) execution statements were checked against published receipts.

Authorities applied include Milan v1.2 4.4.2.1, 5.3.7.6, 5.4.2.9, 5.4.2.10.2 and 7.6.1; IEEE 1722-2016 4.3.5, 4.4.4.5, 4.4.4.9, 7.5 and 10.6–10.8; IEEE 1722.1-2021 7.4.77.1; REQUIREMENTS.md, MEDIA_CLOCK_FOLLOWING.md, TIME_SYNC.md and REGISTER_MAP.md. The AAF-exact ruling is applied as written. Its documented non-whole-period limitation is not converted into universal Equation (15) compliance.

## Findings

### R678-3-F1 — MINOR — Docs — retired render behavior remains authoritative text

**Artifacts:** `docs/design/TIME_SYNC.md:108`, `:297`, `:480`, `:482`, `:484`; `docs/design/GM_LOSS_RECOVERY.md:227`, `:228`, `:235`, `:237`, `:277`; `docs/design/MEDIA_CLOCK_FOLLOWING.md:1354`.

**Authority/evidence:** Round 4 implements timestamp presentation and retires the #386 setpoint stage and #387 render re-base. `milan_datapath.sv:6990` instantiates the queue with bind-wipe flushing; MEDIA_CLOCK_FOLLOWING.md:1925 correctly limits settle recentring to LOOP queues. Nevertheless:

- TIME_SYNC says each PHC step has a counted render re-base and that this behavior is retained. Its new listener section ends by saying an owner area decision is pending, the listener keeps the old fill law, and a timestamp law would replace it.
- GM_LOSS_RECOVERY describes the two default render controls as an extra identity re-base and an omitted step re-base, and says disabling re-base fails the check. The actual controls empty the queue on identity/step and fail because PDUs disappear without refusal accounting. The adjacent accept-timed-buffer explanation and simulation table also describe the retired mechanism.
- MEDIA_CLOCK_FOLLOWING's bind measurement still includes one counted render recentre. If retained as historical evidence, that measurement needs an explicit pre-#632 qualification; it is not the present harness result.

**Impact:** The authoritative pages give contradictory behavior and test contracts, including an action the new design intentionally forbids. These are behavioral/verification claims, not pure wording residue.

**Required outcome:** Separate PHC `tu`/holdover from queue presentation and refusal/slip accounting. Replace the pending-area/fill-law passage with the implemented timestamp law and remaining bench obligation. Describe the actual queue-flush controls. Mark the old bind measurement as historical or correct its render claim without inventing a new measurement.

**Verification:** Cross-read the corrected passages against the queue, root flush connection, `gmstep_mutants.py:CONTROLS`, the GM-step receipt and revised bind grade. No current contract should require the retired render recentre.

### R678-3-F2 — MINOR — Docs — stale resource figures and campaign counts

**Artifacts:** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1939`, `:1940`, `:1950`; `docs/testing/TESTING.md:271`.

**Authority/evidence:** The storage paragraph states 594 LUT / 231 FF at 1x1 and 945 / 395 at 8x8. Published `round4/ooc_bb9a9200/q1x1.rpt` and `q8x8.rpt` report **553 / 228** and **890 / 387**, with 2 RAMB18 and 6 RAMB36 and zero LUTRAM. Queue RTL is unchanged from that measurement to this head. The proof table says 18 queue defects; the exact-head receipt catches **22**. TESTING calls follow_ring's inventory fifteen controls; its changed inventory and published `fr_mutants.log` contain **16**.

**Impact:** Resource and proof summaries disagree with reproducible evidence. Figures/test counts are outside the owner's RESIDUE exception.

**Required outcome:** Correct both LUT/FF pairs and both inventory counts, with measurement provenance. Keep OOC counts distinct from routed image deltas.

**Verification:** Compare against the OOC reports, `round5/sweep_ee5ece60/shard1/render_queue.log`, and `round4/follow_ring_controls_bb9a9200/fr_mutants.log`.

### R678-3-F3 — MAJOR — Tests, Docs — required full campaigns lack post-replacement execution evidence

**Artifacts:** `docs/testing/TESTING.md:272`, `:273`, `:278`; `tb/verilator/milan_dp_render/Makefile:234`, `:248`; `tdm8_render_mutants.py:MUTATIONS` in that directory; `tb/verilator/milan_dp_gm_steps/Makefile:34` and `gmstep_mutants.py:CONTROLS`; PR #770 “How to validate” and checked “Required local verification bar passes”; receipt manifest and `campaign-audit.json`.

**Authority/evidence:** TESTING requires authors/reviewers changing the render path or harness to run the full shipping render inventory and 18 boot-phase pull-ins plus the standing phase after serial/CRF/LAW history. For the changed queue, render flush and GM-step harness, it requires the complete GM-step inventory on the whole leg, including the small-step phase. Those dependencies and assertions changed here.

| Campaign | Required inventory | Published post-replacement execution found |
|---|---|---|
| Shipping TDM8 gateware/shape mutations | 20, in addition to leg-side controls | 4 mutations, 3 leg-side controls and 3 clean modes in `round4/milan_dp_render_632_bb9a9200/tdm8_subset.log` |
| Shipping render pull-in | 18 boot phases plus standing phase after full history | Only `+1562`, through the subset's `--pullin`; no complete explicit-campaign receipt |
| GM-step controls | 20, with specified full-leg/small-step coverage | 5 default controls and 2 queue-counter controls; receipts explicitly use `--no-small-steps` |

`gmstep_full.log` is a clean leg run, not the full mutation campaign. The exact-head default sweep repeats its default subsets, not these explicit full targets. `campaign_audit.py` reads the current inventories and searches published round-4/5 logs for named successful kills: 4/20, 7/20, and only one shipping pull-in phase. No other complete receipt appears in the supplied manifest. This finding concerns published evidence; it does not assert that an unreported run never occurred.

**Impact:** The redesigned integration and regraded assertions have not been shown to retain all required discrimination and pull-in coverage. Results against the replaced stage cannot prove that the changed harnesses reject each defect. The checked local-verification claim is unsupported. The manager's future current-dev candidate bank is a separate obligation and supplies no source-head result today.

**Required outcome:** Publish complete applicable campaigns on this head or a descendant, including clean controls, every required named kill, all pull-in phases/history, commands, head and exit status. Correct the local-bar claim until that evidence exists. Do not count compile failures, interruptions or default subsets as complete campaigns.

**Verification:** Reconcile receipts one-for-one with the 20 render and 20 GM-step entries and explicit pull-in target. Check required small-step coverage. Re-review evidence and resulting source changes. No manager source bank is requested or presumed.

### R678-3-R1 — RESIDUE — Docs — three new comments name review rounds

**Artifacts and exact fixes:**

- `tb/verilator/media_phase/phase_mutants.py:206`: replace `(round 2's binding, every row through the rounder) instead of as set` with `(every row through the rounder) instead of as set`.
- `tb/verilator/media_phase/sim_ofs.cpp:35`: remove ` (round 2's binding)`.
- `tb/verilator/milan_dp/gsi_mutants.py:125`: replace `round 4's binding: every output's row through one rounder, read back so` with `#632: every output's row through one rounder, read back so`.

**Authority/evidence:** The owner's comment rule permits issue/requirement IDs and behavior/reason, but excludes review-round history. These are new instances in the delta.

**Impact:** Wording only; no executable statement, measurement, clause claim or privacy rule changes. This leaves no lens unclean.

**Required outcome/verification:** Apply the three textual edits and inspect added source comments for review/lane labels. Existing residue owned by #746 is not refiled here.

## Applied-lens evidence

**Conformance.** Checked raw AAF connection `milan_datapath.sv:1447`, CRF-only `g_pres_crf` at `:3454`, and GET_STREAM_INFO selection at `:5005`/`:5258`. `KL_mtt_round.sv:129`/`:182` and runtime conversion keep 33 bits; `KL_crf_tx.sv:303` and its timestamp sum retain them in 64 bits. `sim_ofs.cpp` independently computes rational ceilings and compares full-width timestamps at reset/runtime boundaries. The exact-head clean case passes 93 checks. AAF stamps/readback are as set; CRF alone rounds. CRF 0xFFFFFFFF applies 4,294,979,167 ns, not 11,871 ns.

For presentation, examined `KL_render_queue.sv`, depacketizer header timing, `KL_media_if_latency_pkg.sv:163`/`:171`, root wiring `:6918`–`:7030`, and `media_phase/render_wrap.sv`/`sim_render.cpp`. One domain event indexes PDUs; each interface reads with its derived lead. The K=2/K=3 test decodes sample identities at slot MSBs and checks missing/extra samples and phase. Its clean case and all five presentation-rule/lead controls pass independently. The +/-5% claim applies to timestamps on the domain grid; arbitrary-phase/hold cases use the documented nearest-frame bound.

The documented 1x1 interval is 31,119–2,656,119 ns ahead at arrival; 8x8 is 25,942–2,650,942 ns, from K, event latency and 128 rows (MEDIA_CLOCK_FOLLOWING.md:1850). Offset-minus-transit, first-event arrival, early refusal and the shipping 2,126,000 ns STREAM_INPUT declaration are distinguished. The 7.4.77.1 controller/buffering statement does not promise that this finite listener accepts every talker offset. Larger builder-declared buffers do not enlarge the queue; that limit is explicit.

**RTL.** Examined reset, indexed carry writes, parameter bounds, divider/header lead, synchronous bank read/write behavior, read/scrub scheduling, stream-qualified flush and root source/CSR wiring. Queue banks at `KL_render_queue.sv:350` infer block RAM with no device primitive. `out_lead_ok` bounds the path and rejects an adoption-straddling lead. The existing TDM crossing remains the interface boundary; the queue uses axis clock. CRF-only elaboration removes AAF rounder rows, including no-CRF shapes. Published changed-top synthesis and OOC receipts support portability; no independent full synthesis bank was run.

**Robustness.** Checked reset/bind flushing, silence before presentation, invalid `tv`, per-PDU late/early accounting, gaps/overlaps, odd padding, wrap, stream isolation, clock hold and long PDUs. `KL_render_queue.sv:464` keeps later too-early events refused before frame-number wrap can reuse live rows. Published 40-event/300-event tests and both long-PDU controls discriminate that fix. The independent queue model passes 36 checks, including long PDUs, flush, lap, wrap, rules, two interfaces and counters. Queued rows persist over PHC steps/clock hold; subsequent placement accounts for refusals or slips. Listener-only PHC stepping remains documented analysis, not a separately executed integration case.

**Tests.** Examined independent arithmetic/model/pin oracles and mutation predicates. `phase_mutants.py:345` requires successful build, rc=1, `RESULT: FAIL` and the designated failed assertion. The carry receipt prints the first failure, but its kill requires the full-64-bit Equation (14) assertion. `sim_det.cpp:254` settles near zero, holds, then supplies balanced +/-Ps/2 samples; retaining the old reference is killed. Checked replacement #386 grades in render_queue, milan_dp/aclk, follow_ring, milan_dp_gm_steps, milan_dp_render and milan_dp_mclk, including separation of #645 LOOP recentres from queue presentation. F3 prevents clean coverage despite passing checks below.

**Docs.** Compared decisions and PR claims with design pages, CSR fields, compliance limitations, source lists, test policy and raw resources/campaigns. The AAF/CRF split and finite listener range are documented. F1/F2 retain contradictory contracts/figures; F3 retains an unsupported completion claim. Passing documentation automation does not resolve semantic defects.

## Executable evidence and resource accounting

Evidence root: [review-evidence/632-r1 at 7aa121b32be32be9d0ea45840bc9dc19e78e02f7](https://github.com/kebag-logic/milan-fpga/tree/7aa121b32be32be9d0ea45840bc9dc19e78e02f7/review-evidence/632-r1).

`verify_evidence.py` checked all **1,640 author-r5 receipt blob hashes** against the publication manifest, with zero mismatches, without reading the reviews directory. This establishes packet consistency, not signer authentication: the publication commit reports signature status `N`, and no detached signature was found in the supplied packet. No cryptographic authentication claim is made.

| Evidence | Result and scope |
|---|---|
| Exact-head source sweep | 63/64 suites. Shard 0: 14/15, 47,447 checks, three notify failures. Shards 1–3: 16/16, 17/17, 16/16; 331,516 / 262,062 / 1,540,265 checks, zero failures |
| Notify at source pin | 459 checks, three failures in CRF-output steps 3/4; AAF steps pass. Explicitly recorded processor dependency |
| Notify with E_SINFO splice | 459/0 and all 11 GSI controls caught in modified-submodule scratch evidence. Diagnostic isolation, not a source-pin or integrated-#771 pass |
| Remaining milan_dp legs | Pool stops at notify; separate `d5b516f6` receipts cover eleven other legs and four render controls without failures |
| Full media_phase campaign | All 40 distinct named kills at exact head, reconciled in `phase-inventory.json`. Interrupted chunk2 is not a successful campaign: its two unfinished controls have successful replacement receipts in chunk2b |
| Queue campaign | Exact-head sweep: two clean shapes and all 22 controls caught, including both long-PDU defects |
| Other controls | follow_ring 16/16, render CSR controls, and the two nxn stamp defects caught; shipping render/GM-step subsets remain bounded as F3 states |
| Independent focused execution | Three clean phase cases plus seven named kills: 10/10. Queue model: 36/36. Both tasks completed rc=0 concurrently in disposable trees |
| Source gates | Published changed-top synthesis passes; lint 89 against ratchet 89; exact-head documentation workflow 49 gates passes. These are source evidence, not a manager source bank |

The independently killed controls are `hold_keeps_ref`, `crf_carry_dropped`, `render_b_lead_dropped`, `render_read_untimed`, `render_frame_off_by_one`, `render_late_rule_removed`, and `render_early_rule_removed`. Compiler identity was verified before use; version/hash are recorded in `compiler-identity.txt`. `run_focused.py` accepts repository/compiler paths, archives the exact head, uses four build jobs per build and `make -j16` for the queue, and ran at most two phase builds plus one queue build concurrently. No job remains running.

Resource measurements are distinct:

- Queue OOC at `bb9a9200`, unchanged through this head: 1x1 **2 RAMB18, 553 LUT, 228 FF**; 8x8 **6 RAMB36, 890 LUT, 387 FF**; no LUTRAM.
- Route-1x1 at last-RTL-change `5b502a05`, under the repository route resource recipe: **49,922 LUT (+309), 52,696 FF (+343), 15,793 slices (+68), 74 RAMB36 (+0), 27 RAMB18 (+2), 13 DSP (-1)**. Route complete; **WNS +0.108 ns, WHS +0.015 ns**. Later changes affect tests/docs, as checked in `lineage.txt`.
- The resource gate actually exits **1, MATERIAL REGRESSION**, solely for the owner-authorized RAMB18 +2 against the old record of 25. It is not relabeled PASS. The manager must re-record the accepted measurement at the merge onto the fourth pin adoption.

## Prior public findings

| Finding | Disposition at this head |
|---|---|
| R678-2-F1 | Resolved: full carry reaches 64-bit CRF stamps; reset/runtime/readback boundaries and the named truncation control discriminate it; independently checked |
| R677-2-F2 | Resolved: det:afterhold checks reference restart; hold_keeps_ref independently killed |
| R677-2-F3 | Original cause resolved: PR history corrects 404-LUT/8-slice headroom and campaign count, and separates current figures. New stale design-page figures are F2 here |
| R677-2-F1 | Retained as explicit integration dependency, not called fixed at this pin. Processor #199 implements option (b), consumed by #771. Expected source failures are isolated by splice evidence; integrated proof remains mandatory |
| R678-1-F1 | Queue, derived leads and pin grades implement the superseding build-now decision. F3 records remaining execution coverage; bench proof stays pending |
| R678-1-F2 | Superseded by AAF-exact ruling: raw AAF stamping/readback is required, CRF alone rounds. Full-width CRF is checked; documented non-whole-period limitation retained without reopening the ruling |
| R678-1-F3 | Circular-aggregation repair retained; unchanged detector implementation. Exact-head boundary/tracking/re-fold/settled controls pass; hold restart additionally closed above |
| R678-1-F4 | Snapshot-edge hold repair retained; exact-head snapshot/control receipts preserve before/on/after-edge distinction; implementation unchanged |
| R678-1-R1 | Public roles identify independent internal/external reviewers |
| R677-1-F1 | Blend constants/frame-assembly repair retained; current blend is 24 checks across six reset phases and both defects remain killed |
| R677-1-F2 | PHC-step hold case and step_hold_removed remain covered at exact head; implementation unchanged |
| R677-1-F3 | Settled timing/range predicates and their planted controls remain covered |
| R677-1-F4 | Old nine-case budget basis corrected; current suite timing is separate from mutation timing. No renewed budget defect established |
| R677-1-F5 | Assigned stale CRF-divider comments remain corrected |
| R678-2-R1 / R677-2-R1 | Old review-ID comments removed; three new round-history instances listed as R678-3-R1 |
| R677-2-R2 | Offset comments now distinguish AAF as set and CRF as applied |
| R678-2-R2 / R677-2-R3–R5 | Earlier scope deferral superseded by build-now. PR/design scope follows it; contradictory TIME_SYNC text is retained as F1, not silently cleared |
| R677-2-S1 | Raw-versus-rounded AAF monitor suggestion overtaken by AAF-exact ruling; no new mismatch established |
| R677-2-S2 | Truncation cause fixed by carry; additional factory-row policy guard remains optional |
| R677-2-S3 | Closing-cycle fold-reference behavior unchanged/documented; optional suggestion retained |
| R677-2-S4 / R677-1-F6 | Separately literal data-delay coupling remains optional maintainability work; no correctness defect found |

## Reviewer-owned ledger

CLEAN entries cover the delta and applicable prior causes within the public scope, subject to the explicit processor integration and hardware limits. They do not make this NEGATIVE round merge approval.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Clauses/rulings; root AAF/GSI/CRF connections; KL_mtt_round; KL_crf_tx; queue; sim_ofs/sim_render; notify isolation | R678-3 | ee5ece607816a1bfc834bd51734b703a8aab8e46 |
| RTL | CLEAN | Queue banks/scheduling/flush; depacketizer lead; latency package/root wiring; carry/reset paths; OOC/synthesis receipts | R678-3 | ee5ece607816a1bfc834bd51734b703a8aab8e46 |
| Robustness | CLEAN | Queue model/22 controls; long-PDU walk/refusal hold; det:afterhold; hold/step/source-switch grades and receipts | R678-3 | ee5ece607816a1bfc834bd51734b703a8aab8e46 |
| Tests | UNCLEAN — F3 | Campaign inventories/targets; sweep/subset receipts; pin/model oracles; independent seven-control and queue runs | R678-3, applied but not clean | ee5ece607816a1bfc834bd51734b703a8aab8e46 |
| Docs | UNCLEAN — F1, F2, F3 | TIME_SYNC; GM_LOSS_RECOVERY; MEDIA_CLOCK_FOLLOWING; TESTING; CSR map; issue decisions; PR claims; resource/campaign receipts | R678-3, applied but not clean | ee5ece607816a1bfc834bd51734b703a8aab8e46 |

## Limits and pending manager duties

- Resolve F1–F3 and obtain independent re-review. Carry R1 to the residue checklist. An open MINOR is not clean coverage under this contract.
- This source review uses published author receipts and bounded independent probes. No manager source bank exists or is inferred at this head. No full parent/processor/gPTP/synthesis/builder bank, hosted acceptance, local container replication, route or hardware run was performed by this reviewer.
- The manager owns hosted/local-replica acceptance and the final current-dev candidate. Source base `e26f1816` is not that candidate. Stated live dev is `d77a8afdbc960d70d1ceeee9af1163624f102b16`: compose with the fourth pin adoption, execute required builder/native banks on the actual result, and link receipts when published. Changed pins/tree invalidate affected evidence.
- Require the adopted processor to pass complete notify/GSI integration. A microcode splice isolates three failures; it does not prove the merged dependency configuration.
- Re-record accepted RAMB18 use and validate route/resource/timing on the merge candidate. Source authorization does not establish candidate results.
- Physical calibration is NOT RUN. Field skips and modeled pins are not hardware proof. #632/#764 bench items remain open after merge, as publicly scoped; neither issue is closed by this review.
- Complete the review bar, ensure no review is in flight, obtain explicit maintainer merge authorization, and perform post-merge containment. No GitHub write or merge was made.

Probes used disposable copies under this packet's `scratch/`. `checkout-integrity.json` verifies parent head/tree, all 1,439 parent tracked blob bytes/modes and index, and all 1,072 tracked blobs/indexes in five initialized submodules. Required gitlinks match: protocol `2cbed0a987c1e68402658d69459ab7e5aa571adc`, gPTP `e4869fd0c42889b2ac806587cc5c78afb1c33461`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, tsn-c-stack `70936b77dc41981e192438388cd0aced69954f18`. No tracked bytes, modes or index entries changed.

Publish only REPORT.md and files listed in MANIFEST.sha256. The manifest excludes `scratch/`; scripts, integrity/audit results and selected unmodified public receipts are included. Full original receipt hashes/paths are in `evidence-hashes.json`.

R678-3 FINISHED
