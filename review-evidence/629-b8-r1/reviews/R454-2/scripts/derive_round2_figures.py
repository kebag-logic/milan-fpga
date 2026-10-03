#!/usr/bin/env python3
"""Re-derive the figures the round-2 delta added or changed, from the
published B8 packet (review-evidence/629-b8-r1/author at 36ee6d8a).

usage: derive_round2_figures.py AUTHOR_DIR
"""
import json, os, re, sys

A = sys.argv[1]
J = lambda p: json.load(open(os.path.join(A, p)))
FPS = 48000

# CRF window: capture loss, stall clusters, positions, signatures (page :1618-1635, :1758-1760)
g = J("summary/crfll/grade.json")
w = g["window"]
lost = g["attribution"]["capture path"]["lost_frames"]
ev = [json.loads(l) for l in open(os.path.join(A, "runs/crfll/events.jsonl"))]
t0 = next(e["t"] for e in ev if e.get("kind") == "window-start")
t1 = next(e["t"] for e in ev if e.get("kind") == "window-end")
print(f"CRF window: events span {t1 - t0:.3f} s; captured {w['frames']} frames = {w['frames'] / FPS:.2f} s; "
      f"capture_lost_frames {lost} = {lost / FPS:.3f} s; captured + lost = {(w['frames'] + lost) / FPS:.2f} s")
print(f"CRF window polls: {g['polls_in_segment']} in the grade; lockloss.json window polls "
      f"{J('summary/crfll/lockloss.json')['window']['polls']}; polls missing a word "
      f"{J('summary/crfll/lockloss.json')['polls_missing_a_word']}")
cl = g["skip_clusters"]
stall = [c for c in cl if c["recent_read_gap_ms"] > 1000 and c["lost_frames"] > FPS]
before = 0
for c in cl:
    pos = (c["first_frame"] - w["start_frame"]) / FPS
    if c in stall:
        print(f"  stall cluster {c['cluster']}: read gap {c['recent_read_gap_ms'] / 1000:.2f} s, lost {c['lost_frames']} "
              f"({c['lost_ms'] / 1000:.2f} s), starts {pos:.1f} s captured / {pos + before / FPS:.1f} s with prior losses, "
              f"size_signature {c['size_signature']}, steps {c['steps'] if len(c['steps']) <= 2 else str(len(c['steps'])) + ' steps'}")
    ok = abs(c["read_rise_ms"] - c["lost_ms"]) <= 1 + 0.02 * c["lost_ms"]
    if not ok:
        print(f"  cluster {c['cluster']} FAILS the 1 ms + 2 % rise rule")
    before += c["lost_frames"]
print(f"  clusters {len(cl)}; stall clusters lost {sum(c['lost_frames'] for c in stall) / FPS:.2f} s; "
      f"all pass the rise rule: {all(abs(c['read_rise_ms'] - c['lost_ms']) <= 1 + 0.02 * c['lost_ms'] for c in cl)}")
print(f"  2172 = 48 n + 12: {(2172 - 12) % 48 == 0}")

# #645: slips around the INTERNAL-to-AAF set (page :1573-1600)
s = J("summary/sw/switches.json")
ch = s["phases"][0]["changes"]
print(f"#645: binds end {s['binds_end_s_before_first_set']:.3f} s before the set")
for c in ch:
    if "slip_lb" in c or "render_prefill" in c or "servo" in c:
        print(f"  {c['s_lo']:+.3f} to {c['s_hi']:+.3f} s: " + ", ".join(f"{k}={c[k]}" for k in ("slip_lb", "render_prefill", "servo") if k in c))
fb = s["from_binds"]
print(f"  last pre-set slip ends {fb[-1]['s_hi']:.3f} s after the binds' end")
slips = [c for c in ch if "slip_lb" in c and c["s_hi"] < 0]
print(f"  pre-set slips: {len(slips)}; greatest separation {slips[-1]['s_hi'] - slips[0]['s_lo']:.3f} s; "
      f"skips {[c['slip_lb'][1] for c in slips]}")
lk = next(c for c in ch if c.get("servo") == "LOCKED")
post = next(c for c in ch if "slip_lb" in c and c["s_lo"] > lk["s_lo"])
print(f"  post-LOCKED slip {post['s_lo'] - lk['s_hi']:.3f} to {post['s_hi'] - lk['s_lo']:.3f} s after the first LOCKED read")
print(f"  steady 5.92 ppm slip period {1 / (FPS * 5.92e-6):.3f} s")

# pend (page :1679, :1700-1701)
for l in open(os.path.join(A, "runs/pc/events.jsonl")):
    e = json.loads(l)
    if e.get("kind") == "nvm":
        d = json.dumps(e)
        vals = {m.group(1): m.group(2) for m in re.finditer(r'"(\w*(?:seq|dirty|commit_busy|pend|commits_ok))": (\d+)', d)}
        print(f"NVM {e.get('tag')}: {vals}")
for f in ("identity/console-identity.txt", "identity-resume/console-identity.txt", "runs/sw/dut-before-bind.txt",
          "runs/crfll/dut-final.txt", "restore/dut-end2.txt"):
    m = re.search(r"\bpend=(\d)", open(os.path.join(A, f)).read())
    print(f"NVM status line in {f}: pend={m.group(1)}")
# post-boot SLIP_LB (page :1721-1728)
polls = [json.loads(l) for l in open(os.path.join(A, "runs/pc/poll-post-relock-noaction.jsonl"))]
print("post-boot polls SLIP_LB:", [p.get("words", p).get("0x8d4") for p in polls])
