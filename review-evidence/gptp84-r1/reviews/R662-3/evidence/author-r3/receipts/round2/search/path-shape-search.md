# Whole-parent search for the old path shape (milan-fpga dev e9cbb676)

Question: which parent expectations assume the published path is the received
pathSequence only, without thisClock appended (the shape #85 corrects)?

## Method

1. Text search of every first-party parent file (submodules, generated build
   output excluded), case-insensitive:
   - `path_count|pathtrace|as_path|pub_path|path_tail` in `*.cpp *.h *.c *.py
     *.sv *.json *.yaml *.feature`: 32 files;
   - `pathsequence|received path|path ?trace` in `*.md *.sv *.py *.cpp *.c
     *.h` (history and findings excluded): 63 files, mostly prose.
2. Each hit was read and classified: does it drive this engine with a peer
   Announce and then grade the count, length or entries of the published path?
3. The suite inventory records the snapshot and result for each
   enabled-engine suite. Execution cross-checks use the unpatched-head and
   companion-adoption runs listed there. The tsn_fuzz field campaigns were
   skipped and supplied no engine-execution evidence.

## Expectations of the old shape (all now covered by a companion)

| File:line at e9cbb676 | Check | Old | Now | Companion |
|---|---|---:|---:|---|
| `tb/verilator/gptp_shadow/sim_main.cpp:891` | published full path count | 3 | 4 | gptp_shadow-85 |
| `tb/verilator/gptp_shadow/sim_main.cpp:930` | explicit one-entry PathTrace count (+ tail is thisClock) | 1 | 2 | gptp_shadow-85 |
| `tb/verilator/gptp_shadow/sim_main.cpp:943` | present path restored for servo controls | 3 | 4 | gptp_shadow-85 |
| `tb/verilator/gptp_shadow/sim_main.cpp:1003` | better Announce preserves full path count | 3 | 4 | gptp_shadow-85 |
| `tb/verilator/milan_dp/sim_gptp.cpp:984` | fabric live AS_PATH count | 4 | 5 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_gptp.cpp:1044` | GET_AS_PATH full-tail wire length | 74 | 82 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_gptp.cpp:1046` | GET_AS_PATH cdl | 48 | 56 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_gptp.cpp:1048` | GET_AS_PATH count | 4 | 5 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_gptp.cpp:1399` | wait loop for the one-entry publication | 1 | 2 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_gptp.cpp:1403` | explicit one-entry fabric PathTrace count | 1 | 2 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_gptp.cpp:1414` | explicit one-entry GET_AS_PATH cdl | 24 | 32 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_gptp.cpp:1416` | explicit one-entry GET_AS_PATH count | 1 | 2 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_gptp.cpp:1450` | in-flight response remains wholly old: count | 1 | 2 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:938` | PathTrace count (each healthy publication of the run) | 2 | 3 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:980` | GET_AS_PATH wire length | 60 | 66 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:982` | GET_AS_PATH control data length | 32 | 40 | milan_dp-85 |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:983` | GET_AS_PATH padding bytes are zero (no padding remains) | 0 | removed | milan_dp-85 |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:984` | GET_AS_PATH ordered identities | 2 | 3 | milan_dp-85 |

The sim_ax1x1gptp.cpp rows were not in the reviews: they are in the
physical-rate leg run by `tb/verilator/milan_dp_gptp`, which the default sweep
excludes (nightly and manual job).

## Hits that do not assume the old shape

| File | Why it is unaffected |
|---|---|
| `hdl/milan/milan_datapath.sv`, `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`, `hdl/milan/KL_pp_shadow.sv`, `hdl/common/csr/milan_csr.sv` | RTL that carries the count and entries through unchanged; no shape is assumed |
| `tb/verilator/csr/sim_gptp.cpp` | drives the CSR's AS_PATH inputs directly; the engine is not elaborated |
| `tb/verilator/gptp_txts/gptp_txts_wrap.sv` | leaves the path outputs unconnected |
| `tb/verilator/gptp_tables/sim_main.cpp`, `tb/verilator/tsn_fuzz/fuzz_ptp_timing.py` | comments only (loop detection; stepsRemoved) |
| `tb/verilator/milan_dp/sim_nxn.cpp` | the plane is elaborated off; grades the ownerless empty path |
| `avdecc/milan_controller.py:382` | bench check of a standalone DUT: count 1, the entity's own identity, which is `{thisClock}` (#82) |
| `scripts/baremetal_uart_smoke.py` | accepts any count 1..8; its count-3 value is a parser self-test string |
| `tests/steps/aecp_engine_*.py`, `tb/tools/*`, `sw/firmware/*` | command tables, models fed from register values, console formatting |
| `README.md:163-165`, `docs/reference/REGISTER_MAP.md:331` | "the GM followed by up to seven identities" stays true with thisClock last |
| `docs/findings/*`, `docs/history/*` | dated measurement records, not current contracts |

## Other expectations the runs found (not path shape)

Running the engine-building suites at head also found expectations of the
pre-#82 boot state and of the pre-#84 grandmaster role. They are listed in
`suite-inventory.md` and covered by `parent-adoption-milan_dp-82.patch` and
`parent-adoption-milan_dp_gptp-84.patch`.
