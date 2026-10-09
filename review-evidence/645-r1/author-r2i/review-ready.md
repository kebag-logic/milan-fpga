[A531] REVIEW READY — Round 2i
Commit: 7426045c94c317363e5589856e6f3f9fde1a2d21

R475-7-F1: exact rational decimal times now govern event/PDU half-open bins, origins, bounds, steps and servo comparisons. The five original standing methods remain; three new methods cover decimal start/end/interior edges, adjacent instants, PDU attribution and the short final bin. No grace interval was added.

Validation: all 48 recorded validation jobs returned rc 0.
- `python3 -B tb/verilator/follow_ring/test_trace_table.py`: 8/8 methods pass, including 27 event/PDU boundary cases and nine 1e-30 neighbours.
- Unchanged public `scripts/decimal_boundaries.py SOURCE PACKET`: 9/9 pass. The parent reader gives 0/9; the new standing methods also fail against it. Expected raw failures are retained separately; their validation wrapper passes.
- Unchanged recentre probe and genuine counter receipts replay correctly. Fresh pull-in, duplicate and skip acquisitions each pass 18 checks. Their event bins report respectively (slips, skips, recentres) = (0,0,1), (1,0,0), (1,1,0); bounded inputs reproduce the full-trace rows.
- All 34 source/documentation checks pass; committed diff/punctuation and scope checks pass.
- `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`: rc 0, 1231.392 s. The historical gate-11 mf48 calibration arm remains explicitly uncovered because its placed report is absent; there is no RV32/elaboration toolchain skip.

R474-5-F1 records: verified all 277 hashes and 45 source bindings in the [published Round 2h packet](https://github.com/kebag-logic/milan-fpga/tree/5c575da7157c814088ea4df12aab6c5877841f4b/review-evidence/645-r1/author-r2h). TESTING.md and both Makefile headers now record [run 37892515345, shard 0/5 job 113696564335](https://github.com/kebag-logic/milan-fpga/actions/runs/37892515345/job/113696564335): sequential `make -C`, successive verdict windows including build time, follow_ring 1114.2 s PASS (margins 325.8/685.8 s), render 1218.7 s PASS (221.3/581.3 s). The earlier projections remain, with render's 1050.3 s underestimation stated explicitly.

HANDOFF.md and PR-BODY.md retain earlier rounds and add Round 2i reproduction, classification, options, zero RTL-area delta, protocol effect, test plan and recommendation. The bounded Round 2i packet includes command/rc receipts, hashes and a passing portable replay. The worktree is clean and all jobs have ended. RTL, recipes, pins and CI policy are unchanged.

Assigned corrections are ready for independent re-review. Finding closure and lens coverage remain with the reviewer; the manager owns packet/branch publication and hosted acceptance of this new head. The hosted measurements above cover 8e4b1e53, not this later commit.
