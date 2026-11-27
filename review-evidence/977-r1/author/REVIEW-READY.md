[A825] REVIEW READY
Commit: milan-fpga `095995243bc354b8a41755f3fdfae343511cc668` (`pf-977-1`); tsn-c-stack `5d03517f2ab42416654a8f2be2f71cfc51d82440` (`977-settle`: its two commits on `main` `a795471c`, with `main` `c3bff8f3` merged in; the pin for now); lwSRP `73007b4807977517045e8aa485c61ebb8f5ee843` (unchanged). All of it is local, for the manager to push.

Round 8 applies the owner's decision on round 7's STOP: option (a), ADP's LINK_UP bound stated at 12. It then measures the merged image. Every bound and ruling figure is unchanged.

**1. What changed since round 7's STOP (`8000dae1`)**

`2fe50d53` and `09599524` change only `scenario.py` after `ea52ec11`: its step's docstring, and the fixture's LINK_UP probe's stated model accesses, which the arm tables show and no script carries. The firmware gate, coverage, the twin and memory gates at `ea52ec11` stand for them. The four arms with that probe were regraded, and the harness self-tests and the docs workflow rerun, at `09599524`.

| Commit | What |
|---|---|
| `b9c01152` | `ADP_MBX_LAT_LINK` 12 (`adp_mbx.h`: "6 + the seed's NOW_MS 1 + 3 + 2"; `MAILBOX_SPLIT.md`: `LINK_UP / LINK_DOWN` 12 / 9). These are #1015's lines, word for word (branch `970-discovery` `f4833e16`). #1015's `adp_mbx_set_clock` and its THE DRAW comment are its own change and are not taken: the image is unchanged. |
| `6e2c9116` | `seed-left-at-zero` wrapped as #1015 wraps it, the same plant. A trial merge with #1015's branch (`35d29eb7`) is clean in `adp_mbx.h`, `MAILBOX_SPLIT.md`, `ctrl_mutants.py` and `scenario.py`. The pin's docs and diagram still conflict, because #1015 pins tsn-c-stack `c3bff8f3`; the PR that lands second regenerates them. |
| `ea52ec11`, `2fe50d53`, `09599524` | The CPU budget harness waited 2,200 ms for ADP's ENTITY_AVAILABLE after its link-up. That is the startup draw's 0 to 2 s (Milan v1.2 5.6.3.5.2), but the scenario raises the link after enable, so the draw is LINK_UP's 0 to 4 s (5.6.3.5.3, Table 5.50; tsn-c-stack `ADP_DELAY_MAX_MS`). The window is now 4,200 ms; the five groups that take it (`adp-link`, `adp-gm`, `adp-discover`, `adp-advertise`, `control`) run 2 s longer; LINK_UP's model accesses read 12. `2fe50d53` folds the step's docstring onto one line, keeping `scenario.py` at the 1,000-line module ratchet (`check_py_idiom.py`). #1015 has since made the same fix; `09599524` takes its docstring line and its `fixture.link_up` at 12 model accesses, so `scenario.py` merges cleanly with #1015 too. Round 6's draw happened to fall under 2.2 s. PR 40's seed draws 3.48 s at 1x1/1if: with the old window `adp-advertise` is refused there in both arms (`adp.tmr_delay.if0`: no TMR_DELAY expiry in the window), the negative control; with the new window it passes. |

**2. Results**

| Item | Result |
|---|---|
| every arm, both points, on the merged image (regraded at `ea52ec11`; the four `fixture` arms again at `09599524`) | all 16 exit 0. `none` / `answering-ports`: 103 / 104 groups, 0 refusals, only the 7 ledgered `backlog-owed` misses, 0 passes over THE SHARE (1x1: 179,032 / 163,371; 8x8/1if: 312,803 / 295,955). The small arms: 0 misses. |
| image identity | 16 of 16 harness images byte-identical between `163e467f` (the every-arm run), `6e2c9116` and `ea52ec11`. The models are identical but for their build path and its build-id. |
| `flip_grade.py --check`, both points | PASS, every ruling figure unchanged: 1x1/1if last 132.95 (135), ACMP 29.40 (30; margin 0.60), txL 47.98 (49), ADP 27.79, MAAP 27.89, R5 74.57, R6 72.69 ms; 8x8/1if load 0.757 (0.76), THE TRANSMIT 76.86 of 77 ms |
| `load_grade.py --check` | PASS; 1x1/1if 0.518 (0.70) |
| the 1x1/1if AECP notice item (stated 165 us, 16,500 cycles) | 15,544 cycles (answering-ports), 15,408 (declaring-outputs), 13,746 (none) |
| registrations term (stated 135 / 120 us) | 8x8/1if at most 12,806 cycles a Talker, 135 us by the rule; THE SETTLE at most 4,136 a sink. 1x1/1if at most 11,172 cycles, 120 us by the rule. |
| `kept_grade.py` | PASS at both points, nothing owed |
| `egress_ledger.py --point 8x8-1if` | PASS: all seven rows measured, within by 0.11 to 0.21 ms; `--selftest` 18 mutants PASS |
| firmware gate (`ea52ec11`) | 4 of 4 shards PASS; C0 12 accesses, bound 12; 851 of 851 planted defects caught; `latency-extra-read` caught at 13 |
| `fw_coverage.py --check` (`ea52ec11`) | PASS (40 files) |
| harness self-tests (`09599524`) | PASS: `run.py --self-test` 0 failures; kept_grade 33 checks; load 28 of 28; flip 616 of 616; shape costs 25 of 25, `--check` PASS |
| twin's four targets, `test_ctrl_memory.py`, `plat_ledger.py --self-test` (`ea52ec11`) | PASS (the twin's 0 findings; its plants and the maps leg's plant caught) |
| `plat_ledger.py` (`8000dae1`; images unchanged since) | PASS |
| `ctrl_hot.py --check` | PASS (279 entries, in the recorded order) |
| routes (the merge's platform images; worst corner) | the #818 floor met at every corner, 0 routing errors. 1x1/1if WNS +0.234 / WHS +0.036 ns; 32,693 LUT, 42,793 FF, 82 BRAM. 8x8/1if WNS +0.098 / WHS +0.036 ns; 45,704 LUT, 53,348 FF, 100.5 BRAM. |
| docs workflow (`09599524`, em-dash base `4df125b8`) | 105 steps, 0 failed, no tracked file changed (at `ea52ec11` one step failed, the module ratchet, which `2fe50d53` fixes) |
| tsn-c-stack (`5d03517f`) | quality job 28 of 28 gates (512 caught, 0 escaped; `src/acmp.c` 877/877, 468/468); bare-metal job PASS; merges with `dev-linux` `9e1cd60` without conflict |

**3. Notes for the reviewers**

- `ea52ec11` changes the harness's measurement scripts for five groups. The control is the same image under the old window (refused) and the new one (passes): `receipts/harness/adp-link-up-window-control.txt`.
- The hot list is not relearned at `5d03517f` (integration only). PR 40's `leave_down` and `mix` run only on a transition out of DOWN.
- The adapter's seed is `NOW_MS`. #1015 brings the microsecond clock.

Open risks/questions: none.
