#!/usr/bin/env python3
"""Re-derive the round-2 figures of the B8 section from the published packet.

usage: rederive_round2.py AUTHOR_DIR   (review-evidence/629-b8-r1/author at 36ee6d8a)
Prints each figure with its source; states no capture channel count or format.
"""
import json, os, re, sys
A = sys.argv[1]
J = lambda p: json.load(open(os.path.join(A, p)))
g = J("summary/crfll/grade.json"); ll = J("summary/crfll/lockloss.json")
ev = [json.loads(l) for l in open(os.path.join(A, "runs/crfll/events.jsonl"))]
t = {e["kind"]: e for e in ev if e["kind"] in ("window-start", "window-end")}
host = t["window-end"]["t"] - t["window-start"]["t"]
w = g["window"]; lost = g["frame_rate_ratio"]["counted"]["capture_lost_frames"]
print("CRF window: polls in segment %d; table polls %d; missing-word polls %s"
      % (g["polls_in_segment"], ll["window"]["polls"], ll["polls_missing_a_word"]))
print("CRF window: host span %.2f s; captured %d frames = %.2f s; capture_lost %d = %.2f s; sum %.2f s"
      % (host, w["frames"], w["frames"] / 48000, lost, lost / 48000, (w["frames"] + lost) / 48000))
cl = g["skip_clusters"]; print("clusters %d, lost total %d" % (len(cl), sum(c["lost_frames"] for c in cl)))
cum = 0
for c in cl:
    pos = (c["first_frame"] - w["start_frame"]) / 48000
    print("  cluster %d: start %.1f s captured, %.1f s counting lost before; lost %.3f s; read gap %.2f s; signature %s; steps %s"
          % (c["cluster"], pos, pos + cum / 48000, c["lost_frames"] / 48000, c["recent_read_gap_ms"] / 1000,
             c["size_signature"], c["steps"] if len(c["steps"]) < 4 else "%d steps" % len(c["steps"])))
    cum += c["lost_frames"]
st = [c for c in cl if c["recent_read_gap_ms"] > 1000 and c["lost_frames"] > 1000]
print("stall clusters %s lost %.2f s" % ([c["cluster"] for c in st], sum(c["lost_frames"] for c in st) / 48000))
s = J("summary/sw/switches.json"); b = s["binds_end_s_before_first_set"]
print("#645: binds end %.3f s before the set" % b)
for p in s["from_binds"]:
    print("  poll %d: %s to %s s after binds' end = %s to %s s after set; slip_lb %s; prefill %s"
          % (p["poll"], p["s_lo"], p["s_hi"], None if p["s_lo"] is None else round(p["s_lo"] - b, 2),
             round(p["s_hi"] - b, 2), p.get("slip_lb"), p.get("render_prefill")))
print("  drift period at 5.92 ppm: %.2f s" % (1 / (48000 * 5.92e-6)))
pc = J("summary/pc/pc.json")
for n in pc["nvm"]:
    print("NVM %s/%s: pend %d dirty %d commit_busy %d commits %d image_seq %d"
          % (n["stage"], n["tag"], n["pend"], n["dirty"], n["commit_busy"], n["commits_ok"], n["image_seq"]))
for f in ("identity-postboot/console-identity.txt", "restore/dut-end2.txt"):
    m = re.search(r"\bpend=([01])", open(os.path.join(A, f)).read()); print("NVM %s: pend %s" % (f, m.group(1)))
for l in open(os.path.join(A, "runs/pc/poll-post-relock-noaction.jsonl")):
    print("post-boot poll SLIP_LB 0x%s" % json.loads(l)["words"]["0x8d4"])
m = re.search(r"0x900008d4\s+((?:[0-9a-f]{2} ){12})", open(os.path.join(A, "restore/dut-end2.txt")).read())
by = m.group(1).split(); print("end SLIP_LB dups %d; RENDER_STAT rails %d" % (int(by[1] + by[0], 16), int(by[11] + by[10], 16)))
p = J("summary/proof/proof.json")
for c in p["channels"]:
    print("proof ch%d nonzero %d range %d..%d" % (c["channel"], c["nonzero"], c["min"], c["max"]))
