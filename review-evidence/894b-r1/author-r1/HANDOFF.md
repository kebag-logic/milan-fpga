# 894b-a781: #894's 8x8/1if follow-up (lane 894b), HANDOFF

**Status: STOP at head `c9226ff3a71777c8b92da17c8f839eb9a1dc5467`** (five commits on `8a3791e4`; not pushed). The comment text is `STOP-COMMENT.md`, posted on #894 as issuecomment-6871307898 at 04:55 CET. No REVIEW READY was posted. Started 00:20 CET 2026-11-14.

- Lane: `$LANES/894-8x8` (a link to `/data-2/milan/lanes/894-8x8`), branch `894-8x8-1if`, start head
  `8a3791e44533d6b1cc26d486d0b18e7d83470dc1` (#894 round 7's REVIEW READY head). Submodules as at that head.
- Authority: #894 issuecomment-6867393730 (the ruling), item (b). Also read: issuecomment-6867318907 (round 7's REVIEW
  READY), round 7's HANDOFF-r7.md and receipts, #872 issuecomment-6862464924 (the two-core trigger), #910.
- Nothing pushed. Comments allowed: one `[A781] TAKEN` (with the step-1 table) and one REVIEW READY or STOP on #894.

## 0. Exit

- **STOP on the two-core trigger as written:** measured 8x8/1if rows over their bound. Only `backlog-owed`'s seven
  egress rows are over, 61.83 to 64.20 ms, set by the scenario's 60 ms egress hold. They miss the same way at 1x1/1if
  (61.82 to 63.64 at `8a3791e4`) and at 8x8/2if, and section 13 records no CPU lever as moving them (tsn-c-stack#26).
  Whether they count is the maintainer's call.
- **Every row the CPU decides is within its bound:** AECP 3.743 (20), ACMP 5.588 (30), ADP 5.581 (30), MAAP 5.618
  (30), SRP 9.823 (90), MRPDU 31.653 (50) and notices 2.031 (20) ms. The load is 0.706 / 0.672 (0.75), the joins 186.298
  to 192.080 ms, the platform image 56.0 RAMB36.
- **Built:** the shape keying (item 2), 1x1/1if unchanged (item 3), and the 8x8/1if slice 1,475 us with builds
  1,475/1,795 us (item 4).
- **Left for a decision:** (1) whether the egress rows count toward the trigger; (2) the MRPDU row's harness budget,
  20 ms or 50 ms (2 budget misses at 31.65 ms); (3) `CTRL_LOOP_SRP_UNIT_US` per shape, 365 us at 8x8/1if (SRP slices up
  to 1,562 us against 1,475); (4) the harness's poll statements at 8x8/1if.
- **The full pass was not run:** the decisions change the head. Pre-checks: the firmware jobs at `93afe385`; the
  model, table, docs and style gates, the images and the harness self-test at the head.

## 1. Step 1: the model-only txL table at 1x1/1if, P = 6 to 11

Posted in the TAKEN comment, issuecomment-6867451690, at 00:24 CET (text: `TAKEN-COMMENT.md`; receipt
`receipts/model/txl-table-8a3791e4.txt`, script `scripts/txl_table.py`). Every P from 6 to 11 holds txL <= 50 with
R4L <= 240: txL 49.99 / 47.73 / 47.03 / 44.96 / 44.96 / 43.40; R4L 158.34 + 15 ms a step.

## 2. Design decisions (made public in the PR body and REVIEW READY)

- **Where the shape is stated.** The builder (`srp_arms.prepared`, used by both image builders, the harness and the
  SRP arms) already holds the interface count and the configuration. It writes the mailbox contract (`MBX_N_IF`) and
  the shape header `srp_entity_gen.h` (`CTRL_SRP_SOURCES`, `CTRL_SRP_SINKS`, the counts ADP advertises), force-included
  into every unit an image compiles. The boundary gate already calls it "the SRP builds' shape header". So the shape is
  (`MBX_N_IF`, `CTRL_SRP_SOURCES`, `CTRL_SRP_SINKS`): 1x1 is (n, 2, 2) and 8x8 is (n, 9, 9).
- **The table.** `ctrl_loop.h` lists each shape with its slice, build of both and build of one; any other shape
  hits `#error`. 1x1/1if keeps 900/1010/725, and both two-interface shapes keep 1300/1995/1215, so their images are
  unchanged. 8x8/1if gets its own row.
- **A compile with no shape header** composes no SRP and builds no image (the host arms, `ctrl_image.py`). It takes
  the shipping 1x1's streams as a default, the way the tracked contract defaults to one interface. A Python check
  holds that default to `srp_entity.py`'s output on the shipping config.
- **Arty configs** (5x5 and 1x2 streams) are now unlisted shapes. `srp_arms.all_shapes` builds SRP at every shipped
  config, so at those configs it now expects the build to be refused by the `#error`'s words. That refusal is the
  natural plant. They lose the SRP static-storage arm at those shapes, which is a consequence of the ruling.
- **The build of both at 8x8/1if** is never made on the built image: the slice holds one build
  (`CTRL_LOOP_BUILD_MOST` 1), so whole_grade's 'build' kind measures 0 at every point under THE TIERS. It must stay
  over the slice, or `BUILD_MOST` goes to 2 (a behaviour change). It must also stay under two builds of one, or the
  load's and rows' max() takes the both-branch and halves the per-build items. It is stated from the built image as
  the heaviest pair of one build's two build-one passes, plus 5 % (pending measurement).

## 3. Changes, with file:line and reason

- **`789d887e`, the keying:**
  - `sw/firmware/ctrl/loop/ctrl_loop.h:277-318`: THE SHAPES. `:291-297` takes the shape header's streams, or the
    shipping streams with none. `:298` is `CTRL_LOOP_SHAPE`; `:300-316` the four shapes; `:317` the `#error`. The slice's
    comment is `:261-276` and the builds' is `:361-368`. Why: ruling item (b); 1x1/1if keeps its values (byte-identical
    images).
  - `tb/verilator/ctrl_service_budget/shape_costs.py` (new): `listed` (`:63`), `at` (`:123`), `of_config` (`:140`),
    `of_point` (`:150`), `findings` (`:156`), `controls` (`:206`). Why: one reader of the table for every grader.
  - `slice_grade.py:35`, `whole_grade.py:30`, `poll_grade.py:121` (an owed MRPDU at the shape's build of one, where 725
    and 1,215 were typed): their `stated_us` take an int or a Shape. `grade.py:914-918` and `run.py:513`: a run is graded
    at its build's shape.
  - `rows_grade.py:117` (`header` keys the builds on the shape) and `:305` (`point_inputs` reads at the point's shape):
    the only rows_grade change.
  - `load_grade.py:245`: `macros` reads the builds at the shape. `rows_tiers.py:173` (`built_constants` at the point's
    shape) and `:881` (its slice control plants into the table).
  - `srp_arms.py:135-176`: unlisted configurations are held refused in the `#error`'s words (`refused`,
    `listed_shapes`). `ctrl_configs.py:259`: `shape_costs.py` named among the boundary gate's no-compile scripts.
  - `selftest_round.py`: the 8x8/1if slice, builds and owed-MRPDU checks; the shape checks registered. Six mutants in
    `selftest_mutants.py`.
- **`93afe385`:** `load_grade.py:108` (the 8x8/1if point), `:116` (`NEAREST`), `:298-325` (`shape`, `stated`);
  `flip_grade.py:56-60` (`FLIP` 0.75 at 8x8/1if, `POINTS`, `REPORTED`), `:143` (the table's controls), `:415` (its
  findings); the flip 8x8/1if mutant. Why: "the flip check holds both points".
- **`7405720e`:** the Python idiom gate. `rows_tiers.py` and `selftest.py` back within 1,000 lines
  (`built_constants` takes the point), and two lines wrapped.
- **`06147ff9`:** `shape_costs.findings` holds `BUILT` equal to `run.POINTS`, with its control.
- **`c9226ff3`:** FR_NFR 3.4.1 (the ruled 8x8/1if gate); SPLIT_CONTROL_MEMORY section 13 "THE SHAPES and 8x8/1if"
  (the table, the measurements, the findings, "Left for a decision"); the srp and harness READMEs.

## 4. New checks, planted mutants and failing words

| Check | Plant | Failing words |
|---|---|---|
| A shape not listed fails the build | the 12 arty SRP arms (3 configurations x 1, 2 interfaces x host, RV32) | `#error "THE SHAPES: the shape (MBX_N_IF, CTRL_SRP_SOURCES, CTRL_SRP_SINKS) is not one ctrl_loop.h lists"` |
| The table's rules | `shape_costs.controls`: 11 plants | e.g. "a slice of 1605 us, over the ruling's 1600 us"; "a build of both of 1450 us, not under two builds of one of 725 us, where its slice holds one build"; "1x1/1if: the builder states the shape (1, 2, 2), which ctrl_loop.h does not list"; "the model's points are built at ..., not at the harness's points'" |
| The harness grades at the image's shape | `shapes: the slice and builds keyed on the interface count alone (earlier rule)` | "THE TRANSMIT's builds at 8x8/1if are its shape's ..." |
| The slice at 8x8/1if is its shape's | `shapes: the slice held at the interface count (earlier rule)` | "a slice at 8x8/1if is held to its shape's length ..." |
| The passes given whole and an owed MRPDU at the shape | `shapes: a pass given whole held to its builds at the interface count`; `shapes: an owed MRPDU held to the interface count's build of one` | "THE TRANSMIT's builds at 8x8/1if are its shape's, a pass given whole held to them and an owed MRPDU to its build of one ..." |
| An unlisted shape is refused | `shapes: a shape not listed taken at the shipping shape's costs` | "the flip check refuses the table of shapes: a shape the table does not list" |
| The cap is the ruling's | `shapes: the slice cap not held` | "the table of shapes: the slice cap not the ruling's 1,600 us" |
| The flip check holds 8x8/1if at 0.75 | `flip: 8x8/1if held to a looser ceiling`; controls `an over-ceiling row at 8x8/1if`, `a row within its ceiling at 8x8/1if` | "the flip ceilings not 0.70 at 8x8/2if and 0.75 at 8x8/1if" |

## 4b. 1x1/1if unchanged

`receipts/images/images-start-8a3791e4.txt` and `images-head-c9226ff3.txt`: every 1x1 image (1if and 2if) and every
8x8/2if image has the same ELF and loadable sha256 at the start and at the head. Two clones at different paths agree,
so the images are path-independent. Only the two 8x8/1if images moved, at the same sizes.

## 5. 8x8/1if gate

`receipts/harness/gate-8x8-1if-93afe385.txt`, `builds-8x8-1if-93afe385.txt`, `legs-summary.txt`,
`egress-rows-and-1x1-save.txt`; the rows by every source in `receipts/model/rows-8x8-1if-head.txt`. Section 0 has the
outcome.

## 6. Gate table

| Gate | Where | Result |
|---|---|---|
| The table of shapes `--check --selftest` | head | PASS, 11/11 |
| Flip check at 1x1/1if; at 8x8/1if; at 8x8/2if | head | PASS (round 7's rows); PASS (0.706/0.75); exit 1 as reported |
| Flip, load and rows_tiers self-tests | head | 568/568, 25/25, 969/969 |
| `load_grade.py --check`, `tier_grid.py --point 1x1/1if` | head | 0.513/0.509 PASS; exit 0 |
| docs_check, em-dash, Python and C++ idiom, ctrl_hot, `git diff --check 8a3791e4` | head | 0 findings each |
| Every image, sha256 | head and start | 1x1 and 8x8/2if identical |
| The harness self-test | head (H-st) | 0 failures, 846 checks, 246 caught, 0 escaped; at m1 (pre-check) 0 failures, 246 caught |
| firmware-unit, firmware-boundary, firmware-srp-mutants (every step) | 93afe385 | every step 0 |
| Arm A at 8x8-1if, every group, and AL | 93afe385 | section 0 (exit 1: STATED and the egress rows) |
| The 1x1 save groups | 93afe385 | rc 0, 0 misses |
| The sweep and every hosted job | not run | waits for the decisions |

## 7. Run history

- 00:20 CET: start; read the ruling, round 7's REVIEW READY, HANDOFF-r7, the trigger and #910.
- 00:24: TAKEN posted with the step-1 table (issuecomment-6867451690).
- 00:3x: baseline images at 8a3791e4 on two clean clones at different paths, all identical
  (`receipts/images/images-start-8a3791e4.txt`).
- 00:4x: the C table and its readers in the working tree. Every 1x1 image (one and two interfaces) and every
  8x8/2if image is byte-identical to the baseline; only the two 8x8/1if ELFs moved, at the same sizes.
- 00:56: measurement clone m1 (8a3791e4 + the working diff). Started arm A at 8x8-1if (every group), the
  answering-ports leg (`aecp-largest-notice`) and the harness self-test. The first self-test hit a name clash
  (`at` in `grade.grade`), fixed.
- 01:00: the largest-notice leg at 8x8-1if, slice 1,475 us, passed: rc 0, no STATED, 0 budget misses, joins
  187.98 to 189.85 ms, build-one 95,074 cycles.
- **Found:** the answering-every-port arm can't build at 8x8-1if (its model holds 40 notices, not
  `AECP_NOTICES_MOST` 12). This predates the lane (round 6/7), so the queued-notice rows can't be measured there.
  Reported, not widened.
- **Found:** by the pair rule, 1x1/1if's build of both at its 900 us slice is 99,546 cycles (1,050 us), over its
  stated 1,010. That 1,010 is a single pass's measurement from an earlier slice, and no pass builds both now. 1x1/1if
  doesn't move (ruling (b)). Reported.
- 01:20: the `srp` + `datapath-events` leg at 8x8-1if, slice 1,475: build-one 140,273 cycles, the same as at 900 us,
  so 1,475 is a fixed point. The pair is 140,273 + 30,613 = 170,886, so the build of both is 1,795 us. Exit 1 on two
  STATED lines that are not slice or build costs: a walk item 4,829 > 3,500 and an SRP record's apply 29,720 > 28,000,
  the one-interface poll statements applied at 8x8/1if. These are reported, not keyed (outside item (b)). The 8x8/1if
  load already charges them at 8x8/2if's 60 and 365 us.
- 01:2x: commits `789d887e` (the keying), `93afe385` (8x8/1if in the load model and the flip check), `7405720e` (the
  Python idiom gate: module lengths, two long lines). The first two were split from one working tree without
  interactive staging, and their sum was checked identical to the saved diff.
- 01:26: arm A at 8x8-1if restarted at the code head `93afe385` on clean clone c1, in four parts (A0-A3, balanced by
  simulated time) plus the answering-ports leg AL. The first arm A ran on a dirty clone and was stopped: its reuse was
  refused because `ctrl_configs.py` changed under its build.
- 01:31: AL at 93afe385 rc 0 (identical figures to m1).
- 01:51: pre-checks at 93afe385 all pass: firmware-boundary, firmware-unit (the suite PASS, 12 arty arms refused by
  THE SHAPES' words, the store OK, coverage PASS on 39 files) and firmware-srp-mutants. Receipts follow in the full pass.
- 01:54: the harness self-test pre-check on m1 (the final Python): 0 failures, 844 checks, 246 mutants caught, 0
  escaped, the seven new ones each by its own words.
- 02:0x: `06147ff9` (`shape_costs` holds the model's points to `run.POINTS`, 11 controls).
- 03:05-03:10: arm A parts A1-A3 at 93afe385 ended rc 1. 74 groups graded (with AL), 736 instances:
  - **no instance over the ruling's bound:** AECP 3.74 (20), ACMP 5.59 (30), ADP 5.58 (30), MAAP 5.62 (30), SRP 9.70
    (90), MRPDU 31.65 (50) and notices 2.03 (20) ms;
  - **2 budget misses:** `save-held.mrpdu.join.if0` 31.653 ms and `save-starved.mrpdu.join.if0` 31.637 ms, against
    the harness's budget for the row of min(T_svc 20, the srp ceiling) = 20 ms. The ruling's and FR_NFR 3.4.1's
    MRPDU bound is 50 ms. **A conflict between the gate's "0 budget misses" and its "MRPDU 50 ms".**
  - joins: 228 in 73 groups, 186.298 to 192.080 ms;
  - **tier-2 slices of SRP's records over the stated 147,500:** up to 156,198 cycles (1,562 us), in backlog-adp
    groups. The cause is `CTRL_LOOP_SRP_UNIT_US` keyed by `MBX_N_IF` alone: 250 us at one interface, while an SRP
    record at 8x8/1if takes up to about 337 us with its handler (its apply 32,023 cycles). The overrun is R - 250 us
    whatever the slice, so it existed at 900 us too (unmeasured then). The fix is the 8x8 shape's `record.srp`,
    365 us. That would be a behaviour change at 8x8/1if beyond the ruled constants, so it was not made: a decision;
  - **STATED polls at 8x8/1if over the one-interface statements:** base 22,478 > 20,500; walk 4,829 > 3,500; an SRP
    record's apply 32,023 > 28,000; rebuild 56,003 > 29,000; withdraw 10,238 > 9,000. The 8x8 shape's two-interface
    statements, which the 8x8/1if load charges, bound each. Keying them is outside item (b): a decision.
- 04:1x: read the two rulings that arrived during the lane. Round 8 (issuecomment-6867990126, 00:56 CET) item 6:
  lane 894b takes 49 and 238 ms after #902 merges, re-measures 8x8/1if's command pass against its ledger, and checks
  1x1/1if byte-identity against #902's merged head. Round 9 (issuecomment-6870437042, 03:46 CET): this lane picks it
  up by merge after #902 merges; its direct map index is sized from build-time shape constants. Neither changes this
  lane's bounds before the merge. Under round 8's figures the measured MRPDU row (31.653 ≤ 49) and joins (186.298 to
  192.080, within 181.0 to 239.0) hold.
- 03:25: S1, `save-held` and `save-starved` at 1x1 at 93afe385. This shows whether the 20 ms MRPDU budget is stale
  under THE TIERS at 1x1/1if too (round 7's full pass ran no save group).
- 04:55: the harness self-test at the head: 0 failures, 846 checks, 246 caught, 0 escaped. Rechecked #894: no comment since
  round 9's ruling. The tree is clean at `c9226ff3`. **STOP posted, issuecomment-6871307898**, the lane's second and last
  comment. Nothing was pushed. The units still running: none of mine.
