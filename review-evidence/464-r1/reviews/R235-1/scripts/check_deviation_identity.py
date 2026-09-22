#!/usr/bin/env python3
"""R235: the six recorded AUDIO_MAP deviations, base vs head, and exactness.

Loads avdecc/aem_maps.py KNOWN_MAP_DEVIATIONS from the base and head scratch
extracts in separate interpreters' worth of module namespaces, and the head
deployed model's deviations, then checks:
  1. head set == base set with only "AUDIO_MAP[1]" -> "AUDIO_MAP[0]" changed;
  2. every other byte of each string is identical (per-string diff);
  3. head deployed model deviations == head recorded set (both directions),
     with multiplicity (list) as well as set equality;
  4. the fixture's own deviations are NOT in the recorded set (the fixture
     cannot contaminate the allowlist) and are what the fixture docstring
     implies (output map, stream channels 2..7).
Usage: check_deviation_identity.py <scratch-root>
"""
import importlib.util
import runpy
import sys
from pathlib import Path

root = Path(sys.argv[1])


def known(tree: str) -> set[str]:
    ns = runpy.run_path(str(root / tree / "avdecc" / "aem_maps.py"),
                        init_globals=None, run_name="aem_maps_probe")
    return set(ns["KNOWN_MAP_DEVIATIONS"])


sys.path.insert(0, str(root / "base" / "avdecc"))
base_known = known("base")
sys.path[0] = str(root / "head" / "avdecc")
for m in [m for m in list(sys.modules) if m.startswith("aem_")]:
    del sys.modules[m]
head_known = known("head")

print("base recorded:", len(base_known), " head recorded:", len(head_known))
mapped = {s.replace("AUDIO_MAP[1]", "AUDIO_MAP[0]", 1) for s in base_known}
print("1. head == base with AUDIO_MAP[1]->[0] only:", mapped == head_known)
for b in sorted(base_known):
    h = b.replace("AUDIO_MAP[1]", "AUDIO_MAP[0]", 1)
    diffs = [i for i, (x, y) in enumerate(zip(b, h)) if x != y]
    assert len(b) == len(h) and len(diffs) == 1, (b, h)
print("2. every string differs from its base twin in exactly one character: True")

spec = importlib.util.spec_from_file_location(
    "gen_aem_store", root / "head" / "avdecc" / "gen_aem_store.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
M = g.build_model(g.builtin_spec())
got = M["SMAP"]["DEVIATIONS"]
print("3. deployed deviations (list):", len(got), " distinct:", len(set(got)))
print("   model - recorded:", sorted(set(got) - head_known))
print("   recorded - model:", sorted(head_known - set(got)))
print("   exact both ways:", set(got) == head_known and len(got) == len(set(got)))
print("   g.KNOWN_MAP_DEVIATIONS is aem_maps.KNOWN_MAP_DEVIATIONS set-equal:",
      set(g.KNOWN_MAP_DEVIATIONS) == head_known)

F = g.build_model(g._map_fixture())
fdev = F["SMAP"]["DEVIATIONS"]
print("4. fixture deviations:", len(fdev))
for d in fdev:
    print("   ", d[:100])
print("   fixture deviations intersect recorded set:",
      sorted(set(fdev) & head_known))
