# [A378] Round 2 handoff

Status: assignment items 1-5 complete; committed page and prepared PR body ready for independent re-review.
PR: #600. Refs #394. Refs #387.
Branch: `394-387-e1-cycles`.
Starting head: `fddc58e43733afd90d6222e58999e0f416a30df9`.
Executor: [A378]. Reviewers: [R360] and [R361].
Scope: assignment items 1-5; findings page and prepared PR body.
No push or hardware activity is authorized.

## Assignment response

| Item | Findings | Change and file:line | Evidence |
|---|---|---|---|
| 1 | R360-1 F1; R361-1 F2 | `docs/findings/394_387_E1_SWITCH_CYCLES.md:235`: nine-cell delimiter; measurements unchanged | rc 0; six rendered tables; header, delimiter and ten data rows each have nine cells; zero recomputed differences |
| 2 | R360-1 F2; R361-1 F3 | `docs/findings/394_387_E1_SWITCH_CYCLES.md:185` and `:282`: unwritten software-published reset value, no PHY-driven counter edges through that status, unobserved PHY loss, possible inline capture hold-up; retain #394 FAIL. Also state unsampled guard/control and flat peer counters | #599; integration source; both reviews; all ten published peer counter deltas are zero |
| 3 | R360-1 F3; R361-1 F1 | `docs/findings/394_387_E1_SWITCH_CYCLES.md:11`, `:161`, `:223`, `:235`, `:345`: #387 NOT MET (not exercised), running-stream measurement required, counted event with no elapsed bound, #117 context distinguished, outage interval renamed | Both step-context receipts show HOLDOVER and no streams for all ten steps; linked round-2 decision settles the verdict |
| 4 | R360-1 F4; R361-1 F4 | `docs/findings/394_387_E1_SWITCH_CYCLES.md:383`: public branch, commit, path and publisher index; raw cold storage with size/hash indexes and historical temporary names; obsolete manifest claim removed | Publisher MANIFEST.json verified all 165 published hashes at 8f983d245a12e18a47ced37904d405b624c7e024 |
| 5 | Matching PR body | `PR-BODY.md:1`, `:3`, `:14`: original [A375] first line and issue references preserved; Round 2 maps both reviews to corrections | Prepared locally only; no PR edit or issue closure |

## Committed-head gates

Head: `6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1`.
Every command ran in the foreground from the physical worktree.
Gate output was redirected directly to receipts, never piped.
The Markdown gates used the pinned `tools/markdown/requirements.txt` environment.
The dependency environment is outside this packet.
`gates.json` records the exact head, commands, return codes and durations.

| Gate | Result |
|---|---|
| `python3 scripts/docs_check.py` | rc 0; `gate-docs-check.txt` |
| `python3 scripts/check_doc_style.py` | rc 0; `gate-doc-style.txt` |
| `python3 scripts/gen_toc.py --check` | rc 0; `gate-toc.txt` |
| `python3 scripts/check_em_dash.py --base 2a2a7bb6` | rc 0; `gate-em-dash.txt` |
| `python3 scripts/check_doc_paths.py` | rc 0; `gate-doc-paths.txt` |
| `python3 scripts/ci_scope.py --selftest` | rc 0; `gate-ci-scope.txt` |
| `python3 scripts/check_baremetal_only.py --check` | rc 0; `gate-baremetal.txt` |
| `python3 scripts/check_feature_status.py --self-test` | rc 0; `gate-feature-status.txt` |
| `git diff --check` | rc 0; `gate-diff-check.txt` |
| Per-cycle table header, delimiter and row cell counts | rc 0; `verification.txt`, lines 2-13; all nine cells |

## Delivery

Commit: `6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1`. Branch remains unpushed.
Issue takeover: https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5859056617.
Review-ready comment: https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5859147312.
Published from `REVIEW-READY.md`; round-2 author work stopped.
Independent re-review remains required.
R360-1 S1 is outside this PR; assignment routes it to #495.


## Evidence verification

- `verification.txt`: rc 0 at the committed head. Run `python3 verify_round2.py <physical-worktree>` using the pinned Markdown dependencies. It checks the table cells and rendered HTML, unchanged cycle rows, publisher hashes, 50 raw-artifact index entries, step context, peer counter deltas and locator hygiene.
- `recompute-table.txt`: rc 0 using R360-1 `scripts/recompute_table.py <page> <operator-packet>`. All ten rows MATCH; zero differing rows; all summary measurements agree.
- `hygiene-page.txt`: only the known `041060010000bb80` CRF format matches the identifier heuristic. No private location, host, device name or serial is reported.
- `git diff --check 2a2a7bb6 HEAD`: rc 0 for the committed page, in addition to the required clean-worktree check.
- Public archive: `394-387-review-evidence`, `review-evidence/394-387-r1`, commit `8f983d245a12e18a47ced37904d405b624c7e024`; publisher `MANIFEST.json` verifies 165/165 entries.
- Raw captures remain in private cold storage. This correction checked retained analyses and indexes; it did not decode unavailable raw captures or acquire new hardware evidence.

## Scope and remaining work

Only `docs/findings/394_387_E1_SWITCH_CYCLES.md` changed in the repository.
The committed subject is one line, with no body or trailers.
The working tree is clean and the branch is unpushed.
PR-BODY.md is prepared locally; no PR edit was made.
No existing issue or PR comment was edited or deleted.
No other checkout, hardware, or delegation was used.
Only the authorized input packets and public repository state were read.

#394 acceptance 2 remains FAIL; #599 owns the publication fix and re-run.
#387 acceptance 4 remains NOT MET (not exercised).
The running-stream grandmaster-change measurement remains outstanding.
Independent reviewers must re-review the corrected head.
This author response does not supply a review verdict or clean-lens ledger.
