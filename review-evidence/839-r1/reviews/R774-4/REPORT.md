[R774] POSITIVE - exact head 4f210018e6556a9753ed409885d82744c8f5effa

Round R774-4, external independent review of PR #841 (issue #839). Head `4f210018e6556a9753ed409885d82744c8f5effa`, tree `b565b4c16317c1732ba431ff6335ccf46feab8c5`. The delta since the head round 3 reviewed is `3c229478..4f210018`: the merge of dev `cc204c6f` (`dc7eebff`) and one regeneration commit (`4f210018`).

Verdict: no BLOCKER, MAJOR, MINOR or RESIDUE.

- **The merge keeps both sides exactly.** It had no conflicts, and `docs/reference/REGISTER_MAP.md` auto-merged with both hunks kept.
- **The regeneration commit is generator output only.** It is byte-for-byte what `scripts/docs_inventory.py --write` produces on the merge commit. `--check` exits 0 at the head, and my own regeneration is byte-identical.
- **There is one merge base**, `cc204c6f`.
- **The gates pass at the head.** Every docs workflow gate step I could run passes. `bootsa` passes 67 of 67 checks and `bootsa-mutants` passes 13 of 13.
- **This PR adds no image command-table mismatch.** The digest drift is the same set on dev and at the head (#838).

Two optional suggestions follow, both about dev-side tooling and not about this PR.

## 1. What was reconstructed

- **Contract.** AGENTS.md sections 6 and 7: the five lenses, and per-lens coverage banked against a commit. The round 4 scope comes from the assignment: dev sync and inventory regeneration only, with its three checks.
- **Public state**, read without any GitHub write:
  - issue #839 comments `[A731d] TAKEN` (6674674241) and `[A731d] REVIEW READY` (6675710674);
  - PR #841's head (`4f210018`, base `dev`, open, not draft);
  - the review start comment 6676033791.

  Prior review findings were read only after my own pass over the diff (section 4).
- **Published evidence.** `review-evidence/839-r1` at `b06fad40`, fetched sparsely.
  - All 339 `author-r4/` files match their `published_sha256` in `MANIFEST.json`, with 0 bad, 0 unlisted and 0 missing (`receipts/evidence_manifest_check.txt`).
  - The evidence commit itself carries no git signature; the API reports `unsigned`. The manifest digests are what I verified.

## 2. Checks and results (the three assignment checks)

| # | Claim | Method | Result | Receipt |
|---|---|---|---|---|
| 1a | The merge keeps both sides | `git merge-tree --write-tree 3c229478 cc204c6f`, compared with the tree of `dc7eebff` | rc 0, no conflict. The replay tree `0957ad26` equals the merge commit's tree. So the merge is the clean automatic merge with no manual edits | `receipts/merge_tree_replay.txt` |
| 1b | Neither side lost a hunk | Each side's diff before and after the merge, with `index` and `@@` lines removed | PR side `604899c0..3c229478` = `cc204c6f..dc7eebff` (sha `282705c4...`). Dev side `604899c0..cc204c6f` = `3c229478..dc7eebff` (sha `f770707b...`) | `receipts/pr_side*.diff`, `receipts/dev_side*.diff` |
| 1c | REGISTER_MAP auto-merged | Read at the head | Dev's line 428 (the #599 link-cycle finding) and this PR's two `Sequencing (#839)` rows (`:411-412`) are both present | `docs/reference/REGISTER_MAP.md:411-412,428` |
| 2a | The regeneration went only through the generator | In a scratch clone at `dc7eebff`: `--check` rc 1 (`STALE (13 lines differ)`), then `--write` rc 0, then hash the output | The generated blob `9d5cf0fe` equals the head blob `4f210018:docs/DOCUMENTATION_AUDIT.md` | `receipts/inv_check_merge.*`, `receipts/inv_write_merge.*`, `receipts/regen_from_merge.txt` |
| 2b | Fresh at the head, and my regeneration is byte-identical | In this clone: `--check` rc 0. In a scratch clone at the head: `--write` rc 0, `git status` empty, `--check` rc 0 | `DOCUMENTATION_AUDIT.md` (sha256 `ee2a0fff...`) and `docs_inventory.json` (`6b53c9b3...`) are identical. The generator reads `docs_inventory.json` as input and never writes it, so it is correctly unchanged, as the handoff says | `receipts/inv_check_head.*`, `receipts/inv_write_regen.*`, `receipts/regen_bytes.sha256`, `receipts/regen_status.txt` |
| 2c | Fresh without Git metadata | `git archive` of the head, then `--check` with `-I` and no bytecode written | rc 0, `540 lines ... fresh` (S1 describes a caveat about this mode) | `receipts/inventory_nogit_clean.log` |
| 2d | The generator counts this PR's page edits by its own rules | `wc -l` at the head, compared with the regenerated rows | Line counts match: CHANGELOG 1111, BAREMETAL_FIRMWARE 2338, TESTING 1937, `milan_dp/README` 1817, REGISTER_MAP 2580 (±0). The quoted-line column moved +3 for D0-011/012/013/061/062 (now 218/221/222/203/2289, each the line of its quote in `BAREMETAL_FIRMWARE.md`) and +2 for D0-057 (TESTING). Totals went from 92,127 to 92,285 (+158 = 24+3+2+129) | `docs/DOCUMENTATION_AUDIT.md:30-34,121,270,334,432,485-489,537` |
| 2e | Evidence text anchored at dev `1f29f189` is unaffected | D0-062's evidence cites "line 2291". The page anchors its evidence at dev `1f29f189` ("Findings cite source lines at dev `1f29f189`") | At `1f29f189`, line 2291 holds the cited text. This is correct under the page's own anchor rule, so it is not a finding (see S2) | `git show 1f29f189:docs/integration/BAREMETAL_FIRMWARE.md`, line 2291 |
| 3a | One merge base | `git merge-base --all HEAD cc204c6f`, plus the parents of both commits | One base, `cc204c6fd2349b543d73f15c97162a2c4434c86e`. `dc7eebff` has parents `3c229478` and `cc204c6f`; `4f210018` has parent `dc7eebff` | `receipts/merge_base.txt` |
| 3b | Whitespace | `git diff --check` on `cc204c6f..HEAD` and on `3c229478..HEAD` | rc 0 for both | `receipts/diff_check.log` |
| 3c | Docs workflow steps | Each local-runnable `run:` step of `.github/workflows/docs.yml` at the head, in the workflow's shell (`bash -eo pipefail`). The pinned Markdown renderer (hash-pinned `tools/markdown/requirements.txt`) and `wavedrom==2.0.3.post3` came from a disposable scratch venv | 40 gate steps, all rc 0: 38 in `docs-gates-0`/`docs-gates-2`, the no-git job's step and the wire-accountability step. Three steps first failed only because a package was missing (em-dash, WaveDrom, TOC) and pass when re-run with the venv. They include the new `Documentation inventory freshness gate` (`--check` OK; `--selftest` OK, 50 controls) and the em-dash gate on `cc204c6f..HEAD` (179 added lines, 0 findings) and on `3c229478..HEAD` (534 added lines, 0 findings) | `receipts/docs_steps_summary.tsv`, `receipts/docs_steps/`, `receipts/docs_steps_venv*`, `receipts/docs_check_no_git.log`, `receipts/wire_accountability.log`, `receipts/venv_freeze.txt` |
| 3d | `bootsa` and `bootsa-mutants` | `make -C tb/verilator/milan_dp bootsa-mutants` (it runs `bootsa` first), using the scoped Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`) | `== bootsa: checks: 67   failures: 0 ==` and `RESULT: PASS`. Then `13 checks: 13 PASS, 0 FAIL`: the clean leg plus 12 controls, each failing by its named check. rc 0 | `receipts/bootsa_mutants.log`, `.rc` |
| 3e | Submodule pins | `git ls-tree` of the six gitlinks | Equal to `3c229478` and to dev `cc204c6f` | `receipts/gitlinks_head.txt` |
| — | #838 command table | Every `scripts` digest declared in `ci/image/command-table.json`, checked against the file bytes at the head and at dev | 37 of 151 mismatch or are missing at both commits, and it is the same set. No file this PR changes is declared in the table. The checker itself refuses on this host (`CI_IMAGE_SHFMT`), as it does on dev | `receipts/table_digests_head.txt`, `receipts/table_digests_dev.txt`, `receipts/tool_inventory_head.log` |

Docs workflow steps I did not run, and why:

- **Install, download and pip steps:** `pip`, `apt`, sv2v, the RV32 SDK, the package cache, and `Build the validated HDL reference`, which pip-installs.
- **Builder steps:** the two builder legs (`docs-gates-1` and `docs-gates-2`, step 14), and `Compiler-absent firmware controls`, which I stopped (rc -15) because its `--absent` half runs the builder gate.
- **Runner and recording steps:** `act_ci.py --selftest`, and the record, upload, manifest and fail-fast steps.

The builder steps are outside my allowed scope, and the delta touches none of their inputs (no `sw/` change in `3c229478..HEAD`). The author's round 4 receipts report all of them in `author-r4/receipts/gates/docsyml/docs-yml-table.md`.

## 3. Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

Comment rule: the delta adds no source comment. It contains only the merge and generated table rows. Both commit subjects are one line with no trailers. There is no new residue.

### S1 - SUGGESTION - Robustness, Tests - `scripts/docs_inventory.py` (dev side, from PR #815) - the no-Git walk counts ignored cache directories
- Evidence: I ran `scripts/docs_check.py` without `-I` in a `git archive` copy of the head, which wrote `scripts/__pycache__/`. A `--check` after that reports STALE: it adds the row `| scripts/__pycache__/ | no | 0 |` and the audit grows to 541 lines (`receipts/nogit_vs_git_audit.diff`). A clean copy is fresh (`receipts/inventory_nogit_clean.log`).
- Impact: none on this PR. The hosted no-git job does not run the inventory gate, and the gate in Git mode uses `git ls-files`. Only a local no-Git run can be broken by bytecode caches.
- Outcome (optional, for the #797 lanes, not this PR): leave ignored and cache directories out of the filesystem walk, or document the limit.

### S2 - SUGGESTION - Docs - `docs/DOCUMENTATION_AUDIT.md` D0-062 (dev-side data, `scripts/docs_inventory.json:466`)
- Evidence: the evidence text says "line 2291". At the head, the cited text is at `BAREMETAL_FIRMWARE.md:2294` because this PR adds 3 lines above it. The page anchors evidence at dev `1f29f189`, where 2291 is right, so this is not a defect.
- Outcome (optional): the area lane that fixes D0-062 removes the entry anyway. #841 needs no change.

## 4. Prior findings, resolved or retained at this head

The delta changes no file under `tb/`, `hdl/` or `sw/`, and neither `CHANGELOG.md` nor `scripts/measure_test_evidence_readers.py` (`git diff --quiet 3c229478 HEAD -- ...` returns rc 0). So every round 3 item stands as published.

| Prior item | Status at `4f210018` |
|---|---|
| R774-2 F1 (MINOR, Docs) = R773-2 RES-1 | Resolved in round 3. The delta does not touch `milan_dp/README.md` |
| R774-2 S1 (name every check a control fails), S2 (use the exported offsets instead of `0x108`/`0x10C`/`0x784`), S3 = R773-2 S3 (`gen_boot_fw.py:112` spacing) | Retained as optional. Files unchanged |
| R774-2 S4 / R773-2 S1 ("untouched" labels), R773-2 S2 (CRF condition) | Taken in round 3. Unchanged |
| R773-2 S4 (PM2 is an equivalent mutant) | Informational. No `hdl/` change |
| R773-3 S1-S3 and R774-3 S1-S4 (README wording and placement; the EtherType check has no planted control) | Retained as optional. Their artifacts are unchanged |

## 5. Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment checks 1-3 (section 2). `REGISTER_MAP.md:411-412,428`. The delta changes no protocol behaviour: `tb`, `hdl` and `sw` are unchanged since `3c229478`, which R774-3 and R773-3 covered | R774-4 | `4f210018e6556a9753ed409885d82744c8f5effa` |
| RTL | CLEAN | `git diff 3c229478 HEAD -- hdl` is empty. `bootsa` is 67/0 at the head. The merge-tree replay shows the dev side brings no HDL | R774-4 | `4f210018e6556a9753ed409885d82744c8f5effa` |
| Robustness | CLEAN (S1 optional, dev side) | The 13/13 control campaign at the head. The no-Git inventory mode (`receipts/inventory_nogit_clean.log`) | R774-4 | `4f210018e6556a9753ed409885d82744c8f5effa` |
| Tests | CLEAN | `receipts/bootsa_mutants.log` (67/0, 13/13). The inventory `--selftest` (50 controls). The 40 docs gate steps, all rc 0. The #838 digest set, equal to dev's | R774-4 | `4f210018e6556a9753ed409885d82744c8f5effa` |
| Docs | CLEAN (S2 optional) | `docs/DOCUMENTATION_AUDIT.md`, regenerated byte-identically from `dc7eebff` and from the head. The line counts of the five #839 pages. The em-dash, link, TOC and cited-path gates. The handoff text (6675710674), whose every claim matches the receipts | R774-4 | `4f210018e6556a9753ed409885d82744c8f5effa` |

## 6. Real limits

- No manager source bank ran at this head, and I claim none. The source-head execution evidence is the author's published round 4 receipts plus my own probes above.
- I did not run:
  - the builder legs or the compiler-absent builder gate;
  - `act_ci` or its selftest, or Docker/act;
  - the full sweep or the HDL reference build;
  - `ci_tool_inventory.py --check` itself. It refuses on this host, so the command-table comparison is by digest only.
- I did not inspect hosted contexts. The manager owns hosted and act acceptance.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- The no-git docs check ran on a `git archive` copy, not on a checkout with `.git` removed. The tracked content of the two is the same.
- After the probes, the clone is at the exact head: index tree `b565b4c1`, no untracked or ignored files in the superproject or any submodule, and all six gitlinks at their pins (`receipts/restore_verification.txt`).

## 7. Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts. At this writing, the source base and live dev are both `cc204c6f`.
- Record the exact-head hosted `rtl-fast`, `verilator-suites` and `yosys-portability` results, and the act replica.
- Carry S1, S2 and the optional suggestions retained in section 4 to the author or the #797 lanes.
- Obtain the second positive review (R773-4) and the maintainer's explicit merge authorization.

R774-4 FINISHED
