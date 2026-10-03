[A516]

# Handoff: issue #234, the #229 area baseline, ranking, budget and gate

Status: REVIEW READY at `2a765a6c3868400c20ede2e357876f28a811c811` (not pushed; no PR opened).

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
