#!/usr/bin/env python3
"""Replay every ORIGINAL _selftest_map_bounds vector (dev ec34fcde) against
the CURRENT builtin_spec() and report outcome, exception class and message.

Read-only: imports avdecc/ from the checkout named by argv[1], writes nothing.
Usage: python3 probe_original_arms.py <checkout>
"""
import sys
import traceback
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "avdecc"))
import gen_aem_store as g  # noqa: E402

# (label, expectation, mutate) copied verbatim from the base-head self-test.
ARMS = [
    ("global cluster index where 7.2.19 wants a port-relative offset", "refuse",
     lambda s: s["audio_maps"].__setitem__(
         1, [[0, c, 8 + c, 0] for c in range(8)])),
    ("base_map naming an AUDIO_MAP the model does not define", "refuse",
     lambda s: s["ports_out"][0].update(base_map=7)),
    ("number_of_maps != 1 on a static port", "refuse",
     lambda s: s["ports_out"][0].update(maps=2)),
    ("cluster_channel past the cluster's channel_count (7.2.16)", "refuse",
     lambda s: s["audio_maps"][0].__setitem__(0, [0, 0, 0, 1])),
    ("stream_index past the descriptors this direction has (7.2.13)", "refuse",
     lambda s: s["audio_maps"][0].__setitem__(0, [9, 0, 0, 0])),
    ("INPUT: two mappings onto the SAME cluster channel (7.2.19)", "refuse",
     lambda s: s["audio_maps"][0].__setitem__(1, [0, 0, 0, 0])),
    ("a mapping onto the CRF sink, which carries no audio channels", "refuse",
     lambda s: s["audio_maps"][0].__setitem__(0, [1, 0, 0, 0])),
    ("OUTPUT: the same (stream_index, stream_channel) twice", "refuse",
     lambda s: s["audio_maps"].__setitem__(1, [[0, 0, 0, 0], [0, 0, 1, 0]])),
    ("OUTPUT: the same cluster_offset twice IS allowed", "accept",
     lambda s: s["audio_maps"].__setitem__(1, [[0, 0, 0, 0], [0, 1, 0, 0]])),
    ("more mappings in one AUDIO_MAP than Table 7-32 allows (62)", "refuse",
     lambda s: s["audio_maps"].__setitem__(
         0, [[0, c % 8, c, 0] for c in range(63)])),
]

spec = g.builtin_spec()
print("current builtin geometry:")
print("  ports_in  =", spec["ports_in"])
print("  ports_out =", spec["ports_out"])
print("  audio_maps: %d map(s)" % len(spec["audio_maps"]))
print("  stream_inputs =", [(s["name"], s["kind"]) for s in spec["stream_inputs"]])
print("  stream_outputs =", [s["name"] for s in spec["stream_outputs"]])
print()
for label, want, mutate in ARMS:
    s = g.builtin_spec()
    try:
        mutate(s)
    except Exception as e:  # the fixture itself cannot be built
        print(f"[{want:6}] {label}\n   MUTATION CRASHED: {type(e).__name__}: {e}")
        continue
    try:
        g.build_model(s)
        print(f"[{want:6}] {label}\n   BUILT")
    except Exception as e:
        print(f"[{want:6}] {label}\n   {type(e).__name__}: {str(e)[:260]}")

print()
M = g.build_model(g.builtin_spec())
got = sorted(M["SMAP"]["DEVIATIONS"])
rec = sorted(g.KNOWN_MAP_DEVIATIONS)
print(f"deployed deviations: {len(got)}; recorded: {len(rec)}; "
      f"equal: {got == rec}")
for d in got:
    print("  got :", d)
for d in rec:
    print("  rec :", d)
