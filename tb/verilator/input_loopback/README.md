# Input-mapped loopback wire test

Issue #979; Milan v1.2 5.3.3.8 and IEEE 1722.1-2021 7.2.19.

`make` sends distinct stream/channel/frame values through the real Ethernet
parser, receive monitor, AAF depacketizer, render queue, mapped input RAM,
capture crossbar and AAF packetizer. It compares every capture pair and every
transmitted audio sample with the injected wire events and commanded maps.
The expected frame is the received presentation frame plus one.
No expected sample comes from internal queue or buffer state.

The default shape has eight streams and 63 independent loop destinations.
`make run STREAMS=1 FIRST=8 CHANNELS=8 LEAD=2` tests the 1x1 geometry.
The scoreboard covers cross-stream and reversed-channel mappings, every
loop destination, out-of-range silence, input and output fan-out, REMOVE,
replacement, edits during copying, live clock stop/restart, reset during
activity, bind flush, timestamp wrap and prolonged absence across tag wraps.
The wrapper supplies committed logical maps directly.
The [parent integration test](../input_loopback_dp/README.md) executes mapping commands.
It also checks generated geometry and committed parent connections. This test does not claim a board audio soak.

`python3 mutants.py --output <scratch-directory>` runs a clean control and seven
sequential planted defects. Ignored mappings, wrong bank parity, skipped
copying, ignored invalidation, retained words and an extra frame of latency
and a missing clock-loss flush must each fail the unchanged sample scoreboard. A compilation failure is
not a successful detection.

The builder union includes `test_input_loopback_contract`: both geometries,
page crossing, source identities, key and NAME ceilings, and byte equality
of disabled builder artifacts and descriptor images. Routed resources and
all-corner timing are measured separately and recorded in [PR #987](https://github.com/kebag-logic/milan-fpga/pull/987).

## Retention and capture-clock bounds

The supported out-lead is at most two frames.
Eight pages keep a claimed page throughout its capture walk.
A concurrent domain event cannot overwrite that claimed page.
Larger leads fail elaboration before synthesis.
Expiry precedes page reuse; capture consumes each publication once.

The capture timestamp window includes four datapath clock cycles.
Two cover marker synchronization; two cover timestamp quantization.
It also covers 1000 ppm across the prediction horizon.
That horizon is the out-lead plus one media period.
One additional nanosecond covers integer rounding.
At 100 MHz, the maximum window is 104 ns.
At 50 MHz, it is 144 ns.
Both are below half the 48 kHz media period.
Offsets outside this bound may yield silence.
This bound does not claim sample-rate conversion.

The wire scoreboard does not isolate five defensive guards.
They are bind-only flush, one-shot claim, expiry, backlog, and age.
Combined invalidation and steady scheduling currently mask their removal.
They remain untested defence in depth, not mutation-proven guarantees.

`make bounds` checks both supported shapes.
A signed 1000-ppm ramp carries 84 ns marker jitter.
That is four wrapper clock cycles, leaving rounding margin.
Both ramp signs must pass within the derived window.
Increasing jitter to 87 ns must fail sample comparisons.
An out-lead of three must fail elaboration.
