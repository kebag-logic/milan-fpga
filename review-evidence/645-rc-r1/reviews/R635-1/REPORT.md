[R635] NEGATIVE - exact head 2639eecf3f94aa1a8be5c922058a05f0a48b1933

Round R635-1, external independent review of issue #645 / PR #742.
Tree: `c0bece4c6943bee323b9a72c4e677abdda840004`.
Comparison base: `f62602531d415d6c1cae1374a3cc2938faf54049`.

All five lenses were applied. One MINOR remains: the claimed measured lower bound on B17's primed margin is not derived by the cited evidence. It affects the test's classification and the design's measurement claims. No functional RTL defect was established. This is a source-head review, not merge authorization or bench acceptance.

Public contract and evidence

The [design-round decision](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187595500) freezes this PR's scope: reproduce the bind slip, arm the existing settle recentre at the first PDU at INTERNAL, preserve following and firing rules, retain existing checks, measure area, and document the change. The bench repeat belongs to the manager after merge. The original issue's bench acceptance remains open.

I read the repository operating contract, contribution rules and documentation index; the issue and public scope decisions; requirements and media-clock, counter, queue and area authorities; both source commits and the complete twelve-file diff; then the executable evidence. The source commits are `4e6b53981` and `2639eecf3`. No private author material or other reviewer's report was read. No source edits, builds, simulations, bank runs, hardware actions or GitHub writes were performed. The evidence itself supplied the falsifying example, so no simulation rerun was necessary.

The [author's source-head statement](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6192046983) is checked against the immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/a86dc902d332e27ce093f5f56ccdaa5e46f9ce90/review-evidence/645-rc-r1). B17 inputs come from `review-evidence/645-b17-r1/author/summary/c01.json` through `c10.json` at `bdb96b6685751a424fbbdc952726f33efd17282a`. Packet paths below are relative to `review-evidence/645-rc-r1/author/` unless stated otherwise. `audit-evidence.log` records independent calculations from those immutable objects and verifies the published hashes; the portable reader is `audit_evidence.py`.

Reproduction and checks

The base datapath supplies the counterfactual before judging the fix. Across its 32 published runs and 320 binds, no run passes; no bind arm, settle action or render recentre occurs. Every one of the 169 binds classified inside the selected window slips exactly one frame at the first burst. The base has 414 post-action-boundary slips and six earlier slips. The author reports reproducing before implementing; the public receipts independently establish the base/head behavior comparison, rather than a timestamped development chronology.

At the candidate, all 32 runs pass. All 320 binds have one arm, one settle action and one render recentre. There are zero post-action slips, and all 169 selected-window binds have zero counter movement. Measured firing is 2047.02 to 2048.02 tick periods after the arm, consistent with the tick-count rule and its phase. Minimum empty-side margin is 3.479 ticks; minimum full-side margin is 4.884 ticks. Artifacts: `campaign/base/bind_j*.log`, corresponding `.rc` files, and the corresponding `campaign/fix/` files. These figures are independently recalculated, not accepted from the summary table.

The ten C++ parameter rows exactly match the B17 summary's first-PDU delays, first-burst offsets and peaks, and largest later peaks. Fitting the recorded first-burst tails gives mean decay 1.538083 us/PDU, rounded to 1.538. The summary's p99.9 range is 4.448 to 6.139 us; uniform 0 to 5 us is a selected simulation envelope supported by that scale, not a complete replay of recorded arrivals. The 10-us priming-bound derivation fails as detailed below.

`suites/fr_mutants.log` and `.rc` record 15/15 controls caught. I checked the implementation of the mutation reader: each control must build, exit nonzero, and print each specifically required failed check. NO-BIND-ARM requires the no-counter-change failure for cycles 5, 4 and 9; BIND-RISE requires it for cycles 4 and 9; FOLLOWING-ARM requires the no-bind-arm-under-following failure. These controls distinguish the trigger, its timing, and the source gate. `controls/sc_plants/*.run.log` separately exercises removal of wait, stream, last-beat, fall and following qualifications.

The existing tests' checks were not weakened in the diff. The altered shared stimulus preserves the previous arrival expression for the non-bind legs. Published `suites/fr_default.log` retains 48 B8 checks, 18 pull-in checks, 30 bind checks, fine-pull 10/10 and controller passes at all four rates. `suites/render.log` retains 266 plus 71 checks, the LAW phases, T30/T31 and 5/5 controls; `render_pullin.log` retains 19 legs and 838 checks with zero loopback slips; `render_lawb.log` records 81/81. The tally records 52,122 checks across eleven default-sweep suites, including capture 847, datapath 11,956, media clock 168, clock steps 196, coherence 21,194, shadow 2,184, CSR 1,815, mailbox 2,123 and parser 11,201, all with zero in-suite failures. This is the author's scoped source evidence, not a claim of a manager full source bank.

Finding R635-1-F1

- Severity: **MINOR**.
- All attributable lenses: **Conformance, Tests, Docs**.
- Artifacts: `docs/design/MEDIA_CLOCK_FOLLOWING.md:1287` and `:1342`; `tb/verilator/follow_ring/sim_main.cpp:171`, `:1307` and `:1357`; the PR body's reproduction and arming-window claims. Input authority: B17 `author/tools/ana_b17.py:51` and `:333`, plus the ten summary JSON files.
- Authority/evidence: design-round item 1 requires parameters derived from B17. The design says B17 bounds the primed margin above 10 us because nothing that late slipped it. However, the B17 reader stores only arrivals **greater than** 10 us in `late_pdus`, and there are none before the first burst. Absence of a tested arrival above that reporting threshold cannot establish tolerance of 10 us. The alternative cycle-5 inference printed nearby gives `30.260 - 20.833333 = 9.426667 us`, which also does not establish greater than 10 us. The author's own `campaign/base/bind_j0_p09.log`, cycle 1, demonstrates the logical counterexample: 9.120 to 9.280 us margin, exactly one slipped frame at the first burst and no later slip. This does not measure the actual bench margin; it shows why the observed slip pattern does not imply the claimed lower bound.
- Impact: the selected 10 to 24.565 us interval is presented as an established bench bound and controls `in_window`, the 169/151 classification, and whether the whole-cycle no-slip check is applied in `--any-phase`. The simulation counts are reproducible, but the evidence does not justify calling the excluded phases outside what B17 could have primed. This is not RESIDUE: it concerns a measurement claim and executable acceptance classification.
- Required outcome: derive any claimed bench bound from observations that establish it, or explicitly identify the interval as a selected modelling window with its uncertainty. Make the source comments, test labels/classification rationale, design and PR claims agree. Reassess any acceptance exclusion that relies on a measured greater-than-10-us margin. Retain the reported early slips and the complete sweep; no RTL change is prescribed by this finding.
- Verification: rerun the parameter/evidence audit against the corrected derivation, check every affected measurement and test-classification statement, and use the existing sweep receipts if test semantics are unchanged. If classification or stimulus changes, regenerate the affected campaign and counts. The absence of >10-us pre-burst entries must not itself be used as a lower-bound proof.

RTL and robustness results

[R635] PASS RTL - `hdl/milan/milan_datapath.sv:6616`, `:6409`, `:1311`, `:6641`, `:6710` - the production change is confined to the settle-recentre block. It adds a reset-cleared wait bit per loopback stream, matches accepted last beats by stream, clears the wait on the beat or unbind, and gates the new arm with `!follow_sel_r`. The tap already includes `tvalid && tready`; no extra backpressure, CDC, port, register field or parameter is introduced. The source-change, re-engagement, excursion, dwell, recovery and ceiling logic is unchanged. The existing pulse fanout reaches render and every loopback stream. Queue priming agrees with `KL_chan_map_capture.sv:958`; render action counting remains `KL_render_setpoint.sv:665`, and the recentre's loopback holds/drops remain outside SLIP_LB.

[R635] PASS Robustness - `tb/verilator/follow_ring/settle_control.py:112`, `follow_ring_wrap.sv:162`, `hdl/ieee1722/avtp/KL_stream_table.sv:142`, `hdl/milan/milan_datapath.sv:6635`, `suites/fr_default.log`, `controls/sc_plants/`, and `campaign/fix/` - applied the reset, repeated-PDU, missing-bind, wrong-stream, incomplete-PDU, unbind-before-PDU, recovery, following and feature-disabled cases. Existing controller checks retain interrupted dwell, reset, source priority, disengaged settling and the independent ceiling at four rates. Production accepted-beat qualification prevents stalled or incomplete payloads from arming. The no-loopback configuration folds the tap valid low. The controller test uses one real stream and a wrong-stream input; the multi-stream fanout is additionally established by inspection, not claimed as a new multi-stream runtime campaign. F1 remains an evidence/classification defect, not an established failure of the controller's robustness contract.

Area and runtime

`area/base_n1.vivado.util.txt` and `head_n1.vivado.util.txt` report 73/93 to 76/94 LUT/FF: +3/+1. `head_off.vivado.util.txt` reports 73/93, equal to the base, with the tap disabled as in shipping 8x8 (`configs/endstation_ax7101_8x8.yaml:248`). The enabled eight-stream measurement is separately 85/101, or +12/+8, and must not be confused with shipping 8x8's zero delta. I inspected the extracted block and the 50-MHz, target-part synthesis recipe. These are block estimates, not a fresh full-image placement or timing guarantee. NFR-RES-01 remains the 38,040-LUT whole-image target; +3 LUT is about 0.0245% of the recorded 12,227-LUT excess and 0.0471% of the plan's 6,373-LUT margin. This PR does not establish whole-image compliance with that target.

`wallclock/result.txt` gives 857.648 s for five legs and 800.859 s for four, both rc 0. The cold-build script uses one four-CPU set and clears build directories between runs. The increase is 7.091011%; applying that ratio to the historical 1114.2-s hosted window gives 1193.208 s, 66.792 s below 1260 s. The docs correctly call this a projection. It is not exact-head hosted acceptance.

Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | Design-round items 1-5; REQUIREMENTS section 8; MEDIA_CLOCK_FOLLOWING settle table and bind section; B17 summaries; both sweep populations; NFR-RES-01 | R635-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |
| RTL | CLEAN | milan_datapath:1196, 1311, 6409, 6616-6713; stream-table edge owner; capture PRIME/FLUSH/recentre; render action counter; area wrappers and receipts | R635-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |
| Robustness | CLEAN | settle_control driver and controller; sc_plants receipts; accepted-beat wiring; base/fix sweep logs; following leg; shipping lane-disable configuration | R635-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |
| Tests | UNCLEAN, F1 | sim_main B17 constants and run_bind; dp_glue; wrapper; mutants and sweep drivers; default/render/switch receipts; immutable regression diff | R635-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |
| Docs | UNCLEAN, F1 | All four changed docs; test-reader disposition; PR body; issue decisions; B17 derivation; area and runtime claims | R635-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |

Prior findings and review independence

After the independent diff pass, PR #742's public review and inline-comment endpoints contained no prior reviews or findings. Its two issue comments were review-start notices. There was therefore no earlier finding on this PR to resolve or retain at the observed snapshot. Another review remains independent; no report from it was consulted. B17's public scope amendments were read as source decisions, not as a substitute for reviewing this implementation.

Real limits and pending manager duties

- The six early slips are visible in the raw fixed sweep, all outside the selected modelling window, at phases 0.8125 and 0.8750 with jitter. Their delays after the first PDU are 0.129 to 2.127 ms. They precede the approximately 42.7-ms action. The code and docs retain them as limits rather than declaring them acceptable hardware behavior; F1 concerns the claimed bench-bound justification.
- Following binds intentionally arm nothing. The default leg retains cycle 5's one-frame slip under CRF following. A bind also recentres other running streams when a multi-stream shape enables the loopback lane; an already-centred loopback ring takes no step. Both effects are stated in the design and PR.
- The author reports the physical-path simulation at 197 checks with two declared -5 recentres and unchanged SLIP_LB. Its log expressly excludes licensed ACMP/SRP streaming, physical TDM render, calibration and physical compliance. Physical calibration was NOT RUN. The builder's historical gate-11 report arm was also NOT RUN. Neither skip is hardware proof.
- Author gates include lint 90 within 90, parser zero findings, portability 58/58 and builder execution with its stated historical skip. The failed `milan_dp.simjobs4-refused` attempt is retained; the subsequent `milan_dp` receipt is rc 0. These are author source-head receipts. **No manager source bank ran at this head, and none is inferred.**
- The read-only hosted snapshot has completed successful jobs, pending jobs and a skipped physical job. The exhaustive aggregates and measured follow_ring window were not complete in that snapshot. `hosted-snapshot.json` preserves names, states and links. The manager owns local-replica and hosted acceptance; no skipped context is counted as executed evidence here.
- The manager must build and validate the final current-dev merge candidate, including builder and native banks, and publish its receipts. Source base `f62602531d415d6c1cae1374a3cc2938faf54049` is distinct from the supplied live-dev tip `65617779018f41d7e55d1b1ac189ef882bff6367`; neither author source validation nor this review proves that future merged tree.
- F1 requires correction and re-review. The manager must also obtain the complete independent review bar, settle all in-flight reviews, complete hosted acceptance and candidate validation, obtain merge authorization, and perform post-merge containment. B17's ten-bind repeat on the resulting image remains the manager's post-merge acceptance work; issue #645 is not closed by this report.

Checkout integrity

`checkout-integrity.log` verifies the exact head/tree, every tracked blob's raw bytes and executable/symlink mode, the complete stage-zero index, and registered required submodules against their pinned trees. All pass: 1,325 superproject blobs and 1,046 blobs across the five initialized dependencies. No restoration was needed because no candidate byte was modified. The optional external gitlink remains recorded and uninitialized. The scoped simulator identity was checked but not used to rerun simulations. Only files named in `MANIFEST.sha256` and this report are intended for publication; `scratch/` is excluded.

R635-1 FINISHED
