[R773] POSITIVE - exact head 4f210018e6556a9753ed409885d82744c8f5effa

Round R773-4: internal independent review of PR #841 (issue #839). Exact head `4f210018e6556a9753ed409885d82744c8f5effa`, tree `b565b4c16317c1732ba431ff6335ccf46feab8c5`. The PR's GitHub head is the same SHA. Source base and live `dev`: `cc204c6fd2349b543d73f15c97162a2c4434c86e`. The previously reviewed head is `3c22947861e5c057a6195ad46e1a379d67592559`, where R773-3 and R774-3 were both POSITIVE.

Scope of this round: the round-4 delta `3c229478..4f210018`. It is one `--no-ff` merge of dev `cc204c6f` (PR #836 and PR #815, the documentation audit) and one regeneration commit. Code the delta does not touch keeps its round-3 lens verdict, because the merge changes nothing it depends on (section 1). All five lenses were applied to the delta, and each is backed by artifacts and receipts in this packet.

Verdict: no open BLOCKER, MAJOR or MINOR, and no RESIDUE. One optional SUGGESTION (S1) about dev's data, outside this PR's scope. Every prior SUGGESTION is retained as optional, and nothing it depends on moved.

## 1. Merge: both sides kept, one base (focus items 1 and 3)

Receipt: `receipts/merge_structure.txt`.

- `dc7eebff` has parents `3c229478` and `cc204c6f`. `git merge-base --all HEAD cc204c6f` prints one base, `cc204c6fd2349b543d73f15c97162a2c4434c86e`. The round-3 head's base was `604899c0`, so `604899c0..cc204c6f` is exactly what dev added.
- **PR side kept, byte for byte.** `git diff 604899c0 3c229478` (round-3 PR diff) equals `git diff cc204c6f dc7eebff` (PR diff on the new base), compared with `index` lines and hunk offsets normalised: IDENTICAL, 17 files, +1693/-22.
- **Dev side kept, byte for byte.** `git diff 604899c0 cc204c6f` equals `git diff 3c229478 dc7eebff`: IDENTICAL, 10 files, +2096/-226.
- Only `docs/reference/REGISTER_MAP.md` was touched by both sides. Both hunks are present at the head: the PR's `MAC_ADDR_LO/HI` sequencing rows at `:414-415`, and dev's #599 link-cycle sentence at `:428`. This matches the handoff ("auto-merged, no conflict").
- No gitlink changed against dev or against `3c229478`. `scripts/docs_inventory.py` and `scripts/docs_inventory.json` are byte-identical to dev.
- `git diff --check cc204c6f 4f210018`: rc 0, no output (`receipts/diff_check.rc`).
- No `.github/` or `ci/` file differs from dev. So this PR cannot add an image command-table mismatch (#838). The checker refuses identically at the head and on a `cc204c6f` archive in this environment (`REFUSED: CI_IMAGE_SHFMT must name the checksum-pinned Bash parser`; `receipts/cmdtable_dev_vs_head.diff` is empty). No finding.

## 2. Regeneration through the generator only (focus item 2)

Receipts: `receipts/inventory_write.*`, `receipts/inventory_regen_cmp.txt`, `receipts/inventory_check.*`, `receipts/nogit_inventory_check_*`.

- `4f210018` changes only `docs/DOCUMENTATION_AUDIT.md` (13 lines). `--write` writes only `OUTPUT` (`scripts/docs_inventory.py:990`). The JSON writes at `:722`, `:726`, `:807-809` belong to the self-test fixtures. So the JSON is generator input, and it correctly stays unchanged.
- **I regenerated it myself:** `python3 -I scripts/docs_inventory.py --write` rc 0 at the head. The output is BYTE-IDENTICAL to the committed page: sha256 `ee2a0fff5ef5265450a6cf702299dbe804bf852dd4e6e91b1bdace2cd946216a` for both. After that, `--check` rc 0: "documentation inventory: OK (540 lines, docs/DOCUMENTATION_AUDIT.md is fresh)". `--selftest` rc 0, 50 controls.
- **The commit was needed, and it falsifies.** `--check` on a no-git archive of the merge parent `dc7eebff` gives rc 1: "STALE (13 lines differ); first difference at line 30: committed: | current | 176 | 73,487 |". On a no-git archive of the head it gives rc 0, fresh. That makes the filesystem-walk population agree with the git population.
- **This PR's edits are counted by the generator's own rules.** I checked them independently with `wc -l` at the head (`receipts/merge_structure.txt`):
  - Page lengths: CHANGELOG 1111, BAREMETAL_FIRMWARE 2338, TESTING 1937 and milan_dp README 1817 match the four rows. REGISTER_MAP stays at 2580, because the PR rewrote two rows in place.
  - The totals move by +153 current (CHANGELOG +24, README +129), +5 stale (BAREMETAL +3, TESTING +2) and +158 overall. These equal the merge-side diff stat.
  - The re-resolved finding lines are correct. D0-011, D0-012, D0-013, D0-061 and D0-062 move by +3, because the PR adds three lines at BAREMETAL `:112-116`, above all five. D0-057 on TESTING moves by +2, because of the PR's row at `:277` and the run-list rewrap at `:406-411`. I confirmed with grep that D0-011 is at `:218`, D0-012 at `:221` and D0-061 at `:203`.
  - Cited paths and standards are unchanged, which is correct under the generator's directory-granularity rule. REGISTER_MAP's D0 rows (`:416` and others) do not move.

## 3. Gates at the head (focus item 3)

All of these ran in this clone at `4f210018`. The tracked tree was restored afterwards (section 7).

- `make -C tb/verilator/milan_dp bootsa` with the pinned Verilator (`Verilator 5.050 2026-07-01 rev v5.050`, `receipts/bootsa.verilator_version.txt`): rc 0, `== bootsa: checks: 67   failures: 0 ==`, `RESULT: PASS` (`receipts/bootsa.log:578`).
- `make bootsa-mutants`: rc 0, `13 checks: 13 PASS, 0 FAIL` (`receipts/bootsa_mutants.log:184`). Every one of the twelve controls is caught by its named checks. These are the same names as the author's round-4 table.
- docs.yml `run:` steps (`run_docs_gates.sh`, `receipts/docs_gates.tsv`):
  - 78 of 82 commands gave rc 0 on the first run.
  - The other 4 failed only because the pinned Markdown renderer was not installed: `check_em_dash.py --base cc204c6f`, and `gen_toc.py --selftest`, `--verify-anchors` and `--check`. I reran all four with the pinned `tools/markdown/requirements.txt` in a disposable venv, and all gave rc 0 (`receipts/docs_*_venv.*`). Em-dash: 0 findings over 179 added lines in 6 pages, `cc204c6f..HEAD`. TOC: 1501/1501 arms, 582 anchors, 151 pages OK.
  - Also rc 0: `gen_wavedrom.py --selftest` and its three `--check` runs (venv, `wavedrom==2.0.3.post3`), `test_firmware_compiler.py --selftest` and `--absent` ("GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations"), `gen_hdl_reference.py --selftest` (44/44) and the HDL reference build.
  - The no-git job (`docs_check.py`, `check_feature_status.py`) ran on a `git archive` of the head with no `.git`: both rc 0, 0 findings (`receipts/nogit_*`).
  - Gate 46 (inventory `--check` and `--selftest`) is rc 0 in both modes.
- Published author evidence: `review-evidence/839-r1/author-r4/HANDOFF.md` (sha256 `b84f3032…`) and `receipts/INDEX.md` (sha256 `92a26f80…`) match their entries in the published `MANIFEST.json` at `b06fad40` (`receipts/published_author_r4_sha256.txt`). The author's gate table (67/0, 13/13, inventory OK, merge base, diff-check) matches what I reproduced. I did not check the manifest's signature.
- Hosted, exact head, a snapshot only (`receipts/hosted_check_runs.tsv`): 28 completed/success, 1 skipped, and 29 still queued or in progress, including the Verilator and Yosys shards and `docs-check`. The manager owns hosted/act acceptance. I claim nothing from the incomplete contexts.

## 4. Prior findings, resolved or retained at this head

I read these after my own pass over the delta. Round 3 (R773-3, R774-3) left no BLOCKER, MAJOR, MINOR or RESIDUE open. Its open items are SUGGESTIONs, and the delta touches none of the files they cite (the PR-side diff is identical, section 1):

| Item | Status at `4f210018` |
|---|---|
| R773-3 S1-S3 (README `:1205` "instead", `:1191-1192` AECP grouping, `:1210` CRF placement) | Retained, optional; README unchanged by the delta |
| R774-3 S1, S2, S4 (README wording) | Retained, optional |
| R774-3 S3 (EtherType check has no planted control) | Retained, optional; `bootsa_mutants.py` unchanged |
| R773-2 S3 = R774-2 S3 (`gen_boot_fw.py:112` spacing) | Retained, optional; file unchanged |
| R774-2 S1 (name every check a control fails), S2 (exported offsets for `0x108`/`0x10C`/`0x784`) | Retained, optional; `sim_boot_sa.cpp`, `bootsa_mutants.py` unchanged |
| R773-2 S4 (PM2 equivalent mutant) | Informational; no `hdl/` change in the delta |
| R774-2 F1 = R773-2 RES-1 | Resolved at round 3; the resolving README text is unchanged here |

## 5. Findings

### S1 - SUGGESTION - Docs - docs/DOCUMENTATION_AUDIT.md:492 (D0-062, data `scripts/docs_inventory.json`) - the evidence's own line reference does not follow the page
Evidence: the generator re-resolves the Line column (2286 to 2289), as it should. The D0-062 evidence text still says "(2026-08-19, line 2291)", and at this head that record is at BAREMETAL_FIRMWARE.md line 2294. The page's header says findings cite source lines at dev `1f29f189`, so the text is consistent with the stated convention. It is not this PR's text, and it is not this PR's edit to make. Impact: a reader who opens the page at the head finds the record line ("The measured cell is commit `1e80a106`") 3 lines lower: it is `:2291` at dev `cc204c6f` and `:2294` at the head. Optional outcome: the #797 D0 data could drop that line reference, or the generator could resolve it. Track it with #797, not here. Verification: grep `1e80a106` in BAREMETAL_FIRMWARE.md at the head and compare it with the evidence text.

No source comments were added in the delta. It adds only dev's tree and a generated page, so the comment rule has nothing new to apply to. The lane labels ("area lane", "D0") in the generated audit come from dev's generator and data, on a findings page.

## 6. Lens results

[R773] PASS Conformance — receipts/merge_structure.txt; docs/reference/REGISTER_MAP.md:414-415,428 at 4f210018 — the merge keeps both sides byte-identical, with one base `cc204c6f`. Issue #839 acceptance 1-4 and the maintainer decision record are unaffected: the PR-side diff is identical to round 3's, and acceptance 2's gate is green (67/0; 13/13).
[R773] PASS RTL — `git diff cc204c6f 4f210018 -- hdl/milan/milan_datapath.sv` equals round 3's PR-side hunk (merge_structure.txt); dev's side touches no `hdl/` file — the RTL depends on nothing the delta changed; the round-3 RTL verdict stands. bootsa rebuilt with pinned Verilator 5.050: 67/0.
[R773] PASS Robustness — receipts/bootsa.log:578 and receipts/bootsa_mutants.log:167-184 at 4f210018 — the early-enable, single-half and reset-boot arms and all twelve planted controls behave as at round 3 on the merged tree; there are no new input paths in the delta.
[R773] PASS Tests — receipts/inventory_regen_cmp.txt, receipts/nogit_inventory_check_dc7eebff35.*, receipts/docs_gates.tsv and the venv reruns, receipts/bootsa_mutants.log — gate 46 fails at the merge parent (STALE, 13 lines) and passes at the head, so the freshness evidence can fail. The regeneration is byte-identical. The docs.yml steps are green. bootsa-mutants is 13/13.
[R773] PASS Docs — docs/DOCUMENTATION_AUDIT.md:30-34,124,273,337,435,488-492,540 against `wc -l` and grep at the head; the PR #841 body Round 4 section against my receipts — the counts and lines follow the generator's rules. The PR text is accurate. The em-dash and TOC gates pass. S1 is optional and out of scope.

## 7. Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merge structure (both sides identical); REGISTER_MAP `:414-415`, `:428`; issue #839 acceptance and decision record; bootsa 67/0 | R773-4 | 4f210018e6556a9753ed409885d82744c8f5effa |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv` PR-side hunk identical to round 3; no dev `hdl/` change; pinned-Verilator rebuild | R773-4 | 4f210018e6556a9753ed409885d82744c8f5effa |
| Robustness | CLEAN | `receipts/bootsa.log`, `receipts/bootsa_mutants.log` (early-enable, single-half arms, 12 controls) | R773-4 | 4f210018e6556a9753ed409885d82744c8f5effa |
| Tests | CLEAN (prior optional SUGGESTIONs retained) | inventory `--write` byte-identity, `--check` stale at `dc7eebff` / fresh at the head (git and no-git), `--selftest` 50; docs.yml steps; bootsa-mutants 13/13 | R773-4 | 4f210018e6556a9753ed409885d82744c8f5effa |
| Docs | CLEAN (S1 and prior SUGGESTIONs optional) | `docs/DOCUMENTATION_AUDIT.md` regenerated rows; page line counts; PR body Round 4 section; em-dash and TOC gates | R773-4 | 4f210018e6556a9753ed409885d82744c8f5effa |

Restore check (`receipts/restore_verify.txt`): HEAD `4f210018`, worktree and index clean, `git write-tree` = `b565b4c16317c1732ba431ff6335ccf46feab8c5`. The `git ls-files -s` digest is recorded. The gitlinks are unchanged: gptp-processor `135afd04`, protocol-processor `a9e84b66`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`, external `efeb541a`. The ignored build outputs from these probes (`obj_bootsa`, hex files, `__pycache__`, `sw/builder/out`) were removed.

## 8. Real limits and pending manager duties

Limits:
- These docs.yml steps were not run:
  - the pip, apt and sv2v install steps, and the RV32 SDK installer, because shared installs are not allowed;
  - `make -C gptp-processor docs`.
  These do not depend on the delta, since gitlinks and generator inputs are unchanged.
- Four renderer-dependent gates ran from a disposable venv with the repository's pinned hashes, not from the hosted image.
- The command-table checker refuses in this environment at both the head and dev. Equivalence rests on there being no `.github/` or `ci/` change.
- The full Verilator, Yosys and parent banks were not run (not allowed). No manager source bank ran at this head, and I do not infer one.
- Hosted contexts were still running at the snapshot.
- In `receipts/bootsa.log` and `receipts/bootsa_mutants.log`, the host-local install path of the pinned Verilator in the compiler command lines is replaced by `<pinned-verilator-root>`. Nothing else in them is edited.
- I verified the published author receipts by hash against `MANIFEST.json`. I did not verify any signature over it.
- Physical calibration was NOT RUN. Field skips are not hardware proof. Issue #839 stays open for the hardware boot capture, per the maintainer decision record.

Pending manager duties:
- Exact-head hosted `rtl-fast`, `verilator-suites`, `yosys-portability` and `docs-check` completion, and act acceptance.
- The current-dev merge candidate (builder and native banks) at the merge turn. Source base and live dev are both `cc204c6f`.
- Carry S1 to #797, and the retained round-2/3 SUGGESTIONs to the author, as optional.
- The external reviewer's round-4 verdict. Merge only with explicit maintainer authorization.

R773-4 FINISHED
