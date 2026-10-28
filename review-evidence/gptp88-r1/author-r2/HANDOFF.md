# [A690c] HANDOFF — FPGA-gPTP #87 + #88, round 2 on PR #93 (R721-1)

Status: REVIEW READY at head `5ed415a7`. Every repository gate is rc 0 at base and head. The parent consumer list is 15/15 rc 0 at base, and at head with the new companion; tsn_fuzz `ptp` is rc 0.

- Repository: Mister-M-alt/FPGA-gPTP, branch `87-88-announce-pathtrace` (local, not pushed)
- Base: main `55680bff3b287b9a7b0c759f51471fa617c17335`
- Round-1 head: `c1bc9e21a273fd8506b4806a2470fb7bab13f72f`
- Round-2 head: `5ed415a7f072fe218500adedde64659c95c69804`, two commits on `c1bc9e21`:
  - `7c71dcb` Hold the two #87 engine mutants to every check they name (#87)
  - `5ed415a` Restore the space in the parser arm's PAIRS assignment (#88)
- The PR is seven commits on main `55680bff`.
- Round-2 assignment: #88 issuecomment-6460926505 (link corrected in issuecomment-6460927866). It answers R721-1, PR #93 issuecomment-6460897668 (F1, F2, F3 MINOR; S1 SUGGESTION).
- TAKEN: #88 issuecomment-6460933232.
- REVIEW READY (head `5ed415a7`): #88 issuecomment-6463142482.

## Findings and what was done

| Finding | Required outcome | Done |
|---|---|---|
| F1 | `"#87 "` in the strict prefixes at `mutants.py:894`, comment at `:892` | `tb/verilator/engine/mutants.py:892-895` (`7c71dcb`). Engine arm 85/85 at head; both #87 controls print every named FAIL line (12 and 7). A control shows the old arm passes them with their checks silenced and the new arm refuses them. |
| F2 | companion updates `REGISTER_MAP_CLASSES.md:102` to the 2011 rules | Companion `docs/reference/REGISTER_MAP_CLASSES.md:102`. `grep -n "count zero\|count ? GM"` is empty; `docs_check.py` rc 0. |
| F3 | parent checks: an entry-0-only change at equal count and tail in both detectors, and a control that fails each | gptp_shadow: one generation step. milan_dp `gptp`: one generation, one GET_AS_PATH push, new entry 0 served. Control C2 fails both benches. Control C3 fails the push check. |
| S1 | `PAIRS = ((` | `tb/verilator/parser/mutants.py:134` (`5ed415a`), as at base. Parser arm 16/16. |

## Changes (file:line)

Repository, at `5ed415a7`:

- `tb/verilator/engine/mutants.py:892-895` (F1). `named_verdict` holds controls whose `breaks` start with `#82 `, `#84 `, `#85 `, `#87 `, `#88 ` or the priority1-255 prefix to every check they name. The line count is unchanged (998), under the parent's 1000-line Python ratchet.
- `tb/verilator/parser/mutants.py:134` (S1): whitespace only.
- No RTL, generator, harness, doc or ROM change. The suite tallies are the same as round 1.

milan-fpga companion, scratch snapshot `3f936ba7149c8d3311479cd2b76e72dd766a4341`:

- The snapshot is dev `97aab1d0` plus the patch, with the gptp-processor gitlink at `5ed415a7`. It is a local commit and was never pushed.
- `docs/reference/REGISTER_MAP_CLASSES.md:102` (F2), the 0x7DC–0x7E4 row:
  - eight identities from entry 0, by 802.1AS-2011 10.3.10.2.1 d);
  - a TLV is copied as received, its head included, and thisClock is appended;
  - an empty TLV gives `{thisClock}`;
  - an Announce without a TLV writes nothing, so the previous pathTrace stays (`{thisClock}` after reset or mastership);
  - Table 5.22 compares `(count ? entry 0 : 0, count, active tails)`, and a GM change that leaves the served sequence unchanged is silent.
- `tb/verilator/gptp_shadow/sim_main.cpp` (F3):
  - `:898-937`: the #88 steps move into `check_the_path_is_served_from_its_head()`. This keeps `check_announce_adoption_and_path_trace` under the parent's 100-line C++ function limit (`check_cpp_idiom.py`, F.3).
  - New step at `:922-935`: `{PATH_HOP, GM}` is followed by `{PATH_HOP2, GM}`. Count 3, tail 1 = GM and tail 2 = thisClock are equal; only the head moves. The step spends exactly one path generation.
  - `:1001-1009`: the restore and eight-entry Announces take sequence ids 19 and 20. The restore's generation is now counted from the new step. The receive path does not check Announce sequenceId.
  - 325 checks (320 in round 1).
- `tb/verilator/milan_dp/sim_gptp.cpp` (F3):
  - `:1565-1603`: `prove_an_entry_zero_change_is_a_path_change()`, called last in the leg (`:1861`). The served path `{PATH_B3, PEER, thisClock}` becomes `{PATH_B2, PEER, thisClock}`. The probe checks:
    - one generation and count 3 at 0x7E4;
    - one GET_AS_PATH push;
    - the solicited response: count 3, entry 0 `PATH_B2`, entry 1 the parent, thisClock last;
    - the push body equal to the solicited path.
  - The probe first re-sends REGISTER_UNSOLICITED_NOTIFICATION. That late in the leg the first registration has passed its IEEE 1722.1-2021 7.4.37.2 timeout (300 s, compressed in this bench), and no unsolicited message of any kind leaves. Receipts:
    - `receipts/companion-probe-placement/end-of-leg-without-reregistration.txt`: 0 pushes in 2.2 M cycles, including the served-head change from count 1 to 3;
    - `after-207-without-reregistration.txt`: pushes resume earlier in the leg.
  - It goes at the end because the #207 drop-counter block is cycle-timed. Its status is not graded: a refused registration fails the push check.
  - 200 checks in both the `gptp` and `gptp-lat` legs (192 in round 1).

Companion patch: `milan-fpga-companion.patch` beside this file is `git diff 97aab1d0 3f936ba7 -- . ':(exclude)gptp-processor'`. The same command at the round-1 snapshot gives round 1's `fa3c22f0…`.

- sha256 `259fa9d889e89cccff84736a2509829faf3bf0f7fea1a0b1a2dbb41260cd1418` (81806 bytes; round 1 `fa3c22f0a2856f4e3fd79fda60cdfdcd9b281492da564ca4123c69145d71a986`).
- It applies cleanly to dev `97aab1d0`; the result equals the snapshot tree, the gitlink aside. It reverses cleanly on the snapshot.
- Compared with round 1, it adds only the three files above.
- The microcode generator is untouched (left to PR #92).

## New checks, mutants, failing words

### F1: the arm's strictness for #87 controls

The new check is the arm's own verdict. Control, `receipts/f1-control/`, script `receipts/scripts/f1_control.py`:

- Two trees at `5ed415a7`. In each, the harness's `"#87 G1 to G2 without a TLV"` checks are renamed to `"#87 G1 to G2 sans TLV"` (one line, `sim_main.cpp:2646`), so they can never print under the names the two #87 mutants give.
- The `old` tree carries the round-1 `mutants.py` (`c1bc9e21`), the `new` tree this head's.
- The arm's own control, then its own `run_mutant()`, ran for the two #87 mutants:

| Arm | "the empty sequence published without a TLV" | "a TLV-less Announce publishes {thisClock}" |
|---|---|---|
| round 1 (`c1bc9e21`) | `[PASS] mutant caught` (survives the silenced checks) | `[PASS] mutant caught` |
| head (`5ed415a7`) | `[FAIL] mutant 'the empty sequence published without a TLV' missed its named check(s): #87 G1 to G2 without a TLV: count; #87 G1 to G2 without a TLV: its commit names the grandmaster and path` | `[FAIL] mutant 'a TLV-less Announce publishes {thisClock}' missed its named check(s): #87 G1 to G2 without a TLV: count; #87 G1 to G2 without a TLV: head` |

The unmutated control passes in both trees. At the real head harness, the engine gate's arm (`receipts/head-repo/04.log`) catches both. Each prints every check it names before its `[PASS]` line: 12 of 12 and 7 of 7.

### F3: the parent checks and their controls

Controls, each planted alone in a clone of the snapshot, running gptp_shadow `run` and milan_dp `gptp` (`receipts/companion-mutants/`, script `receipts/scripts/companion_mutants_r2.py`):

- C2, the shadow path generation compares entries 1..7 only (`pub_path_next_w[8*64-1:64] != pub_path_o[8*64-1:64]`):
  - gptp_shadow 2 FAIL: `FAIL entry-0-only change spends one path generation got 0000000000000005 exp 0000000000000006`, and the next step's `FAIL restored path spends one generation`;
  - milan_dp `gptp` 1 FAIL: `FAIL entry-0-only change advances generation once got 0000000000000008 exp 0000000000000009`.
- C3, the Table 5.22 comparator `gsi_asp_chg_w` without its `asp_live_head_w` term:
  - milan_dp `gptp` 2 FAIL: `FAIL entry-0-only change emits one GET_AS_PATH push got 0000000000000000 exp 0000000000000001` and `FAIL entry-0-only push body equals solicited path …`;
  - gptp_shadow passes, as it should: the shadow does not hold this comparator.
- Both are R721-1's probes C2 and C3 as described. The reviewer's own scripts are not public, so these edits are mine.

Every check name new since the round-1 companion fails under at least one planted mutant: 13 of 13, from 9 mutants (`receipts/companion-mutants/coverage-r2.md`, script `coverage_r2.py`).

| Mutant | gptp_shadow FAIL | milan_dp gptp FAIL |
|---|---:|---:|
| C2 the shadow path generation compares entries 1..7 only | 2 | 1 |
| C3 the AS_PATH comparator drops its entry-0 term | 0 | 2 |
| GET_AS_PATH entry 0 served from the grandmaster (the old datapath) | 0 | 7 |
| the shadow drops entry 0 (the old seven-slot canonicaliser) | 9 | 10 |
| the shadow drops entry 1 (new) | 5 | 4 |
| the received path is published without thisClock (engine arm) | 14 | 24 |
| thisClock lands one slot early (engine arm) | 4 | 6 |
| the appended entry is the announcing source (engine arm) | 4 | 6 |
| the received head replaced by the grandmaster (engine arm) | 4 | 5 |

The round-1 companion's 64 new checks and their mutant map are unchanged (round-1 handoff).

## Base and head records

Every gate ran through the recorded runner, one command at a time, each with its own exit code, seconds and log, never piped.

- Environment: Verilator 5.050 (pinned), with `-j 0` mapped to `-j 8` by a scratch wrapper and nothing else changed; sv2v v0.0.12 (pinned); Yosys 0.66 (the CI pin); TMPDIR in scratch.
- Separate units, MemoryMax 10G (mutation units 5-8G), on free CPU ranges.
- Head: a fresh clone at `5ed415a7` (`receipts/head-repo/`, spec `receipts/specs/head-repo.json`).
- Base: `55680bff` is unchanged, so [A690]'s base records are reused as in round 1. They come from the same environment and the same command list (`receipts/base-reused/`).

| # | Repository gate | Base `55680bff` | Head `5ed415a7` |
|---|---|---|---|
| 1 | `make contract` | rc 0 | rc 0 |
| 2 | `make -C tb/verilator/ucpu` | rc 0, 768/768 | rc 0, 768/768 |
| 3 | `make -C tb/verilator/parser` (run + mutants) | rc 0, 337/337; arm 9/9 | rc 0, 378/378; arm 16/16 |
| 4 | `make -C tb/verilator/engine` (4 passes + mutants) | rc 0, 1703 ×3 + 53; arm 73/73 | rc 0, 1875 ×3 + 54; arm 85/85 (4321 s) |
| 5 | `make -C tb/verilator/gaskets` | rc 0, 81/81; arm 5/5 | rc 0, 81/81; arm 5/5 |
| 6 | `make -C tb/tsngen` | rc 0, 288/288; arm 4/4 | rc 0, 288/288; arm 4/4 |
| 7 | `make -C bench/arty test` | rc 0, PASS | rc 0, PASS |
| 8 | `make lint` | rc 0 | rc 0 |
| 9 | `make docs` | rc 0, evidence 20 exact | rc 0, evidence 20 exact |
| 10 | `git diff --exit-code` after the run | rc 0 | rc 0 |
| + | `syn/ooc/check_ooc_clock.py --selftest` | PASS, 30 arms | PASS, 30 arms (`receipts/ooc-selftest/`) |

## Scratch-parent consumer gate table

Scratch clones of milan-fpga dev `97aab1d0`. All public submodules are initialised; the private `external` is not, since no gate builds it. Nothing was pushed.

- Base: `97aab1d0` itself, gitlink `55680bff`. [A690]'s records are reused, as in round 1 (`receipts/base-reused/base-parent*`, `base-fuzz`).
- Head: snapshot `3f936ba7149c8d3311479cd2b76e72dd766a4341`, which is the round-2 patch committed with the gitlink at `5ed415a7`.
  - Records: `receipts/head-parent/` and `receipts/head-fuzz/`; specs in `receipts/specs/`.
  - Each gate ran in its own clone of the snapshot (`receipts/scripts/mkclone.sh`), and the gate clone is clean and on the snapshot afterwards.
- The list is the manager template's full 15 commands, checked command for command against it. It includes both idiom checks and milan_dp's `gptp` and `gptp-lat` legs.
- tsn_fuzz `ptp` (parent CI rtl.yml shard 1) runs in its own clone, because it rewrites its `TEST_RESULTS.md` timestamp.

| # | Consumer gate | Base (gitlink `55680bff`) | Head (`3f936ba7`, gitlink `5ed415a7`) |
|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0 | rc 0 |
| 2 | `scripts/check_py_idiom.py` | rc 0 | rc 0 |
| 3 | `scripts/xvlog_gate.py --check` | rc 0, PASS | rc 0, PASS |
| 4 | `scripts/check_rtl_source_lists.py` | rc 0, OK | rc 0, OK |
| 5 | `sw/builder/test_builder.py` | rc 0, all pass except 1 NOT RUN | rc 0, same (the same host-dependent calibration arm, gate 11) |
| 6 | `make -C tb/verilator/gptp_shadow -j8` | rc 0, 310/310 | rc 0, 325/325; its mutation arm and lifecycle PASS |
| 7 | `scripts/check_port_contracts.py` | rc 0 | rc 0 |
| 8 | `scripts/measure_naming.py --check` | rc 0 | rc 0 |
| 9 | `scripts/measure_test_evidence.py --check` | rc 0 | rc 0 |
| 10 | `scripts/docs_check.py` | rc 0, 0 findings | rc 0, 0 findings |
| 11 | `scripts/lint_rtl.py --check` | rc 0 (89 <= 89) | rc 0 (89 <= 89) |
| 12 | `make -C tb/verilator/milan_dp gptp` | rc 0, 185/185 | rc 0, 200/200 |
| 13 | `make -C tb/verilator/milan_dp gptp-lat` | rc 0, 185/185 | rc 0, 200/200 |
| 14 | `make -C tb/verilator/milan_dp_gptp` | rc 0, RESULT PASS | rc 0, RESULT PASS (4899 s); 215 verdict lines, identical to round 1's head run |
| 15 | `make -C tb/verilator/milan_dp_gm_steps` | rc 0, 6/6 | rc 0, 6/6 |
| + | `make -C tb/verilator/tsn_fuzz ptp` (own clone, tsn-gen at the CI pin `deca300c`) | rc 0: 677 pass, freshness PASS | rc 0: 675 pass, 0 fail, 0 known gaps; freshness PASS. Its rewrite of `TEST_RESULTS.md` is the timestamp alone (`receipts/head-fuzz/test-results-rewrite.diff`) |

- Round 2 changes no parent RTL, so the round-1 extras still stand: the csr suite (its lockstep and controls) and gptp_txts, rc 0 at the round-1 snapshot.
- The tsn_fuzz count is 675 by design: the BTCA section's two retired-rule rejections became adoptions (round 1).

## Open items / notes

- Nothing was pushed, no PR was touched, and nothing was committed in a parent other than the local scratch snapshot. The companion lands with the gPTP pin adoption.
  - The microcode generator is untouched here; it is left to PR #92.
  - If #89/#90/#91's companion also touches tsn_fuzz, regenerate `TEST_RESULTS.md` once, after both.
- The milan_dp gPTP leg's unsolicited registration lapses before its end, by the 7.4.37.2 registration timeout (300 s, compressed in this bench). That is the cause of round 1's note that no push leaves that late. The new probe registers again; nothing else depends on it.
- Unchanged from round 1 (pre-existing since #85): d) is applied at the BTCA `take` that elects the sender, one Announce before a literal SlavePort reading. From the next Announce both readings agree.
- Not run: `make ooc` past its selftest (this host has no synthesis tool for it); hardware of any kind.
- Receipts: `receipts/INDEX.md` lists every file present (path, bytes, sha256 prefix). Host paths are replaced by named placeholders (`receipts/scripts/receipts.py`).
