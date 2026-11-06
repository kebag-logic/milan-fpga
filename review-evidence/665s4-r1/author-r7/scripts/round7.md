## Round 7: no silent placeholder image

Relates to #665.

[The assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6689759393) answers [R737-3](https://github.com/kebag-logic/milan-fpga/pull/812#issuecomment-6689752907) and [R738-4](https://github.com/kebag-logic/milan-fpga/pull/812#issuecomment-6689696235), both NEGATIVE at `7643aef613`. Four commits on `7643aef613`, with no rebase and no force. No RTL and no firmware C changes. `split_soc.py` and `ctrl_runs.py` are untouched.

| Commit | Change |
|---|---|
| `7a20a67a0e` | `ctrl_plat_image.py` refuses a link with no `--flash-map`, before it compiles. `ctrl_image_selftest.py` tests the refusal. Both documented link commands carry the map, and the platform page says where it comes from. |
| `154fe81188` | `boot_soc.build`'s refusal moves into `refuse_deviation`, unchanged in behaviour, and `ctrl_split_boot/run.py` gains the placement controls and two planted defects of that refusal. |
| `c2befb12d1` | The two pages give the gated receipt's 13.861 ms. |
| `37e0393094` | The pages that list the self-tests name what they now hold: the image self-test's 37 checks, and the placement controls. |

| Finding | Severity | Outcome |
|---|---|---|
| R737-3-F1, R738-4-F1 | MINOR, MAJOR | A link with no map is refused by name. The page's command carries the map. Round 7's item 1, below. |
| R738-4-F2 | MINOR | `nvm_split_target/README.md:158` and `ctrl_nvm/README.md:338` give 13.861 ms. The body's three lines are restated. `rg '13\.863'` finds it only in `SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, where that page records history. |
| R738-4-F3 | MINOR | `run.py --placement-controls` is the committed negative test, and it runs last in `--self-test`. |
| R737-3-R1, R737-3-R2, R738-4-RES2 | RESIDUE | Applied, because the same lines had to change: the docstring's lane label and the help text's possessive in `ctrl_plat_image.py`. |

### Item 1: what a link without a map does now

The refusal reads `REFUSED: no --flash-map: a split platform image is never linked on the flash port's RV32 stand-ins; gen_flash_port.py writes the map from the split SoC's export`, exit 2. It fires before anything compiles, whenever at least one runtime archive exists.

The boundary gate's compile is the one run it leaves alone. That run's archives both do not exist, so it compiles every object, then stops at its link with `No such file` and makes no ELF, so `ctrl_runs.stopped_at_link` stays true for it with `ctrl_runs.py` unchanged.

`gen_flash_port.py` takes only the product split export. The boot SoC's export has no part size or journal to give it, so the page names `milan_soc.py --ctrl-mailbox --ctrl-firmware` as `$SOC`.

**Neither review listed this:** `docs/design/SPLIT_CONTROL_MEMORY.md:319` is a second documented `ctrl_plat_image.py` link with no map. It would now be refused as written, so it carries the map too.

**Not changed:** `ctrl_srp_image.py --layout split --with-aecp` still links its size fixture on the stand-ins when given no map, and the design page documents that command. The fixture is a separate builder and not a booted image (`sw/firmware/ctrl/README.md`), and `build.flash_map` needs that image to make the first export the map is read from. Refusing it would break the map's own generation, so it is left to a maintainer to say if the ruling's "any split image" reaches it.

### Verification

The reviewer's `nomap_probe.sh`, unedited, now prints `no-map link rc=2` and the refusal, and no ELF exists.

Each page's command was taken from the page's own `sh` fence and run unedited at this head:

| Page | Exit | Stand-in timer (`lui 0xf0004`) in `ls_*` | Stand-in window (`lui 0x20000`) in `ls_*` | Plan |
|---|---:|---:|---:|---|
| `sw/firmware/ctrl/plat/README.md`, 1x1 | 0 | 0 | 0 | 39.0 tiles, `rom` 109,552 B |
| `docs/design/SPLIT_CONTROL_MEMORY.md`, 8x8 with two interfaces | 0 | 0 | 0 | 59.0 tiles, ledgered, `rom` 125,040 B |

The scan can fail: on a no-map image linked at `7643aef613` it finds `lui 0xf0004` four times and `lui 0x20000` once, in the functions the reviews name. The map the plat page's generator line writes equals the run's `split-soc/flash-map`.

The S3 figures do not move: 84.372 ms and 4,218,617 CPU cycles at 1x1, 184.622 ms and 9,231,088 at 8x8, 18 of 18 writes at each.

The `rom` figures are 8 bytes under `SPLIT_CONTROL_MEMORY.md` section 5's rows, which are labelled as measured at `b8628704` on no-map images (R737-3-S3). Tiles are unchanged, so those rows are left as they are.

### New checks and their mutants

Each mutant was planted literally in a scratch clone of this head, one at a time, and each check is green with no mutant.

| Check | Planted defect | Its words |
|---|---|---|
| `ctrl_image_selftest.py`, plat | the refusal's call removed | `AssertionError: ('both archives', 'collect2: error: ld returned 1 exit status')` |
| `ctrl_image_selftest.py`, plat | `any` archive changed to `all` | `AssertionError: ('the C library alone', ...` |
| `ctrl_image_selftest.py`, plat | refused even with a map | `AssertionError: REFUSED: no --flash-map: ...` |
| `ctrl_runs.stopped_at_link` | refused with no archives as well, so the boundary gate's compile cannot run | `exit 2; ELF present False; stopped_at_link False` |
| `run.py --placement-controls` | `refuse_deviation`'s call removed from `build` (R738-4's `boot_soc.py:96-98`) | `PLACEMENT export-refuses: WRONG (export TAKEN)` |
| `run.py --placement-controls` | the `raise` removed | `PLACEMENT export-refuses: WRONG (export TAKEN)` |
| `run.py --placement-controls` | `map_deviations` returns empty | `PLACEMENT register-moved: WRONG (deviations [])` |
| `run.py --placement-controls` | the window comparison removed | `PLACEMENT window-moved: WRONG (deviations [])` |
| the boot itself | the guard refuses a true map | `RuntimeError: the boot SoC does not place the flash port's devices as the split SoC does: []`, exit 2 |

The two planted defects are also in the tree (`GUARD_PLANTS`), so every `--self-test` shows that the export control can fail: `PLANT guard-removed: caught` and `PLANT deviations-empty: caught`.

The placement controls need the product LiteX tree, because `split_soc` imports it, so they are not portable and no hosted job runs them (R738-4-S2 stands). A portable check of `map_deviations` would need that function moved out of `split_soc.py`, which S2's and S4's harnesses share, so it was not done here.

### Gates

GATES_TABLE

### What this round did not run or change

- The 97 short gates, the other long gates, S2 and S4 at either point, and the D5 plant: the assignment's gates are those the delta touches, and nothing they read changed. `split_soc.py`, the firmware C and the RTL are unchanged.
- No sweep and no Vivado route: RTL is unchanged.
- R738-4-RES1, R738-4-RES3 and the retained residue: not in the assignment, so they stay on the checklist.
- The two open questions stand: the gate environment's SDK, and an owner for S2's 8x8 page. This round's figures were measured with that same SDK.
