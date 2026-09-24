[R275] NEGATIVE - exact head 64bcf768d28b4b9763fbe5917a734bcefa2a66e0

Round R275-1. External cleared-context independent review of PR #537 (Closes #511; Relates to #394 and #510).

- Head `64bcf768d28b4b9763fbe5917a734bcefa2a66e0`, tree `8027683077254647a146b13ebd9c5434432858b3`.
- Source base `759da623072358afdb0e9d570a7b4b6a788492c9`, which is an ancestor of the head.
- Six linear one-line commits, with no trailers.
- Eleven Markdown files changed, +199/-26. No non-Markdown file and no gitlink changed.

## Verdict

**NEGATIVE.** Two MINOR findings are open at this head, F1 and F2. Both fall under Conformance and Docs, and both sit in the #511 design record, which is the issue this PR closes.

Both were first published by the internal round R274-1. I read that round only after my own verdict and ledger were written and hashed (see "Prior public review findings"). I retain both here on the evidence given below.

The #394 and #510 records are accurate and complete at this head. RTL, Robustness and Tests are covered clean. There are also three SUGGESTIONs, none of which affects coverage.

Reconstructed from, in this order:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. The bodies and comments of #394, #510 and #511: the owner decisions of 2026-09-23, the assignment and the executor's REVIEW READY comments.
3. The PR body and its manager comments.
4. REQUIREMENTS.md, FR_NFR.md, the compliance matrix and the feature-status ledger, with its JSON facts.
5. The pinned processors' own clause references.
6. `git diff 759da623..64bcf768` and its history.
7. The public packet at `9fc8ebe3d6b38b1b5658b0c2b388dff99f4998f0/review-evidence/394_510_511-r1`.
8. The exact-head hosted check runs.

## Findings

### R275-1-F1: MINOR. Lenses: Conformance, Docs. Retains R274-1 F1

- **Where:** `docs/design/GPTP_PLANE.md:359`, the "Where would it enter?" row. It reads: "ClockSlaveSync `syncReceiptTime` and `setMDSyncReceive()` `upstreamTxTime`. At zero both terms vanish."
- **Authority and evidence:** IEEE 802.1AS-2011 11.2.13.2.1 f) and 10.2.12 (Figure 10-9).
  - The executor's published clause receipt (`author/receipts/standards-clause-receipts.txt`, sha256 `0e017019...71b7`) shows two things:
    - 11.2.13.2.1 subtracts "delayAsymmetry (see 10.2.4.8) for this port divided by rateRatio" when it forms `upstreamTxTime` (extraction line 7399).
    - 10.2.12 adds `+ delayAsymmetry` to `syncReceiptTime` (line 4615).
  - ClockSlaveSync also sets `syncReceiptLocalTime`, the local-time instant paired with `syncReceiptTime`. That value is reached from `upstreamTxTime` only by adding back what 11.2.13.2.1 subtracted: `+ neighborPropDelay/neighborRateRatio + delayAsymmetry/rateRatio`.
  - R274-1 quotes that second 10.2.12 assignment at extraction lines 4614-4617.
  - So delayAsymmetry enters three expressions, not two, and "both terms" is wrong. The executor's #511 REVIEW READY repeats the omission ("it enters only 10.2.12 `syncReceiptTime` and 11.2.13.2.1 `upstreamTxTime`").
- **Impact:** v1.2 behavior does not change, because the value is zero.
  - This row is the record's statement of the arithmetic an adoption must reproduce. #511 asks that the arithmetic clauses be verified, and acceptance 3 asks for exact arithmetic.
  - Suppose an adoption applies only the two named terms. Then `syncReceiptLocalTime` stays short by delayAsymmetry/rateRatio, and the offset moves by about twice the configured value.
  - The proof plan's "Positive and negative" arm (`GPTP_PLANE.md:407`) would catch that later. So the defect is in the record's reading of the standard.
- **Required outcome:** The row names all three terms at the cited clauses, or it states the net clause-level effect equivalently. The net effect is +delayAsymmetry on `syncReceiptTime`, and the `syncReceiptLocalTime` term cancels the 11.2.13.2.1 subtraction. "Both terms" is corrected.
- **Verification:** A reviewer re-reads `GPTP_PLANE.md` at the fix head against Figure 10-9 and 11.2.13.2.1 f).

### R275-1-F2: MINOR. Lenses: Conformance, Docs. Retains R274-1 F2 and supersedes my independent S1

- **Where:**
  - `docs/design/GPTP_PLANE.md:360`, which reads: "IEEE 802.1AS-2011 14.6.9 lists it read-write and recommended".
  - The revisit trigger at `docs/design/GPTP_PLANE.md:378-384` and `REQUIREMENTS.md:141-143`.
- **Authority and evidence:**
  - The only published excerpt of the grading row is the executor's own receipt, line 11204: `delayAsymmetry  scaledNs  RW  Tdot3FD  14.6.9`. It carries a conformance code, not a recommendation. No published line supports "recommended".
  - In my independent pass I rated that gap SUGGESTION, because the claim was unsupported but not refuted.
  - R274-1 has since published a reading of the Table 14-6 legend: "Tdot3FD = Required for time-aware IEEE 802.3 full-duplex port". It places "(recommended)" as a Data-type annotation, which `neighborPropDelay` and `neighborPropDelayThresh` also carry at conformance `T`. It also reads management as a whole as optional (Annex A PICS `MGT` = O).
  - That reading agrees with the published row excerpt. The PR's "recommended" grade therefore stands both unsupported and contradicted, in the row #511 asked to verify.
- **Impact:** The exclusion still holds, because the product claims no 802.1AS management.
  - The record misstates the object's conformance grade.
  - The revisit trigger ("a second cabled port"; "a REQ-PTP-06 amendment") misses the re-entry path that claiming 802.1AS management would open. If a future claim is made, for example for the P4 "802.1AS conformance" item on the README roadmap, Table 14-6 would require a read-write delayAsymmetry object on the product's 802.3 full-duplex port.
- **Required outcome:**
  - The row states Table 14-6 accurately: RW; conformance `Tdot3FD`; management optional; none claimed by this product.
  - The revisit trigger adds "claiming 802.1AS management" in the GPTP_PLANE record and the REQUIREMENTS.md scope note, or states why that cannot arise.
- **Verification:** A reviewer re-reads at the fix head against Table 14-6, its legend and PICS `MGT`.

### R275-1-S2: SUGGESTION. Lenses: Tests, Docs. The new AS-13 row is not gated

`scripts/check_gptp_docs.py:73-75` requires rows `AS-1` to `AS-12` only. Probe D1 deleted the AS-13 row, and every documentation gate still exited 0 (`receipts/50-doc-gate-reach-probes.txt`).

This is optional: extend the required range to AS-13, or derive it from the requirement map.

### R275-1-S3: SUGGESTION. Lens: Tests. Retains R274-1 S1

The executor raised the same point. "Can a configuration set it? No" (`GPTP_PLANE.md:361`) is structural (`sw/builder/endstation_builder.py:3940-3948`). No committed builder arm plants an asymmetry key.

The reviewer probe shows the refusal holds at this head:

- The two-key control is accepted.
- `delay_asymmetry_ns`, `delayAsymmetry` and `asymmetry_ns` are each refused, naming the key (`receipts/10-builder-gptp-key-probe.txt`).

### R275-1-S4: SUGGESTION. Lenses: Docs, Conformance. AS-13 does not name its edition

AS-13's clause cell (`docs/traceability/ieee8021as.md:49`) cites `8.3, 10.2.4.8, 14.6.9` in 2011 numbering, but does not say so. AS-8 in the same table uses the 2020 number `11.2.19`.

Labelling the cell "2011" keeps a cold reader from mapping 10.2.4.8 onto the 2020 edition.

My independent S1 is superseded by F2. None of these findings is attributed to RTL or Robustness.

## Per-lens results

```text
[R275] PASS RTL - diff 759da623..64bcf768 (11 *.md, 0 non-Markdown, 0 gitlink changes) and the RTL the new text cites - protocol-processor 424c688 hdl/aecp/KL_aecp_engine.sv:1290-1296 (only command_type 0x0000 with the Milan protocol_id and an 8-byte payload leaves the echo; banner :161-171), hdl/aecp/ucode/gen_ucode.py:112 (MILAN_FEATURES_FLAGS 0), hdl/top/protocol_processor_top.sv:1594 (.N_IF_P(1)); parent hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:115-116 (INGRESS_LAT_NS_P/EGRESS_LAT_NS_P), docs/reference/REGISTER_MAP.md:1392 (GPTP_LAT 0x7F0); gptp-processor c1b6174 has no asymmetry input and no tuner outside docs/history (receipts/11; the one other hit is inside base64 image data of docs/diagrams/gptp_architecture.svg, receipts/12); sw/litex/milan_soc.py:3632 (one --eth-port e1|e2)
[R275] PASS Robustness - sw/builder/endstation_builder.py:3940-3948 driven by scripts/probe_builder_gptp_keys.py (control accepted; three asymmetry spellings refused; receipts/10) and the MVU fallback for 0x0001/0x0003/0x0004 at 8-, 16-, 80- and 12-byte payloads in the pinned pp_top: byte-exact NOT_IMPLEMENTED echo for each (receipts/42); the REDUNDANCY flag is a microcode constant and the key refusal is global, so no shipping configuration changes either result
[R275] PASS Tests - no test file changed; the checks the text cites ran at the pinned bytes (git archive of 424c688) under Verilator 5.050 rev v5.050 (receipts/30): pp_top 1371/1371 (receipts/41); with six added arms 1383/1383 (receipts/42); an engine fault that serves 0x0000..0x0004 as GET_MILAN_INFO is caught by M4 and all six arms, 7 FAIL (receipts/43, 40-*.diff); 14 documentation gates exit 0 (receipts/20); gate-reach probes D2 (anchor), D3 (U+2014) and D4 (served-MVU over-claim) are caught, D1 (AS-13 deleted) is not (S2) and D5 (FR-MVU-02 back to M) is review-guarded by design (receipts/50); the adoption proof plan GPTP_PLANE.md:400-413 names a failing condition for every arm
```

**Conformance is UNCLEAN**, because of F1 and F2. Everything else under this lens was checked and found clean:

- Milan v1.2:
  - 4.2.5 and 8.1: redundancy is optional. The executor's receipt and the processor's own REQ-SCP-001 (`docs/00_MILAN_COMPLIANCE_REVIEW.md:442`) agree.
  - 5.4.4.1 with Table 5.20: bit 31 is `0x00000001` REDUNDANCY (receipt; `06_aecp_engine.md:1016`).
  - Table 5.18 lists the MVU commands. Table 5.19 gives `NOT_IMPLEMENTED` = 1 (engine banner: "Table 5.19 = IEEE Table 9-6").
  - The recommendation note appears in all five places cited: 5.4.4.2, .3, .4, .5 and 7.6. The processor's REQ-MVU-004 cites 7.6.
  - 8.3.1: at least two AVB-capable ports.
  - Zero mentions of asymmetry.
- 802.1AS-2011:
  - 8.3: measurement not explicitly required; sign convention.
  - 8.4.3: `ingressLatency`/`egressLatency`.
  - 10.2.4.5 is `syncInterval`, and 10.2.4.8 is delayAsymmetry (unmodelled means zero). The donor pages cite 10.2.4.5 for it.
  - 11.2.15 is MDPdelayReq, and 11.2.15.2.4 is `computePropTime()`.
- FR-MVU-02 moves M to S. That is exactly the #510 decision, since RFC 2119 SHOULD = RECOMMENDED.
- No other requirement is weakened:
  - FR-MVU-03 stays M/I, with equivalent wording.
  - NFR-SCOUT-05 stays S/A,D.
  - REQ-PTP-06 text is unchanged.
  - FR_NFR step 10 moves from "redundancy-off recovery" to "single-port link-loss recovery", which is not a weakening.
  - Adding delayAsymmetry to the out-of-scope list does not weaken FR-CLK-01, because 802.1AS does not require modelling it.
- The FR_NFR ledger's move from "PARTLY MET" to "FR-MVU-01 and FR-MVU-03 MET" is supported: pp_top M1 grades the byte-exact GET_MILAN_INFO body, M2 grades `features_flags` 0, and compliance-matrix 5.4.4.1 reads implemented.

**Docs is UNCLEAN**, because of F1 and F2. Everything else under this lens was checked and found clean:

- All eleven changed pages were read in context.
- Added table rows match their headers' column counts.
- The ASCII roadmap block stays aligned.
- All 20 decision links pair each issue with its own owner-decision comment (`receipts/13`).
- The new anchor `#propagation-asymmetry-is-not-modelled` resolves from all five pages, and gen_toc reproduces it.
- The cross-referenced issue titles match their use:
  - #416 is P4 and #417 is P5.
  - #64, #488, #110, #117 and #75 match.
  - Processor issues 55, 56 and 77 and donor issue 58 match.
- The feature-status JSON has no redundancy, asymmetry or recommended-MVU feature ID, and `served_mvu_operations` is `["GET_MILAN_INFO"]`.
- Every remaining occurrence of the command names or the features in the tree is consistent or dated. The saved-state pages list SUID/MCR records as "allocated, nothing writes them". The dated audit is untouched.
- The commits are one line each, with no trailers.

## Decision-by-decision check

| Decision | Recorded at the head | Clause | Revisit trigger | Result |
|---|---|---|---|---|
| #394: declared non-redundant end station | `README.md:329-337`; `REQUIREMENTS.md:48,262-270`; `FR_NFR.md:31,149,195,297,392-394,406-415,441`; compliance matrix `:34,:183`; roadmap `:474` | Milan v1.2 4.2.5, 5.4.4.1/Table 5.20, 8.1, 8.3.1 | P4/P5 PCB (#416/#417) | Accurate. Acceptance 1's four surfaces all change in `909d8feb` |
| #510: MVU SUID/MCR rows RECOMMENDED | `FR_NFR.md:88-92,149,194,433`; compliance matrix `:136-137`; roadmap `:470-471`; feature status `:120-126`; `SUBMODULES.md:111` | Milan v1.2 5.4.4.2-.5, 7.6, Tables 5.18/5.19 | P4 (#416) if the lab requires; processor issues 55/56 | Accurate. The fallback claim is true for all four commands at the pin (receipts/42) |
| #511: delayAsymmetry not modelled; UART tuner donor-bench-only | `GPTP_PLANE.md:348-429`; `REQUIREMENTS.md:130-145,272-276`; `FR_NFR.md:31,228-236,416-422,442`; compliance matrix `:226`; roadmap `:475`; `ieee8021as.md:29,49,64,77`; `TIME_SYNC.md:63`; `MANAGER.md:34` | 8.3 and 10.2.4.8 exact; arithmetic incomplete (F1); 14.6.9 grade misstated (F2) | Second cabled port; REQ-PTP-06 amendment. Missing the management-claim path (F2) | F1 and F2 open |

The trigger for #511 is stated in REQUIREMENTS section 4 and the plane record. The other #511 surfaces point to those two, which keeps a single source for it.

The partial-close reasons are accurate:

- **#394 stays open:** acceptance 2, the bench proof, needs hardware and is unmet.
  - The PR body's "acceptance 4 met" is acceptable. Gate 11 is an environment-bound SKIP, a missing local build report.
  - The two intermediate commits not run through `test_builder` change only Markdown the builder never reads. `test_builder.py` names `GPTP_PLANE` only as the `GPTP_PLANE_EN_P` parameter and in one comment, and `ieee8021as` only as an `hdl/` path.
- **#510 stays open:**
  - At the pin, `docs/architecture/01_overview.md:169`, in section 7, "Parameter master table (F01.5)", still lists `P-EN-MVU-SUID / P-EN-MVU-MCR | 1 / 1`, and no such parameter exists in `hdl/` or `tb/` (receipts/11).
  - Only 0x0002 has a committed byte-exact check.
- **#511's "Closes" is not yet earned:** F1 and F2 fall under its acceptance 1 to 3.

## Prior public review findings

- **How the prior round was read:**
  - My verdict and ledger were written before any other reviewer's report was opened. They are `receipts/80-independent-verdict-and-ledger.md`, hashed at 2026-09-24T00:22:13Z, sha256 `16f0c06d...8d90`.
  - At that point this round's verdict was POSITIVE, with all five lenses clean and four SUGGESTIONs.
  - I then read R274-1 (https://github.com/kebag-logic/milan-fpga/pull/537#issuecomment-5805065861, 00:11:02Z; `receipts/81-prior-findings-read.txt`). No other review object or inline comment exists, and the head is unchanged.
- **R274-1 F1 (MINOR):** retained as R275-1-F1. My independent pass missed the `syncReceiptLocalTime` term. I verify it from the executor's own published receipt lines and from the pairing of `syncReceiptTime` with `syncReceiptLocalTime` described under F1.
- **R274-1 F2 (MINOR):** retained as R275-1-F2. My independent pass flagged the same "recommended" qualifier as unsupported, at SUGGESTION. The published row excerpt together with R274-1's legend reading makes it a misstatement, and the missing management re-entry path follows from it.
- **R274-1 S1 (SUGGESTION):** retained as R275-1-S3.

Nothing at this head resolves any of them.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Milan v1.2 and 802.1AS-2011 clauses cited on all 11 pages, against the executor's clause receipt, the processors' clause references and R274-1's published readings; FR-MVU-01..03, NFR-SCOUT-05, FR-CLK-01 and REQ-PTP-06 levels; issue acceptance of #394/#510/#511 | R275-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |
| RTL | CLEAN | Diff file list and gitlinks; `KL_aecp_engine.sv:1290-1296,161-171`; `gen_ucode.py:112`; `protocol_processor_top.sv:1594`; `KL_gptp_shadow.sv:115-116`; `REGISTER_MAP.md:1392`; gptp-processor `c1b6174` tree; `milan_soc.py:3632` | R275-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |
| Robustness | CLEAN | Builder `_known_gp` refusal probe (control plus 3 keys); MVU fallback probe at 4 payload sizes for 0x0001/0x0003/0x0004; configuration independence of both | R275-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |
| Tests | CLEAN | pp_top at pinned bytes (1371/1371, 1383/1383 with arms, fault caught 7/7); 14 documentation gates; gate-reach probes D1-D5; adoption proof plan `GPTP_PLANE.md:400-413` | R275-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |
| Docs | UNCLEAN (F1, F2) | All 11 changed pages; table shapes; 20 decision links; anchor; cross-referenced issue titles; feature-status JSON; tree-wide occurrences; commit messages; PR and issue partial-close text | R275-1 | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |

The fix head must be re-covered under Conformance and Docs. RTL and Robustness stay covered unless the fix touches their scope. Tests must be re-covered if the fix changes the adoption proof plan (`GPTP_PLANE.md:400-413`) or any gate.

## Executed evidence in this packet

Every file below is listed in `MANIFEST.sha256`. Absolute paths are redacted to `$PACKET`, `$CLONE`, `$PINNED_TOOL_BIN` and `$HOME` (`scripts/redact_paths.sh`).

- `scripts/tree_state.sh` produced `receipts/00-baseline-tree-state.txt` and `receipts/90-final-tree-state.txt`. They record HEAD, tree, index==HEAD, every tracked blob rehashed with its mode (0 mismatches), 0 untracked, 0 ignored files at the end, and the three required gitlinks equal to their checked-out, clean submodule HEADs.
- `scripts/pin_claims.sh` produced `receipts/11-pin-claims.txt`. `receipts/12-gptp-svg-asym-hit.txt` shows the 3 SVG hits are all inside base64 data.
- `scripts/probe_builder_gptp_keys.py` produced `receipts/10-builder-gptp-key-probe.txt`. It is a read-only in-process import and writes no bytecode.
- `receipts/13-decision-links.txt` records the decision-link pairing.
- `scripts/run_doc_gates.sh` produced `receipts/20-doc-gates-at-head.txt`: 14 gates, all exit 0, with the executor's counts reproduced (199 added lines in 11 pages; 164 md and 848 scrubbed files; 46/46; 154 anchors).
- `receipts/30-verilator-identity.txt`: wrapper and resolved binary hashes, version 5.050 rev v5.050.
- The processor probe, run with `scripts/pp_mvu_probe_patch.py` and `scripts/run_pp_top.sh` on `git archive` copies of `424c688` in the unpublished scratch area, capped at 8 build jobs:
  - `receipts/40-pp-probe-arms.diff` and `receipts/40-pp-probe-mutant.diff`: the patches.
  - `receipts/41-pp_top-base.log`: 1371/1371.
  - `receipts/42-pp_top-arms.log`: 1383/1383.
  - `receipts/43-pp_top-mutant.log`: 1376/1383, and the 7 FAILs are M4 plus the six arms.
- `scripts/doc_gate_reach_probes.sh` produced `receipts/50-doc-gate-reach-probes.txt`. It ran in a disposable `--shared` clone, never the review clone.
- `receipts/60-dev-drift-files.txt` and `receipts/61-dry-merge-tree.txt`: live `dev` `26d855a9` is 4 commits ahead of the base. It also touches `docs/design/TIME_SYNC.md`, in a different hunk. A disposable textual `git merge-tree` of the head onto it is clean (tree `a369f86617cdd7824fe51d53a852d8db629158e3`). This is not a gated candidate.
- `receipts/70-hosted-check-runs.txt`: the exact-head hosted contexts.
- `receipts/80-independent-verdict-and-ledger.md`, `receipts/80-independent-verdict.timestamp` and `receipts/81-prior-findings-read.txt`: the ordering of the independent verdict and the prior-findings read.
- `receipts/05-public-evidence-sha256.txt`: hashes of the public-packet files read (not republished).

## Real limits

- **Standards texts.** The standards texts were not available to this reviewer; the public download was refused. Clause checks rest on four sources:
  - the executor's line-numbered excerpts;
  - the pinned processors' independent clause references;
  - derivation;
  - R274-1's published readings.

  I did not see the Table 14-6 legend or PICS `MGT` myself.
- **Manager bank evidence.** The linked public tree at `9fc8ebe3` holds the executor's packet. The files I read are hashed in `receipts/05-public-evidence-sha256.txt`, and I re-derived what they claim rather than relying on them. I found no separate manager bank log there. The manager's static/builder and native bank pass at this head is taken from the round brief and not relied on.
- **Not run:** full parent, processor, gPTP, Yosys or builder banks; Docker/act; the host act runner; hardware. Physical calibration is NOT RUN, and field skips are not hardware proof.
- **Hosted, exact head:** 8 contexts executed and succeeded: `bdd-conformance`, `changes`, `docs-check`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `rtl-fast` and `wire-accountability`. 7 were skipped: `verilator-suites`, `yosys-portability`, their shards, `verilator-lint`, `yosys-elaboration` and Physical gPTP. A skipped context is not executed evidence.
- **Scratch-only probe.** The MVU per-command probe is scratch-only. It is evidence for this round, not a committed regression.

## Pending manager duties

1. Route F1 and F2 to the executor. Then run a re-review at the fix head under Conformance and Docs, and under Tests if the proof plan or a gate changes.
2. Obtain owner confirmation or replacement of the #511 revisit trigger. The executor asked for it in the PR and on #511, and F2 adds the management-claim condition.
3. Correct or annotate the two #511 REVIEW READY statements that F1 and F2 identify.
4. File the out-of-diff item the executor reported and I confirmed. `tests/features/aecp_response_contract.feature:98-106` sends `build_mvu_command()`, whose default is GET_MILAN_INFO 0x0000 (`tests/steps/aecp_engine_model.py:591`), through the offline model and asserts status 1 `NOT_IMPLEMENTED`. The pinned engine serves that command (pp_top M1).
5. Keep #394 open for the bench proof (#117, #75). Keep #510 open for processor F01.5 (issue 77) and for committed per-command checks (issues 55 and 56). `receipts/42` and `receipts/43` are available as supplementary pin evidence.
6. Build the candidate against live `dev` `26d855a9176d63625e6635a029a0c44e3d57ce9a` with the full local bar. Also own hosted and act acceptance, and post-merge containment.
7. Publish, or point to, the manager's own bank receipts for this head.

R275-1 FINISHED
