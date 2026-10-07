[R533] NEGATIVE - exact head cce554f64f6bdab1f6d26e5c4d7b46d54d228c52

Round R533-6, external independent delta review of issue #665 / PR #690. The receive-recovery MAJOR is resolved. One new MINOR remains in the published executable reproduction instructions, leaving Tests and Docs unclean. One publication-tense RESIDUE remains. No production correctness defect was found in this round.

Reviewed tree: `c27f9958d4f5a2f86e9cfcb34316d00213e6d28d`. Full context: `db9aa8c9b135b34ff3d070a979dee70440b37cc6..cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`; focused delta: `500b8f64..cce554f6`. Merge `069874955e9c1061872d47afc3b7e57fc24e19bd` has assigned dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df` as its second parent.

I reconstructed the repository contract, documentation index, frozen issue scope and public decisions, requirements and interfaces, then reviewed the source delta before consulting prior public findings. Authorities include issue comments 5992455815, 6008744385, 6009661573, 6030279477, 6030870481 and 6038730087; REQUIREMENTS section 1; NFR-SCOUT-03/H-SRP; the mailbox contract; the pinned dependency API; IEEE 802.1Q-2018 Tables 10-3/10-4, 10.7.11 and 35.1.2.2; and Milan v1.2 4.2.7, 4.3.2 and 5.5.2.7. Standard digests are in `receipts/standards.json`; their text is not published.

Public author evidence was read from the supplied initial archive and round-6 author packet at evidence commit `0ba22f6e8ad692a830a3f68d18d3c650601ecd3c`. The latter publishes HANDOFF.md and PR-BODY.md, not the auxiliary ROUND6 receipt files those summaries name. Author summaries are distinguished from independently executed receipts below. No private author material, management checkout, or parallel round-6 review was consumed.

**R533-6-F1 | MINOR | Tests, Docs | Published mailbox reproduction command aborts before validation**

Artifact: live PR #690 body, “How to validate,” line 127 in `receipts/pr-body.txt`; the same command in public `author-r6/PR-BODY.md`. Evidence: `receipts/public-recipe-reproduction.json` and `public-mailbox-export-failure.log`.

Authority/evidence: CONTRIBUTING's reproducible verification bar and AGENTS sections 4/6 require executable evidence another cold reviewer can reconstruct. The prescribed `git archive ... HEAD ... scripts/mutant_run.py` exits 128: `fatal: pathspec 'scripts/mutant_run.py' did not match any files`. That path is absent from this exact tree. This was reproduced directly, before compilation. Removing this nonexistent input allows the tracked export and both bus controls to pass. The recipe also refers to `$PACKET/round6-helpers/hdl-j8`; that helper is absent from the published round-6 packet.

Impact: the documented clean-checkout route cannot reach the mailbox validation it is offered to reproduce. This does not invalidate the independently passing firmware or bus results. It is not wording-only RESIDUE: the defective text is an executable validation recipe, and its actual failure is the evidence.

Required outcome: publish a runnable exact-head mailbox recipe. Remove the nonexistent archive member, and publish the referenced helper or replace it with a complete bounded invocation using the configured compiler. Preserve the concurrency cap. No production-source change is requested.

Verification: execute the corrected public instructions from a fresh tracked export, with only documented prerequisites, retaining export and gate exits. `scripts/reproduce_public_recipe.py` reproduces the failure; `scripts/mailbox.py` supplies the successful focused bus control. The manager must validate the complete advertised mailbox gate after correcting its public recipe.

**R533-6-R1 | RESIDUE | Docs | Published PR still describes this head as unpushed**

Artifact: PR body lines 17, 20, 22 and 73 in `receipts/pr-body.txt`. This retains R532-5-R1 / R532-2-R2. The live API and remote branch identify cce554f6, while the body says “REVIEW READY locally,” “The candidate is unpushed,” that the PR contains Round 5, and “After publication.”

Authority/evidence: assignment 6038730087 explicitly carries the publication residue; `receipts/hosted.json` records the published head. Impact: stale publication status only; no measurement, test, code, conformance claim or verdict changes.

Exact fix: state “Round 6 REVIEW READY at published head `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`; fresh independent review is in progress.” Delete “The candidate is unpushed” and the sentence saying the PR contains Round 5. Retain the historical statement that both Round 5 reviews were negative. Replace “After publication, set” with “Set”. Verification: compare the live body with the live head. Historical author handoff statements need not be rewritten as though authored after publication.

[R533] PASS Conformance - `sw/firmware/ctrl/srp/srp_mbx.c:355`, `:379`, `:649`; `third_party/lwSRP/src/include/shish_lan/mrp.h:272`, `:360`; `srp_walk.cpp`; recovery/timing receipts - The adapter honors recoverable receive refusal: complete owned record, original interface/arrival, identical-payload retry, separate refusal accounting and one successful completion count. Rapid-leave, #608 deadline, MVRP scope, startup declarations and selected processor-wire cases pass. The unchanged independent withdrawal probe completes without peer retransmission at IF=1/2.

[R533] PASS RTL - `ctrl_app_srp.c:8`, `ctrl_app.c:36`, `ctrl_loop.c:110`, `srp_mbx.c:574`, `:622`; `merge-resolution.diff`, `source-checks.json`, `mailbox.log` - Checked static ownership, bounded dispatch, ordered RX gating, lifecycle reset and attach refusal. ADP timer slots start at zero; MAAP starts at MBX_N_IF; SRP uses centisecond fan-out. Composition preserves all three RX enables, events and ticks. Refusal preserves ADP/MAAP. All three actual merge conflicts retain both sides semantically. Imported MAAP sources/tests, ctrl_app.c, ctrl_build.py and mailbox Makefile match F2 blobs. HDL delta against assigned dev is empty; older HDL changes in FC-to-head belong to imported dev history. Both bus controls pass.

[R533] PASS Robustness - `srp_rx_retry.cpp:25`, `:58`, `:80`, `:104`, `:122`, `:141`, `:154`, `:172`, `:195`, `:213`, `:240`; `srp_mbx.c:266`, `:291`, `:577` - Mixed/partial payloads retain later attributes; repeated refusal preserves bytes/time. Later records and binds cannot overtake retained input. Destroy cancels it; reset cancels only its interface and fences its published prefix. Other-interface reset preserves it. Recreation failure, MVRP participant selection, owed TX, tick/lifecycle backlog, invalid suffix and future-version cases pass. Existing lifecycle/shared-binding regressions pass at both counts.

Tests was applied to observables, mutation grading, coverage/exclusions, wire differential, composition and public reproduction. Behavioral and coverage checks pass; F1 leaves Tests unclean. Docs was applied to API/README commitments, pin/licensing inventory, merge claims, public scope, author summaries, PR instructions and timing/size limits. Production-adaptation and timer-removal corrections agree with source. F1 leaves Docs unclean; R1 does not.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | mrp.h; srp_mbx.c; cited clauses; independent controls; srp_walk.cpp; timing/size receipts | R533-6 | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |
| RTL | CLEAN | ctrl_app.c/ctrl_app_srp.c; ctrl_loop.c; mailbox contract; srp_mbx.c; F2 blob/remerge checks; bus receipts | R533-6 | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |
| Robustness | CLEAN | srp_rx_retry.cpp; srp_mbx.cpp; srp_debug.cpp; lifecycle/order/refusal and retry-removal probes | R533-6 | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |
| Tests | UNCLEAN, F1 | 90-plant campaign; IF=1/2 suites; coverage; dependency note reversals; broken public mailbox recipe | R533-6, applied | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |
| Docs | UNCLEAN, F1; R1 is RESIDUE | SRP/firmware/test READMEs; dependency inventory; assignment; author packet; live PR body and recipe receipts | R533-6, applied | cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 |

**Independent executable evidence**

All receipt paths below are relative to `receipts/`.

| Check | Result | Receipt |
|---|---|---|
| Unchanged R533-5 independent.cpp | Four cases pass per IF count; withdrawal active=0, received=2, malformed=0, stops=1 | `control-if1.log`, `control-if2.log`, `probes.json` |
| Reviewer retry-removal plant | Compiles; withdrawal active-state assertion fails at IF=1/2; each binary exits 1 | `retry-removed-if1.log`, `retry-removed-if2.log`, `retry-plant.json` |
| SRP suites, each IF count | 53 adapter, 11 recovery, 2 composition, 5 differential, 5 timing and 3 debug cases pass | `suites.log`, `suites.rc` |
| Preserved MAAP tests | 37 core; 12 one-interface and 13 two-interface mailbox cases pass | `suites.log` |
| Entire SRP campaign | All 90 named plants detected; compile failures do not count | `campaign.log`, `campaign.rc`, `campaign/` |
| Coverage | 19 files at 100% lines/branches after unchanged exclusions; SRP 459/459 lines, 432/432 branches; composition 10/10, 6/6 | `coverage.log`, `coverage.rc`, `source-checks.json` |
| Dependency profiles | 87 tests each; OFF 19901 assertions, ON 19889; three scenarios/ten steps each | `upstream-OFF.log`, `upstream-ON.log` |
| Table 10-3 notes 4/5 | Three unchanged reversals killed in each profile after successful builds; restored controls pass | `note-reversals-OFF.log`, `note-reversals-ON.log`, `notes-OFF/`, `notes-ON/` |
| Linked composition/base | Four head and four FC-base links; head figures exactly match public handoff | `sizes.json`, `sizes.log`, section/symbol receipts |
| Mailbox buses | 316 Wishbone, 361 AXI4-Lite checks; zero failures; scoped 5.050 identity verified before use | `mailbox.log`, `mailbox.rc` |
| Focused static/documentation | Generator, submodule docs, C++/Python idiom and diff whitespace checks pass | `static.json`, `static-*.log` |
| Source integrity | Raw blobs/modes/indexes match for parent and four required submodules | `integrity.log`, `integrity.rc` |

The dependency production `src/` diff from a4cbe41d to 9197193e is empty. PR #15's two note tests and three reversal mappings are in the pinned public tree. The initial upstream collector exited 1 after successful unit/behavior runs because the reviewer driver misspelled a reversal selector. That setup failure is retained, not counted as a passing invocation; corrected separate note runs provide the final reversal evidence. The public mailbox export failure is likewise separate from the successful focused bus invocation.

The following measurements use the same pinned compiler and 57 hash-verified public runtime inputs. Initialized data is zero throughout. The arena is already in BSS. All spans include alignment and an 8192-byte stack reservation, which is not a whole-call-chain proof.

| Shape / IF | text | rodata | BSS | arena within BSS | head span | FC-base span | increase |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1 / 1 | 33440 | 2846 | 18072 | 9920 | 62560 | 18752 | 43808 |
| 1x1 / 2 | 34676 | 2846 | 29424 | 19840 | 75152 | 19248 | 55904 |
| 8x8 / 1 | 33380 | 2846 | 32824 | 24032 | 77264 | 18752 | 58512 |
| 8x8 / 2 | 34628 | 2846 | 58928 | 48064 | 104608 | 19248 | 85360 |

Required ADP, MAAP, SRP, bind, RX/TX and storage symbols survive the link. The fixture has no board reset entry or connected fabric licence output. The FC comparison includes F2; it is not an SRP-only area claim.

**Prior public findings at this head**

| Prior finding | Reviewer disposition and current evidence |
|---|---|
| R533-5-F1 / R532-5-F1, lost refused Leave | RESOLVED under assignment 6038730087. Full retention/retry and refusal accounting; unchanged probe passes without retransmission at IF=1/2; retry removal fails; all recovery cases/plants pass. |
| R533-1-F1 / R532-1-F1, Milan rapid Leave | RESOLVED, retained. MSRP-only override, immediate Listener/Talker, MVRP scope and original #608 deadline checks pass. Exhaustion adaptation is now resolved above. |
| R533-1-F2 / R532-2-F1, lifecycle/link recovery | RESOLVED, retained. Attach/poll level, adjacent edges, stale fences, cancelled DOWN and reattach cases pass; plants detected. |
| R533-1-F3 / R533-2-F1, shared StreamID/rebind | RESOLVED, retained. Aggregate declarations, inherited state, both orders and consecutive replacement pass; plants detected. |
| R533-1-F4, linked size | RESOLVED. Four exact head links and FC comparisons reproduced with reachable composition and separate sections. |
| R532-1-F2 parts 1/2, admission and ReadyFailed | RESOLVED, retained. Boundary and strict callback cases pass; overhead/ceiling/callback plants detected. |
| R532-1-F2 part 3 / R533-2-F2, notes 4/5 | RESOLVED. Public pin contains tests; suites and three reversals executed in both profiles. |
| R532-2-F2, dependency inventory/diagram | SOURCE RESOLVED, retained. Pin/ownership inventory and submodule gate pass; hosted acceptance is separate. |
| R532-2-F3, final never-eligible shared VID | RESOLVED, retained. Both unbind orders pass; last-ineligible-vid-leaks detected. |
| R532-2-F4, lifecycle/shared-VLAN gaps | RESOLVED, retained. reset-keeps-owed-domain, reset-keeps-sink-vlan and shared-ready-uses-first-vlan detected. |
| R532-3-F1, inheritance gaps | RESOLVED, retained. Cross-slot/cross-StreamID cases pass; joining-binding-loses-applicant and applicant-inherited-across-streams detected. |
| R532-3-F2, final-unbind Domain VID | RESOLVED, retained. Both Domain VIDs tested; final-unbind-withdraws-domain-vid detected; README states exception. |
| R532-1-S1, LeaveAll scope | ADDRESSED, retained. Upstream per-type/per-port case and selected Run-B differential pass. |
| R532-1-S2, duplicate generic LV Join | RESOLVED, retained. Ordinary LV rows have no indication; changed-value handling remains; independent changed-LV probe passes. |
| R532-1-S3, participant recreation | ADDRESSED, retained. Partial allocation releases both participants; retry and surviving interface verified. |
| R532-2-S1, Milan option affecting MVRP | ADDRESSED, retained. Scope case passes at IF=1/2; scope plant detected. |
| R532-1-R1, TICK units | RESOLVED, retained. Centiseconds distinguished from NOW_MS milliseconds. |
| R532-1-R2, size limitation | SUPERSEDED/RESOLVED. Actual linked evidence exists; obsolete object-only limitation not restored. |
| R532-2-R1, fetch wording | RESOLVED. Anonymous exact-pin HTTPS checkout succeeds; docs identify public main. |
| R532-3-R1, STOP/compiler-absent status | RESOLVED, retained. STOP wording gone; source validation and candidate duties separate. |
| R532-2-R2 / R532-5-R1, publication tense | RETAINED as R533-6-R1 RESIDUE with current exact fix. |
| R532-5-R2, local Applicant merge wording | RESOLVED. SRP README records merged public PR #15 and pin 9197193e. |
| R532-5-S1, stale timer-removal claim | ADDRESSED. Harness README corrected; destruction/recreation/reset checks pass. |
| R532-5-S2, adapter wire cases | ADDRESSED. Future-version and atomic-invalid cases pass; named plants detect acceptance/counting defects. |

**Limits and pending manager duties**

The timing envelope charges 100 ns per mailbox access, one aggregate 1 ms CPU/preemption allowance and 100 ns uncertainty. Storage recovery retains the original arrival: one-millisecond recovery reports 1.9831 ms / 1.9784 ms including the envelope; eleven-millisecond storage exhaustion fails the budget predicate. Retry grants no new allowance. Permanent exhaustion cannot satisfy a finite service deadline. These are conditional host results, not target-cycle or wire-departure measurements.

The full parent, processor, gPTP, synthesis and builder banks were not run. The manager's reported source-bank passes are separate evidence, not executions claimed here. This round ran focused bus controls, not the complete mailbox mutation/cosimulation bank. The selected SRP processor stimulus is a firmware differential, not full processor-suite execution. No shared installation, source fix, commit, push, GitHub write, merge, container runner, privileged operation or hardware access was performed.

The exact-head hosted snapshot records successful executed firmware-unit, bdd-conformance, wire-accountability, docs-check-no-git, lint, four synthesis shards and one simulation shard. Several jobs were in progress; aggregate completion is not claimed. Physical gPTP was skipped. Hosted acceptance and local replication remain manager-owned. Physical calibration was NOT RUN; field skips are not hardware proof.

The manager must correct and verify F1's public recipe, carry R1 to the residue checklist, obtain clean completion of Tests/Docs and the other independent review, and complete hosted/local gate acceptance. Then construct and validate the final candidate against live dev at the merge turn. This review is source-head evidence, not candidate validation. Explicit maintainer authorization, post-merge containment, issue/project closure, live MAAP/stream updates, F3 binding calls, fabric licence wiring and target release evidence remain separate duties. No merge approval is granted.

All mutations/build products stayed under packet scratch. Final verification covers 1185 parent blobs and 936 dependency blobs, their modes and complete indexes, required gitlinks, and absence of hidden index flags/untracked files. Optional external remains uninitialized with unchanged gitlink. Publish only this report and files in MANIFEST.sha256; scratch is never publishable. Portable scripts and normalized raw receipts retain command/exit details and original-byte provenance.

R533-6 FINISHED
