import hashlib,json,os,pathlib,subprocess,sys
p=pathlib.Path(sys.argv[1]).resolve();copy=p/'scratch/rtl-copy';cwd=copy/'tb/verilator/mbx'
f=copy/'sw/firmware/ctrl/app/ctrl_app.c';original=f.read_bytes(); v=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
vf='--cc --exe --build -j 4 --top-module tb_mbx_top -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I'+str(copy/'sw/firmware/ctrl/mbx')+'"'
exe=cwd/'obj_cosim/Vmbx_cosim';before=hashlib.sha256(exe.read_bytes()).hexdigest(); results=[]
try:
 for name,raw in [('mutated',original.replace(b'return cfg->acmp == NULL ||',b'return true || cfg->acmp == NULL ||')),('restored',original)]:
    assert raw!=original or name=='restored';f.write_bytes(raw)
    with (p/'receipts'/('relink-'+name+'.log')).open('w') as log:
        r=subprocess.run(['make','-j16','run-cosim','VERILATOR='+v,'VFLAGS='+vf],cwd=cwd,stdout=log,stderr=subprocess.STDOUT)
    (p/'receipts'/('relink-'+name+'.rc')).write_text(str(r.returncode)+'\n')
    after=hashlib.sha256(exe.read_bytes()).hexdigest();results.append(dict(stage=name,rc=r.returncode,binary_sha256=after,changed=before!=after));before=after
    print(name,r.returncode,flush=True)
finally:f.write_bytes(original)
(p/'receipts/relink.json').write_text(json.dumps(results,indent=2)+'\n')
assert results[0]['rc']!=0 and results[0]['changed'] and results[1]['rc']==0 and results[1]['changed']
