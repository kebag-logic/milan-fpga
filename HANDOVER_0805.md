# HANDOVER 2026-08-05 — listener-0 row closed at desk, the 1×1×8 TDM8 pivot, gptp single-source

State when written: the 3-seed Vivado sweep `tdm8b` for the NEW shipping
shape is running (`~/litex-milan/work/build_ax7101_{asl,eto,eppo}_tdm8b/`),
rootfs rebuilt and staged, everything else committed.

## 1. The return-leg fix is DESK-COMPLETE (VERSION 0x0023, commit e3fd67dd)

Two layers, both verified by 8 Verilator suites + yosys 49/49 + tap-purity:

1. **Sink 0 owns a dedicated lwSRP row** (`SRP_LSN0_ROW_C = L+T-1`): the
   legacy row 0 is the talker-0/software pair, and sink 0's TA coupling
   read THAT registrar — bind → eternal re-probe → no Listener Ready →
   licence shut (the whole 07-28..08-05 return-leg cluster). Now: fabric
   provisioner slot, bind-time declaration with the derived sid, probe
   answer re-provisions (5.5.3.5.18), 5.5.3.5.27 promotion from its own
   row. CSR: `A_STRM_SEL[9]` selects the row ({dir=0,idx=0} is the park
   state and could not carry the meaning); `A_STRMW_SRP` idx-0 yields to it.
2. **The walker sentinel bug (wire-facing, found under 1)**:
   `KL_lwsrp_ctx_tx.find_row` returned 4 bits with `4'hF` = "no more rows"
   — which is ALSO real lane 15, so any ≥16-ext-lane shape (8×8+CRF+
   listener-0 = 17 rows) could never serialize its top lane and re-emitted
   a stale row's sid. The milan_dp 4c leg caught it (17 rows there too).
   Fix: 6-bit `ROW_NONE_C=63`; every ctx/walker row index is 5-bit now,
   rows ≤ 32 guarded, builder row law = **L+T** (was L+T−1).

**Silicon verification PENDING** on the tdm8b flash: `bash /tmp/retleg3.sh`
(pw0) — pass = our `stream_input 0` FRAMES_RX ~8000/s after the peer bind.

## 2. USER pivot: the shipping AX shape is 1×1×8 TDM8 (509297af)

`configs/endstation_ax7101_1x1_tdm8.yaml`: ONE 8ch listener + ONE 8ch
talker stream, `channel_names: [FL,FR,FC,LFE,RL,RR,SL,SR]` (NEW yaml
parameter — names host clusters verbatim, suffixes loopback), host pool 8,
pilot, loopback 8 **fabric-backed** (`loopback_lane: true` — 4 pair holds
at this shape vs the 8×8's refused +2303 LUT), latency_taps + datapath
probes back ON. `sweep.sh ax7101` now defaults to this config; the 8×8
stays one `SWEEP_CFG=configs/endstation_ax7101_8x8.yaml` away. Fragment
always emits `NS=` now (a silent 1-stream config inherited the board 8).

Generated ROM verified: input port clusters FL..SR, output port FL..SR +
Pilot Tone + `Loopback S0 FL..SR`, PDYN all-dynamic, NPORTS=1.

## 3. gptp: yaml section = ONE source (milan-fpga + private repo commits)

`gptp:` in the yaml drives BOTH the AVB_INTERFACE descriptor's static
clock fields AND the generated `/etc/gptp.<board>.cfg` (S50milan copies it
over /etc/gptp.cfg before its seds, which are now runtime-only/idempotent).
OPT-IN: absent = byte-identical legacy ROM; present = joins model_shape so
the entity_model_id rotates (controllers cache by model id — measured today:
Hive offered ports from a stale cached model). AX values: priority1 **238**,
class 248, acc 0xFE, oslv 0xFFFF, logs [−3,0,0]. ROM bytes verified.
The LIVE half (GM id, pdelay, flags, MSRP mapping) was already served by
GET_AVB_INFO — no RTL change needed.

## 4. The user's mapping BAD_ARGUMENTS — root-caused live, docs written

`addStreamOutputAudioMappings(port 1)` refusal = the vendor validity rules
working as built. Reproduced all four side-by-side on the flashed board
(TROUBLESHOOTING **§23**): parity (L cluster→odd channel; the crossbar's
half bits are enables, not swaps), unbacked loopback cluster (8×8 build),
cross-stream index, cluster_channel≠0. Identity mapping = SUCCESS. On the
1×1 shape the cross-stream and loopback classes vanish. Probe traps (cost
an hour): STREAM_PORT types are **0x000E/0x000F** (0x0014 is
AUDIO_CLUSTER — reading ports through it serves clusters with the echoed
index rewritten = fake corrupt directory); raw AECP cdl EXCLUDES
target_entity_id and multicast AEM commands are never answered.

## 5. PB_SILENCE truth (re-scoped #11)

`0xf0003148` = the pb engine's PB_SILENCE = Milan 5.3.7.3 underrun-silence
policy. snd-kl-milan SETS it at probe — **correct**, not a gap. Clearing
it in the music chain was a workaround masking chronic fill-under. Do not
"fix" the driver; update MUSIC_REPULL on the board post-flash instead.

## 6. Rootfs staged (br-milan-output/images/rootfs.cpio.xz, 16:05)

Carries: E4-aware persist script, `gptp.ax7101.cfg` + S50milan preference
hook, 1×1 identity conf, and the **PipeWire consumer stack DEFAULT-OFF**
(single-hart budget; opt-in `touch /etc/milan-pipewire-on` or
`/etc/init.d/S99milan-audio pipewire`).

## 7. Flash sequence when tdm8b closes (pick best WNS of asl/eto/eppo)

1. csr.csv vs DTB regs + `boot_chain_pin` (dma-ts 0xf0003100, pcm-dma
   0xf0003120) — the 1×1 shape + probes-back-ON can shift windows (gate
   19c / the 5ce9a13 CSR-rot class). Deployed DTS already runs
   capture-streams=1 / playback-streams=1 — no functional DTB edit
   expected, but VERIFY.
2. Flash both slots + verify (standing rule), cold-cycle.
3. Boot checks: VERSION `0x0001_0023`, new entity_model_id (clear
   la_avdecc/Hive cache or expect a NEW entity), FL..SR clusters visible,
   descriptor gPTP fields 238/…, GET_AVB_INFO live GM.
4. `bash /tmp/retleg3.sh` — the listener-0 row on silicon.
5. Music on the new shape (aplay hw:Milan → stream 0), Hive mapping edits
   (identity + parity-preserving moves should now SUCCEED; loopback
   clusters are REAL on this build).

## 8. Open

- 0.44% stress-late residue: the tdm8b build HAS latency taps — reproduce
  under load and read the per-stage breakdown (#6).
- LiteSPI mtd decision for the journal (#7 tail).
- MUSIC_REPULL/PB_SILENCE doc on the board (#11 tail).
- Odd-index/self-loop harness guards for the next campaign run
  (secondary-network SKIP annotation).

Traps of the day, so nobody repays them: gen_aem_store.py CLOBBERS the
tracked ROM (rerun `--write-rtl <shipping cfg>` after); a sweep launched
mid-regeneration reads mixed sources (killed and relaunched clean —
tdm8a is dead, tdm8b is truth); Verilator rootp exposes internal flops
but not submodule output regs.

---
# EVENING ADDENDUM (written ~23:30) — the boot-hang saga + bench state

## The tdm8c boot hang: bisected to the N=1 core
Both tdm8c seeds hang at BIOS→OpenSBI (Liftoff, then silence; DRAM memtest
green; QSPI images proven). Eliminated by JTAG SRAM experiments (QSPI never
touched): OpenSBI (code-identical rebuild + prev binary both fine), kernel,
DTB, CLINT map, P&R marginality (2 seeds identical), **the 0x0023 RTL
(bisA: pre-round RTL hangs identically)**, and — round 1, all HANG —
loopback-lane, latency-taps+probes, the TDM8 front-end (tdm32 variant hung
too). Remaining common core: **--num-streams 1 (+ --aaf-playback +
--talker-wire-chans 8)**. ROUND 2 IN FLIGHT: `nopb` (N=1 sans playback),
`n2` (full set at N=2), `min` (bare N=1, Arty-proven shape). Verdict
automation: scratchpad/bis2_boottest.sh (JTAG load + serial verdict + strip
cycle-back + restage). USER standing order: FLASH the first booting
variant (prefer n2 > nopb; per-variant DTB/opensbi regen needed — the pb/
pcm CSR windows move with the shape; check_dtb_csr gates it).
SIDE FINDING: the 0x0023 row-widening no longer FITS the 8×8 (12,193
slices vs 11,139 — bisB placement death).

## Bench operational truths learned tonight
- **acmp-persist watcher**: 1 Hz fork loop costs aplay ~80 ms/s
  (underruns); watcher OFF = clean audio, watcher ON = rebind provisioning.
  BUT: by late evening even watcher-assisted rebind cycles stopped reviving
  the return leg (edge fires, counters reset per 5.3.8.10 — visible live —
  but no Listener Ready reaches the wire). The RETURN LEG IS DOWN on
  0x0022 tonight; the native fix is the 0x0023 build this bisect unblocks.
- **Music whole-track recipe (WORKS, zero underruns)**: pw0:9300 serves
  /tmp/ew4.raw (4ch repack, 446 MB = full track); board wget ~7 min;
  loopD = plughw:Milan 4ch S32_BE, periods 4096/32768, pb_silence cleared
  per pass, watcher OFF. Board has NO nc; wget streams ~1.1 MB/s (< 8ch
  rate — no live-stream path). RAM rootfs mints NEW ssh host keys each
  boot — ssh-keygen -R first (baked into bench_restage.sh).
- **bench_restage.sh (pw0)**: one shot after any cycle — entity wait
  (grep counters_valid, NOT rc: the tool polls forever, rc always 124),
  format-adapted binds both legs, max_transit 500000 (resets to 2 ms every
  boot while persistence is OFF — the EARLY_TIMESTAMP cause at the DS20D),
  watcher stop, music pull + loopD + soak report.
- **fmt_guard.sh (pw0)**: Hive's connect does NOT do the 5.5.1.2
  adaptation (user had to force formats by hand) — the guard audits all 8
  pairs and adapts mismatches. Run after every Hive session.
- avdecc_l2.py traps: `disconnect` takes NO --*-mac args (usage dump
  otherwise); `counters` never exits (pipe to grep, ignore rc).

## Counters: the coalesced law (USER-corrected, COMMITTED)
FRAMES_RX/TX = ATDECC quantity (frames) at Milan cadence (≤1 s publish):
the counter advances ~8000/step once per second. Implemented in
KL_avtp_rx_monitor_ctx (frx acc) + KL_talker_diag_ctx (facc), TB-green
(rxmon 93+109 incl the TV+TNV==FRX identity restored, milan_dp all legs,
VERSION pins bumped 0x0023). The peer xside deviation self-heals next
campaign. Matrix updated; first RED recorded: features_flags=0 while
accepting running mapping edits (Table 5.20 bit 30 fix queued).
