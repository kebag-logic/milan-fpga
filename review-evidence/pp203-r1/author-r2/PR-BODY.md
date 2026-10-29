[A699b] AECP REBOOT (IEEE 1722.1-2021 §7.4.43): answer SUCCESS, notify, send ENTITY_DEPARTING, hold reboot_req_o, then stay silent until reset

Closes #203

## What it does

A controller can REBOOT ENTITY 0 (IEEE 1722.1-2021 §7.4.43, Figure 7-68). The processor answers
SUCCESS, echoing the command's four bytes at cdl 16. It then tells the other registered controllers
and sends ENTITY_DEPARTING where the entity was advertising. Then it raises the one new top-level
output, `reboot_req_o`, a level held until `rst_n`. From the final ENTITY_DEPARTING until that
reset, it sends nothing at all, however long the reset is withheld. The reset itself, and what the
end station restores after it, are the integrator's (milan-fpga #787).

| Command | Answer (every answer is `{descriptor_type, descriptor_index}` at cdl 16) |
|---|---|
| cdl < 16, too short for Figure 7-68's four bytes | `BAD_ARGUMENTS` |
| any descriptor_type but ENTITY (this build has no MEMORY_OBJECT firmware image, §7.4.43.1's other target) | `NOT_SUPPORTED` |
| ENTITY at any index but 0 | `NO_SUCH_DESCRIPTOR` |
| ENTITY 0 under another controller's lock (§7.4.43.2, §7.4.2) | `ENTITY_LOCKED` |
| ENTITY 0, otherwise (a padded command included) | `SUCCESS` |

`ENTITY_ACQUIRED` (§7.4.43.2, §7.4.1) cannot arise: this entity is never acquired (Milan v1.2
§5.4.2.1, ACQUIRE_ENTITY is refused `NOT_SUPPORTED`), and a test shows it. The type and index
refusals come before the lock check, as START/STOP_STREAMING's do; neither standard orders them.

**The notification.** §7.4.43 says "On success this command also sends an unsolicited
notification". §7.5.2 lists REBOOT, and Milan v1.2 §5.4.5.2 makes it a SHALL to every registered
controller but the requester. It rides class 9 (the `{type, index}` body of START/STOP_STREAMING's
notification), with REBOOT's opcode in the job's first argument.

**Acceptance, and no further command.** The REBOOT is accepted at its SUCCESS response's TX grant.
A refusal, or a response the memory voided into `ENTITY_MISBEHAVING`, leaves the entity in service.
From the grant, the AECP engine takes no command from its queue, and the top discards, whole, every
frame that starts on `rx_*`.

**The request.** The top reads `tx_*` itself: a frame has left when the MAC takes its last byte. It
waits for three things in order. First, the SUCCESS response. Second, the notification round: no
command notification queued or running, and no unsolicited frame in flight. Third,
ENTITY_DEPARTING: ADP's effective enable falls for good, which is Milan v1.2's SHUTDOWN, and the top
waits until ADP has nothing left to build, queue or send. Then `reboot_req_o` rises. It does not
wait for persistence: an integrator that must keep a late change holds its reset until
`(|nvm_unflushed_o) | d3_unflushed_o` is 0.

**Silence until the reset.** A reset held back, for persistence or because `reboot_req_o` is not
wired, still leaves producers running on their own: the lock's automatic unlock and every other
notification, CONTROLLER_AVAILABLE, the listener's probes, MAAP and SRP. All control-plane TX goes
through one arbiter. From the clock ADP has built and queued its last ENTITY_DEPARTING until
`rst_n`, the top masks every arbiter request but ADP's. ADP, its enable fallen, builds nothing more.
A masked request is never granted and a started frame is never cut, so frames stay whole.

The gate waits for the DEPARTINGs to be built because a producer held at the gate keeps the TX slot
its frame waits in, and ADP builds into the same slots. A gate closed at the SHUTDOWN could leave no
slot for the DEPARTING, and then no DEPARTING and no request would ever come; a test fills every
slot to show this. Until the gate closes every lane drains, ahead of the DEPARTINGs. An entity that
was not advertising has no DEPARTING; its gate closes two clocks after the notification round, and
a frame granted in those two clocks still goes.

## Where ENTITY_DEPARTING comes from (the clause the issue asked for)

- Milan v1.2: §5.2 is the chapter's overview only. The requirement is §5.6.3: the SHUTDOWN event
  (§5.6.3.3), WAITING/SHUTDOWN (§5.6.3.5.8) and DELAY/SHUTDOWN (§5.6.3.5.11), each "Send an ADP
  ENTITY_DEPARTING message". Table 5.51 ignores SHUTDOWN in DOWN, so an entity that is not
  advertising sends none.
- IEEE 1722.1-2021: §6.2.1 introduces the Advertising Entity and Advertising Interface state
  machines. The send is `doTerminate` (§6.2.4.1.3, §6.2.5.1.1) and `txEntityDeparting()`
  (§6.2.5.2.2, Figure 6-3). §6.2.6 is the receiving controller's Discovery state machine, which
  removes the entity on `rcvdDeparting` (Figure 6-4).
- The figure: REBOOT's format is IEEE 1722.1-2021 Figure 7-68 (Figure 7-75 is AUTH_ADD_KEY).

## Changes

- `hdl/top/protocol_processor_top.sv` changes these: `reboot_req_o` (the only top-level change),
  the REBOOT sequence, the frame gate on `rx_*`, and ADP's effective enable. It also adds the
  transmit gate (`arb_req_w = arb_want_w & rbt_tx_open_w`) and makes REBOOT a `CFG_BARRIER` with
  the global key.
- `hdl/aecp/KL_aecp_engine.sv`: the opcode, the A_PLD-exit route to three new programs, the
  acceptance hold, and class 9's REBOOT command_type.
- `hdl/aecp/ucode/gen_ucode.py`: E_RBOOT, E_RBOOTNS and E_RBOOTBAD. `hdl/aecp/KL_aecp_notify.sv`
  `cmd_busy_o` and `hdl/adp/KL_adp_engine.sv` `tx_busy_o` are internal levels the sequence reads.
- The command model `hdl/aecp/ucode/aecp_commands.json` gains the REBOOT row. F06.14 and
  `tb/aecp_cmds/decode.json` are regenerated by their generators.
- Docs:
  - 06 §6.11 (with "Silence until the reset"), F06.9, §8.1 and F06.14.
  - The compliance review's GAP-13, REQ-FWX-001 and its F00.2 row.
  - 02 reset rule 6 and F02.10, the 03 F03.5 rule "REBOOT gate", and 04.
  - The integrator and operator guides, and diagram 21.
  - The `tb/pp_top` and `tb/aecp_cmds` READMEs.

## Tests and mutants

Section RBT in `tb/pp_top` (`make -C tb/pp_top reboot`; the default build runs it): 127 checks.

- RBT1 to RBT5: every refusal, byte-exact at cdl 16, each followed by no acceptance, no request and
  no notification, with the entity still in service. ACQUIRE_ENTITY is `NOT_SUPPORTED`.
- RBT6: the lock holder's REBOOT with three controllers registered. On the wire, in order: SUCCESS,
  the notification to the other two (none to the requester), one ENTITY_DEPARTING (each byte-exact),
  then the request, held. The engine's own command count moves by the REBOOT alone; AEM, ACMP and ADP
  commands after it go unanswered.
- RBT7: the MAC holds the SUCCESS response's last byte 30 ms. The request stays 0, and while every TX
  lane is still open, a command queued behind the REBOOT and ACMP commands arriving meanwhile get no
  answer.
- RBT8: not advertising, a padded command: SUCCESS at cdl 16, the notification, no DEPARTING, the
  request.
- RBT9 is the all-frame assertion through a reset withheld 75 s. The entity runs internal MAAP and
  SRP. Three controllers are registered, the requester's lock expires, and a sink is bound to a
  discovered talker. AVB-info, path, grandmaster and counter changes arrive every 5 s, commands
  arrive, and the link bounces. The MAC holds the DEPARTING's last byte 1.5 s, so requests wait when
  it leaves. From the final DEPARTING's last byte to the reset, the MAC is offered no byte at all. The
  unsolicited AECP lane, the listener, MAAP and SRP each asked the arbiter to send meanwhile. After
  the reset the request reads 0 and the entity advertises again.
- RBT10: the same silence while three CONTROLLER_AVAILABLE probes fall due (the originator asks to
  send). A held producer keeps its TX slot, so this producer needs a window of its own.
- RBT11: every standard TX slot is taken when the SHUTDOWN comes (eight sinks probing, the lock
  expiring, the MAC holding the notification 5 s). The DEPARTING still leaves, byte-exact, the request
  follows, and nothing follows the DEPARTING.

Thirty arms in `tb/pp_top/aecp_dispatch_mutants.py` (target `reboot`) are all KILLED by name, each
count equal to its README cell:

- Seventeen drop each wait, guard and route of the sequence. `rbt-request-at-acceptance` raises the
  request before the response is sent.
- Thirteen plant the transmit gate's defects:
  - the gate removed (`rbt-quiet-gate-dropped`), or closed only with the request;
  - each producer that runs on its own let through it (notifications, originator, listener, MAAP,
    SRP);
  - ADP's enable back on after the DEPARTING;
  - each answering lane let through with its command gates dropped;
  - the gate closed at the SHUTDOWN (it deadlocks in RBT11);
  - the gate closed on a required frame (the DEPARTING, the notifications).

Two round-1 arms keep their plant under new names. The frame gate is now named by RBT7 and the
engine's hold by its command count, because RBT6's late answers now reach no wire.

## Gates (all rc 0, at this head)

| Gate | Result |
|---|---|
| `make check` | every gate OK; AECP command gate 32 commands, F06.14 42 rows, self-test 231 of 231 |
| `bash scripts/run_suites.sh` with `REQ_TAG_LOG` | 1,030,893 checks, 0 failing (pp_top 11,032) |
| `python3 scripts/check-req-tags.py --suites ... --evidence ...` | 262 evidence lines, 14 suites |
| `make -C tb/pp_top reboot` | 127 checks, 0 failures |
| `bash scripts/lint_hdl.sh` (Verilator 5.052 and 5.050) | 41 modules clean |
| `./syn/yosys/run.sh`; `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | every top elaborates; 93 of 93 |
| `python3 tb/pp_top/aecp_dispatch_mutants.py` | 5 controls PASS, 99 of 99 arms KILLED (30 REBOOT); every count equals its README cell |
| `python3 tb/pp_top/aecp_mutants.py` | 67 of 67 |
| `python3 tb/pp_top/d3_mutants.py` (two parts, reconciled against the driver's arm list) | 110 of 110 KILLED, goldens PASS |
| `python3 tb/pp_top/notify_mutants.py` | 137 of 137 KILLED, goldens PASS |
| `python3 tb/pp_top/ctr_mutants.py` | 18 of 18 |
| `python3 tb/pp_top/acmp_mutants.py` | 101 of 101 KILLED, goldens PASS |
| `python3 tb/pp_top/gsi_mutants.py` | 30 detected by named checks, golden and restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py` | decode killed, golden and restored PASS |
| `make -C tb/elab_guards mutants` | control PASS, 160 of 160 killed |
| `make -C tb/aecp_cmds mutants` | 17 of 17 detected, golden and restored PASS |
| `make -C tb/adp_engine mutants` | 62 of 62 |

## Consumer gate (milan-fpga, a local scratch clone of dev 1e80128f, never pushed)

The gitlink is this head; `reboot_req_o` is left unconnected.

| Gate | Result |
|---|---|
| Full sweep in four shards, then `scripts/suite_tally.py ... --expect-suite-root tb/verilator` | 64 suites, each once; 2,191,694 checks, 0 in-suite failures (`milan_dp`, `pp_shadow`, `nvm_cosim`, `capture_coherence` among them). The first run's shards shared CPUs with the processor campaigns, and suites in each hit the wall clock (result unknown, 0 failures). Each shard was re-run whole with the sweep's own `SUITE_TIMEOUT` override, and the tally is of those runs |
| `lint_rtl.py --check`, port contracts, wire accountability, SV/C++/Python idiom, RTL source lists, `pp_srcs.py`, hygiene, TODO ownership, doc paths, entity shape (with self-tests) | all pass |
| behave, yosys elaboration of `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow`, `xvlog_gate.py --check` | all pass |
| feature status, `docs_check.py`, doc style, em dash, submodule docs and diagram, DOC_MAP, module matrix, diagram PNGs, solution docs, shell idiom, SoC sources | all pass |
| `./syn/yosys/ooc.sh --record-rom-digests` | ucode digest `49a993be...`, the latency ROM unchanged |
| OOC area of `KL_pp_shadow` (yosys `synth_xilinx`) against dev | -257 LUT, +9 FF, +4 CARRY4; LUTRAM, BRAM and DSP unchanged |

Adopting the pin takes four parent edits, which the scratch parent carries:

1. Name the pin at KL_pp_shadow's instance. With it absent, `lint_rtl.py --check` fails
   (`PINMISSING reboot_req_o`). Wire it to the reset (milan-fpga #787) or leave it open with a
   rationale.
2. Add REBOOT to `tests/steps/aecp_engine_steps.py` SERVED. Without it behave fails on
   `aecp_response_contract.feature:359`.
3. Add REBOOT to `docs/reference/milan_feature_status.json`, its four fact documents and the
   "thirty" served counts (`check_feature_status.py`).
4. Bump the pin documentation and regenerate `submodule_boundaries` (any pin bump).

## Open risks for the integrator

- Adopting this pin with `reboot_req_o` absent from KL_pp_shadow's instance fails the parent's RTL
  lint ratchet (`PINMISSING reboot_req_o`). The adoption has to name the pin: wired to the reset
  (milan-fpga #787), or open with a rationale until then.
- Until #787 wires the reset, a controller's REBOOT takes the entity off the network, silent, until
  the next reset.
- The request does not wait for persistence (see above).
- While the reset is withheld, the producers held at the gate keep their TX slots and their pending
  work. The reset clears all of it; nothing is meant to resume without it.
- Area: milan-fpga's area budget records 16 of 15,850 slices left on the shipping route. A Vivado
  route at adoption is the deciding measurement; none was run here.
