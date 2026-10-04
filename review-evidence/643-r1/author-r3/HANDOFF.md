# [A522] HANDOFF: #643, the T30 INTERNAL law against the feed's phase

## Round 3: REVIEW READY at `36207e91c81fd33782b01486e3bc2fea50e91a1e`

Answers R456-2 and R457-2, both NEGATIVE on one shared MINOR (the stated
spread), under the
[round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5976170456).
Branch `643-t30-phase`, not pushed (not allowed in this lane). Every item is
met. The suite, the boundary diagnostic and the docs gates are rc 0 at both
processors. The full campaign is rc 2 at both on the same four pre-existing
arms as rounds 1 and 2; every arm this round touches passes.

- R456-2: https://github.com/kebag-logic/milan-fpga/pull/648#issuecomment-5976136338
- R457-2: https://github.com/kebag-logic/milan-fpga/pull/648#issuecomment-5976168264
- Their packets: `643-review-evidence` at `91603c66` (`review-evidence/643-r1/reviews/R456-2`, `R457-2`).
- REVIEW READY (round 3): https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5977016377

History on top of round 2's `6b96391d`, no rebase, no amend. Dev is still
`241f91845230ae410506dffb16b71937127fd175` (`ls-remote`), already merged.

| Commit | What |
|---|---|
| `ca3db9f3ecf160ca5555136859c6026af87b5628` | the walk measured as defined, W = 5 + 4 = 9, the per-window walk in the diagnostic, the CRF span and ceiling-check wording, the stray quote |
| `36207e91c81fd33782b01486e3bc2fea50e91a1e` | docs only: `MEDIA_CLOCK_FOLLOWING.md`, `TESTING.md`, `tb/verilator/README.md` |

### R3.1 Item 1: measure as defined, S re-derived, W = 9

**The measure** (`tb/verilator/milan_dp_render/sim_tdm8_render.cpp` at the head):

| Line | What |
|---:|---|
| 184-199 | The comment states the walk as the end-to-nearest-pop offset's range over the window's steady ends (`EndOffsets::walk`), measured at most 3 in a `[LAW]` phase and 5 across T30's CRF window at dev's pin; `kLawWalkCycles` 4 -> **5**; `kLawGuardCycles` **4** (that line kept byte-identical, so R456's guard probes still apply); `kLawAmbiguityCycles` = **9** |
| 1433-1453 | `EndOffsets`: `walk()` was `min(nearest range, next range)`; it is now the **nearest pop's range** (`dmax - dmin`). `walk_wraps()` is true only when that range exceeds half a tick, i.e. the ends sit half a tick from the grid and the nearest pop changes side; only then is the walk the first pop after's range (R457-2's suggested fix). No window in any log of this round or the published ones wraps |
| 3236-3265 | `the_window_is_gradable()`: the offsets line is byte-identical in format up to `margin N` (both reviewers' parsers read it); only when the range wraps it appends "; the nearest pop changes side half a tick from the grid, so the walk is the first pop after's range". The histogram line, `    if (law_boundary) print_the_offset_histogram(...)`, is kept byte-identical (R456's `crfhist` edit) |

**S re-derived from every published window** (`rederive.py`: the nearest-pop
range from each offsets line, and from each histogram line where printed;
grouped by processor, design and window kind):

| Source | Windows | Sound design: largest walk | Where |
|---|---:|---|---|
| R456-2 + R457-2 receipts (round-2 head), dev's pin | 829 sound | CRF **5**; `[LAW]` standing 2; boundary 3 | CRF -592..-587 (`suite-p631.log`, `hp-crfhist-full.log`: `-592:3 -591:32 -590:54 -589:71 -588:106 -587:26`) |
| the same, `c4cb84ff` | 464 sound | CRF 4; `[LAW]` standing 2; boundary 3 | CRF +336..+340 |
| round 2's item-1 scan (`law-boundary-scan.md`, histograms) | 486 | boundary 3 | descending and alone |
| this round (suites, `--law-only`, `--crf-only`, both packets rerun), dev's pin | 847 sound | CRF **5**; `[LAW]` standing 2; boundary 3 | the same CRF window, now printed `(walk 5)` |
| the same, `c4cb84ff` | 483 sound | CRF 4; `[LAW]` standing 2; boundary 3 | |
| this round's two diagnostics (rows 5 and 6 of R3.5), from their own per-window lines | 564 per processor, 188 sound | boundary 3 | "the largest walk over 564 windows is 3 cycles" |

No window wraps (0 of 1,903 published, 0 of 1,976 this round). In this
round's logs the printed walk equals the nearest-pop range in every window
(0 of 1,976 differ; 165 of the published 1,903 differed under the old
`min`). The only walks above 5 are planted defects whose grid moves: A2-a
removed (18, at every phase) and the no-dwell probe (11, at two phases), and
every one of those windows fails its settled-hold check. **S = 5**, the CRF
window at dev's pin; **W = S + 4 = 9**.

**The standing margins at W = 9** (`margin` = least clearance - 9; every
standing window gradable, its check passing; fill 14..14 at every graded end):

| Window | dev: nearest pop, walk, clearance, margin | `c4cb84ff`: nearest pop, walk, clearance, margin |
|---|---|---|
| T30 CRF (292 PDUs), full leg | -592..-587, **5**, 587, **578** | +336..+340, 4, 335, **326** |
| T30 CRF, `--crf-only` | -1021..-1018, 3, 1018, 1009 | -94..-91, 3, 91, 82 |
| `[LAW]` +0, full leg / `--law-only` | -59..-57, 2, 57, **48** / -58..-56, 2, 56, **47** | the same |
| `[LAW]` +130 | -189..-187, 2, 187, 178 | -189..-187, 2, 187, 178 |
| `[LAW]` +260 | -319..-317, 2, 317, 308 | -319..-317, 2, 317, 308 |
| `[LAW]` +391 | -450..-448, 2, 448, 439 | -450..-448, 2, 448, 439 |
| `[LAW]` +521 | -580..-578, 2, 578, 569 | -580..-578, 2, 578, 569 |
| `[LAW]` +651 | -710..-708, 2, 708, 699 | -710..-708, 2, 708, 699 |
| `[LAW]` +781 | -839..-838, 1, 838, 829 | -840..-838, 2, 838, 829 |
| `[LAW]` +911 | -970..-968, 2, 968, 959 | -970..-968, 2, 968, 959 |
| `[LAW]` +927 | -986..-984, 2, 984, 975 | -986..-984, 2, 984, 975 |
| `[LAW]` +1042 | +983..+985, 2, 982, 973 | +982..+984, 2, 981, 972 |
| `[LAW]` +1156 | +869..+871, 2, 868, 859 | +868..+870, 2, 867, 858 |
| `[LAW]` +1172 | +852..+854, 2, 851, 842 | +853..+854, 1, 852, 843 |
| `[LAW]` +1302 | +722..+724, 2, 721, 712 | +723..+724, 1, 722, 713 |
| `[LAW]` +1432 | +593..+594, 1, 592, 583 | +593..+595, 2, 592, 583 |
| `[LAW]` +1562 | +463..+465, 2, 462, 453 | +462..+464, 2, 461, 452 |
| `[LAW]` +1693 | +331..+333, 2, 330, 321 | +332..+333, 1, 331, 322 |
| `[LAW]` +1823 | +202..+203, 1, 201, 192 | +202..+204, 2, 201, 192 |
| `[LAW]` +1953, full leg / `--law-only` | +72..+74, 2, 71, 62 / +73..+74, 1, 72, 63 | +72..+73, 1, 71, 62 / +73..+74, 1, 72, 63 |

**The setpoint +/-1 mutants still fail every graded standing phase**: the
campaign's two arms, `caught` against all 36 named fill and band checks at
both processors (R3.5 rows 3-4); R456's `hp-/c4-spm1-law`, `-spp1-law`
(106/36) and R457's `arm-*-sp-low/-high` (`caught`, 0 named checks not
failing) at both; under `--crf-only` both fail the CRF fill and band checks.

**The boundary diagnostic at W = 9**, both processors identical (rc 0, 81 of
81; every window in `round3-boundary-walks.md`):

| Design | The leg's own scan (+0, then +1,986..+2,066) | Descending | Each of +2,014..+2,038 alone |
|---|---|---|---|
| unmutated | 61 graded, all pass; not gradable +2,015..+2,035 | 60 graded, all pass; not gradable +2,016..+2,036 | +2,014 and +2,038 graded and pass; +2,015..+2,037 not gradable |
| setpoint one event low / high | 61 graded, every one failing fill and band; the same band | 60 graded, all failing both; the same band | +2,014, +2,038 graded and failing both; the same band |

Against round 2 (W 8 -> 9) exactly the phases whose least clearance is 9
left grading: +2,015, +2,016 and +2,035 ascending; +2,016, +2,035 and +2,036
descending; +2,015 and +2,037 alone. Their clearances are identical to round
2's (R457's histories, both rounds, both processors): the simulation is
unchanged. Each scan still holds both kinds. The defects show the
same offsets, walks and not-gradable phases as the sound design in every
history. Over 288 graded sound-design windows (both packets and both suites)
the first event landed at least 10.00 cycles inside the band's upper edge and
12.33 inside its lower one; the design page now states that measured figure.

### R3.2 Item 2: the re-measure, checkable

`tb/verilator/milan_dp_render/tdm8_render_mutants.py` at the head:

| Line | What |
|---:|---|
| 70-76 | The module docstring: `--law-boundary` prints every window's nearest-pop range and walk and the largest walk against the stated one |
| 467-469 | The `LAW_BOUNDARY_*` comment says the same |
| 482-485 | `OFFSETS_LINE` reads the harness's own offsets line; `STATED_WALK_LINE` reads "a walk of N" from the leg's `[LAW-BOUNDARY]` header |
| 764-768 | `window_walks()`: (phase, nearest-pop low, high, walk, least clearance) of every window a run printed |
| 771-783 | `print_the_largest_walk()`: "the largest walk over N windows is W cycles (design, history, +phase); the leg states a walk of S" |
| 786-813 | `judge_boundary_rounds()`: under each run's verdict line, `[i]   +p: <outcome>; the pop nearest the boundary a..b (walk w), least clearance c`. Print only: no verdict, judge or tally changes, so R457-2's offline `judge_test.py` reads ALL OK |

At both processors the output ends: `[i] law boundary: the largest walk over
564 windows is 3 cycles (the unmutated gateware, descending, +2066); the leg
states a walk of 5`, then `81 checks: 81 PASS, 0 FAIL`.

### R3.3 Item 3: docs to the measured figures

| File:line (head) | Change |
|---|---|
| `sim_tdm8_render.cpp:184-199` | the suite comment (R3.1) |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:1329` | the `[LAW]` row: the ceiling counted from the start of `[LAW]`'s own wait (R456-1 S3) |
| `:1330` | the diagnostic row: every window's nearest-pop range and walk, the largest beside the stated one |
| `:1371` | "walks by up to 5 cycles" |
| `:1376-1381` | **The walk** defined: the nearest pop's range over the steady ends, printed beside that range; the half-tick exception |
| `:1382-1389` | **Measured**: 3 in every `[LAW]` phase; the CRF window 5 at dev's pin (-592..-587) and 4 at `c4cb84ff` (+336..+340); stated against the larger, 5 |
| `:1390-1394` | **The window**: 5 + 4 = 9 cycles |
| `:1395-1403` | margins 47 and 48 at +0; the CRF window's clearance 587 and 335; its span leaves out the settled recentre's re-snap end (R456-2 S1) |
| `:1404-1414` | **If T30's CRF window is not gradable** (R456-2 S3): its place moves with the processor and history (-587 / +336 in the full leg; -1,018 / -91 under `--crf-only`); how the failure reads; a placement fault fixed in the test, never by narrowing the window or dropping the check |
| `:1415-1420` | the band edges: at least 10 cycles inside both, measured |
| `docs/testing/TESTING.md:270` | the campaign's command from inside the suite directory (R457-2 S1) |
| `:521` | the 9-cycle window; the ceiling counted from the wait's start |
| `:523` | the campaign run from the suite directory; the diagnostic's per-window walk and largest walk; both targets from the suite directory and why |
| `tb/verilator/README.md:63` | the 9-cycle window; the target prints every window's walk |
| PR body, Known limitations | W = 9 = 5 + 4, tolerance 10, the margins, the CRF window's place, the probes that do not apply |

### R3.4 Item 4: suggestions

| Suggestion | Taken? | Where |
|---|---|---|
| R456-2 S1: the CRF span leaves out the recentre's re-snap end | Taken, as a sentence (the span unchanged) | `sim_tdm8_render.cpp:3422-3424`; `MEDIA_CLOCK_FOLLOWING.md:1400-1403` |
| R456-2 S2 = R457-2 S2: check each standing window's walk against `kLawWalkCycles` | **Open**: a check, not a print or a sentence. Both outputs now print the walk beside the stated one | |
| R456-2 S3: what a CRF gradability failure means | Taken | `MEDIA_CLOCK_FOLLOWING.md:1404-1414` |
| R456-2 S4: the stray quote in the verdict line | Taken | `tdm8_render_mutants.py:687-696`: `breaks "<name>" and 35 more` |
| R457-2 S1: `make -C ... tdm8render-mutants` advertised | Taken for the docs (`TESTING.md:270`, `:523`, the runner's usage `:79-82`); the Makefile defect itself is **open** for a new Issue | |
| R457-2 S3: the CRF window's exact PDU count (292) | **Open**: a check change | |
| R457-2 S4: `law-boundary-scan.md` not in the public packet | For the manager: it is in this directory, with `round3-boundary-walks.md` | |
| R456-1 S3: name the ceiling check for what it bounds | Taken: "...inside the declared 32768-tick ceiling, counted from this wait's start" (`sim_tdm8_render.cpp:3488-3490`); the `[LAW]` row and `TESTING.md:521`. Nothing parses that name | |
| R456-1 S2: the stage's counters unchanged across a window | **Open**: a check | |
| R456-1 S1 = R457-1 S3: the accept-pulse instrument in `milan_dp` | **Open**: out of scope, a candidate new Issue | |

### R3.5 Gate table

Pinned Verilator 5.050; GNU make 4.3 (the release tarball, sha256
`e05fdde4...8e19`, built in scratch) first on `PATH` for every suite,
campaign and diagnostic, and `TMPDIR` on disk (this host's `/tmp` is tmpfs).
The code was run at `ca3db9f3`; the head `36207e91` adds docs only (`git diff
--stat ca3db9f3 HEAD`: the three docs files). Dev-pin rows ran in the lane,
except the diagnostic, which ran in an archive copy equal to the head's tree
(every index entry identical). The `c4cb84ff` rows ran in archive copies with
the `protocol-processor` gitlink and checkout at `c4cb84ff` (fetched from the
processor fork) and both adoption patches `git apply`'d after a clean
`--check`: 9 index entries differ from the head (the gitlink and the 8
patched files), never committed. A shared host: load average 37 to 119 from
other lanes and this round's own concurrent runs, so wall times are
indicative only.

| # | Command | Where | rc | Result |
|---:|---|---|---:|---|
| 1 | `make -C tb/verilator/milan_dp_render`, cold (`make clean` first) | lane, dev's pin | 0 | 245/0, 65/0, leg defects 5/5; 774.0 s (`dev-suite.log`, 181,364 B, sha256 `42c70c2fda409829c088f94f95f207219c26d2110944218a2126160c6aa066c5`) |
| 2 | the same | `c4cb84ff` copy | 0 | the same counts; 797.1 s (`c4-suite.log`, 182,094 B, `d4ef3348eb8c2b9f5f811b4db48141010349e27679c8dfa3dfbe25af832cf2e8`) |
| 3 | `cd tb/verilator/milan_dp_render && make tdm8render-mutants` | lane, after row 1 | **2** | 32 checks: 28 PASS, 4 FAIL, the four pre-existing (round 1 section 7.7); A2-a and both setpoint arms caught; 3,334 s (`dev-campaign.log`, 20,499 B, `f9cb2dabcd7373ff320bd055df7d930b40387045fdac0cacbc2de68d66b16efb`) |
| 4 | the same | `c4cb84ff` copy, after row 2 | **2** | verdict lines identical to row 3; 3,462 s (`c4-campaign.log`, 20,514 B, `23d973050a6cf84238e64447bac68b27459fabcb257f86d766d735fefc99787b`) |
| 5 | `cd tb/verilator/milan_dp_render && make tdm8render-law-boundary LAW_BOUNDARY_JOBS=6` | head copy, dev's pin | 0 | 81/81; largest walk 3 of 564 windows, stated 5; 2,674 s (`dev-bnd.log`, 145,190 B, `e7f75cbe4b255647469e8cffba0a4611bbbae2f715c48334abcf0ea8859b1594`) |
| 6 | the same | `c4cb84ff` copy | 0 | the same verdict lines; 2,770 s (`c4-bnd.log`, 145,544 B, `b26a4dc3253ad45ddbfb03a19f14231edac1d474ccc8c6e6a697e1b90267a3e2`) |
| 7 | `./obj_tdm8r/Vmilan_dp_tdm8r --law-only`, from rows 1 and 2's binaries | both | 0, 0 | 106/0 each; +0 margin 47, +1953 margin 63; waited 4,014 / 4,013 ticks |
| 8 | `--crf-only`, the same binaries | both | 0, 0 | 53/0 each; the CRF window at -1021..-1018 (margin 1009) and -94..-91 (margin 82) |
| 9 | docs: `docs_check`, `check_em_dash --base 241f9184` (pinned Markdown venv), `check_doc_style` (+selftest), `check_gptp_docs` (+selftest, `--with-submodule`), `DOC_MAP.gen` / `timesync_chain.gen` / `submodule_boundaries.gen` `--check` (+selftest), `check_solution_docs` (+selftest), `check_feature_status` (+`--self-test`), `gen_module_matrix.py --check`, `check_doc_paths`, `check_archive` (+selftest), `check_submodule_docs`, `check_diagram_pngs`, `gen_toc --selftest / --verify-anchors / --check` | lane at the head | 0 each (26) | em-dash: 0 findings over 94 added lines; doc paths: 902 cited paths resolve |
| 10 | code: `check_cpp_idiom` (+selftest), `check_py_idiom` (+selftest), `check_hygiene --check`, `check_todo_ownership`, `check_sh_idiom`, `check_sv_idiom`, `check_port_contracts`, `check_rtl_source_lists`, `check_soc_sources`, `check_baremetal_only --check`, `check_nvm_record_space`, `check_wire_accountability --self-test`, `measure_test_evidence --check`, `measure_fail_fast --check`, `measure_naming --check`, `measure_cohesion` / `measure_control_flow --selftest`, `ci_events --check` / `--selftest`, `ci_scope --selftest` | lane at the head | 0 each (22) | no ratchet moved |
| 11 | rtl-fast's local half: `lint_rtl.py --check --self-test` (pinned Verilator), `pp_srcs.py --check`, `--selftest`, `behave` in `tests/` | lane at the head | 0 each | lint 90 <= 90; behave 14 features, 404 scenarios |
| 12 | `ci_scope.py` on the paths changed since dev `241f9184` | lane | 0 | `true` (RTL/tooling scope: `tb/` changed) |

Not run: the Yosys elaboration and the `syn/ooc` steps that need the pinned
sv2v v0.0.12 (this host has v0.0.13; no `hdl/` file changed); `act` and the
hosted contexts (nothing is pushed from this lane). PR #638's gates (round 2,
R2.5) are untouched by this round.

### R3.6 Both reviewers' round-2 probes, unchanged

Both packets' scripts were copied from `643-review-evidence` at `91603c66`
and run unchanged (each file byte-identical to the published one, recorded
in `pkt45x-scripts.sha256`). Their `MANIFEST.sha256` files do not verify
against the published blobs for 25 (R456-2) and 7 (R457-2) entries, every one
a file that carries a placeholder such as `$VALIDATION_TOOLS` or a redacted
path: the manifests were taken before redaction. Their trees were built as in
round 2: archive copies of the head's code commit, every path indexed, no
commit; `protocol-processor` a local clone with `c4cb84ff` fetched from the
processor fork; for `c4cb84ff`, both adoption patches `git apply`'d (R457's
own `trees` step does that itself from the evidence tree's copies, which are
byte-identical to this directory's). Environment only: `VALIDATION_TOOLS`
pointed at the tool directory, `vl_jobs.sh` made executable, GNU make 4.3
and the pinned Verilator first on `PATH`, `TMPDIR` on disk.

**R456-2** (`r2_builds.sh` lanes L1-L7, `r2_runs.sh` batches B1-B4, the
`crfhist` and `crfw1104` runs through its unchanged `run_probe.py run`, then
`r2_summarize.py`, rc 0):

| Probe | Result at the head (W = 9) | Round 2 (W = 8), for comparison |
|---|---|---|
| builds | 18 of 21 built; `tieoff`, `tietr18`, `tietr36` refuse (their edits name the tie code round 2 removed), as in round 2 | the same |
| **`hp-crfhist-full`** | rc 0, 245/0. CRF window: `-592:3 -591:32 -590:54 -589:71 -588:106 -587:26`, printed `-592..-587 (walk 5)`, clearance 587, margin 578. **Agrees with the stated S = 5** | `(walk 4)` beside a 5-cycle range (F1) |
| **`c4-crfhist-full`** | rc 0, 245/0. `336:21 337:47 338:64 339:98 340:62`, `(walk 4)`, margin 326 | the same range |
| `hp-crfw1104-crf` (W = 1105) | rc 1, 50/1: "T30 CRF LAW: gradable" fails by name, the law not graded | the same |
| `hp-clean-law`, `c4-clean-law`, `hp-boottrace-law` | rc 0, 106/0 | the same |
| `hp-a2a-law`, `c4-a2a-law` | 106/19: the ceiling and all 18 settled checks | the same |
| `hp-spm1-law`, `hp-spp1-law`, `c4-spm1-law`, `c4-spp1-law` | 106/36: fill and band at all 18 phases | the same |
| `hp-spm1-crf`, `hp-spp1-crf` | 53/2: the CRF fill and band checks | the same |
| `hp-tieon-law`, `c4-tieon-law` (+2,018..+2,035 standing) | 52/18: all 18 not gradable, each failing "gradable" by name | 55/17: +2,035 graded and passing at clearance 9 |
| `hp-tiespm1-law`, `hp-tiespp1-law` | 52/18: the same 18 not gradable; nothing graded | 55/19: +2,035 graded and failing both |
| `hp-tie36-law` (+2,010..+2,045) | 133/21: +2,016..+2,036 not gradable; 15 graded pass | 139/19 |
| `hp-bootnodwell-law` | 106/14: 14 phases fail their settled hold | the same |
| `p631-base-full`, `c4-base-full` (dev's base harness) | 155/0; 155/2 (#643's failure reproduced at `c4cb84ff`) | the same |
| `--law-boundary` lists, sound design (`hp-/c4-clean-lb-*`, 16 runs) | all rc 0, no graded failure; not gradable +2,016..+2,036 (`hp` 2010up, `c4` down), +2,015..+2,036 (`c4` up), +2,018..+2,035 (2018up); alone: +2,016/+2,020/+2,025/+2,030/+2,036 not gradable, +1,990/+2,010/+2,042/+2,062 graded pass | not gradable bands one cycle narrower |
| `hp-/c4-spm1-lb-2018up` | rc 0: all 18 not gradable, nothing failed | 1 graded |
| W ablations: `hp-w4-*` (guard 0, W = 5), `hp-w0-*` (guard -4, W = 1) | sound design: every graded window passes (69/67 graded at W = 5, 77/76 at W = 1); `spm1w0`, `spp1w0`: 77 graded, every one failing both law checks | the same shape: W is not exercised by a failure at this model (R456-2 S2, left open) |
| `r2_summarize.py` | largest walk per log, sound design: 2 in `[LAW]` standing, 3 at the boundary, **5** for CRF at dev's pin (`hp-crfhist-full`), 4 at `c4cb84ff`; A2-a 18 and no-dwell 11 (moving grid, settled checks failing) | |

**R457-2** (`reproduce.sh` steps `trees`, `probes`, `launch2`, `launch1`,
`launch3`, `analyse`, unchanged; `histories.sh` unchanged):

| Step | Result at the head |
|---|---|
| `trees`, `probes` | rc 0; `probe-instrument.patch` and both setpoint patches apply to the head (round 2's did not) and build |
| `launch1`: the suite, `make -C`, at both | rc 0 at both: 245/0, 65/0, 5/5 (715 s, 735 s) |
| `launch1`: `make tdm8render-law-boundary LAW_BOUNDARY_JOBS=4`, at both | rc 0 at both: 81/81, verdict lines identical to R3.5 rows 5 and 6, "the largest walk over 564 windows is 3 cycles ...; the leg states a walk of 5" (3,668 s, 3,798 s) |
| `launch1`: `law_arm.py` sp-low, sp-high, at both | rc 0 each: `caught`, 0 of 36 named checks not failing |
| `launch2`: `stdhist` | rc 0, 108/0, 18 graded; the probe's identity checks: 0 instant and 0 take-cycle mismatches, and the fill read differs from `fill_end_w` only at each phase's snap PDU (id 2), which is not graded, as in round 2 |
| `launch2`: `tiehist`, `tiealone` | 34/8 and 20/1: every phase not gradable, failing "gradable" by name |
| `launch2`: `nodwell` | 108/14: 14 settled-hold failures |
| `launch2`: `sp-std`, `sphi-std` | 112/38: fill and band at all 18 standing phases; +2,025 and +2,026 not gradable |
| `launch2`: interleaved `il-*` (+2,005..+2,045 from both edges inward) | sound 117/0: 20 graded pass, +2,016..+2,036 not gradable; -1 and +1: 117/40, all 20 graded failing both law checks. `judge_il.py` rc 1 on all three, reporting only "+2,016 and +2,036 NOT GRADABLE at clearance 9": it hard-codes "clearance 8 or less" (W = 8); at W = 9 that is the window, not a defect. Least band-edge margin over graded sound windows 10.00 |
| `launch3`: `lawonly-head`, `lawonly-c4` | rc 0, 106/0, +0 margin 47; the `[LAW]` lines byte-identical to R3.5 row 7's |
| `launch3`: `probe-window-wider-than-a-tick.patch` | **does not apply** (`sim_tdm8_render.cpp:193`): its context is the walk statement this round restates (`kLawWalkCycles = 4`), so `set -e` stops there |
| its equivalent: the patch's one edit (`kLawGuardCycles = 4` -> `2100`) by hand in a fresh copy, then `probe-wfault-full` | rc 1, 188/19: exactly the 18 `[LAW]` and the CRF window's "gradable" checks, every law check skipped (245 -> 188), as in round 2 |
| `histories.sh` (step 8), `JOBS=8` | 54 legs, rc 0 each; `hist_summary.py`: identical at both processors, not gradable +2,015..+2,035 ascending, +2,016..+2,036 descending, +2,015..+2,037 alone; 0 FAIL lines; largest offset range 3 |
| `analyse`: `judge_test.py` | ALL OK (the judge and the argument parsing unchanged) |
| `analyse`: `walks.py` | 587 `[LAW]` windows: largest reported walk 3, largest nearest-pop range 3, **0 windows whose nearest-pop range exceeds the reported walk** (49 in round 2); 2 CRF windows: reported 5, nearest-pop 5, 0 exceed |

### R3.7 Interpretations, limits and open items

1. **One measure, both figures.** The `[LAW]` figure (3) and the CRF figure
   (5) are now both the nearest pop's range, the page's definition, and the
   harness prints exactly that. Round 2's `[LAW]` figure already was (it came
   from the histograms); only the CRF figure changes, 4 -> 5.
2. **W = 9, a stated choice.** The assignment set W = S + 4. The guard stays
   4 and the walk becomes 5, so the window grows by one cycle: the phases at
   clearance 9 (three in each scan, two alone) are now not gradable (R3.1),
   and every standing window loses one cycle of margin (+0: 47/48;
   CRF: 578/326). A graded window now tolerates a walk of up to 10 cycles
   before a crossing could reach a graded end.
3. **S is a settled-window figure.** The only walks above 5 in any log are
   the A2-a mutant (18) and the no-dwell probe (11), where the grid moves;
   every one of those windows fails its settled-hold check by name.
4. **The half-tick exception is untested by data.** No window in any log
   sits half a tick from the grid, so `walk_wraps()` never fired; it exists
   so that a model change cannot print a 2,083-cycle walk there, and the line
   says which range it reports if it does.
5. **No check compares the measured walk with the stated one** (R456-2 S2 =
   R457-2 S2, open). Both outputs print it beside the stated figure, and
   R456's ablations show W = 1 and W = 5 still pass the sound design and fail
   both setpoint defects at this model, so a walk that outgrew S would today
   be seen only by reading.
6. **The CRF window under `--crf-only` at `c4cb84ff`** sits at -94..-91,
   clearance 91, margin 82: the nearest any standing-style window came to W
   this round, and the reason the design page now says what a CRF
   gradability failure means.
7. **Reviewers' scripts and W = 9.** R457-2's `judge_il.py` hard-codes
   W = 8; its only complaints are the two clearance-9 phases (R3.6). R457-2's
   `probe-window-wider-than-a-tick.patch` cannot apply to any head that
   restates the walk; its one edit was run instead.
8. **The `make -C` defect** is still unfiled; the docs now give both campaign
   targets from inside the suite directory, and the runner's usage too. The
   Makefile is unchanged (a separate Issue's).
9. **Pre-existing campaign failures unchanged**: the `--epoch-only` positive
   control and its two clean controls, and the surviving "uncounted repeat"
   mutant (round 1 section 7.7).
10. **Wall times** ran beside every other job of this round (load average 37
    to 119), so they are not a cold uncontended figure; TESTING.md's 663.8 s
    stands (this round adds print lines and one comparison only).
11. **The processor fork's `main`** is not re-read this round; the scratch
    parent uses `c4cb84ff` as assigned.

### R3.8 Files in this directory (round 3)

| File | Bytes | sha256 | What |
|---|---:|---|---|
| `HANDOFF.md` | | | this file |
| `PR-BODY.md` | 18,380 | `04b8712fb10cc5f9e45d4ab7f6150d866478ec508acf2f3aadb0c9ef8503b195` | the PR body, round 3 ("Closes #643", "Relates to #629", "Relates to #647") |
| `round3-boundary-walks.md` | 13,593 | `0da1c5e6a5ab5781cdc65698d0f094e825f3720a38e48b42acf07b9dca439fac` | every window of both diagnostics at W = 9: nearest-pop range, walk, clearance and outcome per phase and history |
| `law-boundary-scan.md`, `phase-law-tables.md`, the rest | | | rounds 1 and 2, unchanged |

Scratch (never committed, not in this directory): `$VALIDATION_STORAGE/643-a522/r3/`
holds the trees, both packets with their receipts, every log named above and
`bin/` (the wrappers and `rederive.py`).

---

## Round 2: REVIEW READY at `6b96391d13c5d777a98b1c7be9265c63d651c911`

Answers R456-1 (F1 MAJOR, F2 MINOR) and R457-1 (F1 MINOR, F2 MINOR) under the
[round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5974715857):
the tie rule is withdrawn and a measured ambiguity window replaces it. Branch
`643-t30-phase`, not pushed (not allowed in this lane). Every item of the
ruling is met; the suite, the boundary diagnostic and the docs gates are rc 0
at both processors; the full mutant campaign is rc 2 at both on the same four
pre-existing arms as round 1, and every arm this round adds or touches passes.

- R456-1: https://github.com/kebag-logic/milan-fpga/pull/648#issuecomment-5974712082
- R457-1: https://github.com/kebag-logic/milan-fpga/pull/648#issuecomment-5974627143
- Their packets: branch `643-review-evidence` at `301507482f8c` (`review-evidence/643-r1/`; the author inputs at `531abe2b`).
- REVIEW READY (round 2): https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5975549174

History on top of round 1's `98729742`, no rebase, no amend:

| Commit | What |
|---|---|
| `7aa7b449acc61154a4b4c903d9fe6db896086325` | `--no-ff` merge of dev `241f91845230ae410506dffb16b71937127fd175` (PR #638), no conflict |
| `e63c4279ef9a4d21e66d89ebe94b9fca032ad31f` | the window, the gradable checks, the setpoint +/-1 mutants, `--law-boundary`, the docs |
| `6b96391d13c5d777a98b1c7be9265c63d651c911` | TIME_SYNC.md's restated sentence held to that page's style limits (docs only: the code is `e63c4279`'s) |

### R2.1 Item 1: the spread, measured

**Method.** The round-2 harness's `--law-boundary` leg, at dev's processor pin
`631eeb34` (the lane) and at processor `c4cb84ff` (the scratch parent, both
adoption patches, never committed), GNU make 4.3, the pinned Verilator 5.050.
The leg located the boundary itself from the +0 phase's own offsets: the first
pop after each PDU end is taken +2,025..+2,028 cycles after it, so an end meets
a pop near +2,026. Every phase from +1,986 to +2,066 (+/-40, one cycle apart)
was graded in three histories per processor:

- **ascending**: the leg's own scan, after its locating +0 phase;
- **descending**: `--law-boundary=2066..1986`;
- **alone**: one run per phase, `--law-boundary=<p>`: the boot dwell, the
  settled wait, then that phase only.

That is 486 graded windows plus 2 locating ones. Each window records, per PDU
end, the offset of the stream-0 pop nearest the boundary its fill reads across
(the cycle the pop was taken in minus the end beat's; 0 or less is in the fill).
Every row, with its offset histogram, is in `law-boundary-scan.md`.

| Processor | History | Phases | Not gradable | Graded pass | Graded fail | Max walk | Walk: phases |
|---|---|---:|---|---:|---:|---:|---|
| dev's pin `631eeb34` (the lane) | ascending | 81 | +2017..+2034 (18) | 63 | 0 | 2 | 0: 1, 1: 63, 2: 17 |
| dev's pin `631eeb34` (the lane) | descending | 81 | +2017..+2034 (18) | 63 | 0 | 3 | 0: 2, 1: 60, 2: 17, 3: 2 |
| dev's pin `631eeb34` (the lane) | alone | 81 | +2016..+2036 (21) | 60 | 0 | 3 | 3: 81 |
| processor `c4cb84ff` (scratch parent, both patches) | ascending | 81 | +2017..+2034 (18) | 63 | 0 | 2 | 0: 1, 1: 63, 2: 17 |
| processor `c4cb84ff` (scratch parent, both patches) | descending | 81 | +2017..+2034 (18) | 63 | 0 | 3 | 0: 2, 1: 60, 2: 17, 3: 2 |
| processor `c4cb84ff` (scratch parent, both patches) | alone | 81 | +2016..+2036 (21) | 60 | 0 | 3 | 3: 81 |

**Results.**

1. **No graded window failed the sound design**: 0 of 372, at either
   processor, in any history.
2. **The walk.** Within one window the offset walks by at most 2 cycles in the
   ascending scan, 3 in the descending scan and 3 in every alone run (where a
   few ends at the start of the window sit one cycle lower; the alone history
   is identical at every phase). These walks are recomputed from the logged
   histograms and can only overstate: see the note in `law-boundary-scan.md`. The full leg's `[LAW]` phases walk at most 2
   (R2.3). T30's CRF window, 292 PDUs under CRF, walks 4 at both processors.
3. **History moves the boundary, not just the walk.** The same phase reads
   differently by history: +2,016 is gradable in both scans (clearance 9,
   margin 1) and not gradable alone (clearance 8); the band left not gradable
   is +2,017..+2,034 in both scans and +2,016..+2,036 alone.
4. **Both processors give identical offsets at every phase in every history.**
   The processor does not enter the RX-end-to-pop path.

**The window.** S = 4 cycles, the largest walk any graded window showed (the
CRF window; 3 in every `[LAW]` history). Guard G = 4 = S. **W = 8 cycles**
(`sim_tdm8_render.cpp:195-197`). A phase is graded only when every PDU end's
nearest pop is at least 9 cycles from the boundary. A crossing of the boundary
between the snap and a graded end needs a walk of at least that end's clearance
plus 1, so a graded phase tolerates a walk of up to 9 cycles: more than twice
the largest measured.

**The tie-scan evidence, corrected.** Round 1's section 6 and
`phase-law-tables.md` section 8 said "ties only at +2,025 and +2,026" and that
one cycle of feed jitter moves a pop across the boundary. That was one run
history and is withdrawn. The end-to-pop offset walks by up to 3 cycles within
a `[LAW]` phase and shifts with the run's history. Both reviewers' failures,
+2,025 reading 15 with the pop taken 2 cycles after the end, and the setpoint
-1 defect passing at +2,025 and +2,026, lie inside today's not-gradable band,
so neither phase is graded any more (R2.6 shows it on their own probes).

### R2.2 Item 2: grading by the window

`tb/verilator/milan_dp_render/sim_tdm8_render.cpp` at `e63c4279` (unchanged
since):

| Line | What |
|---:|---|
| 183 | `kBandSlackCycles` 64 -> 1: only the pop pulse's register. The 64 cycles existed for ties; in a graded window the first event lands more than W cycles inside both band edges |
| 186-197 | The ambiguity window, stated as a measurement: `kLawWalkCycles` 4, `kLawGuardCycles` 4, `kLawAmbiguityCycles` 8 |
| 223 | `kLawUngradedTailPdus` 4 (was a literal) |
| 226 | `kLawBoundaryHalfBand` 40 |
| 305 | `parse_the_phase_list()`: `--law-boundary=PHASES`, numbers or `LO..HI` runs, refused on anything else |
| 677 | The tie evidence (`tie_pop`, `last_end_id`) is gone; `pop_take` records the cycle every stream-0 pop was taken in (its pulse, seen a cycle later, minus 1) |
| 703 | `observe_pdu_end()` records the take cycle instead of a tie |
| 734 | `pop_nearest_the_end()`: the pop nearest the boundary a PDU end's fill reads across: its offset, its clearance (whole cycles from the boundary; 0 for a pop taken with the end beat or one cycle after) and whether the end is steady (a pop within two ticks each side, so not the snap, whose earlier pops prefill held) |
| 1435, 3175 | `EndOffsets` / `offsets_at_pdu_ends()`: the least clearance over every end (snap included) and the walk over the steady ends |
| 3200 | `print_the_offset_histogram()` (`--law-boundary` only) |
| 3228 | `the_window_is_gradable()`: prints offsets, walk, clearance and margin; prints `[NOT GRADABLE] <tag>: PDU <id>'s end has a pop taken <offset> cycles from it` when the clearance is 8 or less; for a STANDING window it is the check `<tag>: gradable, every PDU end clear of a pop by more than the ambiguity window` |
| 3268 | `prove_the_setpoint_law_still_holds(span_first, first, last, tag, expect_n)`: not gradable -> no law check at all (neither pass nor fail); gradable -> fill exactly 14 (no allowance), band (8T, 9T + 1], and the PDU count exact where stated (124 for `[LAW]`, R457-1 S1) |
| 3413 | T30 CRF LAW: a standing window too, judged over its own 292 PDUs |
| 3443, 3456 | `phase_internal_law()` and the shared `wait_for_the_settled_report()` |
| 3486, 3507 | `phase_law_boundary()` and `locate_the_law_boundary()` |
| 3529 | `grade_the_law_at_a_feed_phase()`: gradability over every PDU end of the fresh stream (the snap included); `[BOUNDARY] +<p>: graded PASS / graded FAIL / NOT GRADABLE, <n> check(s) failed` in `--law-boundary` |
| 4010, 4062 | `--law-boundary[=PHASES]` parsed and dispatched after the same boot dwell as `--law-only` |

Every standing window is gradable at both processors with a margin of at least
48 cycles (R2.3). Check count: shipping leg 226 -> 245 (one gradable check per
`[LAW]` phase and one for the CRF window); `--law-only` 88 -> 106.

`tb/verilator/milan_dp_render/tdm8_render_mutants.py`: `LAW_FILL`, `LAW_BAND`
(`:133`, `:135`); `SETPOINT_LINE`, `SETPOINT_DEFECTS` (`:139`, `:141`); the two
setpoint mutants in `MUTATIONS`, `--law-only`, each required to fail all 36
named checks (`:340`); the `--law-boundary` diagnostic (`:465` constants,
`boundary_problems` `:691`, `law_boundary_designs` `:735`,
`judge_boundary_rounds` `:752`, `run_law_boundary` `:776`); `parse_args`
(`:558`) takes `--law-boundary [--jobs N]` and refuses `--jobs` elsewhere.
`Makefile:202`: the explicit `tdm8render-law-boundary` target
(`LAW_BOUNDARY_JOBS`, default 8).

### R2.3 Item 3: the standing proof

**Every standing window is gradable, with its margin asserted.** The suite
gate at both processors (full leg, `e63c4279`; the code is unchanged at the
head): the pop nearest each PDU end, the walk over the steady ends, the least
clearance from the boundary over every end (the snap included), the margin
from W = 8, and the graded law.

| Window | Nearest pop (dev) | Walk | Clearance | Margin | PDUs, fill, delay (T) | Nearest pop (`c4cb84ff`) | Walk | Clearance | Margin | PDUs, fill, delay (T) |
|---|---|---:|---:|---:|---|---|---:|---:|---:|---|
| T30 CRF (292 PDUs) | -592..-587 | 4 | 587 | 579 | 292, 14, 8.717..8.719 | +336..+340 | 4 | 335 | 327 | 292, 14, 8.162..8.164 |
| `[LAW]` +0 | -59..-57 | 2 | 57 | 49 | 124, 14, 8.972..8.973 | -59..-57 | 2 | 57 | 49 | 124, 14, 8.973..8.973 |
| `[LAW]` +130 | -189..-187 | 2 | 187 | 179 | 124, 14, 8.910..8.911 | -189..-187 | 2 | 187 | 179 | 124, 14, 8.910..8.911 |
| `[LAW]` +260 | -319..-317 | 1 | 317 | 309 | 124, 14, 8.847..8.848 | -319..-317 | 2 | 317 | 309 | 124, 14, 8.847..8.848 |
| `[LAW]` +391 | -450..-448 | 2 | 448 | 440 | 124, 14, 8.784..8.785 | -450..-448 | 2 | 448 | 440 | 124, 14, 8.785..8.785 |
| `[LAW]` +521 | -580..-578 | 2 | 578 | 570 | 124, 14, 8.722..8.723 | -580..-578 | 2 | 578 | 570 | 124, 14, 8.722..8.723 |
| `[LAW]` +651 | -710..-708 | 2 | 708 | 700 | 124, 14, 8.660..8.661 | -710..-708 | 2 | 708 | 700 | 124, 14, 8.660..8.661 |
| `[LAW]` +781 | -839..-838 | 1 | 838 | 830 | 124, 14, 8.598..8.598 | -840..-838 | 2 | 838 | 830 | 124, 14, 8.597..8.598 |
| `[LAW]` +911 | -970..-968 | 2 | 968 | 960 | 124, 14, 8.535..8.536 | -970..-968 | 2 | 968 | 960 | 124, 14, 8.535..8.536 |
| `[LAW]` +927 | -986..-984 | 2 | 984 | 976 | 124, 14, 8.528..8.528 | -986..-984 | 2 | 984 | 976 | 124, 14, 8.527..8.528 |
| `[LAW]` +1042 | +983..+985 | 2 | 982 | 974 | 124, 14, 8.472..8.473 | +982..+984 | 2 | 981 | 973 | 124, 14, 8.472..8.473 |
| `[LAW]` +1156 | +869..+871 | 2 | 868 | 860 | 124, 14, 8.418..8.418 | +868..+870 | 2 | 867 | 859 | 124, 14, 8.417..8.418 |
| `[LAW]` +1172 | +852..+854 | 2 | 851 | 843 | 124, 14, 8.410..8.411 | +853..+854 | 1 | 852 | 844 | 124, 14, 8.410..8.411 |
| `[LAW]` +1302 | +722..+724 | 2 | 721 | 713 | 124, 14, 8.347..8.348 | +723..+724 | 1 | 722 | 714 | 124, 14, 8.348..8.348 |
| `[LAW]` +1432 | +593..+594 | 1 | 592 | 584 | 124, 14, 8.285..8.286 | +593..+595 | 2 | 592 | 584 | 124, 14, 8.285..8.286 |
| `[LAW]` +1562 | +463..+465 | 2 | 462 | 454 | 124, 14, 8.223..8.223 | +462..+464 | 2 | 461 | 453 | 124, 14, 8.222..8.223 |
| `[LAW]` +1693 | +331..+333 | 2 | 330 | 322 | 124, 14, 8.160..8.160 | +332..+333 | 1 | 331 | 323 | 124, 14, 8.160..8.160 |
| `[LAW]` +1823 | +202..+203 | 1 | 201 | 193 | 124, 14, 8.098..8.098 | +202..+204 | 2 | 201 | 193 | 124, 14, 8.098..8.098 |
| `[LAW]` +1953 | +72..+74 | 2 | 71 | 63 | 124, 14, 8.035..8.036 | +72..+73 | 1 | 71 | 63 | 124, 14, 8.035..8.036 |

`--law-only` from the same binaries (rc 0, 106 checks, 0 failing, at both): +0
clears the boundary by 56 cycles (margin 48), +1953 by 72 (margin 64); the
wait after the dwell was 4,014 / 4,013 ticks.

**The setpoint +/-1 mutants in `--law-only`** (`tdm8_render_mutants.py:340`),
each required to fail the fill check and the band check at all 18 phases (36
named checks): **caught at both processors**, "breaks \"T30 INTERNAL LAW +0:
the fill at every PDU end is the setpoint plus that PDU, 14 events\" and 35
more" (`campaign-*.log`). R456's own `spp1`/`spm1` probes and R457's
setpoint-7 patch give the same 36 (R2.6).

**The full campaign** (`cd tb/verilator/milan_dp_render && make
tdm8render-mutants VERILATOR=<pinned>`), at both processors: **rc 2, 32
checks, 28 PASS, 4 FAIL**, the verdict lines identical in the two trees
(3,190 s and 3,274 s). Every arm this round adds or touches passes: the
`--law-only` positive control; A2-a removed (18 of 18 settled checks); both
setpoint arms; the `--crf-only` control and the clock-source-trigger mutant.
The four failures are round 1's pre-existing four, unchanged: the
`--epoch-only` positive control and its two clean controls (the four "T30 CRF
... recentre" checks, red since #629's A2-a), and the surviving "uncounted
repeat" mutant (round 1 section 7.7, reproduced there with dev's own
harness).

**The boundary diagnostic** (`cd tb/verilator/milan_dp_render && make
tdm8render-law-boundary VERILATOR=<pinned> LAW_BOUNDARY_JOBS=6`, in scratch
copies of the head at each processor): **rc 0, 81 checks, 81 PASS, at both**
(2,600 s at dev's pin, 2,686 s at `c4cb84ff`, on a shared host).

| Design | Leg's own ascending scan (+1,986..+2,066, after +0) | Descending scan | Each of +2,014..+2,038 alone |
|---|---|---|---|
| unmutated | 64 graded, all pass; not gradable +2,017..+2,034 | 63 graded, all pass; not gradable +2,017..+2,034 | +2,014, +2,015, +2,037, +2,038 graded and pass; +2,016..+2,036 not gradable |
| setpoint one event low | 64 graded, all fail fill and band; not gradable +2,017..+2,034 | the same | +2,014, +2,015, +2,037, +2,038 graded and fail both; +2,016..+2,036 not gradable |
| setpoint one event high | the same | the same | the same |

Identical at both processors. Every not-gradable phase failed nothing; each
scan held both kinds; no phase was ever graded FAIL on the sound design or
graded PASS on a defect. At the gradable edge the margin is 1 cycle (+2,035
in the scans, clearance 9) and both law checks still separate the three
designs there: delay 8.996 T (sound), 7.996 T (low), 9.996 T (high)
(R456's own `tiespm1`/`tiespp1` probes, R2.6).

### R2.4 Item 4: docs

| File:line | Change |
|---|---|
| `docs/design/TIME_SYNC.md:451-455` (R456-1 F2 = R457-1 F2) | "The fill at accept stays the setpoint" restated: each PDU end's fill is the setpoint plus that PDU, every first event in the law band, both graded at the PDU end, the window in the test plan. Held to that page's 10-word sentence and 20-word paragraph limits (`6b96391d`) |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:1329` | The `[LAW]` row: gradable with its margin a check, fill exactly 14, the pulse's one-cycle register instead of 64 cycles, and the setpoint +/-1 negatives |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:1330` | A row for `tdm8render-law-boundary` |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md:1367-1398` | "The tie rule" replaced by "The ambiguity window": the coincidence, the measured walk (3 in every `[LAW]` history, 4 in the CRF window), W = 4 + 4 = 8, not gradable means neither pass nor fail, every standing window gradable with +0's margin of 48 and 49, and what a graded window grades |
| `tb/verilator/README.md:63` | The suite's row: the window and the not-gradable rule instead of "one cycle" |
| `docs/testing/TESTING.md:521` | The `[LAW]` row: exactly 14, the one-cycle register, gradable with the 8-cycle window |
| `docs/testing/TESTING.md:523` | The campaign: twenty-one mutants, 32 checks; the setpoint +/-1 arms; the `--law-boundary` round (81 checks) and why it is run from the suite directory |

The PR body's "No standing phase is a tie" paragraph is restated against the
asserted margin (`PR-BODY.md`, Known limitations).

### R2.5 Item 5: the merge of dev and its touched gates

`7aa7b449` merges dev `241f9184` (PR #638) with `--no-ff`; `git merge-tree`
showed no conflict and no file of this lane is touched by it. PR #638 changed
three CI definitions: `.github/workflows/rtl-fast.yml` (three resource-gate
commands in the `yosys-elaboration` job), `scripts/ci_events.py` (the same
three in its step lists) and `scripts/ci_scope.py` (`AREA_BUDGET.md` is a
gate-read doc). Run at the head, all rc 0:

| Command | Result |
|---|---|
| `python3 syn/ooc/pp_resource_gate.py --selftest` | 260 arms and 500 generated cases PASS |
| `python3 syn/ooc/pp_resource_gate_mutants.py` | control passes, all 174 mutants fail |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | baseline PASS: 3 endpoints |
| `python3 scripts/ci_events.py --check` / `--selftest` | OK, 1655 contract items across 4 workflow files and CI_WORKFLOWS.md / PASS, 2215 arms |
| `python3 scripts/ci_scope.py --selftest` | PASS |
| `python3 syn/ooc/pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py` (the same step) | PASS |

Not run from that step: `syn/ooc/dp_srcs.py --selftest` and the two `--top`
reads, `ooc_tcl_selftest.py`, and the Yosys elaboration, which need the pinned
sv2v v0.0.12 and Yosys; this host's sv2v is v0.0.13, and no `hdl/` file
changed in this lane.

### R2.6 The reviewers' reproduction steps

Both packets' scripts were run **unchanged** (byte-identical to their
`MANIFEST.sha256`, verified) against scratch copies of the head built the same
way as the scratch parent: a `git archive` of the head and its submodules with
every path in a git index and no commit; `protocol-processor` a local clone at
its pin with `c4cb84ff` fetched from the processor fork, checked out and the
two adoption patches `git apply`'d for the `c4cb84ff` trees. GNU make 4.3 and
the pinned Verilator 5.050 first on `PATH`. Two environment steps only:
R457's `reproduce.sh` needs `$PKT/scratch` to exist (its `rsync` does not make
parents), and R456's `vl_jobs.sh` wrapper was made executable.

**R457-1 `scripts/reproduce.sh`** (rc 1 overall, from step 5):

| Step | Result at the head |
|---|---|
| 1. the two trees (head, and `c4cb84ff` with both patches) | built |
| 2. the default target, cold, at both processors | rc 0 at both: 245/0, 65/0, leg defects 5/5 |
| 3. the campaign's own A2-a arm and its `--law-only` control, through `plant/build/run_leg/verdict`, at both | clean: `pass` at both (106/0); A2-a: `caught` at both (19 failing: the ceiling and all 18 settled checks) |
| 4. the tuple verdict and the phase table, offline | all seven OK |
| 5. `git apply scripts/probe-instrument.patch` | **does not apply** (`sim_tdm8_render.cpp:119`): the patch's hunks are written against the tie code this round removed (`tie_pop`, `last_end_id`), so step 5 cannot run unchanged; `set -e` stops there |

Step 5's five runs, re-run with the head's own instrument (`--law-boundary`
prints the per-PDU nearest-pop histogram that `probe-instrument.patch` added)
and R457's own `probe-setpoint-minus-one.patch` applied to a datapath copy:

| R457 run | Equivalent at the head | Result |
|---|---|---|
| `stdhist` (`LAW_PHASES=$STD`) | `--law-boundary=$STD` | 18 graded PASS, 88/0; histograms in the log |
| `tiehist` (+2,023..+2,028, +2,025, +2,025) | `--law-boundary=2023,...,2025,2025` | every one **NOT GRADABLE**, 0 failing (24/0) |
| `tiealone` (+2,025) | `--law-boundary=2025` | **NOT GRADABLE**, 17/0 |
| `nodwell` | R456's `bootnodwell` below | |
| `sp-std` (setpoint 7, `$STD`, +2,025, +2,026) | the same patch, `--law-boundary=$STD,2025,2026` | all 18 standing phases **graded FAIL** on fill and band; +2,025 and +2,026 **NOT GRADABLE**; 90/36 |
| (and as a standing leg) | the same binary, `--law-only` | rc 1, 106/36: exactly the 18 fill and 18 band checks |

**R456-1 `scripts/probes.sh`, `probes2.sh`, `probes3.sh`,
`check_mutant_verdict.py`** (each script rc 0; a probe whose edit string no
longer matches is reported `BUILD FAILED` by the script itself and not run):

| Probe | Result at the head |
|---|---|
| `hp-clean`, `c4-clean` (`--law-only`) | rc 0, 106/0 at both |
| `hp-a2a`, `c4-a2a` | 106/19: the ceiling and all 18 settled checks, at both |
| `hp-spp1-law`, `hp-spm1-law` | 106/36: fill and band at all 18 phases |
| `hp-spp1-crf` (`--crf-only`) | the CRF window's fill and band checks fail |
| `hp-tieon`, `c4-tieon` (+2,018..+2,035 as a standing list) | rc 1, 55/17: +2,018..+2,034 each fail **"gradable"** (named, with PDU and offset, from +7 to -7); +2,035 is graded and passes. A standing list that strays into the band now fails loudly instead of passing or failing by a rule |
| `hp-tiespp1`, `hp-tiespm1` (the same list, setpoint +/-1) | 55/19: the same 17 not gradable, and +2,035 graded and failing fill and band (delay 9.996 T and 7.996 T against 8.996 T sound) |
| `hp-tieoff` (the tie rule switched off) | not built: its edit is the removed tie line |
| `hp-boottrace` (`probes2.sh`) | rc 0, 106/0, the boot trace printed |
| `hp-bootnodwell` (`probes2.sh`) | 106/14: without the dwell, 14 phases fail their settled check, as round 1 measured |
| `c4-base-full`, `p631-base-full` (dev's base harness) | `c4cb84ff`: 155/2, #643's failure reproduced; `631eeb34`: 155/0 |
| `hp-tie36` (`probes3.sh`, +2,010..+2,045 as a standing list) | 139/19: +2,016..+2,034 not gradable, each named; the 17 graded phases pass with fill 14..14 |
| `hp-tietr18`, `hp-tietr36` (the per-PDU tie trace) | not built: their edits are the removed `tie_pop` and `last_end_id` |
| `check_mutant_verdict.py` | all seven PASS |

### R2.7 Findings answered

| Finding | Answer | Evidence |
|---|---|---|
| R456-1 F1 (MAJOR) = R457-1 F1 (MINOR): the tie rule's one-cycle premise fails at the boundary; a sound design fails and a setpoint -1 defect passes there | Ruled (5974715857): the tie rule is withdrawn. A window with a PDU end within W = 8 cycles of a pop is NOT GRADABLE, reported by phase, PDU and offset, neither pass nor fail. Every standing window must be gradable, its margin a check. Fill must read 14 exactly; the band lost its 64-cycle tie slack | R2.1 (the spread), R2.2 (`sim_tdm8_render.cpp:183`, `:195-197`, `:3228`, `:3268`), R2.3 (margins; the setpoint +/-1 mutants; the boundary diagnostic), R2.6 (their probes) |
| R456-1 F1, "required outcome": the documented rule matches the measured walk; the docs, README, TESTING and PR body no longer claim one cycle | Restated against the measured walk and the 8-cycle window | R2.4 |
| R456-1 F2 = R457-1 F2 (MINOR): `TIME_SYNC.md:451` still states the accept-pulse reading | Restated for the PDU end | `TIME_SYNC.md:451-455` |
| R457-1 S1: grade the exact PDU count per phase | Adopted: 124 per `[LAW]` phase, a `dec` check; the CRF window keeps "at least 100" | `sim_tdm8_render.cpp:3268` |
| R457-1 S2: the A2-a arm proves the settle gate, not the law grading | Unchanged, as ruled; the setpoint +/-1 arms now prove the law grading | R2.3 |
| R456-1 S2: require the stage's counters unchanged across a window | Not taken (optional) | |
| R456-1 S3: the ceiling check's name | Not taken (optional) | |
| R456-1 S1 = R457-1 S3: the accept-pulse instrument in `milan_dp` | Out of scope (a candidate new Issue) | |

### R2.8 Gate table

Pinned Verilator 5.050; GNU make 4.3 (the release tarball, sha256
`e05fdde4...8e19`, built in scratch) first on `PATH` for every suite, campaign
and diagnostic. The lane at the head for the dev-pin rows; for `c4cb84ff`, the
scratch parent (a `git archive` of the head and its submodules, every path in
a git index, no commit; `protocol-processor` at `c4cb84ff`, fetched from the
processor fork; both patches `git apply`'d after a clean `--check`, 8 files
differing from the head, 1,003 index entries). A shared host: other lanes ran
Vivado and processor simulations throughout, so wall times are indicative.

| # | Command | Where | rc | Result |
|---:|---|---|---:|---|
| 1 | `make -C tb/verilator/milan_dp_render VERILATOR=<pinned>`, cold | lane | 0 | 245/0, 65/0, leg defects 5/5; 661.3 s (`suite-dev.log`, 181,429 B, sha256 `b035d35877bf7298...`) |
| 2 | the same | scratch parent, `c4cb84ff` | 0 | the same counts; 673.8 s (`suite-c4.log`, 182,158 B, `902a039be7bb42dc...`) |
| 3 | `--law-only` from the binaries of rows 1 and 2 | both | 0, 0 | 106/0 each; +0 margin 48, +1953 margin 64 |
| 4 | `cd tb/verilator/milan_dp_render && make tdm8render-mutants VERILATOR=<pinned>` | lane | **2** | 32 checks: 28 PASS, 4 FAIL, the four pre-existing (R2.3); both setpoint arms and A2-a caught; 3,190 s (`campaign-dev.log`, 20,565 B, `3baf1aca946403e9...`) |
| 5 | the same | scratch parent | **2** | identical verdict lines; 3,274 s (`campaign-c4.log`, 20,580 B, `14e7151c00397c2f...`) |
| 6 | `cd tb/verilator/milan_dp_render && make tdm8render-law-boundary VERILATOR=<pinned> LAW_BOUNDARY_JOBS=6` | a scratch copy of the head | 0 | 81 checks, 81 PASS; 2,600 s (`bnd-dev.log`, 91,871 B, `405786f3ec86c7c2...`) |
| 7 | the same | a scratch copy at `c4cb84ff` | 0 | 81 checks, 81 PASS; 2,686 s (`bnd-c4.log`, 92,225 B, `c01000bec484f925...`) |
| 8 | item 1: `--law-boundary` (ascending), `--law-boundary=2066..1986`, and `--law-boundary=<p>` for each p in +1,986..+2,066 | both | 0 each (166 runs) | R2.1, `law-boundary-scan.md` |
| 9 | R457-1 `scripts/reproduce.sh`, unchanged | the head's trees | **1** | steps 1 to 4 pass; step 5's patch does not apply to the removed tie code (R2.6) |
| 10 | R457-1 step 5, equivalents | lane binaries | 0, 0, 0, 1, 1 | as R2.6: the tie phases not gradable; setpoint 7 fails every graded phase |
| 11 | R456-1 `probes.sh`, `probes2.sh`, `probes3.sh`, `check_mutant_verdict.py`, unchanged | the head's trees | 0 each | per probe in R2.6 |
| 12 | docs: `docs_check`, `check_em_dash --base 241f9184`, `check_doc_style` (+selftest), `check_gptp_docs` (+selftest, `--with-submodule`), `DOC_MAP.gen` / `timesync_chain.gen` / `submodule_boundaries.gen` `--check` (+selftest), `check_solution_docs` (+selftest), `check_feature_status` (+`--self-test`), `docs/traceability/gen_module_matrix.py --check`, `check_doc_paths`, `check_archive` (+selftest), `check_submodule_docs`, `check_diagram_pngs`, `gen_toc --selftest / --verify-anchors / --check` | lane at the head | 0 each | `check_doc_style` failed at `e63c4279` on the restated TIME_SYNC.md sentence (five findings); `6b96391d` fixed it |
| 13 | code: `check_cpp_idiom` (+selftest), `check_py_idiom` (+selftest), `check_hygiene --check`, `check_todo_ownership`, `check_sh_idiom`, `check_sv_idiom`, `check_port_contracts`, `check_rtl_source_lists`, `check_soc_sources`, `check_baremetal_only --check`, `check_nvm_record_space`, `check_wire_accountability --self-test`, `measure_test_evidence --check`, `measure_fail_fast --check`, `measure_naming --check`, `measure_cohesion` / `measure_control_flow --selftest` | lane | 0 each | no ratchet moved (functions under 100 lines; the driver at 867 of 1,000 module lines) |
| 14 | rtl-fast's local half: `lint_rtl.py --check --self-test` (pinned Verilator), `pp_srcs.py --check --selftest`, `behave` in `tests/` | lane | 0 each | lint 90 <= 90; behave 14 features, 404 scenarios |
| 15 | PR #638's touched gates (R2.5) | lane | 0 each | |
| 16 | `ci_scope.py` on the changed paths since dev `241f9184` | lane | 0 | `true` (RTL/tooling scope: `tb/` changed) |

Not run: the Yosys elaboration and the `syn/ooc` steps that need the pinned
sv2v v0.0.12 (this host has v0.0.13; no `hdl/` file changed); `act` and the
hosted contexts (nothing is pushed from this lane).

### R2.9 Interpretations, limits and open items

1. **S includes the CRF window.** The `[LAW]` phases walk at most 3 cycles
   in every history measured; T30's CRF window walks 4. The CRF window is
   graded by the same rule and must be gradable, so the walk is stated as 4.
   W = 4 + 4 = 8.
2. **The snap.** Prefill holds the pops before the snap, so the snap end has
   no pop on its earlier side and cannot show where it sits against the
   grid. It counts toward the clearance (from its later pop) and not toward
   the walk. The first steady end, one PDU later, carries the same relation.
3. **The band lost its 64-cycle slack** (now the pulse's one-cycle register).
   The slack existed for ties; in a graded window the first event lands more
   than 8 cycles inside both edges. Both law checks now separate a setpoint
   one event off at every graded phase, including +2,035 at a margin of 1.
4. **The diagnostic locates its own boundary** from the +0 phase's offsets,
   so it follows a model change instead of scanning a fixed list. Its alone
   set is the boundary +/-12, one run per phase and design (75 runs); the
   ruling's +/-40 alone runs are item 1's measurement (R2.1), not repeated in
   the standing target for its cost.
5. **`--jobs`** is accepted only with `--law-boundary`; elsewhere it is
   refused, since the rest of the campaign runs one arm at a time.
6. **The `make -C` defect** (round 1, section 7.7) is still unfiled and
   reaches the new target the same way, so TESTING.md states that
   `tdm8render-law-boundary` is run from the suite directory. Not fixed here:
   it is a separate Issue's.
7. **Cosmetic, pre-existing from round 1's code:** a tuple arm's verdict line
   reads `breaks "<first name>" and 35 more"` with one stray quote. Left, so
   that the driver the campaign graded is the one at the head.
8. **The processor fork's `main` has moved** to `5c71928a` (`ls-remote`); the
   scratch parent uses `c4cb84ff` as assigned.
9. **Suggestions not taken:** R456-1 S2 (counters unchanged across a window)
   and S3 (the ceiling check's name). Out of scope: R456-1 S1 = R457-1 S3,
   the accept-pulse instrument in `milan_dp`, a candidate new Issue.

### R2.10 Files in this directory (round 2)

| File | What |
|---|---|
| `HANDOFF.md` | this file |
| `PR-BODY.md` | the PR body, round 2 ("Closes #643", "Relates to #629", "Relates to #647") |
| `law-boundary-scan.md` | item 1: every phase of the +/-40 scan, three histories, both processors |
| `phase-law-tables.md` | round 1's per-phase tables; sections 8 and 9 now carry the round-2 correction |
| the rest | round 1's, unchanged (section 10 below) |

---

# Round 1 (history)

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

**Withdrawn in round 2** (see R2.1): this was one run history, and the tie rule is gone.

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
