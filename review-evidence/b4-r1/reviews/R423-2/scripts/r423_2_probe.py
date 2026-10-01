#!/usr/bin/env python3
"""Round-2 reviewer probe for the #451 timing page (PR #627).

usage: r423_2_probe.py <repo> <evidence_author_dir>

Read-only. Four parts, each printed as JSON:
  arith    -- the page's round-2 numbers re-derived from the public evidence:
              the 630 s recording size, frames and seconds of the raw capture,
              the 58.7 s talker-to-unbind gap, and the ppm decomposition.
  fs       -- fs re-derived from the raw status samples in soc-capture.log by
              an independent parser (endpoints and least squares).
  offset   -- a bit-serial TDM8 line (256 bit clocks per frame, eight 32-bit
              slots, MSB first) is built for data delay D = 0, 1, 2 and read
              by a receiver fixed at D = 1 (dsp_a). Ordinals start at a random
              seed-fixed value and run past 0xffff -> 0, with repeats and skips.
              Each received capture is judged by this script's own checker and
              by the packet's decode_capture.py (hash recorded).
  text     -- page assertions: the over-claims gone, the round-2 claims present,
              and every table at HEAD against 35a60c8d byte-for-byte.
"""
import collections
import hashlib
import json
import os
import random
import re
import struct
import subprocess
import sys
import tempfile

ROUND1 = "35a60c8d6ee742216f98232c85926b435ab01b91"
PAGE = "docs/findings/451_TDM8_TIMING_SOC_BOARD.md"


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout


def arith(ev):
    ev_lines = [json.loads(x) for x in open(os.path.join(ev, "runs/timing-long/events.jsonl"))]
    unbind = next(e["t"] for e in ev_lines if e.get("tag") == "unbind")
    talker_end = next(json.loads(x)["t"] for x in open(os.path.join(ev, "runs/timing-long/controller-logs.txt"))
                      if x.startswith('{"kind":"end"'))
    start = ev_lines[0]
    plan_audio = 100e6 * 23 / (2 * 37) * 34 / 43
    plan_fs = plan_audio / 2 / 256
    return dict(
        capture_s_planned=start["capture_s"],
        bytes_at_630s=630 * 48000 * 8 * 4,
        mb_at_630s=630 * 48000 * 8 * 4 / 1e6,
        mb_at_600s=600 * 48000 * 8 * 4 / 1e6,
        raw_bytes=730595328, raw_frames=730595328 // 32, raw_seconds=730595328 / 32 / 48000,
        talker_end_t=talker_end, unbind_t=unbind, talker_end_to_unbind_s=round(unbind - talker_end, 3),
        plan_audio_hz=round(plan_audio, 3), plan_fs_hz=round(plan_fs, 4),
        plan_ppm=round((plan_fs / 48000 - 1) * 1e6, 3),
    )


def parse_status(path):
    samples, cur = [], {}
    for ln in open(path, errors="replace"):
        m = re.match(r"^(state|trigger_time|tstamp|hw_ptr)\s*:\s*(\S+)", ln)
        if m:
            cur[m.group(1)] = m.group(2)
            if m.group(1) == "hw_ptr":
                if cur.get("state") == "RUNNING" and "tstamp" in cur:
                    samples.append(dict(cur))
                cur = {}
    return samples


def fs_part(ev, plan_fs):
    s = parse_status(os.path.join(ev, "runs/timing-long/soc-capture.log"))
    trig = {x["trigger_time"] for x in s}
    t = [float(x["tstamp"]) for x in s]
    n = [int(x["hw_ptr"]) for x in s]
    fe = (n[-1] - n[0]) / (t[-1] - t[0])
    k = len(t)
    mt, mn = sum(t) / k, sum(n) / k
    slope = sum((a - mt) * (b - mn) for a, b in zip(t, n)) / sum((a - mt) ** 2 for a in t)
    res = [b - (mn + slope * (a - mt)) for a, b in zip(t, n)]
    rms = (sum(r * r for r in res) / k) ** 0.5
    steps = collections.Counter((b - a) % 4 for a, b in zip(n, n[1:]))
    return dict(samples=k, triggers=sorted(trig), window_s=round(t[-1] - t[0], 3), frames=n[-1] - n[0],
                fs_endpoints=round(fe, 4), fs_lsq=round(slope, 4),
                ppm_48k_endpoints=round((fe / 48000 - 1) * 1e6, 2), ppm_48k_lsq=round((slope / 48000 - 1) * 1e6, 2),
                ppm_plan_endpoints=round((fe / plan_fs - 1) * 1e6, 2),
                bclk_endpoints=round(256 * fe, 1), resid_rms_frames=round(rms, 3),
                resid_last_frames=round(res[-1], 2), hw_ptr_deltas_mod4=dict(steps),
                last_tstamp_after_trigger_s=round(t[-1] - float(s[0]["trigger_time"]), 3))


# ---------------------------------------------------------------- offset probe
def ordinals(frames, seed):
    rnd = random.Random(seed)
    n = rnd.randrange(0, 0x10000)
    out, events = [], []
    for f in range(frames):
        out.append(n & 0xFFFF)
        r = rnd.random()
        if r < 0.0005:
            events.append((f, "repeat"))          # next frame repeats
        elif r < 0.001:
            n += 2; events.append((f, "skip"))
        elif r < 0.0012:
            n += 7; events.append((f, "jump+7"))
        else:
            n += 1
    return out, events


def word(tag, n):
    return ((tag << 16) | (n & 0xFFFF)) << 8


def receive(seq, d):
    """Bit-serial line: data of frame f starts d bit clocks after its frame-sync edge.
    Receiver takes 256 bits starting one bit clock after each edge (dsp_a)."""
    frame_ints = []
    for n in seq:
        v = 0
        for s in range(8):
            v = (v << 32) | word(s + 1, n)
        frame_ints.append(v)
    out = bytearray()
    m256 = (1 << 256) - 1
    nf = len(frame_ints)
    for f in range(nf):
        prev = frame_ints[f - 1] if f else 0
        nxt = frame_ints[f + 1] if f + 1 < nf else 0
        win = (prev << 512) | (frame_ints[f] << 256) | nxt
        rx = (win >> (255 + d)) & m256
        for s in range(8):
            out += struct.pack("<I", (rx >> (32 * (7 - s))) & 0xFFFFFFFF)
    return bytes(out)


def own_check(raw):
    """Independent checker: per-channel tag == c + 1, invalid (low byte or tag
    outside 1..8), zero; torn frames; ordinal steps over untorn frames."""
    nf = len(raw) // 32
    w = struct.unpack("<%dI" % (nf * 8), raw)
    wrong_tag = [0] * 8; invalid = [0] * 8; zero = [0] * 8; lowbyte = [0] * 8; above8 = [0] * 8
    torn = 0; steps = collections.Counter(); prev = None
    for f in range(nf):
        ords = set()
        for c in range(8):
            v = w[f * 8 + c]
            t = v >> 24
            if v == 0:
                zero[c] += 1; continue
            if v & 0xFF:
                lowbyte[c] += 1
            if t > 8:
                above8[c] += 1
            if v & 0xFF or not 1 <= t <= 8:
                invalid[c] += 1; continue
            if t != c + 1:
                wrong_tag[c] += 1
            ords.add((v >> 8) & 0xFFFF)
        if len(ords) != 1:
            torn += 1; continue
        o = ords.pop()
        if prev is not None:
            steps[(o - prev) & 0xFFFF] += 1
        prev = o
    return dict(frames=nf, torn=torn, zero=zero, invalid=invalid, low_byte=lowbyte, tag_above_8=above8,
                valid_wrong_tag=wrong_tag,
                tag_ok_frames=[nf - wrong_tag[c] - invalid[c] - zero[c] for c in range(8)],
                step_hist=dict(sorted(steps.items())[:12]))


def offset_part(ev, frames=70000, seed=423):
    dec = os.path.join(ev, "tools/decode_capture.py")
    seq, events = ordinals(frames, seed)
    exp_steps = collections.Counter((b - a) & 0xFFFF for a, b in zip(seq, seq[1:]))
    res = dict(frames=frames, seed=seed, first_ordinal=seq[0], wraps=sum(1 for a, b in zip(seq, seq[1:]) if b < a),
               aligned_expected_steps=dict(sorted(exp_steps.items())),
               decoder_sha256=hashlib.sha256(open(dec, "rb").read()).hexdigest())
    with tempfile.TemporaryDirectory(dir=os.environ.get("SCRATCH")) as td:
        for name, d in (("aligned_D1", 1), ("one_bit_early_D0", 0), ("one_bit_late_D2", 2)):
            raw = receive(seq, d)
            p = os.path.join(td, name + ".raw")
            open(p, "wb").write(raw)
            r = json.loads(subprocess.run([sys.executable, dec, p], check=True, capture_output=True,
                                          text=True).stdout)
            res[name] = dict(
                own=own_check(raw),
                packet_decoder=dict(torn=r["torn_frames"], silent=r["silent_frames"],
                                    non_pattern=[c["non_pattern_words"] for c in r["per_channel"]],
                                    zero=[c["zero_words"] for c in r["per_channel"]],
                                    tags=[c["tags"] for c in r["per_channel"]],
                                    ordinal_steps=r["ordinal_steps"]))
    return res


# ---------------------------------------------------------------- text checks
def tables(text):
    out, cur, start = [], [], None
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.startswith("|"):
            if not cur:
                start = i
            cur.append(ln)
        elif cur:
            out.append((start, cur)); cur = []
    if cur:
        out.append((start, cur))
    return out


def text_part(repo):
    new = git(repo, "show", "HEAD:" + PAGE).decode()
    old = git(repo, "show", ROUND1 + ":" + PAGE).decode()
    tn, to = tables(new), tables(old)
    tab = []
    for (ln_n, a), (ln_o, b) in zip(tn, to):
        diff = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
        tab.append(dict(new_line=ln_n, old_line=ln_o, rows=(len(a), len(b)),
                        sha256_new=hashlib.sha256("\n".join(a).encode()).hexdigest()[:16],
                        identical="\n".join(a) == "\n".join(b), changed_rows=[d[0] for d in diff]))
    flat = re.sub(r"\s+", " ", new)
    must_absent = ["48 kHz within the SoC board's clock accuracy", "48 kHz at the board's accuracy",
                   "sum of both boards' clock errors", "every class of word check", "921.6 MB",
                   "about 55 s before the unbind"]
    must_present = ["967.7 MB at the full 630 s", "47,997.947 Hz on the SoC board's uncalibrated clock",
                    "-10.64 ppm is the plan, and the remaining -32.1 ppm is the DUT oscillator's error relative to the SoC board's clock, unsplit and unquantified",
                    "since a fast SoC board clock lowers the measured fs",
                    "One bit early trips the tag checks and the ordinal steps",
                    "The torn-frame count, the low byte and the zero-word count stay clean",
                    "One bit late trips the tag, low-byte and torn-frame checks",
                    "Only the zero-word count stays clean",
                    "not a register readback", "58.7 s before the unbind", "with `id` (uid 0)",
                    "every identity value equals that page's"]
    within = [m.start() for m in re.finditer(r"within", flat)]
    return dict(tables_new=len(tn), tables_old=len(to), tables=tab,
                absent={s: s not in flat for s in must_absent},
                present={s: s in flat for s in must_present},
                within_contexts=[flat[max(0, i - 60):i + 60] for i in within],
                page_sha256=hashlib.sha256(new.encode()).hexdigest())


def main():
    repo, ev = sys.argv[1], sys.argv[2]
    a = arith(ev)
    out = dict(head=git(repo, "rev-parse", "HEAD").decode().strip(), arith=a,
               fs=fs_part(ev, a["plan_fs_hz"]), text=text_part(repo), offset=offset_part(ev))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
