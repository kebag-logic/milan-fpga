[R741] POSITIVE - exact head 297b642f06aede7b818a5451722c75032fb05099

# R741-6: composition review of merge-train candidate for issue #797 / PR #815

Candidate `297b642f06aede7b818a5451722c75032fb05099`, tree `274a5320231c562168a58416a3a3c316ced60493`. Parents: live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6` and PR head `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63`. Scope: composition acceptance only.

The composed tree adds no defect beyond the reviewed source. No BLOCKER, MAJOR or MINOR is open. All five lenses are clean. Two wording RESIDUEs from round 5 are retained. Two retained SUGGESTIONs are recorded again with composition evidence. Earlier optional suggestions are carried unchanged.

## 1. What the composition is

| Fact | Evidence |
|---|---|
| Predecessor PRs queued in the candidate | None. The candidate is a two-parent merge of dev `e61a4afa` and PR head `e8ec8d20` (`git log -1 --format=%P`) |
| Candidate tree vs PR head tree | Identical: `274a5320` on both. `git diff --name-status e8ec8d20 297b642f` is empty (`receipts/probes/merge_structure.txt`) |
| Merge base of PR head and dev | `e61a4afa`, the only one. Dev is an ancestor of the PR head, so the candidate merge adds no bytes |
| PR files vs dev `e61a4afa` | 10 files: `.github/ci-templates/docs.yml`, `.github/workflows/docs.yml`, `ci/image/command-table.json`, `docs/DOCUMENTATION_AUDIT.md`, `docs/README.md`, `docs/guides/VERIFICATION_DEVELOPER.md`, `docs/reference/REGISTER_MAP.md`, `scripts/ci_events.py`, `scripts/docs_inventory.json`, `scripts/docs_inventory.py` |
| Files changed both by this PR and by dev since the lane's earlier base `1f29f189` | One: `docs/README.md`. Dev added the Mark II stream-engines row at line 81. The PR changed the media-clock row at line 73. The hunks don't overlap |
| Lane's dev-sync merge `b48b2fd5` | `git merge-tree --write-tree 8d8c2e36 e61a4afa` gives `f10e50b9`, which equals `b48b2fd5^{tree}`. It is a clean automatic merge with no hand resolution |
| Regeneration commit `e8ec8d20` | Changes only `docs/DOCUMENTATION_AUDIT.md` |
| Submodule gitlinks | All six are identical at `1f29f189`, `e61a4afa` and the candidate |

### Semantic interactions checked

1. **Documentation inventory and audit page.** These read every tracked page, and dev changed 26 Markdown files and added `docs/design/MARK_II_STREAM_ENGINES.md`. On the candidate, `docs_inventory.py --check` passes (213 pages, page fresh) and `--selftest` passes 50/50. Probes in a disposable clone (`receipts/probes/inventory_composition_probes.txt`) show the gate refuses each composition drift, with rc 1 for each probe:
   - the pre-sync page from `8d8c2e36` put back on the composed tree (403 lines differ);
   - dev's README row removed from the overlapping file (3 lines differ);
   - dev's new page untracked (379 lines differ).

   The baseline is rc 0 before and after the probes.
2. **Workflow step counts and CI-event contract.** Dev changed no file under `.github/` and did not change `scripts/ci_events.py` or `ci/image/command-table.json`. On the candidate:
   - `ci_events.py --check`: 2207 contract items; `--selftest`: 5270 arms. Both rc 0.
   - `ci_gate_workflows.py --check`: rc 0.
   - The docs-check step count recorded at 52 holds.
3. **Command-table digest.** `sha256sum scripts/docs_inventory.py` = `2756e5b5…459b`, which equals the `ci/image/command-table.json` entry.
4. **TOC, anchors, links and the em-dash rule.** These ran with the pinned renderer from `tools/markdown/requirements.txt`, installed in a disposable scratch venv:
   - `gen_toc.py --check`: 151 pages.
   - `--verify-anchors`: 582 cross-page fragments.
   - `--selftest`: 1501/1501.
   - `check_em_dash.py --base e61a4afa`: 0 findings over 534 added lines, 339/339 arms.
   - `docs_check.py`: 0 findings over 213 md files.
   - `check_doc_paths.py`: 1618 paths.
   - `check_doc_style.py`: OK.
   - `git diff --check e61a4afa 297b642f`: rc 0.

   Without the venv, the four renderer gates stop with rc 2 ("renderer not installed"). That is an environment gap, not a finding. Both logs are kept in `receipts/gates/`.
5. **Finding citations against dev's source changes.** Dev changed 19 non-doc files since the citation anchor `1f29f189`. Four of them are cited by findings in `scripts/docs_inventory.json`: `hdl/milan/milan_datapath.sv`, `sw/litex/milan_soc.py`, `scripts/run_litex_sims.sh` and `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv`.
   - 19 distinct "lines A-B" ranges are cited. At dev tip, 18 of them point at different content. Every cited block is still present word for word, shifted by 0 to 19 lines (`receipts/probes/cited_lines_relocation.txt`, reproduced by `scripts/cited_line_shift.py`).
   - Dev's changes in those files are the MII launch-shape parameters and observer wiring (#829). No finding is about MII, launch shape or `sink.ready`.
   - D0-015's "`milan_soc.py` never connects the datapath's `o_phy_reset_n`" still holds: `phy_reset_n` appears 0 times at both commits.
   - The page states "Findings cite source lines at dev `1f29f189`" (`docs/DOCUMENTATION_AUDIT.md:26`), so the citations are honest. The shift is recorded under S2 below.

## 2. Signed local-CI packet

Source: `review-evidence/797d0-r1/local-ci/e8ec8d20` at `8054a3fa`, copied to `receipts/local-ci/`.

| Check | Result |
|---|---|
| `manifest.json` sha256 | `de5f9acc29056164b6981883c4671abd6539bf0c3fce3c18b297a06096d927ae`, as stated |
| `allowed_signers` | One line, principal `milan-local-ci`, namespace `milan-local-ci`. Key fingerprint `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`, as required (`receipts/local-ci/verify.txt`) |
| `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` | `Good "milan-local-ci" signature`, rc 0 |
| Subject | Candidate `297b642f…`, candidate_parent `e61a4afa…`, candidate_tree `274a5320…`, head `e8ec8d20…`, head_tree `274a5320…`, PR 815, `kebag-logic/milan-fpga`. All match this review |
| Workflow definitions | The manifest's sha256 for `docs.yml`, `elaborate.yml`, `rtl-fast.yml` and `rtl.yml` (candidate and head) equals `sha256sum .github/workflows/*.yml` at the candidate. These are the only four workflow files |
| Coverage | 47 entries across docs, elaborate, rtl-fast and rtl, all `ok: true`. 46 are by act. One is `not-run`: `rtl/physical-gptp`, which runs only on schedule and dispatch events, and the manifest notes it is not hardware evidence |
| Execution | act exit 0 with 68 jobs (all success except the scheduled Physical gPTP job, which was skipped). Bank `full-native`: 5 commands, all rc 0. Bank `manager-builder`: 48 commands, all rc 0. Result `success` |

No claim in the packet needed falsifying. The composition gates I reran agree with its docs and CI-event coverage.

## 3. Hosted evidence at PR head `e8ec8d20` (inspected, not accepted)

The candidate `297b642f` is not a pushed ref, so it has no check runs (HTTP 422). The PR head has 68 check runs (`receipts/hosted_check_runs_e8ec8d20.tsv`): 25 success, 32 cancelled, 10 failure, 1 skipped.

- Every one of the 10 failures is an aggregate step refusing a cancelled leg (`receipts/hosted_failure_steps.txt`), not a content failure:
  - "Require every gate exactly once" (`docs-check`, `elaborate`);
  - "Require successful owners and every case exactly once" (six Unions);
  - shard and worker tallies (`verilator-suites`, `yosys-portability`).
- Example: `elaborate-gates-1` was running and passing tests when it was cancelled at 17:07:55Z (`receipts/hosted_elaborate-gates-1_*.log`, `##[error]The operation was canceled.` right after `PASS test_retained_cdc_storage`). Then fail-fast recorded `{"first_failure": "elaborate-gates-1", "conclusion": "cancelled"}` and the union refused it (`receipts/hosted_cancellation_order.tsv`).
- No executed hosted job failed on content.
- The required hosted contexts at the PR head are not green. Accepting them belongs to the manager (section 7).

## 4. Findings

No BLOCKER, MAJOR or MINOR.

### R1 - RESIDUE (retained from R741-5 R1 / R742-5 R1) - Docs - PR #815 body, line 16 ("Status") and the "Hosted result" bullet under "Known limitations" - the hosted statements are stale

- **Authority/evidence:** the body still reads "GREEN locally; hosted not yet run." and "Hosted result: this head has no hosted run until it is pushed". The head `e8ec8d20` was pushed and has 68 check runs (section 3).
- **Impact:** wording only. A cold reader is told no hosted run exists. No measurement, code, gate or verdict changes.
- **Required outcome, exact fix (PR body):**
  - Line 16: replace "GREEN locally; hosted not yet run." with "GREEN locally. Hosted results at `e8ec8d20` are read from its check runs; the manager owns their acceptance."
  - Bullet: replace it with "Hosted result: read from the exact-head check runs of `e8ec8d20`; local results above are not hosted evidence."
- **Verification:** read the body against `gh pr view 815 --json headRefOid` and the head's check runs.

### R2 - RESIDUE (retained from R741-4 R2 via R741-5 R2 / R742-5 R2) - Docs - `scripts/docs_inventory.py:32` - "the punctuation ending it" is wider than the code

- **Authority/evidence:** the generator is unchanged at the candidate. The docstring at `:32` still says "the punctuation ending it", but the normaliser strips only `.,;:`.
- **Impact:** wording only. No recorded statement ends in `!` or `?`.
- **Required outcome, exact fix:** "the punctuation ending it" becomes "the full stop, comma, semicolon or colon ending it". This moves the `ci/image/command-table.json` digest of `scripts/docs_inventory.py`, so it can wait for the next edit of the file.
- **Verification:** read `:32` against the normaliser, and check the command-table digest still matches.

### S1 - SUGGESTION (retained from R741-5 S1 / R742-5 S1) - Conformance, Docs - `scripts/docs_inventory.json` D0-001, D0-033, D0-056 - three entries dev has fixed remain as "re-verify: quote not found" rows

- The data file is unchanged at the candidate, so this is still optional and waits on the Mark II end-state decision named in the PR body.

### S2 - SUGGESTION (retained from R741-5 S2 / R742-5 S2, re-measured on the candidate) - Docs - `docs/DOCUMENTATION_AUDIT.md:26` and the Findings "Contradicted by" cells - line citations pinned at `1f29f189` trail the merged tree

- **Evidence:** after merge, a reader on dev who follows a line number lands 1 to 19 lines off. The content holds: the page states its anchor, and every block is still present word for word.
  - 18 of 19 cited ranges in dev-changed files point at different lines at the candidate.
  - `hdl/milan/milan_datapath.sv`: +6 lines.
  - `sw/litex/milan_soc.py`: +10 or +19 lines.
  - `scripts/run_litex_sims.sh`: +1 line.
- **Optional outcome:** when an area lane next edits the data file, re-anchor `cited_at` to a current dev commit, or render the citations as commit-pinned links.

### Carried unchanged (optional; the candidate doesn't touch them)

- R741-4 S1 / R742-4 S3 (broad `also` fragments, D0-059, D0-002).
- R741-4 S2 / R742-4 S2 (a quote that normalises to nothing is accepted).
- R741-4 S3 / R742-4 S1 (surviving self-test mutants).
- R741-4 S4 / R742-4 S4 (generator at 999 of 1,000 lines).
- R742-4 S5 (the watcher's job limit cancels healthy runs; outside this PR). Section 3's externally cancelled legs are consistent with this.
- Every earlier SUGGESTION listed by R741-5 and R742-5.

### Earlier BLOCKER, MAJOR and MINOR findings

| Prior finding | Status at this head | Basis |
|---|---|---|
| R741-3 F1 / R742-3 F1 BLOCKER, literal path fails `pp_srcs.py --check` | Stays RESOLVED | The candidate tree equals `e8ec8d20`, where both round-5 reviews recorded `pp_srcs.py --check --selftest` rc 0. No source-list file changed in the composition |
| R742-3 F2 MINOR, search misses real copies | Stays RESOLVED | Generator unchanged. Inventory `--selftest` passes 50/50 on the candidate |
| Round 1 and 2 BLOCKER, MAJOR and MINOR findings | Stay RESOLVED | None of the files they depend on differs between `e8ec8d20` and the candidate |

### Comment rule

The composition adds no source line. Scanning the PR's added code and CI comments against dev finds no bench lane label, reviewer ID, round number or comment ID. "Area lane" in `scripts/docs_inventory.py` names the inventory's lane column, an output concept, which findings and inventory artifacts may name. There is no new RESIDUE under this rule.

## 5. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The composition touches its scope only through the audit page's counts and statuses. Inventory `--check` and the three drift probes on the candidate; the citation-substance check (D0-015 `phy_reset_n`, MII-only dev diff). Otherwise covered by R741-5 and R742-5 at `e8ec8d20`, which has the same tree | R741-6 | `297b642f06aede7b818a5451722c75032fb05099` |
| RTL | CLEAN | Not touched by the composition. The PR diff against dev holds no HDL, testbench or synthesis file. Gitlinks are identical, and the dev RTL arrives through a reproduced clean merge (`merge_structure.txt`). Signed packet: Verilator, Yosys and Union act jobs plus the builder and native banks, all ok. Source RTL lens covered by R741-5 and R742-5 | R741-6 (composition), R741-5 / R742-5 (source) | `297b642f06aede7b818a5451722c75032fb05099` |
| Robustness | CLEAN | Drift probes: stale page, edited overlap file and untracked new page, each rc 1, then restored to rc 0. The single merge base, and the clean merge-tree reproduction. Generator edge cases otherwise covered by R741-5 and R742-5 | R741-6 | `297b642f06aede7b818a5451722c75032fb05099` |
| Tests | CLEAN | On the candidate: inventory `--check` and `--selftest` (50); `ci_events.py --check` and `--selftest` (5270 arms); `ci_gate_workflows.py --check`; `gen_toc.py` check, anchors and selftest (1501); `check_em_dash.py --base e61a4afa` (339 arms); `docs_check.py`; `check_doc_paths.py`; `check_doc_style.py`; `git diff --check`. The signed manifest's coverage is all ok, with digests matching the workflows | R741-6 | `297b642f06aede7b818a5451722c75032fb05099` |
| Docs | CLEAN (R1 and R2 residue, S1 and S2 optional) | The `docs/README.md` overlap hunks; `docs/DOCUMENTATION_AUDIT.md` Summary and the citation-anchor line `:26`; the TOC, anchor, em-dash and docs-check gates; the PR #815 body Status line and Known-limitations bullet | R741-6 | `297b642f06aede7b818a5451722c75032fb05099` |

Source reviews relied on for code the composition doesn't change: R741-5 (POSITIVE, `e8ec8d20`) and R742-5 (POSITIVE, `e8ec8d20`).

## 6. Real limits

- No source bank was run at this head, and none is claimed. The source-head execution evidence is the author's published gate receipts plus the manager's signed act replay of `e8ec8d20` and candidate validation.
- No Verilator, Yosys, LiteX or builder suite was rerun: the composition changes no byte relative to `e8ec8d20`, and the signed packet covers those suites.
- Physical calibration was not run. The Physical gPTP context is scheduled-only, and field skips are not hardware proof.
- The citation-shift check matches the "path lines A-B" form only. Singular "line N" citations with no path immediately before them were read by hand for D0-015 only.
- The renderer-dependent gates ran under a scratch venv with the pinned wheels (`cmarkgfm==2025.10.22`, `html5lib==1.1`) on CPython 3.14.

## 7. Pending manager duties

- Hosted acceptance at the merge candidate. The PR head's required contexts are cancelled, and their aggregates refused the cancelled legs (section 3).
- Build and validate the final current-dev candidate at the merge turn, and link its receipts on the PR.
- Apply RESIDUE R1 to the PR body, and carry R2 to the residue checklist.
- Get explicit maintainer authorization before merge, then confirm the merge lands in `dev`, post-merge containment, and the Issue's status (`Relates to #797`; this is lane D0 of a sweep, so the issue stays open).

## Receipts

Listed in `MANIFEST.sha256`:

- `receipts/local-ci/`: the signed packet and `verify.txt`.
- `receipts/gates/`: the candidate gate logs and rc files.
- `receipts/probes/`: merge structure, drift probes, citation shift and relocation, restore-adjacent checks.
- `receipts/hosted_*`: check runs, failure steps and cancellation order.
- `receipts/restore_check.txt`.
- `scripts/composition_checks.sh` and `scripts/cited_line_shift.py`.

After the probes, the review clone is at exact head `297b642f`: tree and index tree `274a5320`, no status entries (including ignored files), and the six gitlinks unchanged (`receipts/restore_check.txt`).

R741-6 FINISHED
