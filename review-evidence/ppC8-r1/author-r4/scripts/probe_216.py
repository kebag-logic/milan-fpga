"""Scratch: a CLOCK_DOMAIN of 216 sources (Table 7-61's maximum, 508 octets)
packs; 217 (510 octets) is refused by L12 descriptor-maximum."""
import importlib.util
import struct
import sys

sys.path.insert(0, "tb/desc_store")
spec = importlib.util.spec_from_file_location("t", "tb/desc_store/test_gen_desc_image.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
mut = t.mut
for n in (216, 217):
    model = t.normalised(t.MILAN_MIN)
    for k in range(2, n):
        mut.add(model, (mut.CLOCK_SOURCE, k, 0), mut.body(model, mut.CLOCK_SOURCE, 0))
    mut.set_sources(model, list(range(n)))
    print(n, "sources, CLOCK_DOMAIN", len(mut.body(model, mut.CLOCK_DOMAIN, 0)), "octets:", end=" ")
    try:
        t.gen_desc_image.build(model)
        print("PACKED")
    except t.gen_desc_image.ImageError as exc:
        print("REFUSED:", " | ".join(str(exc).splitlines()))
