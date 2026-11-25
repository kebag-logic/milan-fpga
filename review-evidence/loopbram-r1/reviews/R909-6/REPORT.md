[R909] NEGATIVE - exact head 09201d35d7ea720b3ba205da185ba35c159ec24a

# R909-6: internal independent re-review of PR #987 (issue #979)

- **Head.** `09201d35d7ea720b3ba205da185ba35c159ec24a`, tree `a3b3dca8a55b738e714ada4662a309a50118a481`. This is the PR's live `headRefOid`. The PR is open and not a draft.
- **Previously reviewed head.** `1516b2ffe321337858389ec8e42897f8a80644bb` (R909-5 POSITIVE). The delta is four commits:
  - merge `7049c524` of dev-soft-core `5de21ff3`;
  - `12382bc8`, which moves the sweep to twenty-seven workers;
  - `e9f95da4`, which registers the firmware-boundary builder;
  - `09201d35`, which adapts the leaf harness to the depacketizer verdicts.
- **Source base.** `3cda030c17`. The live dev-soft-core tip is `5de21ff3`, which is now an ancestor of the head. The brief names live dev `e275d795` for the merge-turn candidate, which nothing in this round builds.
- **Verdict reason.** One MINOR finding is open under Conformance and RTL (R909-6-N1). The merge brought 619 inserted and 225 deleted lines of receive-path RTL into the enabled images. #979's routing and area evidence was measured before that change. Everything else in the delta is clean:
  - the merge resolution;
  - the leaf-harness adaptation;
  - the 27-worker planner and its documentation;
  - the firmware-boundary registration;
  - disabled builder identity.
- **Also recorded.** One new RESIDUE and two SUGGESTIONs. The prior RESIDUE R909-5-R1 is still unapplied and is carried.

## Delta structure (proved)

- **The merge is mechanical.** Merging PR #987's own patch onto dev reproduces the patch exactly. For each of the PR's 42 files, the `+`/`-` lines of `git diff 3cda030c17 1516b2ff` and `git diff 5de21ff3 7049c524` are equal, and so are the file sets. The one exception is `scripts/suite_shards.py`, where the merged patch no longer removes three blank lines that dev had already removed (`receipts/merge_patch_compare.txt`, `receipts/merge_suite_shards_delta.txt`). The combined diff `git show --cc 7049c524` has one hunk: the automatic three-way union of dev's figures with the two loopback rows in `SUITE_SECONDS`. The merge contains no hand edit.
- **The PR's own post-merge commits** change eight files (`git diff --name-only 7049c524 HEAD`, `receipts/delta_scope.txt`):
  - `.github/workflows/rtl.yml`, regenerated;
  - `scripts/suite_shards.py`;
  - `docs/testing/{CI_WORKFLOWS,RUNNING_TESTS,TESTING}.md`;
  - `sw/firmware/ctrl/README.md`;
  - `sw/firmware/ctrl/test/ctrl_configs.py`;
  - `tb/verilator/input_loopback/loopback_wrap.sv`.

  None of them is shipped RTL, configuration, firmware source or a gitlink.
- **The merge changes RTL.** It brings dev's RTL in four files: `KL_aaf_rx_depacketizer.sv`, `KL_avtp_rx_monitor_ctx.sv`, `avtp_stream_parser.sv` and `milan_datapath.sv` (#948's per-input verdicts). The head's `hdl` tree is `244c59e0`. The enabled 8x8 route's source tree was `aefab080`, the `hdl` tree at `9acb9b82` and at `1516b2ff`. `git diff 9acb9b82 HEAD -- hdl/` is byte-equal to dev's own change (`receipts/route_source_vs_head.txt`).
- **Gitlinks.** The head's six gitlinks equal dev `5de21ff3`'s (gptp-processor `1213ac5b`, lwSRP `d1bb4f4e`).

## Executable evidence I ran at this head

All runs used the scoped Verilator 5.050. Its wrapper resolves to the pinned install and reports `Verilator 5.050 2026-07-01 rev v5.050`. Host load was about 150 on 32 CPUs.

| Probe | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/input_loopback` (300 s arm) | PASS in 24 s: 8x8 79587 checks, 468 packets; 1x1 76017 checks, 447 packets. These equal the author's figures and the round-6 figures | `receipts/suite_input_loopback.log` |
| `make -C tb/verilator/input_loopback_dp` (300 s arm) | PASS in 67 s: 16173 and 122549 checks, 0 failures | `receipts/suite_input_loopback_dp.log` |
| Leaf campaign `input_loopback/mutants.py` | control PASS, and every one of the 7 plants is caught: ignored_mapping, wrong_bank, skipped_copy, ignored_invalidation, retained_word, missing_clock_flush, wrong_latency. rc 0 | `receipts/leaf_mutants.log` |
| Parent campaign `input_loopback_dp/mutants.py` | 2 controls and 15 plants PASS, rc 0, 528 s. The plants cover edit invalidation and disconnected maps at both shapes, overwritten and truncated pages, and a missing output at each of the 8x8 talkers 0-7 and at the 1x1 talker | `receipts/parent_mutants.log` |
| `suite_shards.py --selftest` | selftest: PASS | `receipts/gate_suite_shards_py_selftest.log` |
| `ci_gate_workflows.py --check`, `ci_suite_workflows.py --check`, `measure_test_evidence.py --check` | each rc 0 (the regenerated `rtl.yml` is fresh) | `receipts/gates_summary.txt` |
| My projection probe `scripts/projection_vs_table.py` (the planner's own `balance()` against the `CI_WORKFLOWS.md` projection table) | head: 96 units, and 27 of 27 rows equal the planner; `input_loopback_dp` is on worker 14 and `input_loopback` on worker 15. At the merge `7049c524`, the probe **fails** with 23 mismatches. That shows the probe can fail, and it reproduces the author's over-budget workers 10, 20, 21 and 24 at 1304, 1278, 1290 and 1306 s | `receipts/projection_vs_table_head.log`, `receipts/projection_vs_table_merge7049.log` |
| Builder-registry probe (`ctrl_configs.BUILDERS`, `candidates()`) | The new entry has `needs="verilator"` and runs `--build-only` at shapes 1 and 8. `ctrl_runs.py:178` passes `VERILATOR` to the builder, and `run.py:72` honours it. Of the seven loopback candidates, only `input_loopback_dp/run.py` names the firmware tree (`run.py:52`) | `receipts/ctrl_configs_probe.log` |
| Disabled builder identity: my own `scripts/builder_identity.sh`, run on a dev `5de21ff3` export and on the head with one fixed config path | `endstation_ax7101_1x1_tdm8`: 12 files IDENTICAL. `endstation_ax7101_8x8`: 12 files IDENTICAL. As a control, 8x8 with `input_loopback_lane: true` differs in 11 of 12 artifacts | `receipts/builder_identity_dev_vs_head.log` |
| Docs gates: `docs_check.py`, `check_hygiene.py --check`, `check_doc_style.py`, `check_doc_paths.py`, `docs/DOC_MAP.gen.py --check` | each rc 0 | `receipts/gate_*.log`, `receipts/gate_doc_map_check.log` |
| `check_em_dash.py` (pinned renderer installed with hashes into a scratch-only venv) | rc 0. `--base 1516b2ff`: 0 findings over 1021 added lines. `--base 3cda030c17`: 0 over 1662 | `receipts/em_dash_base_*.log` |
| Packet integrity: `review-evidence/loopbram-r1/author-r7` at `73eaef87` | 114 of 114 files match the `MANIFEST.json` `published_sha256`. The commit is **unsigned**, so integrity rests on the content hashes | `receipts/author-r7-verify.log` |
| Restore | HEAD, index and worktree equal the exact head (index tree `a3b3dca8`). Submodule checkouts equal the six gitlinks. Ignored build outputs were removed | `receipts/restore_check.txt` |

### Leaf-harness adaptation (`tb/verilator/input_loopback/loopback_wrap.sv:64-69`)

#948's depacketizer queues a PDU on `pdu_enq_p_i`. It completes the PDU on `pdu_done_p_i` and records the accepting inputs from `pdu_done_mask_i`. It then reads the frame out once for each accepting input, with tuser set to that input (`hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:78-84, 104-113, 434-465`).

The wrapper drives enqueue and done from `|accept_w` and sets the mask to `accept_w`. In dev's own N=1 flat-monitor wrappers (`tb/verilator/aaf_audio_loop/aaf_audio_loop_wrap.sv:146-147`, `tb/verilator/avtp_rxmon/avtp_rxmon_wrap.sv:117-118`), enqueue and done are the accept pulse and the mask is `1'b1`. The leaf wrapper is the same protocol at N inputs: each monitor has a distinct stream ID, so `accept_w` is one-hot, and the tuser it gives matches the removed index encoder.

The packet counts are identical (468 and 447), and all seven leaf plants are still caught. So the adaptation is neither vacuous nor lossy. The parent harness instantiates the real merged `milan_datapath`, and it passes at both shapes with every output stream graded.

## Findings

### R909-6-N1 - MINOR - Conformance, RTL - enabled-build route and area evidence predates the merged receive-path RTL

- **Where.**
  - The PR body: "Enabled 8x8, routed at 9acb9b82's source ... Enabled 1x1 RTL is unchanged since its route ... Those routes predate the merged dev changes to the datapath."
  - `docs/design/INPUT_MAPPED_LOOPBACK.md:397-413`: "Report historical comparison separately from fresh same-head measurements." It records the floor as `+0.030 ns` setup and nonnegative hold.
  - `receipts/route_source_vs_head.txt`.
- **Authority.**
  - Issue #979 acceptance: "**Routing:** both shapes routed at #818's timing floor", and "**Area:** the measured cost at 8x8/1if (LUT/FF/BRAM)".
  - AGENTS.md section 7: "Coverage is banked against a commit ... A later commit that changes any artifact within a lens's scope un-covers that lens."
  - Earlier rounds closed the enabled-route findings explicitly on source identity: R909-2-N2 and R910-2-F2, closed at R909-3 and R910-3 ("on identical RTL", "Source-identical enabled 8x8 export").
- **Evidence.** The head's `hdl` tree (`244c59e0`) is not the routed `aefab080`. The difference is dev's #948 receive path: 619 inserted and 225 deleted lines across the depacketizer verdict queue, the monitor context's match vector, the parser and the datapath glue. All of it is elaborated in both enabled images and sits on the path that feeds the loopback copy (`hdl/milan/milan_datapath.sv:8060-8065, 8519-8521`). The recorded 8x8 margin is placement-sensitive. Only AltSpreadLogic_high met the floor (+0.223 ns setup). The other two prescribed directives reached +0.008 and +0.003 ns, below +0.030.
- **Impact.** At the head that would merge, the enabled-build criteria that #979 freezes have no measurement:
  - routing at #818's floor at every corner;
  - the 8x8/1if LUT/FF/BRAM cost (48901 / 54672 / 111 tiles).

  A merged enabled build could miss the floor with nothing in the record showing it.
- **Not a defect in the delta's own code.** Disabled identity is not affected (see the limits).
- **Required outcome.** Either of:
  - (a) both enabled shapes routed from a tree whose `hdl` equals this head's. At 8x8, run the three prescribed directives, with the best meeting +0.030 ns setup and 0 ns hold at every signoff corner, with zero failing endpoints and zero routing errors. Restate the enabled 8x8 utilization. Bind the source to `git rev-parse <head>:hdl`.
  - (b) a public owner or manager decision on #979 or #987 that the pre-merge enabled routes and area satisfy #979's Routing and Area criteria for a head that contains dev's #948 RTL. The PR body and the design page should then state that basis.
- **Verification.** Corner reports and a source binding whose `hdl` tree equals the candidate head's, or a link to the decision.

### R909-6-R1 - RESIDUE - Docs - `docs/testing/TESTING.md:478`

- **Text.** "So #979 adds a twenty-seventh worker, as its N1 decision provides when the self-test requires one."
- **Problem.** "N1" is a review-finding label. A cold reader of an authoritative page cannot resolve it.
- **Wording only.** The rule it stands for is in the planner itself (`scripts/suite_shards.py:240-244`: "add a worker if one is then predicted over ...").
- **Exact fix.** "So #979 adds a twenty-seventh worker, as the selector's new-suite steps provide when a provisional figure leaves a worker over its budget."
- **Verification.** Read `TESTING.md:478`. Docs gates stay green.

### R909-6-S1 - SUGGESTION - Docs - `scripts/suite_shards.py:150-151`

- The delta rewrapped this comment, which still cites "step 3 of the module docstring's new-suite steps". The docstring (`:14-19`) is an unnumbered paragraph, and the list of steps is spelled out in `table_problems()` (`:240-244`).
- The wording predates the PR and was only rewrapped, so I file it as a suggestion and not RESIDUE. This carries R909-5-S2.
- **Optional fix.** "(the new-suite steps in the module docstring and table_problems())".

### R909-6-S2 - SUGGESTION - Tests - no loopback case binds one stream to two inputs

- After #948, one stream bound to several Stream Inputs is delivered once per input (`hdl/milan/milan_datapath.sv:8060-8065`). Each delivery carries the copy's mapping sideband (`:8519-8521`).
- Neither loopback harness binds one stream to two inputs, both with loopback-mapped channels. The copy is keyed by the input index, so this should work by construction.
- A parent case would pin it. It is optional: #948's own suites own the fan-out.

**Comment-rule and privacy scan.** I scanned the 91 lines that the PR's own post-merge commits add (`receipts/own_commits_added_lines.txt`; the scan output `receipts/own_commits_scan.txt` is empty). They contain:

- no bench lane label, lane name, review round, reviewer ID or comment ID;
- no host, device or tool name;
- no private path.

The new source comments (`loopback_wrap.sv:64-65`, `ctrl_configs.py:140`, `suite_shards.py:155-156`) cite #948, #979 and #998 by behaviour. The only review label in the delta is the one in R909-6-R1, which is prose in a page.

## Prior public findings at this head

| Finding | Status at `09201d35` | Evidence |
|---|---|---|
| R909-2-N2 MINOR and R910-2-F2 MAJOR (enabled 8x8 route) | **Basis withdrawn by the merge; carried as R909-6-N1.** They were closed for source-identical RTL, and the routed `hdl` tree is no longer the head's | `receipts/route_source_vs_head.txt` |
| R909-1-F2 MAJOR (disabled canonical netlist identity) | **Prior resolution retained by construction; not re-measured.** The PR's hdl patch is byte-identical before and after the merge. Its hunks are P-gated (generate branches, `24*(INPUT_LOOPBACK_P != 0)` widths, zero-count replications). They reference no signal dev's merge changed: only `dpkt_pcm_*`, which keep their declarations. Builder artifacts, descriptors and firmware images equal dev's | `receipts/merge_patch_compare.txt`, `receipts/builder_identity_dev_vs_head.log`; the author's firmware-image comparison `author-r7/receipts/identity--logs--fwimages-compare.md.txt` (hash-verified). See the limits |
| R909-2-N1, R909-3-N1, R909-4-N1 (planner registration, provisional figures, budget table) | **RESOLVED; still holding.** The 27th worker follows the registered rule. The self-test passes, the policy's projection table equals the planner, and the budget table is unchanged | the planner rows above; `docs/testing/CI_WORKFLOWS.md:684-688` |
| R909-5-R1 RESIDUE (now `docs/testing/CI_WORKFLOWS.md:681-682`) | **Not applied; carried as RESIDUE** with its exact fix: "The measured hosted worst case plus a stated margin sets each named entry, except a provisional one, which keeps its own arm until its hosted window is measured:" | `CI_WORKFLOWS.md:680-682` |
| R909-5-S1, R909-4-S1/S2/S3, R909-3-S1..S3, R909-2-S3/S4, R910-3-S1 | Optional and unadopted; none is affected by the delta | The artifacts are untouched, except `suite_shards.py:150`, carried as R909-6-S1 |
| R909-1-F1, F3..F7, R910-1-F1, R910-2-F1, R909-2-N3 and all earlier RESIDUE | **Prior resolutions stand.** Their artifacts are the harnesses, campaigns, render-queue and capture RTL and pages. They have no PR byte in this delta except `loopback_wrap.sv`, which was re-verified above. Both campaigns and both suites pass at this head | the probe table above |

## Lens results (this round)

```text
[R909] MINOR Conformance, RTL - R909-6-N1 - PR body route section; docs/design/INPUT_MAPPED_LOOPBACK.md:397-413; receipts/route_source_vs_head.txt (hdl 244c59e0 vs routed aefab080) - #979 Routing/Area unmeasured for the merged enabled composition
[R909] PASS Conformance (other criteria) - receipts/builder_identity_dev_vs_head.log (12+12 identical, control 11 differ); receipts/suite_input_loopback*.log; receipts/parent_mutants.log - end-to-end, mapping change, silence, plants and disabled builder identity hold at the head
[R909] PASS RTL (delta's own code) - tb/verilator/input_loopback/loopback_wrap.sv:64-69 vs KL_aaf_rx_depacketizer.sv:104-113,434-465 and aaf_audio_loop_wrap.sv:146-147; git show --cc 7049c524 (one automatic hunk, in a script) - verdict protocol matches dev's usage at N; no shipped RTL byte from the PR changed
[R909] PASS Robustness - receipts/parent_mutants.log, receipts/leaf_mutants.log, receipts/projection_vs_table_*.log, receipts/ctrl_configs_probe.log - invalidation, disconnection, truncated/overwritten page and per-stream output plants are caught at both shapes; the planner keeps every regular worker at or under 1276 s and the probe fails at the merge; the builder gets its Verilator through ctrl_runs.py:178
[R909] PASS Tests - receipts/leaf_mutants.log (7/7 caught), receipts/parent_mutants.log (15/15 caught, 2 controls), receipts/suite_input_loopback.log (79587/76017 checks, packets 468/447 unchanged), receipts/gate_suite_shards_py_selftest.log - the adapted harness is neither vacuous nor lossy; S2 optional
[R909] PASS Docs - docs/testing/{CI_WORKFLOWS,TESTING,RUNNING_TESTS}.md delta, sw/firmware/ctrl/README.md:158-160; receipts/gate_*.log, receipts/em_dash_base_*.log, receipts/projection_vs_table_head.log - 27-worker text and table equal the planner; docs gates green; R909-6-R1 and R909-5-R1 are RESIDUE only
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN** (R909-6-N1) | #979 acceptance; PR body; `INPUT_MAPPED_LOOPBACK.md:397-413`; builder identity; both suites; parent campaign | R909-6 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |
| RTL | **UNCLEAN** (R909-6-N1) | `loopback_wrap.sv`; the merge combined diff; the merged `KL_aaf_rx_depacketizer.sv`/`milan_datapath.sv` interfaces; the hdl tree against the route source | R909-6 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |
| Robustness | CLEAN | both campaigns; planner probe; builder registry | R909-6 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |
| Tests | CLEAN | both suites; leaf 7 plants; parent 15 plants plus 2 controls; planner self-test | R909-6 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |
| Docs | CLEAN (RESIDUE R909-6-R1 and R909-5-R1 carried) | three testing pages; firmware README; docs gates; em-dash gate | R909-6 | `09201d35d7ea720b3ba205da185ba35c159ec24a` |

## Real limits

- **No route, synthesis or netlist comparison ran in this round.** No implementation tool is installed here. Full Yosys banks are out of scope.
  - The disabled-netlist identity (R909-1-F2) is carried by construction, not re-measured against dev `5de21ff3`.
  - The enabled route and area remain open as R909-6-N1.
- **Not re-run by me:**
  - firmware images and the CPU budget harness. I verified the author's comparison by hash, not by rebuilding;
  - the firmware-boundary split legs and their judge;
  - `egress_ledger.py --point 8x8-1if`;
  - the docs builder legs;
  - the elaboration gates;
  - the `render_queue` and `chmap_capture` suites. Their RTL is untouched by the delta, and they are the author's receipts only;
  - other suites building the merged datapath;
  - the 27 shards;
  - portability.
- **Owner bounds.** Loads 0.70/0.75, last notice 140 ms, ACMP 30 ms, txL 49 ms and THE SHARE 2 ms were not re-measured. The delta changes no firmware source, and the default images equal dev's.
- **Hosted, snapshot 2026-11-25T16:55:45Z** (`receipts/hosted_check_runs_exact_head.tsv`). 58 check runs:
  - six completed with success: Verilator preflight, full-ci-gate, bdd-conformance, changes, docs-check-no-git and wire-accountability;
  - one completed as skipped: Physical gPTP, nightly and manual;
  - 20 in progress and 31 queued, including every Verilator shard, `firmware-verilator`, both boundary capture legs and the elaboration gates.

  I claim no hosted `rtl-fast`, `verilator-suites` or `yosys-portability` evidence at this head.
- **No manager source bank** exists at this head, and I infer none. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- **Hosted acceptance at `09201d35`.** No hosted run has yet completed:
  - either loopback suite (shards 14/27 and 15/27);
  - `firmware-verilator`, with the new builder;
  - the split `firmware-boundary` legs and judge;
  - the elaboration gates;
  - portability.
- **The merge-turn candidate** on current dev, with builder and native banks. Include disabled-image identity against that dev.
- **A disposition for R909-6-N1:** a fresh enabled route and area at a head with dev's #948 RTL, or a public decision.
- **The residue checklist:** R909-6-R1 and R909-5-R1.
- **The 27th worker.** Confirm it, or choose the author's 240 s alternative. Replace the provisional figures with hosted windows when they exist.

R909-6 FINISHED
