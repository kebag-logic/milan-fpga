# Reviewer scripts, R462-1 (processor PR #155, milan-fpga #639)

Every script runs from an exported tree (`git archive <rev> | tar -x`), never from a
checkout, and writes only under the directories it is given. Each script needs Verilator
5.050 first on PATH (or `python3` alone, where marked).

| Script | What it does |
|---|---|
| `lockstep_armq/gen.py` | Cuts the timer arm-port mux block out of a `protocol_processor_top.sv` (from the `// ====` line above "timer arm-port priority mux (banner)" to the line before the `// ====` above "PRNG draw-port owner mux (banner)"), byte for byte, and wraps it with the eight faces as inputs. `--mutant NAME` plants one reviewer control. |
| `lockstep_armq/lock_top.sv`, `lock_main.cpp` | `main`'s block (`armq_ref`) beside the head's (`armq_dut`) on identical random arms. Phases: fully random, a few hot faces, every face saturated, light. Resets of 1 to 4 clocks are taken mid-run with arms still offered. Uninitialised state is randomised (`--x-initial unique`, `randReset(2)`). After every edge it compares the port's valid and arm and the drop counter. Run as `Vlock_top SEED CYCLES`; it exits 1 on any mismatch. |
| `lockstep_armq/run.sh` | `run.sh MAIN_TOP HEAD_TOP AW OUTDIR [MUTANT]` builds one binary at slot width AW. |
| `lockstep_lsn/gen_shadow.py` | Writes a `KL_pp_acmp_listener` with the listener's own name, parameters and ports. It holds `main`'s listener and the head's on the same inputs and compares every output, the working record `rec_r`, the walk state `xs_r` and (in X_LATCH and X_STRT_AP) the record read bus at every rising edge. A final line `LOCKSTEP: ...` gives the edge and mismatch counts. |
| `lockstep_lsn/run_suite_shadow.sh` | Builds a suite (`tb/acmp_listener`, or `tb/pp_top` for `make gsi-build`) with the shadow in place of the listener. |
| `aq_probe.sh` | Plants one arm-queue defect in a disposable copy of the head and runs `tb/pp_top --arm-queue-only`. |
| `run_campaigns.sh` | Runs the processor campaigns that build the top or the listener, each with its own log and rc file. |
| `vivado/rederive.py` (python3 only) | Re-derives the area, timing and per-block figures from the published reports at milan-fpga `28663f5a` `review-evidence/pp639-r1/author-r1/vivado/`. |
| `vivado/gate_policy.py` (python3 only) | Applies the parent gate's tolerance policy (`syn/ooc/pp_resource_baseline.json` and `judge()` at dev `241f9184`) to those figures. The gate's identity and input-digest checks need the scratch parent and are not re-run. |
