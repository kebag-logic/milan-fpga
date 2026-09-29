[A438] REVIEW READY
Commit: `f9eab5bf55ca4471e6e48ae3d38018d7e804505b` on `b1-bench-0929` (one commit on dev `13eda870`; local, not pushed).
Changed: two new findings pages only: `docs/findings/599_394_E1_LINK_CYCLES.md` (#599 acceptance 4, #394 acceptance 2) and `docs/findings/387_SOFTWARE_GM_STEP.md` (#387 acceptance 4). No other doc, RTL or firmware change.
Validation: all rc 0 at the head, run in the foreground and not piped:
- In the pinned Markdown environment: `docs_check.py` (0 findings), `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 13eda870` (0 findings over 671 added lines) and `check_doc_paths.py`.
- `ci_scope.py --selftest`, `check_baremetal_only.py --check` (0 findings), `check_feature_status.py --self-test` (46/46) and `git diff --check`.
Acceptance criteria (operator measurements; the reviews decide):
- Identity gate PASS: VERSION `0x00020060`; ROM `acad92b9`, QSPI payload `d84bce7b` (seed `eto`) and AEM `93742dd2`. ENTITY and CONFIGURATION are byte-exact to the AEM image, entity `020000fffe000001`. Grader 10/10.
- #599 acceptance 4, first half: PASS. A switch cycle drops the DUT PHY link. The firmware's BMSR publication (MAC_STATUS and `link_status`, sampled read-only) fell 2.31-2.56 s after OFF and returned 37.07-37.32 s after OFF. The inline capture point does not hold it up; no owner decision needed. OUT4 re-proven in the same cycle.
- #599 acceptance 4: PASS, 10/10 cycles at +1/+1. LINK_UP/LINK_DOWN went from 2/1 to 12/11, and MAC_STATUS went `0x0d`, `0x00`, `0x0d` each cycle.
- #394 acceptance 2 (e1): PASS, 10/10. The reservation, both bindings, asCapable and MEDIA_LOCKED recovered with no reboot and no re-bind. MEDIA_UNLOCKED went +1 per cycle. gPTP recovered in 0.544-1.786 s against 5 s. Restart time recorded, not a #75 verdict.
- #387 acceptance 4: PASS with one recorded deviation. Five software-grandmaster takeovers and releases stepped the DUT PHC +9.99 ms and -10.00 ms on a running, locked CRF stream. No `mr` changed, MEDIA_RESET stayed +0 and neither listener unlocked. `A_MCSRV_STAT` read LOCKED throughout, and the DUT was steady 3.00-4.53 s after each step. The original grandmaster was restored and proven.
- Restore PASS: outlets as found; switch grandmaster; both pairs unbound and INTERNAL restored; census 53/53 equal; controller host and tap returned to their found state; bench lock free.

Per-cycle table (seconds after OFF):

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

Per-step table (seconds after the software-grandmaster start):

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

Open risks/questions:
1. **Proposed new issue (manager):** after every PHC step the DUT lost asCapable for 2.0 s, 0.22-0.97 s after the step. The published peer delay read 0 ns at takeovers and 4,039-4,701 ns at releases. Each loss adds `tu` episodes and GPTP_GM_CHANGED and CLOCK_DOMAIN counts. Media was unaffected; the mechanism is not established.
2. #387's counted render re-base is not observable on this bench: no AAF stream and no tally CSR.
3. As found, the reference peer was in configuration 1 at 48 kHz and OUT1/OUT3 were OFF, unlike PR #600. Both were left as found.
4. The capture driver again needed the temporary rebuild PR #600 used; it has been unloaded.
