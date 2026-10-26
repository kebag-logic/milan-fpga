[R700] NEGATIVE - exact head a3e24ac5ef984cb92458f1728f2c275349ae9854

External independent review R700-2, issue #396 part A / PR #786. Tree `0b14ef1a593071516d72535e62bce90537c6364e`. Source base `e76a755afc0536453161e3cd33f6f4d2dcd7641f`; reviewed delta `21faa48242e021177a1dc702f28e51347c6a7a57..a3e24ac5ef984cb92458f1728f2c275349ae9854`, one commit, six files. All five lenses were applied. Unchanged scope retains the R700-1 assessment. One MAJOR and one MINOR remain; neither is deferred. No new RESIDUE or SUGGESTION is added.

## Findings

### F1 | MAJOR | Conformance, Robustness, Tests, Docs | Capture-boundary slips can still earn PASS

**Artifacts:** `tb/tools/torture_campaign.py:4136`, `:4199`, `:4459`, `:4487`; `docs/testing/TESTING.md:1340`, `:1345`; `REQUIREMENTS.md:408`; `delta-probes.json`, rows `tail-slip-8191-2048`, `tail-slip-8190-8192`, `tail-slip-chunked`, and `tail-slip-8191-4096`.

**Authority/evidence:** the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6409763644) requires zero-glitch proof throughout the run and correctly graded edge events. The independent generator in `delta_probes.py` supplies four channels, all six required planted arms, valid wall/gPTP anchors and an explicit empty discontinuity log. Dropping 2048 source samples at stored index 8191 of 8192 returns **PASS**, no DUT event, no missed arm and zero unsupported timestamps. Dropping 8192 samples at index 8190 also passes. The 113-byte chunked form reproduces the first false pass.

The retained hashes show these truncated captures are byte-identical to the clean control: the new code bit has not exposed the changed block before capture ends. This is an observation-boundary ambiguity, not a demand that identical bytes decode differently. Nevertheless, the grader certifies the entire stored duration without sufficient observation beyond the qualified endpoint or an uncertified-tail indication. The plan supplies no such guard. The full sequence's long period does not solve this shorter observation problem.

The documented fallback is inaccurate too: a 4096-sample drop at the last frame produces four `bit-flip` events with mask `0x00000100`, without `unresolved`. TESTING says a slip in the last 63 samples carries `unresolved`. The self-test covers a four-sample endpoint slip, but misses whole-block endpoint ambiguity. At the other edge, `initial-slip` reports ten corrupt words from index zero for a 4096-sample slip at index ten, demonstrating the need to distinguish acquisition from the qualified interval.

**Impact:** a DUT sample slip can receive the zero-glitch verdict with all controls and timestamps present. This retains R700-1 F1's unresolved proof obligation, although its original interior 4096-sample reproducer is fixed. Packet sequencing does not resolve this on the outbound or TDM-loop paths.

**Required outcome:** qualify only an explicitly bounded interval supported by sufficient acquisition and trailing observation, or refuse evidence unable to support that interval. Do not count an unobservable tail as proved clean. Preserve the full required 24-hour qualified duration. Reconcile endpoint classification/uncertainty in the grader, plan, requirements and TESTING. Narrowing accepted proof requires a public scope decision.

**Verification:** retain the byte-identical endpoint pairs; exercise whole-block slips near both boundaries, with and without sufficient guard observations, both byte orders and chunking. An affected qualified interval must not PASS without supporting evidence. Uncertainty must not become an exact corruption claim. Add a named control for the qualifying-interval rule.

### F2 | MINOR | Conformance, Robustness, Tests, Docs | The constant-mask rule changes silently at 64 samples

**Artifacts:** `tb/tools/torture_campaign.py:3920`, `:4146`, `:4164`; `docs/testing/TESTING.md:1332`, `:1339`; `delta-probes.json`, rows `constant-code-xor-63`, `constant-code-xor-64`, `constant-code-xor-100`, `constant-code-xor-chunked`.

**Authority/evidence:** the new canonical rule says two or more words leaving and returning to the track with one constant XOR mask form one corruption. It expressly chooses that interpretation even when slips could produce the same words. The independent probe XORs `0x00000100` into channel 2 at indices 3000-3099, then returns to the original track. The result is a **499717412864-sample repeat**, followed by a drop of that same size, with no corruption or uncertainty marker. A 63-word burst reports one corruption correctly; a 64-word burst already switches to the enormous slip pair. Chunking does not change it.

The inverted code can decode as another valid block. `_step` closes and adopts that track after 64 samples, before `_audio_excursion` sees the return. This is a real ambiguity; the finding is the contradiction with the chosen rule and unqualified exact-class claim, not a claim that physical cause is always uniquely inferable.

**Impact:** the run still FAILs, but its class and counts misdirect diagnosis. The limits and tests do not disclose or pin this transition. This is the remaining compound-event concern from R699-1 F1; R700-1 F2's original tag and short-burst cases are corrected.

**Required outcome:** apply the documented interpretation consistently, or explicitly represent and document this longer-burst ambiguity under the assignment's allowance for genuine ambiguities. Do not present the measurements as unconditionally exact slips. Align the assertion text and add a boundary test.

**Verification:** independently generate constant-mask excursions of 63, 64, 65 and 100 words, including chunk and source-block boundaries. Require the documented class or uncertainty, and show that removing its handling fails a named check.

## Prior findings and assignment reconciliation

The independent delta pass and initial assessment were recorded in `independent-pass.txt` before deliberate prior-finding reconciliation. Public [R700-1 findings](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6409757802) and [R699-1 findings](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6409756577) were then checked at their causes. No other round-2 report was consulted.

| Prior item / assignment | Disposition and evidence at this head |
|---|---|
| R700 F1: repeating signal; R699 F3: false sequence-counter backstop | Interior cases fixed; R700 F1 retained as boundary F1 above. The incorrect backstop sentence is removed. Original layout-ported 3000/4096 probes report exact drops; independent +/-3000, +/-4096, 8192 and 409600 probes fail correctly. |
| R699 F1: holds, bursts, edges, static swap | Holds, short bursts and static swaps corrected; boundary/compound obligations remain under F1/F2. `hold` reports repeat 1 then drop 1 on every channel. `static-swap` FAILs with two full-run swaps and every arm found. |
| R700 F2: tag integrity, copies, adjacent corruption | Original defects resolved; longer-burst limitation recorded separately as F2. Original layout-ported tag flip preserves mask `0x00200000`; unilateral copy is corruption; two `0x400` corruptions form one two-word corruption. Self-test checks all 32 container bits and reciprocal exchanges. |
| R700 F3: pending defaults; missed commit window | Resolved. All-default and single-default pending snapshots are NOT RUN. Valid old/new snapshots PASS inside `[40,41)`; mixed state FAILs. Cuts at 39 or 41 are NOT RUN with `the cut hit no journal commit`. Bare pending snapshots cannot PASS. |
| R700 F4: planted exceptions spanning read intervals | Resolved. Original 0/60-second probe with a 10-20-second plant FAILs. Edge-bracketed in-window growth PASSes; growth after the window FAILs. Both reads must lie within that input's window. |
| R700 F5: capture-loss clocks | Resolved for the checked timing contract. Original no-anchor probe now returns null timestamps with a reason. Independent anchored 409600-frame loss puts event 3000 at acquisition index 412600, wall 108.5958333333 and gPTP 208.5958333333. Four capture drops remain separate from one DUT corruption. A gPTP step yields null gPTP with its reason. Multiple-loss branches pass the self-test. |
| R699 F2: surviving G07, G12, R03 | Resolved. Unchanged public runner: 22 KILLED, 0 SURVIVED, six obsolete anchors INVALID. Separate raw receipts prove G07 fails `test_audio_capture_loss_needs_every_channel`; G12 fails `test_audio_tag_integrity_decides_first`; R03 fails `test_release_commit_cut_evidence`. |
| R699 R1 / R700 R1: source comments | Resolved. Inspection and `comment-scan.json` find no prohibited added identifiers. Both issue-comment IDs and the changed `round 3` docstring are removed. |
| R699 S1, S2, S3 | S1/S2 adopted; S3 remains optional and publicly declined. Arms occupy first/last tenth; the fast path is per-channel. No independent throughput figure is claimed. gPTP tolerance-hold expansion remains outside this delta. |

The period arithmetic is correct: `2^11 * 2^32 = 8796093022208` frames, about **530.243 days at 192 kHz**, versus **16588800000** frames in 24 hours. The multiplier is odd, hence bijective modulo `2^32`. The rate reference now names Milan v1.2 6.2/Table 6.1 rather than the listener-buffer clause. This establishes sequence period, not boundary observability. S32 packing, tags and byte-order handling preserve the capture interface. Existing counter authorities, inventory, clocks/reset/CDC and ADP/rebind rules retain their prior assessment outside this delta.

## Executed and public evidence

Commands completed in the foreground. Independent lightweight checks ran concurrently, with at most nine test processes, no heavy build and no candidate source modification. Exact commands and exits are in `checks.json`; associated logs are raw receipts.

| Check | Result |
|---|---|
| Planner `--self-test` | 103 tests, rc 0 |
| Full `cd tests && python3 -B -m behave --no-capture -f plain` | 14 features, 469 scenarios, 2206 steps; zero failures/skips |
| Release-area coverage | soak/audio/power complete, rc 0 |
| docs_check, paths, TOC, anchors, em-dash, style | All rc 0; 1065 paths, 149 TOC pages, 538 fragment links |
| Python idiom, feature status and its self-test, diff whitespace | All rc 0 |
| Original R700 probe source, unchanged bytes | Executed. Old encoding yields NOT RUN; script exits 1 at its removed count-mutation anchor, occurrence count zero. Traceback and partial results retained. This is INVALID compatibility evidence, not a killed behavioral mutant. |
| Minimal independent R700 port | Only word encoding and count-mutant anchor changed; `round1-port.patch` records every change. Original cases rerun. Count mutant killed by named failures including `test_audio_grader_classes` and `test_audio_block_slips_are_sized_exactly`. |
| Prior public 28-mutant runner, unchanged | Pristine self-test/feature pass; 22 killed, six obsolete anchors, no surviving valid mutation |
| Independent delta probes | Reproduce F1/F2; positive controls and corrected prior defects behave as recorded in `delta-probes.json` |

The [published source packet](https://github.com/kebag-logic/milan-fpga/tree/33f88334442dfebf6829ec5b051eb41835bb32c4/review-evidence/396g-r1) was checked against its manifest for **23 files**, including source identity, author self-test, behavior summary, documentation/mutation receipts and public prior scripts. `public-evidence-checks.json` identifies each digest. The author receipt reports **219 mutations killed**; that whole shipped campaign was not redundantly rerun here. Its exact-head record agrees with the clone. Published receipts for the six re-anchored equivalents and the 14 new/changed arms failing the prior planner were spot-checked; these remain author evidence, distinct from reviewer execution.

**Signature limit:** the public evidence commit API reports `verified: false`, `reason: unsigned`. `packet-provenance.json` retains its identity and verification fields. Public receipt hashes were verified; cryptographic signer authentication is not claimed. No manager source bank exists at this head, and none is inferred.

Portable reproduction from the packet directory:

```sh
python3 -B run_checks.py /path/to/exact-clone /path/to/pinned-markdown-python
python3 -B rerun_round1.py /path/to/exact-clone
python3 -B survivor_checks.py /path/to/exact-clone
python3 -B delta_probes.py /path/to/exact-clone
python3 -B verify_integrity.py /path/to/exact-clone
```

Disposable artifacts stay under packet `scratch/`. Required unchanged public scripts are included in the manifest. The Markdown interpreter needs the pinned renderer; the test interpreter needs behave. The original compatibility failure is explicitly distinguished from a killed mutation or failed gate.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1/F2 | #396 decisions/assignment; REQUIREMENTS:333,402,439; planner assertions and counter/state/audio graders; independent events | R700-2 applied; no clean covering round | a3e24ac5ef984cb92458f1728f2c275349ae9854 |
| RTL | CLEAN | Six-file delta/full nine-file inventory; empty HDL/firmware/gitlink diff; REGISTER_MAP:1300,1922,1923; thdn.py:61; S32 arithmetic; verified pins | R700-2 delta; R700-1 unchanged scope retained | a3e24ac5ef984cb92458f1728f2c275349ae9854 |
| Robustness | UNCLEAN: F1/F2 | Counter windows, identity acquisition, edges, XOR lengths, slip directions, chunking, commit boundaries, planted windows, losses/gPTP steps | R700-2 applied; no clean covering round | a3e24ac5ef984cb92458f1728f2c275349ae9854 |
| Tests | UNCLEAN: F1/F2 | _ReleaseGateChecks; feature/steps delta; shipped mutation anchors/receipts; unchanged prior mutation runner; survivor controls; independent probes | R700-2 applied; no clean covering round | a3e24ac5ef984cb92458f1728f2c275349ae9854 |
| Docs | UNCLEAN: F1/F2 | REQUIREMENTS section 8; TESTING 6d; PR round-2 body; public scope; CONTRIBUTING/README/materialization base-to-head changes; docs gates/comment scan | R700-2 applied; no clean covering round | a3e24ac5ef984cb92458f1728f2c275349ae9854 |

[R700] PASS RTL - base-to-head diff has no HDL, firmware, builder or gitlink change; `REGISTER_MAP.md:1300,1922,1923` and `tb/tools/thdn.py:61` remain consistent with the plan's register/S32 interfaces. Desk tests establish no hardware correctness result.

## Integrity, limits and remaining duties

`integrity.json` verifies root HEAD/tree, all **1442 tracked blob bytes/modes**, all **1448 index entries**, and every root gitlink. Required submodules are verified against pins, bytes/modes, indexes and registered superproject relationships: axis 214 blobs, protocol processor 704, gPTP processor 107, stack 98. The initially absent stack was initialized only in this clone. Final status is clean. Candidate source bytes were never changed; all mutations stayed under packet `scratch/`.

Physical calibration is **NOT RUN**. Field skips, offline controls and desk passes are not hardware proof. No simulation/synthesis/builder bank, hardware action, hosted execution, local workflow replica, commit, push or GitHub write occurred. Hosted/act acceptance remains the manager's duty; this report claims no executed hosted context.

Source base is `e76a755a`; the assignment's live dev is `a8594bb95631fa5c49d18fa0bbc9530e31ad59aa`. These source-head checks do not validate the future current-dev merge candidate. The manager must construct and validate that candidate, run the required native/builder banks, publish receipts, reconcile both reviews, obtain merge authorization and complete containment. F1/F2 require correction and re-review first.

Part B remains open. The later public owner decision specifies AECP REBOOT for the 50 powered resets and analog baseline-plus-6-dB limits after first-hour measurement. These are physical preparation duties, with REBOOT implementation still required. The provisional 30-second restoration ceiling still needs ratification. None may be presented as measured release success; this part-A PR must not close physical acceptance items.

R700-2 FINISHED
