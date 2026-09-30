[R412] POSITIVE - exact head b3ae17233eb9dd5934255f4018da7d45a159b5ac

Round R412-5, cleared-context internal review of PR #623 (#70 lane 2). Exact head `b3ae17233eb9dd5934255f4018da7d45a159b5ac`, tree `02d9741fb9f57d81c758ae42adea26ed9694f647`. It has two commits on round-4 head `5b4a47e9`: `ae203a01` (item 1) and `b3ae1723` (item 2). Assignment: #70 comment 5911775903. Ruling record: #495 comment 5911779020.

All five lenses were applied at this head, and each is clean. There is one SUGGESTION (S1), and it does not affect coverage. R412-4 F1 and R413-4 F1 are resolved. Every earlier finding stays resolved.

## Sources reconstructed, in order

1. `AGENTS.md` sections 3 and 5 to 8, and the review bar in `CONTRIBUTING.md`.
2. `docs/README.md`, for the authority order.
3. The body of Issue #70.
4. The round-5 assignment and ruling (#70 5911775903).
5. The widened #495 entry 5911779020, and the two entries it supersedes, 5906401051 and 5909985902.
6. The census's standing limits, `docs/integration/BAREMETAL_FIRMWARE.md:808-827` ("What the census does NOT observe").
7. `git diff 5b4a47e9..b3ae1723`, the two commit objects, and the scope of the lane diff since `79c36963`.
8. The PR body at review time (`receipts/pr623_body_snapshot.md`).
9. The public author packet `review-evidence/70L2-r1/author-r5` at evidence commit `851e5aa7`: REVIEW-READY, HANDOFF and receipts.
10. After my own pass over the diff: the round-4 public reviews R412-4 (5911768447) and R413-4 (5911515860). I read them only for their findings and dispositions. I did not read any round-5 report by another reviewer.

## Method

All probes ran on disposable copies of this clone under the packet's `scratch/`. The review clone itself was never edited. `receipts/clone_integrity.log` shows HEAD, tree, index tree and an empty status (ignored and untracked included). All 976 index entries match in bytes and mode. The gitlinks are `gptp-processor 5dce647a`, `protocol-processor b2db3a97` and `third_party/verilog-axis 48ff7a7e`, all clean, and `external` is not initialised. Result: `INTEGRITY OK`.

- **Census compiler.** The provisioned RV32 SDK selector (`riscv32-linux-gcc.br_real (Buildroot 2026.05) 14.3.0`) was run with `--require-rv32` in argv, so nothing stood down.
- **Harness.** The scripts are my own and portable:
  - `probe_lib.py` builds each variant as exact, count-checked text edits on a copy.
  - `run_gate1b.py` runs only `test_baremetal_profile_contract()`, not the builder bank.
  - An observation hook prints three things: the per-break premise bytes, the pins each refusal names, and one line after the verdict controls. In stop mode that line ends the run with rc 0. The hook never changes a verdict.
  - `run_variants.sh` runs at most 8 variants at a time in stop mode. `run_whole.sh` runs the whole gate function. `run_gate1b_absent.sh` runs the gate with every cross-compiler candidate hidden.
- **Nothing reused.** No earlier reviewer's or author's script was run or copied. Their mutant shapes were rebuilt independently where named (see the mapping under Real limits).

## Item 1 (`ae203a01`): the verdict limit as the callee class, with no count

Judgment: **met as ruled.**

- **The six places R412-4 listed now state the class.** In each, a called function writing through any pointer with no relocation on the verdict's bytes is not seen, and its shapes are examples:
  - the rule comment, `sw/builder/test_builder.py:1653-1674` ("THE LIMIT, stated rather than closed ... Its shapes include, and are not limited to");
  - `docs/integration/BAREMETAL_FIRMWARE.md:966-1007` ("What the pins do not see, stated rather than closed ... examples and not a complete list"). The "Outside the two limits below" consequence is gone.
  - the refusal row, `BAREMETAL_FIRMWARE.md:1651` ("are examples, not a complete list");
  - the printed closing line, `test_builder.py:17233-17237`. It prints verbatim in `receipts/H0_head.whole.log`.
  - the PR body, Round 5 item 1.
  - The docstring (`test_builder.py:6920-6931`) and `CHANGELOG.md:66-67` were aligned as well.
- **No text counts limits.** `receipts/text_scan.log` finds no "two limits", "outside the two", "two writes put", "two addresses reach", "second limit", "both limits" or "four-byte range" in `CHANGELOG.md`, `docs/` or `sw/builder/`. The remaining hits are unrelated texts, such as the one-second limit and "the two authorized exceptions". In the PR body, "four-byte range" appears only as a quotation of the corrected texts. The round-4 history section there no longer counts.
- **The link to the standing limit is right.** "The first entry under What the census does NOT observe" is the callee entry at `BAREMETAL_FIRMWARE.md:811-821`.
- **The probes stay accepted and match the class's words.** Each was planted as the first statement of `nvm_boot()` in the shipping firmware, and the whole gate function ran. Every one returned `GATE1B PASS` with "kept the slot of aem_loaded", 17/17 breaks refused, and the class line printed (`receipts/L*_*.whole.log`, `receipts/whole_summary.txt`):

  | Probe (my own) | Pointer | Words of the class it matches |
  |---|---|---|
  | L1 `csr_pointer_sscanf` | `(char *)(uintptr_t)milan_read(MILAN_ID)` | "a pointer read from a CSR or NVM" |
  | L2 `stack_runtime_sscanf` | `loc + (int)milan_read(MILAN_ID)`, where `loc` is a frame array | "a frame address plus a run-time offset" |
  | L3 callee return | `(char *)(uintptr_t)strtoul(...)` | "returned by a callee" |
  | L4 literal | `(char *)0x40001000u` handed to `sscanf()` | "a literal address" |
  | L5 the unit's own store at a literal | `*(volatile char *)0x40001000u = 1;` | "a store this unit makes through it is placed at that number and ... taken not to land on the verdict" (`:983-985`), and the row's "a store this unit makes that the resolver places at a number" |
  | L6 neighbour overrun | `sscanf("%s")` into a 4-byte static declared before the verdict | "another object's address carried outside that object" |
  | L7 the unit's store through a neighbour pointer | `int *p = milan_nbr_i; p[1] = 5;` | "a store this unit makes through such a pointer at an offset the resolver places on the neighbour ... is not seen either" |

  L1 and L2 are the shapes of R412-4's `csr_pointer_sscanf` and `stack_runtime_sscanf`, rebuilt from their description in R412-4 F1. L4 and L6 are the round-3 and round-4 shapes.

## Item 2 (`b3ae1723`): breaks on bytes +2 and +3

Judgment: **met.**

- **The new breaks.** `test_builder.py:14649-14662` adds the +2 and +3 breaks beside round 4's +1, and they are graded at `:14738-14741`. The premise is checked per break to its one byte at `:14751-14771` (`assert reached == [offset]`).
- **The unmutated head.** In stop mode the premise lines print `+1 reached [1]`, `+2 reached [2]` and `+3 reached [3]`. Each of the three interior breaks is refused naming the escape pin and no other. The run ends with `kept=['aem_loaded'] refused=17/17 interior_bytes=[1, 2, 3]` (`receipts/H0_head.stop.log`). The whole gate function passes in 937 s (`receipts/H0_head.whole.log`).
- **With every cross-compiler candidate hidden.** The gate passes in 525 s, and the census stands down as designed (`receipts/H0_head.absent.log`).
- **Census narrowings** (`receipts/variants_summary.txt`). Each is killed by the break on the byte it drops:

  | Mutant (my own) | Narrowing | Result |
  |---|---|---|
  | D0 | `rv32_image_references()` skips byte +0 | KILLED by the shipping firmware ("enters entity_advertise() with [None]") |
  | D1, D2, D3 | skips byte +1, +2 or +3 | each KILLED by "the resolver accepted a neighbour's address folded onto byte +k" |
  | P1 | reads the first byte only (the M9 shape) | KILLED by the +1 break |
  | P2 | reads the first two bytes (the N1 and N4 shapes) | KILLED by the +2 break |
  | P3 | reads the first three bytes (the N2 shape) | KILLED by the +3 break |
  | R1, R2, R3 | the same prefixes applied to `verdict_image_pins()`'s own range | KILLED by +1, +2 and +3 |
  | S1 | the pins' range starts at +1 | KILLED by the shipping firmware |
  | E2, E3 | `%lo` on an `addi` at byte +2 or +3 misread as an upper part | KILLED by the +2 and +3 breaks |

- **Counterfactual** (`receipts/counterfactual_summary.txt`). The new breaks, and only they, catch these narrowings:
  - The head with the +2 and +3 breaks removed passes 15/15, as does that tree under P2, P3 or "drop only +2".
  - The head with no interior break passes 14/14 under a first-byte-only census.
  - This also confirms the page's history sentence at `BAREMETAL_FIRMWARE.md:1038-1041`.
- **Pin removals, the M1-M8 class** (`receipts/pin_mutants_summary.txt`). All 8 are killed:
  - K1, no write pin: the second assignment is accepted.
  - K2, no escape pin: `&aem_loaded` is refused without naming escape.
  - K3, no name pin: `alias_sscanf` is refused without naming the name pin.
  - K4, no locality pin: the external-linkage break is refused without naming it.
  - K5, no AUIPC pin: the AUIPC break is accepted.
  - K6, no address pin: the address break is refused without naming it.
  - K7, no second-unit pin: the second-unit break is accepted.
  - K8, the image's store half removed: the `#ifndef __PIE__` write is accepted.
- **Premise mutants.** The premise is not vacuous:
  - Q1: the +2 break moved onto the neighbour fails on `byte(s) []`.
  - Q2: the +3 break moved onto +1 fails on `[1]`.
  - Q3: the +2 break moved onto +0 fails on `[0]`.
  - Q4: the +3 break moved onto +1, with the premise weakened to membership, still fails on `[1]`.
  - Q0: under round 4's weaker premise ("non-empty and not byte 0"), the +3 break moved onto +1 passes silently as `interior_bytes=[1, 2, 1]`. So the exact premise is what makes each break measure its byte.
- **The texts match what the controls measure.**
  - `test_builder.py:14612-14621` and `BAREMETAL_FIRMWARE.md:1035-1045` say that a census which stops reading any of +1..+3 no longer refuses the break on that byte, and that byte +0 is guarded by the shipping firmware. D0 to D3 show exactly this.
  - The closing line (`:17226-17232`) prints "3 of them reaching it at one byte each, +1, +2, +3".
  - "seventeen breaks" (`:1011`) and the three-break table row agree with the 17 graded.

## Findings

### S1 - SUGGESTION - Docs, Robustness - the closure sentence no longer names the RAM map for the unit's own store at a literal address

- **Where:**
  - `docs/integration/BAREMETAL_FIRMWARE.md:1005-1007`: "Closing this needs call-argument provenance, or a memory-safety check on every call inside `nvm_boot()`. It is recorded on the residue checklist (#495)".
  - `sw/builder/test_builder.py:1673-1674`, the same sentence.
  - #495 5911779020.
- **Evidence:**
  - The unit's own store at a literal address (L5) passes the whole gate with the slot kept (`receipts/L5_unit_literal_store.whole.log`). The page states this as unseen (`:983-985`, and the row at `:1651`).
  - It is not a call, so neither closure named in the sentence reaches it.
  - The round-4 text named its closure: "Closing this needs the SoC's RAM map in the gate, which is a separate rule on the residue checklist (#495)". The #495 entry 5906401051 recorded the same thing.
  - 5911779020 supersedes 5906401051, but its class and closure cover only a called function. The page keeps just "only the SoC's RAM map could place it there" (`:982-983`).
- **Why not MINOR:**
  - No proof is overclaimed. The page states the unit's store at a number as unseen, and gives it as the standing model's assumption (`:966-968`, and the census's second standing entry at `:822-825`).
  - "It" in the closure sentence reads naturally as the callee class, which is what the ruling asked the texts to state.
- **Impact:** a reader who closes the callee class by call-argument provenance could take the section as closed, while the unit's own literal-address store stays unseen. The residue record no longer carries the RAM-map closure that 5906401051 did.
- **Suggested outcome (optional):**
  - Either the manager confirms that the unit's own store at a literal address stays tracked on #495 with its RAM-map closure,
  - or a later text change adds, beside the closure sentence, that the unit's own stores at a number are closed only by the SoC RAM map.
- **Verification:** re-read `:981-1007` and the #495 record. L5 then matches a stated closure.

No other finding.

## Per-lens results at this head

```text
[R412] PASS Conformance - #70 5911775903 items 1-2 against BAREMETAL_FIRMWARE.md:966-1045,1651; test_builder.py:1653-1674,6920-6931,14612-14771,17226-17237; CHANGELOG.md:66-67; PR body Round 5 (receipts/pr623_body_snapshot.md); receipts/text_scan.log; receipts/L*_*.whole.log - every ruled place states the class with examples and no count; the +2/+3 breaks exist with exact premises; N1/N2/N4/M9 shapes killed, M1-M8 class killed, head passes with slot kept
[R412] PASS RTL - receipts/scope_and_digest.log - round diff is CHANGELOG.md, BAREMETAL_FIRMWARE.md, test_builder.py only; git diff 0a80abcb..b3ae1723 over hdl, tb, sw/firmware, syn, constraints, sw/litex and all four gitlinks is empty; milan_baremetal.c sha256 a73ecc25...0eb3 equals measurements.json product_firmware_sha256; gitlinks b2db3a97/5dce647a/48ff7a7e/efeb541a unchanged
[R412] PASS Robustness - receipts/L1..L7 whole-gate plants, receipts/H0_head.absent.log, receipts/Q*_*.stop.log - run-time, callee-return, literal, overrun and unit-store shapes behave as the stated class and model say; feature-absent arm (every cross-compiler hidden) passes; misplaced breaks fail their premise before grading
[R412] PASS Tests - receipts/variants_summary.txt, pin_mutants_summary.txt, counterfactual_summary.txt, H0_head.stop.log, H0_head.whole.log - each new break fails for the narrowing it claims (D1-D3, P1-P3, R1-R3, E2-E3 killed; survive 15/15 without them), byte +0 guarded by the shipping firmware (D0, S1), pin removals K1-K8 killed, premise mutants Q1-Q4 refused, Q0 shows the exact premise is needed
[R412] PASS Docs - BAREMETAL_FIRMWARE.md:966-1045,1651; CHANGELOG.md:66-67; PR body; receipts/docs_gates.log (docs_check 0 findings/177 md, check_doc_paths OK 861, check_doc_style OK 22, check_archive OK 21, gen_toc --check OK 119, check_em_dash 0/568 lines, check_py_idiom rc 0, measure_test_evidence --check PASS, git diff --check 79c36963..HEAD empty; pinned cmarkgfm/html5lib renderer) - texts match measured behaviour; S1 is a SUGGESTION
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 5911775903 items 1 and 2 against `BAREMETAL_FIRMWARE.md:966-1045,1651`, `test_builder.py:1653-1674,6920-6931,14612-14771,17226-17237`, `CHANGELOG.md:66-67` and the PR body; the class probes L1-L7; the mutant tables | R412-5 | b3ae17233eb9dd5934255f4018da7d45a159b5ac |
| RTL | CLEAN | `receipts/scope_and_digest.log`: nothing in RTL, TB, firmware, SoC or submodule scope changed since `0a80abcb`; the firmware digest equals the capture receipt; commits are one line with no trailers | R412-5 (the RTL scope is unchanged since R413-3's POSITIVE at `0a80abcb` and R412-4's RTL PASS at `5b4a47e9`) | b3ae17233eb9dd5934255f4018da7d45a159b5ac |
| Robustness | CLEAN (S1 is a SUGGESTION) | Whole-gate plants L1-L7; the absent arm; premise mutants Q0-Q4 | R412-5 | b3ae17233eb9dd5934255f4018da7d45a159b5ac |
| Tests | CLEAN | Stop-mode head and 31 variants (the D, P, R, S, E, K, Q and C sets); the whole gate function at the head | R412-5 | b3ae17233eb9dd5934255f4018da7d45a159b5ac |
| Docs | CLEAN (S1 is a SUGGESTION) | The page, the refusal row, the CHANGELOG and the PR body; 8 docs and ratchet gates plus `git diff --check`, all rc 0 | R412-5 | b3ae17233eb9dd5934255f4018da7d45a159b5ac |

## Disposition of prior public review findings at this head

| Finding | At `b3ae1723` |
|---|---|
| R412-4 F1 (MINOR: the texts count two limits, and a run-time pointer handed to a callee is a third) | **Resolved as ruled.** All six places state the callee class with example shapes and no count. `csr_pointer_sscanf` and `stack_runtime_sscanf` stay accepted and match "a pointer read from a CSR or NVM" and "a frame address plus a run-time offset" (L1, L2) |
| R413-4 F1 (MINOR: the interior break measures byte +1 only; N1, N2 and N4 survive) | **Resolved.** The +2 and +3 breaks have exact premises. The N1/N4 shape (P2) is killed by +2 and the N2 shape (P3) by +3. Without the new breaks both survive, 15/15. The "four-byte range" texts are replaced by what the controls measure |
| R412-3 F2 (M9, first byte only) | Still resolved. P1 and R1 are killed by the +1 break |
| R412-3 F1 (neighbour-overrun limit) | Still resolved as ruled. It is now one example shape of the class, and L6 is accepted as stated |
| Findings of rounds 1-3 (R412-1/2, R413-1/2, and the alias and weakref class) | Resolved at round 3 (R413-3 POSITIVE at `0a80abcb`), and their scope is untouched this round. The alias, weakref, splice, paste, macro, PIE, data-word and AUIPC breaks are all among the 17 refused, and the K-set pin removals are killed |

## Real limits of this round

- **What I re-reviewed.** Only the round-5 delta. I did not re-review the whole lane diff `79c36963..b3ae1723`. For RTL, firmware, TB and SoC scope, I verified that it has not changed since the heads where earlier rounds covered it.
- **Which gates I ran.** Gate 1b's function alone, at the head and on probe copies. I did not run the full builder bank, the PP, gPTP or Yosys banks, `act`, or the hosted runs, as the assignment requires.
- **Stop mode.** It ends right after the verdict controls. It measures the controls, not the rest of gate 1b. Whole-gate runs cover the head (present and absent) and the seven class probes.
- **Earlier reviewers' scripts.** R412-3's `census_mutants_run.sh`, R413-4's `r413_census_stop_run.sh` and R412-4's probe hook were not run. I rebuilt their shapes myself from the published finding texts:
  - M9 → P1
  - N1, N4 → P2
  - N2 → P3
  - M1-M8 → K1-K8
  - `csr_pointer_sscanf`, `stack_runtime_sscanf` → L1, L2
- **Mutants are on the census as Python.** A narrowing spelled differently from the ones listed may exist. The kill set covers every single-byte drop, every prefix, and the pins' range.
- **Hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- **Hosted checks.** At snapshot time (`receipts/hosted_checks_b3ae1723.txt`), `rtl-fast` succeeded, as did Yosys shards 0-3, Verilator shards 0 and 3, `yosys-elaboration` and `verilator-lint`. Still in progress: Verilator shards 1, 2 and 4, `elaborate` and `docs-check`. Physical gPTP was skipped by design. The manager owns hosted and act acceptance.
- **Merge candidate.** Build and validate the final current-dev candidate at the merge turn (source base `79c36963`, live dev `ccdd07b5`), and run post-merge containment.
- **S1.** Decide whether the unit's own store at a literal address keeps a #495 record with its RAM-map closure, as 5906401051 had.
- **Evidence packaging.** The published `review-evidence/70L2-r1/author-r5/MANIFEST.sha256` does not verify: 85 of 127 files differ (`receipts/author_r5_manifest_check.log`). The local git blob ids equal the published tree, so the files are as published, and the mismatching files carry path placeholders such as `$VALIDATION_STORAGE`, consistent with a rewrite after hashing. Regenerate that manifest, or state the rewrite. This packet's judgments rest on its own receipts, not on that manifest.
- **Merge authorization.** A maintainer must explicitly authorize any merge.

R412-5 FINISHED
