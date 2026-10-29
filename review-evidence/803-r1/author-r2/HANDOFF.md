# HANDOFF — #803 round 2 (PR #805), executor [A693b]

Status: **REVIEW READY** at `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31` (worktree clean, every submodule at its
gitlink, live remote dev `5fcec84b` unchanged). Base head `fb182b19925b9ea24443d48d0e71b656de52b8ae` (round 1,
[A693]); six commits on top; nothing pushed. Every gate the round-2 delta reaches is rc 0 at the final head, the full
sweep included (gate table). STOP conditions not met (section STOP). The slice headroom stays an owner decision.

- Lane: $LANES/803-adopt-gptp, branch 803-adopt-gptp-f97c1803 (PR #805), from dev 5fcec84b
- origin: https://github.com/kebag-logic/milan-fpga.git (verified); protocol-processor toplevel and origin
  (https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git) verified before reading it; no git
  command ran inside the lane's gptp-processor. The mutant runner restores engine files with `git -C <clone>/gptp-processor`
  in scratch clones; each clone's gptp-processor is its own toplevel, origin the lane's checkout, at f97c1803 and clean
  after the streams (`receipts/mutants/clone-integrity.txt`)
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/803#issuecomment-6483237783
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/803#issuecomment-6485793112
- Assignment: the [A10] round 2 ruling on #803; reviews R727-1 and R728-1 on PR #805

## Commits (all one-line, no body, no trailer)

| # | Commit | Item | Change |
|---|---|---|---|
| 9 | `63a8e123` | F1 | GET_AS_PATH in-flight cut: the response is held at its count beat while the empty path commits; ordering check; entry-1 check |
| 10 | `40896b8a` | S1 | #207 full-queue window: pop-free behind a held Pdelay_Req at the queue head; both pointers graded unmoved; level restored |
| 11 | `a5a4af26` | F2, R1 | pin page and changelog: true scope; "meets timing at +0.333 ns WNS" |
| 12 | `acbbe973` | 6 | AREA_BUDGET.md:140: 7 of 15,850 slices free at the f97c1803 route; :141 (owner decision) kept verbatim |
| 13 | `d6404184` | 5 | physical suite deadline 5400 -> 6900 s, its nightly/manual job 120 -> 145 min, through the template and generator |
| 14 | `2b1565fd` | S1 | the #207 arm's pointer copies one name per declaration (ES.10; the idiom gate's regex misses `const unsigned a = x, b = y;`) |

Final head: `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31`.

No synthesis or firmware input changes: `git diff fb182b19..2b1565fd -- hdl sw configs syn avdecc features
gptp-processor protocol-processor third_party` is empty (`receipts/scope/round2-delta-scope.txt`), so round 1's Vivado
(route-1x1, ooc-1x1, ooc-8x8), Yosys 60/60, lint, xvlog and the pin-record gates stand for this head unchanged. No RTL
file is touched, the comment beside `asp_resp_entry_w` included: the harness now makes it true as written.

## Item 1 — F1: the GET_AS_PATH first-count snapshot has a check (Tests, Robustness)

Clause: IEEE 1722.1-2021 7.4.41.2 pairs `count` with `path_sequence` ("The count field is set to the number of ClockIdentities present in the path_sequence field"); `docs/reference/REGISTER_MAP.md:333` ("The
response snapshots the canonical selected path before gathering entries, so it stays on one coherent generation").

Why it survived: the processor gathers every entry about 13 cycles after the first-count capture (R728-1's probe),
while the cut's publication commits about 460 cycles after the Announce, so the gather had finished before the path
changed and a live read and the snapshot gave the same answer.

| file:line (head) | Change |
|---|---|
| `tb/verilator/milan_dp/sim_gptp.cpp:351` | `hold_gsi_beat`: while set, every clock clears the info server's first match stage (`gsi_srv1_r`), so the processor HOLDs its presented GSI beat inside its bounded gather wait (`MEM_TIMEOUT_CYC_P` 4096 cycles; `KL_aecp_engine.sv:2445-2456`), and resumes when cleared |
| `sim_gptp.cpp:353, 426-428` | `asp_entry_cyc`: the last cycle `asp_resp_entry_w` (a path-entry request) was presented, recorded on every clock independent of the hold |
| `sim_gptp.cpp:1424-1430` | arm comment now states what the arm proves (replaces "These checks kill torn-response mutations") |
| `sim_gptp.cpp:1474-1497` | after the first-count capture, hold the count beat, send the empty-TLV Announce, wait (at most 3000 cycles) for the commit, release; print `[cut]`; new check `empty path commits after first-count snapshot, before entry gather` (commit seen and no path-entry request since the capture). Replaces `empty path commits before captured old response leaves wire`; the MAC hold it relied on is removed |
| `sim_gptp.cpp:1504-1505` | new check `in-flight response remains wholly old: ends with thisClock` (entry 1 at offset 50) beside the existing count-two and entry-0 checks |

Measured at the head: `[cut] count beat held 474 cycles; commit seen 1; path-entry request before the commit 0`
(well inside 4096). The RTL comment at `hdl/milan/milan_datapath.sv:6032-6035` ("Its in-flight cut must complete
PUBLISH after the count snapshot but before the first path-entry request") is now true as written and asserted.

## Item 2 — F2 and item 3 — R1 (Docs)

| file:line | Now reads |
|---|---|
| `docs/reference/SUBMODULES.md:310-314` | No top-level port, parameter or register changes. / `KL_gptp_shadow.pub_path_o` widens with the engine's: eight entries from entry 0. / Its test wrapper `gptp_shadow_wrap` adds `pub_path_head_o`. |
| `CHANGELOG.md:72-75` | the same three statements as list items (concise-style limits) |
| `docs/reference/SUBMODULES.md:334` | Its shipping route meets timing at +0.333 ns WNS. |

## Item 4 — S1: the #207 full-queue arm leaves the engine as it found it (Tests)

Why: forcing `evq_lvl_r` to 4 makes every slot look live; with the real queue empty, dispatch popped stale entries
inside the window (R727-1: `rp 0->3, wp 0->0`) and the `(wp-rp)&3` restore left level 1, a phantom entry.

| file:line (head) | Change |
|---|---|
| `sim_gptp.cpp:1667-1677` | comment: why no pop can happen and what is graded |
| `sim_gptp.cpp:1679-1694` | wait for s1's response claim (`resp_claim_valid_r`) with its Pdelay_Resp held at the MAC, then send s1b, a second real Pdelay_Req, which waits at the queue head (`pdreq_block_w`, `KL_gptp_engine.sv:542-544`): dispatch cannot pop, stale or not |
| `sim_gptp.cpp:1695-1711` | record level and both pointers before the window, read both after, restore the level to its own value, print `[#207]` |
| `sim_gptp.cpp:1719-1720` | new check `the full-queue window pops and pushes no event` (both pointers equal before and after) |

Measured at the head: `[#207] full-queue window: level 1, rp 1->1, wp 2->2` (no pop, no push; s1b runs as a real
event after the MAC is released). Control H2 (s1b not sent) prints `level 0, rp 1->0, wp 1->1` (three stale pops) and
fails the pointer check, and **seven checks of the later #88 arm then fail as well**
(`#88 path headed elsewhere serves count three` and six more): the stale-event hazard S1 named does decide later arms.

## Item 5 — the physical leg's deadline

Re-projection at the head by the README's method (`receipts/projection/projection.txt`, from `scripts/projection.py`):
the round-2 delta changes no input of the physical leg (`sim_ax1x1gptp.cpp`, the RTL, the microcode, configs and the
recipe are unchanged; `sim_gptp.cpp` is not compiled into `obj_ax1x1gptp`), so the scenario is still 899,637,137
cycles (round 1's receipt; this round's physical run at the head measured 899,637,137 again).

| Quantity | Value |
|---|---|
| Hosted projection, the two README branches | 5,346.8 s and 5,484.0 s |
| Against the 5,400 s suite deadline | 99.0 % and 101.6 % (above 80 %) |
| Deadline for a worst case at most 80 % | at least 6,855 s; **6,900 s** (115 min, the next whole 5 min): 77.5 % and 79.5 % |
| The job (keeps its 30 min for setup and upload) | 120 -> **145 min**; margin 53.6 to 55.9 min, worst case 63.0 % |

Both timeouts belong to the nightly/manual `physical-gptp` job only (the 5,400 s is its suite's deadline in
`scripts/run_all_suites.sh`, the 120 min its `timeout-minutes`); raising only the latter would leave the 101.6 % against
the former, and raising only the former would leave 5 min for the job's setup. No PR-gating job or other timeout
changes: the generated workflow diff is the one line `.github/workflows/rtl.yml:418`.

| file:line | Change |
|---|---|
| `scripts/run_all_suites.sh:41, 252-254, 259` | header default, the #803 reason, `milan_dp_gptp ... ${SUITE_TIMEOUT:-6900}` |
| `.github/ci-templates/rtl.yml:321` -> `.github/workflows/rtl.yml:418` | `timeout-minutes: 145`, through `python3 scripts/ci_gate_workflows.py` (`--check` rc 0) |
| `scripts/ci_events.py:178, 2008` | the pinned physical job contract (145) and its policy tokens (`6900`, `145`); its mutation arms still change the budget (180) and the suite env (7200) |
| `scripts/measure_test_evidence.py:673, 680`; `measure_test_evidence_selftest.py:297` | the pinned budget table and its message; the self-test's budget mutation from the new value |
| `docs/testing/CI_WORKFLOWS.md:537, 656-661`; `RUNNING_TESTS.md:88`; `TESTING.md:172-173`; `tb/verilator/milan_dp/README.md:354-355, 429-435`; `tb/verilator/milan_dp_gptp/README.md:26-27` | the deadline and job time; the README records the projection and the new percentages |
| `CHANGELOG.md:79-80`; `docs/reference/SUBMODULES.md:322-324` | the adoption record notes both raises |

Not touched: `ci/image/tool-inventory.json` records digests of these scripts, but it is refreshed by its own image
lane (earlier budget changes, e.g. `6f7b70ed`, left it alone) and no workflow checks it.

## Item 6 — slice headroom figures

`docs/design/AREA_BUDGET.md:140` now reads: "The slice row is the binding limit: the shipping route at FPGA-gPTP
`f97c1803` (#803) places 15,843 slices, so placement has 7 of 15,850 left." Line 141 ("The next growth on the
shipping image therefore has no slice room and needs its own owner decision") is unchanged. Not ruled here; the table
above it remains the gate's committed record.

## New checks, their planted defects and the words they fail with

Runner: `scripts/round2_mutants.py` (round 1's `parent_mutants.py` plus the round-2 rows): one defect at a time in a
clean clone at the head, a fresh build, the file restored after; a clean pass first in the same clone prints no FAIL.
Two streams at `2b1565fd` (A: the round-2 rows; B: round 1's milan_dp rows), one stream at `fb182b19` (C: the
reviewers' two probes before the fix). Table with every printed line: `receipts/mutants/mutant-table-head.md`,
`mutant-table-fb182b19.md`; per-stream verdicts, log digests and the printed lines in `receipts/mutants/<stream>/`.

| Defect (planted) | File | At `fb182b19` | At `2b1565fd`, gptp and gptp-lat legs: the FAIL line |
|---|---|---|---|
| clean | - | 200 checks: 200 PASS, 0 FAIL | 202 checks: 202 PASS, 0 FAIL (both legs; and in stream B) |
| M9 entry 0 from `asp_live_head_w` (R727-1 `probe-m9.diff`) | `milan_datapath.sv:6305` | survives, 200/200 | `FAIL in-flight response remains wholly old GM got 02a1b2fffec3d4e5 exp 00aaccfffe010204` |
| M9b entries 1..7 from `asp_live_path_w` (`probe-m9b.diff`) | `milan_datapath.sv:6309` | survives, 200/200 | `FAIL in-flight response remains wholly old: ends with thisClock got 0000000000000000 exp 02a1b2fffec3d4e5` |
| M9c count from `asp_live_count_w` | `milan_datapath.sv:6300` | - | `FAIL in-flight response remains wholly old count two got 0000000000000001 exp 0000000000000002` (and the entry-1 check) |
| H1 harness: no count-beat hold | `sim_gptp.cpp:1482` | - | `FAIL empty path commits after first-count snapshot, before entry gather got 0000000000000000 exp 0000000000000001` (`[cut] ... path-entry request before the commit 1`) |
| H2 harness: s1b not sent | `sim_gptp.cpp:1692` | - | `FAIL the full-queue window pops and pushes no event got 0000000000000000 exp 0000000000000001` (`[#207] ... level 0, rp 1->0, wp 1->1`), plus 7 #88-arm FAILs |

Round 1's milan_dp rows re-run at the head (stream B), every named check FAIL: P1, P2, P3, P4, P5, P6 (the #207 arm's
own control, `a full queue moves only the event count`), D1, D2, D3, D4, D6: 11 of 11 KILLED. Total at the head:
19 (defect, leg) rows, 19 KILLED; 3 clean passes, 0 FAIL.

Clean-leg count: 200 -> 202 (one check replaced, two added: the entry-1 check and the pointer check). The ruling's
"the clean leg stays 200/200" is read as "every clean check passes"; the two added checks are the ones the ruling asks
for.

## Gate table (final head `2b1565fd` unless noted; every command unpiped, its own rc and log)

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| milan_dp `gptp` leg, clean (streams A and B) | 0, 0 | 202 checks: 202 PASS, 0 FAIL | `receipts/mutants/A`, `B` |
| milan_dp `gptp-lat` leg, clean (stream A) | 0 | 202 checks: 202 PASS, 0 FAIL | `receipts/mutants/A` |
| Mutant streams A, B (`round2_mutants.py`) | 0, 0 | 19 / 19 KILLED, 3 CLEAN | `receipts/mutants/` |
| Stream C at `fb182b19` (reproduction) | 1 (expected) | M9, M9b ESCAPED at the reviewed head | `receipts/mutants/C-fb182b19` |
| Docs workflow replica (`docs_steps.py`: the run: bodies literally, GNU Make 4.3, CPython 3.12.3) | 0 | 44 steps, 0 failed: 42 run, 2 skipped by rule (gate_42 runs the candidate act runner on the host; the no-git job's body deletes `.git`). Includes ci_events --check and --selftest (`selftest: PASS (2199 contract items, 5258 arms)`), ci_gate_workflows --check and its self-test (`gate workflow and union controls: PASS`), measure_test_evidence --check and --selftest (105/105), the four idiom gates (cpp: `multi-declarator declaration: 0 <= 0`, `long function: 0 <= 0`), hygiene, em dash, concise style, TOC, docs_check, feature status, the builder legs | `receipts/docs/all.out`, `all-receipts.json`, `all.sha256` |
| Builder leg 1 again with the LiteX interpreter | 0 | 1 step, 0 failed; ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, the absent mf48 calibration build), as round 1 | `receipts/docs/leg1-litex*` |
| Builder leg 0 (in the replica) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 1b, inert under Make 4.3), as round 1 | `receipts/docs/docs-gates-1.gate_25_0.not-run.txt` |
| The five Markdown gates on CPython 3.12.3 | 0 | 5 steps, 0 failed | `receipts/docs/md312*` |
| No-git job's gates on a `git archive` export | 0, 0 | docs_check, feature status | `receipts/docs/nogit_*` |
| milan_dp_gptp (physical), `scripts/run_all_suites.sh <logs> --wait --physical-gptp` with SUITE_TIMEOUT unset, so its default 6900 s governs; then `suite_tally.py <logs> --quiet --expect-suite-root tb/verilator --physical-gptp` | 0, 0 | 1 / 1; **205 checks, 0 failures**: physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre 14; 17.992742740 simulated s, 899,637,137 cycles (equal to round 1's: the scenario is unchanged); simulation 4,213 s; **suite 5,391 s, 78.1 % of 6,900 s** on this loaded host, beside the sweep, the mutant streams and the docs replica | `receipts/physical/` |
| Full sweep, 4 shard units (`native-shards.py 803-a693b <spec> <out> 4 0-15 16-31 96-99 100-111`, MemoryMax 10G, -j4) | 0 x4 | shards 15/15 (250,962 checks, 4,098 s), 17/17 (1,536,446, 2,577 s), 16/16 (380,086, 5,047 s; `capture_coherence` 42/42 on four CPUs, unit peak 6.7 GB), 16/16 (23,927, 2,504 s) | `receipts/sweep/shard-*` |
| `python3 scripts/suite_tally.py <union of the four shards' logs> --quiet --expect-suite-root tb/verilator` | 0 | **64 / 64 suites, 2,191,421 checks, 0 in-suite failures, 0 timed out** (round 1: 2,191,417; +2 in each of the `gptp` and `gptp-lat` legs): `milan_dp` 13,617 over 18 tallies, `milan_dp_gm_steps` 202, `gptp_shadow` 325, `gptp_plane` 99, `tsn_fuzz` 897 | `receipts/sweep/suite-tally-quiet.out`, `suite-tally-per-suite.txt`, `union-logs.sha256` |
| rtl-fast | not re-run | no rtl-fast job reads a round-2 file, and no RTL, firmware or feature input changed (`receipts/scope/round2-delta-scope.txt`); round 1's replica (12/12 jobs, behave 495) stands | round 1 packet |
| Yosys, lint, xvlog, Vivado route-1x1 / ooc-1x1 / ooc-8x8 | not re-run | no synthesis input changed; round 1's results stand (route-1x1 +481 LUT, tolerance 500, WNS +0.333 ns) | round 1 packet |

## STOP conditions (none met)

- A top-level port, register-map or contract change: none. No RTL, register map or interface file changes; the CI
  change is the physical job's two timeouts the ruling orders.
- route-1x1 LUT beyond the record tolerance: no synthesis input changed, so route-1x1 is round 1's +481 (tolerance 500).

## Run notes

- A first pair of mutant streams ran at `40896b8a`; the ES.10 split (`2b1565fd`) moved the head, so they were stopped
  and every row was re-run at the final head. A first physical run at `d6404184` was cancelled by TERM after 5 min for
  the same reason ("CANCELLED: TERM"); the run in the table is at `2b1565fd`.
- The mutant streams and the docs replica ran at nice 10 beside the physical leg, whose wall time is graded against its
  deadline.
- Shard 2 owns `capture_coherence`, whose mutation bank runs one build per CPU of its affinity; it ran on four CPUs
  (round 1's eight-CPU shard was OOM-killed at its 10 GB cap there).
