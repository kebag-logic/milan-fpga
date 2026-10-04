R463-3 own pass, written before any prior review report or finding text was read.
Exact head c725be12d7ea6bf96f1b64e3a56416f0d4defd6c, tree 0bb7199a3caf38df44071cac4e2d56fef89f1b7c.

Provisional verdict: POSITIVE (pending the notify campaign and the two AECP TD arms still running).

Own findings:
- S1 SUGGESTION (Tests, Robustness): section AQ's drive gives each arm a serial number as
  its deadline. The serial stays below 2^20, so deadline bits 20 to 31 never toggle through
  the rings in AQ2 or AQ3. Probes that never store deadline bit 21, 22 or 31 in the ring
  pass AQ (4 of 4). Probes on bit 0 and on the cancel bit fail AQ2 and AQ3. The RTL
  stores the whole word, and lint catches a narrowed ring, so this is not a defect at the
  head. Suggested outcome: draw the deadline's high bits at random and keep the serial in
  the low bits.

Provisional ledger:
| lens | state |
|---|---|
| Conformance | CLEAN |
| RTL | CLEAN |
| Robustness | CLEAN |
| Tests | CLEAN (S1 is a SUGGESTION) |
| Docs | CLEAN |
