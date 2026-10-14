[R592] POSITIVE - exact head 7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0

# R592-6: internal review of PR #713 (issue #640, Mark II lane M7), round 6

- Exact head `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0`, tree `540ed6c59e0004185e682f28be9bb5b42e584f09`.
- Donor `gptp-processor` gitlink `e4869fd0c42889b2ac806587cc5c78afb1c33461`, unchanged.
- Scope: the round-6 delta `4c5d70b5..7fb3664b`, one commit (`7fb3664b9`, one-line message, no trailers).
- Authority: the round-6 ruling ([issue #640 comment 6164557611](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6164557611)), answering R592-5 ([PR #713 comment 6164547737](https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6164547737)).
- Earlier rounds stand for every artifact this delta does not touch.

## Summary

- **R592-5-F1 (MINOR, Docs) is resolved.** `docs/testing/CI_WORKFLOWS.md:1321-1322` now says "passing `--expect` the worker matrix size, six for Verilator and four for Yosys". That matches `.github/workflows/rtl.yml:426` (`--expect 6`) and `:602` (`--expect 4`), and the shard lists and `total` values at `rtl.yml:161-162,463-464`. No literal `` `--expect N` `` figure remains on the page.
- **R592-5-S1 (SUGGESTION) was applied.** `CI_WORKFLOWS.md:1337-1338` now reads "a matrix of seven and a stale total of six ... shard 6/7's". That matches `_m_shard_denominator_stale` (`scripts/ci_events.py:5256-5263`): it starts from six shards, restates the total as `"6"`, and appends shard index 6.
- **The delta is exactly one documentation file**, 3 insertions and 3 deletions, mode `100644`. No gitlink changed, and the donor is still `e4869fd0`.
- **R593-4-D1 (RESIDUE) is resolved as written.** All three of its exact phrases are now in the PR body.
- **R592-6-D1 (RESIDUE, Docs) is new.** The edited PR body still calls `7fb3664b` local and unpushed, but it is now the published PR head. This is wording only, and the exact fix is below.
- **No MINOR, MAJOR or BLOCKER is open.** All five lenses are clean at this head, so the verdict is POSITIVE.

## Independent executions at this head

All commands ran in the foreground on the exact-head clone. Receipts are under `receipts/`, and the portable script is under `scripts/`.

| What | Result | Receipt |
|---|---|---|
| `python3 -I scripts/docs_check.py` | rc 0. 0 findings across 207 md files and 1299 scrubbed text files | `receipts/docs_check.log` |
| `python3 -I scripts/ci_events.py --check` | rc 0. `OK (2175 contract item(s) across 4 workflow files and docs/testing/CI_WORKFLOWS.md)` | `receipts/ci_events_check.log` |
| `python3 -I scripts/check_doc_style.py` | rc 0. `documentation style: OK (22 current documents)` | `receipts/check_doc_style.log` |
| `python3 -I scripts/ci_events.py --selftest` | rc 0, `PASS (2175 contract items, 3096 arms)`. This includes `ok caught: O9 verilator matrix grows, the denominator is a literal`, the fixture the documentation example describes | `receipts/ci_events_selftest.log` |
| `scripts/compare_counts.py` on the head | rc 0, `AGREE` | `receipts/compare_counts.log` |
| `scripts/compare_counts.py` on the `4c5d70b5` files (negative control) | rc 1, `DISAGREE`. It finds `` `--expect 5` `` and the five/four example, so the script detects the defect it checks for | `receipts/compare_counts.log` |
| `grep -n -- --expect docs/testing/CI_WORKFLOWS.md` | Lines 537, 806, 1185-1186, 1321, 1327 and 1335. Only 537 (`--expect-suite-root`, which matches `rtl.yml:379`) carries a value. The rest name the flag generically, and 1321-1322 give six and four in words | this report; `receipts/compare_counts.log` |
| `git diff --stat --raw 4c5d70b5..7fb3664b` | One file, `docs/testing/CI_WORKFLOWS.md`, mode `100644` to `100644`, `3 +++---` | `receipts/delta-stat.txt` |
| Clone identity, read before and after the work | Unchanged both times: HEAD, tree and `write-tree` are `7fb3664b` / `540ed6c5`; the worktree is clean; 0 blob mismatches; modes are 1275 × 100644, 48 × 100755 and 6 × 160000 | `receipts/identity.log` |

**Submodule gitlinks:**
- `gptp-processor` `e4869fd0`, `protocol-processor` `2ad2f845`, `tsn-c-stack` `70936b77`, `verilog-axis` `48ff7a7e` and `lwSRP` `08ee86e8` all match their checkouts.
- `external` (`efeb541a`) is not initialized; its index entry was checked instead.

The negative control read only blobs extracted with `git archive` into the disposable `scratch/`. Nothing in the clone was edited.

## Hosted evidence at this exact head (read, not owned)

**Run and tree.**
- The `docs` workflow run `38538854496` (`pull_request`, `head_sha` `7fb3664b`) succeeded.
- Its `docs-check` job `115768354809` ran from 08:57:42 to 09:31:51 UTC, and all 55 steps succeeded.
- It checked out GitHub's merge `2d3f68ef648b90bf528dd90cd4b4f04a0fc0e75d`, whose parents are dev `fa820988` and this head.
- That merge's tree is `540ed6c5`, the same as the head tree, because dev `fa820988` is already an ancestor of the head. The checks therefore ran on exactly the head's bytes.

**Job log (excerpt in `receipts/hosted-docs-check-excerpt.txt`).**
- `docs_check: 0 finding(s) across 207 md files + 1299 scrubbed text files`.
- `documentation style: OK (22 current documents)`.
- `ci_events: OK (2175 contract item(s) ...)`.

**Other contexts, read at 09:33 UTC.**
- Complete with success:
  - `docs-check-no-git`;
  - `rtl-fast` and `elaborate`;
  - `changes` and `full-ci-gate`;
  - `verilator-lint` and `yosys-elaboration`;
  - Yosys shards 0/4 to 3/4;
  - the six firmware jobs;
  - `publication-census`, `wire-accountability` and `bdd-conformance`.
- Still running: Verilator shards 0/6 to 5/6, so `verilator-suites` had not run yet.
- `Physical gPTP (nightly and manual)` is skipped by design. That is not evidence.

Full table: `receipts/hosted-check-runs.tsv`. Acceptance of hosted results belongs to the manager.

## Findings

### R592-6-D1: RESIDUE (Docs). The PR #713 body calls the published head `7fb3664b` local and unpushed

- **Location** (excerpt in `receipts/prbody-excerpt.txt`):
  - Status: "Published parent: `4c5d70b5…`" and "Round 6's local continuation is listed below, pending publication and review."
  - How to get into the same state: "The Round 6 continuation remains local until publication."
  - Round 6: "Parent continuation: `7fb3664b…` (local, unpushed)" and "The status separates the published revisions from this local continuation."
- **Evidence:** `gh pr view 713` reports `headRefOid` `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0`, and hosted runs executed on it (`receipts/pr713.json`).
- **Why it is RESIDUE:** the wording only describes publication state, which went stale when the head was pushed after the body was written. It changes no measurement, figure, verdict, test, code, generated artifact or clause claim, and it touches no privacy rule. The Round 6 section names the correct SHA.
- **Exact fix:**
  - Status: replace "Published parent: `4c5d70b5…`" with "Published parent: `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0` (PR head; Round 6)". Delete "Round 6's local continuation is listed below, pending publication and review."
  - How to get into the same state: delete "The Round 6 continuation remains local until publication."
  - Round 6: replace "(local, unpushed)" with "(published PR head)". Replace "The status separates the published revisions from this local continuation." with "The status lists the published parent and donor."
- **Verification:** read the corrected body against `headRefOid`.
- **Owner:** the manager carries this item to the residue checklist.

## Prior public review findings at this head (read after this round's own pass)

| Finding | Status at `7fb3664b` | Evidence |
|---|---|---|
| R592-5-F1 MINOR (Docs): `--expect 5` at `CI_WORKFLOWS.md:1322` | **Resolved** | `:1321-1322` gives six and four in words, the same as `rtl.yml:426,602`. `compare_counts.py` agrees at the head and disagrees at the base |
| R592-5-S1 SUGGESTION (Docs): five-worker stale-denominator example | **Applied** | `:1337-1338` gives seven, six and 6/7, matching `ci_events.py:5256-5263`. The selftest arm is caught |
| R593-4-D1 RESIDUE (Docs): PR body local-only wording | **Resolved as written** | All three phrases are present: "REVIEW READY at the published parent and donor revisions listed above", "Check out the published parent revision and initialize its pinned submodules", and the no-push sentence qualified as implementation-stage history. Its new form at this head is R592-6-D1 |
| R592-4-S1 SUGGESTION: inert ROM-ledger row | Retained (optional, declined) | `syn/yosys/rom_digests.tsv` is outside the delta |
| R592-3-RES1, R592-3-RES2, R593-3-R-01 RESIDUEs | Retained, carried | Their files are outside the delta, so the exact fixes already published still stand |
| R593-3-S-01, R592-2-S1, R593-1-S-03 SUGGESTIONs | Retained, optional | Their artifacts are outside the delta |

## Lens results

```text
[R592] PASS Conformance - docs/testing/CI_WORKFLOWS.md:1321-1322,1337-1338; .github/workflows/rtl.yml:161-162,426,463-464,602; ruling 6164557611 items 1-4 - the verifier figure states six/four in words as item 1 allows, grep agrees with rtl.yml, the optional example matches the O9 fixture, the delta is one docs file, and the three gates return rc 0 locally and in hosted docs-check job 115768354809
[R592] PASS RTL - receipts/delta-stat.txt (git diff --raw 4c5d70b5..7fb3664b: one .md file, no hdl, tb, syn or gitlink path); receipts/identity.log (donor e4869fd0) - nothing in RTL scope changed, so RTL content coverage from R592-4 at the same donor still stands
[R592] PASS Robustness - scripts/ci_events.py:5256-5263 and receipts/ci_events_selftest.log (O9 arm caught, 3096 arms); receipts/delta-stat.txt - the delta changes no fail-closed path, and the stale-denominator refusal that the documentation now describes is exercised and caught at this head
[R592] PASS Tests - receipts/delta-stat.txt (no test or fixture changed); receipts/ci_events_selftest.log; receipts/compare_counts.log (the head agrees, and the base control is refused) - the existing contract tests stay green, and the documentation example is tied to the live fixture by an executed check that can fail
[R592] PASS Docs - docs/testing/CI_WORKFLOWS.md full-page grep for --expect and worker counts; PR #713 body (receipts/prbody-excerpt.txt); hosted docs-check run 38538854496 - R592-5-F1 is fixed, S1 is applied and R593-4-D1 is applied; R592-6-D1 is RESIDUE (wording only) and is carried
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6164557611 items 1-4; `CI_WORKFLOWS.md:1321-1322,1337-1338`; `rtl.yml:161-162,426,463-464,602`; the three gates run locally and in hosted `docs-check` | R592-6 (delta); R592-5 for the unchanged selector, matrix and contract | `7fb3664b` (the R592-5 artifacts are unchanged since `4c5d70b5`) |
| RTL | CLEAN | Delta path list (docs only); gitlinks; donor `e4869fd0` | R592-6 (delta); R592-4 (RTL content) | `7fb3664b`; RTL content at `412e3f6c`/donor `e4869fd0`, untouched since |
| Robustness | CLEAN | `ci_events.py` O9 arm and selftest; the delta changes no fail-closed path | R592-6 (delta); R592-5 (probes M1-M5, M7) | `7fb3664b` (the probe artifacts are unchanged since `4c5d70b5`) |
| Tests | CLEAN | Selftest at 3096 arms; `compare_counts.py` with its base negative control; no test changed | R592-6 | `7fb3664b` |
| Docs | CLEAN. R592-6-D1 and the earlier RESIDUEs are carried; the optional SUGGESTIONs are retained | `CI_WORKFLOWS.md` delta and full-page grep; PR body; hosted `docs-check` | R592-6 | `7fb3664b` |

## Real limits of this round

- This was a delta review only. I ran no full parent, PP, gPTP, Yosys or builder bank, and I ran no simulation; the delta contains no RTL or test change.
- No manager source bank exists at this head, and none is claimed or inferred.
- Hosted `docs-check` validated GitHub's merge `2d3f68ef` with dev `fa820988`, and that merge's tree equals the head tree. It is not the manager's current-dev candidate, which is built at the merge turn from source base `e8454e27` and live dev `fa820988`.
- When I read them, the Verilator shards at this head had not finished and `verilator-suites` had not run. I make no claim about them; the last completed Verilator evidence is R592-5's reading at tree `8156e281`.
- Physical calibration was NOT RUN. The skipped `Physical gPTP` context and any field skips are not hardware proof.
- No gate reads the counts stated in prose on the CI policy page (established in R592-5). `compare_counts.py` is review evidence only, not a repository gate.

## Pending manager and executor duties

1. Carry R592-6-D1, plus R592-3-RES1, R592-3-RES2 and R593-3-R-01, to the residue checklist.
2. Selector step 3 is still outstanding: replace the provisional 1800 s `gptp_tables` figure and the new worker's overhead with `--measure` figures from a successful hosted run, and drop the suite from `PROVISIONAL_SUITES`.
   - The PR's own Definition of Done lists this as unchecked.
   - That commit would touch `scripts/suite_shards.py`, so Conformance, Tests and Docs would need to be re-covered at that head.
3. The manager owns:
   - exact-head hosted acceptance, including the Verilator shards and `verilator-suites` at this head;
   - the current-dev candidate (builder and native banks);
   - donor-before-parent landing;
   - post-merge containment.
4. Merge also needs the external reviewer's verdict at this head and an explicit maintainer authorization.

I made no GitHub write, source fix, commit, push or merge, contacted no author, ran no container or local CI replica, and took no hardware action.

R592-6 FINISHED
