Status: REVIEW READY
ETA: complete; no author jobs remain.

[A826] Round 5, issue #979 / PR #987. Head 9acb9b828b29aba71bd51303a4836f86c2278267 on pf-loopbram-1, target dev-soft-core.
Seven local commits on dc78aedae34c25a97125ecd6816a1f645db5575f; nothing pushed; no issue or PR comment.
No RTL, firmware, configuration, submodule or workflow byte changed. Under `hdl/`, only three Markdown files changed.

- R909-2-N1 (BLOCKER): both suites are registered at measured, scaled figures (38 s, 107 s). The planner
  self-test passes and 19/19 shard listings exit 0. The largest predicted worker is 1615 s of 1620.
  Shards 15/19 and 16/19 pass through the sweep driver with complete accounting.
- R910-2-F1 (MAJOR): delivery is graded per output stream in both phases, with a one-packet tail bound.
  The reviewer's exact talker-7 plant now fails `WIRE_STREAM_DELIVERY`/`WIRE_STREAM_COMPLETE`. Every 8x8 talker
  and the 1x1 talker are planted. The parent campaign has 17 entries, all passing.
- R909-2-N3 (MINOR): the parent campaign is listed in TESTING.md's explicit-campaign registry.
- R910-2-F2 / R909-2-N2: the enabled 8x8/1if image was routed from this head's source. The release placement
  missed (+0.008 ns), so best of three was run: +0.223 ns setup, +0.036 ns hold, all four corners, zero failing
  endpoints and routing errors. LUT 48901, FF 54672, BRAM tiles 111, DSP 11. One of three recipes meets the
  floor, so the margin is placement-sensitive; every worst path is in the mailbox. The 70.5-tile control
  memory is S14 debt (+11.5 over the 59-tile ledger) and the allocator still refuses it. 1x1 was not re-routed:
  its RTL is unchanged.
- Disabled identity: unchanged by construction; round 4's canonical hashes stand.
- Found by the author and fixed: seven gates that failed on this PR's own files. They are the Python and
  C/C++ idiom gates, the test-evidence, traceability, contents and inventory gates, and the sweep tally.
  The hosted docs and Verilator aggregates would have failed at dc78aeda.

Every round-3/4 gate passes at 9acb9b82, together with the docs workflow replay (43 steps).
The render campaign ran in pieces under the two-hour job limit; their union is exactly the runner's 32 arms.

Not done: the complete serial sweep (about 8 h); hosted and act runs; candidate-merge validation.
Two scratch temp directories from the stopped render runs remain under /data-2/milan/tmp/loopbram-a826-r5;
deleting them was not permitted in this session.

[Round-5 delta and finding closures](REVIEW-READY.md)
[Full updated PR body](PR-BODY.md)
[Exact-head receipts](receipts/INDEX.md)

REVIEW READY 9acb9b828b29aba71bd51303a4836f86c2278267
