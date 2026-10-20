[A652] REVIEW READY
Commit: f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d (round 4: two commits on d30a208d, no rebase, no amend; not pushed by this lane)
Changed:
- `16358b62`: `[762-DP]` now also runs at the end of the `obj_dynmap` leg (`tb/verilator/milan_dp/sim_nxn.cpp:4564-4621`, called at `:3036`). That leg's recipe is the `obj_ax1x1` argv on `endstation_ax7101_1x1_tdm8`, the shipping AX7101 1x1 TDM8 geometry. After `[DYNMAP]` the leg boots afresh and prints its elaborated stream, audio and prune parameters, which `dynmap_probes.vlt:24-41` opens as constants. Two checks then require one AAF input and the CRF Media Clock Input at sink `N_STREAMS`. Then the TRAP-1 bind, the 5.3.8.7 discard section and `[762-DP]` run unchanged. The existing legs are kept. The dynmap argv is unchanged, so the CI command table is untouched. No RTL change.
- `f3fef856`: the milan_dp README (the `obj_dynmap` row, its section intro, the `[762-DP]` paragraph, the `obj_ax1x1` substitutes).
Validation (clean clones of f3fef856, CPython 3.12.3, Verilator 5.050):
- `make -C tb/verilator/milan_dp`: rc 0, 0 failures on every leg. `obj_dynmap` has 199 checks, 15 of them `[762-DP]`; `obj_nxn` 1,981, `obj_nxndv` 1,983, `obj_nxn8` 3,765, `obj_nxn4c` 1,981.
- Elaborated parameters against the entity definition (the config's generated design argv, mapped as `sw/litex/milan_soc.py` maps it, and its `adp_shape_defaults.svh`): 19 of 22 are the same, including `N_STREAMS` 1, `CRF_SNK_IDX_C` 1, 8 wire channels, TDM8 master, loopback, `I2SPB_P` 0 and `LPF_P` 0. Three are the shared `obj_ax1x1` verification substitutes: the 100 MHz fabric clock, gPTP option OFF, and the render lane pruned.
- Wiring mutants at `milan_datapath.sv:6308` on that elaboration, built through `dynmap-build` with `DP_SRC` overridden; each run logs identical parameters. The tie-off and `[N_STREAMS:1]` (the CRF sink's level at N=1) each fail exactly `[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0` and `[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0`. The bound-level form fails exactly `[762-DP] 4 started gap: STREAM_INTERRUPTED +1`. The clean control has 199 checks and 0 failures.
- `make -C tb/verilator/milan_dp dynmap-mutants`: 16/16. A first run in the fresh clone failed its listener clean control because the render suite's generated AEM image was missing (the campaign builds that leg with `-o`). After generating the image with that suite's own targets, the re-run passed; both runs are kept.
- docs gate_50: rc 0 x14 (`shard 0/35 refused`, 34 driver cases).
- Other 82 docs-workflow commands: 80 rc 0. The same two host-only self-tests fail as in rounds 2-3, on files unchanged since the base, with identical failure lines.
- Builder bank: pass, except gate 11 NOT RUN.
- Not re-run, because nothing of theirs changed since d30a208d: avtp_rxmon, crf_rx, the 63-suite sweep, Yosys, route-1x1.
Acceptance criteria: met.
- Item 1: the `[762-DP]` count-graded case runs on the AX 1x1 TDM8 elaboration with its parameters logged. The clean leg passes, and the tie-off and the `[N_STREAMS:1]` mutant each fail named `[762-DP]` checks on that elaboration.
- Item 2: the PR body names each leg's entity (`obj_nxn4c` is the retired Arty 4x4), and both mutant script headers name their shapes.
- Item 3: Status and Known limitations cite the hosted run at d30a208d (63 success), with `Physical gPTP` skipped.
Updated PR-BODY.md (Round 4 section) and HANDOFF.md are in the lane's output folder.
Open risks/questions:
- Pre-existing tree text still calls `obj_nxn4c` "shipping Arty": the README row, the `build-nxn4c` comment, and the `CASE_OPTIONS_nxn4c` banner in the CI command table.
- `AX1X1_BUILD`'s "byte for byte" comment predates the shipping `--audio-interface-render 8`.
- `dynmap-mutants` does not make its listener leg's inputs.
- Each of these three is a candidate for its own Issue; none is changed here.
- R663-3-S1 (optional, not assigned) is not taken.
- No hardware; physical calibration NOT RUN.
