# Parent suites that build gptp-processor (milan-fpga dev e9cbb676)

For the manager: the consumer gate list ran one of the suites that execute
this engine (gptp_shadow). The list below is read from each suite's Makefile
and was then measured. "Engine runs" means the gPTP plane is elaborated on,
so a test drives `KL_gptp_engine` and its microcode image.

## A. The engine runs (plane on)

| Suite (how CI reaches it) | Source | In the consumer list | Base 43acfbcc | Head, no companion (gitlink 093b9c3b) | Adoption E 564466ea (head 2022d363 + four companions; snapshot D 3f053cc1 gave the same) |
|---|---|---|---|---|---|
| `tb/verilator/gptp_shadow` | `Makefile:6-30` (`GPTP_DIR`) | yes (gate 6) | 309/309 (Round 1) | 305/309 at 53ac2e9d (Round 1; same RTL) | rc 0, 310/310, mutation arm 9 controls, 0 failures |
| `tb/verilator/milan_dp` leg `gptp` (in its default `run`, `PREFIX_CASES`, `Makefile:557`) | `Makefile:367-373`, `sim_gptp.cpp` | **no** | rc 2, 179/182 (#82 rows) | rc 2, 171/182 (#82 + #85 rows) | rc 0, 185/185 |
| `tb/verilator/milan_dp` leg `gptp-lat` (same `run`) | `Makefile:420-429`, `sim_gptp.cpp` | **no** | not run (same source as `gptp`) | rc 2, 171/182 | rc 0, 185/185 |
| `tb/verilator/milan_dp_gptp` (leg `ax1x1gptp`; nightly/manual `physical-gptp` job, excluded from the default sweep) | `milan_dp/Makefile:539`, `sim_ax1x1gptp.cpp` | **no** | rc 2, harness 141/143 (#82 rows) | rc 2, harness 129/143 (#82, #85 and #84 rows) | rc 0, harness 155/155; setup abort 6/6, no-TX 20/20, no-Pdelay 14/14, recentre 14/14 |
| `tb/verilator/milan_dp_gm_steps` (leg `gmstep` + its controls) | `milan_dp/Makefile:393-401`, `sim_gmstep.cpp` | **no** | not run | not run | rc 0, 190/190, 6/6 controls caught |
| `tb/verilator/gptp_plane` | `Makefile:5-34` | no | not run | rc 0 at 6814d01c (head + #85 companions; this suite compiles none of the companion files): 29/29, phc_step 62/62, campaign 8/8 | as head |
| `tb/verilator/gptp_tables` | `Makefile` (`GPTP_DIR`) | no | not run | rc 0 at 6814d01c: 36/36, every limit arm caught | as head |
| `tb/verilator/gptp_txts` | `Makefile` (`GPTP_DIR`) | no | not run | rc 0 at 6814d01c: 85/85, 6/6 controls | as head |
| `tb/verilator/tsn_fuzz` | `Makefile` (`GPTP_DIR`) | no | not run | rc 0 at 6814d01c, but both field campaigns are SUITE-SKIP here (the external traffic generator is absent), so the engine was **not** exercised; only grader self-tests 54/54 and traceability 2/2 ran | as head |

The base and head columns for `milan_dp_gptp` stop at the harness: its make
recipe ends at the first failing step, so their verifiers did not run.

What each companion covers:

- `#82` rows (fail at base): the boot and reset publication names thisClock
  as grandmaster and arms the holdover (`sim_gptp.cpp:825, 826, 835`;
  `sim_ax1x1gptp.cpp:1149, 1197`).
- `#85` rows: the path shape (see `path-shape-search.md`).
- `#84` rows (physical leg only): after the peer is lost this station is
  grandmaster, so tu is clear once the holdover has run, and CLKV "healthy"
  no longer implies the peer is elected (`sim_ax1x1gptp.cpp:344, 948, 1015,
  1018, 1055`).

## B. The sources are compiled but the plane is off

These elaborate `-GGPTP_PLANE_EN_P=0` (`milan_dp/Makefile:102-103`,
`DP_VFLAGS`), and `milan_datapath.sv:7531` then elaborates `g_gptp_off`
instead of the plane, so the engine is not instantiated and not graded:
every other `milan_dp` case (`base notify crflic dynmap nxn nxndv nxn8 nxn4c
nolpf prune ax1x1 aclk`, the counter cases, `render-mutants`), the suites that
import its source list and flags (`milan_dp_mclk`, `milan_dp_render`,
`capture_coherence`, through `print-srcs` / `print-dp-vflags`), and
`pp_shadow` (`Makefile:98`). Not run here.

## C. Static gates and builds that read gptp-processor sources

Consumer gates 3 (`xvlog_gate.py`), 4 (`check_rtl_source_lists.py`),
7 (`check_port_contracts.py`) and 11 (`lint_rtl.py`); the synthesis and SoC
flows (`syn/ooc`, `syn/yosys`, `sw/litex/milan_soc.py`), which need tools not
present here.

## Suggested widening of the consumer list

Add `make -C tb/verilator/milan_dp gptp gptp-lat` (about 2.5 min each here),
`make -C tb/verilator/milan_dp_gm_steps` (750 s here) and, where a long
budget exists, `make -C tb/verilator/milan_dp_gptp` (5171 s here under load;
the parent declares 5400 s). `gptp_plane`, `gptp_tables` and `gptp_txts` are
cheaper and also drive the engine.
