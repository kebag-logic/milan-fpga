[R700] NEGATIVE - exact head 21faa48242e021177a1dc702f28e51347c6a7a57

Independent review R700-1, PR #786, issue #396 part A. Tree `dff7043fb74a2b30bca12bc48fa9e7d6fafd3296`; base `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. All five lenses were applied. This independent verdict and ledger were written before reading another reviewer's report or prior PR findings.

The decided 24-hour defaults and 100/50/50 cycle mix are present. The three negative controls fail their named desk assertions. The new graders nevertheless have false passes and incorrect measurements.

### Findings

**F1 | MAJOR | Conformance, Robustness, Tests, Docs | tb/tools/torture_campaign.py:3765; docs/testing/TESTING.md:1302 | The repeating audio payload cannot establish zero glitches.**

Authority/evidence: issue #396's signal-design and part-A decisions require every discontinuity classified exactly; REQ-VER-06 requires zero DUT-attributed glitches. In `probes.json`, `drop-4096` injects a 4096-sample drop between six correctly detected planted arms. The grader returns PASS with no DUT event. `drop-3000` reports a 1096-sample repeat. The payload repeats every 4096 samples. TESTING acknowledges this, but asserts that sequence/interruption counters cover it. Packet continuity does not prove sample-content continuity on every digital path; a content skip with intact packet sequencing/timing need not increment either counter. No independent disambiguation result is required by this oracle before PASS.

Impact: corrupted audio can earn PASS; the direction/count can also be wrong. Disclosure does not amend frozen acceptance.

Required outcome: supply independent sequence/time evidence or a signal that detects and disambiguates these slips; ambiguous evidence cannot pass the release assertion. Correct the claimed counter fallback. Narrowing acceptance instead requires a public decision.

Verification: preserve the 4096/3000 probes; add larger multiples and both directions; test the complete release assertion with unchanged AVTP error counters.

**F2 | MAJOR | Conformance, Robustness, Tests, Docs | tb/tools/torture_campaign.py:3817; docs/testing/TESTING.md:1300 | Tag corruption is falsely classified as a channel swap.**

Authority/evidence: the exact-classification contract distinguishes corruption masks and swaps. `single-tag-bit-flip` XORs `0x00200000` into channel 0 at sample 8000; channel 2 remains unchanged. The grader emits a swap with partner 2 and no mask. It checks only whether a word matches another channel's expected word, without requiring reciprocal exchange. `copy-channel` also becomes a swap. `two-low-bit-flips` shows adjacent corruptions reported as a drop and repeat.

Impact: event classification/localization is wrong despite an overall FAIL in these examples. A correctly logged tag-bit planted arm can be missed by class.

Required outcome: distinguish an actual exchange from isolated corruption/duplication; preserve the exact mask for the single-bit case. Report genuinely ambiguous bursts as uncertain rather than inventing exact classes, and reconcile that limitation with the accepted contract.

Verification: test flips in every container bit, reciprocal swaps, unilateral copies and consecutive corruptions against independent expected events.

**F3 | MAJOR | Conformance, Robustness, Tests | tb/tools/torture_campaign.py:3569 | Pending default values defeat the commit-cut vacuity guard.**

Authority/evidence: REQ-VER-06 requires non-vacuous restore proof for every item. The guard checks only the old snapshot. `commit-target-defaults-persistence-disabled` supplies nine non-default old values, an all-default pending snapshot and an all-default readback. The oracle returns PASS as the new snapshot.

Impact: a commit-cut cycle can pass without restoring any persistence. The idle negative control does not prove this phase.

Required outcome: ensure each admissible snapshot gives non-vacuous evidence for every item, or refuse a cycle unable to distinguish default fallback from restore.

Verification: test all-default and single-item-default pending snapshots with disabled/partial restore, valid distinct non-default old/new snapshots and mixed-state refusal.

**F4 | MAJOR | Conformance, Robustness, Tests, Docs | tb/tools/torture_campaign.py:3538; docs/testing/TESTING.md:1115 | Planted exceptions expand to entire counter-read intervals.**

Authority/evidence: the owner requires zero MEDIA_UNLOCKED outside a planted event. `unlock-outside-planted-window` has reads at 0/60 seconds, a planted window at 10-20 seconds, and an actual unlock at 45 seconds producing the sampled increment. The oracle returns PASS because the window intersects the read interval; it has no evidence locating the increment inside that window. Tests explicitly accept even windows touching read endpoints.

Impact: an unrelated unlock tens of seconds outside the planted event is excused. TESTING changes the required exception into interval overlap.

Required outcome: confine each excused increment to its event window using observations with a justified error bound; otherwise refuse the ambiguous exception. Preserve the stricter owner criterion.

Verification: bracket the event with observations or correlate timestamped transitions. A before/after unlock in the same periodic interval must not pass; retain a genuine in-window positive control.

**F5 | MAJOR | Conformance, Robustness, Tests, Docs | tb/tools/torture_campaign.py:3722; docs/testing/TESTING.md:1307 | Capture losses do not advance event clocks.**

Authority/evidence: the signal-design decision requires wall/gPTP timestamps and surrounding state walks. `_emit` calculates start plus stored-frame index/rate. `timestamps-after-capture-loss` places a corruption at stored index 8000 after a logged 409600-frame capture loss. Recorded wall time is 100.1666667 seconds; actual acquisition time is 108.7 seconds. The 8.5333333-second error also affects gPTP time and exceeds the default five-second context. Losses affect attribution only. A single starting gPTP time also cannot represent a later discontinuity.

Impact: retained event records identify the wrong state/counter window, defeating required correlation.

Required outcome: map indices to acquisition timestamps accounting for capture gaps and clock discontinuities; refuse unsupported timing evidence rather than manufacturing exact timestamps.

Verification: independently check event times and context after capture gaps, multiple losses and gPTP steps.

**R1 | RESIDUE | Docs | tb/tools/torture_campaign.py:3317, :3591; tests/steps/torture_release_steps.py:239 | New comments retain prohibited identifiers.**

Authority/evidence: the supplied owner comment rule forbids issue-comment IDs and review rounds in added source comments. Two new comments contain `issuecomment-5978644444`; the changed docstring contains `round 3`.

Impact: wording-only source-comment residue, with no required execution or measurement change.

Exact fix: replace the first comment with `Issue #396, REQ-VER-06: the audio counter run shares the soak window.`; remove `(issuecomment-5978644444)` from the second and add `REQ-VER-06`; replace the docstring with `L3 #396 / REQ-VER-06: T0 follows the cycle kind; the hold is recorded separately.` Keep adjacent behavioral explanations.

Verification: inspect added comment lines; untouched historical labels remain outside this delta. R1 does not dirty a lens.

### Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #396 decisions; REQUIREMENTS section 8; planner assertions/graders; Milan 1.2 and IEEE 1722-2016 clauses; F1-F5 | R700-1 applied, no clean covering round | 21faa48242e021177a1dc702f28e51347c6a7a57 |
| RTL | CLEAN | Nine-file diff; unchanged HDL/submodule entries; ARCHITECTURE.md; REGISTER_MAP AVTPRX_TSD and SLIP contracts | R700-1 | 21faa48242e021177a1dc702f28e51347c6a7a57 |
| Robustness | UNCLEAN | Counter/reset/commit branches; framing, alias, corruption, missing-arm and loss probes; F1-F5 | R700-1 applied, no clean covering round | 21faa48242e021177a1dc702f28e51347c6a7a57 |
| Tests | UNCLEAN | Plan feature and release steps; self-tests; torture_release_mutants.py; independent probes/mutant; F1-F5 | R700-1 applied, no clean covering round | 21faa48242e021177a1dc702f28e51347c6a7a57 |
| Docs | UNCLEAN | REQUIREMENTS, CONTRIBUTING, README, TESTING 6d, SAVED_STATE_MATERIALIZATION; F1/F2/F4/F5 | R700-1 applied, no clean covering round | 21faa48242e021177a1dc702f28e51347c6a7a57 |

[R700] PASS RTL - base-to-head nine-file diff and docs/overview/ARCHITECTURE.md - HDL, clock/reset/CDC boundaries and processor gitlinks are unchanged. This desk-only review found no new RTL defect; Python tests supply no RTL/hardware proof.

### Contract and clause audit

Reconstruction used AGENTS/CONTRIBUTING, docs/README, the frozen issue and public owner decisions, requirements/interfaces, then the one-commit nine-file diff and tests. The decisive public sources are [issue #396](https://github.com/kebag-logic/milan-fpga/issues/396), its [owner decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6408072465), [part-A assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6408079016), [audio design](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5978644444), and [reconnect bound #75](https://github.com/kebag-logic/milan-fpga/issues/75).

`plan_audit.json` records all 17 generated steps and confirms that all 80 assertion occurrences have clause and severity fields. Release assertions retain their requirement references. The soak and audio durations are 86400 seconds, with audio inside the soak. Soak observations default to 60 seconds, with continuous transition evidence separately required. Power defaults are 100 idle cold cuts, 50 journal-commit cold cuts and 50 powered soft resets: 200 total, including 150 cold cuts. The plan names the eight inventory items plus binding, complete old/new commit snapshots, ADP valid_time=10 in two-second units, a provisional 30-second automatic-restoration bound and the additional strict less-than-one-second #75 reconnect bound. Fixture topology is ineligible for release until explicitly supplied.

Clause references were checked against the primary Milan v1.2, IEEE 1722-2016 and IEEE 1722.1-2021 texts, not inferred from assertion strings:

| Authority | Checked interpretation |
|---|---|
| Milan 5.3.8.10 Table 5.6; 5.3.7.7 Table 5.4 | Listener/output counter meanings, reset/binding behavior and observation requirements. Zero growth is the owner's stricter qualification rule, not a claim that the standard universally forbids every counter increment. F4 weakens that rule in execution. |
| Milan 4.2.6.2.2/4.2.6.2.3, Tables 4.1/4.2 | gPTP protocol intervals and receipt timeouts remain distinct from the planner's 60-second counter-read period. These device timing authorities cannot be proved by periodic healthy samples. asCapable continuity uses 4.2.6.2.4 and transition evidence. |
| Milan Annex B.1/B.1.1/B.1.2; IEEE 1722 4.4.4.3/4.4.4.7 | The 0.25-second uncertainty minimum, stated implementation 0.5-second upper bound and five-second media-clock holdover are distinguished. mr uses media-clock causes and an eight-PDU hold; a GM change alone is not a valid mr cause. Complete GM/discontinuity history and bounded observation resolution are required. |
| IEEE 1722 4.4.4.6 and 7.3.5 | Packet sequence semantics and chronological, interleaved audio-channel layout are relevant; packet sequencing alone cannot remove the sample-counter ambiguity in F1. |
| Milan 5.3.5.1, 5.3.7.1/5.3.7.6, 5.3.8.1/.2/.3/.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 | Sampling rate, formats, presentation offset, binding, mappings, clock source and names are appropriately mapped. Configuration is explicitly anchored to project issue #70's inventory. F3 concerns the proof of restoration, not that inventory. |
| Milan 5.5.1.4/5.5.2.6; IEEE 1722.1 6.2.2.5; Milan 5.6.2 | Automatic recovery and ADP field semantics are separated from project timing decisions. The power-on/reset-command T0 and provisional restoration bound are public project decisions. The #75 reconnect remains an additional check after automatic recovery, not its substitute. |

REQUIREMENTS section 8 (including REQ-VER-05/06), CONTRIBUTING's release gate, README and TESTING 6d consistently state the 24-hour/200-cycle decision and mandatory evidence. REQ-VER-05 remains the registry requirement; REQ-VER-06 supplies the release qualification contract. The delta uses “the reference peer” and “an external digital capture” without identifying private bench equipment. The docs do not convert NOT RUN into hardware proof. Their substantive grader claims are nevertheless affected by F1/F2/F4/F5.

### Executed evidence

All independent gate commands completed in the foreground, with up to eight concurrent lightweight processes and no heavy bank. Exact commands, return codes and elapsed times are in `gates.json`; corresponding `.log` and `.rc` files retain raw output.

| Check | Result |
|---|---|
| `torture_campaign.py --self-test` | 94 tests passed, rc 0 |
| `cd tests && python3 -m behave --no-capture -f plain` | 14 features, 452 scenarios, 2154 steps passed; none failed or skipped |
| `torture_release_mutants.py` | All 192 shipped mutations killed; rc 0 |
| Release-area plan and coverage | soak/audio/power emitted; all three coverage results complete |
| docs_check, check_doc_paths, TOC check, anchor check, check_em_dash, check_doc_style | All rc 0; 1065 paths resolved, 149 TOC pages checked, 537 fragment links reproduced |
| Python idiom and feature-status gates | rc 0; feature-status self-test 46/46 |
| Base-to-head diff whitespace check | rc 0 |
| Independent grader mutant | Dropped/repeated count changed by +1 in a disposable copy; self-test rejected it, rc 1 as expected |

`probes.py` constructs independent four-channel S32 captures, including six planted arms. `probes.json` and `probes.log` preserve results: exact five-sample drops, four-sample repeats, six-sample silence and reciprocal swaps are detected; the missed-arm case is NOT RUN; logged capture-side losses are attributed separately. The same probe suite reproduces F1-F5. The shipped offline #366, persistence-disabled and planted-drop controls fail their named assertions, as exercised by the self-tests and behavior suite. These passing controls do not cover the additional failing cases above.

Portable reproduction from the packet directory, with an isolated clone at this exact head and the required Python dependencies:

```sh
python3 -B run_gates.py /path/to/clone /path/to/markdown-python
python3 -B probes.py /path/to/clone
python3 -B verify_integrity.py /path/to/clone
```

The scripts create disposable data only under the packet's `scratch/`. Raw default-plan output is retained there for local inspection; the publishable `plan_audit.json` records its digest and release contract without fixture identities.

The [public source-head receipts](https://github.com/kebag-logic/milan-fpga/tree/080e38fb8eb2e965f03b7291c855f32a23ef35ae/review-evidence/396g-r1) were reconciled after independent code review. `public_evidence_checked.json` records 21 fetched files whose hashes match their public manifest, including the exact-head record, source self-tests, behavior suite, documentation gates and mutation receipts. These are author-published source evidence. The throughput receipt explicitly says NOT RUN because arms were absent; it is not a qualifying audio run. No manager source bank exists at this head, and none is inferred.

After the independent verdict and ledger were written, PR comments, formal reviews and review threads were checked for prior findings. The returned public state contained two review-start comments, zero formal reviews and zero review threads; there were no prior findings to resolve or retain. `public_review_state.json` records that reconciliation. No other reviewer's report was read.

### Open items, integrity and remaining duties

The unspecified 997/9973 Hz analog limits are honestly reported: the assertion remains NOT RUN and cannot qualify a physical release. A recorded threshold decision belongs before part-B calibration; it does not warrant an additional part-A finding while the plan refuses a fabricated pass. The soft-reset mechanism is also honestly left to a declared physical hook with timestamp and evidence that power stayed on. The planner does not invent an unsupported protocol reset; part B must validate that mechanism. The provisional 30-second restore bound still requires the recorded measurements and ratification. The 4096-slip limitation is candidly disclosed, but it defeats the accepted desk oracle contract and therefore belongs in this PR as F1, not merely an open future item.

`integrity.json` verifies the published root HEAD/tree, all 1442 tracked root blob bytes and modes, all 1448 index entries, and all gitlinks. It also verifies checked-out bytes/modes/index and registered worktrees for the required verilog-axis, protocol-processor, gptp-processor and tsn-c-stack pins. The initially uninitialized tsn-c-stack was initialized only in this isolated clone. Final status is clean. Source files were never edited; the mutant existed only in `scratch/`.

Physical calibration is NOT RUN. No hardware, HDL simulation, synthesis, builder bank, hosted job or local workflow replica was executed by this review. Field skips and desk passes prove no physical qualification. The manager owns hosted/local workflow acceptance, final current-dev merge-candidate construction and native/builder validation, receipt publication, completion of both independent reviews, residue tracking and merge authorization. Source-head checks here are distinct from that future candidate validation. F1-F5 require correction and independent re-review before their lenses can become CLEAN; no merge approval is given.

R700-1 FINISHED
