# [A529] HANDOFF: milan-fpga #653 (UNBIND_RX response vs MEDIA_UNLOCKED push order)

**Status: STOP at item 1.** The base trace does not show the counters
notification first. On both the AAF and the CRF STREAM_INPUT, the UNBIND_RX
response leaves the MAC before any GET_COUNTERS push that reports the unlock.
Item 1 says to STOP with the trace in that case, so this lane stops here.

Nothing is committed. The branch `653-unbind-order` is still at dev
`fea346e76c2a57ed5cd131af8fc68dfeff57f877` (processor pin `631eeb34`) and the
worktree is clean. The reproduction bench is kept as a patch in this directory.

- Lane: `$LANES/653-unbind-order`, branch `653-unbind-order`, origin
  `https://github.com/kebag-logic/milan-fpga.git`.
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980090994
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980111926
- STOP: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980272602

## 1. Reproduction at base (item 1)

### Bench

The bench is the timed `[NOTIFY]`/`[GSI]` leg of `tb/verilator/milan_dp`
(`make notify`, `obj_notify`). It elaborates the shipping AX 1x1 TDM8 shape:

- sink 0 is the AAF input and sink 1 is the CRF input;
- the processor's millisecond is compressed to 100 fabric cycles; the fabric
  clock stays at 100 MHz;
- the leg holds the datapath counters, the processor's ACMP listener, the
  `KL_aecp_notify` scheduler, the AECP engine and the real MAC TX trunk.

The patch adds a section `[UNB]`, run after `[GSI]` on the same ports. For
each sink it does the following:

1. registers controllers A and B (REGISTER_UNSOLICITED_NOTIFICATION);
2. sends BIND_RX from A, answers the PROBE_TX with SUCCESS, and locks the
   input off clean PDUs at the settled stream_id and address (AAF: 1 PDU
   locks; CRF: 8 PDUs lock);
3. keeps a talker live through the unbind (AAF: one PDU per 125 us; CRF: one
   per 2 ms);
4. waits until the row has pushed nothing for a full second, so the
   per-descriptor one-second limiter is open when the unbind lands, as on a
   long-connected input (this is checked);
5. sends UNBIND_RX from A;
6. stamps, per cycle, every event the assignment names, plus the processor's
   own response queueing and GET_STREAM_INFO pushes.

It grades U1 (the response is SUCCESS), U2 (every push reporting the unlock
leaves after the response, and one does reach each controller) and U3 (the
Table 5.6 pair right after the response, and every push after it).

### Trace (cycles after the UNBIND_RX command's last byte was taken at the MAC RX)

| Event | AAF sink 0 | CRF sink 1 |
|---|---|---|
| Listener queues its response (`lstn_txreq_valid_w`) | +193 | +193 |
| Debounced bind level falls (`bound_hold_r`) | +199 | +199 |
| MEDIA_UNLOCKED written at its source | **+204** (bind-fall walk) | **+9,818,177** (100 ms silence timeout) |
| Source's Table 5.22 pulse | +204 | +9,818,177 |
| Descriptor arbiter delivers {STREAM_INPUT, s} | +205 | +9,818,178 |
| **UNBIND_RX response leaves (last byte)** | **+277** | **+277** |
| GET_STREAM_INFO push to A / to B | +887 / +1,497 | +887 / +1,497 |
| **GET_COUNTERS push reporting the unlock**, to A / to B | **+2,294 / +3,057** | **+9,819,137 / +9,819,900** |

The source counters are `avtprx_unlocked_c` and `crf_unlockcnt_w`. The
source pulses are `avtprx_dirty_p_w[0]` and `crf_dirty_p_w`.

Wire order at base, per input:

- AAF: response, then GET_STREAM_INFO push, then counters push.
- CRF: response, then GET_STREAM_INFO push, then about 98 ms later the
  counters push.

On neither input does the push come first. The owner's report is **not**
reproduced. The run that produced this table is `base-unb-trace-run.log`.

### Why the order holds in this RTL (the chain, at `fea346e7` / processor `631eeb34`)

1. On UNBIND_RX the listener reaches A7 (`KL_pp_acmp_listener.sv:1292`). It
   builds the response and requests TX at `X_BLD_REQ`
   (`KL_pp_acmp_listener.sv:1378-1379`). It then runs `X_WB` (`:1396`) and
   `X_CONSUME` (`:1431`) to `X_IDLE` (`:1435`).
2. The raw bind bit drops at A9 (`:1171`), before the response is built. The
   level the fabric sees is the debounced `bound_hold_r`. It follows the raw
   bit only while the listener is idle
   (`protocol_processor_top.sv:948-952`, `dbg_busy_o = xs_r != X_IDLE` at
   `KL_pp_acmp_listener.sv:761`). So the fabric's bind fall (+199) comes
   strictly after the response is queued (+193).
3. The fabric's bind level feeds everything downstream:
   - the AAF stream table entry 0 (`milan_datapath.sv:5484`), whose fall arms
     the monitor's unlock walk (`KL_avtp_rx_monitor_ctx.sv:857`), which writes
     MEDIA_UNLOCKED (`:1030`);
   - `KL_crf_rx`'s `en_i` (`milan_datapath.sv:5625`, from `acmpl1_bound`
     at `:5155`).
4. The ACMP lane holds the top TX priority class: lane 2 is class 0 in
   `PRIO_MAP_P` (`protocol_processor_top.sv:872`, `:4453`). The processor has
   one packed TX stream, merged into the MAC by one control mux
   (`milan_datapath.sv:7054`). Under talker load, a frame queued after the
   response cannot leave before it.
5. A push needs the AECP engine to gather the counters and build a 174-byte
   body per registered controller, after the scheduler promotes the row
   (`KL_aecp_notify.sv:1033`). The gather follows the unlock write, so any
   push carrying the unlock is requested after the response is already
   pending at top priority.

So in this RTL, a push reporting an unbind-caused unlock cannot overtake that
unbind's response. The same holds under a busy TX slot pool, since the
listener stays busy and the bind level stays high, and under MAC
backpressure, since there is one serial stream.

### What the bench cannot see (for the decision)

These are open questions, not findings:

- **Different build:** the DUT may run a build other than `fea346e7` /
  `631eeb34`.
- **Talker stopped first:** the talker may have stopped before the UNBIND_RX.
  The unlock would then come from the 100 ms silence path and could precede
  the command.
- **Controller-side order:** the controller may log or process ACMP
  responses and AECP unsolicited frames in an order other than wire order.
  One concrete case is a lost multicast ACMP response followed by a retried
  command.

A capture at the DUT port of one disconnect, with frame timestamps, would
settle which of these it is. That capture is a bench item, outside this lane.

## 2. Fix choice (item 2)

**Not made.** Item 1's STOP condition applies before item 2. There is also no
reproduced defect for either candidate to fix:

- (a) holding the unbind's unlock write until the response has left;
- (b) holding a STREAM_INPUT's push while its ACMP transaction is in flight.

Either would change nothing observable on the measured path, since the
response already leads by about 2,000 cycles. A wire-order test could
therefore not be shown red at base, except by a planted mutant that reverses
the order.

## 3. The CRF invariant (item 3): measured, not fixed

- **Mechanism at base:**
  - UNBIND_RX drops `en_i` (`milan_datapath.sv:5625`). That gates `w_hit`
    off (`KL_crf_rx.sv:309`), so nothing more is accepted.
  - `locked_o` and MEDIA_LOCKED do **not** change at the unbind. The unlock
    is counted only by the 100 ms silence timeout (`KL_crf_rx.sv:533-536`,
    `TOUT_CYC_C = CLK_FREQ_HZ_P / 10`), measured here at +9,818,177 cycles.
- **Measured violation:** a GET_COUNTERS right after the UNBIND_RX response
  reads MEDIA_LOCKED 1 and MEDIA_UNLOCKED 0 for the now-unbound CRF input.
  That is `[FAIL] [UNB] CRF sink 1 U3 right after the response:
  MEDIA_UNLOCKED = MEDIA_LOCKED got=0x0 exp=0x1`.
  - Table 5.6 reads LOCKED = UNLOCKED + 1 as "synchronized". So for up to
    100 ms after the unbind the CRF input claims synchronization while
    unbound.
  - After the timeout it reads 1/1, and STREAM_INTERRUPTED stays 0, as
    required.
  - The AAF input reads 1/1 at once: task #32's bind-fall unlock,
    `KL_avtp_rx_monitor_ctx.sv:857`.
  - Acceptance 3 ("at every instant") is therefore **not met for CRF at
    base**.
- **Correction to the issue's pointer:**
  - At `fea346e7`, `KL_crf_rx.sv:597-605` is the rate-ring update.
  - The arm that drops lock without counting is the bind-**rise** arm
    (`:619-670`). It zeroes all ten tallies first, so 0 = 0 is correct
    there.
  - The CRF unbind (`en_i` fall) does not drop lock at all; it waits for the
    timeout.
- **Not fixed, because item 1 STOPs the lane.** A natural parent-only fix:
  - count the unlock on the `en_i` fall while locked, as the AAF path does
    (task #32);
  - this needs no port, register-map or parameter change;
  - because `en_i` comes from the same debounced level, the CRF push would
    then follow the response exactly as the AAF one does (about +2,000
    cycles), and would also show the CRF U3 check green;
  - this needs a decision to re-scope the lane, since this STOP precedes it.

## 4. Tests and planted controls (item 4)

Not committed (STOP). The `[UNB]` section in the patch carries:

- the wire-order check (U2) for AAF and CRF, with a non-vacuity arm (a push
  reporting the unlock must reach each controller);
- the invariant check (U3) right after the response and on every later
  push, including STREAM_INTERRUPTED = 0.

At base, U3 is red for CRF (the "unlock not counted" case, measured, not
planted). U2 is green on both inputs, which is the STOP evidence. No mutation
driver was written.

Bench artifact handled in the patch: at the compressed timebase, the CRF
timeout unlock lands about 98 processor seconds after the unbind. That is
past the 30-60 s Milan 5.4.5.3 departing-controller monitor, which had
deregistered both controllers and suppressed the push in the first run. The
section now has each controller send one command every 10 processor seconds
while it waits.

## 5. Area (item 5)

Not measured: no RTL change was made.

## 6. Gates and evidence

| Run | Command (from `tb/verilator/milan_dp`) | rc | Result |
|---|---|---|---|
| Base build, clean tree | `make notify-build VERILATOR=<pinned 5.050> VERILATOR_JOBS=16` | 0 | built |
| Base run, clean tree | `./obj_notify/Vmilan_dp_notify` | 0 | `checks: 383 failures: 0`, PASS, 19 s (`base-notify-clean-run.log`) |
| Base build + `[UNB]` patch | same `make notify-build` | 0 | built |
| Base run + `[UNB]` patch | `./obj_notify/Vmilan_dp_notify` | 1 | `checks: 417 failures: 1` (the CRF U3 check above), 51 s; trace lines `[i] [UNB] ...` (`base-unb-trace-run.log`) |

No lint, Yosys, xvlog, act or full-sweep run: nothing was committed and no
RTL changed.

### Files in this directory

| File | Bytes | sha256 |
|---|---|---|
| `653-unb-repro-sim_nxn.patch` (the `[UNB]` section, `git apply` on `fea346e7`) | 18,163 | `bc4bf43272f33b52f0c5820924ae4316a1333632e2c2a662a3e35dfb48a06826` |
| `base-unb-trace-run.log` (base + patch run; the trace) | 33,981 | `2e06bcedafa09cb5c139c0aa2801a3846c1f15f763d8dab97f569f921da52124` |
| `base-notify-clean-run.log` (clean base run) | 30,576 | `6a2dbf1bda233ddbb7990d61d8971d313a3029ecb9c5d184fa53cd0dbe7f04b1` |

The four parent-adoption patches (c8, p2-p1, c10, 232) were not used: no
processor branch was made.

### Reproduce the trace

```sh
cd $LANES/653-unbind-order       # at fea346e7, submodules at their pins
git apply <output dir>/653-unb-repro-sim_nxn.patch
cd tb/verilator/milan_dp
make notify-build VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=16
./obj_notify/Vmilan_dp_notify | grep '\[UNB\]'
```

## 7. Decisions needed

1. **Owner's report vs this bench.** Is a port capture of one disconnect
   available, or can the DUT's build and whether its talker was still
   streaming at the UNBIND_RX be confirmed? Until then, no fix is grounded on
   a reproduced defect.
2. **CRF invariant.** Fix it as a re-scoped lane (parent-only, count the
   unlock on the `en_i` fall while locked), with the `[UNB]` section as its
   committed test and the two planted controls (unlock not counted; push
   ahead of the response)? Or file it as its own Issue?
