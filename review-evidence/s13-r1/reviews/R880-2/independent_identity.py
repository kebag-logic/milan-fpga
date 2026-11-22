#!/usr/bin/env python3
"""Independent operand audit. Usage: independent_identity.py public-s13-directory checkout.
Reads published operands only; no author replay imports, builds or writes.
"""
import binascii, gzip, hashlib, json, lzma, pathlib, struct, subprocess, sys
pub, repo=map(pathlib.Path,sys.argv[1:]); root=pub/'author-r2/receipts/identity'
missing=[]
def read(p):
 if not p.exists(): missing.append(str(p.relative_to(root))); print('MISSING',p.relative_to(root)); return None
 b=p.read_bytes()
 return lzma.decompress(b) if p.suffix=='.xz' else gzip.decompress(b) if p.suffix=='.gz' else b
def h(b): return hashlib.sha256(b).hexdigest()
def diff(a,b):
 assert len(a)==len(b)
 return [i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
def jdiff(a,b,path=''):
 if type(a)!=type(b): return [(path,a,b)]
 if isinstance(a,dict):
  assert a.keys()==b.keys(),path
  return sum((jdiff(a[k],b[k],path+'/'+k) for k in a),[])
 if isinstance(a,list):
  assert len(a)==len(b),path
  return sum((jdiff(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [(path,a,b)]
rows=json.loads((pub/'MANIFEST.json').read_text()); checked=0
for row in rows:
 if not row['file'].startswith(('author-r1/receipts/','author-r2/')): continue
 p=pub/row['file']
 assert p.exists(),row['file']
 assert h(p.read_bytes())==row['published_sha256'],row['file']
 checked+=1
print('PUBLIC OUTER MANIFEST hashes match',checked,'entries')
for line in (root/'MANIFEST.sha256').read_text().splitlines():
 digest,name=line.split(None,1); name=name.strip(); p=root/name
 if p.exists(): assert h(p.read_bytes())==digest,name
 else: missing.append(name); print('MANIFEST MISSING',name)
print('Packet commit signature present:',b'gpgsig ' in subprocess.check_output(['git','cat-file','commit','491ffed7fa0a1e1f502606a7bc23d2cecfce5127'],cwd=repo).split(b'\n\n')[0])

def headers(data):
 off=2+int.from_bytes(data[:2],'big'); assert data[off:off+2]==b'\0\1'; off+=2
 fields={}
 while True:
  tag=chr(data[off]); off+=1; width=4 if tag=='e' else 2
  n=int.from_bytes(data[off:off+width],'big'); off+=width
  if tag=='e': assert n==len(data)-off; return fields,off
  fields[tag]=(off,data[off:off+n]); off+=n

def elfdata(data):
 assert data[:6]==b'\x7fELF\x01\x01'
 shoff=struct.unpack_from('<I',data,32)[0]; sz,num,strings=struct.unpack_from('<HHH',data,46)
 sec=[struct.unpack_from('<10I',data,shoff+i*sz) for i in range(num)]
 symbols={}
 for s in sec:
  if s[1]!=2: continue
  st=sec[s[6]]
  for off in range(s[4],s[4]+s[5],s[9]):
   no,addr,size,info,other,index=struct.unpack_from('<IIIBBH',data,off)
   name=data[st[4]+no:data.index(b'\0',st[4]+no)].decode()
   if index<len(sec): symbols[name]=(sec[index][4]+addr-sec[index][3],addr,size)
 phoff=struct.unpack_from('<I',data,28)[0]; psz,pnum=struct.unpack_from('<HH',data,42)
 loads=[struct.unpack_from('<8I',data,phoff+i*psz) for i in range(pnum)]
 return symbols,[s for s in loads if s[0]==1]

def elfcheck(a,b,label,ae=None):
 sa,pa=elfdata(a); sb,pb=elfdata(b); assert sa==sb and pa==pb
 e,addr,size=sa['aecp_entity_image']; aa=a[e:e+size]; bb=b[e:e+size]
 assert diff(aa,bb)==[0x184] and aa[0x184:0x18a]==b'2.96.0' and bb[0x184:0x18a]==b'3.96.0'
 if ae: assert (aa,bb)==ae
 changed=diff(a,b); assert len(changed)==6 and e+0x184 in changed
 words=sorted({i//4*4 for i in changed if i!=e+0x184}); assert len(words)==2
 crcs=[]
 for data in (a,b):
  hi,lo=[struct.unpack_from('<I',data,w)[0] for w in words]
  assert hi&127==55 and lo&0x707f==19
  assert (hi>>7)&31==(lo>>7)&31==(lo>>15)&31
  imm=lo>>20; imm=imm-4096 if imm>=2048 else imm
  crcs.append(((hi&0xfffff000)+imm)&0xffffffff)
 assert crcs==[binascii.crc32(aa),binascii.crc32(bb)]
 assert all(any(s[1]<=i<s[1]+s[4] for s in pa) for i in changed)
 print('ELF',label,'length',len(a),'six byte offsets',changed,'CRC',*[hex(x) for x in crcs],'layout equal')
 return pa,pb

for shape,bits_expected in [('1x1',22),('8x8',15)]:
 base=root/'shipping'/shape; a=read(base/'bench/alinx_ax7101.bit'); b=read(base/'flip/alinx_ax7101.bit')
 fa,offset=headers(a); fb,other=headers(b); assert offset==other
 print('BIT',shape,'sha256',h(a),h(b),'byte differences',len(diff(a,b)))
 allowed=set()
 for k in fa:
  loc,va=fa[k]; locb,vb=fb[k]; assert loc==locb
  ds=diff(va,vb); print('HEADER',shape,k,'offsets',[loc+i for i in ds],repr(va),repr(vb))
  if k=='a':
   qa=va.split(b';'); qb=vb.split(b';'); assert len(qa)==len(qb)
   for x,y in zip(qa,qb):
    if x!=y: assert x.split(b'=')[0]==y.split(b'=')[0] and x.startswith((b'SW_CRC=',b'SW_HDR_SHA256='))
  elif ds: assert k in ('c','d')
  allowed.update(loc+i for i in ds)
 pos=a.index(b'\xaa\x99\x55\x66',offset)+4; framebits=0; framebytes=0; crcbytes=0
 while pos<len(a):
  word=struct.unpack_from('>I',a,pos)[0]; assert a[pos:pos+4]==b[pos:pos+4]
  typ=word>>29; count=0
  if typ==1: reg=(word>>13)&0x3fff; count=word&0x7ff
  elif typ==2: count=word&0x7ffffff
  start=pos+4; end=start+4*count
  ds=diff(a[start:end],b[start:end])
  if ds:
   assert reg in (0,2)
   allowed.update(start+i for i in ds)
   if reg==2: framebytes+=len(ds); framebits+=sum((a[start+i]^b[start+i]).bit_count() for i in ds)
   else: crcbytes+=len(ds)
  pos=end
 assert allowed==set(diff(a,b)) and framebits==bits_expected and crcbytes==4
 print('PAYLOAD',shape,'CRC bytes',crcbytes,'frame bytes/bits',framebytes,framebits,'all bytes accounted')
 ae=tuple(read(base/s/'aem_desc.bin') for s in ('bench','flip'))
 elves=tuple(read(base/s/'ctrl_app.elf') for s in ('bench','flip'))
 loads=elfcheck(*elves,shape,ae)
 for side,data,segs in zip(('bench','flip'),elves,loads):
  bankpaths=sorted((base/side/'gateware').glob('*rom_bank*.init'))
  rom=b''.join(struct.pack('<I',int(w,16)) for p in bankpaths for w in p.read_bytes().split())
  expected=bytearray(len(rom))
  for s in segs: expected[s[3]:s[3]+s[4]]=data[s[1]:s[1]+s[4]]
  assert rom==expected
  print('ROM',shape,side,len(bankpaths),'banks',len(rom),'all load segments and gaps/padding equal')
 for name in ('aem_desc.json','aem_desc.map','gateware/alinx_ax7101_mem.init'):
  assert read(base/'bench'/name)==read(base/'flip'/name)
 for name,keys in [('csr.json',{'/constants/milan_aem_image_crc32'}),('flashboot_layout.json',{'/aem_image_crc32','/aem_image_sha256','/bitstream_payload_sha256'}),('image_manifest.json',None)]:
  xa=json.loads(read(base/'bench'/name)); xb=json.loads(read(base/'flip'/name)); rows=jdiff(xa,xb)
  print('EXPORT',shape,name,json.dumps(rows))
  if keys: assert {r[0] for r in rows}==keys
  else: assert len(rows)==3 and all(r[0].endswith(('/version','/sha256','/bitstream_payload_sha256')) for r in rows)
 for x,y in zip(read(base/'bench/csr.csv').splitlines(),read(base/'flip/csr.csv').splitlines()):
  if x!=y: assert x.startswith((b'# Auto-generated by LiteX',b'constant,milan_aem_image_crc32,')); print('CSV',shape,x,y)
 for kind in ('cells','nets','bram'):
  if kind=='bram' and shape=='1x1': continue
  x=read(base/'dump'/('bench.'+kind+'.xz')); y=read(base/'dump'/('flip.'+kind+'.xz'))
  if x is None or y is None: continue
  if kind=='nets': assert x==y; print('ROUTES',shape,len(x.splitlines()),'byte equal'); continue
  assert len(x.splitlines())==len(y.splitlines()); total=0; changed=0
  for u,v in zip(x.splitlines(),y.splitlines()):
   if u==v: continue
   us,vs=u.split(),v.split(); assert len(us)==len(vs)
   assert us[:2]==vs[:2] and (b'/csr/' in us[0] or b'rom_bank' in us[0]); changed+=1
   for l,r in zip(us,vs):
    if l==r: continue
    assert l.startswith(b'INIT') and l.split(b'=')[0]==r.split(b'=')[0]
    total+=(int(l.split(b"'h")[1],16)^int(r.split(b"'h")[1],16)).bit_count()
  assert total==bits_expected; print('CELLS',shape,kind,len(x.splitlines()),'changed cells',changed,'INIT bits',total)

for p in sorted((root/'harness').glob('*/*/measured.elf')):
 elfcheck(read(p),read(p.with_name('head.elf')),str(p.parent.relative_to(root)))
 assert read(p.with_name('measured.parts.json'))==read(p.with_name('head.parts.json'))
print('HARNESS 16 pairs and partitions checked')
groups=0; logs=0
for p in sorted((root/'groups').glob('*/*/*.measured.json')):
 q=p.with_name(p.name.replace('.measured.','.head.'))
 assert json.loads(read(p))==json.loads(read(q)); groups+=1
 print('GROUP JSON',p.relative_to(root),'all values and structure equal')
 x=read(p.with_name(p.name.replace('.json','.log.gz'))); y=read(q.with_name(q.name.replace('.json','.log.gz')))
 if x is None or y is None: continue
 logs+=1; assert len(x.splitlines())==len(y.splitlines())
 for ln,(u,v) in enumerate(zip(x.splitlines(),y.splitlines()),1):
  for off in diff(u,v):
   assert u[off]==ord('2') and v[off]==ord('3')
   print('LOG DELTA',p.relative_to(root),ln,off,u[max(0,off-45):off+45],v[max(0,off-45):off+45])
print('GROUP TOTAL',groups,'JSON pairs;',logs,'complete log pairs')
print('MISSING TOTAL',len(set(missing)),sorted(set(missing)))
print('Available operands passed; complete identity remains unproved' if missing else 'ALL IDENTITY CHECKS PASSED')
