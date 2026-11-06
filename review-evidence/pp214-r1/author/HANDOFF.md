# [A736b] HANDOFF: processor issue #214, round 2 (merge main, then gates)

**Status: REVIEW READY at `cc92e90a95376151a9ebd484c429bc53feb8573c`.** Every acceptance item is met
(§10). Every gate below is rc 0 at this head.

- Repository: the processor repository (`git remote get-url origin` checked), branch
  `214-one-vector-per-value`, local, not pushed.
- Base `a9e84b66`; round 1 head `e692a97` (lane [A736], receipts in `pp214-a736/`).
- Main merged: `92100657` (PR #213, issue #212). `git ls-remote` showed main still there at the
  last commit of this round.
- Head: `cc92e90`. On top of `e692a97`:
  - `71357ea` Merge main 92100657 into 214-one-vector-per-value
  - `fefb2b3` Declare one variable per statement in the PV and OV rows and give each OV row its
    own function, Rule 11 (issue #214)
  - `cc92e90` Record the merged testbench's count against the base RTL in the srp_top README,
    8683 checks and 17,650 MRPDUs (issue #214)
- Posts on #214: `[A736b] TAKEN`, an earlier `[A736b] STOP fefb2b3...` (the shard launcher), and
  `[A736b] REVIEW READY` with this head (`receipts/ISSUE-STATUS.txt`).

## 0. What this resume changed

The earlier STOP was the shard launcher, which cannot run this repository. The manager corrected
the instruction: the sweep is `scripts/run_suites.sh`, serial, with make -j16. That STOP is
withdrawn. Auditing the lane found three more things, all fixed, and a fourth arose during the
run (§9):

1. **Two figures the merge moved were never re-measured.** `tb/srp_top/README.md` still read
   `8681 checks: 8673 PASS, 8 FAIL` and 17,643 MRPDUs, beside the 8683 of its first page. The
   merged testbench on the unfixed encoder reads `8683 checks: 8675 PASS, 8 FAIL`, 69 of 17,650
   (`receipts/repro-merged/`). `cc92e90` corrects both; that is its whole diff.
2. **Four campaigns had never been in the chain:** `tb/srp_admission/mutants.py`,
   `tb/name_state/mutants.py`, `tb/elab_guards/mutants.py` and
   `tb/acmp_talker/retry_mutants.py`. Round 1 did not run them either. The first is an SRP
   campaign that runs `srp_top` per arm. All four are now in the chain.
3. **The arm count was off by one.** The diff tool's pattern refused the capital in
   `my-no-walk-at-sLA`, so "269 verdicts" should have read 270. Fixed in `tools/campdiff.py`.

Because `cc92e90` is a new head, every gate ran again at it on fresh clones, rather than arguing
that a README cannot change a result. The parent was rebuilt from `604899c0`, so it is exactly
two commits on top: the gitlink, then the ROM recorder's output. Everything from `fefb2b3` is kept
under `receipts/superseded-fefb2b3/` and nothing there is cited for this head.

## 1. The merge

`git fetch origin main`; `git merge --no-ff origin/main` (the SHA resolved with `git rev-parse`),
subject `Merge main 92100657 into 214-one-vector-per-value`, no body, no trailer, no rebase, no
force. Merge commit `71357ea95e59487a3bd99fe9f15909c2d89ff826`, parents `e692a97` (this branch)
and `9210065779b0` (main). `hdl/` and `docs/` merged without conflict; three testbench files
conflicted where both branches appended, as in the round 1 scratch merge.

Each was resolved with the round 1 scratch merge `c41acbe`'s file, after checking that file
against the conflicted one: every line outside the conflict hunks is in it, in order, and every
line of both sides of every hunk is kept (the three single-line hunks are joined,
`receipts/merge/resolution-check.txt`):

| File | Conflict | Resolution (both sides kept) |
|---|---|---|
| `tb/srp_top/mutants.py` | both appended arms after `talker-leave-copy-rewritten-while-parked`; both extended the coverage list | main's issue #212 block, then this branch's issue #214 block; coverage `("PS", 24), ("LK", 1), ("OV", 7)` |
| `tb/srp_top/sim_main.cpp` | both added a group at the end of `run()` (`link`, `onevec`) and to `main()`'s group list | main's `link` line, then `onevec` and OV0 (so OV0 also reads the `link` group's MRPDUs); both names in the list |
| `tb/srp_top/README.md` | the check count; the `RUN_ARGS` list; the `listener-settle-compare-dropped` row; the coverage paragraph | the count re-measured; `share`, `link` or `onevec`; main's row with this branch's SW change (SW2, SW3 (3), with main's PS cells); main's re-measurement sentence, then this branch's paragraph |

`c41acbe` held the placeholder `MERGED_COUNT` for the count. Its recorder is the suite's own tally:
`make -C tb/srp_top` on the merged tree read `8683 checks: 8683 PASS, 0 FAIL` (main's 8671, plus
this branch's 12), and 8683 was written in.

`listener-shares-nothing-encoder-appends` was flagged in round 1 as needing a re-cut if PR #213
landed first. It did not: `listener-settle-compare-dropped.patch` is unchanged on main, the arm
applies to the merged tree and is killed by name (§5).

## 2. Rule 11: the parent's C++ idiom gate at the merge

The parent's `scripts/check_cpp_idiom.py`, with the merge `71357ea` as the gitlink, failed:

    FAIL: multi-declarator declaration 13 > ratchet 0. ...
    FAIL: long function 1 > ratchet 0. ...

All fourteen findings were this branch's round 1 rows; main's files report 0. The gate's own
`sites()` named them (`receipts/merge/cpp-idiom-sites-71357ea.txt`). `fefb2b3` fixes them without
changing behaviour: one declaration per statement, and `check_one_vector_per_value()`
(`tb/srp_top/sim_main.cpp:3453`) calls one function per row, in the same order, 46 lines at most
(`receipts/merge/fn-lengths-fefb2b3.txt`). Same stimulus, same checks: `tb/srp_top` before and
after reads `8683 checks: 8683 PASS, 0 FAIL` with the same `TOTAL_CLOCKS 227128039`.

## 3. Reproduction

At the base (`receipts/repro-base/`, base `hdl/` with the head's `tb/`): `tb/srp_top` reads
`8681 checks: 8673 PASS, 8 FAIL`, OV0 to OV7; `tb/srp_encoder` reads `692 checks: 644 PASS, 48 FAIL`.

At the merge (`receipts/repro-merged/`, the head's tree with main 92100657's encoder, the only file
under `hdl/` that differs): `8683 checks: 8675 PASS, 8 FAIL`, OV0 to OV7; `692 checks: 644 PASS,
48 FAIL`. OV0 finds 69 of 17,650 MRPDUs carrying a value twice: Domain {6, 3, 2} twice after a
received LeaveAll with a `periodic!` in the window (OV1, 7 of 63 frames), and VID 2 up to eight
times in one MVRP MRPDU (OV5). At the fix both suites pass with 0 FAIL.

The cause and the argument for fixing it at the queueing point are in
`receipts/ORIGINAL-CHANGE.md` §2: the pending tables were append-only, each entry became its own
VectorAttribute, and a value is not the +1 successor of itself, so runs never fold it.

## 4. Changes (file:line at `cc92e90`, clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/srp/KL_srp_encoder.sv:27`, `:78`, `:101` | banner, decision, `ev_ready_o` note: one entry per value, the search's cost | 802.1Q-2022 10.7.7, Table 10-3, 10.7.5.13, 10.8.2.10.1 |
| `hdl/srp/KL_srp_encoder.sv:189`, `:205` | event codes; `key_f`, a value's identity: application, AttributeType, first eight FirstValue octets | 10.8.1.2; 11.2.3.1.7; 35.2.2.8, 35.2.2.8.1, 35.2.2.8.2, 35.2.2.9.1 |
| `hdl/srp/KL_srp_encoder.sv:222`, `:234` | `merge_ev_f`, `merge_fp_f`: the one message a merged entry carries | 10.7.7, Table 10-3; 10.7.6.3, 10.7.6.5, 10.7.6.12; 35.2.2.7.2 |
| `hdl/srp/KL_srp_encoder.sv:421` to `:465`, `:467` (`value_search`), `:481` (`pend_write`), `:496` (`pend_read`) | search through the RAM's own read port, one entry per clock; a hit rewrites in place, a miss appends; a changed offer restarts the search | 10.7.7 |
| `hdl/srp/KL_srp_encoder.sv:679` | a merge takes no new entry | 10.7.7 |
| `tb/srp_encoder/sim_main.cpp:1430`, `:1534` onward | O8 restated (one search clock); PV1-PV12 | acceptance 1, 2 |
| `tb/srp_top/sim_main.cpp:331`, `:503`, `:729`, `:1286`, `:3453` to `:3712` | `doubled_values()` over every frame; OV0; N9 re-cut; OV1-OV10 | acceptance 1, 2 |
| `tb/srp_top/srp_top_wrap.sv:176` | read-only probes that place stimuli in the window | acceptance 1, 2 |
| `tb/srp_top/mutants.py:215`, `:374` to `:390`, `tb/srp_top/mutations/` | eight new arms, two issue #193 arms re-pointed, eight patches re-cut as the same edit | acceptance 2 |
| `docs/architecture/10_srp_engine.md:117`, `:281`, `:389`, `:444`; `docs/architecture/09_verification.md:823`; both suite READMEs | the invariant, the search's latency, the rows, the measured counts | same clauses |

Only `hdl/srp/KL_srp_encoder.sv` changes under `hdl/`. `KL_srp_listener_fsm.sv` has an empty diff
against main. The encoder's module header, parameters and ports, comments stripped, is
byte-identical to main's, so no top-level port, parameter or register-map change exists
(`receipts/IDENTITY.txt`). No MRP timer changes: Milan v1.2 4.2.7.1.1 Table 4.3 (the timer table)
and 4.2.7.2.2 (instantaneous IN to MT on rLv) are both as they were. The brief's "4.2.7.2.2, Table
4.3" names two clauses; both were read (`receipts/STANDARDS.txt`).

## 5. New checks, planted arm, failing words (measured at `cc92e90`)

| Check (failing words) | What it requires | Planted arm | Failing |
|---|---|---|---:|
| `OV1:` to `OV7:`, `OV0:` (`tb/srp_top` onevec) | no MRPDU carries a value twice, through received and own LeaveAll, `periodic!`, LINK_UP and adoption | `second-queueing`: `sr_hit_w` tied 0, every push appends (the base's second queueing) | 8 |
| `PV1 two re-joins of one Domain value` (`tb/srp_encoder`) | the capture's shape at unit level: one JoinIn | `second-queueing` | 46 |
| `OV6:` (LINK_UP, New first) | a later join keeps a pending New | `join-displaces-new` | 2 (OV6, OV7) |
| `PV2 New then a re-join` | same, unit | `join-displaces-new` | 5 |
| `PV4 a re-join then Lv` | a later Lv replaces | `leave-does-not-replace` | 2 |
| `PV5 JoinIn then Mt` | an s replaces only an s | `s-displaces-declaration` | 3 |
| `PV6 Listener Ready then AskingFailed` | the newer declaration type | `listener-type-oldest` | 2 |
| `PV8 three types of one StreamID` | AttributeType in the identity | `merge-ignores-type` | 2 |
| `PV10 a value offered after another` | the search starts again when the offer changes | `search-no-restart` | 3 |
| `SW1:` (`tb/srp_top` share) | one Listener vector per shared stream, now held by two layers | `listener-shares-nothing-encoder-appends` | 6 (OV0, SW1, SW2, SW3) |

OV8, OV9 and OV10 have no killer by construction: they pass at the base too, because the stream
applicants transmit only at tx!. They are property rows for acceptance item 1.

## 6. Processor gates (clean clones of `cc92e90`)

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| elab_guards | 0 | 496 | elab guards: 93 checks: 93 PASS, 0 FAIL |
| gen_matrix_check | 0 | 1 | matrix: OK (94 rows, 0 untested) |
| lint_hdl_5050 | 0 | 33 | LINT OK  protocol_processor_top |
| lint_hdl_5052 | 0 | 57 | LINT OK  protocol_processor_top |
| make_check | 0 | 119 | figures: 3 draw.io, 18 WaveDrom, 5 hand-authored, OK |
| yosys_run | 0 | 196 | YOSYS XILINX OK  KL_aecp_engine |
| check_req_tags_exec | 0 | 0 | req-tags executed: 266 evidence lines, 14 suites, OK |
| run_suites | 0 | 6989 | suites: 1031116 checks total, 0 failing |
| area_head | 0 | 701 | / srp_top_8x8 / 28002 / 4399 / 11297 / 179 / 580 / 190 / |

The sweep ran as the manager specified: `scripts/run_suites.sh`, serial, make -j16, Verilator 5.050.

Sweep: 36 suites of 36, `1031116 checks total, 0 failing`, then the executed traceability check,
266 evidence lines in 14 suites, OK. `srp_top` 8683, `srp_encoder` 692, `srp_stream_fsms` 1512. The
clone was still clean after the run. `git diff --check` against `92100657`: rc 0, no output.

**Memory: the 10 GB target was exceeded.** The sweep, campaigns and parent chain ran concurrently in
one unit. `memory.peak` reached 10,772 MB, at the unit's soft limit, with 40,522 `high` throttle
events, 0 at the hard limit and 0 OOM kills. The largest anon the governor logged was 10,008 MB, so
this was real use, not only cache. No gate was lost to it, but it was over the instruction.

## 7. Campaigns

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| camp-acmp | 0 | 3590 | ACMP mutations: 103 of 103 KILLED by their named checks; goldens PASS |
| camp-acmp-retry | 0 | 226 | PASS: 62 mutants killed; 7 equivalence controls; 1 performance controls; baseline and restored rc 0 |
| camp-adp | 0 | 557 | 62 checks: 62 PASS, 0 FAIL |
| camp-aecp | 0 | 1511 | 67 checks: 67 PASS, 0 FAIL |
| camp-aecp-cmds | 0 | 578 | AECP command decode controls: 17 of 17 detected by their named failures; golden and restored PASS |
| camp-aecp-dispatch | 0 | 3694 | 105 checks: 105 PASS, 0 FAIL |
| camp-ctr | 0 | 476 | 18 checks: 18 PASS, 0 FAIL |
| camp-d3 | 0 | 7988 | D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS |
| camp-elab-guards | 0 | 980 | elab guard mutants: 160 of 160 killed |
| camp-gsi | 0 | 1361 | GSI mutations: 30 detected by named checks; golden and restored PASS |
| camp-maap | 0 | 164 | 32 checks: 32 PASS, 0 FAIL |
| camp-name-state | 0 | 777 | 16 of 16 KILLED by name; golden PASS |
| camp-name-wr | 0 | 138 | Name-write mutation: decode killed; golden and restored PASS |
| camp-notify | 0 | 3301 | C6 notification mutations: 137 of 137 KILLED by their named checks; goldens PASS |
| camp-nvm-figures | 0 | 1187 | all measured figures agree with the tree |
| camp-srp | 0 | 4187 | 291 checks: 291 PASS, 0 FAIL |
| camp-srp-admission | 0 | 817 | 12 checks: 12 PASS, 0 FAIL |

Sixteen mutation campaigns and the `nvm_port` figures gate, every one rc 0, none with an arm that
survived. `tb/acmp_talker`'s 7 equivalence controls and 1 performance control are that driver's own
declared classes, not escapes: the planted edit is required to keep the baseline behaviour or
documented bounds. `acmp` is 103 where round 1 read 101: main's arms.

SRP: rc 0, **291/291**, assertion coverage **174/174**, none missing. 243 arm names declared in
`tb/srp_top/mutants.py` and 243 graded; 270 verdicts, all KILLED by name, 0 UNPROVEN; 20 controls
PASS. That is main's 260 rows (PR #213's arms included) and this branch's 10. Against `fefb2b3`:
270 identical, 0 moved (`receipts/campaigns/fefb2b3-vs-head.campdiff.txt`).

## 8. Area against main 92100657 (the processor's yosys flow)

| Shape | LUT main → head | INV main → head | FF main → head | RAM main → head |
|---|---|---|---|---|
| 2x2 | 13030 → 13536 (+506) | 2981 → 2993 (+12) | 5334 → 5407 (+73) | 114 → 114 |
| 8x8 | 28480 → 28002 (-478) | 4194 → 4399 (+205) | 11224 → 11297 (+73) | 179 → 179 |
| encoder alone | 2420 → 2747 (+327) | 939 → 1016 (+77) | 1280 → 1358 (+78) | 52 → 52 |

The flip-flop figures are exact: the search adds 78 in the encoder (`sr_key_r` 73, `sr_idx_r` 4,
`sr_on_r` 1), and the 2x2 and 8x8 tops net +73. No RAM changes. Read the LUT figures with care:
10 §5.1 records that this flow's LUT count moves by up to about 300 at 2x2 for an edit of a few
LUT. The change adds logic and removes none, so the -478 at 8x8 should be read as flow noise, not a
saving (that is an inference; the flow gives no per-edit attribution). The encoder's own +327 is the
better estimate of the cost. Receipts: `receipts/proc/area/`. The `cc92e90` stats are byte-identical to
`fefb2b3`'s, as `hdl/` is.

## 9. Scratch-parent consumer gate table

Parent `604899c0` plus two local commits, never pushed: `3bb7b202bf` (gitlink to `cc92e90`) and
`fff0311097` (`./syn/yosys/ooc.sh --record-rom-digests`, rc 0, two rows for the new pin).

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| rom_digests | 0 | 0 | ooc.sh: recorded ROM content digests for protocol-processor pin cc92e90a95376151a9ebd484c429bc53feb8573c and g |
| behave | 0 | 10 | 2330 steps passed, 0 failed, 0 skipped |
| cache_selftest | 0 | 171 | cache selftest: OK (unit self-test + 5 original live arms on cdc_pulse + ROM controls) |
| check_cpp_idiom | 0 | 7 | build without warnings: 0 <= 0 |
| check_cpp_idiom_selftest | 0 | 7 | 75 checks: 75 PASS, 0 FAIL |
| check_doc_paths | 0 | 0 | doc path gate: OK (1092 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| check_hygiene | 0 | 1 | HYGIENE RATCHET: PASS (3 population(s), 1308 file(s)) |
| check_port_contracts | 0 | 7 | port contract gate: OK (4081 first-party port(s): hdl 2182, gptp-processor 127, protocol-processor 1772; 347 u |
| check_py_idiom | 0 | 33 | over-long line: 0 <= 0 |
| check_py_idiom_selftest | 0 | 33 | 54 checks: 54 PASS, 0 FAIL |
| check_rtl_source_lists | 0 | 4 | RTL source-list gate: OK (112 files in the milan_datapath closure, 4 of 4 consumer list(s) carry all of them;  |
| check_sh_idiom | 0 | 1 | top-heavy long script: 0 <= 0 |
| check_sh_idiom_selftest | 0 | 1 | 48 checks: 48 PASS, 0 FAIL |
| check_sv_idiom | 0 | 2 | SystemVerilog idiom gate: OK (141 first-party HDL file(s) across the superproject and both processor submodule |
| check_sv_idiom_selftest | 0 | 1 | 55 checks: 55 PASS, 0 FAIL |
| ci_scope_classify | 0 | 0 | syn/yosys/rom_digests.tsv |
| ci_scope_selftest | 0 | 83 | selftest: PASS |
| docs_check | 0 | 22 | docs_check: 0 finding(s) across 213 md files + 1440 scrubbed text files, scrub self-test 23/23, routing arms 4 |
| fw_boundary | 0 | 2502 | ctrl_boundary: PASS |
| fw_coverage | 0 | 707 | firmware coverage: PASS (30 files) |
| fw_coverage_selftest | 0 | 1 | coverage self-test: 29 of 29 planted cases read as planted |
| fw_ctrl_nvm | 0 | 280 | saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests |
| fw_rv32_sdk_selftest | 0 | 5 | OK |
| fw_rv32_selftest | 0 | 22 | RV32 build self-test: 17 checks PASS |
| fw_shard0 | 0 | 889 | test_ctrl_firmware: PASS |
| fw_shard1 | 0 | 3170 | test_ctrl_firmware: PASS |
| fw_shard2 | 0 | 947 | test_ctrl_firmware: PASS |
| fw_shard3_srp | 0 | 1911 | test_ctrl_firmware: PASS |
| fw_tally_selftest | 0 | 10 | tally self-test: 18 of 18 planted cases read as planted |
| fw_verilator | 0 | 1243 | ctrl_boundary: PASS |
| guard_selftest | 0 | 107 | elaboration guard self-test: 36 controls passed |
| lint_rtl | 0 | 42 | LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off) |
| measure_fail_fast | 0 | 7 | FAIL-FAST RATCHET: PASS (78 <= 84 modules without an elaboration contract, 3 <= 4 masked pipeline(s), 0 <= 0 d |
| measure_naming | 0 | 1 | NAMING RATCHET: PASS (95 candidate(s), all recorded by identity; 95 recorded) |
| measure_test_evidence | 0 | 29 | TEST-EVIDENCE RATCHET: PASS (67 <= 77 suite(s) without a mutation arm, 10 <= 10 unseeded draw site(s), 0 <= 0  |
| milan_dp | 0 | 6425 | 6 checks: 6 PASS, 0 FAIL |
| milan_dp_mclk | 0 | 2617 | 34 checks: 34 PASS, 0 FAIL |
| milan_dp_render | 0 | 2876 | 5 checks: 5 PASS, 0 FAIL (--leg-defects: the arms that need no elaboration; the gateware and shape mutants are |
| ooc_read_sets | 0 | 1841 | baseline PASS: 3 endpoints |
| ooc_selftest | 0 | 113 | ooc.sh refusal self-test: 75 arm(s) passed |
| pp_shadow | 0 | 1314 | RESULT: PASS |
| pp_srcs | 0 | 1 | pp source list: 46 tracked source(s) derived; no build input carries a literal copy (self-test passed) |
| publication_census | 0 | 2317 | 26 class-D net(s) from the wrapper cell's ports, 4 unread; 41 read(s) of 22 class-D net(s) in each shape; RESU |
| yosys_elaborate | 0 | 318 | RESULT: PASS |

**The CI venv disappeared mid-run, and fourteen gates were run again.** The venv lived in the round
1 scratch directory, and that whole directory was removed while `milan_dp` ran. No command of this
lane did it; what did was not established. Python then fell through `PATH` to the system's 3.14.8
with no error, which only surfaced when `fw_boundary` failed, rc 2, on `No module named 'migen'`,
importing a Python test before any simulation. Bytecode timestamps date the switch: no 3.14 process
touched the tree before 14:18:13, so every gate ending by 13:25:48 ran on the venv, including both
idiom gates and `fw_shard3_srp`. `milan_dp` straddled it and the rest ran on 3.14.8, so all fourteen
were discarded, though only `fw_boundary` had failed. The venv was rebuilt from the same pins in this
lane's own scratch, and they ran again on clean trees, with each gate asserting the interpreter
before and after (`<gate>.python`, 16 of 16 pinned on both sides). Evidence:
`receipts/parent-chain/INTERPRETER.txt`; the discarded logs are in
`receipts/parent-chain/first-attempt-system-python/` and are not cited.

The firmware gates of that re-run used a byte-exact copy of the parent at the same commit, to run
beside `milan_dp`; head, gitlink and clean state were checked on both trees first.

These are the workflow's `run` steps executed locally on the pinned tools, job by job, not a run of
the workflow itself, so the aggregate `rtl-fast` job, which only collects the others, did not execute.

`check_cpp_idiom.py` reports 0 for every rule. `check_py_idiom.py` is rc 0: every absolute rule is
0, and the four ratcheted rules sit exactly at the parent's budgets (long function 9, long module
10, `os.path` 1, too many parameters 7), so this branch adds none.

Beyond the list asked for, the parent chain also ran the docs-workflow gates that read the
processor tree, `pp_shadow`, whose harness requires the processor's frames on the wire, and
`milan_dp_mclk` and `milan_dp_render`, which compile the processor sources. `csr` was left out: it
does not compile the encoder.

## 10. Acceptance items

1. **Met.** Each value at most once per MRPDU, for MSRP Domain, Talker and Listener and MVRP, through
   a received LeaveAll, an own LeaveAll, `periodic!` and a join in one window: OV0 reads every MRPDU
   of the run, OV1 to OV10 place each case, PV1 to PV12 grade each merge. `tb/srp_top` 8683 of 8683,
   `tb/srp_encoder` 692 of 692.
2. **Met.** OV0 to OV7 and the PV rows fail without the fix, at the base and on merged main (§3), and
   pass at the head. `second-queueing` re-enables the second queueing and fails `OV1:` and `PV1 two
   re-joins of one Domain value` by name (§5).
3. **Met.** All campaigns green, every arm caught by name (§7). Area at 2x2 and 8x8 against main (§8).
4. **Met on the scratch parent.** 43 gates rc 0 with `cc92e90` as the gitlink and the ROM digests
   re-recorded: `milan_dp`, both SRP campaigns, every rtl-fast job's steps, `check_cpp_idiom.py` at 0
   for every rule, and the Python idiom gate (§9). The real parent bump is still to be done.

## 11. Open questions and notes for review

1. **Pre-existing README drift, not touched.** A script comparing `tb/srp_top/README.md`'s per-arm
   counts with the campaign flags 28 of 209 arms. All 28 have the same counts at the base
   `a9e84b66` as here, so this change did not move them. Some are multi-suite rows the script
   reads imperfectly; some may be real drift on main. Worth a separate pass; out of scope here.
2. **A push now waits one clock per pending entry.** For the one hand-over the drain does not wait
   for (the Domain's re-join on a tx! clock), three or more pending Domain entries at the 2x2
   shape let the round's drain start first, so that re-join rides the next MRPDU, one T-MRP-JOIN
   later. LeaveTime is 5 s and two (an adoption's Lv and New) still fit. Written in 10 §3.
   *Recommend:* accept.
3. **The merge also keeps a planted issue #193 Listener defect off the wire.** One Listener vector
   per shared stream is now held twice, so two arms were re-pointed to SW2 and SW4, and SW1 got an
   arm that removes both layers. *Recommend:* accept; the listener arms are still killed in the
   stream-FSM suite unchanged.
4. **Talker identity is the StreamID.** Two Talker values with one StreamID and different other
   fields merge to the newer one; MSRP allows no FirstValue change for an existing StreamID
   (802.1Q-2022 35.2.2.8), and the newer value is what the talker now declares.
5. **The standing STOP comment.** `[A736b] STOP fefb2b3...` stays on the issue, since comments may
   not be edited. The later REVIEW READY supersedes it.
