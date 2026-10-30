# [A699c] processor #203 round 3 handoff: the request only after the last started frame has left

Status: REVIEW READY at head `013ee63`. Code, tests, arms and docs are committed.

- Every gate and campaign below finished with rc 0, each in one run, and every planted arm was
  KILLED.
- The reviewers' probes, unchanged, pass at the head.
- The scratch-parent consumer gate passes with `reboot_req_o` unconnected.
- The STOP condition was not met. Not pushed. PR-BODY.md is ready.
- One process fault: this unit's memory peaked at 12.48 GB, once, before a governor was added
  ("Gates run", Memory).

## Assignment

- Round 3 is the latest [A10] comment on issue #203 (issuecomment-6511187991). It asks for a
  fix of R731-F1 = R732-F3 (MAJOR) and R732-F4 (MINOR).
  - R731-F1 = R732-F3: when the entity is not advertising, no DEPARTING is sent, and
    `reboot_req_o` rose while a non-ADP frame was still on `tx_*`.
  - R732-F4: PR-BODY.md's validation figures were round 1's.
- Reviews: R731-1 (PR #209 issuecomment-6511183050) and R732-2 (issuecomment-6510713462), both
  NEGATIVE at `ec1ff27`. Their probes were read and run unchanged (below).
- TAKEN posted: issuecomment-6511210749. REVIEW READY posted with head `013ee63`:
  issuecomment-6514665539. These two are this round's only posts.

## Base and head

- Repository: processor (protocol-processor-control-plane-avb-milan), branch `203-aecp-reboot`.
  Before the first commit, `git remote get-url origin` was the processor repository and HEAD was
  round 2's `ec1ff27`. Main `f65c8ff7` is its merge base.
- Base: main `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8`. Round-2 head:
  `ec1ff275a72d885f0908fd213d8009e9e4dda4d9`.
- **Head: `013ee63fd42455987ddbbbeb3b66f5af106b5793`** (tree `b0f66acb`). Two commits on top
  of `ec1ff27`, with no rebase, no force and no push. One-line subjects, no body, no trailers:

| Commit | Subject |
|---|---|
| `cb73ff3` | Raise reboot_req_o only once the TX arbiter is idle, so a frame another lane started leaves whole first, with or without a DEPARTING, and grade it with the reviewers' two non-advertising cases (issue #203) |
| `013ee63` | Say in the architecture, guides and compliance review that reboot_req_o waits for the last frame started, of any lane (issue #203) |

## R731-F1 = R732-F3: design

- **The defect.** RB_DEP left on ADP's builder, ADP's lane queue and ADP's own frame in flight.
  An entity that is not advertising builds no DEPARTING, so RB_DEP passed in its first clock.
  A frame another lane had selected while the gate was still open was then still streaming:
  in R731's probe it was the lock's unlock notification, in R732's probe the listener's
  CONNECT_TX_COMMAND.
- **The fix: the arbiter's own state.** `KL_pp_tx_arbiter` gets an internal output `busy_o`,
  `arb_st_r != A_IDLE`. It is high from the clock after a frame's selection (A_START) to the
  clock the downstream takes that frame's last byte. Its `eof_w` is that handshake, at the MAC
  face, because the shim passes `tx_ready_i` through on the body. The grant pulse falls inside
  that span: the pool streams at the earliest one clock after it accepts the start. So an idle
  arbiter has no frame selected, starting or streaming, and no grant outstanding.
- **RB_DEP's exit** is now `!adp_tx_busy_w && (laneq_adp_cnt_r == 0) && !arb_busy_w`. It
  replaces round 2's `!tx_fly_adp_r`. ADP's frame is one of the arbiter's frames, so the old
  flop was a strict subset and is removed.
- **No new frame after the request.** The exit is taken only with the transmit gate closed.
  `rbt_quiet_w` holds in RB_DEP when ADP is not busy, which is part of the exit condition. ADP's
  queue is also empty then, so no lane requests and no frame is being selected in that clock
  (selection reads `pend_r & req_valid_i`, and the gate masks `req_valid_i`). From RB_REQ the
  gate stays closed to every lane but ADP's, and ADP, its enable fallen, builds nothing more
  (round 2). So nothing is offered on `tx_*` from the rise to `rst_n`.
- **Both cases.**
  - Advertising: the last frame is the final DEPARTING, exactly as before.
  - Not advertising: the gate closes two clocks after the notification round has left. A frame
    selected by then is sent whole, and the request waits for its last byte.
- **Required frames stay first.** The SUCCESS response is granted before the acceptance. The
  notifications are granted before RB_DOWN (RB_NTF, unchanged), and the DEPARTING is queued only
  at RB_DOWN. The sequence's earlier waits are unchanged.
- **No top-level change.** `busy_o` is a port of an internal module, connected at the top
  (`arb_busy_w`) and in the `tb/tx_arbiter` harness. The processor top's port list, parameters
  and register map are unchanged, so the STOP condition is not met.

## Changes (file:line at head, clause)

| # | File:line | Change | Clause / item |
|---|---|---|---|
| 1 | `hdl/packet_engine/KL_pp_tx_arbiter.sv:85`, `:301` | `busy_o` = `arb_st_r != A_IDLE`, with the grant-inside-span reason | REQ-FWX-001; R731-F1 "the arbiter idle with no grant outstanding" |
| 2 | `hdl/top/protocol_processor_top.sv:4593`, `:4732` | `arb_busy_w`, connected to `u_tx_arbiter.busy_o` | same |
| 3 | `hdl/top/protocol_processor_top.sv:4947` | RB_DEP waits for `!arb_busy_w` instead of ADP's frame in flight; `tx_fly_adp_r` removed (`:4912`) | REQ-FWX-001; IEEE 1722.1-2021 §7.4.43, §7.5.2; Milan v1.2 §5.4.5.2, §5.6.3.5.8, §5.6.3.5.11 |
| 4 | `hdl/top/protocol_processor_top.sv:4879`, `:4899` | sequence banner: RB_DEP's wait for the last frame started, of any lane, with or without a DEPARTING; the gate's frame waited for | same |
| 5 | `hdl/top/protocol_processor_top.sv:833` | `reboot_req_o` port comment: it also waits for the last frame started; a reset taken on its rise cuts no frame; from the rise no byte is offered | REQ-FWX-001; R731-F1 contract |
| 6 | `docs/architecture/06_aecp_engine.md:1103` (step 4), `:1135`, `:1140`, `:1145`, `:1503` (§8.1 row) | step 4 of the request (the TX arbiter idle); no byte from the rise; the not-advertising case; RBT7, RBT12, RBT13 and the arms | same |
| 7 | `docs/architecture/02_interfaces.md:138` (reset rule 6), `:584` (F02.10 `reboot_req`) | the request after the last frame started, of any producer; no byte offered from its rise | same |
| 8 | `docs/architecture/03_packet_engine.md:494` | F03.5 "REBOOT gate" row: the request waits for the arbiter's `busy_o` | same |
| 9 | `docs/architecture/04_adp_engine.md:166` | the request once the DEPARTING, and any frame started before it, has left | same |
| 10 | `docs/guides/integrator.md:588` (status table), `:699` (bring-up step 7) | no frame on `tx_*` at the rise, so a reset taken on it cuts none | R731-F1 "the guide asks the integrator to rely on it" |
| 11 | `docs/guides/operator.md:52` | REBOOT row: a frame already started finishes, then nothing | same |
| 12 | `docs/00_MILAN_COMPLIANCE_REVIEW.md:316` (GAP-13), `:557` (REQ-FWX-001 row) | the request after the last frame started; the arbiter's `busy_o` in the realization cell | REQ-FWX-001 |
| 13 | `tb/pp_top/pp_top_wrap.sv:303`, `:836` | tap `dbg_rbt_tx_open_o` = `u_dut.rbt_tx_open_w` (the lanes the gate lets start a frame) | test observability |
| 14 | `tb/pp_top/sim_main.cpp:1004`, `:1703`, `:2166` | harness: `stall_after_t`, so the MAC holds the last byte of every frame whose first byte it took after that clock | R731/R732 "backpressure on its EOF" |
| 15 | `tb/pp_top/sim_main.cpp:12718` | RBT7: every TX lane open while the MAC holds the SUCCESS response's last byte | keeps RBT7's premise graded (see the arms) |
| 16 | `tb/pp_top/sim_main.cpp:13066` to `:13187` | RBT12 and RBT13 (below), and their two shared steps | R731-F1, R732-F3 "make each probe a permanent check" |
| 17 | `tb/pp_top/aecp_dispatch_mutants.py:76` to `:88`; `tb/pp_top/aecp_dispatch_mutations/rbt-last-frame-unwatched.patch`, `rbt-last-byte-offered.patch` (new), `rbt-departing-unwatched.patch`, `rbt-request-pulse.patch` (re-cut, same plants) | the two new arms; two arms re-targeted (below) | "a planted defect that raises the request early" |
| 18 | `tb/pp_top/README.md:1425` to `:1455` (arm table, every REBOOT count re-measured), `:1514`, `:2671`, `:2706` | RBT7's gate check, RBT12, RBT13, the arms and the renames | docs |
| 19 | `tb/tx_arbiter/tx_arbiter_harness.sv:47`, `:105`; `tb/tx_arbiter/sim_main.cpp:113`, `:240`, `:614`; `tb/tx_arbiter/README.md:7`, `:40`, `:59` | the harness exposes `busy_o`; every clock it is compared to the model's owner (a selection pending or a frame in service), in every phase, and test G checks it | the new output's own unit check |

## New checks, planted arms and failing words

Section RBT has 155 checks, 0 failures at the head (`make -C tb/pp_top reboot`). Round 2 had
127. The new rows are the two reviewers' probes, made permanent, each with EOF backpressure on the
other lane's frame:

| Check | What it grades |
|---|---|
| RBT7 `every TX lane is open while the MAC holds the SUCCESS response's last byte` | `dbg_rbt_tx_open_o` reads `0xFF` at the end of the 30 ms hold. This is RBT7's own premise: an answer let in would reach the wire |
| RBT12 (R731's probe): not advertising, one other controller, the requester's lock | The MAC holds the REBOOT notification's last byte 1 s, so the lock expires and every lane stays open (`RBT12 every TX lane is open while the MAC holds the REBOOT notification's last byte`). Released, the next frame is held at its last byte (`... another lane's frame follows the REBOOT notification, its last byte held`), and it is the lock's unlock notification (LOCK_ENTITY, u = 1, to the other controller). `RBT12 reboot_req_o stays 0 while the MAC holds the last byte of another lane's frame` (20 ms). Released: `RBT12 reboot_req_o rises after that frame's last byte, and no byte is offered on tx_* from the rise through 5000 ms to the reset` (`tx_offer_t` equals that frame's last byte). Also: response, notification, then that frame, no DEPARTING; every byte in a whole frame; the request held; the reset clears it |
| RBT13 (R732's probe): the same, with the link up and eight sinks bound to a discovered talker | The MAC holds the notification 5 s, and `RBT13 every standard TX slot is taken when the MAC releases the REBOOT notification (0 free)`. The held frame is the listener's CONNECT_TX_COMMAND (ACMP, message 0). The same request checks follow |
| `tb/tx_arbiter` G `busy_o from each selection to its last byte taken` | `busy_o` equals the model's owner (a selection pending or a frame in service) every clock of every phase, and each phase's clean check includes it. 67 checks |

Arms (target `reboot`), each KILLED by its named check at the head, from the full campaign
(`aecp-dispatch-013ee63`, 105 of 105). The last column is the number of failing checks, equal to
the README cell (`readme-counts.py`: 100 arms, 0 problems).

| Arm | Plant | Named failing words | Failing checks |
|---|---|---|---|
| `rbt-last-frame-unwatched` (new; was `rbt-departing-flight-unwatched`) | RB_DEP without `!arb_busy_w`: ADP's build and queue alone | `RBT12 reboot_req_o stays 0 while the MAC holds the last byte of another lane's frame` (it rose before that frame's last byte); RBT13, RBT6, RBT9 and RBT11 fail too | 11 |
| `rbt-last-byte-offered` (new) | RB_DEP exits on `!arb_busy_w \|\| (tx_valid_o && tx_eof_o)`: the last byte offered taken for taken | `RBT13 reboot_req_o stays 0 while the MAC holds the last byte of another lane's frame`; RBT12 and RBT9's held DEPARTING fail too | 7 |
| `rbt-response-unwatched` (re-targeted) | RB_RESP without the response's last byte (round 1's plant) | `RBT7 every TX lane is open while the MAC holds the SUCCESS response's last byte` (open `08`) | 1 |
| `rbt-notification-flight-unwatched` (re-targeted) | RB_NTF without `tx_fly_uns_r` (round 1's plant) | `RBT12 every TX lane is open while the MAC holds the REBOOT notification's last byte` (open `08`); no frame follows the notification in RBT12 and RBT13 | 10 |

Why two arms were re-targeted. With the last frame's wait in RB_DEP, dropping the response's or the
notification's own wait no longer moves the request: the drain holds it through either loss.
Round 1's named checks for them (RBT7's held request, RBT8's order) therefore pass. What each loss
still changes is when the transmit gate closes. It closes while the MAC still holds that frame, so
no other lane's frame can follow it. The checks that see this are the open-gate checks at the end
of each hold, which are also those rows' premises.

`tb/tx_arbiter` plants (README M6 and M7, `txarb-plants.py`, receipts `processor/tx-arbiter-plants`):

- M6, `busy_o` from the stream only: fails 9 of 67, including `G busy_o from each selection to its
  last byte taken` (3084 clocks off).
- M7, `busy_o` ending at the last byte offered: fails 9 of 67 (1491 clocks off).
- M1 to M5 were re-planted at the 67-check shape: 13, 6, 23, 31 and 2. M4 also fails the `busy_o`
  check.

Every other REBOOT arm keeps its plant and its name. Its count was re-measured; RBT12 and RBT13 add
failures under several. `rbt-departing-unwatched` and `rbt-request-pulse` were re-cut for the moved
context, with the same plant.

The reviewers' probes, unchanged, at the exact head (`probes/reviewer-probes-013ee63`, pinned
Verilator 5.050):

- R731 `run_window_probe` scenarios: PRB-NA, where `reboot_req_o` rose at 105515 and the last byte
  was offered at 105513 (at `ec1ff27`: rose 105454, last byte 105513), and PRB-ADV. 11 checks, 0
  failures.
- R732's post-DEPARTING probe: 156 checks, 0 failures.
- R732's non-advertising probe, made as `run-probes.py` makes it: 162 checks, 0 failures, with
  `request=16184544 in_frame=0`.

## Gates run

Every gate ran in a disposable clone of `013ee63`: `<work>` and `<work2>` (head clones) and
`<clone>` (the campaign clone). Every rc is the command's own status. Campaign arm builds used the
host's Verilator 5.052 through a wrapper that only caps `--build -j 0` (`receipts/tools/vl-j4/verilator`),
with `TMPDIR` on disk. The cap was 4, then 1 while the processor sweep ran beside the dispatch
campaign, then 2 from d3 on. All rc 0:

| Gate | Result | Receipt |
|---|---|---|
| `make check` (PATH with the mermaid CLI) | rc 0; AECP command gate 32 commands, 88 entries, F06.14 42 rows; self-test 231 of 231 planted defects caught by name; req-tags 264 tags | `processor/head-013ee63/make_check.*` |
| `bash scripts/run_suites.sh` with `REQ_TAG_LOG` and `MAKEFLAGS=-j16` | `suites: 1030922 checks total, 0 failing`; pp_top 11,060 (round 2: 11,032), tx_arbiter 67 (66) | `run_suites.*`, `suites.txt`, `req-tags.txt` |
| `python3 scripts/check-req-tags.py --suites suites.txt --evidence req-tags.txt` | rc 0; 264 evidence lines, 14 suites (round 2: 262); REQ-FWX-001 14 lines | `check_req_tags_exec.*` |
| `make -C tb/pp_top reboot` | rc 0; RBT 155 checks, 0 failures | `reboot.*` |
| `bash scripts/lint_hdl.sh` under 5.052 and under the pinned 5.050 | rc 0 both; 41 modules LINT OK | `lint_hdl_5052.*`, `lint_hdl_5050.*` |
| `./syn/yosys/run.sh` (sv2v + yosys) | rc 0; every top, `protocol_processor_top` and `KL_aecp_engine` (Xilinx) OK | `yosys_run.*` |
| `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | rc 0; 93 checks, 0 FAIL | `elab_guards.*` |
| `python3 -B aecp_dispatch_mutants.py --jobs 8` | rc 0; 105 checks: 5 controls PASS, 100 arms KILLED (31 REBOOT); all 100 counts equal their README cells (`readme-counts.py`) | `campaigns/aecp-dispatch-013ee63/` |
| `python3 -B acmp_mutants.py --jobs 8` | rc 0; 101 of 101 KILLED, goldens PASS | `campaigns/acmp-013ee63/` |
| `python3 -B notify_mutants.py --jobs 8` | rc 0; 137 of 137 KILLED, goldens PASS | `campaigns/notify-013ee63/` |
| `python3 -B d3_mutants.py --jobs 8` (one complete run) | rc 0; 110 of 110 KILLED, goldens PASS | `campaigns/d3-013ee63/` |
| `python3 -B aecp_mutants.py --jobs 8` | rc 0; 67 checks PASS | `campaigns/aecp-013ee63/` |
| `python3 -B gsi_mutants.py --jobs 8` | rc 0; 30 detected by named checks, golden and restored PASS | `campaigns/gsi-013ee63/` |
| `make -C tb/elab_guards mutants JOBS=8 MUTANT_OUTPUT=<runs>/...` | rc 0; control PASS, 160 of 160 killed | `campaigns/elab-guards-013ee63/` |
| `python3 -B ctr_mutants.py --jobs 4` | rc 0; 18 checks PASS | `campaigns/ctr-013ee63/` |
| `make -C tb/aecp_cmds mutants MUTANT_OUTPUT=<runs>/...` | rc 0; 17 of 17 detected, golden and restored PASS | `campaigns/aecp-cmds-013ee63/` |
| `make -C tb/adp_engine mutants JOBS=8 MUTANT_OUTPUT=<runs>/...` | rc 0; 62 checks PASS | `campaigns/adp-engine-013ee63/` |
| `python3 -B name_wr_mutant.py` | rc 0; decode killed, golden and restored PASS | `campaigns/name-wr-013ee63/` |

Before the commits, on the same working tree:

- the focused run of the 31 REBOOT arms (`campaigns/rbt-arms-working-tree/`, `32 checks: 32
  PASS`), whose counts set the README cells;
- the reviewers' probes (`probes/reviewer-probes-working-tree/`);
- the `tb/tx_arbiter` plants (`processor/tx-arbiter-plants/`).

The full campaign at the head reproduces every one of those counts.

Memory: the owner cap was exceeded once, and I report it.

- `memory.peak` of this unit reads 12,480,049,152 bytes (12.48 GB), over the 12 GB cap. The
  highest 10 s sample was 11.97 GB, at 01:30. At that time `run_suites.sh` (`-j16`), the
  dispatch campaign (8 arms, 4 compile jobs each), the elab guards (`--jobs 4`) and yosys ran
  together.
- From 01:45 a governor (`tools/memgov.sh`) was in place: it stops the campaigns' process groups
  above 9 GB and resumes them below 7 GB. The arm compile cap was also cut to 1.
- From then on the highest sample was 8.59 GB. The governor never had to stop anything
  (`records/memory/memgov.log`). `memory.peak` cannot be reset (the write is ignored), so it still
  shows the earlier value (`records/memory/memory-peak.log`).

## Scratch-parent consumer gate

Scratch parent `<parent>`: the round-1 committed local clone of milan-fpga dev `1e80128f`, with push
URL `DISABLED-never-push`; it was never pushed. This round's commits on top of round 2's `8fb40ef0`:

| Parent commit | Content |
|---|---|
| `68d4cc3a` | gitlink protocol-processor -> `013ee63` (round 1's open `.reboot_req_o ()` stays) |
| `1c7c258f` | `./syn/yosys/ooc.sh --record-rom-digests` rows for `013ee63` (ucode `49a993be...`, ltn unchanged: the same as `ec1ff27`) |
| `b63bd18a` | `docs/reference/SUBMODULES.md` pin row; `submodule_boundaries.gen.py` regenerated (`--check` OK) |

Every consumer gate below ran at parent head `b63bd18a` (pin `013ee63`):

| Consumer gate | Result |
|---|---|
| Full sweep: `native-shards.py pp203-a699c-parent <spec> <out> 4 80-83 84-87 88-91 92-95` | `cpu_ranges.py pick` gave 80-95, the only free 16-CPU range. Like the other lane's sweep on the host, it was split 4 per shard. `SUITE_TIMEOUT=7200` (the script's own override) was in the spec from the start. Exit 0 in all four: 14 + 17 + 17 + 16 suites passed, 0 failed, 0 timed out, in 70 to 86 min (`parent/sweep-b63bd18a/`) |
| `scripts/suite_tally.py <the four log dirs> --expect-suite-root tb/verilator` | rc 0; 64 suites, each once; **2,191,694 checks, 0 in-suite failures** (`milan_dp` 13,757, `pp_shadow` 2,310, `nvm_cosim` 465, `capture_coherence` 21,721). Round 2 had the same total (`parent/full-tally/`) |
| 38 static and documentation gates (`parent/static-docs-b63bd18a/`), round 2's list (`tools/parent-all.list`) | all rc 0. `lint_rtl.py --check` passes with the open pin, `check_cpp_idiom.py` passes on the new bench C++, and `xvlog_gate.py --check` passes (an xvlog parse, not a route) |
| `./syn/yosys/ooc.sh --record-rom-digests` (`parent/rom-digests/`) | rc 0; rows for `013ee63`, digests equal to `ec1ff27`'s (no microcode change) |
| OOC area `./syn/yosys/ooc.sh KL_pp_shadow`, in its own unit (MemoryMax 10G) on this lane's CPUs 48-63, after the static gates | rc 0: 61,594 LUT / 4,332 LUTRAM / 28,341 FF / 15 RAMB36 / 4 RAMB18 / 10 DSP / 2,432 CARRY4. Dev `1e80128f` (round 1's receipt, same tools): 61,979 / 4,332 / 28,334 / 15 / 4 / 10 / 2,428, so **-385 LUT, +7 FF, +4 CARRY4**. Round-2 head: 61,722 LUT, 28,343 FF |

Findings for the adoption: none new. The four round-1 adoption steps still apply and are carried.
They are the open pin with its rationale, REBOOT in behave SERVED, the feature ledger, and the pin
documentation with the regenerated diagram.

Area: milan-fpga's AREA_BUDGET records 16 of 15,850 slices left on the shipping route. A Vivado
route at adoption decides; none was run here.

The shard clones `<lanes>/pp203-a699c-parent-shard0..3` are left in place, as `native-shards.py` made
them.

## STOP check

Not met; no STOP posted.

- The processor top's port list is unchanged in this round. `git diff ec1ff27 013ee63 --
  hdl/top/protocol_processor_top.sv` adds or removes no `input`, `output`, `inout`,
  `parameter` or `localparam` line (`records/processor-records.txt`).
- Over the whole PR (`f65c8ff7..013ee63`) the only top-level change is the authorised
  `reboot_req_o`. There is no register-map change.
- The new port `busy_o` belongs to the internal module `KL_pp_tx_arbiter`. It is connected at the
  top's instance (`arb_busy_w`) and in the `tb/tx_arbiter` harness, the only two instances. The
  parent instantiates neither. The tap `dbg_rbt_tx_open_o` is the bench wrap's.

## Acceptance items (round 3, and rounds 1 and 2 kept)

| Item | Met by |
|---|---|
| R731-F1 = R732-F3: the request rises only after the last frame the processor started has completed at the MAC face (its EOF handshake), with and without a DEPARTING | RB_DEP waits for the arbiter's `busy_o` (changes 1 to 3). RBT12 and RBT13 (not advertising) and RBT6, RBT9 and RBT11 (advertising): the request after the frame's last byte, held at the MAC. Reviewer probes PRB-NA, PRB-ADV and the non-advertising probe pass at the head |
| No new frame starts after that point | the exit is taken with the gate closed and ADP's queue empty; RBT12 and RBT13 `no byte is offered on tx_* from the rise through 5000 ms to the reset` (`tx_offer_t` = the held frame's last byte); RBT9 and RBT10 unchanged through 75 s and 65 s |
| The SUCCESS response and the notifications stay first (IEEE 1722.1-2021 §7.4.43, §7.5.2) | RB_RESP and RB_NTF unchanged; RBT6, RBT8 and RBT9 order checks; RBT12 and RBT13 `the SUCCESS response, the notification, then that frame, and no ENTITY_DEPARTING` |
| Each reviewer's probe a permanent check: a non-advertising REBOOT with another producer's frame in flight, plus backpressure on its EOF | RBT12 (R731: the lock-expiry notification) and RBT13 (R732: the listener's frame, every slot taken), each with the MAC holding that frame's last byte 20 ms |
| Each needs a planted defect that raises the request early | `rbt-last-frame-unwatched` (named by RBT12) and `rbt-last-byte-offered` (named by RBT13), both KILLED; each also fails the other row |
| R732-F4: PR-BODY validation figures at the final head | PR-BODY.md: every figure is from this head's runs; earlier rounds are listed as superseded, and the author source and scratch-consumer evidence is kept apart from the manager's candidate |
| Keep RBT1 to RBT8, the all-frame quiet assertion and every round-2 gate rc 0 | RBT 155 checks, 0 failures (RBT1 to RBT11 included). Every round-2 gate and campaign was re-run at the head, all rc 0 ("Gates run"). Two round-1 arms were re-targeted to the open-gate checks, with their plants unchanged |
| R732-F2, R731's suggestions | F2 resolved in round 2. R731-S1 (register the request, or state its clock domain) and R731-S2 (the RX discard has no wire effect) are not in this round's assignment; the PR body's open risks say the request is a `clk_i`-domain decode |
| The issue's items (rounds 1 and 2) | unchanged and still graded at this head: RBT1 to RBT11, the 29 round-1 and round-2 REBOOT arms (two re-targeted, one renamed), the consumer gate |

Every acceptance item is met, so PR-BODY.md carries "Closes #203".

## Not done (by the assignment's rules)

- No push, no PR creation or edit, no merge or rebase, no force, and no edit of any issue or PR
  comment. On #203 the only posts this round are TAKEN and REVIEW READY.
- No hardware or bench access, no flashing, and no Vivado route. The scratch parent's push URL is
  disabled and it was never pushed.
- Sub-agents were not used.
- R731-S1 and R731-S2 are suggestions outside this round's assignment, so neither was implemented.
  R731-S1 asks to register `reboot_req_o`, or to state its `clk_i`-domain sampling. The PR body's
  open risks say it is a `clk_i`-domain decode, to be synchronized by an asynchronous consumer.

## Receipts

- Everything cited is under `receipts/`.
- Every directory has an `INDEX.md` listing every file in it and below it, with bytes and a
  truncated sha256, generated from the files present (`receipts/tools/index.py`). The output
  directory's own `INDEX.md` covers this file and PR-BODY.md too.
- Host paths are replaced by placeholders (`<work>`, `<work2>`, `<clone>`, `<runs>`,
  `<parent-runs>`, `<parent>`, `<shard>`, `<lane>`, `<tools>`, `<tool>`, `<scratch>`, `<mgmt>`,
  `<home>`, `<tsn-gen>`, `<data>`).
- A file over 200 KB, or a binary, is not copied: it is listed with its size and full sha256 in
  a `RAW-RECORDS.txt` beside the copies.

| Directory | Holds |
|---|---|
| `records/` | `processor-records.txt` (origin, base, head, tree, commits and bodies, diff stats, no top port/parameter change, the clean lane), `parent-records.txt` (scratch parent commits, gitlinks, push URL, the open pin), `memory/` (the 10 s samples, the governor's log, the `memory.peak` record) |
| `processor/head-013ee63/` | `make check`, `run_suites` (`suites.txt`, `req-tags.txt`), the executed `check-req-tags`, section RBT alone, lint (5.052 and 5.050, with `*.version`), yosys, elab guards |
| `processor/tx-arbiter-plants/` | the `tb/tx_arbiter` control and plants M1 to M7 (`SUMMARY.txt` and one log each) |
| `campaigns/<driver>-013ee63/` | one per campaign in "Gates run": cmd, log, rc, start/end, memory samples, per-arm output |
| `campaigns/rbt-arms-working-tree/` | the focused run of the 31 REBOOT arms before the commits (`32 checks: 32 PASS`) |
| `probes/reviewer-probes-013ee63/`, `probes/reviewer-probes-working-tree/` | R731's window probe and R732's two probes, unchanged, at the head and on the working tree before the commits |
| `parent/` | `sweep-b63bd18a/` (spec, launch, four shards' logs and records), `full-tally/`, `static-docs-b63bd18a/` (38 gates, `SUMMARY.txt`), `rom-digests/` (and the diagram generator's log), `ooc-area/` (head, and dev's from round 1) |
| `tools/` | the scripts that ran the gates and wrote the receipts: `gate.sh`, `camp.sh`, `withmem.sh`, `memguard.sh`, `memgov.sh`, `vl-j4/verilator`, `mkpatch.py` (it cut the arm patches), `patchcheck.sh`, `run-review-probes.py`, `txarb-plants.py`, `readme-counts.py`, `parent_static.sh` and its list, `index.py`, and `runners/`. The scrubber that copied the receipts is not included, since its rule table is host paths |
