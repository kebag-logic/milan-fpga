"""Print PUBFLAGS and decode the words at it and in SRTO."""
import sys, importlib.util
spec = importlib.util.spec_from_file_location("g", sys.argv[1])
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
seq = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0
g.RUNTIME["cease_ms"] = 3000; g.RUNTIME["p1"] = 248; g.set_servo_gains(2_000_000)
rom, used = g.build(0x02A1B2C3D4E5, seq)
inv = {v: k for k, v in g.OPS.items()}
def dec(w):
    return (inv[w >> 43], (w >> 39) & 15, (w >> 35) & 15, (w >> 31) & 15, (w >> 28) & 7, (w >> 24) & 15, hex(w & 0xFFFFFF))
print("PUBFLAGS", g.LB["PUBFLAGS"], "PDPAIR", g.LB["PDPAIR"])
for a in range(g.LB["PUBFLAGS"], g.LB["PUBFLAGS"] + 3): print(a, dec(rom[a]))
for a in range(g.LB["SRTO"], g.LB["SRTO"] + 11): print(a, dec(rom[a]))
