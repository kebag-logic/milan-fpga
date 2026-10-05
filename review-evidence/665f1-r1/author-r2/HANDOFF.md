# HANDOFF: [A544] lane F1 for #665 (bare-metal saved-state handling), round 2

Status: REVIEW READY at head `7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11`, every
gate in section 6 rc 0 at that head.

- Branch: `665-f1-nvm` from dev `fa450d301805881ad713b67521477bf042ddadfd`, not
  pushed. Dev moved to `510fae60b26bef1db138de5cf2ac72b17b5011a5` (PR #663,
  processor pin `ead80360`) during the round, so item 9 merged it with
  `--no-ff`. The merge touched no lane file; the submodule is at the new pin.
- Round-1 head `215c3c0be5d8db6d9a1ba5aca3827dfe969c042e` was reviewed
  NEGATIVE by R500-1 (PR #669 comment 5996001016) and R501-1 (PR #669 comment
  5995888263).
- Round-2 assignment: #665 comment 5996009284. Round-2 TAKEN: #665 comment
  5996281116. Round-2 REVIEW READY: #665 comment 5997533145.
- Round 2 adds three one-line commits on `215c3c0b`, no rebase, no amend:
  - `c1fb42a5` the code and the suite: timer0 time base, bounded LiteSPI
    waits, one-read slot judgment, the binding walk, DR2a and DR2c per
    captured work set, 37 checks and 69 planted defects;
  - `7725bcfa` the module page;
  - `7f8dc1b1` the `--no-ff` merge of dev `510fae60`.
- Dev's PR #663 amended both saved-state pages: maps become the parent's to
  restore and roll back on `restore_rb_o`, and processor issues 15 and 20 are done. None
  of the clauses this lane rests on changed: FASTCONNECT 9.2 and 9.4, D3
  6.3, 8.1, the bindings paragraph of 8.6, and the DR2a and DR2c rows.
  D3 8.1 step 8 still restores the names last, after the maps' re-judge.
- Round 1 (eight commits, `96c78891` to `215c3c0b`) is described in the
  round-1 REVIEW READY, #665 comment 5995604696.

## 0. What round 2 changed, finding by finding

| Finding | What was wrong | What changed | Check | Planted defect that fails it |
|---|---|---|---|---|
| Item 1: R500-1 F1, R501-1 F3 (time base) | Windows, backoff and media deadlines ran on the PHC, held on a backward step | The LiteSPI port owns LiteX `timer0`, free-running, accumulated to 64 bits; the PHC is never read. The store samples the time once per service step. The unused blocking helper `nvm_flash_wait` is removed | `time_base` (LiteSPI): PHC steps of -60 s and +60 s in the debounce window, the backoff, a hung erase and a hung program, plus a window across the counter's 42.9 s wrap, all graded on the model's own clock | `phc_time` (the round-1 PHC read restored), `clock_not_accumulated` |
| Item 2: R500-1 F2, R501-1 F2 (DR2c) | Every change call reset the budget; a success cleared the exhaustion; the console bypassed backoff and exhaustion | `nvm_store_changed` only marks records. The capture decides: a changed staged byte is a new work set, otherwise the same set continues. An exhausted unchanged set is never attempted again ("withheld"). The console is refused inside the backoff and does not override exhaustion. `abandoned` and `abandoned_vd` are kept until reset | `dr2c_unchanged_set`, `dr2c_console`, `media_failures`, `recovers_after_failure` | `budget_rearmed_by_change`, `budget_rearmed_by_capture`, `commit_now_overrides_exhaustion`, `commit_now_ignores_backoff`, `success_forgives_exhaustion` |
| Item 3: R501-1 F1 (boot validation) | The pick used a SEQ from a re-read after the CRC passed, unchecked; the published SEQ was not the applied container's | Each slot is read into RAM once and judged there: CRC, records and SEQ from the same bytes. The chosen slot's re-stage is judged again with its CRC, and its SEQ must equal the pick's. The published SEQ is the applied container's | `read_flip_boot` (R501-1's probe: bit 3 of byte 8 flipped on every boot read covering it, both slots, both orders, across the wrap: 24 runs); `read_alias_at_stage`; `read_fail_boot` | `select_on_unchecked_reread`, `stage_seq_unchecked`, `slot_read_fail_ignored` |
| Item 4: R501-1 F4 (bounded SPI) | `ls_open` and `ls_xfer` spun forever on a stalled master | Each wait gives up after 4,096 status reads without progress, releases chip select and fails the call. The store fails the attempt under the step's verdict. The controller model withholds TX or RX readiness, delayed or for good, or reports RX that never drains; it counts a firmware that spins past 1,000,000 reads as hung | `port_stall` (LiteSPI): slow by 4,000 reads a wait (completes), stalled TX in a page program and in a sector erase, stalled RX in a page program and a status poll, a stuck drain, a dead master | `xfer_unbounded`, `open_unbounded` (both caught by the hang counter), `stall_ignored` |
| Item 5: R500-1 F3 (DR2a) | A change taken by the running capture left the window armed | A change the running capture has yet to reach arms nothing; the window opens only for a change still waiting | `debounce` (a change taken mid-capture, then a change 5 s later; a change after the capture) | `capture_leaves_window_armed` |
| Item 6: R500-1 F4 (bindings) | Bindings were inside the D3 transaction and rolled back with it | D3 section 8.1 steps 4 and 5 and section 8.6 are explicit, so no STOP. The binding walk runs first as its own unit: a fault fails it whole (`rollback(NVM_W_BIND)`, nothing preloaded) and the D3 walk runs anyway; a failed undo is CLOSED. A D3 roll-back (`rollback(NVM_W_D3)`) leaves the bindings applied | `binding_walk`, `apply_fault_rolls_back`, `settle_fault_rolls_back` (bindings asserted still applied); the state model polices bindings-before-D3 in every run | `d3_rollback_takes_bindings`, `bindings_in_d3_walk`, `binding_fault_aborts_d3`, `binding_fault_keeps_preloads` |
| Item 7: R500-1 F5 (planted defects) | Five reviewer defects survived; read-fail never armed; the helper never called; the tie never exercised | One check and one planted defect per claim | `verify_tail`, `blankcheck_tail`, `media_verdicts`, `newer_wins` (tie), `time_base`, `read_fail_boot` | `verify_skips_last_stretch`, `blankcheck_first_stretch_only`, `blankcheck_read_fail_ignored`, `verify_read_fail_ignored`, `program_refusal_ignored`, `tie_picks_b`, `phc_time`, `slot_read_fail_ignored` |
| Item 8: R500-1 F6 (README bound) | The service-bound sentence read as a CPU bound | README "The service bound": bytes (asserted), model time (asserted, and what it charges), CPU time (DERIVED, with its assumptions and what it leaves out) | `service_bound` | `capture_in_one_step`, `spin_wait` |
| R500-1 S1 (suggestion) | The lane gate runs in no hosted workflow | Not wired here: it needs a workflow and CI-events change outside this lane. Recorded as an open risk for the manager (section 7) | | |

## 1. The flash port and its two implementations

`nvm_flash.h`: `read`, `program` (1 to 256 bytes inside one page), `erase`
(the 64 KiB block), `busy` (1 in progress, 0 done, negative fault) and
`now_us`. Every call returns in bounded time; `program` and `erase` only
start an operation and the store polls `busy` once per service step. `now_us`
is the contract item 1 turned on: elapsed microseconds from a LOCAL counter
that only counts up, never the PHC.

1. **`plat/nvm_flash_litespi.c`, on chip.** The shipping writer's access code
   behind the port: memory-mapped reads; WREN, PP, SE and RDSR through the
   LiteSPI CSR command master, one byte at a time. Changes from the shipping
   writer:
   - program and erase only start;
   - they are refused outside `MILAN_FLASH_JOURNAL_*`;
   - every wait on the master is bounded. `ls_ready` makes at most 4,096
     status reads, and the drain in `ls_open` at most 4,097. A failure
     releases chip select, and the call fails;
   - time is `timer0`: `nvm_flash_litespi_power_on()` sets load and reload
     to `0xffffffff` and enables it, and `ls_now_us` accumulates the 32-bit
     down-count difference into 64 bits, divided by
     `CONFIG_CLOCK_FREQUENCY / 1e6`.

   Obligations on the image that links it: call
   `nvm_flash_litespi_power_on()` once before `nvm_store_boot()`; nothing
   else reprograms `timer0`; the event loop calls `nvm_store_service()` at
   least once per 42.9 s. `timer0` is there to own: LiteX's `SoCCore` adds it
   by default (`with_timer=True`, `timer_uptime=False`) and
   `sw/litex/milan_soc.py` does not turn it off. A local ax7101 build's
   generated `csr.h` carries `CSR_TIMER0_*`, and its `soc.h` carries
   `CONFIG_CLOCK_FREQUENCY` 100000000. `milan_baremetal.c` does not touch
   `timer0`.
2. **`host/nvm_fmodel.c`.** A 16 MiB NOR array with a power cut inside any
   erase or page program, and these faults, each armed for `count`
   operations after `skip`:
   - erase hang, refusal, or a byte left programmed at a chosen offset;
   - program hang, refusal, drop or flip;
   - read fail, a flip in the middle byte, a flip of bit 3 of a chosen
     address, or an answer from the neighbouring block;
   - a flip at rest.

   Contract breaches are counted and asserted zero.
3. **`host/litespi_model.c`.** The command master, `timer0` (LiteX
   semantics: count down from load, reload at zero) and the PHC (an epoch
   plus model time plus every step) over the flash model. Every CSR access
   costs 40 ns of model time. The stalls withhold TX or RX readiness, or
   report RX that never drains, for a set number of reads per wait or for
   good. A wait still asked after 1,000,000 withheld reads is counted
   `hung` and released, so an unbounded firmware loop ends the run with a
   finding instead of hanging it.

**The seam with F0.** Unchanged in shape: F0's event loop calls
`nvm_store_service()` and `nvm_store_changed()`; nothing in F1 depends on
F0's files. One condition for the seam (R500-1's): whichever time call the
split image settles on keeps `now_us`'s contract, a local counter that only
counts up, never the PHC.

## 2. The boot path and its format checks

1. Model check: CLOSED, cause MODEL (D3 8.1 step 6, DR3b).
2. Shape check: DEFAULTS, cause SHAPE, persistence off (DR3b).
3. **Each slot judged on one read.** The 40 header bytes give IMG_LEN (rules
   1 to 3). A container that fits the stage (IMG_LEN + 8) is then read
   whole, once, and `nvm_klj2_check` judges those bytes: head, CRC-32,
   identity, records, the area's end and N_REC, in the section 6.2 order.
   The SEQ the pick uses is read from the same bytes. A longer container is
   never this shape's (the argument is in `nvm_klj2.c`): its CRC is
   streamed only so the refusal comes in the 6.2 order. Verdict parity with
   `klj2_decode` is unchanged: the shipping suite's 19-case refusal table
   plus three more.
4. **Pick and re-stage.** The newer by `(int32_t)(A.seq - B.seq) >= 0`; A on a
   tie, as the shipping writer picks (section 7 below has the conflict
   with FASTCONNECT section 7's pseudo-code). The pick is read into the stage again and
   judged again with `nvm_klj2_check`, its CRC included, and its SEQ must
   equal the pick's. If not, the other slot is offered (cause STAGE). The
   published SEQ is read from the staged bytes.
5. **The binding walk** (D3 8.1 step 4): every BINDING record, ascending,
   through `apply`. A FAULT fails the walk whole: `rollback(NVM_W_BIND)`
   drops what it preloaded, `bind_terminal` DEFAULTS, `bind_cause` APPLY, and
   the D3 walk runs. A failed undo ends CLOSED.
6. **The D3 walk** (8.6): every other record, ascending; settle after the
   maps and before the names (8.4). A FAULT or a settle fault calls
   `rollback(NVM_W_D3)`: every D3 value to its image default, the bindings
   untouched. The result is DEFAULTS, or CLOSED when the roll-back fails.
7. **Release** once at the D3 walk's COMPLETE or DEFAULTS, or BLANK; never at
   CLOSED.

## 3. The write path: atomicity rules and power-loss injection

The step table is the module page's ("Write-back"). Rules, each with its
check:

- **The authoritative slot is never erased or programmed**
  (`change_commit_bytes`, `powercut`, the `protected` invariant).
- **The trailer is the commit mark; the authority moves only on a read-back of
  the whole container** (`powercut`, `verify_tail`, `media_failures`).
- **The blank check covers the whole span** (`blankcheck_tail`).
- **Each failure is named by its step**, a refused program or erase and a read
  failure included (`media_verdicts`).
- **Pages ascend** (the `descending` invariant).
- **DR2a**: a first-dirty window that a change taken by the running capture
  does not open (`debounce`).
- **DR2b**: only a proven-unchanged projection of a verified container is
  suppressed (`unchanged_no_erase`, `failed_commit_not_skipped`).
- **DR2c**: three attempts per unchanged captured work set, each 1,000 ms after
  a failure, the console included. The exhaustion record survives later
  successes until reset (`dr2c_unchanged_set`, `dr2c_console`,
  `media_failures`, `recovers_after_failure`).
- **DR5**: a refused slot kept while a blank one takes the commit
  (`refused_slot_kept`).

**Power-loss injection**, unchanged in method:
- every shipped shape, both ports;
- three starts: blank media, one slot, two slots;
- a cut inside every media effect of one commit, at 0, 1/256, 128/256 and
  255/256 of it, and once during the read-back;
- after each cut, a boot, then a further change that must commit and boot
  back.

| Shape | Effects per commit | Cases per start | Starts x ports | Cases | Bad |
|---|---:|---:|---:|---:|---:|
| `endstation_arty_current` | 11 | 45 | 6 | 270 | 0 |
| `endstation_ax7101_1x1_tdm8` | 15 | 61 | 6 | 366 | 0 |
| `endstation_arty_4x4` | 20 | 81 | 6 | 486 | 0 |
| `endstation_arty_8ch` | 30 | 121 | 6 | 726 | 0 |
| `endstation_ax7101_8x8` | 53 | 213 | 6 | 1,278 | 0 |
| **Total** | | | | **3,126** | **0** |

The per-run split (old and new outcomes) is in `powercut_table.txt` beside
this file, regenerated at the round-2 head; it equals round 1's.

## 4. Static sizes

RV32I `-Os` freestanding: the codec, the store and the LiteSPI port, in
bytes. bss includes alignment.

| Shape | Records | Container | Stage | Payload | Chunk | Store state | Clock | bss | text |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `endstation_arty_current` | 42 | 2,516 | 2,524 | 66 | 256 | 280 | 12 | 3,144 | 10,981 |
| `endstation_ax7101_1x1_tdm8` | 54 | 3,336 | 3,344 | 136 | 256 | 280 | 12 | 4,032 | 10,997 |
| `endstation_arty_4x4` | 88 | 4,808 | 4,816 | 66 | 256 | 280 | 12 | 5,436 | 10,989 |
| `endstation_arty_8ch` | 120 | 7,368 | 7,376 | 66 | 256 | 280 | 12 | 7,996 | 10,989 |
| `endstation_ax7101_8x8` | 164 | 13,256 | 13,264 | 576 | 256 | 280 | 12 | 14,392 | 11,001 |

Against round 1:
- the store state grows by 24 B: this step's time, the walk and
  exhaustion fields;
- the clock is 12 B (`ls_ticks` and `ls_tick_last`), where round 1's
  `ls_last_us` was 8 B;
- text grows by about 630 B.

## 5. Tests and their planted defects

Gate: `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test`.

37 checks per shape:
- 29 on both ports;
- 5 on the flash model's port alone: `read_flip_at_stage`, `read_flip_boot`,
  `read_alias_at_stage`, `read_fail_boot` and `media_verdicts`. LiteSPI
  reads are memory-mapped, and its refusals are the guard's;
- 3 on LiteSPI alone: `time_base`, `port_stall` and `port_guard`.

69 planted defects, each naming the checks that must fail; every check is
named by at least one. The full table (check, ports, what it proves, the
defects that must fail it) is `mutant_table.md` beside this file, generated
from the suite's own docstrings and defect list.

Every run is also held to the contract:
- no write outside the journal or into the authoritative slot;
- no page wrap, no write while busy, no descending page;
- step bytes within the bound;
- the state port's order: bindings before the D3 walk, each ascending,
  settle between maps and names, nothing after release;
- no call over 1,000 us of model time;
- on LiteSPI: WREN before every PP and SE, no short or unknown command, no
  hung wait.

## 6. Gate table

Every gate ran at the merge head `7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11`
(dev `510fae60` merged), as a background or foreground job with its own log
and rc file, none piped. The same set ran at `7725bcfa` before dev moved; all
42 were rc 0 there too. The logs of the merge-head run are in
`logs/gates-7f8dc1b1/` beside this file.

| Gate | Command | Result |
|---|---|---|
| this lane's suite: every shape, both ports, RV32, 69 planted defects | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test` | rc 0, 146 s: "OK across 5 shape(s), 37 checks, and all 69 planted defects reddened" |
| shipping writer host suite | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | rc 0, 80 s |
| capture census and receipt | `python3 scripts/check_nvm_capture.py` | rc 0 |
| record space and its controls | `python3 scripts/check_nvm_record_space.py`, then `--self-test` | rc 0, rc 0 (48 s) |
| builder bank (Verilator 5.050 first on PATH) | `python3 sw/builder/test_builder.py --require-rv32` | rc 0, 1,274 s: "ALL GATES PASS EXCEPT 1 NOT RUN". The arm not run is gate 11, which reads a local Vivado utilization report of the mf48 build tree this host does not hold: environmental, the same verdict as round 1. Its "disabled-writer ... FAIL" lines are the planted control's, caught in both states, as in round 1 |
| C and C++ idiom | `scripts/check_cpp_idiom.py`, `--selftest` | rc 0, rc 0 |
| Python idiom | `scripts/check_py_idiom.py`, `--selftest` | rc 0, rc 0 |
| shell idiom | `scripts/check_sh_idiom.py`, `--selftest` | rc 0, rc 0 |
| hygiene | `scripts/check_hygiene.py --check`, `--selftest` | rc 0, rc 0 |
| TODO ownership | `scripts/check_todo_ownership.py`, `--selftest` | rc 0, rc 0 |
| test evidence | `scripts/measure_test_evidence.py --check`, `--selftest` | rc 0, rc 0 |
| bare-metal scope | `scripts/check_baremetal_only.py --check`, `--selftest` | rc 0, rc 0 |
| fail-fast, control flow, cohesion | `measure_fail_fast.py --check`, `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | rc 0 each |
| documentation wording and privacy | `scripts/docs_check.py` | rc 0 |
| em dash | `check_em_dash.py --base 510fae60` (316 added lines, 0 findings) and `--selftest`, pinned Markdown environment | rc 0, rc 0 |
| documentation style and maps | `check_doc_style.py` and `--selftest`; `check_gptp_docs.py`; `docs/DOC_MAP.gen.py --check` and `--selftest`; `check_solution_docs.py`; `check_submodule_docs.py`; `check_feature_status.py --self-test`; `docs/traceability/gen_module_matrix.py --check`; `check_doc_paths.py`; `check_archive.py` | rc 0 each |
| contents blocks | `gen_toc.py --selftest`, `--verify-anchors`, `--check` (pinned Markdown environment) | rc 0 each |
| CI event contract | `scripts/ci_events.py --check` | rc 0 |
| whitespace | `git diff --check 510fae60 HEAD` | rc 0 |

Not run, with reasons:

- `nvm_cosim`, `lint_rtl`, `xvlog_gate`, the RTL source lists and Yosys:
  this lane changes no HDL and nothing those gates read. The merge brought
  dev's own HDL and pin changes, which dev's hosted gates already cover.
- `act_ci`: there is no PR head; pushing is not allowed in this lane.

## 7. Findings outside the scope, for the manager

1. **Verdict parity gap in the SHIPPING writer** (unchanged from round 1): for
   a framed record whose `payload_length` runs past the record area,
   `milan_baremetal.c` `nvm_validate` answers VD_REC where `klj2_decode`
   answers VD_LEN. Both reviews carried it as a manager duty.
2. **The tie rule.** FASTCONNECT section 7's pseudo-code,
   `newer = (int32_t)(A.seq - B.seq) > 0`, offers B on equal sequences. The
   shipping writer (`nvm_pick_slot`, `>= 0`) and this store offer A. The
   writers never write equal sequences, but item 3 below shows one way they
   can meet. This store keeps the shipping writer's rule and now tests it
   (`newer_wins`, `tie_picks_b`); the page and the code disagree and need
   one decision.
3. **A transient refusal can strand a commit (new, needs its own Issue).**
   Take a board where slot A holds a valid container at SEQ s > 1 and slot
   B is blank, and a read fault refuses A at boot. With no slot accepted,
   the store (like the shipping writer) writes the next commit at SEQ 1 to
   the blank slot B (DR5). On the next clean boot A (s) is newer than B
   (1), so the committed change is not restored although it was reported
   durable. Choosing the sequence after a refusal is a design decision, for
   example from a refused slot's readable header. It is not this lane's
   item.
4. **The lane gate is not in hosted CI** (R500-1 S1). Wiring
   `test_ctrl_nvm.py` into a workflow needs a workflow and `ci_events.py`
   contract change outside this lane; until then the gate is local only,
   while the shared scripts it imports can change under it.

## 8. Readings stated publicly, and STOP conditions

No STOP. The three readings, each also in the module page and the TAKEN:

- **Bindings (item 6).** D3 section 8.1 steps 4 and 5 and section 8.6 ("What
  it does not touch") are explicit: the binding walk is its own unit and a
  D3 roll-back leaves it applied. The state port's `rollback()` takes the
  walk it undoes. The one addition the pages do not spell out: a binding
  walk whose undo fails ends CLOSED, as a failed D3 roll-back does, because
  the listener's state can no longer be proven.
- **The exhaustion record (item 2).** FASTCONNECT 9.2 and D3 6.3 rule that
  firmware transaction exhaustion has no reset-sticky alarm of its own (the
  DR2c-carrier ruling names only the producers' `nvm_alarm`, and adds no
  status bit), and that a later successful commit clears `nvm_stale`. So the
  record the assignment names is this store's status: `abandoned` and
  `abandoned_vd`, never cleared by a success, only by reset. `stale` keeps
  the section 9.2 recovery rule.
- **Two buffers to one** (round 1, unchanged): the shipping writer's live
  window and private stage become one stage plus the owners' live values,
  latched at capture.
