import copy, pathlib, sys
root=pathlib.Path(sys.argv[1]).resolve(); log=pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import egress_ledger as e
instances,errors,logs=e.read([log]); point='8x8-1if'; errors+=e.findings(instances,point,logs)
print('Published Listener-image log baseline findings:', errors)
assert not errors
for name,limit in e.LEDGER[point].items():
 planted=copy.deepcopy(instances)
 row=next(x for x in planted if x['probe']==name)
 row['ms']=limit+0.001
 found=e.findings(planted,point,logs)
 matched=[s for s in found if name in s and 'larger miss' in s]
 print(name,'above ledger by 0.001 ms:', 'REFUSED' if matched else 'ESCAPED')
 assert matched,found
print('RESULT: baseline passes; all seven larger-miss probes refused by name')
