[R354] NEGATIVE - exact head 77998f14b16bf7605956332d0f0ac8af0cecab5a

# R354-2: internal independent re-review of PR #596 (issue #582)

- Role: internal independent reviewer, cleared context, own detached clone.
- Head under review: `77998f14b16bf7605956332d0f0ac8af0cecab5a`, tree `8efca551799d1ef09c09e6194720bc6fb25b840a`.
- Source base: `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`.
- Delta under review: `3baff441..77998f14`, two commits:
  - `f8c03bd0` "Close clock contract review gaps in CI, ROM checks, refusals and documentation";
  - `77998f14` "Preserve the system clock mutation after adding CLI help".
- The whole PR diff `9e9954e9..77998f14` was also read. It touches 13 files. Nothing changed under `hdl/`, `tb/`, `sw/firmware/` or `configs/`, and no gitlink moved.
- Scope was reconstructed from:
  - AGENTS.md, CONTRIBUTING.md (sections 2, 5 and 6) and docs/README;
  - the issue #582 body (acceptance 1-4);
  - [A10] comments 5853404680, 5855343934 and 5857543940;
  - the round-2 assignment 5858125516 (required items 1-6, the out-of-scope note and the unchanged list);
  - the [A374] TAKEN and REVIEW READY comments;
  - `CI_WORKFLOWS.md` gate-read policy, `scripts/ci_scope.py`, `BAREMETAL_FIRMWARE.md` build contract, `README-parameters.md` Product profile, `ENDSTATION_BUILDER.md` rows 5a and 34, and the `milan_soc.py` usage block and help.
- Lenses applied this round: Conformance, RTL, Robustness, Tests, Docs.

The implementation meets all six required items, and the second commit does not weaken a test. Specifically:
- every round-1 mutant from both reviews that the assignment names is now KILLED;
- the five configurations stay byte-identical to the base;
- no argparse default changed.

The verdict is NEGATIVE for one MINOR Docs finding. The CI policy page now classifies `docs/AAF_LATENCY_TAPS.md` in two contradictory ways (F1).

## Findings

### F1 - MINOR - Docs - `docs/testing/CI_WORKFLOWS.md:67-69,74` against `:56-63` and `scripts/ci_scope.py:52-58,62-73` - the tap page is listed both as relevant and as a page that stays documentation only

**Authority and evidence.**
- `CI_WORKFLOWS.md:56-63` now says that four pages under `docs/` are relevant, `AAF_LATENCY_TAPS.md` among them. The classifier agrees:
  - `GATE_READ_DOCS` lists the page (`ci_scope.py:54`);
  - `echo docs/AAF_LATENCY_TAPS.md | python3 scripts/ci_scope.py` prints `true` (`receipts/ci_scope_classify.log`).
- The table that follows is introduced at `:67-69` by the rule: "A page that a skipped gate reads stays documentation only when an always-run `docs-check` step runs the same check on it".
- The new row at `:74` places this page's reader in that table and answers "yes, through the same builder bank" in the `docs-check` column. By the table's own rule, the page would therefore stay documentation only, which contradicts `:56-63` and the classifier.
- Every other row in the table names pages that do stay documentation only:
  - the six pages `test_builder.py` reads;
  - the matrix artifacts;
  - this policy page itself.
  No page in `GATE_READ_DOCS` has a row.
- The classifier's own docstring gives the same rule (`ci_scope.py:18-20`, `:66-69`): `test_builder.py` sits in `DOCS_JOB_PY` because `docs-check` runs it.
  - The new reader, `test_clock_contract.py`, runs its tap check only through `test_builder.py`: no workflow, script or Makefile invokes it otherwise, and `test_pp_mem_bridge.py` imports only its SoC function.
  - So the page's stated reason for being relevant, "Python in a classifier-gated job names them", applies equally to the six `test_builder.py` pages, and those pages are documentation only.
- The page states that nothing checks this table mechanically (`:78-79`, "stays the author's to keep true"). My mutant M29, which deletes the row, survives `ci_scope.py --selftest` (`receipts/mutants2.log`). Only a reader can catch the contradiction.
- The registration decision itself is the manager's (round-2 item 1), and this finding does not dispute it. The code is correct and conservative: a docs-only change to the page now runs the RTL-relevant gates.

**Impact.**
- The authoritative CI policy gives a cold reader two opposite answers for this page. Can a docs-only change to it skip `rtl-fast`?
  - The prose and the classifier say no.
  - The table's rule says yes.
- A later maintainer who follows the table could move `test_clock_contract.py` into `DOCS_JOB_PY` or drop the page from `GATE_READ_DOCS`, believing that restores the policy. That would reverse the recorded decision without anyone noticing.
- Round-1 F1 asked for the reader table to state the new read truthfully. The row's cells are true, but where it sits contradicts the classification.

**Required outcome.** `CI_WORKFLOWS.md` states this page's classification consistently with `GATE_READ_DOCS`. For example, the row could leave the "stays documentation only" table, or the text could say why this page is relevant even though `docs-check` also runs its check (the #582 round-2 decision). The design is the author's choice.

**Verification.**
- A reader applying the table's rule to every row reaches the classifier's result for each page.
- `python3 scripts/ci_scope.py --selftest` and the docs gates stay rc 0.

### SG1 - SUGGESTION - Docs - `sw/litex/milan_soc.py:3623` - `--no-milan` help

- The option help still reads "bare SoC, no NIC (bring-up smoke test)".
- The refreshed header (`:13-14`, `:19`) now says the path is a CLI smoke path only and "cannot finish a bare-metal image". That matches `:3947-3949`, which raises "baremetal firmware requires the protocol-processor entity image".
- The help text predates this PR, and round-2 item 5 named only the usage block and the two clock options, so this is optional.

## Required items (round-2 assignment 5858125516)

1. **Tap page gate-read: met (docs: see F1).**
   - `GATE_READ_DOCS` lists `docs/AAF_LATENCY_TAPS.md` (`ci_scope.py:54`), and the selftest case at `:265` plants it as relevant.
   - `ci_scope.py --selftest` returns rc 0 at the head (`receipts/gates-head/00-*.log`).
   - M27, which unregisters the page, and M28, which files the case as docs-only, are both KILLED.
   - `CI_WORKFLOWS.md:56-63` registers the page. The exact-head hosted `changes` and `rtl-fast` checks concluded `success` (`receipts/hosted_check_runs_head.tsv`).
2. **ROM follows the configured clock: met.**
   - `test_gptp_rom_clock` (`test_clock_contract.py:75-98`) compares the builder's `gptp_ucode.hex` for every configuration with an independent generator run at the normalized `milan_clk_hz`. It also proves that the default-clock and system-clock ROMs differ.
   - It runs in the builder bank (`test_builder.py:27557-27566`; an assertion propagates at `:27642`) and in the file's own `__main__`.
   - My round-1 M21 (`--clk-hz` dropped) is KILLED by that test and by the whole file (M21, M21b).
   - The system-clock-fed mutant, the external probe 36, is KILLED (M22, M22b).
   - M21d, my round-1 gate-1b replica, still survives. That is expected: it replays only the old assertions and is kept as a control showing the mutant changes the shipping-AX ROM (`21e846a7...` against `78c8418a...`).
3. **Product argv, `--no-milan` and `flashboot: none`: met.**
   - The SoC test now refuses ±1 Hz, 80 MHz and 100 MHz on each configuration's `emit_soc_argv` (`:125-132`). It covers `--no-milan` through both clock options, as positives and refusals (`:143-147`).
   - The builder refuses every bad clock with `flashboot: none` (`:60-63`).
   - My own implementations of the external S1-S4 (the guard exempts `--no-milan`, `--full`, `--board arty` or `--with-spiflash`) and B3 (the builder guard applies only to flashboot `baremetal`) are all KILLED.
   - Identity controls C1-C5 pass.
   - M31 is additional: `--no-milan` is exempt unless a Milan clock is given. It is KILLED.
   - M26 is additional: the builder argv drops `--milan-clk-freq`. It is KILLED.
4. **Fixed clock by reference: met.**
   - `README-parameters.md:58` names `CPU_HZ` in `recipe.py` and says "divergent values refuse".
   - `ENDSTATION_BUILDER.md:967` (row 5a) and `:1014` (row 34) say the same.
   - None restates the number, and every link resolves (`check_doc_paths` rc 0).
5. **Usage block and clock help: met; no default changed.**
   - `receipts/soc_usage_probe.log` parses the seven documented usages from the header.
     - As written, each exits 2 with `baremetal clock: effective --milan-clk-freq must be 50000000 Hz (... build contract)`, which names the requirement.
     - With the options the header names, each reaches the platform boundary: `--milan-clk-freq <CPU_HZ>` plus `--entity-gen-dir`, or `--sys-clk-freq <CPU_HZ>` for `--no-milan`.
   - An AST comparison of all 54 `add_argument` calls between base and head finds no non-help keyword difference.
   - The `--sys-clk-freq` and `--milan-clk-freq` help (`:3391-3405`) matches the guard `(args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ` (`:3704`).
   - The `--entity-gen-dir` note is refreshed (`:3494-3499`). It is consistent with `_builder_out` (`:3296-3315`) and with the bare-metal image requirement (`:3947-3949`).
6. **Normalized configuration: met.**
   - `configured_clock_pairs()` (`test_pp_mem_bridge.py:389-397`) and `_assert_sweep_clocks` (`test_clock_contract.py:161-168`) read `eb.load_config(...)["constraints"]`.
   - New arms cover an omitted `sys_clk_hz`, which resolves to the board default.
   - My probe shows the round-1 `KeyError` is gone: `configured_clock_pairs -> [('endstation_nosys', 100000000, 50000000)]` (`receipts/bypass_probe.log`).
   - The mutants for a raw YAML read (M23), a raw read with a wrong default (M24) and a sweep that fills an omitted system clock from the Milan clock (M25) are all KILLED.

**Second commit (`77998f14`).** It touches only `scripts/check_solution_docs.py:794-795`. Receipt: `receipts/second_commit_check.log`.
- Adding `help=` to `--sys-clk-freq` split the argument across lines, so the old needle `... default=100e6, type=float)` matches 0 times at the head. The `f8c03bd0` checker's selftest then fails with "missing fixture for system clock default".
- The new needle `... default=100e6,` matches exactly once and makes the same substitution (100e6 to 80e6).
- The fact is read through the AST (`check_solution_docs.py:250-268`), so `help=` does not affect it.
- The selftest reports 43 mutation controls at both base and head, rc 0.
- M30, the same mutation run against the real checker, is KILLED.
- Conclusion: no test was weakened.

**`scripts/check_solution_docs.py`, not named in the assignment.** The needle edit above is the whole change to this file (2 lines) and is required by item 5's help text. No other assertion changed.

**Five configurations byte-identical.**
- Base and head were extracted with `git archive`, and identical submodule contents were added to both.
- The five configurations were built with each tree's own builder, with fragments written.
- 58 of 58 generated files are identical (`receipts/artifact_identity.log`, `artifact_identity_head.sha256`).
- The shipping AX ROM stays `78c8418a...`, the value the capture receipt records, and `check_nvm_capture.py` returns rc 0.

**Acceptance 1-4 of #582.** Unchanged from R354-1, and still met at this head:
- the refusals and bypass probe (`receipts/bypass_probe.log`, 15 of 15 as expected);
- mutants M01-M20, all KILLED again;
- the tap table (M19 and M20 KILLED);
- artifact identity.

## Kill-tests (`scripts/mutants2.py`, `receipts/mutants2.log`)

- **Controls:** 5 of 5 pass (C1-C5).
- **Totals:** 39 mutants. 37 are KILLED and 2 are informational survivors (M21d, M29).
- **Round-1 mutants:** M01-M20, M21 and M21b are all KILLED again. M21d survives as the expected replica control.
- **Named external mutants:** probe 36 (M22 and M22b), S1-S4 and B3 are all KILLED.
- **New for round 2:** M23-M28, M30 and M31 are KILLED.
- **M29 survives.** It deletes the new CI_WORKFLOWS row, and by the page's stated policy no check covers that row. It is evidence for F1, not a separate finding.

## Prior public review findings (read after my own pass over the diff)

| Prior item | Status at 77998f14 | Evidence |
|---|---|---|
| R354-1 F1 BLOCKER (gate-read page unregistered) | RESOLVED for the classifier, selftest and hosted classification. The reader-table part is superseded by R354-2 F1 | `gates-head/00`, M27/M28, `hosted_check_runs_head.tsv` (`changes`, `rtl-fast` success) |
| R354-1 F2 MINOR (ROM clock not proven) | RESOLVED | M21, M21b KILLED by `test_gptp_rom_clock` |
| R354-1 S1 (raw YAML reads) | RESOLVED (taken as item 6) | M23-M25 KILLED; `bypass_probe.log` |
| R354-1 S2 (usage block, `--entity-gen-dir` note) | RESOLVED | `soc_usage_probe.log` |
| R354-1 S3 groups 1-3 | RETAINED as informational, consistent with the one-source decision | unchanged files |
| R354-1 S3 groups 4-5 | Out of scope by assignment (#495 at merge) | - |
| R355-1 F1 BLOCKER | RESOLVED, as R354-1 F1 | as above |
| R355-1 F2 MINOR (S1-S4, B3 survive) | RESOLVED | my own S1-S4 and B3 KILLED, controls pass |
| R355-1 F3 MINOR (probe 36) | RESOLVED | M22, M22b KILLED |
| R355-1 F4 MINOR (parameter reference) | RESOLVED | `README-parameters.md:58`, `ENDSTATION_BUILDER.md:967,1014` |
| R355-1 F5 MINOR (usage and help) | RESOLVED | `soc_usage_probe.log` |
| R355-1 SG1-SG4, observation | RETAINED as suggestions; not required by the assignment and not re-examined | - |
| Manager bank r1 comment 5857952562 (gate 6) | RESOLVED | `gates-head/00` rc 0 |

## Gates run at the exact head (`scripts/run_gates.py`, `receipts/gates-head/SUMMARY.tsv`, `receipts/gates-md/`)

- **All rc 0:**
  - `ci_scope.py --selftest`;
  - `check_solution_docs.py`, plain and `--selftest`;
  - `docs_check.py`, plain and `--selftest`;
  - `check_doc_style.py`, plain and `--selftest`;
  - `check_doc_paths.py`;
  - `DOC_MAP.gen.py --check`;
  - `check_baremetal_only.py --check` and `--selftest`;
  - `check_entity_shape.py --self-test`, `check_deploy_shape.py --self-test` and `check_sweep_shape.py --self-test`;
  - `check_py_idiom.py` and `check_sh_idiom.py`;
  - `check_hygiene.py --check`;
  - `measure_naming.py --check`, `measure_fail_fast.py --check` and `measure_test_evidence.py --check`;
  - `check_soc_sources.py`;
  - `check_nvm_capture.py`;
  - `test_declarations.py`;
  - `test_clock_contract.py --soc`;
  - `test_pp_mem_bridge.py`;
  - `git diff --check 9e9954e9 HEAD`.
- **Renderer gates.** `check_em_dash.py --base 9e9954e9` (49 added lines, 339 of 339 arms) and `--selftest`, plus `gen_toc.py --check`, `--verify-anchors` and `--selftest`, returned rc 2 in the first pass: the host interpreter lacks the pinned Markdown renderer. All five returned rc 0 in a private venv under `scratch/`, installed with `--require-hashes` from `tools/markdown/requirements.txt`.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #582 acceptance 1-4; [A10] 5853404680, 5855343934, 5857543940, and 5858125516 items 1-6 plus its unchanged list; `endstation_builder.py:66-71,4295-4305,4724-4726,5695-5704`; `milan_soc.py:1-24,3391-3405,3494-3499,3697-3707`; `README-parameters.md:47-60`; `ENDSTATION_BUILDER.md:967,1014`; `receipts/artifact_identity.log`, `soc_usage_probe.log`, `bypass_probe.log`, `second_commit_check.log`, `gates-head/25` | R354-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |
| RTL | CLEAN | Empty diff for `hdl/ tb/ sw/firmware/ configs/` and all four gitlinks (`receipts/restore_verification.log`); round-2 `milan_soc.py` changes are comment and help only (AST: 54 of 54 options, no non-help keyword change); effective-clock semantics of `_CRG` `:251-264`, `with_cpu_clk` `:2578`, `milan_cd` `:2775` and `MILAN_CLK_FREQ_HZ` `:2958`, checked against the guard at `:3704`, including `--no-milan` with a Milan domain | R354-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |
| Robustness | CLEAN | `receipts/bypass_probe.log`: `=` form, repeated options, EXTRA appended, disabled domain, `-0`, `--no-milan` at 50 and 100 MHz, sub-hertz; builder string, float, bool and int-normalized values; omitted `sys_clk_hz` through the builder, the pairs and the sweep. `test_clock_contract.py:36-72,120-149,171-198`; M13-M15, M25, M31 | R354-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |
| Tests | CLEAN | `test_clock_contract.py` (whole file); `test_pp_mem_bridge.py:386-432,945-951`; `test_builder.py:17119-17124,27555-27566,27641-27642`; `check_solution_docs.py:250-268,763-822,940-975`; `ci_scope.py:48-73,255-270`; `receipts/mutants2.log` (5 of 5 controls pass; 37 of 39 mutants KILLED; M21d and M29 are informational survivors, see above), `second_commit_check.log`, `gates-head/SUMMARY.tsv` | R354-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |
| Docs | UNCLEAN (F1 MINOR open) | `CI_WORKFLOWS.md:43-92`; `ci_scope.py:1-73`; `AAF_LATENCY_TAPS.md:11-31,139-146`; `BAREMETAL_FIRMWARE.md:19-70`; `README-parameters.md:47-60`; `ENDSTATION_BUILDER.md:967,1014`; `milan_soc.py:1-24,3391-3405,3494-3499,3623`; `receipts/gates-head/01-12,18-19`, `receipts/gates-md/*`, `ci_scope_classify.log`, M29 | R354-2 | 77998f14b16bf7605956332d0f0ac8af0cecab5a |

## Real limits

- **Not run, as assigned:** the full builder bank (either compiler mode), the parent, PP, gPTP, Yosys and native banks, Docker/`act`, host `act_ci` and hardware.
  - The new ROM test ran as a function and through `test_clock_contract.py`. Its inclusion in the builder bank was checked statically (`test_builder.py:27557-27566`).
- **Verilator not used.** The scoped path `$VALIDATION_STORAGE/tmp/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host, so its identity could not be verified. No RTL, bench or gitlink changed, so no Verilator run was needed, and no substitute was used.
- **Interpreters.** LiteX-dependent tests used the host LiteX interpreter. The five renderer gates used a private hash-pinned venv under `scratch/` (not published). Nothing was installed into a shared location.
- **SoC probes stop before the platform.** They use the PR's own boundary (`assert_front_end_routed`). Full SoC elaboration of each documented usage and Vivado were not run.
- **Hosted evidence** was inspected read-only (`receipts/hosted_check_runs_head.tsv`, fetch time in `hosted_check_runs_head.fetched.txt`).
  - At fetch time these had concluded `success`: `changes`, `rtl-fast`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, Verilator shard 3/5, `bdd-conformance`, `docs-check-no-git` and `wire-accountability`.
  - Still in progress: `docs-check`, `elaborate` and Verilator shards 0, 1, 2 and 4.
  - `Physical gPTP` was skipped, which is not evidence either way.
  - Hosted acceptance is the manager's.
- **Public evidence tree.** The linked tree `e0c591ff/review-evidence/582-r1` holds the round-1 author evidence at `3baff441`. At inspection I found no public manager bank comment at `77998f14` on the issue or the PR. The brief's statement that the manager's source banks passed at this head was not independently verified here.
- **Physical calibration NOT RUN.** Field skips are not hardware proof, and no hardware or timing-closure claim is made.
- **Clone restore** (`receipts/restore_verification.log`):
  - head, tree and index tree equal `77998f14`/`8efca551`;
  - `ls-files -s` (mode, blob, path) is identical to `ls-tree -r HEAD`, and the worktree is clean against the index after a stat refresh;
  - the four gitlinks are unchanged, and the three checked-out submodules sit at their gitlinks, clean;
  - ignored byproducts created during this round (`__pycache__/`, `sw/builder/out/`) were removed with `git clean -fdX`, so `status --ignored` is empty.
- **Redaction.** Host paths in the receipts are redacted to `$HOME` and `$VALIDATION_STORAGE`.

## Pending manager duties

- Hosted and local-replica acceptance at the head that answers F1. F1 is docs-only, so a doc-only follow-up commit un-covers only the Docs lens.
- The final current-dev candidate build: source base 9e9954e9, live dev 6d5ebd73.
- Re-review of the F1 fix under the Docs lens at the new head.
- Publishing the manager bank evidence for the reviewed head, if it is meant to be cited.

R354-2 FINISHED
