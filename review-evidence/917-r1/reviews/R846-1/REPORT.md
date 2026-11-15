[R846] NEGATIVE - exact head 3926c271aaf77420fb9093694be0ab9d511b898d

Round R846-1, external independent review of issue #917 / PR #918. Reviewed tree `09b50fe085b129c81e7b033b9611a861af4fb9d4`, against `cec88385ad0a0ec0d61b91597640797766e45010`, including all three commits. All five lenses were applied. Two substantive findings remain. No receive-datapath failure was observed in the executed checks.

Scope was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, [issue #917](https://github.com/kebag-logic/milan-fpga/issues/917), the [public ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6894152131) and [owner decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6898289590), REQUIREMENTS.md section 1, FR_NFR.md sections 3.4.1/3.4.2, MAILBOX_CONTRACT.md, MAILBOX_SPLIT.md, and IEEE 1722.1-2021. The diff was examined before the published evidence. No private author material or other reviewer's report was read. The source was never edited.

**R846-1-F1 — MINOR — Conformance, Docs — Incorrect controller restriction and timeout attribution.**

Artifacts: `docs/design/MAILBOX_SPLIT.md:277`, `hdl/milan/mailbox/KL_mbx_rx.sv:39`, `tb/verilator/mbx/suite.hpp:393`, `tb/verilator/mbx/suite.hpp:1544`, and PR #918's Description and Authoritative references.

Authority/evidence: IEEE 1722.1-2021 9.2.2.4 defines the message_type field. Section 9.2.2 permits pipelining AEM/Address Access requests; 9.3.6 maintains multiple inflight commands. AEM timeout/retry behavior belongs to 9.3.2.6 and 9.3.6. The changed text instead attributes one-command-in-flight operation to 9.2.2.4. The suite comment also calls exceeding one refill period a controller timeout, although its five-millisecond assertion is a delivery bound, not the standard's 250 ms transaction timeout. See `standard-check.txt`.

Impact: the acceptance workload is presented as a protocol restriction. Readers could infer that compliant pipelined controllers cannot encounter the remaining counted drops. This is a clause/conformance claim, outside the wording-residue exemption.

Required outcome: attribute the one-in-flight workload to #917's public scope and the affected controller behavior; explicitly retain its limit. Cite 9.3.2.6/9.3.6 for timeout/retry behavior, and describe the bench deadline as next-refill delivery. Correct the corresponding source, design and PR assertions without changing the ruled bucket behavior.

Verification: inspect every new one-in-flight/timeout attribution against the clauses and public ruling; retain the passing B0/B1/B2 behavior and the drop-instead-of-hold negative control.

**R846-1-F2 — MAJOR — Conformance, Tests, Docs — The held path invalidates the published ingress allowance and CPU-budget record attribution.**

Artifacts: `docs/reference/FR_NFR.md:426`, `docs/reference/FR_NFR.md:432`, `tb/verilator/ctrl_service_budget/grade.py:54`, `tb/verilator/ctrl_service_budget/grade.py:144`, and the new deferred commit in `hdl/milan/mailbox/KL_mbx_rx.sv:779`.

Authority/evidence: FR_NFR.md requires ingress in the complete response interval and remaining margin, yet still claims a 1 ms ingress allowance based on publication within 64 clocks of the last byte. The new AECP path can wait nearly its 5 ms refill period; the generic mechanism also affects other channels. The CPU-budget `owner()` helper assumes a commit belongs to the most recently completed frame within 64 clocks, classifying all older pending frames as refused. That assumption no longer holds while an older frame is held.

`check_budget_owner.py` executes that exact helper, with an immediate-frame positive control. A held frame ending at cycle 100 and committing at 500100 is refused as following no frame. With a refused follower ending at 500090, the helper assigns the held record's commit to that follower and marks the held frame refused. `budget-owner.log` records both results. This is a constructed-history helper probe, not a CPU-system campaign. The real RTL's delayed publication and preservation through following frames passed the mailbox tests and independent probes.

Impact: the existing 94-group comparison proves equality only for its exercised token-backed inputs. It cannot support the universal ingress allowance, and its grader cannot correctly measure the held path when added. The published 218/228 ms AECP network margins still subtract only 1 ms ingress. This does not establish a 240 ms wire-response violation; it establishes a false allowance and an executable attribution defect caused by deferred publication.

Required outcome: reconcile the authoritative ingress allowance and response-margin table with held and immediate delivery for the affected channels. Preserve the immediate-path bound. Make record attribution distinguish an older held record from later filtered/refused records and other channels, without accepting missing, duplicate or misordered commits. Add a focused held-record budget/attribution case and a negative control. Publish any necessary normative scope decision rather than silently treating the old allowance as satisfied.

Verification: an immediate record still meets its existing bound; a held record is assigned to its own frame and measured with its ingress delay; a later refused frame is never credited with that commit. Check the corrected per-channel allowance and complete-response margins. Re-running the unchanged 8x8 population alone would not resolve this finding because it lacks the triggering empty-bucket input.

**R846-1-R1 — RESIDUE — Docs — New source comments include an issue-comment identifier.**

Artifacts: `hdl/milan/mailbox/KL_mbx_rx.sv:39`, `sw/mailbox/mailbox.yaml:1098`, `tb/verilator/mbx/suite.hpp:782`, `tb/verilator/mbx/suite.hpp:1541`, `tb/verilator/mbx/mutants.py:647`.

Authority/evidence: the owner's 2026-10-15 source-comment rule permits issue and requirement IDs but excludes issue-comment IDs. These added comments contain `6894152131`.

Impact: source-comment convention only; removing the identifier changes no behavior, measurement, clause claim or privacy property.

Required outcome / exact fix: replace `#665, comment 6894152131 item 2` (including its split-line form) with `#665`, retaining #917 and the behavior/reason text. F1 separately governs the incorrect standards claim; removing the identifier does not resolve F1.

Verification: inspect added source-comment lines for this identifier and other new session/lane identifiers. Existing instances outside this delta remain outside this finding. This residue does not make a lens unclean.

**Artifact-specific results and acceptance.**

- **RTL PASS:** examined `KL_mbx_rx.sv:457`, `:509`, `:589`, `:605`, `:729`, `:749` through the channel-state updates. Speculative writes use `wr_head_r`; both occupancy guards reserve held storage and reject a tail ahead of the committed head. Refill releases the held record without moving the write base beneath a following frame. HDR1 uses an existing token or the current refill; release consumes that refill and clears the hold. The serial FSM prevents competing accepted same-channel header commits. Published head visibility remains delayed until the registered header write reaches memory. No new clock/reset domain or CDC is introduced. V0/V1 and B5/B6 check the unchanged immediate path and refill boundaries.
- **Robustness PASS:** applied the frame/channel state, B3-B6, T0/T1, V0/V1, and independent `probe.cpp` P0-P3. Probes covered disable after acceptance, disabled/runt/truncated/identity-filtered followers, counted valid followers, the last fitting ring slot, physical-ring and 16-bit counter wrap over 4,000 held records, and refill during a following frame's reception. Both adapters passed 26 checks; the host model passed 20 applicable checks. B3 covers reset forgetting the held record and restoring the bucket. No overwrite, duplicate commit, lost held payload or held-plus-token state was observed.
- **Conformance:** B0's 50 commands pass for the explicitly stated one-command-in-flight workload, consistent with the issue's regression and permission to drop behind a held record. This is not a promise to accept 50 unpaced pipelined commands. B1 proves the third command is dropped/counts once in RATE_DROP with ERR. B2 delivers 100 commands with nominal 1 ms pacing while respecting one in flight; after token exhaustion it waits for delivery, so it is not a sustained 1 kHz input-rate guarantee. F1/F2 remain open.
- **Contract/model:** `audit.py` regenerated in a disposable tree. `KL_mbx_pkg.sv`, `KL_mbx.sv` and `mbx_contract.h` remain byte-identical to base and head. Parsed YAML is identical: rates, registers, fields, rings and version did not move. `mbx_model.c:262`, `:515`, `:557` mirrors deferred commitment, space accounting and counter precedence. The change is needed for RTL parity; the model is excluded from `ctrl_build.PORTABLE`, `ctrl_image.CTRL_SOURCES` and `ctrl_plat_image.compile_all`. The three changed `test_acmp_mbx.cpp` loops count committed records and wait out held work; their capacity/service expectations are unchanged.
- **Tests:** stock checks passed with 607/652 through the one-interface adapters, 614/659 at two interfaces, 532 on the two-interface host model, and 32 firmware co-simulation checks. The seven new RTL mutants were independently rebuilt and each failed its named assertion. Expected mutant failures are not source-head failures. Published campaigns record four mailbox controls and 238/238 named catches, plus 699/699 firmware catches. The mutation evaluator requires exit 1 and the named assertion; build errors do not count. F2 leaves Tests unclean despite those passes.
- **Docs:** examined the changed generator/reference, design hold section, test README, source comments and public PR evidence against code. Hold visibility, disable behavior, counter precedence and unchanged ABI are documented. F1/F2 remain substantive inaccuracies/omissions; R1 is residue only.

**Published evidence and limits.** The archive is [ee633e64, author-r1](https://github.com/kebag-logic/milan-fpga/tree/ee633e64c0f99b0644076b79b02d2cfaba9faac8/review-evidence/917-r1/author-r1). All 423 available manifest-listed files match their published hashes. These are author receipts, not manager source-bank results.

The 46 fixture-image hash lists match exactly. The split comparison records matching 1x1/1if firmware hash `bb04b69678bda6d7aa21458b5a39da1a611c3211efabd314ff590e06f6c76978` and 8x8/1if hash `506a1ae4da57e1d71f22201f02f4e1df49d6cb110dfe677c5d1fba0e154ca8fb`, with ROM banks. These builds were not independently repeated. The later two commits change no image source or recorded budget build input.

The 1x1 budget comparison records 94 groups with identical scripts, simulation results and table; its aggregate build digest changes with RTL. Seven pre-existing budget misses are not converted into passes. `scenario.py:673` bounds bursts by tokens and space; `save_window.py:210` replenishes tokens before the next burst. This supports unchanged existing service rows and load accounting. Omitting an identical-population 8x8 rerun is a disclosed limit, not the cause of F2. No held-path CPU measurement or universal ingress proof follows from this comparison.

Route receipts identify the exact head, device, recipe and directives. AltSpreadLogic_high meets #818 at all four corners: slow setup +0.203 ns / hold +0.102 ns; fast setup +1.636 ns / hold +0.036 ns; zero failing endpoints. #818 requires WNS >= +0.030 ns and WHS >= 0 ns. All three reported routes meet it. The stronger +0.030 ns hold comparison comes from the separate [#870 ruling](https://github.com/kebag-logic/milan-fpga/issues/870#issuecomment-6779934014), which the helper checks as a second threshold; ExtraPostPlacementOpt misses only that stronger threshold. This does not invalidate the selected route. Area reports LUT +74 to +181, FF +75/+76, unchanged BRAM/DSP. No route was rerun here.

The workflow table contains 139 rc=0 receipts and 226 explicit skip reasons. Of those executed receipts, 137 have readable exact-head log headers; two larger logs are published only by hash/size plus rc (BDD and docs gate 41). Four earlier sweep shards total 65/65 at `84d8a214`; the mailbox-containing shard is 17/17 at the reviewed head. The two later commits affect docs and mailbox test/mutation text, not RTL or firmware-image inputs. Skipped orchestration/install/physical work is not executed evidence. No hosted or local-replica acceptance verdict is inferred here.

**Prior public findings.** After the independent diff pass, the PR conversation, submitted reviews and review threads were checked. The retrieved conversation contained two review-start notices; reviews and threads were empty. No prior public review finding was available to resolve or retain. `public-scope.json` records this snapshot. No other reviewer's report was consulted.

**Reviewer-owned coverage ledger.** CLEAN means no open BLOCKER, MAJOR or MINOR under that lens; it does not complete merge or hardware duties.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | #917/#665 decisions; IEEE clauses; REQUIREMENTS section 1; FR_NFR:353,414,426,432; YAML/generated ABI; B0-B6 | R846-1 applied; no clean covering round | 3926c271aaf77420fb9093694be0ab9d511b898d |
| RTL | CLEAN | KL_mbx_rx.sv:457,509,589,605,729,749; registered ring interface; route receipts; stock-mailbox.log; probe-0.log; probe-1.log | R846-1 | 3926c271aaf77420fb9093694be0ab9d511b898d |
| Robustness | CLEAN | KL_mbx_rx frame/channel state; suite.hpp B3-B6/T0/T1/V0/V1; probe.cpp P0-P3; probe-model.log | R846-1 | 3926c271aaf77420fb9093694be0ab9d511b898d |
| Tests | UNCLEAN: F2 | suite.hpp; bench.hpp; mutants.py; ctrl_mutants.py; test_acmp_mbx.cpp; grade.py:144; stock/probe/mutation and published campaign receipts | R846-1 applied; no clean covering round | 3926c271aaf77420fb9093694be0ab9d511b898d |
| Docs | UNCLEAN: F1, F2; R1 residue | MAILBOX_SPLIT; MAILBOX_CONTRACT; FR_NFR:426,432; mailbox README; source comments; issue/PR/evidence | R846-1 applied; no clean covering round | 3926c271aaf77420fb9093694be0ab9d511b898d |

**Reproduction and integrity.** Portable scripts take checkout and packet paths; build scripts also take the compiler-wrapper path. `run_stock.py` runs the four mailbox targets, `run_probes.py` the independent boundaries, `run_mutations.py` the seven defects, `check_budget_owner.py` the attribution counterexamples, and `audit.py` source/ABI/receipt checks. Builds remain in `scratch/`; concurrent builds stayed below 16 workers. The first stock attempt lacked a copied common harness directory and failed during setup; the corrected run passed. Published logs normalize local paths only, with raw originals retained in unpublished scratch. MANIFEST.sha256 lists the publishable receipts.

The mailbox benches use explicit millisecond pulses, with 24 clocks per modeled millisecond. Their results establish functional sequencing, not CPU wall time or physical calibration. The grader counterexample uses the actual design frequency of 100 MHz and is explicitly a helper-level history probe.

The final audit proves all 1,606 tracked superproject blob bytes/modes, the index, exact head/tree, and required submodule gitlinks and tracked bytes/indexes. The four required pins plus lwSRP match the source head. No source fixes, commits, pushes, GitHub writes, hardware access or manager banks were performed.

**Pending manager duties and real limits.** F1/F2 require correction and independent re-review; resulting artifact changes invalidate affected lens coverage. The manager owns the current-dev merge candidate, including synchronization with the moved dev-soft-core base, builder/native banks, hosted/local-replica acceptance and receipt publication. This review proves neither that merge tree nor a manager source-head bank. Three hardware descriptor walks remain owed to the bench campaign; physical calibration is NOT RUN, and field skips are not hardware proof. Merge authorization, other independent review completion, candidate validation, post-merge containment and final issue closure remain outstanding.

R846-1 FINISHED
