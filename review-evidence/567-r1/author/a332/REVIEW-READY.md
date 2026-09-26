[A332] REVIEW READY
Commit: `54b4c3bbbc8cdea5ced0be29c9226fdf82233b74`
Branch: `567-pp-pin-0922e434`; starting head `c9484ac8e86cb33d1120471530f9e1762bd4af1f`.

Changed: only the assigned passages in `CHANGELOG.md` and `docs/reference/SUBMODULES.md`. Both now state that the repository recorder added `0922e434` ledger rows whose digests match the `990f9652` rows. The superseded unchanged-ledger and open-decision claims are removed. Direct comparison confirms both ledger digests match; the ledger itself is unchanged in this round.

Validation: every assigned gate ran in the foreground without a pipeline and returned 0. The em-dash gate and metadata-free export used final HEAD; other content checks used the exact committed bytes.

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

The metadata-free mode's inventory-parity skip is expected and is not counted as a pass. Renderer dependencies came from the repository's hash-locked requirements in an isolated environment.

Acceptance: the [Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845274184) is met. The commit contains only the two requested document edits, with a one-line message and no body or trailers. The working tree is clean. `HANDOFF.md` and the full three-round `PR-BODY.md` are prepared in the assigned output directory.

Open risks/questions for this text alignment: none. Independent review and the wider merge bar remain pending. The head remains local; no push, PR creation or merge was performed.
