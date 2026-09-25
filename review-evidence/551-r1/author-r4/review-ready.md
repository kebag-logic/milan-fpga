[A315] REVIEW READY

History split for PR #553 is complete locally.

Commit: `f219a5edaa191b33acc8b77abd22469f8f0db1f9`
Merge commit: `8dc98a429bd9918ad643fdb0051c2c9660395722` (parents `babb8925`, `864b36f5`).

The merge changes only the five conflict blocks; no additional build repair was needed. The following commit holds the remaining unwarmed-refusal requirement, admission control and documentation changes.

Validation: the merge's `make -C tb/verilator/milan_dp crflic CRFLIC_MDIR=obj_crflic_a315_merge VERILATOR_JOBS=4` passed 253 checks with zero failures. `git diff --check` passed for both merge parents and the content commit. The final em-dash gate against `864b36f5` passed with zero findings and 339/339 controls.

Acceptance: final tree `aca067d42122d785d8319d4d0926484dd9351568` equals `9eee4383^{tree}`; `git diff 9eee4383 HEAD` is empty. Submodule gitlinks and checkouts are unchanged. The two-commit split preserves all original content.

Open risks/questions for this assignment: none. Branch not pushed; no PR edits or merge into dev.
