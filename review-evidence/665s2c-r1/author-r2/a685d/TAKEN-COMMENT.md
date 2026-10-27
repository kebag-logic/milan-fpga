[A685d] TAKEN

Branch: `665-s2c-icache` (local, not pushed), on [A685c]'s REVIEW READY head `de91db59` (PR #796, base `dev-soft-core`, stacked on PR #792 at `f58d049b`). New commits go on top; the manager pushes.

Authoritative references: the owner's NFR-SCOUT-01 amendment (issuecomment-6434741232) and its correction (issuecomment-6434744436), whose wording governs; `docs/reference/FR_NFR.md` NFR-SCOUT-01.

Interpreted scope:
- `docs/reference/FR_NFR.md:321`: NFR-SCOUT-01's first sentence becomes the corrected text, "The release architecture MUST use one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it stays cacheless." The rest of the row is unchanged.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md`: its one repetition of "cacheless" for the control hart (`:62`) takes the same wording.
- `docs/design/MARK_II_AREA_PLAN.md:383`: "NFR-SCOUT-01: one RV32I hart, 4 KiB instruction cache, no data cache".
- `docs/design/SPLIT_CONTROL_MEMORY.md:243-245`: the open-conflict paragraph becomes a record of the amendment and the 2026-10-27 decision.
- `docs/history/` is not edited. No code, test, measurement or other file changes. The PR body states the amendment instead of an open conflict.

Validation plan: the docs workflow's check-mode gates, `scripts/check_baremetal_only.py --check` and `--selftest`, `git diff --check`, and `cd tests && behave`. Every gate runs in the foreground, unpiped, and must return rc 0.

Blockers: none.
