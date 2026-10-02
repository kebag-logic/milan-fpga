# [A504] Lane C8 round 4 (merge only): HANDOFF

Status: done. Items 1 to 3 complete at `bd86f64`; REVIEW READY posted on #60 (comment
5959903762) with that head.

- Repository Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #144, branch
  `c8-descriptor-lint`. Start head `97f6eace064901f223e13abed7026f96bc4df805`. Remote
  confirmed: `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.
- Merged: processor `main` `631eeb342ca1e3fa80e734077a56a943aee76ff1` (PR #142, P141),
  with `git merge --no-ff`. No rebase.
- Head: `bd86f6466baa77113eea2266c00044c3a29678f2`. Two commits added, nothing amended,
  nothing pushed.
- Assignment: issue #60 comment 5958629222 (round 4, merge only; R434-3 and R435-3 were
  POSITIVE at 97f6eace). TAKEN: #60 comment 5958632979.
- Parent: milan-fpga dev `cdf49d1a` (read-only checkout, never modified; HEAD cdf49d1a and
  `git status --porcelain` empty afterwards) and PR #634's head `0b066b6e`, fetched from
  `refs/pull/634/head` into a scratch bare repository (`$VALIDATION_STORAGE/c8-a504/src`).

## Commits

| Commit | Item | Subject |
|---|---|---|
| `3bfc7c6` | 1 | Merge main 631eeb34 (#142, P141) into the C8 lane, keeping both sides: main's restated L6 and REQ-MDL-005 with the lint's columns, and domain-source-identity credited to IEEE 1722.1-2021 7.2.32 as main's L6 does |
| `bd86f64` | 1 | Add L6's positive case: one CLOCK_DOMAIN listing INTERNAL 0, the CRF input's source 1 and one INPUT_STREAM source per AAF input at 2 + k, eight AAF inputs and ten sources, as main's restated L6 allows |

Items 2 and 3 need no commit: nothing re-measured moved, and no parent model packs
differently, so neither parent patch changes.

## Item 1: the merge and L6

Clauses, read in the standards' text this round:
- Milan v1.2 §5.3.3.6: "For each Stream Input that supports [CRF] ..., or for the single
  Stream Input that supports [AAF] when the Configuration does not support CRF input,
  there shall be exactly one associated CLOCK_SOURCE" (INPUT_STREAM at STREAM_INPUT); "at
  least one" INTERNAL when the Configuration has a Stream Output; at least one
  CLOCK_SOURCE per Clock Domain. It sets no count for an AAF input beside a CRF input.
- IEEE 1722.1-2021 §7.2.32 Table 7-61: `clock_sources_offset` 76, `clock_sources_count`
  "maximum value ... 216", `clock_sources` "the list of CLOCK_SOURCE descriptor indices
  which the clock_source_index may be set to". 76 + 2 × 216 = 508, §7.2's maximum.

### Conflicts, resolved keeping both sides

| Change | Where |
|---|---|
| 07 §3.1 L6 row: main's statement whole (the §5.3.3.6 set as a minimum; one INPUT_STREAM per AAF input allowed beside the CRF input's, IEEE §7.2.9.2 Table 7-17; the consumer's order INTERNAL 0, CRF 1, AAF k at 2 + k; any length up to Table 7-61's 216; the membership test of §7.2.32; BAD_ARGUMENTS per Table 7-141 carrying the current index, §7.4.23.1; main's clause column). The lint's side keeps "sits at 76, is `76 + 2 × count` long" and its Checks column, and adds "neither the processor nor the lint reads an order" and "(76 + 2 × 216 is §7.2's 508 octets, L12's `descriptor-maximum`)" | `docs/architecture/07_memory_maps.md:186` |
| REQ-MDL-005: main's clause and requirement text; Arch "consumer's model (07 §3.1 ownership); the processor's range check over L6's identity list; packer model lint L6, which accepts that set and reads no order (defence in depth)"; Doc `07 §3.1, 09 §8.5`, Ver `DIR` (the lane's) | `docs/00_MILAN_COMPLIANCE_REVIEW.md:450` |
| The check implementing L6's list cites the clause main's L6 now credits: `domain-source-identity` `IEEE + "§7.2.32; 06 §6.4"` (was `§7.4.23.1`) | `hdl/aecp/desc/model_rules.py:174` |

Everything else auto-merged. `git diff 631eeb34 HEAD` on 06, `hdl/aecp/ucode` and
`tb/pp_top` shows only the lane's own `tb/pp_top/README.md` note (+7, the fixture image is
not linted), present since round 1. The lane's delta against main is the same 19 files as
against `2ebd4fe8`.

Probe for the added bound (`scripts/probe_216.py`, `receipts/probe_216.txt`): 216 sources,
508 octets: PACKED; 217 sources, 510 octets: refused, `L12 descriptor-maximum`.

### L6 positive case

No rule changes. The lint already accepted main's L6 (`crf-input-source`,
`aaf-input-source` only without a CRF input, `internal-source`; no count for AAF inputs
beside a CRF input; no class order read).

| Change | Where |
|---|---|
| `ConformingModelTest.test_a_source_per_aaf_input_beside_crf`: `milan_min` plus STREAM_INPUTs 2..8 (copies of AAF input 0; ENTITY `listener_stream_sinks` 9), CLOCK_SOURCEs 2..9 INPUT_STREAM at STREAM_INPUT 0, 2..8, CLOCK_DOMAIN 0 `[0..9]`; packs with the lint on and no waiver | `tb/desc_store/test_gen_desc_image.py:455` |
| record: 09 §8.5 `ConformingModelTest` row | `docs/architecture/09_verification.md:313` |
| record: README "Standard-conforming models pack" list, and the round-4 plant table | `tb/desc_store/README.md:99-102`, `:202-213` |

The test that fails without it: five stricter L6 readings planted one per copy
(`scripts/l6_plant.py`, `scripts/l6_plants_run.sh`; `receipts/l6_plants.txt`):

| Plant | At `3bfc7c6` (no new test) | At `bd86f64` |
|---|---|---|
| control (nothing planted) | gate passes | gate passes |
| beside a CRF input, at most one INPUT_STREAM source at the AAF inputs together | SURVIVED | KILLED: `test_a_source_per_aaf_input_beside_crf` |
| beside a CRF input, no INPUT_STREAM source at an AAF input | KILLED: `test_boundaries_pack` | KILLED: the new test and `test_boundaries_pack` |
| `clock_sources_count` capped at 8 | SURVIVED | KILLED: the new test |
| `clock_sources_count` capped at 9 | SURVIVED | KILLED: the new test |
| at most two INPUT_STREAM sources in a configuration | SURVIVED | KILLED: the new test |

`milan_min`'s recorded digest and `model_ids.json` are unchanged (`IdentityTest` passes).

## Item 2: re-measured

### Gate and checks

| Command | Head | Result |
|---|---|---|
| `python3 -B tb/desc_store/test_gen_desc_image.py` | merge (uncommitted), `bd86f64` | rc 0: 58, then 59 tests |
| `make -C tb/desc_store lint-suppression` (head export) | `bd86f64` | rc 0: control passes; 56 of 56 checks killed. The log equals round 3's apart from its two directory lines |
| `git apply --check`, every campaign patch (head export) | `bd86f64` | 207 of 207: adp_engine 28, maap 27, pp_top dispatch 37 (main added `sclks-bound-inclusive`, `sclks-bound-three`) and mutations 42, srp_top 73 |
| `make check` | merge, `bd86f64` | rc 0: 41 mermaid + 18 wavedrom, 1,050 links, 115 REQ / 17 GAP, 94 module rows / 0 untested, 27 parameters |
| `python3 scripts/gen_matrix.py --check` | `bd86f64` | rc 0 (94 rows, 0 untested) |
| `git diff --check 97f6eac..HEAD`, `631eeb34..HEAD` | `bd86f64` | clean |

### Processor suites

| Command | Head | Result |
|---|---|---|
| `./scripts/run_suites.sh` (head export) | `bd86f64` | rc 0: 33 suites, 1,019,127 checks, 0 failing; `desc_store` 584, `pp_top` 9,168. Against round 3's log (1,019,110) only `pp_top` moves, by main's 17 D3C checks |
| `./scripts/lint_hdl.sh` (head export) | `bd86f64` | rc 0: 41 tops LINT OK |

Verilator 5.052 (this host). Not re-run, with the reason: the RTL mutation campaigns and
`nvm_port` figures. The merge brings main's `tb/pp_top` and `hdl/` changes byte for byte,
which P141 measured at main, and the lane adds no RTL, harness or patch change. Every
campaign patch still applies (207 of 207).

### Reviewer plant scripts, unchanged from the read-only round-3 packets

| Script | At `bd86f64` | At `97f6eac` (the reviews) |
|---|---|---|
| R434-3 `r3/plant_r3.py` (40) | 40 KILLED | 40 KILLED |
| R434-3 `r2/plant_r2.py` (37) | 37 KILLED | 37 KILLED |
| R434-3 `r2/plant_r435_titles.py` (8) | 8 KILLED | 8 KILLED |
| R434-3 `r1/plant.py` (29) | 24 KILLED, 4 BADPLANT, 1 expected-pass control green | the same |
| R435-3 `r3_plants.py` (16) | 15 KILLED; `g-own-loader` SURVIVED | the same |
| R435-3 `prior-r435-2/r2_plants.py` (37) | 37 KILLED | 37 KILLED |

`g-own-loader` is R435-3's S1 suggestion (pin that `model_rules` loads through the shared
loader), which this merge-only round does not take. Receipts: `receipts/rplants_*.txt`.

### Parent models packed

Five tracked configs, through the builder caller (`endstation_builder._entity_model_image`
with the parent's post-pack checks, then `build()` with `adp=` from the overlay, then
without the waiver), and through `avdecc/gen_aemi_image.py` (the CLI caller). The processor
is at `bd86f64` at both heads; `gptp-processor` 5dce647a, `verilog-axis` 48ff7a7e.

| Model | Clock sources at dev / #634 | dev `cdf49d1a` | PR #634 `0b066b6e` |
|---|---|---|---|
| `endstation_arty_current` | 2 / 3 | packed, 0 waivers, driven ADP values agree | the same |
| `endstation_arty_4x4` | 2 / 6 | packed, 0 waivers | the same |
| `endstation_arty_8ch` | 2 / 6 | packed, 0 waivers | the same |
| `endstation_ax7101_1x1_tdm8` | 2 / 3 | packed, 0 waivers | the same |
| `endstation_ax7101_8x8` | 2 / 10 | packed only with its waiver, listed: `L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0..7: 8 finding(s) waived; reason: kebag-logic/milan-fpga#584` | the same |
| `endstation_ax7101_8x8`, waiver removed | | refused: 8 lines, `L1 port-cluster-minimum` on STREAM_PORT_INPUT 0..7 | the same |
| `endstation_ax7101_8x8`, waiver widened to 0..8 | | refused as stale | the same |

At `0b066b6e` each model's CLOCK_DOMAIN 0 lists INTERNAL 0, CRF 1 and one INPUT_STREAM per
AAF input at 2 + k (`scripts/clock_probe.py`, `receipts/parent_clock_sources.txt`).

The `pack_models.py` and CLI outputs are byte-identical to round 3's at both heads, model
digests included (round 3's #634 head `d81198c2` already carried the sources;
`receipts/pack-*-bd86f64.txt`, `cli-*-bd86f64.txt`, `widen-*-bd86f64.txt`). No model packs
differently, so `parent-adoption-c8-cdf49d1a.patch` is unchanged (sha256
aa5a88eb8e04e5ce0d44ec65973e88215860a9ea5317255016409442000ad209), and so is
`parent-adoption-c4c6-ea3fb388.patch` (sha256
67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c). At #634 the C8 patch's
one `avdecc/aem_assemble.py` hunk does not apply (`git apply --check` rc 1, context
moved). It was ported by its identical one-line edit; the other six files apply
(`receipts/mkparent-pr634.txt`).

## Item 3: parent consumer set (16)

milan-fpga dev `cdf49d1a`, scratch copy `$VALIDATION_STORAGE/c8-a504/parent-dev`
(`scripts/mkparent.sh`; `receipts/mkparent-dev.txt`):
- a `git archive` of the read-only checkout (tree 904f3079, equal to the checkout's), its
  gitlinks recorded;
- `gptp-processor` 5dce647a and `third_party/verilog-axis` 48ff7a7e cloned at their pins
  from fresh scratch bare clones of their upstreams;
- `parent-adoption-c4c6-ea3fb388.patch`, then `parent-adoption-c8-cdf49d1a.patch`, applied
  with `git apply --index` (10 files, +53 −8);
- `protocol-processor` a clone of this branch at `bd86f64`, its gitlink recorded, and
  `git submodule init` run.

| # | Gate | Result at `bd86f64` |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held; 298 Python modules, long function 9 <= 9, long module 10 <= 10, too many parameters 7 <= 7, over-long line 0 |
| 3 | `xvlog_gate.py --check` (alone, after every other build of this run) | rc 0: 4 findings == ratchet, 0 in `hdl/`, pinned at `protocol-processor@bd86f646` |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded) |
| 6 | `sw/builder/test_builder.py` | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11 needs a board utilisation report not on this host). Gate 36b's 67 lines are identical to round 3's |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 646, 606 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0: 3,798 ports; 49 literal-bound, 59 without a rationale (lowerable by 3, as before) |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0: 72 <= 77 suites without a mutation arm, 10 <= 10 unseeded, 0 <= 0 unexplained DUT readers, 3 <= 3 wall-clock files |
| 11 | `docs_check.py` | rc 0, 0 findings across 185 md files |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS (second run, alone) |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

The light gates' last lines are byte-identical to round 3's.

The first `milan_dp` run failed, rc 2, at 20:50:40. It ran beside `test_builder.py`, as
in round 3. The error: `milan_csr.sv:1355: Cannot find include file:
'gen/lwsrp_csr_defaults.svh'` (`receipts/parent_dev_milan_dp_run1_error.txt`). Builder
gates 23j and 23k take that tracked file away and put it back while they run; its mtime
is 20:51:16. After the builder test finished, `milan_dp` was re-run alone and passed. The
failed log is kept (`milan_dp.run1-race.log`, below). Other lanes' builds and an
`xvlog_gate` were also running on the host (not this lane's; separate temp dirs).

## Parent-visible list (round 4)

- No parent model packs differently, no digest moves, and neither parent patch changes.
  All five models at PR #634 `0b066b6e`, with #629's clock sources, pack under the lint.
- One refusal text changes: `L6 domain-source-identity` ends "(IEEE 1722.1-2021 §7.2.32;
  06 §6.4)", where it ended "(IEEE 1722.1-2021 §7.4.23.1; 06 §6.4)". No parent file quotes
  it.
- Text the parent cites moves: the 07 §3.1 L6 row and REQ-MDL-005 (main's restatement
  with the lint's columns), 09 §8.5, and the `tb/desc_store` README. The parent's own L6
  (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89`) and `MEDIA_CLOCK_FOLLOWING.md:204` still
  credit 7.4.23.1. That row is already on the design's documentation list.
- Processor totals at this head: `pp_top` 9,168 and the sweep 1,019,127 (main's P141 plus
  this lane's unchanged figures). No parent file at `cdf49d1a` quotes them.
- No processor or parent port, parameter or interface change.

## Not taken (outside a merge-only round)

R435-3 S1, R434-2 S2 and R434-1 S3/S4 are not taken. The redundant-pair rules stay
unlinted (processor #69).

## Scratch evidence

Small receipts and the scratch scripts are in this directory (`receipts/`, `scripts/`).
Large logs stay under `$VALIDATION_STORAGE/c8-a504/`:

| File | Bytes | sha256 |
|---|---|---|
| `gates-dev/test_builder.log` | 99916 | 6aa0a10f637745afb3b31524a1bf1e21eb3bec67f5ba1441e3b20aab23867a93 |
| `gates-dev/pp_shadow.log` | 293768 | 383064d5c1b2d3162bcdc59591b06b9f99e57b1fefd91e38c539c4db92fc3998 |
| `gates-dev/milan_dp.log` | 1441279 | d3512828f26274c2c5d372e920b243373e6862a448527081edb775a39ab999e5 |
| `gates-dev/milan_dp.run1-race.log` | 606888 | 2cbcc4eaed691b5a20f0709c145d208a3968e2da1eee18c142cd5a27ef420264 |
| `gates-dev/milan_dp_render.log` | 153543 | c2c30c7ec953c1f1c8ca4e9662ece4478940f6f84504568482fb4b59d885c1b5 |

Scratch trees (not in the output directory): `suites/tree`, `applycheck/tree`,
`rplants/head` (exports of `bd86f64`), `plants/` (L6 plant copies), `parent-dev`,
`parent-pr634`, `src/` (bare clones).

## Close

REVIEW READY posted on #60, comment 5959903762, with head
`bd86f6466baa77113eea2266c00044c3a29678f2`. Its text is `receipts/review-ready.md`.
