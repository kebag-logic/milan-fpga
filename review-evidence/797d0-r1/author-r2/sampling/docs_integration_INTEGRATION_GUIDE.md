# Sampling ledger: docs/integration/INTEGRATION_GUIDE.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 3 | sentence | This contract describes the current all-fabric shipping control plane. | - | ok: sw/litex/milan_soc.py:2621 all-fabric default |
| 10 | item | RTL remains the final interface authority. | - | policy: authority rule |
| 11 | item | The documentation gate classifies every wrapper port. | - | ok: scripts/check_solution_docs.py and scripts/check_port_contracts.py classify the wrapper ports (gates a015, a045 rc 0) |
| 27 | code | ```mermaid flowchart LR CONTROL[External control] --> CSR[AXI4-Lite CSR] DP <--> MAC[Ethernet MAC] DP <--> DESC[Descriptor memory] DP <--> RESP[Response memo... | - | ok: the faces exist as milan_datapath ports (i_desc_mem_*, i_resp_mem_*, MMCM DRP servo MCSRV) |
| 40 | item | Optional parameters change live interface behavior. | - | policy |
| 41 | item | Every compiled feature needs truthful external wiring. | - | policy |
| 58 | sentence | GET_STREAM_INFO has two owners (#508). | issue 1 | ok: #508 CLOSED, the change that split GET_STREAM_INFO between the processor and milan_datapath |
| 64 | item | `milan_datapath` answers every other word and every validity flag. | - | ok: as line 58 (lines 60-63 name the processor's four fields) |
| 65 | item | Never add a second source for the processor's four fields. | - | policy |
| 87 | item | These rows cover every declared wrapper port. | - | ok: scripts/check_port_contracts.py classifies every declared port |
| 88 | item | The checker rejects unclassified future ports. | - | ok: same gate refuses an unclassified port |
| 90 | item | They do not provide working media protocols. | - | ok: optional faces tied off give no media protocol |
| 96 | row | \| Descriptor \| One request; ordered 64-bit beats; final `rsp_last` \| Propagate `i_desc_mem_rsp_err` \| | - | ok: hdl/milan/milan_datapath.sv:380 i_desc_mem_rsp_err |
| 98 | row | \| Response write \| One aligned beat; honor every byte strobe \| Pulse `wr_done`; propagate `wr_err` \| | - | ok: milan_datapath.sv:399-424 zero-strobe bytes unmodified, i_resp_mem_wr_done, i_resp_mem_wr_err |
| 103 | item | Propagate every memory error. | - | policy |
| 104 | item | Never fabricate completion pulses. | - | policy |
| 113 | row | \| `axis_resetn` \| Synchronous, active-low axis reset \| | - | ok: milan_datapath.sv:471 axis_resetn |
| 119 | item | Shipping deployment selects 50 MHz for `axis_clk`. | - | ok: configs/endstation_ax7101_1x1_tdm8.yaml:44 milan_clk_hz 50000000 |
| 120 | item | The PHC therefore also runs at 50 MHz. | - | ok: the PHC counts on axis_clk (ptp_csr_sync/timestamp_counter in milan_datapath) |
| 121 | item | `gtx_clk` does not mean the PHY's 125 MHz clock. | - | ok: sw/builder/test_builder.py:18199 gate 1d ties gtx_clk to axis_clk |
| 124 | item | Never infer one clock from another. | - | policy |
| 126 | item | Use only approved crossing structures. | - | policy: CONTRIBUTING CDC rule |
| 128 | sentence | It distinguishes physical sources, reset aliases, and timestamp boundaries. | - | ok: scripts/check_port_contracts.py clock classes |
| 137 | code | ```mermaid sequenceDiagram participant Host participant CSR participant Memory participant Entity Host->>CSR: Assert resets Host->>CSR: Release required rese... | - | ok: same sequence as milan_baremetal.c milan_init/load_aem_image/nvm_boot/entity_advertise |
| 155 | item | Apply every inactive start from the inventory. | - | policy |
| 156 | item | Release resets only with stable clocks. | - | policy |
| 159 | item | Load and verify descriptor memory before `PP_CTRL[1]`; a restore started without it cannot prove the image and ends CLOSED. | - | ok: milan_baremetal.c:1880-1891 loads and CRC-checks the AEM before nvm_boot(); REGISTER_MAP 0x920 PP_CTRL[1] restore_go |
| 162 | item | Start the restore walk with `PP_CTRL[1]` on every boot. | - | ok: milan_baremetal.c:1886 'nvm_boot() starts the walk on every path' |
| 163 | item | The ACMP listener answers nothing until that walk ends. | - | ok: milan_baremetal.c nvm_boot comment: the processor holds its ACMP listener and AECP until the walk reaches its terminal |
| 164 | item | AECP answers nothing until the D3 walk ends. | - | ok: same |
| 165 | item | `PP_STAT[2]` reports the end, and `PP_STAT[16]` a CLOSED one. | - | ok: REGISTER_MAP.md 0x924 PP_STAT [2] restore_done (never after CLOSED), [16] restore_closed |
| 166 | item | A silent device ends each wait at 20 ms. | - | ok: protocol-processor docs/architecture/01_overview.md:186 P-NVM-RS-TMO-CYC 20 ms per wait |
| 167 | item | The whole restore is bounded at 1,000 ms. | - | ok: protocol-processor docs/architecture/01_overview.md:187 P-NVM-RS-AGG-CYC 1,000 ms |
| 168 | item | Enable only fully wired protocol features. | - | policy |
| 173 | item | Initialize every pinned submodule. | - | policy |
| 188 | item | Reset during active traffic. | - | policy |
| 189 | item | Stall every memory request channel. | - | policy |
| 190 | item | Inject every memory error input. | - | policy |
| 194 | code | ```sh make -C tb/verilator/milan_dp python3 sw/litex/test_pp_mem_bridge.py python3 sw/litex/test_pp_boot_bus_freeze.py ``` | command 3 | ok: tb/verilator/milan_dp/Makefile and both LiteX tests exist (auto) |
