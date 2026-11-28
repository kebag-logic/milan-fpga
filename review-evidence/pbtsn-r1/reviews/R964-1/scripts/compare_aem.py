#!/usr/bin/env python3
"""Compare the model dump at the reviewed head with the published firmware image dump.

Usage: compare_aem.py <model-dump> <firmware-image-dump>
Lines are "label_type label_index length hex".  The comparison is on the descriptor bytes, keyed by the type
and index the bytes themselves carry (octets 0..3), not by the label columns.
"""
import sys, zlib

def load(path):
    out, labels = {}, []
    for line in open(path):
        t, i, n, h = line.split()
        b = bytes.fromhex(h)
        assert len(b) == int(n), (path, t, i)
        key = (int.from_bytes(b[0:2], 'big'), int.from_bytes(b[2:4], 'big'))
        assert key not in out, key
        out[key] = b
        labels.append(((int(t), int(i)), key))
    return out, labels

model, ml = load(sys.argv[1])
image, il = load(sys.argv[2])
same = sum(1 for k in model if image.get(k) == model[k])
print(f"model descriptors {len(model)}, image descriptors {len(image)}, identical by own type/index {same}")
print("key sets equal:", set(model) == set(image))
for name, labels in (("model", ml), ("image", il)):
    bad = [(l, k) for l, k in labels if l != k]
    print(f"{name}: label columns differing from the descriptor's own type/index: {len(bad)} {bad}")
order = [k for _, k in ml]
blob = b''.join(model[k] for k in order)
print(f"model bytes {len(blob)} crc32 0x{zlib.crc32(blob):08x} (model emission order)")
blob = b''.join(image[k] for k in order)
print(f"image bytes {len(blob)} crc32 0x{zlib.crc32(blob):08x} (same order)")
sys.exit(0 if same == len(model) == len(image) == 84 else 1)
