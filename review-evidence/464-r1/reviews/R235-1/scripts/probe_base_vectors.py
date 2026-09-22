#!/usr/bin/env python3
"""R235: replay the BASE self-test's AUDIO_MAP vectors (copied verbatim from
88e9276b avdecc/gen_aem_store.py) against the base deployed model, one at a
time, and report what each one actually raised. Also reports the base
KNOWN_MAP_DEVIATIONS against the deployed model's deviations.

Run from inside a scratch extract of the BASE tree:
  cd <scratch>/base && python3 -B -E -s <this>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "avdecc"))
import gen_aem_store as g  # noqa: E402

BASE_VECTORS = [
    ("global_index", lambda s: s["audio_maps"].__setitem__(
        1, [[0, c, 8 + c, 0] for c in range(8)]),
     "cluster_offset", True),
    ("base_map=7", lambda s: s["ports_out"][0].update(base_map=7),
     "base_map=7 names", True),
    ("maps=2", lambda s: s["ports_out"][0].update(maps=2),
     "number_of_maps=2", True),
    ("cluster_channel", lambda s: s["audio_maps"][0].__setitem__(0, [0, 0, 0, 1]),
     "cluster_channel 1 >= channel_count", True),
    ("stream_index", lambda s: s["audio_maps"][0].__setitem__(0, [9, 0, 0, 0]),
     "stream_index 9 >=", True),
    ("INPUT dup", lambda s: s["audio_maps"][0].__setitem__(1, [0, 0, 0, 0]),
     "for a STREAM_PORT_INPUT", True),
    ("CRF sink", lambda s: s["audio_maps"][0].__setitem__(0, [1, 0, 0, 0]),
     "advertises no audio format with channels", True),
    ("OUTPUT dup", lambda s: s["audio_maps"].__setitem__(
        1, [[0, 0, 0, 0], [0, 0, 1, 0]]), "for a STREAM_PORT_OUTPUT", True),
    ("OUTPUT same cluster_offset (accept)", lambda s: s["audio_maps"].__setitem__(
        1, [[0, 0, 0, 0], [0, 1, 0, 0]]), None, False),
    ("63 mappings", lambda s: s["audio_maps"].__setitem__(
        0, [[0, c % 8, c, 0] for c in range(63)]), "has 63 mappings", True),
]


def run(name, mutate, cause, must_refuse):
    spec = g.builtin_spec()
    try:
        mutate(spec)
    except Exception as e:  # the vector could not even be applied
        return f"{name:40s} VECTOR-APPLY {type(e).__name__}: {e}"
    try:
        g.build_model(spec)
    except ValueError as e:
        tag = "OWN-CAUSE" if (cause and cause in str(e)) else "OTHER-CAUSE"
        return f"{name:40s} REFUSED {tag}: {str(e)[:120]}"
    except Exception as e:
        return f"{name:40s} CRASH {type(e).__name__}: {e}"
    return f"{name:40s} BUILT" + ("  <- expected refusal" if must_refuse else "")


print("base builtin: ports_in", g.builtin_spec()["ports_in"])
print("base builtin: ports_out", g.builtin_spec()["ports_out"])
print("base builtin: n audio_maps", len(g.builtin_spec()["audio_maps"]))
for v in BASE_VECTORS:
    print(run(*v))

M = g.build_model(g.builtin_spec())
got = set(M["SMAP"]["DEVIATIONS"])
known = set(g.KNOWN_MAP_DEVIATIONS)
print(f"deployed deviations: {len(got)}; recorded: {len(known)}; "
      f"new(not recorded): {len(got - known)}; stale(recorded, absent): "
      f"{len(known - got)}")
for d in sorted(got):
    print("  model:", d[:90])
for d in sorted(known):
    print("  recorded:", d[:90])
