"""Run standing grader assertions against isolated planted functions."""
import ast, importlib.util, io, sys, unittest
from pathlib import Path
root=Path(sys.argv[1]).resolve()
spec=importlib.util.spec_from_file_location('counter_grader',root/'tb/tools/torture_campaign.py')
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
classes=[value for name,value in vars(module).items() if name.startswith('_') and name.endswith('Checks') and isinstance(value,type)]
case=type('StandingContracts',(*classes,unittest.TestCase),{})
source=(root/'tb/tools/torture_campaign.py').read_text()
def plant_function(name,old,new):
    node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name==name)
    text='\n'.join(source.splitlines()[node.lineno-1:node.end_lineno])
    assert text.count(old)==1,(name,old)
    original=getattr(module,name)
    exec(compile(text.replace(old,new),'<planted function>','exec'),vars(module))
    return original
def run(omit=()):
    suite=unittest.TestSuite(case(name) for name in unittest.defaultTestLoader.getTestCaseNames(case) if name not in omit)
    report=io.StringIO();result=unittest.TextTestRunner(stream=report).run(suite)
    return result,report.getvalue()
assert run()[0].wasSuccessful()
plants=[
 ('snapshot','check_tv_tnv','if total > frx:', 'if frx and total > frx:',
  ('test_unpublished_zero_receive_snapshot',),'[726 SNAPSHOT]'),
 ('packet-rate','_perframe_deviant_sides','[role for role in ticks if sem[role] == "interval"]','[]',
  ('test_packet_agreement_attributes_interval_sides','test_concurrent_packet_law_attributes_each_direction'),'[726 '),
]
for label,name,old,new,omit,marker in plants:
    original=plant_function(name,old,new)
    detected,text=run()
    assert not detected.errors,text
    assert detected.failures,text
    assert all(marker in detail for _,detail in detected.failures),text
    assert {test._testMethodName for test,_ in detected.failures}<=set(omit),text
    escaped,escape_text=run(omit)
    assert escaped.wasSuccessful(),escape_text
    setattr(module,name,original)
    print(f'{label}: {len(detected.failures)} named standing failure(s); omission escape {escaped.testsRun} tests PASS')
assert run()[0].wasSuccessful()
