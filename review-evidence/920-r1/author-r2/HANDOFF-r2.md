# [A786] #920 round 2: the merge of dev-soft-core 70f4056f, the save groups re-measured, the gates

Lane: `920-save-burst`. Round 1's head `54280c94` (round 1: `../round1/HANDOFF-r1.md`, its STOP #920
issuecomment-6908928237). Round 2 follows the manager's ruling on that STOP, #920 issuecomment-6910219988.

Status: REVIEW READY at `bd252db1`, posted as #920 issuecomment-6932870595 (`REVIEW-READY-r2.md`): every gate in section 5 passes, the harness exiting 1 at 8x8/1if on #914's per-shape
stated-cost lines alone, as ruled.

## 1. The ruling, as applied

- **The 8x8/1if routes:** recorded as **misses at the base, owed to #927**, with the figures below. No seed, no extra
  directive, no further route. The merge brings no gateware change, so there is nothing to re-route (section 2).

  | 8x8/1if directive | WNS, slow corners | WHS, fast corners |
  |---|---|---|
  | ExtraPostPlacementOpt (the recipe's) | +0.011 | +0.034 |
  | ExtraTimingOpt | +0.171 | +0.014 |
  | AltSpreadLogic_high | +0.215 | +0.014 |

  The base `659d7687`'s own 8x8/1if image, at the recipe's directive, gives the same: WNS +0.011, WHS +0.034, on the
  same paths. 1x1/1if met at all three; the best is ExtraTimingOpt, WNS +0.133, WHS +0.036.
- **8x8/1if's stated-cost lines:** recorded as #914's per-shape statements, as at the base (section 4).
- **The sync onto #919** waits for #919's REVIEW READY; it is not done in this round.

## 2. The merge (`d66b4045`, `--no-ff`, parents `54280c94` and `70f4056f`)

`70f4056f` adds one PR to this branch's base, #901 (#895): a Talker declares only while its SRP parameters are valid.
Its 50 commits change 52 files.
- **Gateware:** none. The merge's diff over `54280c94` touches no `hdl/`, `syn/`, constraint, board config or SoC
  builder file. Its files are firmware (`sw/firmware`), testbenches (`tb/verilator/ctrl_service_budget`,
  `tb/verilator/milan_dp`'s SRP TX mutants and plants), the memory ledger (`sw/litex/ctrl_memory*.py`) and docs. A
  route of the merge would differ only in the ROM's bytes.
- **Firmware that both sides touch:** `aecp_nvm.{c,h}`. #901 holds the names table as runs (`struct aecp_name_run`),
  and this branch gives the pending bits layout 3's id space. Both are kept: the runs' loop marks through the widened
  `mark()`, and the static assert and the burst plant's anchor are unchanged. `ctrl_loop.h` (the slice at one
  interface is 900 us, AECP_QUEUED_MS 140 ms, CTRL_LOOP_TX_MS) and `test_aecp.cpp` merged cleanly.
- **Conflicts, each resolved with both sides kept:**
  - `aecp_nvm.h`: this branch's `AECP_NVM_WORDS`, then #901's runs and their comment.
  - `ctrl_memory.py`, `ctrl_memory_ledger.py` and section 3 of `SPLIT_CONTROL_MEMORY.md`: both sides raised the
    platform's 8x8/2if entry to 60.5. #895's reason stands, and #920's is added within that cap. `ctrl_plat` is
    measured on the merge: 17,664, 19,200, 18,304 and 20,480 B, where #901's tree has 17,536, 19,072, 18,240 and
    20,352. At 1x1/1if the 36 words now take 128 B, since the padding #901 left is spent.
- **ROM per image on the merge** (`img/merge.txt` against `img/dev70.txt`, the same script and inputs): every image is
  #901's plus 296 to 304 B. The platform's 8x8/2if image holds 132,040 B of `rom` in its 60.5 RAMB36, within the cap.
  No entry is passed, so the BRAM rule raises nothing.
- **Checks on the merge before its commit:** `aecp_arms.py --nvm --filter 'Nvm.*'` passed 9 of 9 tests, among them
  `EveryAcknowledgedNameSurvivesTheRealStorePowerCycle`. `test_ctrl_memory.py`, the Python idiom gate (every ratchet
  at or under its budget), `docs_check.py`, `check_doc_style.py` and `check_doc_paths.py` all passed.

## 3. Round 1's units, collected

- **Round 1's suite sweep at `54280c94`** (the whole sweep serially on one range, on its own clean clone), finished at
  14:22: 65 suites, 61 passed, 2,712,626 checks, 0 in-suite failures (`round1-units/sweep-54280c94/summary.txt`).
  - `gptp_shadow` FAILED on its mutant-lifecycle step alone, a 12 s subprocess timeout, while its own 325 checks
    passed.
  - `media_phase`, `milan_dp` and `reboot_ctrl` timed out on the sweep's wall clock (1,400, 4,800 and 300 s), result
    unknown, under a host load average of 300 to 1,000.
  - The four suites, re-run alone on that clone on a booked range after the sweep (`rerun.sh`, from 23:57), each passed:
    `gptp_shadow` rc 0 in 228 s, `media_phase` 512 s, `milan_dp` 1,785 s, `reboot_ctrl` 153 s
    (`round1-units/rerun-54280c94/`). So round 1's head passes every suite of its sweep.
- `54280c94` is round 1's head, so this record stands for round 1. Round 2's head has its own sweep (section 5).

## 4. The re-measure (both points, every group)

**Why every group.** About 78 of each point's groups are saves or save windows, which this change moves. #901 moves
the rest: SRP's records, the transmit row, the queued notices, and the one-interface slice at 900 us. So every row is
an affected row. The build at each point runs `save-burst` and `save-flight` first. The rest run as part units on that
build (`--reuse-build`), and one `--regrade` of the point grades every group's log together.

**Interruptions.** Every unit without a recorded rc was treated as cut. Its half-written group logs were removed and
those groups run again; a log counts as complete only if it ends in its SUMMARY and `RESULT: PASS`.
- **The power cycle of 15:40.** It cut the eight first parts (`r2p0..3`), with 46 groups complete at 1x1/1if and 38 at
  8x8/1if, the two builds' save groups among them. 24 half-written logs were removed.
- **The crash of 18:46.** It cut the three 1x1/1if re-run parts (`r2q0..2`) with no group complete; their 21
  half-written logs were removed.
- **The maintenance stop of 19:39.** It came while `queue8` waited for a range, with nothing of it started.
- **From 19:44** the 111 groups left (52 at 1x1/1if, 59 at 8x8/1if) ran as four 16-CPU parts, `r2s0..1` at each
  point, 15 jobs each. All four recorded an rc by 22:12: 0 at 1x1/1if, and 1 at 8x8/1if from stated-cost lines alone.

**The image.** The builds' firmware is the merge's: `ctrl_app.elf` `e6ce5e91` at 1x1/1if and `898c2860` at 8x8/1if,
where round 1 had `1ae81a2c` and `a7c7a56e`.

**1x1/1if, all 98 groups** (`harness/regrade-1x1.txt`, the head's `run.py --regrade` over every group's log): exit 0.
- 0 refusals and 0 of 132,926 work passes over the share.
- The 7 budget misses are the seven held-egress rows of `backlog-owed` (61.9 to 63.9 ms, behind the 60 ms egress
  hold), as at the base and in round 1.
- No STATED line. The longest tier-2 slices: SRP's records 78,943, THE TRANSMIT's build 56,882, THE RETRY's round
  8,682 cycles, against the 90,000 of #901's 900 us slice.
- Joins 188.2 to 190.1 ms.
- The aged windows: 48, with 15 aged steps among their records; the least margin is 8.826 ms
  (`backlog-adp@blank-aged2-5`, SRP's last record at 11.174 ms).
- The longest pass carrying the store's step is 101,602 cycles (1.016 ms), within the 2.0 ms share; the longest step
  is 78,825 (0.788 ms).

**8x8/1if, all 97 groups** (`harness/regrade-8x8-1if.txt`): exit 1, on STATED lines alone.
- 0 refusals and 0 of 231,039 work passes over the share.
- The 7 budget misses are the same held-egress rows (61.9 to 64.7 ms).
- The longest slices: SRP's 71,041, the build's 44,249 and the round's 10,002, all within 90,000. Joins 187.8 to
  190.4 ms.
- The aged windows: 48 with 17 aged steps; the least margin is 9.506 ms (`backlog-adp@program-aged2-5`, at
  10.494 ms).
- The longest pass carrying a step is 115,570 cycles (1.156 ms); the longest step is 78,737 (0.787 ms).
- **The STATED lines are #914's per-shape statements, recorded as such** (the ruling). One interface takes 1x1/1if's
  statements at every shape on this base (`harness/8x8-1if-stated.txt`):
  - the polls base: 90 lines in 78 groups, the most 25,015 cycles (`save-starved`) against 22,500, in the pass that
    delivers a name. This change's `nvm_mark` takes 731 cycles of that pass, measured in round 1's triage.
  - an ACMP item: 3 lines, the most 7,277 against 5,500 (`backlog-owed`);
  - a declined ACMP offer: 4 lines, the most 2,338 against 2,000 (`backlog-owed`).

  Before the merge the build of one MRPDU and its slice were over one interface's statements at 8x8/1if too. On the
  merge the build fits the slice.

**The save groups, on the merge.** Round 1's figures, on this branch before the merge, are in brackets.

| | 1x1/1if | 8x8/1if |
|---|---|---|
| `save-burst`, the latest name durable after its response | 1,107.8 ms (1,101.7); names 258.9 to 1,107.8 | 1,370.3 ms (1,367.5); names 342.7 to 1,370.3 |
| `save-burst`, saves | 1, 73.1 ms from erase to durable; every name at the cut (seq 1) | 6, each 307.8 to 322.0 ms; every name at the cut (seq 6) |
| `save-flight`, durable after its response | 165.0 ms (158.5); next save 19 steps (want 19) | 663.1 ms (657.7); 59 steps (want 59) |
| `save`, `save-held` | 1,081.8, 1,097.2 of 4,070 ms | 1,308.8, 1,356.1 of 12,470 ms |
| `save-starved`, `save-second` | 4,049.1 of 4,070; 6,030.3 of 6,070 ms | 12,448.1 of 12,470; 22,829.6 of 22,870 ms |

Every name is durable within 1.4 s of its response at both points, against the ruling's 5 s.

The docs restate these figures in `bd252db1`: section 13's #920 subsection and the store's README.

## 5. Gates

Final head `bd252db1`: one docs-only commit over the merge `d66b4045` (its diff touches section 13 of
`SPLIT_CONTROL_MEMORY.md` and `sw/firmware/ctrl_nvm/README.md` alone). The code gates ran at `d66b4045`. The docs
jobs, the quick local gates and the suite sweep run at `bd252db1`. Each runs on a clean clone of its head, on CPUs
booked with `cpu_ranges.py`.

| Gate | Head | Command | Result | Receipt |
|---|---|---|---|---|
| CPU budget harness, every group, both points | `d66b4045` | `run.py` builds and parts, one `--regrade` a point | 1x1/1if exit 0. 8x8/1if exit 1 on STATED lines alone, #914's per-shape statements. Every row the CPU decides is within its bound at both | `harness/` |
| Harness self-test | `d66b4045` | `run.py --self-test` | 0 failures; 875 checks; 251 of 251 mutants caught | `tests/budget-selftest-d66b4045.txt` |
| Store suite with its planted defects | `d66b4045` | `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | 0: 546 tests at 5 shapes, all 152 planted defects caught | `tests/store-suite-selftest-d66b4045.txt` |
| rtl-fast firmware jobs | `d66b4045` | `run_wf.py` replica: changes, firmware-unit (with `fw_coverage --check`), -aecp-, -control- and -srp-mutants, -verilator, -boundary (the LiteX venv) | 0 failed steps in each; `verify_wf`: 24 ran, 83 not run with a reason, 0 bad | `workflows/d66b4045/`, `verify-rtl-fast-d66b4045.md` |
| elaborate jobs | `d66b4045` | `run_wf.py`: elaborate-gates-0, -1, elaborate (the LiteX venv) | 0 failed steps; `verify_wf`: 10 ran, 36 not run, 0 bad | `verify-elaborate-d66b4045.md` |
| docs jobs | `bd252db1` | `run_wf.py`: wire-accountability, docs-check-no-git, docs-gates-0, -1, -2, and rtl-fast's changes | 0 failed steps in each (docs-check-no-git's three steps rc 0; the replica's after-job `git status` cannot run once that job strips `.git`, by design); `verify_wf`: 61 ran, 34 not run with a reason, 0 bad | `workflows/bd252db1/`, `verify-docs-bd252db1.md` |
| Load gate | `bd252db1` | `load_grade.py --check` | 0: 1x1/1if 0.517 of 0.70 (0.514 with tsn-c-stack #32) | `gates/` |
| Memory ledger | `bd252db1` | `test_ctrl_memory.py` (the LiteX venv) | 0 | `gates/` |
| Python idiom, docs, style, paths | `bd252db1` | `check_py_idiom.py` (and `--selftest`), `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py` | 0 each | `gates/` |
| Suite sweep, four shards | `bd252db1` | each shard as `native-shards.py` starts it (`one_shard.py`: its own clean clone, `--shard k/4`), each started as soon as a range was booked for it (23:12 to 23:50), `SUITE_TIMEOUT` 10800 | 0 in every shard: 65 suites of 65 passed (15, 17, 17 and 16), 0 failed, 0 timed out; 2,713,040 checks, 0 in-suite failures | `sweep-bd252db1/` |
| ROM per image | `d66b4045` | `qimg.sh` against #901's tree | every image #901's plus 296 to 304 B; within every entry | `merge/` |
| The routes | | | misses at the base, owed to #927 (section 1): none run, as ruled | `../round1/receipts/image/` |

Before the power cycle of 15:40, the merge's firmware-unit, -aecp-mutants, -boundary and elaborate-gates-0 had
recorded their results, so they were not run again. The cut jobs (-control-mutants, elaborate-gates-1, the store
suite) and those never started ran again after it. Each half-written job directory was removed first.

## 6. Open items

- **The sync onto #919's review head** waits for #919's REVIEW READY (the ruling; the train puts #919 first).
- **8x8/1if's stated-cost lines** are #914's to state per shape. The polls base is the most at 25,015 cycles against
  one interface's 22,500.
- **The 8x8/1if routes** miss at the base and are owed to #927.
- The starved worst cases and the product part's figures stay above 10 s at 8x8. They are stated, not gated (the
  ruling of #665, item 1), and the append-only design (#823) closes them.
- The platform's 8x8/2if image fills its 60.5 RAMB36 cap with 1,080 B of `rom` left, as S14 debt.
