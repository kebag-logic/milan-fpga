[R787] NEGATIVE - exact head 9d5a5af78f95f655e5104056c2c0ee2cca689279

Round R787-4, issue #848, PR #849. Tree `3f07baf86f848eb6f2d08d61224e96edd157c832`. Delta review of the manager sync.

## Verdict

The sync itself is sound. The merge is faithful, the audit is exactly what the generator writes, it carries no line counts, and the command table lost nothing.

The verdict is NEGATIVE because of one open MINOR, R787-4-F1, which comes out of focus check 4. The new page `docs/reference/STRICTER_READINGS.md` is rendered as verified by D0, and the lane figure rises from 18 to 19. D0 was checked at `1e80128f` on 2026-10-29, and the page was first committed on 2026-11-05. So the audit claims a check that cannot have happened.

**This is the one judgement call, and the manager may want to read it.** The #849 generator did not cause this. The rule is unchanged from dev, and `8ab3a930` already renders the same cell and the same 19. I still rate it MINOR for three reasons:

- This head's own commit adds the row and moves the figure.
- It is not wording. It is a generated cell and a generated figure, so the owner rule excludes RESIDUE.
- AGENTS.md section 7 says severity must not be lowered to bank a lens.

If the manager rules that the fix belongs elsewhere, that ruling should be public, and it should say that #842 carries the same row.

| ID | Severity | Lenses | Title |
|---|---|---|---|
| R787-4-F1 | MINOR | Conformance, Robustness, Docs | The audit claims a D0 check for a page that did not exist at the D0 commit |
| R787-4-S1 | SUGGESTION | Tests | 38 table digests differ from their files and 1 names a missing file, all unchanged from dev |
| R787-4-R1 | RESIDUE | Docs | The PR body still gives the page as 546 lines and its Validation section names `171fd56b` |
| R787-4-R2 | RESIDUE | Docs | The sync receipt's `parents` line belongs to the merge commit, not the head |

## Focus checks

**1. Merge faithfulness: PASS.** The head is not itself the merge. `a578ceb5` merges `171fd56b` and `8ab3a930`, and `9d5a5af7` regenerates the audit on top of it.

- `git merge-tree` of the two parents conflicts only in `docs/DOCUMENTATION_AUDIT.md`.
- Its tree `c904e03e` differs from `a578ceb5`, and from the head, in that one path only (`receipts/01_merge_tree.txt`, `receipts/02_tree_compare.txt`).
- The two sides changed only two files in common: the audit and `ci/image/command-table.json`.
- All six gitlinks are the same on both parents and at the head.

**2. Audit regeneration: PASS.**

- `--check` gives rc 0 in this clone and in a clone with unpopulated submodules.
- `--write` in the disposable clone reproduces blob `fd7e9edf`, sha256 `f1b9f3c0...`, byte for byte (`receipts/03_regen_and_differential.txt`).
- An independent read finds 214 rows for a population of 214, with none missing, extra or duplicated (`receipts/07_audit_rows.txt`).
- That read reproduces the status totals of 177, 16, 0 and 21, and every lane row.
- No table has a `Lines` column, and no inventory cell is a bare number.
- The remaining "line" text is the page's fixed prose and the recorded citations in the data file, not computed counts. The page has 76 Findings rows.

**3. Command table: PASS, with one item open.**

- A three-way compare of 2582 leaves against dev finds 0 mismatches (`receipts/04_command_table_threeway.txt`).
- The head carries `docs_inventory.py` at `092505ae`, the three #842 digests (`fw_service_budget/run.py`, `nvm_capture_cpu/run.py`, `nvm_capture_cpu/soc.py`) and the #842 MAC row `0x024b4c4b4c01`.
- The MAC row matches `tb/verilator/milan_dp/Makefile:597`, and the old row is gone from both.
- All four moved digests match their blobs (`receipts/05a_digests.txt`).
- `scripts/ci_differential.py --check` passes: 224 fixtures, 185 census shapes.
- `ci_tool_inventory.py --check` refuses here because `CI_IMAGE_SHFMT` is not set. That is the open item listed under pending manager duties, not a finding.

**4. #842 pages in the #849 generator: PASS except F1.** All eight changed or added pages have rows, and the rows follow the generator's rules. For the new page, these fields check out by independent reading (`receipts/10_new_page_row.txt`):

- Audience: `integrator`, through the `docs/reference/.*` rule.
- Lane: `reference`.
- Cited paths: `sw/builder`, `configs`, `sw/firmware/milan_baremetal`.
- Standards: Milan v1.2, 1722.1-2021, 802.1AS, 802.1BA. It has no 1722-2016 or 802.1Q citation.
- Area count: the `docs/reference` section has 11 rows, matching `(11)`.

The `Verified` cell is the one that fails.

**#848 acceptance on the merged tree: holds** (`receipts/08_probes.txt`). All eight probes behaved as required:

| Probe | rc |
|---|---:|
| Untouched head | 0 |
| A line added to the new page | 0 |
| A line added to every tracked page | 0 |
| Title changed | 1 |
| Supersession banner added (status change) | 1 |
| Page removed | 1 |
| Tracked page added | 1 |
| The pre-regeneration audit from `a578ceb5` | 1 |

## Findings

### R787-4-F1 - MINOR - Conformance, Robustness, Docs

**Where:** `docs/DOCUMENTATION_AUDIT.md:23`, `:43` and `:314`; rule at `scripts/docs_inventory.py:97` and `:492-493`.

**Evidence:**
- Line 23 says "Statements on D0 pages were checked at dev `1e80128f`." Line 24 says "Other pages wait for their area lane."
- Line 314 gives the new page `D0`. Line 43 gives the reference lane 19, up from 18.
- `git cat-file -e 1e80128f:docs/reference/STRICTER_READINGS.md` fails. Commit `1e80128f` is dated 2026-10-29, and the page arrived in `7c4f61b4` on 2026-11-05.
- `D0` is assigned by a path pattern alone, so a page added after the baseline inherits it.
- Every other D0-class page at dev exists at `1e80128f`, so this is the first page that makes the claim false.
- #797 item 2 defines that step as checking each normative or numeric statement against source. The new page carries clause readings that this check never covered.

**Impact:** The audit's purpose is to show which pages have been verified. A reader is told a register of clause readings was checked statement by statement, and it is not listed as waiting for its area lane. Its status of `current` is not affected. Later pages under `docs/guides`, `docs/integration` or `docs/reference` will repeat this.

**Required outcome:** The page makes no D0 claim for a page absent from `verified_at`, in both the row and the lane figure, or a public manager ruling places the fix elsewhere.

**Sizing, not a prescribed design:** a disposable one-line narrowing of `RELEASE_FACING` keeps the module at 1000 lines. It changes 2 audit lines (19 to 18, `D0` to `area lane`), and `--check` and all 56 selftest controls pass (`receipts/11_sizing_probe.txt`). A generator change also needs a digest re-pin. A rule that handles later pages, not just this one, is the better fix.

**Verification:** `--write` then `--check` at the new head, and a control where a page absent from the baseline does not render `D0`.

### R787-4-S1 - SUGGESTION - Tests

**Where:** `ci/image/command-table.json`, `scripts` section; enforcement at `scripts/ci_command_table.py:219`.

**Evidence:** Of 151 entries, 112 match their blobs, 38 differ, and `tb/verilator/render_setpoint/mutants.py` is not in the tree. The sets are identical at dev, both parents and the head (`receipts/05a_digests.txt`), so this merge did not introduce them. The digest is compared only when the audit walk reaches a script.

**Impact:** "The table pins each script" is true only for scripts the walk reaches. I did not establish why those entries differ, or whether any of them is reached.

**Required outcome:** Optional. A separate issue could prune or refresh the entries. It does not affect this PR.

### R787-4-R1 - RESIDUE - Docs

**Where:** PR #849 body, line 17 and the Validation section at line 97.

**Exact fix:** Change "546 lines" to "547 lines". Say the sync also adds the new page's row. Name the current head in the Validation section, or mark that section as `171fd56b` evidence.

### R787-4-R2 - RESIDUE - Docs

**Where:** `review-evidence/848-r1/author-r4/manager-sync-gates.txt`, line 3.

**Exact fix:** Label the line as the parents of `a578ceb5`. The head's single parent is `a578ceb5`.

## Prior findings

`scripts/docs_inventory.py`, `scripts/docs_inventory.json` and `.github/ci-templates/docs.yml` are byte-identical to `171fd56b`, so each disposition below stands unless this delta changes what it depends on.

| Finding | State at this head |
|---|---|
| R787-1-F1 to F4, R788-1 F1 | RESOLVED. Closed at `171fd56b`. The code is unchanged, the selftest passes 56 controls, and the page's route text is at audit lines 465-468. |
| R787-1-F5, R788-1 F4 | RESOLVED. The docstring reads "No computed line count or number reaches the page". |
| R787-2-F1, F2, R788-2 F1, F2 | RESOLVED. Closed at `171fd56b`, code unchanged. |
| R788-2 R1, R2 | RESOLVED. PR body lines 43 and 115 now state the corrected text. |
| R787-1-S1 = R787-2-S1 = R788-2 S5 = R788-3 S7 | RETAINED SUGGESTION. Generator unchanged. |
| R787-2-S2 = R788-2 S1 = R788-3 S3 | RETAINED SUGGESTION. |
| R788-2 S2 = R788-3 S4 | RETAINED SUGGESTION. |
| R787-2-S3 remainder = R788-3 S5 | RETAINED SUGGESTION. |
| R787-2-S4 = R788-2 S4 = R788-3 S6 | RETAINED SUGGESTION. |
| R787-3-S1 to S4, R788-3 S1, S2 | RETAINED SUGGESTION. |
| R787-3-R1, R788-3 R1 | RETAINED RESIDUE. PR body line 41 still reads wider than the control. |
| R787-3-R2 | RETAINED RESIDUE. `W8` still names two mutants, at PR body lines 52 and 83. |

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #848 acceptance via `receipts/08_probes.txt`; #797 item 2 against audit lines 23, 43, 314 | R787-4 | `9d5a5af78f95f655e5104056c2c0ee2cca689279` |
| RTL | CLEAN | `receipts/12_restore.txt`: 0 delta files under `hdl`, `syn` or the submodule roots; gitlinks unchanged | R787-4 | `9d5a5af78f95f655e5104056c2c0ee2cca689279` |
| Robustness | UNCLEAN (F1) | `scripts/docs_inventory.py:97`, `:492-493`; `--check` with submodules unpopulated; page-set and status probes | R787-4 | `9d5a5af78f95f655e5104056c2c0ee2cca689279` |
| Tests | CLEAN | `--selftest`, 56 controls (`receipts/06_selftest.txt`); `ci_differential.py --check`; `check_doc_style.py --selftest`; the eight probes | R787-4 | `9d5a5af78f95f655e5104056c2c0ee2cca689279` |
| Docs | UNCLEAN (F1) | Audit at the head, 214 rows and 76 findings; `check_doc_style.py`; `DOC_MAP.gen.py --check`; PR body | R787-4 | `9d5a5af78f95f655e5104056c2c0ee2cca689279` |

## Real limits

- This is a delta review. The content of #842 was not reviewed, and neither were the comments in its files. The only new text checked against the comment rule is the audit delta, which has no instance.
- `scripts/check_em_dash.py` could not run here because its pinned renderer is missing (rc 2). The added audit lines contain no em dash, by direct search.
- `ci_tool_inventory.py --check` was refused for lack of `CI_IMAGE_SHFMT`, and `gate_25_0` was not run.
- Author evidence at `40c2814a` was spot-checked: the two `author-r4` receipts are listed in `MANIFEST.json` by hash, and their figures match this round's own runs. Its `docs_check` line was not reproduced here.
- Hosted runs: all six check runs at this head were still queued, so no hosted job has executed.
- Physical calibration was NOT RUN, and no hardware claim is made.
- This round ran no manager source bank and infers none.

## Pending manager duties

- Rule on F1, as described under Verdict.
- Run act at this head, which covers `gate_25_0` and the tool-inventory self-test with `CI_IMAGE_SHFMT`. This is open, not a finding.
- Accept hosted results once the queued runs finish.
- Build and validate the current-dev merge candidate at the merge turn, and link its receipts on the PR.
- Carry R787-4-R1, R787-4-R2 and the retained RESIDUE items to the residue checklist.

## Restoration

No probe touched this clone. All writes went to the disposable clone. Worktree and index equal the head, `git status` is empty, and all six gitlinks are at their required commits (`receipts/12_restore.txt`).

R787-4 FINISHED
