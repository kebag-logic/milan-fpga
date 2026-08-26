# Torture campaign `ax-rv32-g` — the before/after that vindicates the graders

Run concluded 2026-08-05. Device under test: ALINX AX7101, 8x8x8, single-hart
RV32 VexiiRiscv, gateware VERSION **`0x00010022`** (x32f1_eto, WNS +0.017,
all seven 08-03/04 trunk fixes + the AEM-store BRAM fix), booted by a **true
cold power cycle**, no music player running, instrument clean end to end
(**zero** INSTRUMENT-SUSPECT rows). Graded by the harness carrying the
ax-rv32-f H1/H2 fixes (measured-span rates, quantization-aware interval
ceiling, Milan 5.4.2.19 refusals as conformance).

This is the identical plan ax-rv32-f ran on 2026-08-04
([CAMPAIGN_RV32F_TRIAGE.md](CAMPAIGN_RV32F_TRIAGE.md)), so every delta is
attributable to (a) the
grader fixes, (b) the new gateware, or (c) bench state — and the rows say
which.

## Contents

- **[Totals, against rv32-f](#totals-against-rv32-f)** — the side-by-side verdict counts, FAIL 157 → 68, and the headline: rv32-f's 100 false failures did not recur.
- **[The 68, decomposed — every row accounted for](#the-68-decomposed--every-row-accounted-for)** — each FAIL class attributed: 38 known peer counter-semantics rows, the return-leg cluster, a new self-loop harness gap (H3), seven mid-run stale-classifier artifacts, and the single 0.44% late-frame row.
- **[What this run newly established](#what-this-run-newly-established)** — `0x00010022` holds through the full matrix and real power cycles; the audio-loop zeros are proven not contamination; refusals graded first-class; instrument clean throughout.
- **[Genuinely open after rv32-g](#genuinely-open-after-rv32-g)** — the return leg root-caused the same day to OUR ACMP classify dropping talker PROBE_TX_RESPONSEs (`is_lstn_cmd=0`), plus the 0.44% late row, the persistence re-flash, and the NEEDS-HUMAN cable-pull quartet.
- **[Lesson](#lesson)** — why evidence recorded inside every row made the run self-triaging: artifacts identified themselves and re-graded mechanically.

## Totals, against rv32-f

| verdict | rv32-f | rv32-g |
|---|---:|---:|
| PASS | 3,267 | 3,206 |
| SKIP | 2,575 | 2,663 |
| INFO | 277 | 323 |
| **FAIL** | **157** | **68** |
| CONFORMANT-REFUSAL | 2 | 4 |
| NEEDS-HUMAN | 4 | 4 |
| KNOWN-PENDING | 1 | 0 |
| total | 6,283 | 6,268 |

> **HEADLINE: the 100 false failures of rv32-f did not recur.** Not one row
> of `update-law` "impossible 18,048/s" (H1), not one 0.996/s "neither" from
> an unfixed classifier at SHALL severity (H2), and every peer-rate
> accusation in this run records the physically-true ~7,982–8,018/s. The
> before/after is the proof the fix campaign was aimed at the right defects.

## The 68, decomposed — every row accounted for

| class | n | side | disposition |
|---|---:|---|---|
| `xside.peer-counter-semantics` | 38 | peer | **known settled deviation**, correctly attributed: the peer's stream FRAMES_RX keeps the IEEE 1722.1 per-frame reading (~8,000/s) against Milan Table 5.6's interval wording. Predicted by the f-triage; not a new defect, never an artifact — the recorded rates are now physical. |
| `counters.stream_input.frames-rx-advances` | 8 | ax | **return-leg residue (real, external)**: `audio.identity.loop-ch12.t0–t7`, our listener honestly at 0.0/s on the peer's return leg. Ran with NO player this time — **rv32-f's "contamination" hypothesis for these rows is disproven**; this is the known lazy-TA / return-reservation cluster. |
| `counters.stream_input.frames-rx-advances` | 7 | ax | **harness gap H3 (new)**: `loop.axt0-axl1..7` are single-port SELF-loops; 802.1Q-2018 8.6.1 forbids the bridge returning a frame to its ingress port, so these listeners are structurally unreachable and 0.0 is the honest topology. `interval_ticks_agree()` already SKIPs self-loops with that citation; `A_RX_TICKING` did not. Fixed same day (runner: self-loop guard); these become SKIP-with-reason on the next run. |
| `stream.starts-on-bind-alone` + `frames-tx-advances` | 5+2 | ax | **stale-classifier artifacts**: all seven re-grade to band "interval" under the tick-space fix (`bc071253`, landed mid-run after the first artifact appeared — the running process had imported the older module). Offline re-grade: 7/7 flip, 0 survive. |
| `xside.interval-ticks-agree` | 4 | pair | **return-leg residue**: the peer's return talker at wire rate (~72k ticks) while our listener saw zero — one-sided streaming, same cluster as the audio rows. |
| `stream.stop-takes-effect` | 1 | peer | **real, peer**: the peer's return talker still framing at 5,323/s after UNBIND + STOP_STREAMING (`ret.peert0-axl0.disconnect`). The fixed stop-grader catching exactly what it was built for. |
| `counters.stream_input.no-late-or-early-growth` | 1 | peer | **real, load-dependent, the run's one fabric-implicating row**: under the 110 s aggregate-load stress window, the peer's input on pair axt3→peerl6 counted LATE_TIMESTAMP +3,848 of 879,231 frames (**0.44%**) — our talker's frames arriving past their presentation time under load. The other three peer-bound stress pairs did not flow (SKIP), so this is one flowing stream's evidence. Next: reproduce on a `--latency-taps` build for the per-stage breakdown; this build ships without taps. |
| `counters.stream_input.update-law-per-counter` | 1 | peer | **bind-edge measurement**: TIMESTAMP_VALID at 500.7/s on a `connect` step — a stream that started mid-window (~0.6 s of traffic in a 9 s window). Grader refinement candidate (per-frame law vs partial window), not a device finding. |
| `state.restored-after-power-cycle` | 1 | ax | **expected before-picture**: the flashed image predates the E4-aware persist script, so no format replay ran after the DUT power cycle. The corrected script is in the staged image; re-test after its flash. |

## What this run newly established

1. **The gateware holds.** `0x00010022` survived the full matrix, churn,
   multi and stress areas with zero fabric-side findings — including
   three-hour stretches without a single new FAIL — and **real automated
   power cycles**: the entity re-armed and re-advertised after each cycle
   (`adp.alive` clean), retiring the boot-time arming concern as a bench
   one-off (the switch was still converging that once).
2. **The audio-loop zeros are not contamination.** Same 8 rows as rv32-f,
   now with no player anywhere — the failing condition is the peer's return
   leg, coherent with the one-sided pairs and the undead return talker.
   Everything open on the DUT side of this campaign is that ONE cluster.
3. **Refusals are now first-class.** 4 CONFORMANT-REFUSAL rows (set-format
   refusals under bind states the spec licenses) instead of f's mislabels.
4. **The instrument was clean** for the entire run — no verdict in this
   campaign needs an instrument-health caveat.

## Genuinely open after rv32-g

- **The return leg (peer → ax) — ROOT-CAUSED LIVE the same day, and it is
  OURS.** Two refinements first: odd stream indices are the SECONDARY
  (redundancy) network, which the bench does not cable — the odd half of the
  cluster (audio t1/3/5/7, `axl1`) was structurally void, leaving 8 even-index
  rows. A live probe (bind `peert0 → axl0` with the 5.5.1.2 format
  adaptation, ACMP capture on the wire) then showed the whole chain: our
  listener SM sends PROBE_TX correctly; the peer answers **every** probe
  within 1.4 ms with a flawless PROBE_TX_RESPONSE (its stream_id, a MAAP
  dmac, SR VID 2, echoed sequence); and our ACMP RX classify **drops the
  response** — `ACMPL_DBG` (0x6E8) reads `is_lstn_cmd=0` at the classify,
  because the walker admits listener COMMANDS only and has no path for
  talker RESPONSES. The SM re-probes forever, the lwSRP row keeps its stale
  DMAC, no Listener Ready is ever declared, and the peer is correctly never
  licensed. This is the previously-filed "probe response not matched" ACMP
  gap, now with its RTL mechanism and a one-command repro
  (`bash /tmp/retleg3.sh` on the runner host). The peer is exonerated for
  the silence — though its post-stop framing row stands on its own.
- **0.44% late frames under aggregate load** (one stream's evidence). Needs
  the latency-taps build for attribution (talker presentation offset vs
  shaper/queueing under load vs peer strictness).
- **Persistence after power cycle** — the staged image carries the E4 CSR
  replay; flash, cold-cycle, re-run the physical area.
- The **cable-pull quartet stays NEEDS-HUMAN**: the tap control API cannot
  enumerate through the current kernel driver (probed 08-04, user and root),
  so software link-bounce remains closed until the driver-unbind experiment.

## Lesson

The f-triage's discipline — record the evidence inside every row (rate AND
measured span), cross-check graders against each other, and re-run the
identical plan after a fix — is what made this run self-triaging: the seven
mid-run artifacts identified themselves from their own recorded numbers and
re-graded mechanically, and every remaining FAIL carries its attribution on
its face. A campaign whose failures arrive pre-explained is the difference
between a red wall and a work list.
