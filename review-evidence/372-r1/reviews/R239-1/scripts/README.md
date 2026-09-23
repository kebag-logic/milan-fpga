# R239-1 reviewer scripts (issue #372 / PR #518, exact head 059c3a60b8290873ed9fd14673f9981e8af754ce)

All scripts are portable: every path is an argument. Placeholders used below:
`<clone>` the review clone at the exact head; `<scratch>` a disposable copy of that head
(`git archive` of the head plus `third_party/verilog-axis` at its gitlink); `<pinned>` the scoped
Verilator 5.050 selector; `<layer>` the package root it executes from; `<out>` this directory.
No script writes to `<clone>`; builds are capped at 8 jobs.

| Script | Purpose | Invocation |
|---|---|---|
| `verify_tool_mtree.py` | hash every regular file of the pinned package against its mtree | `python3 verify_tool_mtree.py <layer>` |
| `probe_mutants.py` | 13 independent DUT mutants (not in the campaign) and 20 checker-weakening probes run against the campaign | `python3 probe_mutants.py <scratch> <pinned> <out>/receipts/probes/mutants dut\|weaken [name-prefix]` |
| `top_bind_probe.sh` + `top_bind_witness_stub.cpp` | build the ORIGINAL ptp_ts_top leg (unchanged sim_main.cpp) with the #372 checker and bind added, and count witness calls on the product mux instance | `sh top_bind_probe.sh <scratch> <pinned> <dir holding witness_stub.cpp>` |
| `sem_probe.sv` + `sem_main.cpp` | pinned-tool semantics named in the guide: reset-edge skip, vacuous pass after reset, first-edge `$past`/`$stable`, pass action per edge, `assume` | `<pinned> --cc --exe --build -j 8 [--assert] --top-module sem_probe sem_probe.sv sem_main.cpp -o Vsem` then run with `+verilator+error+limit+1000` |
| `verify_integrity.py` | prove a checkout equals a commit: blob bytes, kind, mode, index, required gitlinks, clean status | `python3 verify_integrity.py <clone> <head> <tree> third_party/verilog-axis protocol-processor gptp-processor` |

The cover and `$assertvacuousoff` variants of the semantics probe are in
`receipts/probes/semantics/` (`sem_probe_cover.sv`, `sem_probe_vacoff.sv`).
