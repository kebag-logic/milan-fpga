[A753e]

## Contents

- **[Status](#status)** — Round 5 of #823, the gates on the head, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and dependency commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from CONTRIBUTING.md.

## Status

Round 5 of #823, at `7c97e99f`, `823-nvm-format` -> `dev-soft-core`. `dev-soft-core` is still `1d6bf555`, which round 4 merged.

- On a clean clone of this head: every `run:` step of the four workflows a pull_request to `dev-soft-core` triggers. 152 ran, all rc 0; the 198 that need the hosted runner each have a reason.
- Also on that clone, all rc 0: the builder bank, the LiteX simulations, the store's self-test (191 planted defects), the page's drift gate, `make twin` and `make twin-plants`.
- The full sweep ran at `b6a60fbd`, 65 of 65 suites PASS. The later commits change no file a sweep suite reads.
- **Decision needed:** the 8x8 two-interface ledger, and #818's routed gate, which was not run (Known limitations).

The evidence is in the REVIEW READY comment on #823.

## Linked Issue / roles

Relates to #823

Executor: `[A753e]`
Internal cleared-context reviewer: `[R805]`
External reviewer: `[R806]`

## Description

#823 gives the split placement its own saved-state format, sized for shapes up to 32x32.
Round 3 built the record space and framing; round 4 merged `dev-soft-core` and fixed what both reviews found.
Round 5 (the ruling of issuecomment-6754858510) builds the split store's append-only save path, decisions 3, 4, 5 and 7, and fixes the two Docs findings of round 4's reviews.
The all-fabric placement keeps KLJ2 and today's limits: the processor, `KL_nvm_backend` and `milan_baremetal.c` are unchanged, and the store reaches the flash only through its own LiteSPI port.

| Piece | What it adds |
|---|---|
| `sw/firmware/ctrl_nvm/nvm_store.[ch]` | The append-only journal. A slot is a base and a log of deltas behind it. A save appends the changed records as one delta, at most 28 pages, and never erases. A compaction writes the stage as a base into the other slot at the old slot's sequence, page by page, yielding to a save, a record a page cuts carried whole; then the old slot's new deltas are copied behind it and the authority moves. The other slot is prepared in the background: every page read blank, a written block erased and read again. A save during that erase suspends it, times the suspend, programs and resumes it. The boot walks each log (two walks that agree, as a refusal does) and replays the chosen slot's into the stage, to the end it was judged to have. 150 ms first-dirty window; 500 ms deadline per append |
| `sw/firmware/ctrl_nvm/nvm_flash.h`, `plat/nvm_flash_litespi.c` | Two port calls, `suspend` and `resume`: PES (`0x75`) and PER (`0x7a`) on the command master |
| `sw/firmware/ctrl_nvm/nvm_shape.h`, `nvm_klj2.[ch]` | The log's geometry (`NVM_LOG_START`, `NVM_RESERVE`, `NVM_SEG_PAGES`), a delta's header check, and compile-time refusals of a slot that holds no base and log at least as large, and of a record larger than a segment. `NVM_DOCTORED_MAPIN` is refused outside the host test's shape header |
| `sw/firmware/ctrl_nvm/host/` | The flash model's erase suspend (15 us, the datasheet's typical; slow or ignored on request; no progress when suspended within 40 us), and its policing of a read while busy, a program into the suspended block, and an erase of the kept slot. The command-master model decodes PES and PER |
| `sw/firmware/ctrl_nvm/test/` | `test_nvm_journal.cpp` (replay, torn and stale deltas, every delta rule alone, compaction with a save in it and its carry, the suspended erase, the reserve, the deadline), `test_nvm_bound.cpp` (the save bound and the commit deadline at 32x32/2if TDM8), the write tests on the append path, a power-cut sweep of a compaction, compile checks for the fit, the 255-entry input table and the doctored macro, and 183 planted defects with 8 controls |
| `scripts/nvm_klj3.py`, `scripts/check_nvm_klj3.py` | The reference's journal (`klj3_delta`, `klj3_slot`, `klj3_slot_decode`), and its gate's journal rule with 3 more plants |
| `scripts/check_nvm_format_32x32.py`, `scripts/nvm_format_32x32_tables.py` | The page's test plan rows T7 to T13 and T15 done; layer anchors on the save path; the store's four save-path constants held to the page's figures; a line citation refused in every form (S-a), with a plant per form |
| Docs | The 32x32 format page (section 4's rules as built, the host suite's bound, decisions 3 to 7 implemented); the store's README; FASTCONNECT section 5, its contents entry and status row (RS5, RS6); QSPI_FLASHBOOT (N2); SPLIT_CONTROL_MEMORY (N1, and the append path's memory); the materialization register's note on decision 4 |

Round 5, by item of the ruling:

1. **The append-only save path**, decisions 3, 4, 5 and 7, as the table above describes, with its tests and its planted defects. At 32x32/2if TDM8 the host suite measures 321,274 us from the change to the read back when the save meets the erase, and 325,187 us when it meets a compaction. The bound is 500 ms, and the page's arithmetic gives 304.71 ms plus the suspend. Twice the worst append is 350,374 us (the worst append is 175,187 us), within the 500 ms deadline. The suspend is graded at its typical 15 us. The writer times every suspend (`suspend_us_max`) and counts each one longer than the 95.29 ms room (`suspend_slow`). The save path never reaches the flash through the processor or `KL_nvm_backend`.
2. **N1.** SPLIT_CONTROL_MEMORY reports what the `c20ed894` run printed, 3,344 against 13,264 bytes, and points at section 5 for the KLJ3 sizes.
3. **N2.** QSPI_FLASHBOOT says who reads and writes each reserved range, as FASTCONNECT section 5's table does: the split's store owns `journal_klj3`, the all-fabric writer writes `journal`, and the split's store reads `journal`'s two headers and never writes it. The stale "nothing writes or reads them" and "blank-flash responder" sentences are gone.
4. **Residue.** RS5 and RS6 in FASTCONNECT. RS-a: "(#665, the split placement's saved-state store)" in `nvm_klj2.c`, `nvm_klj2.h`, `nvm_shape.h`, and the other comment instances this change added. RS-b: the rewritten write tests name `nvm_klj3.py`; `nvm_rig.cpp` and `test_nvm_boot.cpp` keep theirs, as ruled.
5. **Suggestions.** S-a (SG3): `LINE_CITE_RE` refuses a range, a list, an unquoted path, "`path` line N" and a `#L` link, a plant each. S-b (SG4): the codec compiles at 255 input entries, and a control makes the limit one less. S-c: `#error` when `NVM_DOCTORED_MAPIN` is defined outside the host test build, with its control.
6. **Area.** #818's gate is a routed Vivado gate, and this round runs no Vivado, so it was not run. The split memory plan was linked instead, at `30ca4b21` and at this head, on clean clones with the pinned SDK. The append path adds 5,280 B of `rom` (5,288 at 8x8 with one interface) and 800 to 1,248 B of `sram`. 1x1 goes from 37.5 to 39.0 RAMB36, 1x1 with two interfaces from 41.0 to 42.0, and 8x8 from 51.0 to 52.5. **8x8 with two interfaces plans 59.5 RAMB36 against its ledgered 57.5, and the plan refuses it.** The ledger is not moved; the decision is put on #823.

## Authoritative references

- #823: the round 5 ruling (issuecomment-6754858510); the round plan (issuecomment-6730985093), item 2; decisions 3, 4, 5 and 7 of issuecomment-6730773797; the owner's 0.5 s bound (issuecomment-6545924397) and the append-only direction (issuecomment-6545894131)
- [Saved-state format up to 32x32](docs/design/SAVED_STATE_FORMAT_32X32.md), sections 3, 4, 8 and 9
- [Saved-state backing store](docs/design/SAVED_STATE_FASTCONNECT.md), sections 5, 6.2, 7 and 9.4
- [Materialization](docs/design/SAVED_STATE_MATERIALIZATION.md), DR2a, DR2b, DR2c and DR5
- N25Q128 datasheet, section 9.1.20 and Tables 17 and 18: the erase suspend, its 15 us typical latency with no maximum, and what a suspended device programs and reads

## How to get into the same state

```sh
git fetch origin
git checkout 823-nvm-format
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
python3 -m pip install pyyaml
```

## How to validate

```sh
python3 scripts/check_nvm_klj3.py --self-test
python3 scripts/check_nvm_format_32x32.py
python3 scripts/check_nvm_format_32x32.py --self-test
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32
make -C tb/verilator/milan_dp twin
make -C tb/verilator/milan_dp twin-plants
```

Expected result / pass criteria:

- Each command exits 0.
- The store's gate prints `OK across 5 shape(s)` and `all 191 planted defects reddened`, and at the bound shape `save bound at 32x32/2if TDM8` with both figures under 500 ms.
- The page gate prints `0 finding(s)`, and its self-test `self-test: PASS`.
- The reference gate prints `all 9 planted defects caught`.

## Known limitations / out of scope

- **The 8x8 two-interface ledger** (57.5 RAMB36) does not hold the append path, which plans 59.5. No CI gate plans the linked image, so nothing fails today. It is the owner's decision.
- **#818's routed area gate was not run**: this round runs no Vivado.
- The target platform's image was not linked again: `ctrl_plat_image.py` takes the store from its own tree.
- The stage stays the whole container. A stage of only one page and one record would need compaction to stream from the owners. That is not built.
- The suspend latency is graded at the datasheet's typical 15 us, which has no maximum. The real part, its timing and real power cuts need the board.
- The all-fabric placement keeps KLJ2 and its whole-image commit; nothing in it changes.
- RS-c and SG5 are not this round, as ruled.
- Found, not changed: the header comments of `nvm_rig.hpp` and `nvm_suite.hpp` name `scripts/nvm_klj2.py` as the fixture's source, which is now `nvm_klj3.py`.
- Hosted CI has not run on this head; the evidence is local.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
