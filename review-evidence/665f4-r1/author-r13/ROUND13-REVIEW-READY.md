[A560] REVIEW READY

Head: `154722e14781c7373f3229420b6e007f9bcf9835`.

Round 13 adds the three Failed-kind intra-PDU mailbox/composition cases for R532-12-F1 and exact q04/q13/q06-equivalent plants. Each plant is caught by its named observable at IF=1 and IF=2, including both standing campaign passes. The original three reviewer probes pass at both counts. R533-12-R1's stale lwSRP citation is corrected.

Required validation passes, all 86 final command records rc 0: complete ctrl campaign (471 control plants, 169 SRP at IF=2, 68 at IF=1, both pin-refusal controls); composition 52 cases per count; AddressSanitizer 140 tests per count; unchanged 22-file coverage ratchet at 100%; documentation and contract gates.

Only two test files and the pin citation change. The optional R532-12-S1 production guard remains unimplemented in this tests-only delta. Firmware, dependency pins, RTL, registers and shipping inputs are unchanged.

HANDOFF.md and PR-BODY.md retain earlier rounds and add Round 13, with file:line changes, test-to-plant mappings, coverage and gate tables. The packet records reproducible commands, hashes, and the two corrected development attempts. Worktree clean; all jobs complete. Independent corrected-head review and manager publication/acceptance remain required.
