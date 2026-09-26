[A325] TAKEN
Branch: `567-pp-pin-0922e434` from `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
Executor: [A325]. Reviewers: [R326] internal and [R327] external.
Authoritative references: #567 acceptance, assignment comment, `CONTRIBUTING.md`, `docs/reference/SUBMODULES.md`.
Interpreted scope: adopt processor `0922e43408f891fc0b84a84691df86b4fd0f1c0d`, refresh the parent pin documentation and generated diagram, and run the assigned parent gates plus the new processor parameter inventory gate. No parent RTL or donor edits.
Validation plan: the assigned processor-shadow, builder (SDK and no-compiler), NVM, documentation, source-list, language, lint, traceability and behavior gates; compare processor HDL and ROM inputs across the pin range; check the parent parameter bindings.
Decision needed: acceptance 2 permits digest re-recording only when processor ROM sources change. `git diff --stat 990f9652 0922e434 -- hdl/` is empty, including both ROM generators and their inputs. However, `syn/yosys/ooc.sh:464-470` requires rows for the exact new gitlink, absent from the existing ledger. Following acceptance 2 leaves that separate OOC path unable to accept the new pin. The ledger remains unchanged pending a public decision; the other scoped work proceeds.
