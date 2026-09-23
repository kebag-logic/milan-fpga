[A204] REVIEW READY
Commit: `f815577559d4922c945dcf1436d4394ff2c10567` on `529-crf-input-counters` (four commits on dev `ede8d48e`). It is not pushed from this lane: the push and the draft PR (body prepared, `Closes #529`) are the coordinator's.
Changed:
- `hdl/milan/milan_datapath.sv`: all ten `KL_crf_rx` Table 5.16 outputs are connected. A gather-face row serves them for STREAM_INPUT `N_STREAMS`, only when the shape declares the CRF sink, full 32-bit at their Table 7-157 quadlets under `counters_valid = 0xF3F`. AAF rows keep `0xFFF`, and undeclared indices keep NO_SUCH_DESCRIPTOR with the empty body. The Table 5.22 arbiter's STREAM_INPUT row widens by the CRF sink, so `dirty_p_o` reaches the processor's rate-limited scheduler as {STREAM_INPUT, `N_STREAMS`}. No processor, pin or product-shape change.
- `tb/verilator/milan_dp/sim_nxn.cpp`: `[CTRS-CRF]` (54 checks on each broad leg) and `[NOTIFY-CRF]` (8 checks on the timed leg).
- Docs: REGISTER_MAP (gap closed, with evidence per criterion), compliance matrix 5.4.2.25 -> implemented, audit B4, REGISTER_MAP_CLASSES, roadmap, FR_NFR, builder page, milan_dp README, CHANGELOG (unreleased, no VERSION step). Comment-only fixes in `KL_crf_rx.sv`. `port_docs.budget` regenerated.
Validation (pinned simulator 5.050, 8 jobs):
- milan_dp, every leg of its `run` recipe: nxn 1687/0, nxndv 1689/0, nxn8 3115/0, nxn4c 1687/0, notify 143/0, obj_dir 230/0, nolpf 230/0, prune 33/0, ax1x1 227/0, aclk 139/0, gptp 181/0, gptplat 181/0, render mutants 6/6.
- pp_shadow 371/0; milan_dp_render 150/0 + 59/0 + leg defects 5/5; crf_rx 13836/0; behave 316 scenarios passed.
- `lint_rtl.py --check` 90 <= 90; `xvlog_gate.py --check` PASS (`hdl/` 0 findings); `check_sv_idiom`, `check_port_contracts`, `check_rtl_source_lists` OK; `gen_module_matrix.py` regenerated with no change, `--check` up to date; `check_em_dash` 0 findings over 121 added lines; 26 further docs-workflow gates exit 0.
- Mutations, each red: the row removed, quadlets 0/1 swapped, a 16-bit FRAMES_RX slice, a claimed tv pair, the dirty source removed, the CRF row answering for the AAF inputs, the AAF guard answering for the CRF input, and one tally unwired.
- Focused synthesis of `milan_datapath`: 1,631,301 -> 1,632,435 generic cells (+1,134, +0.07%). No other top contains it.
Acceptance criteria:
- REGISTER_MAP closure criteria 1-4: met, with evidence as above.
- Milan-compatible verdict on silicon: not yet, it follows the merge (#117).
Open risks/questions:
- The prompt's "compact mask" is read as Milan Table 5.16 at the IEEE offsets (`0xF3F`, tv pair unclaimed), which is the repository's counters contract; only the Stream Output table compacts. Reviewers should confirm.
- No VERSION minor reserved.
- Not run locally: `milan_dp_gptp` (physical-rate selection), the full sweep, the Yosys bank, `act`, and the HDL reference build (parser wheel absent).
