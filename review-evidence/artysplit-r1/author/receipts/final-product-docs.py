"""Write the Arty product memory ledger from its ELF receipt, then run the docs gates."""
import datetime,hashlib,json,os,subprocess,sys,time
from pathlib import Path
from harness_slots import slot
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4');root=Path.cwd();out=r/'docs-final'
while not (r/'identity-final-compare.json').exists():
 p=r/'final-products-commands.json'
 if p.exists() and any(x['returncode'] for x in json.loads(p.read_text())):raise SystemExit('Product build failed')
 time.sleep(3)
assert json.loads((r/'identity-final-compare.json').read_text())['status']=='PASS'
product=r/'arty-product-final/endstation_arty_split/product'
size=json.loads((product/'size.json').read_text());elf=product/'ctrl_app.elf'
artifact=next(x for x in size['artifacts'] if x['name']=='ctrl_app.elf')
assert elf.stat().st_size==artifact['size'] and hashlib.sha256(elf.read_bytes()).hexdigest()==artifact['sha256']
assert size['shape']=='endstation_arty_split' and size['interfaces']==1
plan=size['split'];assert plan['tiles']<=plan['budget_tiles']==56
doc=root/'docs/design/SPLIT_CONTROL_MEMORY.md';before=doc.read_bytes()
heading='### Arty firmware memory ledger\n'
assert doc.read_text().count(heading)==1
rows=[('Linked ELF file',f"{artifact['size']} bytes")]
rows += [(f'`{name}`',f'{size["sections"][name]} bytes') for name in ('.text','.rodata','.data','.bss','.stack')]
rows += [('ROM live extent, including initial data',f"{plan['rom']['bytes']} bytes"),
         ('SRAM live extent, including stack',f"{plan['sram']['bytes']} bytes")]
for name in ('rom','sram'):
 part=plan[name];rows.append((name.upper()+' allocation',f"{part['RAMB36']+part['RAMB18']/2:g} RAMB36"))
rows += [('Total allocation',f"{plan['tiles']:g} RAMB36"),('Budget',f"{plan['budget_tiles']:g} RAMB36")]
text=heading+'''
This is a new Arty ledger (#878).
It records the product firmware linked with the measured 80 MHz scheduler row.
The existing 56 RAMB36 limit applies.
Memory fit does not waive the service-budget or routed timing checks.

| Item | Bytes or RAMB36 equivalent |
|---|---:|
'''+''.join(f'| {name} | {value} |\n' for name,value in rows)+'''
The linked image's `size.json` records the sections and bank decomposition.
The routed image binds that firmware through `image_manifest.json`.
'''
doc.write_text(doc.read_text().split(heading)[0]+text)
(r/'arty-product-ledger.json').write_text(json.dumps(dict(status='PASS',kind='Product memory fit; service and routing qualification separate',
 time=datetime.datetime.now(datetime.timezone.utc).isoformat(),firmware=artifact,size_receipt=str(product/'size.json'),
 doc=str(doc.relative_to(root)),before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(doc.read_bytes()).hexdigest(),rows=rows),indent=2)+'\n')
out.mkdir();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(r/'work-tmp'))
commands=[row['command'] for row in json.loads((r/'docs/results.json').read_text())]
results=[]
with slot('final documentation gates'):
 with (out/'toc-refresh.log').open('w') as log:
  subprocess.run(['$VALIDATION_STORAGE/artysplit-a829/docs-venv/bin/python','scripts/gen_toc.py','--write',
                  'docs/design/SPLIT_CONTROL_MEMORY.md','docs/litex/CLOCK_DOMAINS.md'],stdout=log,stderr=subprocess.STDOUT,
                 env=env,check=True,timeout=1800)
 for number,argv in enumerate(commands):
  log=out/f'{number:02d}-{Path(argv[1]).stem}.log';started=time.monotonic()
  with log.open('w') as stream:p=subprocess.run(argv,stdout=stream,stderr=subprocess.STDOUT,env=env,timeout=3600)
  results.append(dict(command=argv,rc=p.returncode,seconds=round(time.monotonic()-started,3),log=log.name))
  (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
  print('DOC',number,p.returncode,flush=True)
print('Product ledger and documentation gates',len(results),'completed',flush=True)
raise SystemExit(any(x['rc'] for x in results))
