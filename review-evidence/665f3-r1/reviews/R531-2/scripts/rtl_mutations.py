import concurrent.futures, json, os, pathlib, subprocess, sys
p=pathlib.Path(sys.argv[1]).resolve(); copy=p/'scratch/rtl-copy'; cwd=copy/'tb/verilator/mbx'
source=copy/'hdl/milan/mailbox/KL_mbx_rx.sv'; original=source.read_text()
v=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
env=dict(os.environ,TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1')
flags='--cc --exe --build -j 4 --top-module tb_mbx_top -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I'+str(copy/'sw/firmware/ctrl/mbx')+'"'
cases=[
 ('wrong-byte-index', 'assign c_tap_w[k] = sr_r[cmp_b_w];', "assign c_tap_w[k] = sr_r[cmp_b_w ^ 3'd4];",False),
 ('stale-first-byte', "live_w[e] && eq_w[e] && (cnt_r == 11'(BO_C) || match_r[e])", "live_w[e] && (cnt_r == 11'(BO_C) ? (eq_w[e] || match_r[e]) : (eq_w[e] && match_r[e]))",False),
 ('last-entry-excluded','assign bound_hit_w = |(match_r & live_w);','assign bound_hit_w = |(match_r[NB_C-2:0] & live_w[NB_C-2:0]);',False),
 ('opposite-interface',"{1'b1, if_r} : '0;","{1'b1, (if_r ^ MBX_IF_W_C'(1))} : '0;",True)
]
def run(name,host,ifs):
    if not ifs: args=['make','-j16','run-wb' if host==0 else 'run-axil','VERILATOR='+v,'VFLAGS='+flags]
    else:
        import shlex
        gen=cwd/'obj_if2/gen'; mdir='obj_if2/obj_wb' if host==0 else 'obj_if2/obj_axil'; exe='Vmbx_wb' if host==0 else 'Vmbx_axil'
        rtl=copy/'hdl/milan/mailbox'
        names=[str(gen/'KL_mbx_pkg.sv')]+[str(rtl/n) for n in ['KL_mbx_ring.sv','KL_mbx_rx.sv','KL_mbx_tx.sv','KL_mbx_evt.sv']]+[str(gen/'KL_mbx.sv')]+[str(rtl/n) for n in ['KL_mbx_wb.sv','KL_mbx_axil.sv']]+['tb_mbx_top.sv','sim_main.cpp']
        args=[v,*shlex.split(flags.replace(str(copy/'sw/firmware/ctrl/mbx'),str(gen))),'-GHOST_P='+str(host),'--Mdir',mdir,*names,'-o',exe]
    path=p/'receipts'/('mutation-'+name+'-'+str(host)+'.log')
    with path.open('w') as f:
        f.write('Command: '+repr(args)+'\n');f.flush()
        res=subprocess.run(args,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
        build=res.returncode
        if ifs and build==0: res=subprocess.run([str(cwd/mdir/exe),str(host)],cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
    log=path.read_text(); caught=res.returncode!=0 and '[FAIL]' in log and ('Q12' in log or 'Q13' in log or 'Q14' in log)
    path.with_suffix('.rc').write_text(str(res.returncode)+'\n')
    print(name,host,'caught',caught,flush=True)
    return dict(defect=name,adapter=host,interfaces=2 if ifs else 1,rc=res.returncode,caught=caught)
results=[]
try:
    for name,old,new,ifs in cases:
        assert original.count(old)==1,(name,original.count(old))
        source.write_text(original.replace(old,new))
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results += [f.result() for f in [pool.submit(run,name,0,ifs),pool.submit(run,name,1,ifs)]]
finally: source.write_text(original)
(p/'receipts/rtl-mutations.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(int(not all(x['caught'] for x in results)))
