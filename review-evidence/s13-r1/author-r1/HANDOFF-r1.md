# HANDOFF, round 1: the Mark II split FLIP PR (#665), [A815]

## Status (00:4x, 2026-11-22, 2026-11-21): READY FOR REVIEW AT `62477be4`. NO STOP: BOTH IMAGES CHANGE ONLY IN THE VERSION WORD, THE FIRMWARE STRING AND THE INTEGRITY WORDS COMPUTED OVER THEM. EVERY OWNER BOUND HOLDS; THE FLOOR IS MET; EVERY GATE PASSES BUT THE RECORDED ENVIRONMENT ROWS

- Branch `s13-flip-default`, 16 commits on dev-soft-core `59b09884` (local; nothing pushed). Base = the remote
  dev-soft-core tip (checked with `git ls-remote` at the start: `59b09884`).
- Public: TAKEN #665 issuecomment-7065258935 (`receipts/public/`); REVIEW READY: #665 issuecomment-7070924358 (`receipts/public/review-ready-7070924358.md`).
- Scratch `<scratch>` (outside this directory). Receipts: `receipts/`, indexed in `receipts/INDEX.md`.
- No unit of this lane is running at the handoff (every unit of this lane has ended; the scratch keeps the clones, builds and dumps).

| Commit | What |
|---|---|
| `822e3af0` | The image-affecting change: the AX7101 configs at `control.placement: split`; a split image's VERSION `0x0003_0060` (firmware 3.96.0), all-fabric `0x0002_0060` |
| `9eeff00a` | The split datapath leg pins VERSION and major 3, with a planted defect; the all-fabric major 2; the split stand-ins at `0x0003_0060`; the UART grader's major 2 or 3 |
| `d72a91e9` | Builder gates 23m, 23n, 23o for the split-shipping configs; the entity-shape gate per placement with a plant; the AX7101 sweep fragment regenerated |
| `4dd3c1fd` | `build.sh`'s `BUILD_PLACEMENT` (the all-fabric release image's one launch) |
| `9817d008` | The identity gate reads a manifest's VERSION at the claimed (split) placement |
| `6eef968e` | Docs, feature ledger, generated register map, changelog, documentation inventory |
| `f7139ce1` | The platform console test expects the split stand-in's VERSION |
| `51966e13` | The UART grader's arms name their failures; the ledger checker within the module ratchet; gate 23o's ROM control within the column ratchet |
| `e1f3863e` | The split leg's VERSION arm renamed (its scratch path cannot carry `#` to make) |
| `bfdb5a2d` | The clock-constraint probe elaborates the split at both shapes and the all-fabric release; the census reads each config's all-fabric build; the control-memory SoC cases start from the all-fabric argv; `sweep.sh`'s AX7101 row carries the split; the sweep-shape plant re-anchored |
| `15db681a` | `test_ctrl_memory.py` back within the module ratchet |
| `ec1cc8de` | Builder gates 1e and 23g (and their controls) take the synthetic split image wherever a shipping launcher names the split's |
| `a18d3148` | Gate 24 per placement and the model id across both; gate 25c's 1.1.0 rendition with its own image path; the key map names `control.placement` |
| `ee4c1a9c` | Gate 24's ENTITY+116 expectation per config |
| `80af65ef` | Gate 24's RTL read in one helper (the long-function ratchet) |
| `62477be4` | `#665` alone, without the lane label, in every source comment, message and the register-map text they generate |

## Authoritative references read

- NFR-SCOUT-02 (`docs/reference/FR_NFR.md` 3.4); `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 7 (major 0x0003 only for
  split images, all-fabric keeps its identity, MINOR flat, the version chain and its five simulations).
- Flip plan item 6 (issuecomment-6799253003). Owner decisions issuecomment-6410301079 (the flip changes only the
  default and sets VERSION major 3; all-fabric stays buildable and gated), -6845315282 (8x8/1if a must; 2if
  optional, #890/#810), -6930885185 (#818's floor: +0.030 ns setup, 0 ns hold, best of three directives),
  -7044585511 (the 1x1/1if rows), the bench re-check -7063917242 (`c7189218`, `7d903412`; #954 after the flip).

## Changes (file:line, reason)

- `hdl/common/csr/milan_csr.sv:208` `VERSION_SPLIT_MAJOR = 16'h0003`, `:212` `CTRL_SPLIT_P`, `:2002` `VERSION_C`,
  `:2011` `csr_default` reads it: a split image's VERSION is `{0x0003, VERSION[15:0]}`; the minor is stated once.
  VERSION reaches the fabric only as the defaults ROM's word for 0x004 (`dflt_rom`, `:2120`, a block RAM).
- `hdl/milan/milan_datapath.sv:2850` passes `CTRL_SPLIT_P` to `milan_csr`: the placement selects VERSION's major only.
- `avdecc/aem_descriptors.py:52,59,94` `rtl_version`/`firmware_version_string` take the placement (one source).
- `sw/builder/endstation_builder.py:3270,3290,3824,4595,4572`: the firmware string at the config's placement, and
  `with_placement` re-derives it; `:6252` any `--placement` recipe refuses `--write-rtl`/`--write-fragment`, so the
  tracked fragment follows the config's own placement.
- `configs/endstation_ax7101_1x1_tdm8.yaml:75`, `configs/endstation_ax7101_8x8.yaml:98`: `control: {placement: split}`.
  The Arty configs stay all-fabric (the bench gate covered only the AX7101 shapes).
- `sw/litex/milan_soc.py:3071` the manifest's VERSION is the split one; `sw/litex/check_image_identity.py:153` the
  expected VERSION follows the claimed placement (the placement rule holds the datapath to it).
- `sw/litex/build.sh:29,327` `BUILD_PLACEMENT=all-fabric ./build.sh ax7101` (the builder's recipe): the release image.
- `configs/generated/sweep_opts_ax7101.sh` regenerated (`--write-fragment`, the 1x1 config owns it); `sw/litex/sweep.sh`
  AX7101 row carries the split; `deploy.sh` sources the fragment.
- Tests: `tb/verilator/milan_dp/sim_split.cpp` `check_identity` (ID, VERSION, major 3) with `split_mutants.py`'s arm;
  `sim_main.cpp` the all-fabric major 2; the split stand-ins (`ctrl_split_boot`, `ctrl_reboot`, `ctrl_service_hooks`,
  `plat_bus.hpp`, `test_plat.cpp`) at `0x0003_0060`; `baremetal_uart_smoke.py` major 2 or 3; builder gates 1e, 23g,
  23m-23p, 24, 25c; `check_entity_shape.py` (+ plant 7b); `check_feature_status.py` (+ 2 plants);
  `check_sweep_shape.py` (plant re-anchored); `test_shipping_clock_constraints.py` (split at both shapes, all-fabric
  release); `census_elab.py` (all-fabric build); `test_ctrl_memory.py` (all-fabric base).
- Docs: the "which placement ships" sentences (README, REQUIREMENTS section 1 and its VERSION paragraph, FR_NFR 1.2,
  ARCHITECTURE_HW_SW_SPLIT top and section 7, MAILBOX_SPLIT, nine page banners, design pages), the ledger
  (`gateware.current-version` `0x0003_0060`, its source tie `VERSION_SPLIT_MAJOR` over the minor, 8 rows), the
  register map generator (the record's placement, the split VERSION), CHANGELOG, BUILDING.md, ENDSTATION_BUILDER 34a,
  CSR notes; the documentation inventory retires D0-001/033/056 (the default they contradicted is now the split).

## New checks (planted mutant, failing words)

| Check | Planted defect | Refused with | Receipt |
|---|---|---|---|
| `sim_split.cpp` `check_identity`: the split datapath's ID, VERSION `0x0003_0060`, `VERSION >> 16 == 3` | `split_mutants.py` arm "a split datapath whose CSR keeps the all-fabric VERSION" (`.CTRL_SPLIT_P(0)` on `milan_csr`) | "caught by [ID] the split datapath reads VERSION major 0x0003 (VERSION >> 16)"; full set 32 of 32 | `checks/split-mutant-arm-e1f3863e.log` |
| `milan_dp/sim_main.cpp`: all-fabric `VERSION >> 16 == 2` beside the full word | (the full-word check beside it refuses any major change too) | - | `sweep/rerun-milan_dp.txt` |
| `check_entity_shape.py`: the string at each config's placement and at both recipes | plant 7b: `VERSION_SPLIT_MAJOR` moved to `0x0004` | "endstation_arty_4x4: firmware_version at the split recipe: got '3.96.0', expected '4.96.0'" | docs workflow, self-test |
| `check_feature_status.py`: the current version is `VERSION_SPLIT_MAJOR` over `VERSION`'s minor | "source split major drift", "source split major missing" | "gateware version conflict"; "cannot locate VERSION and VERSION_SPLIT_MAJOR parameters" | self-test 48/48 |
| Builder gate 23n: the AX7101 configs split, the rest all-fabric | the flip reverted at 8x8 | "ax7101_8x8: a tracked config is {'placement': 'all-fabric'}, not split" | builder suite |
| Builder gate 23o: both recipes; shape artifacts equal but for `firmware_version` | a ROM byte past the field; an overlay name; an unchanged overlay; a recipe leaving the config's own placement | the gate's assertion words; "differs from the file stating the key" | builder suite |
| Builder gate 24: the string per placement; the model id the same at both | (the bad-declaration arms as before) | - | builder suite |
| `baremetal_uart_smoke.py`: major 2 or 3, minor >= 0x0056 | the old rule (`== 2`) in a scratch copy; arms 0x00030055, 0x00040056 | "AssertionError: a split image's VERSION major 3 was refused" | `checks/uart-grader-planted-major2-only.txt` |
| `endstation_builder.build`: any `--placement` recipe refuses `--write-rtl`/`--write-fragment` | gate 23o drives both placements with both flags | "the placement recipe writes no tracked file" | builder suite |
| `check_image_identity.py`: a manifest's VERSION at the claimed placement | gate 23p's "split datapath built without CTRL_SPLIT_P" | refused by the placement rule again | builder suite |

## Image identity (item 3): NO STOP

- 1x1/1if (`68e5308b`, the gating recipe at `822e3af0`, ExtraPostPlacementOpt, 16 threads like the bench) against
  `c7189218`: same length and packet structure; 103 bytes differ: 77 in the `.bit` header's `SW_CRC`/`SW_HDR_SHA256`
  text, 4 in the configuration CRC word, 22 bits in 7 of 9,464 frames. All 121 Vivado phase checksums equal; the
  checkpoints hold all 95,172 routes and all 86,465 cells (type, LOC, BEL) equal; 8 block RAMs hold the 22 bits: the
  CSR defaults ROM 1 (VERSION), ROM bank 1 20 (words 2198-2199: the AEM image's CRC32 `0x38a80323` -> `0xdb1deab5`,
  a `lui`/`addi` pair), ROM bank 3 1 (word 46: `'2'` -> `'3'`). Signoff equal to the bench's to the picosecond.
- 8x8/1if (`6a1ff1ef`) against `7d903412`: 93 bytes: 74 header, 4 CRC word, 15 bits in 7 frames; all 149 phase
  checksums equal; the 111 block RAMs at the same sites, 14 holding the 15 bits (CSR defaults ROM 1, ROM bank 0 13
  at words 18563-18564 and 1 at word 28702). Signoff equal to the bench's.
- Firmware at both points: 6 loaded bytes (the string, its CRC); layout equal.
- Inputs carried: the images' inputs at `62477be4` equal the `822e3af0` build's (19 and 16 compared), so these are the
  head's images. The RTL and config edits after `822e3af0` are comment-only.
- For review: the AEM CRC32 is not itself a version field; it is the integrity word of the descriptor image that
  carries the string, as the configuration CRC and the header digests are the bitstream's. Nothing else changes.

## Gate table

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| Image identity, 1x1/1if | `gchain.sh`; `bitdiff.py`, `elfdiff.py`, `dump.tcl` | `822e3af0` (inputs = `62477be4`) | version fields and their integrity words only | `identity/1x1/` |
| Image identity, 8x8/1if | same | `822e3af0` (inputs = `62477be4`) | same | `identity/8x8/` |
| Timing floor (#818), best of three | `gchain.sh` x 6, `signoff.py` | `822e3af0` (inputs = `62477be4`) | best of three met at every corner: 1x1/1if ExtraPostPlacementOpt +0.131/+0.102, +1.636/+0.036 ns; 8x8/1if ExtraPostPlacementOpt +0.176/+0.102, +1.523/+0.036. ExtraTimingOpt 1x1/1if +0.002 (0.028 under the setup floor alone), 8x8/1if +0.059; AltSpreadLogic_high +0.046, +0.150 (all WHS +0.102/+0.036) | `identity/TIMING.md`, `identity/<point>/signoff-*.txt` |
| Release (all-fabric) export | `release_export.sh`, `cmp_export.py` | `59b09884` / `f7139ce1` | every loaded file equal; Verilog equal outside comments; argv equal | `release/` |
| Flip check | `flip_grade.py --check --point 1x1/1if`, `--point 8x8/1if`, `--check` | `bfdb5a2d` (+ `62477be4` quick list) | PASS, PASS; all points rc 1 at 8x8/2if (reported, not held), byte-identical to base | `flip/` |
| Load grade | `load_grade.py --check` | `bfdb5a2d` | PASS | `flip/` |
| Firmware gate | `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4` | `f7139ce1` (inputs unchanged after) | rc 0 x 4 | `gates/` |
| Sweep | `native-shards.py` 4 shards; 14 wall-clock kills rerun alone | `15db681a` | 65 of 65 suites pass, 0 failures | `sweep/SUMMARY.txt`, `sweep/reruns.txt` |
| Builder suite | `test_builder.py --require-rv32 --require-elaboration` | `ee4c1a9c`; `62477be4` | ALL GATES PASS EXCEPT 2 NOT RUN (recorded) | `gates/builder-suite-*.log` |
| Docs workflow | the 103 commands | `62477be4` | 99 pass; 4 CI-environment rows, as the train's | `gates/docs-workflow-62477be4.txt` |
| Quick list | 58 commands (harness model checks, generators, idioms, census, shape gates) | `62477be4` | all pass but the all-points flip check (8x8/2if, reported) and the CI-environment tool inventory; `run.py --self-test` 0 failures | `gates/quick-62477be4.txt` |
| Split boot | `ctrl_split_boot/run.py` x 2 shapes | `15db681a` | PASS x 2 | `gates/split-boot-*` |
| Twin, plants, maps, rxmon | campB | `15db681a` | rc 0 | `gates/campB-15db681a.log` |
| ctrl_boundary, plat ledger | campC | `15db681a` | PASS | `gates/campC-15db681a.log` |
| Split CDC, parallel, mutants | `make split-cdc`, `split_parallel.py`, `split_mutants.py` | `ee4c1a9c` | rc 0, rc 0, 32 of 32 | `gates/splitjobs-ee4c1a9c.log` |
| BDD, xvlog, Yosys | `behave`; `xvlog_gate.py`; `run.sh --shard k/4` | `15db681a` | 2346 steps; PASS; rc 0 x 4 | `gates/` |
| CPU-budget harness | `hbuild.sh` + `elfdiff.py`; `hsubset.sh` + `hcompare2.py` | `f7139ce1` | 16 images differ in the same 6 bytes; 13 of 13 descriptor groups identical leaf by leaf | `budget/` |
| Carry | scoped `git diff` | `62477be4` | nothing a firmware, harness or image run reads changed after its head but comments | `gates/carry-*.txt` |

## Open questions / decisions

1. NFR-SCOUT-02 and REQUIREMENTS section 1 tie the processor's deletion to "the switch-over". This PR follows
   issuecomment-6410301079 and the task: the flip changes the default; deletion waits for the full qualification.
   REQUIREMENTS section 1 is restated to that order; the normative NFR-SCOUT-02 row is unchanged. For the owner.
2. The full CPU-budget re-measure (64 parts a point) was stopped: at host load ~190 it needed 8-12 h more. Measured
   instead: the descriptor groups and `control` at both points, identical. The full run is owed if reviewers want it.
3. The register map keeps its recorded all-fabric SoC export (now stated); re-recording from a split export
   restates its memory map and the 0x920 window. Follow-up.
4. Not gated and left: `syn/resmap/soc_sweep.py` reads the base config's argv (now the split's); the harness appends
   the split flags to an argv that carries them (argparse takes its own image; images verified); the
   BUILD_FLASH_BOOT diagram describes the all-fabric BIOS flow.
5. CPU bookings: `cpu_ranges.py pick` had no free range most of the session; units ran on the shared session pool
   64-95 by CPU weight (the train's practice), and on booked ranges when one freed (8-15, 40-47, 48-55).
