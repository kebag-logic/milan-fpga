[A461] REVIEW READY
Commit: `b3ae17233eb9dd5934255f4018da7d45a159b5ac` (branch `70-lane2-pin-d352`, local only, tree `02d9741f`; 30 commits on dev `79c36963`, two this round on `5b4a47e9`: `ae203a01` and `b3ae1723`; processor pin `b2db3a97`, unchanged).

Changed, under the [round-5 assignment](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5911775903):
1. **R412-4 F1, `ae203a01`: the limit is one callee class, with no count.** The six places R412-4 lists now say this: a reference is found by its relocation, so a called function that writes through any pointer carrying no relocation on `aem_loaded`'s bytes is not seen by the pins, whatever the pointer's origin. That is the census's standing callee limit (`BAREMETAL_FIRMWARE.md`, the first entry under "What the census does NOT observe") applied to the verdict. The six places are the rule comment (`sw/builder/test_builder.py:1647-1674`), `docs/integration/BAREMETAL_FIRMWARE.md:966-1007` (now headed "What the pins do not see") with its refusal row (`:1651`), the printed closing line (`test_builder.py:17233-17237`) and the PR body. The shapes are named as examples, not a closed list:
   - a literal address;
   - another object's address carried outside that object;
   - a pointer of run-time origin: a CSR or NVM read, a callee's return, or a frame address plus a run-time offset.

   Closing the class needs call-argument provenance or a memory-safety check on every call inside `nvm_boot()` (#495, 5911779020). No text counts limits or says what holds "outside" them. The `verdict_image_pins()` docstring and the CHANGELOG, which carried the same two-shape wording, are aligned too.
2. **R413-4 F1, `b3ae1723`: breaks on bytes +2 and +3.** Gate 1b's interior-byte break is now three, one `int` back from a static just after the verdict plus 1, 2 and 3 bytes (`test_builder.py:14648-14662`). Each is refused on the escape pin alone. The premise check is per break and exact: `nvm_boot()`'s relocation targets on the verdict must be `[k]` and nothing else. Round 4 asked only for "past the first byte". There are now seventeen breaks. The closing line reads "3 of them reaching it at one byte each, +1, +2, +3 of its storage, so a census that stops reading any of those bytes no longer refuses the break on it". The "four-byte range" texts (the comment over the controls, the closing line and `BAREMETAL_FIRMWARE.md:1035-1045`) now say what the breaks measure. The page adds that the first byte is where `milan_init()`'s one store lands, so a census that stops reading it refuses the shipping firmware. Both +2 and +3 are needed: a +3 break alone misses a census that drops only byte +2 (mutant D2 below).

No firmware, RTL, bitstream, CI or processor change. The round's diff touches `CHANGELOG.md`, `BAREMETAL_FIRMWARE.md` and `test_builder.py` only.

Validation at `b3ae1723`, clean tree, physical path, never piped, every gate rc 0:
- Builder bank with the RV32 compiler required (`--require-elaboration --require-rv32`, 1,071 s). Gate 1b "refused 17/17 planted pin breaks on the verdict, each naming its pins, 3 of them reaching it at one byte each, +1, +2, +3", then states the class. It ends "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11's calibration tree, as before).
- The same bank with every cross-compiler candidate hidden (668 s): "EXCEPT 2 NOT RUN", then "FULL BUILDER ABSENT PASS".
- R413-4's `r413_census_stop_run.sh`: N1 and N4 are killed by the +2 break and N2 by the +3 break, each by name. N3 is killed by the shipping firmware. The unmutated head reads "kept=['aem_loaded'] refused=17/17 interior_bytes=[1, 2, 3]". Its nine plants give its round-4 outcomes.
- R412-3's `census_mutants_run.sh`: M1 to M9 are all killed, M9 by the +1 break. Its `probe_all.sh` gives the round-4 outcomes for all 25 early probes. The head, `nbr_runtime_sscanf` and `pre_overrun_sscanf` each give `GATE1B PASS` through the whole gate 1b with 17/17.
- R412-4's probes through `patch_probe_hook.py`: 21 probes, with outcome and relocation lines identical to its receipts. Through `whole_gate_plant.py`, `csr_pointer_sscanf` and `stack_runtime_sscanf` return from the whole gate function, and the gate prints the class. Its K0 to K8 are killed. B1 and B2 fail the +1 premise, and N0 passes.
- This round's own mutants. D0 to D3 each drop one byte from the census: D0 is killed by the shipping firmware, and D1, D2 and D3 each by the break on that byte. Premise mutants Q2 (the +2 break moved onto the neighbour, "byte(s) []") and Q3 (the +3 break moved onto +1, "byte(s) [1]") are refused before grading.
- The docs gates (the six Markdown gates in the pinned environment), and the firmware digest: `sw/firmware` is unchanged since `597dba85`, `943a3dac`, `0a80abcb` and `5b4a47e9`, and `a73ecc25...0eb3` equals the capture receipt's.
- Supporting: `check_nvm_capture`, the `fw_service_budget` self-test (52 checks), R412-3's grader mutants, the Python idiom ratchets (`rv32_step` 95 lines, `verdict_image_pins` 99), the evidence classifier and `git diff --check`.

Acceptance criteria, met:
- Item 1: no text says "two" limits or "outside the two limits". `csr_pointer_sscanf` (a CSR read) and `stack_runtime_sscanf` (a frame address plus a CSR-read offset) stay accepted with the slot kept, and each matches the third shape's words. R412-4's `parsed_pointer_sscanf` and `literal_sscanf` match the callee's-return and literal shapes.
- Item 2: the +2 and +3 breaks are refused on the escape pin with their premises checked. N1, N2, N4 and M9 are killed. M1 to M8 stay killed, and the head passes with the slot kept.

Open risks/questions: none.
