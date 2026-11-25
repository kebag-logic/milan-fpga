# HANDOFF r4: [A834] lane lwsrppin, round 4 (R913-4 F1 option (a), F2)

Status (23:10 CET 2026-11-24): **STOP: an owner decision is needed on the egress ledger at 8x8/1if.** Everything
else in the brief is done, with evidence. The harness ran on the merge head's images, proven identical. All six
runs and the self-test exit 0, and the PR body is rewritten for `507bce7f`. But `egress_ledger.py --point 8x8-1if`
fails at the merge head, and under its rule only a ruling can restate it. Nothing of this lane is running.
ETA: none. The lane waits for the ruling. Once it exists, the body needs one paragraph changed, and nothing needs
re-running unless the ruling asks for it.

Head `507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698`, unchanged and pushed. No commit, no push, no comment, no bench.

Outputs: `REVIEW-READY.md` (the evidence, in the review-ready form, headed as not ready), `PR-BODY.md` (full; not
applied to the PR), `receipts/INDEX.md`.

## Brief items

| # | Item | Outcome |
|---|---|---|
| 1 | Harness, arm A, every-port and later, 1x1/1if and 8x8/1if, on the merge head's images | Image identity proven: arm A is `79c5326c…` and `eed56acc…`, equal to the ledger files. The variants differ only in the size fixture object. All 6 runs rc 0, and `run.py --self-test` rc 0. 0 passes over THE SHARE in five runs. At 8x8/1if arm A, 1 pass is over THE SHARE: `srp-bound`'s 210,174 cycles, owed to #977 by #969's amended ruling, with `kept_grade` PASS (0 findings) at both points; it is 216,785 on the train's image. MRPDU and own-LeaveAll rows all within 49 ms. Load and flip PASS within the owner bounds, byte-identical to `2509db68`'s. **The egress ledger FAILS at 8x8/1if**: 7 of 7 rows over. The train's image already has 5 of 7 over, and the pin's +0.086 ms takes 2 more over (the comparison is in `REVIEW-READY.md`) |
| 2 | PR body | `PR-BODY.md`: the merge, the gates at `507bce7f`, the image deltas against both parents, the merge-head route, the harness, and the egress decision as an open section. Every statement that held only at `30796098` or earlier is removed or labelled with its commit |

## Notes for the manager

1. **The decision.** The egress ledger's figures (`egress_ledger.py` `MEASURED`) need a ruling for the composed
   image (#894's ledger rule: growth reproduced at a ruled upstream head), or another disposition. The growth is
   mostly the train's. `dev-soft-core` at `2509db68` already fails the leg on its own image, and the train's record
   of its composition does not mention the ledger. That probably wants an Issue of its own, whatever happens to this
   PR.
2. **THE SHARE wording.** R913-4 F1 asks that "0 passes may exceed THE SHARE". The one pass over it is owed by
   #969's amended ruling and matches the train's own record. A reviewer may want that named in the verdict.
3. **Do not post `REVIEW-READY.md` as review-ready** until the decision exists. `PR-BODY.md` can replace the live
   body now: it states the open decision rather than hiding it.
4. **Runtime.** The host was saturated (load 160 to 215 until about 19:30), and arm A took 7.2 and 7.5 h, against
   round 1's 3.4 h. The base comparison (2 groups at `2509db68`) took 27 min once the load fell.
5. **Housekeeping.** Scratch: `/data-2/milan/tmp/lwsrppin-a834/r4/` (harness build trees and full logs, 7.0 GB). The train worktree `/data-2/milan/tmp/lwsrppin-a834/base` is still detached at `2509db68`, with porcelain 0.
   The lane checkout has porcelain 0. The earlier rounds' scratch (`route`, `fw3`, `r3`) is still there; `r3/ledger`
   holds the image files this round's identity proof reads.
6. Receipts: every file is text and under 200 KB, with no .gz. Logs over 190,000 B are cut to their first and last
   90,000 B, with the full size and sha256 at the cut (`tools/rcopy.py`).

STOP: egress_ledger.py --point 8x8-1if fails at the merge head 507bce7f (7 of 7 held-egress rows over their ledger figures, by 0.004 to 0.688 ms); the train's own image 2509db68 already fails it (5 of 7) and the pin's lwSRP change adds about 0.086 ms to six rows; a restatement needs an owner ruling under #894's ledger rule; every other F1/F2 item is done (6 harness runs and the self-test rc 0 on images proven identical to the merge head's, kept_grade PASS, PR body rewritten)
