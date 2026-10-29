"""Compare ROM packing of two generator files over many configurations.
usage: packsweep.py <base_gen.py> <head_gen.py> <n>"""
import importlib.util, random, sys

def load(path, tag):
    spec = importlib.util.spec_from_file_location(tag, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def used(m, mac, p1, clk, cease, seq, sseq):
    m.RUNTIME["p1"] = p1
    m.RUNTIME["cease_ms"] = cease
    m.set_servo_gains(clk)
    try:
        return m.build(mac, seq, sseq)[1]
    except AssertionError as e:
        return str(e)

base, head = load(sys.argv[1], "b"), load(sys.argv[2], "h")
rng = random.Random(94)
bad = same = 0
for i in range(int(sys.argv[3])):
    mac = rng.getrandbits(48) if i else 0x02A1B2C3D4E5
    p1 = rng.choice([0, 1, 127, 128, 200, 246, 247, 248, 254, 255, rng.randrange(256)])
    clk = rng.choice([2_000_000, 8_000_000, 50_000_000, 100_000_000, 125_000_000])
    cease = rng.choice([3000, 300_000, 1000, rng.randrange(1, 1 << 24)])
    seq, sseq = rng.choice([(0, 0), (0x200000, 0), (0, 0x10000)])
    b = used(base, mac, p1, clk, cease, seq, sseq)
    h = used(head, mac, p1, clk, cease, seq, sseq)
    if b == h:
        same += 1
    elif isinstance(b, int) and not isinstance(h, int):
        bad += 1
        print("REGRESSION", hex(mac), p1, clk, cease, seq, sseq, b, h)
    else:
        print("DIFF", hex(mac), p1, clk, cease, seq, sseq, b, h)
print(f"configs {sys.argv[3]}: identical used-count {same}, regressions {bad}")
