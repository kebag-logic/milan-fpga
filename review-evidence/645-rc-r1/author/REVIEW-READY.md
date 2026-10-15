[A620] REVIEW READY
Commit: `2639eecf3f94aa1a8be5c922058a05f0a48b1933` (branch `645-bind-recentre` from dev `f6260253`: `4e6b5398` code and tests, `2639eecf` docs; local, not pushed, no PR)

Changed:
- `hdl/milan/milan_datapath.sv`: inside the settle recentre's block, each loopback stream waits from its bind rise for its first accepted `tlast` beat, the beat that primes its queue. At INTERNAL that beat arms the settle recentre, which fires by the unchanged "Fires at INTERNAL" rule (2,048 settled or disengaged ticks, 21.8 s ceiling) and stays the declared discontinuity: counted in `recentres_o`, not in `SLIP_LB`. Under following it arms nothing. No port, register field, parameter or other module changes.
- `tb/verilator/follow_ring`: a `bind` case that replays B17's cycles from PR #741's packet; a fifth default leg (B17 cycles 5, 4 and 9 at INTERNAL, then one bind under CRF following); `make sweep-bind`; controls NO-BIND-ARM, BIND-RISE and FOLLOWING-ARM; `settle_control.py` grades the arm at all four axis rates.
- Docs: `MEDIA_CLOCK_FOLLOWING.md` (the bind arm in the settle-recentre table, "A bind primes the ring where its first PDU lands; at INTERNAL the bind's settle recentre centres it", a new "A bind at INTERNAL" citing B17, the test plan), `TIME_SYNC.md`, `REGISTER_MAP.md`'s `SLIP_LB` row, `TESTING.md`.

**Reproduction, parameters derived from B17** (`review-evidence/645-b17-r1/author/summary/cNN.json`):
- Per cycle: the first PDU's delay after the bind, the first burst's time after that PDU and its peak, and the largest later burst. A burst's PDUs fall 1.538 us per PDU, B17's mean slope.
- The peer runs on the DUT's clock (B17's delta was within 0.0017 ppm), with 0 to 5 us of lateness (B17's p99.9 was 4.4 to 6.1 us).
- B17 bounds the primed margin to 10 to 24.565 us. The first PDU is placed at 16 phases of a media tick; 10 of them prime inside that window.

`sweep-bind`, 320 binds, all ten cycles at 16 phases, with and without lateness:

| | Dev's datapath | With the arm |
|---|---|---|
| Runs passing | 0 / 32 (the reproduction) | 32 / 32 |
| Arms / settle recentres / render recentres | 0 / 0 / 0 | 320 / 320 / 320, firing 2,047.0 to 2,048.0 ticks after the arm |
| The 169 binds priming inside B17's window | each slips exactly one frame (+2 dups), at its first burst | none slips |
| Frames slipped after the ring acts | 414 | 0 |
| Margins after the recentre | - | empty side at least 3.48 ticks, full side at least 4.88 |

Validation (every command unpiped, rc 0; Verilator 5.050):
- `follow_ring`: default 5 legs, b8 48, pullin 18, bind 30 checks, small pulls 10/10, controller PASS at four rates. `make mutants`: 15/15 caught, each new control by its named check. NO-BIND-ARM fails "no SLIP_LB change across the cycle" in all three cycles.
- `chmap_capture` 847, `milan_dp` 11,956, `milan_dp_render` 342 (266 + 71 with `[LAW]`, T30 and T31, and 5/5 leg controls), `tdm8render-pullin` 19 legs 838 checks with 0 loopback slips, `tdm8render-law-boundary` 81/81.
- `milan_dp_mclk` 168 (31/31 controls among them), `milan_dp_gm_steps` 196 (6/6), `capture_coherence` 21,194 (30/30), `pp_shadow` 2,184, `csr` 1,815, `mbx` 2,123, `avtp_parser` 11,201.
- Physical `milan_dp_gptp` 197/0: two declared -5 recentres, startup and reset, with `SLIP_LB` unchanged.
- `suite_tally.py`: 52,122 checks across the 11 sweep suites plus 197 physical, 0 failures.
- `lint_rtl.py --check` (90 <= 90), `xvlog_gate.py --check` (0 findings), `syn/yosys/run.sh` (58/58), `test_builder.py --require-rv32 --require-elaboration` (all gates but gate 11's historical Arty arm, report absent, as before).
- The source and docs gates, `check_em_dash.py --base f6260253` (0 findings over 118 lines), and `git diff --check`.
- Area, out of context, base against head, Vivado 2026.1 under the lock: +3 LUT and +1 FF on the shipping 1x1 TDM8 shape. The shipping 8x8 has no loopback lane and prunes the arm away (0 / 0). Against NFR-RES-01 that is 0.02 % of the image's 12,227-LUT gap, and 0.05 % of the #640 plan's 6,373-LUT margin.

Acceptance criteria (the design round's items):
1. Reproduced first in simulation, matching B17: met (above).
2. The fix as ruled: met; the switch rules are untouched.
3. Checks: met. One counted recentre and no `SLIP_LB` change for every in-window bind. The existing suites pass with their checks unchanged. The planted control fails the reproduction. Area as above.
4. Docs: met, B17 cited by PR #741 and its report.
5. The bench repeat: after the merge, the manager's.

Open risks/questions:
- **The arming window.** For the 42.7 ms between a bind's first PDU and its recentre, the ring keeps its primed margin. 6 of the 151 out-of-window binds, all at the two phases nearest the empty edge with 0 to 5 us of lateness, slipped once in that window, each within about 2 ms of the first PDU. Every one of the 169 in-window binds held. Stated in the design as a limit, not declared. If a ruling wants it removed: prime the ring at its target on the first PDU (a `KL_chan_map_capture` change).
- **Under following a bind arms nothing**, as ruled. The default leg shows B17's cycle-5 burst still slipping that ring once under CRF following. Stated, not declared.
- **One recentre for every stream.** A bind at INTERNAL also recentres the other running streams on a multi-stream shape with the loopback lane; a centred ring takes no step. The shipping 1x1 has one listener stream, and the shipping 8x8 has no lane.
- **Wall clock.** The fifth leg costs 7.1 % (857.6 s against 800.9 s back to back, cold, on four CPUs), projecting the last hosted window to 1193.2 s, under 1260 s. The exact-head hosted run is owed.
- **The physical leg's startup and reset recentres** decide later than in PR #672's evidence (input PDUs 9,822 and 95,986, against output PDUs 6,047 and 92,220). That is consistent with the bind's arm restarting the pending dwell; no base run of that leg was made.

`HANDOFF.md` and `PR-BODY.md` are in the lane's output directory. Stopping here.
