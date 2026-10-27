"""Trace channel 0 of R699-6 F1's case through the counter scan: each window close, hold, release and record.

usage: python3 -I -B trace_f1.py <torture_campaign.py> <frames> <start> <length> <mask> <kind> <slip_at> <n>
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r699-6-packet", "scripts"))
import probe_lib  # noqa: E402

mod = probe_lib.load(sys.argv[1])
t = probe_lib.case(mod)
frames, start, length, mask = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5], 0)
kind, slip_at, n = sys.argv[6], int(sys.argv[7]), int(sys.argv[8])
scan = mod._CounterScan
orig_close, orig_release, orig_record, orig_hold = scan._close, scan._release, scan._record, scan._hold


def close(self, channel, found, reason):
    if channel == 0:
        w = self.slots[0].window
        print("close", w.start, w.end(), "found", found, "reason", reason, "image",
              None if self.slots[0].image is None else (self.slots[0].image.start, hex(self.slots[0].image.mask)))
    return orig_close(self, channel, found, reason)


def release(self, channel, why):
    if channel == 0:
        img = self.slots[0].image
        print("release", why, "image start", img.start, "events",
              [(e["capture_index"], e["class"], e["n"]) for e in img.events])
    return orig_release(self, channel, why)


def record(self, channel, event):
    if channel == 0:
        print("  record", event["capture_index"], event["class"], event["n"], event.get("located_within"))
    return orig_record(self, channel, event)


def hold(self, slot, track, events, tokens, final):
    out = orig_hold(self, slot, track, events, tokens, final)
    if slot is self.slots.get(0):
        print("hold in", [(e["capture_index"], e["class"], e["n"]) for e in events], "final", final,
              "-> now", [(e["capture_index"], e["class"], e["n"]) for e in out], "image",
              None if slot.image is None else (slot.image.start, hex(slot.image.mask),
                                               [(e["capture_index"], e["class"], e["n"]) for e in slot.image.events]))
    return out


scan._close, scan._release, scan._record, scan._hold = close, release, record, hold
events = [{"kind": "flip", "index": start + k, "channel": 0, "mask": mask} for k in range(length)]
if kind != "none":
    events.append({"kind": kind, "index": slip_at, "n": n})
verdict, detail, _ = t._sweep_grade(frames, events)
print("verdict", verdict, detail.get("why"))
print(json.dumps([(e["capture_index"], e["class"], e["n"], e.get("mask")) for e in detail["events"]
                  if e["attribution"] == "dut" and e["channel"] == 0]))
