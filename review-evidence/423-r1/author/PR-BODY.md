[A171]

## Status

Implementation ready for independent review: `423-retained-redundant-replay` -> `dev`.
Head `fed4f63f33e6185e5c7e4735a27234db99651d24`; tree `330afc6078441daf4d6a59d5dc760303a501477f`. Manager validation and reviews remain pending.

## Linked Issue / roles

Closes #423
Relates to #514

Executor: A171. Manager: A10. Cleared internal reviewer: R243 Codex. External reviewer: R244 Opus.

## Description

An exact replay containing one redundant merge previously fell through to STRANDED. The new final fallback proves the settled G1 shape, uses the existing distinct whitespace-exact historical replay helper, and requires raw current retention. A conflict-free three-way merge must reproduce the tip bytes exactly under the permitted file/mode conditions. Historical replay without retention reports UNKNOWN and names the unproved paths.

Existing arm order, linear historical semantics and exit codes remain unchanged. Shared Git transport preserves CRLF and undecodable bytes. The default containment self-test owns the 31 public fixtures, ten guard mutations and boundary controls. CONTRIBUTING documents the exact shape and limits.

## Authoritative references

REQ-VER-04; CONTRIBUTING section 2.1 step 7; [settled decision](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218).

## How to get into the same state

Use an isolated checkout at `fed4f63f33e6185e5c7e4735a27234db99651d24` with Git 2.39.0 or newer and the repository Python environment. The factual author packet supplies the immutable public inputs and reproduction scripts.

## How to validate

```sh
rtk proxy python3 scripts/check_merge_containment.py --selftest
rtk proxy python3 scripts/docs_check.py
rtk proxy python3 scripts/gen_toc.py --check
rtk proxy python3 scripts/check_py_idiom.py
rtk proxy python3 scripts/check_hygiene.py --check
rtk proxy python3 scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896
```

Expected: exit 0; containment self-test 326/326, including all 145 original assertions. Selected source/ratchet gates also pass; exact commands and receipts belong in the evidence comment. Manager owns the complete merge bar.

## Known limitations / out of scope

Actual gPTP processor PR62 and the published adjacent extension remain UNKNOWN/1. Arbitrary later semantic rewrites remain unresolved. Repeated-block coverage is bounded, without a general alignment proof. Existing linear historical policy is tracked separately in #514.

## Definition of Done

- [x] AC1-3 have local implementation evidence.
- [x] Changed behavior has self-checking tests under the existing owner.
- [x] Documentation reflects the exact proof and limits.
- [ ] Full required local/act/hosted verification bar passes.
- [ ] Factual self-test evidence is posted to the PR.
- [ ] Independent R243 and R244 reviews and final lens ledger are complete.
- [ ] Findings are fixed and re-reviewed; no round remains in flight.
- [ ] Current candidate merge is validated, merge authorized, post-merge containment clean.
