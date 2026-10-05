[A544]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at the lane head (round 4):

- 42 checks per shipped shape (5 shapes), each shape built and graded at its
  own system clock: the three Arty shapes at 83,333,000 Hz and the two AX7101
  shapes at 100 MHz. Of the 42, 29 run on both flash ports, 8 on the flash
  model's port alone and 5 on the LiteSPI port alone;
- 3,126 power-cut cases, 0 bad;
- 82 of 82 planted defects caught;
- the RV32I freestanding build is clean at every shape's clock;
- every gate the change touches is at rc 0.

`665-f1-nvm` -> `dev`.

## Linked Issue / roles

Relates to #665: lane F1, assignment comment 5993775541, with rounds 2, 3
and 4 in comments 5996009284, 5997929153 and 5999350068. The issue stays
open for F0 and F2 to F5.

Executor: `[A544]`
Internal cleared-context reviewer: `[R500]`
External reviewer: `[R501]`

## Description

This PR adds the bare-metal saved-state store of the Mark II split: a new
portable C11 module, `sw/firmware/ctrl_nvm/`, with no OS and no heap. Every
buffer is a static array sized from the entity shape at build time. Nothing
links it into an image yet: it sits behind the #665 build switch, whose
default is the all-fabric build. The shipping writer
`sw/firmware/milan_baremetal/milan_baremetal.c` is byte-identical. No RTL,
SoC, builder, register-map or configuration file changes. One authoritative
page changes: `docs/design/SAVED_STATE_FASTCONNECT.md` section 7, the tie
rule of decision 1.

| Piece | Files | What it does |
|---|---|---|
| shape | `nvm_shape.h` | the record set and container sizes, from the generated `MILAN_NVM_*` constants the shipping writer compiles against |
| codec | `nvm_klj2.c` | KLJ2 container and F07.8 record codec, the section 6.2 acceptance order with the erased-record rule; verdicts equal `scripts/nvm_klj2.py` |
| flash port | `nvm_flash.h`, `plat/nvm_flash_litespi.c`, `host/nvm_fmodel.c` | Read, program, erase, busy and time, with every wait bounded and every call bounded. The on-chip port is the shipping writer's LiteSPI access code, and it refuses writes outside the journal. A wait gives up after 4,096 status reads without progress. A call still waiting after 2,000 us of `timer0` time fails: 166,666 clocks at 83.333 MHz, 200,000 at 100 MHz. Time is `timer0`, a local counter, never the PHC. Its clocks become microseconds exactly at any clock in hertz. The host model injects power cuts inside any erase or page program, media, refusal and read faults, bit flips, and a byte read wrong a different way each time |
| state port | `nvm_state.h` | apply (judged by the SET rule), settle (formats against maps, where #658's restore clip lands), rollback of one walk, latch, release |
| boot | `nvm_store.c` | Each slot is judged on one read, so CRC, records and SEQ are the same bytes. A verdict stands on at most 3 reads. OK stands on one; any other verdict only when two reads return the same bytes: the same verdict, byte count and CRC-32 digest over every byte the port delivered. A slot that gives neither is UNREAD. The newer slot is re-staged and re-judged, with its SEQ equal to the pick's. Then the binding walk; then the model check, where an unproven model is CLOSED with the bindings kept; then the D3 walk as one transaction. AECP is released only at COMPLETE, BLANK or DEFAULTS. An UNREAD slot holds the writer until reset |
| write-back | `nvm_store.c` | the 1,000 ms first-dirty window (a change the running capture takes opens none); a capture that latches one record per step; the seal; erase, blank check, ascending page program and read-back of the slot that is not authoritative; DR2c per captured work set, the console included, with a reset-sticky exhaustion record; DR2b suppression, which also heals `stale`; DR5 slot choice |
| host suite | `test/` | 42 checks per shape against `scripts/nvm_klj2.py`, the shipping suite's parity table and the recorded vectors `tb/verilator/nvm_backend/records_*.txt`. Each shape is built at its config's `sys_clk_hz`. Also the power-cut sweep; PHC steps and the counter's wrap at each shape's clock; a stalling and a slowed command master; reads that disagree; 82 planted defects; the RV32 arm |

**Round 4** answers R500-3 and R501-3, both NEGATIVE at `9412006b` with one
MAJOR each, under #665 comment 5999350068:

| Item | Finding | Change | Planted defects that now fail |
|---|---|---|---|
| 1 | R501-3 F1 (MAJOR): two reads with the same refusal code were taken as agreeing, whatever bytes they returned. A byte read XOR 8, then XOR 16, refused a valid slot, and the next commit lost saved values on a clean boot: 32 of 32 probe cases | Each boot read keeps a CRC-32 digest of every byte the port delivered, with their count. A refusal or a blank verdict stands only when two reads have the same verdict, count and digest. Differing bytes are a media fault, counted, and the slot is read again within the 3-read bound, so the clean read is applied. If no two reads agree, the slot is UNREAD and the writer HELD (decision 2). The new check `read_disagreement` keeps R501-3's probe. It covers both orientations, SEQ 1, 5, 0x80000000 and 0xFFFFFFFF, and a header byte and a body byte. XOR 8, then XOR 16, then clean: the clean read is applied. XOR 8, 16, then 32: the writer is held. Every case goes through a change, a clean reboot, a commit and a clean reboot, and every saved value is compared each time | `refusal_by_verdict` (new: verdict equality only), `refusal_unconfirmed`, `unread_not_held` |
| 2 | R500-3 F1 (MAJOR): the LiteSPI port's integer ticks-per-us and static assertion did not compile at the Arty shapes' 83,333,000 Hz, and the suite's 100 MHz stand-ins reported those shapes OK | Exact 64-bit conversion; the deadline in clocks computed in 64 bits and published (`nvm_flash_litespi_call_ticks`, 166,666 at 83.333 MHz); the assertion and both stand-ins removed. The suite writes each shape's `generated/soc.h` from its config's `sys_clk_hz`, held to the builder's `--sys-clk-freq`. The model's `timer0` and the RV32 arm use that clock. The new check `port_clock` compares the clock, the deadline in clocks, and the port's elapsed time against the model's over 120 s. `time_base` crosses the wrap at each shape's own wrap time | `ticks_per_us_truncated` (new, graded at `endstation_arty_current`) |
| 3 | merge dev if it moved | dev did not move | |
| | R500-3 R1 (residue) and S1 (its first half) | the module page takes R1's exact wording, and states that a slot which never reads cleanly holds the writer on every boot | |

**Static RAM**: the stage is the container plus 8 bytes. With the largest
payload, one 256-byte read-back chunk, 288 bytes of state and the 20-byte
clock and deadline, bss is 4,048 B at the shipping 1x1 TDM8 and 14,408 B at
8x8, unchanged from round 3. Text is about 12.4 KB. That container-sized RAM
is what #640 D4 needs, with no DDR3.

**The service bound**, from the module page:
- **Bytes, asserted.** The longest step touches `max(256, 2P + 6)` bytes,
  with P the shape's largest payload: 278 B at 1x1 and 1,158 B at 8x8.
- **Nominal calls, model time.** Runs with no command-master stall armed are
  asserted under 250 us per call. The suite's real maximum over all such runs
  is 168 us on the flash model's port and 210 us on LiteSPI, at every shape.
- **The cumulative bound for a slowed or stalled master, model time.** Every
  run is asserted under 2,213 us per call. That is the sum of the deadline
  (2,000 us), one check interval (3 us), the rest of a page program at the
  ready pace (42 us), and the link time of the window the call closes
  (168 us). The suite's real maximum over all runs is 2,189 us, or 2,190 us
  at `endstation_arty_4x4`. That case slows twelve waits, ending just before
  the deadline, and the call finishes past it at the ready pace. The same
  figures hold with the Arty shapes at their own 83.333 MHz. Measured cases
  at 1x1 and 8x8:

  | Master | Longest call |
  |---|---:|
  | two waits slowed by 4,000 reads | 539 us |
  | two drains slowed by 4,000 reads | 859 us |
  | ten waits slowed | 1,859 us |
  | twelve waits slowed, the call finishing past the deadline | 2,189 us |
  | every wait slowed: each program fails at the deadline | 2,009 us |

  Without the deadline, the every-wait case holds one call for 41,970 us.
- **CPU time, not measured.**
  - A port call still waiting on the master fails at its `timer0`
    deadline, which is real time on chip, whatever a CSR access costs.
  - The store's own work per step is derived, as a floor only: about 1.2 ms
    for the largest capture step at the capture receipt's per-byte rate. It
    is compared with nothing.

**Stated readings**, each in the module page:
- "The same bytes" is a CRC-32 digest of every byte the port delivered for a
  read, with its count. That is the 40 header bytes for a header verdict,
  and the header plus the whole container otherwise. A full comparison would
  need a second container-sized buffer.
- The port's deadline in clocks is published so the suite can hold it to the
  config's clock; it is the value the port compares with.
- The clock is the config's `sys_clk_hz`, held to what the builder hands
  `milan_soc.py`.
- From round 3: two reads that differ are a media fault, and a blank verdict
  needs confirmation like a refusal. The read retry is bounded at boot, and
  a slot still unread holds the writer until the next reset.
- From round 2: the binding walk is its own unit (D3 8.1 and 8.6), with a
  failed undo CLOSED. The exhaustion record is this store's status
  (FASTCONNECT 9.2, D3 6.3).

## Authoritative references

- #665: the lane F1 assignment (comment 5993775541), the round-2 assignment
  (comment 5996009284), the round-3 assignment and decisions 1 and 2
  (comment 5997929153), the round-4 assignment (comment 5999350068), and the
  bare-metal-first directive (comment 5992455815).
- #640 D4 and D5 (comment 5991591637).
- Reviews R500-1 (PR comment 5996001016), R501-1 (PR comment 5995888263),
  R500-2 (PR comment 5997904664), R501-2 (PR comment 5997910948), R500-3 (PR
  comment 5999342108) and R501-3 (PR comment 5999339293).
- #671, the same generation restart in the shipping writer.
- `configs/endstation_*.yaml` `board.constraints.sys_clk_hz`, and the
  builder's `--sys-clk-freq` (`sw/builder/endstation_builder.py`
  `emit_board_opts`).
- `docs/design/SAVED_STATE_FASTCONNECT.md`:
  - 4.2, the allocation;
  - 6.1 and 6.2, KLJ2 and its acceptance order;
  - 7, the A/B contract and, as amended here, the tie;
  - 9.2, loss and recovery;
  - 9.4, the deadlines.
- `docs/design/SAVED_STATE_MATERIALIZATION.md`:
  - 3, the no-shadow latch;
  - 6.1 to 6.3, the writer's state machines and the firmware DR2c policy;
  - 8.1, 8.3, 8.4, 8.6 and 8.8, the restore order, value rules, formats and
    maps, the transaction, and the no-progress deadline rule;
  - 15.1, DR2a, DR2b, DR2c, DR3b and DR5.
- `docs/design/PRESENTATION_TIME_WRAP.md` "The causal chain": a grandmaster
  restart moves domain time backwards.
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 7: the writer
  sequence the shipping writer follows.
- The processor writer `hdl/aecp/KL_aecp_nvm_writer.sv` at the pinned
  processor: F07.8 framing, the restore passes and the apply writes.
- #658 ruling comment 5988843004 item 3: the restore clip, cited and not
  depended on.

## How to get into the same state

```sh
git fetch origin
git checkout 665-f1-nvm
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install pyyaml
# the em-dash and contents gates use the pinned Markdown renderer
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
# the RV32 arm uses the pinned SDK (scripts/ci_rv32_sdk.py installs it);
# without one it reports SKIPPED unless --require-rv32 is given
# the builder bank wants Verilator 5.050 first on PATH
```

## How to validate

```sh
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 scripts/check_nvm_capture.py
python3 scripts/check_nvm_record_space.py && python3 scripts/check_nvm_record_space.py --self-test
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/check_cpp_idiom.py && python3 scripts/check_py_idiom.py
python3 scripts/measure_test_evidence.py --check && python3 scripts/check_baremetal_only.py --check
python3 scripts/docs_check.py && python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/gen_toc.py --check && python3 scripts/check_doc_paths.py
```

Expected result / pass criteria: every command exits 0.

- The first ends with `saved-state store gate (#665 F1): OK across 5 shape(s),
  42 checks, and all 82 planted defects reddened`.
- Per shape it prints the clock: `clock=83333000 Hz` for
  `endstation_arty_current`, `endstation_arty_4x4` and `endstation_arty_8ch`,
  and `clock=100000000 Hz` for the two AX7101 shapes. Its RV32 lines say
  `rv32 at 83333000 Hz` for the Arty shapes.
- Per shape, it prints the longest service call: 210 us with no stall armed,
  and 2,189 us with a command-master stall (2,190 us at
  `endstation_arty_4x4`).
- Its RV32 lines read `bss=4048` at `endstation_ax7101_1x1_tdm8` and
  `bss=14408` at `endstation_ax7101_8x8`.
- The self-test line for `ticks_per_us_truncated` says it was caught at
  83333000 Hz.
- The builder bank ends "ALL GATES PASS EXCEPT 1 NOT RUN" on a host without
  the mf48 Vivado report its gate 11 reads; that gate is environmental and
  unrelated to this change.

## Known limitations / out of scope

- No image links the store until F0's default-off switch merges. So the board
  proof is not here: real LiteSPI timing, a real power cut, and the CPU time
  of a step, which is derived.
- The LiteX-generated CSR and memory maps are stood in for: MMIO stand-ins
  for the RV32 build, and models of the command master and `timer0` for the
  host suite. The system clock is each shape's own.
- The owners behind the state port (the AECP, ACMP and map stores) are F3 and
  F5; a host state model stands in for them here.
- The packet mailbox and its HAL are F0's. The seam is the time call (a
  local counter, never the PHC) and the service and change hooks the event
  loop calls.
- A read fault that corrupts a valid slot the same way on every boot read,
  unreported by the port, reads as content: two reads of the same wrong
  bytes refuse it, and the generation can restart below it. Decision 2 takes
  no generation from unvalidated bytes, so this is a stated limit.
- Two different reads whose CRC-32 digests collide are taken as agreeing.
  That cannot happen when they differ in one or two bits, or only within 32
  consecutive bits; otherwise its probability is about 2^-32.
- The read retry runs at boot only. A slot that never reads cleanly, from a
  permanent fault or from reads that differ on every boot, holds the writer
  on every boot. The device serves and reports the hold, but nothing
  persists. R500-3 S1's narrower hold would be a change to decision 2.
- Raised for the manager:
  - the shipping writer's VD_REC/VD_LEN parity gap;
  - the shipping writer's generation restart, which is #671;
  - the lane gate is not yet in a hosted workflow;
  - how HELD with changes outstanding maps onto FASTCONNECT 9.2's flags, at
    integration (R500-3 S2).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
