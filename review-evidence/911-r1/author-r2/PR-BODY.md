[A782]

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

GREEN -- 150/150 workflow steps rc 0 (522 not run with a stated reason; no RTL change, so the Verilator suites stand at 65/65 from round 1), 27/27 lane gates, reviewer mutants K3, K4, K7 and K9 red -- `911-ax7a200t-variant` -> `dev`, head `8e523a2b` on dev `b7d69295`.

## Linked Issue / roles

Closes #911

Executor: `[A782]`
Internal cleared-context reviewer: `[R841]` (round R841-1 at `4958ca4f`)
External reviewer: `[R842]` (round R842-1 at `4958ca4f`)

## Description

The XC7A200T variant of the ALINX board: the AX7101's 1x1 TDM8 shipping shape, built for `xc7a200t-fbg484-2`.

| Piece | Change |
|---|---|
| `sw/litex/build.sh` | `cfg_ax7a200t` is `cfg_ax7101` plus `--fpga-part xc7a200t-fbg484-2`; `recipe_config` binds it to `configs/endstation_ax7101_1x1_tdm8.yaml`; `board_facts` gives it the programmer part `xc7a200tfbg484`. |
| `sw/litex/platforms/` | `BOARD_PARTS` and `board_part()` in `ax7101_timing.py`; `configure_commands(part)`; `alinx_ax7101.Platform(part=)`. Pins and constraints stay in the one platform file. |
| `sw/litex/milan_soc.py` | `--fpga-part` (refused with `--board arty`); `FLASHBOOT_BITSTREAM_SLOT` moves the 200T's AEM region to `0xA00000`; the layout records `flash_device` and `flash_jedec_id`. |
| `sw/litex/flash_map.py` | `layout_for()`, the one statement of the slot rule; `load_map(part)`. |
| `sw/litex/layout_from_soch.py` | Bitstream budget from the compiled AEM offset; flash device from soc.h through litespi. |
| `sw/litex/qspi_owner_transition.py`, `deploy.sh` | `check-board`: before the first dump or write, `flash`, `flash-images` and `flash-pair` read the JTAG die and the flash JEDEC ID. They refuse a die or flash other than the image set's, a JTAG chain with more than one 7-series device, and a target layout that names no flash device. |
| `scripts/check_sweep_shape.py` | `BUILD_DIES`: `--fpga-part` allowed on `ax7a200t` only, two plants. |
| `scripts/board_variants.py` | New: the guide's board variant table is checked against `build.sh`, the flash map and the SoC's flash module, with six mutation controls; `--layout` checks a built layout. |
| `sw/builder/test_builder.py` | Gate 1e: the fake programmer answers `--detect` (one or two chain devices, one or two ID lines); refusal arms on all three paths; a 200T image set on the 200T map (AEM and bitstream budget at `0xA00000`, a 9,730,652-B payload) flashes through `build.sh flash ax7a200t` with the AEM at `0xA00000` and the payload at 0. Gate 24d's anchor follows the new platform line. |
| `sw/builder/test_timing_grade.py` | `test_board_parts`, `test_board_variant_docs` and `test_layout_from_soch` (a LiteX-rendered soc.h per die rebuilds the SoC's exported layout and flash device; the 200T's payload passes the deploy validation), all run by the timing-grade builder gate. |
| Docs | `docs/guides/BOARD_DEPLOYMENT.md` (variant table, "Flash an image set over JTAG", `INSTALLED_BUILD`, "The board check", "Image sets built before #911", what is untested), `docs/integration/QSPI_FLASHBOOT.md` (the variant's layout, the AX7101's two new layout fields), `docs/integration/BUILDING.md` and `docs/integration/BAREMETAL_FIRMWARE.md` (each die's slot and AEM offset), `docs/diagrams/flash_layout*` (one map per die). |

QSPI: compression first. The 200T's compressed image measured 5,566,832 B, which is 1,372,528 B over the 4 MiB slot. So the 200T keeps its 9,730,652-B uncompressed image in a 10 MiB slot (755,108 B spare), and its AEM region starts at `0xA00000`. The AX7101 map is unchanged: a 4 MiB slot, AEM at `0x400000`. Both boards use the N25Q128A13 (16 MiB, JEDEC `0x20BA18`).

Round 2 answers R841-1 and R842-1 at their cause:

| Finding | Answer |
|---|---|
| R842-1-F1, R1 | Every statement of the 4 MiB slot and the AEM at 4 MiB as universal is scoped to the AX7101. The 200T's 10 MiB slot and AEM at `0xA00000` stand beside it, with the authority that derives them. That covers BUILDING.md (a table of both dies), BAREMETAL_FIRMWARE.md, the QSPI page's AEM caveat and a `build.sh` comment. `BUILD_PARTS` reads `BUILD_DIES`. |
| R841-1-F1 | Gate 1e's 200T arm runs on the 200T map, and `test_layout_from_soch` covers the reconstruction. The reviewer's K7 turns the timing-grade gate red; K9 turns gate 1e and the timing-grade gate red. |
| R841-1-F2 | The guide's "Update a flashed board" step has rc 0 receipts on two 200T image sets, in both directions. The AX7101 comparisons cite the AX7101 release's own reports. |
| R841-1-F3 | The guide and the QSPI page say that a pre-#911 layout is refused as a target, what to do with one, and that the board check has run only against a stub programmer on both boards. The refusal line no longer blames the FPGA when the layout is the cause. |
| R841-1-F4 | Gate 1e plants two disagreeing ID lines and two-device chains; K3 and K4 turn it red. A chain of two equal dies is refused too. |
| R841-1-F5 | Raw per-corner `report_timing_summary` and `report_cdc` of the routed design, read from the image build's checkpoint. |
| R841-1-RS1 | "The JTAG cable is a Digilent FT232H." |

Results:

- **Timing** (`build.sh ax7a200t`, image commit `1e604e1b`, first route, ExtraPostPlacementOpt): every signoff corner meets the floor. Vivado's Design Timing Summary for the routed design gives Slow 0/85 C WNS +0.174 ns and WHS +0.102 ns, and Fast 0/85 C WNS +1.633 ns and WHS +0.036 ns. TNS and THS are 0, and WPWS is +0.264 ns.
- **Utilisation** on `xc7a200t-fbg484-2`: 53,590 LUTs (40.05 %), 54,971 FFs (20.54 %), 19,672 slices (58.81 %), 87.5 BRAM tiles, 15 DSPs, 109 IOBs.
- **check_timing**: no unconstrained internal endpoints, no loops, no unclocked pins.
- **Against the AX7101 release** (its own reports, `b7d69295`): the same 16 clock pairs with the same endpoint counts, classification and inter-clock constraint. The same CDC rules, severities and counts (CDC-10 10, CDC-15 199, CDC-26 121, CDC-6 52, ...). The same 113 used pins in signal, pin name, use, I/O standard and bank. The XDC is byte-identical between the dies.
- **Image**: header part `7a200tfbg484`. `alinx_ax7101.bit` sha256 `b7d7dc4ec9ce9254a089fc99d6699d13eba1b8271ed889d000bded46be64954f` (9,730,856 B). `aem_desc.bin` sha256 `bdfde7cf448ed032ffb1663b0898aeef9ded3bb11b4ead5dc36dfa3df873f180`. `flashboot_layout.json` sha256 `73c2d40e3f3d6ae122b93b71b896abdf75a2f75e9014411b84dced32289a1837`.
- **The image still stands at this head**: both recipes were elaborated at `1e604e1b` and at this head in one clone path. They read the same 150 build inputs: Tcl sources, include directories and init files. Their outputs are identical apart from generated-on stamps. Build C's own inputs match this head's.
- **AX7101**: against `b7d69295` its 150 build inputs and Verilog body are identical. Its `flashboot_layout.json` gains `flash_device` and `flash_jedec_id`, which the flash-device check needs. No bitstream input changes, so it needs no re-route.
- **Guide run**, against a stub programmer that opens no cable:
  - The variant's layout read, `check-images`, `flash-images` and `flash` succeed.
  - "Update a flashed board" succeeds from one 200T image set to the other and back. It writes the AEM at `0xA00000`, then the bitstream at 0, and the readback holds both. The second set is the delivered one with one payload byte changed and rebound, because no second 200T build exists.
  - A 100T board, another flash, a missing escape and the AX7101 recipe on a 200T set are refused, and nothing is written. So is a compressed 200T build on the 4 MiB map, which its own layout refuses.
  - The AX7101 release's pre-#911 set is refused as a target. Its layout, regenerated from soc.h as the guide says, then flashes.
  - The Vivado `write_cfgmem` fallback ran on the image set.

## Authoritative references

- #911 scope and acceptance 1 to 4, with the scope changes in issuecomment-6876968816 and issuecomment-6877123911.
- #818: the +0.030 ns WNS and 0 ns WHS floor at every signoff corner.
- #395: the commercial release timing grade (`TIMING_GRADE`).
- `docs/integration/QSPI_FLASHBOOT.md`, `docs/guides/BOARD_DEPLOYMENT.md`, `docs/integration/BUILDING.md`.
- Reviews R841-1 (issuecomment-6881465909) and R842-1 (issuecomment-6881181571).

## How to get into the same state

```sh
git fetch origin 911-ax7a200t-variant
git checkout 8e523a2b17faf17c4564e5af155b73f95dc2a0a5
git submodule update --init gptp-processor protocol-processor third_party/tsn-c-stack third_party/verilog-axis third_party/lwSRP
```

## How to validate

```sh
python3 scripts/check_sweep_shape.py --self-test
python3 scripts/board_variants.py
python3 scripts/board_variants.py --selftest
python3 sw/builder/test_builder.py --gates test_qspi_owner_transition_completed_write_prefixes
python3 sw/builder/test_timing_grade.py "$(command -v python3)"
python3 sw/builder/test_builder.py --gates test_commercial_timing_grade
sw/litex/build.sh ax7a200t --dry-run
sw/litex/build.sh ax7a200t
```

Run the timing-grade commands with the LiteX environment active.

Expected result / pass criteria: every command exits 0. The build's signoff reports meet +0.030 ns WNS and 0 ns WHS at every corner, and `gateware/alinx_ax7101.bit` carries part `7a200tfbg484`.

## Known limitations / out of scope

- No XC7A200T board is on this bench, so the image has not run on silicon. The colleague is to confirm speed grade -2, the flash JEDEC ID and the JTAG cable, a Digilent FT232H. These are listed in the guide's "What is untested on the XC7A200T".
- The die and flash ID check has run only against a stub programmer, on both boards. The first real AX7101 flash after merge is also its first real run. R841-1 matched its parser against the programmer's own output strings.
- Image sets built before #911 no longer flash through `deploy.sh` as a target. The guide's "Image sets built before #911" gives the three ways forward.
- The board identity (MAC, serial number) is the shipping config's, the same as the bench AX7101's.
- Pre-existing, not fixed here: `python3 sw/litex/qspi_owner_transition.py --self-test` raises `NameError` on dev (#912).
- Pre-existing, not fixed here: BAREMETAL_FIRMWARE.md's slot table calls the journal slots "read and written" by the firmware. The QSPI page says nothing has used them since 2026-08-13.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
