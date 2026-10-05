# HANDOFF: [A544] lane F1 for #665 (bare-metal saved-state handling), round 3

Status: REVIEW READY at head `9412006bd58c002835bb06d46045c53098cc59a5`,
with every gate in section 6 at rc 0 at that head. Round-3 REVIEW READY: #665
comment 5999002886.

- Branch: `665-f1-nvm` from dev `fa450d301805881ad713b67521477bf042ddadfd`.
  It is not pushed.
- Live dev moved twice during the lane:
  - to `510fae60` (PR #663, processor pin `ead80360`), merged in round 2 as
    `7f8dc1b1`;
  - to `28f9666feab2b2ba287643c63ed3a16b1e0bb863` (PR #666, one findings
    page, `docs/findings/653_DISCONNECT_ORDER_BENCH.md`), merged in round 3
    with `--no-ff` as `e2000ef9`. That merge touches no lane file and no
    submodule.
- Round-2 head `7f8dc1b1` was reviewed NEGATIVE:
  - R500-2: PR #669 comment 5997904664;
  - R501-2: PR #669 comment 5997910948.
- Round-3 assignment and decisions: #665 comment 5997929153. Round-3 TAKEN:
  #665 comment 5998087724.
- Round 3 adds five commits on `7f8dc1b1`, one-line subjects, no rebase, no
  amend:
  - `da35570a`: the code and the suite;
  - `ce78be4a`: the FASTCONNECT section 7 tie edit (decision 1);
  - `716d3213`: the module page;
  - `e2000ef9`: the `--no-ff` merge of dev `28f9666f`;
  - `9412006b`: the cumulative call bound corrected from 2,171 us to
    2,213 us, with the twelve-slowed-waits case that shows why. A gate run
    at `e2000ef9` passed everything finished; the builder bank there was
    stopped for this commit. Section 6 is the run at `9412006b`.
- Rounds 1 and 2 are described in their REVIEW READY comments, #665
  5995604696 and 5997533145.

## 0. What round 3 changed, finding by finding

| Item / finding | What was wrong at `7f8dc1b1` | What changed | Check | Planted defects that fail it |
|---|---|---|---|---|
| Item 1, decision 2; R501-2 F1 (MAJOR) | A boot read fault refused the slot like bad content. With slot A valid at SEQ s and B blank, the next commit wrote SEQ 1 to B, and a clean boot preferred A | A slot's verdict stands on at most 3 reads (`NVM_READ_TRIES`). OK stands on one read; any other verdict, BLANK included, only when two reads agree. A failed read is a media fault. A slot with no standing verdict, or that never re-stages as judged, is UNREAD: `VD_LEN`, a bit in the new status field `unread`, and no SEQ taken from it. Any UNREAD slot puts the writer in the new phase HELD until reset: changes are marked and reported dirty, nothing is erased or written, and the console is refused | `authority_unknown`. It runs both orientations at SEQ 1, 5, 0x80000000 and 0xFFFFFFFF, under four faults: 3 failed reads (held), 2 failed reads, an unreported flip, and an aliased read that makes the valid slot read blank. Each case continues through a clean reboot, a change, a verified commit and another clean reboot, with the restored payload compared every time. Also `read_fail_boot` (two failed reads then a good one applied; three held), `read_flip_at_stage`, `read_alias_at_stage` and `fallback_restage` | `unread_not_held` (the generation restart), `read_not_retried`, `refusal_unconfirmed`, `blank_unconfirmed`, `restage_not_retried` |
| Item 2, decision 1; R501-2 F3 | The page's pseudo-code said `> 0`, which offers B on a tie | FASTCONNECT section 7 now reads `>= 0 ? A : B` and cites the decision. The code was already `>= 0` | `newer_wins`: ties at 7 and at 0xFFFFFFFF, with distinct payloads in the two slots | `tie_picks_b` |
| Item 3; R501-2 F2, R500-2 F2 | Only each wait was bounded, so a slow master could hold one page program for 41,970 us of model time. The stated CPU figure did not follow from its inputs, and the PR body said "at most 210 us measured" | A LiteSPI call still waiting on the master after `LS_CALL_US` = 2,000 us of `timer0` time now fails. The check runs every 64 not-ready status reads, counted over the whole call. The README separates three things. First, nominal calls: asserted under 250 us, measured at 168 us on the model port and 210 us on LiteSPI. Second, the cumulative bound: asserted under 2,213 us, as the sum of four terms, with a table of eight measured master cases. Third, CPU time. The derived capture figure is a floor and is compared with nothing | `port_deadline`: ten slowed waits complete in 1,859 us. Twelve slowed waits end just before the deadline, and the call finishes past it in 2,189 us. With every wait slowed, each program fails at the deadline (2,009 us) and three attempts are spent. The contract asserts 250 us for every run with no stall and 2,213 us for every run with one | `call_deadline_ignored` (41,970 us), `deadline_per_wait` (43,306 us) |
| Item 4; R500-2 F1 | The model check returned CLOSED before the binding walk | Order of D3 section 8.1: slots, binding walk (steps 4 and 5), model check (step 6), D3 walk. An unproven model ends CLOSED with the bindings kept. The shape check stays first and touches no slot | `model_unproven_closes`: bindings applied, `bind_terminal` COMPLETE, CLOSED, nothing released; blank and unproven is CLOSED | `bindings_skipped_unproven`, `model_ready_ignored` |
| Item 4; R500-2 F3 | No check failed for the fallback's re-stage judgement, nor for the DR2a boundary record | New check `fallback_restage`, where both slots' re-stages flip every time; `debounce` adds a change to the record the capture examines next | `fallback_restage`, `debounce` | `fallback_restage_unchecked`, `taken_off_by_one` |
| Item 4; R500-2 F4 | A DR2b suppression left `stale` set with nothing un-durable | `nvm_heal()` runs at a verified commit and at a DR2b suppression | `recovers_after_failure`: a failed attempt, then the same value set again while the retry writes, then DR2b; it ends with `stale` 0 | `dr2b_keeps_stale` |
| R500-2 S1 (suggestion) | A failed fallback re-stage kept `VD_OK` | The fallback loop marks every slot that fails its re-stage `VD_LEN` and UNREAD | `fallback_restage` | as above |
| Item 5 | Dev moved to `28f9666f` | `--no-ff` merge `e2000ef9` | | |

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
   - per call (round 3): `ls_call_begin()` reads `timer0` when `program`,
     `erase` or `busy` begins. `ls_late()` reads it again every 64 status
     reads that find the master not ready, counted over the whole call, and
     fails a call still waiting once 2,000 us have passed. A call whose
     master stops being slow just before then finishes at the ready pace. A
     failure releases chip select, and the call fails;
   - time is `timer0`: `nvm_flash_litespi_power_on()` sets load and reload
     to `0xffffffff` and enables it. `ls_now_us` accumulates the 32-bit
     down-count difference into 64 bits, divided by
     `CONFIG_CLOCK_FREQUENCY / 1e6`.

   Obligations on the image that links it, unchanged:
   - call `nvm_flash_litespi_power_on()` once before `nvm_store_boot()`;
   - nothing else reprograms `timer0`;
   - the event loop calls `nvm_store_service()` at least once per 42.9 s.
2. **`host/nvm_fmodel.c`.** A 16 MiB NOR array with a power cut inside any
   erase or page program, and these faults, each armed for `count`
   operations after `skip`:
   - erase hang, refusal, or a byte left programmed;
   - program hang, refusal, drop or flip;
   - read fail, and new in round 3, a read fail only on reads covering a
     chosen address (a bad region);
   - read flips: in the middle byte, or bit 3 of a chosen address;
   - an answer from the neighbouring block;
   - a flip at rest.
3. **`host/litespi_model.c`.** The command master, `timer0` and the PHC over
   the flash model. Each CSR access costs 40 ns of model time. Stalls
   withhold TX or RX readiness, or report RX that never drains, for a set
   number of reads per wait or for good. A firmware still spinning after
   1,000,000 withheld reads is counted `hung` and released.

**The seam with F0**, unchanged: F0's event loop calls `nvm_store_service()`
and `nvm_store_changed()`. Whichever time call the split image settles on
must keep `now_us`'s contract.

## 2. The boot path and its format checks

1. Shape check: when the record walk and the build disagree, nothing is
   walked and persistence is off. The result is DEFAULTS, cause SHAPE (DR3b),
   or CLOSED when the model is unproven too.
2. **Each slot judged on one read** (round 2, unchanged): the 40 header bytes
   give IMG_LEN, then one read of the whole container is judged in RAM by the
   section 6.2 order. Verdict parity with `klj2_decode`: the shipping suite's
   19-case table plus three more.
3. **The read bound** (round 3, decision 2): at most 3 reads per slot. OK
   stands on one read, because its CRC-32 covers the SEQ. Any other verdict,
   BLANK included, stands only when two reads agree. A read the port fails is
   a media fault and counts in `read_faults`. A slot with no standing verdict
   within the bound is UNREAD (`VD_LEN`, its `unread` bit set).
4. **Pick and re-stage.** The newer slot wins by `(int32_t)(A.seq - B.seq) >= 0`,
   A on a tie (decision 1). The pick is read into the stage again and judged
   again with its CRC, and its SEQ must equal the pick's. A failed re-stage is
   tried again, 3 re-stages in all. A slot that never re-stages as judged is
   UNREAD, and the other slot is offered and re-staged the same way (cause
   STAGE). The published SEQ is read from the staged bytes.
5. **The binding walk** (D3 8.1 steps 4 and 5), unchanged from round 2: a
   fault fails it whole through `rollback(NVM_W_BIND)`; a failed undo is
   CLOSED.
6. **The model check** (step 6), moved here in round 3: an unproven model
   ends CLOSED, cause MODEL, with the bindings kept and nothing released. On
   blank media too.
7. **The D3 walk** (8.6), unchanged: a fault or a settle fault calls
   `rollback(NVM_W_D3)`, giving DEFAULTS, or CLOSED when the roll-back fails.
8. **Release** once at the D3 walk's COMPLETE or DEFAULTS, or at BLANK; never
   at CLOSED.
9. **HELD** (round 3): any UNREAD slot puts the write path in `NVM_P_HELD`
   until reset. This is reported through `phase`, `unread`, and `dirty` for
   the changes it keeps.

## 3. The write path: atomicity rules and power-loss injection

The rules and their checks from round 2 stand, with these round-3 additions:

- **No commit while the authority is unknown** (`authority_unknown`,
  `fallback_restage`, `read_fail_boot`, `read_flip_at_stage`,
  `read_alias_at_stage`).
- **DR2a at the boundary**: a change to the record the running capture
  examines next is that capture's, and opens no window (`debounce`).
- **`stale` heals on DR2b too**, once nothing changed is left outside a
  verified slot (`recovers_after_failure`).

Power-loss injection is unchanged in method:
- every shipped shape, both ports;
- three starts: blank media, one slot, two slots;
- a cut inside every media effect of one commit, at 0, 1/256, 128/256 and
  255/256 of it, and once during the read-back;
- after each cut, a boot, then a further change that must commit and boot
  back.

The per-run table is `powercut_table.txt` beside this file, regenerated at
the round-3 head (section 6).

## 4. Static sizes

RV32I `-Os` freestanding: the codec, the store and the LiteSPI port, in
bytes. bss includes alignment.

| Shape | Records | Container | Stage | Payload | Chunk | Store state | Clock | bss | text |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `endstation_arty_current` | 42 | 2,516 | 2,524 | 66 | 256 | 288 | 20 | 3,160 | 11,757 |
| `endstation_ax7101_1x1_tdm8` | 54 | 3,336 | 3,344 | 136 | 256 | 288 | 20 | 4,048 | 11,773 |
| `endstation_arty_4x4` | 88 | 4,808 | 4,816 | 66 | 256 | 288 | 20 | 5,452 | 11,765 |
| `endstation_arty_8ch` | 120 | 7,368 | 7,376 | 66 | 256 | 288 | 20 | 8,012 | 11,765 |
| `endstation_ax7101_8x8` | 164 | 13,256 | 13,264 | 576 | 256 | 288 | 20 | 14,408 | 11,777 |

Against round 2:
- the store state grows by 8 B (`unread`, `read_faults`);
- the clock grows by 8 B (`ls_call_start`, `ls_waited`);
- text grows by about 780 B.

## 5. Tests and their planted defects

Gate: `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test`.

40 checks per shape:
- 29 run on both ports;
- 7 run on the flash model's port alone: `read_flip_at_stage`,
  `read_flip_boot`, `read_alias_at_stage`, `read_fail_boot`,
  `fallback_restage`, `media_verdicts` and `authority_unknown`;
- 4 run on LiteSPI alone: `time_base`, `port_stall`, `port_deadline` and
  `port_guard`.

There are 80 planted defects: round 2's 69 and 11 new ones. Each names the
checks that must fail, and every check is named by at least one.
`mutant_table.md` beside this file lists each check with its ports, what it
proves and the defects that must fail it. It is generated from the suite's
own docstrings and defect list.

Every run is also held to the contract:
- no write outside the journal or into the authoritative slot;
- no page wrap, no write while busy, and no descending page;
- step bytes within the bound;
- the state port's order;
- on LiteSPI: WREN before every PP and SE, no short or unknown command, and
  no hung wait;
- new in round 3: no call over 250 us of model time with no stall armed, and
  none over 2,213 us with one. The 2,213 us is the sum of the deadline
  (2,000), one check interval (3), a page program's accesses at the ready
  pace (42) and its link time, which the model charges at chip-select
  release (168).

The longest calls the gate prints per shape at this head are 210 us with no
stall armed. With a stall they are 2,189 us, or 2,190 us at
`endstation_arty_4x4`: the twelve-slowed-waits case.

## 6. Gate table

Every gate ran at `9412006bd58c002835bb06d46045c53098cc59a5` as a
background job with its own log and rc file, none piped. Logs:
`logs/gates-9412006b/` beside this file.

| Gate | Command | Result |
|---|---|---|
| this lane's suite: every shape, both ports, RV32, 80 planted defects | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test` | rc 0, 175 s: "OK across 5 shape(s), 40 checks, and all 80 planted defects reddened" |
| shipping writer host suite | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | rc 0, 79 s |
| capture census and receipt | `python3 scripts/check_nvm_capture.py` | rc 0 |
| record space and its controls | `python3 scripts/check_nvm_record_space.py`, then `--self-test` | rc 0, rc 0 (46 s) |
| builder bank (Verilator 5.050 first on PATH) | `python3 sw/builder/test_builder.py --require-rv32` | rc 0, 1,339 s: "ALL GATES PASS EXCEPT 1 NOT RUN". The arm not run is gate 11, which reads a local Vivado utilization report of the mf48 build tree that this host does not hold. It is environmental, the same verdict as rounds 1 and 2. Its two "disabled-writer ... FAIL" lines are the planted control's, as in round 2 |
| C and C++ idiom | `scripts/check_cpp_idiom.py`, `--selftest` | rc 0, rc 0 |
| Python idiom | `scripts/check_py_idiom.py`, `--selftest` | rc 0, rc 0 |
| shell idiom | `scripts/check_sh_idiom.py`, `--selftest` | rc 0, rc 0 |
| hygiene | `scripts/check_hygiene.py --check`, `--selftest` | rc 0, rc 0 |
| TODO ownership | `scripts/check_todo_ownership.py`, `--selftest` | rc 0, rc 0 |
| test evidence | `scripts/measure_test_evidence.py --check`, `--selftest` | rc 0, rc 0 |
| bare-metal scope | `scripts/check_baremetal_only.py --check`, `--selftest` | rc 0, rc 0 |
| fail-fast, control flow, cohesion | `measure_fail_fast.py --check`, `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | rc 0 each |
| documentation wording and privacy | `scripts/docs_check.py` | rc 0 |
| em dash | `check_em_dash.py --base 28f9666f` (415 added lines in 3 pages, 0 findings) and `--selftest`, pinned Markdown environment | rc 0, rc 0 |
| documentation style and maps | `check_doc_style.py` and `--selftest`; `check_gptp_docs.py`; `docs/DOC_MAP.gen.py --check` and `--selftest`; `check_solution_docs.py`; `check_submodule_docs.py`; `check_feature_status.py --self-test`; `docs/traceability/gen_module_matrix.py --check`; `check_doc_paths.py`; `check_archive.py` | rc 0 each |
| contents blocks | `gen_toc.py --selftest`, `--verify-anchors`, `--check` (pinned Markdown environment) | rc 0 each |
| CI event contract | `scripts/ci_events.py --check` | rc 0 |
| whitespace | `git diff --check 28f9666f HEAD` | rc 0 |

The power-cut table (`powercut_table.txt`) was regenerated at this head:
3,126 cases, 0 bad, identical to round 2's.

Not run, with reasons:

- `nvm_cosim`, `lint_rtl`, `xvlog_gate`, the RTL source lists and Yosys:
  this lane changes no HDL and nothing those gates read. The dev merges
  brought dev's own changes, which dev's hosted gates cover.
- `act_ci`: there is no PR head, because pushing is not allowed in this
  lane.

## 7. Findings outside the scope, for the manager

1. **Verdict parity gap in the SHIPPING writer**, unchanged from round 1: for
   a framed record whose `payload_length` runs past the record area,
   `milan_baremetal.c` `nvm_validate` answers VD_REC where `klj2_decode`
   answers VD_LEN.
2. **The shipping writer's generation restart** is #671 (decision 2). This
   store no longer has it.
3. **The lane gate is not in hosted CI** (R500-1 S1, retained by R500-2).
4. **A read fault that repeats itself exactly** (a stated limit, README "What
   this does not prove"). Take a fault that corrupts a valid slot the same
   way on every boot read, without the port reporting it. Two agreeing reads
   then refuse that slot as content, and the generation can restart below it.
   No reading of the bytes can tell that from a really corrupt slot, and
   decision 2 takes no generation from unvalidated bytes.

## 8. Readings stated publicly, and STOP conditions

There is no STOP. The readings below are in the round-3 TAKEN and the module
page.

- **Two disagreeing reads are a media fault.** Decision 2 separates a media
  read fault from "a content refusal of cleanly read bytes". The store can
  only call bytes cleanly read when the port reports no error and a second
  read agrees. BLANK needs the same confirmation as a refusal: a misread
  blank slot lets the next commit restart the sequence below a container
  that survives, just as a misread refusal does. `authority_unknown` drives
  both cases, an unreported flip and an aliased read.
- **The retry is bounded at boot.** A slot still UNREAD after 3 reads holds
  the writer until the next reset, whose boot reads it again. The store does
  not re-read in service.
- **The per-call deadline** answers item 3 with the alternative R500-2 F2
  offered: the port caps the call, so the stated figure holds. It is
  enforced on `timer0`, which is real time on chip, so the port call's bound
  does not depend on a CSR access cost. The store's own CPU work per step is
  still derived, as a floor.
- Round-2 readings stand: the binding walk is its own unit (D3 8.1, 8.6);
  the exhaustion record is the store's status (FASTCONNECT 9.2, D3 6.3); one
  stage replaces the shipping writer's two buffers.
