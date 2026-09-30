# [A455] #70 lane 2, round 2 (PR #623): handoff

Status: REVIEW READY at `943a3dac973abc7130fe1a19bb6f5943788a01fe` (items 1-4
done, every gate rc 0 at that head, clean tree)

- Repository: kebag-logic/milan-fpga, branch `70-lane2-pin-d352`, local only
  (no push, no PR operation).
- Start head: `597dba8593553ad85b1e94936b016907c4d2003a` (round 1).
- Round-2 head: `943a3dac973abc7130fe1a19bb6f5943788a01fe`.
- Processor pin: `b2db3a970cedbbff2f8ba813acb96122c442bc58`, unchanged.
- Assignment: #70 comment 5904325345 (rulings: `18199bac` accepted; D3
  section 5.3 change 3 recorded as open, not implemented here). Ruling on the
  kept slot: 5894183475. Reviews: R412-1 (PR #623 5904318669) and R413-1
  (PR #623 5904299081). #70 record of the two open items: 5904331147.
- TAKEN: #70 comment 5904344040.

## Commits (one per item; item 3 is the PR body only)

| Item | Commit | Subject |
|---|---|---|
| 1 (R412-1 F1, R413-1 F1) | `bab4f32dd8f05ee8014ec6470f2b0b1746c44edc` | Read gate 1b's verdict pins on the compiled unit, the census's stores and a register-variable compile, and refuse a spliced, pasted or macro-spelled write and a macro-spelled address |
| 2 (R412-1 F2) | `666f0623b6f5a4f92745f21ca9ad95ac476b127b` | Pin the service grader's arming to the run's first opportunity with an armed command whose leading gap is one cycle past the allowance |
| 3 (R413-1 F2, R412-1 S2) | none | PR body remaining-work list (below) |
| 4 (R412-1 S1) | `943a3dac973abc7130fe1a19bb6f5943788a01fe` | State in the service-budget page that only boot's 20000 ms comparison grades reset to the first PHY publication, and how the AEM-first order lengthened that prefix |

`git diff --stat 597dba85..943a3dac`: `sw/builder/test_builder.py`,
`docs/integration/BAREMETAL_FIRMWARE.md`, `tb/verilator/fw_service_budget/run.py`,
`tb/verilator/fw_service_budget/README.md`, `docs/findings/397_SERVICE_BUDGET.md`.
No firmware, RTL, harness-RTL, bitstream input or CI definition is touched.

## Item 1: gate 1b's pins hold on the compiled code

### The change

- `sw/builder/test_builder.py:1632-1648`, the call rule's soundness comment:
  states the three compiled pins and the model boundary (a store the census
  cannot place is refused by rule 1b; one placed at a number, a range, the
  stack or another static is taken, as everywhere in this model, not to land
  on the verdict), and claims only "within that model nothing writes it but
  that one store".
- `:6521-6528`: `verdict_write_re` and `verdict_address_taken()` stay the
  source rules of `assert_boot_contract()` (unchanged at `:11508-11518`); the
  comment now says they read the text as written and that the pins do not use
  them.
- `:6553-6555`: `VERDICT_PIN_WRITE` names the compiled fact ("the compiled unit
  stores to aem_loaded other than milan_init()'s one store of
  load_aem_image()'s return"). `VERDICT_PIN_ADDRESS`, `VERDICT_PIN_STATIC`,
  `VERDICT_PIN_UNIT` keep their text.
- `:6579-6608`, new `verdict_register_diagnostic()`: the preprocessed unit
  (`preprocess_take()`, the census's own compiler and flags) with its one
  `static int aem_loaded;` blanked and `register int aem_loaded
  __asm__("s1");` placed first (GCC requires a global register variable before
  any function definition); compiled `-std=gnu99 -x cpp-output
  -fsyntax-only`. C forbids taking a register variable's address, so the
  compiler answers for every spelling. Measured before use on a probe unit:
  `*NVM_REF(x) = 1`, `f(&J(aem_,loaded))` and `*&x = 2` are each refused
  ("address of global register variable 'aem_loaded' requested"); `sizeof`,
  `__typeof__`, reads and the verifier's assignment compile.
- `:6610-6672`, `aem_verdict_pins(assembly, unit, preprocessed, units)`:
  1. write pin: every store of `unit["runs"]` whose resolved address is
     `Rv32Where("sym", "aem_loaded")`, over every function, must be exactly
     `[("milan_init", <call:load_aem_image>)]`; the refusal lists what was
     resolved;
  2. address pin: exactly one `static int aem_loaded;` line in the blanked
     preprocessed unit, and the register diagnostic accepts it; otherwise the
     refusal carries the compiler's error, or says it was not asked;
  3. static pin: that declaration count, `aem_loaded` defined by the assembly,
     not `.globl`, `.comm` only with `.local` (the assembly checks are
     round 1's); unit pin: unchanged text read of the other linked units, and
     the docstring now says that what actually keeps them from naming it is
     the internal linkage the assembly shows.
- `:6674-6738`, `assert_resolved_boot_flow()` (pins read at `:6731-6738`): the pins read `forgetting =
  rv32_unit(assembly)` (forget-on-call, so no pin depends on the slot it
  decides) and `preprocess_take(source, label)`; the kept unit is computed
  only when every pin holds. No new parameter (the Python idiom ratchet of
  seven over-long signatures holds).
- `:14205-14222` comment, `:14237-14245` `in_nvm_boot()`, `:14273-14290`: four
  new planted controls (below). `:16738`: the summary line says the pins are
  read on the compiled unit.
- `docs/integration/BAREMETAL_FIRMWARE.md:922-952`: the kept-slot paragraph
  states the three compiled pins, the model boundary, "within that model
  nothing writes it but that one store", and the nine controls; `:1558` the
  rules-table row ("however either is spelled", "read on the compiled unit").

### Planted controls (gate 1b, each refused on the verdict pin with its pin named)

Refusal text is the suffix of "enters entity_advertise() with [None] ...
aem_loaded's slot did not cross a call, because: ..." (receipt
`receipts/gate1b_pins_controls_worktree.log`, and the complete run in the
gate bank below).

| Control | Pin | Refusal text after "because:" |
|---|---|---|
| `aem_loaded = 0;` inside `nvm_boot()` | write | the compiled unit stores to aem_loaded other than milan_init()'s one store of load_aem_image()'s return (resolved: milan_init() stores <call:load_aem_image>, nvm_boot() stores 0) |
| `aem_loaded = 1;` in the UART status handler | write | ... (resolved: milan_init() stores <call:load_aem_image>, milan_status_handler() stores 1) |
| `int *clear_p = &aem_loaded; *clear_p = 0;` in `nvm_boot()` | address (and write) | ... nvm_boot() stores 0); the address of aem_loaded is taken (the compiler, with aem_loaded a register variable: address of global register variable 'aem_loaded' requested) |
| `int aem_loaded;` (no `static`) | static | the address of aem_loaded is taken (the compiler was not asked: the preprocessed unit declares `static int aem_loaded;` 0 time(s)); aem_loaded is not a file-scope static of the compiled unit |
| second translation unit `milan_verdict.c` declaring it | unit | aem_loaded is named in a second translation unit (milan_verdict.c) |
| NEW: `aem_\`-newline-`loaded = 1;` in `nvm_boot()` | write | ... (resolved: milan_init() stores <call:load_aem_image>, nvm_boot() stores 1) |
| NEW: `MILAN_VERDICT_JOIN(aem_, loaded) = 1;` (`a##b`) in `nvm_boot()` | write | ... nvm_boot() stores 1) |
| NEW: `MILAN_VERDICT_SET(aem_loaded);` (`((flag) = 1)`) in `nvm_boot()` | write | ... nvm_boot() stores 1) |
| NEW: `(void)sscanf("1", "%d", MILAN_VERDICT_REF(aem_loaded));` (`(&(obj))`) in `nvm_boot()` | address alone | the address of aem_loaded is taken (the compiler, with aem_loaded a register variable: address of global register variable 'aem_loaded' requested) |

The last control is the one the census cannot see at all (libc makes the
write), so it is refused by the address pin alone: it shows the address pin
is load-bearing. The shipping firmware and the AEM-first base are accepted
with `kept=['aem_loaded']`; the base with no source handed in (forget-on-call)
is refused on the verdict.

**Each new control can fail** (`probes/old_gate_controls.py`, receipt
`receipts/round1_gate_new_controls.log`): the four controls copied byte for
byte into the round-1 builder (`597dba85`) are all ACCEPTED there ("ROUND-1
GATE ACCEPTED" for each), i.e. the round-1 text pins kept the slot and the
resolver passed them.

### The reviewers' probes, rerun with their own scripts

`probes/rerun_reviewer_probes.py` copies the committed tree's tracked files
into fresh scratch trees and runs R413-1's `instrument_builder.py`,
`plants.py`, `run_gate1b.py` (stopped after the shipping-firmware verdict) and
R412-1's `early_stop.py`, `plant.py`, `run_gate1b.py` (early and complete).
Only adaptation: R413's `plants.py` read the head's firmware from its review
clone, which does not exist on this host; a copy reads a pristine copy of
this head's firmware, which is byte-identical to `597dba85`'s (the script
asserts it). Receipts `receipts/bab4f32d/` (first run, at the item-1 commit)
and `receipts/943a3dac/` (rerun at the round-2 head): the same outcome for
every probe. The two census assemblies R412's early stop dumped differ only in
the temporary directory named by four inline-asm line markers.

| Probe | Result | Reason named |
|---|---|---|
| R413 `none` | ACCEPTED, `kept=['aem_loaded']` | |
| R413 `none` + `R413_FORCE_FORGET=1` | REFUSED | enters entity_advertise() with [None] (forget-on-call) |
| R413 `plain_write` | REFUSED | source rule: "aem_loaded must contain only the image verifier's verdict" |
| R413 `splice_write` | REFUSED | verdict; write pin (nvm_boot() stores 1) |
| R413 `paste_write` | REFUSED | verdict; write pin (nvm_boot() stores 1) |
| R413 `alias_write` | REFUSED | rule 1b: a STORE this gate cannot PLACE ... nvm_boot() through sym(milan_r413_alias) |
| R412 early, unplanted | ACCEPTED, `kept=['aem_loaded']`; forget-on-call REFUSED | |
| R412 `m_macro_set` (early and complete) | REFUSED | verdict; write pin (nvm_boot() stores 1) |
| R412 `m_macro_addr` (early and complete) | REFUSED | verdict; write pin (nvm_boot() stores 1) and address pin (address of global register variable 'aem_loaded' requested) |
| R412 `m_ctrl_direct` | REFUSED | source rule, as in round 1 |

## Item 2: the service grader's arming is pinned

- `tb/verilator/fw_service_budget/run.py:520-534`: a fourth control in
  `armed_controls()`. Writer armed by one opportunity at cycle 104,472,844
  (the recorded 8x8 arming); a `milan_status` duty from 150,000,000 to
  180,000,001 whose first opportunity inside is at +25,000,001 (250 ms and one
  cycle), then one every 100,000 cycles (50 in the block). The row is built as
  `add_tick_bounds()` builds one (`tick_span()` over the same events, bound
  250 + no-tick + TX allowance 0). Required: exactly "over-budget tick
  stretch: milan_status" and "over-budget PHY service stretch: milan_status".
  Refusal text when it fails: "an armed duty's leading gap escaped: arming was
  not the run's first opportunity". The grader's rule lines (`armed_bound()`
  `:349-366`) are unchanged, so the reviewers' mutant anchors still apply.
- `tb/verilator/fw_service_budget/README.md:148-158`: "the run's first
  heartbeat opportunity"; four controls, and what each pins, including that an
  arming cycle read per duty, or from a later block, is refused.
- `docs/findings/397_SERVICE_BUDGET.md:318`: 51 grading controls (the
  self-test's own count; it was 50).

### Grader mutants (self-test run on each; R412-1 `grader_mutants.py` unchanged, R413-1 `armed_mutants.py` with its review-clone path swapped for a pristine copy of the committed `run.py`)

| Mutant | Round 1 (R412-1 receipt) | Round 2 head | Killing check |
|---|---|---|---|
| W0 identity | passes | passes (51 checks) | |
| W1 whole span | KILLED | KILLED | unarmed AEM prefix was charged as an armed gap |
| W2 unarmed never charged | KILLED | KILLED | armed bound not recorded |
| W3 arming read per duty | SURVIVED | **KILLED** | an armed duty's leading gap escaped: arming was not the run's first opportunity |
| W4 arming from the last block | SURVIVED | **KILLED** | same |
| W5 PHY stretch on the whole span | KILLED | KILLED | unarmed AEM prefix was charged as an armed gap |
| W6 armed bound without the UART allowance | passes | passes | stricter, not weaker (R412-1's own reading); not required |
| R413 skip_every_unarmed_start | KILLED | KILLED | armed bound not recorded |
| R413 anchor_last_tick | KILLED | KILLED | tick block crossed a duty boundary |
| R413 anchor_first_heartbeat_write | KILLED | KILLED | unarmed AEM prefix was charged as an armed gap |
| R413 span_from_duty_start | KILLED | KILLED | unarmed AEM prefix was charged as an armed gap |
| R413 exempt_aem_by_name | KILLED | KILLED | armed bound not recorded |
| R413 armed_bound_without_250_base | KILLED | KILLED | armed bound not recorded |

R412-1's `w3_demo.py` rerun: the head grader refuses the 400 ms armed lead on
both stretches; the W3 and W4 copies return no finding, which is the weakening
the new self-test control now kills.

## Item 3: remaining work (PR body)

The PR body's remaining-work list gains "Open after lane 2, for the next
persistence lane": D3 section 5.3 change 3 (restore-wait timeout and the
enable line reporting that the fabric holds the enable; `entity_advertise()`
still prints "fabric entity enabled" after a CLOSED restore) and the
persistence-disabled path's unpublished PHY link (`nvm_started` never set, so
`phy_link_tick()` never runs; the link-status CSR keeps its reset constant,
`sw/litex/milan_soc.py:1748-1762`: link up, board-wiring speed, full duplex).
Both point to the #70 record 5904331147. No repository change.

## Item 4: the reset-to-first-PHY-publication prefix

`docs/findings/397_SERVICE_BUDGET.md:175`, one line after "Boot's unarmed
prefix precedes the first heartbeat opportunity.": reset to the first PHY
publication spans that prefix, only boot's 20000 ms comparison grades it, and
the AEM-first order added the AEM copy and CRC to it, from 316.91802 ms at 1x1
and 970.14222 ms at 8x8 (the base page's boot rows at `79c36963`; the current
373.90220 and 1106.14204 ms stay in the page's tables). Checked against the
firmware: `nvm_heartbeat_tick()` returns before `phy_link_tick()` until
`nvm_started` (`milan_baremetal.c:933-937`).

## Gates at the round-2 head

`run_gates.py` (this packet) at `943a3dac`, clean tree before and after, the
physical path, never piped; logs outside the packet, each with its size and
SHA-256 in `gates-943a3dac.json`. The two builder banks ran one after the other;
the other gates ran in a second chain beside them.

| Gate | Command | rc | Seconds | Result |
|---|---|---|---|---|
| builder-present | `test_builder.py --require-elaboration --require-rv32` (LiteX venv) | 0 | 1050.6 | gate 1b: "kept the slot of aem_loaded across a call under the verdict's three pins, read on the compiled unit, accepted the AEM-first base only with it kept, and refused 9/9 planted pin breaks on the verdict, each naming its pin"; closes "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11: the calibration build tree is not on disk, as in round 1) |
| builder-absent | `full-builder-absent.py` (every cross-compiler candidate hidden) | 0 | 675.3 | "FULL BUILDER ABSENT PASS: all three cross-compiler candidates hidden"; "EXCEPT 2 NOT RUN": gate 1b's compiled census (no RV32 target, by design of this arm) and gate 11 |
| fw_service_budget-selftest | `run.py --self-test` | 0 | 0.6 | "fw_service_budget_oracle: checks: 51 failures: 0", flash 14/0 |
| grader-mutants | `check_mutants.py` | 0 | 2.2 | W0 passes; W1-W5 KILLED (W3, W4 by the new control); W6 passes (stricter); R413's six KILLED |
| check_nvm_capture | `scripts/check_nvm_capture.py` | 0 | 0.7 | seven controls detected; "capture census, clocks, both timing arms and receipt agree" |
| firmware-digest | `check_firmware_digest.py` | 0 | 0.0 | `sw/firmware` unchanged since `597dba85`; `milan_baremetal.c` sha256 `a73ecc25...0eb3` = reviewed head = capture receipt |
| check_py_idiom | `scripts/check_py_idiom.py` | 0 | 3.4 | every ratchet holds (too many parameters 7 <= 7) |
| measure_test_evidence | `scripts/measure_test_evidence.py --check` | 0 | 5.7 | |
| diff-check | `git diff --check 79c36963 HEAD` | 0 | 0.0 | |
| md-docs_check, md-check_doc_paths, md-check_doc_style, md-check_archive, md-gen_toc, md-check_em_dash | pinned Markdown environment | 0 each | 0.0-4.5 | |

Also at the head, outside the receipt: both reviewers' gate-1b probes
(`receipts/943a3dac/`, above).

## Firmware digest

`sw/firmware` has no difference from `597dba85`;
`sw/firmware/milan_baremetal/milan_baremetal.c` sha256
`a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3` at
`597dba85`, at `943a3dac`, and in `tb/verilator/nvm_capture_cpu/measurements.json`
`product_firmware_sha256` (`check_firmware_digest.py`, gate `firmware-digest`).
`check_nvm_capture` rc 0 at `943a3dac`.

## Not done, and why

- No native service or capture re-run, no sweep: no firmware, RTL or
  bitstream input changed (the assignment expects none), so round 1's
  receipts stand; the manager confirms at the new head.
- W6 still passes the self-test; it is stricter than the rule, and the
  assignment requires only W3 and W4 killed.
- No hardware, bench, flashing, push or PR operation.

## Head and tree

- Head `943a3dac973abc7130fe1a19bb6f5943788a01fe`, tree
  `ffb89f749a18aeb6ec7d843f320fb6b095b08e10`, 24 commits on dev `79c36963`
  (three this round on round 1's `597dba85`).
- Gitlinks unchanged: `protocol-processor` `b2db3a97`, `gptp-processor`
  `5dce647a`, `third_party/verilog-axis` `48ff7a7e`.

## Packet

- `PR-BODY.md` (Round 2 section, remaining-work list), `TAKEN.md`,
  `REVIEW-READY.md`, `HANDOFF.md`, `gates-943a3dac.json`, `MANIFEST.sha256`.
- `run_gates.py`, `check_mutants.py`, `check_firmware_digest.py`,
  `full-builder-absent.py` (round 1's), `run_detached.sh`, `wait_for.py`.
- `probes/`: `instrument_gate1b.py`, `run_gate1b.py`, `old_gate_controls.py`,
  `rerun_reviewer_probes.py`.
- `receipts/`: the reviewer probes at both heads, the round-1 gate with the new
  controls, the worktree controls run.
