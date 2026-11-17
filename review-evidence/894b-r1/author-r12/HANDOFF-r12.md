# HANDOFF — lane 894b (8x8/1if follow-up of #894), round 12, [A781]

Status: REVIEW READY at `8883d499` (comment text `REVIEW-READY-COMMENT.md`, posted once on #894 as issuecomment-6939551029, its text the file's). PR text
`PR-BODY.md`, the full body (Closes #930). Nothing pushed; no PR created or edited.

- Start head: 05a7ea82 (round 11's STOP, #894 issuecomment-6936661453), tree clean, 05:43 CET. No unit of mine running.
- Assignment: the manager's ruling on round 11's STOP, #894 issuecomment-6938589932 (read in full; saved at the
  scratch's r12/ruling-r12.md): (1) retarget the SRP plants asking-is-ready and readyfailed-ignored to where #930 moved
  the behaviour (the Listener callback, srp_mbx.c:185), each caught by name, proven on a clean clone, nothing weakened;
  (2) the twin and twin-plants failures are the base's stale split-talker-failed row, fixed by PR #935: record them as
  owed to #935; (3) then the SRP campaign and the shards that did not complete (1, 3, 4, 6, 10, 17) from fresh clones
  carrying the donor provenance; then one REVIEW READY on #894, this file and PR-BODY.md. Push nothing. Stop my own
  units by name at the end.

## Items

1. The plants. — `8883d499`: srp_mutants.py's asking-is-ready plants `declaration == MSRP_LISTENER_DECL_ASKING_FAILED`
   into the Listener's indication's copy (`i->registered[n] = ...`), and readyfailed-ignored replaces its
   `declaration == MSRP_LISTENER_DECL_READY_FAILED` with `false`; each keeps its test and words. Caught on the lane's
   tree at one and two interfaces, then on a clean clone of 8883d499 (plants_on_clone.py, the clone's own srp_mutants
   and lwSRP; the clone unchanged after): receipts/firmware/retargeted-plants-on-clean-clone-if{1,2}.txt.
2. The twin. — Owed to PR #935 (open against dev-soft-core: "restate the twin's stale Talker row"), recorded in the PR
   body's gate table and limitations; round 11's logs are the evidence.
3. The gates. — On fresh clones of 8883d499 (launchM.py, 8 units, at most 4 at once, on the session's CPUs; every range
   booked): the SRP campaign (run_wf.py, rtl-fast.yml firmware-srp-mutants): steps 1, 3, 9 rc 0, 436 [ok], 0 [ESCAPED];
   shards 1, 3, 4, 6, 10, 17 (vshard_r12.sh: the tsn-c-stack origin set to .gitmodules' URL, the provenance the shard
   reads): 37 suites, 966,909 checks, 0 failed; quick checks 23/23; qimg: all 8 images identical to 46cf2a7d's.
   Shard 1's tsn_fuzz rewrote the date line of two generated TEST_RESULTS.md pages in its clone (counts unchanged).
   receipts/gates/ (logs over 190 KB excerpted with their size and sha256; raw-manifest.json).

## Run history (CET)

- 05:43 resume; head 05a7ea82, clean; the ruling and round 11's STOP read (saved at r12/).
- 05:4x the plants retargeted; dev plants at one and two interfaces caught; py idiom (one long line wrapped); commit
  8883d499; a clean clone; both plants caught there at both interface counts.
- 05:46-06:24 the gates (above), every unit rc 0 and every workflow step rc 0.
- 06:2x the receipts; scratch back to 12 GB (shard clones and round 11's disposable clones removed, their logs filed);
  PR-BODY.md, REVIEW-READY-COMMENT.md, the index; the REVIEW READY posted once on #894.
