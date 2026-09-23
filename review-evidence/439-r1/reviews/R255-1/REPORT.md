[R255] POSITIVE - exact head f01f237d4b48c7b1ed59c80aca51430901791624

Round R255-1, external cleared-context review of issue #439 / PR #525.

- Head `f01f237d4b48c7b1ed59c80aca51430901791624`, tree `ff1c54c52cbb196db754ce6999c661730a3d0e94`.
- Sole parent and source base `483a133ed08867ea0d300d2b4a027b5b48a4282f`; live `dev` read back at review time was the same commit.
- Changed files: `scripts/ci_events.py` and `docs/testing/CI_WORKFLOWS.md` only. No workflow, HDL, gitlink, budget or normalizer change.
- Verdict, findings and ledger below were written from my own pass before I read any prior review report on this PR. The prior-findings section was added afterwards and is marked as such.
- Reproduction: exact commands are in `receipts/COMMANDS.txt`, the portable probe scripts in `scripts/`, and every published receipt is listed in `MANIFEST.sha256`.
- Probes ran at most eight parallel jobs and used only disposable copies. The clone was re-verified afterwards (`receipts/integrity_post_probes.txt`): 851 tracked entries, bytes and modes, a clean index with no hidden-flag entries, and the three required submodules clean at their gitlinks.

## Scope reconstructed

From the frozen issue body, the scope decision (issue comment 5772547851) and the source-lane decision (issue comment 5782501927), plus CI_WORKFLOWS items 4, 7, 11, 12 and "One authoritative SHA":

- Every recognized `run` step of the seven RTL jobs: `verilator-shards`, `verilator-suites`, `yosys-shards`, `yosys-portability` (rtl.yml) and `verilator-lint`, `bdd-conformance`, `yosys-elaboration` (rtl-fast.yml). That is 37 run steps.
- Plus `full-ci-gate` step 2, "Print the event and pin the one SHA this run validates". Total 38 scripts.
- Carrier form from #407: the record sits beside the step identity and uses item 11's comparison and item 7's normalization.
- Out of scope: step sequence and membership authority (#406), physical leg, fast selector and verdict, other gate steps (their specialized pins), workflow schedule, carriers, budgets, normalization semantics.

I took this population from the issue text, not from the checker. My scripts list the seven job ids and the SHA step name as literals.

## Findings

No BLOCKER, MAJOR or MINOR finding. Two SUGGESTIONs (optional, no effect on lens coverage).

### R255-S1 SUGGESTION - Robustness, Tests, Docs

- Location: `scripts/ci_events.py:7704-7706` (`_rtl_script_arms`), and `docs/testing/CI_WORKFLOWS.md:779-780` and `:793`.
- Evidence: the SHA-specific controls find the mismatch block with bare `lines.index(...)` on three literal lines. If the live SHA-pin body no longer holds `if [ "$head" != "$GITHUB_SHA" ]; then`, a later `fi` and a later `exit 1`, `--selftest` aborts with an unhandled `ValueError` traceback. It does not report a named problem.
  - Case A, legitimate maintenance. I respelt the `if` line as `"${GITHUB_SHA}"` in both the workflow and its record. `--check` exits 0 and `--selftest` exits 1 with the traceback. Receipts: `receipts/sha_assertion_maintenance_check.txt` and `receipts/sha_assertion_maintenance_selftest.txt`.
  - Case B, malformed pristine body. I put a U+00A0 in that line. `--check` exits 1 with the named refusal, but `--selftest` crashes before its own "pristine tree is not clean" report. Receipts: `receipts/malformed_pristine_check.txt` and `receipts/malformed_pristine_selftest.txt`.
  - Maintenance that leaves the three anchor lines alone does pass both modes. For example, adding a line to the SHA body and to its record gives `--check` OK and `--selftest` PASS with 2143 arms (`receipts/srcmaint_*.txt`).
- Impact: this fails closed, so it is never a false green. The diagnostic is poor, though. The page says matching script/record maintenance is "accepted" and names two edits (script and record). A rewrite of the assertion's anchor lines needs a third edit, to the self-test locator, and nothing names that edit.
- Suggested outcome, optional: turn a missing anchor into a named self-test problem, and say on the page that the SHA controls anchor on those lines.
- Verification: rerun cases A and B. The self-test should print a named problem instead of a traceback.

### R255-S2 SUGGESTION - Tests, Robustness

- Location: `scripts/ci_events.py:7675-7690` (`_rtl_script_edits`) with `:7598-7631` (`_carrier_script_edits`).
- Evidence: the self-test swallows exit status only in the `|| true` spelling. Its appended-command control is `echo appended`. I wrote a weakened checker copy whose comparison drops bare `true` lines (W8). Its default `--selftest` still passes 2135 arms (`receipts/probe_weakened_checker.tsv`). The real checker refuses a trailing `true` line in all 38 bodies, with the named first-line diagnostic (`receipts/probe_workflow_mutations.tsv`, lever `append-bare-true`).
- Impact: none at this head. Several pinned bodies have no `set -e`, for example both aggregate SHA verifiers. In those bodies a trailing `true` line swallows the gate's exit status just as `|| true` does. A future change to the comparator or the normalizer that ignored no-op lines would therefore pass the gate's own proof.
- Suggested outcome, optional: add an appended bare-`true` (or `exit 0`) control per body.
- Verification: the W8 weakened copy must fail `--selftest`.

## Acceptance criteria at this head

1. **Content pin on every scoped step. MET.**
   - All 38 records are literal tuples of `str`. At the same step position, each equals my own independent shell-style normalization of the live body: 38 scripts, 208 lines, 0 mismatches (`receipts/verify_records.txt`).
   - Shared constants (`RTL_FETCH_SCRIPT`, `RTL_VERILATOR_BUILD_SCRIPT`, `RTL_YOSYS_BUILD_SCRIPT`, `RTL_YOSYS_INSTALL_SCRIPT`) and the reused specialized constants are module-level literals. No module-level code reads a workflow file.
   - The record shape is the #407 carrier shape, compared by the same `check_carrier_script` (`scripts/ci_events.py:3738-3756`), which is now also called for these jobs (`:3816-3820`).
2. **A changed command is refused by name. MET.**
   - I edited the YAML text of each live body directly: 742 refusal probes across all 38 bodies. Every one exits 1 and prints `job <id> step <n> (<name>) script is not the canonical form: line <k> must be <expected>` at the correct first differing line (`receipts/probe_workflow_mutations.tsv`).
   - Per line, each body was swallowed, deleted and replaced by `true`. Per body, it was also given an appended command, an appended `true`, and a whole-body `true`.
   - The same 742 probes against the base checker: 518 left `--check` green. That includes 28 of the 31 SHA-step probes, among them block deletion and `exit 1` made `true`. The other three were refused by the older "print the event name" rule. The remaining 224 base probes, those three included, were refused only by older specialized pins (`receipts/probe_workflow_mutations_BASE.tsv`, `receipts/probe_base_vs_head_summary.txt`).
3. **The pin cannot pass vacuously. MET.**
   - Record faults under the full `--check`: 152 of 152 refused by name. That is 38 bodies times four faults: record removed, empty tuple, list instead of tuple, and stale line 1 (`receipts/probe_record_faults.tsv`).
   - The self-test holds 228 record arms: missing, empty, blank, wrong type, stale and maintained, through `check_sequence_pin_coverage`.
   - Vacuity stub: 1807 arms fail.
4. **Pristine green, arm count does not fall. MET.**
   - Base: 1513 items and 1150 arms. Head: 1589 items and 2135 arms. Both modes exit 0 (`receipts/base_*.txt`, `receipts/head_*.txt`).
   - Every base `ok` line is still present at head. The only changed line is the vacuity count, 1051 to 1807.
5. **SHA-pin controls, maintenance and policy text. MET.**
   - Four SHA-pin edits are each refused as the only finding, at step 2 line 4 or line 6: the mismatch block deleted, `exit 1` made `true`, `exit 1` made `exit 0`, and the condition inverted.
   - Every line is also swallowed, deleted and replaced.
   - Matching maintenance, script and record edited together, was run under the full `--check` for all 38 bodies (`receipts/probe_maintenance.tsv`). 26 are accepted outright. 12 are held only by their pre-existing specialized pins, as the page states. The content pin refuses 0.
   - The policy text is accurate; see the Docs line below. The anchor-line nuance is S1.

## Per-lens results

- [R255] PASS Conformance - issue #439 acceptance 1-5, comments 5772547851 and 5782501927; `docs/testing/CI_WORKFLOWS.md` items 4/7/11/12; `scripts/ci_events.py:2029-2356`, `:3738-3756`, `:3816-3820` - each criterion was checked with black-box probes against records audited as literals. The mapping is above.
- [R255] PASS RTL - diff 483a133..f01f237 (2 files; no HDL, gitlink or workflow bytes); `receipts/compare_step_lists.txt`; `receipts/lint_rtl_check_selftest.txt` - the recorded RTL-gate scripts equal what the workflows run; only the 38 `run` records were added; specialized constants and normalization are unchanged; the pinned lint gate passes at 90 of 90 with the verified scoped Verilator 5.050; the self-test costs 6.7 s more (`receipts/selftest_timing.txt`); all four gitlinks match the manager's native-bank integrity record.
- [R255] PASS Robustness - `receipts/probe_record_faults.tsv`, `receipts/malformed_pristine_*.txt`, `receipts/probe_maintenance.tsv`, `receipts/srcmaint_*.txt` - covers missing, empty, list-typed, blank, wrong-type and stale records; refused characters in a pinned body; single-line and 12-line bodies; shared constants maintained per job; guarded steps compared regardless of their `if`. Every case fails closed. Diagnostic quality is S1.
- [R255] PASS Tests - `receipts/probe_workflow_mutations*.tsv`, `receipts/probe_weakened_checker.tsv`, `receipts/head_selftest.txt` - the new arms can fail: 518 base escapes are now refused. Eight of ten weakened-checker copies fail the default self-test. W8 is S2. W10 is the documented trust boundary, answered by the literal audit. All 1150 original arms are kept, and the focused gates pass (`receipts/focused_gates.txt`).
- [R255] PASS Docs - `docs/testing/CI_WORKFLOWS.md:768-793`, `:927-931`, `:945-965`; code comments at `scripts/ci_events.py:1996, 2021, 2029-2030, 2302-2303, 3740, 3765` - each new statement was checked against the executed behavior above. The old "future work under #439" residue is gone. The "machine-checked" wording in "One authoritative SHA" is now true for the gate's refusal and for both workers' refusals, which escaped at base. The docs, em-dash (explicit base), contents and anchor gates pass. The maintenance wording nuance is S1.

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #439 body and decisions; CI_WORKFLOWS items 4/7/11/12 and One authoritative SHA; `ci_events.py` records and wiring; verify_records, probe_workflow_mutations (head and base), probe_record_faults, probe_maintenance | R255-1 | f01f237d4b48c7b1ed59c80aca51430901791624 |
| RTL | CLEAN | 2-file diff, no HDL, gitlink or workflow change; compare_step_lists; pinned lint gate under verified Verilator 5.050; gitlinks; self-test timing | R255-1 | f01f237d4b48c7b1ed59c80aca51430901791624 |
| Robustness | CLEAN (S1, S2 are SUGGESTION) | record faults x4 x38; malformed pristine; SHA anchor rewrite; matching maintenance x38; source-level maintenance with self-test | R255-1 | f01f237d4b48c7b1ed59c80aca51430901791624 |
| Tests | CLEAN (S1, S2 are SUGGESTION) | 780 black-box probes at head and base; 10 weakened-checker copies; self-test population diff base to head; focused gates | R255-1 | f01f237d4b48c7b1ed59c80aca51430901791624 |
| Docs | CLEAN (S1 is SUGGESTION) | CI_WORKFLOWS.md:768-793, 927-931, 945-965; changed code comments; docs, em-dash, contents and anchor gates | R255-1 | f01f237d4b48c7b1ed59c80aca51430901791624 |

## Evidence observations (read-only)

- **Manager source evidence** (tree ff790f6, `review-evidence/439-r1/source/manager`):
  - Five native groups exit 0: `run_all_suites.sh`, uncached `syn/yosys/run.sh`, processor suites, gPTP `make all`, behave.
  - 48 of 48 builder/static commands exit 0.
  - Integrity PASS on 851 files, with the same four gitlinks as this clone.
  - I did not re-execute these banks.
- **Hosted, exact head** (`receipts/hosted_check_runs.tsv`):
  - `rtl.yml` run 35782624367 and `rtl-fast.yml` run 35782624387 executed with SUCCESS: `full-ci-gate`, Verilator shards 0-4, Yosys shards 0-4, both aggregates, `changes`, `verilator-lint`, `bdd-conformance`, `yosys-elaboration` and `rtl-fast`.
  - `docs.yml` and `elaborate.yml` carriers: SUCCESS.
  - The physical gPTP leg was SKIPPED. That is a nightly/manual context and not hardware evidence.
  - Earlier runs 35782622600 and 35782622869 at the same head are cancelled or fail-closed failures. The later successful runs supersede them.
  - The manager owns hosted and local-replica acceptance.

## Prior public findings

I added this section after the verdict and ledger above were written. Sources: the R254-1 report (PR comment 5784203100), the manager summary (5784203694) and the scope decision's summary of PR #505 R220-2 F3. Each disposition rests on my own evidence at this head.

| Prior finding | Original severity / lenses | Disposition at f01f237d4b48c7b1ed59c80aca51430901791624 |
|---|---|---|
| Issue #439 gap: recognized RTL scripts and the sibling SHA step had no content pin (measured on PR #505 R220-2 F3) | frozen task defect | RESOLVED. At base, 518 of 742 probes, including 28 of 31 SHA-step probes, left `--check` green. At head all 742 are refused by name. |
| R219/R220 F1: the shape-gate paragraph said scripts were not pinned | MINOR / Docs | REMAINS RESOLVED. `CI_WORKFLOWS.md:1081-1085` states canonical-script records for the three shape gates. This diff does not touch it, and the docs gates pass. |
| R220 F2: only last-line swallowing was tested | MINOR / Tests, Conformance | REMAINS RESOLVED. `_carrier_script_edits` is unchanged. Carrier `or-true-line-N` arms are 117 at base and 117 at head. The new RTL arms add 170 more non-last-line swallow arms. My black-box probes swallowed all 208 lines, and every one was refused. |
| R220 F3: residue sentence omitted the sibling SHA gap | MINOR / Docs | RESOLVED. `CI_WORKFLOWS.md:768-772` now states that the SHA script is pinned, and both originally escaping edits are refused at step 2 lines 4 and 6. |
| Earlier append/reorder, coverage-list and maintenance suggestions | SUGGESTION / Tests or Docs | REMAIN ADOPTED. Carrier append (57) and reorder (40) arms are unchanged. The W4 prefix-compare and W5 order-insensitive weakenings are detected. |
| R220 / R254 malformed-pristine self-test traceback (carrier bodies, `scripts/ci_events.py:7606`, `:7643`) | SUGGESTION / Robustness | RETAINED as optional. It is the same class as my R255-S1. S1 is a new instance in `_rtl_script_arms` that a legitimate maintenance edit can also trigger. It fails closed and does not affect coverage. |

No prior finding is open at BLOCKER, MAJOR or MINOR. Reading the prior reports did not change my verdict or my ledger.

## Real limits

- I ran no full parent, processor, gPTP, Yosys or builder bank, no local workflow replica, and no hardware step. For those I rely on the manager's public evidence and name it as such.
- Physical calibration was NOT RUN. The physical gPTP hosted skip is not hardware proof.
- **Trust boundary.** A checker that built its records from the on-disk workflows at import would pass its own self-test and pass a candidate with the mismatch block deleted (W10, `receipts/probe_weakened_checker.tsv`). Only a review of the literals catches that. At this head all 38 records are literals, but any later record edit needs the same audit.
- My workflow probes rewrite one `run` scalar at a time as a literal block. They do not probe YAML anchors or aliases, duplicate keys, or differences between the local YAML parser and the hosted runner's parser.
- **PR #521 composition.** PR #521 is currently open at `3d90958f`. Its diff for the two shared files applies textually onto this head in a dry run (`receipts/compose_521_dryrun.txt`). That is informational only. It is not a candidate, and it does not validate the composition.

## Pending manager duties

- After #504 / PR #521 lands, build the current-dev candidate. Both PRs edit `scripts/ci_events.py` and `docs/testing/CI_WORKFLOWS.md`, so the composition needs fresh review of the affected artifacts in all five lenses, plus the full local bar, the trusted local replica and the exact-head hosted required contexts on the final head.
- Merge needs the internal positive plus this external positive at the merge head. If the merge head differs, re-cover any lens whose scope changed.
- Merge also needs maintainer authorization, no review round in flight, then post-merge containment and closing the issue as Done.

R255-1 FINISHED
