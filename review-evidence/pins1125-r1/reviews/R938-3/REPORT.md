[R938] POSITIVE - exact head d3cb3cf180f846a969f5baacf8b2bec34e4acd50

R938-3 external independent review of issue #1013 / PR #1016.
Tree: `eb3ebcb7e1ad48818893afad260ff060937c6c96`.

Scope: the one-commit delta from `e5d8a71b6fa90352eca72314c7bd2275a1b20285`, plus the four specified PR/source corrections. The issue, public pin ruling, repository authorities, source-base diff and history were reconstructed before evaluating the delta. All five lenses were applied to this scope. Unchanged implementation coverage is retained under the owner's later-round rule; this is not a new full-bank review.

The independent pass found no new blocking, major, minor, residue or suggestion finding. The verdict and ledger were written before consulting prior reviewer reports. The prior-finding reconciliation below retains one existing wording residue and two optional suggestions; none makes a lens unclean.

Evidence and bounded conclusions:

- `round3.diff` and `verify_review.py` prove that the single commit changes exactly the specified source comment and one changelog line. Both retain mode `100644`. Every other tree entry is identical to the preceding reviewed head. The harness differs only by the exact comment replacement: no expression, constant, stimulus, check, test name, build input, RTL or gitlink changes.
- `tb/verilator/gptp_shadow/sim_main.cpp:2985` now describes `before - kGradedOffsetNs`, with `kGradedOffsetNs = 400` and `kOffsetNearNs = 64`. Lines 3047-3053 capture before/after, send the graded pair and check freshness beyond 200 ns plus proximity to `before - 400`. `near` at line 171 uses inclusive bounds. The comment states the small-delay discrimination limit and delegates nanosecond grading to phase 6. The enclosing block cites FPGA-gPTP #109 and governing clauses. The new text contains no reviewer identity, round, bench label or private path.
- PR body, phase-22 table row: “as it does when” describes the observed passing case without claiming the 64 ns tolerance uniquely proves the exact signed delay. `tb/verilator/gptp_plane/sim_main.cpp:693` checks the expected offset exactly. Its eight defect cases in `link_delay.py:54` and the published receipt cover finer delay semantics, including the -799 ns floor and used-delay clamp.
- `CHANGELOG.md:75` correctly counts eleven planted gPTP defects: eight in `gptp_plane/link_delay.py`, plus public negative-delay publication, stale offset and omitted graded Follow_Up in `gptp_shadow/mutants.py:213`. The clean baseline is not a defect. The round-two receipts name all eight plane catches and these three shadow catches.
- PR body, final reproduction instruction: `gptp_shadow run` now expects `25 FAIL`. Published `old-generator-red.log:38-63` contains 25 shadow failure lines and `490 checks: 465 PASS, 25 FAIL`. The same receipt records plane `32 FAIL` and datapath `3 FAIL`; neither is substituted for the shadow result.

Prior public finding reconciliation (read after the independent verdict and ledger were written):

| Finding | Original severity and lenses | Disposition at this head | Cause-level evidence |
|---|---|---|---|
| R937-2-F1 | MINOR; Tests, Docs | RESOLVED | PR body line 94 now says “as it does when”, consistent with the phase-22 64 ns predicate and README row 22. The published R937-2 p6 probe still passes the -3 ns trial with a wrong used delay of zero (delta -398 ns); the revised claim no longer excludes that observation. |
| R937-2-F2 | MINOR; Docs | RESOLVED | CHANGELOG.md:75 says “Eleven planted defects”. Source tables and named catches establish 8 + 3; the clean baseline is excluded. |
| R938-2-F1 | MINOR; Tests, Docs | RESOLVED | PR body line 193 says “25 FAIL”; the completed shadow tally and all 25 failure lines in the published old-generator receipt agree. |
| R938-2-F2 | MINOR; Tests, Docs | RESOLVED | sim_main.cpp:2985 now specifies the previous offset less kGradedOffsetNs, matching :3053. The zero expectation and obsolete nearest-wrong-value explanation are gone. The published clean receipt has before=1/after=-400 and before=-12/after=-408 for the first and -263 ns trials. |
| R937-1-F1; R938-1-F1 | MINOR; Tests, Docs | Resolution retained | The before/after predicates and both added controls are unchanged. The author receipt catches stale-bank and omitted-pair plants by name; published R938-2 probes also reject an omitted Follow_Up. |
| R937-1-F2 | MINOR; Docs | Resolution retained | GPTP_PLANE.md:160-164 still distinguishes exact engine/used-delay checks from public-bank coverage. |
| R938-1-F2 | MINOR; Tests, Docs | Resolution retained | The published old-generator datapath receipt ends 239 PASS / 3 FAIL; PR text expressly excludes the unrun gptp-lat comparison. |
| R938-1-F3 | MINOR; Tests, Docs | Resolution retained | SUBMODULES.md:1133-1139 retains “no base pair” and the three-pair boundary; CHANGELOG.md:82 and PR route text restrict equality to paired/selected results. |
| R937-1-R1; R938-1-R1 | RESIDUE; Docs | Resolution retained | The phase-6 README row remains contiguous with rows 1-5. |
| R937-1-R2 | RESIDUE; Docs | Resolution retained | GPTP_PLANE.md:150-152 retains the explicit signed-use antecedent. |
| R937-1-R3 | RESIDUE; Docs | Resolution retained | The current PR begins with one role-prefix line. |
| R937-1-S1 | SUGGESTION; Tests | Addressed, unchanged | milan_dp/sim_gptp.cpp:1705 retains “harness precondition: the peer presents a negative delay”. |
| R938-2-R1 | RESIDUE; Docs | RETAINED, non-blocking | The two old PR scope summaries remain. Exact disposition below. |
| R937-2-S1; R937-2-S2 | SUGGESTION; Docs | RETAINED, optional | The unchanged adoption summaries remain true but abbreviated. Exact dispositions below. |

The four closures above leave no MINOR, MAJOR or BLOCKER open in this scope. R938-2's clean Conformance, RTL and Robustness coverage remains applicable because this delta changes none of its executable dependencies; this round rechecks the changed claims and restores clean Tests/Docs coverage at the exact current head.

Retained non-blocking items, consolidated for the manager:

**R938-2-R1 - RESIDUE - Docs - PR body lines 25 and 202.**
Authority/evidence: the prior public finding and the unchanged summaries omit the later harness/control edits, while the same PR's history and test sections identify them and the image-input equality remains established. Impact: wording inconsistency only; no measurement, test result, clause or privacy claim changes.
Exact required outcome: replace “Only the gitlink and the records naming the pin changed after them” with “Later changes also update consumer harnesses and controls; image inputs remain unchanged.” Replace the final sentence of the limitations paragraph with “Later changes move the gPTP pin from 3009f9a2 to 3ce71b76 with identical hdl/ and syn/ trees, update pin records, and revise consumer harnesses and controls.”
Verification: both summaries agree with the changed-file history and existing image-input proof. This remains on the residue checklist; it does not unclean Docs.

**R937-2-S1 - SUGGESTION - Docs - docs/reference/SUBMODULES.md:1107.**
Authority/evidence: the prior public suggestion and the unchanged sentence name only the clamp-removal control, while mutants.py:213-240 contains three phase-22 controls. Impact: an accurate but incomplete summary.
Optional outcome: “Its campaign plants the clamp's removal, a stale public offset and an unsent graded pair; each fails by name.”
Verification: compare the three cases and their named campaign catches. No mandatory change or coverage loss.

**R937-2-S2 - SUGGESTION - Docs - docs/design/GPTP_PLANE.md:164.**
Authority/evidence: the prior public suggestion and unchanged sentence mention public-word coverage; phase 22 also has its 64 ns graded offset check. Impact: abbreviated coverage description.
Optional outcome: “gptp_shadow phase 22 grades the public word and, to 64 ns, the used delay; the milan_dp legs grade the public word.”
Verification: compare the public-bank and offset checks with the phase-22 README row, preserving the stated tolerance. No mandatory change or coverage loss.

Public finding sources: [R938-2](https://github.com/kebag-logic/milan-fpga/pull/1016#issuecomment-7182632172), [R937-2](https://github.com/kebag-logic/milan-fpga/pull/1016#issuecomment-7182662299), and their linked prior dispositions. Historical reviewer receipts were opened only after this round's own verdict and ledger were written. Three supporting prior probe receipts were independently checked against the manager's published SHA-256 manifest. Their executions remain attributed to round two.

Reviewer-owned coverage ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #1013 and public pin ruling; REQUIREMENTS.md REQ-PTP-05/07; GPTP_PLANE.md:133; phase-22 PR row; gptp_shadow/sim_main.cpp:2985,3053; exact phase-6 check at gptp_plane/sim_main.cpp:693 | R938-3, narrow delta with unchanged coverage retained | d3cb3cf180f846a969f5baacf8b2bec34e4acd50 |
| RTL | CLEAN | round3.diff; verification.log; unchanged hdl tree, image inputs and gitlinks; exact source-comment replacement check | R938-3, narrow delta with unchanged coverage retained | d3cb3cf180f846a969f5baacf8b2bec34e4acd50 |
| Robustness | CLEAN | gptp_shadow/sim_main.cpp:3047; gptp_shadow/mutants.py:213; published stale/omitted-pair catches and plane boundary/floor catches; unchanged predicates | R938-3, narrow delta with unchanged coverage retained | d3cb3cf180f846a969f5baacf8b2bec34e4acd50 |
| Tests | CLEAN | gptp_plane/link_delay.py:54; gptp_shadow/mutants.py:213; round-two gptp_plane.log, gptp_shadow.log, old-generator-red.log; PR reproduction instruction; exact no-behavior-change verification | R938-3, narrow delta with unchanged coverage retained | d3cb3cf180f846a969f5baacf8b2bec34e4acd50 |
| Docs | CLEAN | CHANGELOG.md:75; gptp_shadow/sim_main.cpp:2985; current PR phase-22 row and reproduction instruction; governing source-comment rule | R938-3, narrow delta with unchanged coverage retained | d3cb3cf180f846a969f5baacf8b2bec34e4acd50 |

Receipt provenance and verification:

- Round-one public evidence is pinned to `4b3b21e2104d37db96040622edfe75a5acbf2a76`; round-two evidence is pinned to `e185cf1181dac7690707428deda80b88537f16b0`, under `review-evidence/pins1125-r2`. All 78 round-one and 11 round-two published author-receipt hashes match their manifests.
- These manifests establish byte integrity, not independently executed results or cryptographic signer authentication. No detached signature or signing authority was supplied in those packet paths; no signature-authentication claim is made.
- The round-two author receipts record preceding source head `e5d8a71b6fa90352eca72314c7bd2275a1b20285`: plane 102/102, shadow 490/490, shadow campaign 16/16, and named old-generator failures. They remain relevant through the proven comment-only delta. They are not relabeled as executions at the round-three head.
- Independently executed at this head: documentation style passes for 25 current documents; the documentation/privacy gate reports zero findings across 226 Markdown and 1,959 text files, with 23/23 scrub controls and 4/4 routing arms. Receipts: `doc-style.log`, `docs-check.log` and their `.rc` files. The live PR head/body were also re-read and match `pr-snapshot.json` and `pr-body.md`.
- Reproduce this review's bounded checks from the detached clone with `python3 /path/to/packet/verify_review.py .`, followed by `python3 /path/to/packet/check_claims.py .`. The pinned public evidence commits must be present. `verification.log`, `claims.log` and their `.rc` files record success. Documentation commands were `python3 -B scripts/check_doc_style.py` and `python3 -B scripts/docs_check.py`. No simulation or mutation rerun was necessary for these four corrected prose claims.
- The verifier compares raw working-tree blob hashes and filesystem modes against the commit and every index entry against that tree. All 1,984 superproject blobs and the five initialized required submodules pass. The unused `external` gitlink remains recorded and uninitialized. No source bytes were edited.

Limits and pending manager duties:

This review does not establish full acceptance or authorize merge. No manager source bank ran at this head, and none is inferred. Source execution receipts are the author's published evidence. The manager owns exact-head hosted/local-replica acceptance, distinguishing executed jobs from skipped contexts, and the hosted em-dash gate whose renderer is unavailable on the author host. This reviewer did not run that gate or claim a hosted result.

The manager must validate and publish builder/native-bank receipts for the final current-dev merge candidate. Source base: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`; stated live dev: `e275d7950ef3385753e6a15d2e191ba855b171ed`. These are distinct from the reviewed source head. Required independent review completion, merge authorization, containment and issue closure remain manager duties. Physical calibration is NOT RUN; field skips and desk receipts supply no hardware proof.

R938-3 FINISHED
