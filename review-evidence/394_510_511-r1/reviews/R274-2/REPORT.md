[R274] POSITIVE - exact head 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6

Round R274-2. Internal cleared-context re-review of PR #537 (Closes #511; Relates to #394 and #510) after correction round 1.

- Head `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6`, tree `ef96bf2fe0d66dd9c0b1ba45c6b4300d89ba658c`.
- Source base `759da623072358afdb0e9d570a7b4b6a788492c9`, an ancestor of the head.
- Seven linear commits. Each is one line with no trailers (`receipts/commit_messages.txt`).
- Whole PR: 11 Markdown files, +230/-26. Correction round: one commit on `64bcf768`, 4 Markdown files, +40/-9.
- No RTL, firmware, builder, configuration, test or gitlink change (`git diff --raw`: all `*.md`, modes 100644).

Reconstructed from, in this order:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. The bodies of #394, #510 and #511, the 2026-09-23 owner decisions, the manager's assignments, and the public REVIEW READY comments (A215, then A226 for this round).
3. REQUIREMENTS.md (REQ-PTP-05/06/09), FR_NFR.md, the compliance matrix, the feature-status ledger and the traceability page.
4. The texts of IEEE 802.1AS-2011, Cor1-2013, Cor2-2015 and 802.1AS-2020, and Milan v1.2 (2023-11-30). I read these from local licensed copies, not through any excerpt.
5. `git diff 759da623..70f2c50d`, the round diff `64bcf768..70f2c50d`, and the history.
6. The pinned processors: gPTP processor `c1b6174`, protocol processor `424c688`.
7. Public evidence at `9c71d05f` (`review-evidence/394_510_511-r1`): the correction-round receipts. I did not open the author handoff files. I opened the prior review packets only after my verdict.
8. The exact-head hosted check runs.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head, and all five lenses are covered clean at the exact head.

This round's two MINORs were R274-1 F1/F2, which are the same findings as R275-1 F1/F2. Both are resolved. I verified each fix against the standard's own text:

**F1: every place delayAsymmetry enters the arithmetic.** `docs/design/GPTP_PLANE.md:378-394` names all three terms, and every row matches the 2011 text:

- 11.2.13.2.1 f): `upstreamTxTime` subtracts `delayAsymmetry/rateRatio`.
- Figure 10-9: `syncReceiptTime` gains `+delayAsymmetry`.
- Figure 10-9: `syncReceiptLocalTime` gains `+delayAsymmetry/rateRatio`.

The rest of the table also holds:

- **Carriage:** 11.2.14.2.3 a) carries the first term into a relayed Follow_Up, and only between ports (10.2.11 `localPortNumber != thisPort`).
- **CSN:** Annex E.5.2.2 takes the inputs from the CSN TLV.
- **Net effect:** the `rateRatio` difference is exactly the Figure 10-4 `rateRatio += (neighborRateRatio - 1.0)` update. NOTE 2 of 11.2.13.2.1 calls that difference negligible.
- **Doubling claim:** "omitting the `syncReceiptLocalTime` term roughly doubles the shift" follows from that arithmetic.
- **Corrigenda:** Cor1 restates f) unchanged and does not touch Figure 10-9. Cor2 changes only Figure 11-8.
- **Completeness:** a map of every 2011 occurrence of `delayAsymmetry` to its clause shows no other arithmetic site. The rest are definitions, descriptive text (11.1.3, Table 11-5, 11.2.5), management and MIB text, and CSN.
- **Row and plan:** the "Where would it enter?" row (`:359`) and the adoption "Application point" (`:422`) were corrected to match.

**F2: Table 14-6 and the management condition.** The "Is it managed?" row (`GPTP_PLANE.md:360`) matches the 2011 Table 14-6 at 14.6.25, and the Cor1 replacement keeps the row:

- `scaledNs (recommended)`, `RW`, `Tdot3FD`.
- The legend reads "Tdot3FD = Required for time-aware IEEE 802.3 full-duplex port".
- The 14.3.2 analogue ("It is recommended that the data type be scaledNs") holds.
- 14.6.9 carries no grade.
- A.5 `MGT` is `O`.

The management revisit condition is present in the record (`:402-410`), in REQUIREMENTS.md (`:141-146`), in the FR_NFR out-of-scope entry (`:421-424`) and in the compliance-matrix row (`:226`). Every other #511 surface defers to the record instead of restating the trigger.

## Findings

Every finding below is a SUGGESTION: optional, with no effect on coverage or the verdict.

### R274-2-S1: SUGGESTION. Lenses: Conformance, Docs. PICS `MGT` is worded for Bridges

- **Where:** `docs/design/GPTP_PLANE.md:360` ("Management is optional: PICS item `MGT` (A.5) is `O`"), and `docs/reference/MILAN_COMPLIANCE_MATRIX.md:226` ("management is optional (PICS `MGT`)").
- **Authority and evidence:** 802.1AS-2011 A.5 `MGT` reads "Is management of the timing synchronization in Bridges supported?", status `O`, reference Clause 15 (`receipts/clause_check.txt`).
  - For an end station, optionality follows from two further facts. Clause 5.3 and 5.3.1 list no Clause 14 or 15 requirement. Annex A (A.1 to A.17) has no management item group.
- **Impact:** None on the conclusion, which is correct. The citation alone is narrower than the product it is applied to.
- **Outcome (optional):** Cite 5.3 and 5.3.1 next to `MGT`, or note that `MGT`'s wording names Bridges.
- **Verification:** Re-read against A.5 and 5.3.

### R274-2-S2: SUGGESTION. Lens: Docs. The existing AS-11 range overlaps the new AS-13

- **Where:** `docs/traceability/ieee8021as.md:47`, the existing AS-11 row "12-16 Non-Ethernet media layers, Not applicable", and `:49`, the new AS-13 row "8.3, 10.2.4.8, 14.6.9, Excluded".
- **Authority and evidence:**
  - Clause 14 is timing and synchronization management and Clause 15 is managed object definitions, in both the 2011 and 2020 editions. In 2020, CSN is Clause 16. In 2011, CSN is Annex E.
  - So 14.6.9 sits inside a range AS-11 marks Not applicable, while AS-13 marks it Excluded.
  - The record's own "(AS-11)" citation for CSN (`GPTP_PLANE.md:389`) depends on the 2020 numbering.
  - The compliance matrix (`MILAN_COMPLIANCE_MATRIX.md:215-220`) calls this page the 2020 cross-trace, but AS-13 uses 2011 numbers. That part overlaps R275-1-S4.
- **Impact:** A cold reader can find two different states for clause 14.6.9. AS-11 predates this PR.
- **Outcome (optional):** File a follow-up Issue to narrow AS-11 to the media clauses and to label the clause editions. Per AGENTS.md section 4, this is not an expansion of this lane.
- **Verification:** Re-read the traceability page at the follow-up head.

### R274-2-S3: SUGGESTION. Lenses: Conformance, Docs. PICS MINTA-8 is the conformance-statement basis for optional modelling

- **Where:** `docs/design/GPTP_PLANE.md:358` and `docs/reference/MILAN_COMPLIANCE_MATRIX.md:226`. Both cite 8.3 alone.
- **Authority and evidence:** 802.1AS-2011 A.7 MINTA-8, "If path delay asymmetry is modeled by this device does it comply with the requirements of 8.3?", has status `O` (`receipts/clause_check.txt`).
- **Impact:** None. 8.3 already says measurement is not required.
- **Outcome (optional):** Add MINTA-8 beside 8.3.
- **Verification:** Re-read against A.7.

### R274-2-S4: SUGGESTION. Lens: Docs. The 2020 comparison row summarises CMLDS

- **Where:** `docs/design/GPTP_PLANE.md:390`, which reads "With CMLDS, 11.2.17.2 a) folds it into the mean link delay".
- **Authority and evidence:** 802.1AS-2020 11.2.17.2 b) and f) show two further entry points when CMLDS is used:
  - the Pdelay_Req `correctionField` is set to minus delayAsymmetry (11.2.19.3.1 c) 2));
  - `computePdelayRateRatio()` adds delayAsymmetry (11.2.19.3.3 b) 4)).
- **Impact:** None for the edition of record. The row is labelled a comparison, and it points to 11.2.17.2, which lists both.
- **Outcome (optional):** Cite 11.2.17.2 as a whole, or add b) and f).
- **Verification:** Re-read against 11.2.17.2.

### R274-2-S5: SUGGESTION. Lens: Tests. The pinned pp_top has no per-command arm for the unserved MVU commands

- **Where:** `protocol-processor` `424c688`, `tb/pp_top/sim_main.cpp:2330-2340`: M4 grades 0x0002 only. The limit is disclosed at `docs/reference/MILAN_COMPLIANCE_MATRIX.md:137` as "no per-command PP arm yet".
- **Authority and evidence:** In a scratch export of the pinned bytes, a decode mutant that serves 0x0003 as GET_MILAN_INFO passes all 1371 pinned checks. Only this round's added 0x0003 arms catch it: 1383/1385, and the 2 FAILs are both 0x0003 arms (`receipts/pp_top_mutant.log`, `receipts/pp_probe_mutant.diff`).
- **Impact:** The PR's claim is honest and true at the pin: all seven arms pass (`receipts/pp_top_arms.log`). The regression gap belongs to the processor.
- **Outcome (optional):** Forward the arms (`receipts/pp_probe_arms.diff`) to processor issues 55, 56 and 77.
- **Verification:** A committed processor check fails under the mutant.

## Per-lens results

```text
[R274] PASS Conformance - docs/design/GPTP_PLANE.md:348-455, REQUIREMENTS.md:48, :130-148 and :256-279, docs/reference/FR_NFR.md:31,88-92,149,194-195,228-236,297,392-424,435,443-444, docs/reference/MILAN_COMPLIANCE_MATRIX.md:34,136-137,183,226, docs/MILAN_V12_ROADMAP.md:470-475, docs/traceability/ieee8021as.md:29,49,64,77 at 70f2c50d - checked against local 802.1AS-2011, Cor1-2013, Cor2-2015 and 2020 and Milan v1.2 texts by scripts/check_clauses.py (0 failures, receipts/clause_check.txt): 8.3 sign and non-requirement, 10.2.4.8 zero and no data type, Figure 10-9 both assignments, Figure 10-4, 11.1.3 d)/e), 11.2.13.2.1 f) and NOTE 2, 11.2.14.2.3 a), 10.2.11, Table 11-5, 11.2.15/11.2.15.2.4 (no asymmetry term), 14.6.9, Table 14-6 row and legend (2011 and Cor1), 14.3.2, A.5 MGT, A.7 MINTA-8, E.5.2.2, 2020 10.2.13/11.2.14.2.1/11.2.15.2.3/11.2.17.2 a); Milan 4.2.5, 4.2.6, Tables 5.18-5.20, the five recommendation notes, 8.1, 8.3.1, no asymmetry text; donor citations (issue 58 "802.1AS-2011 11.2.15", prototype pages "10.2.4.5") correctly corrected; FR-MVU-02 M->S equals the #510 decision; no other requirement weakened; #511 acceptance 1-5 met; #394/#510 partial status stated honestly (Relates, not Closes)
[R274] PASS RTL - diff 759da623..70f2c50d (11 *.md, 0 gitlink or mode changes) and every RTL fact the text relies on - parent hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:115-116,345 and KL_gptp_txret.sv:276-283 (ingress subtracted, egress added through TXTS_NET_NS_C, once), docs/reference/REGISTER_MAP.md:1392 (GPTP_LAT 0x7F0), sw/builder/endstation_builder.py:3940-3948 (no asymmetry key), sw/litex/milan_soc.py:3632 (one --eth-port); gptp-processor c1b6174 has no asymmetry text outside docs/history/v1/prototype (the one other hit is base64 image data in docs/diagrams/gptp_architecture.svg); protocol-processor 424c688 hdl/aecp/KL_aecp_engine.sv:1290-1296 with banner :160-171 (only command_type 0x0000 leaves the NOT_IMPLEMENTED echo), hdl/aecp/ucode/gen_ucode.py:112 (features_flags 0), hdl/top/protocol_processor_top.sv:1594 (.N_IF_P(1)); no P-EN-MVU parameter exists in hdl
[R274] PASS Robustness - scripts/probe_builder_asym_refusal.py on scratch copies of configs/endstation_ax7101_1x1_tdm8.yaml (control loads; gptp.delay_asymmetry_ns=100, delayAsymmetry=-100, asymmetry_ns=0, delay_asymmetry=1 each refused naming the key; receipts/probe_builder_asym_refusal.txt) and the MVU fallback in pinned pp_top for 0x0001 (8/12 B), 0x0002 (12 B), 0x0003 (8/80 B), 0x0004 (8/12 B): byte-exact NOT_IMPLEMENTED echo each (receipts/pp_top_arms.log, 1385/1385); adoption plan GPTP_PLANE.md:412-439 covers zero, both signs, limits, reset/update, double correction and configuration-to-engine; the omitted-term failure mode (:394) is caught by the magnitude arm (:433)
[R274] PASS Tests - no test or gate file changed; 27 documentation gate and self-test runs exit 0 at the head (receipts/gates/gates_summary.txt: docs_check 0/164 md+848, em-dash 0 over 230 and 40 added lines, feature_status, TOC/anchors 154, doc paths 832, gPTP docs 8 pages and 30 controls, style 22, submodule, solution 43 controls, wire accountability, diagrams, baremetal 377 arms, module matrix 69); pp_top at the pinned bytes under Verilator 5.050 rev v5.050 (receipts/verilator_identity.txt) with 7 probe arms 1385/1385, and a decode mutant caught by the two 0x0003 arms (1383/1385), so the arms can fail; the adoption proof plan is byte-identical to 64bcf768 (sha256 5efb6309..., receipts/proof_plan_*.md) and each arm names a failing condition
[R274] PASS Docs - all 11 changed pages at 70f2c50d and the 4 round pages - new heading #where-the-term-enters unique at GPTP_PLANE.md:378, #propagation-asymmetry-is-not-modelled at :348; 20 owner-decision links each pair with their own A10 decision comment (receipts/decision_links.txt); donor and processor issues and #64/#110/#416/#417/#488 resolve and match their use (receipts/external_issue_links.txt); no stale phrasing ("both terms", "lists it read-write and recommended" absent); the trigger is restated in exactly four places, all with the management condition, and the rest defer to the record; README roadmap line lengths identical to the base (columns preserved); the A215 statements superseded by the A226 comment on #511; commits one line with no trailers
```

## Prior public review findings

My verdict and ledger were written and hashed before I read any other reviewer's work (`receipts/independent_verdict_before_prior_findings.md`, 2026-09-24T03:42:44Z, sha256 `c31a1902...b7a1`). I then read R274-1 (issuecomment-5805065861) and R275-1 (issuecomment-5805241709). The PR has no review objects. The only later comment is the manager's R275-2 start notice.

| Prior finding | Severity; lenses | State at 70f2c50d | Evidence |
|---|---|---|---|
| R274-1 F1 = R275-1-F1 | MINOR; Conformance, Docs | RESOLVED | `GPTP_PLANE.md:359,378-394,422`; clause check |
| R274-1 F2 = R275-1-F2 (supersedes R275-1's independent S1) | MINOR; Conformance, Docs | RESOLVED | `GPTP_PLANE.md:360,402-410,418`; `REQUIREMENTS.md:141-146`; `FR_NFR.md:421-424`; matrix `:226` |
| R274-1 S1 = R275-1-S3 | SUGGESTION; Tests | RETAINED (optional, not taken) | No committed builder test plants an asymmetry key. The probe shows the refusal works |
| R275-1-S2 | SUGGESTION; Tests, Docs | RETAINED (optional, not taken) | `scripts/check_gptp_docs.py:15,74` still `range(1, 13)`, so AS-13 is ungated |
| R275-1-S4 | SUGGESTION; Docs, Conformance | RETAINED (optional, not taken) | `ieee8021as.md:49` names no clause edition. See also R274-2-S2 |

Details are in `receipts/prior_findings_resolution.txt`. Nothing in the prior rounds changes this round's independent verdict.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Every clause the 11 pages cite, checked against the 802.1AS-2011/Cor1/Cor2/2020 and Milan v1.2 texts (`receipts/clause_check.txt`); FR-MVU-01..03, NFR-SCOUT-05, FR-CLK-01, REQ-PTP-06 levels; #511 acceptance 1-5; #394/#510 partial status | R274-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |
| RTL | CLEAN | Diff file list, modes and gitlinks; `KL_gptp_shadow.sv:115-116,345`; `KL_gptp_txret.sv:276-283`; `REGISTER_MAP.md:1392`; builder `:3940-3948`; `milan_soc.py:3632`; gptp-processor `c1b6174` tree; protocol processor `KL_aecp_engine.sv:160-171,1290-1296`, `gen_ucode.py:112`, `protocol_processor_top.sv:1594` | R274-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |
| Robustness | CLEAN | Builder refusal probe (control plus 4 keys); MVU fallback probe, 7 arms including the 80-byte SET_MEDIA_CLOCK_REFERENCE_INFO; adoption plan `GPTP_PLANE.md:412-439` negative, boundary, reset and double-correction arms | R274-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |
| Tests | CLEAN | 27 documentation gate and self-test runs; pp_top 1385/1385 with arms, mutant caught 2/2; proof plan byte-identity with `64bcf768`; builder probe control | R274-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |
| Docs | CLEAN | All 11 pages; anchors; 20 decision links; external links; stale-phrase sweep; trigger restatements; roadmap alignment; commit messages; A226 public corrections | R274-2 | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |

This is the internal review. The two-positive bar also needs the external round R275-2, which is in flight at this head.

## Evidence in this packet

Every file listed in `MANIFEST.sha256` is published with this report. Absolute local paths are redacted to `<packet>`, `<clone>`, `<scoped-verilator>` and `<scoped-verilator-root>`. The standards directory is passed as an argument (`$STANDARDS_DIR`).

- **Diffs:** `receipts/full_diff_759da623..70f2c50d.patch` and `receipts/round_diff_64bcf768..70f2c50d.patch`.
- **Clause check:** `scripts/check_clauses.py` produced `receipts/clause_check.txt`. It converts the local PDFs, records their sha256, echoes only short fragments with line numbers, and ends with the per-occurrence clause map.
- **Documentation gates:** `scripts/run_doc_gates.sh` produced `receipts/gates/*`: 27 runs, all exit 0.
- **Builder probe:** `scripts/probe_builder_asym_refusal.py` produced `receipts/probe_builder_asym_refusal.txt`. It loads the builder in-process on scratch configs and writes nothing to the clone.
- **Processor probe:** `scripts/patch_pp_mvu_probe.py` and `scripts/run_pp_top.sh` ran on `git archive` exports of `424c688` in scratch, with builds capped at 8 jobs.
  - Patches: `receipts/pp_probe_arms.diff` and `receipts/pp_probe_mutant.diff`.
  - Runs: `receipts/pp_top_arms.log` (1385/1385) and `receipts/pp_top_mutant.log` (1383/1385).
  - `receipts/verilator_identity.txt`: the Verilator 5.050 wrapper and binary hashes.
- **Proof plan:** `receipts/proof_plan_64bcf768.md` and `receipts/proof_plan_70f2c50d.md` are byte-identical.
- **Links:** `receipts/decision_links.txt` and `receipts/external_issue_links.txt`.
- **Hosted runs:** `receipts/hosted_check_runs.tsv` and `receipts/hosted_status.txt`.
- **Live dev:** `receipts/live_dev_drift_files.txt` and `receipts/dry_merge_live_dev.txt`.
- **Review ordering:** `receipts/independent_verdict_before_prior_findings.md` with its `.timestamp`, and `receipts/prior_findings_resolution.txt`.
- **Commits:** `receipts/commit_messages.txt`.
- **Clone state:** `scripts/tree_state.sh` produced `receipts/tree_state_final.txt`. It shows:
  - HEAD, tree and write-tree all equal the exact head and tree;
  - the index equals HEAD;
  - 872 tracked blobs rehashed with their modes, 0 mismatches;
  - 0 assume-unchanged or skip-worktree flags;
  - 0 untracked and 0 ignored files;
  - `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` checked out at their gitlinks and clean.

  A documentation self-test wrote an ignored `scripts/__pycache__/` during this round. It was removed before the final state was taken. `external` is uninitialised, as it was at the start, and no gate reads it.

## Real limits

- **Not run here:** the full parent, processor, gPTP, Yosys and builder banks (including `sw/builder/test_builder.py`), Docker/act, the host act runner and its self-test, and hardware.
- **Manager bank evidence:** the round brief states that the manager's source static/builder and native banks passed at this head. The cited tree `9c71d05f` holds the author, correction-round and prior-review packets, but I found no separate manager bank receipt for `70f2c50d` there. The author's public gate receipt at this head matches my own gate results.
- **Physical calibration is NOT RUN.** The #394 bench proof is not attempted. Field skips are not hardware proof.
- **Hosted, exact head:** 8 contexts executed and succeeded: `bdd-conformance`, `changes`, `docs-check`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `rtl-fast` (an aggregator: "Require every applicable fast gate to pass") and `wire-accountability`.
  - 7 contexts were skipped: `verilator-suites`, `yosys-portability`, their shard matrices, `verilator-lint`, `yosys-elaboration` and Physical gPTP. The PR is docs-only, and `full-ci-gate` selected the no-op path.
  - A skipped context is not executed evidence. The legacy combined status reads `pending` with zero statuses.
- **The processor probe is scratch-only:** it is evidence for this round, not a committed regression.
- **Standards readings** come from `pdftotext -layout` extractions of local copies. PDF hashes are in `receipts/clause_check.txt`.
- **The dry merge onto live dev is textual only:** a `git merge-tree` in a disposable `--shared` clone. It is not a gated candidate.

## Pending manager duties

1. **External review:** R275-2 is in flight at this head. The merge waits for it and for the two-positive bar.
2. **Candidate merge:** build and gate the candidate against live `dev` `50e78097564244c124e1ec30dd8821f83951ab06` with the full local bar.
   - Live dev is 14 commits ahead of the base, and 4 of this PR's pages also change there: ROADMAP, TIME_SYNC, FR_NFR and the compliance matrix.
   - Live dev's hunks in those pages concern the CRF counters (#529) and the grid aligner, not the #394/#510/#511 rows.
   - The textual merge-tree is clean (tree `348267ed0ccdf364f4e81bbd9ffe1939126f33c9`).
3. **Hosted and act acceptance** on the exact head, then post-merge containment, then moving #511 to Done.
4. **Revisit trigger:** obtain owner confirmation or replacement of the #511 revisit trigger. The executor derived it from the decision's two grounds plus the Table 14-6 management condition, and asked about it publicly on #511.
5. **Open issues:** keep #394 open for the bench proof (#117, #75). Keep #510 open for processor F01.5 (issue 77) and committed per-command checks (issues 55, 56). `receipts/pp_top_arms.log` and `receipts/pp_top_mutant.log` are available as supplementary pin evidence.
6. **Out-of-diff item:** file the item that earlier rounds carried, if not already filed. `tests/features/aecp_response_contract.feature` sends GET_MILAN_INFO (0x0000) through the offline model and asserts `NOT_IMPLEMENTED`, but the pinned engine serves that command (pp_top M1).
7. **Bank receipts:** publish, or point to, the manager's own bank receipts for `70f2c50d`.
8. **Optional follow-ups:** consider R274-2-S1 to S5 and the retained R274-1 S1, R275-1-S2 and R275-1-S4. S2's AS-11 range is a candidate follow-up Issue.

R274-2 FINISHED
