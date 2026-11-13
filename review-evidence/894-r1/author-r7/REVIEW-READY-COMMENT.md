[A773] REVIEW READY
Commit: 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 (`894-tiers`, 20 commits on `ccb47e39`, the merge of dev-soft-core `cec88385`; not pushed)

**1x1/1if holds every row by every source** under #908's cuts and the contingent ruling (issuecomment-6858269025) with its amendment (issuecomment-6862465874). Nothing went back to the owner. **8x8/1if is a STOP** on its per-point slice; by ruling item 6 that does not hold back 1x1/1if. #908 stays open.

**Rows at 1x1/1if, by every source** (`flip_grade.py --check --point 1x1/1if`: PASS; slice 900 us, P = 6 ms, join timer 19 cs):

| Row | ms | Original bound | Bound now | Moved by |
|---|---:|---:|---:|---|
| R4 | 12.82 | 20 | 20 | |
| R4L (paced) | 158.34 | 240 | 240 | |
| ACMP | 28.35 | 30 | 30 | |
| ADP | 26.76 | 30 | 30 | |
| MAAP | 26.88 | 30 | 30 | |
| first queued notice | 14.50 | 20 | 20 | |
| R5 | 72.71 | 90 | 90 | |
| R6 | 68.62 | 90 | 90 | |
| last queued notice | 125.84 | 125, **over** | 130 | the amendment (the row rounded up to the next 5 ms) |
| tx | 29.78 | 40 | 50 | item 3 (240 less 19 cs) |
| txL | 49.99 | 40, **over** | 50 | item 3 |

- **Loads:**
  - 1x1/1if: 0.513 at the pin and 0.509 with tsn-c-stack#32, against 0.70 (`load_grade.py --check`).
  - 8x8/1if (derived): 0.698, against 0.75.
- **Images:** within their caps (1x1/1if: fixture 40.5 and platform 42.5 RAMB36, cap 56; 8x8/1if: platform 56.0, cap 56; 8x8/2if: fixture 59.0, its ledgered cap, and platform 60.0, cap 60.5).
- **Margins:** txL holds by 0.01 ms and the last queued notice by 4.16 ms.

**The cuts came first (#908; item 1):**
- **Lever (a): ACMP's item is itemised.**
  - The send is 50 us and a declined offer 20 us at 1x1/1if.
  - Declines are at most 2 a send + 1. The firmware's proof is `acmp_mbx.c:111-128`, `:157-175` and `:186-187`; the plant `acmp-redelivered-every-poll` is caught.
- **Lever (b): the polls' base growth is attributed.**
  - The register read accounts for 2 cycles and the hot list for 203.
  - About 4,400 cycles are data-cache stalls: KLJ3's 552 B `nvm` sits on SRP's state's sets.
- **Lever (c):** three placements were tried; none was taken. Each moves the conflict onto THE RETRY's rounds and AECP's item, whose costs the loop schedules by.
- **After the cuts:** txL was 46.58 ms at P = 8 and over 40 at every P to 13; the last queued notice was 135.64 ms.

**The moves.** Each is its own commit amending FR_NFR 3.4.1 and citing the ruling:
1. **The join timer at 19 cs** (`158265c2`). `CTRL_LOOP_JOIN_CS 19u`; `CTRL_LOOP_TX_BOUND_MS` is `(240u - 10u * CTRL_LOOP_JOIN_CS)`, derived and never typed. lwSRP is configured from `SRP_JOIN_CS = CTRL_LOOP_JOIN_CS`, so lwSRP is unchanged.
2. **THE PACE at 6 ms** (`1560e4f4`): the smallest P that holds txL with R4L ≤ 240.
3. **The slice at 900 us** (`dec9f1d7`): the slice ruling's own rule (`rows_tiers.ruled`), applicable once every row holds.
4. **The last queued notice at 130 ms** (`8cf7e2b7`; the amendment). Its row after the cuts is 125.84 ms. `AECP_QUEUED_MS` states 130 at 1x1/1if, and `queued_bound.py` derives it and refuses any other statement (three plants).

**A refuted stated cost, restated** (`7290f0f3`). This is the row behind move 4.
- At a slice that holds one MRPDU's build, the `srp` group's build after its Listener Ready makes its declarations in the first MRPDU's pass: 68,951 cycles at 1x1/1if, against the stated 430 us.
- It is refused at this branch's start `ccb47e39` too (the `srp` group at 1x1), so it predates this round.
- By the +5 % rule, `CTRL_LOOP_BUILD_ONE_PASS_US` is 725 us at 1x1/1if, and an owed MRPDU (`poll_grade` mrpdu) follows it by its documented rule. That moved the last queued notice from 117.19 to 125.84 ms and txL from 49.70 to 49.99.
- At 8x8/2if the same build is 147,613 cycles, 1,550 us by the rule, over the 1,300 us slice it must fit (`ctrl_loop.c:201`). 8x8/2if's 1,215 us therefore stands, refuted, with its reported rows. **This needs an owner decision and a new Issue** (I may not open one).

**Join intervals (item 4).**
- `join_grade.py` reports each group's shortest and longest (`JOINS` lines) and fails a run with one outside 180.0 to 240.0 ms (six planted defects caught).
- **Definition:** an interval ends only at an MRPDU that a join timer's run-out released (`mrpdu_grade.released`). lwSRP arms the timer at a commit and nowhere else (`mrp_mad.c:1540`), so a request after an idle run-out sends at once and ends no interval. The first definition counted those, and the `srp` group showed it at 715 to 783 ms. The corrected one is `0ab4e574`, with a planted defect for the earlier rule.
- **Measured at the head:** 52 intervals in 14 group runs over 1x1, 8x8 and 8x8-1if, the `srp` group included, 185.668 to 190.025 ms (1x1: 188.036 to 190.025); no run has one outside the range.
- **Owed:** the flip check's bench capture of the join intervals on the wire. This round may not use hardware or the bench, so someone with bench access must take it. No capture was made, so none is outside the range.

**8x8/1if (ruling item 6): STOP on "the per-point slice built".**
- `ctrl_loop.h` states the slice and the build costs by `MBX_N_IF` alone, and `rows_grade.py` (closed this round) reads them that way. Where the shape is stated is a decision.
- Held: the load (0.698 derived, against 0.75) and the platform image (56.0 of 56 RAMB36).
- Reported only (owed to #872): the derived rows by every source (R4 19.12, last 395.65, txL 199.96 ms) and the harness's 8x8-1if legs (`aecp-largest-notice`, `datapath-events` and `srp` exit 1 on build-one passes of 93,175 to 140,273 cycles against the one-interface 72,500, over the 900 us slice; the answering-every-port arm refuses to build there, its model holding 40 notices, as in round 6).

**Twin.** Three plants' words carried the split's MRP times at 20 cs (200→190, 212→200, 31012→31010 ms). They are restated (`f02457a6`), and each is refused by the same finding. `make twin` and `make twin-plants` pass.

Changed (the round's commits after the levers):
- `ctrl_loop.h`: `CTRL_LOOP_JOIN_CS`, `CTRL_LOOP_TX_BOUND_MS`, the 900 us slice, the 725 us build of one.
- `aecp_mbx.h`: `AECP_PACE_MS 6u`, `AECP_QUEUED_MS` 130 at 1x1/1if.
- `srp_mbx.c:29`: `SRP_JOIN_CS`.
- SRP tests that derive the JoinTime (`18e14164`), and two more timed from it so their planted defects fail them by their own words (`5cbebb80`).
- The TSN stack boundary gate's list names `queued_bound.py` (`8a3791e4`).
- The harness:
  - `join_grade.py` and `queued_bound.py`, both new;
  - `mrpdu_grade.released`;
  - `rows_tiers.bounds_at`;
  - the flip check's statements and controls;
  - the self-test checks and mutants.
- Docs: FR_NFR 3.4.1, SPLIT_CONTROL_MEMORY section 13 (a new "The contingent moves" subsection), and the srp, harness and twin READMEs.

Validation, every hosted job's steps run locally at the head on a clean clone, never piped:
- **The sweep** (`scripts/run_all_suites.sh`) ran as four shards, each on its own clean clone: every shard exit 0; 65 suites, 2,713,040 checks, 0 failures.
- **Every hosted job step** of rtl-fast, rtl, elaborate and docs, replayed locally on a clean clone and checked step by step: 139 steps run, **0 bad**. 226 were not run, each with its stated reason (the hosted context, or tools this host already carries at their pins).
- **The firmware jobs** pass: the unit, control, AECP and SRP mutation campaigns, the TSN stack boundary, and Verilator.
- **The lane's gates:** 43 exit 0. These include:
  - the harness self-test (0 failures; 239 mutants caught, 0 escaped);
  - `flip_grade.py --check --point 1x1/1if` (PASS) and `tier_grid.py --point 1x1/1if`;
  - rows_tiers 969 of 969, flip 555 of 555 and load 25 of 25;
  - `load_grade.py --check`; the em-dash, idiom, docs and diff-check gates; `ctrl_hot`;
  - the boot gates and their plants; the BDD suite (511 scenarios); the builder tests;
  - `make twin` (0 findings) and `make twin-plants` (every plant refused).
- **Four lane gates exit 1 by design** (8x8/2if is reported): `rows_tiers.py --terms`, `flip_grade.py --check`, `--point 8x8/2if` and `--design as-built`.
- **The CPU budget harness** at the head, 15 legs on a clean clone:
  - every 1x1 leg exits 0 (`datapath-events`, `notice-every-0`, `aecp-largest-notice`, `backlog-owed`, `srp`), and the plant control `acmp-redelivered-every-poll` is caught;
  - 8x8/2if exits 0 in four groups; `srp` exits 1 on the refuted build of one (above);
  - the 8x8-1if legs exit 1 (reported, above).
- **The first full pass, at `11c586a8`, failed two steps.** The TSN stack boundary refused `queued_bound.py` as unlisted, and two SRP mutants escaped their failing words at 19 cs. `5cbebb80` and `8a3791e4` fix them, and this pass is at the head with both fixes. Both passes' records are kept.

Acceptance criteria:
- **Ruling item 5 (1x1/1if): met** under the contingent moves, by every source.
- **Item 6 (8x8/1if): not met (STOP).** The load and the image hold; the slice is not built.
- **#908:** levers a and b are met; c was tried with none taken. It stays open (item 6 of the contingent ruling).

Open risks/questions:
1. **The 8x8/2if build-one statement is refuted** (above) and needs a decision.
2. **txL's margin is 0.01 ms**, so any re-measure that raises a txL term moves it over 50.
3. **The bench capture of the join intervals is owed.**
4. **8x8/1if's per-point slice is a decision.**
