# How to play music out of the Milan talker

Plays a file from the board's RAM out of the AAF talker, over AVB, to a peer
listener. Proven on silicon 2026-08-03 (FLAC out of a DS20D's AES 3/4 while
the pilot tone ran on its 1/2). The full software-path audit is
[findings/APLAY_SOFTWARE_PATH_AUDIT_0803.md](findings/APLAY_SOFTWARE_PATH_AUDIT_0803.md).

The player already ships on the board as **`/usr/bin/play-milan`** (source of
truth: `milan-tests-avb/fpga/buildroot/br2-external/board/milan_naxriscv/rootfs_overlay/usr/bin/play-milan`).
Read its header before changing anything — every parameter in it is measured.

## Contents

- **[1. Convert, on a peer host: never on the board](#1-convert-on-a-peer-host-never-on-the-board)** -- The one `ffmpeg` line that produces the ring's native format (raw **S32_BE**, 48 kHz, 8 ch interleaved) and why each part of it is mandatory rather than preferred: the board is a 1-hart softcore at 0 % idle so decoding on it guarantees underruns, there is no sample-rate converter in the datapath, and a 44.1 kHz source needs `-1 dB` because resampling overshoots by a measured +0.91 dB and a loud master will clip.
- **[2. Transfer: HTTP, not scp](#2-transfer-http-not-scp)** -- Stage the whole file in `/tmp` first, over HTTP. The numbers are the argument: dropbear moves ~41 KB/s (softcore crypto), `wget` ~800 KB/s, and playback needs 1.536 MB/s, so streaming during playback competes with playback for the same hart.
- **[3. Play](#3-play)** -- `play-milan`, the four things it does that are all load-bearing (the `ktimers/0` priority raise, killing the PipeWire consumer, the map write, the exact `aplay` invocation), and an explicit do-not-improve list: `plughw:` underruns on format conversion alone, the buffer size is a cap not a choice, and the `HRTIMER_MODE_REL_HARD` "fix" hung the board dead.
- **[Honest expectation](#honest-expectation)** -- This board does **not** play 8ch/48k gap-free, and the section says so with numbers. What the recipe reliably buys is survival: without it `aplay` dies at ~20 s on the first 1.7 ms underrun. Treat a nonzero xrun count as the platform's capacity limit, not a regression.
- **[The channel map changed at VERSION 0x0043](#the-channel-map-changed-at-version-0x0043)** -- The old first trap, "the power-on map is silence," is retired: since `0x0043` stream channels 0-7 boot mapped to the host ring, so `play-milan` should sound with no map write at all. Keeps the manual bench layout for the tone-plus-music case, with two cautions: the map has been per stream **channel** since `0x0027`, not per pair slot, and the window writes a source word, so it is untouched by the `0x0043` cluster renumbering.
- **[If it is silent](#if-it-is-silent)** -- A symptom → first-check table for the failures that actually happen here: dying at ~20 s (you bypassed `play-milan`), continuous underruns (`plughw:` or the file is not on tmpfs), a silent listener needing an explicit connect-tx, a board that looks dead after cold boot until it transmits once, wrong channels (check the `0x0043` map, not an older recipe), an entity that discovers but enumerates nothing (the descriptor image was never loaded into DRAM), and a `NOT_IMPLEMENTED` reply from a command outside the current served inventory.

## 1. Convert, on a peer host: never on the board

The board is a 1-hart 100 MHz softcore at 0% idle. Decoding on it guarantees
ring underruns. Produce the ring's native format: **raw S32_BE, 48 kHz, 8 ch
interleaved**.

```sh
ffmpeg -i track.flac \
       -af "aresample=48000:resampler=soxr:precision=28,pan=7.1|c0=c0|c1=c1" \
       -f s32be -acodec pcm_s32be track.raw
```

`s32be` — **big endian**, not LE. There is no sample-rate converter in the
datapath, so 48 kHz is mandatory, not a preference. If the source is 44.1 kHz,
add `,volume=-1dB`: resampling overshoots between samples (+0.91 dB measured
here), and a commercial master near full scale will clip.

Size: 48000 x 8 x 4 = **1.536 MB/s**, so 120 s = 184,320,000 B.

## 2. Transfer: HTTP, not scp

dropbear on the board runs **~41 KB/s** (softcore crypto); wget gets
**~800 KB/s**. Playback needs 1.536 MB/s, so stage the whole file in `/tmp`
first — streaming it in competes with playback for the same hart.

```sh
# on the peer host
python3 -m http.server 8080 --directory "$(dirname track.raw)"

# on the board
wget -O /tmp/music.raw http://<peer>:8080/track.raw
```

`scp` needs `-O` (no sftp-server) and is too slow for anything long.

## 3. Play

```sh
play-milan /tmp/music.raw          # default is /tmp/music.raw

while true; do play-milan; done    # it ENDS - loop it if a human is listening
```

That second line is not a joke: the 08-03 bench listened *after* the excerpt
had finished, twice, and concluded the path was dead.

The script does four things, all necessary:

1. raises `ktimers/0` to `chrt -f -p 70` — on PREEMPT_RT the driver's soft
   hrtimer defers there at SCHED_FIFO **1**, below napi (50) and ptp4l (80);
2. kills the PipeWire consumer stack, which is pure overhead for playback;
3. writes the channel map (see below);
4. `exec chrt -f 60 aplay -D hw:Milan,0 -f S32_BE -r 48000 -c 8
   --period-size=512 --buffer-size=4096`.

**Do not "improve" these.** `plughw:` instead of `hw:` underruns continuously
on format conversion alone. `--buffer-size=4096` is the cap, not a choice
(`PB_LEN 0x20000` = 4096 frames = 85.3 ms). `--period-size=512` gives eight
periods; the 2048 default gives two, so one late wake drains the whole ring
(measured over 115 s: 2048 -> 18 xruns, 512 -> 11).

And do **not** change the driver's hrtimer to `HRTIMER_MODE_REL_HARD` to fix
the stutter. It **hung the board dead** — no console, no network, cold cycle to
recover — because `_HARD` runs the callback in hard-IRQ context where
`snd_pcm_period_elapsed()`'s stream lock is an RT sleeping lock.

## Honest expectation

This board does **not** play 8ch/48k gap-free. Best observed is 0 xruns over
45-85 s windows; the same recipe over 115 s gave 10. What the recipe buys
reliably is *survival*: without it aplay takes one 1.7 ms underrun and dies
with `write error: Input/output error` at ~20 s. **Treat a nonzero xrun count
as the platform's capacity limit, not a regression.**

## The channel map changed at VERSION 0x0043

The old first trap was "the power-on map is silence" — every slot booted to
SRC 5 loopback, which emits digital silence unless something is bound inbound.
**That is no longer true.** Since 0x0043 the talker boots mapped to the host
ring:

```
AEM_ODMAP_INIT_C = '{6'h28 .. 6'h2F}   = valid + clusters 8..15
cluster  0-7  = 0x12xx/0x1Axx  SRC 2  TDM8 physical (J11)
cluster  8-15 = 0x13xx/0x1Bxx  SRC 3  host PCM ring   <- the boot identity
cluster  16   = 0x1400         SRC 4  Pilot tone
cluster 17-24 = 0x15xx/0x1Dxx  SRC 5  loopback
```

So **stream channels 0-7 wake up on the host ring** — the music path — and
`play-milan` should sound without any map write at all.

Its step 3 remains only if you want the 08-03 bench layout (tone on one
channel, music on another):

```sh
devmem 0x90000900 32 1        # CHMAP_CTRL[0]: BOTH write-arm and fabric-enable
devmem 0x90000904 32 0x100    # capture side (bit 8), entry 0
devmem 0x90000908 32 0xC000   # EN | SRC=4 TONE
devmem 0x90000904 32 0x101    # entry 1
devmem 0x90000908 32 0xB000   # EN | SRC=3 PCM_TX, idx 0
```

Two cautions on those writes:

* The map has been **per stream channel since 0x0027**, not per pair slot. The
  script's header still describes the retired pair law ("slot k feeds channels
  2k and 2k+1"), so on current gateware these two writes set **channel 0** and
  **channel 1**, not channels 0/1 and 2/3. Channels 2-7 keep their boot value.
* The window writes a *source word*, not a cluster index, so it is unaffected
  by the 0x0043 cluster renumbering. The protocol processor serves
  `GET_AUDIO_MAP` for both Stream Port directions from the live root mapping
  stores. `ADD_AUDIO_MAPPINGS` and `REMOVE_AUDIO_MAPPINGS` atomically update
  those stores and their crossbar projection. The `0x900` window remains the
  direct diagnostic programmer. Controllers can read mappings through
  `GET_AUDIO_MAP`; software can use the `CHMAP_SNAP`/`CHMAP_LOOP` readback at
  `0x910`/`0x914`. The latter
  reports what the RAM actually holds, and its `LOOP_SUSPECT` bit separates a
  slot that is mapped but never fed from one that is working and quiet.

## If it is silent

The controller-facing diagnoses are checked against the
[Milan feature status ledger](reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `aem.mandatory-missing-set` | `missing` | - |
| `state.nonvolatile-persistence` | `missing` | - |
<!-- milan-feature-status:end -->

| symptom | first thing to check |
|---|---|
| dies ~20 s with `write error: I/O error` | you bypassed `play-milan`; the ktimers/scheduling block is missing |
| continuous underruns | `plughw:` instead of `hw:Milan,0`, or the file is not on tmpfs |
| wire is up, listener silent | the peer needs an explicit connect-tx: our ACMP listener answers CONNECT_RX SUCCESS with a null stream_id and never issues CONNECT_TX |
| board looks dead from the peer after a cold boot | the RX shield drops unsolicited inbound ARP until the board transmits once — ping *out* first |
| plays but wrong channels | check the map against the 0x0043 table above, not against an older recipe |
| the controller sees the entity but enumerates nothing — every `READ_DESCRIPTOR` returns `BAD_ARGUMENTS` | the **descriptor image was not loaded into DRAM** before the entity was enabled. The AEM model is no longer a fabric ROM: the processor's descriptor store fetches it from main memory at a **compile-time base** (the top 1 MiB of `main_ram`, derived by the LiteX builder — there is no base register to reprogram). An unloaded region fails the `"AEMI"` header magic, reports a configuration count of zero, and the read is rejected on its `configuration_index` before any locate is attempted — hence `BAD_ARGUMENTS` rather than `NO_SUCH_DESCRIPTOR`. Load the image, then re-enable — a late load heals **without a reset**, because every locate against an invalid image re-arms the header probe |
| enumeration mostly works but one descriptor type comes back `NO_SUCH_DESCRIPTOR` | **not the same fault as the row above.** `NO_SUCH_DESCRIPTOR` means the image *is* loaded and that descriptor type/index is genuinely not in it — a model-content problem, not a load problem. Check the image against the config it was generated from |
| a controller command comes back `NOT_IMPLEMENTED` | Check the [current AECP inventory](testing/MILAN_V12_AUDIT_2026-08-16.md#b1-the-mandatory-aecp-command-set-is-incomplete). The processor serves enumeration, counters, selected stream, clock, configuration, control, map-read and live map mutation, packed dynamic information, registration, and Milan-info commands. `NOT_IMPLEMENTED` is expected only for the mandatory gaps listed there, including `SET_STREAM_FORMAT`, `SET_STREAM_INFO`, and name access. Live mapping changes are not restored after a power cycle because saved-state persistence remains open |
