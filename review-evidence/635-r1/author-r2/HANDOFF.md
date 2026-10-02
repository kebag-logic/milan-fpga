# [A509] Issue #635 round 2 handoff: PR #636 review answers

Status: REVIEW READY at `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` (local; not pushed: push and PR edits are not this lane's). Items 1 to 4 are committed, one commit each (items 2 and 3 share the `#80` commit), and every gate in section 4 is rc 0 at that head.

- Repository kebag-logic/milan-fpga (`origin` checked: `https://github.com/kebag-logic/milan-fpga.git`, unchanged), branch `635-pp-pin-631eeb34`.
- Start head `3370c6cbd5e4b096167c19ca709556a40207e538` (round 1). Five commits were added on top of it; nothing was amended, rebased or pushed.
- The remote branch head is still `3370c6cb`, and live remote `dev` is still `cdf49d1a28527562888f0a903de51b6b15b1244f`, the branch's merge base.
- Assignment: #635 comment 5962734738. Findings answered: R438-1 (PR #636 comment 5962667464), R439-1 (PR #636 comment 5962728186). TAKEN: #635 comment 5962752104. REVIEW READY: #635 comment 5963295768.
- The `protocol-processor` gitlink stays `631eeb342ca1e3fa80e734077a56a943aee76ff1`. Round 2 changes no gitlink, port, parameter, generated file, SoC, CSR, VERSION or firmware. `git -C protocol-processor rev-parse --show-toplevel` was checked to be the submodule directory before any git command inside it.
- No existing issue or PR comment was edited or deleted.

## Commits, in item order

| # | Commit | Item | Finding | Subject |
|---:|---|---|---|---|
| 1 | `ce9488612f251876cce2ea8369dab6239ee5484d` | 1 | R438-1 F1 = R439-1 F1 | Record C5a's NOT_IMPLEMENTED echo for a non-AEM command whose response memory fails, GET_MILAN_INFO among them |
| 2 | `e19f14849f1a80c83380af7a0141670bc71cf781` | 2 | R439-1 F2 | Narrow the changelog's C5a deadline answer: a refusal already chosen stands, and a command that had changed state answers for itself |
| 3 | `987720eb8352fb5092088a56948f8ad27ec091e7` | 2, 3 | R439-1 F3 = R438-1 S1 | Qualify KL_pp_shadow's EN_IDENTIFY_NOTIF_P rationale as the ruling on protocol-processor #80, not milan-fpga #80 |
| 4 | `b8ab4f817941295be0801d611dbe6ee61a1b265c` | 2 | R439-1 F4 | Pair the three scoreboard kill tie-offs with C5a's deadline row in the submodule ledger, not the hazard row |
| 5 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` | 4 | R439-1 S1 | Give ADP_IDX0's current_configuration_index its processor pin 631eeb34 meaning: the fallback while the configuration row is unset |

Every commit has one parent, a one-line subject, no body and no trailer. `git diff 3370c6cb 420b778a --stat` covers 4 files, 10 insertions and 5 deletions: `CHANGELOG.md`, `docs/reference/REGISTER_MAP.md`, `docs/reference/SUBMODULES.md` and `hdl/milan/KL_pp_shadow.sv`.

## 1. The pin change and the records it re-records

The pin change itself is round 1's (`14f8c27f`): the gitlink moved from `b2db3a970cedbbff2f8ba813acb96122c442bc58` to `631eeb342ca1e3fa80e734077a56a943aee76ff1`, carrying processor PRs #136, #135, #137, #138, #140, #139 and #142. Round 2 does not move it. Every record that round 1 re-recorded for it still holds at the round-2 head:

| Record | Round-1 commit | Generator | Round-2 check at `420b778a` |
|---|---|---|---|
| `syn/yosys/rom_digests.tsv` (rows for `631eeb34`: `ltn_rom.hex` `23cc67ee...e956`, unchanged; `ucode.hex` `518b900c...37f8`) | `3c68c6b1` | `cd syn/yosys && ./ooc.sh --record-rom-digests` | re-run, rc 0; `git diff --exit-code syn/yosys/rom_digests.tsv` rc 0 (no diff) |
| `docs/diagrams/submodule_boundaries.{svg,drawio,png}`, `PNG_MANIFEST.json` | `81a80dd6` | `docs/diagrams/submodule_boundaries.gen.py` | `--check` rc 0 (twice: standalone and the docs step) |
| `scripts/port_docs.budget` (three scoreboard kill tie-offs left: 62 -> 59 without a rationale) | `46ed4e91` | `check_port_contracts.py --write-budget` | gate rc 0: 3,798 ports, undocumented hdl 217 <= 217, gptp 19 <= 19, processor 111 <= 111; 59 without a rationale, all recorded. The comment edit is a `//!` line above a parameter binding, which is outside the inventory, and the count is unchanged |
| `scripts/naming.budget` | `216d6feb` | `measure_naming.py --write-budget` | `--check` rc 0, 96 recorded |
| `docs/reference/SUBMODULES.md` pin table | `eb775875` | none: hand-edited the way the earlier adoptions were, verified by `check_submodule_docs.py` | rc 0, 4 exact gitlinks. Round 2 edits only the parent-observable table below it (items 1 and 2) |

Not re-recorded, as in round 1: `scripts/test_evidence.budget` stays at 77, although the ratchet reads 72; the reviewers took this as the manager's ruling. The capture receipt is also left as it is (section 3).

## 2. Patch hunks

### Round 2 (this lane)

| Commit | File:line at the head | Hunk | Processor change it answers |
|---|---|---|---|
| `ce948861` | `CHANGELOG.md:47-49` | Three bullets under "Unreleased - processor pin 631eeb34": "So does a non-AEM command whose response memory fails."; "GET_MILAN_INFO is one; at `b2db3a97` it answered ENTITY_MISBEHAVING."; "Processor PR #140 cites Milan Table 5.19 for this." | C5a, processor PR #140, round-2 item 2. The fault rebuilds at A_ALLOC and A_WR answer any message type but AEM_COMMAND NOT_IMPLEMENTED, with the command echoed (`protocol-processor/hdl/aecp/KL_aecp_engine.sv:1751-1753` `st_echo_w`, `:3767-3771` A_ALLOC, `:3799-3801` A_WR, at `631eeb34`). Processor operator guide at `631eeb34`, lines 55 and 326. At `b2db3a97`, line 54 said ENTITY_MISBEHAVING. Clause: Milan v1.2 Section 5.4.3.3, Table 5.19 (MVU statuses SUCCESS and NOT_IMPLEMENTED only) |
| `ce948861` | `docs/reference/SUBMODULES.md:115` | New parent-observable row: "C5a answers a non-AEM command whose response memory fails NOT_IMPLEMENTED, with the command echoed ([processor PR 140](...); Milan v1.2 Section 5.4.3.3, Table 5.19)" / "No top port or parameter; GET_MILAN_INFO is such a command, and at `b2db3a97` the same fault answered ENTITY_MISBEHAVING" | as above |
| `e19f1484` | `CHANGELOG.md:44-45` | "Its answer is ENTITY_MISBEHAVING unless a refusal was already chosen." / "A command that had already changed state answers for itself." (was: "...unless a refusal was chosen.") | C5a, PR #140: the deadline kill answers the best current status through E_FAILSAFE unless the program already produced an effect (`KL_aecp_engine.sv:1723-1737`); operator guide line 56 |
| `987720eb` | `hdl/milan/KL_pp_shadow.sv:1099` | `//! wired to identify_button_i (processor lane C6, manager ruling on protocol-processor #80)` (was "... on #80"). Comment only | C6, processor PR #139: parameter `EN_IDENTIFY_NOTIF_P`, held at 0 by the ruling on processor issue 80 |
| `b8ab4f81` | `docs/reference/SUBMODULES.md:114`, `:116` | Deadline row's parent cell: "No top port or parameter; its kill ports stay inside the processor, and the three scoreboard kill tie-offs left the processor top". Hazard row's parent cell: "No top port or parameter" | C5a, PR #140: the scoreboard's `kill_valid_i`, `kill_id_i` and `kill_resp_queued_i` are driven from the deadline block (`protocol_processor_top.sv:1022-1024`, `aecp_dl_kill_w`, `aecp_dl_queued_w`) |
| `420b778a` | `docs/reference/REGISTER_MAP.md:1016` | `ADP_IDX0` description: "`[15:0]` current_configuration_index the ADPDU carries until a SET_CONFIGURATION or D3 restore writes the processor's configuration row, and again after a D3 roll-back (from processor pin `631eeb34`), `[31:16]` identify_control_index" | C3, processor PR #136. The ADPDU index is `aecp_cur_cfg_v_w ? aecp_cur_config_o : current_cfg_i` (`protocol_processor_top.sv:1852-1862`). The overlay's valid flag is set by a write to configuration row 0 and cleared by the store reset, which includes the D3 roll-back (`KL_aecp_engine.sv:1610`, `:1912-1920`) |

Where the text differs from the reviewers' exact words:

- **F2.** `scripts/check_doc_style.py` holds `CHANGELOG.md` to 10 words per sentence. Run on the reviewers' sentence, its `analyze()` reports "sentence has 20 words; maximum is 10". So the two clauses are two bullets, and the words are unchanged.
- **R439-1 S1** (an optional text). It adds ", and again after a D3 roll-back", which the processor top's own comment states ("the image default while it is unset (from reset, and after a D3 roll-back)").
- **F3** uses R439-1's text ("protocol-processor #80"). R438-1 S1 proposed "processor issue 80" for the same point, and the assignment's item 2 says to use the reviewers' exact text.

Not taken: the optional pointer from `REGISTER_MAP.md`'s protocol-processor memory-bridge section, which is keyed on ENTITY_MISBEHAVING (`:2357-2358`). Both F1s call it optional, and item 1 names only the CHANGELOG and SUBMODULES.

### Round 1 adoption patch (unchanged, for the record)

`parent-adoption-c4c6-ea3fb388.patch`, sha256 `67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c`, committed one concern per commit. The three commits equal `git apply` of the whole patch (patch-id `791277578ee8659a7daaec098a841e6df070f31d`).

| Commit | File:line at `420b778a` | Hunk | Processor change |
|---|---|---|---|
| `c4bf64e2` | `scripts/measure_test_evidence.py:597-600` | `DUT_READER_DISPOSITIONS` entry for `protocol-processor/tb/pp_top/acmp_mutants.py` | C4, PR #137 |
| `15933a60` | `hdl/milan/KL_pp_shadow.sv:1098-1100` (line 1099 reworded in round 2) | `.EN_IDENTIFY_NOTIF_P (1'b0)` with its `//!` rationale | C6, PR #139 |
| `15933a60` | `hdl/milan/KL_pp_shadow.sv:1138-1140` | `.identify_button_i (1'b0)` with its `//!` rationale | C6, PR #139 |
| `927428d1` | `scripts/measure_test_evidence.py:601-604` | entry for `protocol-processor/tb/pp_top/notify_mutants.py` | C6, PR #139 |

## 3. Saved state: capture check

`python3 scripts/check_nvm_capture.py`: rc 0, "PASS: capture census, clocks, both timing arms and receipt agree". All seven controls were detected (bytes, records, clock, configured-clock, system-clock, ignore-off-timing, off-time-limit). It ran twice: once standalone and once as the docs step "Capture measurement census and clock gate".

- The receipt's `measured_for` matches: `endstation_ax7101_8x8` 12,634 bytes, 156 records; `endstation_ax7101_1x1_tdm8` 3,218 bytes, 53 records; CPU 50 MHz, system 100 MHz.
- The product firmware `sw/firmware/milan_baremetal/milan_baremetal.c` has sha256 `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`, equal to the receipt's `product_firmware_sha256`.
- Round 2 changes no firmware, census input or processor source, so no re-measure is owed. The recorded 8x8 maximum stays 13.23 ms, below the 24.5 ms STOP line.

## 4. Gates

All gates ran at the committed head `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0`, from the physical path `$LANES/635-pp-pin`. None was piped; each wrote its own log and rc file under `$VALIDATION_STORAGE/635-a509/gates/logs`. `SUMMARY.txt` there has sha256 `775db7b5c46a790d45fd186beef835905b9d7b2fcd8020235f01d9fcb3bbfd9d`.

- `git status --porcelain` was empty before the gates and after them, and all three submodules were clean at their gitlinks. The gates left no hex files or other litter.
- Four background tracks ran concurrently, launched with `setsid`, with `TMPDIR` and `RUNNER_TEMP` under `$VALIDATION_STORAGE/635-a509`.
- The two builder runs ran one after the other, not together.
- The xvlog gate ran last, alone, with no other build of this lane running.
- The service cgroup peaked at 10.3 GB of 12 GB, with no OOM event (`memory.events`: oom 0).

Tools:

- Verilator 5.050 (`2026-07-01 rev v5.050`), first on `PATH` for every track.
- Host GNU Make 4.4.1 for the consumer commands.
- GNU Make 4.3, built here from `make-4.3.tar.gz` (sha256 `e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19`, verified) with `./configure --disable-nls && make`. Binary sha256 `b34990d51cf07f43658c09b3f2096cd5cdd491dc2993ee705e12921ae79fd4d9`. It was first on `PATH` in every docs step.
- sv2v v0.0.12 from the release zip (sha256 `ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00`, verified) in the docs track.
- Yosys 0.66; Python 3.14.7; Vivado 2026.1 `xvlog`.

### The 16 consumer commands (host make 4.4.1)

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, 0 in `hdl/`, 4 in the pinned processors (`KL_aecp_notify.sv:557`, `KL_pp_originator.sv:194`, `KL_pp_rx_validator.sv:383`, `protocol_processor_top.sv:922`, all VRFC 10-3380); run alone, 147 s |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | 107 files in the `milan_datapath` closure, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 6 | `python3 sw/builder/test_builder.py` (whole, 1,109 s) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11, the calibration gate, needs a local board build tree |
| 7 | `make -C tb/verilator/pp_shadow -j16` (214 s) | 0 | 606, 606, 646 and 311 checks, 0 failures, RESULT PASS x4 |
| 8 | `python3 scripts/check_port_contracts.py` | 0 | 3,798 ports (processor 1,757); undocumented 217/19/111 at the ratchet; 59 without a rationale, all recorded |
| 9 | `python3 scripts/measure_naming.py --check` | 0 | 96 candidates, all recorded |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, 0 <= 0 unexplained DUT-source readers, 3 <= 3 |
| 11 | `python3 scripts/docs_check.py` | 0 | 0 findings across 185 Markdown files and 956 scrubbed text files |
| 12 | `make -C tb/verilator/nvm_cosim lint` | 0 | pass (Verilator 5.050) |
| 13 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 14 | `make -C tb/verilator/milan_dp -j16` (1,519 s) | 0 | 9 RESULT PASS: `sim` 235, `notify` 382, `crflic` 416, `nxn` 1,845, `nxndv` 1,847, `nxn8` 3,525, `nxn4c` 1,845, `nolpf` 235, `prune` 33, `ax1x1` 232, `aclk` 191; prerequisites `gmstep` 104, `gptp` 182, `gptplat` 182; `render_mutants.py` 6/6, `gmstep_mutants.py` 6/6 |
| 15 | `make -C tb/verilator/milan_dp_render -j16` (331 s) | 0 | 65 and 152 checks, 0 failures; leg defects 5/5 |
| 16 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |

The comment edit's four named gates are rows 7, 4, 3 and 16 above.

### `docs.yml`: every step and job as the workflow runs it, with the make version per step

Each step ran in its own `bash --noprofile --norc -e` from the lane root. The commands were copied from the workflow, with `python3` from the Markdown environment and GNU Make 4.3 first on `PATH`. Each log's first line records the make that `PATH` resolves.

Substitutions for runner-only setup:

- pyslang 11.0.0 was installed `--require-hashes` into a scratch `--target` and put on `PYTHONPATH`, in place of the system pip install.
- pyyaml, wavedrom 2.0.3.post3, cmarkgfm and html5lib were already present. The Markdown lock was checked with a `--require-hashes` dry run.
- The em-dash step ran in its pull_request form (`PR_BASE_REF=dev`, `git fetch origin dev`, merge base `cdf49d1a`).
- The RV32 SDK step was given a fresh `--destination` under the lane's scratch.
- The act self-test ran from the audited install, whose sha256 equals live `dev`'s `scripts/act_ci.py`. AGENTS.md section 5 forbids running the candidate's copy on the host.
- `docs-check-no-git` ran on a `git archive HEAD` export with no `.git`.

| Step (workflow name) | Make | rc | Result |
|---|---|---:|---|
| Build the validated HDL reference | GNU Make 4.3 | 0 | self-test 44/44; HTML written (71 sections) |
| (Install the python gate dependencies, the Markdown renderer and diagram dependencies) | GNU Make 4.3 | 0 | present; Markdown lock satisfied (`--require-hashes` dry run); `rsvg-convert` present |
| Link health, wording, dead-reference and local-info gate | GNU Make 4.3 | 0 | 0 findings |
| Added-line em-dash gate | GNU Make 4.3 | 0 | base `cdf49d1a`; 0 findings over 69 added lines in 4 pages, arms 339/339 |
| Concise audience documentation gate | GNU Make 4.3 | 0 | 22 documents OK; gPTP docs and both self-tests |
| Audience diagram no-drift gate | GNU Make 4.3 | 0 | |
| Product solution source-fact gate | GNU Make 4.3 | 0 | 43 mutation controls |
| Verified submodule documentation gate | GNU Make 4.3 | 0 | |
| HDL timing diagram no-drift gate | GNU Make 4.3 | 0 | |
| Published diagram PNG gate | GNU Make 4.3 | 0 | 6 rasters, 28 controls |
| Milan feature-status consistency gate | GNU Make 4.3 | 0 | |
| Traceability matrix no-drift gate | GNU Make 4.3 | 0 | 69 modules |
| Fetch the builder source dependencies | GNU Make 4.3 | 0 | no-op: all three at their gitlinks |
| Imported gPTP documentation gate (runs `make -C gptp-processor docs`) | GNU Make 4.3 | 0 | |
| Code-quality measurement self-tests | GNU Make 4.3 | 0 | |
| Install the pinned sv2v release | GNU Make 4.3 | 0 | `sv2v v0.0.12` on `PATH` |
| Bare-metal scope gate | GNU Make 4.3 | 0 | 700 arms |
| Install and verify the pinned RV32 SDK | GNU Make 4.3 | 0 | self-test; fresh installation verified (`riscv32-linux-gcc` 14.3.0) |
| Compiler-absent firmware controls | GNU Make 4.3 | 0 | GATE 1b PASS; 2 NOT RUN; 0 compiler invocations (the absent arm) |
| End-station builder gates: `test_builder.py --require-rv32` (1,068 s; runs make probes) | GNU Make 4.3 | 0 | ALL GATES PASS EXCEPT 2 NOT RUN: gate 11 (board build tree), and gate 1b's `MAKEFLAGS += -e` arm, which make 4.3 does not honour (the builder measures this and says so) |
| NVM record-space gate | GNU Make 4.3 | 0 | 0 findings across 5 configs |
| Capture measurement census and clock gate | GNU Make 4.3 | 0 | PASS |
| Saved-state writer gate | GNU Make 4.3 | 0 | 5 shapes, every planted defect reddened |
| SoC source-list gate | GNU Make 4.3 | 0 | iob_pack 21 arms |
| RTL source-list drift gate (consumer expansions via make) | GNU Make 4.3 | 0 | 49 self-test checks |
| Boundary-unit naming ratchet | GNU Make 4.3 | 0 | |
| Port contract gate | GNU Make 4.3 | 0 | |
| Fail-fast ratchet | GNU Make 4.3 | 0 | |
| TODO ownership gate | GNU Make 4.3 | 0 | |
| Test-evidence ratchet | GNU Make 4.3 | 0 | |
| Mechanical hygiene ratchet | GNU Make 4.3 | 0 | |
| SystemVerilog idiom gate | GNU Make 4.3 | 0 | |
| C and C++ idiom gate | GNU Make 4.3 | 0 | |
| Python idiom gate | GNU Make 4.3 | 0 | |
| Shell idiom gate | GNU Make 4.3 | 0 | |
| CI event and SHA contract gate | GNU Make 4.3 | 0 | 1,655 items, 2,206 arms |
| Local act runner contract gate | GNU Make 4.3 | 0 | audited install, sha256 `79579e6b618f1d05fae202018e18f066a23cd8d667202fdbe03b561ecad638f8` |
| Doc cited-path gate | GNU Make 4.3 | 0 | 877 cited paths |
| Archive integrity gate | GNU Make 4.3 | 0 | |
| Per-page contents gate | GNU Make 4.3 | 0 | 127 pages |
| AEM store generator self-test | GNU Make 4.3 | 0 | |
| Sweep/build shape gate | GNU Make 4.3 | 0 | |
| Deploy shape gate | GNU Make 4.3 | 0 | |
| Entity shape gate (`make -pqrR` inventory) | GNU Make 4.3 | 0 | 219 checks, 0 failures |
| `wire-accountability` job | GNU Make 4.3 | 0 | 77 checks, 0 findings |
| `docs-check-no-git` job | GNU Make 4.3 | 0 | 0 findings; feature status 0 findings |

### Also run

| Gate | rc | Result |
|---|---:|---|
| `behave --no-capture -f plain` in `tests/` (the `rtl-fast` step; `scripts/ci_scope.py` lists `REGISTER_MAP.md` among the pages the behave suite reads) | 0 | 14 features, 404 scenarios, 1,968 steps |
| `python3 scripts/lint_rtl.py --check --self-test` | 0 | 90 <= 90 |
| `python3 scripts/check_submodule_docs.py`, `docs/diagrams/submodule_boundaries.gen.py --check` | 0, 0 | 4 exact gitlinks |
| `cd syn/yosys && ./ooc.sh --record-rom-digests`, then `git diff --exit-code syn/yosys/rom_digests.tsv` | 0, 0 | no diff |

### Not run in round 2

- `scripts/run_all_suites.sh`, `syn/yosys/run.sh` and the physical gPTP suite. The round-2 gate list does not name them, and the round-2 diff is Markdown plus one `//!` comment line, so the elaborated RTL is unchanged. Round 1's results stand: 57/57 suites, 54/54 tops, 179 physical checks.
- `elaborate.yml` (no LiteX here) and `act_ci.py --pr 636`. The act replica follows a pushed head, and push is not this lane's.
- Hardware, bench and flashing: not allowed, not needed.

## 5. Parent-visible list (at `420b778a`)

- **Ports and parameters.** `protocol_processor_top` gains input `identify_button_i` and parameter `EN_IDENTIFY_NOTIF_P` (default 0), both from C6. `KL_pp_shadow` ties both to 0. No other top port or parameter changes, and no parent port, pin, SoC, CSR, VERSION (`0x0002_0060`) or firmware changes.
- **C5a, deadline.** An AECP command past its 100 ms deadline is answered:
  - ENTITY_MISBEHAVING, unless a refusal was already chosen;
  - a command that had already changed state answers for itself;
  - a non-AEM message on that path answers NOT_IMPLEMENTED with the command echoed.
  
  There is no top port. The kill ports stay inside the processor, and the three scoreboard kill tie-offs left the processor top (port-contract inventory 62 -> 59).
- **C5a, response-memory fault (round 2, F1).** A non-AEM command whose response memory fails answers NOT_IMPLEMENTED with the command echoed (Milan v1.2 Section 5.4.3.3, Table 5.19; processor PR #140). GET_MILAN_INFO is such a command. At `b2db3a97` the same fault answered ENTITY_MISBEHAVING. AEM commands still answer ENTITY_MISBEHAVING.
- **C5a, hazards.** AECP and ACMP work serialize by hazard class. No top port or parameter.
- **C5b.** These refusals carry the value in force: locked `SET_SAMPLING_RATE`, `SET_CLOCK_SOURCE` and `SET_CONTROL`, and `SET_CONTROL`'s out-of-range refusal. GET_AUDIO_MAP serves pages of 63 to 71 records whole. READ_DESCRIPTOR carries the stored current values. `DESC_LINE_BYTES_P` must lie in 576..1008 in steps of 8, and the parent binds 576.
- **C3.** The ADPDU's current_configuration_index is the processor's configuration row once a SET_CONFIGURATION or D3 restore writes it. `current_cfg_i` (`ADP_IDX0[15:0]`) is the fallback while the row is unset: from reset, and again after a D3 roll-back. `REGISTER_MAP.md` now says so (round 2). The parent image declares one configuration, so the wire is unchanged while `ADP_IDX0` is 0.
- **C6 at the parent's setting (0).** An unsolicited SET_STREAM_INFO carries the 84-byte SET body. IDENTIFY_NOTIFICATION is never originated. The `KL_pp_shadow` rationale now names the ruling as protocol-processor #80 (round 2).
- **C2.** It acts only with `cfg_maap_internal_i` = 1, which the parent ties to 0.
- **C4 and P141.** No RTL change. P141's D3C1 to D3C4 grade SET/GET_CLOCK_SOURCE over ten sources for #629, and `docs/design/MEDIA_CLOCK_FOLLOWING.md` records them as landed at `631eeb34`.
- **ROMs.** `ltn_rom.hex` is unchanged; `ucode.hex` is `518b900c...37f8`.

## 6. Open items for the manager

- Re-review at `420b778a`. R439-1 noted that a docs-only change does not un-cover RTL, Robustness or Tests. The one non-Markdown change is a `//!` comment line in `hdl/milan/KL_pp_shadow.sv`. Whether that line touches those lenses' scope is the reviewers' call.
- Push the five commits, then run the act replica and the hosted contexts on the pushed head.
- Rulings still to publish, carried over from both reviews: `scripts/test_evidence.budget` 77 vs 72; the #495 routing (the stale `milan_dp_gptp` README figure, the `current_cfg_i` comment rewording, the compliance-matrix citations); and the optional REGISTER_MAP memory-bridge pointer.
