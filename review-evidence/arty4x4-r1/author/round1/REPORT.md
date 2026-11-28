Status: STOP. No row of the 4x4/1if point meets every owner bound. Every other step of the round is done, the fixed point is not reached, and no row is installed.

# Arty split 4x4/1if, round 1 (desk)

[A863]. Branch `arty-4x4-1127` on `aa53840d9` (PR #1004's round-9 integration merge). Local only: nothing pushed or posted, no bench, no flash.

## 1. Envelope at 100 Mb/s

Milan v1.2 4.3.3.2 Table 4.4's recipe gives each stream's reservation: MaxFrameSize, +22 octets of header and FCS, a 68-octet floor, +20 of preamble and gap, x 8000 x 8.
The class-A limit is 802.1Q 34.3.1's default 75 %, 75,000 kb/s, on each direction of the full-duplex link.
Receipt: `receipts/envelope.json` (`tools/envelope.py`).

| Format (PCM32) | kb/s per stream | 4 streams + CRF, kb/s | % of the 75 % limit | Fits four-up |
|---|---:|---:|---:|---|
| 48 kHz 1ch | 5,824 | 28,928 | 38.6 | yes |
| 48 kHz 2ch (default) | 7,360 | 35,072 | 46.8 | yes |
| 48 kHz 4ch | 10,432 | 47,360 | 63.1 | yes |
| 48 kHz 6ch | 13,504 | 59,648 | 79.5 | yes |
| 48 kHz 8ch | 16,576 | 71,936 | 95.9 | yes |
| 96 kHz 4ch | 16,576 | 71,936 | 95.9 | yes |
| 96 kHz 6ch | 22,720 | 96,512 | 128.7 | no |
| 96 kHz 8ch | 28,864 | 121,088 | 161.5 | no |
| 192 kHz 2ch | 16,576 | 71,936 | 95.9 | yes |
| 192 kHz 4ch and up | 28,864 and up | 121,088 and up | 161.5 and up | no |

The CRF stream is 5,632 kb/s (Table 4.4's row). gPTP egress (Sync and Follow_Up at logSyncInterval -3, Announce and the three Pdelay messages once a second) is about 16 kb/s on the line.

**Egress** (the four talkers and the CRF output): 35,072 kb/s reserved, 46.8 % of the class-A limit; the builder states the same figure (`build_plan.md`, "reserved 35072000 bps"). About 64.9 Mb/s is left for best-effort and control frames.

**Ingress** (the four listeners and the CRF input): the worst admissible case is four 8-channel 48 kHz streams and the CRF, 71,936 kb/s, 95.9 % of the limit.

**What the image offers, and why.**
- Stream Outputs: the 2-channel 48 kHz Base format only. The framer is stereo: the I2S front-end supplies one pair, and `framer_wire_channels` caps the wire width by the supply. SET_STREAM_FORMAT on an output admits only the declared shape, so any other format is refused there (served since VERSION 0x0053). An 8-channel output format would fit the wire four-up at 48 kHz, but this fabric cannot frame it.
- Stream Inputs: the 2-channel 48 kHz Base format current, and Milan v1.2 6.4's 48 kHz family (1, 2, 4, 6, 8 channels) appended by the builder as one up-to entry. All of them fit four-up. No 96 or 192 kHz Stream Input format is advertised. Section 6.4 would then owe that rate's 6- and 8-channel formats, which do not fit four-up (96 kHz 8ch: 121,088 kb/s).
- CRF input and output: Milan 7.3.2's format, which Milan 7.2.3 requires once two AAF inputs exist.

**Specification conflict, for a decision.** The task says formats that do not fit are refused at SET_STREAM_FORMAT. Milan v1.2 5.4.2.7 names two refusals, STREAM_IS_RUNNING and BAD_ARGUMENTS for mapped channels that would vanish, then says "In all other cases a PAAD-AE shall return SUCCESS". IEEE 1722.1-2021 7.4.9.2 allows a reject only by example; Milan removes that latitude.
So a bandwidth refusal of an *advertised* format is not available to a PAAD-AE. This image instead advertises only formats that fit four-up, and an unadvertised format is refused as it is today. Nothing in the firmware was changed for this. If the owner wants a bandwidth check at SET_STREAM_FORMAT as well, that needs a ruling against 5.4.2.7.

## 2. Build

- `configs/endstation_arty_split_4x4.yaml` (`7aef00c4a`): `endstation_arty_split`'s shape four times over at `control.placement: split`, 80/50 MHz, the 1409/100 ns latency pair, MAC 02:4b:4c:4b:4c:02, plus `crf_output`.
  - Its own hash-derived model id `0x001BC5F7283384B4`, no pin. A new model, IEEE 1722.1-2021 6.2.2.8.
  - Descriptors: 5 STREAM_INPUT, 5 STREAM_OUTPUT, 4 + 4 stream ports, 40 AUDIO_CLUSTER, 4 AUDIO_MAP, 6 CLOCK_SOURCE.
  - The builder's 9 lwSRP attribute rows fit its 9 contexts.
- Generated: `configs/generated/endstation_arty_split_4x4/gen/adp_shape_defaults.svh`. No other tracked generated file moved.
- Scheduler shape (1,5,5) in `ctrl_loop.h`. Census 1 ran at the 1x1's statements.
- The builder's pre-Vivado estimate says "OVER (worst LUT 84.9 %)". It says the same of the shipping AX7101 8x8 (85.4 %, same die), and #827 records that it misprices stream pairs, so the route below decides.

### Firmware memory (product ELF at the census-1 row)

| Item | 1x1 (section 15) | 4x4 |
|---|---:|---:|
| `.text` | 113,908 | 114,844 |
| `.rodata` | 11,558 | 17,638 |
| `.bss` | 45,136 | 61,168 |
| ROM live extent | 125,572 | 132,672 |
| SRAM live extent | 53,456 | 69,552 |
| ROM allocation, RAMB36 | 31 | 32.5 (banks 128 K + 2 K) |
| SRAM allocation, RAMB36 | 13.5 | 17 (banks 64 K + 4 K) |
| Total, of 56 | 44.5 | **49.5** |

ROM headroom before the next 2 KiB granule: 448 bytes. ELF `3bc41eb7fd1528f2b8409ee9a9a915ebeaf495a359345bec6288f92cf7d993e9`, 168,120 B.

### Fit and routes

The census-1 image (ELF `3bc41eb7...`, the 48/96/192 kHz AUDIO_UNIT; see section 3 for the final ELF), routed at the three #818 directives through `vivado-slot.sh` at nice 19, CPUWeight 10 and 4 Vivado threads, one at a time.
The floor is WNS >= +0.030 ns and WHS >= 0 with zero failing endpoints, in all four signoff reports. Slow and Fast are the speed models; 0 and 85 C are power metadata.

| Directive | Slow 0/85 C WNS / WHS, ns | Fast 0/85 C WNS / WHS, ns | LUT | FF | Slices | BRAM tiles | Floor |
|---|---|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt (selected) | +0.486 / +0.179 | +1.665 / +0.054 | 41,745 | 46,802 | 15,333 | 86 | PASS |
| ExtraTimingOpt | +0.126 / +0.104 | +1.656 / +0.011 | 41,734 | 46,802 | 14,934 | 86 | PASS |
| AltSpreadLogic_high | +0.065 / +0.104 | +1.656 / +0.011 | 41,734 | 46,802 | 14,933 | 86 | PASS |

The selected route has the best worst-corner WNS, as at the 1x1. Of the xc7a100t it uses 65.8 % of the LUTs, 36.9 % of the FFs, 63.7 % of the BRAM tiles (70 RAMB36 + 32 RAMB18), 13 DSPs and 96.7 % of the slices.
Against the 1x1's routed 33,015 / 40,369 / 13,791 / 78: +8,730 LUT, +6,433 FF, +1,542 slices, +8 BRAM tiles.
**Baseline for the ~50-LUT routed-total rule: 41,745 LUT, 46,802 FF, 15,333 slices, 86 BRAM (ExtraPostPlacementOpt).** 4x4 is new, so this is its first baseline. It is the census-1 image's: the AUDIO_UNIT change since moves the ELF, not the gateware, and a qualifying row would move the ELF again.
The image identity gate and the offline flash-pair input check pass for all three (`receipts/route-graded-images.json`). Nothing was flashed.

## 3. Service budget: STOP

### The point

`arty-4x4`: `endstation_arty_split_4x4` at one interface, shape (1,5,5), CPU and bus exactly 80 MHz. It has its own entry in every per-point table: `run.py`, `record_classes.py`, `shape_costs.py`, `load_grade.py` (counts: 5 sources, 5 sinks, 16 registrations, 12 counter descriptors, 24 notices), `poll_grade.py`, `rows_tiers.py`, `rows_grade.py`, `edit_rows.py` and `arty_grade.py --point arty-4x4`, under the same owner bounds.
The census ran at the 1x1's statements, the only basis available before a measurement; the harness tables and the `ctrl_loop.h` row still state them, because no derived row qualifies.

### Census 1

159 native cases, the eight image variants, 6 legs at CPUWeight 10 (`receipts/census1-completed.json.gz`, runner `tools/census-run.py`, round 9's runner at `arty-4x4`, measurement only).
- Every case native PASS; no harness refusal; no pass over THE SHARE. The longest pass is 151,744 cycles, 1.897 ms of 2 ms (`answering-every-port/notice-every-5`).
- No late row, save, burst, notice or join miss.
- Over budget: the seven `backlog-owed` held-egress rows, 61.92 to 64.13 ms (1x1 ledger: 61.99 to 63.51). No 4x4 ledger exists; stating one by #894's hold-plus-service rule would need a ruling at this point.
- 19 cases measured costs over the 1x1 statements: polls base, SRP record apply up to 74,557 cycles, build-one.
- #1009's bind groups ran with the same scratch-only sentinels as round 9 (no Arty bind bound is ruled); no verdict drawn.

### Costs by the rule

Measured CPU time plus 5 %, rounded up to 5 us (`tools/census4.py`, round 9's `census7.py` at (1,5,5); `receipts/census1-969.json`).

| Work | 1x1 statement, us | 4x4 measured by the rule, us |
|---|---:|---:|
| SRP record | 300 | 375 |
| Ordinary AECP record | 290 | 275 |
| Paced AECP record (accepted SET_CONFIGURATION) | 335 | 520 |
| Long AECP record | 1105 | 1145 |
| ACMP record | 245 | 265 |
| ADP record | 120 | 140 |
| MAAP record | 125 | 150 |
| ACMP timer event | 165 | 205 |
| MAAP timer event | 165 | 190 |
| Centisecond work | 160 | 245 |
| Poll base | 235 | 290 |
| Both MRPDU builds | 1035 | 1025 |
| One MRPDU build | 660 | 750 |
| Aged SRP step | 1060 | 1060 |
| LINK event | 190 | 250 |
| Retry cold / attempt / notice | 130 / 30 / 230 | 150 / 30 / 235 |

#969's disposition, as at the 1x1: ten `srp-kept` and `srp-bound` measurements of the owed kinds over the installed statements are recorded as owed and kept out of the maxima. These are SRP record applies to 84,070 cycles, polls base to 35,422 and build-one to 68,299. #1022 owns them at the Arty point.

### Derivation by the rule, and the table

`tools/derive4.py` (round 9's `derive-own.py` at `arty-4x4`). For every queued-notice bound 125/130/135/140 ms and every pace 1 to 13 ms, the slice is chosen by `slice_choice` and the rows by `rows_tiers`. A row is kept only if the pace rule, the queued rule and every owner bound agree. Full table: `receipts/derive1-969.json` and `receipts/derive1-no969.json`.

**Result: NO QUALIFIED MODEL, with the disposition and without it.**

With #969's disposition (long-window load 0.578):

| Queued, ms | Pace, ms | Slice, us | last, ms | ACMP, ms | txL, ms | R4L, ms | R5 / R6, ms | Owner findings |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 125-140 | 1-4 | 400 | no finite row | 38.23-43.47 | 126.52-154.55 | 83.85-128.85 | 173.9-178.1 | last, ACMP, txL |
| 135 | 5 | 950 | 267.92 | 38.33 | 97.56 | 144.44 | 104.6 / 99.8 | last, ACMP, txL |
| 140 | 5 | 800 | 277.38 | 38.18 | 97.41 | 144.29 | 104.4 / 99.6 | last, ACMP, txL |
| 125-140 | 6 | 1200 | 215.06 | 38.37 | 84.87 | 159.73 | 95.8 / 88.6 | last, ACMP, txL |
| 125-140 | 9 | 1200 | 205.95 | 37.89 | 68.34 | 204.73 | 89.7 / 87.3 | last, ACMP, txL |
| 125-140 | 12 | 1200 | 202.79 | 37.64 | 58.71 | 249.73 | 89.0 / 86.8 | last, ACMP, txL |
| 125-140 | 13 | 1200 | 201.93 | 37.39 | 58.71 | 264.73 | 88.8 / 86.6 | last, ACMP, txL |
| **Bound** | | | **140** | **30** | **49** | 238 | 90 | load 0.70, THE SHARE 2 ms |

Every one of the 52 candidates misses last notice, ACMP and txL. The least each reaches is 201.93, 37.39 and 58.71 ms, each 7 to 62 ms over its bound. No pace up to 13 ms satisfies the pace rule. No candidate's queued rule agrees with its bound: every finite last-notice row is over 140 ms.

Without the disposition (the #1022 control, every owed line counted): load 1.027, over 0.70; no finite last-notice row at any candidate; least ACMP 43.12 ms, least txL 73.30 ms.

**Why it misses.** Both the counts and the costs move. The same search at the 1x1's own costs, with only the 4x4's counts, already finds no row: least ACMP 29.84 and least txL 48.79 ms, never in the same candidate (`receipts/floor-search.json`). The measured costs then add 3 to 10 ms: SRP record +25 %, centisecond +53 %, paced record +55 %, one MRPDU build +14 %. This lane has no rule-conforming lever left: the clock is ruled at 80 MHz and the bounds are the owner's.

### Egress at 100 Mb/s (the PR #1020 ruling, items 2(a) and 2(b), without the injected frame)

`tools/egress_replay.py` replays every commit (`TXC`) of all 159 census traces through a model of the shipping transmit queue:
- KL_mbx_tx's commit-order merge at one byte per 80 MHz cycle, the contract's ring sizes (ADP 128, ACMP 256, AECP 512, MAAP 128, SRP 512 words) and TX_TAIL moving after a record's last byte;
- the control lane's 512-cycle gasket at 50 MHz;
- the round-robin frame merges with the gPTP plane and with the data lane;
- MilanMAC's store-and-forward FIFO (512 x 8 B, 8 frames);
- the line at 80 ns an octet with preamble, padding, FCS and gap;
- the 4x4 SR frames (four 90-octet AAF frames every 125 us, a 46-octet CRF frame every 2 ms) and gPTP (Sync and Follow_Up every 125 ms, Announce and three Pdelay messages a second), at five phases;
- the testbench's own holds, held here too.

| Check | Result |
|---|---|
| (a) every commit's free-space test keeps its census outcome | **PASS**, 159 traces, every phase |
| (b) worst commit-to-last-octet wait | 535.88 us (`answering-every-port/notice-burst-6`) |
| (b) + 5 % + fixed path 2 us | **564.67 us <= 1000 us, PASS** |

Records whose wait spans a testbench hold (the held-egress rows) are excluded from (b) and counted.
For (a), the replayed ring is checked at the later of the commit less 20 us and the census ring's own first room for the record.
This mattered once. In `backlog-owed`, an ACMP commit 17.35 us after the 60 ms hold's release passes only because the test instant is tied to the census's room. A blanket 20 us allowance put the test inside the hold and refused it.
The tool's self-test (13 cases, including that case both ways) passes.

Limits, stated:
- This is a lane-local grader. The ruling puts the in-tree grader, with its planted defects, in PR #1004's next round, and this lane will adopt it.
- The fixed path, 2 us, is an analytic bound: the scan, header, crossings, core and PHY stages, about 1.2 us. It is not the ruling's "measured on the shipping chain at the MII rate"; that measurement is owed with #1004's grader.
- The replay runs at the census-1 statements. A qualifying row would need it again on its own census.
For comparison only, round 9's 1x1 `backlog-owed` trace replays at the 1x1's SR load: (a) PASS, (b) 331.48 us (350.06 us).

### What a ruling would need to choose from

This lane does not choose. The candidate decisions, none taken:
- Re-scope the Arty point, for example to 2x2/1if: the counts alone already put 4x4 over at the 1x1's costs.
- Firmware cost work at 4x4: the SRP record, centisecond, paced-edit and build costs listed above.
- Re-rule the Arty clock: the 80 MHz ruling stands, and this lane measured no other.

#1022 stays the owner of the owed registration lines at this point as well. Its acceptance names "the 4x4/1if target", so its control derivation here is the no-disposition table above.

## 4. Byte identity of the 1x1 and ALINX images

Built at base `aa53840d9` (a shared clone in scratch, same submodule pins) and at this head, with the same recipe:
- The builder's outputs for all six existing configs (`arty_4x4`, `arty_8ch`, `arty_current`, `arty_split`, `ax7101_1x1_tdm8`, `ax7101_8x8`): 66 files, every one byte-identical.
- The linked product ELF of each existing split config:

| Config | ELF sha256, base = head |
|---|---|
| `endstation_arty_split` | `f17d1a9da8ba6e50a1e8cf0af9b77ed434288a1d0a689a357a0c6a57ecda92cf` (= round 9's product) |
| `endstation_ax7101_1x1_tdm8` | `6e0a54124483adfadd04e8e6f62d296bdf884794b197d0ed9dc24c71de49fd56` |
| `endstation_ax7101_8x8` | `0f1450acefdd7fa0173d1de3221f8c5a6456e59d96fc99611b5121b1c26a2c3f` |

- Only `size.json` differs, through the hashes it lists of `libc.a`/`libcompiler_rt.a` (`ar` member mtimes) and `ctrl_app.map` (absolute paths). The maps are equal once the build path is normalised.
- No HDL, LiteX, mailbox or existing-config file changed (`git diff --stat aa53840d9..HEAD -- hdl sw/litex sw/mailbox configs/*.yaml` lists only the new config). So every existing gateware input is unchanged by construction.

## 5. Gates

The 1x1 lane's set, at the 4x4 shape where it has one. All run at nice 19 / CPUWeight 10 from `tools/gates.py`, `tools/gates-4x4.sh`, `tools/service-selftest.py` and `tools/builder-suite.sh`.

| Gate | Head | Result |
|---|---|---|
| Firmware, four shards, `--require-rv32` (RV32 coverage) | `1c158ec15` | PASS |
| Split boot simulation at `endstation_arty_split_4x4` | `11f903bd4` | PASS, 0 findings |
| Native controls at the 4x4 shape | `11f903bd4` | 6 of 6 as required |
| Region decode self-test at the 4x4 shape | `11f903bd4` | PASS |
| Split boot simulation at `endstation_arty_split` | `1c158ec15` | PASS, 0 findings |
| `sw/litex/test_ctrl_memory.py` (memory gates) | `1c158ec15` | PASS |
| MII and `lat` host arms (round 9's set) | `1c158ec15` | PASS, 15 of 15 plants |
| Service self-test, 8 partitions | `1c158ec15` + the two point checks (`4d6011177`) | 323 of 323 mutants caught, 0 failures |
| `rows_tiers`, `load_grade` (28/28), `egress_ledger`, `record_classes`, `shape_costs`, `arty_grade` self-tests | `1c158ec15` | PASS |
| `arty_grade.py` (arty-1x1) / `--point arty-4x4` | `11f903bd4` | PASS / refused (the STOP) |
| `sw/builder/test_builder.py` | `11f903bd4` | PASS, all gates but gate 11 (its area-calibration report is not on disk; NOT RUN, as in the 1x1 lane) |
| `test_clock_contract.py` | `1c158ec15` | PASS |
| Docs: `docs_check`, `docs_inventory --check`, `check_doc_style`, `check_doc_paths`, `gen_toc --check` and `--verify-anchors`, `check_em_dash --base aa53840d9`, `check_gptp_docs` | `11f903bd4` | PASS |
| Idiom: `check_py_idiom`, `check_cpp_idiom`; `git diff --check aa53840d9 HEAD` | `11f903bd4` | PASS |

Between `1c158ec15` and the head, the commits change only documentation, harness self-test checks, the builder suite's tables and the 4x4 configuration's AUDIO_UNIT rate list. No firmware source and no file the firmware, 1x1 boot, memory or host gates read changed in that span. The three gates that read the 4x4 configuration ran again at the head.
"The twin" in the 1x1 lane's list is fixed to the AX7101 shape (round 1 of #878) and is not an Arty gate; it is unchanged here.

## 6. Notes and departures

- **Census basis.** Census 1 ran at the 1x1's statements. Its images carried the 48/96/192 kHz AUDIO_UNIT list, since narrowed to 48 kHz (builder gate 36a, and this envelope).
  That narrowing changes the model id (now `0x001BC570F86D0133`) and the ELF (`9ea79cc3...`: `.rodata` -8 B, `.bss` -64 B, `.text` the same size).
  It cannot move rows that miss by 7 to 62 ms. A qualifying row would have needed a census on its own image anyway.
- **Latency pair.** The builder suite now registers the 4x4 configuration's 1409/100 ns pair as the board's measured 1,509 ns sum (#829). It was measured on the 1x1 image; the PHY, MII path and clock are the same.
- **Held-egress rows.** `backlog-owed` measures 61.92 to 64.13 ms at this point. No ledger is stated: #878's held-egress ruling names the (1,1,2) point.
- **Bind groups.** #1009's `save-bind*` groups ran with round 9's scratch-only sentinels, since no Arty bind bound is ruled.
- **Base tree.** For the identity proof the base was a `git clone --shared` of the train repository at `aa53840d9`, in scratch, with its own `.git/config`. The shared `.git/config` was never written (sha256 checked before and after the submodule work).
- **Removals.** Logged before they ran in `disk-cleanup.log`: the first, plain `git archive` base tree, which the image builder refuses without gitlinks, and the firmware gate's untracked `dispatch-build/` in the checkout.
- Scratch: about 7.8 GB of the 12 GB cap, kept for review (the census traces).
