#!/usr/bin/env python3
"""Re-derive the numbers the two findings pages state from the public packet's
graded outputs (grade.json, decode.json, attribution.json, grade-summary.json,
DUT console reads). The raw captures are not public; this checks that every
stated figure follows arithmetically from the tools' published outputs.

usage: recheck_numbers.py <packet-author-dir>
"""
import json, os, re, sys
d = sys.argv[1]
J = lambda p: json.load(open(os.path.join(d, p)))
fails = 0
def chk(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {name}: got {got!r} want {want!r}")

g = J("runs/din-long/grade.json")
chk("din pdus", g["pdus"], 758604)
chk("din frames = pdus*6", g["frames"], g["pdus"] * 6)
chk("din frames", g["frames"], 4551624)
chk("din seq gaps", g["sequence_gaps"], 0)
chk("din header mismatch", g["header_mismatch"], 0)
chk("din region frames", g["region"]["frames"], 3360036)
chk("din region = last-first+1", g["region"]["last_frame"] - g["region"]["first_frame"] + 1, 3360036)
chk("din torn region", g["torn_frames_in_region"], 0)
chk("din torn whole", g["torn_frames_whole_recording"], 0)
chk("din invalid region", g["invalid_frames_in_region"], 0)
chk("din pair states", g["pair_offset_vs_pair0"], {"[0, 0, 0]": 3360036})
chk("din L/R mismatch", g["left_right_mismatch_per_pair"], [0, 0, 0, 0])
chk("din steps identical all ch", g["steps_identical_in_all_channels"], True)
chk("din non-unit steps", g["channel0_non_unit_steps"], {"0": 36})
chk("din +1 steps per ch", g["region"]["frames"] - 1 - 36, 3359999)
chk("din step gap range", (g["step_gap_min"], g["step_gap_max"]), (93990, 93993))
out = g["frames"] - g["region"]["frames"]
chk("din outside frames", out, 1191588)
chk("din outside words total", sum(g["outside_region_words"].values()), out * 8)
chk("din outside zero words = 6 (f45587) + 776*8 + 3", g["outside_region_words"]["zero"], 6 + 776 * 8 + 3)
chk("din frames after region", g["frames_after_region_before_idle"], 777)
chk("din first stop-tail frame all zero", g["edge_frames"][str(g["region"]["last_frame"] + 1)], ["00000000"] * 8)
chk("din frame 45587", g["edge_frames"]["45587"], ["ffffff00", "fffff000"] + ["00000000"] * 6)

def slip(path, tsname):
    t = open(os.path.join(d, path)).read()
    m = re.search(r"0x900008d4\s+((?:[0-9a-f]{2} ){12})", t)
    b = bytes.fromhex(m.group(1).replace(" ", ""))
    w = int.from_bytes(b[4:8], "little")
    ts = re.search(r"### (\S+) cmd='mem_read 0x900008d4", t).group(1)
    return w & 0xFFFF, w >> 16, ts
s = {k: slip(f"runs/din-long/dut-{k}.txt", k) for k in ("before", "streaming", "after-play", "final")}
for k, v in s.items():
    print(f"     SLIP_TDM {k}: dups {v[0]} skips {v[1]} at {v[2]}")
chk("SLIP_TDM reads", [s[k][0] for k in ("before", "streaming", "after-play", "final")], [383, 391, 427, 440])
chk("SLIP_TDM skips", [s[k][1] for k in s], [0, 0, 0, 0])
st = slip("restore/dut-start.txt", "start")
chk("SLIP_TDM as found", st[0], 333)

dd = J("runs/dout-long/decode.json")
at = J("runs/dout-long/attribution.json")["summary"]
chk("dout frames", dd["frames"], 3360000)
chk("dout torn/silent", (dd["torn_frames"], dd["silent_frames"]), (0, 0))
chk("dout per-channel own tag only", all(pc["tags"] == {str(c + 1): 3360000} and pc["zero_words"] == 0 and pc["non_pattern_words"] == 0 for c, pc in enumerate(dd["per_channel"])), True)
cl = dd["cluster_detail"]
beat = [c for c in cl if not c["other"] and c["skips"] > 0]
chk("dout clusters", len(cl), 59)
chk("dout beat clusters", len(beat), 36)
chk("dout beat repeats/skips", (sum(c["repeats"] for c in beat), sum(c["skips"] for c in beat)), (696, 732))
chk("dout beat net one drop each", {c["skips"] - c["repeats"] for c in beat}, {1})
bs = [c["first_frame"] for c in beat]
chk("dout beat spacing", (min(b - a for a, b in zip(bs, bs[1:])), max(b - a for a, b in zip(bs, bs[1:]))), (93989, 93992))
chk("dout attribution", (at["beat"], at["sender"], at["unexplained"], at["alignment_multiple"]), (36, 12, 11, 7))

for run, want in (("usb-long", dict(silent=327339, stretches=2420, aligned=344438, rot=2919511, other=8712,
                                    changes=2833, longest=2922, lownz=25484975, words=26163422, spread=636231,
                                    steps=(3248176, 2825, 601, 7758), joins=(4588, 5), after_sil=1315, first=1632, maxsil=2459)),
                  ("usb-long2", dict(silent=3244, stretches=4, aligned=428820, rot=3166358, other=1578,
                                     changes=238, longest=95998, lownz=28102227, words=28773277, spread=188754,
                                     steps=(3589776, 3269, 743, 889), joins=(500, 5), after_sil=4, first=0, maxsil=2441))):
    u = J(f"runs/{run}/grade-summary.json")
    fc = u["frame_classes"]
    chk(f"{run} frames", u["frames"], 3600000)
    chk(f"{run} strict valid", u["strict"]["valid_frames"], 0)
    chk(f"{run} silent", (fc["silent"], u["silent_stretches"]), (want["silent"], want["stretches"]))
    chk(f"{run} aligned", fc["aligned"], want["aligned"])
    chk(f"{run} rotated 1-7", sum(fc[f"rot{k}"] for k in range(1, 8)), want["rot"])
    chk(f"{run} every rotation occurs", all(fc[f"rot{k}"] > 0 for k in range(1, 8)), True)
    chk(f"{run} other", fc["other"], want["other"])
    chk(f"{run} classes sum", sum(fc.values()), 3600000)
    chk(f"{run} rotation changes", u["rotation_changes"], want["changes"])
    chk(f"{run} longest rotation run", u["rotation_run_span_frames"]["max"], want["longest"])
    chk(f"{run} words tag 1-8", u["words"]["tag_1_8"], want["words"])
    chk(f"{run} low byte nonzero", u["words"]["tag_1_8"] - u["low_byte_histogram"]["0x00"], want["lownz"])
    print(f"     {run} low-byte nonzero share {100 * want['lownz'] / want['words']:.2f}%  aligned share {100 * fc['aligned'] / 3.6e6:.2f}%")
    chk(f"{run} spread >= 1", u["channel_spread_in_aligned_or_rotated_frames"][">=1"], want["spread"])
    ws = u["within_segment_steps"]
    chk(f"{run} steps", (ws["+1"], ws["0"], ws["+2"], ws["other"]), want["steps"])
    chk(f"{run} joins", (u["joins_between_ordinal_segments"], u["joins_with_unit_step"]), want["joins"])
    chk(f"{run} rotation changes after silence", u["rotation_changes_after_silence"], want["after_sil"])
    chk(f"{run} first non-silent / longest silence", (u["first_non_silent_frame"], u["silent_stretch_frames_max"]), (want["first"], want["maxsil"]))
print("RESULT", "PASS" if fails == 0 else f"FAIL ({fails})")
sys.exit(1 if fails else 0)
