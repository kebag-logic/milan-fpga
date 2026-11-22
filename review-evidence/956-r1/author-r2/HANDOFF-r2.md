# HANDOFF r2: [A809], #956 and #957 (part of #665): the correction round for PR #958

Status: ROUND 2 COMPLETE. Final head `1825ba4eaccfe40788391b7af5533fae8c910a85`; code head `847b2e21`, whose only change after `b4a1dde2` is a plant
table. The round's one
`[A809] REVIEW READY` is posted on #956 (issuecomment-7073147873; its text is `REVIEW-READY.md`). Nothing is pushed: the manager
pushes `pf-951-943n-1` to `956-redeclare-inside-30s`. `PR-BODY.md` here restates the PR body for this head, for the
manager to apply if wanted; round 1's body still says the sliced build's lost due is "seen beside it, not changed".

Lane: `/data-2/milan/lanes/post-flip-fix`, branch `pf-951-943n-1`, on the flip train's head `15168e14` (PR #945).
Round 1's packet is `../round1/`. The reviews this round answers: R876-1 (issuecomment-7069018804, packet
`956-r876-1/`) and R875-1 (issuecomment-7069301447, packet `956-r875-1/`), both NEGATIVE at `0d80f0ed`.

## Commits this round (oldest first)

| Commit | What |
|---|---|
| `04819246` | Code: the sliced build keeps what came due between its slices, with the paused build THE TRANSMIT's due and the poll's owed (`tx_owed`, #956). The reset clears `declaration[]` (#957). Tests: the phase sweep and its 8x8/1if arm, the running-timer case, the paused-build unit test, and the SRP and composed reset tests. Plants for each, the transmit plants re-anchored, and the harness's `transmit-aged` plant anchor. |
| `578478bc` | Docs: FR_NFR's SRP row (R876-F3, R875-F2), and the SRP README (reset clear, sliced build, rom; R875-F3). |
| `b4a1dde2` | Code: a frame refused in a build's second slice keeps its interface due (A3; a corner `04819246` opened), with its test case and plant. A one-interface build's interface is fixed at compile time (112 B back at 8x8/1if). **Images and every code gate except the firmware gate ran here.** |
| `847b2e21` | Plant table: the new anchor renamed from `AGAIN`, which had overwritten the module's `AGAIN` test name, so `talker-unchanged-held` escaped in the gate at `b4a1dde2`. **The firmware gate ran here, all four shards.** |
| `1825ba4e` | Docs: SPLIT_CONTROL_MEMORY section 13 (the corrections, images, rom, rows) and the SRP README for `b4a1dde2` (final head). |

## Findings answered (detail in `REVIEW-READY.md`)

| Finding | Cause | Fix | Regression tests | Receipts |
|---|---|---|---|---|
| R876-1-F1, R875-1-F1 (MAJOR) | `reset_interface` kept `declaration[]` after destroying the registrations with no indication | `04819246`: cleared with `listener_present[]` | `Talker.ListenerRegistrationAfterAResetIsNoticed`, `AppOutputs.ListenerRegistrationAfterALinkResetIsItsStreamOutputsNotice` | `new-tests-fail-at-0d80f0ed.txt`, `reviewer-probes-at-b4a1dde2.txt`, `fw-gate-*` |
| R876-1-F2 (MAJOR) | A sliced build's second slice cleared a due a join timer's end set again between the slices | `04819246` + `b4a1dde2`: the pause takes the due, the paused build is owed (`tx_owed`), what came due is kept, and a refused second slice stays due | `EveryPhase/TalkerPhase.*` (200 a point, three points), `Talker.…WithTheJoinTimerRunning`, `Srp.ABuildPausedBetweenSlicesStaysOwedAndKeepsWhatCameDue` | the same, and `cpu-*-legs-*.md` |
| R876-1-F3, R875-1-F2 (MINOR) | FR_NFR's row kept #951's and pre-#951's figures and the old direction | `578478bc` | docs steps | `docs-steps-1825ba4e.txt` |
| R875-1-F3 (MINOR) | README said 18 B (the sections' sum); the ledger counts `rom_end`, 16 | `578478bc`, `1825ba4e`: now the ledger's 139,136 B, 128 left | `plat_ledger.py` | `rom-ledger-images-0d80f0ed-vs-b4a1dde2.txt` |

## How the round went (what a successor should know)

- The straightforward F2 fix read `tx_due` and `tx_resume` as two bytes in `transmit_aged` and the poll. That form put the
  8x8/1if image at 139,280 B, over its 58 RAMB36. The union's halfword read made it fit at exactly 139,264.
- Re-reading the result against THE TRANSMIT's contract then showed one corner broken: a frame the ring refuses in the
  second slice left its interface not due, because the pause had taken the due. That broke A3. Fixing it needed bytes.
  Fixing a one-interface build's interface at compile time, as it always was there, gave 112 back, and both fit
  (`b4a1dde2`).
- The firmware gate at `b4a1dde2` caught `talker-unchanged-held` escaping. My table's new anchor constant reused the
  module's `AGAIN` name. `847b2e21` renames it, and all four shards passed there. The `b4a1dde2` run's state is in
  `fw-gate-b4a1dde2-first-run.txt`.
- The 8x8/1if `srp-talker-held` leg was stopped once at the author's environment's time limit, then ran again alone,
  unbooked, in its own unit, since no CPU range was bookable. `srp-talker-loss` was graded from the first run's
  complete log (`run.py --regrade`).
- The release image varies from run to run in one string: LiteX's order of the CPU ISA's extensions, in the BIOS and
  the library's debug strings. The same revision exported three times shows both orders. It is not this lane's.

## Open risks

- The formal CPU measurement is not run. On the legs: `item.acmp_declined` sits at its statement at both points (as at
  `0d80f0ed`), and so does 8x8/1if's `record.srp`, 35,507 cycles, 375 of 375 us, about 200 cycles under the next step.
- A due set between a build's two slices now costs one more build pass, as after a build made whole. It is measured in
  the legs' groups, and every one is within.
- 8x8/1if's rom has 128 B left.
- The bench measurement of #956 (29 to 30 s at both points) is not done.

## Where the evidence is

- `receipts/` (`INDEX.md` is generated from the files present); per-image diffs are in `receipts/imgdiff/`.
- Scratch (not public): the lane's scratch directory holds the measurement trees, logs and tools. Nothing in the packet
  depends on them.
