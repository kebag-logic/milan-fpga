import ast,copy,importlib.util,json,os,re,sys,subprocess
from pathlib import Path
root=Path(__file__).resolve().parent.parent;tmp=Path(os.environ['REVIEW_TMP'])
p=root/'sw/builder/test_builder.py'
spec=importlib.util.spec_from_file_location('review_acceptance',p);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);m.OUT=tmp/'acceptance-out'
source=p.read_text()
if '--base' in sys.argv:source=subprocess.check_output(['git','show','07294a76:'+str(p.relative_to(root))],text=True)
tree=ast.parse(source);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='test_baremetal_profile_contract')
cut=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='baseline_census_verdict' for t in n.targets))
fn.body=fn.body[:cut]+[ast.Return(value=ast.Call(func=ast.Name(id='locals',ctx=ast.Load()),args=[],keywords=[]))]
exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(p),'exec'),m.__dict__)
f=m.test_baremetal_profile_contract();fw=f['firmware_source'];docs=f['docs_source'];csr=f['csr_source'];results=[]
def whole(text,listing=None):return f['assert_boot_contract'](text,docs,csr,listing=listing)
baseline=whole(fw);present=baseline['ran'];print('BASELINE', 'RV32' if present else 'NO RV32',flush=True)
if '--baseline' in sys.argv:sys.exit(0)
def span(name):
 pat=re.compile(r'^static[^;{}]*?\b'+name+r'\([^;{}]*?\)\s*\{.*?^}',re.M|re.S)
 hit=pat.search(fw);assert hit,name;return hit.start(),hit.end()
def at_end(name,text):
 _,end=span(name);return fw[:end-1]+text+'\n'+fw[end-1:]
def outcome(label,call,expect_reason=None):
 try:call()
 except (AssertionError,ValueError) as e:
  assert expect_reason and expect_reason in str(e),(label,str(e));verdict='REFUSED: '+str(e).splitlines()[0]
 else:
  assert expect_reason is None,label+' unexpectedly accepted';verdict='ACCEPTED'
 print(label,verdict,flush=True);results.append([label,verdict])
def instrument(text,kind):
 if kind=='preprocessed':return f['assert_preprocessed_boot_path'](f['blanked'](text),text,f['preprocess_take'](text,'reviewer'))
 taken=f['census_take'](text,'reviewer');f['assert_compiled_census_is_clean'](text,'reviewer',taken=taken)
 return f['assert_resolved_boot_flow'](taken['text'],f['CsrModel'](f['blanked'](text),f['blanked_sv'](csr)),helper='milan_reg')
debug=at_end('milan_init','#ifdef R214_REVIEW_DEBUG\n\tprintf("review debug\\n");\n#endif')
paste=fw.replace('\tprint_tod(gettime_ns());','#define R214_JOIN(x,y) x##y\n\tR214_JOIN(print,_tod)(gettime_ns());',1)
cast='static unsigned int review_word;\n'+at_end('configure_fabric','\t*(volatile unsigned int *)&review_word = 7u;')
store='static unsigned int review_word;\nstatic void review_poke(volatile unsigned int *dst) { *dst = 7u; }\n'+at_end('configure_fabric','\treview_poke(&review_word);')
a,b=span('parse_u64');c,d=span('seconds_to_ns');assert b<c
reorder=fw[:a]+fw[c:d]+fw[b:c]+fw[a:b]+fw[d:]
rows=[('debug',debug,'preprocessed','conditional group', 'is not the boot path'),('paste',paste,'preprocessed','must not paste tokens',None),('cast',cast,'census','casts to a pointer are pinned',None),('store',store,'census','stores through a pointer are pinned',None),('reorder',reorder,'census','stores through a pointer are pinned',None)]
for label,text,kind,reason,ireason in rows:
 assert text!=fw
 outcome(label+' whole',lambda text=text:whole(text),reason)
 if present:outcome(label+' instrument',lambda text=text,kind=kind:instrument(text,kind),ireason)
 else:print(label+' instrument SKIPPED: no RV32',flush=True)
listing=tuple(sorted(f['firmware_listing']+('README','notes.txt')))
outcome('directory whole',lambda:whole(fw,listing),'directory is pinned')
if present:outcome('directory instrument',lambda:f['assert_include_resolution_is_pinned'](f['include_resolution_planted'](('README','notes.txt'),fw)))
else:print('directory instrument SKIPPED: no RV32',flush=True)
for name,call in [('CRF','milan_write(MILAN_CRF_TX_CTRL, 3u);'),('CAPS','milan_write(0x614u, 0x00008588u);')]:
 text=at_end('entity_advertise','\t'+call)
 outcome(name+' extra whole',lambda text=text:whole(text),'resolved boot-word census' if present else None)
(tmp/('acceptance-results-'+('rv32' if present else 'absent')+'.json')).write_text(json.dumps(results,indent=2))
print('ACCEPTANCE PROBE PASS',flush=True)
