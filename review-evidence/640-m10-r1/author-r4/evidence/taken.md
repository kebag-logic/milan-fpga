[A720n] TAKEN
Branch: 640-charter-followup (PR #835, at d52e966b on dev 503bc97c; round 4; nothing pushed by this pass)
Authoritative references: R765-3 (PR #835 issuecomment-6580969269), NEGATIVE on one MINOR, R765-3-F1; R766-3 POSITIVE (issuecomment-6580971431); M8a-1 (docs/design/MARK_II_AREA_PLAN.md Block RAM ledger, AREA_BUDGET.md:301); owner stage list (issuecomment-6545999204).
Interpreted scope: docs only, docs/design/MARK_II_AREA_PLAN.md. R765-3-F1's required outcome: stage 1's "Removes" cell no longer credits stage 1 with the BIOS ROM and SRAM or their 18 RAMB36; it may say they left at the switch-over (M8a-1). The owner's "Change" wording stays, and the note names that cell as the one keeping the owner's words. The whole stage table and every per-stage RAMB36 or LUT credit are re-read for the same double booking; any found is fixed the same way and listed. One commit; nothing else changes.
Validation plan: every run step of .github/workflows/docs.yml on a clean clone of the committed head, each rc recorded; check_doc_style on every touched page; git diff --check against 503bc97c; the reviewer's census_coverage.py.
Blockers: none
