[R260] POSITIVE - exact head 0ca178678490024707b3a2393a86dc9e7b2a0ca4

# R260-1: independent review of protocol-processor issue #104 / PR #105

| | |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| Issue / PR | #104 / #105 (`104-fixture-guard-idiom` into `main`) |
| Exact head | `0ca178678490024707b3a2393a86dc9e7b2a0ca4`, tree `897a49d0e7eb25e910ff63984c5000403375dca2` |
| Source base | `e1d0176d3a486bce4a80765cfbcefcb61964f8e9` (PP `main` at review time; PR is MERGEABLE/CLEAN) |
| Parent consumer | kebag-logic/milan-fpga live `dev` `ede8d48ecd7c7f589a14b957951f040d92c99c70` |
| Round | R260-1, internal independent reviewer, cleared context, own detached clone |
| Verdict | **POSITIVE**. No BLOCKER, MAJOR or MINOR finding. Three SUGGESTIONs, none of which affects lens coverage. All five lenses are CLEAN at the exact head. |

## 1. What was reconstructed, in order

1. **Repository conventions.** This repository has no `AGENTS.md` or `CONTRIBUTING.md`, so its conventions were read from `README.md` (the "Building and checking" gates and the consumption contract), `docs/README.md`, `hdl/README.md` (the submodule consumption contract), `.github/workflows/hdl.yml`, `tb/pp_top/Makefile` and `tb/pp_top/README.md:523-544`. The consumer's review contract is the parent's `AGENTS.md` §6-§7, covering lenses, finding format and completion ledger.
2. **Frozen acceptance for issue #104** (issue body): both functions are annotated and documented; the parent's `check_py_idiom.py` exits 0 with this repository staged at the fix head; this repository's own gates stay green. The manager's assignment comment adds that two independent reviewers review the PR and that the parent consumer gates run with the fix head staged before merge.
3. **Requirement authority.** This is parent `docs/development/CODE_QUALITY.md` Rule 12 at `ede8d48` (line 2567 onward): "New and touched public functions SHOULD carry a complete PEP 484 signature and a docstring". The gate is parent `scripts/check_py_idiom.py`. It treats a function as public unless its name starts with `_` (`:247`). "Annotated" means every non-`self`/`cls` parameter plus a return annotation (`:256-258`). "Documented" means `ast.get_docstring(node) is not None` (`:400-404`). The population includes both pinned processors through `code_quality_scope.py`, which refuses an off-pin checkout.
4. **Diff and history** `e1d0176..0ca1786`: one commit on the base, 2 files, +19/-2, modes unchanged at 100644 (`receipts/diff-and-hygiene.txt`).
5. **Public evidence.** Author packet `review-evidence/pp104-r1/author-a193/` at milan-fpga `667e920`. Manager consumer receipts `review-evidence/pp104-r1/manager-consumer/` at `a906e65`, the direct child of `667e920`, as linked from the PR comment. Every downloaded blob re-hashed to its tree entry. The archived `PR-BODY.md` equals the live PR body apart from a trailing newline. Hosted CI at the exact head was also inspected.

## 2. Findings

None at BLOCKER, MAJOR or MINOR. Three SUGGESTIONs are optional improvements; per parent `AGENTS.md` §7 they do not affect coverage.

**S1**
```text
[R260] SUGGESTION Docs, Robustness - tb/pp_top/fixture_guards.py:14-23 - main()'s docstring omits two environmental preconditions
Requirement/evidence: The docstring says "A failed VERILATOR_ROOT query or model generation raises
  CalledProcessError". That is true for a tool that runs and exits non-zero (receipts/contract-probes.txt S07, S08).
  An ABSENT Verilator (S09) or an ABSENT C++ compiler (S10) raises FileNotFoundError instead, from :32 and :53.
  The compiler case is not mentioned at all. The function also compiles "sim_main.cpp" relative to the current
  working directory (:54), which only tb/pp_top/Makefile:68 establishes. Base and head behave identically on all
  four paths, and nothing the docstring states is false.
Impact: A direct caller outside the Makefile may not expect an OSError, or the CWD dependence. No gate reads the docstring.
Required outcome (optional): name the absent-tool OSError and the tb/pp_top working-directory precondition, or leave as is.
Verification: re-run scripts/contract_probes.py; S09/S10 unchanged, docstring clauses matched.
```

**S2**
```text
[R260] SUGGESTION Conformance, Tests - tb/pp_top/test_fixture_guards.py:15,35 - the new "-> None" opts the test body into type checking, where one pre-existing inference gap shows
Requirement/evidence: The annotation is correct (the method has no return statement; receipts/annotation-check.txt).
  Because the method is now annotated, a PEP 484 checker in default mode checks its body for the first time and reports
  `:35 Need type annotation for "results"`, on a line this PR did not touch. At base, default mode reports nothing
  because the body is unchecked. fixture_guards.py is clean even under --strict at head. No gate in this repository
  or the parent runs a type checker (searched; parent CODE_QUALITY.md says no type-checker configuration exists).
Impact: None today. It would surface only if a type checker is adopted later.
Required outcome (optional): if a checker is ever adopted, annotate `results` as list[subprocess.CompletedProcess[str]].
Verification: scripts/annotation_check.sh, default mode, exits 0 at the head.
```

**S3**
```text
[R260] SUGGESTION Tests, Robustness - tb/pp_top/fixture_guards.py:63-67 - the documented "Returns 1" contract has no in-repository regression arm (pre-existing, outside #104)
Requirement/evidence: The new docstring states the mismatch contract, and the stub probes confirm it at base and head
  (S03-S06). The unit test covers only the exit-0 path, and its docstring claims no more than that. Mutant M13
  ("never report a mismatch") survives it at base and head (receipts/mutation-probes.txt). `make fixture-guards` runs
  only the passing real-compiler cases. tb/pp_top/README.md's mutation record lists no control for this branch.
  The gap predates this PR, which changes no statement.
Impact: A regression that stopped the guard from failing would pass locally and in CI.
Required outcome (optional, separate work): a mocked-subprocess arm that requires exit 1 and the printed compiler output on a mismatch.
Verification: M13 is killed.
```

## 3. Per-lens results (clean lens lines carry their artifact)

```text
[R260] PASS Conformance - issue #104 acceptance; parent scripts/check_py_idiom.py:247-258,400-404 at ede8d48; receipts/parent-consumer/{base,head,shipping}/01-02 - staged at base e1d0176 the gate exits 1 with "unannotated public function 2 > ratchet 0" and "undocumented public function 2 > ratchet 0", and --list attributes exactly one of each to tb/pp_top/fixture_guards.py and to tb/pp_top/test_fixture_guards.py; staged at 0ca1786 it exits 0 with both at 0 <= 0 and every other ratchet at budget (220 modules, 160384 lines, the same totals as the manager's receipt 02.log); the shipping pin 424c688 also exits 0; --selftest 54/54 at head. An independent re-derivation of the Rule 12 census over all 11 tracked .py files (receipts/ast-equivalence.txt; stricter, since it also counts *args/**kwargs) gives 2/2 at base and 0/0 at head. Both annotations are complete signatures (no parameters besides self). The repository-gates leg of the acceptance is covered under Tests and Docs below.
[R260] PASS RTL - receipts/untouched-trees.txt; receipts/repo-gates/head-lint-hdl.log; receipts/repo-gates/head-pp-top-suite.log - the only changed paths are the two tb/pp_top/*.py files; hdl/, syn/, scripts/, docs/, .github/, tb/pp_top/{sim_main.cpp,pp_top_wrap.sv,Makefile,README.md} have identical object ids at base and head. lint_hdl.sh exits 0 at head with the pinned Verilator 5.050 (37 LINT OK). Full tb/pp_top suite at head: 1411 checks, 1411 PASS, 0 FAIL. The parent's source-list gates (check_rtl_source_lists, pp_srcs --check --selftest) give byte-identical output with base and head staged. No RTL contract can have moved.
[R260] PASS Robustness - receipts/contract-probes.txt/.json (S01-S12, base vs head) - every failure path gives the same exit status, stdout, final exception line and tool-call log at base and head: a compiler that always succeeds, an unrelated error, a missing diagnostic, an extra error, a failing root query, failing model generation, an absent Verilator, an absent compiler, the form without "--", and --help (the argparse description is the module docstring, which is unchanged). S01 uses a locale-sensitive stub compiler with the caller at LC_ALL=fr_FR.UTF-8; it passes only because the compiler really receives LC_ALL=C, while model generation still sees the caller's LC_ALL. The only observable differences are unittest's -v description line and traceback line numbers (+10), and no gate or script consumes either (Makefile:71-72 runs the test, and nothing parses its report).
[R260] PASS Tests - receipts/mutation-probes.txt; receipts/repo-gates/{base,head}-fixture-guards*.log - the kill matrix is identical at base and head. All 12 behavioural mutants are killed (failures=2, both LC_ALL subtests), and each maps to a clause of the new test docstring: the LC_ALL override removed or changed, LC_ALL leaking into model generation, the caller environment mutated, a case dropped, the cxx command not split, a non-zero final return, an exact-flag change, the root-query arguments, the leading "--" kept, flag order, and stderr not merged. The docstring-text and annotation-removal controls survive. The one other survivor (M13) is outside what the docstring claims (see S3). With the real pinned Verilator and compiler, the make fixture-guards verdict lines ("4 cases PASS") are byte-identical at base and head. Hosted "suites" at the exact head ran every suite (30 suites PASS, pp_top 1411/1411).
[R260] PASS Docs - tb/pp_top/fixture_guards.py:14-23 and tb/pp_top/test_fixture_guards.py:16-22 against the code at fixture_guards.py:24-71 and test_fixture_guards.py:23-67; tb/pp_top/README.md:523-544; receipts/repo-gates/head-{check-links,check-matrix,wavedrom-check,make-stale,gen-matrix-check}.log - every docstring clause was checked against the code and by a probe. For main(): its inputs, one model generation into a temporary directory, the four cases in order under LC_ALL=C, "Returns 1 after printing the compiler output" on an exit-status, diagnostic or error-count mismatch, and CalledProcessError. For the test: the mocked subprocesses, the two LC_ALL states, and the listed requirements, each killed by a mutant. No clause overclaims (S1 records two omitted preconditions). Both docstrings agree with the README's fixture-guards paragraphs, which need no change, and docs/ is untouched. Docs gates pass at head (links 807 OK, matrix 115 REQ / 17 GAP OK, wavedrom 18 OK, stale OK, module matrix 86 rows / 0 untested). The PR body and the public author packet give a cold reviewer enough to reproduce. New lines are at most 88 columns, with no trailing whitespace, tabs or non-ASCII.
```

## 4. Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #104 acceptance; parent CODE_QUALITY.md Rule 12 and check_py_idiom.py at `ede8d48`; parent gates with the PP gitlink staged at base/head/shipping; independent Rule 12 census | R260-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |
| RTL | CLEAN | full diff name-status; subtree ids of hdl/syn/scripts/docs/.github and the pp_top bench at base vs head; lint_hdl.sh; full tb/pp_top suite; parent source-list gates | R260-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |
| Robustness | CLEAN | contract probes S01-S12 at base and head (failure, exception, locale, argv and help paths) | R260-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |
| Tests | CLEAN | unit-test kill matrix (16 mutants and controls) at base and head; real-compiler fixture guards at base and head; full pp_top suite; hosted suites job at the exact head | R260-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |
| Docs | CLEAN | both docstrings clause by clause against the code; tb/pp_top/README.md:523-544; docs gates; PR body and author packet | R260-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |

Open findings by lens: none at MINOR or above. S1 (Docs, Robustness), S2 (Conformance, Tests) and S3 (Tests, Robustness) are SUGGESTIONs.

## 5. Behaviour preservation (the focus question)

- **AST equality** (`scripts/ast_equivalence.py`, `receipts/ast-equivalence.txt`). In each file, removing only what the base lacks leaves an AST equal to the base: `main`'s `-> int` and 10-line docstring, and the test method's `-> None` and 7-line docstring. Removing every def docstring and annotation from both sides also gives equality. Module docstrings are unchanged, and nothing else was stripped or added.
- **Annotations are true** (`receipts/annotation-check.txt`). `main` returns only the int literals `0` and `1`, and the runtime returns `int` on both the pass and mismatch paths. The test method has no return statement. A PEP 484 checker, run from a disposable venv and not as a project gate, finds nothing in `fixture_guards.py` at head even under `--strict`. At base, `--strict` flagged `main` as untyped. For the test body, see S2.
- **Consumer effect.** Of the eleven parent gates run at base and head (§3), only `check_py_idiom` output changes, and only in the two Rule 12 counts.

## 6. Hosted evidence at the exact head (inspected, not owned)

Workflow `hdl` ran twice at `0ca1786`: push run 35853375707 and pull_request run 35853380979. In both, the `docs-gates`, `suites` and `portability` jobs **executed** and succeeded. The only skipped step is "Build Verilator v5.050", skipped on a cache hit by design. In the pull_request suites job log, all 30 suites report PASS (pp_top 1411/1411), Verilator is 5.050, lint shows 37 OK, the matrix is OK and the nvm_port figures step ran (`receipts/hosted-suites-verdicts.txt`). Hosted and act acceptance is the manager's.

## 7. Prior public review findings on this PR

This was checked only after the verdict and ledger above were written. It covers PR #105's comments, reviews and inline comments, and issue #104's comments.

- **There were no prior public review findings.** Before this round's public start (PR comment 5794532378, 2026-09-23T12:09:28Z), the PR carried one manager evidence comment and no review. That comment (5793951656) reported the parent consumer gates passing at `0ca17867`, and this round re-derived it independently in `receipts/parent-consumer/`. The PR has no GitHub reviews and no inline comments. The issue carries only the manager's assignment and the author's REVIEW READY hand-off, whose claims are checked in §3 and §5. So nothing needs resolving or retaining.
- One concurrent review was posted after this round started: R261-1, comment 5794884910 at 12:33:21Z. It is not a prior finding. Its content was not read, so that the two reviews stay independent as the owner decision on the PR requires. Reconciling the two reviews is the manager's job.

## 8. Real limits

- The full `./scripts/run_suites.sh` bank was **not run locally**; the brief forbids full PP banks. The diff cannot reach any other suite, since no other suite references the two files. The hosted `suites` job at the exact head ran every suite.
- `make check`'s `lint` target (the mermaid renderer) was **not run**, because the renderer is not installed. The CI docs-gates job does not run it either, and `docs/` is byte-identical to base. All other `make check` components were run.
- The parent's `xvlog_gate --check` (vendor analyser), `sw/builder/test_builder.py` (the builder bank), the `pp_shadow` suite and Yosys portability were **not run** by this reviewer. The manager's receipts at milan-fpga `a906e65` record exit 0 for the first three. `test_builder.py` states "1 GATE ARM(S) DID NOT RUN" (gate 11 needs a build tree), so that arm is not covered. Hosted `portability` succeeded at the exact head.
- The consumer probe used a disposable parent clone at live `dev` `ede8d48` with protocol-processor, gptp-processor (`c1b6174`) and verilog-axis at their recorded pins. `external` was left uninitialised; it is not a project processor, so the scope helper does not require it.
- The local pp_top suite and fixture-guard runs replaced the Makefile's `-j 0` with `-j 8` under `taskset -c 0-7`, the brief's parallelism cap. That is the only change to `VFLAGS`. Local tools: Python 3.14.7, GCC 16.2.1, pinned Verilator 5.050 (`receipts/tool-identity.txt`).
- Probe incident, disclosed. The first local gates attempt exported a helper variable whose name Verilator itself reads. That sent the pinned wrapper into a re-entry loop. Only this reviewer's own process group was terminated; another session's processes were not touched. The aborted receipts were discarded, the variable was renamed, and every affected step was re-run. The parent-consumer receipts were regenerated, and their gate logs are byte-identical to the first run.
- Published receipts have host paths redacted to `$PACKET`, `$REVIEW_CLONE`, `$VALIDATION_STORAGE` and `$WORKSPACE_HOME`. The unredacted originals stay in the unpublished scratch tree.
- **Physical calibration NOT RUN.** No hardware was used, and skipped field or hardware contexts are not hardware proof.

## 9. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn: the parent at live `dev` (`ede8d48` at review time) with the protocol-processor gitlink moved to the merge result of source base `e1d0176` and this head, including the full parent static, builder and native banks.
- Own hosted and act acceptance for the merge candidate.
- The second independent review (R261). Merge requires two independent POSITIVE reviews and the full completion bar in parent `AGENTS.md` §7.
- Publish this packet: REPORT.md plus the files listed in MANIFEST.sha256.

## 10. Reproduction (portable scripts, paths are arguments)

```sh
scripts/ast_equivalence.py   <pp-clone> e1d0176d3a486bce4a80765cfbcefcb61964f8e9 0ca178678490024707b3a2393a86dc9e7b2a0ca4
scripts/contract_probes.py   <pp-at-base> <pp-at-head> <workdir>
scripts/mutation_probes.py   <pp-at-base> <pp-at-head> <workdir>
PINNED_VERILATOR=<verilator-5.050> scripts/repo_gates.sh <pp-at-head> <pp-at-base> <out> {guards|docs|lint|suite}
PINNED_VERILATOR=<verilator-5.050> scripts/parent_consumer.sh <parent-clone-with-pinned-submodules> <out> base=e1d0176... head=0ca1786... shipping=424c688...
scripts/annotation_check.sh  <pp-at-base> <pp-at-head> <type-checker>
scripts/verify_clone.sh      <review-clone> 0ca178678490024707b3a2393a86dc9e7b2a0ca4 897a49d0e7eb25e910ff63984c5000403375dca2
```

Review clone integrity after all probes: `receipts/clone-integrity.txt`.

R260-1 FINISHED
