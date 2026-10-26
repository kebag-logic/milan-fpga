[R703] POSITIVE - exact head f58d049beb377c3f535628067022d4d5b51e8208

# [R703] R703-5: internal cleared-context review of PR #792 (issue #665, lane S2, round 5)

- Head under review: `f58d049beb377c3f535628067022d4d5b51e8208`, tree `ded3925598e677698c7fa80206994caad148bc21`, base `dev-soft-core` `e76a755a` (ancestor: yes).
- Previously reviewed head: `a66148f6b7e59e3f42c939f464fe76e2b05404d7` (R703-4, NEGATIVE, 2 MINOR).
- Delta reviewed: `a66148f6..f58d049b`, two commits, four files, all under `tb/verilator/ctrl_service_budget/`: `run.py` (+18 -7), `selftest.py` (+68 -18), `selftest_mutants.py` (+33) and `README.md` (+23 -9). See `receipts/delta_stat.txt` and `receipts/delta_a66148f6_f58d049b.diff`.
- Scope authority:
  - the S2 assignment on #665 (issuecomment-6409745905) and owner decisions D3/D4/D5 (issuecomment-6409738976);
  - the round-5 assignment (issuecomment-6426822636), which limits the round to `tb/verilator/ctrl_service_budget/` and the PR body, with no firmware change and no change to any measured cycle count;
  - AGENTS.md sections 6 and 7.

## Verdict

**POSITIVE.** Both R703-4 MINORs are fixed at their cause, and each has a named check and mutants that fail when the rule is removed. The published records and table lines reproduce exactly from round 3's grades using the head's code. No measured figure changed.

Open items, none of which blocks:
- two RESIDUE items (wording only) and one carried RESIDUE item;
- three SUGGESTIONs.

All five lenses are CLEAN at this head.

## What I verified

| Claim | Result | Receipt |
|---|---|---|
| Self-test at head | rc 0: 87 `PASS` lines, 62 of 62 `MUTANT caught`, `self-test: 0 failures` (author: 87 / 62) | `receipts/selftest.log`, `selftest.rc` |
| R703-4's `r703_4_probes.py`, unmodified (sha256 `a5977aa5…`), on a clean clone of the head | P1-P5, P7, P8 and P10 caught. P6 and P9 escape (R703-4's optional S1/S2). D1 gives `not_run: ["backlog-adp-refill"]`, `partial: true` for arm B's three rows, and the one-row line `Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): …`. Clone clean afterwards | `receipts/r703_4_probes/` |
| R703-2's `review_mutants2.py` and R703-3's `review_mutants3.py`, unmodified, in the sandbox layout R703-4 used (`scripts/sandbox_from_R703-4.sh`) | 23 of 25 (N11 and N12 escape) and 18 of 21 (G2, G3 and H3 escape), the same as round 4 and as the author reports | `receipts/review_mutants{2,3}_head.log` |
| Arm records and table lines, recomputed independently | I recomputed `composed_maximum` and the two composed lines of `run.table`, using the head's `run.py`, from round 3's published per-group grades (author-r3 `runs/*`). All nine arms (A1, A8, B1, B8, S1, S8 and the three controls) equal the author's round-5 `composed_maximum_records.json` and `head-regrade/*/table.md` lines. A1 and A8: `at least 1,565,803` / `2,209,308` cycles, lower bound, 4 of 4 rows. B1 and B8: `740,260` / `1,392,016`, `partial`, `backlog-adp-refill` not run | `receipts/recompute_composed.txt`, `scripts/recompute_composed.py` |
| Published author packet (evidence commit `f72b9f55`, `author-r5/`) | 151 manifest entries; every published sha256 matches; nothing unlisted or missing; none redacted. The evidence commit itself carries no signature, so the manifest is the integrity record | `receipts/packet_manifest_verify.txt` |
| Masking by a refusal (the round's "found this round" item) | Under the two re-labelled mutants, `composition_checks` raises a `Refusal` before `checks()` returns, which hides the other groups' results. With each check group run on its own: `worst pass: the run's last pass is dropped` still fails `the pass bound runs from the running pass at the bus ratio` and `the worst pass includes the run's last pass`; `the load is the stimulus's own declaration` still fails `a window short of its defined load is refused although it declares it`. Across all 62 mutants, every one fails at least one named check in isolation. No escape is hidden behind a refusal | `receipts/isolate_masked.txt`, `isolate_all.txt`, `scripts/isolate_groups.py` |
| README mutant table against the self-test output | 61 of 62 rows are prefixes of the printed line. One row paraphrases its refusal (R703-5-R1) | `receipts/table_vs_selftest.txt`, `scripts/table_vs_selftest.py` |
| A backlog group that ran but has no composed window cannot be mislabelled "not run" | `grade.py:761-763` refuses such a group (`the load has no composed window`), and a refusal fails the run | `grade.py:761-763` |
| Write path of `results.json` | `run.py:317` writes `summary(...)`. A planted bypass in `main()` (probe M1) is not caught by the self-test (SUGGESTION S1) | `receipts/probe_M1_main_bypass.log`, `probe_M0_copy_baseline.log`, `scripts/probe_main_bypass.py` |
| Gates I ran at head | `check_baremetal_only.py --check` rc 0 (0 findings across 1431 files); `docs_check` rc 0; `check_doc_style` rc 0; `check_doc_paths` rc 0; `check_py_idiom` rc 0; `git diff --check a66148f6..f58d049b` rc 0. NOT RUN here: `check_em_dash` and `gen_toc --check` (the pinned Markdown renderer is not installed, and shared installs are out of scope; both exited 2 "cannot judge"). For those two I rely on the author's head receipts (`em_dash.log`: 0 findings over 643 added lines; `toc_check.log` and `toc_verify_anchors.log` OK, `HEAD.txt` = `f58d049b`), and my own scan of the delta's added lines finds 0 em dashes | `receipts/gates_summary.txt`, `receipts/gate_*.log`, `receipts/comment_rule_delta.txt` |
| Comment rule (owner 2026-10-15) | None of the delta's 142 added lines names a lane, review round, reviewer or comment ID (source: the raw diff). The new source comments state behaviour only | `receipts/comment_rule_delta.txt` |
| PR body | The live body equals the author-r5 `PR-BODY.md` (trailing whitespace aside). Arm B's coverage is stated exactly at lines 19, 69 and 173; R703-4-R1's rename is at line 75; "Relates to #665" | live PR read only |
| Hosted checks at the exact head | Read only, at review time. Completed with success: `bdd-conformance`, `changes`, `docs-check-no-git`, `firmware-aecp-mutants`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, `Prepare pinned Yosys`. Skipped: `Physical gPTP (nightly and manual)`. Still queued or in progress: `docs-gates-*`, `elaborate-gates-*`, the firmware jobs, `publication-census`, `yosys-elaboration`, and the Verilator and Yosys shards. Acceptance of these is the manager's | `receipts/hosted_checks_head.tsv` |

## Findings

No BLOCKER, MAJOR or MINOR.

### RESIDUE (purely wording; exact fix given; does not make the verdict NEGATIVE)

- **R703-5-R1 RESIDUE: Docs. One mutant-table row paraphrases its refusal, so "all 62 rows match the self-test's output" overstates.**
  - Where:
    - `tb/verilator/ctrl_service_budget/README.md:564` reads `refused: synthetic: the composed window committed two ACMP records, its declared load none`.
    - The self-test prints `refused: synthetic: the composed window committed {'adp': 0, 'acmp': 2, 'aecp': 0, 'maap': 0, 'srp': 0, 'GM': 0, 'LINK': 0}, its load is {'adp': 0, 'acmp': 0, …}` (`receipts/selftest.log`).
    - The PR body (finding table, last row) and the REVIEW READY comment say "All 62 rows of the table now match the self-test's output".
    - The published `author-r5/receipts/mutant_table_check.txt` is the check from before the fix (2 BAD), and no receipt from after the fix is published.
  - Impact: none on any figure, check or mutant. The row names the right refusal, but not as printed.
  - Exact fix:
    - Make the row's cell a verbatim prefix of the printed line, for example ``refused: synthetic: the composed window committed {…, 'acmp': 2, …}, its load is {… all zero}`` with the dicts quoted as printed.
    - Or keep the paraphrase and change the PR body's sentence to "61 rows quote the self-test's output; the declared-load row paraphrases its refusal".
  - Verification: `scripts/table_vs_selftest.py README.md selftest.log` reports 0 mismatches.
- **R703-5-R2 RESIDUE: Docs. The PR body says the table line is "rendered from" the `results.json` record.**
  - Where: the PR body's R703-4-F2 row: "A second new check requires that record to equal the expected one, and the table line rendered from it to match word for word."
  - What is true: `run.table` (`run.py:136`) calls `composed_maximum(results)` itself rather than reading the `summary` record. Both come from the same function, and the check pins both against the same expected record (`selftest.py:446-454`).
  - Exact fix: "…and the table line rendered from the same `run.composed_maximum` record to match word for word."
- **R703-1 R-4 / R704-3-R1 (carried, retained).** `docs/testing/TESTING.md:518` still reads "The manual `nvm_capture_cpu` measurement is the Makefile exception." The file is outside the lane, as the author discloses. Fix as R704-3-R1 states.

### SUGGESTION (optional)

- **S1 (probe M1): Tests. The `results.json` check exercises `run.summary`, not the file `main()` writes.**
  - Planting `dict(summary(...), composed_maximum=None)` at `run.py:317` leaves the self-test green (`receipts/probe_M1_main_bypass.log`, rc 0, 0 failures). An unplanted copy of the tree is also rc 0 (`probe_M0_copy_baseline.log`).
  - Today `main()` writes `summary(...)` unchanged, and the published records equal the recomputed ones. So no figure is affected, and R703-4-F2's required outcome (a check on the table line, "or equivalently" on the record) is met by the table-line half.
  - Optional: route the write through a small `write_results(out, ...)` that the check calls on a temporary directory and reads back. Or name the check "`run.summary`'s composed maximum is the record the table renders".
- **S2: Tests. The mutant loop counts any exception from `checks()` as caught (`selftest.py:777-781`).**
  - A refusal or a `TypeError` in one group hides the others' results, which is how the two table rows went stale.
  - The isolation run shows every mutant still fails a named check today.
  - Optional: run each check group under its own `try`, so the first named failure is reported even when another group refuses.
- **S3 (carried, optional):** R703-4 S1 (P6: unsorted fan-out recipients) and S2 (P9: release at exactly the commit), R703-3's H3, and the older G2, G3, N11 and N12 escapes. All are unchanged, and none changes a published value.

## Prior public findings at this head

| Finding | Status at `f58d049b` | Evidence |
|---|---|---|
| R703-4-F1 MINOR (Robustness, Tests, Docs): an incomplete set of backlog rows reported as the composed maximum, arm B's included | **Resolved at cause.** `run.composed_maximum` (`run.py:67-86`) names `not_run` against `grade.BACKLOG_ROWS`, with `rows` and `partial`; `run.table` (`run.py:139-140`) labels the figure "over N of 4 backlog windows, a partial figure (… not run)". The new check `a run without every backlog row names the rows not run, and its composed maximum is partial` (`selftest.py:424-432`) is killed by the mutant `selftest_mutants.py:372`. The README (`:66`, `:157`, `:170`, `:202-204`, `:209-210`, `:441-446`) and the PR body (lines 19, 69, 173) state arm B's three rows. D1 reports the rows and the label | `receipts/r703_4_probes/`, `receipts/recompute_composed.txt`, `receipts/selftest.log` |
| R703-4-F2 MINOR (Tests): the check did not pin its own lower-bound rule or the published label | **Resolved at cause.** `selftest.py:417-422` has the longest window release its load while a shorter one does not, and asserts `lower_bound: True`; P7 is caught, and so is the own-window mutant at `selftest_mutants.py:370`. `selftest.py:434-454` pins the record and both table lines word for word in three cases; P3, P4 and P5 are caught, as are the mutants at `selftest_mutants.py:374-379` | `receipts/r703_4_probes/summary.txt`, `receipts/selftest.log` |
| R703-4-R1 (PR body row label) | **Applied**: "A recipient's cost, every fan-out, both arms (arm A in brackets)" | live PR body line 75 |
| R703-1 R-4 / R704-3-R1 (`docs/testing/TESTING.md:518`) | **Retained** as residue (outside the lane) | `docs/testing/TESTING.md:518` |
| R703-4 S1 to S3 (optional) | Not applied; they stay optional | `receipts/r703_4_probes/summary.txt`, `review_mutants{2,3}_head.log` |

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **CLEAN** | `[R703] PASS Conformance — run.py:67-86, :115-145; README.md:197-214, :436-446; PR body lines 14-30, 66-75; author-r5 head-regrade composed_maximum_records.json, recomputed in receipts/recompute_composed.txt — the S2 acceptance (worst pass at the composed maximum; each backlog row at 1x1/1 interface and 8x8/2 interfaces; each against T_svc and the 3.4.1 ceiling) holds for the formal arm A: all four rows run, and at least 31.32 / 44.19 ms is labelled a lower bound. Arm B's figure is now labelled partial, not the composed maximum. No measured cycle count changed, per the round-5 scope. The rows still miss T_svc, which is the D4 STOP, so the PR says "Relates to #665"` | R703-5 | `f58d049beb377c3f535628067022d4d5b51e8208` |
| RTL | **CLEAN** | `[R703] PASS RTL — receipts/delta_stat.txt (git diff --stat a66148f6..f58d049b): only run.py, selftest.py, selftest_mutants.py and README.md change. No RTL, SoC (split_soc.py), sim_main.cpp, observe.vlt, build.py, firmware or CI file is in the delta, so the R703-3 RTL result (mailbox RX accounting against mailbox.yaml:419-433) still holds; nothing it depends on changed` | R703-5 (R703-3 at `f8876638`, an ancestor whose RTL-lens scope nothing has touched since) | `f58d049beb377c3f535628067022d4d5b51e8208` |
| Robustness | **CLEAN** | `[R703] PASS Robustness — run.py:67-86, :139-140 against configuration-dependent group selection (--groups, README.md:44-66): one row, three rows and all four rows (D1, selftest.py:424-454); an unreleased window shorter than the longest (selftest.py:417-422); a backlog group without a composed window is refused (grade.py:761-763); controls and the SHUTDOWN arm give a null record and no line (receipts/recompute_composed.txt)` | R703-5 | `f58d049beb377c3f535628067022d4d5b51e8208` |
| Tests | **CLEAN** | `[R703] PASS Tests — selftest.py:393-455 (maximum_checks), :777-781 (mutant loop); selftest_mutants.py:117-136, :370-379; receipts/selftest.log (87/62); receipts/isolate_all.txt (each of 62 mutants fails a named check in isolation); receipts/r703_4_probes (P3, P4, P5, P7 now caught); receipts/review_mutants{2,3}_head.log (unchanged); receipts/probe_M1_main_bypass.log (SUGGESTION S1 only)` | R703-5 | `f58d049beb377c3f535628067022d4d5b51e8208` |
| Docs | **CLEAN** (RESIDUE R1, R2 and the carried TESTING.md item do not leave a lens unclean) | `[R703] PASS Docs — README.md delta by section (:63-67, :154-158, :167-170, :199-216, :438-446, :519-526, :558-601); receipts/table_vs_selftest.txt; live PR body against author-r5 PR-BODY.md; receipts/gates_summary.txt (docs_check, doc_style, doc_paths, py_idiom rc 0) and the author's em_dash and toc receipts at HEAD f58d049b; receipts/comment_rule_delta.txt (0 lane, round or ID labels in 142 added lines)` | R703-5 | `f58d049beb377c3f535628067022d4d5b51e8208` |

My earlier ledger entries (R703-2 and R703-3) stand for code this delta does not touch: `sim_main.cpp`, `build.py`, `split_soc.py`, `scenario.py`, `grade.py`, `frames.py`, `runtime_ssp.py`, `fixture_variant.py`, `observe.vlt`, `fixture.log` and `oracle.json` are unchanged since `a66148f6`.

## Real limits of this review

- No build or simulation was run, and no figure was re-measured. The figures were checked by recomputing records and table lines from round 3's published per-group grades with the head's code. The logs themselves rest on earlier rounds' byte-identical regrades and on my R703-1 reproduction.
- `check_em_dash` and `gen_toc --check` were NOT RUN here, because the pinned renderer is absent. They rest on the author's receipts at this head plus my direct em-dash scan of the delta.
- I read the author's other 90 gates from the published summary only and did not re-run them.
- I did not run the parent, protocol-processor, gPTP, Yosys or builder banks. Physical calibration was NOT RUN, and the field skips are not hardware proof.
- Hosted contexts were read once and most were still running.
- No source bank was run by the manager at this head, and I claim none.
- The first invocation of the two older mutant scripts was wrong: I passed a plain clone instead of the sandbox layout. The scripts refused, and the damage was confined to my disposable clones, which I restored with `git checkout`. The rerun in the correct layout is the result above.
- Session-created ignored bytecode (`scripts/__pycache__` from the docs gates) was removed from the review clone. Afterwards, tracked bytes and modes match HEAD, the index tree is `ded39255…`, the status (ignored files included) is empty, and the six submodule gitlinks are as at HEAD (`receipts/clone_identity_final.txt`).

## Pending manager duties

- Hosted acceptance of the exact-head contexts still running at review time (`docs-gates-*`, `elaborate-gates-*`, the firmware jobs, `publication-census`, `yosys-elaboration`, and the Verilator and Yosys shards), and act replication.
- The current-dev merge candidate (source base `e76a755a`, live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`, target `dev-soft-core`), with builder and native banks, before the merge turn.
- The residue checklist: R703-5-R1, R703-5-R2, and the carried `docs/testing/TESTING.md:518` item.
- Carried from the author's open questions: whether the ACMP owed-capacity drop, the SRP starvation and the per-recipient fan-out cost become Issues or S2b scope.

R703-5 FINISHED
