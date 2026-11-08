"""Build this round's PR-BODY.md from round 5's. Usage:
    python3 -I make_pr_body.py <r5 body> <out> <head> <r5 head> <dev full sha> <steps>"""
import sys
from pathlib import Path

src, out, head, r5head, dev, steps = sys.argv[1:7]
t = Path(src).read_text(encoding="utf-8")


def sub(a, b):
    global t
    assert t.count(a) == 1, (t.count(a), a[:80])
    t = t.replace(a, b)


sub("[A720o]\n", "[A720p]\n")
sub("GREEN, documentation only -- every run step of the docs workflow exits 0", "GREEN, documentation only -- every locally runnable step of the docs workflow exits 0")
sub("- **[Round 5](#round-5)** -- The answer to R765-4-F1 / R766-4-F1 and three residues, one commit each.\n",
    "- **[Round 5](#round-5)** -- The answer to R765-4-F1 / R766-4-F1 and three residues, one commit each.\n"
    "- **[Sync with dev 0a75aa77](#sync-with-dev-0a75aa77)** -- One merge of dev; one conflict, both sides' rows kept.\n")
sub(f"clean clone of head `{r5head}`, including both builder legs (55 recorded steps, all rc 0), "
    "and `git diff --check` against the merge base `503bc97c` is clean",
    f"clean clone of head `{head}`, including both builder legs ({steps}), "
    "and `git diff --check` against the merge base `0a75aa77` is clean")
sub("then `[A720o]` for round 5\n", "then `[A720o]` for round 5, then `[A720p]` for the sync with dev\n")
sub("## Authoritative references\n", f"""## Sync with dev 0a75aa77

Both round 5 reviews were POSITIVE at `d85da329`: R765-5 (issuecomment-6586963259) and R766-5 (issuecomment-6587152040). Dev then moved, so this round merges it.

One merge commit, `git merge --no-ff origin/dev`, with no rebase, force or amend. Dev brought 9 merges, 231 commits, from `503bc97c` to `0a75aa77`:

| PR | Issue | Subject |
|---|---|---|
| #831 | #829 | Run the gPTP plane on the MII port at 100 Mb/s |
| #836 | #737 | Split the hosted LiteX simulations into three measured elaborate legs |
| #815 | #797 | Generate the documentation audit from every tracked document and verify the release-facing pages |
| #834 | #833 | Bound and explain the owned-process cleanup under load |
| #841 | #839 | Hold the CSR-addressed transmitters until the station MAC is written |
| #842 | #840 | Prototype identity, 1000BASE-T-only advertisement on 1G PHYs, and the stricter-reading page |
| #849 | #848 | Drop line counts from the generated audit page |
| #847 | #845 | Adopt protocol-processor main `92100657` |
| #846 | #843 | Adopt FPGA-gPTP main `1616fc8f` |

| File | Merge | Resolution |
|---|---|---|
| `docs/findings/README.md` | conflict on two adjacent rows | Dev's 234 row (#843's route record, #845's standalone records) and this branch's 649 row are both kept, each unchanged. |
| `docs/design/AREA_BUDGET.md` | clean | Dev's #845 and #843 records and this branch's target sentences are on separate lines; both kept. |
| `docs/design/MARK_II_AREA_PLAN.md` | clean | Dev's +0.242 ns record and its #845 and #843 lines merge beside this branch's text. No branch line cites a record dev moved. |

No generator output changes. The inventory, contents, diagram and matrix checks are fresh at the merge, so there is no regeneration commit.

Nothing else changes. The head differs from dev only in this branch's four pages: 231 lines added and 53 removed, as before.

Both round 5 reviews asked for the census coverage check on current dev. At the merge it passes against dev's `sw/litex/milan_soc.py`.

Its control against the round 1 page still fails, as it must.

## Authoritative references
""")
sub("- PR #835's round 4 reviews: R765-4 (issuecomment-6584004136) and R766-4 (issuecomment-6582620684).\n",
    "- PR #835's round 4 reviews: R765-4 (issuecomment-6584004136) and R766-4 (issuecomment-6582620684).\n"
    "- PR #835's round 5 reviews: R765-5 (issuecomment-6586963259) and R766-5 (issuecomment-6587152040), both POSITIVE.\n")
sub(f"git rev-parse HEAD        # {r5head}", f"git rev-parse HEAD        # {head}")
sub("git merge-base HEAD origin/dev   # 503bc97cd4f24ad07596c17e7188f2024617972d",
    f"git merge-base HEAD origin/dev   # {dev}")
sub("python3 scripts/check_em_dash.py --base 503bc97c\n", "python3 scripts/check_em_dash.py --base 0a75aa77\n")
sub("python3 scripts/check_doc_paths.py\ngit diff --check 503bc97c HEAD\n",
    "python3 scripts/check_doc_paths.py\npython3 scripts/docs_inventory.py --check\ngit diff --check 0a75aa77 HEAD\n")
sub('["git", "diff", "-U0", "503bc97c", "--", page]', '["git", "diff", "-U0", "0a75aa77", "--", page]')
Path(out).write_text(t, encoding="utf-8")
