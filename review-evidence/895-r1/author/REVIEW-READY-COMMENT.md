[A775] REVIEW READY
Commit: d023b77a7bf677205e45195e0e1f0daf80d1a4d4 (branch `895-talker-redeclare`, base `66f71326`, #810 round 29's `7f50ee6a` and `b2d39235` merged; for `dev-soft-core`, after #810)
Changed: a split Talker declares only while its SRP parameters are valid (Milan v1.2 4.3.3.1, 5.3.7.4). The composition hands each interface's DA gate (the MAAP adapter's, ACMP's `acmp_declaring`) and range base to SRP every pass (`ctrl_app_srp.c` -> `srp_mbx_gate`). SRP declares a valid source at once, at base + n, on its own interface; withdraws it when validity lapses (LICENCE, then `TALKER_DECL` and `IDLE_SLOPE`, then the Leave); re-declares an unchanged destination at once and a changed one two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8); and swaps an admission change in place. No boot-time Talker Failed. No mailbox contract, RTL, tsn-c-stack, lwSRP or donor change. Tests, plants, a harness arm, the load tables, the ROM ledger and the docs follow.

**Design note (at the head)**

| Source | SRP |
|---|---|
| not valid | declares nothing |
| valid | Talker Advertise when admitted, else Talker Failed code 1; at once, on its own interface |
| validity lapses (no probe for 15 s and no Listener, or MAAP loses or restarts the range) | withdraws: LICENCE, `TALKER_DECL` and `IDLE_SLOPE` before the Leave of its declared type |
| destination changes while valid | withdraws the old first |
| valid again: same destination / changed destination | at once / after `SRP_REDECLARE_CS` = 2,022 cs from the Leave's request |
| admission change | swapped in place, the new type first; a refused join keeps the declared type |
| link reset | a moved source held; an unchanged one at once |

Bounded work: the gate's hand-off is a mask compare and, per valid source, a 6-byte compare and copy, in the polls' base. `declare_sources` makes at most one licence closure, one Leave and one join per source, once per interface per THE TRANSMIT call. The centisecond consumer counts held sources down.

**Validation** (one clean-clone pass on this head; receipts in the lane's output directory):
- every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml` (the four a PR to `dev-soft-core` triggers), each job on its own fresh clone: 139 steps rc 0, 226 not run, each with its reason (hosted orchestration, installs this host carries, the full sweep: no RTL changed), 0 bad; every job tree clean after;
- `test_ctrl_firmware.py --require-rv32 --self-test`: PASS. Control campaign 696 of 696 caught, AECP 227, SRP 392 (the 28 Talker plants at both points among them), 0 escaped;
- `fw_coverage.py --check`: PASS (39 files; `srp_mbx.c` 724/724 lines, 653/653 branches; `ctrl_app_srp.c` 89/89, 72/72). The TSN stack boundary: PASS. The saved-state store gate: 455 tests;
- CPU budget harness at both points, every arm (arm A, answering-every-port, valid-destinations, arm B `aecp`), each built at this head. The image's loadable bytes equal the measurement legs' builds. A group re-run per arm is byte-identical to its measured log. Every measured group was regraded by the head's graders: rc 0, 0 refusals; arm A 7 of 945 and 7 of 996 misses (the merged head's seven, tsn-c-stack #26); every other arm 0; no work pass over the share; no pass over its stated cost;
- `load_grade.py --check` rc 0, `--selftest` 25 of 25; `flip_grade.py --selftest` 131 of 131, `--check` rc 1 by design; `test_ctrl_memory.py` PASS;
- `test_builder.py --require-rv32` rc 0; `cd tests && behave`: 508 scenarios, 2,330 steps passed; the split boot simulation at 1x1 and 8x8, its native controls and its self-test rc 0; `git diff --check` against the base and #810's merged head clean.
- The first pass, on `f44f0b6e`, found SRP's new plant table missing from the TSN stack boundary's registry (`firmware-boundary`); `d023b77a` adds it, and the whole pass above ran again on it.

**Tables**

Costs moved (`load_grade.py`; each the larger of this round's legs and the committed table; the polls' and builds' bounds unchanged):

| Column | 1x1/1if | 8x8/2if |
|---|---|---|
| pin | `record.maap` 90 -> 115, `event.AECP` 60 -> 65 | `record.maap` 130 -> 150, `event.TICK` 40 -> 45 |
| tsn-c-stack#32 | the same, and `base` 155 -> 160, `item.acmp` 120 -> 125, `item.walk` 20 -> 25 | `record.maap` 130 -> 150, `base` 285 -> 290 |

The new work, measured in CPU cycles:
- the gate's hand-off, in the polls' base: at most 15,078 and 27,578, each 422 under `poll_grade.py`'s bound;
- the hold-off countdown, in a centisecond's consumers: at most 19,596 at 8x8/2if, under the 510 us stated;
- the declaration and withdrawal passes: their heaviest work pass is 57,354 and 74,023, under the 200,000 share.

Load and rows (before -> after; `load_grade.py --check` rc 0; `flip_grade.py --check` rc 1 by design, #890/#894):

| Point | Load at the pin | With tsn-c-stack#32 | Ceiling | R4 / R5 / R6 by every source, ms |
|---|---|---|---|---|
| 1x1/1if | 0.486 -> **0.488** | 0.483 -> **0.486** | 0.70, held | 66.12 -> 66.77 (red before) / 35.95 -> 36.24 / 28.67 -> 28.92 |
| 8x8/2if | 0.816 -> 0.817 | 0.767 -> 0.768 | reported against 0.75: over, as before | 346.15 -> 347.69 / 144.15 -> 144.53 / 135.80 -> 136.15 (red before) |

The least row margin by measurement is 9.733 ms at 8x8/2if and 11.255 ms at 1x1/1if (arm A). The Talker rows reach at most 199.4 of 220 ms (a JoinTime's wait plus T_svc).

ROM, RAMB36 (fixture / platform): 1x1/1if 38.5 / 39.5; 1x1/2if 41.5 / 43.0; 8x8/1if 51.5 / 53.0; 8x8/2if **58.0 / 60.0**.
- The platform's 8x8/2if image is ledgered at 60.0 (cap 60.5), with 4.0 RAMB36 = 16,384 B of cold code owed to S14.
- The fixture's 8x8/2if point is ledgered at 58.5, its cap. The fixture's image plans 58.0, but its `answering-every-port` harness arm needs 112,688 B of sram, 48 B past 58.0. The ruling's cuts recover about 30 of those 48 B, so the fallback applies.

Simulation (the CPU budget harness's split SoC, the `valid-destinations` arm; the wire decoded):
- nothing is declared before a probe;
- each source's Talker Advertise carries MAAP's base + n on its own interface (1x1: `91e0f000a134` + 0 and + 1; 8x8: `91e0f000d1a4` + 0 .. 8);
- the 15 s window's end withdraws each source 15.0 to 15.2 s after its probe;
- a range lost to a peer's ANNOUNCE withdraws the interface's sources at the next transmit opportunity, with nothing declared during the hold-off;
- no Talker Failed appears at any time.

Acceptance criteria: 1 met; 2 met; 3 met (9 unit and 3 composition tests, 28 plants each killed by name at both points, coverage 100 % of the changed files); 4 met (1x1/1if 0.488 / 0.486 within 0.70; 8x8/2if reported); 5 met (the ruled caps; every other point at or under 56); 6 is the bench lane's.

Open risks/questions:
- The Domain adoption re-declares in place with a changed vlan_identifier, a FirstValue change 35.2.2.8 does not allow either. Pre-existing and outside #895; to be proposed as an issue.
- Each source is now declared on its own interface only (before, every interface declared every source).
- Thin margins, under bounds this lane did not change: the polls' base, 422 cycles at both points; the 1x1/1if registrar walk, 13 cycles (1,987 of 2,000; this lane does not touch the walk).
- #896: this change removes the board's standing Talker Failed that #896's trigger correlates with. `capture()` and the Listener path are unchanged, so #896's mechanism and fix stay its own.
- `ctrl_split_boot` has no frame input, so the wire evidence is the CPU budget harness's.
