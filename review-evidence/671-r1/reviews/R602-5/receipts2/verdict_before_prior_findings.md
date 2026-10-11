[R602] NEGATIVE - exact head 0c276b621d638c9a83e82f71fbf07bc153517bf7
Written after the independent pass and before reading any prior review finding on PR #715.

R602-5-F1 MAJOR Tests - sw/firmware/nvm_hosttest/read_fault_cases.py:153-169 (GROUPS, FLIPS, SEALED), :30-60 (READ_FAULT_MUTATIONS); firmware sw/firmware/milan_baremetal/milan_baremetal.c:768-780 -
the refused-read comparison's trailer half (a.tail == b.tail) and the last prefix bytes are reached by no standing case; a one-line plant that drops the tail compare restores #671's loss (53 / 163 saved records lost on 1x1 / 8x8) and the standing check 13 + 14 report 0 findings on all three control shapes.

Ledger (before prior findings):
| lens | state | covering round | head |
| Conformance | CLEAN | R602-5 | 0c276b62 |
| RTL | CLEAN | R602-5 | 0c276b62 |
| Robustness | CLEAN | R602-5 | 0c276b62 |
| Tests | UNCLEAN (F1) | R602-5 | 0c276b62 |
| Docs | CLEAN | R602-5 | 0c276b62 |
