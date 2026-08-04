# Handover — 2026-08-02

Continues [HANDOVER_0731.md](HANDOVER_0731.md) (the `HANDOVER_0801.md` in the
working tree is untracked and stale — this file supersedes it). Repo:
`milan-fpga`, branch **`main-push`**; written at head `cc1057ec`, and while it
was being written **the SRP-arbiter re-time landed as `200bb618`** (see §4).
Facts below are from the tree, the build dirs and the sibling
`milan-tests-avb` repo; the few things only a live bench can confirm are
marked **[session-lore, verify]**.

DUT = **ALINX AX7101 ONLY** (Arty retired by USER 07-31). Shape fixed by
USER: 8 talkers × 8 listeners, 8ch/stream, RV32 VexiiRiscv. Bench operations:
[docs/findings/BENCH_TOPOLOGY.md](docs/findings/BENCH_TOPOLOGY.md) (refreshed
today). The day's three closed defect classes:
[docs/findings/DEFECT_CLASSES_0802.md](docs/findings/DEFECT_CLASSES_0802.md).

---

## Contents

- **[1. One-line state](#1-one-line-state)** — Silicon, campaign and the one blocker (a fit) in a single sentence.
- **[2. What is ON SILICON](#2-what-is-on-silicon)** — What the flashed x32p_aslm bitstream (WNS +0.014, VERSION still 0x0001_0021) and the PREEMPT_RT shielded rootfs actually contain, feature by commit — read this before attributing any bench behaviour to "old gateware".
- **[3. Campaign state (ax-rv32-e)](#3-campaign-state-ax-rv32-e)** — The running campaign, the harness upgrade whose deployment is still pending between rounds, and the FAIL triage that motivated it: 31 conformant binds and 37 smeared pairs reclassified, 35 ax-to-ax tick disagreements still real.
- **[4. The playback-fit campaign](#4-the-playback-fit-campaign)** — The desk-complete FLAC/playback path and the fit ledger that gates it: which flows died in place/route, what the BRAM directory bought, the -0.623 best seed, and the non-negotiable recipe (AlternateRoutability + ExtraNetDelay_high + PYTHONHASHSEED=0).
- **[5. What rides the next flash](#5-what-rides-the-next-flash)** — The landed-and-gated commit set that ships with the first closing playback seed, and why the flash must carry the full image set (window shifts; OpenSBI embeds the FDT).
- **[6. Open task queue](#6-open-task-queue)** — The internal ledger (#49, #53, the 08-01/02 items marked for recovery) plus the two suspected reds — and the warning that GitHub issue numbers are a different sequence.
- **[7. Bench recipes that matter](#7-bench-recipes-that-matter)** — Copy-ready: the FLAC playback end-to-end chain, the campaign launch pattern, and the flash + cold-cycle incantation with slot sizes, the shared-overlay trap and the post-boot posture checks.

## 1. One-line state

**The board runs the `x32p_aslm` bitstream (WNS +0.014) + the PREEMPT_RT
shielded rootfs; campaign `ax-rv32-e` runs against it; the playback round is
desk-complete and waits only on a fit** (best so far −0.623).

---

## 2. What is ON SILICON

**Bitstream `build_ax7101_x32p_aslm`** — the only RV32 seed to close timing
(**WNS +0.014**, bitstream written 08-02 03:50). It contains `main-push`
through `80196965`, i.e. everything the 0x0021 era added plus the 08-01/02
AECP/ACMP round:

| feature | commit(s) |
|---|---|
| ACMP CONNECT_RX provisions the lwSRP **listener row** (no more software staging) | `d2739b1b` |
| STREAM_OUTPUT counters + Milan 5.4.5 **unsolicited** pushes | `b37e3426` |
| **Dynamic audio maps**: STREAM_PORT_INPUT wakes as identity, STREAM_PORT_OUTPUT drives the capture crossbar | `a760225b`, `101b5562` |
| Listener STREAM_INPUT counters follow Milan Table 5.6 **interval** semantics | `3c82068d` |
| AECP builder **re-times** (registered emit address, oracles, one-phase-early map key, zero-fill register pair) | `e0a5759d`, `e028662a`, `235924ee`, `80196965` |
| Talker TSpec describes the emitted frame (the 0x0021 line) | `c88c07b7` |

`devmem 0x90000004` reads **`0x0001_0021`** — the VERSION constant has not
been bumped since (`milan_csr.sv:70`), so 0x0021 now names more than the
TSpec fix. **This build's AECP declared-vs-delivered length validator is what
exposed the years-old cdl defect** — see
[docs/findings/DEFECT_CLASSES_0802.md](docs/findings/DEFECT_CLASSES_0802.md) §2.

**Rootfs/image** (`milan-tests-avb`): **PREEMPT_RT** (`417840f` fragment +
threadirqs dtb + OpenSBI re-embed), RT policy fixed for one hart (`1029f16`,
`70b63cf`, `b49401b`, `4183754` — loops niced, ptp4l-only FIFO, `phc2sys -a
-rr`), the **RX shield** (`7b6f8b6` driver MC_HASH+TCAM, `ae3df43` gated
promisc, `c1ee98c` sysfs version read), **derived entity identity**
(`fa4a5e4` board side + `44c3f9f8` builder emits the conf, gate 25 forbids
literals), OpenSBI rv32 mstatush skip (`d8f09d3`). All of it boot-proven
zero-touch on 08-02 — a cold cycle comes up shielded (`eth0` flags `0x1203`)
with the correct identity and a clean gPTP cadence **[session-lore, verify
after any reflash]**.

---

## 3. Campaign state (`ax-rv32-e`)

Running on the peer host against the silicon above **[session-lore for the
live process — check the runner's jsonl mtime on pw0]**. The
**upgraded harness is committed but its deployment to pw0 is pending between
rounds**: `cc1057ec` (milan-fpga: plan + attribution semantics) and `3576806`
(milan-tests-avb: runner). Deploy both before the next round or the triage
below repeats.

FAIL-triage results that drove those fixes (details and clause quotes in
[docs/testing/TORTURE_CAMPAIGN.md](docs/testing/TORTURE_CAMPAIGN.md)):

- **31 conformant binds filed as SHALL violations** (26 reset→0→re-lock
  shapes + 5 rebinds/leftover binds). Milan 5.3.8.10 resets on the
  not-bound→bound *transition* only; 5.5.3.5.43 rebinds never transit
  UNBOUND, so they owe no reset; a small post-bind count is proof OF reset.
- **37 pair verdicts smeared** by `xside.interval-ticks-agree` when the
  peer's per-frame FRAMES counters (~8,000/s vs the Table 5.6 interval
  clause) disagreed with our conformant interval ticks — now attributed to
  the deviant side as `xside.peer-counter-semantics`.
- Still real and open: **35 ax→ax interval-tick disagreements** (both sides
  ours, so no per-frame excuse applies) **[session-lore, verify count against
  the re-run under the upgraded harness]**.

---

## 4. The playback-fit campaign

**The playback path is desk-complete**: `ad574077` (host ring → `KL_pcm_tx`
pb engine → talker wire, one-ring ship flip; hostplane + pcm_tx + milan_dp
TB legs), `d9e9f81a` (soc forwards `aaf_pb_streams`), and milan-tests-avb
`de99c33` (`snd-kl-milan` playback PCM rides the pb ring; capture-only
fallback on pre-`KL_pcm_tx` gateware). What is missing is silicon: no
playback-bearing build has closed timing yet.

Fit history (all `work/build_ax7101_*`, 08-02):

| build | flow | verdict |
|---|---|---|
| `x32p_aslm` | pre-playback tree | **+0.014 — flashed** (§2) |
| `x32pb_eto` / `x32full_eto` / `x32full_aslm` | playback tree, perf-era flows | **died in place_design** |
| `x32pb_aslm` | AltSpreadLogic_medium | **died in route_design** (2 h 34 m) |
| `x32fb_aslm` | + BRAM directory, AltSpreadLogic_medium | bitstream, **−3.517** |
| `x32fb_artb` | AlternateRoutability variant | bitstream, **−0.714** |
| `x32fb_artn` | **AlternateRoutability synth + ExtraNetDelay_high place** (+ AggressiveExplore route) | bitstream, **−0.623 — best** |

The BRAM directory (`e2cb58e6` two-level descriptor directory replacing the
linear scans, `e23f53d4` level-2 into block RAM, `af487e22` OOC source fix)
is what turned "dies in place/route" into "routes with negative slack" —
LUT→BRAM is the winning currency on this LUT-bound part, as the 07-31/08-01
rounds already measured. The `x32fb_artn` critical paths land in
`milan_datapath/lwsrp/ctx/sid_r` (the SRP context-table write behind the
listener/fabric arbitration) — and the SRP-arbiter re-time lane targeting
exactly that path **LANDED while this handover was being written**:
`200bb618` "srp fabric: registered launch stage between arbiter and ctx"
(desk sweep `.suite-logs-retime/`, 08-02 17:11). The next fit seed should
carry it; whether it closes the remaining −0.623 is the open question.

**The recipe, non-negotiable:** `AlternateRoutability` synth +
`ExtraNetDelay_high` place, and **`PYTHONHASHSEED=0` ALWAYS** — `sweep.sh`
exports it (`18fc8717`) so every seed shares one CPU netlist; an unpinned
seed forks the VexiiRiscv netlist and invalidates every A/B comparison.

---

## 5. What rides the next flash

Everything below is landed on `main-push` and desk-gated; it ships the
moment a playback-tree seed closes:

- **Playback**: `ad574077` + `d9e9f81a` (+ board side `de99c33`).
- **Tone re-grid**: `6f872b8e` — crossbar pilot steps on the `media_tick`
  grid (kills the tone/media-clock drift class).
- **GM identity atomic latch**: `50336921` — the pair commits on HI, LO
  stages (closes the on-wire spurious GM_CHANGE half of #49).
- **CRF input counters** on Table 5.6 interval semantics: `8e08af6e`.
- **Derived identity conf**: `44c3f9f8` (+ `fa4a5e4` in the rootfs — already
  deployed on the running image).
- **BRAM directory**: `e2cb58e6` / `e23f53d4`.
- **SRP-arbiter re-time**: `200bb618` (landed 08-02 17:11, after the
  `x32fb_*` seeds ran — the next fit attempt is its first).

Flash = **full image set** (`KERNEL`/`DTB`/`OPENSBI`/`ROOTFS`): the RX-queue
window shift and the pb-ring DT node both move DMA windows, and **OpenSBI
embeds the FDT** — a DTB change means an OpenSBI rebuild. `deploy.sh` gates
the pairing via `check_dtb_csr.py`.

---

## 6. Open task queue

Internal ledger (numbering continues [HANDOVER_0731.md](HANDOVER_0731.md) §6;
**GitHub issue numbers are a different sequence** — see below):

| # | item |
|---|---|
| **49** | Torn 64-bit CSR concats: the GM pair itself landed atomically (`50336921`); the **other ~11 bare `{hi,lo}` concatenations** remain, `o_ptp_tod_wr`/`o_ptp_offset` the most worrying. USER: after the audio checks. |
| **53** | LOCK_ENTITY/ACQUIRE_ENTITY bind descriptor **type but not index**; `w_b16/w_b17` unwired; read the payload offset from 1722.1 7.4.2/7.4.3, do not infer. |
| **54 / 56 / 57 / 58 / 60** | Minted in the 08-01/02 sessions; not yet written to the tree **[session-lore, verify — recover from the session notes before relying on this list]**. |
| — | The **35 ax→ax interval-tick disagreements** (§3). |
| — | **CRF behave red, suspected from `8b5cbd96`** (class-B CBS strip): CRF is CLASS A MANDATORY and must never be weakened — re-run `cd tests && behave` and read the CRF features first before touching anything. |

GitHub (`kebag-logic/milan-fpga`, open, **separate numbering**): **#48** AECP
undersized frames (<45 B) bypass the `target_entity_id` filter — an unmerged
worktree lane holds a candidate fix (`CDL_ORIGIN_C` 6 → 14, with the
exact-boundary TB case); **#50** auto-generate the register map; **#53** Zynq
integration variants.

---

## 7. Bench recipes that matter

**FLAC playback end-to-end** (desk-proven chain; the on-silicon run is what
the next flash buys) **[session-lore, verify the exact device numbers on the
new image]**:

```sh
# on amx-pw0 (the board has no decoder): decode + push
ffmpeg -i track.flac -f s32be -ar 48000 -ac 8 track.raw     # or flac -d
ssh root@192.168.127.1 "cat > /tmp/track.raw" < track.raw    # dropbear: no sftp
# on the board: card "Milan", playback PCM = the KL_pcm_tx pb ring
aplay -D hw:Milan,0 -f S32_BE -r 48000 -c 8 /tmp/track.raw
# bind talker 0 -> a peer (p) primary, then verify AT THE TAP + on the peer
```

**Campaign launch** (peer host, `milan-tests-avb/tools/`; full flag reference
in [docs/testing/TORTURE_CAMPAIGN.md](docs/testing/TORTURE_CAMPAIGN.md) §3):

```sh
sudo -E python3 tools/milan_torture.py --areas matrix --iface enp6s0 ...
python3 tools/test_milan_torture.py        # the runner's own 87-test gate
```

**Flash + cold cycle** (details in
[docs/findings/BENCH_TOPOLOGY.md](docs/findings/BENCH_TOPOLOGY.md) §5):

```sh
AX_FTDI=210512180081 KERNEL=... DTB=... OPENSBI=... ROOTFS=... \
  ./sw/litex/build.sh flash ax7101:build_ax7101_<seed>_<tag>
# deploy wraps each image as a LiteX FBI (litex.soc.software.crcfbigen, -f -l,
# little-endian header) and writes it with:
#   openFPGALoader -o <off> --write-flash --file-type raw --verify \
#     --ftdi-serial 210512180081 -c ft232 --fpga-part xc7a100tfgg484
# slots (16 MB N25Q128): bitstream@0 (4 MiB) · Image.xz (3 MiB slot) ·
#   rootfs.cpio.xz (slot 7,733,248 B - last build had 17 KB slack; xz with
#   1 stream / 1 block / CRC32 per flash_verify.sh)
# SHARED-OVERLAY TRAP: the rv32 ring blobs replaced the rv64 ones in the
#   buildroot overlay (rv64 originals in board/milan_naxriscv/rv64-archive/);
#   restore them before any rv64 rebuild.
ssh amx-pi 'powerstrip off 0; sleep 6; powerstrip on 0'      # OUT0 = the AX
# then: devmem 0x90000004 == 0x00010021 (until VERSION is bumped),
#       cat /sys/class/net/eth0/flags == 0x1203 (shield posture),
#       console CP2102N @115200 (currently /dev/ttyUSB1 - DRAIN it first,
#       the FTDI buffer replays a stale boot log)
```
