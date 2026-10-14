"""Print selected members (regex) of one layer: name, mode, owner, and the first bytes."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from oci_layers import open_image, members
_, _, _, layers = open_image(sys.argv[1])
rx = re.compile(sys.argv[3]); limit = int(sys.argv[4]) if len(sys.argv) > 4 else 400
for m, c in members(layers[int(sys.argv[2])]["data"]()):
    if rx.search(m.name):
        print(f"== {m.name} type={m.type!r} size={m.size} owner={m.uid}:{m.gid}")
        print(c[:limit].decode(errors="replace"))
