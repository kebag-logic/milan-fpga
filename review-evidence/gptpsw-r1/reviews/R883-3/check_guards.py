#!/usr/bin/env python3
"""Execute the two changed builder predicates with disposable text plants, not the full builder bank."""
import ast,re,sys,textwrap
from pathlib import Path
R=Path(sys.argv[1]).resolve()
text=(R/'sw/builder/test_builder.py').read_text(); tree=ast.parse(text)
ns={'re':re}
fun=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='reference_census')
exec(compile(ast.Module(body=[fun],type_ignores=[]),'<exact-head census>','exec'),ns)
census=next(n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='reference_census' and isinstance(n.args[1],ast.Dict) and any(isinstance(k,ast.Constant) and k.value=='gptp_adj_w' for k in n.args[1].keys))
expected=ast.literal_eval(census.args[1])
dp=(R/'hdl/milan/milan_datapath.sv').read_text()
dp=re.sub(r'/\*.*?\*/|//[^\n]*','',dp,flags=re.S)
def check(label, fn, bad=False):
    try: fn()
    except AssertionError as e:
        assert bad, str(e)
        print(label+': CAUGHT: '+str(e)); return
    assert not bad, label+' escaped'
    print(label+': PASS')
check('PHC census control',lambda:ns['reference_census'](dp,expected,'PHC'))
for name in ['gptp_adj_w','gptp_step_we_w','gptp_step_w','phc_load_ts_w']:
    check('additional '+name,lambda name=name:ns['reference_census'](dp+'\nassign planted = '+name+';\n',expected,'PHC'),True)
start=text.index('    owner_at = soc_source.find('); end=text.index('    for launcher in ',start)
block=compile(textwrap.dedent(text[start:end]),'<exact-head gate1c>','exec')
soc=(R/'sw/litex/milan_soc.py').read_text()
def gate(s): exec(block,{'re':re,'soc_source':s})
check('software owner control',lambda:gate(soc))
check('software owner branch plant',lambda:gate(soc.replace('\n        elif gptp_sw:', '\n        elif True:')),True)
check('second software owner plant',lambda:gate(soc+'\nself._gptp_owner = "software"\n'),True)
check('opt-in removed plant',lambda:gate(soc.replace('add_argument("--sw-gptp", dest="sw_gptp", action="store_true"','add_argument("--sw-gptp", dest="sw_gptp", action="store_false"')),True)
print('Bounded predicate checks only; no full builder execution claimed.')
