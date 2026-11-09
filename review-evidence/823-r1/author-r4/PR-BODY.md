[A753d]

## Contents

- **[Status](#status)** — Round 4 of #823, the gates on the merged head, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and dependency commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from CONTRIBUTING.md.

## Status

Round 4 of #823, at `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14`, `823-nvm-format` -> `dev-soft-core`. The head includes `dev-soft-core` `1d6bf555` through merge commit `3bcf0cdd`.

On fresh clean clones of that head, every final rc is 0:
- Every `run:` step of `rtl-fast` (with `split-cdc`), `elaborate`, `rtl` (as for a ready PR) and `docs`: 152 ran, all rc 0. 198 did not run, each for a stated reason: hosted-only steps, tool installs replaced by the pinned tools, and the Verilator shards the sweep covers.
- The full sweep as four shards: 65 suites, 0 failures, 0 timeouts.
- The builder bank: 107 gates exactly once in each union, with `--require-rv32` and `--require-elaboration`.
- `test_ctrl_nvm.py --require-rv32 --self-test`: 506 tests, 130 of 130 planted defects caught.
- The format page's drift gate and its self-test, with a control that moves every cited line.
- The LiteX simulations (8 of 8), the saved-state writer gate, the two-placement simulation and its plants, and `git diff --check` against the merge base.

A first full run on `8c66ab1e` failed one LiteX simulation: the memory plan's rule table had moved to KLJ3 and `ctrl_memory.RULES` had not. `30ca4b21` fixes the rule text, and everything above was run again on it.

The evidence is in the REVIEW READY comment on #823.

## Linked Issue / roles

Relates to #823

Executor: `[A753d]`
Internal cleared-context reviewer: `[R805]`
External reviewer: `[R806]`

## Description

#823 gives the split placement its own saved-state format, sized for shapes up to 32x32.
Round 3 built the record space and framing.
Round 4 (the ruling of issuecomment-6742264763) merges `dev-soft-core` and fixes what both reviews found.
The all-fabric placement keeps KLJ2 and today's limits: the processor, `KL_nvm_backend` and `milan_baremetal.c` are unchanged.

| Piece | What it adds |
|---|---|
| `sw/firmware/ctrl_nvm/nvm_layout3.h` | The one layout 3 declaration: 12 block capacities, bases chained, 1,129 ids, a 10-byte header with a 16-bit `record_id`, NAME ids 222 to 1,128 |
| `scripts/nvm_layout3.py` | Its reader: exactly one decimal line per capacity, the base chain checked, `path:line` per block |
| `sw/builder/endstation_builder.py` | The builder's split output, `nvm_split.json`: every block's first id, count and capacity; a model over any block is refused, naming the declaration line. The all-fabric 128-name check is unchanged |
| `sw/builder/test_builder.py` | Gate 39: the 32x32 TDM8 overlay's 907 names accepted, 908 refused; the all-fabric header still refuses that shape; the 1x1 build writes the split output; 10 planted defects |
| `sw/firmware/ctrl_nvm` (`nvm_shape.h`, `nvm_klj2.[ch]`, `nvm_store.[ch]`, `plat/`, `host/`) | The F1 store in KLJ3 over layout 3, in `journal_klj3`. A shape over a block, or a map entry count past the codec's table (256 on an input port, 65,536 on an output port), does not compile. KLJ2 is refused `VD_VER`. Today's journal is read (two headers) and never written, and its KLJ2 is recorded in `legacy` and in the blank boot's verdict. Open bits carry counts. The whole-image commit erases every block its container spans. The per-step byte bound counts the layout 3 header |
| `sw/firmware/ctrl_nvm/test` | The fixture on the KLJ3 reference. KLJ2 at boot: today's journal, the store's slot, an unreadable header. The `legacy` rule's limits: another format there is not recorded, a refused own slot keeps its verdict, and today's slots are read where the flash map puts them. The NAME block's first, last and one-past id at capacity. A commit over two erase blocks, and one over an older container, with each erase's address checked. 908 names, and a too-wide map count, refused at compile time. 127 planted defects and three compile-time controls |
| `scripts/nvm_klj3.py`, `scripts/check_nvm_klj3.py` | The KLJ3 reference codec and its gate (ledger, split output, round trip, refusals, capacity), 6 plants; in the docs workflow's NVM record-space step |
| `scripts/nvm_format_32x32_tables.py`, `scripts/check_nvm_format_32x32.py` | The format page's drift gate. Each anchor is a file and a token that only one of its lines carries, and the page cites no line number, so a merge that moves the lines leaves the page true. 12 plants and a control that moves every cited line |
| `sw/litex/milan_soc.py`, `sw/litex/ctrl_memory*.py` | `journal_klj3` (640 KiB at 14,592 KiB) in `FLASHBOOT_RESERVED` and its slot comment; the split SoC publishes `MILAN_NVM3_*` from the builder's split output; the KLJ3 stage and the ledgered points' stage size |
| `sw/firmware/ctrl_nvm/plat/gen_flash_port.py`, `tb/verilator/nvm_split_target` | The split SoC's journal rule on `journal_klj3` and today's journal; the split target's cases on the KLJ3 reference |
| `sw/firmware/gtest` | Coverage ratchet re-recorded at 100 % after exclusions; four exclusion rows re-pinned to the new statements |
| Docs | The 32x32 format page: the format is the split's; A3 graded at the typical 15 us with its margin; the declaration gated against the bound shape; the gateware VERSION not moved, as ruled. Also the store's README, the split target's README and the memory plan's KLJ3 delta. FASTCONNECT sections 5 and 6, QSPI_FLASHBOOT and the regenerated flash diagram show `journal_klj3` |

Round 4, by item of the ruling:

1. `dev-soft-core` `1d6bf555` merged with a merge commit. The page's anchors are found by token, and its drift gate is green on the merged tree. The seven files both sides changed have no semantic conflict (below).
2. The step bound counts the crc16 over the layout 3 header's first 8 bytes, not the layout 2 header's 6. `service_bound` takes the header size from the reference, and the plant `step_bytes_layout2` is caught.
3. `journal_klj3` appears in FASTCONNECT section 5, QSPI_FLASHBOOT, the slot comment in `milan_soc.py` and the generated diagram.
4. Three new tests pin the `legacy` rule: `legacy_other_format_not_recorded`, `own_refusal_kept_over_legacy` and `klj2_journal_at_its_flash_map_address`. `capacity_commit_over_stale` grades the multi-block erase over non-blank flash. Each has its plant.
5. The page and its generated T16 cell say the gateware VERSION is "not moved, as ruled (#823)".
6. The residue: no issue-comment ID, lane label or round label in this change's source comments; the page's prose citations by token; KLJ3 where the split's container is meant, in the memory plan's rule and on the page.
7. Two compile-time asserts in `nvm_shape.h` refuse a map entry count past its table. The gate requires both refusals in their words, and a control removes each assert.

The seven files both sides changed:

| File | `dev-soft-core` | This branch | Interaction |
|---|---|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md` | rewords "F-INT PR 2" as the placement switch | the KLJ3 stage figures and table | none |
| `scripts/ci_events.py` | the `split-cdc` job and its result | four commands in the docs NVM record-space step | none |
| `sw/builder/endstation_builder.py` | `control.placement`, `CTRL_SPLIT_P` and the split argv | `emit_nvm_split`, written for every build | a split-placement build reads its `nvm_split.json` from the same output |
| `sw/builder/test_builder.py` | gate 23m's split cases | gate 39 | gate 23m stops at the datapath Instance, before the split output is read |
| `sw/firmware/ctrl/test/ctrl_configs.py` | the twin's sources classified | the KLJ3 scripts classified | none |
| `sw/firmware/ctrl/test/test_aecp.cpp` | the ENTITY `available_index` test | two NVM tests on the KLJ3 macros | none |
| `sw/litex/milan_soc.py` | the placement switch | `journal_klj3` and the split constants | the page's line anchors moved: now found by token |

The two-placement simulation of `1d6bf555` compiles this store and its flash model. On this head, `make -C tb/verilator/milan_dp twin` reports `0 finding(s)`, and `twin-plants` refuses each of its 20 plants.

## Authoritative references

- #823: the round 4 ruling (issuecomment-6742264763), the round 3 ruling (issuecomment-6730985093), and the round 2 ruling (issuecomment-6730773797), decisions 1, 2 and 6
- The gateware VERSION: not moved, as ruled on #823 (issuecomment-6739542795). The format's own chain is the VERSION step: KLJ3 major 3, layout 3, KLJ2 refused `VD_VER`. VERSION 3 lands with the default flip
- [Saved-state format up to 32x32](docs/design/SAVED_STATE_FORMAT_32X32.md), sections 2, 3, 5, 6 and 8
- [Saved-state backing store](docs/design/SAVED_STATE_FASTCONNECT.md), sections 4.2, 5, 6 and 7
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
python3 scripts/check_nvm_format_32x32.py
python3 scripts/check_nvm_format_32x32.py --self-test
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/builder/test_builder.py --gates test_name_count_fits_the_nvm_name_block,test_split_record_space_bounds_the_split_output
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 sw/litex/flash_map.py
```

Expected result / pass criteria:

- Each command exits 0.
- The F1 gate prints `OK across 5 shape(s)` and `all 130 planted defects reddened`.
- The page gate prints `0 finding(s)`, and its self-test `self-test: PASS` with `control moved-lines: 0 finding(s)`.
- Gate 39 prints `10/10 planted defects`, and the reference gate `all 6 planted defects caught`.
- `flash_map.py` lists `journal_klj3` at `0x0E40000`, 640 KiB.

## Known limitations / out of scope

- **The gateware VERSION is not moved, as ruled (#823).** This head changes no gateware.
- The append-only save path, the windows, erase suspend and the commit deadline come after this round is reviewed. The whole-image commit is unchanged apart from its erase loop.
- The TDM8 32x32 AEM ROM limit (87,545 B against 65,536 B) and the builder's 16-row and 5-bit SRP limits are #859's, kept.
- The split target harness's recorded results predate KLJ3 and were not measured again; its portable self-test passes.
- The target platform's split image was not linked again; the size fixture was, at four points.
- Area under #818 applies to the split once the append path lands.
- `flash_layout.png` is rendered from the regenerated SVG at 1,800 px wide. This host's renderer does not reproduce the committed base PNG byte for byte, so its pixels are this renderer's.

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
