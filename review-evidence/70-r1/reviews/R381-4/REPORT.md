[R381] POSITIVE - exact head c08becbbfdbf622ee678d5854312c53faf805d39

# R381-4: composition review of PR #610 (issue #70 lane 0, D3 contract adoption) on the merge-train candidate

- Candidate: `c08becbbfdbf622ee678d5854312c53faf805d39`, tree `cd7ae9561bdb16aec3d422241ad8ec5de2aaf24e`.
- Parents: train `c1fa4183f99293f8ee0777cda454d9d77855ca09` (live dev `54ce8773` plus queued #593 and #75) and PR source head `6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14`.
- Verdict: **POSITIVE**. The composed tree adds no defect beyond the reviewed sources. No BLOCKER, MAJOR or MINOR finding is open. One SUGGESTION (S1) records a citation table that was already stale before this PR and the train. All five lenses are covered clean; see the ledger.
- Scope: composition acceptance only. The source content has two POSITIVE source reviews: [R380-4](https://github.com/kebag-logic/milan-fpga/pull/610#issuecomment-5865637133) at `6b76f2d8` and [R381-3](https://github.com/kebag-logic/milan-fpga/pull/610#issuecomment-5865262556) at the ancestor `816c3b74`.

## 1. Reconstruction (public state only)

I read these in order:

1. AGENTS.md and CONTRIBUTING.md: section 7 (candidate merge validation) and section 6/6.1 (docs and em-dash gates).
2. docs/README.md.
3. The issue #70 body, then the manager comments that set scope:
   - status/plan 5862191328;
   - lane-0 assignment 5862193501;
   - D3 rulings 5862405632;
   - DR2c-carrier ruling 5863247772;
   - round-4 assignment 5865266525.
4. The linked requirement text: REQ-VER-06 in REQUIREMENTS.md, and TESTING 6d.
5. The candidate diff, the history of both parents, the public evidence tree `review-evidence/70-r1` (manifest), and the hosted runs at the source head.

I read the prior review findings on this PR only after my own pass was complete (section 6).

## 2. Composition identity (receipts/01_composition.txt)

| Check | Result |
|---|---|
| Candidate tree reproduction | `git merge-tree --write-tree --merge-base=c07232228 c1fa4183 6b76f2d8` gives `cd7ae956...`, equal to the candidate tree. The merge has no conflicts, and the candidate carries no hand edits. |
| Train maps to real dev | Tree of `1304205cf` (the #582 train step) equals tree of dev `54ce8773`. Tree of `b468a56d9` equals tree of `c07232228`, the PR's source base. |
| PR change set (`c07232228..6b76f2d8`) | 5 pages: `docs/README.md` and `SAVED_STATE_{FASTCONNECT,MATERIALIZATION,SNAPSHOT_OWNERSHIP}.md` under `docs/design/`, plus `docs/integration/BAREMETAL_FIRMWARE.md`. No code, RTL, gitlink or workflow file. |
| Train change set since the source base | #582: 13 files. #593: 7 files. #75: 2 files. See the receipt. |
| Files both sides change | **Only `docs/integration/BAREMETAL_FIRMWARE.md`** (#582 and #610). This matches the manager note. The four other PR pages are byte-identical at the candidate and the source head. |
| Hunks on the shared page | #582 changes Contents and `## Build contract` (lines 19-67). #610 changes `## Saved state: the flash writer` (lines 1896-1925). The hunks are disjoint and in different H2 sections. |

## 3. Gates executed on the candidate (receipts/gates/, 27 of 27 rc 0)

All gates ran in the foreground from the candidate clone. The Python environment carried the hash-locked renderer from `tools/markdown/requirements.txt` (cmarkgfm 2025.10.22, html5lib 1.1). `run_gates.sh` reproduces the first 25 lines of `gates.tsv`; the two `check_gptp_docs.py` lines were run with the same interpreter afterwards.

| Gate | Result (log tail) |
|---|---|
| `docs_check.py` | 0 findings, 173 md + 919 scrubbed files, self-test 23/23 |
| `check_doc_paths.py` | 854 cited paths resolve |
| `check_doc_style.py` and `--selftest` | rc 0 |
| `gen_toc.py --check` | OK, 115 pages carry a contents list |
| `gen_toc.py --verify-anchors` | 232 cross-page fragment links reproduced, 0 missing |
| `gen_toc.py --selftest` | rc 0 |
| `check_em_dash.py --base c1fa4183` (the candidate's train parent) | 0 findings over 948 added lines in 5 pages, arms 339/339 |
| `check_em_dash.py --base c07232228` (the PR's source base) | 0 findings over 2444 added lines in 14 pages |
| `check_em_dash.py --selftest` | rc 0 |
| `DOC_MAP.gen.py --check` | OK |
| `check_feature_status.py` (its ledger names BAREMETAL_FIRMWARE.md) | 0 findings |
| `check_solution_docs.py` (#582 changed it) | rc 0 |
| `check_baremetal_only.py --check` and `--selftest` | rc 0 |
| `check_nvm_record_space.py` | 0 findings across 5 configs |
| `ci_scope.py --selftest` (#582 changed `GATE_READ_DOCS`) | PASS |
| `ci_events.py --check` and `--selftest` | rc 0 |
| `check_gptp_docs.py` and `--selftest` (reads docs/README.md) | rc 0 |
| `check_todo_ownership.py`, `check_hygiene.py --check`, `measure_test_evidence.py --check`, `check_archive.py` | rc 0 |
| `git diff --check`, against both `c1fa4183` and `c07232228` | rc 0 |

## 4. Composition probes

### 4.1 Anchors into and out of the composed pages

Receipts: `receipts/02_anchor_probe.txt` and `receipts/03_anchor_negative_control.txt`.

`probe_anchors.py` uses the repository's own heading reader. It resolves every fragment link on 13 focus pages: the 5 PR pages and the 8 pages the train changed. It also resolves every fragment link from any of the 173 tracked pages into those focus pages.

- Result: 542 links resolved, 0 missing.
- Negative control: I planted a one-letter anchor change in the composed firmware page's new D3 DR2c link, on a scratch export. Both the probe and `gen_toc.py --verify-anchors` fail on it (rc 1).

### 4.2 Line-number citations the train could have shifted

Receipt: `receipts/04_line_citation_probe.txt`, plus section 6 of `receipts/07`.

- The PR pages contain 4 `path:N` citations: `milan_baremetal.c:1254,1438,340` and `nvm_shape.py:146`. None of them is in a file the train changed.
- The D3 citations of the form `` `file` line N `` point at processor or HDL files. The train changed 0 HDL, processor, `syn` or `tb/verilator` paths, and the `protocol-processor` gitlink is `16be6768` on both sides.
- The only train-shifted line target is the FASTCONNECT 5.1 table's `milan_soc.py` rows. That table was already stale at the source base; see S1.

### 4.3 Can the builder test's reads of the composed page flip?

Receipts: `receipts/05_builder_page_constants.txt` and `receipts/06_hosted_docs_composition.txt`.

`sw/builder/test_builder.py` reads `BAREMETAL_FIRMWARE.md` as text. `docs-check` runs those arms on every change (CI_WORKFLOWS table). The full builder bank is outside this round's allowance, so I used two substitutes.

**(a) Differential probe.** I took all 7,350 string constants in `test_builder.py`, each as a literal and, where it compiles, as a regex (14,267 probes). For each, I counted its matches on four versions of the page: the base, the #582 side, the #610 side and the candidate.

- non-additive = 0: every candidate count is exactly the base count plus both deltas.
- 66 probes moved on both sides. All are generic tokenizer or fragment patterns: identifier, number, comment and whitespace regexes, and words such as `the ` or `port`.
- The one documentation-shaped pattern among them, `KEY_TOKEN_RE` at `test_builder.py:26158-26159`, is applied to `docs/ENDSTATION_BUILDER.md`, not to this page.
- The probe exits rc 1 on any both-sides entry. The classification above is my reading of that list, and the receipt records it.

**(b) Hosted evidence.** Hosted `docs` run 36392094990 (event `pull_request`) checked out `ae8108b62`, "Merge 6b76f2d8 into 54ce8773", with tree `c2ba0170...`.

- My local `git merge-tree 54ce8773 6b76f2d8` reproduces that tree.
- All 5 PR pages in that tree are blob-identical to the candidate's, including `BAREMETAL_FIRMWARE.md` blob `fd761272`.
- That tree differs from the candidate only in #593/#75 files. `test_builder.py` references none of those files.
- In that run, all 55 `docs-check` steps succeeded, including "End-station builder gates", "Compiler-absent firmware controls", "Bare-metal scope gate", "NVM record-space gate", the feature-status gate and the em-dash gate. `docs-check-no-git` and `wire-accountability` also succeeded.

### 4.4 Semantic cross-check (receipts/07_semantic_crosscheck.txt)

**#582 clock contract vs the composed pages.**

- The composed Build contract gives the clock one definition: `CPU_HZ = 50_000_000` in `tb/verilator/nvm_capture_cpu/recipe.py`.
- #610's added text on the page uses wall time only: the 1,000 ms DR2a window, and DR2c's 3 attempts at 1,000 ms and 3 at 500 ms. It contains no clock figure.
- The "50 MHz" statements on SNAPSHOT_OWNERSHIP (`:75,1618,1702,1796,1944`) predate the source base and remain true under `CPU_HZ`.
- `:1618` links `BAREMETAL_FIRMWARE.md#build-contract`, and that anchor still resolves. #582 renamed no heading; it changed only Contents descriptions.
- D3 `:556` "25,000,000 at 50 MHz" is an example of the `CLK_HZ_P`-parameterised BACKOFF formula. It agrees with the contract clock.

**#582 SoC CLI change vs the PR pages.** #582 made `--entity-gen-dir configs/generated/<cfg>` mandatory and removed the tracked entity fallback. FASTCONNECT `:982-983` already cites the generated per-config paths. #582 changed no FLASHBOOT, journal or NVM-face line of `milan_soc.py`: its 4 matching lines are all the recipe path.

**#593 vs the D3 pages.** #593 redefines the `mr`/MEDIA_RESET/`tu` release rules in REQ-VER-06, TESTING and GM_LOSS_RECOVERY. The four PR pages contain 0 statements about `mr`, MEDIA_RESET, `tu`, PHC steps or GM changes.

- D3 lane 5's physical contract (`:2743-2757`) agrees with the composed REQ-VER-06 and TESTING 6d on these points: 200 cold cuts (160 idle and 40 in commits), a first ADP before T0 + 20 s with `valid_time=10`, automatic restoration only, and all eight items once #70 lands.
- For counter, uncertainty and observation rules, D3 defers explicitly to REQ-VER-06, so #593's new rules apply without contradiction.
- GM_LOSS_RECOVERY has 0 saved-state, NVM or persistence statements.

**#75 vs the D3 pages.** The findings page's "restoration" (`:918-940`) means the bench state after the measurement: streams unbound by the controller, and configuration and descriptors compared. It makes no claim about NVM saved state or fast connect. D3's "#397/#75 measurements" ratification reference (`:2755`) points at a page that now exists in the candidate.

## 5. Findings

No BLOCKER, MAJOR or MINOR finding.

```text
[R381] SUGGESTION Docs - docs/design/SAVED_STATE_FASTCONNECT.md:548-560 (section 5.1 table) - the citation table was already stale before this PR and the train
```

- **Requirement/evidence:**
  - The table says "Re-derived at this head" and lists `milan_soc.py` at lines 137 and 159, `ooc.sh` at 81 and the sizer at 8.
  - At the source base `c07232228`, `milan_soc.py` cites the page at 130, 527 and 1206, and at the candidate at 143, 540 and 1219. #582 moved each citation by 13 lines.
  - `syn/yosys/ooc.sh` cites it at 168.
  - Blame puts the rows at `52c4d9c6b0` (2026-08-24). The PR did not change them and the train did not create them.
- **Impact:** a reader following the table lands on the wrong lines. This PR and the train each leave it unchanged in kind. The composition adds 13 more lines of drift to rows that were already wrong. No gate reads the table.
- **Why SUGGESTION, not MINOR:** the defect exists at both the reviewed source and live dev, in lines neither side changed, so the composition did not introduce it. Under AGENTS section 4, newly discovered work becomes its own Issue, and this is not a way to bank a lens.
- **Required outcome (optional):** record it as a separate public item, or fold it into lane 1's statement sweep. The fix is either to re-derive the rows or to cite by grep pattern instead of line.
- **Verification:** `grep -n SAVED_STATE_FASTCONNECT sw/litex/milan_soc.py syn/yosys/ooc.sh scripts/check_nvm_record_space.py` matches the table.

## 6. Prior public review findings on PR #610: disposition at this head

I read these after my own pass. The four D3/README pages at the candidate are blob-identical to the source head `6b76f2d8`. The firmware page differs from the source head only by #582's disjoint hunk (section 2). So the source-head dispositions carry over unchanged. I did not re-derive them.

| Finding | Disposition at c08becbb |
|---|---|
| R381-1, R381-2 (F1, F2), R380-1, R380-2 findings (MINOR) | Resolved at source (R381-3, R380-4). They stay resolved because their artifacts are byte-identical here. |
| R380-3 F1 = R381-3 S2 (sweep comment-prefix claim) | Resolved at `6b76f2d8` (R380-4). Byte-identical here. |
| R381-3 S1, S3 and R380-3 S2, S3 (suggestions) | Applied at `6b76f2d8` (R380-4). Byte-identical here. |
| R380-2 S3 (suggestion) | R380-4 reports the `:188` count now reads "Eight". Byte-identical here. |
| R380-4 S1 (suggestion: blockquote and diagram-text wraps not crossed by the sweep) | Still open as a suggestion. The composition does not affect it, and it has no coverage effect. |

The composition reopens no prior finding.

## 7. Lens results

```text
[R381] PASS Conformance - BAREMETAL_FIRMWARE.md:29-82 (#582 build contract, CPU_HZ single definition) + :1896-1925 (#610 DR2a/DR2c/carrier text) at c08becbb; D3 :2743-2757 vs composed REQUIREMENTS.md REQ-VER-06 and TESTING 6d; D3 :556 and SNAPSHOT :1618 vs recipe.py CPU_HZ; rulings 5862405632/5863247772 text unchanged by composition (receipts/01, 07)
[R381] PASS RTL - candidate vs train parent touches 0 HDL/processor/syn/tb-verilator paths; protocol-processor gitlink 16be6768 both sides; #582 milan_soc.py diff (clock refusal, generated-entity requirement) vs D3 CLK_HZ_P BACKOFF text and FASTCONNECT :982-983 (receipts/07 sections 1 and 7)
[R381] PASS Robustness - composition does not touch the PR's failure/retry/alarm/recovery statements: BAREMETAL :1913-1925 and the four D3/README pages byte-identical to source head 6b76f2d8 (blob equality, receipts/06); #582 refusal paths are build-time CLI checks with no saved-state path; source coverage R380-4 at 6b76f2d8
[R381] PASS Tests - builder text reads of the composed page: differential probe non-additive=0 over 14,267 probes (receipts/05); hosted docs-check incl. End-station builder gates on ae8108b whose five PR page blobs equal the candidate's (receipts/06); ci_scope --selftest with #582's GATE_READ_DOCS; anchor probe with a failing planted control (receipts/02, 03)
[R381] PASS Docs - 27 gates rc 0 on c08becbb incl. docs_check, gen_toc --check/--verify-anchors, check_em_dash --base c1fa4183 (948 added lines, 0 findings) and --base c07232228, doc paths/style, DOC_MAP, feature status (receipts/gates); 542 fragment links 0 missing; S1 is a pre-existing SUGGESTION
```

## 8. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition touches this lens: the shared firmware page and the composed REQ-VER-06/TESTING 6d that D3 lane 5 defers to (receipts/07). The source content is covered by R380-4. | R381-4 (composition); R380-4 (source) | `c08becbbfdbf622ee678d5854312c53faf805d39`; `6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14` |
| RTL | CLEAN | Composition touches this lens only through the #582 clock contract and SoC CLI, which I checked against the D3 clock text. No HDL, processor or gitlink change. The source is covered by R380-4 (and by R381-3 at the ancestor `816c3b74`). | R381-4 (composition seam); R380-4 (source) | `c08becbb...`; `6b76f2d8...` |
| Robustness | CLEAN | Composition does not touch this lens: the failure, retry and recovery text is byte-identical to the source head. | R380-4 (source; R381-3 at `816c3b74` for the ancestor), with composition invariance checked by R381-4 | `6b76f2d8...` (ancestor of the candidate; nothing in scope changed since); invariance at `c08becbb...` |
| Tests | CLEAN | Composition touches this lens: the builder reads of the page, ci_scope, and gate inventories (receipts/05, 06, gates) | R381-4 | `c08becbbfdbf622ee678d5854312c53faf805d39` |
| Docs | CLEAN | Composition touches this lens: the composed page, anchors, TOC, em-dash and feature ledger (receipts/gates, 02, 03, 04). S1 is a SUGGESTION. | R381-4 | `c08becbbfdbf622ee678d5854312c53faf805d39` |

## 9. Real limits

- I did not run the full builder bank (`test_builder.py`), the parent, processor, gPTP or Yosys banks, or `act`/hosted replication; this round's allowance excludes them.
  - For the builder's page reads I relied on two things: the differential probe (4.3a), and hosted `docs-check` on `ae8108b`. That tree lacks only the #593/#75 files, which the builder test does not reference.
  - I did not execute builder arms on the exact candidate tree.
- The differential probe covers text constants appearing in `test_builder.py`. It cannot see a pattern assembled at run time from pieces. Section placement and the hosted run bound that gap, but do not close it.
- I checked hosted evidence at the source head only. It is a snapshot: at review time, 2 Verilator shards at the source head were still in progress. GitHub does not know the candidate commit.
- The PR changes documentation only, so I needed no Verilator; the scoped binary was not used.
- Physical calibration was NOT RUN, and field skips are not hardware proof. This lane claims no silicon result.

## 10. Pending manager duties

- Build and gate the final current-dev candidate at the merge turn. It must include the full local bar of CONTRIBUTING section 3/7 and the builder bank on that exact tree.
- If dev has moved past `54ce8773`, recompute the composition.
- Own hosted and `act` acceptance on the exact merge head. That includes the `rtl-full` shards still running at the source head when I checked.
- Decide whether S1 becomes a separate public item or joins lane 1's sweep.
- After merge, run post-merge containment (`check_merge_containment.py`, `check_merge_review_integrity.py`).

## 11. Clone restoration (receipts/08_restore_verification.txt)

- This round made no tracked-file edits in the clone. Every probe mutation ran on a scratch export.
- I removed the Python cache directories the gates created.
- After that:
  - `diff-files` and `diff-index --cached` are clean;
  - the `ls-files -s` digest equals the pre-review digest `7c2558ab...`;
  - `write-tree` gives `cd7ae956...`;
  - the gitlinks are unchanged (`protocol-processor` `16be6768`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, `external` `efeb541a`, the last uninitialised as before);
  - there are no untracked or ignored files.

R381-4 FINISHED
