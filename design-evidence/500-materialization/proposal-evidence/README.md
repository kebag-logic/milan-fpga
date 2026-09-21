# D3 materialization: executable evidence (milan-fpga #500)

Design evidence for the Proposed page
`docs/design/SAVED_STATE_MATERIALIZATION.md` on the page branch. This tree
is on the evidence branch `500-design-evidence` and is never merged.

## What is here

- `prototype/KL_aecp_nvm_writer.proto.sv`: candidate (b), the one
  processor-side record writer for every non-binding group.
- `prototype/KL_pp_nvm_mgr_arb.proto.sv`: the binding manager and the
  writer in front of the one `KL_pp_nvm_port`.
- `harness/`: the co-simulation. `d3_top.sv` instantiates the pinned
  processor's `KL_aecp_dyn_state`, `KL_aecp_desc_store`,
  `KL_acmp_nvm_shadow` and `KL_pp_nvm_port` (424c688f), the shipping
  `hdl/milan/KL_nvm_backend.sv`, the prototype, and the parent glue. The
  shipping firmware `sw/firmware/milan_baremetal/milan_baremetal.c` runs on
  the host through its two CSR primitives, with ONE counted change (the AEM
  image is loaded before `nvm_boot`). The uCPU and the parent's map plane
  are models (`d3_bridge.cpp`).
- `run.py`: builds every build (2 base shapes, the tracked glue under
  `D3_TRACKED`, 24 mutants), runs every case and grades named checks. Every
  mutant must be killed by the one check `KILLERS` names; the tracked glue
  must fail `TRACKED_MUST_FAIL` and pass `TRACKED_MUST_PASS`.
- `results.txt`, `results.json`: the graded run.
- `ooc/`: out-of-context area by the recipe of the saved-state page section
  8.3 (`ooc_measure.sh`, `run_ooc.sh`), the two cost proxies for candidates
  (a) and (c), and `results_ooc.txt`.

## Re-run it

From a checkout of this branch with the three submodules the local bar
names initialised (`third_party/verilog-axis protocol-processor
gptp-processor`), Verilator 5.05x, gcc, Python 3.11 or newer, sv2v and
Yosys:

    cd design-evidence/500-materialization/proposal-evidence
    export D3_OUT=/path/to/scratch/d3          # build trees and run logs
    python3 -B run.py prep                     # the two shapes' inputs, 2 s
    python3 -B run.py build --pool 1 --jobs 8  # 27 builds, about 2.5 min
    python3 -B run.py run --pool 8             # 121 runs, about 1 min
    OOC_OUT=/path/to/scratch/ooc ooc/run_ooc.sh  # 16 area rows, about 5 min

`run.py run` rewrites `results.txt` and `results.json`; its last line must
read `SUMMARY runs 121, checks 778, verdict failures 0`.
