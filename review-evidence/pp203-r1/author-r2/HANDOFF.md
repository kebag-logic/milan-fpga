# [A699b] processor #203 round 2 handoff: silence from the final ENTITY_DEPARTING to reset

Status: REVIEW READY at head `ec1ff27`. Code, tests, arms and docs are committed. Every gate and
campaign below finished with rc 0. Two runs needed a second attempt, both recorded below: the
elab-guards campaign's first attempt was refused at setup, and the parent shards' first run hit the
wall clock under contention. Every planted arm was KILLED. The scratch-parent consumer gate passes
with `reboot_req_o` unconnected. The STOP condition was not met. Not pushed. PR-BODY.md is ready.

## Assignment

- Round 2 is the latest [A10] comment on issue #203 (issuecomment-6503153894). It asks for a fix
  of R732-F1 (MAJOR: a terminal transmit-quiet state after the final DEPARTING) and R732-F2
  (RESIDUE: the port comment heading).
- Review R732-1 was NEGATIVE on PR #209 (issuecomment-6503147824). Its probe counts every frame
  after the last DEPARTING: three automatic-unlock LOCK_ENTITY notifications went out while
  `reboot_req_o` was held.
- TAKEN posted: issuecomment-6503306390. REVIEW READY posted with head `ec1ff27`:
  issuecomment-6510359081. These two are this round's only posts.

## Base and head

- Repository: processor (protocol-processor-control-plane-avb-milan), branch `203-aecp-reboot`.
  `git remote get-url origin` was checked before the first commit, and so was HEAD = round-1 head
  `1be824f` (its base, main `f65c8ff7`, is an ancestor).
- Base: main `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8`. Round-1 head:
  `1be824fccbda5d3341737f5fe033d60edd27af57`.
- **Head: `ec1ff275a72d885f0908fd213d8009e9e4dda4d9`**. Three commits on top of `1be824f`, no
  rebase, no force, not pushed. One-line subjects, no body, no trailers:

| Commit | Subject |
|---|---|
| `aede92e` | Cite REQ-FWX-001 in the reboot_req_o port heading (issue #203) |
| `9f4bba2` | Close every TX lane but ADP's from the last ENTITY_DEPARTING built until reset, and grade the silence through a delayed reset (issue #203) |
| `ec1ff27` | Say in the architecture and guides that nothing follows the final ENTITY_DEPARTING until reset (issue #203) |

## R732-F2 (RESIDUE)

`aede92e` is comment-only. It changes one line, `hdl/top/protocol_processor_top.sv:824`, to
`//! ---- REBOOT request (REQ-FWX-001; IEEE 1722.1-2021 §7.4.43; issue #203) ----`. The review
cites line 823, but the heading is line 824 at `1be824f` too (`git show 1be824f:... | grep -n`).
`git show --stat aede92e` is 1 file, +1 -1.

## R732-F1 (MAJOR): design

- **One gate at the TX arbiter.** Every control-plane frame of the processor goes through
  `u_tx_arbiter`'s eight lanes (AECP solicited, AECP unsolicited, ACMP listener, ADP, SRP, talker
  responses, MAAP, originator), and `tx_*` has no other source. The gate masks the arbiter's
  requests: `arb_req_w = arb_want_w & rbt_tx_open_w`. A masked request is never granted. The
  arbiter only decides which frame starts, and it never truncates one. So no frame is cut, and a
  frame already started is sent whole.
- **When it closes.** `rbt_quiet_w = (RB_DEP && !adp_tx_busy_w) || RB_REQ`, which is the clock
  ADP has built and queued its last ENTITY_DEPARTING. From then until `rst_n`, only ADP's lane is
  open. ADP's enable fell for good at RB_DOWN (the round-1 SHUTDOWN), so ADP builds nothing more
  (`KL_adp_engine`: `pend_avail` is set only in DELAY, `pend_dep` only on the enable's fall). Its
  busy flag therefore only falls, and the condition holds once met. Nothing follows the final
  DEPARTING until reset.
- **Why not at the SHUTDOWN (RB_DOWN).** That was the first cut, and its 75 s test passed. But a
  producer held at the gate keeps the shared TX slot its frame waits in. The originator's timer
  arms only when its frame reaches the serializer, so that slot is held forever. ADP builds its
  DEPARTING into the same four standard slots. Closed at the SHUTDOWN, the frames already waiting
  can hold every slot, and then no DEPARTING and no request ever come. RBT11 builds exactly that
  case. The arm `rbt-quiet-at-the-shutdown` (the first cut) deadlocks there: 0 DEPARTING, no
  request. While ADP builds, every lane stays open, so the waiting frames drain ahead of the
  DEPARTING, the same liveness as round 1.
- **Required frames kept.** The SUCCESS response is granted before the acceptance. The
  notifications are all out before RB_DOWN (RB_NTF, round 1). The DEPARTINGs are ADP's, and ADP's
  lane is never closed. The arms `rbt-quiet-closes-departing` and `rbt-quiet-closes-notifications`
  show that a gate suppressing either is caught.
- **Covers every producer.** The gate closes the producers that run on their own: AECP
  unsolicited (lock expiry, every notification, DEREGISTER), the originator (CONTROLLER_AVAILABLE),
  the listener (its probes), MAAP and SRP. ADP is covered by its fallen enable. The answering lanes
  (AECP solicited, talker responses) are closed too, and in any case get no command after the
  acceptance (the round-1 RX frame gate and engine hold).
- **Not advertising.** There is no DEPARTING to build, so the gate closes in RB_DEP's first clock.
  That is two clocks after the notification round is seen done (RB_NTF's last clock, RB_DOWN). A
  frame granted in those two clocks still goes, after the last notification (06 §6.11 says so).
- **Held request.** It is unchanged: RB_REQ has no exit but `rst_n`.

## Changes (file:line at head, clause)

| # | File:line | Change | Clause / item |
|---|---|---|---|
| 1 | `hdl/top/protocol_processor_top.sv:824` | R732-F2 heading | REQ-FWX-001 (owner's source-comment rule) |
| 2 | `hdl/top/protocol_processor_top.sv:833` | port comment: once the DEPARTINGs are built no frame starts but theirs, and after the last none until `rst_n`; no notification, lock expiry, CONTROLLER_AVAILABLE, ACMP probe, MAAP or SRP frame follows | R732-F1; REQ-FWX-001; #203 acceptance item 3 |
| 3 | `hdl/top/protocol_processor_top.sv:4583`, `:4674`, `:4688` | `arb_want_w` (each lane's own request), `rbt_tx_open_w`; `arb_req_w = arb_want_w & rbt_tx_open_w` | R732-F1 "covers every producer", "frame integrity" |
| 4 | `hdl/top/protocol_processor_top.sv:4855` (banner and the gate's comment, `:4872`), `:4918`, `:4920`, `:4923` | the transmit gate: `rbt_quiet_w` from the last DEPARTING built to the reset; `rbt_tx_gate` opens ADP's lane alone | REQ-FWX-001; IEEE 1722.1-2021 §7.4.43, §7.5.2, §6.2.4, §6.2.5.2.2; Milan v1.2 §5.6.3.3, §5.6.3.5.8, §5.6.3.5.11 |
| 5 | `docs/architecture/06_aecp_engine.md:1111` ("Silence until the reset") and the RBT paragraph after it; `:1490` §8.1 row | the gate, when it closes and why, the slot argument, the not-advertising case, the tests | same |
| 6 | `docs/architecture/03_packet_engine.md:494` | F03.5 rule row "REBOOT gate" | same |
| 7 | `docs/architecture/02_interfaces.md:138` (reset rule 6), `:582` (F02.10 `reboot_req`) | no frame from the final DEPARTING to `rst_n` | same |
| 8 | `docs/architecture/04_adp_engine.md:166` | once the DEPARTINGs are built the arbiter starts no other lane's frame | same |
| 9 | `docs/guides/integrator.md:588` (status table), `:697` (bring-up step 7) | the R732-F1 contradicted claim ("nothing left to send") is now true and stated | R732-F1 docs |
| 10 | `docs/guides/operator.md:52` | REBOOT row: no frame, MAAP and SRP included, until reset | R732-F1 docs |
| 11 | `docs/00_MILAN_COMPLIANCE_REVIEW.md:316` (GAP-13), `:556` (REQ-FWX-001 row) | the silence, and "transmit gate" in the realization cell | REQ-FWX-001 |
| 12 | `tb/pp_top/pp_top_wrap.sv:301`, `:833` | tap `dbg_arb_want_o` = `u_dut.arb_want_w` (each lane's request ahead of the gate) | test observability |
| 13 | `tb/pp_top/sim_main.cpp:1000` to `:1010`, `:1605`, `:1690` to `:1700`, `:1713` | harness: MAC stalls at the DEPARTING's and the REBOOT notification's last byte; `tx_offer_t` (last clock `tx_valid_o` was 1); `tx_torn` (a byte outside a sof-to-eof frame); `arb_want_held` (lanes that asked while the request read 1) | R732-F1 verification |
| 14 | `tb/pp_top/sim_main.cpp:12600` and RBT6/RBT7 (`:12689`) | the engine's own command count; RBT7's queued command and ACMP commands while the response is held | keeps the frame gate and engine hold graded where the transmit gate cannot hide them |
| 15 | `tb/pp_top/sim_main.cpp:12789` to `:13060` | RBT9, RBT10, RBT11 (below) | R732-F1 verification |
| 16 | `tb/pp_top/aecp_dispatch_mutants.py:116` and `tb/pp_top/aecp_dispatch_mutations/rbt-quiet-*.patch`, `rbt-adp-reenabled.patch` (13 new) | the gate's arms; two round-1 arms renamed to new checks | R732-F1 "a planted defect ... must fail it" |
| 17 | `tb/pp_top/README.md:1425` (arm table, every REBOOT count re-measured), `:1497`, `:2659` to `:2700` (section RBT) | RBT7, RBT9 to RBT11, and the arms | docs |

## New checks, planted arms and failing words

Section RBT now has 127 checks, 0 failures at the head (`make -C tb/pp_top reboot`). Round 1 had
79 checks.

| Check | What it grades |
|---|---|
| RBT6 `the engine takes the REBOOT and no command after it` | `dbg_aecp_cmd_o` moves by 1 from before the REBOOT to the end of RBT6 |
| RBT7 `the command queued behind the held REBOOT is never served`, `... the engine takes ...`, `ACMP commands that arrive while the response is held get no answer` | while the MAC holds the SUCCESS response's last byte, every lane is still open. A command let in by a dropped frame gate or engine hold would leave the moment the byte is released |
| RBT9 (75 s), the all-frame assertion | internal MAAP, SRP, the requester's lock (expires 400 ms on), three registered controllers, sink 1 bound to a discovered talker. AVB-info, path, grandmaster and counter changes come every 5 s; AEM, ACMP (talker and listener) and ADP commands at 5 s; a link bounce at 40 s. The MAC holds the DEPARTING's last byte 1.5 s (request 0 meanwhile). Graded: SUCCESS, notifications and DEPARTING byte-exact and in order, then `RBT9 no byte on tx_* after the final ENTITY_DEPARTING` (no frame, and `tx_offer_t` equals the DEPARTING's last byte). Also every byte in a whole frame, the request held, the lock expired, and lanes AECP-unsolicited, listener, MAAP and SRP each asked to send. Then the delayed reset: request 0, and the entity advertises again |
| RBT10 (65 s) | three controllers' CONTROLLER_AVAILABLE probes fall due and RBT9's commands arrive at 5 s: `RBT10 no byte on tx_* after the final ENTITY_DEPARTING`, the originator asked to send. A held producer keeps its slot, and RBT9's take every slot before a probe (or ADP, or the talker) could build, so this producer has its own window |
| RBT11 | eight sinks probing and the lock expiring while the MAC holds the REBOOT notification's last byte 5 s: no standard slot free at the release (`dbg_txs_free_o - dbg_txs_slot4_free_o == 0`), yet `RBT11 ENTITY_DEPARTING still leaves, then reboot_req_o`, byte-exact, and nothing after it |

Arms (target `reboot`), each KILLED by its named check at the head. The last column is the
number of failing checks. Each equals its README cell, in the focused run (`rbt-arms-9f4bba2-tree`,
`31 checks: 31 PASS, 0 FAIL`) and in the full campaign at the head (`aecp-dispatch-ec1ff27`).

| Arm | Plant | Named failing words | Failing checks |
|---|---|---|---|
| `rbt-quiet-gate-dropped` | `rbt_tx_open_w` all ones | `RBT9 no byte on tx_* after the final ENTITY_DEPARTING` (211 frames) | 3 |
| `rbt-quiet-from-the-request` | gate only in RB_REQ | same (1 frame: a waiting listener probe at the clock after the held DEPARTING) | 1 |
| `rbt-quiet-opens-notifications` | AECP unsolicited lane let through | same (15 frames) | 2 |
| `rbt-quiet-opens-originator` | originator lane let through | `RBT10 no byte on tx_* after the final ENTITY_DEPARTING` (6 frames) | 1 |
| `rbt-quiet-opens-listener` | listener lane let through | RBT9 (13 frames) | 2 |
| `rbt-quiet-opens-maap` | MAAP lane let through | RBT9 (2 frames) | 1 |
| `rbt-quiet-opens-srp` | SRP lane let through | RBT9 (4 frames) | 3 |
| `rbt-adp-reenabled` | `rbt_adp_off_w` without RB_REQ: ADP advertises again | RBT10 (7 ENTITY_AVAILABLE) | 2 |
| `rbt-quiet-opens-talker-answers` | talker lane let through, frame gate removed | RBT10 (1 frame) | 2 |
| `rbt-quiet-opens-aecp-answers` | AECP solicited lane let through, frame gate and engine hold removed | RBT9 | 10 |
| `rbt-quiet-at-the-shutdown` | gate closed at RB_DOWN (the first cut) | `RBT11 ENTITY_DEPARTING still leaves, then reboot_req_o` (0 DEPARTING, rise -1) | 2 |
| `rbt-quiet-closes-departing` | ADP's lane closed too | `RBT6 one ENTITY_DEPARTING` | 22 |
| `rbt-quiet-closes-notifications` | gate closed from RB_NTF | `RBT6 the REBOOT notification reaches every other registered controller` | 28 |

Renamed (round-1 arms, same plant). `rbt-rx-gate-dropped` is now named by `RBT7 ACMP commands that
arrive while the response is held get no answer` (1). `rbt-engine-hold-dropped` is now named by
`RBT6 the engine takes the REBOOT and no command after it` (5). With the transmit gate, RBT6's
answers to commands after the request reach no wire, and in the focused run both old names were
UNPROVEN (`rbt-arms-first-gate-run`). Every other round-1 REBOOT arm keeps its plant and name. Its
count was re-measured (RBT9 to RBT11 add failures under several).

No arm exempts the AECP-solicited or the talker-response lane alone. Both are behind the round-1
command gates (RX frame discard from the acceptance, engine hold), which have their own arms, so
exempting either lane alone changes nothing on the wire. The two `opens-*-answers` arms drop those
gates as well, and they show that the all-frame assertion sees an answer.

## Gates run

Every gate ran in a disposable clone of `ec1ff27` (`<work>`: the head clone, a separate sweep clone and
a campaign clone), and every rc is the command's own status. Campaign arm builds used the host's
Verilator 5.052 through a wrapper that only rewrites `--build -j 0` to `-j 4`
(`receipts/tools/vl-j4/verilator`), with `TMPDIR` on disk. Both keep concurrent arms inside the unit's
memory: `/tmp` is a tmpfs charged to it. Round 1 used the same Verilator.

| Gate | Result |
|---|---|
| `make check` (PATH with the mermaid CLI) | rc 0; aecp commands 32 commands, F06.14 42 rows; self-test 231 of 231 planted defects caught |
| `bash scripts/run_suites.sh` with `REQ_TAG_LOG` and `MAKEFLAGS=-j16` | rc 0; `suites: 1030893 checks total, 0 failing`; pp_top 11,032 (round 1: 10,984; RBT 127 against 79) |
| `python3 scripts/check-req-tags.py --suites suites.txt --evidence req-tags.txt` | rc 0; 262 evidence lines (round 1: 259), 14 suites; REQ-FWX-001: 12 lines |
| `make -C tb/pp_top reboot` | rc 0; 127 checks, 0 failures |
| `bash scripts/lint_hdl.sh` under Verilator 5.052 and under the pinned 5.050 (`*.version` receipts) | rc 0 both; 41 modules |
| `./syn/yosys/run.sh` (sv2v + yosys) | rc 0; every top, `protocol_processor_top` and `KL_aecp_engine` (Xilinx) OK |
| `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | rc 0; 93 checks, 0 FAIL |
| `python3 -B aecp_dispatch_mutants.py --jobs 2` | rc 0; 104 checks: 5 controls PASS, 99 arms KILLED (30 REBOOT, 13 new); all 99 failing-check counts equal their README cells (compared by script) |
| `python3 -B aecp_mutants.py --jobs 2` | rc 0; 67 checks PASS |
| `python3 -B d3_mutants.py` in two parts: part 1 `--jobs 2` (38 arms, stopped by me so part 2 could run at `--jobs 4`), part 2 `--jobs 4 --only` the other 72 | part 2 rc 0, "72 of 72 KILLED by their named checks; goldens PASS". `d3-UNION.txt` (`d3_union.py`, the driver's arm list by import): 110 of 110 arms KILLED exactly once, the six goldens PASS in both parts. Part 1 has no rc of its own |
| `python3 -B notify_mutants.py --jobs 2` | rc 0; 137 of 137 KILLED, goldens PASS |
| `python3 -B ctr_mutants.py --jobs 1` | rc 0; 18 checks PASS |
| `python3 -B acmp_mutants.py --jobs 2` (one run) | rc 0; 101 of 101 KILLED, goldens PASS |
| `python3 -B gsi_mutants.py --jobs 2` | rc 0; "30 detected by named checks; golden and restored PASS" |
| `python3 -B name_wr_mutant.py` | rc 0; "decode killed; golden and restored PASS" |
| `make -C tb/elab_guards mutants MUTANT_OUTPUT=<runs>/...` | rc 0; control PASS, 160 of 160 killed. The first attempt, plain `make mutants`, was refused at setup (rc 2, "refusing to write into the existing /tmp/elab-guard-mutants", a directory another run on the host left; not touched). It is kept as `refused-attempt/` |
| `make -C tb/aecp_cmds mutants` | rc 0; 17 of 17 detected, golden and restored PASS |
| `make -C tb/adp_engine mutants JOBS=2` | rc 0; 62 checks PASS |

The aecp_cmds and adp_engine benches compile no file round 2 changed. They were re-run anyway,
because every round-1 gate was to stay rc 0.

Memory: the unit's `memory.peak` reached 11.87 GB once (21:34). That is over the 10 GB working
target and under the 12 GB cap. At that moment anonymous memory was 8.1 GB and reclaimable page
cache 2.6 GB, from eleven concurrent arm builds. From then on, a watchdog
(`receipts/tools/memguard.sh`, log in `records/memory/`) reclaimed page cache above 7.5 GB, and
MemoryCurrent stayed at or under 8.68 GB (anonymous at or under 7.64 GB).

Observation probes at the round-1 head (`receipts/probes/`, not gates). RBT6 was patched to keep
the run 70 s after the request and to print every frame after the DEPARTING (`probe.patch`). With
the unchanged stimulus there were 86 frames: the lock's three unlock notifications (the review's
finding), SRP every second, CONTROLLER_AVAILABLE and DEREGISTER. With MAAP, a bound sink and
integrator changes added there were 136, MAAP and the listener included. This set the list of
producers RBT9 to RBT11 had to exercise.

## Scratch-parent consumer gate

Scratch parent `<parent>`, the round-1 committed local clone of
milan-fpga dev `1e80128f` (push URL `DISABLED-never-push`, never pushed). Round-2 commits on top of
round-1 `ab0b9185`:

| Parent commit | Content |
|---|---|
| `44b9c12f` | gitlink protocol-processor -> `ec1ff27` (the open `.reboot_req_o ()` of round 1 stays) |
| `3138e758` | `./syn/yosys/ooc.sh --record-rom-digests` rows for `ec1ff27` (ucode `49a993be...`, ltn unchanged: same as `1be824f`) |
| `8fb40ef0` | `docs/reference/SUBMODULES.md` pin row; `submodule_boundaries.gen.py` regenerated (`--check` OK) |

Every consumer gate below ran at parent head `8fb40ef0` (pin `ec1ff27`):

| Consumer gate | Result |
|---|---|
| Full sweep: `native-shards.py pp203-a699b-parent <spec> <out> 4 48-51 52-55 56-59 60-63`. `cpu_ranges.py pick` found no free range (the host was fully booked), so the shards ran on this lane's own 16 CPUs, as prior lanes did | first run: 0 in-suite failures in all four, but each shard had suites killed by the wall clock under contention with this unit's campaigns (exit 92 "result unknown"): shard 0 `milan_dp`, shard 1 `milan_dp_render`, shard 2 `capture_coherence` and `maap`, shard 3 `media_phase` and `mmcm_servo` (`sweep-8fb40ef0/contended-first-run/`) |
| Each shard re-run whole, same clone and spec, with `SUITE_TIMEOUT=7200` (the script's own override for contention), one unit per shard on its own CPUs | exit 0 all four: 14 + 17 + 17 + 16 suites passed, 0 timed out (`sweep-8fb40ef0/rerun/`) |
| `scripts/suite_tally.py <the four re-run log dirs> --expect-suite-root tb/verilator` | rc 0; 64 suites, each once; **2,191,694 checks, 0 in-suite failures** (`milan_dp` 13,757, `pp_shadow` 2,310, `nvm_cosim` 465, `capture_coherence` 21,721). Round 1 had the same total |
| 38 static and documentation gates (`static-docs-8fb40ef0/`): port contracts (+selftest), wire accountability, SV/C++/Python idiom (+selftests), RTL source lists (+selftest), `pp_srcs.py --check --selftest`, hygiene (+selftest), TODO ownership (+selftest), doc paths, `lint_rtl.py --check` and `--self-test`, entity shape self-test, behave, `syn/yosys/run.sh --mode elaborate` of `milan_datapath`, `KL_pp_shadow`, `KL_gptp_shadow`, `xvlog_gate.py --check`, `check_feature_status.py` (+self-test), `docs_check.py`, `check_doc_style.py`, `check_em_dash.py --base 1e80128f`, `submodule_boundaries.gen.py --check` (+selftest), `DOC_MAP.gen.py --check` (+selftest), `gen_module_matrix.py --check`, `check_submodule_docs.py`, `check_diagram_pngs.py`, `check_solution_docs.py`, `check_sh_idiom.py`, `check_soc_sources.py` | all rc 0. `check_cpp_idiom.py` passes on the new tb C++, and `lint_rtl.py --check` passes with the round-1 open pin |
| `./syn/yosys/ooc.sh --record-rom-digests` (`rom-digests/`) | rc 0; rows for `ec1ff27`, digests equal to `1be824f`'s (no microcode change) |
| OOC area `./syn/yosys/ooc.sh KL_pp_shadow` (own unit) | rc 0: 61,722 LUT / 4,332 LUTRAM / 28,343 FF / 15 RAMB36 / 4 RAMB18 / 10 DSP / 2,432 CARRY4. Dev `1e80128f` (round 1's receipt, same tools): 61,979 / 4,332 / 28,334 / 15 / 4 / 10 / 2,428, so **-257 LUT, +9 FF, +4 CARRY4**. Round-1 head: 61,878 LUT, the same FF and CARRY4 |

Findings for the adoption: none new. The four round-1 adoption steps still apply and are carried
(the open pin with its rationale, REBOOT in behave SERVED, the feature ledger, and the pin
documentation with the regenerated diagram). Area: milan-fpga's AREA_BUDGET records 16 of 15,850
slices left on the shipping route. yosys shows this change neutral, but a Vivado route at adoption
decides; none was run here (no route beside the sweeps).

## STOP check

Not met; no STOP posted. The top-level port list is unchanged from round 1:
`git diff 1be824f ec1ff27 -- hdl/top/protocol_processor_top.sv` adds no `input`, `output` or
`parameter` line (`records/processor-records.txt`). Over the whole PR the only top-level change is
the authorised `reboot_req_o`. There is no register-map change. No new module port either: the gate
is internal to `protocol_processor_top`, and the new tap `dbg_arb_want_o` is the bench wrap's.

## Acceptance items (round 2 and the issue)

| Item | Met by |
|---|---|
| R732-F1: terminal transmit-quiet state after the notifications and the final DEPARTING, lasting until reset | the gate (changes 3, 4); RBT9 and RBT10 (no byte after the final DEPARTING through 75 s and 65 s); after the delayed reset the entity advertises again |
| covers every producer: AECP unsolicited and lock expiry, ADP, ACMP, MAAP, SRP | one gate on all eight arbiter lanes; ADP by its fallen enable. RBT9/RBT10 positive controls: the unsolicited AECP lane, the originator, the listener, MAAP and SRP each asked to send; the lock expired. Arms `rbt-quiet-opens-{notifications,originator,listener,maap,srp}`, `rbt-adp-reenabled` KILLED |
| frame integrity kept | gate on requests only, never on bytes. RBT9: `tx_torn` 0, `tx_offer_t` = the DEPARTING's last byte (nothing offered, whole or part), the held DEPARTING leaves whole and byte-exact |
| held request kept | RB_REQ unchanged; RBT6 and RBT9 to RBT10 held-level checks; `rbt-request-pulse` KILLED |
| none of the required shutdown frames suppressed | RBT6/RBT8/RBT9 byte-exact SUCCESS, notifications and DEPARTING, in order; RBT11 with every TX slot taken; arms `rbt-quiet-closes-departing`, `rbt-quiet-closes-notifications`, `rbt-quiet-at-the-shutdown` KILLED |
| an all-frame assertion from the final DEPARTING through a delayed reset, exercising lock expiry, asynchronous notifications, pending work and the autonomous producers | RBT9 (and RBT10 for CONTROLLER_AVAILABLE): lock expiry, AVB-info/path/grandmaster/counter changes, a command queued behind the REBOOT, commands in the window, the listener's exchange, the CA exchange and its DEREGISTER, MAAP, SRP, a link bounce |
| a planted defect that reopens any one producer or the terminal gate must fail it | the 13 gate arms above, each KILLED by its named check. Exempting an answering lane alone is not an arm because the command gates stand in front of it; with those dropped, it is (`opens-*-answers`) |
| RBT1 to RBT8 and every round-1 gate stay rc 0 | "Gates run": RBT 127 checks, 0 failures; every round-1 gate and campaign re-run at the head, rc 0; two round-1 arms renamed to checks that still see their defect |
| R732-F2: the port heading | `aede92e`, comment-only |
| the issue's items (round 1: statuses, DEPARTING, request after transmit-done, no further command, level documented, REQ-FWX-001/GAP-13/model/compliance entry, tests and the early-request mutant, parent consumer gate, only `reboot_req_o`) | unchanged and still graded (round-1 handoff), RBT1 to RBT8 and the 17 round-1 arms at this head |

Every acceptance item is met, so PR-BODY.md carries "Closes #203".

Not covered, by construction only: a two-interface REBOOT (`P-N-AVB-INTERFACES` = 2) is not run in
RBT. ADP's busy flag covers every pending DEPARTING, so the gate closes after the last interface's
is built.

## Not done (by the assignment's rules)

No push, no PR creation or edit, no merge or rebase, no force, no edit of any issue or PR comment.
On #203 the only posts are TAKEN and REVIEW READY. No hardware or bench access, no flashing, and no
Vivado route. The scratch parent's push URL is disabled and it was never pushed. Sub-agents were not
used.

## Receipts

Everything cited is under `receipts/`. Each directory has an `INDEX.md` listing every file in it and
below it, with bytes and a truncated sha256, generated from the files present (`receipts/tools/index.py`).
Host paths are replaced by placeholders (`<work>`, `<runs>`, `<parent>`, `<lane>`, `<clone>`, `<tool>`,
`<scratch>`, `<tmp>`, `<mgmt>`, `<home>`). A file over 200 KB, or a binary, is not copied: it is
listed with its size and full sha256 in a `RAW-RECORDS.txt` beside the copies.

| Directory | Holds |
|---|---|
| `records/` | `processor-records.txt` (origin, base, head, tree, commits, diff stats, no port/parameter change, clean lane), `parent-records.txt` (scratch parent commits, gitlinks, push URL, the open pin), `memory/` (the watchdog's log) |
| `processor/head-ec1ff27/` | `make check`, `run_suites` (`suites.txt`, `req-tags.txt`), the executed `check-req-tags`, section RBT alone, lint (5.052, 5.050), yosys, elab guards |
| `campaigns/<driver>-ec1ff27/` | one per campaign in "Gates run": command, log, rc, start/end, memory samples, per-arm output; `d3-ec1ff27/d3-UNION.txt` |
| `campaigns/rbt-arms-9f4bba2-tree/` | the focused run of the 30 REBOOT arms on `9f4bba2`'s tree (`31 checks: 31 PASS`) |
| `campaigns/rbt-arms-first-gate-run/` | the first focused run, on the first gate cut (closed at RB_DOWN), where `rbt-rx-gate-dropped`, `rbt-engine-hold-dropped`, `rbt-adp-reenabled` and `rbt-quiet-opens-talker-answers` were UNPROVEN by their then names, which led to the renames and RBT10's commands |
| `probes/` | the observation probes at the round-1 head |
| `parent/` | `sweep-8fb40ef0/` (spec, launch, contended first run, re-runs), `full-tally/`, `static-docs-8fb40ef0/`, `rom-digests/` (and the diagram generator's log), `ooc-area/` (head, and dev's from round 1) |
| `tools/` | the scripts that ran the gates and wrote the receipts (`gate.sh`, `camp.sh`, `withmem.sh`, `memguard.sh`, `vl-j4/verilator`, `index.py`, `mkpatch.py` that cut the arm patches, `d3_union.py`, `sync.sh`, `parent_static.sh` and its list; the scrubber that copied the receipts is not included, since its rule table is host paths) |
