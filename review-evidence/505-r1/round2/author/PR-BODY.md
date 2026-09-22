[A159]

## Status

Draft revision complete on `407-carrier-script-pins` -> `dev`. Focused author validation passes. Manager validation and independent re-review remain pending; receipts belong in the accompanying REVIEW READY comment.

## Linked Issue / roles

Closes #407
Relates to #439

Executor: `[A159]` revision author; `[A155]` initial implementation.
Internal cleared-context reviewer: `[R219]` Codex.
External cleared-context reviewer: `[R220]` Opus.
Manager: `[A10]`.

## Description

A recognized carrier step could previously keep its name while replacing or swallowing its gate call. Every normalized `run` body in docs-check, wire-accountability, docs-check-no-git and elaborate now has a static canonical record. Refusals name the job, step and first differing line; missing records fail closed.

Regression arms derive from live bodies independently of those records. They exercise replacement, swallowing each normalized line, command/flag removal, appended commands, reordered distinct lines and continue-on-error. Existing specialized checks remain active. Whitespace reformats and deliberate matching record updates remain accepted.

The policy describes the content pins and maintenance cost consistently: update the canonical record explicitly in the same commit as a legitimate workflow edit; mutation arms follow the live body automatically.

## Authoritative references

- Issue #407 and [AC5 scope decision](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5770808527).
- [Accepted revision decision](https://github.com/kebag-logic/milan-fpga/pull/505#issuecomment-5771705480).
- REQUIREMENTS section 8; CONTRIBUTING sections 2, 3, 5 and 6; AGENTS sections 5-7.
- CI_WORKFLOWS items 1, 2, 4, 11 and 12.

## How to get into the same state

After the manager publishes the revision:

```sh
git fetch origin 407-carrier-script-pins
git switch 407-carrier-script-pins
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

## How to validate

```sh
python3 -B scripts/ci_events.py --check
python3 -B scripts/ci_events.py --selftest
python3 -B scripts/docs_check.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 -B scripts/check_py_idiom.py
python3 -B scripts/lint_rtl.py --check
git diff --check origin/dev...HEAD
```

Expected: every command exits zero. Accompanying evidence includes before/after full self-tests under M5b, prefix-only, order-insensitive, removed comparison and removed record enforcement, with exact commands and source variants. These mutants must fail the revised self-test while pristine checks remain green.

## Known limitations / out of scope

The seven RTL jobs' remaining content gap belongs to #439. No workflow behavior, normalization, RTL, firmware, VERSION or gitlink changes are included. Full native/hosted validation and the trusted act replica remain mandatory. The native AC5 analogue does not replace manager-owned act measurement.

## Definition of Done

- [ ] Linked Issue acceptance criteria validated at the final head
- [x] New regression coverage proves the reviewed comparison weaknesses detectable
- [ ] Complete required local verification bar passes
- [ ] Self-test evidence published in a PR comment
- [x] Authoritative policy reflects the implemented contract
- [ ] Internal cleared-context review is positive
- [ ] External cleared-context review is positive
- [ ] All findings re-reviewed and all five lenses covered clean
- [ ] No review round remains in flight
- [ ] Exact-head protected contexts and trusted replica pass
- [ ] Candidate merge result validated
- [ ] Post-merge containment checked before Issue moves to Done
