#!/usr/bin/env python3
"""R235: bind each head AUDIO_MAP refusal vector to the line that raised it.

Re-applies the head self-test's vectors (copied from a769d9db
avdecc/gen_aem_store.py _selftest_map_bounds) to fresh _map_fixture() specs,
captures the ValueError, and reports the innermost aem_maps.py frame that
raised it plus the source line, so each cause oracle is shown to bind to
exactly one raise site (the bound it names). Also counts, over every raise
site in avdecc/*.py, how many ValueError message templates contain each
oracle fragment's leading literal.
Run inside the head extract: python3 -B -E -s <this>
"""
import ast
import linecache
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "avdecc"))
import gen_aem_store as g  # noqa: E402

V = [
    ("global cluster index", lambda s: s["audio_maps"].__setitem__(1, [[0, c, 8 + c, 0] for c in range(8)]),
     "cluster_offset 8 >= this port's number_of_clusters"),
    ("base_map=7", lambda s: s["ports_out"][0].update(base_map=7),
     "base_map=7 names an AUDIO_MAP this model does not define"),
    ("maps=2", lambda s: s["ports_out"][0].update(maps=2), "declares number_of_maps=2"),
    ("cluster_channel", lambda s: s["audio_maps"][0].__setitem__(0, [0, 0, 0, 1]),
     "cluster_channel 1 >= channel_count"),
    ("stream_index", lambda s: s["audio_maps"][0].__setitem__(0, [9, 0, 0, 0]),
     "stream_index 9 >= the 2 stream descriptors"),
    ("INPUT dup", lambda s: s["audio_maps"][0].__setitem__(1, [0, 0, 0, 0]), "for a STREAM_PORT_INPUT"),
    ("CRF sink", lambda s: s["audio_maps"][0].__setitem__(0, [1, 0, 0, 0]),
     "advertises no audio format with channels"),
    ("OUTPUT dup", lambda s: s["audio_maps"].__setitem__(1, [[0, 0, 0, 0], [0, 0, 1, 0]]),
     "for a STREAM_PORT_OUTPUT"),
    ("63 mappings", lambda s: s["audio_maps"].__setitem__(1, [[0, c, c % 8, 0] for c in range(63)]),
     "has 63 mappings"),
]

for name, mutate, cause in V:
    spec = g._map_fixture()
    mutate(spec)
    try:
        g.build_model(spec)
        print(f"{name:22s} BUILT (unexpected)")
        continue
    except ValueError as e:
        frames = [f for f in traceback.extract_tb(e.__traceback__)]
        site = frames[-1]
        # the `if` guarding this raise: walk back to the nearest `if ` line
        ln = site.lineno
        guard = ""
        for k in range(ln, max(ln - 12, 0), -1):
            src = linecache.getline(site.filename, k).strip()
            if src.startswith(("if ", "elif ")):
                guard = f"{k}: {src}"
                break
        print(f"{name:22s} oracle={'MATCH' if cause in str(e) else 'MISS'}  "
              f"raised {Path(site.filename).name}:{site.lineno} in {site.name}()  guard {guard}")

# static: which raise statements in avdecc/*.py could carry each fragment?
frag_heads = {c: c.split(" ")[0] for _, _, c in V}
raises = []
for p in sorted((Path.cwd() / "avdecc").glob("*.py")):
    tree = ast.parse(p.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) \
                and getattr(node.exc.func, "id", "") == "ValueError":
            parts = []
            for a in node.exc.args:
                for sub in ast.walk(a):
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                        parts.append(sub.value)
            raises.append((p.name, node.lineno, " ".join(parts)))
print(f"\nValueError raise sites scanned in avdecc/*.py: {len(raises)}")
checks = {
    "cluster_offset ... >= this port's number_of_clusters": ("cluster_offset", "number_of_clusters"),
    "base_map= ... names an AUDIO_MAP this model does not define": ("names an AUDIO_MAP this model does", ),
    "declares number_of_maps=": ("declares number_of_maps=",),
    "cluster_channel ... >= channel_count": ("cluster_channel", ">= channel_count"),
    "stream_index ... >= the ... stream descriptors": ("stream descriptors this direction has",),
    "for a STREAM_PORT_INPUT": ("for a STREAM_PORT_INPUT",),
    "advertises no audio format with channels": ("advertises no audio format with channels",),
    "for a STREAM_PORT_OUTPUT": ("for a STREAM_PORT_OUTPUT",),
    "has ... mappings": (" mappings; 1722.1-2021 Table 7-32",),
}
for label, needles in checks.items():
    hits = [(f, ln) for f, ln, txt in raises if all(n in txt for n in needles)]
    print(f"  {label:58s} raise sites carrying it: {len(hits)} {hits}")
