# HANDOFF (round 5) — [A775] lane 895

**Status (17:5x CET 2026-11-14): REVIEW READY at `62298ab5cbfeb7056e4567f70e69d578201c75e0` (local, not pushed); the
full pass ran once on it and passed; the comment is posted once on #895: issuecomment-6880958086, its body equal to REVIEW-READY-COMMENT.md.** Push and the PR edit are the
manager's (PR-BODY.md). New assignment (round 5), not a resume. Round 4 ended in the STOP at `91c3fc0e` (issuecomment-6875758968),
answered by the ruling #895 issuecomment-6876349305; #894 issuecomment-6876349104 (#902's AECP record check) running.
The host rebooted at about 12:29 (session cut, resumed 12:33): the in-session ledger link was killed and re-run; the
worktree's uncommitted ledger edits were intact and committed as commit 4.

- Worktree $LANES/895-talker, branch `895-talker-redeclare` (PR #901, base dev-soft-core), not pushed.
- Start: head `91c3fc0e`; origin/894-tiers `7398ec0a` (in HEAD), dev-soft-core `cec88385`, PR #902 OPEN. Checked
  again 12:34: unmoved, #902 OPEN.
- Scratch: /data-2/milan/tmp/895-a775/r5 (G = scratch clone for the analytic gradings, its submodules symlinked;
  L = clean clone of `b3a5ed99` the legs run on; ledgerW = the ledger link; c3 = commit 3's checks). Legs under
  /data-2/milan/tmp/895-a775/{builds,legs}/R5-*, units milan-895-a775-r5-*.
- Superseded scratch removed 12:3x (my own, listed first): rounds 1-3's builds F2-*, F4-*, G*, Q-*, R3-*, P-*, S-*
  under /data-2/milan/tmp/895-a775/builds (their summaries are in those rounds' receipts); /data-2 23 -> 50 GB free.

## Commits

| Commit | What |
|---|---|
| `0d2662c0` | ruling item 2: `load_grade.py` costs at their measurement on the merge (round 4's legs at `a93fceae`), each by the rule (most + 5 %, up to 5 us): 1x1/1if `event.AECP` 65 -> 75, `event.TICK` 45 -> 50, both columns; 8x8/2if `event.AECP` 105 -> 115 (donor 110 -> 115), `event.TICK` 40 -> 55 (donor keeps 85), `events_none` 30 -> 35, `record.maap` 150 -> 155, both columns; `record.aecp` kept at #894's 235 (ruling item 3); section 13 subsection "SRP's Talker declarations on THE TIERS", the costs bullet, #909 named |
| `c2622f79` | ruling item 1: `AECP_PACE_MS` 8 -> 9 (`aecp_mbx.h:55`), `paced_rows.choice` at the tree's tables; FR_NFR 3.4.1 pace sentence; section 13 current rows table, the head table's two new rows, THE PACE bullet, the subsection's pace bullet |
| `b3a5ed99` | ruling item 1: `CTRL_LOOP_TX_MS` 1x1/1if 30 -> 34 (`ctrl_loop.h:366`), the tx row 33.20 rounded up; its two controls' literals (`rows_tiers.py:932-934`, `flip_grade.py:174-178`: figure 34, plant 33); `SRP_REDECLARE_CS` 2,022 -> 2,023 cs at one interface (formula unchanged, 2,029 at two); `srp_talker.cpp:51-55` `kHoldOffMs` derived from the headers (was 20,220 typed; 20,230 / 20,290 now); FR_NFR 3.4.1 SRP row, SRP README, section 13 tx paragraph and bullet |
| `8238156d` | ruling item 4: platform 8x8/2if entry 60.0 -> 60.5 (`ctrl_memory.py` LEDGERED and reason), refused at 61.0; `ctrl_memory_ledger.py` OWN/HELD/REFUSED/planted at 60.5/61.0 (#894's `8db16d5d` pattern); `test_ctrl_memory.py` pin text; section 3, section 5 (flip criterion, this head's plan table), plat README |

| `10cd5472` | gates: srp_gate.hpp:133 one declarator a line; srp_talker_mutants.py `defects` -> `planter`, `declaration_defects`, `entry_defects` (34 plants identical tuple by tuple); build.py two comment blocks reflowed (1,003 -> 1,000 lines): check_py_idiom/check_cpp_idiom, failing since round 4's merges |
| `62298ab5` | section 13's closing items: the head's load (0.515 / 0.511; 8x8/2if 0.796 / 0.754), the ROM bullet, the summary |

Commit order: costs, then pace, then tx. At pace 9 with #894's two costs the slice rule (`rows_tiers.ruled`) takes
950 us, not the built 900, and `rows_tiers.controls` would refuse the tree ("the built design's slice not the rule's");
at the restated costs it takes 900 again (least margin +0.0225). So the costs went first.

## Items

| Item | What | State | Commit | Evidence |
|---|---|---|---|---|
| 1 | sync with origin/894-tiers if it moves / #902 merges | 7398ec0a at 12:07 and 12:34, in HEAD; no merge needed | | |
| 2 | ruling 1: AECP_PACE_MS 8 -> 9, CTRL_LOOP_TX_MS 30 -> 34, each its own commit | done | `c2622f79`, `b3a5ed99` | receipts/graders |
| 3 | ruling 2: AECP timer slot and TICK at measurement + 5 %, 8x8/2if's four costs; note on #909 | done (#909 named in code and docs; a note ON #909 is the manager's: I post only on #895) | `0d2662c0` | receipts/graders |
| 4 | ruling 4: 8x8/2if platform ROM entry 60.5 | done; plat_ledger PASS | `8238156d` | receipts/ledger |
| 5 | harness every point; flip check 1x1/1if composed; section 13 and PR body | done: every arm at both points rc 0, joins 1,091 within 181-239 (185.905 to 190.192 ms); flip PASS; section 13; PR-BODY.md | `62298ab5` | receipts/legs, receipts/costs, receipts/graders |
| 6 | gates; full pass once at the final head on a clean clone | done once at `62298ab5`: all PASS (the table below) | | receipts/gates, receipts/sweep |

## Analytic graders at the final firmware (worktree at `b3a5ed99` / `8238156d`)

1x1/1if, by every source (`flip_grade.py --check --point 1x1/1if`, PASS): R4 12.96 (20), R5 73.46 (90), R6 69.35 (90),
first 14.59 (20), last 127.08 (130), R4L 203.48 (238), ACMP 28.85, ADP 27.20, MAAP 27.29 (30), tx 33.20 (49; stated 34),
txL 47.86 (49). Pace rule 9 ms (txL 49.46 at 8). `tier_grid.py --point 1x1/1if`: 18 of 420 hold, CHOSEN the built
design (900 us, aecp-first, cap 2, buffer), least margin +0.0225. `load_grade.py --check` PASS: 0.515 at the pin,
0.511 with #32; 0.694 with every notice the largest legal one (tier_grid). 8x8/2if (reported): load 0.796 / 0.754,
R4L 210.90, txL 399.09, tx 89.15 (98 stated stands). `flip_grade.py --selftest` 555 of 555; `load_grade.py --selftest`
25 of 25. The ruling's "load 0.528" is round 4's grading with the AECP record at 300 fed too; at the restated tables
(record 235) the load is 0.515.

## ROM (ledgerW, worktree, every image)

| Image | rom / sram B | RAMB36 | Left |
|---|---|---:|---|
| platform 8x8/2if | 131,256 / 114,224 | 60.5 (entry 60.5) | 1,864 B rom |
| fixture 8x8/2if | 126,112 / 113,232 | 59.0 | 864 B |
| arm answering-every-port 8x8/2if | 126,420 / 113,296 | 59.0 | 556 B |
| arm valid-destinations 8x8/2if | 126,280 / 113,232 | 59.0 | 696 B |
| platform 1x1/1if, 1x1/2if, 8x8/1if | 116,992; 118,560; 129,720 | 43.0, 43.5, 56.0 | |
| fixture 1x1/1if, 1x1/2if, 8x8/1if | 111,928; 113,472; 124,608 | 41.0, 42.5, 54.5 | |

Every size equals round 4's merge's (the pace and tx move no byte).

## Changes (file:line, reason)

See Commits. All derived restatements by the ruling; no bound, ceiling, the every-source rule, or lwSRP changed.

## New checks (planted mutant, failing words)

None new. Restated existing controls:
- `rows_tiers.py:932-934` / `flip_grade.py:174-178`: plant `CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 33u : 98u)`, refused
  "CTRL_LOOP_TX_MS states 33 ms, under the built design's tx row 33.20 ms" (flip selftest 555/555).
- `ctrl_memory_ledger.py`: REFUSED "its own image at 61.0 RAMB36, half a tile past its 60.5" (refused 'budget');
  planted ledgers "the platform's entry at 61.0 RAMB36" and "the size fixture's entry at the platform's 60.5", each
  caught (test_ctrl_memory.py 0 failures).
- Talker plants (34, `srp_talker_mutants.py`) caught at 1 and 2 interfaces after `kHoldOffMs` derived (68 of 68).

## Gates (the full pass, once, at `62298ab5`, each on its own clean clone)

| Gate | Command | Result | Receipt |
|---|---|---|---|
| every `run:` step of rtl-fast, rtl, docs, elaborate | round5/scripts/gates/run_wf.py per job (gate_queue.sh), units via disp_once.py | every job failed 0; docs-check-no-git's 3 steps rc 0, its driver's after-run `git status` fails since the job's own step removes `.git` (driver artifact); docs-gates-1 re-run after the SDK link (incident/) | gates/workflows |
| verify | verify_wf.py 62298ab5 <wf> rtl-fast.yml rtl.yml docs.yml elaborate.yml --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4 | rc 0: 139 steps ran, 226 not run with a reason, 0 bad (round 2: the same) | gates/verify-table.md |
| firmware campaigns (in those jobs) | firmware-{control,aecp,srp}-mutants | control 716 of 716 caught; AECP 274 caught; SRP 413 caught (68 talker-: 34 x 2); 0 escaped | gates/workflows |
| builder (docs-gates-1/2) | test_builder.py legs 0/1 | PASS; 17 arms not run here (round 2: 16), the new one gate 23p, no LiteX interpreter in the gate venv | gates/workflows |
| job trees after | run_wf.py tree-after | clean, but firmware-unit and the three mutant jobs leave `?? dispatch-build/` (keys-16x4.yaml, keys-16x32.yaml): #902's `58e6b60f` `aecp_arms.key_arms` writes them as the shard dispatch self-test builds its arm list; not this lane's files, for #894 | gates/workflows/*tree-after.txt |
| full Verilator sweep | native-shards.py 895r5sweep spec 4 on 16-23, 32-39, 56-63, 80-87 (each free at a re-read just before launch; MemAvailable 32 GB) | 65 suites (15 + 17 + 17 + 16), 0 failed, 2,712,199 checks, 0 in-suite failures, each shard exit 0; shard trees clean after; with CI's `MAKEFLAGS=-j4 --no-print-directory` round 2's three plant-script reruns are not needed | sweep/ |
| tsn_fuzz with tsn-gen | suite_rerun.sh in shard 3's clone, TSN_GEN_ROOT the lane's pinned tsn-gen (the hosted job sets it, rtl.yml:380) | make rc 0, verdict rc 0; 164 and 675 field checks pass, freshness PASS; only the two TEST_RESULTS.md date stamps changed, restored | sweep/rerun-tsn_fuzz |
| lane gates a | lane_gates.sh a (in-session chunks + unit lane-a2) | all rc 0 but flip_check and flip_check_8x8 (rc 1 by design, 8x8/2if); flip_check_1x1 rc 0; harness_selftest 0 failures; behave 511 scenarios | gates/lane |
| lane gates b, c | lane_gates.sh b / c | test_builder --require-rv32 rc 0; nvm_selftest, boot_1x1, boot_8x8, boot_native, boot_plants rc 0 | gates/lane |
| CPU budget harness at the head | harness_final.sh 62298ab5 (fresh F5 builds) + compare_builds.py against R5 legs | see harness/ | gates/harness |

## Run history

- 12:07 assignment read; ruling 6876349305 and #894 6876349104 read; origin/894-tiers 7398ec0a (unmoved), #902 OPEN.
- 12:1x graders reproduced at 91c3fc0e (txL 49.20, tx 33.01 > 30). Scratch G: pace 9 alone -> slice rule 950 us;
  with the costs restated -> 900, pace 9, all rows hold, tier_grid built design.
- 12:15-12:26 commits 1-3; talker arms PASS (11 tests at both points), talker plants 68/68.
- 12:26-12:28 commit 4 edits; test_ctrl_memory PASS; ledger link (in-session; pick gave no range) killed by the reboot.
- 12:33 resumed; 12:35 clean clone r5/L of b3a5ed99; leg R5-A1 on 56-63 (the only range free). 12:36-12:40 ledger
  re-linked (ledgerW), commit 4 (`8238156d`).
- 12:4x the gate venv /data-2/milan/tmp/895-a775/gates/venv was gone (rounds' scratch cleanup): recreated (python3
  -m venv; pip wavedrom==2.0.3.post3, behave, pyyaml), the path run_wf.py and lane_gates.sh name.
- 12:4x worktree pre-check of the workflows' check scripts: check_py_idiom (long function 10 > 9, long module 11 > 10)
  and check_cpp_idiom (multi-declarator 1 > 0) FAIL, already at 91c3fc0e, PASS at #902's 7398ec0a: round 4's merges
  (no gate ran in round 4). Fixed, behaviour-preserving, commit `10cd5472`: srp_gate.hpp:133 one declarator a line;
  srp_talker_mutants.py `defects` split into `declaration_defects` + `entry_defects` via `planter` (34 plants
  compared tuple by tuple with HEAD's: identical); build.py two comment blocks reflowed to 120 columns, 1,003 -> 1,000
  lines. Then all 23 workflow check scripts rc 0; talker, srp-acmp-if1/if2 arms PASS.
- 12:51 commit `62298ab5` (section 13's closing items): the candidate final head.
- 12:52-12:56 lane gates part a in-session in two chunks on clone r5/gates/lane-wt-a: all rc 0 but flip_check and
  flip_check_8x8 (rc 1 by design: 8x8/2if); flip_check_1x1 rc 0. harness_selftest cut at 590 s by my timeout (no
  process left), queued with behave as unit lane-a2.
- 13:57 W-docs-gates-1 failed at gate_25_0: test_builder --require-rv32 "the provisioned absolute SDK selector must
  be adopted": run_wf.py's HOME (gates/home) lost its br-milan-rv32 link with the old gates dir (the hosted job's step
  installs the SDK at $HOME/br-milan-rv32; not_run.json's reason names this host's). Link recreated; the failed run
  kept in r5/gates/wf-incident; the job requeued on a fresh clone. W-docs-gates-2 (leg 1) PASS, 17 builder arms not
  run (round 2: 16), the new one gate 23p, the same no-LiteX-interpreter reason.
- 15:4x-16:4x legs merged (merge.py; the 8x8 regrade as unit X-merge-A8); costs at both points (round 1's parsers):
  equal to round 4's cycle for cycle, every cost within the restated tables; the ordinary AECP record 28,173 (300).
- 16:14 sweep launched (sweep_launch.py: four free halves re-read just before native-shards.py); 17:26 all four done.
- 16:5x-17:46 harness_final.sh at the head (F5 builds), compare_builds.py: all eight identical images.
- 17:2x tsn_fuzz with tsn-gen in shard 3's clone; its two TEST_RESULTS.md date stamps restored there.
- 17:4x #894 read: issuecomment-6878200592 (#902's AECP record 27,851 at its head), 6878230332 and 6878532871 (#902
  round 11: cut or class split). 894-tiers still 7398ec0a, #902 OPEN: nothing to sync.
- 17:5x receipts scrubbed and indexed (index.py: 728 files); PR-BODY.md; REVIEW-READY-COMMENT.md; REVIEW READY
  posted once on #895 (issuecomment-6880958086). Nothing pushed.

## For the manager

- Push `895-talker-redeclare` at `62298ab5`; replace PR #901's body with PR-BODY.md; act and the hosted exact-head
  contexts after the push.
- A note on #909 (ruling item 2): AECP's timer slot and the TICK at 1x1/1if rose with the merge's code placement
  (6,188 -> 6,805 cycles, instruction refills 106 -> 119 in the pass), restated by the rule, not chased; the text is
  in SPLIT_CONTROL_MEMORY.md section 13, "SRP's Talker declarations on THE TIERS".
- For #894: the shard-dispatch self-test leaves `dispatch-build/keys/*.yaml` untracked in a firmware job's checkout
  (#902's `58e6b60f`, `aecp_arms.key_arms` writes them while the arm list is built).
- When #902 moves (round 11), this lane syncs and recomputes.
- Scratch kept for reuse: /data-2/milan/tmp/895-a775/{r5,builds/R5-*,builds/F5-*,legs/R5-*}, sweep clones
  $LANES/895r5sweep-shard{0..3}. No unit of this lane runs.
