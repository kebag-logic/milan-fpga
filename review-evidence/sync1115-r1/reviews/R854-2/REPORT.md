[R854] NEGATIVE - exact head e2be92b0e0f9a8f0529dea252f23ed44a21e050a

R854-2, independent external delta review of issue #665 / PR #934. Tree: `54c1e870df27971db88de7ad664a0078ca2cf9cf`.

All five lenses were applied. One MAJOR remains: recorded ownership is not used in two branches of generic MRP timer grading. The LeaveAll overlap repair and the empty-build callback repair work. Conformance, Robustness and Tests remain UNCLEAN; RTL and Docs are CLEAN within this delta. This is a grader defect, not evidence of a product transmission defect.

## R854-2-F1: another participant still hides an owned expiry's missing or late build

- **Severity:** MAJOR.
- **All attributable lenses:** Conformance, Robustness, Tests.
- **Artifacts:** `tb/verilator/ctrl_service_budget/mrpdu_grade.py:214` (missing build), `:239` (build with frames), `:157` (`begin`), `:327` (non-LeaveAll rows); `selftest_leaveall.py:244` (empty-build controls).
- **Authority:** [issue #665 Q1](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6930885185) measures from the participant's transmit opportunity. [R854-001's required outcome](https://github.com/kebag-logic/milan-fpga/pull/934#issuecomment-6932841237) requires independent ownership used consistently for opportunity, missing/late output and service checks. This round explicitly includes periodic ownership. The 49 ms bound remains unchanged.

The expiry has a valid recorded owner, but `resolve()` only uses that fact to reject unowned records. `built()` uses the owner's `anchor()` only when a build sends no frames. Two other branches still derive timing from unrelated participants:

| Probe, with owner `if0 MSRP` | Expected | Actual at this head |
|---|---|---|
| Last owner send 1000 ms; periodic expiry 1300.001 ms; no later build; log ends 1400.020 ms | Absent: more than 49 ms after the owner's opportunity | Absent without a peer; adding MVRP's 1250 ms send changes it to unresolved, with no failure |
| Same owned expiry; first build 1430.980 ms, 130.979 ms after the owner's opportunity | Late, whether it sends nothing or only another participant's frame | Empty build fails; emitting only MVRP on the other interface at 1431 ms changes it to released, with no failure and a 1.000 ms periodic row on the other interface |

In the first case, lines 214-216 select the latest opportunity across every participant. MVRP's join timer postpones that horizon to 1430 ms although MSRP's opportunity is already 1300.001 ms. In the second, lines 239-242 select the participant from the first future frame. `begin()` and the non-LeaveAll row then use that frame's participant too. Thus an empty late build can become timely solely by emitting unrelated output.

**Reproducer:** `python3 -B probe_missing_build.py <checkout>`, expected exit **1 at this head**. `probe_missing_build.log` records both escapes for each application on each interface: four hidden missing builds and four hidden late builds. Four no-peer absence controls, four genuinely short-log controls, and four empty late-build controls behave correctly. No tracked source is changed.

**Impact:** a real CPU service delay or missing build can pass the timer gate even though the expiry's owner is known. A service row may be credited to the wrong interface. This is the remaining owner-association cause from the prior finding, not an unrelated firmware issue. The author also discloses the retained no-build horizon in [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6942387001); disclosure does not satisfy the required owner binding. The frame-bearing escape additionally demonstrates the gap beyond truncated-log classification.

**Required outcome:** use each recorded owner's transmit opportunity consistently to judge missing and late service. Another participant's callback, running join timer or emitted frame must not defer that expiry's deadline or satisfy its service row. Keep correct handling of legitimate empty builds, owed-frame retries, genuinely short logs and the owner's own running join timer. Keep 49 ms unchanged. Align the explanatory text with the repaired rules.

**Verification:** both probe variants must fail by the actual owner and its original opportunity for all four application/interface combinations. The short-log controls must remain unresolved. Add standing controls and a mutation restoring each residual association. Re-run the focused ownership controls, existing mutations and affected published regrades.

No additional MINOR, RESIDUE or SUGGESTION is reported. New source comments contain no prohibited lane labels, review identities, review-round labels or issue-comment IDs.

## Prior findings: disposition at this head

The independent verdict and five-lens ledger were written before reading the prior public review reports. Those reports were then reconciled at their causes; no concurrent round-2 report was read.

| Prior finding | Disposition and evidence |
|---|---|
| R854-001, MAJOR, Conformance/Robustness/Tests/Docs | The demonstrated LeaveAll swap and its documentation overclaim are fixed. Ownership now comes from the expiry argument, and the overlap fails on MSRP at 1180 ms, 191 ms late. The broader required consistent binding remains incomplete for periodic missing/frame-bearing service: retained as R854-2-F1, with its attributable lenses above. |
| R853-1 F1, MINOR, Conformance/Robustness/Tests/Docs | Resolved for its LeaveAll case B. `selftest_leaveall.py:230` tests the second expiry inside the skipped participant's join interval; the old-association mutant fails it. |
| R853-1 F2, MINOR, Conformance/Robustness/Tests | Resolved for its empty-build callback cause. The C0/C controls both fail at 59.979 ms; an unrelated callback no longer restarts the empty-build clock. R854-2-F1 covers different remaining branches, not a claim that this repair failed. |

## Scope and artifact-specific results

Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README, issue #665 and public decisions, REQUIREMENTS.md, FR_NFR 3.4.1, the mailbox and SRP contracts, then the source-range inventory/history and independent delta inspection. The relevant decisions are [sync scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6899740728), [phase coverage](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6907491626), and Q1 above. The latest [train policy](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939574513) governs subsequent composition.

The full source range is `659d7687..e2be92b0`; this later round reviews the 14-file delta from `6ceed75374210935cff4f10d014b9a5ef137615e`, including `c10c549e`, `ccc98b11` and `e2be92b0`. Earlier composition results retain their prior coverage where unchanged. No product firmware, product RTL, configuration, gitlink or numeric bound changes in this delta. `review-state.json` records the range digest, paths and commits.

[R854] PASS RTL - `sim_main.cpp:415`, `observers.py:14`, `observe.vlt:43`, `srp_mbx.c:419`, pinned `third_party/lwSRP/src/core/mrp_mad.c:908`, and published `owner-hook-instructions.txt` - passive observation reads the callback argument and the creation-time binding. The three timers share the participant's registered argument. Creation binds MSRP/MVRP to the interface at Domain publication; incomplete binding becomes unresolved. The published entry instructions preserve the argument registers used by the observer. Generated member-path discovery is carried over with the register-file observer added; product crossings, resets and interfaces are unchanged. No new product RTL build is claimed.

[R854] PASS Docs - `tb/verilator/ctrl_service_budget/README.md:143`, `docs/reference/FR_NFR.md:387`, and `author-r5/receipts/workflows/verify-docs-at-e2be92b0.md` - the LeaveAll proof now states recorded ownership, first MRPDU, 49 ms, commit-versus-wire scope and unresolved-log limits. The generic section accurately describes the retained all-participant no-build horizon and frame-participant rule. Those disclosed rules still fail the functional ownership requirement in F1; their disclosure is not counted as a separate prose defect. The bounds remain 20 ms for measured service rows and 49 ms for this conformance check.

Conformance and Robustness checks independently covered overlapping expiries, reordered clean output, both applications/interfaces, skipped/late/absent LeaveAlls, exact 49 ms boundary and 50 ms rejection, missing/unresolved ownership for all three timer kinds, and empty-build anchors. Tests were also assessed for discrimination: all eight original mutations and seven ownership/anchor mutations are caught, but the two residual F1 branches escape those controls.

## Execution and public receipt audit

Commands below run from this packet, with `<checkout>` naming the reviewed clone.

| Evidence | Result |
|---|---|
| `python3 -B probe_ownership.py <checkout>` | rc 0; 60 controls pass, including the original overlap, clean reordered output and owner rejection |
| `python3 -B check_focused_mutants.py <checkout>` | rc 0; all 15 focused mutations caught, including all eight original controls; clean controls pass |
| `python3 -B probe_missing_build.py <checkout>` | rc 1; eight escapes reproduce F1; twelve discriminating controls pass |
| `python3 -B audit_evidence.py <downloaded-evidence-root>` | rc 0; 214 published files match their published SHA-256 digests; documentation and regrade census passes |
| `python3 -B verify_source.py <checkout>` | rc 0; exact tracked bytes, modes, complete index and required gitlinks match; no restoration needed |
| Full source-range whitespace check | rc 0 |

An optional duplicate local full self-test was stopped intentionally after the blocking defect and focused evidence were established. It completed 879 initial PASS checks and recorded 147 caught mutants before termination, rc 143. It is **not** a complete local campaign pass. Its raw log and rc are retained. The completed full-campaign evidence is the author's published exact-head receipt: rc 0, 879 checks, 261 caught mutants. Its 261 individual catch lines and summary were verified; the full 850,874-byte original log is represented by its digest and selected lines. The earlier round-4 count of 876/258 is superseded by the two later commits.

Public evidence is pinned to [archive ea25c391](https://github.com/kebag-logic/milan-fpga/tree/ea25c391241e10967337ec1bd8ed49ea29c2d4ba/review-evidence/sync1115-r1), author-r4 and author-r5. `evidence-index.json` lists the verified published hashes, separately from pre-redaction hashes. The archive commit's verification metadata says **unsigned**; no cryptographic signature verification is claimed.

- **Documentation:** 63 executed steps have rc 0, and 34 have explicit NOT RUN reasons. There are 62 full raw step logs and one summary/digest-only log, `docs__docs-gates-2__gate_41.log`. Recorded checkout states identify the exact head. Skipped orchestration/install steps are not counted as executed checks.
- **Regrades:** thirteen leg receipts retain their earlier exit codes and tables. Eleven 8x8/1if phases contain 22 loaded groups and 44 owned LeaveAlls, all sent, with no failed LeaveAll outcome. Worst rows remain join 1.86217 ms, LeaveAll 1.64360 ms and periodic 2.96879 ms. The required 1x1/1if valid-destinations leg has rc 0. The 8x8 legs retain rc 1 on the recorded cost findings; they are not whole-leg passes.
- **Ownership and identity:** participant/expiry extracts and entry-instruction receipts were spot-checked. The published comparison records 769 empty builds with owners, 334 anchors moved earlier, and no changed outcomes. Ten seed experiments retain their experiment base and MAC changes with exact-head harness-directory equality recorded. Thirteen firmware image digests match their respective prior runs. These are receipt audits, not independent reconstruction of the unpublished large raw traces or rebuilt images.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | issue #665 Q1; FR_NFR 3.4.1; mrpdu_grade.py:214,239,327; both ownership probes | R854-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |
| RTL | CLEAN | sim_main.cpp:415; observers.py; observe.vlt; srp_mbx.c:419; pinned mrp_mad.c:908; owner-hook-instructions receipt | R854-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |
| Robustness | UNCLEAN, F1 | 60 positive/negative/boundary controls; missing-build and unrelated-frame probes; owner rejection paths | R854-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |
| Tests | UNCLEAN, F1 | selftest_leaveall.py; selftest_mutants.py; 15 focused mutations; exact-head public self-test and regrade receipts | R854-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |
| Docs | CLEAN | budget README:143; FR_NFR:387; PR final behavior sections; 63-step documentation receipt audit | R854-2 | e2be92b0e0f9a8f0529dea252f23ed44a21e050a |

## Limits and pending manager duties

This is a completed negative source review. Fix F1 and independently re-review its affected lenses at the corrected head. Later changes to covered artifacts require renewed coverage. No merge approval is given.

No manager source bank ran at this exact head, and none is inferred. Source-head execution evidence is the author's published receipts plus this review's focused executions. The manager owns hosted/act acceptance, composition review, final current-dev/train builder and native banks, gating qualification, receipt publication, authorized merge and post-merge containment under the latest public train policy. Source base `659d7687` and incoming dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a` are distinct from that future candidate.

#914's per-shape cost lines remain known exclusions. #898's paced SET_CONFIGURATION change is now merged at `cb96336d`; acceptance still needs its composed measurement, not a source-head inference. #929, #916 and #919 retain their stated exclusions. Physical calibration is **NOT RUN**. Simulation, field skips and route/image receipts do not prove hardware behavior.

No source fixes, commits, pushes, GitHub writes, merges, author contact, sub-agents, containers, shared installations, privilege changes or hardware operations were performed. The optional process was stopped and no work remains running. Source verification re-hashed 1,900 superproject blobs plus the initialized required submodules, checking executable/symlink modes and complete index records; the non-required external gitlink remains uninitialized. Disposable inputs remain under scratch and are excluded from publication. Only REPORT.md and files listed by MANIFEST.sha256 are publishable.

R854-2 FINISHED
