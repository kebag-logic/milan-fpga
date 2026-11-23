STATUS (23:08 CET 2026-11-22): READY FOR INDEPENDENT RE-REVIEW at
`5759780f2251ef25221c6a395250312dce656ca4`. All requested Round 2 local gates passed. The extra split-boot
campaign also passed both shipping shapes, six native controls and six plants. Four Round 2 commits are local;
the worktree is clean. No push or PR edit was performed. The single Round 2 REVIEW READY comment is posted and verified
([#973 comment](https://github.com/kebag-logic/milan-fpga/issues/973#issuecomment-7086580403)). Hosted checks and independent re-review remain pending on this head.
ETA: local work complete; manager may push and request re-review now.

# HANDOFF r2 — #973 ([A822]) — PR #978, round 2 (R895-1 NEGATIVE: F1 BLOCKER, F2 MINOR)

Branch `pf-973-1`, pushed by the manager as `973-srp-link-carried` at `9a71daa9`. Round-2 commits on it:
- `f90ede10` F1: the plants' table in the firmware boundary's `OUTSIDE` list;
- `88d81818` the tests first: the reviewer's re-attach probe (it fails at `9a71daa9`), its control, and a link-up
  held behind a full event ring;
- `219df937` F2: an UP no LINK carried is taken once none is owed; four more plants;
- `5759780f` docs.

## 1. Review findings and what was done
Reviews at `9a71daa9`: R896-1 POSITIVE (issuecomment-7084707276, no findings); R895-1 NEGATIVE (issuecomment-7085166316).

**F1 BLOCKER (boundary).**
- Fix: `sw/firmware/ctrl/test/ctrl_configs.py:180-181`. `srp_link_mutants.py` is now in `OUTSIDE` with its reason, as
  `srp_talker_mutants.py`, `srp_listener_mutants.py` and `srp_reclaim_mutants.py` are: it names the firmware's tree
  and compiles nothing.
- Checks:
  - the reviewer's `boundary_census.py` no longer lists it. The five modules it still lists compile in the capture,
    as at the base;
  - `ctrl_boundary.py --require-rv32 --selftest` runs locally at the head (section 2).
- Why round 1 missed it: its validation never ran that documented gate. It is in this round's gate table.

**F2 MINOR (a re-attach that read a DOWN whose record was elided).**
- Fix (`srp_mbx.c:1273-1288`, `carried_up`; `:1303`, the poll; `srp_mbx.h:65-69`). `link_carried` keeps bit 0 as
  before: the level the last LINK the loop dispatched carried, or the register's at attach. Bit 1 is a mark.
  - A poll that reads an UP while bit 0 is clear sets the mark. It does not take the level.
  - A later poll takes the UP if no LINK has come by then (a LINK's level replaces both bits, `on_event`, unchanged)
    and that poll's pass's event take ended on an empty ring (`!loop->events_left`).
- Why that means no LINK is owed:
  - Only the loop takes events.
  - The fabric posts a LINK first of its sources as soon as the ring has four free words (`KL_mbx_evt.sv`; the model
    does the same).
  - So a LINK owed at the marking poll was posted then, if the ring had room. If the ring was full, it was posted as
    the next take made room. That take stops at `CTRL_LOOP_EVENTS_PER_PASS` (8) of the full ring's 16 records
    (`_Static_assert` at `srp_mbx.c:1281`), so `events_left` is set for it.
  - Either way, a later take that empties the ring took that LINK, and `on_event` carried it.
- #973's race stays fixed: its UP record is in the ring at the marking poll, and the next pass dispatches it as a
  first UP.
- Cost: no bus read and no call. The added code runs only for an UP no LINK carried.
- README line 112 ("Polling reconciles that level even without another LINK record") is true again.
  `README.md:114-128` states the rule.
- Tests, committed before the fix (`88d81818`), in `srp_link_pass.cpp` (its own process, 1x1/1if and 8x8/1if):
  - `Srp.AReattachWhoseDownRecordIsElidedFollowsTheLinkThatIsUp` (`:170-192`), the reviewer's probe. It adds "SRP
    resets the interface once for the link it follows". It FAILS at `9a71daa9`'s firmware at both shapes ("SRP does
    not follow a link that is up"), passes on the base firmware (`dd163e41`'s, which followed the register), and
    passes at the head;
  - `Srp.AReattachWithTheLinkDownFollowsItsLaterUp` (`:194-209`), the probe's control. It passes on all three;
  - `SrpLinkPass.ALinkUpHeldBehindAFullEventRingIsTheFirstUp` (`:139-168`), new. 32 stream counter-change records
    fill the 16-record ring twice over. The link comes up after a pass's events while the ring is full, so its LINK
    waits behind more than one pass of records. It checks that SRP takes no UP from the register meanwhile and that
    the first UP resets nothing and keeps the startup participants. It FAILS on the base firmware (the #973 double
    reset by another path) and passes at `9a71daa9` and at the head. It is what makes the rule's empty-take
    condition necessary (plant `link-pass-unowed-up-ignores-the-take`).
- Plants:
  - the reviewer's `rv-poll-resets-on-register-up` and my `link-pass-attach-carries-an-up` stay killed at all three
    campaign shapes;
  - four new plants: `link-pass-unowed-up-never-taken` (F2 reverted), `link-pass-unowed-up-taken-unmarked` (a
    double reset), `link-pass-unowed-up-ignores-the-take` (a double reset behind a full ring) and
    `link-pass-poll-or-instead-of-and`;
  - the planting sites of `link-pass-poll-takes-the-register`, `link-pass-down-waits-for-its-record` and
    `srp-poll-extra-read` follow the poll line. `link-pass-attach-carries-nothing` is caught now on
    `adapter.ifs[i].active[0]`: the first poll drops the UP, so the interface resets twice and loses the offered
    Listener. Section 2 has the table.
- The development campaign `receipts/checks/r2-plants.txt` also records three obsolete author plant expectations:
  two removed the sole use of `carried_up` and failed compilation; one expected the old Talker failure words.
  Their corrected forms pass in `receipts/checks/r2-plants2.txt` and the final full firmware shard. Compilation
  failures are not counted as kills. The raw exploratory failures are retained.
- The reviewer's four plants on the corrected firmware (same campaign driver, `receipts/plants/`):
  - `rv-poll-resets-on-register-up` and `rv-sink-double-reset`: killed;
  - `rv-poll-or-instead-of-and`: its planting site (the round-1 poll line) is gone. `link-pass-poll-or-instead-of-and`
    plants the same defect on the new line and is killed;
  - `rv-poll-clears-carried`: escapes, and under this rule it is no longer a defect. The poll clearing bit 0 when it
    resets on a register DOWN makes a later register UP with no LINK owed (the held DOWN elided) an uncarried UP.
    The rule takes it one poll later, with the same single reset. The final state is the same and no reset is
    added; recovery can be delayed by one poll. The existing test therefore does not kill this altered control,
    and its escaped result is retained rather than reported as killed.

**F3 SUGGESTION (a DOWN inside a pass resets twice): stated, not taken.**
- It is the same mechanism: the poll's fail-closed reset, then the DOWN record's in `on_event`.
- A discarded prototype skips a DOWN reset when a previously seen interface already holds DOWN, while preserving
  the first DOWN and repeated UP resets. Its object adds 16 B (`on_event` 164 -> 180 B in the sizing build).
  A fresh 8x8/1if platform link confirms ROM 139,272 B, 58.5 RAMB36, refused against the unchanged 58-RAMB36 ledger.
  The committed image is 139,256 B, just 8 B below its next ROM allocation. This supersedes the earlier 44 B estimate.
  Evidence: `receipts/checks/f3-discarded-prototype.diff`, `receipts/checks/r2-f3-image.txt`.
- The SRP README states it (`README.md:125-126`). The PR's limitations keep it. Nothing transmits on the down link
  between the two resets, because `link` is false.

**F4 SUGGESTION (an UP the sink drops on a re-entry).**
- Under F2's rule that UP is taken too: bit 0 stays clear, and the poll takes it once no LINK is owed.
- `README.md:124` states it. The path is the elided-record test's (an uncarried UP with no LINK owed), so that test
  covers it.

**F5 RESIDUE.** The PR body's line is now `Relates to #665, #970, #972, #872`.

## 2. Gate table
All Round 2 gates use `5759780f2251ef25221c6a395250312dce656ca4`.
Baseline measurements are retained from Round 1 at `dd163e41`.

| Gate | Result | Receipt |
|---|---|---|
| Test-first regression at both shapes | old firmware fails; current firmware passes | `receipts/repro/` |
| Firmware shard 0: suites | PASS, 77 suite verdicts | `receipts/gates/firmware-shard-0.txt` |
| Firmware shard 1: control plants | PASS, 826 / 826 caught | `receipts/gates/firmware-shard-1.txt` |
| Firmware shard 2: AECP plants | PASS, 385 `[ok]` | `receipts/gates/firmware-shard-2.txt` |
| Firmware shard 3: SRP plants | PASS, 576 `[ok]`; all 11 link plants killed at all three shapes | `receipts/gates/firmware-shard-3.txt`, `receipts/plants/` |
| Firmware boundary with RV32 and self-test | PASS; 4,455 sources, 0 findings, 306 controls | `receipts/gates/r2-bnd.txt` |
| Firmware coverage self-test and check | PASS, 40 files | `receipts/gates/r2-cov.txt` |
| Twin and map twin, both with plants | PASS | `receipts/gates/r2-twin.txt` |
| CPU harness, ten groups each shape | PASS, 88 / 86 probes; no refusal or budget miss | `receipts/cpu/` |
| CPU table graders | PASS, byte-identical to base | `receipts/cpu/graders/`, `receipts/cpu/compare/grader-equality.txt` |
| Platform images | PASS, 45 / 46 / 58 / 63 RAMB36 | `receipts/images/` |
| Split boot and planted controls | PASS, both shipping shapes, 6 native controls and 6 plants | `receipts/gates/r2-boot.txt` |
| Docs workflow steps | PASS, 104 / 104 | `receipts/gates/docs-steps.txt` |
| Builder legs 0 / 1 | PASS with one declared NOT RUN arm each | `receipts/gates/builder-leg-0.json`, `receipts/gates/builder-leg-1.json` |

### Changed checks and killing words

| Check / source | Planted defect | Required failing words |
|---|---|---|
| `srp_link_pass.cpp:170`, elided DOWN at re-attach | `link-pass-unowed-up-never-taken` | `SRP does not follow a link that is up` |
| `srp_link_pass.cpp:139`, UP behind a full ring | `link-pass-unowed-up-ignores-the-take` | `SRP took an UP from the register while its LINK waited behind the ring's records` |
| `srp_link_pass.cpp:136`, UP inside a pass, marking required | `link-pass-unowed-up-taken-unmarked` | `SRP's poll reset the interface on a level no LINK had carried` |
| Existing fail-closed DOWN check, new OR plant | `link-pass-poll-or-instead-of-and` | `adapter.ifs[0].active[0]` |
| `srp_link_pass.cpp:194`, ordinary later UP after re-attach | Paired control for the re-attach probe | Passes on base, Round 1, and corrected firmware; deliberately not a new defect detector |

Every killing assertion is preserved in `receipts/plants/` at 1x1/1if, 8x8/1if and 1x1/2if.
The four new plants are in `srp_link_mutants.py:68-83`; the moved poll-read plant remains in `srp_mutants.py`.

The discarded F3 prototype's expected ledger refusal is a sizing experiment, not a gate result for the candidate.
The reviewer's `rv-poll-clears-carried` control escapes as explained above; its campaign is not reported as all killed.
The hosted checks, local replica after the manager pushes, independent re-review, merge-candidate validation,
fit/timing gating and bench re-runs remain the manager's next steps. No source-bank, merge or LAB approval is claimed.

Publication receipt: `receipts/review-ready-post.json`. Final packet checks: `receipts/packet-audit.txt`.

REVIEW READY 5759780f2251ef25221c6a395250312dce656ca4
