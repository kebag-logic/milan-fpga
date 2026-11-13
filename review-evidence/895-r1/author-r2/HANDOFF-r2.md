# HANDOFF (round 2) — [A775] lane 895: a split Talker declares only while its SRP parameters are valid

**Status: REVIEW READY at `18300f6e5f0c63b2ebc81d6bbc243496034f638a`; the clean-clone gate pass ran once on it and
passed (section 4).** Round 1 ended at REVIEW READY `d023b77a` (#895 issuecomment-6838154041); both reviews NEGATIVE
(R835-1 PR #901 issuecomment-6840458159, R836-1 issuecomment-6840411046); the ruling is #895 issuecomment-6840463408
(items 1-6); acceptance 4 amended. REVIEW READY posted once on #895: issuecomment-6850450637 (11:5x CET). Push and the PR edit are the
manager's (PR-BODY.md).

- Worktree $LANES/895-talker, branch `895-talker-redeclare`, not pushed, clean.
- Base `665-s2b-cycles` at `b2d39235` (#810 round 29) at every check before the gate pass (03:50, 04:05, 05:39, 07:01,
  09:40; the pass started 09:43): nothing merged. #810 round 30's REVIEW READY (`5bea2597`, #665) came 10:10 CET, after
  the pass started; at 11:4x the branch is `32551422` (R711-9/R712-9 reviewing). Not merged (ruling item 6): the
  composition with round 30 is the manager's next step, with its own gate pass.
- No unit of this lane runs. Scratch (legs R3-*, harness F4-*, gates3, gates3h, sweep clones
  $LANES/895r2sweep-shard{0..3}) stays for reuse; /data-2 at about 30 GB free.

| Commit | Subject (short) |
|---|---|
| `e0398c40` | F5: a refused withdrawal Leave kept declared and owed; F4: srp_bounds.h's count; 2 tests, 3 plants |
| `0e2dd73d` | coverage ratchet (superseded by `de381464`) |
| `d4ef6d4f` | two plant-table lines to the 120-column rule |
| `a7609d02` | RS1, RS2 (+S2), README/MAILBOX_SPLIT notes, section 5 (figures restated again in `de381464`) |
| `17ac263f` | `moved` one instruction shorter: the hot layout after `declare_sources` is round 1's again |
| `de381464` | coverage ratchet 725/725, 651/651; section 5 at this head's images |
| `18300f6e` | section 13: this head's graders (8x8/2if pass 320 us), the legs, the hot layout |

## Items (ruling issuecomment-6840463408)

| Item | Finding | State | Commit | Evidence |
|---|---|---|---|---|
| 1 | F1 (both): acceptance 4 by the ruling, head-against-base table | done: PR-BODY.md and the RR state it by the ruling, never "met"; table of every figure at head and base | `18300f6e` | receipts/graders (head-*, base-*), receipts/costs, receipts/legs |
| 2 | F2 (both): SPLIT_CONTROL_MEMORY.md figures; F3: plant count | done: section 13's 8x8/2if pass 320 (grader); section 5 at this head's images, +944 to +1,064 B rom over `b2d39235`; plant count 29 at this head (26 at `d023b77a`, +3) in the PR body and RR (no repo doc states a count) | `de381464`, `18300f6e` | receipts/rom, receipts/gates/workflows/mutant-counts.txt |
| 3 | R835-1-F4: srp_bounds.h argument; counting test | done: at most twice on the interface the call builds; `Talker.TransmitPublishesWithinItsTermsAfterARefusedJoin`; plant `talker-transmit-publishes-past-its-terms` | `e0398c40` | receipts/plants, gate SRP campaign |
| 4 | R835-1-F5: refused withdrawal Leave kept owed | done: `Talker.RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt` (the reviewer's sequence through the real reclaim, the Leave on the wire); plants `talker-refused-withdrawal-forgotten`, `-not-owed`; no lwSRP change | `e0398c40` | receipts/plants, gate SRP campaign |
| 4b | the Domain's own leave/join on the same path | CONFIRMED by a probe, NOT fixed (not the same mechanism): section 2; **for the manager to open an issue** | | receipts/probes/domain-refused-path |
| 5 | RS1 ctrl_memory.py; RS2 SRP README | done (S2 taken in the README; S1 not taken) | `a7609d02` | |
| 6 | base merge if #810 round 30; one clean-clone gate pass | base unmoved before the pass (round 30 RR came after it started; not merged); gate pass once on `18300f6e`: section 4 | | receipts/gates, receipts/sweep |

## 4. The gate pass on `18300f6e` (once)

| Gate | Result |
|---|---|
| every `run:` step of rtl-fast/rtl/elaborate/docs, each job on its own clone (round 1's run_wf.py, verify_wf.py) | 139 rc 0, 226 not run with a reason, 0 bad (verify rc 0); 39 job/lane/harness trees clean after |
| full Verilator sweep, 4 shard units (native-shards.py) | 65 suites, 0 in-suite failures; 62 pass as run; gptp_shadow, gptp_tables, mbx failed only in their plant scripts (make's directory messages under the runner's `MAKEFLAGS=-j4`); re-run on shard 1's clone with CI's `-j4 --no-print-directory`: all pass, every plant caught (receipts/sweep/rerun-shard1) |
| firmware self-test and campaigns | PASS; control 696, AECP 227, SRP 398 (58 talker- lines = 29 x 2), 0 escaped |
| fw_coverage --check; TSN stack boundary; store gate | PASS (39 files); PASS; 455 tests |
| CPU budget harness, every arm, both points (harness_final.sh, compare_builds.py) | image loadable bytes identical to the R3 legs' builds; sample log byte-identical (cmp rc 0) per arm; every measured group regrades rc 0 |
| lane gates a/b/c | every rc equal to round 1's: all 0 but the three flip checks (rc 1 by design, as at the base); behave 508 scenarios |

Gate-pass incidents (mine, not findings of the head): `queue3.sh` first named the deleted `R2-*` legs for the harness
re-check (invalid, stopped, redone as `X-harness2-*` in `gates3h`); then the arm B spec lacked its graded-group field
(93 "no recorded script" refusals; redone as `X-harness3-B`). The `X-harness-*` unit rc files of 0 in receipts/gates/rc
are those superseded units' exits, not checks.

## 1. What changed in code (e0398c40)

- `srp_mbx.c` `declare_sources`: the withdrawal checks `mrp_mad_leave`'s result. Refused (lwSRP: the participant holds
  the MRPDU the ring refused, `mrp_mad.c` :968): the `talkers` bit stays (TALKER_DECL still shows it, as lwSRP still
  declares it), no hold-off starts, `done = false` so `sources_owed` owes it again. THE TRANSMIT's next call starts
  with no frame owed (`transmit_aged`), so its first declarations pass takes the Leave. Accepted: as before.
- `srp_bounds.h`: THE TRANSMIT's publications restated: IDLE_SLOPE and TALKER_DECL at most once a declarations pass,
  so at most twice on the interface the call builds; SR_DOMAIN once; LICENCE once a closed licence; at most
  5 + MBX_N_PUB_SOURCES an interface, within the reset's and the adoption's terms. `SRP_MBX_PUB_POLL_MAX` unchanged.
- Tests (`srp_talker.cpp`, 11 at both points): `TransmitPublishesWithinItsTermsAfterARefusedJoin` (one THE TRANSMIT
  call, source 0 lapsing with its licence open, source 1's join refused: TALKER_DECL and IDLE_SLOPE 2 on the built
  interface and 1 on the other, LICENCE 1, SR_DOMAIN 0); `RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt` (R835-1-F5's
  sequence: a peer Domain with a LeaveAll and an empty Domain, the pool exhausted, the ring full; the first pass's
  adoption refused, the reclaim before the build frees the empty Domain's block, the ring refuses the MRPDU, the second
  pass adopts and the Leave is refused; then the ring drains and the Leave goes on the wire, TALKER_DECL clear at its
  commit, no Advertise after it, the hold-off started).
- Plants: 29 in `srp_talker_mutants.py` (26 at `d023b77a` + 3), all caught at 8x8/2if and 1x1/1if on the worktree
  (receipts/plants/talker-if{1,2}-worktree.log). Four plants re-anchored (the withdrawal's lines moved into the Leave's
  answer); `srp_pub_mutants.REFUSAL_OWED` follows the comment's new words.

## 2. The Domain's leave/join on the same path (for a separate issue)

- Probe (not committed; `receipts/probes/domain-refused-path/probe-test.cpp`, run logs at both points): the F5 sequence,
  then 25 s of wire. The adapter records VID 3 adopted (`domain.vid` 3, nothing owed), but interface 0's MSRP Domain
  stays VID 2 on the wire (28 declaring events, no Leave) and VID 3 is never declared, at 1x1/1if and 8x8/2if.
  `change_domain` (`srp_mbx.c` `mrp_mad_leave(...DOMAIN...)` and `mrp_mad_join(...DOMAIN...)`, both `(void)`) loses both.
- Not the same mechanism, so not fixed here (the ruling's item 4 condition): the adoption reserves the new VID with
  `mvrp_declare` before the Leave, and after it withdraws the old VID, commits `i->domain`, publishes SR_DOMAIN and
  re-declares every source. Keeping it owed after a refused Leave leaves the reserved VID declared, and a Domain that
  changes again before the retry would leak it; a correct fix needs an ordering decision (reserve first, or THE
  TRANSMIT not re-entering the declarations of an interface whose build left a frame owed).

## 3a. The hot layout (found 06:3x; fixed by `17ac263f`)

- `e0398c40`'s legs (below, superseded) failed two stated costs at 1x1/1if by the head's graders: the registrar walk
  2,015 CPU cycles against `poll_grade.py`'s 2,000 (arm A `srp`; round 1 1,987), and a pass's polls' base 16,141
  against 15,500 (`answering-every-port` `notice-burst-5`; round 1 at most 15,078). `run.py` exits 1 on each
  (receipts/legs-e0398c40). Bounds may not change (assignment), so the layout had to.
- Cause: `declare_sources` is hot-listed (`ctrl_split_hot.txt` :185, `ctrl_split.ld` :181) just before
  `mrp_attr_visit`, `registrations`, `same`; the F5 fix grew it by one instruction (RV32, 4 B: 0x3b4 -> 0x3b8 at
  1x1/1if, 0x3a8 -> 0x3ac at 8x8/2if), moving every later hot function and all cold code by 4 B. The span comparison
  (receipts/legs-e0398c40/notice-burst-5-spans-...) shows the cost spread over `maap_mbx:poll` (+67 mean), `aecp_mbx:
  poll` (+56) and `srp_mbx:poll`.
- Tried (round2/scripts/variant.py, trial.sh): 15 behaviour-preserving rewrites of `declare_sources`; none -4 B at
  both points. `moved` (hot, just before it): `i->stale = i->stale || x` -> `i->stale |= x` (same value) is -4 B at
  both points; `nm` of both images against round 1's: only `moved`, `mvrp_declare`, `mvrp_attr_len`,
  `declare_sources` differ; every other symbol at round 1's address and size. `17ac263f`; images back to round 1's
  sizes exactly (receipts/rom/images-head.md); all legs re-run on it (R3-*).

## 3. Legs at `e0398c40` (clean clone r2/L), both points: SUPERSEDED by the R3 legs at `17ac263f`

| Leg | Groups | Refusals | Misses | Passes over the share | Least row margin | Round 1 | Base (#810 r29, base doc s13) |
|---|---:|---:|---|---|---|---|---|
| valid-destinations 1x1/1if (R2-W1) | 2 | 0 | 0 of 5 | 0 of 2,637 | 20.601 ms | 20.594 | n/a (new arm) |
| valid-destinations 8x8/2if (R2-W8) | 2 | 0 | 0 of 20 | 0 of 2,979 | 20.763 ms | 20.768 | n/a |
| answering-every-port 1x1/1if (R2-N1) | 16 | 0 | 0 of 280 | 0 of 19,505 | 8.986 ms | 8.826 | 9.080 |
| answering-every-port 8x8/2if (R2-N8) | 16 | 0 | 0 of 736 | 0 of 14,963 | 7.856 ms | 7.879 | 6.246 |
| arm B aecp 1x1/1if (R2-B1) | 1 | 0 | 0 of 25 | 0 of 110 | 19.708 ms | 19.720 | |
| arm B aecp 8x8/2if (R2-B8) | 1 | 0 | 0 of 39 | 0 of 130 | 19.432 ms | 19.571 | |
| arm A 1x1/1if (R2-A1, parts 0,1,3,4) | 94 | running | | | | 11.255 | 11.006 (7 of 945) |
| arm A 8x8/2if (R2-A8, parts 0,1,4-8,10) | 93 | running | | | | 9.733 | 8.973 (7 of 996) |

Wire (round 1's `wire_talkers.py` on the valid-destinations logs, receipts/sim): every check PASS at both points.

## Run history (this round)

- 03:45 assignment read; reviews, ruling, amended acceptance 4 read.
- 03:50-03:58 F5 fix and tests; the F5 test first missed the refused build (the join timer was running), fixed by
  waiting for an idle join timer; reviewer's sequence then reproduced at both points. Domain probe run and removed.
- 03:58-04:03 plants (29) caught at both points on the worktree; `e0398c40` committed; `fw_coverage.py --write` unit.
- 04:05 clean clone of `e0398c40` (r2/L); legs started (arm A in parts, valid-destinations, arm B, answering-every-
  port, both points); images at the head and at `b2d39235` (receipts/rom: +952 to +1,072 B rom).
- 04:10 coverage written (`0e2dd73d`); 04:12 two plant-table lines over 120 columns split (`d4ef6d4f`); 04:14 RS1,
  RS2, README/MAILBOX_SPLIT notes, section 5 (`a7609d02`). Base graders run at `b2d39235` (receipts/graders).
- 04:05-06:10 legs; CPU blocks scarce (another lane's legs hold 3-5 blocks): arm A's later parts split in halves and
  started as blocks freed; A8's last two halves' unstarted groups run as parts 8 and 10.
- Base `665-s2b-cycles` checked 03:50, 04:05, 05:39: `b2d39235`.
- 06:20 part 10 (A8 part 7's unstarted groups) found 4 of its 5 already started by part 7: its 4 duplicate Vsims
  stopped by PID (arguments listed first). 06:21 my de-duplicator (`round2/scripts/dedupe.sh`) then stopped part 7's
  live copies of the same 4 groups, because the stopped part-10 copies had left logs: my error. No group lost a result
  (merge takes only a completed log); the 4 groups re-run from the start as part 11 at 06:21 (about 5 min of work
  lost). The helper now requires the other copy running or complete.
- 06:3x merged A1 at `e0398c40`: STATED walk 2,015 > 2,000; N1's leg rc 1 (polls' base 16,141 > 15,500). Layout
  traced and fixed (`17ac263f`, 07:01). A8 at `e0398c40` merged: rc 0, 7 of 996, no STATED.
- 07:02 superseded scratch removed (my own, listed first): `builds/R2-A{1,8}/results*` (summaries in receipts) and
  round 1's first-pass `builds/F-*` (superseded by `F2-*`).
- 07:03 legs R3-* at `17ac263f` (clean clone r2/L2): arm A 1x1/1if in 4 parts, 8x8/2if in 5; W, N, B at both points.
  Images at `17ac263f`: round 1's sizes (+944 to +1,064 B rom over `b2d39235`).
- 09:43 gate pass on `18300f6e` started (`gates3`, round 1's `gate_queue.sh` jobs as `X-*` units, disp.py MAX 9).
- 10:02 my error: `queue3.sh` had been written before the R3 legs and named the deleted `R2-*` builds as the harness
  re-check's measured legs, so the four `X-harness-*` units compared and regraded against nothing (cmp rc 2, regrade
  94 refusals): invalid, not a finding of the head. The two still running stopped (`systemctl stop` of my own units,
  processes listed first); the invalid `F3-*` builds removed; corrected lines `X-harness2-*` (against `R3-*`, root
  `gates3h`, builds `F4-*`) queued first. The workflow and lane units are unaffected (they reference no leg).

## 5. For the manager (not done by this session)

- Push `895-talker-redeclare` at `18300f6e`; replace PR #901's body with PR-BODY.md.
- Open an issue for the Domain's own leave and join on the refused path (section 2; the probe's source and logs in
  receipts/probes/domain-refused-path). The ruling's item 4 routes it there.
- Still unfiled (R835-1's pending duty): the Domain adoption's in-place vlan_identifier change, a FirstValue change.
- Hosted exact-head contexts, act, the current-dev merge candidate, and acceptance 6 on the bench.
- Note for reviewers: `17ac263f` is a layout-only change in `moved` (same value); its reason is in section 3a and in
  `SPLIT_CONTROL_MEMORY.md` section 13 ("The hot layout holds those margins").

## 6. Run history, end of round

- 09:43-11:08 the gate pass on `18300f6e` (section 4); 10:07-11:19 the sweep; 11:20-11:32 the three suites re-run.
- 11:4x base check: `665-s2b-cycles` at `32551422` (round 30's RR at 10:10 CET, after the pass started): not merged.
- 11:5x REVIEW READY posted once (issuecomment-6850450637). No unit of this lane runs; the tree is clean at `18300f6e`.
