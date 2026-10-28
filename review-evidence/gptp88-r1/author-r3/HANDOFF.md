# [A690d] HANDOFF — FPGA-gPTP #87 + #88, merge round on PR #93

Status: REVIEW READY at merge head `b0473e69`.

- Every repository gate is rc 0 at base `3426089a` and at the merge head, and both engine mutation arms are killed in full.
- The parent consumer list (15 commands) and tsn_fuzz `ptp` are rc 0 with both companions stacked, #92's first.

- Repository: Mister-M-alt/FPGA-gPTP, branch `87-88-announce-pathtrace` (local, not pushed)
- Base: main `3426089a14d58acc1c69420be30563e3395897b8` (PR #92, #89/#90/#91, merged)
- Round-2 head: `5ed415a7f072fe218500adedde64659c95c69804`
- Merge head: `b0473e697e0f93e3bb38a4da1ba2ad48012d2253`, two commits on `5ed415a7`:
  - `98edabb` Merge main (#89, #90, #91) into the #87/#88 lane, keeping both sides' checks and arms. It is a merge commit with parents `5ed415a7` and `3426089a`; there was no rebase.
  - `b0473e6` Run the #88 issue shapes' whole-interval deferral after phase 40, on the parent's usable Sync (#88)
- Assignment: #88 issuecomment-6463247110 (merge round).
- TAKEN: #88 issuecomment-6463260411.
- REVIEW READY (head `b0473e69`): #88 issuecomment-6468239930.

## What the assignment asked, and what was done

| Item | Done |
|---|---|
| 1. Merge `origin/main` as a merge commit and keep both sides | `98edabb`. Both sides' receipt-rule and path-trace checks and mutant arms are kept, each with its strict named-check prefix. SOURCE_EVIDENCE anchors resolve at the merge head (20 exact, 0 findings). |
| 1. (semantic follow-up) | Merged as is, the engine suite fails 200 of 1968. #92's sync receipt ageing ages the peer in the #88 issue shapes' Sync-less one-second wait. `b0473e6` moves that wait to after phase 40 and feeds it the parent's Sync. |
| 2. Companion stacked on #92's (`b53944d5`) | New patch `milan-fpga-companion.patch`, sha256 `3a3db51805985df7a19bfc2308c8e6602b9784cf305746e18796e11b15376451` (85383 bytes). Order: #92's `b53944d5…`, then this patch. It does not apply to bare dev. |
| 3. Gates | Repository: all 10 rc 0 at base and head, plus the OOC selftest. Engine arm 113/113 at head (112 mutants + control) and 101/101 at base. Parent: 15/15 rc 0 with both companions stacked. tsn_fuzz `ptp`: rc 0, 675 pass, freshness PASS. |

## Changes (file:line, at `b0473e69`)

### Merge commit `98edabb`: the three conflicts

- `tb/verilator/engine/mutants.py:206-214`, "lost response cancels the requester exchange". The body is main's (`BR t1`, from #92's generator). The description stays on one line, as round 2 had it.
- `tb/verilator/engine/mutants.py:888-892`. The strict named-check prefixes are now the union `#82 #84 #85 #87 #88 #89 #90 #91` plus the priority1-255 prefix, with one comment. The module is 995 lines, under the parent's 1000-line Python ratchet.
- `tb/verilator/engine/sim_main.cpp:193-217`. Phase 38 keeps round 2's wording, and main's phases 39–42 follow.
- `docs/SOURCE_EVIDENCE.md:31`. The slew row keeps the engine anchors from this branch (L111, L1020, L1025), and the generator anchor moves to `prog_leg_slew` in the merged generator (L1001).

The other files auto-merged without overlap:

- `hdl/ucode/gen_gptp_ucode.py`: main's code plus round 2's comments. The four ROM images regenerate byte-identical and equal main's (`receipts/engine-merge/merge-checks.txt` §1).
- `docs/INTEGRATION.md`, `docs/HDL_DEVELOPER.md`, `docs/TEST_DEVELOPER.md` and `docs/MANAGER.md`: main's additions carry no path-trace text.

The arm at head is main's 100 entries and round 2's 84, 69 of them shared. Three entries are gone, each deleted on purpose by one side (`merge-checks.txt` §2):

- `every received path is published empty` and `thisClock is appended to an absent path`: round 1 retired these for the 2011 rules.
- `the receipt timeout publishes nothing`: #92 replaced it.

### `b0473e6`: the #88 issue shapes' whole interval, after phase 40

- Cause. 802.1AS-2011 10.3.11 (Figure 10-13 as corrected by Cor1) ages an elected grandmaster when syncReceiptTimeout passes with gmPresent. #92 implements that rule.
  - Phase 8o's `defer_to_a_better_grandmaster` waited 1.05 s after electing a priority1 247 peer that sends no Sync.
  - The peer is now aged at 375 ms. The plane takes mastership and sends Announce, so "no Announce for one interval" fails.
  - The aged port then refuses every later Announce until Sync returns. That is the 200-check cascade: `receipts/engine-merge/merge-commit-98edabb-pass1.log`, 1968 checks, 200 FAIL.
- Rejected alternative: feeding Sync in place at 8o. It runs before phase 10 and spends usable pairs there, so phase 10's link-up pair is no longer the run's first; the generator leaves the servo locked across a GM change (S_LOCK). Base check "late FU never steers" then fails: got 0x14, exp 2 (`receipts/engine-merge/sync-fed-in-place-at-8o-pass1.log`).
- Fix:
  - `tb/verilator/engine/sim_main.cpp:5950-5975`: new phase 43, `defer_a_whole_interval_to_the_issue_shapes()`. It runs where phase 40 left GMS elected with usable Sync. A degraded GMS hands mastership back, then the issue's two shapes run as before: stepsRemoved 3 with one entry, and a head that is not the grandmaster.
  - `:425`: called after phase 40, ahead of the whole-run grades.
  - `:2663-2665`: the whole interval is now 1.125 s of the parent's usable Sync every 125 ms (main's `s39_interval`).
  - `:2634-2637`: the issue shapes' Announces now carry `phc() + 100` (the timestamp form main's phases use) instead of fixed stamps.
  - `:2608-2616`: 8o keeps its two count shapes.
  - Header: `:85-89` (8o) and `:218-222` (43).
- No check was added, removed or renamed. The suite is 1977 per shipping pass: main's 1805 plus round 2's 172 (1875 − 1703). The priority1 255 pass is 60: 59 + 1.

## Checks and mutants

No repository check is new this round. What the merge needs proven:

- Both arms killed in full, in the head engine gate log `receipts/head-repo/04.log`:
  - 112 `[PASS] mutant caught` lines plus the control; no `[FAIL]`, no "missed its named".
  - Every entry with a strict prefix printed every check it names as FAIL before its verdict (`merge-checks.txt` §3).

| Prefix | Mutants | Named checks printed FAIL |
|---|---:|---:|
| `#82 ` | 24/24 | 80/80 |
| `#84 ` | 6/6 | 13/13 |
| `#85 ` | 9/9 | 99/99 |
| `#87 ` | 2/2 | 19/19 |
| `#88 ` | 9/9 | 51/51 |
| `#89 ` | 15/15 | 38/38 |
| `#90 ` | 4/4 | 15/15 |
| `#91 ` | 3/3 | 7/7 |
| priority1 255 | 7/7 | 10/10 |

- The relocated phase-43 checks still bite. In the head arm:
  - `the path-count refusal restored` fails `#88 issue shape: no Announce for one interval got 0000000000000001 exp 0000000000000000`, and also elected, no longer master and count.
  - `the path-head refusal restored` fails `#88 head not the grandmaster: no Announce for one interval got 0000000000000001 exp 0000000000000000`, and also entry 0, parser accepts and more.
  - `the received head replaced by the grandmaster` fails `#88 head not the grandmaster: entry 0 is the received head got 00f5f5fffe000001 exp 00f5f5fffe0000a1`.

### Companion edits this round, and their mutants

Stacking the two companions needed six edits to the round-2 companion; none adds a check:

- `tb/verilator/milan_dp/sim_gptp.cpp:1398, 1434, 1491, 1527` (the four conflict hunks). #92's `run_selected` waits, which send the selected peer one Sync pair first, carry round 2's #87/#88 expectations.
- `:1305`. Round 2's new wait after the TLV-less refresh is `run_selected` too. Hunk 1 had dropped #92's two Sync-fed waits there, and that let the peer age before #207.
- `:1555-1557`. The served-head probe sends one usable pair first. The 8 M-cycle Sync-less leg before it leaves the port aged, and a pair heard as master clears that (main's phase 40).
- `:1590, 1602`. The entry-0-only probe waits are `run_selected`.
- `:1644-1669, 1677-1680`. In the #207 full-queue arm, the forced level is held at four on each of the 400 cycles in which s2's event arrives (it was poked once). The comments now say why.
  - The arm was racy on both stacks: its serializer is idle again while the MAC is held, and dispatch pops a stale entry inside the window.
  - With #92's companion alone, that pop lands after s2's refusal. Stacked, a periodic STREAM_OUTPUT GET_COUNTERS push is at the MAC first, the pop lands before, and s2's event is accepted.
  - Recorded with temporary probes on both stacks (not kept).
- `tb/verilator/tsn_fuzz/fuzz_ptp_timing.py:66-74`. `_btca_adopt` sends one usable pair heard as master first, as #92 does for its 12-hop vector: the rejection probes' master sent no Sync, so the port is aged.
- `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md`: regenerated once, after both companions. The change is the timestamp alone (675 pass).

Mutants and controls, each planted alone in a clone of the stacked snapshot (`receipts/companion-mutants/`, script `receipts/scripts/companion_mutants_r3.py`):

| Mutant or control | Suite | Result, first failing words |
|---|---|---|
| K1 control: the #207 arm pokes the level once (round 2's arm) on this stack | milan_dp `gptp` | 1 FAIL: `FAIL a full queue moves only the event count got 0000000000000000 exp 0000000000000001` |
| K2: the engine stops counting a full-queue refusal (`pev_valid_w && ann_reject_w`) | milan_dp `gptp` | 1 FAIL: the same check |
| K3 control: the BTCA adoptions send no Sync pair first | tsn_fuzz | 6 fail: `path-trace head is not the announced grandmaster (10.3.10.2.1): adopted`, `… one path-trace hop against stepsRemoved 1 (10.3.10.2.1): adopted`, parent, no longer grandmaster |
| `the path-head refusal restored` (engine arm) | tsn_fuzz | 4 fail: `path-trace head is not the announced grandmaster (10.3.10.2.1): adopted`, parent, no longer grandmaster, parser drop counter unmoved |
| `the path-count refusal restored` (engine arm) | tsn_fuzz | 5 fail: `one path-trace hop against stepsRemoved 1 (10.3.10.2.1): adopted`, … and the stepsRemoved-255 one-hop drop check |
| K6 control: the served-head probe sends no Sync pair first | milan_dp `gptp` | 7 FAIL: `#88 path headed elsewhere serves count three got …1 exp …3`, … `#88 GET_AS_PATH entry 0 is the received head` |
| GET_AS_PATH entry 0 served from the grandmaster (the old datapath) | milan_dp `gptp` | 7 FAIL: `#88 GET_AS_PATH entry 0 is the received head`, `entry-0-only change: GET_AS_PATH serves the new entry 0`, `entry-0-only change emits one GET_AS_PATH push`, … |
| C3: the AS_PATH comparator drops its entry-0 term | milan_dp `gptp` | 2 FAIL: `entry-0-only change emits one GET_AS_PATH push got …0 exp …1`, push body |
| `a TLV-less Announce publishes {thisClock}` (engine arm) | milan_dp `gptp` | 10 FAIL: `TLV-less fabric publication keeps the path count got …1 exp …5`, `TLV-less refresh emits no GET_AS_PATH push`, `#87 TLV-less GM switch: …` |

- The same hold arm on #92's companion alone: milan_dp `gptp` 185/185 (`receipts/companion-207/hold-arm-on-the-92-companion-alone.log`).
- The round-1 and round-2 companion checks and their mutant maps are unchanged (64 + 13).

## Base and head records

Every gate ran through the recorded runner, one command at a time, each with its own exit code, seconds and log, never piped.

- Environment:
  - Verilator 5.050 (pinned), with `-j 0` mapped to `-j 8` by a scratch wrapper and nothing else changed;
  - sv2v v0.0.12 (pinned) and Yosys 0.66 (the CI pin);
  - TMPDIR in scratch.
- Separate units, each with MemoryMax 6–10 G on its own CPU range.
- Head: a fresh clone at `b0473e69`. Base: a fresh clone at `3426089a`. Specs are in `receipts/specs/`.

| # | Repository gate | Base `3426089a` | Head `b0473e69` |
|---|---|---|---|
| 1 | `make contract` | rc 0 | rc 0 |
| 2 | `make -C tb/verilator/ucpu` | rc 0, 768/768 | rc 0, 768/768 |
| 3 | `make -C tb/verilator/parser` (run + mutants) | rc 0, 337/337; arm 9/9 | rc 0, 378/378; arm 16/16 |
| 4 | `make -C tb/verilator/engine` (4 passes + mutants) | rc 0, 1805 ×3 + 59; arm 101/101 (7127 s) | rc 0, 1977 ×3 + 60; arm 113/113 (7870 s) |
| 5 | `make -C tb/verilator/gaskets` | rc 0, 81/81; arm 5/5 | rc 0, 81/81; arm 5/5 |
| 6 | `make -C tb/tsngen` | rc 0, 288/288; arm 4/4 | rc 0, 288/288; arm 4/4 |
| 7 | `make -C bench/arty test` | rc 0, PASS | rc 0, PASS |
| 8 | `make lint` | rc 0 | rc 0 |
| 9 | `make docs` | rc 0, evidence 20 exact | rc 0, evidence 20 exact |
| 10 | `git diff --exit-code` after the run | rc 0 | rc 0 |
| + | `syn/ooc/check_ooc_clock.py --selftest` | — | PASS, 30 arms (`receipts/ooc-selftest/`) |

## Scratch-parent consumer gate table

Scratch clones of milan-fpga dev `97aab1d0`. All public submodules are initialised; the private `external` is not, since no gate builds it. Two local snapshots were committed and never pushed:

- Base `5a780e200381fa90afb16f50e0043b38f0569c78`: dev plus #92's companion `b53944d5`, with the gitlink at main `3426089a`.
- Head `723caf3492c27fd5de0e898a15083e26676dd332`: base plus this round's companion, with the gitlink at `b0473e69`.
  - A first full run on `6ec61b86`, which differs only in the #207 arm's comment, was also all rc 0. It was rerun in full on `723caf34` after the comment was corrected, and only the `723caf34` records are cited.

How the gates ran:

- The list is the manager template's full 15 commands, checked command for command against it. It includes both idiom checks and milan_dp's `gptp` and `gptp-lat` legs.
- At head, the commands ran as four units in four clones of the snapshot (receipts are numbered by template index). At base they ran as one unit.
- tsn_fuzz `ptp` (parent CI rtl.yml shard 1) ran in its own clone, with tsn-gen at the CI pin `deca300c`.

| # | Consumer gate | Base (`5a780e20`) | Head (`723caf34`) |
|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0 | rc 0 |
| 2 | `scripts/check_py_idiom.py` | rc 0 | rc 0 |
| 3 | `scripts/xvlog_gate.py --check` | rc 0, PASS | rc 0, PASS |
| 4 | `scripts/check_rtl_source_lists.py` | rc 0, OK | rc 0, OK |
| 5 | `sw/builder/test_builder.py` | rc 0, all pass except 1 NOT RUN | rc 0, same (gate 11, the host-dependent calibration arm, as in round 2) |
| 6 | `make -C tb/verilator/gptp_shadow -j8` | rc 0, 310/310; controls 9/9 | rc 0, 325/325; controls 9/9 |
| 7 | `scripts/check_port_contracts.py` | rc 0, OK | rc 0, OK |
| 8 | `scripts/measure_naming.py --check` | rc 0 | rc 0 |
| 9 | `scripts/measure_test_evidence.py --check` | rc 0 | rc 0 |
| 10 | `scripts/docs_check.py` | rc 0, 0 findings | rc 0, 0 findings |
| 11 | `scripts/lint_rtl.py --check` | rc 0 (89 <= 89) | rc 0 (89 <= 89) |
| 12 | `make -C tb/verilator/milan_dp gptp` | rc 0, 185/185 | rc 0, 200/200 |
| 13 | `make -C tb/verilator/milan_dp gptp-lat` | rc 0, 185/185 | rc 0, 200/200 |
| 14 | `make -C tb/verilator/milan_dp_gptp` | rc 0, RESULT PASS | rc 0, RESULT PASS (5234 s); its six verdict lines are identical to base |
| 15 | `make -C tb/verilator/milan_dp_gm_steps` | rc 0, 6/6 | rc 0, 6/6 |
| + | `make -C tb/verilator/tsn_fuzz ptp` (own clone) | rc 0: 677 pass, freshness PASS | rc 0: 675 pass, 0 fail, 0 known gaps; freshness PASS; the rewrite is the timestamp alone (`receipts/head-fuzz/test-results-rewrite.diff`) |

- milan_dp_gptp's ax1x1gptp physical leg counts 151 checks at head (155 in round 2). That leg's harness is changed only by #92's companion, which reshapes its loss window. The base run on #92's companion alone also counts 151, and its six verdict lines are identical to the head's.
- The tsn_fuzz count is 675 by design: the BTCA section's two retired-rule rejections are adoptions (round 1).

## Open items / notes

- Nothing was pushed and no PR was touched. Nothing was committed in a parent other than the local scratch snapshots. The companion lands with the gPTP pin adoption, after #92's.
- The #207 arm edit is in parent test code and outside path-trace publication proper. It was needed only to keep a pre-existing check deterministic once both companions stack. Its comment says why, and K1/K2 show that it still catches a lost refusal.
- Unchanged from round 1 (pre-existing since #85): d) is applied at the BTCA `take` that elects the sender, one Announce before a literal SlavePort reading. From the next Announce both readings agree.
- Not run: `make ooc` past its selftest (this host has no synthesis tool for it); hardware of any kind.
- Receipts: `receipts/INDEX.md` lists every file present (path, bytes, sha256 prefix). Host paths are replaced by named placeholders (`receipts/scripts/receipts.py`).
