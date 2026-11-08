[A720p] TAKEN
Branch: 640-charter-followup (PR #835, at d85da329 on dev 503bc97c; both round 5 reviews POSITIVE at that head; nothing pushed by this pass)
Authoritative references: the round 5 head d85da329 and its two POSITIVE reviews; origin/dev at 0a75aa77.
Interpreted scope: sync only. Merge origin/dev into the branch with a no-ff merge, no rebase. Resolve each conflict by keeping both sides' intent. Regenerate pages, digests and inventories the branch's files feed, through their generators only. No new content and no rewording beyond what a conflict or a generator forces.
Validation plan: every run step of .github/workflows/docs.yml on a clean clone of the merge head, each rc recorded; scripts/docs_inventory.py --check; check_doc_style on every page the merge touched; cd tests && behave; git diff --check against the merge base.
Blockers: none
