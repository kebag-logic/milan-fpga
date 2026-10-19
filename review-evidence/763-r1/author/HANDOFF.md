# Lane 763 handoff ([A653])

Issue #763: empty dynamic audio mapping lists are not restored after a power cycle.
Assignment: issue #763 comment 6256482855. TAKEN: comment 6256965417. STOP: comment 6257029697.
Branch `763-map-persist` from dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`; origin checked as
`https://github.com/kebag-logic/milan-fpga.git`. Processor submodule at `2cbed0a987c1e68402658d69459ab7e5aa571adc`
(its own origin checked, and the submodule is its own top level). Nothing was run inside a submodule beyond `rev-parse`.

## Status: Round B in progress (see the Round B section at the end). Round A below stopped with no commits.

The lane head is still `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, and the tree is clean.

The issue's suspected cause is not what the board ran. The cause is that no
map-record writer exists in the shipping build. Issue #637 already owns that
writer (materialization lane 4), and #763's acceptance cannot be met inside
#763's scope. Meeting it in place would mean building lane 4 here, which
silently takes over another issue's lane and its dependencies. Changing the
record format, as assignment item 2 suggests, would change an accepted
contract that already separates "empty" from "erased". Both need a decision,
so I stopped before editing anything.

## Findings

F1. **The shipping build writes no channel-map record.** Record ids `0x60`-`0x7F` are never written,
so at boot every map record is erased, and the port reset set (the #658 identity, clipped to the
restored formats) comes back. That is the reported symptom. A non-empty non-default list would
revert in the same way; the qualification run only exercised the empty case.
- The default AX7101 build is `milan_baremetal` plus the processor in fabric
  (`sw/litex/milan_soc.py:4216-4220`). The `ctrl` firmware runs only under `--ctrl-mailbox`, whose
  datapath side is held idle (`sw/litex/milan_soc.py:3827-3833`).
- The processor's D3 writer cannot form a map id. Its group-base function returns only
  `0x00, 0x02, 0x0A, 0x30, 0x40, 0x50, 0x80` (`protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:397-406`),
  and its header says channel maps are the integrator's and that it never writes or reads them (`:119-121`).
  The binding manager writes `0x20 + sink` only (FASTCONNECT section 2).
- In the parent, the maps have no record writer, and their pending clears only at reset
  (`hdl/milan/KL_pp_shadow.sv:929-932`, `:949-951`). Stage 3 is named as the owner of the map restore
  (`hdl/milan/milan_datapath.sv:4452-4455`).
- `milan_baremetal.c:894-921` only programs the backend's per-port map length tables. It latches no map.
- The contract says the same thing: SAVED_STATE_MATERIALIZATION.md:17-20 ("Channel maps (stage 3) are not
  implemented", and they are the parent's to write, restore and roll back), :1217-1219, and
  SAVED_STATE_FASTCONNECT.md:1472-1476 ("accepted images contain bindings and erased spans").
- The owning work is already open: #637 (the parent restores the maps from `0x60`/`0x70`), with acceptance in
  SAVED_STATE_MATERIALIZATION.md section 18.4, lane 4: "Persist input and output ports independently,
  including empty sets", with a cold cycle of ADD/REMOVE on both mutable directions. #637 has no lane yet.

F2. **The record format already tells "empty" from "erased"** (assignment item 2 is met by the accepted contract).
- An erased record is its whole span, the 8 header bytes included, filled with `0xFF` (FASTCONNECT section 6.1, the
  erased-record rule, `SAVED_STATE_FASTCONNECT.md:661-676`).
- An empty set is a FRAMED record (magic `0x1722`, layout, id, length, crc16) whose entries are all UNUSED, and an
  UNUSED entry is exactly eight `0xFF` bytes (`SAVED_STATE_MATERIALIZATION.md:1138-1151`; `SAVED_STATE_FASTCONNECT.md:332`).
  Case V3g in MATERIALIZATION section 8.3 (`:1164`) applies that set as the valid empty set.
- The firmware store separates the two cases on the header alone (`sw/firmware/ctrl_nvm/nvm_store.c:298`), and it frames
  every latched payload, an all-`0xFF` one included (`nvm_store.c:502-516`). `aecp_nvm.c:56-73` applies the framed empty
  payload as `count == 0`. So the issue's reading of `aecp_nvm.c:60-66` (that a `0xFF` row makes the record look erased)
  is wrong: erasure is decided before `apply()` runs, from the header.
- Changing to a row count, or to a non-`0xFF` empty marker, would change MATERIALIZATION section 8.3, FASTCONNECT section 4.2,
  the reference codec (`scripts/nvm_klj2.py`), `scripts/check_nvm_record_space.py` check 12, and the lengths the backend
  derives per port. It would gain nothing, because the two cases are already distinct. Under the assignment's STOP rule
  I did not attempt it.

F3. **Executable confirmation on the firmware path** (scratch only, nothing committed). Receipt: `receipts/probe/`.
The probe appends one test to a scratch copy of `sw/firmware/ctrl/test/test_aecp.cpp` and runs the existing AECP
saved-state arm (`aecp_arms.core_arm`, mode `nvm`, filter `Nvm.*`) at `endstation_ax7101_1x1_tdm8`. It runs once per
direction. The test empties port 0 through REMOVE_AUDIO_MAPPINGS (IEEE 1722.1-2021 7.4.46) and removes one row from port 0
of the other direction. It then commits through the real store, checks the empty record is framed with every entry
unused, resets to defaults, power-cycles the flash model and boots.
| Arm | Result |
|---|---|
| clean sources | rc 0, 8/8 `Nvm.*` pass, the probe included |
| plant `apply-empty-as-erased` (`aecp_nvm.c`: `count == 0` keeps the defaults) | probe FAILS, the empty port comes back with its 8 defaults; the in-tree `WholeMapFramingAndEmptySetAreDistinct` also fails |
| plant `store-payload-as-erased` (`nvm_store.c:298`: an all-`0xFF` payload is read as erased) | probe FAILS, the 8 defaults come back; **no in-tree test fails** |

The second plant is the only failure mode on this path that reproduces the board symptom, and the in-tree suite does
not catch it. That is a real firmware-path test gap, but it is a different defect from the board's. I left it for the
decision (option B below), not fixed opportunistically.

## Proposed decision (the manager's to make)

- **A (recommended).** Treat #763 as a symptom of #637. Close #763 as covered by #637, or keep it open as its
  board-acceptance item, and add #763's acceptance (an empty list and a non-empty non-default list, on both directions,
  across a cold cycle) to #637's acceptance. It is already in MATERIALIZATION section 18.4. Leave the record format
  unchanged (F2).
- **B (small, independent).** Narrow #763 to the firmware path. Commit the probe as an in-tree test in
  `sw/firmware/ctrl/test/test_aecp.cpp`, and register the two plants as mutants in
  `sw/firmware/ctrl/test/aecp_mutants.py`. That closes the F3 gap. It does not fix the board, so the issue's board
  item would move to #637. Gates: `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`.
  The capture check does not pin `ctrl` sources (it hashes `milan_baremetal.c` only), so no capture re-measure is needed.
- **Not proposed.** Building lane 4 under #763. It depends on lanes 1-3, DR3a budgets, the DR4 area ceilings and #501,
  it is RTL work in the map plane, and it belongs to #637.

## Changes

None. No file in the tree was edited and nothing was committed.

## New checks and planted mutants

None in the tree. The scratch probe and its two plants are in `receipts/probe/` (F3).

## Resources and route timing

Not applicable: no RTL changed.

## Gate table

| Gate | Command | rc | Note |
|---|---|---|---|
| firmware AECP saved-state arm, clean, with the probe (scratch) | `python3 -I empty_map_probe.py <repo> <scratch>` | 0 | `receipts/probe/verdict.txt`, `none.log` |
| same, two plants | (same run) | plants red, as required | `apply-empty-as-erased.log`, `store-payload-as-erased.log` |

No in-tree gate was run, because no in-tree file changed. The probe ran on the system interpreter, because the pinned
CPython 3.12.3 lacks PyYAML, which the builder needs.

## Standards

Milan v1.2 5.3.9.1 (STREAM_PORT_OUTPUT channels mapping) and 5.3.10.1 (STREAM_PORT_INPUT channels mapping): the dynamic
mapping list is saved in non-volatile memory and restored after a power cycle. IEEE 1722.1-2021 7.4.45 and 7.4.46
(ADD/REMOVE_AUDIO_MAPPINGS) are the edits that change it.

## Receipts

See `receipts/INDEX.md`, generated from the files present.

## Round B (ruling: issue #763 comment 6257040042)

The ruling: both A and B. #637 owns the board's map-record writer and restore, and takes #763's cold-cycle
acceptance. #763 narrows to B: commit the probe as an in-tree firmware test, with both plants as named mutants,
and run the firmware test gate. No record-format change.

Status: REVIEW READY, posted as issue #763 comment 6258557430. Lane head `07c6c72fce79e705bcf28a70071497d0ce7040e4`, two commits on dev `e9cbb676`, not pushed.

| Commit | Subject |
|---|---|
| `94264da763c161c62502edf423b1a7d1efd8d839` | Prove an empty and a non-default dynamic map survive the store's power cycle, with both #763 plants as AECP mutants |
| `07c6c72fce79e705bcf28a70071497d0ce7040e4` | Document the #763 empty-map persistence and the AECP campaign's planted store copy |

No firmware source, record format, saved-state layout or RTL changed. `aecp_nvm.c`, `nvm_store.c` and `nvm_klj2.c`
are untouched, so records written by the shipping image read exactly as before (assignment item 6 does not arise).
`scripts/check_nvm_capture.py` pins `milan_baremetal.c` only, which is untouched, so no capture re-measure applies.

### Changes

| Where | What | Clause |
|---|---|---|
| `sw/firmware/ctrl/test/test_aecp.cpp:250-286` | New `Nvm.EmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle`, in the `AECP_TEST_NVM` block. Once per direction (STREAM_PORT_INPUT 14, STREAM_PORT_OUTPUT 15): blank flash and boot to `NVM_T_BLANK`. REMOVE_AUDIO_MAPPINGS removes every row of port 0 in that direction and the last row of port 0 in the other. The test commits through the real store (`save()`), then checks the empty record's magic `0x1722` (`:277`) and that its payload is all UNUSED (`:278`). It restores defaults, power-cycles the flash model and boots to `NVM_T_COMPLETE`. The emptied list must stay empty (`:282`), and the other list must equal its saved bytes and hold `default_count - 1` rows (`:283-284`). | Milan v1.2 5.3.9.1, 5.3.10.1; IEEE 1722.1-2021 7.4.46; FASTCONNECT 6.1 (erased-record rule); MATERIALIZATION 8.3 V3g |
| `sw/firmware/ctrl/test/aecp_mutants.py:357-371` | Two named defects (below). | #763 |
| `sw/firmware/ctrl/test/aecp_mutants.py:507-509` | The campaign copies `sw/firmware/ctrl_nvm` (without its `test/`) beside its copy of the firmware tree, so that a store defect can be planted. | #763 |
| `sw/firmware/ctrl/test/aecp_arms.py:20` | `saved_state()` compiles the store from `tree.src.parent / "ctrl_nvm"`. For the checkout (`CTRL`) that is the same directory as before, and every other caller of the AECP arms uses `CTRL` (checked by searching every `Tree(` construction). | #763 |
| `sw/firmware/ctrl/aecp/README.md:105-109`, `:136-139` | The empty-map persistence rule, and the campaign's planted store copy. | Milan v1.2 5.3.9.1, 5.3.10.1 |

A wording edit to `ctrl_configs.py` (SUITES) was tried and reverted. That file is a hash-declared script in
`ci/image/command-table.json`, and its existing text ("copies of the firmware's tree") still holds, because
`ctrl_nvm` is part of `sw/firmware`.

### New check and planted mutants

| Mutant | Plant | Required failures (test, diagnostic) | Result | Without the new test |
|---|---|---|---|---|
| `nvm-empty-map-keeps-defaults` | `aecp_nvm.c` `apply()`: `if (count == 0) return NVM_APPLIED;` before `aecp_map_restore` | new test "the empty list survives the power cycle"; `Nvm.WholeMapFramingAndEmptySetAreDistinct` "all UNUSED is an intentional empty set" | caught (`[ok]`) | `WholeMapFramingAndEmptySetAreDistinct` still fails (72/73 pass) |
| `nvm-unused-payload-reads-erased` | `nvm_store.c:298` `nvm_apply_faults()`: an all-`0xFF` payload also counts as blank | new test "the empty list survives the power cycle" | caught (`[ok]`) | **escapes**: 73/73 AECP app-arm tests pass at two interfaces, and all six store suite binaries pass at the shipping shape |

The last column is the gap the ruling names. Receipts: `receipts/round-b/gap/` and `receipts/round-b/store-gap/`.

### Resources and route timing

Not applicable: no RTL changed.

### Gate table

All gates ran on a tree byte-identical to `07c6c72`, on CPython 3.12.3 (a scratch venv with PyYAML and the pinned
LiteX), the pinned RV32 SDK, and for `--only verilator` the pinned Verilator 5.050.

| Gate | Command | rc | Receipt |
|---|---|---|---|
| firmware bank, every phase and campaign | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test` | 0 | `gates/test_ctrl_firmware/` (`test_ctrl_firmware: PASS`, 939 `[ok]`, 0 escaped; full log 333913 bytes, sha256 `375b9655e7dfd1e416d32b3f85e0d7728ef1351c98a91c5a3d0871f075567f21`, extract kept) |
| four-job shard dispatch | `python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py` | 0 | `gates/fwunit/shards.log` (shard sizes 61, 521, 79, 279) |
| tally self-test | `python3 sw/firmware/gtest/tally_selftest.py` | 0 | `gates/fwunit/tally_selftest.log` |
| RV32 self-test | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | `gates/fwunit/fw_rv32_selftest.log` |
| saved-state store suites | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | `gates/fwunit/test_ctrl_nvm.log` (5 shapes, 435 tests) |
| coverage ratchet | `python3 sw/firmware/gtest/fw_coverage.py --selftest`; `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 0; 0 | `gates/fwunit/fw_coverage_*.log` (30 files, ratchet unchanged) |
| TSN stack boundary | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | 0 | `gates/boundary/without.log` |
| TSN stack boundary, Verilator builders | `VERILATOR=<pinned> python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator` | 0 | `gates/boundary/only-verilator.log` |
| docs | `python3 scripts/docs_check.py`; `python3 scripts/check_feature_status.py`; `python3 scripts/check_doc_style.py` and `--selftest`; `python3 scripts/gen_toc.py --selftest`, `--verify-anchors`, `--check`; `python3 scripts/check_em_dash.py --base e9cbb676` | all 0 | `gates/docs/` |
| new mutants alone, through the real campaign | `python3 -I new_mutants.py <test dir> <scratch>` (the table's own `controls()` first) | 0 | `new-mutants/` |
| clean AECP app arm, `Nvm.*`, one and two interfaces | `python3 sw/firmware/ctrl/test/aecp_arms.py --output <scratch> --app --interfaces 1\|2 --filter 'Nvm.*'` | 0; 0 | `clean-arm/` (8/8 each) |

Not a gate of this change, and recorded as an open item: `python3 scripts/ci_tool_inventory.py --check` exits 2 at
the base `e9cbb676` already ("tool inventory differs"), on the digests of `scripts/check_doc_style.py` and
`scripts/measure_test_evidence_readers.py`. At the lane head it differs by two more input digests, `aecp_arms.py`
and `aecp_mutants.py`, and by nothing else (`receipts/round-b/inventory/`). The check runs in the CI image build
(`ci/image/build.py:211`), not in a pull-request workflow. Regenerating it here would fold unrelated drift into this
lane, so I left it to the inventory's owner. `ci/image/exec-audit-receipt.json` is a committed traced-run receipt and
was not regenerated either.

The gates' build products under `tb/verilator/mbx/obj_*` and the interpreter caches the runs created, including one
inside the processor submodule, were removed. The tree and every submodule are clean.

### Open risks/questions

- The inventory digests above, for the inventory's owner.
- The board symptom is #637's (ruling A). This lane does not touch it.

### Receipts

`receipts/INDEX.md`, generated by `receipts/make_index.py` from the files present. Round B's are under
`receipts/round-b/`, with host paths replaced by `<scratch>`, `<repo>`, `<tools>`, `<home>` and `<data>`.
