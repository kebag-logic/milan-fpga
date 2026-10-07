[R546] NEGATIVE - exact head 35fb2a95007ce6dd1ec4f51c2dcb793800623cfd

# R546-1 internal cleared-context review: issue #691 / PR #693

- Head `35fb2a95007ce6dd1ec4f51c2dcb793800623cfd`, tree `430abfdcb667dded3fd9b874a0a69c464ae1bd7c`, source base `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`. The PR head was re-read at the end of the round and had not changed.
- Read in this order: AGENTS.md and CONTRIBUTING.md; docs/README; the #691 body; assignment 6041364533; the two STOPs (6042535076, 6045727339); rulings 6042557053 and 6045752839; BUILDING.md sections 3 and 5; `sw/litex/milan_soc.py:1440-1510`; upstream LiteEth `liteeth/phy/gmii.py` at pin `276c9e37`; the diff and its three commits; and the public evidence tree `8f502bd4:review-evidence/691-r1`. All 35 evidence blobs matched their git hashes and the published SHA-256 manifest.
- Prior public review findings on PR #693: none. The PR has no reviews and no inline comments, and its only issue comments are the two review-start notices. Nothing needs to be resolved or carried forward.
- Probes ran against disposable copies of the LiteEth package: pre-patch is the shared install, which carries 0002 only; post-patch is that copy plus 0007. Copies and builds are under `scratch/` (not published). The clone was restored afterwards: worktree and index equal HEAD, the `ls-files -s` digest equals the HEAD tree digest, the four gitlinks are unchanged, and there are no untracked or ignored files.

## Verdict basis

The capture change itself is correct. The patched receiver is sequentially equivalent to upstream's, proven by k-induction. The method is not vacuous: it refutes all eight planted mutants. The structure removes every control set from the nine pad flops, and the six full-image IOB reports show all nine flops in ILOGIC on both trees.

One finding blocks the verdict. The PR changes the LiteX patch series, but it does not regenerate the committed converted MAC chain that embeds this receiver. That artifact's own staleness gate refuses it under the patched pinned stack (F1, MAJOR). A second, smaller gap is the documented placement-fixture refusal, which cannot be reproduced from the tree (F2, MINOR).

## Assignment checks

1. **Patch, apply.sh and receiver.**
   - `0007` applies cleanly after `0002` (`git apply` on a copied package).
   - Gate 23h with the patched overlay reports 5 patches = 5 in SERIES and 4 files reconstructed byte for byte. The two GMII patches compose on `gmii.py`, and 5/5 missing-patch fixtures are rejected (`receipts/gate23h.log`).
   - Against the unpatched shared interpreter, gate 23h correctly names 0007 as not applied (`receipts/gate23h-shared.log`).
   - Converted inside the real `LiteEthPHYGMII` composition, the sampled reset resolves to `eth_rx_rst`, not `sys` (`receipts/mac_tx_chain-regen.diff`). So there is no new crossing.
   - Latency, reset at the edge and `source.last` are unchanged:
     - The reviewer's independent pad-sample model was checked over 25,104 cycles. These include every ordered pair of (dv, rst) states and a reset pulse at every phase of 1-, 2-, 3-, 8- and 64-byte frames. Pre- and post-patch traces are byte-identical (sha256 `5df98b07…`), and both match the model (`receipts/oracle-*.log`).
     - Yosys k-induction proves `gold(pre) == gate(post)` on valid, data and last from the real init values (`receipts/equiv-post*.log`).
   - The PR test gives 1,036 comparisons and passes on both receivers (`receipts/capture-*.log`).
2. **Planted controls.** Each was run against the PR test, the reviewer oracle and the equivalence proof (`receipts/mutants/SUMMARY.txt`). Every one of them is refuted by all three:
   - live reset in the valid mask;
   - `last` forced to 0;
   - lost data bit 7;
   - live reset in the data mask;
   - data unmasked;
   - `last` from the unmasked delayed valid;
   - reset not sampled;
   - one extra cycle of latency.

   The preserved reset-before-D LUT2 fixture:
   - Regenerated `capture.v` / `reset_before_d.v` are byte-identical to the author's recorded hashes (`87a52a30…`, `c568bd94…`).
   - The fixture has 9 `dont_touch` LUT2 (INIT=2, pad & ~reset) in front of all nine capture D inputs.
   - The published compact receipts on those exact inputs read 9 PASS in ILOGIC (good) and 9 FAIL "no register reads the pad" (planted).
3. **iob_pack_selftest arm.**
   - 22 arms, 21 mutants, 0 failures (`receipts/iob-selftest.log`).
   - The reviewer probe (`receipts/iob-arm-probe.log`) shows the new arm discriminates:
     - it holds as committed;
     - the same expectation over the fixed `rx_dv()` shape does not hold;
     - the planted netlist under a PASS expectation does not hold;
     - on its own it kills 4/21 check mutants.
4. **Six-row sweep.**
   - `TIMING.json` (24 corner rows) agrees with the PR, issue and handoff tables cell for cell. TNS/THS are 0 everywhere.
   - All six raw IOB reports read 21 PASS / 1 INERT (`eth0_rx_er`) / 0 FAIL, with `milansoc_phy_rx_data_reg[0..7]` and `milansoc_phy_rx_dv_reg` in ILOGIC. Those cell names exist only in the patched receiver.
   - Provenance:
     - 112/116 recorded dev synthesis inputs match this head byte for byte. The other 4 are generated build files.
     - The ring overlay tree recomputes to `01f65c3b` from `2525eae9` plus the PR diff, in an isolated object store.
     - The ring overlay's two #645-only inputs match that tree (`receipts/synthesis-inputs-vs-head.txt`, `receipts/overlay-tree.txt`).
   - Kept-build reading: BUILDING.md:325-328 keeps the best-WNS sweep build. The margins (BUILDING.md:537-538, 667-670) apply to the selected build, at every corner.
     - dev keeps ExtraPostPlacementOpt: +0.492 / fast WHS +0.007.
     - #645 + fix keeps ExtraPostPlacementOpt: +0.238 / fast WHS +0.036.
     - Both are above +0.030 ns setup and 0 ns hold at all four corners.
   - The ruling's reading is applied correctly.
   - One packet inconsistency (S2): `ROUND1B-IOB.json` holds two rows, not six.
5. **No change beyond the capture structure.**
   - The diff touches no SoC source, configuration, CSR or default selection. `milan_soc.py` is untouched, and `LiteEthPHYGMIIRX` has no CSR.
   - The dev and ring builds record identical ROM init hashes.
   - The only generated product-model artifact affected is the one in F1.
6. **Docs.**
   - BUILDING.md:607-616 and patches README:11-15 describe the mechanism correctly. Each claim was checked against the proof and the converted RTL.
   - Gaps: F2 (fixture procedure), R1 (apply.sh header list).

## Findings

### F1 - MAJOR - Tests, Conformance, RTL - committed converted MAC chain still carries the pre-patch receiver

- **Location:** `tb/verilator/gptp_txts/generated/mac_tx_chain.v:52,56,59,823,2204-2210` and `tb/verilator/gptp_txts/generated/manifest.json:17`.
- **Authority:**
  - `sw/litex/gen_mac_tx_model.py:1-60,422` requires the artifact to re-convert byte-identically with the pinned stack. It names "the PHY's own ... receive register stages, `LiteEthPHYGMIIRX`" as part of it.
  - `tb/verilator/gptp_txts/Makefile:86-91` says "A STALE CONVERTED CHAIN IS A RED".
  - `docs/testing/TESTING.md:514` covers the same rule.
  - Gate 23h defines the pinned stack as upstream plus the complete `apply.sh` SERIES, which now includes 0007.
  - #691 acceptance 3 relies on the existing datapath suites.
- **Evidence:**
  - `gen_mac_tx_model.py --check` is OK with the pre-patch receiver (`receipts/model-check-pre.txt`, rc 0). It reports STALE with the patched receiver: "re-converting the product chain does not reproduce the artifact byte for byte" (`receipts/model-check-post.txt`, rc 1).
  - `make -C tb/verilator/gptp_txts model` with that interpreter returns rc 2 (`receipts/gptp_txts-make-model-post.txt`).
  - The difference is exactly the RX stage (`receipts/mac_tx_chain-regen.diff`).
  - Hosted CI cannot see this. `gptp_txts` runs in Verilator shard 0 (`run_all_suites.sh --shard 0/5 --list`), `rtl.yml` provides no LiteX interpreter, and the Makefile default falls back to the weaker source/pins/bytes check.
  - The PR body's own setup exports `MILAN_LITEX_PYTHON` over the patched overlay. Under that setup the root sweep fails at this target.
- **Impact:**
  - The only existing suite that contains this receiver now models the receiver the product no longer builds.
  - The complete local sweep run with the documented LiteX interpreter fails.
  - After merge, every environment that re-runs `apply.sh` (the README instruction) turns `gptp_txts` red.
- **Required outcome:** in this PR, regenerate `mac_tx_chain.v` and `manifest.json` with the pinned stack carrying the full series, and review the diff. It should be confined to the RX stage.
- **Verification:**
  - With a LiteX interpreter carrying all five patches, `make -C tb/verilator/gptp_txts` must be green: `model` OK, the suite, and `mutants.py`.
  - The reviewer showed this is achievable in a disposable in-clone probe, since restored (`receipts/probe-regen-*.log`):
    - the regenerated artifact passes `--check`;
    - the closed loop gives 85 checks, 0 failures;
    - 6/6 controls are caught.
  - The probe artifact had `verilog_sha256` `f3f110e9…`.

### F2 - MINOR - Docs, Tests - the documented reset-before-D placement refusal is not reproducible from the tree

- **Location:** `docs/integration/BUILDING.md:614-616`; `sw/litex/test_gmii_rx_capture.py:87-99`.
- **Authority:** AGENTS.md section 2 says a cold reviewer must be able to reconstruct the task from GitHub and the repository. #691 acceptance 3 requires the planted reset-before-D defect to be refused by the IOB-pack check.
- **Evidence:**
  - `--emit-dir` writes Verilog only.
  - The fixtures carry no IOB constraint, LOC or IOSTANDARD.
  - `kl_iob_pack_check` grades only ports that answer IOB TRUE, and it reads the `.xdc` beside its report (`sw/litex/iob_pack_check.tcl:243-246,331`). Run as the document describes, the check therefore reports an IOB-PACK ERROR, not the nine FAIL rows.
  - The constraint file and driver that produced the receipts exist only in the evidence packet (`capture.xdc`, `capture-check.tcl`).
- **Impact:** the physical half of the acceptance-3 control can be re-run only from an external packet. The repository states the obligation without the means to meet it.
- **Required outcome:** either commit the compact constraint/driver used for the receipts and name the command, or have BUILDING.md state the constraint set the fixtures need and link the #691 receipts.
- **Verification:** a cold reader reproduces 9 PASS / 9 FAIL "no register reads the pad" from the tree and the document alone.

### R1 - RESIDUE - Docs - `sw/litex/patches/apply.sh:6-13` header list omits 0007

The header still enumerates four patches, while SERIES (`apply.sh:33-39`) applies five. This is comment wording only.

Exact fix: after line 8 insert

```text
#   0007-liteeth-gmii-rx-capture.patch -> liteeth (resetless GMII RX pad capture;
#                                         sampled reset masks valid/data after it)
```

### R2 - RESIDUE - Docs - PR #693 body, Description, last sentence of the paragraph after the table

"Default selection, register map and deployed image are unchanged" can be read as saying the shipping bitstream is unchanged. The bitstream changes by design, in the capture structure. The intended claim, that nothing was deployed, is true.

Exact fix: replace the sentence with "Default selection and register map are unchanged; the shipping image changes only in the GMII RX capture structure, and nothing was deployed."

### S1 - SUGGESTION - Tests - `sw/litex/test_gmii_rx_capture.py:43-84`

The behavioural test passes on the pre-patch receiver too (`receipts/capture-pre.log`), so it guards the cycle contract, not the structure. Two things already guard the structure: gate 23h, which checks the patch is applied, and the post-placement IOB check in a full build. An optional cheap guard is to assert, in the converted `capture.v`, that the nine pad flops sit outside every reset branch and take D directly from their pads.

### S2 - SUGGESTION - Docs - evidence packet `8f502bd4:review-evidence/691-r1/author/ROUND1B-IOB.json`

This file lists two of the six rows. The six-row IOB claim is supported by `TIMING.json` and the six raw reports, which agree. If the packet is republished, regenerate the file or drop it.

## Clean-lens results

```text
[R546] PASS Robustness — sw/litex/patches/0007-liteeth-gmii-rx-capture.patch:13-31; liteeth/phy/gmii.py LiteEthPHYGMIICRG (pin 276c9e37 + 0002); receipts/oracle-*.log, receipts/equiv-post*.log, receipts/mutants/SUMMARY.txt — reset asserted at every frame phase including first/last byte and first idle, reset-only/valid-only/both transitions, power-up init (rx_reset init 1 → outputs 0, same as upstream), ready toggling (ignored, as upstream), rx_er toggling (unused, as upstream), async-assert/sync-release eth_rx_rst from the CRG synchroniser now sampled in-domain exactly where upstream's R pins sampled it, MII path untouched (LiteEthPHYMII), ext_reset path reaches the same eth_rx_rst; unbounded equivalence leaves no reachable divergent state
```

Lens results for the lenses left unclean, recorded so that the next round can narrow its scope:

- **RTL:** receiver structure, domain resolution, widths and init all checked clean. The lens is unclean only through F1, the stale generated RTL.
- **Conformance:**
  - Acceptance 1, 2, 4 (per ruling 6045752839) and 5 are met on the evidence above.
  - Acceptance 3 behaviour and the planted refusal are met.
  - The lens is unclean through F1, because the existing datapath suite carrying the receiver is stale.
- **Tests:**
  - The new test, the self-test arm and the runner inventory are sound and fail for their defects.
  - Unclean through F1 and F2.
- **Docs:** unclean through F2. R1 and R2 are residue.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #691 acceptance 1-5, rulings 6042557053/6045752839, BUILDING.md:325-328,537-538,667-670, TIMING.json, 6 IOB reports, compact receipts, receipts/equiv-post*.log, receipts/model-check-*.txt | R546-1 | 35fb2a95007ce6dd1ec4f51c2dcb793800623cfd |
| RTL | UNCLEAN (F1) | patch 0007:13-31, converted RX in receipts/mac_tx_chain-regen.diff (eth_rx_rst), milan_soc.py:1440-1510, upstream gmii.py CRG, tb/verilator/gptp_txts/generated/* | R546-1 | 35fb2a95007ce6dd1ec4f51c2dcb793800623cfd |
| Robustness | CLEAN | see PASS line above | R546-1 | 35fb2a95007ce6dd1ec4f51c2dcb793800623cfd |
| Tests | UNCLEAN (F1, F2) | test_gmii_rx_capture.py, iob_pack_selftest.py:386-394,506-508, run_litex_sims.sh:101, gate 23h, gptp_txts Makefile/model check, receipts/mutants/*, receipts/iob-arm-probe.log, receipts/litex-sims-post.log | R546-1 | 35fb2a95007ce6dd1ec4f51c2dcb793800623cfd |
| Docs | UNCLEAN (F2) | BUILDING.md:600-616, patches/README.md:8-16, apply.sh:1-40, TESTING.md:550-590, PR #693 body, evidence packet | R546-1 | 35fb2a95007ce6dd1ec4f51c2dcb793800623cfd |

## Real limits

- **Implementation not rerun.** No Vivado run was made, as instructed. The six-row and compact placement results are the author's published receipts. Their inputs were proven as follows:
  - compact fixtures: byte-identical;
  - full images: 112/116 tracked inputs match this head;
  - the ring overlay tree was recomputed;
  - the patched receiver is identified by cell names in all six reports.
- **Generated top-level not regenerated.** The four generated build files and the generated top-level Verilog were not regenerated.
- **Banks not run.** The complete local suite sweep, the Yosys portability bank, the full builder and the PP/gPTP banks were not run.
- **Ethernet suites not rerun.** The Ethernet RTL suites (RX filter, RMON, link guard) were not rerun. They do not instantiate the LiteEth receiver, so they cannot observe this change either way. The behavioural evidence for the receiver is the new test plus the reviewer's equivalence proof.
- **Hosted checks still running.** At the 20:15Z snapshot (`receipts/hosted-check-runs.tsv`), 14 contexts had succeeded and 1 was skipped (Physical gPTP, nightly/manual; not executed). Still in progress: `elaborate`, `docs-check`, and Verilator shards 0, 1, 2 and 4. Shard 0 holds `gptp_txts` and cannot detect F1.
- **No hardware.** Physical calibration was NOT RUN, and no hardware was touched.

## Pending manager duties

- Hosted completion on the eventual head, the workflow replica, and candidate-merge validation against live dev `d8b355fe`.
- Run the complete local sweep with a LiteX interpreter carrying all five patches. This is the configuration that exposes F1.
- Re-run `sw/litex/patches/apply.sh` on shared LiteX environments after merge. Gate 23h refuses them until then.
- The external review (R547).
- Carry R1 and R2 to the residue checklist.
- A new round on the corrected head must re-cover Conformance, RTL, Tests and Docs.

R546-1 FINISHED
