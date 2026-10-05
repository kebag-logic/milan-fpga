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

GREEN at the lane head:

- 26 checks per shipped shape (5 shapes), 24 of them on both flash ports;
- 3,126 power-cut cases, 0 bad;
- 46 of 46 planted defects caught;
- the RV32I freestanding build is clean;
- every gate the change touches is at rc 0.

`665-f1-nvm` -> `dev`.

## Linked Issue / roles

Relates to #665 (lane F1, assignment comment 5993775541). The issue stays open:
F0 and F2 to F5 remain.

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
| flash port | `nvm_flash.h`, `plat/nvm_flash_litespi.c`, `host/nvm_fmodel.c` | read, program, erase, busy and time. The on-chip port is the shipping writer's LiteSPI access code, refusing writes outside the journal. The host model injects power cuts inside any erase or page program, media and read faults, and bit flips |
| state port | `nvm_state.h` | apply (judged by the SET rule), settle (formats against maps, where #658's restore clip lands), rollback, latch, release |
| boot | `nvm_store.c` | both slots judged; the newer accepted one re-staged, re-judged and applied as one transaction; an abort rolls back to the image defaults (DEFAULTS), an unproven model or a failed roll-back is CLOSED; AECP is released only at COMPLETE, BLANK or DEFAULTS |
| write-back | `nvm_store.c` | the 1,000 ms first-dirty window; a capture that latches one record per step; the seal; erase, blank check, ascending page program and read-back of the slot that is not authoritative; DR2c retries, DR2b suppression, DR5 slot choice; one bounded step per service call |
| host suite | `test/` | 26 checks per shape against `scripts/nvm_klj2.py`, the shipping suite's parity table and the recorded vectors `tb/verilator/nvm_backend/records_*.txt`; the power-cut sweep; 46 planted defects; the RV32 arm |

Static RAM: the stage is the container plus 8 bytes. With the largest payload,
one 256-byte read-back chunk and 256 bytes of state, the store's bss is
4,000 B at the shipping 1x1 TDM8 and 14,360 B at 8x8; text is about 10.4 KB.
That container-sized RAM is what #640 D4 needs, with no DDR3. The longest
service step touches `max(256, 2P + 6)` bytes, with P the shape's largest
payload: 278 B at 1x1 and 1,158 B at 8x8. That compares with the parent's
24.5 ms capture bound for a one-hold copy of 13,210 bytes; the per-step CPU
time is derived, not measured on the capture harness.

One finding outside this lane's scope: for a framed record whose
`payload_length` runs past the record area, the shipping writer answers
VD_REC where `klj2_decode` answers VD_LEN. It reproduces on the shipping
suite's harness, and that suite's parity table lacks the case. This store
answers VD_LEN. The shipping image needs its own Issue.

## Authoritative references

- #665 lane F1 assignment (comment 5993775541) and the bare-metal-first
  directive (comment 5992455815); #640 D4 and D5 (comment 5991591637).
- `docs/design/SAVED_STATE_FASTCONNECT.md`:
  - 4.2, the allocation;
  - 6.1 and 6.2, KLJ2 and its acceptance order;
  - 7, the A/B contract;
  - 9.4, the deadlines.
- `docs/design/SAVED_STATE_MATERIALIZATION.md`:
  - 3, the no-shadow latch;
  - 6.1 and 6.2, the writer's state machines;
  - 8.1, 8.3, 8.4 and 8.6, the restore order, value rules, formats and maps,
    and the transaction;
  - 15.1, DR2a, DR2b, DR2c, DR3b and DR5.
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 7: the writer
  sequence the shipping writer follows.
- The processor writer `hdl/aecp/KL_aecp_nvm_writer.sv` at the pinned
  processor: F07.8 framing, the restore passes and the apply writes.
- #658 ruling comment 5988843004 item 3: the restore clip, cited and not
  depended on.
- Milan v1.2 5.5.1.2: a rollback to the older slot after a torn newest one is
  within it, as section 7 states.

## How to get into the same state

```sh
git fetch origin
git checkout 665-f1-nvm
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install pyyaml
# the RV32 arm uses the pinned SDK (scripts/ci_rv32_sdk.py installs it);
# without one it reports SKIPPED unless --require-rv32 is given
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
  26 checks, and all 46 planted defects reddened`.
- Its RV32 lines read `bss=4000` at `endstation_ax7101_1x1_tdm8` and
  `bss=14360` at `endstation_ax7101_8x8`.

## Known limitations / out of scope

- No image links the store until F0's default-off switch merges. So the board
  proof is not here: real LiteSPI timing, a real power cut and the capture
  time on the CPU.
- The LiteX-generated headers are stood in for: MMIO stand-ins for the RV32
  build, models of the command master for the host suite.
- The owners behind the state port (the AECP, ACMP and map stores) are F3 and
  F5; a host state model stands in for them here.
- The packet mailbox and its HAL are F0's. The seam is one time call, and the
  service and change hooks the event loop calls.
- The shipping writer's VD_REC/VD_LEN parity gap is reported, not fixed: the
  shipping image is out of scope.

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
