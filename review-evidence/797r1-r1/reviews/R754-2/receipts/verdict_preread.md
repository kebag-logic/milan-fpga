Written before any other reviewer's report at this head was read.

Verdict: NEGATIVE - exact head 96bfa8513978ebc8c2f2e73bd98914b56e84bf12

Findings at this point:
- F1 MINOR Conformance, Docs: MAC_STATUS "writes it only while the saved-state writer runs" is false on the merged firmware.
- F2 MINOR Conformance, RTL, Docs: PP_NVM_STAT[1:0] "stored and read back, drives nothing" is false, and the strobe side effects sit in the TAG row.
- F3 MINOR Conformance, Docs: ADP_CMD W1S rows say "stores and reads back"; the word reads 0.
- F4 MINOR Conformance, Docs: 23 of 71 read-table conditions flatten and/or grouping; one row reads as aaf_ctrl[0] on an absent stream, measured 0.
- F5 MINOR Conformance, Docs: design notes "[9] acts only while [8] is 0" is contradicted by the read mux, measured.

Ledger at this point: Conformance UNCLEAN, RTL UNCLEAN, Robustness CLEAN, Tests CLEAN, Docs UNCLEAN.
