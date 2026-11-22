# [A814] REPORT: gPTP in the split firmware on the #872 optimisation line, round 2 and 2b (#884, #665 F6)

Head `f15b3a7d`: round 2b's four commits on round 2's `17d9d54a`, whose 20 sit on round 1's `424c8cf1`, all on
`dev-soft-core-optimisation` `59b09884`. Local commits only; nothing pushed, no PR, no comment. The rulings applied
are #884 issuecomment-7067495546 (items 1-7, round 2) and issuecomment-7072401468 (items 1-4, round 2b). The gate
table is at the end, and the PR body draft is the last section.

## Round 2b: ruling 1 option (b), the derived gptp burst (issuecomment-7072401468)

All three conditions of option (b) hold, so there is no STOP.

| Condition | 8x8/1if (burst 7) | 8x8/2if (burst 14) |
|---|---|---|
| `backlog-owed.service.acmp.last.if0` at or under 62.62 ms | **62.535 ms**; `egress_ledger.py --point 8x8-1if` **PASS**, all seven held rows within | 62.496 ms (no ledger at this point, see below) |
| Pdelay turnaround at or under 10 ms | **0.186 ms** | **0.266 ms** |
| The flood plant, no delivered stamp lost and lock kept | | **48 of 48 checks PASS**: 490 delivered event messages all stamped, 0 egress records lost, the flooded port locked by 2.9 s and within 95 ns after |

- **The burst is derived, not fitted** (`sw/mailbox/mailbox.yaml`, the gptp channel's `rate`, stated in
  MAILBOX_CONTRACT.md): `burst_per_interface: 7`, times the interfaces (7 at 1if, 14 at 2if). The ruling expected
  about 8 and 16.
  - A full-duplex port receives seven message kinds from its one peer: IEEE 802.1AS-2020 Table 11-5 (Sync,
    Pdelay_Req, Pdelay_Resp, Follow_Up, Pdelay_Resp_Follow_Up) and Table 10-8 (Announce, Signaling). No other
    messageType is used.
  - Each arrives at most once in one 10 ms refill window. Sync and Follow_Up come every 125 ms. Announce, the
    peer's Pdelay_Req, and the Pdelay_Resp pair answering the port's own request come every second (Milan v1.2
    4.2.6.2.2 Table 4.1). A gPTP-capable Signaling comes at its default second (10.7.2.5). Since 90 % of intervals
    fall within 30 % of nominal (10.7.2.2, 10.7.2.3), the closest in-tolerance Sync pair is 87.5 ms apart.
  - Seven, not eight, because nothing the port sends passes the channel's admission: its own Pdelay_Req leaves
    through the transmit ring, and its egress stamp arrives as `TIMESTAMP`.
  - The figure came from the message kinds alone and was fixed (`0bb83b9d`) before the re-measurement (`f828861c`).
- **Where the figure lives:** `mailbox_model.py` scales a burst stated per interface by the contract's interfaces,
  or by a variant's (`_scaled`, `with_interfaces`), and range-checks it. The generated `KL_mbx_pkg.sv` and
  `mbx_contract.h` carry 7, and a two-interface variant carries 14. The RTL's admission reads it (`KL_mbx_rx.sv:747`
  and `:764`: the token bucket's cap and reset value), as does the host mailbox model (`mbx_model.c:55`). No
  firmware source reads it, and the routed build's firmware image is byte-identical to round 2's. The harness
  composes and grades each point at its own interfaces, and a new self-test mutant (the burst held at one
  interface's) is caught.
- **The last gptp record under the composed load** now lands by 6.040 ms at 1if and 7.790 ms at 2if (7.491 and
  7.945 ms at the provisional 16). The composed maxima (1.638 and 1.633 ms) and gPTP's CPU share (0.264 % and
  0.308 %) are unchanged, and no pass exceeds the share (0 of 5,441; 0 of 5,213).
- **`egress_ledger.py` at 8x8/2if, for the record.** The resume note asks for the tool green at both 8x8 points, but
  its ledger exists at 8x8/1if only (#894's ledger ruling; `--point` offers `8x8-1if` alone).
  - Graded against those figures, the 2if run's six same-named rows are all within, its held row at 62.496 ms.
  - The tool still says FAIL. The composed load alternates its AECP records over the interfaces
    (`scenario.py:740`, `n % p.interfaces`, from the base), so at 2if the AECP row's last instance is
    `aecp.last.if1` (62.088 ms, under the 62.16 ms of the `if0` name).
  - The same head without gPTP fails the same way (`receipts/round2b/harness/8x8-nogptp/`: `aecp.last.if1` at
    61.771 ms, no `if0` instance; `acmp.last.if0` at 62.093 ms). So the FAIL comes from applying the 1if ledger at
    2if, not from gPTP or the burst, and no option could make the tool green at 8x8/2if.
  - At 2if gPTP's burst of 14 adds 0.403 ms to the held row's 2.093 ms of service past the 60 ms hold (19 %). At 1if
    the burst of 7 adds 0.045 ms to 2.490 ms (1.8 %). If a 2if ledger were derived by the 1if rule from this one run
    without gPTP (hold plus service plus 5 %, 62.20 ms), the gPTP run's 62.496 ms would be past it.
  - A 2if ledger is the ledger owner's to derive. It is not one of option (b)'s conditions.
- **Found and fixed on the way:** six self-test stand-ins of `check_load` and `defined_load` still had the base's
  signatures. Round 1 added the opened-channel argument, and since then three mutants raised `TypeError` instead of
  planting their defect, which the self-test counted as a catch. Each is now caught by its own named check.
  Separately, the closed loop's two-interface contract copy (`tb/verilator/gptp_sw/Makefile`) had no prerequisites,
  so a kept build dir kept an old burst. It now regenerates on any change to the contract, its generator or the
  driver (`f15b3a7d`). The round 2b flood was built fresh at 14, so no receipt ran the old burst.
- **Re-routed, since the burst reaches the RTL** (the gptp bucket's cap and reset value in `KL_mbx_rx`, 16 to 7), at
  `62fcd154` with the same firmware image (byte-identical to round 2's, sha256 `962eca13...`). AltSpreadLogic_high
  reaches **WNS +0.230 ns, WHS +0.015 ns**, and ExtraPostPlacementOpt +0.205 / +0.013 ns. Both meet #818's floor.
  `f15b3a7d` changes only the closed loop's Makefile.
- **Ruling 2:** the second MAC is #962. This lane keeps one MAC, and the PR body says so.
- **Ruling 3:** the census `GPTP_SW_EN_P` shape is owed to the census owner, with this lane's row list (section 5,
  and the PR body).
- **Open risk:** the count covers the peer's periodic sends at the profile's intervals. An event-driven send (an
  Announce on new information after a role change, or a Signaling that requests an interval) could add one more
  record in a window. A record past the burst is held to the next refill or refused and counted, none is delivered
  without its stamp, and the flood shows the port keeps its lock through such refusals.

## Summary (round 2 and 2b, at the derived burst)

- **Ruling 1, measured at 8x8/2if:** the Pdelay responder's turnaround is **0.266 ms** against the 10 ms bound
  (0.186 ms at 8x8/1if). With every composed row carrying the gptp channel's admitted burst, the composed maximum is
  **1.633 ms** (1.638 ms at 8x8/1if), inside THE SHARE of 2.0 ms, and **no work pass of any group exceeds the
  share** (0 of 5,213; 0 of 5,441). The burst's last record is served by 7.79 ms (6.04 ms at 8x8/1if), inside 10 ms;
  at round 2's provisional burst of 16 it was 7.95 ms.
- **Ruling 2:** every gPTP frame now carries its own ingress stamp, as an eight-octet trailer on its gptp record,
  from a stamp FIFO in step with the split tap's frame FIFO. A frame the mailbox refuses takes its stamp with it,
  so no stamp of a delivered frame can be lost. The planted overrun: 80 frames into the 64-entry FIFO keep 64 with
  their own stamps and refuse 16 (bench), and bursts of 32 Pdelay_Req past the channel's derived burst (14 at two
  interfaces) leave every delivered event message stamped while the port keeps its lock (closed loop).
- **Ruling 4:** the harness's memory refusal is lifted as recorded debt. Three ledger entries: the size fixture's 8x8
  images with gPTP at 59.0 and 64.0 RAMB36, and the platform's 8x8/1if image with gPTP at 62.0. Both 8x8 points are
  measured with gPTP.
- **Ruling 5:** one PHC, one launch observer, one timestamp unit and one control tap per MAC, proven at two
  interfaces in the closed loop with two peers on their own clocks: each port locks its own PHC (2.7 s and 2.5 s to
  within 100 ns), and the two PHCs stand apart as their grandmasters do. The product split SoC has one MAC, so the
  product build still has one of each; the second MAC is #962 (ruling 2 of round 2b).
- **Ruling 6:** the plane stays buildable; nothing of it was deleted.
- **Ruling 7:** the status block is narrowed to `GPTP_GM_LO`, `GPTP_GM_HI`, `GPTP_STATE`, with REGISTER_MAP
  regenerated in the same change. The firmware answers GET_AVB_INFO's gPTP fields and GET_AS_PATH from the snapshot it
  published, and the closed loop checks the answers equal the decoded words. **The saving, from synthesis (S3 against
  round 1's S2, same recipe): −3,049 FF**, the publication path's own cells −2,125 LUT; whole-design LUT is flat
  (−33) because untouched modules move by ±1.3k between syntheses.
- **R2-5:** the adapter has no poll: each callback publishes the port it ran. gPTP's share of the CPU after link-up
  fell from round 1's 1.14 % (1x1) to **0.31 %** at 8x8/2if; the adapter's own cycles fell 11-fold.
- **The routed `--sw-gptp` build at 8x8/1if** (with the gPTP platform image, 62.0 RAMB36) meets #818's floor
  (+0.030 ns / 0 ns at every corner). Re-routed at the derived burst (`62fcd154`), AltSpreadLogic_high reaches
  **WNS +0.230 ns, WHS +0.015 ns** and ExtraPostPlacementOpt +0.205 ns / +0.013 ns. At round 2's head all three
  directives met the floor (AltSpreadLogic_high +0.237 ns, ExtraTimingOpt +0.152 ns, ExtraPostPlacementOpt
  +0.098 ns). Against the plane at round 2's head and the same directive (+0.139 ns): **−4,796 LUT, −5,470 FF,
  −6 DSP**, equal block RAM (95.5 tiles: the gPTP image's 3.5 more tiles offset the plane's RAMs).
- **Gates (round 2b):** the full Verilator sweep (67 of 67 suites) and the 73 docs, idiom and rtl-fast gates at the head `f15b3a7d`, with the
  closed-loop campaign (14 of 14), `milan_dp` `split-sw`, and the memory ledgers. Yosys portability (64 tops), the
  firmware gate's four shards (the control campaign 826 of 826 caught), the publication census with its self-test
  and the harness self-test (298 of 298 mutants) ran at `62fcd154`. All PASS. In round 2, three plants and the
  sweep's duration table needed fixing (section 5).
- **For a decision: none.** Round 2's two (the held-egress row, the second MAC) are resolved by
  issuecomment-7072401468; for the record, the 2if egress ledger and the burst's open risk (round 2b above).

## 1. What changed, and why

### The ingress trailer (ruling 2)

`KL_ctrl_split` (`GPTP_P`) appends each gPTP frame's ingress stamp after its last byte, most significant octet first,
or all ones for a frame that is no event message. The stamp is taken from `KL_gptp_tsu` at the frame's last beat into
a 64-entry stamp FIFO that moves in step with the frame FIFO, and is emitted with the frame. A gPTP frame that finds
the stamp FIFO full is refused at its second beat and counted in the tap's drops. The timestamp unit's own FIFO now
holds egress records only (32, more than the 15 frames the gptp transmit ring holds), and TIMESTAMP carries egress
stamps only. The adapter reads the trailer, hands an event message's stamp to its port, and passes the frame without
it.

### The narrowed publication and the snapshot (ruling 7)

Under `--sw-gptp` the datapath's consumers need only the grandmaster (clock validity, GM counters), asCapable and the
verdict (clock validity) and `DISC`. So contract 2.5 publishes three words an interface; the parent, the peer delay
and the path trace stay in firmware. Their CSR reads (`GPTP_PDELAY`, `AS2_LO/HI`, `ASP_CMD`) read 0 under
`--sw-gptp`, documented in REGISTER_MAP. The firmware keeps the state it published as the snapshot of that `GEN`,
answers GET_AVB_INFO's gPTP fields and GET_AS_PATH from it (`aecp_face_gptp`), and raises AVB_INFO and AS_PATH
changes itself; the datapath's change detectors are off under `GPTP_SW_EN_P`.

### One PHC and one timestamp unit per MAC (ruling 5)

The closed loop (`tb/verilator/gptp_sw`) now builds, per interface, a PHC, the launch observer, the timestamp unit and
the split's control tap, and runs both firmware ports against two independent peers.

### The adapter without a poll (R2-5)

The adapter binds the gptp channel, an event sink and a centisecond; each publishes the port it ran, in the pass that
ran it. The platform's poll table was full (eight of eight), which this also resolves.

### gPTP in the platform image

A `--sw-gptp` build needs an image with gPTP. `ctrl_plat_image.py --with-gptp` builds `plat/ctrl_plat.c` with
`CTRL_PLAT_GPTP`: one port an interface, each the EUI-64 of its interface's MAC, bound after the saved-state store's
centisecond and before the mailbox opens. Its PHC is the CSR's PTP block: `PTP_ADJ`'s addend for the rate, a
`PTP_OFFSET` delta at `PTP_CMD`'s adjtime strobe for a step, and the PHC's rate read from `PTP_INCR` by shifts and
subtractions (the split ISA has no divide). Without the flag the image is byte for byte the one before.

### Contract 2.5's cost to every image

The gptp channel's table entries and the face's answer port add 64 B to the platform's `ctrl_plat` at every point
but 8x8/2if, and 200 B of rom at 8x8/1if. That image is 139,408 B, 144 B past what 58.0 holds, so its entry is
re-measured at 58.5 (at `59b09884` it is 139,208 B and 18,944 B). `plat_ledger.py` links all five points PASS with
its nine controls.

## 2. Measurements

### The service budget (the harness, split CPU at 100 MHz, `receipts/round2b/harness/`)

| Point | gptp burst | Turnaround (bound 10 ms) | Composed maximum (THE SHARE 2.0 ms) | Passes over the share | Last gptp record under the composed load | Held row `acmp.last.if0` (ledger 62.62 ms) | gPTP CPU after link-up | Steady, slave / master |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 8x8/2if | 14 | 0.266 ms | 1.633 ms | 0 of 5,213 | 7.790 ms | 62.496 ms | 0.308 % | 0.343 % / 0.315 % |
| 8x8/1if | 7 | 0.186 ms | 1.638 ms | 0 of 5,441 | 6.040 ms | 62.535 ms | 0.264 % | 0.291 % / 0.256 % |
| 8x8/2if, round 2 | 16 | 0.266 ms | 1.633 ms | 0 of 5,214 | 7.945 ms | | 0.308 % | |
| 8x8/1if, round 2 | 16 | 0.186 ms | 1.638 ms | 0 of 5,441 | 7.491 ms | 62.640 ms | 0.264 % | |
| 1x1/1if (round 1) | | 0.193 ms | — | — | — | | 1.14 % | 0.207 % / 0.183 % |

Each composed window of a gPTP image carries the channel's admitted burst at its point's interfaces as a peer's
Pdelay_Req: the dearest gptp record, which the port answers with a Pdelay_Resp and its Follow_Up. Every window
released its whole load. The dearest pass with gPTP work is 33,428 cycles (0.33 ms), at link-up. Round 2's figures
(`receipts/harness/`) are kept for the comparison.

### Memory (`receipts/memory/`)

| Image | Without gPTP | With gPTP | Ledger entry |
|---|---:|---:|---|
| The size fixture's 8x8/1if (the harness's `8x8-1if`) | 56.0 | 59.0 | `8x8-one-interface-gptp` |
| The size fixture's 8x8/2if (the harness's `8x8`) | 60.5 | 64.0 | `8x8-two-interfaces-gptp` |
| The platform's 8x8/1if (the `--sw-gptp` build's) | 58.5 | 62.0 | `platform-8x8-one-interface-gptp` |

A port adds about 12.5 KB of rom and 1.1 KB of sram.

### Synthesis: what narrowing saved (`receipts/syn/`)

S3 is the `--sw-gptp` design at this head, synthesis only, with round 1's recipe (the gate's argv, flow flags and
`--eth-port e2`) and this line's 8x8/1if image without gPTP, the closest to S2's firmware memory.

| Build | LUT | FF | BRAM tiles | DSP |
|---|---:|---:|---:|---:|
| S0, the plane (round 1) | 44,942 | 51,086 | 94.5 | 11 |
| S2, `--sw-gptp`, 22-word publication (round 1) | 40,349 | 48,952 | 92.0 | 5 |
| **S3, `--sw-gptp`, narrowed, with the trailer** | **40,316** | **45,903** | **92.0** | **5** |

| Cell, S3 against S2 | LUT | FF | LUTRAM |
|---|---:|---:|---:|
| `KL_mbx` own (the publication registers) | −653 | −609 | |
| `KL_mbx_cdc/u_gptp_pub` (the publication's crossing) | −756 | −1,232 | |
| `milan_datapath` own (the decode) | −716 | −1,198 | |
| `ctrl_split` (the trailer and stamp FIFO) | +146 | +85 | +86 |
| `u_gptp_tsu` (egress-only FIFO) | −111 | −87 | |
| whole design | −33 | −3,049 | +86 |

### Routed, 8x8/1if (`receipts/route/`)

The train's recipe (`rprep.sh`, `rbuild.sh`: the builder's split argv, `--eth-port e2`, AreaOptimized_high,
ExploreArea), Vivado 2026.1, one route at a time through `vivado-slot.sh`. The `--sw-gptp` SoC carries the
platform's gPTP image (62.0 RAMB36); the plane SoC carries this line's image without gPTP (58.5). Round 2's clones
at `40bd7738`; the commits after it change no RTL or SoC source, and of the firmware only two comments.

| Build, placement directive | LUT | FF | Slices | BRAM tiles | DSP | WNS (every corner) | WHS (every corner) | #818's floor (+0.030 / 0) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `--sw-gptp`, ExtraPostPlacementOpt | 38,370 | 45,814 | 15,197 (95.9 %) | 95.5 | 5 | +0.098 ns | +0.028 ns | met |
| `--sw-gptp`, ExtraTimingOpt | 38,225 | 45,814 | 14,940 (94.3 %) | 95.5 | 5 | +0.152 ns | +0.023 ns | met |
| **`--sw-gptp`, AltSpreadLogic_high (best)** | **38,227** | **45,814** | **14,943 (94.3 %)** | **95.5** | **5** | **+0.237 ns** | **+0.023 ns** | **met** |
| the plane, ExtraPostPlacementOpt (its image at 58.5) | 43,166 | 51,284 | 15,355 (96.9 %) | 95.5 | 11 | +0.139 ns | +0.036 ns | met |
| **`--sw-gptp` − plane, same directive** | **−4,796** | **−5,470** | **−158** | **0** | **−6** | −0.041 ns | −0.008 ns | |
| round 2b, `--sw-gptp`, ExtraPostPlacementOpt, at `62fcd154` | 38,178 | 45,815 | 15,215 (96.0 %) | 95.5 | 5 | +0.205 ns | +0.013 ns | met |
| **round 2b, `--sw-gptp`, AltSpreadLogic_high, at `62fcd154`** | **38,265** | **45,815** | **14,680 (92.6 %)** | **95.5** | **5** | **+0.230 ns** | **+0.015 ns** | **met** |

Round 2b re-routed the best directive and the plane comparison's directive at `62fcd154` (`receipts/round2b/route/`): the contract's burst reaches
`KL_mbx_rx`, so the netlist moved (+1 FF). The firmware image and the argv are round 2's. The plane was not
re-routed, so its row and the difference row are round 2's, at the burst of 16. `KL_mbx_rx` builds every channel's
bucket in both builds, and the plane's firmware never opens the gptp channel, so the plane's netlist could move by a
few cells too.

The worst setup paths are the mailbox's (the map edit's crossing, `KL_mbx_dma`, the register read), not gPTP's.

## 3. Verification

| Bench or gate | What it proves | Planted defects |
|---|---|---|
| `tb/verilator/gptp_tsu` | both stamp points, the guard, the egress FIFO at 32; the trailer read where the mailbox reads it (I1-I5); the 80-frame flood (T2) and frame-FIFO drops (T3) | 24 of 24 killed |
| `tb/verilator/gptp_sw` (48 checks) | two interfaces, two peers: lock, step once, no bridge; the snapshot, its answers and notices; the cut request refused; the silent grandmaster's replacement published; the pass invariant; the flood | 14 of 14 killed |
| `tb/verilator/milan_dp` `split-sw` | the narrowed words decoded onto the consumers' nets, the detectors off | the bench's own |
| `sw/litex/test_ctrl_memory.py` | the six ledger entries, their cases and sixteen planted ledgers | PASS |
| `tb/verilator/ctrl_split_boot/plat_ledger.py --self-test` | the platform image at five points against the ledger | 9 of 9 controls |
| the harness self-test (`run.py --self-test`) | 1,017 checks, among them a gPTP image's ledgered points and its composed loads at one and two interfaces | 298 of 298 mutants caught (round 2b adds the burst held at one interface's) |

## 4. Decisions (round 2's, resolved by issuecomment-7072401468)

Both are resolved: item 1 by option (b), measured in round 2b above (the row at 62.535 ms, `egress_ledger.py` PASS at
8x8/1if), and item 2 by #962. Round 2's text, for the record:

1. **The held-egress ledger with gPTP in firmware.** At 8x8/1if, `backlog-owed.service.acmp.last.if0` measures
   62.640 ms against its egress-ledger figure 62.62 ms (+0.020 ms). Its service past the 60 ms hold is 2.640 ms with
   gPTP against 2.490 ms without: the gptp burst's 16 Pdelay_Req records add 0.150 ms (6.0 %), past the ledger's
   5 %. The other six held rows are within their figures. Options: (a) derive the row's figure for a gPTP image by
   the ledger's own rule (hold plus the measured service plus 5 %: 62.78 ms); (b) a smaller gptp admission burst
   (ruling 2 keeps admission provisional); (c) gptp records served as tier 2. Recommendation: (a), since the row is
   already ledgered past its budget by design and the burst is the worst case admission allows.
2. **The product SoC's second MAC.** Ruling 5 requires one PHC and one timestamp unit per MAC. The replication is
   built and proven in the closed loop; the split SoC has one MAC, so its build has one. A second MAC in the product
   is NFR-SCOUT-05's redundancy work (32x32). Recommendation: a new Issue for it, this line keeping one MAC.

## 5. Not done in this PR

- **The census `GPTP_SW_EN_P` shape (R2-4; round 2b's ruling 3).** It is owed before this line merges onward, not
  in this PR. The census owner rules the rows the sw build ties off, and this lane's round 3 applies the shape. The
  census elaborates the split with the plane (`GPTP_SW_EN_P = 0`) only. The rows the sw shape changes, for the census
  owner:
  - E rows `o_ctl_avb_chg_p` and `o_ctl_asp_chg_p`: constant 0 under `GPTP_SW_EN_P` (`milan_datapath.sv:10332`), since
    the firmware raises AVB_INFO and AS_PATH changes itself.
  - M rows `i_ctl_gptp_pub` (three words an interface), `i_ctl_gptp_pub_p` and `i_ctl_ts_take`: the
    `GPTP_SW_ONLY` set (`census_split.py:243`), read only under the sw build, where a plane-shape read is refused.
    `GPTP_STATE` bits 11 to 15 are reserved and unread, and its `GEN` is consumed in `KL_mbx_cdc`.
  - `o_ctl_ts_valid` and `o_ctl_ts_data`: tied 0 under the plane (`milan_datapath.sv:9329`), driven by the timestamp
    unit under the sw build.
  - The plane's `gptp_pub_*` parent, peer-delay and path nets: tied 0 under the sw build (`milan_datapath.sv:9405`
    to `9413`); their CSR words read 0 (REGISTER_MAP).
  - `KL_ctrl_split` with `GPTP_P`: adds the stamp FIFO and the ingress trailer on the gptp channel's records.

  The functional proof of those nets today is `milan_dp`'s `split-sw` and the closed loop.
- **64x64/2if on [A813]'s hart split** (R2-5's second half): [A813]'s memory plan does not place a gPTP image yet.
- **`milan_dp`'s `split-sw` leg is not in the suite's default cases**, so the sweep does not run it (this round ran
  it by hand: 151 checks PASS). Adding a case re-deals the hosted legs' windows (`suite_shards.PIECE_SECONDS`, #804),
  a CI scheduling change left to its owner. Recommendation: add it as an ordinary case with the next measured hosted
  run.
- **Bench qualification** (ruling 3): no bench this round.

Fixed on the way, found by this round's gates: round 1's `gptp_sw` and `gptp_tsu` suites had no duration in
`suite_shards.SUITE_SECONDS`, so the sharded sweep (and the hosted shards) refused to schedule; they are now
registered, provisional at 860 s and 120 s, and pinned in the test-evidence runner contract. Three campaign plants no
longer applied after rounds 1 and 2's edits (the platform campaign's saved-state plant, the census's
unraised-notification plant, and the driver campaign's face-count plant, whose `else` stopped compiling once round
1's TIMESTAMP branch followed it); each now plants the same defect at the moved text.

## 6. For [A813] (contract 2.6)

TIMESTAMP names no hart; the gptp channel's rings, the centisecond, the publication window and the PTP block
(`PTP_ADJ`, `PTP_OFFSET`, `PTP_CMD`, `PTP_INCR`) are what gPTP's hart needs. gPTP's load is 0.31 % of a hart.
Both lanes touch `ctrl_plat_image.py`'s argument list and required-symbol check, the ledger dict in `ctrl_memory.py`,
`milan_soc.py`, `mbx_model.c` and the contract; see the merge surface.

## Merge surface

Read-only comparison with the parallel lanes' branches as they stand (each against its own base).

- **[A813] opt-hart2 (contract 2.6 on top of 2.5):**
  - the contract: `sw/mailbox/mailbox.yaml`, `mailbox_model.py`, `mailbox_skeleton.py`, the generated
    `KL_mbx_pkg.sv`, `KL_mbx.sv`, `mbx_contract.h`, `MAILBOX_CONTRACT.md`. 2.5 integrates first; 2.6 regenerates.
  - `sw/firmware/ctrl/test/ctrl_plat_image.py`: both lanes add an argument (`--with-gptp` here, `--harts` there),
    sources in `compile_all`, and edit the required-symbol check in `main` (`required = REQUIRED | GPTP_REQUIRED`
    here). These hunks will conflict textually; the union is both.
  - `sw/litex/ctrl_memory.py`: this lane edits `LEDGERED` (three entries added, `platform-8x8-one-interface`
    re-measured); [A813] adds region and plan code elsewhere in the file. A two-hart image's own ledger entry, if it
    adds one, goes in the same dict.
  - `sw/litex/milan_soc.py` (one line here, `_split`'s local import), `sw/firmware/ctrl/host/mbx_model.c`
    (TIMESTAMP depth, the GPTP snapshot; [A813] edits `read_identity`), `sw/litex/test_ctrl_memory.py`,
    `docs/reference/FR_NFR.md`, `docs/DOCUMENTATION_AUDIT.md` (regenerate after the merge).
  - Contract 2.6 must route TIMESTAMP and LINK, the gptp channel, the centisecond, the publication window and the
    PTP block to gPTP's hart; nothing in 2.5 assumes hart 0.
- **[A808] opt-exec:** the harness. `scenario.py` (theirs +85 lines at 673; mine `Point` at 201-211,
  `composed_load` at 728-745 and two comments; textually disjoint, but the merged file is over the 1000-line module
  limit, theirs already being 1,084), `run.py` (disjoint hunks), `README.md` (disjoint), the documentation audit.
- **[A812] opt-donors:** no shared file.

## Gate table

Final head `f15b3a7d`. Each gate names the head it ran at; the commits after that head touch nothing in its scope
(listed under the table). Round 2b's receipts are under `receipts/round2b/`.

| Gate | Head | Result | Receipt |
|---|---|---|---|
| Full Verilator sweep, 4 parallel shards (`native-shards.py`, the CI-pinned Verilator 5.050) | `f15b3a7d` | 67 of 67 suites PASS, 0 in-suite failures; `tsn_fuzz`'s tsn-gen campaigns, skipped there without `TSN_GEN_ROOT`, are round 2's at `9dacf75b` (nothing they build changed since) | `round2b/sweep/` |
| Docs, idiom and light rtl-fast gates (73, as round 2's) | `f15b3a7d` | 73 of 73 PASS | `round2b/gates/` |
| Closed-loop campaign, `gptp_sw_mutants.py` | `f15b3a7d`; `f828861c` | 14 of 14 killed at each | `round2b/closedloop/` |
| `gptp_sw` suite (`make`: slave, master, flood; 48 checks) at the derived burst | `f828861c`; in the sweep at `f15b3a7d` | 48 of 48 PASS (the flood: 490 stamped, 0 unstamped, 0 egress lost, lock 2.9 s) | `round2b/closedloop/` |
| `milan_dp` `split-sw` and `split-cdc` (built against the new package) | `f15b3a7d` | 151 and 13 checks PASS | `round2b/milan_dp/` |
| `plat_ledger.py --self-test`, `test_ctrl_memory.py` | `f15b3a7d` | 5 points PASS, each identical to round 2's, 9 of 9 controls; PASS | `round2b/memory/` |
| Harness legs, 8x8 and 8x8-1if `--with-gptp` | `f828861c` | rc 0, 0 refusals; round 2b section | `round2b/harness/` |
| `egress_ledger.py --point 8x8-1if` on the 8x8-1if gPTP run | `f828861c` | **PASS**, all seven held rows within | `round2b/harness/` |
| `egress_ledger.py --point 8x8-1if` on 8x8 (2if) runs, with and without gPTP | `f828861c`; `62fcd154` | FAIL in both, the same way (no 2if ledger; round 2b section) | `round2b/harness/` |
| Harness self-test, `run.py --self-test` | `62fcd154` | 1,017 checks PASS; 298 of 298 mutants caught | `round2b/harness/selftest/` |
| Firmware gate, four shards, a clone each | `62fcd154` | 4 of 4 PASS; the control campaign 826 of 826 caught | `round2b/fwgate/` |
| Yosys portability, 4 shards (64 tops; tied-input and tap-purity gates) | `62fcd154` | PASS | `round2b/yosys/` |
| Publication census, `--check --selftest --jobs 4` | `62fcd154` | 246 checks PASS; 164 self-test arms, 57 of 57 rules proved | `round2b/census/` |
| Routes, 8x8/1if `--sw-gptp`, AltSpreadLogic_high and ExtraPostPlacementOpt | `62fcd154` | both meet #818's floor (+0.230 / +0.015 ns; +0.205 / +0.013 ns) | `round2b/route/` |

What moved after each round 2b gate's head: `62fcd154` the design page only (GPTP_SOFTWARE.md); `f15b3a7d` the
closed loop's Makefile only, which no gate but the closed-loop suite and its campaign reads (both re-run at it). Not
re-run in round 2b, and out of the change's scope: `gptp_tsu` and `tsu_mutants.py` (the bench builds no mailbox; the
suite runs in the sweep), and S3 synthesis (superseded by the re-routes).

### Round 2's gate table (head `17d9d54a`)

| Gate | Head | Result | Receipt |
|---|---|---|---|
| Full Verilator sweep, 4 parallel shards (`native-shards.py`, the CI-pinned Verilator 5.050) | `ee0d920c` | 67 of 67 suites PASS, 0 in-suite failures; `tsn_fuzz`'s tsn-gen campaigns, skipped there without `TSN_GEN_ROOT`, run at `9dacf75b`: 164 and 675 PASS | `receipts/sweep/` |
| Yosys portability, 4 shards (64 tops; tied-input and tap-purity gates) | `14a54bbc` | PASS | `receipts/yosys/` |
| Firmware gate, four shards (`test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`), a clone each | `99a329de`; shard 1 (the control campaign) `c3c03fd9` | 4 of 4 PASS; the control campaign 826 of 826 caught | `receipts/fwgate/` |
| Publication census, `--check --selftest --jobs 4` | `fb53183f` | 246 checks PASS; 57 of 57 rules proved | `receipts/census/` |
| Docs, idiom and light rtl-fast gates (73: docs_check, em-dash, doc style, gPTP docs, TOC, docs inventory, register reference, idiom x4 with self-tests, naming, port contracts, RTL and SoC source lists, test evidence, lint, xvlog, gen_mailbox, module matrix, ...) | `17d9d54a` | 73 of 73 PASS | `receipts/gates/` |
| `gptp_sw` suite (`make`: slave, master, flood; 48 checks) | `14a54bbc` | PASS | `receipts/closedloop/` |
| Closed-loop campaign, `gptp_sw_mutants.py` | `14a54bbc` | 14 of 14 killed | `receipts/closedloop/` |
| `gptp_tsu` suite and `tsu_mutants.py` | `14a54bbc` | PASS; 24 of 24 killed | `receipts/tsu/` |
| `milan_dp` `split-sw` and `split-cdc` | `14a54bbc` | 151 and 13 checks PASS | `receipts/milan_dp/` |
| `test_ctrl_memory.py` | `14a54bbc` | PASS | `receipts/memory/` |
| `plat_ledger.py --self-test` | `14a54bbc` | 5 points PASS, 9 of 9 controls | `receipts/memory/` |
| Harness self-test, `run.py --self-test` | `c9f6b873` | 1,017 checks PASS; 297 of 297 mutants caught | `receipts/harness/selftest/` |
| Harness legs, 8x8 and 8x8-1if `--with-gptp` | `0e476c94` | rc 0, 0 refusals; measurements in section 2 | `receipts/harness/` |
| `egress_ledger.py --point 8x8-1if` on the gPTP run | `0e476c94` | FAIL by 0.020 ms on one row (decision 1) | `receipts/harness/` |
| Routes, 8x8/1if `--sw-gptp` x3 directives and the plane | `40bd7738` | all four meet #818's floor | `receipts/route/` |
| S3 synthesis | `0e476c94` | section 2 | `receipts/syn/` |

What moved after each gate's head: `9f97ee71`, `0e476c94`, `5010b5dc`, `14a54bbc`, `6adf9dd5` docs and comments;
`175f114e` the gates' own fixes (the split-sw build flags, the campaign helper, two test modules' length, a linked
doc); `c9f6b873` and `34dbab53` the test-evidence scripts; `99a329de` the platform campaign's plant; `ee0d920c` the
sweep's duration table and timeouts; `fb53183f` the census's plant; `c3c03fd9` and `9dacf75b` the driver campaign's
face-count plant and its module's docstring; `17d9d54a` four comments (two in the adapter, one in the closed
loop, one doc line) citing #884 for a plan item. After `40bd7738` no commit changes RTL, the SoC, or firmware
source beyond those two comments; after `0e476c94` none changes the harness's run inputs (its self-test modules moved in
`175f114e`, and the self-test ran after it, at `c9f6b873`).

## PR body draft (for a PR into dev-soft-core-optimisation)

```markdown
## gPTP in the split firmware on the optimisation line (#884, #665 F6)

Refs #884, #665, #872, #962. Implements the owner's decision of 2026-11-21 (#872) with the rulings of #884
issuecomment-7067495546 and issuecomment-7072401468 applied. Does not close #884: the bench qualification (ruling
item 3 of the first) is owed.

### What it does

- **Firmware owns gPTP** under `milan_soc.py --sw-gptp` (`GPTP_SW_EN_P`): one IEEE 802.1AS-2020 end station port
  an interface (`sw/firmware/ctrl/gptp/gptp.c`), fixed-point, no heap, behind a four-call HAL; the mailbox adapter
  (`gptp_mbx.c`) publishes each port from the callback that ran it, with no poll.
- **The fabric keeps the timestamps and the PHC**: `KL_gptp_tsu` keeps the plane's stamp points and corrections; the
  ingress stamp rides with its frame as an eight-octet trailer from a stamp FIFO in step with the split tap's frame
  FIFO (`KL_ctrl_split`, `GPTP_P`), so no stamp of a delivered frame is lost.
- **Mailbox contract 2.5, additive:** channel `gptp` (5), event `TIMESTAMP` (9, egress, not coalesced, credit-flowed,
  naming no hart), and a three-word gPTP publication an interface (`GPTP_GM_LO`, `GPTP_GM_HI`, `GPTP_STATE`).
- **The gptp channel's admission burst is derived, seven an interface** (`sw/mailbox/mailbox.yaml`, stated in
  MAILBOX_CONTRACT.md): the worst legitimate coincidence of the 802.1AS message kinds in one 10 ms refill window.
  A full-duplex port receives seven kinds from its one peer (IEEE 802.1AS-2020 Tables 11-5 and 10-8), each at most
  once in 10 ms at Milan v1.2 Table 4.1's intervals and 802.1AS's 30 % tolerance (10.7.2.2, 10.7.2.3, 10.7.2.5).
  The model scales it by the interfaces: 7 at one, 14 at two.
- **The status block is narrowed** under `--sw-gptp`: parent, peer delay and path trace stay in firmware, which
  answers GET_AVB_INFO's gPTP fields and GET_AS_PATH from the snapshot it published and raises their changes;
  REGISTER_MAP regenerated.
- **The platform image composes gPTP** (`ctrl_plat_image.py --with-gptp`, `CTRL_PLAT_GPTP`) on the CSR's PTP block.
- **Memory debt ledgered**: the 8x8 gPTP images at 59.0, 64.0 and 62.0 RAMB36; the platform's 8x8/1if entry
  re-measured at 58.5 under contract 2.5.
- **The fabric plane stays buildable**; nothing of it is deleted.
- **One MAC.** The product split SoC has one MAC, so its build has one PHC, one launch observer, one timestamp unit
  and one control tap. The replication per MAC is built and proven at two interfaces in the closed loop. The second
  MAC is #962.

### Evidence

- Closed loop (`tb/verilator/gptp_sw`), two interfaces and two peers: each port locks its own PHC within 100 ns in
  about 2.5 s and holds it; as grandmaster each peer locks to it; bursts of 32 Pdelay_Req past the derived burst
  leave all 490 delivered event messages stamped, with no egress record lost and the lock kept. 48 checks; 14
  planted defects all killed.
- Timestamp unit bench (`tb/verilator/gptp_tsu`): both stamp points, the trailer read where the mailbox reads it, an
  80-frame flood; 24 planted defects all killed.
- Service budget at the derived burst: Pdelay turnaround 0.266 ms at 8x8/2if and 0.186 ms at 8x8/1if, against
  10 ms; composed maximum 1.633 ms inside THE SHARE (2.0 ms); no pass over the share; the burst's last record by
  7.79 ms. gPTP takes 0.31 % of the CPU.
- Held egress: `egress_ledger.py --point 8x8-1if` PASS, every held row within its ledger figure, among them
  `backlog-owed.service.acmp.last.if0` at 62.535 ms against 62.62 ms. The ledger exists at 8x8/1if only. At 8x8/2if the held row is 62.496 ms; the tool cannot pass there on the
  1if figures, with gPTP or without it (the AECP row's last instance falls on interface 1), so a 2if ledger is
  the ledger owner's to derive.
- Synthesis: the narrowing saves 3,049 FF.
- Routed `--sw-gptp` 8x8/1if with the gPTP image, at the derived burst: AltSpreadLogic_high at WNS +0.230 ns,
  WHS +0.015 ns, and ExtraPostPlacementOpt at +0.205 / +0.013 ns, both meeting #818's floor. Against the plane at
  the same directive (round 2's head): −4.8k LUT, −5.5k FF, −6 DSP.
- Local gates: the full Verilator sweep (67 of 67 suites) and 73 docs, idiom and rtl-fast gates at the head; Yosys
  portability (64 tops), the firmware gate's four shards, the publication census with its self-test and the
  harness self-test at its parent, the head adding only the closed loop's Makefile. All PASS.

### Owed, not in this PR

- **The census `GPTP_SW_EN_P` shape**, before this line merges onward. The census owner rules the rows the sw build
  ties off, and this lane's round 3 applies the shape. The rows:
  - E rows `o_ctl_avb_chg_p`, `o_ctl_asp_chg_p`: constant 0 under `GPTP_SW_EN_P`, since the firmware raises those
    changes;
  - M rows `i_ctl_gptp_pub` (three words an interface; `GPTP_STATE` bits 11 to 15 reserved and unread, its `GEN`
    consumed in `KL_mbx_cdc`), `i_ctl_gptp_pub_p`, `i_ctl_ts_take`: read only under the sw build
    (`census_split.GPTP_SW_ONLY`);
  - `o_ctl_ts_valid`, `o_ctl_ts_data`: tied 0 under the plane, driven by the timestamp unit under the sw build;
  - the plane's `gptp_pub_*` parent, peer-delay and path nets: tied 0 under the sw build;
  - `KL_ctrl_split` with `GPTP_P`: the stamp FIFO and the ingress trailer.
- **The bench qualification** of #884.
- **The second MAC**: #962.
```

REVIEW READY f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9
