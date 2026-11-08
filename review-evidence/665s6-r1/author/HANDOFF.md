# #665 S6, the placement switch (F-INT PR 2): [A745] handoff

STATUS: STOP after one round. A coherent, gated part of S6 is done; the rest is listed in section 7 with its reason.

- Lane: `665-s6-placement`, worktree `$LANES/665-s6-placement`.
- Base: `origin/dev-soft-core` `a9d69c774dee18b90eead74c9f2dda24cf8fdeb8`. The PR targets `dev-soft-core`. Nothing is pushed.
- Assignment: [A10] issuecomment-6712890110 on #665, and PLAN.md section S6 as it amends.
- TAKEN: issuecomment-6713000589. STOP: issuecomment-6715517869 (head `6584b7bf`).
- Head: `6584b7bfdf19e923153820c60190d87964e8f57b` (14 commits on the base).

## 1. What this round delivers

| Plan item (S6) | State |
|---|---|
| One parameter `CTRL_SPLIT_P` in the datapath; split: no `KL_pp_shadow`, no `KL_maap` | done, with no `KL_pp_maap_shim` and no map writer either (ruling 6410169666 item 1) |
| Every class-D consumer reads `pub_*`, the stream_id behind `SID_VALID` | done |
| Every S1 face connected to its contract 2.3 port; every G port tied to its reset value | done (F, R, E, M); G tied, the host window answering refused |
| `rx_axis_fabric` feeds the mailbox ingress; the egress takes `ctl_tx_mux`'s `s_data` leg | done (`KL_ctrl_split`) |
| Link, GM and domain feed the mailbox events | done |
| SoC: `CtrlMailbox` drops its idle tie-offs, crossing sys and `milan_cd` with approved primitives | done (`KL_mbx_cdc`: `cdc_handshake`, `cdc_pulse`; frames: `_axis_dp_cdc`) |
| One config key `control.placement: all-fabric \| split`; builder emits the flags and `CTRL_SPLIT_P` | done; gate 23m follows with no edit to its contract, plus a split case |
| The builder links the firmware ELF before the SoC | **not done** (section 7) |
| `pp_placement.py`: drop `f0-f4` or rule it dead | **not done** (section 7) |
| All-fabric netlist identical to `a9d69c77` for every shipped config | done: gateware export and elaborated digest |
| Two-placement `milan_dp` simulation, ADP/ACMP/MAAP/SRP/AECP, the comparison contract | **not done**; a split wiring leg runs instead (section 7) |
| The `full-split` population in a Yosys elaboration of every shape | done |
| The census sees every `pub_*` and contract 2.3 field consumed in the split | **not done** (section 7) |
| The plan's CDC mutant: a crossing without an approved primitive is refused | done as `make split-cdc` (`split_cdc_check.py`, four plants); not yet a CI case (section 7) |
| Yosys LUT/FF of both placements in the shipping shapes; one Vivado placement of the split image, as measurements | done: the split image places (section 6) |
| The full sweep (RTL changed) | done at the head: 65 suites, 0 failures (section 5) |

## 2. Context read

- [A10] issuecomment-6712890110: end state, netlist identity against `a9d69c77`, clock, area, shapes, files and gates.
- PLAN.md S6, D0, D1, D9 and section 1.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/design/MAILBOX_SPLIT.md` (the publication block, the processor's other faces, Default build, Open items), `docs/design/SPLIT_CONTROL_MEMORY.md`.
- S1 to S5 on `dev-soft-core`: `sw/mailbox/census_*.py`, `KL_mbx`, `CtrlMailbox`, the split boot and hook harnesses.
- `640-a734/HANDOFF.md` (read only): the split image did not place at `a68536fa`; its `split-firmware.sh`.

## 3. Changes, file:line and reason

Line numbers are at the head, `6584b7bf`.

### RTL

- `hdl/milan/milan_datapath.sv`
  - `:386` `CTRL_SPLIT_P` (default 0) and `:390` `CTRL_ENTRIES_P` (16, the contract's entries): the switch, at the end of the parameter list so no default shifts.
  - `:694` on: the `o_ctl_*`/`i_ctl_*` ports, at the end of the port list, in the datapath clock.
  - `:8723` `g_maap` gains `&& (CTRL_SPLIT_P == 0)`: the split builds no fabric MAAP engine; the firmware writes the AAF_DMAC window.
  - `:5638` `g_af_amr` around the map writer's deadline block and FSM; `:6132` `g_sp_amr` rests every register at reset, the restore's hold at 0 (ruling 6410169666 item 1).
  - `:9587` `g_af_pp` around `pp_shadow`, plus the ctl outputs tied 0 in all-fabric; `:9958` `g_sp_ctrl`, the split branch: C, F, R, E, M by `census_ports.py`'s classes, G tied. `:10077` `KL_ctrl_split`. `:10129` the host window answers at once, refused, so the CSR never stays busy.
  - `:10196` `g_af_shim` / `:10216` `g_sp_shim`.
  - The pp_shadow instance and the map writer keep their text and indentation, so the census plants' anchors hold.
- `hdl/milan/KL_ctrl_split.sv` (new): the split's receive tap (the wrapper's 4,096-byte frame FIFO and byte drain, only the control subtypes), its transmit packer and the wrapper's three frame counters.
- `hdl/milan/mailbox/KL_mbx_cdc.sv` (new): the crossing. Publication: free-running `cdc_handshake` snapshot. Settings: two `cdc_pulse`, the held bus taken on the edge that turns the acknowledgement. Windows: `KL_mbx_cdc_window`. Events, GM identity and LINK: one free-running `cdc_handshake`.
- `hdl/milan/mailbox/KL_mbx_cdc_window.sv` (new): one window: request and tag in, the processor's req/wait protocol, answer and tag back; a newer request wins.

### SoC and builder

- `sw/litex/milan_soc.py`
  - `:2891` the split-only source lists, `:2895` `CTRL_SPLIT_ENTRIES`, `:2898` `CTRL_SPLIT_PORTS`, then the `KL_mbx_cdc` port maps.
  - `:994` `p_CTRL_SPLIT_P = 1` only for the split; `:1378` the ctl Signals and the split-only source, so an all-fabric export is unchanged.
  - `:3030` `CtrlMailbox`: without a datapath, the idle tie-offs as before (the CPU harnesses build it so); with one, `:3109` `_split` binds the frames through two `_axis_dp_cdc` and the rest through `KL_mbx_cdc`, refusing a contract of other than one interface or 16 entries.
  - `:3166` `add_ctrl_mailbox(dp=)`; `:3751` the NIC is split exactly when `--ctrl-mailbox`.
  - `:4558` a relative `--ctrl-firmware` names a file under the repository root, as the builder emits it.
- `sw/builder/endstation_builder.py`
  - `:4423` `CONTROL_PLACEMENTS`, `:4430` `_load_control`, `:4444` `ctrl_firmware_path`.
  - `:5093` `datapath_params()` states `CTRL_SPLIT_P = 1` for split; `:5124` `emit_soc_argv()` appends `--ctrl-mailbox --ctrl-firmware sw/builder/out/<name>/ctrl_app.elf`.

### Tools, tests and docs

- `sw/mailbox/census_elab.py:127` `FABRIC_SCOPE`/`unscoped`, used at `:344` and `:348`: the census reads the `g_af_*` scopes without their prefix (a shared S1 file; needed so the all-fabric census is unchanged).
- `sw/mailbox/placement_identity.py` (new): the elaborated-netlist identity.
- `syn/ooc/split_population.py` (new): the full-split population on the RTL.
- `tb/verilator/milan_dp/`: `tb_split_top.sv`, `sim_split.cpp`, `split_mutants.py`, `split_cdc_check.py` (new); the Makefile's `split` case (in `ORDINARY_CASES`, so the default `make` and CI run it), `split-mutants` and `split-cdc` (`:871`); `CTLS_SRC`, `CDC_SRC`, `CDCW_SRC` overridable.
- `sw/builder/test_builder.py`
  - Gate 23m's split case (`:23495` `SPLIT_CASES`, `:23506` `_case_argv`, `:23548`) and its mutation (`:23575`); gate 23n (`:23611`, `:23632`).
  - `:22201` `_prune_guard_re`, used by gate 23d. The gate read MAAP_P's guard only as `generate if (MAAP_P != 0)`, so the split's `&& (CTRL_SPLIT_P == 0)` failed it. It now also accepts that conjunction, which keeps the property it pins: MAAP_P = 0 still prunes. It still refuses a disjunction, an inverted test and a guard without MAAP_P, checked in the gate and by two plants (section 4).
- `scripts/check_solution_docs.py:213`: the `Split control face` port group (the gate requires every datapath port classified); its row in `docs/integration/INTEGRATION_GUIDE.md` and `docs/guides/SYSTEM_INTEGRATOR.md`.
- `syn/yosys/run.sh`, `syn/yosys/ooc.sh`: `KL_ctrl_split.sv` in the datapath rows, and its own row.
- Generated, through their generators: `docs/diagrams/cdc_census.{drawio,svg,png}` (`cdc_census.gen.py`, `rsvg-convert`); `docs/traceability/MODULE_MATRIX.md`, `hdl/milan/README-tests.md`, `hdl/milan/mailbox/README-tests.md` (`gen_module_matrix.py`).
- Docs: `docs/design/MAILBOX_SPLIT.md` (status, contents, "The placement switch", Default build, the census scope rule, Open items); `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 5; `docs/ENDSTATION_BUILDER.md` row 34a; `tb/verilator/milan_dp/README.md`.
- The processor's new scope, `g_af_pp`, renames it for every reader that names it by path. The sweep at `490269c1` found the first: `milan_dp`'s `counters` cases no longer compiled. Verilator puts the generate block in the member name, and Vivado names the cell `g_af_pp.pp_shadow`, as it names `g_maap.maap_engine`. So:
  - The testbench probes now read `milan_datapath__DOT__g_af_pp__DOT__pp_shadow__DOT__...`: `tb/verilator/milan_dp/{sim_nxn.cpp, sim_aclk.cpp, sim_crf_licence.cpp, stream_counters.hpp}`, `tb/verilator/milan_dp_mclk/sim_mclk.cpp`, `tb/verilator/capture_coherence/sim_dp.cpp`, `tb/verilator/fw_service_budget/sim_main.cpp`, `tb/verilator/pp_shadow/sim_main.cpp` (46 lines, text only).
  - The Vivado-side tools name `milan_datapath/g_af_pp.pp_shadow`: `syn/ooc/pp_baseline.py:217` (its `KEEP_HIERARCHY` constraint) and `:554`, with the mutant's anchor at `pp_baseline_mutants.py:81`; `syn/ooc/pp_resource_gate.py:123` (the route root), with its fixture at `pp_resource_gate_selftest.py:79`; `syn/resmap/resmap_map.py:102` (the wrapper suffix), with its fixture; and three commands in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
  - Left as written: `docs/design/MARK_II_AREA_PLAN.md`'s hierarchy rows, a measurement at a past head.
- `tb/verilator/milan_dp/sim_split.cpp:187`: one name per declaration. The C++ idiom ratchet (`check_cpp_idiom.py`, multi-declarator, ratchet 0) counted 2 there.
- Shared files touched outside the lane's list: `census_elab.py`, `check_solution_docs.py`, the two integrator pages, the CDC census, the module matrix, `test_builder.py`'s gate 23d, and the scope rename's testbenches and tools above. None of S2b's (`sw/firmware/ctrl/**`) is touched.

## 4. New checks, planted defects and failing words

Each defect is planted in a copy and must fail with the words shown; each campaign also runs a clean control first.

### `tb/verilator/milan_dp` `make split` (48 checks) and `make split-mutants` (13 arms)

| Planted defect (`split_mutants.py`) | Source | Failing words (`FAIL ...`) |
|---|---|---|
| a class-D consumer on a G tie-off | datapath `g_sp_ctrl` | `[PUB] DA_GATE.OPEN reaches the talker's declaration predicate` |
| the licence on its ACTIVE term alone | datapath | `[PUB] ...and its admitted term` |
| a stream_id taken without SID_VALID | datapath | `[PUB] a stream_id without SID_VALID never reaches the listener` |
| a publication that never crosses again | `KL_mbx_cdc` | `[PUB] the stream_id reaches the listener once SID_VALID is set, within 60 mailbox cycles` |
| a setting taken before its commit | `KL_mbx_cdc` | `[FACE] a setting not committed does not reach the datapath` |
| a commit never acknowledged | `KL_mbx_cdc` | `[FACE] the commit is acknowledged within MBX_FACE_ACK_CYCLES` |
| a setting on the wrong datapath port | datapath | `[FACE] F_CLOCK.SOURCE_INDEX reaches the media clock's selector` |
| an answer under another tag | `KL_mbx_cdc_window` | `[WIN] CTR closes DONE, not TIMEOUT` |
| an answer taken while the datapath waits | `KL_mbx_cdc_window` | `[WIN] ...and that word is not the empty one` |
| a tap that hands out the media subtypes | `KL_ctrl_split` | `[RX] ...and the tap hands out no frame` |
| a serializer that drops a frame's last byte | `KL_ctrl_split` | `[RX] its record's length is the frame's` |
| a packer that reverses the lanes | `KL_ctrl_split` | `[TX] ...byte for byte` |
| the LINK level held low | `KL_mbx_cdc` | `[LINK] the datapath's effective link reaches LINK.UP` |

### `syn/ooc/split_population.py --selftest` (3 arms)

| Arm | Failing words |
|---|---|
| control: the tracked sources | none: every role within its limits |
| the processor left in the split (`g_af_pp` forced) | `wrong placement full-split: wrapper (KL_pp_shadow) count 1, expected 0..0` (and the seven processor roles) |
| the fabric MAAP engine left in the split (`g_maap` without the term) | `wrong placement full-split: maap (KL_maap) count 1, expected 0..0` |

### `sw/mailbox/placement_identity.py --selftest` (6 arms)

| Arm | Required |
|---|---|
| control: a comment changes | the recipe shape's digest unchanged |
| an operator of the all-fabric path (`|` to `&`) | the digest changes |
| a wrapper port connected to another net | the digest changes |
| the all-fabric build reads a split port | refused: `reads the split port i_ctl_pub_dom_adopted` |
| a split output driven from a net | refused: `come from a net, not a constant` |
| the switch's default flipped | refused: `not at its default 0` |

### `sw/builder/test_builder.py`

| Gate | Planted defect | Failing words |
|---|---|---|
| 23m mutation | the split SoC stops reaching `CTRL_SPLIT_P` (`p_CTRL_SPLIT_P = 0`) | `ax7101_1x1_tdm8+split: the SoC binds CTRL_SPLIT_P=` |
| 23n | a split key naming the fabric firmware (`ctrl_firmware_path` patched) | `not the split image under its builder output` |
| 23n | `control: {placement: both}`, `{placment: split}`, `split` | `control.placement 'both' is not one of all-fabric, split`; `control: unknown key(s) ['placment']`; `control: must be a mapping` |
| 23d | `g_maap` guarded `((MAAP_P != 0) \|\| (CTRL_SPLIT_P == 0))`, in a copy of the tree | `MAAP_P guards no `generate if`` (rc 1) |
| 23d | `g_maap` guarded `((MAAP_P != 0) && (CTRL_SPLIT_P != 0))`, in a copy of the tree | `MAAP_P guards no `generate if`` (rc 1) |
| 23d, in the gate | the pattern against six spellings: two accepted, four refused | `the prune guard pattern accepts ...` if one is read wrongly |

### `tb/verilator/milan_dp/split_cdc_check.py --selftest` (`make split-cdc`; 4 plants)

The netlist check: every flop, output and primitive source input of `KL_mbx_cdc` reads only its own domain through combinational cells, except the held settings bus `fw_r`.

| Planted defect | Source | Failing words |
|---|---|---|
| control: the tracked sources | | none: `152 sinks read their own domain` |
| the publication block wired straight across | `KL_mbx_cdc` | `output d_pub_sid_o (dp) reads m_pub_sid_i (sys)` |
| the LINK level taken straight across | `KL_mbx_cdc` | `flop m_link_up_o (sys) reads d_link_up_i (dp)` |
| the settings read without their capture | `KL_mbx_cdc` | `output d_cur_config_o (dp) reads m_fw_cur_config_i (sys)` |
| a window's answer taken straight across | `KL_mbx_cdc_window` | `output m_ctr_ans_data_o (sys) reads` |

### The plan's mutants, and where each stands

| Plan mutant | Where |
|---|---|
| the processor left in the split | `split_population.py --selftest` |
| a class-D consumer still on a G tie-off | `split_mutants.py` |
| a CDC crossing without a primitive, which lint or the census refuses | `split_cdc_check.py --selftest` (`make split-cdc`), four plants; not yet a CI case (section 7) |
| a key that selects the split but links the fabric firmware | gate 23n's negative control |
| the two-placement plants (a byte flip, an SRP `+k`, a missing notification) | **not done**: no two-placement simulation yet (section 7) |

## 5. Gate table

Receipts are under `receipts/` (index: `receipts/INDEX.md`). Each receipt's first line names the head it ran at. Every command ran unpiped, its output redirected to the receipt.

The last three commits (`c9fac717`, `a91282af`, `6584b7bf`) change no RTL and no file under `sw/mailbox/`, `sw/litex/`, `sw/builder/endstation_builder.py` or `sw/firmware/`. So the identity, population, census, export and firmware rows at `490269c1` or earlier stand for the head. Every gate whose inputs those commits touch ran again at `6584b7bf` (`receipts/at-6584b7bf/`).

| Gate | Command | rc | Result | Receipt |
|---|---|---|---|---|
| All-fabric identity, elaborated netlist, 6 shapes | `placement_identity.py --dump` (base `a9d69c77`, head) then `--compare` | 0 | every digest equal | `identity/identity-compare.txt`, `identity/ident-*.json` |
| Identity tool self-test | `placement_identity.py --selftest` | 0 | 6 of 6 arms | `identity/identity-selftest.txt` |
| All-fabric identity, gateware export, 5 shipped configs (Arty at 100 MHz as the F-INT method) | `scripts/export_compare.sh` (`compare_same.py`, `export_digest.py`) | 0 | 3,876 files each, 3,856 identical, 20 by the stated normalisations, 0 different; normalised digests equal | `export/at-490269c1/` (and `export/` at `61d680dd`) |
| Split SoC CSR map against the base `--ctrl-mailbox` export | `diff` of `csr.csv` rows | 0 | equal | `export/split-csr-map-equal.txt` |
| Full-split population, 6 shapes | `syn/ooc/split_population.py --check --jobs 4` | 0 | every role within its limits | `population/split-population-check.txt` |
| Population self-test | `split_population.py --selftest` | 0 | 3 of 3 | `population/split-population-selftest.txt` |
| Publication census, 6 shapes | `publication_census.py --check --jobs 6` (at `61d680dd`; after it, its inputs changed only in `KL_ctrl_split.sv`'s comments) | 0 | 246 checks, 0 failures; 41 reads, C 26 F 28 R 34 E 6 M 14 G 111 | `census/census-check.log` |
| Census self-test | `publication_census.py --selftest --jobs 6` (at `61d680dd`) | 0 | 139 arms, 0 failed; 43 rules each proved | `census/census-selftest.log` |
| `milan_dp` split leg | `make -C tb/verilator/milan_dp build-split` then `./obj_split/Vmilan_dp_split` (Verilator 5.052) | 0 | 48 checks, 0 failures | `bench/split-leg.txt` |
| Split leg mutants | `make -C tb/verilator/milan_dp split-mutants` (at `65631759`; its sources unchanged after) | 0 | control passes; 13 of 13 caught by their checks | `bench/split-mutants.log` |
| Split CDC structure | `split_cdc_check.py --selftest` | 0 | 152 sinks in their domain; 4 of 4 plants refused | `bench/split-cdc-check.txt` |
| Builder gates 23m, 23n, 32 | `test_builder.py --gates ...` (at `490269c1`) | 0 | 6 elaborations; 4 of 4 cuts; 23n and its controls; key map | (in the full run below) |
| Builder gate 23d | `test_builder.py --gates test_optional_block_names_reach_the_rtl` | 0 | the guard pattern's six spellings; 23d and 23e pass | `builder/gate23d.txt`; plants `builder/gate23d-plant-{or,inv}.txt` (rc 1 each) |
| Builder, full, at `490269c1` | `python3 sw/builder/test_builder.py --require-rv32` | 1 | stopped at gate 23d (section 3, fixed in `c9fac717`) | `builder/test_builder-490269c1-first-run-tail.txt` |
| Builder, full, at `6584b7bf` | `python3 sw/builder/test_builder.py --require-rv32` | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11's calibration arm needs an earlier board build's Vivado report, not on this host (unrelated to this change) | `builder/test_builder.txt` |
| Firmware self-test | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test` (at `490269c1`) | 0 | `test_ctrl_firmware: PASS`; 1,053 `[ok]`, 0 `[FAIL]`; mutants 570 of 570 caught | `firmware/test_ctrl_firmware-490269c1.txt` |
| Firmware self-test at `6584b7bf` | the same | 0 | `test_ctrl_firmware: PASS`; 1,053 `[ok]`, 0 `[FAIL]`; mutants 570 of 570 caught | `firmware/test_ctrl_firmware.txt` |
| Lint ratchet | `scripts/lint_rtl.py --check` | 0 | 89 <= 89 | `lint/lint_rtl.txt` |
| Sources | `scripts/check_soc_sources.py`; `scripts/check_rtl_source_lists.py` | 0, 0 | 47 modules registered; 113 files, 4 of 4 lists | `lint/` |
| Docs gates | `docs_check.py`, `check_feature_status.py`, `check_em_dash.py --base origin/dev-soft-core` (pinned renderer), `check_doc_style.py` and `--selftest`, `check_gptp_docs.py`, `DOC_MAP.gen.py --check`, `check_solution_docs.py` and `--selftest`, `submodule_boundaries.gen.py --check`, `check_submodule_docs.py`, `check_diagram_pngs.py`, `gen_module_matrix.py --check`, `check_wire_accountability.py --self-test`, `gen_hdl_reference.py --selftest` and the build | all 0 | 0 findings each; again at `6584b7bf` | `docs/`; `at-6584b7bf/docs/` |
| BDD conformance | `cd tests && python3 -m behave --no-capture -f plain` | 0 | 14 features, 508 scenarios, 2,330 steps; again at `6584b7bf` | `docs/behave-summary.txt`; `at-6584b7bf/docs/behave-summary.txt` |
| Full sweep at `490269c1`, 4 shards | `native-shards.py 665s6-a745-490269c1 ... 4 0-7 8-15 48-55 56-63` | 1 | stopped: `milan_dp` FAIL, its `counters-1` and `counters-8` cases did not compile (the probes of section 3); fixed in `6584b7bf` | `sweep/at-490269c1-milan_dp-failure.txt` |
| Full sweep at `6584b7bf`, 4 shards | `native-shards.py 665s6-a745-6584b7bf ... 4 0-7 8-15 48-55 56-63` (each shard `scripts/run_all_suites.sh <logs> --wait --shard k/4`) | 0, 0, 0, 0 | 65 suites, 65 passed, 0 failed, 0 timed out; 2,192,876 checks, 0 in-suite failures. Among them `milan_dp` (its `split` leg and the `counters` cases), `milan_dp_mclk`, `capture_coherence`, `fw_service_budget`, `pp_shadow` and `mbx` | `sweep/SUMMARY.md`, `sweep/shard-*.txt`, `sweep/suite-logs.txt` |
| xvlog, at `6584b7bf`, under the Vivado lock | `scripts/xvlog_gate.py --check`, and `--selftest` | 0, 0 | `xvlog gate: PASS (0 finding(s) == ratchet; 0 hdl/, 0 pinned processors)`; the self-test's planted use-before-declaration reddens it | `at-6584b7bf/xvlog-*.txt` |
| At `6584b7bf`: split leg | `make -C tb/verilator/milan_dp build-split`, then the leg | 0 | 48 checks, 0 failures | `at-6584b7bf/split-leg.txt` |
| At `6584b7bf`: split leg mutants | `make -C tb/verilator/milan_dp split-mutants` | 0 | control passes; 13 of 13 caught by the check each names | `at-6584b7bf/split-mutants.txt` |
| At `6584b7bf`: split CDC structure | `split_cdc_check.py --selftest` | 0 | 152 sinks; 4 of 4 plants refused | `at-6584b7bf/split-cdc-check.txt` |
| At `6584b7bf`: the `counters` case that broke | `stream_counters.py --shape 1` (pinned Verilator 5.050) | 0 | `RESULT: PASS`, 0 failures | `at-6584b7bf/counters-1x1.txt` |
| At `6584b7bf`: C++ idiom | `scripts/check_cpp_idiom.py`, and `--selftest` | 0, 0 | every ratchet held (multi-declarator 0 <= 0); 75 of 75 | `at-6584b7bf/check_cpp_idiom*.txt` |
| At `6584b7bf`: Vivado-side tools (rtl-fast) | `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`, `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py`, `pp_resource_gate.py check-baseline`, `resmap_map.py --selftest` | all 0 | PASS each; 236 of 236 gate mutants fail; 3 endpoints; 15 of 15 arms | `at-6584b7bf/` |
| At `6584b7bf`: docs | `check_em_dash.py --base origin/dev-soft-core`, `check_doc_style.py`, `docs_check.py` | 0, 0, 0 | 0 findings over 165 added lines in 10 pages; 23 documents OK; 0 findings | `at-6584b7bf/` |
| At `6584b7bf`: lint ratchet | `scripts/lint_rtl.py --check` | 0 | 89 <= 89 | `at-6584b7bf/lint_rtl.txt` |

## 6. Measurements

Measurements, not gates. Receipts: `receipts/area/` (Yosys) and `receipts/vivado/` (the one placement).

### Yosys area, both placements, the shipping shapes

Yosys 0.66 `synth_xilinx` of `milan_datapath` at `CTRL_SPLIT_P` 0 and 1. The RTL is `61d680dd`'s; every later `hdl/` change is a comment.

| Shape | Placement | LUT | FF | RAMB36 | RAMB18 | DSP |
|---|---|---|---|---|---|---|
| 1x1 TDM8 | all-fabric | 99,794 | 44,073 | 18 | 15 | 21 |
| 1x1 TDM8 | split | 60,298 | 23,468 | 3 | 14 | 11 |
| 1x1 TDM8 | split minus all-fabric | -39,496 | -20,605 | -15 | -1 | -10 |
| 8x8 | all-fabric | 170,479 | 59,357 | 21 | 15 | 21 |
| 8x8 | split | 84,327 | 28,722 | 5 | 14 | 11 |
| 8x8 | split minus all-fabric | -86,152 | -30,635 | -16 | -1 | -10 |

The split adds, on the mailbox side, `KL_mbx` (9,559 LUT, 9,888 FF, 1 RAMB36, 9 RAMB18) and `KL_mbx_cdc` (464 LUT, 9,633 FF, measured standalone with every output a port). The CPU, its memories and the SoC are not in these rows.

### The split image's memory plan

The split image plans 39.0 of 56 tiles: the ROM is 109,552 B in 27 RAMB36, and the SRAM 47,168 B in 12. (`receipts/image/`.)

### One Vivado placement of the split shipping image

At `6584b7bf`: the split shipping image (`control.placement: split`; the shipping AX7101 1x1 TDM8 argv plus `--ctrl-mailbox --ctrl-firmware`), XC7A100T. The flow is the shipping one cut after placement: synthesis `AreaOptimized_high`, opt `ExploreArea`, place `ExtraPostPlacementOpt`, phys_opt `AggressiveExplore`. It was not routed. **It places**: Vivado rc 0, 0 ERROR, 0 CRITICAL WARNING.

| Step | LUT | FF | Slices | BRAM tiles | DSP | WNS / WHS |
|---|---|---|---|---|---|---|
| Synthesis | 35,952 (56.71 %) | 45,361 | | 93 | 5 | |
| Placement | 34,225 (53.98 %) | 45,222 (35.66 %) | 14,147 of 15,850 (89.26 %) | 93 of 135 (68.89 %: 75 RAMB36, 36 RAMB18) | 5 | -0.071 ns over 24 endpoints / -0.245 ns over 350, post-placement estimates |

Placed blocks: `milan_datapath` 18,546 LUT, 22,468 FF; `KL_mbx` 4,432, 8,563; `KL_mbx_cdc` 1,408, 3,011; `KL_ctrl_split` 224, 261; the CPU core 1,163, 1,120.

The worst setup path is on the 100 MHz system clock: from the SoC bus's AXI-Lite-to-Wishbone handler into `KL_mbx`'s register read data, 19 logic levels, 9.981 ns. Hold is short only between two CRG clocks, which the router normally fixes. Whether a route closes setup is not measured here.

Before this lane, at `a68536fa`, the same image kept the processor beside `KL_mbx` and did not place: 59,102 LUT and 114.5 BRAM tiles at synthesis, 280 slices short (640-a734/HANDOFF.md).

## 7. What remains, and why

1. **The two-placement simulation** (the plan's main acceptance item). It runs the same stimulus through both placements and compares raw ADP/ACMP/MAAP/AECP bytes and the SRP multiset. That needs the split firmware running on this datapath: either the CPU harness's test SoC with `--ctrl-mailbox` and a real datapath, or the host-compiled firmware on the RTL mailbox (as `tb/verilator/mbx`'s co-simulation does), beside the all-fabric processor. With its plants it is the largest remaining piece. This round's split leg proves only the wiring, the crossing and the frame paths, through the contract's registers.
2. **The census on the split elaboration.** The plan asks that the census see every `pub_*` and contract 2.3 field consumed, and pass without the map writer's and REBOOT's exclusions. That needs a second population, the datapath's `i_ctl_*` ports at `CTRL_SPLIT_P = 1`, in `publication_census.py`/`census_ports.py`, with its own rules and plants. This round makes the all-fabric census read unchanged and checks the split's population by module.
3. **The REBOOT carrier** (ruling 6554243203). In the split, `reboot_req_i` is tied 0. A carrier is a contract change (a face-block level, `gen_mailbox.py`) plus the firmware AECP owner's REBOOT (S11), in `sw/firmware/ctrl/aecp`, S2b's area.
4. **The maps on the datapath, and the undone value after a failed change** (MAILBOX_SPLIT Open items). Both are the firmware AECP owner's: it must drive the `EDIT` window, and republish on a late acknowledgement. They live in `sw/firmware/ctrl/aecp`, which this lane stays out of while S2b runs.
5. **The builder links the firmware before the SoC.** The builder emits `--ctrl-firmware sw/builder/out/<name>/ctrl_app.elf`. Linking that image needs the split export's `csr.csv` and flash map first, the cycle the daily recipe breaks with a fixture image. That recipe belongs with S9's split image recipe; a ruling on where it lives is asked.
6. **`pp_placement.py`'s `f0-f4`.** Dropping it redesigns `pp_placement_selftest.py`: seven of its arms use `f0-f4` as the retained-wrapper population. A ruling is asked: drop now, or rule it dead.
7. **The CDC check in CI.** `make split-cdc` refuses a raw crossing, with four plants, but no CI case runs it: the hosted `milan_dp` shards carry no sv2v or Yosys. Adding it to a job that has them is a workflow change, outside this lane's files.
8. **D0's requirement text** (`REQUIREMENTS.md` per-function placement) needs the owner's approval; untouched.

Also found: `split-firmware.sh` (the daily's management recipe) no longer links at the `dev-soft-core` head. Since S4, `ctrl_plat_image.py` refuses a link without `--flash-map`. I ran its remaining steps by hand (`gen_flash_port.py`, then the link with `--flash-map`).
