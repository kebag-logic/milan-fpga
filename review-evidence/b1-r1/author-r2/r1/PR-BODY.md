[A438] Bench lane B1 on the dev `13eda870` image: e1 link-publication switch cycles and software grandmaster steps

Refs #599
Refs #394
Refs #387

Evidence only: two new findings pages, no other change. Neither issue closes here. Assignment: https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5884216527

- `docs/findings/599_394_E1_LINK_CYCLES.md`: #599 acceptance 4 and #394 acceptance 2 (e1 only).
- `docs/findings/387_SOFTWARE_GM_STEP.md`: #387 acceptance 4 with the software grandmaster (owner decision 2026-09-28).

## Verdicts (operator measurements; the reviews decide)

| Acceptance | Verdict | Evidence |
|---|---|---|
| #599 acceptance 4, first half | PASS: a switch cycle drops the DUT PHY link | The firmware's BMSR publication (MAC_STATUS and `link_status`) fell 2.31-2.56 s after OFF and returned 37.07-37.32 s after OFF. The inline capture point does not hold the link up. |
| #599 acceptance 4 | PASS | 10/10 cycles: LINK_DOWN +1 and LINK_UP +1 (DUT 2/1 to 12/11); MAC_STATUS `0x0d`, `0x00`, `0x0d` each cycle |
| #394 acceptance 2, e1 only | PASS | 10/10: reservation, both bindings, asCapable and MEDIA_LOCKED recovered with no reboot and no re-bind. LINK_DOWN, LINK_UP and MEDIA_UNLOCKED +1 per cycle. gPTP 0.544-1.786 s against 5 s. Restart time recorded, not a #75 verdict |
| #387 acceptance 4 | PASS, with one recorded deviation | 10 PHC steps (+9.99 ms takeover, -10.00 ms release) on a running, locked CRF stream. No `mr` change, MEDIA_RESET +0, neither listener unlocked, `A_MCSRV_STAT` LOCKED throughout. Steady again 3.00-4.53 s after each step. Deviation: a 2.0 s asCapable loss after every step |

## Per-cycle table (seconds after OFF)

| Cycle | OFF | MAC_STATUS down | MAC_STATUS up | LINK_DOWN / LINK_UP | GM return | gPTP recovery | First DUT / peer PDU | Link-up to first DUT / peer PDU | CRF licence off / on | Bindings |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 20.90 | 1.81-2.06 | 36.82-37.07 | +1 / +1 | 39.78 | 0.544 | 45.05 / 46.12 | 7.97 / 9.05 | 13.41 / 45.17 | held |
| 2 | 20.97 | 2.06-2.31 | 36.82-37.07 | +1 / +1 | 40.02 | 1.555 | 45.22 / 47.96 | 8.15 / 10.88 | 15.15 / 45.42 | held |
| 3 | 20.88 | 2.31-2.56 | 36.83-37.08 | +1 / +1 | 39.88 | 1.704 | 51.91 / 49.17 | 14.84 / 12.09 | 14.90 / 51.92 | held |
| 4 | 20.86 | 2.06-2.31 | 37.07-37.32 | +1 / +1 | 39.81 | 1.513 | 43.06 / 45.60 | 5.74 / 8.28 | 16.40 / 43.17 | held |
| 5 | 20.86 | 1.81-2.06 | 36.82-37.07 | +1 / +1 | 39.85 | 0.720 | 45.27 / 46.71 | 8.19 / 9.64 | 19.65 / 45.42 | held |
| 6 | 21.06 | 2.31-2.56 | 39.10-39.35 | +1 / +1 | 42.10 | 1.750 | 46.30 / 46.65 | 6.95 / 7.29 | 6.67 / 46.44 | held |
| 7 | 20.88 | 1.81-2.06 | 36.59-36.84 | +1 / +1 | 39.88 | 1.463 | 45.25 / 45.58 | 8.41 / 8.75 | 11.65 / 45.43 | held |
| 8 | 20.85 | 1.81-2.06 | 37.08-37.33 | +1 / +1 | 39.81 | 1.523 | 45.10 / 46.20 | 7.78 / 8.88 | 16.41 / 45.17 | held |
| 9 | 20.87 | 2.31-2.56 | 36.82-37.07 | +1 / +1 | 39.90 | 1.427 | 49.06 / 49.41 | 11.99 / 12.33 | 10.90 / 49.17 | held |
| 10 | 21.05 | 2.06-2.31 | 36.82-37.07 | +1 / +1 | 40.04 | 1.786 | 45.36 / 45.67 | 8.29 / 8.60 | 18.16 / 45.42 | held |

## Per-step table (seconds after the software-grandmaster start)

| Run | Edge | DUT PHC step | Grandmaster time step | `tu` set / steady clear | Step to steady | `tu` episodes | asCapable lost | DUT / peer `mr` changes | MEDIA_RESET talker / listener | DUT / peer MEDIA_UNLOCKED | Servo state; discards |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | takeover | +9.988 ms | +9.994 ms | 4.05 / 7.34 | 3.25-3.54 | 3 | 4.55-6.55 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 10 to 13 |
| 1 | release | -10.004 ms | -9.997 ms | 50.82 / 54.10 | 3.25-3.53 | 3 | 51.57-53.57 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 13 to 14 |
| 2 | takeover | +9.988 ms | +9.995 ms | 3.78 / 7.06 | 3.25-3.53 | 2 | 4.28-6.28 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 14 to 17 |
| 2 | release | -10.005 ms | -9.998 ms | 50.55 / 54.08 | 3.50-3.78 | 3 | 51.30-53.30 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 17 to 19 |
| 3 | takeover | +9.988 ms | +9.995 ms | 3.78 / 8.06 | 4.25-4.53 | 3 | 4.78-6.78 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 19 to 20 |
| 3 | release | -10.004 ms | -9.996 ms | 50.59 / 54.12 | 3.50-3.78 | 3 | 50.84-52.84 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 20 to 21 |
| 4 | takeover | +9.987 ms | +9.995 ms | 3.78 / 6.81 | 3.00-3.28 | 2 | 4.53-6.53 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 21 to 24 |
| 4 | release | -10.004 ms | -9.997 ms | 50.80 / 53.83 | 3.00-3.28 | 3 | 51.55-53.55 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 24 to 25 |
| 5 | takeover | +9.987 ms | +9.995 ms | 3.78 / 7.07 | 3.25-3.54 | 3 | 4.03-6.03 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 25 to 26 |
| 5 | release | -10.003 ms | -9.996 ms | 50.60 / 54.14 | 3.50-3.78 | 3 | 51.11-53.11 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 26 to 27 |

## Method notes

- Identity gate: VERSION `0x00020060`; ROM `acad92b9`, QSPI payload `d84bce7b` (seed `eto`), AEM `93742dd2`; ENTITY and CONFIGURATION byte-exact to the AEM image; grader 10/10.
- The BMSR was read through the firmware's own 125 ms poll, as published in MAC_STATUS and the `link_status` CSR. This image has no console MDIO command, and a manual read needs CSR writes, which the bench rules forbid. The two words agreed in all 7,520 console rounds.
- Software grandmaster: the reference gPTP implementation 4.4, built from a hash-checked tarball in a temporary directory on the controller host. It aligned the host clock to the switch, advanced it by 10 ms and announced priority1 240 for 50 s. Five runs gave five takeovers and five releases.
- Only OUT4 was switched. The DUT was never flashed, reset, rebooted or power-cycled, and its reset epoch stayed 1. Each action held the bench lock for its own duration only.

## Restore

All restored and proven:

- Outlets as found: OUT1 and OUT3 OFF, the other five ON.
- The switch is grandmaster again.
- Both bindings are unbound and the DUT is back on INTERNAL.
- The start and end censuses agree on 53/53 non-counter reads.
- The final tap capture carries no CRF.
- The grader passes 10/10.
- The controller host is back to its found state: no daemon, the same timestamp configuration, and its clock frequency and time trajectory restored. Its temporary files are removed.
- The temporary capture module is unloaded.

## Validation (all rc 0 at the committed head, foreground, not piped)

`docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 13eda870`, `check_doc_paths.py` (pinned Markdown environment); `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, `git diff --check`.

## Open questions

1. Proposed follow-up issue: every PHC step of the locked servo is followed by a 2.0 s asCapable loss. The published peer delay read 0 ns at takeovers and 4,039-4,701 ns at releases. Each loss adds `tu` episodes and GPTP_GM_CHANGED and CLOCK_DOMAIN counts. Media was unaffected; the mechanism is not established.
2. #387's counted render re-base is not observable on this bench: no AAF stream and no tally CSR.
3. As found, the reference peer was in configuration 1 at 48 kHz and two outlets were OFF, unlike PR #600. Both were left as found.
