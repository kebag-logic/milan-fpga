[A386] Measurement method

Refs #75. Only the assigned findings page changes in the repository.

Identity matches the assigned bitstream, AEM, ROM CRC, flash CRC,
VERSION, ENTITY and CONFIGURATION descriptors. Original census retained.
The initial UART grader passed all ten checks.

The matched CRF pairs use format 041060010000bb80.
Reference output 2 feeds DUT input 1 first.
DUT output 1 then feeds reference input 8.
Only one pair is bound at a time.
Neither clock, rate nor format is changed.

Each cycle starts with about three seconds of capture.
The controller obtains current binding state, disconnects, waits two seconds
from the successful response, then reconnects.
The response and first valid CRF are matched on the tap.
The controller identifier and sequence select the exact successful response.
Stream ID, direction, version, stream-valid bit, type, frequency,
length, timestamp interval, VLAN and priority validate CRF.
The next packet must advance sequence and timestamp.
Observation stops three seconds after resumed traffic reaches the recorder,
or thirty seconds after the successful reconnect response returns.
The thirty-second value caps the restart observation, excluding pre-capture
and the mandated two-second disconnect hold.

All captures are retained, including setup, every numbered cycle and teardown.
The tap hardware nanosecond word is unwrapped against host record timestamps.
Both endpoints use that single tap clock; host clock offset is irrelevant.
Reported nanoseconds express capture resolution, without a calibration claim.
Raw full packets remain under /tmp/a386, indexed by size and SHA-256.

Every MSRP vector is decoded with bounds and endmark checks.
Three-packed events and four-packed listener values are expanded.
LeaveAll counts are type-scoped vectors, not packet counts.
Source MAC and tap direction attribute transmitters to DUT or bridge.
The reference peer is across the bridge; its original MSRP is not tapped.
Stream identities identify the advertised talker behind the bridge.
No observation here proves the peer-side exchange by itself.

Rates divide PDU counts by measured window duration.
Before: first captured frame through DISCONNECT_RX response.
After: CONNECT_RX response through final captured frame.
Resumed: first valid CRF through final captured frame.
The complete capture also includes the two-second unbound interval.

The legacy per-plane MSRP/ACMP counter words are structural zeros.
Their readbacks are retained; wire counts carry traffic evidence.
The aggregate processor diagnostic and stream counters are also retained.
No counter is reset.

All commands run under explicit foreground timeouts.
One process owns each capture action and joins its children.
The bench lock covers that action and is released before analysis.
The temporary capture driver uses the earlier operator's three source hashes.
It is removed with the temporary controller scripts during restoration.

Historical review: the removed context module was under ieee8021q/srp,
not the path in the old issue refinement. The August 10 tree was read
without checkout. Its received-LeaveAll arm directly queued refresh.
Current source is the protocol processor's SRP engine.
Phase-1 PR #321 pins six peer LeaveAll cycles to at most 18 PDUs,
at most four per cycle, with Listener Ready every cycle.
This bench run does not change RTL or repeat those simulation gates.

Preparation errors: a nested string prevented initial analysis-script creation.
The following two invocations therefore found no script. No cycle ran.
Corrected scripts were checked against the setup capture before numbered work.
An optional renderer import used an unavailable package; the required
repository renderer and parser are present in the existing documentation environment.

The first policy-gate pass flagged ambiguous capture-drop wording.
The findings now identify capture-host packet drops explicitly.
No validator or acceptance criterion changed.
