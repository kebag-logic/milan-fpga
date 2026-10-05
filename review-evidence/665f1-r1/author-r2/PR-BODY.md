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

GREEN at the lane head (round 2):

- 37 checks per shipped shape (5 shapes): 29 on both flash ports, 5 on the
  flash model's port alone, 3 on the LiteSPI port alone;
- 3,126 power-cut cases, 0 bad;
- 69 of 69 planted defects caught;
- the RV32I freestanding build is clean;
- every gate the change touches is at rc 0.

`665-f1-nvm` -> `dev`.

## Linked Issue / roles

Relates to #665 (lane F1: assignment comment 5993775541, round-2 assignment
comment 5996009284). The issue stays open for F0 and F2 to F5.

Executor: `[A544]`
Internal cleared-context reviewer: `[R500]`
External reviewer: `[R501]`

## Description

This PR adds the bare-metal saved-state store of the Mark II split: a new
portable C11 module, `sw/firmware/ctrl_nvm/`, with no OS and no heap. Every
buffer is a static array sized from the entity shape at build time. Nothing
links it into an image yet: it sits behind the #665 build switch, whose
default is the all-fabric build. The shipping writer
`sw/firmware/milan_baremetal/milan_baremetal.c` is byte-identical, and no
RTL, SoC, builder, register-map or configuration file changes.

| Piece | Files | What it does |
|---|---|---|
| shape | `nvm_shape.h` | the record set and container sizes, from the generated `MILAN_NVM_*` constants the shipping writer compiles against |
| codec | `nvm_klj2.c` | KLJ2 container and F07.8 record codec, the section 6.2 acceptance order with the erased-record rule; verdicts equal `scripts/nvm_klj2.py` |
| flash port | `nvm_flash.h`, `plat/nvm_flash_litespi.c`, `host/nvm_fmodel.c` | read, program, erase, busy and time, every call bounded. The on-chip port is the shipping writer's LiteSPI access code: writes are refused outside the journal, every wait on the command master gives up after 4,096 status reads without progress, and time is `timer0`, a local counter, never the PHC. The host model injects power cuts inside any erase or page program, media, refusal and read faults, and bit flips |
| state port | `nvm_state.h` | apply (judged by the SET rule), settle (formats against maps, where #658's restore clip lands), rollback of one walk, latch, release |
| boot | `nvm_store.c` | each slot judged on one read, so CRC, records and SEQ are the same bytes; the newer one re-staged and re-judged, its SEQ equal to the pick's; the binding walk first, as its own unit; then the D3 walk as one transaction, whose roll-back leaves the bindings applied; AECP released only at COMPLETE, BLANK or DEFAULTS |
| write-back | `nvm_store.c` | the 1,000 ms first-dirty window (a change the running capture takes opens none); a capture that latches one record per step; the seal; erase, blank check, ascending page program and read-back of the slot that is not authoritative; DR2c per captured work set, the console included, with a reset-sticky exhaustion record; DR2b suppression; DR5 slot choice |
| host suite | `test/` | 37 checks per shape against `scripts/nvm_klj2.py`, the shipping suite's parity table and the recorded vectors `tb/verilator/nvm_backend/records_*.txt`; the power-cut sweep; PHC steps and the counter's wrap; a stalling command master; 69 planted defects; the RV32 arm |

**Round 2** answers R500-1 and R501-1, both NEGATIVE at `215c3c0b`, item by
item:

| Item | Finding | Change | Planted defects that now fail |
|---|---|---|---|
| 1 | R500-1 F1, R501-1 F3: the PHC as time base | `timer0` accumulated to 64 bits; the unused blocking helper removed | `phc_time`, `clock_not_accumulated` |
| 2 | R500-1 F2, R501-1 F2: DR2c re-armed and bypassed | the capture decides whether the work set changed; the console respects backoff and exhaustion; `abandoned` and `abandoned_vd` kept until reset | `budget_rearmed_by_change`, `budget_rearmed_by_capture`, `commit_now_overrides_exhaustion`, `commit_now_ignores_backoff`, `success_forgives_exhaustion` |
| 3 | R501-1 F1: selection on an unchecked re-read | one-read judgment; re-stage judged with its CRC and SEQ equal to the pick's | `select_on_unchecked_reread`, `stage_seq_unchecked`, `slot_read_fail_ignored` |
| 4 | R501-1 F4: unbounded SPI waits | no-progress bounds returning a status, chip select released | `xfer_unbounded`, `open_unbounded`, `stall_ignored` |
| 5 | R500-1 F3: DR2a window left armed | a change the running capture takes arms nothing | `capture_leaves_window_armed` |
| 6 | R500-1 F4: bindings in the D3 transaction | the binding walk first, its own unit; the D3 roll-back leaves it applied | `d3_rollback_takes_bindings`, `bindings_in_d3_walk`, `binding_fault_aborts_d3`, `binding_fault_keeps_preloads` |
| 7 | R500-1 F5: claims with no defect that fails | checks for the read-back and blank-check tails, the tie, read failures and refusals | `verify_skips_last_stretch`, `blankcheck_first_stretch_only`, `blankcheck_read_fail_ignored`, `verify_read_fail_ignored`, `program_refusal_ignored`, `tie_picks_b` |
| 8 | R500-1 F6: the service-bound sentence | the module page's "The service bound": bytes and model time asserted, CPU time derived with its assumptions | |

**Static RAM**: the stage is the container plus 8 bytes. With the largest
payload, one 256-byte read-back chunk, 280 bytes of state and the 12-byte
clock, bss is 4,032 B at the shipping 1x1 TDM8 and 14,392 B at 8x8; text is
about 11.0 KB. That container-sized RAM is what #640 D4 needs, with no DDR3.

**The service bound**:
- the longest step touches `max(256, 2P + 6)` bytes, with P the shape's
  largest payload: 278 B at 1x1 and 1,158 B at 8x8 (asserted);
- no call holds the loop past 1,000 us of model time (asserted; at most
  210 us measured);
- the CPU time per step is DERIVED, not measured: about 1.2 ms for the
  largest capture step at the capture receipt's per-byte rate, a floor
  because the step does more per byte than that copy loop. That compares
  with the parent's 24.5 ms capture bound.

**Stated readings**, each in the module page:
- D3 sections 8.1 and 8.6 settle the bindings, so there was no STOP. A
  binding walk whose undo fails ends CLOSED.
- FASTCONNECT 9.2 and D3 6.3 give firmware exhaustion no reset-sticky alarm
  of its own. So the exhaustion record is this store's status, and `stale`
  keeps the 9.2 recovery rule.
- On equal sequences slot A is picked, as the shipping writer picks. Section
  7's pseudo-code would pick B; that conflict is raised for a decision.

## Authoritative references

- #665 lane F1 assignment (comment 5993775541), round-2 assignment (comment
  5996009284), the bare-metal-first directive (comment 5992455815); #640 D4
  and D5 (comment 5991591637); reviews R500-1 (PR comment 5996001016) and
  R501-1 (PR comment 5995888263).
- `docs/design/SAVED_STATE_FASTCONNECT.md`:
  - 4.2, the allocation;
  - 6.1 and 6.2, KLJ2 and its acceptance order;
  - 7, the A/B contract;
  - 9.2, loss and recovery;
  - 9.4, the deadlines.
- `docs/design/SAVED_STATE_MATERIALIZATION.md`:
  - 3, the no-shadow latch;
  - 6.1 to 6.3, the writer's state machines and the firmware DR2c policy;
  - 8.1, 8.3, 8.4, 8.6 and 8.8, the two walks and their order, value rules,
    formats and maps, the transaction, and the no-progress deadline rule;
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
  37 checks, and all 69 planted defects reddened`.
- Its RV32 lines read `bss=4032` at `endstation_ax7101_1x1_tdm8` and
  `bss=14392` at `endstation_ax7101_8x8`.
- The builder bank ends "ALL GATES PASS EXCEPT 1 NOT RUN" on a host without
  the mf48 Vivado report its gate 11 reads; that gate is environmental and
  unrelated to this change.

## Known limitations / out of scope

- No image links the store until F0's default-off switch merges. So the board
  proof is not here: real LiteSPI timing, a real power cut, and the CPU time
  of a step, which is derived.
- The LiteX-generated headers are stood in for: MMIO stand-ins for the RV32
  build, models of the command master and `timer0` for the host suite.
- The owners behind the state port (the AECP, ACMP and map stores) are F3 and
  F5; a host state model stands in for them here.
- The packet mailbox and its HAL are F0's. The seam is the time call (a
  local counter, never the PHC) and the service and change hooks the event
  loop calls.
- Raised for the manager, not fixed here:
  - the shipping writer's VD_REC/VD_LEN parity gap;
  - the tie rule (section 7 against the shipping writer);
  - a commit written at SEQ 1 after a transiently refused slot can lose to
    that slot on the next boot;
  - the lane gate is not yet in a hosted workflow.

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
