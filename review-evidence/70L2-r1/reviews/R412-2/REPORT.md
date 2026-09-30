[R412] NEGATIVE - exact head 943a3dac973abc7130fe1a19bb6f5943788a01fe

Round R412-2, internal independent review of kebag-logic/milan-fpga PR #623 (issue #70, lane 2), at exact head `943a3dac973abc7130fe1a19bb6f5943788a01fe`, tree `ffb89f749a18aeb6ec7d843f320fb6b095b08e10`.
The round covers the three commits on the R412-1 head `597dba85`: `bab4f32d`, `666f0623` and `943a3dac`.
Source base `79c36963660c10e4c1c11a744fb5bff41a552b8b`.

Verdict: NEGATIVE, on one open MAJOR, F1. Its lenses are Conformance, Robustness, Tests and Docs.

- **What F1 is.** Gate 1b still keeps the verdict's slot across `nvm_boot()` when the compiled unit hands the verdict's storage to a library call under another symbol, a GNU `alias` of `aem_loaded`. The complete gate 1b passes that firmware (`GATE1B PASS`, slot kept).
- **What round 2 did fix.** All four spellings from round 1 are now refused, each with its pin named: phase-2 splice, `##` paste, macro write and macro address. The round-1 gate accepted all four.
- **R412-1 F2 is resolved.** W3 and W4 are killed and W0 passes.
- **S1 and S2 are resolved.**
- **R413-1 F2 is resolved.**
- **RTL is covered clean.** No RTL, firmware, submodule, synthesis, script or CI byte changed since `597dba85`.
- **The fix scope is small.** F1 needs a change to builder tooling and documentation only. It needs no firmware, RTL or bitstream change.

## Sources reconstructed, in order

1. `AGENTS.md`; `CONTRIBUTING.md` section 3 (verification bar) and section 6 (wording and em-dash rules); `docs/README.md`.
2. Issue #70:
   - the body;
   - the ruling 5894183475, cited through the round-2 assignment;
   - REVIEW READY 5902107952;
   - the round-2 assignment 5904325345. Its rulings: `18199bac` is accepted; D3 section 5.3 change 3 and the PHY link on the persistence-disabled path are recorded open and not implemented here; no firmware, RTL or bitstream change;
   - the #70 record 5904331147;
   - TAKEN 5904344040;
   - REVIEW READY 5905040298 at this head.
3. The PR #623 body at this head, from its "Round 2" section to "What remains for lanes 3-5".
4. `git diff 79c36963..943a3dac` and `git log`. This round's scope is `597dba85..943a3dac`: 5 files, +197/-56 (`sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md`, `tb/verilator/fw_service_budget/run.py` and its `README.md`, `docs/findings/397_SERVICE_BUDGET.md`).
5. Public evidence: the manager's and author's comments on the issue and the PR, which cite the packet `review-evidence/70L2-r1` and `author-r2`.
6. Prior public review findings on PR #623, read only after my own pass over the diff and my probes: R412-1 (5904318669) and R413-1 (5904299081). Each is dispositioned below.

## Method

All probes ran on disposable copies of the head under `scratch/`, never in the review clone.

- **Gate 1b alone.** `scripts/run_gate1b.py` runs `test_baremetal_profile_contract()` alone with the RV32 compiler required. The compiler is the one the gate adopts, recorded in each log.
- **Early stop.** `scripts/early_stop.py` stops right after the shipping-firmware verdict. It prints the kept set and contrasts it with the same assembly under forget-on-call. It takes about 20 s per tree.
- **Complete runs.** A complete gate 1b takes about 15 minutes (897 s at the unplanted head). The two complete runs therefore ran as tracked jobs that I polled until they finished, and both logs end with their own `rc` and elapsed time.
- **Plants.** `scripts/plants2.py` plants one probe as the first statement of `nvm_boot()`. Where the probe needs one, it also adds a file-scope line after `static int aem_loaded;`. The shipping firmware is already AEM-first, so a probe the gate accepts leaves the slot kept across `nvm_boot()`.

## Judgment of the round-2 items

### Item 1 (R412-1 F1 and R413-1 F1): gate 1b pins on the compiled unit, commit `bab4f32d`

| Probe inside `nvm_boot()` | At this head (early stop) | Round-1 gate (`597dba85` test_builder, same firmware) |
|---|---|---|
| none (shipping firmware) | ACCEPTED, `kept=['aem_loaded']`; forget-on-call REFUSED (`receipts/gate1b_early_base.log`) | n/a |
| `aem_loaded = 1;` (plain) | REFUSED by the source rule, "aem_loaded must contain only the image verifier's verdict" (`gate1b_early_plain_write.log`) | refused (R412-1) |
| `aem_\`-newline-`loaded = 1;` (phase-2 splice) | REFUSED on the write pin; resolved `nvm_boot() stores` named (`gate1b_early_splice_write.log`) | ACCEPTED, slot kept (`gate1b_round1gate_early_splice_write.log`) |
| `R412_JOIN(aem_, loaded) = 1;` (`##` paste) | REFUSED on the write pin (`gate1b_early_paste_write.log`) | ACCEPTED (`gate1b_round1gate_early_paste_write.log`) |
| `NVM_FLAG_SET(aem_loaded);` (macro write) | REFUSED on the write pin (`gate1b_early_m_macro_set.log`) | ACCEPTED (`gate1b_round1gate_early_m_macro_set.log`) |
| `*NVM_REF(aem_loaded) = 1;` (macro address, written here) | REFUSED on the write pin (`gate1b_early_m_macro_addr.log`) | accepted (R412-1 receipts) |
| `sscanf("1","%d",NVM_REF(aem_loaded))` (macro address, library write) | REFUSED on the address pin: "address of global register variable 'aem_loaded' requested" (`gate1b_early_m_macro_addr_sscanf.log`) | ACCEPTED (`gate1b_round1gate_early_m_macro_addr_sscanf.log`) |
| store through a GNU alias, `aem_view = 1;` (global or file-local alias) | REFUSED, but by rule 1b ("a STORE this gate cannot PLACE ... sym(aem_view)"), not by a pin (`gate1b_early_alias_write.log`, `gate1b_early_static_alias_write.log`) | n/a |
| **`sscanf("1","%d",&aem_view)` with `extern int aem_view __attribute__((alias("aem_loaded")));`** | **ACCEPTED, `kept=['aem_loaded']`** (`gate1b_early_alias_addr.log`); **complete gate 1b: `GATE1B PASS`, rc 0, 885 s**, with the summary "kept the slot of aem_loaded ... refused 9/9 planted pin breaks" (`gate1b_full_alias_addr.log`) | n/a |
| same, with a file-local `static int aem_view __attribute__((alias("aem_loaded")));` | **ACCEPTED, slot kept** (`gate1b_early_static_alias_addr.log`) | n/a |
| the global alias declared, no statement | **ACCEPTED, slot kept** (`gate1b_early_alias_decl_only.log`). A 585 s bounded complete run was not refused before its timeout (`gate1b_full_alias_decl_only.log`, rc 124) | n/a |

What holds at this head:

- The four new controls exist at `sw/builder/test_builder.py:14273-14290`.
- The complete unplanted run prints "kept the slot of aem_loaded across a call under the verdict's three pins, read on the compiled unit, accepted the AEM-first base only with it kept, and refused 9/9 planted pin breaks on the verdict, each naming its pin". It ends `GATE1B PASS`, rc 0, 897 s (`receipts/gate1b_full_head.log`). So the five older controls stay refused and the shipping firmware passes with the slot kept.
- The rule is no weaker for any other static.
  - `kept` is empty or exactly `{"aem_loaded"}` (`:6737`).
  - `unit = rv32_unit(assembly, kept) if kept else forgetting` (`:6738`) is equivalent to the previous call.
  - The call rule (`:1648`) and `_rv32_forget_symbols` are unchanged apart from comments.
  - The write pin reads the forget-on-call census (`:6731`), so no pin depends on the slot it decides.
- What does not hold is F1 below. The address pin and the linkage pin ask about the name `aem_loaded` in C. The compiled unit can form the verdict's address, and export it, under another symbol that `.set` equates to it.

### Item 2 (R412-1 F2): the grader's arming, commit `666f0623`

The new control is at `tb/verilator/fw_service_budget/run.py:520-534`.

- It builds an armed `milan_status` duty that starts at cycle 150,000,000. The writer is armed at 104,472,844, before the duty.
- The duty has a serviced block inside it, and its leading gap is 25,000,001 cycles, one cycle past 250 ms. So its whole-span bound is 500.00001 ms, over 500.
- The control requires both the tick finding and the PHY finding.
- Under an arming cycle read per duty, or read from the last block, the bound becomes 251 ms and neither finding fires.

The self-test at this head passes 51 checks with 0 failures (`receipts/fw_service_budget_selftest.log`).

`scripts/grader_mutants.py`, the R412-1 script, gives these results (`receipts/grader_mutants.log`):

- W0 (identity) passes.
- W1, W2 and W5 are KILLED.
- **W3 (arming read per duty) and W4 (arming read from the last block) are KILLED**, by "an armed duty's leading gap escaped: arming was not the run's first opportunity".
- W6 survives. It drops the UART allowance, which makes the rule stricter, not weaker.

`scripts/grader_mutants2.py` re-plants, independently, the rule families R413-1 describes in public (`receipts/grader_mutants2.log`):

- exempt the AEM row by name: KILLED;
- drop the 250 ms base from the armed bound: KILLED;
- arm from the block's report cycle instead of its first opportunity: KILLED;
- widen the "ends before arming" boundary: KILLED;
- arm from the earliest event of any kind: survives. That rule can only arm earlier, which charges more, so like W6 it is stricter, not a weakening.

The README (`tb/verilator/fw_service_budget/README.md:148-158`) and `397_SERVICE_BUDGET.md:318` ("51 grading controls") match the four controls.

### Item 3 (R413-1 F2, R412-1 S2): remaining work

The PR body's "Open after lane 2, for the next persistence lane" list names both items and links the #70 record 5904331147, which records both:

- D3 section 5.3 change 3 (the restore-wait timeout and the enable-line wording), with the CLOSED/"fabric entity enabled" consequence;
- the persistence-disabled path's unpublished PHY link.

This is consistent with the assignment's ruling that neither is implemented here.

### Item 4 (R412-1 S1): the 397 line, commit `943a3dac`

`docs/findings/397_SERVICE_BUDGET.md:175` states that reset to the first PHY publication spans boot's unarmed prefix and is graded only by boot's 20000 ms comparison. It also states that the AEM-first order added the AEM copy and CRC, from 316.91802 ms (1x1) and 970.14222 ms (8x8).

- Those two figures are the base's "Boot to entity enabled" no-tick spans (`79c36963:docs/findings/397_SERVICE_BUDGET.md:102,148`).
- The head's values, 373.90220 and 1106.14204 ms, are in the same page's rows `:105` and `:151`.
- The line is accurate and claims no more than it shows.

### Firmware digest and capture

- `sw/firmware` has the same tree at both heads (`dcda3f7b`).
- `milan_baremetal.c` has sha256 `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3` at the head and at `597dba85`, equal to the receipt's `product_firmware_sha256` (`receipts/firmware_digest.log`).
- `scripts/check_nvm_capture.py`, run on a scratch copy of the head, returns rc 0 with seven controls detected (`receipts/check_nvm_capture.log`).

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests, Docs - `sw/builder/test_builder.py:6610-6672` (`aem_verdict_pins`), `:6579-6608` (`verdict_register_diagnostic`), `:1633-1647` (the soundness comment at the call rule), `:14246-14290` (the controls); `docs/integration/BAREMETAL_FIRMWARE.md:924-936` and `:1558`; PR body item 1 - an alias of `aem_loaded` carries its address out of the unit and the slot is still kept

**Authority.**
- Round-2 assignment 5904325345, item 1:
  - the slot crosses a call only when the pins "hold on the compiled code, not the raw text";
  - "No address of `aem_loaded` is taken in the compiled code."
- The ruling's premise, carried forward: nothing else can write the verdict, so keeping its slot makes the resolver no weaker.
- The head's own claims:
  - "no expression hands a pointer to it to any code" (`test_builder.py:1639`, `BAREMETAL_FIRMWARE.md:930-931`);
  - "defined with internal linkage, so no other unit can name it" (`:1640-1641`, `BAREMETAL_FIRMWARE.md:933-934`);
  - "however either is spelled" (`BAREMETAL_FIRMWARE.md:1558`);
  - "so no expression forms that address, however it is spelled" (PR body item 1).
- The gate already treats this construct as a bypass for the choke point. Its control 5 (`test_builder.py:13028-13038`) is a GLOBAL ALIAS, `.set entity_advertise_public,entity_advertise`, which "passes the export and address-taken rule and is caught only by the whitelist beside it". No such whitelist exists for the verdict.

**Evidence.**
- Probe `alias_addr` adds `extern int aem_view __attribute__((alias("aem_loaded")));` after the verdict's declaration, and `(void)sscanf("1", "%d", &aem_view);` as the first statement of `nvm_boot()`.
- The shipping-firmware verdict keeps the slot: `kept=['aem_loaded']` (`receipts/gate1b_early_alias_addr.log`).
- The complete gate 1b passes: `GATE1B PASS`, rc 0, 885 s (`receipts/gate1b_full_alias_addr.log`).
- The compiled census unit (`receipts/census_asm_alias_addr.s`, excerpt `receipts/census_asm_alias_addr.grep`):
  - line 10: `.set aem_view,aem_loaded`;
  - line 9: `.globl aem_view`;
  - line 3948: `lla a2,aem_view`, followed by `call __isoc99_sscanf@plt`, in `nvm_boot`.
- Why each pin misses it:
  - The write pin sees no store. The library makes the write.
  - The register-variable compile accepts, because `&aem_view` is not `&aem_loaded` in C.
  - The static pin finds no `.globl aem_loaded`.
  - The other-units pin searches only for the name `aem_loaded`.
- A file-local alias (`static_alias_addr`) is also accepted with the slot kept (`receipts/gate1b_early_static_alias_addr.log`). So internal linkage does not close the gap.
- The alias declaration alone (`alias_decl_only`) is accepted with the slot kept (`receipts/gate1b_early_alias_decl_only.log`). It exports a global name for the verdict's storage to every unit and to the BIOS the library links into, which contradicts "no other unit can name it".
- The same construct run on the host (`scripts/alias_semantics_demo.c`, `receipts/alias_semantics_demo.log`): the verifier returns 0, `nvm_boot()` hands `&aem_view` to `sscanf()`, and the verdict reads back `aem_loaded=1`.

**Impact.**
- A firmware can advertise the entity after an AEM CRC failure: `entity_advertise()` receives a verdict a callee overwrote through the alias. Gate 1b certifies that firmware with the slot kept.
- At the base, under forget-on-call, the resolver refused any verdict that crossed a call. So for this class the resolver is still weaker than before, contrary to the ruling's premise.
- The four statements quoted above are false.
- The shipping firmware is correct. The defect is in what the gate proves and what the documents claim.
- A store through the alias is refused today only because the census cannot place `sym(aem_view)`. The gate's model states that a store placed at "another static" is taken not to land on the verdict. So if the census ever learns `.set`, that store would pass as well.

**Required outcome.**
- The slot crosses a call only when no symbol other than `aem_loaded` names its storage in the compiled unit, and when the compiled unit forms its address nowhere except for the loads and stores the census places.
  - For example: refuse to keep the slot when the assembly equates any symbol to `aem_loaded` (`.set`, `.equ`, `=`, `.weakref`, or an alias attribute on the preprocessed unit).
  - Or apply to the verdict the same allowlist of assembly forms the choke point has, reading every line that names it, and every alias of it.
- Planted controls refuse, each with its pin named:
  - an alias's address handed to `sscanf()`, with a global alias and with a file-local one;
  - a global alias declared with no statement.
- The comment at the rule, `BAREMETAL_FIRMWARE.md:924-936` and `:1558`, and the PR body claim only what the pins then prove.

**Verification.**
- `scripts/plants2.py` with `alias_addr`, `static_alias_addr` and `alias_decl_only`, run through `scripts/early_stop.py` and `scripts/run_gate1b.py` on fresh copies: each is refused on the verdict with its pin named.
- The unplanted head still passes with the slot kept.
- The nine existing controls and the six refused probes above stay refused.

## Disposition of prior public review findings at this head

| Finding | Disposition | Evidence |
|---|---|---|
| R412-1 F1 (MAJOR): macro-spelled write and address | RESOLVED for the spellings it named (`m_macro_set`, `m_macro_addr`, and the address handed to a library call), which the gate now refuses on the pins. Its required outcome ("however that write is spelled") is **not fully met**: the alias spelling of the address survives. That is carried as R412-2 F1, the same defect class | table above; `receipts/gate1b_early_m_macro_*.log`, `gate1b_full_alias_addr.log` |
| R412-1 F2 (MINOR): the grader's arming not pinned | RESOLVED | `receipts/grader_mutants.log` (W3, W4 KILLED; W0 passes) |
| R412-1 S1 (SUGGESTION) | RESOLVED | `docs/findings/397_SERVICE_BUDGET.md:175` |
| R412-1 S2 (SUGGESTION, new work) | RESOLVED as recorded open work | PR body remaining-work list; #70 record 5904331147 |
| R413-1 F1 (MAJOR): splice and paste writes | RESOLVED for splice and paste; `alias_write` is refused by rule 1b. The underlying requirement, pins held on what the compiler compiled, is retained under R412-2 F1 for the alias address | `receipts/gate1b_early_{splice,paste}_write.log`, `gate1b_early_alias_write.log` |
| R413-1 F2 (MINOR): section 5.3 change 3 not recorded open | RESOLVED | PR body; #70 record 5904331147 |
| R413-1 S1 (SUGGESTION): reset-to-first-service interval | Addressed in prose by the 397 line; optional, no action required | `397_SERVICE_BUDGET.md:175` |
| R413-1 S2 (SUGGESTION): sweep receipt lacks a source-head field | Retained as optional and owned by the manager. No firmware or RTL change this round, so the sweep receipt is unchanged | none at this head |

## Per-lens results at this head

[R412] UNCLEAN Conformance - F1. Artifacts: assignment 5904325345 items 1-4 against `test_builder.py:6610-6672,14246-14290`, `run.py:493-534`, `397_SERVICE_BUDGET.md:175`, the PR body and the #70 record. Items 2-4 are met, and item 1's "No address of aem_loaded is taken in the compiled code" is not.

[R412] PASS RTL - `git diff 597dba85..943a3dac -- hdl protocol-processor gptp-processor third_party external sw/firmware sw/litex syn scripts .github` is empty, and the gitlinks are unchanged (`receipts/clone_integrity_end.log`). RTL was covered clean by R412-1 at `597dba85`, an ancestor of this head, and nothing in RTL scope has changed since. The gate's RTL-reading rules (the reset literal of `adp_ctrl`/`pp_ctrl_r` and the enable `assign`) are untouched by `bab4f32d`. No RTL harness ran this round; see limits.

[R412] UNCLEAN Robustness - F1. Artifacts: fourteen probe spellings against gate 1b (the table above), the grader's boundary cases (one cycle past, starting armed, ending before arming) with the W and X mutants, and the firmware's boot paths, unchanged since `597dba85` (tree `dcda3f7b`).

[R412] UNCLEAN Tests - F1. The gate's nine controls (`test_builder.py:14246-14290`) miss the alias class. The grader's four controls (`run.py:493-534`) kill every weakening rule tried (`receipts/grader_mutants*.log`). The self-test passes 51 checks with 0 failures.

[R412] UNCLEAN Docs - F1. `BAREMETAL_FIRMWARE.md:924-936,1558`, the comment at `test_builder.py:1633-1647` and the PR body item 1 overstate what is proven. The other changed pages are accurate:

- `fw_service_budget/README.md:148-158`;
- `397_SERVICE_BUDGET.md:175,318`;
- `docs_check.py` rc 0, with 0 em dashes on added lines this round and `git diff --check` clean (`receipts/docs_local_checks.log`).

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Assignment 5904325345 items 1-4 and the rulings; #70 record 5904331147; PR body; `test_builder.py:6579-6672,6731-6738,14246-14290`; `run.py:349-366,493-534`; `397_SERVICE_BUDGET.md:175` | R412-2 | 943a3dac973abc7130fe1a19bb6f5943788a01fe |
| RTL | CLEAN | Empty RTL/firmware/submodule/syn/scripts/CI diff `597dba85..943a3dac`; gitlinks `protocol-processor b2db3a97`, `gptp-processor 5dce647a`, `third_party/verilog-axis 48ff7a7e`; RTL covered clean by R412-1 at ancestor `597dba85`, whose artifacts are `KL_pp_shadow.sv`, `milan_csr.sv`, `milan_datapath.sv`, the processor top and the ROM digests | R412-2 (scope unchanged since R412-1) | 943a3dac973abc7130fe1a19bb6f5943788a01fe |
| Robustness | UNCLEAN (F1) | Gate-1b probes: plain, splice, paste, macro write, macro address, macro address to `sscanf()`, alias write global and file-local, alias address global and file-local, alias declaration alone; grader boundary cases and mutants; firmware boot paths unchanged | R412-2 | 943a3dac973abc7130fe1a19bb6f5943788a01fe |
| Tests | UNCLEAN (F1) | Complete gate 1b at the head (9/9 controls, slot kept, PASS); the alias probe's complete run (PASS); round-1-gate contrast for the four new controls; grader self-test (51/0), W0-W6 and X1-X5 | R412-2 | 943a3dac973abc7130fe1a19bb6f5943788a01fe |
| Docs | UNCLEAN (F1) | `BAREMETAL_FIRMWARE.md:918-955,1558`; the comments at `test_builder.py:1633-1647,6521-6528,6613-6635,14215-14221`; `fw_service_budget/README.md:145-158`; `397_SERVICE_BUDGET.md:170-180,318`; PR body; `docs_check.py`; em-dash scan of added lines | R412-2 | 943a3dac973abc7130fe1a19bb6f5943788a01fe |

## Real limits of this round

- The scoped simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I did not substitute another build, so no Verilator harness ran. RTL coverage rests on the empty RTL-scope diff since `597dba85` and on R412-1's coverage at that ancestor.
- The pinned Markdown environment (`cmarkgfm`/`html5lib` lock) is not installed here, and I made no install. So `check_em_dash.py`, `gen_toc.py` and the other renderer-backed Markdown gates did not run. I ran `docs_check.py` and a direct scan of added lines instead. The manager's docs gates at this head are public evidence.
- I ran gate 1b alone, not the builder bank. It ran with the RV32 compiler present only; the arm with every compiler candidate hidden did not run here.
- The complete gate-1b runs took 885-897 s, beyond one foreground call, so they ran as tracked jobs polled to completion. The `alias_decl_only` complete run was bounded at 585 s and was not refused within that time. Its acceptance rests on the early-stop verdict.
- I did not run the native service groups, the capture harness, Yosys, timing or hosted/act CI. No firmware, RTL or bitstream byte changed, so round 1's capture receipt, native evidence and sweep stand on their public receipts, and the manager confirms that.
- Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof.
- The review clone was never modified. After the probes I re-verified it (`receipts/clone_integrity_end.log`):
  - HEAD and index tree equal the head;
  - no status entries, including untracked and ignored ones;
  - no assume-unchanged or skip-worktree entries;
  - the index equals the HEAD tree by mode, blob and path, and every tracked file hashes to its blob;
  - gitlinks `protocol-processor b2db3a97`, `gptp-processor 5dce647a` and `third_party/verilog-axis 48ff7a7e` are checked out clean, and `external` is uninitialised as at the start.

## Pending manager duties

- Rule on F1. Its fix is builder tooling and documentation only; after it, re-review covers at least Conformance, Robustness, Tests and Docs at the fix head.
- Current-dev candidate build and validation at the merge turn: source base `79c36963`, live dev `ec0cc0c1`. Hosted/act acceptance at the exact head, distinguishing executed jobs from skipped contexts.
- Confirm at the final head that the capture receipt, native evidence and the sweep still stand. This round found the firmware digest unchanged.
- A second positive review and a reviewer-owned ledger at the final head.

R412-2 FINISHED
