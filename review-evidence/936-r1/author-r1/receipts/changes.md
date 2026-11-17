# Changes at 73e30fb2

| File:line | Reason |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.h:88` | Remember the last published declaration, advertised type, VID and pending source bits. |
| `sw/firmware/ctrl/srp/srp_mbx.c:340` | Record a source when its published declaration, type or VID changes; preserve a refused swap until it succeeds. |
| `sw/firmware/ctrl/app/ctrl_app.h:101` | Carry source changes between the SRP and AECP deliveries. |
| `sw/firmware/ctrl/app/ctrl_app_srp.c:66` | Take and clear each interface's source changes. |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c:206` | Raise STREAM_OUTPUT GET_STREAM_INFO through the existing AECP event and pacing path. |
| `sw/firmware/ctrl/test/srp_talker.cpp:631` | Declare/withdraw, type swap including allocation refusal, VID and reset checks. |
| `sw/firmware/ctrl/test/srp_gate.hpp:348` | Probe-driven declaration and probe expiry exercise the composition bridge. |
| `sw/firmware/ctrl/test/test_aecp.cpp:754` | Check both recipients, the selected descriptor and one-shot delivery. |
| `sw/firmware/ctrl/test/srp_talker_mutants.py:18` | Eleven named SRP notice defects. |
| `sw/firmware/ctrl/test/aecp_mutants.py:530` | Four named AECP bridge defects. |
| `sw/firmware/ctrl/srp/README.md:244` | Document triggers, delivery, retries and tests. |
| `sw/firmware/ctrl/aecp/README.md:98` | Document the SRP source of output notices. |
| `sw/litex/ctrl_memory.py:246` | Ledger the fixture at 59.5 RAMB36 and platform object growth under the loose-BRAM decision. |
| `sw/litex/ctrl_memory_ledger.py:7` | Align exact object sizes and named exceptions with the images. |
| `sw/litex/test_ctrl_memory.py:21` | Update the named ledger expectations. |
| `docs/design/MARK_II_AREA_PLAN.md:1088` | Record the fixture's S14 debt. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:137` | Record image sizes, unchanged product banking and the raised S14 entry. |
| `tb/verilator/ctrl_service_budget/README.md:49` | Update the fixture ledger reference; approved CPU bounds unchanged. |
| `tb/verilator/milan_dp/Makefile:40` | Add the dropped-notice capture plant and update the plant count. |
| `tb/verilator/milan_dp/README.md:1382` | Document the removed missing-notice difference and separate destination-MAC defect. |
| `tb/verilator/milan_dp/twin_compare.py:74` | Replace the missing-notice row with exact payload comparison of the remaining destination-MAC defect. |
| `tb/verilator/milan_dp/twin_plants.py:13` | Drop an output notice as a new defect and retarget the vanished-difference plant. |
