"""Write the review body from completed, bound measurement evidence."""
from pathlib import Path
import json
import subprocess
root=Path.cwd()
out=Path(__file__).parent
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
gates=json.loads((out/'final-gates.json').read_text())+json.loads((out/'final-builder-gates.json').read_text())+json.loads((out/'final-target-gates.json').read_text())
assert all(row['rc']==0 and row['head']==head for row in gates)
receipt=json.loads((root/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
maximum=max(row['maximum_ms'] for row in receipt['measurements'] if row['shape']=='endstation_ax7101_8x8' and row['cpu_hz']==50000000)
comparison=max(row['maximum_ms'] for row in receipt['measurements'] if row['cpu_hz']==100000000)
heartbeat=0
for shape in ('1x1','8x8'):
 for plan in ('all','uart-paced','queued-input','queued-short','device-wait'):
  base=Path('/tmp/a385-final3-service-'+shape+('' if plan=='all' else '-'+plan))
  path=base/('service-'+plan+'-1-'+('3000000-5000' if plan=='device-wait' else '0-0')+'.json')
  data=json.loads(path.read_text());assert data['service_findings']==[]
  heartbeat=max(heartbeat,data['heartbeat_max_gap_ms'])
(out/'PR-BODY.md').write_text(f"""[A385]

Closes #590
Closes #592
Relates to #599

Queued Milan commands and long validation walks now provide heartbeat opportunities, retaining the 250 ms rate limit. Wipe yields between slot erases. Capture copies use aligned words inside closed records and bytes at their edges. Firmware reads PHY state over MDIO and publishes link, speed and duplex through the existing status CSR; a brief latched loss and its recovery are resolved in the same poll.

All six capture arms pass 16 captures each at processor pin `16be6768`. The worst 8x8 interval is {maximum:.5f} ms at 50 MHz against 24.5 ms; the labelled 100 MHz comparison is {comparison:.5f} ms. The 50 MHz result gains {24.30246-maximum:.5f} ms of margin over the previous 24.30246 ms receipt. The receipt binds the measured firmware and processor. Both shapes pass all five service plans with continuous backing and a largest observed heartbeat gap of {heartbeat:.5f} ms. The derived publication period is at most 250 ms, using a 125 ms eligibility interval plus measured service reserve.

The byte-only control restores the old copy cost. Missing-copy, missing-traffic, missing-publication, delayed-recovery and dispatch-removal controls are detected. Simulation checks actual MAC_STATUS and fabric link counters; both queued plans and the device-wait plan show one down/up cycle per shape.

Required local gates return zero at `{head}`: both compiler modes of the full builder bank, all-shape host tests including Arty, firmware census, capture receipt, service checks, CI scope, source and documentation checks, and whitespace. The builder's existing physical-utilization calibration remains explicitly unrun because its report is absent; the absent-compiler mode also records its intentional instrument omission. The only builder edit is the authorized fixture count change from 2 to 4.

The physical switch-cycle rerun remains #599 acceptance 4 after merge. Independent review is pending.
""")
print('Wrote PR-BODY.md',head)
