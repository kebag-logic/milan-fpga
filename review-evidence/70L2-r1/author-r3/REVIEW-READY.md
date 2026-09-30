[A457] REVIEW READY
Commit: `0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4` (branch `70-lane2-pin-d352`, local only, tree `47a0b446`; 26 commits on dev `79c36963`, two this round on `943a3dac`: `a033bfd8` and `0a80abcb`; processor pin `b2db3a97`, unchanged).

Changed, under the [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5905511808) and the [ruling on the STOP](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5906400668) (option 1):
1. **F1 (R412-2, R413-2), `0a80abcb`.** Gate 1b decides `aem_loaded`'s pins by address, on the linked image of a second compile of the same source. That compile uses the census's flags and stubs plus the product's `-no-pie`, and the pinned SDK links it alone. `sw/builder/test_builder.py` reads that image's symbols and relocations; no disassembler runs. On the image:
   - every relocation that lands on the verdict's four bytes, under any symbol, is the upper part or a load or store in place;
   - the one store in place is `milan_init()`'s, and the resolver, still reading the position-independent census compile, finds its value to be `load_aem_image()`'s return;
   - no other symbol covers the bytes, `aem_loaded` is local, and every AUIPC carries a relocation.

   The source and compile-time pins stay as early diagnostics. The literal-address limit is stated at the rule, in `docs/integration/BAREMETAL_FIRMWARE.md` and in the CHANGELOG, as the ruling accepts. The page's pin section and refusal row state only what the image census proves.
2. **F2 and S1 (R413-2), `a033bfd8`.** A fifth armed control kills W6 by name. The PR body's W6 sentence is corrected: W6 is more lenient, and no round-2 control separated it.

No firmware, RTL, bitstream, CI or processor change. `sw/firmware` is byte-identical to `597dba85` and `943a3dac`.

Validation at `0a80abcb`, clean tree, physical path, never piped, every gate rc 0:
- Builder bank with the RV32 compiler required (`--require-elaboration --require-rv32`, 1,019 s). Gate 1b keeps the slot for the shipping firmware. Its image holds 6 references to the verdict, each an upper part or an in-place load or store, and the gate "refused 14/14 planted pin breaks on the verdict, each naming its pins". The run ends "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11's calibration tree, as before).
- The same bank with every cross-compiler candidate hidden (645 s): "EXCEPT 2 NOT RUN" (gate 1b's compiled census by design, and gate 11), then "FULL BUILDER ABSENT PASS".
- `fw_service_budget` self-test: 52 grading checks and 14 flash checks. Grader mutants: W0 passes and W1 to W6 are killed (W3, W4 and W6 by name). X1, X2, X4 and X5 are killed, and X3 passes as a stricter rule. R413-2's six rules are killed.
- `check_nvm_capture`, all seven controls detected. The firmware digest `a73ecc25...0eb3` equals the capture receipt's.
- Python idiom ratchets, the evidence classifier, `git diff --check`, and the six Markdown gates in the pinned environment.

Acceptance criteria, met:
- `alias_sscanf` and `weakref_sscanf` were accepted at `943a3dac` and `a033bfd8`, by the reviewers' own scripts. Now both are refused, naming one name and escape: "another symbol of the linked image is on aem_loaded's storage", and "the full address formed in a register (%lo on an addi) ... in nvm_boot()".
- The nine earlier gate controls stay refused, each naming its pins. Three new ones are refused too: a write under `#ifndef __PIE__` (store), the address in a data word (escape), and an AUIPC with no relocation (AUIPC).
- All 12 R413-2 plants and all 11 R412-2 plants are refused, rerun with the reviewers' own scripts. The unplanted head is accepted with `kept=['aem_loaded']` and refused under forced forget-on-call.
- Seven mutants of the image census are each killed by a control: the census breaking nothing, and each pin dropped, with the store pin's two halves dropped separately.

Open risks/questions: the literal-address limit, accepted by the ruling and stated. A store through a hard-coded product address carries no relocation and is outside these pins; #495 carries it. The packet also records a host power-off during the first gate run at this head. The whole gate bank was rerun from the start at the same head and clean tree.
