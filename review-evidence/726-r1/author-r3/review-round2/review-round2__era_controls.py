import runpy, sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
ns=runpy.run_path(str(root/'tests/steps/counters_contract_steps.py'))
wipe=ns['step_cc_crf_era_wipe']; edge=ns['step_cc_crf_era_edge']; lock=ns['step_cc_crf_era_lock']
original=ns['_crf_rx_source']()
key='if (w_bind_rise_w) begin'
prefix,body=original.split(key)
for check in (wipe,edge,lock): check(None)
print('CLEAN: all era checks pass')
for reg in ('iv_uf_r','iv_sm_r','iv_mr_r','iv_tu_r','iv_lt_r','iv_et_r',*ns['CRF_COUNTER_REG'].values()):
    import re
    changed,count=re.subn(r'\b'+reg+r'\s*<=\s*(?:1\x27b0|\x270)\s*;','',body)
    assert count==1,(reg,count)
    source=prefix+key+changed
    wipe.__globals__['_crf_rx_source']=lambda: source
    try: wipe(None)
    except AssertionError as exc:
        assert reg in str(exc),str(exc)
        print('DETECTED',reg, str(exc).replace('\n',' '))
    else: raise AssertionError('escaped '+reg)
    edge(None); lock(None)
    print('OMIT era-wipe: PASS',reg)
source=original.replace('en_i && !en_q','en_i != en_q')
assert source!=original
wipe.__globals__['_crf_rx_source']=lambda: source
try: edge(None)
except AssertionError as exc:
    assert 'RISING edge only' in str(exc)
    print('DETECTED unbind-wipe',str(exc))
else: raise AssertionError('escaped unbind-wipe')
wipe(None); lock(None)
print('OMIT era-edge: PASS unbind-wipe')
print('17 plants detected; 17 omission controls pass')
