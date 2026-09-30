# [A462] lane C5a — AECP deadlines and the scoreboard (HANDOFF)

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch
`c5a-aecp-deadlines` from `main` 0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff.
Issues: #81 (GAP-07), #57 (REQ-MVU-005), #84 (GAP-10). Assignment: #81 comment
5915626788. TAKEN posted 2026-09-30 18:43 CEST (comment 5915631591). REVIEW
READY posted 2026-10-01 with head `f963fe9` (comment 5921217255).

Status: REVIEW READY at head `f963fe9ac591b8a42547700468fc875db27ae5ab` (five
commits on `0451d83d`, not pushed). Design written (section 0) before any
code; no STOP condition met (section 0.5). Items 1 to 3 landed in order
(sections 1 to 3), with the parent-visible list in section 4, the gates in
section 5 (all rc 0) and what remains in section 6. Baseline at `0451d83d`:
`tb/pp_top` 7,944 checks, 0 FAIL (5 min 02 s for both builds). Head:
`tb/pp_top` 8,112 checks over three builds.

Commits:

| Commit | Subject |
|---|---|
| `04c2f5c` | item 1, #81: the deadline read at admission, the kill face, the µCPU preempt, DL1-DL7, P19, the campaign driver and its first 13 arms |
| `9a82661` | item 2, #57: section TB in the third build, its arms, the driver's ROM-image fix |
| `fb0c13c` | item 3, #84: `hz_classify`, the barrier pick, section HZ, its arms |
| `f1898da` | `.gitattributes`: the new mutation patches' blank context lines |
| `f963fe9` | `tb/pp_top/README.md`: two D3 control counts that moved with the deadline (section 5.3) |

## 0. Design (written before any code)

### 0.1 Clauses

- IEEE 1722.1-2021 §9.3.2.6: "All ATDECC messages shall have a 250 millisecond
  timeout ... Entities shall respond to all ATDECC commands within 240
  milliseconds." IN_PROGRESS is not used (06 §5 policy).
- Milan v1.2 §5.4.3.4: "All MVU messages shall have a 250 ms timeout ...
  Entities shall respond to all MVU commands within 240 ms."
- Milan v1.2 §5.4.3.3, Table 5.19: the MVU status codes are SUCCESS (0) and
  NOT_IMPLEMENTED (1); 2 to 31 are reserved.
- IEEE 1722.1-2021 Table 7-141: status 10 ENTITY_MISBEHAVING, "generated an
  internal error while trying to process the command".
- 08 §4 F08.3: T-AECP-RESP 240 ms (hard); T-BUDGET-AECP-WC <= 100 ms (the
  armed deadline); T-BUDGET-ACMP-RESP <= 50 ms (design budget).
- 03 §6 F03.7 (nine classes, keys, matrix) and its rules (d) (the D3 boot hold
  is the one exception, no deadline expiry) and (e) (a deadline expiry forces
  a response through FAIL_SAFE, the key is released only after that response
  is queued, no partial commit survives); F03.3's deadline arc; 06 §8 FAIL_SAFE
  entry; 09 F09.4 last row.

### 0.2 Where the transaction deadline is read

`pp_txn_t.deadline` is stamped by `KL_pp_normalizer.sv:139` as arrival +
`BUDGET_AECP_MS_C` (T-BUDGET-AECP-WC, `protocol_processor_top.sv:838`) and read
by nothing today. It will be read in `protocol_processor_top`'s scoreboard
owner block (`scoreboard_owners`, :3431), at the AECP admission
(`aecp_sb_accept_w`), where the hold id and RX slot are already latched:

- `aecp_dl_r <= aecp_head_w.deadline` for every admitted AECP head;
- rule (d)'s exception: a head that was resident while the D3 walk had not
  reached its done terminal (`!d3_done_w`, the boot hold) is re-armed at its
  admission, `now_ms + T-BUDGET-AECP-WC`, so the one command held through a
  restore is answered by its own program after it (the in-service latch,
  after the terminal, keeps the stamped deadline: rule (d) says it adds no
  media time);
- expired when `now_ms - aecp_dl_r` (mod 2^32, the normalizer's arithmetic)
  has its sign bit clear. One 32-bit register and one comparator: the engine
  is single-issue, so one AECP deadline is live at a time, and F08.4's slot
  map does not change.

ACMP's stamped deadline keeps no kill consumer: the ACMP executors have no
forced-respond program, and 08 §4 gives ACMP a design budget. The TIM suite
asserts T-BUDGET-ACMP-RESP instead (item 2).

### 0.3 How the deadline-kill face reaches the scoreboard

Today `protocol_processor_top.sv:988-990` ties `kill_valid_i`, `kill_id_i` and
`kill_resp_queued_i` to 0. They become:

- `kill_valid_i` = the live AECP hold's deadline has passed (a level, from the
  expiry until the hold ends);
- `kill_id_i` = `aecp_sb_id_r`;
- `kill_resp_queued_i` = a new `KL_aecp_engine` output: a solicited response
  was handed to TX lane 0 this clock (`A_TXW` with `txreq_ready_i`).

`kill_ack_o` (honoured only with the response queued, as the module grades in
`tb/scoreboard`) ends the AECP owner, so the RX-slot return one clock later
cannot release a hold id that may already be reused. A kill with no response
queued never releases: a frame the engine drops (foreign target, an AECP
response as input) owes no response and retires through the normal release.

The engine gains `dl_kill_i` (the top's level) and uses it to preempt:

- `KL_aecp_ucpu` gains `preempt_i`, `preempt_upc_i` and `preempted_o`. At the
  next instruction boundary (an op retiring, or an empty E stage), and only
  while the program has retired no effect op (WRITE_ST, NAME_WR, COMMIT,
  NVM_MARK, NOTIFY_ENQ, SEND_RESP) and the retiring op is not one, the
  sequencer is redirected, the response cursor and length return to 12 (no
  partial body), and the program runs `E_DLKILL`, a new two-word stub in
  front of `E_FAILSAFE`: a SUCCESS status becomes ENTITY_MISBEHAVING, a
  refusal status already chosen is kept (06 §8 "best current status"), and
  `E_FAILSAFE` (BUILD_HDR, SEND_RESP, END) is unchanged. After its first
  effect a program is never redirected: it ends with its real answer, so no
  partial commit survives (rule (e)).
- The engine never asserts `preempt_i` for the three commands whose state
  change rides a gather face (REGISTER/DEREGISTER and LOCK_ENTITY on the
  registry face; ADD/REMOVE_AUDIO_MAPPINGS on the edit face, whose phase-1
  acceptance is its point of no return): they run to their END, every wait
  watchdog-bounded, and answer for real.
- MVU: a preempted MVU command answers NOT_IMPLEMENTED with the command echoed
  (the MVU refusal form), because Milan Table 5.19 reserves status 10.
- GET_DYNAMIC_INFO: its running getter is preempted and the aggregate is voided
  (ENTITY_MISBEHAVING, empty) at the next record boundary, through the
  existing void of the shape check.
- The forced response is unicast to the requester, message_type + 1,
  sequence_id echoed: the 60-byte frame the memory-fault void already emits.
- Bound: an op's wait is watchdog-bounded (the longest single op is a
  descriptor burst, at most 72 beats of `DESC_MEM_TMO_CYC_P` = 4,096 clocks,
  about 2.95 ms at 100 MHz); `E_DLKILL` + `E_FAILSAFE` then cost about 20
  clocks and one lane write, so the forced response is queued a few ms after
  the 100 ms deadline, inside the 140 ms rule (e) keeps for it.

### 0.4 How the six missing F03.7 classes reach the scoreboard

The dispatch-ROM stub `hz_stub` (`protocol_processor_top.sv:1427-1455`:
ACMP = STREAM_CFG, 0x002C/0x002D = MAP_CFG, everything else RO_SNAPSHOT, key =
protocol number) is replaced by `hz_classify`, answered on the normalizer's
existing seam (`hz_class_i`/`hz_key_i`, same cycle): the seam's protocol and
opcode plus the header latch's message_type, target_entity_id and operands
(@24 descriptor_type, @26 descriptor_index, the ACMP consuming engine's
unique_id). No normalizer port changes.

| Transaction | Class | Key |
|---|---|---|
| AEM command 0x0006 SET_CONFIGURATION | CFG_BARRIER | global (0) |
| 0x0008 SET_STREAM_FORMAT, 0x000E SET_STREAM_INFO, 0x0022/0x0023 START/STOP_STREAMING | STREAM_CFG | {type, index} |
| 0x002C/0x002D ADD/REMOVE_AUDIO_MAPPINGS | MAP_CFG | {type, index} (stream port) |
| 0x0014 SET_SAMPLING_RATE, 0x0016 SET_CLOCK_SOURCE | CLOCK_CFG | {type, index} (audio unit / clock domain) |
| 0x0010 SET_NAME | NAME_WR | {type, index} |
| 0x0001 LOCK_ENTITY | LOCK_OP | global (0) |
| 0x0024/0x0025 REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION | REGISTRY_OP | the registry key |
| 0x0018 SET_CONTROL | IDENTIFY | {CONTROL, index} |
| GETs with the {type @24, index @26} shape (0x0009, 0x000F, 0x0011, 0x0015, 0x0017, 0x0019, 0x0027, 0x0029, 0x002B) | RO_SNAPSHOT | {type, index} |
| 0x0028 GET_AS_PATH (index at @24) | RO_SNAPSHOT | {AVB_INTERFACE, index} |
| 0x0000, 0x0002, 0x0007 (ENTITY-addressed) | RO_SNAPSHOT | {ENTITY, 0} |
| READ_DESCRIPTOR, GET_DYNAMIC_INFO, every other AEM opcode, MVU, AA, AECP responses, commands for another entity_id | RO_SNAPSHOT | the none key |
| ACMP GET_RX_STATE (10) | RO_SNAPSHOT | {STREAM_INPUT, listener uid} |
| ACMP GET_TX_STATE (4), GET_TX_CONNECTION (12) | RO_SNAPSHOT | {STREAM_OUTPUT, talker uid} |
| every other ACMP message to the talker (PROBE_TX, DISCONNECT_TX) | STREAM_CFG | {STREAM_OUTPUT, talker uid} |
| every other ACMP message to the listener (BIND/UNBIND, probe responses) | STREAM_CFG | {STREAM_INPUT, listener uid} |

Key = {descriptor_type[5:0], descriptor_index[9:0]}; namespace 0x3F (no
descriptor type) carries the registry key and the none key. Aliasing (a type
above 63, an index above 1023) can only make two different descriptors share
a key: a spurious conflict, never a missed one.

Found while designing, and fixed with it: once CFG_BARRIER exists, the top's
round-robin can deadlock. A refused barrier latches `barrier_pend`, which
refuses every non-barrier head until the barrier grants; if the last grant
was AECP (ACMP preferred) and an ACMP head is a candidate, the ACMP head is
picked and refused for ever and the AECP barrier is never presented again. The
pending barrier is always the AECP head (only SET_CONFIGURATION is a barrier),
so the AECP head wins the pick while `barrier_pend_o` is 1.

Limits recorded, not changed: the F03.7 MAP_CFG cross-lock stays class-wide
(module banner); GET_DYNAMIC_INFO reads several descriptors under one {class,
key} and is keyed like READ_DESCRIPTOR (not serialized against an ACMP step
on a member's stream, as no AECP read was before this lane); with two
single-issue clients (ACMP, AECP) the F03.7 matrix admits no conflict between
CLOCK_CFG, NAME_WR, REGISTRY_OP or IDENTIFY and any class ACMP presents, so
those four are graded by the {class, key} the scoreboard is presented and by
arms proving they do not over-serialize ACMP.

### 0.5 STOP check

No top-level port and no parameter (`BUDGET_AECP_MS_C` stays the top's
localparam). No new source file (the parent's source lists are unchanged). No
port change on a module the parent instantiates by name: `KL_aecp_engine` and
`KL_aecp_ucpu` gain internal ports, instantiated only by the processor
(`tb/ucpu` drives the µCPU's new inputs, which default 0). No register-map
change: F03.3's "count + trace" of a kill is not added, because a snapshot word
would be a register-map change (listed under what remains). No opcode constant
is added to `KL_aecp_engine.sv` (the parent's BDD inventory parses them). In
the parent's integration no AECP command approaches 100 ms, so the kill is
inert there; the classifier only changes which ACMP/AECP pairs may overlap.
No STOP is needed; proceeding.

## 1. Item 1 — #81 GAP-07: deadline read, kill face connected

Commit `04c2f5c`. Clauses: IEEE 1722.1-2021 §9.3.2.6, Milan v1.2 §5.4.3.4 and
§5.4.3.3 Table 5.19, IEEE Table 7-141 (status 10); 03 §6 rules (d) and (e),
08 §4 F08.3, 06 §8.

RTL (file:line at `04c2f5c`):

- `hdl/top/protocol_processor_top.sv`: the kill face at :998-1001
  (`kill_valid_i` = `aecp_dl_kill_w`, `kill_id_i` = `aecp_sb_id_r`,
  `kill_resp_queued_i` = `aecp_dl_queued_w`); the owner cleared on
  `sb_kill_ack_w` (:3478); the deadline block (:3485-3525): `aecp_dl_r`
  latched from `aecp_head_w.deadline` at `aecp_sb_accept_w` (:3509), re-armed
  at admission for a head resident before the D3 done terminal (rule (d)),
  expiry `!(now_ms - aecp_dl_r)[31]` (:3524); the engine's
  `dl_kill_i`/`dl_queued_o` (:3600-3601).
- `hdl/aecp/KL_aecp_engine.sv`: ports `dl_kill_i` (:371), `dl_queued_o`
  (:374); `UPC_DLKILL_C` = 6 (:824); the DEADLINE KILL block (:1673-1701:
  `dl_kill_r`, `ucpu_preempt_w` excluding REGISTER/DEREGISTER, LOCK_ENTITY and
  the map edits, `dl_queued_o`); A_RUN: a preempted MVU command answers
  NOT_IMPLEMENTED with the command echoed (:3612); GET_DYNAMIC_INFO voided at
  A_GDEC (:3001) and A_RUN (:3626).
- `hdl/aecp/KL_aecp_ucpu.sv`: ports `preempt_i` (:82), `preempt_upc_i`,
  `preempted_o`; `pre_go_w` (:483: an instruction boundary, before the first
  effect op, once per dispatch), the redirect at the end of S_RUN (:719, the
  cursor and length back to 12 outside a batch).
- `hdl/aecp/ucode/gen_ucode.py`: `E_DLKILL` = 6, two words falling into
  `E_FAILSAFE` (BR_STATUS keeps a refusal; SET_STATUS 10 otherwise).

Tests and failing arms (`tb/pp_top` section DL, `make deadline`, 29 checks;
`tb/ucpu` P19, 28 checks):

| Check | What it grades | Fails against |
|---|---|---|
| DL1 | a GET_COUNTERS slowed to about 330 ms is answered ENTITY_MISBEHAVING header-only byte-exact; kill at 9,943 clocks after reception, first byte at 13,354 (budget 10,000, T-AECP-RESP 24,000); stopped at an op boundary; one redirect; the kill honoured once, in the hand-off clock; the key held from the expiry to the hand-off | the pre-lane tie-off (`dl-kill-tied-off`: its own SUCCESS at 33,505 clocks), `dl-released-before-queued` |
| DL2 | a SET_NAME past its NAME_WR answers its own SUCCESS (kill at 9,919, response at 18,969), mark once, name reads back | `dl-preempt-after-effect-top` |
| DL3 | a GET_MILAN_INFO queued behind DL1's stall: deadline from reception, answered MVU NOT_IMPLEMENTED with the command echoed at 13,396 clocks after its reception | `dl-armed-at-admission`, `dl-mvu-forced-status-10` |
| DL4 | a 12-record GET_DYNAMIC_INFO against a 3,900-clock lane write is voided at 12,085 clocks | `dl-gdi-runs-on` |
| DL5 | an AECP response frame admitted past its deadline is dropped, one kill honoured, holds free, a later command answered | `dl-kill-tied-off`, `dl-released-before-queued`, `dl-gdi-runs-on` |
| DL6 | an ADD_AUDIO_MAPPINGS still validating at the deadline answers its own SUCCESS, both records committed (kill 9,929, response 12,225) | `dl-edit-preempted` |
| DL7 | RX slots free, READ_DESCRIPTOR byte-exact | |
| D3O6 (existing) | the command held 150 ms through the boot restore is answered byte-exact | `dl-boot-hold-not-exempt` |
| P19a-P19h | the redirect: before the first op, never after an effect, never cutting a waiting op, once per dispatch, dropping a partly built body, a batch's base kept, the best status kept, the next dispatch clean | `dl-preempt-after-effect`, `ucpu-preempt-cuts-a-wait`, `ucpu-preempt-keeps-the-body`, `ucpu-preempt-repeats`, `dlkill-always-misbehaving` |

Mutation campaign (`tb/pp_top/aecp_mutants.py`, patches in
`tb/pp_top/mutations/`, `make -C tb/pp_top aecp-mutants`, added to CI): item 1's
13 arms (12 plus the MVU arm of item 2) all KILLED at `04c2f5c`'s tree:

| Arm | Target | Failing checks |
|---|---|---|
| `dl-kill-tied-off` | pp_top deadline | 16 (DL1 x6, DL3 x5, DL4 x3, DL5 x2) |
| `dl-released-before-queued` | pp_top deadline | 3 (DL1 x2, DL5) |
| `dl-armed-at-admission` | pp_top deadline | 2 (DL3) |
| `dl-boot-hold-not-exempt` | pp_top d3 | 1 (D3O6) |
| `dl-gdi-runs-on` | pp_top deadline | 4 (DL4 x3, DL5) |
| `dl-edit-preempted` | pp_top deadline | 2 (DL6) |
| `dl-preempt-after-effect-top` | pp_top deadline | 2 (DL2) |
| `dl-mvu-forced-status-10` | pp_top deadline | 1 (DL3) |
| `dl-preempt-after-effect` | ucpu run | 4 (P19c x3, P19d) |
| `ucpu-preempt-cuts-a-wait` | ucpu run | 2 (P19e) |
| `ucpu-preempt-keeps-the-body` | ucpu run | 1 (P19f) |
| `ucpu-preempt-repeats` | ucpu run | 18 (P19a-P19h) |
| `dlkill-always-misbehaving` | ucpu run | 1 (P19d) |

Resource cost (yosys 0.66 `synth_xilinx -family xc7 -flatten`, out of context,
base `0451d83d` vs `04c2f5c`; Vivado, the instrument of record, is not
installed on this host):

| Top | Recipe | LUT | FF |
|---|---|---|---|
| `KL_aecp_ucpu` | default | 1,550 -> 1,578 (+28) | 489 -> 491 (+2) |
| `KL_aecp_engine` | default | 8,635 -> 8,123 (-512; MUXF7 1,241 -> 574, MUXF8 427 -> 112: a remapping, not a saving) | 4,580 -> 4,583 (+3) |
| `KL_aecp_engine` | `-nowidelut` (LUT-only) | 7,984 -> 8,135 (+151) | +3 |
| `protocol_processor_top` (8x8) | `-nowidelut` | 62,228 -> 62,912 (+684) | 30,454 -> 30,490 (+36) |

The flop figure is exact: `aecp_dl_r` (32) + `aecp_boot_held_r` + `dl_kill_r` +
the µCPU's `pre_seen_r`/`pre_taken_r` = 36. The LUT figures move with ABC's
mapping of the whole flattened design; read them as "of order a hundred".

## 2. Item 2 — #57 REQ-MVU-005: T-AECP-RESP

Commit `9a82661` (tests, docs and the campaign; no RTL change, so no resource
cost). Clauses: Milan v1.2 §5.4.3.4 (MVU within 240 ms), §5.4.3.3 Table 5.19;
IEEE 1722.1-2021 §9.3.2.6; 08 §4 F08.3.

- The deadline-kill seam for MVU is exercised by item 1's DL3 (a queued
  GET_MILAN_INFO past its deadline answers MVU NOT_IMPLEMENTED, command
  echoed, 13,396 clocks after its reception in the compressed timebase).
- `tb/pp_top` section TB (56 checks) runs in a third build (`make budget`,
  `PP_TOP_TIM_REAL`: 1 ms = 1,000 clocks, the nominal clock's own), so the
  deadline never cuts a measurement; `make` now sums three builds. Latency is
  MAC command byte 0 to MAC response byte 0, graded like B4/B4b against its
  line at P-CLK-HZ (T-AECP-RESP 24,000,000, T-BUDGET-AECP-WC 10,000,000,
  T-BUDGET-ACMP-RESP 5,000,000 clocks), plus structural bounds:

| Check | Stimulus | Measured clocks |
|---|---|---|
| TB1 | GET_MILAN_INFO, byte-exact, suite latency / 143 per access | 248 / 746 |
| TB1 | GET_SYSTEM_UNIQUE_ID (waived: NOT_IMPLEMENTED echo) | 169 / 169 |
| TB2 | READ_DESCRIPTOR of a 576-byte descriptor (618-byte frame, oversize slot), byte-exact | 3,157 / 12,587 |
| TB2 | GET_DYNAMIC_INFO with all 13 getters, SUCCESS, cdl <= 524 | 4,426 / 12,852 |
| TB3 | the three above behind a 15-frame notification fan-out (16 controllers registered), at 143: answered as idle, within one job plus idle latency of the fan-out's last frame | 12,709 / 24,550 / 24,681 |
| TB4 | GET_MILAN_INFO, response memory at 4,000 clocks per access (short of its watchdog) | 16,174 |
| TB5 | ACMP GET_RX_STATE / GET_TX_STATE idle, beside the oversize READ_DESCRIPTOR and during a fan-out: at most idle plus one frame | 172 / 154 in every case |
| TB | the deadline never fired during the section | |

Worst AECP: 24,681 clocks = 0.103 % of T-AECP-RESP at P-CLK-HZ. Finding (not
acted on, recorded in 08 §4): `KL_aecp_notify` holds the AECP command path
while a notification class drains (its `amap_busy_o`), so a solicited command
waits for the whole class, not for one frame gap as 08 §4's fan-out row
states; bounded and measured above (the TB3 premise was first written as
"ahead of the queued jobs" and failed against the RTL, which is how this was
found).

Mutation arms (item 2), all KILLED:

| Arm | Target | Failing checks |
|---|---|---|
| `mvu-silent` (E_MVUINFO without SEND_RESP) | pp_top budget | 12: TB1, TB3, TB4 |
| `fanout-never-ends` (the notification walk never ends its class) | pp_top budget | 23: TB3-TB5 |
| `acmp-waits-for-aecp` (every AEM command MAP_CFG in the stub) | pp_top budget | 2: TB5 |
| `dl-mvu-forced-status-10` | pp_top deadline | 1: DL3 |
| `dl-armed-at-admission` | pp_top deadline | 2: DL3 |

Driver fix found while running these: a patched generator's ROM image outlived
its arm, because the restored `gen_ucode.py` keeps an older timestamp than the
image make had built from the patch; `aecp_mutants.py` now deletes every
generated ROM image before each arm (`forget_generated_roms`). The item-1 arms
were re-run after the fix where a ROM patch preceded them.

## 3. Item 3 — #84 GAP-10: nine F03.7 classes reach the scoreboard

Commit `fb0c13c`. Clauses: 03 §6 F03.7 (classes, keys, matrix), F06.14 (the
state-changing opcodes and their classes); IEEE 1722.1-2021 §7.4.x of each
opcode; the scoreboard's own matrix (`KL_pp_scoreboard.sv`, unchanged).

RTL (`hdl/top/protocol_processor_top.sv`, at `fb0c13c`):

- `hz_classify` replaces `hz_stub` (the dispatch-ROM stub): the table of
  section 0.4, answered on the normalizer seam (`hz_class_i`/`hz_key_i`) from
  the seam's protocol and opcode and the header latch's message_type,
  target_entity_id and operands; `hz_aem_cmd_w` (only an AEM_COMMAND for this
  entity takes its opcode's class); keys `{type[5:0], index[9:0]}`, 0x3F for
  the registry and no-descriptor keys.
- The admission pick (`sb_pick_aecp_w`): the AECP head wins while
  `sb_barrier_w` (a refused CFG_BARRIER's drain) is pending. Found while
  designing and proven by `hz-barrier-no-priority`: without it the admission
  port wedges for good (33 failures, every arm after HZ3).

Tests (`tb/pp_top` section HZ, `make hazards`, 83 checks). An ACMP transaction
is held in flight by stalling the MAC until four GET_RX_STATE answers fill the
standard TX slots, so the next ACMP command is admitted and keeps its key (a
PROBE_TX was tried first: the talker waits for the allocator before taking the
command, so it held its key 16 clocks only).

| Check | Grades | Fails against (failing arms) |
|---|---|---|
| HZ1 | 33 AECP + 6 ACMP transactions each present their F03.7 class and key at the admission port | the pre-lane stub (`hz-stub-restored`: 34 rows), and each per-class mutant |
| HZ2 | SET_CONFIGURATION latches the drain while an ACMP UNBIND_RX holds, is admitted once that key frees, keeps a later ACMP head behind it, answers SUCCESS | stub, `hz-setcfg-not-barrier` |
| HZ3 | a pending barrier is not starved by the round-robin (ACMP preferred, a GET_RX_STATE queued): both answered, the barrier first | stub, `hz-setcfg-not-barrier`, `hz-barrier-no-priority` |
| HZ4 | LOCK_ENTITY waits for a held stream step; the unlock runs beside a held read | stub, `hz-lock-not-lockop`, `hz-acmp-reads-as-steps` |
| HZ5 | START_STREAMING waits for the held sink's key, runs beside another sink's | stub, `hz-stream-key-none` |
| HZ6 | GET_STREAM_INFO likewise; two reads of one sink run together | stub, `hz-reads-keyed-none`, `hz-acmp-reads-as-steps` |
| HZ7 | ADD_AUDIO_MAPPINGS waits for any stream step (class-wide cross-lock) | (held by the stub too) |
| HZ8 | CLOCK_CFG, NAME_WR, REGISTRY_OP, IDENTIFY and READ_DESCRIPTOR run beside a held stream step (no over-serialization) | `hz-clock-as-lock`, `acmp-waits-for-aecp` (TB5 too) |

With two single-issue clients the matrix admits no conflict between CLOCK_CFG,
NAME_WR, REGISTRY_OP or IDENTIFY and any class ACMP presents, so those four are
graded by HZ1 (the class and key the scoreboard is presented) and HZ8 (never
over-serialized): #84 acceptance 2's "one admission conflict per newly
reachable class" cannot be met for them at this top (section 6).

Mutation arms (item 3), all KILLED:

| Arm | Failing checks |
|---|---|
| `hz-stub-restored` | 46: HZ1 x34, HZ2 x3, HZ3 x2, HZ4 x3, HZ5 x2, HZ6 x2 |
| `hz-setcfg-not-barrier` | 5: HZ1, HZ2 x2, HZ3 x2 |
| `hz-lock-not-lockop` | 5: HZ1 x2, HZ4 x3 |
| `hz-stream-key-none` | 6: HZ1 x4, HZ5 x2 |
| `hz-reads-keyed-none` | 11: HZ1 x9, HZ6 x2 |
| `hz-clock-as-ro` | 2: HZ1 |
| `hz-clock-as-lock` | 3: HZ1 x2, HZ8 |
| `hz-name-as-ro` | 1: HZ1 |
| `hz-registry-as-ro` | 2: HZ1 |
| `hz-identify-as-ro` | 1: HZ1 |
| `hz-acmp-reads-as-steps` | 5: HZ1 x3, HZ4, HZ6 |
| `hz-barrier-no-priority` | 33: HZ3 and every later arm |
| `hz-foreign-target-classified` | 1: HZ1 |
| `hz-response-classified` | 1: HZ1 |
| `acmp-waits-for-aecp` (now READ_DESCRIPTOR as CFG_BARRIER) | 2: TB5 |

Resource cost (yosys 0.66 `synth_xilinx -family xc7 -flatten -nowidelut`,
`protocol_processor_top` 8x8, out of context): LUT 62,912 -> 61,962 (-950, the
flattened design's ABC mapping, not a saving), FF 30,490 -> 30,508 (+18; the
classifier is combinational, and 15 of them are most likely the normalizer
register's class and key bits that were constant under the stub and are now
live). Whole lane, base -> head: LUT
62,228 -> 61,962, FF 30,454 -> 30,508 (+54).

## 4. Item 4 — the parent-visible list

Nothing here needs a parent change: the consumer set passes at milan-fpga dev
`ccdd07b5` with `parent-adaptation-132-c1.patch` alone (section 5.3), and no
STOP condition was met.

Interfaces and files:

- `protocol_processor_top`: no port, parameter or register-map change
  (`BUDGET_AECP_MS_C` stays a localparam; no status word or counter added).
- Five new internal ports, all with `//!` contracts, on modules only the
  processor instantiates: `KL_aecp_engine` `dl_kill_i`, `dl_queued_o`;
  `KL_aecp_ucpu` `preempt_i`, `preempt_upc_i[10:0]`, `preempted_o`. The
  parent's port-contract count moves from 1,748 to 1,753 processor ports, with
  the undocumented count unchanged at 111.
- No new or renamed RTL file (the parent's source lists and `pp_srcs` are
  unchanged). No opcode constant added to `KL_aecp_engine.sv` (the parent's
  BDD steps parse them). The µCPU ROM gains `E_DLKILL` at µPC 6 (a slot that
  was free); `check_upc_map` agrees.
- New test files only: `tb/pp_top/aecp_mutants.py`, 29 patches in
  `tb/pp_top/mutations/`, and one `.gitattributes` line for those patches.

Behaviour a consumer can observe:

- Deadline kill (item 1). An AECP command whose program is still running
  T-BUDGET-AECP-WC (100 ms) after its reception is answered by `E_DLKILL`:
  ENTITY_MISBEHAVING header-only, or the refusal status it had already chosen;
  an MVU command gets NOT_IMPLEMENTED with the command echoed; a
  GET_DYNAMIC_INFO is voided. A program that has already retired an effect op
  (a write, name write, commit, NVM mark, notification or its response) is
  never cut, and neither are the registry and map-edit commands. The kill is
  inert in the parent integration, where no command gets near 100 ms: every
  parent gate passes unchanged.
- Hazard classes (item 3). The stub's "everything is RO_SNAPSHOT keyed by
  protocol, ACMP is STREAM_CFG" is replaced by the F03.7 table. Pairs that now
  serialize and did not before:
  - SET_CONFIGURATION drains every ACMP transaction.
  - LOCK_ENTITY waits for an ACMP stream step.
  - A stream-config AECP command, or a stream GET, waits for an ACMP step on
    the same stream.
  - A pending barrier wins the admission pick.

  Nothing that ran concurrently before now waits, except these conflicts.
- Resource cost (yosys, out of context, `-nowidelut`, 8x8 top): +54 FF.
  The LUT figure moves by the flattened ABC mapping (62,228 -> 61,962).

Parent ratchets (read-only, measured in the scratch parent, base `0451d83d`
against head). They move only in the direction the parent may lower:

- `check_port_contracts`: literal-bound named connections 51 -> 48, and those
  without a local rationale 62 -> 59 (the three kill-face tie-offs are gone).
  The gate prints "the ratchet can be lowered".
- Test-only hierarchical observations: 176 -> 189. These are the new
  `tb/pp_top` debug taps; this is an inventory, not a ratchet.
- `measure_test_evidence`: suites without a mutation arm 74 -> 73 (`tb/ucpu`
  now has arms). Unseeded draws (10), DUT-source readers (0) and wall-clock
  files (3) are unchanged, and `aecp_mutants.py` reads logs only.
- `measure_naming`: unchanged (96 recorded).

Documents a consumer reads: `docs/guides/integrator.md` (the new "Slow but
live is bounded too" paragraph and the TB sizing sentence) and
`docs/guides/operator.md` (the §2 row and the §9 ENTITY_MISBEHAVING row); 03
§6, 06 §8/§8.1, 08 §4 and 09 §8.3 (anchor
`#83-the-aecp-deadline-and-the-hazard-classes-issues-81-57-84`).

Processor entry points added: `make -C tb/pp_top deadline | d3 | hazards |
budget | aecp-mutants`. `make -C tb/pp_top` (and so `run_suites.sh`) now
builds and runs three binaries and requires three tallies. CI gains the step "AECP deadline
and hazard-class mutation campaign".

## 5. Gates

Head `f963fe9ac591b8a42547700468fc875db27ae5ab`. After the three item commits
come two small ones:

- `f1898da` adds one `.gitattributes` line, so `tb/pp_top/mutations/*.patch`
  are checked for whitespace like the SRP and ADP patches. Without it,
  `git diff --check 0451d83d..HEAD` flags their blank context lines.
- `f963fe9` changes only `tb/pp_top/README.md`. Two D3 negative-control
  counts moved, as the D3 driver found at `f1898da` (5.3), and the README now
  records the new counts and why.

Placement of the runs:

- Gates that read no Markdown ran at `f1898da`: the suites, lint, yosys, and
  every mutation campaign up to the D3 driver.
- The retry, SRP admission and descriptor-guard campaigns, the docs gates and
  the parent's fast gates ran again at `f963fe9`.
- No gate or suite reads `tb/pp_top/README.md` (searched: `scripts/`, every
  `tb/*/*.py` and Makefile, `syn/`).

Every run was in the foreground or polled to completion, never piped into its
verdict. The working tree was clean after each run.

### 5.1 Processor suites (`./scripts/run_suites.sh` at `f1898da`, rc 0, 7 min 34 s; the same tally at `fb0c13c`)

| Suite | Checks | | Suite | Checks |
|---|---|---|---|---|
| acmp_listener | 2,544 | | release_merge | 18 |
| acmp_nvm | 360 | | resp_buf | 64 |
| acmp_talker | 1,342 | | rx_slots | 130 |
| adp_engine | 1,367 | | rx_validator | 437 |
| aecp_notify | 10 | | scoreboard | 3,705 |
| ca_originator | 16 | | side_port | 368 |
| desc_mem_guard | 78 | | srp_admission | 991,231 |
| desc_store | 584 | | srp_decoder | 190 |
| dispatch | 211 | | srp_encoder | 581 |
| dyn_state | 118 | | srp_stream_fsms | 1,219 |
| event_router | 81 | | srp_top | 2,200 |
| lsn_admit | 18 | | timer_map | 1,360 |
| maap | 75 | | timer_service | 48 |
| nvm_port | 136 | | tx_arbiter | 66 |
| originator | 104 | | tx_slots | 95 |
| **pp_top** | **8,112** (base 7,944) | | **ucpu** | **415** |
| prng | 76 | | | |

33 suites, 1,017,359 checks, 0 failing. The µPC map gate passes: 57 engine
constants, 81 entry points. The `pp_top` total has three parts:

- the default build, 8,036 checks: DL 29, HZ 83 and the D3 sections;
- the fixture build, 20 checks;
- the real-timebase build (section TB), 56 checks.

### 5.2 Other processor gates (all rc 0)

| Gate | At | Result |
|---|---|---|
| `./scripts/lint_hdl.sh` | f1898da | 41 LINT OK |
| `make check` | f963fe9 | 41 mermaid + 18 wavedrom blocks, 1,002 links, matrix 115 REQ / 17 GAP, parameters 26/26/26 |
| `make stale` | f963fe9 | rc 0 |
| `python3 scripts/gen_matrix.py --check` | f963fe9 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | f1898da | 36 tops YOSYS OK + the Xilinx engine check |
| `git diff --check 0451d83d..HEAD` | f963fe9 | clean |

### 5.3 Mutation campaigns

| Campaign | At | Result |
|---|---|---|
| `make -C tb/pp_top aecp-mutants` (this lane) | f1898da | rc 0; 5 controls PASS, 30 arms KILLED (35/35), 7 min 43 s; the same at `fb0c13c` |
| `make -C tb/adp_engine mutants` | f1898da | rc 0; 32/32 |
| `make -C tb/srp_top mutants` | f1898da | rc 0; 90/90, assertion coverage 65/65 (29 min) |
| `make -C tb/nvm_port figures` (after `git fetch --no-tags origin refs/pull/13/head`) | f1898da | rc 0 |
| `tb/pp_top/gsi_mutants.py` | f1898da | rc 0; 20 detected by named checks, golden and restored PASS |
| `tb/pp_top/name_wr_mutant.py` | f1898da | rc 0; decode killed, golden and restored PASS |
| `tb/pp_top/d3_mutants.py` | f1898da | rc 0; 83 of 83 KILLED, goldens PASS (22 min) |
| `tb/acmp_talker/retry_mutants.py` | f963fe9 | rc 0; 62 killed, 7 equivalence and 1 performance controls, baseline and restored rc 0 |
| `tb/srp_admission/mutants.py` | f963fe9 | rc 0; 12/12 |
| `tb/desc_mem_guard/mutate.py` | f963fe9 | rc 0; the hold-deleted mutant is detected by the completed byte assertion |

D3 driver drift, found here and recorded in `tb/pp_top/README.md` (commit
`f963fe9`). The 83 arms are all killed by their named checks, and 80 fail
exactly the count the README records. `validator_admits_held_aecp` is
recorded in `tb/rx_validator/README.md` and matches (4).
`hold_released_at_go` now fails 17 checks against 16 recorded, and
`dispatch_not_held` 6 against 5. In both, the extra failure is D3O6: the
mutant lets the held command run during the slowed restore, and the deadline
kill now answers it instead of its own program. That is correct under rule
(d), which
exempts only a command still held at the terminal. To confirm, the two arms
were re-run in a scratch export of the head with the `dl-kill-tied-off`
patch applied: they failed 16 and 5 again.

### 5.4 Parent consumer gates

Setup:

- A scratch parent under `$VALIDATION_STORAGE`: a `git archive` of the trusted
  milan-fpga checkout at dev `ccdd07b5`, with its submodules at their pins
  (external `efeb541`, gptp-processor `5dce647`, third_party/verilog-axis
  `48ff7a7`).
- `protocol-processor` is a clone of this lane at the head, and its gitlink
  is set to the head.
- `parent-adaptation-132-c1.patch` (sha256 `2ba66803...ddc420`) is applied
  with `git apply`, confirmed by `git apply --check -R`.
- The trusted checkout was not modified. Gates ran in order, heavy builds one
  at a time at `-j8`.

| # | Gate | fb0c13c | f1898da | f963fe9 (head) |
|---|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0, every ratchet 0 <= 0 | rc 0 | rc 0 |
| 2 | `scripts/check_py_idiom.py` | rc 0 (too many parameters 7 <= 7) | rc 0 | rc 0 |
| 3 | `scripts/xvlog_gate.py --check` | rc 0, 4 findings == ratchet, none new | rc 0 | rc 0 |
| 4 | `scripts/check_rtl_source_lists.py` | rc 0, 36/42 tops, 6 recorded | rc 0 | rc 0 |
| 5 | `scripts/pp_srcs.py --check --selftest` | rc 0 | rc 0 | rc 0 |
| 6 | `sw/builder/test_builder.py` | rc 0, ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a board implementation report not on this host) | rc 0, same, 15 min 52 s | not re-run |
| 7 | `make -C tb/verilator/pp_shadow -j8` | rc 0, 295 checks | rc 0, 295 checks | not re-run |
| 8 | `scripts/check_port_contracts.py` | rc 0 (section 4) | rc 0 | rc 0 |
| 9 | `scripts/measure_naming.py --check` | rc 0, 96 recorded | rc 0 | rc 0 |
| 10 | `scripts/measure_test_evidence.py --check` | rc 0 (73 <= 77, 10 <= 10, 0 <= 0, 3 <= 3) | rc 0 | rc 0 |
| 11 | `scripts/docs_check.py` | rc 0, 0 findings | rc 0 | rc 0 |
| 12 | `scripts/lint_rtl.py --check` | rc 0, 90 <= 90 | rc 0 | rc 0 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | rc 0 | rc 0 | rc 0 |
| 14 | `make -C tb/verilator/nvm_cosim quick` | rc 0, 315/315 | rc 0, 315/315 | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | rc 0 (every RESULT PASS, 0 failures, controls 6/6) | rc 0, 22 min 16 s | not re-run |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | rc 0, leg defects 5/5 | rc 0, 5 min 15 s | not re-run |

The four heavy builds were not re-run at `f963fe9`. That commit changes only
`tb/pp_top/README.md`, which no parent build reads (they read the
processor's RTL, ROM generators and source lists, all identical to
`f1898da`).

The lane needs no parent adaptation of its own.

## 6. What remains

Issue closure, as written in PR-BODY.md: Closes #57, Relates to #81, Relates
to #84.

- #57 (REQ-MVU-005): every acceptance item is met.
  - 1: TB1, GET_MILAN_INFO and an unimplemented MVU command at the suite and
    143-clock latencies, against T-AECP-RESP.
  - 2: TB3 (the 16-controller fan-out) and TB4 (the response memory short of
    its watchdog).
  - 3: the kill inputs are driven, and DL1/DL3 provoke the forced response.
- #81 (GAP-07): acceptance 1 to 3 are met.
  - 1: the deadline consumer drives the kill face and FAIL_SAFE.
  - 2: DL1 plus the mutation record.
  - 3: TB for AECP under the 08 §4 worst cases, and TB5 for ACMP.
  - Not done, outside item 1: acceptance 4 (the F08.1 rows with no RTL,
    T-IDENT-BURST, T-IDENT-REARM and T-CTR-OBSERVE, and a check pinning the
    300 s / 60 s defaults).
- #84 (GAP-10): acceptance 1 and 3 are met.
  - Acceptance 2 is met for CFG_BARRIER, STREAM_CFG, MAP_CFG, LOCK_OP and
    RO_SNAPSHOT (HZ2-HZ7).
  - It cannot be met at this top for CLOCK_CFG, NAME_WR, REGISTRY_OP or
    IDENTIFY: with two single-issue clients, the F03.7 matrix admits no
    conflict between them and any class ACMP presents. They are graded by HZ1
    and HZ8 instead.
  - Not done: acceptance 4 (02 §2 rule 5, the synchronous active-low reset),
    a documentation change outside item 3.
- F03.3's kill count and trace are not added: a status word or trace entry
  would be a register-map change.
- ACMP's stamped deadline has no kill consumer. The ACMP executors have no
  forced-respond program, and 08 §4 gives ACMP a design budget, graded by
  TB5. Related: the talker waits up to `MAAP_RSP_MS_P` (10 s) for an
  allocator when one is present.
- Finding (08 §4): `KL_aecp_notify` holds the AECP command path while a
  notification class drains, so a solicited command waits for the whole
  class. It is bounded and measured (TB3), but not changed.
- GET_DYNAMIC_INFO and READ_DESCRIPTOR are keyed NONE, so they are not
  serialized against an ACMP step on a member's stream (as before this lane).
- REQ-MVU-005 latent, found and not acted on: when an MVU response's memory
  fails (a response-memory error or its `MEM_TIMEOUT_CYC_P` watchdog), the
  engine's fault path (`rsp_fail_w`, `KL_aecp_engine.sv`) still rebuilds the
  answer with status 10, which Milan Table 5.19 reserves. The deadline path
  answers NOT_IMPLEMENTED; the fault path was not changed.
- Resource figures are from yosys out of context. The Vivado figures of
  record are to be taken where Vivado is installed.
- Not done here, by the rules of the assignment: hosted CI, reviews, a push,
  a PR, and hardware.
