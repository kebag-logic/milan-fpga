[R666] POSITIVE - exact head 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e

Issue #188 + #189 / PR #195, round R666-3. Tree `34af6de87215cc90a774757debc8af90073aaa87`.

**R666-2-001 is RESOLVED.** The live PR Records bullet contains the required correction, and the remaining numerical Records claims agree with the published author-r2 receipts. No MINOR, MAJOR or BLOCKER remains in this round's scope. All five lenses are CLEAN. Source and executable coverage are carried from R666-2 at the identical head; this round performed evidence-accounting and integrity checks, with no simulation, source edit or GitHub write.

The [public review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195#issuecomment-6285385970), [round-2 scope decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195#issuecomment-6264243047), and [immutable evidence publication](https://github.com/kebag-logic/milan-fpga/tree/61e4bb57da96c2c2e4d60987f390a435384ffe9f/review-evidence/pp188-r1) identify the reviewed work.

Reconstruction followed the assigned order: supplied instructions and repository instruction-file checks (no repository AGENTS.md or CONTRIBUTING.md); docs/README; frozen issue bodies and public manager scope; linked requirement/interface authorities; baseline-to-head diff and history; then published receipts. The source pass concentrated on the listener, top-level registered-type selection and campaign accounting, consistent with the unchanged-head scope. Authorities include REQ-ACMP-011/016/018/022, REQ-NET-003, REQ-SRP-005, architecture/02 event and status contracts, 05 §6.3 and 10 §6.4: Milan Tables 5.30/5.39 and §4.2.7.2.2; IEEE 802.1Q §10.7.7/Table 10-3 and §35.2.6. Original standards PDFs were not supplied. No new normative interpretation is made.

The independent verdict and five-lens ledger were saved in `independent-verdict.md` before reading prior public review findings or another reviewer's report. Previous findings were then reconciled below. No private author material or other checkout was inspected. The PR has no submitted review objects or inline review comments; the public findings are in its conversation comments.

**R666-2-001 — MINOR, now RESOLVED — Docs, Tests.** Artifact: [PR #195 Records](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195), captured in `pr-body.md` and both PR snapshots; accounting owner `tb/srp_top/mutants.py:250,299-313`. The prior claim treated successful goldens and coverage as killed mutants, overstating killed entries by 18 at each revision. The required outcome was to distinguish those categories without changing immutable receipts. The live bullet now reads:

> `tb/srp_top`: 150 -> 161 mutation entries, all KILLED; 17 golden runs PASS at each revision, plus one passing assertion-coverage check (94/94 -> 101/101), giving 168 -> 179 total campaign checks

| Published revision | KILLED mutation entries | PASS goldens | PASS coverage check | Total checks |
|---|---:|---:|---:|---:|
| cb8bab04 | 150 | 17 | 1 (94/94) | 168 |
| cca12e3c | 161 | 17 | 1 (101/101) | 179 |

Verification counted individual raw outcome lines, independently of each footer. Source inventories also contain 150 and 161 entries; the exact reviewed head's driver is byte-identical to cca12e3c. `verify_counts.py` and `counts-verification.txt` reproduce the recount. `pr-body-correction.diff` shows that only this bullet and trailing whitespace differ from the published author-r2 draft. A final live re-fetch confirmed the same body and head.

The other Records claims also agree:

| Claim | Raw receipt verification |
|---|---|
| Suite checks 1,030,051 → 1,030,070, zero failures | Independently summed all 36 suite rows at each revision |
| pp_top 10,533 → 10,543; srp_stream_fsms 1,352 → 1,361 | These are the only changed suite rows |
| ACMP 60 → 65 killed entries | Counted individual JSON verdicts; footer agrees |
| Other affected campaigns identical | All 12 other campaign logs agree after path normalization and line ordering, preserving verdict text |
| Final processor return codes zero | Seven gates and fourteen campaigns per revision, all zero |
| Unchanged lint, matrix, synthesis and elaboration results | Four corresponding raw gate logs byte-identical |
| Documentation check differs only in link/file counts | Links 1,215 → 1,216; files 617 → 625; eight added patch files confirmed from history |
| Consumer results identical, two failures retained | Both retain `lint_rtl=1` and `submodule_docs=1`; other return codes zero |
| Shadow LUT 56,701 → 56,105 | Raw rows agree; other independent resource categories unchanged. Derived LUT_TOT correspondingly changes 60,937 → 60,341 |
| Six author commits in round 2 | History from cb8bab04 to cca12e3c contains six commits |

These are measurements at the expressly named author revisions, not a claim of full-gate execution at the merged review head. Source history, test identifiers, storage widths and clause numbers elsewhere in the body retain their previous assessment.

**Retained residue and suggestions.** These are carried public items, not new work assigned by this round. Their severity and lens treatment are unchanged.

- **R666-2-002 / R665-2-R1 — RESIDUE — Docs, Tests.** `tb/srp_top/mutants.py:184` still says `# WK12's own counts and its precondition, at every shape`. Authority: owner comment rule, 2026-10-15. Impact is explanatory wording only. Exact required fix: `# Grade the repeated-settle walk counts and precondition at every shape.` Preserve executable selectors and expected failure strings. Verification: comment-only diff with no executable change. Carry to the manager's merge residue checklist, as expressly directed; existing unrelated labels remain under #746.
- **R665-2-R2 — RESIDUE — Docs.** `docs/architecture/05_acmp_engine.md:191-192` still says a coalesced event “carries” the type registered when taken. Authority/evidence: 02 §5 and 05 §6.3 distinguish first payload from the live level read by `hdl/top/protocol_processor_top.sv:3300-3313`. Impact is the previously identified wording ambiguity, with no changed implementation or clause claim. Retain the exact fix: “A coalesced `EVT_TK_REGISTERED` is still taken with the type the sink registers at that moment: the top reads it from the SRP listener's level, not from the event's first payload (§6.3).” Verification: inspect that sentence and confirm only prose changes.
- **R665-1-S1 / R666-2-S1 — SUGGESTION — Docs.** `tb/pp_top/README.md:2120-2130` retains the historical measurement-date lead-in alongside the later correct `1 of 58` teardown row. The manager explicitly left this unassigned. Suggested outcome: date the updated cell or explain that issue-specific annotations override the historical date. Verification: point to the existing receipt without altering its count. Impact is provenance clarity only.
- **R665-2-S2 — SUGGESTION — Docs.** PR Records and its WK12 table row retain the optional clarity improvements: state explicitly that cca12e3c receipts precede the merge with main 24c7f853, and add the three controls grading the walk counts/precondition (`listener-rebind-abandons-leave`, `listener-park-never-retires`, `listener-aa-tx-stays-aa`). Authority/evidence: merge history and `tb/srp_top/README.md:806-812`. Impact is summary completeness; existing measurements and controls are accurate. Verification: any optional wording agrees with those artifacts. No new run is required.

**Other prior findings remain resolved at this exact head.** Their closure evidence from [R666-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195#issuecomment-6285089712) is carried unchanged. The later [public internal review](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195#issuecomment-6285373711) was read only after the independent verdict was written.

| Prior finding | Disposition and cause-level evidence |
|---|---|
| R666-001 / R665-1-F2 | RESOLVED, carried. Top reads the current registered type at event acceptance; listener bookkeeping adds no Table 5.30 transition. AS5d/AS5e and the killed first-payload control cover both coalesced directions; 05 §6.3 and the PR remove the former residual exception. |
| R665-1-F1 | RESOLVED, carried. RB4–RB8 cover all five assigned settle arms with named killed controls; RB9 covers no-record startup; WK12 covers repeated settles at both storage implementations. Coverage requires RB1–RB9/WK1–WK12. U6/U7 remain accepted likely equivalents. |
| R665-1-F3 | RESOLVED, carried. Banner, 10 §6.4 and PR same-stream row distinguish LA Leave, LO Empty and either state's New transition. |
| R666-002 | RESOLVED for all original listed locations, carried. Prior explanatory bench-label removals remain; the separate line-184 residue is retained above. |

Reviewer-owned final ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | frozen issues and scope; REQ-ACMP/NET/SRP rows; 02 contracts; 05 §6.3; 10 §6.4; unchanged source identity | R666-2 carried; R666-3 dependency check | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| RTL | CLEAN | listener settle/bookkeeping and top live-type mux diff; exact tracked blobs, modes and index | R666-2 carried; R666-3 identity | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| Robustness | CLEAN | unchanged parked identity, record guard and event coalescing paths; carried RB4–RB9/WK12 and blocked-TX evidence | R666-2 carried; R666-3 dependency check | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| Tests | CLEAN | raw campaign lines and suite rows, source inventories, coverage accounting, published hashes; R666-2-001 closure | R666-2 executable coverage carried; R666-3 accounting | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| Docs | CLEAN | docs/README; live PR versus published draft and raw receipts; retained residue and suggestions | R666-2 coverage carried; R666-3 closure | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |

Evidence integrity and real limits: all 195 selected public artifacts match `published_sha256` in the immutable publication manifest, including declared path redactions. This is a selected receipt audit, not a claim to have rehashed the entire publication. The publication commit's verification record says `unsigned`, and no detached signature was supplied: signer authenticity remains NOT VERIFIED. The final integrity receipt confirms all 680 tracked blob bytes and executable modes, the exact index tree and a clean checkout. The processor has zero gitlinks. All six consumer gitlinks were checked against the public parent with the declared base/head processor substitutions; the supplied live-dev pins were also recorded. No source restoration was needed.

No simulation, full bank, hardware run or hosted job was executed in this round. Prior focused exact-head executions retain their R666-2 coverage; public author full-gate receipts name cca12e3c and consumer parent e9cbb676 with two declared patches. They are neither an all-green consumer bank nor manager execution at 7f56fc4d. No manager source bank exists or is inferred here. Hosted contexts were not re-polled; prior pending work is not represented as completed or skipped contexts as executed. Physical calibration NOT RUN and field skips are not hardware proof. No timing-closure or field-validation claim is made.

The manager retains hosted/act acceptance, the residue checklist, and final current-dev candidate validation with builder/native and consumer banks plus linked receipts at merge turn. Source base is b48312e1; supplied live dev is e26f1816e456dc8027924bc2e5d327a8aa6e46db. Source validation and final candidate validation remain distinct. This positive source review does not authorize a merge or replace the two-independent-positive-review requirement and full completion bar.

Portable checks: run `python3 fetch_receipts.py`, `python3 verify_counts.py`, and `python3 verify_integrity.py /path/to/exact-head-clone` from this packet. The fetcher reads only the fixed public revision. `MANIFEST.sha256` lists every publishable receipt/script using relative paths. Only its listed files and REPORT.md are publishable; `scratch/` is excluded.

R666-3 FINISHED
