"""Run against a checkout: python3 -B probe_attribution.py CHECKOUT.

Constructed observation histories, not CPU-system measurements.
No source modification; exercise the actual parser and path grader.
"""
import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_budget'))
import grade
import held
import scenario
import selftest as st
from selftest_held import held_checks

for name, ok, detail in held_checks(st):
    print(('PASS' if ok else 'FAIL') + ': ' + name)
    assert ok, detail

ch = scenario.CH['aecp']
probe = scenario.Probe('s.held.if0', 'READ_DESCRIPTOR held', 'aecp', f'rxh:{ch}', [f'resp:{ch}:7d00'])
response = st.tx_record(ch, 0, st.aem_response(scenario.CTL1, 0x7D00, 0x0004), 0, 700000)
prefix = ['MARK 1000 s.held.if0', 'RXS 1000 0 60 s.held.if0', 'RXE 1059', f'RXH 1070 {ch}']
base = prefix + ['RXS 500030 0 60 follower', 'RXE 500089', f'RXR 500100 {ch}', *response]

def examine(name, lines):
    try:
        text = st.synthetic(lines)
        log = grade.parse(text, st.SYS_HZ, st.CPU_HZ)
        row = st.one(text, probe)
        print(json.dumps(dict(case=name, parsed=True, rxc=log.rxc, held=log.held,
                              refused=log.refused, row={k: row.get(k) for k in
                              ('status', 'start_sys', 'end_sys', 'ms', 'within_budget', 'ingress_sys')})))
        return row
    except grade.Refusal as error:
        print(json.dumps(dict(case=name, parsed=False, refusal=str(error))))
        return None

examine('positive held frame with refused follower', base)
examine('positive other-channel commit while AECP held', prefix +
        ['RXS 2000 0 60 other_channel', 'RXE 2059', f'RXC 2070 {scenario.CH["acmp"]}',
         f'RXR 500100 {ch}'] + response)
examine('duplicate release', base[:-len(response)] + [f'RXR 500101 {ch}'] + response)
examine('missing release', prefix + response)
examine('release before hold in record order', prefix[:3] + [f'RXR 500100 {ch}', prefix[3]] + response)
examine('release timestamp before hold timestamp', prefix + [f'RXR 1060 {ch}'] + response)
examine('later same-channel frame commits before held frame', prefix +
        ['RXS 2000 0 60 follower', 'RXE 2059', f'RXC 2070 {ch}', f'RXR 500100 {ch}'] + response)
with patch.object(held, 'release', lambda log, pending, channel, cycle: grade.owner(pending, cycle, log.refused)):
    result = examine('negative control: previous attribution', base)
    assert result is None or result['status'] != 'measured'
print('Completed constructed-history attribution probes.')
