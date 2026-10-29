# HANDOFF — #803 round 3 (PR #805), dev merge round, executor [A693c]

Status: **REVIEW READY** at `e06ade312a80eb578579365134ab797cda90622b` (worktree clean, every submodule at its gitlink,
live remote dev `e78472ff` unchanged). Base head `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31` (POSITIVE, R727-2,
R728-2); dev `e78472ffde3da5eeecd4f00e27dcf58a24bfcfdf` (PR #802 for #799) merged as
`6fc0c2140ef66d10b71fb1b05213ae61741e34ed` (no rebase, no force; both are ancestors of the head); one commit on top,
`e06ade31`, the combined route's figures. Nothing pushed. Every gate the merge reaches is rc 0 at the head (section 5).
No STOP condition is met. The slice headroom stays an owner decision (16 of 15,850 free).

## Commits (one-line, no body, no trailer)

| Commit | Change |
|---|---|
| `6fc0c214` | Merge dev e78472ff (PR #802 for #799, processor f65c8ff7) into 803-adopt-gptp-f97c1803, keeping both adoption records and regenerating the ROM ledger and boundary diagram through their generators |
| `e06ade31` | Give the adoption record and the slice-headroom sentence the combined route's figures at processor f65c8ff7: 211 LUTs under the twelfth record, 53 FFs and 54 slices over dev's own route, 16 of 15,850 slices free, +0.303 ns WNS (#803) |

- Lane: $LANES/803-adopt-gptp, branch 803-adopt-gptp-f97c1803 (PR #805), from dev 5fcec84b
- origin: https://github.com/kebag-logic/milan-fpga.git (verified); fetched dev = `e78472ff` (PR #802 merged)
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/803#issuecomment-6486773443
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/803#issuecomment-6489654294
- Assignment: the [A10] round 3 ruling on #803 (dev merge round after #802)

## 1. Merge (no rebase, no force)

`git merge --no-ff --no-commit e78472ff` on `2b1565fd`; merge commit `6fc0c214` (parents `2b1565fd`, `e78472ff`).
Git conflicts: exactly the files the ruling lists. Every other file auto-merged; `hdl/milan/milan_datapath.sv`,
`.github/workflows/rtl.yml`, `docs/testing/CI_WORKFLOWS.md`, `TESTING.md`, `REGISTER_MAP.md` and
`tb/verilator/milan_dp/README.md` were changed on both sides in disjoint hunks.

| File | Resolution | Both sides' content |
|---|---|---|
| `CHANGELOG.md` | Contents: the #803 line, then the #799 line; sections: `## Unreleased - gPTP pin f97c1803` (:51) above `## Unreleased - processor pin f65c8ff7` (:87), newest first as the file runs | both entries verbatim |
| `docs/reference/SUBMODULES.md` | pin table: gPTP `f97c1803` (this lane) and processor `f65c8ff7` (dev), the gitlinks of the merge (`check_submodule_docs.py` reads them); adoption sections in merge order, #799 (:276) then #803 (:321), as the page runs oldest first | both sections verbatim, except :323 "The processor stays at `ed211803`" -> "`f65c8ff7`", the processor this adoption now sits on |
| `docs/testing/RUNNING_TESTS.md:88-89` | "6900 seconds" (this lane's physical deadline) and "nineteen `--ci-pieces` workers" (#799) | the two changed facts are on adjacent wrapped lines |
| `docs/design/AREA_BUDGET.md:142-145` | the table is dev's (the record at `e78472ff`); :143 the #803 route's slices, :144 this lane's owner-decision sentence verbatim, :145 dev's "70 slices left" and its owner decision of 2026-10-28 | dev's two sentences joined into :145 so "placement has" names one route; see section 2 for the figures |
| `syn/yosys/rom_digests.tsv` | generated: dev's file as input, then `bash syn/yosys/ooc.sh --record-rom-digests` (CPython 3.12.3, sv2v v0.0.12, Yosys 0.66), rc 0 | the generated ledger equals the union of both sides' rows (`receipts/merge/rom_digests_union.txt`) |
| `docs/diagrams/submodule_boundaries.{drawio,svg,png}`, `PNG_MANIFEST.json` | generated: this lane's manifest as input (it carries the `timesync_chain` entry for the f97c1803 diagram dev never touched), then `python3 docs/diagrams/submodule_boundaries.gen.py`, rc 0; `--check` rc 0 for it and `timesync_chain.gen.py` | the card shows processor `f65c8ff7c673` and gPTP `f97c18035be6`; the manifest differs from dev's only in the two diagrams this lane and the merge regenerate |

After the merge: `git submodule update --init --recursive` rc 0 (it checked protocol-processor out at `f65c8ff7` and
initialised `external` at its gitlink); every submodule's toplevel, origin, HEAD = gitlink and clean
(`receipts/merge/submodules-after-merge.txt`).

## 2. Area on the combined tree

Bank: `scripts/vivado_bank.sh` (round 1's bank, recipe unchanged: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`,
single-worker synthesis, `general.maxThreads` 32, Vivado 2026.1 Build 6511674), in a clean clone at the merge
`6fc0c214` (the later commit `e06ade31` changes three documents only), one Vivado run at a time, each under
`flock -x $VIVADO_LOCK`, each started above 20 GB MemAvailable, no sweep beside it. Each endpoint then
`python3 syn/ooc/pp_resource_gate.py check <dir> --endpoint <e>` against the record committed at `e78472ff` (the
twelfth record, #799, measured at `8b76de69` under the owner decision of 2026-10-28).

**Dev `e78472ff`'s own route is the record.** `git diff 8b76de69 e78472ff` touches no `hdl/`, `sw/litex`, `configs/`
or submodule file: only a comment block of `sw/mailbox/mailbox.yaml`, two Python test arms and the record itself. The
#799 lane's route at `8b76de69` checked against the record matched it in every figure (its receipt
`route-1x1-check-against-new-record.log`, LUT 52,012, FF 53,707, slices 15,780, WNS +0.440). So this adoption's share
is the merge head minus the record.

| Endpoint | Gate rc | LUT record -> merge (delta, tol.) | FF (delta, tol.) | Other |
|---|---:|---|---|---|
| route-1x1 | **0 PASS** | 52,012 -> 51,801 (**-211**, 500) | 53,707 -> 53,760 (**+53**, 600) | slices 15,780 -> 15,834 (**+54**, tol. 80): **16 of 15,850 free**; RAMB36 74, RAMB18 27, DSP 13 unchanged; WNS +0.440 -> **+0.303**, WHS +0.036 -> **+0.028** ns (floors +0.03 / 0) |
| ooc-1x1 | **0 PASS** | 24,346 -> 24,346 (0, 250) | 20,404 -> 20,404 (0, 250) | RAMB 16/3, DSP 8 unchanged |
| ooc-8x8 | **0 PASS** | 34,156 -> 34,156 (0, 316) | 29,782 -> 29,782 (0, 339) | RAMB 21/5, DSP 8 unchanged |

Route detail: 102,413 of 102,413 routable nets routed, 0 routing errors; IOB packing 21 PASS, 0 FAIL, 1 INERT
(`eth0_rx_er`, no net). Corners: Slow 0C / 85C WNS +0.303, WHS +0.051 ns; Fast 0C / 85C WNS +1.633, WHS +0.028 ns.
Logs: no CRITICAL WARNING or ERROR line (the one match is the IOB-pack check's echoed script text); the one
`Synth 8-6901` is dev's `crft_emit_en_w` (`milan_datapath.sv:3407`), as at #771 and round 1.

**This adoption's share against dev `e78472ff`'s own route: -211 LUT, +53 FF, +54 slices, WNS -0.137 ns,
WHS -0.008 ns.** Placed hierarchy, merge minus the #799 route (`receipts/vivado/route-hierarchy-merge-minus-dev.txt`,
from the two `utilization_hierarchical_place` reports): `KL_gptp_shadow` -169 LUT / +119 FF (round 1 measured +251 /
+119 over dev's route then: the FF growth repeats exactly, the LUT figure is placement); blocks this lane does not
touch move by placement as earlier rebaselines record, `pp_shadow` -313 / -26, `csr` +211 / 0, `avtp_rx_parser`
+116 / 0, `milan_datapath` (self) +77 / -106. Round 1, on processor `ed211803`, measured +310 LUT, +155 FF and +20
slices over that dev route; the slice figure is the stable one to read, and it grows 54 here.

The ooc tops are `KL_pp_shadow`, which instantiates none of the files this lane changes, so ooc-1x1 equals the record
in every figure, and so does ooc-8x8.

Bank timeline (`receipts/vivado/bank-timeline.txt`, UTC): route-1x1 03:14 -> 04:01 (47.7 min), ooc-1x1 04:01 -> 04:14,
rtl-8x8 04:14 -> 04:16, ooc-8x8 04:16 -> 04:44; every Vivado rc 0, every gate rc 0. Log digests:
`receipts/vivado/logs.sha256`.

STOP conditions for this item, none met: placement and routing complete; route-1x1 LUT -211 and slices +54 are within
the record's 500 and 80; free slices 16, above zero.

Tree: `docs/design/AREA_BUDGET.md:143` now reads "the shipping route at FPGA-gPTP `f97c1803` (#803) on processor
`f65c8ff7` places 15,834 slices, so placement has 16 of 15,850 left"; `:144` keeps the owner-decision sentence
verbatim ("The next growth on the shipping image therefore has no slice room and needs its own owner decision");
`:145` keeps #799's 70-slice record and its owner decision. The ruling's `:140` / `:141` are these two lines; dev's
three added lines above them move them by three. `CHANGELOG.md:82-85` and `docs/reference/SUBMODULES.md:371-381`
carry the same figures (commit `e06ade31`).

## 3. CI shards

This PR does not change the `milan_dp` case inventory, so no leg index re-deals (#804) and no worker figure moves.
The six CI piece suites' inventories, read the way the planner reads them (`ci_suite_pieces.inventory`, the owning
driver's `--list`, GNU Make 4.3), are byte-identical at dev `e78472ff` (clean clone) and at the merge head:
`milan_dp` 24 cases, `milan_dp_mclk` 34, `capture_coherence` 43, `maap` 66, `milan_dp_render` 3, `pp_shadow` 4
(`receipts/shards/inventory-*.json`, `inventory-compare.txt`; runner `scripts/inventory_compare.sh`). This lane
changes no case driver: its `tb/verilator/milan_dp` diff against dev is `sim_gptp.cpp` (checks inside the `gptp` and
`gptp-lat` cases), `sim_ax1x1gptp.cpp` (the scheduled physical suite, outside the 19 workers) and the README; its
`scripts/run_all_suites.sh` diff is the physical suite's deadline. So the 19-worker projection is dev's, unchanged, and
no figure changed.

| Check (head `e06ade31`; also run at the merge `6fc0c214`, the same) | rc | Result | Receipt |
|---|---:|---|---|
| `python3 scripts/suite_shards.py --selftest` (CPython 3.12.3, and again inside each worker's step on 3.14.8) | 0 | `selftest: PASS` | `receipts/shards/ownership/selftest-cpython-3.12.3.log` |
| The `verilator-shards` job's "Prove specialized suite ownership" body, literally, for SHARD 0..18 of 19 (`scripts/ownership_step.sh`) | 0 x19 | every worker lists its suites; worker 1 owns `tsn_fuzz`, worker 3 `chmap_capture` | `receipts/shards/ownership/shard-*.log`, `summary.txt` |

The step runs on the host's system python3 (3.14.8): the driver's process-ownership preflight needs
`os.pidfd_open`, which the standalone CPython 3.12.3 build here lacks ("REFUSED: process ownership: unsupported process
facilities"); the hosted image's system python3 has it, and the sweep units use the same 3.14.8.
## 4. Physical leg

The README's method (`tb/verilator/milan_dp/README.md:409-437`) scales the slowest hosted simulation of the
849,624,822-cycle scenario by the cycle ratio, in its two branches, and adds the 830 s hosted remainder. Its only
head-dependent input is the scenario's cycle count, measured here by running the leg at the head:

| Quantity | Value | Receipt |
|---|---|---|
| Scenario at `e06ade31` | `simulated_duration_seconds=17.992742740 cycles=899637137`: equal to the README's figure, so the README needs no change | `receipts/physical/milan_dp_gptp.log` |
| Hosted projection, the two branches | 5,346.8 s and 5,484.0 s | `receipts/physical/projection.txt` (`scripts/projection.py 899637137`) |
| Against the 6,900 s suite deadline | 77.5 % and **79.5 %: the worst case is within the 80 % bound** | same |
| The 145 min job | margin 53.6 to 55.9 min, worst case 63.0 % | same |

Per-cycle cost, checked because the merge adds #799's RTL to the model: both heads' physical binaries
(`2b1565fd`, round 2's build, and `e06ade31`) ran together for the same 540 s, each pinned to its own CPU, and every
`PROGRESS` line was timestamped. Over the simulated interval both reached (0.25 to 0.75 s) the merge head took
**0.981x** the wall time of `2b1565fd` (643.5 against 655.8 wall s per simulated s;
`receipts/physical/sim-rate-2b1565fd-vs-e06ade31.json`, `scripts/sim_rate.py`). The merged RTL adds no measurable
per-cycle cost, so the cycle-ratio method still describes the head. The full local runs (round 2: simulation 4,213 s;
here 4,325.5 s) ran under different host loads and are not a per-cycle comparison.

The leg itself at the head (`scripts/run_all_suites.sh <logs> --wait --physical-gptp`, `SUITE_TIMEOUT` unset, so the
6,900 s default governs; then `suite_tally.py <logs> --quiet --expect-suite-root tb/verilator --physical-gptp`): rc 0,
0; 1 / 1 suite, **205 checks, 0 failures** (physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre 14);
simulation 4,325.5 s; suite 5,450 s, 79.0 % of 6,900 s on this host beside the four sweep shards, the rtl-fast
replica, Yosys and the static bank.

## 5. Gates (head `e06ade31` unless noted; every command unpiped, its own rc and log)

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Vivado route-1x1, ooc-1x1, rtl-8x8, ooc-8x8 at the merge `6fc0c214`, each `pp_resource_gate.py check` | 0 x4, gates 0 x3 | section 2 | `receipts/vivado/` |
| Inventory comparison and the ownership step, x19 | 0 | section 3 | `receipts/shards/` |
| Merge-index gates before the merge commit: `check_submodule_docs.py`, `check_gptp_docs.py` (plain and `--with-submodule`), `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `docs_check.py`, `check_feature_status.py`, `ci_events.py --check`, `suite_shards.py --selftest`, `pp_resource_gate.py check-baseline`; then at `6fc0c214` the four idiom gates, hygiene, naming, ports, test evidence, source lists, `pp_srcs`, integrator params, `ci_gate_workflows.py --check` | 0 x23 | all PASS / OK | `receipts/premerge/table.txt` |
| Generators: `ooc.sh --record-rom-digests` (dev's ledger in, union out), `submodule_boundaries.gen.py` then `--check`, `timesync_chain.gen.py --check`, `ci_gate_workflows.py --check` on the auto-merged `rtl.yml` | 0 x5 | ledger = union of both sides' rows; diagrams OK; workflow equals its generator's output | `receipts/merge/` |
| Docs workflow replica (`docs_steps.py`: the `run:` bodies literally, GNU Make 4.3, CPython 3.12.3), clean clone at `e06ade31`, base = dev `e78472ff` | 0 | 44 steps, 0 failed: 42 run, 2 skipped by rule (gate_42 runs the candidate act runner on the host; the no-git job's body deletes `.git`). Includes `ci_events.py --check` and `--selftest`, `ci_gate_workflows.py --check` and its self-test, `measure_test_evidence.py`, the four idiom gates, the em-dash gate against dev, concise style, TOC, `docs_check`, the diagram and PNG gates | `receipts/docs/all.out`, `all-receipts.json`, `all.sha256` |
| Builder legs in the replica | 0, 0 | leg 0: ALL GATES PASS EXCEPT 1 NOT RUN (gate 1b, inert under Make 4.3); leg 1 without a LiteX interpreter: EXCEPT 16 NOT RUN (the LiteX chain arms and gate 11), as rounds 1 and 2 | `receipts/docs/docs-gates-*.not-run.txt` |
| Builder leg 1 again with the LiteX interpreter | 0 | 1 step, 0 failed; EXCEPT 1 NOT RUN (gate 11, the absent mf48 calibration build), as rounds 1 and 2 | `receipts/docs/leg1-litex*` |
| The five Markdown gates on CPython 3.12.3 | 0 | 5 steps, 0 failed | `receipts/docs/md312*` |
| No-git job's gates on a `git archive` export | 0, 0 | `docs_check`, feature status: 0 findings | `receipts/docs/nogit_*` |
| Static and pin-record bank (`scripts/static_bank.sh`), clean clone at `e06ade31` | 0 x33 | `check-baseline` PASS; `ooc.sh --record-rom-digests` then `git diff --exit-code` (ledger byte-identical); both diagram `--check`; `check_submodule_docs`; `check_gptp_docs --with-submodule` and plain; ports, naming, test evidence, integrator params; lint 89 <= 89 and its self-test; `flock -x` xvlog 0 findings == ratchet; four idiom gates and two self-tests; source lists; `pp_srcs`; `sw/builder/test_builder.py` ALL GATES PASS EXCEPT 2 NOT RUN (gate 1b, gate 11, as round 1); hygiene, fail-fast, TODO ownership, module matrix, SoC sources, NVM capture, feature status, `docs_check` | `receipts/static/table.txt` |
| `syn/yosys/run.sh` (full serial; Yosys 0.66, sv2v v0.0.12), clean clone at `e06ade31` | 0 | tops 60, pass 60, fail 0; tied inputs 29, justified 2, unjustified 0; TAP-PURITY PASS (1,365 s) | `receipts/yosys/` |
| rtl-fast replica (`rtl_fast_steps.py`: every job of the aggregate's `needs:`, the `run:` bodies literally, a pull_request event against dev `e78472ff`), clean clone at `e06ade31` | 0 | `rtl-fast: success; failed jobs: none`; 12 / 12 jobs success, 56 steps rc 0 (5,671 s); `bdd-conformance` runs `cd tests && behave`: **14 features, 495 scenarios, 2,288 steps passed**, 0 failed, 0 skipped | `receipts/rtl-fast/` |
| Full sweep, 4 shard units (`native-shards.py 803-a693c <spec> <out> 4 0-15 16-23 24-27 28-31`, MemoryMax 10G, -j4) | 0 x4 | shard 0 14/14 suites (1,575,325 checks, 3,323 s, peak 5 GB), 1 17/17 (14,364, 3,394 s), 2 17/17 (251,927, 4,850 s; `capture_coherence` on four CPUs, peak 6 GB), 3 16/16 (350,078, 3,977 s); 0 failed, 0 timed out in each | `receipts/sweep/shard-*`, `shard-summaries.txt` |
| `python3 scripts/suite_tally.py <union of the four shards' logs> --quiet --expect-suite-root tb/verilator` (and without `--quiet`) | 0, 0 | **64 / 64 suites, 2,191,694 checks, 0 in-suite failures, 0 timed out** (round 2: 2,191,421; #799 adds the `sidmove` legs and its checks): `milan_dp` 13,757 over 20 tallies, its `gptp` and `gptp-lat` legs `202 checks: 202 PASS, 0 FAIL` each; `milan_dp_gm_steps` 202, `gptp_shadow` 325, `gptp_plane` 99, `tsn_fuzz` 897, `capture_coherence` 21,721 | `receipts/sweep/suite-tally-quiet.out`, `suite-tally-per-suite.txt`, `union-logs.sha256` |
| milan_dp_gptp (physical) at `e06ade31` | 0, 0 | section 4: 205 checks, 0 failures; 5,450 s of 6,900 s | `receipts/physical/` |
| Controlled per-cycle comparison, `2b1565fd` against `e06ade31` | 0 | 0.981x | `receipts/physical/sim-rate-*.json` |
| Final state: worktree, submodules, remote | - | `git status` empty; six submodules toplevel = path, origin as `.gitmodules`, HEAD = gitlink, clean; `git ls-remote origin refs/heads/dev` = `e78472ff`; `2b1565fd` and `e78472ff` are ancestors of the head | `receipts/merge/submodules-final-e06ade31.txt` |

Not re-run, by rule: the act replica (the head is not pushed, and the runner rechecks the remote head); the mutant
streams of rounds 1 and 2 (no line of `sim_gptp.cpp`, `KL_gptp_shadow.sv` or the gPTP engine changed in the merge:
`git diff 2b1565fd e06ade31 -- tb/verilator/milan_dp/sim_gptp.cpp tb/verilator/gptp_shadow hdl/ieee8021as
gptp-processor` is empty, and the clean legs those streams grade pass 202 / 202 at the head).
## STOP conditions (none met)

- The combined route fails placement or routing: no. 102,413 of 102,413 routable nets routed, 0 errors.
- route-1x1 LUT or slices exceed the record's tolerance: no. LUT -211 (tolerance 500), slices +54 (tolerance 80);
  FF +53 (600); RAMB and DSP unchanged; WNS and WHS above their floors.
- Free slices go below zero margin: no. 16 of 15,850 free.
- A conflict needs a design decision: no. Every conflict kept both sides' content; the one sentence edited beyond
  joining is the #803 section's "The processor stays at" pin, which the merge itself sets (`f65c8ff7`).

## Open risks and questions (published in REVIEW READY)

1. **Slice headroom is still an owner decision.** 16 of 15,850 slices are free at the combined route; this
   adoption adds 54 over dev's own route (round 1 measured 20 over the earlier dev route, which left 7). `AREA_BUDGET.md`
   states it and keeps the owner-decision sentence. Not ruled here.
2. **The physical deadline is a projection** (79.5 % worst case) until a hosted run of the current scenario
   completes.
3. **Interpretation:** the ruling's `AREA_BUDGET.md:140` and `:141` are `:143` and `:144` after the merge (dev added
   three lines above them). Dev's "placement has 70 slices left" now reads "The record's route leaves 70 slices", beside
   its owner decision, so "placement has" names one route only.
4. **Interpretation:** the #803 pin-page sentence "The processor stays at `ed211803`" now names `f65c8ff7`, the
   processor this adoption sits on after the merge; its CHANGELOG entry names no processor pin.

## Run notes

- `git submodule update --init --recursive` initialised `external` (SSH) for the first time in this lane; nothing
  reads it (the sweep units exclude it), and it sits at its gitlink.
- Sweep, first launch: every shard's preflight refused because the spec's TMPDIR (`tmp-sweep`) did not exist
  (`mktemp: failed to create directory`); no suite ran. Second launch (CPUs 16-19 / 20-23 / 24-27 / 28-31): stopped
  with `systemctl --user stop` within a minute, during preflight, when CPUs 0-15 freed; no suite result used. Third
  launch (0-15 / 16-23 / 24-27 / 28-31) is the reported run (`receipts/sweep/attempts.txt`). The other lane held CPUs
  32-111 throughout; shard 2 (`capture_coherence`) kept four CPUs, as in round 2, below its OOM point.
- The ownership step runs on the host's system python3 3.14.8: the standalone CPython 3.12.3 build lacks
  `os.pidfd_open`, which the driver's process-ownership preflight requires.
- The physical leg ran beside the sweep, the rtl-fast replica, Yosys and the static bank; its wall time is reported
  against its deadline, and the deadline verdict is the README projection's.
- The Vivado bank ran alone (no sweep); beside it ran the docs replica and light gates only (unit anon at most 6.2 GB).
