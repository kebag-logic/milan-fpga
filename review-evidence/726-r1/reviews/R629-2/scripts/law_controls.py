import runpy, sys
from pathlib import Path
from types import SimpleNamespace
root=Path(sys.argv[1]).resolve()
ns=runpy.run_path(str(root/'tests/steps/counters_contract_steps.py'))
tc=ns['tc']; ctx=SimpleNamespace()
given=ns['step_cc_sem_given']; then=ns['step_cc_sem_then']
given(ctx,'FRAMES_RX',4,4); then(ctx,'FAIL','interval')
print('CLEAN FRAMES_RX 4 packets / 4 s: FAIL under Table 7.157')
tc.STREAM_INPUT_COUNTER_LAW['FRAMES_RX']=('per-interval','Milan v1.2 Table 5.6','at least one Stream Data AVTPDU')
given(ctx,'FRAMES_RX',4,4)
try: then(ctx,'FAIL','interval')
except AssertionError as exc:
    assert 'PASS != FAIL' in str(exc) and 'FRAMES_RX' in str(exc)
    print('DETECTED interval-rate FRAMES_RX:',exc)
else: raise AssertionError('law regression escaped')
given(ctx,'FRAMES_RX',4,4)
assert ctx.cc_sem[0]=='PASS'
print('OMIT semantics verdict: PASS (same plant)')
