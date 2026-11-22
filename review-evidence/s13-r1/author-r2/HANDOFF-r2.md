# [A815] round 2 handoff: PR #960 (#665 S13), correction round

Status: DONE. REVIEW READY posted on #665 as issuecomment-7072252167 (`receipts/public/`), last line "REVIEW READY 9413958c". No unit of this lane is running; the worktree is clean at `9413958c`.

- Base of the round: `62477be4` (round 1's head, PR #960's head as the manager pushed it).
- Reviews answered: R880-1 (issuecomment-7071145133, NEGATIVE) and R879-1 (issuecomment-7071300727, NEGATIVE).
- Branch `s13-flip-default`, local; the manager pushes. Final head `9413958c66c0dcd632b3e0e7ac44505314fed41a`.
- Commits this round (one-line subjects, no body, no trailers):

| Commit | Answers | What |
|---|---|---|
| `59f91d9f` | R880-1-F1 | the resource sweep prices the placement its plan names (all-fabric) and refuses, before any export, an argv naming an absent platform image |
| `bc5a947d` | R879-S1 | the CPU-budget harness replaces the split config's image pair instead of appending a second |
| `e4dd762a` | R879-F1 | the register map labels its memory map and build parameters as the recorded all-fabric build's |
| `530cdbf9` | R879-F2 | the README's pipeline picture is labelled the all-fabric release flow; the split build is stated beside it |
| `2f985971` | R880-1-F4, R880-1-R1, R879-R1 | the identity paragraph states gate 23o's exception; stale "all-fabric ships" labels retired |
| `a9da4c48` | R880-1-F1 | the sweep's self-test reports a plan with no placement by name, not by traceback |
| `9413958c` | (generated) | the documentation audit regenerated for the README paragraph (the docs inventory gate asked for it) |

## Finding table

| Finding | Severity / lens | Cause | Fix | Test: planted defect -> failing words | Receipt |
|---|---|---|---|---|---|
| R880-1-F1 | MAJOR Robustness, Tests | `soc_sweep.prepare()` built the base config at its own placement; the flip made that the split, whose argv names `sw/builder/out/<cfg>/ctrl_app.elf`, which nothing in the sweep builds | `59f91d9f`, `a9da4c48` | plan placement `split` -> "the plan prices the split SoC, not the all-fabric one its recorded figures were taken at"; key removed -> "the plan: the soc section names no control placement"; `missing_images` returning [] -> "an absent platform image: missing images [], want ['sw/builder/out/cfg/ctrl_app.elf']". Real runs: reproduction at `62477be4` (ship, axilite rc 1, FileNotFoundError); at `a9da4c48` a clean export with 0 platform images: ship and axilite accepted, the six refusals kept; the control (a plan copy naming split) refused before any export, naming the image, no export written; ship/axilite against base: argv equal, gateware equal but Verilog comments and the XDC's clock-group order | `f1/`, `gates/plants-9413958c.txt` |
| R880-1-F2 | MAJOR Conformance, Tests, Docs | round 1 published the comparison's hashes and results, not its operands | evidence | `identity/plants.txt`: 11 defects planted in copies of the operands, each refused by the replay | `identity/` |
| R880-1-F3 | MINOR Tests, Docs | round 1 parsed only the design-name string and counted the date and time fields' bytes into it | evidence | the replay names each byte by header field | `identity/replay-output.txt` |
| R880-1-F4 | MINOR Tests, Docs | the identity paragraph kept "byte for byte" when gate 23o gained its firmware_version exception | `2f985971` | doc; checked against `test_builder.py` RECIPE_VERSION_ARTIFACTS | - |
| R880-1-R1 | RESIDUE Docs | three pages kept "all-fabric is the shipping build" | `2f985971` | the reviewer's wording | - |
| R879-F1 | MINOR Docs | `register_page.py` named the recorded all-fabric export "the shipping SoC/build" | `e4dd762a` | `gen_register_reference.py --check` fresh, `--selftest` 61/61, doc style OK | `gates/docswf-9413958c.txt` |
| R879-F2 | MINOR Docs | `BUILD_FLASH_BOOT.gen.py` drew `build.sh ax7101` with the pre-flip boot and VERSION | `530cdbf9` | svg, drawio and png regenerate byte-identical | `gates/round2-checks-a9da4c48.txt` |
| R879-R1 | RESIDUE Docs | the compliance matrix said "before the default changes" | `2f985971` | the reviewer's wording | - |
| R879-S1 | SUGGESTION Tests, Robustness | the harness appended `--ctrl-mailbox --ctrl-firmware <image>` to an argv that already carries the config's pair | `bc5a947d` | `split_argv` appending (the old behaviour) -> "endstation_ax7101_1x1_tdm8: the split SoC argv names the harness image once, after the all-fabric argv: [..., '--ctrl-firmware', 'sw/builder/out/...', '--ctrl-mailbox', '--ctrl-firmware', 'x.elf']"; keeping the config's image -> the same check, both shapes | `s1/`, `gates/plants-9413958c.txt` |

## Changes (file:line, reason)

- `syn/resmap/sweep_plan.json:72` `"placement": "all-fabric"`, and the section's description: the #649 figures were recorded on the all-fabric SoC; the plan names the placement so a later default cannot move it.
- `syn/resmap/soc_sweep.py:65` `plan_placement`, `:73` `missing_images`, `:104` `prepare(work, placement)` passes `--placement` to the builder (`:112`) and refuses an argv naming an absent image (`:117`); `:341` the CLI prints the refusal; `:289-310` the self-test arms (plan placement, a plan with none, an absent image, a flag with no value, an all-fabric argv, an image present).
- `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:129-130`: the placement the SoC options are priced at, and the refusal.
- `tb/verilator/ctrl_service_budget/build.py:355` `split_argv`, `:382` `soc_export` uses it; `selftest.py:731-759` the check at both shapes (`:756`); `README.md:414`.
- `scripts/register_page.py:31` `SPLIT_MAP`, `:519`, `:521`, `:652-654`, `:714`, `:720`; `scripts/gen_register_reference.py:20`, `scripts/register_read_sweep.py:151` docstrings; `docs/reference/REGISTER_MAP.md:27`, `:29`, `:154-157`, `:248` regenerated.
- `docs/BUILD_FLASH_BOOT.gen.py:5`, `:22`, `:90-96`, `:205` and the rendered `.svg`, `.drawio`, `.png`; `README.md:298-313`.
- `docs/design/MAILBOX_SPLIT.md:5`, `:626`, `:1804-1813` (F4), `:2118-2119`; `docs/overview/ARCHITECTURE.md:4`, `:19`; `docs/overview/FULL_FPGA_SOLUTION.md:3`, `:19`; `docs/reference/MILAN_COMPLIANCE_MATRIX.md:6-7`; `docs/DOCUMENTATION_AUDIT.md` regenerated.
- Not changed, on evidence: `syn/resmap/yosys_sweep.py`. Its datapath points bind the plan's parameters (no `CTRL_SPLIT_P`, so 0, all-fabric), and its `shapes` step gives the same outcomes and generated shapes at base and at `62477be4` (`f1/yosys-shapes-59b09884-vs-62477be4.txt`).

## The identity packet (R880-1-F2, F3)

`receipts/identity/`: the operands, `binding.json`, `tools/replay.py` (standard library only) and its recorded output, `plants.txt`, `MANIFEST.sha256`. Replay: `cd identity && python3 -I tools/replay.py .`.

- Shipping pairs, both shapes: the four `.bit`, the four platform ELFs, every ROM bank init, the export files, and the routed checkpoints' full cell and net dumps (xz), plus round 1's 8x8 block RAM dump. The checkpoints (75-93 MB) are named by sha256 only.
- The 16 harness image pairs with their group partitions; the 13 groups' result JSON and raw simulation logs, measured and re-measured.
- Bindings: the bench images hash to the bench re-check's published `c7189218`/`c873a0aa`, `7d903412`/`d67fd049`; the flip images to round 1's. Every measured harness image is byte for byte the harness build at the bench head `8c5e2b4f` (the 8x8/1if measurement ran at `92de01f7`), and every head image the build at `a9da4c48`. The flip images' 19 and 16 inputs are equal at `a9da4c48`. `a9da4c48` -> `9413958c` changes only `docs/DOCUMENTATION_AUDIT.md`.
- Result: see `identity/README.md`; every claim holds. Nothing differs beyond the stated fields, so no STOP and no full CPU re-measure.
- Corrections to round 1, both found here: (1) F3's header split (71+6 and 69+5, now named: date and time); (2) round 1's group driver skipped string leaves holding a `/` as "paths"; they were the 21 `summary` access tuples per group. They are equal, and the replay compares every leaf.

## Gates at the new head

No file in the RTL, builder, config, LiteX, firmware or simulation-suite scope changed since `62477be4`
(`git diff --stat 62477be4 9413958c` lists only the 19 paths above plus the audit page), so round 1's builder suite,
sharded sweep, firmware gate, flip check at the owner's bounds and timing floor carry unchanged.

| Gate | Head | Result | Receipt |
|---|---|---|---|
| docs workflow, 103 commands | `9413958c` | 99 PASS; 4 CI-environment rows (act install dir, `GITHUB_EVENT_PATH` x3), as round 1 | `gates/docswf-9413958c.txt` |
| docs workflow, 103 commands | `2f985971` | 98 PASS; the same 4, and the docs inventory (stale audit page), regenerated in `9413958c` | `gates/docswf-2f985971.txt` |
| quick list, 58 commands | `2f985971` | 55 PASS (`run.py --self-test`: 0 failures); the all-points flip check (8x8/2if, output identical to base `59b09884`'s), the CI tool inventory (CI environment), the docs inventory (fixed in `9413958c`) | `gates/quick-2f985971.txt` |
| round-2 checks (soc/yosys sweep self-tests, diagram regeneration, harness argv checks, solution docs, doc paths) | `a9da4c48`, `2f985971` | 6/6, 6/6 | `gates/round2-checks-*.txt` |
| planted defects of the new checks | `9413958c` | 5/5 caught, controls pass, tree clean | `gates/plants-9413958c.txt` |
| resource sweep: clean export, refusals, missing-image control, base comparison | `a9da4c48`, `59f91d9f` | ship, axilite accepted; 6/6 refused as planned; control refused, nothing written; argv equal to base | `f1/` |
| harness images rebuilt | `a9da4c48`, `2f985971`, bench `8c5e2b4f` | 16/16 equal to the re-measured; 16/16 equal to the measured | `s1/` |
| flip images' inputs carried | `a9da4c48`, `2f985971` | 19/19 and 16/16 equal | `gates/inputs-carry-*` |
| identity replay | packet | ALL CLAIMS HOLD; 11/11 plants refused | `identity/` |
| Vivado | - | two dumps of routed checkpoints (8x8 bench and flip, one slot); no route, no build | - |

## Open questions

1. (from round 1, unchanged) NFR-SCOUT-02's "switch-over" wording: for the owner.
2. The register map's re-record from a split export (R879-F1's first option) is deferred; it needs a public Issue, which this lane may not open. Asked of the manager.
3. Three pages still call `KL_maap` "the shipping allocator" (`docs/reference/FR_NFR.md:173`, the normative FR-MAAP-01 row; `docs/fpga/FPGA_DESIGN.md:313`; `docs/testing/TESTING.md:731`), true of the all-fabric build only. Found while fixing R880-1-R1, outside the reviewed list and partly normative: not edited.
4. The 1x1 block RAM dump was not made separately; the 1x1 full cell dump carries every block RAM's INIT.
