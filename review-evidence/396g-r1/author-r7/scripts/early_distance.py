"""How early the listings are that the ruling's literal lower edge refuses (see literal_bound.py).

For each seed a literal_bound.py run refused, each event and channel it changes with no DUT listing whose samples
meet [first word, last word + 63] but one that ends before the first word, within 63: the distance from that
listing's last sample to the event's first word, and what lies near (other events, planted arms within 64).

usage: python3 -I -B early_distance.py <torture_campaign.py> <literal_bound out.json> <units|nested>
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r699-6-packet", "scripts"))
import probe_lib  # noqa: E402

path, report, family = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
mod = probe_lib.load(path)
t = probe_lib.case(mod)
frames, guard = report["frames"], mod.AUDIO_GUARD_FRAMES
arms = t._sweep_arms(frames)
distances, near_kinds, examples = collections.Counter(), collections.Counter(), []


def span(event):
    low, high = event.get("located_within", (event["capture_index"],) * 2)
    if event["class"] not in ("dropped", "repeated"):
        high = max(high, event["capture_index"] + event["n"] - 1)
    return low, high


for seed in report["refused_seeds"]:
    units = t._fuzz_units(frames, seed) if family == "units" else t._fuzz_nested(frames, seed)
    verdict, detail, _ = t._sweep_grade(frames, [e for u in units for e in u[4]])
    for kind, at, channels, length, _ in units:
        last = at + length - 1
        for channel in channels:
            dut = [span(e) for e in detail["events"] if e["attribution"] == "dut" and e["channel"] == channel]
            if any(high >= at and low <= last + guard for low, high in dut):
                continue
            early = [at - high for low, high in dut if at - guard <= high < at]
            if not early:
                continue
            d = min(early)
            distances[d] += 1
            others = any(u[1] != at and u[1] - 64 <= last and at <= u[1] + u[3] + 64 for u in units)
            armed = any(at - 64 <= a[1] <= last + 64 for a in arms)
            near_kinds[("another event" if others else "") + (" and " if others and armed else "")
                       + ("a planted arm" if armed else "") or "nothing"] += 1
            if len(examples) < 6:
                examples.append({"seed": seed, "event": [kind, at, length], "channel": channel, "early_by": d})
print(json.dumps({"frames": frames, "family": family, "refused_seeds": len(report["refused_seeds"]),
                  "early_by": dict(sorted(distances.items())), "within_64_of": dict(near_kinds),
                  "examples": examples}))
