[A335] REVIEW READY

Commit: `9143e21a57e6315c7678430cfc45b4a2b7e10c09`
Branch: `567-pp-pin-0922e434`
Round: 4, docs only, for PR #569.

Changed:
- F1: `tb/verilator/milan_dp/README.md:468` restores the pin of record and identifies `990f9652` only as the historical passing-measurement pin.
- S1: `docs/reference/SUBMODULES.md:57-58` requires ledger rows matching the exact pin of record. The assigned sentence has 11 words against a ten-word gate; two equivalent sentences preserve the requirement and pass the unchanged gate.
- S3: the complete current PR body is prepared locally as `PR-BODY.md`, with `[A335]` first, a Round 4 section, the two stale status statements removed and `Closes #567` retained. The live PR body remains unchanged for the manager to update.

Validation at this exact head, all foreground and unpiped:

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

Python used an isolated environment with the hash-locked documentation dependencies. The filesystem mode ran in a metadata-free `git archive HEAD` export of this candidate.

Every remaining old-pin hit:

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

Acceptance: F1 and S1 are implemented; S3's full replacement body and `HANDOFF.md` are prepared in the assigned output directory. Only the two assigned Markdown files changed. The one-line commit has no body or trailers; the worktree is clean.

Open risks/questions: R327's Docs and Conformance delta review is pending. Per the assignment, R326-1 remains the ancestor POSITIVE; S2 is tracked in #571. Publication, exact-head hosted evidence and merge duties remain with the manager. No push, PR edit, merge or additional checkout was performed.
