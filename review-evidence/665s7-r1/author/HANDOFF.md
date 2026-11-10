# [A757] #867 (S7 of #665): lwSRP's transmit path to the wire in the split build

Status: **STOP** at head `5fb6904ffe12effc4bde6bf5313faea7a3beebdc` (round 1). Every gate is green at that head. Item 5 holds only under a published test fixture, so its production composition needs a decision (below). TAKEN: issue 867 comment 6751085802. STOP: issue 867 comment 6760788103 (`STOP-COMMENT.md`).

Lane: `$LANES/665-s7-srp-tx`, branch `665-s7-srp-tx`, base `dev-soft-core` `1d6bf555`. Ten commits, added only, not pushed:

| Commit | Subject |
|---|---|
| `6cd55475` | Record the split half's SRP transmit path at lwSRP's boundary, its timers, the SRP ring and the MAC with --srptx, with a held MAC and a fixture-licensed source 0 (#867) |
| `0eb4115c` | Grade the split's MRPDUs at the wire for their 10.8 form, source address, timer spacing within T_svc, a full ring and the #608 stop and licence, with twenty capture plants and nine code mutants (#867) |
| `46950c25` | Hold each source's LICENCE bit to its stream gate and the CRF licence term in the split leg, with two planted defects (#867) |
| `324f7778` | Document the split build's SRP transmit path at the wire, its fixture, measurements, plants and mutants, and the policer check (#867) |
| `3c134c24` | Grade the split's MRP spacing and the #608 stop at min(T_svc, the MRP ceiling), 18 ms, refuse a modeled millisecond past 1 ms, and plant both (#867) |
| `ff27f631` | Name the issue and the behaviour in the SRP transmit check's comments, with no comment ID or plan stage (#867) |
| `864665a7` | Plant the bench's own lwSRP timer layout check, in a capture and in lwSRP's port state (#867) |
| `25a413b3` | Call the SRP channel's ring its transmit ring in the check, its words and docs, the term the bare-metal scope gate keeps (#867) |
| `bf1bba25` | Explain the SRP transmit mutants' reads of lwSRP, the adapter and the datapath to the test-evidence ratchet (#867) |
| `5fb6904f` | Give the firmware README the 183 pin controls the boundary self-test counts with the SRP transmit check's two programs classified (#867) |

There is no RTL, firmware, lwSRP, mailbox-contract, ring or shape-config change, and so no lwSRP donor patch. The changes are in `tb/` and two gate tables, `sw/firmware/ctrl/test/ctrl_configs.py` and `scripts/measure_test_evidence_readers.py`, plus four docs pages. The generators' `--check` runs and the docs inventory gates pass (the docs workflow below).

## The blocking line (item 5)

Item 5 (#608: a withdrawal after a LeaveAll stops the talker) needs a split talker that can hold a licence.

- At this base every split source declares Talker Failed. `sw/firmware/ctrl/plat/ctrl_plat.c:146-161` (`configure_sources`) never sets `allocated`. `sw/firmware/ctrl/srp/srp_mbx.c:170` admits only an allocated source, and `:820-830` licenses only an admitted one.
- #665 ruling issuecomment-6505997821 item 3 defers the adapter entry that re-declares a source once MAAP allocates, until S2b's `srp_mbx.c` lands. S2b (`origin/665-s2b-cycles`) rewrites that file's transmit path, so this lane does not touch it.
- The #608 check therefore runs under a published, test-only fixture, `tb/verilator/milan_dp/srptx.hpp:567` (`__wrap_srp_mbx_init`, licence scenario only). It hands the adapter source 0 allocated at MAAP's pinned simulation range. Every finding of that scenario names the fixture.
- Under it, the stop holds. The peer's LeaveAll at 16,000 ms armed the Listener's Leave timer. The withdrawal at 18,000 ms re-armed nothing. The timer expired at 21,000 ms, `LICENCE` cleared 12 us later, and the stream gate closed that millisecond. The lwSRP mutant that restarts LeaveTime on a withdrawal in LV is refused.
- **The decision needed:** accept item 5 under the fixture, or keep #867 open for the allocation entry. The PR body says "Relates to #867" and does not close it.

## Changes (file:line, reason)

- `tb/verilator/milan_dp/srptx.hpp` (new). The bench, in S7 mode only, with each wrapper passing through otherwise:
  - lwSRP's own output at its boundary: `:486` `__wrap_mrp_transmit` and `:454` `trampoline`;
  - its participants: `:500` `__wrap_mrp_rx` and `:509` `__wrap_mrp_port_configure`;
  - its timers, read from the public `cs` field: `:526` `__wrap_shlan_timer_arm` and `:551` `__wrap_shlan_timer_tick`;
  - the SRP ring's head and tail and every LICENCE write: `:264` `hal_write`;
  - the MAC's frames with their first beat's time, and the peer's answers: `:288` `mac_frame`;
  - the policer each millisecond: `:311` `sample`;
  - the three scenarios: `:324` `scenario`;
  - the fixture: `:567`;
  - the capture: `:365` `write`.
  Reason: items 1 to 6 need lwSRP's output and timers at its own boundary without editing the adapter, which S2b owns.
- `tb/verilator/milan_dp/twin_split.cpp`. Reason: the twin's bench stops clocking once the firmware owes nothing, so a frame sent after another left about 10 modeled ms late (the twin's MVRP at 12 ms). This is changed in S7 mode only, and the twin's own capture is byte-identical with these changes.
  - `:98` the time base (`now_us`);
  - `:318` the MAC hold in `tick_ms`;
  - `:197` the first-beat time and the peer's answers in `tx_take`;
  - `:81` and `:222` the drain, with `:372` its two service rounds;
  - the HAL hooks, and `:464` `srptx_main`.
- `tb/verilator/milan_dp/tb_split_top.sv:106-111, :398-404`: the probes `p_stream_gate`, `p_aaf_gate`, `p_crf_res_active`, `p_crf_emit`, `p_n_talkers` and `p_crf_tk`. Reason: the policer is read where its consumers read it.
- `tb/verilator/milan_dp/Makefile`:
  - `:931` `SRPTX_WRAPS` on `build-twin-sp`: links lwSRP's boundary into the bench;
  - `:909` `TWIN_FW_ARGS`: lets a mutant plant a firmware unit;
  - `:1001-1013` `srptx`, `exec-srptx-%`, `srptx-plants` and `srptx-mutants`, and `clean`.
- `tb/verilator/milan_dp/twin_fw.py:21, :90`: `--replace ORIGINAL=COPY`. Reason: a code mutant builds through the same composition.
- `tb/verilator/milan_dp/srptx_grade.py` (new): the grade.
  - `:142` `walk` and `:262` `grade_wire`: `[WIRE]`, 10.8.1/10.8.2.
  - `:300` `grade_source`: `[SA]`.
  - `:313` `grade_time` and `:375` `measure_time`: `[TIME]` and the measurements. `:63-64` sets the bound to min(T_svc 20, the MRP ceiling 18) = 18 ms, the owner's per-family rule of 2026-10-29.
  - `:424` `grade_tx`: `[TX]`.
  - `:501` `grade_licence`: `[608]` and `[LIC]`.
  - `:563` `grade`, with `[BENCH]`.
- `tb/verilator/milan_dp/srptx_plants.py` (new): 23 capture plants. `tb/verilator/milan_dp/srptx_mutants.py` (new): 10 code mutants.
- `tb/verilator/milan_dp/sim_split.cpp:329` `check_policer`, and two arms in `tb/verilator/milan_dp/split_mutants.py`: item 6 per bit, for every talker.
- Gate tables:
  - `sw/firmware/ctrl/test/ctrl_configs.py:235-237`: `srptx_grade.py` in `OUTSIDE`;
  - `ctrl_configs.py:265-269`: `srptx_mutants.py` in `SUITES`;
  - `scripts/measure_test_evidence_readers.py:253-257`: `srptx_mutants.py`'s disposition.
  Reason: the boundary gate's builders found by text, and the test-evidence ratchet's DUT-source readers.
- Docs:
  - `tb/verilator/milan_dp/README.md:1488`, a new section, plus the `[POL]` row, "twenty-six" defects and the contents (regenerated by `gen_toc.py`);
  - `sw/firmware/ctrl/srp/README.md:380-390`, Integration still owed;
  - `docs/design/MAILBOX_SPLIT.md:1850-1858`, Open items;
  - `sw/firmware/ctrl/README.md:255`, 183 pin controls.

## Checks, planted mutants and failing words

Each check, its plant or mutant, and the words that refuse it: `tb/verilator/milan_dp/README.md`, sections "The plants and the mutants" (23 plants, 10 code mutants) and "The split placement's control path" (the `[POL]` arms). The issue's five:

| The issue's mutant | Capture plant | Code mutant | Refused by |
|---|---|---|---|
| a malformed EndMark | `malformed-endmark` | lwSRP `tx_close` `end[1] = 1` | `MSRP AttributeList EndMark missing where its AttributeListLength ends` |
| a doubled declaration | `doubled-declaration`, `doubled-message` | lwSRP `tx_message`, each value twice | `declared 2 times in one MRPDU`; `2 Messages of AttributeType 4, not one per AttributeType` |
| LeaveAll on the wrong type | `leave-all-wrong-type` | lwSRP `mrp_transmit`, LeaveAll on the last type alone | `a LeaveAll on AttributeTypes [4], not on every MSRP AttributeType [1, 2, 3, 4]` |
| a frame dropped under backpressure | `dropped-under-backpressure` | the adapter's `send_pdu` reporting a refused MRPDU sent | `never left the MAC` |
| a zero source address | `zero-source` | the adapter's `send_pdu`, no source address on the first MRPDU | `[SA] MSRP frame at ms 1 from 000000000000, not the port's MAC` |

The other plants and mutants each kill one more check:
- `[TIME]`: `join-late`, `join-late-in-t-svc` (219 ms: inside a 20 ms bound, past the 18 ms one), `rate`, `leave-all-missing`, the lwSRP Join timer of 23 cs, and the LeaveAll drawn past 1.5 x LeaveAllTime.
- `[TX]`: `reordered`, `backpressure-unseen`, `refused-with-room`, `retention-lost`.
- `[608]`: `late-stop`, `never-stopped`, `stream-after-stop`, and the lwSRP LV/rLv! restart.
- `[LIC]`: `gate-not-licence`, `aaf-without-licence`, `stream-without-licence`, and the datapath's ACTIVE held open.
- `[BENCH]`: `bench-overrun`, `timer-layout`, and a field before lwSRP's Join timer.
- `[POL]`: the licence on the next source's ACTIVE term, and the CRF licence term on source 0's gate.

## Measurements

The `milan_dp` README section "What it finds at this head" has them. They are identical in the gate clone at the final head:
- **Egress after the timer's tick:** Join and periodic 1.52 to 26.31 us. LeaveAll up to 50/70 ms: the transmit opportunity's wait while the Join timer runs.
- **Interval error:** JoinTime -1.01 ms to +0.02 ms (the centisecond grid). Periodic within 13 us. LeaveAll mean 0 with min/max -50/+50 ms (MSRP) and -70/+70 ms (MVRP).
- **N:** 104 Join, about 520 periodic and 39/40 LeaveAll per participant.
- **Frames per transmit opportunity:** 1 (727 MSRP, 722 MVRP).
- **Backpressure:** the ring at 507 of 512 words when a 30-word MSRP record was refused. That MRPDU was retried 160,001 times and was the first sent at 25,000 ms. The queue left about 11 us apart.

## Findings for the manager (this lane may post on #867 only)

- The split's AAF frames carry stream_id 0. No firmware writes the publication block's `SRC_SID` (`MBX_PUB_SRC_REG_SRC_SID_LO/HI`). It is latent until a split talker streams, after the allocation entry.
- The twin's own split half has the bench artifact the S7 drain removes: its MVRP leaves about 11 modeled ms after the MSRP of the same opportunity. The twin's grades pass with it, and the twin is unchanged here.
- `MAILBOX_SPLIT.md` and FR_NFR 3.4.1 at this base still state T_svc as the proposed 10 ms, and the budget harness grades against it. The 20 ms approval and per-family rule live in #665 and S2b's lane.

## Gates (all on clean clones; receipts under `receipts/`, index `receipts/INDEX.md`)

| Gate | Head | rc | Result | Receipt |
|---|---|---|---|---|
| Every `run:` step of docs, elaborate, rtl-fast and rtl for a ready pull request to dev-soft-core (69 job instances, each on its own clean clone; `tools/ci_replay.py`) | `5fb6904f` | 0 | 546 steps ran, all rc 0. 86 not run, each with its reason (APT resolution, source builds of tools pinned here, hosted-only GitHub API steps, and jobs whose `if:` is false for this event). Covered: firmware-boundary with the LiteX venv (`ctrl_boundary: PASS`), firmware-verilator, the firmware self-test (4 shards), `fw_coverage.py --check`, every firmware mutant campaign, `behave`, the builder legs, the 19 Verilator shards and their unions, the Yosys shards, elaborate | `ci/ci-replay-table.md`, `ci/ci-not-run.json`, `ci/key-verdicts.txt` |
| FULL sweep, 4 shards (`run_all_suites.sh --shard k/4`, own clones and units, MemoryMax 10G, `MAKEFLAGS=-j4 --no-print-directory`, pinned Verilator 5.050; capture_coherence's shard 2 on 4 CPUs) | `5fb6904f` | 0 x4 | 65 suites passed, 0 failed, 0 timed out (15, 17, 17, 16); 2,192,910 checks, 0 in-suite failures | `sweep/shard-*.txt`, `sweep/native-spec.json` |
| `git diff --check 1d6bf555 HEAD` | `5fb6904f` | 0 | clean | `gates/diff-check.txt` |
| `make srptx` | `5fb6904f` | 0 | wire, hold, licence: 0 findings each | `srptx/make-srptx.txt`, `srptx/*-report.json.txt`, `srptx/captures-sha256.txt` |
| `make srptx-plants` | `5fb6904f` | 0 | 23 of 23 refused | `srptx/make-srptx-plants.txt` |
| `make srptx-mutants` | `5fb6904f` | 0 | 10 of 10 refused, after clean controls | `srptx/make-srptx-mutants.txt` |
| `make twin`, `make twin-plants` | `5fb6904f` | 0, 0 | `twin: 0 finding(s)` (only ledger and owed rows); 20 plants, each refused by its words, none escaped; the split capture byte-identical to the base binary's | `twin/*.txt` |
| `make split`, `make split-mutants`, `make split-cdc`, `split_parallel.py --selftest` | `5fb6904f` | 0 each | 82 checks, 0 failures; 26 of 26 caught; split-cdc passes; the parallel gate passes | `gates/make-split*.txt`, `gates/split-parallel.txt` |
| `test_builder.py --require-rv32` (LiteX venv, the pinned SDK) | `bf1bba25` | 0 | ALL GATES PASS EXCEPT 2 NOT RUN: gate 1b (this make does not re-read MAKEFLAGS mid-parse) and gate 11 (needs an earlier board build's utilization report) | `firmware/test_builder-bf1bba25.txt` |
| S2's harness `run.py --self-test`, `--point 1x1`, `--point 8x8` (`--record-budget-findings`) | `bf1bba25` | 0 each | 18 and 17 groups graded, 0 refusals; the T_svc misses it records are against this base's proposed 10 ms | `gates/budget-*-bf1bba25.txt` |

The last two rows ran at `bf1bba25`. The final head differs from it only by `sw/firmware/ctrl/README.md:255`, the count 181 to 183, which neither reads (`git diff --stat bf1bba25 5fb6904f`).

Earlier attempts and their causes are recorded in `receipts/ci/attempts.txt`. None is a defect of the change:
- The #833-class cancellation-control timeouts. They were re-run once, both results recorded. The cause was this session's inherited signal state, fixed by `tools/sigclean.py`.
- The replay's git environment, which a suite's guard refuses.
- A sweep that ran at the first head.
- The README count.

**How it ran.** The replay ran up to four local runners in this lane's own unit (8 CPUs, under 10 GB). The tick placed jobs on free 8-CPU ranges as they freed, and the sweep shards ran one per free range (the host never had four free at once). No git config file was written anywhere: git took its settings from `GIT_ALLOW_PROTOCOL` and the `GIT_AUTHOR_*`/`GIT_COMMITTER_*` identity. The RV32 SDK is the pinned release, installed and verified by `scripts/ci_rv32_sdk.py` into scratch.

Not run: `act`, because nothing is pushed. No hardware, bench, Vivado or flashing.

Scratch left for the manager: the shard clones `$LANES/a757-shard0` to `3`, and `$VALIDATION_STORAGE/665s7-a757` (the replay's job clones, the gate clones and the verified SDK).
