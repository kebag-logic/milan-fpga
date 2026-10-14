"""Pair two images' rootfs layers with their history and report which differ."""
import json, sys
a, b = (json.load(open(p))[0] for p in sys.argv[1:3])
print("A id", a["Id"], "size", a["Size"]); print("B id", b["Id"], "size", b["Size"])
la, lb = a["RootFS"]["Layers"], b["RootFS"]["Layers"]
print("layers", len(la), len(lb))
for i, (x, y) in enumerate(zip(la, lb)):
    print(i, "SAME" if x == y else "DIFF", x[7:19], y[7:19])
print("Created", a["Created"], b["Created"])
for k in ("Env", "Labels", "User", "WorkingDir", "Cmd", "Entrypoint"):
    print(k, json.dumps(a["Config"].get(k)), "SAME" if a["Config"].get(k) == b["Config"].get(k) else "DIFF")
