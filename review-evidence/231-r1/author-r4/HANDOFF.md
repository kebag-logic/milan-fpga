[A341]

# Round 4 handoff: issue #231 / PR #572

Commit: `ae729bbfd90934f4d56d3b02f1ffc652496b414d`
Parent: `3a1477c528bdf71b7cecadf86383b7579c9197d6`
Branch: `231-pp-shadow-baseline`
Commit subject: `docs: describe baseline refusal coverage without fixed counts`

Origin was verified as `https://github.com/kebag-logic/milan-fpga.git`.
The worktree was clean at entry and after the commit.

## Assignment and review findings

The [round-four assignment](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5847557806)
authorizes a text-only correction of stale refusal and mutant counts.
Both [R332-4 F1](https://github.com/kebag-logic/milan-fpga/pull/572#issuecomment-5847547395)
and [R333-3 F1](https://github.com/kebag-logic/milan-fpga/pull/572#issuecomment-5847555580)
identify the same MINOR Docs finding.
The [takeover comment](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5847569885)
records scope, roles and the validation plan.

## Change

- `docs/findings/PP_SHADOW_BASELINE.md:282` describes inventory, geometry, binding,
  declaration, endpoint, pathname and CLI containment refusals.
- `docs/findings/PP_SHADOW_BASELINE.md:286` requires every maintained
  enforcement-removal mutant to fail, with the unchanged control passing.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:382` instructs readers to run the
  maintained mutants alongside the positive control.

The delta is two Markdown files, four insertions and three deletions.
No script, RTL, measurement, image, parameter, constraint or gitlink changed.
The corrected prose matches `syn/ooc/pp_baseline.py` and
`syn/ooc/pp_baseline_mutants.py`.
This addresses the requested correction; reviewers must determine closure.

## Validation at the committed head

Every command ran in the foreground, without a shell pipeline.
Every required gate returned rc 0.
Receipts retain each command's output; [gate-results.json](gate-results.json)
records the command and exit status.

| Command | rc | Receipt |
|---|---:|---|
| `python3 syn/ooc/pp_baseline.py --selftest` | 0 | [selftest.log](receipts/selftest.log) |
| `python3 syn/ooc/pp_baseline_mutants.py` | 0 | [mutants.log](receipts/mutants.log) |
| `python3 -B scripts/docs_check.py` | 0 | [docs-git.log](receipts/docs-git.log) |
| `env GIT_DIR=/dev/null python3 -B scripts/docs_check.py` | 0 | [docs-filesystem.log](receipts/docs-filesystem.log) |
| `python3 scripts/check_doc_style.py` | 0 | [doc-style.log](receipts/doc-style.log) |
| `python3 scripts/check_doc_paths.py` | 0 | [doc-paths.log](receipts/doc-paths.log) |
| `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | [em-dash.log](receipts/em-dash.log) |
| `python3 scripts/gen_toc.py --check` | 0 | [toc-check.log](receipts/toc-check.log) |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | [toc-anchors.log](receipts/toc-anchors.log) |
| `git diff --check` | 0 | [diff-check.log](receipts/diff-check.log) |
| `git diff --check 3a1477c528bdf71b7cecadf86383b7579c9197d6 HEAD` | 0 | [diff-check-round4.log](receipts/diff-check-round4.log) |

The self-test reports 40 inventory refusals and a restored positive control.
It also passes the original, parameter/template, endpoint and CLI checks.
The mutant campaign passes its pristine control and kills all 28 mutants.

Both documentation modes inspect 168 Markdown files and 894 text files,
with zero findings. The filesystem mode uses `GIT_DIR=/dev/null` to make
Git metadata unavailable to the gate without altering the worktree metadata.
It exercises the CI filesystem inventory path and skips only Git inventory parity.

The pinned Markdown dependencies were installed into `markdown-deps/` using:

```sh
python3 -m pip install --require-hashes --target "$EVIDENCE_DIR/markdown-deps" -r tools/markdown/requirements.txt
```

Here `EVIDENCE_DIR` denotes this output directory. The Markdown gates ran with
`PYTHONPATH="$EVIDENCE_DIR/markdown-deps"`.
The em-dash gate reports zero findings and 339/339 control arms.
The TOC check passes and all 177 existing cross-page anchors reproduce.
The cited-path gate resolves all 848 citations.
`check_py_idiom` is inapplicable because no script changed.

## Delivery and remaining work

[PR-BODY.md](PR-BODY.md) contains the complete current PR body fetched with
`gh pr view 572 --repo kebag-logic/milan-fpga --json body`, updated with
`[A341]`, this commit, current review status and a Round 4 section.
It preserves `Closes #231` and all earlier implementation and validation context.

This commit is local and unpushed. The live PR was not edited.
No merge, additional checkout or synthesis measurement was performed.
Independent re-review and final-head CI acceptance remain pending.
The manager retains publication, PR-body application, candidate validation
and merge responsibilities.

