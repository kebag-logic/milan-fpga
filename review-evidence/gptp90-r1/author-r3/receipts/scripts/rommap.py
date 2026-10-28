"""Print fixed program sizes, leg sizes, placements and remaining gaps."""
import sys, importlib.util
spec = importlib.util.spec_from_file_location("g", sys.argv[1])
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
args = sys.argv[2:]
p1 = 248; seq = 0; sseq = 0; clk = 100_000_000; cease = 300_000
i = 0
while i < len(args):
    a = args[i]; v = args[i+1]; i += 2
    if a == "--p1": p1 = int(v)
    elif a == "--seq-seed": seq = int(v, 0)
    elif a == "--sync-seq-seed": sseq = int(v, 0)
    elif a == "--clk-hz": clk = int(v)
    elif a == "--cease-ms": cease = int(v)
g.RUNTIME["cease_ms"] = cease; g.RUNTIME["p1"] = p1; g.set_servo_gains(clk)
rom, used = g.build(0x02A1B2C3D4E5, seq, sseq)
fixed = [16,64,128,192,256,320,384,448,512,704]
occ = [False]*g.DEPTH
progs = []
fns = {16:g.prog_rx_sync,64:g.prog_rx_followup,128:g.prog_rx_announce,192:g.prog_rx_pdreq,256:g.prog_rx_pdresp,320:g.prog_rx_pdrfu,384:g.prog_rx_signal,448:g.prog_tx_ts,512:lambda b: g.prog_tmr(b,0x02A1B2C3D4E5,seq,sseq),704:g.prog_tb_battery}
for b,fn in fns.items(): progs.append((b, len(fn(b).words()), f"fixed{b}"))
for n,fn in g.LEG_FNS: progs.append((g.LB[n], len(fn(g.LB[n]).words()), n))
for b,sz,n in progs:
    for k in range(b,b+sz): occ[k]=True
occ[g.DEPTH-1]=occ[g.DEPTH-2]=True
print("used", used)
for b,sz,n in sorted(progs): print(f"{b:5d}..{b+sz-1:5d} {sz:4d} {n}")
free=[]; k=0
while k<g.DEPTH:
    if not occ[k]:
        s=k
        while k<g.DEPTH and not occ[k]: k+=1
        free.append((s,k-s))
    else: k+=1
print("free", free)
