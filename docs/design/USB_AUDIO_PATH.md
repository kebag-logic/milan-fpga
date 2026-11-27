# Optional USB audio path

This is the desk implementation for [#1021](https://github.com/kebag-logic/milan-fpga/issues/1021).
Its wire contract is [USB audio #9 as merged, 9e5ef16](https://github.com/kebag-logic/usb-audio/blob/9e5ef16cfbbcc26722bfef56081b992a5e8fc89f/docs/AUDIO-FPGA.md).
The [socket allocation](https://github.com/kebag-logic/usb-audio/blob/9e5ef16cfbbcc26722bfef56081b992a5e8fc89f/docs/NETWORK.md)
is shared with [the network attachment, #1020](https://github.com/kebag-logic/milan-fpga/pull/1020).
Physical qualification remains a bench prerequisite.

## Contents

- **[Build ownership](#build-ownership)** -- Select the Arty profile and enforce exclusive bus ownership.
- **[Frame transport](#frame-transport)** -- Preserve whole frames across queues, epochs, and status publication.
- **[Clock qualification and diagnostics](#clock-qualification-and-diagnostics)** -- Qualify interval references and report transport losses.
- **[Desk evidence and remaining bench work](#desk-evidence-and-remaining-bench-work)** -- Separate simulated coverage from remaining physical acceptance.

## Build ownership

The optional audio entry point accepts `--usb-audio` only on Arty, with one
eight-channel stream in each direction, a 48 kHz media grid, and the TDM8
master clock configuration. The audio profile is
`configs/endstation_arty_usbaudio.yaml`; it pins the 8x8 profile digest and
the feedback window to the firmware contract. The board's internal media
oscillator and frame grid remain authoritative. The audio harness owns the
external bus pins instead of the physical audio headers.

The Arty profile uses the existing split control-firmware placement. Its
control image must be linked against the selected image's generated register
and flash maps. The CPU and its bus use the split placement's measured
100 MHz clock; the media and external bus clocks remain unchanged.
This leaves room for the audio transport; the fabric-control
variant exceeds the device's placement capacity even after reducing audio
staging logic. Resource comparisons use the same split profile with audio
enabled and disabled. As in the existing single-stream Milan profile, one
CRF input and output accompany the eight-channel AAF input and output.

`--usb-audio` and `--usb-net` are rejected together before board construction.
Each remains independently selectable. Audio addresses sockets 0, 1 and 3
on A1:A0. The network sockets 5 and 6 need A2 before the attachments can
coexist physically. The network attachment and its build entry point are
unchanged by the audio implementation.

Without `--usb-audio`, the entry point delegates to the existing board build.
The three shared audio blocks default to 24-bit storage. Only the audio
profile selects 32-bit storage, retaining the low subslot byte through the
render queue, capture mapper and AAF serializer. This parameter contract
does not by itself prove identity of complete board images; image comparison
is a separate acceptance item.

## Frame transport

Socket 3 carries complete playback/state records and interval-reference
records. Length and the record discriminator determine boundaries; socket
ready transitions do not. A complete state snapshot crosses to the media
domain atomically. Each PCM FIFO beat contains one complete eight-channel
frame and its epoch. The independent clocks use asynchronous frame FIFOs
and locally synchronized reset release. Decoded clock-health and running
levels register in the media domain before entering the bus synchronizers;
logic hazards between source edges cannot become status or qualification
changes.

USB playback feeds the capture mapper as four ordered 32-bit pairs, followed
by its frame-snapshot strobe. Twelve complete frames prime playback. Before
priming or while inactive, the mapper receives whole silent frames on the
media grid. Playback epoch changes wait until the pair walk finishes.
A transition coincident with the grid emits one whole silent frame.
Every grid event retains its snapshot; transitions insert no gaps.
After priming, an empty grid event inserts one whole silent frame,
increments the gap counter, and sets sticky error. A full playback FIFO
rejects and counts a whole frame while continuing to drain state and reference
traffic. No rate conversion or fractional-sample interpolation is present.

USB capture reads stream zero, logical channels 0 through 7, from the actual
render queue. Four ordered S32BE pairs become one FIFO frame with all subslot
bits retained. A partial render frame is never published. FIFO overflow and
incomplete active render frames count as whole-frame drops and set sticky error.

The packetizer waits for twelve complete frames, then sends nonempty intervals
of at most seven frames, low byte first. Available source-clock frames determine
packet size. Validated 1 kHz observations pace eight service slots; the local
bus clock interpolates scheduling only. It is not the feedback reference.
Ordinary backpressure retains the packet and word index. A missed service
slot is counted. A changed capture epoch abandons the partial packet, discards
old-epoch FIFO frames, and primes anew at channel zero. Changing only the
capture epoch does not flush or reprime playback.

The media domain acknowledges the capture epoch after applying it. The bus
domain publishes that acknowledgement in a complete status record before
allowing a new capture packet. Status is scheduled every half millisecond,
including while both audio alternates are inactive. Priority turns between
audio opportunities prevent continuous traffic from starving its ten words.
An unready status socket does not prevent playback/state reads or capture
writes. The service deadline assumes the destination socket is ready. Each status
record and capture interval asserts packet end with its final bus word.

## Clock qualification and diagnostics

A Gray counter timestamps the first interval-record word against the actual
24.576 MHz disciplined media oscillator. Only a completely parsed and validated
record reaches the estimator. The ITP delta conversion is 256/625 oscillator
ticks per timestamp unit. With a 2^13-microframe window, the event difference
is shifted by three into Q16.16 samples per microframe. The reference stride
is eight microframes; sequence and count wrap are explicit modulo arithmetic.

Bad structure, reserved bits, inconsistent raw count, discontinuity, duplicate
or missing sequence, a count step other than eight, a three-millisecond timeout,
or media-clock loss discards the estimator window. Deliveries outside
0.75 to 1.25 milliseconds in source-clock ticks are rejected. A discarded
observation cannot also seed the replacement window. Unqualified feedback
is zero; nominal feedback is never substituted.

The reference watchdog uses the FPGA's own bus clock.
Its three milliseconds include the submission spacing plus margin.
USB interval counts determine reference continuity, including modulo wrap.
Firmware's application timer never supplies reference time.
Watchdog tests accept 2.9 ms and refuse 3 ms.
Their source timestamps remain one millisecond apart.
The separate delivery guard still rejects late source timestamps.
Separate planted defects exercise both sides of that bound.

Two controls default to zero. `armed` releases the coordinated session reset
after the receiver has reset its parsers and queues. `qualified` permits the
lock indication only after physical interval-delivery variation has been
measured and accepted. It does not bypass sequence validation or the complete
measurement window. The desk simulation cannot establish that physical bound.

Diagnostics expose playback drops and gaps, capture drops, reference losses,
rejected playback/state records, digest errors, observed media frames, and
minimum/maximum complete-frame FIFO levels. Minima initialize to 127 until
observed; the low seven bits hold the minimum and the next seven the maximum.
Playback levels are observed on active, primed grid events; capture levels
are observed when a valid frame is available during qualified capture.
Counters saturate. Each diagnostic group crosses to control software as an
atomic snapshot, not independent synchronized bits.

## Desk evidence and remaining bench work

The long-run harness fixes bus/media clocks at a 1:2 ratio.
Their phase stays fixed; only the oscillator is incommensurate.
Playback supplies six frames every 6,250 bus cycles.
Supply and consumption rates match exactly.
It checks full-width channel-distinct samples, stalls, and strict ordering.
It does not test bus/media phase drift or rate mismatch.
The integrated epoch test uses 20 ns and 26 ns clocks.
It changes each direction independently during partial capture intervals.
It also changes capture state during a partial render frame.
Checks cover abandonment, channel-zero restart, and both acknowledgement gates.
Planted bridge defects must fail their named runtime checks.
Grid tests move playback state through all eight walk offsets.
Separate tests exercise reference rejection, raw timestamp correction,
independent epochs, packet fences, phased bus sampling, and the shared AAF
storage paths at both widths. Source-level tests inject decode hazards between
source clock edges across a receiving edge, and check stable changes and reset.
Planted defects must trigger their named runtime
checks; build errors do not count as detections.
The default audio regression runs those bounded tests, both storage widths,
a shortened-window duplex check, and representative reference, epoch, packet
and arbitration defects. The separate `duplex` target retains the full
2^13-microframe qualification window and a 100,000-frame run.

Before routing, the audio placement check requires all 55 pad registers:
sixteen inputs, sixteen outputs, sixteen tristates, six controls and the
forwarded clock. Each register must occupy the input or output logic site
of its own pad. Missing, disconnected, unregistered or misplaced endpoints
stop the build. The default regression includes twelve negative controls of
this check; those controls do not replace the actual placement receipt.
The bus-ready synchronizer retains ordinary hold analysis between its two
same-clock stages under the 2 ns maximum bound. Physical reports include this
pair's setup and hold paths and direct timestamp/FIFO pointer skew results.

Route closure at both speed models, complete-image comparisons, and exact
resource differences require their own recorded results. A successful simulation
does not imply those results. The bench must measure interval latency under load,
coordinate arm/disarm, verify the physical bus timing and capture DMA fence,
and establish bidirectional audio integrity with the real receiver. The extra
address line is an additional prerequisite for concurrent network traffic.
Until that work is accepted, the change relates to #1021 and does not close it.
