[A656] REVIEW READY (round 3c, PR #768)
Commit: `4ff3642e8fe9a0bd48d28374350390cde553bc32` (branch `637-map-records`, local, not pushed). Dev `78ca9bdf` is merged by the merge commit `d26fca65` (parents `1e914414`, `78ca9bdf`; no rebase), followed by one README commit. Processor pin `2cbed0a9` unchanged; dev changed no gitlink. This answers the round-3c assignment, PR #768 comment 6298729116, composition only.

Changed:
- `tb/verilator/milan_dp/sim_nxn.cpp`: the `obj_dynmap` tail runs `[DYNMAP]`, then #767's `[762-DP]` case on its own fresh boot (its precondition on dev), then `[MAPREC]`. `[MAPREC]` starts by booting over an erased window, so it reads nothing the earlier cases left. The #762 function is unchanged, inside the `DYNMAP_DEFAULT_TB` block.
- `tb/verilator/milan_dp/dynmap_probes.vlt`: one shared file holding both sides' opens, so the leg prints its elaborated parameters.
- `tb/verilator/milan_dp/README.md`: the `obj_dynmap` row, the #658 section intro and the `[762-DP]` paragraph give the run order. The campaign table is re-measured at 686 checks; every failure count is unchanged.
- `hdl/milan/milan_datapath.sv` auto-merged. The merge minus the lane equals dev's own change, and the merge minus dev equals the lane's own change, line for line. So #767's `stopped_i` wiring (`:7300`) and this PR's map writer and restore are both present.

Validation (clean clones, one log and one rc per command, unpiped):
- `make -C tb/verilator/milan_dp` (every leg) at `4ff3642e`: rc 0, 12,892 checks, 0 failures. `obj_dynmap` is 686/0: preamble 52 and `[DYNMAP]` 110 are shared, the #762 section adds 37 (15 labelled `[762-DP]`) and `[MAPREC]` adds 487 (dev's leg 199, this lane's 649). `obj_maprec8` 219/0, `obj_maprec4` 137/0, `obj_nxn` 1,981, `obj_nxndv` 1,983, `obj_nxn8` 3,765, `obj_nxn4c` 1,981.
- `make -C tb/verilator/milan_dp_render tdm8render-build`, then `make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4`, at `d26fca65`: rc 0, rc 0; 68 checks, 68 PASS (five clean legs, 63 of 63 controls caught).
- #767's three `[762-DP]` wiring mutants on `obj_dynmap` at `d26fca65`: clean 686/0. `'0` and `acmpl_stopped_v_w[N_STREAMS:1]` each fail exactly `[762-DP] 2 stopped gap` and `[762-DP] 3 stopped silence`. `acmpl_bound_v_w[N_STREAMS-1:0]` fails exactly `[762-DP] 4 started gap`. Nothing else moves, `[MAPREC]` included.
- docs.yml, 95 commands (em-dash against `78ca9bdf`), at `4ff3642e`: all rc 0. Both builder legs: rc 0, rc 0 (gate 11 declared NOT RUN by the builder).
- route-1x1 at `4ff3642e` (the merged RTL differs from both parents' routed RTL): rc 0. LUT 49,937 (+324 over the record), FF 52,629 (+276), SLICE 15,801, RAMB36/RAMB18/DSP 74/25/14, WNS +0.155 ns, WHS +0.036 ns, route complete. ooc-1x1 and ooc-8x8 carry from round 2, because none of `KL_pp_shadow`'s 50 source files changed since `887b6bf2`.
- Full sweep at `4ff3642e`, as the runner's four shards: rc 0 each; 63 of 63 suites, 2,188,446 checks, 0 failures, 0 timed out; the four declared `tsn_fuzz` skips.
- Void, not cited: one docs-gate launch whose relative log paths kept every command from starting, and one sweep launch under `nohup` that the runner's SIGHUP preflight refused before any suite ran. Both were relaunched from the start.

Acceptance criteria: unchanged from round 3. Met except the on-board cold cycle (no bench access here); the PR keeps "Relates to #637". Both round-3 reviews were POSITIVE at `1e914414`; this head is not yet reviewed.
Open risks/questions: none new. The round-3 residue and suggestions stay with the merge checklist, unchanged by this round. Not run because they are not in the round-3c list: the full Yosys run, xvlog, and the rtl-fast lint, elaboration and firmware steps. Their hosted counterparts run on the ready head.
