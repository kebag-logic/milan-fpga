[A427] REVIEW READY
Commit: `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5` (merge head, local and not pushed). Tree `554756a545927a7e1aba734e2b7d8f4e90ba63cd`; parents `a9f5e34f` and dev `7390b43627032c71c470e2aa8d0845eb5b740663`. The subject is `Merge dev into 607-xdc-clock-names`, with no body and no trailers.

Changed: one merge commit, resolved per assignment 5874480647 and disposition 5874542826.
- **Conflicts.** Exactly the three permitted files; everything else auto-merged unedited.
  - `sw/litex/platforms/alinx_ax7101.py` keeps both imports. The `BoundedEthVivadoToolchain` replacement runs first, then #395's `configure_commands()` pre-placement hooks and `kl_timing_grade_reports` post-route hook.
  - `sw/builder/test_builder.py` keeps both functions. The run list holds `test_commercial_timing_grade` and `test_clock_crossing_constraints` once each: 96 entries, no duplicate, and no new gate id beyond dev's `36b`.
  - `docs/integration/BUILDING.md` keeps #395's grade and corner block, then #607's refusal and Ethernet-bound block.
- **Processor.** The `protocol-processor` gitlink and checkout are at dev's `c951a9ff`; no lane pin changed.
- **No stale-statement commit.** I found no statement the merge makes stale. The checked list is in the handoff.

Composition (rule 2). In all three real sweep builds, the emitted Tcl runs:
- `milan_eth_constraints` at line 271, between `synth_design` (258) and `opt_design` (275);
- `kl_timing_grade_configure` at 280, before `place_design` (284);
- `kl_timing_grade_reports alinx_ax7101_signoff` at 314, after `route_design` (303) and before `write_bitstream` (325).

Every seed wrote all 17 `*_signoff_*` reports. The logs show `quasi_static cells=112 setup=4 hold=3` and `budget_ns=8.000`. The two lanes' interaction reports use different names.

Re-sweep (rule 3). AX7101 1x1 TDM8 at `c7ee5cbd`, sequential, `--vivado-max-threads 16` under `taskset -c 0-15`, round-1 recipe. Values are the worst over #395's Slow/Fast models at 0 and 85 C:

| Seed | WNS ns | TNS | WHS ns | THS | Eth slack vs 8 ns (eth->sys / sys->eth / eth->milan / milan->eth) | CW |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| AltSpreadLogic_high | +0.312 | 0 | +0.036 | 0 | +6.141 / +6.644 / +6.465 / +6.591 | 0 |
| ExtraTimingOpt | +0.309 | 0 | +0.014 | 0 | +6.279 / +6.719 / +6.583 / +6.591 | 0 |
| ExtraPostPlacementOpt | +0.063 | 0 | +0.036 | 0 | +6.136 / +6.826 / +6.443 / +6.691 | 0 |

- The +0.030 ns rule holds at every declared corner for every seed.
- In all seven interaction reports per seed, the four Ethernet pairs read `Max Delay Datapath Only` at 8.00 ns, with no unsafe row.
- Each log has 884 WARNING, 0 CRITICAL WARNING and 0 ERROR, with 0 × 12-4739/20-1307/12-5201. The build gate accepted every bitstream.
- The in-build #395 signoff reports equal the read-only per-corner reports.
- The generated ROMs match dev's `c951a9ff` digest rows.

Validation at `c7ee5cbd`: 88 gate commands, all rc 0, each with a log-hash receipt, run sequentially after the sweep.
- **Pins-only environment** (fresh; no picolibc or compiler-rt): `python3 sw/builder/test_builder.py --require-elaboration --require-rv32` returns `ALL GATES PASS EXCEPT 1 NOT RUN`, the historical Arty calibration report. 96 arms ran, with the four `[constraints] shipping ... PASS` lines and three `[timing grade]` lines.
- **Bench banks:** `--require-rv32 --require-elaboration` gives 1 NOT RUN (the same calibration report). The compiler-absent run gives 2 NOT RUN, adding the expected compiled census.
- **Direct tests:** `sw/builder/test_clock_constraints.py` and `sw/builder/test_timing_grade.py` pass in both environments.
- **Live control:** the planted wrong-name control got vendor rc 0, and the build gate REFUSED it. The checkpoint is unchanged.
- **Docs and static gates:** the full docs-check job list. The Markdown gates ran in `$VALIDATION_TOOLS/md-venv-40cdefe08ebd`, and `check_em_dash --base` and `git diff --check` used `7390b436`.
- **Routing correction.** The two `gen_hdl_reference` rows first ran in the Markdown environment and refused because it lacks the pinned `pyslang`. They are not Markdown gates. I re-ran them with the round-1/3 pinned `pyslang` and both were rc 0; the refused receipts are kept.
- **Not run on the host:** `act_ci.py --selftest` (AGENTS.md section 5).

Acceptance criteria:
- **Rule 1** (keep both behaviours): met.
- **Rule 2** (composition): met, by the emitted Tcl, the shipping-hook test and the pins-only bank.
- **Rule 3** (re-sweep): met.
- **Rule 4** (hygiene): met. There is no stale commit, the Markdown gates used the pinned environment, and the baseline is the dev parent.
- **#607 acceptance 1-4** hold at the merge head.

Open risks/questions:
- The merge is local only, so the push and the hosted `elaborate`/`rtl-fast` runs belong to the manager.
- Seed builds took 29-59 min, slower than round 1. Timing is unaffected.
- The delta review is next.
