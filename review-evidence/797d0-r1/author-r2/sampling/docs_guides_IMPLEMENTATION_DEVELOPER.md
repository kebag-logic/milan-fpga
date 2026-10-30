# Sampling ledger: docs/guides/IMPLEMENTATION_DEVELOPER.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 26 | item | Open every linked requirement. | - | policy |
| 60 | item | Reset every state register appropriately. | - | policy |
| 62 | item | Test reset during active traffic. | - | policy |
| 64 | item | Never weaken an oracle. | - | policy: AGENTS.md section 8 |
| 68 | sentence | Then run every required repository gate. | - | policy |
| 74 | sentence | Always confirm module-specific behavior. | - | policy |
| 81 | item | Every payload sideband stays stable during backpressure. | - | ok: AXI-Stream rule; docs/diagrams/wd_axis_backpressure.json shows tdata/tkeep held while tready low |
| 82 | item | Last only qualifies an accepted beat. | - | ok: same diagram, tlast sampled on the accepted beat |
| 88 | item | Source data remains stable during transfer. | - | ok: docs/diagrams/wd_cdc_handshake.json holds src_in through req_tog/ack (cdc_handshake.sv data_hold) |
| 91 | item | Both resets belong to separate clock domains. | - | ok: same diagram carries one reset per domain |
| 92 | item | Shown latency uses default synchronizer parameters. | - | ok: hdl/common/cdc_handshake.sv:24-25 DEST_SYNC_FF = SRC_SYNC_FF = 2, synchroniser vectors [2:0]; docs/diagrams/wd_cdc_handshake.json draws ack_sync[0..2] and req_sync[0..2] |
| 110 | sentence | Finish with required repository gates. | - | policy |
