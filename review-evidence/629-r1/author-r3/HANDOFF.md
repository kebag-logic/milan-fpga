# #629 round 3 handoff ([A486], lane M1, design only)

Status: STOPPED after DECISION (#629 comment 5937429002), awaiting the D8, D5 and D1 rulings (D4 with the owner). Head `a463a1deb9d63614e8bd2134ccd7b2cd541c72ed` on branch `629-media-clock-follow` (PR #631), one commit on `c554ae51b1dcc2285863f0f0117cb025971a594c`. Local, not pushed. Only `docs/design/MEDIA_CLOCK_FOLLOWING.md` changes (+322 / -101); the index row `docs/README.md:72` is unchanged.

Assignment: issue #629 comment 5936791368 (round 3: items 1 to 5, then DECISION and STOP).

## Progress

- [x] TAKEN posted on #629 (comment 5936807981)
- [x] Context read: assignment; R428-2 (5936781329) and R429-2 (5936790644) with their packets and probes; rulings 5935520588; [A482] DECISION 5935490330 and [A483] DECISION 5936327987; round-2b 5936355573 / 5936429406; #629 thread; the live PR #631 body; PR #630 (still OPEN at `26dfc82f`, so the baseline stays cited through the PR); dev still `d4dd7426`.
- [x] Item 1: E8 estimator designed, desk model `meter_rules_model_r3.py` (rc 0, re-run byte-identical)
- [x] Item 2: void rule in the model, +/-2,500 ns row corrected, tolerance stated
- [x] Item 3: switch test redesigned; `mcr_switch_probe/` on the unmodified restart engine, pinned simulator 5.050 (rc 0)
- [x] Item 4: D5 restated (C1 with E8; C2 if E1 is kept)
- [x] Item 5: every suggestion taken (R428-2 S1 to S4, R429-2 S1 to S4)
- [x] Page committed, every gate rc 0 at the head (`gates-head/`)
- [x] PR-BODY.md (first line `[A482]` kept, Round 3 section, "Relates to #629")
- [x] DECISION posted (comment 5937429002), then STOP

## Packet contents

| File | What |
|---|---|
| `taken.md` | the TAKEN comment as posted |
| `meter_rules_model_r3.py`, `.out`, `.rc` | round-3 desk model (standard library, deterministic, at most 8 workers); output sha256 `faed2165...5029` |
| `mcr_switch_probe/sim_switch.cpp`, `run_probe.sh`, `receipt.out`, `receipt.rc` | restart-engine probe; built in scratch (`/tmp/629-a486-mcr2`), not in the packet |
| `gates-head/` | every gate at `a463a1de` (HEAD file, `.out`, `.rc`) |
| `gates/` | the same gates on the uncommitted working tree before the commit (superseded by `gates-head/`; note `check_em_dash` there read `d4dd7426..c554ae51`) |
| `PR-BODY.md`, `decision.md`, `MANIFEST.sha256` | the PR body, the DECISION text, hashes |

## Clause findings (round 3 changes only; rounds 1 and 2 stand)

- IEEE 1722-2016 10.6: "If CRF timestamps are lost due to network packet loss, the media clock free-wheels until the CRF stream resumes" (the qualifier is restored on the page).
- IEEE 1722-2016 10.8 Equation (15) bounds the size of the timestamp error (+/-5 % of a sample period), not its shape; the page now draws the consequence for the rate estimator.
- Milan v1.2 5.3.11.1: "is able to dynamically change the clock source" sits beside "the user is expected to correctly set the clock source", so the permission for an entity-initiated change rests on the absence of a prohibition outside 5.4.2.15's locked scope.

## Code map (file:line, at `c554ae51` = dev `d4dd7426` for RTL)

- Servo: gains `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:228-229`; slew and clamp `:230-231`; lock threshold and windows `:232-233`; FSM `:564-568`; HOLDOVER exit with two-window skip `:571-579`; rate sample `:609`; PI gated on rate valid `:613-615`; error `:643`; integrator `:647`; lock compare `:648`; P term `:669`; slew `:681`.
- CRF receiver: jump bound `hdl/ieee1722/crf/KL_crf_rx.sv:279-294` (384 ns assumption `:283-284`); lock constants `:296-298`; ring read-old/write-new `:320-325`; rate `:523-526`; timeout lock drop `:529-537`; bind rise `:619-624`; `mr` seed `:380`, `:586-587`.
- Restart engine: source-change edge `hdl/ieee1722/avtp/KL_media_clock_restart.sv:213`; request `:236`; merge on `hold_r == 0` `:245`; hold count `:250`; adoption `:261`.
- Root: clock `hdl/milan/milan_datapath.sv:67` (100 MHz); public taps `:704-706`; decode `:1560-1570`; CRF restart term `:3155-3156`; engine instance `:3181-3200` (muxed PDU feed `:3193`).

## Design options and recommendation

| ID | Options | Recommendation |
|---|---|---|
| D8 (new) | E1 (512 ms two-point, round 2), LS1 (least squares over 512 ms), E4 (2,048 ms two-point), E8 (4,096 ms two-point), L (change the servo's lock rule) | **E8.** Only option meeting the lock test under every 10.8-sized error shape without a servo change: worst case 753 ns closed loop at +/-1,426 ns (890 at plant gain 1.2). -1 RAMB18, about +10 to 30 LUT. Rate valid 4.096 s after a restart (was 512 ms); LOCKED 7.3 s after first PDU in the model (3.7 s under E1). |
| D5 (restated) | C0, C1, C2, C3 | **C1 with E8**; **C2 if D8 keeps E1**. |
| D1 | L1, L2 | L1 (unchanged from round 2) |
| D4 | A2-a/b/c/0 | A2-a (with the owner, unchanged) |

Key numbers (model, 120 s, closed loop after first lock, +/-1,426 ns unless stated):

| Shape | E1 + P2 | E8 + P2 |
|---|---|---|
| independent, 300 ppm | 0.960, worst 1,618, 5 drops | 1.000, 197 |
| random sign per group (1,042 ns) | 0.286, worst 4,195, 4 drops | 1.000, 539 |
| 10 ms periodic (1,042 ns) | 0.799, 45 drops | 1.000, 272 |
| 1 s periodic | 0.099, worst 5,703 | 1.000, 316 |
| 2 s periodic | never locks | 1.000, 127 |
| worst case for the estimator | worst 5,736, 3 drops | 1.000, 773 |

Steps: one-sample and half-sample restart at all 16 positions (both); sub-bound 2,000/3,000 ns keep E8 LOCKED (max 432 ns), drop E1. Frequency step: E8 holds LOCKED to about 8 ppm; E1 leaves at 2 ppm.

## Parent-visible change list (round 3 deltas)

- RTL, new: the meter gains the E8 snapshot ring (no RAMB18), the enable, `disrupt_p` (own 100 ms timeout only) and `mr_toggle_p`.
- RTL, root: meter enable from `aaf_clk_selected_r`; the meter's two pulses ORed into the restart request; a `public_flat_rd` tap on that request (harness probe; no port or register).
- Generated row: `hdl/common/gen/adp_shape_defaults.svh` named beside the five config copies.
- Area: total about 390 to 590 LUT, 290 to 450 FF, 0 RAMB18.

## Processor-visible change list

Unchanged from round 2: none in RTL or microcode; documentation and tests under protocol-processor #141.

## Test plan (round 3 deltas)

- Meter suite: design-point row with four shapes (including the worst case), rate within 360 ns, independent within 256 ns; mutants E1, B1, P1. Beyond-tolerance row (random sign +/-1,800 ns at 300 ppm, independent +/-2,100 ns, steps at 16 positions); mutants B3 and void removed. Wrap and history rows use E8's 2,048-interval validity. New pulse row at the meter's ports (exact counts) killing no-re-seed, era-start-as-disruption, `disrupt_p` tied low, and enable tied high.
- `mmcm_servo` with the meter in front: worst-case and random-sign shapes, LOCKED within 10 s and never left; mutant E1.
- `milan_dp` switch row: (i) request tap plus 16 switch phases; (ii) pinned late start (new talker 5 ms after the switch); (iii) INTERNAL dwell. Each mutant fails deterministically at the tap or in (ii)/(iii). The era-start mask has no wire-level mutant (probe: 0 of 13,056).
- Bench B AAF: LOCKED within 15 s and never left during the capture.

## New work found (not filed: outside this lane's allowed actions)

- `KL_crf_rx`'s 512 ms two-point rate has the same worst-case property: closed-loop gain 4.01, so the lock test holds under every shape only below about 255 ns per timestamp, against its own 384 ns assumption. Proposed as a separate issue in the DECISION; recorded in the page's Limits.

## Notes for the next round or reviewer

- The lane checkout's ignored `__pycache__` directories predate this session (18:07 to 18:59 local); left untouched.
- Scratch build directories `/tmp/629-a486-mcr`, `/tmp/629-a486-mcr2` and the clause-text extracts in `/tmp/629-a486-std` are outside the packet.
