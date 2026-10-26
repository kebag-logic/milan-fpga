#!/usr/bin/env python3
"""Re-export all five shipped configurations at base and head, without synthesis."""
import hashlib,json,os,pathlib,re,shutil,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parent
work=packet/'scratch/exports'; work.mkdir(parents=True,exist_ok=True)
tree=work/'tree'; litex=pathlib.Path(os.environ.get('REVIEW_LITEX',str(pathlib.Path.home()/'litex-milan')))
python=litex/'venv/bin/python3'
env=dict(os.environ,PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(work),
         PYTHONPATH=str(litex/'litex')+':'+str(litex/'migen'),
         PATH=str(pathlib.Path(os.environ.get('REVIEW_RV32_BIN',str(pathlib.Path.home()/'br-milan-rv32/host/bin'))))+':'+str(litex/'venv/bin')+':'+os.environ['PATH'])
def run(cmd,cwd=root):
    r=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if r.returncode: raise RuntimeError(str(cmd)+'\n'+r.stdout[-6000:])
    return r.stdout
if not tree.exists():
    run(['git','clone','--shared','--no-hardlinks',root,tree])
    for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
        run(['git','config','submodule.'+sub+'.url',root/sub],tree)
        run(['git','-c','protocol.file.allow=always','submodule','update','--init',sub],tree)
head='44d95625bde2c46d7070c090fc29ed0ba85ab64a'
base='e76a755afc0536453161e3cd33f6f4d2dcd7641f'
configs=sorted(p.stem for p in (tree/'configs').glob('*.yaml'))
for label,rev in [('base',base),('head',head)]:
    run(['git','checkout','--detach',rev],tree)
    for config in configs:
        run([python,'sw/builder/endstation_builder.py','configs/'+config+'.yaml'],tree)
        argv=json.loads((tree/'sw/builder/out'/config/'soc_params.json').read_text())['argv']
        if config.startswith('endstation_arty'):
            argv[argv.index('--sys-clk-freq')+1]='100e6'
        out=work/('out-'+config)
        result=run([python,'milan_soc.py',*argv,'--entity-gen-dir',tree/'configs/generated'/config,
                    '--vivado-max-threads','16','--no-compile-software','--output-dir',out],tree/'sw/litex')
        (work/(label+'-'+config+'.log')).write_text(result)
        out.rename(work/(label+'-'+config))
        print(label,config,'export complete',flush=True)
stamp=re.compile(rb'\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}')
def normal(data,path):
    lines=[x for x in data.split(b'\n') if not stamp.search(x)]
    if path.endswith('.v'):
        box=('│','├','└'); hierarchy=[]; rest=[]
        for line in lines:
            if line.decode(errors='replace').lstrip().startswith(box):
                hierarchy.append(line.replace('└'.encode(),'├'.encode()))
            else: rest.append(line)
        lines=rest+sorted(hierarchy)
    return b'\n'.join(lines)
rows=[]
for config in configs:
    sides=[]; raw=[]
    for label in ['base','head']:
        top=work/(label+'-'+config)
        files={str(p.relative_to(top)):p.read_bytes() for p in top.rglob('*') if p.is_file() and p.name!='litex.log'}
        raw.append(files); sides.append({k:normal(v,k) for k,v in files.items()})
    assert sides[0]==sides[1],(config, [k for k in set(sides[0])|set(sides[1]) if sides[0].get(k)!=sides[1].get(k)])
    digest=hashlib.sha256()
    for k,v in sorted(sides[0].items()): digest.update(k.encode()+b'\0'+hashlib.sha256(v).digest())
    row={'config':config,'files':len(sides[0]),'normalized_sha256':digest.hexdigest(),
         'raw_identical':sum(raw[0][k]==raw[1][k] for k in raw[0]),
         'raw_differences':[k for k in raw[0] if raw[0][k]!=raw[1][k]]}
    rows.append(row); print(row,flush=True)
(packet/'export-digests.json').write_text(json.dumps({'base':base,'head':head,'software_compiled':False,'configs':rows},indent=2)+'\n')
