[A753c]

## Contents

- **[Status](#status)** -- Round 3 of #823, the gates at the head and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and dependency commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

Round 3 of #823, at `f3e902f2a96bb27eac6ed7780c70905af34f389e`, `823-nvm-format` -> `dev-soft-core`.

On fresh clean clones of that head, every final rc is 0. Two first runs were repeated, with both logs kept: one hit a gap in the local runner, and one had two simulations time out beside the sweep.
- Every `run:` step of `rtl-fast`, `elaborate`, `rtl` (as for a ready PR) and `docs`: 149 ran, all rc 0. 193 did not run, each for a stated reason: hosted-only steps, tool installs replaced by the pinned tools, and the Verilator shards the sweep covers.
- The full sweep as four shards: 65 suites, 0 failures. The 11 the wall clock cut at two CPUs per shard were re-run uncontended and all pass.
- The builder bank, with `--require-rv32`: 106 gates exactly once per union.
- `test_ctrl_nvm.py --require-rv32 --self-test`: 474 tests, 123 of 123 planted defects caught.
- The LiteX simulations (8 of 8), the saved-state writer gate, and `git diff --check` against the merge base.

The evidence is in the REVIEW READY comment on #823.

## Linked Issue / roles

Relates to #823

Executor: `[A753c]`
Internal cleared-context reviewer: `[R805]`
External reviewer: `[R806]`

## Description

Round 3 of #823: the split placement's record space and framing (issuecomment-6730985093, with decisions 1, 2 and 6 of issuecomment-6730773797 scoped to the split).
The all-fabric placement keeps KLJ2 and today's limits: the processor, `KL_nvm_backend` and `milan_baremetal.c` are unchanged.
The split store's flash path is its own LiteSPI port (`nvm_flash_litespi.c`), never the processor or `KL_nvm_backend`.

| Piece | What it adds |
|---|---|
| `sw/firmware/ctrl_nvm/nvm_layout3.h` | The one layout 3 declaration: 12 block capacities, bases chained, 1,129 ids, a 10-byte header with a 16-bit `record_id`, NAME ids 222 to 1,128 |
| `scripts/nvm_layout3.py` | Its reader: exactly one decimal line per capacity, the base chain checked, `path:line` per block |
| `sw/builder/endstation_builder.py` | The builder's split output, `nvm_split.json`: every block's first id, count and capacity; a model over any block is refused, naming the declaration line. The all-fabric 128-name check is unchanged |
| `sw/builder/test_builder.py` | Gate 39: the 32x32 TDM8 overlay's 907 names accepted, 908 refused; the all-fabric header still refuses that shape; the 1x1 build writes the split output; 10 planted defects |
| `sw/firmware/ctrl_nvm` (`nvm_shape.h`, `nvm_klj2.[ch]`, `nvm_store.[ch]`, `plat/`, `host/`) | The F1 store in KLJ3 over layout 3, in `journal_klj3`: compile-time refusal of a shape over a block; KLJ2 refused `VD_VER`; today's journal read (two headers) and never written, its KLJ2 recorded in `legacy` and in the blank boot's verdict; open bits with counts; the whole-image commit erases every block its container spans |
| `sw/firmware/ctrl_nvm/test` | The fixture on the KLJ3 reference; KLJ2 at boot (today's journal, the store's slot, an unreadable header); the NAME block's first, last and one-past id at capacity, a commit over two erase blocks, and 908 names refused at compile time; open counts; 13 new planted defects, 9 re-anchored |
| `scripts/nvm_klj3.py`, `scripts/check_nvm_klj3.py` | The KLJ3 reference codec and its gate (ledger, split output, round trip, refusals, capacity), 6 plants; in the docs workflow's NVM record-space step |
| `sw/litex/milan_soc.py`, `sw/litex/ctrl_memory*.py` | `journal_klj3` (640 KiB at 14,592 KiB) in `FLASHBOOT_RESERVED`; the split SoC publishes `MILAN_NVM3_*` from the builder's split output; the KLJ3 stage and the ledgered points' stage size |
| `sw/firmware/ctrl_nvm/plat/gen_flash_port.py`, `tb/verilator/nvm_split_target` | The split SoC's journal rule on `journal_klj3` and today's journal; the split target's cases on the KLJ3 reference |
| `sw/firmware/gtest` | Coverage ratchet re-recorded at 100 % after exclusions; four exclusion rows re-pinned to the new statements |
| Docs | The 32x32 format page (the format is the split's; A3 graded at the typical 15 us with its margin; the declaration gated against the bound shape), the store's README, the split target's README, the memory plan's KLJ3 delta, FASTCONNECT section 6 |

## Authoritative references

- #823: the round 3 ruling (issuecomment-6730985093) and the round 2 ruling (issuecomment-6730773797), decisions 1, 2 and 6
- [Saved-state format up to 32x32](docs/design/SAVED_STATE_FORMAT_32X32.md), sections 2, 3, 5, 6 and 8
- [Saved-state backing store](docs/design/SAVED_STATE_FASTCONNECT.md), sections 4.2, 6 and 7
- N25Q128 datasheet, section 9.1.20 and Table 17: the erase suspend latency, 15 us typical, no maximum
- IEEE 1722.1-2021 SET_NAME and GET_NAME: 64-octet names; Milan v1.2 5.3.13: names persist

## How to get into the same state

```sh
git fetch origin
git checkout 823-nvm-format
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
python3 -m pip install pyyaml
```

## How to validate

```sh
python3 scripts/nvm_layout3.py
python3 scripts/check_nvm_klj3.py --self-test
python3 scripts/check_nvm_format_32x32.py --self-test
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/builder/test_builder.py --gates test_name_count_fits_the_nvm_name_block,test_split_record_space_bounds_the_split_output
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
```

Expected result / pass criteria: each exits 0; the F1 gate prints `OK across 5 shape(s)` and `all 123 planted defects reddened`; gate 39 prints `10/10 planted defects`; the reference gate `all 6 planted defects caught`.

## Known limitations / out of scope

- **The gateware VERSION is not moved.** The format's own chain is done (KLJ3 major 3, layout 3, KLJ2 `VD_VER`). This head changes no gateware, the all-fabric placement must stay unchanged, and the split architecture's section 7 binds VERSION to the placement an image runs, landing the split's with the default flip. Posted as an open question on #823.
- The append-only save path, the windows, erase suspend and the commit deadline are round 4. The whole-image commit is unchanged.
- The TDM8 32x32 AEM ROM limit (87,545 B against 65,536 B) and the builder's 16-row and 5-bit SRP limits are #859's, kept.
- The split target harness's recorded results predate KLJ3 and were not measured again; its portable self-test passes.
- The target platform's split image was not linked again; the size fixture was, at four points.
- Area under #818 applies to the split once round 4 lands.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
