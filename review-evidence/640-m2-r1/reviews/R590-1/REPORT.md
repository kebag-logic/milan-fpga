[R590] POSITIVE - exact head cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6

# R590-1: internal cleared-context review of PR #710 (issue #640, Mark II lane M2 / plan L3)

- Head `cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6`, tree `a766b181e1cb7bcecbce441a943d61ed966f62fa`; base dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (also live dev at review start).
- Reconstructed from: AGENTS.md, CONTRIBUTING.md, issue #640 body and the public lane rulings (D1, D3, D7, D8; lane M2 assignment 6095827337; TAKEN 6095910427; REVIEW READY 6097237423), `docs/design/MARK_II_AREA_PLAN.md` (L3, ledger), `docs/design/AREA_BUDGET.md` (D7 exception, gate policy), `docs/litex/CLOCK_DOMAINS.md`, the pinned LiteX/migen crossing sources, `git diff e8454e27..cfd74eb9`, the three commits, and the published evidence `review-evidence/640-m2-r1` at `16c5a041` (HANDOFF.md, PR-BODY.md, RECEIPTS.tsv; digests match its MANIFEST.json).
- Prior public review findings on PR #710: none exist. The PR carries only the two review-start notices (6097250954, 6097254158) and no review objects, so nothing is resolved or retained from earlier rounds.
- Verdict basis: no BLOCKER, MAJOR or MINOR is open. Two RESIDUE items and two SUGGESTIONs are recorded below. All five lenses are covered clean at this exact head.

## What the change is (as reviewed)

`sw/litex/milan_soc.py` re-declares the single storage `Memory` of a LiteX `stream.ClockDomainCrossing` as two arrays: payload+params with `ram_style="block"` and the two framing flags with `ram_style="distributed"`. Both arrays use the FIFO's own write address, write enable and read address, and their read data is concatenated back in LiteX's bit order (`_payload_in_block_ram`, `milan_soc.py:1433-1470`). `_crossing_storage` (`:1402`) refuses any shape other than the one the pinned LiteX builds. `MilanMAC` applies the split to `mac_tx_cdc`/`mac_rx_cdc` (`:1793-1794`), and `_cross_csr_bus` (`:773-799`, called at `:838`) applies it to the CSR W and R channel FIFOs. The gray pointers, synchronizers and compares stay LiteX's own. `gen_mac_tx_model.py:277` mirrors the call, and the `gptp_txts` chain is regenerated.

## Independent evidence produced in this round

All runs were at the exact head unless marked base. Every receipt is listed in `MANIFEST.sha256`.

1. **Generated top, base vs head (`receipts/top/`).** I exported the shipping ax7101 SoC Verilog without vendor execution twice: from this clone, and from a scratch base tree at `e8454e27` with submodules at their gitlinks. Both exports returned rc 0.
   - Only the storage arrays differ: `top_diff_normalised.txt`, plus three checkout-path strings.
   - The memory census changes in exactly these ways (`mem-base.txt` vs `mem-head.txt`):
     - two 16x74 arrays become 16x72 + 16x2;
     - CSR W 4x38 becomes 4x36 + 4x2;
     - CSR R 4x36 becomes 4x34 + 4x2.
   - Every other array keeps its shape. This includes LiteDRAM, `memory_port_cdc*`, `descmem_*`, `respmem_*`, `nvmmem_*`, the mailbox rings, the media and gPTP tables and `tx_sf`.
   - The `ram_style` attributes go from 0 to 8, all on the changed arrays. The ROM, SRAM and main-memory init files and the XDC are byte-identical.
   - The arrays sit in the intended domains:
     - MAC payload and flags in `macdp`/`macsys`;
     - CSR W written in `sys` and read in `milan`;
     - CSR R written in `milan` and read in `sys`.
   - The read form is unchanged: a synchronous registered read in the read clock, and no storage reset.
2. **Correspondence with the measured Verilog.** The author's receipts give the measured top sizes as 1,763,079 (base) and 1,772,379 (M2). Mine are 1,763,151 and 1,772,376. The residual (+72) - (-3) = 75 bytes is exactly 3 embedded checkout paths x the 25-character difference between my two tree paths. This is size correspondence, not a hash match (`top_census.txt`).
3. **Second shape.** An ax8x8 export at the head (rc 0) has crossing storage Verilog byte-identical to the 1x1 export (`head_{1x1,8x8}_crossing_storage.v.txt`).
4. **Primitive mapping, out of context (`receipts/ooc/`).** I wrote a harness of the seven crossings, built by each tree's own code with every field on a port (`scripts/xing_harness.py`). I synthesized it with `scripts/xing_ooc.tcl` (Vivado 2026.1, `xc7a100tfgg484-2`, AreaOptimized_high, under the host Vivado lock, base then head).
   - Base: 200 LUT (108 LUTRAM), 340 FF, RAMB36 2 / RAMB18 2.
   - Head: 166 LUT (72 LUTRAM), 278 FF, RAMB36 2 / RAMB18 2.
   - Every BRAM is SDP with WRITE_FIRST on both sides. The MAC RAMB36s keep DO_REG=1 (the buffered output register is absorbed). The new CSR RAMB18s have DO_REG=0.
   - So the new RAMB18s are the same dual-clock primitive configuration class as the MAC crossings already ship.
   - DRC: only CFGBVS-1, identical at base and head.
   - Methodology at head adds only SYNTH-4 (shallow block RAM, an accepted trade) and SYNTH-6 (unregistered RAM output; see S2).
   - Logic LUTs are 92 -> 94, so the control logic is unchanged.
   - The harness keeps every flag that the integrated image trims, so its absolute counts are not the image's.
5. **Lane test and planted defects.**
   - `test_retained_cdc_storage.py`: 35/35 VERDICT PASS and 5/5 controls caught, rc 0 (`test_retained_full.log`).
   - My probe driver (`scripts/probe_mutants.py`, `receipts/probe_mutants.log`) plants defects into symlinked scratch copies, leaving the repository untouched. It requires the named checks to fail. Result: **11/11 DETECTED**.
   - Re-applied author controls (3):
     - read-address-ahead -> `order`;
     - one-sided MAC reset -> `reset`;
     - half-depth arrays -> `depth`.
   - Reviewer's own defects (8):
     - concatenation order swapped -> `lockstep`;
     - flags never written -> `lockstep`;
     - flag write address off by one -> `lockstep`;
     - asynchronous read port (latency change) -> `lockstep`;
     - ram styles swapped -> `storage`;
     - B also converted -> `storage`;
     - MAC datapath side outside reinit -> `reset`;
     - AW converted instead of W -> `storage`.
6. **Owning suites and generator.**
   - `scripts/run_litex_sims.sh`: 6/6 passed, none skipped, including `test_gptp_tx_timestamp` on the regenerated chain.
   - `make -C tb/verilator/gptp_txts`: PASS with 6/6 controls. This used Verilator 5.050, identity checked: `--version` "5.050 2026-07-01 rev v5.050".
   - `gen_mac_tx_model.py --check`: OK.
7. **Gate arithmetic and record.**
   - `scripts/gate_arith.py` applies the gate's own `verdict_for` to the author's M2 route figures against the committed `route-1x1` record (`gate_arith.log`).
   - Every gated figure is ok: LUT -128, FF -59, slices -8, RAMB36/RAMB18/DSP equal.
   - WNS 0.306 is above the 0.03 floor and has not fallen. WHS 0.019 is at or above the 0.0 floor and fell by 0.012, within the 0.25 tolerance. BRAM tiles: 87.5 against the 121.5 ceiling.
   - `check-baseline`: PASS 3 endpoints. Gate `--selftest`: rc 0.
   - `syn/` is untouched by the diff, so the record was not re-recorded. That is correct under D7 (`AREA_BUDGET.md:357,440-446,510`). The standalone `ooc-1x1`/`ooc-8x8` endpoints cannot move: no RTL changed, and the `KL_pp_shadow` parameters in the exported top are unchanged.
8. **Docs and quality gates.** These all returned rc 0:
   - `docs_check`;
   - `check_em_dash --base e8454e27`;
   - `check_doc_style`;
   - `gen_toc --check` and `--verify-anchors`;
   - `check_doc_paths`;
   - `DOC_MAP.gen.py --check`;
   - `check_py_idiom` (CPython 3.12.3);
   - `git diff --check e8454e27 HEAD`.

   The three commits are one-line, with no trailers and a single parent each.
9. **Hosted at the exact head.** This is a snapshot at 2026-10-10 12:28 UTC (`hosted_checks.tsv`); the manager owns acceptance.
   - Success: `changes`, `bdd-conformance`, `yosys-elaboration`, `verilator-lint`, `elaborate`, `wire-accountability`, `docs-check-no-git`, `full-ci-gate`, Yosys shards 0-3/4 and Verilator shard 3/5.
   - Still in progress: rtl-fast's `firmware-unit`, `docs-check`, and Verilator shards 0, 1, 2 and 4.
   - `Physical gPTP` was skipped by design (nightly/manual). That skip is not hardware evidence.

## Findings

### R590-1-R1 - RESIDUE - Docs - PR #710 body, Status line ("GREEN at `2b22bf29`")
- Authority/evidence: the PR head is `cfd74eb9`, and the published gate table (HANDOFF section 6, REVIEW READY 6097237423) ran at `cfd74eb9`. The Status line names the previous commit.
- Impact: purely wording in the PR body. No measurement, gate result or verdict changes, because the gates were in fact run at the head.
- Required outcome (exact fix): change the Status line to "GREEN at `cfd74eb9` (local gates, see the gate table below)".
- Verification: re-read the PR body.

### R590-1-R2 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:698` ("The changed arrays' whole LUTRAM footprint was 72 sites.")
- Authority/evidence: the 72 sites are the LUTRAM of the CSR crossing's AW 12 + W 24 + AR 12 + R 24 (HANDOFF section 1). The MAC arrays were block RAM and B was trimmed. Read literally, "changed arrays" (MAC x2, W, R) held 48 sites, not 72. The figure is right for the L3 crossings' arrays, which is the set the sentence argues about (the ceiling for a storage-only saving). The conclusion holds either way (48 or 72 < 100).
- Impact: an imprecise subject only. No figure changes, and the ledger's statement of 34 LUT against 200 (100-400) stays as it is.
- Required outcome (exact fix): replace the sentence with "The seven L3 arrays' whole LUTRAM footprint was 72 sites (AW 12, W 24, AR 12, R 24)." In the PR body, "The arrays' whole LUTRAM footprint was 72 sites." may take the same wording.
- Verification: re-read; the doc gates pass.

### R590-1-S1 - SUGGESTION - Tests - `sw/litex/test_retained_cdc_storage.py:167`
- The MAC bench applies `_payload_in_block_ram` itself, so the test cannot notice if `MilanMAC` (`milan_soc.py:1793-1794`) stops applying it. The same holds for any future `add_milan_datapath` that bypasses `_cross_csr_bus`.
- Such a regression is function-neutral, since stock LiteX storage is the reference. It would surface only as +2 RAMB18 at the next routed gate check.
- Optional: assert the storage census on an elaborated SoC (for example from the builder's elaboration), or build the MAC bench through the product composition.
- At this head the integration is confirmed by the generated-top census (evidence item 1).

### R590-1-S2 - SUGGESTION - RTL, Docs - `milan_soc.py:796-797`; `receipts/ooc/head_methodology_summary.txt`
- The CSR W and R RAMB18s have no output register (DO_REG=0, SYNTH-6). R's read data now leaves a RAMB18 combinationally into the CPU's AXI-Lite bridge at the 100 MHz sys clock, where it used to leave a flip-flop.
- The route meets timing with every endpoint passing (WNS +0.306 is the global worst). `_axis_dp_cdc`'s own comment (`milan_soc.py:1489-1492`) records an earlier BRAM clock-to-out violation class.
- Optional: record that path's routed slack in the M2 ledger section, so later lanes can see its margin.

## Lens coverage

- `[R590] PASS Conformance - issue #640 lane M2 assignment 6095827337 against milan_soc.py:773-838,1399-1474,1793-1794; generated top base vs head (receipts/top/); gate_arith.log; AREA_BUDGET.md:357,440-446,510 - each lane acceptance item is met.`
  - Storage converted only where the image saves LUTs (net -34 post-synthesis).
  - Widths, depths, throughput, read latency, resets and domains preserved (lockstep, top census).
  - Named negative controls (5/5, plus 11/11 reviewer probes).
  - Owning suites (aggregate 6/6, `gptp_txts`; 8x8 crossing Verilog identical).
  - Route and gate through the M0s recipe (author figures; gate arithmetic passes every figure).
  - Re-record correctly withheld under D7.
  - Measured saving reported against 200 (100-400): 34 LUT, honestly below range, with 0 extra tiles.
  - Exclusions honoured (memory census).
- `[R590] PASS RTL - milan_soc.py:1402-1470 against pinned LiteX stream.py:170-294, axi_lite.py:617-660, migen fifo.py:177-235; generated top arrays (receipts/top/); OOC cells (receipts/ooc/*_cells.tsv) - CDC control is untouched LiteX.`
  - Ports keep the write and read domains, the synchronous read and the LiteX bit order (payload, params, first, last).
  - No storage reset, as before.
  - New RAMB18s are SDP WRITE_FIRST like the existing MAC RAMB36/18. In an async FIFO, a same-address read collides only on the empty head entry, which is re-read before the two-stage-synchronized pointer makes it readable.
  - RAMB counts unchanged.
- `[R590] PASS Robustness - milan_soc.py:1402-1430,773-799,1777-1794; test reset/depth checks; probes - malformed shape handling, reset and boundary behaviour checked.`
  - Shape drift in LiteX refuses elaboration rather than silently placing nothing.
  - The `milan_cd == "sys"` path is guarded at both call sites.
  - The paired MAC reinit is kept (one-sided and outside-reinit variants are caught).
  - CSR traffic is exact through a MAC reinit.
  - Full-capacity fill and drain hold at 17/4.
  - A reset with beats in flight leaves no stale or phantom beat, at two clock ratios.
- `[R590] PASS Tests - sw/litex/test_retained_cdc_storage.py:1-487, scripts/run_litex_sims.sh:105; receipts test_retained_full.log, probe_mutants.log, litex_sims.log, gptp_txts.log - the tests fail for the defects they claim to catch.`
  - 5/5 own controls and 11/11 reviewer probes, 8 of them new defect classes.
  - Positive, negative and boundary cases are covered, and existing regressions stay green.
  - S1 is optional.
- `[R590] PASS Docs - docs/litex/CLOCK_DOMAINS.md:220-224,242-252; docs/testing/TESTING.md:681-690; docs/design/MARK_II_AREA_PLAN.md:454,672-701,859; docs/design/AREA_BUDGET.md:197-199,273; PR body; HANDOFF - the changed contracts are documented.`
  - The ledger figures equal the published evidence, and the budget and plan deferral sentences agree.
  - The doc gates return rc 0.
  - Wording residue R1 and R2 does not uncover the lens.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | lane assignment and rulings on #640; diff; generated top base/head; gate record and arithmetic; plan/budget D7 text | R590-1 | cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6 |
| RTL | CLEAN | `milan_soc.py` 770-838, 1399-1474, 1777-1794; pinned LiteX/migen FIFO and AXI-Lite crossing sources; generated top storage blocks; OOC primitive mapping, DRC and methodology | R590-1 | cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6 |
| Robustness | CLEAN | shape refusals; sys-domain guards; reset/reinit checks; capacity and in-flight reset scenarios; 11 planted defects | R590-1 | cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6 |
| Tests | CLEAN | `test_retained_cdc_storage.py` (35 verdicts, 5 controls); reviewer probes 11/11; LiteX aggregate 6/6; `gptp_txts` and controls; generator check | R590-1 | cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6 |
| Docs | CLEAN (RESIDUE R1, R2 carried) | CLOCK_DOMAINS, TESTING, MARK_II_AREA_PLAN, AREA_BUDGET diffs; PR body; published HANDOFF/RECEIPTS; doc gates | R590-1 | cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6 |

## Real limits

- **Route.** I did not re-route the integrated image. The route reports are not published (RECEIPTS.tsv lists them by size and digest only). The LUT, FF, slice, RAMB and timing figures for both routes are therefore the author's, and my gate check judges their arithmetic, not the reports. The link between the measured Verilog and the head rests on size correspondence (evidence item 2), not a hash.
- **Simulation semantics.** migen simulates block and distributed `Memory` identically. The lockstep test proves that the transformation preserves RTL behaviour; it says nothing about the vendor mapping.
  - The block RAM mapping and its dual-clock configuration rest on the OOC synthesis here and on the author's census.
  - The collision argument is reasoned, and it matches the primitive class the MAC crossings already ship.
- **Not run here:**
  - the builder gate (`test_builder.py`);
  - Yosys, PP, gPTP, firmware and full Verilator banks (out of scope for this round, and no file they read changed apart from the `gptp_txts` chain, which ran);
  - CPython 3.12.3 runs of the LiteX test;
  - any 8x8 synthesis;
  - act or the local replica.
- **Environment.** The LiteX environment used for every run has the pinned revisions from `sw/litex/litex_pins.txt`. It carries local modifications only outside the crossing sources (the CPU core wrapper, BIOS and GMII PHY files), and the same environment produced both the base and head exports.
- **Hardware.** No hardware was touched. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Manager source bank.** No manager source bank exists at this head, and none is claimed or inferred.

## Pending manager duties

- Hosted contexts at this head that were still in progress at 12:28 UTC: rtl-fast `firmware-unit`, `docs-check`, Verilator shards 0, 1, 2 and 4 of 5. Exact-head acceptance of rtl-fast, `verilator-suites` and `yosys-portability`, and the act replica.
- Current-dev candidate merge validation (builder and native banks) at the merge turn.
- External review R591 and the two-positive bar.
- Carry RESIDUE R1 and R2 to the residue checklist.
- Post-merge containment.

## Probe hygiene

The clone is restored to the exact head (`receipts/restore_check.txt`):
- all 1,271 tracked non-gitlink blobs re-hash equal;
- index and worktree are clean, with 0 untracked or ignored entries and no assume-unchanged or skip-worktree flags;
- the protocol-processor, gptp-processor and verilog-axis gitlinks are at their pins, and their checkouts are clean.

Probe trees, exports and Vivado runs lived under `scratch/`, which is not published.

R590-1 FINISHED
