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

GREEN -- 150/150 workflow steps rc 0 (522 not run with a reason), 65/65 Verilator suites -- `911-ax7a200t-variant` -> `dev`, head `4958ca4f` on dev `b7d69295`.

## Linked Issue / roles

Closes #911

Executor: `[A782]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

The XC7A200T variant of the ALINX board: the AX7101's 1x1 TDM8 shipping shape, built for `xc7a200t-fbg484-2`.

| Piece | Change |
|---|---|
| `sw/litex/build.sh` | `cfg_ax7a200t` is `cfg_ax7101` plus `--fpga-part xc7a200t-fbg484-2`; `recipe_config` binds it to `configs/endstation_ax7101_1x1_tdm8.yaml`; `board_facts` gives it the programmer part `xc7a200tfbg484`. |
| `sw/litex/platforms/` | `BOARD_PARTS` and `board_part()` in `ax7101_timing.py`; `configure_commands(part)`; `alinx_ax7101.Platform(part=)`. Pins and constraints stay in the one platform file. |
| `sw/litex/milan_soc.py` | `--fpga-part` (refused with `--board arty`); `FLASHBOOT_BITSTREAM_SLOT` moves the 200T's AEM region to `0xA00000`; the layout records `flash_device` and `flash_jedec_id`. |
| `sw/litex/flash_map.py` | `layout_for()`, the one statement of the slot rule; `load_map(part)`. |
| `sw/litex/layout_from_soch.py` | Bitstream budget from the compiled AEM offset; flash device from soc.h through litespi. |
| `sw/litex/qspi_owner_transition.py`, `deploy.sh` | `check-board`: before the first dump or write, `flash`, `flash-images` and `flash-pair` read the JTAG die and the flash JEDEC ID and refuse a mismatch with the image set. |
| `scripts/check_sweep_shape.py` | `BUILD_PARTS`: `--fpga-part` allowed on `ax7a200t` only, two plants. |
| `scripts/board_variants.py` | New: the guide's board variant table is checked against `build.sh`, the flash map and the SoC's flash module, with six mutation controls; `--layout` checks a built layout. |
| `sw/builder/test_builder.py`, `test_timing_grade.py` | Gate 1e: the fake programmer answers `--detect`; refusal arms on all three paths; the 200T named path. Gate 24d's anchor follows the new platform line. The timing-grade gate runs `test_board_parts` and `test_board_variant_docs`. |
| Docs | `docs/guides/BOARD_DEPLOYMENT.md` (variant table, "Flash an image set over JTAG", `INSTALLED_BUILD`, what is untested), `docs/integration/QSPI_FLASHBOOT.md` (the variant's layout), `docs/integration/BUILDING.md`, `docs/diagrams/flash_layout*` (one map per die). |

QSPI: compression first. The 200T's compressed image measured 5,566,832 B, which is 1,372,528 B over the 4 MiB slot. So the 200T keeps its 9,730,652-B uncompressed image in a 10 MiB slot (755,108 B spare), and its AEM region starts at `0xA00000`. The AX7101 map is unchanged. Both boards use the N25Q128A13 (16 MiB, JEDEC `0x20BA18`).

Results:

- **Timing** (`build.sh ax7a200t`, image commit `1e604e1b`, first route, ExtraPostPlacementOpt): every signoff corner meets the floor. Slow 0/85 C: WNS +0.174 ns, WHS +0.102 ns. Fast 0/85 C: WNS +1.633 ns, WHS +0.036 ns. TNS and THS 0, WPWS +0.264 ns.
- **Utilisation** on `xc7a200t-fbg484-2`: 53,590 LUTs (40.05 %), 54,971 FFs (20.54 %), 19,672 slices (58.81 %), 87.5 BRAM tiles, 15 DSPs, 109 IOBs.
- **check_timing**: no unconstrained internal endpoints, no loops. Clock interaction and CDC categories match the AX7101 release.
- **I/O**: all 113 used pins match the AX7101 release in pin name, bank, I/O standard and use.
- **Image**: header part `7a200tfbg484`. `alinx_ax7101.bit` sha256 `b7d7dc4ec9ce9254a089fc99d6699d13eba1b8271ed889d000bded46be64954f` (9,730,856 B). `aem_desc.bin` sha256 `bdfde7cf448ed032ffb1663b0898aeef9ded3bb11b4ead5dc36dfa3df873f180`. `flashboot_layout.json` sha256 `73c2d40e3f3d6ae122b93b71b896abdf75a2f75e9014411b84dced32289a1837`.
- **AX7101**: `build.sh ax7101` was elaborated at `b7d69295` and at this branch. Its 140 build inputs, Verilog body, constraints, Tcl, ROM/RAM init and generated headers are identical; only timestamps and LiteX's hierarchy comment differ, and those also differ between two elaborations of one commit. Its `flashboot_layout.json` gains `flash_device` and `flash_jedec_id`, which the flash-device refusal needs. No bitstream input changes, so it needs no re-route.
- **Guide run** (stub programmer, no cable opened): the variant's layout read, `check-images`, `flash-images` and `flash` succeed; a 100T board, another flash, a missing escape and a wrong recipe are refused, and nothing is written. The Vivado `write_cfgmem` fallback ran on the image set.

## Authoritative references

- #911 scope and acceptance 1 to 4, with the scope changes in issuecomment-6876968816 and issuecomment-6877123911.
- #818: the +0.030 ns WNS and 0 ns WHS floor at every signoff corner.
- #395: the commercial release timing grade (`TIMING_GRADE`).
- `docs/integration/QSPI_FLASHBOOT.md`, `docs/guides/BOARD_DEPLOYMENT.md`, `docs/integration/BUILDING.md`.

## How to get into the same state

```sh
git fetch origin 911-ax7a200t-variant
git checkout 4958ca4f630da1f715bdcd78113b798bbe332b81
git submodule update --init gptp-processor protocol-processor third_party/tsn-c-stack third_party/verilog-axis third_party/lwSRP
```

## How to validate

```sh
python3 scripts/check_sweep_shape.py --self-test
python3 scripts/board_variants.py
python3 scripts/board_variants.py --selftest
python3 sw/builder/test_builder.py --gates test_qspi_owner_transition_completed_write_prefixes
python3 sw/builder/test_timing_grade.py "$(command -v python3)"
sw/litex/build.sh ax7a200t --dry-run
sw/litex/build.sh ax7a200t
```

Expected result / pass criteria: every command exits 0. The build's signoff reports meet +0.030 ns WNS and 0 ns WHS at every corner, and `gateware/alinx_ax7101.bit` carries part `7a200tfbg484`.

## Known limitations / out of scope

- No XC7A200T board is on this bench: the image has not run on silicon. The colleague confirms speed grade -2, the flash JEDEC ID and the JTAG cable (the guide's "What is untested on the XC7A200T").
- The board identity (MAC, serial number) is the shipping config's, the same as the bench AX7101's.
- Pre-existing, not fixed here: `python3 sw/litex/qspi_owner_transition.py --self-test` raises `NameError` on dev (`sw` is undefined in `self_test`); no workflow runs it. It needs its own issue.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
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
