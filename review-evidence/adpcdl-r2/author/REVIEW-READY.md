REVIEW READY ec727b64663b4eef2fc8da1ea5e0eae6541597d1

[A849] tsn-c-stack #37, PR #38, branch `adp-long-discover`, round 2: one commit on `e0b1449`, base main `69bac7c`, tree `00b9b9ee`. Not pushed, nothing posted. `src/` and `include/` are unchanged since `e0b1449`.

| Finding | Outcome |
|---|---|
| External F1 | the absent-surplus arm has its own 82-octet allocation; `ReadsNoOctetPastTheFrame` reads up to a protected page; plant `adp-long-control-length-reads-surplus` is caught by it, and address instrumentation reports the same read in the accept test |
| Internal F1 | every length 57 to 2047 with the surplus absent; four narrowed-mask plants; the reviewer's 15 mutants all caught, the control passes (5 narrowed reads and 2 gaps survived at `e0b1449`) |
| Internal F2 | issue-37 sentence in ADP input validation, change-log link; the generated tables are current |
| Internal F3 | RV32 smoke control with a length of 256 |
| Internal F4 | parent patch: 256 and 2047 with the surplus absent, plus a 0x00FF plant |
| External F2, internal F5 | no host path in this packet |

| Check | Result |
|---|---|
| Linux `validate.py --graphs` on a clean clone | rc 0, 28 of 28 steps |
| RV32 `baremetal.py` on the same clone | rc 0 |
| Plants | 489 of 489 caught |
| Coverage | 100 % lines and branches after the existing exclusions; `adp_rx` fully covered |
| dev-linux | trial merge tree = head tree |
| milan-fpga 5de21ff3 with this core and the patch | 13 arms pass; 10 of 10 selected plants caught; no test unnamed over the full table of 847 |

Not run: the rest of the parent firmware gate (AECP, SRP, lwSRP, platform, MAAP arms), the parent boundary gate, the em-dash gate on the parent patch (its renderer is not installed; a search of the patch finds none), hosted CI, any bench.
