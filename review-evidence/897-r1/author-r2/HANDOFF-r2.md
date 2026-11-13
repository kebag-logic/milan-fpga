# HANDOFF round 2 — lane 897 (A776): the split's GET_AS_PATH, synced onto dev-soft-core after #810

Status: **DONE** (2026-11-13 20:5x CET): the final clean-clone pass at `3bebf03a` is green, every acceptance item holds and no STOP condition was met. `PR-BODY.md` is ready for the manager, and REVIEW READY is posted on #897: issuecomment-6863354920 (`REVIEW-READY-COMMENT.md`).
Round 1 head: `5e6fef3ee74dcf6766ac3923349ae83524bc0e7b` (R833-1 and R834-1 POSITIVE at that head).
**Final head: `3bebf03a1d25bcbde9c0ec48dfd711af7280131e`**. Nothing pushed.
Worktree: `$LANES/897-aspath`, branch `897-split-as-path`. PR #898 targets `dev-soft-core`.

| Commit | Subject |
|---|---|
| `d3202fa2` | the sync merge of `dev-soft-core` `cec88385` (#810 merged), one merge commit |
| `d395f682` | `SPLIT_CONTROL_MEMORY.md` sections 5 and 6, the plat and split-boot READMEs: the images' sizes at the composed head |
| `3bebf03a` | `tb/verilator/ctrl_service_budget/build.py` held within the 1,000-line module limit (a comment rewrapped) |

## 1. Sync (item 1)

- `git fetch origin`: `origin/dev-soft-core` = `cec88385ad0a0ec0d61b91597640797766e45010` (the #810 merge); `7f50ee6a` (round 1's base) is its ancestor and the merge base. Submodule pins are the same on both sides (protocol-processor `a9e84b66`, gptp-processor `135afd04`, lwSRP `08ee86e8`, tsn-c-stack `715589c1`).
- `git merge --no-ff origin/dev-soft-core`: one merge commit `d3202fa2`. 8 files changed on both sides; 6 auto-merged, 2 conflicted.

| File | How | Resolution |
|---|---|---|
| `docs/design/MAILBOX_SPLIT.md` (host tests table) | conflict, two rows | the AECP face row from this branch (base row + the GET_AS_PATH tests; dev-soft-core left it unchanged), the planted-defects row from dev-soft-core ("twelve of them in the default `make`"; this branch left it unchanged) |
| `docs/design/SPLIT_CONTROL_MEMORY.md` (section 5, round 29's block) | conflict, three lines against two | dev-soft-core's platform paragraph (60.0 entry, `plat_ledger.py`) and its harness-arm paragraph (58.5 cap); this branch's GET_AS_PATH paragraph kept between them, then restated at the composed head in `d395f682` |
| `sw/firmware/ctrl/plat/README.md`, `sw/firmware/ctrl/test/test_aecp.cpp`, `sw/firmware/gtest/coverage.ratchet`, `tb/verilator/ctrl_service_budget/{build.py,run.py,README.md}` | auto-merged | checked: each file's diff from `cec88385` is exactly this branch's own diff from `7f50ee6a` (sorted +/- lines equal) |

Checks: `git diff --cached --name-only origin/dev-soft-core` was exactly this branch's 16 files; for every one of them the delta survived unchanged. No design decision was needed.

## 2. The three base reds at the composed head (item 2)

| Gate | Command | Head | rc | Receipt |
|---|---|---|---:|---|
| idiom ratchet | `python3 -B scripts/check_cpp_idiom.py` | `d3202fa2` | 0 | `receipts/early/cpp_idiom.log` ("multi-declarator declaration: 0 <= 0") |
| hooks self-test | `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test` | `d3202fa2` | 0 | `receipts/early/hooks_selftest.log` ("28 of 28 checks pass; 96 of 96 mutants caught") |
| firmware boundary | `rtl-fast.yml` job `firmware-boundary`, every step (`run_wf.py`; step 9 `ctrl_boundary`) | `d3202fa2` | 0 (steps 1, 3, 9) | `receipts/early/wf-d3202fa2/` ("ctrl_boundary: PASS", 0 findings) |

The three were red at round 1's base `7f50ee6a` and are green on the composed tree: #810's later commits fixed them, and none needed a change here. The final pass re-runs all three at `3bebf03a` (lane part a; docs-gates-0 gate_38; the firmware-boundary job).

**A fourth red, the composition's own, found by the pre-pass at `d395f682` and fixed:** `scripts/check_py_idiom.py` failed "long module 11 > ratchet 10": `tb/verilator/ctrl_service_budget/build.py` is exactly 1,000 lines at `cec88385` (the limit, `LONG_MODULE_LINES = 1000`), and this branch's change made it 1,001 (at round 1's base it fitted). `3bebf03a` rewraps the arms' comment above `VARIANTS` (five lines to four, the same words, the generated C unchanged), so the file is 1,000 lines and the gate passes (`receipts/prepass-d395f682/`). The pre-pass was stopped at that point; every other step it had finished was rc 0 (`wf-steps-rc.txt`: 63 steps, among them the firmware boundary and the AECP campaign; the lane's plat_ledger, fixtures, the boots, hooks, coverage and behave).

## 3. Re-run at the composed head (item 3)

All at the final head `3bebf03a` (a composed head; its firmware is `d3202fa2`'s byte for byte, below), in the clean-clone pass (section 5):

| Item | Command | Result | Receipt |
|---|---|---|---|
| firmware self-test | `test_ctrl_firmware.py --require-rv32 --self-test` in its four hosted shards (firmware-unit, control, aecp, srp jobs) | PASS in each | `receipts/gates/wf/rtl-fast__firmware-*__ci_step_9*`, `__firmware-unit__ci_step_10.log` |
| coverage | `fw_coverage.py --check` (firmware-unit step 12; lane part a) | PASS, 39 files; `aecp_face.c` 179/179 lines, 160/160 branches | `receipts/gates/lane/fw_coverage_check.log` |
| AECP campaign | firmware-aecp-mutants step 9 | 236 of 236 `[ok]`, none other; the nine author plants each `[ok]` by its named test (`face-as-path-*`) | `receipts/gates/wf/rtl-fast__firmware-aecp-mutants__ci_step_9.log` |
| control campaign (the platform's plants) | firmware-control-mutants step 9 | "mutants: 699 of 699 caught"; `[ok] mutant plat-as-path-unavailable (platboot1, platboot2)`, first: "B11 GET_AS_PATH answers SUCCESS on AVB interface 0" | `receipts/gates/wf/rtl-fast__firmware-control-mutants__ci_step_9.log` |
| SRP campaign | firmware-srp-mutants step 9 | 340 `[ok]`, none other; PASS | `receipts/gates/large/wf-large-files.txt` (log 210,111 B, sha256 there), excerpt in `gates/wf/` |
| S2's harness, both points | `hs2.sh`: a fresh build of arm A, `answering-ports` and `answering-every-port` at 1x1 and 8x8 on a clean clone at `3bebf03a`, sampled groups (A `aecp,aecp-fanout,acmp-cmd`; B `aecp`; N `notice-burst-0`), and the same at `cec88385` | 0 refusals, 0 budget misses, 0 share misses, 0 notice misses at every build at both heads; each ELF at `3bebf03a` identical to `d3202fa2`'s | `receipts/harness/final-3bebf03a/` (`images.txt`, `compare-*.md`, `summary-*`), `harness/early-d3202fa2/` |
| harness self-test | `run.py --self-test` (lane part a) | "self-test: 0 failures"; the log equals round 30's but for path truncation | `receipts/gates/large/lane-large-files.txt` (659,539 B, sha256 there), excerpt in `gates/lane/` |
| builder | `test_builder.py --require-rv32` (lane part b) | "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 11's calibration tree, as before), rc 0 | `receipts/gates/lane/test_builder.log` |
| docs gates | docs.yml's docs-gates-0/1/2, docs-check, docs-check-no-git, wire-accountability; `docs_check.py` | every step rc 0; "docs_check: 0 finding(s)" | `receipts/gates/wf/docs__*`, `gates/lane/docs_check.log` |
| bdd-conformance | rtl-fast.yml `bdd-conformance`; lane `cd tests && behave` | rc 0; 508 scenarios, 2,330 steps passed, 0 failed | `gates/wf/rtl-fast__bdd-conformance__*`, `gates/lane/behave.log.excerpt.txt` |
| split boot to ready | `ctrl_split_boot/run.py` at 1x1/1if, 8x8/1if (`--shape endstation_ax7101_8x8`), 8x8/2if (`--interfaces 2`); `--native-controls`; `--self-test` | ready at 26.354, 66.001 and 68.389 ms against 20,000 ms, 0 findings each; 6 of 6 native controls, 3 of 3 plants | `gates/lane/boot_*.log` |
| ROM ledger | `plat_ledger.py --self-test`; `fixtures2.sh` | `plat_ledger: PASS`, 7 of 7 controls; the same figures as at `d3202fa2` (section 4) | `gates/lane/plat_ledger.log`, `fixtures.log` |


## 4. Acceptance (item 4)

**Load** (`load_grade.py --check`, the stated tables): 1x1/1if 0.501 at the pin and 0.499 with tsn-c-stack#32, ceiling 0.70, at `cec88385`, `d3202fa2` and `3bebf03a` alike: delta 0.000 (the logs identical but their head line). `flip_grade.py --check` exits 1 at both, output identical (no merge gate).

**ROM ledger** (`plat_ledger.py --self-test` for the platform, `fixtures2.sh` on its runtime and flash maps for the fixture, each on a clean clone; base `cec88385`, head `d3202fa2`, and the final pass at `3bebf03a` repeats every figure exactly (`receipts/gates/lane/plat_ledger.log`, `fixtures.log`); `receipts/rom/`):

| Image, point | Base rom B | Head rom B | Delta | sram | RAMB36 base -> head | Cap | Verdict |
|---|---:|---:|---:|---|---|---:|---|
| fixture 1x1/1if | 108,600 | 108,920 | +320 | 45,920, unchanged | 38.5 -> 38.5 | 56 | holds |
| fixture 1x1/2if | 110,304 | 110,624 | +320 | 57,312, unchanged | 41.0 -> 41.5 | 56 | holds |
| fixture 8x8/1if | 122,136 | 122,464 | +328 | 87,008, unchanged | 51.5 -> 51.5 | 56 | holds |
| fixture 8x8/2if | 123,808 | 124,136 | +328 | 113,168, unchanged | 58.5 -> 58.5 | 58.5 | holds, 792 B before 124,928 |
| platform 1x1/1if | 113,672 | 113,984 | +312 | 46,880, unchanged | 39.5 -> 39.5 | 56 | holds |
| platform 1x1/2if | 115,400 | 115,712 | +312 | 58,336, unchanged | 43.0 -> 43.0 | 56 | holds |
| platform 8x8/1if | 127,256 | 127,568 | +312 | 87,984, unchanged | 53.0 -> 53.0 | 56 | holds |
| platform 8x8/2if | 128,960 | 129,272 | +312 | 114,160, unchanged | 59.5 -> 60.0 | 60.5 | holds: its entry's 60.0, `plat_ledger: PASS` |
| harness arm A 8x8/2if | 123,808 | 124,136 | +328 | 113,168 | 58.5 -> 58.5 | 58.5 | holds, 792 B under |
| harness `answering-ports` 8x8/2if | 123,976 | 124,320 | +344 | 113,168 | 58.5 -> 58.5 | 58.5 | holds, 608 B under |
| harness `answering-every-port` 8x8/2if | 124,116 | 124,452 | +336 | 113,232 | 58.5 -> 58.5 | 58.5 | holds, 476 B under |
| harness arm A 1x1/1if | 108,600 | 108,920 | +320 | 45,920 | 38.5 | 56 | holds |
| harness `answering-ports` 1x1/1if | 108,760 | 109,104 | +344 | 45,920 | 38.5 | 56 | holds |
| harness `answering-every-port` 1x1/1if | 108,908 | 109,244 | +336 | 45,920 | 38.5 | 56 | holds |

No point is over its cap, so no figure goes to the #901 note and no STOP.

## 5. Clean-clone pass (item 5)

Once, on the final head `3bebf03a`, every unit on its own fresh clean clone (`run_wf.py`: the steps from the workflows at the head; `verify_wf.py` reads every `run:` step back), the lane gates in three parts (`lane_gates2.sh`), the harness at both points (`hs2.sh`) and the full Verilator sweep as four `native-shards` units (`native-shard-one.py`, the manager's tool's steps for one shard). A pre-pass at `d395f682` was stopped once it found the py idiom red (section 2). Dispatch: `receipts/gates/dispatch.txt`, `receipts/sweep/launch.txt`. No CPU range was free for most of the pass (one other lane held 11 of the 12), so most units, and sweep shards 0, 1 and 3, ran on the session pool, the dispatcher's fallback. Shard 2 ran on a booked range.

| Gate | Command | Result | Receipt |
|---|---|---|---|
| every workflow step | `verify_wf.py 3bebf03a ... rtl-fast.yml docs.yml elaborate.yml rtl.yml` (yosys-shards 0-3) | **139 steps ran, 226 not run with a reason, 0 bad**; all 28 job clones clean after their steps | `receipts/gates/verify-table.md`, `gates/wf/` |
| full Verilator sweep | `scripts/run_all_suites.sh <logs> --wait --shard k/4`, k = 0..3 | 65 suites: 62 PASS, **0 failed**, 3 killed by the wall clock under the pool's contention (milan_dp at 4,800 s, milan_dp_render and mmcm_servo at 1,800 s; "result UNKNOWN, not a failure"), each re-run alone (below) and PASS; the shards print 2,712,939 checks, 0 in-suite failures. **All 65 suites pass, 0 failed** | `receipts/sweep/shard-*/summary.log`, `complete.json`, `suite-logs-sha256.txt` |
| mmcm_servo re-run | `rerun_suite.sh`: its make under the sweep's 1,800 s clock, alone on a booked range, then `suite_tally.py --verdict` | make rc 0, verdict rc 0, 17.5 min: 320 checks, 0 in-suite failures | `receipts/sweep/rerun/` |
| milan_dp re-run | the same, 4,800 s. The first try, on 88-95 in shard 2's clone, shared its range with another lane's unit started in the two seconds between this lane's units, so it was stopped at half the suite (`rerun/milan_dp.head`). The second ran in a fresh clean clone on the session pool (13 of 32 CPUs busy at launch) | make rc 0, verdict rc 0, 46 min: 13,878 checks, 0 in-suite failures | `receipts/sweep/rerun-dp2/` |
| milan_dp_render re-run | the same, 1,800 s, on the session pool (6 of 32 CPUs busy at launch, no booked range free for 10 minutes), in shard 0's clone (not built there) | make rc 0, verdict rc 0, 21 min: 347 checks, 0 in-suite failures | `receipts/sweep/rerun-render/` |
| lane part a | `diff --check cec88385`, py idiom, cpp idiom, baremetal, docs_check, ctrl_hot self-test/check, harness self-test, load self-test/check, flip self-test, hooks and target self-tests, gen_mailbox check/self-test, lint_rtl, soc_options, ctrl_memory, fw_coverage, behave, twin | every one rc 0; the three flip checks exit 1 as at `cec88385` (identical output, no merge gate) | `receipts/gates/lane/` |
| lane part b | `test_builder.py --require-rv32` | rc 0, "ALL GATES PASS EXCEPT 2 NOT RUN" | `gates/lane/test_builder.log` |
| lane part c | `plat_ledger.py --self-test`, `fixtures2.sh`, the split boot at 1x1/1if, 8x8/1if, 8x8/2if, `--native-controls`, `--self-test`, `test_ctrl_nvm.py --require-rv32 --self-test` | every one rc 0 (section 3); nvm "526 tests, all 144 planted defects reddened" | `gates/lane/` |
| harness, both points | `hs2.sh` x6 at `3bebf03a` (section 3) | rc 0 each | `receipts/harness/final-3bebf03a/` |

The sweep's shard-3 clone has two tracked `TEST_RESULTS.md` files rewritten by a suite. The same two are rewritten in #810 round 30's and another lane's shard-3 clones, so it is not this branch (`receipts/sweep/clones-after.txt`). Every other clone was clean after.

## 6. Changes this round (file:line, reason)

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `d3202fa2` | the two conflicts above | both sides kept | item 1 |
| `d395f682` | `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 | round 1's GET_AS_PATH paragraph (round 29's figures) out of round 29's block; a new paragraph and table after round 30's block: both images at the four points at this head, with the change against `cec88385`; two plans move by half a tile (fixture 1x1/2if 41.5, platform 8x8/2if 60.0, its entry fully used) | the figures at the composed head |
| `d395f682` | `docs/design/SPLIT_CONTROL_MEMORY.md` section 5, the harness arm's table | round 30's row (124,116 B, 812 under) and this head's (124,452 B, 476 under) replace round 1's row (123,756 B) | the same |
| `d395f682` | `docs/design/SPLIT_CONTROL_MEMORY.md` section 6 | the platform's override plans 60.0, half a tile more refused | the same |
| `d395f682` | `sw/firmware/ctrl/plat/README.md:113`, `:139`; `tb/verilator/ctrl_split_boot/README.md:112` | 59.5 -> 60.0 RAMB36 at 8x8/2if | the same |
| `3bebf03a` | `tb/verilator/ctrl_service_budget/build.py:124-127` | the arms' comment rewrapped, five lines to four (120 columns), the same words | the py idiom ratchet's long-module rule at the composed head (above) |

## 7. New checks (planted mutant, failing words)

None this round: no behaviour changed. Round 1's ten plants are re-run by the campaigns (section 3).

## 8. Notes for the next session

- Scratch (`/data-2/milan/tmp/897-a776`, 14 GB at the end; the milan_dp re-run clone, round 2's temp directory and round 1's pass logs removed): `r2/` holds round 2's clones (`cl-base`, `cl-head`, `cl-final-3bebf03a`, `sweep-src-3bebf03a`, `rerun-dp-clone`), harness builds (`r2/builds/`: `b*` base, plain the merge head, `f*` final), the pass's logs (`r2/gates-out/`), the sweep (`r2/sweep-3bebf03a/`). The scripts are in `scripts/r2/`. The shard clones are `$LANES/897-a776-r2-shard{0..3}`. No unit of this lane is left running.
- The round-1 scratch clones were removed at the start (the round-1 receipts are in the output directory).
- Nothing pushed, no PR opened or edited, no board touched.
