[R591] NEGATIVE - exact head cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6

# R591-1: external review of PR #710 (issue #640, Mark II lane M2 / plan L3)

- Head `cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6`, tree `a766b181e1cb7bcecbce441a943d61ed966f62fa`, base dev `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Diff `e8454e27..cfd74eb9`: 10 files, +731/-27, three one-line commits (`4177835c` product, `2b22bf29` docs, `cfd74eb9` test annotations).
- Role: external independent reviewer, cleared context. Sources: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #640 body and its manager/owner comments (lane M2 assignment 6095827337, D3/D7 rulings), `docs/design/MARK_II_AREA_PLAN.md` (L3, ledgers), `docs/design/AREA_BUDGET.md`, `docs/litex/CLOCK_DOMAINS.md`, the gate record `syn/ooc/pp_resource_baseline.json`, the diff, and the published evidence tree `review-evidence/640-m2-r1` at `16c5a041` (HANDOFF.md, PR-BODY.md, RECEIPTS.tsv; their digests match its MANIFEST.json).
- Prior public review findings on PR #710: none. When this pass ran, the PR carried only the two review-start comments and no review, so there is nothing to resolve or retain.

## Verdict

NEGATIVE on one MINOR: F1, under lenses RTL, Robustness and Docs.

The product change itself is correct at this head:
- the seven arrays keep their function cycle for cycle against stock LiteX;
- the FIFO control and every clock-domain contract are untouched;
- the exclusions hold;
- the mapping under the shipping image's port usage is reproduced independently.

F1 is that the new helper's documented resource contract is false for a crossing shape the helper accepts. The precondition that makes the CSR W/R conversion work is also not recorded anywhere. Conformance and Tests are clean. One SUGGESTION and one RESIDUE are recorded.

## Findings

### R591-1-F1 MINOR - RTL, Robustness, Docs - `sw/litex/milan_soc.py:1433-1444`, `docs/litex/CLOCK_DOMAINS.md:245-246`, `sw/litex/milan_soc.py:778-782` - block-RAM placement silently fails on an unbuffered crossing whose framing flags are read

**Claim at the head.**
- The `_payload_in_block_ram` docstring says the helper will "Hold one crossing's payload in block RAM". It adds: "A framing flag nobody reads costs nothing; one that is read costs one LUTRAM column" (`:1443-1444`).
- `CLOCK_DOMAINS.md:246` says, with no condition: "The payload goes to block RAM; `first` and `last` go to LUTRAM."
- `_crossing_storage` (`:1402`) explicitly accepts both an unbuffered `AsyncFIFO` and an `AsyncFIFOBuffered`.

**Evidence.** The reviewer ran Vivado 2026.1 `synth_design -mode out_of_context` on xc7a100tfgg484-2; receipts are in `receipts/ooc/`. The harness holds the seven crossings, each built by that tree's own `milan_soc` code, with every channel field a port (`scripts/r591_crossing_harness.py`).

| Variant (AXI-Lite `first`/`last`) | Directive | Head result | Base result |
|---|---|---|---|
| Exposed and read (`tree`) | `AreaOptimized_high` (`Default`: 207 LUT, also 0 RAMB18) | W and R refused block RAM; 203 LUT / 120 LUTRAM / 0 RAMB18 | 187 / 108 / 2 |
| Written, not read (`tree_wronly`) | `Default` | W and R in `RAMB18E1` | not run |
| Absent, the image's usage (`tree_nofr`) | `AreaOptimized_high` | W and R in `RAMB18E1` (SDP, `WRITE_FIRST`, `DOA_REG 0`); 143 LUT / 60 LUTRAM / 2 RAMB18 | 179 / 100 / 2 |

- In the exposed-and-read case, Vivado reports: `WARNING: [Synth 8-6849] Infeasible attribute ram_style = "block" set for RAM "r591_crossings/storage_7_reg",trying to implement using LUTRAM`, and the same for `storage_9_reg`.
- In that case the conversion costs 16 LUTs instead of saving any, and the two RAMB18s the MAC crossings free go unused.
- The buffered MAC crossings keep their 72-bit payload in `RAMB36E1` in every variant, whether their flags are read or not.

So the docstring's cost model is right for a buffered crossing and wrong for an unbuffered one. The CSR W/R saving in the shipping image rests on an unstated precondition: those channels' `first`/`last` are never consumed. That precondition holds today. The author's census reports the CSR framing trimmed and RAMB18 at 27.

**Impact.**
- No functional effect, and no effect on the shipping image at this head.
- The helper is general by construction. Its contract tells the next user that reading a flag costs one LUTRAM column; later area lanes M6/M7 convert further arrays.
- On an unbuffered crossing, that use silently drops the payload out of block RAM and grows the image. Nothing flags it:
  - the resource gate allows the BRAM decrease;
  - the LUT growth sits inside the gate's 500-LUT tolerance;
  - the lane test's `storage` check sees only the migen-level tags.

**Required outcome.** The helper's contract and the CLOCK_DOMAINS statement match measured behaviour:
- for an unbuffered crossing, block-RAM placement requires the framing flags to be unread;
- the CSR W/R conversion is recorded as relying on that.

Alternatively, the helper restricts or refuses the shapes for which the claim is false. How this is done is the executor's choice.

**Verification.** Re-read the corrected text against `receipts/ooc/cells_*` and `util_*`. If the helper's behaviour changes, re-run `scripts/r591_crossing_harness.py` and `scripts/r591_ooc.tcl` for the `tree`, `tree_wronly` and `tree_nofr` variants, and confirm the documented mapping holds in each.

### R591-1-S1 SUGGESTION - Tests - `sw/litex/test_retained_cdc_storage.py:160-167`, `:184-188` - the MilanMAC call site is not exercised

- The MAC benches rebuild MilanMAC's sequence themselves (`_axis_dp_cdc`, then `_mac_cdc_rename`, then `_payload_in_block_ram`) rather than taking it from `MilanMAC`.
- Reviewer probe `milanmac-call-site-removed` replaces `milan_soc.py:1793-1794` with `pass`. It survives the lane test: rc 0, every verdict PASS (`receipts/mutants/`).
- The same holds if `add_milan_datapath` stopped calling `_cross_csr_bus`.
- Function is unaffected, because the storage falls back to stock LiteX. Only area moves (+2 RAMB18), which a routed gate check catches and no automated suite does.
- Optional: assert the converted storage on an elaborated product top, for example the `ram_style` attributes in the exported SoC Verilog, so the wiring is tested where that is practical.

### R591-1-R1 RESIDUE - Docs - PR #710 body, "Status" - status names a commit that is not the head

The body says `GREEN at 2b22bf29 (local gates, see the gate table below)`. The head under review is `cfd74eb9`, and the published HANDOFF states every gate ran at `cfd74eb9`. This is wording only. Exact fix: in the Status line, replace `2b22bf29` with `cfd74eb9`.

## Lens results

| Lens | Result |
|---|---|
| Conformance | CLEAN |
| RTL | UNCLEAN (F1) |
| Robustness | UNCLEAN (F1) |
| Tests | CLEAN (S1 is optional) |
| Docs | UNCLEAN (F1); R1 is residue |

### Conformance

[R591] PASS Conformance - #640 comment 6095827337 (lane M2 scope) against `git diff e8454e27..cfd74eb9` and `sw/litex/milan_soc.py:773-797,1394-1477,1788-1794`. Each scope item was checked:

- **Scope.** Only `MilanMAC.mac_tx_cdc`/`mac_rx_cdc` and the `milan_axil_cdc` channels change.
  - `_payload_in_block_ram` has exactly four product call sites (`:796-797`, `:1793-1794`).
  - `_axis_dp_cdc` is unchanged, so `descmem_*`, `respmem_*` and `nvmmem_*` are untouched.
  - `tx_sf`, the LiteDRAM queues, `memory_port_cdc*`, the CPU bridges, the mailbox rings and the media/gPTP tables do not appear in the diff.
- **Widths, depths, throughput, read latency, resets and clock domains are preserved.**
  - Lockstep against stock LiteX holds on every edge at two clock ratios: 35/35 PASS.
  - The emitted Verilog keeps the registered-read-address form (`tb/verilator/gptp_txts/generated/mac_tx_chain.v` diff).
  - The inferred RAMB18/RAMB36 are SDP with `DOA_REG 0`, so no read stage is added and no D3 bound is needed.
- **No BRAM growth.** Both routes the author reports show 74 RAMB36 / 27 RAMB18. The lane uses 0 of its two allowed tiles.
- **Saving reported against the plan.** 34 LUT post-synthesis against 200 (100-400), below range. This is stated in MARK_II_AREA_PLAN `:672-701` and AREA_BUDGET `:197-199`.
- **Re-record withheld under D7.** `syn/ooc/pp_resource_baseline.json` is unchanged in the diff, and `check-baseline` returns rc 0.
- **Gate policy arithmetic.** The route-1x1 floors are WNS 0.03 and WHS 0.0, with a 0.25 tolerance. M2 reports WNS +0.306 and WHS +0.019, against the record's +0.299 and +0.031. Both pass their floor and fall limit. Every other figure is within tolerance: LUT -128, FF -59, SLICE -8, RAMB 0/0, DSP 0.

### RTL

F1 is open. Everything else in the lens was checked and is clean:

- **The FIFO control is untouched.** `_crossing_storage` reaches only the `Memory` special of `migen.genlib.fifo.AsyncFIFO`. The gray counters, MultiRegs and compares stay LiteX's. This was confirmed against pinned migen `4c2ae8df` (`genlib/fifo.py:188-230`) and LiteX `a1e1c365` (`stream.py:170-245`, `axi_lite.py:617-660`).
- **Bit order.** `_FIFO_FRAMING_BITS` and the split match `_FIFOWrapper`'s `fifo_layout`: payload, param, first, last, LSB first. The width guard refuses any mismatch.
- **Collisions are harmless.** Neither array has a read enable, so the read address is re-sampled every read cycle. If a read collides with a write while the FIFO is empty, the entry is read again before `readable` can assert through the two-stage pointer synchronizer.
- **Same inference as the base.** The new RAMB18E1s are SDP `WRITE_FIRST` across the asynchronous sys/milan pair. That is the same inference and clock pair as the MAC RAMB36/RAMB18 already in the base (`receipts/ooc/cells_*`).
- **Timing exceptions survive.** sys↔milan stays a false-path pair (`milan_soc.py:276`). No XDC or Tcl line names a storage cell; `clock_constraints.tcl` filters only `quasi_static` and `mr_ff`. Renamed or re-mapped cells therefore drop no constraint.
- **The RAMB18 trade always balances in product images.** The CSR conversion applies whenever `milan_cd != "sys"`, and the MAC conversion only with `with_mac`. The product builder refuses `soc.full != true` (`sw/builder/endstation_builder.py:4397`), so every product image carries both.

### Robustness

F1 is open. Everything else in the lens was checked and is clean:

- **Reset with beats in flight** leaves no stale or phantom beat, and the crossing is exact and full-depth afterwards.
- **MAC reinit.** The CSR channels pass traffic untouched through it. A one-sided MAC reset is caught on either side: the lane control drops the datapath side, and reviewer probe `mac-reset-datapath-side-only` drops the sys side. Both fail `reset`.
- **Backpressure.** With the reader stalled, a crossing fills to exactly 17 (MAC) or 4 (CSR) entries and drains intact.
- **`milan_cd == "sys"`** builds no crossing: `_cross_csr_bus` returns `axil`, and the MAC guard is at `:1788`.
- **Shape guards.** An unknown LiteX or migen shape fails elaboration by name (`_crossing_storage`, and the order/layout guard in `_cross_csr_bus`).

### Tests

[R591] PASS Tests - `sw/litex/test_retained_cdc_storage.py` at the head, its five controls, and eight reviewer probes (`scripts/r591_mutants.py`, `receipts/mutants/mutants.json`).

- **Lane test:** 35/35 VERDICT PASS and 5/5 controls caught, rc 0 (`receipts/j1_lane_test_head.log`).
- **Two lane defects re-applied** by the reviewer with independent anchors. Each fails its named check on mac_tx, mac_rx, csr_w and csr_r:
  - half depth fails `depth`;
  - reading one entry ahead fails `order`.
- **New reviewer probes**, each detected:

  | Probe | Fails |
  |---|---|
  | payload/framing concatenation swapped | `lockstep` |
  | framing read port in the write domain | `lockstep` |
  | framing write-enable dropped | `lockstep` |
  | MAC reset on the sys side only | `reset` |
  | AW converted as well | `storage` |

- **Independent reference.** The comparison is against stock LiteX, not the implementation, so the test does not restate the implementation's assumptions.
- **Owning suites at the head,** run by the reviewer in a scratch clone:
  - `scripts/run_litex_sims.sh`: 6/6 passed, with pinned Verilator 5.050 (wrapper sha256 `905795b9...`, `Verilator 5.050 2026-07-01 rev v5.050`).
  - `make -C tb/verilator/gptp_txts`: RESULT PASS, 6/6 controls.
  - `gen_mac_tx_model.py --check`: OK with the LiteX stack, and also on CPython 3.12.3 without it.
- **Hosted.** The `elaborate` workflow at the head ran the aggregate: 6/6, including `test_retained_cdc_storage` PASS (`receipts/hosted_elaborate_excerpt.txt`).
- S1 (the uncovered call site) is optional.

### Docs

F1 is open and R1 is residue. Everything else in the lens was checked and is clean:

- **Gates.** The reviewer ran these at the head, all rc 0 (`receipts/gates/`):
  - docs gates: `docs_check`, `check_em_dash --base e8454e27`, `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors`, `check_doc_paths`, `DOC_MAP --check`;
  - code-quality ratchets: `check_py_idiom`, `check_hygiene`, `measure_test_evidence`, `measure_fail_fast`, `measure_naming`;
  - `git diff --check e8454e27 HEAD`.
- **Ledger honesty.** MARK_II_AREA_PLAN `:454` and `:672-701`, and AREA_BUDGET `:197-199`, state:
  - 34 LUT post-synthesis and 128 routed, below the 200 (100-400) estimate;
  - why the routed figure is not credited (pp_shadow -42 and other untouched logic);
  - that the cumulative tables keep the planning figure until the week-4 re-measure.
- **Arithmetic re-checked.**
  - LUT: 50,267 - 50,139 = 128.
  - LUTRAM: 11 RAM32M x 4 = 44.
  - Prior LUTRAM sites: 12 + 24 + 12 + 24 = 72.
  - In both routes, logic + LUTRAM + 4 = LUT. The 4 is the remaining LUT-as-memory, the same in both routes.
- **Independent corroboration of the saving.** The reviewer's OOC harness under the image's port usage gives -36 LUT (179 to 143). The author's harness gave -44, and the integrated post-synthesis figure is -34.
- **Memory ledger.** `:809` keeps the +2 M2 allowance as a maximum, and `:859` now says deferring M2 frees none. These are consistent.

## Completion ledger (reviewer-owned)

All five lenses were covered by round R591-1 at exact head `cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6`.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #640 lane M2 assignment and D3/D7 rulings; `milan_soc.py:773-797,1394-1477,1788-1794`; plan L3 `:450-487`; gate record and policy; author route figures | R591-1 | `cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6` |
| RTL | UNCLEAN (F1) | `milan_soc.py` diff; pinned migen/LiteX FIFO sources; emitted `mac_tx_chain.v`; reviewer OOC mapping (`receipts/ooc/`); constraint sources | R591-1 | `cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6` |
| Robustness | UNCLEAN (F1) | reset/backpressure/stall verdicts; reviewer reset probe; `milan_cd == "sys"` path; shape guards; OOC usage variants | R591-1 | `cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6` |
| Tests | CLEAN | `test_retained_cdc_storage.py` and 5 controls; 8 reviewer probes; LiteX aggregate 6/6; `gptp_txts` and 6 controls; generator check; hosted `elaborate` | R591-1 | `cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6` |
| Docs | UNCLEAN (F1) | `CLOCK_DOMAINS.md`, `TESTING.md`, `MARK_II_AREA_PLAN.md`, `AREA_BUDGET.md`, helper docstrings, PR body; docs gates | R591-1 | `cfd74eb9aeb7af72c96b8f4de4afc6dcf4c62af6` |

## Real limits

- **Author evidence, not reproduced.**
  - The integrated routes, the route census, the 8x8 byte-identity check, and the builder `--require-elaboration --require-rv32` run are author evidence.
  - The published evidence binds their logs by digest only (RECEIPTS.tsv); the logs themselves are not published.
  - The reviewer did not re-route, did not run the builder bank (not allowed), and did not synthesise 8x8.
- **Harness, not image.** The reviewer's OOC mapping uses a seven-crossing harness. Its usage variants bracket the image's port usage. Its `nofr` variant reproduces the direction and size of the author's saving.
- **LiteX environment.**
  - The local environment matches the pins in `tb/verilator/gptp_txts/generated/manifest.json`: migen `4c2ae8df`, LiteX `a1e1c365`, liteeth `276c9e37`, litedram `f9b75e03`.
  - Its working trees carry local modifications to the VexiiRiscv core, BIOS and GMII PHY files. These are taken to be the repository's patch series, not re-verified file by file. None of those files is on the crossings' path.
- **Hosted contexts at the head**, snapshot 2026-10-10T12:31Z (`receipts/hosted_check_runs.tsv`):
  - executed and green: `elaborate`, `yosys-elaboration`, Yosys shards 0-3/4, `verilator-lint`, Verilator shard 3/5, `bdd-conformance`, `wire-accountability`, `docs-check`, `docs-check-no-git`, `changes`, `full-ci-gate`;
  - skipped, so not hardware proof: `Physical gPTP`;
  - still in progress and not claimed: `firmware-unit` and Verilator shards 0, 1, 2 and 4. The `rtl-fast` and `rtl-full` workflow runs had therefore not concluded.
- **No hardware.** Physical calibration NOT RUN.
- **No manager source bank** exists at this head, and none is claimed or inferred.

## Pending manager duties

- Route F1 to the executor. RTL, Robustness and Docs need re-review at the corrected head.
- Carry R1 to the residue checklist.
- Accept the hosted results at the exact head: the `rtl-fast` and `rtl-full` runs, `firmware-unit` and the remaining Verilator shards.
- Build and validate the current-dev merge candidate (builder and native banks), then check post-merge containment.
- Rule on the author's offered AW/AR block-RAM option (+2 RAMB18, which fails the zero-growth gate).

## Reviewer actions and integrity

- **Execution.** Commands ran in the foreground; detached jobs were polled to completion within the session.
- **Disposable trees** stayed under `scratch/`: clones at head and base, planted copies, and Vivado work.
- **Vivado** ran three short OOC syntheses under the host lock, one at a time.
- **Clone integrity after the probes.** The review clone is byte-identical to the head:
  - `git status --porcelain --ignored` is empty, with no index or worktree diff;
  - `git ls-files -s` (mode, blob, path) equals `git ls-tree -r HEAD`, digest `71773f75...`;
  - the gitlinks are `gptp-processor 5dce647a`, `protocol-processor 2ad2f845` and `third_party/verilog-axis 48ff7a7e`, and each submodule is clean.
- **No other actions.** No source edit, commit, push, GitHub write, merge or hardware access was made.

R591-1 FINISHED
