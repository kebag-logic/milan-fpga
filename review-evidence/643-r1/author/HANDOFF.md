# [A522] HANDOFF: #643, the T30 INTERNAL law against the feed's phase

**Status: REVIEW READY at `98729742b71d5088f250440eb46085daf1c0cbdb`** on
branch `643-t30-phase` (two commits on dev `5fabb46e767c9308ab2580916237f43577698c6e`,
processor pin `631eeb34`). Not pushed, no PR opened (not allowed in this lane).
The suite and docs gates are rc 0 at both processors. The full mutant campaign
is rc 2 at both, on four arms that fail identically at dev's base (section 5,
section 7.7); every arm this change adds or touches passes.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5972861856
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5972870159
- STOP at item 1: https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973437153
- Ruling, option (c): https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973450039
  (mechanism 2 is filed as #647; this lane implements (a), the test-only fix)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5974434363

## Contents

1. [Item 1: the phase sweep inside and after the transient](#1-item-1-the-phase-sweep-inside-and-after-the-transient)
2. [Diagnosis](#2-diagnosis)
3. [The change](#3-the-change)
4. [Proof against both processors](#4-proof-against-both-processors)
5. [The planted-defect control](#5-the-planted-defect-control)
6. [The tie rule, exercised](#6-the-tie-rule-exercised)
7. [Interpretations and observations for the reviewers](#7-interpretations-and-observations-for-the-reviewers)
8. [Gate table](#8-gate-table)
9. [Reproduction](#9-reproduction)
10. [Files in this directory](#10-files-in-this-directory)

## 1. Item 1: the phase sweep inside and after the transient

Measured before the STOP with a scratch diagnostic mode
(`diag-t30-phase-sweep.patch`), unchanged since. 66 feed phases over one
INTERNAL tick (64 even plus +927 and +1,156), each graded by T30's two
INTERNAL LAW checks as they stood at dev (fill at the RX accept pulse = 8;
first-event delay from it in (8, 9] ticks + 64 cycles), in four windows.
**Settled** = the aligner engaged with |err| <= 32 cycles for 2,048 ticks
running (the declared band, `hdl/milan/milan_datapath.sv:6264-6266`).

| Processor | Settled after T14's hold / after T30's feed start | Inside the transient (T30's own window): phases failing of 66 | After settle, same stream | After settle, fresh stream, nominal cadence | After settle, fresh stream, same clock |
|---|---|---|---|---|---|
| dev's pin `631eeb34` | 158.11 ms / 147.95 ms, every phase | **19** (+684..+1,204; +927: fill 68 / band 105 of 292; +1,156: 227 / 284) | **30** | 3 | **1** (+1,693) |
| main `c4cb84ff` (scratch parent) | 158.10 ms / 147.94 ms, every phase | **18** (+0 among them) | **28** | 3 | **2** (+521, +553) |

Every phase, every window and both checks' counts are in
`phase-sweep-tables.md`. T30's window ran +5.0 to +42.5 ms after its feed
started, wholly inside the transient (walk -106.78 ppm at every phase). The
stock leg with `c4cb84ff` failed as #643 reports (227/292 and 285/292).

## 2. Diagnosis

1. **The window opened inside the aligner's pull-in (test).** T14's 5,200-cycle
   serial-clock hold is under the aligner's watchdog, so it stays engaged and
   pulls the INTERNAL grid back for about 150 ms; T30 graded during that pull.
2. **A stream started inside the pull keeps the displacement (design).** Nothing
   re-centres it at INTERNAL. Ruled out of this lane: **#647**.
3. **The accept-pulse instant is phase-sensitive (test).** The PDU's rows land
   in the setpoint stage 28 to 48 cycles after the RX accept pulse; a pop in
   between moves a fill read at the pulse. The stage's own reference is the
   PDU end (`hdl/ieee1722/aaf/KL_render_setpoint.sv:56`, `:73`).
4. **The nominal feed cadence beats the INTERNAL grid by 10.64 ppm since A2-a
   (test).**

The ruling took (a): grade the law only after the aligner's settled report, on
fresh streams at the INTERNAL grid's own cadence, at the stage's PDU end, with
a stated tie rule, over 18 phases; plant A2-a's removal as the defect.

## 3. The change

Two commits, test, docs and suite only. No RTL file is touched.

| Commit | Subject |
|---|---|
| `22f9a244f4d077b4976f39f826a4cc9928f4da12` | Grade T30's INTERNAL law once the aligner reports settled: an 18-phase [LAW] sweep of fresh streams at the render stage's PDU end with a stated tie rule, the A2-a planted defect failing every phase, and the docs (#643) |
| `98729742b71d5088f250440eb46085daf1c0cbdb` | State the milan_dp_render suite's measured wall time with the [LAW] phase: 663.8 s cold under GNU make 4.3, against 560.0 s (#643) |

`tb/verilator/milan_dp_render/sim_tdm8_render.cpp` (at `98729742`):

| Line | What |
|---:|---|
| 100 | Header: the INTERNAL law after settle; `--law-only` among the short legs |
| 177 | `kBandSlackCycles` = 64 kept, its comment restated for the PDU-end reference |
| 184-186 | The settled report as the LAW under test: `kSettleErrCycles` = 32 (2083/64), `kSettleTicks` = 2048, `kSettleCeilTicks` = 32768 |
| 193 | `kLawPhases`: 0, 130, 260, 391, 521, 651, 781, 911, 927, 1042, 1156, 1172, 1302, 1432, 1562, 1693, 1823, 1953 (cycles after an observed media tick) |
| 200-202 | Per phase: a 4-slot gap (drains the stage into prefill), 16 PDUs of prefill, 128 graded (the last 4 ungraded) |
| 601-622 | The law instrument now records the PDU end (`end_at`), the fill once the end beat is in (`fill_end`) and the tie evidence (`tie_pop`); the accept-time `accept_at` / `fill_at` are gone |
| 647 | `observe_pdu_end()`: the end is the accepted clone beat with tlast for stream 0 (`lb_tap_tvalid_w && lb_tap_tlast_w && lb_tap_tuser_w == 0`, the same accepted clone the stage's `pdu_end_w` is made of, `KL_render_setpoint.sv:534`); the fill is read one cycle later (the stage's `fill_end_w`); a stream-0 pop seen 1 or 2 cycles after the end is a tie |
| 703, 719 | `observe_aligner()`: every media tick, `mga_engaged_w` and `mga_err_w` against the band; `settle_run`, `unsettled_ticks` |
| 983 | `kBootPullInCycles` comment: `--law-only` dwells it too |
| 3067-3137 | `prove_the_setpoint_law_still_holds`: fill at every PDU end = 14 (`kPrefillTargetEvt`, the stage's TARGET_C), or 13 with a pop seen +1 / 15 with a pop seen +2 (the tie rule, `:3110`); first-event delay from the PDU end in (8T, 9T + 64]. Shared by the T30 CRF LAW window |
| 3196 | T30's INTERNAL window keeps its pin and A2-a checks; its law call is removed |
| 3256 | `phase_internal_law()`: the INTERNAL resolve check (`int_clk_selected_r` = 1), the bounded wait (32,768 ticks, a cycle guard at twice that), the report check, the 18 phases, then the nominal cadence restored for the later phases |
| 3291 | `grade_the_law_at_a_feed_phase()`: gap, new record, anchor on the next media tick (bounded at one PDU period), first PDU at tick + phase, physical cadence 12,500 + 52/391, prefill, 128 graded; checks: n >= 100, fill, band, and "the aligner held its settled report through the phase" over a grid that really ticked |
| 3762, 3791 | `--law-only`: `[MAP]`, a 0.3 s dwell (see section 7), `[LAW]` |
| 3820 | The full leg runs `[LAW]` after `[CRF]` (T30, T31) and before `[CSR]`; not in `--epoch-only` |

`tb/verilator/milan_dp_render/tdm8_render_mutants.py`: `LAW_PHASES` and
`LAW_SETTLED` (`:117`); the planted defect "A2-a removed: the aligner is not
engaged at INTERNAL", `milan_datapath.sv:5905` `mga_sel_w = follow_sel_r;`,
leg `--law-only`, must fail all 18 per-phase settled checks (`:307`);
`verdict()` accepts a tuple of names, every one of which must fail (`:462`).

Docs: `docs/design/MEDIA_CLOCK_FOLLOWING.md` test section (a `[LAW]` row,
`:1329`, and "The render law's grading instant (#643)", `:1355`: the instant,
the tie rule, #647, the boot pull-in); `tb/verilator/README.md:63` (the
suite's row); `docs/testing/TESTING.md:285-287` (wall time), `:518` (the leg),
`:520` (the campaign: nineteen mutants, 30 checks);
`tb/verilator/milan_dp_render/Makefile:34-38` (wall time).

**Check count.** Shipping leg 155 -> 226: T30 INTERNAL LAW's 3 removed; 2 new
(resolve, report) and 4 per phase x 18 added.

## 4. Proof against both processors

The suite gate, `make -C tb/verilator/milan_dp_render` under GNU make 4.3,
cold, in the lane (dev's pin) and in the scratch parent (`c4cb84ff`, both
patches). Full per-phase rows: `phase-law-tables.md` sections 1 and 2.

| Processor | Suite rc | Shipping leg | Two-stream leg | Leg defects | `[LAW]` wait | Every phase |
|---|---:|---|---|---|---|---|
| dev's pin `631eeb34` | 0 | 226 checks, 0 failing | 65 / 0 | 5 / 5 | 0 ticks (8,626 already in band) | n 124, fill 14..14, 0 ties, 0 ticks outside the band; delays 8.035..8.973 ticks over the 18 phases |
| `c4cb84ff` | 0 | 226 checks, 0 failing | 65 / 0 | 5 / 5 | 0 ticks (8,627 already in band) | identical within 1 to 2 cycles |

The T30 CRF LAW, now at the PDU end: 292 PDUs, fill 14..14, 8.717..8.719
ticks (dev) and 8.162..8.164 (`c4cb84ff`).

`--law-only`, clean: rc 0, 88 checks, 0 failing, at both processors; the wait
after the dwell was 4,014 / 4,013 ticks (`phase-law-tables.md` sections 3, 4).

## 5. The planted-defect control

`milan_datapath.sv:5905` planted as `wire mga_sel_w = follow_sel_r;` in a
scratch copy, built through the suite's own recipe (`DP_SRC=`), run
`--law-only`:

| Processor | rc | Checks | Failing | Per-phase settled checks failing |
|---|---:|---:|---:|---|
| dev's pin | 1 | 88 | 19 | **18 of 18**, plus "reported settled inside the 32768-tick ceiling" (waited the full 32,768 ticks, 0 in band) |
| `c4cb84ff` | 1 | 88 | 19 | **18 of 18**, plus the same |

Fill and band still pass under it at every phase (the free-running beat moves
a phase by about 16 cycles inside a window), so the settled check is the one
that discriminates it, as the ruling planned. `verdict()` reads these logs as
"caught", the clean ones as "pass", and the superseded 14-of-18 run (section
7) as "failed, but not the named check".

**The full campaign**, run from inside the suite directory (see section 7.7
for why not `make -C`), at both processors: **rc 2, 30 checks, 26 PASS,
4 FAIL**, the verdict lines identical in the two trees (44:34 and 45:35).

- **Every arm this change adds or touches passes.** The `--law-only`
  positive control; "A2-a removed" caught at all 18 phases ("breaks ... +0
  ... and 17 more"); the `--crf-only` control, the clock-source-trigger
  mutant and the internal-select arm.
- **The four failures are pre-existing.** Each fails identically with dev's
  own harness at `5fabb46e` (section 7.7):
  1. the `--epoch-only` positive control;
  2. and 3. the two `--epoch-only` clean controls (modelled arrival skew on
     each epoch level), whose only failures are the same four "T30 CRF ...
     recentre" checks;
  4. the `--serial-only` mutant "uncounted repeat", which survives.

## 6. The tie rule, exercised

No standing phase is a tie: the 18 phases put the first-event delay at 8.035
to 8.973 ticks. A scratch scan (`diag-law-tiescan.patch`, `--law-only`,
+2,010 to +2,045 at one-cycle steps) found ties only at:

| Phase | PDUs with a pop seen +1 / +2 after the end | Fill | Delay |
|---|---|---|---|
| +2,025 | 0 / 78 | 14..14 | 8.001..8.002 ticks |
| +2,026 | 108 / 11 | 14..15 (the 11 with the pop at +2 read 15) | 9.000..9.001 ticks |

All 36 phases pass, at both processors identically; no PDU read off 14
without a tie. Without the rule, +2,026 would fail its fill check on 11 of 124
PDUs; its delays (18,751 to 18,752 cycles) are inside the band only through
the 64-cycle slack.

## 7. Interpretations and observations for the reviewers

1. **The phase anchor.** A phase is a delay from an observed media tick, so it
   means the same against the grid at either processor. +927 and +1,156 are
   kept as two more points; they are no longer the shifts #83 made against
   T30's feed start.
2. **The T30 CRF LAW moved too.** It shares the law instrument, so it is now
   graded at the PDU end as well (ruling item 3 states the instant for the
   law, not for one window). It passes at both processors with no tie.
3. **`--law-only` dwells 0.3 s first.** From boot the aligner's error swings
   from -201 cycles through zero to +49, then decays over about 10,000 ticks;
   the crossing spends just over 2,048 ticks in the band, so the declared
   report fired at the crossing (tick 4,366) and the error then left the band:
   the first `--law-only` build failed the settled check at 14 of 18 phases
   while fill and band passed (`phase-law-tables.md` section 7,
   `diag-law-trace.patch`). The settled-grid trigger's comment
   (`milan_datapath.sv:6256`) calls the loop overdamped. This overshoot is
   measured at the INTERNAL boot pull-in only. **For the owner: a design
   observation, not acted on here.**
4. **`--epoch-only` no longer grades the INTERNAL law** (it runs `[CRF]`
   but not `[LAW]`); the full leg and `--law-only` do.
5. **"The suite README".** `tb/verilator/milan_dp_render` has no README of its
   own; its README entry is its row in `tb/verilator/README.md`, which carries
   the documentation, beside `TESTING.md`.
6. **Pre-existing:** `measure_test_evidence.py --check` prints "the mutation
   ratchet can be lowered to 72"; this suite was armed before the change.
7. **Pre-existing campaign defects, for new Issues (not fixed here).**
   - **The documented command fails every arm.**
     `make -C tb/verilator/milan_dp_render tdm8render-mutants` (TESTING.md's
     form) reports every mutant and clean control as "did not compile", under
     GNU make 4.3 and 4.4.1 alike. The outer `-C` puts `w` in MAKEFLAGS; the
     driver's `make -s -C` runs at MAKELEVEL 1; the Makefile's
     `$(shell $(MAKE) -s -C ../milan_dp print-srcs)` then captures
     "make[1]: Entering directory" into the source list. Reproduced with
     `MAKELEVEL=1 MAKEFLAGS='w -- ...'` (6 polluting tokens at either version;
     none with `--no-print-directory` or without the `w`). The first campaign
     run here hit it (`logs r4`, 7 PASS / 23 FAIL); the numbers in section 5
     come from inside the directory.
   - **`--epoch-only` has been red since #629's A2-a.** It runs `[CRF]` with
     neither the serial phase nor the boot dwell `--crf-only` got, so the four
     "T30 CRF ... recentre" checks read 0. Dev's harness: rc 1, 116 checks,
     4 failing; this head: 113 checks, the same 4. Its two clean controls fail
     on exactly those 4 at the base and at this head.
   - **The "uncounted repeat" mutant survives at dev.** Built with dev's own
     harness and the same planted `KL_tdm_render_master.sv`, `--serial-only`
     exits 0 (verdict "pass"); likewise at this head. T6 ORDER does not see it.

## 8. Gate table

Pinned Verilator 5.050 throughout; GNU make 4.3 (release tarball sha256
`e05fdde4...8e19`, built in scratch) for the suite gates and the campaign.

| # | Command | Where | rc | Result |
|---:|---|---|---:|---|
| 1 | `make -C tb/verilator/milan_dp_render VERILATOR=<pinned>`, cold | lane at `22f9a244` (dev's pin) | 0 | 226/0, 65/0, leg defects 5/5; **663.8 s** |
| 2 | the same | scratch parent, `c4cb84ff` + both patches, tree = `22f9a244` | 0 | 226/0, 65/0, 5/5; 680.0 s |
| 3 | base vs new shipping leg, side by side | lane, dev's pin | 0, 0 | 155/0 in 113.0 s; 226/0 in 215.4 s |
| 4 | `--law-only` clean / A2-a planted | dev's pin | 0 / 1 | 88/0; 88/19, all 18 phases |
| 5 | `--law-only` clean / A2-a planted | `c4cb84ff` | 0 / 1 | 88/0; 88/19, all 18 phases |
| 6 | tie scan, 36 phases | both | 0, 0 | 160/0 each |
| 7 | `cd tb/verilator/milan_dp_render && make tdm8render-mutants VERILATOR=<pinned>` | lane at `98729742` | **2** | 30 checks: 26 PASS, 4 FAIL, all four pre-existing (section 5); A2-a caught at 18/18 |
| 8 | the same | scratch parent at `98729742` + patches | **2** | identical verdict lines |
| 8a | the same command as `make -C ...` (TESTING.md's form) | both, at `98729742` | 2 | 7 PASS / 23 FAIL, every built arm "did not compile": the pre-existing MAKEFLAGS defect (section 7.7); superseded by rows 7 and 8 |
| 8b | `--epoch-only`, dev's base harness vs this head | lane | 1, 1 | the same 4 T30 CRF recentre checks fail in both (116 vs 113 checks) |
| 8c | the two epoch-only clean controls, base harness and head harness, built through the driver's own `plant()`/`build()` | lane | 1 each | only the same 4 checks fail, at base and at head |
| 8d | "uncounted repeat" mutant, base harness and head harness, `--serial-only` | lane | 0, 0 | survives at both |
| 9 | docs: `docs_check`, `check_em_dash --base 5fabb46e`, `check_doc_style` (+selftest), `check_gptp_docs` (+selftest), `DOC_MAP.gen --check`, `timesync_chain.gen --check`, `check_solution_docs`, `check_feature_status --self-test`, `gen_module_matrix --check`, `check_doc_paths`, `check_archive`, `gen_toc --selftest / --verify-anchors / --check` | lane at `98729742` | 0 each | the em-dash gate: 0 findings over 38 added lines |
| 10 | code: `check_cpp_idiom`, `check_py_idiom`, `check_hygiene --check`, `check_todo_ownership`, `measure_test_evidence --check`, `check_sh_idiom`, `ci_events --check` | lane at `98729742` | 0 each | |
| 11 | rtl-fast's local half: `lint_rtl.py --check --self-test`, `pp_srcs.py --check --selftest`, `behave` in `tests/` | lane | 0 each | lint 90 <= 90; behave 404 scenarios |
| 12 | `ci_scope.py` on the changed paths | lane | 0 | `true` (RTL/tooling scope, because `tb/` changed) |

Not run: the Yosys elaboration (it reads only `hdl/`, which is unchanged, and
this host's sv2v is v0.0.13 against CI's pinned v0.0.12); `act` (nothing is
pushed).

**Scratch parent** (`$VALIDATION_STORAGE`, never committed): a `git archive` of
`22f9a244`, every path in the index and no commit; `protocol-processor` at
`c4cb84ff8cecad19bedaa85dde594a8ed68012f6` (still the processor's `main`,
by `ls-remote`), cloned from the fetch of
https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git;
`gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, `external`
`efeb541a` as gitlinks; each submodule's toplevel is its own directory. Both
patches applied with `git apply` after a clean `--check` (8 files,
+110/-39). After the second commit its two changed files were copied in; then
986 tracked files are byte-identical to `98729742`, the 8 patched ones differ,
998 index entries.

## 9. Reproduction

```sh
git checkout 98729742b71d5088f250440eb46085daf1c0cbdb   # with the three submodules at their pins
make -C tb/verilator/milan_dp_render VERILATOR=<pinned verilator 5.050>
# the [LAW] short leg, and the planted defect through the campaign
make -C tb/verilator/milan_dp_render tdm8render-build VERILATOR=<pinned>
(cd tb/verilator/milan_dp_render && ./obj_tdm8r/Vmilan_dp_tdm8r --law-only)
(cd tb/verilator/milan_dp_render && make tdm8render-mutants VERILATOR=<pinned>)   # not make -C: see section 8
# the tie scan / the aligner trace (scratch, never committed)
git apply diag-law-tiescan.patch   # or diag-law-trace.patch, run with DIAG_ERR=1
```

## 10. Files in this directory

| File | Bytes | sha256 | What |
|---|---:|---|---|
| `HANDOFF.md` | | | this file |
| `PR-BODY.md` | 9,181 | `7c072a7a08bd73589a82d018223053e7741c7fef47c1db25d1e80a8575471b61` | the PR body ("Closes #643", "Relates to #629", "Relates to #647") |
| `phase-law-tables.md` | 24,282 | `2c988cb2632025c48db92c485368e932c2910bb7cef1ec825000818d267bac3c` | the `[LAW]` rows per phase: both processors, clean, planted, the superseded boot run, the tie scan |
| `phase-sweep-tables.md` | 38,288 | `a942b0e3241b9c4857efa0cb5fc24547f26f908eda772cb685944b2cbe87f907` | item 1: every phase, every window, both processors |
| `diag-law-tiescan.patch` | 2,097 | `a976ea6d4ac0449712fd23469238fbbcacbca3237330b112c9a308489da143a9` | scratch: the 36-phase tie scan with the per-side tie counts |
| `diag-law-trace.patch` | 813 | `3ef69af125d18f51aa6cd8bf50adf8952ae7d9751d407fa12003da9135a0160a` | scratch: the aligner error every 256 ticks under `DIAG_ERR=1` |
| `diag-t30-phase-sweep.patch` | 11,629 | `6fd302811f5dbf1f86c6e4b7b26142ef0981c4dbdf0ae71bba39823bb16d7501` | item 1's diagnostic harness, against dev |
| `parent-adoption-c8-bbf704ec.patch`, `parent-adoption-p2-p1-1269cdaf.patch` | 8,546; 24,711 | `3340d2e8...8a4c`, `d3034e89...3d84` | inputs, unchanged |
