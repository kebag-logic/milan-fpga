[R674] POSITIVE - exact head 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d

External independent review, R674-3, issue #765 / PR #769. Tree `95076a30447b31a37d02298bf87b4fdd6a809d89`. All five lenses are CLEAN. R673-2-F1 is resolved. No BLOCKER, MAJOR or MINOR remains from this review. One inherited wording RESIDUE and four retained optional suggestions are recorded below. This is a source review verdict; the final merge candidate and manager acceptance remain pending.

Scope and reconstruction

The review followed AGENTS.md, CONTRIBUTING.md, docs/README.md, the [issue and frozen acceptance](https://github.com/kebag-logic/milan-fpga/issues/765), its public scope decisions, FR-STR-03 (`docs/reference/FR_NFR.md:271`), the live compliance entry (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:190`), and the relevant interface/implementation artifacts. Governing clauses remain Milan v1.2 4.4.2.2, Table 5.6 with Table 5.16, and Table 6.2; the wire count is the ten-bit field of IEEE 1722-2016 7.3. Their round-one interpretation is carried forward: no requirement or interface changes this round.

The stacked `4191b098..87a2b77d` history and relevant comparator/test changes were reconstructed, separating inherited merged work from #765. This later-round review concentrates on the single commit after `d4a27e6334118c9eef1023aa27e9fd2b7de9f076`, as the [round-three assignment](https://github.com/kebag-logic/milan-fpga/pull/769#issuecomment-6299394328) requires. The four changed files are recorded in `receipts/round3.diff`. Existing coverage from [R674-1](https://github.com/kebag-logic/milan-fpga/pull/769#issuecomment-6297113349) at `75db4b57cff47bb614d14dead084649a4c2aa2a3` and [R674-2](https://github.com/kebag-logic/milan-fpga/pull/769#issuecomment-6299266323) at `d4a27e6334118c9eef1023aa27e9fd2b7de9f076` carries forward where dependencies are unchanged.

An independent delta verdict and five-lens ledger were written before opening prior findings or reports. The prior public findings were then checked at their causes. No private author material, management checkout, or other current-round report was read. Public execution receipts were read after the source pass. The final PR snapshot still names the requested head; submitted reviews and inline review comments are empty, with prior findings in the issue-comment reviews.

Assigned correction: R673-2-F1

| Artifact at this head | Result |
|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:182-192` | Says the low eight bits must be nonzero, identifies `channels_per_frame[7:0]`, and explicitly says 256 is rejected. The former “drive any count” sentence is also corrected. |
| `tb/verilator/avtp_rxmon/sim_main.cpp:460-464` | The [28] banner states the same low-byte limitation. It distinguishes the device listener's current-format rule. |
| `tb/verilator/tsn_fuzz/fuzz_aaf.py:141-150` | The rationale describes the instrument's eight-bit read and the separate shipped listener's mismatch rejection, with #765, FR-STR-03 and clause references. |
| `tb/verilator/tsn_fuzz/fuzz_aaf.py:176-180` | The docstring describes each probed count, the low-byte predicate, and rejection relative to the device's current format. |
| `tb/verilator/tsn_fuzz/fuzz_aaf.py:181-186` | The title is generated from the unchanged tuple `(1, 2, 3, 4, 8)`. Its parenthesis says the device rejects a count other than its current format's; it does not claim every probe is rejected. |
| `hdl/ieee1722/avtp/doc/TEST_RESULTS.md:29,96` | Both generated titles match the corrected campaign. The timestamp and these two titles are the only changes; 164 passes and the same checks remain. |
| PR body, current Known limitations | Explicitly describes low-eight-bit acceptance, rejection of 256/512/768, and the shipped ten-bit current-format compare. Former titles in the Round 2 history are identified as former wording corrected in Round 3. |

The predicate at `KL_avtp_rx_monitor.sv:178,193-198` reads `fsh_i[47:40]` and tests it against zero. The independently executed published probe confirms count 256 produces `frames_rx=3 unsupported=2`, while count 257 produces `frames_rx=4 unsupported=2`. The source comment, banner, campaign title and public limitation now agree with that behavior.

Prior public findings

| Finding | Disposition at 87a2b77d | Cause-level evidence |
|---|---|---|
| R673-1-F1, MINOR, Docs/Tests/Conformance | Resolved, retained from round 2 | `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:493-510` states and implements the full current-format compare. That artifact is unchanged this round. |
| R673-1-F2, MINOR, Docs/Tests/Conformance | Resolved as assigned, option (a) | The flat instrument is distinguished from the device listener throughout the assigned source/campaign/record/PR text. The deprecated family reading is not presented as the listener's normative rule. |
| R673-2-F1, MINOR, Docs/Tests/RTL | Resolved by this round | All locations above, equivalent executable behavior, published regeneration receipts and independent 256/257 probe. |
| R674-1-RES1, RESIDUE, Docs | Resolved, remains resolved | Current PR body has zero U+2014 characters. |
| R673-1-S1/S2/S3 and R673-2-S1 | Retained, optional | Detailed below; not assigned, and their underlying code/tests are unchanged. |

Findings and retained suggestions

**R674-3-RES1; RESIDUE; Docs, Tests; `tb/verilator/avtp_rxmon/sim_main.cpp:453`.** Authority/evidence: the inherited trailing comment says “any count matches now” beside an explicit `c.chans=2` stimulus. The corrected banner and actual predicate limit the instrument to a nonzero low byte. Impact: imprecise explanatory prose beside a correctly bounded stimulus; it changes no check, measurement, generated artifact, clause claim or privacy rule. Exact fix: replace the trailing comment with `// this 2-channel probe matches the flat instrument's family filter`. Verification: comment-only diff, identical stimulus and expectations, and the existing low-byte wording remains intact. This is outside the assigned edits and does not leave a lens unclean; carry it to the manager's residue checklist.

**R673-1-S1; SUGGESTION; Tests; `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:522`.** Authority/evidence: FR-STR-03 requires subtype matching; the prior public finding's subtype-term removal survived the N=4 harness. Those artifacts are unchanged. Impact: no engine-level discriminating check for that pre-existing term. Optional required outcome: add a non-AAF subtype case on an AAF input and a matching control. Verification: removing the subtype term fails the named check; clean RTL passes. The earlier mutation was not rerun this round.

**R673-1-S2; SUGGESTION; Tests; `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:521,527`.** Authority/evidence: the engine rejects zero even against a zero current count; the prior removal of the nonzero guard survived the harness. Impact: that boundary lacks a discriminating check. Optional required outcome: test a zero wire count against a zero configured count. Verification: the clean engine rejects, and removing the guard fails the named assertion. Unchanged; prior mutation not rerun.

**R673-1-S3; SUGGESTION; Tests; `tb/verilator/milan_dp/sim_main.cpp:1252-1254,1371,1531`.** Authority/evidence: the shipping shape's eight-channel header retains a 48-byte payload, while the label calls the PDU conformant and an old diagnostic names two channels. The existing comment discloses the header-focused scope. Impact: the case proves header acceptance, not whole-sample-frame geometry. Optional required outcome: use a whole-frame payload or name the check for header acceptance, and correct the diagnostic. Verification: preserve acceptance assertions and check payload geometry and printed description for the selected shape. Unchanged this round.

**R673-2-S1; SUGGESTION; Tests; `tb/verilator/avtp_rxmon/sim_main.cpp:83,459`.** Authority/evidence: `channel_freedom_accepts_every_count()` predates the corrected low-byte description; its existing name remains overbroad. Impact: method-name ambiguity only. Optional required outcome: rename it, for example `flat_family_compare_accepts_other_counts`, at definition and call. Verification: name-only change, same 97 checks and expectations. The manager explicitly did not assign this suggestion.

The added source comments and docstring contain no new bench lane label, lane name, review round, reviewer ID or issue-comment ID (`receipts/comment-rule-scan.txt`). Existing identifiers tracked by #746 are not new residue in this delta.

Independent lens results

[R674] PASS Conformance - `docs/reference/FR_NFR.md:271`, `KL_avtp_rx_monitor_ctx.sv:498-528`, `KL_crf_rx.sv:323-344`, and the correction table above - the shipped current-format rule is unchanged, while the instrument's stated limitation is now exact. The probe is instrument evidence, not a claim that the product must accept a mismatching count.

[R674] PASS RTL - `receipts/round3.diff`, `receipts/delta-check.log`, `KL_avtp_rx_monitor.sv:178-198` - comment-stripped tokens match the previous head. Production context/CRF/datapath files and the reference comparator are byte-identical. No register, state, width, port, parameter, clock/reset or CDC change is introduced. R673-2-F1's RTL-description mismatch is closed.

[R674] PASS Robustness - `receipts/probe-full.log`, `sim_main.cpp:459-483`, unchanged `sim_main_nx.cpp:902-999` - the 256/257 boundary agrees with the corrected limitation, with zero-count rejection and matching/nonmatching flat probes still passing. Previously covered shipped matching/mismatch, 264-versus-8, reconfiguration, rejection/recovery and stopped-input behavior retains its dependencies. No reset, timeout, backpressure or malformed-input path changes.

[R674] PASS Tests - `fuzz_aaf.py:176-200`, `scripts/check_delta.py`, `published/author-r3/receipts/r3-rxmon/` and `r3-tsnfuzz/` - C++ is byte-identical outside the banner. Python AST is identical after explicitly substituting the same five-count tuple and removing only the changed docstring/title. The four assertions per probe and their expectations are unchanged. Existing mutation controls pass in the public exact-head receipt; the independent boundary probe agrees.

[R674] PASS Docs - all four changed files, current PR body, `published/author-r3/receipts/r3-regen/`, `receipts/docs-check.log` - the assigned statements consistently describe the instrument, retain the device rule, and match the generated record. Regeneration provenance is corroborated below. One inherited prose-only residue is recorded without concealing it as a blocking finding.

Public evidence and reviewer execution

The immutable [evidence publication](https://github.com/kebag-logic/milan-fpga/tree/71b87fde5932bca3b1cde4a7c98ae564bcfe316e/review-evidence/765-r1) supplies the author's source-head execution receipts. `fetch_receipts.py` checked all 72 selected files against `MANIFEST.json`'s `published_sha256`; all match. This manifest has no detached signature, and the public commit-verification response says `verified: false`, `reason: unsigned`. Therefore signer authentication is unavailable: this review verifies immutable-publication hash consistency, not a signed packet. It does not infer a manager source bank.

| Evidence | Result and attribution |
|---|---|
| Author `r3-aaf` and `r3-tsnfuzz`, exact 87a2b77d | AAF 164/0 with freshness PASS; combined campaign grader 54/0, AAF 164/0, gPTP 677/0, traceability 2/0. Oracle pin `deca300c9eb4863fa13383b45ba6cb6fd0828671`. These are executed source receipts, not skipped hosted contexts. |
| Author `r3-rxmon`, exact 87a2b77d | Flat 97/0, NX 147/0, lockstep N=1 116/0 and N=8 119/0; mutation controls 14/14 and 6/6. |
| Author `r3-static`, exact 87a2b77d | All 36 table rows rc 0, including documentation and delta checks. |
| Author `r3-regen` | Discloses d4a27e63 plus uncommitted round-3 edits. Record absent from before-status modifications, present afterward; campaign 164/0. Initial make rc 2 is the expected freshness refusal against the old committed title, not a green gate. The emitted record diff equals the final committed diff exactly. Final-head campaign freshness then passes. |
| Author `r3-probe` and reviewer `probe-flat.log` | Same published probe SHA-256 `4598ce131eca8b9c08cbb44163b78e7da1a549c716d074b290c5b9e3f6f24a2a`; identical 256/257 observations. |
| Reviewer `probe-full.log`, `probe-full.rc` | Disposable exact-head archive, compiler identity verified as 5.050, compilation capped at 16 jobs. Full executable exits 0 with 97 checks and zero failures; wrapper asserts both boundary observations. |
| Reviewer delta, evidence, freshness and docs checks | All pass. Freshness is a spot-check against the published execution log and checked-out artifact, not a new AAF campaign. Docs: zero findings, 23/23 scrub controls, 4/4 routing controls. |

The first reviewer wrapper attempt correctly obtained the boundary observations but wrongly expected the full suite summary in the original script's filtered output. `probe-verification-first-attempt.log` preserves that wrapper-only failure. The final wrapper also executes the built binary directly, captures its complete output and exit code, and checks the 97/0 summary. No product or test expectation was weakened. The published probe itself is unchanged.

Reviewer-owned completion ledger

Each row applies this round's delta and carries the unchanged scope from R674-1 and R674-2 at the heads identified above. Affected wording/generated artifacts are re-covered here; no open MINOR is carried as clean.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | FR_NFR:271; compliance matrix:190; ctx:498-528; CRF:323-344; assigned wording/PR | R674-3, carrying unchanged R674-1/R674-2 scope | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |
| RTL | CLEAN | round3.diff; flat monitor:178-198; reference:493-510; unchanged production logic; delta-check.log | R674-3, carrying unchanged R674-1/R674-2 scope | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |
| Robustness | CLEAN | sim_main.cpp:459-483; sim_main_nx.cpp:902-999; probe-full.log; unchanged reset/reject/timeout machinery | R674-3, carrying unchanged R674-1/R674-2 scope | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |
| Tests | CLEAN | fuzz_aaf.py:176-200; C++/AST equivalence; r3-rxmon/r3-tsnfuzz; independent probe; optional S1-S3/S1 retained | R674-3, carrying unchanged R674-1/R674-2 scope | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |
| Docs | CLEAN | all four delta files; TEST_RESULTS:29,96; PR snapshot; r3-regen; docs-check.log; RES1 recorded | R674-3, carrying unchanged R674-1/R674-2 scope | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |

Integrity, reproduction and limits

`verify_tree.py` checked raw bytes and executable/symlink modes against Git blob identities, every stage-zero index entry, and all five populated submodules. It passed for 1,423 superproject blobs. Required gitlinks: protocol-processor `2cbed0a987c1e68402658d69459ab7e5aa571adc`; gptp-processor `e4869fd0c42889b2ac806587cc5c78afb1c33461`; verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`; tsn-c-stack `70936b77dc41981e192438388cd0aced69954f18`. Optional lwSRP was also verified; optional external remains uninitialized with its tree/index gitlink intact. Original tracked source bytes were never edited, so no restoration was needed. All disposable builds are under this packet's `scratch/`.

Portable reproduction, from the candidate clone: `python3 <packet>/scripts/check_delta.py .`; `python3 <packet>/scripts/audit_evidence.py .`; `python3 <packet>/scripts/verify_tree.py .`; `python3 <packet>/scripts/run_probe.py . <pinned-compiler>`. The probe wrapper verifies compiler version and caps build workers at 16. `fetch_receipts.py .` retrieves the same selected public objects if the publication commit is available locally. `MANIFEST.sha256` lists publishable files with paths relative to the packet; `scratch/` is excluded.

No full parent/processor/gPTP/synthesis/builder bank, route, hardware operation, local workflow replica, source fix, commit, push, GitHub write, merge or author contact was performed. This round does not rerun prior broad banks. Physical calibration remains NOT RUN; field skips and simulation are not hardware proof. Existing limits remain: input formats above zero supplied through LCTX, the pruned short-frame depacketizer limitation, and samples_per_frame having no comparable PDU field. Full-ten-bit behavior of the flat instrument remains outside the assignment.

Pending manager duties: accept hosted/local-workflow evidence while distinguishing executed jobs from skipped contexts; finish the other independent review; carry RES1 and optional suggestions appropriately; construct and validate the final current-dev merge candidate with builder/native banks and publish its receipts; obtain merge authorization and perform post-merge containment before closing the issue. Source base `4191b098`, reviewed source head `87a2b77d`, and that candidate are distinct. The supplied live-dev tip is `78ca9bdf104819265588726bce4322696c38b8c2`; the merge turn must use the then-current tip. There is no manager source bank at this exact head, and none is claimed or inferred here. This source verdict does not clear those remaining duties.

R674-3 FINISHED
