#!/usr/bin/env python3
"""Lane B7: what the attribution could absorb, per graded case (the six ways listed on the
findings page under lane B6's "What the attribution can absorb"), from a grade_b7.py grade.

usage: b7_absorb.py <grade-full.json> [...]

For each case, prints one JSON object:
  item 1  capture-path skips that are not 48 n + 12 frames, and clusters whose net loss
          (whole loops included) is not 12 x (skips) modulo 48: each could hold a one- or
          two-frame listener event merged with a capture loss (or a USB packet the
          asynchronous capture interface shortened or lengthened by one frame);
  item 2  one-frame repeats attributed to the DUT beat (lane B7 attributes none when
          SLIP_TDM is static);
  item 3  clusters that passed on the read gap and the size rule (a rise measured but not
          matching);
  item 4  clusters under 98 frames, with their read gap and measured rise;
  item 5  clusters that passed on the read gap alone (no measurable rise), with their sizes;
  item 6  multi-frame steps inside a cluster that are not 48 n + 12 (listed under item 1).
Read-only analysis; nothing here touches the bench.
"""
import json
import sys

for path in sys.argv[1:]:
    g = json.load(open(path))
    cl = [c for c in g["skip_clusters"] if c["capture_path"]]
    odd_steps, odd_net = [], []
    for c in cl:
        skips = [s for s in c["steps"] if s > 0]
        for s in c["steps"]:
            if s > 0 and s % 48 != 12:
                odd_steps.append(dict(cluster=c["cluster"], step=s, mod48=s % 48))
            if s < 0:
                odd_steps.append(dict(cluster=c["cluster"], step=s, mod48=s % 48, note="step back"))
        # one loss per skip; a cluster with no skip (a loss shown as a step back once whole loops
        # are added) is one loss
        want = (12 * max(1, len(skips))) % 48
        if c["lost_frames"] % 48 != want:
            odd_net.append(dict(cluster=c["cluster"], lost_frames=c["lost_frames"], mod48=c["lost_frames"] % 48,
                                expected_mod48=want, frames_off=((c["lost_frames"] - want + 24) % 48) - 24,
                                read_rise_ms=c["read_rise_ms"], lost_ms=c["lost_ms"], basis=c["basis"],
                                read_gap_ms=c["recent_read_gap_ms"], steps=c["steps"]))
    beat = g["attribution"].get("DUT beat", {}).get("events", 0)
    item3 = [dict(cluster=c["cluster"], steps=c["steps"], rise=c["read_rise_ms"], gap=c["recent_read_gap_ms"])
             for c in cl if c["basis"] == "read gap and 48 n + 12 size"]
    item4 = [dict(cluster=c["cluster"], lost=c["lost_frames"], rise=c["read_rise_ms"], gap=c["recent_read_gap_ms"],
                  basis=c["basis"]) for c in cl if c["lost_frames"] < 98]
    item5 = [dict(cluster=c["cluster"], steps=c["steps"], gap=c["recent_read_gap_ms"]) for c in cl if c["basis"] == "read gap"]
    notcap = [dict(cluster=c["cluster"], steps=c["steps"], rise=c["read_rise_ms"], gap=c["recent_read_gap_ms"])
              for c in g["skip_clusters"] if not c["capture_path"]]
    print(json.dumps(dict(case=g["case"], segment=g.get("segment"), clusters=len(cl),
                          skips=sum(1 for c in cl for s in c["steps"] if s > 0),
                          item1_steps_off_48n12=odd_steps, item1_clusters_net_off=odd_net,
                          item2_dut_beat_events=beat, item3_gap_and_size=item3, item4_under_98=item4,
                          item5_gap_only=item5, clusters_not_capture_path=notcap,
                          smallest_capture_loss=min((c["lost_frames"] for c in cl), default=None))))
