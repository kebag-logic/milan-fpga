import ast,copy,importlib.util,json,os,sys,subprocess,re
from pathlib import Path
root=Path(__file__).resolve().parent.parent;tmp=Path(os.environ['REVIEW_TMP'])
spec=importlib.util.spec_from_file_location('review_publication',root/'sw/builder/test_builder.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);m.OUT=tmp/'publication-out'
source=m.MILAN_SOC_PY.read_text();tree=ast.parse(source)
loops=[n for n in ast.walk(tree) if isinstance(n,ast.For) and isinstance(n.iter,ast.Call) and isinstance(n.iter.func,ast.Attribute) and isinstance(n.iter.func.value,ast.Call) and isinstance(n.iter.func.value.func,ast.Name) and n.iter.func.value.func.id in {'fabric_constants','firmware_constants'}]
assert len(loops)==2
old_source=subprocess.check_output(['git','show','f8b8c0fe:sw/builder/test_builder.py'],text=True)
old_fn=next(n for n in ast.parse(old_source).body if isinstance(n,ast.FunctionDef) and n.name=='_assert_publication_loop_is_pinned')
old_scope={'re':re,'_PUBLICATION_LOOPS':m._PUBLICATION_LOOPS}
exec(compile(ast.Module(body=[old_fn],type_ignores=[]),'prior-public-checker','exec'),old_scope)
results=[]
def replace(node,text):
 lines=source.splitlines(keepends=True);pad=' '*node.col_offset
 return ''.join(lines[:node.lineno-1])+''.join(pad+line+'\n' for line in text.splitlines())+''.join(lines[node.end_lineno:])
def grade(label,text,refuse,full=False):
 ast.parse(text)
 if label.endswith('-later-write'):
  old_scope['_assert_publication_loop_is_pinned'](text);print(label,'prior checker ACCEPTED',flush=True)
 try:m._assert_publication_loop_is_pinned(text)
 except AssertionError as e:
  assert refuse and 'pinned complete loop' in str(e),(label,str(e));verdict='REFUSED complete-loop pin'
 else:
  assert not refuse,label+' unexpectedly accepted';verdict='ACCEPTED'
 results.append([label,verdict]);print(label,verdict,flush=True)
 if full:
  path=tmp/(label+'.py');path.write_text(text);old=m.MILAN_SOC_PY;m.MILAN_SOC_PY=path
  try:
   try:m.test_boot_policy_follows_the_declaration()
   except AssertionError as e:
    assert refuse and 'pinned complete loop' in str(e),(label,str(e));print(label,'complete gate 35 REFUSED',flush=True)
   else:assert not refuse
  finally:m.MILAN_SOC_PY=old
for i,loop in enumerate(loops):
 name=loop.iter.func.value.func.id
 expr='3 if _name.endswith("CTRL_BOOT") else _value' if name=='fabric_constants' else '300 if _name.endswith("HEARTBEAT_MS") else _value'
 override=ast.parse('soc.add_constant(_name, '+expr+', check_duplicate=False)').body[0]
 altered=copy.deepcopy(loop);altered.body.append(override)
 grade(name+'-later-write',replace(loop,ast.unparse(altered)),True,True)
 altered=copy.deepcopy(loop);altered.orelse=[override]
 grade(name+'-else-write',replace(loop,ast.unparse(altered)),True)
 altered=copy.deepcopy(loop);altered.body.append(ast.If(test=ast.Constant(True),body=[override],orelse=[]))
 grade(name+'-nested-write',replace(loop,ast.unparse(altered)),True)
 altered=copy.deepcopy(loop);altered.body[0].value.args[1]=ast.Constant(17)
 grade(name+'-first-value',replace(loop,ast.unparse(altered)),True)
 grade(name+'-duplicate',replace(loop,ast.unparse(loop)+'\n'+ast.unparse(loop)),True)
 grade(name+'-missing',replace(loop,'pass'),True)
 # Format only the loop, preserving every AST field and normal import lines.
 formatted=ast.unparse(loop).replace('    soc.add_constant(_name, _value)','    # Reviewer formatting control\n    soc.add_constant(\n        _name,\n        _value\n    )')
 grade(name+'-comments-multiline',replace(loop,formatted),False)
 # The full gate's mutation constructors deliberately have narrower locator anchors.
 formatted=ast.unparse(loop).replace('soc.add_constant(_name, _value)','soc.add_constant(  _name,   _value  )')
 grade(name+'-spacing',replace(loop,formatted),False)
grade('pristine',source,False,True)
firmware=(root/'sw/firmware/milan_baremetal/milan_baremetal.c').read_text()
for key,value in m.nvm_shape.WRITER_TIMING_MS.items():
 waits=dict(m.nvm_shape.WRITER_TIMING_MS);waits[key]=value+1
 try:m._assert_writer_waits_generated(firmware,waits)
 except AssertionError as e:assert 'pinned set is' in str(e);print(key,'+1 REFUSED',flush=True)
 else:raise AssertionError(key)
(tmp/'publication-results.json').write_text(json.dumps(results,indent=2))
print('PUBLICATION PROBE PASS',flush=True)
