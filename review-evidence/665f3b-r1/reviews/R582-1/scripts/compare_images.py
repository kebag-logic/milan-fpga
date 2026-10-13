"""Compare reviewer-built ctrl_app ELFs (ctrl_image.py --out DIR) with the author's image-hashes.json.
usage: python3 -I compare_images.py IMAGES_DIR AUTHOR_IMAGE_HASHES_JSON"""
import hashlib, json, sys
from pathlib import Path
images, author = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
rows = {(r["composition"], r["shape"]): r for r in author}
for side, key in (("base", "before"), ("head", "after")):
    for elf in sorted((images / side).glob("*/ctrl_app.elf")):
        shape = elf.parent.name
        h = hashlib.sha256(elf.read_bytes()).hexdigest()
        a = rows.get(("ADP-ACMP-MAAP", shape), {}).get(key, {})
        print(f"{side:4} {shape:28} reviewer {h} author {a.get('elf_sha256')} {'MATCH' if h == a.get('elf_sha256') else 'DIFFER'} author_load={a.get('load')}")
