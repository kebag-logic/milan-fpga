# RESOLUTIONS: the flip train's composition, round 5 (#665)

Round 5 rebuilds the provisional step 10 on the final head. Conventions are round 1's. "Train" is the step-9 branch
`flip-train-1117` at `ed5855fe` (step 9, round 4's cut and ledger). "PR" is #944's frozen head `d1aa4c44` (R861-2 and
R862-2 POSITIVE; its GitHub head checked), fetched from its lane.

`flip-train-1117-p10` is rebuilt from `ed5855fe`, as the manager asked. Its round-4 tip `25299527` is kept as
`refs/ref/p10-r4`. Nothing is pushed.

## Step 10 on the frozen head: merge `49f005b9`, fix `082d0037`

Merge base `70f4056f`. The delta `7cfb8a04..d1aa4c44` is 6 commits:

- the talker-notices harness arm;
- the owed-output report in SRP's taken pass;
- residues;
- ledger and plant re-anchors;
- the Python size moves.

13 files conflicted; git's recorded resolution of round 4 settled `tb/verilator/milan_dp/Makefile`. #944 moves no
submodule, and the index kept the train's gitlinks (`gptp-processor` `1616fc8f`, `protocol-processor` `801ef228`),
staged by path.

| File | Resolution | Why |
|---|---|---|
| `sw/firmware/ctrl/test/aecp_mutants.py` (2) | both imports, both module splices (the train's `aecp_face_mutants`, #936's `aecp_notice_mutants`) | #936's last commit moved its notice plants into `aecp_notice_mutants.py`; round 4's own module of that name is not on this branch |
| `sw/firmware/ctrl/test/test_aecp.cpp` | both | independent tests |
| `tb/verilator/ctrl_service_budget/build.py` (2) | the train's `observers` and #936's `talker_notice` (which replaces the base's unused `talker_window` import); both plant tables | as each side |
| `tb/verilator/ctrl_service_budget/run.py` | the train's `talker_window.groups(point, spec)`, then #936's talker-notices branch | the train's groups take the build for the held group; #936's do not |
| `tb/verilator/milan_dp/twin_compare.py` (2) | round 4's resolution, with #936's owner of the dest-MAC row, #943 | as round 4 |
| `tb/verilator/milan_dp/README.md` (3) | round 4's composed text, the owner #943, sixteen plants | as round 4 |
| `tb/verilator/ctrl_service_budget/README.md` | the train's | the fixture's planner entry is 60.5 on the train |
| `docs/design/SPLIT_CONTROL_MEMORY.md` (6) | the train's, with #936's own "At #936's head" table (round 4's choice) | as round 4 |
| `sw/litex/ctrl_memory.py` (5), `ctrl_memory_ledger.py` (6), `test_ctrl_memory.py` (2) | the train's, to be restated to the measured images at the final tip | an entry is its image's measured tiles |

**Fix `082d0037`.** The union put `run.py` at 1,013 lines (the train's 947 and #936's additions), one long module
past the idiom gate's ratchet. #936's talker-notice plants' verdict (`declared_verdict`, 22 lines) moves into
`talker_notice.py`, #936's own module, its body unchanged; `run.py` calls it there and is 994 lines.

## The hot list (ruling item 1)

The filter (receipts/hot/tools/filter.py) reads each served image's link map: its linked `.text.<function>` sections. The
served images are the split images `ctrl_srp_image.py` links and holds to the list with ctrl_hot's LINKED rule: the
size fixture at 1x1/1if, 8x8/1if and 8x8/2if in each of the six arms, each as itself and as the SoC plan's stand-in
and mapped images, 54 maps. The target platform's image (`ctrl_plat_image.py`) links the same script but is not held
to it: the old list's fixture-only entries never linked there. Counting it as served would also drop the fixture's
`ctrl_aecp_image` functions and `ctrl_loop_run` (five entries); that reading was not taken.

- `b5802de9`: traced at `082d0037`, 269 functions; 267 kept, `aecp owe` and `aecp owed_drain` dropped.
- `68c97849`: re-traced on attempt 2's notice cut (`26f30fea`); the same 267 entries, 70 lines reordered.

- `41d2bc2b`: re-traced on the listener cut (`08c28218`); 266 entries. `acmp_listener_registered` no longer runs in
  the windows' passes, so it leaves the list.

## Attempt 2: the cuts (ruling item 2), each on the step-9 branch and carried onto p10

| Step-9 commit | p10 commit | What | Wire behaviour |
|---|---|---|---|
| `067c319d` | `26f30fea` | AECP's notice fan-out: a buffer's source MAC is stored only when its interface changes; the port's calls, context and the registration's sequence_id are read once | none: every frame's bytes are the same |
| `0bc158a7` | `3e1c3dd9` | `CTRL_CC_INLINE` (GNU always_inline, plain inline otherwise) in `ctrl_cc.h`; `mbx.c`'s transmit commit and `mbx_dma.h`'s record-mover wait inline in `mbx_tx_begin`; the header included outside `CTRL_MBX_BASE` (the host and twin builds) | none |
| `7b3c1c94` | `08c28218` | SRP's delivery calls `acmp_listener_registered` only where ACMP's flag differs from the presence (the call sets that flag and nothing else) | none: ACMP's state is the same at every point |
| `112ab9b1` | `6448e431` | the DMA driver test T8: a word-loop record committed by the next begin while an earlier move's ERR is held (the arc the inline commit adds; the coverage ratchet) | test only |

Re-anchored, not removed: `aecp_fan_mutants.py`'s `notice-source-of-the-first-interface` and
`notice-sequence-low-byte-unwritten`, and `poll_items.py`'s `FAN_NOW` (the walk `notice-fan-out-as-it-was` replaces).
`hooks.py`'s anchor is kept by placing the read-once declarations before `unsigned k`. The merges carrying the cuts
onto p10 (`26f30fea`, `3e1c3dd9`, `08c28218`, `6448e431`) are clean.

Rejected: the paced record's echo inline (measured worse on the same list, its placement outweighing the call).

## The ledger at the final tip: `bf2c1184`

The merge composes #936's 64 B of `ctrl_plat` at 1x1/1if and 8x8/2if (each side alone had its own measured value), and
the cuts with the relearned list take the platform's 8x8/1if image to 137,472 B of `rom`, 256 B past the 137,216 B
that 57.5 holds. `bf2c1184` restates `ctrl_memory.LEDGERED` and `ctrl_memory_ledger.py` to the measured images
(`ctrl_plat` 18,048 / 19,712 / 18,944 / 21,568 B; the 8x8/1if entry 58.0, S14 debt of 2.0 by the owner's rule of
2026-11-15), with its test, the boot README and the design document's ledger and fit text. `plat_ledger.py --self-test`
PASS at four points with 9 of 9 controls, the fixture in six arms within its 60.5, and `test_ctrl_memory` PASS.

## The measurement (HANDOFF-r5.md has the figures)

Each head is measured as round 4's: the formal measurement's legs (arm A in eight parts, answering-every-port in two,
the answering-ports arm's held groups in two, valid-destinations in three), each on its own clean clone, then the
statement survey and `record_classes.py` (receipts/measure).

| Head | What | Measured |
|---|---|---|
| `b5802de9` | the final head as ruled, before the cuts | 8x8/1if's valid-destinations and answering-ports arms; the other legs stopped at 06:23 |
| `68c97849` (A) | the notice cut, re-traced | the answering-ports arm at three points; the rest stopped at 06:15, superseded by B |
| `41d2bc2b` (B) | both cuts, re-traced; the p10 tip `bf2c1184` links its images | every leg at three points |
| `b4f9f26c` (scratch) | B's code with `082d0037`'s list and link script | `srp-talker-held` at three points (ruling item 3) |
| `21486e00` (N, scratch) | B's code with its traced list unfiltered (268) | `srp-talker-held` at 8x8/1if; every leg at 1x1/1if |
| `dd5f60e0` (NU, scratch) | N with the 8x8/1if SRP unit at 375 us | every leg at 8x8/1if |
| `40a6c1a5` (U, scratch) | B with the 8x8/1if SRP unit at 375 us | stopped at 07:27, moot once B's base was known |

The scratch commits exist only in their clones; none is on a lane branch.

## The restatement at the final tip: `7a536fc5`, `0cfe1ddc`

B's traced costs over their statements are restated by the unchanged rule (the most measured plus 5 %, rounded up to
5 us) in `0cfe1ddc`, from the survey by `receipts/regrade/spec_from_survey.py` and `commit_restate.py`, each table's
comment carrying its measurement:

- 1x1/1if: the paced class's one-row edit 310 (29,331 cycles);
- 8x8/1if: the polls base 300 (28,417), the apply 375 (35,350) and the MAAP record 180 (16,682);
- 8x8/2if: the MAAP record 160 (14,770), a pass's events' fixed part 45 (4,069) and AECP's timer event 120 (11,404,
  traced to `arm()`'s walk first).

8x8/1if's `record.srp` (35,547, 375 by the rule) is left at 365. `load_grade.py` holds it to the header constant
`CTRL_LOOP_SRP_UNIT_US`, and ruling item 2 rules out moving one; the table's comment says so. Arm A's legs were still
running at that commit, so if they raise anything, a further commit restates it.

**`7a536fc5`: the restatement made one planted control vacuous, so it is re-anchored, not removed.** `rows_tiers.py
--selftest` refused 1,032 of 1,033 controls with the restated tables. The escaped one, `edit_rows`' "an unpaced
SET_CONFIGURATION charged as ordinary", plants the paced class's record at the one-row edit's alone and expects it to
leave the dearer member out. At 1x1/1if the one-row edit is now measured past SET_CONFIGURATION (310 against 305), so
that plant moves no figure there and no gate could refuse it. The control now plants at 1x1/1if while SET_CONFIGURATION
is that point's dearer member, and otherwise at the first point where it is: 8x8/2if, where the plant shortens ACMP's
row from 69.22 to 67.30 ms. It is refused in both orders (checked in memory with the one-row edit at 295 and at 310),
and on both commits `rows_tiers` refuses 1,033 of 1,033.

## The candidate after RULING-1118b: `3cdc613b`, `0b054867`

- **`3cdc613b`.** In `ctrl_loop.h`'s 8x8/1if block, `CTRL_LOOP_TX_MS` 77 (item 2a: B's tx row of 76.81 rounded up)
  and `CTRL_LOOP_SRP_UNIT_US` 375 (item 2b). In `load_grade.OWN`, 8x8/1if's `record.srp` 375, with its measurement
  in `OWN_MEASURED` (35,547 cycles, `srp-talker-held`). The header's comments say why. `load_grade.py --check` (its
  `srp_unit`) holds the unit to that record. `flip_grade.py --check --point 8x8/1if` passes on B's figures (76.81
  within 77, the load 0.744). The plant sets (load 28/28, flip 616/616, rows_tiers 1,033/1,033, record_classes 20/20,
  shape_costs 25/25) are refused.
- **`0b054867`.** The prose that quotes the restated figures in force: `FR_NFR.md` (8x8/1if's THE TRANSMIT figure and
  the 1x1/1if paced class), `SPLIT_CONTROL_MEMORY.md` (the SRP unit and the 8x8/1if TRANSMIT bullets) and the SRP
  README (the unit). History sentences stay as history. The doc gates pass.
- **The images.** Each arm's `ctrl_app.elf` at the candidate equals U's (`40a6c1a5`, B's tables with the unit at
  375) at 8x8/1if and B's at 1x1/1if and 8x8/2if, sha256 by sha256. `CTRL_LOOP_TX_MS` enters the image only through
  `SRP_REDECLARE_CS`'s `(TX + 9) / 10`, 8 at 75 and 77, so U's image, measured with 75, is the candidate's.
- **The host tests reading the figure.** `srp_talker.cpp` passes at 1x1/1if, 8x8/1if and 8x8/2if, 16 tests each
  (8x8/1if run in addition to the suite's two shapes).
- **`c8ff391a`: a self-test check re-anchored.** `run.py --self-test` failed one check at `0b054867`. The check held
  8x8/1if's `record.srp` equal to 8x8/2if's, the nearest-point premise that item 2b replaces for the SRP record. It now
  holds every 8x8/1if record and event at 8x8/2if's, raised to 8x8/1if's own where OWN states one. That covers 11 keys
  where it checked one, and it fails when OWN and the stated cost disagree (checked in memory). `run.py --self-test`:
  0 failures. Only harness Python changes; the images do not.

## Step 11: #939 (#927) on the candidate, `flip-train-1117-p11` at `3e908539` (RULING-1118c)

#939's frozen head `0297a19a` (its lane's branch `927-8x8-timing` and the GitHub head agree) is merged `--no-ff` onto
the candidate `c8ff391a` in a scratch clone. The new branch `flip-train-1117-p11` is fetched into the lane repo, so the
measured candidate's branch is untouched. Merge base `70f4056f`; #939's delta is 20 files and moves no submodule. The
gitlinks stay `1616fc8f` / `801ef228`.

| File | Resolution | Why |
|---|---|---|
| `tb/verilator/milan_dp/README.md` (2 hunks) | the union: "thirty-one defects", with the train's sentence on #839's transmit gate and #927's on the `EDIT` record's capture-source word | the base plants 26, the train adds 2 (#839) and #927 adds 3; the auto-merged `split_mutants.py` holds 31 arms (26 / 28 / 29 at base, train and #939) |

Everything else merges clean. `sim_split.cpp`, `split_mutants.py` and `tb_split_top.sv` auto-merge.

## The CPU pass and the final step-10 candidate: `4374cc27`

U's 8x8/1if measurement over every arm (the image that carries the unit at 375 us, hash-equal to the candidate's)
holds every test of RULING-1118b item 2b; HANDOFF-r5.md has the table. One statement was over: ADP's record, 12,779
cycles in arm A's `backlog-adp-refill`, 135 us against OWN's 130, as on B's image. `4374cc27` restates it by the
unchanged rule, with its measurement in `OWN_MEASURED`. The restatement made two `load_grade` own-record plants miss
their names, because their expected messages hard-coded "130 us". Both now read the measurement's figure from
`OWN_MEASURED` through `rule_us`, so a restated measurement moves the control with it. 28 of 28 are refused, before
and after. The load stays 0.744 and THE TRANSMIT's row 76.81 ms of 77. The images do not change.

## Step 11 carried: `74481d2e`

`4374cc27` is merged `--no-ff` onto `flip-train-1117-p11` (clean; only `load_grade.py`), so p11 is `74481d2e`: the
candidate plus #939. p11's RTL and images are `3e908539`'s, so its routes, image hashes and confirmation runs stand
for it.

## The preflight fix: `05dc1791`

The candidate preflight refused `74481d2e` on `git diff --check`: "sw/firmware/ctrl/test/plat_mutants.py:581: new
blank line at EOF". The line came in with `6ad5c259`, round 2's composition fix to THE STEP's plant. `05dc1791` drops
it and nothing else, so `git diff --check origin/dev-soft-core...HEAD` prints nothing over the whole train; it had no
other hit. The file is Python only, and the 12 split firmware images are hash-equal to `3e908539`'s. The docs, idiom
and hygiene checks pass. p10 carries the same line; the fix was asked for on p11 only.

## The release record (RULING-1118d, #665 issuecomment-6979461559): STOP at item 2, no commit

The ruling accepts a record-only re-baseline of the resource gate's release route endpoint at the final head, once the
release image's delta is explained by hierarchy from the existing routed checkpoints. It stops if any release CDC FIFO
changed primitives. The two routed checkpoints compared are the candidate `c8ff391a`'s release route and p11's, both
on ExtraPostPlacementOpt (`receipts/step11/release/hier-diff.txt`).

| Instance | Candidate | p11 | Step 11's RTL |
|---|---|---|---|
| `KL_tdm_render_master`'s `u_fcdc` (`cdc_pair_fifo`, WIDTH 192, LOG2D 2) | 3 RAMB36E1, 24 flops | 32 RAM32M (128 LUTRAMs, named `milan_datapath/u_fcdc/g_mem.mem_r_reg*`), 216 flops | #927's `DIST_RAM_P = 1` |
| `KL_tdm_capture_master`'s `u_tcdc` (`cdc_pair_fifo`, default branch) | 34 LUTRAMs, 82 flops | the same; logic LUTs 32 to 21 | the storage block's reorder, behaviour-identical |

`u_fcdc` changed primitives and its flop count. That is the stop condition, so the record is not moved and no commit
is made. #927's comment gives its reason as a fast-corner hold of +0.014 ns on the block RAM's write data. Whether the
move is accepted for the release image is the pending decision. The rest of the delta is in HANDOFF-r5.md's status:
the meter +41 LUTs and -18 flops; the EDIT claim registers +96 flops; about +238 LUTs in modules whose RTL is
unchanged.

## RULING-1118e (#665 issuecomment-6979996755): the CDC check, STOP at item 3, no commit

The ruling resolves the 1118d stop (the render crossing's move to distributed RAM is #927's, reviewed, and shared by
every image that carries the render master, so not split-only). It asks for one check before the record moves: the
new storage-to-read-register crossing covered by its timing exceptions and clean in the CDC report. The check ran on
the existing routed checkpoints: p11's release ExtraTimingOpt and both split images' best routes, plus, for
comparison, the candidate's block-RAM release route (`receipts/step11/cdc/fcdc-summary.txt`). The crossing is covered
(Asynchronous Clock Groups, slack inf), but `report_cdc` reports it as CDC-15, Warning, on its 192 read-register bits
at release and 1x1/1if. Vivado counts those endpoints Safe, and the base's unchanged `u_tcdc` carries the same rule on
50. The 8x8/1if image carries no render master. A flag is the ruling's stop condition, so no record-only commit is
made. The wording item found no train doc or comment calling the option split-only; the PR body's step-11 row and
route note, and the handoff, now say it is shared.

## RULING-1118f (#665 issuecomment-6981065172): the re-baseline, `73272666`

The ruling reads "flagged" in 1118e item 3 as unsafe, unknown, Critical or unconstrained. None applies: the clock
groups cover the paths, the report counts 201 of 201 Safe, and there is no CDC-26. CDC-15 is the expected report for
the gray-pointer LUTRAM FIFO, and no waiver goes into the train. `73272666` is the record-only commit:

- `pp_resource_gate.py record … --write` on p11's three release routes, the record equal to the dry run's;
- the endpoint's `measured` note restated with the rulings, the head and the attribution;
- no other file.

The gate check exits 0, `check-baseline` and the self-tests pass, the docs, idiom and hygiene checks pass, `git diff
--check` is empty, and the 12 split images are hash-equal. `AREA_BUDGET.md`'s utilisation table and the #234 findings
page still quote the previous record; the ruling keeps the commit record-only.

## The documentation audit: `b1f1161b`

The train candidate's builder found `docs/DOCUMENTATION_AUDIT.md` stale (`docs_inventory.py --check`). #934 (step 9)
brings the inventory and its page, fresh at its own head `544fd72c`. The step-9 merge `8f6fbb84` unites it with steps
1 to 8, whose pages it never inventoried, so it is the first stale commit; step 10's merge adds one line more
(`receipts/step11/docs/audit-bisect.txt`). The page is generated, so it changes only through its generator:
`docs_inventory.py --write`, one file, docs only. It lists #881's `tb/verilator/ctrl_reboot/README.md`, restates six
pages' cited paths, and updates the counts. The docs workflow's every command and the other generated-table checks
pass on the result, and the split images are hash-equal.

## Step 12: #947 (#946) on the step-11 head, `d09c7118`, then the ledger, `967b1ca9`

#947's head `66c6edf3` is fetched from origin's `946-ctx-fmt` and checked equal to its lane's checkout. It is merged
`--no-ff` onto `b1f1161b` (`d09c7118`), merge base `cb96336d`. #947's delta is 15 files, all firmware, tests, the
receive monitor's testbench and one evidence script: no RTL, no gitlink. **No conflict.** Git auto-merged four files
that the train also changed (`ctrl_plat.c`, `ctrl_mutants.py`, `plat_arms.py`, `test_ctrl_firmware.py`), each in
hunks apart, as the lane's scratch merge-tree found. The gitlinks stay the train's, `1616fc8f` / `801ef228` (#947
carries the base's, which it does not move).

| File | Resolution | Why |
|---|---|---|
| `sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py`, SPLIT_CONTROL_MEMORY.md, the plat and split-boot READMEs (`967b1ca9`) | the platform's 8x8 two-interface entry 62.5 to 63.0, its refusal 63.0 to 63.5, the ledger's cases and planted ledgers with it, and the debt 6.5 to 7.0 RAMB36 (28,672 B) in section 5's S14 list. The ledger's case writer moves five tiles of `.bss` into `.text` instead of four, so a case reaches 63.5; four reached 63.0 alone, past which `.bss` runs out of `sram`. No case or plant removed | the union broke the ledger: #947's writes add 960 B of `rom` to the 8x8 two-interface image, 140,008 B, 744 B past the 139,264 B 62.5 holds beside its `sram`. That is S14 debt by the owner's rule of 2026-11-15, as the lane found. Every other point holds its entry (1x1 45.0 and 46.0 within 56, 8x8/1if 58.0 at its 58.0, the size fixture unchanged within 60.5). Two of section 5's sentences and one README bullet still gave the one-interface and fixture entries before the step-10 cut (57.5, 60.0); they are brought to 58.0 and 60.5 |

## F-G4 (the split's PHY advertising every mode): STOP, no commit

The gating bench run found it on step 11's split images at both points. The analysis is
`receipts/step12/fg4/fg4-analysis.txt`.

- The split's write frames, values, pins and probe equal the release's.
- The host PHY model and the split boot simulation land every write. The simulation is the real image on the real
  split SoC logic, with a PHY at address 1.
- ~~#590's hardware probe puts the board's PHY at address 1.~~ **Corrected 2026-11-19:** that was wrong. #590's
  `mdio-phase.log` is a reviewer probe run against a simulated peer, and its `phy_address=1` is the model's. No
  record gives a board PHY address. On the board, address 0 answers, holds the writes and reports the e2 link (the
  bench reading of 2026-11-19).
- Neither premise of a known-good comparison holds: the release's advertisement was never measured on hardware
  (#840, no hardware used), and the bench's LINK counts come from the hardware link guard, not the poll.

So the cause is not found in software. The candidates need one boot reading the poll's state. No fix and no
diagnostic were committed; the head stays `967b1ca9`.

## F-G4: the diagnostic images and the fix candidates (no train commit)

The manager's decision of 23:1x: build the diagnostic as a bench image, not a train commit.

- **The diagnostic** is on the scratch branch `fg4-diag-967b1ca9` (`fcdb9f6c`) and adds the console command
  `milan_phy`. The 8x8 one-interface entry is raised to 58.5 for that image only.
- **Its bitstreams** were built by S9's recipe with the bench override `--eth-port e2`. Both pass the boot
  simulation, the identity gate and #818's floor; the status gives their paths and sha256.
- **The three fix candidates** are each a scratch branch off `967b1ca9` and a diff in `round5/fg4/` that applies to
  the train head. Each has a test that fails on the old code by name and passes with the fix, in the `platboot`
  arm, 53 of 53:
  - A: the advertisement re-verified by each poll's own register 9 read;
  - B: a poll a whole period late takes THE STEP's call ahead of the store's centisecond step;
  - C: the release's bit, with the PHY frame's stated cost restated by the rule.
- None is committed to `flip-train-1117-p11` until the manager names the cause.

## F-G4: WITHDRAWN (the manager's resume of 2026-11-19 01:2x)

The bench's second reading (`fg4-board-reading2.md`) read the second diagnostic's `milan_mdio` beside the test
machine.

- **The DUT's own PHY advertises 1000BASE-T full alone,** as #840 requires: R4 `0401`, R9 `0200`.
- **With the test machine at 10BASE-T half alone, the DUT's PHY has no link:** R1 `7949`, no partner page. The test
  machine meanwhile holds a 10 Mb/s link.
- **Its partner offers every mode with no pause** (R5 `c1e1`, R10 `3c00`) while the test machine offers 1000BASE-T
  full alone. So the test machine was negotiating with the bench's inline capture tap, which advertises every speed
  on each side.
- **The address question is closed.** `MDIO_ACK=00000003`: addresses 0 and 1 are one RTL8211E, address 0 the broadcast
  alias of its strap address 1, on e2's own bus.

So F-G4 is a bench-topology finding, not a defect of the train, the split or the release. Nothing goes into the train
for it, and it leaves the known limitations.

- The diagnostic branches (`fg4-diag-967b1ca9`, `fg4-diag2-967b1ca9`) and the candidate branches (`fg4-fix-a`, `-b`,
  `-c`) stay as scratch, never train commits. Their diffs stay in `round5/fg4/` as the record.
- Candidate B's gap goes to #495 as a residue for a later ticket, not into the train: through a 600 ms erase under
  input that leaves no pass empty, the poll publishes a link loss only after the save. Its failing test is
  `Phy.B13APollAPeriodLateTakesItsFrameThroughASave`; its fix would change THE STEP's order, ruled by #665 on
  2026-11-17.
- Candidates A and C answered causes the reading rules out, and are not carried.

## Step 12 with #947's round 2: `7650a02d`

#947's round-2 head `9f4f3de0` (R868-2 POSITIVE) is fetched from origin's `946-ctx-fmt`. It descends from round 1's
`66c6edf3`, which the train merged at `d09c7118`. It is merged `--no-ff` onto `967b1ca9` as `7650a02d`.

Round 2's delta (`66c6edf3..9f4f3de0`) is 13 files. In order:
- `ctrl_plat.c`: each kept format change writes its inputs' contexts in the face's change port, and a waiting change
  whose input was bound meanwhile is refused.
- its tests and mutants: `test_plat_sinks.cpp`, `sink_mutants.py`, now 26 defects;
- `ctrl_plat_image.py`;
- the receive monitor's `sim_ctxfmt.cpp`;
- the split boot simulation's `boot_soc.py`;
- the ROM ledger and its prose.

There is no RTL and no gitlink change; the gitlinks stay `1616fc8f` / `801ef228`.

**Conflicts:** the same seven files the #946 lane's composition found on `b1f1161b` (its
`round2/receipts/merge/composition.txt`), all the ROM ledger's or its prose:
- `SPLIT_CONTROL_MEMORY.md`;
- `sw/firmware/ctrl/plat/README.md`;
- `ctrl_memory.py`, `ctrl_memory_ledger.py` and `test_ctrl_memory.py`;
- `ctrl_split_boot/README.md` and `plat_ledger.py`.

| File | Resolution | Why |
|---|---|---|
| the six ledger files | the train's side, whole (`git checkout --ours`) | The #946 lane's resolution is "take the train's side of each, then raise the train's 8x8/2if entry from 62.5 to 63.0". On `967b1ca9` the train's side already holds 63.0: step 12's own ledger commit raised it. So no raise is owed, and its patch (`composition-ledger-raise.patch`) is not applied. #947's own entries (8x8/2if 61.0, 8x8/1if 56.5 as debt) are its base's and give way to the train's 63.0 and 58.0. |
| `sw/firmware/ctrl/plat/README.md` | its two conflict hunks, both the ROM paragraphs, the train's text; every other hunk as Git merged it | as the #946 lane did; round 2's prose on the formats (the change port, the waiting change's refusal, `platsinks` with 26 defects) merges whole |

**Checks:**
- **Round 2's delta is carried whole outside the ledger.** For each of its six other files, the merge's diff against
  `967b1ca9` equals round 2's own diff (`66c6edf3..9f4f3de0`), line for line:
  - `ctrl_plat.c`, `ctrl_plat_image.py`, `sink_mutants.py`, `test_plat_sinks.cpp`, `sim_ctxfmt.cpp`, `boot_soc.py`.
- **The ledger at `7650a02d`:** `plat_ledger.py --self-test` PASS, controls 9 of 9 as required.
  - 1x1/1if 45 and 1x1/2if 46 RAMB36, within 56.
  - 8x8/1if 58 at `platform-8x8-one-interface` (rom 138,624 B).
  - 8x8/2if 63 at `platform-8x8-two-interfaces` (rom 140,200 B).
  - `test_ctrl_memory.py` 0 failures. The size fixture's six arms build.
  - (`receipts/step12b/ledger/`)

## Step 12 at #947's frozen head: `0839453f`

#947 is frozen at `fe297847`.
- **Its reviews:** R867-3 POSITIVE at `fe297847` (#947 issuecomment-6996096094) and R868-2 POSITIVE at `9f4f3de0`
  (issuecomment-6993952183).
- **Why one review covers round 3:** round 3 is tests and docs only, so by the single-reviewer rule for trivial deltas
  R867-3 covers it.
- **The merge:** `fe297847` is fetched from origin's `946-ctx-fmt`. It descends from round 2's `9f4f3de0`, and is
  merged `--no-ff` onto `7650a02d` as `0839453f`.

Round 3's delta (`9f4f3de0..fe297847`) is 4 files:
- `test_plat_sinks.cpp` (+64): the receive monitor's change gate at a bound input's own index, a STREAM_OUTPUT's
  waiting format and the input's SET_NAME;
- `sink_mutants.py`: its defects, 28;
- the platform README's `platsinks` line;
- one sentence of `ctrl_memory.py`'s ledger comment.

There is no firmware source, no RTL and no gitlink change; the gitlinks stay `1616fc8f` / `801ef228`.

| File | Resolution | Why |
|---|---|---|
| `sw/litex/ctrl_memory.py` (the one conflict) | the train's side, whole | Round 3 renames the ROM debt's owner in one sentence of #947's own ledger comment: "S14" becomes "the hybrid XIP work, the cold-code and descriptor flash migration (#665 decision D3)". That comment gave way to the train's at round 2, and the train's block does not hold the sentence, so as before the ledger prose is the train's. The train's ledger text keeps its "S14" names, as at `7650a02d`. |
| the other three files | as Git merged them | each carries round 3's own diff, line for line |
