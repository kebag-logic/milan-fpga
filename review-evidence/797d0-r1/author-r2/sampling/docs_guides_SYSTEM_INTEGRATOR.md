# Sampling ledger: docs/guides/SYSTEM_INTEGRATOR.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 14 | sentence | `milan_datapath` is the primary integration boundary. | - | ok: hdl/milan/milan_datapath.sv is the module docs/integration/INTEGRATION_GUIDE.md integrates |
| 16 | code | ```mermaid flowchart LR CPU[RV32I firmware] --> CSR[AXI4-Lite CSR] MEM[Entity memories] <--> DP[milan_datapath] CSR --> DP DP <--> MAC[Ethernet MAC] DP --> I... | - | ok: RV32I matches sw/litex/milan_soc.py:3706 ('cacheless RV32I M-mode Vexii core'); the interface groups are held by scripts/check_solution_docs.py (gate a015 rc 0) |
| 54 | item | Identify every clock source. | - | policy: integration step |
| 58 | item | Sequence reset release correctly. | - | policy: integration step |
| 60 | item | Never add direct cross-domain assignments. | - | policy: CONTRIBUTING CDC rule |
| 92 | item | Enable only the verified entity. | - | ok: milan_baremetal.c entity_advertise(aem_loaded) after load_aem_image (line 1889-1891) |
| 94 | item | gPTP remains independent from entity enablement. | - | ok: milan_baremetal.c nvm_boot comment 'PHC and fabric gPTP are live from reset, independent of the AEM gate' |
| 100 | sentence | Never tie response interfaces silently. | - | policy: integration step |
| 110 | item | Reset during active traffic. | - | policy: test step |
| 117 | code | ```sh make -C tb/verilator/milan_dp ``` | command 1 | ok: tb/verilator/milan_dp/Makefile exists (auto) |
| 123 | code | ```sh python3 sw/litex/test_pp_mem_bridge.py python3 sw/litex/test_pp_boot_bus_freeze.py ``` | command 2 | ok: both scripts exist and are in scripts/run_litex_sims.sh INVENTORY (lines 98-106) |
| 128 | sentence | The raw harness cannot prove SoC bridge wiring. | - | policy: evidence boundary |
| 130 | sentence | Run SoC evidence after every bridge change. | - | policy: evidence rule |
| 136 | code | ```sh python3 sw/litex/milan_sim.py --xlen 32 --non-interactive \ --output-dir build_milan_sim ``` | command 1 | ok: sw/litex/milan_sim.py defines --xlen, --non-interactive, --output-dir (auto) |
| 145 | code | ```sh cd build_milan_sim/gateware { sleep 4; printf 'mem_read 0x90000000 16\n'; sleep 5; } \ \| ./obj_dir/Vsim \| tee /tmp/milan-id.log grep -F '4e 4c 49 4d'... | - | ok: milan_csr.sv:1994 ID reset 0x4D49_4C4E ('MILN') read little-endian as 4e 4c 49 4d at MILAN_CSR_BASE 0x9000_0000 (sw/litex/milan_soc.py:99, sw/litex/milan_sim.py:7) |
| 154 | sentence | Then run the required complete gates. | - | policy: gate rule |
