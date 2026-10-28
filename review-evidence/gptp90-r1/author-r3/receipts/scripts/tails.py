"""List flags-write/COMMIT/END tails in every program of the generator."""
import sys, importlib.util
spec = importlib.util.spec_from_file_location("g", sys.argv[1])
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
g.RUNTIME["cease_ms"] = 300000; g.RUNTIME["p1"] = 248; g.set_servo_gains(100_000_000)
g.build(0x02A1B2C3D4E5)
fns = [("fixed%d" % b, b, fn) for b, fn in [(16,g.prog_rx_sync),(64,g.prog_rx_followup),(128,g.prog_rx_announce),(192,g.prog_rx_pdreq),(256,g.prog_rx_pdresp),(320,g.prog_rx_pdrfu),(384,g.prog_rx_signal),(448,g.prog_tx_ts),(704,g.prog_tb_battery)]]
fns += [(n, g.LB[n], fn) for n, fn in g.LEG_FNS]
for name, base, fn in fns:
    p = fn(base); addr = base; ins = []
    for it in p.items:
        if it[0] == "label": continue
        ins.append((addr, it[0], it[1], it[2])); addr += 1
    for i in range(len(ins) - 2):
        a, op, kw, lb = ins[i]
        if op == "WRST" and kw.get("imm") == (g.RG_PUB | 2) and ins[i+1][1] == "COMMIT" and ins[i+2][1] == "END":
            print(f"{name}@{a}: WRST ra={kw.get('ra')} ->PUB2; COMMIT; END   (prev: {ins[i-1][1]} {ins[i-1][2]})")
        if op == "COMMIT" and ins[i+1][1] == "END":
            print(f"  {name}@{a}: COMMIT; END")
print("regs", {k: getattr(g, k) for k in dir(g) if len(k) == 2 and k[0] == 'R' and isinstance(getattr(g, k), int)})
