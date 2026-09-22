import contextlib,json,pathlib,re,sys,tempfile
from unittest.mock import patch
ROOT=pathlib.Path('$VALIDATION_STORAGE/reviews/r227-504-r1'); OUT=pathlib.Path('$WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-r1-r227')
sys.path.insert(0,str(ROOT/'sw/builder')); import test_firmware_compiler as helper
b=helper.builder; captured={}
class Captured(Exception): pass
def trace(frame,event,arg):
 if frame.f_code.co_name=='test_baremetal_profile_contract':
  if event=='line' and 'baseline_census_verdict' in frame.f_locals:
   captured.update(frame.f_locals); raise Captured()
  return trace
 return None
sdk=OUT/'sdk-trial/host'; helper.sdk.verify(sdk)
with (OUT/'raw/store-probe-argv.jsonl').open('w') as log, tempfile.TemporaryDirectory() as temp:
 audit=helper.CompilerAudit(log,sdk)
 with patch.object(helper.subprocess,'run',side_effect=audit.invoke), patch.object(sys,'argv',['store-probes','--require-rv32']),patch.object(b,'OUT',pathlib.Path(temp)),patch.object(b,'SKIPPED',[]):
  try:
   sys.settrace(trace); b.test_baremetal_profile_contract()
  except Captured: pass
  finally: sys.settrace(None)
  assert captured['baseline_census_verdict']['ran']
  print('Pristine full contract reached a real compiled verdict; stopped before shipped mutation bank.')
  fw=captured['firmware_source']; anchor='static void entity_advertise(int verified)\n{'; assert fw.count(anchor)==1
  probes=[('extra-CRFT-write','milan_write(0x750u, 0u);','resolved boot-word census'),('ADP-CAPS-write','milan_write(0x614u, 0u);','resolved boot-word census'),('arithmetic-CSR-store','*(volatile uint32_t *)((0x9000u << 16) | (0x61u << 4)) = 1u;','STORES into the Milan CSR window'),('unrelated-unresolved-call','*r227_store_pointer() = 1u;','STORE this gate cannot PLACE'),('outside-window-positive','*(volatile uint32_t *)0x80001000u = 1u;',None)]
  for label,statement,reason in probes:
   edited=fw.replace(anchor,anchor+'\n\t'+statement)
   if label=='unrelated-unresolved-call':
    edited=edited.replace(anchor,'extern volatile uint32_t *r227_store_pointer(void);\n'+anchor)
   taken=captured['census_take'](edited,label);assert taken['ran'] and taken['arch'].startswith('rv32')
   try:
    result=captured['assert_resolved_boot_flow'](taken['text'],captured['CsrModel'](captured['blanked'](edited),captured['blanked_sv'](captured['csr_source'])),helper=captured['reg_helper_name'])
   except (AssertionError,ValueError) as exc:
    print(json.dumps({'probe':label,'verdict':'REFUSED','reason':str(exc)})); assert reason and reason in str(exc),(label,reason,str(exc))
   else:
    print(json.dumps({'probe':label,'verdict':'ACCEPTED','residual':result['residual']})); assert reason is None,label
 print('4 independent compiled hostile stores refused on property-specific reasons; outside-window store accepted; pristine compiled baseline accepted.')
