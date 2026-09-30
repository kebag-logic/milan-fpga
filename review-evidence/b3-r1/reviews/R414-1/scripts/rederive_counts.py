#!/usr/bin/env python3
"""Re-derive the findings pages' published figures from the published grading
outputs (the raw recordings are not public) and compare with the page values.
usage: rederive_counts.py <packet author dir>"""
import json, os, sys
A = sys.argv[1]
J = lambda p: json.load(open(os.path.join(A, p)))
chk = []
def c(name, got, want):
    chk.append((name, got, want, got == want))
g, p = J("runs/din-long/grade.json"), J("runs/din-long/pairs.json")
r = g["region"]
c("din recording frames", g["frames"], 4551624)
c("din pdus*6 == frames", g["pdus"] * 6, g["frames"])
c("din sequence gaps", g["sequence_gaps"], 0)
c("din header mismatch", g["header_mismatch"], 0)
c("din region frames", r["last_frame"] - r["first_frame"] + 1, 3360036)
c("din region seconds (3 dp)", round((r["last_frame"] - r["first_frame"] + 1) / 48000, 3), 70.001)
c("din torn region", g["torn_frames_in_region"], 0)
c("din torn whole", g["torn_frames_whole_recording"], 0)
c("din invalid region", g["invalid_frames_in_region"], 0)
c("din pair offsets", g["pair_offset_vs_pair0"], {"[0, 0, 0]": 3360036})
c("din LR mismatch", g["left_right_mismatch_per_pair"], [0, 0, 0, 0])
c("din steps identical all ch", g["steps_identical_in_all_channels"], True)
c("din ch0 non-unit steps", g["channel0_non_unit_steps"], {"0": 36})
s = g["step_frames"]; d = [b - a for a, b in zip(s, s[1:])]
c("din repeat spacing min/max", (min(d), max(d)), (93990, 93993))
for ch in p["per_channel"]:
    c(f"din ch{ch['stream_channel']} words/steps", (ch["words"], ch["steps"]), ({"own_tag": 3360036}, {"+1": 3359999, "0": 36}))
out = g["frames"] - (r["last_frame"] - r["first_frame"] + 1)
c("din outside-region frames", out, 1191588)
c("din outside-region words census sums", sum(g["outside_region_words"].values()), out * 8)
c("din outside-region pattern words", g["outside_region_words"].get("pattern", 0), 0)
c("din frames after region before idle", g["frames_after_region_before_idle"], 777)
c("din edge frame 45587", g["edge_frames"]["45587"], ["ffffff00", "fffff000"] + ["00000000"] * 6)
c("din first stop-tail frame all zero", g["edge_frames"][str(r["last_frame"] + 1)], ["00000000"] * 8)
dd, at = J("runs/dout-long/decode.json"), J("runs/dout-long/attribution.json")
c("dout frames", dd["frames"], 3360000)
c("dout torn", dd["torn_frames"], 0)
c("dout silent", dd["silent_frames"], 0)
c("dout per-channel identity", [(x["soc_channel"], x["tags"], x["zero_words"], x["non_pattern_words"]) for x in dd["per_channel"]],
  [(k, {str(k + 1): 3360000}, 0, 0) for k in range(8)])
sm = at["summary"]
c("dout beat/sender/unexplained", (sm["beat"], sm["sender"], sm["unexplained"]), (36, 12, 11))
c("dout beat repeats/drops", (sm["beat_repeats"], sm["beat_skips"]), (696, 732))
b = [x for x in at["clusters"] if x["kind"] == "beat"]
c("dout beat net one drop each", sorted({x["skips"] - x["repeats"] for x in b}), [1])
bs = [x["first_frame"] for x in b]; bd = [q - p_ for p_, q in zip(bs, bs[1:])]
c("dout beat spacing min/max", (min(bd), max(bd)), (93989, 93992))
for run, want in (("usb-long", dict(silent=327339, st=2420, al=344438, rot=2919511, oth=8712, rc=2833, lr=2922, lb=25484975, lw=26163422, sp=636231,
                                     steps={"+1": 3248176, "0": 2825, "+2": 601, "other": 7758}, j=4588, ju=5, ras=1315, smax=2459)),
                  ("usb-long2", dict(silent=3244, st=4, al=428820, rot=3166358, oth=1578, rc=238, lr=95998, lb=28102227, lw=28773277, sp=188754,
                                      steps={"+1": 3589776, "0": 3269, "+2": 743, "other": 889}, j=500, ju=5, ras=4, smax=2441))):
    u = J(f"runs/{run}/grade-summary.json"); fc = u["frame_classes"]
    rot = sum(v for k, v in fc.items() if k.startswith("rot"))
    c(f"{run} frames", u["frames"], 3600000)
    c(f"{run} strict valid", u["strict"]["valid_frames"], 0)
    c(f"{run} classes sum", fc["aligned"] + rot + fc["other"] + fc["silent"], 3600000)
    c(f"{run} silent/stretches/max", (fc["silent"], u["silent_stretches"], u["silent_stretch_frames_max"]), (want["silent"], want["st"], want["smax"]))
    c(f"{run} aligned/rotated/other", (fc["aligned"], rot, fc["other"]), (want["al"], want["rot"], want["oth"]))
    c(f"{run} aligned share %", round(100 * fc["aligned"] / 3600000, 1), round(100 * want["al"] / 3600000, 1))
    c(f"{run} rotation changes/longest", (u["rotation_changes"], u["rotation_run_span_frames"]["max"]), (want["rc"], want["lr"]))
    c(f"{run} rotation changes after silence", u["rotation_changes_after_silence"], want["ras"])
    c(f"{run} nonzero low byte", (u["words"]["tag_1_8"] - u["low_byte_histogram"]["0x00"], u["words"]["tag_1_8"]), (want["lb"], want["lw"]))
    c(f"{run} spread>=1", u["channel_spread_in_aligned_or_rotated_frames"][">=1"], want["sp"])
    c(f"{run} steps", u["within_segment_steps"], want["steps"])
    c(f"{run} joins/unit", (u["joins_between_ordinal_segments"], u["joins_with_unit_step"]), (want["j"], want["ju"]))
    c(f"{run} every rotation 1..7 present", all(fc.get(f"rot{k}", 0) > 0 for k in range(1, 8)), True)
for n, got, want, ok in chk:
    print(("OK   " if ok else "DIFF ") + f"{n}: {got}" + ("" if ok else f" (page {want})"))
print(f"{sum(x[3] for x in chk)}/{len(chk)} page figures re-derive from the published grading outputs")
