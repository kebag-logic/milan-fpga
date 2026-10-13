[A612] REVIEW READY - F3b round 3

Commit: `532ab871272597d83fa08506bcb05298fbe87806` (one new local commit after `651ccb5a`; no push).

Changed: registered `docs/design/MAILBOX_SPLIT.md` and its reader in the CI classifier, added the removal-sensitive classification case, and updated the policy inventory. Documented receive/link snapshot freshness for R582-2-S1. Corrected R582-2-R1 in the prepared PR body.

Validation: `python3 scripts/ci_scope.py --selftest` passes all 109 checks; direct page classification is `true`. Whole-branch inventory: 330 gated files, 185 documentation candidates, eight registered/relevant pages, none missing or stale. `python3 scripts/ci_events.py --check` and `--selftest` pass (2169 contract items, 3064 arms). Compiled service bounds pass 47 checks including all 38 planted controls. Source-list, evidence-reader, documentation, Python, contents, hygiene and added-line checks and controls pass. CPython 3.12.3 used.

Acceptance: round 3's local-validation items are met. Firmware, generated files, campaign inputs and dependency pins are unchanged. All 30 retained ELF sizes/hashes match round 2. Final raw-blob/mode audit passes for 1311 parent and 1043 dependency files; checkout is clean. HANDOFF.md, PR-BODY.md and round3 receipts are updated in the assigned evidence packet.

Remaining: manager push and workflow replica, then successful exact-head hosted `changes`, `firmware-boundary`, `firmware-verilator`, `rtl-fast`, `verilator-suites` and `yosys-portability`; independent re-review and the remaining merge bar. No corrected-head hosted or review verdict is claimed.
