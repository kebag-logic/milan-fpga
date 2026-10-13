[A613]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Local scope and contract gates pass at `0519ff3684258482a56892056edbfbb65c186f88`.
`734-merge-base-scope` -> `dev`. Independent reviews and remote validation pending.
Merge follows 697c, then 696.

## Linked Issue / roles

Relates to #734

Executor: `[A613]`
Internal cleared-context reviewer: pending assignment.
External reviewer: pending assignment.

## Description

A documentation PR forked before later base changes currently triggers RTL work.
All three selectors now compare the recorded base's merge base with the PR head.
The event's own head avoids counting changes in the hosted synthetic merge.
Validation jobs continue to build their original checkout.
Fast push comparisons retain their before-to-after behavior.

The replay event preserves both recorded revisions. Its new history control proves
that a stale-base documentation PR has the same file set locally and hosted.
Shipping scope bodies test documentation, RTL, gitlink and empty-diff cases.
Fifteen planted defects and six contract mutations prove the new assertions.
All five linked configuration images remain byte-identical.

## Authoritative references

- Issue #734 and assignment comment 6151273761.
- [Verification requirements](REQUIREMENTS.md#8-verification-and-release-acceptance), REQ-VER-04.
- [Contribution rules](CONTRIBUTING.md).
- [CI workflow policy](docs/testing/CI_WORKFLOWS.md).

## How to get into the same state

Use CPython 3.12.3 and a writable disk-backed `scratch_root`.

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
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_em_dash.py --base a0f39ad4
python3 scripts/check_em_dash.py --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/pp_srcs.py --check
python3 scripts/pp_srcs.py --selftest
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
```

Run the offline runner contract inside a disposable CI job:

```sh
python3 scripts/act_ci.py --selftest
```

Expected result: every command exits 0. Scope checks cover all three selectors;
the CI-events selftest passes 2834 arms, and the runner reports PASS.
The documentation gate also passes on an exported tree without Git metadata.
Self-test receipts and image hashes are retained for the review evidence comment.

## Known limitations / out of scope

- Reviews, a full PR workflow replay and hosted contexts remain pending.
- Current-dev candidate builder and native banks validate composition before merge.
- Parallel replay slots, firmware behavior and linked images are outside this change.
- Linked-image comparisons use measurement fixtures, not physical measurements.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied, including remote validation
- [x] New or changed behavior has self-checking tests
- [x] Assignment's focused local gates pass
- [ ] Complete required merge verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment is checked before the Issue moves to Done
