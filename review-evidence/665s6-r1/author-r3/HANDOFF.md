# #665 S6a, the placement switch, round 3: [A745c] handoff

STATUS: REVIEW READY at `e6d27f3a188286a5d5e30094e07453e2bbea1945` (five commits on round 2's `526f937c`). The finding and every suggestion assigned are done; every gate rc 0 or its stated reason (section 3).

- Lane: `665-s6-placement`, worktree `$LANES/665-s6-placement`, PR #853 (target `dev-soft-core`).
- Base: `origin/dev-soft-core` `a9d69c774dee18b90eead74c9f2dda24cf8fdeb8` (the live tip, re-read 2026-11-08), the merge base. Round 2 head `526f937c` = `origin/665-s6-placement`. No rebase, no force, nothing pushed.
- Prompt note: the prompt asks to confirm the branch "at 6584b7bf"; that is round 1's head. The branch and the remote are at round 2's `526f937c`, which the prompt's first paragraph and both round 2 reviews name, and `6584b7bf` is its ancestor. This round starts from `526f937c`.
- Assignment: R791-2-F1 = R792-2 F-1 (`f0-f4` ruled dead, where it is defined and on the recipe page); R791-2 S1 to S5; the PR body says `scripts/check_solution_docs.py:184` is format-only. Nothing else.
- TAKEN: issuecomment-6718331828 (text in `TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6719257661 (text in `REVIEW-READY-COMMENT.md`).
- Scratch (outside the output directory): `$VALIDATION_STORAGE/scratch/665s6-a745c/` holds the clean clone (`final`), its byte-identical copy for the reviewers' probes (`probes`), the gates' logs (`gates/`) and the replay (`replay/`). Round 2's CI HOME (`$VALIDATION_STORAGE/scratch/665s6-a745b/ci-home`, the pinned RV32 SDK) and its `a9d69c77` checkout (`cmp-a9d69c77`) are reused, read only.

## 1. Changes, file:line and reason

Line numbers are at the head.

| Commit | Item |
|---|---|
| `98d42d30` | F1: `f0-f4` ruled dead |
| `31acb6d3` | S3: lane label and comment IDs on the docs pages |
| `22f43622` | S4: unit names on the four bench nets |
| `daf8d96a` | S1 and S2: the runts, the datapath's drop count, two mutants |
| `e6d27f3a` | S5: the CDC check names a flop by its own net |

### F1 (R791-2-F1 = R792-2 F-1): `f0-f4` ruled dead (`98d42d30`)

- `syn/ooc/pp_placement.py:14-17`, above `PLACEMENTS`: `f0-f4` is ruled dead (#665); the split moves every control protocol to the firmware at once, so no image is built with only F0-F4 moved and no record measures it; do not select or extend it; it is removed at the flip together with the all-fabric placement. `:47`, the `f0-f4` branch of `limits()`: "Ruled dead (#665); removed at the flip with all-fabric." The reason is ruling 6715535566 item 5 and decision 1 of ruling 6088423771 (the engines are not placed one at a time); the comment cites only #665 and names no stage, lane or comment ID. No behaviour changes: `PLACEMENTS` and `limits()` are as before.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:192`: the row reads "`f0-f4` (ruled dead, #665)". `:195-199`: the same statement as the source, one sentence per line as the page writes. `:214`: the `f0-f4` recipe is kept only until the flip removes it, and is not run.
- No other file presents `f0-f4` as live: `MARK_II_AREA_PLAN.md:669` only lists the three names; the self-tests (`pp_placement_selftest.py`, `pp_baseline.py`, `pp_resource_gate_set_selftest.py`) keep exercising it until the flip removes it, as the ruling says.

### S3: labels and IDs on the docs pages (`31acb6d3`)

Each label R791-2-S3 lists, and one more of the same kind on the same page that this PR added (`MAILBOX_SPLIT.md:1363`):

- `docs/ENDSTATION_BUILDER.md:1073` "(#665 F-INT PR 2)" -> "(#665)".
- `docs/design/MAILBOX_SPLIT.md:1332` and `:1363` "(#665 F-INT PR 2)" -> "(#665)"; `:1378-1380` "(ruling 6088423771, decision 1)" -> "(#665): the processor's engines are not placed one at a time, so the split removes the whole wrapper with the parent MAAP once the firmware owns AECP" (that ruling's reason); `:1403` "(ruling 6410169666 item 1)" -> "(#665)" (the reason, the firmware's AECP owner holding the maps, is the sentence itself); `:1756-1757` "(the ruling of comment 6554243203)" -> ", decided in that lane" (the ruling's words; the sentence already cites S11 (#665)).
- `docs/design/SPLIT_CONTROL_MEMORY.md:4` "after F-INT PR 2 (#665)" -> "after the placement switch (#665)"; `:167` "F-INT PR 2 removes the wrapper" -> "The placement switch (#665) removes the wrapper".
- Not changed: the pages' other comment IDs, which predate this PR and which S3 does not list (`MAILBOX_SPLIT.md:145`, `:173`, `:317`, `:365`, `:398`, `:814`, `:825`, `:1161`, `:1329-1330`, the "lane F-INT" rows; `SPLIT_CONTROL_MEMORY.md:88`, `:186-230`, `:262`).

### S4: the bench nets' units (`22f43622`)

- `tb/verilator/milan_dp/tb_split_top.sv:104` `pub_idle_slope_bps`, `:119` `fw_pt_offset_ns`, `:196` `d_idle_slope_bps`, `:204` `d_pt_offset_ns`, and their eight bindings (`:163`, `:176`, `:229`, `:234`, `:258`, `:262`, `:318`, `:322`). The ports they bind have carried the unit since round 2 (R791-F1). Nothing else reads these names.

### S1 and S2: the runts and the datapath's drop count (`daf8d96a`)

- S1, `tb/verilator/milan_dp/sim_split.cpp:572`: the full-FIFO burst gains one 24-byte frame (three words) before the eight 16-byte ones, so the FIFO ends full to its last word. Without it one word stays free, a runt is stored and reclaimed instead of overflowing, and R791-2's arm 1 survives (measured: the first version of the check let it through). `:586-592`: with the byte side still held, `[TAP] the burst leaves the FIFO full to its last word` (a probe of `u_tap.rx_fifo.full`, `tb_split_top.sv:95`, `:379`) guards the next check's power; then eight one-beat (8-byte) runts and `[TAP] ...nor the one-beat runts a full FIFO turns away` (the count unchanged). The burst's conservation and order checks count the 24-byte frame like the others (109 offered).
- S2, `sim_split.cpp:617-635` `check_dp_drops`, run last (`:652`): `[RX] the datapath's drop count reads 0 while its tap has lost nothing`; then 100 ADP ENTITY_DISCOVERs at the MAC back to back, eight bytes a cycle into a tap that drains one (the mailbox drops on a full ring rather than stalling, and `rx_axis_fabric.tready` is 1, `milan_datapath.sv:1755`); `[RX] a burst at the MAC past the tap's FIFO is counted in the datapath's drop count` (> 0) and `[RX] ...and every frame of it is handed out or counted lost` (handed + lost = 100). The probe is `p_rx_drops = u_dp.pp_rx_drops_w` (`tb_split_top.sv:82`, `:367`), the net `PP_DIAG[15:8]` reads (`milan_datapath.sv:3189`). A "reads 0" probe alone cannot catch a tie-off to 0, so the burst is what binds the net.
- `sim_split.cpp:20-28`: the header's `[RX]` and `[TAP]` lines.
- `tb/verilator/milan_dp/split_mutants.py:129-138`: two arms (section 2).
- Docs: `tb/verilator/milan_dp/README.md:109`, `:1134` (`[RX]` row), `:1137` (`[TAP]` row), `:1139-1144` (twenty-four arms, eleven on the encoding, the tap and the drop counts); `docs/design/MAILBOX_SPLIT.md:1431-1434`.
- No RTL file changes: `git diff 526f937c..HEAD -- hdl/` is empty. The tie-off is a mutant of a copy only.

### S5: the CDC check's flop names (`e6d27f3a`)

- `tb/verilator/milan_dp/split_cdc_check.py:175-181` `flop_name`: a flop is named by a name of its Q net that is not a port's; with only a port's name, as "driving <port>"; with none, by its cell. `label_of` (`:183-190`) uses it ("the flop driving <port>" as a source), and so does a flop sink's label (`:200`). The unused first-alias map is gone.
- The window plant now reports `output m_ctr_ans_data_o (sys) reads u_ctr.ans_r (dp)` (was "... reads m_ctr_ans_data_o (dp)", an output reading itself); its required words are now that whole line (`:274`, was only "output m_ctr_ans_data_o (sys) reads"), so the message is held. The LINK plant's flop has only its port's name: `flop driving m_link_up_o (sys) reads d_link_up_i (dp)` (`:266`, was `flop m_link_up_o (sys) ...`). Same refusal, same strength; only the words change.
- Not changed: R792-2 S-2 (a refused clock pin labelled by a Yosys temporary net), which this round's assignment does not include.

### PR body

- `PR-BODY.md` states that `scripts/check_solution_docs.py:184` (round 2) is a format-only change: the pre-existing `Interrupt` `PortGroup` in the file's three-line form, keeping the module under the long-module ratchet; behaviour unchanged.

## 2. New checks, planted defects and failing words

`make -C tb/verilator/milan_dp split`: 71 checks (was 66). `split_mutants.py`: 24 arms (was 22), each caught by the check it names after a clean control passes:

| Planted defect (source) | Caught by |
|---|---|
| a drop count that counts runts: `last_kept_r` also records a frame ending at beat 0, R791-2's arm 1 (`KL_ctrl_split`) | `FAIL [TAP] ...nor the one-beat runts a full FIFO turns away: got 0x34, want 0x2c` |
| the datapath's drop count tied off: the split `ctrl_split`'s `.rx_drops_o` left open and `pp_rx_drops_w` tied to 0 (`milan_datapath.sv`) | `FAIL [RX] a burst at the MAC past the tap's FIFO is counted in the datapath's drop count` |

The guard's own power: with the 24-byte frame removed from a copy of `sim_split.cpp` (restored after, `cmp` equal), the leg fails `FAIL [TAP] the burst leaves the FIFO full to its last word` (1 failure of 71).

R791-2's `tap_reviewer_mutants.py` arm 1, unchanged: "rc 1, caught", by the runt check.

## 3. Gate table

Receipts are under `receipts/` (index: `receipts/INDEX.md`, generated from the files present); host path prefixes in them read `<scratch>`, `<round2-scratch>`, `<lane>`, `<mgmt>`, `<tools>` or `~`. Every row ran at `e6d27f3a` on a clean clone (`git status` empty, submodules at their gitlinks), each command unpiped, its output to the receipt, whose first line names the head. Tools: Verilator 5.050 (pinned build), sv2v 0.0.12, Yosys 0.66.

### The hosted jobs, replayed (round 2's tooling, `scripts/`)

`scripts/run_job.py` replays one job on its own fresh clone and venv; `scripts/verify_jobs.py` reads every `run:` step of the four workflows at the head (matrix expanded) and requires an rc of 0 or a rule of `scripts/not_run.json` for each. This round adds five scope rules at the top of `not_run.json`, for the jobs whose inputs the delta does not touch (no file under `hdl/`, no firmware source or test, no shared bench): `publication-census`, the three firmware mutant campaigns, the `rtl-fast` aggregate, the 19 Verilator shards (the one case whose sources change, the split leg, runs directly below with its mutants) and the Yosys shards. Round 2's replay at `526f937c` ran each of them rc 0.

**Result: 128 steps ran rc 0 (14 of them as a stated substitute), 499 not run with a reason, 0 bad; verifier rc 0** (`receipts/replay/verify.log`, `receipts/replay/jobs-summary.md`; the full table is over 200 KB, so its sha256 is recorded in `jobs-table.md.sha256`; every step's log and rc in `receipts/replay/logs/`).

| Job (workflow) | Why in scope | rc | Result |
|---|---|---|---|
| docs-gates-0 (docs) | every docs page, Python, C++ and SV file touched | 0 each | naming PASS (95 recorded); port contracts OK (hdl 217 <= 217); test evidence PASS (0 unexplained readers, 3 <= 3 wall-clock files); Python, C++, SV, shell idiom held; doc style OK (23 documents); em dash 0 over 217 added lines; solution docs OK |
| docs-check-no-git, wire-accountability (docs) | the docs pages | 0 | 0 findings; PASS |
| docs-gates-1, -2 (docs) | `test_builder.py` reads `ENDSTATION_BUILDER.md`'s section 3 table | 0, 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 1b's retired mutation), `EXCEPT 16 NOT RUN` (arms needing LiteX) |
| elaborate-gates-0, -1 (elaborate) | the same table | 0, 0 | `EXCEPT 1 NOT RUN` (gate 1b), `EXCEPT 1 NOT RUN` (gate 11, an earlier board build's report not on this host); 8 of 8 LiteX simulations |
| changes, verilator-lint (rtl-fast) | the bench | 0 | rtl=true; `LINT GATE: PASS (89 <= 89)` |
| yosys-tool, yosys-elaboration (rtl-fast) | `pp_placement.py` (the baseline and resource gate self-tests) | 0 each | PASS |
| bdd-conformance (rtl-fast) | `tests/` reads docs | 0 | 14 features, 508 scenarios, 2,330 steps |
| firmware-unit (rtl-fast) | `ctrl_service_bounds.py` reads `MAILBOX_SPLIT.md` | 0 each | `test_ctrl_firmware: PASS`; saved-state store 435 tests over 5 shapes; coverage PASS |
| firmware-boundary, firmware-verilator (rtl-fast) | the assignment names it; the bench's compiled sources | 0, 0 | `ctrl_boundary: PASS` each |
| full-ci-gate (rtl) | the scope decision | 0 each | run_full true; its default-branch step read "unreadable" (the replay forwards no credential) and warns, as it does on a pull_request; read with the host's login: `dev` (`gates/default-branch.log`) |

### The lane's own gates and the findings' verification steps

| Gate | Command | rc | Result | Receipt |
|---|---|---|---|---|
| R791-2-F1 / R792-2 F-1 | read `pp_placement.py:14-17`, `:47` and the recipe page `:192`, `:195-199`, `:214` | - | each states the ruling | section 1 |
| Placement self-test (F1's step) | `python3 syn/ooc/pp_baseline.py --selftest` (imports `pp_placement_selftest`); `pp_placement_selftest.py` itself, unchanged | 0, 0 | every placement check PASS | `gates/pp-baseline-selftest.log`, `gates/pp-placement-selftest.log` |
| Delta scan (F1's step) | added lines of `526f937c..HEAD` against lane, review and stage labels and comment IDs | - | no match | `gates/delta-label-scan.log` |
| Python idiom, doc style (F-1's step) | `check_py_idiom.py`; `check_doc_style.py`; `doc_style_added.py 526f937c` | 0 each | ratchets held; OK (23 documents); the five touched pages are outside the gate's population (their added lines are listed against its rules for the record) | `gates/py-idiom.log`, `gates/doc-style.log`, `gates/doc-style-added-lines.log` |
| C++ idiom, em dash | `check_cpp_idiom.py`; `check_em_dash.py --base a9d69c77` | 0, 0 | held; 0 over 217 added lines | `gates/cpp-idiom.log`, `gates/em-dash.log` |
| Split leg | `make -C tb/verilator/milan_dp split` | 0 | 71 checks, 0 failures | `gates/split-leg.log` |
| The full-FIFO guard's power | the leg with the 24-byte frame removed from a copy | 1 (required) | `FAIL [TAP] the burst leaves the FIFO full to its last word` | `gates/split-leg-without-24-byte-frame.log` |
| Split mutants | `make -C tb/verilator/milan_dp split-mutants` | 0 | control passes; 24 of 24 caught | `gates/split-mutants.log` |
| CDC structure | `make -C tb/verilator/milan_dp split-cdc` | 0 | 253 sinks; 13 of 13 (the control and 12 plants) | `gates/split-cdc.log` |
| S1's verification | R791-2's `tap_reviewer_mutants.py` arm 1, unchanged | 0 | arm 1 "rc 1, caught" | `gates/r791-2-tap-mutant-1.log` |
| S5 against the reviewers' probes | R791-2 `cdc_plants.py`, `cdc_extra_plants.py`; R792-2 `cdc_allowance_probes.py`; R792-1 `cdc_check_probes.py`; each unchanged, on a byte-identical copy of the clone | 0 each | 0 let through; 7 of 7, 0 unexpected; 11 probes, 0 departures; 5 probes, 0 departures | `gates/r79*-*.log` |
| Lint | `scripts/lint_rtl.py --check --self-test` | 0 | `LINT GATE: PASS (89 <= 89)` | `gates/lint.log` |
| All-fabric identity, 6 shapes | `placement_identity.py --dump` (head; base `a9d69c77`, round 2's checkout), `--compare` | 0, 0, 0 | every digest equal, and equal to round 2's | `gates/identity-*.log`, `gates/ident-*.json` |

Not run, with the reason: the full sweep (no RTL or shared bench change; the assignment needs none); the census, the population, the export compare, the builder bank outside its CI legs, the Vivado placement and xvlog (their inputs are unchanged since round 2 at `526f937c`: no RTL change); the hosted contexts (this PR targets `dev-soft-core`, so no act replay runs; the hosted checks are the CI evidence once the head is pushed).

## 4. Not done, and why

- **The pages' older comment IDs** (`MAILBOX_SPLIT.md:145`, `:173`, `:317`, `:365`, `:398`, `:814`, `:825`, `:1161`, `:1329-1330` and the "lane F-INT" rows; `SPLIT_CONTROL_MEMORY.md:88`, `:186-230`, `:262`). They predate this PR, and S3 lists only the seven it names; the one more taken (`MAILBOX_SPLIT.md:1363`) is this PR's own and the same label.
- **R792-2's suggestions** (S-1 the bench port `p_pt_offset0`, S-2 the clock-pin message's temporary path, S-3 to S-6): not assigned this round. S-1's four nets are R791-2-S4's, done.
- **`docs/testing/PP_SHADOW_BASELINE_RECIPE.md:206-208`** still says that at `7c1b52be` the `--ctrl-mailbox` datapath connections are idle and the first M0s route is STOP. It sits beside this round's edit, but is outside F1, which concerns `f0-f4`; it is the same staleness R792 D-1 found elsewhere, for the manager to route.
- **Carried from round 2**, unchanged: `KL_pp_shadow`'s identical uncounted drop (R791-F4's Issue, the manager's to open); `sw/firmware/ctrl/plat/README.md:137` (S2b's tree); the seven split-leg paths the reviewers' mutants pass (S6b's).
