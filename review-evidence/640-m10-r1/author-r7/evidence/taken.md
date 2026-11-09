[A720q] TAKEN
Branch: 640-charter-followup (PR #835, at 72816d26 on dev 0a75aa77; both round 6 reviews POSITIVE at that head; nothing pushed by this pass)
Authoritative references: the round 6 head 72816d26 and its two POSITIVE reviews; origin/dev at ac0a01e3 (PR #852, #851).
Interpreted scope: sync only. Merge origin/dev into the branch with a no-ff merge, no rebase. Keep both sides' rows in docs/findings/README.md. Check every area figure the branch's pages cite against dev's after the merge; correct only one the merge made stale. Regenerate through generators only. Nothing else.
Validation plan: every run step of .github/workflows/docs.yml on a clean clone of the merge head, each rc recorded; scripts/docs_inventory.py --check; check_doc_style on every page the merge touched; cd tests && behave; git diff --check against the merge base.
Blockers: none
