import sys
from runner import load
m=load(base='--base' in sys.argv,expose=True);x=m.test_baremetal_profile_contract()
f=x['firmware_source']
old='milan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);'
new='milan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT\n#ifndef MILAN_CENSUS_SOC\n| 4u\n#endif\n);'
assert f.count(old)==1;s=f.replace(old,new)
try:x['assert_boot_contract'](s,x['docs_source'],x['csr_source'])
except AssertionError as e:assert 'a conditional group reaching' in str(e);print('whole REFUSE retained reach rule')
else:raise AssertionError('conditional allowed')
if '--base' not in sys.argv and x['census_used'].get('target'):
 x['assert_preprocessed_boot_path'](x['blanked'](s),s,x['preprocess_take'](s))
 print('preprocessor alone ACCEPT literal-selected argument: declared instrument boundary')
else:print('SKIP added-instrument observation')
