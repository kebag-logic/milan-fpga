[R533] NEGATIVE - exact head a6e6916826448f81de2b779ca61a87a9f8c47278

Independent first-pass conclusion, recorded before consulting prior public review findings or any other reviewer report. The full local control mutation campaign is still running; this is an evidence checkpoint, not the final report.

R533-8-F1: MAJOR; Conformance, RTL, Tests, Docs.
The merge brings F3 into the base but does not deliver its SRP requests to the attached SRP adapter. Issue #665 assignment 6030279477, Part B.4, requires that port to be wired in `ctrl_app` when F3 is present. `ctrl_app.c:47` retains the supplied external environment; `ctrl_app_srp.c:7` only attaches loop handlers and opens reception. `acmp.c:161` sends the request to that external environment. No application bridge calls `srp_mbx_bind`. The changed `srp/README.md:257` instead assigns delivery and retries to target integration. The round-8 composition assignment does not explicitly waive Part B.4.

The independent mailbox probe accepts BIND_RX and PROBE_TX_RESPONSE, observes the correct ACMP SRP request, services 320 ms, and finds the attached SRP sink unbound. Direct delivery through `srp_mbx_bind` immediately binds it. Reproduced for IF=1 and for both interfaces at IF=2. See `binding_probe.py` and `receipts/binding-delivery.log`. Its wrapper returns zero only when the expected failure and direct-delivery positive control are both observed; the embedded required-behavior test fails.

Required outcome: complete the assigned serialized binding delivery, including refusal/retry and unbind handling, with an integration regression and discriminating plants; or obtain an explicit public scope decision before considering this acceptance item complete. The reviewer does not resolve the scope conflict by adopting the author's deferral.

The newly composed IRQ mask, SRP-only wake checks, timer ownership, module pass bounds and documentation arithmetic otherwise agree with the round-8 assignment. Both parents' named tests remain present. Mailbox RTL, generated contract and register-map artifacts equal dev. SRP adapter bytes equal the round-7 baseline. Local coverage passes the existing 100% ratchet over 22 files, the mailbox suite passes, and both linked-image profiles build with the checksum-verified pinned SDK. The four SRP fixture ELF hashes reproduce the public evidence.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #665 Part B.4 and round-8 assignment; app/ctrl_app.c; app/ctrl_app_srp.c; binding-delivery.log | R533-8 independent pass | a6e6916826448f81de2b779ca61a87a9f8c47278 |
| RTL | UNCLEAN | app/ctrl_app.c; acmp/acmp.c; app/ctrl_app_srp.c; merge-retention.log; mailbox.log | R533-8 independent pass | a6e6916826448f81de2b779ca61a87a9f8c47278 |
| Robustness | CLEAN | srp/srp_mbx.c; test/srp_rx_retry.cpp; test/srp_mbx.cpp; test/test_acmp_mbx.cpp; coverage.log | R533-8 independent pass | a6e6916826448f81de2b779ca61a87a9f8c47278 |
| Tests | UNCLEAN | test/test_acmp_mbx.cpp; test/srp_mutants.py; binding_probe.py; binding-delivery.log | R533-8 independent pass | a6e6916826448f81de2b779ca61a87a9f8c47278 |
| Docs | UNCLEAN | #665 Part B.4; srp/README.md:257; docs/design/MAILBOX_SPLIT.md:715; bound-table.log | R533-8 independent pass | a6e6916826448f81de2b779ca61a87a9f8c47278 |

Prior public findings and final running-campaign results remain to be reconciled into REPORT.md. No source fix or GitHub write was made.
