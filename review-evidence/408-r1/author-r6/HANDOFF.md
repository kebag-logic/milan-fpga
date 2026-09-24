[A276] PR #535, correction round 6

Head: `062e89ad098806ae5def8341fcb8c2815583ca00`
Parent: `991d59653ff82ccf73ef4df9477de1df8c8c5964`
Source base: `759da623072358afdb0e9d570a7b4b6a788492c9`
Branch: `408-409-boot-gate-retire`
Worktree: `$LANES/408-409-boot-gate-retire`
Commit subject: `Scope closure evidence and cover the block-comment opener`

The commit has a one-line subject, no body and no trailers. It is local and awaits manager publication. The full replacement PR body is [PR-BODY.md](PR-BODY.md).

Assignment: [#408 round 6](https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5820090472).
Reviews read: [R273-7](https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5818979463) and [R272-6](https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5820082965). Their archived REPORT.md files were fetched at `c43534ea28880af8abce6f29653cff5eaf23d0d7` and `2b05a4549bb54264a78335b7780c17d2d0c6d4f8`; each matches the corresponding public comment's report text.

## Changes

| Finding | Disposition |
|---|---|
| R273-7 F1, MINOR, Docs | Scoped the gate-call comment: allowlist refusal is position-independent; agreement is measured at 23 table positions and bounded by the two lexer corpora elsewhere |
| R273-7 S1 | Named null-directive refusal in the page and cost row, including positions outside the closure table |
| R272-6 S1 | Added one fixed `/*/` corpus spelling, recorded as keeping `a` and `z` on the pinned compiler |
| R272-6 S2 | Distinguished the directive-line continuation position from the eleven comment/literal positions and two file-end positions |
| R272-6 S3 | Added `8e12d31f` to both dollar-identifier finding references and `a13b6e2e` to the form-feed reference |

Only `sw/builder/test_builder.py` and `docs/integration/BAREMETAL_FIRMWARE.md` changed. [scope-check.json](scope-check.json) proves that removing the added corpus row makes the syntax tree identical to the parent. The mutation table, accepted edits, lexical rules and closure table remain unchanged. The current documentation tally is 1846 spellings, 79 fixed plus 1767 generated.

## Regression evidence

[corpus-control.log](corpus-control.log) records an independent single-file `-std=gnu99 -E` measurement of the added spelling on the verified pinned SDK: return code 0, keeping exactly `a` and `z`.

[corpus-control.py](corpus-control.py) changes only the in-memory closer-search offset from `i + 2` to `i + 1`. In each compiler mode, gate 1b then stops at the new row because the readers keep `a`, `b`, `z`. Both refusals name the corpus case and the lexer disagreement pin. This control returned 0 after verifying the expected refusals; no worktree source was mutated.

## Required gates

| Check | Exit | Result | Receipt |
|---|---|---|---|
| Full builder, verified SDK mapped, `--require-rv32` | 0 | 280/280 mutations; 29/29 + 4/4 accepted edits; 1846/1846 spellings; 6440/6440 cells; 1 named NOT RUN | [full-builder-sdk.log](full-builder-sdk.log) |
| Full builder, cross compilers hidden | 0 | 222/222 mutations; 29/29 + 4/4 accepted edits; 1846/1846 spellings; 6440/6440 cells; 0 firmware compiles; 2 named NOT RUN | [full-builder-absent.log](full-builder-absent.log) |
| `python3 -B scripts/docs_check.py`, repository mode | 0 | 0 findings | [docs-git.log](docs-git.log) |
| `python3 -B scripts/docs_check.py`, no-metadata CI mode | 0 | 0 findings | [docs-no-git.log](docs-no-git.log) |
| `python3 scripts/check_baremetal_only.py --check` | 0 | PASS | [baremetal-only.log](baremetal-only.log) |
| `python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9` | 0 | PASS | [em-dash.log](em-dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | PASS | [doc-style.log](doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | PASS | [toc.log](toc.log) |
| `python3 scripts/check_doc_paths.py` | 0 | PASS | [doc-paths.log](doc-paths.log) |
| `python3 scripts/check_py_idiom.py` | 0 | PASS | [python-idiom.log](python-idiom.log) |
| `git diff --check` | 0 | Clean | [diff-check.log](diff-check.log) |
| `git diff --check 991d59653ff82ccf73ef4df9477de1df8c8c5964 HEAD` | 0 | Clean | [committed-diff-check.log](committed-diff-check.log) |

Every required command returned 0. [gates.json](gates.json) records the command arrays, exact head, durations and log names. Gate logs contain the complete unfiltered output. No gate was piped.

The SDK run uses [full-builder-sdk.py](full-builder-sdk.py), copied from the assignment's `$VALIDATION_STORAGE/408-manager-r6/full-builder-sdk.py` with only the receipt destination changed. It verifies `$VALIDATION_STORAGE/504-manager-r1/sdk-install`, maps only the settled selector's argument zero, then runs all of `sw/builder/test_builder.py` with `--require-rv32`. The SDK archive digest is `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`.

The absent run uses [full-builder-absent.py](full-builder-absent.py), the repository's `CompilerAudit`, and the full builder entry point. It verifies that all three cross candidates are hidden, no firmware compilation occurs, and the missing instruments are registered NOT RUN. Real host version and target probes remain available.

The second documentation run uses an exact-head tracked-source export without repository metadata, in disposable scratch under `$VALIDATION_STORAGE`. That export is removed after the run. No checkout was created.

Reproduce from the candidate worktree, with `EVIDENCE_DIR` naming the directory containing this handoff. Preserve existing receipts before rerunning the two full-suite drivers, which refuse to overwrite them.

```sh
python3 -u "$EVIDENCE_DIR/full-builder-sdk.py"
python3 -u "$EVIDENCE_DIR/full-builder-absent.py"
python3 -B scripts/docs_check.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/check_py_idiom.py
git diff --check
git diff --check 991d59653ff82ccf73ef4df9477de1df8c8c5964 HEAD
```

Run `python3 -B scripts/docs_check.py` from the disposable export for the no-metadata CI mode. [run-gates.py](run-gates.py) records the complete sequence, including the export and its cleanup. All commands ran in the foreground with generous timeouts.

## Acceptance and next actions

Acceptance 4 is met for this correction: 280/280 SDK and 222/222 absent, with full-suite return code 0 in both modes. Both accept 29/29 firmware and 4/4 Makefile edits. The 1846/1846 spelling checks and unchanged 6440/6440 closure cells pass in both modes, re-measured with the SDK and read against the recorded oracle without it. The full-suite final verdicts name only the existing missing-report arm with the SDK, and that arm plus the missing compiler instruments without it.

The final worktree is clean at the stated head; [final-state.json](final-state.json) records the branch, head and tree. No changes followed validation.

Reviewers must assess this head independently; this author handoff supplies no approval or reviewer-owned coverage ledger. The new corpus row changes test evidence as well as documentation. Manager duties remain publication, final-head review and required CI acceptance, candidate-merge validation, authorized merge and containment.

The only public write authorized for this session is the `[A276] REVIEW READY` comment on #408. The commit and prepared PR body remain local. No push, PR edit, merge, other checkout, delegated work or hardware operation was performed.
