[A516]

# Handoff: issue #234, the #229 area baseline, ranking, budget and gate

Status: ROUND 5 REVIEW READY at `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` (see "Round 5" at the end), on top of
`79e53831a4f623a594f22765be1d05dffeb696a7` (round 4, pushed by the manager to PR #638; R447-4 POSITIVE, R446-4
NEGATIVE on one MINOR). Rounds 1 to 4 below are kept as published; the "Round 5" section at the end supersedes them
where they differ.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5966260488
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5966304381
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967818534
- Branch `234-area-baseline`, base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b` (processor pin `631eeb34`).
  Remote `https://github.com/kebag-logic/milan-fpga.git` confirmed; HEAD was `1269cdaf` at entry; worktree clean at exit.
- Executor [A516]; reviewers [R446] (internal) and [R447] (external).
- Scratch root, never committed or pushed: `$VALIDATION_STORAGE/234-a516` (scratch repos `A/repo`, `B/repo`, run
  directories under `A/work`, `B/work`).

Commits (one-line subjects, no body, no trailers):

| Commit | Subject |
|---|---|
| `22460b6b7` | Let the baseline recipe constrain the standalone wrapper at its bound CLK_HZ_P with --integrated-clock |
| `8ffbce867` | Add a resource-regression gate for the protocol processor shadow with a planted-regression self-test and its mutants |
| `0932ce151` | Record the issue #234 resource baseline at dev 1269cdaf and run the gate's Vivado-free checks in rtl-fast |
| `bdcce7065` | Publish the issue #234 area baseline, ranking, budget and resource-gate policy |
| `2a765a6c3` | Wrap three resource-gate self-test and mutant lines to the 120-column Python idiom limit |

Diff `1269cdaf..2a765a6c3`: 11 files. No RTL, no processor source, no interface, no generated file other than
`syn/ooc/pp_resource_baseline.json` (records written only by `pp_resource_gate.py record --write`) and the
Contents blocks (written by `scripts/gen_toc.py --write`; descriptions by hand).

| File | Change |
|---|---|
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` | new: the baseline, sub-blocks, storage mapping, Yosys reconciliation, ranking, receipts |
| `docs/design/AREA_BUDGET.md` | new section "Protocol processor budget and resource gate"; link to the findings; Contents separator to `--` (CONTRIBUTING 6.1) |
| `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` | `--integrated-clock`, the elaboration route to 8x8 parameters, a "Resource gate" section |
| `syn/ooc/pp_resource_gate.py` | new gate (record / check / check-baseline / --selftest) |
| `syn/ooc/pp_resource_gate_selftest.py` | new: 51 planted arms, end to end through the real parser |
| `syn/ooc/pp_resource_gate_mutants.py` | new: 25 enforcement-removal mutants, each must fail the self-test |
| `syn/ooc/pp_resource_baseline.json` | new: A's three endpoints and their policy |
| `syn/ooc/pp_baseline.py` | `standalone_clock()`, `--integrated-clock`, `clock_selftest()` |
| `syn/ooc/pp_baseline_mutants.py` | four new mutants for the clock code (32 total, all killed) |
| `.github/workflows/rtl-fast.yml` | three lines added to the existing OOC step: gate self-test, mutants, `check-baseline` |
| `scripts/ci_events.py` | the pinned step list for that step, same three lines |

## 1. Measurement method

Combinations, each a local scratch git repository built from the lane and never pushed:

- A: `git archive` of lane HEAD `1269cdaf` plus the three public submodules fetched at their gitlinks
  (`protocol-processor` `631eeb34`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`), each
  verified with `git -C <submodule> rev-parse --show-toplevel` before any git command. Its `ls-tree -r` equals lane
  HEAD's except the SSH-only `external` gitlink, which no gate reads. Scratch commit `75eba3715f6c`.
- B: the same tree; `protocol-processor` advanced to `ddb3119dbbce59f81bf7a536a1ad90a20546edb2` fetched from
  `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git` (`631eeb34` is its ancestor);
  then `parent-adoption-c8-cdf49d1a.patch` (sha256 `aa5a88eb8e04e5ce0d44ec65973e88215860a9ea5317255016409442000ad209`)
  and `parent-adoption-p2-cdf49d1a.patch` (sha256 `590f791de7fc5d00986a8d76c43e4488d522305b19876b8b4f30bc0a76f539fa`)
  applied with `git apply --check` then `git apply`, in that order. Scratch commit `e06ca4b7b235` (9 files, +83 -27,
  gitlink included). Functional processor HDL change A to B: `KL_pp_nvm_port` deadline (`MEM_TIMEOUT_CYC_P`) and its
  top binding `NVM_MEM_TMO_CYC_P = CLK_HZ_P`; `KL_acmp_nvm_shadow`, `KL_aecp_desc_store`, `KL_aecp_nvm_writer` and
  `KL_pp_nvm_mgr_arb` change only comments. Neither patch changes a wrapper parameter (both shapes' 21 parameters equal).

Tools: Vivado v2026.1 build 6511674 (`$WORKSPACE_HOME/Xilinx/2026.1`), part `xc7a100t-fgg484-2`; LiteX venv with the four
repository patches already applied (`git apply --reverse --check`, not modified); RV32 SDK
`riscv32-ilp32d--glibc--stable-2025.08-1` (`scripts/ci_rv32_sdk.py --verify-only`, rc 0); Yosys 0.66
(`86f2ddebc-dirty`), sv2v v0.0.13, jemalloc preload (results allocator-independent per `syn/yosys/README.md`);
Python 3.14.7; GNU Make 4.3 built here from `make-4.3.tar.gz` (sha256 `e05fdde4...8e19` verified, `./configure
--disable-nls && make`, binary sha256 `2cc4089ab4ef599e924c1fd7d34ff16dc322b662d52df381a2a4a45c3a81234f`) first on
`PATH` for every gate.

Recipe (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`) per combination:

1. Export: `bash sw/litex/build.sh ax7101|ax8x8 --dry-run` (rc 0 x4), then the printed `milan_soc.py` argv without
   `--build` and with `--output-dir` in the scratch work directory (rc 0 x4; `scratch-scripts/export.py`).
   A and B exports differ only in generated comments.
2. Integrated route: `pp_baseline.py <gateware>`, then `vivado -mode batch -source baseline_integrated.tcl`
   (AreaOptimized_high / ExploreArea / ExtraPostPlacementOpt / AggressiveExplore; 32 threads; default seed; 50 MHz).
3. Standalone: `pp_baseline.py <gateware> --output <ooc> --integrated-log <log> --integrated-clock` (20 ns from the
   bound `CLK_HZ_P` = 50,000,000; the recipe's 10 ns default kept).
4. 8x8 parameters: the 8x8 integrated script cut after `synth_design`, `-rtl -rtl_skip_mlo` added, run in its own
   directory with copies of the export's `.xdc`/`.init` files. Control: the same at 1x1 gives 21 parameters equal to the
   full synthesis log's.
5. Yosys: `syn/yosys/ooc.sh KL_pp_shadow` with `OOC_CHPARAM`/`OOC_SHAPE`/`OOC_TMP` per the recipe; the recipe's
   hierarchical mapping (no `-flatten`) and `pp_baseline_mapping.py` for A.
6. Storage attribution: FFs per array counted by name in `baseline_cells.tsv`; read/write cones per array from the A
   1x1 checkpoint (`scratch-scripts/cone_probe.tcl`, `evidence/A-1x1-storage-cones.tsv`).
7. Control: A 1x1 standalone at 10 ns (#231's clock).

Memory: one integrated synthesis alone reaches the 12 GB cap (about six parallel-synthesis helpers). The first B
route launch ran beside A's synthesis, pushed the cgroup to the cap with 5 GB swapped, and was stopped during
synthesis before any report (partial files in `B/work/killed-run-1`); B was rerun alone. At most two Vivado
instances ever ran together, never beside Yosys; `memory.events` oom 0 throughout.

Every log has zero `Synth 8-4445` diagnostics (one match each: the echoed severity command). Every
`baseline_images.json` image rehashed equal after the runs.

## 2. Figures and run receipts

Integrated shipping route (whole image):

| | LUT | FF | Slice | RAMB36 | RAMB18 | tiles | DSP | CARRY4 | WNS | WHS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 50,128 (79.07 %) | 59,006 | 15,815 (99.78 %) | 79 | 27 | 92.5 | 14 | 3,405 | +0.063 | +0.036 |
| B | 50,753 | 59,014 | 15,827 (99.85 %) | 79 | 27 | 92.5 | 14 | 3,423 | +0.101 | +0.036 |

Zero routing errors; no setup, hold or pulse-width failures; all four signoff corners agree. Critical path A:
`u_rx_validator/hdr_ctlr_eid_r[28]` to `u_tx_arbiter/slot_r[2]`, 36 levels, 19.684 ns; B: `u_notify/rows_r[5][69]`
to `u_tx_arbiter`, 37 levels. Routed split A: `milan_datapath` 41,527 LUT, wrapper name 23,937, CPU 3,526, SoC top
4,857. B: wrapper +259, rest of datapath +389, CPU -17; integrated synthesis whole image 52,807 -> 53,209 (+402).

Standalone `KL_pp_shadow`, 20 ns:

| | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | int. WNS |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1 A | 24,343 | 25,344 | 21 | 3 | 8 | 1,623 | -1.616 |
| 1x1 B | 24,505 | 25,470 | 21 | 3 | 8 | 1,638 | -0.496 |
| 8x8 A | 31,562 | 33,929 | 26 | 5 | 8 | 2,001 | -1.947 |
| 8x8 B | 31,390 | 33,844 | 26 | 5 | 8 | 2,016 | -1.221 |
| 1x1 A at 10 ns | 24,370 | 25,345 | 21 | 3 | 8 | 1,623 | -8.967 |

The 10 ns control shows the clock does not explain the step from #231 (22,350 LUT at 10 ns, pin `990f9652`): the
wrapper grew 2,020 LUT, 812 FF, 3 DSP (in `u_nvm`). In the 1x1 standalone B changes `u_nvm_port` +83 LUT / +33 FF;
untouched blocks moved net +101 LUT (sum of magnitudes 309), `armq_r` +107 FF; at 8x8 B is -172 LUT / -85 FF.

Per-sub-block tables (SRP, ADP, ACMP talker/listener, AECP, microcontroller, saved-state writer, notification, NVM
port, NVM arbiter, ACMP binding store, NVM backend, RX pools, TX slots, trace ring, control FIFO) at both shapes and
both combinations are in the findings page and `evidence/tables.md`; complete rankings in
`evidence/*-ranking.tsv`. Per added stream context (1x1 to 8x8): SRP talker FSM 212 LUT / 221 FF, listener FSM
227 / 278, SRP 590 / 679, wrapper 1,031 / 1,226.

Yosys flattened: 1x1 A 50,578 LUT_TOT (44,582 + 5,996), 23,831 FF, 15/4 RAMB, 10 DSP, 2,067 CARRY4; 1x1 B 50,681;
8x8 A 93,226 (87,066 + 6,160), 33,453 FF, 8,134 CARRY4; 8x8 B 93,063. Gap decomposition (exact): 1x1
26,235 = 17,328 raw + 4,153 combining + 4,754 memory; 8x8 61,664 = 51,733 + 4,809 + 5,122. Hierarchical: SRP +9,478
(1x1), +19,918 (8x8); ACMP talker +19,620 at 8x8 (Yosys 21,457 vs Vivado 1,837 raw); own +6,793 / +11,613.

Run receipts: `receipts/run-receipts.json` (full sha256 and size of every log, report and checkpoint; directories in
scratch); summary table in the findings page. All 17 runs rc 0.

## 3. Ranking (1x1 shipping shape)

| # | Lever | Issue | Where | Measured cost | Est. saving |
|---:|---|---|---|---|---|
| 1 | Registry in distributed RAM, walked for the command-hit check | #232 | `KL_aecp_notify.sv:329`, `:541-544`, `:551-552` | 2,048 FF; read cone 2,292 LUT (upper bound); Vivado 8-7186 "rows_r is not inferred as ram due to incorrect usage" | ~2,000 FF, ~1,500 LUT |
| 2 | SRP timer-arm FIFOs as distributed RAM | #232 class in #230's SRP | `KL_srp_top.sv:947`, `:959-973` | 2,304 FF; 648 LUT + 288 MUXF7 read mux; Yosys keeps it in flops too | ~2,300 FF, ~580 LUT, 288 MUXF7 |
| 3 | Processor timer-arm shift queues as RAM FIFOs | #232 class, processor top | `protocol_processor_top.sv:2921` | 1,153 FF; 1,178 LUT write side | ~1,100 FF, ~1,000 LUT |
| 4 | Share SRP per-stream FSM evaluation | #230 | `KL_srp_talker_fsm.sv:351-392`/`:401-816`; `KL_srp_listener_fsm.sv:348-388`/`:403-850` | talker 662/714, listener 420/667 | ~440 LUT (8x8 ~3,100) |
| 5 | Serial throttle check, stamps in RAM | #232 | `KL_aecp_notify.sv:392`, `:934`, `:1034-1037` | 192 FF, 48 CARRY4 | ~190 FF, 50 LUT |
| 6 | Listener records out of block RAM | #232 class, ACMP listener | `KL_pp_acmp_listener.sv:385` | 5 RAMB36 for 752 bits | 5 tiles for ~250 LUT |

Levers 1-5: about 5,600 FF and 3,600 LUT. Image would be near 46,500 LUT (73 %), still ~8,500 over NFR-RES-01.
#233: not needed for placement headroom (its phase-1 audit found every stream-shaped parameter derived; remaining
candidates are a 5-bit refcount, FIFO/queue depths that levers 2-3 make moot, and an index already in one RAM32M
depth), and it cannot close the NFR-RES-01 gap. The AECP response buffer's historical 5,079-FF spill cannot recur
(the buffer is in main memory, `KL_aecp_resp_buf.sv`); #234's AC2 is nevertheless not met at A (registry and SRP
FIFOs spill about 2,000 FF each).

## 4. Budget

`docs/design/AREA_BUDGET.md`, "Protocol processor budget and resource gate". Accepted headroom target: NFR-RES-01,
at most 60 % LUT (38,040); A is 79.07 % (12,088 over). Slices are the binding limit (35 free at A, 23 at B). Proposed
block RAM reserve 13.5 tiles (ceiling 121.5 tiles; 42.5 free). Timing floor from BUILDING.md section 5 (WNS at least
+0.03, WHS at least 0; met). Allocation: meeting NFR-RES-01 with the rest unchanged needs the wrapper below 11,849
LUT (half of it); #229's 30 % non-CPU milestone (19,020 LUT) is exceeded by the wrapper alone; the levers estimate
~3,600 LUT. So the allocation needs an owner decision; until then the gate holds every resource at its record.

## 5. Gate design and self-test

`syn/ooc/pp_resource_gate.py`: `record` reads one recipe directory (kind from its single recipe script) into
identity (tool build, device, design, state, flow commands without paths/generics, standalone clock), an input
digest (every `read_verilog`/`read_xdc`/`source` file in order, every include-directory header, generics with
basename paths, image digests; generated files normalized for comments/dates and build roots), figures (LUT, FF,
SLICE, RAMB36, RAMB18, BRAM tiles, DSP, CARRY4, WNS, WHS) and sub-blocks (three levels, with CARRY4 from the census).
`check` exits 2 on a kind/identity mismatch or identical inputs with different figures, 1 on growth beyond tolerance,
a ceiling, a timing floor or fall; else 0, printing the 12 largest sub-block movements. `check-baseline` refuses a
baseline whose policy is incomplete or whose record breaks its own floor/ceiling.

Policy (`syn/ooc/pp_resource_baseline.json`): route LUT +500, FF +600, SLICE +80, RAMB/DSP +0, WNS >= +0.030 and
WHS >= 0 with a 0.25 ns fall limit, BRAM ceiling 121.5; ooc-1x1 +250/+250; ooc-8x8 +316/+339; RAMB/DSP +0. About 1 %:
standalone movement in untouched blocks from B's change was 101-309 LUT, so a smaller standalone tolerance judges
noise; the route is the fit, so its 1 % catches B.

Self-test: 51 arms, each planting real report/input text and going through `record` then `judge`: control; changed
source; LUT at/over tolerance; FF over; register rows disagree; slice over; +1 RAMB36/RAMB18/DSP; BRAM ceiling; WNS
below floor; WNS fell beyond / within tolerance; WHS below floor; improvement; tool build, device, placement
directive, thread count changed (2); identical inputs (2); export date only (2); generated logic, include header,
sourced constraint, memory image changed (1); duplicate row, malformed count, missing row, timing columns, missing
report, second recipe script, census header (2); standalone control, clock change (2), generic change (1), moved
image path (2), RAMB18, FF; CARRY4 attribution; 5 baseline refusals; 5 CLI verdicts; cross-kind refusal.
Mutants: 25 enforcement removals in `pp_resource_gate.py`, each fails the self-test; the control passes.
`pp_baseline.py --integrated-clock`: `clock_selftest()` plus 4 new killed mutants (32 in total).

Real data (receipts `gate-check-*.log`): A route / ooc-1x1 / ooc-8x8 against the committed baseline rc 0; B route
rc 1 (LUT +625 > 500; `u_nvm_port` +80, the rest optimization movement); B ooc-1x1 rc 0 (+162/+126); B ooc-8x8 rc 0
(-172/-85); A 1x1 at 10 ns rc 2 (standalone clock identity).

Where it runs (proposal): hosted `rtl-fast` runs self-test, mutants and `check-baseline` (Python only; no new runner
or tool, so no STOP); the Vivado measurement and `check` run in the manager's local bank per merge candidate that
moves the processor pin, `KL_pp_shadow`, the shipping configuration or the build flow (route 50-56 min and 1x1
standalone 15-24 min here, sharing the host). No Yosys hosted ratchet: `syn/yosys/README.md` records a deliberate
decision against a checked-in cell baseline; Yosys does not predict Vivado, has no timing, and its hosted top is the
8-stream default, not the shipping shape.

## 6. Gate table (rc at `2a765a6c3`, worktree clean, GNU Make 4.3 first on PATH)

`$MDPY` = `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python` (Markdown gates). Each command ran in the foreground
from the lane root (physical `/data` path), without a pipeline; `docs-check-no-git` and `feature-status-no-git` set
`GIT_DIR=/dev/null`. Machine record: `receipts/gate-results.json`.

| # | Gate | Command | rc | Receipt |
|---:|---|---|---:|---|
| 1 | dp-srcs-selftest | `python3 syn/ooc/dp_srcs.py --selftest` | 0 | [receipts/dp-srcs-selftest.log](receipts/dp-srcs-selftest.log) |
| 2 | ooc-tcl-selftest | `python3 syn/ooc/ooc_tcl_selftest.py` | 0 | [receipts/ooc-tcl-selftest.log](receipts/ooc-tcl-selftest.log) |
| 3 | pp-baseline-selftest | `python3 syn/ooc/pp_baseline.py --selftest` | 0 | [receipts/pp-baseline-selftest.log](receipts/pp-baseline-selftest.log) |
| 4 | pp-baseline-mutants | `python3 syn/ooc/pp_baseline_mutants.py` | 0 | [receipts/pp-baseline-mutants.log](receipts/pp-baseline-mutants.log) |
| 5 | pp-baseline-reports-selftest | `python3 syn/ooc/pp_baseline_reports_selftest.py` | 0 | [receipts/pp-baseline-reports-selftest.log](receipts/pp-baseline-reports-selftest.log) |
| 6 | resource-gate-selftest | `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | [receipts/resource-gate-selftest.log](receipts/resource-gate-selftest.log) |
| 7 | resource-gate-mutants | `python3 syn/ooc/pp_resource_gate_mutants.py` | 0 | [receipts/resource-gate-mutants.log](receipts/resource-gate-mutants.log) |
| 8 | resource-gate-check-baseline | `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | [receipts/resource-gate-check-baseline.log](receipts/resource-gate-check-baseline.log) |
| 9 | dp-srcs-milan-datapath | `python3 syn/ooc/dp_srcs.py --top milan_datapath` | 0 | [receipts/dp-srcs-milan-datapath.log](receipts/dp-srcs-milan-datapath.log) |
| 10 | dp-srcs-kl-pp-shadow | `python3 syn/ooc/dp_srcs.py --top KL_pp_shadow` | 0 | [receipts/dp-srcs-kl-pp-shadow.log](receipts/dp-srcs-kl-pp-shadow.log) |
| 11 | pp-srcs-check-selftest | `python3 scripts/pp_srcs.py --check --selftest` | 0 | [receipts/pp-srcs-check-selftest.log](receipts/pp-srcs-check-selftest.log) |
| 12 | docs-check | `$MDPY scripts/docs_check.py` | 0 | [receipts/docs-check.log](receipts/docs-check.log) |
| 13 | docs-check-no-git | `GIT_DIR=/dev/null $MDPY scripts/docs_check.py` | 0 | [receipts/docs-check-no-git.log](receipts/docs-check-no-git.log) |
| 14 | feature-status-no-git | `GIT_DIR=/dev/null $MDPY scripts/check_feature_status.py` | 0 | [receipts/feature-status-no-git.log](receipts/feature-status-no-git.log) |
| 15 | feature-status-selftest | `$MDPY scripts/check_feature_status.py --self-test` | 0 | [receipts/feature-status-selftest.log](receipts/feature-status-selftest.log) |
| 16 | em-dash | `$MDPY scripts/check_em_dash.py --base 1269cdafb4bb964c757baae0f0c5a932d43f540b` | 0 | [receipts/em-dash.log](receipts/em-dash.log) |
| 17 | em-dash-selftest | `$MDPY scripts/check_em_dash.py --selftest` | 0 | [receipts/em-dash-selftest.log](receipts/em-dash-selftest.log) |
| 18 | doc-style | `$MDPY scripts/check_doc_style.py` | 0 | [receipts/doc-style.log](receipts/doc-style.log) |
| 19 | doc-style-selftest | `$MDPY scripts/check_doc_style.py --selftest` | 0 | [receipts/doc-style-selftest.log](receipts/doc-style-selftest.log) |
| 20 | doc-paths | `$MDPY scripts/check_doc_paths.py` | 0 | [receipts/doc-paths.log](receipts/doc-paths.log) |
| 21 | toc-selftest | `$MDPY scripts/gen_toc.py --selftest` | 0 | [receipts/toc-selftest.log](receipts/toc-selftest.log) |
| 22 | toc-verify-anchors | `$MDPY scripts/gen_toc.py --verify-anchors` | 0 | [receipts/toc-verify-anchors.log](receipts/toc-verify-anchors.log) |
| 23 | toc-check | `$MDPY scripts/gen_toc.py --check` | 0 | [receipts/toc-check.log](receipts/toc-check.log) |
| 24 | archive | `$MDPY scripts/check_archive.py` | 0 | [receipts/archive.log](receipts/archive.log) |
| 25 | archive-selftest | `$MDPY scripts/check_archive.py --selftest` | 0 | [receipts/archive-selftest.log](receipts/archive-selftest.log) |
| 26 | doc-map-check | `$MDPY docs/DOC_MAP.gen.py --check` | 0 | [receipts/doc-map-check.log](receipts/doc-map-check.log) |
| 27 | module-matrix-check | `$MDPY docs/traceability/gen_module_matrix.py --check` | 0 | [receipts/module-matrix-check.log](receipts/module-matrix-check.log) |
| 28 | solution-docs | `$MDPY scripts/check_solution_docs.py` | 0 | [receipts/solution-docs.log](receipts/solution-docs.log) |
| 29 | baremetal-only | `python3 scripts/check_baremetal_only.py --check` | 0 | [receipts/baremetal-only.log](receipts/baremetal-only.log) |
| 30 | gptp-docs-make | `make -C gptp-processor docs` (GNU Make 4.3) | 0 | [receipts/gptp-docs-make.log](receipts/gptp-docs-make.log) |
| 31 | ci-scope-selftest | `python3 scripts/ci_scope.py --selftest` | 0 | [receipts/ci-scope-selftest.log](receipts/ci-scope-selftest.log) |
| 32 | ci-events-check | `python3 scripts/ci_events.py --check` | 0 | [receipts/ci-events-check.log](receipts/ci-events-check.log) |
| 33 | ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | [receipts/ci-events-selftest.log](receipts/ci-events-selftest.log) |
| 34 | act-ci-selftest | `python3 scripts/act_ci.py --selftest` | 0 | [receipts/act-ci-selftest.log](receipts/act-ci-selftest.log) |
| 35 | py-idiom | `python3 scripts/check_py_idiom.py` | 0 | [receipts/py-idiom.log](receipts/py-idiom.log) |
| 36 | py-idiom-selftest | `python3 scripts/check_py_idiom.py --selftest` | 0 | [receipts/py-idiom-selftest.log](receipts/py-idiom-selftest.log) |
| 37 | fail-fast | `python3 scripts/measure_fail_fast.py --check` | 0 | [receipts/fail-fast.log](receipts/fail-fast.log) |
| 38 | hygiene | `python3 scripts/check_hygiene.py --check` | 0 | [receipts/hygiene.log](receipts/hygiene.log) |
| 39 | todo-ownership | `python3 scripts/check_todo_ownership.py` | 0 | [receipts/todo-ownership.log](receipts/todo-ownership.log) |
| 40 | test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | [receipts/test-evidence.log](receipts/test-evidence.log) |
| 41 | control-flow-selftest | `python3 scripts/measure_control_flow.py --selftest` | 0 | [receipts/control-flow-selftest.log](receipts/control-flow-selftest.log) |
| 42 | cohesion-selftest | `python3 scripts/measure_cohesion.py --selftest` | 0 | [receipts/cohesion-selftest.log](receipts/cohesion-selftest.log) |
| 43 | diff-check-base | `git diff --check 1269cdafb4bb964c757baae0f0c5a932d43f540b HEAD` | 0 | [receipts/diff-check-base.log](receipts/diff-check-base.log) |
| 44 | diff-check-worktree | `git diff --check` | 0 | [receipts/diff-check-worktree.log](receipts/diff-check-worktree.log) |

An earlier run at `bdcce7065` failed only `py-idiom` (three new lines over 120 columns); `2a765a6c3` fixed them and
the whole table above was rerun at that head.

Not run, because nothing they execute changed (no RTL, processor, testbench or Yosys-script change):
`scripts/run_all_suites.sh` (does not invoke any touched script), `syn/yosys/run.sh`, `scripts/lint_rtl.py`,
`scripts/xvlog_gate.py`, `syn/yosys/ooc_selftest.py`, `syn/yosys/cache_selftest.py`, the builder bank.
`scripts/ci_scope.py` classifies the diff as RTL/tooling-relevant (`true`), so the hosted `verilator-suites` and
`yosys-portability` contexts will run on a ready PR head, and CONTRIBUTING's local long gates belong to the
candidate-merge validation.

## 7. Conflicts and decisions needed

1. NFR-RES-01 (at most 60 % LUT) is not met at dev: 79.07 %, 12,088 LUT over; the ranked levers estimate ~3,600.
   #229's "non-CPU stack under 30 %" (19,020 LUT) is exceeded by the wrapper alone; "non-CPU stack" was read as
   `milan_datapath` (41,527 LUT). The per-resource allocation for `KL_pp_shadow` needs an owner ruling; the
   proposed BRAM reserve (13.5 tiles) and the gate tolerances are proposals.
2. #234's first acceptance criterion says "at 100 MHz"; the shipping configuration declares a 50 MHz Milan clock
   (#565), and both routes were measured there (WNS +0.063 / +0.101 ns). At 100 MHz the 19.7 ns critical path
   cannot close.
3. #234's fourth criterion ("CI rejects ...") is met by this proposal only if the manager's local bank counts as the
   CI for the Vivado half. A hosted Vivado runner would be a new runner (a STOP item); none is proposed.
4. #234's second criterion (no unexpected FF spill) is not met at A: the registry (2,048 FF, against its own
   distributed-RAM attribute) and the SRP timer-arm FIFOs (2,304 FF). Fixes are processor RTL lanes (levers 1-2).
5. The next adoption (B) is rejected by the route gate (+625 LUT); accepting it is a reviewed `record --write` of its
   route. It also needs two `syn/yosys/rom_digests.tsv` rows for `ddb3119d` (equal to `631eeb34`'s), which the C8 and
   P2 patches do not carry; without them `syn/yosys/ooc.sh` exits 2 at that pin.
6. New child issues are recommended for levers 1, 2, 3, 5 and 6 (processor RTL); this lane opened none.

No push, PR, merge, rebase, sub-agent, other checkout, hardware, flashing, RTL, processor or interface change.
No existing comment edited.

## Round 2

Status: REVIEW READY at `0feff20fa228d0cb91d507943e6d39495b28b880` (not pushed; the manager pushes).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5968015720
- REVIEW READY (round 2): https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5968531831
- Answers R446-1 (PR #638 comment 5968004900) and R447-1 (5968008794); rulings 5967852698; owner decision 5967924270.
- Reviewer packets read from `origin/234-review-evidence` at `7891d083b08c4b1992a2bf0332ccb9925bc90f00`
  (`review-evidence/234-r1/reviews/R446-1`, `.../R447-1`), exported with `git archive` to
  `$VALIDATION_STORAGE/234-a516/r2/review-evidence`, not checked out. Its `author/evidence` records are byte-identical to
  this directory's `evidence/*.json` (sha256 compared).
- No Vivado run in round 2: every new check reads the existing run directories under `$VALIDATION_STORAGE/234-a516`.
- Same branch, same checkout, three new one-line commits on `2a765a6c3` (no rebase, no amend, no trailers):

| Commit | Subject |
|---|---|
| `9b1d35370` | Hold the resource gate to one exit-code contract, route completion and the budget's policy table, with an arm and a killed mutant per refusal |
| `5c92cacab` | Give B's standalone movement on one named partition, record the manager rulings and owner decision, and index both baseline findings |
| `0feff20fa` | Say that the resource gate reads each route status report at every check rather than storing it, and name the record's levels once |

Diff `1269cdaf..0feff20f`: 14 files (round 1's 11 plus `scripts/ci_scope.py`, `docs/testing/CI_WORKFLOWS.md`,
`docs/findings/README.md`). Round 2 touches no RTL, processor, interface, workflow, pin list or baseline JSON.

### R2.1 Finding-by-finding

| Finding | Severity, lens | Answer | Evidence at `0feff20f` (receipts under `receipts/round2/`) |
|---|---|---|---|
| R446-1 F1: non-finite slack passes | MINOR Conformance, Robustness, Tests | `timing()` refuses (exit 2, named) a WNS or WHS that is `inf`/`nan`, and a summary whose `TNS Total Endpoints` / `THS Total Endpoints` are absent or 0. Arms: WNS `nan`; WNS and WHS `inf`; zero timed endpoints. Mutants `finite slack`, `timed endpoints` killed. | `probes/r446-probe-gate-cli.log`: `nan` rc 2; `inf` + 0 endpoints rc 2, printed BAD only because the probe's literal want is 1 (F1: "exit 2 ... or exit 1"; assignment item 1: exit 2). 116 of 117 cases as the probe expects. |
| R446-1 F2: claimed refusals without arm | MINOR Tests | Arms: design, design state, all 8 `FLOW` commands (fixture gains `phys_opt_design` and `kl_timing_grade_configure` lines), standalone RAMB36 and DSP, WNS at a floor (policy edit 0.3), WHS at its floor, WNS fall of exactly 0.25, BRAM tiles at the ceiling. Shipped mutants for each. | `probes/r446-probe-gate-mutants.log`: 23/23 KILLED, control passes, 0 not applied. |
| R446-1 F3: partitions mixed | MINOR Docs | One partition in both pages: own logic of every instance the gate record lists (wrapper and three levels) outside `u_nvm_port`, 51 terms. Net +79 LUT / +93 FF; absolute 391 LUT / 121 FF. Processor top's own logic stated as one term: -23 LUT / +107 FF = `armq_r` 1,153 -> 1,260 flops (counted by name in each `baseline_cells.tsv`). | `probes/r446-reconcile.log` (unchanged script): 2 BAD, both the hard-coded round-1 sentences; the second asserts FF +95 on a partition whose records give -12, so it fails for any prose. `probes/r446-reconcile-adapted.log`: 0 mismatches; `probes/reconcile-r2.diff` is the whole change (those two checks re-pointed at the round-2 sentences, figures recomputed from the records). |
| R446-1 R1, R2 | RESIDUE Docs | Same three `AREA_BUDGET.md` lines as R447-1 RESIDUE 1, different words; R447-1's per-line wording used, which carries all of R446-1's content (ceiling accepted; bank runs for RTL, pin or recipe changes; local half of criterion 4). | `docs/design/AREA_BUDGET.md` headroom table, "Where the gate runs". |
| R446-1 R3 | RESIDUE Docs | Lever 2 "#230 (joins its scope)", levers 3 and 6 "#639"; lever 5 stays #232. | Findings ranking table. |
| R446-1 R4 | RESIDUE Docs | PR body decisions 1-5 rewritten from the rulings and the owner decision. | `PR-BODY.md`. |
| R446-1 S1-S5 | SUGGESTION | All taken (items 2, 5, 6, the index, and the header/`located()`/count-format arms). S3: growth-only confirmed, as the assignment states. | Self-test, mutants. |
| R447-1 MINOR 1: tracebacks | MINOR Robustness, Tests | `load()` refuses a missing, non-JSON or endpoint-less baseline; `check` validates its endpoint with `entry_problems()` (no record, incomplete record, missing tolerance or floor, ceiling naming no figure, record outside its own limits, malformed policy); `inputs()` refuses a wrong-shape image manifest; `record()` also maps `IndexError`/`TypeError` to exit 2. One `except Refusal` in `main()` prints `NOT COMPARABLE: <reason>` and returns 2. 13 `check` and 20 `check-baseline` arms through `main()`. | `probes/r447-probe-cli.log`: 54 of 54 as documented (the 6 BAD of round 1 now exit 2). |
| R447-1 MINOR 2: disabled checks survive | MINOR Tests | Arms and mutants for (a)-(d) and the three boundaries. | `probes/r447-extra-mutants.log`: 18/18 KILLED, control passes. |
| R447-1 MINOR 3: route completion | MINOR Robustness | `routing()` reads the one `*_route_status.rpt`: routing errors, an `unrouted` row or routable != fully routed -> exit 1 (`ROUTE INCOMPLETE ... the image does not fit`); none, two, an unreadable count, no `nets with routing errors` row, or routable without fully routed -> exit 2. 9 route arms, 2 CLI arms. A's real status recorded as clean. | `probes/r447-probe-route-status.log`: clean 0, 37 unrouted 1. `gate-check-A-route.log`: "route status: complete" (A: 105,566 of 105,566 routable nets fully routed, 0 with routing errors; report sha256 `cd999ac5...` as in `receipts/run-receipts.json`). |
| R447-1 MINOR 4: partitions mixed | MINOR Docs | As F3. | `probes/r447-partition-check.log` (unchanged): its complete-partition line "+79, abs 391, +93" and "u_pp own logic: LUT -23, FF +107" equal the prose; `probes/r447-partition-vs-prose.log` compares them mechanically: 0 mismatches (its last line is the script's hard-coded round-1 text). |
| R447-1 RESIDUE 1 | RESIDUE Docs | Taken exactly (:114, :182, :185). | `AREA_BUDGET.md`. |
| R447-1 RESIDUE 2 | RESIDUE Docs | Taken exactly for items 2, 3 and the limitations bullet; item 1 states the owner decision (which postdates the prescribed "needs the owner's ruling"). | `PR-BODY.md`. |
| R447-1 suggestions 1, 2 | SUGGESTION | Taken (items 5, 4). | As above. |

Assignment item 8 also: the owner decision cited in `AREA_BUDGET.md` (link to 5967924270; NFR-RES-01 stays at 60 %,
redesign in milestone "Optimisations Mark II" #640 after Instrument verification; levers keep their order); a
one-line pointer from the findings page; both findings pages indexed in `docs/findings/README.md`.

### R2.2 Gate changes

- Exit contract: 0 within tolerance; 1 material regression (growth, ceiling, floor, fall, incomplete route); 2 not
  comparable, unreadable measurement or unusable baseline, each printed as `NOT COMPARABLE: <reason>`.
- `check-baseline`: per-endpoint `entry_problems()` plus `policy_table()` read from `docs/design/AREA_BUDGET.md`
  (`--budget` overrides). The table there was re-laid as one value per cell (Endpoint, LUT, FF, Slice, RAMB36, RAMB18,
  DSP, WNS floor, WHS floor, Timing fall, BRAM tile ceiling); every value is unchanged. Each JSON policy value must
  equal its cell; an endpoint or a row on one side only, a missing or second table, a repeated row or a non-value cell
  is a problem. The route's BRAM tile ceiling is required. Real data: `baseline PASS: 3 endpoints`.
- Because the gate now names `docs/design/AREA_BUDGET.md`, `scripts/ci_scope.py --selftest` refused until the page
  joined `GATE_READ_DOCS` (plus a classification case); `docs/testing/CI_WORKFLOWS.md` now counts five gate-read pages.
- Improvements: a gated figure that improves by more than its tolerance prints `re-baseline recommended: <figures>`;
  exit unchanged. `judge()` keeps a two-argument form (route status `None` = not read) so R447's `replay_records.py`
  still runs.
- Self-test: 113 arms (68 route, 8 standalone, 1 relocation, 13 `check` and 20 `check-baseline` through `main()`,
  CARRY4 and `record --write`, cross-kind). An escaped exception fails its arm by name instead of crashing.
- Mutants: 84 (25 from round 1, one re-targeted to the new `elif`), control passes; R446's
  `probe_pr_mutant_reasons.py` classifies 84/84 as killed by an arm assertion, 0 by a crash
  (`probes/r446-probe-pr-mutant-reasons.log`).

### R2.3 Real data through the gate (no Vivado; existing run directories)

| Receipt (`receipts/round2/`) | Directory | Endpoint | rc | Result |
|---|---|---|---:|---|
| `gate-check-A-route.log` | `A/work/ax7101/gateware` | `route-1x1` | 0 | PASS; route status complete |
| `gate-check-A-ooc-1x1.log` | `A/work/ax7101-ooc` | `ooc-1x1` | 0 | PASS |
| `gate-check-A-ooc-8x8.log` | `A/work/ax8x8-ooc` | `ooc-8x8` | 0 | PASS |
| `gate-check-B-route.log` | `B/work/ax7101/gateware` | `route-1x1` | 1 | LUT +625 > 500; route status complete (105,559 of 105,559) |
| `gate-check-B-ooc-1x1.log` | `B/work/ax7101-ooc` | `ooc-1x1` | 0 | PASS (+162 / +126) |
| `gate-check-B-ooc-8x8.log` | `B/work/ax8x8-ooc` | `ooc-8x8` | 0 | PASS (-172 / -85) |
| `gate-check-A-ooc-1x1-10ns.log` | `A/work/ax7101-ooc10` | `ooc-1x1` | 2 | standalone clock identity |

Other probes rerun unchanged: `probes/r447-check-tables.log` 49 groups, 0 mismatches; `probes/r447-replay-records.log`
A 0/0/0, B 1/0/0, 10 ns 2. Probe runner: `scratch-scripts/run_probes_r2.sh`; adapted scripts:
`receipts/round2/probes/reconcile-r2.diff`, `receipts/round2/probes/partition_vs_prose.py`.

### R2.4 Gate table

Head `0feff20fa228d0cb91d507943e6d39495b28b880`, worktree clean: True; `GNU Make 4.3` first on `PATH`. `$MDPY` = `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`.
Each command ran in the foreground from the lane root (physical `/data` path), without a pipeline;
`docs-check-no-git` and `feature-status-no-git` set `GIT_DIR=/dev/null`. Machine record:
`receipts/round2/gate-results.json`; runner `scratch-scripts/run_gates_r2.py`.

| # | Gate | Command | rc | Seconds | Receipt |
|---:|---|---|---:|---:|---|
| 1 | dp-srcs-selftest | `python3 syn/ooc/dp_srcs.py --selftest` | 0 | 16.4 | [receipts/round2/dp-srcs-selftest.log](receipts/round2/dp-srcs-selftest.log) |
| 2 | ooc-tcl-selftest | `python3 syn/ooc/ooc_tcl_selftest.py` | 0 | 422.5 | [receipts/round2/ooc-tcl-selftest.log](receipts/round2/ooc-tcl-selftest.log) |
| 3 | pp-baseline-selftest | `python3 syn/ooc/pp_baseline.py --selftest` | 0 | 0.1 | [receipts/round2/pp-baseline-selftest.log](receipts/round2/pp-baseline-selftest.log) |
| 4 | pp-baseline-mutants | `python3 syn/ooc/pp_baseline_mutants.py` | 0 | 2.7 | [receipts/round2/pp-baseline-mutants.log](receipts/round2/pp-baseline-mutants.log) |
| 5 | pp-baseline-reports-selftest | `python3 syn/ooc/pp_baseline_reports_selftest.py` | 0 | 0.0 | [receipts/round2/pp-baseline-reports-selftest.log](receipts/round2/pp-baseline-reports-selftest.log) |
| 6 | resource-gate-selftest | `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | 0.3 | [receipts/round2/resource-gate-selftest.log](receipts/round2/resource-gate-selftest.log) |
| 7 | resource-gate-mutants | `python3 syn/ooc/pp_resource_gate_mutants.py` | 0 | 15.4 | [receipts/round2/resource-gate-mutants.log](receipts/round2/resource-gate-mutants.log) |
| 8 | resource-gate-check-baseline | `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | 0.1 | [receipts/round2/resource-gate-check-baseline.log](receipts/round2/resource-gate-check-baseline.log) |
| 9 | dp-srcs-milan-datapath | `python3 syn/ooc/dp_srcs.py --top milan_datapath` | 0 | 8.4 | [receipts/round2/dp-srcs-milan-datapath.log](receipts/round2/dp-srcs-milan-datapath.log) |
| 10 | dp-srcs-kl-pp-shadow | `python3 syn/ooc/dp_srcs.py --top KL_pp_shadow` | 0 | 4.9 | [receipts/round2/dp-srcs-kl-pp-shadow.log](receipts/round2/dp-srcs-kl-pp-shadow.log) |
| 11 | pp-srcs-check-selftest | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.2 | [receipts/round2/pp-srcs-check-selftest.log](receipts/round2/pp-srcs-check-selftest.log) |
| 12 | docs-check | `$MDPY scripts/docs_check.py` | 0 | 4.9 | [receipts/round2/docs-check.log](receipts/round2/docs-check.log) |
| 13 | docs-check-no-git | `$MDPY scripts/docs_check.py` | 0 | 4.9 | [receipts/round2/docs-check-no-git.log](receipts/round2/docs-check-no-git.log) |
| 14 | feature-status-no-git | `$MDPY scripts/check_feature_status.py` | 0 | 0.8 | [receipts/round2/feature-status-no-git.log](receipts/round2/feature-status-no-git.log) |
| 15 | feature-status-selftest | `$MDPY scripts/check_feature_status.py --self-test` | 0 | 0.8 | [receipts/round2/feature-status-selftest.log](receipts/round2/feature-status-selftest.log) |
| 16 | em-dash | `$MDPY scripts/check_em_dash.py --base 1269cdafb4bb964c757baae0f0c5a932d43f540b` | 0 | 3.0 | [receipts/round2/em-dash.log](receipts/round2/em-dash.log) |
| 17 | em-dash-selftest | `$MDPY scripts/check_em_dash.py --selftest` | 0 | 3.2 | [receipts/round2/em-dash-selftest.log](receipts/round2/em-dash-selftest.log) |
| 18 | doc-style | `$MDPY scripts/check_doc_style.py` | 0 | 0.1 | [receipts/round2/doc-style.log](receipts/round2/doc-style.log) |
| 19 | doc-style-selftest | `$MDPY scripts/check_doc_style.py --selftest` | 0 | 0.0 | [receipts/round2/doc-style-selftest.log](receipts/round2/doc-style-selftest.log) |
| 20 | doc-paths | `$MDPY scripts/check_doc_paths.py` | 0 | 0.1 | [receipts/round2/doc-paths.log](receipts/round2/doc-paths.log) |
| 21 | toc-selftest | `$MDPY scripts/gen_toc.py --selftest` | 0 | 0.9 | [receipts/round2/toc-selftest.log](receipts/round2/toc-selftest.log) |
| 22 | toc-verify-anchors | `$MDPY scripts/gen_toc.py --verify-anchors` | 0 | 2.7 | [receipts/round2/toc-verify-anchors.log](receipts/round2/toc-verify-anchors.log) |
| 23 | toc-check | `$MDPY scripts/gen_toc.py --check` | 0 | 4.2 | [receipts/round2/toc-check.log](receipts/round2/toc-check.log) |
| 24 | archive | `$MDPY scripts/check_archive.py` | 0 | 0.4 | [receipts/round2/archive.log](receipts/round2/archive.log) |
| 25 | archive-selftest | `$MDPY scripts/check_archive.py --selftest` | 0 | 0.1 | [receipts/round2/archive-selftest.log](receipts/round2/archive-selftest.log) |
| 26 | doc-map-check | `$MDPY docs/DOC_MAP.gen.py --check` | 0 | 0.4 | [receipts/round2/doc-map-check.log](receipts/round2/doc-map-check.log) |
| 27 | module-matrix-check | `$MDPY docs/traceability/gen_module_matrix.py --check` | 0 | 1.1 | [receipts/round2/module-matrix-check.log](receipts/round2/module-matrix-check.log) |
| 28 | solution-docs | `$MDPY scripts/check_solution_docs.py` | 0 | 0.1 | [receipts/round2/solution-docs.log](receipts/round2/solution-docs.log) |
| 29 | baremetal-only | `python3 scripts/check_baremetal_only.py --check` | 0 | 17.1 | [receipts/round2/baremetal-only.log](receipts/round2/baremetal-only.log) |
| 30 | gptp-docs-make | `make -C gptp-processor docs` (GNU Make 4.3) | 0 | 0.7 | [receipts/round2/gptp-docs-make.log](receipts/round2/gptp-docs-make.log) |
| 31 | ci-scope-selftest | `python3 scripts/ci_scope.py --selftest` | 0 | 4.1 | [receipts/round2/ci-scope-selftest.log](receipts/round2/ci-scope-selftest.log) |
| 32 | ci-events-check | `python3 scripts/ci_events.py --check` | 0 | 0.2 | [receipts/round2/ci-events-check.log](receipts/round2/ci-events-check.log) |
| 33 | ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | 15.5 | [receipts/round2/ci-events-selftest.log](receipts/round2/ci-events-selftest.log) |
| 34 | py-idiom | `python3 scripts/check_py_idiom.py` | 0 | 3.9 | [receipts/round2/py-idiom.log](receipts/round2/py-idiom.log) |
| 35 | py-idiom-selftest | `python3 scripts/check_py_idiom.py --selftest` | 0 | 3.8 | [receipts/round2/py-idiom-selftest.log](receipts/round2/py-idiom-selftest.log) |
| 36 | fail-fast | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.5 | [receipts/round2/fail-fast.log](receipts/round2/fail-fast.log) |
| 37 | hygiene | `python3 scripts/check_hygiene.py --check` | 0 | 0.4 | [receipts/round2/hygiene.log](receipts/round2/hygiene.log) |
| 38 | todo-ownership | `python3 scripts/check_todo_ownership.py` | 0 | 1.6 | [receipts/round2/todo-ownership.log](receipts/round2/todo-ownership.log) |
| 39 | test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | 6.6 | [receipts/round2/test-evidence.log](receipts/round2/test-evidence.log) |
| 40 | control-flow-selftest | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.1 | [receipts/round2/control-flow-selftest.log](receipts/round2/control-flow-selftest.log) |
| 41 | cohesion-selftest | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.1 | [receipts/round2/cohesion-selftest.log](receipts/round2/cohesion-selftest.log) |
| 42 | diff-check-base | `git diff --check 1269cdafb4bb964c757baae0f0c5a932d43f540b HEAD` | 0 | 0.0 | [receipts/round2/diff-check-base.log](receipts/round2/diff-check-base.log) |
| 43 | diff-check-worktree | `git diff --check` | 0 | 0.0 | [receipts/round2/diff-check-worktree.log](receipts/round2/diff-check-worktree.log) |

43 gates, 0 non-zero. Not run, as in round 1 (nothing they execute changed):
`scripts/run_all_suites.sh`, `syn/yosys/run.sh`, `scripts/lint_rtl.py`, `scripts/xvlog_gate.py`, the Yosys
self-tests and the builder bank; and `scripts/act_ci.py --selftest` (see R2.5).

### R2.5 Notes and deviations

- `scripts/act_ci.py --selftest` is dropped from the table: AGENTS.md section 5 allows the candidate's copy to run its
  self-test only inside the disposable CI job boundary. Round 1's table (row 34) ran it on the host, which that rule
  does not permit; round 2 does not. This PR does not change `scripts/act_ci.py`.
- R446's unchanged `reconcile.py` cannot report 0 against any prose (see F3); the adapted copy is published with its diff.
- R446-1 R1/R2 and R447-1 RESIDUE 1 prescribe different words for the same lines; R447-1's were used.
- R447-1 RESIDUE 2 item 1 prescribes "needs the owner's ruling", which the owner decision 5967924270 superseded.
- Gate-table runs: the first stopped at a 590 s guard (`ooc-tcl-selftest` alone takes about 410 s), the second was
  stopped to drop the act-ci self-test, the third for the `0feff20f` wording commit; the fourth ran to completion at
  `0feff20f` in the background with its own log and rc file. Stopping `ooc-tcl-selftest` left one ignored
  `syn/ooc/.ooc-mut-*.tcl` copy, and manual runs left two ignored `__pycache__` directories; all three were removed and
  `git status --porcelain --ignored` is empty at exit.
- No STOP condition met: no RTL, no new hosted runner or tool, no tolerance or ceiling value changed (the budget table
  only moved to one value per cell; `check-baseline` confirms every value equals the JSON).
- No push, PR edit, merge, rebase, sub-agent, other checkout, hardware, flashing, processor or interface change. No
  existing comment edited. The scratch tree and the run directories stay under `$VALIDATION_STORAGE/234-a516`.

## Round 3

Status: REVIEW READY at `b5894838d6c47180ac4169e7d52dd746f461af21` on `234-area-baseline` (not pushed; the manager
pushes), on top of `0feff20fa228d0cb91d507943e6d39495b28b880` (no rebase, no amend).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5968718943
- REVIEW READY (round 3): https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5969184448
- Answers R446-2 (PR #638 comment 5968664092) and R447-2 (5968715741).
- Reviewer packets read from `origin/234-review-evidence` at `baa3747b4265f4d87220ce45e2d41ddf03c43cc7`, exported with
  `git archive` to `$VALIDATION_STORAGE/234-a516/r3/review-evidence`, not checked out.
- No Vivado run in round 3 (the assignment forbids it): every real-data check reads the existing run directories.

Same branch, same checkout, four new one-line commits on `0feff20f` (no rebase, no amend, no trailers):

| Commit | Subject |
|---|---|
| `d54f61802` | Validate the whole resource baseline before check or check-baseline reads it, read every report count as ASCII digits and require one row of each route status count, with arms and killed mutants |
| `b38bb06d3` | State the resource gate's total exit-code contract and the stale route status report risk, and say the processor top's 107 FFs are its timer-arm queues |
| `2b98e4859` | Scope the budget page's exit-code sentence to check, which exits 2 for every input it cannot judge |
| `b5894838d` | Add a shipped mutant for the timed-endpoint count boundary, whose reviewer mutant no longer applies after the ASCII count change |

Diff `0feff20f..b5894838`: 6 files (`syn/ooc/pp_resource_gate.py`, `_selftest.py`, `_mutants.py`,
`syn/ooc/pp_baseline_rank.py`, `docs/design/AREA_BUDGET.md`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`). Diff
`1269cdaf..b5894838`: 15 files (round 2's 14 plus `syn/ooc/pp_baseline_rank.py`). No RTL, processor, interface,
workflow, pin list, baseline JSON, tolerance, floor or ceiling change.

### R3.1 Finding-by-finding

Receipts under `receipts/round3/`; every probe is the reviewer's published script, unchanged.

| Finding | Severity, lens | Answer | Evidence at `b5894838` |
|---|---|---|---|
| R446-2 F1: a route status report without its routable-net rows reads complete | MINOR Conformance, Robustness, Tests | `routing()` requires exactly one `routable nets` and one `fully routed nets` row (`pp_resource_gate.py:277-279`) beside the one `nets with routing errors` row (`:280-281`); anything else exits 2 naming the label and how many rows it has. Arms: without its routable row, without its fully routed row, without both rows, with a second routable row. Shipped mutants `routable and routed rows present` (`!= 1` to `> 1`), `routable and routed rows single` (`< 1`) and `fully routed row required` killed. | `probes/r446-2-probe-route-status-A.log`: both CONTRACT cases (rows removed, rows relabelled) rc 2; 15 of 16 as the probe expects, the 16th is S1 (declined below). `probes/r447-2-probe-route-real-A.log`: "both routable rows missing" rc 2. |
| R446-2 F2: the policy pin is proven only for tolerance cells; the endpoint-column guard has no arm | MINOR Tests | The fixture's WNS floor is now 0.03, as the real route's, so a floor read as zero differs. Arms: a budget floor the baseline does not hold, a budget ceiling the baseline does not hold, a baseline policy figure the budget table lacks, a timing summary without its endpoint columns. Shipped mutants `budget comparison of every policy field`, `budget comparison of baseline-only figures`, `budget floors read` and `timed endpoint columns` killed. | `probes/r446-2-probe-extra-mutants.log`: all four named mutants KILLED, control passes (181 arms). |
| R446-2 F3 and R447-2 MINOR 1: malformed record fields exit 1 by traceback or pass `check-baseline` | MINOR Conformance, Robustness, Tests, Docs | One validator, `load()` (`:421-434`), run by `check` and `check-baseline` before any field is used. Strict JSON: `NaN`, `Infinity` and a decimal that reads as infinity are refused (`constant()`, `finite()`). `shape_problems()` (`:380-418`) per endpoint: a record with every field; a known kind; an identity with exactly the recorded keys and types (flow and clock lists of text); a 64-digit hex input digest; exactly the kind's recorded figures, each a number and not a bool; scopes holding exactly `LUT FF RAMB36 RAMB18 DSP CARRY4` as non-negative integers; every tolerance, floor and ceiling a table of numbers; no unknown field in the file or an endpoint. Any deviation: exit 2, `NOT COMPARABLE: baseline <path> is malformed: <endpoint>: <reason>`. `entry_problems()` and `judge()` run only on a baseline `load()` accepted. 25 malformed-baseline arms, each driven through `main()` by both commands (50 arms). Shipped mutants, one per check, all killed: `baseline NaN and Infinity`, `baseline overflowing numbers`, `finite baseline numbers`, `baseline nested too deep`, `baseline file fields`, `baseline shape validated`, `baseline record presence`, `baseline record completeness`, `baseline record kind`, `baseline endpoint fields`, `baseline identity keys`, `baseline identity types`, `baseline identity text`, `baseline input digest`, `baseline figure names`, `baseline figure numbers`, `numbers are not bools`, `baseline scope shape`, `baseline scope whole numbers`, `baseline scope non-negative`, `baseline policy tables`, `baseline policy numbers`. | `probes/r446-2-probe-malformed-record.log`: 0 of 8 cases not exit 2, no traceback, both commands. `probes/r447-2-probe-contract.log`: all 13 edited cases rc 2 in both columns, no traceback; the control keeps check rc 1 (MATERIAL REGRESSION) and check-baseline rc 0. |
| R447-2 MINOR 2: the route status reader accepts absent net rows, and a superscript count escapes as a traceback | MINOR Conformance, Robustness, Tests | As F1, and the class closed in every parser: each report count is read through `[0-9]+` (route status `:274`, timed endpoints `:140`, utilization `:118`, hierarchy rows `pp_baseline_rank.py:30`), never `str.isdigit()` or `\d`; the slack through `-?[0-9]+\.[0-9]+` (`:137`); budget cells through `[0-9]` (`:476`). Arms: route status count a superscript, route status count in other digits, utilization count in other digits, WNS in other digits, timed endpoints in other digits, hierarchy count in other digits, a hierarchy row without counts. Shipped mutants, all killed: `count format`, `count format ASCII`, `ASCII counts`, `timed endpoint count format`, `timed endpoint boundary`, `finite slack`, `finite WHS`, `ASCII slack`, `route status counts`, `route status count format`, `budget cells ASCII`, and in the hierarchy parser `hierarchy counts`, `hierarchy ASCII counts` and `hierarchy header only`. | `probes/r447-2-probe-route-real-A.log` 15 of 15: superscript rc 2, both rows missing rc 2. `probes/r447-2-probe-route-real-B.log` 14 of 15: the 15th is B's own +625 LUT (rc 1, wanted 0), as in R447-2's receipt. |
| R447-2 SUGGESTION: the route status report is not bound to the run | SUGGESTION Robustness | Assignment item 5: a recipe note; no binding added. | `PP_SHADOW_BASELINE_RECIPE.md:459-460`. |
| R446-2 R1 | RESIDUE Docs | Taken exactly. | `AREA_BUDGET.md:170`. |
| R446-2 S1: the wholly unrouted layout | SUGGESTION | Not taken (assignment): exit 2 fails closed. | `probes/r446-2-probe-route-status-A.log`: BAD want 1 got 2, "0 'fully routed nets' rows". |
| R446-2 S2: stale route status report | SUGGESTION | Recipe note (assignment item 5): the report has no header and is read from the run directory, so each measurement uses a fresh directory; the bank deletes nothing. | `PP_SHADOW_BASELINE_RECIPE.md:459-460`. |
| R446-2 S3: B's `armq_r` census | SUGGESTION | Published: `evidence/round3/armq-census.tsv` (script `scratch-scripts/armq_census.py`). | `armq_r` flip-flops at 1x1: A 1,153, B 1,260 (+107); each census file's sha256 equals `receipts/run-receipts.json`. 8x8 and route rows and the `armq_cnt_r` counters are in the same file. |

Assignment item 5 also: the exit-code contract as it now holds is stated in `AREA_BUDGET.md:189-196`, the recipe
(`:456-469`) and the PR body. The recipe's ranking step says the hierarchy parser refuses a non-count row (`:242`).

### R3.2 Gate changes

- Exit contract of `check`: 0 within tolerance; 1 a material regression only (growth, ceiling, floor, fall, incomplete
  route); 2 for every input it cannot judge, printed as `NOT COMPARABLE: <reason>`; no input reaches a traceback.
  `check-baseline`: 0 or 2.
- `load()` is the one validator (above). `check` then runs `entry_problems()` on its endpoint; `check-baseline` runs it
  on every endpoint and pins the policy to the budget table, both on validated data only.
- Parsers: ASCII counts and slack as above; `located()` takes a `KL_pp_shadow.sv` only with three parents
  (`:151`, so a path too near the root is refused by name rather than an `IndexError`); `record()` maps
  `RecursionError` from the image manifest to exit 2.
- `syn/ooc/pp_baseline_rank.py` `hierarchy()`: only the `Total LUTs` head row is skipped; every other ten-cell row must
  hold ASCII counts or is refused (`ValueError`, exit 2 through `record()`). On all seven real hierarchy reports (A and
  B route, 1x1, 8x8 and the 10 ns control) the new parser returns exactly what the old one did (compared in scratch).
- Self-test: 181 arms (82 route, 8 standalone, 1 relocation, 13 `check`, 24 `check-baseline`, 25 malformed baselines
  through both commands, `record --write` and CARRY4, cross-kind).
- Mutants: 122 (119 of the gate, 3 of the hierarchy parser), control passes. Against round 2: 2 removed with the code
  they mutated (`routable and routed rows`, `malformed policy`), 14 re-targeted to moved spans, 40 added (37 of the
  gate, 3 of the hierarchy parser). R447-2's
  `classify_mutants.py` (gate mutants only): 96 ARM, 23 ESCAPED, 0 CRASH, 0 survived; each ESCAPED removes a refusal,
  so the escaped exception is the defect its arm's exit-2 contract names.

### R3.3 Self-audit: every conversion and index of file content

Assignment item 4. Every `int()`, `float()`, subscript and `.get()` the gate applies to content read from a file:
the baseline JSON, the image manifest, the vendor reports, the recipe script, the cell census, the budget page, and
the hierarchy parser the gate imports (`syn/ooc/pp_baseline_rank.py`, `hierarchy()`; its `ranking()` is not called
by the gate). Line numbers are at `b5894838` (both files unchanged since `d54f6180`). "R3" marks a place this
round fixed; every other place already had the guard named. Every exception a guard does not pre-empt is named in the
last column and maps to exit 2 with a reason. File reads: every `read_text()` / `read_bytes()` of a measurement file
is inside `record()` (`:247-258`, `OSError`/`ValueError` incl. `UnicodeDecodeError`, `KeyError`, `IndexError`,
`TypeError`, `RecursionError` -> exit 2) or `routing()` (`:268-271`); the baseline read is in `load()` (`:423-426`);
the budget read is in `check_baseline()` (`:488-491`).

| # | Site | Data | Operation | Validation in front |
|---:|---|---|---|---|
| 1 | `pp_resource_gate.py:424` | baseline file | `json.loads` | R3: `parse_constant=constant` refuses `NaN`/`Infinity`/`-Infinity`; `parse_float=finite` refuses a decimal that reads as infinity; `OSError`, `ValueError`, `RecursionError` -> exit 2 (`:425-426`) |
| 2 | `:364` | baseline number text | `float(text)` | only text JSON's number grammar accepted reaches `parse_float`; `math.isfinite` after it (`:365`) |
| 3 | `:427`, `:431` | baseline top level | `.get("endpoints")`, `["endpoints"]` | `isinstance(baseline, dict)` short-circuits first; `:427-428` refuse a missing or non-object table |
| 4 | `:429` | baseline top-level keys | `set(baseline)` | R3: unknown keys refused (`:430`, `:432-433`) |
| 5 | `:382` | endpoint | `.get("record")` | `isinstance(entry, dict)` in the same expression |
| 6 | `:388` | record | `base["kind"]`, `["identity"]`, `["figures"]`, `["scopes"]` | R3: `isinstance(base, dict)` `:383`; every `RECORD` key present `:385-387` |
| 7 | `:392` | endpoint keys | `set(entry)` | entry is a dict (`:382-383`); R3: unknown keys refused `:393-394` |
| 8 | `:397` | identity | `identity[key]` | R3: `:395` requires a dict with exactly the `IDENTITY` keys (elif chain) |
| 9 | `:399` | identity flow, clock | iterate `identity[key]` | R3: `:397` requires both to be lists; items must be `str` |
| 10 | `:401` | input digest | `base["inputs_sha256"]`, `re.fullmatch` | R3: key present (`:385`); `isinstance(..., str)` before the match; 64 lower-case hex digits |
| 11 | `:403` | kind | `ROWS[kind]` | R3: `isinstance(kind, str) and kind in GATED` `:389`; `GATED` and `ROWS` have the same keys |
| 12 | `:404-407` | figures | `sorted(figures)`, `.values()` | R3: dict with exactly the kind's recorded figure set; every value a number, not a bool (finite by row 1) |
| 13 | `:408-412` | scopes | `.values()`, `sorted(counts)` | R3: dict of dicts with exactly `SCOPE` keys; every count `type(count) is int` and `>= 0` |
| 14 | `:414-416` | tolerance, floor, ceiling | `entry.get(field, {})`, `.values()` | R3: `isinstance(..., dict)` first; every value a number, not a bool (finite by row 1) |
| 15 | `:439` | validated endpoint | `entry["record"]["kind"]`, `["figures"]` | `load()` (rows 1-14) runs before `entry_problems()` in both commands (`:522`, `:531`, `:487`) |
| 16 | `:441`, `:448` | kind | `GATED[kind]`, `CEILINGS[kind]` | row 11 |
| 17 | `:442` | tolerance | `.get("tolerance", {}).get(figure, -1) >= 0` | row 14: a dict of numbers; absence reads -1 and is refused |
| 18 | `:446` | floor, figures | `figures[figure]`, `entry["floor"][figure]` | row 12: the timing figures are recorded; `:444` refuses an absent floor first (elif) |
| 19 | `:451-455` | ceiling, figures | `.get("ceiling", {})`, `figures[figure]` | row 14; `:452` refuses a ceiling naming no recorded figure first (elif) |
| 20 | `:296-304` | baseline record, candidate | `entry["record"]`, `base[...]`, `candidate[...]` | baseline: rows 1-15 and `entry_problems()` (`:531-533`); candidate: built by `record()` with every key (`:254-256`) |
| 21 | `:299-300` | identities | `base["identity"][key]`, `candidate["identity"].get(key)` | iterates the baseline's own keys; `.get` tolerates a missing candidate key (reads `None`, a change) |
| 22 | `:309-310` | figures | `GATED[base["kind"]]`, `base["figures"][figure]`, `candidate["figures"][figure]` | kinds equal (`:297`); both hold exactly the kind's figure set (row 12; `record()`) |
| 23 | `:315`, `:336`, `:338` | policy | `entry["tolerance"][figure]`, `entry["floor"][figure]` | `entry_problems()` in `main()` (`:531-533`) refuses a missing or negative tolerance and a missing floor |
| 24 | `:317-320` | ceiling | `entry.get("ceiling", {})`, `candidate["figures"][figure]` | row 19 (every ceiling names a recorded figure); candidate has the same figure set |
| 25 | `:353-354` | scopes | `.get(key, {})`, `.get("LUT", 0)`, `f"{lut:+d}"` | row 13 (integer counts, so `:+d` cannot raise); candidate counts are `int` from `hierarchy()` |
| 26 | `:102` | report header | `hits[0]` | `len(hits) != 1` refused `:100-101` |
| 27 | `:111` | utilization row | `cells[0]`, `cells[1]` | `len(cells) >= 2` `:110` |
| 28 | `:113-114` | utilization | `ROWS[kind]`, `seen.get(label, set())` | kind from `kind_of()` (exactly one recipe script, `:239-242`); `:115` refuses anything but one value |
| 29 | `:120` | utilization count | `float(value)` / `int(value)` | R3: `re.fullmatch(r"[0-9]+(\.5)?", value)` `:118` (was `\d`, which takes non-ASCII decimal digits) |
| 30 | `:129` | timing report | `blocks[1]` | `len(blocks) != 2` refused `:127` |
| 31 | `:133-134` | timing summary | `lines[heads]`, `lines[heads + 2]` | `heads is None or heads + 2 >= len(lines)` refused `:131` |
| 32 | `:135`, `:137-138` | timing columns | `names[0]`, `names[4]`, `values[0]`, `values[4]` | same condition: `len(names) != len(values) or len(names) < 5` is tested first |
| 33 | `:140` | timed endpoints | `int(value)` | R3: `COUNT.fullmatch(value)` (`[0-9]+`) in the same `and` (was `str.isdigit()`); `not paths` refuses absent columns |
| 34 | `:142` | slack | `float(values[0])`, `float(values[4])` | R3: `SLACK.fullmatch` (`-?[0-9]+\.[0-9]+`) `:137` (was `float()` then `isfinite`, which takes `1_0` and non-ASCII digits) |
| 35 | `:150` | recipe script paths | `path.parents[2]` | R3: `len(path.parents) > 2` in the same filter (was an `IndexError` caught by `record()`) |
| 36 | `:160` | located sources | `generated[0]`, `repository[0]` | `len(...) != 1` refused `:152-153` |
| 37 | `:171` | roots | `roots[0]` | the three-tuple `:160` builds; no file content indexes it |
| 38 | `:180` | image manifest | `json.loads` | `ValueError`, R3: `RecursionError` -> exit 2 (`:257`); values are only hashed, so `NaN` cannot reach a number |
| 39 | `:181-182` | manifest entries | `image.get("path")`, `image.get("sha256")` | `isinstance(images, list)`, `isinstance(image, dict)` short-circuit first |
| 40 | `:184-185` | manifest entries | `row["path"]`, `image['path']`, `image['sha256']` | `:181-183` refuse anything but a list of objects with string `path` and `sha256` |
| 41 | `:197` | tool header | `tool[1]` | `tool is None` refused `:192-193` |
| 42 | `:206` | cell census | `lines[0]` | `not lines` tested first in the same condition |
| 43 | `:212`, `:216`, `:233`, `:253` | CARRY4 counts | `carry[""]`, `carry.get(...)` | `carry` starts as `{"": 0}` (`:208`); file content only adds keys |
| 44 | `:223` | kind | `ROOTS[kind]` | row 28 |
| 45 | `:231` | hierarchy key | `key.split("/", 1)[1]` | `"/" in key` in the same expression |
| 46 | `:232` | hierarchy row | `counts[name]` | `hierarchy()` builds every row from `zip(FIELDS, ..., strict=True)` (rank `:42`), so all eight names exist |
| 47 | `:242` | recipe scripts | `kinds[0]` | `len(kinds) != 1` refused `:240-241` |
| 48 | `:248` | kind | `SCRIPTS[kind]` | row 28 |
| 49 | `:269` | route status reports | `reports[0]` | `len(reports) != 1` refused `:266-267` |
| 50 | `:276` | route status count | `int(value)` | R3: `COUNT.fullmatch(value)` `:274` (was `str.isdigit()`, so `²` reached `int()` as a traceback) |
| 51 | `:278-282` | route status rows | `counts.get(label, [])`, `sum(...)` | R3: exactly one `routable nets`, one `fully routed nets` (`:277-279`) and one `nets with routing errors` row (`:280-281`) |
| 52 | rank `:26-28` | hierarchy report | `split("|")[1:-1]`, `fields[2]` | slice cannot raise; `len(fields) != 10` tested first |
| 53 | rank `:30` | hierarchy row | `fields[2:]` | R3: every count cell must be `[0-9]+` or the row is refused (`ValueError` -> exit 2); only the `Total LUTs` head row is skipped (was: any row whose third cell failed `str.isdigit()` was skipped silently) |
| 54 | rank `:32`, `:34` | hierarchy row | `fields[0]` | row 52 |
| 55 | rank `:42` | hierarchy count | `int(value.strip())` | R3: row 53 |
| 56 | `:489` | budget page | `read_text()` | `OSError`, `ValueError` -> a named problem, exit 2 (`:490-491`) |
| 57 | `:467` | budget lines | `lines[starts[0] + 2:]` | `len(starts) != 1` refused `:464-465` |
| 58 | `:471-474` | budget row | `cells[0]`, `name[1]` | `split` yields at least one cell; `name is None` and the cell count refused `:472-473` |
| 59 | `:480` | budget cell | `float(value[1])` | R3: `re.fullmatch(r"([+-]?[0-9]+(?:\.[0-9]+)?)(?: ns)?", cell)` `:476` (was `\d`); a cell too long to be finite reads as infinity, which no strict-JSON baseline value equals, so the pin refuses it |
| 60 | `:486`, `:496-502` | baseline, table | `["endpoints"]`, `endpoints[name]`, `entry.get(field, {})`, `table[name][field]`, `.get(figure)` | `load()`; `:493-495` skip a name not on both sides; every table row holds all three fields (`:474`) |
| 61 | `:525-546` | baseline | `baseline["endpoints"]`, `.get(args.endpoint)`, `setdefault(...)["record"]`, `[args.endpoint]` | `load()`; `check` needs a known endpoint (`:527-529`, else argparse exits 2 with its usage) |

No place was found without a guard after the R3 fixes. The one exit not covered by the contract is an environment
failure in `record --write` (`:544`, writing the baseline file): it is not input and is not caught.

### R3.4 Every reviewer probe of rounds 1 and 2, unchanged

Runner `scratch-scripts/run_probes_r3.sh` (exported packet `baa3747b`, scratch outside the checkout,
`PYTHONDONTWRITEBYTECODE=1`); one log and rc per probe under `receipts/round3/probes/`; `git status --porcelain
--ignored` empty afterwards. `R446-2/r1-probes/` and `R447-2/r1probes/` are byte-identical to the round-1 scripts
(`cmp`), so the round-1 rows are their results too.

| Reviewer | Probe | rc | Result at `b5894838` | Reading |
|---|---|---:|---|---|
| R446-1 | `probe_gate_cli.py` | 1 | 117 cases, 1 not as expected | That one is `inf` slack with 0 endpoints: rc 2 against the probe's literal want of 1; R446-1 F1 allowed 2 and the round-2 assignment required it, as in round 2. |
| R446-1 | `probe_gate_mutants.py` | 0 | 21 killed, 0 survived, control passes, 2 not applied | Not applied because round 3 rewrote the line: `count format accepts any decimal` (the pattern is now `[0-9]`; shipped `count format decimals` covers it) and `check_baseline: recorded figure below floor` (re-indented when the policy checks lost their `try`; shipped `baseline floor value` covers it). Both shipped mutants are killed. |
| R446-1 | `probe_pr_mutant_reasons.py` | 0 | 119 of 119 ARM | Every shipped gate mutant is killed by an arm assertion. |
| R446-1 | `reconcile.py` | 1 | 2 mismatches | Both are its hard-coded round-1 sentences, as in round 2; R446-2's `partition_rederive.py` re-derives the round-2 partition (0 mismatches). |
| R447-1 | `probe_cli.py` | 0 | 54 of 54 as documented | |
| R447-1 | `extra_mutants.py` | 0 | 17 killed, 0 survived, 1 not unique | `baseline floor value`: the same re-indented line; the shipped mutant of that name is killed. |
| R447-1 | `probe_route_status.py` | 0 | clean report exit 2; 37 unrouted nets exit 2 | Its invented report has no `routable nets` or `fully routed nets` row, which item 2 now refuses with 2 (round 2: 0 and 1). |
| R447-1 | `partition_check.py` | 0 | complete partition +79 LUT / 391 / +93 FF; `u_pp` own logic -23 / +107 | Equal to the prose; its last line is its fixed round-1 text. |
| R447-1 | `replay_records.py` | 0 | A 0, 0, 0; B 1, 0, 0; 10 ns control 2 | |
| R447-1 | `check_tables.py` | 0 | 49 groups, 0 mismatches | |
| R446-2 | `partition_rederive.py` | 0 | 0 mismatches over 10 sentences | R1's rewording keeps "-23 LUTs and +107 FFs". |
| R446-2 | `probe_extra_mutants.py --jobs 12` | 0 | control passes; F2's four KILLED; 8 KILLED, 2 not applicable, 1 note | Not applicable: `timed endpoints at zero accepted` (its span held `isdigit()`; shipped `timed endpoint boundary` added and killed) and `check skips the ceiling list` (re-indented; shipped `baseline route ceiling` killed). |
| R446-2 | `probe_malformed_record.py` | 0 | 0 of 8 cases not exit 2; 16 runs, no traceback | |
| R446-2 | `probe_policy_pin.py` | 0 | 105 of 105 | |
| R446-2 | `probe_route_status.py` (A) | 1 | 15 of 16 | Both CONTRACT cases rc 2. The 16th is S1, the wholly unrouted layout: want 1, got 2, declined by the assignment. |
| R447-2 | `classify_mutants.py` | 0 | 96 ARM, 23 ESCAPED, 0 CRASH, 0 survived, of 119 | Each ESCAPED mutant removes a refusal, so its escaped exception is the defect the arm's exit-2 contract names. |
| R447-2 | `partition_r2.py` | 0 | 51 terms; +79 / 391 LUT; +93 / 121 FF; `u_pp` -23 / +107 | |
| R447-2 | `probe_contract.py` (A) | 0 | 13 edited cases rc 2 in both columns, no traceback | Control: `check` rc 1 (MATERIAL REGRESSION), `check-baseline` rc 0. |
| R447-2 | `probe_policy.py` | 0 | 107 of 107 | |
| R447-2 | `probe_route_real.py` (A) | 0 | 15 of 15 | Superscript count rc 2; both net rows missing rc 2. |
| R447-2 | `probe_route_real.py` (B) | 0 | 14 of 15 | The 15th is B's real report: rc 1 for B's +625 LUT, wanted 0, as in R447-2's own receipt. |
| R447-2 | `real_data.sh` | 0 | A 0, 0, 0; 10 ns 2; B 1, 0, 0 | |
| R447-2 | `run_gates.sh` | 0 | 31 of 31 jobs rc 0 (`receipts/round3/r447-2-run-gates/`) | Make 4.3 first on `PATH`. R447-1's `run_gates.sh` is the same list less four jobs. |

### R3.5 Real data through the gate (no Vivado; existing run directories)

| Receipt (`receipts/round3/`) | Directory | Endpoint | rc | Result |
|---|---|---|---:|---|
| `real/gate-check-A-route.log` | `A/work/ax7101/gateware` | `route-1x1` | 0 | PASS; route status complete |
| `real/gate-check-A-ooc-1x1.log` | `A/work/ax7101-ooc` | `ooc-1x1` | 0 | PASS |
| `real/gate-check-A-ooc-8x8.log` | `A/work/ax8x8-ooc` | `ooc-8x8` | 0 | PASS |
| `real/gate-check-B-route.log` | `B/work/ax7101/gateware` | `route-1x1` | 1 | LUT +625 > 500; route status complete |
| `real/gate-check-B-ooc-1x1.log` | `B/work/ax7101-ooc` | `ooc-1x1` | 0 | PASS (+162 LUT) |
| `real/gate-check-B-ooc-8x8.log` | `B/work/ax8x8-ooc` | `ooc-8x8` | 0 | PASS (-172 LUT) |
| `real/gate-check-A-ooc-1x1-10ns.log` | `A/work/ax7101-ooc10` | `ooc-1x1` | 2 | standalone clock identity |

The committed baseline passes the new validator unchanged (`check-baseline`: "baseline PASS: 3 endpoints").

### R3.6 Gate table

Head `b5894838d6c47180ac4169e7d52dd746f461af21`, worktree clean: True; `GNU Make 4.3` first on `PATH`. `$MDPY` =
`$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`. Each command ran in the foreground of the runner from the lane
root (physical `/data` path), without a pipeline; `docs-check-no-git` and `feature-status-no-git` set
`GIT_DIR=/dev/null`. Machine record: `receipts/round3/gates/gate-results.json`; runner `scratch-scripts/run_gates_r3.py`,
driven by `scratch-scripts/run_all_r3.sh` in the background with its own log and rc file.

| # | Gate | Command | rc | Seconds | Receipt |
|---:|---|---|---:|---:|---|
| 1 | dp-srcs-selftest | `python3 syn/ooc/dp_srcs.py --selftest` | 0 | 14.2 | [receipts/round3/gates/dp-srcs-selftest.log](receipts/round3/gates/dp-srcs-selftest.log) |
| 2 | ooc-tcl-selftest | `python3 syn/ooc/ooc_tcl_selftest.py` | 0 | 431.0 | [receipts/round3/gates/ooc-tcl-selftest.log](receipts/round3/gates/ooc-tcl-selftest.log) |
| 3 | pp-baseline-selftest | `python3 syn/ooc/pp_baseline.py --selftest` | 0 | 0.1 | [receipts/round3/gates/pp-baseline-selftest.log](receipts/round3/gates/pp-baseline-selftest.log) |
| 4 | pp-baseline-mutants | `python3 syn/ooc/pp_baseline_mutants.py` | 0 | 2.5 | [receipts/round3/gates/pp-baseline-mutants.log](receipts/round3/gates/pp-baseline-mutants.log) |
| 5 | pp-baseline-reports-selftest | `python3 syn/ooc/pp_baseline_reports_selftest.py` | 0 | 0.0 | [receipts/round3/gates/pp-baseline-reports-selftest.log](receipts/round3/gates/pp-baseline-reports-selftest.log) |
| 6 | resource-gate-selftest | `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | 0.4 | [receipts/round3/gates/resource-gate-selftest.log](receipts/round3/gates/resource-gate-selftest.log) |
| 7 | resource-gate-mutants | `python3 syn/ooc/pp_resource_gate_mutants.py` | 0 | 27.8 | [receipts/round3/gates/resource-gate-mutants.log](receipts/round3/gates/resource-gate-mutants.log) |
| 8 | resource-gate-check-baseline | `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | 0.1 | [receipts/round3/gates/resource-gate-check-baseline.log](receipts/round3/gates/resource-gate-check-baseline.log) |
| 9 | dp-srcs-milan-datapath | `python3 syn/ooc/dp_srcs.py --top milan_datapath` | 0 | 7.5 | [receipts/round3/gates/dp-srcs-milan-datapath.log](receipts/round3/gates/dp-srcs-milan-datapath.log) |
| 10 | dp-srcs-kl-pp-shadow | `python3 syn/ooc/dp_srcs.py --top KL_pp_shadow` | 0 | 4.5 | [receipts/round3/gates/dp-srcs-kl-pp-shadow.log](receipts/round3/gates/dp-srcs-kl-pp-shadow.log) |
| 11 | pp-srcs-check-selftest | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.2 | [receipts/round3/gates/pp-srcs-check-selftest.log](receipts/round3/gates/pp-srcs-check-selftest.log) |
| 12 | docs-check | `$MDPY scripts/docs_check.py` | 0 | 4.7 | [receipts/round3/gates/docs-check.log](receipts/round3/gates/docs-check.log) |
| 13 | docs-check-no-git | `GIT_DIR=/dev/null $MDPY scripts/docs_check.py` | 0 | 4.9 | [receipts/round3/gates/docs-check-no-git.log](receipts/round3/gates/docs-check-no-git.log) |
| 14 | feature-status-no-git | `GIT_DIR=/dev/null $MDPY scripts/check_feature_status.py` | 0 | 0.9 | [receipts/round3/gates/feature-status-no-git.log](receipts/round3/gates/feature-status-no-git.log) |
| 15 | feature-status-selftest | `$MDPY scripts/check_feature_status.py --self-test` | 0 | 0.8 | [receipts/round3/gates/feature-status-selftest.log](receipts/round3/gates/feature-status-selftest.log) |
| 16 | em-dash | `$MDPY scripts/check_em_dash.py --base 1269cdafb4bb964c757baae0f0c5a932d43f540b` | 0 | 2.9 | [receipts/round3/gates/em-dash.log](receipts/round3/gates/em-dash.log) |
| 17 | em-dash-selftest | `$MDPY scripts/check_em_dash.py --selftest` | 0 | 2.9 | [receipts/round3/gates/em-dash-selftest.log](receipts/round3/gates/em-dash-selftest.log) |
| 18 | doc-style | `$MDPY scripts/check_doc_style.py` | 0 | 0.0 | [receipts/round3/gates/doc-style.log](receipts/round3/gates/doc-style.log) |
| 19 | doc-style-selftest | `$MDPY scripts/check_doc_style.py --selftest` | 0 | 0.0 | [receipts/round3/gates/doc-style-selftest.log](receipts/round3/gates/doc-style-selftest.log) |
| 20 | doc-paths | `$MDPY scripts/check_doc_paths.py` | 0 | 0.1 | [receipts/round3/gates/doc-paths.log](receipts/round3/gates/doc-paths.log) |
| 21 | toc-selftest | `$MDPY scripts/gen_toc.py --selftest` | 0 | 0.8 | [receipts/round3/gates/toc-selftest.log](receipts/round3/gates/toc-selftest.log) |
| 22 | toc-verify-anchors | `$MDPY scripts/gen_toc.py --verify-anchors` | 0 | 2.4 | [receipts/round3/gates/toc-verify-anchors.log](receipts/round3/gates/toc-verify-anchors.log) |
| 23 | toc-check | `$MDPY scripts/gen_toc.py --check` | 0 | 3.5 | [receipts/round3/gates/toc-check.log](receipts/round3/gates/toc-check.log) |
| 24 | archive | `$MDPY scripts/check_archive.py` | 0 | 0.3 | [receipts/round3/gates/archive.log](receipts/round3/gates/archive.log) |
| 25 | archive-selftest | `$MDPY scripts/check_archive.py --selftest` | 0 | 0.0 | [receipts/round3/gates/archive-selftest.log](receipts/round3/gates/archive-selftest.log) |
| 26 | doc-map-check | `$MDPY docs/DOC_MAP.gen.py --check` | 0 | 0.4 | [receipts/round3/gates/doc-map-check.log](receipts/round3/gates/doc-map-check.log) |
| 27 | module-matrix-check | `$MDPY docs/traceability/gen_module_matrix.py --check` | 0 | 0.9 | [receipts/round3/gates/module-matrix-check.log](receipts/round3/gates/module-matrix-check.log) |
| 28 | solution-docs | `$MDPY scripts/check_solution_docs.py` | 0 | 0.1 | [receipts/round3/gates/solution-docs.log](receipts/round3/gates/solution-docs.log) |
| 29 | baremetal-only | `python3 scripts/check_baremetal_only.py --check` | 0 | 16.0 | [receipts/round3/gates/baremetal-only.log](receipts/round3/gates/baremetal-only.log) |
| 30 | gptp-docs-make | `make -C gptp-processor docs (GNU Make 4.3)` | 0 | 0.7 | [receipts/round3/gates/gptp-docs-make.log](receipts/round3/gates/gptp-docs-make.log) |
| 31 | ci-scope-selftest | `python3 scripts/ci_scope.py --selftest` | 0 | 3.8 | [receipts/round3/gates/ci-scope-selftest.log](receipts/round3/gates/ci-scope-selftest.log) |
| 32 | ci-events-check | `python3 scripts/ci_events.py --check` | 0 | 0.2 | [receipts/round3/gates/ci-events-check.log](receipts/round3/gates/ci-events-check.log) |
| 33 | ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | 15.3 | [receipts/round3/gates/ci-events-selftest.log](receipts/round3/gates/ci-events-selftest.log) |
| 34 | py-idiom | `python3 scripts/check_py_idiom.py` | 0 | 3.6 | [receipts/round3/gates/py-idiom.log](receipts/round3/gates/py-idiom.log) |
| 35 | py-idiom-selftest | `python3 scripts/check_py_idiom.py --selftest` | 0 | 3.6 | [receipts/round3/gates/py-idiom-selftest.log](receipts/round3/gates/py-idiom-selftest.log) |
| 36 | fail-fast | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.5 | [receipts/round3/gates/fail-fast.log](receipts/round3/gates/fail-fast.log) |
| 37 | hygiene | `python3 scripts/check_hygiene.py --check` | 0 | 0.3 | [receipts/round3/gates/hygiene.log](receipts/round3/gates/hygiene.log) |
| 38 | todo-ownership | `python3 scripts/check_todo_ownership.py` | 0 | 1.4 | [receipts/round3/gates/todo-ownership.log](receipts/round3/gates/todo-ownership.log) |
| 39 | test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | 5.9 | [receipts/round3/gates/test-evidence.log](receipts/round3/gates/test-evidence.log) |
| 40 | control-flow-selftest | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.1 | [receipts/round3/gates/control-flow-selftest.log](receipts/round3/gates/control-flow-selftest.log) |
| 41 | cohesion-selftest | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.1 | [receipts/round3/gates/cohesion-selftest.log](receipts/round3/gates/cohesion-selftest.log) |
| 42 | diff-check-base | `git diff --check 1269cdafb4bb964c757baae0f0c5a932d43f540b HEAD` | 0 | 0.0 | [receipts/round3/gates/diff-check-base.log](receipts/round3/gates/diff-check-base.log) |
| 43 | diff-check-worktree | `git diff --check` | 0 | 0.0 | [receipts/round3/gates/diff-check-worktree.log](receipts/round3/gates/diff-check-worktree.log) |

43 gates, 0 non-zero. Not run, as in rounds 1 and 2 (nothing they execute changed): `scripts/run_all_suites.sh`,
`syn/yosys/run.sh`, `scripts/lint_rtl.py`, `scripts/xvlog_gate.py`, the Yosys self-tests, the builder bank, and
`scripts/act_ci.py --selftest` (AGENTS.md section 5).

### R3.7 Notes and deviations

- `syn/ooc/pp_baseline_rank.py` is outside the gate file but is the gate's hierarchy reader, so item 4 covered it. It
  is shared with the ranking command; its self-tests (`pp_baseline_reports_selftest.py`, `pp_baseline.py --selftest`,
  32 mutants) pass, and its output on all seven real reports is unchanged.
- `check` now refuses a baseline file in which any endpoint is malformed, not only the endpoint it judges: one
  validator for the file, as item 1 asks. The committed file passes.
- The self-test fixture's WNS floor moved from 0 to 0.03 (item 3). That is fixture data, not the accepted policy:
  no tolerance, floor or ceiling of `pp_resource_baseline.json` or the budget table changed, so no STOP.
- The gate-table run was started at `b38bb06d` and stopped after its first gate to scope one docs sentence ("the exit
  status is total" overclaimed: a failed `record --write` file write is an environment error that is not caught). It
  then ran complete at `2b98e485`; the boundary mutant (`b5894838`) followed, and every check in this section was
  rerun at `b5894838`. Stopping the run killed one `ooc_tcl_selftest.py`; `git status --porcelain --ignored` was empty
  afterwards and at exit.
- No STOP condition met: no RTL, no new hosted runner or tool, no accepted tolerance or ceiling changed.
- No push, PR edit, merge, rebase, sub-agent, other checkout, hardware, flashing, processor or interface change. No
  existing comment edited. Scratch and run directories stay under `$VALIDATION_STORAGE/234-a516`.

## Round 4

Status: REVIEW READY at `79e53831a4f623a594f22765be1d05dffeb696a7` on `234-area-baseline` (not pushed; the manager pushes), on top of
`b5894838d6c47180ac4169e7d52dd746f461af21` (round 3; no rebase, no amend).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5969446300
- REVIEW READY (round 4): https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5970259375
- Answers R446-3 (PR #638 comment 5969323709) and R447-3 (5969442442), both NEGATIVE on MINOR findings only.
- Reviewer packets read from `origin/234-review-evidence` at `8894136ac297aae0f46d885887b25762f47177c1`, exported with
  `git archive` to `$VALIDATION_STORAGE/234-a516/r4/review-evidence`, not checked out.
- No Vivado run (the assignment forbids it): every real-data check reads the existing run directories.

Five new one-line commits on `b5894838` (no body, no trailers):

| Commit | Subject |
|---|---|
| `82bc432b5` | Hold the resource gate's exit-code contract by construction: one barrier in main, ASCII-safe output, one bounded converter per number type, named and unrepeated baseline keys, with arms and killed mutants |
| `d8638e6ef` | Add a seeded generative test of the resource gate's exit-code contract: 500 cases in its self-test and a --fuzz mode for real measurements |
| `e6710d133` | State the resource gate's exit-code contract as it holds by construction: the barrier, ASCII output, the two converters, named baseline keys and the generative test |
| `39e9329b8` | Refuse a check of an endpoint the baseline does not hold inside the barrier, as the generative test found it leaving through argparse |
| `79e53831a` | Keep the self-test's timing fixture in its round-3 layout so reviewer probes still plant it, and arm and kill an upper-case input digest and a slack without a fraction |

Diff `b5894838..79e53831`: 6 files (`syn/ooc/pp_resource_gate.py`, `_selftest.py`, `_mutants.py`,
`syn/ooc/pp_baseline_rank.py`, `docs/design/AREA_BUDGET.md`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`). Diff
`1269cdaf..79e53831`: the same 15 files as round 3. No RTL, processor, interface, workflow, pin list, baseline JSON,
tolerance, floor or ceiling change, so no STOP condition was met.

### R4.1 Finding-by-finding

Receipts under `receipts/round4/`. Every probe named is the reviewer's published script, unchanged (R4.5).

| Finding | Severity, lens | Answer | Evidence at `79e53831` |
|---|---|---|---|
| R446-3 F1: a slack too long to be finite reads as infinity and passes | MINOR Conformance, Robustness, Tests, Docs | Item 3: `real()` (`pp_resource_gate.py:374-382`) is the gate's only float conversion and refuses by name a value whose float is not finite. It converts the slack (`:157`, after the `SLACK` grammar `:151`), the half BRAM tile (`:134`, after `[0-9]+(\.5)?` `:131`), every JSON decimal (`parse_float=decimal`, `:385-387`, `:414`) and every budget cell (`:531`). Arms: a WNS and a WHS of 401 digits; a BRAM tile of 401 digits plus `.5`; the same WNS through `main()`. Killed mutants: `finite decimals`, `slack converter`, `hold slack converter`, `half-count converter`. | R446-3 `probe_r3_numbers.py` (A): 0 cases not as the contract states; the WNS, WHS, negative WNS and BRAM-tile cases give rc 2, the controls 0 (`probes/r446-3-probe-r3-numbers.log`). |
| R446-3 F2, R447-3 F2: an integer too large for a float, or a count past the integer-text limit, reaches a traceback and exit 1 | MINOR Conformance, Robustness, Tests, Docs | Item 3: `whole()` (`pp_baseline_rank.py:29-36`) is the only integer conversion: 1 to 15 ASCII digits (a sign only for JSON), so every whole number is below 2**53 and its float is exact and finite. It reads every JSON integer (`parse_int=integer`, `:390-392`), every route status count (`:286`, now inside `routing()`'s `try`), the timed endpoints (`:153`), the utilization counts (`:134`) and every hierarchy count (rank `:59`). A 4,401-digit count is refused by the pattern before `int()` sees it. Arms: a WNS_ns recorded as a 401-digit integer, a scope count of 16 digits and a 4,401-digit integer, each through both commands; a route status count of 16 digits and of 4,401 digits (through `main()`); utilization, timed-endpoint and hierarchy counts of 16 digits. Killed mutants: `baseline integers converted`, `whole number bound`, `route status converter`, `utilization converter`, `timed endpoint converter`, `hierarchy count converter`, `undecodable route status`. | R446-3 `probe_r3_numbers.py`: the route status count of 4,401 digits and both 401-digit baseline integers give rc 2 in `check` and in `check-baseline`. R447-3 `probe_bigint.py` on B and on A: both `10**400` literals rc 2 in both columns, no traceback; B's control keeps `check` rc 1, `check-baseline` rc 0. |
| R446-3 F3: seven claimed refusals without an arm | MINOR Tests | Item 4: an arm through `main()` and a killed shipped mutant for each. Extra identity key (`baseline identity exact keys`); extra figure (`baseline figures exact`); extra scope count (`baseline scope counts exact`); a digest that is a number (`baseline input digest type`); a malformed endpoint after the first (`baseline every endpoint validated`); a doubled errors row (`routing-error row single`); an other-script digit in a middle and in the last hierarchy cell (`hierarchy counts end early`, `hierarchy counts from the fourth cell`). R446-3's two uncounted survivors also got an arm and a killed mutant: an upper-case digest (`baseline input digest lower case`) and a slack without a fraction (`slack fraction`). | R446-3 `probe_r3_mutants.py --jobs 12`: control passes, 20 of 20 KILLED, 0 not applied (`probes/r446-3-probe-r3-mutants.log`). |
| R447-3 F1: a lone-surrogate name turns a refusal into exit 1 by traceback | MINOR Conformance, Robustness, Tests, Docs | Items 1 and 2. One barrier: everything in `main()` after the arguments are read is inside one `try` (`:679-708`); any exception, expected or not, prints `NOT COMPARABLE: <reason>` and exits 2, and exit 1 comes only from `judge()` (`:703-705`). Every line goes through `emit()` (`:646-652`), which writes printable ASCII and escapes any other character as `ascii()` does, so printing cannot raise. And `strict()` refuses any key outside the name class before the validator sees it (`named()`, `:400-409`). The self-test's `cli()` now prints into an ASCII-only strict stream, so every command-line arm fails on a character printing could not encode. Arms: an endpoint field and a scope named by a lone surrogate (both commands); an exception carrying a lone surrogate and an escape character planted in `load`, `census`, `routing`, `judge`, `entry_problems` (through `check`) and in `load` and `check_baseline` (through `check-baseline`), each exit 2; a measurement directory named in another script, exit 0 with the name escaped. Killed mutants: `barrier`, `ASCII output`, `printable ASCII output`, `baseline key names`, `baseline keys checked`. | R447-3 `probe_text.py` (A, real CLI, real stdout): cases A to E rc 2 in both columns with the name escaped (`'\ud800'`, `'r\xe9route'`), no traceback; the control 0 and 0 (`probes/r447-3-probe-text.log`). |
| R447-3 F3: six claimed refusals without an arm | MINOR Tests | Item 4: duplicate errors row (as R446-3 F3); a route status report and a budget page that are not UTF-8 (`undecodable route status`, `undecodable budget page`); THS Total Endpoints 0 with TNS non-zero (`hold-timed endpoints counted`); a standalone clock list holding a number (`baseline standalone clock text`); an extra identity key (as R446-3 F3). Each arm asserts its reason, so a mutant whose exception the barrier catches is still killed by the wrong reason. | R447-3 `extra_mutants_r3.py`: control passes, 13 of 13 KILLED. `probe_gaps.py`: all six cases rc 2. |
| R447-3 S1: duplicate JSON keys are accepted silently | SUGGESTION Robustness | Item 2: `named()` refuses a key an object already holds, in the baseline and in the image manifest. Arms: a repeated ceiling key (both commands), a repeated manifest key. Killed mutant: `baseline repeated keys`. | `probe_text.py` case F: rc 2 and 2, "the key 'LUT' appears twice in one object". |
| R447-3 S2: bool scope counts and late hierarchy cells have no arm | SUGGESTION Tests | Item 4: a scope count that is `true` (`baseline scope counts not bools`); an other-script digit in the middle and last hierarchy cells (`hierarchy counts end early`). | `extra_mutants_r3.py`: both KILLED. |
| R447-3 R1: the PR body names a packet file the archive does not hold | RESIDUE Docs | Item 6: the file is now in this round's packet as `receipts/round4/armq-census.tsv` (sha256 `c9a8113268b037ef4b06f63ea431854a721f345cf65606b927ca35691bf165ff`, the same bytes as round 3's `evidence/round3/armq-census.tsv`, which the round-3 archive did not take). The PR body row now names it and says how to re-derive it: count `armq_r` FD* cells in each run's `baseline_cells.tsv`, whose sha256 is in `43ad8362` `author/receipts/run-receipts.json` (A 1,153, B 1,260). | R447-3 `armq_count.py`: A 1x1 1,153 and B 1x1 1,260, census digests equal to the file's (`probes/r447-3-armq-count.log`). |

### R4.2 The contract by construction

- **Item 1, one barrier.** Argument parsing (argparse, exit 2 with its usage) and the two test modes come first. Then
  one `try` holds every command (`:679-708`). Its handler catches `Exception`: a `Refusal` prints its own reason, any
  other exception its type and message, both as `NOT COMPARABLE: ...`, and the status is 2. The only `return 1` path is
  `judge()`'s status (`:703-705`). Every printed line goes through `emit()`. Arms: the seven planted exceptions above; a
  mutant that narrows the handler to `Refusal` (`barrier`) is killed by them, and one that returns another status from
  it (`refusal exit status`) by every refusal arm.
- **Found by the generative test (a 20,000-case fixture run at `e6710d13`) and fixed in `39e9329b`:** a `check` of an
  endpoint the baseline does not hold left
  through `parser.error` (exit 2 by `SystemExit`, which the barrier does not catch, with the reason on standard error).
  It is now a `Refusal` inside the barrier, "baseline ... holds no endpoint X, only ...". Arm `check of an endpoint the
  baseline does not hold`, mutant `check names a recorded endpoint`. Only missing arguments still exit through argparse.
- **Item 2, names.** `strict()` (`:412-415`) reads every JSON the gate reads (the baseline and the image manifest)
  with `object_pairs_hook=named`: every key 1 to 128 of `A-Z a-z 0-9 _ . : / - [ ]`, none repeated, refused by name.
  `load()` then holds endpoint names (`:480-481`) and policy figure names (`:464-465`) to `NAME`, without brackets. The
  fixed sets (file, endpoint, record, identity, figures, scope counts) are compared exactly, and the record's own key
  set is now closed too (`:438-440`). See R4.8 for the bracket.
- **Item 3, converters.** `whole()` and `real()` as in R4.1; the self-audit (R4.3) cites the converter at every site.
  The bound: at most 15 digits, so every whole number is below 10**15 < 2**53 and converts to a float exactly.
- **`record --write`** now validates the text it is about to write with the same `load()` and refuses, exit 2, a
  baseline the next read would refuse (`:700`). Arm: an endpoint named `copy[1]`, file unchanged. Mutant `record
  --write validated`.
- **Self-test:** 247 arms (96 route, 8 standalone, 1 relocation, 16 `check`, 27 `check-baseline`, 42 malformed
  baselines through both commands, 7 planted exceptions, a non-ASCII directory, a refused write, `record --write` and
  CARRY4, cross-kind) and 500 generated cases.
- **Mutants:** 158 (149 of the gate, 9 of the hierarchy parser and converter), control passes, all killed. Against
  round 3: 6 removed with the code they mutated (`ASCII counts`, `route status counts`, `route status count format`,
  `timed endpoint count format`, `baseline overflowing numbers`, `finite baseline numbers`, all replaced by converter
  mutants), 42 added. The campaign now runs its mutants in parallel, one per processor (`concurrent.futures`): here
  the 158 took 3.5 s, against 27.8 s for round 3's 122 one after another.

### R4.3 Self-audit, with the converter at each site

Line numbers at `79e53831` in `syn/ooc/pp_resource_gate.py` unless marked "rank" (`syn/ooc/pp_baseline_rank.py`).
"R4" marks a place this round changed.

Every number conversion. `int(` and `float(` appear nowhere else in either module (rank `:36` is inside `whole()`,
`:379` inside `real()`):

| # | Site | Data | Converter | Guard in front |
|---:|---|---|---|---|
| N1 | `:414` (`strict()`) | every JSON integer of the baseline and the image manifest | R4: `parse_int=integer` (`:390-392`) -> `whole(signed=True)` | JSON's own grammar; 1 to 15 digits |
| N2 | `:414` | every JSON decimal of both files | R4: `parse_float=decimal` (`:385-387`) -> `real()` | JSON's grammar; finite after `float()` (`:380`) |
| N3 | `:414` | `NaN`, `Infinity`, `-Infinity` | `parse_constant=constant` (`:395-397`) refuses | - |
| N4 | `:134` | utilization used count | R4: `whole()`, or `real()` for a half tile | `[0-9]+(\.5)?` (`:131`) |
| N5 | `:153` | TNS and THS Total Endpoints | R4: `whole()` (was `COUNT` then `int()`) | column name; then `> 0` (`:155`) |
| N6 | `:157` | WNS, WHS | R4: `real()` (was bare `float()`) | `SLACK` `-?[0-9]+\.[0-9]+` (`:151`) |
| N7 | `:286` | every route status count | R4: `whole()`, inside the `try` (`:284-288`; was `COUNT` then `int()` outside it) | `STATUS_ROW` (`:103`) |
| N8 | rank `:59` | every hierarchy count cell | R4: `whole()` (was `int()`) | every cell `[0-9]+` (rank `:47`) |
| N9 | `:531` | budget policy cell | R4: `real()` (was `float()`) | `[+-]?[0-9]+(?:\.[0-9]+)?( ns)?` (`:527`) |

Where the converted numbers are used: `judge()` (`:321-333`), `verdict_for()` (`:346-358`), `entry_problems()`
(`:493-505`), `check_baseline()` (`:551`) and `scope_deltas()` (`:365-369`) only compare, subtract and format. A whole
number is exact as a float and a decimal is finite, so no mixed subtraction can raise. Two finite floats near the
float limit could subtract to infinity; that only compares and prints, and `round(inf, 3)` returns infinity.

Every index, subscript and `.get()` of file content, carried from round 3 (rows 1-61) at the new line numbers:

| # | Site | Data | Operation | Guard in front |
|---:|---|---|---|---|
| 1 | `:473` | baseline file | `strict()` | R4: N1-N3 and `named()`; `OSError`, `ValueError`, `RecursionError` -> exit 2 (`:474-475`) |
| 3 | `:476`, `:481-482` | top level | `.get("endpoints")`, `["endpoints"]` | `isinstance(baseline, dict)` first; `:476-477` refuse |
| 4 | `:478-479` | top-level keys | `set(baseline)` | unknown keys refused |
| 4a | `:480-481` | endpoint names | `NAME.fullmatch` | R4: 1 to 128 of `A-Z a-z 0-9 _ . : / -` |
| 5 | `:425` | endpoint | `.get("record")` | `isinstance(entry, dict)` in the same expression |
| 6 | `:431` | record | `base["kind"]`, `["identity"]`, `["figures"]`, `["scopes"]` | `:426-430`: a dict holding every `RECORD` key |
| 7 | `:435-437` | endpoint keys | `set(entry)` | unknown keys refused |
| 7a | `:438-440` | record keys | `set(base)` | R4: unknown record fields refused |
| 8 | `:443` | identity | `identity[key]` | `:441` exactly the `IDENTITY` keys (elif chain) |
| 9 | `:445` | flow, clock | iterate | `:443` both lists; items text |
| 10 | `:447` | input digest | `re.fullmatch` | `isinstance(..., str)` first; 64 lower-case hex |
| 11 | `:449` | kind | `ROWS[kind]` | `:432` |
| 12 | `:450-453` | figures | `sorted()`, `.values()` | exactly the kind's figures; each a number, not a bool; N1-N2 |
| 13 | `:454-458` | scopes | `.values()` | dict of dicts holding exactly `SCOPE`; `type(count) is int`, `>= 0`; N1 |
| 14 | `:459-465` | policy | `.get(field, {})`, `.values()` | dict first; numbers (N1-N2); R4: figure names `NAME` |
| 15 | `:490` | validated endpoint | `entry["record"]["kind"]`, `["figures"]` | `load()` before `entry_problems()` in both commands (`:680`, `:689`, `:538`) |
| 16-19 | `:492-505` | policy, figures | `GATED[kind]`, `.get(...)`, `figures[figure]`, `entry["floor"][figure]` | rows 11-14; absences refused first (elif) |
| 20-24 | `:308-333` | record, candidate | `entry["record"]`, `base[...]`, `candidate[...]`, `entry["tolerance"][figure]` | `load()` and `entry_problems()` (`:689-691`); candidate built by `record()` with every key |
| 25 | `:365-369` | scopes | `.get(...)`, `:+d` | integer counts (row 13, N8) |
| 26 | `:115` | report header | `hits[0]` | `len(hits) != 1` refused `:113-114` |
| 27-28 | `:124-127` | utilization | `cells[0]`, `cells[1]`, `ROWS[kind]`, `seen.get` | `len(cells) >= 2`; kind from `kind_of()`; one value per label (`:128-129`) |
| 30-32 | `:143-149` | timing | `blocks[1]`, `lines[heads + 2]`, `names[0]`, `values[4]` | `:140-150` |
| 35-37 | `:165`, `:175`, `:186` | script paths | `parents[2]`, `generated[0]`, `roots[0]` | `len(path.parents) > 2`; `len(...) != 1` refused |
| 38-40 | `:195-200` | image manifest | `strict()`, `.get("path")`, `image['sha256']` | R4: `strict()` (N1-N3, `named()`); list of objects with text `path` and `sha256` (`:196-198`) |
| 41 | `:212` | tool header | `tool[1]` | `tool is None` refused |
| 42-43 | `:221-231`, `:248`, `:268` | cell census | `lines[0]`, `carry[...]` | `not lines` first; `carry` starts `{"": 0}` |
| 44-48 | `:238-263` | kind, hierarchy | `ROOTS[kind]`, `split("/", 1)[1]`, `counts[name]`, `kinds[0]`, `SCRIPTS[kind]` | as round 3 |
| 49-51 | `:285-296` | route status | `reports[0]`, `counts.get(label, [])` | one report (`:281-282`); one row of each label (`:289-293`) |
| 52-55 | rank `:43-59` | hierarchy | `fields[...]`, `int` | ten cells; every count cell `[0-9]+` (`:47`); R4: `whole()` (N8) |
| 56 | `:540` | budget page | `read_text()` | `OSError`, `ValueError`, `Refusal` -> named problem, exit 2 (`:541-542`) |
| 57-59 | `:518-531` | budget table | `lines[...]`, `cells[0]`, `name[1]`, `value[1]` | one table; row shape; cell grammar; R4: `real()` (N9) |
| 60 | `:537-553` | baseline, table | `["endpoints"]`, `.get(figure)` | `load()`; names on both sides |
| 61 | `:680-705` | baseline | `["endpoints"]`, `.get(args.endpoint)`, `[args.endpoint]` | `load()`; R4: a `check` endpoint the baseline lacks is refused in the barrier (`:685-687`) |

Rows 2 (`float()` of a JSON decimal) and 29, 33, 34 and 50 (report conversions) are N1-N9 now. No site was found
without a guard. Anything a guard does not pre-empt is caught by the barrier, and the generative test (R4.4) found no
case that reached it except the argparse path fixed in `39e9329b`.

### R4.4 The generative test (item 5)

`mutate_json()` and `mutate_report()` (`syn/ooc/pp_resource_gate_selftest.py`) generate one case each from a seeded
`random.Random`. They return the changed file's bytes and whether the change breaks a shape the gate documents. The
gate's `fuzz()` (`pp_resource_gate.py`, the `--fuzz N` mode) lays each case out beside the measurement: every
unchanged file is linked, the changed one is written. It runs `check`, and `check-baseline` for a baseline case,
through `main()` into the ASCII-only stream. Each target's recorded input digest is zeroed first, so a changed figure
reaches `judge()` rather than the identical-inputs refusal.

- Baseline (40 % of cases): a value of another JSON type where the documented shape takes one type; a number changed
  within its type; a required key removed; a key added to a closed object; a key renamed to a non-name, or to a name
  with a generate index; a key written twice; a value replaced by an overflowing or non-JSON number; a digit replaced by
  another script's digit; truncation; a lone surrogate, control, mark or wide character inserted in a text; deep
  nesting, 2,000 extra scopes or a 200,000-character text; bytes that are not UTF-8.
- Reports (utilization, timing, hierarchy, cell census, image manifest, route status, the standalone clock): a gated
  count, slack or tile replaced by other-script digits, a value past its bound, a non-number, or another valid
  number; a header or Design Timing Summary written twice or removed; a route status row written twice or removed; a
  second route status report; the census header changed; truncation; a line deleted, doubled or swapped; 500 junk
  lines; a stray character; bytes that are not UTF-8; an empty or missing file.
- Every case must exit 0, 1 or 2, never by an escaped exception, and give a reason with 2 (`NOT COMPARABLE` for
  `check`). Every case whose change breaks a documented shape must exit 2.

| Run (`receipts/round4/fuzz/`) | Cases | rc | Exits 0 / 1 / 2 (`check`) | Shape-breaking cases, all exit 2 | Result |
|---|---:|---:|---|---:|---|
| Self-test, seed 234, fixtures | 500 | 0 | in `gates/resource-gate-selftest.log` | - | 0 failures |
| `fuzz-A-route-20000.log` | 20000 | 0 | 4089 / 175 / 15737 | 13505 | 0 failures; case digest `1c07ac027c0c26b3` |
| `fuzz-fixtures-20000.log` | 20000 | 0 | 3489 / 165 / 16348 | 12781 | 0 failures; case digest `36552f395d6ef669` |
| `fuzz-A-ooc-1x1-5000.log` | 5000 | 0 | 1158 / 21 / 3822 | 3140 | 0 failures; case digest `9f1495ce5396f57b` |

`fuzz-A-route-20000` is A's real route directory against the committed baseline and budget page; `fuzz-A-ooc-1x1-5000`
is A's real standalone 1x1 directory. Counts include one control case per target. The shape-breaking count comes from
`scratch-scripts/replay_broken.py`, which replays each run's generation without the gate (the generators draw every
random choice) and checks that its per-label totals equal the run's log (`replay-*.log`: equal for all three). The
inputs' sha256 are in `fuzz/inputs.sha256`, the head in `fuzz/head.txt`.

The generative test by itself, without the arms (`receipts/round4/fuzz-kill-matrix.log`,
`scratch-scripts/fuzz_kill_matrix.py`): each shipped mutant is applied to a copy, which runs only `--fuzz 500 --seed
234`. The 500 cases alone detect 53 of 158 shipped mutants, with the control passing. It is not the self-test's kill rate (the arms and cases together kill all 158); it shows that the
generated cases can fail, and on which defects. Among those it detects: the timed-endpoint, slack, utilization, route
status and hierarchy converters, the JSON integer and decimal converters, the finite check, the bound and the ASCII
digits of `whole()`, the ASCII output, repeated and checked keys, and the record's closed field set. The barrier is
not among them: no generated case reaches it, because the gate's own handlers name every failure first, so the seven
planted-exception arms test it.

### R4.5 Every reviewer probe of rounds 1 to 3, unchanged

Runner `scratch-scripts/run_probes_r4.sh` (exported packet `8894136a`, scratch outside the checkout,
`PYTHONDONTWRITEBYTECODE=1`); one log and rc per probe under `receipts/round4/probes/`; `git status --porcelain
--ignored` empty afterwards. `R446-3/r1-probes/` and `r2-probes/` are byte-identical to R446-1's and R446-2's scripts
(`probes/copies-cmp.txt`), so those rows are their results too.

| Reviewer | Probe | rc | Result at `79e53831` | Reading |
|---|---|---:|---|---|
| R446-1 | `probe_gate_cli.py` | 1 | 117 cases, 1 not as expected | As in rounds 2 and 3: `inf` slack with 0 endpoints gives 2 against the probe's literal want of 1, which R446-1 F1 allowed. |
| R446-1 | `probe_gate_mutants.py` | 0 | 21 killed, 0 survived, control passes, 2 not applied | As in round 3: `count format accepts any decimal` and `check_baseline: recorded figure below floor`; shipped `count format decimals` and `baseline floor value` are killed. |
| R446-1 | `probe_pr_mutant_reasons.py` | 0 | 149 of 149 ARM | Every shipped gate mutant is killed by an arm assertion. |
| R446-1 | `reconcile.py` | 1 | 2 mismatches | Its two hard-coded round-1 sentences, as in rounds 2 and 3. |
| R447-1 | `probe_cli.py` | 0 | 54 of 54 as documented | |
| R447-1 | `extra_mutants.py` | 0 | 16 killed, 0 survived, 2 not unique | `CLI refusal exits 0` (the barrier rewrote the line; shipped `refusal exit status` killed) and `baseline floor value` (as round 3; shipped mutant killed). |
| R447-1 | `probe_route_status.py` | 0 | clean report exit 2; 37 unrouted exit 2 | As round 3: its invented report has no net-count rows. |
| R447-1 | `partition_check.py` | 0 | +79 / 391 / +93; `u_pp` -23 / +107 | Equal to the prose; its last line is fixed round-1 text. |
| R447-1 | `replay_records.py` | 0 | A 0, 0, 0; B 1, 0, 0; 10 ns 2 | |
| R447-1 | `check_tables.py` | 0 | 49 groups, 0 mismatches | |
| R446-2 | `partition_rederive.py` | 0 | 0 mismatches | |
| R446-2 | `probe_extra_mutants.py --jobs 12` | 0 | control passes; every applicable mutant KILLED; 3 not applicable, 1 note | Not applicable: `budget floors read as zero` (the `float()` it rewrites is `real()` now; shipped `budget floors read` killed), `timed endpoints at zero accepted` and `check skips the ceiling list` (as round 3; shipped `timed endpoint boundary` and `baseline route ceiling` killed). |
| R446-2 | `probe_malformed_record.py` | 0 | 0 cases not exit 2 | |
| R446-2 | `probe_policy_pin.py` | 0 | 0 cases not as expected | |
| R446-2 | `probe_route_status.py` (A) | 1 | 15 of 16 | Both CONTRACT cases 2; the 16th is the declined S1 layout (want 1, got 2). |
| R447-2 | `classify_mutants.py` | 0 | 145 ARM, 4 ESCAPED, 0 CRASH, 0 survived, of 149 | ESCAPED: `barrier`, `undecodable route status`, `image manifest nested too deep`, `Slice row`. Each removes a refusal, so the escaped exception is the defect its arm names. Round 3 had 23 ESCAPED. |
| R447-2 | `partition_r2.py` | 0 | +79 / 391; +93 / 121; `u_pp` -23 / +107 | |
| R447-2 | `probe_contract.py` (A) | 0 | every case rc 2 in both columns | Control: `check` 1, `check-baseline` 0. |
| R447-2 | `probe_policy.py` | 0 | 107 of 107 | |
| R447-2 | `probe_route_real.py` (A / B) | 0 / 0 | 15 of 15 / 14 of 15 | The B miss is B's own +625 LUT (rc 1), as in R447-2's receipt. |
| R447-2 | `real_data.sh` | 0 | A 0, 0, 0; 10 ns 2; B 1, 0, 0 | |
| R446-3 | `probe_r3_mutants.py --jobs 12` | 0 | 20 of 20 KILLED, control passes | Round 3: 11 killed. |
| R446-3 | `probe_r3_numbers.py` (A) | 0 | 0 cases not as the contract states | F1 and F2 cases rc 2; controls 0. |
| R446-3 | `probe_r3_untested.py` (A) | 0 | 0 cases where the head does not refuse | |
| R446-3 | `probe_r447_2_cases.py` (A) | 0 | 0 not exit 2 | |
| R446-3 | `probe_hierarchy_equiv.py` (old `0feff20f`) | 0 | 0 mismatches on the seven real reports | Tables equal and ranking TSV byte-identical; the planted non-count row refused. |
| R447-3 | `extra_mutants_r3.py` | 0 | 13 of 13 KILLED, control passes | Round 3: 5 killed. |
| R447-3 | `probe_text.py` (A) | 0 | A-F rc 2 in both columns, no traceback | E (an ordinary non-ASCII endpoint name) and F (a repeated key) are refused too. |
| R447-3 | `probe_bigint.py` (B / A) | 0 / 0 | both `10**400` literals rc 2 in both columns | B's control `check` 1, `check-baseline` 0. |
| R447-3 | `probe_gaps.py` (A) | 0 | 6 of 6 rc 2 | |
| R447-3 | `hier_compare.py` (old `0feff20f` / `b5894838`) | 0 / 0 | 7 reports, 0 differing | |
| R447-3 | `armq_count.py` | 0 | 1x1: A 1,153, B 1,260; route: A 1,125, B 1,120 | Census digests as in the run receipts. |
| R447-3 | `real_data.sh` | 0 | A 0, 0, 0; 10 ns 2; B 1, 0, 0 | |
| R446-3, R447-3 | `run_gates.sh` | - | see R4.7 | |

### R4.6 Real data through the gate (no Vivado; existing run directories)

| Receipt (`receipts/round4/`) | rc | Result |
|---|---:|---|
| `real/gate-check-A-ooc-1x1.log` | 0 | LUT 24343 24343 0 ok; RESULT: PASS |
| `real/gate-check-A-ooc-1x1-10ns.log` | 2 | NOT COMPARABLE: tool or recipe change in standalone_clock_ns; measure the baseline again under the new identity instead of comparing across it |
| `real/gate-check-A-ooc-8x8.log` | 0 | LUT 31562 31562 0 ok; RESULT: PASS |
| `real/gate-check-A-route.log` | 0 | LUT 50128 50128 0 ok; route status: complete, no unrouted net and no routing error; RESULT: PASS |
| `real/gate-check-B-ooc-1x1.log` | 0 | LUT 24343 24505 162 ok; RESULT: PASS |
| `real/gate-check-B-ooc-8x8.log` | 0 | LUT 31562 31390 -172 ok, below the baseline; RESULT: PASS |
| `real/gate-check-B-route.log` | 1 | LUT 50128 50753 625 REGRESSION: grew by more than 500; route status: complete, no unrouted net and no routing error; RESULT: MATERIAL REGRESSION |

The committed baseline passes the validator unchanged (`check-baseline`: "baseline PASS: 3 endpoints").

### R4.7 Gate table

Head `79e53831a4f623a594f22765be1d05dffeb696a7`, worktree clean: True; `GNU Make 4.3` first on `PATH`. `$MDPY` =
`$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`. Each command ran in the foreground of the runner from the lane
root (physical `/data` path), without a pipeline; `docs-check-no-git` and `feature-status-no-git` set
`GIT_DIR=/dev/null`. Machine record: `receipts/round4/gates/gate-results.json`; runner `scratch-scripts/run_gates_r4.py`,
driven by `scratch-scripts/run_all_r4.sh` in the background with its own log and rc file.

| # | Gate | Command | rc | Seconds | Receipt |
|---:|---|---|---:|---:|---|
| 1 | dp-srcs-selftest | `python3 syn/ooc/dp_srcs.py --selftest` | 0 | 16.1 | [receipts/round4/gates/dp-srcs-selftest.log](receipts/round4/gates/dp-srcs-selftest.log) |
| 2 | ooc-tcl-selftest | `python3 syn/ooc/ooc_tcl_selftest.py` | 0 | 466.6 | [receipts/round4/gates/ooc-tcl-selftest.log](receipts/round4/gates/ooc-tcl-selftest.log) |
| 3 | pp-baseline-selftest | `python3 syn/ooc/pp_baseline.py --selftest` | 0 | 0.1 | [receipts/round4/gates/pp-baseline-selftest.log](receipts/round4/gates/pp-baseline-selftest.log) |
| 4 | pp-baseline-mutants | `python3 syn/ooc/pp_baseline_mutants.py` | 0 | 2.7 | [receipts/round4/gates/pp-baseline-mutants.log](receipts/round4/gates/pp-baseline-mutants.log) |
| 5 | pp-baseline-reports-selftest | `python3 syn/ooc/pp_baseline_reports_selftest.py` | 0 | 0.0 | [receipts/round4/gates/pp-baseline-reports-selftest.log](receipts/round4/gates/pp-baseline-reports-selftest.log) |
| 6 | resource-gate-selftest | `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | 1.7 | [receipts/round4/gates/resource-gate-selftest.log](receipts/round4/gates/resource-gate-selftest.log) |
| 7 | resource-gate-mutants | `python3 syn/ooc/pp_resource_gate_mutants.py` | 0 | 3.5 | [receipts/round4/gates/resource-gate-mutants.log](receipts/round4/gates/resource-gate-mutants.log) |
| 8 | resource-gate-check-baseline | `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | 0.1 | [receipts/round4/gates/resource-gate-check-baseline.log](receipts/round4/gates/resource-gate-check-baseline.log) |
| 9 | dp-srcs-milan-datapath | `python3 syn/ooc/dp_srcs.py --top milan_datapath` | 0 | 8.6 | [receipts/round4/gates/dp-srcs-milan-datapath.log](receipts/round4/gates/dp-srcs-milan-datapath.log) |
| 10 | dp-srcs-kl-pp-shadow | `python3 syn/ooc/dp_srcs.py --top KL_pp_shadow` | 0 | 5.2 | [receipts/round4/gates/dp-srcs-kl-pp-shadow.log](receipts/round4/gates/dp-srcs-kl-pp-shadow.log) |
| 11 | pp-srcs-check-selftest | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.3 | [receipts/round4/gates/pp-srcs-check-selftest.log](receipts/round4/gates/pp-srcs-check-selftest.log) |
| 12 | docs-check | `$MDPY scripts/docs_check.py` | 0 | 5.0 | [receipts/round4/gates/docs-check.log](receipts/round4/gates/docs-check.log) |
| 13 | docs-check-no-git | `$MDPY scripts/docs_check.py` | 0 | 5.0 | [receipts/round4/gates/docs-check-no-git.log](receipts/round4/gates/docs-check-no-git.log) |
| 14 | feature-status-no-git | `$MDPY scripts/check_feature_status.py` | 0 | 0.9 | [receipts/round4/gates/feature-status-no-git.log](receipts/round4/gates/feature-status-no-git.log) |
| 15 | feature-status-selftest | `$MDPY scripts/check_feature_status.py --self-test` | 0 | 0.9 | [receipts/round4/gates/feature-status-selftest.log](receipts/round4/gates/feature-status-selftest.log) |
| 16 | em-dash | `$MDPY scripts/check_em_dash.py --base 1269cdafb4bb964c757baae0f0c5a932d43f540b` | 0 | 3.4 | [receipts/round4/gates/em-dash.log](receipts/round4/gates/em-dash.log) |
| 17 | em-dash-selftest | `$MDPY scripts/check_em_dash.py --selftest` | 0 | 3.2 | [receipts/round4/gates/em-dash-selftest.log](receipts/round4/gates/em-dash-selftest.log) |
| 18 | doc-style | `$MDPY scripts/check_doc_style.py` | 0 | 0.1 | [receipts/round4/gates/doc-style.log](receipts/round4/gates/doc-style.log) |
| 19 | doc-style-selftest | `$MDPY scripts/check_doc_style.py --selftest` | 0 | 0.0 | [receipts/round4/gates/doc-style-selftest.log](receipts/round4/gates/doc-style-selftest.log) |
| 20 | doc-paths | `$MDPY scripts/check_doc_paths.py` | 0 | 0.1 | [receipts/round4/gates/doc-paths.log](receipts/round4/gates/doc-paths.log) |
| 21 | toc-selftest | `$MDPY scripts/gen_toc.py --selftest` | 0 | 0.9 | [receipts/round4/gates/toc-selftest.log](receipts/round4/gates/toc-selftest.log) |
| 22 | toc-verify-anchors | `$MDPY scripts/gen_toc.py --verify-anchors` | 0 | 2.5 | [receipts/round4/gates/toc-verify-anchors.log](receipts/round4/gates/toc-verify-anchors.log) |
| 23 | toc-check | `$MDPY scripts/gen_toc.py --check` | 0 | 3.8 | [receipts/round4/gates/toc-check.log](receipts/round4/gates/toc-check.log) |
| 24 | archive | `$MDPY scripts/check_archive.py` | 0 | 0.3 | [receipts/round4/gates/archive.log](receipts/round4/gates/archive.log) |
| 25 | archive-selftest | `$MDPY scripts/check_archive.py --selftest` | 0 | 0.1 | [receipts/round4/gates/archive-selftest.log](receipts/round4/gates/archive-selftest.log) |
| 26 | doc-map-check | `$MDPY docs/DOC_MAP.gen.py --check` | 0 | 0.4 | [receipts/round4/gates/doc-map-check.log](receipts/round4/gates/doc-map-check.log) |
| 27 | module-matrix-check | `$MDPY docs/traceability/gen_module_matrix.py --check` | 0 | 1.0 | [receipts/round4/gates/module-matrix-check.log](receipts/round4/gates/module-matrix-check.log) |
| 28 | solution-docs | `$MDPY scripts/check_solution_docs.py` | 0 | 0.1 | [receipts/round4/gates/solution-docs.log](receipts/round4/gates/solution-docs.log) |
| 29 | baremetal-only | `python3 scripts/check_baremetal_only.py --check` | 0 | 17.1 | [receipts/round4/gates/baremetal-only.log](receipts/round4/gates/baremetal-only.log) |
| 30 | gptp-docs-make | `make -C gptp-processor docs` | 0 | 0.7 | [receipts/round4/gates/gptp-docs-make.log](receipts/round4/gates/gptp-docs-make.log) |
| 31 | ci-scope-selftest | `python3 scripts/ci_scope.py --selftest` | 0 | 3.8 | [receipts/round4/gates/ci-scope-selftest.log](receipts/round4/gates/ci-scope-selftest.log) |
| 32 | ci-events-check | `python3 scripts/ci_events.py --check` | 0 | 0.2 | [receipts/round4/gates/ci-events-check.log](receipts/round4/gates/ci-events-check.log) |
| 33 | ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | 16.3 | [receipts/round4/gates/ci-events-selftest.log](receipts/round4/gates/ci-events-selftest.log) |
| 34 | py-idiom | `python3 scripts/check_py_idiom.py` | 0 | 3.9 | [receipts/round4/gates/py-idiom.log](receipts/round4/gates/py-idiom.log) |
| 35 | py-idiom-selftest | `python3 scripts/check_py_idiom.py --selftest` | 0 | 3.9 | [receipts/round4/gates/py-idiom-selftest.log](receipts/round4/gates/py-idiom-selftest.log) |
| 36 | fail-fast | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.5 | [receipts/round4/gates/fail-fast.log](receipts/round4/gates/fail-fast.log) |
| 37 | hygiene | `python3 scripts/check_hygiene.py --check` | 0 | 0.4 | [receipts/round4/gates/hygiene.log](receipts/round4/gates/hygiene.log) |
| 38 | todo-ownership | `python3 scripts/check_todo_ownership.py` | 0 | 1.6 | [receipts/round4/gates/todo-ownership.log](receipts/round4/gates/todo-ownership.log) |
| 39 | test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | 6.3 | [receipts/round4/gates/test-evidence.log](receipts/round4/gates/test-evidence.log) |
| 40 | control-flow-selftest | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.1 | [receipts/round4/gates/control-flow-selftest.log](receipts/round4/gates/control-flow-selftest.log) |
| 41 | cohesion-selftest | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.1 | [receipts/round4/gates/cohesion-selftest.log](receipts/round4/gates/cohesion-selftest.log) |
| 42 | diff-check-base | `git diff --check 1269cdafb4bb964c757baae0f0c5a932d43f540b HEAD` | 0 | 0.0 | [receipts/round4/gates/diff-check-base.log](receipts/round4/gates/diff-check-base.log) |
| 43 | diff-check-worktree | `git diff --check` | 0 | 0.0 | [receipts/round4/gates/diff-check-worktree.log](receipts/round4/gates/diff-check-worktree.log) |

43 gates, 0 non-zero. The two round-3 reviewers'
gate runners, unchanged, ran after it: R446-3 `run_gates.sh` (`receipts/round4/r446-3-run-gates/`) and R447-3
`run_gates.sh` (`receipts/round4/r447-3-run-gates/`); their totals are in the note below. Not run, as in rounds 1 to
3 (nothing they execute changed): `scripts/run_all_suites.sh`, `syn/yosys/run.sh`, `scripts/lint_rtl.py`,
`scripts/xvlog_gate.py`, the Yosys self-tests, the builder bank, and `scripts/act_ci.py --selftest` (AGENTS.md
section 5).

Round-3 reviewers' gate runners, unchanged, at this head: R446-3 `run_gates.sh` 31 of 31 jobs rc 0; R447-3 `run_gates.sh` 31 of 31 jobs rc 0. R446-3's runner calls `python3` for the Markdown gates, so it ran with the Markdown environment's interpreter first on `PATH`; both had GNU Make 4.3 first.

### R4.8 Notes and deviations

- **Item 2's name class, one deviation, published here.** `[A-Za-z0-9_.:/-]{1,128}` would refuse the committed
  baseline: five recorded scope names hold a generate index, `u_pp/g_rx_pool[0].u_rx_slots` to `[5]`, which is how
  Vivado names a generate block's instances. Holding item 2 literally would make A's three endpoints exit 2, against
  the same assignment's real-data gate, or need a re-recorded baseline whose scope names no longer match the reports.
  So sub-block scope names alone may also hold `[` and `]` (`SCOPE_NAME`, `:93-94`). Endpoint, field and figure names
  are held to the class exactly. Arms: a scope name with a generate index is accepted; an endpoint `route[1]` and a
  tolerance figure `LUT[0]` are refused. Mutants `scope names hold a generate index`, `endpoint names` and `policy
  figure names` are killed. If the class should be literal everywhere, that needs a decision on how scope names are
  recorded.
- **Where the generative test lives.** The generators and their oracle are in the self-test module; the `--fuzz`
  driver (`run_case()`, `violations()`, `fuzz()`, about 85 lines) is in the gate module. Both reviewers' mutant probes
  copy exactly three modules (the gate, the hierarchy parser, the self-test), so the test could not move to a fourth.
  Wholly in the self-test it would exceed the repository's 1,000-line module limit (`scripts/check_py_idiom.py`).
- **The barrier's limit.** It cannot report a failure of standard output itself (a closed pipe), because there is no
  output to report it on; that is the environment, not an input. Round 3's one uncaught exit, a failed `record
  --write` file write, is now inside the barrier and exits 2.
- **Behaviour added beyond the findings, each with an arm and a killed mutant:** the record's own field set is closed
  (`baseline record fields`); the image manifest is read as strict JSON too (`image manifest strict`); `record --write`
  validates before writing; an unknown endpoint is refused inside the barrier.
- **Self-test fixture:** `82bc432b` widened the fixture's timing table to Vivado's twelve columns for the THS arm.
  That broke R447-1's `probe_cli.py`, which plants the six-column value row, so `79e53831` restored the round-3 table
  and plants the THS column in that one arm instead. The fixture baseline's arms now use an `edit()` helper; no
  round-3 arm was dropped.
- No push, PR edit, merge, rebase, sub-agent, other checkout, hardware, flashing, processor or interface change. No
  existing comment edited. Scratch and run directories stay under `$VALIDATION_STORAGE/234-a516`.

## Round 5

Status: REVIEW READY at `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` on `234-area-baseline` (not pushed; the manager pushes), on top of
`79e53831a4f623a594f22765be1d05dffeb696a7` (round 4; no rebase, no amend).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5970587136
- REVIEW READY (round 5): https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5970940747
- Answers R446-4 (PR #638 comment 5970466762, NEGATIVE on one MINOR) and R447-4 (5970584109, POSITIVE, with three
  RESIDUE items and two SUGGESTIONs).
- Reviewer packets read from `origin/234-review-evidence` at `92c0a2d4c77103c7f5e2b3b1cf30a4c6b0d88eab`, exported with
  `git archive` to `$VALIDATION_STORAGE/234-a516/r5/review-evidence`, not checked out.
- No Vivado run: every real-data check reads the existing run directories.

Two new one-line commits on `79e53831` (no body, no trailers):

| Commit | Subject |
|---|---|
| `6a4fa92f0` | Hold every key of the baseline and the image manifest to the name class, open objects included and scope names alone allowed brackets, with arms, killed mutants and generated note and manifest keys, and scope the gate docstring's exit contract to its three commands |
| `ec7eb2d8f` | State the resource gate's name class as it holds for every key, notes and image manifest entries included, and the generative test's oracle as it checks |

Diff `79e53831..ec7eb2d8`: 5 files (`syn/ooc/pp_resource_gate.py`, `_selftest.py`, `_mutants.py`,
`docs/design/AREA_BUDGET.md`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`), +115 / -64. Diff `1269cdaf..ec7eb2d8`: the
same 15 files as rounds 3 and 4. No RTL, processor, interface, workflow, baseline JSON, tolerance, floor or ceiling
change.

### R5.1 Finding-by-finding

Receipts under `receipts/round5/`. Every probe named is the reviewer's published script, unchanged (R5.5).

| Finding | Severity, lens | Answer | Evidence at `ec7eb2d8` |
|---|---|---|---|
| R446-4 F1: a bracketed key outside a sub-block scope name is accepted, against the stated name class | MINOR Conformance, Robustness, Tests, Docs | Item 1, ruling (a). One walk, `names()` (`pp_resource_gate.py:418-436`), run by `strict()` (`:439-447`) on every JSON the gate reads, holds every key to `NAME` (`:98`), the keys inside open objects included: notes such as `description` and `measured`, and image manifest entries. The one exception is the keys of the object at `SCOPES = ("endpoints", None, "record", "scopes")` (`:102`), a record's sub-block scope names, which are held to `SCOPE_NAME` (`:100`). `load()` passes `SCOPES` (`:503`); the image manifest (`:203`) passes none, so every manifest key is a `NAME`. Anything else raises a `ValueError` naming the key, its class and its place (`the key 'x[1]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /description/0`), which `load()` and `record()` turn into exit 2. `named()` (`:408-415`) now refuses repeated keys only. The per-site checks this subsumes are removed: `load()`'s endpoint-name line and `shape_problems()`'s policy-figure line. Arms: a bracketed key in an image manifest entry (2) and another named key there (0); a bracketed key in a list inside the file's `description` note (2) and in a `scopes` object inside an endpoint's `measured` note (2), each through `check` and `check-baseline`; a bracketed scope name through `check` (0, new) and `check-baseline` (0); the bracketed endpoint name, policy figure and `record --write` endpoint, with the new reason. Mutants killed (R5.3): `every key named`, `baseline key names` (rewritten onto the walk), `baseline scope names`, `scope names at their path only`, `scope path matched in full`, `names inside lists`, `names below the top level`, and the kept `scope names hold a generate index`. The generator reaches keys inside open objects (R5.4). | R446-4 `probe_r4_structure.py`, unchanged: the two bracketed note cases and the bracketed manifest key give rc 2; the other 29 cases are unchanged against R446-4's published log (`r446-4-structure-compare.txt`: 32 cases, 3 changed, 29 unchanged). The probe prints the manifest case `BAD rc=2 want=0`, because its built-in want of 0 predates ruling (a), under which 2 is required. |
| R446-4 R1: "only missing arguments exit 2 through argparse" | RESIDUE Docs | Item 2, exact fix, in the PR body's Round 4 paragraph: "only a command line that argparse rejects (a missing, unknown or ill-typed argument) exits 2 through argparse, before the barrier". | `PR-BODY.md`, Round 4. |
| R446-4 S1: the docstring's exit-status sentence covers the test modes | SUGGESTION Docs, Robustness | Item 2: the sentence now reads "Exit status of check, record and check-baseline: ..." (`pp_resource_gate.py:22`). | Gate docstring. |
| R447-4 R1: the docstring's barrier sentence is scoped to all of `main()` | RESIDUE Docs | Item 2, exact fix: "For check, record and check-baseline, main() holds one barrier around everything after argument parsing:"; "every line those commands print is printable ASCII"; appended "--selftest and --fuzz are test drivers outside the barrier: a non-zero exit there means the test failed or could not start." (`:24-31`). | Gate docstring. R447-4 `probe_r4_structure.py`: 51 cases, 0 off expectation, rc per case equal to R447-4's published log; its three tracebacks are the `--fuzz` test-mode cases this sentence now describes. |
| R447-4 R2: "holds every case to this contract" claims more than the oracle checks | RESIDUE Docs | Item 2, exact fix: `AREA_BUDGET.md:208` and recipe `:477` now state what `violations()` checks. | The two pages. |
| R447-4 R3: "two bounded converters" | RESIDUE Docs | Item 2, exact fix in the PR body's Description row: "every number goes through one of two converters, whole() (1 to 15 ASCII digits) or real() (a finite float)". | `PR-BODY.md`, Description. |
| R447-4 S1: the oracle could check where exit 1 comes from | SUGGESTION Tests | Not taken (item 3); listed as open in the PR body's limitations. | R447-4 `probe_r4_oracle.py` at this head: 1a and 1b 0 failures with the stricter oracle; 2a the shipped oracle misses the `check-baseline problems exit 1` mutant, 2b the stricter one detects it (42 failures in 2,000); the arms kill it. |
| R447-4 S2: the budget page and manifest numbers, `NaN` and repeated keys are outside the generator | SUGGESTION Tests | Not taken (item 3); listed as open. Item 1's manifest operator writes keys only, so the budget page and the manifest's numbers, `NaN` and repeated keys stay outside the generator. Its keys do reach the `manifest via json.loads` mutant that S2 names: the generated cases alone now detect it (R447-4 `probe_r4_fuzzkill.py`: fuzz500 and fuzz5k DETECTED; round 4: passed). `budget cell via float()` is still missed by them and killed by an arm. | R447-4 `probe_r4_fuzzkill.py`, R5.5. |

### R5.2 The name class by construction

- **One rule, one place.** Round 4 checked the class per site: `named()` held every key to the bracket class, and
  `load()` and `shape_problems()` re-applied `NAME` to endpoint names and policy figures. Open objects fell between
  the sites. Round 5 states the rule once: `strict(text, scopes)` parses (repeated keys, `NaN`, `Infinity` and both
  converters, as in round 4) and then `names()` walks the whole tree. Every key is a `NAME`, except the keys of the
  object at the path `scopes`, which are `SCOPE_NAME`. So a field added to the baseline shape later is covered without
  a new check.
- **The walk.** An explicit stack, so a tree as deep as `json.loads` returns cannot exhaust Python's stack (the arms
  with 100,000 levels are still refused by `json.loads` itself, as `RecursionError`, exit 2). Each object's keys are
  checked before anything below it, so the place a refusal prints holds only names and is printable ASCII.
  The place is the path from the root, keys joined by `/` and list positions as numbers.
- **Where `scopes` matches.** `SCOPES` has `None` for the endpoint name. A path matches only when it has the same
  length and every other element is equal. A `scopes` object inside a note
  (`/endpoints/route/measured/scopes`) is therefore held to `NAME`: an arm plants it, and the mutant that matches on the
  last key alone (`scope path matched in full`) is killed by it.
- **Messages.** A bracketed or otherwise misnamed key reads, for example, `NOT COMPARABLE: baseline <path> is
  unreadable: the key 'x[1]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /endpoints/route-1x1/measured`.
  A scope name reports its own class, with `[ ]`. Round 4's endpoint-name and policy-figure reasons ("the endpoint name
  ... is not 1 to 128", "a tolerance figure is not named by") are gone with their checks; no reviewer probe asserted
  either text (searched in every packet).
- **Self-test:** 254 arms (round 4: 247): 99 route (+2), 8 standalone, 1 relocation, 17 `check` (+1), 27
  `check-baseline` (the bracketed-scope arm now shares the `INDEXED` edit with the new `check` arm), 45 malformed
  baselines through both commands (+2), 7 planted exceptions, a non-ASCII directory, a refused write, `record --write`
  and CARRY4, cross-kind; and 500 generated cases. Correction to R4.2: at `79e53831` the route and malformed-baseline
  arms were 97 and 43, not 96 and 42 (the breakdown predates `79e53831`'s two arms; the total, 247, was right).
- **The 1,000-line module limit.** The self-test would have been 1,008 lines. Nine existing arm entries whose first
  two lines fit in 120 columns were joined (a whitespace-only change; `git diff -w` shows none of it), so the module is
  999 lines and still one of the three modules every reviewer probe copies.

### R5.3 Mutants

- **Shipped campaign:** 162 (153 of the gate, 9 of the hierarchy parser), control passes, all killed
  (`gates/resource-gate-mutants.log`, 3.4 s). Against round 4: `endpoint names` and `policy figure names` removed with
  the lines they mutated; `every key named`, `baseline scope names`, `scope names at their path only`, `scope path
  matched in full`, `names inside lists` and `names below the top level` added; `baseline key names` re-pointed at the
  walk's class check.
- **Name mutants, shipped and adapted** (`name-kill.log`, `scratch-scripts/name_kill_r5.py`). Each runs `fuzz(500,
  234)`, `fuzz(5000, 447)` and `--selftest`. The seven reviewer round-4 mutants whose spans round 5 rewrote are
  re-pointed at the code that now holds the same rule (two pairs share one adapted mutant, so five rows):

| Mutant | fuzz 500 / 5,000 alone | Self-test |
|---|---|---|
| shipped `baseline key names`, `every key named`, `scope names at their path only`, `scope path matched in full`, `names inside lists`, `names below the top level`, `baseline repeated keys`, `baseline keys checked`, `image manifest strict` | DETECTED / DETECTED (all nine) | killed |
| shipped `scope names hold a generate index`, `baseline scope names` | passed / passed | killed |
| adapted R446-4 `strict(): plain json.loads` (no hooks, no walk) | DETECTED / DETECTED | killed |
| adapted R446-4 `named(): no name class`, R447-4 `key name class removed` (the walk's check off) | DETECTED / DETECTED | killed |
| adapted R446-4 `named(): NAME class for every key` (no scope exception) | passed / passed | killed |
| adapted R446-4 `load(): endpoint names not held to NAME`, R447-4 `brackets allowed in endpoint names` | passed / DETECTED | killed |
| adapted R447-4 `policy figure names unchecked` | DETECTED / DETECTED | killed |

  16 mutants: the self-test kills 16, the generated cases alone detect 13. The three they miss make the gate too
  strict, refusing a bracketed scope name. The oracle allows exit 2 for a case that breaks no shape, so only the arms,
  which require exit 0 for a bracketed scope name, can catch those, and they do.
- **The generated cases alone over every shipped mutant** (`fuzz-kill-matrix.log`, 500 cases at seed 234, no arm): 54
  of 162 detected (round 4: 53 of 158). New detections: five of the six new walk mutants (all but `baseline scope
  names`), and `image manifest strict`, `baseline NaN and Infinity` and the re-pointed `baseline key names`. Of the two
  removed, round 4's 500 cases detected `policy figure names` and missed `endpoint names`. Six mutants the round-4 500 cases
  detected are missed at 500 now, because the new operator and the fixture's object notes move the random stream. Five
  are detected at 5,000 cases on two seeds (`fuzz-kill-six-5000-s234.log`, `-s447.log`). The sixth, `count format
  ASCII`, can only be seen through an other-script digit in the half-tile count, and is detected at 20,000
  (`fuzz-kill-count-ascii-20000.log`, 2 failures). The arms kill all six.

### R5.4 The generative test reaches keys inside open objects (item 1)

- `mutate_json()` has a new operator, `note`. It writes a key from `OPEN_KEYS` (two names; brackets, as in `x[1]`,
  `g_rx[5].u` and `]`; and every bad name) into a note of the file or of any endpoint, wrapped as an object, a list or
  a `scopes` object. The case breaks a shape unless the key is one of the two names.
- `mutate_report()` has a manifest operator, `entry key`. It adds a key from the same list to a random entry of
  `baseline_images.json`, with the same rule.
- The self-test fixture's notes are now objects (`description` holds text and a list of runs, `measured` holds a run),
  so every existing key operator (remove, add, rename to a bad or bracketed name, repeat, overflow, digit) also reaches
  keys inside notes. The committed baseline's notes are text, so on a real measurement only `note` reaches them.

| Run (`receipts/round5/fuzz/`) | Cases | rc | Exits 0 / 1 / 2 (`check`) | Shape-breaking cases, all exit 2 | `note` / `entry key` cases (shape-breaking) | Result |
|---|---:|---:|---|---:|---|---|
| Self-test, seed 234, fixtures | 500 | 0 | in `gates/resource-gate-selftest.log` | - | 10 / 7 | 0 failures; case digest `bec87b3c7cbe1125` |
| `fuzz-fixtures-20000.log` | 20000 | 0 | 3607 / 163 / 16232 | 12861 | 547 (470) / 275 (239) | 0 failures; case digest `9c76c8a0b096b5a6` |
| `fuzz-A-route-20000.log` | 20000 | 0 | 4122 / 191 / 15688 | 13602 | 568 (498) / 273 (235) | 0 failures; case digest `5355bf60a587d04c` |
| `fuzz-A-ooc-1x1-5000.log` | 5000 | 0 | 1150 / 25 / 3826 | 3175 | 145 (121) / 79 (71) | 0 failures; case digest `734d9bfa6aabaa08` |

`fuzz-A-route-20000` is A's real route directory against the committed baseline and budget page, and
`fuzz-A-ooc-1x1-5000` A's real standalone 1x1 directory. Counts include one control case per target. The
shape-breaking counts come from `scratch-scripts/replay_broken.py`, which replays each run's generation without the
gate and checks that its per-label totals equal the run's log (`replay-*.log`: equal for all three). Every
shape-breaking `note` and `entry key` case exited 2. The inputs' sha256 are in `fuzz/inputs.sha256`, the head in
`fuzz/head.txt`. R447-4's `run_fuzz.sh` reproduces the case digests of the fixture and standalone runs at seed 234
(R5.5).

### R5.5 Both reviewers' round-4 probes, unchanged

Runners `scratch-scripts/run_probes_r5.sh` (heavy group) and `run_probes_r5b.sh` (light and gates groups; see R5.8),
exported packet `92c0a2d4`, scratch outside the checkout, `PYTHONDONTWRITEBYTECODE=1`, GNU Make 4.3 first on `PATH`.
One log and rc per run under `receipts/round5/probes/`. R447-4's `verify_tree.sh` passed after each group, and `git
status --porcelain --ignored` was empty afterwards.

| Reviewer | Probe | rc | Result at `ec7eb2d8` | Reading |
|---|---|---:|---|---|
| R446-4 | `probe_r4_structure.py` (A route) | 0 | 32 cases, 1 BAD | Item 1's check. Bracketed note keys (file and endpoint) and the bracketed manifest key now give rc 2; the other 29 cases are unchanged against R446-4's log (`r446-4-structure-compare.txt`). The one BAD is the manifest case, rc 2 against the probe's pre-ruling want of 0. |
| R446-4 | `probe_r447_3_cases.py` (B route) | 0 | 9 cases, 0 not as expected | |
| R446-4 | `probe_r4_adhoc.py` | 0 | 0 not as expected | All six rankings byte-equal to the published TSVs; all six `armq_r` census rows and digests equal the round-4 packet's. |
| R446-4 | `probe_r4_generative.py --jobs 8` | 0 | 22 runs, 2 BAD, 4 not applied | BAD: the two barrier-narrowing mutants, which no generated case reaches and the self-test kills, as in round 4. Not applied, because round 5 rewrote their spans: `strict(): plain json.loads`, `named(): no name class`, `named(): NAME class for every key`, `load(): endpoint names not held to NAME`; each re-pointed in R5.3 and killed. Round 4's third BAD (`named(): NAME class for every key`, missed by the cases) is among them. |
| R447-4 | `probe_r4_structure.py` (A route, A 1x1) | 0 | 51 cases, 0 off expectation | rc per case equal to R447-4's published log. The three tracebacks are the `--fuzz` test-mode cases of R1. |
| R447-4 | `probe_r4_resolution.py` (A, B) | 0 | 0 off expectation | |
| R447-4 | `probe_r4_oracle.py` | 0 | 1a, 1b 0 failures; 2a 0; 2b 42 failures; 3 117 failures | As R447-4 found: the stricter oracle is sound at this head and detects `check-baseline problems exit 1` (S1, open). |
| R447-4 | `probe_r4_fuzzkill.py` (12 jobs) | 0 | 23 mutants: 20 applied, all killed by the self-test; 3 NOT-UNIQUE | Not unique: `key name class removed`, `brackets allowed in endpoint names`, `policy figure names unchecked`; spans rewritten, re-pointed in R5.3 and killed. One change from R447-4's log: `manifest via json.loads` is now DETECTED by the cases alone (S2). |
| R446-4 | `run_prior_probes.sh` light, mutants, reasons | 0 | as in R446-4's table | `probe_gate_cli` 116 of 117 (the `inf` case, rc 2 as ruled); `probe_gate_mutants` 21 killed, 0 survived, 2 not applied (as round 4); `probe_pr_mutant_reasons` 153 of 153 ARM; `reconcile` 2 mismatches (its round-1 sentences); `partition_rederive` 0; `probe_extra_mutants` every applicable mutant KILLED, 3 not applicable (as round 4); `probe_malformed_record` 0 not exit 2; `probe_policy_pin` 0 not as expected; `probe_route_status` 15 of 16 (the declined S1 layout); `probe_r3_mutants` 20 of 20 KILLED; `probe_r3_numbers`, `probe_r3_untested`, `probe_r447_2_cases` 0 off contract; `probe_hierarchy_equiv` 0 mismatches. |
| R447-4 | `reruns.sh` light, heavy | 0 | as in R447-4's table | `check_tables` 49 groups, 0 mismatches; `partition_check` and `partition_r2` +79 / 391 / +93, `u_pp` -23 / +107; `probe_cli` 54 of 54; `probe_route_status` clean exit 2, 37 unrouted exit 2; `replay_records` A 0/0/0, B 1/0/0, 10 ns 2; `probe_contract`, `probe_bigint` A and B, `probe_gaps`, `probe_text` every case rc 2; `probe_policy` 107 of 107; `probe_route_real` A 15 of 15, B 14 of 15 (B's own +625 LUT); `armq_count` A 1,153, B 1,260, A-8x8 1,318; `hier_compare` 7 reports, 0 differing; `extra_mutants` 16 killed, 2 not unique (as round 4); `classify_mutants` 149 ARM, 4 ESCAPED, 0 survived, of 153; `extra_mutants_r3` 13 of 13 KILLED. |
| R446-4 | `run_gates.sh` | 0 | 31 of 31 jobs rc 0 | Markdown environment's interpreter and GNU Make 4.3 first on `PATH`. |
| R447-4 | `run_fuzz.sh` | 0 | 6 runs, 90,000 cases, 0 failures, no traceback | Seed 234 reproduces this round's case digests: fixtures `9c76c8a0b096b5a6`, A route `5355bf60a587d04c`, A 1x1 `734d9bfa6aabaa08`. Seed 4474: fixtures `a11a378a10ba0a90`, A route `0137ba98eeae4cca`, A 8x8 (5,000) `5f669519439856cf`. |
| R447-4 | `verify_tree.sh` | 0 | PASS after each group | |

### R5.6 Real data through the gate (no Vivado; existing run directories)

| Receipt (`receipts/round5/`) | rc | Result |
|---|---:|---|
| `real/gate-check-A-route.log` | 0 | LUT 50128 50128 0 ok; route status: complete, no unrouted net and no routing error; RESULT: PASS |
| `real/gate-check-A-ooc-1x1.log` | 0 | LUT 24343 24343 0 ok; RESULT: PASS |
| `real/gate-check-A-ooc-8x8.log` | 0 | LUT 31562 31562 0 ok; RESULT: PASS |
| `real/gate-check-B-route.log` | 1 | LUT 50128 50753 625 REGRESSION: grew by more than 500; route status: complete; RESULT: MATERIAL REGRESSION |
| `real/gate-check-B-ooc-1x1.log` | 0 | LUT 24343 24505 162 ok; RESULT: PASS |
| `real/gate-check-B-ooc-8x8.log` | 0 | LUT 31562 31390 -172 ok, below the baseline; RESULT: PASS |
| `real/gate-check-A-ooc-1x1-10ns.log` | 2 | NOT COMPARABLE: tool or recipe change in standalone_clock_ns |

The committed baseline passes the validator unchanged (`check-baseline`: "baseline PASS: 3 endpoints").

### R5.7 Gate table

`$MDPY` = `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`. Each command ran in the foreground of the runner from
the lane root (physical `/data` path), without a pipeline; `docs-check-no-git` and `feature-status-no-git` set
`GIT_DIR=/dev/null`. Machine record: `receipts/round5/gates/gate-results.json`; runner `scratch-scripts/run_gates_r5.py`,
driven by `scratch-scripts/run_all_r5.sh` in the background with its own log and rc file. The list is round 4's,
a superset of the gates the change touches.

Head `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5`, worktree clean: True; `GNU Make 4.3` first on `PATH`.

| # | Gate | Command | rc | Seconds | Receipt |
|---:|---|---|---:|---:|---|
| 1 | dp-srcs-selftest | `python3 syn/ooc/dp_srcs.py --selftest` | 0 | 14.6 | [receipts/round5/gates/dp-srcs-selftest.log](receipts/round5/gates/dp-srcs-selftest.log) |
| 2 | ooc-tcl-selftest | `python3 syn/ooc/ooc_tcl_selftest.py` | 0 | 501.7 | [receipts/round5/gates/ooc-tcl-selftest.log](receipts/round5/gates/ooc-tcl-selftest.log) |
| 3 | pp-baseline-selftest | `python3 syn/ooc/pp_baseline.py --selftest` | 0 | 0.1 | [receipts/round5/gates/pp-baseline-selftest.log](receipts/round5/gates/pp-baseline-selftest.log) |
| 4 | pp-baseline-mutants | `python3 syn/ooc/pp_baseline_mutants.py` | 0 | 2.7 | [receipts/round5/gates/pp-baseline-mutants.log](receipts/round5/gates/pp-baseline-mutants.log) |
| 5 | pp-baseline-reports-selftest | `python3 syn/ooc/pp_baseline_reports_selftest.py` | 0 | 0.0 | [receipts/round5/gates/pp-baseline-reports-selftest.log](receipts/round5/gates/pp-baseline-reports-selftest.log) |
| 6 | resource-gate-selftest | `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | 1.6 | [receipts/round5/gates/resource-gate-selftest.log](receipts/round5/gates/resource-gate-selftest.log) |
| 7 | resource-gate-mutants | `python3 syn/ooc/pp_resource_gate_mutants.py` | 0 | 3.4 | [receipts/round5/gates/resource-gate-mutants.log](receipts/round5/gates/resource-gate-mutants.log) |
| 8 | resource-gate-check-baseline | `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | 0.1 | [receipts/round5/gates/resource-gate-check-baseline.log](receipts/round5/gates/resource-gate-check-baseline.log) |
| 9 | dp-srcs-milan-datapath | `python3 syn/ooc/dp_srcs.py --top milan_datapath` | 0 | 7.7 | [receipts/round5/gates/dp-srcs-milan-datapath.log](receipts/round5/gates/dp-srcs-milan-datapath.log) |
| 10 | dp-srcs-kl-pp-shadow | `python3 syn/ooc/dp_srcs.py --top KL_pp_shadow` | 0 | 5.4 | [receipts/round5/gates/dp-srcs-kl-pp-shadow.log](receipts/round5/gates/dp-srcs-kl-pp-shadow.log) |
| 11 | pp-srcs-check-selftest | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.3 | [receipts/round5/gates/pp-srcs-check-selftest.log](receipts/round5/gates/pp-srcs-check-selftest.log) |
| 12 | docs-check | `$MDPY scripts/docs_check.py` | 0 | 4.7 | [receipts/round5/gates/docs-check.log](receipts/round5/gates/docs-check.log) |
| 13 | docs-check-no-git | `$MDPY scripts/docs_check.py` | 0 | 4.7 | [receipts/round5/gates/docs-check-no-git.log](receipts/round5/gates/docs-check-no-git.log) |
| 14 | feature-status-no-git | `$MDPY scripts/check_feature_status.py` | 0 | 0.9 | [receipts/round5/gates/feature-status-no-git.log](receipts/round5/gates/feature-status-no-git.log) |
| 15 | feature-status-selftest | `$MDPY scripts/check_feature_status.py --self-test` | 0 | 0.8 | [receipts/round5/gates/feature-status-selftest.log](receipts/round5/gates/feature-status-selftest.log) |
| 16 | em-dash | `$MDPY scripts/check_em_dash.py --base 1269cdafb4bb964c757baae0f0c5a932d43f540b` | 0 | 3.3 | [receipts/round5/gates/em-dash.log](receipts/round5/gates/em-dash.log) |
| 17 | em-dash-selftest | `$MDPY scripts/check_em_dash.py --selftest` | 0 | 3.3 | [receipts/round5/gates/em-dash-selftest.log](receipts/round5/gates/em-dash-selftest.log) |
| 18 | doc-style | `$MDPY scripts/check_doc_style.py` | 0 | 0.1 | [receipts/round5/gates/doc-style.log](receipts/round5/gates/doc-style.log) |
| 19 | doc-style-selftest | `$MDPY scripts/check_doc_style.py --selftest` | 0 | 0.0 | [receipts/round5/gates/doc-style-selftest.log](receipts/round5/gates/doc-style-selftest.log) |
| 20 | doc-paths | `$MDPY scripts/check_doc_paths.py` | 0 | 0.1 | [receipts/round5/gates/doc-paths.log](receipts/round5/gates/doc-paths.log) |
| 21 | toc-selftest | `$MDPY scripts/gen_toc.py --selftest` | 0 | 0.8 | [receipts/round5/gates/toc-selftest.log](receipts/round5/gates/toc-selftest.log) |
| 22 | toc-verify-anchors | `$MDPY scripts/gen_toc.py --verify-anchors` | 0 | 2.7 | [receipts/round5/gates/toc-verify-anchors.log](receipts/round5/gates/toc-verify-anchors.log) |
| 23 | toc-check | `$MDPY scripts/gen_toc.py --check` | 0 | 4.0 | [receipts/round5/gates/toc-check.log](receipts/round5/gates/toc-check.log) |
| 24 | archive | `$MDPY scripts/check_archive.py` | 0 | 0.4 | [receipts/round5/gates/archive.log](receipts/round5/gates/archive.log) |
| 25 | archive-selftest | `$MDPY scripts/check_archive.py --selftest` | 0 | 0.1 | [receipts/round5/gates/archive-selftest.log](receipts/round5/gates/archive-selftest.log) |
| 26 | doc-map-check | `$MDPY docs/DOC_MAP.gen.py --check` | 0 | 0.5 | [receipts/round5/gates/doc-map-check.log](receipts/round5/gates/doc-map-check.log) |
| 27 | module-matrix-check | `$MDPY docs/traceability/gen_module_matrix.py --check` | 0 | 1.0 | [receipts/round5/gates/module-matrix-check.log](receipts/round5/gates/module-matrix-check.log) |
| 28 | solution-docs | `$MDPY scripts/check_solution_docs.py` | 0 | 0.1 | [receipts/round5/gates/solution-docs.log](receipts/round5/gates/solution-docs.log) |
| 29 | baremetal-only | `python3 scripts/check_baremetal_only.py --check` | 0 | 22.9 | [receipts/round5/gates/baremetal-only.log](receipts/round5/gates/baremetal-only.log) |
| 30 | gptp-docs-make | `make -C gptp-processor docs` | 0 | 0.9 | [receipts/round5/gates/gptp-docs-make.log](receipts/round5/gates/gptp-docs-make.log) |
| 31 | ci-scope-selftest | `python3 scripts/ci_scope.py --selftest` | 0 | 4.2 | [receipts/round5/gates/ci-scope-selftest.log](receipts/round5/gates/ci-scope-selftest.log) |
| 32 | ci-events-check | `python3 scripts/ci_events.py --check` | 0 | 0.2 | [receipts/round5/gates/ci-events-check.log](receipts/round5/gates/ci-events-check.log) |
| 33 | ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | 17.8 | [receipts/round5/gates/ci-events-selftest.log](receipts/round5/gates/ci-events-selftest.log) |
| 34 | py-idiom | `python3 scripts/check_py_idiom.py` | 0 | 3.8 | [receipts/round5/gates/py-idiom.log](receipts/round5/gates/py-idiom.log) |
| 35 | py-idiom-selftest | `python3 scripts/check_py_idiom.py --selftest` | 0 | 3.6 | [receipts/round5/gates/py-idiom-selftest.log](receipts/round5/gates/py-idiom-selftest.log) |
| 36 | fail-fast | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.5 | [receipts/round5/gates/fail-fast.log](receipts/round5/gates/fail-fast.log) |
| 37 | hygiene | `python3 scripts/check_hygiene.py --check` | 0 | 0.4 | [receipts/round5/gates/hygiene.log](receipts/round5/gates/hygiene.log) |
| 38 | todo-ownership | `python3 scripts/check_todo_ownership.py` | 0 | 1.5 | [receipts/round5/gates/todo-ownership.log](receipts/round5/gates/todo-ownership.log) |
| 39 | test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | 6.1 | [receipts/round5/gates/test-evidence.log](receipts/round5/gates/test-evidence.log) |
| 40 | control-flow-selftest | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.1 | [receipts/round5/gates/control-flow-selftest.log](receipts/round5/gates/control-flow-selftest.log) |
| 41 | cohesion-selftest | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.1 | [receipts/round5/gates/cohesion-selftest.log](receipts/round5/gates/cohesion-selftest.log) |
| 42 | diff-check-base | `git diff --check 1269cdafb4bb964c757baae0f0c5a932d43f540b HEAD` | 0 | 0.0 | [receipts/round5/gates/diff-check-base.log](receipts/round5/gates/diff-check-base.log) |
| 43 | diff-check-worktree | `git diff --check` | 0 | 0.0 | [receipts/round5/gates/diff-check-worktree.log](receipts/round5/gates/diff-check-worktree.log) |

43 gates, 0 non-zero.

Not run, as in rounds 1 to 4 (nothing they execute changed): `scripts/run_all_suites.sh`, `syn/yosys/run.sh`,
`scripts/lint_rtl.py`, `scripts/xvlog_gate.py`, the Yosys self-tests, the builder bank, and `scripts/act_ci.py
--selftest` (AGENTS.md section 5).

### R5.8 Notes and deviations

- **Reviewer spans rewritten.** Round 5 moves the class check out of `named()` and removes two per-site checks. So
  seven reviewer round-4 mutants no longer apply (four in R446-4's generative probe, three in R447-4's fuzzkill). Each
  is re-pointed at the code that now holds its rule, and killed, in `name-kill.log` (R5.3). That run is mine; the
  reviewers' scripts ran unchanged.
- **Wording of a misnamed key.** It is refused while reading strict JSON, so the baseline reason reads "is
  unreadable: the key ..."; round 4's endpoint-name and policy-figure reasons read "is malformed". Both exit 2 with the
  key named. The image manifest's reads "unreadable measurement ...: ValueError: the key ...", as its repeated-key
  refusal did in round 4.
- **A defect in my scratch runner, fixed.** `run_probes_r5.sh` deleted `receipts/round5/probes/` at the start of
  every group, so starting the heavy group removed the first light run's receipts (its console log is kept as
  `run-probes-light-first-run-receipts-deleted.log`; every rc was 0). The light group was rerun with
  `run_probes_r5b.sh`, which only creates directories, and the gates group used it too. The tables report the rerun.
- **Self-test layout:** nine existing arm entries joined onto fewer lines (R5.2); no arm dropped, none changed in
  data. The fixture's timing table and every text reviewer probes plant are unchanged.
- No push, PR edit, merge, rebase, sub-agent, other checkout, hardware, flashing, processor or interface change. No
  existing comment edited. Scratch and run directories stay under `$VALIDATION_STORAGE/234-a516`.
