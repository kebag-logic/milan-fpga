[A527] REVIEW READY (round 2)
Commit: 4742d2c02c109f7dd8e21d74905efb182b2dbca2 on `649-resource-map`, not pushed: round-1 head `da0dbc37`, the `--no-ff` merge of dev `fea346e7` (`689a9010`), and seven one-line round-2 commits. Against the merged dev the lane still touches only `syn/resmap/` and two findings pages.

Changed:
- **Ruling (R466-1 F6 = R467-1 F3): the CPU, cache and L2 options are priced.**
  - Method: a scratch-only copy of the recipe with exactly the two profile refusals removed. It is never committed; the tracked `milan_soc.py` is unchanged. The CPU netlists come from scratch copies of the generators, and the shipping netlist is reproduced byte for byte. Then 20 Vivado out-of-context syntheses, one at a time under the shared lock, compared after synthesis because `opt_design` refuses the black-boxed datapath. Every variant is labelled "not buildable under the shipping software profile".
  - Each core: +1,484 LUT (1, 2, 4 cores).
  - Both L1 caches at one way: +1,210 LUT, then +132 LUT and +3.5 BRAM tiles per way (1, 2, 4 ways).
  - L2 on the L1-cached core (8, 16, 32 KiB): its controller is about +1,300 LUT, and its size costs only BRAM.
  - FPU on the M core: F adds 2,569 LUT; D adds 3,548 LUT and 5 DSP.
  - NaxRiscv at RV32: +14,348 LUT.
  - Not generated, even from the copy: F and F+D on the shipping RV32I core. The FPU needs the M extension's unsigned-operand service; the reason is recorded. The FPU keeps three points on the M core, so there is no STOP.
  - XLEN and the core choice are two-valued by nature, so each is priced at two bases.
  - Two measured no-ops: the recipe's `--with-fpu` on the VexiiRiscv path, and `--l2-bytes` on the shipping cacheless core, where the lane's patched generator builds no L2.
- **1 What is tied.** The census tie now reads every row's four LUT columns, leaf and parent, as distinct LUT sites, and all 218 rows of the route equal the report. So every leaf LUT figure and every sharing adjustment is read twice. Partition is stated as an identity. There are five ties and 15 self-test arms, each arm caught by its own tie; the stray-owner check is armed; the `route_map.tcl` depth comment is fixed. The page, the README row, the PR body and both script headers agree.
- **2** A generated "LUT reconciliation" table: the leaves sum to 51,123 LUT, the 17 sharing adjustments by parent total -356 (each beside the census's shared-site count), and the image is 50,767.
- **3** Growth is stated as sub-linear, with the residual signs and the increments.
- **4** The README row says 59 points. There is one census rate: 64 lines a second, from the stopped reopen's own files.
- **5** Guards fail closed: a missing or hard-error record stops the models. New arms cover the stream fit, the processor fit, the TDM model, the calibration and the page check.
- **7** Full rank is asserted, and HEAD plus a clean-tree check go into every sweep receipt; S4 is listed open.
- **8** Residue applied. **9** dev merged.

Validation at `4742d2c0`:
- 48 of 48 local gates rc 0, worktree clean before and after, ignored files included. They include the five self-tests with their new arms, `docs_check` with and without git, `check_em_dash` against both bases, `gen_toc`, `check_doc_paths` and `check_py_idiom`.
- `resmap_tables.py ... --soc-variants ... --page`: "every table equals a fresh generation", rc 0. `resmap_map.py map`: `TIED: 175 blocks, depth 5`.
- `sw/builder/test_builder.py --require-rv32`, in a scratch export: rc 0. Two arms did not run, for their environment: gate 1b's make control, and gate 11, which needs an Arty build tree.
- Reviewer probes, run unchanged:
  - R467-1 `probe_partition.py` stops at its arm-A assertion, because the function it stubs no longer exists; the stated identity answers that. Its arm B, run verbatim, is caught by the census LUT tie.
  - `probe_stray_owner.sh`: the mutant is killed.
  - `probe_selftests.py`: the three F7 mutants are caught; it then stops at the partition arm.
  - R466-1's guard-probe mutant is killed. `mutate_map_selftest.py` stops at `partition-off`, because that mutation site is gone.
- The lane's own mutation probe: 12 of 12 tie mutants killed; the 2 bookkeeping guards that the docstring names as implied survive.

Acceptance criteria:
1. Met. The method is stated exactly, every leaf's LUT, FF, RAMB and DSP figures are read twice, and the totals are tied to the record.
2. Met. Every parameter is priced at three or more points, or is two-valued by nature, and the fits carry residuals; the CPU, cache and L2 parameters are now priced.
3. Met. The SoC synthesis is also calibrated against the route: 1.13 for the SoC, 1.16 for the CPU.
4. Met. Scripts, findings page and receipts are in place; there is no RTL, configuration, shipping-shape or gate-baseline change.

Open risks/questions:
- The round-2 evidence (inputs, logs, probes and manifest) is ready to publish as `review-evidence/649-r2/author/` on `649-review-evidence`; the page names that path.
- The census `map_cells.tsv` (12.5 MB, 540 KB compressed) is over the evidence's 200 KB limit. Its digest is in the manifest, and a compressed copy is staged in the lane's scratch for publishing. Both commands read it. From the published inputs plus the census, a cold re-run reproduces `TIED`, a byte-equal `models.json` and every table equal.
- The #229/#640 summary comment draft is updated and still unposted.
- For the tooling issues: `milan_soc.py --with-fpu` is a silent no-op on the shipping VexiiRiscv path.
- No push, PR edit or merge was done.
