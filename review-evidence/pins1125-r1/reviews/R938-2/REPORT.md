[R938] NEGATIVE - exact head e5d8a71b6fa90352eca72314c7bd2275a1b20285

R938-2, external independent delta review of issue #1013 / PR #1016. All five lenses applied. The prior functional test findings are resolved: the revised checks detect an absent pair, an absent Follow_Up and a stale bank. Two stale expected-result statements remain MINOR under Tests and Docs. One additional wording residue is recorded. No production implementation defect was demonstrated.

Reviewed tree: `490a2f2ac0734ccb7be0db84be3b3452e9bfccb5`. Full diff base: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`. Delta: `a6864a49293ba3d0df37029abfa581468ef78dce..e5d8a71b6fa90352eca72314c7bd2275a1b20285`, one commit, nine files. The independent delta pass preceded examination of prior public findings. Unchanged production code retains its earlier coverage after the continuity checks below.

Authorities examined: `AGENTS.md` sections 6-7; `CONTRIBUTING.md` sections 2-3 and 6; `docs/README.md`; issue #1013 and its [public pin ruling](https://github.com/kebag-logic/milan-fpga/issues/1013#issuecomment-7178757153); `REQUIREMENTS.md` REQ-PTP-05/06/07; `docs/design/GPTP_PLANE.md` ownership and link-delay sections; the pinned engine's `docs/INTEGRATION.md`; `docs/reference/REGISTER_MAP.md:2132`; and `docs/integration/BUILDING.md:614`. The adopted contracts cite IEEE 802.1AS-2011 11.2.2 b), Figure 11-8 and 11.2.13.2.1 f), Milan v1.2 4.2.6.2.7, and IEEE 1722.1-2021 6.2.2.6/6.2.7.1.3. No new clause interpretation is introduced by this delta.

**Findings**

[R938] R938-2-F1 MINOR Tests, Docs - PR #1016, “How to validate”, saved as `receipts/pr-body.md:193` - The reproduction instruction still predicts the previous failure count.

Authority/evidence: the instruction says that the old generator produces `15 FAIL` in the shadow suite. The current published receipt, `receipts/published-old-generator-red.log`, completes with `490 checks: 465 PASS, 25 FAIL`. The PR's regression table and the round-2 review-ready record correctly report 25. The delta adds freshness checks that now fail for ignored pairs, so the old expectation no longer applies.

Impact: the same exact-head experiment has contradictory expected results in the review object. A reproducer cannot satisfy both. This is a numerical test-result claim, not wording-only residue.

Required outcome: change the shadow expectation in that instruction from `15 FAIL` to `25 FAIL`, or describe the named failures without a stale total. Keep the direct-engine expectation at 32 and the executed datapath comparison at 3 of 242; the old-generator latency leg remains unexecuted.

Verification: compare the revised instruction, regression table and published completed tallies. No new simulation is needed for this correction.

[R938] R938-2-F2 MINOR Tests, Docs - `tb/verilator/gptp_shadow/sim_main.cpp:2985` - The tolerance comment still specifies a zero expected offset.

Authority/evidence: the comment describes the graded pair's “expected 0”. The changed assertion at line 3052 instead requires `before - kGradedOffsetNs`, where `kGradedOffsetNs` is 400. Independent clean observations are approximately -400 ns, not zero: the first trial is `before=1, after=-400`, and the -263 ns trial is `before=-12, after=-408` (`receipts/clean.log`). The delta changed the test contract that this adjacent comment describes.

Impact: the source explanation and executable expectation disagree about the central repair. Treating this as a harmless stylistic edit would leave an incorrect numerical test-contract statement in place; it is therefore MINOR under the supplied conservative classification rule.

Required outcome: replace the three-line tolerance comment with an accurate description, for example: “Maximum error from the previous offset less kGradedOffsetNs; the ingress stamps quantise to the 8 ns tick.” Remove the obsolete nearest-wrong-value sentence. Change no assertion or tolerance to match the stale comment.

Verification: the comment describes the expression at line 3052 and agrees with the clean offset receipt. Existing probe results remain applicable if only the comment changes.

[R938] R938-2-R1 RESIDUE Docs - PR #1016 status and limitations, saved as `receipts/pr-body.md:25` and `:202` - Two scope summaries omit the round-2 harness changes.

Authority/evidence: these sentences say only the gitlink and pin records changed after the earlier measurements. Elsewhere the same body correctly lists the new harness assertions, controls and lifecycle changes. The complete delta confirms those additions, and `receipts/evidence-audit.log` independently proves that image inputs remain identical.

Impact: wording inconsistency only. The accurate image-input continuity, measurement results and coverage statements do not need changing.

Exact required outcome: replace “Only the gitlink and the records naming the pin changed after them” with “Later changes also update consumer harnesses and controls; image inputs remain unchanged.” In the limitations paragraph, replace its final sentence with “Later changes move the gPTP pin from 3009f9a2 to 3ce71b76 with identical hdl/ and syn/ trees, update pin records, and revise consumer harnesses and controls.”

Verification: both summaries agree with the commit's changed-file list and the existing image-input proof. This residue does not leave a lens unclean.

**Disposition of every prior finding**

| Prior finding | Disposition at this head | Evidence |
|---|---|---|
| R937-1 F1; R938-1 F1: unused pair / stale offset passes | RESOLVED | Lines 3046-3052 compare before/after offsets and require the attributable -400 ns change. Independent stale-bank, omitted-pair and omitted-Follow_Up probes fail both named checks at every negative trial. The published previous-generator run now fails both at -81 ns. |
| R937-1 F2: phase 6 credited with public-bank coverage | RESOLVED | `docs/design/GPTP_PLANE.md:160` names asCapable and the used delay for phase 6, and assigns public-word coverage to the shadow/datapath suites. Compared with the actual `if (kept)` engine-publication check and shadow public-bank checks. |
| R938-1 F2: unexecuted old-generator datapath comparison claimed | RESOLVED | The new published receipt completes the `gptp` leg with 239 PASS / 3 FAIL, naming -81, -263 and -5,000,000 ns asCapable checks. The PR expressly excludes `gptp-lat` from that experiment. The separate stale shadow total is new F1 above. |
| R938-1 F3: route equality beyond available pairs | RESOLVED | `docs/reference/SUBMODULES.md:1133`, `CHANGELOG.md:82`, the current PR body and round-2 review-ready record restrict equality to paired measurements. All four corners and utilization match for the three pairs. The extra head directive is explicitly unpaired. |
| R938-1 R1; R937-1 R1: split phase table | RESOLVED | `tb/verilator/gptp_plane/README.md:24` is contiguous with rows 1-5; the intervening blank line is gone. |
| R937-1 R2: unclear “then” antecedent | RESOLVED | `docs/design/GPTP_PLANE.md:150` now explicitly states signed use before explaining cancellation. |
| R937-1 R3: duplicated role prefix | RESOLVED | Current PR body starts with one role-prefix line. |
| R937-1 S1: prediction labelled as observation | ADDRESSED | `tb/verilator/milan_dp/sim_gptp.cpp:1705` now says “harness precondition”; the expression and product assertions are unchanged. |

The immutable round-1 packet remains a historical record. Its earlier overstatements are superseded by the corrected round-2 record; no historical execution was silently reattributed to this head.

**Independent controls and receipts**

`probe.py` creates four disposable registered clones beneath this packet's `scratch/`. Each builds with four compilation workers; all four run concurrently under one joined foreground supervisor. The scoped executable's identity was checked before execution. The only addition to the clean harness is an offset diagnostic print. Neither production behavior nor assertions are changed in that control.

| Arm | Completed suite result | What it establishes |
|---|---|---|
| Clean | 490 PASS, 0 FAIL; rc 0 | The repaired assertions pass. Offset deltas across the seven accepted trials are -401, -396, -394, -396, -396, -396 and -395 ns. |
| `unsent-pair` | 476 PASS, 14 FAIL; build/run rc 2 | Removing only the graded pair breaks freshness and expected-offset checks for all seven accepted trials. |
| `stale-bank` | 469 PASS, 21 FAIL; build/run rc 2 | Holding the bank's offset breaks both new checks for all seven accepted trials; unrelated offset checks also fail. |
| `unsent-follow-up` | 476 PASS, 14 FAIL; build/run rc 2 | Keeping each graded Sync while suppressing only its Follow_Up still breaks both checks. A Sync arrival alone cannot satisfy them. |

The nonzero control statuses accompany completed simulation tallies, not compilation failures. Each negative-delay trial, including -263 ns, fails the two intended checks. The no-step assertion remains a separate safety check; it is not used as evidence of consumption. The published `public_bank_keeps_a_stale_offset` and `graded_follow_up_not_sent` controls are also caught by their exact designated freshness name (`receipts/published-gptp_shadow.log`).

`receipts/probe-summary.txt`, the four arm logs and return-code files retain these observations. `audit.py` verifies raw tracked bytes, modes, index entries and initialized submodule commits without relying on status flags. Both the original clone and all four restored probe clones pass. The source clone has all five initialized gitlinks intact; `external` remains intentionally uninitialized. Probe clones initialize the two inputs their focused build consumes; all remaining gitlink index entries are still exact. No process remains running.

Reproduction: place `probe.py` and `audit.py` in a fresh output directory. Run `python3 probe.py <exact-head-clone> <scoped-executable>`, then `python3 audit.py <exact-head-clone> evidence` and `python3 audit.py <exact-head-clone> integrity`. The evidence audit requires the published evidence commit in that clone. Run `audit.py <scratch-arm> probe-integrity` for each restored arm. No shared installation or production source edit is required.

**Artifact-specific lens results and reviewer-owned ledger**

[R938] PASS Conformance - issue #1013's pin ruling; `docs/design/GPTP_PLANE.md:133`; `gptp-processor/hdl/ucode/gen_gptp_ucode.py:2238`; `third_party/tsn-c-stack/src/adp.c:301` - The frozen pin behavior remains unchanged: negative delays are accepted, signed use is floored at -800 ns, and only the public bank clamps to zero. The ADP fixed-prefix acceptance and 128-octet mailbox limit are unaffected. The revised test documents distinguish engine and public-bank observations. Selected routes retain the governing margins.

[R938] PASS RTL - exact delta file list; `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:745`; `receipts/evidence-audit.log` - No production RTL, firmware, configuration, constraint, ROM-ledger or gitlink changes occur in this round. The publication bank still samples one committed generation. The new stale-bank mutation targets the offset assignment only in disposable copies. Existing clock, reset, CDC and consumer contracts retain their prior coverage.

[R938] PASS Robustness - `tb/verilator/gptp_shadow/sim_main.cpp:3025`; `mutants.py:224`; four independent arm receipts - Applied stale-data and absent-event checks to the delta, including Follow_Up loss with Sync preserved. The clean suite retains asCapable/public-clamp checks, no-step checks and +800/+801 behavior. No unchanged malformed-input, reset or transport campaign was rerun merely to bank another round.

[R938] Tests applied, UNCLEAN - `sim_main.cpp:3046`, `mutants.py:224`, lifecycle count updates, published source-head receipts and PR reproduction instructions - The repaired behavior is falsifiable and both new controls are effective. F1/F2 remain incorrect expected-result descriptions.

[R938] Docs applied, UNCLEAN - `GPTP_PLANE.md:160`, `SUBMODULES.md:1133`, both suite READMEs, `CHANGELOG.md:82`, source comments and the current PR body - Prior coverage and route overclaims are corrected. No newly added review identity, review-round label or issue-comment ID was found in source comments. F1/F2 remain; R1 is wording-only residue.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Public scope ruling; signed-delay and ADP contracts; unchanged pins; paired route receipts | R938-2, retaining unchanged R938-1 coverage | e5d8a71b6fa90352eca72314c7bd2275a1b20285 |
| RTL | CLEAN | Delta file list; public-bank commit logic; raw image-input tree identities | R938-2, retaining unchanged R938-1 coverage | e5d8a71b6fa90352eca72314c7bd2275a1b20285 |
| Robustness | CLEAN | Phase 22 and independent stale-bank / pair-loss / Follow_Up-loss controls | R938-2 | e5d8a71b6fa90352eca72314c7bd2275a1b20285 |
| Tests | UNCLEAN | New assertions, mutations, lifecycle changes, source comment and PR expectations; F1/F2 | R938-2 applied; no clean covering round | e5d8a71b6fa90352eca72314c7bd2275a1b20285 |
| Docs | UNCLEAN | Changed documentation, published evidence and current PR body; F1/F2 | R938-2 applied; no clean covering round | e5d8a71b6fa90352eca72314c7bd2275a1b20285 |

**Evidence limits and pending manager duties**

The public evidence source is commit `4b3b21e2104d37db96040622edfe75a5acbf2a76`, under `review-evidence/pins1125-r1/author` and `review-evidence/pins1125-r2/author`. All 81 round-1 author files and all 14 round-2 author files match their published SHA-256 manifests. The commit is unsigned (`%G? = N`), and these packet paths provide no detached signature. Accordingly this review verifies content identity, not a cryptographic signer.

Published source-head receipts report 102 direct-engine checks, eight phase-step campaign arms, nine link-delay campaign arms, 490 shadow checks with 16 caught controls and lifecycle PASS, and 242 checks for each datapath leg. They are author evidence; only the focused four-arm experiment above was independently executed in this round. Documentation-step receipts record 56 passes, 24 skips and three SDK-provenance installation refusals. They are not an unconditional complete-workflow pass.

The round-1 firmware, boundary, transport, ledger and route receipts remain earlier-image evidence. Both pins are unchanged at this head: gPTP `3ce71b768a2f6f6a5274c127080146e755d02275`, stack `a795471c0abc4e38f7e5146b4e539dd607b6f501`. The excluded later donor revision has identical `hdl/` and `syn/` tree IDs. No image input changes in this delta, and both budgets are unchanged. The egress ledger's passing non-regression verdict does not turn its underlying pre-existing service-budget failures into passes.

Three route pairs match across all four corners and reported utilization. The selected 1x1 result has worst setup/hold +0.178/+0.021 ns; selected 8x8 has +0.283/+0.036 ns. Both satisfy the governing +0.030 ns setup and nonnegative hold floors. The first 8x8 directive misses the setup floor on both sides. The extra head directive has no base pair. Matching figures do not prove identical placements.

No manager source bank ran at this head, and none is claimed. Hosted execution and local workflow-replica acceptance remain manager-owned; this round did not inspect or certify them. Physical calibration is NOT RUN. Field skips and physical-path simulations are not hardware proof.

The manager must obtain the F1/F2 corrections and re-cover Tests/Docs, carry R1 to the residue checklist, finish both independent review verdicts, and settle hosted/local workflow acceptance. At the merge turn, build and validate the current-dev candidate with the builder and native banks: source base `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`, supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, refreshed then. Source-head receipts do not validate that future merge tree. Merge authorization, post-merge containment and issue/project completion remain separate duties. This session made no GitHub writes, commits, pushes or source fixes.

R938-2 FINISHED
