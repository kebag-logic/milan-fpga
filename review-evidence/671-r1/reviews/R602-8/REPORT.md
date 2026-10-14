[R602] POSITIVE - exact head d5cd863561ba1ee7bc6342fb1b00f57dd786bd97

# R602-8: internal cleared-context review of PR #715 / issue #671, round 8 (delta)

Head `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97`, tree `029737bc62cb0fc1bbf45e3aed82a39160ee41da`. Source base `e8454e2751d05b02ee8e5a571857589ab358ab86`, live dev `fa8209889411e8ca95757174c981f720dbcd95a2`. Delta under review: `9b32002c..d5cd8635`, per the [round-8 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6161596895).

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. All five lenses are CLEAN at `d5cd8635`.

- Two new SUGGESTIONs are filed: R602-8-S1 and R602-8-S2.
- RESIDUE R602-7-R1 is retained and re-filed at this head's line numbers, because `d5cd8635` rewrote the lines it names.
- RESIDUE R602-6-R1 is retained unchanged.
- SUGGESTIONs R602-4-S1 and R602-4-S2 remain optional.

## Scope and reconstruction

I read the sources in this order:

1. AGENTS.md, CONTRIBUTING.md (commit rule) and docs/README.md.
2. The #671 body and its frozen acceptance 1-3.
3. Every lane assignment and REVIEW READY comment on the issue, through [round 8](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6161596895) and the [round-8 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6165001131).
4. The PR body (Status, Round 8, How to validate, Known limitations).
5. The design authority, `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and UNRESOLVED 6.
6. The capture harness README, `check_nvm_capture.py` and `sw/litex/milan_soc.py`.
7. The git objects of `9b32002c`, `fa820988`, `f3bb2014`, `d5cd8635` and `c6bd08c6`.
8. The public author packet at evidence commit `10d91cdb` (`review-evidence/671-r1/author-r8`, plus one round-7 capture log for comparison).

I wrote my verdict and ledger before reading prior review findings. I read no report from this round's other reviewer.

The round-8 assignment asks for four things:

1. Merge `origin/dev` `fa820988` with a merge commit, with no rebase.
2. Re-run the gates this lane's files touch, plus `ci_scope --selftest`, `act_ci --selftest` and `ci_events --check`.
3. Re-measure only what dev's changes could affect, and justify every measurement that still holds.
4. Change nothing else.

## Delta facts established (independently)

Receipt: `receipts/merge_provenance.log` (script `scripts/merge_provenance.sh`).

- **Merge commit.** `f3bb2014` has parents `9b32002c` and `fa820988`, so it is a `--no-ff` merge. The merge-base is `c6bd08c6`, the dev commit merged in round 7. `git merge-tree --write-tree 9b32002c fa820988` returns `7a2041b6a0b7ea13c019a3b5be08f0eb3555f8ac` with no conflict output. That equals the merge commit's tree, so nothing was resolved by hand.
- **Branch-owned paths.** At the merge, exactly 15 paths differ from dev, and they are the same set that differed in round 7 (`c6bd08c6..9b32002c`). All 15 are byte-identical to `9b32002c`.
- **Merge delta.** Dev changed 160 paths since `c6bd08c6`, none of them among the 15 branch-owned paths. `git diff --full-index --binary 9b32002c f3bb2014` is byte-identical to `git diff --full-index --binary c6bd08c6 fa820988`. So the merge delta is exactly dev's delta.
- **Gitlinks.** The only gitlink change is dev's new `third_party/tsn-c-stack` at `70936b77`. The other pins are unchanged: protocol `2ad2f845`, gPTP `7dda9c3b`, verilog-axis `48ff7a7e`, lwSRP `08ee86e8` and external `efeb541a`. The pins are the same at `d5cd8635`.
- **Head commit.** `d5cd8635` changes exactly two files: `tb/verilator/nvm_capture_cpu/measurements.json` (+5/-5) and `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` (+9/-6).
  - Receipt: only the top-level keys `date`, `base`, `tree`, `remeasurement_assignment` and `provenance` change (`receipts/receipt_compare.txt`).
  - The `measurements` array, all six arms and 96 rows, is identical to round 7's receipt, including every per-arm hash. The `maxima` are also identical.
- **Commit messages.** Both new commits have one-line messages with no trailers (CONTRIBUTING "Commits: one line, no trailers").

### The re-measure decision

Receipts: `receipts/capture_rtl_map.txt`, `receipts/dev_closure.txt`, `receipts/verilation_reports.txt`.

- **Which dev RTL is in the capture SoC.** Dev changed eight RTL files.
  - Seven are in `_MILAN_DATAPATH_SOURCES` (`sw/litex/milan_soc.py:548`), which the capture SoC instantiates: `KL_maap.sv`, `KL_avtp_rx_monitor.sv`, `KL_avtp_rx_monitor_ctx.sv`, `KL_talker_diag_ctx.sv`, `KL_aaf_packetizer.sv`, `KL_crf_rx.sv` and `milan_datapath.sv`.
  - The eighth, `KL_mbx_pkg.sv`, is only in `_CTRL_MAILBOX_SOURCES` (`:2619`). `tb/verilator/nvm_capture_cpu/soc.py` never enables `ctrl_mailbox`.
  - So the author's "seven dev-changed RTL files" is exact. The commit history confirms MAAP (#696) and the stream counters (#726).
- **The receipt gate cannot see RTL.** `check_nvm_capture.py:48-73` hashes the census, the clocks, the firmware and the harness, but no RTL. A re-measure was therefore the only way to bind the merged RTL. Choosing all six arms is the conservative, correct reading of the round-7 rule. The PR body says the gate alone would not have asked for it.
- **Inputs dev did not change.** Dev touched none of:
  - the capture harness, firmware, configs, LiteX patches, builder, processor submodules or `KL_nvm_backend.sv`;
  - the host-gate and co-simulation helper modules (`nvm_shape`, `nvm_contract`, `nvm_klj2`, `boot_policy`, `flash_map`, `check_nvm_record_space`).

  Its one change on the SoC-generator side is `milan_soc.py`. That change is gated on `ctrl_mailbox` (`:2825`, `:2928-2932`, `:2959-2960`), which neither harness sets.
- **The run really compiled the new RTL.** The published round-8 8x8/50/ON build reports `152.662 MB sources ... 21.882 MB in 124 C++ files`, where round 7's reports `152.652 MB ... 21.854 MB in 125 C++ files`.
- **The run's outputs match the receipt and round 7.** Receipts: `receipts/arm_vs_receipt.txt`, `receipts/artifacts_vs_receipt.txt`.
  - All six published per-arm `measurement.json` files have rows equal to the committed receipt's rows.
  - The run's artifact index gives `bios.bin` and instrumented-firmware hashes equal to both the receipt and round 7's receipt.
  - The BIOS links the firmware library, so the compiled firmware binary and its generated headers' effect on it are unchanged.
- **Figures.** The 8x8/50 maximum is 1,386,328 cycles at 100 MHz, or 13.86328 ms. That leaves 10.63672 ms of margin to 24.5 ms and gives 49/13.86328 = 3.5345x. The 1x1 maximum is 3.96548 ms, and the non-contract 100 MHz comparison is 10.42973 ms.
- **What holds without re-measure.** Each claim is justified:
  - Firmware size: the source is byte-identical, with SHA-256 `497845e6...1bed`.
  - Boot read cost: the CPU netlist, BIOS, LiteSPI revision and flash model are unchanged.
  - Backend area: `KL_nvm_backend.sv` is unchanged.
  - Writer-gate time: the suite is unchanged.
- **Simulator version.** The superseded 5.050 attempt is recorded as superseded and does not feed the receipt. The receipt names `Verilator 5.052` (`measurements.json:16`), as do the harness README and the published run logs.

### Section 18

Receipt: `receipts/section18_vs_receipt.txt` (script `scripts/section18_vs_receipt.py`).

- Recomputed from the receipt, all six table rows (minimum, maximum, ratio), the worst 8x8 value, its ratio and margin, the measured commit, tree, firmware digest, both pins, the date and the assignment link appear verbatim in section 18.
- The new prose at `:1629-1631` is accurate. It names dev's MAAP and stream-counter RTL, and says the firmware, harness, pins, clocks and census are unchanged.
- `:1670-1671` ("previous #671 receipt ... and so did the one before it", "All 96 captures repeat the previous #671 receipt") remain true: round 7 equals round 5.
- UNRESOLVED 6 (`:1844-1860`) remains true.

## Findings

### R602-8-S1 - SUGGESTION - Docs - `review-evidence/671-r1/author-r8/receipts/r8/GATE-TABLE-R8.md` (evidence commit `10d91cdb`) - the round-8 scripts the gate table cites are not published

- **Evidence.** The gate table cites six round-8 scripts: `$EVIDENCE/scripts/r8/{assemble_receipt.py, refresh_section18.py, compare_products.py, docs_replica.sh, final_gates.py, fw_size.py}`.
  - `author-r8/` holds 112 files and no `scripts/` directory.
  - Earlier rounds published theirs: `author-r7/scripts/` has 96 files.
  - `receipts/evidence_provenance.txt` lists the gap.
- **Impact.** A cold reader cannot re-run the receipt assembler, the section-18 refresher or the products comparison. That includes the "headers equal apart from timestamp and build directory" normalisation, which `compare-products-attempt1.log` shows was needed for `variables.mak`.
- **Why it does not block.** No claim at this head depends only on those scripts. I re-derived each one from published artifacts and my own runs:
  - receipt content and rows (`arm_vs_receipt.txt`, `receipt_compare.txt`);
  - BIOS and firmware identity (`artifacts_vs_receipt.txt`);
  - section 18 (`section18_vs_receipt.txt`);
  - the final capture and document gates (`receipts/gates/`, `receipts/docgates/`).
- **Suggested outcome.** Publish `author-r8/scripts/r8/` with the packet, or point the gate table at where the scripts live.
- **Verification.** Every `$EVIDENCE/scripts/...` path in `GATE-TABLE-R8.md` resolves in the evidence tree.

### R602-8-S2 - SUGGESTION - Tests - `scripts/check_nvm_capture.py:65-75`; `tb/verilator/nvm_capture_cpu/measurements.json` - the receipt does not bind the capture SoC's RTL

- **Evidence.** The receipt gate binds the census, the clocks, the product firmware digest and the harness hashes. It binds no digest of the RTL that `soc.py` compiles, although `run.py` already writes `sources.json` per arm.
- **Impact.** This round's re-measure rested on the reviewer and author reading `_MILAN_DATAPATH_SOURCES` by hand. An RTL change inside the capture SoC would leave the receipt gate green.
- **Scope.** This is pre-existing gate design, outside this delta and outside #671. It should go to a new Issue if taken up.
- **Suggested outcome.** The receipt records a digest of the source list and its file contents, and the gate refuses a mismatch.
- **Verification.** A planted one-byte edit to a capture-SoC RTL file fails the gate by name.

### Prior public findings: disposition at this head

| Finding | Disposition | Evidence at `d5cd8635` |
|---|---|---|
| R602-7-R1 (RESIDUE, Docs) | RETAINED, residue; re-filed below at the new line numbers | `d5cd8635` rewrote the chain. Now `:1632`, `:1637` and `:1641` each say "required the previous one" about three different receipts, and `:1635`, `:1639` and `:1642` say "the one before (that)". |
| R602-6-R1 (RESIDUE, Docs) | RETAINED, residue | `sw/firmware/nvm_hosttest/README.md:165-168` is byte-identical to `9b32002c`. The parenthetical still lists only the blank-other sequences. The round-6 exact fix still applies. |
| R602-4-S1 (SUGGESTION, Tests); R602-4-S2 (SUGGESTION, Tests, Robustness) | RETAINED, optional | The host suite and firmware are byte-identical to `9b32002c`. |
| R602-5-F1, R603-5-F1, R603-4-F1 (MAJOR) and every earlier F-finding | RESOLVED, holds | The firmware and host suite are byte-identical to the heads where they were resolved. The writer gate's self-test at this tree catches `r_omit_trailer`, `r_omit_prefix_crc`, `r_digest_with_trailer` and the comparison check by their own words (`receipts/hostsuite/writer_gate_selftest.log`). |

**R602-7-R1, re-filed - RESIDUE - Docs - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632-1642`.**

- **Problem.** The receipt chain's relative objects name different receipts with the same words. No figure, identity, test or claim is wrong.
- **Exact fix.** Replace each relative object with a named receipt:
  - `:1632` "required the round-7 receipt, at the merge of dev `c6bd08c6` into #671";
  - `:1635` "required the round-5 receipt on #671";
  - `:1637` "required the round-4 receipt";
  - `:1639` "required the round-3 receipt";
  - `:1641` "required the round-2 receipt, for the console report of the writer's hold";
  - `:1642` "required the first #671 receipt, for the boot read-fault rule".
- **Verification.** `scripts/docs_check.py` and `scripts/check_doc_style.py` stay at 0 findings.

## Lens results

```text
[R602] PASS Conformance - merge_provenance.log; f3bb2014 parents 9b32002c+fa820988; d5cd8635 diff (2 files); #671 acceptance 1-3 artifacts byte-identical to 9b32002c (milan_baremetal.c sha256 497845e6...1bed) - round-8 items 1-4 checked against the assignment: merge commit, no rebase, no hand resolution; own 15 paths unchanged; merge delta == dev delta; only gitlink change is dev's tsn-c-stack; re-measure confined to the receipt and section 18; acceptance 1-3 evidence unchanged and the writer gate re-passes at this tree
[R602] PASS RTL - sw/litex/milan_soc.py:548,2619,2825,2928-2932,2959-2960; tb/verilator/nvm_capture_cpu/soc.py; capture_rtl_map.txt; verilation_reports.txt; dev_closure.txt - no lane RTL in the delta; seven dev RTL files enter the capture SoC (KL_mbx_pkg only via opt-in ctrl_mailbox); KL_nvm_backend.sv, KL_pp_shadow.sv and processor pins unchanged; dev's SoC-generator change is opt-in and unused by both harnesses; the round-8 Verilator build compiled the changed sources; CPU netlist, BIOS and microcode hashes equal round 7
[R602] PASS Robustness - receipts/hostsuite/writer_gate_selftest.log (merged tree); dev_closure.txt; measurements.json arms ON/OFF - read-fault, restart, term and boundary campaigns pass on 5 shapes with every planted defect reddened; co-simulation and host-gate inputs unchanged by dev (re-run would repeat round 7); both traffic arms within 24.5 ms under the merged RTL; superseded 5.050 attempt kept out of the receipt
[R602] PASS Tests - receipts/gates/*.log (check_nvm_capture rc 0; --mutation bytes/records/clock/ignore-off-timing/receipt-opt-out rc 1 each by name; ci_scope --selftest rc 0; ci_events --check rc 0, 2174 items); suite_shards --selftest PASS; writer gate --self-test rc 0 - each gate still fails for its planted defect; dev's nvm_cosim shard figure (scripts/suite_shards.py:178) does not interact with this lane's unchanged co-simulation; act_ci selftest relies on the author's container receipt (see limits)
[R602] PASS Docs - SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1626-1671,1844-1860 vs measurements.json (section18_vs_receipt.txt); receipts/docgates (docs_check, doc_style, doc_paths, em-dash vs fa820988: 0 findings over 365 added lines, TOC, hygiene, git diff --check vs e8454e27/fa820988/f3bb2014: all rc 0); PR body Status and Round 8 - every figure, identity and unchanged-input claim matches the receipt and git; RESIDUEs are wording only; S1 is an evidence-publication suggestion
```

## Reviewer-owned completion ledger (this round)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #671 acceptance and round-8 assignment vs merge provenance, head diff, byte-identity of the lane's 15 paths | R602-8 | `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97` |
| RTL | CLEAN | Capture-SoC source lists and dev's RTL delta, `milan_soc.py` opt-in change, gitlinks, round-7 vs round-8 build reports | R602-8 | `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97` |
| Robustness | CLEAN | Writer gate self-test at the merged tree; dev input closure for host gate and co-simulation; ON/OFF arms vs bound | R602-8 | `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97` |
| Tests | CLEAN (S2 optional; R602-4-S1/S2 optional) | `check_nvm_capture` + 5 mutations, `ci_scope --selftest`, `ci_events --check`, `suite_shards --selftest`, writer gate `--self-test` | R602-8 | `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97` |
| Docs | CLEAN (RESIDUE R602-7-R1 re-filed, R602-6-R1 carried; S1 optional) | Section 18 and UNRESOLVED 6 vs receipt; doc gates; PR body Round 8; author-r8 evidence packet | R602-8 | `d5cd863561ba1ee7bc6342fb1b00f57dd786bd97` |

## Execution receipts (this packet)

Every run started and finished at the exact head, and the clone ended byte-identical to it.

| Receipt | Command | Result |
|---|---|---|
| `receipts/merge_provenance.log` | `scripts/merge_provenance.sh REPO` | rc 0, facts above |
| `receipts/gates/*.log`, `*.rc` | `scripts/gates.sh REPO OUT` | capture gate rc 0; five mutations rc 1 with `FAIL:` by name; `ci_scope --selftest` rc 0; `ci_events --check` rc 0 |
| `receipts/hostsuite/writer_gate_selftest.log` | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 16` | rc 0, "OK across 5 shape(s), and every planted defect reddened", 3 min 21 s |
| `receipts/docgates/*.log`, `*.rc` | `scripts/docgates.sh REPO OUT` | all rc 0. em-dash and TOC were re-run with the pinned Markdown renderer environment after an rc-2 "renderer not installed" refusal with the default interpreter. |
| `receipts/receipt_compare.txt` | `scripts/receipt_compare.py OLD NEW` | only 5 metadata keys differ; arms identical |
| `receipts/arm_vs_receipt.txt` | `scripts/arm_vs_receipt.py RECEIPT EVIDENCE_DIR` | all six arms' published rows equal the receipt (the capture-log regex column is not applicable: the build logs carry no CAPTURE rows) |
| `receipts/artifacts_vs_receipt.txt` | `scripts/artifacts_vs_receipt.py RECEIPT INDEX OLD` | BIOS and firmware hashes match the receipt and round 7 for all arms |
| `receipts/section18_vs_receipt.txt` | `scripts/section18_vs_receipt.py RECEIPT DOC` | 16/16 lines present |
| `receipts/capture_rtl_map.txt` | `scripts/capture_rtl_map.py REPO c6bd08c6 fa820988` | 7 of 8 dev RTL files in the capture datapath list |
| `receipts/dev_closure.txt` | `scripts/dev_closure.sh REPO` | only `sw/litex/milan_soc.py` changed among lane inputs |
| `receipts/verilation_reports.txt` | extract from the published logs | round-7 vs round-8 source size differs |
| `receipts/evidence_provenance.txt` | sha256 of the downloaded public evidence and the script gap | as stated |
| `receipts/hosted_check_runs.tsv`, `receipts/hosted_workflow_runs.tsv` | read-only API snapshot, 09:30 UTC | see below |
| `receipts/checkout_integrity.txt` | git verification after all runs | HEAD, index and tree equal the head; 0 status lines; six gitlinks at their pins |

## Hosted evidence at this head (read-only snapshot, manager-owned)

The snapshot was taken at 2026-10-14 09:30 UTC.

- **Workflows.** Four `pull_request` runs exist at `d5cd8635`: docs, elaborate, rtl-fast and rtl-full. All four were still in progress.
- **Completed success (13):**
  - bdd-conformance, changes, docs-check-no-git and full-ci-gate;
  - firmware-aecp-mutants, firmware-srp-mutants, firmware-unit and firmware-verilator;
  - verilator-lint and wire-accountability;
  - Yosys shards 1/4, 2/4 and 3/4.
- **Skipped (1):** "Physical gPTP (nightly and manual)". It is a skipped context, not an executed job.
- **In progress (12):**
  - docs-check, elaborate, firmware-boundary, firmware-control-mutants and publication-census;
  - Verilator shards 0-4/5;
  - yosys-elaboration and Yosys shard 0/4.

No hosted job had failed at the snapshot. I make no claim about the unfinished jobs.

## Real limits

- **Capture not re-run here.** The product LiteX/RV32 SDK environment is not on this host's tool path, and the receipt binds Verilator 5.052, not the scoped 5.050. I verified the re-measure from its published per-arm results, artifact index and build logs, not by a re-run.
- **act_ci not run here.** Under this round's rules I did not run `scripts/act_ci.py --selftest`. That claim rests on the author's container receipt.
- **Long suites not re-run here.** Co-simulation, the builder bank, control-firmware phases, the Mark II store suite and the docs-check replica were not re-run. Their lane inputs are byte-identical to round 7, and dev's changes do not reach them (`dev_closure.txt`), except the Mark II suite's own dev edit, which adds an orthogonal `--build-only` mode.
- **No manager source bank.** No manager source bank ran at this exact head, and none is claimed or inferred.
- **No hardware proof.** Physical calibration was NOT RUN. Field skips and simulated capture timing are not hardware proof. The capture is a deterministic simulated scenario: no phase sweep, no worst-case contention bound, no silicon memory ordering. The boot read cost remains an estimate. The writer-restart model assumes retained fabric/window state.
- **Merge candidate not covered.** This review covers the source head. It does not cover the current-dev merge candidate the manager builds at the merge turn: source base `e8454e27`, live dev `fa820988` at review time.

## Pending manager duties

- Accept the hosted checks at `d5cd8635` once the 12 in-progress jobs finish, and run act at this head.
- Build and validate the current-dev merge candidate (builder and native banks), and link its receipts on the PR.
- Carry RESIDUE R602-7-R1 (re-filed at `:1632-1642` with the exact fix above) and R602-6-R1 to the residue checklist.
- Optionally act on R602-8-S1: publish `author-r8/scripts/r8/`.
- Optionally open an Issue for R602-8-S2: bind the capture-SoC RTL in the receipt.

R602-8 FINISHED
