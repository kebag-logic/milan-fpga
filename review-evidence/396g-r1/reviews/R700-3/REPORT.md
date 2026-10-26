[R700] POSITIVE - exact head 4d69e1923ce8209029af6e084336f13cca834c29

External independent review R700-3, issue #396 part A / PR #786. Tree `55e22fe10172e2965687b6fbab734cab19fe183d`. Reviewed delta: `a3e24ac5ef984cb92458f1728f2c275349ae9854..4d69e1923ce8209029af6e084336f13cca834c29`, two commits, six files. Source base: `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. The R700-2 ledger stands outside this delta.

All five lenses were applied. The five assigned prior findings are resolved at their causes. No BLOCKER, MAJOR, MINOR or RESIDUE remains in the reviewed delta. One optional SUGGESTION follows. This is a source review verdict, not acceptance of the future merge candidate or a physical release.

## Authority and scope

Reconstructed from AGENTS.md and CONTRIBUTING.md, docs/README.md, the issue body and public owner/manager decisions, REQ-VER-06, TESTING section 6d, the S32 capture and register interfaces, then the base-to-head inventory, delta and history. Prior public findings were reconciled after the independent code pass. No current-round peer report or private author material supplied the verdict.

The [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6413452035) permits proof of a bounded observed interval while retaining the full 24-hour qualified-duration requirement. The [owner values](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6408072465) remain 24 hours, zero DUT-attributed audio events, and 200 power cycles. Physical acceptance items 3 and 4 remain part B. The PR correctly uses `Relates to #396`.

The delta changes no HDL, firmware, builder, CSR address, counter encoding, byte packing, submodule pin, protocol timeout, reset or CDC contract. Unchanged protocol clauses retain the preceding review's assessment; this round does not claim a fresh full protocol audit.

## Prior findings and assigned outcomes

| Prior finding | Disposition at this exact head |
|---|---|
| R700-2 F1, MAJOR, Conformance/Robustness/Tests/Docs: capture-boundary proof | **Resolved.** `_CounterScan.qualified` (`tb/tools/torture_campaign.py:4461`), `_audio_qualified` (`:4676`) and the duration check (`:4799`) bound and enforce observed time. `_audio_boundary` (`:3993`) and `_audio_open` (`:4081`) distinguish unconfirmed boundary changes. REQUIREMENTS.md:414 and TESTING.md:1353 state the same limit. Unchanged endpoint probes, the minimal duration port and independent guarded/endian/chunk cases agree. |
| R700-2 F2, MINOR, Conformance/Robustness/Tests/Docs: mask rule at 64 | **Resolved.** `_AudioImage` (`:4263`), `_CounterScan._close` (`:4389`) and `_audio_excursion` (`:4033`) preserve the chosen interpretation. Original 63/64/65/100-word probes each yield one bit-flip. Independent masks `0x100`, `0x80000`, `0x200`, through 66,000 words, preserve class, mask and affected-word total; bounded pieces are permitted. TESTING.md:1337,1350,1388 explains the rule and bound. |
| R699-2 F1, MINOR, Conformance/Robustness/Tests/Docs: slip plus corruption | **Resolved.** `_audio_fit` (`:3980`) splits runs around unexplained words; `_audio_window_events` (`:4170`) re-evaluates departures after offset changes. The self-test and independent compound probes find both distinguishable events. DUT slips near planted flips FAIL with arms found; the passing self-test covers arms 10,40,63 samples apart. Published unmodified compound/arm receipts agree. Indistinguishable cases are explicitly disposed below. |
| R699-2 F2, MINOR, Conformance/Robustness/Tests/Docs: last-63-sample slips | **Resolved.** Observable code-only boundary stretches are `unresolved` with bounded `located_within`, not exact corruptions. Invisible slips outside the interval never certify the tail. A logged loss outside the interval is refused by name (`:4781`). Original endpoint probes and published edge receipts agree with TESTING.md:1382,1431. |
| R699-2 F3, MINOR, Tests: loss at the event index | **Resolved.** `test_audio_capture_losses_advance_the_clocks` (`:8014`) checks index and both clocks at the loss itself. The feature at `tests/features/torture_campaign_plan.feature:514` checks the boundary. Independent N07 mutation retains the exact old replacement and fails this named self-test. |

Earlier findings remain resolved. The interior-slip, tag/copy/static-swap and hold cases still pass their regression checks. The unchanged round-2 probes again exercise pending-default and commit-window refusals, planted-window boundaries and capture-loss clocks. The self-test retains these arms. The public receipt for the unchanged prior mutation runner reports 32 killed, zero survivors, zero invalid anchors. No finding is moved to another issue in place of correction.

The four prior suggestions were adopted: capture-after-flow guidance, anchor gaps, bounded failure to acquire, and the documented window limit. Added source comments contain none of the prohibited lane, reviewer, round or issue-comment identifiers (`comment-scan.json`).

## Interval and classification evidence

The first qualified sample in the clean 8,192-frame probe is **63**. The exclusive end is **8129**, so the last qualified sample is **8128**. Its interval is **[63,8129)**: **8,066 observed frames**, or **0.16804166666666667 seconds at 48 kHz**. The initial-slip probe instead qualifies **[73,8129)**.

The clean capture and both endpoint pairs remain byte-identical, SHA-256 `f395a643b6d210b302c6e8cd7a8e4b849fd420f307f44e6bb4c59951b7493c6f`: drop 2048 at index 8191, and drop 8192 at index 8190. All three are **NOT RUN** under the unchanged script's default `required_s=86400`. With only the explicit short required duration supplied, they PASS **only [63,8129)**. Requiring the whole capture duration is NOT RUN. The slips are outside what is proved; unobservable tails never become clean evidence.

The original 4096-sample final-frame slip and initial slip are unresolved. The original tail probe with 64 more frames is FAIL with unresolved events; sufficient further observation resolves guarded cases to sized slips. Both byte orders and 113-byte chunks preserve outcomes. Logged losses advance acquisition indices and clocks but add no observed frames to duration. Unacquired channels and out-of-interval arms/losses are refused.

The independent matrix contains 134 cases: 80 boundary/duration, 24 mask and 30 compound cases. All 24 mask cases match the documented rule, including lengths 65535,65536,65537,66000. Twenty-eight compound cases report both injected classes directly. The other two are the proved byte-identical cases below, not unreported failures. These are synthetic grader measurements; no 24-hour physical capture ran.

## Optional finding

### S1 | SUGGESTION | Tests, Docs | Pin two concrete compound ambiguities

**Artifact:** `tb/tools/torture_campaign.py:3980,4170`; `docs/testing/TESTING.md:1378`; `boundary-matrix.json` rows `compound-4096-1-100`, `compound-4096-1-80000`; `compound-ambiguity.json`.

**Authority/evidence:** the documented short-cluster rules select compatible offsets and acknowledge indistinguishable signals. Independent four-channel captures prove these byte equalities on channel 2:

- Drop 4096 at 3000, XOR `0x100` at 3001, equals a single drop 4096 at 3005.
- Drop 4096 at 3000, XOR `0x80000` at 3001, equals repeat 1024 at 3001 followed by drop 5120 at 3002.

The other three channels match in each pair. Full-capture hashes match, respectively `3d005e4f54680e96861c4ce6333d5cd9fde0d67a9504f650fe4f03e563bccabf` and `c0dd365ae897ba87d95fa3aaf70a232052355c13e1952865ea9902f94854383c`. Both runs FAIL with every planted arm found. The bytes cannot identify a unique injected cause; the selected readings agree with the existing ambiguity rule.

**Impact:** no false PASS or regression is established. Explicit examples would prevent future tests from demanding impossible physical-cause recovery.

**Suggested outcome:** optionally add named equality controls and a short example beside the cluster rule. No acceptance change is required.

**Verification:** `python3 -B compound_ambiguity.py /path/to/exact-clone` proves equality; `boundary_matrix.py` records classes and verdicts.

## Test causality and gates

Commit `4d69e192` changes only the invalid-anchor arm. It retains earlier malformed/zero-index/reversed-index/backward-time/past-end cases, adds equal-wall-time refusal and a valid-anchor PASS control, and asserts the refusal reason. The explicit short duration makes the anchor defect decide the verdict. Production grading and earlier arms are not relaxed.

Independent **N07, N30, N31** mutations each return rc 1 and fail `test_audio_capture_losses_advance_the_clocks`. Five more mutations covering the qualified end, required duration, constant-mask adoption, run splitting and re-evaluation after a slip fail their named tests. The pristine self-test passes. `spot-mutants.json` and raw logs establish behavioral kills; no parser error or invalid anchor is counted as a kill.

| Executed in this clone | Result |
|---|---|
| Planner `--self-test` | 108 tests, rc 0 |
| Full `cd tests && python3 -B -m behave --no-capture -f plain` | 14 features, 481 scenarios, 2244 steps; no failures/skips |
| Release-area coverage | soak/audio/power complete, rc 0 |
| docs_check, paths, TOC, anchors, em-dash, style | All rc 0; 1065 paths, 149 TOC pages, 538 fragment links |
| Python idiom, feature status and self-test, whitespace | All rc 0 |
| Unmodified R700-2 `delta_probes.py` | rc 0; exact published bytes |
| Minimal required-duration port | rc 0; changes in `qualified-probes.patch` |
| Independent matrix and equality proof | rc 0; outcomes and ambiguity disposition above |
| Eight focused mutations | All killed by named assertions |

Independent lightweight checks ran concurrently with at most eight mutation workers. The foreground driver waited for every subprocess; no detached job or heavy build ran. Exact commands, exits and raw receipts are retained. Candidate source bytes were never edited.

## Published evidence

Verified **83 archived files** against the manifest at [evidence commit a1ee144d](https://github.com/kebag-logic/milan-fpga/tree/a1ee144df01e081225919a557a6113a98e2f90b2/review-evidence/396g-r1), including source identity, author gates and prior probe source. `public-evidence-checks.json` records each digest; `verify_public_evidence.py` reproduces verification. The unchanged probe also matches its prior published manifest.

Spot-checked author receipts report **249 shipped mutations killed**, nine feature mutations detected, all gate return codes zero and the unchanged prior 32-mutant runner fully killed. The transplanted-test receipt distinguishes behavioral failures from missing-interface errors. These are **author evidence**, not reviewer executions of the whole campaign; that campaign was not redundantly rerun.

**Signature limit:** the evidence commit is **unsigned**, with public verification fields `verified: false`, `reason: unsigned` (`packet-provenance.json`). Receipt hashes and repository provenance were checked; signer authentication is not claimed. No manager source bank exists at this head, and none is inferred.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #396 assignment; REQUIREMENTS:408-432; planner assertions, qualification and duration predicate; endpoint pairs | R700-3 delta; R700-2 outside delta | 4d69e1923ce8209029af6e084336f13cca834c29 |
| RTL | CLEAN | Empty HDL/firmware/builder/gitlink delta; thdn.py:61; TESTING:1284 S32 layout; REGISTER_MAP:1922-1923; verified pins/bytes | R700-3 delta; R700-2 outside delta | 4d69e1923ce8209029af6e084336f13cca834c29 |
| Robustness | CLEAN | Boundary/fit/image paths; guards, masks through 66000 words, endian/chunk variants, compound equality, loss/arm refusals | R700-3 delta; R700-2 outside delta | 4d69e1923ce8209029af6e084336f13cca834c29 |
| Tests | CLEAN | _ReleaseGateChecks:8014-8350; feature:477-516 and steps delta; pristine gates; eight named mutation failures; verified author receipts | R700-3 delta; R700-2 outside delta | 4d69e1923ce8209029af6e084336f13cca834c29 |
| Docs | CLEAN | REQUIREMENTS section 8; TESTING:1275-1434; qualification/counter_limits; public PR and decisions; comment scan; docs gates | R700-3 delta; R700-2 outside delta | 4d69e1923ce8209029af6e084336f13cca834c29 |

S1 is optional and leaves no lens unclean. This ledger does not clear pending workflow or physical gates.

## Integrity, limits and manager duties

`integrity.json` verifies HEAD/tree, **1442 tracked blob bytes/modes**, **1448 root index entries**, and all root gitlinks independently of status flags. Required submodules match pins, blob bytes/modes, indexes and registered superproject relationships: axis 214 blobs, protocol processor 704, gPTP processor 107, stack 98. The initially absent stack was initialized at its pin only in this clone. Final status is clean. Disposable copies remain under packet `scratch/`, excluded from publication.

Physical calibration is **NOT RUN**. Field skips and synthetic passes are not hardware proof. No full native/processor/synthesis/builder bank, hardware action, local workflow replica, source fix, commit, push, merge or GitHub write occurred. Hosted contexts were not inspected or accepted here.

The manager must build and validate the **current-dev merge candidate**, run required builder/native banks, and publish receipts. Source base is `e76a755a`; the assignment identifies live dev as `76de691e5625cc4ea2f9a19def9e07c1183a14ee`. This review validates neither their future merge tree nor later dev changes. Hosted/replica acceptance, the other independent verdict, final review reconciliation, explicit merge authorization and post-merge containment remain manager duties.

Part B remains open. The later owner decision specifies AECP REBOOT for 50 powered resets and first-hour analog baseline-plus-6-dB limits. The PR acknowledges that plan text still needs those separately routed updates; this unchanged preparation work is outside the assigned delta. REBOOT implementation, recorded analog limits, physical campaigns and controls, and ratification of the provisional 30-second restoration ceiling remain necessary before release success can be claimed. This PR must not close physical acceptance items.

Publish only REPORT.md and files listed in MANIFEST.sha256. Reproduction scripts: `run_checks.py`, unchanged `delta_probes.py`, `qualified_probes.py`, `boundary_matrix.py`, `compound_ambiguity.py`, `spot_mutants.py`, `verify_public_evidence.py`, `verify_integrity.py`. Each takes the exact clone path; `run_checks.py` also accepts the pinned Markdown interpreter. Git evidence objects must be present for public verification.

R700-3 FINISHED
