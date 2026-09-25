[A317] HANDOFF

PR #563 / issue #545, docs round.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5833028966
- Review: https://github.com/kebag-logic/milan-fpga/pull/563#issuecomment-5833027417
- Branch: `545-crf-servo-slew`.
- Starting head: `b376f6113b388929fe82e883d400e5361319b966`.
- Final local head: `4538d7c03dc4f56d7ed4c971603e15bda82050a8`.
- Documentation comparison base: `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.
- Origin confirmed: `https://github.com/kebag-logic/milan-fpga.git`.
- Commit subject: `docs: align slew campaign inventories with their controls`.

## Changes

| Finding | File:line | Change |
|---|---|---|
| R301-3 F1 | `tb/verilator/milan_dp/README.md:590` | States fourteen explicit controls and links the authoritative `CONTROLS` list. Derives the total as eleven tabulated controls plus three #545 controls; identifies the table's two option-off entries. Dated historical measurements remain intact. |
| R301-3 S1 / R300-3 S2 | `scripts/measure_test_evidence.py:597` | The slew campaign disposition names all eight defects, adding streak increment on slew discard and slew discard counted as a guard trip. |

The static inventory check finds fourteen datapath controls: twelve gmstep and two option-off, including three policy-level controls. The servo campaign has five `MUTANTS` and three `STREAK_MUTANTS`. Outside the single disposition string, the evidence reader's syntax tree is identical to the starting head. Only the two assigned files changed. See [scope-inventory.log](scope-inventory.log).

## Gates

Every gate ran in the foreground without a pipeline, with a 1200-second timeout. Receipts identify the exact committed head, command, result and elapsed time.

| Command | RC | Result | Receipt |
|---|---|---|---|
| `python3 scripts/measure_test_evidence.py --check` | 0 | Ratchet PASS; no unexplained source readers | [measure_test_evidence_check.log](measure_test_evidence_check.log) |
| `python3 scripts/measure_test_evidence.py --selftest` | 0 | 101/101 | [measure_test_evidence_selftest.log](measure_test_evidence_selftest.log) |
| `python3 -B scripts/docs_check.py` | 0 | Git mode: 0 findings; 23/23 scrub, 4/4 routing | [docs_check_git.log](docs_check_git.log) |
| `python3 -B scripts/docs_check.py` | 0 | No-Git archive: 0 findings; 22/22 scrub, 4/4 routing | [docs_check_no_git.log](docs_check_no_git.log) |
| `python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7` | 0 | 0 findings; 339/339 arms | [check_em_dash.log](check_em_dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | 22 documents OK | [check_doc_style.log](check_doc_style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | 107 contents lists OK; 17 below threshold | [gen_toc_check.log](gen_toc_check.log) |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | 174 links reproduced | [gen_toc_verify_anchors.log](gen_toc_verify_anchors.log) |
| `python3 scripts/check_doc_paths.py` | 0 | 847 cited paths resolve | [check_doc_paths.log](check_doc_paths.log) |
| `python3 scripts/check_py_idiom.py` | 0 | Ratchet PASS | [check_py_idiom.log](check_py_idiom.log) |
| `git diff --check` | 0 | Clean worktree | [git_diff_check.log](git_diff_check.log) |
| `git diff --check 864b36f5e9450ef64f75ca3f0d68c44330e447d7 HEAD` | 0 | Committed delta also clean | [git_diff_base_check.log](git_diff_base_check.log) |

The em-dash and contents gates used `/tmp/545-a317-docs-venv/bin/python3`, installed from the hash-locked `tools/markdown/requirements.txt`. Other commands used the system `python3`. Each command was invoked through `rtk proxy`, preserving its output and exit status.

No-Git mode ran the exact committed tree exported with `git archive --format=tar --output=<temporary-archive> 4538d7c03dc4f56d7ed4c971603e15bda82050a8` and extracted with `tar -xf <temporary-archive> -C <temporary-tree>`. The temporary tree had no Git metadata; its two changed files matched the worktree bytes. Its expected inventory-parity arm was skipped because that arm requires Git; all applicable arms passed. The archive and export were created under `/tmp` and removed after the gate. No toolchain or tree export is stored in this output directory.

## Handoff state

Both assigned outcomes are implemented and locally validated. Independent Docs re-review remains pending; this is author evidence, not a review verdict.

The local branch is one commit ahead of its remote tracking branch and the worktree is clean. No push, PR edit, merge, other checkout, sub-agent or hardware operation was performed. The planned final publication is the `[A317] REVIEW READY` comment on issue #545.

[PR-BODY.md](PR-BODY.md) preserves the complete current body fetched by `gh pr view 563 --repo kebag-logic/milan-fpga --json body`, changes its first line to `[A317]`, and appends the docs-round section. It retains `Closes #545`. The source response is [PR-BODY.original.json](PR-BODY.original.json); its body SHA-256 is `d0a4754b8311d14fdc9f530b95cf8cf87aef24e0b8ab8334c7f910d62f340079`. The prepared body contains no absolute home path, tool/model attribution or attribution footer.
