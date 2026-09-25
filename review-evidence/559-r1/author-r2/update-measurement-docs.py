from pathlib import Path
import json
root=Path.cwd()
receipt=json.loads((root/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
points={(a['shape'],a['cpu_hz'],a['traffic']):a for a in receipt['measurements']}
small='endstation_ax7101_1x1_tdm8'
large='endstation_ax7101_8x8'
w8=max(points[large,50000000,a]['maximum_ms'] for a in ('on','off'))
w1=max(points[small,50000000,a]['maximum_ms'] for a in ('on','off'))
w100=max(points[large,100000000,a]['maximum_ms'] for a in ('on','off'))
rows=[]
for shape,clock in [(small,50000000),(large,50000000),(large,100000000)]:
 for arm in ('on','off'):
  item=points[shape,clock,arm]
  ticks=[r['sys_cycles'] for r in item['rows']]
  label='1x1' if shape==small else '8x8'
  basis='contract' if clock==50000000 else 'non-contract'
  rows.append(f"| {label} | {clock//1000000} / 100, {basis} | {arm.upper()} | {min(ticks):,} to {max(ticks):,} | {item['minimum_ms']:.5f} to {item['maximum_ms']:.5f} | {49/item['maximum_ms']:.4f}x |")
def effect(shape,clock):
 on=points[shape,clock,'on']['maximum_ms'];off=points[shape,clock,'off']['maximum_ms']
 return on-off,100*(on/off-1)
e8,p8=effect(large,50000000);e1,p1=effect(small,50000000);e100,p100=effect(large,100000000)
text=f"""Timing. MEASURED on 2026-09-25 in the
[product CPU capture harness](../../tb/verilator/nvm_capture_cpu/README.md).
The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112) governs this measurement.
**Hold sizing uses the writer's actual clock.**
The [bare-metal contract](../integration/BAREMETAL_FIRMWARE.md#build-contract) specifies a 50 MHz CPU.
Both shapes use that clock, with aligned system rising edges.
The system timer remains at 100 MHz.
The harness overrides the stale 8x8 configuration explicitly.
[#565](https://github.com/kebag-logic/milan-fpga/issues/565) owns that configuration's reconciliation.
The 100 MHz 8x8 point is a non-contract comparison.

The backend retains its nominal 50 ms hold.
Its free-running millisecond tick gives a 49 ms guaranteed floor.
The first tick can arrive immediately after ARM.
The acceptance limit is therefore 24.5 ms, half that floor.
**The worst 8x8 measurement is {w8:.5f} ms.**
This gives {49/w8:.4f}x margin against the guaranteed floor.
It leaves {24.5-w8:.5f} ms below the assigned limit.
The first remedy applies only while measured inputs remain unchanged.
Product firmware, RTL and builder census lists remain unchanged.

Each point contains 16 captures per traffic arm.
The published maximum includes every capture in both arms.
The 8x8 overall maximum also exceeds both non-contract arms.
The 1x1 overall maximum is {w1:.5f} ms ({49/w1:.4f}x floor margin).

| Shape | CPU / system MHz, basis | Traffic | System ticks, minimum to maximum | Elapsed ms, minimum to maximum | 49 ms / arm maximum |
|---|---|---|---|---|---|
{chr(10).join(rows)}

The full closed-record census is 3,218 bytes / 53 records at 1x1.
At 8x8 it is 12,634 bytes / 156 records.
That includes all 4,672 output-map bytes.
Materialization does not affect this copy.
An accepted RELOAD closes every allocated backend record.

The harness uses the board's cacheless CPU and product buses.
It retains memory CDC, PP bridges and the DDR controller.
Firmware brackets ARM through successful ATTEST with the system timer.
This includes ownership reads, record walking, copying and the fence.
Instrumentation overhead is included.
Flash prefill and destination poisoning precede ARM.
Every capture checks attestation, closed ownership and every destination byte.

Traffic offers continuous AEM READ_DESCRIPTOR ENTITY 0 requests.
The MAC AXIS driver respects backpressure; TX remains ready.
It applies neither line-rate throttling nor Ethernet inter-frame gaps.
Counters span record walking and copying, ending before ATTEST.
ON requires accepted requests, successful responses and shared-memory read ACKs.
OFF requires zero traffic counts and still grades elapsed time.

The offered load supplies no established worst-case stress bound.
At 50 MHz, 8x8 ON exceeds OFF by {e8:.5f} ms.
That is {p8:.3f}% between their maxima.
The 1x1 difference is {e1:.5f} ms ({p1:.3f}%).
The observed effect is small but measurable.
At 100 MHz, ON is {-e100:.5f} ms faster than OFF.
This is why both arms determine the maximum.

The [harness README](../../tb/verilator/nvm_capture_cpu/README.md#run) provides the complete run matrix.
The [receipt](../../tb/verilator/nvm_capture_cpu/measurements.json) contains all 96 captures and input hashes.
Run the hosted input gate without a compiler or simulation:

```sh
python3 scripts/check_nvm_capture.py
```

It regenerates each shape's tables and expands closed-record inventories.
Bytes, records and CPU clock must match the measured-for values.
Configured CPU and system clocks are checked too.
Firmware edits also require new measurements.
Harness hashes prevent carrying evidence across measurement-path changes.
Named controls alter bytes, records and clocks independently.
A slower OFF fixture must determine the published maximum.
A planted grader ignoring OFF timing fails that fixture.
The OFF timing limit checks equality and one extra tick.
Both simulation controls also detect missing copying and missing traffic.

Measurements retire the six-instructions-per-byte and fifty-instructions-per-record estimates.
They retire ten cycles per instruction and thirty per access.
The estimated two accesses per byte are also retired.
The blanket twofold penalty is retired.
The actual-clock requirement remains; 50 MHz is not retired.
Actual execution, record walking and bus latency are measured directly.

The DDR model retains controller-facing phase and latency settings.
The README names every substituted model, including clocks and UART.
Physical leveling, Ethernet transport and board timing remain outside measurement.
Hold expiry still voids a capture after a mutating grant.
Release and retry preserve safety.
The hold remains below heartbeat and commit deadline limits.
Physical timing and memory ordering remain UNRESOLVED 6.

"""
p=root/'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md';s=p.read_text()
a=s.index('Timing. MEASURED on 2026-09-25');b=s.index('## 19. The executable model',a)
s=s[:a]+text+s[b:]
a=s.index('6. Physical timing remains unmeasured');b=s.index('7. Alarm forgiveness.',a)
u=f"""6. Physical timing remains unmeasured: capture hold, debounce and memory ordering.
   [Section 18](#18-cost) replaces the copy model with product-CPU measurements.
   Both shapes use the contract's 50 MHz CPU and aligned edges.
   Each has 16 captures per traffic arm, ON and OFF.
   The worst 8x8 copy is {w8:.5f} ms across both arms.
   It covers 12,634 bytes and 156 records, including output maps.
   Its margin against the guaranteed 49 ms floor is {49/w8:.4f}x.
   It meets 24.5 ms only under the measured conditions.
   The unchanged nominal 50 ms hold is retained conditionally.
   The 1x1 maximum is {w1:.5f} ms ({49/w1:.4f}x floor margin).
   Both intervals include the complete record walk and attestation.
   The 100 MHz 8x8 comparison is non-contract: {w100:.5f} ms maximum.
   [#565](https://github.com/kebag-logic/milan-fpga/issues/565) owns the stale configuration clock.
   Hold sizing still uses the writer's actual clock.
   The hosted input gate requires unchanged census and clock values.
   Changed product firmware also forces new measurements.
   Traffic effects are quantified in section 18, including small increases.
   These measurements do not establish a general contention bound.
   Instruction/access cost factors and the blanket twofold penalty are retired.
   Physical memory-port ordering remains unmeasured under section 19.
   Debounce remains open under
   [section 14](SAVED_STATE_FASTCONNECT.md#14-what-this-page-does-not-decide).
"""
s=s[:a]+u+s[b:];p.write_text(s)
print('Updated section 18 and UNRESOLVED 6 from the measured receipt.')
