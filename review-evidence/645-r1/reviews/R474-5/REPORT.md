[R474] NEGATIVE - exact head 1e79ebdc06528edff74c0a7f530f20f99e3326a2

Review R474-5: internal cleared-context review of PR #672 (issues #645 and #647), rounds 2f and 2g.

- Exact head: `1e79ebdc06528edff74c0a7f530f20f99e3326a2`, tree `067514daece6faf87e9d675bd628759c7bec83fa`.
- Delta reviewed: `85db3534..1e79ebdc`. It holds the `--no-ff` merge `a5ca6e51` of dev `6aa25dec`, the records-only re-baseline `4640d995` (round 2f) and the default-suite split `1e79ebdc` (round 2g).
- Baseline: R474-4 (NEGATIVE at `85db3534`, one MAJOR), R475-4 (POSITIVE at `85db3534`) and the composition review R475-5 (POSITIVE at candidate `17c39e57`).

Both rounds do what their assignments ask. The three resource records regenerate exactly from the published receipts, and the policy is unchanged. The moved campaigns still catch their controls, and no RTL changed after the merge. At this exact head, hosted shard 0/5 ran `follow_ring` and `milan_dp_render` to PASS on a dev-class runner, and the `verilator-suites` aggregate is success. R474-4-F1 is therefore resolved.

The verdict is NEGATIVE on two MINOR findings, both under Tests and Docs:

- **R474-5-F1 (new).** The wall times recorded for the default suites do not describe the hosted invocation. `TESTING.md` projects 559.5 s for `follow_ring`, but the exact-head hosted run took 1,422.5 s. That is 98.8 % of the ruled 1,440 s ceiling.
- **R475-6-F1 (retained).** It is confirmed here by an independent probe.

Conformance, RTL and Robustness are CLEAN.

## Scope and method

Context was read in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. Issue #645's body and every public manager ruling, through the round-2f assignment 6061613334 and the round-2g assignment 6073617515.
4. The author's REVIEW READY 6066156323 and STOP 6074038320.
5. `AREA_BUDGET.md` (the re-baseline duty at lines 194-195), `CI_WORKFLOWS.md:185-229` (per-suite wall clocks), `TESTING.md:170-300` and `scripts/run_all_suites.sh`.
6. The diff and history `6aa25dec..1e79ebdc`, focusing on `85db3534..1e79ebdc`.
7. The published evidence at `1747b39f` (`author-r2f/resource-receipts`, archived at `d59599ef` and unchanged since; `author-r2g`) and the PR body.

I read R474-4, the stated baseline from this reviewer role, after my own pass over the diff. I read the other reviewer's reports (R475-4, R475-5 and R475-6) only after my verdict and ledger were written. The draft is `receipts/DRAFT-VERDICT-PRE-PRIOR-READ.md`, written 2026-10-09T05:00:39Z.

No private author material and no other checkout was used.

Execution used the pinned simulator, Verilator 5.050 rev v5.050. The wrapper's SHA-256 is `905795b9...e92f` and the binary's `verilator_bin` is `44898b22...bfdd` (`receipts/verilator-identity.txt`).

- Every build and run used a `git archive` export of the head and its three required submodules under `scratch/`, never the clone.
- The submodule copies were indexed so `scripts/pp_srcs.py` can list them; their file counts equal the clone's (562, 104 and 214).
- The detached jobs were pinned to disjoint four-CPU sets, each with its own log, rc and elapsed-time file (`scripts/launch.sh`). They were waited on by foreground polls.
- The peak memory of the service was 5.6 GB.

## Findings

### R474-5-F1 MINOR: the recorded default-suite wall times do not describe the hosted run; `follow_ring` is at 98.8 % of the ruled ceiling, not 39 %

- **Lenses:** Tests, Docs.
- **Where:**
  - `docs/testing/TESTING.md:293-300`: "Default suite (`make -j16`)", "`follow_ring`: four standing legs | 354.1 | 559.5 s | 1440 s", "`milan_dp_render` ... | 733.2 | 1158.5 s", and "both pass without changing any suite budget".
  - `tb/verilator/follow_ring/Makefile:22-27`: "354.1 s cold with make -j16 ... At the documented 1.58x hosted factor this is 559.5 s".
  - `tb/verilator/milan_dp_render/Makefile:46-52`: the same form, with 733.2 and 1158.5 s.
- **Authority:**
  - `CI_WORKFLOWS.md:185-187`: "The measured hosted worst case plus a stated margin sets each named entry".
  - `CI_WORKFLOWS.md:219`: default suites over 80 % of their budget take a ruled increase.
  - The round-2g assignment 6073617515, item 3: both defaults at or under 80 % of 1,800 s (1,440 s), measured and stated.
  - `TESTING.md:181-183`: the 1.58x factor was measured against local runs under four-core affinity.
  - `scripts/run_all_suites.sh:394`: the hosted sweep runs each suite as `timeout "$TMO" make -C "$d"`. That is serial make, on a four-core runner (`TESTING.md:174`). The workflow step sets no `MAKEFLAGS` (`.github/workflows/rtl.yml:294-297`).
- **Evidence:** times in seconds.

  | Basis | `follow_ring` | `milan_dp_render` | Receipt |
  |---|---:|---:|---|
  | Author, `make -j16`, recorded | 354.1, stated as 559.5 at 1.58x | 733.2, stated as 1158.5 at 1.58x | `TESTING.md:295-296` |
  | **Exact-head hosted**, shard 0/5, run `37882435947`, job `113665137864` | **1,422.5 PASS** | **1,093.9 PASS** | `receipts/hosted/shard0-suite-windows.txt`, `receipts/hosted/shard0-job.log` |
  | Local replica of the hosted invocation: serial `make`, four CPUs, cold | 800.2 (1,264.3 at 1.58x) | 826.7 (1,306.2 at 1.58x) | `receipts/runs/T1-follow-default.*`, `receipts/runs/T2-render-default.*` |

  - The hosted runner is dev-class. Its short shared suites took 68.6, 23.3 and 16.2 s (`gptp_txts`, `ptp`, `rx_filter`), against dev's 68, 24 and 16 s in R474-4's table.
  - Hosted `follow_ring` is 2.54 times the documented projection. That is 79.0 % of the 1,800 s guard and 98.8 % of the 1,440 s ceiling: 17.5 s from the 80 % line and 377.5 s from the guard.
  - The cause is the measured invocation. With `make -j16` the four legs (`b8`, `pullin`, `small-pullin`, `settle-control`) overlap. The hosted sweep runs them one after another.
  - My replica ran beside other jobs on disjoint CPUs. Even so, its `follow_ring` figure exceeds the recorded one by 2.3 times.
  - The render projection happens to sit above the hosted figure, so its conclusion stands. Its stated basis has the same flaw.
- **Impact:**
  - The authoritative testing page says `follow_ring` has about 880 s of hosted headroom under the ruled ceiling. It has 17.5 s.
  - A later change that adds about 1 % to this suite's default would cross the 80 % line that `CI_WORKFLOWS.md:219` uses for ruled increases. The page would still say there is 61 % headroom.
  - This is the defect class R474-4-F1 named: a documented local projection that the hosted runner does not reproduce. There, the pre-lane render figure "about 1049 s" stood while the hosted suite hit 1,800 s.
  - No check, gate or CI result is wrong today: both suites pass inside their guard at this head.
- **Required outcome:**
  - `TESTING.md:293-300` and both Makefile headers state a figure that describes the hosted invocation. That is either:
    - the exact-head hosted windows (1,422.5 s and 1,093.9 s, with the run, job and runner class), or
    - a local measurement taken the way the sweep runs the suite (serial `make` under four-core affinity, the basis of the 1.58x factor), scaled by that factor.
  - The `follow_ring` row states its real margin against 1,440 s and 1,800 s.
  - Whether a suite at 79 % of its budget needs a further split, or a #673-form budget entry, is the manager's decision. The page must not record 559.5 s as its hosted projection.
- **Verification:**
  - Each stated figure matches its receipt: the hosted job log's verdict-timestamp windows, or a local log with its invocation and CPU affinity recorded.
  - `docs_check`, `check_doc_style`, `gen_toc --check` and `--verify-anchors` pass.
- **Why not RESIDUE:** it changes measurement figures and the headroom claim they support.

### R475-6-F1 MINOR (retained, independently confirmed): `trace_table.py` counts the declared settle recentre as a slipped frame

- **Lenses:** Tests, Docs (as R475-6 filed it).
- **Where:**
  - `tb/verilator/follow_ring/trace_table.py:63-65`: every margin rise over 0.5 tick is counted as a slip.
  - `tb/verilator/follow_ring/trace_table.py:12-13`: "slips  frames the ring slipped in the step (a margin jump of +1)". The ring-law text on line 12, "a slip below 0, a skip above 3", still describes the former 8-entry ring, not the 16-entry ring with target 11.
- **Authority:**
  - `MEDIA_CLOCK_FOLLOWING.md:1096`, the Counted row: the recentre "is the declared discontinuity, not a slip".
  - `REGISTER_MAP.md:1870`.
- **Evidence:** `receipts/trace-table-probe.txt`, with inputs in `receipts/trace-table-probe-inputs/`. A synthetic trace holds the margin at 1.3 ticks. A declared hold then raises it to 5.3 ticks at +0.6 s, with no slip. The helper prints `slips 1` in the +0.75 s row.
  - R475-6's own counterexample on a real pull-in trace shows the same thing.
  - The file is unchanged since `85db3534`.
- **Impact:**
  - The diagnostic table reports a false slip for every passing settle action.
  - It contradicts the counters and the harness verdict, and could misdirect a later diagnosis.
  - No gate reads it.
- **Required outcome:** as R475-6 states it. The table distinguishes real slips from declared actions, or stops presenting the heuristic as a slip count. Its docstring states the current ring law.
- **Verification:**
  - The probe above prints `slips 0`.
  - A trace with a genuine one-frame slip still prints `slips 1`.

### R474-5-S1 SUGGESTION: the evidence disposition of `follow_ring/mutants.py` does not say that it is outside the default sweep

- **Lenses:** Docs.
- **Where:** `scripts/measure_test_evidence_readers.py:92-97`.
- **Detail:** the `milan_dp` explicit campaigns' entries end "It is the explicit X target, outside the default sweep" (`:105-123`). This driver no longer runs in its suite's default target, but its entry does not say so.
- **Optional outcome:** add that clause. It changes no check.

No new RESIDUE.

## Round 2f: re-baseline on the merge result

**The merge is the automatic one.** `git merge-tree --write-tree 85db3534 6aa25dec` gives tree `47e1e22d`, which is `a5ca6e51^{tree}`, with rc 0.

- The datapath lines that `a5ca6e51` brings in, against `85db3534`, equal dev's own `99e4eb6c..6aa25dec` lines (19 lines, all comments).
- `KL_chan_map_capture.sv` is byte-identical from `85db3534` to the head.
- The other HDL it brings in is dev's `KL_maap.sv` and its documentation (#686).

**Records regenerate exactly** (`scripts/regen_records.py`, `receipts/regen_records.log`, rc 0). The script uses the gate's own parsers from `syn/ooc/pp_resource_gate.py` on the retained `baseline_utilization.rpt`, timing summary, `baseline_hierarchy.rpt`, recipe Tcl and route status. For each of `route-1x1`, `ooc-1x1` and `ooc-8x8`:

- The figures (LUT, FF, slice, BRAM tile, RAMB36, RAMB18, DSP, WNS, WHS and total CARRY4 from the primitive table) equal both the published `record` output and the record committed at the head.
- The identity (tool build, device, design, state and every flow command, `synth.maxThreads 1` included) is equal.
- The sub-block LUT, FF, RAMB and DSP scopes are equal.
- The published record equals the committed record field for field, including `inputs_sha256`.
- The route status is complete: 101,396 of 101,396 routable nets routed and 0 with routing errors.

Values: route 50,267 LUT, 54,413 FF, 15,779 slices, WNS +0.299 ns and WHS +0.031 ns. OOC 1x1 is 23,179 / 19,779 and OOC 8x8 is 30,135 / 27,380.

**The gate verdict replays exactly, and the policy is unchanged** (`scripts/check_2f_policy_inputs.py`, `receipts/check_2f_policy_inputs.log`, rc 0):

- `judge(dev 6aa25dec record, published record)` reproduces each `check-*.log` line for line, with status 0. The route shows -124 LUT, +150 FF, -9 slices, WNS +0.058 and WHS +0.002; both OOC endpoints show 0.
- Every non-record field (tolerance, floor, ceiling) and every top-level field equals dev's.
- The merge itself did not touch the JSON.
- Every repository input that the four configurations read has a raw SHA-256 equal to its blob at both the merge `a5ca6e51` and the head: 122/122 for the AX7101, 119/119 each for the 8x8 and both OOC.
- The 5 inputs per configuration that git does not bind are the generated LiteX top, its XDC and the three shared-environment CPU files. They are hashed in the author's inventory.

**Gate self-checks at the head:** `pp_resource_gate.py check-baseline` gives "baseline PASS: 3 endpoints", and `--selftest` gives 260 arms and 500 generated cases PASS (`receipts/gate-*.log`).

**Documentation figures checked against the receipts:**

- 79.29 %, 42.91 % and 99.55 % of the device, with 71 slices free.
- 12,227 LUTs over the 38,040 target, so the wrapper may use at most 11,118 (52 %).
- `milan_datapath` 41,689 LUTs (65.8 %), the wrapper 23,345.
- The four corner rows: slow +0.299/+0.063, fast +1.434/+0.031.
- The 14-level path `milansoc_write_w_buffer_level0_reg[1]` to `storage_13_dat1_reg[14]`, with a 9.294 ns delay split 1.963 ns logic and 7.331 ns route.
- The IOB check: all PASS, RX valid at `ILOGIC_X0Y119`.
- The 0.25 ns fall limit binding at +0.049 ns.

## Round 2g: default-suite split

- **No RTL change.** `4640d995..1e79ebdc` touches only `docs/` and `tb/`. It is one commit on `4640d995` with a one-line subject and no body or trailers, and no merge, rebase or amendment.
- **`follow_ring`.** `all: run`, and `run: b8 pullin small-pullin settle-control` (`Makefile:71-72`). `mutants` remains an explicit target.
  - My cold default ran all four legs, rc 0: b8 48/0, pullin 18/0, small pulls 10/10, controller PASS at 6.25, 25, 50 and 100 MHz. There is no mutant line in its log.
  - `make mutants SWEEP_JOBS=4`, the exact command in `TESTING.md:272`, gave rc 0 and **12/12 caught**, each by its named check, in 436.8 s (`receipts/runs/C1-follow-mutants.log`).
- **`milan_dp_render`.** `sim_tdm8_render.cpp:4406` gates `phase_pullin` on the new `--with-pullin`. The multi-stream leg never ran `[PULLIN]` (`:4355-4360`). No mutant or clean control in `tdm8_render_mutants.py` used the no-argument leg's `[PULLIN]`: the NO-SETTLE plant runs `--pullin` (`:351`).
  - My cold default gave shipping 258/0, two-stream 71/0 and leg defects 5/5, with rc 0. It has 0 `T647` lines and still prints the `[LAW]` phases.
  - `make tdm8render-pullin` gave rc 0 and **19/19 legs, 830 checks, 0 failures** (`receipts/render-pullin-summary.txt`). The preserved history leg had 272 checks, with the settle 1,327.7 ms after the hold. The 18 boot phases had 31 checks each, with the settle 1,246.8 ms after the hold. That matches the corrected `kPullinMaxWaitPdus` comment (`:250-253`).
- **Fault probe, history leg.** I planted the inventory's NO-SETTLE edit (`settle_recentre_p_r <= 1'b0`, `receipts/probe-no-settle.diff`) in a scratch copy only. I ran it through the real target with `DP_SRC=<copy> PULLIN_PHASES=1562` (`receipts/runs/P1-no-settle-history.*`, `receipts/probe-no-settle/`).
  - The `--with-pullin` history leg fails 4 of 272 checks, including the named law check "T647 PULLIN +1562 after the settle: every PDU's first event is inside the law band from its PDU end" (got 123, expected 124).
  - The boot leg fails the same 4.
  - xargs exits 123, so the target exits 2.
  - So the moved standing phase can fail, and the campaign's verdict cannot be lost in its pipeline.
- **The moved coverage is declared in a campaign someone runs.** Both campaigns are rows of `TESTING.md:272-273`'s explicit-campaign table, with command and owner (manager merge bank), as the assignment requires. The `follow_ring` row in the suite table (`:525`) and the render row (`:539`) say what the default omits. #647's pull-in remains graded in the hosted default through `follow_ring`'s `pullin` and small-pull legs.
- **Doc corrections are correct.**
  - `MEDIA_CLOCK_FOLLOWING.md:1086` now names `g_src_recentre`, which is the #386 block at `milan_datapath.sv:6534-6565`. The settle recentre is `g_settle_recentre` at `:6615`.
  - The second test-plan link in `TESTING.md:525` now targets `#simulation` (`MEDIA_CLOCK_FOLLOWING.md:1509`), which holds the controls column.
- **Gates at the head**, all rc 0 (`receipts/gates/SUMMARY.txt`): `docs_check`, `check_doc_style`, `gen_toc --check`, `--verify-anchors`, `check_doc_paths`, `check_em_dash --base 85db3534`, `git diff --check 85db3534..1e79ebdc`, `measure_test_evidence --check` and `--selftest`, `ci_events --check`, `check_hygiene --check`, `check_cpp_idiom`, `measure_fail_fast --check`, `suite_shards --selftest` and `gen_module_matrix --check`.

## Prior public findings at this head

| Prior finding | Severity / lenses | Status at `1e79ebdc` | Evidence |
|---|---|---|---|
| R474-4-F1 | MAJOR / Tests, Docs | **RESOLVED** | Exact-head hosted shard 0/5 (run `37882435947`, job `113665137864`, dev-class) PASSes both suites inside the 1,800 s guard: `follow_ring` 1,422.5 s and `milan_dp_render` 1,093.9 s. The recorded figures match the author's receipts for the invocation they name. `measure_test_evidence --check` and `--selftest` pass. The basis of those figures is the new R474-5-F1. The exact-head `verilator-suites` aggregate is success (job `113687075824`). |
| R474-4-R1 | RESIDUE / Docs | **RESOLVED** as prescribed | `TESTING.md:525`, second link `#simulation` |
| R475-2-R2 | RESIDUE / Docs | **RESOLVED** as prescribed | `MEDIA_CLOCK_FOLLOWING.md:1086` `g_src_recentre` |
| R475-6-F1 | MINOR / Tests, Docs | **RETAINED** | See above; `trace_table.py` is unchanged since `85db3534` |
| R474-2-S1, R474-2-S2, R474-2-S3 / R474-1-S2 | SUGGESTION | **RETAINED** | `settle_control.py`, `quiet_distributions.py` and `sim_ax1x1gptp.cpp` are unchanged since `85db3534`. The `follow_ring/Makefile` change is the header and `all:` only |
| R474-1-F1 to F4, R474-2-F1, R475-1-F1 to F3, R474-2-R1/R2, R475-2-R1, R474-3-R1/R2 | as filed | Remain **resolved** | The delta touches none of their artifacts. Lane HDL is unchanged from `85db3534` apart from dev's comment lines. My `mutants` run caught HELD-DUP, STARVED-HELD-DUP, SINGLE-DROP, OVERSHOOT and the other eight by their named checks |
| R475-4, R475-5 | no findings of their own | carried items as above | |

## Lens results

```text
[R474] PASS Conformance - docs/design/AREA_BUDGET.md:194-195 duty and ruling 6061613334 against receipts/regen_records.log and receipts/check_2f_policy_inputs.log; ruling 6073617515 items 1-5 against tb/verilator/follow_ring/Makefile:71-72, sim_tdm8_render.cpp:4406, docs/testing/TESTING.md:272-273,525, MEDIA_CLOCK_FOLLOWING.md:1086, receipts/hosted/shard0-suite-windows.txt - merge-result re-measure with single-thread synthesis, check against dev's records, record --write with policy unchanged, route above both floors; default split as ruled, both explicit campaigns declared with command and owner, hosted defaults within 1,440 s; bench items remain the manager's
[R474] PASS RTL - git merge-tree reproduction of a5ca6e51 (tree 47e1e22d); hdl/milan/milan_datapath.sv delta equal to dev's 19 comment lines; hdl/ieee1722/aaf/KL_chan_map_capture.sv byte-identical 85db3534..1e79ebdc; 4640d995..1e79ebdc touches no hdl/syn/constraints/sw path; route-1x1 route status, corner and IOB reports - no RTL authored in 2f or 2g; the merged image routes completely at +0.299/+0.031 ns with every GMII RX capture packed
[R474] PASS Robustness - receipts/probe-no-settle/ and receipts/runs/P1-no-settle-history.* (planted defect through the real tdm8render-pullin target: history leg fails its named law check, target exits 2); receipts/render-pullin-summary.txt (19 legs, 830 checks); receipts/runs/T1-*, T2-* (serial four-CPU cold defaults rc 0) - the moved campaign's failure propagates through xargs and make; mode gating leaves the multi-stream leg, the short legs and the leg-defect arms unchanged
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #645 rulings 6061613334 and 6073617515 with the earlier rulings; `AREA_BUDGET.md:96-125, 160-215`; `234_PP_SHADOW_AREA_BASELINE.md:30-98`; three records regenerated and the policy compared; hosted shard-0 windows against the 1,440 s ceiling; `TESTING.md:262-300` | R474-5 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |
| RTL | CLEAN | merge reproduction; datapath and capture deltas; no RTL in `4640d995..1e79ebdc`; route status, corner, IOB and critical-path receipts | R474-5 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |
| Robustness | CLEAN | NO-SETTLE fault probe through the real pull-in target; 19-leg campaign; serial four-CPU defaults; `run()` mode gating (`sim_tdm8_render.cpp:4337-4415`) | R474-5 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |
| Tests | **UNCLEAN** (R474-5-F1 MINOR; R475-6-F1 MINOR retained) | `follow_ring` default and `make mutants` 12/12; render default and the 19-leg pull-in; the fault probe; `run_all_suites.sh:394`; hosted windows; the evidence check; `trace_table.py:63-65` probe | R474-5 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |
| Docs | **UNCLEAN** (R474-5-F1 MINOR; R475-6-F1 MINOR retained) | `TESTING.md:174, 181-183, 262-300, 525, 539`; both Makefile headers; `MEDIA_CLOCK_FOLLOWING.md:1086, 1509-1545`; `AREA_BUDGET.md`; the `234_` record; `trace_table.py:1-20`; PR body Round 2f and 2g; 14 documentation and source gates | R474-5 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |

## Hosted evidence (inspected, not owned)

Snapshot at 2026-10-09T05:39:00Z (`receipts/hosted/checks-snapshot.tsv`), run `37882435947` on `1e79ebdc`:

- **`verilator-suites`: success** (job `113687075824`).
  - Shard 0/5 took 45m49s, 1/5 1h29m31s, 2/5 1h18m13s, 3/5 11m14s and 4/5 55m22s, all success.
  - Shard 0's sweep reports 12/12 suites passed, 0 timed out and 402,109 checks with 0 in-suite failures (`receipts/hosted/shard0-job.log`).
- **`yosys-portability`: success.** Yosys shards 0-3, `verilator-lint`, `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `firmware-unit`, `yosys-elaboration`, `bdd-conformance`, `wire-accountability`, `changes` and `full-ci-gate` are all success.
- **`Physical gPTP (nightly and manual)`: skipped.** A skipped context is not evidence that it executed.
- **Ownership:** hosted and act acceptance stay with the manager. I did not run any act replica.

## Real limits

- **No vendor run here.** The 2f records were regenerated from the published reports, not re-measured.
  - Per-scope CARRY4 could not be regenerated: the 8 MB cell census is retained only as an excerpt. The totals were cross-checked against the primitive table.
  - The final `inputs_sha256` could not be recomputed: the generated LiteX top is retained by hash only. Every repository-sourced input was bound to its blob instead.
  - The critical-path text comes from the author's `route-details.json`, because the full timing report is an excerpt.
- **No full bank.** I did not run the full sweep, builder, firmware, portability, vendor-parser, arrival campaign or #657 mutation campaign; they are outside this review's allowance. The author's gate receipts are source-head evidence. No manager source bank exists at this head, and none is inferred.
- **The local timing replica ran beside other jobs on disjoint CPUs** of a shared host. Render compilation was capped at four workers to mirror a four-core runner. The hosted windows include tally overhead between adjacent verdicts, as `CI_WORKFLOWS.md` notes for its survey.
- **Physical calibration NOT RUN.** Field skips and simulation are not hardware proof. `Physical gPTP (nightly and manual)` is a skipped context, which is not evidence.

## Pending manager duties

- Rule on R474-5-F1. Have the wall-time record corrected, and decide whether `follow_ring` at 79 % of its budget needs a further split or a #673-form entry.
- Have R475-6-F1 corrected and re-reviewed.
- Accept the exact-head hosted evidence (`verilator-suites` is success) and the act replica. Both are the manager's.
- Run the explicit campaigns now owned by the merge bank: `make -C tb/verilator/follow_ring mutants SWEEP_JOBS=4` and `cd tb/verilator/milan_dp_render && make tdm8render-pullin`.
- Build and validate the current-dev merge candidate in the builder and native banks. The source base and live dev are both `6aa25dec`; re-check them at the merge turn.
- Run the B-lane bench repeat of the INTERNAL→AAF and AAF→CRF switches after the merge.
- Run post-merge containment.
- Carry the retained SUGGESTIONs.

## Restoration

`receipts/restoration.txt` (`scripts/verify_restore.sh`):

- HEAD is `1e79ebdc`, tree `067514da`. The index tree equals the HEAD tree.
- The worktree equals the index, and the index equals HEAD.
- No untracked or ignored entry remains.
- `protocol-processor` `2ad2f845`, `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` are at their gitlinks and clean.
- `external` and `third_party/lwSRP` are not initialized in this clone, as received.
- One interpreter cache directory that my first regeneration run created under `syn/ooc/` was removed at once. Every later run used `-B`.

R474-5 FINISHED
