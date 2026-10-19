[R650] POSITIVE - exact head acfef36b39283c3102ba5f6948fe1f8c8c494853

# R650-4 internal independent review: FPGA-gPTP PR #83 (issue #82), round 4

- Repository: Mister-M-alt/FPGA-gPTP, PR #83. Exact head `acfef36b39283c3102ba5f6948fe1f8c8c494853`, tree `e2e1cb62ba1a232761aa80c74a2230e7c9ac078f`. The PR's head SHA matches.
- Delta reviewed: two commits on `334e9fe6`:
  - `dea718c`: `tb/verilator/engine/sim_main.cpp` and `tb/verilator/engine/mutants.py`.
  - `acfef36`: `docs/INTEGRATION.md`, one line.
- Source base for the whole PR: `b9ade3a63d1b2292d75eb9b1809647e6439542a0`. Parent dev used for the consumer gates: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`.
- Assignment: PR comment 6255991019 (round 4). Review start: 6256804837. Author REVIEW READY: issue #82 comment 6256511083.
- Evidence: kebag-logic/milan-fpga `911a38b5f6f9e93d883f7d833643d7dddc41587e`, `review-evidence/gptp82-r1/author-r4`.
- Code the delta does not touch keeps its round-3 verdicts (R650-3 and R651-3 were both POSITIVE at `334e9fe6`). The delta changes nothing those verdicts depend on: no RTL, microcode, generator, Makefile, port or image changed.

## Verdict summary

Every round-4 item holds at this head. No MINOR, MAJOR or BLOCKER is open.

1. **The ratchets are back within the parent's budgets, and no ratchet was raised.** I ran the parent's own `check_py_idiom.scan` and `check_cpp_idiom.scan`/`long_functions` (parent `e9cbb676`) on both changed files at both revisions:

   | file | 334e9fe6 | acfef36b |
   |---|---|---|
   | `mutants.py` | long function 1 (`main`, 104 lines at :549); undocumented public function 1 (`failing`, :624) | none |
   | `sim_main.cpp` | long function 1 (`run_suite`, 102 lines at :244) | none |

   - These are exactly the three over-budget counts the manager's run reported (C++ long function 1 > 0; Python long function 10 > 9, undocumented 1 > 0).
   - The delta touches no other counted file, so the tree totals now equal the budgets: C++ long function 0 ≤ 0; Python long function 9 ≤ 9, undocumented public function 0 ≤ 0.
   - Budgets live in the parent (`scripts/*_idiom.budget`). The author's parent snapshot `dd2e1fd9` changes only the gitlink (`pin-commit.diff`, 1 file), so no budget moved.
   - `mutants.py` is 680 lines, under `LONG_MODULE_LINES` (1000).
2. **No behaviour change.** I reran the evidence myself, with the pinned Verilator 5.050 (identity checked):
   - **Engine suite** (`make run`, all four images) at `334e9fe6` and at this head, from clean archives: both rc 0, 1,642 / 1,642 / 1,642 / 46 checks passing. After removing paths, timing and make banners, the two logs are identical (empty diff).
   - **Mutation arm** at this head, in the published 18-way shard layout: every shard rc 0. All 18 of my shard logs are byte-identical (cmp rc 0) to the author's `334e9fe6` logs and to the author's head logs. That is 58 of 58 caught (58 distinct names), 71 named failure lines, and 18 clean controls.
   - **C++ split, static check.** I parsed both revisions' phase lists (`phase_lists.py`):
     - The old self-publication branch minus its tally and return equals `run_the_self_publication_phases` (8 statements).
     - The old fall-through list minus its tally and return equals `run_every_phase` (83 statements).
     - Neither new body has a return, break or goto, so the single tally and return in `run_suite` (`sim_main.cpp:244-251`) is reached on both paths, as before.
   - **Python split, stubbed equivalence probe** (`verdict_equiv.py`, reviewer-owned and independent of the author's meta-run). It drives both revisions' own `main()` over 20 stubbed controls, once with a passing and once with a failing positive control. The controls are:
     - pattern counts of 0 and 2, a refused image, and a failed build;
     - a generator mutant, to confirm it reuses the clean executable and never calls build;
     - a survivor, a masked exit 0, an abort, a signal and a skip;
     - an unnamed catch;
     - slew named / only in the fourth pass / unrelated;
     - #82 all named / one missing / only in the fourth pass;
     - a fourth-pass-prefixed name present / only in the shipping pass;
     - an uncaught #82 control.

     Stdout, return code and the stub call sequence are identical. The probe prints EQUIVALENT.
   - The author's own controls verify as published: `split-swap` rc 2 (54 fourth-pass failures), `split-drop` rc 0 with the check count falling to 1,629, and `meta-branches` base = head for both halves.
3. **R650-3-R1 is applied exactly.** `docs/INTEGRATION.md:480` reads "Flags carry gmPresent alone, or nothing with priority1 255." This is the exact text I asked for in round 3. `make docs contract` passes at this head in a clean archive (rc 0: diagrams, docs and self-test, source evidence 20 exact plus its 7-arm self-test, PHC contract).
4. **The full parent consumer list passes on a committed local parent snapshot.** `consumer_check.py` matches each of the 11 commands in the manager's template (`pgates/manager-334e9fe6/parent-consumer.json`, base `e9cbb676`) to exactly one author result, with the same argument tail, at parent `dd2e1fd9` with gptp-processor `acfef36b`:
   - All 11 exit 0, and each has its log. This includes `check_cpp_idiom.py` and `check_py_idiom.py`, which were rc 1 in the manager's `334e9fe6` run.
   - The idiom logs read "long function: 0 <= 0" (C++) and "long function: 9 <= 9 … undocumented public function: 0 <= 0" (Python).
   - The builder suite (`test_builder.py`) reports "ALL GATES PASS EXCEPT 1 NOT RUN". The arm not run is gate 11 (calibration report, needs a board build tree). The manager's `334e9fe6` run has the identical line and the same gate-arm set.
   - `gptp_shadow`: 309/309, mutant lifecycle PASS, controls 9, failures 0.
5. **The author-r4 receipts verify.**
   - All 498 `author-r4/` entries in the evidence `MANIFEST.json` match their published sha256. No file is unlisted or missing, and no host paths remain.
   - The author's `verify_receipts.py` (run from a copy outside the data directory) reports 497 files, 497 index rows, 0 mismatches, rc 0.

Open items: two RESIDUE (wording only, in docstrings and comments of the reviewed delta) and one new SUGGESTION. The round-3 suggestions are retained unchanged.

## Reconstruction and authorities

- The repository has no AGENTS.md or CONTRIBUTING.md. The applicable sources are `docs/README.md` (truth order: RTL and µcode, then tests, then guides, then history), `docs/INTEGRATION.md` and `docs/TEST_DEVELOPER.md`.
- Frozen acceptance:
  - Issue #82 (802.1AS-2020 10.3.13.2.4 b), g), i); thisClock and {thisClock} from reset; parent consumer gates).
  - The prior scope decisions, as summarised in the round-3 reviews.
  - The round-4 assignment: split and document under the parent's CODE_QUALITY Rules 11 and 12 without raising a ratchet; no behaviour change; run the full parent consumer list including both idiom gates; apply R650-3-R1.
- Interface authority:
  - Parent `scripts/check_cpp_idiom.py` and `scripts/check_py_idiom.py` at `e9cbb676`: `LONG_FUNCTION_LINES = 100` in both, `LONG_MODULE_LINES = 1000`, public means no leading underscore.
  - The scanners count every tracked first-party file across both project submodules (`code_quality_scope.tracked`, `git ls-files --recurse-submodules`).
- Order kept:
  1. Independent pass over `git diff 334e9fe6..acfef36b` and the two commits.
  2. My own probes.
  3. Only then the prior public findings (R650-3 6255749431, R651-3 6255692428), to resolve them.

## Lens findings on the delta

- **Conformance.** No conformance-bearing source changed. The one documentation change makes the reset-state sentence agree with the graded priority1-255 behaviour (flags 0x0, `p1 255 #82 cold release: that commit's flags are gmPresent alone`, expected 0) and with `INTEGRATION.md:508`.
- **RTL.** The delta has no HDL, generator or image change (`git show --stat`). The round-3 RTL verdict stands.
- **Robustness.**
  - The C++ split keeps one tally line and one exit-status path.
  - The new members are private, after the existing `private:` (`sim_main.cpp:253`). Previously `private:` came after `run_suite` with the same blank-line style.
  - The Python split keeps the same verdict precedence (slew narrowing, then #82/fourth-pass narrowing, on the same `answer`).
  - `fails` and `passes` are incremented exactly once per mutant, as before (each early `continue` became `return False`).
  - The engine build at head emits no compiler warnings under `-Wall -Wextra` (0 "warning" lines in my log).
- **Tests.** Identical checks and identical mutant verdicts, proven by execution and statically (above). The split is not itself guarded by a planted mutant, and the author states it plainly: dropping a call is visible only as a lower check count. See S1.
- **Docs.** R650-3-R1 is exact. The new comments and docstrings state behaviour and reason and cite only issue numbers. They contain no lane label, lane name, review round, reviewer ID or comment ID. Two wording inaccuracies are recorded as RESIDUE below.
- **PR body (Round 4 section).** I checked it against the receipts. These are all accurate:
  - "102 lines" and "104 lines".
  - "long function 0 of 0 … 9 of 9 … 0 of 0".
  - 1,642 checks ×3 and 46.
  - 18 shard logs byte-identical, 58 of 58 caught, 71 named lines.
  - 54 checks for the inverted dispatch, 1,642 → 1,629 for a dropped call.
  - 11 commands, one builder arm not run.

## Findings

### R650-4-R1 - RESIDUE - Docs - `run_suite`'s comment says it runs every phase

- **Where:** `tb/verilator/engine/sim_main.cpp:242-243`: "Runs every phase in file order and prints the one tally line the sweep parses."
- **Evidence:** `run_suite` now only dispatches. Every phase runs in `run_every_phase`; the priority1-255 image runs `run_the_self_publication_phases`, which is a subset. The sentence was already loose at `334e9fe6`, but this delta made `run_suite` a dispatcher and gave "every phase" to the other function, so the mismatch is now visible.
- **Impact:** wording only. It changes no check, code or verdict.
- **Exact fix:** "Runs this image's pass (every phase, or only the self-publication phases for a priority1-255 image) and prints the one tally line the sweep parses. Returns the process exit status: 0 pass, 1 fail."

### R650-4-R2 - RESIDUE - Docs - `run_mutant`'s docstring lists only some of the False outcomes

- **Where:** `tb/verilator/engine/mutants.py:597-599`: "False, with the reason printed, when it survived, did not build, its image was refused, or its pattern no longer appears exactly once."
- **Evidence:** `run_mutant` also returns False when a caught control misses a named check (`named_verdict`), and when the harness gives no usable verdict: a masked exit 0, an abort, a signal or a skip (`verdict`). My stubbed probe shows each of these.
- **Impact:** wording only.
- **Exact fix:** "False, with the reason printed, when it survived, missed a check it names, gave no harness verdict, did not build, its image was refused, or its pattern no longer appears exactly once."

### R650-4-S1 - SUGGESTION - Tests - the phase dispatch has no guard of its own

- **Where:** `tb/verilator/engine/sim_main.cpp:244-353`. Evidence: the author's published `split-drop` control (rc 0, 1,629 checks).
- **Evidence:** removing a phase call from `run_every_phase` leaves the suite green. Only the tally count shows it. This was equally true of the inline list at `334e9fe6`, so it is not a regression.
- **Suggestion:** have the suite fail on a check count below a recorded floor for each pass, or have the sweep pin the count. A dropped or misdispatched phase would then fail by name.
- **Verification:** the clean run passes; the `split-drop` plant fails.

### Prior public findings, resolved at this head

| Prior ID | Severity, lenses | Disposition at this head |
|---|---|---|
| R650-3-R1 | RESIDUE, Docs | CLOSED: exact text at `docs/INTEGRATION.md:480`. |
| R650-3-S1 (immediate mastership on capability return) | SUGGESTION, Conformance and Tests | RETAINED. The delta does not touch it, and the author declined it as out of scope. |
| R650-3-S2 / R651-3-S1 (assert the phase-36 preconditions) | SUGGESTION, Tests and Robustness | RETAINED. The phase-36 body is unchanged by the delta. |
| R650-3-S3 (state the priority1-255 phase coverage in the PR text) | SUGGESTION, Tests and Docs | RETAINED. The new `run_the_self_publication_phases` comment and the header (`sim_main.cpp:161-165`) are exact; the PR text is unchanged. |
| R650-3-S4 (bench presence LED) | SUGGESTION, RTL | RETAINED. Unchanged. |
| R650-3-S5 (manifest pre-redaction digests) | SUGGESTION, evidence provenance (manager) | RETAINED. All 498 author-r4 entries again record `path_redacted: false` with original = published, while RECEIPTS.md says the manager redacted the files. Verification of the published copy is unaffected. |
| R650-2-S1, R650-2-S2, R651-2-S2 | SUGGESTION | RETAINED. Unchanged code. |
| All round-1 and round-2 MAJOR/MINOR/RESIDUE items | as recorded | CLOSED at round 3. The delta changes nothing they depend on. |

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `docs/INTEGRATION.md:480` against the graded priority1-255 reset flags and `:508`; the delta has no conformance-bearing source change; round-3 conformance verdict carried | R650-4 (delta) + R650-3 | acfef36b39283c3102ba5f6948fe1f8c8c494853 |
| RTL | CLEAN | `git show --stat dea718c acfef36` (no HDL, generator or image change); engine build warning-free; round-3 RTL verdict carried | R650-4 (delta) + R650-3 | acfef36b39283c3102ba5f6948fe1f8c8c494853 |
| Robustness | CLEAN | `sim_main.cpp:244-353` (one tally and exit path, private members); `mutants.py:549-677` (verdict precedence, one tally increment per mutant); stubbed 20-row probe over both control outcomes | R650-4 | acfef36b39283c3102ba5f6948fe1f8c8c494853 |
| Tests | CLEAN | own engine runs at base and head (identical); own 18-shard mutation arm at head (byte-identical to the author's base and head logs, 58/58); `phase_lists.py`; `verdict_equiv.py`; the author's split and meta controls; parent idiom scanners on both files at both revisions; 11/11 consumer results against the template | R650-4 | acfef36b39283c3102ba5f6948fe1f8c8c494853 |
| Docs | CLEAN (2 RESIDUE carried) | `docs/INTEGRATION.md`; new comments and docstrings checked against the comment rule; `make docs contract` rc 0; PR body Round 4 section against the receipts; author-r4 manifest and index | R650-4 | acfef36b39283c3102ba5f6948fe1f8c8c494853 |

## Real limits

- Source-head execution evidence is the author's published gate receipts plus my focused reruns: engine suite, engine mutation arm, docs and contract, and the parent idiom scanners on the changed files.
- I did not run any full parent, protocol-processor, gPTP, Yosys or builder bank. That includes the 11 parent consumer commands, which I verified from the author's receipts against the manager's template. No manager source bank runs at this exact head, and I neither claim nor infer one.
- The author's consumer snapshot `dd2e1fd9` is dev `e9cbb676` plus only the gitlink. The plane-on `milan_dp` adaptations and docs re-points the PR body describes for round 3 belong to the parent pin bump, not to this snapshot.
- There are no hosted check runs or statuses at this exact head (check-runs total 0, status pending with 0 contexts). Hosted and act acceptance stays with the manager.
- Physical calibration was NOT RUN. The builder suite's gate-11 calibration arm did not run (it needs a board build tree), and a field skip is not hardware proof.
- My clone was restored and verified after the probes, and all probes ran in disposable archives:
  - HEAD and tree are exact.
  - No untracked or ignored files.
  - index = HEAD and worktree = index.
  - The ls-tree and ls-files mode/blob/path digests are equal.
  - The head tree has no gitlinks, so no submodule pins apply in this repository.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `b9ade3a6`, live dev `e9cbb676`) with the builder and native banks at the merge turn, and link those receipts on the PR.
- Carry R650-4-R1, R650-4-R2 and the round-3 R650-3-R1 closure to the residue checklist.
- Hosted/act acceptance at the merge candidate.
- The parent pin bump with its docs, ROM-ledger and `milan_dp` boot-state updates, as the PR body says ("Refs", not "Closes").

## Receipts in this packet

- `scripts/`:
  - `idiom_probe.py`: the parent scanners on the changed files.
  - `phase_lists.py`: the C++ phase-list equivalence.
  - `verdict_equiv.py`: the stubbed Python equivalence.
  - `shard.py` and `launch.sh`: the engine and mutation runs.
  - `consumer_check.py`: the template against the author's results.
- `receipts/`:
  - `idiom-probe.txt`, `phase-lists.txt`, `verdict-equiv.txt`.
  - `mutants-compare.txt`, `consumer-check.txt`.
  - `author-r4-index-verify.txt`, `docs-contract-head.{log,rc}`, `clone-integrity.txt`.
  - `runs/`: the engine logs at base and head, their diff, and the 18 head shard logs with their rc files. Host paths are replaced with placeholders.

R650-4 FINISHED
