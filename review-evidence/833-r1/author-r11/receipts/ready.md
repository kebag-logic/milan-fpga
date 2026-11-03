[A726k] REVIEW READY
Commit: 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea (branch `833-owned-process`, two commits on round 10's `fce77f0e`; not pushed by this lane)

Changed:
1. **R763-10-F1, pinned (`7b3b7e6f`).**
   - Two listings in `owner_stated_seconds`: "a stubborn parent beside a stopped shell" and "a stubborn parent under a stopped shell". They have R763-10-F1's stated events: `SIGTERM` to parent and child at 0; `SIGKILL` to the child at 2 and to the parent at 4; at 14 `SIGKILL` to the shell, parent and child; then the verdict. The guide lists them.
   - `first-census-parent-unspared-beside-shell` joins `MUTANTS`, with R763-10's edit byte for byte. It is red on `owner_stated_seconds` with "a stubborn parent beside a stopped shell's ...", on those two listings alone of 48, and on the whole test. It is named in row 3.
   - The listings come after every other listing. Placed beside "a stubborn parent", they would fail first for `resume-with-one-live` and `parent-under-unresumed-shell-unspared`, which would then print the new words instead of their own.
   - Room under the 1000-line ratchet: both modules were full (999 and 996 lines).
     - The stubborn parent's stated events get a name, `stubborn`, with the identical literal, and the new listings reuse it.
     - "a stopped shell" and "a live new descendant beside a stopped shell" are re-laid with no code change.
     - An AST check against `fce77f0e`: with the new loop removed and the name inlined, the module is identical. No `MUTANTS` entry changed value or order. Both modules are now 1000 lines.
2. **The exact RESIDUE wording (`5843d1af`).**
   - R764-10-R1's text.
   - R763-10-R1's text in the guide and in `kept`'s docstring. R764-10-R2 gives a different exact text for the same two lines, so it is taken through R763-10-R1. Its docstring text needs a third line, and the module has none left.
   - R764-10-S1 is not taken, at the author's judgement. Neither the assert nor the split fits on the existing line under the limit, and every growing listing's words start with "a ".
   - R764-6-S1 is retained, not taken, as before.

`scripts/owned_process.py` is unchanged, and no probe showed it wrong.

Validation, at the head, one log and rc each, SIGHUP at its default:
- Every `run:` step of docs.yml: verifier rc 0. 64 steps rc 0, 31 not run with round 1's reasons, 0 bad. Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`.
- `python3 scripts/test_suite_cancellation.py`: rc 0, `suite cancellation: PASS`.
- `--mutants`: rc 0, `owned-process mutants: PASS (150 mutants, 147 with a control that must fail)`.
- `--matrix`: 4 parts, 1694 runs, each part PASS.
- `make -C tb/verilator/gptp_shadow lifecycle`: rc 0.
- `cd tests && behave`: rc 0, 2330 steps passed.
- `git diff --check 1f29f189 HEAD`: silent.

Both reviewers' round 10 probes, unchanged, at the head:
- `natural10.py`: the new mutant is killed; `none` is green everywhere.
- R763-10's sweep: 4224 mutants, 2716 equivalent, 1110 killed, 398 survivors. Every survivor also survived in R763-10's own run, and the classifier finds the same 82 classes and the same 12 out-of-domain ones.
- R764-10's cell sweep and `whole_rerun.py`: the same 25 as at round 10 (24 survive, 1 red on `owner_shell_window`). `--author` maps all 150 entries.
- Per-listing map, cell probe (65 of 65), table, byte and module-move checks: as published.
- `owner_report` stress: 0 red of 3000 under each reviewer's driver.

No new survivor, and none inside a stated domain.

Cost: about 2 ms more in-process for `owner_stated_seconds` (median 52 to 54 ms). The whole test averages 60.6 s at round 10 and 60.7 s here.

Acceptance criteria: round 11 ruling item 1 met (pinned, not narrowed); item 2 met as above.
Open risks/questions: none. The PR body's round 11 section is ready for the manager to publish.
