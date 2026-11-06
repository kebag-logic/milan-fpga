## Round 12

Both round 11 reviews of `5843d1af1d3a892fdc0fbb766ba2058ec44c26ea` are POSITIVE. Dev has moved to `cc204c6f` with PR #836, the elaborate-gate split, and PR #815, the documentation audit. #815 adds `scripts/docs_inventory.py` and `docs/DOCUMENTATION_AUDIT.md`, which is generated from every tracked document. This PR changes `docs/testing/TESTING.md`, so the audit page went stale on the merge. Round 12 does only these two things:
1. merges dev;
2. regenerates the page through its generator.

No other file is touched.

### Round 12 commits

| Commit | Subject |
|---|---|
| `3f4e39f35d19b416b7acb3a570273bfb1a327c0d` (parents `5843d1af`, `cc204c6f`) | Merge dev cc204c6f into 833-owned-process |
| `3e475161e528baa655a5ba84d6a38d78f8c64f3b` | Regenerate the documentation inventory on the merge of dev cc204c6f: 213 pages, 176 current and 16 stale (#833) |

**The merge had no conflict.** `docs/testing/TESTING.md` is the only file changed on both sides, and git merged it automatically, keeping both. Dev's lines there come from #737 and #829.

The PR's diff against its base has the same stable patch-id before and after the merge, `a5e12980a28b73885022d9b0d029df8f1555af6e`: `git diff 1f29f189 5843d1af` against `git diff cc204c6f 3f4e39f3`. So the change under review is the one both round 11 reviews saw. The four PR files other than TESTING.md are byte-identical to round 11's head. TESTING.md differs from it only by dev's lines.

**The regeneration ran through the generator alone.** Before it, `python3 scripts/docs_inventory.py --check` was rc 1: `STALE (4 lines differ)`, first at the stale-lines total. Then `--write` ran, and its diff is 4 lines of `docs/DOCUMENTATION_AUDIT.md`, all following TESTING.md's merged length:
- TESTING.md's row: 1935 to 2019 lines;
- D0-057's cited line: 1818 to 1902, which is still the "Presentation-time offset is pinned at the Milan 2 ms DEFAULT" line;
- the stale and total line counts: 10,638 to 10,722 and 92,127 to 92,211.

Page counts are unchanged at 213 pages, 176 current and 16 stale. `scripts/docs_inventory.json` was not changed by `--write`. Afterwards, `--check` and `--selftest` both gave rc 0.

### Round 12 gates

All at head `3e475161e528baa655a5ba84d6a38d78f8c64f3b`, each on a clean clone of it, one log and rc each, never piped, SIGHUP at its default in every launcher.

| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 65 steps rc 0, 31 not run with the round 1 reason (hosted-only or apt), 0 bad. Dev's new docs-gates-0 inventory step is the 65th step, and it printed `documentation inventory: OK` and `selftest: OK (50 controls)`. That step shifts the later docs-gates-0 ids by one, so the hosted-only receipts-record step is now `ci_step_55`, and its not-run entry follows it with its reason unchanged. The tree was clean after each job. Builder legs: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in rounds 1 to 11 |
| `python3 scripts/docs_inventory.py --check` | rc 0, `documentation inventory: OK (540 lines, docs/DOCUMENTATION_AUDIT.md is fresh)` |
| `python3 scripts/docs_inventory.py --selftest` | rc 0, `documentation inventory selftest: OK (50 controls)` |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| `git diff --check cc204c6f HEAD` | rc 0, silent |
| `git merge-base --all HEAD origin/dev` | One merge base, `cc204c6f` |
| `--mutants`, `--matrix`, `behave`, the reviewers' probes, the full sweep | Not rerun in round 12, which changes none of the files they exercise beyond dev's merged lines |

The image command-table checker (#838) is not a gate this round. At this head and at dev it refuses identically, on an unset image-parser setting, before checking any table.
