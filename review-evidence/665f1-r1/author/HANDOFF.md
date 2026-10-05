# HANDOFF: [A544] lane F1 for #665 (bare-metal saved-state handling)

Status: REVIEW READY at head `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e`, every gate in section 6 at that head.

- Branch: `665-f1-nvm` from dev `fa450d301805881ad713b67521477bf042ddadfd`, not pushed.
- Head: `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e`, eight one-line commits on the base:
  - `96c78891` the store: KLJ2 codec, boot restore and write-back behind a flash port and a state port;
  - `724c30f4` the two flash ports: LiteSPI command master and host flash model with faults;
  - `ccb239b6` the host suite: 26 checks per shape on both ports, power-cut sweep, recorded-vector round trip, 46 planted defects, RV32 arm;
  - `d3a2f133` the module page and the documentation index row;
  - `5f629d3e` a trailing blank line removed;
  - `0e4a4244` the step bound published as a store constant; the tie rule stated;
  - `448df784` the module page's count of checks run on both ports corrected;
  - `215c3c0b` the attempt limit and the step bound worded as the code enforces them.
- Assignment: #665 comment 5993775541 (lane F1). The session pointer named #658
  comment 5988328859, which is the #658 stage-1 lane; this lane follows 5993775541.
- Directive: #665 comment 5992455815 (bare-metal first: no OS, no heap, static pools).
- TAKEN: #665 comment 5993934000. REVIEW READY: #665 comment 5995604696.
- Reviewers named by the assignment: [R500] (internal), [R501] (external).

## 0. What landed

A new portable C11 module, `sw/firmware/ctrl_nvm/`, plus one row in
`docs/README.md`: 32 files, 4,751 lines added, none removed. Nothing else in
the tree changes:

- no RTL, no SoC, builder, register-map or configuration change;
- `sw/firmware/milan_baremetal/milan_baremetal.c` is byte-identical, so the
  capture receipt's firmware digest still holds;
- nothing links the module into any image. It sits behind the #665 build
  switch, whose default is the all-fabric build. That switch is F0's
  `--ctrl-mailbox`, which is on F0's lane and not merged.

| File | Lines | What it is |
|---|---:|---|
| `nvm_shape.h` | 139 | the record set and container sizes, from the generated `MILAN_NVM_*` constants |
| `nvm_klj2.h`, `nvm_klj2.c` | 493 | KLJ2 container and F07.8 record codec; the section 6.2 acceptance order |
| `nvm_flash.h`, `nvm_flash.c` | 72 | the flash port; its one blocking helper |
| `nvm_state.h` | 65 | the state port (apply, settle, rollback, latch, release) |
| `nvm_store.h`, `nvm_store.c` | 734 | the boot restore and the write-back |
| `plat/` | 237 | the LiteSPI flash port; the target's constants header |
| `host/` | 818 | the flash model with faults, the LiteSPI command-master model, the state model, stub headers |
| `test/` | 1,985 | the scenario runner (C), the checks, the mutants, the RV32 arm, the gate |
| `README.md` | 207 | the module page |

## 1. The flash port and its two implementations

`nvm_flash.h`: `read(addr, dst, len)`, `program(addr, src, len)` (1 to 256
bytes inside one page), `erase(addr)` (the 64 KiB block holding addr),
`busy()` (1 in progress, 0 done, negative fault) and `now_us()` (monotonic).
`program` and `erase` only START an operation. The store polls `busy` once per
service step and never spins on it in service. `nvm_flash_wait()` is the one
blocking helper, kept for the boot and console paths.

1. **`plat/nvm_flash_litespi.c`, on chip.** This is the shipping writer's access
   code (`nvm_spi_open/xfer/close`, `nvm_flash_status`, `nvm_flash_write_enable`,
   `nvm_flash_command`, `gettime_ns` in `milan_baremetal.c`) ported behind the
   port:
   - reads through the memory-mapped QSPI window;
   - WREN, PP, SE and RDSR through the LiteSPI CSR command master, one byte
     at a time, 1x mode;
   - time from the fabric PHC snapshot.

   Three changes from the shipping writer:
   - an erase or program only starts here;
   - program and erase are refused outside `MILAN_FLASH_JOURNAL_OFFSET` and
     `_SIZE`;
   - time never steps backwards: it holds the last value. A forward gPTP step
     can end a wait early; that attempt fails and is retried 1 s later, and
     nothing is lost.

   `nvm_flash_litespi_power_on()` clears the last-time static. The target's
   .bss clear does the same; the host suite calls it at every modelled power
   on.
2. **`host/nvm_fmodel.c`, the host flash model.** A 16 MiB NOR array: an erase
   sets a block to 0xFF, a program ANDs, and each holds `busy` for its model
   time. Each port call costs its 1x 12.5 MHz link time. Faults, each armed
   for `count` operations after `skip` of them:
   - a **power cut** inside media effect k (an erase or a page program),
     landing `frac`/256 of it, with the edge cells left half way by a
     fixed-seed pattern; after it every call fails;
   - erase hang, or erase that leaves a programmed byte;
   - program hang, drop or bit flip;
   - read fail, or read that returns one bit flipped;
   - bit flip at rest.

   The model also refuses and counts contract breaches, which every check
   asserts zero:
   - a program across a page;
   - a program or erase while busy;
   - any write outside the journal;
   - a write into the protected (authoritative) slot;
   - pages written in descending order.
3. **`host/litespi_model.c`.** The LiteSPI command master over the same flash
   model. The on-chip port runs on the host unchanged against stubs in
   `host/stubs/`. A chip-select window collects the bytes, and deselect
   executes WREN, PP or SE, as the N25Q128 does. RDSR answers from the model.
   It counts PP or SE without WREN, short commands, refusals and unknown
   commands; all are asserted zero.

**The seam with F0.** F0's HAL (`sw/firmware/ctrl/mbx/mbx_hal.h` on lane
`665-f0-mailbox`) is the mailbox's three-call bus port; this port is the
media's five-call port.

- They overlap in time only. When F0's time call lands, the LiteSPI port's
  `now_us` becomes a call to it.
- F0's event loop calls `nvm_store_service()` once per pass, and the protocol
  adapters (F3, F5) call `nvm_store_changed(group, index)`.
- F0 publishes `MILAN_FLASH_JOURNAL_*` and `MILAN_NVM_*` to the split image
  the same way `milan_soc.py` does for the shipping one; `plat/nvm_shape_gen.h`
  includes `generated/soc.h`.
- Nothing in F1 depends on F0's files.

## 2. The boot path and its format checks

`nvm_store_boot(flash, state)` runs before the event loop:

1. **Model check.** `state->model_ready()` is 0: **CLOSED**, cause MODEL. No
   apply, no release, no writer (D3 section 8.1 step 6, DR3b).
2. **Shape check.** `nvm_shape_consistent()` checks the run-time record walk
   against the compile-time sizes. If it fails: **DEFAULTS**, cause SHAPE,
   release, persistence disabled (DR3b).
3. **Both slots judged.** The section 6.2 order:
   - blank (40 header bytes 0xFF);
   - magic, major version, IMG_LEN 44 to 65,536, CRC-32 over [0, IMG_LEN-4);
   - entity id, model id (the shape binding), record layout;
   - every record: magic 0x1722, layout, length inside the area, crc16,
     ascending id, a shape id with the shape's payload length; or an ERASED
     span at the position of the next required record;
   - the area ends exactly at the trailer;
   - every required record present (VD_INCOMPLETE).

   The CRC is streamed through the stage, so a slot of any IMG_LEN is judged
   without a 64 KiB buffer. The walk is bounded by the loaded bytes; the
   argument for why a valid shape record never needs more is in
   `nvm_klj2.c`. A slot that does not deliver its bytes is VD_LEN (rule 4).
   The verdicts equal `scripts/nvm_klj2.py` `klj2_decode` on the shipping
   suite's whole refusal table plus three cases it lacks (check
   `verdict_parity`).
4. **Pick.** The newer accepted slot by `(int32_t)(A.seq - B.seq) >= 0`
   (section 7). The picked slot is read into the stage AGAIN and judged again
   in RAM, with `nvm_klj2_check()` and its own CRC test; only those bytes are
   applied. If that fails, the other slot is offered (cause STAGE). No slot:
   the stage gets the blank container (every record erased, the pad zero,
   sequence 0), terminal **BLANK**, and the verdict is named.
5. **The live and stage records.** The stage is the only container buffer. It
   holds the last verified container from boot on, and it is the prefill for
   every capture. The LIVE values are not copied: they stay with their owners,
   behind the state port, and the write path latches them when they are saved
   (the D3 "no shadow" rule).

   This replaces the shipping writer's two DDR3 buffers (`MILAN_NVM_LIVE_BASE`,
   the window the backend writes records into, and `MILAN_NVM_STAGE_BASE`, its
   private copy). Under the split, the owners are firmware, so no producer
   writes a record in place. #640 D4 removes DDR3, so one container-sized
   buffer is all the RAM the store keeps.
6. **The restore transaction** (D3 sections 8.3, 8.4, 8.6). Every record in
   ascending id:
   - an ERASED one applies nothing, and its default stands;
   - a framed one goes to `state->apply(group, index, payload)`: APPLIED,
     REFUSED (the value rule refuses; the default stands and the walk goes
     on), or FAULT (the rule cannot be judged), which aborts.

   These are the same writes the fabric owner makes today:
   - `KL_aecp_nvm_writer`'s W_APPLY: value plus valid flag on the state bus,
     after the SET program's rule;
   - the binding manager's preload;
   - a map record as one staged ADD;
   - names to the name table.

   `state->settle()` runs once, after the last map record and before the
   first name (section 8.4 step 4). #658's restore clip lands in that step
   (ruling 5988843004 item 3: a restored narrower format clips the identity
   default before AECP is released). It is cited, not depended on; the store
   calls the step either way.

   An abort calls `state->rollback()`, which puts every value back to its
   image default: **DEFAULTS**. A failing rollback is **CLOSED**. Otherwise
   the terminal is **COMPLETE**.
7. **Release.** `state->release()` runs once, at COMPLETE, BLANK or DEFAULTS,
   never at CLOSED. The writer is armed except at CLOSED.

After DEFAULTS the stage still holds the accepted slot's records. A later
commit writes them again beside the new change, as the fabric's window keeps
them after a D3 roll-back. DR1a still holds: DEFAULTS service is never
counted as reusable persistence.

## 3. The write path: atomicity rules and power-loss injection

`nvm_store_changed(group, index)` sets the record's dirty bit and starts the
first-dirty window if none is open. Each `nvm_store_service()` call is ONE
bounded step:

| Phase | Step |
|---|---|
| IDLE | dirty, the 1,000 ms first-dirty window elapsed (DR2a), not in backoff, not exhausted: start a capture |
| CAPTURE | the next dirty record: `state->latch()` into a payload buffer, compare with the staged bytes, copy, frame (crc16); dirty to in-flight |
| SEAL | if nothing changed and the stage is VERIFIED: skip, no erase (DR2b). Else the header at seq+1, then 256 B of CRC-32 per step, then the trailer |
| ERASE | erase the slot that is NOT authoritative (DR5: with none accepted, a blank slot before a refused one) |
| ERASE_WAIT | one status poll; 3,500 ms timeout: VD_ERASE |
| BLANKCHECK | 256 B read back per step, all 0xFF, or VD_ERASE |
| PROGRAM, PROGRAM_WAIT | one page, ascending (header page first, trailer last); 50 ms timeout: VD_PROGRAM |
| VERIFY | 256 B read back per step, equal to the stage, or VD_VERIFY; at the end the authority moves |

The rules, each with its check (section 5):

- **The authoritative slot is never erased or programmed** (`change_commit_bytes`,
  `powercut`, the `protected` invariant). The store refuses an erase target
  equal to the authority too, as defence in depth.
- **The trailer is the commit mark.** A slot is accepted only when its last
  page closes the CRC. The authority moves only on a verified read-back
  (`powercut`, `media_failures`).
- **Pages ascend** (the `descending` invariant).
- **DR2c.** A failure names its stage, returns in-flight records to dirty,
  sets `stale`, and retries after 1,000 ms, at most 3 attempts per unchanged
  work set. A new change opens a new work set. Success clears `stale` when
  nothing is dirty (`media_failures`, `recovers_after_failure`).
- **DR2b.** Only a proven-unchanged projection of a VERIFIED container is
  suppressed (`unchanged_no_erase`, `failed_commit_not_skipped`).
- **DR2a.** A first-dirty window, not a quiet-period timer (`debounce`).

**Power-loss injection.** For every shipped shape, both ports and three
starting points (blank media; one slot; two slots with the target holding an
older valid image), the power fails inside every media effect of one commit
(the erase and each page program) at 0, 1/256, 128/256 and 255/256 of it,
and once during the read-back. Each case then boots. It must restore the old
values, or the new ones only if the new container reached the media whole
(and strictly the new ones for the read-back cut), never a mix and never a
write into the authoritative slot. A further change must then commit and
boot back.

| Shape | Effects per commit | Cases per start | Starts x ports | Cases | Bad |
|---|---:|---:|---:|---:|---:|
| `endstation_arty_current` | 11 | 45 | 6 | 270 | 0 |
| `endstation_ax7101_1x1_tdm8` | 15 | 61 | 6 | 366 | 0 |
| `endstation_arty_4x4` | 20 | 81 | 6 | 486 | 0 |
| `endstation_arty_8ch` | 30 | 121 | 6 | 726 | 0 |
| `endstation_ax7101_8x8` | 53 | 213 | 6 | 1,278 | 0 |
| **Total** | | | | **3,126** | **0** |

Per run the outcome split is "old" for every cut but one or two, and "new"
for the read-back cut. A second "new" appears where the 255/256 cut of the
last page left the final trailer byte fully programmed. The container was
then whole, and booting it is correct. The full per-run table is in
`powercut_table.txt` beside this file.

**The capture bound.** The parent pins 24.5 ms at 8x8 for a capture that
copies all 13,210 record bytes in one hold (`check_nvm_capture.py`; receipt
maximum 13.86 ms at 50 MHz). Here a capture never holds the loop for more
than one record per step:

- the longest step touches `max(256, 2P + 6)` bytes, where P is the largest
  payload: 278 B at 1x1 and 1,158 B at 8x8, asserted exactly per shape by
  `service_bound`;
- at the receipt's measured 1.05 us per captured byte, that is about 1.2 ms
  at 8x8;
- that figure is DERIVED, not measured on the CPU harness. The harness
  measures the shipping writer, and this store is not in an image.

`service_bound` also proves:

- no call holds the loop past 1,000 us of link time (at most 169 us in the
  suite's runs);
- one status poll per call;
- the loop keeps running through a 3 s erase.

## 4. Static sizes

Derived from the shape at build time (`nvm_shape.h`) and measured on the
RV32I freestanding build, in bytes:

| Shape | Records | Container (IMG_LEN) | Stage | Payload buffer | Read-back chunk | Store state | Total bss | text |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `endstation_arty_current` | 42 | 2,516 | 2,524 | 66 | 256 | 256 | 3,112 | 10,348 |
| `endstation_ax7101_1x1_tdm8` | 54 | 3,336 | 3,344 | 136 | 256 | 256 | 4,000 | 10,364 |
| `endstation_arty_4x4` | 88 | 4,808 | 4,816 | 66 | 256 | 256 | 5,404 | 10,356 |
| `endstation_arty_8ch` | 120 | 7,368 | 7,376 | 66 | 256 | 256 | 7,964 | 10,356 |
| `endstation_ax7101_8x8` | 164 | 13,256 | 13,264 | 576 | 256 | 256 | 14,360 | 10,368 |

- **Stage** = `NVM_IMG_LEN + 8`. The 8 bytes are one record header of
  look-ahead, so the 6.2 walk over an over-long slot can read the header after
  the shape's last record.
- **Payload** = the shape's largest payload, `NVM_PAYLOAD_MAX`: the MCR 66 B,
  or the largest map record (17 x 8 at 1x1, 72 x 8 at 8x8).
- **Chunk** = one read-back step.
- **Store state** = the static struct: two 256-bit record bitmaps, the
  status, the cursors.
- data is 24 B; the record table is walked, never stored.

Against #640 D4 (no DDR3), the store's RAM is container-sized: 4.0 KB at the
shipping 1x1 shape, 14.4 KB at 8x8. That compares with the 64 KiB slot and
the 1 MiB DDR3 window the shipping writer uses.

## 5. Tests and their mutants

Gate: `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test`.

The runner (`test/nvm_test.c`) is a script interpreter over the store, the
models and either port. The checks run in Python against `scripts/nvm_klj2.py`
(reference encoder and decoder), the shipping suite's parity table
(`sw/firmware/nvm_hosttest/test_nvm_firmware.py parity_cases`) and the
recorded vectors (`tb/verilator/nvm_backend/records_*.txt`).

Every run is also held to a contract:

- no write outside the journal or into the authoritative slot;
- no page wrap, no write while busy, no descending page;
- step bytes at or under the bound;
- the state port called in order: ascending ids, formats and maps before
  settle, names after it, nothing after release, release once;
- no call over 1,000 us;
- on LiteSPI: every PP and SE after a WREN, no short or unknown command.

26 checks per shape, 24 of them on both ports (`read_flip_at_stage` on the
model only, because LiteSPI reads are memory-mapped; `port_guard` on LiteSPI
only).
46 planted defects; each names the checks that must fail on it, and every
check is named by at least one:

| Check | Ports | What it proves | Planted defects that must fail it |
|---|---|---|---|
| `blank_boot` | both | blank board: BLANK, AECP released once, nothing applied, stage = nvm_klj2's all-erased container | `no_blank_verdict`, `pad_not_zero`, `header_n_rec`, `no_blank_stage` |
| `golden_restore` | both | golden slot chosen, every record applied in the D3 order, state = klj2_decode's | `settle_after_names`, `release_before_apply` |
| `erased_records` | both | an erased record applies nothing; framed neighbours apply | `apply_erased` |
| `newer_wins` | both | newer slot wins, including across the sequence wrap | `pick_older`, `pick_no_wrap` |
| `torn_falls_back` | both | a torn newer slot falls back to the older one | `no_crc_check` |
| `both_torn_blank` | both | two torn slots: defaults, the failure named | `verdict_not_named` |
| `verdict_parity` | both | the verdict equals klj2_decode's for every 6.2 refusal (22 cases) | `no_crc_check`, `erased_header_only`, `no_ascending`, `overrun_as_rec`, `incomplete_accepted` |
| `wrong_version_falls_back` | both | major 1 and 3 refused VD_VER, the older slot offered | `no_version_check` |
| `read_flip_at_stage` | model | a bit the re-stage read flips is never applied; the other slot is | `stage_not_rechecked` |
| `apply_fault_rolls_back` | both | an unjudgeable value: DEFAULTS, every value at its default, released | `no_rollback`, `fault_as_refusal` |
| `settle_fault_rolls_back` | both | an unjudgeable settle step rolls back | `no_rollback`, `settle_fault_ignored` |
| `rollback_fault_closes` | both | a failing roll-back: CLOSED, never released, no writer | `rollback_failure_ignored`, `release_on_closed` |
| `model_unproven_closes` | both | no model: CLOSED, nothing applied | `model_ready_ignored` |
| `refused_keeps_default` | both | a refused value keeps its default and the walk goes on | `refusal_aborts` |
| `first_commit_bytes` | both | console commit on a blank board = nvm_klj2's container at seq 1; one erase, one program per page; LiteSPI WREN per PP/SE | `header_n_rec`, `descending_pages`, `litespi_no_wren`, `litespi_status_ignored` |
| `change_commit_bytes` | both | a change per group commits byte for byte at seq+1 to the other slot; the authority untouched; the boot reads it back | `frame_crc_init`, `same_sequence`, `erase_authoritative` |
| `debounce` | both | no erase before 1,000 ms; erase by 1,050 ms; a second change does not extend the window | `quiet_period`, `no_debounce` |
| `unchanged_no_erase` | both | DR2b: an unchanged value erases nothing | `no_dr2b` |
| `failed_commit_not_skipped` | both | DR2b never suppresses an unverified stage | `dr2b_ignores_durability`, `no_verify` |
| `media_failures` | both | erase hang and stuck, program hang, drop and flip: their verdict, 3 attempts 1,000 ms apart, then stop; authority untouched | `no_backoff`, `unbounded_attempts`, `no_blankcheck`, `no_verify`, `no_timeout` |
| `recovers_after_failure` | both | a third attempt that succeeds clears stale; after exhaustion a new change commits | `attempts_kept`, `stale_kept` |
| `refused_slot_kept` | both | DR5: a refused image is kept while a blank slot takes the commit | `refused_slot_overwritten` |
| `service_bound` | both | step bytes exactly `max(256, 2P + 6)`; calls at or under 1,000 us; loop alive through a 3 s erase | `capture_in_one_step`, `spin_wait` |
| `powercut` | both | the sweep of section 3 | `no_crc_anywhere`, `erase_authoritative` |
| `vector_round_trip` | both | the recorded vectors: IMG_LEN, CRC-32 and every offset equal; bytes equal nvm_klj2's; booted back | `frame_crc_init` |
| `port_guard` | LiteSPI | no program or erase outside the journal | `litespi_no_guard` |

Notes:

- `no_crc_check` removes the slot CRC test only. The power-cut sweep stays
  green on it, because the RAM re-check of step 2.4 has its own CRC test.
  `no_crc_anywhere` removes both, and `powercut` then fails with 46 of 61 bad
  cases at 1x1.
- The vectors: 1x1 at 3,336 B, CRC-32 0x6FEA9AD3, 54 records; 8x8 at
  13,256 B, 0x01F55611, 164 records. Both are reproduced byte for byte; the
  other three shapes have no recorded vector.
- RV32 arm: the codec, the store, the helper and the LiteSPI port compile
  with `riscv32-linux-gcc -march=rv32i -mabi=ilp32 -Os -ffreestanding -Wall
  -Wextra -Werror` against MMIO stand-ins (`test/rv32/`). The only undefined
  symbols are C-library memory functions and libgcc helpers: no heap, no
  stdio, no OS.

## 6. Gate table

Every gate below ran at the head `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e`
(base `fa450d30`), as a background job with its own log and rc file, none
piped. Two earlier rounds were the same: at `d3a2f133`, all rc 0 but
`git diff --check` (one trailing blank line, fixed by `5f629d3e`); at
`0e4a4244`, all rc 0. The last two commits change comments and the module
page only, and every gate was run again at the head regardless.

| Gate | Command | Result |
|---|---|---|
| this lane's host suite: every shape, both ports, RV32, 46 defects | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test` | rc 0, 103 s |
| shipping writer host suite | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | rc 0, 86 s |
| capture census and receipt | `python3 scripts/check_nvm_capture.py` | rc 0 |
| record space and its controls | `python3 scripts/check_nvm_record_space.py && ... --self-test` | rc 0, 52 s |
| builder bank (pinned Verilator 5.050 first on PATH) | `python3 sw/builder/test_builder.py --require-rv32` | rc 0, 1,198 s: "ALL GATES PASS EXCEPT 1 NOT RUN"; the arm not run is gate 11, which needs a local Vivado utilization report of the mf48 build tree that this host does not hold (environmental, the same verdict at `d3a2f133`) |
| C and C++ idiom | `scripts/check_cpp_idiom.py`, `--selftest` | rc 0, rc 0 |
| Python idiom | `scripts/check_py_idiom.py`, `--selftest` | rc 0, rc 0 |
| shell idiom | `scripts/check_sh_idiom.py`, `--selftest` | rc 0, rc 0 |
| hygiene | `scripts/check_hygiene.py --check`, `--selftest` | rc 0, rc 0 |
| TODO ownership | `scripts/check_todo_ownership.py`, `--selftest` | rc 0, rc 0 |
| test evidence | `scripts/measure_test_evidence.py --check`, `--selftest` | rc 0, rc 0 |
| bare-metal scope | `scripts/check_baremetal_only.py --check`, `--selftest` | rc 0, rc 0 |
| fail-fast, control flow, cohesion | `measure_fail_fast.py --check`, `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | rc 0 each |
| documentation wording and privacy | `scripts/docs_check.py` | rc 0 |
| em dash | `check_em_dash.py --base fa450d30` (208 added lines, 0 findings) and `--selftest`, pinned Markdown environment | rc 0, rc 0 |
| documentation style and maps | `check_doc_style.py` and `--selftest`; `check_gptp_docs.py`; `DOC_MAP.gen.py --check` and `--selftest`; `check_solution_docs.py`; `check_submodule_docs.py`; `check_feature_status.py --self-test`; `gen_module_matrix.py --check`; `check_doc_paths.py`; `check_archive.py` | rc 0 each |
| contents blocks | `gen_toc.py --selftest`, `--verify-anchors`, `--check` (pinned Markdown environment) | rc 0 each |
| CI event contract | `scripts/ci_events.py --check` | rc 0 |
| whitespace | `git diff --check fa450d30 HEAD` | rc 0 |

Not run, with reasons:

- `nvm_cosim`: nothing it reads changed. `git diff --stat fa450d30 HEAD` over
  `hdl`, `tb`, `sw/firmware/milan_baremetal`, `sw/firmware/nvm_hosttest`,
  `scripts`, `sw/litex`, `sw/builder`, `configs` and both processors is empty.
- `lint_rtl`, `xvlog_gate`, the RTL source lists and Yosys: no HDL changed.
- `act_ci`: there is no PR head; pushing is not allowed in this lane.

## 7. Findings outside the scope, for the manager

1. **Verdict parity gap in the SHIPPING writer.** For a framed record whose
   `payload_length` runs past the record area, `milan_baremetal.c`
   `nvm_validate` returns VD_REC (its `nvm_frame` folds the length test into
   the frame test), where `scripts/nvm_klj2.py` `klj2_decode` returns VD_LEN.
   I reproduced it on the shipping suite's own harness
   (`test_nvm_firmware.make_bench` at 1x1, the case from
   `nvm_checks.parity_extra`): "shipping writer VD_REC, klj2_decode VD_LEN".
   The shipping suite's parity table lacks the case, so its gate is green.
   The shipping image is out of scope here; it needs its own Issue, and the
   F1 store already answers VD_LEN.
2. **The #665 switch.** F1 links into no image until F0's default-off switch
   merges. The on-target capture time of section 3 is derived, not measured,
   until then.

## 8. Open questions and STOP conditions

No STOP: neither the format nor the atomicity rules needed an owner decision.
The store implements KLJ2 and section 7 as written, plus DR2a, DR2b, DR2c,
DR3b and DR5 as ruled. Two interpretations are stated publicly for the
reviewers:

- The shipping writer's two buffers (live window and private stage) become
  one stage plus the owners' live values, latched at capture (the D3 "no
  shadow" rule). That is what fits #640 D4's container-sized RAM. The
  capture then holds the loop one record per step, where the shipping one
  holds producers for the whole copy.
- DR2c's firmware attempts are counted per work set, and a new change opens
  a new one, so repeated changes against a failing medium keep retrying, each
  1,000 ms after the last failure. The shipping writer's rule is the same,
  read the same way.
