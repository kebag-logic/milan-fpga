[R274] NEGATIVE - exact head 64bcf768d28b4b9763fbe5917a734bcefa2a66e0

Round R274-1. Internal cleared-context review of PR #537 (Closes #511; Relates to #394 and #510).

- Head `64bcf768d28b4b9763fbe5917a734bcefa2a66e0`, tree `8027683077254647a146b13ebd9c5434432858b3`.
- Source base `759da623072358afdb0e9d570a7b4b6a788492c9`.
- Six one-line commits, no trailers.
- Eleven Markdown files changed, +199/-26.
- No RTL, firmware, builder, configuration, test or gitlink change (`receipts/rtl_lens_checks.txt`).

Reconstructed from, in this order:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. The bodies of #394, #510 and #511, and their comments: the owner decisions of 2026-09-23, the assignment and the executor's REVIEW READY.
3. REQUIREMENTS.md, FR_NFR.md and the compliance matrix.
4. The Milan v1.2 (2023-11-30) and IEEE 802.1AS-2011 texts, with Cor1-2013 and Cor2-2015.
5. The diff and its history.
6. The public evidence packet at `9fc8ebe3` (`review-evidence/394_510_511-r1`).
7. The exact-head hosted check runs.

## Verdict

**NEGATIVE.** Two MINOR findings are open, F1 and F2. Both fall under Conformance and Docs. Both sit in the #511 design record, and #511 is the issue this PR closes.

The #394 and #510 records are accurate and complete at this head. RTL, Robustness and Tests are covered clean. The fixes are small prose corrections in `docs/design/GPTP_PLANE.md`, plus one clause in the REQUIREMENTS.md scope note.

## Findings

### F1: MINOR. Lenses: Conformance, Docs. The record omits one of the three places where delayAsymmetry enters the arithmetic

- **Where:** `docs/design/GPTP_PLANE.md:359`, the "Where would it enter?" row. It reads: "ClockSlaveSync `syncReceiptTime` and `setMDSyncReceive()` `upstreamTxTime`. At zero both terms vanish."
- **Authority and evidence:** IEEE 802.1AS-2011 10.2.12, Figure 10-9. No corrigendum replaces this figure (Cor1/Cor2 contain no hit for it).
  - The figure adds delayAsymmetry in two assignments: `syncReceiptTime = ... + delayAsymmetry;` and `syncReceiptLocalTime = rcvdPSSyncPtr->upstreamTxTime + neighborPropDelay/neighborRateRatio + delayAsymmetry/rcvdPSSyncPtr->rateRatio;`.
  - 11.2.13.2.1 f) subtracts `delayAsymmetry/rateRatio` from `upstreamTxTime`.
  - That makes three terms, not two. See `receipts/standards_clause_receipts.txt`, extraction lines 4614-4617 and 7397-7399.
  - The executor's #511 REVIEW READY comment repeats the omission: "it enters only 10.2.12 `syncReceiptTime` and 11.2.13.2.1 `upstreamTxTime`".
- **Impact:** The v1.2 behavior does not change, because the value is zero.
  - This row is the record's statement of the arithmetic an adoption must reproduce. #511 asks that "the applicable management/arithmetic clauses" be verified, and acceptance 3 asks for "exact arithmetic/sign discrimination".
  - Suppose an adoption applies only the two named terms and omits the `syncReceiptLocalTime` term, which restores what `upstreamTxTime` subtracted. Then `syncReceiptLocalTime` ends up short by delayAsymmetry/rateRatio. The synchronized offset then moves by about twice the configured value.
  - The plan's "Positive and negative" arm (`GPTP_PLANE.md:407`) would catch that later. So the defect lies in the record's reading of the standard, not in the proof plan.
- **Required outcome:** The row names all three terms at the cited clauses, or it states the clause-level point in an equivalent way:
  - 10.2.12 applies the term to both `syncReceiptTime` and `syncReceiptLocalTime`.
  - The second cancels the 11.2.13.2.1 subtraction.
  - So the net effect is +delayAsymmetry on `syncReceiptTime`.
  - "Both terms" is corrected.
- **Verification:** A reviewer re-reads `GPTP_PLANE.md` at the fix head against Figure 10-9 and 11.2.13.2.1 f).

### F2: MINOR. Lenses: Conformance, Docs. The management row misstates Table 14-6, and the revisit trigger omits the management condition

- **Where:**
  - `docs/design/GPTP_PLANE.md:360`, which reads: "IEEE 802.1AS-2011 14.6.9 lists it read-write and recommended".
  - The revisit trigger at `docs/design/GPTP_PLANE.md:378-384` and `REQUIREMENTS.md:141-143`.
  - The executor's #511 REVIEW READY comment repeats the claim: "14.6.9 is a recommended RW object".
- **Authority and evidence:**
  - 14.6.9 defines the object and does not grade it.
  - Table 14-6 (14.6.25) grades it. The Cor1 replacement is identical for this row: Operations `RW`, Conformance `Tdot3FD`. The legend reads "Tdot3FD = Required for time-aware IEEE 802.3 full-duplex port".
  - "(recommended)" is an annotation in the Data type column. `neighborPropDelay` and `neighborPropDelayThresh` carry the same annotation, and their Conformance is `T` (required). So it cannot mean that the object is recommended.
  - Management as a whole is optional: Annex A PICS item `MGT` is `O`.
  - See `receipts/standards_clause_receipts.txt`: 2011 extraction lines 11200-11205, 11223-11226 and 15166; Cor1 lines 2663-2666.
- **Impact:** The exclusion still holds, because the product claims no 802.1AS management and exposes no Clause 14/15 surface.
  - The record states the wrong conformance grade, in the very row #511 asked to verify.
  - The revisit trigger ("a second cabled port"; "a REQ-PTP-06 amendment") misses a real re-entry path. If the product ever claims 802.1AS management, for example for the P4 802.1AS conformance run, Table 14-6 makes a read-write delayAsymmetry object required on its 802.3 full-duplex port. A reader relying on "recommended" would not see that.
- **Required outcome:**
  - The row states Table 14-6 accurately: RW; required (`Tdot3FD`) on a time-aware IEEE 802.3 full-duplex port where 802.1AS management is supported; management optional (PICS `MGT` = O); none claimed by this product.
  - The revisit trigger adds "claiming 802.1AS management" in the GPTP_PLANE record and the REQUIREMENTS.md scope note, or states why that cannot arise.
  - Optional: `GPTP_PLANE.md:392` ("Units: scaledNs ... (10.2.4.8, 14.6.9)") can cite Table 14-6 for `scaledNs`, since the 2011 text of 10.2.4.8 gives no data type.
- **Verification:** A reviewer re-reads at the fix head against Table 14-6, its legend and PICS `MGT`.

Neither finding is attributed to the other three lenses:

- **RTL:** no RTL changed, and no RTL claim is wrong.
- **Robustness:** no product behavior or configuration path depends on either finding. The builder refuses every asymmetry key (probe below).
- **Tests:** the adoption proof plan's positive/negative arm detects F1's error, and F2 concerns no test.

### S1: SUGGESTION. Lens: Tests. Grade the configuration half of the exclusion

`_known_gp` (`sw/builder/endstation_builder.py:3940-3948`) refuses every unknown `gptp` key. The reviewer probe shows it refuses four asymmetry spellings, and a positive control shows the probe can pass. No committed builder test plants such a key; the executor raised the same point.

This is optional. It does not affect coverage.

## Per-lens results

These use the AGENTS.md section 6 format, with ` - ` as the separator.

```text
[R274] PASS RTL - diff 759da623..64bcf768 (11 files, all *.md, 0 gitlink changes; receipts/rtl_lens_checks.txt) and the pinned RTL the new text cites - no RTL change and no RTL claim false: protocol-processor 424c688 hdl/aecp/KL_aecp_engine.sv:1287-1293 (only command_type 0x0000 with the Milan protocol_id and an 8-byte payload takes the GET_MILAN_INFO arm; banner :166-170 echoes everything else NOT_IMPLEMENTED), hdl/aecp/ucode/gen_ucode.py:112 (features_flags 0), hdl/top/protocol_processor_top.sv:1594 (.N_IF_P(1)); parent hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:345 and :986 with KL_gptp_txret.sv:283 (the two REQ-PTP-06 constants applied once, inside the shadow hierarchy); gptp-processor c1b6174 has no asymmetry input (receipts/asym_grep.txt: 0 hits outside docs/history and one base64 SVG blob); sw/litex/milan_soc.py:3632 (one --eth-port e1|e2)
[R274] PASS Robustness - sw/builder/endstation_builder.py:3940-3948 driven by scripts/probe_builder_asym_key.py (the unmodified shipping config loads; gptp.delay_asymmetry, delay_asymmetry_ns, asymmetry_ns and delayAsymmetry are each refused naming the key; receipts/probe_builder_asym_key.txt) and the MVU fallback under every unserved command type at its Milan Figure 5.5/5.6/5.7 length, including the largest (SET_MEDIA_CLOCK_REFERENCE_INFO, 80 payload bytes; KL_aecp_engine.sv:804-805 gives PLD_MAX 580 at LINE_BYTES_P 576): byte-exact NOT_IMPLEMENTED echo, counters move once per command, M2 features_flags 0 in the same run (receipts/probe_pp_mvu_run.txt)
[R274] PASS Tests - no test file changed; the checks the new text cites (pp_top M1, M2, M4) executed at the exact pinned bytes (git archive of 424c688; blob 97f31bc2 verified) under Verilator 5.050 rev v5.050: 1382 checks, 1382 PASS = 1371 pinned + 11 probe; the probe can fail (flipped-byte and SUCCESS-status negative controls DETECTED; receipts/probe_pp_mvu_run.txt, receipts/probe_pp_mvu_patch.diff); the adoption proof plan GPTP_PLANE.md:400-411 has arms that fail for the defect each names (zero trajectory, sign-swap mutation, limits, reset/update, neighborPropDelay invariance, I/E constants unchanged, configuration to engine); 14 documentation gates exit 0 at the head (receipts/doc_gates.txt)
```

**Conformance is UNCLEAN**, because of F1 and F2. Everything else under this lens was checked and found clean:

- Milan v1.2:
  - 4.2.5 and 8.1: redundancy is optional.
  - 4.2.6.
  - 5.4.4.1 with Table 5.20: bit 31 is REDUNDANCY.
  - The recommendation note appears in all five places cited: 5.4.4.2, .3, .4, .5 and 7.6.
  - Table 5.18 and Table 5.19: `NOT_IMPLEMENTED` = 1.
  - 8.3.1: at least two AVB-capable ports.
  - Zero mentions of asymmetry.
- 802.1AS-2011:
  - 8.3: sign convention; measurement not required.
  - 8.4.3.
  - 10.2.4.5 is `syncInterval`, and 10.2.4.8 is delayAsymmetry (unmodelled means zero).
  - 11.2.15 is MDPdelayReq, and 11.2.15.2.4's Equation 11-5 has no asymmetry term.
- FR-MVU-02 moves M to S. That is exactly the decision, since RFC 2119 SHOULD = RECOMMENDED. No other requirement is weakened: FR-MVU-03 stays M/I, NFR-SCOUT-05 stays S/A,D, and the REQ-PTP-06 text is unchanged.
- The donor citation corrections are right. Donor issue 58 cites 11.2.15, and the prototype pages cite 10.2.4.5 (`BENCH_OPERATIONS.md:117`, `MGMT_INTERFACE.md:54`).

**Docs is UNCLEAN**, because of F1 and F2. Everything else under this lens was checked and found clean:

- Every #394 and #510 surface listed below.
- All 9 new relative links and anchors resolve (`receipts/added_links.txt`).
- All 7 new external links resolve: the three owner-decision comments, donor issue 58, and processor issues 55, 56 and 77 (`receipts/external_links.txt`).
- The em-dash, style, TOC, anchor, path, feature-status, gPTP-docs and submodule-docs gates are green.
- The commits are one line each, with no trailers (`receipts/commit_history.txt`).
- The feature-status ledger has no redundancy or asymmetry feature ID, so it needs no entry for #394 or #511. The only traceability page covering these features is `ieee8021as.md`.

## Decision-by-decision check

| Decision | Recorded at the head | Clause | Revisit trigger | Result |
|---|---|---|---|---|
| #394: non-redundant end station | `README.md:329-337`; `REQUIREMENTS.md:48,262-270`; `FR_NFR.md:31,149,195,297,392-394,406-415,441`; compliance matrix `:34,:183`; roadmap `:474` | Milan v1.2 4.2.5, 5.4.4.1/Table 5.20, 8.1, 8.3.1 | P4/P5 PCB (#416/#417) | Accurate; all four acceptance-1 surfaces change in `909d8feb` |
| #510: MVU rows RECOMMENDED | `FR_NFR.md:88-92,149,194,433`; compliance matrix `:136-137`; roadmap `:470-471`; feature status `:120-127`; `SUBMODULES.md:111` | Milan v1.2 5.4.4.2-.5, 7.6, Table 5.19 | P4 (#416) if the lab requires; processor issues 55/56 | Accurate. The fallback claim for 0x0001/0x0003/0x0004 is true at the pin (reviewer probe) |
| #511: no delayAsymmetry; UART tuner donor-bench-only | `GPTP_PLANE.md:348-428`; `REQUIREMENTS.md:130-145,272-276`; `FR_NFR.md:31,228-236,416-422,442`; compliance matrix `:226`; roadmap `:475`; `ieee8021as.md:29,49,64,77`; `TIME_SYNC.md:63`; `MANAGER.md:34` | 802.1AS-2011 8.3 and 10.2.4.8 exact; 14.6.9 grade wrong (F2); arithmetic incomplete (F1) | Second cabled port; REQ-PTP-06 amendment. Incomplete (F2) | F1 and F2 open |

The partial-close reasons are accurate:

- **#394 stays open:** acceptance 2, the ten-cycle `e1` bench proof and the `--eth-port e2` repeat, needs hardware and is unmet. Acceptance 4's intermediate commits without a `test_builder` run are inert for it: the builder and its test read none of the eleven changed pages, and the test only rglobs `hdl/*.sv`.
- **#510 stays open:**
  - At the pin, `docs/architecture/01_overview.md:169` still lists `P-EN-MVU-SUID / P-EN-MVU-MCR | 1 / 1`, and no HDL parameter exists (`receipts/pp_pin_claims.txt`).
  - Only 0x0002 has a committed byte-exact check (pp_top M4).
  - The reviewer probe adds byte-exact evidence for 0x0001, 0x0003 and 0x0004 at the pin (`receipts/probe_pp_mvu_run.txt`). It is scratch-only, not a committed regression.
- **#511's "Closes" is not yet earned:** F1 and F2 fall under its acceptance 1 to 3. Those ask for a clause-backed, verified management/arithmetic contract.

## Prior public review findings

The PR thread was read at the start of this round, before the independent pass. It held three manager round-start comments, no review objects and no inline review comments. So there was no prior finding to resolve or retain at this head.

The thread was re-checked after this verdict and ledger were written. The result is in the addendum at the end of this report.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Milan v1.2 and 802.1AS-2011 (+Cor1/Cor2) clauses cited by all 11 pages; FR-MVU-02/03, NFR-SCOUT-05 and REQ-PTP-06 levels | R274-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |
| RTL | CLEAN | Diff file list and gitlinks; `KL_aecp_engine.sv:1287-1293,804-805`; `gen_ucode.py:112`; `protocol_processor_top.sv:1594`; `KL_gptp_shadow.sv:345,986`; `KL_gptp_txret.sv:283`; gptp-processor `c1b6174` ports; `milan_soc.py:3632` | R274-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |
| Robustness | CLEAN | Builder `_known_gp` refusal probe (4 keys plus a positive control); MVU fallback probe for 0x0001/0x0003/0x0004 at the Milan payload lengths, counters and M2 | R274-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |
| Tests | CLEAN | pp_top at pinned bytes (1382/1382), probe negative controls, adoption proof-plan arms (`GPTP_PLANE.md:400-411`), 14 documentation gates | R274-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |
| Docs | UNCLEAN (F1, F2) | All 11 changed pages; new links and anchors; external links; em-dash/style/TOC/path gates; commit messages; issue and PR partial-close text | R274-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |

The fix for F1 and F2 must be re-reviewed at its head under Conformance and Docs. RTL and Robustness stay covered unless the fix touches files in their scope. Tests must be re-covered if the fix changes the adoption proof plan (`GPTP_PLANE.md:400-411`).

## Evidence in this packet

Every file listed in `MANIFEST.sha256` is published with this report. Absolute paths are redacted to `$PACKET`, `$CLONE`, `$PINNED_TOOL_BIN` and `$HOME`.

- `scripts/run_doc_gates.sh` produced `receipts/doc_gates.txt`: 14 read-only documentation gates at the head, all exit 0.
- `scripts/check_added_links.py` produced `receipts/added_links.txt`.
- `receipts/external_links.txt`: read-only fetches of every external issue and decision comment the PR cites.
- `scripts/probe_builder_asym_key.py` produced `receipts/probe_builder_asym_key.txt`. It loads the builder in-process on scratch copies of the shipping config and writes nothing to the clone.
- `scripts/probe_pp_mvu_fallback.sh` and `scripts/patch_pp_mvu_probe.py` produced these receipts:
  - `receipts/probe_pp_mvu_extract.txt`
  - `receipts/probe_pp_mvu_gen.txt`
  - `receipts/probe_pp_mvu_build.txt`
  - `receipts/probe_pp_mvu_run.txt`
  - `receipts/probe_pp_mvu_patch.diff`

  The probe exports a `git archive` of the pinned processor into scratch, patches only that copy, and caps builds at 8 jobs. The Verilator identity is in `receipts/verilator_identity.txt`.
- `receipts/standards_clause_receipts.txt`: short clause excerpts with line numbers, plus the source PDF hashes.
- `receipts/asym_grep.txt`, `receipts/pp_pin_claims.txt` and `receipts/rtl_lens_checks.txt`: pin and parent greps.
- `receipts/hosted_check_runs.tsv` and `receipts/hosted_status.txt`: exact-head hosted contexts.
- `receipts/commit_history.txt` and `receipts/pr_diff.patch`: history and the reviewed diff.
- `receipts/prior_findings_recheck.txt`: the after-ledger PR review-state read.
- `receipts/state_before.txt` and `receipts/state_after.txt`: the clone state before and after.
  - HEAD, tree, write-tree, index hash and all four gitlinks are identical.
  - Tracked bytes and modes are clean with `core.fileMode=true`.
  - No assume-unchanged or skip-worktree flags are set.
  - A documentation-gate subprocess wrote one ignored bytecode cache, `scripts/__pycache__/png_artifact.cpython-314.pyc`, during this round. It was removed, and the ignored count is back to 0.

## Real limits

- **Not run here:** the full builder, Verilator, Yosys, processor and gPTP banks, Docker/act, the host act runner, and hardware. The manager's source static/builder and native bank pass at this head is taken from the round brief. The public packet at `9fc8ebe3` holds the executor's receipts, which I read (`test_builder` `ALL GATES PASS EXCEPT 1 NOT RUN`, pp_top `1371 PASS`, gates at `64bcf76`). It does not hold a separate manager bank log.
- **Hosted, exact head:** 8 contexts executed and succeeded: `bdd-conformance`, `changes`, `docs-check`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `rtl-fast` and `wire-accountability`. 7 were skipped: `verilator-suites`, `yosys-portability`, their shards, `verilator-lint`, `yosys-elaboration` and Physical gPTP. A skipped context is not executed evidence. The legacy combined status reads `pending`, with zero statuses.
- **No physical evidence.** Physical calibration is NOT RUN. The #394 bench proof is not attempted. Field skips are not hardware proof.
- **The MVU probe is scratch-only.** It is evidence for this round, not a committed regression.
- **How the standards were read.** Clause readings come from text extractions of local copies of the standards. F2 rests on the Table 14-6 Conformance column and its legend; it does not depend on where the "(recommended)" annotation is placed.
- **No candidate merge was built.** The candidate against live `dev` `26d855a9176d63625e6635a029a0c44e3d57ce9a` is the manager's duty at the merge turn.

## Pending manager duties

1. Route F1 and F2 to the executor, then run a re-review at the fix head, following the ledger note above.
2. Obtain owner confirmation or replacement of the #511 revisit trigger. It was derived by the executor from the decision's two grounds, and F2 adds a third condition.
3. Correct or annotate the two statements in the #511 REVIEW READY comment that F1 and F2 identify.
4. File the out-of-diff item the executor reported: `tests/features/aecp_response_contract.feature:98-106` sends `GET_MILAN_INFO` (0x0000) through the offline model and asserts `NOT_IMPLEMENTED`, while the pinned engine serves that command (pp_top M1).
5. Keep #394 open for the bench proof (#117, #75). Keep #510 open for processor F01.5 (issue 77) and for committed per-command checks (issues 55 and 56). The reviewer probe receipt is available as byte-exact pin evidence for #510 acceptance 3, if the manager accepts a scratch probe for that purpose.
6. Hosted and act acceptance, candidate-merge validation against live `dev` with the full local bar, and post-merge containment.

## Addendum: after-ledger re-check of prior public findings

The PR was re-read at 2026-09-24T00:09Z, after the verdict and ledger above were written (`receipts/prior_findings_recheck.txt`).

- The head is unchanged at `64bcf768d28b4b9763fbe5917a734bcefa2a66e0`.
- The thread holds four manager round-start comments: R274-1 twice and R275-1 twice.
- There are no review objects and no inline review comments.
- The #394, #510 and #511 issue threads carry no comment beyond those read at the start.

No prior public finding exists on this PR, so nothing needs to be resolved or retained. The verdict and ledger stand as written.

R274-1 FINISHED
