# Behave test plan — validate every aspect of the Milan end-station

Status: 2026-07-23 (planning round). Executes **roadmap item 10** (peer-review the
204-row traceability matrix 1:1, then author a behave per confirmed row). Companion
docs: `docs/SPEC_TRACEABILITY.md` (the 204-row matrix this suite mirrors),
`docs/testing/PROTOCOL_VALIDATION_MATRIX.md`, `docs/reference/REGISTER_MAP.md`
(CSR ABI, base `0x90000000`), `docs/findings/BENCH_TOPOLOGY.md` (rig + tap tools).

## 0. Principle — the suite IS the matrix

The behave suite is a **live mirror of `SPEC_TRACEABILITY.md`**, not a parallel pile.
Every `Scenario` carries `@clause/@matrix/@roadmap` tags, so running the suite *reports
compliance* and the matrix's 🟡/❌ rows literally generate the backlog. A matrix row
may be marked ✅ only once a passing (non-`@wip`) behave scenario cites it. Prefer
real-wiring-path assertions (USER standing rule); fall back to CSR readback only where
the behavior is wire-invisible.

## 1. Current state (reconnaissance 2026-07-23)

Four real behave suites exist; **no `behave.ini`, no tag taxonomy, no CI** ties them
together, and the two CERT copies are drifting.

| Suite | Path | Feat/Scen | Class | Role in the new plan |
|-------|------|-----------|-------|----------------------|
| **A CERT** | `the-private-test-repo/tests/cert-recreate/features/` | 26 / 63 | real-wire (AVDECC + tap) | the T2 AVDECC/AEM backbone; retag + keep |
| **B AETS** | `the-private-test-repo/private/recreate/aets_recreate_20260721/` | 25 / ~58 | real-wire (snapshot, bundles `aem/`) | **converge into A** (drift source) |
| **C PipeWire E2E** | `the-private-test-repo/tests/features/` | 7 / ~24 | real-wire HIL (audio/THD+N/clock) | the T2 media/stream backbone; retag + extend |
| **D milan-fpga AECP** | `milan-fpga/tests/` | 8 / 55 | host-sim (+ tsn_gen frame codec) | the T0 RTL-contract tier; already has `@tsn_gen @T2 @wip` |

**Coverage holes visible immediately** (domains with weak/no behave today): **MAAP**,
**CBS/shaper + classifier/TCAM/VLAN**, **DMA/perf/throughput**, **saved-state /
fast-connect**, **AX42 TX-wedge recovery**, **PCM-ring integrity under CPU read**,
**RMON good/bad vs tap ground-truth**, and the media-map **es-4.16** (absent between
es-4.15 and es-4.17). Suite D has no live-DUT wiring (Verilator socket "pending").

## 2. Architecture (decisions locked with USER)

1. **Organize by subsystem**, clause-tagged (one `.feature` per subsystem; tags let you
   still slice by clause / matrix-row / roadmap for a compliance report).
2. **Three tiers**, keep **T0/T1 CI-green**, gate **T2** behind `@bench`:
   - **T0 host/sim** — no board: packet builders, tsn_gen frame codec, Python RTL-mirror
     models, AEM-JSON schema, Verilator-TB outputs. Runs in CI / the `Containerfile.bdd-runner`.
   - **T1 board-CSR** — one board via `ssh-pw0` + `devmem` on base `0x90000000`; asserts on
     CSR readback. Headless-capable.
   - **T2 real-wire** — both boards + ProfiShark taps + pw0 raw sockets; asserts on captured
     frames / decoded audio / iperf. The gold tier; `@bench`-gated.
3. **P0 first** = the 7 matrix-❌ rows + this session's roadmap validations (they double as
   acceptance gates for work already proven or in flight).

## 3. Tag taxonomy (author into a shared `behave.ini` + `environment.py`)

```
@subsystem:{gptp,srp,maap,avdecc,aaf_talker,aaf_listener,crf,alsa,link,qos,dma,saved_state,rmon,robustness}
@clause:{1722.1-7.4.15, 802.1as-8.4.3, milan-5.5.1.4, ...}   # normative anchor
@matrix:{R-id or family row, e.g. M-ACMP-9, AVTP-3}          # SPEC_TRACEABILITY row
@roadmap:{1..12}                                             # USER 12-item roadmap
@tier:{t0,t1,t2}                                             # + @bench on every t2
@negative        # asserts a correct rejection / no-crash on bad input
@wip             # not-yet-implemented; spec-anchored TODO, excluded from green gate
@rtl-defect      # asserts CURRENT non-compliant behavior on a pinned RTL gap (flip when fixed)
@regression:{name}  # pins a hard-won past bug (mf52-shed, vid2-clobber, mac-tx-wedge, ...)
@tsn_gen         # frames really generated/decoded by the tsn-gen packet_gen codec
@soak            # long-running (hour rails soak, 1000× flap)
```
Green gate = `behave --tags=-wip --tags=-bench --tags=-soak` (T0+T1, CI).
Bench gate = add `--tags=bench`. Compliance report = `--tags=@matrix:<row>` per row.

## 4. The 14-domain coverage map

Legend: **E**=exists today · **G**=gap (matrix row) · **→**=planned feature · tool =
the "Then" assertion mechanism (see BENCH_TOPOLOGY / REGISTER_MAP for each).

| # | Subsystem | Exists (E) | Gaps (matrix) | Planned feature(s) | Assertion tool |
|---|-----------|-----------|---------------|--------------------|----------------|
| 1 | **gPTP/802.1AS** | es-1.1 cadence via tap | AS-4 latency calib ❌; AS-6 DUT-BMCA 🟡; M-DEV-2/3/4 Pdelay 🟡; M-DEV-13 tu 🟡 | `gptp.feature`, `gptp_latency.feature`, `gptp_bmca.feature`(@wip switch-gated) | `gptp_cadence.py` (tap1, ether[40:2]=0x88f7); CSR GM `0x624/8`, pdelay `0x6E4` |
| 2 | **SRP/lwSRP** | es-1.2 Domain via tap | SRP-9 NxN ❌; SRP-8 class B 🟡; SRP-2 single-stream 🟡; MRP-7 🟡; M-CLK-2 ❌ | `srp.feature`, `srp_nxn.feature`, `srp_classb.feature`(@wip) | `srp_domain.py` (0x22ea), `srp_qna.py`; CSR `0x680/694/698/69C` |
| 3 | **MAAP** | silicon_battery defend check (thin) | (MAAP ✅ RTL, no behave) | `maap.feature` | inject conflict on pw0 → tap defend frame; CSR eff dmac |
| 4 | **AVDECC/ATDECC** | es-2.1..4.18 (63), Suite C bind, Suite D AECP models | AECP-8 🟡; CMD-7 🟡; CMD-14/M-AECP-12 🟡; M-AECP-11 🟡; **M-AECP-9 ❌** | retag es-4.x; `aecp_mvu.feature`(M-AECP-9 @wip); `aecp_identify_cadence.feature` | raw AF_PACKET (`aem/controller.py`, `avdecc_l2.py`, `silicon_battery.Ctl`); la_avdecc counters-probe `verdict CLEAN` |
| 5 | **AAF talker** | Suite C talker_steps (VID2/prio3/subtype/dmac, rate) | SRP-2/SRP-9 NxN | `aaf_talker.feature`, extend for NxN | tap AAF capture → inter-frame Δt histogram, byte fields (`pcap2s32.py`) |
| 6 | **AAF listener** | Suite C bind + counters | **es-4.16 media-map ADD/REMOVE** (absent); AVTP-3 🟡; AVTP-5/M-CNT-4 🟡 | `aaf_listener.feature`, `media_maps.feature`(es-4.16), `pcm_ring.feature` | STREAM_INPUT GET_COUNTERS; AVTPRX `0x6B8/6BC/6C0/6C4` |
| 7 | **CRF/media clock** | Suite C clock_recovery | **CRF-8 ❌**, **M-CLK-3 🟡** (actuator — *proven this session*) | `media_clock_servo.feature` (lock/rails/holdover/auto_repair/soak) | MCSRV_STAT `0x8F8` (state,verified[3],locked[5],trim[31:16]); THD |
| 8 | **ALSA/audio** | Suite C audio THD+N | roadmap-7 playback (KL_pcm_tx); arecord byte-exact | `alsa_record.feature`, `alsa_playback.feature`(@wip) | `tone_thdn.py` (digital ≤−120, analog ≤−80); `pcm_ring_dump.c` |
| 9 | **Link/L1-L2** | es link-flap → counters | **AX42 TX-wedge recovery** (gaps item 0); <50 ms timing | `link_guard.feature` | real flap (`devmem 0xf0003800`); tap TX-liveness; LINK_CTRL `0x71C`, RST_EPOCH `0x720`; LINKG_STAT `0x774` (`{bounce16,flags,state,eth_rst,alive}`) |
| 10 | **QoS/datapath** | `cbs-iperf3-interference.sh` (no behave) | CBS/classifier/TCAM/VLAN behave absent | `cbs_shaper.feature`, `classifier.feature` | iperf3 dual-flow reserved-vs-BE; CBS slopes `0x400+q*0x20` |
| 11 | **DMA/perf** | perf harness (no behave) | throughput/RSC/fanout behave absent | `perf_throughput.feature`(@bench) | iperf3 Mbit; queue-drop + RMON `0x21C/0x230` |
| 12 | **Saved-state** | acmp-persist (no behave) | **M-ACMP-9 ❌** (*proven this session*) | `saved_state.feature` | reboot survival; ACMPL_STATE `0x6A4`; `acmp-persist show` |
| 13 | **RMON/diag** | es-4.15, hive-get-counters | good/bad vs tap ground-truth | `rmon.feature` | RMON `0x21C/0x230` (snapshot `STATS_CTRL 0x200[0]`) vs tap count |
| 14 | **Robustness** | Suite D tsn_gen fuzz; es-4.x refusals | AVTP-3 version gate 🟡; back-to-back eater; reset-defaults | `robustness.feature` (@negative/@rtl-defect) | tsn_gen `packet_gen` fuzz; malformed inject → no-crash + reject |

## 5. P0 backlog — concrete feature skeletons

The 7 ❌ rows split three ways. **Two are already silicon-proven this session** — their
scenarios *flip the matrix to ✅*. Four already-drafted roadmap gates back the RTL lanes
now in flight. The rest start `@wip` and *drive* their implementation.

### 5.1 "Lock the win" (proven this session → author behave → flip ❌→✅)

```gherkin
# saved_state.feature  — M-ACMP-9
@subsystem:saved_state @clause:milan-5.5.1.4 @matrix:M-ACMP-9 @roadmap:9
Feature: Milan saved-state fast-connect

  @tier:t2 @bench
  Scenario: A saved media bind survives reboot and re-arms with no controller
    Given the sink is bound and `acmp-persist save` succeeded
    When the board reboots
    Then S51 restore re-arms the sink to LSM PRB_W_AVAIL (ACMPL_STATE 0x6A4 [2:0]=1)
    And the stream re-locks with no controller present

  @tier:t1 @regression:acmp-persist-wedge
  Scenario: `acmp-persist save` never wedges under the watch daemon
    Given the acmp-persist watch daemon is running
    When I run `acmp-persist save` 6 times back-to-back
    Then all 6 complete within 5 s each with no SPI tx/rx spin   # the tx_ready-gate fix
    And every journalled record verifies byte-exact on readback
```

```gherkin
# media_clock_servo.feature  — CRF-8 / M-CLK-3
@subsystem:crf @clause:1722-10.6 @matrix:CRF-8,M-CLK-3 @roadmap:6
Feature: MMCM-DRP media-clock servo disciplines the local media clock

  @tier:t1
  Scenario: The servo locks at clock_source=2 with the DRP config verified
    Given clock_source == 2 (CRF descriptor) and the CRF sink locked
    Then MCSRV_STAT 0x8F8 state == 4 (LOCKED) and [3] DRP-verified == 1
    And the signed trim 0x8F8[31:16] is within the coherent-chain band

  @tier:t1 @matrix:M-CLK-3
  Scenario: auto_repair repairs a divider mismatch only when enabled
    Given the CLKOUT0 divider is corrupted via DRP
    When auto_repair is enabled (0x8FC reserved-bit, bench-gated)
    Then the servo read-modify-writes it back to the O=43 encoding (state 2 REPAIR→4)
    And with auto_repair disabled the servo issues zero DRP writes

  @tier:t2 @bench @soak
  Scenario: Rails hold zero across an hour soak
    When I soak the locked servo for 1 hour
    Then MCSRV_STAT never leaves LOCKED and no PSDONE/relock fault ([7]/[8]) sets

  @tier:t2 @bench
  Scenario: Coherent analog loop meets the converter-floor acceptance
    Given the coherent CRF chain is locked
    Then tone_thdn.py on the analog loop is ≤ −80 dB (digital wire ≤ −120)
```

### 5.2 Roadmap gates for the RTL lanes in flight (TB proves in sim, behave on the wire)

```gherkin
# link_guard.feature  — AX42 (gaps item 0)
@subsystem:link @clause:milan-gaps-5 @matrix:—(robustness) @roadmap:2 @regression:mac-tx-wedge
Feature: Link-bounce TX-wedge auto-recovery (AX42)

  @tier:t2 @bench
  Scenario: A link bounce recovers TX on the wire within 50 ms, no daemon
    Given the AX7101 streams an AAF talker on e2 and tap1 shows egress
    When I flap the AX e2 link for 100 ms
    Then tap1 egress frames resume within 50 ms of link-up
    And no gateware reload and no phy_crg_reset daemon strobe occurred  # guard covers the PHY-side gtx path

  @tier:t1 @negative
  Scenario: The freeze hook drills the full FSM with no cable
    When I set LINK_CTRL freeze (0x71C)
    Then reinit asserts and eth_rst sequences eth-first-then-sys
    And clearing freeze recovers within the settle window
```

```gherkin
# pcm_ring.feature  — BRAM ring / mf52 no-shed
@subsystem:aaf_listener @clause:milan-gaps-2 @matrix:—(streaming) @roadmap:5 @regression:mf52-shed
Feature: PCM ring integrity under concurrent CPU read

  @tier:t1
  Scenario: Write pointer advances with no mod-24 holes under CPU-read load
    Given a bound 48k-stereo listener and a concurrent arecord rw load
    When I sample the pcm offset CSR across 24k beats
    Then the offset advances exactly 8 bytes/beat with zero gaps   # BRAM ready==1 ⇒ no shed

  @tier:t2 @bench
  Scenario: Recorded audio is artifact-free at the converter floor
    When I arecord 10 s during a concurrent CPU-read load
    Then tone_thdn.py reports no 2 kHz whole-frame artifact and ≤ −80 dB
```

**RTL/TB side already delivered this round (2026-07-23)** — the sim half of these gates
exists and passes; the behave scenarios above are the *wire* half:

| Gate feature | RTL module | Verilator TB (self-checking) | Status |
|--------------|-----------|------------------------------|--------|
| `link_guard` (AX42) | `gmii.py`+`milan_soc.py` `ext_reset` (applied) | `tb/verilator/eth_tx_reset/` 40/40 | **applied + elaboration-clean** (SoC emits netlist w/ `eth_rst`); Vivado build + AX bench remain |
| `pcm_ring` (BRAM) | `hdl/ieee1722/aaf/KL_pcm_ring_bram.sv` (wired `--pcm-ring bram`) | `tb/verilator/pcm_ring_bram/` 17/17 + 9/9 | **applied + elaboration-clean** (ring instantiated, read slave @0x9010_0000, double-drive fixed, default path unchanged); Vivado build confirms ~8 RAMB36 |
| `media_clock_servo` (auto_repair) | `KL_mmcm_drp_servo.sv` (repair FSM) | `tb/verilator/mmcm_servo_autorepair/` 47/47 | TB solid; tie NOT flipped (bench readback of 0x8FC gates enablement) |
| `alsa_playback` (KL_pcm_tx) | `hdl/ieee1722/aaf/KL_pcm_tx.sv` | `tb/verilator/pcm_tx/` 27/27 | scaffold solid; SoC integration design-only (documented caveats) |

### 5.3 "Drive the impl" (`@wip` until the RTL lands)

- `srp_nxn.feature` — **SRP-9** (802.1Q 35.2.7): N simultaneous reservations (AX 8×8),
  per-stream registrar; gated on AX42→8×8 (lane A). `@wip @roadmap:5`.
- `crf_reservation.feature` — **M-CLK-2** (Milan 7.3.3): CRF carried under an SRP
  reservation (2nd lwSRP listener attribute). `@wip`.
- `aecp_mvu.feature` — **M-AECP-9** (Milan 5.4.4.4/.5): SET/GET_MEDIA_CLOCK_REFERENCE_INFO
  (no tokens in `aecp_pkg.sv` yet). `@wip @tier:t0` (tsn_gen model first).
- `media_clock_mgmt.feature` — **M-CLK-5** (Milan 7.6): reference election / MCRI
  priorities; depends on M-AECP-9. `@wip`.
- `gptp_latency.feature` — **AS-4** (802.1AS 8.4.3): per-board ingress/egress latency
  calibration procedure (only the sum is measured today). `@wip @tier:t2`.

## 6. P1 backlog — the 17 🟡 partials (each pins the one missing assertion)

| Matrix | Clause | Feature / step | The specific assertion to add |
|--------|--------|----------------|-------------------------------|
| AVTP-3 | 4.4.3.4 | `robustness.feature` `@rtl-defect` | a v1 PDU is (currently) parsed as v0 — assert present behavior, flip on fix |
| AVTP-5 | 4.4.4.3 | `aaf_listener.feature` `@rtl-defect` | talker `mr` toggle never ticks MEDIA_RESET (pairs M-CNT-4) |
| CMD-7 | 7.4.15/16 | `aecp_stream_info.feature` | SET_STREAM_INFO flags beyond MSRP_ACC_LAT → NOT_SUPPORTED (documented) |
| CMD-14 | 7.4.39 | `aecp_identify_cadence.feature` | IDENTIFY_NOTIFICATION periodic re-send cadence while active |
| AECP-8 | 9.4 | `aecp_address_access.feature` `@negative` | ADDRESS_ACCESS admits only AEM/VU; hostile write-TLVs dropped |
| MRP-7 | 10.7.10 | `srp.feature` | explicit PeriodicTransmission enable/disable vector |
| SRP-2 | 35.1.2 | `srp.feature` | talker declare/withdraw (single-stream today; NxN → SRP-9) |
| SRP-8 | 35.1.4/34.5 | `srp_classb.feature` `@wip` | declaring/using SR class B (engine is class A only) |
| AS-6 | 10.2/10.3 | `gptp_bmca.feature` `@wip` | DUT-wins-BMCA (switch-gated; USER attack-list bottom) |
| M-DEV-2 | 4.2.6.2.5 | `gptp.feature` | multiple Pdelay responses handling |
| M-DEV-3 | 4.2.6.2.6 | `gptp.feature` | Pdelay turnaround bound measurement |
| M-DEV-4 | 4.2.6.2.7 | `gptp.feature` `@negative` | negative Pdelay values |
| M-DEV-13 | 4.3.5.2 | `aaf_talker.feature` | talker-side `tu` set on a real GM change |
| M-AECP-11 | 5.4.5.3 | `avdecc` | ADP-departure-triggered controller cleanup |
| M-AECP-12 | 5.4.5.4 | (= CMD-14) | identify notification |
| M-CNT-4 | Table 5.17 | `aaf_talker.feature` | STREAM_OUTPUT MEDIA_RESET asserted (pairs AVTP-5) |
| M-CLK-3 | 7.2.2/7.5.2 | (= §5.1 servo) | actuator — covered by media_clock_servo.feature |

**Doc bug — RECONCILED (2026-07-23):** the summary tallied 18 partials / 9 Milan, but a
1:1 re-count of every Milan row's leading glyph gives **39✅ / 8🟡 / 4❌ / 1➖ = 52**. It
was a summing typo (one ✅ counted as partial), not a mismarked row — no compliance status
changed. `SPEC_TRACEABILITY.md` now reads **163✅ / 17🟡 / 7❌ / 17➖** (Milan 39/8). The
17 🟡 rows above are the authoritative partial backlog. Stale downstream quotes of
"162✅/18🟡" (HANDOVER roadmap table) should now read 163✅/17🟡.

## 7. P2 — regression pins + verification infrastructure

- **Regression-pin** one scenario per hard-won past bug (`@regression`): mf52 ring-shed,
  vid2-clobber, ACMP listener deafness, back-to-back eater, double-Philips, mac-tx-wedge,
  ingressLatency, I2SPB double-delay. Red-if-it-regresses forever.
- **tsn_gen model authoring — committed P1 lane** (USER 2026-07-23: in scope). The
  verification-infra gap is that only AECP/ADP have tsn_gen YAML models; ACMP, all of
  802.1Q, gPTP, MAAP, and CRF have none, so those ✅ rows can only be *replayed*, not
  *fuzzed*. Author order (highest value first):
  1. **ACMP model** (`protocols/acmp/*.yaml`) — lets the suite fuzz connection-management
     (BIND/UNBIND/PROBE/GET_RX_STATE); pairs with Suite D `acmp_listener_tsn_gen.feature`
     and the CERT ACMP path. Highest-value: ACMP is the most stateful engine with no model.
  2. **CRF model** (M-CLK-1 params) + **MRPDU/MSRP models** (M-DEV-5..9, 802.1Q) — fuzz the
     reservation + media-clock framing.
  3. **gPTP model** + **MVU payload models** (GET_MILAN_INFO / SYSTEM_UNIQUE_ID /
     MEDIA_CLOCK_REFERENCE_INFO — the last unblocks the M-AECP-9 `@wip` scenario).
  Each model is exercised via the existing `@tsn_gen` tier (`packet_gen` codec, `tsn_gen_steps.py`),
  so no new harness — just the YAML + a fuzz scenario per model asserting "no illegal
  transition on N seeded frames" (the pattern already in `acmp_listener_tsn_gen.feature`).
- **Breadth pass**: a single passing scenario across all 14 domains (the "whole-system
  smoke" ring) once P0 lands.

## 8. Cross-cutting infrastructure

- **Add `behave.ini`** at each suite root with the tag taxonomy + a `default` profile that
  excludes `@wip,@bench,@soak` (the CI green gate). None exists today.
- **Converge suites A and B** (they differ in 8 files and will keep drifting); keep one
  CERT tree, snapshot only for release tags. Commit the `aem/` package into the tracked
  tree (today it lives only in the private snapshot; the tracked steps `import from aem`).
- **CI**: `Containerfile.bdd-runner` + `Containerfile.dut-sim` already exist for Suite D —
  wire the T0 green gate into it; no CI YAML exists in any repo yet.
- **Harness traps every new step must bake in** (from BENCH_TOPOLOGY / tool sources):
  ProfiShark **+28** byte offset, never `tcpdump -e`; raw AVDECC sockets **must
  PACKET_MR_PROMISC-join `91:E0:F0:01:00:00`**; ADP census matches `ether[14]==0xFA`;
  board ACMP/MAAP responses do **not** reach pw0's port (switch relay gap → verify via
  CSR/counters, not capture); la_avdecc feature-defines are ABI; `AAF_CTRL 0x654` writes
  must preserve VID 2; a new plain-RW CSR ≥0x800 needs the `rd_in_window` carve-out or
  reads lie; validate wire frames by **length**, not headers alone.

## 9. Execution phasing

1. **Infra** — `behave.ini` + tag taxonomy; retag existing es-4.x / Suite C / Suite D
   scenarios with `@subsystem/@clause/@matrix/@tier`; converge A/B; commit `aem/`.
2. **P0** — §5 features (3 "lock the win" + 4 roadmap gates + 5 `@wip` drivers). The
   roadmap gates come online as the RTL lanes (AX42, BRAM ring, servo, KL_pcm_tx) land.
3. **P1** — the 17 🟡 rows (§6), reusing existing steps.
4. **P2** — regression pins, tsn_gen ACMP model, whole-system smoke ring.

Run: T0/T1 green gate `behave --tags=-wip --tags=-bench --tags=-soak`; add `--tags=bench`
on the rig (`run_alinx.sh`/`run_arty.sh` pattern); compliance report per row via
`--tags=@matrix:<row>`.
