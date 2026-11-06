[A739] REVIEW READY
Commit: 212b7d6ec506489a4c371e1f214b89a58a60b21e
Changed: `scripts/docs_inventory.py` no longer renders the summary and inventory `Lines` columns, the page's own-row count, the Findings line number (now `Located`: `on page` or `re-verify: quote not found`) or the banner line number. `--findings-dir` keeps its line numbers. `docs/DOCUMENTATION_AUDIT.md` is regenerated: same 540 lines, same 76 findings. The digest is re-pinned in `ci/image/command-table.json`. One comment line in `.github/ci-templates/docs.yml` no longer lists line count; the generated workflows are unchanged.
Validation, all on a clean clone of that head, base dev 87e9d03aa2a4797957ac0124d0c7851a2eec234c:
- `python3 scripts/docs_inventory.py --check`: rc 0
- `python3 scripts/docs_inventory.py --selftest`: rc 0, 53 controls; 13 planted mutants, all killed
- every `run:` step of `.github/workflows/docs.yml`: 72 ran rc 0, 24 not run with a stated reason (hosted context, apt or sudo), 0 bad; every job's tree clean after it
- `git diff --check`: rc 0
- privacy check of the added lines against origin/dev: 0 private lines
Acceptance criteria:
- Page changes only on status, finding or page set, not length: met for length. Added and removed lines, and lines added above a finding, a copy and a banner, leave `--check` rc 0. On the real tree, lines added to two pages, one above a recorded finding, gave rc 0. See the open question for the literal "only".
- Self-test proof: met. An added line gives rc 0; a status change with no document edit, a new page and a removed page each go stale. The same probes on the real tree gave rc 1.
- `--check`, `--selftest`, the re-pin and the docs gates: met. No script writes the table's digest, so the re-pin used the table's own hash and serializer helpers; the diff is that one line. `scripts/ci_tool_inventory.py --check` was not run, because it needs the pinned shell parser, which is not available here.
Open risks/questions:
1. Audience, Purpose and Describes stay, so an edit to a title, audience line or cited path still refreshes the page. Decision requested: is that the intended reading of "only"? #797 requires those columns.
2. `ci/image/tool-inventory.json` records a command-table digest that was already stale at dev (`c9bd5d35` against `c20764fa`). No docs.yml step reads it, and this change leaves it alone. It needs its own Issue.
3. `scripts/docs_inventory.py` is at 999 lines against the 1000-line limit. The first head, f5ccb318, failed the Python idiom gate at 1044 lines; 212b7d6e fixes that and the full docs.yml run was repeated on it.
4. An open PR carrying the old page needs one more `--write` after this lands.
