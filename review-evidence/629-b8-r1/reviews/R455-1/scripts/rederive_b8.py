#!/usr/bin/env python3
"""Re-derive the lane B8 page's graded figures from the published packet.

usage: rederive_b8.py <author-dir> <out.txt>
Reads summary/{sw,crfll,pc,proof}/*.json and runs/*/events.jsonl only.
"""
import json
import sys
from pathlib import Path

A, out = Path(sys.argv[1]), Path(sys.argv[2])
L = []
J = lambda p: json.loads((A / p).read_text())  # noqa: E731
EV = lambda r: [json.loads(x) for x in (A / "runs" / r / "events.jsonl").read_text().splitlines() if x.strip()]  # noqa: E731

# --- item 2: switches -------------------------------------------------------
sw = J("summary/sw/switches.json")
L.append("== SW switches")
for p in sw["phases"]:
    al = p["after_lock"]
    L.append(f"{p['tag']}: {p['from_source']}->{p['to_source']} {p['set_status']} rb={p['readback']} "
             f"LOCKED {p['set_to_locked_s']} s; clock_reads={[c['source'] for c in p['clock_reads']]}; "
             f"hold polls={al['polls']} states={al['servo_states']} trim={al['trim_ppm']} "
             f"slip_lb={al['slip_lb_first_last']} slip_tdm={al['slip_tdm_first_last']} rails={al['render_rails_first_last']}")
    for c in p["changes"]:
        L.append(f"   change {c}")
c = sw["counters"]
L.append("counter marks (CLOCK_DOMAIN L/U | DUT out0 MR | peer in0 MR | DUT in0/in1 disruptions):")
for tag in ["after-binds", "aaf1-locked", "aaf1-end", "crf-locked", "crf-end", "aaf2-locked", "aaf2-end", "final"]:
    m = c[tag]
    dis = {k: sum(v for kk, v in m[k].items() if kk != "MEDIA_LOCKED" and kk != "MEDIA_UNLOCKED") for k in ("dut-0x0005-0", "dut-0x0005-1")}
    unl = {k: m[k]["MEDIA_UNLOCKED"] for k in ("dut-0x0005-0", "dut-0x0005-1")}
    L.append(f"  {tag}: {m['dut-0x0024-0']['LOCKED']}/{m['dut-0x0024-0']['UNLOCKED']} | {m['dut-0x0006-0']['MEDIA_RESET']} | "
             f"{m['peer-0x0005-0']['MEDIA_RESET']} | other-disruption-sums={dis} MEDIA_UNLOCKED={unl}")
# one per change rule
seq = [c[t]["dut-0x0006-0"]["MEDIA_RESET"] for t in ("aaf1-before-set", "aaf1-locked", "crf-locked", "aaf2-locked")]
dom = [(c[t]["dut-0x0024-0"]["LOCKED"], c[t]["dut-0x0024-0"]["UNLOCKED"]) for t in ("aaf1-before-set", "aaf1-locked", "crf-locked", "aaf2-locked")]
L.append(f"MEDIA_RESET per change: {[b - a for a, b in zip(seq, seq[1:])]} (declared 1 each)")
L.append(f"CLOCK_DOMAIN pairs per change: {[(b[0]-a[0], b[1]-a[1]) for a, b in zip(dom, dom[1:])]} (declared (1,1) each); "
         f"invariant LOCKED-UNLOCKED in {{0,1}}: {all(l-u in (0,1) for l,u in dom)}")
mid_end_same = all(c[f"{p}-locked"] == c[f"{p}-mid"] == c[f"{p}-end"] for p in ("aaf1", "crf", "aaf2"))
L.append(f"locked/mid/end marks identical per phase: {mid_end_same}")
fb = sw["from_binds"]
L.append(f"from binds (s after binds end; binds end {sw['binds_end_s_before_first_set']} s before set): {fb}")
t = sw["tone"]
L.append(f"SW tone: {t['window']} blocks={t['tone']['blocks']} clean={t['tone']['clean_blocks']} events={t['tone']['events']} "
         f"attrib={ {k: v['lost_frames'] for k, v in t['attribution'].items()} } counted={t['counted']} "
         f"timed={t['timed_ppm']:.3f}+-{t['timed_halfwidth95_ppm']:.3f} read_gap_max={t['capture_reads']['read_gap_ms_max']}")
ev = EV("sw")
ws = next(e for e in ev if e["kind"] == "window-start"); we = next(e for e in ev if e["kind"] == "window-end")
sets = [e for e in ev if e["kind"] == "switch"]
L.append(f"SW window wall {we['t']-ws['t']:.2f} s; switches at +{[round(s['t']-ws['t'],1) for s in sets]} s from window start (inside if 0<x<{we['t']-ws['t']:.1f})")

# --- #645 data --------------------------------------------------------------
ph = sw["phases"][0]
lk = ph["set_to_locked_s"]
sl = [ch for ch in ph["changes"] if "slip_lb" in ch]
L.append("== #645: SLIP_LB changes around INTERNAL->AAF: " + str([(ch["s_lo"], ch["s_hi"], ch["slip_lb"]) for ch in sl]))
last = sl[-1]
L.append(f"post-LOCKED slip interval after first LOCKED read: {last['s_lo']-lk[1]:.3f} to {last['s_hi']-lk[0]:.3f} s")

# --- item 3: CRF window and lock loss --------------------------------------
ll = J("summary/crfll/lockloss.json")
tw = ll["tone_window"]
ev = EV("crfll")
ws = next(e for e in ev if e["kind"] == "window-start"); we = next(e for e in ev if e["kind"] == "window-end")
wall = we["t"] - ws["t"]
cl = tw["clusters"]
big = [x for x in cl if x["lost_ms"] > 1000]
L.append("== CRF window")
L.append(f"wall {wall:.3f} s; captured {tw['window']['seconds']} s; wall-captured {wall - tw['window']['seconds']:.3f} s")
L.append(f"capture-lost frames all clusters {tw['counted']['capture_lost_frames']} = {tw['counted']['capture_lost_frames']/48000:.3f} s")
L.append(f"three stall clusters lost {sum(x['lost_ms'] for x in big)/1000:.3f} s; read-time rise {sum(x['read_rise_ms'] for x in big)/1000:.3f} s; "
         f"stall gaps >1 s: {[g for g in tw['capture_reads']['stall_gaps_ms'] if g > 1000]} sum {sum(g for g in tw['capture_reads']['stall_gaps_ms'] if g > 1000)/1000:.3f} s")
L.append(f"stall clusters at captured-time {[round((x['first_frame']-tw['window']['start_frame'])/48000,1) for x in big]} s into the window; size_signature={[x['size_signature'] for x in big]}")
L.append(f"clusters={len(cl)} all capture_path={all(x['capture_path'] for x in cl)}; rise-vs-loss within 1 ms+2%: "
         f"{all(abs(x['read_rise_ms']-x['lost_ms']) <= 1 + 0.02*x['lost_ms'] for x in cl)}")
L.append(f"PAGE CLAIM: 'three read stalls ... lost 19.0 s' and 401.3 captured of 420 -> evidence gives {tw['counted']['capture_lost_frames']/48000:.2f} s (all clusters) / {sum(x['lost_ms'] for x in big)/1000:.2f} s (the three stall clusters)")
L.append(f"window: polls={ll['window']['polls']} states={ll['window']['servo_states']} trim={ll['window']['trim_ppm']} set->LOCKED={ll['set']['set_to_locked_s']} "
         f"crf_rate={ll['window']['crf_rate_ppm']} counted={tw['counted']} timed={tw['timed_ppm']:.2f}+-{tw['timed_halfwidth95_ppm']:.2f}")
L.append(f"unbind held {ll['held_s']} s; after_unbind={ll['after_unbind']}; holdover={ {k: ll['holdover'][k] for k in ('polls','servo_states','trim_ppm')} }")
L.append(f"after_rebind={ll['after_rebind']}; clock_reads={[x['source'] for x in ll['clock_reads']]}")
cc = ll["counters"]
for tag in ("ll-before", "ll-holdover", "ll-after", "final"):
    m = cc[tag]
    L.append(f"  {tag}: CD {m['dut-0x0024-0']['LOCKED']}/{m['dut-0x0024-0']['UNLOCKED']} DUT out0 MR {m['dut-0x0006-0']['MEDIA_RESET']} "
             f"DUT out1 MR {m['dut-0x0006-1']['MEDIA_RESET']} peer in0 MR {m['peer-0x0005-0']['MEDIA_RESET']} DUT in1 MEDIA_UNLOCKED {m['dut-0x0005-1']['MEDIA_UNLOCKED']}")
g = J("summary/crfll/grade-lockloss.json")
L.append(f"lock-loss segment: {g['window']} tone={ {k: g['tone'][k] for k in ('blocks','clean_blocks','events')} } counted={g['frame_rate_ratio']['counted']} read_gap_max={g['capture_reads']['read_gap_ms_max']}")

# --- item 4: power cycle ----------------------------------------------------
pc = J("summary/pc/pc.json")
L.append("== PC")
L.append(f"clock={[(x['tag'], x['source']) for x in pc['clock']]}")
L.append(f"nvm={[(x['tag'], x['image_seq'], x['commits_ok'], x['dirty'], x['commit_busy'], x['pend']) for x in pc['nvm']]} (tag, image_seq, commits, dirty, busy, pend)")
L.append(f"boot={ {k: pc['boot'][k] for k in ('first_byte_to_prompt_s',)} } milestones={pc['boot']['milestone_lines'][3:4]}")
L.append(f"polls={[(p['tag'], p['polls'], p['locked_s']) for p in pc['polls']]}; relock={pc['relock']}")
m = pc["counters"]["post-post-boot"]
L.append(f"post-boot CD {m['dut-0x0024-0']}; DUT in0 {m['dut-0x0005-0']['MEDIA_LOCKED']}/{m['dut-0x0005-0']['MEDIA_UNLOCKED']}; peer out0 START/STOP {m['peer-0x0006-0']['STREAM_START']}/{m['peer-0x0006-0']['STREAM_STOP']} vs pre {pc['counters']['pre-pre-locked']['peer-0x0006-0']}")
L.append(f"first command after strip return ~ {pc['post_first_command_t'] - (pc['boot']['first_byte'] - 0.3):.1f} s")

# --- item 1: proof ----------------------------------------------------------
pr = J("summary/proof/proof.json")
L.append("== proof: " + str([(c["channel"], c["rms_dbfs"], c["min"], c["max"], c.get("share_997"), c.get("share_9973")) for c in pr["channels"]]) + " " + pr["verdict"])
out.write_text("\n".join(L) + "\n")
print("\n".join(L))
