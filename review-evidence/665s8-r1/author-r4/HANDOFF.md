# HANDOFF: #868 (#665 S8), wire timing in the split simulation ([A758c], rounds 3 and 4)

Status: REVIEW READY at `dbe54e46f0` (round 4; its gates below all pass). Round 3 ended REVIEW READY at `e3f96a67b5` (issuecomment-6800331535), with the one full clean-clone pass at that head (the round 3 gate table, further down).

## Round 4 (2026-11-11 20:26 local on): controls only

Authority: the manager's ruling on R815-2 (NEGATIVE, one MINOR) and R816-2 (POSITIVE) at `e3f96a67`, #868 issuecomment-6805224780: round 4 adds the controls R815-2 F1 (PR #879 issuecomment-6805127079) asks for, exactly as its Required outcome and Verification state; no harness behaviour, figure or firmware changes. Gates: the wire-timing self-test, `run.py --ci`, the docs gates and `git diff --check`, on a clean clone of the final head.

- The tree was clean at `e3f96a67b5` when round 4 began; nothing was uncommitted.
- REVIEW READY for round 4: issuecomment-6806398083 (the text in `REVIEW-READY-COMMENT.md`; round 3's is kept as `REVIEW-READY-COMMENT-round3.md`). No new TAKEN (round 3's, issuecomment-6788798513, stands). Nothing pushed.
- One commit, `dbe54e46f0`, `wire_selftest.py` and the harness README only (`receipts/round4/diff-round4.txt`):
  - `wire_selftest.py:241` `loaded()`: the clean loaded log gains a MAAP arm that the final probe expiry's pass makes and cancels before its deadline (`CANCELLED_DEADLINE`, 1,720 ms, inside the log), as the firmware's final probe expiry does with its 2,210 ms deadline; its burst is delivered whole and meets no expiry. It also gains a last AECP offer the log ends inside, one of its three frames received. The MAAP arms are now read as arms only (a cancel is no arm) and in cycle order.
  - `wire_selftest.py` `LOADED`: MAAP 5 queued, 5 armed, 4 delivered, 3 met; AECP 2 queued, 1 delivered whole, 1 in part.
  - `received-frame-unaccounted`'s words follow the larger log: 17 delivered load frames, 26 received.
  - New control `load-offer-over-delivered` (R815-2 F1's option): a fourth frame received under the first offer's tag, of three queued; words `LOAD: 4 frames of offer 0 of load acmp were received, 3 were queued`, its only finding.
  - `README.md` (Controls and self-test): `clean-loaded`'s description and counts, the two control rows.
- Not taken, as the ruling limits round 4 to controls: R815-2 S1 (the CI page's cold figure) and S2 (the `window` local in `acmp()`). R1 (the PR body's 693 s sentence) is fixed in `PR-BODY.md`, which is not in the tree.

### New and changed checks (planted mutant, failing words)

| Control | Planted mutant | Failing words |
|---|---|---|
| `clean-loaded` (clean, extended) | none: a cancelled arm's burst delivered, an offer delivered in part | (must pass, with `LOADED` exactly: MAAP met 3 of 4 delivered, AECP partial 1) |
| `load-offer-over-delivered` (new) | a fourth frame under offer 0's tag, three queued | `LOAD: 4 frames of offer 0 of load acmp were received, 3 were queued` |
| `received-frame-unaccounted` (words updated) | one frame of the AECP offer received untagged | `LOAD: 17 delivered load frames and 4 a draw (2 draws) are not the 26 frames the model received` |

Self-test: `50 controls, 0 failed`.

### R815-2 F1's Verification

`scripts/delta_mutants.py` from the R815-2 packet, unchanged (sha256 `27d4b028f477f3ad`, equal to the packet's), on a disposable clone at `dbe54e46f0` (`receipts/round4/delta_mutants.log`): `expiry-met-ignores-arm` and `partial-offers-never-counted` are KILLED (`clean-loaded` fails); the other 11 stay KILLED. `over-delivery-check-gone` now makes the self-test fail (rc 1, failing `load-offer-over-delivered`), but the script scores it SURVIVED because it expects `clean-loaded` to fail, which no clean log can for an over-delivery (a clean log has no finding). A copy that changes only that mutant's expected control to `load-offer-over-delivered` (`delta_mutants_overdelivery_control.py`, its diff in the file's docstring) reports 14 of 14 KILLED. The clone was restored after each mutant (0 changes).

### Round 4 gate table

At `dbe54e46f09802ab8b9bd3f3223d36bf4891394b`, each on its own fresh clone (`gates4/` in scratch; receipts `receipts/round4/gates/`). CPUs from `cpu_ranges.py show` (64-79, 80-95 free): the `wire-timing` job on 64-67, the docs jobs on 80-87, the self-test and `git diff --check` on 68-71.

| Gate | Command / runner | Result | Receipt |
|---|---|---|---|
| the wire-timing self-test | `python3 -B tb/verilator/ctrl_wire_timing/run.py --self-test` | rc 0, `50 controls, 0 failed` | `round4/gates/extra/logs/wire-self-test.log` |
| `run.py --ci`: `rtl-fast / wire-timing`, every `run:` step | `run_wf.py rtl-fast wire-timing` (LiteX venv) | 4 steps rc 0, 10 not run with a stated reason, 0 bad; the step `PASS, wall 564 s` (build 80 s, the CPU netlist from the local generator's cache) on 4 uncontended CPUs, both runs `0 finding(s)`, both plants caught; results, logs, stimulus and UART byte-identical to the measurement | `round4/gates/wire-timing-job-table.md`, `round4/gates/rtl-fast/logs/`, `round4/gates/wire-timing-ci-vs-head.txt` |
| the docs gates: `docs.yml`, 9 jobs, every `run:` step | `run_docs_yml.py` per job | 64 steps rc 0, 31 not run with a stated reason, 0 failed (docs-gates-0 1,250 s, docs-gates-1 1,114 s, docs-gates-2 664 s on 80-87) | `round4/gates/docs-yml-table.md` |
| `git diff --check` against the merge base `1d6bf5556a` | `git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD` | rc 0 | `round4/gates/extra/logs/diff-check.log` |

Trees clean after each gate.

## Round 3

- TAKEN: issuecomment-6788798513 (2026-11-11). REVIEW READY: issuecomment-6800331535 (2026-11-11, the text in `REVIEW-READY-COMMENT.md`). PR body for the manager: `PR-BODY.md`. Nothing pushed.
- Lane `$LANES/665-s8-wire-timing`, branch `665-s8-wire-timing`; scratch `/data-2/milan/tmp/665s8-a758c`.
- The prompt's line "the lane is at 086e186e" names round 1's first commit; the lane was at `bfb2df3707` (round 2's head, `086e186e87` its ancestor), as the round 3 text says. Remote `origin` is `https://github.com/kebag-logic/milan-fpga.git`; `origin/dev-soft-core` `1d6bf5556a`, unchanged on the remote (`git ls-remote`, 2026-11-11).
- **Host incident, 2026-11-11 about 09:15 local:** the root filesystem (`/dev/sda2`, which holds `/home`) was remounted `emergency_ro` by the kernel, and reads from it stalled for tens of seconds. `/data` (the lane) and `/data-2` (scratch) stayed writable. From then on this handoff, the PR body and the receipts were staged under the scratch's `out/` and copied to the output directory when it could be written again (see the end of this file).

## Timeline

- 07:48 local: commits `a3ec99904d` (stimulus), `0e38c2fdd2` (reuse guard), `267fc9815d` (grader, model, self-test, run.py) on `bfb2df3707`. Self-test `49 controls, 0 failed`.
- 07:50: the CI step at `267fc9815d` from a clean clone on CPUs 120-123 (`WIRE_JOBS=4`), its 1x1 build from scratch (ready after 85 s), PASS, wall 693 s; the 8x8/2if build (88 s) and its two 16-draw runs on CPUs 116-119, rc 0 each.
- 08:0x: the four campaign units on that 1x1 build, `systemd-run --user --unit=milan-a758c-camp<N> -p MemoryMax=4G taskset -c <range>`, ranges 8-15, 24-31, 32-39, 40-47 (`cpu_ranges.py pick`: the two free halves, then the halves of a free 16 block); seeds 1-4, loads none, none, composed, composed.
- The reviewers' probes at `267fc9815d`: every one found or refused by its own words (below).
- 08:25: the hosted run of PR #879 at `bfb2df3707` (run 42906628236) shows `wire-timing` (job 130154674162) failed its gate step at the build: `ModuleNotFoundError: No module named 'pythondata_software_picolibc'` (`tb/verilator/ctrl_service_budget/build.py:192`). The job installs `sw/litex/litex_pins.txt`, which carries no runtime sources; the bench venv has them, so no local pass could see it. No reviewer saw it: the job was queued when both reviews ended. Commit `528554c93f` installs the two packages at the bench venv's revisions (item 5; below).

- 08:30: commit `528554c93f` (the `wire-timing` job's runtime sources; item 5). At about 09:05 a replica of that job as a fresh runner does it (fresh clone, fresh venv by the job's own install steps, no bench venv) was begun in scratch `replica/`.
- **Host reset, 2026-11-11 09:23 local** (after the 09:15 read-only root filesystem): every unit was killed. The campaign units had run 07:02Z-08:23Z of about 2.5 h, so none finished; the replica was in its LiteX install. Resumed 09:55 local: the tree held the README edits uncommitted and the four commits; nothing else was lost. The staged handoff and receipts were copied from scratch `out/` to the output directory, and every receipt the stall left empty was rebuilt from its scratch source and checked byte for byte (`receipts/head/*` against each run's directory; the reviewer scripts against their packets).
- 09:57 local (08:57Z): the four campaign units restarted on the same 1x1 build (the reuse guard accepted it at the restart: the head changes nothing it records), the same commands, ranges 8-15, 24-31, 40-47, 48-55 (`cpu_ranges.py`: three free halves and the first half of a free 16 block). The killed runs are kept as `camp<N>/killed-at-reset/` in scratch, not cited.
- 09:58 local: the replica restarted from scratch as unit `milan-a758c-replica`, CPUs 56-63 (the step on 56-59), with the host's offline Scala settings (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`, as round 2's environment); the Scala caches are copies of the host's, as a cache restore; the CPU metadata cache is empty, as on a cold runner. The killed attempt is kept as `replica/killed-at-reset/`, not cited.

- 10:00 local: the replica at `528554c93f` got past the hosted failure (the runtime archives built, the image linked) and stopped at the CPU half's export: `ImportError: pythondata-misc-tapcfg module not installed!` (`litex/build/sim/verilator.py:189`, LiteX's simulation export reads tapcfg's data). `sw/litex/litex_pins.txt` carries no tapcfg either, so the hosted job would have stopped there next. Diagnosis in the replica's own venv: with `pythondata-misc-tapcfg` at `a12c3f59` (the bench venv's checkout) installed, the step passed, `PASS, wall 892 s`, its results, logs, stimulus and UART byte-identical to the head's bench-venv runs (`receipts/replica/attempt1-528554c9/`).
- 10:2x: commit `fbe5acc983` adds tapcfg to the same install step (renamed), its pinned entry and the CI page. The full replica restarted from scratch at `fbe5acc983` (unit `milan-a758c-replica2`, CPUs 56-63, the step on 56-59): every setup step rc 0 (the venv; `pip install -r sw/litex/litex_pins.txt`; `ci_litex_env.py`; the patch series; the job's own runtime-sources step, read from the workflow at the head; the SDK; Verilator 5.050), then the step `PASS, wall 1299 s`, the build 323 s with the CPU netlist generated cold by sbt (no metadata cache), both runs `0 finding(s)`, both plants caught on each. Results, logs, stimulus and UART byte-identical to the head's bench-venv runs (`receipts/replica/replica-vs-head.txt`). Host load about 120 then. The interpreter was the host's Python 3.14, the hosted job's 3.12.
- 10:27: another lane's `capture_coherence` sweep ran 32 threads on CPUs 40-47, campaign unit 2's range, leaving its simulator half a core. With every free range of the host taken (`cpu_ranges.py`: 124 of 128 CPUs held), each unit's simulator was pinned to two CPUs of unit 0's own range (8-9, 10-11, 12-13, 14-15) and each unit's other processes to 8-15, which handed 24-31, 40-47 and 48-55 back (`camp<N>/cpus.txt` in scratch).

- 12:42 local: all four campaign units ended rc 0 (below). 12:44: commit `e3f96a67b5` (docs: the harness page's results, campaign, load counts and reuse record; milan_dp's `print-split-srcs`; the MAAP note at the head's and the campaign's figures). This is the final head; the one clean-clone gate pass runs on it.
- 12:46: the gate pass began, each chain a unit with `taskset` first in its ExecStart. CPUs: the gate range 0-95 had only 20-23 and 64-67 free (`cpu_ranges.py show`: 120 of 128 held), so chain A (rtl-fast's census, boundary and short jobs) ran on 20-23 and chain C (docs.yml, then elaborate.yml, which holds the 900 s `test_soc_timing_cuts` wall clock) on 64-67, uncontended; chains B (rtl-fast's `wire-timing` and firmware jobs) and D (rtl.yml's gate and Yosys shards, then the named extra gates) on session-pool blocks 108-111 and 112-115, as round 2 ran them. The docs jobs first stopped before any clone (the runner's skip list `not_run.json` was not copied; no step ran; kept as `gates/docs-runner-error/`), and ran again at 12:48 in a unit of their own, 104-107. `physical-gptp` is not run: a pull request does not trigger it (its `if:`), recorded in `not_run_rtl.json`.
- 13:12: the sweep. MemAvailable was 17-24 GB, under the 30 GB the four-shard rule needs, so the shards run serially, each by the same clone, unit and command `native-shards.py` issues (`shard_some.py`, its copy for the listed shards), shard 2 (`capture_coherence`) first on 48-51; a later shard starts beside it only while MemAvailable is above 30 GB.

- 13:22: MemAvailable rose to 34 GB, so shards 0, 1 and 3 started beside shard 2, on 80-83, 84-87 and 88-91 (the same launcher).
- 14:05: chains A and C done; the named extra gates (`extra.sh`) moved to a unit of their own (`chainE.sh`) on 20-23 and 52-55, the gate range's free 4-CPU blocks then, instead of waiting for chain D's last Yosys shard; `extra.sh` claims itself once, so chain D skips it when it gets there (`gates/extra-claim.log`).

- 16:46 local: the pass ended, every gate with a passing result (below); receipts collected into `receipts/gates/` and `receipts/sweep/`, host paths written as placeholders; `receipts/INDEX.md` generated from the files present.

## Changes (file:line, reason)

| File:line | Reason (ruling item; finding) |
|---|---|
| `tb/verilator/ctrl_wire_timing/wire_grade.py:472` | a bind's PROBE_TX is the first after its own BIND_RX_RESPONSE and before the next draw's bind; none is a finding (`:475`), censored only when the log ends within the bound (1; R815 F3, R816 F1) |
| `wire_grade.py:502` | the graded PROBE_TX transactions must equal the draws (1) |
| `wire_grade.py:468` | a BIND_RX_RESPONSE whose status is not SUCCESS, IEEE 1722.1-2021 Table 8-3 (1; R816 F1 R4) |
| `wire_grade.py:530` | an AEM or MVU final response whose status is not the scenario's stated one (`statuses`, by default `wire_scenario.aecp_statuses`, `:690`); a graded command with no stated status is refused (2; R816 F2) |
| `wire_grade.py:624` | at `announces > 1`, no `adp.advertise_period` sample is a finding (1; R815 F3) |
| `wire_grade.py:625` | a log that runs on 9,400 ms past its last ENTITY_AVAILABLE has stopped advertising: the same defect anywhere in a run (1; R815 F3) |
| `wire_grade.py:597`, `:133`, `:316` | the advertise period's clause text carries the widened 4,998 to 9,400 ms bound, and its row publishes `strict_ms` 9,000 and `strict_margin_ms` beside the widened margin (6; R816 SUG-1) |
| `wire_grade.py:203` `Offer`, `:216`, `parse` | each LOAD line with its queue cycle, trigger, skips per interface, and the interfaces whose first ANNOUNCE had left (TXW, TXB) by then, in log order; RXW and RXB tags counted; an old-format LOAD line is refused (3, 4) |
| `wire_grade.py:642` `loads` | queued (offers, those an arm queued, frames, echoes skipped), delivered (offers whole and in part, frames, by tag) and expiries met (the arm expired, its burst delivered), apart in `results.json` and the table (4; R815 F2) |
| `wire_grade.py:672` | delivered load frames + 4 a draw must equal SUMMARY `rx_frames` + `bench_rx` (`summary_count`, `:285`), on every run (4) |
| `wire_grade.py:669` | an echo skipped after its interface's first ANNOUNCE left is a finding (3; R815 F1) |
| `wire_main.cpp:139`, `:489` | each echo keeps its own newest match as each frame is sent, so the ANNOUNCE is found whenever one has been sent; the 64-frame history of every protocol is gone (3; R815 F1) |
| `wire_main.cpp:504-524`, `:324` | each offer tagged `load-<name>-<n>`; the LOAD line gains its queue cycle, its trigger (the arm's slot, or `-`) and its skips per interface (3, 4) |
| `wire_main.cpp:531-532` | `defload` after the first frame sent, or twice, is refused: an echo matches from its definition on |
| `wire_scenario.py:111` | GET_AVB_INFO is 0x0027 on AVB_INTERFACE 0, its IEEE 1722.1-2021 7.4.40.1 command (descriptor_type 9, descriptor_index 0) (2; R816 F2) |
| `wire_scenario.py:102`, `:117` | each AEM command's stated final status, SUCCESS for all, which the grader reads (2) |
| `wire_scenario.py:18`, `:29-35` | `THE LOAD (#868):` (6; R815 R1, R816 RES-1); the echo's text |
| `wire_build.py:225` `inputs` | the reuse record: the recipe's own source list (`split_sources`, `:131`: milan_dp's `print-split-srcs` at the build's `split_vars`, `:114`), every file a Verilator run or the native compile read (`read_by_tools`, `:153`, from each `__ver.d` and `.d` file), the export's checkout modules, the shape's config, `TOOLS` (`:86`, `milan_dp/Makefile` among them) and `tree:firmware` (`:239`: the CPU budget harness's `FIRMWARE_TREES`, `:83`, tsn-c-stack and lwSRP among them) (5; R815 F4, R816 F3) |
| `wire_build.py:3-35` | the docstring states what the record holds |
| `wire_build.py:271` | a build.json with no inputs is refused |
| `wire_soc.py:136` | `generator_modules`: the checkout's modules the export imported, for the record (5) |
| `tb/verilator/milan_dp/Makefile:1096` `print-split-srcs` | the split recipe's whole source list at its SPLIT_* variables (5); the recipe's own command lines are unchanged |
| `run.py:191` `refusing` | a refused stimulus or an unreadable log is exit 2 on `--point`, `--campaign` and `--regrade` too (R815 S1) |
| `wire_selftest.py` | 16 new controls (below); the synthetic logs carry each draw's unbind and the model's SUMMARY counts; the `Changes` and `Queued` dataclasses keep the Python idiom gate's parameter limit |
| `.github/ci-templates/rtl-fast.yml:744-754`; `.github/workflows/rtl-fast.yml` (by `scripts/ci_gate_workflows.py`) | the `wire-timing` job installs `pythondata-software-picolibc` at `6a13ccce`, `pythondata-software-compiler_rt` at `6eb76609` and `pythondata-misc-tapcfg` at `a12c3f59`, the bench venv's checkouts (item 5; the hosted failure and the replica above; commits `528554c93f`, `fbe5acc983`) |
| `scripts/ci_events.py:2658` | the job's pinned step list carries the new step |
| `docs/testing/CI_WORKFLOWS.md:465-485` | the new step, its three packages and why; the CI step's local wall time at the head, 693 s |
| `tb/verilator/ctrl_wire_timing/README.md` | both rulings linked; the reuse record; the LOAD line and tags; GET_AVB_INFO; the echo; the PROBE_TX pairing, the statuses, the advertise checks and the load counts; the head's results; the campaign; the controls |
| `tb/verilator/milan_dp/README.md:1203-1207` | `print-split-srcs` |
| `sw/firmware/ctrl/maap/README.md:47-50` | (pending) the egress note's figures at the head |

No firmware, shape config, ring geometry, saved-state, contract, production RTL or `milan_soc.CtrlMailbox` change.

## New checks (planted mutant, failing words)

`run.py --self-test`: `49 controls, 0 failed` (`receipts/head/ci-head.console`). Each control is a planted mutant of a clean input, refused or found by its own words; each clean input must pass. The 16 new ones:

| Control | Planted mutant | Failing words | Item |
|---|---|---|---|
| `clean-reuse` (clean) | a stand-in build directory recorded by `wire_build.inputs` | (accepted) | 5 |
| `reuse-after-an-edit-of-tb_split_top.sv` | its recorded digest changed, as an edit after the build leaves it | `'tb/verilator/milan_dp/tb_split_top.sv'` | 5 |
| `reuse-after-an-edit-of-milan_datapath.sv` | the same for the datapath | `'hdl/milan/milan_datapath.sv'` | 5 |
| `reuse-after-an-edit-of-KL_mbx.sv` | the same for the split top's KL_mbx | `'hdl/milan/mailbox/KL_mbx.sv'` | 5 |
| `reuse-after-an-edit-of-Makefile` | the same for milan_dp's recipe | `'tb/verilator/milan_dp/Makefile'` | 5 |
| `reuse-after-an-edit-of-tree:firmware` | the firmware trees' digest changed | `'tree:firmware'` | 5 |
| `clean-loaded` (clean) | none: an offer before each bind (echo skipped before the ANNOUNCE), one at each of MAAP's four arms (the last past the end), 70 unrelated frames after the ANNOUNCE, one more offer whose echo is found | (pass; load reported exactly: MAAP 4 queued, 3 delivered, 3 met) | 3, 4 |
| `bind-without-its-probe-tx` | the first bind causes no PROBE_TX, the second's follows | `the BIND_RX acmp-bind-0 caused no PROBE_TX after its response and before the next bind` | 1 |
| `probe-tx-transactions-not-the-draws` | the same log: one PROBE_TX for two binds | `ACMP: 1 PROBE_TX transactions graded (1 sent), the run asked for 2 draws` | 1 |
| `bind-refused` | the first BIND_RX_RESPONSE at status 1 | `the BIND_RX_RESPONSE to acmp-bind-0 (sequence_id 0x4100) carries status 1, not SUCCESS` | 1 |
| `aem-refused` | the first AEM response at status 2 | `aecp-read_descriptor_entity-0 (sequence_id 0x6100) carries status 2, not the 0 its scenario states` | 2 |
| `mvu-refused` | the first draw's MVU GET_MILAN_INFO answered at status 1 | `aecp-mvu_get_milan_info-0 (sequence_id 0x6100) carries status 1, not the 0 its scenario states` | 2 |
| `no-advertise-period` | the 37 s log with no advertising after the startup ENTITY_AVAILABLE | `adp.advertise_period: no sample in a run to its second ANNOUNCE` | 1 |
| `stopped-advertising` | advertising stops after the second period | `the entity stopped advertising` | 1 |
| `echo-skipped-after-the-announce` | the loaded log's last offer with its echo skipped, as a filled history leaves it | `LOAD: 1 echoes of load aecp skipped on interface 0 at cycle 175000000, after its first ANNOUNCE left` | 3 |
| `received-frame-unaccounted` | one of that offer's frames received untagged | `LOAD: 14 delivered load frames and 4 a draw (2 draws) are not the 23 frames the model received` | 4 |

The 33 round 2 controls still pass by their own words (`late-response`'s first word is now the missing PROBE_TX, since its 200 ms answer lands after the next bind; its own words, `acmp.bind_rx: 200.0 ms is not under 200.0 ms`, are still found). The plants on every run's own log are unchanged.

## Reviewer probes at the fixed head (`267fc9815d`)

The reviewers' own scripts (sha256 in `receipts/probes/reviewer-scripts.sha256`), unchanged, on the head's fresh logs (the CI step's 1x1 runs, the 8x8 runs) and on a disposable clone for the edit probes. `receipts/probes/`:

| Probe | Result |
|---|---|
| R816 `grader_probes.py` R0 | 1x1 and 8x8 unloaded: 0 findings; results identical to the head's `results.json` |
| R816 R1 (draw 5's PROBE_TX never sent, nor answered) | 2 findings: `ACMP: the BIND_RX acmp-bind-5 caused no PROBE_TX after its response and before the next bind`, `ACMP: 15 PROBE_TX transactions graded (15 sent), the run asked for 16 draws` |
| R816 R2 (only the last of 16 sent) | 16 findings: binds 0 to 14 each `caused no PROBE_TX ...`, and the count |
| R816 R3 (control, none sent) | 18 findings |
| R816 R4 (first BIND_RX_RESPONSE at status 1) | `carries status 1, not SUCCESS (IEEE 1722.1-2021 Table 8-3)` |
| R816 R5 (first AECP response at status 1) | `carries status 1, not the 0 its scenario states` |
| R815 `probe_missing_probe_tx.py`, 1x1 k=0, 1x1 k=3, 8x8 k=3 | `VERDICT: caught` each, the same two words |
| R815 `probe_no_advertise.py` | control 0 findings; no periodic advertising: 2 findings, `no sample in a run to its second ANNOUNCE` and `the entity stopped advertising` |
| R815 `probe_reuse_stale.py` | 6 of 6 refused: `tb_split_top.sv`, `KL_mbx.sv`, `KL_ctrl_split.sv`, `KL_mbx_wb.sv` by name, `maap_mbx.c` by `tree:firmware`, `milan_dp/Makefile` by its source list no longer reading (the probe's `// probe` line is not make syntax); tree restored |
| R816 `reuse_probe.py` | unchanged: accepted; `wire_main.cpp`, `tb_split_top.sv`, `KL_mbx.sv`, `milan_datapath.sv` refused by name, `third_party/tsn-c-stack/src/maap.c` and `maap_mbx.c` by `tree:firmware` |
| R816 `status_census.py`, the four head runs | every ACMP and AECP response status 0 |
| R816 `aecp_status.py`, 1x1 unloaded | `0x0027` on `(9, 0)`, status 0, 3 of 3 |

## Measurements

### The head's runs (16 draws, seed 0), at `267fc9815d`

The CI step from a clean clone on CPUs 120-123 (`receipts/head/ci-head.console`: self-test `49 controls, 0 failed`, build ready after 85 s, `PASS, wall 693 s`); the 8x8/2if build and both runs on CPUs 116-119 (`receipts/head/8x8-*.console`, 707 s and 661 s). Every run `0 finding(s)`, both plants caught. Results, tables, stimulus, UART per run in `receipts/head/`; the loaded logs by sha256 and size in `receipts/head/large.sha256`.

| Path (N: min / mean / max ms) | bound ms | 1x1 none | 1x1 composed | 8x8/2if none | 8x8/2if composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 16: 0.396 / 0.673 / 0.966 | 16: 0.728 / 1.339 / 3.423 | 16: 0.401 / 0.920 / 1.727 | 16: 0.758 / 11.940 / 18.277 |
| `acmp.bind_to_probe_tx` | - | 16: 0.585 / 0.862 / 1.155 | 16: 0.917 / 1.528 / 3.613 | 16: 0.607 / 1.127 / 1.933 | 16: 0.965 / 12.147 / 18.483 |
| `acmp.probe_tx` | 200.0 | 16: 0.399 / 0.909 / 1.080 | 16: 0.399 / 2.946 / 5.263 | 16: 0.841 / 1.175 / 2.177 | 16: 0.841 / 1.921 / 5.763 |
| `acmp.probe_tx.entity` | - | 16: 0.177 / 0.458 / 0.839 | 16: 0.219 / 2.495 / 4.539 | 16: 0.180 / 0.725 / 1.456 | 16: 0.180 / 1.470 / 5.043 |
| `aecp.response` | 240.0 | 16: 0.964 / 1.708 / 2.264 | 16: 3.003 / 3.710 / 4.151 | 16: 1.550 / 2.234 / 3.178 | 16: 4.053 / 9.820 / 24.504 |
| `aecp.response.get_avb_info` | - | 3: 1.528 / 1.593 / 1.639 | 3: 3.296 / 3.550 / 3.746 | 3: 1.611 / 2.139 / 2.877 | 3: 8.543 / 15.044 / 24.504 |
| `maap.egress` | 11.0 | 4: 0.410 / 0.787 / 1.008 | 4: 1.147 / 1.546 / 1.972 | 4: 0.961 / 1.250 / 1.479 | 4: 1.771 / 2.036 / 2.472 |
| `maap.probe_interval` | 600.0 | 3: 513.505 / 530.413 / 559.139 | 3: 514.340 / 531.270 / 560.297 | 3: 515.482 / 539.817 / 582.696 | 3: 516.571 / 540.663 / 583.689 |
| `maap.interval_error` | 11.0 | 3: 0.139 / 0.349 / 0.505 | 3: 0.174 / 0.937 / 1.340 | 3: 0.274 / 0.484 / 0.696 | 3: 0.728 / 1.329 / 1.689 |
| `adp.egress` | 400.0 | 1: 0.838 / 0.838 / 0.838 | 1: 1.550 / 1.550 / 1.550 | 1: 0.911 / 0.911 / 0.911 | 1: 2.207 / 2.207 / 2.207 |
| `egress.acmp.first` | - | 48: 0.36 / 0.37 / 0.37 us | 240: 0.36 / 0.36 / 0.37 us | 48: 0.36 / 0.36 / 0.37 us | 240: 0.36 / 0.37 / 0.37 us |
| `egress.maap.first` | - | 5: 0.36 / 0.37 / 0.37 us | 12: 0.36 / 0.37 / 0.37 us | 5: 0.36 / 0.37 / 0.37 us | 9: 0.36 / 0.36 / 0.37 us |

| Run | findings | censored | simulated ms | ready ms | load queued: offers (by an arm) / frames / echoes skipped | delivered: offers whole (in part) / frames | expiries met |
|---|---:|---|---:|---:|---|---|---|
| 1x1 none | 0 | none | 1935 | 49.102 | none | none | - |
| 1x1 composed | 0 | none | 1935 | 49.102 | acmp 16 (0) / 896 / 112, adp 2 (2) / 64 / 14, aecp 16 (0) / 839 / 105, maap 5 (5) / 200 / 0 | acmp 16 (0) / 896, adp 1 (0) / 32, aecp 16 (0) / 839, maap 3 (0) / 120 | adp 1, maap 3 |
| 8x8/2if none | 0 | none | 2001 | 115.271 | none | none | - |
| 8x8/2if composed | 0 | none | 2001 | 115.271 | acmp 16 (0) / 896 / 112, adp 2 (2) / 64 / 14, aecp 16 (0) / 839 / 105, maap 5 (5) / 200 / 0 | acmp 16 (0) / 896, adp 1 (0) / 32, aecp 16 (0) / 839, maap 3 (0) / 120 | adp 1, maap 3 |

1x1 none: delivered 0 + 4 x 16 = 64; rx_frames 64 + bench_rx 0 = 64
1x1 composed: delivered 1887 + 4 x 16 = 1951; rx_frames 1951 + bench_rx 0 = 1951
8x8/2if none: delivered 0 + 4 x 16 = 64; rx_frames 64 + bench_rx 0 = 64
8x8/2if composed: delivered 1887 + 4 x 16 = 1951; rx_frames 1104 + bench_rx 847 = 1951

### The campaign, at `267fc9815d`, restarted 2026-11-11T08:55:57Z after the reset

Four units on the 1x1 build, side by side; each rc 0, `0 finding(s)`, nothing censored, both plants caught. Wall times 8,834, 9,253, 9,975 and 9,406 s (3.9, 3.75, 3.5 and 3.7 ms of simulated time a second; unit 2 shared its first 30 minutes with another lane's sweep, see the timeline). Receipts `receipts/campaign/` (per unit: results, run parameters, table, UART, status, rc, start, end, CPUs, console, unit script; the logs and stimuli over 200 KB in `logs.sha256`; `tables.md`, `summary.txt`, `echoes.txt`, `status-census.log`).

| Path (N: min / mean / max ms) | bound ms | unit 0, seed 1, none | unit 1, seed 2, none | unit 2, seed 3, composed | unit 3, seed 4, composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 342: 0.358 / 0.734 / 2.694 | 342: 0.355 / 0.733 / 2.650 | 342: 0.389 / 1.288 / 5.024 | 342: 0.384 / 1.296 / 6.728 |
| `acmp.bind_to_probe_tx` | - | 342: 0.548 / 0.923 / 2.883 | 342: 0.545 / 0.923 / 2.839 | 342: 0.579 / 1.477 / 5.213 | 342: 0.573 / 1.485 / 6.918 |
| `acmp.probe_tx` | 200.0 | 342: 0.399 / 1.045 / 4.487 | 342: 0.399 / 1.167 / 4.490 | 342: 0.399 / 2.959 / 5.593 | 342: 0.399 / 3.039 / 5.591 |
| `acmp.probe_tx.entity` | - | 342: 0.166 / 0.570 / 3.528 | 342: 0.171 / 0.643 / 3.534 | 342: 0.163 / 2.462 / 5.298 | 342: 0.164 / 2.546 / 5.245 |
| `aecp.response` | 240.0 | 342: 0.834 / 1.756 / 3.902 | 342: 0.834 / 1.709 / 3.550 | 342: 2.202 / 3.997 / 7.251 | 342: 2.328 / 4.037 / 6.882 |
| `aecp.response.get_avb_info` | - | 57: 1.353 / 1.731 / 3.716 | 57: 1.362 / 1.672 / 3.550 | 57: 2.825 / 3.964 / 6.214 | 57: 2.831 / 4.032 / 6.637 |
| `maap.egress` | 11.0 | 5: 0.323 / 0.556 / 0.856 | 5: 0.302 / 0.641 / 0.800 | 5: 0.981 / 1.639 / 2.457 | 5: 0.957 / 1.346 / 2.083 |
| `maap.probe_interval` | 600.0 | 3: 513.174 / 530.274 / 558.840 | 3: 513.086 / 530.344 / 559.099 | 3: 513.730 / 531.435 / 559.756 | 3: 513.386 / 531.094 / 560.408 |
| `maap.interval_error` | 11.0 | 4: 0.160 / 0.199 / 0.267 | 4: 0.086 / 0.209 / 0.498 | 4: 0.730 / 1.172 / 1.819 | 4: 0.021 / 0.576 / 1.408 |
| `maap.announce_interval` | 32000.0 | 1: 31957.267 / 31957.267 / 31957.267 | 1: 31956.502 / 31956.502 / 31956.502 | 1: 31958.383 / 31958.383 / 31958.383 | 1: 31957.021 / 31957.021 / 31957.021 |
| `adp.egress` | 400.0 | 6: 0.415 / 0.608 / 0.834 | 6: 0.355 / 0.494 / 0.839 | 6: 0.233 / 0.897 / 1.304 | 6: 0.281 / 1.229 / 2.637 |
| `adp.advertise_period` | 9400.0 | 5: 5362.581 / 6820.423 / 8387.053 | 5: 5363.114 / 6820.105 / 8385.816 | 5: 5362.966 / 6820.604 / 8385.438 | 5: 5364.705 / 6821.437 / 8387.356 |
| `egress.acmp.first` | - | 1026: 0.36 / 0.36 / 0.37 us | 1026: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us |
| `egress.maap.first` | - | 6: 0.36 / 0.36 / 0.37 us | 6: 0.36 / 0.36 / 0.37 us | 1656: 0.36 / 0.36 / 0.37 us | 1656: 0.36 / 0.36 / 0.37 us |

| Run | findings | censored | simulated ms | ready ms | load queued: offers (by an arm) / frames / echoes skipped | delivered: offers whole (in part) / frames | expiries met |
|---|---:|---|---:|---:|---|---|---|
| unit 0, seed 1, none | 0 | none | 34703 | 49.102 | none | none | - |
| unit 1, seed 2, none | 0 | none | 34706 | 49.102 | none | none | - |
| unit 2, seed 3, composed | 0 | none | 34705 | 49.102 | acmp 342 (0) / 21434 / 112, adp 12 (12) / 454 / 14, aecp 342 (0) / 20073 / 105, maap 6 (6) / 240 / 0 | acmp 342 (0) / 21434, adp 11 (0) / 415, aecp 342 (0) / 20073, maap 5 (0) / 200 | adp 11, maap 4 |
| unit 3, seed 4, composed | 0 | none | 34690 | 49.102 | acmp 342 (0) / 21434 / 112, adp 12 (12) / 454 / 14, aecp 342 (0) / 20073 / 105, maap 6 (6) / 240 / 0 | acmp 342 (0) / 21434, adp 11 (0) / 415, aecp 342 (0) / 20073, maap 5 (0) / 200 | adp 11, maap 4 |

unit 0, seed 1, none: delivered 0 + 4 x 342 = 1368; rx_frames 1368 + bench_rx 0 = 1368
  adp.advertise_period: margin 1012.947 ms to 9400.0, strict margin 612.947 ms to 9000.0
unit 1, seed 2, none: delivered 0 + 4 x 342 = 1368; rx_frames 1368 + bench_rx 0 = 1368
  adp.advertise_period: margin 1014.1839 ms to 9400.0, strict margin 614.1839 ms to 9000.0
unit 2, seed 3, composed: delivered 42122 + 4 x 342 = 43490; rx_frames 43490 + bench_rx 0 = 43490
  adp.advertise_period: margin 1014.5621 ms to 9400.0, strict margin 614.5621 ms to 9000.0
unit 3, seed 4, composed: delivered 42122 + 4 x 342 = 43490; rx_frames 43490 + bench_rx 0 = 43490
  adp.advertise_period: margin 1012.6435 ms to 9400.0, strict margin 612.6435 ms to 9000.0

- Announce intervals 31,956.5 to 31,958.4 ms (41.6 ms or more below 32 s); probe intervals 513.1 to 560.4 ms; every interval within 1.82 ms of its draw; MAAP egress at most 2.46 ms over 20 timer-driven frames.
- Advertise periods 5,362.6 to 8,387.4 ms: 1,012.6 ms inside the graded 9,400 ms and 612.6 ms inside the strict 9,000 ms (SUG-1); ADP egress at most 2.64 ms.
- The slowest transaction over 1,368 draws: AEM 7.25 ms (unit 2, READ_DESCRIPTOR), ACMP 6.73 ms (unit 3, a bind). GET_AVB_INFO 1.35 to 6.64 ms, 228 of 228 SUCCESS.
- Every ACMP and AECP frame the entity sent carries status 0 in all four units (R816's `status_census.py`).
- The echoes (ruling 3): in each loaded unit, 38 offers before the first ANNOUNCE skipped 231 echoes; the 664 offers after it (663 with echoes) found 4,641 and skipped none (round 2's units delivered 49 of 4,788). The entity sent 1,650 DEFENDs, 4 PROBEs and 2 ANNOUNCEs on the MAAP channel (`echoes.txt`): about five DEFENDs a draw after the first ANNOUNCE, so a window of that channel, the CPU budget harness's 32 frames, would have lost the ANNOUNCE within about seven draws; each echo therefore keeps its own newest match.
- The load (ruling 4): a loaded unit queues 6 MAAP and 12 ADP deadline bursts; 5 and 11 are delivered, 4 and 11 meet an expiry (the cancelled 2,210 ms probe deadline's burst is delivered and meets none; the 64,083 ms announce deadline and the last advertise timer fall past the log). Delivered load frames 42,122 + 4 x 342 = 43,490 = `rx_frames` + `bench_rx`, in each loaded unit; 1,368 in each unloaded one.

### What the head keeps

`git diff --stat 267fc9815d e3f96a67b5` (`receipts/diff-since-measurement.txt`): the `wire-timing` job's template and generated workflow, `scripts/ci_events.py`, `docs/testing/CI_WORKFLOWS.md`, and three READMEs; nothing the model, the build, the stimulus or the grader reads but the MAAP page, which lies inside a firmware tree the reuse guard digests whole, so the guard would refuse the campaign's build at the head for that README edit alone (by design: it refuses on any change in those trees). Every run's stimulus regenerates byte-identical at `e3f96a67b5` (`receipts/stimulus-at-head.txt`).

## Gate table

One clean-clone pass at `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53`, 12:46-16:46 local, each workflow job on its own fresh clone (`gates/run_wf.py`, `run_docs_yml.py`), verified by `gates/verify_wf.py` and `verify_docs_yml.py` from the workflow at the head, so a step missing from a table is a red. One build per point in the pass, at that head. CPUs as the timeline states. Receipts: `receipts/gates/` (runner scripts, the four tables, `jobs.txt`, every step log and rc under 200 KB, larger logs by sha256 and size in `large.sha256`), `receipts/sweep/` (each shard's spec, results, completion, summary, suite and preflight logs, unit end). No step of the pass has an rc other than 0 (138 rc files).

| Gate | Command / runner | Result | Receipt |
|---|---|---|---|
| `rtl-fast.yml`, 18 jobs, every `run:` step | `run_wf.py rtl-fast` per job (LiteX venv for `firmware-boundary`, `wire-timing`) | 56 steps rc 0, 65 not run with a stated reason (round 2's 64 and the new install step, which the LiteX venv on PATH carries at its revisions; the step's own command ran in the replica), 0 bad | `gates/rtl-fast-table.md` |
| `rtl-fast / wire-timing` (item 5) | step `python3 tb/verilator/ctrl_wire_timing/run.py --ci` | rc 0, `49 controls, 0 failed`, both runs `0 finding(s)`, both plants caught per run, `PASS, wall 2505 s` (build 626 s) on 4 session-pool CPUs at host load about 110; results, logs, stimulus and UART byte-identical to the head measurement | `gates/rtl-fast/logs/rtl-fast__wire-timing__ci_step_21.log`, `gates/wire-timing-ci-vs-head.txt` |
| firmware self-test | `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4` in `firmware-unit`, `-control-mutants`, `-aecp-mutants`, `-srp-mutants` | rc 0 each, `test_ctrl_firmware: PASS`; control shard `mutants: 570 of 570 caught` | `gates/rtl-fast/logs/*firmware-*__ci_step_9.log`, `*firmware-unit__ci_step_10.log` |
| coverage ratchet | `fw_coverage.py --selftest`, `--check` (`firmware-unit` step 12) | rc 0, `firmware coverage: PASS (35 files)` | `gates/rtl-fast/logs/rtl-fast__firmware-unit__ci_step_12.log` |
| behave | `cd tests && behave` (`bdd-conformance` step 5) | rc 0, 14 features, 508 scenarios, 2330 steps passed, 0 failed | `gates/rtl-fast/logs/rtl-fast__bdd-conformance__ci_step_5.log` |
| `docs.yml`, 9 jobs, every `run:` step | `run_docs_yml.py` per job | 64 steps rc 0, 31 not run with a stated reason, 0 bad (a first start stopped before any clone, the runner's skip list missing; `gates/docs-runner-error/`) | `gates/docs-yml-table.md` |
| `elaborate.yml`, 6 jobs, every `run:` step | `run_wf.py elaborate` per job | 13 steps rc 0, 33 not run with a reason, 0 bad; `elaborate-gates-1` gate_19 (the LiteX aggregate) `simulations: 8 passed: 8`, `test_soc_timing_cuts` inside its wall clock (uncontended 64-67) | `gates/elaborate-table.md`, `gates/elaborate/logs/*gate_19*` |
| `rtl.yml` `full-ci-gate` | `run_wf.py rtl full-ci-gate` (ACT=true) | rc 0 | `gates/rtl-table.md` (4 steps rc 0, 86 not run with a reason, 0 bad) |
| `rtl.yml` `yosys-shards` 0-3 | `syn/yosys/run.sh --shard k/4` | rc 0 each, `RESULT: PASS` (shard 0 also `TAP-PURITY RESULT: PASS`); tree clean after | `gates/rtl/logs/rtl-yosys-shard-*.log` |
| `rtl.yml` `verilator-shards`: the full sweep | four shard units, `MAKEFLAGS=-j4 --no-print-directory`; shard 2 (`capture_coherence`) on 48-51 from 13:12 alone (MemAvailable under 30 GB), shards 0, 1, 3 on 80-83, 84-87, 88-91 from 13:22 (34 GB) | shard 0: 15/15, 360,992 checks, rc 0, 5,308 s; shard 1: 17/17, 1,526,104 checks, rc 0, 4,867 s; shard 2: 17/17, 284,228 checks, rc 0, 5,663 s (`capture_coherence` inside its wall clock); shard 3: 16/16, 21,575 checks, rc 0, 4,033 s. 65 of 65 suites, 2,192,899 checks, 0 failures; preflight (`test_suite_cancellation.py` included) PASS in all four | `sweep/shard-k/spec-01.log`, `results.json`, `complete.json`, `logs/` |
| `rtl.yml` `physical-gptp` | not triggered by a pull request (its `if:` needs a schedule or dispatch event) | not run, recorded in `not_run_rtl.json` | `gates/not_run_rtl.json` |
| `git diff --check` against the merge base `1d6bf5556a` | `extra.sh` | rc 0 | `gates/extra/logs/diff-check.log` |
| tally mutants | `sw/firmware/gtest/tally_selftest.py --mutants` | rc 0, `listener defects: 18 of 18 caught` | `gates/extra/logs/tally-mutants.log` |
| saved-state self-test | `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | rc 0, 5 shapes, 435 tests, 109 of 109 planted defects | `gates/extra/logs/nvm-self-test.log` |
| `test_builder.py --require-rv32` | LiteX venv | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN`: gate 1b's `MAKEFLAGS += -e` mutant has no effect on this make, gate 11 needs a placed Vivado report (no route in this lane) | `gates/extra/logs/test-builder.log` |
| S2's harness, self-test | `ctrl_service_budget/run.py --self-test` | rc 0, `self-test: 0 failures` | `gates/extra/logs/budget-self-test.log` |
| S2's harness at 1x1/1if | `run.py --point 1x1 --record-budget-findings` | rc 0, `18 groups graded, 0 refusals` (34 recorded T_svc misses: S2b's, as in round 2) | `gates/extra/logs/budget-1x1.log` |
| S2's harness at 8x8/2if | `run.py --point 8x8 --record-budget-findings` | rc 0, `17 groups graded, 0 refusals` (63 recorded T_svc misses, S2b's) | `gates/extra/logs/budget-8x8.log` |
| wire timing at 8x8/2if, no load and composed | `ctrl_wire_timing/run.py --point 8x8 --draws 16 --load none`, then `--reuse-build --load composed` | rc 0 each, `0 finding(s)`, both plants caught; results, logs, stimulus and UART byte-identical to the head measurement | `gates/extra/logs/wire-8x8-*.log`, `gates/wire-8x8-vs-head.txt` |

Beside the pass (not gates of the bar):

| Check | Result | Receipt |
|---|---|---|
| the `wire-timing` job replicated as a fresh runner does it, at `fbe5acc983` | every setup step rc 0; the step `PASS, wall 1299 s`, build 323 s with the CPU netlist generated cold; byte-identical to the head's bench-venv runs | `receipts/replica/` |
| the reviewers' probes at `267fc9815d` | every one found or refused by its own words (above) | `receipts/probes/` |
| the stimulus at the final head | every run's regenerates byte-identical | `receipts/stimulus-at-head.txt` |

### Remaining risks

- Item 5's hosted wall time: the step took 1,299 s in the replica (4 CPUs, load about 120, cold CPU generation) and 2,505 s in the gate pass (4 contended session-pool CPUs); round 2's hosted job never reached the step. The first hosted run of this head settles it against the 30-minute timeout.
- The CPU budget harness's GET_AVB_INFO row sends 0x0028 the same way (`tb/verilator/ctrl_service_budget/scenario.py:464`); ruling item 2 puts it outside this lane, and it needs its own Issue (the manager's).
- The issue body is not edited here: if it quotes round 2's 20.6 ms AEM figure, that was a GET_AS_PATH refusal; the corrected figures are in the PR body and the harness page.
- `dev-soft-core` moved on the remote during the round, to `764482b45f`; the lane's merge base is still `1d6bf555` (no rebase in this lane), so the candidate merge against the live base is the manager's.
- The reuse guard digests the firmware trees whole, so any edit in them, a README included, refuses a reuse: conservative by design, and a rebuild is the remedy.
