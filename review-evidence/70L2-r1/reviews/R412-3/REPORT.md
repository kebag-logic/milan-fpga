[R412] NEGATIVE - exact head 0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4

Round R412-3, cleared-context internal review of PR #623 (#70 lane 2).

- Exact head `0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4`, tree `47a0b44682dee2817b131da935a9e2dffd42bd53`.
- Source base `79c36963660c10e4c1c11a744fb5bff41a552b8b`.
- Two commits this round on my round-2 head `943a3dac`: `a033bfd8` (the grader's W6 control) and `0a80abcb` (gate 1b's linked-image census).
- Processor pin `b2db3a97`, unchanged.

Two findings are open, both MINOR:

- **F1** (Docs, Conformance, Robustness): the verdict's pins do not see a called function that writes the verdict through a pointer formed from another object. The rule comment and the firmware page still say "nothing writes the verdict but that one store", and the stated limit names only a literal address.
- **F2** (Tests): no control measures the census's four-byte address range. A census narrowed to the verdict's first byte passes every control and the whole of gate 1b.

My round-2 F1 (the alias and weakref class) is resolved as ruled. R413-2 F2 and S1 are resolved. Nothing changed in firmware, RTL or bitstream.

## Sources reconstructed, in order

1. `AGENTS.md` and `CONTRIBUTING.md`: sections 2.1 and 3, and the em-dash rule in 6.1.
2. `docs/README.md` (the documentation map). `REQUIREMENTS.md` was consulted only for the release-campaign boundary, which this round does not touch.
3. Issue #70:
   - the body;
   - the lane-2 scope record 5880276193 and assignment 5888775832;
   - round 2, 5904325345, and the record 5904331147;
   - the round-3 assignment 5905511808;
   - the STOP 5906387036 and the ruling 5906400668 (option 1);
   - REVIEW READY 5909022757.
4. Interface authority: `docs/integration/BAREMETAL_FIRMWARE.md`, the verdict-pin section at `:919-1000`, "What the census does NOT observe" at `:808-830`, and the refusal table at `:1605`. Also `tb/verilator/fw_service_budget/README.md` and `docs/findings/397_SERVICE_BUDGET.md`.
5. The history `79c36963..0a80abcb` and the round-3 diff `943a3dac..0a80abcb`: `CHANGELOG.md`, `BAREMETAL_FIRMWARE.md`, `sw/builder/test_builder.py`, `397_SERVICE_BUDGET.md`, and the `fw_service_budget` `README.md` and `run.py`.
6. The PR #623 body at the head.
7. Public evidence `review-evidence/70L2-r1/author-r3` at evidence commit `08c55aa7`: the builder-present and builder-absent logs, `check_nvm_capture`, the firmware digest, `gates-0a80abcb.json` and `probes/image_pin_mutants.py`.
8. After my own pass was complete, my own round-2 report, for the disposition table only. I read no other reviewer's report.

## Method

All work ran in the isolated clone, which was never modified (`receipts/clone_integrity_start.log`, `receipts/clone_integrity_end.log`). Probes ran on disposable copies under the packet's `scratch/`, at most 8 jobs at once.

Scripts in `scripts/`:

- `plants3.py`: plants one probe into the shipping firmware, first statement of `nvm_boot()`. The shipping firmware is AEM-first, so a probe that is accepted keeps the verdict's slot across `nvm_boot()`.
- `early_stop3.py`: stops gate 1b right after the shipping-firmware verdict. It prints the kept set, the verdict's references in the linked image and the objects placed next to it, all read with the gate's own `verdict_image_take()` and `rv32_image_references()`. It also prints the forget-on-call answer.
- `run_gate1b.py`: runs `test_baremetal_profile_contract()` alone with `--require-rv32`. This is my round-2 runner, unchanged.
- `probe_all.sh`: builds each copy and runs it. The early mode uses `git archive` of the head plus each submodule at its gitlink. `R412_MODE=full` makes a byte copy of the clone and runs the whole gate 1b uninstrumented.
- `census_mutants.py` and `census_mutants_run.sh`: nine mutants of the image census, each run through the whole gate 1b.
- `grader_mutants.py` and `grader_mutants2.py`: my round-2 W0-W6 and X1-X5 mutants of the service grader, rerun unchanged.
- `clone_integrity.py`: the end-of-round byte, mode, index and gitlink check.

The RV32 compiler is the pinned SDK, `$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc`, "Buildroot 2026.05 14.3.0". Gate 1b adopts it with driver `()` (`receipts/gate1b_early_base.log`).

## Judgment of the round-3 items

### Item 1 (R412-2 F1, R413-2 F1): the pins decided by address on the linked image

What the census requires, checked against `test_builder.py` at the head:

- **Every reference is an in-place use.** `rv32_image_references()` (`:2115-2160`) takes every relocation of an allocated section whose target lies in `[low, high)`. The target is the symbol value plus the addend. For a `%pcrel_lo`, it is the target of the upper part at its label, and one with no upper part is reported as unplaced.
  - Only three roles count as in place: `HI20` on LUI or `PCREL_HI20` on AUIPC (the upper part); `LO12_I` or `PCREL_LO12_I` on a LOAD or LOAD-FP; and `LO12_S` or `PCREL_LO12_S` on a STORE or STORE-FP.
  - Everything else is reported as an escape: `%lo` on OP-IMM (the whole class, not only `addi`), a GOT entry, a data word, and any other kind or opcode (`:2148-2158`). `verdict_image_pins()` breaks the escape pin on any of them (`:6950-6955`).
- **The one store.** The in-place stores must be exactly `["milan_init()"]`. The resolver, on the position-independent census compile under forget-on-call, must find exactly one store on a symbol the image places on those bytes, or places nowhere: `milan_init()` storing `call:load_aem_image` (`:6936-6949`).
- **One name.** No other defined, non-section, non-file symbol overlaps the four bytes, with a zero size counted as one byte (`:6956-6961`). This covers a GNU alias, a weakref and an absolute `.set` symbol.
- **Locality.** `aem_loaded` is `STB_LOCAL` (`:6962-6963`). The image must define exactly one object of that name (`:6910-6915`).
- **Every AUIPC is relocated.** Every AUIPC word in an executable section must carry a CALL, CALL_PLT, GOT_HI20 or PCREL_HI20 relocation. An image flagged as containing compressed code fails closed (`:2087-2094`, `:6964-6971`).
- **The image compile.** It uses the census compiler, driver and flags (`-std=gnu99 -O0 -fno-inline`, now one tuple at `:4749` shared with the census compile, so the two compiles stay equal) plus `-no-pie`. It is linked alone with `-nostdlib -static -Wl,-q -Wl,--no-relax` and a script that defines no symbol (`:6838-6879`).
- **The early pins.** The source and compile-time pins stay, as early diagnostics that also forget the slot (`:7003-7029`).
- **Kept only when the pins hold.** The slot is kept only when no pin breaks, and only `aem_loaded`'s slot is kept (`:7096`). `_rv32_forget_symbols()` keeps nothing else (`:1817-1828`), so the rule is no weaker for any other static.

Measured at the head:

- **Unplanted head.** The whole gate 1b passes with the slot kept (`receipts/gate1b_full_base.log`, `GATE1B PASS`). It prints: "6 reference(s) to aem_loaded's storage are each the upper part or a load or store in place ... accepted the AEM-first base only with it kept, and refused 14/14 planted pin breaks on the verdict, each naming its pins; a store through a literal address carries no relocation and is outside these pins".
- **Forget-on-call.** The early stop reproduces the six references. The same assembly is refused under forget-on-call (`receipts/gate1b_early_base.log`).
- **The fourteen controls** (`:14616-14691`) are the table at `BAREMETAL_FIRMWARE.md:981-994`, and each lists the pins the doc names. The loop at `:14713-14728` requires `RESOLVER_VERDICT_PIN` and every listed pin in the refusal text.
- **Every probe I have, rerun at this head**, 24 planted probes with this round's scripts (early stop; one receipt each, `receipts/gate1b_early_<probe>.log`):

| Probe inside `nvm_boot()` | At this head | Pins named, or the rule that refused first |
|---|---|---|
| none (shipping firmware) | ACCEPTED, `kept=['aem_loaded']` | 6 references, all in place; refused under forget-on-call |
| `alias_sscanf` (`extern` GNU alias, address to `sscanf()`) | REFUSED | escape (`%lo` on an addi in `nvm_boot()`); one name (`aem_view`) |
| `weakref_sscanf` | REFUSED | escape; one name (`aem_wref`) |
| `static_alias_sscanf` (file-local alias) | REFUSED | escape; one name |
| `alias_decl_only` (the global alias alone) | REFUSED | one name |
| `alias_write`, `static_alias_write` | REFUSED | store (image `nvm_boot()` and `milan_init()`; resolved `nvm_boot()` stores 1); one name |
| `splice_write`, `paste_write`, `m_macro_set` | REFUSED | store |
| `m_macro_addr` | REFUSED | store; address (early) |
| `m_macro_addr_sscanf` | REFUSED | escape; address (early) |
| `plain_write` | REFUSED | source rule "aem_loaded must contain only the image verifier's verdict" |
| `block_extern_sscanf` | REFUSED | source rule "the address of aem_loaded must not be taken" |
| `pie_write` (`#ifndef __PIE__`), `optimize_write` (`#ifdef __OPTIMIZE__`) | REFUSED | graded per arm selection ("`__PIE__` not defined" / "`__OPTIMIZE__` defined"), then the source rule |
| `bcp_write` (write under `__builtin_constant_p` of a local) | REFUSED | source rule |
| `nbr_before_sscanf` (`&r412_pad - 1`, a constant offset) | REFUSED | escape: the compiler folds the offset into the relocation, which then lands on the verdict |
| `nbr_byte_sscanf` (`(char *)&r412_pad - 3`, one byte by `%c`) | REFUSED | escape, on an interior byte of the verdict |
| `nbr_runtime_store` (in-unit store through a run-time offset) | REFUSED | rule 1b, "a STORE this gate cannot PLACE" |
| **`nbr_runtime_sscanf`** (`&r412_pad + k`, `volatile int k = -1`, to `sscanf()`) | **ACCEPTED, slot kept** | F1: in the census image `r412_pad` is `0x158e4` and `aem_loaded` is `0x158e0` |
| **`pre_overrun_sscanf`** (`"%s"` of five characters into `static char r412_line[4]`, declared just before the verdict) | **ACCEPTED, slot kept** | F1: `r412_line` is `0x158c8`-`0x158cb` and `aem_loaded` is `0x158cc`, so the `\001` lands on the verdict's low byte |
| `nbr_after_sscanf`, `arr_overrun_sscanf` | accepted | layout controls: their writes land on `nvm_started` above the verdict, not on it |
| `nbr_memset` | REFUSED | identity-sample register diagnostic, not on the verdict |

- **The two F1 probes through the whole gate.** Both run through the uninstrumented gate 1b to `GATE1B PASS`, rc 0, with the same "kept the slot ... refused 14/14" line (`receipts/gate1b_full_nbr_runtime_sscanf.log`, `receipts/gate1b_full_pre_overrun_sscanf.log`).
- **Census mutants** (my own, independent of the author's seven; `receipts/census_mutant_*.log`). Each drops or narrows one pin, and the whole gate 1b is run on the shipping firmware:
  - M1 (no escape pin), M2 (no name pin), M3 (no locality pin), M4 (no AUIPC pin), M5 (the store pin's image half), M6 (its resolver half), M7 (`%lo` on OP-IMM read as a load) and M8 (no image at all) are each KILLED by a control that names the pin, or by an accepted control.
  - **M9**, which counts only relocations whose target is exactly the verdict's first byte, **SURVIVES**. The gate reports `GATE1B PASS` and "refused 14/14" (F2).
  - Under M9, `nbr_byte_sscanf` is accepted with the slot kept (`receipts/gate1b_early_m9_nbr_byte_sscanf.log`). At the head it is refused on escape.

**The ruling's premise.** The question is whether the `-no-pie` census establishes that nothing else can write the verdict, for every relocated reference the image shows.

- For every relocation that lands on the verdict's four bytes, it does. Each is an upper part, or a load or store used in place. The only in-place store is `milan_init()`'s, holding the verifier's return. No other symbol names the bytes.
- Its by-address reading is stronger than the text suggests. A constant offset from a neighbouring object is folded into the relocation and caught (`nbr_before_sscanf`, `nbr_byte_sscanf`). A run-time offset stored through in the unit is refused as unplaceable (`nbr_runtime_store`).
- It does not establish the premise for a relocated reference to ANOTHER object whose pointer a called function writes through past that object's end. Two cases reach the verdict that way: a run-time index, and a library overrun. Neither puts a relocation on the verdict's bytes, and the whole gate keeps the slot.
- The page already says the resolver does not observe a store made inside a called function (`BAREMETAL_FIRMWARE.md:811-821`). The verdict's section does not carry that limit into its conclusion (F1).
- The literal-address limit is stated as the ruling requires: at the rule (`test_builder.py:1652-1658`, `:6904-6909`), on the page (`:964-969`), in the CHANGELOG (`:65-66`) and in the gate's printed line (`:17136-17151`).

### Item 2 (R413-2 F2 and S1): W6, commit `a033bfd8`

- The fifth armed control (`run.py:534-547`) is a `milan_status` command that starts before arming, with a 10 ms TX allowance. It passes at an armed bound of exactly 500 ms and is charged one cycle later.
- The self-test passes: "checks: 52 failures: 0" (`receipts/fw_service_budget_selftest.log`).
- My W6 ("the armed bound forgets the UART allowance") is now KILLED by name, "an unarmed-start command's UART allowance left its armed bound".
- W0 passes and W1-W5 stay killed (`receipts/grader_mutants.log`).
- X1, X2, X4 and X5 are killed. X3 passes; it only arms earlier and so charges more (`receipts/grader_mutants2.log`).
- The README (`fw_service_budget/README.md:150-160`) and `397_SERVICE_BUDGET.md:318` ("52 grading controls") match the code.
- The PR body's W6 sentence now reads "more lenient than the rule, not stricter: no control separated it", which is correct.

### No firmware, RTL or bitstream change

- The round-3 diff touches only the builder, the grader and documentation.
- `sw/firmware` is identical to `597dba85` and `943a3dac`.
- `milan_baremetal.c` has sha256 `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`, which equals the capture receipt's `product_firmware_sha256` (`receipts/firmware_digest.log`).
- `check_nvm_capture.py`: all seven controls detected, PASS, rc 0 (`receipts/check_nvm_capture.log`).
- `hdl/`, `syn/`, `sw/litex`, `.github` and every gitlink are unchanged since `597dba85` (`receipts/scope_diff.log`).

## Findings

### F1 - MINOR - Docs, Conformance, Robustness - a called function writing through another object's pointer reaches the verdict, and the verdict section still claims nothing else writes it

**Where:**

- `docs/integration/BAREMETAL_FIRMWARE.md:935-939` ("So no relocated reference forms the full address in a register ... where a call argument ... could carry it") and `:964-975` ("So, within that model and that limit, nothing writes the verdict but that one store");
- the refusal row at `:1605` ("with its full address never formed");
- the rule comment at `sw/builder/test_builder.py:1631-1658` ("So within that model nothing writes it but that one store") and the `verdict_image_pins()` docstring at `:6893-6909`.

**Authority:**

- Round-3 assignment 5905511808, item 1: the rule comment and the page "state only what the census proves".
- Ruling 5906400668: the literal-address limit is the one limit accepted as stated.
- Assignment rule 1 defines a reference as "any instruction or data word that materializes that address, by relocation or by PC-relative or absolute address computation, under any symbol name".

**Evidence:**

- `pre_overrun_sscanf` plants `static char r412_line[4];` just before `static int aem_loaded;`, and `(void)sscanf("abcd\001", "%s", r412_line);` in `nvm_boot()`.
  - In the gate's own linked image, `r412_line` occupies `0x158c8`-`0x158cb` and the verdict `0x158cc`.
  - The library's sixth byte, `\001`, lands on the verdict's low byte, making a zero verdict non-zero.
- `nbr_runtime_sscanf` hands `sscanf()` `&r412_pad + k`, with `volatile int k = -1`. `r412_pad` is at `0x158e4` and the verdict at `0x158e0`.
- In both, the only relocations near the verdict land on the neighbour, not on the verdict's bytes (`R412 nvm_boot() relocations ...` lines in the early receipts).
- The whole gate 1b passes each, with the slot kept (`receipts/gate1b_full_{nbr_runtime,pre_overrun}_sscanf.log`).
- The class is narrow, and the gate closes its neighbours: a constant offset is folded and refused by address, and the same run-time offset stored through in the unit is refused as unplaceable (table above). What remains is a called function writing through a pointer to another object past its end.
- The standing model states exactly this for the census as a whole (`BAREMETAL_FIRMWARE.md:811-821`: "a C-library or libatomic call that writes through a pointer this unit forms is not observed"). The verdict section cites "the resolver's standing model", but quotes only its placed-store clause, and concludes that nothing but `milan_init()`'s store writes the verdict.

**Impact:**

- A firmware whose `nvm_boot()` overruns a neighbouring static, a plain buffer overrun, can turn a failed AEM verdict into a non-zero one across the AEM-first call. `entity_advertise()` then enables the entity, and gate 1b certifies that firmware with the slot kept.
- The shipping firmware is not affected. The defect is that the section claims more than the census proves, and that the ruling's accepted limit does not cover this class.

**Required outcome:**

- The rule comment, the verdict section of `BAREMETAL_FIRMWARE.md` (including the refusal row at `:1605`) and the PR body state this limit beside the literal one: an address formed from another object's relocated reference and carried past that object's end by a called function reaches the verdict with no relocation on its bytes, and is outside the pins. That is the standing callee limit of `:811-821` applied to the verdict.
- The manager rules on accepting it as a stated limit (with #495) or on closing it.
- Alternatively the gate closes it, for example by keeping the slot only when no call in the unit is handed a pointer to a static whose run-time extent the resolver cannot bound. If closed, both probes above must be refused naming the pin.

**Verification:** re-read the three texts at the fix head. `scripts/plants3.py` `nbr_runtime_sscanf` and `pre_overrun_sscanf` through `scripts/probe_all.sh` must either be refused naming a pin, if closed, or accepted and matching the stated limit's words, if accepted.

### F2 - MINOR - Tests - no control measures the four-byte range, so a census narrowed to the verdict's first byte passes gate 1b

**Where:** the controls at `sw/builder/test_builder.py:14616-14691`, and the range test at `:2131`.

**Authority:**

- `AGENTS.md` section 6, `Tests`: "Each new test can fail for the defect it claims to detect".
- `BAREMETAL_FIRMWARE.md:935`: "every relocation that lands on the four bytes of `aem_loaded`, under any symbol".

**Evidence:**

- Census mutant M9 replaces `not low <= target < high` with `target != low`, so only relocations at the first byte are references.
- The whole gate 1b still passes on the shipping firmware, and its fourteen controls are all refused, each naming its pins (`receipts/census_mutant_M9_by_name_only.log`: `GATE1B PASS`, "refused 14/14").
- Under M9, `nbr_byte_sscanf`, whose folded relocation lands on the verdict's second byte and whose `sscanf("%c")` writes it, is accepted with the slot kept (`receipts/gate1b_early_m9_nbr_byte_sscanf.log`). At the head it is refused on escape (`receipts/gate1b_early_nbr_byte_sscanf.log`).
- Every control's reference to the verdict lands on its first byte, so the range, the one part of "by address" that no name can stand for, is unmeasured.

**Impact:** a future edit narrowing the range to the symbol's value would drop interior-byte references and stay green on every control.

**Required outcome:** a planted control whose only reference to the verdict lands inside its bytes but not on its first byte is refused, naming the escape pin, so that M9 is killed. `nbr_byte_sscanf`'s shape is one such control.

**Verification:** `scripts/census_mutants.py` M9 through `scripts/census_mutants_run.sh` fails gate 1b on that control. M1-M8 stay killed, and the unplanted head passes with the slot kept.

### Considered and not raised

- **Code-model and optimisation differences.** A write selected by `#ifndef __PIE__` or `#ifdef __OPTIMIZE__` is graded per arm selection and refused. A write under `__builtin_constant_p` is refused by the source rule.
- **Inline asm spellings** (`.set`, labels, `la`, offset addends) are refused by the boot-unit asm allowlist (`test_builder.py:5477-5518`) before any pin. The image pins remain as the by-address backstop.
- **The literal-address limit** is stated as ruled. Recording it on #495 is the manager's.

## Disposition of prior public review findings at this head

This disposition covers my own round-2 findings and the round-2 items as the round-3 assignment states them. I read no other reviewer's report.

| Finding | Disposition | Evidence |
|---|---|---|
| R412-2 F1 (MAJOR): an alias or weakref of `aem_loaded` hands its address to `sscanf()` and the slot is kept | RESOLVED as ruled. Every alias, weakref and address spelling I have is refused naming one name and/or escape, the whole gate carries `alias_sscanf` and `weakref_sscanf` as controls, and the head passes with the slot kept. The callee-overrun class is a new, narrower finding (R412-3 F1), not this one retained: it needs no name for the verdict, and its remedy is a stated limit like the ruled literal one | table above; `receipts/gate1b_full_base.log`; `receipts/census_mutant_M2_no_name.log` |
| R413-2 F1 (MAJOR, the same defect) | RESOLVED as above, by the round-3 assignment's description of it (`alias_sscanf`, `weakref_sscanf`) | same |
| R413-2 F2 (MINOR): the PR body called W6 stricter | RESOLVED: the PR body now says W6 is more lenient and that no round-2 control separated it | PR body, round 2 item 2 |
| R413-2 S1 (SUGGESTION): a control that kills W6 | TAKEN: W6 is killed by name | `receipts/grader_mutants.log` |
| Rounds 1 and 2, all other findings | Stay resolved: no artifact in their scope changed this round except as listed | `receipts/scope_diff.log` |

## Per-lens results at this head

[R412] UNCLEAN Conformance - F1. Artifacts: the round-3 assignment items 1-2 and ruling 5906400668 against `test_builder.py:2115-2160,6838-7029,14616-14728,17136-17151`; `run.py:493-547`; the PR body; the #70 record 5904331147. Every ruled requirement is implemented and measured. The texts' claim that nothing else writes the verdict is not proven.

[R412] PASS RTL - `receipts/scope_diff.log` - `git diff 597dba85..0a80abcb -- hdl protocol-processor gptp-processor third_party external sw/firmware sw/litex syn .github` is empty, and the gitlinks are unchanged. RTL was covered clean by R412-1 at `597dba85`, an ancestor of this head, and nothing in RTL scope has changed since. The round-3 builder hunks (`rv32_step`, the image reader, the census flag tuple, `aem_verdict_pins`, the controls and the summary) touch none of gate 1b's RTL-reading rules: no `adp_ctrl`, `pp_ctrl_r`, enable-assign or datapath line changed. No Verilator harness ran (see limits).

[R412] UNCLEAN Robustness - F1. Artifacts: 24 planted probes through gate 1b (the table above), of which two escape class probes were also run through the whole gate. Also: the grader's boundary controls with W0-W6 and X1-X5, and the firmware's boot paths, byte-identical since `597dba85`.

[R412] UNCLEAN Tests - F2. Artifacts: the whole gate 1b at the head (14/14 controls, slot kept, PASS), and nine census mutants (eight killed, M9 survives). Also the grader self-test (52 checks, 0 failures), with W6 killed by its new control, and `check_nvm_capture`'s seven controls.

[R412] UNCLEAN Docs - F1. Artifacts: `BAREMETAL_FIRMWARE.md:808-830,919-1000,1605`; the comments at `test_builder.py:1631-1658,1964-2016,6765-6783,6834-6909,6974-7002,14565-14591`; `CHANGELOG.md:65-66`; `fw_service_budget/README.md:150-160`; `397_SERVICE_BUDGET.md:318`; the PR body. Supporting checks: `docs_check.py`, `check_doc_style.py` and `check_doc_paths.py` rc 0; 0 em dashes on lines added this round; `git diff --check` clean (`receipts/docs_gates_local.log`, `receipts/docs_local_checks.log`). The fourteen-row table matches the controls, and the W6 text matches the code.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-3 assignment 5905511808, STOP 5906387036, ruling 5906400668; `test_builder.py:2115-2160,6838-7029,14616-14728,17136-17151`; `run.py:493-547`; PR body; #70 record 5904331147 | R412-3 | 0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4 |
| RTL | CLEAN | Empty RTL, firmware, submodule, `syn` and CI diff `597dba85..0a80abcb` (`receipts/scope_diff.log`); gitlinks `protocol-processor b2db3a97`, `gptp-processor 5dce647a`, `third_party/verilog-axis 48ff7a7e`; RTL covered clean by R412-1 at ancestor `597dba85` | R412-3 (scope unchanged since R412-1) | 0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4 |
| Robustness | UNCLEAN (F1) | 24 gate-1b probes (early stop) and 2 whole-gate probe runs; grader boundary controls and mutants; firmware digest | R412-3 | 0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4 |
| Tests | UNCLEAN (F2) | Whole gate 1b at the head; 9 census mutants (M9 survives); grader self-test and W0-W6, X1-X5; `check_nvm_capture` | R412-3 | 0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4 |
| Docs | UNCLEAN (F1) | `BAREMETAL_FIRMWARE.md:808-830,919-1000,1605`; rule comments and docstrings in `test_builder.py`; `CHANGELOG.md:65-66`; grader README; `397_SERVICE_BUDGET.md:318`; PR body; local docs gates | R412-3 | 0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4 |

## Real limits of this round

- **No Verilator harness ran.** The scoped simulator path `$VALIDATION_STORAGE/tmp/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host, and I did not substitute another build. RTL coverage rests on the empty RTL-scope diff since `597dba85` and on R412-1's coverage there.
- **Some Markdown gates did not run.** The pinned renderer (`cmarkgfm`/`html5lib`) is not installed, and I made no install, so `check_em_dash.py --base`, `gen_toc.py` and the other renderer-backed gates did not run. I ran `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py` and a direct scan of the added lines. The manager's pinned gates at this head are public evidence.
- **Gate 1b only, compiler present.** I ran gate 1b alone, not the builder bank, and only with the RV32 compiler present. The compiler-hidden arm rests on the public `builder-absent.log` ("EXCEPT 2 NOT RUN", "FULL BUILDER ABSENT PASS").
- **The layout is the census image's own.** The F1 probes land on the verdict in the census's linked image, which is one unit linked alone. The product's layout under its own flags is not linked here, as the ruling states for the literal limit. I did not verify the product `bios.elf` reference count cited in the STOP.
- **Three runs overran one call.** Three complete-gate runs and one mutant batch outlasted a single foreground call. They were polled to completion, and every run finished before this report.
- **Not run here:** the native service groups, the capture harness, Yosys, timing, and hosted or local CI replication. No firmware, RTL or bitstream byte changed, so round 1's capture receipt, native evidence and sweep stand on their public receipts.
- **No hardware.** Physical calibration was NOT RUN, no hardware was used, and field skips are not hardware proof.
- **The clone was never modified.** At the end:
  - HEAD, the index tree, and every tracked file's blob and mode equal the head;
  - no assume-unchanged or skip-worktree entries;
  - the gitlinks are checked out clean, and `external` is uninitialised as at the start (`receipts/clone_integrity_end.log`).

  The docs scripts and gate imports had left 11 ignored `__pycache__/*.pyc` files in the clone, none of them tracked. They were removed before that check.

## Pending manager duties

- Rule on F1: accept the callee-overrun class as a stated limit (text only, with #495) or require it closed. Rule on F2: a control that kills M9, which is builder tooling only.
- After the fix, re-review covers at least Conformance, Robustness, Tests and Docs at the fix head.
- Record the literal-address limit, and F1's class if accepted, on #495.
- At the merge turn, build and validate the current-dev candidate (source base `79c36963`, live dev `ccdd07b5`). Own hosted and local CI acceptance at the exact head, distinguishing executed jobs from skipped contexts.
- Confirm at the final head that the capture receipt, native evidence and sweep still stand. The firmware digest is unchanged at this head.
- A second positive review, and a reviewer-owned ledger, at the final head.

R412-3 FINISHED
