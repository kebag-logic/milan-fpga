[R550] POSITIVE - exact head b959830acd53a868febfe362974e33e144481aa7

Round R550-3. This is a composition review of the issue #654 / PR #694 merge-train candidate. Candidate commit `b959830acd53a868febfe362974e33e144481aa7`, tree `be74ac164d59496f91af1474ca0621e2ce09aac0`. Its parents are live dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240` and the PR source head `853a7357ba86d758a0e38f65db89a6187fb547bc`. The review covers the composition only. Both source reviews at `853a7357` are POSITIVE: the internal review [R550-2](https://github.com/kebag-logic/milan-fpga/pull/694#issuecomment-6047401298) and the external review [R551-2](https://github.com/kebag-logic/milan-fpga/pull/694#issuecomment-6047390785).

Verdict: the composed tree introduces no defect beyond the reviewed sources. This round raises no finding of any severity. One optional SUGGESTION from R550-2 stays open, unchanged by the composition (section 6). Every other prior finding is resolved at this head.

## 1. Context reconstructed

I read the following, in order:

- AGENTS.md and CONTRIBUTING.md, including section 7 on candidate-merge validation and the em-dash gate.
- docs/README.md.
- The issue #654 body, its three acceptance items and the assignment (6045462105).
- The resume ruling (6045774790), which narrows acceptance item 3 to the two AX7101 product configurations and puts Arty under #583.
- The round-2 assignment (6046709819).
- The PR #694 body.
- The full candidate diff against dev, and the history of both parents.
- The public author evidence under `review-evidence/654-r1/author*` at `a2917fb3`. I used `export_compare.py` from it as the model for my own export harness.

I did not read any other reviewer's report before writing the verdict and ledger. Prior findings are reconciled in section 6, which was written afterwards.

## 2. Composition identity (receipt `receipts/composition.txt`)

- Merge base of dev and the PR is `e21c1ca0`, the PR's assigned base.
- `git merge-tree --write-tree 99e4eb6c 853a7357` reproduces `be74ac16`, so the candidate is the clean three-way merge with no hand edits.
- The candidate-vs-dev patch is identical to the PR-vs-base patch, ignoring index lines and hunk headers.
- `sw/litex/milan_soc.py`, `sw/builder/test_builder.py` and `sw/builder/test_soc_options.py` are byte-identical to the reviewed source head (blobs `6f36cdcc`, `4e9fb30a`, `f12c185d`). Dev did not touch them after `e21c1ca0`.
- **The only file both sides changed is `docs/integration/BUILDING.md`.** The PR changed lines around 130-163 (CPU option refusals). Dev's #691/#693 work changed it around 607-630 (GMII RX capture, patch 0007 and the placement fixture command). A standalone `git merge-file` of base, PR and dev exits 0 with no conflict, and its output is byte-identical to the candidate blob (`e4add203...`).

## 3. Semantic interaction checks

- **BUILDING.md, both regions, read in full at the candidate.**
  - PR region: candidate lines 129-163. Line 133 reads "the section 2.1 refusals then apply to that config", and section 2.1 is still the heading at line 165 ("What `build.sh` refuses, before anything launches"), directly after the PR's block. The option table, the whole-byte rules and the two test commands are intact and appear once.
  - Dev region: candidate lines 637-661. The GMII RX capture paragraph, the fixture command block and the nine-PASS / nine-expected-FAIL expectation are intact and appear once. The paragraph still sits between the IOB-PACK FAIL paragraph and the INERT paragraph, which is where dev placed it.
  - No text was lost or duplicated, and neither side added or renamed a heading.
  - The page's generated blocks (feature-status, solution-cpu-contract, Contents) are unchanged by either side and still pass their checkers.
- **Patch series vs option validation.**
  - Dev added `0007-liteeth-gmii-rx-capture.patch` to `sw/litex/patches/apply.sh` and the patch README. It touches only liteeth.
  - The PR's refusals run in `main()` before the product-profile check and platform construction, and in `MilanSoC.__init__` before CPU setup. They read only `cpu`, `with_fpu` and `l2_bytes`.
  - The VexiiRiscv L2 refusal rests on patch 0005 (cacheless), which dev did not change.
  - No dev-changed file passes `--with-fpu` or `--l2-bytes`, or constructs `MilanSoC`. I grepped all 91 dev-changed paths. The only hits are documentation prose already on the page.
- **Registries and inventories.**
  - The PR registers `test_soc_option_refusals` in the builder main tuple, which dev did not touch.
  - Dev added `test_gmii_rx_capture` to the `run_litex_sims.sh` inventory, which the PR did not touch. The PR's new test lives in `sw/builder/`, outside that inventory's reconciliation.
  - Workflow contracts (`ci_events.py --check`) and test-evidence and naming measurements pass at the candidate.

## 4. Gates run at the candidate (all rc 0; receipts `receipts/gates/*.log|rc`, summary `receipts/gates_summary.txt`)

The runner is `run_gates.sh` with `gates.txt`, running at most 16 jobs in parallel.

Documentation gates, run with an interpreter carrying the locked renderer:

| Gate | Result |
|---|---|
| `docs_check.py` | 0 findings over 199 md files |
| `check_doc_style.py`, `check_doc_paths.py` | rc 0 |
| `gen_toc.py --check` | OK, 139 pages |
| `gen_toc.py --verify-anchors` | 401 cross-page fragment links reproduced |
| `check_em_dash.py --base 99e4eb6c` (the dev parent, the base a docs job derives at this candidate) | 0 findings over 31 added lines on 1 page |
| `check_em_dash.py --base e21c1ca0` | 0 findings over 1148 added lines on 15 pages |
| `check_em_dash.py --selftest` | rc 0 |
| `check_solution_docs.py`, `check_feature_status.py` | rc 0 (both read BUILDING.md blocks) |
| `gen_module_matrix.py --check` | rc 0 |

Other gates, all rc 0:

- `ci_events.py --check`: 1741 items. `ci_events.py --selftest`: rc 0.
- `check_py_idiom`, `check_soc_sources`, `check_hygiene --check`, `measure_fail_fast/naming/test_evidence --check`.
- The sweep, deploy and entity shape self-tests.
- `check_gptp_docs`, `check_submodule_docs`, `check_port_contracts`, `check_todo_ownership`, `check_baremetal_only --check`.

LiteX gates used the bench interpreter. I confirmed read-only (`git apply --reverse --check`) that all five patches in the series, 0007 included, are applied in its trees:

- `sw/builder/test_soc_options.py`: 52 constructor cases, 18 CLI cases, 9 killed controls, PASS.
- `builder_subset.py` ran three arms with no skip recorded: the PR's registered `test_soc_option_refusals`, gate 23h `test_toolchain_patches_are_applied` ("the 5 patches in sw/litex/patches are the 5 apply.sh applies ... reproduces all 4 installed files byte for byte"), and its control `test_toolchain_patch_gate_bites` (5/5 fixtures rejected).
- `scripts/run_litex_sims.sh`: 5 run, 5 passed, 0 skipped, 0 timed out. Dev's new `test_gmii_rx_capture` is included. Verilator was the scoped 5.050 wrapper, which reports `Verilator 5.050 2026-07-01 rev v5.050`.

## 5. Composition probes (receipts `receipts/probes/*`, script `probes.sh`)

All probes ran on a disposable clone of the candidate. Each one confirmed the gate green on exact bytes, planted one defect, required red, then restored and re-verified the blob and HEAD. The two em-dash plants were committed locally in the disposable clone, because that gate reads committed history. The clone was reset to the candidate afterwards.

| Probe | Plant | Gate | Result |
|---|---|---|---|
| `em_dash_pr_region` | em dash in the PR's option table row | `check_em_dash --base 99e4eb6c` | KILLED (BUILDING.md:142) |
| `em_dash_dev_region` | em dash in dev's GMII paragraph | same | KILLED (BUILDING.md:639) |
| `solution_cpu_block` | deploy L2 cell 0 -> 8192 | `check_solution_docs` | KILLED ("product contract table differs from source") |
| `toc_contents` | rename section 2 heading | `gen_toc --check` | KILLED (TOC DRIFT BUILDING.md) |
| `vexii_fpu_refusal` | disable the VexiiRiscv FPU refusal | `test_soc_options.py` | KILLED |
| `apply_series_0007` | drop 0007 from `apply.sh` SERIES | builder subset (gate 23h) | KILLED ("only in the directory ['0007-...']") |

**AX7101 byte identity at the composed tree** (receipts `receipts/export/*`, script `compose_export.py`). Acceptance item 3, as narrowed by the ruling, was checked against the merge result rather than against the source base. I generated both product configurations in the candidate tree with the 0007-patched LiteX twice: once with dev's `milan_soc.py` blob (`551d6aae`) and once with the candidate's (`6f36cdcc`). Both runs used identical fixed time and diagnostic Instance-repr inputs, and nothing generated was normalized. Result: `ax7101_1x1_tdm8` 32/32 and `ax7101_8x8` 32/32 artifacts byte-identical.

The VexiiRiscv netlist cache came from an isolated copy, and nothing under the shared install was written during the run.

A first attempt ran the interpreter with `-I`. That implies `-E` and drops `PYTHONHASHSEED`, so the CPU ISA string, which is spelled from a set, differed between the two phases. This was a defect in my harness, not in the candidate. The rerun used `-P -s` with the seed pinned. The first attempt is kept unpublished under `scratch/`.

## 6. Prior public findings at this head

This section was written after the verdict and ledger above. The prior rounds are:

- [R551-1](https://github.com/kebag-logic/milan-fpga/pull/694#issuecomment-6046673982), NEGATIVE at `d6b6ca89`.
- [R550-1](https://github.com/kebag-logic/milan-fpga/pull/694#issuecomment-6046704603), POSITIVE at `d6b6ca89`.
- [R551-2](https://github.com/kebag-logic/milan-fpga/pull/694#issuecomment-6047390785) and [R550-2](https://github.com/kebag-logic/milan-fpga/pull/694#issuecomment-6047401298), both POSITIVE at `853a7357`.

Each finding was re-checked at the candidate. Receipts: `receipts/prior_findings_recheck.log`, the gate logs and the candidate source lines. The composition keeps each source resolution intact.

| Prior finding | Status at `b959830a` | Evidence at this head |
|---|---|---|
| R551-1-F1 MINOR (Conformance, Robustness, Tests, Docs): fractional byte counts underflow to an accepted zero | **Resolved, retained by the composition** | `--l2-bytes 1e-400`, `-1e-400` and `0.5` each exit 2 with "--l2-bytes must be a finite, non-negative whole number of bytes"; `8192` exits 2 with the cacheless reason (`receipts/prior_findings_recheck.log`). Bank: "killed: lossy byte-count parsing: 1e-400 / -1e-400" (`receipts/gates/soc_options_bank.log`). Parser at `sw/litex/milan_soc.py:2573` |
| R550-1 RESIDUE (Docs): `BUILDING.md:133` "the refusals below" | **Resolved, retained** | Candidate `docs/integration/BUILDING.md:133` reads "the section 2.1 refusals", and section 2.1 is still at `:165` after the merge |
| R550-1 SUGGESTION S1 (Docs, Tests): name `--nax-data-dir` | **Resolved, retained** | Candidate `docs/integration/BUILDING.md:158-161` |
| R550-1 SUGGESTION S2 (Robustness): an unknown constructor CPU bypasses the NaxRiscv zero refusal | **Resolved, retained** | `_validate_cpu_options("bogus", False, 0)` raises "unsupported CPU 'bogus'" (`receipts/prior_findings_recheck.log`). Guard at `sw/litex/milan_soc.py:2584` |
| R550-2 SUGGESTION (Docs): `BUILDING.md:154-155` should name the interpreter the option tests need | **Open, optional** | Text unchanged at candidate `:154-155`. It is a SUGGESTION, so it does not affect lens coverage or the verdict. The composition neither worsens nor resolves it |
| R551-2 | No open item | That round records no open finding |

## 7. Receipts

Published receipts are the files listed in `MANIFEST.sha256`, plus this report. Raw logs are unedited, with one exception: absolute host paths are replaced by placeholders before hashing.

- `<packet>` is this packet.
- `<candidate-clone>` is the detached candidate clone.
- `<docs-venv>` is the interpreter carrying the locked renderer.
- `<bench-litex>` is the bench LiteX installation.
- `<home>` is the user home.

Scripts: `run_gates.sh` + `gates.txt`, `builder_subset.py`, `probes.sh`, `compose_export.py`. Disposable trees stay under `scratch/` and are not published: the probe clone, the isolated VexiiRiscv data copy, export snapshots, the first export attempt and the sim logs.

## 8. Reviewer-owned ledger

| Lens | Status | Composition touches scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes: acceptance item 3 (product configurations unchanged) must hold on the merge result | `receipts/export/*` (both AX7101 configurations, 32/32 raw-identical, dev vs candidate recipe in the composed tree); `sw/litex/milan_soc.py` blob identity with the source head; acceptance items 1-2 via `receipts/gates/soc_options_bank.log` and `builder_subset.log` | R550-3 | `b959830acd53a868febfe362974e33e144481aa7` |
| RTL | CLEAN | No: neither side's interaction touches HDL. The PR changes no RTL, and the only file both sides changed is BUILDING.md. The generated gateware in the composed tree is byte-identical with and without the PR (`receipts/export/*`) | `receipts/composition.txt` (changed-path intersection); export identity of `export/gateware/alinx_ax7101.v`; source RTL coverage from the reviews at `853a7357` | R550-3 (composition); source by R550-2 and R551-2 | `b959830acd53a868febfe362974e33e144481aa7` (source `853a7357ba86d758a0e38f65db89a6187fb547bc`) |
| Robustness | CLEAN | Yes, for the ordering of refusals versus dev's patch series and setup | `sw/litex/milan_soc.py:2573-2599,2624,3802-3805` at the candidate; dev-changed-path grep; `receipts/gates/soc_options_bank.log`; probe `vexii_fpu_refusal` | R550-3 | `b959830acd53a868febfe362974e33e144481aa7` |
| Tests | CLEAN | Yes: the builder registry, the LiteX sims inventory (dev added `test_gmii_rx_capture`) and gate 23h over the 0007-extended series | `receipts/gates/builder_subset.log`, `litex_sims.log`, `ci_events_*.log`, `test_evidence.log`; probes `apply_series_0007` and `vexii_fpu_refusal` | R550-3 | `b959830acd53a868febfe362974e33e144481aa7` |
| Docs | CLEAN | Yes: `docs/integration/BUILDING.md` was changed by both sides | Candidate BUILDING.md:129-165 and 637-661 read in full; `receipts/composition.txt` (merge-file identity); `receipts/gates/{docs_check,doc_style,doc_paths,toc_check,toc_anchors,em_dash_*,solution_docs,feature_status,module_matrix}.log`; four doc probes | R550-3 | `b959830acd53a868febfe362974e33e144481aa7` |

## 9. Real limits

- I did not run the full builder, Verilator, Yosys, protocol-processor or gPTP banks, by rule. The builder coverage here is the three composition-relevant arms only.
- I did not run `lint_rtl.py --check`, because the composition changes no HDL.
- I did not run `test_soc_options.py --netlists`. It needs the NaxRiscv generator, and no NaxRiscv input changed on either side.
- The candidate commit is not on GitHub, so no hosted run exists at `b959830a`. Hosted checks at the source head `853a7357` show 22 executed contexts succeeded and 1 skipped ("Physical gPTP (nightly and manual)"). That skip is not hardware proof. The manager owns hosted and act acceptance.
- No physical calibration, synthesis, implementation or hardware run was made. The export identity is a generated-artifact claim only.
- The bench LiteX interpreter was used as found, with its series verified read-only. The VexiiRiscv netlist data came from an isolated copy.

## 10. Pending manager duties

- Validate the current-dev merge candidate with the builder and native banks at the merge turn, and link the receipts on the PR.
- Confirm live dev is still `99e4eb6c` when merging. If dev moves, this composition verdict does not carry over.
- Hosted and act acceptance at the merged head, then post-merge containment (`check_merge_containment.py`, `check_merge_review_integrity.py`).
- Close #654 and move it to Done.

## 11. Restoration

The review clone was verified after all runs (`receipts/state_before.txt` and `receipts/state_after.txt` are identical):

- HEAD and tree are as above, and the `git ls-files -s` digest is unchanged.
- Index and worktree match HEAD.
- The submodule gitlinks are unchanged: protocol-processor `2ad2f845`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`, external `efeb541a` (uninitialized). Their worktrees are clean.
- Ignored build products created by the gates (Python caches, `sw/builder/out/`, `tb/verilator/gptp_txts/obj_pad/`) were removed with `git clean -fdX` after listing them. None existed before the run.

R550-3 FINISHED
