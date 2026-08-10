# How to play music out of the Milan talker

Plays a file from the board's RAM out of the AAF talker, over AVB, to a peer
listener. Proven on silicon 2026-08-03 (FLAC out of a DS20D's AES 3/4 while
the pilot tone ran on its 1/2). The full software-path audit is
[findings/APLAY_SOFTWARE_PATH_AUDIT_0803.md](findings/APLAY_SOFTWARE_PATH_AUDIT_0803.md).

The player already ships on the board as **`/usr/bin/play-milan`** (source of
truth: `milan-tests-avb/fpga/buildroot/br2-external/board/milan_naxriscv/rootfs_overlay/usr/bin/play-milan`).
Read its header before changing anything — every parameter in it is measured.

## 1. Convert, on a peer host — never on the board

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

## 2. Transfer — HTTP, not scp

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
  by the 0x0043 cluster renumbering. `GET_AUDIO_MAP` and the RAM readback are
  keyed by the same register, so their agreeing proves storage, not the write
  key — probe with a known-content `ADD_AUDIO_MAPPINGS` if you doubt it.

## If it is silent

| symptom | first thing to check |
|---|---|
| dies ~20 s with `write error: I/O error` | you bypassed `play-milan`; the ktimers/scheduling block is missing |
| continuous underruns | `plughw:` instead of `hw:Milan,0`, or the file is not on tmpfs |
| wire is up, listener silent | the peer needs an explicit connect-tx: our ACMP listener answers CONNECT_RX SUCCESS with a null stream_id and never issues CONNECT_TX |
| board looks dead from the peer after a cold boot | the RX shield drops unsolicited inbound ARP until the board transmits once — ping *out* first |
| plays but wrong channels | check the map against the 0x0043 table above, not against an older recipe |
