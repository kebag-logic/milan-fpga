[R354] POSITIVE - exact head aafcae59732c0a12333b73d82d5cdcbcbf90c47f

# R354-3: internal independent delta review of PR #596 (issue #582)

- Role: internal independent reviewer, cleared context, own detached clone.
- Head under review: `aafcae59732c0a12333b73d82d5cdcbcbf90c47f`, tree `0fe5f78b9be923b8f4d8ba3be3c7de196c2d7fd5`. The PR head reported by the host at fetch time is the same commit (`receipts/pr_head_state.txt`).
- Delta under review: `77998f14..aafcae59`, one commit, "Clarify clock CI policy and complete product clock test controls". It has a one-line message and no trailers. It touches three files, all mode `100644` (`receipts/head_tree_and_gitlinks.txt`):
  - `docs/testing/CI_WORKFLOWS.md`, +6 -4;
  - `sw/builder/test_clock_contract.py`, +10 -4;
  - `sw/litex/milan_soc.py`, +3 -1.
- Source base `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`. No gitlink moved between base and head (`receipts/head_tree_and_gitlinks.txt`, recursive listing).
- Scope was reconstructed from:
  - AGENTS.md, CONTRIBUTING.md sections 5-6, and docs/README.md;
  - the issue #582 body (acceptance 1-4);
  - the [A10] comments 5853404680, 5855343934, 5857543940 and 5858125516, and the round-3 assignment 5859065834;
  - the [A379] TAKEN and REVIEW READY comments;
  - the manager bank comment 5857952562;
  - the classifier `scripts/ci_scope.py`, `.github/workflows/docs.yml`, and the builder bank skip ledger in `sw/builder/test_builder.py`.
- Lenses applied this round: Conformance, RTL, Robustness, Tests, Docs.
- Independence: my verdict and ledger were written before I read any prior review text (`receipts/independent_verdict_before_prior_findings.md`). Prior findings were then resolved or retained below. The final verdict is unchanged from that draft.

The delta does what round 3 required, and nothing else changed behaviour:
- R354-2 F1 is resolved.
- The three taken suggestions are met.
- All five configurations are byte-identical to the base.
- The SoC CLI surface differs from `77998f14` only in the `--no-milan` help string.

Two new SUGGESTIONs are recorded. They do not affect coverage.

## Round-3 items (assignment 5859065834)

1. **R354-2 F1 = R355-2 SG5: tap-page classification. RESOLVED.**
   - `CI_WORKFLOWS.md:56-70` lists four relevant pages, `AAF_LATENCY_TAPS.md` among them. `:64-66` states why the page is relevant although `docs-check` also runs its check: "remains relevant under the #582 decision. Its reader is absent from `DOCS_JOB_PY`."
   - The tap row has left the table. `:71-72` now introduces the table as a list of pages that stay documentation only, with no general "when" rule.
   - My classification probe (`scripts/classification_probe.py`, `receipts/head_classification_probe.log`, PROBE PASS) checks the following at the head:
     - the four pages the paragraph names equal `GATE_READ_DOCS`, the count word "Four" matches, and each classifies relevant;
     - the table has three rows;
     - each row's reader is outside the scan, either in `DOCS_JOB_PY` or outside `GATED_ROOTS`;
     - every page each row names classifies documentation only. That is 9 builder-named pages, 3 matrix pages and this policy page;
     - the tap reader is scanned and absent from `DOCS_JOB_PY`;
     - `docs.yml` runs the builder bank, whose `__main__` runs `test_tap_clock_docs`.
   - So a reader who applies the table's rule to every row reaches the classifier's result.
   - `ci_scope.py --selftest` returns rc 0 (`receipts/head_ci_scope_selftest.log`).
   - **M29 rerun.** The row that M29 deleted no longer exists, so I ran two analogues (`scripts/m29_replay.sh`, `receipts/m29_replay.log`):
     - M29a deletes the new clause at `:64-66`. It survives `ci_scope --selftest`, `ci_events --check`, `docs_check` and my probe. This is informational, as in R354-2: the page says the table "stays the author's to keep true".
     - M29b restores the `77998f14` page, which is the F1 state. Only my probe kills it, and it does so on content (`receipts/m29b_probe_failures.log`): four rows, and the tap reader sits inside the scan.
   - A residual wording point outside the table is recorded as S2.
2. **R354-2 SG1: `--no-milan` help. MET.**
   - `milan_soc.py:3623-3625` now reads "CLI smoke path only; cannot finish a bare-metal image because firmware requires the Milan entity". That matches the usage block at `:13-14` and `:19`.
   - The claim is true in the code: `:3946-3952` raises "baremetal firmware requires the protocol-processor entity image" when no Milan windows exist.
   - An argparse dump at `77998f14` and at the head (`scripts/cli_dump.py`, `receipts/cli_diff.txt`) finds 86 actions on each side. The only differences are this help string and its `--help` rendering. No default, type or choice changed.
3. **R355-2 SG6: product argv carries `--entity-gen-dir`. MET, and S9 is KILLED.**
   - `test_clock_contract.py:133` appends `--entity-gen-dir <ROOT>/configs/generated/<stem>`. That is the form `sweep.sh:96,116` launches, and every stem's directory is tracked.
   - The SoC test stops at `assert_front_end_routed`, before the directory is read, so no generated artifact is needed.
   - My implementation of S9, mutant E1, exempts the guard whenever `--entity-gen-dir` is given (`scripts/mutants.sh`, `receipts/mutants.log`):
     - the head test KILLS it, on the arty product argv at 49999999 Hz;
     - the `77998f14` test lets it SURVIVE;
     - both unmutated controls pass.
4. **R355-2 SG7: equal-clock ROM control. MET.**
   - `test_clock_contract.py:94-102` skips the system-clock control when `sys_clk_hz == milan_clk_hz`, and prints a named `SKIP` line for it.
   - Probe EQ adds a sixth configuration: the 1x1 with `sys_clk_hz` set to 50 MHz (`receipts/mutants.log`, `receipts/mutant_logs_summary.txt`).
     - The head test passes with exactly one `SKIP` line, for that shape. No tracked shape is skipped.
     - The `77998f14` test fails with "ROM clock control is insensitive".
   - Both ROM-clock mutants remain KILLED on the tracked shapes. Each fails with "gPTP ROM does not use configured Milan clock":
     - R1 drops `--clk-hz`;
     - R2 feeds `sys_clk_hz`;
     - EQ+R1 drops `--clk-hz` with the equal-clock shape present.
   - The unmutated ROM arm passes.
   - See S1 for how the SKIP is reported inside the builder bank.
5. **Nothing else changed behaviour, and the five configurations stay byte-identical. MET.**
   - The delta touches only the three files above:
     - `milan_soc.py`: help text only (item 2);
     - `CI_WORKFLOWS.md`: prose only;
     - `test_clock_contract.py`: the two test edits above.
   - `scripts/identity.sh` builds all five configurations with the builder CLI and `--write-fragment`. Both sides use one disposable copy at the same path, checked out first at `9e9954e9` and then at `aafcae59`.
   - All 57 generated files are identical: output trees plus `configs/generated/`. The diff is empty (`receipts/identity.log`, `receipts/identity/identity_{base,head}.sha256`, `identity_diff.txt`).

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### S1 - SUGGESTION - Tests, Robustness - `sw/builder/test_clock_contract.py:95-97` - the equal-clock SKIP bypasses the builder bank's skip ledger

- **Authority and evidence.**
  - `test_builder.py:370-402` keeps `SKIPPED` and `skip()` so that "the verdict names what did not run" (#154).
  - `:27643-27651` prints `ALL GATES PASS EXCEPT n NOT RUN` from that ledger.
  - `test_builder.py:27559-27566` runs `test_gptp_rom_clock` inside that bank. The new SKIP only prints, so on an equal-clock shape the bank would still print `ALL GATES PASS`.
- **Impact.** None today: all five tracked shapes have `sys_clk_hz != milan_clk_hz` (receipt EQ: exactly one SKIP, for the planted shape only).
  - The skipped control is also logically inapplicable. On such a shape the system-clock mutant cannot change bytes, and the main byte-equality assertion still runs.
  - So no proof of product behaviour is lost. This is why it is a suggestion.
- **Suggested outcome.** Either route the SKIP through the bank's ledger when the bank runs it, or word the line as "not applicable" so it does not read as a declined proof.
- **Verification.** Rerun probe EQ through `test_builder.py`'s entry point. The bank verdict should name the arm, or the line should read as not applicable.

### S2 - SUGGESTION - Docs - `docs/testing/CI_WORKFLOWS.md:44-45`; `scripts/ci_scope.py:12-13,18-20,66-68` - general wording still implies the tap page is documentation only

- **Authority and evidence.** The lead definition at `CI_WORKFLOWS.md:44` reads "Documentation is a path that no gate the docs-only path skips reads without `docs-check` reading it too". The classifier docstring repeats it at `ci_scope.py:12-13` and `:18-20`, and the `DOCS_JOB_PY` rationale at `:66-68` ("left out because docs.yml's `docs-check` runs it ... every arm that reads a page included") rests on the same criterion.
  - Probe check D shows that the tap page meets that criterion: `docs-check` runs `test_tap_clock_docs` through the builder bank.
  - The page is nonetheless relevant.
- **Why this is a suggestion.** The operative parts all agree with `GATE_READ_DOCS`:
  - the enumeration at `:45-46`, "less the pages a gated module reads";
  - the explicit exception at `:64-66`, citing the #582 decision;
  - the table.
  - The frozen round-3 criterion is met.
  - Classification is conservative: RTL-relevant gates run on a docs-only edit of the page.
- **Suggested outcome.** Name the exception, or narrow the criterion to "a gated module outside `DOCS_JOB_PY`", in the lead sentence and the docstring. This could go with #495 at merge.
- **Verification.** A reader of `:44` alone reaches the classifier's answer for the tap page. `ci_scope.py --selftest` and the doc gates stay rc 0.

### Observation, not a finding

The default-clock control (`test_clock_contract.py:94`, `[]`) would equal the correct ROM if the contract clock ever equalled the generator's default of 100 MHz (`gen_gptp_ucode.py:2110`).
- That case is unreachable while the builder refuses any bare-metal clock other than `CPU_HZ = 50_000_000` (`recipe.py:5`, `endstation_builder.py:4296-4299`).
- If it were reached, it would fail loudly, not pass silently.

## Prior public review findings (read after my own pass)

Status at `aafcae59`. The delta touches only the three files listed above. Findings on other files keep their `77998f14` state, which R354-2 and R355-2 recorded.

| Prior item | Status at aafcae59 | Evidence |
|---|---|---|
| R354-2 F1 MINOR Docs (tap page both relevant and in the documentation-only table) | RESOLVED | Item 1; probe PASS; M29b is now detected on content; S2 records the residual lead-sentence wording as a suggestion |
| R354-2 SG1 (`--no-milan` help) | RESOLVED | Item 2; `receipts/cli_diff.txt` |
| R355-2 SG5 (same as R354-2 F1) | RESOLVED | as F1 |
| R355-2 SG6 (product argv without `--entity-gen-dir`; S9 survives) | RESOLVED | Item 3; E1 (S9) KILLED at head and SURVIVES at `77998f14` |
| R355-2 SG7 (ROM test fails when the clocks are equal) | RESOLVED | Item 4; EQ PASS with a named SKIP; the parent test fails; R1/R2 KILLED; S1 is a new suggestion about the SKIP's reporting |
| R355-2 SG8 (`sweep_extra.sh` launches without `--entity-gen-dir`) | RETAINED, out of scope; to #495 at merge per assignment | `sweep_extra.sh` is not in the delta |
| R355-1/-2 SG1 (literal mirror or `tb` import shadowing) | RETAINED, out of scope; to #495 at merge per assignment | not in the delta |
| R355-1/-2 SG2 (P1 precedence-loop mutant), SG3 (restatements, groups 4-5 to #495), SG4 (`sweep_extra.sh` argument order) | RETAINED as suggestions, unchanged | the files are not in the delta |
| R354-1 F1 BLOCKER, R355-1 F1 BLOCKER, manager bank r1 gate 6 | RESOLVED (R354-2, R355-2); still holds | `ci_scope.py --selftest` rc 0; hosted `changes`, `rtl-fast` and `full-ci-gate` succeed at this head |
| R354-1 F2 MINOR, R355-1 F3 MINOR (ROM clock binding) | RESOLVED; still holds | R1 and R2 KILLED at this head |
| R355-1 F2 MINOR (guard-narrowing mutants S1-S4, B3) | RESOLVED; still holds after the argv change | `scripts/mutants_round1_replay.sh`, `receipts/mutants_round1_replay.log`: S1-S4 and B3 KILLED, controls pass |
| R355-1 F4, F5 MINOR; R354-1 S1, S2 | RESOLVED (R354-2, R355-2); files outside the delta, or help-only in it | `receipts/cli_diff.txt` |
| R354-1 S3 groups 1-3 | RETAINED as informational | unchanged |
| R354-1 S3 groups 4-5 | Out of scope; to #495 at merge | - |

## Gates and probes run at the exact head

- **Focused tests:**
  - `test_clock_contract.py --soc` returned rc 0: 50 named refusals, 5 ROMs, sweep, tap and SoC checks (`receipts/head_test_clock_contract_soc.log`);
  - `test_pp_mem_bridge.py` returned rc 0 with 113/113. It imports and runs the changed SoC test (`receipts/head_test_pp_mem_bridge.log`).
- **Policy and documentation gates** (`receipts/doc_gates.log`), rc 0:
  - `docs_check.py`;
  - `check_doc_style.py` and `check_doc_paths.py`;
  - `ci_events.py --check` and `ci_scope.py --selftest`;
  - `check_solution_docs.py`;
  - `check_hygiene.py --check` and `check_py_idiom.py`;
  - `measure_fail_fast.py --check`, `measure_naming.py --check` and `measure_test_evidence.py --check`;
  - `check_baremetal_only.py --check` and `check_soc_sources.py`;
  - `DOC_MAP.gen.py --check`;
  - `git diff --check` over both `77998f14..aafcae59` and `9e9954e9..aafcae59`.
- **Renderer gates.** `check_em_dash.py` (twice) and `gen_toc.py --check` returned rc 2 on the first pass, because the pinned Markdown renderer is not installed on the host. All three returned rc 0 under a private, hash-pinned interpreter under `scratch/` (`receipts/doc_gates_renderer.log`):
  - em dash: 0 findings over 6 added lines (base `77998f14`) and over 54 added lines (base `9e9954e9`), 339/339 arms;
  - TOC: OK.
- **Mutation and fault probes.** The controls are listed in `receipts/mutants.log`, `mutants_round1_replay.log`, `m29_replay.log` and `mutant_logs_summary.txt`.
  - KILLED as expected: E1 (S9), R1, R2, EQ+R1, S1-S4 and B3.
  - The two parent-test controls match: E1 survives the `77998f14` test, and EQ fails it.
  - M29a survives, as informational. M29b is detected by my probe only.
  - Every unmutated control passes.
- **Hosted evidence, read-only** (`receipts/hosted_check_runs_head.tsv`, fetched `2026-09-27T20:13:29Z`):
  - `success` (15): `changes`, `rtl-fast`, `full-ci-gate`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `wire-accountability`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, and Verilator shards 0/5 and 3/5. `docs-check` runs the builder bank, which contains the changed ROM arm.
  - Still in progress: `elaborate`, and Verilator shards 1/5, 2/5 and 4/5.
  - Skipped: "Physical gPTP (nightly and manual)". That is not evidence either way.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 assignment 5859065834, items 1-4 and "Unchanged"; issue #582 acceptance 4. `CI_WORKFLOWS.md:56-78` against `ci_scope.py:54-59,73`. `milan_soc.py:3623-3625` against `:13-14,19,3946-3952`. `test_clock_contract.py:93-104,133`. Receipts `head_classification_probe.log`, `cli_diff.txt`, `mutants.log`, `identity.log` and `identity/*.sha256` | R354-3 | aafcae59732c0a12333b73d82d5cdcbcbf90c47f |
| RTL | CLEAN | No change under `hdl/`, `tb/`, `sw/firmware/` or `configs/`, and no gitlink change, base to head (`head_tree_and_gitlinks.txt`). The clock guard `milan_soc.py:3706` and builder guard `endstation_builder.py:4296-4299` are unchanged in the delta. The ROM clock input `endstation_builder.py:5699-5704` and `gen_gptp_ucode.py:2110` were checked against the test's byte comparison. 57/57 generated files identical (`identity_diff.txt` empty). SoC argparse surface identical except one help string (`cli_diff.txt`) | R354-3 | aafcae59732c0a12333b73d82d5cdcbcbf90c47f |
| Robustness | CLEAN (S1 is a suggestion) | Equal system and Milan clock shape (EQ, EQ+R1); `--entity-gen-dir` bypass (E1); dropped and system-fed ROM clock (R1, R2); `--no-milan`, `--full`, arty and spiflash exemptions (S1-S4); `flashboot` narrowing (B3); the `--no-milan` bare-metal refusal path `milan_soc.py:3946-3952`. Receipts `mutants.log`, `mutants_round1_replay.log`, `mutant_logs_summary.txt` | R354-3 | aafcae59732c0a12333b73d82d5cdcbcbf90c47f |
| Tests | CLEAN (S1 is a suggestion) | `test_clock_contract.py` (whole file, with changes at `:93-104,133`); `test_builder.py:370-402,27559-27566,27643-27651`; `test_pp_mem_bridge.py:947-951`. Receipts `head_test_clock_contract_soc.log`, `head_test_pp_mem_bridge.log`, `mutants.log` (E1 killed only by the head test; EQ fails only the parent test), `mutants_round1_replay.log` | R354-3 | aafcae59732c0a12333b73d82d5cdcbcbf90c47f |
| Docs | CLEAN (S2 is a suggestion) | `CI_WORKFLOWS.md:42-90`; `ci_scope.py:1-73`; `milan_soc.py:1-24,3623-3625`; `docs.yml:205`. Receipts `head_classification_probe.log`, `m29_replay.log`, `m29b_probe_failures.log`, `doc_gates.log`, `doc_gates_renderer.log`, `head_ci_scope_selftest.log` | R354-3 | aafcae59732c0a12333b73d82d5cdcbcbf90c47f |

- **Coverage basis.** R355-2 is POSITIVE at `77998f14`, with all five lenses clean. This round covers all five lenses again at `aafcae59`.
- **What the delta touched:**
  - Docs scope: `CI_WORKFLOWS.md`, and the `milan_soc.py` help;
  - Tests scope: `test_clock_contract.py`;
  - Conformance scope: all three files.
- So R355-2's coverage of those lenses is superseded here. This ledger's heads are the merge candidate's source head.

## Real limits

- **Not run, as assigned:**
  - the full builder bank (either compiler mode);
  - the parent, PP, gPTP, Yosys and native banks;
  - Docker/act, host `act_ci`, and hardware.
- **How the changed tests ran.** They ran on their own and through `test_clock_contract.py` and `test_pp_mem_bridge.py`. Their inclusion in the builder bank was checked statically at `test_builder.py:27559-27566`. The hosted `docs-check` success is the only execution of the bank at this head that I saw.
- **Scoped simulator not used.** The scoped path `$VALIDATION_STORAGE/tmp/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host, so its identity could not be verified. No RTL, bench or gitlink changed, so no simulator run was needed, and no substitute was used.
- **Interpreters.** LiteX-dependent tests used the host LiteX interpreter, which I used read-only. The renderer gates used a private hash-pinned interpreter under `scratch/`. Nothing was installed into a shared location.
- **Probe scope.**
  - The SoC probes stop at the PR's own pre-platform boundary (`assert_front_end_routed`). No full SoC elaboration or vendor flow was run.
  - Mutants are my own implementations of the published descriptions. They ran on disposable copies under `scratch/`, and the reviewed clone was never edited.
- **Public evidence.** The public evidence tree `e0c591ff/review-evidence/582-r1` holds round-1 author evidence at `3baff441` only. I found no public manager bank comment at `aafcae59` on the issue or the PR. The brief's statement that the manager's source static/builder and native banks passed at this head was not independently verified.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof, and no hardware or timing-closure claim is made.
- **Clone restore** (`receipts/restore_verification.txt`):
  - HEAD, tree and index tree are `aafcae59`/`0fe5f78b`;
  - the `ls-files -s` digest equals the `ls-tree -r HEAD` digest (mode, blob, path), and the worktree shows 0 diffs against the index and HEAD;
  - the four gitlinks are unchanged, and the three checked-out submodules are clean at their gitlinks;
  - `status --ignored` is empty after I removed the `__pycache__/` byproducts of my first test run.
- **Redaction.** Host paths in the receipts are redacted to `$HOME` and `$VALIDATION_STORAGE`.

## Pending manager duties

- **Hosted and local-replica acceptance at this head.** `elaborate` and Verilator shards 1/5, 2/5 and 4/5 were still running at my fetch.
- **The full builder bank in both compiler modes, and the native banks, at this head.** Publish their evidence if it is meant to be cited.
- **The final current-dev candidate build and validation.** Source base `9e9954e9`, live dev `6d5ebd73`.
- **Follow-ups for #495 at merge, per the assignment:**
  - R355-2 SG8;
  - R355-1/-2 SG1;
  - R354-1 S3 groups 4-5;
  - optionally S1 and S2 above.
- **Completion-ledger acceptance** against this round's heads.

R354-3 FINISHED
