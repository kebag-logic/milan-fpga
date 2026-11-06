[A698h] TAKEN

Branch: `665-s4-f1-target` (local worktree branch `s4-f1-target`), at round 6's head `7643aef6`, which contains `dev-soft-core` `a68536fa`. PR #812 targets `dev-soft-core`. Commits go on top, with no rebase and no force.

Authoritative references:
- [A10]'s round 7 assignment (issuecomment-6689759393). It is the whole assignment.
- R737-3 (issuecomment-6689752907) and R738-4 (issuecomment-6689696235), both NEGATIVE at `7643aef6`.
- The ruling on option (a) (issuecomment-6677095110): no F1 placeholder in any split image.

Interpreted scope:
- **Item 1, no silent placeholder image.** A link of the split platform image with no flash map is refused with a named error, or cannot produce an ELF. The boundary gate's compile-only run stays, with `ctrl_runs.stopped_at_link` true for it. `sw/firmware/ctrl/plat/README.md:88-92` carries the map in its command and says where the map comes from. Every other documented `ctrl_plat_image.py` link follows, or it would be refused as written.
- **Item 2, R738-4 F2.** The current writer's 8x8 maximum is restated at the merged head on the two pages, and the PR body's lines 53, 98 and 99 are corrected.
- **Item 3, R738-4 F3.** A committed negative test for `boot_soc.py`'s refusal of a deviating map, which also accepts the true map, with a mutant caught by name.
- **Item 4.** PR body line 213 states what is then true.
- **Unchanged.** RTL, firmware C sources, and `split_soc.py`'s behaviour.

Validation plan, all rc 0, on a clean clone of the committed head:
- the reviewer's `nomap_probe.sh`, and the page's command as written, with neither the `0x20000` window nor the `0xf0003800` timer constant in `ls_*`;
- `firmware_boundary` in both modes;
- S3's split boot at both shapes, and its self-test;
- the docs gates, with a clean HOME;
- `git diff --check` and the privacy check at 0;
- `check_nvm_capture.py`, and `rg '13\.863'` only where the design page records history.

RTL is unchanged, so there is no sweep and no Vivado run.

Blockers: none.
