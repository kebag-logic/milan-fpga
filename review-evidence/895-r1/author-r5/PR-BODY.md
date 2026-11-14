[A775]

## Contents

- **[Status](#status)** — Round 5 at its head: what the ruling on round 4's STOP restates, and what ran on it.
- **[Linked Issue / roles](#linked-issue--roles)** — Public tasks, executor, and independent reviewers.
- **[Round 5](#round-5)** — Each item of the ruling and of the round's assignment, and the commit that answers it.
- **[The composed 1x1/1if flip check at pace 9](#the-composed-1x11if-flip-check-at-pace-9)** — Every row by every source, the pace rule, the slice rule, `tier_grid.py` and the load.
- **[The CPU budget harness](#the-cpu-budget-harness)** — Every arm at both points, the join intervals, and the measured costs.
- **[ROM ledger](#rom-ledger)** — Every point, the platform's 8x8/2if image at its 60.5 entry.
- **[The gate pass](#the-gate-pass)** — Every hosted job step run locally, the Verilator sweep, the lane gates and the harness at the head.
- **[Description](#description)** — The validity gate and the declarations (rounds 1 and 2), and each source's stream_id (#905).
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**REVIEW READY** at `62298ab5cbfeb7056e4567f70e69d578201c75e0` (`895-talker-redeclare` -> `dev-soft-core`), round 5.

The branch history:
- Rounds 1 to 3 to `9e30c2c3`; round 4 merged #902's `894-tiers` twice (`a93fceae` at `5b264bf2`, `91c3fc0e` at `7398ec0a`) and stopped: the composed 1x1/1if flip check failed (txL 49.20 of 49, tx 33.01 against `CTRL_LOOP_TX_MS` 30) and the 8x8/2if platform image planned 60.5 against its 60.0 entry (#895 issuecomment-6875758968).
- The ruling issuecomment-6876349305 answers it: option (a), the cost drifts restated, the AECP record left to #894, and the platform's entry at 60.5. Round 5 applies it in six commits on `91c3fc0e`. `894-tiers` stayed at `7398ec0a` all round and #902 is open, so no sync merge was needed.
- #902's round 11 on the AECP record (#894 issuecomment-6878230332, amended by 6878532871) opened during this round. The merge order stays #902, then #901; when `894-tiers` moves, this branch merges it again and recomputes the rows, the pace and THE TRANSMIT's figure by the same rules.

No rebase, no force, no amend. No RTL, mailbox-contract, tsn-c-stack, lwSRP or donor change. No bound, ceiling or the every-source rule moves; each figure moved is a derived restatement the ruling names.

## Linked Issue / roles

Relates to #895
Relates to #905 (acceptance 1 to 3 and 5 here; 4 is the bench run)
Relates to #894 (#902 merged here; its names patch carried unchanged; the AECP record's check, #894 issuecomment-6876349104)
Relates to #906, #907 (srptx findings, not fixed here)
Relates to #909 (the code and data placement the merge moves, named, not chased)
Relates to #896
Relates to #665

Executor: `[A775]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Round 5

| Commit | Ruling item | What |
|---|---|---|
| `0d2662c0` | 2 | `load_grade.py` states AECP's timer slot and the TICK at 1x1/1if at their measurement on the merge plus 5 %, rounded up to 5 µs (65 -> 75 and 45 -> 50 µs, both columns), and 8x8/2if's four: AECP's timer slot 105 -> 115 (with tsn-c-stack#32 110 -> 115), the TICK 40 -> 55 (#32's 85 kept, the larger), a pass's events' fixed part 30 -> 35, MAAP's record 150 -> 155. The AECP record stays #894's 235 µs (item 3). Section 13 names #909 for the placement the merge moves. |
| `c2622f79` | 1 | `AECP_PACE_MS` 8 -> 9 ms (`aecp_mbx.h`), `paced_rows.choice` at the tree's tables; FR_NFR 3.4.1's pace sentence and section 13's rows. |
| `b3a5ed99` | 1 | `CTRL_LOOP_TX_MS` at 1x1/1if 30 -> 34 ms (`ctrl_loop.h`), the tx row 33.20 by every source rounded up (`rows_tiers.tx_statements`); its two controls' planted figure 29 -> 33; `SRP_REDECLARE_CS` 2,022 -> 2,023 cs at one interface (formula unchanged; 2,029 at two); the Talker tests' hold-off horizon derived from the same headers (`srp_talker.cpp`; it was 20,220 ms typed); FR_NFR 3.4.1's SRP row, the SRP README, section 13. |
| `8238156d` | 4 | The platform's 8x8/2if entry 60.0 -> 60.5 RAMB36, the owner's cap (#665 issuecomment-6824896581; precedent issuecomment-6831583372), refused at 61.0; the ledger's own image, refusals and planted ledgers restated as #894's `8db16d5d` restated the fixture's; sections 3 and 5, the platform README. S14's debt 4.5 RAMB36, the cap fully used. |
| `10cd5472` | (gates) | Three files of the merged tree held to the idiom ratchets, each change behaviour-preserving: `srp_gate.hpp`'s one declarator a line (`check_cpp_idiom.py`), the Talker plant table split into two functions in its order (`check_py_idiom.py` long function; the 34 plants identical, compared tuple by tuple), `build.py`'s comments reflowed to 1,000 lines (long module; #902's is 1,000, the merge's import and registration made it 1,003). Round 4's merges left these; no gate ran there. |
| `62298ab5` | 5 | Section 13's closing items: the head's load, ROM and summary. |

**The order** is costs, pace, tx. At pace 9 with #894's AECP slot and TICK, the slice rule (`rows_tiers.ruled`) takes 950 µs, not the built 900, and `rows_tiers.controls` refuses the tree ("the built design's slice not the rule's"). At the restated costs it takes 900 again (least margin +0.0225), so no commit states a slice its rule does not take.

**The AECP record** (item 3): stated at #902's 235 µs. #894 issuecomment-6876349104 runs the check; `origin/894-tiers` has not moved, so nothing is recomputed here.

**#909** (item 2): the note belongs on #909, which this lane does not post on; the manager carries it. The text is in section 13 ("SRP's Talker declarations on THE TIERS").

## The composed 1x1/1if flip check at pace 9

`flip_grade.py --check --point 1x1/1if` at the head, by every source (ms):

| Row | Bound | #902 `7398ec0a` | Round 4 composed, pace 8 | Head, pace 9 |
|---|---:|---:|---:|---:|
| R4 | 20 | 12.85 | 12.90 | 12.96 |
| R5 / R6 | 90 | 72.91 / 68.80 | 73.19 / 69.07 | 73.46 / 69.35 |
| first queued notice | 20 | 14.51 | 14.57 | 14.59 |
| last queued notice | 130 | 126.46 | 126.78 | **127.08** |
| R4L | 238 | 188.39 | 188.44 | 203.48 |
| ACMP / ADP / MAAP | 30 | 28.44 / 26.83 / 26.95 | 28.66 / 27.05 / 27.15 | **28.85** / 27.20 / 27.29 |
| tx | 49 (`CTRL_LOOP_TX_MS`) | 29.86 (30) | 33.01 (30) | 33.20 (**34**) |
| txL | 49 | 48.09 | 49.20 | **47.86** |
| result | | PASS | FAIL | **PASS** |

- **The pace rule** (`paced_rows.choice`): txL 53.03 at 7 ms, 49.46 at 8, **47.86 at 9**, 46.25 at 10; R4L 203.48 at 9. So 9 ms is the smallest that holds, as the ruling's 47.86 / 203.48 states. At #894's two costs it was also 9 (47.60 / 203.44, round 4's `flip-option-a.log`).
- **`tier_grid.py --point 1x1/1if`**: 18 of 420 designs hold every row and the load; **CHOSEN the built design** (900 µs, AECP first, cap 2, the slot buffer), least margin +0.0225 (round 4 composed: 0 of 420).
- **The load** (`load_grade.py --check`, PASS): 1x1/1if **0.515** at the pin and 0.511 with tsn-c-stack#32, 0.694 with every notice the largest legal one, each within 0.70. 8x8/2if 0.796 / 0.754, reported (the flip check holds it, rc 1 as before). The ruling's 0.528 was round 4's grading with the AECP record at 300 too; at 235 the load is 0.515.
- **8x8/2if** (reported, not held): R4L 210.90 within 238, txL 399.09, tx 89.15 under the 98 stated, which stands.
- Self-tests: `flip_grade.py --selftest` 555 of 555 plants refused, `load_grade.py --selftest` 25 of 25.

## The CPU budget harness

Every group of every arm at 1x1/1if and 8x8/2if, on a clean clone of `b3a5ed99`, whose firmware is the head's (the later commits change the ledger, the idiom-only edits and docs). `run.py --record-budget-findings --record-share-findings`; arm A in five parts a point, merged and regraded as one leg. The images carry the new constants: the pace gate compares against 9 (`sltiu a0,a0,9`; 8 at round 4).

| Point | Arm | Groups | Refusals | Budget misses | Passes over the share | `STATED` | rc |
|---|---|---:|---:|---|---|---:|---:|
| 1x1/1if | A (5 parts, merged) | 96 | 0 | 7 of 950 | 0 of 134,749 | 0 | 0 |
| 8x8/2if | A (5 parts, merged) | 94 | 0 | 7 of 994 | 0 of 230,855 | 0 | 0 |
| 1x1/1if | `answering-every-port` | 16 | 0 | 0 of 280 | 0 of 20,903 | 0 | 0 |
| 8x8/2if | `answering-every-port` | 16 | 0 | 0 of 736 | 0 of 16,050 | 0 | 0 |
| 1x1/1if | `valid-destinations` | 2 | 0 | 0 of 5 | 0 of 2,668 | 0 | 0 |
| 8x8/2if | `valid-destinations` | 2 | 0 | 0 of 20 | 0 of 3,053 | 0 | 0 |
| 1x1/1if | B (`aecp`) | 1 | 0 | 0 of 25 | 0 of 112 | 0 | 0 |
| 8x8/2if | B (`aecp`) | 1 | 0 | 0 of 39 | 0 of 140 | 0 | 0 |

- **The misses** are arm A's seven `backlog-owed` held-egress rows at each point (ruling 6871343905 (a)), as before.
- **Join intervals: 1,091 in 227 group runs, 185.905 to 190.192 ms, every one within 181.0 to 239.0** (`join_grade.py`, #894's egress ruling item 1).
- **At the head** (`harness_final.sh` on `62298ab5`, a fresh build of every point and arm): the image's loadable bytes are identical to the legs' builds at all eight (`compare_builds.py`; the executables differ only by LiteX's stamps), each sample group's log is byte-identical to the leg's, and every measured group regrades rc 0 on the head's graders.

**The measured costs** (round 1's parsers over these legs) equal round 4's merge's cycle for cycle, so the pace and the figure move no cost:
- 1x1/1if: AECP's timer slot 6,805 (75 µs by the rule, stated 75), the TICK 4,385 (50; 50), MAAP's record 9,536 (105; 115); every other `load_grade.py` cost within.
- 8x8/2if: AECP's timer slot 10,824 (115; 115), the TICK 4,948 (55; 55), a pass's events' fixed part 2,882 (35; 35), MAAP's record 14,361 (155; 155); every other within.
- The largest legal command's record is 92,046 (970 µs), within `LONG_RECORD_US`'s 975.
- **The ordinary AECP record** (arm A without `aecp-largest-notice`): 28,173 cycles in `aecp-fanout`, 300 µs by the rule against the 235 stated. By the ruling it stays at #902's figure: #894's check (issuecomment-6878200592) reproduces it on #902's own head at 27,851 and opens #902's round 11 (6878230332, 6878532871), a cut or a class split. When #902 moves, this lane syncs and recomputes.

## ROM ledger

RV32 images linked by the head's `plat_ledger.py` (the platform's, every point, against the ledger) and `ctrl_srp_image.py` (the size fixture and the harness's two 8x8/2if arms) on each shape's split export and runtime. rom / sram need in B, then RAMB36:

| Point | Image | Entry or budget | #902 `5b264bf2` | Head | Left |
|---|---|---:|---|---|---:|
| 1x1/1if | fixture | 56 | 110,576 / 55,152: 40.5 | 111,928 / 55,184: 41.0 | |
| 1x1/2if | fixture | 56 | 111,872 / 57,312: 41.5 | 113,472 / 57,360: 42.5 | |
| 8x8/1if | fixture | 56 | 124,104 / 96,240: 54.0 | 124,608 / 96,288: 54.5 | |
| 8x8/2if | fixture | 59.0 | 125,368 / 113,168: 59.0 | 126,112 / 113,232: 59.0 | 864 B |
| 8x8/2if | harness `answering-every-port` | 59.0 | 125,676 / 113,232: 59.0 | 126,420 / 113,296: 59.0 | 556 B |
| 8x8/2if | harness `valid-destinations` | 59.0 | (no such arm) | 126,280 / 113,232: 59.0 | 696 B |
| 1x1/1if | platform | 56 | 115,640 / 56,224: 42.5 | 116,992 / 56,224: 43.0 | |
| 1x1/2if | platform | 56 | 116,952 / 58,336: 43.5 | 118,560 / 58,400: 43.5 | |
| 8x8/1if | platform | 56 | 129,208 / 97,264: 56.0 | 129,720 / 97,264: 56.0 | 1,352 B |
| 8x8/2if | platform | **60.5** (60.0 before) | 130,504 / 114,160: 60.0 | 131,256 / 114,224: **60.5** | 1,864 B |

- `plat_ledger.py` PASS (0 findings); `test_ctrl_memory.py` PASS: the platform's own image plans 60.5 under its entry, 61.0 is refused, and the planted entry at 61.0 and the fixture's at the platform's 60.5 are each caught.
- Every image is round 4's composed image to the byte: the pace and THE TRANSMIT's figure move no byte.
- 58.5 stays out of reach for the 8x8/2if fixture and arms: #902's own fixture is 59.0.

## The gate pass

Once, at `62298ab5cbfeb7056e4567f70e69d578201c75e0`, every job on its own clean clone (`run_wf.py` from the workflows at the head; units on ranges `cpu_ranges.py` booked), never piped:

| Gate | Result |
|---|---|
| every `run:` step of `rtl-fast.yml`, `rtl.yml`, `docs.yml`, `elaborate.yml` (`verify_wf.py`) | **139 rc 0, 226 not run with a stated reason, 0 bad**; every job "failed 0" |
| firmware campaigns (in those jobs) | control 716 of 716 caught, AECP 274, SRP 413 (the 34 Talker plants at both interface counts among them), 0 escaped |
| full Verilator sweep, 4 shard units (`native-shards.py`, each on its own booked range) | **65 suites, 0 failed, 2,712,199 checks, 0 in-suite failures**; every shard exit 0 and its clone clean after. `tsn_fuzz` re-run with the pinned tsn-gen, as the hosted job sets `TSN_GEN_ROOT`: 164 and 675 field checks pass, freshness PASS |
| lane gates | `git diff --check` against dev-soft-core and #902, the idiom gates, `docs_check.py`, the hot list, the load, flip and harness self-tests, `gen_mailbox`, `lint_rtl`, `test_soc_options`, `test_ctrl_memory`, the hooks and target self-tests, `test_builder.py --require-rv32`, the NVM self-test, the split boot at 1x1, 8x8, native and its plants, behave (511 scenarios): all rc 0, but `flip_grade.py --check` and `--point 8x8/2if`, rc 1 by design (they hold 8x8/2if); `--point 1x1/1if` rc 0 |
| the CPU budget harness at the head | above: images identical, samples byte-identical, every group regraded rc 0 |

Before the pass, the workflows' check scripts were run on the worktree: `check_py_idiom.py` and `check_cpp_idiom.py` failed already at round 4's `91c3fc0e` (they pass at #902's head), which `10cd5472` answers without changing behaviour.

Recorded, not this lane's:
- `firmware-unit` and the three mutant jobs leave an untracked `dispatch-build/keys/` (two key-geometry YAMLs) in their checkout: #902's `aecp_arms.key_arms` (`58e6b60f`) writes them while the shard-dispatch self-test builds its arm list. For #894.
- The builder legs run 17 gate arms "not run" here for want of a LiteX interpreter in the gate venv (round 2: 16; the new one is the base's gate 23p).
- `docs-check-no-git`'s three steps are rc 0; the local driver's after-run `git status` cannot run there, since that job's own step deletes `.git`.

Not run here: act (`scripts/act_ci.py`) and the hosted exact-head contexts, which follow the manager's push.

## Description

### Validity and the declarations (rounds 1 and 2, unchanged)

A source declares its MSRP Talker only while its SRP parameters are valid: MAAP holds its destination, and a probe of the last 15 s or a registered Listener asks for it (Milan v1.2 4.3.3.1, 5.3.7.4).
- It declares at once, Talker Advertise with base + n and its TSpec, or Talker Failed (code 1) when its bandwidth does not fit.
- A lapse withdraws it, its licence and TALKER_DECL bit first. A Leave lwSRP refuses stays owed until lwSRP takes it.
- An unchanged destination is declared again at once. A changed one waits two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8, Table 10-7), plus a JoinTime and THE TRANSMIT's MRPDU by every source (`SRP_REDECLARE_CS`, 2,023 cs at one interface, 2,029 at two), so the count covers the Leave's own lateness. Under the tiers the JoinTime is the loop's, 19 cs.

Under THE TIERS, the declarations ride THE TRANSMIT's slices. A slice that holds one MRPDU makes the MSRP one, and the next makes the MVRP one and that interface's declarations. The Talker's licence still waits for the MVRP commit (Milan v1.2 4.3.2).

### Each source's stream_id (#905, unchanged this round)

The datapath stamps each source's `SRC_SID_HI:SRC_SID_LO` on its AVTPDUs. The contract (`KL_mbx_pkg.sv:345`) says the owner writes both words while the source's `DA_GATE` bit is clear.
- The MAAP adapter (`maap_mbx.c`), which owns `DA_GATE`, writes them through `mbx_pub_src_sid`: every source's at its start, before any pass and any bit opens, and again before each reopening.
- Four `SrpGate.F905A*` tests at 1x1/1if, 1x1/2if and 8x8/2if, five plants, and srptx's `[SID]` check.

## Authoritative references

- #895 rulings issuecomment-6876349305 (round 5), 6864645058, 6857334948. #894 issuecomment-6876349104 (the AECP record's check), rulings 6867990126 (the egress bounds: MRPDU 49 ms, paced R4L 238 ms, the join gate 181 to 239 ms), 6870437042 (item 4, the pace rule), 6845846512 (the slice rule), 6844175391 (item 2, the 59.0 fixture). #665: the owner's decision issuecomment-6824896581 (platform 60.0, cap 60.5) and issuecomment-6831583372 (an entry raised to its cap).
- IEEE 1722.1-2021 9.3.2.6; IEEE 802.1Q-2018 10.7.11, 35.2.2.8, Tables 10-5 to 10-7; Milan v1.2 4.2.7.1.1 (Table 4.3), 4.3.2, 4.3.3.1, 5.3.7.4.
- `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 13 ("SRP's Talker declarations on THE TIERS"); FR_NFR.md 3.4.1; `sw/firmware/ctrl/loop/ctrl_loop.h` (`CTRL_LOOP_TX_MS`, `CTRL_LOOP_TX_BOUND_MS`, `CTRL_LOOP_JOIN_CS`); `sw/firmware/ctrl/aecp/aecp_mbx.h` (`AECP_PACE_MS`); `sw/litex/ctrl_memory.py` (`LEDGERED`).

## How to get into the same state

```sh
git fetch origin 895-talker-redeclare && git checkout 62298ab5cbfeb7056e4567f70e69d578201c75e0
git submodule update --init --recursive
# the product LiteX tree's environment, the pinned RV32 SDK on PATH, Verilator 5.050,
# COURSIER_MODE=offline, SBT_OPTS=-Dsbt.offline=true, PYTHONHASHSEED=0
```

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if   # rc 0: txL 47.86, last 127.08, ACMP 28.85, tx 33.20 (34)
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if            # rc 0: 18 of 420, CHOSEN the built design at 900 us
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                   # rc 0: 0.515 / 0.511
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest                # rc 0: 555 of 555
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/pl          # rc 0: 8x8-if2 60.5 within its 60.5
python3 sw/litex/test_ctrl_memory.py                                                # rc 0
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant valid-destinations \
  --build-dir /tmp/w1 --record-budget-findings --record-share-findings              # rc 0
```

## Known limitations / out of scope

- **The AECP record** (300 µs measured, 235 stated) is #894's check; if #902 restates it, this lane syncs and recomputes. At 300 the composed ACMP row would be 33.64 of 30 ms at any pace (#894's #872 trigger).
- **Layout sensitivity (#909):** AECP's timer slot and the TICK rose with the merge's code placement, restated by the rule, not chased.
- **The platform's 8x8/2if image has no headroom past its granule:** 1,864 B of rom at the cap; any further growth there is a stop.
- **Found before, for their own issues:** srptx `[TIME]` (#906) and the hold `[TX]` path (#907), recorded in the milan_dp README.
- **8x8/1if** is lane 894b's; its harness point was not run here.
- **Round 2's items stand:** the Domain's own leave and join on the refused path, and the Domain adoption's in-place VID change, each for its own issue. The bench run (#895 acceptance 6, #905 acceptance 4) is the bench lane's.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (acceptance 4 composed holds by the ruling at the head; acceptance 6, the bench run, is the bench lane's)
- [x] Required tests and local gates pass at the exact head (the full pass above)
- [ ] Current PR head has a successful `rtl-fast` verdict
- [ ] Exact-head `verilator-suites` and `yosys-portability` after ready
- [x] No undocumented requirement/interface change
- [ ] Internal cleared-context review POSITIVE at the exact head
- [ ] External review POSITIVE at the exact head
- [ ] Every review lens covered clean at the merge candidate
- [ ] Candidate merge validated, post-merge containment clean
