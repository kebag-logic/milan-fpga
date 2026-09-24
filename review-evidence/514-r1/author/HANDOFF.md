[A246] Author handoff for #514

Implementation head: `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6`.
Tree: `9151db9e2286e15f1b9d46dcbeb95de87dae2e72`.
Base: `3d2f3e3131c9db5898e1db9dd3e2a35149843109`.
Branch: `514-containment-retention`; clean, two local commits, not pushed.

20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 Use permitted wording for containment proof claims
3f2fe73d11e269ad6357db23b829283c61b5a48a Separate optional linear retention from historical containment


## Scope and policy

The [decision](https://github.com/kebag-logic/milan-fpga/issues/514#issuecomment-5789750055) and [assignment](https://github.com/kebag-logic/milan-fpga/issues/514#issuecomment-5810682208) authorize preserving historical linear inclusion and adding a separate optional retention arm. The default verdicts and exits are preserved. The author supplies no independent approval or lens ledger.

`--current-retention` keeps the ordinary `contained` line and adds a distinct current-retention line. The added arm accepts only a nonempty source-only linear range with distinct exact replays (H), then applies the unchanged #423 raw-entry/no-op three-way criterion (T). `retained` is exit 0 only when every requested result succeeds. Unproved, unsupported or unmeasurable retention is `UNKNOWN`, exit 1. Intentional supersession never becomes retention evidence.

The optional arm is deliberately bounded: ancestry-only histories, squash-only equivalence, source-only merges and empty net deltas are not supported. The existing redundant-merge fallback is unchanged and remains available in the default check. Enabling the linear-only option can therefore produce `UNKNOWN` alongside an existing successful proof. Adjacent/overlapping legitimate extensions may also remain unresolved. These limits are stated in CONTRIBUTING and the command docstring.

Changed files: `scripts/check_merge_containment.py`, `scripts/merge_containment_replay.py`, the self-test owner and new `scripts/merge_containment_selftest_linear.py`; CONTRIBUTING 2.1 step 7, AGENTS completion wording, CI workflow documentation and the running-tests guide. No RTL, workflow configuration, pins, ratchets or existing expected verdicts changed. The two public reproduction reports and the #423 decision are archived under `public/issue-423.json`; #514 is under `public/issue-514.json`. Public R242 scripts and receipts were fetched at immutable commit `badb350c0892fd5a6c771f24943463c9b1440c24`.

## Reproduction receipts

These were measured before implementation, at the assigned base. Fixture 30 uses R242's published builder unchanged; both heads match its immutable JSON receipt exactly. `linear-patch-fallback` invokes the repository's existing builder with fixed commit dates. [Base receipts](logs/base-reproduction.json), [candidate receipts](logs/candidate-reproduction.json), [base self-test](logs/base-selftest.log).

### fixture30

Source: `9a9c1e7b26ff2d3439ef5c5ec439cc3a13c9a34a`.
Target: `219aa2256e055e8a577f9899ac6d36bd8bd986e0`.
Base checker: exit 0.

```text
contained  refs/heads/pr  [every commit has a whitespace-exact equivalent in refs/heads/main (2 not ancestors -- rebase merge)]
```

Candidate default: exit 0.

```text
contained  refs/heads/pr  [historical inclusion only: every commit has a whitespace-exact equivalent in refs/heads/main (2 not ancestors -- rebase merge)]
```

Candidate with `--current-retention`: exit 1.

```text
contained  refs/heads/pr  [historical inclusion only: every commit has a whitespace-exact equivalent in refs/heads/main (2 not ancestors -- rebase merge)]
  UNKNOWN    refs/heads/pr: current retention: unproved on: 'mod.txt'

1 tip(s) lack a requested proof; see UNKNOWN above.
  Unresolved history or current retention is not a pass.
```
### linear-patch-fallback

Source: `8c7f71d524a70c49ae12d4f9d38bfc6adf782077`.
Target: `206dc8a16726a10e15dfe9946a51777139402daa`.
Base checker: exit 0.

```text
contained  refs/heads/linear-feature  [every commit has a whitespace-exact equivalent in refs/heads/linear-base (1 not ancestors -- rebase merge)]
```

Candidate default: exit 0.

```text
contained  refs/heads/linear-feature  [historical inclusion only: every commit has a whitespace-exact equivalent in refs/heads/linear-base (1 not ancestors -- rebase merge)]
```

Candidate with `--current-retention`: exit 1.

```text
contained  refs/heads/linear-feature  [historical inclusion only: every commit has a whitespace-exact equivalent in refs/heads/linear-base (1 not ancestors -- rebase merge)]
  UNKNOWN    refs/heads/linear-feature: current retention: unproved on: 'linear'

1 tip(s) lack a requested proof; see UNKNOWN above.
  Unresolved history or current retention is not a pass.
```


Reproduction scripts: `reproduce_base.py <repository>` expects the assigned base checker; `reproduce_candidate.py <repository>` expects the implemented checker. They create and remove disposable fixture repositories. Do not run the base script against the candidate and relabel its result as baseline evidence. Full baseline self-test: 678 assertions, exit 0.

## Examples and mutation sensitivity

All rows traverse the shipped command. All content examples retain the default `contained/0`. The native and mutant receipts include exact fixture heads, command arguments, verdict text and exits in [linear-examples.json](logs/linear-examples.json); [assertion log](logs/linear-examples.log). Reproduce with `python3 record_examples.py <repository>`.

| Example | Optional result | Mutant result | Original oracle against mutant |
|---|---|---|---|
| Exact retention | `retained/0` | Not needed | Positive control |
| Exact reversion | `UNKNOWN/1` | T bypass: `retained/0` | Fails |
| Partial reversion | `UNKNOWN/1` | T bypass: `retained/0` | Fails |
| Legitimate non-overlapping extension | `retained/0` | Not needed | Positive control |
| Intentional supersession | `UNKNOWN/1` | T bypass: `retained/0` | Fails |
| Source executable-bit loss | `UNKNOWN/1` | T bypass: `retained/0` | Fails |
| Later mode change allowed by T | `retained/0` | Not needed | Positive control |
| Regular file becomes symlink | `UNKNOWN/1` | T bypass: `retained/0` | Fails |
| Exact symlink identity | `retained/0` | Not needed | Positive control |
| Symlink reversion | `UNKNOWN/1` | T bypass: `retained/0` | Fails |
| Exact gitlink identity | `retained/0` | Not needed | Positive control |
| Gitlink reversion | `UNKNOWN/1` | T bypass: `retained/0` | Fails |
| Binary change | `UNKNOWN/1`, raw merge unmeasurable | T bypass: `retained/0` | Fails |
| Retained deletion | `retained/0` | Not needed | Positive control |
| Reverted deletion | `UNKNOWN/1` | T bypass: `retained/0` | Fails |
| Failed object read | `UNKNOWN/1`, names cat-file failure | T bypass under the same injected read failure: `retained/0` | Fails |
| Ancestry-only history | `UNKNOWN/1`, unsupported | False success for missing H: `retained/0` | Fails |
| Merge-shaped source | `UNKNOWN/1`, unsupported | Removed zero-merges guard: `retained/0` | Fails |
| Squash-only endpoint | `UNKNOWN/1`, unsupported | H bypass: `retained/0` | Fails |

T-bypass mutation edits only the new arm's `missing = _retained_at_tip(source, target, git)` to `missing = []` in a disposable source copy. Existing #423 code and its mutation locations are unchanged. The unavailable-object case keeps the injected failure active while bypassing T in process. Assertions require both the original refusal and the mutant's changed exit/verdict; this is executable evidence that each negative example rejects the weakened implementation. Additional controls cover duplicated flags, self-test option exclusion, mixed targets, and merged-PR target dispatch. All 100 added assertions run under the default self-test.

Initial full implementation run found four positive fixtures with accidental empty later commits; the inherited H helper correctly treated those measurements as unknown. Fixture histories were corrected by adding unrelated later work; their expected positive results were not changed. [Initial result](logs/implementation-selftest.log). Initial docs checks rejected two added words; a separate wording-only commit corrected them. [Initial gate statuses](logs/initial-gates.json), [initial docs log](logs/initial-docs-check.log), [initial no-Git docs log](logs/initial-docs-check-no-git.log). Final evidence below supersedes those failures.

## Final gate table

Every row ran at `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6` and returned 0. Commands ran in the foreground, without pipelines. [Machine-readable gate table](logs/gates.json). Reproduce using `python3 run_gates.py <repository>`.

| Command | Exit | Receipt |
|---|---:|---|
| `python3 scripts/check_merge_containment.py --selftest` | 0 | [containment-selftest](logs/containment-selftest.log) |
| `python3 scripts/docs_check.py` | 0 | [docs-check](logs/docs-check.log) |
| `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | [docs-check-no-git](logs/docs-check-no-git.log) |
| `python3 scripts/check_em_dash.py --base 3d2f3e3131c9db5898e1db9dd3e2a35149843109` | 0 | [em-dash](logs/em-dash.log) |
| `python3 scripts/check_em_dash.py --selftest` | 0 | [em-dash-selftest](logs/em-dash-selftest.log) |
| `python3 scripts/check_doc_style.py` | 0 | [doc-style](logs/doc-style.log) |
| `python3 scripts/check_doc_style.py --selftest` | 0 | [doc-style-selftest](logs/doc-style-selftest.log) |
| `python3 scripts/gen_toc.py --check` | 0 | [toc](logs/toc.log) |
| `python3 scripts/gen_toc.py --selftest` | 0 | [toc-selftest](logs/toc-selftest.log) |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | [toc-anchors](logs/toc-anchors.log) |
| `python3 scripts/check_doc_paths.py` | 0 | [doc-paths](logs/doc-paths.log) |
| `python3 scripts/check_py_idiom.py` | 0 | [python-idiom](logs/python-idiom.log) |
| `python3 scripts/check_py_idiom.py --selftest` | 0 | [python-idiom-selftest](logs/python-idiom-selftest.log) |
| `git diff --check 3d2f3e3131c9db5898e1db9dd3e2a35149843109` | 0 | [diff-check](logs/diff-check.log) |
| `git diff --check` | 0 | [diff-check-worktree](logs/diff-check-worktree.log) |

Containment: 778/778 assertions, 678 existing plus 100 added; no locale `NOT RUN` notices. `merge_containment_selftest_content.py` has no separate entry point; its content cases run inside the required self-test. No standalone no-op invocation is claimed as validation.

The no-Git docs invocation forces Git discovery to fail using `GIT_DIR=/dev/null`, exercising the workflow's filesystem-inventory mode in this same checkout. Both inventories examined 165 Markdown files and 851 scrubbed text files with zero findings. Normal mode passed 23/23 scrub checks and 4/4 routing arms; no-Git mode passed 22/22 and 4/4, with its expected inventory-parity skip. Normal mode supplies that parity evidence. No Git metadata was removed and no second project checkout was used.

The em-dash gate found zero findings over 52 added Markdown lines. The Python idiom gate passed without changing budgets. [Final integrity](logs/final-integrity.json) records the clean checkout, exact head/tree and two one-line commits. [Patch](514.patch) is the complete reviewable base-to-head diff.

## Handoff and remaining workflow

Implementation portions of AC1, AC2, AC3 and AC5 are met; the decided historical policy remains intact. The assigned local gate subset of AC4 passes. Independent reviews and their five-lens ledger, complete remaining workflow gates, publication, candidate validation, authorized merge and post-merge containment remain with the manager. This handoff is not an approval or a claim that the Issue can close now.

The board/body still carried Backlog when read; the later decision and explicit assignment authorized implementation. That stale state and the manager-owned independent review assignment were noted publicly in [TAKEN](https://github.com/kebag-logic/milan-fpga/issues/514#issuecomment-5810713843). No project-state or PR change is claimed.

Per assignment: no push, PR creation/edit, merge, additional project checkout, hardware, delegated work or workflow replay. Public writes are the #514 takeover and final `[A246] REVIEW READY` evidence. `PR-BODY.md` is a proposal for later publication.
