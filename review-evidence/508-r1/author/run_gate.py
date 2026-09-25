from pathlib import Path
import datetime,json,os,subprocess,sys,time
out=Path(__file__).resolve().parent
root=Path('$LANES/508-pp-pin-adopt')
env=dict(os.environ)
env['PATH']='$VALIDATION_STORAGE/508-a295-tools:$VALIDATION_STORAGE/408-manager-r7/pinned-tool-bin:'+env['PATH']
env['VERILATOR_JOBS']='8'
env['PYTHONPATH']='$VALIDATION_STORAGE/508-a295-tools/markdown'+(':'+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
env['PYTHONUNBUFFERED']='1'
# All children execute synchronously in the foreground, with logs as files.
name=sys.argv[1]
cwd=root
args=sys.argv[2:]
if args[:1]==['--cwd']:
 cwd=root/args[1];args=args[2:]
log=out/(name+'.log')
assert not log.exists(), log
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
start=time.time()
record=dict(name=name,argv=args,cwd=str(cwd),head=head,start=datetime.datetime.now(datetime.timezone.utc).isoformat(),log=log.name)
(out/(name+'-running.json')).write_text(json.dumps(record,indent=2)+'\n')
print('START',name,'head='+head,flush=True)
with log.open('w') as stream:
 stream.write(json.dumps(record)+'\n');stream.flush()
 try:
  rc=subprocess.run(args,cwd=cwd,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=21600).returncode
 except subprocess.TimeoutExpired:
  rc=124
record.update(rc=rc,seconds=round(time.time()-start,2))
with (out/'gates.jsonl').open('a') as stream:stream.write(json.dumps(record)+'\n')
rows=[json.loads(line) for line in (out/'gates.jsonl').read_text().splitlines()]
ledger='| Command | Exit | Seconds | Log |\n|---|---|---|---|\n'
for row in rows:
 command=' '.join(row['argv']).replace(str(out),'$EVIDENCE')
 command=command if len(command)<240 else row['name']+' (complete argv in linked log)'
 ledger+=f"| `{command}` (cwd `{Path(row['cwd']).relative_to(root)}`) | {row['rc']} | {row['seconds']} | [{row['log']}]({row['log']}) |\n"
handoff=out/'HANDOFF.md'
a,b=handoff.read_text().split('<!-- gates:start -->',1)
_,b=b.split('<!-- gates:end -->',1)
handoff.write_text(a+'<!-- gates:start -->\n'+ledger+'<!-- gates:end -->'+b)
(out/(name+'-running.json')).unlink(missing_ok=True)
print('END',name,'rc='+str(rc),'seconds='+str(record['seconds']),flush=True)
print('\n'.join(line[:300] for line in log.read_text(errors='replace').splitlines()[-6:]),flush=True)
sys.exit(rc)
