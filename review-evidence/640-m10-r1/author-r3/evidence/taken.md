[A720m] TAKEN
Branch: 640-charter-followup (PR #835, at 30eb4834 on dev 503bc97c; round 3; nothing pushed by this pass)
Authoritative references: R766-2 (PR #835 issuecomment-6579449561), NEGATIVE on one MINOR, R766-2-F1; R765-2 POSITIVE; D18 (issuecomment-6575277828); sw/litex/ctrl_memory.py and sw/litex/milan_soc.py at 30eb4834.
Interpreted scope: docs only, docs/design/MARK_II_AREA_PLAN.md. R766-2-F1's required outcome: the BIOS rows say the switch-over removes the BIOS and its integrated ROM and SRAM, and that ctrl_memory's rom and sram banks hold those regions until stage 3; from stage 1 the boot loader fills rom (D18). Lane 2's scope says it drops DDR3 and fills rom from the flash copy, and no longer says it drops the BIOS ROM. Every statement of who removes the BIOS memory, on every page this PR touches, is made to agree and listed in the handoff. One commit; nothing else changes.
Validation plan: every run step of .github/workflows/docs.yml on a clean clone of the committed head, each rc recorded; check_doc_style on every touched page; git diff --check against 503bc97c; the census coverage check; the AREA_BUDGET.md and MAILBOX_SPLIT.md readers.
Blockers: none
