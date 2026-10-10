[R591] POSITIVE - exact head f340d92372b5d04cb74b0ee4425ce353a83133a7

# R591-2: external review of PR #710 (issue #640, Mark II lane M2 / plan L3), round 2

- **Head:** `f340d92372b5d04cb74b0ee4425ce353a83133a7`, tree `e35a54e76e9ae1aae9b27b25fd25ccec14ecdc4d`.
- **Base:** source base dev `e8454e2751d05b02ee8e5a571857589ab358ab86`, which is also live `dev` at review time (`git ls-remote`). The base is an ancestor of the head.
- **Diff `e8454e27..f340d923`:** 10 files, +906/-28, in five one-line commits with no trailers:
  - `4177835c`: the product change, and the measured commit;
  - `2b22bf29` and `cfd74eb9`: docs and test annotations;
  - `67a3b68d`: `READ_FIRST`, the `blockram` check, MAC benches built from `MilanMAC`, and the regenerated chain;
  - `f340d923`: docs and a docstring.
- **Role:** external independent reviewer, cleared context.
- **Sources, in order:**
  - AGENTS.md, CONTRIBUTING.md (sections 1-3) and docs/README.md;
  - the #640 body and its public scope decisions: the lane M2 assignment (comment 6095827337), the D3/D7/D8 manager rulings, the owner's D2/D4/D5/D9 decisions, and the round-2 assignment;
  - `docs/design/MARK_II_AREA_PLAN.md` (L3 and the ledgers), `docs/design/AREA_BUDGET.md` and `docs/litex/CLOCK_DOMAINS.md`;
  - the diff and history;
  - the published evidence tree `review-evidence/640-m2-r1` at `16c5a041` (HANDOFF, PR-BODY, RECEIPTS), plus the executor's round-2 REVIEW READY on #640 and the PR body.
- **Order of reading.** Prior public findings (R591-1, R590-1) were read only after my own pass and a draft verdict.

## Verdict basis

No BLOCKER, MAJOR or MINOR is open. All five lenses are covered clean at this exact head.

What the evidence shows:
- Only the storage of the seven retained crossing arrays moved. The crossing control, widths, depths, read latency, buffering, clock domains and the paired MAC reset are unchanged.
- Lockstep against stock LiteX holds on every edge at two clock ratios. The planted defects fail by name: 7/7 lane controls and 11/11 independent reviewer probes.
- The LiteX-emitted crossing Verilog, which is what the SoC uses, is byte-identical between the measured commit `4177835c` and this head. The routed figures therefore carry over to this head.
- R591-1-F1, my own round-1 MINOR, is resolved.

Open items:
- three SUGGESTIONs, one of them carried from round 1;
- one RESIDUE, carried from R590-1.

## Scope derived from the issue

The #640 body sets the milestone acceptance: at most 38,040 LUT with timing met, unchanged function, and a re-recorded gate.

This PR is one lane of that milestone. It "Relates to #640" and does not close it. Its frozen lane acceptance is the M2 assignment (6095827337):
- Inspect `mac_tx_cdc`/`mac_rx_cdc`, keeping their buffering and paired reset.
- Inspect the `milan_axil_cdc` AW/W/B/AR/R FIFOs, keeping AXI-Lite ordering.
- Convert storage only where it saves LUTs.
- Preserve widths, depths, throughput, reset behaviour and every clock-domain contract.
- Exclude `tx_sf`, LiteDRAM, `memory_port_cdc*`, the CPU bridges, `descmem_*`/`respmem_*`/`nvmmem_*`, the mailbox rings and the media/gPTP tables.
- Target about 200 LUT (100-400), with at most +2 tiles.
- Proof:
  - per-array lockstep, with wrong-depth, wrong-reset and ordering-break controls;
  - the owning suites in both shapes;
  - the primitive mapping;
  - an M0s-recipe route and gate.
- Re-record only if all of that holds. D7 keeps the record until M9.
- Report the measured saving against the estimate.

## Findings

### R591-2-S1 SUGGESTION - Tests - `sw/litex/milan_soc.py:838` (`add_milan_datapath` -> `_cross_csr_bus`), `sw/litex/test_retained_cdc_storage.py:196-214`

- **Evidence:**
  - The MAC half of R591-1-S1 is fixed. The benches take the crossings from a real `MilanMAC` (`test_retained_cdc_storage.py:218`), and control `milanmac-call-site-removed` fails `storage` (`receipts/lane_test_full.log`).
  - The CSR half remains. The test builds the CSR crossing by calling `_cross_csr_bus` itself, so dropping the call at `:838` would pass every check.
  - The PR body lists this under "Known limitations" with a reason: elaborating `add_milan_datapath` needs builder outputs.
- **Impact:** function-neutral, because stock storage is the reference. Only area moves (+2 RAMB18), and a routed gate check would catch that.
- **Optional:** assert the converted CSR storage on an elaborated SoC, for example from the builder's elaboration.

### R591-2-S2 SUGGESTION - Tests - `sw/litex/test_retained_cdc_storage.py:481-484`, `:340-344`

- **Evidence:** `storage` and `blockram` are judged once per bench and then copied onto every channel of that bench. A defect in one array therefore fails the verdict of every array in the bench. Reviewer probe `csr-wrong-channel-aw` fails `storage`/`blockram` on all five CSR channels, including B and R (`receipts/mutants.log`).
- **Impact:** none on detection. The `VERDICT <array> storage FAIL` lines do not localise the faulty array.
- **Optional:** compare the arrays under each channel's own FIFO, or label these two checks as per-bench.

### R591-2-S3 SUGGESTION - RTL, Docs - `sw/litex/milan_soc.py:796-797`; `docs/design/MARK_II_AREA_PLAN.md:672-701` (retains R590-1-S2)

- **Evidence:** R's read word now leaves a RAMB18 with no output register into the CPU's AXI-Lite bridge in the sys domain. `_axis_dp_cdc`'s own comment records an earlier BRAM clock-to-out violation class. The routed M2 run meets timing (WNS +0.306 is the global worst; executor evidence). The ledger section still does not record that path's own slack.
- **Optional:** record the routed slack of the R-channel RAMB18 path in the M2 section.

### R591-2-RES1 RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:698`; PR #710 body (retains R590-1-R2)

- **Evidence:** at this head, line 698 still reads "The changed arrays' whole LUTRAM footprint was 72 sites."
  - The 72 sites are AW 12 + W 24 + AR 12 + R 24 (HANDOFF section 1), and AW and AR are not changed.
  - The changed arrays (MAC x2, W, R) held 48 sites.
  - The figure is right for the seven L3 arrays, and the argument it supports (storage alone cannot reach 100) holds either way.
  - No measurement, gate, test or claim changes, so this is wording only.
- **Exact fix:** replace the sentence with "The seven L3 arrays' whole LUTRAM footprint was 72 sites (AW 12, W 24, AR 12, R 24)." In the PR body, change "The arrays' whole LUTRAM footprint was 72 sites." the same way.

## Prior public findings at this head

| Finding | Status at `f340d923` | Evidence |
|---|---|---|
| R591-1-F1 MINOR (RTL, Robustness, Docs): an unbuffered crossing's payload fell to LUTRAM when its flags were read | **Resolved** | See below |
| R591-1-S1 SUGGESTION (Tests): MilanMAC call site not exercised | **Resolved** for MilanMAC; the `_cross_csr_bus` call-site part is **retained** as R591-2-S1 | Control `milanmac-call-site-removed` is caught: rc 1, fails `mac_tx`/`mac_rx` `storage` and `blockram` |
| R591-1-R1 RESIDUE: PR status named `2b22bf29` | **Resolved** | The PR body Status reads "GREEN at `f340d923`" |
| R590-1-R1 RESIDUE: same stale status | **Resolved** | As above |
| R590-1-R2 RESIDUE: "changed arrays ... 72 sites" | **Retained** as R591-2-RES1 | `MARK_II_AREA_PLAN.md:698` is unchanged |
| R590-1-S1 SUGGESTION: MAC bench bypasses MilanMAC | **Resolved**; the CSR part is retained in R591-2-S1 | As for R591-1-S1 |
| R590-1-S2 SUGGESTION: R-channel RAMB18 slack unrecorded | **Retained** as R591-2-S3 | The ledger section is unchanged on this point |

How R591-1-F1 is resolved:
- `_payload_in_block_ram` now declares `READ_FIRST` on both split arrays (`milan_soc.py:1473`). Each array therefore registers its own read word, and no shared read-address register remains for synthesis to merge.
- The root cause is confirmed independently. Round 1's harness used migen's emitter. `receipts/emit_compare.txt` shows that at `4177835c` migen emitted twin `memadr` read-address registers, and at the head it emits `memdat <= storage[adr]` per array.
- LiteX's emitter forces `READ_FIRST` on every two-clock array anyway (pinned LiteX `litex/gen/fhdl/memory.py:37-41`). The SoC's Verilog is therefore byte-identical between `4177835c`, `67a3b68d` and the head for all three benches.
- The lane test's `blockram` check reads every framing flag under both emitters and passes for all seven arrays. Control `read-address-registered`, the `cfd74eb9` form, fails it on every bench.
- The docstring (`milan_soc.py:1433-1457`) and `CLOCK_DOMAINS.md:242-263` now state the cost exactly: an unread flag is trimmed, and a read flag costs one RAM32X1D and one flip-flop.
- The Vivado result for the flags-read variants is executor evidence that is not published (see limits). The structural condition named in round 1 is now met under both emitters.

## Lens results (each applied at this head)

[R591] PASS Conformance - #640 comment 6095827337 (M2 scope/proof list) and D3/D7 rulings against `git diff e8454e27..f340d923`, `sw/litex/milan_soc.py:773-797,1402-1490,1800-1808`, `docs/design/MARK_II_AREA_PLAN.md:672-701` - each scope item checked:
- **Only the in-scope arrays change.** `_payload_in_block_ram` has exactly four product call sites (W, R, mac_tx, mac_rx). `_axis_dp_cdc` is unchanged, and no excluded object appears in the diff.
- **Buffering, depth 16, paired reset and AXI-Lite channel order are kept.** The lockstep, depth and reset verdicts show this, and so do probes `mac-cdc-unbuffered` and `mac-rename-dropped`, which are caught.
- **No read-latency change.** Cycle-exact lockstep against stock LiteX holds on every edge, so no D3 bound is needed.
- **The lockstep proof and its three named controls exist and are caught:** half depth fails `depth`, a one-sided reset fails `reset`, and reading one entry ahead fails `order`.
- **No re-record, consistent with D7.** `check-baseline` passes 3 endpoints, and `syn/ooc/pp_resource_baseline.json` is not in the diff.
- **The saving is reported against the estimate:** 34 LUT reproducible, below 200 (100-400), with 0 of the +2 tiles used. It is stated in the plan, in AREA_BUDGET and in the PR.
- **The route and gate are executor evidence at `4177835c`.** The crossing Verilog the SoC uses is byte-identical at the head (`receipts/emit_compare.txt`).

[R591] PASS RTL - `sw/litex/milan_soc.py:1402-1490` against pinned migen `4c2ae8df` `genlib/fifo.py:187-245` and LiteX `a1e1c365` `stream.py:170-192,237-300`, `axi_lite.py:617-660`, `gen/fhdl/memory.py:17-41`; `receipts/emit_compare.txt`, `tb/verilator/gptp_txts/generated/mac_tx_chain.v` diff:
- **The FIFO control is untouched.** Only the `Memory` special is replaced, and the gray counters, MultiRegs and compares stay LiteX's.
- **Bit order is preserved.** The split follows `_FIFOWrapper`'s LSB-first payload, param, first, last order, and a width guard refuses any mismatch.
- **Both new arrays use the old ports' address and enable,** and the read data is the concatenation.
- **Storage has no reset, as in LiteX.** A read port with no enable re-reads every cycle, so a write/read collision on an empty entry is re-read before `readable` asserts through the two-stage sync. This is the same pattern as the MAC RAMB36 already in the base.
- **The SoC Verilog is identical** between the measured commit and the head under LiteX's emitter.
- **The regenerated chain differs only by the split** and the data-registered read form.

[R591] PASS Robustness - `receipts/lane_test_full.log` (reset with beats in flight, stall to capacity, CSR through a MAC reinit), `receipts/probe_sys_shape.log`, `receipts/probe_raw_migen_form.log`, `receipts/mutants.log`:
- **Reset and backpressure.** A destructive reset with beats in flight leaves 0 stale beats, and the crossing is exact and full-depth afterwards. Stalled fill reaches 17 (MAC) or 4 (CSR) entries and drains intact.
- **Feature-off shape.** With `milan_cd == "sys"`, `MilanMAC` builds no crossing and `_cross_csr_bus` returns the same interface.
- **Guards.** The width guard and the shape guard refuse by name.
- **Raw migen read form.** The two read forms differ at three edges only (t = 650.5 and 651.0), all inside the 650-660 destructive-reset window. That bounds what the test's `as_emitted` normalisation hides.
- **A reset-domain fault** (`mac-rename-dropped`) is caught.

[R591] PASS Tests - `sw/litex/test_retained_cdc_storage.py` at the head, run by the reviewer: 42/42 VERDICT PASS, 7/7 controls caught, rc 0. Further evidence:
- **Reviewer probes:** 11/11 caught (`scripts/probe_mutants.py`, `receipts/mutants.log`). They cover:
  - framing never written;
  - concatenation swapped;
  - `lsb` not advanced;
  - AW converted instead of W;
  - `ram_style` swapped;
  - read port in the write domain;
  - asynchronous-read latency change;
  - write address ahead;
  - MAC rename dropped;
  - MAC crossing unbuffered;
  - R not converted.
- **Owning suites:**
  - LiteX aggregate 6/6, and its self-test 10/10;
  - `gptp_txts` 85 checks, 0 failures, 6/6 controls;
  - `gen_mac_tx_model.py --check` OK.
- **Reference.** The reference is stock LiteX, not the implementation.
- **Open items.** S1 and S2 are optional.

[R591] PASS Docs - `docs/litex/CLOCK_DOMAINS.md:217-263`, `docs/testing/TESTING.md:681-696`, `docs/design/MARK_II_AREA_PLAN.md:454,672-701,856-861`, `docs/design/AREA_BUDGET.md:197-199,273-274`, docstrings at `milan_soc.py:773-783,1433-1457`, and the PR body:
- **Claims checked against the evidence above:**
  - the storage split and the cost per read flag;
  - the seven arrays and seven controls;
  - 34/128 LUT, with no tile used;
  - the +2 ledger row kept as a maximum, consistent with "deferring it frees none" and the week-4 re-pricing.
- **Gates, all rc 0 at the head:**
  - docs gates: `docs_check`, `check_em_dash --base e8454e27`, `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors`, `check_doc_paths`, `DOC_MAP --check`;
  - quality ratchets: `check_py_idiom`, `measure_naming`, `measure_test_evidence`, `check_hygiene`, `measure_fail_fast`;
  - `git diff --check e8454e27 HEAD`.
- **Open items.** RES1 is wording only, and S3 is optional.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #640 lane M2 assignment, D3/D7 rulings, round-2 assignment; diff; `milan_soc.py:773-797,1402-1490,1800-1808`; plan L3/M2 sections; gate `check-baseline`; emitter identity `4177835c` = head | R591-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |
| RTL | CLEAN | `milan_soc.py` split/guards; pinned migen/LiteX FIFO, AXI-Lite CDC and memory emitter sources; emitted Verilog at base/`4177835c`/`67a3b68d`/head under both emitters; regenerated `mac_tx_chain.v` | R591-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |
| Robustness | CLEAN | reset/stall/reinit verdicts; sys-shape and guard probe; raw-migen-form probe; reset/buffering mutants | R591-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |
| Tests | CLEAN (S1, S2 optional) | lane test + 7 controls; 11 reviewer probes; LiteX aggregate 6/6 + self-test 10/10; `gptp_txts` + 6 controls; generator check | R591-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |
| Docs | CLEAN (RES1 residue, S3 optional) | `CLOCK_DOMAINS.md`, `TESTING.md`, `MARK_II_AREA_PLAN.md`, `AREA_BUDGET.md`, docstrings, PR body; 7 docs gates, 5 quality ratchets, `git diff --check` | R591-2 | `f340d92372b5d04cb74b0ee4425ce353a83133a7` |

## Independent evidence produced (receipts in MANIFEST.sha256)

| Run | Result | Receipt |
|---|---|---|
| Lane test, full, `--jobs 7` | rc 0; 42 PASS; 7/7 controls; 3 min 11 s; 77 MB RSS | `receipts/lane_test_full.{log,rc}` |
| LiteX aggregate | rc 0; 6/6 | `receipts/litex_aggregate.{log,rc}`, `receipts/litex-sim-logs/` |
| Aggregate self-test | rc 0; 10/10 | `receipts/litex_selftest.{log,rc}` |
| `make -C tb/verilator/gptp_txts` (pinned Verilator 5.050) | rc 0; 85 checks, 0 failures; 6/6 controls | `receipts/gptp_txts_make.{log,rc}` |
| `gen_mac_tx_model.py --check` | rc 0; OK, region `792c35e9020a` | `receipts/genmac_check.{log,rc}` |
| `pp_resource_gate.py check-baseline` | rc 0; 3 endpoints | `receipts/gate_check_baseline.{log,rc}` |
| Docs and quality gates (12), `git diff --check` | all rc 0 | `receipts/gate_*.{log,rc}` |
| Reviewer mutation probes | 11/11 caught | `scripts/probe_mutants.py`, `receipts/mutants.{log,rc}`, `receipts/mutants/` |
| Emitter comparison: base, `4177835c`, `67a3b68d`, head | LiteX-emitted crossings identical `4177835c` = `67a3b68d` = head; migen form changed only to per-array data registers | `scripts/probe_emit.py`, `receipts/emit_compare.txt`, `receipts/emit/` |
| Raw migen read form (normalisation disabled, scratch copy) | rc 1 only on `csr_w`/`csr_r` `lockstep` at t = 650.5 and 651.0, inside the reset window | `receipts/probe_raw_migen_form.{log,rc}`, `scripts/probe_raw_form_test_copy.py.txt` |
| Feature-off shape and guards | rc 0; no crossing, same interface, both guards refuse | `scripts/probe_sys_shape.py`, `receipts/probe_sys_shape.{log,rc}` |
| Hosted snapshot | see limits | `receipts/hosted_check_runs.tsv` |
| Environment identity | pins, patch digests, Verilator | `receipts/env_identity.txt` |
| Clone integrity | clean; see below | `receipts/clone_integrity.txt` |

## Real limits

- **Executor evidence, not reproduced.** I did not reproduce:
  - the integrated routes at `e8454e27` and `4177835c`;
  - the gate `check` runs on them;
  - the integrated synthesis census at `67a3b68d`;
  - the out-of-context Vivado mapping, including round 2's six flags-read variants;
  - the 1x1/8x8 byte-identity;
  - the builder `--require-elaboration --require-rv32` run.

  Round-2 Vivado and census logs are not in the published evidence tree; `16c5a041` carries round 1 only. Their figures are public only as summaries in the REVIEW READY comment and the PR body.
- **No Vivado.** I ran no Vivado: another Vivado job and several heavy builds were active on the host (load about 35). F1's fix is established structurally, under both emitters, plus the executor's summary.
- **Builder bank not run** (not allowed in this round). The `add_milan_datapath` -> `_cross_csr_bus` integration is not exercised by any test I ran (S1).
- **LiteX environment.** I used exports of the pinned revisions with the repository's patch series 0002/0007/0004/0006 applied in scratch. 0005 (VexiiRiscv pythondata) was not applied, because it is not on the crossings' path. The base interpreter was CPython 3.14.7. No CPython 3.12 run was made.
- **Hosted contexts at the head** (snapshot 2026-10-10T14:53Z):
  - executed and green: `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, Verilator shard 3/5, `wire-accountability`, `yosys-elaboration`, Yosys shards 0-3/4;
  - skipped, so not hardware proof: `Physical gPTP`;
  - in progress and not claimed: `docs-check`, `elaborate` (which runs the LiteX aggregate), `firmware-unit`, and Verilator shards 0, 1, 2 and 4.
- **No hardware.** Physical calibration NOT RUN. No manager source bank exists at this head, and none is claimed or inferred.

## Pending manager duties

- Accept the hosted results at the exact head: `elaborate`, `docs-check`, `firmware-unit`, Verilator shards 0/1/2/4, and the `rtl-fast`/full verdicts.
- Build and validate the current-dev merge candidate (builder and native banks) and link its receipts. The source base equals live dev `e8454e27` at review time.
- Carry RES1 (R590-1-R2) to the residue checklist, with the exact fix above.
- Decide whether to publish the round-2 executor receipts (the Vivado flags-read variants and the `67a3b68d` census).
- Rule on the offered AW/AR block-RAM option (+2 RAMB18, a zero-growth gate failure).
- Check post-merge containment; the lane does not close #640.

## Reviewer actions and integrity

- **Execution.** Long jobs ran detached with their own log and rc files, and were polled to completion in the foreground.
- **Disposable trees** stayed under `scratch/`: pinned LiteX exports, `git archive` trees at four commits, planted copies and emitted Verilog.
- **Cleanup.** The only artifacts created in the clone were ignored `gptp_txts` build outputs (`obj_dir/`, `obj_pad/`, `gptp_ucode.hex`). They were removed with `git clean -fdX tb/verilator/gptp_txts`.
- **Clone integrity after the probes** (`receipts/clone_integrity.txt`):
  - `git status --porcelain --ignored --untracked-files=all` is empty;
  - `git ls-files -s` equals `git ls-tree -r HEAD` (digest `4d470133...`);
  - all 1,271 tracked regular files match their index blob byte for byte (`git hash-object --no-filters`) and mode for mode;
  - the gitlinks are `gptp-processor 5dce647a`, `protocol-processor 2ad2f845`, `third_party/verilog-axis 48ff7a7e`, `external efeb541a` (not initialised) and `third_party/lwSRP 9197193e` (not initialised), and the three initialised submodules are clean.
- **No other actions.** No source edit, commit, push, GitHub write, merge, Docker/act or hardware access was made. The shared LiteX checkout was used read-only, with bytecode writes disabled.

R591-2 FINISHED
