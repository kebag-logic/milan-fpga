# HANDOFF r3: [A825] #977 (part of #665): round 3, ruling item 5 (builds after swaps, copies, single delivery)

Status: **STOP** (03:10 CET 2026-11-25), for the owner by the ruling's item 6. The STOP comment is posted once on
#977 (issuecomment-7150059792; its text: REVIEW-READY.md). Nothing is pushed; the manager pushes.

- 8x8/1if load 0.759 against 0.75 (`flip_grade.py --check --point 8x8/1if` FAIL). The registrations term (0.015, at
  150 us a Talker all in) is all of the excess, 0.744 without it. The 64 us target is not reachable with exact changes
  in item 5's scope: THE SETTLE (ACMP's completion of each sink, tsn-c-stack) is ~5.4k cycles a Talker, 60 us by the
  rule, by itself.
- 1x1/1if: AECP's notice item over its stated 150 us in the answering-ports and declaring-outputs arms (15,283 and
  15,282 cycles; the base's 14,212 and 14,001), so those two arms fail. It is code placement (the same instructions;
  `fan_out`'s loop at another address), and the split image's hot list was not relearned at this head. Remedies for
  the owner: relearn the hot list, or state 165 us (`AECP_QUEUED_MS` 135, within 140). Either way it is a new image.
- Every other acceptance item holds. 0 passes over THE SHARE on all 16 arms; every slice and record within its
  stated length and charge; kept_grade PASS with nothing owed; rows at 1x1/1if equal to the base's; owner bounds
  unmoved.

## Heads (local, not pushed)

- milan-fpga `pf-977-1` `4935ef692356ae39f0c1ba818569a1a4961e2196`: round 2 `4ddbcb81` + the train `adc13dbd`
  (`871dcfee`) + #992 `002a195b` (`673dec63`) + round 3's commits + `dev-soft-core` `2509db68` (`abb6b585`) + #992
  `507bce7f` (`4935ef69`). The image is `8b4a79d5`'s; every later commit is ledger, harness, test runners, twin or
  docs, and every image built at `4935ef69` is byte-identical to the one measured and routed.
- lwSRP `opt-exec-3` `73007b4807977517045e8aa485c61ebb8f5ee843` (new branch: opt-exec-1 and opt-exec-2 rebased onto
  `main` `d1bb4f4e` + round 3's options); the pin. All 14 lwSRP gates pass there.
- Comparison base: train `adc13dbd` + #992 `002a195b` merged in a scratch clone (local `38f599ff`), lwSRP `d1bb4f4e`.

## Round 3 changes

| Commit | What |
|---|---|
| `60a777ec`, `035db6e9`, `03d437ae`, `670e2b63` | lwSRP RAPID_REPLACE, LEAN_COPY, LEAN_TX at both one-interface shapes |
| `61aa055e`, `96c5ff49`, `2607bbac` | sink index by StreamID last byte; a declaration owes the walk only for a source's StreamID; tests, 7 defects |
| `3cb54229` | Q1: `whole_grade.redeclared` |
| `683e56d7`, `3b9cd5d9` | kept_grade owes nothing; its charge lookup fixed (it held every record to the unit alone) |
| `32cdfe60`, `8b4a79d5` | kept path: last byte first, last-octet sets, inline StreamID copies; 4 tests, 8 defects |
| `72b38c99`, `dd26638e` | ledger: fixture 8x8 58.5 / 62.0, platform 8x8 60.5 / 65.0, ctrl_plat 18,240 / 19,968 / 19,264 / 22,016 B |
| `c03f11ae` | walk 35 / 120 us, 1x1/1if last queued notice 130 ms, THE TRANSMIT 8x8/1if 77 ms |
| `3059a8ab` | the flip check's self-test plant at 76 ms |
| `9c2c2add` | registrations term 150 / 135 us; docs |
| `abb6b585`, `4935ef69` | merges of dev-soft-core 2509db68 and #992 507bce7f (kept_grade's self-test 33 checks) |

## Evidence (receipts/, INDEX.md)

Every gate at `4935ef69`: firmware gate 4 of 4, coverage, twin (32 plants refused), builder legs (one arm each not
runnable here), docs workflow (104 steps), harness self-tests, plat_ledger --self-test (9 of 9) and test_ctrl_memory.
Routes at `dd26638e` (images identical): 1x1/1if WNS +0.301 / WHS +0.014 ns, 8x8/1if WNS +0.143 / WHS +0.036 ns.
Every arm: runs on the image, regraded at `4935ef69` (tables identical), base-vs-head differential with named
differences (receipts/arms/diff-NOTES.md), every poll item restated over every arm (receipts/arms/restate-*).

## Manager answers to round 2 (status)

- Q1: done; on both arms with the registering groups, 8 and 2 re-declaring builds, none over.
- Q2: recovered in six of eight 1x1/1if arms (at most 14,070 cycles); not in answering-ports and declaring-outputs.
- Q3: the drain difference kept named with its NOTE; this round's base predates the registering groups.
- 130 ms wording: corrected.

STOP: the 8x8/1if load is 0.759 against 0.75 (ruling item 6, for the owner), and AECP's notice item is over its stated 150 us by code placement in two 1x1/1if test-port arms
