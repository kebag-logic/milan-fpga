#!/usr/bin/env python3
"""Build the lane B3 page tables and summary from the offline analyses.

usage: b3_tables.py <raw_root> <summary_json_out> <tables_md_out>

Reads the analyses written next to each raw capture (grade_617.py,
decode_din_pairs.py, decode_capture.py, attribute_dout.py and grade_usb.py
outputs) and the DUT console reads of each action, and writes one JSON
summary and the Markdown tables the findings pages carry. No bench access.
"""
import json
import re
import sys
from pathlib import Path

raw, out_json, out_md = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])


def load(p):
    return json.loads((raw / p).read_text())


def words(path, addr):
    """The little-endian 32-bit words of one mem_read dump in a console transcript."""
    txt = (raw / path).read_text(errors="replace").replace("\r", "")
    m = re.search(r"cmd='mem_read 0x%08x (\d+)'.*?\n(0x%08x .*?)\n(?:\x1b|litex|###|$)" % (addr, addr), txt, re.S)
    b = []
    for line in m.group(2).splitlines():
        parts = line.split()
        for h in parts[1:17]:
            if re.fullmatch(r"[0-9a-f]{2}", h):
                b.append(int(h, 16))
            else:
                break
    return [b[i] | b[i + 1] << 8 | b[i + 2] << 16 | b[i + 3] << 24 for i in range(0, len(b) - 3, 4)]


def n(x):
    return f"{x:,}"


S = {}
md = []
# ---------------------------------------------------------------- DIN
g = load("din-long/grade.json")
pr = load("din-long/pairs.json")
slip = {t: words(f"din-long/dut-{t}.txt", 0x900008D4)[1] for t in ("before", "streaming", "after-play", "final")}
S["din"] = dict(file=g["file"], bytes=g["bytes"], sha256=g["sha256"], pdus=g["pdus"], frames=g["frames"],
                sequence_gaps=g["sequence_gaps"], header_mismatch=g["header_mismatch"], region=g["region"],
                torn_region=g["torn_frames_in_region"], torn_recording=g["torn_frames_whole_recording"],
                invalid_region=g["invalid_frames_in_region"], lr_mismatch=g["left_right_mismatch_per_pair"],
                states=g["pair_offset_vs_pair0"], steps_identical=g["steps_identical_in_all_channels"],
                ch0_steps=g["channel0_non_unit_steps"], step_gap_min=g["step_gap_min"], step_gap_max=g["step_gap_max"],
                step_frames=g["step_frames"], outside_words=g["outside_region_words"],
                tail_frames=g["frames_after_region_before_idle"],
                slip_tdm={t: dict(dups=v & 0xFFFF, skips=v >> 16) for t, v in slip.items()},
                per_channel=pr["per_channel"])
d = S["din"]
md.append("<!-- din-run -->")
md.append("| Run | Recording | AVTP PDUs | Sequence gaps | Playback region | Torn frames, region | Torn frames, whole recording | Invalid words, region | Result |")
md.append("|---|---|---|---|---|---|---|---|---|")
md.append(f"| `din-long` | {n(d['frames'])} frames | {n(d['pdus'])} | {d['sequence_gaps']} | {n(d['region']['frames'])} frames, "
          f"{d['region']['seconds_at_48k']} s | {d['torn_region']} | {d['torn_recording']} | {d['invalid_region']} | PASS |")
md.append("")
md.append("<!-- din-channels -->")
md.append("| Stream channel | Pattern tag | TDM slot | Valid words | +1 steps | Repeats | Skips | Other steps | Result |")
md.append("|---|---|---|---|---|---|---|---|---|")
for c in d["per_channel"]:
    st = c["steps"]
    md.append(f"| {c['stream_channel']} | {c['expected_tag']} | {c['stream_channel']} | {n(c['words'].get('own_tag', 0))} | "
              f"{n(st.get('+1', 0))} | {st.get('0', 0)} | {st.get('+2', 0)} | {st.get('other', 0)} | In order |")
md.append("")
# ---------------------------------------------------------------- DOUT
dc = load("dout-long/decode.json")
at = load("dout-long/attribution.json")["summary"]
rd = {t: dict(stat=words(f"dout-long/dut-{t}.txt", 0x900006B8), tsd=words(f"dout-long/dut-{t}.txt", 0x900006EC)[0],
              slip=words(f"dout-long/dut-{t}.txt", 0x900008D4)) for t in ("before", "active-2", "after-capture", "final")}
S["dout"] = dict(file=dc["file"], bytes=dc["bytes"], sha256=dc["sha256"], frames=dc["frames"], silent=dc["silent_frames"],
                 torn=dc["torn_frames"], per_channel=dc["per_channel"], steps=dc["ordinal_steps"], attribution=at,
                 avtprx_err_after=rd["after-capture"]["stat"][2], pcmrx_after=rd["after-capture"]["stat"][3],
                 avtprx_stat_after=rd["after-capture"]["stat"][0], tsd_after_ns=rd["after-capture"]["tsd"],
                 render_rails=[rd[t]["slip"][2] >> 16 for t in ("before", "active-2", "after-capture", "final")])
d = S["dout"]
md.append("<!-- dout-run -->")
md.append("| Run | Frames | Torn | Invalid words | Zero words | Slot order | Beat clusters | Underrun clusters | Result |")
md.append("|---|---|---|---|---|---|---|---|---|")
inval = sum(c["non_pattern_words"] for c in d["per_channel"])
zero = sum(c["zero_words"] for c in d["per_channel"])
md.append(f"| `dout-long` | {n(d['frames'])} (70 s) | {d['torn']} | {inval} | {zero} | Identity | {at['beat']}: "
          f"{at['beat_repeats']} repeated, {at['beat_skips']} dropped | {at['underrun_clusters']}: {at['sender']} after logged "
          f"talker lateness, {at['unexplained']} without | PASS |")
md.append("")
md.append("<!-- dout-channels -->")
md.append("| SoC capture channel | Mapped stream channel | TDM slot | Recovered tag | Valid words | Result |")
md.append("|---|---|---|---|---|---|")
for c in d["per_channel"]:
    (t, k), = c["tags"].items()
    md.append(f"| {c['soc_channel']} | {c['soc_channel']} | {c['soc_channel']} | {t} | {n(k)} | In order |")
md.append("")
# ---------------------------------------------------------------- USB
S["usb"] = []
md.append("<!-- usb-runs -->")
md.append("| Run | Capture | Frames | Pass the pattern rule | Silent frames (stretches) | Slot order kept | Rotated by 1 to 7 words | Other | Rotation changes | Longest run in one rotation | Result |")
md.append("|---|---|---|---|---|---|---|---|---|---|---|")
for r in ("usb-long", "usb-long2"):
    u = load(f"{r}/grade.json")
    ev = [json.loads(l) for l in (raw / r / "events.jsonl").read_text().splitlines() if l.startswith("{")]
    arec = next(e for e in ev if e["kind"] == "arecord")
    fc = u["frame_classes"]
    rot = sum(fc.get(f"rot{k}", 0) for k in range(1, 8))
    lb = u["low_byte_histogram"]
    nz = sum(v for k, v in lb.items() if k != "0x00")
    tot = sum(lb.values())
    longest = max((x["last_frame"] - x["first_frame"] + 1 for x in u["rotation_run_list"]), default=0)
    stat = {t: words(f"{r}/dut-{t}.txt", 0x900006B8) for t in ("active-2", "after-capture")}
    rails = {t: words(f"{r}/dut-{t}.txt", 0x900008D4)[2] >> 16 for t in ("active-2", "after-capture")}
    row = dict(run=r, bytes=u["bytes"], sha256=u["sha256"], frames=u["frames"], seconds=arec["seconds"], arecord_rc=arec["rc"],
               strict_valid=u["strict"]["valid_frames"], silent=fc.get("silent", 0), silent_stretches=u["silent_stretches"],
               silent_stretch_max=u["silent_stretch_frames_max"], aligned=fc.get("aligned", 0), rotated=rot,
               other=fc.get("other", 0), rotation_changes=u["rotation_changes"],
               rotation_changes_after_silence=u["rotation_changes_after_silence"], longest_rotation_run=longest,
               rotation_frames_by_k=u["rotation_frames_by_k"], low_byte_nonzero=nz, low_byte_words=tot,
               spread=u["channel_spread_in_aligned_or_rotated_frames"], within_segment_steps=u["within_segment_steps"],
               joins=u["joins_between_ordinal_segments"], joins_unit=u["joins_with_unit_step"],
               dut_avtprx_err=stat["after-capture"][2], dut_pcmrx_drops=stat["after-capture"][3] >> 16,
               dut_media_unlocked=(stat["after-capture"][0] >> 16) & 0xFF, render_rails=[rails["active-2"], rails["after-capture"]])
    S["usb"].append(row)
    md.append(f"| `{r}` | {row['seconds']} s, rc {row['arecord_rc']} | {n(row['frames'])} | {row['strict_valid']} | "
              f"{n(row['silent'])} ({n(row['silent_stretches'])}) | {n(row['aligned'])} ({100 * row['aligned'] / row['frames']:.1f}%) | "
              f"{n(row['rotated'])} | {n(row['other'])} | {n(row['rotation_changes'])} | {n(longest)} frames | FAIL |")
md.append("")
md.append("<!-- usb-detail -->")
md.append("| Run | Words with a non-zero low byte | Frames spread one ordinal or more | Steps inside one rotation: +1, repeat, skip, other | Joins between rotations | Joins that continue the ordinal |")
md.append("|---|---|---|---|---|---|")
for row in S["usb"]:
    st = row["within_segment_steps"]
    md.append(f"| `{row['run']}` | {n(row['low_byte_nonzero'])} of {n(row['low_byte_words'])} "
              f"({100 * row['low_byte_nonzero'] / row['low_byte_words']:.1f}%) | {n(row['spread'].get('>=1', 0))} | "
              f"{n(st.get('+1', 0))}, {n(st.get('0', 0))}, {n(st.get('+2', 0))}, {n(st.get('other', 0))} | {n(row['joins'])} | {row['joins_unit']} |")
md.append("")
out_json.write_text(json.dumps(S, indent=1) + "\n")
out_md.write_text("\n".join(md) + "\n")
print("\n".join(md))
