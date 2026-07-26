# Stress + adversarial campaign — 2026-07-26

Deliberate attempt to break the deployed end-station from a tester's
perspective: repeated stop/start, provisioning storms, illegal CSR access,
engine cycling and boundary values. Run on the AX7101 (8×8 shape) carrying
pre-round gateware `VERSION 0x0001_000B`.

**Every test restored the working binding afterwards.** The board finished
healthy: accepting, `AVTPRX_ERR = 0`, `RST_EPOCH` unchanged at 1 (no MAC reset
was ever provoked), zero kernel errors.

**Not attempted here:** a link flap. That has a documented history of wedging
MAC-TX permanently on this hardware, and the bench is the only path to a flash.
It is listed at the end as the outstanding test.

## Result

**19 checks, 0 failures.** Nothing broke it. Two behaviours are worth knowing
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

## Outstanding

**Link flap** — down/up the interface, verify the MAC recovers, then repeat.
Deliberately not run: MAC-TX has wedged permanently on a link bounce before, and
a wedged board blocks the pending gateware flash. It should be run when a reflash
is already scheduled, so a wedge costs nothing that was not already planned.
