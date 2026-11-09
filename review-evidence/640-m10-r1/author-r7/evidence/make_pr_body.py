"""Build this round's PR-BODY.md from round 6's. Usage:
    python3 -I make_pr_body.py <r6 body> <out> <head> <r6 head> <dev full sha> <steps>"""
import sys
from pathlib import Path

src, out, head, r6head, dev, steps = sys.argv[1:7]
t = Path(src).read_text(encoding="utf-8")


def sub(a, b):
    global t
    assert t.count(a) == 1, (t.count(a), a[:80])
    t = t.replace(a, b)


sub("[A720p]\n", "[A720q]\n")
sub("- **[Sync with dev 0a75aa77](#sync-with-dev-0a75aa77)** -- One merge of dev; one conflict, both sides' rows kept.\n",
    "- **[Sync with dev 0a75aa77](#sync-with-dev-0a75aa77)** -- One merge of dev; one conflict, both sides' rows kept.\n"
    "- **[Sync with dev ac0a01e3](#sync-with-dev-ac0a01e3)** -- Round 7: one merge of dev; one conflict, both rows kept; no figure corrected.\n")
sub(f"clean clone of head `{r6head}`, including both builder legs (65 run steps, all rc 0; 31 hosted-only steps not run, each with its stated reason), "
    "and `git diff --check` against the merge base `0a75aa77` is clean",
    f"clean clone of head `{head}`, including both builder legs ({steps}), "
    "and `git diff --check` against the merge base `ac0a01e3` is clean")
sub("then `[A720p]` for the sync with dev\n", "then `[A720p]` for the sync with dev, then `[A720q]` for the second sync\n")
sub("## Authoritative references\n", """## Sync with dev ac0a01e3

Both round 6 reviews were POSITIVE at `72816d26`: R765-6 (issuecomment-6719846258) and R766-6 (issuecomment-6719945800). Dev then moved, so this round merges it.

One merge commit, `git merge --no-ff origin/dev`, with no rebase, force or amend. Dev brought one merge, 11 commits, from `0a75aa77` to `ac0a01e3`:

| PR | Issue | Subject |
|---|---|---|
| #852 | #851 | Adopt the processor pin that sends one vector per value: processor `044cb25f`, the fifteenth area record, the area budget and the #234 page |

| File | Merge | Resolution |
|---|---|---|
| `docs/findings/README.md` | conflict on two adjacent rows | Dev's 234 row (now #851's record of 2026-11-08) and this branch's 649 row are both kept, each unchanged. |
| `docs/design/AREA_BUDGET.md` | clean | Dev's #851 record, record table and allocation figures sit on other lines than this branch's target sentences; both kept. |
| `docs/design/MARK_II_AREA_PLAN.md` | clean | Dev's +0.210 ns warning row and its #851 anchor line merge beside this branch's text. |

Corrected figures: none. Every figure the branch's lines cite comes from the 2026-10-31 basis build or NFR-RES-01. Dev changed neither.

No branch line cites a record figure that #851 moved. The superseded #843 figures still on the pages are dev's history lines.

No generator output changes. The inventory, contents, diagram and matrix checks are fresh at the merge, so there is no regeneration commit.

Nothing else changes. The head differs from dev only in this branch's four pages: 231 lines added and 53 removed, as before.

The census coverage check still passes at the merge, and its round 1 control still fails. Dev's `sw/litex/milan_soc.py` has not changed since `0a75aa77`.

Both round 6 residues, R765-6-R1 and R766-6-RESIDUE-1, ask for the reference bullet's base. It now names the merge base `ac0a01e3`.

## Authoritative references
""")
sub("- PR #835's round 5 reviews: R765-5 (issuecomment-6586963259) and R766-5 (issuecomment-6587152040), both POSITIVE.\n",
    "- PR #835's round 5 reviews: R765-5 (issuecomment-6586963259) and R766-5 (issuecomment-6587152040), both POSITIVE.\n"
    "- PR #835's round 6 reviews: R765-6 (issuecomment-6719846258) and R766-6 (issuecomment-6719945800), both POSITIVE.\n")
sub("`docs/integration/QSPI_FLASHBOOT.md` at `503bc97c`; NFR-RES-01",
    "`docs/integration/QSPI_FLASHBOOT.md` at `ac0a01e3`, the merge base; since `503bc97c` only `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md` changed, by dev's #845, #843 and #851 records; NFR-RES-01")
sub(f"git rev-parse HEAD        # {r6head}", f"git rev-parse HEAD        # {head}")
sub("git merge-base HEAD origin/dev   # 0a75aa774b89ac89351700f63dd8cbb89694af6c",
    f"git merge-base HEAD origin/dev   # {dev}")
sub("python3 scripts/check_em_dash.py --base 0a75aa77\n", "python3 scripts/check_em_dash.py --base ac0a01e3\n")
sub("git diff --check 0a75aa77 HEAD\n", "git diff --check ac0a01e3 HEAD\n")
sub('["git", "diff", "-U0", "0a75aa77", "--", page]', '["git", "diff", "-U0", "ac0a01e3", "--", page]')
Path(out).write_text(t, encoding="utf-8")
