from pathlib import Path
import json,subprocess,time,hashlib
OUT=Path(__file__).resolve().parent
TREE=OUT/'tree'
SEED=Path('$VALIDATION_STORAGE/yosys-seed-52711029/cache-build')
rows=[]
def run(name,args):
    start=time.monotonic()
    with (OUT/(name+'.log')).open('w') as log:
        result=subprocess.run(args,cwd=TREE,stdout=log,stderr=subprocess.STDOUT)
    text=(OUT/(name+'.log')).read_text()
    rows.append(dict(name=name,command=args,exit_code=result.returncode,seconds=round(time.monotonic()-start,3),cache_hit='(result cache)' in text))
    (OUT/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
base=['bash','syn/yosys/run.sh','--top','KL_pp_shadow','--no-structural']
run('01-original-warm',base+['--cache',str(OUT/'warm-cache'),'--cache-seed',str(SEED)])
assert rows[-1]['exit_code']==0 and rows[-1]['cache_hit'],rows
p=TREE/'protocol-processor/hdl/aecp/ucode/gen_ucode.py'
original=p.read_bytes()
mutant=b"import pathlib,sys\npathlib.Path(sys.argv[sys.argv.index('-o')+1]).write_text('INVALID_ROM_DATA\\n')\n"
(OUT/'generator-original.sha256').write_text(hashlib.sha256(original).hexdigest()+'\n')
(OUT/'generator-mutant.py').write_bytes(mutant)
try:
    p.write_bytes(mutant)
    run('02-malformed-ROM-cached',base+['--cache',str(OUT/'mutant-cache'),'--cache-seed',str(SEED)])
    run('03-malformed-ROM-uncached',base)
finally:
    p.write_bytes(original)
receipt=dict(head='52711029f374650dc93830d5ea28e81cb5c8f410',tree='31ddc6b5615ff91ceed7a6b52afca61c5fb9653d',results=rows,source_restored=p.read_bytes()==original,demonstrates_false_cached_pass=rows[1]['exit_code']==0 and rows[1]['cache_hit'] and rows[2]['exit_code']!=0)
(OUT/'complete.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
