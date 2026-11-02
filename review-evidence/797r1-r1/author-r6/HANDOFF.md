# [A711f] #797 lane R1, round 6 handoff

- Head: `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2`, parent `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d`. Local branch `797-r1-regref` (PR #825). Nothing pushed; the manager pushes.
- Lane base: branched from dev `1e80128f`, dev `1f29f189` merged in an earlier round; `git merge-base --all origin/dev HEAD` gives one base, `1f29f189` (live dev is `503bc97c`, not merged). Origin `https://github.com/kebag-logic/milan-fpga.git`.
- Posted on #797: TAKEN issuecomment-6576239786; REVIEW READY issuecomment-6576760481 (text in `review_ready.md`).
- Receipts: `receipts/INDEX.md`, generated from the files present, host paths replaced. Tools: `tools/`.

## Assignment

R753-5 F1 (issuecomment-6576201147) and R754-5 F1 (issuecomment-6576176288), the same MINOR, Tests lens: no swept state separates the clear of `srp_fresh_r` on a provisioning `STRMW_CTRL` write (`hdl/common/csr/milan_csr.sv:3128`, gated by `srp_prov_w`), so the m4 mutant (that clear deleted) passed the sweep with 0 disagreements.

- Required: the sweep drives a poll answered, then a provisioning `STRMW_CTRL` write posted and left unanswered, then reads the words. The docstring (`register_read_sweep.py:17-20` at `ef7dc985`) describes the orders the modes actually drive.
- Verification: the sweep exits 0 on both builds at the new head; m4 exits 1; m1, m2 and m5 still exit 1; the round 4 wording planted back still exits 1.
- STOP condition: a page or description change becomes necessary. It did not: the head page passes in the new state on both builds, with no generator, page or description edit.

## The change: one commit, `2c500d0a`

Subject: "Sweep a poll answered and then a provisioning STRMW_CTRL write left unanswered, so the write's clear of the SRP-served word is read (#797)". One file, `scripts/register_read_sweep.py`, +21/-11 (`receipts/lane/delta_ef7dc985_2c500d0a.diff`). Lines are at the head.

| Where | Change | Reason |
|---|---|---|
| `scripts/register_read_sweep.py:17-26` | The docstring lists the SRP orders the states drive: none; a poll; a provisioning write answered, alone or then a poll; a write posted, then a poll, then the write answered or not; a poll, then a write left unanswered; a poll, then another master's beat, alone or then a poll. It also states the carried-in order, below | F1's docstring item: the old text said "in either order around the write", but no state answered a poll before the write |
| `:342` | `srpmode < 8` becomes `srpmode < 9` | One state added; reads per build go from 48,007 to 54,007 |
| `:350-359` | The harness comment numbers the states: new state 6, steal states 7 and 8, and says why 8 runs last | States the orders as driven |
| `:361-364` | State 6: `answer_srp()` (a poll), then `wr(0x810, aaf_ctrl)` with `srpw` from `o_srp_ctx_we`, and no answer. States 7 and 8 are the old 6 and 7, unchanged | F1's required state. The existing end-of-state cleanup (`:401`) answers the pending write before the next selection |

### Why the new state is 6 and not 8

The first commit of this round (`836906fc`, local only, amended before anything was published) appended the state as 8. On a clean clone of it, the head gave 0 and m4 exited 1, but m5 (the `STRM_SEL`-write clear, `:3119`, deleted) gave rc 0 with 0 disagreements (`receipts/sweeps_first_attempt/`).

- **Cause:** the reviewers' m5 log at `ef7dc985` shows every m5 disagreement in state 0, with `srp=0`. Each pass's state 0 follows the previous pass's last state, "poll, beat, poll", which leaves the word served. Only the `STRM_SEL` write at the top of state 0 clears it.
- **Effect of appending:** the new state's pending write is answered by the cleanup before the next pass, which clears the word, so the selection clear was never needed.
- **Fix:** numbering the new state 6 keeps "poll, beat, poll" last. The `ef7dc985` sequence then stays intact as states 0-5, 7 and 8. m5 is back to 96 disagreements, its `ef7dc985` count: 60 with no snapshot, 36 with one, all in state 0.
- **Recorded:** the docstring (`:24-26`) and the harness comment (`:356-357`) state that this carried-in order is the only one that reads a poll answered before the selection, so the dependency is visible. A dedicated state for it is outside this round's scope (open risk 1).

## Verification (clean clone of `2c500d0a`, Verilator 5.050 pinned)

`tools/run_sweeps.sh` runs each sweep with `python3 -I -B`. Mutants are `git archive` copies of the head with the reviewers' patches applied (`receipts/patches/m{1,2,4,5}.rtl.diff`, copied unchanged from R754-5). The round 4 wording is the `79fdea05` page passed with `--page` (`receipts/plants/round4_wording.page.diff`, 4 rows).

| Run | rc | Disagreements (shipping + 2x2) | Failing words, and the state they fail in |
|---|---:|---|---|
| Head | 0 | 0 + 0, 54,007 reads each | none |
| m4: provisioning `STRMW_CTRL` clear removed (`:3128`) | 1 | 24 + 120 = 144 | `STRMW_SRP` 0x85C (ship 24, 2x2 72), `STRMW_SID_LO` 0x814 24, `STRMW_SID_HI` 0x818 24. All `srp=1 srpw=1 srppoll=0 srpsince=0`, the new state: the read is the snapshot, the page says 0 |
| m1: steal clear removed (`:3132`) | 1 | 24 + 120 = 144 | the same three words, `srppoll=1 srpsteal=1`: the read is the snapshot, the page says 0 |
| m2: write answer sets instead of clears (`:3115`) | 1 | 48 + 240 = 288 | the same three words, `srpw=1 srppoll=0`, with `srpsince` 0 and 1 |
| m5: `STRM_SEL` clear removed (`:3119`) | 1 | 12 + 84 = 96 | `STRMW_SRP` (ship 12, 2x2 48), `STRMW_SID_LO`/`_HI` 18 each; all `srp=0`, in state 0 |
| Round 4 wording planted back | 1 | 48 + 240 = 288 | the same three words: 144 `srppoll=1 srpsteal=1`, 144 `srpw=1 srppoll=0 srpsince=1`; the read is 0, the round 4 row says the snapshot |

Receipts: `receipts/sweeps/sweep_<run>.{log,rc,time}`, `verilator_version.txt`. Each run peaked at about 380 MB.

The m4 count equals R753-5's `m8_p4_noprov.log` (144: shipping `STRMW_SRP` 24; 2x2 24, 24, 72). m1, m2, m5 and the round 4 wording equal their `ef7dc985` counts in R754-5.

## Generator and its freshness gate

- `scripts/gen_register_reference.py` (unchanged this round). The docs workflow step "Register reference freshness gate" runs `--check`, `--selftest` and the memory-map `--check`.
- At the head: `--selftest` rc 0, 61/61 controls; `--check` rc 0, "fresh (203 registers, 34 modules, 240 files)"; `--write` rc 0, then `git status --short --ignored` is empty (`receipts/lane/`).
- Planted stale page: the `79fdea05` page in a copy of the head makes `--check` exit 1, "STALE docs/reference/REGISTER_MAP.md" (`receipts/plants/plant_stale_page_check.{log,rc}`). The planted RTL field rename and reset-value change are selftest controls, and pass in the 61/61.

## Findings count per area

| Area | Count | State |
|---|---:|---|
| R753-5 F1 / R754-5 F1 (Tests, sweep) | 1 | Fixed in `2c500d0a`; verification above |
| R753-5 S1, R754-5 S1, S2 (suggestions) | 3 | Not taken, optional |
| Residue carried (R753-3 RES2, RES3; R754-3 R1) | 3 | Unchanged, on the manager's list |
| Page, descriptions, RTL, generator, gates | 0 | Not touched |

## Gate table

Method as rounds 2 to 5. Each step of the head's `.github/workflows/docs.yml` ran as its job runs it, read from the workflow by `../797-a711b/tools/run_docs_workflow.py`. Each step is one `bash -e` script, with its output written to a file and never piped. Each job had its own fresh clone of `2c500d0a`, and `docs-check-no-git` had its own export clone. Three job chains ran at once (`tools/run_all_gates.sh`), in a unit capped at 8 GB. Peak use reached the cap: the kernel reclaimed memory (`memory.events` max 84), with `oom_kill 0` and every step rc 0. After the run every clone was at the head with an empty status (`gates/clones_after.txt`). Logs and rc files: `receipts/gates/`. The style gate prints "documentation style: OK (24 current documents)", with `REGISTER_MAP.md` among them.

| Job | Step id | Name | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 | Submodule path 'gptp-processor': checked out '135afd043309369a87ddbc8d6550aff8ec52a157' |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 0 | 0 | RESULT: PASS |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 |  |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | Wrote: <scratch> |
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

58 steps ran, 0 not rc 0, 24 not run in these jobs.

Not run: wire-accountability: Record actual job execution; docs-check-no-git: Retain checkout identity before removing metadata; docs-check-no-git: Record actual job execution; docs-gates-0: Install the python gate dependencies; docs-gates-0: Install the pinned Markdown renderer; docs-gates-0: Resolve exact package downloads 6; docs-gates-0: Install diagram gate dependencies; docs-gates-0: Install the pinned sv2v release; docs-gates-0: Record executed gate outcomes; docs-gates-0: Record actual job execution; docs-gates-1: Install the python gate dependencies; docs-gates-1: Install the pinned Markdown renderer; docs-gates-1: Resolve exact package downloads 4; docs-gates-1: Install diagram gate dependencies; docs-gates-1: Install the pinned sv2v release; docs-gates-1: Record executed gate outcomes; docs-gates-1: Record actual job execution; docs-gates-2: Install the python gate dependencies; docs-gates-2: Install the pinned Markdown renderer; docs-gates-2: Resolve exact package downloads 4; docs-gates-2: Install diagram gate dependencies; docs-gates-2: Install the pinned sv2v release; docs-gates-2: Record executed gate outcomes; docs-gates-2: Record actual job execution.

The four jobs `docs-check`, `ci-manifest`, `ci-fail-fast` and `ci-cancel-tail` verify uploaded CI receipts or cancel runs, so they run only on GitHub. `Record ...` and `Retain checkout identity` are GitHub run evidence. `Install ...` and `Resolve exact package downloads` are apt, sudo or pip steps; the venv already holds the pinned tools.

## Lane checks

| Check | rc | Receipt |
|---|---:|---|
| `git diff --check 1f29f189 HEAD` | 0 | `lane/diff_check.{log,rc}` |
| `git merge-base --all origin/dev HEAD`: one line, `1f29f189` | 0 | `lane/merge_base.{txt,rc}` |
| `gen_register_reference.py --selftest`, `--check`, `--write` then clean status | 0 | `lane/gen_*.{log,rc}`, `lane/status_after_write.txt` |
| Sweep at the head, both builds | 0 | `sweeps/sweep_head.*` |

## Open risks

1. The `STRM_SEL`-write clear is read only through the carried-in state 0 of each pass, not by a dedicated state. A future reorder that ends a pass without a served word would hide m5 again, as `836906fc` showed. The comment says so; a dedicated state would be a separate change.
2. Block level only: the shipping datapath ties the SRP grant and the steal input to 0 (`milan_datapath.sv:3010`, `:8720`).
3. Live dev `503bc97c` is not merged.
4. Not run: Verilator suites, Yosys, behave suite, hardware, Vivado (documentation lane, no RTL change).
