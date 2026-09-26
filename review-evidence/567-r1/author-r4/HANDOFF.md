[A335] Round 4 handoff

Issue: [#567](https://github.com/kebag-logic/milan-fpga/issues/567)
PR: [#569](https://github.com/kebag-logic/milan-fpga/pull/569)
Assignment: [Round 4](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845507642)
Finding: [R327-1](https://github.com/kebag-logic/milan-fpga/pull/569#issuecomment-5845505218)

Branch: `567-pp-pin-0922e434`
Starting head: `54b4c3bbbc8cdea5ced0be29c9226fdf82233b74`
Candidate head: `9143e21a57e6315c7678430cfc45b4a2b7e10c09`
Validation base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`
Confirmed origin: `https://github.com/kebag-logic/milan-fpga.git`
Commit subject: `docs: restore the recorded processor pin and clarify ledger rows`
Commit body and trailers: none.

## Changes and acceptance

1. F1: `tb/verilator/milan_dp/README.md:468` now restores the pin of record. The recorded passing result explicitly names `990f9652` as its measurement pin.
2. S1: `docs/reference/SUBMODULES.md:57-58` requires ledger rows for the pin of record, then requires those rows to match that exact pin.
3. S3: [PR-BODY.md](PR-BODY.md) contains the complete body retrieved from the current PR, updated for this head with the first line `[A335]`, a Round 4 section, both stale status statements removed, and `Closes #567` retained. This is a local deliverable; the live PR was not edited.

The assigned S1 sentence has 11 words; the required gate permits 10.
The equivalent two-sentence wording passes without changing the gate:
"OOC synthesis requires ledger rows for the pin of record.
Rows must match that exact pin."
This adaptation is recorded in the [takeover comment](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845522071).

Only the two named Markdown files changed in this round.
The commit has three added lines and two removed lines.
The worktree is clean and one commit ahead of its tracking branch.
No push, PR edit, merge, additional checkout or delegation occurred.
S2 remains outside this round, tracked by #571.

## Validation at the candidate head

All commands ran in the foreground without pipelines.
Python commands used the isolated environment at `/tmp/a335-docs-venv`.
Its dependencies were installed from `tools/markdown/requirements.txt` with `--require-hashes`.

| Command | Mode / result | rc |
|---|---|---|
| `git grep -n 990f965` | 12 matching lines; every hit explained below | 0 |
| `python3 -B scripts/docs_check.py` | Git inventory: 0 findings; 166 Markdown files, 884 text files; self-test 23/23 | 0 |
| `python3 -B scripts/docs_check.py` | Metadata-free archive: 0 findings; same file counts; self-test 22/22; Git inventory parity explicitly skipped | 0 |
| `python3 -B scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 findings; 339/339 controls | 0 |
| `python3 -B scripts/check_doc_style.py` | 22 current documents OK | 0 |
| `python3 -B scripts/gen_toc.py --check` | 108 annotated contents lists; 17 pages below threshold | 0 |
| `python3 -B scripts/gen_toc.py --verify-anchors` | 176 cross-page fragment links reproduced | 0 |
| `python3 -B scripts/check_doc_paths.py` | 847 cited paths resolve | 0 |
| `git diff --check` | Clean worktree | 0 |
| `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD` | Candidate range clean | 0 |

The filesystem CI mode used an archive of this exact committed head:

```sh
git archive --format=tar --output=/tmp/a335-no-git-j2WuE9/head.tar HEAD
tar -xf /tmp/a335-no-git-j2WuE9/head.tar -C /tmp/a335-no-git-j2WuE9/tree
```

The extraction directory was created first.
From that directory, `/tmp/a335-docs-venv/bin/python3 -B scripts/docs_check.py` returned 0.
No Git metadata was present; the gate reported `filesystem walk (no git)`.
The explicit inventory-parity skip matches that CI mode.

Receipts: [old-pin hits](receipts/old-pin-hits.txt),
[Git docs mode](receipts/docs-git.txt),
[filesystem docs mode](receipts/docs-no-git.txt),
[em dash](receipts/em-dash.txt),
[style](receipts/doc-style.txt),
[contents](receipts/toc-check.txt),
[anchors](receipts/toc-anchors.txt),
[cited paths](receipts/doc-paths.txt),
[worktree whitespace](receipts/diff-working.txt),
[candidate whitespace](receipts/diff-range.txt).
The whitespace receipts are empty because both commands succeeded without diagnostics.

## Every remaining old-pin hit

| Remaining hit | Why it is historical |
|---|---|
| `CHANGELOG.md:14` | Contents link to the earlier #508 adoption entry. |
| `CHANGELOG.md:36` | The source pin in the recorded #567 transition to `0922e434`. |
| `CHANGELOG.md:45` | Comparison with the previous pin's retained ROM digest rows. |
| `CHANGELOG.md:72` | Heading for the earlier #508 adoption entry. |
| `CHANGELOG.md:74` | The #508 transition from `09f9bf38` to the former pin. |
| `docs/reference/SUBMODULES.md:42` | PR 115's merge is explicitly called the previous pin. |
| `docs/reference/SUBMODULES.md:55` | Comparison with the previous pin's retained ROM digest rows. |
| `syn/yosys/rom_digests.tsv:32` | Retained historical `ltn_rom.hex` digest keyed by the old pin. |
| `syn/yosys/rom_digests.tsv:33` | Retained historical `ucode.hex` digest keyed by the old pin. |
| `tb/verilator/milan_dp/README.md:442` | Provenance for the recorded ACTIVE-to-licence latency measurement. |
| `tb/verilator/milan_dp/README.md:468` | Explicit past-tense passing measurement; the procedure restores the pin of record. |
| `tb/verilator/milan_dp/README.md:552` | Two fixed historical source permalinks for field lineage and settlement details; neither selects a checkout revision. |

There are 12 matching lines, including two old-pin permalinks on line 552.
None instructs a reader to restore the old pin or calls it current.

## Review handoff

R327 must re-review the Docs and Conformance delta at the candidate head.
Per the assignment, R326-1 remains the ancestor POSITIVE at `54b4c3bbbc8cdea5ced0be29c9226fdf82233b74`.
This author handoff supplies evidence and does not publish a review verdict.
The manager owns publication of the local commit and revised PR body.
Exact-head hosted evidence, remaining independent review, candidate-merge validation and post-merge containment remain outstanding.
No RTL, simulation, synthesis or hardware evidence was rerun or newly claimed in this docs-only round.
