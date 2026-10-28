[A685e] REVIEW READY
Commit: `5527a9c66716331fd06285f428ea1a653c526ada` on branch `665-s2c-icache`, not pushed. On [A685d]'s REVIEW READY head `e0bb857a` (PR #796): a merge of `dev-soft-core` `1a635a4c` and two commits. PR base: `dev-soft-core` `1a635a4c`, which now contains S2 (PR #792, merged as `6660a1a0`). The PR's diff against it is this lane's 15 files.

Changed, per the round-3 assignment (issuecomment-6461736980):
1. **Merge.** `10d8df98` merges `origin/dev-soft-core` `1a635a4c` as a merge commit, with no rebase and no conflict. Between S2's final head `f58d049b` and `1a635a4c`, nothing under the harness, `sw/litex` or `sw/builder` changed except the harness README's classification paragraph. S2's rules are therefore unchanged, and no figure of the cache is re-stated.
2. **R713-2-F1 / R714-2-F1.** `5e679594`: `docs/reference/FR_NFR.md:5-8`, the page summary, now reads "The release uses one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it stays cacheless (NFR-SCOUT-01)." That is `:321`'s clause. The paragraph keeps its four lines, so no line citation into the page moves. The PR body's "no open requirement conflict" is now true.
3. **S2's round-6 classification.** This PR adds no harness file. Of the six classified files, it adds to `build.py`, `selftest.py` and `split_soc.py`. Only `build.py` gains a compile: the hybrid-XIP arm's relink through `ctrl_srp_image.link`. That relink compiles the split layout's reset entry from an unchanged copy and edits only the linker script. `5527a9c6` names it in `build.py`'s `OUTSIDE` reason (`sw/firmware/ctrl/test/ctrl_configs.py:181-191`) and in the README's classification paragraph (`:133`).

Validation at `5527a9c6`. Every gate ran one at a time in the foreground, unpiped, with the tree clean after each: **0 of 100 gates nonzero**.
- Harness self-test: rc 0, 93 `PASS`, 70 `MUTANT caught`, `self-test: 0 failures`.
- `python3 sw/builder/test_soc_options.py`: rc 0, 6 killed controls on the split cache, `RESULT: PASS`. `python3 sw/litex/test_ctrl_memory.py`: rc 0, `RESULT: PASS`.
- rtl-fast `firmware-boundary`, run locally (`python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator`): rc 0, `0 finding(s), 112 boundary, 167 pin and 4 figure controls, 0 misbehaved`, `ctrl_boundary: PASS`.
- rtl-fast `publication-census`, run locally (`python3 sw/mailbox/publication_census.py --check --selftest --jobs 4`, Yosys 0.66 at `86f2ddeb`, sv2v 0.0.12): rc 0, `6 shape(s), checks: 234   failures: 0`, `RESULT: PASS`.
- `python3 scripts/check_baremetal_only.py --check`: rc 0, `baremetal-only: OK (0 findings across 1432 tracked first-party file(s))`. `--selftest`: rc 0.
- The docs workflow's 87 check-mode gates: rc 0 each. Among them: `check_em_dash: 0 finding(s) over 380 added line(s) ... [1a635a4c..HEAD]`, `docs_check: 0 finding(s)`, `TOC gate: OK`, `anchor check: 552 ... reproduced`, `doc path gate: OK`. `git diff --check 1a635a4c HEAD`: rc 0.
- `cd tests && behave`: rc 0, 14 features, 406 scenarios, 1977 steps passed.
- `python3 sw/builder/test_builder.py --require-rv32`: rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`. The NOT RUN is the registered calibration report, the same as round 2.

**Real harness build at 1x1 with the cache**, at `5527a9c6`, run to the measurement: `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <outside the checkout> --record-budget-findings`.
- `build.json` records `fetch_l1 split` and geometry 64 x 1. The netlist is round 1's (generator arguments `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`).
- Result: `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`, rc 0. That is the PR's figure.
- `table.md` is byte-identical to the round-2 regrade on S2's final harness: composed maximum at least 966,218 CPU cycles (19.324 ms), a lower bound, as the PR states.
- All 18 per-group grades are byte-identical to that regrade's.

Acceptance criteria: round-3 items 1 to 4 are met, with the evidence above. The PR stays "Relates to #665", because the cache does not close T_svc.

Open risks/questions: none blocking.
- Not run this round, because round 3 changes no RTL, generator option, SoC or export: the four-shard sweep, Yosys and Vivado out-of-context runs, and the all-fabric export digest.
- The reviewers' optional suggestions (R713-2-S1 to S5, R714-2-S1 and S2) are listed in the PR body and not taken.
