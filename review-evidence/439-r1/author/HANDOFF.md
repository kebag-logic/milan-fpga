# A181 source handoff for issue #439

Source implementation complete for manager integration and independent review. This is author evidence, not a review verdict or merge clearance.

- Repository: kebag-logic/milan-fpga
- Worktree: $CANDIDATE
- Branch: 439-rtl-script-content-pins
- Exact base and sole parent: `483a133ed08867ea0d300d2b4a027b5b48a4282f`
- Exact source head: `f01f237d4b48c7b1ed59c80aca51430901791624`
- Exact source tree: `ff1c54c52cbb196db754ce6999c661730a3d0e94`
- Subject: Pin remaining RTL workflow scripts and the gate SHA assertion
- Source clean and unpublished. Remote source branch still names the base; no source push, PR, merge, Docker/act, candidate act orchestrator/selftest, privilege, shared install, hardware action or other agent was used.
- Author: A181. Reserved independent reviewers: internal R254 Codex and external R255 Opus. Neither review is claimed here.

## Contract and public state

Read AGENTS.md, CONTRIBUTING.md, docs/README.md, REQ-VER-01/02/04, the full public issue, the scope decision, relevant CI_WORKFLOWS authorities, validator code and executable tests before editing. Public assignment confirms the branch was created with gh issue develop, Project In progress, and settled scope. Every shell invocation started with rtk.

- Scope decision: https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5772547851
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5782501927
- TAKEN, before first source edit: https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5782545395
- Full initial public issue and PR521 public diff: logs/public-issue.stdout and logs/public-pr521.stdout.

Only PR521's public diff was consulted to identify its non-RTL SDK edits. No #504 lane state was read, edited, merged, or cherry-picked. This source depends only on the stated dev483 base. Its changes have not been composed with #504.

## Changed artifacts and implementation facts

| Artifact | Change | Git mode |
|---|---|---|
| scripts/ci_events.py | Canonical run records for all seven RTL jobs and the sibling SHA-pin step; shared comparison wiring; live-derived controls and isolated record/maintenance tests | 100755 |
| docs/testing/CI_WORKFLOWS.md | Replace the remaining-gap statement with measured coverage, maintenance policy, diagnostic requirements and test scope | 100644 |

38 run scripts contain 208 normalized lines. Four shared literal RTL scripts avoid repetition. Existing ownership, aggregate, environment-writer, sv2v and OOC constants are reused where applicable. The runtime never constructs expected scripts from candidate workflows.

The comparator, normalization executable body, sequence/membership comparison, non-RTL carrier records, all specialized pins, workflow files, all budgets, product sources and processor pins are preserved. Non-content fields in all seven RTL sequence records compare equal to the base. Controls require the new comparison's job, step and first-differing-line reason. Missing-record controls call the actual sequence-to-content wiring without earlier specialized checkers, so an earlier refusal cannot satisfy them.

The normal `python3 scripts/ci_events.py --selftest` owns all new controls. Its default hosted owner remains `.github/workflows/docs.yml`, job `docs-check`, step `CI event and SHA contract gate`. `full-ci-gate` remains the independent second `--check` runner. There is no new runner, schedule, processor suite owner or budget.

## Measured validation

| Command or control | Actual result |
|---|---|
| Pristine python3 scripts/ci_events.py --check | exit 0; 1513 contract items |
| Pristine python3 scripts/ci_events.py --selftest | exit 0; 1513 items, 1150 arms |
| Initial explicit SHA controls | exit 1; both regressions escaped with findings=[]; 0/2 caught |
| Final python3 scripts/ci_events.py --check | exit 0; 1589 contract items |
| Final python3 scripts/ci_events.py --selftest | exit 0; 1589 items, 2135 arms |
| Corrected explicit SHA controls | exit 0; 2/2 caught, full-ci-gate step 2, normalized lines 4 and 6 |
| coverage_and_maintenance.py | exit 0; all 1051 existing mutations retain names, edits and required reasons; all 1150 original success-result lines remain |
| Added default self-test controls | 756 content mutations + 228 record/maintenance cases + 1 whole-scope whitespace case = 985 added arms |
| Per-line content controls | all 208 normalized lines have swallowing, deletion and replacement controls |
| Additional full-check record controls | 114 attributable missing/empty/stale refusals across 38 scripts |
| Full-check maintenance controls | RTL Install behave and sibling SHA-pin script-only edits refuse; matching records and scripts pass |

The 228 record cases are six per live script: missing, empty tuple, blank line tuple, wrong type, stale content, and matching maintenance. Sequence-only maintenance is measured for every script; separately specialized pins continue to apply in the full checker. Two full-check controls additionally prove maintenance for newly pinned bodies without changing any specialized authority.

All 756 new content mutations require the new content comparison's own exact reason. Existing #407 edits include append/reorder/flag controls where applicable. Deletion and replacement controls separately cover syntax and comment lines, where trailing `|| true` is not an executable swallowed call. The named SHA controls remove the complete checkout mismatch block and replace its `exit 1` with `true`.

| Deliberately weakened validator | Live findings | Default self-test exit | Total failures | New #439 failures |
|---|---|---|---|---|
| Remove shared content call | 0 | 1 | 1407 | 946 |
| Remove seven-job condition | 0 | 1 | 911 | 911 |
| Remove sibling SHA condition | 0 | 1 | 35 | 35 |
| Force content equality true | 0 | 1 | 1236 | 832 |
| Accept missing canonical record | 0 | 1 | 171 | 114 |

These are expected mutation refusals, not source gate failures. Mutants execute only ci_events in memory; they do not modify the source checkout. Exact mutated scripts and raw outputs are retained in mutants/ and logs/. Two initial mutation-helper invocations refused an ambiguous replacement target before loading any mutant; their original script, exact argv/exits and raw errors remain, and the corrected helper narrows to the specific comparator before retaining the same uniqueness assertion. They are not counted as detector evidence.

Focused gate results, all exit 0:

- docs_check.py: zero findings; 163 Markdown files, 827 scrubbed text files, 23/23 scrub and 4/4 routing arms.
- check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f: zero findings across 31 added lines in one Markdown page; 57/57 arms. Separate --selftest: 57 arms.
- gen_toc.py: --check 105 annotated pages plus 17 below threshold; --verify-anchors 144 links; --selftest 707/707.
- check_py_idiom.py: 210 modules, all hard refusals zero, existing ratchets pass. --selftest 54/54.
- measure_test_evidence.py --check: runner contract OK; ratchets pass at 75<=77, 10<=10, 0<=0, 3<=3. --selftest 101/101.
- measure_fail_fast.py --check: ratchets pass at 82<=84, 4<=4, 0<=0, two existing site waivers. --selftest 106/106.
- check_todo_ownership.py: zero owned/unowned markers, 28 near-misses over 756 files. --selftest 45/45.
- check_hygiene.py --check: 706 files, three complete populations, all findings zero.
- check_doc_style.py: 22 current documents pass.
- git diff --check: clean.

No ratchet was grown or tightened, exemption added, assertion dropped, or count substituted. The unsupported initial `check_py_idiom.py --check` invocation returned 2; the correct default invocation passed. Other inspection-command failures are preserved in original-command-failures.txt. The original baseline SHA failures remain intact in logs/baseline-sha-controls.*.

All test commands used the default `python3`. The runner records PYTHONDONTWRITEBYTECODE=1, VERILATOR_JOBS=8 and MAKEFLAGS=-j8. No more than eight gate processes were launched together. It did not run any full builder, parent/processor simulation or synthesis bank.

## Source integrity and evidence map

Default process ownership was uid 1000, gid 1000. Both changed files retain their original ownership, file kind and full POSIX mode. All 855 tracked parent entries are enumerated; 853 are byte-identical to the base. Every tracked blob/symlink is hashed directly on disk against HEAD, and each index record is compared by path, mode, oid and stage. Index flags and all tracked kinds/modes/ownership match the baseline.

Required registered submodule heads, pinned bytes, kinds, modes and index records are unchanged:

- protocol-processor: 424c688fa2205b934a7689a58f2aa766420f2326
- gptp-processor: c1b617435824929a790739ea8585c3fe1a328cc0
- third_party/verilog-axis: 48ff7a7e2ef782cf778d47910cf85835c64b1bce

The external gitlink is unchanged and uninitialized, outside the required population. Git object reads explicitly used GIT_NO_REPLACE_OBJECTS=1. Baseline and final integrity manifests report no problems.

- commands.jsonl: exact argv, cwd, environment overrides, start, duration and exit for each captured command.
- results.tsv: compact index into raw logs, including failures.
- logs/: unfiltered stdout and stderr, with original failures retained.
- baseline-integrity.json and final-integrity.json: every tracked byte/kind/mode/index and all required pin populations.
- source-inventory.json: exact base/head/tree, changed blobs, SHA256 values and preservation facts.
- source.patch: exact two-artifact diff against the stated base.
- content-coverage.json: all 38 script identities, normalized records, line and mutation counts.
- mutation-results.json: actual exit/failure totals and attributable #439 failures.
- sha_controls.py, coverage_and_maintenance.py, mutate_validator.py, integrity.py, run.py: reproducible evidence tools.
- base-ci_events.py and base-CI_WORKFLOWS.md: original tracked source artifacts, no private transcripts.
- add_records.py: one-time literal record edit tool, not checker runtime or a maintenance command.
- SHA256SUMS: complete evidence-file checksums, excluding itself.

## Remaining manager and independent review bar

Manager owns publication, the draft PR and later current-dev integration after #504 lands. Compose these shared-file changes semantically, validate the resulting current-dev candidate, and renew every applicable changed-artifact review. Source evidence is not candidate-merge evidence.

Manager owns the complete local builder/parent/processor/Yosys banks, trusted act from a clean live-dev validation worktree, required hosted contexts, R254/R255 independent reviews and the reviewer-owned lens ledger. No full local bar, hosted result, reviewer verdict, merge authorization, merge, post-merge containment or Issue closure is claimed. No source implementation blocker or new requirement conflict was found. Stop this source branch at the head named above.

Author REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5782749254
