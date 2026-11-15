[R836] POSITIVE - exact head 1215bd82f4444ee9d4d9b552a711279a1a5bc1d8

External independent review R836-5 of issue #895 / PR #901. All five lenses are CLEAN for this source-head delta. The four named MINOR/MAJOR findings from R835-4 and R836-4 are resolved. One PR wording residue and the optional suggestions below remain. This verdict does not clear physical or merge-candidate obligations.

Tree: `a547c5a7fae9de4f6e7c0aa1ec4e768325dbdc9f`.
Review start: https://github.com/kebag-logic/milan-fpga/pull/901#issuecomment-6901535392.

Scope and authority

Reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and delegated public rulings, the linked requirement/interface authorities, the full-range change footprint/history from `cec88385`, and the two-commit delta `056d619d..1215bd82`. Applied the later-round rule: unchanged code retains its prior verdict unless a changed dependency invalidates it. This is not a fresh exhaustive review of all 114 files in the full-range diff.

Authorities include Milan v1.2 4.3.3.1 and 5.3.7.4; IEEE 802.1Q-2018 35.2.2.8 and Table 10-7; REQUIREMENTS.md; MAILBOX_CONTRACT.md:255-259; FR_NFR 3.4.1; and issue #895 rulings 6824623445, 6840463408, 6857334948, 6876349305, 6886630886, 6892130675 and 6895331865. The supplied scope accepts grading 1x1/1if and 8x8/2if here; 8x8/1if measurements remain due on the composed image before the flip.

Public evidence is pinned to [archive ea30c5a0](https://github.com/kebag-logic/milan-fpga/tree/ea30c5a0abb21abc91db12d7bf5e5c3d15150966/review-evidence/895-r1), principally `author-r10`, with carried `author-r8` and `author-r9` receipts. REVIEW READY is [6901464046](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6901464046). Prior public findings were read only after the independent diff pass and the written verdict/ledger in `independent-pass.md`.

Resolved findings at their causes

| Finding, original severity and lenses | Disposition | Cause checked and verification |
|---|---|---|
| R836-4-F2; MAJOR; Conformance, Tests, Docs | RESOLVED | Published `author-r10/scripts/costs_vs_stated.py:145,185` passes `r.command` to `record_classes.held` and reads `classes.paced`. `record.aecp` is counted. The real-leg CLI receipt covers all eight preserved round-8/9 selections together and passes. Four over-cost records fail both corrected paths, while the old survey passes them. Coverage and historical exceptions are corrected at `SPLIT_CONTROL_MEMORY.md:2703-2721`. Details below. |
| R835-4-F1; MINOR; Tests, Conformance | RESOLVED | `srp_talker.cpp:336-359` delays Leave to request + JoinTime + TX and asserts that exact departure. Its safety oracle is observed Leave time + fixed 20,000 ms, independent of the macro-derived observation horizon. `srp_talker_mutants.py:118-126` adds drop-TX, floor-TX and drop-both controls. Own runs pass 12 Talker tests at each shape and catch all three plants at each shape on their named assertions. |
| R836-4-F1; MINOR; Docs | RESOLVED | Section 5's old table is bound to round 6 at `SPLIT_CONTROL_MEMORY.md:522`, followed by current images at `:533-544`. The static-assert-only reader claim is attributed to #894 at `:2564`; SRP's current read is stated. Round-13 legs are attributed at `:2726`; this branch's 130,341/218,322 passes are separate. Current notice/TX figures appear at `:2733-2734` and `FR_NFR.md:390`. The 178-entry inventory was counted and relevant provenance changes checked against code/receipts. |
| R835-4-F2; MINOR; Docs | RESOLVED | `SPLIT_CONTROL_MEMORY.md:2279,2734`, `ctrl/aecp/README.md:120` and `ctrl_service_budget/README.md:172` now give 140 ms and 105 ms where current, with #894's 130/99 attributed. Header constants and current analytical rows agree. |
| R836-4-RS1 / R835-4-RS1; RESIDUE; Docs | Original defect RESOLVED | Live roles name R835-5/R836-5, retaining round-4 starts/verdicts as history. Remaining “next” wording is R836-5-RS1 below. |
| R835-4-S1; SUGGESTION; Tests, Docs | TAKEN | `SPLIT_CONTROL_MEMORY.md:2682` distinguishes 18 us of bound headroom from the rounded TX statement's zero slack. `author-r10/receipts/flip-226.log` refuses 34 ms against 34.02 ms at the 226 us base. |
| R835-4-S2; SUGGESTION; Docs | TAKEN | The same paragraph names `review-evidence/895-r1/author-r8/scripts/per_pass_threshold.py` and its evidence branch. |

Cost coverage

`author-r10/receipts/classes/record_classes-real.log` covers arm A, answering-every-port, valid-destinations and answering-ports at both held points. Group counts are 96/16/2/3 at 1x1/1if and 94/16/2/3 at 8x8/2if. The two-interface valid-destinations selection is the round-9 rerun. A passing synthetic self-test is not substituted for these real-leg receipts.

| Point | Class/path | Most CPU cycles | Rule / statement, us |
|---|---|---:|---:|
| 1x1/1if | Paced, accepted SET_CONFIGURATION | 28,288 | 300 / 300 |
| 1x1/1if | Ordinary | 21,187 | 225 / 235 |
| 1x1/1if | Long | 86,698 | 915 / 975 |
| 1x1/1if | SET_STREAM_INFO, held ordinary | 20,363 | 215 / 235 |
| 8x8/2if | Paced, accepted SET_CONFIGURATION | 55,365 | 585 / 595 |
| 8x8/2if | Ordinary | 18,904 | 200 / 265 |
| 8x8/2if | Long | 126,152 | 1,325 / 1,650 |
| 8x8/2if | SET_STREAM_INFO, held ordinary | 17,511 | 185 / 265 |

The audit independently recomputed every nonzero survey row using measurement +5%, rounded upward to 5 us: 63 statements per point, 57 measured within their statements, six unstaged. The six are probe items in both load columns, donor build, donor owed MRPDU, poll owed MRPDU, and whole-pass build. These are explicitly derived, not measurements. Round costs remain under each leg's separate round check; the tick floor is not another surveyed measurement.

Published controls raise SET_CONFIGURATION to 40,000/60,000 cycles and SET_STREAM_INFO to 30,000 at each point. Both corrected paths return 1 and identify the offending class; the survey prints UNDER 1. Unplanted controls return 0. The old survey returns 0 for all four plants, reproducing the original hole. Own predicate probes confirm that passing SET_STREAM_INFO holds it, omitting its command excludes it, and 30,000 cycles exceeds both ordinary statements. The unchanged class grader's 11 self-controls pass. `held` excludes 8x8/1if; no class measurement is claimed there.

Every measured value remains inside its statement. No row, load, pace or slice restatement follows. Unchanged inputs select the 900 us slice, 9 ms pace, 140 ms queued bound and 34/105 ms TX statements. Documented 1x1/1if rows remain R4 13.25, R5 75.84, R6 73.36, first/last notice 14.72/136.65, R4L 203.57, ACMP 29.63, ADP 27.86, MAAP 27.96, TX 34.00 and TXL 48.58 ms. Their unchanged dependencies and published receipts were checked; a previously covered full analytical bank was not rerun.

Test sensitivity and executable evidence

Own native runs used two concurrent foreground child processes, eight compiler jobs each. Baselines pass all 12 Talker tests per point. Drop-TX fails with wire intervals of 19,966 ms at one interface and 19,895 ms at two; floor-TX fails at 19,996/19,995 ms. Drop-both still fails the existing wire-floor test. The new test therefore detects the previously escaping TX-term regression and rounding down. Its baseline assertion proves the 20,000 ms floor; its macro-derived horizon only allows observation to finish.

The delta contains two test files and five Markdown files. No HDL, firmware image source, interface or gitlink changes occur in it. The full-range footprint also has no HDL/submodule changes. Independently compared author hash lists have the same 552 entries and hashes at 056d619d and 1215bd82. This corroborates carrying unchanged image measurements; it is not a reviewer image rebuild.

The exact-head author ledger passes all four platform points: 43.0, 44.0, 56.0 and 60.5 RAMB36. The 8x8/2if platform has 131,752 B ROM, 1,368 B spare; fixture 126,608 B, 368 B spare; answering-every-port/valid-destinations 60/200 B spare. `ctrl_plat` at 8x8/1if is 18,240 B. Current documentation matches those receipts.

The workflow table counts 86 executed steps at this head, 53 carried from 056d619d, 226 NOT RUN with reasons, zero bad. Changed-path jobs include firmware-unit and all three firmware mutation jobs. Source-head receipts report SRP 421 plants, 76 Talker rows, zero escaped; control 716/716 and AECP 299 rows. The six new plant runs account for SRP's change from 415 to 421. The 65-suite sweep and unaffected builder/native jobs remain carried author evidence, not current-head manager executions. NOT RUN is not counted as executed.

All 1,178 selected public files match the published SHA-256 manifest. Receipt INDEX entries match 203/203 for r8, 670/670 for r9 and 226/226 for r10. The archive commit's Git signature status is `N`: no cryptographic signature is present. Verified integrity is against published hashes at the pinned Git object, not a signed attestation. Original built objects and complete raw simulation legs were not rebuilt or regraded locally.

Earlier findings

| Prior IDs / severity / lenses | Disposition and cause at this head |
|---|---|
| R835-3-F1 MAJOR; Conformance, RTL, Tests, Docs | RESOLVED including the wider audit: 225 us covers 21,094 cycles; its remaining class-audit hole is closed as R836-4-F2. Slice/dependencies are unchanged in this delta. |
| R835-3-F2 MINOR; Conformance, Tests | Closure retained: `rows_tiers.py:101` states 30 us for 2,465 cycles; survey arithmetic checks it. |
| R836-3-F1 MINOR; Docs | Closure retained: current R4 remains 13.25, not 12.85. |
| R836-1-F1 / R835-1-F1 MAJOR; Conformance, Docs; R836-2-F1 MINOR; Conformance, Docs | Closures retained under the public amendment and current PR evidence. Acceptance 4 is the ruled composition scope; 8x8/2if is reported, hardware separate. Round-1 source/count claims are no longer current. |
| R836-1-F2(a,b) / R835-1-F2 MINOR; Docs | Historical pass-cost/ROM-growth corrections retained; later images separately attributed in sections 5/13. Latest attribution defects closed above. |
| R836-1-F3 / R835-1-F3 MINOR; Docs | Closure retained: current table has 38 Talker plants at each count, receipts 76 rows and SRP 421. Earlier 26/28 confusion is historical. |
| R835-1-F4 MINOR; RTL, Robustness, Docs; R836-1-RS2 RESIDUE; Docs | Closure retained at `srp_bounds.h:49-59`: once per declarations pass, twice on the built interface. Publication test at `srp_talker.cpp:534` passes in both own baselines. |
| R835-1-F5 MINOR; Robustness, Conformance; R836-1-S1 SUGGESTION | Closure retained at `srp_mbx.c:296-301,339`: refused Leave keeps declaration/work owed and starts no hold-off. Refusal test at `srp_talker.cpp:579` passes at both shapes. Original unreachable-path interpretation remains withdrawn. |
| R836-1-RS1 / R835-1-RS1 RESIDUE; Docs | Issue-only/cold-code wording retained in `ctrl_memory.py`; no new forbidden source-comment identifiers in this delta. |
| R835-1-RS2 RESIDUE; Docs | First-declaration/gateless qualifications retained at SRP README:193-198. |
| R835-2-RS1 RESIDUE; RTL, Docs | Corrected second-pass/refused-withdrawal wording retained at `srp_bounds.h:54-55`. |
| R836-2-RS1 / R836-3-RS1 RESIDUE; Docs | Scope-of-unchanged-figures and size-versus-byte-identity corrections retained. Current equality has separate hash evidence. |
| R835-3-RS1 RESIDUE; Docs | Originally unassigned roles remain assigned; “next” residue is separate below. |
| R835-3-S3 SUGGESTION; Docs | Base attribution remains explicit at `SPLIT_CONTROL_MEMORY.md:528`, against 5b264bf2 and separately round 5/6. |
| R835-2-S2 / R836-3-S5 SUGGESTION; Docs | Taken for current evidence: every selected INDEX entry matches final published bytes. |
| R835-1-S2 / R835-2-S4 SUGGESTION; Conformance | Closed: SRP README:229-233 distinguishes configured LeaveAllTime from random intervals. |

Current residue

R836-5-RS1 | RESIDUE | Docs | PR #901, “Linked Issue / roles”.

Authority/evidence: roles say R835-5/R836-5 “(next)”, but public starts [6901529577](https://github.com/kebag-logic/milan-fpga/pull/901#issuecomment-6901529577) and [6901535392](https://github.com/kebag-logic/milan-fpga/pull/901#issuecomment-6901535392) already exist. Impact: stale navigation wording only; no figure, verdict, clause, privacy or execution claim changes. Exact outcome: replace each “(next)” with a “started” link to its current start, then link published verdicts when available. Verification: live role lines match those starts. This does not make Docs unclean.

Retained optional suggestions

Every row below has severity SUGGESTION. These unchanged causes are not promoted into requirements.

| ID / all lenses | Artifact and authority/evidence | Impact | Optional outcome | Verification |
|---|---|---|---|---|
| R835-4-S3; Robustness | `srp_mbx.c:650`, first-call cached-gate guard; init clears `gate_seen` | First-call guard lacks its own mutation control | Add drop-`gate_seen` control | First-call test kills it at both shapes |
| R836-3-S1 / R836-1-S2; Conformance, Robustness | `srp_mbx.c:639-676`; IEEE 802.1Q 35.2.2.8; unchanged destination comparison | D/E/D recovery can conservatively wait | Track last-declared identity if latency warrants it | Timed D/E/D test distinguishes unchanged/changed FirstValue |
| R836-3-S2 / R836-1-S3; Tests | `srp_talker.cpp:393`, admission-swap allocation refusal | Refusing all allocation suppresses transmission, limiting wire-order oracle | Refuse only replacement join, leave transmission available | Leave-before-join plant fails on wire order |
| R836-3-S3 / R835-1-S1 / R835-2-S3; Tests | `srp_mbx.c:131`, expiry wake-up | Other two-interface activity can mask missing isolated wake-up | Isolate expiry from other scheduling stimuli | Missing-wake plant fails independently of never-ending hold-off |
| R836-3-S4 / R835-2-S1; Robustness | `srp_mbx.c:296,1186,1232`, refused Leave and VLAN/licence ordering | Future refusal paths could break implicit dependency | Document invariant or explicitly gate licence on validity | Listener-registered refused-withdrawal test proves no premature reopening |
| R835-3-S1; Robustness | `maap_mbx.c:260-268`, startup SID-written mark and fixed entity identity | Future dynamic identity before first opening needs explicit invariant | Document fixed identity or test supported first-opening transition | Both SID words precede gate opening |
| R835-3-S2; Tests | `record_classes.py` and published survey; 5%-then-5-us rule | Correct wider survey is still a per-round evidence script | Consider integrating full survey into routine validation | Same real-leg and over-cost controls exercise that entry point |

Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #895 acceptance/rulings; MAILBOX_CONTRACT.md:255-259; srp_mbx.c:31-35; srp_talker.cpp:336-359; record_classes.py:128-168; class/survey receipts against wire floor and cost rule | R836-5 | 1215bd82f4444ee9d4d9b552a711279a1a5bc1d8 |
| RTL | CLEAN | Full-range/delta footprints; unchanged product blobs/pins; srp_bounds.h:49-59; 552-image comparison; exact-head ledger and unchanged analytical dependencies | R836-5, delta plus preserved prior coverage | 1215bd82f4444ee9d4d9b552a711279a1a5bc1d8 |
| Robustness | CLEAN | Latest-Leave scheduling at both counts and three fault controls; reset/admission/refusal tests in own baselines; command-sensitive holding and four published over-cost controls | R836-5 | 1215bd82f4444ee9d4d9b552a711279a1a5bc1d8 |
| Tests | CLEAN | srp_talker.cpp:336; srp_talker_mutants.py:118-126; own baseline/six fault logs; class CLI receipt; survey arithmetic/coverage; workflow rerun/carry table and SRP campaign | R836-5 | 1215bd82f4444ee9d4d9b552a711279a1a5bc1d8 |
| Docs | CLEAN | All five changed Markdown files; sections 5/13 current/historical figures; FR_NFR.md:390; README deltas; 178-entry inventory; PR/REVIEW READY; manifest/indexes; wording residue separated | R836-5 | 1215bd82f4444ee9d4d9b552a711279a1a5bc1d8 |

Real limits and pending manager duties

- This verdict covers the source head. No manager source bank ran at this exact head; none is inferred from author receipts or carried executions.
- The manager must construct/validate the current-dev merge candidate, including builder and native banks, and publish candidate SHA/tree and receipts. Source base is cec88385; supplied live dev is `6b66f66d89cf25d2717687bcc2c3bf617685a99a`. Re-read dev at the merge turn. The historical dev-soft-core candidate does not prove this candidate.
- Hosted/act acceptance remains manager-owned. This reviewer did not run Docker, act or the host orchestrator, or inspect hosted jobs. Source execution counts do not establish hosted required contexts; skipped contexts are not executed banks.
- Hardware acceptance 6, physical calibration and field campaigns are not established here. Physical calibration is NOT RUN; field skips are not hardware proof. Both stream directions with counters and applicable timing-floor proof remain bench/manager duties.
- 8x8/1if has no class leg in this packet; measure it on the composed image before its flip. 8x8/2if still misses its reported flip targets; #890/composition duties remain. The 1x1 paced class has no statement margin, ACMP has 0.37 ms and TXL 0.42 ms, and the largest answering arm has 60 B ROM spare.
- Carry R836-5-RS1 to the residue checklist. Wait for the other review to finish, obtain required positives, validate the candidate, obtain merge authorization, then perform containment and public Issue/Project completion.

Reproduction and receipts

From the exact source head with required initialized pins, using a writable packet directory:

```sh
rtk git fetch --no-tags origin ea30c5a0abb21abc91db12d7bf5e5c3d15150966
rtk proxy python3 -B probe_talker.py SOURCE PACKET
rtk proxy python3 -B audit_receipts.py SOURCE PACKET
rtk proxy python3 -B verify_source.py SOURCE PACKET
```

`probe_talker.py` runs focused native tests and disposable fault copies. `audit_receipts.py` extracts only selected public author packets into scratch, verifies published hashes/indexes, compares image receipts, and checks survey arithmetic and command-sensitive predicates. `verify_source.py` verifies raw tracked bytes, executable modes and the full index against HEAD, repeating at all five initialized required pins.

Final identity check: 1,626 parent blobs and 1,238 submodule blobs match pinned bytes/modes; all six indexes match, required gitlinks match, porcelain status is empty. Source files were never edited; mutations lived under packet scratch. No new prohibited source-comment identifiers were found. Only MANIFEST.sha256-listed files and REPORT.md are publishable; scratch is excluded.

R836-5 FINISHED
