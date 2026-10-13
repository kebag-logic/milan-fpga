"""The image table: every ELF of two manifests (sha256sum lines), side by side. usage: image_table.py <dev> <head>"""
import sys
from pathlib import Path


def read(path):
    rows = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        digest, name = line.split(maxsplit=1)
        rows[name.removeprefix("./").removesuffix("/ctrl_app.elf")] = digest
    return rows


dev, head = read(sys.argv[1]), read(sys.argv[2])
print("| Image (shape) | dev `c20c85bd` sha256 | head `a8fe548a` sha256 | |")
print("|---|---|---|---|")
for name in sorted(dev.keys() | head.keys()):
    a, b = dev.get(name, "-"), head.get(name, "-")
    print(f"| `{name}` | `{a[:16]}…` | `{b[:16]}…` | {'same' if a == b else 'DIFFERS'} |")
print(f"\n{sum(dev.get(n) == head.get(n) for n in dev | head)} of {len(dev.keys() | head.keys())} identical")
