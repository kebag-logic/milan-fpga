# D3 materialization: executable evidence (milan-fpga #500)

Design evidence for the Proposed page
`docs/design/SAVED_STATE_MATERIALIZATION.md` on the page branch. This tree
is on the evidence branch `500-design-evidence` and is never merged.

## What is here

- `prototype/KL_aecp_nvm_writer.proto.sv`: candidate (b), the one
  processor-side record writer for every non-binding group. Its restore is
  a transaction: it owns the state bus from reset, every restore wait is
  bounded by a watchdog, a DEVICE error (the port's cause, seam S1) or a
  descriptor fault aborts, the passes must agree record by record, an abort
  in pass 1 rolls every restorable owner back to its reset state, and an
  image it cannot prove ends CLOSED.
- `prototype/KL_pp_nvm_mgr_arb.proto.sv`: the binding manager and the
  writer in front of the one port, with the drain that keeps either
  manager's abandoned read's late bytes from reaching any manager.
- `prototype/KL_aecp_desc_mem_guard.proto.sv` (seam S2): response isolation
  on the descriptor store's memory face. It holds the store's next request
  while an accepted burst still owes its terminal beat, on the hard reset
  only, and publishes that debt.
- AMENDED PROTOTYPES of two PINNED modules, labelled as such and renamed so
  they cannot be mistaken for the pinned RTL:
  `prototype/KL_pp_nvm_port.amended.proto.sv` (module `KL_pp_nvm_port_amd`,
  seam S1: the terminal cause DEVICE or UNFRAMED) and
  `prototype/KL_acmp_nvm_shadow.amended.proto.sv` (module
  `KL_acmp_nvm_shadow_amd`, seams S1 and S3: the binding manager consumes
  the cause and bounds its restore walk's read phase). Each is exactly its
  pinned source (protocol-processor `424c688f`) with the amendments
  `run.py` declares in `AMENDMENTS`; every `run.py` action but `receipts`
  and `amend` refuses a file that differs by anything else, and
  `run.py amend` rewrites them.
- `harness/`: the co-simulation. `d3_top.sv` instantiates the pinned
  processor's `KL_aecp_dyn_state` and `KL_aecp_desc_store`, the shipping
  `hdl/milan/KL_nvm_backend.sv`, the prototypes and the amended port and
  binding manager, and the parent glue with the enable the restore
  releases. The TRACKED build (`D3_TRACKED`) instantiates the PINNED port
  and binding manager and no guard, as the parent ships them. The shipping
  firmware `sw/firmware/milan_baremetal/milan_baremetal.c` runs on the host
  through its two CSR primitives, with counted changes: the AEM image is
  loaded before `nvm_boot`, and its restore-timeout and enable lines report
  that the fabric holds the enable. The uCPU, the parent's map plane and the
  memories are models (`d3_bridge.cpp`). The descriptor memory is an
  in-order FIFO that accepts a request while earlier bursts are owed, as the
  parent's asynchronous CDC FIFO in front of `pp_desc_bridge` does.
  Harness-only faces, never product wiring: the peeks behind the
  cleared-first checks, the knob that lends the state bus to the stale-store
  control, the change-snoop knob, the early-enable knob, and the fault
  injection (held or failed memory reads, silent faces, a failing, delayed
  or once-erring descriptor memory, window bytes changed between the
  passes).
- THE FORMAT JUDGE has two modes. The SYNTHETIC judge (every case but the
  V1s ones) admits a narrower AAF output format, which the product refuses;
  every case whose stimulus narrows an output (V1a, V1b, V6, V8, V9, V20c,
  V20d, and every case booting from V1a's slots) is labelled so in the
  results. The SHIPPING judge (the V1s cases) is
  `hdl/milan/milan_datapath.sv`'s `sfv_supported_w` transcribed: an output
  admits exactly its declared format, an input the 1/2/4/6/8 family.
- `run.py`: builds every build, runs every case and grades named checks. It
  also runs the process-level controls and prints the file digests.
- `results.txt`, `results.json`: the graded full run.
- `ooc/`: out-of-context area by the recipe of the saved-state page section
  8.3 (`ooc_measure.sh`, `run_ooc.sh`), the two cost proxies for candidates
  (a) and (c), and `results_ooc.txt`. The amended port and binding manager
  are measured beside their pinned rows, so their increments are
  differences of two syntheses. Figures are measurements of prototypes and
  proxies out of context: estimates, never bounds on an integrated
  implementation.
- `../reviewer-probes/`: both round-two reviewers' published probes, rerun
  against this evidence in adapted copies, graded against the behaviour
  each demanded.

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
    python3 -B run.py build --pool 1 --jobs 8  # 69 builds, about 8 min
    python3 -B run.py run --pool 8             # the FULL run, about 3 min
    python3 -B run.py controls --pool 8        # 8 process controls
    OOC_OUT=/path/to/scratch/ooc ooc/run_ooc.sh  # 20 area rows, about 7 min
    python3 -B run.py receipts                 # digests of the tracked files

`run.py run` with no build named is the FULL run: every build and every
planned case must be there, or it refuses. It rewrites `results.txt` and
`results.json`, and its last line must read
`SUMMARY FULL builds 69, runs 312, checks 3462, verdict failures 0`.
Naming builds makes it a FOCUSED run: it prints that it is one, names its
builds, and writes `results-focused.*` under `$D3_OUT`, never here.

Exit status of `run` and `controls`: 0 no verdict failure; 1 verdict
failures, each printed by name; 2 refused (a build not built, an unknown
build or shape). A planned case that did not run is a verdict failure of
its own (`INCOMPLETE`). A mutant counts as killed only when EVERY check
`run.py` names for it fails, each in a run that completed; the verdict line
shows each named check's own state. `prep` and `build` stop with a non-zero
status and the failing command's log on any failure.

`run.py controls` doctors copies of the built binaries in private output
trees and runs the real CLI on them: a healthy binary as a mutant, an
executable that fails before its scenario, a failed baseline result, a
violated tracked control, a violated vacuity control, an absent tracked
build, a mutant killed by one of its two named checks, and an empty
selection. Each must end with its named exit status and diagnostic, and the
action exits 0 only if all eight do.
