[A332]

# Issue #567, Round 3 handoff

Head: `54b4c3bbbc8cdea5ced0be29c9226fdf82233b74`
Starting head: `c9484ac8e86cb33d1120471530f9e1762bd4af1f`
Branch: `567-pp-pin-0922e434`
Base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`
Origin confirmed: `https://github.com/kebag-logic/milan-fpga.git`
Commit: `Align processor pin documentation with recorded ROM digests`

The commit has one subject line, no body and no trailers.

## Assignment and changes

The [Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845274184) limits this round to two passages.

- `CHANGELOG.md:44`: replace the unchanged-ledger claim with the recorded outcome.
- `docs/reference/SUBMODULES.md:53`: replace the unchanged-ledger and open-decision claims with the recorded outcome; retain the exact-pin OOC requirement.

Both passages now state that the repository recorder added rows for `0922e434`, and their digests match the `990f9652` rows. The commit changes only these two documents: five insertions and four deletions.

## Ledger evidence

The [Round 2 decision](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845149786) authorized re-recording because the ledger keys include the exact processor pin. The [Round 2 evidence](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845257136) records the repository command and successful normal OOC validation.

Direct comparison of `syn/yosys/rom_digests.tsv` confirms:

| Image | SHA-256 at both `0922e434` and `990f9652` |
|---|---|
| `ltn_rom.hex` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` |
| `ucode.hex` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` |

The ledger itself was not modified in this round.

## Validation

Every listed gate ran in the foreground without a pipeline and returned 0. Content checks ran on the exact working-tree bytes committed at the head above. The em-dash gate and metadata-free export checked final HEAD.

| Command / CI mode | Result | Evidence |
|---|---|---|
| `python3 -B scripts/docs_check.py` (Git mode) | rc 0; 0 findings; 23/23 scrub, 4/4 routing controls | `docs-git.log` |
| `python3 -B scripts/docs_check.py` (metadata-free export of final HEAD) | rc 0; 0 findings; 22/22 scrub, 4/4 routing controls; inventory parity skipped because it requires Git | `docs-no-git.log` |
| `python3 -B scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | rc 0; 0 findings; 339/339 controls | `em-dash.log` |
| `python3 -B scripts/check_doc_style.py` | rc 0; 22 current documents | `doc-style.log` |
| `python3 -B scripts/gen_toc.py --check` | rc 0; 108 contents lists, 17 below threshold | `toc-check.log` |
| `python3 -B scripts/gen_toc.py --verify-anchors` | rc 0; 176 fragment links reproduced | `toc-anchors.log` |
| `python3 -B scripts/check_doc_paths.py` | rc 0; 847 paths resolve | `doc-paths.log` |
| `git diff --check` | rc 0 | `diff-check.log` |
| `git diff --cached --check` (before commit) | rc 0 | Terminal result |
| `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD` | rc 0 | Terminal result |

Renderer dependencies were installed from `tools/markdown/requirements.txt` with hash verification in an isolated temporary environment. The filesystem-mode check used an archive of final HEAD extracted outside every Git worktree, containing no Git metadata. Its inventory-parity skip is expected and is not counted as a pass.

## Review handoff

The Round 3 assignment is satisfied. Reviewers remain [R326] internal and [R327] external. Full issue review and the merge bar remain pending; this is an author handoff.

`PR-BODY.md` contains the full proposed PR body, covering the pin/documentation adoption, generated ledger rows with identical digests, and this text alignment. Earlier validation claims are linked to public issue evidence. No private transcript was consulted. No push, PR creation, merge, or additional checkout was performed.
