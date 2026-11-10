[A753f]

## Contents

- **[Status](#status)** — #823 as the format only, the gates on the head, and `823-format` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and dependency commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from CONTRIBUTING.md.

## Status

#823's saved-state format for the split placement, at `2905c8749a4573450b9999dd546bb20ae5c7fc38`, `823-format` -> `dev-soft-core`.
It is round 4's head `30ca4b21` plus seven commits of the round 6 ruling (PR #863 issuecomment-6767385787), and nothing of the save path.
The merge base is `dev-soft-core` `1d6bf555`.

On fresh clean clones of that head, every final rc is 0:
- Every `run:` step of `rtl-fast` (with `cd tests && behave`), `elaborate`, `rtl` (as for a ready PR) and `docs`: 152 ran, all rc 0. 145 ran at the head. The 7 of `firmware-unit` passed at `e0adcc09`, whose only difference is one plant string in `scripts/check_nvm_format_32x32.py`, which that job neither names nor scans. 198 did not run, each for a stated reason: hosted-only steps, tool installs replaced by the pinned tools, and the Verilator shards the sweep covers.
- The full sweep as four shards: 65 of 65 suites pass, 0 in-suite failures. `capture_coherence` hit its 2,400 s wall clock in its shard and passed when run again alone on four CPUs (2,262 s). Every preflight passed, suite cancellation included.
- The builder bank: 107 gates exactly once in each union, with `--require-rv32` and `--require-elaboration`.
- `test_ctrl_nvm.py --require-rv32 --self-test`: 506 tests, 132 of 132 planted defects caught.
- The format page's drift gate and its self-test: 0 findings; every plant caught, the control that moves every cited line at 0.
- `behave` (508 scenarios), the control mutants (570 of 570), the AECP and SRP campaigns, the firmware boundary, the LiteX simulations (8 of 8), the saved-state writer gate, and `git diff --check` against the merge base.

The first full run, on `e0adcc09`, found one defect: the firmware boundary took the drift gate for an unregistered firmware builder, because a plant's citation named the firmware's tree. `2905c874` moves that citation outside it.

The evidence is in the REVIEW READY comment on #823.

## Linked Issue / roles

Closes #823
Relates to #876 (the append-only save path, built there) and #877 (the 32x32 save worst case against 0.5 s)

Executor: `[A753f]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

#823 gives the split placement its own saved-state format, sized for shapes up to 32x32.
The all-fabric placement keeps KLJ2 and today's limits: the processor, `KL_nvm_backend` and `milan_baremetal.c` are unchanged.

**Section 4 of the format page, the save path, is designed here and built under #876.**
Its rules, its 32x32 worst case and its deadlines are the ruled design (decisions 3, 4, 5 and 7).
At this head the split store still saves by the whole-image commit.

| Piece | What it adds |
|---|---|
| `sw/firmware/ctrl_nvm/nvm_layout3.h` | The one layout 3 declaration: 12 block capacities, bases chained, 1,129 ids, a 10-byte header with a 16-bit `record_id`, NAME ids 222 to 1,128 |
| `scripts/nvm_layout3.py` | Its reader: exactly one decimal line per capacity, the base chain checked, `path:line` per block |
| `sw/builder/endstation_builder.py` | The builder's split output, `nvm_split.json`: every block's first id, count and capacity; a model over any block is refused, naming the declaration line. The all-fabric 128-name check is unchanged |
| `sw/builder/test_builder.py` | Gate 39: the 32x32 TDM8 overlay's 907 names accepted, 908 refused; the all-fabric header still refuses that shape; the 1x1 build writes the split output; 10 planted defects |
| `sw/firmware/ctrl_nvm` (`nvm_shape.h`, `nvm_klj2.[ch]`, `nvm_store.[ch]`, `plat/`, `host/`) | The split store in KLJ3 over layout 3, in `journal_klj3`. A shape over a block, or a map entry count past the codec's table (256 on an input port, 65,536 on an output port), does not compile; 255 on an input port does. The doctored input-width build compiles only under the host test's shape header. KLJ2 is refused `VD_VER`. Today's journal is read (two headers) and never written, and its KLJ2 is recorded in `legacy` and in the blank boot's verdict. Open bits carry counts. The whole-image commit erases every block its container spans. The per-step byte bound counts the layout 3 header |
| `sw/firmware/ctrl_nvm/test` | The fixture on the KLJ3 reference. KLJ2 at boot: today's journal, the store's slot, an unreadable header. The `legacy` rule's limits. The NAME block's first, last and one-past id at capacity. A commit over two erase blocks, and one over an older container, with each erase's address checked. Compile-time refusals and their accept side. 127 planted defects and five compile-time controls |
| `scripts/nvm_klj3.py`, `scripts/check_nvm_klj3.py` | The KLJ3 reference codec and its gate (ledger, split output, round trip, refusals, capacity), 6 plants; in the docs workflow's NVM record-space step |
| `scripts/nvm_format_32x32_tables.py`, `scripts/check_nvm_format_32x32.py` | The format page's drift gate. Each anchor is a file and a token that only one of its lines carries. The page cites no line number in any form: `path:N`, a range, a list, unquoted, "`path` line N" or a `#L` link. 17 plants and a control that moves every cited line |
| `sw/litex/milan_soc.py`, `sw/litex/ctrl_memory*.py` | `journal_klj3` (640 KiB at 14,592 KiB) in `FLASHBOOT_RESERVED` and its slot comment; the split SoC publishes `MILAN_NVM3_*` from the builder's split output; the KLJ3 stage and the ledgered points' stage size |
| `sw/firmware/ctrl_nvm/plat/gen_flash_port.py`, `tb/verilator/nvm_split_target` | The split SoC's journal rule on `journal_klj3` and today's journal; the split target's cases on the KLJ3 reference |
| `sw/firmware/gtest` | Coverage ratchet re-recorded at 100 % after exclusions; four exclusion rows re-pinned to the new statements |
| Docs | The 32x32 format page; the store's README; the split target's README; the memory plan's KLJ3 delta; FASTCONNECT sections 1, 5 and 6; QSPI_FLASHBOOT; the regenerated flash diagram |

The round 6 ruling's items, on top of `30ca4b21`:

| Item | Commit | What changed |
|---|---|---|
| N1 | `249cca50` | SPLIT_CONTROL_MEMORY reports what the `c20ed894` run printed: 3,344 against 13,264 bytes, the KLJ2 stage sizes; section 5 gives both formats' |
| N2 | `249cca50` | QSPI_FLASHBOOT names each reserved range's owner as FASTCONNECT section 5 does: the split's store writes `journal_klj3`; the all-fabric writer owns `journal`, whose two headers the split store reads and never writes; `user` has no owner |
| RS5, RS6 | `249cca50` | FASTCONNECT's contents entry and status row name `journal_klj3` |
| Section 4 under #876 | `8e29bc74` | The page's status line, contents, section 4 lead, sections 3 and 9, and the test plan's state cells (through the generator) say the save path is designed here and built under #876 |
| R806-5 R2 | `8e29bc74` | "The room, taken from the all-fabric worst case (404.71 ms) and so conservative for the split, is 95.29 ms." Both figures are gated |
| #818 waiver | `8e29bc74` | Section 7 says area under #818's gate is waived for this format and names the memory plan as its evidence |
| RS-a | `64c3565e`, `e0adcc09` | "(#665, the split placement's saved-state store)" in `nvm_klj2.c`, `nvm_klj2.h` and `nvm_shape.h`, and the same wording in the branch's other comments that named the lane: `nvm_layout3.h`, `nvm_layout3.py`, `nvm_klj3.py`, `check_nvm_klj3.py`, `endstation_builder.py`, `test_builder.py` |
| RS-b | `64c3565e` | `nvm_klj3.py` in the six places in `test_nvm_write.cpp`; `nvm_rig.cpp` and `test_nvm_boot.cpp` keep `nvm_klj2.py`, as ruled |
| RS-d | `64c3565e` | `scripts/nvm_klj3.py` as the fixture's source in `nvm_rig.hpp` and `nvm_suite.hpp` |
| SG3 = S-a | `4d0353e3`, `2905c874` | `LINE_CITE_RE` refuses every line-number form; six plants, one per form, each caught by the citation it names. `2905c874` moves the list-form plant's citation outside the firmware's tree, which the firmware boundary reads as a builder's |
| SG4 = S-b | `0d9e9b50` | The codec must compile at 255 input entries; control `mapin_limit_one_early` (`>= 255u`) is caught |
| S-c | `0d9e9b50` | `nvm_shape.h` has an `#error` for `NVM_DOCTORED_MAPIN` without `NVM_HOST_TEST`, which only the host test's builds define; `doctored_outside` requires the refusal in its words, and control `doctored_error_removed` is caught |

**#818's route is waived** (round 6 ruling): this head changes no HDL, gitlink or generated SoC RTL against `dev-soft-core` `1d6bf555`.
- `git diff --name-only 1d6bf555 HEAD` lists no `.sv`, `.svh`, `.v`, `.vh` or `.vhd` file and nothing under `hdl`, `syn` or a submodule; no gitlink changes; nothing under `configs/generated` changes.
- The shipping AX7101 SoC, elaborated with its own launch line at both commits and no vendor run, gives the same generated RTL: init files, constraints and build script byte-identical; the Verilog and Tcl identical apart from each clone's path, the date stamp and the hierarchy comment's sibling order.
- The area evidence is the memory table at `30ca4b21` (SPLIT_CONTROL_MEMORY section 5): the ledgered 8x8 two-interface point plans 57.5 RAMB36, its ledger. The store's code is unchanged since `30ca4b21`: its freestanding RV32 build has the same section sizes at all five shapes.

## Authoritative references

- #823: the round 6 ruling (PR #863 issuecomment-6767385787), items 2 to 5 of the round 5 ruling (issuecomment-6754858510), R805-5 RS-d (issuecomment-6766982225) and R806-5 R2 (issuecomment-6767224297); the round 4 (issuecomment-6742264763), round 3 (issuecomment-6730985093) and round 2 (issuecomment-6730773797) rulings
- The gateware VERSION: not moved, as ruled on #823 (issuecomment-6739542795). The format's own chain is the VERSION step: KLJ3 major 3, layout 3, KLJ2 refused `VD_VER`. VERSION 3 lands with the default flip
- [Saved-state format up to 32x32](docs/design/SAVED_STATE_FORMAT_32X32.md), sections 2 to 9
- [Saved-state backing store](docs/design/SAVED_STATE_FASTCONNECT.md), sections 4.2, 5, 6 and 7
- N25Q128 datasheet, section 9.1.20 and Table 17: the erase suspend latency, 15 us typical, no maximum
- IEEE 1722.1-2021 SET_NAME and GET_NAME: 64-octet names; Milan v1.2 5.3.13: names persist

## How to get into the same state

```sh
git fetch origin
git checkout 823-format
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
git diff --name-only 1d6bf555 HEAD -- '*.sv' '*.svh' '*.v' '*.vh' '*.vhd' hdl syn protocol-processor gptp-processor third_party external configs/generated
```

Expected result / pass criteria:

- Each command exits 0, and the last prints nothing.
- The store's gate prints `OK across 5 shape(s)` and `all 132 planted defects reddened`, with the lines `at width: MILAN_NVM3_MAPIN_ENTRIES_0 = 255, its table's limit, compiles` and `doctored build outside the host test: refused at compile time`.
- The page gate prints `0 finding(s)`, and its self-test `self-test: PASS` with `control moved-lines: 0 finding(s)`.
- Gate 39 prints `10/10 planted defects`, and the reference gate `all 6 planted defects caught`.
- `flash_map.py` lists `journal_klj3` at `0x0E40000`, 640 KiB.

## Known limitations / out of scope

- **The save path is #876's.** Section 4 of the format page is its design: the append-only journal, compaction, background erase with suspend, the 150 ms firmware window and the 500 ms append deadline. Nothing of it is built here. The 32x32 save worst case against 0.5 s is #877.
- **The gateware VERSION is not moved, as ruled (#823).** This head changes no gateware.
- **#818's route is not run**: it is waived by the round 6 ruling while the head changes no HDL, gitlink or generated SoC RTL (above).
- The Arty shipping SoC's launch line fails identically at `1d6bf555` and at this head in the local LiteX environment (no PLL configuration for its clocks), so only the AX7101 SoC's generated RTL is compared.
- The TDM8 32x32 AEM ROM limit (87,545 B against 65,536 B) and the builder's 16-row and 5-bit SRP limits are #859's, kept.
- The split target harness's recorded results predate KLJ3 and were not measured again; its portable self-test passes.
- The target platform's split image was not linked again; the size fixture was, at four points, at round 4.
- `flash_layout.png` is rendered from the regenerated SVG at 1,800 px wide. Another renderer does not reproduce the committed base PNG byte for byte.
- FASTCONNECT section 5.1's citation table gives `milan_soc.py` lines from an older head; it is on the residue checklist #495, as ruled.

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
