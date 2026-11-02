# [A711d] R1 register reference (#797): handoff, round 4

Status: REVIEW READY at the head below. Every docs-workflow step that can run here is rc 0 on clean clones of the head. Local branch; the manager pushes.

- Branch `797-r1-regref`. Head `79fdea05ef` (full SHA and tree in `receipts/gates/HEAD.txt`), five local commits on `e90284bd`.
- Base: dev `1f29f189`, one merge base. Nothing was merged or rebased. During the round dev moved to `503bc97c` (PR #828, #640 documentation). It touches none of this PR's files, and the merge base is still `1f29f189` (`receipts/merge_base_after_dev_moved.txt`). The candidate merge with live dev is the manager's.
- Origin verified: `https://github.com/kebag-logic/milan-fpga.git`. Round 1 branched from dev `1e80128f`, an ancestor of the head.
- Submodules at their pins, unchanged. Each of the four the docs jobs fetch was verified as its own top level, with its own origin (`protocol-processor`: the processor repository), before any read.
- TAKEN: issuecomment-6573241681 (`taken_posted.md`). REVIEW READY: issuecomment-6574144047 (`review_ready_posted.md`).
- Receipts: `receipts/INDEX.md`, generated from the files present, host paths replaced. Tools: `tools/`.
- Round 3's handoff, `../797-a711c/HANDOFF.md`, still describes everything this round did not touch.

## Assignment as read

R753-3 and R754-3 on PR #825 are NEGATIVE at `e90284bd` with one MINOR each, both a read-table row false as printed.

- R753-3 F1: `STRMW_SRP` says `STRM_SEL[9]` "selects the listener row"; at `SEL` `0x300` the read is 0. State the condition by the bit's value, with the finding's wording.
- R754-3 F1: the `RENDER_STAT` row holds only at `N_LISTENERS_P` = 1. Make it true on any build, with the finding's proposed row unless the RTL says otherwise.
- The class: the sweep read a clause by the generator's flop, not as printed, and left five tables out. Extend it to all 17 read tables on the shipping and the 2x2 build, map every clause to the printed words, report disagreements per table, and fix every row it finds false, listing those neither reviewer named.
- Not this round: the suggestions, a new gate or diagram, text moved between pages, any search beyond the 17 tables, a dev merge. STOP if a row needs an RTL change. None did.

## Commits

One per finding plus one for the sweep. One-line subjects, no body, no trailer. Each fix commit regenerates the page through the generator and is `--check` fresh.

| Commit | Subject |
|---|---|
| `fd12faf9` | Sweep all 17 read tables on the shipping and a 2x2 build, reading each clause as the page prints it |
| `7c508db4` | State the STRMW_SRP index-0 conditions by the value of STRM_SEL[9] |
| `dbe2b143` | Read the RENDER_STAT listener loop as one selection, so its read table holds at any N_LISTENERS_P |
| `f7f6ea7d` | State that an SRP-served word needs a poll answer since the last STRM_SEL or STRMW_CTRL write, since a provisioning write's answer leaves it 0 |
| `79fdea05` | State the CHMAP_LOOP read conditions by the value of CHMAP_SNAP[1], since a re-armed or timed-out readback reads the poison |

## Each change, with file:line and its reason

`P` is `docs/reference/REGISTER_MAP.md`, `J` is `scripts/register_descriptions.json`, `S` is `scripts/register_read_sweep.py`. Lines are at the head.

### The sweep: `fd12faf9`

- **What:** `S` builds `milan_csr` with Verilator at the page's "Build parameters" (`S:134`) and at `N_LISTENERS_P` = `N_TALKERS_P` = 2 with `SRP_LSN0_ROW_P` 4 (`S:60`). The harness (`S:213`) drives `STRM_SEL` with `[9]`, `[8]` and indices 0, 1, 2, 3, 15. It adds an ACMP answer, an SRP answer to a poll, to a provisioning write, or to both, a running snapshot, and three counter-kind patterns. It reads every word that has a read table. `CHMAP_LOOP` gets seven readback states: never, answered, re-armed in flight, timed out, answered, re-armed, timed out.
- **The class closed:** `CLAUSE` (`S:77`) maps each printed clause to what the harness did, or to what it read back through a register: `STRM_SNAP[0]`, `CHMAP_SNAP[1]`, the written `STRM_SEL` bits. It never reads the flop the generator worded. A table answers only while the block asks, the engines' contract. A clause or value cell it cannot read refuses (exit 2). Every table's words are read, so a new table is swept without an edit.
- **Where the sweep sets state inside the block:** the counter kinds and the latched snapshot words are deposited, and the clause that reads them names the recorded kind. `mac_wire_w` is read from the model for the value column only.
- **Why in `scripts/`, not a gate:** it needs Verilator and a C++ compiler, and the assignment adds no gate. `scripts/check_py_idiom.py` holds it.

### R753-3 F1: `7c508db4`

- `J:4094`, `J:4095`: `srp_idx0_ls_w` is worded "`STRM_SEL[9]` is 1" and "is 0", the finding's text. `J:3406` and `P:3634`: "Index 0 with `STRM_SEL[9]` at 0: the live `LWSRP_STATUS` word. ...", the finding's text. `P:3638`, `P:3639` follow.
- **Reason:** `milan_csr.sv:2528` has no direction term, so at `SEL` `0x300` the read takes the SRP arm (`:2574-2576`). On every datapath build `SRP_LSN0_ROW_C` (`milan_datapath.sv:1891`) is at least 1, so `srp_idx0_ls_w` equals the bit.
- **Check:** `receipts/sweep/s1_after_r753_f1.txt`. Every `SEL` `0x300` disagreement of `s0` is gone. What remains in `STRMW_SRP` is the provisioning-write state, fixed in `f7f6ea7d`.

### R754-3 F1: `dbe2b143`

- `scripts/register_sv.py:867` `selection`, called at `:833`: a `for (v = 0; v < N; v++) if (c && x == v) t = f(v);` loop with `N` a named constant is read as `if (c && x < N) t = f(x)`. At most one pass assigns, so this is exact. It no longer folds at the shipping `N`. `:849` `substitute` and `:860` `conjuncts` serve it. The only loop in the read paths is `milan_csr.sv:2447`.
- `scripts/register_page.py:788` `named`, called at `:781`: a pair of row terms that is one arm of a worded wire prints as that wire. With `strm_dir_r` at 0, `win_in_range_w` is `strm_idx_r < N_LISTENERS_P` (`milan_csr.sv:1109-1110`). The wire takes the choice's place and the choice stays.
- `scripts/register_fields.py:242`: `x[i*w +: w]` with `i` unknown names word `i` of `x`, so the field keeps its name `RENDER_STATUS`.
- **Page:** `P:3974` reads "the selected stream exists and `STRM_SEL[8]` selects a listener", the finding's proposed row. The RTL agrees: `milan_csr.sv:2445-2451` with `:1109-1110`. No other line of the page changed.
- **Check:** `receipts/sweep/s2_after_r754_f1.txt`: `RENDER_STAT` 0 on both builds, every row hit on 2x2.

### Found by the sweep, named by neither reviewer: `f7f6ea7d`

- **Rows:** `STRMW_SID_LO` `P:3462`, `STRMW_SID_HI` `P:3483`, `STRMW_SRP` `P:3639`, `P:3640`. Each said "the SRP table answered since the last selection".
- **Why false as printed:** the table's answer to a provisioning write clears `srp_fresh_r` (`milan_csr.sv:3113-3115`), and the `STRMW_CTRL` write that starts it clears it too (`:3120-3128`). The read is 0 although the table answered. `s1` holds 168 such reads, `srpw=1 srppoll=0` in each line.
- **Fix:** `J:4086`, `J:4087`: "the SRP table answered a poll since the last `STRM_SEL`/`STRMW_CTRL` write". A slash, because `and` or `or` inside a clause would split the cell. Each row using it already requires a selection whose `STRMW_CTRL` write provisions (`:3091-3093`).
- **Check:** `receipts/sweep/s3_after_srp_poll.txt`: the three tables at 0 on both builds.

### Found by the sweep, named by neither reviewer: `79fdea05`

- **Rows:** `CHMAP_LOOP` `P:4269`, `P:4270`. They said "a channel-map readback has completed".
- **Why false as printed:** a re-arm clears `cmrd_valid_r` (`milan_csr.sv:2773`), and a timeout ends a readback with it at 0 (`:2791-2794`). After a completed readback both read the poison, although a readback has completed. 4 reads per build.
- **Fix:** the `cmrd_valid_r` entry is deleted from `condition_words` in `J`. The generator then names the bit by the field software reads it at: "`CHMAP_SNAP[1]` is 1" and "is 0". That field's row says "Valid: the last snapshot carries fabric data."
- **Check:** `receipts/sweep/s4_after_chmap.txt`: 0 disagreements, every table on both builds.

## The sweep, per table

`receipts/sweep/`. `s0` is the sweep at `fd12faf9` on the `e90284bd` page, and `s4` is the head. 24,007 reads per build: 960 per window word, 9,600 for `STRMW_CNTn`, 7 for `CHMAP_LOOP`.

| Table | `s0` shipping | `s0` 2x2 | Head shipping | Head 2x2 |
|---|---:|---:|---:|---:|
| `STRMW_CTRL` | 0 | 0 | 0 | 0 |
| `STRMW_SID_LO` | 0 | 24 | 0 | 0 |
| `STRMW_SID_HI` | 0 | 24 | 0 | 0 |
| `STRMW_DMAC_LO` | 0 | 0 | 0 | 0 |
| `STRMW_DMAC_HI` | 0 | 0 | 0 | 0 |
| `STRMW_FMT_LO` | 0 | 0 | 0 | 0 |
| `STRMW_FMT_HI` | 0 | 0 | 0 | 0 |
| `STRMW_STATE` | 0 | 0 | 0 | 0 |
| `STRMW_CNTn` | 0 | 0 | 0 | 0 |
| `STRMW_PDUS` | 0 | 0 | 0 | 0 |
| `STRMW_SRP` | 60 | 108 | 0 | 0 |
| `STRMW_CTLR_LO` | 0 | 0 | 0 | 0 |
| `STRMW_CTLR_HI` | 0 | 0 | 0 | 0 |
| `STRMW_BIND` | 0 | 0 | 0 | 0 |
| `STRMW_RSVD_86C` | 0 | 0 | 0 | 0 |
| `RENDER_STAT` | 0 | 96 | 0 | 0 |
| `CHMAP_LOOP` | 4 | 4 | 0 | 0 |
| **Total** | **64** | **256** | **0** | **0** |

- **Coverage:** the 2x2 build hits every printed row. The shipping build leaves 6 rows unhit, each needing an index above 0, which it does not have (`s4` lines 3 to 48).
- **The sweep can fail:** `receipts/sweep/controls.tsv` (`tools/sweep_controls.py`). On a copy of the head's page: baseline 0; the `e90284bd` `RENDER_STAT` row, an index-0 `STRMW_SRP` row without `[9]`, swapped `CHMAP_LOOP` values, a `STRMW_CNTn` RAW row reading the poison, and a `STRMW_SID_LO` row without its SRP clause each exit 1. A clause it cannot read exits 2. A new table at 0x7FC exits 1 with no sweep edit.

## Findings count per area

| Area | R753-3 | R754-3 | Fixed |
|---|---:|---:|---:|
| Read-table rows false as printed | 1 (F1) | 1 (F1) | 2 |
| Rows found false by the sweep, named by neither | - | - | 2 |
| Suggestions | 4 | 5 | 0, not taken |
| Residue | 3 | 3 | R753 RES1 and R754 R3 are PR-body text, taken there. R754 R2 is R753 F1's fix. R753 RES2, RES3 and R754 R1 are outside the 17 tables, left for the manager's residue list |

## Generator and freshness gate

Unchanged in shape: step "Register reference freshness gate" of `.github/workflows/docs.yml`, `id: gate_50`. `--selftest`: 61/61. No control was added: freshness holds each change, as the mutants show.

`receipts/mutants/generator_mutants.tsv` (`tools/generator_mutants.sh`): each undoes one change of this round in an export of the head and runs `--check` with no `--write`.

| Mutant | `--check` |
|---|---|
| baseline | rc 0, fresh |
| `selection` off | rc 1, STALE |
| `named` off | rc 1, STALE |
| the `x[i*w +: w]` naming off | rc 2, refuses `RENDER_STAT.RENDER_STATUS` |
| `srp_idx0_ls_w` old wording | rc 1, STALE |
| `srp_fresh_r` old wording | rc 1, STALE |
| `cmrd_valid_r` phrase restored | rc 1, STALE |

The third column of that file compares the export with the lane's `scripts/`. The 73 files it counts at baseline are the lane's `__pycache__`.

## Dropped statements

Only generated rows of this PR changed. None was on the old page, so round 3's `receipts/survival.txt` is unchanged.

| Dropped | Why, with the RTL line |
|---|---|
| "Index 0, unless `STRM_SEL[9]` selects the listener row" and "`STRM_SEL[9]` (does not) select(s) the listener row at index 0" | Contradicted at `SEL` `0x300`: `milan_csr.sv:2528`, `:2574-2576` |
| "`STRM_SEL[8]` selects a listener and the stream index `STRM_SEL[3:0]` is 0" (`RENDER_STAT`) | Contradicted above `N_LISTENERS_P` = 1: `milan_csr.sv:2445-2451` |
| "the SRP table answered since the last selection" | Contradicted after a provisioning write: `milan_csr.sv:3113-3115`, `:3120-3128` |
| "a channel-map readback has completed" and its negation | Contradicted after a re-arm or a timeout: `milan_csr.sv:2773`, `:2791-2794` |

## Open risks and decisions

1. **The harness is `milan_csr` alone.** The engines are answers on their ports, and the counter kinds and snapshot words are deposited. The datapath ties the SRP grant and `i_srp_ctx_stolen` to 0 (`milan_datapath.sv:3010`, `:8720`). So SRP-answered states exist only in the harness, and a stolen beat is not swept.
2. **The `STRM_SEL[9]` wording relies on `SRP_LSN0_ROW_P` being nonzero.** It is on every datapath build (`milan_datapath.sv:1891`). A bare `milan_csr` at its default 0 would read the alias at `[9]` = 1.
3. **R754-3 S1 stands:** at `SEL` `0x300` on 2x2 the poll presents row `N_LISTENERS_P - 1`, also listener 1's row. No read disagrees, and the suggestion was not taken.
4. Round 3's risks 1, 3, 6 and 7 stand: ETH_GUARD, unrendered Mermaid, statements read rather than simulated, and the lane conflict with PR #815.

## Gate table

Method as rounds 2 and 3: each step of the head's `.github/workflows/docs.yml` ran as its job runs it, read from the workflow by `../797-a711b/tools/run_docs_workflow.py`, one `bash -e` script per step, output to a file, never piped. Each job had its own fresh clone of the head, and `docs-check-no-git` its own export clone. The jobs fetched their submodules at the pins. Three job chains ran at once (`tools/run_all_gates.sh`). After the run every clone was at the head with an empty status (`gates/clones_after.txt`). Logs and rc files: `receipts/gates/`.

| Job | Step id | Name | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 | Submodule path 'gptp-processor': checked out '135afd043309369a87ddbc8d6550aff8ec52a157' |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 0 | 0 | RESULT: PASS |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 |  |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | Wrote: /tmp/a711d/gates/scratch-docs-gates-0/runner_temp/docs-gates-0/milan-hdl-reference/ |
| docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | docs_check: 0 finding(s) across 213 md files + 1688 scrubbed text files, scrub self-test 2 |
| docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | check_em_dash: 0 finding(s) over 6722 added line(s) in 45 changed Markdown page(s), 0 mirr |
| docs-gates-0 | gate_9 | Concise audience documentation gate | 0 | gPTP documentation selftest: OK (30 controls) |
| docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 | time-sync diagram selftest: OK (source, status, XML, raster) |
| docs-gates-0 | gate_11 | Product solution source-fact gate | 0 | solution documentation selftest: OK (45 mutation controls) |
| docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 | submodule documentation selftest: OK (table and diagram controls) |
| docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 | WaveDrom current: docs/diagrams/wd_gptp_pdelay.json |
| docs-gates-0 | gate_14 | Published diagram PNG gate | 0 | diagram PNG selftest: OK (6 rasters, 28 mutation controls) |
| docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 | traceability matrix up to date (80 modules, 0 untested <= ratchet 0, 0 archived) |
| docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 | Submodule path 'third_party/verilog-axis': checked out '48ff7a7e2ef782cf778d47910cf85835c6 |
| docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 | source evidence selftest: PASS (7 arms) |
| docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 | 18 checks: 18 PASS, 0 FAIL |
| docs-gates-0 | gate_21 | Bare-metal scope gate | 0 | baremetal-only selftest: PASS (867 arm(s)) |
| docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 | GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations |
| docs-gates-0 | gate_26 | NVM record-space gate | 0 | 0 finding(s) across 5 config(s): the inventory's (group, index) key set is exactly the set |
| docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 | PASS: capture census, clocks, both timing arms and receipt agree |
| docs-gates-0 | gate_28 | Saved-state writer gate | 0 | saved-state writer gate: OK across 5 shape(s), and every planted defect reddened |
| docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without  | 0 | iob_pack_selftest: 22 arms, 21 mutants, 0 failure(s) |
| docs-gates-0 | gate_30 | RTL source-list drift gate | 0 | 50 checks: 50 PASS, 0 FAIL |
| docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 | 66 checks: 66 PASS, 0 FAIL |
| docs-gates-0 | gate_32 | Port contract gate | 0 | 82 checks: 82 PASS, 0 FAIL |
| docs-gates-0 | gate_33 | Fail-fast ratchet | 0 | 106 checks: 106 PASS, 0 FAIL |
| docs-gates-0 | gate_34 | TODO ownership gate | 0 | 45 checks: 45 PASS, 0 FAIL |
| docs-gates-0 | gate_35 | Test-evidence ratchet | 0 | 105 checks: 105 PASS, 0 FAIL |
| docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 | 35 checks: 35 PASS, 0 FAIL |
| docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 | 55 checks: 55 PASS, 0 FAIL |
| docs-gates-0 | gate_38 | C and C++ idiom gate | 0 | 75 checks: 75 PASS, 0 FAIL |
| docs-gates-0 | gate_39 | Python idiom gate | 0 | 54 checks: 54 PASS, 0 FAIL |
| docs-gates-0 | gate_40 | Shell idiom gate | 0 | 48 checks: 48 PASS, 0 FAIL |
| docs-gates-0 | gate_43 | Doc cited-path gate | 0 | doc path gate: OK (1091 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within t |
| docs-gates-0 | gate_44 | Archive integrity gate | 0 | archive selftest: OK (24 controls) |
| docs-gates-0 | gate_45 | Per-page contents gate | 0 | TOC gate: OK (151 page(s) carry an annotated contents list, 18 below the 3-section thresho |
| docs-gates-0 | gate_46 | AEM store generator self-test | 0 | gen_aem_store self-test: PASS |
| docs-gates-0 | gate_47 | Sweep/build shape gate | 0 |   [self-test] OK: 1 drift(s) reported |
| docs-gates-0 | gate_48 | Deploy shape gate | 0 |   [selftest] OK: 1 drift(s) reported |
| docs-gates-0 | gate_49 | Entity shape gate | 0 | RESULT: PASS |
| docs-gates-0 | gate_50 | Register reference freshness gate | 0 | memory map diagram: fresh |
| docs-gates-0 | ci_step_53 | Fetch inventory dependencies | 0 | Submodule path 'third_party/tsn-c-stack': checked out '70936b77dc41981e192438388cd0aced699 |
| docs-gates-0 | gate_51 | CI scheduling and evidence controls | 0 | manifest comparison controls: PASS |
| docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 | Submodule path 'third_party/verilog-axis': checked out '48ff7a7e2ef782cf778d47910cf85835c6 |
| docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 | ALL GATES PASS |
| docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 | Submodule path 'third_party/verilog-axis': checked out '48ff7a7e2ef782cf778d47910cf85835c6 |
| docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 | selftest: PASS (2207 contract items, 5271 arms) |
| docs-gates-2 | gate_42 | Local act runner contract gate | 0 | selftest: PASS |

58 steps ran, 0 not rc 0, 38 not run.

Not run: wire-accountability: Record actual job execution; docs-check-no-git: Retain checkout identity before removing metadata; docs-check-no-git: Record actual job execution; docs-gates-0: Install the python gate dependencies; docs-gates-0: Install the pinned Markdown renderer; docs-gates-0: Resolve exact package downloads 6; docs-gates-0: Install diagram gate dependencies; docs-gates-0: Install the pinned sv2v release; docs-gates-0: Record executed gate outcomes; docs-gates-0: Record actual job execution; docs-gates-1: Install the python gate dependencies; docs-gates-1: Install the pinned Markdown renderer; docs-gates-1: Resolve exact package downloads 4; docs-gates-1: Install diagram gate dependencies; docs-gates-1: Install the pinned sv2v release; docs-gates-1: Record executed gate outcomes; docs-gates-1: Record actual job execution; docs-gates-2: Install the python gate dependencies; docs-gates-2: Install the pinned Markdown renderer; docs-gates-2: Resolve exact package downloads 4; docs-gates-2: Install diagram gate dependencies; docs-gates-2: Install the pinned sv2v release; docs-gates-2: Record executed gate outcomes; docs-gates-2: Record actual job execution; docs-check: Set CPU-derived job budgets; docs-check: Install the pinned evidence reader; docs-check: Require every gate exactly once; docs-check: Record actual job execution; ci-manifest: Set CPU-derived job budgets; ci-manifest: Fetch inventory dependencies; ci-manifest: Install the pinned evidence reader; ci-manifest: Collect actual runtime evidence; ci-fail-fast: Set CPU-derived job budgets; ci-fail-fast: Observe the first failed job; ci-fail-fast: Cancel this run and sibling workflows; ci-fail-fast: Record actual job execution; ci-cancel-tail: Set CPU-derived job budgets; ci-cancel-tail: Cancel confirmed terminal failures.

Reasons for the steps not run, as rounds 2 and 3:

- **`Record ...`, `Retain checkout identity`:** GitHub run evidence only.
- **`Install ...`, `Resolve exact package downloads`:** apt, sudo or pip. The host and venv already hold these tools. The runner also drops the `python3 -m pip install` lines inside gate steps and leaves their other commands intact.
- **Jobs `docs-check`, `ci-manifest`, `ci-fail-fast`, `ci-cancel-tail`:** they verify uploaded CI receipts or cancel runs, so they run only on GitHub.

Builder leg 1 reports `ALL GATES PASS EXCEPT 16 NOT RUN` with rc 0, as in rounds 2 and 3. `docs-gates-2__gate_41.log` is over the size limit: its digest, size and tail are in `gates/docs-gates-2__gate_41.log.tail`.

Also on this head, on the clean clone of `docs-gates-0`:

| Check | rc | Receipt |
|---|---:|---|
| `git diff --check 1f29f189 HEAD` | 0 | `gates/lane__diff_check.rc` |
| `git merge-base --all origin/dev HEAD`: one base, `1f29f189` | 0 | `gates/lane__merge_base.txt` |
| `gen_register_reference.py --selftest`, standalone: 61/61 | 0 | `gates/lane__selftest.log` |
| `gen_register_reference.py --check`, standalone | 0 | `gates/lane__check.log` |
| `register_read_sweep.py`: 17 tables, 0 disagreements on both builds | 0 | `gates/lane__read_sweep.txt` |
| Clone status after the run: 0 lines | 0 | `gates/lane__clone_status_after.txt` |
| Sweep controls: 8 of 8 as wanted | 0 | `sweep/controls.tsv` |
| Generator mutants: 6 of 6 fail `--check` | - | `mutants/generator_mutants.tsv` |

Not run: the Verilator suites, Yosys and the behave suite (documentation lane, no RTL changed). No hardware, no Vivado.
