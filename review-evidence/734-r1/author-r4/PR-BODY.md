[A613]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Round 2](#round-2)
- [Round 3](#round-3)
- [Round 4](#round-4)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Focused local gates pass at `59354ffe75697e17a16fd117d9ba853e104394bc`.
The two Round 4 commits remain local; publication is pending.
`734-merge-base-scope` -> `dev`.
Independent re-review and remote acceptance remain pending.
Merge follows 697c, then 696.

## Linked Issue / roles

Closes #734
Relates to #734

Executor: `[A613]`
Internal cleared-context reviewer: `[R632]`, re-review pending.
External reviewer: `[R633]`, re-review pending.

## Description

Scope selection uses the live base the job validates against.
Hosted jobs compare their synthetic merge to its first parent.
Replay composes the fetched live base with the PR head.
It compares the composed tree against that live base.
Both modes therefore classify the changes landing would make.
A lane restoring RTL after merging dev remains relevant.
Stale documentation branches still skip RTL work.
Candidate builder and full native banks validate composition before merge.

## Round 2

The live-base correction addresses R632-1-F1.
Real REV and REV+E histories preserve restored RTL relevance.
The corrected environment bindings and counts address R632-1-F2.
Historical B16 retains its two documentation paths.

## Round 3

The standalone runner now owns inline history fixtures.
Its explicit worktree supplies bounded source and workflow reads.
The documented non-writable flat install passes isolated Python.
A planted sibling import fails in an isolated child.

Fixture Git uses clean configuration, home directories and fixed identities/dates.
Hostile signing and Git-directory settings cannot change the fixture target.
Automatic maintenance is disabled for deterministic repository snapshots.
These changes address R633-2-F1 and R632-2-F1.

Replay uses the composed merge tree, addressing R632-2-F2.
Base-side renames into gate-read paths remain relevant.
Identical RTL edits already present on dev contribute no path.
Both controls require identical hosted/replay paths and verdicts.
Missing ancestry, ambiguous ancestry and merge conflicts fail scope.

R632-2-R1's failure wording is corrected.
R632-2-S1's history wiring is independently guarded by the runner.
All five linked configuration images remain byte-identical.

## Round 4

The CI runner contract step now runs both selftest forms.
It installs only the runner file into an empty temporary directory.
The mode is `0555`; isolated Python receives the explicit checkout.
The ordinary selftest also executes the entire isolated flat copy.
The child skips only that launcher to avoid recursion.

R632-3-F1 is addressed with the reviewer's unrelated sibling-import mutation.
It passed the previous CI command but fails both corrected invocation forms.
The removed-history-call and in-scope sibling-import mutations still fail.
CI-events controls pin the flat installation and reject weakened invocations.

R632-3-R1's stale fail-safe sentence in TESTING.md is corrected.
Empty deltas stay relevant; unresolved PR revisions or ancestry fail scope.
The prepared body has one closing keyword, addressing the duplicate residue.
Live-base scope, REV, REV+E, B16 and all five image bytes stay unchanged.

## Authoritative references

- Issue #734 and assignment comments 6151273761, 6151933918, 6152693618 and 6153494016.
- PR #735 reviews R632-3 (6153487534) and R633-3 (6153458432).
- [Verification requirements](REQUIREMENTS.md#8-verification-and-release-acceptance), REQ-VER-04.
- [Contribution rules](CONTRIBUTING.md).
- [CI workflow policy](docs/testing/CI_WORKFLOWS.md).

## How to get into the same state

Use CPython 3.12.3 and a writable disk-backed `scratch_root`.
Replay scope requires Git with `merge-tree --write-tree` support.

```sh
git switch 734-merge-base-scope
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m venv "$scratch_root/venv"
. "$scratch_root/venv/bin/activate"
export TMPDIR="$scratch_root"
export PYTHONDONTWRITEBYTECODE=1
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
python3 -m pip install PyYAML==6.0.3
```

## How to validate

```sh
python3 scripts/ci_scope.py --selftest
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/docs_check.py
python3 scripts/docs_check.py --selftest
python3 scripts/check_doc_paths.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_em_dash.py --base a0f39ad4
python3 scripts/check_em_dash.py --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/check_sh_idiom.py
python3 scripts/check_sh_idiom.py --selftest
python3 scripts/pp_srcs.py --check
python3 scripts/pp_srcs.py --selftest
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
```

Run both offline runner forms inside a disposable CI job.
For the flat installation, `candidate` names its read-only source tree.
`install_dir` is an otherwise empty writable directory in that job.

```sh
python3 scripts/act_ci.py --selftest
install -m 0555 "$candidate/scripts/act_ci.py" "$install_dir/act_ci.py"
python3 -I "$install_dir/act_ci.py" --selftest --worktree "$candidate"
```

Expected result: every command exits 0.
There are 197 scope assertions and 2860 CI-events arms.
The ordinary runner passes 566 assertions; the flat invocation passes 564.
The difference is the two launcher checks skipped to prevent recursion.
The scope histories kill 48 mutations across the three selectors.
Documentation also passes without Git metadata.
The Round 4 packet records 30 before/after scope rows,
all five image hashes, and each gate's planted controls.

## Known limitations / out of scope

- Current-head reviews, trusted full replay and hosted contexts remain pending.
- Current-dev candidate builder and native banks validate composition before merge.
- Parallel replay slots, firmware behavior and linked images are outside this change.
- Linked-image comparisons are desk measurements; no physical calibration ran.
- The optional hosted merge-shape assertion remains unchanged.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied, including remote validation
- [x] New or changed behavior has self-checking tests
- [x] Assignment's focused local gates pass
- [ ] Complete required merge verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive at the corrected head
- [ ] External review is positive at the corrected head
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment is checked before the Issue moves to Done
