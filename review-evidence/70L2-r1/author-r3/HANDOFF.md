# [A457] #70 lane 2 round 3 handoff (PR #623)

Status: **item 1 done as ruled (`0a80abcb`), item 2 done (`a033bfd8`)**. Every gate is rc 0 at
`0a80abcb` (clean tree, physical path, never piped), both builder banks included. REVIEW READY is
posted.

A host power-off (2026-09-30 10:30 to 11:34) cut the first gate run at `0a80abcb` while the
builder bank was running, and emptied `/tmp`, logs included. The whole gate bank was then rerun
from the start at the same head and clean tree. `gates-0a80abcb.json` is that rerun's receipt.
The probe receipts under `receipts/` were complete before the power-off, and are kept as
they were.

- Branch `70-lane2-pin-d352`, local only. Start head `943a3dac973abc7130fe1a19bb6f5943788a01fe`.
- End head `0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4`, tree `47a0b44682dee2817b131da935a9e2dffd42bd53`.
  That is 26 commits on dev `79c36963`, two this round (`a033bfd8`, `0a80abcb`). Processor pin
  `b2db3a97`, unchanged.
- Assignment: round 3 on #70, comment 5905511808. The STOP on item 1 (5906387036) was ruled by
  5906400668: option 1. Also read: ruling 5894183475, and the reviews R412-2 (5905505282) and
  R413-2 (5905465715).
- On #70: TAKEN 5905847785, STOP 5906387036, REVIEW READY 5909022757 (this round's final post,
  text in `REVIEW-READY.md`).

## Item 1: F1, as ruled (`0a80abcb`)

### The change

`sw/builder/test_builder.py`:

- `:1964-2160`, module level: the linked-image reader.
  - `rv32_image()` (`:2018`) reads an ELF32 little-endian image by hand: the section headers,
    the symbol table and every RELA table that applies to an allocated section. A
    `%pcrel_lo` is placed at its upper part's target. It returns the major opcode of each
    allocated word, and every AUIPC in an executable section with no call, GOT or PC-relative
    relocation at its site. An RVC image is flagged and its words are not read. An SHT_REL
    table is refused, since RISC-V never emits one.
  - `rv32_image_references()` (`:2115`) lists every relocation that lands on a byte range, under
    any symbol. Each gets a role: the upper part, a load in place, a store in place, or a
    sentence saying how the full address is formed (`%lo` on an `addi`, a GOT entry, a data word,
    anything else).
  - The ELF gABI and RISC-V psABI numbers are named constants with their source stated. A
    misread number cannot pass quietly: the shipping image must show the store and the loads in
    place, and each control must be refused on its class.
- `:4749` `census_flags`: one tuple for both census compiles (`census_take()` now uses it).
- `:6765-6782` the pins. Five are decided on the image: the store (`VERDICT_PIN_WRITE`), escape,
  one name, local object, AUIPC. Three are kept as early diagnostics: address (register
  variable), static, second unit.
- `:6838` `verdict_image_layout`, `:6845` `verdict_image_take()`: the census's compiler, driver,
  flags and stub headers plus `-no-pie`, `-c`. Then a link with the same driver: `-nostdlib
  -nostartfiles -static -Wl,-q -Wl,--no-relax -Wl,--unresolved-symbols=ignore-all -Wl,-e,0` and a
  script that defines no symbol.
- `:6881` `verdict_image_pins()`, which decides:
  - the store: the image's in-place stores are exactly `milan_init()`'s, AND the resolver on the
    PIC census compile (forget-on-call) finds exactly `milan_init()` storing
    `<call:load_aem_image>` on any symbol the image places on the verdict's bytes, or does not
    know at all. A name the image leaves undefined is placed by the product's linker in another
    unit, and rule 1b refuses a store through it;
  - escape: every other reference is an upper part or a load in place;
  - one name: no other defined symbol overlaps the bytes;
  - local object;
  - AUIPC: no RVC, no bare AUIPC.
- The docstring states the literal-address limit.
- `:6974` `aem_verdict_pins()` now takes the image and returns `(broken, references)`. The
  by-name write check is gone; the by-address store pin above subsumes it.
- `:7090` the resolver takes the image of `source`. The line R413-2's instrument edits,
  `kept = frozenset() if broken else ...`, is unchanged. `:7499` returns `verdict_references`.
- `:1634-1658` the call-rule comment states what the image census proves, and the literal-address
  limit (#495).
- `:14570-14737` the controls. Each entry's second field is now a tuple of the pins its refusal
  must name. Five new entries (`:14658`, `:14668`, `:14674`, `:14679`, `:14685`). The loop at
  `:14719` names the pins missing from a refusal.
- `:17139` the gate's summary sentence: the shipping image's references, `n/n` breaks, and the
  literal limit.

`docs/integration/BAREMETAL_FIRMWARE.md`:

- `:922-1003` (was `:922-952`): the pins, by address on the `-no-pie` image. Also the code-model
  reason, the early diagnostics, **Limit, stated rather than closed** (`:964`), and a table of
  the fourteen breaks with the pins each must name.
- `:1605` (was `:1558`): the refusal row, rewritten to what the census proves, plus the limit.

`CHANGELOG.md:65-66`: two lines, the pins read by address on a linked image, and the literal
limit.

No firmware, RTL, bitstream, CI or processor byte changed. No new tool: the census uses the
census's own compiler (the pinned SDK under `--require-rv32`).

### Planted controls (gate 1b, `receipts/verdict_controls_0a80abcb.log`)

Run with `probes/instrument_verdict_controls_r3.py`. That is R413-2's
`instrument_verdict_controls.py` adapted to the tuple field, since the original reads the loop's
old `pin` name. The shipping AEM-first base is accepted with `kept = ['aem_loaded']`. Its image
references are milan_init() upper part, store in place, upper part, load in place, and
milan_status_handler() upper part, load in place. Refused 14 of 14:

| Control (inside `nvm_boot()` unless stated) | Pins it must name | Refusal text (image pins) |
|---|---|---|
| `aem_loaded = 0;` | store | "a store lands on aem_loaded's storage other than milan_init()'s one store of load_aem_image()'s return (the image stores in place from nvm_boot(), milan_init(); resolved: milan_init() stores <call:load_aem_image>, nvm_boot() stores 0)" |
| `aem_loaded = 1;` in the status handler | store | same pin, "from milan_init(), milan_status_handler()" |
| `&aem_loaded` taken, written through | address, escape, store | "the linked image forms the full address of aem_loaded's storage (the full address formed in a register (%lo on an addi) at 0x00012b88 in nvm_boot() (R_RISCV_LO12_I))"; store: "the image stores in place from milan_init(); resolved: ..., nvm_boot() stores 0" |
| `int aem_loaded;` | static, local | "aem_loaded is not a local object of the linked image" |
| a second unit declares it | second unit | "aem_loaded is named in a second translation unit (milan_verdict.c)" |
| splice, paste, macro writes (three) | store | "the image stores in place from nvm_boot(), milan_init(); resolved: ... nvm_boot() stores 1" |
| **new** `aem_loaded = 1;` under `#ifndef __PIE__` | store | "the image stores in place from nvm_boot(), milan_init(); resolved: milan_init() stores <call:load_aem_image>" (the resolver's PIC compile does not hold it) |
| macro-spelled address to `sscanf()` | address, escape | escape "(%lo on an addi) ... in nvm_boot()" |
| **new** `alias_sscanf` | one name, escape | "another symbol of the linked image is on aem_loaded's storage (milan_verdict_alias)"; escape "(%lo on an addi) at 0x00012b88 in nvm_boot()" |
| **new** `weakref_sscanf` | one name, escape | "... (milan_verdict_ref)"; escape as above |
| **new** address in a data word | address, escape | "the full address held in a data word at 0x000158c4 in .data (R_RISCV_32)" |
| **new** `auipc` with no relocation | AUIPC | "an AUIPC of the linked image carries no relocation (0x00012b84 in nvm_boot())" |

The round-2 gate accepted `alias_sscanf` and `weakref_sscanf`, per R413-2's own scripts at
`943a3dac` and `a033bfd8` (`receipts/gate1b-head/`). It would also have accepted the AUIPC break,
which no pin read. The data-word break was already refused there by the register-variable pin.

### Gate mutants of the image census (`probes/image_pin_mutants.py`, `receipts/image_pin_mutants_0a80abcb.log`)

On an export of `0a80abcb`, each mutant is run through the verdict controls:

| Mutant | Result | Killed by |
|---|---|---|
| M0 identity | passes (14/14) | |
| G0 `verdict_image_pins()` breaks nothing | KILLED | "accepted a second assignment inside nvm_boot()" |
| G1 one-name pin dropped | KILLED | `alias_sscanf` refused without naming one name |
| G2 escape pin dropped | KILLED | `&aem_loaded` break refused without naming escape |
| G3 locality dropped | KILLED | `int aem_loaded;` refused without naming local |
| G4 AUIPC pin dropped | KILLED | the `auipc` break accepted |
| G5 the image's in-place stores not read | KILLED | the `#ifndef __PIE__` write accepted |
| G6 the resolver's by-address stores not read | KILLED | `&aem_loaded` break refused without naming store |

### The reviewers' probes, rerun (`probes/rerun_reviewer_probes.py`, `receipts/gate1b-0a80abcb/`)

These are the reviewers' own scripts, unmodified, on fresh copies of an export of `0a80abcb`:
R413-2 `instrument_builder.py`, `plants.py` and `run_gate1b.py` (early stop); R412-2
`early_stop.py`, `plants2.py` and `run_gate1b.py`.

| Probe | At `0a80abcb` | Pins named |
|---|---|---|
| r413 `none` | ACCEPTED, `kept=['aem_loaded']` | |
| r413 `none`, forced forget | REFUSED on the verdict | (forget-on-call) |
| r413 `alias_sscanf` | REFUSED (was ACCEPTED at `a033bfd8`) | escape, one name |
| r413 `weakref_sscanf` | REFUSED (was ACCEPTED at `a033bfd8`) | escape, one name |
| r413 `asm_label_sscanf`, `inline_asm_la` | REFUSED | escape |
| r413 `alias_write` | REFUSED | store, one name |
| r413 `splice_write`, `paste_write`, `m_macro_set` | REFUSED | store |
| r413 `m_macro_addr` | REFUSED | store, escape, address |
| r413 `m_macro_addr_sscanf` | REFUSED | escape, address |
| r413 `plain_write` | REFUSED by the source rule "aem_loaded must contain only the image verifier's verdict" | |
| r413 `block_extern_sscanf` | REFUSED by the source rule "the address of aem_loaded must not be taken" | |
| r412 `plain_write` | REFUSED by the source rule (as r413) | |
| r412 `splice_write`, `paste_write`, `m_macro_set` | REFUSED | store |
| r412 `m_macro_addr` | REFUSED | store, address |
| r412 `m_macro_addr_sscanf` | REFUSED | escape, address |
| r412 `alias_write`, `static_alias_write` | REFUSED | store, one name |
| r412 `alias_addr`, `static_alias_addr` | REFUSED | escape, one name |
| r412 `alias_decl_only` | REFUSED | one name |

R413-2's `alias_escape_demo.c` and `weakref_escape_demo.c`, built with host `gcc -DHOST_MAIN`,
still print `entity_advertise(verified=1): ENABLE WRITTEN` (`receipts/escape_demos_host.log`).
That is the defect's semantics, which the gate now refuses on the firmware.

Toolchain checks (scratch, `/tmp`): `riscv64-elf-gcc -march=rv32i -mabi=ilp32` builds and links
the same image and gives the same references. `-march=rv32ic` sets the RVC flag, which the
census reads and refuses. The SDK defines `__PIE__` by default and not under `-no-pie`;
`riscv64-elf-gcc` defines neither, so there the `__PIE__` break is also a resolver store, and the
store pin names it either way. The gate's arm selections grade every conditional group both
ways, so a `__PIE__` arm elsewhere in the firmware is graded as its own firmware (no new issue).

## Item 2: R413-2 F2 and S1 (done, `a033bfd8`)

- `tb/verilator/fw_service_budget/run.py:534-547`: a fifth control in `armed_controls()`. A
  `milan_status` command starts at cycle 100,000,000, before the writer's arming at 104,472,844,
  with `uart_tx_allowance_ms=10.0`.
  - Ending 24,000,000 cycles after arming, its armed bound is 250 + 240 + 10 = 500 ms, and it is
    refused only on the PHY stretch (125 ms phase): `armed bound with a UART allowance refused
    its boundary`.
  - One cycle later, the tick stretch is refused too: `an unarmed-start command's UART allowance
    left its armed bound`.
- `tb/verilator/fw_service_budget/README.md:153,159-160`, `docs/findings/397_SERVICE_BUDGET.md:318`.
- PR body: round 2's item 2 says W6 is more lenient, and no control separated it because no
  armed-path row carried a UART allowance (the corrected W6 sentence).

### Grader mutants at `0a80abcb` (`check_mutants.py`, gate log)

| Mutant | Source | Result |
|---|---|---|
| W0 identity | R412-2 `grader_mutants.py` | passes (52 checks) |
| W1 old whole span | R412-2 | KILLED: "unarmed AEM prefix was charged as an armed gap" |
| W2 unarmed never charged | R412-2 | KILLED: "armed bound not recorded" |
| W3 first tick inside duty | R412-2 | KILLED: "an armed duty's leading gap escaped: arming was not the run's first opportunity" |
| W4 last tick | R412-2 | KILLED: same |
| W5 PHY whole span | R412-2 | KILLED: "unarmed AEM prefix was charged as an armed gap" |
| W6 armed bound without UART | R412-2 | KILLED: "an unarmed-start command's UART allowance left its armed bound" |
| X1, X2, X4, X5 | R412-2 `grader_mutants2.py` | KILLED |
| X3 arming from any event kind | R412-2 | passes: it only arms earlier, so it charges more |
| six rules | R413-2 `armed_mutants.py` | all KILLED |

`receipts/w6_direction_0a80abcb.log`: R413-2's `w6_direction.py` gives 505 ms at the head with
both findings, and 495 ms under W6 with the PHY finding only.

## Gates at `0a80abcb`

The receipt is `gates-0a80abcb.json`: each command with its rc, seconds, and the log's size and
sha256, plus the head and cleanliness after the run (`0a80abcb`, clean). The logs were written
under `/tmp/a457-gates/0a80abcb/`, and are copied to `receipts/gates-0a80abcb/` with the same
bytes (each is under 200 KB). Every gate ran at a clean tree, on the physical path, and was never
piped. The two builder banks ran one after the other, and the rest ran beside them.

| Gate | rc | s | Result (last lines of the log) |
|---|---|---|---|
| builder bank, RV32 compiler required (`--require-elaboration --require-rv32`) | 0 | 1019 | gate 1b "kept the slot of aem_loaded across a call under the verdict's pins, decided by address on the linked image of the census's -no-pie compile, where the firmware's 6 reference(s) to aem_loaded's storage are each the upper part or a load or store in place (...), accepted the AEM-first base only with it kept, and refused 14/14 planted pin breaks on the verdict, each naming its pins; a store through a literal address carries no relocation and is outside these pins". It ends "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11's calibration build tree, as in rounds 1 and 2. Log sha256 `df6abbc9...7df5` |
| builder bank, every cross-compiler candidate hidden (`full-builder-absent.py`) | 0 | 645 | "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 1b's compiled census, by design of that arm, and gate 11), then "FULL BUILDER ABSENT PASS: all three cross-compiler candidates hidden". Log sha256 `443ed395...bb5c` |
| `fw_service_budget/run.py --self-test` | 0 | 0.9 | flash 14 checks, 0 failures; oracle 52 checks, 0 failures |
| grader mutants (`check_mutants.py`) | 0 | 3.7 | "MUTANTS AS EXPECTED: W0 passes; W1-W6 killed (W3, W4 and W6 by name); X1, X2, X4, X5 killed and X3 passes as a stricter rule; all six R413 rules killed" |
| `scripts/check_nvm_capture.py` | 0 | 0.7 | "PASS: capture census, clocks, both timing arms and receipt agree" (all seven controls detected) |
| firmware digest (`check_firmware_digest.py`) | 0 | 0.1 | unchanged since `597dba85` and `943a3dac`, sha256 = capture receipt |
| `scripts/check_py_idiom.py` | 0 | 3.4 | every ratchet at or under its bound |
| `scripts/measure_test_evidence.py --check` | 0 | 5.7 | "TEST-EVIDENCE RATCHET: PASS" |
| `git diff --check 79c36963 HEAD` | 0 | 0.1 | empty |
| `scripts/docs_check.py` (pinned Markdown environment, as are the next five) | 0 | 4.4 | "0 finding(s) across 177 md files" |
| `scripts/check_doc_paths.py` | 0 | 0.1 | "OK (861 cited paths all resolve)" |
| `scripts/check_doc_style.py` | 0 | 0.0 | "OK (22 current documents)" |
| `scripts/check_archive.py` | 0 | 0.3 | "OK (21 historical page(s))" |
| `scripts/gen_toc.py --check` | 0 | 3.1 | "OK (119 page(s))" |
| `scripts/check_em_dash.py --base 79c36963` | 0 | 3.1 | "0 finding(s) over 521 added line(s) in 24 changed Markdown page(s)" |

## Firmware digest

`sw/firmware` has no difference from `597dba85` or `943a3dac`. `milan_baremetal.c` sha256 is
`a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`, equal to the capture
receipt's `product_firmware_sha256`.

## Packet

- `TAKEN.md`, `STOP.md` (both posted), `REVIEW-READY.md` (posted), `PR-BODY.md` (the Round 3
  section, the round-2 item-1 correction, and the corrected W6 sentence; not pushed).
- `probes/image_census_probe.py` (the prototype behind the STOP), `probes/instrument_verdict_controls_r3.py`,
  `probes/image_pin_mutants.py`, `probes/rerun_reviewer_probes.py`.
- `receipts/verdict_controls_0a80abcb.log`, `receipts/image_pin_mutants_0a80abcb.log`,
  `receipts/gate1b-0a80abcb/`, `receipts/escape_demos_host.log`, `receipts/w6_direction_0a80abcb.log`;
  from before the ruling: `receipts/image-census/`, `receipts/gate1b-head/`,
  `receipts/product_image_verdict_refs.txt`, `receipts/grader_mutants_a033bfd8.log`,
  `receipts/w6_direction.log`, `gates-a033bfd8.json`.
- `run_gates.py`, `check_mutants.py`, `check_firmware_digest.py`, `full-builder-absent.py`,
  `run_detached.sh`, `wait_for.py`, `gates-0a80abcb.json`, `receipts/gates-0a80abcb/`.
- `MANIFEST.sha256`: the sha256 of every file in the packet but itself.
- No push, no PR edit. Scratch trees under `/tmp` are exports of committed files, not checkouts.

## Open

- The literal-address limit, accepted by the ruling and stated at the rule, in
  `BAREMETAL_FIRMWARE.md` and in the CHANGELOG. The manager records it on #495.
