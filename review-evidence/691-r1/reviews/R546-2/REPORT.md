[R546] POSITIVE - exact head ba080007a402dced74fa74656338710e0b6cb880

# R546-2 internal cleared-context review: issue #691 / PR #693

- Head `ba080007a402dced74fa74656338710e0b6cb880`, tree `6e18c4f36d5bf75ab61a5a7fd8d691d9644d985a`. Delta under review: `35fb2a95..ba080007` (one commit). Source base `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`. The PR head was re-read at the end of the round and was unchanged (`receipts/environment.txt`).
- Read in this order: AGENTS.md and CONTRIBUTING.md; docs/README.md; the #691 body; assignment 6041364533; STOPs 6042535076 and 6045727339; rulings 6042557053 and 6045752839; round-2 assignment 6046111178; REVIEW READY 6046891932; REQUIREMENTS.md section on the MAC (REQ-MAC-01..08, untouched); `docs/integration/BUILDING.md:597-636`; `docs/testing/TESTING.md:514`; `sw/litex/gen_mac_tx_model.py`; `tb/verilator/gptp_txts/Makefile:86-91`; `sw/litex/platforms/alinx_ax7101.py:47-61`; the full diff `e21c1ca0..ba080007` and the round-2 delta; and the public evidence `c963b35b:review-evidence/691-r1/author-r2` (ROUND2-IOB.json, ROUND2-MODEL.diff, ROUND2-ARTIFACTS.json, ROUND2-GATES.json, ROUND2-SOURCE.json, both ROUND2 compact IOB reports).
- No manager evidence comment beyond the review-start notices exists on the issue or PR. Prior public review findings (R546-1 and R547-1) were read only after the independent pass over the diff and probes. Their disposition is below.
- The capture fix is unchanged since `35fb2a95`. `git diff 35fb2a95 ba080007` touches none of `sw/litex/patches/0007-liteeth-gmii-rx-capture.patch`, `hdl/`, `configs/` or `sw/litex/milan_soc.py`. The seven changed paths are BUILDING.md, the new `.xdc` and `.tcl`, `apply.sh`, `test_gmii_rx_capture.py`, and the two generated gptp_txts files.

## Method

- **Interpreter.** A private interpreter was built under `scratch/`. It has pristine archives of all seven `sw/litex/litex_pins.txt` revisions, plus the LiteX-pinned VexiiRiscv `Soc.scala` that 0005 patches. The head's `sw/litex/patches/apply.sh` was applied to it (`receipts/apply_series.log`: 5 patches, rc 0). A second interpreter, identical except that 0007 is reversed, serves as the discriminating control.
- **Simulator.** The scoped simulator identifies as `Verilator 5.050 2026-07-01 rev v5.050`, with its binary hash in `receipts/environment.txt`. The gptp_txts log shows it was the one invoked.
- **Placement.** One locked Vivado placement was run with the compact fixtures only, exactly as in BUILDING.md. A second locked compact run placed the pre-patch receiver as a probe. No full-image synthesis or implementation was run, and nothing ran beside another heavy job.
- **Probe trees.** Probes and builds used `git archive` copies under `scratch/`. The review clone was used read-only, apart from bytecode caches created by the run, and those were removed. Final integrity is in `receipts/final_integrity.log`: 1,168 root blobs match in bytes and mode, the index equals the HEAD tree, and the three required gitlinks are at their pins and clean. The optional `external` submodule is not initialised. The clone has no untracked or ignored files.

## Verification of the round-2 items

**R546-1-F1 (MAJOR): RESOLVED.**

- At the head, `gen_mac_tx_model.py --check` under the full five-patch interpreter reports `checked by re-converted from the product source` (2,683 lines), with rc 0 (`receipts/gen_check_head.log`).
- A 2x2 control matrix discriminates (`receipts/gen_check_controls.log`). Without 0007 the old artifact would still be accepted, so 0007 is exactly what makes the old artifact stale.

  | Stack | Head artifact | `35fb2a95` artifact |
  |---|---|---|
  | All five patches | OK, rc 0 | STALE, rc 1 |
  | 0007 reversed | STALE, rc 1 | OK, rc 0 (2,682 lines) |

- The diff is confined to the GMII RX stage (`receipts/mac_tx_chain-round2.diff`, identical in its `.v` portion to the published `ROUND2-MODEL.diff`).
  - Only `phy_source_valid`, `phy_source_payload_data`, `phy_dv_d` and `phy_rx_*` declarations changed (lines 52-61).
  - The three RX assigns changed (lines 825-827).
  - The `eth_rx_clk_1` capture process changed (lines 2207-2213). The pads now load `phy_rx_dv`/`phy_rx_data` with no reset branch, and `phy_rx_reset` samples `eth_rx_rst` in the same domain.
  - The manifest changed only in `verilog_sha256` (now `f3f110e9…`).
- `make -C tb/verilator/gptp_txts`, run on an exact-head copy with `MILAN_LITEX_PYTHON` set to the five-patch interpreter and `VERILATOR` set to the pinned simulator, returned rc 0 (`receipts/gptp_txts_make.log`).
  - The model check passed at the strong level.
  - The suite ran 85 checks with 0 failures.
  - `mutants.py` caught 6/6 controls.
  - The probe tree was clean afterwards.
- No other committed artifact converts LiteEth RX. In the root and in all three initialised submodules, the only file carrying a Migen/LiteX generation banner is `tb/verilator/gptp_txts/generated/mac_tx_chain.v`.
  - The only data or Verilog artifact naming `rx_dv` is that same file.
  - Other `liteeth` hits are prose, pins, or the historical `docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json` input manifest. That manifest is a measured-commit record, not a conversion.

**R546-1-F2 (MINOR): RESOLVED.**

- The BUILDING.md command was run verbatim from the head clone. `SCRATCH` was set to a scratch path, `VIVADO_LOCK` to the exclusive implementation lock, and `MILAN_LITEX_PYTHON` to the patched interpreter (`receipts/vivado_capture_check.log`).
- The emitter returned rc 0, and the driver returned `vivado_rc=0`.
- The driver printed `GMII capture placement: 9 PASS / 9 expected FAIL`:
  - The good fixture placed all nine captures as FDRE in ILOGIC.
  - The planted fixture reported nine `FAIL … IN, no register reads the pad, only: LUT2…` rows and an `IOB-PACK FAIL: 9 port(s)` refusal.
  - The only critical warnings were the nine expected Place 30-722 terminals on the planted fixture.
- Both live reports are byte-identical to the published `ROUND2-capture-*-capture_iob_pack.rpt` (`receipts/live-*.rpt`).
- The emitted fixtures match the published round-2 hashes `a0bd28a2…` and `f300dcf3…`.
- The `.xdc` LOCs are the platform's eth0 pins: `rx_dv` M22, `rx_data` N22 H18 H17 M21 L21 N20 M20 N19, and `rx` clock K18 (`sw/litex/platforms/alinx_ax7101.py:47-58`).
- The driver is not a rubber stamp (`sw/litex/gmii_rx_capture_check.tcl:30-43`):
  - It requires exact counts on both sides: 9/0/0 for the good fixture, and 0/9/0 with nine named "no register reads the pad" rows for the planted one.
  - It requires the checker's own refusal message.
  - It errors on a wrong argument count or a missing fixture.

**R546-1-R1 (RESIDUE): RESOLVED exactly.** `sw/litex/patches/apply.sh:9-10` is byte-identical to the two prescribed lines.

**R546-1-R2 (RESIDUE): RESOLVED exactly.** PR #693 body, Description, line 43 carries the prescribed sentence verbatim. The old sentence is gone.

**R546-1-S1 (SUGGESTION): ADOPTED.**

- `sw/litex/test_gmii_rx_capture.py:96-128` adds the structural check and its six text controls. `main` runs both before `--emit-dir` (line 148). The live run reports 1,036 comparisons and 6/6 controls caught (`receipts/test_gmii_rx_capture.log`).
- Independently, six source-level mutants of the patched `liteeth/phy/gmii.py` were planted in private copies (`scripts/probe_capture_mutants.sh`, `receipts/probe_capture_mutants.log`).
  - Five were caught. Restoring the reset on valid and restoring the reset on data are caught only by the new structural check, which proves it adds discrimination beyond the behavioural oracle. A live reset in the valid mask, an unmasked data path, and `last` taken from the unmasked delayed valid are caught behaviourally.
  - The sixth, an `rx_reset` initial value of 0, survives. It is equivalent: the captured `rx_dv`/`rx_data` initialise to 0, so the visible outputs are identical from power-up.

**R546-1-S2 (SUGGESTION): ADOPTED.** The published `ROUND2-IOB.json` lists all six rows, each with 21 PASS, 1 INERT and 0 FAIL. This matches the sweep table in the PR body and the issue.

**R547-1:** recorded no findings, so there is nothing to carry.

## Findings at this head

### R546-2-R1 - RESIDUE - Docs - PR #693 body, section "Round 2", second-to-last paragraph

- **Evidence:** the body says "All jobs have ended. The new head remains local and requires independent re-review." The head `ba080007` is now the pushed PR head (`gh pr view 693` headRefOid).
- **Impact:** this is wording only. It changes no measurement, verdict, test, code, artifact or clause claim.
- **Exact fix:** replace "The new head remains local and requires independent re-review." with "The new head is the PR head and requires independent re-review."
- **Verification:** the sentence reads as replaced in the PR body.

### R546-2-S1 - SUGGESTION - Tests, Docs - `sw/litex/gmii_rx_capture.xdc:4-14`; `docs/integration/BUILDING.md:612-630`

- **Evidence:** the compact `.xdc` restates the platform's eth0 RX LOCs by hand, and no gate ties them to `alinx_ax7101.py`. They agree today.
- **Probe:** a locked compact placement of the pre-patch receiver, with 0007 reversed, also packs all nine captures in ILOGIC at control-set threshold 100 (`receipts/old-design-capture_iob_pack.rpt`, `receipts/vivado_old_design_probe.log`). The compact fixture therefore proves the checker refuses a reset-before-D structure. It does not reproduce the full-image control-set remapping. BUILDING.md does not claim that it does, and the full-image evidence is the six-row sweep.
- **Optional outcomes:**
  - derive the `.xdc` LOCs from the platform, or add a one-line cross-check;
  - add one sentence to BUILDING.md saying the compact placement grades the checker's refusal, not the synthesis heuristic.
- **Effect on this review:** neither outcome blocks.

No BLOCKER, MAJOR or MINOR finding is open at this head.

## Lens results

```text
[R546] PASS Conformance — #691 acceptance 1-5 under rulings 6042557053/6045752839; patch 0007 unchanged since 35fb2a95; tb/verilator/gptp_txts/generated/mac_tx_chain.v:52-61,825-827,2207-2213; receipts/gen_check_controls.log; receipts/vivado_capture_check.log — acceptance 1: the converted product chain at this head captures the nine pads with no reset or enable; acceptance 3: the planted reset-before-D defect is refused by the #475 check from the tree alone (9/9 named rows), and the existing datapath suite carrying the receiver now models the receiver the product builds (strong re-conversion, 85/0, 6/6); acceptance 5: round 2 changes no product source, config, register map or default selection; acceptance 2/4 evidence (six-row sweep) is unchanged from the R546-1/R547-1 baseline since no build input changed
[R546] PASS RTL — tb/verilator/gptp_txts/generated/mac_tx_chain.v:59-61,825-827,2207-2213; sw/litex/gmii_rx_capture_check.tcl:11-43; receipts/live-*-capture_iob_pack.rpt — sampled reset is eth_rx_rst in the same eth_rx_clk domain (no new crossing), phy_rx_reset init 1 preserves the zero visible state, last = ~pads_rx_dv & masked valid as upstream, widths 1/8 unchanged; compact placement puts all nine captures as FDRE in ILOGIC and the LUT-before-D control in slices
[R546] PASS Robustness — sw/litex/gmii_rx_capture_check.tcl:5,13,30-43; sw/litex/test_gmii_rx_capture.py:96-128; receipts/probe_capture_mutants.log; receipts/vivado_old_design_probe.log — the driver refuses a wrong arg count, a missing fixture, any count drift on either side, and a refusal without the checker's own message; the structural check accepts only the pinned converter's single capture process and fails closed on shape change; source mutants restoring a pad reset or using live reset are refused; the one survivor is an equivalent init-value mutant
[R546] PASS Tests — sw/litex/test_gmii_rx_capture.py:88-150; tb/verilator/gptp_txts (receipts/gptp_txts_make.log); sw/litex/iob_pack_selftest.py (receipts/iob_pack_selftest.log: 22 arms, 21 mutants, 0 failures); receipts/gen_check_controls.log — the strong model check discriminates both stale directions; the suite is green with 85/0 and 6/6; 6/6 built-in structural controls and 5/5 non-equivalent source mutants are caught; the test is in the scripts/run_litex_sims.sh:99-105 inventory
[R546] PASS Docs — docs/integration/BUILDING.md:612-630; sw/litex/patches/apply.sh:6-15; sw/litex/patches/README.md:11-15; PR #693 body; receipts/docs_check.log (0 findings), receipts/check_em_dash.log (0 findings), receipts/check_hygiene.log (rc 0) — the documented command reproduces the stated 9 PASS / 9 expected FAIL with exit 0 and the stated reason text; the apply.sh header names all five patches; PR-body Round 2 claims match the receipts; the one stale PR-body sentence is RESIDUE R546-2-R1
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #691 acceptance 1-5 and rulings; 0007 unchanged; generated mac_tx_chain.v RX stage; gen 2x2 controls; locked compact placement; ROUND2-IOB.json | R546-2 | ba080007a402dced74fa74656338710e0b6cb880 |
| RTL | CLEAN | mac_tx_chain.v:52-61,825-827,2207-2213; gmii_rx_capture_check.tcl; gmii_rx_capture.xdc versus alinx_ax7101.py:47-58; live and old-design IOB reports | R546-2 | ba080007a402dced74fa74656338710e0b6cb880 |
| Robustness | CLEAN | driver refusal paths; structural-check fail-closed shape; six source mutants; old-design placement probe | R546-2 | ba080007a402dced74fa74656338710e0b6cb880 |
| Tests | CLEAN | test_gmii_rx_capture.py (1,036 comparisons, 6/6); gptp_txts make (strong model, 85/0, 6/6); iob_pack_selftest (22/21/0); run_litex_sims.sh inventory | R546-2 | ba080007a402dced74fa74656338710e0b6cb880 |
| Docs | CLEAN (RESIDUE R546-2-R1 carried) | BUILDING.md:612-630; apply.sh:6-15; patches/README.md; PR #693 body; docs_check, check_em_dash, check_hygiene | R546-2 | ba080007a402dced74fa74656338710e0b6cb880 |

## Real limits

- **No full-image implementation was rerun.** The six-row sweep, with WNS/WHS and the full IOB reports, is author evidence at `35fb2a95` that R546-1 and R547-1 accepted. Round 2 changes no build input: the patch, product source and configuration are byte-unchanged. Only the compact fixtures were placed live.
- **The compact fixture does not reproduce the heuristic.** The pre-patch receiver also packs in it (see S1). The placement control proves the checker's refusal; the structural fix and the full-image sweep carry acceptance 1 and 2.
- **Banks not run.** The complete builder, `run_litex_sims.sh`, the parent, PP and gPTP banks, the Yosys portability bank and the full suite sweep were not run here, as instructed. The manager's source-bank pass and the author's round-2 builder, sims and documentation receipts are relied on as published.
- **Hosted checks.** At the 21:19Z snapshot (`receipts/hosted-check-runs.tsv`) these had succeeded: changes, verilator-lint, wire-accountability, docs-check-no-git, firmware-unit, bdd-conformance, full-ci-gate, and Yosys shards 0, 2 and 3. Still in progress: docs-check, elaborate, yosys-elaboration, Verilator shards 0-4 and Yosys shard 1. `Physical gPTP` is skipped, which is not executed evidence. Hosted CI runs the model check only at the weaker no-LiteX level.
- **Physical calibration was NOT RUN.** Field skips are not hardware proof. No hardware was touched.

## Pending manager duties

- Hosted completion on this head; the workflow replica; candidate-merge validation of the final current-dev candidate against live dev `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`, which this review does not cover.
- Run the complete local sweep with a LiteX interpreter carrying all five patches, so that gptp_txts runs at the strong level.
- After merge, re-run `sw/litex/patches/apply.sh` on shared LiteX environments. Until then, gate 23h and the new structural check in `test_gmii_rx_capture.py` refuse a stack without 0007.
- Carry RESIDUE R546-2-R1 to the residue checklist. R546-1-R1 and R2 are already applied.
- Confirm the external R547-2 verdict and the completion ledger. Ensure no review remains in flight. Merge authorization, post-merge containment and issue/project closure remain manager duties.

R546-2 FINISHED
