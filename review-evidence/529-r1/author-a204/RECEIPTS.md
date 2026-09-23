# #529 receipts ([A204])

Base: `ede8d48ecd7c7f589a14b957951f040d92c99c70` (live dev at assignment).
Head: `f815577559d4922c945dcf1436d4394ff2c10567` (branch `529-crf-input-counters`, local, not pushed).
Submodule pins (unchanged): protocol-processor `424c688f`, gptp-processor `c1b61743`,
third_party/verilog-axis `48ff7a7e`.

Commits:

| SHA | Subject |
|---|---|
| `869da89e` | Serve the CRF Media Clock Input's Table 5.16 bank on GET_COUNTERS and deliver its dirty pulse to the Table 5.22 arbiter |
| `2a798d19` | Grade the CRF input's counters row, wrap, isolation and one-second push at the root in sim_nxn |
| `d8340bd5` | Record the CRF Stream Input counter gap as closed by #529 with its root-wire evidence |
| `f8155775` | Log the CRF input counters as an unreleased product change |

`git diff 2a798d19 f8155775 -- hdl tb` is empty: every suite below ran on the RTL and
harness bytes that are committed.

## Tool identity

- Simulator: the scoped wrapper `pinned-tool-bin/verilator` (sha256 `905795b9...`) reporting
  `Verilator 5.050 2026-07-01 rev v5.050`; its `verilator_bin` sha256 `44898b22af41...bfdd`.
  Put first on `PATH` for every build. The host default (5.052) was not used.
- Synthesis: Yosys 0.66, sv2v v0.0.13, jemalloc allocator (syn/yosys/run.sh default).
- xvlog: the bench Vivado 2026.1 install that `xvlog_gate.py` resolves (analysed, not skipped).
- C++: g++ 16.2.1. Python 3.14.7. behave 1.3.3.
- Jobs: `VERILATOR_JOBS=8` (8 cores).

## Suites (all at the committed RTL/harness bytes)

The 10-minute foreground limit per command meant `make -C tb/verilator/milan_dp` was run as
its own `make -n run` recipe, split into five sequential chunks without reordering
(logs `logs/suite_milan_dp_{A..E}.txt`, recipe `milan_dp_run_recipe.sh`); `make gptp` ran
first on its own.

| Suite / leg | Result |
|---|---|
| milan_dp `obj_gptp` | 181 / 0 fail |
| milan_dp `obj_gptplat` | 181 / 0 |
| milan_dp `obj_dir` (sim_main, 1x1) | 230 / 0 (1 section guarded on this shape, as at base) |
| milan_dp `obj_notify` (timed, AX 1x1) | 143 / 0 (includes 8 new `[NOTIFY-CRF]`) |
| milan_dp `obj_nxn` (4x4) | 1687 / 0 (includes 54 new `[CTRS-CRF]`) |
| milan_dp `obj_nxndv` (divergent 4x4) | 1689 / 0 |
| milan_dp `obj_nxn8` (8x8) | 3115 / 0 |
| milan_dp `obj_nxn4c` (shipping Arty 4x4) | 1687 / 0 |
| milan_dp `obj_nolpf` | 230 / 0 |
| milan_dp `obj_prune` | 33 / 0 |
| milan_dp `obj_ax1x1` | 227 / 0 |
| milan_dp `obj_aclk` | 139 / 0 |
| milan_dp `render_mutants.py` | 6 / 6 mutants caught |
| pp_shadow (`make`) | 371 / 0 |
| milan_dp_render `tdm8render` | 150 / 0 |
| milan_dp_render `tdm8render-multi` | 59 / 0 |
| milan_dp_render `tdm8_render_mutants.py --leg-defects` (the rest of its `run`) | 5 / 5 caught |
| crf_rx (`make`) | 13836 / 0 |
| behave (`tests/`, whole) | 14 features, 316 scenarios, 1515 steps passed |

Not run: `milan_dp_gptp` (the physical-rate selection outside the 55 default suites; one
binary longer than the foreground limit), `scripts/run_all_suites.sh`, the Yosys bank
(`syn/yosys/run.sh` over every top), the `tdm8render-mutants` gateware campaign (an explicit
target outside `make`), `act`/Docker, and the HDL reference build (`gen_hdl_reference.py`
refuses without its pinned parser wheel; installing it would be a shared install).

## Gates (at `f8155775`)

| Gate | Result |
|---|---|
| `scripts/lint_rtl.py --check` | PASS, 90 <= ratchet 90 (unchanged from base) |
| `scripts/lint_rtl.py --pragmas` | PASS |
| `scripts/xvlog_gate.py --check` | PASS, `hdl/` 0 findings, pinned processors 4 == ratchet |
| `scripts/check_sv_idiom.py` | OK |
| `scripts/check_port_contracts.py` | OK; budget regenerated with `--write-budget` (see note) |
| `scripts/check_rtl_source_lists.py` | OK |
| `docs/traceability/gen_module_matrix.py` (regenerated) / `--check` | no tracked output changed; up to date, 69 modules, 0 untested |
| `scripts/check_em_dash.py --base ede8d48e` | 0 findings over 121 added lines in 9 pages |
| 26 further docs-workflow gates (`logs/docs_gates_final.txt`) | all exit 0 |

Port-contract budget note: regenerating removes this change's three `crf_rx.cnt_*_o`
unjustified-open rows. The same regeneration also drops three `chan_tdm_render.*` rows and
updates the header port totals: those were already stale at base (the base gate printed
"the ratchet can be lowered ... 6 recorded connection(s) gained a rationale or left").

`measure_test_evidence --check` and `measure_fail_fast --check` both pass and report
pre-existing slack ("can be lowered"); this change adds no suite and no runner, so neither
budget was touched.

## Mutations (at `d8340bd5`, whose `hdl/` and `tb/` bytes equal `f8155775`'s; receipt `mutation_receipt.txt`, driver `mutate.py`)

Each mutant is a copy of `hdl/milan/milan_datapath.sv` with the named edit, built through the
suite's own `print-srcs`/`print-dp-vflags` with `DP_SRC` overridden (`leg.sh`), then run.
M1 and M8 remove the only reader of some tallies. The simulator would then drop those flops,
and the harness seeds them by name, so it would no longer compile. These two mutants also
mark the seven tally wires `public_flat_rw`, a simulator pragma with no logic effect, so the
red is behavioural.

| Mutant | Edit | Leg | Red checks |
|---|---|---|---|
| M1 row removed | drop `: ctr_crf_w ? ctr_crf_blk_w` from the answer mux | nxn | 18 (mask, all ten signatures, wrap) |
| M1 | same | notify | 1 (the pushed mask) |
| M2 ML/MU swapped | quadlet 0 <- `crf_unlockcnt_w`, 1 <- `crf_lockcnt_w` | nxn | 2 (signatures @0, @4) |
| M3 16-bit slice | quadlet 11 <- `{16'd0, crf_pducnt_w[15:0]}` | nxn | 2 (signature @44, wrap readback) |
| M4 tv pair claimed | `CTR_VALID_CRF_C = 0xFFF` | nxn | 3 (every mask check) |
| M5 dirty removed | `pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w}` | nxn | 1 (arbiter bit N) |
| M5 | same | notify | 8 (every `[NOTIFY-CRF]` check) |
| M6 CRF row answers every input | index term dropped, CRF arm ahead of the AAF arm | nxn | 8 (7 AAF `[CTRS]` + the `[CTRS-CRF]` isolation check) |
| M7 AAF guard admits N | `ctrq_index_r <= N_STREAMS` in `ctr_sin_w` | nxn | 18 (mask 0xFFF, all signatures, wrap) |
| M8 one tally unwired | quadlet 2 <- `32'd0` | nxn | 3 (signature @8, both SI wrap reads) |

Clean positive control: the same legs at the same head, unmutated, 1687/0 and 143/0 above.

## Synthesis (focused `syn/yosys/run.sh --top <T> --no-structural`, head measured at `d8340bd5`, same RTL as `f8155775`)

| Top | Base `ede8d48e` | Head | Delta |
|---|---:|---:|---:|
| `milan_datapath` | 1,631,301 cells | 1,632,435 cells | +1,134 (+0.07%) |

The base figure came from restoring the base `milan_datapath.sv` bytes (`git show
ede8d48e:...`) into the lane, synthesizing, and `git checkout HEAD --` straight after (tree
clean afterwards). `datapath_wrap` is not affected: it wraps `traffic_controller_802_1q`, not
`milan_datapath` (185,015 cells at head). `KL_crf_rx.sv` changed only in comments.
The growth is the seven 32-bit tallies and their incrementers, which synthesis used to
remove as unread, plus the 12-way answer arm and one arbiter row. Generic `synth` cells
are not a device LUT/FF count.
