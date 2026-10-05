# HANDOFF: [A544] lane F1 for #665 (bare-metal saved-state handling), round 4

Status: REVIEW READY at head `d763fce6f3e48fa9c468aaa835653befb8382d06`,
with every gate in section 6 at rc 0 at that head. Round-4 REVIEW READY: #665
comment 6000120843.

- Branch: `665-f1-nvm` from dev `fa450d301805881ad713b67521477bf042ddadfd`.
  It is not pushed.
- Live dev moved twice during the lane, and not in round 4:
  - to `510fae60` (PR #663, processor pin `ead80360`), merged in round 2 as
    `7f8dc1b1`;
  - to `28f9666feab2b2ba287643c63ed3a16b1e0bb863` (PR #666, one findings
    page), merged in round 3 with `--no-ff` as `e2000ef9`. Live dev was
    still `28f9666f` when round 4 finished, so item 3 had nothing to merge.
- Round-3 head `9412006b` was reviewed NEGATIVE, one MAJOR each:
  - R500-3: PR #669 comment 5999342108;
  - R501-3: PR #669 comment 5999339293.
- Round-4 assignment: #665 comment 5999350068. Round-4 TAKEN: #665 comment
  5999489236.
- Round 4 adds three commits on `9412006b`, one-line subjects, no rebase, no
  amend:
  - `f1cf5c08`: the code and the suite, both findings;
  - `c2e33963`: the module page;
  - `d763fce6`: the module page states that a slot which never reads cleanly
    holds the writer on every boot (R500-3 S1, its first half). A gate run
    started at `c2e33963` was stopped for this commit; section 6 is the run
    at `d763fce6`.
- Rounds 1 to 3 are described in their REVIEW READY comments, #665
  5995604696, 5997533145 and 5999002886.

## 0. What round 4 changed, finding by finding

| Item / finding | What was wrong at `9412006b` | What changed | Check | Planted defects that fail it |
|---|---|---|---|---|
| Item 1; R501-3 F1 (MAJOR) | `nvm_slot_check` let a refusal stand when two reads gave the same verdict, whatever bytes they returned. One byte read XOR 8, then XOR 16, gave two `VD_CRC` refusals (body) or two `VD_MAGIC` refusals (header) of different bytes. So the valid slot was refused, the change committed SEQ 1 into the blank slot, and a clean boot lost saved values: 32 of 32 of R501-3's cases | Each boot read keeps a CRC-32 digest of every byte the port delivered for it, with their count (`nvm_take`). A verdict other than OK stands only when an earlier read of the slot has the same verdict, count and digest (`nvm_agrees`). A read with other bytes than every earlier one is a media fault, counted in `read_faults`, and the slot is read again within `NVM_READ_TRIES` = 3, so a clean read is judged and stands as OK. No two reads agree: UNREAD, and the writer HELD (decision 2) | `read_disagreement`, new, on the flash model's port at every shape. The valid slot is A or B, the other blank, at SEQ 1, 5, 0x80000000 and 0xFFFFFFFF. The fault is at its first header byte or at body offset 0x100, read XOR 8 then XOR 16 then clean (the clean read is applied, one media fault counted). Or XOR 8, 16 and 32 (UNREAD, HELD, two media faults counted). That is 32 cases per shape, each followed through a change, a clean reboot, a commit and a clean reboot, with every saved value compared. The new host fault is `read-vary-at` | `refusal_by_verdict` (new: agreement reduced to verdict equality), `refusal_unconfirmed`, `unread_not_held` |
| Item 2; R500-3 F1 (MAJOR) | The port converted `timer0` clocks with an integer `CONFIG_CLOCK_FREQUENCY / 1000000` behind a static assertion, so it did not compile at the Arty shapes' 83,333,000 Hz. Both clock stand-ins fixed 100 MHz, so the suite reported those shapes OK | Exact conversion at any clock in hertz: whole seconds, then the remainder times 10^6, in 64 bits. The deadline in clocks is `nvm_flash_litespi_call_ticks` = `LS_CALL_US * CONFIG_CLOCK_FREQUENCY / 10^6`, also in 64 bits: 166,666 at 83.333 MHz and 200,000 at 100 MHz. `ls_late()` compares with it. The static assertion is gone, and so are both stand-ins (`host/stubs/generated/soc.h`, `test/rv32/generated/soc.h`). The bench writes each shape's `generated/soc.h` from its config's `sys_clk_hz` and holds that to the builder's `soc_params.json` argv (`--sys-clk-freq 83.333e6`, or `milan_soc.py`'s 100 MHz default when none is given). The model's `timer0` counts at that clock, and the RV32 arm builds against it | `port_clock`, new, on LiteSPI: the runner's clock equals the config's, the deadline equals 2,000 us of it in clocks, and over 120 s (two wraps or more) the port's elapsed time matches the model's to 2 us. `time_base` puts its window across the wrap at the shape's own wrap time (51.5 s at 83.333 MHz) and asserts that the window holds it | `ticks_per_us_truncated` (new, graded at `endstation_arty_current`): deadline 166,000 clocks for 166,666; 120,481,469 us counted over 120,000,023 us; `time_base` windows close at 997 ms |
| Item 3 | | Live dev did not move | | |
| R500-3 R1 (residue) | "a ready master costs one timer read" held in the model only | The reviewer's exact wording, in the paragraph item 2 changes | | |
| R500-3 S1 (suggestion) | The module page said "until reset", not "on every boot while the slot never reads cleanly" | Boot item 9 states it. The narrower hold is an owner decision and is not taken | | |

Not changed, and why:
- R500-3 S2 (HELD with changes shows `dirty=1`, `stale=0`): how HELD maps onto
  FASTCONNECT 9.2's flags belongs to integration (F0/F5).
- R500-1 S1 (the lane gate in no hosted workflow): carried, section 7.

Both reviewers' probes, re-run at the round-4 code (copies under scratch,
since the packets are read-only):
- R500-3 `probe_arty_clock.sh`, after its `gen_shape_header.py` for
  `endstation_arty_current`: rc 0 at 100,000,000 and at 83,333,000.
- R501-3 `probe_read_agreement.py --jobs 2`: rc 0. 16 cases each at 1x1 and
  8x8, 0 losing a saved value; every case `unread=0`, one media fault
  counted, the commit verified. 16 single-corruption controls each, and the
  permanent read failure live.

## 1. The flash port and its two implementations

`nvm_flash.h` defines five calls: `read`, `program` (1 to 256 bytes inside
one page), `erase` (the 64 KiB block), `busy` (1 in progress, 0 done,
negative fault) and `now_us`. Every call returns in bounded time, and so does
every call as a whole. A failing `read` is a media fault, never a verdict.
`program` and `erase` only start an operation; the store polls `busy` once
per service step. `now_us` is a LOCAL counter that only counts up, never the
PHC.

1. **`plat/nvm_flash_litespi.c`, on chip.** The shipping writer's access code
   behind the port: memory-mapped reads, and WREN, PP, SE and RDSR through the
   LiteSPI CSR command master, one byte at a time. Changes from the shipping
   writer:
   - program and erase only start;
   - they are refused outside `MILAN_FLASH_JOURNAL_*`;
   - per wait: `ls_ready` makes at most 4,096 status reads, and the drain in
     `ls_open` at most 4,097;
   - per call: `ls_call_begin()` reads `timer0` when `program`, `erase` or
     `busy` begins. `ls_late()` reads it again every 64 status reads that
     find the master not ready, counted over the whole call. It fails a call
     still waiting once more than `nvm_flash_litespi_call_ticks` clocks have
     passed. That is 2,000 us at the shape's clock: 166,666 clocks at
     83.333 MHz, 200,000 at 100 MHz (round 4). A failure releases chip
     select, and the call fails;
   - time is `timer0`: `nvm_flash_litespi_power_on()` sets load and reload
     to `0xffffffff` and enables it. `ls_now_us` accumulates the 32-bit
     down-count difference into 64 bits. Round 4 converts it exactly at any
     clock in hertz, whole seconds and then the remainder times 10^6.

   Obligations on the image that links it:
   - call `nvm_flash_litespi_power_on()` once before `nvm_store_boot()`;
   - nothing else reprograms `timer0`;
   - the event loop calls `nvm_store_service()` at least once per 2^32
     system clocks: 42.9 s at 100 MHz (AX7101 shapes), 51.5 s at 83.333 MHz
     (Arty shapes).
2. **`host/nvm_fmodel.c`.** A 16 MiB NOR array with a power cut inside any
   erase or page program, and these faults, each armed for `count`
   operations after `skip`:
   - erase hang, refusal, or a byte left programmed;
   - program hang, refusal, drop or flip;
   - read fail, or a read fail only on reads covering a chosen address;
   - read flips: in the middle byte, or bit 3 of a chosen address;
   - new in round 4, `read-vary-at`: the byte at a chosen address read wrong
     a different way each time, XOR 8, then 16, then 32;
   - an answer from the neighbouring block;
   - a flip at rest.
3. **`host/litespi_model.c`.** The command master, `timer0` and the PHC over
   the flash model. Each CSR access costs 40 ns of model time. Round 4:
   `timer0` counts at the shape's `CONFIG_CLOCK_FREQUENCY`, converted
   exactly from model nanoseconds. Stalls withhold TX or RX readiness, or
   report RX that never drains, for a set number of reads per wait or for
   good. A firmware still spinning after 1,000,000 withheld reads is counted
   `hung` and released.

**The seam with F0**, unchanged: F0's event loop calls `nvm_store_service()`
and `nvm_store_changed()`. Whichever time call the split image settles on
must keep `now_us`'s contract.

## 2. The boot path and its format checks

1. Shape check: when the record walk and the build disagree, nothing is
   walked and persistence is off. The result is DEFAULTS, cause SHAPE (DR3b),
   or CLOSED when the model is unproven too.
2. **Each slot judged on one read**: the 40 header bytes give IMG_LEN, then
   one read of the whole container is judged in RAM by the section 6.2 order.
   Verdict parity with `klj2_decode`: the shipping suite's 19-case table plus
   three more.
3. **The read bound**, round 4's agreement rule: at most 3 reads per slot.
   OK stands on one read, because its CRC-32 covers the SEQ. Any other
   verdict, BLANK included, stands only when two reads return the same bytes.
   "The same bytes" means the same verdict, the same byte count and the same
   CRC-32 digest over every byte the port delivered for the read. That is
   the 40 header bytes for a header verdict (blank, magic, version, length),
   and the header plus the whole container otherwise, streamed for a
   container longer than the stage. A read with other bytes than every
   earlier one, and a read the port fails, are media faults, counted in
   `read_faults`. A slot with no standing verdict within the bound is UNREAD
   (`VD_LEN`, its `unread` bit set).
4. **Pick and re-stage**, unchanged. The newer slot wins by
   `(int32_t)(A.seq - B.seq) >= 0`, A on a tie (decision 1). The pick is
   read into the stage again and judged again with its CRC, and its SEQ must
   equal the pick's. A failed re-stage is tried again, 3 re-stages in all. A
   slot that never re-stages as judged is UNREAD, and the other slot is
   offered (cause STAGE). The published SEQ is read from the staged bytes.
5. **The binding walk** (D3 8.1 steps 4 and 5), unchanged.
6. **The model check** (step 6), unchanged: an unproven model ends CLOSED,
   cause MODEL, with the bindings kept and nothing released.
7. **The D3 walk** (8.6), unchanged.
8. **Release** once at the D3 walk's COMPLETE or DEFAULTS, or at BLANK; never
   at CLOSED.
9. **HELD**: any UNREAD slot puts the write path in `NVM_P_HELD` until
   reset, reported through `phase`, `unread`, and `dirty` for the changes it
   keeps. A slot that never reads cleanly holds the writer on every boot.

## 3. The write path: atomicity rules and power-loss injection

The rules and their checks from rounds 2 and 3 stand. Round 4 adds no write
rule. `read_disagreement` follows each case through a commit and two clean
reboots, as `authority_unknown` does.

Power-loss injection is unchanged in method:
- every shipped shape, both ports, each shape at its own clock;
- three starts: blank media, one slot, two slots;
- a cut inside every media effect of one commit, at 0, 1/256, 128/256 and
  255/256 of it, and once during the read-back;
- after each cut, a boot, then a further change that must commit and boot
  back.

The per-run table is `powercut_table.txt` beside this file, regenerated at
the round-4 head (section 6).

## 4. Static sizes

RV32I `-Os` freestanding: the codec, the store and the LiteSPI port, in
bytes, each shape built at its own clock. bss includes alignment.

| Shape | Clock (Hz) | Records | Container | Stage | Payload | Chunk | Store state | Clock counters | bss | text |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `endstation_arty_current` | 83,333,000 | 42 | 2,516 | 2,524 | 66 | 256 | 288 | 20 | 3,160 | 12,352 |
| `endstation_ax7101_1x1_tdm8` | 100,000,000 | 54 | 3,336 | 3,344 | 136 | 256 | 288 | 20 | 4,048 | 12,368 |
| `endstation_arty_4x4` | 83,333,000 | 88 | 4,808 | 4,816 | 66 | 256 | 288 | 20 | 5,452 | 12,360 |
| `endstation_arty_8ch` | 83,333,000 | 120 | 7,368 | 7,376 | 66 | 256 | 288 | 20 | 8,012 | 12,360 |
| `endstation_ax7101_8x8` | 100,000,000 | 164 | 13,256 | 13,264 | 576 | 256 | 288 | 20 | 14,408 | 12,372 |

Against round 3:
- bss is unchanged;
- text grows by about 595 B: the digest, and the 64-bit conversion;
- while a slot is judged, the stack holds a 36-byte array: three words per
  read, for its verdict, digest and count.

## 5. Tests and their planted defects

Gate: `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test`.

Each shape is built and graded at its own clock. The suite prints the clock
per shape, and its RV32 lines say `rv32 at 83333000 Hz` for the Arty shapes.

42 checks per shape:
- 29 run on both ports;
- 8 run on the flash model's port alone: `read_flip_at_stage`,
  `read_flip_boot`, `read_alias_at_stage`, `read_fail_boot`,
  `fallback_restage`, `media_verdicts`, `authority_unknown` and, new,
  `read_disagreement`;
- 5 run on LiteSPI alone: `time_base`, `port_stall`, `port_deadline`,
  `port_guard` and, new, `port_clock`.

There are 82 planted defects: round 3's 80 and 2 new ones,
`refusal_by_verdict` and `ticks_per_us_truncated`. Each names the checks that
must fail. Every check is named by at least one defect. All are graded at
`endstation_ax7101_1x1_tdm8`, except `ticks_per_us_truncated`, which is
graded at `endstation_arty_current`: at 100 MHz a whole number of clocks per
us is exact, and the defect would be graded at a clock where it does
nothing. `mutant_table.md` beside this file lists each check with its ports,
what it proves and the defects that must fail it. It is generated from the
suite's own docstrings and defect list.

Seams moved by round 4's code, with the defect itself kept:
- `slot_read_fail_ignored` and `select_on_unchecked_reread` (the reads now go
  through `nvm_take`);
- `refusal_unconfirmed` and `blank_unconfirmed` (the standing test is now
  `nvm_agrees`);
- `clock_not_accumulated`, `phc_time` and `call_deadline_ignored` (the new
  conversion and the published deadline).

Every run is also held to the contract, unchanged: journal only, never the
authoritative slot, no page wrap, no write while busy, ascending pages, the
step bound, the state port's order, WREN before every PP and SE on LiteSPI,
no hung wait, 250 us per call with no stall armed and 2,213 us with one.

## 6. Gate table

Every gate ran at `d763fce6f3e48fa9c468aaa835653befb8382d06` as a
background job with its own log and rc file, none piped. Logs, host paths
redacted: `logs/gates-d763fce6/` beside this file.

| Gate | Command | Result |
|---|---|---|
| this lane's suite: every shape at its own clock, both ports, RV32, 82 planted defects | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test` | rc 0, 184 s: "OK across 5 shape(s), 42 checks, and all 82 planted defects reddened"; `clock=83333000 Hz` on the three Arty shapes |
| shipping writer host suite | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | rc 0, 81 s |
| capture census and receipt | `python3 scripts/check_nvm_capture.py` | rc 0 |
| record space and its controls | `python3 scripts/check_nvm_record_space.py`, then `--self-test` | rc 0, rc 0 (48 s) |
| builder bank (Verilator 5.050 first on PATH) | `python3 sw/builder/test_builder.py --require-rv32` | rc 0, 1,261 s: "ALL GATES PASS EXCEPT 1 NOT RUN". The arm not run is gate 11, which reads a local Vivado utilization report of the mf48 build tree that this host does not hold. It is environmental, the same verdict as rounds 1 to 3. Its two "disabled-writer ... FAIL" lines are the planted control's, as in rounds 2 and 3 |
| C and C++ idiom | `scripts/check_cpp_idiom.py`, `--selftest` | rc 0, rc 0 |
| Python idiom | `scripts/check_py_idiom.py`, `--selftest` | rc 0, rc 0 |
| shell idiom | `scripts/check_sh_idiom.py`, `--selftest` | rc 0, rc 0 |
| hygiene | `scripts/check_hygiene.py --check`, `--selftest` | rc 0, rc 0 |
| TODO ownership | `scripts/check_todo_ownership.py`, `--selftest` | rc 0, rc 0 |
| test evidence | `scripts/measure_test_evidence.py --check`, `--selftest` | rc 0, rc 0 |
| bare-metal scope | `scripts/check_baremetal_only.py --check`, `--selftest` | rc 0, rc 0 |
| fail-fast, control flow, cohesion | `measure_fail_fast.py --check`, `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | rc 0 each |
| documentation wording and privacy | `scripts/docs_check.py` | rc 0 |
| em dash | `check_em_dash.py --base 28f9666f` (468 added lines in 3 pages, 0 findings) and `--selftest`, pinned Markdown environment | rc 0, rc 0 |
| documentation style and maps | `check_doc_style.py` and `--selftest`; `check_gptp_docs.py`; `docs/DOC_MAP.gen.py --check` and `--selftest`; `check_solution_docs.py`; `check_submodule_docs.py`; `check_feature_status.py --self-test`; `docs/traceability/gen_module_matrix.py --check`; `check_doc_paths.py`; `check_archive.py` | rc 0 each |
| contents blocks | `gen_toc.py --selftest`, `--verify-anchors`, `--check` (pinned Markdown environment) | rc 0 each |
| CI event contract | `scripts/ci_events.py --check` | rc 0 |
| whitespace | `git diff --check 28f9666f HEAD` | rc 0 |

Also at this head:
- the power-cut table (`powercut_table.txt`): 3,126 cases, 0 bad, identical
  to rounds 2 and 3;
- R500-3's master-table probe (`logs/probes-d763fce6/mt.*.log`), at 1x1,
  8x8, `endstation_arty_current` and `endstation_arty_4x4`. Every row of
  the module page's table reproduces exactly at 1x1, 8x8 and
  `endstation_arty_current` (83.333 MHz). At `endstation_arty_4x4` four rows
  are 1 us higher (540, 860, 1,860 and 2,190 us), as at round 3; the table
  is scoped to 1x1 and 8x8. The worst call is 2,189 us (2,190 us at 4x4),
  within 2,213;
- both reviewers' probes, section 0 (`logs/probes-d763fce6/`).

After the builder bank, the checkout held its ignored outputs
(`configs/generated/*.hex`, `sw/builder/out/`) and bytecode caches. They
were removed, so the tree is clean.

Not run, with reasons:

- `nvm_cosim`, `lint_rtl`, `xvlog_gate`, the RTL source lists and Yosys:
  this lane changes no HDL and nothing those gates read.
- `act_ci`: there is no PR head for this round, because pushing is not
  allowed in this lane.

## 7. Findings outside the scope, for the manager

1. **Verdict parity gap in the SHIPPING writer**, unchanged from round 1: for
   a framed record whose `payload_length` runs past the record area,
   `milan_baremetal.c` `nvm_validate` answers VD_REC where `klj2_decode`
   answers VD_LEN.
2. **The shipping writer's generation restart** is #671. This store no
   longer has it, for a failed read (round 3) or for differing reads
   (round 4).
3. **The lane gate is not in hosted CI** (R500-1 S1, retained by R500-3 and
   R501-3).
4. **A read fault that repeats itself exactly**, a stated limit (README "What
   this does not prove"): two reads with the same wrong bytes are taken as
   content. New in round 4, also stated: two different reads whose CRC-32
   digests collide. That cannot happen for reads differing in one or two
   bits or within 32 consecutive bits; for any other difference, the
   probability is about 2^-32.
5. **R500-3 S1, the narrower hold**: the hold could be limited to the case
   where no slot is authoritative. That is a change to decision 2, so it is
   the owner's call, and round 4 does not take it.
6. **R500-3 S2**: how HELD with changes outstanding maps onto FASTCONNECT
   9.2's `nvm_backed`/`nvm_stale` is integration work (F0/F5).

## 8. Readings stated publicly, and STOP conditions

There is no STOP. The readings below are in the round-4 TAKEN and the module
page.

- **"The same bytes" is a digest.** The assignment allows a full comparison
  or a digest of the whole container. A full comparison would need a second
  container-sized buffer, or chunked compare reads that change the boot's
  read pattern. The digest covers every byte the port delivered for the
  read, which is every byte the verdict was judged on. A header verdict is
  judged on the 40 header bytes; any other verdict is judged on the header
  and the whole container.
- **The deadline in clocks is published** (`nvm_flash_litespi_call_ticks`),
  so the suite can hold it to the config's clock. It is the very value
  `ls_late()` compares with.
- **The clock comes from the config**, `board.constraints.sys_clk_hz`, as
  the assignment says. It is also held to what the builder hands
  `milan_soc.py`, so the two cannot drift apart unseen.
- Rounds 2 and 3 readings stand: the binding walk is its own unit (D3 8.1,
  8.6); the exhaustion record is the store's status (FASTCONNECT 9.2, D3
  6.3); one stage replaces the shipping writer's two buffers; the retry is
  bounded at boot; the per-call deadline caps a port call on `timer0`.
