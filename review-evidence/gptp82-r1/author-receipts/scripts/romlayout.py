import sys, importlib.util
spec = importlib.util.spec_from_file_location("g", sys.argv[1])
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
for args in [dict(), dict(seq_seed=0x200000), dict(sync_seq_seed=0x10000)]:
    g.set_servo_gains(2000000); g.RUNTIME["cease_ms"]=3000
    rom, used = g.build(0x02A1B2C3D4E5, **args)
    fixed = [16,64,128,192,256,320,384,448,512,704]
    occ = [False]*1024
    progs = [(16,g.prog_rx_sync),(64,g.prog_rx_followup),(128,g.prog_rx_announce),(192,g.prog_rx_pdreq),(256,g.prog_rx_pdresp),(320,g.prog_rx_pdrfu),(384,g.prog_rx_signal),(448,g.prog_tx_ts),(512,lambda b: g.prog_tmr(b,0x02A1B2C3D4E5,args.get('seq_seed',0),args.get('sync_seq_seed',0))),(704,g.prog_tb_battery)] + [(g.LB[n],fn) for n,fn in g.LEG_FNS]
    for b,fn in progs:
        n=len(fn(b).words())
        for i in range(b,b+n): occ[i]=True
    free=[i for i in range(1024) if not occ[i]]
    print(args, "used", used, "free", free, "tmr", len(progs[8][1](512).words()))
