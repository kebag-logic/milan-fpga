"""Final firmware shards or complete Arty boot campaign, sharing four harness slots."""
import concurrent.futures,json,os,subprocess,sys
from pathlib import Path
from harness_slots import slot
root=Path.cwd();r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
mode=sys.argv[1];records=[]
def command(label,argv):
 log=r/(label+'.log')
 with slot(label):
  with log.open('w') as sink:proc=subprocess.run(argv,cwd=root,stdout=sink,stderr=subprocess.STDOUT,timeout=86400)
 result=dict(label=label,command=argv,returncode=proc.returncode,log=str(log))
 (r/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
 return result
if mode=='firmware':
 def shard(number):
  return command('final-firmware-'+str(number),[sys.executable,'-B','sw/firmware/ctrl/test/test_ctrl_firmware.py',
   '--self-test','--require-rv32','--shard',f'{number}/4','--jobs','1','--build-dir',str(r/'final-firmware'/str(number))])
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(shard,range(4)))
elif mode=='boot':
 def boot(args):
  label,directory,extra=args
  return command(label,[sys.executable,'-B','tb/verilator/ctrl_split_boot/run.py','--shape','endstation_arty_split',
                         '--interfaces','1','--build-dir',str(directory),*extra])
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  records=list(pool.map(boot,[('final-boot-positive-fixedseed',r/'final-boot-positive-fixedseed',[]),
                             ('final-boot-controls-fixedseed',r/'final-boot-controls-fixedseed',['--self-test'])]))
else:raise SystemExit('Expected firmware or boot')
(r/('final-'+mode+'-results.json')).write_text(json.dumps(records,indent=2)+'\n')
raise SystemExit(any(row['returncode'] for row in records))
