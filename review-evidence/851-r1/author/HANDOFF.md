# HANDOFF: milan-fpga issue #851, [A744]

Status: **REVIEW READY** at `2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a`. Every gate below ran on a clean clone of this exact
head and exited 0; the shipping route fits and meets the floor at this head. Nothing is pushed. One judgement call for
review: Findings item 1 (all three resource endpoints re-recorded).

- Repository: milan-fpga, origin https://github.com/kebag-logic/milan-fpga.git (checked), branch `851-adopt-pp-044cb25f`.
- Base: dev `1eb5289db8fc9d139ce90cad2e380b4515793806`, also the merge base. `origin/dev` had not moved at the last fetch.
- Head: `2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a`, six commits, one-line subjects, no body, no trailers. Nothing pushed.
- Processor: `protocol-processor` (origin https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git,
  checked with its top level before every git command in the submodule) moves `92100657` ->
  `044cb25f4ed2187bd238490650e73d5d189855d1`, processor `origin/main`, the merge of PR #215 (parents `92100657`, `7feeccea`);
  its tree `60300bb0` equals `7feeccea`'s.
- TAKEN: issuecomment-6711626333. REVIEW READY: issuecomment-6714940292 (`receipts/records/review-ready.md`).

## Commits

| Commit | Subject (abridged) |
|---|---|
| `1bf061bf` | gitlink `92100657` -> `044cb25f` |
| `a566d4f9` | ROM digests (recorder), pin-table row, boundary diagram (generator) |
| `230e4223` | `syn/ooc/pp_resource_baseline.json`: three endpoints through `pp_resource_gate.py record --write`, then the three `measured` notes |
| `39f4c427` | pin page, CHANGELOG, integration contract |
| `405f1587` | the fourteenth resource record: AREA_BUDGET, MARK_II plan, #234 finding page, findings index |
| `2d939d2d` | documentation audit (generator) |

`git diff --name-only a566d4f9 2d939d2d` lists documentation and `syn/ooc/pp_resource_baseline.json` only, so no synthesis
input changes after the measured commit. The exact-head route confirms it (Route, below).

## The processor change, as read at the pin

- `git -C protocol-processor diff --name-only 92100657 044cb25f -- hdl` is `hdl/srp/KL_srp_encoder.sv` alone. No port or
  parameter change; only the `ev_ready_o` comment and the banner change in its declarations. `protocol_processor_top.sv`,
  `KL_pp_shadow.sv` and `milan_datapath.sv` are unchanged.
- The pending tables hold one entry per value; a push for a pending value rewrites its entry in place (`merge_ev_f`); the
  value is found by searching the table one entry per clock through the RAM's own read port before the push is accepted.
- The shipping elaboration binds `N_STREAM_IN_P` = `N_STREAM_OUT_P` = 2 (the route's `vivado.log`), so the processor's
  "2x2" statements (its docs 10, Section 3) are the shipping image's.
- Both ROM digests at `044cb25f` equal the `92100657` rows (ltn `23cc67ee...`, ucode `49a993be...`).

## Changes (file:line at the head, and the clause each states)

| # | File:line | Change | Clause / source |
|---|---|---|---|
| 1 | `protocol-processor` (gitlink) | `92100657` -> `044cb25f` | processor #214 / PR #215 |
| 2 | `syn/yosys/rom_digests.tsv:9-10` | two rows for `044cb25f`, by `./syn/yosys/ooc.sh --record-rom-digests` | equal to the `92100657` rows |
| 3 | `docs/reference/SUBMODULES.md:25` | the processor pin row (verified by `scripts/check_submodule_docs.py`) | - |
| 4 | `docs/diagrams/submodule_boundaries.{svg,drawio,png}`, `PNG_MANIFEST.json` | `python3 docs/diagrams/submodule_boundaries.gen.py` | - |
| 5 | `docs/reference/SUBMODULES.md:635-780` | the #851 adoption: the rule, the value identity, the merge table, the search's cases at the shipping shape, unchanged ports and ROMs, the shipping route, the gate and its record | IEEE 802.1Q-2022 10.7.7, 10.7.5.13 c), 10.8.2.10.1, Table 10-3, 10.7.6.3, 10.7.6.5, 10.7.6.12, 35.2.2.8, 35.2.2.8.1 a), 35.2.2.8.2, 35.2.2.9.1, 11.2.3.1.7; Milan v1.2 4.2.7.1.1 Table 4.3; BUILDING.md section 5 |
| 6 | `CHANGELOG.md:11`, `:57-92` | contents entry and the section | the same |
| 7 | `docs/integration/INTEGRATION_GUIDE.md:89-109` | the integrator-facing contract | the same, and Milan v1.2 Table 4.3 (joinTime 200 ms) |
| 8 | `syn/ooc/pp_resource_baseline.json` | `route-1x1`, `ooc-1x1`, `ooc-8x8` records by `pp_resource_gate.py record --write`; the three `measured` notes (lines 451, 919, 1377) by `scripts/set_measured.py`, since the recorder leaves them; it refuses unless only the notes differ | maintainer decision of 2026-11-06 (#845 issuecomment-6689114981) |
| 9 | `docs/design/AREA_BUDGET.md:13`, `:125-128`, `:145-155`, `:172-173`, `:191-215`, `:228-231`, `:632-636` | the fourteenth record: intro, record list, the table, the #851 gate block with its directive table, critical path and the #845 image moved into history, allocation, record history | the same decision; BUILDING.md section 5 |
| 10 | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:13-14`, `:19-20`, `:26-27`, `:49-156` | the fourteenth record's section, intro and contents | precedent `23c34dde` |
| 11 | `docs/design/MARK_II_AREA_PLAN.md:59`, `:938-939`; `docs/findings/README.md:25` | the current record's figures and anchor | precedent `23c34dde` |
| 12 | `docs/DOCUMENTATION_AUDIT.md:276` | `scripts/docs_inventory.py --write`: the integration contract now cites 802.1Q | generator |

Clause texts were read from the standards (802.1Q-2022, Milan v1.2 consolidated); `docs/spec-refs.md` does not exist at
this head. 35.2.2.8's "MSRP does not support changes in any of the FirstValue fields for an existing StreamID" was checked
before stating it.

**No new check is added to the tree**, so there is no planted mutant of this lane's own. The behaviour is graded in the
processor (srp_encoder PV1 to PV20, srp_top OV0 to OV10, the campaign's `second-queueing` arm, 314 of 314 at `7feeccea`).
The parent's SRP-reading campaigns were re-run with their planted arms (Gates).

## Gate table (head `2d939d2d`, each group on its own clean clone; every rc read from its log)

| Gate | Command | Result |
|---|---|---|
| Full sweep, 4 shards | `native-shards.py`'s four units, spec `MAKEFLAGS=-j4 --no-print-directory`, pinned tools | rc 0 each: 15+17+17+16 = **65 suites passed, 0 failed, 0 timed out; 2,192,502 checks, 0 in-suite failures**. `capture_coherence` in shard 2, on 4 CPUs (112-115): 42 of 42, about 2,100 s of 2,400. Preflight passed in every shard (`suite cancellation: PASS`); the #833 case did not occur |
| milan_dp (shard 0) | sweep | 12,075 `[ok]`, 1,301 `[PASS]`, 0 `[FAIL]` |
| Firmware self-test | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard k/4`, k = 0..3 | rc 0 each: `test_ctrl_firmware: PASS`; control campaign 523 of 523 caught; shard 3 holds both SRP campaigns |
| Firmware unit job's other steps | `tally_selftest.py`; `ci_rv32_sdk_selftest.py` and `ci_rv32_sdk.py --verify-only`; `fw_rv32_selftest.py --require-rv32`; `test_ctrl_nvm.py --require-rv32 --jobs 8` | rc 0: 18 of 18; 25 tests OK and SDK verified (archive `d42680e9...`); 17 checks PASS; OK across 5 shapes, 435 tests |
| `fw_coverage.py --check` | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8` (and `--selftest`) | rc 0: "firmware coverage: PASS (30 files)"; self-test 29 of 29 |
| Firmware boundary / verilator | `ctrl_boundary.py --require-rv32 --selftest --without verilator` (LiteX-pinned venv) / `--only verilator` | rc 0, `ctrl_boundary: PASS` each |
| Builder | `python3 sw/builder/test_builder.py --require-rv32` | rc 0: "ALL GATES PASS EXCEPT 17 NOT RUN" (no LiteX interpreter) |
| Builder, LiteX chain | the same with `MILAN_LITEX_PYTHON` set | rc 0: "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 1b: this make does not re-read MAKEFLAGS; gate 11: no Arty mf48 build tree) |
| behave | `cd tests && behave --no-capture -f plain` | rc 0: 14 features, 508 scenarios, 2,330 steps passed |
| docs.yml, every `run:` step | `run_docs_yml.py` per job on a fresh clone, `verify_docs_yml.py` | verifier rc 0: **65 steps ran rc 0, 31 not run with a stated reason, 0 bad**; every job's tree clean after (`receipts/docsyml-2d939d2d/docs-yml-table.md`) |
| docs inventory | `python3 scripts/docs_inventory.py --check` | rc 0: fresh, 547 lines |
| `git diff --check` | `git diff --check 1eb5289d HEAD` | rc 0, no output |
| rtl-fast scope | `ci_scope.py --selftest`; classify | rc 0; RTL/tooling relevant: `true` |
| rtl-fast verilator-lint | `lint_rtl.py --check --self-test --jobs 8`; `pp_srcs.py --check --selftest` | rc 0: 89 <= ratchet 89; 46 sources derived |
| rtl-fast yosys-elaboration | `syn/yosys/run.sh --mode elaborate --no-structural` (3 tops); `ooc_selftest`, `guard_selftest`, `cache_selftest`; the OOC read-set and gate self-tests with `check-baseline` | rc 0 each: RESULT PASS; 75 arms; 36 controls; cache OK; baseline PASS, 3 endpoints |
| rtl-fast publication-census | `publication_census.py --check --selftest --jobs 8` | rc 0: 0 of 31 rules no arm proves |
| `check_cpp_idiom.py` | plain, `--list`, `--selftest` | rc 0: every rule 0 <= 0; 75 of 75 |
| xvlog gate | `XVLOG=<vivado>/bin/xvlog python3 scripts/xvlog_gate.py --check` | rc 0: PASS, 0 findings |
| ROM ledger | `./syn/yosys/ooc.sh --record-rom-digests && git diff --exit-code -- syn/yosys/rom_digests.tsv` | rc 0: the recorder reproduces the committed rows |
| Submodule docs | `check_submodule_docs.py`; `submodule_boundaries.gen.py --check` | rc 0: 6 exact gitlinks; diagram OK |
| SRP-reading campaigns | `make -C tb/verilator/milan_dp crflic-mutants`, `gsi-mutants`, `unb-mutants` | rc 0: 10 of 10; 15 of 15 (clean leg 499, every arm's count as recorded); 6 of 6 (clean leg 499, as recorded) |
| Resource gate | `pp_resource_gate.py check` on the three endpoints, against the new record; `check-baseline` | rc 0 each |
| Exact-head route | below | rc 0: equal to the `a566d4f9` measurement in every figure |
| Push privacy check | `push-privacy-check.py <lane> 1eb5289d` | rc 0: 0 private lines |

No campaign count moved: `gsi-mutants` reads 7, 7, 7, 7, 24, 50, 16, 2, 3, 3, 3, 3, 1, 1 failures and `unb-mutants` 4, 2,
2, 2, 2, as the milan_dp README records, so nothing was re-recorded there.

## Route

Shipping recipe, one directive, under `2026-09-23/vivado-slot.sh` and `build-dev.sh` with `SEEDS=eppo --no-capture` (no
board step; nothing flashed): `configs/endstation_ax7101_1x1_tdm8.yaml`, synthesis AreaOptimized_high, opt ExploreArea,
placement ExtraPostPlacementOpt, Vivado 2026.1, at most 32 threads. One route at a time for this lane, never beside its
sweep.

| Figure | #845's route, `519d9c2b` | `a566d4f9` and `2d939d2d` | Change |
|---|---:|---:|---:|
| Slice LUT | 52,497 | 53,033 | +536 |
| Slice register | 54,579 | 54,729 | +150 |
| Slice, of 15,850 | 15,780 | 15,792 (58 free) | +12 |
| Block RAM tile | 87.5 | 87.5 | 0 |
| DSP | 13 | 13 | 0 |
| WNS, Slow_0C / Slow_85C | +0.198 | +0.044 | -0.154 ns |
| WNS, Fast corners | +1.590 | +1.408 | |
| WHS, worst (Fast) | +0.015 | +0.035 | +0.020 ns |
| Routing errors | 0 | 0 | |

It fits, and the floor (BUILDING.md section 5: WNS >= +0.03 ns and WHS >= 0 at every corner) is met, WNS by 0.014 ns. Worst
setup path `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][0]` to `.../u_aecp/u_d3/deb_cnt_r_reg[17]`, 36
logic levels, 20 ns processor clock, outside the encoder. The change includes dev's PRs #841 (datapath RTL) and #842
(configurations and firmware), merged after `519d9c2b`.

The `2d939d2d` route equals the `a566d4f9` route in every figure (`receipts/route-2d939d2d/head-2d939d2d.json` against
`receipts/route-a566d4f9/head-a566d4f9.json`); its generated top is identical with comments removed and the build names
normalised, and its three memory images are byte-identical (`generated-verilog-identity.txt`). The recipe's own
ExtraPostPlacementOpt route (single-thread synthesis) reproduces it too.

**Resource gate** (recipe form, `--single-thread-synthesis`, measured at `a566d4f9`):

| Endpoint | `check` vs thirteenth record | Figures |
|---|---:|---|
| `route-1x1`, ExtraTimingOpt selected (+0.258) over ExtraPostPlacementOpt (+0.044) and AltSpreadLogic_high (+0.028) | **1** | LUT 53,050, **+521 of +500**; FF +147 of +600, slices 15,831 (-4; 19 free), RAM, DSP, WNS -0.115, WHS +0.024 pass; every corner meets the floors |
| `ooc-1x1` | 0 | LUT 25,199 (+203 of +250), FF 21,010 (+76 of +250) |
| `ooc-8x8` | 0 | LUT 37,048 (+184 of +316), FF 32,116 (+80 of +339) |

Sub-block rows (not gated): `u_pp/u_srp/u_encoder` +101 / +99 (route), +78 / +75 (`ooc-1x1`), +105 / +71 (`ooc-8x8`).
AltSpreadLogic_high misses the WNS floor at its slow corners (+0.028 ns); the gate judges the selected route against the
floors, and the shipping image is built from it (BUILDING.md section 5).

## Findings and judgement calls (published here, not resolved)

1. **All three endpoints re-recorded, though only `route-1x1` was refused.** The maintainer decision re-baselines "if the
   gate refuses"; it refused the route. I re-recorded both standalone endpoints too, so the record holds one processor pin,
   as every earlier record does (#632's record re-recorded two unchanged standalone endpoints). The alternative, the route
   alone, is one `git checkout 1eb5289d -- syn/ooc/pp_resource_baseline.json`, then `record --write` for `route-1x1` only,
   and the matching doc edits. A reviewer may prefer it: re-recording a passing endpoint absorbs +203 and +184 LUTs of
   tolerance without a refusal.
2. **The adoption's own share of the route growth is not measured.** No dev `1eb5289d` route exists on this recipe. The
   daily route read +246 LUTs and +10 FFs for #841 (`cc204c6f` to `3f6bef88`); #842 was not measured alone. The
   standalone endpoints are this adoption's alone: the wrapper's bound parameters equal the thirteenth record's but for
   the ROM file paths, whose images are byte-identical.
3. **WNS margins.** The one-directive shipping route meets the floor by 0.014 ns; AltSpreadLogic_high misses it by 0.002 ns.
   The selected ExtraTimingOpt route has 0.228 ns. 19 slices remain on it.
4. **PR #846 (the gPTP pin) will conflict** in `syn/ooc/pp_resource_baseline.json`, `docs/design/AREA_BUDGET.md`, the #234
   finding page and the pin page; whichever merges second re-measures and re-records on the other.
5. The [A10]-era note that a re-export does not reproduce a record's `inputs_sha256` (the LiteX module-tree comment
   order) still applies; this record's digests are the measured exports'.

## Process notes

- **CPUs.** This session's unit holds 32-39; every Vivado run, the firmware, rtl, campaign, builder and docs gates ran on it.
  Sweep shards booked by `scripts/pick4.py`, which applies `cpu_ranges.pick8` to the live busy set plus each earlier pick
  (four calls of `pick` alone return the same range): 24-31, 120-127, 112-119 (shard 2 used 112-115 only), 104-111.
  `receipts/records/cpu-booking.txt`.
- **Memory.** This session's unit stayed under 2 GB. The two build-dev routes ran in their own units (24 GB cap) and peaked
  at 17.3 and 17.4 GB, over the 12 GB target, as #845's did (Vivado's 32-thread synthesis); no OOM. The recipe runs
  peaked at 8,256 MB (Vivado's own report).
- **Vivado overlap.** `ooc-8x8` (synthesis, not a route) ran in a second slot beside the first shipping route; no two routes
  of this lane overlapped, and no route ran beside the sweep (the exact-head route was held until all four shards ended).
- **Corrected in this session**, each before its result was used:
  - the route queue's `pgrep` matched my own polling shell (the pattern in its text); I stopped writing it in polling commands;
  - the build clone's `git fetch` recursed into lane-path submodules; `fetch.recurseSubmodules false` in that scratch clone;
  - the first `ooc-8x8` chain shared a clone with the 1x1 chain, whose export re-pointed `sw/builder/out`; re-run in its own
    clone (attempt kept in scratch);
  - my composite SDK gate verified the SDK through a symlinked `HOME` path and failed provenance (rc 1, kept as
    `fw_rv32_sdk_selftest.symlinked-path.*`); re-run at the real install path, rc 0. The firmware gates compiled with the
    same verified bytes through that link;
  - the first docs.yml run (`receipts/superseded/docsyml-2d939d2d-r1/`) had 5 bad steps, all environmental: no `wavedrom`
    in my venv, the SDK step refusing the symlinked `HOME`, and docs-gates-0's gate-receipt step whose id moved from
    `ci_step_54` to `ci_step_55`. Rerun on a fresh 3.12.3 venv whose pip config applies `ci/constraints-ci.txt` (the jobs'
    `PIP_CONSTRAINT`), with `wavedrom==2.0.3.post3` as the install step does, and a fresh `HOME` where the SDK step
    installs and verifies the SDK. `not_run.json` moves `ci_step_54` to `docs-gates-0/ci_step_55` with legs 1 and 2's reason.
- Tools: Verilator 5.050, Yosys 0.66, sv2v 0.0.12, GNU Make 4.3, GoogleTest 1.14.0, the pinned RV32 SDK (GCC 14.3.0),
  CPython 3.12.3 venvs of `ci/constraints-ci.txt`, Vivado 2026.1 (`receipts/records/tool-versions.txt`).
- Scripts are in `scripts/`; receipts in `receipts/`, indexed by `receipts/INDEX.md` (generated from the files present).
  Logs over 200 KB are a masked tail plus size and SHA-256 in that directory's `RAW-RECORDS.txt` or `large.sha256`.

## Not done (by the assignment's rules)

No push, no PR creation or edit, no merge or rebase, no comment edits, no other issue posts, no project-field change, no
hardware or bench access, no flashing, no sub-agents.
