[A698i] TAKEN

Branch: `665-s4-f1-target` (local worktree branch `s4-f1-target`), at round 7's head `37e03930`, which is PR #812's live head. PR #812 targets `dev-soft-core`. Commits go on top, with no rebase and no force.

Authoritative references:
- [A10]'s round 8 ruling (issuecomment-6692215350). It is the whole assignment.
- R737-4 (issuecomment-6692178209, NEGATIVE) for R737-4-F1, and R738-5 (issuecomment-6692208886, POSITIVE).
- The note keeping the size fixture out (issuecomment-6691621669).

Interpreted scope:
- **The refusal.** `ctrl_plat_image.py` refuses a `--flash-map` directory that lacks `generated/csr.h` or `generated/mem.h`, as it refuses a missing map, at the link and before the compiler is called.
- **The tests.** The self-test's map fixture carries the complete map shape. New checks cover a JSON-only map and each missing header, at the shape's true clock, each with a planted mutant.
- **The statements.** The four universal statements (`ctrl_plat_image.py:15`, `ctrl_image_selftest.py:30`, `plat/README.md:101`, PR body line 217) are made true or narrowed.
- **Unchanged.** The size fixture, `ctrl_srp_image.py`, RTL and firmware C. SUGGESTION and RESIDUE items stay out unless the same edit fixes them.

One file outside the ruling's list: `sw/firmware/ctrl/README.md:711,719-721` quotes the self-test's count (37) and describes its "last four" checks, so the ruled checks make that page false. I plan to correct those lines in a commit of their own, which can be dropped without touching the rest. Say so if you would rather leave it out.

Validation plan, all rc 0, on a clean clone of the committed head:
- `ctrl_image_selftest.py --require-rv32`;
- `firmware_boundary` in both modes;
- the docs gates, with a clean HOME;
- `git diff --check` and the privacy check at 0.

No listed gate links a real generated map, so I will also run the reviewer's partial-map verification and S3's split boot at both shapes, to show a complete map is still accepted. No long gates, no sweep, no Vivado.

Blockers: none.
