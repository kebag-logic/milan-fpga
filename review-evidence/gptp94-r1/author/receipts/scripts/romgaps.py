"""Print fixed-program sizes, leg sizes and the free ROM addresses for one
generator configuration. usage: romgaps.py <gen_gptp_ucode.py> [gen args...]"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("gen", sys.argv[1])
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
args = sys.argv[2:]
def opt(name, default, conv=lambda s: int(s, 0)):
    return conv(args[args.index(name) + 1]) if name in args else default
g.RUNTIME["cease_ms"] = opt("--cease-ms", 300000)
g.RUNTIME["p1"] = opt("--p1", 248)
g.set_servo_gains(opt("--clk-hz", 100000000))
seq, sseq = opt("--seq-seed", 0), opt("--sync-seq-seed", 0)
rom, used = g.build(0x02A1B2C3D4E5, seq, sseq)
fixed = [(16, g.prog_rx_sync), (64, g.prog_rx_followup), (128, g.prog_rx_announce),
         (192, g.prog_rx_pdreq), (256, g.prog_rx_pdresp), (320, g.prog_rx_pdrfu),
         (384, g.prog_rx_signal), (448, g.prog_tx_ts),
         (512, lambda b: g.prog_tmr(b, 0x02A1B2C3D4E5, seq, sseq)), (704, g.prog_tb_battery)]
owned = [False] * g.DEPTH
for b, fn in fixed:
    n = len(fn(b).words()); print("fixed", b, n)
    for i in range(n): owned[b + i] = True
for name, fn in g.LEG_FNS:
    n = len(fn(g.LB[name]).words()); print("leg", name, g.LB[name], n)
    for i in range(n): owned[g.LB[name] + i] = True
owned[1022] = owned[1023] = True
print("used", used, "free", [i for i in range(g.DEPTH) if not owned[i]])
