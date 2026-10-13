[A613]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Round 2](#round-2)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Focused local gates pass at `33ac35b54648ef919227c5dd8b9abc97fa6bedbd`.
`734-merge-base-scope` -> `dev`. The new commit is local and unpushed.
Independent re-review and remote acceptance remain pending.
Merge follows 697c, then 696.

## Linked Issue / roles

Relates to #734

Executor: `[A613]`
Internal cleared-context reviewer: `[R632]`, re-review pending.
External reviewer: `[R633]`, re-review pending.

## Description

Scope selection uses the live base the job validates against.
Hosted jobs compare their synthetic merge to its first parent.
Source-head replay compares the fetched live base's unique merge base to the PR head.
The recorded base oid remains metadata, so merging newer dev and restoring RTL
cannot hide the restored file behind a docs-only verdict.
Stale documentation branches still skip RTL work; push comparisons retain their
before-to-after behavior. Candidate builder and full native banks validate composition.

## Round 2

Addresses R632-1-F1 with live-base scope and real REV/REV+E histories.
Addresses R632-1-F2 by correcting the authoritative environment bindings and counts.
All three shipping selectors run against seven histories with 42 killing mutations.
The unchanged reviewer probe functions pass nine graded current-head cases;
historical B16 still lists exactly two documentation paths.
All five linked configuration images are byte-identical to the previous head.

## Authoritative references

- Issue #734, original assignment comment 6151273761 and Round 2 comment 6151933918.
- PR #735 reviews 6151873947 and 6151927790.
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
python3 scripts/check_doc_style.py
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

Expected result: every command exits 0; 180 scope assertions, 2846 CI-events
arms and 552 runner assertions pass. Documentation also passes without Git metadata.
The handoff carries each gate's controls, before/after scope tables and five image hashes.

## Known limitations / out of scope

- New-head reviews, full PR replay and hosted contexts remain pending.
- Current-dev candidate builder and native banks validate composition before merge.
- The optional suggestion to separately pin history-selftest wiring remains open.
- Parallel replay slots, firmware behavior and linked images are outside this change.
- Linked-image comparisons are desk measurements; no physical calibration ran.

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
