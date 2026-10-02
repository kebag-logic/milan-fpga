<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# milan_dp_mclk: media-clock following at the root (#629)

This suite runs the `milan_datapath` rows of the
[media-clock following design](../../../docs/design/MEDIA_CLOCK_FOLLOWING.md#simulation)'s
test plan. The datapath follows INTERNAL, one AAF Stream Input or the CRF
input, through the real decode, reference mux, AAF clock meter, servo,
restart request and CLOCK_DOMAIN counters.

## Contents

- **[The elaboration](#the-elaboration)** -- The two-stream shape, the 4 MHz fabric and true-ratio audio clocks, the modelled MMCM fine phase shift and the `tu` test double.
- **[The legs](#the-legs)** -- The planted talker offsets and which rows legs A and B run.
- **[Mutants](#mutants)** -- The fourteen named defects, planted once as mutant schemata, each with its short leg and the check it must fail.
- **[Running](#running)** -- The default target, the pool width and the single legs.
- **[Limits](#limits)** -- Where this suite departs from the design's test plan, and why.

## The elaboration

The shape is the shipping AX7101 TDM8 config with a second listener and a
second talker (`gen_mclk_shape.py`, through the real builder). Its clock
sources are INTERNAL 0, CRF 1, AAF input 0 at 2 and AAF input 1 at 3; the
script asserts that on the generated header before anything is elaborated.

| Clock | Rate | Why |
|---|---|---|
| fabric, gtx and PSCLK | 4 MHz | the smallest whole-ns PHC tick Q8.24 holds is 255 ns, so gPTP time is the wheel's |
| audio and TDM | 100 MHz x 391/1591 | the shipping plan, so the TDM frame is the physical 48 kHz grid |

The servo's fine phase shift drives `tb/verilator/mmcm_servo/mmcm_model.h`.
Each step moves the modelled audio clock by 1/59 ns, the servo's own
`GAIN_NUM_P`, so the plant gain is the one the servo is designed for. The
model answers PSDONE 2 PSCLK cycles after PSEN instead of 12; the servo waits
for PSDONE and never counts cycles.

`clkv_double.sv` replaces `KL_ptp_clock_validity` in this suite only. The
ownerless elaboration holds `tu` at 1 structurally, so no C1 counter could
move. The double makes `tu` a register the harness writes.

## The legs

Talkers: AAF input 0 at -6 ppm, AAF input 1 at -8 ppm with the opposite `mr`
level, CRF at -14 ppm. The plan alone is -10.64 ppm.

| Leg | Rows |
|---|---|
| A | AAF input 0 selected from INTERNAL, LOCKED, followed within 0.5 ppm; the CSR words; the echo; one PDU lost in every 0.3 s for 3 s; a 150 ms lock loss and return |
| C | AAF input 0 LOCKED, then W2 onto the locked CRF input, LOCKED and followed within 0.5 ppm |
| B | the CRF input selected and LOCKED; its lock loss and return; the switch sweep at 16 phases of the CRF output; one recentre per switch kind; a switch onto a silent talker; an INTERNAL dwell; INTERNAL with the aligner engaged, the grids at one rate and no junction slip |

Every leg grades the C1 invariant every millisecond: LOCKED equals UNLOCKED
or UNLOCKED + 1. Leg C repeats A's AAF lock so the pool runs the two side by
side.

## Mutants

`mclk_mutants.py` plants the design's fourteen named root defects once, as
mutant schemata. Each copy of `milan_datapath.sv`, `KL_aaf_clock_meter.sv` and
`milan_csr.sv` reads `+MCLK_MUT=<id>`; id 0 is the tracked RTL. Each mutant
runs a short leg that must fail its named check. The schemata at id 0 must
pass every short leg.

| Id | Defect | Short leg | Named check |
|---|---|---|---|
| 1 | the decode kept as the CRF-only compare | `--select` | AAF0: the servo leaves IDLE once the meter locks |
| 2 | the reference mux stuck on `KL_crf_rx` | `--refmux` | AAF0: the trim holds until the meter's rate validates |
| 3 | the aligner left disengaged at INTERNAL | `--internal` | INTERNAL: the packet grid holds the physical grid's rate |
| 4 | the one-cycle unlocked presentation removed | `--w2` | W2: the switch onto a locked CRF passes HOLDOVER |
| 5 | no re-seed on a change of the followed listener | `--switch` | switch: no request pulse at any switch |
| 6 | the meter's raw lock-fall edge as the disruption | `--switch` | switch: no request pulse at any switch |
| 7 | the meter's enable tied high | `--dwell` | (iii) INTERNAL dwell: AAF0's mr toggle raises no request |
| 8 | `disrupt_p` not ORed into the request | `--aafloss` | AAF loss: one request at the meter's timeout |
| 9 | the echo ungated | `--echo` | echo: the unfollowed AAF1's toggle raises no request |
| 10 | C0's level | `--select` | C1: UNLOCKED moves at the switch onto AAF0 |
| 11 | C2's level | `--select` | C1: LOCKED holds until the servo reads LOCKED |
| 12 | the meter's held lock cleared on a sequence gap | `--loss` | loss leg: the servo stays LOCKED through single lost PDUs |
| 13 | the read-window terms missing | `--csr` | CSR: AAFM_STAT reads the meter's status word |
| 14 | the decode table one source short | `--switch` | switch: AAF1 decodes as listener 1 and the meter follows it |

## Running

`make` builds the leg and runs `mclk_mutants.py`, which builds the schemata
and runs the three legs, the controls and the mutants `SIM_JOBS` at a time
(default 4). `make mclk` runs leg A alone; `./obj_mclk/Vmilan_dp_mclk --b`
and `--c` run the others.

## Limits

- The selection is poked into the processor's stored row, as `obj_aclk`
  does. The AECP chain into that row is `tb/verilator/milan_dp`'s
  `[CLKSRC-WALK]`.
- The loss leg is 3 s, not the design's 60 s. One leg costs about 20 s of
  wall time per simulated second. A 60 s leg would take the suite past its
  guard, and its defect shows at the first lost PDU.
- One recentre per switch is graded over 0.8 s gaps. At 4 MHz the settle band
  is one fabric cycle, so a settle can take its 683 ms ceiling.
- INTERNAL is graded after a dwell, not from boot. At 4 MHz the aligner's
  keep-off is a quarter sample (20 cycles) rather than 256, and the TDM
  junction counts skips until the boot pull-in walks the lock clear of the
  walk's crossing, about 2.5 s after boot. `--internal` waits 3.5 s.
  `tb/verilator/milan_dp`'s `obj_aclk` grades INTERNAL from boot at 100 MHz,
  where no junction slip is counted.
- Timestamps are ideal. The meter's own suite owns their error shapes.
