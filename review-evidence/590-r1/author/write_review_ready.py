"""Prepare the permitted final issue comment from completed evidence."""
from pathlib import Path
import json
import subprocess
out=Path(__file__).parent
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
gates=[]
for name in ('final-gates.json','final-builder-gates.json','final-target-gates.json'):
    gates+=json.loads((out/name).read_text())
assert all(g['head']==head and g['rc']==0 for g in gates)
assert len(gates)==33
receipt=json.loads(Path('tb/verilator/nvm_capture_cpu/measurements.json').read_text())
maximum=max(r['maximum_ms'] for r in receipt['measurements'] if r['shape']=='endstation_ax7101_8x8' and r['cpu_hz']==50000000)
(out/'REVIEW-READY.md').write_text(f"""[A385] REVIEW READY

Commit: `{head}` (local branch `590-592-599-firmware`).

Changed: #590 command-entry, CRC/validation and wipe-boundary service opportunities retain the 250 ms heartbeat rate limit. #592 copies aligned words within closed records and bytes at their edges. #599 publishes PHY link, speed and duplex through MDIO and the existing status CSR; brief latched loss and recovery resolve in the same poll. The builder edit is only the authorized fixture count 2 to 4. The draft commits and resolution-only dev merge are retained; the initialized processor pin is `16be6768f710e79450aace277abacd6c2c3336e5`.

Validation: all 33 recorded gate invocations return rc 0 at the commit above. This includes both full builder modes, the firmware census, the all-shape host self-test including Arty, the capture gate, the service self-test, ten bound service regrades and the dispatch-removal regrade, CI scope, documentation/source gates and whitespace. Exact argument arrays, return codes, log sizes and SHA-256 values are in the final gate manifests and HANDOFF.md.

All six capture arms pass 16/16. The 50 MHz 8x8 maximum is {maximum:.5f} ms against 24.5 ms, leaving {24.5-maximum:.5f} ms. The replaced receipt binds firmware `{receipt['product_firmware_sha256']}` and the merged processor pin. The earlier processor and firmware measurements are historical only.

Both shapes pass all five service plans with continuous backing and heartbeat gaps below 500 ms. The final findings page records every duty, tick placement, UART allowance and the derived 250 ms publication bound. The scheduling calculation reserves the complete measured poll plus nine maximum MDIO transactions. Both queued plans and device-wait show one actual fabric down/up cycle per shape and updated MAC_STATUS. Byte-only, missing-copy, missing-traffic, missing-publication, deferred-recovery and dispatch-removal controls are recorded; portable checks pass 42 grading and 14 flash controls.

Acceptance: #590 and #592 assigned criteria met; #599 criteria 1, 2, 3 and 5 met within the assigned simulation scope. HANDOFF.md and PR-BODY.md are complete in the assigned packet. Neither timing STOP condition occurred.

Open limits: #599 acceptance 4 remains the later physical switch-cycle lane. The builder bank explicitly leaves its existing physical-utilization calibration unrun because its report is absent; absent-compiler mode also records its intentional compiler-dependent omission. Independent review by the assigned reviewers is pending. No push, PR operation, merge to dev or hardware action was performed.
""")
print('Prepared final issue comment',head)
