# [A503] Issue #635 handoff: adopt protocol-processor `main` `631eeb34`

Status: REVIEW READY at `3370c6cbd5e4b096167c19ca709556a40207e538` (local; not pushed). Items 1 to 5 are committed and every gate listed in section 6 is rc 0 at that head.

- Repository: kebag-logic/milan-fpga, branch `635-pp-pin-631eeb34` from dev `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- Assignment: issue #635 comment 5958619779. TAKEN: comment 5958652460. REVIEW READY: comment 5962152491.
- Patch: `parent-adoption-c4c6-ea3fb388.patch`, sha256 `67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c`.
- Nothing was pushed, no PR was opened, and no issue or PR comment was edited.

## Commits, in item order

| # | Commit | Item | Subject |
|---:|---|---|---|
| 1 | `14f8c27fa26062bb3e7c2101097fb31efeceb72f` | 1 | Pin the protocol processor at 631eeb34 (processor PRs #135 to #140 and #142) |
| 2 | `c4bf64e2fc8e6b51ea631bbe19878b114206fa52` | 2 | Record the C4 acmp_mutants.py campaign as a disposed DUT-source reader in the test-evidence ratchet |
| 3 | `15933a60cb0624ab57cde0a8160cb8677ccc3268` | 2 | Tie the processor's C6 identify_button_i to 0 and bind EN_IDENTIFY_NOTIF_P at 0 in KL_pp_shadow |
| 4 | `927428d161eae953265797409e4c620cfc870400` | 2 | Record the C6 notify_mutants.py campaign as a disposed DUT-source reader in the test-evidence ratchet |
| 5 | `3c68c6b1ca3b8b6a0ea01f9abce85725511cb033` | 3 | Re-record the ROM digest ledger at protocol-processor pin 631eeb34 with ooc.sh --record-rom-digests |
| 6 | `81a80dd63573fff008cfd00bfc3ebdced15d0fa1` | 3 | Regenerate the submodule boundary diagram at protocol-processor pin 631eeb34 |
| 7 | `46ed4e913c5417296f703c69a14fb2776e42c1b5` | 3 | Re-record the port-contract ratchet at protocol-processor pin 631eeb34: three scoreboard kill-face tie-offs left the processor top |
| 8 | `216d6febaa9c02b5bf57b3ed965324abc4d395bc` | 3 | Re-record the boundary-unit naming ratchet at protocol-processor pin 631eeb34 |
| 9 | `eb7758756cc3e511789300fb42ab5f40a6917036` | 3 | Record protocol-processor pin 631eeb34 and the seven merged processor lanes it carries in the submodule ledger |
| 10 | `2087ee76f13504d6ea040bce5f3823b9c70699aa` | 5 | Record what the parent can observe of processor pin 631eeb34: the identify tie-off, the C5a deadline and hazard faces and the other lanes |
| 11 | `2ed1f7e4291693ebedbf6193cbca69a6f189de80` | 5 | Mark #629's protocol-processor changes landed at 631eeb34 with the D3C tests that carry them |
| 12 | `3370c6cbd5e4b096167c19ca709556a40207e538` | 5 | Record processor pin 631eeb34's parent-observable changes in the changelog |

Item 4 (saved state) needed no commit: the capture check passes unchanged (section 4).

## 1. The pin change

- `protocol-processor` gitlink `b2db3a970cedbbff2f8ba813acb96122c442bc58` -> `631eeb342ca1e3fa80e734077a56a943aee76ff1`. It is the only processor change: the submodule checkout is clean at `631eeb34` (`git submodule status`, leading space; `git status --short` empty).
- The commit was fetched from `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git` inside `protocol-processor`, after checking that `git -C protocol-processor rev-parse --show-toplevel` is that directory. The parent's `origin` is unchanged.
- `b2db3a97` is an ancestor of `631eeb34`. First-parent history `b2db3a97..631eeb34`:

| Lane | Processor PR | `main` after merge |
|---|---|---|
| C3 (ADP) | #136 | `0451d83d` |
| C2 (MAAP) | #135 (the issue's table shows "-") | `d5f73bac` |
| C4 (ACMP) | #137 | `3f3ea56b` |
| C5b (AECP dispatch and responses) | #138 | `16ea10ac` |
| C5a (AECP deadlines and hazards) | #140 | `03c842a7` |
| C6 (notifications and Identify) | #139 | `2ebd4fe8` |
| P141 (SET/GET_CLOCK_SOURCE, #629) | #142 | `631eeb34` |

- `631eeb34`'s tree is `877a0f78e3b6f15c1159899c10d7ba5e3ca3c836`, the same tree as PR #142's round-2b head `a90ca735`, so that round's line table applies at the pin.

### Records the pin change re-records

| Record | How | Result |
|---|---|---|
| `syn/yosys/rom_digests.tsv` | `cd syn/yosys && ./ooc.sh --record-rom-digests` (rc 0; the way `syn/yosys/README.md` and `ooc.sh` document it) | two rows added for `631eeb34`: `ltn_rom.hex` `23cc67ee...e956` (equal to the `b2db3a97` row), `ucode.hex` `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8` (moves; equal to PR #142's ROM map for `main`); every other pin's rows retained; the gPTP row for `5dce647a` already existed |
| `docs/diagrams/submodule_boundaries.{svg,drawio,png}`, `docs/diagrams/PNG_MANIFEST.json` | `python3 docs/diagrams/submodule_boundaries.gen.py` (`--check` rc 1 before, rc 0 after) | the protocol-processor node reads `pin 631eeb342ca1`; PNG 323,884 -> 323,340 bytes, manifest raster and source digests re-recorded by the generator |
| `scripts/port_docs.budget` | `python3 scripts/check_port_contracts.py --write-budget` | the gate reported "the ratchet can be lowered ... 3 recorded connection(s) gained a rationale or left". Removed: `protocol-processor:hdl/top/protocol_processor_top.sv:u_scoreboard.kill_id_i`, `.kill_resp_queued_i`, `.kill_valid_i` (C5a now drives the kill face). Header: ports per tree hdl 1916, gptp-processor 125, protocol-processor 1757; unjustified protocol-processor 7 -> 4. Undocumented ratchets unchanged (111 <= 111 for the processor) |
| `scripts/naming.budget` | `python3 scripts/measure_naming.py --write-budget` | the identity rows are unchanged (96 recorded, all candidates); only the generated count line moves from "95 candidate(s) ... protocol-processor 21" to "96 ... protocol-processor 22". The base's own count was not re-measured here (it would need the processor checked out at `b2db3a97`) |
| `docs/reference/SUBMODULES.md` | not a generated file: the pin table between the `submodule-pins` markers is verified by `scripts/check_submodule_docs.py`, and every earlier adoption edited it the same way | pin row -> `631eeb34...`; "Issue #70 lane 2 adopted"; a new "Issue #635 adopts processor pin `631eeb34`" table of the seven lanes; the ROM ledger note |

Not re-recorded, on purpose:

- `scripts/test_evidence.budget`: `measure_test_evidence.py --check` passes 72 <= 77 and prints "the mutation ratchet can be lowered to 72". The file has no generator (it is hand-lowered to the tool's figure), the assignment's record list does not name it, and the processor PRs call the lowering optional ("that is the parent's edit"). Left at 77 for a ruling.
- `tb/verilator/nvm_capture_cpu/measurements.json` and the provenance lines in `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1626`, `docs/findings/397_SERVICE_BUDGET.md:40`: they record the processor pin a past measurement ran at. The capture check (section 4) says the census and firmware are unchanged, so nothing is re-measured.

## 2. Patch hunks

The patch was split into its three concerns and committed one per concern. The combined result is byte-identical to `git apply` of the whole patch on dev `cdf49d1a` (blobs `46f3faf8ef66d34ab2f5a1cd60b4cfbc39bc02d0` and `b33d91c6f9bfc5dda8f8def0be5e269933ccc5a7`, which are also the patch's `index` lines), and `git diff 14f8c27fa 927428d16 | git patch-id --stable` equals the patch's own patch-id (`791277578ee8659a7daaec098a841e6df070f31d`).

| Commit | File:line (at the head) | Hunk | Processor change it answers |
|---|---|---|---|
| `c4bf64e2f` | `scripts/measure_test_evidence.py:597-600` | `DUT_READER_DISPOSITIONS` entry for `protocol-processor/tb/pp_top/acmp_mutants.py` | C4, PR #137 (`3f3ea56b`): the new ACMP mutation driver reads DUT sources; without the entry `measure_test_evidence.py --check` fails with 1 unexplained DUT-source reader (PR #137 round 2 item 2, PR #138 round 3, PR #140 round 3) |
| `15933a60c` | `hdl/milan/KL_pp_shadow.sv:1097-1100` | `.EN_IDENTIFY_NOTIF_P (1'b0)` with a `//!` rationale | C6, PR #139 (`2ebd4fe8`): the top gains parameter `EN_IDENTIFY_NOTIF_P` (default 0); bound explicitly at 0 until a debounced board button exists (ruling on processor #80) |
| `15933a60c` | `hdl/milan/KL_pp_shadow.sv:1138-1140` | `.identify_button_i (1'b0)` with a `//!` rationale | C6, PR #139: the top gains input `identify_button_i`; without the tie-off `lint_rtl.py --check` fails on a new PINMISSING (PR #139 "Measured need") |
| `927428d16` | `scripts/measure_test_evidence.py:601-604` | `DUT_READER_DISPOSITIONS` entry for `protocol-processor/tb/pp_top/notify_mutants.py` | C6, PR #139: the new notification/identify mutation driver; without it the evidence ratchet fails with 1 unexplained DUT-source reader |

## 3. Re-recorded records

See "Records the pin change re-records" above.

## 4. Saved state: capture check

`python3 scripts/check_nvm_capture.py`: rc 0, "PASS: capture census, clocks, both timing arms and receipt agree"; all seven controls detected.

- Census at the head equals the receipt's `measured_for`: `endstation_ax7101_8x8` 12,634 raw bytes, 156 records; `endstation_ax7101_1x1_tdm8` 3,218 bytes, 53 records; CPU 50 MHz (configured 50 MHz), system 100 MHz.
- Product firmware `sw/firmware/milan_baremetal/milan_baremetal.c` sha256 `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`, equal to the receipt.
- Neither moved, so no re-measure. Recorded 8x8 maximum: 13.23352 ms at 50 MHz (margin 3.70) and 9.95772 ms at 100 MHz, below the 24.5 ms STOP line.

## 5. What the parent can observe

| Observable | Where recorded |
|---|---|
| The identify input tied off, and the parameter at 0 | `hdl/milan/KL_pp_shadow.sv:1097-1100`, `:1138-1140` (the `//!` rationales); `docs/reference/SUBMODULES.md` parent-observable table; `CHANGELOG.md` |
| Integrator diagram 21 | The parent does not mirror it: no parent file copies `21-integration-faces`; the only reference is a pinned-commit link (`16be6768`) in `docs/design/SAVED_STATE_MATERIALIZATION.md:2358`'s historical plan. Recorded as such in `SUBMODULES.md` |
| C5a deadline and hazard faces | No top port or parameter. The kill ports (`dl_kill_i`, `dl_queued_o`, `preempt_i`, `preempt_upc_i`, `preempted_o`) are on `KL_aecp_engine` and `KL_aecp_ucpu`, which the parent never instantiates (only comments name them). Parent-visible effects: the 100 ms deadline answer, the NOT_IMPLEMENTED echo for non-AEM messages on that path, AECP/ACMP serialization by hazard class, and the three scoreboard kill tie-offs leaving the port-contract inventory. Recorded in `SUBMODULES.md` and `CHANGELOG.md` |
| The clock-source tests behind #629 | `docs/design/MEDIA_CLOCK_FOLLOWING.md`, "Protocol-processor changes": "Status: landed at `631eeb34`", naming D3C1 to D3C4 in `protocol-processor/tb/pp_top`, the six mutants, and the line citations at `631eeb34` (`gen_ucode.py:1654-1663`, `:1674-1711`). The page header now says the processor citations are at the "then-pinned" `b2db3a97` |

## 6. Gates

All at the committed head `3370c6cbd5e4b096167c19ca709556a40207e538` (tree clean before and after every gate; `git status --short` empty), from the physical path `$LANES/635-pp-pin`, never piped, each with its own log and rc file. The live remote `dev` tip was still `cdf49d1a` when checked (`git fetch origin dev`), so the branch descends directly from the unchanged base and its tree is the candidate merge tree.

Tools: Verilator 5.050 (the CI pin, a local build first on `PATH`); Yosys 0.66; `sv2v` v0.0.12 (the docs workflow's pinned release, verified by its sha256) except under `syn/yosys/run.sh`, which prepends `$HOME/.local/bin` and so ran `sv2v` v0.0.13; Python 3.14.7; host GNU Make 4.4.1; GNU Make 4.3 built from `make-4.3.tar.gz` (sha256 `e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19`, the recipe in `make43_checks.sh`), binary sha256 `03aa26a7317c75964a7249f91fff38d33f539df9525d51dfc941b320ce677c26`; Vivado 2026.1 `xvlog` for the xvlog gate.

### The 16 consumer commands (host make 4.4.1)

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, 0 in `hdl/`, 4 in the pinned processors (the same four), pinned at `protocol-processor@631eeb34`. First run beside the Yosys gate and the builder test; re-run alone (182 s, no other build of this lane running), same verdict |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | 107 files in the `milan_datapath` closure, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 6 | `python3 sw/builder/test_builder.py` (whole, one run, 1,083 s) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11, the calibration gate, needs a local mf48 board build tree |
| 7 | `make -C tb/verilator/pp_shadow -j16` | 0 | 606, 606, 646 and 311 checks, 0 failures |
| 8 | `python3 scripts/check_port_contracts.py` | 0 | 3,798 ports (processor 1,757); undocumented hdl 217 <= 217, gptp 19 <= 19, processor 111 <= 111; 59 without a rationale, all recorded |
| 9 | `python3 scripts/measure_naming.py --check` | 0 | 96 candidates, all recorded |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | 72 <= 77 suites without a mutation arm, 10 <= 10 unseeded draws, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock files; "can be lowered to 72" |
| 11 | `python3 scripts/docs_check.py` | 0 | 0 findings |
| 12 | `make -C tb/verilator/nvm_cosim lint` | 0 | pass |
| 13 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 14 | `make -C tb/verilator/milan_dp -j16` (one run, 1,609 s) | 0 | 9 RESULT PASS, none failing: `sim` 235, `notify` 382, `crflic` 416, `nxn` 1,845, `nxndv` 1,847, `nxn8` 3,525, `nxn4c` 1,845, `nolpf` 235, `prune` 33, `ax1x1` 232, `aclk` 191; prerequisites `gmstep` 104, `gptp` 182, `gptplat` 182; `render_mutants.py` 6/6, `gmstep_mutants.py` 6/6 |
| 15 | `make -C tb/verilator/milan_dp_render -j16` | 0 | 65 and 152 checks, 0 failures; leg defects 5/5 |
| 16 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |

### The rest of the local bar

| Gate | rc | Result |
|---|---:|---|
| `scripts/run_all_suites.sh <logs>` with `MAKEFLAGS=-j16` (5,194 s) | 0 | 57 of 57 suites passed, 0 failed, 0 timed out; 2,147,149 checks, 0 in-suite failures; preflight self-tests (suite cancellation, containment, review integrity, xvlog self-test, tally) pass. 4 declared skips, all `tsn_fuzz` without the tsn-gen oracle (the suite skips by design; hosted shard 1 builds the oracle). A first attempt stopped in preflight (rc 2): its hard-HUP cancellation control timed out because that launch ran under `nohup`, which ignores SIGHUP; relaunched without it, the control passed |
| `syn/yosys/run.sh` (747 s) | 0 | 54 tops, 54 pass, 0 fail; the `milan_datapath` tied-off input inventory and the tap-purity structural check pass |
| `scripts/run_all_suites.sh <logs> --physical-gptp` with `VERILATOR_JOBS=4`, then `suite_tally.py ... --physical-gptp` (the nightly `rtl.yml` job) | 0 | 1 of 1 suite, 179 checks, 0 failures: `ax1x1gptp physical` 139, setup abort 6, no-TX accounting 20, no-Pdelay accounting 14; driver wall 3,982.59 s, exit 0; `suite_tally.py --physical-gptp` 179, 0 failures. The suite README says 137 physical and 177 in total, but the hosted nightly run on dev `cdf49d1a` (run 36976503884) already counted 139 physical checks with 0 failures, so that figure is stale at the base and is not this lane's. That hosted job timed out at its 5,400 s deadline (exit 92), on dev, before this lane |
| `python3 scripts/check_nvm_capture.py` | 0 | PASS (section 4) |
| `cd syn/yosys && ./ooc.sh --record-rom-digests` | 0 | recorded; the commit is that output |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check`, `scripts/check_submodule_docs.py` | 0, 0 | 4 exact gitlinks, decoded PNG |

### `docs.yml`, every step as the workflow runs it, GNU Make 4.3 first on `PATH`

Each step ran in its own `bash -e` from `$LANES/635-pp-pin`, the commands exactly as the workflow spells them. Steps that invoke `make` themselves are marked (make): `make -C gptp-processor docs`, the builder's make probes and `make -s print-srcs`, `check_rtl_source_lists.py`'s consumer expansions and `check_entity_shape.py`'s `make -pqrR` inventory, all under make 4.3.

| Step (workflow name) | rc | Result |
|---|---:|---|
| Build the validated HDL reference | 0 | self-test and HTML build (`pyslang` 11.0.0 installed from the hash-locked `tools/hdl_reference/requirements.txt` into a scratch target) |
| Link health, wording, dead-reference and local-info gate | 0 | 0 findings |
| Added-line em-dash gate (pull_request form: `git fetch origin dev`, merge base `cdf49d1a`) | 0 | 0 findings over 63 added lines in 3 pages, arms 339/339 |
| Concise audience documentation gate | 0 | 22 documents OK; gPTP docs and both self-tests |
| Audience diagram no-drift gate | 0 | |
| Product solution source-fact gate | 0 | |
| Verified submodule documentation gate | 0 | |
| HDL timing diagram no-drift gate | 0 | |
| Published diagram PNG gate | 0 | |
| Milan feature-status consistency gate | 0 | |
| Traceability matrix no-drift gate | 0 | |
| Imported gPTP documentation gate (make) | 0 | `make -C gptp-processor docs` under make 4.3 |
| Code-quality measurement self-tests | 0 | |
| Bare-metal scope gate | 0 | 0 findings, 700 arms |
| Install and verify the pinned RV32 SDK | 0 | self-test; `ci_rv32_sdk.py` given a fresh `--destination` under the lane's scratch, as its docstring requires off a CI runner (the home SDK tree carries no receipt and is never replaced) |
| Compiler-absent firmware controls (make) | 0 | |
| End-station builder gates: `test_builder.py --require-rv32` (make, 1,140 s) | 0 | ALL GATES PASS EXCEPT 2 NOT RUN: gate 11 (board build tree), and gate 1b's `MAKEFLAGS += -e` mutation, which make 4.3 does not honour (the builder measures this and says so, as on the hosted runner); compiler `riscv32-linux-gcc` 14.3.0 at `$HOME/br-milan-rv32/host` |
| NVM record-space gate | 0 | |
| Capture measurement census and clock gate | 0 | |
| Saved-state writer gate | 0 | |
| SoC source-list gate | 0 | |
| RTL source-list drift gate (make) | 0 | |
| Boundary-unit naming ratchet | 0 | |
| Port contract gate | 0 | |
| Fail-fast ratchet | 0 | |
| TODO ownership gate | 0 | |
| Test-evidence ratchet | 0 | |
| Mechanical hygiene ratchet | 0 | |
| SystemVerilog idiom gate | 0 | |
| C and C++ idiom gate | 0 | |
| Python idiom gate | 0 | |
| Shell idiom gate | 0 | |
| CI event and SHA contract gate | 0 | |
| Local act runner contract gate | 0 | run as `python3 -I <audited install>/act_ci.py --selftest --worktree <candidate>` from the audited install whose sha256 `79579e6b...38f8` equals dev `cdf49d1a`'s `scripts/act_ci.py` (unchanged on this branch): AGENTS.md section 5 forbids host execution of the candidate's copy |
| Doc cited-path gate | 0 | 877 cited paths resolve |
| Archive integrity gate | 0 | |
| Per-page contents gate | 0 | |
| AEM store generator self-test | 0 | |
| Sweep/build shape gate | 0 | |
| Deploy shape gate | 0 | |
| Entity shape gate (make) | 0 | 219 checks, 0 failures, under make 4.3 |
| `wire-accountability` job | 0 | |
| `docs-check-no-git` job (a `git archive HEAD` export, no `.git`) | 0 | 0 findings; feature status 0 findings |

### `rtl-fast.yml` steps

| Step | rc | Result |
|---|---:|---|
| `lint_rtl.py --check --self-test` (Verilator 5.050) | 0 | 90 <= 90 |
| `pp_srcs.py --check --selftest` | 0 | |
| `behave --no-capture -f plain` in `tests/` | 0 | 14 features, 404 scenarios, 1,968 steps passed |
| `syn/yosys/run.sh --mode elaborate --no-structural` on `milan_datapath`, `KL_pp_shadow`, `KL_gptp_shadow` | 0 | 3 of 3 |
| OOC read sets: `dp_srcs.py --selftest`, `ooc_tcl_selftest.py`, `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`, `dp_srcs.py --top milan_datapath`, `--top KL_pp_shadow` | 0 | |
| `syn/yosys/ooc_selftest.py` | 0 | 75 arms |
| `syn/yosys/cache_selftest.py` | 0 | |

### Not run here

- `elaborate.yml` (`test_builder.py --require-elaboration --require-rv32`, `run_litex_sims.sh`): this host has no LiteX, VexiiRiscv or sbt. The hosted `elaborate` context covers it.
- `act_ci.py --pr <number>`: there is no PR (creating one is not this lane's to do).
- Hardware, bench and flashing: not allowed and not needed.
- The hosted contexts and the manager's builder, native and candidate banks (acceptance 4) follow the push.

## 7. Parent-visible list

- **Ports and parameters.** `protocol_processor_top` gains input `identify_button_i` and parameter `EN_IDENTIFY_NOTIF_P` (default 0), both C6. `KL_pp_shadow` ties both to 0, each with a `//!` rationale. No other top port or parameter changes. No parent port, pin, SoC, CSR, VERSION (`0x0002_0060`) or firmware change.
- **C5a (deadlines and hazards).** No top port. The kill ports are internal (`KL_aecp_engine`, `KL_aecp_ucpu`), and the parent instantiates neither. An AECP command past its 100 ms deadline is answered: ENTITY_MISBEHAVING unless a refusal was already chosen; NOT_IMPLEMENTED with the command echoed for non-AEM messages on that path. AECP and ACMP work serialize by hazard class (F03.7). The scoreboard kill face is now driven, so three literal-bound connections leave the port-contract inventory (62 -> 59 without a rationale).
- **C5b (dispatch and responses).** Locked `SET_SAMPLING_RATE`, `SET_CLOCK_SOURCE` and `SET_CONTROL` refusals, and `SET_CONTROL`'s out-of-range refusal, carry the value in force. GET_AUDIO_MAP pages of 63 to 71 records are served whole (in the parent only the 8x8 Stream Port Output subset exceeds 62). READ_DESCRIPTOR carries the stored current values of configuration-0 AUDIO_UNIT, CLOCK_DOMAIN and STREAM_INPUT/OUTPUT. `DESC_LINE_BYTES_P` must be a multiple of 8 in 576..1008; the parent binds 576.
- **C3 (ADP).** The ADPDU's current_configuration_index follows a SET_CONFIGURATION or a D3 restore; `current_cfg_i` is the fallback. The parent image declares one configuration, so the wire is unchanged while `ADP_IDX0` is 0. The `KL_pp_shadow` comment on `current_cfg_i` still reads "ADPDU current_configuration_index"; PR #136 suggests "while no configuration is set or restored", not taken (an RTL comment beyond the patch).
- **C6 at the parent's setting (0).** An unsolicited SET_STREAM_INFO carries Figure 7-40's 84-byte body. IDENTIFY_NOTIFICATION is never originated.
- **C2 (MAAP).** Acts only with `cfg_maap_internal_i` = 1, which `milan_datapath` ties to 0.
- **C4 (ACMP) and P141 (clock sources).** No RTL change; their tests (C4's AL/AI/AS, P141's D3C1 to D3C4) run in the processor's suites.
- **ROMs.** `ltn_rom.hex` unchanged; `ucode.hex` moves to `518b900c...37f8`.
- **Records.** Two DUT-reader dispositions (C4, C6); ROM ledger rows; the boundary diagram; the port-contract and naming budgets.
- **Open for a ruling.** `scripts/test_evidence.budget` can be lowered from 77 to 72 (not done: no generator, not in the assignment's list). Optional compliance-matrix citations offered by the processor PRs (5.4.2.x, 5.4.5, 5.5.2/5.5.3, 5.6.x) are not taken.
