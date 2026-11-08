[R754] POSITIVE - exact head 06c89f1d48c73ec1977791f2a2c4f99579ae4853

Round R754-8, external cleared-context review of PR #825 (issue #797, register reference). Exact head `06c89f1d48c73ec1977791f2a2c4f99579ae4853`, tree `40c99b22fcee5e4b9e182bef92c3512485d66168`. Previously reviewed head `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` (R754-7 POSITIVE; R753-7 NEGATIVE on F1, MINOR, Conformance and Docs). Source base `1e80128f`; live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`, which is the head's single merge base.

**Why POSITIVE:** the one commit of this round does what R753-7 F1's option (a) asks, and F1's verification holds exactly as written. `scripts/docs_inventory.json` loses 15 whole entries and nothing else. `docs/DOCUMENTATION_AUDIT.md` is the generator's byte-exact output for that data file. Both reference pages stay `stale` only through D0-057 and D0-040, which are correctly kept for their copy rows. The PR body's "Fixed" sentence now agrees with the ledger. No BLOCKER, MAJOR or MINOR is open.

## Scope and method

1. Read AGENTS.md (sections 3, 6 and 7), the inventory rule in `scripts/docs_inventory.py:22-43`, and the PR body's Description and Round 8 sections.
2. Ran my own pass over `git diff 1de759d3..06c89f1d` and the gates. My own probes ran on disposable `git archive` copies of the head, under the packet's `scratch/`.
3. Verified the author's round-8 receipts at evidence commit `d0fabcdc` (`review-evidence/797r1-r1/author-r8`).
4. Only then read the prior public reports: R753-7 (comment 6720354516) and my own R754-7 (6720338707). I did not read any report at this head by another reviewer.

Token economy: code that the delta does not touch keeps its R754-7 verdict, because nothing it depends on changed (see the RTL row).

## The delta (one commit, `06c89f1d`, parent `1de759d3`)

`git diff --stat`: `scripts/docs_inventory.json` has 111 deletions, and `docs/DOCUMENTATION_AUDIT.md` has 2 insertions and 17 deletions. The subject is one line with no body and no trailer. `git diff --check 1de759d3 HEAD` gives rc 0 (`receipts/commit_and_diffcheck.txt`).

Checked with `scripts/inventory_delta.py` (`receipts/inventory_delta.txt`):

- The `verified_at`, `cited_at`, `verified_pages` and `judged` keys are unchanged.
- Findings go from 65 to 50. Nothing is added. The 50 kept entries are byte-identical and in the same order.
- Removed, exactly: D0-006, -007, -008, -014, -015, -016, -017 and -058, -059, -060 on `REGISTER_MAP.md`, plus D0-018 and -041 to -044 on `REGISTER_MAP_CLASSES.md`. These are R753-7's 14 plus D0-018. All are on the two register pages.
- No entry of a removed ID is left in the data file, and no audit line names one. `git grep -w` finds no file in the tree that names one (`receipts/tree_names_and_copies.txt`).
- Every Findings row of a non-removed ID is identical before and after the change. No copy row was lost (`receipts/old_audit_rows_of_removed.txt`).

## R753-7 F1: its verification, item by item

| Verification as written | Result at `06c89f1d` | Receipt |
|---|---|---|
| `docs_inventory.py --check` rc 0 | rc 0, "OK (533 lines, docs/DOCUMENTATION_AUDIT.md is fresh)" | `receipts/gate_rc.txt`, `receipts/inventory_check.log` |
| `docs_inventory.py --selftest` rc 0 | rc 0, "OK (60 controls)" | `receipts/inventory_selftest.log` |
| "re-verify: quote not found" count drops by the removed entries | 19 to 5 overall; 16 to 2 on the two pages (11 to 1 on `REGISTER_MAP.md`, 5 to 1 on `REGISTER_MAP_CLASSES.md`). The drop of 14 is the removed entries that rendered re-verify. D0-018 rendered "on page" | `receipts/inventory_delta.txt` |
| No row of a removed ID remains | 0 audit lines and 0 data entries for all 15 | `receipts/inventory_delta.txt` |
| Each page is stale only through D0-040 or D0-057 | `REGISTER_MAP.md`: `stale`, "1 finding(s): D0-057". `REGISTER_MAP_CLASSES.md`: `stale`, "1 finding(s): D0-040" (`DOCUMENTATION_AUDIT.md:313-314`) | delta above |
| The PR body's "Fixed" sentence matches the ledger | Yes. It lists D0-006 to -008, -014 to -018, -040 to -044 and -057 to -060 as fixed on the pages. The 15 removed are listed. D0-040 and D0-057 are named as kept, with copies on four and seven other pages. D0-009 is no longer claimed, and the body points to dev `859ab22a`, which dropped it. | see the checks below |

Further checks behind those rows:

- **The removed statements are really gone everywhere.** `scripts/removed_quote_sweep.py` imports the generator's own `flatten` and `carried_line` normalisation and searches all 215 tracked Markdown files for each removed quote and `also` spelling (`receipts/removed_quote_sweep.txt`). Thirteen of the fifteen are found nowhere. There are two hits:
  - D0-018's anchor row `0x7C8–0x7D4` is still on the classes page. That is by design: the finding was a missing row, and its correction, the `0x7D8` ETH_GUARD row with class **needed**, is at `REGISTER_MAP_CLASSES.md:102`.
  - D0-058's statement and its `also` spelling are on four `docs/history/v1/` pages. Each of those pages carries a retained D0-040 copy row (`DOCUMENTATION_AUDIT.md:487-488`, `:491-492`) for the same "Nothing in this device persists a binding across a power cycle" statement. That is why D0-058 had no copy row of its own at `1de759d3`: `copies()` (`docs_inventory.py:396-416`) suppresses a copy that a row on the page already holds. Removing D0-058 therefore leaves no copy untracked.
- **The corrections are on the pages** (`receipts/page_fix_spotcheck.txt`):
  - D0-006: 35.2.2.7.2 (Table 35-3) at `REGISTER_MAP.md:1769`.
  - D0-007/-008: IEEE 1722.1-2021 Table 7-156 and Milan Table 5.6 at `:1957`.
  - D0-014/-016: the `0x7D8` ETH_GUARD section at `:3148-3191`.
  - D0-015: PHY_RESET is inert, and `milan_mac_phy_crg_reset` resets the PHY (`:561`, `:4503`).
  - D0-017: MAC_STATUS reset at `:408` and `:495`.
  - D0-060: one AAF stream, while the 8x8 config declares eight (`:3357`).
  - D0-041: the bare-metal firmware writes these at every boot (`REGISTER_MAP_CLASSES.md:84`).
  - D0-042: `0x4xx` is write-only scratch (`:83`).
- **Copy counts claimed in the PR body.** D0-040 has 5 rows, 4 of them copies. D0-057 has 8 rows, 7 of them copies (`receipts/tree_names_and_copies.txt`).
- **D0-009 provenance.** `859ab22a` is an ancestor of dev `0a75aa77` and is outside the lane range `0a75aa77..HEAD`. Its subject says it drops D0-009.
- **Kept D0-057's source pointer.** It cites "`REGISTER_MAP.md` lines 351-356", which on the generated page is now IRQ_STATUS. The audit states that findings cite lines at dev `cited_at` = `1f29f189` (`docs_inventory.py:573`). At that commit's page the 0x0053 note is at those lines, so this is not a defect.

## Probes (disposable copies, restored; `scripts/mutation_probe.sh`, `receipts/mutation_probe.txt`)

| Probe | Expected | Got |
|---|---|---|
| M0: pristine copy, `--check` | 0 | 0 |
| M1: round-7 data file with the head page | 1 | 1 |
| M2: `--write` with the round-7 data file | page == `1de759d3`'s page | byte-identical |
| M3: `--write` with the head data file | page == head page | byte-identical, so the audit is the generator's output |
| M4: also drop the kept D0-040, then `--write` | its 5 rows vanish | 0 rows (head has 5), which shows why D0-040 must stay |
| D0-018 restored alone, `--check` | 1 | 1 (replays the author's P3) |
| D0-040 dropped, `--check` | 1 | 1 (replays the author's P4) |
| M5b: D0-006's wrong text re-added to `REGISTER_MAP.md` with head data, inventory `--check` | (characterisation) | 0, see limits |

## Author receipts (evidence commit `d0fabcdc`)

- `receipts/INDEX.md`: all 196 rows match their files' size and sha256. No file is unindexed, and none is missing (`scripts/verify_receipt_index.py`, `receipts/author_r8_index_verify.txt`). The evidence commit itself is unsigned (GitHub `verification.verified=false`), so the integrity check is the index hashes, not a signature.
- `HEAD.txt` is the exact head.
- Lane gates: `docs_inventory_check`, `docs_inventory_selftest`, `doc_style` and the three `diff_check` runs are all rc 0.
- Plants: P0-P7 are all as expected. P1-P6 exit 1, and P0 and P7 exit 0.
- `docs.yml`: 66 steps ran with rc 0. 31 are hosted-only and not run, each with a stated reason. `verify_docs_yml.rc=0`. All four job clones show head `06c89f1d` and a clean status after the run. The register reference gate is `docs-gates-0__gate_51`, rc 0.
- The HANDOFF numbers (65 to 50; 19 to 5; 16 to 2; copies 4 and 7; only the `reference` area changes) agree with my own receipts.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding is raised at this head. The delta adds no source comment: it is a JSON data file and a generated page. So the comment rule is not engaged, and there is no new lane, round, reviewer or comment-ID label in source.

## Prior public review findings at this head

| Prior item | State at `06c89f1d` | Evidence |
|---|---|---|
| R753-7 F1 (MINOR; Conformance, Docs) | **Resolved**, option (a) | every verification row above |
| R754-7 S3 (SUGGESTION; Docs; D0 rows on the two pages) | **Resolved** by the same commit | `DOCUMENTATION_AUDIT.md:313-314`, `:529-530` |
| R753-7 S1 / R754-7 S1 (SUGGESTION; extract staleness not gated) | Retained, optional (not taken, as the PR body says) | `scripts/register_map_soc.json` and `gen_register_reference.py` untouched by the delta |
| R753-7 S2 / R754-7 S2 (SUGGESTION; #839 hold only in the notes) | Retained, optional | `REGISTER_MAP.md` and `register_descriptions.json` untouched |
| R753-7 S3 (SUGGESTION; `verified_pages` keeps the rewritten page as "D0") | Retained, optional | the `verified_pages` key is unchanged (`receipts/inventory_delta.txt`) |
| R753-7 RES1 / R754-7 RES1 (merge commit `57264e30` subject) | Retained, on the residue checklist (cannot be amended) | history unchanged |
| R754-7 RES2 (`author-r7/HANDOFF.md` gate table row) | Retained, on the residue checklist | the round-7 evidence file is unchanged |
| R753-6 S1, S2; R754-6 S1, S2; R753-5 S1; R754-4 S1, S2 (SUGGESTION) | Retained, optional | `register_read_sweep.py`, `register_sv.py`, `register_descriptions.json` and `REGISTER_MAP.md` untouched |
| R753-3 RES2 (`REGISTER_MAP.md:4503`), R753-3 RES3 (`CSR_REGISTER_NOTES.md:974`), R754-3 R1 (`CSR_REGISTER_NOTES.md:78`) | Retained, on the residue checklist | files untouched by the delta |

No prior BLOCKER, MAJOR or MINOR is reopened.

## Lens results

```text
[R754] PASS Conformance - scripts/docs_inventory.json (15 removed, 50 kept byte-identical), docs/DOCUMENTATION_AUDIT.md:313-314 and :529-530, scripts/docs_inventory.py:25-28 - F1 option (a) and the lane-removal rule checked: each removed entry had no copy row, each correction is on its page (page_fix_spotcheck), D0-040/D0-057 kept for 4/7 copies
[R754] PASS RTL - git diff 1de759d3..06c89f1d (2 files: a data file and a generated page; 0 files under hdl/, configs/, sw/) - inapplicable by artifact; the R754-7 RTL verdict at 1de759d3 stands, since nothing it depends on changed
[R754] PASS Robustness - scripts/docs_inventory.py:396-416 copies() suppression traced for D0-058; removed_quote_sweep (215 pages, generator normalisation); probes M1, M4, D0-018-alone and D0-040-dropped fail closed - no removed statement survives untracked
[R754] PASS Tests - docs_inventory.py --check rc 0 and --selftest 60 controls rc 0 at the head; M2/M3 show the page is the generator's byte-exact output; author plants P0-P7 and docs.yml (66 rc 0, 31 stated not-run), verified through 196/196 index hashes
[R754] PASS Docs - PR #825 body Description "Fixed on" sentence and its D0 ledger bullets, Round 8 table; author-r8 HANDOFF.md - checked against the regenerated audit (copy counts 4/7, D0-009 at dev 859ab22a, the stale cells); check_doc_style.py rc 0 (25 current documents)
```

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `scripts/docs_inventory.json` delta; `DOCUMENTATION_AUDIT.md:313-314`, `:529-530`; `docs_inventory.py:22-28`; corrections at `REGISTER_MAP.md:408,495,561,1769,1957,3148-3191,3357,4503` and `REGISTER_MAP_CLASSES.md:83,84,102` | R754-8 | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |
| RTL | CLEAN | The delta touches no `hdl/`, `configs/` or `sw/` file. The R754-7 basis (lane patch has no RTL; `milan_csr` fingerprint fresh) is unchanged | R754-8 (the R754-7 basis at `1de759d3`, an ancestor with nothing in scope touched) | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |
| Robustness | CLEAN | `copies()` suppression, the removed-quote sweep, probes M1/M4/D0-018/D0-040, `receipts/mutation_probe.txt` | R754-8 | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |
| Tests | CLEAN | inventory `--check`/`--selftest`; M2/M3 regeneration identity; author plants and `docs.yml` receipts (index-verified) | R754-8 | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |
| Docs | CLEAN | PR body Description and Round 8; `author-r8/HANDOFF.md`; regenerated audit; doc-style gate | R754-8 | `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |

## Real limits

- `gen_register_reference.py --check` did not run here: rc 2, because the pinned `wavedrom` package is absent on this host and shared installs are not allowed (`receipts/gen_register_reference_check.log`). The delta changes no generator input. The author's `docs-gates-0__gate_51` (rc 0) and plants P6/P7 cover it, and R754-7 ran it fresh at `1de759d3`.
- By design, the inventory gate does not watch a removed entry's statement. Probe M5b re-added D0-006's wrong text to `REGISTER_MAP.md` and the inventory `--check` stayed 0. On the generated page, the register freshness gate catches a hand edit (author P6). On the hand-written `REGISTER_MAP_CLASSES.md`, nothing would catch a re-introduced statement. This follows from #815's design ("the gate ties the inventory to the files, not every sentence to its source", `docs_inventory.py:37-40`). It is not a defect of this PR.
- Exact-head hosted run 42476866170 is not green. `elaborate-gates-0` failed at step 8, "Install the pinned sv2v release" (exit code 22, a download step). Fail-fast then cancelled 43 jobs, including `docs-gates-0` and `rtl-fast`. `docs-check` failed at "Require every gate exactly once" as a consequence, and the `verilator-suites`, `yosys-portability`, Union and `elaborate` aggregates failed. Jobs that completed with success: `docs-check-no-git`, `wire-accountability`, `bdd-conformance`, `changes` and `full-ci-gate`. "Physical gPTP" was skipped (`receipts/hosted_checkruns_summary.txt`). This is not evidence for or against the delta. Hosted acceptance belongs to the manager.
- No manager source bank ran at this head, and none is claimed. No Verilator, Yosys, builder, Vivado or hardware run was made. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Re-run the hosted contexts at the exact head after the sv2v download failure. Confirm `rtl-fast`, `docs-gates-0/1/2`, `docs-check`, `verilator-suites` and `yosys-portability` on `06c89f1d`.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, against live dev `0a75aa77` or its successor, and link the receipts on the PR.
- Carry the retained RESIDUE items (R753-7 RES1 / R754-7 RES1, R754-7 RES2, R753-3 RES2 and RES3, R754-3 R1) on the residue checklist.
- Get explicit maintainer authorization before any merge.

## Clone restoration

The clone was never modified. Probes ran on `git archive` copies under the packet's `scratch/`. HEAD `06c89f1d…`, `git write-tree` = `40c99b22…`, worktree == index == HEAD, 0 status entries, 0 untracked. All 6 gitlinks are identical in HEAD and the index (`receipts/clone_restoration.txt`).

R754-8 FINISHED
