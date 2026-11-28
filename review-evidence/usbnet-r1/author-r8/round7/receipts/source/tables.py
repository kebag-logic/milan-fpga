"""Render measured results without introducing a qualification rule."""
import json, sys
from pathlib import Path
root=Path.cwd(); out=Path('$VALIDATION_STORAGE/usbnet-a855/round7/census')
packet=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7/receipts')
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import egress_ledger
measured=json.loads((out/'merged-census.json').read_text())
derived=json.loads((out/'derived-model.json').read_text())
qualification=json.loads((out/'qualification.json').read_text())
lines=['# Complete measured derivation', '', 'The inherited rule and dispositions are unchanged. This table reports the complete census, including its failure.', '', '| Cost | Measured maximum (us) | Rule (us) | Witness |', '|---|---:|---:|---|']
for name,row in sorted(measured['costs'].items()):
 lines.append(f"| {name} | {row['us']:.5f} | {row['rule_us']} | {row['group']} |")
lines+=['', '| Queued (ms) | Pace (ms) | Slice (us) | Pace rule | Queued rule | ACMP (ms) | txL (ms) | Last (ms) | Owner findings |', '|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for row in derived['candidates']:
 r=row['rows_ms']
 lines.append(f"| {row['queued_ms']} | {row['pace_ms']} | {row['slice_us']} | {row['pace_rule']} | {row['queued_rule']} | {r.get('ACMP')} | {r.get('txL')} | {r.get('last')} | {'; '.join(row['owner_findings']) or 'none'} |")
lines+=['', 'Derived load: '+str(derived['load'])+'. Retry terms (us): '+str(derived['retry_us'])+'.', '', '| Held-egress row | Measured (ms) | Frozen ledger (ms) | Result |', '|---|---:|---:|---|']
held=json.loads((out/'none/results/backlog-owed.json').read_text())
ledger=egress_ledger.LEDGER['arty-1x1']
for row in held['probes']:
 if row['probe'] in ledger:
  limit=ledger[row['probe']]
  lines.append(f"| {row['probe']} | {row['ms']:.5f} | {limit:.2f} | {'PASS' if row['ms'] <= limit else 'FAIL'} |")
lines+=['', 'Qualification findings:', '']+['- '+x for x in qualification['findings']]
(packet/'DERIVATION.md').write_text('\n'.join(lines)+'\n')
print('Wrote complete cost, candidate-row and frozen-ledger tables')
