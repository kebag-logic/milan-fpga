import copy,sys,json
from pathlib import Path
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'scripts'))
import ci_events as c
w=c.parse_world(c.read_tree(root));pristine=w[c.DOCS];results=[]
def run(label,mutation=None,specchange=None,want=''):
 wf=copy.deepcopy(pristine);spec=copy.deepcopy(c.CARRIER_STEP_LISTS[(c.DOCS,'docs-check')]);ss=wf['jobs']['docs-check']['steps'];at=next(i for i,s in enumerate(ss) if s.get('name')=='AEM store generator self-test')
 if mutation:mutation(ss,at)
 if specchange:specchange(spec,at)
 check=c.Contract();c.check_carrier_steps(check,c.DOCS,wf,'docs-check',spec)
 good=not check.findings if not want else any(want in f for f in check.findings)
 assert good,(label,check.findings)
 results.append({'label':label,'expected_fragment':want,'findings':check.findings})
run('pristine')
for label,body in [('no-op','true'),('swallowed','python3 avdecc/gen_aem_store.py --self-test || true'),('appended','python3 avdecc/gen_aem_store.py --self-test\necho appended'),('flag removed','python3 avdecc/gen_aem_store.py'),('wrong source','python3 old/avdecc/gen_aem_store.py --self-test')]:
 run(label,lambda ss,at,b=body:ss[at].update(run=b),want='script is not the canonical form')
for key,value in [('if',False),('continue-on-error',True),('working-directory','other'),('shell','bash')]:
 run(key,lambda ss,at,k=key,v=value:ss[at].update({k:v}),want=('must carry no `'+key+'`') if key in ['if','continue-on-error'] else 'surplus: '+key)
run('removed',lambda ss,at:ss.pop(at),want='exactly 44 steps')
run('missing source record',specchange=lambda spec,at:spec[at].pop('run'),want='must record a canonical normalized `run` script')
run('checkout source redirected',lambda ss,at:ss[0]['with'].update(ref='dev'),want='with')
Path(__file__).with_name('ci-control-results.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS',len(results),'independent carrier controls')
