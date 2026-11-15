# HANDOFF: #871 (#665 S11), AECP REBOOT, round 5 ([A761c]): the flip train's merge of #902

Status: REVIEW READY at `d3566d44`, #871 issuecomment-6899968849 (16 commits on round 4's accepted `049f0e4d`; nothing pushed by this lane). No STOP
condition holds. Next: two delta reviews from `049f0e4d`; the sync onto #898's head when the manager relays it.

## The assignment

The maintainer's ruling #665 issuecomment-6894152131, item 1: #881 joins the flip train (#902, #901, #898, #881, #914),
starts on #902's review head `41ca9f87` (REVIEW READY #894 issuecomment-6893619187; rulings #894 issuecomment-6883864236,
-6886633874, -6888782796) and syncs again on #898's. It measures REBOOT's record, accepted and refused, in a tracked
answering-ports group, held as an ordinary record by the rule; then the survey of every stated table over every 1x1/1if
leg, and the pace, slice and bound rules. STOP on the last queued notice over 140 ms, any other 1x1/1if row over its
bound, the load over 0.70, or REBOOT's record over the ordinary class. A ROM image past its ledger entry is reported, not a
stop (the owner's decision #665 issuecomment-6892332745).

## Commits (on `049f0e4d`, first parent)

| Commit | What |
|---|---|
| `6cfdf650` | Merge of `41ca9f87`, both sides kept (the PR body's table); the REBOOT port's CSR bank moved to `n_locs - 4`, below #902's record mover's; the wire model's initializer back to the base's form |
| `7072343a` | B15, B17 step twice per 10 ms (THE STEP), as #902's B10; B18's and B23's rings from the boot's first read, for the driver's cached tail |
| `b4b0c3eb` | THE RETRY's round holds an accepted REBOOT (`round_waits`); core check and defect `reboot-retries-after-its-success` |
| `88b0fcd1` | B18 full for its SHUTDOWN's sends and the next poll's, over room for one frame, so the owed DEPARTING's defect is caught |
| `b01968a4` | The harness's `aecp-reboot` group in the answering-ports arm (its patch list gives the fixture a reset port); `record_classes.py` holds REBOOT's records as ordinary and refuses a pass without an accepted and a refused one |
| `24e63089` | The platform's 8x8/2if entry 60.5 RAMB36 at `ctrl_plat` 20,416 B (owner 2026-11-15); `ctrl_plat` at every point |
| `a3e45e68` | The REBOOT simulation's flash device held to the flash map's KLJ3 journal |
| `9447702a` | Within the idiom ratchets: `aecp_reboot_mutants.py`, `reboot_group.py`, a rewrapped comment, B18's flags apart |
| `7b452a5f` | Documents: the size table, REBOOT_RESET section 8, the READMEs, the REBOOT simulation's figures |
| `7653571f` | Restated at 1x1/1if by the rule: `record.srp` and `item.retained` 285, `CTRL_LOOP_SRP_UNIT_US` 285, `record.aecp` 240, `events_none` 40, the paced class 305, `AECP_QUEUED_MS` 135 |
| `935dacf2` | `notice_window.RUN_MS` 135, the notice self-test's bound and over-bound case |
| `41dcdd8f` | Documents: FR_NFR 3.4.1, SPLIT_CONTROL_MEMORY section 13, the AECP and harness READMEs |
| `57daf4ff` | REBOOT_RESET section 8: REBOOT's record and its evidence row |
| `20e08ceb` | The REBOOT simulation's early-reset plant before AECP's handler (a plain response is committed in the record's turn under #894) |
| `cb0fc679` | That plant described as it acts: every AEM_COMMAND REBOOT's take, refused ones too |
| `d3566d44` | `owed-round-beside-the-queue`'s anchor beside the REBOOT's `round_waits` term (the full AECP campaign had refused it) |

## Results

- REBOOT's record (`aecp-reboot`): at 1x1/1if SUCCESS 11,467 cycles (125 us), the refusals 100 to 115 us, all within the
  ordinary 240 us; at 8x8/2if 95 to 115 us within 265. Both images give the same cycles.
- The survey (`compare_point.py` over arm A, the answering-every-port arm and the answering-ports arm): four costs over,
  all restated by `7653571f` (the PR body's table); the cause is the hot-code move (`aecp_retry_aged` -28 B fourth in the
  hot order; `aecp_command` +124, `aecp_rx` +36, `aecp_poll` +36, `aecp_tx_complete` +28, `aecp_ready` +12).
- On the rebuilt image every leg again: only the class lines over; `record_classes.py` RESULT PASS over every leg.
- Rows at 1x1/1if, flip check PASS: R4 13.23, R5 74.81, R6 72.88, first 14.69, last 134.74 of 135, R4L 188.51, ACMP
  29.22 of 30, ADP 27.53, MAAP 27.65, tx 33.66, txL 48.75 of 49. Load 0.520 (0.516). Slice 950 us chosen (4 of 420 hold),
  pace 8 ms.
- Images: fixture 41.0, 42.5, 54.5, 59.0; platform 43.0, 43.5, 56.0, 60.5 (past 60.0, raised). Unchanged by the
  restatements.
- The final pass: every gate green (the PR body's table, with the head each ran at). The identity of the carried gates:
  after `57daf4ff` only the REBOOT simulation's plant and README, their comments and one AECP mutant row changed; each
  gate that runs one of those ran again after it.

## Notes for the next round

- The margins are small (txL 0.25 ms, the last queued notice 0.26, ACMP 0.78); the #898 sync will move the hot code again,
  so the survey must rerun there.
- `CTRL_LOOP_SRP_UNIT_US` (`sw/firmware/ctrl/loop/ctrl_loop.h`) is restated by #894's derivation rule; it is this lane's
  only `ctrl/loop/` change, flagged in the PR body.
- The REBOOT-only mutant drivers plant only REBOOT rows; a merge that touches shared lines needs the full AECP campaign
  (here it found `owed-round-beside-the-queue`'s moved anchor), or an anchor check over every table
  (`scripts/anchor_check.py`; `receipts/model/anchor-check-d3566d44.txt`: 314 defects, each one site).
- Scratch (`<scratch>`) is about 8 GB; the legs' and passes' logs are in `receipts/`.
