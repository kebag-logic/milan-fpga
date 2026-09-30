# [A461] #70 lane 2 round 5 handoff (PR #623)

Status: **item 1 done (`ae203a01`), item 2 done (`b3ae1723`)**. Every gate is rc 0 at
`b3ae1723` (clean tree, physical path, never piped), both builder banks included, and every
reviewer script the assignment names gives the expected outcome there. REVIEW READY is posted.

- Branch `70-lane2-pin-d352`, local only. Start head `5b4a47e99f5a453832ccabccfbf4aae116d6fea0`.
- End head `b3ae17233eb9dd5934255f4018da7d45a159b5ac`, tree `02d9741fb9f57d81c758ae42adea26ed9694f647`:
  30 commits on dev `79c36963`, two this round, `ae203a01` (item 1) and `b3ae1723` (item 2).
  Processor pin `b2db3a97`, unchanged. No push, no PR edit.
- Assignment: round 5 on #70, comment 5911775903. Also read: the ruling 5894183475, the round-4
  assignment 5909983141 and its #495 record 5909985902, the widened #495 entry 5911779020, the
  reviews R412-4 (5911768447) and R413-4 (5911515860) in full, #70's lane-2 records (TAKEN, STOP,
  REVIEW READY and rulings of rounds 1 to 4), the author packets 70-a448, 70-a455, 70-a457 and
  70-a460, and the review packets 70L2-r412-3, 70L2-r412-4 and 70L2-r413-4.
- On #70: TAKEN 5911791356, REVIEW READY 5912923414 (text in `REVIEW-READY.md`). Nothing else
  was posted, and no comment was edited or deleted.

## Item 1: R412-4 F1, the callee class with no count (`ae203a01`)

The ruling states the limit as one class: a called function that writes through any pointer
carrying no relocation on the verdict's bytes is not seen by the pins. Its shapes are examples,
not a closed list. It is the census's standing callee limit (`BAREMETAL_FIRMWARE.md:811-821`)
applied to the verdict.

The six places R412-4 lists, at `b3ae1723`:

| Place | Before (`5b4a47e9`) | Now |
|---|---|---|
| `sw/builder/test_builder.py:1647-1651` (rule comment, the claim) | "... the only one, so outside the two limits below the word this function stored is still the word it reads back after the call" | "... milan_init()'s one store is the only one. A static that fails any pin is forgotten here as every other one is." The consequence is dropped. |
| `sw/builder/test_builder.py:1653-1674` (rule comment, the limit) | "LIMITS ...: a reference is found by its relocation, and two addresses reach the static's bytes with no relocation on them", then two bullets | "THE LIMIT, stated rather than closed: a reference is found by its relocation, so a called function that writes through any pointer carrying no relocation on the static's bytes is not seen, since a call's arguments are recorded and not judged. It is the census's standing callee limit applied to the verdict (#495). Its shapes include, and are not limited to:" a literal address; another object's address carried outside that object; "a pointer of run-time origin: a CSR or NVM read, a callee's return, or a frame address plus a run-time offset". Then "Closing it needs call-argument provenance or a memory-safety check on every call inside nvm_boot(), and this gate proves neither." |
| `docs/integration/BAREMETAL_FIRMWARE.md:966-972` (the claim) | "Outside the two limits below, the word that store wrote is the word read back after `nvm_boot()`." | dropped |
| `docs/integration/BAREMETAL_FIRMWARE.md:973-1007` (the limits) | "**Two limits, stated rather than closed.** ... two addresses reach the verdict's bytes with no relocation on them" | "**What the pins do not see, stated rather than closed.**" The class in one paragraph, tied to "What the census does NOT observe"; three example shapes, "examples and not a complete list", the third being "**A pointer of run-time origin.** A pointer read from a CSR or NVM, returned by a callee, or formed as a frame address plus a run-time offset can reach the verdict's bytes with no relocation on them", with R412-4's two probes as its examples; "Closing this needs call-argument provenance, or a memory-safety check on every call inside `nvm_boot()`. It is recorded on the residue checklist (#495), and gate 1b is not a memory-safety prover." |
| `docs/integration/BAREMETAL_FIRMWARE.md:1651` (refusal row) | "Two writes put no relocation on its storage and are outside these pins: one through a literal address, and one through another object's address ..." | "A called function writing through any pointer with no relocation on its storage is outside these pins, whatever the pointer's origin, and so is a store this unit makes that the resolver places at a number or on another static. A literal address, another object's address carried outside that object, and a pointer read from a CSR or NVM, returned by a callee or formed as a frame address plus a run-time offset are examples, not a complete list" |
| `sw/builder/test_builder.py:17233-17237` (the printed closing line) | "; two writes put no relocation on its storage and are outside these pins: one through a literal address, and one through another object's address carried outside that object, such as a called function's overrun of a neighbouring static" | "; a called function writing through any pointer with no relocation on its storage is outside these pins, whatever the pointer's origin, such as a literal address, another object's address carried outside that object, a CSR or NVM read, a callee's return or a frame address plus a run-time offset" |
| PR body | round 4 item 1 "Two addresses reach those bytes ... both are stated limits" | a Round 5 section states the class; round 4's and round 3's sentences no longer count ("stated limits", "the stated limit", "state the callee limit") |

Two more places carried the two-shape wording and were aligned, not listed by R412-4:
- `sw/builder/test_builder.py:6920-6931`, the `verdict_image_pins()` docstring (R412-4 judged it
  accurate; its list after "passes:" now reads "whatever its origin. Such pointers include ...",
  adding the run-time shape). The function is 99 lines, under the idiom ratchet's 100.
- `CHANGELOG.md:66-67`: "Writes via pointers without a verdict relocation stay outside them." and
  "Examples: a literal, another object's overrun, a run-time pointer." (the doc-style gate's
  ten-word bound).

`git grep` over the tree finds no gate-1b text saying "two limits", "two writes", "two addresses",
"second limit", "both limits" or "outside the two".

`rv32_step()` is 95 lines (was 97).

## Item 2: R413-4 F1, breaks on bytes +2 and +3 (`b3ae1723`)

- `sw/builder/test_builder.py:14648-14662`, `verdict_interior_breaks`: three breaks keyed by the
  byte, each the AEM-first base with `static int milan_verdict_next;` declared just after the
  verdict and `(void)sscanf("\001", "%c", (char *)(&milan_verdict_next - 1) + k);` opening
  `nvm_boot()`, for k = 1, 2, 3. The +1 break is round 4's, byte for byte, so the round-4
  reviews' premise mutants (A460's P1, P2; R412-4's B1, B2) still apply to it unchanged.
- `:14738-14741`, three `verdict_pin_breaks` entries, "a neighbour's address folded onto byte +k
  of aem_loaded and handed to sscanf() inside nvm_boot()", pins `(VERDICT_PIN_ESCAPE,)`.
- `:14746-14771`, the premise check, now per break and exact: the relocation targets from
  `nvm_boot()` on the verdict's bytes, read on the image directly, must be exactly `[k]`
  (round 4 asked for non-empty and not byte 0). `verdict_interior_bytes` (the name the round-4
  external review's stop script prints) collects the bytes reached.
- `:17226-17232`, the closing line: "refused 17/17 planted pin breaks on the verdict, each naming
  its pins, 3 of them reaching it at one byte each, +1, +2, +3 of its storage, so a census that
  stops reading any of those bytes no longer refuses the break on it" (was "one of them reaching
  it only at byte(s) +1 of its storage, which measures the census's four-byte range").
- `:14612-14621`, the comment over the controls: "The last three name no verdict at all ... Each
  one's only reference lands on one byte past the verdict's first, +1, +2 or +3, so a census that
  stops reading any of those bytes no longer refuses the break on it ([R412-3] F2, [R413-4] F1) ...
  The first byte is where milan_init()'s one store lands, so a census that stops reading it refuses
  the shipping firmware itself." (was "so it is the break that measures the census's four-byte
  range").
- `docs/integration/BAREMETAL_FIRMWARE.md:1011` "seventeen breaks"; `:1028` one table row for the
  three ("one, two or three bytes ... (three breaks)", escape); `:1035-1045` the paragraph, with the
  narrowings that passed before (round 3: first byte only; round 4: first two, first three) and
  the first byte measured by the shipping firmware (was "It is the one break that measures the
  census's four-byte range").

### Why +2 and +3, not +3 alone

A +3 break alone kills N1, N2, N4 and M9, but not a census that drops only byte +2. This round's
mutant D2 (every byte but +2) is killed only by the +2 break (table below). With the base's store
on byte 0 and one break on each of +1, +2 and +3, a census that drops any one of the four bytes
fails gate 1b, and each drop is caught by the control on that byte.

### The planted controls and their refusal text (at `b3ae1723`)

Each interior break is refused on the escape pin alone, and its premise reads exactly its byte:
"A461 PREMISE +1: nvm_boot() reaches byte(s) [1]", "+2 ... [2]", "+3 ... [3]", then "the linked
image forms the full address of aem_loaded's storage (the full address formed in a register (%lo
on an addi) at 0x00012b88 in nvm_boot() (R_RISCV_LO12_I))" for each of the three. The whole gate 1b
prints "refused 17/17 ... 3 of them reaching it at one byte each, +1, +2, +3". Details and the
other fourteen breaks' refusals are under "The planted controls and their refusal text" below.

## Census mutants and the reviewers' probes, rerun at `b3ae1723`

All runs copy from one byte-exact snapshot of the lane at `b3ae1723`
(`$VALIDATION_STORAGE/a461-70L2r5/clone`, 4.2 GB, not kept), checked with R412-4's
`clone_integrity.py` before any run (`receipts/clone_integrity_start.log`: HEAD, tree, empty status,
976 index entries, every blob's bytes and mode, the three initialised submodules at their
gitlinks). The reviewers' scripts ran unchanged, from copies whose sha256 equal their packets'
`MANIFEST.sha256` (9 of R412-3's, 8 of R412-4's, 16 of R413-4's).

`check_review_runs.py` asserts every row below from the receipts (gate `review-runs`, rc 0: "REVIEW
RUNS AS EXPECTED at b3ae1723...").

### Census mutants (the grader mutants of the verdict's pins)

| Mutant (script, unchanged) | What it narrows | At `5b4a47e9` (reviews' receipts) | At `b3ae1723` | Killed by |
|---|---|---|---|---|
| R413-4 N1 (`r413_census_stop_run.sh`) | census reads bytes +0, +1 only | SURVIVED, "refused=15/15 interior_bytes=[1]" | **KILLED** | "the resolver accepted a neighbour's address folded onto byte +2 of aem_loaded ..." |
| R413-4 N2 | reads +0, +1, +2 | SURVIVED | **KILLED** | "... folded onto byte +3 ..." |
| R413-4 N3 | skips +0 | KILLED | KILLED | the shipping firmware itself ("enters entity_advertise() with [None]") |
| R413-4 N4 | reads +0, +1 (`target not in (low, low+1)`) | SURVIVED | **KILLED** | "... folded onto byte +2 ..." |
| R413-4 `none` | unmutated head | passes, 15/15, `[1]` | passes: "kept=['aem_loaded'] refused=17/17 interior_bytes=[1, 2, 3]" | |
| R412-3 M1 to M8 (`census_mutants_run.sh`, whole gate 1b) | one pin each | KILLED | KILLED | as in round 4: M1, M7 the `&aem_loaded` break without the escape pin; M2 `alias_sscanf` without one name; M3 external linkage without locality; M4 the AUIPC break accepted; M5 the `#ifndef __PIE__` write accepted; M6 `&aem_loaded` without the store pin; M8 the second assignment accepted |
| R412-3 M9 | `target != low` (first byte only) | KILLED (by the +1 break) | KILLED | "... folded onto byte +1 ..." |
| R412-4 K0 to K6 (`run_mutants.py`, stop after gate 1b's closing note) | no pin ever breaks; each pin or half dropped | KILLED | KILLED | K0 the second assignment accepted; K1 the `#ifndef __PIE__` write accepted; K2 and K3 the `&aem_loaded` break without the store and the escape pin; K4 `alias_sscanf` without one name; K5 external linkage without locality; K6 the AUIPC break accepted |
| R412-4 K7, K8 | first byte only; the pins' own range one byte | KILLED | KILLED | "... folded onto byte +1 ..." |
| R412-4 B1, B2 | the +1 break moved to +4 and to +0 | fail the premise | fail the premise | "the interior-byte +1 break's references from nvm_boot() land on byte(s) [] ..." and "... [0] ..." |
| R412-4 N0 | none | passes | passes through gate 1b's closing note, 17/17 at +1, +2, +3 and the class | |
| this round D0 (`drop_byte_mutants.py` via `stop_run.sh`) | drops byte +0 only | | KILLED | the shipping firmware ("enters entity_advertise() with [None]") |
| this round D1 | drops byte +1 only | | KILLED | "... folded onto byte +1 ..." |
| this round D2 | drops byte +2 only | | KILLED | "... folded onto byte +2 ..." (no other control) |
| this round D3 | drops byte +3 only | | KILLED | "... folded onto byte +3 ..." |
| this round Q2 (`premise_mutants_a461.py`) | the +2 break moved to `+ 6`, the neighbour | | refused before grading | "the interior-byte +2 break's references from nvm_boot() land on byte(s) [] of aem_loaded's storage, not on byte +2 alone, so it does not measure that byte: ..." |
| this round Q3 | the +3 break moved to `+ 1` | | refused before grading | "the interior-byte +3 break's references from nvm_boot() land on byte(s) [1] ..." |
| round 4's P1, P2 (70-a460 `premise_mutants.py`, read-only) | the +1 break moved to the neighbour and to byte 0 | refused | refused | "... +1 break's ... byte(s) [] ..." and "... [0] ..." |

### The planted controls and their refusal text (`receipts/own/stop_break_refusals.log`)

`print_break_refusals.py` adds one print after gate 1b records a break as refused, and one after
each premise check; the gate stops after its verdict controls. At `b3ae1723`: "A461 PREMISE +1:
nvm_boot() reaches byte(s) [1]", "+2: ... [2]", "+3: ... [3]"; 17 breaks refused; "R413 verdict
controls: ran=True kept=['aem_loaded'] refused=17/17 interior_bytes=[1, 2, 3]". The three interior
breaks each name the escape pin and no other: "the linked image forms the full address of
aem_loaded's storage (the full address formed in a register (%lo on an addi) at 0x00012b88 in
nvm_boot() (R_RISCV_LO12_I))". The other fourteen name the pins round 4 recorded. R412-4's hook
probes of the same shape (`nbr_fold_byte2`, `nbr_fold_byte3`) show the relocations:
`(2, 'nvm_boot()', 'R_RISCV_HI20'), (2, 'nvm_boot()', 'R_RISCV_LO12_I')` and the same at 3.

### The reviewers' probes

| Probes (script, unchanged) | At `b3ae1723` |
|---|---|
| R412-4 `make_probes.py` (18) and `make_probes_r3shapes.py` (3), through `patch_probe_hook.py` and `run_gate.sh` (`probes/r412_probe_run.sh`) | Outcome and relocation lines identical to R412-4's receipts at `5b4a47e9` (addresses normalised; the probe sets are byte-identical, sha256 `e5ce6fd9...` and `83621e03...`). **Accepted, slot kept:** `csr_pointer_sscanf`, `stack_runtime_sscanf`, `parsed_pointer_sscanf`, `literal_sscanf`, `pre_overrun_sscanf`, `nbr_runtime_sscanf`, `nbr_fold_own`, `own_store_localptr`, `own_store_pre_array_local`, `unplanted`, and both round-3 overrun shapes. Refused on escape: `nbr_fold_byte0` to `3`, `pre_fold_byte2`, `r3_nbr_byte_sscanf`. Refused on the store and escape: `own_store_fold`. Refused by rule 1b: `own_store_runtime`, `own_store_bounded_loop`. |
| R412-4 `whole_gate_plant.py`: `csr_pointer_sscanf`, `stack_runtime_sscanf` planted in the shipping firmware, whole gate function | both "RETURNED (whole gate function accepted the planted firmware)"; each log prints the new class line |
| R412-3 `probe_all.sh`, early (25) | same outcome as its round-3 and round-4 tables: accepted `base`, `nbr_after_sscanf`, `arr_overrun_sscanf`, `nbr_runtime_sscanf`, `pre_overrun_sscanf`; every other probe refused naming the same pins or rule |
| R412-3 `probe_all.sh`, `R412_MODE=full`: `base`, `nbr_runtime_sscanf`, `pre_overrun_sscanf` | each `GATE1B PASS`, rc 0, slot kept, "refused 17/17 ... 3 of them reaching it at one byte each, +1, +2, +3", then the class |
| R413-4 `r413_probe.sh` (9) | same as its round-4 table: accepted `own_local_under_store`, `own_callee_store`, `data_word_nbr_sscanf`; refused on the store and escape `own_folded_store`, `interior_b1_store`; by rule 1b `own_runtime_store`, `data_word_nbr_store`; on escape alone `interior_b2_sscanf`, `interior_b3_sscanf` |
| R413-4 `r413_mutant_probe.sh`: N1 with `interior_b2_sscanf`, `interior_b3_sscanf` | ACCEPTED at the early stop, as at `5b4a47e9`: that stop comes before gate 1b's verdict controls, so it measures the census, not the controls. Under N1 the new +2 break is what now fails gate 1b (N1 row above). |

### How the limit's words match the probes

| Probe | Pointer | Shape in the stated class |
|---|---|---|
| `csr_pointer_sscanf` | `(char *)(uintptr_t)milan_read(MILAN_ID)` handed to `sscanf()` | "a pointer read from a CSR or NVM" |
| `stack_runtime_sscanf` | `loc + (int)milan_read(MILAN_ID)`, `loc` a frame array | "a frame address plus a run-time offset" |
| `parsed_pointer_sscanf` | `strtoul()`'s return cast to a pointer | "returned by a callee" |
| `literal_sscanf` | `(char *)0x40001000u` | "a literal address" |
| `pre_overrun_sscanf`, `nbr_runtime_sscanf` (and the round-3 shapes) | a neighbour's address carried past its end or before its start | "another object's address carried outside that object" |

In each, a called function writes through a pointer with no relocation on the verdict's bytes
(the image's relocations on the verdict are unchanged from `unplanted`), so the pins do not see
it, as every text now states.

## Suite and gate table

Two receipts from `run_gates.py`: `gates-b3ae1723-builder.json` (the two builder banks, one after
the other, run in the lane while the review scripts copied from the snapshot) and
`gates-b3ae1723-rest.json` (the other fourteen, after all review runs). Each records the command,
rc, seconds, log size and sha256, and the head, tree and cleanliness after: `b3ae1723`, tree
`02d9741f`, clean in both. Logs are in `receipts/gates-b3ae1723/`, byte for byte. Every gate ran
at the clean committed tree, from the physical path, never piped.

| Gate | rc | s | Result |
|---|---|---|---|
| builder bank, RV32 compiler required (`--require-elaboration --require-rv32`) | 0 | 1071 | gate 1b "... accepted the AEM-first base only with it kept, and refused 17/17 planted pin breaks on the verdict, each naming its pins, 3 of them reaching it at one byte each, +1, +2, +3 of its storage, so a census that stops reading any of those bytes no longer refuses the break on it; a called function writing through any pointer with no relocation on its storage is outside these pins, whatever the pointer's origin, such as a literal address, another object's address carried outside that object, a CSR or NVM read, a callee's return or a frame address plus a run-time offset". Ends "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11's calibration build tree, as in rounds 1 to 4). Log sha256 `97aced8c...` |
| builder bank, every cross-compiler candidate hidden (`full-builder-absent.py`) | 0 | 668 | "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 1b's compiled census by design, gate 11), "FULL BUILDER ABSENT PASS: all three cross-compiler candidates hidden". Log sha256 `97d983fa...` |
| `review-runs` (`check_review_runs.py`) | 0 | 0.0 | "REVIEW RUNS AS EXPECTED at b3ae1723...": every row of the tables above |
| firmware digest (`check_firmware_digest.py`) | 0 | 0.1 | unchanged since `597dba85`, `943a3dac`, `0a80abcb`, `5b4a47e9`; sha256 = capture receipt |
| `scripts/check_nvm_capture.py` | 0 | 0.7 | "PASS: capture census, clocks, both timing arms and receipt agree" |
| `fw_service_budget/run.py --self-test` | 0 | 0.6 | oracle 52 checks, flash 14, 0 failures |
| grader mutants (`check_grader_mutants.py`, R412-3's scripts unchanged) | 0 | 2.6 | "W0 passes; W1-W6 killed (W3, W4 and W6 by name); X1, X2, X4, X5 killed and X3 passes as a stricter rule" |
| `scripts/check_py_idiom.py` | 0 | 3.5 | every ratchet at or under its bound (long functions 9 <= 9: `rv32_step` 95 lines, `verdict_image_pins` 99) |
| `scripts/measure_test_evidence.py --check` | 0 | 5.6 | "TEST-EVIDENCE RATCHET: PASS" |
| `git diff --check 79c36963 HEAD` | 0 | 0.0 | empty |
| `scripts/docs_check.py` (pinned Markdown environment, as are the next five) | 0 | 4.5 | "0 finding(s) across 177 md files" |
| `scripts/check_doc_paths.py` | 0 | 0.1 | "OK (861 cited paths all resolve)" |
| `scripts/check_doc_style.py` | 0 | 0.0 | "OK (22 current documents)" |
| `scripts/check_archive.py` | 0 | 0.3 | "OK (21 historical page(s))" |
| `scripts/gen_toc.py --check` | 0 | 3.1 | "OK (119 page(s))" |
| `scripts/check_em_dash.py --base 79c36963` | 0 | 3.0 | "0 finding(s) over 568 added line(s) in 24 changed Markdown page(s)" |

The assignment's gates are the two builder banks, the reviewers' `census_mutants_run.sh`,
`r413_census_stop_run.sh` and probe scripts (all through `review-runs`), and the docs gates. The
digest, capture check, service self-test, grader mutants, idiom and evidence ratchets and
`git diff --check` are supporting.

Integrity: R412-4's `clone_integrity.py` passes on the snapshot and on the lane, before the first
run and after the last (`receipts/clone_integrity_{start,end}.log`,
`receipts/lane_integrity_{start,end}.log`).

### A pre-commit check that is not evidence

Before committing item 2 I ran gate 1b on a byte copy of the uncommitted tree: stopped after the
verdict controls ("refused=17/17 interior_bytes=[1, 2, 3]") and whole (`GATE1B PASS` after 15
minutes, printing the new closing line). A shell call that outlived its foreground limit left that
whole run going while I started a second one on the same copy; I stopped the second, and its log
file mixes both, so neither log is kept as evidence. Every result above is from runs at the
committed head `b3ae1723`.

## Firmware digest

`sw/firmware` has no difference from `597dba85`, `943a3dac`, `0a80abcb` or `5b4a47e9`.
`milan_baremetal.c` sha256 `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3` equals
the capture receipt's `product_firmware_sha256`. The round's diff `5b4a47e9..b3ae1723` touches
`CHANGELOG.md`, `docs/integration/BAREMETAL_FIRMWARE.md` and `sw/builder/test_builder.py` only.

## Packet

- `TAKEN.md` (posted, 5911791356), `REVIEW-READY.md` (posted, 5912923414), `PR-BODY.md` (a Round 5 section;
  round 4's and round 3's limit sentences no longer count; not pushed).
- `run_gates.py`, `full-builder-absent.py` and `check_grader_mutants.py` (the previous round's,
  the last two byte-identical), `check_firmware_digest.py` (adds `5b4a47e9`),
  `check_review_runs.py`, `run_detached.sh`, `wait_for.py`, `gates-b3ae1723-builder.json`,
  `gates-b3ae1723-rest.json`.
- `probes/drop_byte_mutants.py` (D0-D3), `probes/premise_mutants_a461.py` (Q2, Q3),
  `probes/stop_run.sh` (the round-4 external review's stop procedure with a mutant script as an
  argument), `probes/r412_probe_run.sh` (the round-4 internal review's probe hook, run unchanged),
  `probes/print_break_refusals.py`.
- `receipts/r412-3/`, `receipts/r412-4/`, `receipts/r413-4/`, `receipts/own/` (every run above, at
  the head), `receipts/gates-b3ae1723/` (every gate log), `receipts/*_integrity_*.log`.
- The scratch area (`$VALIDATION_STORAGE/a461-70L2r5`) held the reviewers' script copies, the
  snapshot and the disposable trees. The trees and the snapshot are deleted after the gates ran,
  so rerunning `check_review_runs.py` needs a fresh snapshot of the lane at `b3ae1723`.
- `MANIFEST.sha256`: the sha256 of every file in the packet but itself.

## Open

- The callee class is recorded on #495 by the manager (5911779020, which supersedes the two
  earlier gate-1b entries).
- Nothing in this round needs a decision. Hosted checks, the act replica and the merge-turn
  candidate build are the manager's.
