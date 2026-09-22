[R219] POSITIVE - exact head ad62493186576144f9fa1568babad012bc9ad8ca

Cold independent internal review R219-2 of PR505 / issue407, against base b17580b91deb11f3441dfc5d7f9fafe539d929b8. All five lenses applied at this head. F1 and F2 are resolved under their original lens assignments; no open MINOR, MAJOR or BLOCKER remains from this review. This is a code-review verdict, not a merge-ready declaration. The separate execution and merge bar remains outstanding as recorded in public comment 5772174202.

The review was reconstructed from repository authorities, the public issue and decisions, the two commits and their diff, executable tests, public first-round reports, and the immutable evidence archive at b7380181b8a87edbf965e2ba99fd48b69f65a912. No private author/manager material, other reviewer's files, or reviewer collaboration was used. Public reports 5771593926 and 5771705156 were read as the findings to resolve, not adopted as independent measurements.

Prior findings and accepted suggestions:

| Prior item | Disposition at the reviewed head | Evidence |
|---|---|---|
| R219 F1 / R220 F1, MINOR Docs | Resolved. The actual shape-gate paragraph now states name, position and canonical-script pins, first-differing-line refusals, and the matching-record remedy. | docs/testing/CI_WORKFLOWS.md:1051; scripts/ci_events.py:1065; receipts/line-swallowing.json includes the three shape gates; documentation CLI logs. |
| R220 F2, MINOR Tests and Conformance | Resolved under both lenses. Every non-last normalized line receives its own swallowing arm, including all bounded ratchet checks and the exact AC5 first line. M5b now makes the full self-test fail by the required named line. | scripts/ci_events.py:7430 and :7466; receipts/check-calls.json, line-swallowing.json, M5b-selftest.log. |
| Append/reorder sensitivity suggestion | Addressed. Appending is tested on all 56 bodies; swapping adjacent distinct lines is tested on all 40 multi-line bodies. | scripts/ci_events.py:7447; receipts/prefix-selftest.log and unordered-selftest.log. |
| Coverage list, RTL-table comments and maintenance wording suggestions | Addressed. The policy describes the current population without the stale ten-script limit; comments distinguish RTL sequence/shape pins from carrier script pins; canonical edits are explicit and mutation derivation automatic. | docs/testing/CI_WORKFLOWS.md:643, :653, :895; scripts/ci_events.py:865, :1981, :2016. |

[R219] PASS Conformance - issue407 AC1-5 and decision 5770808527; scripts/ci_events.py:870, :3574, :3651, :7421; receipts/inventory.json and check-calls.json - The required population, diagnostics and corrected acceptance behavior are supported

Independent enumeration of the actual YAML, using literal carrier IDs and a separate implementation of the documented normalization, found 56 bodies: docs-check 41, wire-accountability 2, docs-check-no-git 1, elaborate 12. Every canonical tuple equals its live normalized body. Each of the 173 lines was independently altered with trailing `|| true`; the full checker refused each by job, step number/name and exact first differing line. Each edit and expected reason also matches a generated self-test arm.

All 14 live `--check` calls are covered. In particular, docs-check steps 26, 28, 30 and 31 cover the first-line bounded naming, fail-fast, test-evidence and hygiene checks. Step 34 covers the first-line `python3 scripts/check_py_idiom.py`, not only its subsequent self-test. The reference build, Python gates, bounded ratchets and builder gates all participate. Flag removal remains limited to bodies containing an actual proof/check flag: neither the no-git body nor the docs builder call acquires a fabricated flag requirement.

| Acceptance | Assessment and independently inspected evidence |
|---|---|
| AC1 | Met: 56 static canonical bodies, complete named line refusals, missing records refused. scripts/ci_events.py:3574; receipts/inventory.json and line-swallowing.json. |
| AC2 | Met: replacement 56, swallowing 173, command removal 40, flag removal 35, continue-on-error 56; additionally append 56 and reorder 40. The 173 swallowing arms include 117 non-last lines. receipts/mutation-population.json and M5b-selftest.log. |
| AC3 | Independently passed: actual CLI `--check` over 1,505 items and `--selftest` with 1,144 arms. receipts/pristine-check.log and pristine-selftest.log. |
| AC4 | Met: items 11/12 close the carrier residue, preserve the seven-RTL-job residue, and describe the explicit canonical update with automatically derived mutations. Required docs/TOC/path commands exit 0. The corrected shape-gate paragraph resolves F1. |
| AC5 | Historical measured behavior retained with the scope justification below. Independently reproduced the new-head native refusal for the exact first-line edit; no new act run is claimed. |

No unresolved acceptance conflict remains. The preimplementation decision explicitly replaces the contradictory whole-job-green wording: the tampered step succeeds, both contract steps reject it, docs-check fails, and both aggregates fail closed. The accepted revision covers both previously stated readings of AC2. AC4's maintenance remedy is implemented with automatic mutation derivation rather than a manually maintained mutation table. Neither acceptance nor the comparison has been weakened.

[R219] PASS Robustness - scripts/ci_events.py:3026, :3574, :3630, :7430; independent_probes.py; receipts/line-swallowing.json, positive-controls.log and maintenance-matching-selftest.log - Malformed inputs fail closed and legitimate maintenance remains possible

Across all 56 bodies, independent probes rejected empty/no-op/appended/commented scripts and non-string run values, six invalid canonical-record forms, and NBSP, U+2028, CR and NUL insertions. The retained 56 missing-record controls pass. All 456 carrier mutation arms produce their specific expected reasons; an unrelated specialized refusal cannot satisfy those reasons. These are checker-input probes, not claims that every mutated shell body was executed.

Whitespace positives pass for every carrier body. An actual CLI fixture with an appended idiom-step command fails at line 3 until its static record is updated; the matching pair passes both `--check` and the complete `--selftest`, now with 1,145 automatically derived arms. All fixture edits were in disposable scratch or memory. The existing normalization, including its documented whitespace equivalence, is unchanged; this review does not invent a stricter shell-equivalence contract.

[R219] PASS Tests - scripts/ci_events.py:7430, :7466, :7525, :7531, :7820, :7978; receipts/cli-results.json and mutation-population.json - Runnable controls detect their named defects and preserve earlier controls

Actual source mutants changed only the targeted comparison or missing-record diagnostic inside `check_carrier_script`, outside the checkout. Every mutant's pristine `--check` still exited 0, so the following failures come from sensitivity controls rather than a broken pristine fixture:

| Source mutation | Full self-test result at this head |
|---|---|
| M5b: ignore trailing `|| true` on non-last lines | Exit 1; 117 failures, including `carrier-script-407 docs-check step 34 or-true-line-1`, whose expected reason names Python idiom gate line 1. |
| Accept canonical prefix with appended commands | Exit 1; 56 failures. |
| Compare lines without order | Exit 1; 40 failures. |
| Remove body comparison | Exit 1; 400 failures. |
| Remove missing-record enforcement | Exit 1; 56 failures. |

The old source with M5b and its old policy passes the full 931-arm self-test; the new M5b checker accepts the AC5 mutation while the real new checker refuses it. These independently reproduce the old blind spot and demonstrate that the revised self-test detects it. The base checker also accepts that same workflow edit, confirming the new production refusal's relevance.

All 833 prior workflow mutation identities, expected reasons and resulting mutated worlds are identical at this head. All 590 base specialized arms still produce their expected reasons with `check_carrier_script` disabled. The new population is 1,046 workflow mutations, including 456 carrier arms; the stub-vacuity stage fails all 1,046. The 1,144 total also includes separate negative and positive stages, so vacuity is not claimed for all 1,144. Existing non-mutation stages and their wiring are preserved by source comparison.

[R219] PASS RTL - receipts/base-head.diff and source-preservation.json; .github/workflows/docs.yml, elaborate.yml, rtl.yml and rtl-fast.yml; docs/overview/ARCHITECTURE.md:98 - Gate architecture and product interfaces are preserved

Only scripts/ci_events.py and docs/testing/CI_WORKFLOWS.md differ from base. No RTL, firmware, build input, workflow blob or gitlink changes. All four workflow blob IDs match base and the first-round head. Against the first-round source, only `_carrier_script_edits` and `_carrier_script_arms` change executable AST; the other 331 top-level function/class definitions, all top-level assignments/imports, and the canonical records remain equal. Production comparison, record enforcement, normalization, specialized checks, aggregate rules and CLI dispatch are unchanged. The new content check remains restricted to the two carrier workflow files; the seven RTL jobs' remaining script-content scope stays with #439. No RTL sweep was run or inferred from this structural review.

[R219] PASS Docs - docs/testing/CI_WORKFLOWS.md:635, :768, :895, :1051; scripts/ci_events.py:865, :1981, :2016; receipts/docs-check.log, toc-check.log, doc-paths.log and em-dash.log - The corrected policy consistently describes the implemented pins and maintenance obligations

All remaining #407 references were checked against the current code. The stale shape-gate declaration is gone, and the coverage and whitespace descriptions match the executable population. Independently run commands exit 0: `python3 -B scripts/docs_check.py`, `python3 -B scripts/gen_toc.py --check`, `python3 -B scripts/check_doc_paths.py`, and `python3 -B scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8`. The path checker reports 824 resolved cited paths with one allowlisted path; these semantic text checks accompany, rather than substitute for, inspection of F1's paragraph.

Historical AC5 evidence and its limits:

The [manager's published measurement](https://github.com/kebag-logic/milan-fpga/pull/505#issuecomment-5771305219) is at normal head 6af65a151663e1301f1983a6c9d22650a0b35da9 and scratch head 66ba210630ff7f412e5706427b3ea976ebee3ba2. GitHub's scratch-commit record independently confirms its sole parent and one-line docs.yml change. Downloaded archive blobs were verified against their Git object IDs, and 59 available published-manifest hashes were verified. The supplied receipt verifier was inspected and rerun successfully; raw step/job context was also read.

| Raw public artifact | Observation attributed to A10 |
|---|---|
| ac5-act/01.log:1762, :1837 | The altered Python idiom step runs and succeeds. |
| ac5-act/01.log:1902, :1904, :1909 | Named docs-check / Python idiom / line 1 refusal; the contract step and docs-check job fail. |
| ac5-act/02.log:37, :39, :44 | Independent full-ci-gate emits the same refusal; step and job fail. |
| ac5-act/02.log:85, :88, :95, :100, :105 | Verilator aggregate executes; zero of five shard directories, absent tally evidence and skipped workers cause mandatory failures and a failed job. |
| ac5-act/02.log:146, :149, :157, :162, :167 | Yosys aggregate executes; zero of four directories, absent inventory evidence and skipped workers cause mandatory failures and a failed job. |
| ac5-act/results.json; act-draft-fast/01.log:3700 | Both scratch invocations exit 1 as workflow failures; the old normal docs run passes. |

Retaining this historical measurement for AC5 is justified. The actual `--check` execution functions, constants/canonical records, Python idiom gate implementation, workflow scripts, job conditions, needs and aggregate bodies are unchanged. The whole ci_events.py and policy files are not byte-identical: this revision changes mutation-generation code and documentation. The changed self-test path is not reached by the scratch docs contract step after its first `--check` command fails; the second runner invokes `--check` only. Checking the old and new policy with the current checker yields the same clean result, and the actual new-head CLI reproduces the exact AC5 rejection. The manager's new-head Python-idiom scan additionally reports success on the changed source population. This supports retaining the old behavioral measurement at its recorded head; it does not convert it into an exact-newhead act run or replace any required new-head execution gate.

The scratch idiom scan reports no live policy finding: the evidence demonstrates the successful tampered step required by AC5, not a planted defect being swallowed. The optional author fixture was not executed and is not counted. Artifact-download transport errors precede the aggregates' explicit mandatory refusals; those later checks demonstrably run. The SHA-verifier findings concern missing shard evidence, not a demonstrated disagreement between source SHAs. These distinctions require no stronger acceptance criterion.

Reviewer-owned completion ledger; all entries are newly applied at the current head, with no prior-head coverage merely carried forward:

| Lens | Covering round / state | Head |
|---|---|---|
| Conformance | R219-2 CLEAN | ad62493186576144f9fa1568babad012bc9ad8ca |
| RTL | R219-2 CLEAN | ad62493186576144f9fa1568babad012bc9ad8ca |
| Robustness | R219-2 CLEAN | ad62493186576144f9fa1568babad012bc9ad8ca |
| Tests | R219-2 CLEAN | ad62493186576144f9fa1568babad012bc9ad8ca |
| Docs | R219-2 CLEAN | ad62493186576144f9fa1568babad012bc9ad8ca |

Evidence limits and remaining lane obligations:

- The archive's round2/manager-builder/results.json records 40 commands exiting 0 at this head. Commands and corresponding receipts were inspected, not rerun wholesale. Builder log 40 explicitly excludes one unrun gate-11 calibration arm because its real placement report is absent; exit 0 is not coverage of that arm.
- The captured GitHub check-run records confirm successful exact-head rtl-fast, docs-check, wire-accountability, docs-check-no-git and elaborate contexts. The draft's verilator-suites and yosys-portability are **skipped**, not exhaustive passes. No hosted polling or waiting was used.
- The exhaustive native checks and trusted draft act replica remain outside this review's completed evidence, as openly recorded in [comment 5772174202](https://github.com/kebag-logic/milan-fpga/pull/505#issuecomment-5772174202). The complete local bar, ready-head replication/hosted exhaustive evidence, candidate validation, independent external review and post-merge containment remain required. Old/cancelled runs are not new-head passes. This report does not authorize merging or marking the lane complete.
- This isolated review checkout began and ends with all four submodules uninitialized: external, gptp-processor, protocol-processor and third_party/verilog-axis. Their gitlinks are unchanged, but their checkout bytes were not available to verify. The independent standalone Python idiom scan exited 2 with the expected missing-processor-population refusal, not PASS; receipts/python-idiom.log preserves it. Manager log round2/manager-builder/11.log supplies separately attributed new-head evidence.
- No Docker/act execution, privileged operation, hardware access, dependency installation, compilation, full parent RTL sweep, unrelated regression, product fix, commit, push, public write, merge or subagent was performed. All executable source mutations were disposable; tracked product bytes were never edited.

Final integrity: receipts/final-integrity.json verifies exact HEAD and tree 6b279253aa7d3edd6d9b5e9adc1ed9caf6f13d75, all 850 parent tracked blobs against committed raw bytes and file modes, all 854 index entries against HEAD, clean status and diff-check, and unchanged uninitialized submodule state. Reproduction commands and factual receipt descriptions are in README.md; no private reasoning is published.

R219-2 FINISHED
