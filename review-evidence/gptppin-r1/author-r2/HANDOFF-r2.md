# HANDOFF r2 — [A835] #994 gPTP pin 1213ac5b, PR #995

**Status (2026-11-24, CET afternoon): REVIEW READY at `f97e49fe`.** ETA: done. Nothing is running; every command ran in the foreground. Not pushed (the manager pushes). Scratch: `$VALIDATION_STORAGE/gptppin-a835-r2` (clones, probe trees, build products), disposable.
Branch `994-gptp-pin-1213ac5b`: round 1's four commits, then the merge of dev-soft-core `2509db68` (tree-identical), then two commits. PR body: `PR-BODY.md`. Delta and evidence: `REVIEW-READY.md`. Receipts: `receipts/INDEX.md` (53 files, 472 KB, none over 200 KB, no .gz, host paths normalized).

## Commits since bbfdb674
- `3a8bdbf0` Merge dev-soft-core 2509db68 (PR #988 train) into the 1213ac5b pin lane. Tree `eb8282df`, equal to bbfdb674's.
- `d616b1c6` Grade FPGA-gPTP #106 and #107 through the gptp_shadow slice and the real PHC, with both donor defects planted in its campaign.
- `f97e49fe` Record the gptp_shadow takeover grading and #997 in the 1213ac5b records, and state the release routes' selection rule as #818 does.

## Done, per item
1. F1 (MAJOR, both reviews): `tb/verilator/gptp_shadow` phases 18 (#107), 19 and 20 (#106), through the real engine, the real PHC and the slice transport. 408/408 at the head.
   - The campaign is 11/11. The two new controls fail their named checks, and R916-1's own patches each turn 4 named checks red at the head.
   - gptp_shadow, gptp_plane (run and all 8 phc-step arms), gptp_tables (run and 26/26 controls), gptp_txts, tsn_fuzz with tsn-gen, and milan_dp gptp and gptp-lat all pass at f97e49fe.
2. F2: #997 linked from the PR body's Known limitations and the #994 record in SUBMODULES.md.
3. R1: the #994 record's selection rule in R915-1-R1's words, fitted to the style gate's 10 words (see the open question). check_doc_style.py OK (25 documents). R916-1-R1, R915-1-R2, R3 and S1 done too.
4. Image inputs: none changed, so no re-route. Paths since 973f2f20 are docs, Markdown, tb/ and the ROM ledger, and the gitlinks are identical. The ROM regenerates to the ledger's 4eb21cef. plat_ledger PASS, with 24/24 image digests equal to round 1's.

## For the manager
- Push the branch, then replace the PR body with PR-BODY.md. The stacking paragraph is gone: the train has merged and this branch merged dev-soft-core.
- The PR is not a draft, so the push starts the hosted exhaustive gates on the new head. Run the act replica from a trusted dev-soft-core worktree.
- `gptp_shadow` now runs about twice as long: its default target runs the simulation 12 times, at 94 s against 47 s per run on the loaded host. `scripts/suite_shards.py` registers 393 s, measured hosted before this change. Re-measure it from this head's hosted window (`suite_shards.py --measure`) if the worker projection needs it.
- Not run this round, with the reason in REVIEW-READY.md: both builder legs and the docs job's compiler-absent firmware controls (each beyond a ten-minute window, and none reads a changed path), the full sweep and the physical milan_dp_gptp leg (no input of theirs changed except the suites re-run above).
- Candidate Issue (pre-existing, not changed here): gptp_shadow's `credit_never_withheld` control names a check that does not exist ("credit: the engine is held off at the reserve"). It is caught only by other checks, at bbfdb674 as now.
- Open for the reviewers: R915-1-R1's exact sentences exceed the style gate it also asks for. The wording kept its words and split one sentence. Confirm it.
