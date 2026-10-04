# [A533] HANDOFF: #652, the builder refuses a writable-name count above the saved-state NAME block

Status: **Round 2, REVIEW READY at `d5e74344`** (see [Round 2](#round-2), which
supersedes sections 1 to 6 wherever they differ: check 14 moved file, and the
resource-map arms moved and grew). Sections 1 to 6 are round 1b at `2f0f5929`.

- Issue: kebag-logic/milan-fpga#652
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/652#issuecomment-5982676356
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/652#issuecomment-5982727512
- Round-1 STOP: https://github.com/kebag-logic/milan-fpga/issues/652#issuecomment-5983982744
- Ruling (round 1b): https://github.com/kebag-logic/milan-fpga/issues/652#issuecomment-5983995755
- REVIEW READY (round 1b): https://github.com/kebag-logic/milan-fpga/issues/652#issuecomment-5984460909
- Branch: `652-builder-names`, from dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`
- Head: `2f0f59291080aeab934e0d72e124fb448c105e12` (five commits, not pushed)
- Roles: executor [A533]; reviewers [R478] (internal), [R479] (external)
- Scratch (never in the tree): `/tmp/652-a533/` (round 1), `/tmp/652-a533/r1b/` (this round)
- Evidence in this directory: `r1b/` (gate logs, resmap derivation, controls, scratch scripts)

## Commits

| Commit | What |
|---|---|
| `d33bdc3d` | Round 1: the NAME capacity as one RTL declaration, the builder's refusal, gate 38, two doc paragraphs. |
| `0da678f0` | Ruling item 1: gate 24a (d) and (e) under the NAME block, with planted controls; D8 restated. |
| `bcc31bcd` | Ruling item 2: the resource-map sweep records a builder refusal as a refused point with its line. |
| `68e4d89a` | Ruling item 2: the #649 page's two refused-point tables regenerated through `resmap_tables.py --write`, prose restated. |
| `2f0f5929` | Ruling item 3: SAVED_STATE_FASTCONNECT 4.2 at the current shapes, every figure checked by the record-space gate. |

## 1. The change (file:line at the head)

### 1.1 The refusal (round 1, unchanged since `d33bdc3d`)

| File | Lines | What |
|---|---|---|
| `hdl/milan/KL_nvm_backend.sv` | 243-247 | `localparam int unsigned N_NAME_MAX_C = 128;` beside `ID_NAME_C`: the NAME block's capacity, ids `0x80..0xFF`. Internal localparam: no port, register, parameter or parameter default changes. |
| `hdl/milan/KL_nvm_backend.sv` | 293-295 | `g_refuse_names` bounds `N_NAME_P` by `N_NAME_MAX_C`, printed through `%0d`; the elaborated message is byte-identical to the base's. |
| `sw/builder/endstation_builder.py` | 2687-2713 | `NVM_BACKEND_SV`, `nvm_name_capacity()`: exactly one live decimal `N_NAME_MAX_C` declaration, returned with its `path:line`; zero or two refuse (fail closed). |
| `sw/builder/endstation_builder.py` | 2716-2750 | `_adp_name_entries()` refuses a count above the capacity inside the write-free derivation pass, naming the count, the capacity and the declaration. |
| `sw/builder/test_builder.py` | 28823-29048 | Gate 38 (`test_name_count_fits_the_nvm_name_block`, line 29019). |

The refusal, verbatim (CLI, the 8x8 TDM8 variant):

```text
CONFIG ERROR: this AEM model has 235 writable names and the saved-state backend holds 128 NAME records (N_NAME_MAX_C, hdl/milan/KL_nvm_backend.sv:247): each writable name is one saved record, so KL_nvm_backend would refuse this shape at elaboration. The model is 107 over: remove named descriptors (streams, clusters or clock sources)
```

### 1.2 Ruling item 1: gate 24a and D8 (`0da678f0`)

| File | Lines | What |
|---|---|---|
| `sw/builder/test_builder.py` | 25182-25205 | (d) `_PHYSICAL_POOL_CAPTURE = 8` and `_assert_physical_pool_reappears()`: the physical-pool shape at 8 routed capture channels (123 names, same subject), and two planted controls. |
| `sw/builder/test_builder.py` | 25208-25251 | `_build_physical_pool(capture)`: the unchanged (d) assertions, parameterized by the channel count, with a named message on the pool order. |
| `sw/builder/test_builder.py` | 25254-25280 | `_check_rom_ceiling(cfg, overlay)` (the 16-bit store refuses this overlay's ROM) and `_check_rom_ceiling_marked(p)` (the former (e) assertions: ROM not emitted, `aem_rom_unsupported` names 16-bit, plan "planned", `--write-rtl` refuses). |
| `sw/builder/test_builder.py` | 25283-25330 | (e) `_assert_overwide_pool_is_refused()`: the over-wide pool (8 x (16+1+72) = 712 clusters, 747 names) is refused by `build()` before any write naming both figures; its own overlay's ROM is refused at the 16-bit ceiling; with the NAME capacity planted at its count the ceiling path is checked through the build. |
| `sw/builder/test_builder.py` | 28880-28940 | `_check_names_refused` and `_expect_red` take a `gate` label (default `gate 38`), so (e) reuses gate 38's refusal check. |
| `docs/ENDSTATION_BUILDER.md` | 101-104 | The tree diagram's `build_plan.md` line: a model past the NAME block is refused instead of marked planned. |
| `docs/ENDSTATION_BUILDER.md` | 754-775 | D8 "The size ceilings are real and enforced": the NAME block refuses the stress shape first, naming both figures; the 16-bit ROM ceiling is the second limit; the gate list. The stale 840-cluster figure is now the gate's 712. |

### 1.3 Ruling item 2: the resource-map sweep (`bcc31bcd`, `68e4d89a`)

| File | Lines | What |
|---|---|---|
| `syn/resmap/yosys_sweep.py` | 327-339 | `BUILDER_REFUSAL`, `builder_outcome(rc, text)`: built (exit 0); refused only on exit 1 with exactly one `CONFIG ERROR: ` line and no traceback; anything else failed. |
| `syn/resmap/yosys_sweep.py` | 342-368 | `command_shapes`: records every variant's outcome in `shapes/outcomes.json` (rc, outcome, expected, refusal line, log digest); fails the step on any outcome the plan does not expect, so a crash, an unexpected refusal and an expected refusal that builds all stop it. |
| `syn/resmap/yosys_sweep.py` | 371-381 | `builder_refusal(work, plan, point)`: the refusal line for a point on a refused variant; a variant with no recorded outcome is refused (fail closed), never assumed built. |
| `syn/resmap/yosys_sweep.py` | 475-497, 692-722, 725-732 | `run` reports a builder-refused point and does not price it (not a failure); `summary` records it as `{"builder": {"refusal": line}}` and refuses a priced receipt for one; `vivado-point` refuses it with the line. |
| `syn/resmap/yosys_sweep.py` | 126-128 | `load_plan` refuses an `expect` that is neither `built` nor `refused`. |
| `syn/resmap/yosys_sweep.py` | 855-922 | Self-test arms: the outcome classifier (a build, a refusal, and four planted non-refusals), one real builder refusal of the 8x8 TDM8 variant with nothing written, the refused-point path through `run` and `summary`, and the contradiction. |
| `syn/resmap/sweep_plan.json` | 3, 58, 62 | `rm_ax7101_8x8_tdm8` and `rm_ax7101_8x8_tdm8_2ch` are `"expect": "refused"`; the description says what that means. |
| `syn/resmap/resmap_models.py` | 151-163, 238, 373, 389-391 | A builder record is a refusal (no guard record needed); an unpriced point has no marginal; `guards.by_builder` lists the builder-refused points (absent when there are none, so the published inputs give a byte-identical `models.json`). Self-test arm for the builder-refused point. |
| `syn/resmap/resmap_tables.py` | 299-306, 361, 384-390 | `refusal_table`: Point, Refused by (`builder` or `elaboration guard`), Refusal. Self-test arm. |
| `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` | 586-596, 733-759 | `guard-refusals` and `datapath-marginals` regenerated through the generator (section 3.2). |
| `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` | 26, 91, 103, 598-600, 604, 1118 | Prose: the builder accepted these shapes when #649 ran and refuses them since #652; a builder-refused point is listed with the refusals and not priced. |

### 1.4 Ruling item 3: SAVED_STATE_FASTCONNECT 4.2 (`2f0f5929`)

| File | Lines | What |
|---|---|---|
| `docs/design/SAVED_STATE_FASTCONNECT.md` | 283-290 | User names 39 and 107, records 54 and 164, highest ids `0xA6` and `0xEA` (were 38, 99, 53, 156, `0xA5`, `0xE2`); the columns named as configurations and the check that binds them. |
| `docs/design/SAVED_STATE_FASTCONNECT.md` | 302-305 | The name-block sentence no longer restates a count: it points at the 8x8 column (and #389/#629 for the history). |
| `scripts/check_nvm_record_space.py` | 666-734 | Check 14: `ALLOCATION_PAGE`, `ALLOCATION_HEAD`, `ALLOCATION_COLUMNS` (1x1 = `endstation_ax7101_1x1_tdm8`, 8x8 = `endstation_ax7101_8x8`), `allocation_findings()`: every row's block against `ALLOC`, every count cell against the inventory derived for that column's shape, the record total and the highest id. |
| `scripts/check_nvm_record_space.py` | 830-832, 984-993 | `check_one` also returns the shape's census; `main` runs check 14 on a default run (and on a `--config` set that holds both shapes). |
| `scripts/check_nvm_record_space.py` | 88-91, 296-304 | Docstring check 14; the `stale_allocation_table` negative control. |
| `scripts/nvm_contract.py` | 233-236 | `SEAM.ALLOCATION_PAGE_EDIT`, the seam that control plants through. |

## 2. The shared source of the NAME capacity

Unchanged from round 1: `N_NAME_MAX_C` at `hdl/milan/KL_nvm_backend.sv:247`
is the one declaration. The RTL guard (`g_refuse_names`, line 293) and the
builder (`nvm_name_capacity()`, `endstation_builder.py:2696`) both read it; the
builder holds no copy of 128. Gate 38 ties them (text check always; Verilator
elaboration at 128, 129 and a planted 127 where Verilator is on PATH).

Observed, not changed: the record-space gate's own allocation contract,
`scripts/nvm_contract.py` `ALLOC["NAME"] = (0x80, 128)`, states the same block
for its check 3. It predates #652 and is outside the builder; a follow-up could
read it from the same declaration.

## 3. Tests and their failing controls

### 3.1 Gate 24a (builder bank)

| Check | Shape | Expected | Planted control that turns it red |
|---|---|---|---|
| (d) physical pool leads the talker port, static map on it | `ax7101_8x8`, 8 routed capture channels, pilot, loopback 2 | builds; pools physical, pilot, loopback; 11 clusters; primary role physical; names physical-first; 123 writable names | 16 routed channels (the size until #652): refused, "writable names and the saved-state backend holds"; no routed channel: "not physical, pilot, loopback" |
| (e) name refusal | `ax7101_8x8`, 16 capture, pilot, loopback 72 | 712 AUDIO_CLUSTERs; 747 names (graded by `nvm_shape.expected_names`, not the builder); `build()` raises naming `747 writable names`, `128 NAME records` and `hdl/milan/KL_nvm_backend.sv:247`; output directory never created | capacity planted at 747 in a copy of the RTL: "747 writable names accepted" |
| (e) ROM ceiling on its overlay | the same overlay | `emit_aem_rom_svh` raises "exceeds the 16-bit store address space" | the shipped `ax7101_8x8` overlay: "the AEM ROM was emitted" |
| (e) ceiling through the build | the same config, capacity planted at 747 | ROM not emitted, `aem_rom_unsupported` names 16-bit, plan "planned", `--write-rtl` refuses ("entity definition is incomplete") | (the former (e) assertions, kept; this arm is what still exercises the `--write-rtl` refusal of a ROM-less shape, which no tracked shape reaches now) |

In the final bank at the head (`r1b/gates/bank/builder_bank.log`, lines
343-346 and 502-503): (d) "2/2 planted controls turned it red", (e) "2/2
planted controls turned their check red", gate 38 "9/9 planted defects".

### 3.2 The resource-map sweep

Self-test arms (`yosys_sweep.py --selftest`, `resmap_models.py --selftest`,
`resmap_tables.py --selftest`), and ten planted defects, each loaded as an
in-memory copy of the module with the same `__file__` (tree untouched,
`r1b/scratch-scripts/mutate_resmap.py`): **10/10 turned their self-test red**.

| Planted defect | Red because |
|---|---|
| a traceback read as a refusal | `outcome: a traceback read as ('refused', ...)` |
| any exit with one refusal line read as a refusal | `outcome: a usage error read as ('refused', ...)` |
| a variant with no outcome taken as built | `refused: a variant with no builder outcome was taken as built` |
| `run` prices a builder-refused point | `refused: run exited 1 or priced the refused point` |
| `summary` ignores a receipt for a refused point | `refused: a priced receipt for a refused point was summarized` |
| `summary` drops the builder record | `refused: summary exited 0 with {}` |
| the plan accepts any expectation | `plan: an expectation that is neither built nor refused was accepted` |
| a builder refusal not read as a refusal (models) | `GuardError: s16: no guard record` (the models stop) |
| an unpriced point given a marginal (models) | `KeyError: 'hierarchical'` (the self-test crashes) |
| builder refusals labelled as guards (tables) | `refusal table: who refused each point is wrong` |

The real `shapes` step at `bcc31bcd` (`r1b/resmap/shapes.log`): rc 0; seven
variants built, `rm_ax7101_8x8_tdm8` and `rm_ax7101_8x8_tdm8_2ch` refused
with the line above, as the plan expects; nothing written for them. Its two
controls (`r1b/controls/`): the plan without the `expect` marks, rc 1
("refused where the plan expects built"); the plan expecting the 2x2 to be
refused, rc 1 ("built where the plan expects refused").

**The page (ruling item 2's "show or update").** Evidence in `r1b/resmap/`.

1. Published #649 inputs (round-2 packet, `summary.json` sha256
   `8f8060f5...`, census `b377ddec...`), this head's resmap code:
   `models.json` byte-identical to the published one (`cmp` rc 0); 25 of 26
   page tables equal; `guard-refusals` differs only by the new Refused by
   column (`blockdiff-published-inputs-vs-base-page.txt`).
2. The new pipeline's summary, derived without re-pricing anything: the base
   `summary` code over #649's 59 point directories reproduces the published
   `summary.json` byte for byte (`8f8060f5...`); this head's `summary` over
   the same 59 refuses the two now-refused points ("priced, but the builder
   refuses its shape", rc 1); over the 57 others plus this head's
   `shapes/outcomes.json` it gives 57 entries identical to the published ones
   and the two builder records (rc 0). Every priced variant point's receipt
   names exactly the shape header this head generates
   (`shape-headers-vs-649.txt`), so #649's Yosys figures stand for them.
3. Models from that summary: every fit, calibration, TDM model and
   in-context figure identical to the published ones; only
   `datapath_marginals` (the two points, never priced, have none) and
   `guards` (their refusal is the builder's line; `by_builder`) change.
4. Tables: 24 of 26 equal; `guard-refusals` and `datapath-marginals` change
   (`blockdiff-derived-vs-base-page.txt`). Filled through
   `resmap_tables.py --page ... --write`, then rechecked: "every table equals
   a fresh generation", rc 0. The prose was restated to match (section 1.3).

### 3.3 The 4.2 allocation table (record-space gate check 14)

| Run | Result |
|---|---|
| check 14 against the page as it was (38, 99, 53, 156, `0xA5`, `0xE2`) | rc 1, exactly six findings: 1x1 and 8x8 user names, records and highest id (`r1b/controls/nvm-check-against-stale-page.log`); every block and group count already matched |
| against the updated page | rc 0, "every allocation-table figure at 1x1 (endstation_ax7101_1x1_tdm8), 8x8 (endstation_ax7101_8x8) is the derived one" |
| `--mutate=stale_allocation_table` (a digit prefixed to the 1x1 name count) | rc 1, `1x1 user name reads 139, the endstation_ax7101_1x1_tdm8 inventory derives 39`; required by `--self-test` |

## 4. Byte identity of the tracked configurations

Round 1 (at `d33bdc3d` against the base): every artifact of all five tracked
configurations regenerates byte-identically (120 files, `diff -r` and sha256
rc 0), and `git status` stays clean after regeneration. Since `d33bdc3d`,
`git diff d33bdc3d..HEAD -- sw/builder/endstation_builder.py hdl/ configs/
avdecc/ sw/litex/` is empty and no submodule pin moved, so the builder and
everything it reads are unchanged.

Re-run at the head `2f0f5929` with the same scratch script
(`/tmp/652-a533/dump_artifacts.py`: every in-memory artifact of
`_derive_artifacts()` plus a full `build()` per tracked configuration, taking
the tracked writes exactly as today's owners do):

| Comparison | Result |
|---|---|
| sha256 manifest, head vs round 1's base (`r1b/gates/head-out-final.sha256`, `base-out-round1.sha256`), 120 files | identical, `cmp` rc 0 |
| `diff -r` head vs base trees | rc 0 |
| `git status --porcelain` after regeneration | empty |

## 5. Gates at the head

At `2f0f59291080aeab934e0d72e124fb448c105e12`, tree clean, pinned Verilator
5.050 first on `PATH`, `PYTHONDONTWRITEBYTECODE=1`. Each gate ran unpiped in
the foreground of its runner with its own log and rc
(`r1b/scratch-scripts/run_gates.py`; logs and `results.json` per set in
`r1b/gates/`). The bank ran alone; the read-only set beside it; the
builder-consumer set and the suites after it, beside each other.

| Gate | Command | rc | Result |
|---|---|---|---|
| **Builder bank** | `python3 sw/builder/test_builder.py --require-rv32` | **0** | `ALL GATES PASS EXCEPT 1 NOT RUN` in 1,154 s; gate 24a (d) 2/2 and (e) 2/2 planted controls, gate 38 9/9; NOT RUN: gate 11 (the Arty `mf48` build tree is not on this host) |
| Record space | `python3 scripts/check_nvm_record_space.py` | 0 | 0 findings across 5 configs; check 14: every 4.2 figure is the derived one |
| Record space self-test | `... --self-test` | 0 | 19/19 negative controls red, including `stale_allocation_table` |
| NVM capture census | `python3 scripts/check_nvm_capture.py` | 0 | census, clocks, both timing arms and receipt agree |
| Saved-state writer | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | OK across 5 shapes, every planted defect reddened |
| Entity shape | `python3 scripts/check_entity_shape.py --self-test` | 0 | PASS |
| Sweep/build shape | `python3 scripts/check_sweep_shape.py --self-test` | 0 | PASS |
| Deploy shape | `python3 scripts/check_deploy_shape.py --self-test` | 0 | PASS |
| Wire accountability | `python3 scripts/check_wire_accountability.py --self-test` | 0 | 77 checks, 0 findings |
| AEM store self-test | `python3 avdecc/gen_aem_store.py --self-test` | 0 | PASS |
| Resmap sweep self-test | `python3 syn/resmap/yosys_sweep.py --selftest` | 0 | PASS (0 problems) |
| Resmap models self-test | `python3 syn/resmap/resmap_models.py --selftest` | 0 | PASS |
| Resmap tables self-test | `python3 syn/resmap/resmap_tables.py --selftest` | 0 | PASS |
| Resmap map self-test | `python3 syn/resmap/resmap_map.py --selftest` | 0 | 15 of 15 arms |
| Resmap SoC self-test | `python3 syn/resmap/soc_sweep.py --selftest` | 0 | PASS |
| Resmap `shapes` | `python3 syn/resmap/yosys_sweep.py --work <scratch> shapes` (at `bcc31bcd`; `syn/resmap` unchanged since) | 0 | 7 built, 2 refused as expected; two planted plans rc 1 (section 3.2) |
| #649 page tables | `resmap_tables.py --work --models --map --soc-variants --page ...` over the derived inputs | 0 | every table equals a fresh generation (section 3.2) |
| `nvm_backend` suite | `make -j16 -C tb/verilator/nvm_backend` | 0 | 541 + 210 checks, 0 failures; negative controls alias, stride, stale_mask, blind_read red |
| `nvm_cosim` suite | `make -j16 -C tb/verilator/nvm_cosim` | 0 | 465 checks PASS |
| `fw_service_budget` suite | `make -j16 -C tb/verilator/fw_service_budget` | 0 | 52 checks, 0 failures |
| Docs | `python3 scripts/docs_check.py` | 0 | 0 findings |
| Em-dash | `check_em_dash.py --base 6c22d3ca` (pinned renderer) | 0 | 0 findings over 66 added lines in 3 pages |
| Doc style | `check_doc_style.py` and `--selftest` | 0, 0 | OK |
| Contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` (pinned renderer) | 0, 0, 0 | 1501/1501 arms; 340 anchors; OK |
| Cited paths | `check_doc_paths.py` | 0 | 911 paths resolve, 9 line anchors |
| Archive, feature status, module matrix, doc map, bare-metal scope | `check_archive.py`; `check_feature_status.py --self-test`; `gen_module_matrix.py --check`; `DOC_MAP.gen.py --check`; `check_baremetal_only.py --check` | 0 each | OK |
| Solution docs | `check_solution_docs.py` and `--selftest` | 0, 0 | OK, 43 controls |
| Python idiom | `check_py_idiom.py` and `--selftest` | 0, 0 | every ratchet held; 54/54 |
| SV idiom, hygiene, fail-fast, port contracts, naming, TODO, test evidence | the `scripts/` checks | 0 each | PASS (fail-fast 81 <= 84, test evidence 72 <= 77) |
| RTL lint | `lint_rtl.py --check` | 0 | 90 <= 90 |
| SoC sources, RTL source lists | `check_soc_sources.py` (+`--selftest`), `check_rtl_source_lists.py` | 0 | OK |
| Byte identity | section 4 | 0 | 120 files identical, tree clean |

Not re-run in round 1b, with the reason:

- The full Verilator sweep (`scripts/run_all_suites.sh`: 59/59, 2,148,513
  checks), `syn/yosys/run.sh` (55/55 tops), `xvlog_gate.py --check` and the
  base-vs-head guard elaboration all ran at `d33bdc3d` (round 1, section 5 of
  the STOP). Since then no RTL, testbench, builder, configuration or
  submodule pin changed (`git diff --stat d33bdc3d..HEAD -- hdl/ tb/ sw/builder/endstation_builder.py configs/`
  is empty). The four suites that import a module this round changed were
  re-run above.
- `tb/verilator/nvm_capture_cpu` is a LiteX CPU measurement, not a make suite
  (my `make` invocation found no Makefile, rc 2, and measured nothing). It
  reads only `nvm_shape.closed_record_census`, which is unchanged; its hosted
  input gate, `check_nvm_capture.py`, binds its receipt to that census and is
  rc 0 above.
- `test_builder.py --require-elaboration --require-rv32` (elaborate.yml): that
  flag only refuses skips of the no-LiteX or toolchain kind
  (`_require_elaboration_verdict`, `test_builder.py:24472`); the run above has
  one NOT RUN row, gate 11's missing report, which is neither, so it would
  give the same verdict. Not run separately.
- Hosted CI and the `act` replica: no push in this lane.

## 6. Open items and follow-ups

- `ALLOC["NAME"] = (0x80, 128)` in `scripts/nvm_contract.py` restates the NAME
  block for the record-space gate (section 2). Not changed; a follow-up.
- `avdecc/aem_assemble.py:309-312` says the builder catches the 64 KiB
  ceiling as `aem_rom_unsupported` and marks the shape planned. The code path
  is unchanged and gate 24a (e) still exercises it, but no shape reaches it
  through the NAME block today. Left as is.
- The #649 page's Yosys run-receipt rows for `streams-8` and
  `streams-8-chans-2` are #649's runs and stay as recorded.
- Not run: hosted CI and the `act` replica (no push in this lane).


## Round 2

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/652#issuecomment-5984666082
- REVIEW READY (round 2): https://github.com/kebag-logic/milan-fpga/issues/652#issuecomment-5985156837
- Reviews answered, both on PR #660: R478-1 (comment 5984662963, NEGATIVE on
  F1, MINOR, `Tests` and `Docs`) and R479-1 (comment 5984636580, NEGATIVE on F1,
  MINOR, `Robustness` and `Tests`). Packets: branch `652-review-evidence` at
  `1dfd0c58`.
- Starting head `2f0f5929`. Dev had moved `6c22d3ca` -> `c0280fc0`.
- Head **`d5e743440a56c77c43241879226b851abb3c62ac`**: one merge and four
  one-line commits on top of `2f0f5929`. No rebase, no amend, not pushed.
- Scratch, never in the tree: `/tmp/652-a533/r2/`. Evidence in this directory: `r2/`.

### R2.1 Commits

| Commit | Item | What |
|---|---|---|
| `ef236411` | 5 | Merge dev `c0280fc0` with `--no-ff`. Dev's 12 files (CRF unbind, #653/#655) overlap no file of this lane; no submodule pin moved. |
| `b71979dc` | 1 | R479-1 F1: check 14 refuses a section 4.2 row without one cell per header column. The check moved to `scripts/nvm_allocation_table.py`. Two planted controls. |
| `694e2b18` | 2 | R478-1 F1: `generate_shapes()` split from the export; a stand-in-builder arm holds the `shapes` verdict; an end-to-end `build()` arm holds `guards.by_builder`. The sweep's builder-refusal arms live in `syn/resmap/yosys_sweep_selftest.py`. |
| `94a12eb8` | 3 | R479-1 S2: each expected refusal pins its cause; a refusal for any other cause fails the step. Stand-in control; the real builder's line is read for both pinned variants. |
| `d5e74344` | 2, 3 | Found by my own mutation campaign (R2.6): with the expectation check removed, the old plan arm still passed, because the new cause check refused its plan instead. Each plan-validation arm now requires its own refusal message. |

### R2.2 Why two modules moved: the long-module ratchet

`scripts/check_py_idiom.py` counts modules over 1,000 lines against a ratchet
of 10 that "may only go down", and new Python must comply immediately
(`docs/development/CODE_QUALITY.md`, Rule 12). At `2f0f5929`,
`check_nvm_record_space.py` had 998 lines and `yosys_sweep.py` 995. This
round's code took them to 1,045 and 1,067, and the count to 12 > 10 (rc 1,
`r2/gates/py_idiom_before_move.log`). Raising the budget would weaken a gate.
So I moved only this PR's own code out, along seams the tree already uses:

| Moved | To | Precedent | Lines |
|---|---|---|---|
| Check 14, written in round 1b (`ALLOCATION_*`, `allocation_findings` and its helpers) | `scripts/nvm_allocation_table.py`; the gate imports it (`check_nvm_record_space.py:144`) and keeps the controls in `MUTATIONS` | `scripts/nvm_map_checks.py` holds #501's checks for the same gate | gate 998 -> 951 |
| The sweep's builder-refusal self-test arms (round 1b's outcome and refused-point arms, and this round's shapes arm) | `syn/resmap/yosys_sweep_selftest.py`; `yosys_sweep.selftest()` imports it (`yosys_sweep.py:906-907`) | `scripts/check_rtl_source_lists_selftest.py` holds that gate's arms | sweep 995 -> 949 |

`run_arms()` takes the running module, `sys.modules[__name__]`, and calls its
functions. A defect planted in memory with `mutate_module.py` is therefore the
code the arms exercise. The r3 anchor (`failures += outcome != expected`,
`yosys_sweep.py:379`) and the r11 anchor (`result["guards"]["by_builder"] =
builder`, `resmap_models.py:391`) stay where R478-1 planted them. Result:
`long module: 10 <= 10`, rc 0.

### R2.3 Item 1 (R479-1 F1): a row that lost a figure

| File | Lines | What |
|---|---|---|
| `scripts/nvm_allocation_table.py` | 32-35 | `_allocation_cells()`: one table line's cells. The header is split the same way as the body. |
| `scripts/nvm_allocation_table.py` | 52-60 | `_allocation_width()`: the finding for a row whose cell count is not the header's. It names the columns with no figure, or the cells past the last column. |
| `scripts/nvm_allocation_table.py` | 74-113 | `allocation_findings()`: a row of the wrong width is reported and skipped, never compared on its first cells. The figure comparison is `zip(..., strict=True)`. A row still marks its group as seen, so a malformed row does not also report "no row". |
| `scripts/check_nvm_record_space.py` | 88-92 | Docstring check 14: a row without one cell per column is itself a finding. |
| `scripts/check_nvm_record_space.py` | 306-328 | Controls `short_allocation_row` (the 8x8 cell dropped from the user-name row) and `long_allocation_row` (that cell repeated), beside `stale_allocation_table`. |

| Run | Result |
|---|---|
| `--mutate=short_allocation_row` | rc 1, one finding: `0x80 .. 0xFF user name has no 8x8 figure (5 cells under a 6-column header)` |
| `--mutate=long_allocation_row` | rc 1, one finding: `0x80 .. 0xFF user name has 1 cell(s) past the 8x8 column (7 cells under a 6-column header)` |
| The same two page edits under `2f0f5929`'s gate, run in memory under its real path (`r2/scratch-scripts/before_after.py`) | rc 0 and rc 0: R479-1's defect, reproduced (`r2/evidence/before-nvm-*.log`) |
| `--self-test` | 21/21 controls red, the three allocation-table controls among them |
| unedited page | rc 0, "every allocation-table figure ... is the derived one" |
| `--emit-record-table` for the 8x8 and 1x1 fixtures | byte-identical to `tb/verilator/nvm_backend/records_*.txt` (the moved code is not on that path) |

### R2.4 Item 2 (R478-1 F1): the `shapes` verdict and the `by_builder` producer

| File | Lines | What |
|---|---|---|
| `syn/resmap/yosys_sweep.py` | 348-350 | `command_shapes()` exports the tree and calls `generate_shapes()`. |
| `syn/resmap/yosys_sweep.py` | 353-382 | `generate_shapes(work, plan, tree)`: the unchanged loop, now callable on a synthetic tree. |
| `syn/resmap/yosys_sweep_selftest.py` | 33-44, 81-108 | `STAND_IN_BUILDER` and `_shapes()`: a synthetic tree with no export. Every outcome expected gives rc 0 and records both outcomes with the refusal line. An unexpected refusal, an expected refusal that builds, a refusal without the pinned cause, and a crash each give rc 1. |
| `syn/resmap/resmap_models.py` | 361-363 | `build()` takes `plan_path` (default: the tracked plan). |
| `syn/resmap/resmap_models.py` | 477-496 | `_selftest_build()`: `build()` end to end over the synthetic plan and summary. With the builder-refused point, `guards.by_builder == ["s16"]` and its refusal is the builder's line. With none, `by_builder` is absent, which is what keeps #649's `models.json` byte-identical. |

R478-1's bar, re-planted with its own `scripts/mutate_module.py` (sha256
`e0a4c996...`, used unchanged):

| Mutant | Self-test | Red because |
|---|---|---|
| r3: `failures += outcome != expected` -> `failures += outcome == "failed"` | `yosys_sweep.py` rc 1 | `shapes: an unexpected refusal exited 0, not 1`; `shapes: an expected refusal that builds exited 0, not 1` |
| r11: `result["guards"]["by_builder"] = builder` -> `pass` | `resmap_models.py` rc 1 | `build: with a builder-refused point, guards.by_builder is None` |
| unmutated control | rc 0 | |

### R2.5 Item 3 (R479-1 S2): the expected refusal's cause is pinned

| File | Lines | What |
|---|---|---|
| `syn/resmap/sweep_plan.json` | 3, 58, 62 | Both 235-name variants carry `"cause": "writable names and the saved-state backend holds"`. That is the cause clause of the builder's line; gate 24a's control matches the same text. The description says what the field means. |
| `syn/resmap/yosys_sweep.py` | 130-134 | `load_plan` refuses an expected refusal with no cause, and a cause on a variant expected to build. |
| `syn/resmap/yosys_sweep.py` | 372-380 | `foreign`: a refusal the plan expects, whose line does not carry the pinned cause. It prints "without the cause the plan pins" and fails the step. `outcomes.json` records the cause. |
| `syn/resmap/yosys_sweep_selftest.py` | 47-78 | `_outcome()` runs the real builder on every variant the plan expects refused and requires the plan's pinned cause in its line (both variants, nothing written). |
| `syn/resmap/yosys_sweep.py` | 852-870 | Plan arms: an expectation that is neither built nor refused, an expected refusal with no cause, and a cause on a built variant. Each must be refused with its own message (`d5e74344`). |
| `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` | 91 | The plan pins the cause each refusal line must carry, and a refusal for another cause stops the step. |

The real step at the head (`r2/shapes/`):

| Plan | rc | Outcome |
|---|---|---|
| tracked | 0 | 7 built, 2 refused as expected, each carrying the pinned cause |
| both `expect`/`cause` marks removed | 1 | "refused where the plan expects built", twice |
| each cause replaced by a text the builder never prints | 1 | "refused without the cause the plan pins", twice |
| the 2x2 expected refused | 1 | "built where the plan expects refused" |
| that foreign-cause plan under `2f0f5929`'s sweep, in memory | 0 | S2 reproduced: any refusal was accepted (`r2/evidence/before-shapes-othercause.log`) |

### R2.6 Mutation campaign at the head

`r2/scratch-scripts/mutate_r2.py` drives R478-1's `mutate_module.py`
(unchanged, sha256 `e0a4c996...`) once per mutant. Each run is a fresh process,
the module is planted in memory, and the tree is never written. Result:
**19/19 verdicts as expected** (`r2/evidence/mutations.txt`). The unmutated
control is green, and these 18 mutants are red:

- R478-1's r3 and r11;
- the step fails on every outcome;
- a foreign-cause refusal not counted;
- the pinned cause ignored;
- an expected refusal needing no cause;
- a cause allowed on a built variant;
- the plan accepting any expectation;
- a traceback read as a refusal;
- any exit with one refusal line read as a refusal;
- a variant with no outcome taken as built;
- `run` pricing a refused point;
- `summary` accepting a priced receipt for one;
- `summary` dropping the builder record;
- `by_builder` written with no builder-refused point;
- a builder refusal not read as a refusal;
- an unpriced point given a marginal;
- builder refusals labelled as guards.

The first run at `94a12eb8` was 18/19. "The plan accepts any expectation"
survived because the cause check answered for it; `d5e74344` fixed that arm
(R2.1).

### R2.7 Item 4: S1 needs no change; S3 stays open

- **S1 (both reviewers).** `scripts/nvm_contract.py:164` `ALLOC["NAME"] =
  (0x80, 128)` is the record-space gate's independent expectation of the
  section 4.2 design contract. It predates #652, and it is a verification
  oracle, not a builder mirror. The builder holds no copy of 128: it reads
  `N_NAME_MAX_C` (`KL_nvm_backend.sv:247`). Gate 38 pins
  `_NAME_BLOCK_RECORDS = 128` independently. Both reviewers note one residual
  drift path (the RTL capacity and gate 38's pin moving together without
  `ALLOC`); per the assignment it is not closed here.
- **S3, open.** `ID_NAME_C + N_NAME_MAX_C` filling exactly the 8-bit
  `record_id` space is unchecked, as it was with the old literal. An
  elaboration-time guard would close it. Listed open in the PR body.

### R2.8 #649 page and models

Round 1b's derived inputs (`/tmp/652-a533/r1b/resmap/new-work`, the #649
`map` and `soc_prices.json`), run through this head's code:

- `resmap_models.py`: `models.json` is byte-identical to round 1b's
  (sha256 `659e3420...`).
- `resmap_tables.py --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md`:
  rc 0, "every table equals a fresh generation"; `tables.md` is byte-identical
  to round 1b's (sha256 `8d708dc7...`).
- The one page edit this round (line 91) is prose outside every table block.

### R2.9 Byte identity of the tracked configurations

At `d5e74344`, `/tmp/652-a533/dump_artifacts.py` (round 1's script, unchanged)
regenerated every in-memory artifact of `_derive_artifacts()`, plus a full
`build()`, for all five tracked configurations, with the tracked writes taken
exactly as today's owners take them.

| Comparison | Result |
|---|---|
| sha256 manifest, 120 files (`r2/byte-identity/head-out-r2.sha256`) against round 1b's (`r1b/gates/head-out-final.sha256`, which equals round 1's base manifest `base-out-round1.sha256`) | identical, `cmp` rc 0 |
| `diff -r` against round 1's head output tree | rc 0 |
| `git status --porcelain` after the in-tree rewrites | empty |

Since the base's outputs reappear byte for byte with dev `c0280fc0` merged,
dev's changes alter nothing the builder emits. The new base therefore emits the
same 120 files.

### R2.10 Gates at the head

At `d5e743440a56c77c43241879226b851abb3c62ac`, tree clean, pinned Verilator
5.050 first on `PATH`, `PYTHONDONTWRITEBYTECODE=1`. Each gate ran unpiped in
the foreground of `r2/scratch-scripts/run_gates.py`, with its own log and rc
(`r2/gates/<set>/`). The bank ran beside the read-only set, then beside the
consumers and the suites. Nothing those three sets touch is shared with the
bank's build directories.

| Gate | Command | rc | Result |
|---|---|---|---|
| **Builder bank** | `python3 sw/builder/test_builder.py --require-rv32` | **0** | `ALL GATES PASS EXCEPT 1 NOT RUN` in 1,216 s; gate 24a (d) 2/2 and (e) 2/2 planted controls; gate 38 9/9 planted defects, capacity read from `KL_nvm_backend.sv:247`; NOT RUN: gate 11 (the Arty `mf48` report is not on this host) |
| Record space | `python3 scripts/check_nvm_record_space.py` | 0 | 0 findings across 5 configs; check 14: every 4.2 figure is the derived one |
| Record space self-test | `... --self-test` | 0 | 21/21 controls red, among them `short_allocation_row`, `long_allocation_row` and `stale_allocation_table` |
| NVM capture, saved-state writer, entity, sweep and deploy shape, wire accountability, AEM store | the builder-consumer set | 0 each | 9/9 |
| Resmap self-tests | `yosys_sweep`, `resmap_models`, `resmap_tables`, `resmap_map`, `soc_sweep` `--selftest` | 0 each | PASS |
| Resmap `shapes`, tracked plan | `python3 syn/resmap/yosys_sweep.py --work <scratch> shapes` | 0 | 7 built, 2 refused as expected with the pinned cause |
| Resmap `shapes`, three planted plans | `--plan <planted> ... shapes` | 1, 1, 1 | as R2.5 |
| Resmap mutation campaign | `r2/scratch-scripts/mutate_r2.py` | 0 | 19/19 verdicts as expected |
| #649 page tables | `resmap_tables.py ... --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` | 0 | every table equals a fresh generation (R2.8) |
| `nvm_backend` suite | `make -j16 -C tb/verilator/nvm_backend` | 0 | 541 + 210 checks, 0 failures; 4 negative controls red |
| `nvm_cosim` suite | `make -j16 -C tb/verilator/nvm_cosim` | 0 | 465 checks PASS; 39 of 39 mutants killed |
| Docs, contents, cited paths, em-dash (`--base c0280fc0`), doc style, archive, feature status, module matrix, solution docs, doc map, bare-metal scope | the read-only set | 0 each | 33/33 with the rows below |
| Python idiom and its self-test | `check_py_idiom.py`, `--selftest` | 0, 0 | `long module: 10 <= 10`, `long function: 9 <= 9`; before the move it was rc 1, `long module 12 > ratchet 10` (`r2/gates/py_idiom_before_move.log`) |
| SV idiom, hygiene, fail-fast, port contracts, naming, TODO, test evidence, RTL lint, SoC sources, RTL source lists | the `scripts/` checks | 0 each | PASS |
| Byte identity | R2.9 | 0 | 120 files identical, tree clean |

Not run in round 2, with the reason:

- The full Verilator sweep, `syn/yosys/run.sh` and `xvlog_gate.py`. They ran at
  `d33bdc3d`, and no RTL, testbench, builder or configuration file of this lane
  changed after it. The RTL and testbench files the dev merge brought
  (`KL_crf_rx.sv`, `milan_datapath.sv`, `tb/verilator/crf_rx`,
  `tb/verilator/milan_dp`) were validated in their own lane; the candidate-merge
  validation stays with the merge step.
- An earlier bank run at `94a12eb8` was stopped (SIGTERM) and superseded by the
  run above at the final head.
- Hosted CI and the `act` replica: nothing is pushed from this lane.

### R2.11 Open items

- R479-1 S3 / R478-1 S3: `ID_NAME_C + N_NAME_MAX_C` filling the 8-bit id
  space is unchecked (R2.7).
- S1's residual drift path: `ALLOC` against the RTL capacity (R2.7). Not closed
  here, per the assignment.
- `resmap_tables.py`'s refusals-table arm reads a hand-made `by_builder`. The
  producer is held by the `resmap_models.py` arm (R2.4), not by one arm through
  both.
