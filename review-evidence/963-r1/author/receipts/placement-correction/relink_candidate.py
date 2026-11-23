from pathlib import Path
import sys,os,subprocess,struct,json,hashlib
T=Path('<scratch>');root=Path('<lane>');V=T/'variants/sep_bool';O=T/'variants/relinked';O.mkdir(exist_ok=True)
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'));import ctrl_srp_image as im
cc='<home>/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-gcc';nm=cc.removesuffix('gcc')+'nm'
env=dict(os.environ,PATH='<home>/litex-milan/venv/bin:<home>/br-milan-rv32/host/bin:/usr/local/bin:/usr/bin:/bin',LITEX_ENV_CC_TRIPLE='riscv32-buildroot-linux-gnu',MAKEFLAGS='-j16 --no-print-directory')
rt=T/'meas/full/h4/8x8-1if/none/split-soc/stand-ins/runtime'
args=['<home>/litex-milan/venv/bin/python3','-B',str(root/'sw/firmware/ctrl/test/ctrl_srp_image.py'),'--config',str(root/'configs/endstation_ax7101_1x1_tdm8.yaml'),'--ctrl-source',str(V/'ctrl'),'--interfaces','1','--with-aecp','--layout','split','--output',str(V/'image-1x1'),'--libc',str(rt/'libc.a'),'--compiler-runtime',str(rt/'libcompiler_rt.a')]
with (V/'build-1x1.log').open('w') as f:r=subprocess.run(args,env=env,stdout=f,stderr=subprocess.STDOUT)
assert r.returncode==0

def segments(p):
 b=p.read_bytes();assert b[:6]==b'\x7fELF\x01\x01';phoff=struct.unpack_from('<I',b,28)[0];size,n=struct.unpack_from('<HH',b,42);assert size==32
 out={}
 for i in range(n):
  typ,off,va,pa,sz,mem,flags,align=struct.unpack_from('<IIIIIIII',b,phoff+i*size)
  if typ==1:out[pa]=b[off:off+sz]
 return out
rows=[]
for point in ['1x1','8x8-1if']:
 obj=V/('image-1x1' if point=='1x1' else 'image')/'19-aecp_maps.o'
 for build in sorted((T/'meas/full/base'/point).iterdir()):
  if not (build/'image/ctrl_app.elf').exists():continue
  out=O/point/build.name;out.mkdir(parents=True,exist_ok=True)
  old=build/'image';objs=sorted(old.glob('[0-9]*-*.o'),key=lambda p:int(p.name.split('-')[0]));objs=[obj if p.name=='19-aecp_maps.o' else p for p in objs]
  # All other objects, runtime archives and the linker contract are the original build's.
  runtime=build/'split-soc/stand-ins/runtime'
  elf,_=im.link(cc,root/'sw/firmware/ctrl',out,objs,[runtime/'libc.a',runtime/'libcompiler_rt.a'],'split')
  im.verify_abi(cc,elf,'rv32im');im.hot_list(root/'sw/firmware/ctrl',out/'ctrl_app.map','split')
  a,b=segments(old/'ctrl_app.elf'),segments(elf);syms=subprocess.check_output([nm,'-S',str(old/'ctrl_app.elf')],text=True)
  sym=next(x.split() for x in syms.splitlines() if x.endswith(' aecp_map_command'));start,size=int(sym[0],16),int(sym[1],16)
  same_layout=set(a)==set(b) and all(len(v)==len(b[k]) for k,v in a.items());dif=[]
  if same_layout:
   for k,v in a.items():dif.extend(k+i for i,(x,y) in enumerate(zip(v,b[k])) if x!=y)
  row={'point':point,'arm':build.name,'same_load_layout':same_layout,'only_map_command':same_layout and all(start<=x<start+size for x in dif),'changed_bytes':len(dif),'map_start':hex(start),'map_bytes':size,'elf_sha256':hashlib.sha256(elf.read_bytes()).hexdigest()};rows.append(row);print(row,flush=True)
(O/'proof.json').write_text(json.dumps(rows,indent=1)+'\n')
