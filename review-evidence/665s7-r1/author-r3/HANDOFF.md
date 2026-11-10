# [A757] #867 (S7 of #665), round 3: a Join timer's frame is what lwSRP did, not a time window

Status: **REVIEW READY** at head `2128daad26b932feeed1ef2bde8f2774e8a51a31`. Every gate below is rc 0 at that head, on clean clones. TAKEN: issue 867 comment 6766827070 (`TAKEN-COMMENT.md`). REVIEW READY: issue 867 comment 6778937341 (`REVIEW-READY-COMMENT.md`).

Authority:
- the round 3 ruling (PR #874 issuecomment-6766550989), items 1 to 4;
- R813-2 (issuecomment-6766539856): F-1, R-1 and R-2, with its `scripts/request_probe.py` and `receipts/request-probe.txt` on `665s7-review-evidence`;
- R814-2 (issuecomment-6766441473): R-1 to R-3;
- #867 acceptance item 3;
- `docs/reference/FR_NFR.md` 3.4.1;
- IEEE 802.1Q-2018 10.7.4.1, 10.7.11 and Table 10-7.

Lane: branch `665-s7-srp-tx`, base `dev-soft-core` `1d6bf555` (live remote tip, re-read). One commit was added on round 2's `2131eff4`, with no merge, rebase, force or amend. Nothing is pushed.

| Commit | Subject |
|---|---|
| `2128daad` | Attribute a Join timer's transmit opportunity by what lwSRP did at its boundary, grade each requested one within JoinTime of lwSRP's last idle poll, and control the peer's LeaveAll at 16280 and 16240 ms (#867) |

`git diff --stat 2131eff4 2128daad` lists seven files: `tb/verilator/milan_dp/srptx.hpp`, `twin_split.cpp`, `srptx_grade.py`, `srptx_plants.py`, `Makefile`, `README.md`, and `sw/firmware/ctrl/srp/README.md`. There is no RTL, firmware, lwSRP, adapter, loop, shape, ring, fixture or generated-file change. The licence fixture (`__wrap_srp_mbx_init`) is untouched. Item 5 stays owed.

## The exit (not triggered)

The exit asks whether lwSRP's state at the boundary can tell a timer-gated transmit from a requested one without editing lwSRP or the adapter. It can:
- each transmit arms the Join timer and sets `join_wait` (`third_party/lwSRP/src/core/mrp_mad.c:1539-1540`);
- `join_wait` holds every later transmit (`:1421`);
- the timer's expiry only clears `join_wait` (`:854`).

So lwSRP's first `mrp_transmit` after a Join expiry either sends the transmit the timer held (it returns nonzero) or finds nothing to send (it returns 0).

The bench already wraps `mrp_transmit` and `shlan_timer_tick`, and it already reads each timer's `cs` field. So it records that outcome per MRPDU with no new wrap and no edit to lwSRP or the adapter.

## Changes (file:line at `2128daad`, reason)

Item 1, attribution by what lwSRP did:
- `tb/verilator/milan_dp/srptx.hpp:176-178`: each `Lib` record (an MRPDU lwSRP handed the adapter) gains `after_join` and `idle_us`.
  - `after_join`: the participant's first transmit poll since its Join timer expired.
  - `idle_us`: with the Join timer stopped, the last poll since the participant's last transmit that sent nothing.
- `srptx.hpp:217-219`: the `Participant` keeps both between polls.
- `srptx.hpp:500-525`: `join_owner()` and `poll()`, with the reason in the comment (`mrp_mad.c` `on_join_timer`, `mrp_transmit`).
- `srptx.hpp:536-542`: `__wrap_mrp_transmit` reads the Join timer's `cs` before the call, because the call's transmit re-arms it, then marks the records the call pushed.
- `srptx.hpp:609-613`: `__wrap_shlan_timer_tick` flags the participant whose Join timer expired.
- `srptx.hpp:407-410`: the capture writes both fields.
- `srptx.hpp:15-18`: the header says what each MRPDU carries.
- `tb/verilator/milan_dp/srptx_grade.py:136-139`, `:264-265`: `Mrpdu.after_join` and `idle_us`, read from the matched record. A capture without them raises KeyError rather than grading silently.
- `srptx_grade.py:408-421` (`causes`): a frame lwSRP sent at its first poll after a Join expiry is that timer's, at the latest Join expiry before it, with no window. Periodic and LeaveAll keep their `ATTRIBUTE_MS` window. That window serves the measurement only, and no check reads it.
- `srptx_grade.py:424-428` (`join_intervals`): only frames with `after_join`, LeaveAll frames included.
- `srptx_grade.py:342-348`: the Join interval check reads `join_intervals` directly. `:444`: `measure_time` takes its JoinTime figures from the same function.
- `srptx_grade.py:349-359`: the requested-opportunity rule. Each frame sent with the Join timer stopped must leave within JoinTime + T_svc (`JOIN_FOLLOW_MS`, 220 ms) of the last poll at which lwSRP had nothing to send. Spans that touch a hold are excluded. Reason: the ruling's "a requested opportunity after an idle expiry is graded by the 'within JoinTime' rule instead", `FR_NFR.md` 3.4.1, Milan v1.2 4.2.7.1.1, IEEE 802.1Q-2018 10.7.4.1.
- `srptx_grade.py:18-26`: the docstring says which frame is a Join timer's, and states the requested rule.

Item 2, keep the refusals: there is no change to `join-early-past-t-svc`, `join-interval-late`, the controls or the arms. They still move or plant what they did, and `move()` carries each record's `after_join` with its frame.

Item 3, the control:
- `tb/verilator/milan_dp/srptx.hpp:227`, `:358`: `Recorder.peer_leave_all_ms`, default `kPeerLeaveAllMs`. The constexpr line R813-2's probe edits is unchanged at `:98`.
- `srptx.hpp:55-59`: the usage line documents the new option.
- `tb/verilator/milan_dp/twin_split.cpp:510-528`: `srptx_args()` takes `--ms` and `--peer-leave-all-ms` in any order. An unknown option falls through to the twin's usage, rc 2.
- `twin_split.cpp:470-474`: `--peer-leave-all-ms` outside `licence` is refused, rc 2.
- `twin_split.cpp:36`: usage.
- `tb/verilator/milan_dp/Makefile:998-1009`, `:1016-1019`: `make srptx` also runs `exec-srptx-off-grid-16280` and `-16240`, each graded clean. `:42-43`: the help.
- `tb/verilator/milan_dp/srptx_plants.py:114-117` (`OFF_GRID`), `:207-222` (`off_grid()`), `:355-371`. Each off-grid capture must grade clean and hold its case: the first MSRP frame after the peer's LeaveAll at its ms, not sent at a first poll after a Join expiry, and following a Join expiry that found nothing to send. Reason: so the control cannot go hollow if the stimulus drifts.
- `srptx_plants.py:9-11`: the docstring.

The new rule's plant and control (item 1's rule needs a test that fails on its plant):
- `srptx_plants.py:68-72`: `requested-late`.
- `:110`: `requested-within`.
- `:113`: `REQUESTED`.
- `:194-204` (`plant_requested()`): the record of the first MSRP frame sent with its Join timer stopped and no Join expiry in the 222 ms before it. That is `wire`'s frame at ms 1000. Its last idle poll moves 221 ms, or 219 ms for the control, before the frame. lwSRP's state allows it there: no transmit and no Join timer in that span.
- `:241-242`: the dispatch.

Item 4, residue:
- R813-2 R-2: `srptx_grade.py:97-98`. `ATTRIBUTE_MS` serves the periodic and LeaveAll measurement only. A Join timer's frame is the one sent at the first poll after the expiry.
- R814-2 R-2: `srptx_grade.py:20-22`, the docstring:
  - "each transmit opportunity a Join timer sends within JoinTime's range (180 to 240 ms) of the one before, widened by T_svc on each side (160 to 260 ms; 10.7.4.1, 10.7.11)";
  - and "no four in 1.5 x JoinTime less T_svc".
- R814-2 R-2: `srptx_grade.py:342-343`, the comment: "each transmit opportunity a Join timer sent, against the one before it".
- R814-2 R-3: `tb/verilator/milan_dp/README.md:1557`, the `[TIME]` row: "No four transmit opportunities in 1.5 x JoinTime less T_svc (280 ms)".
- R813-2 R-1, R814-2 R-1: `PR-BODY.md` `## Status` no longer reads as stopped. The option (a) outcome is stated with #810 and #495.

Documentation:
- `tb/verilator/milan_dp/README.md`:
  - `:111`: the contents line;
  - `:1490-1491`: the scenarios;
  - `:1503-1505`: what each MRPDU carries;
  - `:1539`: the off-grid row;
  - `:1557`: `[TIME]`, with the Join timer's frame and the requested rule, citing Milan v1.2 4.2.7.1.1 and FR_NFR 3.4.1;
  - `:1563-1586`: why the attribution is what lwSRP did, the off-grid case, and the two time windows the ablation shows would refuse;
  - `:1582-1585`: the requested rule's limit;
  - `:1599`, `:1606`: what it finds, with the off-grid row;
  - `:1617-1627`: the figures and what N counts;
  - `:1633-1637`: the interval range across all five runs;
  - `:1670`, `:1696-1702`: the plant, the control and the off-grid check.
- `sw/firmware/ctrl/srp/README.md:384-385`: each requested transmit opportunity within JoinTime and T_svc.

## Checks, planted mutants and failing words

| Check | Plant or mutant | Refused by | Without the change |
|---|---|---|---|
| `[TIME]` requested opportunity (new) | `requested-late`: `wire`'s MSRP frame at ms 1000, its last idle poll 221 ms before it | `a requested transmit opportunity at ms 1000, 221.000 ms after lwSRP last had nothing to send, past JoinTime + T_svc (220 ms` | rule removed (every `idle_us` dropped): ESCAPED, 0 findings (`probes/ablate.txt`) |
| the same, inside | control `requested-within`, 219 ms | none: graded clean | |
| `[TIME]` Join interval under the new attribution, low side | `join-early-past-t-svc`, 159 ms | `a Join timer's transmit opportunity at ms 160, 159.000 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms` | `after_join` dropped: ESCAPED |
| the same, high side | `join-interval-late`, 261 ms | `a Join timer's transmit opportunity at ms 15021, 261.000 ms after the one before, ...` | `after_join` dropped: ESCAPED |
| the same, in code | lwSRP Join timers of 10 and 15 cs (`srptx_mutants.py`) | `a Join timer's transmit opportunity at ms 100, 98.989 ms ...` and `at ms 150, 148.989 ms ...`, `outside JoinTime's range widened by T_svc (160 to 260 ms` | |
| the attribution itself (F-1) | the off-grid control `licence-16280`, a real run | graded clean at this head | 2131eff4's grade, and this head's with 2131eff4's window put back: `[TIME] MSRP: a Join timer's transmit opportunity at ms 16281, 281.030 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms` (`probes/ablate.txt`) |
| the off-grid control's case | `off_grid()` on `licence-16280` and `licence-16240` | `FAIL licence-<ms>: ... wanted clean with a requested transmit opportunity after an idle Join expiry` if the case is gone | |

Counting a LeaveAll frame the Join timer held is safe only with the bench's record. With 2131eff4's 100 ms window applied to LeaveAll frames too, `wire` gives six false Join-interval refusals: LeaveAll frames that followed a Join expiry which found nothing to send (`probes/ablate.txt`, window-la).

## Gates

All ran at `2128daad26b932feeed1ef2bde8f2774e8a51a31`, each group on its own clean clone (`tools/clone.sh`: `--shared` clone of the lane, submodules from the lane's). Pinned Verilator 5.050. Receipts are under `receipts/`, indexed by `receipts/INDEX.md`. Every earlier attempt and its cause is in `receipts/ci/attempts.txt`.

| Gate | rc | Result | Receipt |
|---|---|---|---|
| `make srptx` | 0 | wire 0 findings (1,449 MRPDUs), hold 0 (169), licence 0 (69), `licence-16280` 0 (69), `licence-16240` 0 (69) | `srptx/make-srptx.txt`, `srptx/*-report.json.txt`, `srptx/captures-sha256.txt` |
| `make srptx-plants` | 0 | `srptx plants: 26 of 26 refused; 4 of 4 controls inside their bound clean; 2 of 2 off-grid controls clean with their requested transmit opportunity` | `srptx/make-srptx-plants.txt` |
| `make srptx-mutants` | 0 | 5 clean controls, then `srptx mutants: 12 of 12 refused`. The 10 cs and 15 cs arms: `at ms 100, 98.989 ms` and `at ms 150, 148.989 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms` | `srptx/make-srptx-mutants.txt` |
| R813-2's `request_probe.py tb/verilator/milan_dp WORK 280 240`, unchanged (sha256 `baa576da...4a3c`, equal to its manifest) | 0 | 0 findings at both offsets. The answer at 16,281.044 and 16,241.044 ms has no Join cause. `srptx.hpp` is restored byte for byte | `probes/request-probe.txt` |
| R814-1's `code_probe.py`, unchanged (sha256 `0e5d16ae...736c`), arms `join-10cs` and `join-15cs` | 0 | `join-10cs` REFUSED (15 findings), `join-15cs` REFUSED (16): the counts both reviewers reported at round 2 | `probes/r814-1-code-probe.txt` |
| the ablation (`tools/ablate.py`) on the head's own captures | 0 | The grade at `2131eff4`, and this head's with `2131eff4`'s window put back, refuse `licence-16280` by F-1's words. Both give `licence-16240` 0 findings. Without the requested rule, `requested-late` escapes. Without `after_join`, the two Join plants escape. With that window over LeaveAll frames too, `wire` gets 6 false refusals | `probes/ablate.txt` |
| the attribution and figures (`tools/attrib_compare.py`, `tools/join_figures.py`, `tools/measured_diff.py`) | 0 | Every frame `2131eff4` gave the Join timer in wire, hold and licence is one the bench saw sent at the first poll after a Join expiry. Only R813-2's frame changes class in each off-grid run. Join intervals are 198.958 to 200.024 ms, 0 outside 160 to 260. Requested ones leave at most 1.0253 ms after the last idle poll. The changed measured leaves are listed, all Join/periodic counts and means | `probes/attribution-compare.txt`, `srptx/join-figures.txt`, `srptx/measured-diff-vs-round2.txt` |
| `make twin`, `make twin-plants` | 0, 0 | The split capture `obj_twin/split.json` is 54,965 bytes, sha256 `ee143865...6308`, equal to round 1's. The twin plants are each refused | `srptx/make-twin*.txt`, `srptx/twin-split-capture.txt` |
| the srptx clone after the gates, and after the code probe | 0 | `git status --porcelain` empty | `srptx/gate-clone-clean.txt`, `probes/code-probe-clone-clean.txt` |
| every `run:` step of every job a ready pull request to `dev-soft-core` triggers: docs, elaborate, rtl-fast (with firmware-boundary in the LiteX venv and firmware-verilator) and rtl, 69 job instances (`tools/ci_replay.py`) | 0 | `546 steps ran, 0 failed or missing; 86 not run, each with its reason`. 68 instances success; `physical-gptp` skipped by its own `if:`. The 86 are 41 APT resolutions, 22 and 5 source builds of the pinned Verilator and Yosys already built here, 16 hosted-only GitHub API steps, 1 default-branch read and the skipped job | `ci/ci-replay-table.md`, `ci/not_run.json.txt`, `ci/replay-results.txt` |
| within it: the firmware self-test, 4 shards (`test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`) | 0 x4 | `test_ctrl_firmware: PASS` in each. The control campaign: `mutants: 570 of 570 caught`. The AECP and SRP campaigns and their pin controls pass | `ci/key-verdicts.txt` |
| within it: `fw_coverage.py --selftest`, `--check` | 0 | `firmware coverage: PASS (35 files)` | `ci/key-verdicts.txt` |
| within it: `ctrl_boundary.py --require-rv32 --selftest`, without and with Verilator | 0, 0 | `ctrl_boundary: PASS`, 183 pin controls | `ci/key-verdicts.txt` |
| within it: `cd tests && behave` (bdd-conformance) | 0 | 14 features, 508 scenarios, 2,330 steps passed, 0 failed, 0 skipped | `ci/key-verdicts.txt` |
| within it: elaborate, the 19 Verilator shards and their unions, the Yosys shards and portability, the docs workflow's jobs, publication-census, split-cdc | 0 | as the table shows | `ci/ci-replay-table.md` |
| the FULL sweep, 4 shards (`run_all_suites.sh --shard k/4`, each its own clone and unit, MemoryMax 10G, `MAKEFLAGS=-j4 --no-print-directory`; shard 2, with capture_coherence, on 4 CPUs) | 0 x4 | 65 suites passed, 0 failed, 0 timed out (15, 17, 17, 16); 2,192,910 checks, 0 in-suite failures | `sweep/shard-*.txt`, `sweep/shard-*-complete.json.txt`, `sweep/launch.txt`, `sweep/native-spec.json.txt` |
| `test_builder.py --require-rv32` (LiteX venv, the pinned SDK installed and verified by `ci_rv32_sdk.py`) | 0 | `ALL GATES PASS EXCEPT 2 NOT RUN`: gate 1b (this make does not re-read MAKEFLAGS mid-parse) and gate 11 (needs an earlier board build's utilization report), as in round 1 | `gates/test-builder.txt`, `gates/rv32-sdk*.txt` |
| S2's harness: `run.py --self-test`, `--point 1x1` (1 interface), `--point 8x8` (2 interfaces), `--record-budget-findings` | 0, 0, 0 | 18 and 17 groups graded, 0 refusals. The T_svc misses it records (34 and 63) are against this base's proposed 10 ms, as in round 1 | `gates/budget-*.txt` |
| `make split`, `split-mutants`, `split-cdc`, `split_parallel.py --selftest`, then the clone's status | 0 each | `checks: 82 failures: 0`; `split mutants: 26 of 26 caught`; split-cdc passes; `split_parallel: PASS`; clean | `gates/make-split*.txt`, `gates/split-*.txt` |
| `git diff --check 1d6bf555 2128daad` and `2131eff4 2128daad` | 0, 0 | clean | `gates/diff-check*.txt` |

Before committing, the working tree also passed the following, and the docs jobs above re-ran them on clean clones:
- `docs_check.py`, after one wording fix ("as requested" read as attribution);
- `gen_toc.py --check` and `--verify-anchors`, with the pinned Markdown venv;
- `check_em_dash.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_hygiene.py --check` and `check_todo_ownership.py`;
- `check_py_idiom.py` and `check_cpp_idiom.py`;
- `measure_test_evidence.py`, `measure_naming.py` and `measure_fail_fast.py --check`.

**Attempts before the kept results** (`receipts/ci/attempts.txt`; none is a defect of the change):
- **`publication-census`.** Attempt 1 was stopped by me: its 9 census workers, sized by the step from this session unit's 16 GiB limit, took the unit to 14.8 GB. Attempt 2 was killed by the host restart. Attempt 3 ran alone on 2 CPUs: success.
- **`elaborate-gates-1`.** Three attempts in the shared session pool ended `gate_19` at exit 92, UNKNOWN: `test_soc_timing_cuts` hit its 900 s wall clock, with 7 of 8 passed and 0 failed. The same step in that job's environment with `LITEX_SIM_TIMEOUT=7200` passed 8 of 8, `test_soc_timing_cuts: 0 failure(s)`, in 1,864 s (`gates/litex-sims-diag.txt`, a diagnostic). The fourth attempt, on its own unit on a dedicated range: success, 8 of 8 within the 900 s clock. `elaborate` and the jobs after it re-ran on it.
- **`verilator-shards__5`.**
  - Attempt 1 was the #833 class: the preflight's suite-cancellation control, `CLEANUP FAILED: owned descendants remain`. Re-run once; both results are kept.
  - Attempts 2 and 3: `media_phase` hit its 1,400 s wall clock, UNKNOWN, with 0 in-suite failures.
  - Attempt 4, on a dedicated unit: success. `media_phase` also passed in the full sweep.
- **`verilator-shards__7`.** Attempt 1: `mmcm_servo` hit its 1,800 s wall clock, UNKNOWN, with 0 in-suite failures. Attempt 2: success. `mmcm_servo` also passed in the full sweep.
- **The host restart at about 18:01.** It killed shards 1 to 3 of the replay's Verilator jobs, the census, two sweep shards, `budget-8x8` and a diagnostic. Each re-ran from a fresh start: the sweep in full on new units, and `budget-8x8` on its own fresh clone.
- **The sweep's CPU bookings.**
  - At 14:58, a release hold booked 0-7 in the same minute shard 2 launched there.
  - At 18:07, release holds booked 0-31 while all four `native-shards.py` units launched there.

  Each time I stopped my units within 2 minutes, kept no result, and relaunched on free ranges only. The kept sweep's four units each had their cores to themselves (`sweep/launch.txt`). No four 8-CPU ranges were free at once after the restart, so the shards launched one by one through `tools/sweep-shard.py`, which does for one shard what `native-shards.py` does for each.

**How it ran.** The replay ran three local runners in my own session unit, each pinned to its own 8 CPUs. Long or memory-heavy jobs ran in their own units on dedicated 0-95 ranges (`tools/unit_job.py`, `tick`), MemoryMax 10G. After the census stop, the session unit's anonymous memory peaked at 9.77 GB (`tools/memlog.py`). No git config file was written. The RV32 SDK is the pinned release, installed from its pinned archive and verified by `scripts/ci_rv32_sdk.py` into scratch.

## Not run, and why

- `act`: nothing is pushed, and the manager owns the act replica and the hosted contexts.
- No hardware, bench, Vivado route, flashing, push or PR edit.
- The 86 replay steps in `ci/not_run.json.txt`, each with its reason (above).

Scratch left for the manager: `/data-2/milan/tmp/665s7-a757c` (the gate clones, the replay's job clones and attempts, the sweep logs and the dev build), and the shard clones `$LANES/a757c-shard0` to `3`.
