[A829]

## Description

Adds the Arty split configuration with one AAF talker, one AAF listener and one CRF input.
The system bus and CPU run at exactly 80 MHz, with an 800 MHz VCO, 50 MHz datapath and exact output divisors.
The `(1,1,2)` scheduler point uses its own measured costs: a 1250 us slice and a 10 ms AECP pace.
MII advertises only 100BASE-TX full duplex and refuses to publish an incompatible link mode.
Optional writable timestamp corrections reset to the configured 1409/100 ns pair.
The latency console accepts `lat IIIII EEEEE`, which exactly fills the 16-byte receive FIFO.
Existing scheduler rows and shared AX product images are unchanged. No Linux scheduling point is added.

## Round 9: integration with dev-soft-core `0b594023`

The branch merges dev-soft-core `0b5940237e8de8bd5912db87e5e036a78f59b5a6` by a merge commit, `aa53840d9`. That brings #1015's seeded ADP link-up draw, #1017's 100 ms binding save window and #1019's CI tooling.

- One textual conflict, `sw/firmware/ctrl/test/ctrl_mutants.py`. The base added `CDL_BOUND` inline; this branch had moved the planted-defect fixtures to `ctrl_mutant_fixtures.py`. `CDL_BOUND` joins them there.
  All 880 planted defects keep unique names, and each anchor occurs once in its file. The firmware gate's control campaign catches every one.
- `run.py` reached 1003 lines, three from each side, against the 1000-line module rule. This branch's own docstring paragraph is rewrapped and its duplicate point comment dropped.

### The Arty row on the merged firmware

The full 159-case census on the merged image (147 cases plus #1017's 12 bind groups) was derived by the rule, as in round 7.
Costs are the larger of each measurement and the one before; #969's disposition applies, with #1022 owning the owed lines.
The scheduler choice holds (slice 1250 us, pace 10 ms, queued bound 125 ms, transmit bound 35 ms). Six stated costs rise (`563ee9105`):

| Stated cost | Before | Now |
|---|---:|---:|
| ADP record | 120 us | 125 us |
| ACMP event, and the ACMP timer | 165 us | 175 us |
| LINK event | 190 us | 205 us |
| AECP response and probe items, AECP transmit response | 45 us | 50 us |

No constant in `ctrl_loop.h` changes, so no firmware byte changes: the product ELF rebuilt at the head equals the merge's.
The census at the installed row therefore regrades the same traces, and its derived model equals the installed row: a fixed point after one step.

| Owner bound | Value | Limit |
|---|---:|---:|
| Load | 0.5013971140 | 0.70 |
| ACMP | 29.84 ms | 30 ms |
| txL | 48.90 ms | 49 ms |
| Last queued notice | 117.58 ms | 140 ms |
| Longest whole pass | 143165 cycles, 1.7895625 ms | 2 ms |

`kept_grade.py` passes (5 lines owed to #977, carried at this point by [#1022](https://github.com/kebag-logic/milan-fpga/issues/1022)).
Counting those lines, the no-disposition control finds no qualifying row: the least last notice is 237.0 ms.
The seven held-egress rows measure below their ledger (61.80119 to 63.30645 ms).

### The Arty's bind-save bounds (round 9 measurement; ruled in round 10)

#1017's bind groups grade the in-flight bound and the burst's save count per point. #1009's ruling 3, item 4, states them at 1x1/1if (450 ms; 4 saves) and 8x8/1if (950 ms; 3 saves), not at the Arty.
Measured at the Arty:

| Bind group | Measured |
|---|---|
| Idle store (`save-bind`), ruled 800 ms at every point | 288.8 ms |
| Bind in flight, worst of ten arrival phases | 369.2 ms (`save-bind-in-capture`) |
| 64-bind burst | 239.6 ms; 4 saves, 4 erases |

Round 10 states them by the rule (400 ms, 4 saves), and the link-rate census grades all 12 bind groups against them.

## Round 10: the Arty's bind bounds, the 100 Mb/s egress gate and the carried findings

### The Arty's bind-save bounds
By [PR #1004's ruling](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7221391389), #1009's ruling 3, item 4 applies here with the Arty's own save as the census models it (`7af5117f1`).
The save-bind group's 288.8 ms, less its 100 ms window, is a 188.8 ms save. The rule gives 377.6 ms, stated 400 ms, and 4 saves for the 64-bind burst.
The bench's 1.146 to 1.245 s SET_NAME would give at most a 245 ms save, and 490 ms (500 stated). Section 15 states both; the rule uses the census model.
Measured: in flight at most 369.2 ms, the burst 239.6 ms and 4 saves, the idle store 288.8 ms.

### The 100 Mb/s egress gate
[PR #1020's ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7216971645) makes `T_egress` a held row at 100 Mb/s, and this PR carries its items 2(a) and 2(b) as a [merge gate](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7216972073).
- **The queue.** `egress_queue.hpp` models the shipping transmit path below the mailbox, each figure read from its source by `egress_mii.py`:
  - the control lane's 17-byte crossing;
  - KL_ctrl_split's packer, eight bytes in nine datapath cycles;
  - the 512-cycle minimum-gap gasket, 10.26 us at 50 MHz;
  - the merges with the shape's SR frames (90 bytes each 125 us) and gPTP frames;
  - the store-and-forward FIFO's 512 words and 8 frames;
  - 80 ns a wire octet.
  `gen_mac_tx_model.py` covers MII: its converted MII chain gives the fixed path, 312.5 ns at most over 64 clock phases, stated 320 ns (`egress_fixed.py`).
- **(a) does not carry the instant-egress census.** Replayed through the queue, round 9's census changes the free-space outcome in 11 of 159 cases.
  The firmware reads TX_TAIL in three places, not one: the free-space test (`mbx.c`), AECP's completions (`aecp_mbx.c`) and REBOOT's drain (`ctrl_plat.c`).
  So, by the ruling's item 3, the census ran again with egress drained at link rate through the queue, and each of those reads sees the link-rate tail.
- **The census at link rate**, 159 cases on round 9's image, has no finding. Its costs derive the installed row unchanged, a fixed point.
  The qualification passes with the row checked as `egress-100`, and the no-disposition control still finds no qualifying row (least last notice 237.0 ms).
- **(b)**: the largest commit-to-last-octet wait is 426.47 us (`aecp-largest-notice`). With one whole gPTP burst (54.88 us), times 1.05, plus the fixed path, the row is 505.74 us of its 1 ms.
  The replay, anchored to each record's last mailbox byte, reproduces every departure the testbench printed exactly. Unanchored, it sweeps the SR stream over eight phases.
  At most 19 records queue at once. The two cases with a held egress leave 44 records to the held-egress ledger.
- **Structural.** AECP's admission burst, a notice's 16 registrations at the 1,514-byte largest frame, is the structural maximum FR_NFR 3.4.1 states. The ring holds one such record at a time, so each waits at most 391.5 us, and the burst leaves in 2.18 ms.
  All five rings full of the least record (254 records, the count FR_NFR now states) would leave the last 2.65 ms after commit, at the gasket's pace. See the open questions.
- `egress_mii.py --selftest`: 8 controls, and 9 planted defects each caught by its own control.

### Carried findings
- R928-3-F2: `575118fac` reads a part of exactly the stated limit; `census_extract.py --selftest` (`6e49d1fad`) plants it, a first part of exactly the limit, and the reader's refusal at a limit of the part's size.
- R928-3-F3: a line longer than a part is now refused instead of looping, alone, after an emitted part and with no newline.
- R927-3-F2: `receipts/builder/builder-split.log` records the command, the four heads, every output's SHA256 and the exit status. 22 outputs are identical from `4adfa9dc` to `011aaa6f` and from `aa53840d9` to the head; the merge changes only `gptp_ucode.hex`.
- R928-3-F1: through the publication scrub as patched on 2026-11-27, round 9's extract and this round's each pass unchanged, 0 of 834 files.

## Issue and roles

Relates to #878; its acceptance ruling keeps #878 open for the offset measurement under #1007.
Relates to #665, #969, #977, #1009, #1015, #1017, #1019 and #1022.
Target: `pf-arty-split-1` -> `dev-soft-core`. #977 lands on dev-soft-core first and needs one more integration after this one.
Executor: `[A829]`. Independent reviewers: `[R927]` and `[R928]`; review of this head is pending.

## Source and image

Head `640699e6866602b2a5de5d404c43f3bd4df8037c`. The image is at `aa53840d9`; the link-rate census executables are at `7bc47c0ee`.
The later commits change harness graders, tables and documentation only; no firmware or gateware source changes.
Selected implementation: `ExtraPostPlacementOpt`. Slow WNS/WHS +0.316/+0.156 ns, Fast +1.606/+0.017 ns, zero failing endpoints in all twelve reports. `AltSpreadLogic_high` and `ExtraTimingOpt` also pass (+0.211/+0.104, +1.660/+0.021).
Post-route utilization (selected, routed checkpoint `6aec5a4a...`): 33077 LUTs, 40373 registers, 12959 slices, 78 BRAM tiles.
That is +62 LUTs on round 7's routed 33015, above the ~50-LUT band. The merge's only RTL-side change is the base's gPTP processor pin (`1213ac5b` -> `3ce71b76`, its microcode).
Bitstream SHA256 `82a226e3bce30999c3a8283d58657895f3884f7d7732b1d8a8f14ff711e9ffd8`.
Firmware ELF SHA256 `f17d1a9da8ba6e50a1e8cf0af9b77ed434288a1d0a689a357a0c6a57ecda92cf`: 159844 bytes, `.text` 114240, ROM live 125900 bytes, 44.5/56 RAMB36, 1076 bytes of ROM headroom.
Image identity and offline flash-pair input checks pass.

## Validation

At `aa53840d9`: all four firmware shards with RV32 coverage; Arty native boot (0 findings), native controls 6/6, region self-test; the ten documentation gates. Also 323/323 service mutants and 15/15 MII/`lat` plants.
At the head: the ten documentation/idiom gates; the `rows_tiers`, `load_grade`, `egress_ledger`, `record_classes`, `arty_grade`, `kept_grade`, `census_extract` and `egress_mii` self-tests; and `arty_grade.py`.
The harness self-test passes 8/8 partitions at `1903077be`; `egress_fixed.py` passes on the converted MII chain.

## Reproduce and inspect

The compact census extract of the link-rate census (`receipts/census-extract/`, 834 files, 1.49 GB, largest file 13,999,999 bytes) holds every case manifest, scenario, stimulus, grade and journal. It also holds the observation lines a grader reads, the queue's `EGRESSQ` and `EGRESS` lines and the holds the egress grade reads among them.

```sh
python3 tb/verilator/ctrl_service_budget/receipt_regrade.py census-extract
python3 -I tb/verilator/ctrl_service_budget/egress_mii.py --packet census-extract
```

The first reproduces all 159 grades and passes the cross-case step, identically to the same regrader over the full packet; a copy without `srp-bound` is refused. The second grades the 100 Mb/s row from the published observations: 505.74 us.

## Definition of done

- [x] dev-soft-core `0b594023` merged by a merge commit; conflicts resolved by meaning.
- [x] Arty row derived by the rule on the merged firmware, installed, fixed point reached; owner bounds hold.
- [x] Image routed and timing-qualified at every corner; post-route utilization compared.
- [x] The Arty bind-save bounds ruled, stated, and the bind groups graded against them.
- [x] The 100 Mb/s egress gate: the link-rate census, its fixed point, the row at 505.74 us of 1 ms, and its grader with planted defects.
- [x] The carried findings R928-3-F1, -F2, -F3 and R927-3-F2.
- [ ] The +62-LUT routed delta accepted or explained by review.
- [ ] Independent reviews, hosted checks, local replica, merge-candidate validation, maintainer authorization and post-merge containment.
