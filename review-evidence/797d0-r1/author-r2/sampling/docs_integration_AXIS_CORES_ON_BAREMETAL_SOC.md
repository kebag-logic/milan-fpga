# Sampling ledger: docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 3 | sentence | This page defines the packet-stream boundary used by the supported LiteX integration. | - | ok: scope sentence; sw/litex/milan_soc.py is the supported integration |
| 15 | sentence | `milan_datapath` receives and emits 64-bit MAC streams. | - | F: D0-034 (third sentence); first two ok: hdl/milan/milan_datapath.sv:65 TDATA_WIDTH = 64, byte order and tkeep rule held by tb/verilator/milan_dp |
| 15 | sentence | Byte lane zero carries the first wire byte; `tkeep` is contiguous on the final beat; `tlast` closes a packet; and backpressure is honored at every registered... | - | F: D0-034 (third sentence); first two ok: hdl/milan/milan_datapath.sv:65 TDATA_WIDTH = 64, byte order and tkeep rule held by tb/verilator/milan_dp |
| 15 | sentence | The MAC adapter may cross clock domains only with a complete-packet asynchronous FIFO. | - | F: D0-034 (third sentence); first two ok: hdl/milan/milan_datapath.sv:65 TDATA_WIDTH = 64, byte order and tkeep rule held by tb/verilator/milan_dp |
| 20 | sentence | The current shipping placement keeps control traffic in fabric. | - | F: D0-033 (third sentence); the rest ok: sw/litex/milan_soc.py:2621 default all-fabric, ARCHITECTURE_HW_SW_SPLIT.md:6-8 acceptance, milan_datapath.sv:654-664 no general-data chain |
| 20 | sentence | Mark II passes selected control frames through filtered packet mailboxes. | - | F: D0-033 (third sentence); the rest ok: sw/litex/milan_soc.py:2621 default all-fabric, ARCHITECTURE_HW_SW_SPLIT.md:6-8 acceptance, milan_datapath.sv:654-664 no general-data chain |
| 20 | sentence | Its default is bare-metal control; all-fabric remains supported. | - | F: D0-033 (third sentence); the rest ok: sw/litex/milan_soc.py:2621 default all-fabric, ARCHITECTURE_HW_SW_SPLIT.md:6-8 acceptance, milan_datapath.sv:654-664 no general-data chain |
| 20 | sentence | All-fabric stays the shipping default until F2 to F5 acceptance. | - | F: D0-033 (third sentence); the rest ok: sw/litex/milan_soc.py:2621 default all-fabric, ARCHITECTURE_HW_SW_SPLIT.md:6-8 acceptance, milan_datapath.sv:654-664 no general-data chain |
| 20 | sentence | That acceptance covers all streams, counters and the audio soak. | - | F: D0-033 (third sentence); the rest ok: sw/litex/milan_soc.py:2621 default all-fabric, ARCHITECTURE_HW_SW_SPLIT.md:6-8 acceptance, milan_datapath.sv:654-664 no general-data chain |
| 20 | sentence | The generic classifier/queue/CBS input remains inactive in today's shipping boundary. | - | F: D0-033 (third sentence); the rest ok: sw/litex/milan_soc.py:2621 default all-fabric, ARCHITECTURE_HW_SW_SPLIT.md:6-8 acceptance, milan_datapath.sv:654-664 no general-data chain |
| 32 | sentence | Interrupt status remains available in the CSR block. | path 1 | ok: hdl/common/csr/milan_csr.sv A_IRQ_STATUS 0x010; the FR_NFR.md anchor is held by the anchor gate |
| 32 | sentence | [NFR-SCOUT-03](../reference/FR_NFR.md#341-control-service-budget-and-normative-timing) defines that obligation. | path 1 | ok: hdl/common/csr/milan_csr.sv A_IRQ_STATUS 0x010; the FR_NFR.md anchor is held by the anchor gate |
| 40 | sentence | The protocol processor has a read-only memory request/response interface for the AEM image. | - | ok: milan_baremetal.c load_aem_image (1836-1866) then entity_advertise (1827-1833); KL_pp_shadow descriptor memory face is read-only |
| 40 | sentence | Firmware validates the generated raw image, copies it to the reserved window, and only then enables the entity. | - | ok: milan_baremetal.c load_aem_image (1836-1866) then entity_advertise (1827-1833); KL_pp_shadow descriptor memory face is read-only |
| 40 | sentence | This is a descriptor store, not a packet path. | - | ok: milan_baremetal.c load_aem_image (1836-1866) then entity_advertise (1827-1833); KL_pp_shadow descriptor memory face is read-only |
| 47 | sentence | Physical acceptance additionally requires UART grading and an external packet capture. | - | policy: evidence rule |
