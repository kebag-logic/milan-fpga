# Stress + adversarial campaign — 2026-07-26

Deliberate attempt to break the deployed end-station from a tester's
perspective: repeated stop/start, provisioning storms, illegal CSR access,
engine cycling and boundary values. Run on the AX7101 (8×8 shape) carrying
pre-round gateware `VERSION 0x0001_000B`.

**Every test restored the working binding afterwards.** The board finished
healthy: accepting, `AVTPRX_ERR = 0`, `RST_EPOCH` unchanged at 1 (no MAC reset
was ever provoked), zero kernel errors.

**Includes the MAC-TX wedge drill (AX42)** — see section H. The AX42 fix is
now **validated on silicon**: 9 induced eth-clock-death events, 9 clean
recoveries, TX never wedged on the wire.

## Result

**19 checks + 9 wedge-drill cycles, 0 failures.** Nothing broke it. Two behaviours are worth knowing
about, and one of them explains why the listener blocker took so long to find.

## The tests

### A — stream stop/start

| # | test | result |
|---|---|---|
| A1 | 20 × stop (`CTRL en=0`) then start (stage sid + `CTRL=0x3`), checking acceptance resumes each cycle | **all 20 recovered** |
| A2 | 50 × rapid `en=0`/`en=1` toggle with **no settle time** | accepting afterwards |
| A2b | MAC reset provoked by the above? | **no** — `RST_EPOCH` unchanged |

### B — illegal / adversarial CSR access

| # | test | result |
|---|---|---|
| B1 | `A_STRM_SEL` set to index 15 on an 8-stream build (out of range) | no hang; CSR plane still responsive |
| B2 | read unmapped `0x7FC` and `0xFFC` | both read `0`, no bus hang |
| B3 | write `0xDEADBEEF` to the read-only `VERSION` | ignored, register unchanged |
| B4 | read a snapshot register **immediately** after the SNAP strobe, racing the busy flag | returns a word, no hang |
| B5 | 30 × switch `SEL` mid-read | CSR plane intact |
| B6 | still accepting after all of B | yes |

### C — engine cycling

| # | test | result |
|---|---|---|
| C1 | 10 × lwSRP engine off/on | `LWSRP_CTRL` restored |
| C2 | 10 × chmap arm/disarm | `CHMAP_CTRL` restored |
| C3 | provisioning write **while the engine is off**, then re-enable | recovered after an explicit re-arm |

### D — the entry-0 blocker, triggered on purpose

The most valuable test: rather than observing the blocker, **cause** it.

1. Stage a foreign stream_id for **index 2**.
2. Select **index 0** and issue a route-flags-only `CTRL` commit, with nothing
   staged for index 0.

| # | test | result |
|---|---|---|
| D0 | accepting before the trap | yes |
| D1 | **listener goes DEAF after the cross-index commit** | **confirmed** |
| D2 | explicit re-stage + commit at index 0 recovers it | yes |

This is the root cause demonstrated by **causation** on silicon, not inferred
from a symptom: one stray commit at index 0, with another index's stream_id in
the shared staging pair, and the listener stops accepting. It is exactly what
the simulation predicted, and exactly what `VERSION 0x000F` fixes by tagging the
staging set with the index it was staged for.

### E — eviction semantics

| # | test | result |
|---|---|---|
| E1 | `CTRL en=0` stops acceptance | yes |
| E2 | re-arm recovers | yes |

On this gateware an eviction cannot hand entry 0 back to the ACMP alias — that
is the second half of the defect, and the release-to-alias encoding that fixes
it only exists from `0x000F`.

### F — provisioning storm

| # | test | result |
|---|---|---|
| F1 | 200 back-to-back provisioning writes, **interleaving all 8 stream indices** | survived; recovered on re-arm |
| F2 | MAC reset provoked? | **no** |

### G — boundary stream_ids

| sid written | accepting | why |
|---|---|---|
| all zeros | **yes** | correct — the "a sid was actually staged" guard **suppresses** the table write for a zero sid, so the previous binding survives. This is the guard doing its documented job: it exists so a route-only commit cannot hijack the live alias with the zero reset value |
| all ones | no | correct — a real override that matches no traffic |
| minimal non-zero | no | correct |

## Two behaviours worth knowing

### The diagnostic register can disagree with the match table

After test D put the listener into the deaf state, the window readback at index
0 showed the **correct** stream_id — while the parser was matching nothing.

The engine-backed context readback and `KL_stream_table`'s override entry are
**different structures**, and a cross-index commit can leave them disagreeing.
So *"the window shows the right sid"* does **not** prove the match table holds
it. That is a large part of why this blocker resisted diagnosis for so long: the
first register anyone checks reports the right answer.

The trustworthy evidence is the `0x8B4` parser probe (`VERSION ≥ 0x000D`),
which counts frames *parsed* against frames *matched* upstream of the table, or
simply whether the accept counter ticks.

### A bind edge clears the per-stream error counters

`AVTPRX_ERR` read `0x000B_0000` (11 sequence gaps) before the campaign and
`0x0000_0000` after. Stop/start cycling resets the per-stream counters on the
bind edge — Milan 5.3.8.10 behaviour, and correct, but it means **error counts
are per-binding, not cumulative since boot**. Read them before re-binding, or
they read as a clean slate that was never clean.

## Operational note

800 `devmem` invocations took over ten minutes. The cost is **busybox process
spawn on the softcore**, not the CSR plane — the writes themselves are fast. A
storm test should batch its accesses in one process rather than a shell loop.

## H — the MAC-TX wedge drill (AX42): **the fix is validated on silicon**

The long-standing hazard was that a link bounce wedges the e2 TX path
permanently — *internal TX counters keep ticking while the wire stays empty*, so
a live-counter check is blind to it and only a tap tells the truth. The AX42
logic fix extended the link guard's `eth_rst` scope to cover the PHY-side
`eth_tx`/gtx path. It had never been proven on hardware.

**First: the fix really is on the deployed board.** The shipping netlist wires
the guard's reset into exactly the domain the wedge lives in:

```
assign phy_eth_reset                     = (phy_reset0 | eth_rst);
assign impl_xilinxasyncresetsynchronizerimpl8 = (eth_tx_rst | eth_rst);   // eth_tx domain
assign impl_xilinxasyncresetsynchronizerimpl9 = (eth_rx_rst | eth_rst);
```

**A netdev down/up is NOT this test.** `ip link set eth0 down` detaches the
Linux host plane while the AAF talker keeps transmitting from fabric —
`LINKG_STAT` never moved and the peer's RX never dipped. The guard saw nothing
because nothing happened to the link. Use the purpose-built hook instead:
**`LINK_CTRL[3]` `linkg_freeze`** — *fake eth clock death, drills the full FSM
with no cable* — which is the wedge's actual mechanism.

**The wire truth is the PEER's RX counter.** Since the failure mode is "local
counters lie", the only trustworthy observer is the other board: if this board's
TX wedges, the peer stops receiving.

### Single drill

| t | state | `eth_rst` | tx_alive | rx_alive | bounce |
|---|---|---|---|---|---|
| pre | 0 RUN | 0 | 1 | 1 | 0 |
| +00 | **1 HOLD** | **1** | 0 | 0 | 1 |
| +01 | 1 HOLD | 1 | 0 | 0 | 1 |
| **+02** | **0 RUN** | 0 | **1** | **1** | 1 |

Fault detected, `eth_rst` asserted, **recovered to RUN in ~2 s**, `RST_EPOCH`
unchanged (no MAC-domain reset was needed). Throughout, the peer's RX advanced
97k-114k frames per 5 s with **no dip** — TX never stopped on the wire.

### Repeatability — 8 consecutive cycles

All 8 recovered: peak `LINKG` showed HOLD + `eth_rst` each time, every cycle
returned to RUN with TX ticking, `bounce_cnt` counted every event (1 → 9), and
`RST_EPOCH` never moved. Final state: RUN, carrier up, **0 kernel errors**.

This is the silicon validation roadmap item 0 was waiting for.

### Honest limit

`linkg_freeze` fakes **eth clock death**, which is the wedge's mechanism and the
thing the AX42 reset scope had to cover — so the fix itself is proven. It is not
a physical cable pull, which would additionally exercise PHY autoneg and
link-loss detection. A cable drill remains worth doing, and is now low-risk:
the recovery path it depends on has been exercised 9 times.

## Outstanding

A **physical cable-pull** drill (see the limit above), and the same drills on the
Arty.
