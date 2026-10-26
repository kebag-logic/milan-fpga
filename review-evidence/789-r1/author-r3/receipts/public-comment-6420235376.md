url: https://github.com/kebag-logic/milan-fpga/issues/789#issuecomment-6420235376
created: 2026-10-26T15:40:44Z

[A682c] TAKEN
Branch: `789-yosys-tool-job`, round 3 on PR #794, adding commits on top of round-2 head `1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086` (dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`).
Authoritative references: #789 Decision and Acceptance; round-3 assignment issuecomment-6420212695; R707-2 (PR #794 issuecomment-6420207322); `AGENTS.md` sections 6 and 7.
Interpreted scope: fix R707-2-01 at its cause. A named judge must hold `rtl-fast`'s emitted `yosys-elaboration` and `yosys-tool` jobs after every transform stage, the key-binding stage included, so that a post-derivation stage which removes, adds, reorders or rewrites a step of either job fails by name. Add a plant in the key-binding stage that drops one self-test, which must fail a named judge. Correct `docs/testing/CI_WORKFLOWS.md` item 4 and the PR body to say exactly which list each judge holds. State a choice on the optional S1 and S2. Push after the privacy check and confirm the hosted `rtl-fast` stays green at the new head.
Validation plan: `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py` (the fast-tool controls), the rest of the "CI scheduling and evidence controls" list, `ci_events.py --check` and `--selftest`, `act_ci.py --selftest` and the runner contract gate (offline only), `check_py_idiom.py`, and the docs gates under the pinned Markdown renderer; a generator-mutant replay with the new key-binding-stage plant; hosted `rtl-fast` at the new head.
Blockers: none

