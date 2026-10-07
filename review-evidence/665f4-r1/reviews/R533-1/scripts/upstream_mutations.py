#!/usr/bin/env python3
"""Plant codec fixes in disposable source copies; run unchanged pinned tests."""
import pathlib,sys,subprocess,os,shutil,json
root=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(__file__).resolve().parents[1]
base=root/'third_party/lwSRP';results=[]
definitions=[
 ('up-domain-vector','src/modules/msrp.c','d->class_id = (uint8_t)(buf[0] + offset);','d->class_id = buf[0];','domain_and_vector_offsets_match_wire_fields'),
 ('up-validation','src/core/mrp_pdu.c','int r = parse_pass(pdu, len, ops, NULL, NULL, NULL);','int r = parse_pass(pdu, len, ops, on_attr, on_leaveall, ctx);','truncation_respects_complete_vectors_and_pdu_end')]
sources=['src/ports/alloc.c','src/ports/timer.c','src/core/mrp_mad.c','src/core/mrp_pdu.c','src/core/switch.c','src/modules/sim_adapter.c','src/modules/mvrp.c','src/modules/mmrp.c','src/modules/msrp.c']
for name,path,old,new,test in definitions:
 work=packet/'scratch'/name; work.mkdir(exist_ok=True);shutil.copytree(base/'src',work/'src',dirs_exist_ok=True)
 target=work/path;text=target.read_text();assert text.count(old)==1;target.write_text(text.replace(old,new))
 cmd=['gcc','-std=c11','-Wall','-Wextra','-fPIC','-shared','-I'+str(work/'src/include'),'-I'+str(work/'src/modules'),'-I'+str(work/'src'),*[str(work/s) for s in sources],'-o',str(work/'libshlan.so')]
 r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,r.stderr
 env=os.environ.copy();env['LD_LIBRARY_PATH']=str(work)+':'+str(packet/'scratch/cgreen-build/src')
 r=subprocess.run([str(packet/'scratch/upstream/unit_tests')],env=env,capture_output=True,text=True)
 log='COMMAND '+json.dumps(cmd)+'\n'+r.stdout+r.stderr
 (packet/'receipts'/f'{name}.log').write_text(log);(packet/'receipts'/f'{name}.rc').write_text(str(r.returncode)+'\n')
 caught=r.returncode==1 and test in log and 'Failure' in log
 results.append({'name':name,'path':'third_party/lwSRP/'+path,'old':old,'new':new,'test':test,'rc':r.returncode,'caught':caught})
 print(name,'caught',caught,'rc',r.returncode,flush=True)
(packet/'receipts/upstream-mutations.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(0 if all(row['caught'] for row in results) else 1)
