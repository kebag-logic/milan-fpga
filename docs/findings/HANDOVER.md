# HANDOVER — machine, topology, live state, tasks

> **Fresh session? Read `BENCH_TOPOLOGY.md` (same directory) FIRST** —
> it is the where-is-what: machines, consoles, build/flash pipeline,
> pw0 tooling, CERT-suite privacy rules, and the at-handover state.

Updated 2026-07-20 (all-night CERT conformance campaign + two-entity re-verify
after the AX manual power-cycle; ACMP-timeout mystery SOLVED = test-tool NIC
filter, never a DUT bug).
This is THE entry point for a fresh session or person: everything needed to
operate the bench, trust the current state, and pick the next task. Detail
lives in the named normative docs; this file states what is true NOW.

---

## ★ CURRENT STATE 2026-07-21 all-night — CLOSE-ALL-GAPS CAMPAIGN (read first) ★

**USER directives this night: CRF talker for the e2e test ("crf is paced @
2ms... the PTO applies like any streams"), "to flash use qspi" (AX policy
flipped), "you have a night to close all gaps".**

1. **CRF talker KL_crf_tx IS IN (0e5e8a7 + PTO 0821aeb):** Avnu Pro Audio
   500 PDU/s sourced from the REAL audio-MMCM 96-sample grid
   (self-contained /512+/96 divider in cd_audio, cdc_pulse, ptp_now
   capture), every timestamp future-dated by the presentation time offset
   from the SAME source as the AAF framer (SET_STREAM_INFO ACC_LAT/MTT,
   reset 2 ms) per the USER's Milan reading. CSRs 0x750-0x764; 6th
   control-merge source (untagged best-effort until the 2nd lwSRP TA
   attr). S50 provisions the ALINX with DMAC = MAAP claim+1 on gateware
   >= 0x0005 (VERSION bumped f301cde; rootfs #8 = 6068b11). TB: module 31
   (incl future-dating window + skip-on-busy grid truth), dp loopback
   closure (tx->rx locked). **Wire e2e pending an AX >= 25 bitstream.**
2. **CRF rx SILICON-PROVEN vs a synthetic pw0 source (mf37):** locks
   in-stream, 13000/13000 PDUs counted zero-loss (incl a 4x overspeed
   burst - injector pacing quirk), fmt/seq 0, rate-from-ts-field = 0,
   100 ms timeout unlock, delta latch. /tmp/crf_inject.py + provisioning
   recipe in BENCH_TOPOLOGY.
3. **CRF sink-1 bind chain IS IN (b692395, silicon pending mf40/AX25):**
   listener uid=1 = a REAL bind record (fast-connect sid/dmac from the
   command, zero-sid falls back to {eid,tuid}; no probe SM/MSRP attach/
   depart-watch - documented), GET_RX_STATE + GET_STREAM_INFO(input 1)
   reflect it, the datapath drives KL_crf_rx en/sid from the bind (CSR
   pair stays the manual lever), ACMPL_STATE bit31 = bound. dp TB proves
   CONNECT_RX(uid1) -> engine locks on the bound sid -> DISCONNECT cuts.
   **Servo actuator gap named precisely:** the clean-clock rework RETIRED
   the NCO (trim_o = 0, "future MMCM-DRP servo") - CRF clock recovery
   needs that DRP engine; measurement + bind + CLOCK_DOMAIN muxing are
   done, actuation is the remaining engine (gaps doc).
4. **0x4B silicon saga - THREE defects deep, forensics armed:** (a) the
   BSCAN capture race (a4c0630, mf38); (b) cbuf RAM written inside the
   async-reset engine block -> Vivado refuses RAM inference (Synth
   8-4767) and mangles set/reset priority ("may cause simulation
   mismatches") -> silicon garbage scans while ALL TBs pass; fixed
   f3f4b15 (own sync-only process; 8-4767 verified GONE from mf39+
   builds); (c) mf39 silicon STILL answers BAD_ARGUMENTS deterministically
   (empty batch SUCCESS / 1-record 0-for-50 / echo byte-perfect = the
   discriminator) -> live suspect = block-local `automatic` temporaries in
   the scan/parse clocked phases (the synth log materializes such locals
   as sequential elements); hoisted to comb wires + **BDBG CSRs
   0x768/0x76C/0x770 latch {header bytes as scanned, cmd15+dlen16,
   ptr+end} at every verdict** (b692395, rides mf40/AX25) - if the hoist
   is not the mechanism, ONE devmem read after a failing probe names it.
5. **AX QSPI policy images->boot (USER, 17acf0b):** the manifest-"full"
   layout has always reserved bitstream@0 (kernel at 4 MiB - the
   kernel-clobber note described the DEAD layout); 3.6 MiB bit + 8.2 MiB
   rootfs fit the 16 MB flash. `build.sh flash ax7101:` now writes
   gateware + images in one verb; whether the FPGA self-configures from
   QSPI depends on the board's mode pins - JTAG stays the belt, a
   --reset after the first flash is the test.
6. **CERT suite 43 -> 63 scenarios:** es-4.1/4.2/4.6/4.11/4.14/4.15/4.17/
   4.18 recreated (new steps es4x_steps.py; la_avdecc-consistent
   expectations: ACQUIRE rejected, LOCK exclusion + 60 s self-expiry
   LIVE-verified, START/STOP_STREAMING input-only + unsolicited,
   GET_MILAN_INFO version 1, counters masks 0x23/0x3/0xF3F @ cdl 148),
   **es-1.1 ALINX-GM half** (ProfiShark tap cadences: announce 1.0001 s,
   sync 8/s, pdelay 1/s, priority1 238, clockClass 248; the DUT-wins-BMCA
   variants stay switch-gated) and **es-1.2 SRP wire half** (every Domain
   declaration = {class A(6), prio 3, VID 2}). Tap helpers
   /tmp/gptp_cadence.py + /tmp/srp_domain.py on amx-ubuntu-server; suite
   snapshot in private/recreate/aets_recreate_20260721 (git-ignored).
   **★ ARTY mf39: 61/61 scenarios, 305/305 steps, 0 failures ★** (+ the
   2 tap features green in separate runs).
7. **Loop analog leg BROKEN tonight (-2.8 dB, level-tracking):** the
   decomposition exonerates every digital path - AX source at the tap
   -135.1 dB, ARTY's own digital tone through its talker -135.1 dB, LPF
   on/off immaterial - the DAC->cable->ADC leg is sick in a saturating,
   level-tracking way (NOT the sign-square class). Physical/PMOD
   suspicion (the same leg was reseat-cured 07-20); MORNING BENCH ITEM.
   New trap: pcm_ring_dump SEGFAULTS on mf39+rootfs#8 (mmap page fault at
   the ring read) - the pre-DAC ring check is unavailable until fixed.
8. **Silicon state:** ARTY QSPI = **eto_milanfinal39 (+0.099) + rootfs #8**
   (boot-verified, VERSION 0x0005, 61/61 cert). mf38 (eto +0.158) was
   flashed and superseded the same evening (its 0x4B is broken on
   silicon). AX = **eppo_milanfinal21 SRAM + rootfs #4 still** - AX24
   FAILED TIMING x3 (asl -0.045 / eto -0.209 / eppo -0.288; violators =
   the OLD lwsrp-walker + batch_q marginal cones, not the CRF logic);
   **AX25 sweep in flight** (HEAD b692395, everything above), mf40 arty
   sweep auto-chains after it; extra AX seeds with fresh place
   directives if wave 1 misses.
9. New traps burned: git-worktree + SYMLINKED third_party makes verilator
   resolve ../.. into the MAIN repo (silently builds stale RTL - copy,
   never link); `timeout N sudo tcpdump` leaves the root child running
   (sudo timeout N tcpdump); tap filters for TAGGED streams need
   ether[44:2]=0x22f0 (the VLAN pushes the ethertype +4 past the +28
   record header); KL_crf_tx had to be registered in a FOURTH source
   list (milan_soc.py) beyond verilator/yosys/dp-TB.

## ★ PREVIOUS 2026-07-20 night — COMPLIANCE-GAPS ROUND ★

**"continue to fix all gaps" campaign (post-43/43 cert), all committed:**
1. **Honest capability counts**: ADP talker sources 8→1, listener sinks
   8→2 (S50 0x618/0x61C; ENTITY overlays follow).
2. **No-change SET suppression generalized**: WRITE_S reads the old store
   byte before writing (2-phase), wb_diff gates the u=1 replay — covers
   SET_NAME/SAMPLING_RATE/CLOCK_SOURCE/STREAM_FORMAT beyond es-4.5.
3. **Audio maps: RESOLVED AS COMPLIANT** — Milan 5.4.2.27/28 mandates
   NOT_SUPPORTED for ports WITH static Audio Maps (we have them).
4. **GET_DYNAMIC_INFO rewritten to the real 7.4.76 BATCH semantics**
   (the pipewire-modeled fixed blob ignored request records = garbage to
   a parsing controller): 512B capture, BSCAN validate/size pass
   (non-fixed-size type → whole-cmd BAD_ARGUMENTS+echo; over-cap records
   skipped per spec), per-record dispatch through the normal segment
   engine (record-virtual arg window/echo base), NOT_SUPPORTED+echo for
   legal-unimplemented, 8B record headers; ingress FIFO 1024. TB checks
   every record BYTE-EXACT vs its classic response. aecp 469.
5. **CRF measurement engine (Milan 7.3.2)**: KL_crf_rx + parser fsh2
   extension; CSRs 0x738-0x74C (en/sid, delta = ts_delta contract,
   256-PDU/512ms rate error, status, lock); CLOCK_DOMAIN LOCKED/UNLOCKED
   muxed to CRF when clock_source=2. Remaining chain: ACMP sink-1 SM,
   2nd lwSRP listener attr, servo hookup. dp TB 105 (13 CRF checks).
6. **es-1.1 recreation BLOCKED by the bench switch**: it claims gPTP
   priority1=246/cc248/acc0x20 (tap-read) — outranks every Milan-legal
   end-station value. Bench keeps priority1=100 override (ALINX-GM
   one-oscillator architecture); **cert/shipping value = 246** — needs
   the switch claim weakened (mgmt ssh 192.168.127.1, user credentials).
   Official es-1.1 interval checks verified against our gptp.cfg
   (announce 0, sync −3, pdelay 0 ✓).
Silicon: mf37 (arty) + AX22 sweeps carry 1-5; verification tools staged
on pw0 (/tmp/dyninfo_probe.py = batch-vs-classic byte-exact,
/tmp/crf_inject.py = 500Hz Milan CRF source). Rootfs #6 staged (counts +
priority1-override comments). CERT rerun follows flash.

## ★ PREVIOUS 2026-07-20 late ★

**LPF + AS_PATH + overlay + VID-2 + servo round (07-20 evening).** Four
user-caught issues, all root-caused, fixed, committed, silicon-verified:

1. **AAF VID-0 flood** ("the AVTP is sent everywhere"): S50's
   `w 0x654 0x3` clobbered AAF_CTRL's VID[27:16] → untagged SR frames =
   best-effort flood on every switch port, no pruning, no shaped path
   (all earlier audio ran best-effort despite res_active!). Fix
   `0x00020003`; tap-proven: PCP3/VID2 tags, switch prunes to zero ports
   when unbound, forwards ONLY to the bound listener, pw0 clean.
2. **AVB_INTERFACE overlay +2** (Hive showed one arbitrary gPTP flag):
   gen_aem_store.py put the MAC/CLOCK_ID overlays at A+72/A+80 vs spec
   70/78 — the MAC tail overwrote interface_flags (wire 0x0001/0x0002 =
   MAC last bytes) and shifted clock_identity. The aecp TB had the same
   wrong offsets (it validated the bug). Both fixed; wire now 0x0007 +
   correct MAC/ckid on BOTH boards.
3. **GET_AS_PATH** per 1722.1-2021 §7.4.41.2: path_sequence = Announce
   PathTrace = [GM, traversed bridges]. New AS2 CSRs 0x730/0x734 fed by
   gptp2csr (pmc PARENT_DATA_SET parentPortIdentity). Wire: ARTY n=2
   [GM 020000fffe000001, switch 3cc0c6fffefe0210], ALINX-GM n=1 [self].
4. **KL_pcm_lpf** (fc 20 kHz Butterworth on the DAC render tap only,
   LPF_CTRL 0x72C default-on, auto-bypass ≠2ch): v1 combinational cone
   failed AX 100 MHz (WNS −4.7); **v2 = serial-MAC** (one shared 17×24
   mult, ~12 cyc/pair, burst FIFO, own m_tvalid + capture mux in
   KL_i2s_playback). Loop A/B servo-locked on the reserved path:
   **ON −73.4 dB (all-time record), OFF −72.2**. NB: pure-ACMP binds
   keep the 8ch default format = LPF bypassed; SET_STREAM_FORMAT
   0x0205022000806000 (2ch) engages it.

**Media unlock cycle root-caused (was hiding for days as "variable loop
numbers"):** (a) stream_phc_sync steered the PHC whenever portState !=
SLAVE — on the GM board that's ALWAYS (MASTER), so a listener bind made
the ALINX slew the domain's timebase every poll; and a single pmc
timeout triggered multi-ms PHC steps that blew up ptp4l (log: adj −5..
−9 ms, rms 777 µs). Fixed: SLAVE|MASTER both = healthy + 5-poll miss
hysteresis. (b) kl-eth TX-timestamp kworker can stall >50 ms under
CPU/bus load → ptp4l SLAVE→FAULTY (16 s reset) → unlock;
tx_timestamp_timeout 50→500 ms. STREAM_INPUT counters LOCKED/UNLOCKED
are the detector (SEQ/INTERRUPTED stay 0 — wire was never at fault).
Driver-side stamp-latency fix remains owed (workarounds section).

**★★ FINAL DUAL-BOARD CERT CERT (07-20 late): ARTY 43/43 + ALINX
43/43, 0 failures ★★** (suite grew to 15 features / 43 scenarios with
the new AS_PATH + counters coverage). Keepers: **ARTY QSPI =
`asl_milanfinal35` (+0.310, serial-MAC LPF v2)**, **ALINX SRAM =
`eppo_milanfinal21` (+0.057, v2)**, both + rootfs #4 (VID-2 S50,
gptp2csr parent publish, stream_phc_sync role fix, 500 ms tx-ts
timeout). Harness fix folded in: the la_avdecc counters-probe expected
the pre-revert ENTITY GET_COUNTERS non-success — now expects
SUCCESS+empty (built on pw0; the old binary only ever lived on pw1). Tool fixes:
milan_controller.py ENTITY_DISCOVER cdl 0→56 (a Hive cdl=0 report on
07-20 13:50 was OUR tool from pw0, not the DUT). Board file transfer:
boards run dropbear (root@22) — scp via pw0; ProfiShark BPF offsets +28.

## ★ PREVIOUS STATE 2026-07-20 (dual-board cert) ★

**★★ DUAL-BOARD CERT CERTIFICATION (07-20): ARTY 41/41 + ALINX 41/41 ★★**
RE-CONFIRMED on the final durable state (cold-booted rootfs both boards,
ALINX-as-GM from boot, one gPTP domain, reseated loop): ARTY 41/41 +
ALINX 41/41 in a single back-to-back confirmation run.
Every scenario of every recreated CERT feature passes on BOTH boards
(es-2.1 through es-4.13, hive-get-counters, link-flap; ALINX 3x-stable
on link-flap after one cold-path first-run outlier). Final keepers:
**Arty QSPI = `asl_milanfinal33` (+0.120)**, **AX SRAM =
`eto_milanfinal19` (+0.094)**, both + the final rootfs (up-after-settle
linkmon, vt=10, board names, gm_locked, rx_packets liveness). Post-cert
sanity: la_avdecc CONNECT SUCCESS both Milan=1, ALINX -126.2 dB;
ARTY-loop degraded to -57..-60 dB (was -66..-70) - DIAGNOSED as the
ANALOG leg only: the arty's own digital tone through the same talker =
-125.5 dB, capture 0 seq-gaps, clocks stable, harmonics clean -87 dBc,
broadband-only on both channels = physical loop-cable/PMOD connection
(disturbed during the bench AX intervention?). RESOLVED by the user's cable
reseat: loop back to -64.7..-65.9 dB. Also fixed during the diagnosis (and made cold-boot-durable after two
follow-up traps): **the ALINX is grandmaster by priority1=100**. Traps:
(a) the base gptp.cfg SHIPS priority1 248, so an append-if-absent never
fired - S50 now sed-REPLACES; (b) when a board IS the GM, linuxptp
reports gmPresent=false and gptp2csr published ZEROS as the ADP
gptp_grandmaster_id, putting the GM board in a different Hive "gPTP
domain" than its slaves = the user-seen WRONG-DOMAIN error - gptp2csr
now publishes the LOCAL clockIdentity in that case. Cold-boot-verified:
both entities advertise gm=020000fffe000001 (the ALINX), one domain,
loop -64.7 dB with fully coherent clocks. The mf33/AX19 deltas vs mf31/AX18: ENTITY
GET_COUNTERS SUCCESS+empty revert (Hive), nochg replay suppression,
freq-scaled ADP DELAY (the 100 MHz AX).

**Two-entity finale (AX18 + mf31, 07-20):** la_avdecc CONNECT SUCCESS,
both Milan=1, listener Connected; pdelay 96% (capture-edge misses);
**MVRP 46/45 s on the wire from the arty, paired with MSRP** (the IFG
gasket holding on final silicon); AX reservation res_active + gate +
slope (0x37E); audio ALINX −126.2 dB / ARTY loop −68.0 dB. ACMP via the
FIXED avdecc_l2: **15/15**. Both entities
alive, discoverable, Milan-clean on the wire.

**★ THE ACMP-TIMEOUT MYSTERY IS SOLVED — it was NEVER our DUT. ★** The
session-long "intermittent ACMP CONNECT_RX timeout" against avdecc_l2 was the
CONTROLLER's raw AF_PACKET socket not joining the AVDECC multicast
(91:E0:F0:01:00:00): the pw0 NIC's multicast filter dropped the DUT's
CONNECT_RX_RESPONSE, so avdecc_l2 "timed out" even though the listener had
responded + settled to 0xE07F EVERY time (the forensics always said so — that
was the tell). Reliability appeared to "flip" only because whatever other tool
ran last sometimes left enp6s0 promiscuous. FIX = `PACKET_MR_PROMISC`
membership in `~/the-private-test-repo-controller/avdecc_l2.py` on pw0 →
**15/15 connect success**, deterministic. The earlier "response-delivery
timing/race, masked by controller retry" conclusion (§ lower down) is
**RETRACTED**. Lesson for the next tool bring-up: a raw-socket AVDECC
controller MUST add the 91:E0:F0:01:00:00 membership or go promiscuous.

**★ USER-CAUGHT Hive ADPDU crash (protocolAdpdu.cpp:77) FIXED. ★** Hive/
la_avdecc logged `ControlDataLength minimum 56, only 0 advertised` for
[68:05:CA:95:B2:D1] — that MAC is **pw0 itself** (the silicon_battery probe),
not a board. Our ENTITY_DISCOVER built the ADPDU with cdl=0; our fabric was
lenient so it "worked", but strict receivers (Hive) reject/could-crash. FIXED
`silicon_battery.py` ENTITY_DISCOVER to cdl=56 + valid_time. Wire re-swept:
**every ADPDU from every source is now cdl=56 = Hive-safe.** (Board ADP
advertisements were always cdl=56/correct.)

**CERT Milan endstation conformance (behave cert_recreate + tsn-gen models,
pw0 ~/cert-run):** essentially the whole plan now passes. es-2.1 (ADP DELAY),
es-3.1 (model_id), es-4.3 (SET_CONFIG, model-adapted), es-4.4 (STREAM_FORMAT,
channel-adaptive), es-4.5 (SET_STREAM_INFO unsol), es-4.7/4.8/4.9/4.10/4.12/
4.13, hive-get-counters, **link-flap** — all green or fixed at HEAD. See the
per-fix list in the campaign section below.

**Board entity names (USER):** first 8 chars of `entity_name` overlaid from
CSRs 0x724/0x728 (nonzero = override ROM; SET_NAME still wins). S50milan writes
**"ARTY"** / **"ALINX"** per `/proc/device-tree/model`.

**Bench-op reminders unchanged:** AX power = powerstrip **OUT0** (the user
power-cycled it this session to clear a JTAG "TDO stuck at 0" hang — a manual
reset is the only recovery; do NOT script OUT0 cuts). Switch = OUT4. Every
openFPGALoader carries `--ftdi-serial` (AX `210512180081 -c ft232`, Arty
`210319AFEED0 -c digilent`). AX flash = images-only (bitstream slot NEVER);
`flash-images` loads a JTAG SPI-proxy so JTAG-reload the gateware after.

---

**Project in one paragraph:** a fully-FPGA Milan v1.2 AVB endstation — the
whole TSN datapath AND the AVDECC control plane (ADP + AECP/AEM + ACMP talker
SM) run in fabric, zero-CPU; a VexiiRiscv 2-hart Linux softcore does only
provisioning, linuxptp and ops (USER DIRECTIVE rev 2: "everything goes FPGA,
use lwSRP" — normative split: `docs/design/ARCHITECTURE_HW_SW_SPLIT.md`).
Roles: AX7101 = the full endstation (:01), Arty A7-100 = a small endstation
(:02), nothing bridge-side in scope. Both boards are silicon-validated
**Milan=1 CLEAN** (la_avdecc) as of 2026-07-14.

---

## 0. BENCH SESSION 2026-07-18 (audio quality root-caused) — results + open items

**User-audible bug ("pumping") root-caused end to end.** The morning silence
("nothing on the Arty PMOD") and the afternoon pitch-pumping were TWO
distinct defects, both now fixed in RTL (milanfinal9, build pending):

1. **Silence** = format mismatch, NOT the switch: the AX transmits 2ch
   frames (framer hardwired stereo) while its AEM STREAM_OUTPUT *declared*
   8ch; Hive format-matched the arty listener to the declared 8ch → RX
   monitor rejected every frame UNSUPPORTED (0x6C0 mid-byte counting).
   Diagnosis path: `ip -s link` showed ~7 kpkt/s arriving while FRAMES_RX
   sat at 0 → wire capture → chans=2 on the wire. Fix = **talker truth**
   (`fd11b4d`): STREAM_OUTPUT declares + accepts ONLY the wire format
   (2ch 48k); listener stays adaptive (1..8ch). Controller gained
   `--bind TALKER_SFX LISTENER_SFX` (talker fmt → listener fmt →
   CONNECT_RX) — user bug 5.
2. **Pumping** = media-clock rate: wire cadence measured EXACTLY 122,880 ns
   /frame = clk/2^N = **48,828.125 Hz** (+1.725%), outside the playback
   servo's ±1.56% range → servo limit-cycled (trim swept −412→+510, fill
   68→351, ~4 s period). Fix = `KL_media_adv` fractional-N advance
   (`c9f0e8b`), sim-measured 48,000.000 Hz. Digital wire quality itself is
   PRISTINE: **THD+N −149.7 dB** (pw0 capture, 20k frames, 0 gaps).
3. **Second stream discovered**: the ARTY was also transmitting (Hive
   cross-connect probe-activated its talker) −132 dBFS noise into the SAME
   DMAC. Cleared via DISCONNECT_RX on the AX listener; MAAP enable is the
   structural guard (still en=0).
4. **gPTP dynamic info now live** (user bugs 1-4, `eca5510`): GM regs
   0x624/0x628 already existed (daemon-writable); NEW `GPTP_PDELAY` 0x6E4
   (RW ns) feeds GET_AVB_INFO propagation_delay; flags |0x02 when GM
   present; GET_AS_PATH is GM-aware ([GM,us] on foreign GM). Board daemon:
   the-private-test-repo `fpga/tools/gptp2csr.sh` (pmc → devmem, 5 s poll).
5. **Media-lock semantics per clock source** (USER rule, `f4eaf52`):
   internal = lock on first valid PDU (buffer position); external
   (stream/CRF) = lock gated on servo convergence (fill mid±64/100 ms,
   exit ±128; unlock on divergence). rxmon TB 69.
6. Format-change lock loss (user bug 6) DISPROVEN in fabric (TB [27]:
   relock on next matching PDU after silence-unlock) — the silicon symptom
   was controller-left mismatched formats = bug 5.

**Traps burned this session:**
- **Build launcher env — TWO requirements** (cost 4 wasted launches):
  (1) venv on PATH (`export PATH="$HOME/litex-milan/venv/bin:$PATH"`) —
  the BIOS Makefile invokes bare `python3 -m litex...crcfbigen`, so
  calling the venv python explicitly is NOT enough; (2) `source
  /home/alex/Xilinx/2026.1/Vivado/settings64.sh` — nohup/scripted envs
  have no Vivado (LiteX dies post-BIOS with "Unable to find or source
  Vivado toolchain"). Interactive shells get both from the profile,
  which is why manual runs always worked. Scratchpad `launch_ax9.sh` /
  `launch_arty9.sh` are the canonical templates. Also: `pkill -f` with a
  plain build-tag pattern kills YOUR OWN shell and any monitor whose
  command text contains the tag (exit 144) — use a bracket pattern like
  `pkill -f "output-dir.*milanfinal[9]"`.
- pw0 can NEVER see the boards' ACMP responses (fabric TX doesn't cross
  Linux tcpdump on-board; the switch doesn't relay board ACMP multicast
  uplink) — verify ACMP effects via CSRs (0x6A4/0x6B0), not pcap.
- ADP GM/AS_PATH/AVB_INFO were all correct RTL-side but nothing ever
  WROTE the GM CSRs — "displays wrong GM" class bugs are provisioning.
- STREAM_OUTPUT format ≠ wire format is a silent trap: TBs used the
  generator as oracle so declared-vs-wire divergence was invisible to
  every suite; only a format-matching controller (Hive) exposed it.

**MILANFINAL9 AX ON SILICON (later 07-18):** all 3 seeds timing-met
(eto **+0.057** = keeper, JTAG-SRAM loaded; asl +0.043, eppo +0.004);
wire cadence measured **median 125,000 ns/frame = 48,000.000 Hz PASS**
(was 122,880 / 48,828.125). Talker-truth live: GET_STREAM_FORMAT(out0)
returns the 2ch wire format; `--bind 0001 0002` matched the listener and
locked (RATE ~8.1k). **Mirror bug found by that very test**: the arty
PLAYER's nominal NCO step (0x8000) is the same clk/2^N = 48,828 Hz
architecture — vs the now-true 48k source its trim pegged **−512 with
fill 5** (floor 48,065 Hz, still +65 Hz fast → periodic underrun dumps).
Fix `10f3616`: NOM_STEP from CLK_FREQ_HZ (32212, −8 ppm, same value on
both boards). Arty milanfinal9 sweep carries it + TONE_CTRL[3:1] tone
attenuation (`fbf19eb`; the analog loopback clips the Pmod ADC at
0 dBFS — H3 within 1 dB of H1 measured). NOTE: the AX build is 2 commits
behind arty (no attenuation/player-step — AX player unused; analog
THD+N acceptance needs an AX round with attenuation or a passive pad).
**Loopback instrument**: PMOD line-out→line-in loop; arty talker in
bypass (0x654=0x3, tone OFF) streams the played audio back as sid :02 →
pw0 capture = frequency-vs-time of what the DAC actually plays (this
measured the wobble: ±1.5 % @ ~2 s period = exactly the servo clamp).
**Post-power-cycle rebuild traps:** pw0 /tmp wiped (redeploy
milan_controller.py + gptp2csr.sh), scratchpad tooling wiped (con.sh /
daemons / numpy venv), AX JTAG reload = fresh boot → console needs
`root` login + `dmesg -n 1` (kl-eth bd-stage spam buries it), and
board-side ramfs deployments are lost on the reloaded board.

**CLOSED (eve 07-18): AUDIO CLEAN END-TO-END ON MILANFINAL12.** Final
loopback verdict: played tone **1000.297 Hz, 0.3 mHz pp (0 ppm wobble)**,
level −17.5 dBFS, 1 seq gap / 70k frames — vs ±15 Hz @ 2 s at session
start. Arty keeper = **eppo_milanfinal12 (+0.126) QSPI-flashed**; AX keeper =
**eppo_milanfinal11 (+0.073) JTAG-SRAM** (walker fix + watchdog +
forensics + attenuator; cadence re-verified 125,000 ns PASS; rebind
SUCCESS post-reload; arty SETTLED/locked/RATE 8.6k/trim 0). Free-run internal clock per USER rule: trim frozen 0, fill
drift ~12 ppm (slip every ~minutes, accepted); SET_CLOCK_SOURCE(1)
engages the servo when exact tracking is wanted.
**THE REAL AFTERNOON VILLAIN was the CONTROLLER, not (only) the fabric:**
(1) my `bind()` sent 68-byte ACMPDUs — 2 bytes short (missing the
reserved tail) — and the listener len check RIGHTLY rejected every one;
Hive's spec-correct 70-byte frames were the only accepts all day (fixed
`9cf1842`). (2) bind()'s GET_STREAM_FORMAT readback was offset +2
(r[44:52] vs r[42:50]) so the listener kept its 8ch default → the whole
stream rejected UNSUPPORTED post-bind (same fix). The forensics CSR
0x6E8 pinpointed both in ONE read each (flags 0xE7 = len fail; then
UNSUPPORTED counting + fmt readback). The always-armed capture fix
(440f6fb) is silicon-validated too (dst captures clean under full
flood) and the zero-gap loss it fixes was REAL (unit [Z]).

**(root-cause narrative of the fabric-side fix, for the record):** ACMP listener deafness = the
walker's 1-cycle CLASSIFY blind window × gap-compressed RX.** The
capture logic ran only in COLLECT_S; a frame arriving ZERO-GAP behind
the previous one loses its beat-0 (dst) capture during CLASSIFY_S.
On silicon the RX FIFOs drain gaplessly whenever the DMA consumer
stalls (kl-eth gro ~56 µs/frame vs 125 µs spacing = chronic backlog),
so EVERY queued command followed an AAF-flood frame into the blind
window → ~100 % loss; the rare accepts were frames that arrived into
an idle FIFO. Morning "cmd_count 84" = Hive retransmit persistence.
Unit repro [Z] (acmp_lstn TB): AAF frame + command back-to-back with
zero idle beats → command lost; FIX `440f6fb` = ALWAYS-ARMED capture
(captures run through CLASSIFY_S, capture owns wbeat/ovfl, beat-0
clears ovfl, runts dropped, fword stays RESPOND-protected — b2b
double-command response loss is retransmit-covered). [Z] green, lstn
102, dp 78, yosys 27. Extra hardening from the hunt (all shipped):
TX-grant watchdog + wedge counter (`b8e4613`, proven NOT the cause:
WEDGE=0 on mf10), walker forensics CSR 0x6E8 (`c0360bb`).
**milanfinal12** (arty, in flight) = fix + forensics + servo rule +
everything since mf9. AX needs the same fix (milanfinal11+ AX round
queued behind).

**(the original elimination table, kept for the record):**
Both boards, milanfinal8 AND 9/10, accept ~0-2 listener commands then
nothing (CC frozen; responders/AECP/ADP/streaming all fine on the same
multicast stream). Eliminated WITH EVIDENCE: switch aging (responders
answer multicast live), allmulti (MAC_CTRL=0x1B has bit3), bypass mode,
lwSRP off, entity provisioning (responder matches the same eid net),
frame length/padding (byte-exact + flood-interleave sim replays PASS),
seed dependence, synthesis pruning (1091 LUTs), RESPOND_S wedge
(milanfinal10 watchdog: WEDGE=0 while deaf). Sim CANNOT reproduce
except zero-gap back-to-back frames ([STORM] loss - real but the
quiet-network silicon test also failed, so not the whole story).
Morning CC=84 on arty-8 is best explained as Hive retry persistence
over hours, i.e. the loss has likely been chronic; the walkers sample
bare tvalid (no tready qualify - OK only if rx_axis_to_dma never
stalls; aecp shares the pattern and works). NEXT: milanfinal11 (in
flight) adds ACMPL_DBG 0x6E8 RO-live {classify_cnt, fc_cnt,
fc_flags{dst,etype,sv0,len,ovfl,lstnr_hi,lstnr_lo,is_cmd}, base_hits}
- one read after a poke says whether the walker classifies frames at
all and which accept term fails. Watchdog (b8e4613) + forensics
(c0360bb) both ride it. Audio is DOWN until a bind lands (AX streams
true 48k regardless; arty QSPI currently milanfinal10-asl).

**EVENING TASK RUN (07-18 late):** MAAP ENABLED ON SILICON: AX probe->
announce->claim in 8 s, address 91:E0:F0:00:D7:97 (offset 0xD797, 0
conflicts), GET_STREAM_INFO reports it, STREAM MIGRATED MID-FLIGHT with
zero listener interruption (sid-filtered) - left ON. Enumeration drill
41/41 BOTH entities. Counters healthy (FRAMES 8000/s exact, 0 mismatch).
LATE_TIMESTAMP fully explained: counts because no clock sync exists; the
switch WILL NOT relay 802.1AS announces (single-claimant recipe retried:
AX 100/cc6 claims, arty clientOnly, pw0 test slave - NOBODY receives
announces; switch sends only pdelay_req). Stream-PHC-sync stopgap (shell
loop vs avtp_ts) got LATE=+0 but oscillates vs the 12 ms accept window
(process-spawn noise ~30 ms) -> proper fix = ts_delta CSR 0x6EC
(HW-latched signed avtp_ts-now at each accepted PDU) riding milanfinal13.
**SRP BREAKTHROUGH FINDING: the switch's MSRP Domain declares SR class A
prio 3 on VID 0x27E = 638 (NOT VLAN 2!)** - the VLAN-2 assumption dates
to the MVP and explains BOTH the historical tagged-VID2 ingress filtering
AND every TalkerFailed degradation. Tagged-638 streaming attempt: AX
streams 8.8k fr/s tagged, switch still does NOT forward to the arty
(MVRP join for 638 not registering - switch registrar shows bare
LeaveAll; lwSRP re-arm cycle didn't help). lwSRP-vs-switch session now
has a concrete agenda: (1) MVRP join encoding vs this switch, (2) then
MSRP TA in-domain on 638, (3) then reservation -> SETTLED_RSV_OK.
Audio restored on untagged bypass after the experiment.
**Playback P-servo (508bbca, in milanfinal13):** SET_CLOCK_SOURCE(stream)
on mf12 silicon engaged the servo (rule works!) but the integrator
LIMIT-CYCLED (+-480 trim, lock flap 2/s) - no damping once the big offset
was gone; P-control trim=4*(fill-mid) is self-damping. Internal/free-run
unaffected (still the default).

**MILANFINAL13 CLOSE-OUT (07-18 night):** arty keeper = **eto_milanfinal13
(+0.187, session-best) QSPI**. Silicon-verified in one pass: bind SUCCESS
(controller+walker fixes), **ts_delta CSR 0x6EC live** -> stream_phc_sync
v2 rides it: **LATE +0 / EARLY +0 / FRAMES 8000/s exact / UNCERTAIN +0**
(the whole timestamp story closed; real 802.1AS stays switch-blocked).
**P-servo converged flat: trim -8 LSB (~-12 ppm = crystal delta), fill
pinned 254-257, zero limit cycle** - the arty now runs CLOCK SOURCE =
STREAM (exact media-clock recovery, SET_CLOCK_SOURCE(1)); the external
media-lock convergence rule verified live. Daemons persisted in the
the-private-test-repo rootfs overlay (ramfs deploys still needed until the
next image flash). AX milanfinal12 parity sweep in flight (P-servo +
ts_delta + responder hardening; AX bench roles unaffected meanwhile).

**gPTP FINAL EVIDENCE (07-18 night, certified-switch session):** the
boards are CORRECT 802.1AS participants - the AX answers the switch's
pdelay_req with HW-timestamped responses (frame-verified), masters/
announces/syncs properly when claiming, and runs clean clientOnly
slaves. THE SWITCH withholds announce relay in its current state: the
ONLY relay ever observed was a ~1-minute window right after the pw0
i210 started claiming (4 announces reached the arty, capture-proven);
never again - not after a clean switch power-cycle with a single stable
claimant, not with SW vs HW timestamps, not from board ports vs pw0's
port. The switch also never announces its own GM into any observed port
(pdelay_req only, forever). A certified bridge doing this = its own
gPTP/management configuration (per-port 802.1AS enable, GM policy -
possibly reset by today's power cycles). NEXT ACTION = the switch's
management UI (user). Meanwhile the timestamp deliverable is COMPLETE
via stream-sync (ts_delta 0x6EC): LATE/EARLY exactly 0 sustained, GM
published, media clocks servo-locked.
**AX keeper = eppo_milanfinal12 (+0.031) JTAG-SRAM** (P-servo + ts_delta
+ responder hardening parity); pair re-verified: bind SUCCESS, 8.7k fr/s,
fill mid-pinned. MAAP re-enabled on the fresh boot (re-claims an offset
each boot until NV persistence lands in S50milan).

**TASK LIST COMPLETE (07-18 night): PIPEWIRE CONSUMER LIVE.** Formal
ring acceptance: pcm_ring_dump on the pcmring DT reservation
(0x4FF00000/1 MiB, no-map) -> **THD+N -134.4 dB PASS** (limit -120;
level -15.1 dBFS with the -12 dB attenuator). `pw-milan-ring-source`
(fpga/pipewire/, overlay /usr/bin) = PipeWire Audio/Source mapping the
ring + chasing the DMA offset CSR: with wireplumber (now in the image)
the graph auto-links and samples flow at EXACTLY 48,000 words/s,
under=0. Bring-up (manual until S-scripts land): XDG_RUNTIME_DIR=/tmp/pw
pipewire & wireplumber & pw-milan-ring-source & pw-loopback
--capture-props='node.target=milan-aaf-capture' &.
**Image-cycle traps burned:** (1) generic fw_jump.bin WEDGES the boot -
the custom litex_nax opensbi EMBEDS the dtb (rebuild build_opensbi.sh
with DTB=<new> for any dts change; the dtb flash slot is decorative);
(2) `make defconfig` CLOBBERS the accumulated .config (pipewire was
interactively enabled and never saved - now durable in the defconfig
with wireplumber+lua5.4); (3) buildroot may leave rootfs.cpio.xz STALE
after an incremental rebuild - regenerate manually (`xz -9
--check=crc32`, crc32 REQUIRED by the BIOS xz_embedded decoder) and
size-check vs the 8.5 MiB rootfs slot budget; (4) `pw-cli load-module`
modules die with the pw-cli process - use pw-loopback / conf drop-ins.

**CLEAN AUDIO CLOCK (07-18 night, milanfinal14/15):** the fractional-N
divider chain put +-1-sys-cycle (~10 ns) edge jitter on MCLK - the
CS4344/CS5343 delta-sigma cores tolerate ~ps: measured analog THD+N
-4.5 dB (H3 -7.7 dBc) at ANY level. Fix rev A (mf14, asl **+0.399** -
session-best timing since the serializer left the 50 MHz domain): MMCM
cd_audio 24.576 MHz (S7MMCM fractional, margin 1e-3) + player serializer
in-domain with registered dividers /2 /8 /512 + cdc_pair_fifo (gray
CDC). Re-measure came back IDENTICAL -4.6 dB -> **the loopback's ADC leg
(aaf_talker_i2s I2S masters, still NCO-jittered) was the measuring
instrument AND the distorter** - the post-fix DAC may already be clean.
Fix rev B (mf15, in flight): talker/tone front-ends also in cd_audio,
pairs cross via cdc_pair_fifo, KL_media_adv retired. S99milan-audio
boots the whole stack (verified: pipewire+wireplumber+ring-source+
phc-sync all self-start). LESSON (measure-don't-assume corollary):
when a fix measures identical, ask whether the INSTRUMENT shares the
defect - here both legs of the loop had the same clock pathology.

**ANALOG LOOP INVESTIGATION (07-18 late night, still open):** with both
converters clean-clocked (mf15, eto +0.484 project-best) and JP1
confirmed SLV, the loop STILL measures the same square: plateaus at
~0.3 FS, H3 -7.7 dBc, identical to 0.1 dB across three clock
architectures, a cable swap, AND source level (-12 vs -24 dB source =
SAME amplitude -> LEVEL-INDEPENDENT). Facts: ring/PCM data -134 dB
clean; capture->framer digital path -132.8 dB clean (tone inject);
L/R identical (corr 1.0000); ADC noise floor healthy when unplugged;
both serializer generations sim bit-exact yet show the same silicon
signature. Standing model: the CS4344 receives ~only the sign bit
(sign(sine) x const = level-independent square). Discriminators in
flight: I2SPB_DBG CSR 0x6F0 (mf16) captures the exact 32 serial bits
at the DAC pin per LEFT half-frame; user ear/phone-spectrum check
(buzzy square vs pure sine) at the line-out.

**DEEP SILICON BATTERY (07-18 late, both entities on final keepers):**
first-ever silicon verification of: **GET_DYNAMIC_INFO 0x4B** (SUCCESS
cdl 124 both), CLOCK_DOMAIN counters (mask 0x3, locked counting),
full **DISCONNECT -> count 0 -> CONNECT -> count 1** ladder, **MAAP
DEFEND** (probed the live claim: defends counter 0->1, address HELD -
the announce-state defend per the reference), **unsolicited replay**
(controller A registered, controller B's SET_NAME arrived at A with
u=1 - the 4-slot engine live), GET_AUDIO_MAP (cdl 88 both;
ADD/REMOVE = NOT_SUPPORTED by design). Command-code traps recorded in
the-private-test-repo fpga/tests/silicon_battery.py (audio maps are
0x2B/0x2C/0x2D desc 0x000E; rx-state count at resp[60:62]; MAAP
re-claims per boot). ONE cosmetic gap found: GET_RX_STATE returns a
ZEROED stream_dest_mac (should echo the bound MAAP address) - minor,
listed for the next RTL batch.

**AUDIO DEFECT CLOSED (07-18 night, milanfinal17):** the analog-loop
level-independent sign-square was a DOUBLE Philips delay in the rewritten
serializer (explicit pad slot + the output-register pipeline both delaying
one slot -> the chip's MSB slot always read 0 and our sign bit sat at
magnitude weight 2^22). Fix 78bbabe. Silicon: loop THD+N **-4.5 dB ->
-69.9 dB** (harmonics all <= -90 dBc, remainder = converter noise at
-20 dBFS = physics), level now tracks linearly (0.25->0.14, 0.0625->0.035).
Forensic chain in memory (i2s-sign-square-rootcause). TB gap fixed: both
chip-model decoders were double-delayed too + the async TB now strict-ramp.
**Arty QSPI keeper = build_arty_eto_milanfinal17 (+0.132).** asl/eppo seeds
died only at write_cfgmem (SPI_BUSWIDTH quirk, bitfiles routed fine).
EAR CHECK still owed from the user (loop measures clean; a listen is the
final human acceptance).

**lwSRP UNBLOCKED (07-18 night):** the switch's MSRP Domain declares SR
class A **VID 638** (0x27E); our VID CSR held 2 -> nothing ever matched.
With 0x684=0x27E + 0x680=0xF on BOTH boards: talker_declared+domain_ok on
both, and the AX registrar saw a **Listener Ready arrive through the
switch** (first cross-switch MSRP attribute propagation ever on this bench).
res_active still 0 (reservation completion = next session's thread).
S50milan now writes both CSRs at boot (the-private-test-repo 9a21ff6).

**GET_RX_STATE dest_mac now echoed** (3136b7e, lstn 103 checks): rides the
AX13 parity sweep; the arty picks it up next round.

**silicon_battery.py is executable** (the-private-test-repo 3dd10db): 25 checks
green against the live pair from pw0, incl. the spoofed-second-controller
unsolicited replay. GET_COUNTERS mask offset trap: counters_valid at
resp[42:46] (38/40 are desc type/index).

**lwSRP end-to-end diagnosis COMPLETE (07-18 late):** with VID 638 the
switch ACCEPTS both boards' TalkerAdvertise (re-declares both streams at
pw0's port as TalkerFailed code 8 - correct there, pw0 runs no MSRP) and
relays Listener declarations both ways. The arty's walker silicon-registers
the TF code 8 for its bound stream (visible at 0x6A4 bit7; the exact
switch PDU replayed through KL_lwsrp_rx in tb/verilator/lwsrp_switchpdu
parses bit-perfectly, TA variant too). Code 8 = "egress not AVB capable":
the switch never relays Sync/Announce INTO board ports (the known
management gap), so the boards can't be time-synced and the switch is
CORRECT to fail the reservation. => Our SRP fabric is done and proven;
res_active/SETTLED_RSV_OK unlocks with the SAME switch-management visit
that unblocks 802.1AS relay (per-port gPTP/SR-domain enable in the d&b UI).

**AX PARITY DONE (07-18 night): keeper = eppo_milanfinal14 (+0.101, SRAM
via JTAG - volatile as always).** Carries everything mf13-17 + dmac echo +
the audio MMCM. Port trap fixed on the way: register_clkin of the audio
MMCM on the AX's differential clk200 = a second IBUFDS = Place 30-475; AX
now cascades from the buffered sys clock (5eed747). Silicon: battery 25/25
vs the pair, source tone -127.1 dB digital, arty loop -69.0 dB, and
**GET_RX_STATE dest_mac echo verified on silicon** (91e0f000fe01 on an
AX-listener bind; bench unbound after). TRAP: the AX's QSPI rootfs carries
a STALE S50milan (writes 0x654=0x00020002 = VID-2 + probe-gate -> the
talker is silent after every reboot; manual `devmem 0x90000654 32 0x3`
revives; durable fix = reflash the AX kernel/rootfs partitions with the
current overlay - allowed, only BITSTREAM is banned from AX QSPI).
REFLASH CAVEAT (07-19 00:30): the AX's LIVE fdt md5 (609972b7...) matches
NO dtb on disk (milan_ax7101_linux/milan_100mhz/milan.dtb all differ) -
the staged opensbi embeds an unidentified DTB variant. flash-images
rewrites ALL manifest slots, so a naive reflash risks a wrong dtb/opensbi
pairing. Kernel identity IS confirmed (#15 Jul 6 = br-milan-output Image).
Before reflashing: either dump the staged dtb slot for comparison or
rebuild opensbi+dtb for the AX from source with known params. New rootfs
(lwSRP writes, 8.58 MiB, fits) is ready at /tmp/scratch/rootfs.cpio.xz. Arty
next round should pick up 3136b7e for its own dmac echo.

**FINAL PAIR (07-19 ~01:00): Arty QSPI = eppo_milanfinal18 (+0.322) +
NEW rootfs / AX SRAM = eppo_milanfinal14 (+0.101).** mf18 verified on
silicon: battery 25/25, **BOTH boards now echo stream_dest_mac**
(arty: 91e0f000fe01), loop THD+N -69.7 dB, audio stack self-starts, and
**lwSRP boots enabled on VID 638 from S50milan with zero manual steps**
(0x684=0x27E, 0x680=0xF at power-on). The arty side is fully durable;
only the AX's stale rootfs (see reflash caveat below) still needs its
0x654 revive after reboots.

**PROFISHARK GROUND TRUTH (07-19 early, user-directed) - MAJOR
CORRECTIONS + 3 real bugs fixed.** Tap host amx-ubuntu-server
(ubuntu-profitaps): tap1 inline on the AX<->switch link (tap2 powered
but NOT inline - candidate for the arty link). Strict per-link dissection
(fpga/tools/srp_qna.py in the-private-test-repo + tshark) OVERTURNS 07-18:

1. **The SR VID is 2** (switch Domain = classes B{5,2,2}+A NoV=2 vector;
   Milan default - the user called it). "638" was the switch's MVRP VLAN
   declaration misparsed as the Domain. Our Domain now {A,3,2} and the
   switch's class-A value flips to JoinIn = registered match. The 07-18
   "VID-638 breakthrough" was a confounder (the same command also flipped
   lwSRP CTRL from its disabled boot default).
2. **TalkerFailed root cause #1 was OURS: code 5** (dest address in use)
   - both talkers declared+streamed the same static DMAC
   91:E0:F0:00:FE:01. Fixed: MAAP enabled both boards; S50milan
   milan_maap_adopt polls the claim (0x6D4==6) and copies
   91:E0:F0:00:<0x6D0[15:0]> into the lwSRP dest-MAC CSRs 0x688/68C.
   Code 5 VANISHED on the wire immediately after.
3. **Bug #2 was OURS: rogue gPTP GM** - stale gptp.cfg (gmCapable 1, no
   clientOnly) had the AX mastering Announce+Sync INTO the switch (and
   polluting every earlier "relay alive" observation - pw0's morning
   Syncs were its own TX). Both boards now clientOnly (RAM + overlay).
4. Remaining failure both directions: **code 8** (egress not AVB
   capable), now proven clean-room: pdelay healthy 1/s both ways, no
   rogue master, Domain matched - and the switch sends ZERO
   Sync/Announce into board ports. The 802.1AS-per-port management
   setting is the single remaining unlock for SETTLED_RSV_OK.
5. Our MRPDU encodings validate byte-clean (strict 802.1Q walk incl.
   Listener 3+4-pack); Listener attach propagates (re-declared
   AskingFailed pending TF-8). **OUR lwSRP fixes for the next RTL
   round:** (a) domain_ok is too lenient - it reported OK against
   {B,2,2} vs our {A,3,638}; needs strict {class,prio,vid} compare;
   (b) the applicant re-declares every join tick (5.4 Hz spam - should
   quiesce per MRP and re-declare on LeaveAll/state change only).
6. Switch behavior notes: echoes the registered TA back to its talker
   (event In), strips VID-0 priority tags on egress (arty stream arrives
   untagged at the AX - NOT a talker bug).

Arty reflashed with all of it (same eppo-mf18 gateware): boots VID 2,
MAAP claim auto-adopted (fresh random claim each boot), clientOnly,
battery 25/25, loop clean. AX carries the same fixes in RAM only (stale
rootfs; reflash still gated on the dtb-identity caveat below).

**KERNEL-SHIELD ROUND (07-19 morning): the pdelay starvation root cause
and the architectural fix.** The 35% pdelay response rate was NOT
scheduling (SCHED_FIFO changed nothing) - the arty's allmulti (the kl-eth
mc-filter workaround) feeds the FULL 16 kfps AVTP flood into the 1-hart
kernel (55k RX drops); the lightly-loaded AX (stale rootfs, no allmulti)
answers 97%. Fix chain in 670a888:
  1. The AVTP monitor + AAF depacketizer taps moved PRE-filter (the media
     path must not depend on the kernel's dest-MAC filter config).
  2. rx_mac_filter grew a RUNT GUARD (a 1-beat frame is never legal;
     upstream re-present warts at drop tails minted ghosts in the dp TB).
  3. CSR VERSION bumped to 0x0004 = "pre-filter taps present"; S50milan
     (the-private-test-repo 234d32f) arms a TCAM drop entry for 91:E0:F0::/24
     on the CPU DMA path ONLY when VERSION >= 4 (on older gateware the
     drop would starve playback - the gate matters).
TB debugging traps burned this round (all in dp sim_main): post-edge
sampling counts upstream re-presents and MISSES single-cycle final beats
(sample PRE-edge: lo(); read; hi()); Verilator interface-instance
pointers (__PVT__*_axi_stream_if) are ALIASED-DEAD storage - reads are
garbage (flattened rx_filter__DOT__* internals are real); printf'ing a
VlUnpacked array misaligns ALL later varargs; --strip-probes builds have
no MilanDebug counters. mkaaf's 2nd arg = NSR nibble (0x05 = 48k!).
Wrong-rate section checks are now DELTA-based. milanfinal20 sweep carries
the round (fallback keeper: mf19 eto +0.448 = lwSRP fixes only).

**MF20 VALIDATED END-TO-END (07-19 morning, la_avdecc + taps): Arty QSPI
keeper = eto_milanfinal20 (+0.366) + shield rootfs.** Full checklist:
  - pdelay: **100% (62/62)** after the kernel shield (mask corrected to
    /32: /24 also covered the AVDECC multicast 91:E0:F0:01 and the fabric
    ACMP taps sit post-filter - connect timed out 997 until narrowed) +
    the ptp4l S65 trap (the initscript prepends /usr/sbin to $DAEMON -
    an absolute DAEMON path = silent dead daemon; bare name now).
  - ATDECC via la_avdecc 4.3.1 (pw0 ~/la_avdecc_work/stream-probe):
    both entities Milan=1/Misbehaving=0, library connectStream SUCCESS,
    listener model state=Connected. THE PROBE NOW SETS THE FORMAT FIRST
    (Hive flow): the AEM default STREAM_INPUT format is EIGHT-channel -
    a pure-ACMP connect on a fresh boot rejects the 2ch wire as
    UNSUPPORTED_FORMAT (4.2M rejects observed). My old controller's
    --bind always set 2ch first, masking this since forever. RTL
    FOLLOW-UP: default the AEM current format to talker-truth 2ch
    (0x0205022000806000).
  - Counters (la_avdecc, cached from our 1 Hz unsolicited push):
    listener MediaLocked=1, ClockDomain Locked=1, FRAMES_RX 1M+ @8k/s,
    LATE_TIMESTAMP froze at 51,006 (format-set convergence window only;
    servo at +6.35 ms on target), UNSUPPORTED frozen historical,
    GmChanged=2 (the clientOnly restarts). Talker FramesTx 287M+.
  - Audio loop -66.6 dB THD+N through the pre-filter/shielded
    architecture (media path proven independent of the kernel filter).
  - **Switch restarted per user (powerstrip OUT4): behavior UNCHANGED** -
    still zero Announce/Sync into board ports and TF code 8 on the peer
    stream, deterministic across a fresh boot => config, not a wedge.
    The per-port 802.1AS/AVB management setting remains the unlock.
  - OPEN: the arty's MVRP frames STILL never reach the wire (the
    back-to-back gap fix did NOT cure it - eater unfound, engine
    tx_count counts them); MSRP cadence 80/60 s (above the ~18 quiesce
    target: rx_leaveall + lstn_ready-flap re-arms suspected).
  - Console trap: a foreground pipe on the serial console (ptp4l | head
    without timeout) wedges the shell EATING all subsequent commands as
    its stdin - recover with ctrl-C via the console daemon's _in pipe.

**FINISH-EVERYTHING ROUND (07-19 midday):**
  - AEM default STREAM_INPUT format = talker-truth 2ch now (2f09bda:
    FORMATS[0] in gen_aem_store.py + regen; a pure-ACMP la_avdecc connect
    works against a fresh boot without SET_STREAM_FORMAT).
  - **MVRP eater LOCALIZED + WORKED AROUND**: the dp TB's lwsrp-egress
    test proves the MSRP+MVRP pair reaches the MAC port intact => the
    eater is the arty's MAC path when frame 2 enters within one
    100 Mbit serialization (~6 us) of frame 1 (GbE AX unaffected; MAAP
    singles never bitten). lwSRP gap 64 -> 1024 cycles (20 us) clears
    it; REAL FIX OWED: MilanMAC back-to-back TB. MSRP cadence note
    corrected: ~1.3/s = the intended 1 s refresh + LeaveAll traffic,
    working as designed.
  - **AX stale-rootfs era ENDED**: staged flash images identified by
    read-back (dtb slot = milan_ax7101_linux.dtb, opensbi slot =
    opensbi.bin, kernel = #15) => provably-safe images reflash with the
    new rootfs. S50milan sed-debris cleaned: the AX section was MISSING
    0x654/maap_adopt/kernel_shield entirely (+ arty duplicate call);
    now: AX boots turnkey (entity, talker 0x654=3, tone -12 dB, VID 2,
    MAAP claim adopted, shield, clientOnly ptp4l-rt). TRAP: flash-images
    loads the JTAG SPI-proxy = the running SRAM gateware is CLOBBERED -
    always JTAG-reload after an AX flash op.
  - Both boards on VERSION 0x0004 gateware: arty QSPI eto_milanfinal20
    (+0.366); AX SRAM eto_milanfinal15 (+0.099, asl +0.108 banked, eppo
    pending). Validated: la_avdecc SET_FORMAT+CONNECT SUCCESS, both
    Milan=1, connection state=2, pdelay 100% cold-boot, audio
    -126.2 dig / -69.3 loop on fresh MAAP DMACs both sides.
  - PENDING AT HANDOVER-TIME: arty milanfinal21 sweep (2ch default +
    gap-1024; launches when the AX sweep frees Vivado) -> flash with the
    124961b rootfs; AX images-reflash once more for the tone line +
    JTAG the best seed; then the MVRP-on-wire check (gap fix's silicon
    proof) via the tap.

**EVERYTHING FINISHED (07-19 afternoon). FINAL PAIR: Arty QSPI =
eppo_milanfinal21 (+0.233) / AX SRAM = asl_milanfinal15 (+0.108), both
VERSION 0x0004 with the 0f54f67 rootfs.** Cold-boot to full bench with
ZERO manual steps on both boards (entity, talker 0x654=3, AX tone -12,
VID 2, MAAP claim adopted into SRP dmac, kernel shield /32, clientOnly
RT ptp4l, audio stack). Cold-boot validation: la_avdecc SET_FORMAT(no-op
now, 2ch default)+CONNECT SUCCESS state=2, pdelay 69/69=100%, **MVRP
SILICON-PROVEN on the wire (84/60s paired with MSRP 82 - the gap-1024
fix works)**, audio -126.2 digital / -66.9 loop. Remaining truly-open:
(1) the switch management UI visit (announce/sync into board ports ->
reservations complete; restart proven ineffective = config); (2)
MilanMAC back-to-back TB (the gap workaround stands); (3) user
ear-check of the loop. AX flash images now fully identified+safe
(kernel #15 / opensbi.bin / milan_ax7101_linux.dtb + rootfs slot);
remember: ANY AX flash op clobbers the SRAM gateware - JTAG after.

**======= THE SRP UNLOCK (07-19 afternoon) =======**
The user was right on both counts ("the switch is by default MSRP correct
and AVB certified" + "MSRP Failure in Hive"): EVERY historical SRP/gPTP
failure against the switch was OUR pdelay timestamp reference. kl-eth RX
stamps are late vs the wire (**arty 3511 ns @100M, AX 1490 ns @GbE**,
ProfiShark-measured via tap-turnaround minus our t3-t2; profitap u64 ts
unit = ns*2^32!). The offset/2 lands in the switch's computed neighbor
delay > the 802.1AS 800 ns threshold -> asCapable never true -> the
CORRECT bridge neither relays 802.1AS nor admits reservations (TF code 8).
Direct-cable board-to-board always canceled the offset - the entire
"switch withholds gPTP / management-UI visit needed" thread is RETRACTED.
FIX (5b6478d): per-board linuxptp ingressLatency (S50milan seds it into
gptp.cfg pre-S65) + **the AX is the bench GRANDMASTER** (clientOnly
removed there only; pw0's SW-ts claimant never qualified and is now
retired). RESULT within a minute: first-ever Announce+Sync relay into the
arty port, arty ta_registered/SETTLED_RSV_OK, **AX res_active=1 + CBS
slope engaged + stream gate open = the complete Milan SRP reservation**,
audio through the reserved path -70.4 dB (best loop yet). Hive's "MSRP
Failure" clears (ta_failed=0); the mf22 build additionally makes the
STREAM_INFO/AVB_INFO fields Milan-exact (real failure code/bridge when
one DOES exist, acc-lat/vlan from the registered attr, msrp_mappings,
AS_CAPABLE).

**STRESS ROUND (07-19 evening, user-directed: bind/unbind cycles + REAL
switch power-kill recoveries + per-phase Milan counter analysis).**
Sequence: baseline / bind+settle / 5x rapid rebind / clean unbind /
bind + 2x switch power cycles (powerstrip OUT4), counters snapshotted
per phase via GET_COUNTERS (fpga tools counters_dump.py on pw0, stress
driver in the session scratchpad).

CLEAN RESULTS: frame accounting EXACT (FramesTx == FramesRx 269,777 over
a bind window - zero loss); MediaLocked/Unlocked, CD Locked/Unlocked,
StreamStart/Stop all track events correctly; ZERO SeqNumMismatch /
UnsupportedFormat / EarlyTs through 5 rapid rebinds; the ARTY rode out
both switch outages (stream, servo, stack all resumed unaided);
post-outage the parked listener SM re-settles AUTOMATICALLY once the
talker's ADP returns (it waits on tk_avail - correct behavior).
Rebind->switch-registration ~100 ms on the tap; settle ~4 s.

DEFECTS FOUND (ranked):
 1. [CRITICAL] **AX MAC TX wedges PERMANENTLY on a link bounce** (RGMII
    path): every fabric+kernel TX frame silently eaten (engines count
    accepted frames, tap shows nothing; RX keeps working). ip-link
    bounce does NOT recover; only a JTAG gateware reload does. THIS also
    resets the datapath (counters/ACMP/ADP state to defaults) while the
    **area-70 CSR shadow BRAM keeps serving stale pre-reset values on
    reads - the CSR plane LIES after any fabric reset** (the MAAP claim
    even 'survives' because the LFSR reseeds identically). Next-session
    deep fix: LiteEth RGMII re-init / reset decoupling + a shadow-vs-live
    canary. Mitigation until then: JTAG reload after any link event on
    the AX.
 2. [MILAN] Listener rx counter group resets on rebind (FramesRx went
    negative across the phase) - Milan requires power-up-only clearing;
    make the exposed counters monotonic (the monitor's internal settle
    reset must not clear them).
 3. [GAP] The ARTY has no link tracking (fabric i_link_up=1, driver
    carrier static): LinkUp/LinkDown counters are decorative and no
    link-loss reactions occur (also why the arty is IMMUNE to defect 1).
 4. [RESIDUAL] fast-join LeaveAll-at-bind: sim-proven, but the mf23
    silicon rebind capture shows the prompt pair WITHOUT the LA bit
    (periodic LA at ~10 s did appear) - re-verify with an isolated
    capture; the settle is fast regardless.

**LINK/RECOVERY ROUND FIXED + SILICON-PROVEN (07-19 night).** Answering
"fix all issues... link up/down + early/late/gm":
 - **The AX MAC-TX wedge is FIXED (software-only recovery, NO JTAG).**
   Drill on AX-mf17: real switch power-cycle -> TX WEDGED (confirmed on
   the tap) -> wrote LINK_CTRL[1] MAC-sys-reset + phy_crg_reset + release
   -> **full traffic resumed** (40k stream + MSRP/MVRP/gPTP/AVTP), AX
   re-advertised, rebind OK, **reservation re-formed** (res_active +
   arty SETTLED_RSV_OK). The reset-epoch canary (0x720) stayed at 1 =
   PROOF the reinit recovered the MAC ONLY, not the datapath. Root cause
   was the LiteEthMACCore sys-side CDC halves keeping pointers across an
   eth-domain reset; MilanMAC now runs its sys side in cd_macsys
   (reinit-resettable). linkmon.sh automates the whole sequence on RX
   liveness loss.
 - **Link up/down**: LINK_CTRL[0] mirrors real link (RX-liveness; arty
   MII-PMOD MDIO reads float, measured - RX-liveness is wiring-free and
   measures reachability) -> AVB_INTERFACE LinkUp/LinkDown + ADP behavior.
 - **Shadow-lie canary**: RST_EPOCH 0x720 counts reset-releases in
   reset-immune flops (bitstream-init, no reset clause); linkmon
   re-runs S50 config if the fabric ever resets behind the config shadow.
 - BUG caught by this very work: LINK_CTRL 0x71C was NOT in the milan_csr
   plain-RW shadow set -> writes read back 0 -> linkmon's assertions were
   silent (321f0d7; mf25 carries it). The mac_reinit STROBE still worked
   (real register drives the fabric output; only READBACK was stale) -
   which is exactly why the manual drill above succeeded on mf17.
 - Milan "defect 2" (counter reset on rebind) RETRACTED: Table 5.6
   mandates the not-bound->bound reset; the code cites it; correct.

**ATDECC VERIFICATION via avdecc_l2 (tsn-stack Milan controller) + behave
(07-19 night).** Ran the the-private-test-repo behave BDD suite against OUR
bench (AX talker :01, arty listener :02) - added AVB_LISTENER_EID env
override (committed; was hardcoded to pw0). RESULTS:
 - **avdecc_l2 reads BOTH entities' stream_format cleanly and confirms
   Milan v1.2 Section 5.5.1.2 compatibility** (format_check: compatible,
   0205022000806000) - the 2ch-default fix validated through a THIRD
   independent controller. Against the switch it correctly REFUSES
   (format_unreadable) - proper Milan behavior.
 - avdecc_l2 ACMP CONNECT_RX -> SUCCESS + SETTLED_RSV_OK (clean runs).
 - **INTERMITTENT ACMP-response reliability [OPEN, real]**: avdecc_l2
   sometimes gets clean 4/4 SUCCESS, sometimes 12/12 timeout - state/
   timing dependent (observed after behave's SET_STREAM_FORMAT + while
   our milan_controller also had the listener bound; multi-controller
   or post-AECP-op state). Our own milan_controller.py is reliable.
   Suspect: CONNECT_RX_RESPONSE delayed past avdecc_l2's 5s under load
   (the response rides 5 low-rate arbiters + a probe round-trip to the
   busy AX talker), or a controller-exclusivity interaction. NEXT: latch
   an ACMP-response-emitted timestamp/counter to distinguish "listener
   never responded" from "responded too late"; the tx-grant watchdog
   (2^20 cyc) may be firing. NOT a framing bug (avdecc_l2 frames parse +
   sometimes succeed).
 - behave setup/audio scenarios assume pw0-as-listener+pipewire (not our
   arty-listener topology) - those failures are harness-topology, not DUT.
 Toolchain: SSH_PW0 wrapper + behave venv (numpy/scipy) + NTP-off guard
 (AVB_TESTS_SKIP_CLOCK_CHECK=1); recipe in the session notes.

**TRAFFIC-SHAPER / QoS VERIFIED under interference (07-19 night) +
Issue #1 (two-servo audio) CLOSED.** iperf3 best-effort flood (TCP 4-stream
+ UDP 900M) from the AX kernel through the MilanMAC egress, competing with
the AAF stream at the final mux, while measuring AAF integrity on the arty:
  - **AVB stream integrity PERFECT under max interference**: LateTs +0,
    EarlyTs +0, StreamInterrupted +0, SeqNumMismatch +0, ts_delta rock-
    steady at 1.9 ms. The reservation bw-gate + switch class-A priority
    protect the stream; best-effort never disturbs it.
  - Interference surfaced the two-servo audio degradation (arty loop
    -31.7 dB under old daemon): stream_phc_sync fighting linuxptp for the
    PHC jittered the DAC PLAYBACK clock (not the stream - :01 stayed
    -126 dB; only the arty's :02 loop degraded). ROOT CAUSE = the already-
    diagnosed two-servo fight; FIX (gm_locked gPTP-aware daemon) now
    FLASHED on mf25. Verified: portState SLAVE -> servo stands down,
    arty loop back to **-69.3 dB even under iperf flood**, AX source
    -125.3 dB. Note: CBS per-queue shaper (0x400+) is DISABLED (en=0) -
    the AAF uses the lwSRP reservation bw-gate, not the classifier CBS;
    per-queue CBS verification (multi-PCP kernel traffic) is a separate
    future item.
  - Measurement trap: pw0 tcpdump drops AAF packets while its NIC eats
    900M UDP -> apparent audio degradation in-capture; measure after the
    flood or on a clean tap.

**ACMP-TIMEOUT — RETRACTED CONCLUSION (see ★ CURRENT STATE at top).** The
07-20 solve: avdecc_l2's socket wasn't joined to the AVDECC multicast, so
pw0's NIC filter dropped the response the DUT DID send (that is exactly why
the forensics below always showed a clean 0xE07F settle). Fixed in the
controller (PACKET_MR_PROMISC) → 15/15. The "response-delivery timing/race"
text that follows is WRONG and kept only for history. --- Forensics 0x6E8/
0x6B0 across an avdecc_l2 timeout: the listener STILL processes the CONNECT_RX
every time - cmd_count +1, basehit +1, SM 0x8000 -> 0xE07F (SETTLED_RSV_OK),
probe emitted. The response IS generated; avdecc_l2 just doesn't receive/
match it in the timeout cases. RULED OUT: command rejection, tx-grant
watchdog (tx_wedge stable), format (5.5.1.2 passes). => response-delivery
timing/race (RESPOND-then-PROBE + low-rate TX arbiter latency), masked by
controller retry. FIX: latch a response-emit PHC-timestamp counter to
measure emit latency; consider emitting the response before arming the
probe.

**ISSUE-BY-ISSUE FIX ROUND (07-19 late night):**
 1. MilanMAC back-to-back frame EATER (root cause of BOTH the MVRP-pair
    loss AND the intermittent ACMP CONNECT_RX_RESPONSE timeout) - FIXED
    at the root: datapath-proved the eater is MAC-side (the merge emits
    both frames even at a 2-cycle gap), so added a control-lane min-IFG
    gasket (hdl/common/tx_ifg_gasket.sv, 512 cyc) that spaces every
    LOW-RATE control frame before the MilanMAC while leaving data/AAF
    throughput untouched. lwSRP's local gap 1024->8 (gasket generalizes).
    ifg TB + full regression green (mf26 building). Silicon verify owed:
    MVRP still on wire + ACMP reliability improved.
 2. Two-servo audio degradation (gm_locked daemon) - FIXED + flashed +
    verified (loop -69.3 under iperf flood).
 3. Arty GmChanged=0 on a GM bounce - gptp2csr poll 5s->2s (daemon
    already publishes gm=0 on gmPresent-false; it just polled too slowly
    to observe the ~8s transient). rootfs rebuilt.
 4. Full Verilator regression GREEN across all ~30 suites after the
    session's changes (aaf/acmp/acmp_lstn/aecp 432/lwsrp/maap/dp 89/
    ifg/shaper_core/cbs/ptp_ts/... all pass) + yosys 27/27.
 REMAINING (by design / user / future): per-queue CBS disabled (AAF uses
 the reservation bw-gate - correct for a single stream); ear-check;
 ACMP response race is masked by controller retry (real controllers).

**CERT MILAN ENDSTATION TEST-PLAN CAMPAIGN (07-19/20 night) - full
behave suite (cert_recreate) + tsn-gen protocol models, DUT = arty
listener :02.** Setup: harness copied to pw0 (~/cert-run), behave venv +
numpy/scipy/pyyaml, tsn-gen YAML models wired (AECP_YAML_DIR ->
~/cert-run/tsn-models/aecp, 20 models), AVB_LISTENER_EID override.
RESULTS:
  PASS: es-3.1 (entity_model_id - FIXED, was all-zeros), es-4.7
  (SET_NAME - was FAIL), es-4.8 (SAMPLING_RATE - was FAIL), es-4.9
  (CLOCK_SOURCE - was INCONCLUSIVE), es-4.10 (CONTROL/Identify - was
  INCONCLUSIVE). The four previously-FAIL/INCONCLUSIVE tests now PASS
  from the session's AECP work.
  FIXED, pending mf28 flash: es-2.1 (ADP DELAY state - random delay +
  coalescing), es-4.13 (GET_AVB_INFO NOT_IMPLEMENTED vs
  NO_SUCH_DESCRIPTOR).
  MODEL CHOICES (not DUT bugs): es-4.3 SET_CONFIGURATION to index 1 ->
  BAD_ARGUMENTS is CORRECT for our single-config entity (the reference
  Milan-EndStation-1 has 2 configs; adding a 2nd config is a design
  decision, not a conformance requirement); es-4.4 scenario 1 expects an
  8ch default STREAM_INPUT format but we default to 2ch (deliberate, so
  a pure-ACMP la_avdecc connect works - the 2ch talker match); 2/3 pass.
  es-4.5 SET_STREAM_INFO(talker) unsolicited: gated by STREAM_IS_RUNNING
  when a listener is bound (correct Milan behavior).
  ** THE BIG FIX - discovery reliability **: the session-long flaky
  discovery was linkmon using the lwSRP rx_pdu counter for RX-liveness,
  which STALLS when MRP goes quiet (unbind) -> false link-down ->
  needless eth_reinit -> DUT flickered offline. Switched to the kernel
  eth0 rx_packets counter (gPTP alone keeps it ticking): **5/5 discovery**.
  Plus the linkmon DEADLOCK fix (reinit on down, not just down->up - the
  MAC wedge stalls RX permanently with no up-transition to trigger
  recovery).

**CERT interpretation differences (NOT DUT bugs, documented decisions):**
es-4.12 dereg-under-lock PASSES; hive-get-counters 4/5 - the one miss is
GET_COUNTERS on ENTITY: CERT wants BAD_ARGUMENTS, but IEEE 1722.1-2021
7.4.42 allows SUCCESS + empty valid-mask for ENTITY with no counters, and
a real Hive field report drove our SUCCESS+empty-mask (KEPT - not changed;
the CERT expectation is a stricter reading). link-flap errors = harness
needs a controllable DUT link (can't flap the arty's from the runner).

**CERT CAMPAIGN FINAL TALLY (mf28, arty DUT :02):**
  FULLY PASS (7): es-3.1 (model_id), es-4.7 (SET_NAME), es-4.8
  (SAMPLING_RATE), es-4.9 (CLOCK_SOURCE), es-4.10 (CONTROL/Identify),
  es-4.12 (dereg-under-lock), es-4.13 (GET_AVB_INFO). Of these, 5 were
  FAIL/INCONCLUSIVE before this session.
  es-2.1 (ADP DELAY): 2/3 - DELAY state works (random delays 0.095-0.319s,
  coalesces 12->6); recalibrated to [200ms,870ms] for spread>0.3s +
  coalesce<=4 (mf29 building).
  es-4.3 (SET_CONFIGURATION): 3/5 - the misses are our single-config
  entity (SET config 1 -> BAD_ARGUMENTS is correct; reference has 2).
  es-4.4 (STREAM_FORMAT): 2/3 - default 2ch vs the test's expected 8ch
  (deliberate for pure-ACMP connect).
  Net: the DUT passes the Milan endstation AECP/ADP test plan bar the
  documented model choices (1 config, 2ch default) + the es-2.1 tuning.

**es-4.5 SET_STREAM_INFO unsolicited gap [OPEN, characterized]**: the
unsolicited trigger (KL_aecp_response_builder ~line 775) fires only on
ACMP state changes (talker_active/listener_observed XOR), NOT on the
SET_STREAM_INFO(ACC_LAT) write itself (pres_wr_p_o). So a SET_STREAM_INFO
does not notify other registered controllers. FIX DIRECTION: trigger
unsol_pend on pres_wr_p_o (excluding the issuing controller, like the
reference), or add SET_STREAM_INFO to is_replay_cmd (risk: the response-
rebuild path for the larger stream-info payload - needs a careful TB).
Deferred (not a functional bug - the SET works; unsolicited is a
polling-avoidance convenience).

**==== CERT CAMPAIGN COMPLETE (mf29, arty keeper) ==== **
Final: **23/24 CERT scenarios PASS** on mf29 (arty DUT :02). es-2.1 (ADP
DELAY) now FULLY PASSES after the [200ms,870ms] recalibration - bounded
random delays, spread>0.3s, burst coalesces to <=4. The single remaining
failure is es-4.4 scenario 1 (default STREAM_INPUT format 2ch vs the
test's expected 8ch = the deliberate pure-ACMP-connect choice, not a bug).
es-4.3 excluded from the tally (single-config entity, reference has 2).
ARTY KEEPER = build_arty_asl_milanfinal29 (+0.276) in QSPI + the full-fix
rootfs (rx_packets linkmon, gm_locked servo, entity_model_id, IFG gasket
gateware, ADP DELAY, es-4.13, MAAP adopt, kernel shield, clientOnly RT
ptp4l). All self-configuring from cold boot; discovery 5/5 stable.

**HIVE FIELD SESSION (07-20, user-driven) — three catches, all fixed:**
 1. protocolAdpdu.cpp:77 'cdl minimum 56, 0 advertised' = silicon_battery's
    ENTITY_DISCOVER built with cdl=0 (tool bug since day one; our fabric was
    lenient so it hid). Fixed to cdl=56.
 2. protocolAdpdu.cpp:77 'Not enough data in buffer' = MY cdl fix then
    shrank the pad 64->56, truncating the ADPDU by 8 bytes (64 was
    entity_id(8)+body(56)). Fixed back to 64; wire re-swept with a
    LENGTH-validating check this time: every ADPDU on the segment is the
    full 82 bytes with cdl 56 = Hive-safe.
 3. onGetEntityCountersResult 'values deemed bad' on :02 = my CERT-driven
    flip of ENTITY GET_COUNTERS to BAD_ARGUMENTS. Hive/la_avdecc treat
    entity counters as first-class (1722.1-2021 defines them) - REVERTED
    to SUCCESS + empty valid mask (the original field-proven behavior);
    the CERT recreation feature was the wrong reading and is fixed
    instead. Gateware carrying the revert: AX19-final (building) + arty
    mf33 (queued after) - until the arty flashes mf33, Hive still logs
    the entity-counters warning against :02.

**ALINX-as-DUT campaign (07-20):** CERT runner cloned for :01
(/tmp/runcert-alinx.sh + ax-linkflap.sh). AX18 tally: 36/39 - residuals
all fixed at HEAD: 2x nochg scenarios (AX18 predates nochg_q) + es-2.1
randomness spread (DELAY params were CYCLE-based: the 100 MHz AX halved
the wall-time range -> now scaled by MILAN_CLK_FREQ_HZ, d99fb5d). The
AX-flap quirk: phy_crg reset on the AX does not drop carrier cleanly -
RX dies AFTER the window (eth-domain desync) and linkmon's wedge path
recovers it unattended (~20 s, silicon-verified). ARTY remains 41/41.

**CERT MUST-PASS FIX ROUND (07-20) — per-fix ledger:**
 - es-4.4 STREAM_FORMAT: 8ch default RESTORED (matches the test) + the RX
   monitor now CHANNEL-ADAPTS (accepts wire 1..fmt channels; depacketizer was
   already data_len-driven) so a pure-ACMP 2ch connect still works under the
   8ch default. rxmon TB +[28] adaptation suite.
 - es-4.5 SET_STREAM_INFO: added to is_replay_cmd so the SET response replays
   u=1 to the OTHER controllers (removed the old GET-shaped pres_wr push that
   double-notified).
 - hive-get-counters: GET_COUNTERS(ENTITY) -> BAD_ARGUMENTS full-size (Milan
   defines no ENTITY counters; the 07-11 Hive report was about SIZE, kept).
 - es-4.3 SET_CONFIGURATION: out-of-range -> NO_SUCH_DESCRIPTOR (1722.1
   7.4.7.1, was BAD_ARGUMENTS); feature adapted to our single-config model
   (Milan mandates one current config; 2 configs was the reference DUT option).
 - link-flap: AVB_INTERFACE GET_COUNTERS UNSOLICITED push on link/GM edges
   (new pend3 path, Milan 5.4.5) + pend2/pend3 now cleared on DEREGISTER
   (pend2 dereg-clear was latently missing); behave flap step made pluggable
   (CERT_FLAP_CMD) + a real PHY-level flap helper (phy_crg_reset via the
   console) since the arty has no ssh; behave setup stops pipewire via
   systemctl --user (systemd was auto-restarting it).
 - Board names: entity_name overlay CSRs 0x724/0x728 -> "ARTY"/"ALINX".
 - Regression at HEAD: aecp 440, milan_dp 90, rxmon 75, adp 268, lwsrp
   37/445/96, ifg 4, yosys 27 - all green.

**Open (ranked):** (a) flash milanfinal9 both boards + re-drill (cadence
125,000 ns, servo converged, la_avdecc 41/41, Milan=1 CLEAN ×2);
(b) deploy gptp2csr.sh + ptp4l pair → GM/pdelay live (clears
LATE_TIMESTAMP too); (c) lwSRP TA-propagation vs switch (listener stuck
SETTLED_NO_RSV, ~3.6k re-probes logged); (d) PCM-ring formal THD+N
(reserved-memory rebuild); (e) MAAP enable + bind-follow flow.

## 0b. BENCH SESSION 2026-07-17 (milanfinal2 silicon) — results + open items

Both boards run `*_eppo_milanfinal2` (arty: QSPI bitstream@0 REFLASHED —
survives the serial-DTR reset; AX: JTAG-SRAM, volatile). Old 2-hart QSPI
images boot fine on the 1-hart gateware (cpu1 timeout, degraded-OK).

**PASSED on silicon:** CSR identity + all 11 new registers exact ·
**MAAP live**: probe→ANNOUNCE, claim 91:E0:F0:00:9F:60, byte-perfect
announces at pw0 through the switch (fe 03 / 08 1c / cadence 3.7-4.1 s) ·
la_avdecc-style controller drill **41/41** on the new AECP · **full ACMP
listener ladder**: BIND_RX → ADP discovery → PROBE_TX → SETTLED, bound
talker = AX EID, VLAN learned · MSRP dialogue live (both engines ~109 TX /
~730 RX MRPDUs with the switch).

**FINDING 1 (product bug, caught by the new counters on first exposure):**
`aaf_talker_i2s` emits 2-ch AAF while STREAM_OUTPUT advertises the 8-ch
format ⇒ the arty monitor rejects every PDU (UNSUPPORTED_FORMAT 0x6C0
counting, FRAMES_RX 0). Fix = task #23 (framer 8-ch zero-fill), then the
tone/ring/servo acceptance completes.

**FINDING 2 (lwSRP↔switch, needs a dedicated session):** with lwSRP enabled
both sides: domain OK both; AX TalkerAdvertise declared; **TA never
registers at the arty** (0x6A4[6]=0) ⇒ bound listener declares AskingFailed
⇒ switch propagates it back to AX (0x694=0x35: lstn-reg=1, decl=asking-
failed) ⇒ no reservation, gate closed. MRP is link-local — debug needs the
switch's own MSRP view (d&b tooling) or a direct-cable peer (pw0 mrpd).
Workaround in force for streaming drills: AAF bypass=1 + VID0 (0x654=0x3).

**✅ FINAL STATE 07-17 LATE: MILAN=1 CLEAN + AUDIO LOCKED.** la_avdecc
verdict CLEAN rc=0 complaints=0 (both entities; clock-domain counters in).
Acceptance drill on milanfinal8/milanfinal7: rate nominal, servo CONVERGED
(trim +248 ≈ +0.76 % steady-state inter-board rate residual, fill
mid-range), ZERO overruns/underruns since lock, ZERO stream errors.
KEEPERS: arty asl_milanfinal8 +0.189 (QSPI-flashed), AX asl_milanfinal7
+0.040 (JTAG-SRAM). Remaining niceties: ring-dump THD+N measurement
(needs the 1-hart image/reserved-mem rebuild), lwSRP TA-propagation
session, arty/AX keeper re-unification on one tag.

**🔊 AUDIO E2E ON SILICON (07-17, after the OUT4 switch power-cycle):**
AX tone talker → switch → arty listener: **FRAMES_RX 376k PDUs / 46 s,
locked once and stayed locked, ZERO seq/format errors, PCM ring
committing, I2S serializing on the jack.** Adaptive 2-ch SET verified on
hardware. **Servo finding:** trim PEGGED at +80 (≈+1200 ppm clamp) with
fill riding the top rail (509/512) — the talker's media clock outruns the
arty's local 48 kHz by MORE than the clamp; widen the trim range
(KL_i2s_playback ±80 localparam) and/or quantify via 0x6D8 overrun rate
next session. Bench traps: the AX POWER outlet = powerstrip OUT0 (cut it
once — JTAG-SRAM lost, reload needed); switch = OUT4; AX serial login
resets provisioning after each reboot (0x654/0x6DC re-poke needed).

**SILICON FINDS 4+5 (audio-rate arc):** `d05546a` the AX framer's I2S
divider was fixed for 50 MHz — at 100 MHz it sampled 97.7 kHz while
advertising 48 k (measured 16.9k fr/s; servo pegged at BOTH clamps
chasing a 2× stream); dividers now scale with MILAN_CLK_FREQ_HZ.
`9d213a1` the playback NCO's 0x10000 nominal step carried EVERY cycle —
the divider could slow but never exceed nominal, so positive trim was a
no-op and a high FIFO could never drain; now 0x8000 half-rate nominal,
trim ±1.56 % both directions. AX keeper = asl_milanfinal7 +0.040
(rate fix); arty milanfinal8 (NCO fix) = the final acceptance build.

**FIELD FIXES from the user's Hive/la_avdecc session (post-drill):**
`a387e6b` AUDIO_CLUSTER 90→87 B (stray aes3_* tail; la_avdecc "Remaining
bytes: 3" — invisible to our TBs since the generator is their oracle) ·
`651fd4b` ACMP sink 1 (CRF) now valid-always-unbound on GET_RX_STATE
(UNKNOWN_ID for an ADVERTISED sink = la_avdecc Fatal Enumeration Error;
sink-0 state masked out of sink-1 replies) · `c6fc7c8` adaptive listener
formats (1..8ch on the base rates — the 2ch-talker rejection was correct
counting, the GAP was no way to adapt). ALL THREE ride milanfinal4
(arty sweep in flight; AX needs the same build after — its 41/41 drill
doesn't exercise these paths, Hive does).

**Bench traps:** arty serial-open DTR = board reset (QSPI reconfigures —
JTAG-SRAM images do not survive; hence the bitstream reflash); use the
persistent console daemons (scratchpad con.sh) + `dmesg -n 1`.

## 1. Topology

```
┌──────────────── dev VM (this machine) ──────────────────────────┐
│ repos + Vivado + buildroot + build tree (see §2)                │
│                                                                 │
│ USB passthrough (BY-ID ONLY, numbers shuffle on every replug):  │
│  FT232H  210512180081 = AX7101 JTAG                             │
│  CP2102N 66e0ce96...  = AX7101 console (115200)                 │
│  FT2232  210319AFEED0 = Arty JTAG (if00) + console (if01)       │
└──────┬──────────────────┬───────────────────────────────────────┘
       │ JTAG+serial      │ JTAG+serial          (VM has NO data
       ▼                  ▼                       plane; mgmt ssh
┌──────────────┐   ┌──────────────┐               to amx-pw0 only)
│ AX7101       │   │ Arty A7-100  │
│ full endstn  │   │ small endstn │
│ EID ...:01   │   │ EID ...:02   │
│ 192.168.127.1│   │ .3           │
│ 1G GMII      │   │ 100M MII     │
└──────┬───────┘   └──────┬───────┘
       │ 1G               │ 100M
     ┌─▼──────────────────▼─┐   d&b audiotechnik AVB switch
     │      AVB SWITCH      │   (OUI 3c:c0:c6, clock 3cc0c6.fffe.fe0210)
     └──────────┬───────────┘   remote power-cycle via amx-pi
                │ 1G (uplink = the only full-control-plane port)
        ┌───────▼──────┐
        │ amx-pw0 i210 │  192.168.127.2  enp6s0  68:05:ca:95:b2:d1
        │ (ssh, sudo)  │  controller drills + la_avdecc live here
        └──────────────┘
```

- **amx-pw1 is RESERVED — never touch it.** The VM never gets a
  192.168.127.x address.
- Entities: AX EID `02:00:00:ff:fe:00:00:01` (MAC 02:00:00:00:00:01),
  Arty EID `...:02` (MAC ...:02). stream_id = {station_mac, uid16} —
  byte-identical across ACMP/AECP/AVTP by construction (bug fixed 07-14).
- Switch behavior is DEFINITIVE (docs/findings/GPTP_RXPAD_ROOTCAUSE.md):
  edge ports are GM-source+pdelay BY DESIGN — boards never receive
  Sync/Announce through it; board-as-slave = direct cable only. Relay recipe
  = exactly ONE strong GM claimant (port 8, prio1 100, cc6). It forwards only
  registered AVB multicast between edge ports and INGRESS-FILTERS VLAN 2
  (hence the VID0 priority-tag policy until lwSRP/MVRP registers VLANs).
- A second session may drive the bench concurrently (attribute ptp4l deaths
  via ps before debugging "crashes").

## 2. Machine (dev VM)

Arch Linux VM, **96 vCPU / 31 GB RAM**. No data-plane NIC (rule above);
bench reach = ssh amx-pw0 (passwordless sudo) + USB serial/JTAG.

| Path | What |
|---|---|
| `~/prjs-avb-on-fpga/milan-fpga` | THIS repo: RTL (`hdl/`), testbenches (`tb/`), LiteX SoC + build system (`sw/litex/`), controller (`avdecc/`), docs |
| `~/the-private-test-repo` | kl-eth Linux driver, DTs, boot images, buildroot glue (`fpga/`) |
| `~/prjs-avb-on-fpga/fpga-ps-tools` | BSP/DT extraction tools (main AHEAD-5 UNPUSHED — user's call) |
| `~/litex-milan` | LiteX env: **venv** `~/litex-milan/venv` + **work/** = all build dirs (~525) |
| `~/br-milan-output` | buildroot output: `images/` (Image, rootfs.cpio.xz), host toolchain, linux-7.0.11 tree; rootfs overlay incl. `.../board/milan_naxriscv/rootfs_overlay/etc/init.d/S50milan` (dir name is historical — CPU is VexiiRiscv) |
| `~/refs/AX7101` | Alinx board repo clone — reference ONLY, push disabled |
| `~/Xilinx`, `~/Xilinx2` | Vivado 2026.1 ×2; **build.sh sources `~/Xilinx2/2026.1/Vivado/settings64.sh`** (has Artix-7 + Zynq-7000) |

- Build env: `source ~/Xilinx2/2026.1/Vivado/settings64.sh` +
  `export PATH=~/litex-milan/venv/bin:$PATH`; long jobs via `setsid nohup`
  with a log under `~/litex-milan/work/` (plain bg jobs die with the session).
- `rtk` proxies/dedups CLI output (token filter); for forensics read raw
  files or `rtk proxy <cmd>`.
- git identities: milan-fpga = default (hackerman-kl); the-private-test-repo
  commits use `-c user.name="Alexandre Malki" -c user.email="alexandremalki89@gmail.com"`.
- pw0 tools: `/tmp/milan_controller.py` (deployed copy of
  `avdecc/milan_controller.py` — REDEPLOY after edits),
  `~/la_avdecc_work/enum-probe` (built with la_avdecc's OWN feature defines —
  ABI trap, see §8), tcpdump, iperf3.

## 3. Boards — facts + live state (2026-07-14)

| | AX7101 | Arty A7-100T |
|---|---|---|
| FPGA | xc7a100t-2fgg484 | xc7a100t-1csg324 (slower die) |
| CPU | VexiiRiscv 2-hart @100 MHz | VexiiRiscv 2-hart @83.333 MHz |
| Milan datapath clk | 100 MHz (`--milan-clk-freq 100e6`) | 50 MHz |
| PHY | RTL8211E GMII 1G | MII 100M |
| EID / IP | ...:01 / 192.168.127.1 | ...:02 / .3 |
| Gateware NOW | `build_ax7101_eto_miltalk` WNS +0.072, **JTAG-SRAM** | `build_arty_eppo_miltick` WNS +0.381, **in QSPI** |
| QSPI (16 MB) | policy `images`: Linux images only, kernel @0 — **NEVER flash a bitstream** (kernel-clobber trap; deploy.sh refuses without FORCE_BITSTREAM_FLASH=1). Image set = hwts4-era per-board rootfs + fixed opensbi/dtb | policy `boot` (v3): bitstream @0 (4 MiB) + xz kernel @0x400000 + opensbi @0x700000 + dtb @0x760000 + rootfs @0x780000; **JP1=QSPI, fully self-hosting** |
| Power-cycle | FPGA goes BLANK → JTAG reload needed | reboots to full Milan endstation hands-free |
| Driver | kl-eth auto-loads; `kl,rsc-clk-mhz` from DT (AX 100 / Arty 50); RSC on @250 µs | same |
| Talker | AAF present but **off** (talker half idle) | **TRUE Milan mode**: S50milan writes `0x654=0x1` → silent until PROBE_TX, then 8138 fr/s AAF from the Pmod I2S2, hard stop 15 s after last probe |

Both boards: probe window 14–15 s measured, ADP cadence 31 s (×2 periods),
dormancy self-heal ≤5 s proven, controller drill 41/41, la_avdecc Milan=1
CLEAN. Bench cosmetics: AX console needs `dmesg -n 1` under talker RX;
initramfs "invalid magic" after the real unpack is benign.

**gPTP bench end-state:** reflash bounces re-triggered the switch's port
flap-suppression → the Arty's cc6 announces are not relayed uplink; pw0 is
SLAVE ~5 ns to the SWITCH HOLDOVER (3cc0c6, cc248). Arty GM itself runs
clean (txto=0). Remedy is physical: switch power-cycle (amx-pi) or direct
cable. Data plane unaffected.

**Fallback builds** (all in `~/litex-milan/work/`):

| Build | What | WNS |
|---|---|---|
| build_arty_eto_lwsrp | Arty lwSRP keeper CANDIDATE (not yet loaded; asl −0.287 fail, eppo died in route — sweep variance) | +0.121 |
| build_ax7101_*_lwsrp | ALL 3 SEEDS FAIL PLACEMENT (Place 30-487: LUTs 62408/63400 = 98.4 %). AX was ~97 % before lwSRP | — |
| build_arty_*_milanv12 | ALL 3 SEEDS FAIL PLACEMENT (66599/63400 LUTs = 105 % — the v1.2 close-out logic tipped ARTY too). **Root cause found by hierarchical synth report: aecp u_ingress = 8197 LUTs** (128-byte register fbuf with unaligned byte write decoders + replay muxes) — vs the lwSRP BRAM-FIFO ingress at 106 LUTs | — |
| build_ax7101_asl_milanv12d | **AX7101 Milan-v1.2 KEEPER** — closes at 100 MHz after area-70 round 1 (`42fdc6f`+`f018fd0`+`a6976dc`, −15.3K placed LUTs → 51284/63400 = 80.9 %, slices 97.6 %); all 3 seeds ≥ +0.023 (eto +0.082, eppo +0.023). NOT loaded | +0.123 |
| build_arty_eppo_milanv12d | **Arty Milan-v1.2 KEEPER** — area-fixed netlist, all 3 seeds close (asl +0.117, eto +0.022), LUTs 51306 = 80.9 % (supersedes eppo_milanv12b +0.001). NOT loaded | +0.154 |
| build_arty_*_milanv12e | **DO NOT USE** — csr shadow-RAM regressed it: 2 if-arm writes inferred 2 write ports → Synth 8-6849 BRAM-infeasible → +704 LUTRAM, LUTs 51542-69 = 81.3 %, best eppo +0.077. Fix `95a82f7` (single muxed write port → RAMB18 SDP). **Rule: grep new builds for 8-6849** | +0.077 |
| build_arty_asl_milanv12f | **Arty Milan-v1.2 KEEPER (supersedes eppo_milanv12d)** — csr shadow in BRAM (`16fe234`+`95a82f7`): LUTs 50720 = 80.0 % (−586 vs v12d), slices 96.9 %, 8-6849 clean; all 3 seeds close (eto +0.126, eppo +0.094 @ slices 96.3 %). NOT loaded | +0.174 |
| build_ax7101_asl_milanv12f | **AX7101 Milan-v1.2 KEEPER (RTL-current, supersedes asl_milanv12d)** — same shadow-BRAM netlist: LUTs 50723 = 80.0 % (−561 vs v12d), slices 97.7 %, 8-6849 clean; all 3 seeds close (eto +0.011, eppo +0.001 — thin, sweep variance; v12d asl +0.123 remains the higher-margin fallback on the pre-shadow RTL). NOT loaded | +0.076 |
| build_arty_eto_rxmon | Arty rxmon fallback — AVTP-RX monitor netlist (`832aa19`): LUTs 51630 = 81.4 %, all 3 close (asl +0.118, eppo +0.068); +0.396 = best margin ever on this design. NOT loaded | +0.396 |
| build_ax7101_eto_rxmon | AX rxmon fallback — same netlist: eto closes thin (eppo −0.050 / asl −0.088 FAIL; slices 97.6 % = space-bound; USER 07-17 authorized --l2-bytes 32768 when space-bound). NOT loaded | +0.027 |
| build_arty_eppo_pcmring2 | Arty 2-hart fallback — + AAF RX depacketizer + PCM ring (`e8efecc`+`53042cc`+hold_r-64b fix): LUTs 51860 = 81.8 %, slices 98.4 %; all 3 close (eto +0.087, asl +0.069). Traps: pcmring(1) sweep died on Vivado 8-524 out-of-range part-select in the unrolled hold_r byte mux — Verilator/yosys tolerated it; only Vivado is the Vivado oracle. NOT loaded | +0.162 |
| build_ax7101_eto_pcm1h | **AX KEEPER (RTL-current, 1-HART — USER 07-17 "keep 1 hart for now")** — same PCM-ring netlist, `--cpu-count 1`: LUTs 45545 = 71.8 % (−6.2K vs 2-hart), slices 95.8 %; ALL 3 close (eppo +0.069, asl +0.041) where 2-hart was 2/3 FAIL. L2 kept 64 KB (32 KB authorization unused). ⚠ 1-hart dtb pairs with this bitstream; 2-hart NAPI perf records don't apply. NOT loaded | +0.127 |
| build_arty_asl_pcm1h | Arty 1-hart fallback (pre-MAAP) — LUTs 45206 = 71.3 %; all 3 close (eppo +0.313, eto +0.088). NOT loaded | +0.386 |
| build_arty_asl_milanfull2 | **Arty KEEPER (RTL-current, 1-hart, FULL feature set)** — + MAAP, I2S playback, SET-replays, pilot tone (`668c179`): LUTs 46489 = 73.3 %; all 3 close (eppo +0.072, eto +0.048). E2E audio acceptance ready: TONE_CTRL 0x6DC + pcm_ring_dump + tone_thdn.py (digital −149.9 dB vs −120 limit). NOT loaded | +0.240 |
| build_ax7101_asl_milanfull2 | AX full-feature fallback (pre-0x4B/servo) — LUTs 46805 = 73.8 %; all 3 close (eppo +0.149, eto +0.029). NOT loaded | +0.172 |
| build_arty_eto_milanfinal | Arty complete-end-station fallback (pre cum-pipeline) — LUTs 47010 = 74.2 %; all 3 close (asl +0.267, eppo +0.183). ⚠ its netlist carries the 15-term cum chain: fine at 50 MHz, NEVER port to 100 MHz | +0.334 |
| build_ax7101_*_milanfinal | **DO NOT USE** — the segment-growth 15-term single-cycle cum chain = WNS −5.64/−5.88 at 100 MHz (hidden by arty's 20 ns period; found via report_timing on the failed seed). Fix `b99d56c` = 4-segs/cycle ×4 pipeline | −5.64 |
| build_ax7101_eppo_milanfinal2 | **AX KEEPER (COMPLETE end-station, cum-pipelined)** — LUTs 47239 = 74.5 %; ALL 3 close (eto +0.066, asl +0.042). THE AX bench bitstream. NOT loaded | +0.076 |
| build_arty_eppo_milanfinal2 | **Arty KEEPER (COMPLETE end-station, RTL-identical to the AX keeper)** — LUTs 46924 = 74.0 %; ALL 3 close (asl +0.077, eto +0.068). THE Arty bench bitstream (QSPI-flashable, v3.1 flow). NOT loaded | +0.143 |
| build_arty_eppo_miltick | Arty KEEPER (param-fixed tick, flashed) | +0.381 |
| build_ax7101_eto_miltalk | AX KEEPER (talker SM; eppo/asl failed — sweep variance) | +0.072 |
| build_arty_asl_adpfix | Arty pre-talker fallback (dormancy fix) | +0.243 |
| build_ax7101_asl_adpfix | AX pre-talker fallback | +0.158 |
| build_ax7101_eto_hwts_ax2 / arty asl_hwts5 | HW-timestamp keepers | +0.118 / — |
| build_ax7101_eto_acmp2 | first Milan=1 CLEAN control plane | +0.096 |
| build_arty_asl_arty_v8 | first Arty AVDECC stack (probes stripped) | +0.312 |
| build_ax7101_adp2 / build_arty_v7 | AECP-less / probes-only floors | +0.102 / +0.018 |

**Branches (all pushed unless noted):** milan-fpga `milan-arty-bringup` =
b19287e local (the working line, this doc; push on request); `main` = f51a27b (PR #12 AECP/AEM
merged). the-private-test-repo `milan-avb-stabilizing-milan` = c03c139.
fpga-ps-tools main ahead-5 unpushed. Never commit `graphify-out/`/.gitprep.

## 4. What works on silicon today (and how it was proven)

| Feature | State | Proof / normative doc |
|---|---|---|
| ADP advertise + depart + **dormancy self-re-arm** | DONE both boards | drill 0x00020001→0x00020101 ≤5 s; `docs/findings/ADP_DORMANCY.md` |
| AECP/AEM Milan entity (5 descriptors, getters/setters, LOCK, MVU, COUNTERS, AS_PATH) | DONE | la_avdecc Milan=1 CLEAN; `hdl/aecp/doc/atdecc_architecture.drawio` |
| AECP streaming cmds (GET/SET_STREAM_INFO Milan semantics, START/STOP=NOT_SUPPORTED, **real unsolicited** 4-slot engine) | DONE | 121-check TB + drill §7/7b; `docs/design/MILAN_TALKER_SM.md` |
| ACMP Milan talker SM (CONNECT_TX==PROBE_TX, 15 s window, near-stateless) | DONE | 71-check TB + wire probe→stream→expiry; same doc |
| AAF talker (48 kHz I2S2 → class-A frames, probe-gated, VID0) | DONE | 8138 fr/s, seq+1/122 µs; `docs/design/MVP_TALKER.md` |
| gPTP PHC + **HW timestamps** | DONE both boards | pdelay 1.3 µs, pw0 rms 2–5 ns through floods; `docs/findings/PTP_TS_METADATA_FIX.md`, `GPTP_RXPAD_ROOTCAUSE.md` |
| QSPI v3 self-hosted boot (Arty) | DONE | flash→login hands-free; `docs/integration/QSPI_FLASHBOOT.md` |
| TCP perf (separate perf-lineage gateware) | TX >500, RX 316 practical ceiling | `docs/findings/PERFORMANCE_GOAL.md` |
| Portability | XPM-free HDL; Yosys/sv2v 22/22 tops (ECP5 check) | `syn/yosys/run.sh` |
| **lwSRP fabric engine** (MSRP talker-adv + domain + **Listener attr declare**, MVRP, both-side registrars, 75 % bw gate → CBS slope + TX gate + listener_observed) | **RTL+TB DONE `b19287e`+07-15; silicon vs switch/pw0 PENDING** | 445+96+36-check TBs; `docs/LWSRP_FPGA_ARCHITECTURE.md` |
| **AEM/AECP Milan v1.2 mandatory set** (full 34-descriptor ROM FR-ENUM-02, SET/GET_CLOCK_SOURCE, CONTROL IDENTIFY → LED, GET_AUDIO_MAP, MVU SYSTEM_UNIQUE_ID + MEDIA_CLOCK_REF_INFO, live GET_COUNTERS, MAX_TRANSIT_TIME 0x4C/4D, STREAM_INPUT stream-info/format/start-stop) | **RTL+TB DONE 07-15; silicon re-cert PENDING** | aecp TB 345; `hdl/aecp/doc/README.md` |
| **ACMP listener SM** (BIND_RX/UNBIND_RX/GET_RX_STATE + probe ladder + SRP binding via lwSRP TA registrar; CSR 0x6A4 RO group) | **RTL+TB DONE 07-15; silicon vs a real talker PENDING** | acmp_lstn TB 89; pipewire acmp-milan-v12.c contract |

Regression: 25 Verilator harnesses under `tb/verilator/<name>/` (latest
counts: acmp 71, acmp_lstn 89, aecp 345, milan_dp 53, csr 98, lwsrp_tx 445,
lwsrp_rx 96, lwsrp 36, cls 200024) + Yosys 22/22. PLUS the behave BDD tier
(`tests/`, 8 features / 57 scenarios green — run
`~/litex-milan/venv/bin/behave tests`): two 2026-07-15 `@tsn_gen` features
drive the tsn-gen packet_gen binary (the AM65x-validation recipe) — seeded
frame generation, bit-exact field patches cross-checked via `--decode`,
Milan semantic models for SET_CLOCK_SOURCE/IDENTIFY + the ACMP listener SM,
the tsn-gen CDL+8 deviation pinned, and a repo-carried ACMPDU YAML
(`tests/protocols/acmp/`).
`docs/testing/RUNNING_TESTS.md` / `PROTOCOL_VALIDATION_MATRIX.md`.

**The reference that decides Milan semantics:** pipewire module-avb
(`acmp-milan-v12.c` etc.) — ALWAYS extract the contract from it before
writing RTL; it overturned every assumption (probe model, count=0,
DISCONNECT no-op, stream_id formula).

## 5. CSR quickref (milan_csr AXI-Lite @ **0x90000000**, both boards)

Full map: `docs/reference/REGISTER_MAP.md`. The ones you touch on the bench:

| Offset | Reg | Notes |
|---|---|---|
| 0x100 | MAC_CTRL | bit3 allmulti (`ip link set eth0 allmulticast on` — reboot reverts) |
| 0x400+q*0x20 | CBS q0-3 | +0 idle +4 hi +8 lo +C en; reset en=0. Shaper is NEVER removed (user rule) |
| 0x520 | A_PTP_CMD | PHC discipline strobes (0x500 group = INCR/ADJ hooks) |
| 0x600 | ADP_CTRL | 0x1F01 = enabled, valid_time 31; 0x1F00 = silence (single-entity drills) |
| 0x604.. | identity | programmed by `avdecc/aecp_csr_setup.sh` (caps 0x8588) |
| 0x640 | ADP_CMD | bit1 = depart strobe (nothing in SW writes it — see dormancy forensics) |
| 0x644 | ADP_STATUS | available_index; healthy = +1 per 31 s (measure ≥2 periods) |
| 0x648/0x64C | AECP cmd/resp counters | balanced ⇒ no responder mid-frame |
| 0x650 | ACMP counters | |
| 0x654 | AAF_CTRL | {vid[27:16], bypass[1], enable[0]}; reset 0x0002_0002 (VID 2, bypass on). S50milan → 0x1 = TRUE Milan mode (probe-gated, VID0); legacy always-on = `devmem 0x90000654 32 0x3` |
| 0x658/0x65C | AAF DMAC | 0x660 frames / 0x664 pairs counters |
| 0x668 | A_ADP_DIAG RO | {[17:16] last depart src, [15:8] rearm_cnt, [7:0] depart_cnt} |
| 0x66C | A_ACMP_TALKER RO | {bit3 aaf_gate, bit2 lobs, bit1 talker_active, bit0 probe_armed} |
| 0x670 | A_ACMP_LOBS RW | bit0 = listener_observed (manual); with lwSRP on, effective lobs = this OR SRP listener-ready |
| 0x680 | LWSRP_CTRL | {qidx[3:2] (reset q3), talker[1], enable[0]}; reset 0xC = **disabled** (zero behavior change) |
| 0x684–0x690 | LWSRP VID/DMAC/TSPEC | VID (reset 2), stream DMAC, {interval[31:16], max_frame[15:0]} |
| 0x694 | LWSRP_STATUS RO | drops/tfail+code/slope_en/gate/over_limit/active/domain_ok/declared/ready/reg/decl — see REGISTER_MAP |
| 0x698/0x69C/0x6A0 | LWSRP slope/cnt/latency | granted idleSlope bps RO; {rx_pdus[31:16], tx_count[15:0]}; accum latency |
| 0x6A4–0x6B4 | ACMPL_* RO | listener SM: state[2:0]/bound/active/declared/ta_reg/ta_fail/status/probing/tk_avail/vlan · talker EID lo/hi · {probes,cmds} · {fail_code, tuid} |

NIC ring/perf/debug CSRs live in the LiteX region (0xf0003xxx ring/steer,
0xf0004xxx probes) — perf-era docs in `docs/findings/`. devmem trap: 64-bit
CSRs read high-word-first.

## 6. Operating recipes

```sh
# Consoles (tmux; litex_term needs the venv path)
tmux new-session -d -s milan_qspi_boot \
  "~/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_66e0ce968c16f011808241adb887153e-if00-port0 --speed 115200"
tmux new-session -d -s arty_console \
  "~/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Digilent_Digilent_USB_Device_210319AFEED0-if01-port0 --speed 115200"
# scripted console exec: send-keys + sentinel; grep '^MARKER' (line-anchored,
# else it matches the echoed command). Board busybox has NO timeout/pgrep.

# JTAG loads (SRAM)
openFPGALoader --ftdi-serial 210512180081 -c ft232    <ax7101.bit>
openFPGALoader --ftdi-serial 210319AFEED0 -c digilent <arty.bit>
# Arty: reconfigure from QSPI without power touch:
openFPGALoader --ftdi-serial 210319AFEED0 -c digilent --reset

# Builds (sw/litex/build.sh; docs/integration/BUILDING.md)
./sw/litex/build.sh ax7101 --sweep      # 3-directive place sweep, keep best WNS
./sw/litex/build.sh arty   --sweep
# Flash (policy-aware; board_facts in build.sh):
KERNEL=~/br-milan-output/images/Image ROOTFS=~/br-milan-output/images/rootfs.cpio.xz \
DTB=~/the-private-test-repo/fpga/dts/milan_arty_vexii.dtb OPENSBI=~/the-private-test-repo/fpga/boot/opensbi_arty.bin \
PYTHON=~/litex-milan/venv/bin/python3 ./sw/litex/build.sh flash arty:<builddir>

# Milan validation drill (from pw0: ssh amx-pw0)
sudo python3 /tmp/milan_controller.py enp6s0 --eid 01   # AX   -> 41 pass, 0 fail
sudo python3 /tmp/milan_controller.py enp6s0 --eid 02   # Arty -> 41 pass, 0 fail
sudo ~/la_avdecc_work/enum-probe enp6s0 40              # Milan=1, verdict CLEAN
# enum-probe exits at its FIRST clean enumeration -> for a single-entity
# verdict, silence the other board first: devmem 0x90000600 32 0x1F00 (restore 0x1F01)

# ADP census — MUST filter, AVTP shares ethertype 0x22F0 (the arty's 8.1k fr/s
# AAF stream otherwise reads as an ADP flood / drowns :01):
sudo timeout 45 tcpdump -i enp6s0 'ether proto 0x22f0 and ether[14] = 0xfa'

# Probe the talker from pw0 (what activates the arty's stream):
#   milan_controller.py section 9 does it; window = 15 s after the last probe.

# Recovery one-liners (board console)
devmem 0x90000600 32 0x1F00; devmem 0x90000600 32 0x1F01   # ADP re-arm (pre-fix gw only)
dmesg -n 1                                                  # unbury console under RX
ip link set eth0 allmulticast on                            # gPTP RX (reverts on reboot)

# gPTP direct-cable session (Arty-as-slave validation, physical cable move):
sw/litex/gptp_direct_cable.sh   # AX=GM cc6/prio100; gates: SLAVE+rms, pdelay ~1-3us, txto=0
```

## 7. The rules (each one was paid for)

**USB / cables**
1. Serial consoles by `/dev/serial/by-id/` only, never ttyUSBn.
2. Every openFPGALoader call carries `--ftdi-serial` (two FTDI cables; a
   flash op on the wrong board is destructive).
3. VM USB passthrough is pinned by vendor:product (0403:6014, 0403:6010,
   10c4:ea60); a replug without the rule silently drops the device.

**Network / measurement**
4. amx-pw1 RESERVED; VM never gets a .127.x address.
5. Ghost-peer check before trusting any number: board `ip neigh | grep 127.2`
   must show `68:05:ca:95:b2:d1`.
6. A gate number is only valid with its FULL cell recipe; A/B in-session on
   the same cell (the cbsf_epo "TX regression" was a phantom baseline).
7. **Cadence claims need ≥2 periods** (the adpfix "31 s measured" was a
   single-period coin flip that hid the CLK-param gap for a day). ADP capture
   windows ≥70 s.
8. Measure, don't assume: no lever before its HW counter exists; decompose
   the symptom; measure before AND after (`docs/findings/` is full of
   refuted-plausible stories). OOC-synth a module before believing a
   hierarchical utilization line; read the LAST (physopt) timing summary.
9. Busybox `timeout` doesn't exist on the boards — a piped
   `timeout N tcpdump` dies instantly and fakes an empty capture.

**Pairing (LETHAL class)**
10. Driver `hs_pgsz` MUST equal gateware `--hs-page-bytes` (DMA overrun =
    panic). Capability CSR @0xf000311c + probe-check guard new pairs.
11. Ship gateware folds the legacy byte-ring; `bd=0` drivers park with
    counted drops. Arty driver domain = 50 MHz (DT `kl,rsc-clk-mhz` now
    carries it — zero-override boots).

**Flash policies (16 MB QSPI each; `board_facts` in sw/litex/build.sh)**
12. AX7101 = `images`: kernel at offset 0, NEVER flash a bitstream
    (deploy.sh refuses without FORCE_BITSTREAM_FLASH=1). Gateware JTAG-SRAM;
    power-cycle blanks the FPGA.
13. Arty = `boot` (v3): bitstream @0 + image set at shifted offsets; JP1=QSPI
    self-hosting. `build.sh flash arty:<dir>` does both stages + verify;
    sweep dirs get their layout reconstructed from soc.h.
14. OpenSBI is BOARD-SPECIFIC and EMBEDS a DTB (FW_FDT_PATH bypasses the
    flashed dtb slot). Build per board via build_opensbi.sh env; ALWAYS from
    a clean build dir (warm-tree rebuilds embedded the previous board's dtb —
    panic@0.000000; script force-cleans now).

**Builds**
15. 32 Vivado threads per build (hard cap), max 3 parallel on the 96-core
    box (USER RULE: saturate it — important configs = 3-seed sweeps, keep
    best WNS), launches staggered 90 s, always setsid.
16. Gate: WNS ≥ 0 (QSPI corrupted below +0.03 at 112.5 MHz once). Arty die
    is -1: sys 83.333 + datapath 50 is the closing clocking.
17. Elaborate WITHOUT --build first (~2 min) before burning 40 min of P&R.
    After scripted SV edits: grep the result AND read synth warnings —
    an undriven data input is silicon-silent (o_ptp_now trap; milan_dp TB
    now runs -Werror-UNDRIVEN).

**Repo / HDL**
18. Commits: ONE short line, no attribution trailers, both repos.
19. New HDL is ALWAYS SystemVerilog; Python only for soft-CPU SoC plumbing
    (USER RULE).
20. The CBS traffic shaper is never REMOVED from a build (USER RULE);
    bit-exact internal optimization is allowed.
21. Workstreams on separate branches; main receives merges. Push only on
    request.

## 8. Traps index (verified, still-live)

- **la_avdecc enum-probe ABI**: build against the lib's own feature defines
  (CBR/JSON/REDUNDANCY/STRICT_2018 + nlohmann) or the vtable mismatches and
  it SIGSEGVs on the first virtual call.
- available_index must +1 on EVERY ADPDU (bump-on-change reads as
  offline/online cycling to la_avdecc).
- ADP entity_id sits at wire byte 18 (not 16); ADP census filter
  `ether[14] = 0xfa`; CDL = frame_len − 26 (tsn-gen's model is WRONG).
- VID0 policy: stream_vlan_id legitimately reads 0 in ACMP/AECP responses —
  never assert vlan≠0 in drills; assert dmac≠0 + ACMP/AECP vlan consistency.
- Milan windows: poll at 0.2 s when measuring the 15 s probe window (1 s
  polls race the expiry and read short).
- kl-eth multicast RX: kl_set_rx_mode ignores mc groups — standalone ptp4l
  is DEAF without allmulti; reboot reverts it (proper fix = open task).
- Switch: multi-GM-claimant makes it announce-SILENT everywhere; one strong
  claimant only. Port flap-suppression from reflash bounces needs a physical
  remedy (power-cycle via amx-pi).
- LiteX `Instance(...)`: parameters are only passed if you pass them —
  `p_MILAN_CLK_FREQ_HZ` was silently defaulted for a week (2 s ticks).
  Grep the generated verilog for every new p_/i_/o_ hookup.
- iperf3/console orchestration: one-off servers (`-s -1`), fresh ports per
  cell, unique grep tags, `ssh -n` inside while-read loops.
- QSPI images from sweep dirs: `layout_from_soch.py` reconstructs the
  manifest (soc.h is the source of truth).
- Canonical Arty images: `br-milan-output/images/rootfs.cpio.xz` (Jul-13
  turnkey). `boot/rootfs.cpio.gz` is a STALE Jul-5 copy without S50milan.

## 9. Tasks

### Closed arcs (chronological; proof in §4)
M-A1..A5 bring-up → perf campaign (TX>500/RX 316, every remaining lever
measured-refuted) → area-70 phase 1 (CBS slope engine −8K LUTs) → de-Xilinx
track 1 (XPM-free + Yosys) → QSPI v3 flashboot → ADP advertiser → AECP/AEM
entity (Milan=1) → ACMP stateless responder → gPTP Phase A (PHC) + Phase B
(HW timestamps, rms 2–5 ns) → MVP AAF talker → ADP dormancy fix → Milan
talker SM (ACMP PROBE_TX + AECP streaming + unsolicited), both boards
Milan=1 CLEAN → lwSRP fabric engine `b19287e` → **Milan v1.2 mandatory-set
close-out 2026-07-15: full 34-descriptor AEM ROM + every mandatory AEM/MVU
command + live counters + ACMP LISTENER SM with lwSRP SRP-binding**
(silicon validation = open task #1).

### Open, ranked (next work; 1–3 are the USER-directed rev-2 order)
1. **Silicon validation of the 07-14/07-15 arcs** (one bench session):
   (a) lwSRP vs the AVB switch registration DB + a real SRP peer (pw0
   module-avb or OpenAvnu mrpd): STATUS 0x694 declared→ready→active,
   granted slope @0x698, Ready withdraw closes the gate ≤600 ms, MVRP gets
   VLAN 2 registered (retires VID0 — verify switch ingress filter first).
   (b) AECP re-cert: milan_controller drill + la_avdecc enum (rebuild
   enum-probe — ~/la_avdecc_work is GONE from the VM) against the full
   descriptor ROM; aecp_csr_setup.sh now writes caps 0xC588 (identify bit
   is BACK — CONTROL[0] exists); Hive identify → user_led0.
   (c) ACMP listener: BIND_RX from pw0 controller → board probes the AX
   talker → SETTLED_RSV_OK with real SRP; CSR 0x6A4 state walk.
   Mind: with LWSRP_CTRL[0]=1 and no listener Ready, the talker stays
   silent BY DESIGN. TCAM explicit entries for 01:80:C2:00:00:0E/21
   (default-pass covers today).
2. **pw0 PipeWire listener (BIND_RX)** — module-avb listener against the
   arty talker = the audible end-to-end; then media clock recovery (NCO from
   gPTP) per `docs/design/MVP_TALKER.md`. Natural pairing with #1.
3. **Listener media path — IMPLEMENTATION COMPLETE 07-17** (this entry kept
   for lineage; see the keeper table + audio-e2e-tone memory): monitor with
   ALL Table 7-156 counters real (incl. LATE/EARLY/MEDIA_RESET via the
   playback NCO servo, trim @0x6E0), depacketizer -> PCM ring + I2S DAC
   playback, pilot tone acceptance path. Control plane (ACMP listener SM) + diagnostics
   (AVTP-RX monitor 07-17) + **fabric/SoC media plumbing DONE 07-17
   (`e8efecc`)**: KL_aaf_rx_depacketizer (hdl/avtp) strips 38/42-byte
   headers off monitor-accepted PDUs and streams full-word S32BE payload
   out m_axis_pcm into a WishboneDMAWriter loop-mode DRAM ring
   (milan_dma_pcm_* CSRs @0xf0003120, additions-only; offset = wr pointer;
   tlast NOT forwarded — the TS-ring phase-B trap). CSR 0x6C4 pdus/drops +
   0x6C8 last avtp_ts (media-clock hook). milan_dp proves BIND->AAF->
   byte-exact 64B payload (untagged rotate-2 AND tagged rotate-6) + reject
   isolation. REMAINS: the Linux/PipeWire consumer (mmap the ring, chase
   offset — bench), CRF clock recovery + dynamic audio maps.
4. **gPTP direct-cable session** — Arty-as-slave validation; script ready
   (`sw/litex/gptp_direct_cable.sh`), needs the physical cable move.
5. **Switch power-cycle via amx-pi** — clear flap suppression, restore the
   Arty-GM→pw0 relay.
6. **kl-eth set_rx_mode** — honor mc groups (allmulti workaround reverts
   every reboot).
7. **is_1g CBS slopes on the Arty** — true class-A shaping at 100M (today
   the talker injects post-shaper, unshaped).
8. **One-opensbi durable form** — BIOS passes a1=dtb, platform reads
   timebase from FDT (removes the per-board opensbi class).
9. **Priority TX ring / doorbell in kl-eth** — the gPTP TX-flood delay is
   the single 256-slot TX ring.
10. **Area-70 continuation** (USER directive 07-15: back below ~70 %,
    config-in-RAM approach). **ROUND 1 EXECUTED 07-15 late** (yosys LC
    before/after): aecp ingress 8.2K→0.1K (`42fdc6f`) · acmp responder
    4647→498 + listener 4860→1127 (`f018fd0`) · aecp builder buf_r
    3865→3018 (`a6976dc`) ≈ **−17K banked**, all byte-exact-gated.
    Recipe: beat-aligned word writes → distributed RAM, fixed-lane
    register captures for decode fields, per-beat lane overrides at
    emit (async LUTRAM reads = zero FSM change). REMAINING:
    (a) milan_csr 2348 LCs — read-shadow RAM (CAREFUL: shadow must
    store the READBACK value, masked fields/W1C differ from wdata);
    (b) byte-ring fold (rule-11 pairing checklist); (c) walker shared
    subtractor + control sets + accessor dir → RAM. Quantifying
    arty/AX resweep pends on build slots (AX round-2 occupying).
    CBS shaper NEVER removed. Success = arty WNS ≥ +0.1 and AX closing
    100 MHz with margin.
11. **Perf follow-ups** (perf lineage): ~220-vs-525 cell-recipe gap, TX
    mid-flow stall, AF_XDP ZC (the RX>500 lane).
12. **Arty listener half — media** (AAF RX sink/I2S out/CRF): the control
    plane (descriptors, ACMP listener SM, SRP binding) landed 07-15; the
    audio path is what remains.
13. **AECP deferred (small tail)**: NV persistence of SET_* (volatile
    mirror today), GET_DYNAMIC_INFO 0x4B (SHOULD), dynamic audio-map edits
    (ADD/REMOVE — static maps shipped), MAAP dynamic allocation,
    unsolicited pushes for clock/control changes. **DONE 07-17:
    STREAM_INPUT counters** — KL_avtp_rx_monitor (hdl/1722) on the RX tap
    matched to the ACMP-listener bound sid: valid=0xF3F live (lock/settle/
    mismatch/interrupt/100ms-unlock/format-compare per the pipewire
    stream.c contract), GET_COUNTERS(in0/in1) full-size, unsolicited
    counters push 1/s, CSR 0x6B8-0x6C0, 26 suites + yosys 23/23.
    MEDIA_RESET/LATE/EARLY advertised-zero (= reference; land with the
    media path / media clock).
14. fpga-ps-tools: push main (ahead-5) — user's call.

### Doc index (normative first)
`docs/design/ARCHITECTURE_HW_SW_SPLIT.md` (rev 2 split) ·
`docs/design/MILAN_TALKER_SM.md` (talker contract + SM) ·
`docs/LWSRP_FPGA_ARCHITECTURE.md` (lwSRP as-built; CSR 0x680 map) ·
`docs/design/MVP_TALKER.md` · `docs/overview/FULL_FPGA_SOLUTION.md` ·
`docs/reference/REGISTER_MAP.md` · `docs/integration/BUILDING.md` ·
`docs/integration/QSPI_FLASHBOOT.md` · `docs/testing/RUNNING_TESTS.md` ·
`docs/testing/PROTOCOL_VALIDATION_MATRIX.md` · findings:
`ADP_DORMANCY.md`, `GPTP_RXPAD_ROOTCAUSE.md`, `PTP_TS_METADATA_FIX.md`,
`PERFORMANCE_GOAL.md` (perf lineage), `SESSION_HANDOFF.md` (historical).

### History anchors (git, newest first)
`2d700ec` AECP Milan v1.2 mandatory-set close-out (34-descriptor ROM + all
mandatory commands) ·
`b19287e` lwSRP fabric engine (hdl/lwsrp ×9, CSR 0x680, 3 TB suites) ·
`3fce652` miltick close-out (window 15 s exact, cadence 31 s ×2, 41/41,
Milan=1) · `c3b0e82` MILAN_CLK_FREQ_HZ never passed — plumbed ·
`165d57c` talker SM RTL · `ba76908` ADP dormancy self-re-arm + DIAG ·
PR #12 AECP/AEM merge (`f51a27b`).
