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

GREEN at the lane head (round 3):

- 40 checks per shipped shape (5 shapes): 29 on both flash ports, 7 on the
  flash model's port alone, 4 on the LiteSPI port alone;
- 3,126 power-cut cases, 0 bad;
- 80 of 80 planted defects caught;
- the RV32I freestanding build is clean;
- every gate the change touches is at rc 0.

`665-f1-nvm` -> `dev`.

## Linked Issue / roles

Relates to #665: lane F1, assignment comment 5993775541, with rounds 2 and 3
in comments 5996009284 and 5997929153. The issue stays open for F0 and F2 to
F5.

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
| flash port | `nvm_flash.h`, `plat/nvm_flash_litespi.c`, `host/nvm_fmodel.c` | read, program, erase, busy and time, with every wait bounded and every call bounded. The on-chip port is the shipping writer's LiteSPI access code. Writes are refused outside the journal. A wait gives up after 4,096 status reads without progress, and a call still waiting after 2,000 us of `timer0` time fails. Time is `timer0`, a local counter, never the PHC. The host model injects power cuts inside any erase or page program, media, refusal and read faults, and bit flips |
| state port | `nvm_state.h` | apply (judged by the SET rule), settle (formats against maps, where #658's restore clip lands), rollback of one walk, latch, release |
| boot | `nvm_store.c` | Each slot is judged on one read, so CRC, records and SEQ are the same bytes. A verdict stands on at most 3 reads: OK on one, any other verdict only when two reads agree. A slot that gives neither is UNREAD. The newer slot is re-staged and re-judged, with its SEQ equal to the pick's. Then the binding walk; then the model check, where an unproven model is CLOSED with the bindings kept; then the D3 walk as one transaction. AECP is released only at COMPLETE, BLANK or DEFAULTS. An UNREAD slot holds the writer until reset |
| write-back | `nvm_store.c` | the 1,000 ms first-dirty window (a change the running capture takes opens none); a capture that latches one record per step; the seal; erase, blank check, ascending page program and read-back of the slot that is not authoritative; DR2c per captured work set, the console included, with a reset-sticky exhaustion record; DR2b suppression, which also heals `stale`; DR5 slot choice |
| host suite | `test/` | 40 checks per shape against `scripts/nvm_klj2.py`, the shipping suite's parity table and the recorded vectors `tb/verilator/nvm_backend/records_*.txt`; the power-cut sweep; PHC steps and the counter's wrap; a stalling and a slowed command master; 80 planted defects; the RV32 arm |

**Round 3** answers R500-2 and R501-2, both NEGATIVE at `7f8dc1b1`, under
the decisions in #665 comment 5997929153:

| Item | Finding | Change | Planted defects that now fail |
|---|---|---|---|
| 1, decision 2 | R501-2 F1 (MAJOR): after a transient boot read fault, a verified commit at SEQ 1 lost to the surviving slot on a clean boot | A failed read is retried, 3 reads per slot. A refusal or a blank verdict needs two agreeing reads. A slot with no standing verdict, or that never re-stages as judged, is UNREAD, and the writer is then HELD until reset: no erase, no write, the console refused, changes reported dirty. No SEQ is taken from an unvalidated slot. `authority_unknown` runs both orientations at SEQ 1, 5, 0x80000000 and 0xFFFFFFFF, with a clean reboot, a change, a commit and another clean reboot, and compares the restored payload | `unread_not_held` (the generation restart), `read_not_retried`, `refusal_unconfirmed`, `blank_unconfirmed`, `restage_not_retried` |
| 2, decision 1 | R501-2 F3: the tie rule | FASTCONNECT section 7 reads `>= 0`, A on a tie, citing the decision. `newer_wins` ties at 7 and at 0xFFFFFFFF with distinct payloads | `tie_picks_b` |
| 3 | R501-2 F2, R500-2 F2: a per-wait bound offered as a per-call figure | A per-call deadline on `timer0` (2,000 us) in the port. Nominal runs are asserted under 250 us and every run under 2,213 us. `port_deadline` slows ten, twelve and every wait. With every wait slowed, the program fails at the deadline | `call_deadline_ignored`, `deadline_per_wait` |
| 4 | R500-2 F1: the model check before the binding walk | the order of D3 8.1: binding walk, model check, D3 walk; CLOSED keeps the bindings | `bindings_skipped_unproven`, `model_ready_ignored` |
| 4 | R500-2 F3: the fallback re-stage and the DR2a boundary untested | `fallback_restage`; `debounce` changes the record the capture examines next | `fallback_restage_unchecked`, `taken_off_by_one` |
| 4 | R500-2 F4: DR2b left `stale` set | `stale` heals at a DR2b suppression too | `dr2b_keeps_stale` |
| 4 | R500-2 S1 | a failed fallback re-stage is `VD_LEN` and UNREAD | as above |
| 5 | dev moved | `--no-ff` merge of dev `28f9666f` | |

**Static RAM**: the stage is the container plus 8 bytes. With the largest
payload, one 256-byte read-back chunk, 288 bytes of state and the 20-byte
clock and deadline, bss is 4,048 B at the shipping 1x1 TDM8 and 14,408 B at
8x8. Text is about 11.8 KB. That container-sized RAM is what #640 D4 needs,
with no DDR3.

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
  the deadline, and the call finishes past it at the ready pace. Measured
  cases at 1x1 and 8x8:

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
- Two reads of one slot that disagree are a media fault, and a blank verdict
  needs confirmation like a refusal.
- The read retry is bounded at boot, and a slot still unread holds the writer
  until the next reset.
- From round 2: the binding walk is its own unit (D3 8.1 and 8.6), with a
  failed undo CLOSED. The exhaustion record is this store's status
  (FASTCONNECT 9.2, D3 6.3).

## Authoritative references

- #665: the lane F1 assignment (comment 5993775541), the round-2 assignment
  (comment 5996009284), the round-3 assignment and decisions 1 and 2
  (comment 5997929153), and the bare-metal-first directive (comment
  5992455815).
- #640 D4 and D5 (comment 5991591637).
- Reviews R500-1 (PR comment 5996001016), R501-1 (PR comment 5995888263),
  R500-2 (PR comment 5997904664) and R501-2 (PR comment 5997910948).
- #671, the same generation restart in the shipping writer.
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
  40 checks, and all 80 planted defects reddened`.
- Per shape, it prints the longest service call: 210 us with no stall armed,
  and 2,189 us with a command-master stall (2,190 us at
  `endstation_arty_4x4`).
- Its RV32 lines read `bss=4048` at `endstation_ax7101_1x1_tdm8` and
  `bss=14408` at `endstation_ax7101_8x8`.
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
- A read fault that corrupts a valid slot the same way on every boot read,
  unreported by the port, reads as content. Two agreeing reads refuse it,
  and the generation can restart below it. Decision 2 takes no generation
  from unvalidated bytes, so this is a stated limit.
- The read retry runs at boot only; a slot still unread holds the writer
  until the next reset.
- Raised for the manager:
  - the shipping writer's VD_REC/VD_LEN parity gap;
  - the shipping writer's generation restart, which is #671;
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
