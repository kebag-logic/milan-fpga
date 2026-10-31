[R735] POSITIVE - exact head 683e59712b93b2ef9fc81d22cc21c7d96e4c3909

Composition review, round R735-3, issue #806 / PR #813. The merge-train candidate is `683e59712b93b2ef9fc81d22cc21c7d96e4c3909`, tree `556e790607ad5e53dd9950f6c2e191dcebf3ef0b`. It equals live dev `71d6ed07a59ec35b703b658edc9157d6b454d131` (with #70 and #817 merged) plus PR head `0c45ebf28e2c11352aa4ad40d46780143b1a77ab`. The merge base is `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.

All five lenses were applied to the composition. No BLOCKER, MAJOR, MINOR or new RESIDUE is open. The composed tree introduces no defect beyond the reviewed sources. One prior RESIDUE, R735-2-R1, is retained. It is in a file the composition does not touch.

## What the composition is

- **The candidate is the clean textual merge.** `git merge-tree --write-tree 71d6ed07a 0c45ebf28` produces `556e7906`, which is the candidate tree. There are no merge-time edits (`receipts/integrity.txt`).
- **The overlap is one file.** The PR changes 28 paths since the merge base, and dev changes 31. Only `tb/verilator/milan_dp/README.md` is in both lists. The candidate matches the PR head on every other PR path, and it matches dev on every dev-only path (0 diff lines).
- **The two sides' hunks are disjoint.**
  - The PR changes one line: the `obj_gptp` legs-table row at `README.md:91`, which adds the FPGA-gPTP #94 asCapable/portEnabled checks.
  - Dev changes five places, all for `[VOLATILE]` (#70):
    - the `obj_dynmap` row (`:84`);
    - the leg-order sentence (`:842`);
    - the volatile-set paragraph (`:884-900`);
    - the failing-arms paragraph and measurements (`:904-918`);
    - mutant rows 64 to 66 (`:985-987`).
- **Gitlinks:** `gptp-processor` is `135afd04` (from the PR) and `protocol-processor` is `f65c8ff7`. Neither side changes the protocol-processor link.

## Checks run on the candidate

| Check | Result | Receipt |
|---|---|---|
| Composed README against both parents. Every line either side added appears in the candidate as many times as on that side, and every line either side removed is gone. | dev: 31 added and 5 removed, 0 mismatches. PR: 1 added and 1 removed, 0 mismatches. | `receipts/readme_compose_check.log`, script `readme_compose_check.sh` |
| Mutant table numbering | 66 rows, unique and contiguous 1 to 66, with no lost or duplicated row | same |
| Each `obj_*` leg in the legs table has an existing source and a Makefile reference | 21 of 21 | same |
| `make` targets the README names | each real target is in `milan_dp/Makefile`. `gmstep-mutants` is in `milan_dp_gm_steps/Makefile:34`, as the row says. The other matches are prose ("make the", "make a") | same |
| `dynmap_mutants.py`: all 66 arms still anchor in the composed RTL. Each pattern must match exactly once in its plant file. This guards the PR's `milan_datapath.sv` edit against dev's mutant campaign. | 66 mutations, 0 bad patterns | `receipts/mutant_anchor_probe.log`, script `mutant_anchor_probe.py` |
| `docs_check.py` | 0 findings, 210 md files | `receipts/docs_check_venv.log` |
| `check_em_dash.py --base 71d6ed07…` | 0 findings over 138 added lines in 12 pages, arms 339/339 | `receipts/em_dash.log` |
| `gen_toc.py --verify-anchors` / `--check` | 542 cross-page anchors reproduced; TOC OK across 149 pages | `receipts/toc_anchors.log`, `receipts/toc_check.log` |
| `check_doc_style.py` | OK across 23 documents. The milan_dp README is not in its scope list (`scripts/check_doc_style.py:16-30`) | `receipts/doc_style_venv.log` |
| `check_port_contracts.py`. The PR edits `scripts/port_docs.budget`, and dev's only HDL edit (`KL_mmcm_drp_servo.sv`) adds an attribute and no ports. | pass | `receipts/port_contracts.log` |
| `ci_events.py --check` and `--selftest`, `generate_ci_evidence_pins.py --check`, `ci_gate_workflows.py --check`, `check_rtl_source_lists.py`, `check_gptp_docs.py` (with and without the submodule), `check_submodule_docs.py`, `check_solution_docs.py`, `check_feature_status.py`, `check_doc_paths.py`, `check_diagram_pngs.py`, `measure_test_evidence.py --check`, `check_hygiene.py --check`, `check_cpp_idiom.py`, `check_sv_idiom.py`, `check_todo_ownership.py`, `measure_naming.py --check` | all exit 0 | `receipts/*.log`, `*.rc` |

The renderer-dependent gates first refused to run because the pinned Markdown renderer was not installed (an environment issue). They were rerun from a disposable venv built with `pip install --require-hashes -r tools/markdown/requirements.txt`, which gave cmarkgfm 2025.10.22 and html5lib 1.1.

## Signed local CI packet

The packet is at `review-evidence/806-r1/local-ci/0c45ebf2` at commit `98fe7180`. Receipts: `receipts/sig_verify.log`, `receipts/manifest_inspect.log`, `receipts/manifest_coverage.log`.

1. `manifest.json` sha256 is `dfde2043…a60c`, as stated. `allowed_signers` holds exactly one key, ED25519 `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`, with principal `milan-local-ci`. This is the expected key.
2. `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` exits 0 with a good signature.
3. The subject names candidate `683e5971` (parent `71d6ed07`, tree `556e7906`), head `0c45ebf2` (tree `9aa29667`) and PR 813.
   - All four workflow definition hashes match the candidate's `.github/workflows/*`.
   - The result is success.
   - All 47 coverage entries are `ok: true`: 46 by act, plus 1 `not-run` (`rtl/physical-gptp`). Its named reason is that the job runs only on schedule or dispatch and is not hardware evidence.
   - Of the 68 act jobs, only that skipped job is not success.
   - The banks match the packet's claims: manager-builder ran 48 of 48 commands and full-native ran 5 of 5, each with exit 0.

## Findings

No new finding.

**Prior public findings, resolved or retained at this head.** I read them after my own pass.

- **R736-1-R1 (RESIDUE, Docs): stays RESOLVED.** R735-2 and R736-2 resolved it at `0c45ebf2`. The composition does not touch the files it covers.
- **R735-2-R1 (RESIDUE, Docs, `docs/design/AREA_BUDGET.md:146`): RETAINED.** The candidate still reads "The next growth on the shipping image therefore has no slice room". Dev does not touch the file, so the bytes are the source's. It stays on the residue checklist with the fix the earlier rounds gave.
- **R735-1 S1 to S5, R735-2 S6 and S7, R736-2-S1 and S2 (SUGGESTION): retained.** They are optional, and the composition touches none of their artifacts.

**Comment rule.** The composition adds no source line beyond the two reviewed parents, because the tree is the clean merge. So it adds no new comment instance.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The composition touches no protocol logic. The only shared file is the README, and its `obj_gptp` row (IEEE 802.1AS-2011 10.2.4.11 via #94) and its `[VOLATILE]` text (Milan v1.2 5.3.4.1, 5.3.4.2, 5.3.12) are byte-identical to their sources. The source-head protocol claims are covered by R735-2 and R736-2 at `0c45ebf2`. | R735-3 (composition); R735-2, R736-2 (source) | 683e59712b93b2ef9fc81d22cc21c7d96e4c3909 |
| RTL | CLEAN | The candidate's RTL equals the PR head on PR paths and dev on dev paths: `hdl/milan/milan_datapath.sv` (PR) and `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:1292-1294` (dev: ASYNC_REG plus a comment, no ports, no logic) are disjoint. Gitlinks: `135afd04` and `f65c8ff7`. Gates: `check_port_contracts.py`, `check_rtl_source_lists.py` and `check_sv_idiom.py` pass. The source RTL is covered by R735-2 and R736-2. | R735-3; R735-2, R736-2 | 683e59712b93b2ef9fc81d22cc21c7d96e4c3909 |
| Robustness | CLEAN | The composition adds no new input, state or reset path. The disjoint files are listed in `receipts/integrity.txt`. The source robustness work is covered by R735-2 and R736-2 at `0c45ebf2`, and by dev's own #70 and #817 reviews. | R735-3; R735-2, R736-2 | 683e59712b93b2ef9fc81d22cc21c7d96e4c3909 |
| Tests | CLEAN | `tb/verilator/milan_dp/README.md` legs table: 21 of 21 legs have a source and a Makefile target. Mutant rows run 1 to 66 contiguously. All 66 `dynmap_mutants.py` arms anchor exactly once in the composed `milan_datapath.sv`, `KL_pp_shadow.sv` and processor leaves. The Makefile's 66-arm comment (`Makefile:652-654`) agrees with the README. `sim_gptp.cpp` (PR) and `sim_nxn.cpp` (dev) are disjoint. The signed packet covers the candidate's banks (48/48, 5/5) and an act replay of the PR head. | R735-3 | 683e59712b93b2ef9fc81d22cc21c7d96e4c3909 |
| Docs | CLEAN (RESIDUE R735-2-R1 retained, unaffected) | The composed README was checked section by section against both parents (`receipts/readme_compose_check.log`). Gates: `docs_check.py`, `gen_toc.py --verify-anchors/--check`, `check_em_dash.py --base 71d6ed07`, `check_doc_style.py` (the README is out of its scope), `check_doc_paths.py`, `check_gptp_docs.py`, `check_submodule_docs.py`, `check_solution_docs.py`, `ci_events.py --check`. The in-page anchor `#the-658-power-on-audio-maps-obj_dynmap` resolves to `README.md:837`. | R735-3 | 683e59712b93b2ef9fc81d22cc21c7d96e4c3909 |

## Real limits

- I built no RTL and ran no simulation, suite or mutant campaign on this candidate. Execution evidence for the composed tree is the manager's signed banks. I verified the packet but did not rerun it. The act replay in the packet ran on PR head `0c45ebf2`, not on the candidate.
- The route figures on `docs/design/AREA_BUDGET.md:141-145` describe the source build (FPGA-gPTP `135afd04` on processor `f65c8ff7`): 15,823 slices, 27 free, +0.032 / +0.034 ns, refused by the gate. Dev's #817 adds an ASYNC_REG attribute and an asynchronous cut on the servo's ps_clk reset-sync input. That change cannot alter LUT or FF counts, but the composed tree has not been placed and routed. No Vivado run was made in this round. This is a limit, not a finding: the page pins its figures to the named submodule heads, not to a parent commit.
- Physical calibration was NOT RUN. The `physical-gptp` job was skipped by design. Field skips are not hardware proof.
- This round did not examine hosted exact-head runs. The manager owns hosted and act acceptance.

## Pending manager duties

- Publish this report and the receipts listed in `MANIFEST.sha256`.
- Carry R735-2-R1 to the residue checklist.
- At the merge turn, confirm live dev is still `71d6ed07`. If dev has moved, the candidate must be rebuilt and re-reviewed.
- Hosted exact-head contexts and the maintainer's merge authorization remain mandatory.

R735-3 FINISHED
