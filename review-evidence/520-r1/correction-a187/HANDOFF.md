# HANDOFF: A187, issue #520 / PR #522, R248-1 F1 (Docs)

## Identity

| field | value |
|---|---|
| branch | `520-yosys-rom-cache-identity` (local only, not pushed) |
| reviewed head (parent) | `28e350b99ac240a750326b762c6d029f0653362c` |
| new head | `d253f86e410e301d146d4bd4e74d027f00cfb462` |
| new tree | `ab5c567780993d405d0954092361396492cf49be` |
| base / live dev | `483a133ed08867ea0d300d2b4a027b5b48a4282f` (already an ancestor; `origin/dev` fetched and equal; no merge made) |
| commit subject | `Name the generated ROM bundle in the Yosys cache summaries` (one line, no trailers) |
| worktree | clean (`git status --porcelain` empty) |

## Change (Docs only, 2 files, +13/-12)

- `syn/yosys/README.md` Contents block (lines 24-31): page-wide separator switch from U+2014 to `--`
  (CONTRIBUTING.md 550-559). Descriptions that carried U+2014 were reworded with a colon, a
  parenthesis or a sentence break, with no change of meaning. The `ooc.sh` entry label keeps its U+2014
  because the generator copies it from the base heading; `check_em_dash` reports it as the single
  mirrored label exemption.
- `syn/yosys/README.md:27` (the result cache): no longer lists the pre-#520 inputs as sufficient. It now
  says a skip needs every input the key binds, the generated ROM bundle (#520) included, and names the
  key definition, the three ROM images and the schema-2 migration as section content.
- `.github/workflows/rtl.yml:538-542`: comment-only. The skip condition is now "every input its key
  binds, the generated ROM bundle (#520) included". It points to `syn/yosys/README.md` "The result cache"
  for the key definition. The rest of the comment (trust boundary, scoping) is unchanged. No YAML key,
  value, step or `run` text changed.
- `gen_toc.py --write syn/yosys/README.md` on the edited page wrote 0 pages, so the block is
  byte-identical to the generator's render.

Full diff: `diff-28e350b9..d253f86e.patch`
(sha256 `28f84379ef42529ffd8c0412737bb2ce4c269726f20fb1fffea6a2ffb40a7659`).

## Gates at the committed head (`gates/exits.txt`, raw logs in `gates/`)

Python 3.14.7. Each exit code is followed by the gate and its command.

```
head d253f86e410e301d146d4bd4e74d027f00cfb462 tree ab5c567780993d405d0954092361396492cf49be
0  gen_toc-check  :: python3 scripts/gen_toc.py --check
0  gen_toc-verify-anchors  :: python3 scripts/gen_toc.py --verify-anchors
0  gen_toc-selftest  :: python3 scripts/gen_toc.py --selftest
0  docs_check  :: python3 scripts/docs_check.py
0  docs_check-selftest  :: python3 scripts/docs_check.py --selftest
0  check_doc_style  :: python3 scripts/check_doc_style.py
0  check_em_dash  :: python3 scripts/check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f
0  check_em_dash-selftest  :: python3 scripts/check_em_dash.py --selftest
0  ci_events-check  :: python3 scripts/ci_events.py --check
0  ci_events-selftest  :: python3 scripts/ci_events.py --selftest
0  measure_fail_fast-check  :: python3 scripts/measure_fail_fast.py --check
0  measure_fail_fast-selftest  :: python3 scripts/measure_fail_fast.py --selftest
0  ci_scope-selftest  :: python3 scripts/ci_scope.py --selftest
0  check_hygiene-check  :: python3 scripts/check_hygiene.py --check
0  git-diff-check-base  :: git diff --check 483a133ed08867ea0d300d2b4a027b5b48a4282f HEAD
0  git-diff-check-prev  :: git diff --check HEAD~1 HEAD
0  git-diff-check-worktree  :: git diff --check
status_lines=0
```

`check_em_dash` summary: `0 finding(s) over 57 added line(s) in 2 changed Markdown page(s), 1 mirrored label(s) exempt, arms 57/57 [483a133e..HEAD]`.

`rtl.yml` readers in `scripts/`: `ci_events.py` (contract), `measure_fail_fast.py` (pipeline ratchet),
`ci_scope.py` (path classification only) and `act_ci.py` (workflow map). All except `act_ci.py` were run
and pass. `act_ci.py --selftest` was NOT RUN: AGENTS.md section 5 forbids running the candidate's copy on
the host, and this lane has no container authority. `measure_test_evidence.py` reads only the
protocol-processor workflow, not `rtl.yml`.

`gates-pre-commit/` is superseded and kept only for transparency. It ran on the uncommitted worktree, where
`check_em_dash` diffs base..HEAD and so judged only the parent's 49 lines. The committed-head run above is
the evidence.

## Sensitivity controls (disposable clone, deleted after; `controls/`)

| control | mutation at `d253f86e` | `check_em_dash --base 483a133e` | `gen_toc --check` |
|---|---|---|---|
| C1 | line 27 separator only back to U+2014 (mixed block) | exit 1 (2 findings: lines 27, 31) | exit 1 (TOC DRIFT) |
| C2 | whole block separator back to U+2014, new descriptions kept | exit 1 (6 separator findings) | exit 0 |

These reproduce the R248-1 executor note: only the page-wide `--` switch passes both gates.

## Not done / out of scope

- No push, PR edit, merge, container replica or hosted run. The new head exists only in this lane's local branch.
- SG1/SG2/SG3 untouched. The 48-vs-54 top-count prose (`README.md:93-94,159-160`) is untouched; R248-1
  listed it as outside #520.
- This change touches `.github/workflows/rtl.yml`, so the Docs lens and any lens whose scope includes
  that file must be re-covered at `d253f86e`. Exact-head act/hosted rtl-full evidence is required for the
  new head (manager-owned).
- No self-approval and no completion claim.
