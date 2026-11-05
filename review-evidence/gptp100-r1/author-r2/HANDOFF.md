# [A733b] HANDOFF: FPGA-gPTP #100 round 2 (PR #101): merge main 5184fb3, wording residue

Status: REVIEW READY at head 84fd227 (2026-11-06). The merge of main 5184fb3 and the three wording items are done. Every gate is rc 0 on clean clones of the head, in the repository and in the scratch parent. Nothing is pushed.

- Repository: Mister-M-alt/FPGA-gPTP (origin `https://github.com/Mister-M-alt/FPGA-gPTP.git`), branch `100-followup-tlv-values`.
- Round-1 head: `3e3f0418ad081e5906d02d872614fe3a81e148e5` (PR #101). Main: `5184fb36e34926d007f1ca4d5121863faf9b89fa`.
- Head: `84fd22781c95f7b7e65d7d18c99a5ed49a68e11c` (four commits on 3e3f041; nothing pushed).
- Issue posts: TAKEN issuecomment-6670625787; REVIEW READY 84fd227 issuecomment-6672361457.

## Commits

| Commit | Subject |
|---|---|
| `1615187` | Merge main 5184fb3 into 100-followup-tlv-values (parents 3e3f041, 5184fb3) |
| `1400c83` | Name region 6's three Follow_Up TLV fields and their scales in the developer guide (#100) |
| `1d61f9e` | Define lastGmPhaseChange by 11.4.4.3.8 and say the plane sends its last slave offset (#100) |
| `84fd227` | Read CLOCK_ACCURACY_UNKNOWN_C in the --clock-accuracy help, where 0xFE is chosen (#100) |

## 1. Merge of main 5184fb3

`git merge --no-ff origin/main` (origin/main resolved to `5184fb36e3...` by `git rev-parse`).

Conflicts: one, `docs/SOURCE_EVIDENCE.md`, one hunk (the five rows from "Deferred receive event" to "Accepted-beat result face").

| Row | Branch (3e3f041) | Main (5184fb3) | Resolution |
|---|---|---|---|
| Deferred receive event | `KL_gptp_rx_parser.sv#L392` | `#L439` | main's `#L439` (the parser is main's) |
| Four-entry event queue | `KL_gptp_engine.sv#L559` | `#L467` | the branch's `#L559` (the engine is the branch's) |
| Parser arbitration priority | `#L586` | `#L494` | the branch's `#L586` |
| Priority timestamp return | `#L407` | `#L405` | the branch's `#L407` |
| Accepted-beat result face | `#L413` | `#L411` | the branch's `#L413` |
| Ignored receive flag bits | `KL_gptp_rx_parser.sv#L472` | `#L521` | merged without conflict to main's `#L521` |

So the file is this branch's file with main's two parser anchors, as the round-1 handoff recorded. `python3 scripts/check_source_evidence.py` on the merge: "source evidence: 20 exact, 0 findings", rc 0. No other anchor moved: the engine and generator are byte-identical to 3e3f041 at the merge, and the parser anchors are main's.

Auto-merged without conflict: `docs/HDL_DEVELOPER.md`, `docs/INTEGRATION.md`, `docs/MANAGER.md`, `docs/TEST_DEVELOPER.md`, `tb/verilator/engine/sim_main.cpp` (two comment hunks from #98, outside the `#100` section). Taken from main alone: `docs/README.md`, `hdl/wire/KL_gptp_rx_parser.sv`, `tb/verilator/parser/{Makefile,README.md,mutants.py,sim_main.cpp}`.

The first merge commit (`c169aad`) kept git's "# Conflicts:" comment lines as a body, because `git commit --no-edit` does not strip comments. It was never pushed; its message was amended to the bare subject (`1615187`, same tree and parents).

## 2. Residue (wording only; no RTL, generator output or harness change)

| Item | File:line at head | Change | Clause |
|---|---|---|---|
| R777-1 R1 | `docs/HDL_DEVELOPER.md:328`, `:330` (the review's `:320`, moved by the merge's eight parser lines) | "Region 6 serves all three fields as ScaledNs and scaled." becomes "Region 6 serves gmTimeBaseIndicator, lastGmPhaseChange as ScaledNs." and "It also serves scaledLastGmFreqChange, scaled by 2^41." | 11.4.4.3.7 to 11.4.4.3.9 |
| R778-1 S3 | `docs/INTEGRATION.md:857-865` | "lastGmPhaseChange is the last slave offset, as ScaledNs." becomes five sentences: 11.4.4.3.8 defines it as a ScaledNs; it is the current grandmaster's time minus the previous one's; it is taken when the current grandmaster became grandmaster; this plane sends the offset last measured as a slave; that offset is not extrapolated to the handover | 11.4.4.3.8 |
| R778-1 S4 | `hdl/ucode/gen_gptp_ucode.py:2612` (constant at `:553`) | The `--clock-accuracy` help, the place the build parameter's 0xFE alternative is chosen, now reads `CLOCK_ACCURACY_UNKNOWN_C` (`f"0x{CLOCK_ACCURACY_UNKNOWN_C:02X} when the "`). `--help` prints the same "0xFE when the oscillator is not characterised". `grep` now shows a reader | 8.6.2.3 b) |

**R777-1 R1's exact text and the docs gate.** The review's exact sentence is 13 words. The repository's docs gate (`scripts/check_docs.py`, `MAX_WORDS = 10`) refuses it: "docs check: FAIL (1 findings) docs/HDL_DEVELOPER.md:328: 13 words: Region 6 serves gmTimeBaseIndicator, lastGmPhaseChange as ScaledNs and scaledLastGmFreqChange scaled by 2^41." (receipt `receipts/residue/r777-r1-exact-text-docs-check.log`, rc 1). The committed wording keeps every word of the review's text in its order, split into two sentences at "and". The only changes are a full stop after "ScaledNs", "and" becoming "It also serves", and a comma before "scaled". The docs gate passes on it. Changing the docs gate's rule was not part of this round.

**S3's wording, in the same gate.** A clause number counts as five words in that gate, so the definition is spread over three short sentences. It is wording only: `KL_gptp_engine.sv` and `gen_gptp_ucode.py`'s ROM are unchanged, and the regenerated ROM images match the committed ones (repository gate 13).

## 3. Not changed this round (to the residue checklist)

- R778-1 S1 (grade scaledLastGmFreqChange exactly, plant the truncation probe), S2 (a Sync between an Announce's end and its handler, plant R7), S5 (parent `OUR_CQ` names), S6 (an elaboration bound on `CLK_HZ_P` for the TLV multiply).
- R777-1 S1 to S3 are the same findings as R778-1 S1, S6 and P1 (the BTCA literal 3000 against `ANN_RTO_MS_C`); R777-1 S4 is R778-1 S4, done above.
- R777-1 R2 and S5 belong to the parent re-pin PR (builder wording, and whether 0x22 covers every parent configuration).

## 4. Gate table (repository, clean clone of head 84fd227)

Each run was a recorded-gates unit (MemoryMax 10G, `MAKEFLAGS=-j4`, `VERILATOR_JOBS=4`, the pinned Verilator 5.050, Vivado 2026.1) in its own clone of the lane at 84fd227, never the lane's working tree. Every command rc 0, none piped.

Receipts: `receipts/final/repo-gates-84fd227/`, `receipts/final/engine-arm-84fd227/jobs.md`, `receipts/final/engine-arm-run-84fd227/`, `receipts/merge/diff-check-5184fb3.log`.

| # | Gate | rc | Tally |
|---:|---|---:|---|
| 1 | `make contract` | 0 | PHC interface contract: PASS |
| 2 | `make -C tb/verilator/ucpu` | 0 | 768 checks: 768 PASS, 0 FAIL |
| 3 | `make -C tb/verilator/parser` (suite and the parser mutation arm, in full) | 0 | 482 checks: 482 PASS; mutation arm 35 checks: 35 PASS (the control and 34 mutants, each caught) |
| 4 | `make -C tb/verilator/engine run` | 0 | 2098 / 2098 / 2098 PASS (shipping, request-seeded, Sync-seeded), 61 PASS (fourth pass, `--p1 255 --clock-accuracy 0xFE`) |
| 5 | engine mutation arm, in full (`make -C tb/verilator/engine mutants`'s jobs, run by `arm_jobs.py --jobs 8`), then `git diff --exit-code --stat` and `git status --porcelain` | 0 | 160 checks: 160 PASS, 0 FAIL: the unmutated control and 159 mutants, all 24 #100 controls among them, each caught by name; 4,286 s; tree clean after |
| 6 | `make -C tb/verilator/gaskets` | 0 | 81 checks PASS; mutation arm 5 PASS |
| 7 | `make -C tb/tsngen` | 0 | 288 checks PASS; mutation arm 4 PASS |
| 8 | `make -C bench/arty test` | 0 | PASS: two MII done toggles carried tags |
| 9 | `make lint` | 0 | Verilator `--lint-only -Wall`, engine and bench tops |
| 10 | `make docs` (the docs gate and the source-evidence checker, each with its selftest, and the diagrams) | 0 | docs check PASS (14 current, 18 historical pages); docs selftest PASS (127 arms); source evidence 20 exact, 0 findings; selftest PASS (7 arms); diagrams PASS |
| 11 | `make diagrams-check` | 0 | diagram check PASS, selftest PASS (10 arms) |
| 12 | `make ooc` | 0 | clock-order selftest PASS (30 arms); both syntheses' logs and timing reports PASS; figures below |
| 13 | `git diff --exit-code --stat` | 0 | the regenerated ROM images match the committed ones |
| 14 | `git status --porcelain` | 0 | nothing untracked |
| 15 | `git diff --check 5184fb3 84fd227` | 0 | no whitespace errors |

The engine counts equal round 1's at 3e3f041, as expected: the merge brings no engine RTL, generator or engine-harness check change. The parser counts are main's (482 + 35, from PR #99).

`native-shards.py` shards `scripts/run_all_suites.sh`, which FPGA-gPTP does not have (the script asserts exactly one such command in its spec). As in round 1, the sweep ran as recorded-gates units instead. They were pinned to this lane's own booking, 48-63: main's OOC run on 48-51, the repository list on 52-55, the engine arm on 56-63, then milan_dp_gptp on 48-51. The parent's list A ran on 0-15, the range `cpu_ranges.py pick` returned just before its launch. MemAvailable read 50 to 57 GB at every check. Each unit had MemoryMax 10G. MemoryCurrent, read once mid-run, was 0.15 to 0.46 GB, and milan_dp_gptp's unit peaked at 1.55 GB (MemoryPeak).

## 5. Area and timing (processor's own gates)

`make ooc` (Vivado 2026.1 out-of-context synthesis, xc7a100tfgg484-2, clk 10 ns from `ooc_clock.xdc`). Receipts: `receipts/ooc-5184fb3/`, `receipts/ooc-84fd227/`, `receipts/ooc-figures.md`, `receipts/base/ooc-run-5184fb3/`. Round 1's figures are in its own handoff.

| Top | Run | LUTs (logic + LUTRAM) | FFs | BRAM tiles | DSPs | WNS | TNS | Failing / total endpoints |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `KL_gptp_ucpu` | main 5184fb3 | 1,643 (1,511 + 132) | 733 | 1.5 | 4 | +1.941 ns | 0 | 0 / 3,165 |
| `KL_gptp_ucpu` | head 84fd227 | 1,643 (1,511 + 132) | 733 | 1.5 | 4 | +1.941 ns | 0 | 0 / 3,165 |
| `KL_gptp_engine` | main 5184fb3 | 4,920 (4,430 + 490) | 3,461 | 1.5 | 4 | +2.249 ns | 0 | 0 / 12,004 |
| `KL_gptp_engine` | head 84fd227 | 5,395 (4,905 + 490) | 3,620 | 1.5 | 6 | +2.043 ns | 0 | 0 / 12,372 |
| `KL_gptp_engine` | round 1 3e3f041 (before the merge) | 5,425 (4,935 + 490) | 3,618 | 1.5 | 6 | +2.043 ns | 0 | 0 / 12,372 |

Against main, the engine adds 475 LUTs, 159 FFs and two DSPs (the TLV frequency multiply), and slack falls by 0.206 ns, to +2.043 ns at 10 ns. The microCPU is unchanged. Against round 1's head, the merged engine is 30 LUTs smaller and 2 FFs larger. That is PR #99's parser, which on its own took main from 4,926 LUTs and 3,459 FFs to 4,920 and 3,461.

## 6. Scratch-parent consumer gate table

Scratch parent: `$VALIDATION_STORAGE/scratch/gptp100-parent`, round 1's clone of `$LANES/trusted-dev-20261104-604899c0` (milan-fpga dev `604899c0`) with round 1's companion commits. The gitlink was re-pointed and committed locally, never pushed: `2278661f24` "Consumer check: gptp-processor at 84fd2278", on `94a9f1860f` (round 1's 3e3f041 gitlink). milan_dp_gptp ran in round 1's second clone (`gptp100-parent-C`), moved to `2278661f24` with its gptp-processor from the first. Before every submodule git command, `git -C <dir> rev-parse --show-toplevel` was checked to be that directory. The parent's xvlog gate reports "pinned at: ... gptp-processor@84fd2278 - the superproject gitlink".

List A, `receipts/final/parent-A-84fd227/` (one unit, commands in this order, none piped):

| # | Gate | rc | Tally |
|---:|---|---:|---|
| 1 | `make -C tb/verilator/gptp_shadow -j8` | 0 | 325 checks: 325 PASS, 0 FAIL |
| 2 | `make -C tb/verilator/milan_dp gptp` | 0 | 210 checks: 210 PASS, 0 FAIL |
| 3 | `make -C tb/verilator/milan_dp gptp-lat` | 0 | 210 checks: 210 PASS, 0 FAIL |
| 4 | `make -C tb/verilator/gptp_plane` | 0 | RESULT: PASS; 29 PASS; phc_step 62 checks, 0 failures; campaign 8 PASS |
| 5 | `make -C tb/verilator/gptp_txts` | 0 | gptp_txts 95 checks, 0 failures (three shapes); controls 13, 0 failures |
| 6 | `make -C tb/verilator/gptp_tables` | 0 | gptp_tables 36 checks, 0 failures; controls 26, 0 failures |
| 7 | `make -C tb/verilator/tsn_fuzz ptp` | 0 | built the gPTP slice; field campaign SKIPPED (packet generator not installed), not a pass |
| 8 | `make -C tb/verilator/milan_dp_gm_steps` | 0 | gmstep 196 checks, 0 failures; 6 PASS |
| 9 | `python3 scripts/check_cpp_idiom.py` | 0 | |
| 10 | `python3 scripts/check_py_idiom.py` | 0 | (covers the generator's new f-string help) |
| 11 | `python3 scripts/xvlog_gate.py --check` | 0 | xvlog gate: PASS (0 findings == ratchet; 85 hdl/ files, 52 pinned-processor files) |
| 12 | `python3 scripts/check_rtl_source_lists.py` | 0 | |
| 13 | `python3 scripts/check_port_contracts.py` | 0 | |
| 14 | `python3 scripts/measure_naming.py --check` | 0 | |
| 15 | `python3 scripts/measure_test_evidence.py --check` | 0 | |
| 16 | `python3 scripts/docs_check.py` | 0 | |
| 17 | `python3 scripts/lint_rtl.py --check` | 0 | PRAGMA GATE PASS; LINT GATE PASS (89 <= ratchet 89) |
| 18 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs a LiteX place report that is not on this machine (not gPTP; the same NOT RUN as round 1) |
| 19 | `git status --porcelain` | 0 | clean |

List B, `receipts/final/parent-B-84fd227/` (the scheduled physical gPTP suite; beyond the three named gates, run because the gitlink now carries PR #99's parser):

| # | Gate | rc | Tally |
|---:|---|---:|---|
| 1 | `make -C tb/verilator/milan_dp_gptp` | 0 | ax1x1gptp physical 151 checks, 0 failures (RESULT: PASS); setup abort 6, no-TX accounting 20, no-Pdelay accounting 14, recentre controls 14, each 0 failures; 5,317 s |
| 2 | `git status --porcelain` | 0 | clean |

The parent companion change is round 1's, unchanged (`../gptp100-a733/milan-fpga-companion.patch`): the merge and this round's wording move nothing the parent pins.

## 7. Notes

- **No STOP.** No behaviour changes this round. No top-level port, parameter or register map changes: the only non-documentation line is the generator's help text, and the ROM images are byte-identical (repository gate 13).
- **One merge, no rebase, no force.** The merge commit's message was amended once, before anything was pushed, to drop git's "# Conflicts:" comment lines (section 1). That is the only history rewrite, and it touched only local, unpushed history.
- **tsn_fuzz** skipped its field campaign again, because its packet generator is not installed. It is not one of the assigned gates.
- **Scratch.** Clones, specs and raw logs live under `$VALIDATION_STORAGE/scratch/gptp100-a733b` (runs `r2-fast`, `r2-arm`, `main-ooc`) and the two scratch parents. None of it is pushed.
