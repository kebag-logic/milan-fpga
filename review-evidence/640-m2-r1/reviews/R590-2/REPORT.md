[R590] POSITIVE - exact head f340d92372b5d04cb74b0ee4425ce353a83133a7

# R590-2: internal cleared-context review of PR #710 (issue #640, Mark II lane M2 / plan L3), round 2

- Head `f340d92372b5d04cb74b0ee4425ce353a83133a7`, tree `e35a54e76e9ae1aae9b27b25fd25ccec14ecdc4d`, base dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (live dev at review start is the same commit).
- Diff `e8454e27..f340d923`: 10 files, +906/-28, five one-line commits. Product commits are `4177835c` (the measured route) and `67a3b68d` (round 2: `READ_FIRST` read ports, lane test, regenerated `gptp_txts` chain). `2b22bf29`, `cfd74eb9` and `f340d923` change docs and test annotations.
- Role: internal reviewer, cleared context. Sources, in order:
  - AGENTS.md, CONTRIBUTING.md, docs/README.md;
  - the #640 body and its manager/owner comments: lane M2 assignment [6095827337](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6095827337), D3/D7 rulings [5990755268](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268), round-2 assignment [6097529220](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097529220), the executor's TAKEN and both REVIEW READY comments;
  - `docs/design/MARK_II_AREA_PLAN.md` (L3, ledgers), `docs/design/AREA_BUDGET.md`, `docs/litex/CLOCK_DOMAINS.md`;
  - the pinned LiteX/migen sources the helper depends on;
  - the diff and history;
  - the public evidence tree `review-evidence/640-m2-r1` at `16c5a041` (HANDOFF.md, PR-BODY.md, RECEIPTS.tsv; digests match its MANIFEST.json).
- Prior review findings on PR #710 (R590-1, R591-1) were read only after the independent pass and a provisional verdict were written. Each is resolved or retained under "Prior findings at this head".

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open at this head under any lens. One RESIDUE is retained from R590-1, and two new SUGGESTIONs are recorded.

The change alters storage form only, and it is correct:
- `_payload_in_block_ram` (`sw/litex/milan_soc.py:1433-1483`) splits the one `Memory` of a LiteX async FIFO in two:
  - a payload+params array (`ram_style="block"`) and a 2-bit framing array (`ram_style="distributed"`);
  - both on the FIFO's own write address, write enable and read address;
  - the read word is reassembled in LiteX's `_FIFOWrapper` bit order (payload, param, first, last, LSB first).
  The gray-pointer control is untouched.
- Each split array's read port registers the word (`mode=READ_FIRST`, `:1473`). LiteX's emitter (`litex/gen/fhdl/memory.py:36-41`, pinned `a1e1c365`) already forces that form on every port of a two-clock array. So the SoC's Verilog does not change with the declaration. Reviewer probe E1 shows the LiteX-emitted crossings byte-identical with and without it.
- Function is identical to stock LiteX on every edge of both clocks, at two clock ratios. That includes a reset with beats in flight and a MAC reinit seen by the CSR crossing. The lane test, rerun here, gives 42/42 PASS with 7/7 controls caught.
- Placement applies only to `mac_tx_cdc` and `mac_rx_cdc` (`:1806-1807`, under `milan_cd != "sys"`) and to CSR W/R (`:796-797`). `_axis_dp_cdc` is unchanged, so `descmem_*`, `respmem_*` and `nvmmem_*` are untouched.

## Independent evidence produced in this round

All of it is under this packet (`receipts/`, `scripts/`).
- Interpreter: the pinned LiteX environment, CPython 3.14.7. Its migen `4c2ae8df`, LiteX `a1e1c365`, liteeth `276c9e37` and litedram `f9b75e03` equal `tb/verilator/gptp_txts/generated/manifest.json`.
- Verilator: the scoped 5.050 wrapper (`Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9...`).

1. **Owning checks at the head.** `scripts/campaign.sh` ran them concurrently, one log and rc each (`receipts/campaign/`):
   - `test_retained_cdc_storage.py --jobs 8`: 42 `VERDICT ... PASS` (7 arrays x 6 checks), 7/7 controls caught, `RESULT: PASS`, rc 0;
   - `scripts/run_litex_sims.sh`: 6/6 passed (member logs in `receipts/campaign/litex-sim-logs/`, including `test_gptp_tx_timestamp` against the regenerated chain); `--selftest` 10/10; rc 0;
   - `gen_mac_tx_model.py --check`: OK with the LiteX stack (re-converted from the product source) and with plain `python3` (source region, pins and bytes); rc 0 both;
   - `make -C tb/verilator/gptp_txts`: 85 checks, 0 failures, 6/6 mutants caught, rc 0.
2. **Reviewer mutants** (`scripts/mutants.py`, `receipts/mutants/`). Twelve defects, independent of the lane's own controls, were each planted in a scratch copy of `milan_soc.py`. The lane test caught **12/12**:

   | Probe | Fails (subset) |
   |---|---|
   | read word reassembled flags-first | lockstep, order, depth, reset on mac_tx, mac_rx, csr_w, csr_r |
   | split arrays written every cycle (`we=1`) | lockstep, depth on all four |
   | write word sliced one bit off | lockstep on all four |
   | split arrays read at the write pointer | lockstep on all four |
   | framing flags read asynchronously (one cycle early) | lockstep on all four |
   | split arrays written in the read clock | lockstep on all four |
   | CSR helper places AW instead of W | storage, blockram (CSR) |
   | CSR helper leaves R stock | storage, blockram (CSR) |
   | `MilanMAC` drops the `mac_rx_cdc` call | mac_rx storage, blockram |
   | `ram_style` attribute dropped | storage, blockram |
   | block/distributed styles swapped | storage, blockram |
   | split arrays twice the pointer range | storage, blockram |
3. **Robustness probes** (`scripts/robustness.py`, `receipts/robustness/robustness_head.log`), 8/8 ok:
   - `MilanMAC(milan_cd="sys")` elaborates with no crossing;
   - `_cross_csr_bus(..., "sys")` returns the CPU bus and adds nothing;
   - a second placement on the same crossing is refused by name, so there is no silent double split;
   - a same-domain crossing and a module without an AsyncFIFO are refused;
   - a param-carrying crossing splits as payload+params (37 bits, block) and flags (2 bits, distributed);
   - a `with_common_rst` crossing is accepted;
   - the stock array and both its ports leave the specials, and the split arrays carry no init.
4. **E1, emitter identity** (`scripts/emit_identity.py`, `receipts/emit/emit_identity.txt`). The lane test's three benches, with every `first`/`last` a port, were emitted twice: from the head, and from the head with `mode=READ_FIRST` reverted (the `4177835c` product form).
   - LiteX emitter: the MAC TX, MAC RX and CSR benches are byte-identical.
   - migen emitter: they differ, as intended.
   This corroborates at crossing level the executor's statement that round 2 left the image's Verilog unchanged. The `4177835c` route therefore stands for the head's crossings.
5. **Gates at the head** (`scripts/gates.sh`, `receipts/gates/`), 18/18 rc 0: `docs_check`, `check_em_dash --base e8454e27`, `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors`, `check_doc_paths`, `DOC_MAP.gen.py --check`, `check_py_idiom`, `check_sh_idiom`, `measure_naming --check`, `measure_fail_fast --check`, `measure_test_evidence --check`, `check_hygiene --check`, `check_todo_ownership`, `check_soc_sources`, `pp_resource_gate.py check-baseline`, `run_litex_sims.sh --list`, `git diff --check e8454e27 HEAD`.
6. **Out-of-context mapping** (`scripts/ooc_run.sh`, `scripts/ooc_bench.tcl`, `receipts/ooc/`). Vivado 2026.1, `synth_design -mode out_of_context -directive AreaOptimized_high`, xc7a100tfgg484-2. Five runs, serial, under the host lock (acquired 15:05:21Z, done 15:07:13Z). Each bench holds the product crossing beside its stock reference, with every `first`/`last` a port, so every framing flag is read:

   | Bench (emitter) | Product block RAM | Stock reference | Synth 8-6849 | RAMB36 / RAMB18 total |
   |---|---|---|---|---|
   | CSR, head (LiteX) | W `4 x 36` and R `4 x 34`: RAMB18 each | AW/W/B/AR/R in LUTRAM | 0 | 0 / 2 |
   | CSR, head (migen) | W and R: RAMB18 each | LUTRAM | 0 | 0 / 2 |
   | CSR, `READ_FIRST` reverted (migen), the R591-1-F1 form | none: W and R fall to LUTRAM | LUTRAM | 8 | 0 / 0 |
   | MAC TX, head (LiteX) | payload `16 x 72`: one RAMB36; flags: 2 RAM32X1D | `16 x 74`: RAMB36 + RAMB18 | 0 | 2 / 1 |
   | MAC TX, head (migen) | the same | the same | 0 | 2 / 1 |

   So with its flags read, the payload stays in block RAM at the head under both emitters, and the reverted form reproduces F1. This independently confirms the round-2 fix at synthesis level.
7. **Hosted snapshot** at the exact head (`receipts/hosted/check_runs_snapshot.tsv`, read-only):
   - executed and green at snapshot time: `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, Verilator shard 3/5, `wire-accountability`, `yosys-elaboration`, Yosys shards 0-3/4;
   - skipped, so not hardware proof: `Physical gPTP`;
   - in progress and not claimed: `docs-check`, `elaborate`, `firmware-unit`, Verilator shards 0, 1, 2 and 4.

## Findings

### R590-1-R2 (retained) - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:698`
- Text: "The changed arrays' whole LUTRAM footprint was 72 sites."
- Evidence: 72 = AW 12 + W 24 + AR 12 + R 24 (HANDOFF section 1 census at `16c5a041`). The arrays this lane changed held 48 sites: CSR W 24 and R 24, with the MAC crossings previously in block RAM. The figure is right for the L3 crossings the sentence argues about, which bound a storage-only saving. The conclusion holds with either set.
- Classification: my independent pass found this sentence again before reading R590-1. I weighed MINOR under the "unsure" rule and retain RESIDUE. The defect is the subject noun only. No measured figure (34, 128, 44, 72), verdict, test, code or gate changes, and nothing downstream computes from it.
- Exact fix: "The L3 crossings' whole LUTRAM footprint was 72 sites (AW 12, W 24, AR 12, R 24)." The PR body's "The arrays' whole LUTRAM footprint was 72 sites." may take the same wording.
- Verification: re-read; the docs gates pass.

### R590-2-S1 - SUGGESTION - Tests - `sw/litex/test_retained_cdc_storage.py:341-344,482-484`
- The CSR bench's `storage` and `blockram` results are one bench-level comparison, copied onto all five CSR channels.
- So `VERDICT csr_aw blockram PASS` (and the csr_b and csr_ar lines) says nothing about AW, B or AR on their own. Six of the 42 verdicts are such copies.
- Reviewer mutants `csr-aw-instead-of-w` and `csr-r-not-placed` fail all five CSR channels together. Detection is unaffected.
- Optional: print bench-level checks once per bench, or say in the docstring and TESTING.md that they are bench-level.

### R590-2-S2 - SUGGESTION - Docs - `sw/litex/milan_soc.py:1455-1457`; `docs/litex/CLOCK_DOMAINS.md:248`
- "A read flag costs one RAM32X1D and one flip-flop" is exact for every crossing the product applies the helper to (depths 16 and 4), and for any depth up to 32.
- The helper accepts any depth. A deeper crossing's read flag maps to a deeper distributed primitive.
- Optional: qualify the sentence with "for a crossing up to 32 entries deep".

## Prior findings at this head

| Finding | Status at `f340d923` | Evidence |
|---|---|---|
| R591-1-F1 MINOR (RTL, Robustness, Docs): the payload leaves block RAM on an unbuffered crossing whose flags are read | **Resolved**, by explicit handling, which the round-2 assignment allowed | `milan_soc.py:1473` declares `READ_FIRST`, so each split array has its own read-word register under either emitter. Docstring `:1445-1457` and `CLOCK_DOMAINS.md:245-262` state the condition and the cost. The `blockram` check emits every bench with all flags read, through both emitters, and requires a per-array read register: 42/42 at the head. Control `read-address-registered` fails it by name. E1 shows the SoC's crossings unchanged. Reviewer OOC synthesis (evidence item 6): W and R are RAMB18 with all flags read under both emitters and no Synth 8-6849; the reverted form gives 0 RAMB18 and 8 Synth 8-6849. |
| R591-1-S1 SUGGESTION (required in round 2): the MilanMAC call site is not exercised | **Resolved** | `test_retained_cdc_storage.py:218` takes both MAC crossings from a real `MilanMAC`. Control `milanmac-call-site-removed` and reviewer mutant `mac-rx-call-removed` both fail `storage`. |
| R591-1-R1 RESIDUE: the PR status line names a stale commit | **Resolved** | The PR body Status reads "GREEN at `f340d923`". |
| R590-1-R1 RESIDUE: the same stale status line | **Resolved** | As above. |
| R590-1-R2 RESIDUE: plan `:698` "changed arrays' ... 72 sites" | **Retained** as RESIDUE | The text is unchanged at the head; see Findings. |
| R590-1-S1 SUGGESTION: the MilanMAC and `add_milan_datapath` call sites | MilanMAC part resolved. `add_milan_datapath`'s call to `_cross_csr_bus` (`:838`) is still not exercised by the lane test; the PR body states it as a known limitation. | Optional |
| R590-1-S2 SUGGESTION: record the R channel's routed slack (RAMB18 `DO_REG=0` into the sys-side bridge) | Not adopted; optional | The route at `4177835c` meets every endpoint. |

## Lens coverage (round R590-2, head `f340d92372b5d04cb74b0ee4425ce353a83133a7`)

[R590] PASS Conformance - #640 lane M2 assignment 6095827337 and round-2 assignment 6097529220 against `git diff e8454e27..f340d923`, `sw/litex/milan_soc.py:773-797,838,1399-1490,1801-1807`, plan L3 and M2 ledger `MARK_II_AREA_PLAN.md:450-487,672-701`, and `AREA_BUDGET.md:197-199,273` - each item checked:
- Scope covers only the MAC crossings and CSR W/R. Every `_payload_in_block_ram` call site is listed above, `_axis_dp_cdc` is unchanged, and the exclusions are absent from the diff.
- Widths, depths, read latency, resets and domains are preserved (lockstep 42/42), so no D3 bound is needed.
- No block-RAM growth: the executor's routes show 74/27 both, using 0 of the 2 allowed tiles.
- The saving is reported against the estimate: 34 LUT post-synthesis and 128 routed, below 200 (100-400).
- No re-record, per D7: `check-baseline` rc 0, and the record file is not in the diff.
- Round-2 items 1-3 are met, as tabulated above.

[R590] PASS RTL - `sw/litex/milan_soc.py:1402-1483` against pinned migen `genlib/fifo.py` (AsyncFIFO, AsyncFIFOBuffered) and LiteX `stream.py:170-298`, `axi_lite.py:617-655`, `gen/fhdl/memory.py:36-41,94-183` and `gen/fhdl/verilog.py:521-540` - each property checked:
- The bit order matches `_FIFOWrapper`, and the width guard refuses a mismatch.
- Both arrays use the FIFO's own `adr`/`we` and read address, so every entry is in both at every moment.
- The read word is registered per array, the form LiteX's emitter writes for any two-clock array. Storage stays unreset, as in LiteX.
- The original array and both its ports leave the specials, and `read.dat_r` has one driver (probe R8; the generated `mac_tx_chain.v` diff).
- The `ram_style` attribute precedes LiteX's memory comment block and binds to the `reg` declaration.
- The gray-pointer control and its synchronizers are LiteX's, so CONTRIBUTING section 1's CDC rule is not engaged.
- No array has a read enable. A write/read collision on the empty slot is therefore re-read before `readable` can rise through the two-stage synchronizer.

[R590] PASS Robustness - `receipts/robustness/robustness_head.log` (R1-R8) and the lane test's `reset` and `depth` verdicts at the head - each case checked:
- The all-sys configuration builds no crossing on either path.
- A second placement, a same-domain crossing and a non-crossing module are refused by name. A param-carrying crossing and a common-reset crossing are handled.
- A reset with beats in flight leaves no stale or phantom beat, and the crossing is exact and full-depth after it.
- A one-sided MAC reset is caught, and so is a CSR crossing in the MAC reinit domain. The CSR crossing passes traffic untouched through a MAC reinit.
- Under backpressure a crossing fills to exactly 17 (MAC) or 4 (CSR) entries and drains intact.

[R590] PASS Tests - `sw/litex/test_retained_cdc_storage.py` at the head (42/42, 7/7 controls), `receipts/mutants/results.json` (12/12 reviewer mutants caught), the LiteX aggregate 6/6 with self-test 10/10, `gptp_txts` (85 checks, 6/6 mutants) and generator `--check` at both levels - each property checked:
- The reference is stock LiteX, not the implementation.
- Stock and product are simulated in the SoC's emitted read form (`as_emitted`, `:455-468`). That makes the `READ_FIRST` declaration invisible to simulation by design. The structural `blockram` check and its control cover exactly that gap.
- Each control and each reviewer mutant fails its named check.
- S1 is optional.

[R590] PASS Docs - `docs/litex/CLOCK_DOMAINS.md:217-262`, `docs/testing/TESTING.md:681-696`, `docs/design/MARK_II_AREA_PLAN.md:450-487,672-701,856-862`, `docs/design/AREA_BUDGET.md:194-200,270-275`, helper docstrings `milan_soc.py:774-781,1403-1410,1434-1457,1487-1489`, and the PR #710 body; 18 gates rc 0 - each property checked:
- Changed contracts are documented where the crossing map and the lane ledger live.
- The measured figures match the r1 evidence tree's census and route tables: 50,267 - 50,139 = 128; 11 RAM32M x 4 = 44; RAM32X1D level.
- The round-2 condition is stated in both the docstring and CLOCK_DOMAINS.
- No obsolete requirement is restored.
- RESIDUE R590-1-R2 is wording only; S2 is optional.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #640 lane M2 and round-2 assignments, D3/D7 rulings; `milan_soc.py:773-838,1399-1490,1801-1807`; plan L3 and M2 ledger; AREA_BUDGET; gate record and `check-baseline`; executor route and census figures | R590-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |
| RTL | CLEAN | `milan_soc.py` diff; pinned migen/LiteX FIFO, stream, AXI-Lite and emitter sources; regenerated `mac_tx_chain.v`; E1 emitter identity; probe R8; reviewer OOC mapping (`receipts/ooc/`) | R590-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |
| Robustness | CLEAN | probes R1-R8; lane `reset`/`depth` verdicts and reset controls; reviewer mutants on write enable, domain and read pointer | R590-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |
| Tests | CLEAN (S1 optional) | lane test and 7 controls; 12 reviewer mutants; LiteX aggregate and self-test; `gptp_txts` and its mutants; generator check | R590-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |
| Docs | CLEAN (RESIDUE R590-1-R2 carried; S2 optional) | CLOCK_DOMAINS, TESTING, MARK_II_AREA_PLAN, AREA_BUDGET, helper docstrings, PR body; 18 docs and quality gates | R590-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |

## Real limits

- **Integrated image.** I did not route or synthesize the integrated image. The following are executor evidence:
  - the base and M2 routes (at `4177835c`) and the route census;
  - the 8x8 crossing-Verilog identity;
  - the round-2 synthesis census at `67a3b68d` (RAMB36 74, RAMB18 27, no Synth 8-6849).
  The round-2 receipts (HANDOFF "Round 2", RECEIPTS, r2-evidence) are not yet in a public evidence tree; only the REVIEW READY comment states them. E1 corroborates that the head's crossings emit the same Verilog as the measured commit.
- **Builder.** `sw/builder/test_builder.py --require-elaboration --require-rv32` was not run, because the builder bank is not allowed in this round. So `add_milan_datapath`'s call to `_cross_csr_bus` (`:838`) was checked here only by reading it. The executor's builder receipt and hosted `elaborate` cover its elaboration.
- **Simulation model.** migen simulates block and distributed `Memory` identically, so the lockstep proves function, not mapping. Mapping rests on the structural `blockram` check, E1, the executor's census and the reviewer OOC runs (evidence item 6). Those runs synthesize bench harnesses, not the image; they bracket the image's port usage from above (every flag read).
- **Block RAM across asynchronous clocks.** The collision argument (no read enable; the slot is re-read before `readable` rises) is a protocol argument, not a hardware measurement. It is the same inference and clock pair as the MAC crossings' block RAM already in the base image.
- **LiteX environment.** Its LiteX and liteeth working trees carry local modifications (VexiiRiscv core, BIOS, GMII PHY). None is on the crossings' path. The migen package equals its pinned checkout. The lane test was not rerun under CPython 3.12.3.
- **Hosted.** This is a snapshot only, and several contexts were still in progress. The manager owns hosted and local-replica acceptance.
- **Hardware.** None was touched. Physical calibration NOT RUN; field skips are not hardware proof.
- **Manager source bank.** None exists at this head, and none is claimed or inferred.

## Pending manager duties

- Publish the executor's round-2 evidence (HANDOFF "Round 2", RECEIPTS, r2-evidence), so the round-2 census and OOC claims are public.
- Accept the hosted results at the exact head: `elaborate`, `docs-check`, `firmware-unit`, the remaining Verilator shards and the `rtl-fast`/`rtl-full` runs.
- Build and validate the current-dev merge candidate (builder and native banks), then check post-merge containment.
- Carry RESIDUE R590-1-R2 to the residue checklist.
- Rule on the executor's offered AW/AR block-RAM option (+2 RAMB18, which fails the zero-growth gate). The record stays unchanged under D7 until M9.

## Probe hygiene

- Every probe ran from this packet or a scratch copy. Planted trees, emitted benches and Vivado work stayed under `scratch/`, which is not published.
- The only in-clone outputs were the `gptp_txts` build products (`obj_dir/`, `obj_pad/`, `gptp_ucode.hex`), removed after the run.
- Vivado ran only after every other campaign of this round had finished, one run at a time under the host lock.
- Published receipts have host names, user names and absolute host paths replaced by `<host>`, `<user>`, `<home>` and `<data>` placeholders; nothing else in them was edited.
- Clone integrity after the probes (`scripts/integrity.sh`, `receipts/integrity/integrity_after_probes.txt`, repeated at the end as `integrity_final.txt`):
  - HEAD and tree match, `git status --porcelain --ignored` is empty, and there is no index or worktree diff;
  - `git ls-files -s` equals `git ls-tree -r HEAD` (mode, blob, path; digest `4d470133...`), and every tracked file's bytes and mode equal its blob;
  - gitlinks: `gptp-processor 5dce647a`, `protocol-processor 2ad2f845` and `third_party/verilog-axis 48ff7a7e` are initialised and clean; `external efeb541a` and `third_party/lwSRP 9197193e` are not initialised, as at the start.
- No source edit, commit, push, GitHub write, merge or hardware access was made.

R590-2 FINISHED
