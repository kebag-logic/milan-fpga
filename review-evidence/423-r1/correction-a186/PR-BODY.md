[A171 / A10 / A186] Prove bounded replay of one redundant merge while refusing unproved current retention. Git filenames and patches reach Git again as their original bytes, in the existing touched-path and patch arms and in the new fallback, under any filesystem encoding.

Closes #423

## Description

The final fallback requires the settled exact two-parent shape, distinct whitespace-exact replay commits with matching postimages, and current raw entry retention or an exact no-op three-way blob merge. Missing work, resolution changes and unproved later reversions remain nonzero. The existing linear historical policy stays with #514; actual gPTP processor PR62 remains UNKNOWN. No PP (protocol processor) or gPTP processor pin changes.

`scripts/merge_containment_git.py` is the shared Git transport. Filenames Git lists and patch text travel as bytes to the next Git command, never through Python's filesystem codec. Other Git output is decoded, and output that does not re-encode to identical bytes (Big5 turns `a1 fe` into `a2 41`) counts as a failed command, so it can only become UNKNOWN or a refusal. Diagnostics quote filenames as ASCII byte literals in every locale; the STRANDED `paths differing:` note now quotes names the same way as the fallback's UNKNOWN note.

The default self-test owns the controls: an in-process Big5 filesystem codec on every host; fresh UTF-8-mode, ASCII, strict UTF-8, Latin-1 and Big5 processes (installed or disposable locale data, otherwise `NOT RUN`, which is not evidence); a three-target report through a real stdout; and real-history controls for rename unfolding, hostile `diff.renames`/`diff.ignoreSubmodules`, the single merge base, the ancestor type rule and replay distinctness.

## How to reproduce

```sh
python3 scripts/check_merge_containment.py --selftest
LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 python3 scripts/check_merge_containment.py --selftest
```

## Validation

Author-local only, at `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34` (tree `ab96af335f1428770a1a96c0345a9f55278ad25b`, descends from dev `483a133e`): default self-test 678/678 under default, UTF-8-mode, strict UTF-8, ASCII, Latin-1 and Big5 parents; docs, em-dash, TOC, doc-style, doc-path, Python idiom, hygiene and ratchet gates exit 0. Removing the byte transport, the output guard, the ASCII labels, the byte source copies or any of the five retention guards fails the self-test, including on a host without `localedef`. Evidence and receipts: [#423 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/423).

[R244-1](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5789494311) was NEGATIVE at `4671e582`; its findings and every lens need re-review at the new head. The complete local bar, trusted replica, hosted checks and current-candidate validation have not run at this head.

## Definition of Done

- [ ] Complete local source validation and integrity at the corrected head
- [ ] Trusted replica and new exact-head hosted checks
- [ ] Two independent positives and clean reviewer-owned lens ledger
- [ ] Current candidate validation, authorized merge and containment
- [ ] Post-merge hosted results and Closed/Done
