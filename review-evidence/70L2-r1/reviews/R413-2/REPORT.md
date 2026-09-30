[R413] NEGATIVE - exact head 943a3dac973abc7130fe1a19bb6f5943788a01fe

Round R413-2 is the external independent review of kebag-logic/milan-fpga PR #623 (issue #70, lane 2).

- Head `943a3dac973abc7130fe1a19bb6f5943788a01fe`, tree `ffb89f749a18aeb6ec7d843f320fb6b095b08e10`.
- The head is three commits on my round-1 head `597dba85`: `bab4f32d`, `666f0623` and `943a3dac`.
- All five lenses were applied.
- One MAJOR finding and one MINOR finding are open, so the verdict is NEGATIVE. RTL is the only lens clean at this head:
  - F1 is my round-1 F1, narrowed but not closed. The four spellings the assignment named are now refused. Two other spellings of the verdict's address still reach compiled code, and the gate still keeps the slot for them.
  - F2 is new: a factual error in the PR body.
- Resolved at this head: R412-1 F2 (the armed grader control), R413-1 F2 (the remaining-work list) and the S1 line on the service page.

## Reconstruction (public state only)

- **Contract:** AGENTS.md, CONTRIBUTING.md and docs/README.md.
- **Issue #70:** the round-2 assignment 5904325345, whose rulings accept `18199bac` and record section 5.3 change 3 as open, not implemented here. Also the #70 record 5904331147 and the review start 5905074062.
- **Authority for F1:** the ruling 5894183475. The slot survives a call only while its pins hold, on the premise that nothing else can write it. Assignment item 1 adds: "No address of `aem_loaded` is taken in the compiled code".
- **Code and evidence:**
  - the diff `79c36963..943a3dac`, focusing on `597dba85..943a3dac` (5 files; `receipts/round2_scope.txt`);
  - the PR body at the head;
  - the public evidence `f94a0f11:review-evidence/70L2-r1/author-r2`, including `gates-943a3dac.json`: 15 gates at rc 0, head and head_after equal to `943a3dac`, clean tree.
- **Order of reading:** my own round-1 report was read first. The other reviewer's round-1 findings were read only after this verdict and ledger were written (see the section on prior findings). Before that, I used only the other reviewer's public `grader_mutants.py`, which the assignment asks me to rerun.

## Findings

### F1 - MAJOR - lenses: Tests, Conformance, Docs, Robustness (R413-1 F1 and R412-1 F1 retained, narrowed)

**Where:**
- `sw/builder/test_builder.py:6579-6608` (`verdict_register_diagnostic`, which asks `-fsyntax-only`);
- `:6610-6671` (`aem_verdict_pins`), with the rule comment at `:1634-1647`;
- `:14246-14290` (the planted controls);
- `docs/integration/BAREMETAL_FIRMWARE.md:924-952` and `:1558`.

**Authority:**
- The ruling 5894183475 lets the slot survive a call only while "nothing else can write it".
- Assignment 5904325345 item 1 requires "No address of `aem_loaded` is taken in the compiled code".
- The docs state that the address pin is what refuses a write made by a library through the verdict's address. `BAREMETAL_FIRMWARE.md:950-952` says "only the address pin refuses it".

**The problem.** The address pin asks the compiler whether the preprocessed unit still parses with `aem_loaded` redeclared as a global register variable, and it asks only with `-fsyntax-only`. That catches every C-level `&aem_loaded`, however it is spelled.

It does not catch a second symbol bound to the static. GCC resolves `alias` and `weakref` targets after parsing, so a syntax-only compile never sees that the target became a register variable (`receipts/alias_register_check.txt`):
- with `-fsyntax-only`, rc 0;
- with a full `-S` compile, rc 1: "'milan_r413_alias' aliased to undefined symbol 'aem_loaded'".

**Evidence.** Each plant is placed at the end of `nvm_boot()` in a scratch copy. Probes are in `probes/` and receipts in `receipts/`.

| Plant (inside `nvm_boot()`) | Head gate | Slot | Refused on |
|---|---|---|---|
| `plain_write`, `aem_loaded = 1;` | refused | forgotten | source rule and the write pin |
| `splice_write` (phase-2 splice) | refused | forgotten | write pin, "nvm_boot() stores 1" |
| `paste_write` (`##`) | refused | forgotten | write pin |
| `m_macro_set`, `((flag) = 1)` | refused | forgotten | write pin |
| `m_macro_addr`, pointer through a macro, then a store | refused | forgotten | write pin |
| `m_macro_addr_sscanf`, address through a macro to `sscanf()` | refused | forgotten | address pin, "address of global register variable 'aem_loaded' requested" |
| `alias_write`, a GNU alias written directly | refused | forgotten | rule 1b, an unplaceable store |
| `asm_label_sscanf`, `extern int x __asm__("aem_loaded")` | refused | forgotten | boot-unit asm allowlist |
| `inline_asm_la`, `la %0, aem_loaded` | refused | forgotten | boot-unit asm allowlist |
| `block_extern_sscanf`, a block-scope `extern int aem_loaded;` | refused | forgotten | source address rule |
| **`alias_sscanf`**: `extern int milan_r413_alias __attribute__((alias("aem_loaded")));` and `sscanf("1", "%d", &milan_r413_alias);` | **ACCEPTED** | **kept** | none |
| **`weakref_sscanf`**: `static int milan_r413_ref __attribute__((weakref("aem_loaded")));` and `sscanf("1", "%d", &milan_r413_ref);` | **ACCEPTED** | **kept** | none |

These results are in `receipts/gate1b_head_<plant>.log`.

**What the two accepted plants compile to.** The standalone demos `probes/alias_escape_demo.c` and `weakref_escape_demo.c` were built with the pinned RV32 compiler (`receipts/alias_escape_compile.txt`, `weakref_escape_compile.txt`):
- `nvm_boot()` passes `lla a2,milan_r413_alias`, and the unit binds that name to the static with `.set milan_r413_alias,aem_loaded`. For the weakref it is `.set milan_r413_ref,aem_loaded`.
- At -O0 and at -Os, `milan_init()` reloads `aem_loaded` from memory after `nvm_boot()` returns.
- A host build at -O0, -O2 and -Os prints `entity_advertise(verified=1): ENABLE WRITTEN` when `load_aem_image()` returned 0.

**Impact.**
- For these two spellings the resolver keeps a verdict slot that library code has overwritten through the verdict's address. So the gate accepts a firmware that enables the entity after an AEM CRC failure, which is the bypass gate 1b exists to refuse.
- The shipping firmware is unaffected. This is a gap in the instrument that proves it, and the ruling's premise does not hold at this head.
- These statements are false for the alias and weakref spellings:
  - "the compiler accepts the unit with it declared a register variable ... so no expression hands a pointer to it to any code" (`test_builder.py:1637-1639`, `BAREMETAL_FIRMWARE.md:929-932`);
  - "defined with internal linkage, so no other unit can name it" (`:1640-1641`, `:933-936`). The `alias` form also emits `.globl milan_r413_alias`, which exports the static under a second global name that pin 3 never reads (it looks for `aem_loaded` only);
  - "with its address never taken, however either is spelled" (`BAREMETAL_FIRMWARE.md:1558`).

**What is resolved.** The four spellings that assignment item 1 names are refused on the head gate:
- my `splice_write`, `paste_write`, `m_macro_set` and `m_macro_addr` probes (the last as both the pointer-store and `sscanf` forms);
- the four new in-gate controls, each naming its pin (`receipts/gate1b_head_verdict_controls.log`).

The round-1 gate from `597dba85` accepts all four with the slot kept (`receipts/gate1b_r1gate_*.log`), so the new controls can fail.

The five older controls stay refused, each by name:
- write pin: `nvm_boot() stores 0` and `milan_status_handler() stores 1`;
- address pin;
- static pin;
- second-unit pin (`milan_verdict.c`).

The shipping head passes with the slot kept, both at the early stop (`receipts/gate1b_head_none.log`, `kept= ['aem_loaded']`) and in the whole `test_baremetal_profile_contract()`:
- 879 s, rc 0;
- "refused 9/9 planted pin breaks on the verdict, each naming its pin" (`receipts/gate1b_head_full.log`).

Under forget-on-call the shipping head is refused (`receipts/gate1b_head_none_forget.log`).

The rule is no weaker for any other static:
- `kept` is `{"aem_loaded"}` or empty (`:6737`);
- the pins are read on the forget-on-call unit (`:6731`), so they do not depend on the slot they decide;
- `_rv32_forget_symbols` is unchanged.

**Required outcome:**
- The address pin, and the single-unit pin, must hold for every symbol the compiled unit binds to `aem_loaded`, not only for C expressions that name it. Two acceptable forms:
  - a compile step that resolves aliases;
  - a census of the assembly's `.set`, `.weakref`, `.equ` and `.globl` bindings whose target is the verdict.
- Planted controls must refuse an `alias(...)` and a `weakref(...)` of the verdict whose address is handed to `sscanf()` inside `nvm_boot()`, each naming the broken pin. They must be accepted by this head's gate, so they can fail.
- The rule comment and `BAREMETAL_FIRMWARE.md:924-952,1558` state only what is proven.

**Verification:**
- Rerun `probes/plants.py` with `alias_sscanf` and `weakref_sscanf` through `probes/run_gate1b.py`: both must be refused, naming a pin.
- Every other row of the table must stay as recorded.
- The shipping head must still pass with the slot kept.

### F2 - MINOR - lens: Docs

**Where:** the PR #623 body, round-2 item 2: "W6, the armed bound without the UART allowance, passes because it is stricter."

**Evidence.**
- W6 (the other reviewer's public mutant) survives the head self-test (`receipts/grader_mutants_w0_w6.log`).
- W6 is **more lenient**, not stricter. It drops `uart_tx_allowance_ms` from `armed_period_bound_ms`, which lowers the bound compared against 500 ms and 250 ms.
- On one synthetic duty that starts before arming, with a 10 ms allowance and a 245 ms armed lead (`probes/w6_direction.py`, `receipts/w6_direction.log`):
  - the head rule gives a bound of 505 ms and raises both the tick and the PHY stretch findings;
  - W6 gives 495 ms and loses the tick finding.

**Impact.** The PR body gives a cold reviewer the wrong reason for a surviving mutant, and hides that no control pins the UART term of the armed bound.

This does not reach a measured receipt:
- Every row that takes the armed path (`aem_copy_crc`, `restore_walk`) carries a zero allowance.
- Console commands start after arming.

**Required outcome:** the PR body states W6's survival correctly: it is a more lenient rule that no control separates, because no armed-path row carries a UART allowance. Alternatively, a control kills W6 (S1).

**Verification:** a cold read of the PR body, or `grader_mutants` showing W6 KILLED.

### S1 - SUGGESTION - lens: Tests

A fifth armed control would pin the UART term of the armed bound and kill W6: a duty that starts unarmed, carries a non-zero `uart_tx_allowance_ms`, and has an armed lead within the allowance of 500 ms. This is optional; no measured row reaches that path today.

## Judgments on the assigned items

1. **F1 (`bab4f32d`): partly resolved. Retained as F1 above.**
   - Pin 1 now reads the resolved census's stores on the compiled unit, and every compiled store I could plant is refused.
   - Pin 2 closes every C-level address-take, but not a symbol alias.
   - All the other assigned checks hold, with evidence given under F1.
2. **R412-1 F2 (`666f0623`): resolved.**
   - The fourth control (`run.py:520-533`) is one cycle past the allowance: 25,000,001 cycles, a bound of 500.00001 ms. It has an armed block before the duty and a serviced block inside it.
   - W0 passes. W3 and W4 are KILLED, each with the new control's message: "an armed duty's leading gap escaped". W1, W2 and W5 are KILLED (`receipts/grader_mutants_w0_w6.log`).
   - My six round-1 wrong rules are all KILLED at the head (`receipts/service_rule_mutants_r413.log`).
   - The self-test passes 51 checks (`receipts/service_selftest_head.log`). That matches "51 grading controls" in `397_SERVICE_BUDGET.md:318`.
   - The README lines at `README.md:148-158` match the four controls.
   - W6 survives; see F2 and S1.
3. **R413-1 F2: resolved.**
   - The PR body's "Open after lane 2" list names D3 section 5.3 change 3, the restore-wait timeout and the enable line. It also names the persistence-disabled path's unpublished PHY link.
   - Both are recorded on #70 (5904331147).
   - Consistent with the ruling, no firmware change was made.
4. **S1 (`943a3dac`): resolved.** `397_SERVICE_BUDGET.md:175` is accurate:
   - The boot rows' unarmed prefixes are 316.91802 / 970.14222 ms at the base and 373.90220 / 1106.14204 ms at the head, at 1x1 / 8x8.
   - The first PHY read in the 8x8 uart-paced receipt is at cycle 110,679,579, just after the first opportunity at 110,614,268, so the interval spans the prefix.
   - Among `service_findings()`'s checks, only the boot row's 20000 ms budget covers it. The heartbeat gap starts at the first heartbeat, and the PHY interval check is pairwise.
5. **Firmware digest: unchanged.**
   - `milan_baremetal.c` sha256 is `a73ecc25...0eb3` at both `597dba85` and the head. The `sw/firmware` tree id is `dcda3f7b` at both.
   - The capture receipt's `product_firmware_sha256` matches.
   - `scripts/check_nvm_capture.py` passes with all seven controls (`receipts/check_nvm_capture_head.log`).

## Per-lens results

[R413] UNCLEAN Tests - F1: gate 1b keeps the slot for the `alias_sscanf` and `weakref_sscanf` plants.

[R413] UNCLEAN Conformance - F1: the ruling 5894183475 premise and assignment item 1, "No address of `aem_loaded` is taken in the compiled code".

[R413] UNCLEAN Docs - F1 (`test_builder.py:1637-1641`, `BAREMETAL_FIRMWARE.md:929-936,1558`) and F2 (the PR body's W6 rationale).

[R413] PASS RTL - `receipts/round2_scope.txt` (`git diff 597dba85..943a3dac`: 5 files, none under `hdl/`, `syn/`, `constraints/` or `sw/firmware/`; no gitlink change; processor still `b2db3a97`) and `receipts/clone_integrity.log`. Checked that nothing in the RTL lens's scope changed since R413-1 covered it clean at `597dba85` (port connections, PP_STAT packing, clock/reset, deadline derivations, ROM digests). The hosted `rtl-fast`, `verilator-lint`, `elaborate` and `yosys-elaboration` checks on the exact head read success; the manager owns their acceptance.

[R413] UNCLEAN Robustness - F1: the gate's refusal of hostile firmware input, a lens the retained R412-1 F1 also carries.

The Robustness lens was applied, and the rest of its scope was clean at this head:
- `sw/firmware/milan_baremetal/milan_baremetal.c`: sha256 `a73ecc25...0eb3`, identical to `597dba85`, so the boot paths checked in round 1 are unchanged, including CLOSED, refused-window and re-attach;
- `tb/verilator/fw_service_budget/run.py:349-366,493-534`: the new control sits exactly one cycle past the allowance, and the start-armed and ends-before-arm cases hold;
- `scripts/check_nvm_capture.py`: the boundary and one-tick-over controls are detected.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | ruling 5894183475; assignment 5904325345 items 1-4; #70 record 5904331147; the PR body's remaining work; D3 section 5.3 change 3 recorded as open | R413-2 | 943a3dac973abc7130fe1a19bb6f5943788a01fe |
| RTL | CLEAN | `597dba85..943a3dac` scope (no RTL, constraint, firmware or gitlink change); the RTL artifacts covered at R413-1 | R413-2 (scope check); R413-1 (applied, clean) | 943a3dac973abc7130fe1a19bb6f5943788a01fe (R413-1 at ancestor 597dba8593553ad85b1e94936b016907c4d2003a, untouched in scope since) |
| Robustness | UNCLEAN (F1) | the gate against hostile firmware spellings (12 plants); firmware digest; `run.py` armed rule and controls; `check_nvm_capture.py` | R413-2 | 943a3dac973abc7130fe1a19bb6f5943788a01fe |
| Tests | UNCLEAN (F1) | gate 1b: 12 plants and the unplanted head on the head gate, 6 plants and the unplanted head on the round-1 gate, the 9 in-gate controls, the full `test_baremetal_profile_contract()`; grader: self-test, W0-W6, six round-1 rules, W6 direction | R413-2 | 943a3dac973abc7130fe1a19bb6f5943788a01fe |
| Docs | UNCLEAN (F1, F2) | `BAREMETAL_FIRMWARE.md:924-952,1558`; `test_builder.py` comments `:1634-1647,6520-6530,6579-6640,14215-14221`; `397_SERVICE_BUDGET.md:175,318`; `fw_service_budget/README.md:148-158`; PR body | R413-2 | 943a3dac973abc7130fe1a19bb6f5943788a01fe |

## Prior public review findings on PR #623

I read these only after the verdict and ledger above were written. The sources are R412-1 (comment 5904318669) and R413-1 (comment 5904299081).

- **R412-1 F1, MAJOR** (Conformance, Robustness, Tests, Docs; a macro-spelled write or address): **retained, narrowed, and merged into F1.**
  - Its named probes are refused at this head. My equivalent `m_macro_set` and `m_macro_addr` plants were checked, both as a pointer store and as an address handed to `sscanf()`, and so were the gate's own macro controls.
  - Its required outcome, "no compiled code other than the verifier's single assignment can write `aem_loaded`, however that write is spelled", is not met. The alias and weakref plants write it through a library call.
  - F1 therefore carries that finding's lenses, Robustness included.
- **R412-1 F2, MINOR** (Tests; which opportunity arms the writer): **resolved.** W3 and W4 are KILLED by the new control and W0 passes (item 2).
  - That report also calls W6 "stricter, not weaker". It is more lenient (F2 here, `receipts/w6_direction.log`).
- **R412-1 S1:** resolved (item 4).
- **R412-1 S2:** recorded as open on #70 (5904331147) and in the PR body, by ruling. It is not implemented here and was not required.
- **R413-1 F1:** retained, narrowed (F1).
- **R413-1 F2:** resolved (item 3).
- **R413-1 S1:** answered by the same service-page line (item 4).
- **R413-1 S2** (the sweep receipt has no head field): optional and not taken. No sweep was rerun this round.

## Real limits

- The scoped Verilator binary `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host, so no Verilator simulation was run. Round 2 changes no RTL or harness C++.
- Probes ran on scratch copies. Each copy has an index-only `git init` in the three submodules, because the builder test and `check_nvm_capture.py` call `git ls-files` there.
- The full `test_baremetal_profile_contract()` ran once on the shipping head: rc 0, 9/9. Its tool-level foreground cap was exceeded, so the session runner detached it. It ran to completion on the unplanted firmware, and its receipt is complete.
- The builder bank itself was not run.
- The two accepted plants were run through gate 1b and compiled standalone, but no product firmware containing them was linked. That the product's BIOS library provides `sscanf()` is taken, as the gate's own `sscanf()` control takes it.
- I did not rerun native service or capture groups, or the sweep. The firmware is byte-identical, so round 1's receipts stand.
- No hardware was used. Physical calibration was NOT RUN, and field skips are not hardware proof.
- Hosted status at inspection: most exact-head contexts read success. `docs-check`, Verilator shard 1/5 and Verilator shard 4/5 were still in progress. `Physical gPTP` was skipped, which is not an executed job.
- Source validation at `79c36963` is distinct from the current-dev merge candidate at live dev `ec0cc0c1`.

## Pending manager duties

- Rule on F1 (retained) and F2, and note that F2 disagrees with the other reviewer's round-1 statement that W6 is stricter.
- A fix to F1 changes `sw/builder/test_builder.py` and `BAREMETAL_FIRMWARE.md`, which un-covers Tests, Conformance, Robustness and Docs. Those must be covered again at the fix head.
- The current-dev candidate build and validation at the merge turn, hosted/act acceptance and sweep acceptance.
- A second positive review, and a reviewer-owned ledger at the final head.

R413-2 FINISHED
