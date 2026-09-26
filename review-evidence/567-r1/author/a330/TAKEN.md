[A330] TAKEN
Branch: `567-pp-pin-0922e434`; starting head `1912c0472635ea174f1a2e2de2f3c96d09f55e9b`.
Executor: [A330]. Independent reviewers remain [R326] internal and [R327] external.
Authoritative references: #567 and the [Round 2 decision](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845149786), `CONTRIBUTING.md`, `AGENTS.md`, `syn/yosys/ooc.sh`.
Interpreted scope: re-record the exact-pin ROM ledger using `./ooc.sh --record-rom-digests`, compare both new processor digests with the previous pin, and stop on any mismatch. The assigned Round 2 repository delta is the ledger only.
Validation plan: the normal OOC path for `KL_pp_shadow`; the three-top elaboration command from `rtl-fast.yml`; documentation checks in Git and metadata-free filesystem modes; em-dash check against `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`; whitespace checks.
Blockers: none for the assigned ledger work. The Round 1 statements in `CHANGELOG.md` and `docs/reference/SUBMODULES.md` describing an unchanged ledger and an unresolved decision are superseded by the linked decision; they remain outside this explicitly ledger-only round.
