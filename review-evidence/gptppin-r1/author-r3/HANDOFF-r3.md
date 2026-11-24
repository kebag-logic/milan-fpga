# HANDOFF r3 — [A835] #994 gPTP pin 1213ac5b, PR #995

**Status (2026-11-24, CET evening): REVIEW READY at `fc6870ca`, with one stated gap.** ETA: done; nothing is running. Every command ran in the foreground.

The gap: milan_dp `gptp` and `gptp-lat` did not finish at this head inside a 590 s window. There were six attempts each, at load 195 to 260 on 96 CPUs. Their inputs are unchanged since `f97e49fe`, where both passed 212/212.

Not pushed (the manager pushes). Branch `994-gptp-pin-1213ac5b` = `f97e49fe` + 2 commits. PR body: `PR-BODY.md`. Delta and evidence: `REVIEW-READY.md`. Receipts: `receipts/INDEX.md` (172 files, about 1.07 MB, none at 200 KB, no .gz, host paths as placeholders, screened for agent and vendor model names). Scratch (disposable): `$VALIDATION_STORAGE/gptppin-a835-r3`.

## Commits since f97e49fe (one-line, no trailers)
- `567eaa48` Grade the gptp_shadow race against the re-election clock and the Announce credit through the ticket reserve, with both defects planted in the campaign.
- `fc6870ca` Record the reserve-credit arm, the race's re-election boundary and the renumbered takeover phases, and order the #994 selection rule as #818 states it.

## Done, per item
1. R916-2-F1: the race check now counts master Announces whose last lane beat precedes `fall`, the re-election clock. R916-2's lane stall fails "#106 race: one master Announce reaches the lane before the re-election" (423/424). It is campaign control `master_announce_reaches_the_lane_after_the_re_election`.
2. R915-2-F1: phase 21's new reserve arm withholds credit by the ticket reserve, with no fence: one Sync record is held and the Announces fill the ticket to 5 outstanding. R915-2's p106-nocredit fails "#106 reserve: no master Announce reaches the lane without credit" (421/424). It is campaign control `announce_leg_ignores_the_credit`. The seal arm stays, renamed "#106 seal: ...", and grades the retry.
3. R1-R3 exactly as stated. S1: the sign is in the README and the PR; the donor issue was not filed (no GitHub writes). S2: declined, with the reason in the PR. S3: measured here; the hosted estimate is about 840 to 950 s of the 1,800 s suite timeout, and the shard balance holds to 1,200 s.
4. At the head:
   - gptp_shadow: run 424/424, lifecycle PASS, campaign 13/13.
   - gptp_plane: 31/31, phc-step 62 checks and 8/8 arms.
   - gptp_tables: 36 checks and 26/26 controls. gptp_txts: 95 checks and 13/13 controls.
   - Docs: 48 workflow steps rc 0.
   - Images unchanged by hash: 24/24 firmware digests, 291 blobs and gitlinks, both pin PNGs, ROM `4eb21cef`.
   - milan_dp gptp and gptp-lat: NOT COMPLETED (above).

## For the manager
- Push, then replace the PR body with PR-BODY.md. PR-BODY.md ends with the tool-attribution line this session's instructions add to PR descriptions. Round 2's body had none, so drop it if the lane's convention says so.
- The push starts the hosted exhaustive gates (the PR is not a draft). Run the act replica from a trusted dev-soft-core worktree. The hosted or act `verilator-suites` run is where milan_dp `gptp`/`gptp-lat` complete at this head.
- `gptp_shadow` needs its hosted figure. Run `suite_shards.py --measure` on this head's worker log and replace 393 s if the worker projection needs it.
- Re-review scope: Tests and Robustness (both findings), plus Docs and Conformance (README, SUBMODULES and CHANGELOG changed). No product RTL, synthesis or firmware input changed.
- Not done, not asked: R915-2-S4 (`ownership()` under an inherited `make -s`) and S5 (an Issue for `credit_never_withheld`'s unmatched name; still caught only by the quiet-start guards).
