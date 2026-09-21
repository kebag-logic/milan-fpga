# D3 materialization: executable evidence (milan-fpga #500)

Design evidence for the Proposed page
`docs/design/SAVED_STATE_MATERIALIZATION.md` on the page branch. This tree
is on the evidence branch `500-design-evidence` and is never merged.

## What is here

- `prototype/KL_aecp_nvm_writer.proto.sv`: candidate (b), the one
  processor-side record writer for every non-binding group. Its restore is
  a transaction: it owns the state bus from reset, every restore wait is
  bounded by a watchdog, and an abort in pass 1 rolls every restorable owner
  back to its reset state.
- `prototype/KL_pp_nvm_mgr_arb.proto.sv`: the binding manager and the
  writer in front of the one `KL_pp_nvm_port`, with the drain that keeps an
  abandoned read's late bytes from reaching any manager.
- `harness/`: the co-simulation. `d3_top.sv` instantiates the pinned
  processor's `KL_aecp_dyn_state`, `KL_aecp_desc_store`,
  `KL_acmp_nvm_shadow` and `KL_pp_nvm_port` (424c688f), the shipping
  `hdl/milan/KL_nvm_backend.sv`, the prototype, and the parent glue with the
  enable the restore releases. The shipping firmware
  `sw/firmware/milan_baremetal/milan_baremetal.c` runs on the host through
  its two CSR primitives, with TWO counted changes: the AEM image is loaded
  before `nvm_boot`, and its restore-timeout and enable lines report that
  the fabric holds the enable. The uCPU and the parent's map plane are
  models (`d3_bridge.cpp`). Harness-only faces, never product wiring: the
  peeks behind the cleared-first checks, the knob that lends the state bus
  to the stale-store control, the change-snoop knob, and the fault injection
  (held or failed memory reads, silent faces, a failing descriptor memory).
- `run.py`: builds every build, runs every case and grades named checks. It
  also runs the process-level controls and prints the file digests.
- `results.txt`, `results.json`: the graded full run.
- `ooc/`: out-of-context area by the recipe of the saved-state page section
  8.3 (`ooc_measure.sh`, `run_ooc.sh`), the two cost proxies for candidates
  (a) and (c), and `results_ooc.txt`. Figures are measurements of
  prototypes and proxies out of context: estimates, never bounds on an
  integrated implementation.

## Shapes

`1x1` and `8x8` are the two SHIPPED configurations. `1x1r2` is a SYNTHETIC
test configuration, derived at prep time from the 1x1 one by one line:
`clocking.audio_unit_rates_hz: [48000, 96000]`. The builder accepts it and
marks the 96 kHz rate planned. It exists so that a legal non-default sampling
rate can be saved and restored at all; no shipped configuration lists two
rates, and no configuration the builder emits has two configurations.

## Re-run it

From a checkout of this branch with the three submodules the local bar
names initialised (`third_party/verilog-axis protocol-processor
gptp-processor`), Verilator 5.05x, gcc, Python 3.11 or newer, sv2v and
Yosys:

    cd design-evidence/500-materialization/proposal-evidence
    export D3_OUT=/path/to/empty/scratch/d3    # build trees and run logs
    python3 -B run.py prep                     # the three shapes' inputs
    python3 -B run.py build --pool 1 --jobs 8  # 55 builds, about 6 min
    python3 -B run.py run --pool 8             # the FULL run, about 2 min
    python3 -B run.py controls --pool 8        # 7 process controls
    OOC_OUT=/path/to/scratch/ooc ooc/run_ooc.sh  # 16 area rows, about 6 min
    python3 -B run.py receipts                 # digests of the tracked files

`run.py run` with no build named is the FULL run: every build and every
planned case must be there, or it refuses. It rewrites `results.txt` and
`results.json`, and its last line must read
`SUMMARY FULL builds 55, runs 230, checks 2524, verdict failures 0`.
Naming builds makes it a FOCUSED run: it prints that it is one, names its
builds, and writes `results-focused.*` under `$D3_OUT`, never here.

Exit status of `run` and `controls`: 0 no verdict failure; 1 verdict
failures, each printed by name; 2 refused (a build not built, an unknown
build or shape). A planned case that did not run is a verdict failure of
its own (`INCOMPLETE`). A mutant counts as killed only by its named check
in a run that completed. `prep` and `build` stop with a non-zero status and
the failing command's log on any failure.

`run.py controls` doctors copies of the built binaries in private output
trees and runs the real CLI on them: a healthy binary as a mutant, an
executable that fails before its scenario, a failed baseline result, a
violated tracked control, a violated vacuity control, an absent tracked
build and an empty selection. Each must end with its named exit status and
diagnostic, and the action exits 0 only if all seven do.
