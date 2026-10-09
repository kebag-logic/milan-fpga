[A572] REVIEW READY — round 2

Head: `0ded1f269a44d107498f177c8276665656e07d30` on `665-f5-aecp`, new commits on `1e68d1b62ef2facdf0e8dbad28a202297d433c61`. Unpushed; PR #700 remains at the round 1 head.

Changed: root READ_DESCRIPTOR configuration handling; current SET_STREAM_INFO response fields and command flags; independent timed notification retries; cross-instance guards for all 15 public inputs; typed non-AEM refusals including the clause-correct HDCP response; and ENTITY available_index observed from the composed ADP owner. The README records the message-type decisions and remaining wire differences by clause.

Validation, all rc 0:
- Firmware bank with `--require-rv32 --jobs 4`: 59 named arms, 65 tallies, 1406 checks, zero failures.
- All 12 unchanged review probes pass. Both sanitizer arms pass 69 tests. All 69 source plants are caught by their named assertions.
- `fw_coverage.py --write` followed by `--check`: 30 files pass; all eight AECP/application units have raw 100% line and branch coverage, with no new exclusion. Coverage, tally and RV32 grader self-tests pass.
- Fresh wire differential: 132 observations at one interface and 137 on each two-interface ingress; six oracle controls per ingress pass.
- Default mailbox target and all five quick plants pass; `gen_mailbox.py --check` passes.
- Complete builder bank: four ordinary and four profile partitions pass, with the exact fixture-table union verified. All 73 documentation commands and final style checks pass.
- Re-linked shipping one/two-interface spans: 140400 / 153056 bytes. Largest shape: 194224 / 221728 bytes, including the 8192-byte stack reservation. All remain below 224 KB.

HANDOFF.md and PR-BODY.md are updated with Round 2. The packet includes every changed file:line, all 73 test-to-defect mappings, coverage/gate/size tables, exact reproduction commands and artifact hashes. The worktree is clean; generated artifacts are in scratch. No default-build, shipping-image, RTL or register-map change; no push, PR mutation, merge or hardware operation.

The assigned corrections are implemented. Independent re-review, publication checks, routed memory fit and physical calibration remain owed. No review verdict or merge approval is claimed.
