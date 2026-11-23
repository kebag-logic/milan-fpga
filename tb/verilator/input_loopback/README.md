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
The wrapper supplies committed logical maps directly; protocol command
acceptance, atomicity and physical projection remain the existing datapath
render suites' responsibility. This test does not claim a board audio soak.

`python3 mutants.py --output <scratch-directory>` runs a clean control and seven
sequential planted defects. Ignored mappings, wrong bank parity, skipped
copying, ignored invalidation, retained words and an extra frame of latency
and a missing clock-loss flush must each fail the unchanged sample scoreboard. A compilation failure is
not a successful detection.

The builder union includes `test_input_loopback_contract`: both geometries,
page crossing, source identities, key and NAME ceilings, and byte equality
of disabled builder artifacts and descriptor images. Routed resources and
all-corner timing are measured separately and recorded in the review packet.
