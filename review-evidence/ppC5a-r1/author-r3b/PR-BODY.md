[A462]
Closes #57
Relates to #81
Relates to #84

Lane C5a: AECP deadlines and the scoreboard. Branch `c5a-aecp-deadlines` from
`main` 0451d83d. Round 1 has five commits:

- one per item;
- a `.gitattributes` line for the new mutation patches;
- a `tb/pp_top/README.md` record of two D3 control counts the deadline
  moved.

Round 2 (the "Round 2" section below) adds one commit per review item and
two records. Round 3 (the "Round 3" section below) merges processor main
3f3ea56b and adds one commit per item. Round 3b (the "Round 3b" section
below) merges processor main 16ea10ac. No top-level port, parameter or
register-map change in any round.

## 1. #81 (GAP-07): the deadline is read and the kill face is connected

Clauses: IEEE 1722.1-2021 §9.3.2.6 (respond within 240 ms; 250 ms timeout);
Milan v1.2 §5.4.3.4 (MVU within 240 ms) and §5.4.3.3 Table 5.19 (MVU statuses
SUCCESS and NOT_IMPLEMENTED only); IEEE 1722.1-2021 Table 7-141 (status 10
ENTITY_MISBEHAVING); 03 §6 F03.7 rules (d) and (e); 08 §4 F08.3
(T-BUDGET-AECP-WC 100 ms); 06 §8 FAIL_SAFE.

- `hdl/top/protocol_processor_top.sv` reads `pp_txn_t.deadline` (the
  normalizer's arrival + T-BUDGET-AECP-WC stamp) at the AECP admission.
  - A head that was resident while the D3 walk had not reached its done
    terminal is re-armed at admission instead. This is rule (d)'s boot-hold
    exception.
  - Expiry is `!(now_ms - deadline)[31]`: one 32-bit register and one
    comparator.
  - The scoreboard kill face, tied to 0 until now, is driven:
    - `kill_valid_i` = the live AECP hold is past its deadline;
    - `kill_id_i` = the hold id;
    - `kill_resp_queued_i` = the engine handed a solicited response to TX
      lane 0 this clock.
  - `kill_ack_o` ends the AECP owner. So the key is released only after the
    forced response is queued, as rule (e) requires.
- `hdl/aecp/KL_aecp_engine.sv` and `hdl/aecp/KL_aecp_ucpu.sv`: the µCPU is
  preempted at an instruction boundary into `E_DLKILL`, a new two-word stub
  in front of `E_FAILSAFE` (`hdl/aecp/ucode/gen_ucode.py`).
  - Preemption happens only before the program's first effect op, never
    during a waiting op, and once per dispatch.
  - A partly built body is dropped. A refusal status the program had already
    chosen is kept; otherwise the answer is status 10.
  - An MVU command answers NOT_IMPLEMENTED with the command echoed, because
    Table 5.19 reserves status 10.
  - A GET_DYNAMIC_INFO is voided.
  - The registry and map-edit commands, whose state change rides a gather
    face, run to their own END. No partial commit survives.
- Tests:
  - `tb/pp_top` section DL (`make -C tb/pp_top deadline`, 29 checks): a
    GET_COUNTERS stalled to about 330 ms is killed about 99 ms after
    reception and answered ENTITY_MISBEHAVING byte-exact about 134 ms after
    reception. These times are in the compressed timebase, where 1 ms is
    100 clocks.
    - A SET_NAME past its name write answers its own SUCCESS.
    - A queued GET_MILAN_INFO answers the MVU refusal.
    - A GET_DYNAMIC_INFO is voided.
    - An AECP response frame past its deadline retires.
    - An ADD_AUDIO_MAPPINGS still validating answers its own SUCCESS.
    - The hold is kept until the hand-off.
  - `tb/ucpu` P19a to P19h (28 checks) grade the redirect rules.
  - The existing D3O6 grades the boot-hold exception.

## 2. #57 (REQ-MVU-005): T-AECP-RESP

Clauses: Milan v1.2 §5.4.3.4 and §5.4.3.3 Table 5.19; IEEE 1722.1-2021
§9.3.2.6; 08 §4 F08.3 (T-AECP-RESP 240 ms, T-BUDGET-AECP-WC 100 ms,
T-BUDGET-ACMP-RESP 50 ms).

- The deadline-kill seam for MVU is exercised by DL3: a queued GET_MILAN_INFO
  past its deadline answers MVU NOT_IMPLEMENTED with the command echoed.
- `tb/pp_top` section TB (56 checks) runs in a third build, `make -C
  tb/pp_top budget`, where 1 ms = 1,000 clocks, so the deadline never cuts a
  measurement. It measures MAC command byte 0 to MAC response byte 0 against
  T-AECP-RESP at P-CLK-HZ, the way B4/B4b do. Measured, in clocks:

| Check | Stimulus | Clocks |
|---|---|---|
| TB1 | GET_MILAN_INFO (byte-exact), suite latency / 143 per access | 248 / 746 |
| TB1 | an unimplemented MVU command (GET_SYSTEM_UNIQUE_ID) | 169 / 169 |
| TB2 | READ_DESCRIPTOR of a 576-byte descriptor; GET_DYNAMIC_INFO with 13 getters | 3,157 / 12,587; 4,426 / 12,852 |
| TB3 | all three behind a 15-frame notification fan-out | at most 24,681 |
| TB4 | GET_MILAN_INFO, response memory at 4,000 clocks per access | 16,174 |
| TB5 | ACMP GET_RX_STATE / GET_TX_STATE beside the oversize read and during a fan-out | 172 / 154, unchanged from idle |

- The worst AECP case is 0.103 % of T-AECP-RESP.
- Finding, recorded in 08 §4 and not acted on: `KL_aecp_notify` holds the
  AECP command path while a notification class drains. So a solicited
  command waits for the whole class, not for one frame gap. This is bounded
  and measured by TB3.

## 3. #84 (GAP-10): the nine F03.7 classes reach the scoreboard

Clauses: 03 §6 F03.7 (classes, keys, matrix), 06 F06.14 (the state-changing
opcodes), and IEEE 1722.1-2021 §7.4 for each opcode.

- `hz_classify` replaces the dispatch-ROM stub on the normalizer's existing
  seam:
  - SET_CONFIGURATION is CFG_BARRIER (global key) and LOCK_ENTITY is LOCK_OP
    (global key).
  - SET_STREAM_FORMAT/INFO and START/STOP_STREAMING are STREAM_CFG, keyed by
    stream; ADD/REMOVE_AUDIO_MAPPINGS are MAP_CFG.
  - SET_SAMPLING_RATE and SET_CLOCK_SOURCE are CLOCK_CFG, SET_NAME is
    NAME_WR, REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION are REGISTRY_OP,
    and SET_CONTROL is IDENTIFY.
  - Descriptor GETs are RO_SNAPSHOT, keyed by descriptor.
  - ACMP state reads are RO_SNAPSHOT and every other ACMP message is
    STREAM_CFG, keyed by the talker's or listener's stream.
  - Only an AEM command for this entity takes its opcode's class.
- Found and fixed with it: once a barrier exists, the round-robin could wedge
  the admission port. A refused barrier refuses every other head, and ACMP
  could keep the pick for good. A pending barrier now wins the pick.
- Tests: `tb/pp_top` section HZ (`make -C tb/pp_top hazards`, 83 checks).
  - HZ1 checks the class and key presented for 33 AECP and 6 ACMP
    transactions.
  - An ACMP command is held in flight by exhausting the TX pool. Against it,
    HZ2 to HZ8 grade:
    - the barrier drain and its order;
    - LOCK_ENTITY waiting for a stream step;
    - per-stream keys for stream config and reads;
    - the MAP_CFG class-wide cross-lock;
    - CLOCK_CFG, NAME_WR, REGISTRY_OP, IDENTIFY and READ_DESCRIPTOR running
      beside a held stream step.
- Documents: these now describe the landed shape:
  - 03 §6's classifier paragraph and its barrier-priority note;
  - 06 §8's Dispatch decision note;
  - F06.14's SET_CONFIGURATION row.

  08 §4, 09 §8.3, the integrator and operator guides and the compliance
  review's GAP-03 residue carry the deadline (items 1 and 2).

## Mutation campaign

`make -C tb/pp_top aecp-mutants` (`tb/pp_top/aecp_mutants.py`, 29 patches in
`tb/pp_top/mutations/`, added to CI).

- Each arm is applied to a scratch copy and must fail its named check.
- 5 positive controls PASS and 30 arms are KILLED:
  - 12 on item 1: the tie-off restored, release before the response is
    queued, the deadline armed at admission, the boot hold not exempt, the
    GDI running on, a map edit preempted, preemption after an effect (µCPU
    and top), a wait cut, the body kept, a repeated redirect, and a refusal
    status overwritten.
  - 4 on item 2: an MVU forced to status 10, an MVU never answered, a
    fan-out that never ends, and ACMP serialized behind AECP.
  - 14 on item 3: the stub restored, and one arm per class or key rule, the
    barrier priority, the foreign target and the response input.

## Resource cost

Measured out of context with yosys `synth_xilinx -family xc7 -flatten`.
Round 2 adds the Vivado figures, the instrument of record (see "Round 2").

- Item 1:
  - `KL_aecp_ucpu`: +28 LUT, +2 FF.
  - `KL_aecp_engine`: +151 LUT (LUT-only recipe), +3 FF.
  - Top: +36 FF. That is exactly the deadline register, the boot-hold bit,
    the engine's kill latch and the µCPU's two preempt bits.
- Item 2: no RTL change.
- Item 3: +18 FF. The classifier is combinational; the normalizer's class
  and key bits are now live.
- Whole top (8x8, `-nowidelut`): FF 30,454 -> 30,508; LUT 62,228 -> 61,962
  (ABC remapping, not a saving).

## Validation (round 1)

The head is f963fe9. Its last commit changes only `tb/pp_top/README.md`,
which no gate reads; the gates not re-run there ran at f1898da.

- `./scripts/run_suites.sh`: rc 0. 33 suites, 1,017,359 checks, 0 failing.
  `tb/pp_top` has 8,112 checks (baseline 7,944) and `tb/ucpu` has 415.
- These are all rc 0: `./scripts/lint_hdl.sh`, `make check` (links, matrix,
  parameters, wavedrom), `make stale`, `scripts/gen_matrix.py --check`, the
  µPC map gate, `syn/yosys/run.sh` and `git diff --check 0451d83d..HEAD`.
- Mutation campaigns, all rc 0:

| Campaign | Result |
|---|---|
| `make -C tb/pp_top aecp-mutants` (new) | 5 controls PASS, 30 arms KILLED |
| `make -C tb/adp_engine mutants` | 32/32 |
| `make -C tb/srp_top mutants` | 90/90 |
| `tb/pp_top/d3_mutants.py` | 83/83 KILLED |
| `tb/pp_top/gsi_mutants.py` | 20 detected |
| `tb/pp_top/name_wr_mutant.py` | killed |
| `tb/acmp_talker/retry_mutants.py` | 62 killed |
| `tb/srp_admission/mutants.py` | 12/12 |
| `tb/desc_mem_guard/mutate.py` | detected |
| `make -C tb/nvm_port figures` | rc 0 |

- Two D3 controls now fail one check more than recorded:
  `hold_released_at_go` fails 17 and `dispatch_not_held` fails 6. The extra
  check is D3O6: those mutants let the held command run during the restore,
  and the deadline now answers it. With the kill tied off, the counts are 16
  and 5 again. `tb/pp_top/README.md` records this.
- Parent consumer gates, all 16 rc 0: milan-fpga dev ccdd07b5 in a scratch
  copy, with the combined parent adaptation `parent-adaptation-132-c1.patch`
  applied and the processor at this branch.
  - The gates: C++ and Python idiom, xvlog, RTL source lists, pp_srcs, the
    builder test, pp_shadow (295), port contracts, naming, test evidence,
    docs_check, lint_rtl, nvm_cosim lint and quick (315), milan_dp, and
    milan_dp_render.
  - One builder-test arm did not run: it needs a board implementation report
    that is not on this host.
  - The four heavy builds ran at f1898da; the other twelve gates ran again at
    f963fe9.
  - The lane needs no parent adaptation of its own.

## Parent-visible list (round 1)

- No top-level port, parameter or register-map change. No new or renamed RTL
  file, and no opcode constant added to the engine.
- New internal ports, each with a `//!` contract, on modules only the
  processor instantiates:
  - `KL_aecp_engine`: `dl_kill_i`, `dl_queued_o`;
  - `KL_aecp_ucpu`: `preempt_i`, `preempt_upc_i`, `preempted_o`.
- Behaviour:
  - An AECP command still running 100 ms after reception is answered by the
    kill; it is inert in the parent integration.
  - AECP and ACMP transactions now serialize per the F03.7 matrix: a
    barrier drains ACMP, LOCK_ENTITY waits for a stream step, and stream
    config and reads wait for a step on the same stream.
- Parent ratchets move only down:
  - Port contracts: literal-bound connections 51 -> 48 and those without a
    rationale 62 -> 59, because the kill-face tie-offs are gone.
  - Suites without a mutation arm: 74 -> 73.
  - Naming, draws, DUT readers and wall-clock files: unchanged.
- Processor entry points `make -C tb/pp_top deadline | d3 | hazards | budget |
  aecp-mutants`. `make -C tb/pp_top` now sums three builds, and CI gains the
  AECP campaign step.
- The operator and integrator guides describe the forced answer and its
  bound.

## Round 2

Rulings: issue #81 comment 5923634905, on the reviews R418-1 and R419-1
(both NEGATIVE). Six items in the ruled order. One commit per item, plus
two records: the `tb/pp_top/README.md` campaign count and the Vivado area
record in `syn/ooc/README.md`. No port, parameter or register-map change. The
only RTL logic change is in `KL_aecp_engine` (items 2 and 3). The
`KL_aecp_ucpu` and top edits are comments.

Commits, in order:

- 44db34b, item 1;
- 9f0299a, item 2;
- a2d2a24, item 3;
- 5107327, item 4;
- bf9b32d, item 5;
- 49041e6, item 6;
- 88e3459, the campaign record;
- 44a6bb9, the Vivado record.

### Item 1: every reachable ACMP conflict is graded; the false statement is removed (R418-1 F1, R419-1 F1)

Clauses: 03 §6 F03.7 (the RO_SNAPSHOT, NAME_WR, CLOCK_CFG, MAP_CFG, LOCK_OP
and CFG_BARRIER rows) and the scoreboard's rules (1) to (6)
(`KL_pp_scoreboard.sv`). IEEE 1722.1-2021 §7.4.17 (SET_NAME names any named
descriptor, STREAM_INPUT and STREAM_OUTPUT included), §7.4.21.1, §7.4.25.1
and §7.4.45.1 (the descriptor types SET_SAMPLING_RATE, SET_CONTROL and
ADD_AUDIO_MAPPINGS take), and Table 7-141 (NOT_SUPPORTED).

ACMP presents only RO_SNAPSHOT (its state reads) and STREAM_CFG (every other
step), always on a stream key. The AECP engine is single-issue.

| AECP class | vs ACMP RO_SNAPSHOT, same key | vs ACMP STREAM_CFG | Graded by |
|---|---|---|---|
| CFG_BARRIER | yes (global) | yes (global) | HZ2, HZ3, HZ11a |
| LOCK_OP | no (key 0 is no stream key) | yes | HZ4, HZ11b-c |
| STREAM_CFG | yes | yes, per key | HZ5, HZ10a-d |
| MAP_CFG | only for a command naming a stream descriptor | yes, class-wide | HZ7, HZ11d-e, HZ12c |
| CLOCK_CFG | only for a command naming a stream descriptor | no (rule 6) | HZ8, HZ12a |
| NAME_WR | **yes, with a legal command** | no (rule 6) | HZ8, HZ9a-f |
| IDENTIFY | only for a command naming a stream descriptor | no (rule 6) | HZ8, HZ12b |
| REGISTRY_OP | no: its key is the registry's, which no ACMP transaction presents | no (rule 6) | HZ1, HZ8 |
| RO_SNAPSHOT | no (two reads) | yes, per key | HZ6, HZ10e-f |

- Found while doing it: both reviewers' talker-side probes were
  inconclusive, because section HZ ran with no MAAP allocator. The talker
  sat in its MAAP request wait and took no command.
  - Section HZ now runs with the allocator answering.
  - A talker transaction keeps its key a few clocks only, so talker-side
    pairs are held from the AECP side, by the same TX-pool stall.
  - Every "waits" check now requires the scoreboard to have refused the
    head at least once. A head that waits for its engine rather than its
    key cannot pass. This uses new testbench-wrapper taps.
- Tests: `make -C tb/pp_top hazards` goes from 83 to 176 checks.
  - HZ8 (added): REGISTER runs beside a held GET_RX_STATE.
  - HZ9a-f: SET_NAME on STREAM_INPUT 1 waits for a held GET_RX_STATE of
    sink 1, answers SUCCESS and reads back byte-exact. On STREAM_INPUT 0 it
    runs beside. Held on STREAM_OUTPUT 1 or STREAM_INPUT 1, it holds back
    GET_TX_STATE of source 1 or GET_RX_STATE of sink 1, and not source 2.
  - HZ10a-f: STOP_STREAMING and GET_STREAM_INFO against reads and
    DISCONNECT_TX on the same and another source.
  - HZ11a-e: SET_CONFIGURATION, LOCK_ENTITY and ADD_AUDIO_MAPPINGS held
    against the talker's read and step.
  - HZ12a-c: SET_SAMPLING_RATE, SET_CONTROL and ADD_AUDIO_MAPPINGS naming
    STREAM_INPUT 1 wait for a read of sink 1, then are refused
    NOT_SUPPORTED. Naming STREAM_INPUT 0 they run beside. Held naming
    STREAM_OUTPUT 1, they hold back GET_TX_STATE of source 1.
- 19 new arms, all KILLED. Each class and key pair has an arm on the
  listener's key and one on the talker's: `hz-name-key-none` (three
  targets), `hz-name-as-stream`, `hz-stream-key-none` (three targets),
  `hz-talker-keyed-as-listener`, `hz-reads-keyed-none-talker`,
  `hz-setcfg-not-barrier-talker`, `hz-lock-not-lockop-talker`, `hz-map-as-ro`
  (two; HZ7 had no arm in round 1), `hz-clock-key-none`,
  `hz-identify-key-none` and `hz-map-key-none` (two each).
- The statement is removed. 03 §6 now states the reachability above, and
  09 §8.3 lists HZ8 to HZ12. This body's "What remains" is corrected.
- #84 acceptance 2, re-judged: every class with a reachable conflict at
  this top is graded against ACMP. That is eight of the nine. REGISTRY_OP
  has no reachable admission conflict, so no conflict can grade it. It is
  graded by its class and key (HZ1) and by never over-serializing (HZ8). So
  #84 stays "Relates to" (see "What remains").

### Item 2: an MVU response whose memory fails answers NOT_IMPLEMENTED (REQ-MVU-005; R418-1 F3, R419-1 F3)

Clauses: Milan v1.2 §5.4.3.3 Table 5.19 (MVU statuses SUCCESS and
NOT_IMPLEMENTED; 2 to 31 reserved); IEEE 1722.1-2021 Table 9-6.

- `KL_aecp_engine.sv:3696` (A_ALLOC) and `:3726` (A_WR) are the fault
  rebuilds. They now answer a command that is not an AEM_COMMAND
  NOT_IMPLEMENTED, with the command echoed from its RX slot. This is the
  frame the deadline path forces.
- The failure can come after the TX slot is granted. So such a response
  requests the oversize slot whenever its echo would need it (`:2548-2554`).
  A legal command (cdl at most 524) always fits the standard slot.
- Check: `tb/pp_top` DL8. GET_MILAN_INFO is run under three faults: a
  response-memory read error, a write error and a tied-off master. It is
  also run padded to a 578-byte echo under a read error. Each answers MVU
  NOT_IMPLEMENTED with the command echoed, byte-exact, and each void is
  counted.
  - An AEM GET_CONFIGURATION under the read error still answers
    ENTITY_MISBEHAVING, header only.
  - Afterwards, RX slots free, and GET_MILAN_INFO answers SUCCESS.
- Arms: `mvu-fault-status-10` (fails 4) and `mvu-echo-slot-std` (fails 1).
- Docs: the 06 §6.9 GET_MILAN_INFO row, 00 REQ-MVU-005 and GAP-03, and both
  guides.

### Item 3: the deadline-killed residual-bucket types (R418-1 F2)

Clauses: IEEE 1722.1-2021 Table 9-2 (SUCCESS and NOT_IMPLEMENTED are the
codes every message type shares) and Table 7-141 (status 10 is AEM's).
Also Tables 9-4, 9-5 and 9-8 (the ADDRESS_ACCESS, AV/C and HDCP APM codes)
and §9.4.2.5.

- `st_echo_w` (`KL_aecp_engine.sv:1705-1707`) is true for every message
  type but AEM_COMMAND.
- The A_RUN remap (`:3644`) answers a preempted command of such a type
  NOT_IMPLEMENTED with the command echoed. Round 1 did this for MVU only.
  Item 2's fault path uses the same signal.
- Check: DL9 sends an ADDRESS_ACCESS, an AVC, an HDCP_APM and an EXTENDED
  command.
  - Sent idle, each answers NOT_IMPLEMENTED with the command echoed.
  - Queued behind a stall past its deadline, each answers the same frame,
    byte-exact, inside T-AECP-RESP.
- Arm: `dl-non-aem-forced-status-10`, which restores the round-1 MVU-only
  rule (fails 4).
- Docs: 03 §6, 06 §8.1, both guides and 09 §8.3.

### Item 4: the two surviving kill-seam mutants (R419-1 F2)

- Registry and lock exemption (`KL_aecp_engine.sv:1719-1720`), checked by
  DL10. A REGISTER_UNSOLICITED_NOTIFICATION and a LOCK_ENTITY are each
  queued past their deadline.
  - Each answers its own SUCCESS, byte-exact, with no redirect.
  - The lock is then held.
  - After the unlock, a SET_NAME by another controller is pushed to the
    registered controller.
  - Arms `dl-registry-preempted` and `dl-lock-preempted` (each fails 2)
    prove each exemption alone.
- Owner clear on an honoured kill (`protocol_processor_top.sv:3581`).
  - DL1: after the kill, the RX-slot return releases no hold id again.
  - DL11: across the section, every normal release names a live hold.
  - Arm: `dl-kill-ack-keeps-owner` (fails 2).
- R419-1's own `reviewer_mutants.py`, re-run at the head:
  `r-registry-lock-preempted` and `r-kill-ack-keeps-owner` are now KILLED.
  The three arms R419-1 S1 classed as equivalent still survive.

### Item 5: check IDs and the HZ banner (R418-1 F4, R419-1 F4)

- The deadline checks of `tb/ucpu` are now P20a to P20h. P19 stays
  GET_AUDIO_MAP's; P20 was unused. The campaign, the README, 09 §8.3 and
  06 §8.1 follow.
- The HZ banner now describes the TX-pool stall. The vestigial
  `io.maap_on = false` line is replaced by `io.maap_on = true`, with its
  reason at the line. The doubled `HZ HZ5` prefixes are now single.

### Item 6: suggestions

| Suggestion | Taken or retained | Where, or why |
|---|---|---|
| R418-1 S1 (the MVU preempt trade-off) | taken | 06 §8.1 |
| R418-1 S2 (LOCK_OP's key 0 is also {ENTITY, 0}) | taken | comment at the top's classifier |
| R418-1 S3 (ACMP waiting behind a conflicting AECP hold) | taken, stated, not measured | 08 §4: up to T-BUDGET-AECP-WC plus the forced response, inside T-ACMP-CMD |
| R418-1 S4 (the fan-out row) | partly | The F08.3 row now says "not met as written". The tracking issue is left to the manager, because this round may post only TAKEN, REVIEW READY or STOP. |
| R419-1 S1 (the equivalent arms are defence in depth) | taken | comments in `KL_aecp_ucpu.sv` and `KL_aecp_engine.sv`. Every µprogram was scanned: only `E_AMADD` leads with COMMIT, and it is exempt. |
| R419-1 S2 (TB2 wording) | taken | "all thirteen getters" in the check names and 08 §4 |
| R419-1 S3 (Vivado figures) | taken | the table below and `syn/ooc/README.md` |

### Resource cost, Vivado (R419-1 S3)

The complete processor was synthesized out of context with
`syn/ooc/protocol_processor_ooc.tcl`, using Vivado 2026.1 at the default
8x8 shape, `xc7a100tfgg484-2` and a 10 ns clock. It ran against base
0451d83d and the lane's RTL at 88e3459.

| Resource | Base | Lane | Delta |
|---|---:|---:|---:|
| Slice LUTs | 30,334 | 30,645 | +311 |
| Registers | 31,820 | 31,994 | +174 |
| LUT as distributed RAM | 1,206 | 1,222 | +16 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |

- Most of the new registers are in modules the lane does not edit. Their
  class, key and kill inputs were constants under the stub and the tied-off
  kill face:
  - `u_scoreboard`: 73 -> 169;
  - `u_dispatch`: 903 -> 926;
  - `u_normalizer`: 366 -> 384.
- The top's own registers go from 4,689 to 4,722: the deadline register and
  the boot-hold bit.
- `u_aecp` goes from 6,430 to 6,584 LUTs.
- Both builds have negative OOC slack at 10 ns (-10.114 and -8.922 ns), as
  the earlier records in `syn/ooc/README.md` do. This is area only.

### Round 2 validation

The head is 44a6bb9. The following ran at the head:

- `./scripts/run_suites.sh`: rc 0. 33 suites, 1,017,487 checks, 0 failing.
  - `tb/pp_top` has 8,240 checks (round 1: 8,112).
  - `tb/ucpu` has 415.
  - The µPC map gate passes.
- `./scripts/lint_hdl.sh`, `make check`, `make stale`,
  `scripts/gen_matrix.py --check` and `git diff --check` (from 0451d83d and
  from f963fe9): all rc 0.

The campaigns, `syn/yosys/run.sh` and the four heavy parent builds ran at
49041e6 or 88e3459. Those commits differ from the head only in
`tb/pp_top/README.md` and `syn/ooc/README.md`, which no build, campaign or
gate reads.

- `syn/yosys/run.sh`: rc 0.
- yosys out-of-context `KL_aecp_engine`, LUT-only recipe: 8,135 -> 8,130
  LUT, and 4,583 FF either way.

| Campaign | Result |
|---|---|
| `make -C tb/pp_top aecp-mutants` | 5 controls PASS, 55 arms KILLED (round 1: 30) |
| R419-1 `reviewer_mutants.py` | 3 KILLED (round 1: 1), 3 equivalent survivors (S1) |
| `tb/pp_top/d3_mutants.py` | 83/83 KILLED |
| `make -C tb/adp_engine mutants` | 32/32 |
| `make -C tb/srp_top mutants` | 90/90, assertion coverage 65/65 |
| `tb/pp_top/gsi_mutants.py` | 20 detected |
| `tb/pp_top/name_wr_mutant.py` | killed |
| `tb/acmp_talker/retry_mutants.py` | 62 killed |
| `tb/srp_admission/mutants.py` | every arm detected, controls PASS |
| `tb/desc_mem_guard/mutate.py` | detected |
| `make -C tb/nvm_port figures` | rc 0 |

Parent consumer gates: milan-fpga dev e4b771f9 in a scratch copy, with its
submodules at their pins and the processor at the head. No parent
adaptation is needed. Verilator 5.050. All 16 are rc 0.

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held |
| 3 | `xvlog_gate.py --check` | rc 0, 4 findings == ratchet, none new |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded) |
| 6 | `sw/builder/test_builder.py` | rc 0, all gates pass except 1 not run (it needs a board implementation report not on this host) |
| 7 | `make -C tb/verilator/pp_shadow` | rc 0, 311 checks |
| 8 | `check_port_contracts.py` | rc 0: 48 literal-bound, 59 without a rationale, lowerable by 3 |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0: 73 <= 77 suites without a mutation arm, lowerable to 73 |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp` | rc 0, every RESULT PASS |
| 16 | `make -C tb/verilator/milan_dp_render` | rc 0, leg defects 5/5 |

Gates 6, 7, 15 and 16 ran with the processor at 88e3459. The other twelve
ran at both 88e3459 and 44a6bb9.

### Round 2 parent-visible list

- No top-level port, parameter or register-map change. No RTL port or
  parameter line changed in round 2. No new or renamed RTL file.
- Behaviour on the AECP wire: a command of any AECP message type but
  AEM_COMMAND, whose response memory fails or which is preempted past its
  deadline, answers NOT_IMPLEMENTED with the command echoed.
  - This covers MVU, ADDRESS_ACCESS, AV/C, HDCP APM, EXTENDED and the
    reserved types. Round 1 answered status 10, header only, except on
    MVU's deadline path.
  - For an over-long command (cdl past 524), that echo takes the oversize
    TX slot.
  - The parent's AECP response-contract feature already expects
    NOT_IMPLEMENTED for every non-AEM message.
- Added to round 1's list: the classifier landed in round 1 also makes
  SET_NAME wait for an ACMP read of the stream it names, and makes an ACMP
  read wait for a SET_NAME on its stream. A SET_SAMPLING_RATE, SET_CONTROL
  or ADD_AUDIO_MAPPINGS naming a stream descriptor waits the same way
  before it is refused NOT_SUPPORTED.
- Testbench only: the `tb/pp_top` wrapper gains four scoreboard taps.
  Section HZ runs with a MAAP allocator answering.
- Entry points are unchanged. The AECP campaign grows to 55 arms.

## Round 3

Ruling: issue #81 comment 5929634478, on the reviews R418-2 (POSITIVE) and
R419-2 (NEGATIVE on one MINOR, F5). Three items in the ruled order, one commit
each:

- 97fe22f, item 1, the merge commit (parents 44a6bb9 and 3f3ea56b);
- e4c70b5, item 2;
- d4ca85c, item 3.

There is no port, parameter or register-map change. This round edits no RTL
logic. Its one RTL edit is a comment in the top's classifier banner. The merge
brings main's `KL_pp_maap.sv` change unchanged.

### Item 1: processor main 3f3ea56b merged (C2 and C4)

- `git merge --no-ff` of main 3f3ea56b: #135 (MAAP, lane C2) and #137 (ACMP,
  lane C4). No rebase.
  - Main changes one RTL file, `hdl/maap/KL_pp_maap.sv`.
  - It changes no top port or parameter, and no generator.
  - The top's and `KL_pp_maap`'s port and parameter headers are byte-identical
    at 0451d83d, 3f3ea56b and the head.
- Eight files were changed on both sides. Six merged cleanly:
  - `.gitattributes`, `.github/workflows/hdl.yml`;
  - docs 00 and 09;
  - `tb/pp_top/README.md` and `pp_top_wrap.sv`.
- Two conflicted. Both keep both sides:
  - `tb/pp_top/Makefile` `.PHONY`: main's `maap-internal` beside this lane's
    `deadline`, `d3`, `hazards`, `budget`, `budget-build` and `aecp-mutants`.
  - `tb/pp_top/sim_main.cpp`, the section switch: main's `--acmp-only` and
    `--maap-internal-only` beside `--deadline-only` and `--hazards-only`. The
    default build runs section AC beside DL and HZ, and MP stays opt-in, as on
    main.
- Generated ROMs and tables:
  - `ucode.hex` and `ltn_rom.hex` are build products and are not committed.
    Every run started from a tree with all build products deleted, so both were
    regenerated from `gen_ucode.py` and `gen_ltn_rom.py`.
  - The one committed generated table, `docs/traceability/MODULE_MATRIX.md`,
    regenerates byte-identical: 94 rows, 0 untested.
- Re-measured at the merge commit, all rc 0:
  - `./scripts/run_suites.sh`: 33 suites, 1,018,218 checks. `tb/pp_top` has
    8,288: this lane's 8,240 plus main's 48.
  - All twelve campaigns (the table below).
  - The AECP campaign: 5 controls PASS and 55 of 55 arms KILLED. Every failing
    count equals the `tb/pp_top/README.md` record.
  - The ACMP campaign: 3 goldens PASS and 19 of 19 KILLED. Every failing count
    equals #137's table.
  - No arm was lost in either.

### Item 2: R419-2 F5, as ruled

Clauses:

- 03 §6 F03.7: RO_SNAPSHOT is keyed by the addressed descriptor and "blocked
  only vs in-flight write on the same key".
- IEEE 1722.1-2021 §7.4.76.1: each GET_DYNAMIC_INFO element is handled "as if
  it were an independent command". §7.4.76.2 lists GET_STREAM_INFO among its
  members.
- Milan v1.2 §5.4.2.10, Figure 5.1: the probing and ACMP status of
  GET_STREAM_INFO.

The ruling's first outcome, with no RTL change:

- `protocol_processor_top.sv`, the classifier banner (`:1464-1471`):
  - READ_DESCRIPTOR's NONE key is stated as harmless, because no ACMP step
    writes a descriptor-image field. Its only live fields are
    current_configuration and the name overlay, both written by AECP.
  - GET_DYNAMIC_INFO's NONE key is stated as a known gap. Its GET_STREAM_INFO
    records of a STREAM_INPUT read the listener binding record. That is the
    probing and ACMP status, `lstn_gsi_status_r` (`:3342`), written only by
    the listener record write. ACMP listener steps write it, so the batch is not serialized
    against them, where a stand-alone GET_STREAM_INFO is.
- 03 §6, beside the no-descriptor-key sentence, records the same limitation
  and the HZ6 contrast. Serializing it is left to a later #84 item.
- "What remains" names it under #84, which stays "Relates to".
- Verification: R419-2's `probe_gdi_stream_info.py`, unchanged, on an export of
  e4c70b5. Its results equal the reviewer's:
  - G0: a stand-alone GET_STREAM_INFO STREAM_INPUT 1 waits for a held
    UNBIND_RX of sink 1 (refused 498 clocks).
  - G1: a GET_DYNAMIC_INFO carrying that record is admitted beside it (key
    0xFC00, refused 0 clocks).
  - G2: the same, beside a held GET_RX_STATE.
  - HZ: 179 checks, 0 failures.

### Item 3: suggestions

| Suggestion | Taken or retained | Where, or why |
|---|---|---|
| R418-2 S1 (the 08 §4 hold bound for LOCK_ENTITY and the audio-map edits, with the cross-lock listed) | taken, with S6 | see below |
| R419-2 S6 (the 08 §4 ACMP-wait wording) | taken, with S1 | see below |
| R418-2 S2 (DL8's "540 payload bytes") | taken | the DL8 label, the campaign's named check for `mvu-echo-slot-std`, and the 09 §8.3 row now say "a command padded to 540 payload bytes". Both DL8 arms are still KILLED (4 and 1) |
| R418-2 S3 (the `KL_aecp_notify` fan-out tracking item) | the manager's | per the ruling, it goes to the residue checklist at merge |

The 08 §4 paragraph (S1 and S6) now does three things:

- It lists every AECP hold an ACMP transaction can meet, including the
  MAP_CFG class-wide cross-lock against any stream step (F03.7 rule 5).
- It bounds each hold in one of two ways:
  - A command the deadline preempts holds until its forced response.
  - LOCK_ENTITY and ADD/REMOVE_AUDIO_MAPPINGS are never preempted
    (`ucpu_preempt_w`, `KL_aecp_engine.sv:1719-1720`). They run the rest of
    their own program. The engine's shared gather watchdog
    (`KL_aecp_engine.sv:2342`) bounds every face wait in it, at
    `DESC_MEM_TMO_CYC_P` = 4,096 clocks at the top.
    - LOCK_ENTITY makes 2 registry-face waits, about 82 µs.
    - A mapping edit makes at most 2N + 3 edit-face waits. The engine
      refuses a cdl past 524 before dispatch (`KL_aecp_engine.sv:3215`), so
      N ≤ 63. That is at most 528,384 clocks, about 5.3 ms.
- REGISTER and DEREGISTER are never preempted either, but they meet no ACMP
  transaction.

The conclusion is unchanged: such an ACMP answer can come later than the 50 ms
design budget, though inside T-ACMP-CMD.

### Round 3 validation

The head is d4ca85c. Every command ran with Verilator 5.050 under an
eight-CPU mask, from a tree with every build product deleted, and all are rc 0
at the head:

- `./scripts/run_suites.sh`: 33 suites, 1,018,218 checks, 0 failing. The µPC
  map gate passes.
  - `tb/pp_top` has 8,288 checks (round 2: 8,240; main's +48 arrive with the
    merge).
  - `tb/ucpu` has 415.
- `./scripts/lint_hdl.sh` (41 modules), `make check` (1,004 links), `make
  stale` and `scripts/gen_matrix.py --check` (94 rows, 0 untested).
- `git diff --check` from 0451d83d, from 44a6bb9 and from 3f3ea56b.
- Each `tb/pp_top` entry point alone, each with 0 failures:

| Entry point | Checks |
|---|---:|
| `name-writes` | 85 |
| `gsi-internal` | 6,182 |
| `maap-internal` | 34 |
| `adp-config` | 55 |
| `deadline` | 64 |
| `d3` | 133 |
| `hazards` | 176 |
| `budget` | 56 |
| `--acmp-only` | 43 |

- `make -C tb/ucpu run`: 415 of 415.
- `./syn/yosys/run.sh`: 36 tops.

Every campaign ran in full at the merge commit and again at the head, with the
same result at both:

| Campaign | Result |
|---|---|
| `make -C tb/pp_top aecp-mutants` | 5 controls PASS, 55 of 55 KILLED; every failing count equals `tb/pp_top/README.md` |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 3 goldens PASS, 19 of 19 KILLED; every failing count equals #137's table |
| `make -C tb/maap mutants` | 32 of 32: 3 controls (maap 196, pp_top MP 34, rx_validator 555), 29 arms KILLED |
| `make -C tb/adp_engine mutants` | 32 of 32 |
| `make -C tb/srp_top mutants` | 90 of 90, assertion coverage 65/65 |
| `make -C tb/nvm_port figures` | every measured figure agrees with the tree |
| `python3 tb/pp_top/d3_mutants.py --jobs 2` | 83 of 83 KILLED; the two moved controls fail 17 and 6, as recorded |
| `python3 tb/pp_top/gsi_mutants.py` | 20 detected |
| `python3 tb/pp_top/name_wr_mutant.py` | killed |
| `python3 tb/acmp_talker/retry_mutants.py` | 62 killed, 7 equivalence and 1 performance control |
| `python3 tb/srp_admission/mutants.py` | 12 of 12 |
| `python3 tb/desc_mem_guard/mutate.py` | detected |

ACMP mutation table, re-measured (failing checks, equal at the merge commit and
at the head):

| Mutant | Suite | Failing |
|---|---|---|
| `msg_ok_forced` | acmp_listener / pp_top AC | 93 of 2988 / 1 of 43 |
| `guard_ctlr_dropped`, `guard_talker_eid_dropped`, `guard_talker_uid_dropped` | acmp_listener | 50 / 40 / 30 of 2984 |
| `cdl_not_44_rejected` | rx_validator / pp_top AC | 27 of 555 / 19 of 43 |
| `st_ls_settle_as_withdraw`, `st_ls_sid_da_swapped`, `st_ls_state_none`, `st_ls_vid_dropped` | pp_top AC | 7 of 43 each |
| `st_ls_index_zero` | pp_top AC | 6 of 43 |
| `st_ls_teardown_as_declare`, `bound_view_not_cleared` | pp_top AC | 1 of 43 each |
| `st_ls_teardown_lost`, `bound_view_not_latched`, `bound_dmac_from_sid` | pp_top AC | 2 of 43 each |
| `matcher_da_ignored`, `matcher_vid_ignored` | pp_top AC | 5 of 43 each |

The AECP table is `tb/pp_top/README.md`'s, unchanged. Each arm's failing count
at the merge commit and at the head equals its row: 38 rows were read
automatically, and the 17 shared-row arms were checked by hand.

Parent consumer gates were run in a scratch parent:

- The parent is a `git archive` of a read-only checkout at milan-fpga dev
  ea3fb388. Its tree equals that checkout's (981 index entries).
- Submodules:
  - `gptp-processor` and `third_party/verilog-axis` are at their recorded
    pins.
  - `external` is recorded and uninitialized, as in the checkout.
  - `protocol-processor` is a clone of this branch at d4ca85c, with the
    gitlink set to it.
- #137's `acmp_mutants.py` disposition line (+4 lines in
  `scripts/measure_test_evidence.py`) is applied first. The pin bump owes that
  adaptation, not this lane. Apart from the gitlink, it is the only change
  against ea3fb388.
- The gates ran one at a time with Verilator 5.050. All 16 are rc 0:

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held |
| 3 | `xvlog_gate.py --check` | rc 0: 4 findings == ratchet, none new, pinned at protocol-processor@d4ca85c6 |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded) |
| 6 | `sw/builder/test_builder.py` | rc 0: all gates pass except 1 not run (it needs a board implementation report not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | rc 0: builds of 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0: 48 literal-bound, 59 without a rationale, lowerable by 3 |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0: 72 <= 77 suites without a mutation arm (lowerable to 72), 0 <= 0 unexplained DUT readers, 3 <= 3 wall-clock files |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | rc 0, 9 RESULT PASS, none failing |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | rc 0, leg defects 5/5 |

### Round 3 parent-visible list

- No top-level port, parameter or register-map change. The top's port and
  parameter header is byte-identical to the base and to round 2's head. No RTL
  file is added or renamed. This round's one RTL edit is a comment.
- The merge brings #135 and #137. Their own parent-visible lists apply at pin
  adoption:
  - #137 needs one parent registry entry:
    `protocol-processor/tb/pp_top/acmp_mutants.py` in
    `DUT_READER_DISPOSITIONS` of the parent's
    `scripts/measure_test_evidence.py`, with the line recorded in #137's
    body. The pin bump owes it; this lane does not. It was applied in the
    scratch parent above.
  - #135 needs none: its MAAP change acts only with
    `cfg_maap_internal_i = 1`, which the parent ties to 0.
  - Main's new entry points: `make -C tb/maap mutants`, `make -C tb/pp_top
    maap-internal`, `./obj_dir/Vpp_top_sim --acmp-only` and
    `tb/pp_top/acmp_mutants.py`.
- With main in, the parent's test-evidence ratchet reads 72 ≤ 77 suites without
  a mutation arm (round 2: 73), because `tb/maap` is now armed. It can be
  lowered to 72. The other ratchets are unchanged.
- `tb/pp_top` has 8,288 checks.
- Docs: 03 §6 records the GET_DYNAMIC_INFO limitation, and 08 §4 bounds the
  ACMP wait for each kind of hold. The DL8 check label is renamed.
- No wire behaviour changes in this round.

## Round 3b

Ruling: issue #81 comment 5936567141. Processor main moved to 16ea10ac (PR
#138, lane C5b, AECP dispatch) while round 3 ran. One item, the merge, then
its measurements:

- ee0e2b7, the merge commit (parents d4ca85c and 16ea10ac). `git merge
  --no-ff`, no rebase. It is the head.

The merge resolution edits no RTL logic. Its one RTL edit is a comment in the
top's classifier banner. There is no port, parameter or register-map change.

### Item 1: processor main 16ea10ac merged (C5b)

Main changes the AECP engine, the µCPU, `ucpu_pkg`, `gen_ucode.py` and two
parameter comments in the top. The top's port and parameter header is
byte-identical to main's. With comments stripped, it is identical to
0451d83d, 3f3ea56b and d4ca85c.

Eight files conflicted. Each keeps both sides:

| File | Resolution |
|---|---|
| `.gitattributes` | both whitespace exemptions: `tb/pp_top/mutations/` and `tb/pp_top/aecp_dispatch_mutations/` |
| `.github/workflows/hdl.yml` | both campaign steps: `aecp-mutants`, then `aecp-dispatch-mutants` |
| `tb/pp_top/Makefile` | four builds: default, the DV fixture, C5b's line build third (section AX at `DESC_LINE_BYTES_P` 584) and this lane's timebase build fourth (section TB). The tally line expects four. Both campaign targets and both output variables are kept, every target of both sides is in `.PHONY`, and `clean` removes `obj_line` and `obj_tim` |
| `tb/pp_top/pp_top_wrap.sv` | both tap groups (DL and HZ beside AX) and both define-driven overrides |
| `tb/pp_top/sim_main.cpp` | `load_descriptor_image` takes C5b's appended rows and this lane's SIGNAL_MULTIPLEXER length. Section AX runs beside DL, TB and HZ. `main()` has the fixture, line and timebase builds and every focus flag of both sides: `--aecp-dispatch-only`, `--deadline-only` and `--hazards-only` |
| `tb/pp_top/README.md` | both mutation tables (C5b's AX campaign beside this lane's DL and HZ campaign), and the build table with four rows |
| `tb/ucpu/sim_main.cpp`, `README.md` | the batch dispatch takes either side's flag (C5b's `batch` argument, this lane's `batch_base`). The count is re-measured: 427 |

`aecp_dispatch_mutants.py` and `aecp_mutants.py` are both kept, each with its
own patch directory and make target.

Three edits are needed so that the merge keeps both sides true. None of them
is a textual conflict:

- C5b's arms `ov-oversize-never` and `ov-oversize-at-576` no longer applied.
  At the merge, the engine's `txs_oversize_o` is this lane's three-line
  expression: the MVU fault echo also takes the oversize slot (Milan v1.2
  §5.4.1; REQ-MVU-005, §5.4.3.3 Table 5.19). Both patches are re-cut on the
  merged engine with the same defect:
  - `ov-oversize-never`: the whole request is `1'b0`;
  - `ov-oversize-at-576`: `>=` for `>` on the frame-length term.
  Both arms fail their recorded counts (18 and 4). The other 75 patches of the
  two campaigns apply unchanged.
- Main's #82 makes READ_DESCRIPTOR overlay the current sampling rate (IEEE
  1722.1-2021 §7.2.3), clock source (§7.2.32) and stream format (§7.2.6). The
  round-3 classifier comment and 03 §6 said READ_DESCRIPTOR loses nothing by
  its no-descriptor key because no ACMP step writes a descriptor-image field.
  Both now also name the overlaid rows, which only the AECP engine's state
  port writes: `KL_aecp_dyn_state` has one write port, driven inside
  `KL_aecp_engine`. So F03.7's RO_SNAPSHOT rule ("blocked only vs in-flight
  write on the same key") still loses no conflict for READ_DESCRIPTOR.
- Section TB's build is now the fourth. 08 §4, 09 §8.3, the `tb/pp_top`
  README, the bench and `aecp_mutants.py` say so.

Generated ROMs and tables:

- `ucode.hex` and `ltn_rom.hex` are build products and are not committed.
  Every run started from a tree with every build product deleted, so both
  were regenerated from their generators. `gen_ucode.py` gives 2,048 words and
  87 programs, and the µPC map gate agrees: 59 engine constants, 87 entry
  points.
- `docs/traceability/MODULE_MATRIX.md`, the one committed generated table,
  regenerates unchanged: 94 rows, 0 untested.

### Round 3b validation

The head is ee0e2b7, the merge commit. Every command ran there with Verilator
5.050 under an eight-CPU mask, one at a time, from a tree with every build
product deleted. All are rc 0:

- `./scripts/run_suites.sh`: 33 suites, 1,018,843 checks, 0 failing. The µPC
  map gate, the M9 selftest (9 of 9) and the M9 gate (30 opcodes) pass.
  - `tb/pp_top` has 8,901 checks over four builds: 8,607 default, 20 fixture,
    218 line and 56 timebase.
  - That is 8,288 (d4ca85c) + 8,605 (main, #138's record) − 7,992 (base
    3f3ea56b, #137's record), so no check was lost.
  - `tb/ucpu` has 427 = 415 + 398 − 386, with main and the base measured here
    from exports.
  - The sweep is 1,018,218 + 1,018,518 − 1,017,893.
- `./scripts/lint_hdl.sh` (41 modules), `make check` (1,017 links) and
  `scripts/gen_matrix.py --check` (94 rows, 0 untested).
- `git diff --check` from 0451d83d, 44a6bb9, 3f3ea56b, d4ca85c and 16ea10ac.
- Each `tb/pp_top` entry point alone, each with 0 failures:

| Entry point | Checks |
|---|---:|
| `name-writes` | 85 |
| `gsi-internal` | 6,182 |
| `maap-internal` | 34 |
| `adp-config` | 55 |
| `deadline` | 64 |
| `d3` | 133 |
| `hazards` | 176 |
| `budget` | 56 |
| `--acmp-only` | 43 |
| `aecp-dispatch` (main's) | 915 |
| `aecp-line` (main's) | 218 |
| `line-guards` (main's) | 6 of 6 cases |

- `make -C tb/ucpu run`: 427 of 427.
- `./syn/yosys/run.sh`: 36 tops.

Every campaign ran in full at the merge commit:

| Campaign | Result |
|---|---|
| `make -C tb/pp_top aecp-mutants` | 5 controls PASS, 55 of 55 KILLED. Every failing count equals `tb/pp_top/README.md`: 49 cells read by script, and the six "the same N" cells by hand |
| `make -C tb/pp_top aecp-dispatch-mutants` | 3 controls PASS, 35 of 35 KILLED. Every failing count equals its README cell, read by script |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 3 goldens PASS, 19 of 19 KILLED. Every failing count equals #137's table |
| `make -C tb/maap mutants` | 32 of 32: 3 controls (maap 196, pp_top MP 34, rx_validator 555) and 29 arms KILLED. Every count equals `tb/maap/README.md` |
| `make -C tb/adp_engine mutants` | 32 of 32: 2 controls and 30 arms KILLED. Every count equals `tb/adp_engine/README.md` |
| `make -C tb/srp_top mutants` | 90 of 90, assertion coverage 65/65 |
| `make -C tb/nvm_port figures` | every measured figure agrees with the tree |
| `python3 tb/pp_top/d3_mutants.py --jobs 2` | 83 of 83 KILLED, goldens PASS. Every failing count equals its record: 82 in `tb/pp_top/README.md` and `tb/acmp_nvm/README.md`, read by script, and `validator_admits_held_aecp` in `tb/rx_validator/README.md` (M4, 4) |
| `python3 tb/pp_top/gsi_mutants.py` | 20 detected; golden and restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py` | killed; golden and restored PASS |
| `python3 tb/acmp_talker/retry_mutants.py` | 62 killed, 7 equivalence and 1 performance control |
| `python3 tb/srp_admission/mutants.py` | 12 of 12 |
| `python3 tb/desc_mem_guard/mutate.py` | detected |

No arm was lost in any campaign. The merge changes no input of the SRP,
NVM, retry, srp_admission or desc_mem_guard campaigns: it touches docs, CI,
`hdl/aecp`, `hdl/top`, scripts, `tb/pp_top` and `tb/ucpu` only. The MAAP,
ADP, ACMP and D3 campaigns run arms on the merged `tb/pp_top` bench, and every
count is compared above. The gsi and name-write campaigns record no per-arm
count, and their results equal round 3's.

Parent consumer gates were run in a scratch parent:

- The parent is a `git archive` of a read-only checkout at milan-fpga dev
  d4dd7426. Its tree equals that checkout's (982 index entries, the same tree
  object).
- Submodules:
  - `gptp-processor` and `third_party/verilog-axis` are at their recorded
    pins.
  - `external` is recorded and uninitialized, as in the checkout.
  - `protocol-processor` is a clone of this branch at ee0e2b7, with the
    gitlink set to it.
- #137's `acmp_mutants.py` disposition line (+4 lines in
  `scripts/measure_test_evidence.py`) is applied first. The pin bump owes that
  adaptation, not this lane. Apart from the gitlink, it is the only change
  against d4dd7426, before and after the gates.
- The gates ran one at a time with Verilator 5.050. All 16 are rc 0:

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held |
| 3 | `xvlog_gate.py --check` | rc 0: 4 findings == ratchet, none new, pinned at protocol-processor@ee0e2b72 |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded; 46 sources, self-test passed) |
| 6 | `sw/builder/test_builder.py` | rc 0: all gates pass except 1 not run (it needs a board implementation report not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | rc 0: builds of 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0: 48 literal-bound, 59 without a rationale, lowerable by 3 |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0: 72 <= 77 suites without a mutation arm, 0 <= 0 unexplained DUT readers, 3 <= 3 wall-clock files |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | rc 0, 9 RESULT PASS, none failing |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | rc 0, leg defects 5/5 |

### Round 3b parent-visible list

- No top-level port, parameter or register-map change. The top's header is
  main's, byte for byte, and its declarations equal the lane base's. The
  merge resolution edits one RTL comment and no RTL logic.
- The merge brings #138 (lane C5b). Its own parent-visible list applies at
  pin adoption:
  - `DESC_LINE_BYTES_P` has an enforced legal range, a multiple of 8 from 576
    to 1008. The parent's 576 is the floor.
  - GET_AUDIO_MAP pages of 63 to 71 records are served whole.
  - READ_DESCRIPTOR serves the current values a SET stored (#82).
  - Foreign SETs under lock answer ENTITY_LOCKED with the value in force
    (#53), and REBOOT and the other #74 commands are graded.
  - New entry points: `make -C tb/pp_top aecp-dispatch`, `aecp-line`,
    `line-guards` and `aecp-dispatch-mutants`, and `--aecp-dispatch-only`.
  - It needs no parent registry entry. At this head the parent's
    `measure_test_evidence.py --check` counts 0 unexplained
    DUT-source readers with only #137's line added.
- #137's `DUT_READER_DISPOSITIONS` line is still owed by the pin bump, not by
  this lane. It was applied in the scratch parent above.
- `tb/pp_top` has 8,901 checks over four builds, `tb/ucpu` 427, and the sweep
  1,018,843.
- Docs: 03 §6 and the classifier banner name READ_DESCRIPTOR's overlaid rows,
  and 08 §4 and 09 §8.3 name section TB's build as the fourth.
- The wire changes are #138's. This lane's merge adds none.

## What remains

- #81 acceptance 4 is not done: the F08.1 rows with no RTL (T-IDENT-BURST,
  T-IDENT-REARM, T-CTR-OBSERVE) and a check pinning the 300 s / 60 s
  defaults. So this PR relates to #81 and does not close it.
- #84 is not closed:
  - REGISTRY_OP has no reachable admission conflict at this top, so it is
    graded by HZ1 and HZ8 only. Every other class is graded against ACMP.
  - Acceptance 4 (02 §2 rule 5, the synchronous active-low reset) is not
    done.
  - A GET_STREAM_INFO record of STREAM_INPUT k inside a GET_DYNAMIC_INFO is
    not serialized against sink k's ACMP listener steps, although the
    stand-alone GET_STREAM_INFO is (R419-2 F5).
    - It reads the listener binding record, which those steps write, and the
      batch takes the no-descriptor key.
    - 03 §6 and the classifier comment record this.
    - Serializing it is a later #84 item.
    - READ_DESCRIPTOR's no-descriptor key loses nothing, because no ACMP step
      writes what it reads: a descriptor-image field, or the current sampling
      rate, clock source or stream format it overlays since #82.
  - So this PR relates to #84.
- F03.3's kill count and trace are not added: a status word would be a
  register-map change.
- ACMP's stamped deadline has no kill consumer. The ACMP executors have no
  forced-respond program, and ACMP keeps a design budget, graded by TB5.
  Behind a conflicting AECP hold, an ACMP command can wait past its 50 ms
  design budget, though inside T-ACMP-CMD. 08 §4 bounds each kind of hold.
- `KL_aecp_notify` holds solicited commands behind a whole notification
  class (08 §4 finding). Its tracking item (R418-1 S4, R418-2 S3) is the
  manager's, for the residue checklist at merge.
- Hosted CI, the review of the merge head, and hardware: none run here.
