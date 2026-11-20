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

## F-G5, a composition fix: `01765bb0` (the manager's resume of 2026-11-19 12:3x)

**The finding.** The final gating run's (h) #25, on the 1x1/1if final image (the `7650a02d` gating build):
- STREAM_INPUT 0 was narrowed from 8 ch to 1 ch, SUCCESS, its 8 mappings removed first.
- After one cold cycle it read 8 ch again, while every other saved item persisted.
- It was confirmed in a direct repeat. 8x8/1if keeps the change in the same check, and the release passed it.
- The clause is REQUIREMENTS.md:476-482, the persisted inventory (Milan v1.2 5.3.8.1, 5.3.13).

**The cause, and which of the suspects it is.** It is the restore's validation, judged against the datapath's map
store while that store still holds its reset set.
- **The boot restore** of NVM_G_FMTI (`aecp_nvm.c:84`) goes `aecp_value_restore` -> `aecp_scalar_validate` -> the
  `format` port -> the face's SET_STREAM_FORMAT verdict (GSI kind 0 selector 15, `aecp_face.c`).
- **The verdict:** `milan_datapath.sv:6501-6577` computes it as bit 0 supported and bit 1 "every channel an existing
  audio mapping references still exists", judged against the datapath's own map store (`amap_in_store_r`). The face
  required the low byte to be exactly 3.
- **What the store holds during the restore:** before the face opens it is its reset set. The restored maps reach it
  only through the EDIT window after the open's publication (`aecp_restore_commit`).
- **At 1x1/1if** that set maps input 0's 8 channels, so a saved 1-ch format got verdict 1. The restore was refused
  (`NVM_REFUSED`), and the 8-ch default stayed. The saved empty map was then restored, which is why the bench found
  the mappings gone too.
- **At 8x8/1if** the input ports have no reset mappings (the bench saved SI0's mappings as `{}`), so bit 1 was always
  set and the restore was taken.
- **The other suspects are not the cause:**
  - The 1x1 shape's format list: the verdict's bit 0 is a family decode that admits 1 ch.
  - The ordering against the mappings' restore: the store is stale before the publication in either order.
  - #947's context write at boot: 1x1/1if has no receive-monitor contexts. #947's change port calls the face's
    port first and the NVM mark is the bridge's, so nothing is overwritten or dropped.

**The fix** (`aecp_face.c`, `format`): before the face opens (`f->ready` clear), the verdict's bit 1 is not read, and
a saved format is judged supported alone. The restored maps are already checked against the restored formats by
`aecp_restore_settle` (#658), and `aecp_restore_commit` brings the store to them after the open. From the open on, the
low byte must be exactly 3, as before.
- No other caller reaches the port before the open: the live SET_STREAM_FORMAT runs only once AECP is open, and also
  keeps its own `aecp_maps_allow_format` check.
- 8x8/1if's behaviour, #947's boot-time context writes and every other saved item are unchanged.

**The tests**, each failing by name on `0839453f` and passing with the fix (`receipts/fg5/`):
- **`Sinks.S12ANarrowedInputFormatIsKeptAcrossAPowerCut`**, at both shapes:
  - **The scenario:** input 0's mappings are removed and it is narrowed to 1 ch. The store's service writes it back,
    then a power cut: the fabric, CPU and memory from power-on, the flash kept. The format is then read.
  - **The far model** keeps the datapath's map store (the reset set from power-on, moved by EDIT commits) and judges
    the verdict from it, as the RTL does.
  - **On `0839453f`:** it FAILS at 1x1/1if ("S12 input 0's narrowed format is restored after the cut") and PASSES at
    8x8/1if, the bench's pattern.
  - **With the fix:** it passes at both.
- **`Face.BeforeOpenAFormatVerdictJudgesSupportAlone`:** before the open, verdicts 1 and 0x103 pass, and 0, 2 and 5
  refuse; once open, 1 refuses and 3 passes.
  - **On `0839453f`:** it FAILS ("supported, before the open"); with the fix it passes, with all 27 Face tests.

**The plants:**
- **The control campaign:**
  - `restore-format-survival-read` in `sink_mutants.py` (now 29 defects), caught by S12 in a new `platsinks1` arm:
    the sink suite at the shipping 1x1/1if.
  - The arms dict is reflowed by one line, `"rv32"` beside `"entity"`, to keep `ctrl_mutants.py` at the idiom
    gate's 1,000 lines; its words are unchanged.
- **The AECP campaign:** `face-format-survival-read-before-the-open` and `face-format-survival-unread-once-open` in
  `aecp_face_mutants.py`, caught by the Face test on their own words.
  - `Face.StreamAvbAndFormatAreTheDatapathsWords` already holds verdict 1 refused once open.

**The docs:** `aecp_face.h`'s port line, MAILBOX_SPLIT.md's verdict sentence, the AECP README's face defects and the
platform README's `platsinks` line. The AECP README's "the face's 59 defects" was already stale before this change: no
current table counts 59. It is left as it was, as residue.

**The gates at `01765bb0`** (`receipts/fg5/`):
- **The four shards:** PASS. The control campaign catches 826 of 826, and the AECP campaign 368 with 0 escaped. The three
  new plants are caught by name.
- **Sinks:** 12/0 at both shapes. `fw_coverage --check` PASSES.
- **The twin and plants, the receive monitor and the split boot at both shapes:** PASS.
- **The ledger:** PASS with 9 of 9 controls; each point has 16 B more `rom`, within its entry.
- **The quick lists:** PASS, with the same exceptions as `7650a02d`: `flip_grade --check`'s identical base eleven, and
  the CI-environment-bound set.
- **`git diff --check`:** clean.

**The images:**
- **The release:** byte-identical where loaded.
- **The four split platform images:** changed (1x1/1if `86c6f802…`, 8x8/1if `e814cce6…`).
- **The split gateware:** unchanged at both points (`gateware15.py`), so no routes are owed.
- **The twelve CPU budget images:** changed, `aecp_face.c` being linked in.
  - **The layout:** in the hot region the addresses and opcodes are identical, with 72 immediates changed. The cold
    code and `.rodata` moved 16 B, and the changed expression is never reached in the harness, whose format window
    is never answered.
  - **The confirmation:** step 11's seven groups re-run on the new images are all within bound (0 misses, every
    slice under its figure). Their figures move by up to about 5% each way, for example 8x8/1if's SRP records 129,393
    → 133,080 cycles against the 147,500 slice.
  - **So** the rows do not carry byte for byte, and re-establishing every row needs the full measurement. That is
    left to the manager, with the recommendation to measure once after steps 13 and 14, which move the same path.

## Step 13: #953 (#943) at its frozen head `a16899b1`, merged as `c05d5acb`

#953 is frozen at `a16899b1`.
- **Its reviews:** R871-2 POSITIVE (#953 issuecomment-7019514213) and R872-2 POSITIVE (issuecomment-7018882584).
- **The merge:** `a16899b1` is fetched from origin's `943-out-status`. It descends from `0839453f`, and is merged
  `--no-ff` onto `01765bb0` (F-G5's fix).
- **Its delta:** 15 commits and 22 files. A declaring STREAM_OUTPUT's stream_dest_mac is its Talker's MAAP address, and
  REGISTERING and REGISTERING_FAILED are its Listener's (`ctrl_app_aecp.c`, `aecp_commands.c`, `aecp_maps.c`). It adds
  their tests and 14 planted defects (`aecp_output_mutants.py`), the CPU budget's declaring-outputs arm, the twin's
  owed row removed and its zero stream planted, and the docs. There is no RTL and no gitlink change.

**No conflict.** Git auto-merged two files the train had also changed, as lane 955's scratch merge of the same three
found:
- `sw/firmware/ctrl/aecp/README.md`: F-G5's face-defect bullet and #943's bridge text;
- `test_aecp.cpp`: F-G5's Face test and #943's output tests.

**Both sides are kept.**
- For #943's 20 other files, the merge's diff equals #943's own, line for line.
- In the two shared files, every line either side added is in the merge (#943's 8 and 149, F-G5's 4 and 18).

## Step 14: #952 (#951) at `f09d82e0`, merged as `4b9f66c5`

#952 is at `f09d82e0`.
- **Its reviews:** R869-1 POSITIVE. R870-2 NEGATIVE only because the complete final-image CPU timing evidence is
  pending (R870-1-F2's remainder). This round's full re-measure provides it, and R870 re-checks it in the composition
  delta review.
- **The merge:** `f09d82e0` is fetched from origin's `951-redeclare`. It descends from `0839453f`, and is merged
  `--no-ff` onto `c05d5acb`.
- **Its delta:** 5 commits and 10 files. A withdrawn Talker's changed destination is held over two of the longest
  LeaveAll periods (`srp_mbx.c`), with its tests, plants and docs.

**No conflict.** Git auto-merged three docs files the train had also changed: `MAILBOX_SPLIT.md`,
`SPLIT_CONTROL_MEMORY.md` and the CPU budget README.
- **Both sides are kept.** For #951's 7 other files, the merge's diff equals its own.
- In the three shared files, every line either side added is in the merge.

## Composition fix: `c1e95dc1`, the firmware boundary's builders found by text

#943's lane found that the firmware-boundary gate (`ctrl_boundary.py`) refuses two builders found by text, which the
union left unclassified.
- `sw/firmware/ctrl/test/sink_mutants.py` (#946);
- `tb/verilator/ctrl_service_budget/talker_notice.py` (#936).

Both name the firmware's tree in their text, compile nothing, and are no program. So by `ctrl_configs.py`'s taxonomy
each belongs in `OUTSIDE`, with the reason its compiles are none of the firmware's:
- `sink_mutants.py` beside `plat_mutants.py`: the receive monitor's formats' planted defects, which the control
  campaign plants;
- `talker_notice.py` beside `notice_window.py`: it writes the talker-notice groups' stimulus, grades their notices,
  and names the planted defects `build.py` builds for its arm.

The gate's text search, re-run at the commit, finds no other unclassified builder. Its remaining "no program" builders
compile in the capture, as the taxonomy admits. One commit, 5 lines.

## The full CPU budget re-measure at `c1e95dc1`: STOP, an owner bound breaks (no restatement)

The manager's resume of 2026-11-19 21:0x, item 4. The run:
- **What:** every arm the harness holds and every group, with the formal measurement's options
  (`--record-budget-findings --record-share-findings`). That is arm A, answering-ports (all 100 groups),
  answering-every-port, valid-destinations, answering-later, shutdown-entry, talker-notices and #953's
  declaring-outputs.
- **Where:** at 1x1/1if and 8x8/1if, 64 parts a point on CPUs 0-63 (booked through `cpu_ranges.py`), 128 of 128 parts
  at rc 0.
- **The analysis:** the statement survey (`survey_point4.py`, `costs_r5.sh`, `compare_point.py`) and
  `record_classes.py` over every leg, then the flip check's own row rules (#955's `project.py` at this head, each
  statement planted).

**1x1/1if:**
- **The statements:** 0 of 69 exceeded by the rule.
- **The records by class:** the held map edit is 310 us of 310 (29,468 cycles), the held SET_STREAM_INFO 245 of 245
  (23,167) and the largest legal command 965 of 975.
  - The declaring-outputs arm reports, without holding, a map edit of 320 us (30,232). That arm holds only the records
    that ran a completion.
- **The notice path:** the AECP notice item is 150 us against 210, and the long notice 315 against 365.
- **The rows:** last 137.97 of 140 ms, ACMP 29.93 of 30, txL 48.89 of 49, and the load 0.522 of 0.70. If the reported
  edit were held, last would be 141.47.

**8x8/1if:** two costs exceed their statements by the rule, both in the valid-destinations arm's `srp-talker-held`:
- `record.srp`: 35,846 cycles, 380 us, against 375. `unit375` measured 35,547.
- `item.reclaim`: 3,840 cycles, 45 us, against 40. `unit375` measured 3,562.

The rule restates both: 380 and 45, never lowered.
- **What breaks:** with both, 8x8/1if's load is **0.7512, over the owner's 0.75**. With either alone it is 0.7461 or
  0.7487, and as stated 0.7436.
- **What holds:**
  - THE TRANSMIT's held line, 77 ms against tx 76.84;
  - the largest legal command, held at 1720 of 1720 (the declaring arm reports 1765 and 1725, not held);
  - the long notice, 310 of 320.

So no statement is restated and nothing is committed for it: "if an owner bound breaks, do NOT restate around it: STOP
with the figures". The owner decides between the options in #955's STOP. The figures are in `CPU-TABLE-c1e95dc1.md`
and the HANDOFF status.

The images and the gateware:
- **The release:** byte-identical where loaded.
- **The split gateware:** unchanged against `01765bb0`.
- **The four split product images:** as listed in the HANDOFF.

## The SRP cut (#665's ruling of 2026-11-20, item 3): `92de01f7`

RULING-1120 (#665 issuecomment-7029526172, `round5/RULING-1120.md`) asks for a logic cut of 8x8/1if's valid-destinations
`srp-talker-held` work, a composition fix. It is sized so 8x8/1if holds 0.75 with every exceeded cost restated by the
rule, with margin against about 300 cycles of layout movement.

**Where the cycles went** (committed-PC traces of `c1e95dc1`'s image, split by function; `receipts/srpcut/`):
- **The dearest record** (35,846 cycles, the burst's ninth Listener Ready, a new registration): 21,430 cycles are in
  cold code. The adapter's own share is about 7,100:
  - `same`: 27 calls, 2,374 cycles. The receive filter, its indication and its Registrar change each matched the
    Listener against every source.
  - the receive filter: 1,316, its pass over the sinks included;
  - the captures, 756; the two snapshots, 695; `apply_receive`, 736.
- **The reclaim** (`item.reclaim`, 3,840 at most): `mrp_reclaim`'s walk of MSRP's about 20 attributes. A walk costs
  about 28 cycles a node warm and two data-cache refills a node cold.
  - The group walked in every poll after its records and builds, about 3,010 cycles a walk.
  - The walk's mean held flat from 5 s to the end, so no walk freed an attribute then.
  - The dearest came in the poll after THE TRANSMIT's MSRP build.

**The cut** (`sw/firmware/ctrl/srp/srp_mbx.c`; each exactly equivalent, lwSRP's pin unchanged):
1. **lwSRP's reclaim is owed only where an attribute may be freed.** That is a change into Registrar MT with Applicant
   VO, AO or QO, which is `mrp_reclaim`'s own test, or a receive that created an attribute and left it at creation's
   VO and MT.
   - lwSRP reports every Applicant and Registrar change to the observer but a creation.
   - A receive's created attributes are the room for attributes it took from the pool, less the changes out of that
     state it reported.
   - Any other change or receive leaves nothing to free. SPLIT_CONTROL_MEMORY.md had drafted the same rule as an
     lwSRP change.
2. **The receive filter's pass over the sinks runs only while the interface is stale.** Only a Talker's indication
   changes what it reads, and that marks the interface stale.
3. **A Listener is looked up among the sources once a use** (`sources_of`): in the filter, the indication, the
   Registrar change and the walk. Its StreamID is compared with a source's only where their last bytes agree.
4. **The walk-free snapshot's capture is made in place**, its declaration unchanged.

What the cut costs:
- **RAM:** `srp_interface.fresh` sits in the room before `gate_base`'s alignment, so no RAM grows. An earlier place
  grew the struct 4 bytes an interface and the platform's 1x1/2if key 64 B; the ledger refused it, and it was moved.
- **Code:** 284 bytes.

**On the way:**
- The reclaim's walk had kept MSRP's attributes in the data cache for the next record. Cut alone, the reclaim fell to 0
  and the record hardly moved (35,824): the record's own walks now took the refills.
- About 60 % of the record is instruction refills of cold code. So the adapter's instruction savings move with the
  layout: 35,341 and 35,047 cycles at two layouts of nearly the same code.
- The cut therefore removes whole calls of cold code: the 27 `same` calls, the cold pool count and the 18 snapshot
  captures.

**The measurement before the full re-measure** (8x8/1if's `srp-talker-held` alone, on the committed code's image,
`survey_point4.py`):

| Cost | `c1e95dc1` | `92de01f7` | By the rule | Stated |
|---|---:|---:|---:|---:|
| `record.srp` | 35,846 | **34,803** | 370 us | 375 |
| `item.record` (held to `item.retained`) | 35,536 | **34,550** | 365 us | 375 |
| `item.reclaim` | 3,840 | **0** (no reclaim in the group's polls) | 0 | 40 |

`record.srp` is 911 cycles (2.6 %) under 375 us's 35,714.

**The tests** (`srp_listeners.cpp`, built with `srp_arms.LISTENER_SEAMS`'s new seams on `mrp_rx`, `mrp_reclaim` and
`mrp_set_rx_filter`):
- **The differential against the adapter before the cut:** two random 3,000-step sequences. After every step, every
  mailbox write, licence call and state is equal, and so is each participant's attribute list with its states and
  values. Frees are equal, and the walks fewer.
- **Four direct tests:** steady Listener records and builds walk no attributes; an attribute left as created is
  reclaimed, alone and beside another change; a leaving Listener is reclaimed.
- **On the old adapter they fail:** both differentials (walks equal) and the steady test (356 extra walks).
- **Every arm passes:** `srp_listeners.cpp` 8 of 8 at 1x1/1if and 8x8/1if, and the SRP arms 41 of 41.

**The plants:** `srp_reclaim_mutants.py` has 10 defects, each caught by its named test in the two-interface, 1x1/1if
and 8x8/1if campaigns, 30 of 30.
- It is registered in `srp_mutants.py`, in `test_ctrl_firmware.run_srp_mutants`'s selections and in `ctrl_configs.py`'s
  `OUTSIDE`.
- All 359 SRP plants have one site each.

**The harness tie:** `load_grade.RETRY_RULE`'s "each Applicant or Registrar change marked" moves to the observer's
`++i->fresh; } i->moved = true;`. The rule is unchanged: every change is still marked.

**A finding for its own Issue** (not fixed here): the walk-free snapshot's copy of a continuing kind, before the cut
`capture(s, s->desired)`, is covered by no test. Removing it escapes every suite, before the cut as after. A delivered
withdrawal retires the binding and a rebind sets the kind itself, so no reachable state found here needs it.

**The gates at `92de01f7`:** shard 3 (the SRP campaign) found two existing plants escaped. The cut had moved what
they observe:
- **`same-skips-the-last-byte`:** a Listener's StreamID is now told apart from a source's by its last byte before
  `same` is called.
- **`feedback-latest-filter-failed-first`:** the filter now recomputes only from a Talker's indication on, which its
  one-attribute test never meets.

Every other gate passed. The fix is the next commit.

## Two SRP plants re-targeted: `fb083864`

Tests only. Each defect is kept, planted where the cut leaves it observable:
- **`same-skips-the-last-byte`:** planted under a Talker's near miss of a bound sink,
  `SrpWalk.StreamMatcherNearMissSwapAndImmediateWithdrawal` (`srp_walk.cpp`), where `same` is the whole test.
- **`feedback-latest-filter-failed-first`:** planted against the cut's differential,
  `Listeners.RandomRecordsMatchTheReferenceReclaim`. Its reference recomputes every sink at every filter call, which
  a copy other than `listener_kind`'s makes differ.
  - A direct test was tried and dropped. Its earlier message had to be a Talker indication of the same stream, and that
    replaces the other kind (35.2.6). The second sink a cleaner test needs is on another interface at two interfaces.

Shard 3 passes on this content: the two in the campaigns that plant them, and the cut's 10 in all three. The CPU-budget
and product images at `fb083864` are byte-identical to `92de01f7`'s.

## The full CPU re-measure at `92de01f7`, and STOP at 1x1/1if

- **The run:** every arm and group, the formal options, 64 parts a point, 128 of 128 at rc 0.
- **The crash:** the host crash of 2026-11-20 13:31 cut 8x8/1if. Its 55 unfinished parts re-ran on the arms' own
  builds (`r6meas/resume6.sh`), whose image hashes are the measured ones. Two arms had completed, and two in part.
- **The table:** `CPU-TABLE-92de01f7.md`, with the step-14 head's figure for each statement beside it.

**8x8/1if: 0 of 68 exceeded.** The load is 0.7436 of 0.75.
- `record.srp`: 34,803 cycles (370 us), was 35,846.
- `item.record`: 34,550 (365), was 35,536.
- `item.reclaim`: 995 (15 us), was 3,840.

**1x1/1if: 3 of 68 exceeded, and two AECP records over their classes:**
- **The map edit (paced), held:** 29,993 cycles, 315 us against 310.
- **SET_STREAM_INFO, held:** 23,726, 250 against 245.
- **`record.adp`:** 9,585, 105 against the graded column's 100.
- **`centisecond`:** 15,976, 170 against 150.

The two AECP records moved by layout alone, since the cut does not touch AECP. `record.adp` and `centisecond` moved by
the cut's cache effect: 1x1/1if's records and ticks now take the refills the reclaim walk used to.

**By the usual rule** (those four raised), 1x1/1if's last queued notice is 141.53 ms against 140, and its ACMP row
32.74 ms against 30. Both are owner bounds.

**Ruling item 4 would hold them:**
- **What it restates:** the AECP notice item to 150 us (14,084 cycles), and the long notice to 315 (29,652).
- **The rows then:** last 132.93, ACMP 29.01, txL 47.83, the load 0.511.
- **But:** item 4's premise is "the rows already hold", and it "is not used to pass a missed bound". At this head it
  would be exactly that.

So no 1x1/1if statement is restated and nothing is committed for it.
- **The patch:** item 4 and the four raises, prepared in a scratch clone, is in `receipts/step15/item4/` with its
  grading. It also needs `CTRL_LOOP_QUEUED_MS` at 135, which the harness's notice windows read, and three planted
  controls re-anchored.
- **The decision:** the owner's, between allowing item 4 here, a further AECP or layout-neutral cut, and the bounds.

## Ruling item 4 at 1x1/1if, as the owner decided: `8c5e2b4f`

The owner decided that item 4 applies at 1x1/1if here (#665 issuecomment-7044585511). One composition-fix commit on
`fb083864` applies the prepared patch. Each statement's comment names the decision:
- **The notice path, restated from its measurement:** the AECP notice item 210 -> 150 us (14,084 cycles,
  `declaring-outputs`' `aecp-fanout`), and the long notice 365 -> 315 (29,652, arm A's `aecp-largest-notice`).
- **The four moved costs, raised by the rule:** the paced map edit 310 -> 315 (29,993 cycles), SET_STREAM_INFO's AECP
  record 245 -> 250 (23,726), ADP's donor-column record 100 -> 105 (9,585) and the centisecond 150 -> 170 (15,976).

**What the patch did not show, and what the tree now states.**
- **The slice moves.** At the restated statements #894's slice rule (`rows_tiers.ruled`: "the slice the tree must
  state at 1x1/1if") takes **950 us**, not 900.
  - The patch's own grading had listed this as the escaped control "the built design's slice not the rule's". That
    control is the only check of the ruling, so it is not re-anchored: `CTRL_LOOP_SLICE_US` is 950 at 1x1/1if.
- **The queued figure follows the slice.** At 950 us the last queued notice's row is 127.31 ms, and the queued rule
  makes `CTRL_LOOP_QUEUED_MS` **130**, not the 135 the patch and the resume named.
  - 135 is refused at 950 (`queued_bound.controls`), and 900 is refused by the slice rule, so 950 and 130 is the
    tree's only consistent statement.
  - The owner's bound stays 140 ms.
- **The rows** at 1x1/1if by every source, at the cut's measured costs: R4 13.26, R5 73.88, R6 69.75, first 14.69,
  last 127.31 of 130, R4L 203.48, ACMP 29.06 of 30, ADP 27.51, MAAP 27.61, tx 33.44 and txL 47.88 of 49. All hold.
- **The slice is code** (`ctrl_loop.c` reads it), so the 1x1/1if images change and 1x1/1if is measured again in full at
  `8c5e2b4f` (below). The 8x8 shapes' statements do not move.

**The controls, re-anchored to the rows, none weakened:**
- **THE TRANSMIT's figure under its row** (`rows_tiers`, `flip_grade`): the control planted one under the statement.
  1x1/1if's 35 ms now stands over its 33.44 ms row (a statement is not lowered), so 34 was not under the row. It is now
  planted one under the row rounded up (`shape_costs.one_under`).
- **The last queued notice's bound keyed on the interface count** (`shape_costs`): 1x1/1if and 8x8/1if now state the
  same 130 ms, so the plant could not tell them apart, and its guard ("not apart") escaped. Where the tree states one
  figure at both, the plant now states the interface count's shape 5 ms apart in its own table. The value check must
  still name 8x8/1if falling back; the textual check refuses the plant in either case.
- **run.py's queued constants** (`selftest_notice.py`): (140, 130, 62) -> (130, 130, 62). Its late probe is now one
  over the bound, read from the header, as 141 was over 140.
- **Results:** `flip_grade --selftest` 616 of 616, `rows_tiers --selftest` 1033 of 1033, `shape_costs --selftest` 25 of
  25. Each re-anchored control was also run against a blinded or off-by-one detector, and each escapes there
  (`receipts/step15/item4b/`).
- **The idiom gate:** `rows_tiers.py` stays at its 1,000 lines. The rounding is `shape_costs.one_under`, and two
  header-path lines are folded into one.

**Docs:** `ctrl_loop.h` and `aecp_mbx.h` (comments), FR_NFR.md 3.4.1 (140 ms the owner's bound, 130 the statement), the
harness and SRP READMEs, and SPLIT_CONTROL_MEMORY.md (a section, "The notice path restated on the SRP cut").

**The images at `8c5e2b4f`:**
- **CPU budget:** the 8 images at 8x8/1if and 8x8/2if are byte-identical to `fb083864`'s.
- **1x1/1if:** the 4 images differ, each in 10 bytes. These are five `addi`/`li` immediates: 900 -> 950, and the
  values derived from it. Their sections, symbols and `.rodata`/`.data` are equal (`receipts/step16/images/`).
- **Product images:** `1x1-if2`, `8x8-if1` and `8x8-if2` are byte-identical to `fb083864`'s. `1x1-if1` differs by the
  same five immediates.
- **Release export:** byte-identical where loaded.

**The 1x1/1if full re-measure at `8c5e2b4f`** (`CPU-TABLE-8c5e2b4f.md`): every arm and group, the formal options, 64 of
64 parts at rc 0. The measured images are the image build's.
- **No statement is exceeded:** 0 of 68.
- **The costs** are `92de01f7`'s cycle for cycle, as the unchanged layout predicts, except two that the slice's
  scheduling moves:
  - the centisecond, 15,672 (15,976);
  - ACMP's event, 13,859 (13,781).
- **The records by class:** `record_classes` PASS. SET_STREAM_INFO is 23,726 cycles at its 250 us, and the paced map
  edit 29,993 at its 315. The declaring-outputs arm's paced record is reported, not held, as at `92de01f7`.
- **The long notice:** 29,652 cycles at its 315 us.
- **The groups:** 241, with 0 refusals and 0 of 388,313 work passes over the share. The 14 BUDGET lines are the seven
  held-egress rows (tsn-c-stack #26), each twice, as at `92de01f7` (each 0.005 ms later). Every queued notice is within
  its bound.
- **Every owner bound holds at 1x1/1if** (`project.py`, the rows by every source):
  - R4 13.26 of 20, R5 73.88 and R6 69.75 of 90;
  - the first queued notice 14.69 of 20, the last 127.31 of 130 (owner 140);
  - R4L 203.48 of 238;
  - ACMP 29.06, ADP 27.51 and MAAP 27.61 of 30;
  - tx 33.44 and txL 47.88 of 49;
  - the load 0.5114 at the pin and 0.5083 with tsn-c-stack #32, of 0.70.
- **8x8/1if** is not re-measured. Its images are identical and no statement it reads moved, so `92de01f7`'s
  measurement stands: 0 of 68 exceeded, the load 0.7436 of 0.75. Its projected rows equal `92de01f7`'s line for line.

**The gates at `8c5e2b4f`: all PASS, with the previous heads' exceptions.**
- **Shards:** all four pass. The control campaign catches 826 of 826, as at `92de01f7`.
- **Also PASS:** fw_coverage, the twin and plants, `avtp_rxmon`, the split boot at both shapes, `ctrl_boundary` twice,
  the ledger (9 of 9), run.py `--self-test`, flip and load grades and self-tests, and the docs and generated checks.
- **Exceptions:** 8x8/2if's base findings (reported, not held), `ci_tool_inventory_check`, and the docs workflow's
  environment-bound rows.

**The gating bench bitstreams of `8c5e2b4f`** (the step-12b recipe, `--eth-port e2`, through `vivado-slot.sh`). Each
meets #818's floor at every corner, with 0 routing errors, and passes the identity gate:
- 1x1/1if: `c7189218…` (Slow +0.131/+0.102, Fast +1.636/+0.036 ns);
- 8x8/1if: `7d903412…` (Slow +0.176/+0.102, Fast +1.523/+0.036 ns).

Their loaded firmware sections equal the ledger's link of the head's product images. The two-sided receipt is
`receipts/step16/gating/loaded-identity/` (R866-4-F1), and the clones' head and porcelain are in
`receipts/step16/gating/clone-state/` (R865-4-F2).

## The re-measure recorded: `8dc85884` (docs only)

`SPLIT_CONTROL_MEMORY.md` alone changes:
- the new section records the 1x1/1if re-measure;
- "What is left" states the slice and the queued bound at this head, 950 us and 130 ms, which still read 900 and 140.

The docs checks pass at `8dc85884`, and `git diff --check fb083864 8dc85884` is clean. No other file changes, so
`8c5e2b4f`'s images, gates and bitstreams are this head's.

## The source-comment rule: `15168e14` (R865-4-R1 and R2; comments and message strings only)

By the owner's rule of 2026-10-15, source comments carry behaviour and reason with issue and requirement IDs only. One
commit on `8dc85884` therefore removes every issue-comment ID and review ID that the train (`cb96336d..8dc85884`) adds
in source and test comments and check texts. Each ruling is cited by its issue, date and item instead.
- **14 files:**
  - the headers `aecp_mbx.h` and `ctrl_loop.h`;
  - the hot list's header comments (`ctrl_split_hot.txt`, whose parser skips `#` lines);
  - a test comment in `test_nvm_write.cpp`;
  - the ROM ledger's record text in `ctrl_memory.py`;
  - nine harness modules' comments and docstrings, and two check texts: run.py's self-test's queued constants, and
    the declaring arm's fixture check, which dropped "R872-1-F2".
- **Line counts:** every changed file keeps its line count.
- **Dates:** each ID was resolved to its ruling's date from the documents that link it. The save-window ruling cited by
  #920's lines is 2026-11-15.

**Proof that nothing executable changed** (`receipts/step16/sweep/`):
- **The scan:** at `15168e14`, no line the train adds in a code, test, script or data file carries an issue-comment or
  review ID in a source comment or check text. Its control is the same scan at `8dc85884`, which finds 21.
  - Three data records keep theirs: the register reference's description text, the resource gate's record (written
    only by its generator) and a measurement record's provenance field.
  - `reboot_ctrl/mutants.py:113`'s ID is older than the train.
- **The classifier:** with comments removed and string literals masked, each of the 14 files is the same code at both
  commits. Its control, a plant re-target, is refused.
- **The images:** the twelve CPU budget images, the four product images the ledger links and the release export, all
  rebuilt at `15168e14`, are byte-identical to `8dc85884`'s. The release is compared where loaded, and its Verilog is
  equal outside its comments.
- **The gates:**
  - the ledger self-test (9 of 9) and `test_ctrl_memory.py`;
  - the quick list at `15168e14`: every self-test and check, flip, load, rows, shapes, queued bound, record classes
    (which runs the declaring arm's checks), the hot list's check and self-test, run.py's `--self-test`, the idioms
    and the docs.
  - The only failures are the previous heads' exceptions: `flip_check`'s base findings at 8x8/2if, reported and not
    held, and the CI-bound tool inventory.

## R865-4's two Docs findings (evidence and records only)

- **F1: the PR body's "final head" figures.** "Composed figures at the final head" and "Restated at the final head"
  now carry `8dc85884`'s figures. These are flip and load checks at the head, `CPU-TABLE-8c5e2b4f.md` and
  `CPU-TABLE-92de01f7.md`, and item 4's six statements with `CTRL_LOOP_SLICE_US` 950 and `CTRL_LOOP_QUEUED_MS` 130.
  - The CPU budget images table now carries the measured images, and "At the final head" the current state.
  - The Known limitations say the full re-measure is done, the gating bitstreams are `8c5e2b4f`'s, and the bench
    re-check is pending. The stale release-comparison bullet is gone.
  - Every other "final head" that named the step-10 or step-11 head of its time now says so.
- **F2: the evidence behind three identity claims**, published with scripts, logs, rc and planted controls:
  - the gating builds' clone head and porcelain, now and as each chain logged them (`gating/clone-state/`);
  - the release export compared where loaded across every head from `b1f1161b` to `15168e14`, eight pairs and 40 of
    40 loaded files equal (`release/`);
  - with author-r7's two-sided loaded-identity receipt (`gating/loaded-identity/`).
