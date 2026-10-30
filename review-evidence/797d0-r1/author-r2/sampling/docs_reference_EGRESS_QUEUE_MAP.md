# Sampling ledger: docs/reference/EGRESS_QUEUE_MAP.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 3 | sentence | The classifier, queue bank, and 802.1Qav credit logic remain implemented and independently verified, but the bare-metal product boundary supplies no packet s... | path 1 | ok: hdl/milan/milan_datapath.sv:654-664 no general-data TX chain; milan_csr.sv:1996-2000 CAP.CBS 0 |
| 3 | sentence | The CSR words below are write-only scratch and `CAP.CBS` reads 0 ([REGISTER_MAP.md](REGISTER_MAP.md)); the blocks are building material for a class-A shaping... | path 1 | ok: hdl/milan/milan_datapath.sv:654-664 no general-data TX chain; milan_csr.sv:1996-2000 CAP.CBS 0 |
| 33 | sentence | The five-queue CSR geometry remains stable: | - | ok: NUM_QUEUES 5 (milan_csr.sv CAP reset 4'(NUM_QUEUES)); ethernet_packet_pkg.sv:217-223 five classes |
| 37 | row | \| q4 \| class A \| disabled until a valid admitted slope is supplied \| | - | ok: ethernet_packet_pkg.sv:222 SRA_CLASS q4 |
| 38 | row | \| q3 \| gPTP classification target \| disabled \| | - | F: D0-028 |
| 39 | row | \| q2 \| class B \| disabled until configured \| | - | F: D0-028 (the swapped pair) |
| 40 | row | \| q1 \| control \| disabled \| | - | ok: ethernet_packet_pkg.sv:219 CONTROL_CLASS q1 |
| 41 | row | \| q0 \| best effort/default \| disabled \| | - | ok: ethernet_packet_pkg.sv:218 BEST_EFFORT q0 |
| 43 | sentence | Queue indices outside the elaborated count clamp to q0. | - | ok: hdl/ieee8021q/ts/traffic_class_map.sv:222-225 clamps a queue index >= NUMBER_OF_QUEUES to BEST_EFFORT; the focused suites exist (tb/verilator/classifier, queues, cbs) |
| 43 | sentence | The focused classifier, queue, and CBS suites are the authority for this retained generic logic. | - | ok: hdl/ieee8021q/ts/traffic_class_map.sv:222-225 clamps a queue index >= NUMBER_OF_QUEUES to BEST_EFFORT; the focused suites exist (tb/verilator/classifier, queues, cbs) |
| 55 | row | \| q4 SR class A \| 450 Mb/s \| 45 % \| 684 \| −837 \| | - | ok: ethernet_packet_pkg.sv:276-282 450 Mb/s; hiCredit 1522*0.45 = 684, loCredit 1522*(-0.55) = -837 (calc_hi/lo_credit, lines 301-318) |
| 56 | row | \| q3 SR class B \| 150 Mb/s \| 15 % \| 228 \| −1293 \| | - | ok: same, 150 Mb/s, 228, -1293 |
| 57 | row | \| q2 gPTP \| 50 Mb/s \| 5 % \| 76 \| −1445 \| | - | ok: same, 50 Mb/s, 76, -1445 |
| 58 | row | \| q1 control \| 50 Mb/s \| 5 % \| 76 \| −1445 \| | - | ok: same, 50 Mb/s, 76, -1445 |
| 59 | row | \| q0 best effort \| 25 Mb/s \| 2.5 % \| 38 \| −1483 \| | - | ok: same, 25 Mb/s, 38, -1483 |
| 61 | sentence | The sum is 725 Mb/s (72.5% of the port), below the 75% ceiling. | - | ok: 450+150+50+50+25 = 725 Mb/s = 72.5 %, under the 75 % ceiling (ethernet_packet_pkg.sv:287-288) |
| 61 | sentence | Every queue still powers up unshaped. | - | ok: 450+150+50+50+25 = 725 Mb/s = 72.5 %, under the 75 % ceiling (ethernet_packet_pkg.sv:287-288) |
| 66 | sentence | None of it is instantiated in the shipping datapath (see the top of this page), so no shaper consumes a slope or an admission verdict on the wire. | - | ok: historical (#530 CLOSED) and the not-instantiated statement as line 3 |
| 66 | sentence | While the stream gate was the raw admission verdict, until #530, opening a source and accounting its slope occurred on the same admission-round edge. | - | ok: historical (#530 CLOSED) and the not-instantiated statement as line 3 |
| 66 | sentence | Teardown closed the source first and could retain its slope until the next round, which is conservative: no stream could transmit against an unbudgeted slope. | - | ok: historical (#530 CLOSED) and the not-instantiated statement as line 3 |
| 77 | sentence | The shipping licence now requires ACTIVE and the real grant (#551). | issue 1 | ok: #551 CLOSED; REGISTER_MAP 0x750 [6] ACTIVE AND real grant |
| 84 | item | **Admitted.** The licence opens when both terms hold. Normal Listener Ready arrivals follow admission, adding no delay. An earlier arrival waits for the real... | - | ok: licence rule of #551 (REGISTER_MAP 0x750 [6]/[7]) |
| 87 | item | **Refused, including changed TSpecs.** ACTIVE can pulse; licences stay closed. No STREAM_START/STREAM_STOP pair or Table 5.4 counter reset follows. No PDU le... | - | ok: same rule |
| 92 | sentence | Every declaration clears its source's grant until that evaluation completes. | issue 2 | ok: processor #112 adopted through #508 (CLOSED) |
| 92 | sentence | A round that meets any pending declaration publishes nothing. | issue 2 | ok: processor #112 adopted through #508 (CLOSED) |
| 92 | sentence | This follows [processor #112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112), adopted through #508. | issue 2 | ok: processor #112 adopted through #508 (CLOSED) |
| 98 | sentence | `CRFT_CTRL[6]`/`[7]` and source 0's `LWSRP_STATUS[8]` require the grant. | - | ok: REGISTER_MAP 0x750 [6]/[7] and 0x694 [6] OR of raw ACTIVE, [8] stream gate |
| 98 | sentence | `LWSRP_STATUS[6]` remains the OR of raw ACTIVE across sources. | - | ok: REGISTER_MAP 0x750 [6]/[7] and 0x694 [6] OR of raw ACTIVE, [8] stream gate |
| 98 | sentence | It can therefore rise while every licence stays closed. | - | ok: REGISTER_MAP 0x750 [6]/[7] and 0x694 [6] OR of raw ACTIVE, [8] stream gate |
| 104 | sentence | No shaper consumes `LWSRP_SLOPE`; it remains diagnostic. | - | ok: milan_datapath.sv:8552-8558 |
| 104 | sentence | A future shaping implementation must prove its own slope/gate ordering. | - | ok: milan_datapath.sv:8552-8558 |
| 109 | sentence | Fabric gPTP has its own timer-driven transmit source and merges directly onto the control lane; there is no classifier/shaper chain in the shipped trunk for ... | - | ok: milan_datapath.sv:8812-8818 timer-driven gPTP source, RX tap stamp, TX launch since #360 |
| 109 | sentence | It therefore cannot be delayed by queue occupancy or firmware service. | - | ok: milan_datapath.sv:8812-8818 timer-driven gPTP source, RX tap stamp, TX launch since #360 |
| 109 | sentence | The RX event timestamp is captured off the RX tap; the TX one is not captured at this boundary at all - since #360 it is the frame's observed LAUNCH, reporte... | - | ok: milan_datapath.sv:8812-8818 timer-driven gPTP source, RX tap stamp, TX launch since #360 |
| 109 | sentence | The rule this section is named for - gPTP must never queue behind a shaped class - is what any future class-A shaping lane over the fabric's own sources has ... | - | ok: milan_datapath.sv:8812-8818 timer-driven gPTP source, RX tap stamp, TX launch since #360 |
| 119 | sentence | The `0x88F7` classifier rule remains a tested generic mapping but is not the release gPTP path. | - | ok: the classifier keeps the 0x88F7 rule; not instantiated (line 3) |
| 131 | sentence | No ingress queue is exposed to target software. | - | ok: no ingress queue CSR in milan_csr.sv |
| 137 | sentence | A CSR reset map is not evidence that a release packet traverses these queues: none does, and none can - the chain is not in the shipped datapath. | - | ok: as line 3 |
