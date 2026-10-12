[A604] REVIEW READY
Commit: `61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3` (branch `727-shard-balance`; round 2 on top of `a57d384d`, new commits only, not pushed)

Changed (round 2, per [A10] Round 2 6126048117):
- `1d5f1c88` **F1** (R626-1 F1 = R627-1-F1). `scripts/suite_shards.py:596-611`: the 116/117-minute arm now keeps the bound each planted `rtl.yml` applied. A new arm requires the bound applied at `rtl.yml`'s 120 and at the planted 116 and 117 to equal `minutes * 36` s, computed without `bound_seconds` or `HEADROOM_PERCENT`. At the head it prints `[ok] ... {116: 4176, 117: 4212, 120: 4320}`.
- `78cee0d6` **S2** (optional). `:585-588` plants `aaf` at 0 s, and `:613-620` plants `total: [6]` in `rtl.yml`; each must be refused. `with_verilator_key` (`:548-557`) replaces `with_verilator_timeout`.
- `61296ea1` **R1** (R626-1-R1 = R627-1-R1). `docs/testing/CI_WORKFLOWS.md:191-196` now reads: "All figures come from one dev run, except `maap`, which keeps #696's figure from its pull-request run until a dev run measures that change."
- **R627-1-R2** is applied in the PR body text: "Overheads assume warm Verilator and Yosys caches; worker 1's overhead includes the tsn-gen build." The evidence is `rtl.yml:278-292`, which builds tsn-gen with no cache step.
- `rtl.yml` is byte-identical (item 4), and the `:136-137` comment goes to #495. No table, balance or selection changed. The five `--shard I/5 --list` outputs are byte-identical to round 1's, and the predictions are unchanged at 4204/4205/4203/4205/2877 s against 4320 s.

Validation (head `61296ea1`, all rc 0, CPython 3.12.3 and 3.14.7):
- `python3 scripts/suite_shards.py --selftest`: `selftest: PASS`, 11 `[ok]` planted-defect lines (round 1 had 8), 0 ESCAPED/FAIL.
- R626-1's `mutate.py` (sha256 `571bd0aa...fcfc031`, equal to its manifest) ran unmodified, 29 cases, 0 DRIFT:

| Case | at `a57d384d` | at `61296ea1` |
|---|---|---|
| `headroom-75-percent` | rc 0 | rc 1, new 36 s arm ESCAPED (applied 5400 s at 120 min), only failure |
| `headroom-100-percent` | rc 0 | rc 1, new 36 s arm ESCAPED (7200 s), only failure |
| `bound-formula-div10` | rc 0 | rc 1, new 36 s arm ESCAPED (43200 s), only failure |
| `table-zero-duration-allowed` | rc 0 | rc 1, zero-duration arm ESCAPED, only failure |
| `worker-count-mirrored-5` | rc 0 | rc 1, six-worker arm ESCAPED, only failure |
| `tree-head` | rc 0, PASS | rc 0, PASS |

  The other 23 cases give the same rc as at `a57d384d`. `timeout-mirrored-120` now fails the new arm as well as the 116-minute arm.
- The round-1 harness `mutants_727.py` (19 cases) behaves as in round 1, except that `m_timeout_mirrored` now fails 3 arms.
- `ci_events.py --check` and `--selftest`, `test_suite_cancellation.py`, `check_py_idiom.py`, `measure_naming.py --check`, `measure_fail_fast.py --check`, `check_hygiene.py --check`, `check_todo_ownership.py`, `measure_test_evidence.py --check`, `suite_tally.py --selftest`, `check_baremetal_only.py --check` and `check_archive.py` all exit 0.
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base c6bd08c6` (0 findings over 33 added lines) and `--selftest`, and `check_doc_paths.py` all exit 0.
- `scripts/run_all_suites.sh --shard I/5 --list` for I = 0..4 lists 15, 16, 14, 16 and 1 suites. Their union equals the 62-suite `--list`, with no suite twice. 4/5 is `milan_dp` alone, `tsn_fuzz` is in 1/5 and `chmap_capture` in 3/5. `git diff --check c6bd08c6 HEAD` and `git diff --check` exit 0.

Acceptance criteria:
- 1, 2 and 4: met as in round 1. Case 3's 60% half now has its own control.
- 3: pending. The PR run 38258772791 (`a57d384d`, same split) still had all five Verilator jobs in progress at 2026-10-12T14:22Z. The exact-head measurement comes from `61296ea1`'s run after the push. The command that reads it is in the PR body and the handoff, section 6.

Open risks/questions:
- R626-1's `nondeterministic-tie` mutant (equal durations broken by `hash(suite)`) exits 0 at both heads. The in-process determinism arm uses one hash seed, while the hosted workers each run their own process.
  - The head's tie-break is lexical, and its lists are identical under `PYTHONHASHSEED` 0, 1, 2 and 12345.
  - Neither review raised this, and round 2's scope is frozen, so it is not fixed here. It is published for a decision.
- R626-1-S1 (the renamed-copy skip) is not in the round-2 assignment and is unchanged.
- Not run, as in round 1: the Verilator suites, the serial sweep, `syn/yosys/run.sh` and the `act` replica, because there is no new pushed head.
