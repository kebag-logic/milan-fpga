[R602] POSITIVE - exact head 9b32002cc0c3aafae9e864af7b4f08c1089a188a

# R602-7: internal cleared-context review of PR #715 / issue #671, round 7 (delta)

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. One new RESIDUE is filed (prose wording only, R602-7-R1). The earlier RESIDUE R602-6-R1 is carried unchanged, and two earlier SUGGESTIONs remain optional. All five lenses are CLEAN at `9b32002cc0c3aafae9e864af7b4f08c1089a188a` (tree `7ac62ffdcfcf060c763d5dd7d63ada7fdbeca40f`).

This is a source-review verdict on the round-7 delta only. It is not a manager source bank, it does not cover the current-dev merge candidate, and it is not hosted or act acceptance. Physical calibration was NOT RUN, and skipped field contexts are not hardware proof.

## Scope and reconstruction

- **Order of reading.** AGENTS.md and CONTRIBUTING.md (sections 3-7). The #671 body (Required; Acceptance 1-3). The round-6 ruling ([6112358549](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6112358549)) and the round-7 assignment ([6125761347](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6125761347)). The executor's round-6 and round-7 REVIEW READY posts. The capture harness README and `scripts/check_nvm_capture.py`. Then the diff `e8454e27..9b32002c` and the two new commits. Prior reviewers' findings were read only after this pass was complete.
- **Round-7 delta.** Two commits on `c7d0ad63`, the head that holds the two round-6 POSITIVEs:
  - `44416838`: a merge commit, parents `c7d0ad63` and dev `c6bd08c6`, tree `6bdf8b0d`;
  - `9b32002c`: changes only `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `tb/verilator/nvm_capture_cpu/measurements.json`.
- **Judged.** Only the merge and the re-measure, per the assignment's four items:
  1. the conflict resolution keeps both sides' statements;
  2. the receipt was re-measured at the merged tree and passes `check_nvm_capture` with the merged firmware digest within its bound;
  3. the files that differ from dev are exactly this branch's own, and nothing else changed;
  4. the round-6 term list, its fault classes and its removal controls still hold at the merge head.

## Findings

### R602-7-R1 - RESIDUE - Docs - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632-1639` - the receipt chain's relative references now name two receipts "the previous one"

- **Evidence.** The round-7 commit moved the round-5 line from "requires this remeasurement" to "required the previous one on #671" (line 1632). The round-4 line still reads "required the previous one" (line 1634), so two adjacent lines say "the previous one" about two different receipts. The pattern was already loose at `c7d0ad63`: round 2 (line 1638) also says "the previous one".
- **Impact.** A reader can still date each receipt from its linked assignment. No figure, hash, receipt identity, measurement, test or conformance claim changes. The text is wrong as wording only.
- **Why RESIDUE.** Purely prose. The measured identities (lines 1647-1651), the figures and the #621 lines are correct and were checked against the receipt (`receipts/capture_receipt_probes.log`).
- **Exact fix.** Replace the relative objects with named receipts:
  - line 1632: "required the round-5 receipt";
  - line 1634: "required the round-4 receipt";
  - line 1636: "required the round-3 receipt";
  - line 1638: "required the round-2 receipt, for the console report of the writer's hold";
  - line 1639: "required the first #671 receipt, for the boot read-fault rule".
- **Verification.** Reading lines 1629-1646 names each receipt once, and `scripts/docs_check.py` and `scripts/check_doc_style.py` stay at 0 findings.

### Prior findings at this head

| Prior IDs | Disposition at `9b32002c` | Evidence |
|---|---|---|
| R602-6-R1 (RESIDUE, Docs) | RETAINED, residue | `sw/firmware/nvm_hosttest/README.md:165-168` is byte-identical to `c7d0ad63`. The parenthetical still lists only the blank-other sequences. The round-6 exact fix still applies. |
| R602-4-S1 (SUGGESTION, Tests); R602-4-S2 (SUGGESTION, Tests, Robustness) | RETAINED, optional | Host suite and firmware are byte-identical to `c7d0ad63` (`receipts/merge_provenance.log`). Not taken up; not required. |
| R602-5-F1, R603-5-F1 (MAJOR) | RESOLVED, holds at merge head | Covered under item 4 below. `r_omit_trailer` and `r_omit_prefix_crc` are caught by their own words on three shapes (`writer_gate_selftest.log:111-116`). The independent removal probes give exactly 32 own-class findings and none from another class (`removal_probe_*.log`). |
| R603-4-F1 (MAJOR) | RESOLVED, holds | `r_digest_with_trailer` is caught by name in the head self-test. The firmware is byte-identical to `c7d0ad63`. |
| Every earlier F/S/R ID dispositioned RESOLVED at round 6 | RESOLVED, unchanged | None of their artifacts changed in the delta (`merge_provenance.log`: 12 of 15 branch files are byte-identical to `c7d0ad63`; the other three are the two judged files and the clean `test_builder.py` union). All their controls are still caught by name (`writer_gate_selftest.log`). |
| R603-2-OBS-1 / R602-2-S2 (prefill) | RETAINED OUTSIDE SCOPE | #717. |

## Delta facts established

**Item 3: merge provenance** (`receipts/merge_provenance.log`).
- `44416838` has two parents, `c7d0ad63` and `c6bd08c6`. Their merge base is the source base `e8454e27`.
- `git diff --name-only c6bd08c6 9b32002c` is exactly the 15 files of `e8454e27..c7d0ad63`.
- Every path outside that set equals dev, gitlinks included: protocol-processor `2ad2f845`, gptp-processor `7dda9c3b`, lwSRP `08ee86e8`, verilog-axis `48ff7a7e`, external `efeb541a`. There are no mode changes; the only `mode` lines are the branch's two new-file creations.
- Within the branch set, 12 files are byte-identical to `c7d0ad63`. The three that are not:
  - the design document;
  - the receipt;
  - `sw/builder/test_builder.py`. This was a clean union. Against dev it carries only the branch's 3+/1- (timeout 600 to 1200 s). Against `c7d0ad63` it carries exactly dev's gate-23m hunks. It parses.

**Item 1: design document.**
- Merged against dev, the document adds only:
  - the branch's #671 statements;
  - a reframing of dev's #621 receipt as "In parallel, on dev", which keeps its ruling link, commit, tree, firmware, both pins, the byte-identical-logs line, the drift line, its 13.86318 ms / 3.5345x / 10.63682 ms figures and its six-row table;
  - dev's receipt-opt-out sentence, kept verbatim (`:1743`).
- Merged against `c7d0ad63`, it adds only dev's statements. Nothing from either side is dropped, except the superseded current-receipt header (date and identities), which by construction names the newest receipt.
- `9b32002c` changes only:
  - the current-receipt header (date, assignment, merge, identities);
  - two "previous #671 receipt" lines;
  - the "All 96 captures repeat" line.

**Item 2: receipt** (`receipts/capture_receipt_probes.log`, `check_nvm_capture*.log`, `gptp_ucode_hash_head.log`).
- `check_nvm_capture.py` at the head: rc 0, `PASS: capture census, clocks, both timing arms and receipt agree`, with all eight built-in controls detected. Its five mutation arms (`bytes`, `records`, `clock`, `ignore-off-timing`, `receipt-opt-out`) each exit 1 with their named reasons.
- The receipt binds the head's firmware SHA-256 `497845e6...` and `run.py` `c230cb3e...` (dev's harness). Config hashes equal `sha256sum configs/*.yaml`.
- The gPTP ROM hash `fd3dad06...` was regenerated independently at the head with the builder and equals the receipt's. It also equals dev's receipt, since both use pin `7dda9c3b`.
- Tree `6bdf8b0d` equals the merge tree. Pins equal the head gitlinks.
- **Stale receipts are refused at the head tree**, in a disposable git-backed export:
  - the round-5 receipt (`c7d0ad63`) fails with `measurement harness changed`;
  - dev's receipt (`c6bd08c6`) fails with `product firmware changed`.

  So the receipt could not have been carried over or hand-merged from either side. It had to be rebuilt against the merged harness and firmware.
- **Hand-edits are refused:**
  - one 8x8/50 OFF row one tick over half the floor (2,450,001 cycles) fails `exceeds half the 49 ms hold floor`;
  - the worst 1x1 ON row edited by one cycle with its summary kept fails `receipt summary differs from rows`;
  - a one-byte firmware change fails `product firmware changed`.
- **Bound.** The 8x8/50 MHz maximum is 13.86328 ms against 24.5 ms: margin 10.63672 ms, 3.5345x the 49 ms floor. The 1x1 maximum is 3.96548 ms (12.3566x). The 100 MHz comparison is 10.42973 ms. All six section-18 table rows and the identity lines were regenerated from the receipt and match the document.
- The "All 96 captures repeat" claim holds: all 96 rows equal the round-5 receipt's, in every field. "And so did the one before it" holds too: the round-4 receipt at `7bc7ceca` also gives 13.86328 ms.

**Plausibility of unchanged cycles.** The merge brings capture-SoC changes from dev (`milan_soc.py` CSR-crossing storage mapping, `milan_csr.sv` read path, mailbox, datapath) that neither earlier receipt measured.
- The `milan_soc.py` changes add no LiteX CSR, constant or memory-map entry, and document unchanged FIFO depth, width and read latency. That is consistent with identical BIOS and instrumented-firmware hashes and identical cycle counts.
- The cycle counts themselves can only be reproduced with the measurement toolchain, which is not on this host. See Real limits.

**Item 4: round-6 terms at the merge head** (`receipts/writer_gate_selftest.log`, `removal_probe_*.log`).
- `test_nvm_firmware.py --self-test --jobs 12` at the head: rc 0 in 151 s, `OK across 5 shape(s), and every planted defect reddened`. That covers:
  - 54 named control catches (18 #671 controls x 3 shapes), including `restart_at_zero` (Acceptance 2) and the four `r_omit_*` controls, each caught by its own words "which differ only in their <term>" on arty 4x4, 1x1 and 8x8;
  - all 9 comparison-check arms: four terms without their class, four without their control, and one extra firmware term.
- **Independent removal probes.** In a disposable copy of the head, the trailer term (`a.tail == b.tail`) and, separately, the prefix-CRC term (`a.digest == b.digest`) were replaced by `1`, and the ordinary gate was run on 8x8. Each exits 1 with exactly 32 findings naming its own term and none naming another term. The production comparison `milan_baremetal.c:776-780` is byte-identical to `c7d0ad63`.
- **Co-simulation** at the head bytes, run in a disposable export with Verilator 5.050: 465/465 checks PASS and 39/39 mutants killed by their named check, in 326 s. Its RTL and driver inputs are byte-identical to `c7d0ad63`. The one dev RTL file near it, `KL_pp_shadow.sv`, is not compiled by this suite.

## Lens results

`[R602] PASS Conformance - receipts/merge_provenance.log; SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1626-1699,1743,1841-1860; measurements.json at 9b32002c; receipts/check_nvm_capture.log; receipts/writer_gate_selftest.log - the four round-7 assignment items and #671 Acceptance 1-3 at the merge head`
- Item 1: both sides' statements stand.
- Item 2: re-measured at the merged tree, not carried over. Stale receipts are refused, the gate passes, and 13.86328 ms is within 24.5 ms.
- Item 3: the files that differ from dev are exactly the branch's 15. There is no other change.
- Item 4: the term list, classes and controls hold.
- #671 Acceptance 1-2: the unchanged firmware, with `restart_at_zero` caught on three shapes. Acceptance 3: the write path is unchanged and co-sim passes 465/465.

`[R602] PASS RTL - git diff c6bd08c6 9b32002c over hdl, protocol-processor, gptp-processor, third_party, external, syn, constraints (empty: receipts/merge_provenance.log "non-branch paths equal dev"); sw/litex/milan_soc.py dev hunks e8454e27..c6bd08c6; receipts/nvm_cosim.log - the branch adds no RTL; the merged RTL and gitlinks are dev's byte for byte; the dev capture-SoC hunks add no CSR, constant or memory-map entry and state unchanged FIFO latency, consistent with the unchanged BIOS hash and cycle counts`

`[R602] PASS Robustness - receipts/capture_receipt_probes.log (6 refusal probes); receipts/removal_probe_trailer.log, removal_probe_prefix.log; receipts/check_nvm_capture_mut_*.log - the gate fails on stale or hand-edited receipts, an over-bound row and a firmware edit; each comparison term removed alone is caught by its own class only; the merge leaves the boot read-fault paths (milan_baremetal.c:776-815) byte-identical`

`[R602] PASS Tests - receipts/writer_gate_selftest.log (rc 0, 5 shapes, 54 named control catches plus 9 comparison arms); receipts/check_nvm_capture*.log (pass plus 5 mutation arms rc 1); receipts/nvm_cosim.log (465/465, 39/39); sw/builder/test_builder.py merged hunk (timeout 1200 s; dev gate 23m kept) - every control the round-6 bar names still reddens at the merge head; the merged builder test file is the clean union`

`[R602] PASS Docs - SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1626-1699,1743,1841-1860 at 9b32002c against measurements.json and dev c6bd08c6; receipts/docs_check.log (0 findings, 204 md files); receipts/em_dash.log (0 over 362 added lines, base c6bd08c6); receipts/doc_style.log (OK) - every figure and identity matches the receipt and both sides' statements stand; RESIDUE R602-7-R1 (wording only) and carried R602-6-R1 leave the lens clean`

## Reviewer-owned completion ledger (this round)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Merge provenance, design doc section 18 and UNRESOLVED 6, receipt, capture gate, writer gate self-test | R602-7 | `9b32002cc0c3aafae9e864af7b4f08c1089a188a` |
| RTL | CLEAN | Dev-only RTL and gitlinks (equal to dev), `milan_soc.py` dev hunks, co-sim | R602-7 | `9b32002cc0c3aafae9e864af7b4f08c1089a188a` |
| Robustness | CLEAN | 6 receipt refusal probes, 2 term-removal probes, 5 gate mutation arms | R602-7 | `9b32002cc0c3aafae9e864af7b4f08c1089a188a` |
| Tests | CLEAN | Writer gate self-test, capture gate and arms, co-sim 465/39, merged `test_builder.py` | R602-7 | `9b32002cc0c3aafae9e864af7b4f08c1089a188a` |
| Docs | CLEAN (RESIDUE R602-7-R1 filed; R602-6-R1 carried) | Design doc vs receipt and dev, docs_check, em-dash, doc-style | R602-7 | `9b32002cc0c3aafae9e864af7b4f08c1089a188a` |

## Execution receipts (this packet)

| Run | Result | Receipt |
|---|---|---|
| `check_nvm_capture.py` and 5 `--mutation` arms | rc 0; arms rc 1, each with its named reason | `receipts/check_nvm_capture*.log` |
| `scripts/capture_receipt_probes.py` (disposable export) | rc 0, 6/6 probes as required, 96/96 rows equal round 5, table and identity lines match | `receipts/capture_receipt_probes.log` |
| `scripts/gptp_ucode_hash.py` | `fd3dad06...` for both capture shapes, equal to the receipt | `receipts/gptp_ucode_hash_head.log` |
| `test_nvm_firmware.py --self-test --jobs 12` | rc 0, 151 s | `receipts/writer_gate_selftest.log`, `.rc`, `.secs` |
| `scripts/removal_probe.sh` trailer and prefix (8x8) | rc 1 each, 32 own-term findings, 0 other-term | `receipts/removal_probe_trailer.log`, `removal_probe_prefix.log` |
| `nvm_cosim/run_cases.py --shapes 1x1,8x8` (Verilator 5.050, disposable export) | rc 0, 465/465, 39/39, 326 s | `receipts/nvm_cosim.log`, `.rc`, `.secs` |
| `docs_check.py`; `check_em_dash.py --base c6bd08c6`; `check_doc_style.py` | rc 0, rc 0, rc 0 | `receipts/docs_check.log`, `em_dash.log`, `doc_style.log` |
| Merge provenance | as stated above | `receipts/merge_provenance.log` |
| Clone integrity after all runs | HEAD and index tree `7ac62ffd`, 0 status lines including ignored; gitlinks and submodule checkouts at the pinned commits, clean | `receipts/clone_integrity.log` |
| Hosted checks, exact head (snapshot 2026-10-12T16:59:35Z) | Completed and successful: bdd-conformance, changes, docs-check-no-git, full-ci-gate, publication-census, verilator-lint, wire-accountability, yosys-elaboration, Yosys shards 0-3. In progress: docs-check, elaborate, firmware-unit, Verilator shards 0-4. Skipped context: Physical gPTP | `receipts/hosted_checks_snapshot.txt` |

## Real limits

- **The capture timing was not reproduced here.** Re-running `run.py` needs the product LiteX tree, the pinned CPU netlist, the RV32 SDK and Verilator 5.052, and none are on this host. The cycle counts, and the claim that they come from `run.py` at `44416838`, rest on:
  - the executor's statement;
  - the receipt's internal consistency, regraded by the gate;
  - hashes this review verified independently: firmware, harness, configs, gPTP ROM, tree and pins;
  - proof that neither side's receipt passes at the merged tree.

  The BIOS, instrumented-firmware and CPU-netlist hashes, and the 96 row values, were not independently recomputed.
- The em-dash gate ran under an existing local renderer environment whose packages are the pinned names (`html5lib 1.1`, `cmarkgfm`). No install was made.
- No manager source bank was run or inferred. The full builder, parent, PP, gPTP and Yosys banks were not run here (not allowed). The firmware-unit replica and lint/BDD were not re-run, since their inputs are byte-identical to `c7d0ad63` except dev's.
- Physical calibration was NOT RUN. The skipped Physical gPTP context is not hardware proof. All timing is simulation only.

## Pending manager duties

- Hosted and act acceptance of the exact head. docs-check, elaborate, firmware-unit and the Verilator shards were still in progress at the snapshot. docs-check is the hosted home of `check_nvm_capture` and the writer gate.
- Current-dev merge-candidate validation (builder and native banks) at the merge turn, on live dev.
- Publish `44416838` and `9b32002c` together. The merge commit alone fails the capture gate by design (confirmed here: the round-5 receipt at the merged tree fails on the harness hash).
- Carry RESIDUE R602-7-R1 and R602-6-R1 to the residue checklist.
- The merge needs maintainer authorization and the full completion bar, including the second independent review of this head.

R602-7 FINISHED
