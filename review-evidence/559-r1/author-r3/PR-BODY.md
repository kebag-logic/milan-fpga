[A314]

Closes #559

Status: ready for independent review of round 3.

Description: measure the complete saved-state capture on the product CPU and memory buses. Across both traffic arms, with 16 captures each at the contract's aligned 50 MHz clock, the worst 8x8 result is 24.30454 ms. This gives 2.0161x margin against the guaranteed 49 ms floor of the unchanged nominal 50 ms hold. The 1x1 maximum is 6.60642 ms. The hold remains sufficient only while the measured copy and clocks remain unchanged.

How to reproduce: use the full measurement matrix linked from [snapshot ownership section 18](docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md#18-cost). The linked receipt contains all 96 captures, input hashes and the labelled 100 MHz comparison. Every capture checks the complete closed-record copy, attestation, ownership and its traffic condition.

How to validate: all requested round 2 local gate commands returned zero, including both builder modes, the backend and firmware suites, both documentation inventory modes and the new capture-input gate. Named changes to bytes, records, clocks and OFF timing are detected. The compiler-absent run intentionally skips its compiled census; both builder modes lack the historical placement-calibration report.

DoD: the runnable harness, conditional hold remedy, section 18 and UNRESOLVED 6 are updated. Physical timing and memory ordering remain open. Independent re-review and exact-head hosted acceptance remain to be completed.

## Round 2

- Both shapes use explicit 50 MHz clock overrides and aligned rising edges. Configuration reconciliation remains in #565.
- Traffic ON and OFF each receive 16 captures and identical timing grading. The 8x8 100 MHz maximum is 19.79024 ms, labelled non-contract. Section 18 quantifies the small observed traffic effects.
- The hosted input gate regenerates closed-record bytes and records, checks clocks and source identity, and refuses stale measurements. A planted grader that ignores OFF timing fails its control.
- Test indexes name the manual measurement, its prerequisites and Makefile exception. The harness instructions identify all substituted devices and clock phases.
- Both reviewers' 50 MHz probe figures were reproduced cycle-for-cycle. The stop condition was not triggered; product firmware and hold settings remain unchanged.

## Round 3

- Pin the capture measurement gate's name, position 28, command and exact step keys. The recorded job count is now 50, with existing position and count controls updated.
- Preserve every earlier mutation control. Add removal, reordering, renaming and conditional-execution controls. Existing script and missing-record controls also protect the new step; all nine focused mutations are rejected.
- Document the gate's ordering, checks and contract protection. Round 2 measurements, capture logic and workflow contents remain unchanged.
- All requested round 3 local gates pass. The workflow contract covers 1,655 items and its self-test passes 2,197 arms. The runner's offline contract check, capture gate, both documentation inventory modes, and requested documentation, idiom and whitespace gates pass. All four explicit capture mutations fail as expected.

Independent re-review and exact-head hosted acceptance remain pending.
