[A703c] REVIEW READY
Commit: 8b28ebaf035e786ccf5b8e50098dbc111f51831f (branch 814-soc-timing-cut, dev 1e80128f plus five commits, unchanged from rounds 1 and 2: no gate needed a fix, so round 3 added no commit; not pushed)

Changed: nothing this round. At the head, all in the SoC wiring, the three cuts: `SPIPHYStage` between LiteSPI's core and its PHY (`sw/litex/milan_soc.py:2465`, via `MilanSoC.add_spi_flash` `:3670`); `AXIReadyStage` on the CPU memory port's aw and ar between its crossing and LiteDRAM (`:2397`, `:2391`); `RegisteredRefresher` through LiteDRAM's `refresh_cls` (`:2430`, `add_staged_sdram` `:2454`). Plus the check `sw/litex/test_soc_timing_cuts.py`, its inventory entry, and TESTING.md and CLOCK_DOMAINS.md.

Validation:
1. **The round-2 route set under #818.** PR #820's gate at `32f0d9b5`, used in scratch and not committed, judged the three routed directories round 2 made at this head: `pp_resource_gate.py check <shipping> --endpoint route-1x1 --comparison <AltSpreadLogic_high> --comparison <ExtraTimingOpt>`.
   - It gave rc 0, `RESULT: PASS`, with **ExtraPostPlacementOpt selected** at +0.128 ns worst-corner WNS.
   - Its corners: Slow 0C / 85C WNS +0.128, WHS +0.059; Fast 0C / 85C WNS +1.311, WHS +0.030. All are at or above the +0.030 / 0 floor.
   - The fall from the +0.440 ns record is 0.312 ns, printed as `WARNING`. LUT -185, FF +315, slices -16; RAMB and DSP unchanged; the route is complete.
   - AltSpreadLogic_high (+0.039) and ExtraTimingOpt (+0.010, below the floor at its slow corners) are not selected.
   - Controls on the same inputs: the shipping route alone with `--shipping-selection` gives rc 0 with the same verdict; with neither flag, rc 2; the ExtraTimingOpt directory alone, rc 2. #818's own self-tests give 304 arms + 500 fuzz PASS, and 230 of 230 mutants fail.
2. **The full sweep**: `scripts/run_all_suites.sh --shard k/4` in four units, 64 of 64 PASS (14, 17, 17, 16), rc 0 x4.
   - On the first start, shards 0, 2 and 3 aborted in the same second, in the preflight's cancellation self-test (hard-stop cleanup: `CLEANUP FAILED: owned descendants remain`), during a host memory dip to about 19 GB. No suite had started.
   - Rerun unchanged (same clones, specs and units, 75 s apart), each passed the self-test and its suites.
3. **rtl-fast**, the workflow's step bodies replayed at the head (the head is unpushed): `rtl-fast: success`, all 12 needed jobs, 56 steps rc 0, `rtl=true`.
4. **The docs workflow gates**: 42 steps rc 0, plus builder leg 1 on the LiteX interpreter (rc 0), the 5 markdown gates on CPython 3.12.3 (rc 0), and the no-git step's `docs_check` and `feature_status` on an archive export (rc 0). `gate_42` was not run, by AGENTS.md section 5: it runs the candidate's act runner on the host.
5. **The builder bank**: `python3 sw/builder/test_builder.py` rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN`. These are the same two arms dev's bank leaves unrun on this host: gate 1b's MAKEFLAGS mutation is inert under Make 4.3, and gate 11 needs the absent mf48 build.
6. **Unchanged from round 2 at this head**: ooc-1x1 and ooc-8x8 gate PASS, equal to the record; the capture's six arms and three controls rc 0 (worst 13.85922 ms against 24.5 ms); the service-budget runs, 1x1 and 8x8, PASS. From round 1: `test_soc_timing_cuts.py` 15 arms PASS.

Acceptance criteria:
- Met under the round-3 ruling (issuecomment-6527475726). The route set meets the build floor at every corner on its best directive, under #818, and the fall is a warning.
- F1 to F3 are each more than 1 ns from the worst path at every directive.
- The gates the STOP skipped all pass.
- The record is not re-recorded, by the record rule (issuecomment-6525285974): it is re-recorded once on dev after the last release merge.
- No Vivado ran this round.

Open risks/questions:
- The WNS is now set by families this change does not touch: F4, the memory bridges into the CPU DMA port, the milan reset into the MMCM servo's reset synchroniser, the AECP micro-CPU, LiteEth TX and the LiteDRAM bank machines.
- The flash PHY stage has not been on hardware.
- The sweep's cancellation self-test can abort under host load.
- The PR body cites the ruling and #818, drops the STOP and owner-decision text, and keeps "Closes #814".
