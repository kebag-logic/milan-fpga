"""Read all three routed candidates; retain the best candidate meeting every corner floor."""
import hashlib,json,os,re,subprocess,sys
from pathlib import Path
root=Path.cwd(); out=Path(sys.argv[1]).resolve(); elf=Path(sys.argv[2]).resolve(strict=True)
sys.path.insert(0,str(root/'scripts'))
from area_baseline import parse_timing
directives=('ExtraPostPlacementOpt','AltSpreadLogic_high','ExtraTimingOpt')
def artifact(p):
 return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def utilization(p):
 rows={}
 for line in p.read_text().splitlines():
  if not line.lstrip().startswith('|'):continue
  cells=[x.strip() for x in line.strip().strip('|').split('|')]
  if len(cells)<2:continue
  name=cells[0].rstrip('*').strip()
  if name in ('Slice LUTs','Slice Registers','Slice','Block RAM Tile','RAMB36/FIFO','RAMB18'):
   try:rows.setdefault(name,float(cells[1].replace(',','')))
   except ValueError:continue
 assert all(k in rows for k in ('Slice LUTs','Slice Registers','Slice','Block RAM Tile')),p
 return rows
rows=[]
for directive in directives:
 work=out/directive; receipt=out/(directive+'.result.json')
 record=dict(directive=directive,status='FAIL',findings=[],corners=[])
 if not receipt.exists():
  record['findings'].append('No completed attempt receipt')
  rows.append(record);continue
 attempt=json.loads(receipt.read_text())
 if attempt['rc']!=0:record['findings'].append('Build exited '+str(attempt['rc']))
 for corner in ('Slow','Fast'):
  for temperature in (0,85):
   path=work/'gateware'/f'digilent_arty_signoff_{corner}_{temperature}C_timing.rpt'
   timing=parse_timing(path)
   if not timing:record['findings'].append(f'Missing timing: {corner} {temperature} C')
   elif timing['wns']<0.030 or timing['whs']<0.0 or timing['failing_endpoints']:
    record['findings'].append(f'Floor missed: {corner} {temperature} C: {timing}')
   record['corners'].append(dict(corner=corner,junction_c=temperature,timing=timing,
                                 **({'report':artifact(path)} if path.exists() else {})))
 bit=work/'gateware/digilent_arty.bit'
 layout=work/'flashboot_layout.json'; manifest=work/'image_manifest.json'
 aem=work/'aem_desc.bin'; aem_manifest=work/'aem_desc.json'
 for name,path in (('bitstream',bit),('layout',layout),('manifest',manifest),
                   ('aem',aem),('aem_manifest',aem_manifest)):
  if path.is_file():record[name]=artifact(path)
  else:record['findings'].append('Missing '+name)
 utilization_reports=sorted((work/'gateware').glob('*utilization_route.rpt'))
 if not utilization_reports:utilization_reports=sorted((work/'gateware').glob('*utilization_place.rpt'))
 if len(utilization_reports)!=1:record['findings'].append('No unique implementation utilization report')
 else:
  record['utilization_report']=artifact(utilization_reports[0])
  try:record['utilization']=utilization(utilization_reports[0])
  except (AssertionError,ValueError) as exc:record['findings'].append(str(exc))
 if bit.is_file() and layout.is_file() and manifest.is_file():
  cmd=[sys.executable,str(root/'sw/litex/check_image_identity.py'),str(work),
       '--firmware',str(elf),'--bitstream',str(bit)]
  proc=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=600)
  identity=out/(directive+'-identity.log');identity.write_text(proc.stdout)
  record['identity']=dict(returncode=proc.returncode,receipt=artifact(identity))
  if proc.returncode:record['findings'].append('Image identity gate failed')
  if aem.is_file():
   # check-images materializes and checks the target set with no programmer I/O.
   env=dict(os.environ,BIT=str(bit),LAYOUT=str(layout),AEM=str(aem),
            FPGA_PART='xc7a100tcsg324',EXPECTED_GPTP_OWNER='fabric',
            PYTHON='<home-path>/litex-milan/venv/bin/python3',TMPDIR=str(out))
   proc=subprocess.run(['bash',str(root/'sw/litex/deploy.sh'),'check-images'],
                       env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=600)
   preflight=out/(directive+'-offline-pair.log');preflight.write_text(proc.stdout)
   record['offline_pair']=dict(returncode=proc.returncode,receipt=artifact(preflight))
   if proc.returncode:record['findings'].append('Offline flash-pair input preflight failed')
 if not record['findings']:
  record['status']='PASS'
  record['worst_wns_ns']=min(c['timing']['wns'] for c in record['corners'])
  record['worst_whs_ns']=min(c['timing']['whs'] for c in record['corners'])
 rows.append(record)
passing=[r for r in rows if r['status']=='PASS']
best=max(passing,key=lambda r:(r['worst_wns_ns'],r['worst_whs_ns'])) if passing else None
result=dict(status='PASS' if best else 'FAIL',firmware=artifact(elf),candidates=rows,best=best,
            floor=dict(wns_ns=0.030,whs_ns=0.0),
            corner_note='Slow/Fast are fixed speed models; endpoint temperatures are power metadata.')
(out/'graded-images.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(not bool(best))
