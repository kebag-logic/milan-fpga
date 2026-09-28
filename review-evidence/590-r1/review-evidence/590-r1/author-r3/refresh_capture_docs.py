"""Render current capture identities and margins directly from the committed receipt."""
from pathlib import Path
import json
import re

root = Path.cwd()
receipt = json.loads((root/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
measurements = receipt['measurements']
by_key = {(m['shape'], m['cpu_hz'], m['traffic']): m for m in measurements}
def maximum(shape, hz):
    return max(by_key[shape, hz, traffic]['maximum_ms'] for traffic in ('on', 'off'))
small = maximum('endstation_ax7101_1x1_tdm8', 50000000)
large = maximum('endstation_ax7101_8x8', 50000000)
comparison = maximum('endstation_ax7101_8x8', 100000000)
assert large <= 24.5
margin = 24.5-large
gained = 24.30246-large
page = root/'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md'
text = page.read_text()
start = text.index('Timing. MEASURED on ')
end = text.index('The full closed-record census', start)
lines = [f'''Timing. MEASURED on {receipt['date']} in the
[product CPU capture harness](../../tb/verilator/nvm_capture_cpu/README.md).
The [capture procedure](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112) governs the matrix.
The [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5865679172) requires this firmware remeasurement.
Measured commit: `{receipt['base']}`.
Measured tree: `{receipt['tree']}`.
Firmware SHA-256: `{receipt['product_firmware_sha256']}`.
Protocol-processor pin: `{receipt['processor_pins']['protocol-processor']}`.
The receipt's BIOS patch digest is informational provenance.
Native service receipts also bind the installed build inputs.
**Hold sizing uses the writer's actual clock.**
The [bare-metal contract](../integration/BAREMETAL_FIRMWARE.md#build-contract) specifies a 50 MHz CPU.
Both shapes use that clock, with aligned system rising edges.
The system timer remains at 100 MHz.
The 100 MHz 8x8 point is a non-contract comparison.

The backend retains its nominal 50 ms hold.
Its free-running millisecond tick gives a 49 ms guaranteed floor.
The first tick can arrive immediately after ARM.
The acceptance limit is therefore 24.5 ms, half that floor.
**The worst 8x8 measurement is {large:.5f} ms.**
Its floor ratio is {49/large:.4f}x.
The margin to 24.5 ms is {margin:.5f} ms.
The historical pre-word-copy maximum was 24.30246 ms.
The word-copy remedy gains {gained:.5f} ms of margin.
Firmware changed; hold behavior and the record census remain unchanged.
The receipt binds the new firmware, including its startup guard.

Each point contains 16 captures per traffic arm.
The published maximum includes every capture in both arms.
The 1x1 maximum is {small:.5f} ms ({49/small:.4f}x floor ratio).

| Shape | CPU / system MHz, basis | Traffic | Elapsed ms, minimum to maximum | 49 ms / arm maximum |
|---|---|---|---|---|''']
for m in measurements:
    shape = '1x1' if '1x1' in m['shape'] else '8x8'
    basis = 'contract' if m['cpu_hz']==50000000 else 'non-contract'
    lines.append(f"| {shape} | {m['cpu_hz']//1000000} / 100, {basis} | {m['traffic'].upper()} | {m['minimum_ms']:.5f} to {m['maximum_ms']:.5f} | {49/m['maximum_ms']:.4f}x |")
text = text[:start]+'\n'.join(lines)+'\n\n'+text[end:]
start = text.index('The offered load supplies no established worst-case stress bound.')
end = text.index('The [harness README]',start)
text = text[:start]+'''The offered load supplies no established worst-case stress bound.
Both traffic arms contribute to the measured maximum.
Their differences describe these deterministic simulated scenarios only.

'''+text[end:]
start = text.index('6. Physical timing remains unmeasured: capture hold, debounce and memory ordering.')
end = text.index('   Both intervals include', start)
text = text[:start]+f'''6. Physical timing remains unmeasured: capture hold, debounce and memory ordering.
   [Section 18](#18-cost) gives the current receipt's identities and six maxima.
   Both shapes use the contract's 50 MHz CPU and aligned edges.
   Each has 16 captures per traffic arm, ON and OFF.
   The worst 8x8 copy is {large:.5f} ms across both arms.
   It covers 12,634 bytes and 156 records, including output maps.
   Its ratio to the guaranteed 49 ms floor is {49/large:.4f}x.
   The 24.5 ms margin is {margin:.5f} ms.
   The word-copy remedy gains {gained:.5f} ms over historical byte copying.
   The unchanged nominal 50 ms hold is retained conditionally.
   The 1x1 maximum is {small:.5f} ms ({49/small:.4f}x floor ratio).
'''+text[end:]
text = re.sub(r'The 100 MHz 8x8 comparison is non-contract: [0-9.]+ ms maximum\.',
              f'The 100 MHz 8x8 comparison is non-contract: {comparison:.5f} ms maximum.',text)
page.write_text(text)
print(f'Capture docs: 8x8 {large:.5f} ms, margin {margin:.5f} ms, gained {gained:.5f} ms')
