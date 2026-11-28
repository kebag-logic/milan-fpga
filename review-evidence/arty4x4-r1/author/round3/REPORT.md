# Arty split 4x4/1if, round 3: the 100 MHz path

[A863]. Branch `arty-4x4-1127`, local only: nothing pushed or posted, no bench, no flash. The final head is in the handoff.
Owner bounds, unchanged: load 0.70, ACMP 30 ms, txL 49 ms, last notice 140 ms, THE SHARE 2 ms.

## 1. Route at 100 MHz

The 4x4 configuration with sys and the control CPU at 100 MHz: the board PLL's 800 MHz VCO divided by 8, so the exact-divider contract holds. The 50 MHz datapath, the 25 MHz MII reference and the audio clocks are unchanged.
Routed through `vivado-slot.sh` at nice 19 and CPUWeight 10, three directives, 4 Vivado threads each.
The floor (#818) is WNS >= +0.030 ns and WHS >= 0 with zero failing endpoints, in all four signoff reports.

Final image, ELF `1b8066e4cd65f446366f6f2574a8e6b099310f7d34f6d8923d861f20a887b09c`, the qualified row:

| Directive | Slow 0/85 C WNS / WHS, ns | Fast 0/85 C WNS / WHS, ns | Failing endpoints | Floor |
|---|---|---|---:|---|
| **ExtraPostPlacementOpt** | **+0.049 / +0.156** | **+1.606 / +0.012** | 0 | **PASS** |
| ExtraTimingOpt | +0.002 / +0.126 | +1.321 / +0.015 | 0 | misses (+0.002 < +0.030) |
| AltSpreadLogic_high | +0.002 / +0.126 | +1.504 / +0.013 | 0 | misses (+0.002 < +0.030) |

- Selected: ExtraPostPlacementOpt. Bitstream `3b27bedd6b27de99169db565a0bbd7186c90506b5da6ee3a8241588ca0e65cc4` (3,271,451 B). The image identity gate and the offline flash-pair input check pass.
- Utilization: 41,858 LUT (66.0 %), 46,808 FF, 15,387 slices (97.1 %), 86 BRAM tiles (70 RAMB36 + 32 RAMB18).
  That is +113 LUT against round 1's 80 MHz baseline (41,745). It is the 100 MHz image's own first baseline for the ~50-LUT rule.
- The setup margin is thin: +0.019 ns over the floor, on one directive of three.
- The first 100 MHz route used an ELF built before the row was installed. It gave identical figures; its receipts are `receipts/route100-first-*`.

## 2. The census at 100 MHz and the row

The AUDIO_UNIT has been 48 kHz alone since round 1 (`1e186eca6`), so every census below runs on the final configuration.

| Census | Egress model | Row it measured at | Result |
|---|---|---|---|
| 2 | instant (the testbench takes a byte a cycle) | basis: round 1's 4x4 cycles restated at 100 MHz (`8b7ba27b7`) | 159/159 native PASS; the rule's row is 125 / 5 / 1250, four statements one rounding step off: build 820 -> 825, retry cold 120 -> 125, notice 185 -> 195, centisecond 200 -> 190 us (installed `45de3bc59`) |
| 3 | instant | `45de3bc59` | 159/159; no cost above census 2's; the merged derivation equals the installed row (a fixed point) |
| 4 | **link rate** (the shipping queue, below) | `45de3bc59` | 159/159; the merged derivation moves only `CTRL_LOOP_TX_MS` 28 -> 29 ms and the harness's AECP timer event 75 -> 180 us (installed `00f1fcd9d`) |

**Why census 4.** A replay of census 3's commits through the shipping transmit queue at 100 Mb/s failed condition (a) of the PR #1020 ruling in AECP's notice bursts: 16 of the first 85 traces. The faster CPU commits 174-octet notices faster than the line and the 10.24 us gasket drain them, so the 512-word AECP ring is full where the census found room. The least slack was -26.7 us.
At 80 MHz (round 1) every trace kept its outcome. So by the ruling's item 3 the census was re-run with egress drained at link rate.
That mode, and the in-tree grade `egress_mii.py` with its planted defects, are #1004's round 10 (`640699e68`). It found the same failure at the 1x1 (11 of 159). This branch merges that head (`f33bfcebf`).

**Fixed point.** `CTRL_LOOP_TX_MS` is read by the firmware only through `SRP_REDECLARE_CS`, where (28 + 9) / 10 and (29 + 9) / 10 are both 3, and by a compile-time assertion. So the product ELF is byte-identical after the move (`1b8066e4...`).
All eight census images rebuilt at the head have native executables byte-identical to census 4's (`receipts/census4-rebuild-identity.txt`). Census 4's traces are therefore the installed row's, as in round 7's second step. Reinstalling the derivation changes no file.

**The derivation** is the unchanged rule (`derive4.py`, round 9's `derive-own.py` at `arty-4x4`). Each cost is the largest of its three censuses' measurements (`merged234-969.json`); #969's disposition applies, and #1022 owns the owed lines.
The rule's first choice by pace, then queued bound, then slice is **queued 125 ms, pace 5 ms, slice 1250 us**. A second row also qualifies: 130 / 5 / 1000.

| Bound | 4x4 at 100 MHz (installed) | Owner | Margin |
|---|---:|---:|---:|
| Long-window load | 0.4689 | 0.70 | 0.23 |
| ACMP | 28.52 ms | 30 ms | 1.48 ms |
| txL | 48.72 ms | 49 ms | **0.28 ms** |
| Last queued notice | 117.68 ms | 140 ms | 22.3 ms |
| THE SHARE, longest whole pass | 173,322 cycles = 1.733 ms (`answering-every-port/notice-burst-1`) | 2 ms | 0.27 ms |

From census 4 alone (no merge) the row is the same: ACMP 28.49, txL 46.74, last 115.74 ms, load 0.4685.
Without the disposition (#1022's control): load 0.82, over 0.70, and no finite last-notice row, at every census.

Installed statements (`ctrl_loop.h`, (1,5,5)): slice 1250, both builds 825, one build 600, SRP unit 300, retry cold 125 / attempt 25 / notice 195 us, queued 125 ms, tx 29 ms, aged step 850, centisecond 190 us, pace 5 ms.

**Qualification** (`tools/qualify4.py`, round 9's qualifier at `arty-4x4`; `receipts/qualification.json`): **PASS**.
It checked:
- all 159 cases native PASS with their trace hashes, with no refusal, share or late finding;
- all eight variant regrades by `run.py --point arty-4x4 --regrade` (rc 0);
- `record_classes` over the legs, PASS;
- every STATED line under #969's disposition, 16 owed lines;
- `arty_grade --point arty-4x4` PASS;
- every installed statement equal to the measured rule's, and the installed model's rows and load equal to the derivation's.

**Bind groups.** No bind bound was ruled for this point. PR #1004's rule gives the 1x1's 400 ms from its `save-bind` group: twice (the group's worst less its 100 ms window), rounded up to 50 ms; and burst saves = floor(530 / save) + 2.
Applied to census 4's `save-bind`: 353.671 ms - 100 = 253.671 ms, so **550 ms** and **4 saves** (`d0f402ee5`). The census's own bind groups fit them: worst in flight 345 ms, the burst 3 saves.

**Cycles at 100 MHz against 80 MHz** (census 2 against round 1's census 1): within ±13 %, mostly within ±5 %. The owner's "cycles unchanged" assumption held to that.

## 3. 100 Mb/s egress at 4x4 traffic

`egress_mii.py` (#1004's grade, in-tree) over census 4's eight build directories, 159 cases: **PASS** (`receipts/egress_mii-census4.log.gz`).
- (a) holds by construction: the census drains at link rate, so every TX_TAIL read the firmware makes is against the link-rate tail. Every case's replay reproduces the testbench's departures exactly (agree 0 ps).
- (b): largest wait 446.76 us (`answering-every-port/notice-every-1`) + one gPTP burst 54.88 us, x 1.05, + fixed path 0.32 us = **527.04 us <= 1000 us**. At most 35 records are queued at once.
- The SR load is four 90-octet AAF frames and the CRF output's 46-octet frame every 125 us. `e7bc55f8a` adds the CRF frame, which #1004's grade did not count, at sixteen times its 2 ms rate (conservative).
- Fixed path: `egress_fixed.py` measures 312.5 ns at an 80 MHz sys (the stated 320 ns holds) and **300.0 ns at 100 MHz**, inside the stated figure (`41166c346` adds the clock option; `receipts/egress-fixed-80-100.txt`).

## 4. Gates

| Gate | Head | Result |
|---|---|---|
| Firmware, four shards, `--require-rv32` | `00f1fcd9d` | PASS |
| Split boot simulation at the 4x4 (100 MHz) | `00f1fcd9d` | PASS, 0 findings |
| Native controls at the 4x4 | `00f1fcd9d` | 6 of 6 |
| Region decode self-test at the 4x4 | `00f1fcd9d` | PASS |
| Split boot simulation at `endstation_arty_split` | `00f1fcd9d` | PASS |
| `test_ctrl_memory`; MII and `lat` host arms (15/15 plants) | `00f1fcd9d` | PASS |
| Standalone self-tests: `rows_tiers` 1033/1033, `load_grade` 28/28, `egress_ledger` 21, `record_classes` 9/9, `shape_costs` 25/25, `arty_grade`, `egress_mii` 17/17, `kept_grade` 32 | `d0f402ee5` | PASS |
| Service self-test, 8 partitions | `d0f402ee5` | 323 of 323 mutants caught, 0 failures |
| `sw/builder/test_builder.py` | `d0f402ee5` | PASS, every gate but gate 11 (its area-calibration report is not on disk; NOT RUN, as in rounds 1 and the 1x1 lane) |
| Docs and idiom: `docs_check`, `check_doc_style`, `docs_inventory --check`, `check_doc_paths`, `gen_toc --check` / `--verify-anchors`, `check_em_dash --base aa53840d9`, `check_gptp_docs`, `check_py_idiom`, `check_cpp_idiom`, `git diff --check` | `ac0ed29bc` | PASS |

Between `00f1fcd9d` and the head the commits change only harness Python (the bind bounds), the fixed-path bench's clock option, and documentation. No firmware source and nothing the firmware, boot, region, memory or host gates read changed.

## 5. Byte identity of the 1x1 and ALINX images

At `e7bc55f8a`, the head side was built again against round 1's base (`aa53840d9`, a shared clone). No firmware or existing-config file changed after it.
- All 66 builder outputs of the six existing configs are byte-identical.
- The product ELFs are byte-identical: `endstation_arty_split` `f17d1a9d...`, `endstation_ax7101_1x1_tdm8` `6e0a5412...`, `endstation_ax7101_8x8` `0f1450ac...`.
- Only `size.json` differs, through `ar` member mtimes and absolute map paths; the maps are equal after path normalisation.
- No HDL, LiteX, mailbox or existing-config file changed in the round. #1004's round 10, merged here, changes only harness, bench and docs files.

## 6. Recorded and owed

- **Latency pair.** The 4x4 keeps the board's 1409/100 ns, measured at an 80 MHz sys (#829). Two of its ingress terms cross into sys, so at 100 MHz it must be measured again on the board. #878 read a 1,465 ns sum at a 100 MHz sys on an earlier image. The service model does not use it.
  The builder suite registers the 1,509 ns sum for this configuration, stated as the 80 MHz measurement standing until then; the configuration's comments say the same.
- **Milan v1.2 5.4.2.7.** Formats that do not fit the 100 Mb/s class-A limit four-up are left out of the advertised set, not refused at SET_STREAM_FORMAT, which allows no bandwidth refusal (round 1's envelope, unchanged).
- **Held-egress ledger at `arty-4x4`: decision needed.** The seven `backlog-owed` rows measure 61.56 to 63.33 ms. #878's held-egress ruling states a ledger for (1,1,2) only, so none is stated here.
  By that ruling's rule (60 ms hold + 1.05 x service, up to 0.01 ms) they would be 62.78, 62.97, 63.14, 63.32, 63.50, 61.91 and 61.65 ms.
- **Bind bounds** above apply PR #1004's ruled rule to a new point; a reviewer should confirm.
- **Dependency.** This branch merges #1004 round 10 (`640699e68`, REVIEW READY, unpushed). If #1004 changes in review, this branch must take the change and re-qualify.
- **One logging slip:** eight freshly rebuilt, empty `c4q/<variant>/results` directories were removed before the log entry. A late entry records it; nothing was lost.
- Scratch: about 8.2 GB of 12. The four censuses' traces are archived compressed: `c1`/`c2`/`c3`/`c4-*.tar.zst`, census 4 sha256 in `receipts/census4-traces-archive.sha256`.
