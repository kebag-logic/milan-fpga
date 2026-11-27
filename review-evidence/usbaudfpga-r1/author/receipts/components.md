# USB audio protocol components

Relates to #1021. This is incomplete, unconnected component work.
No product build enables these modules.

The interface is pinned to usb-audio PR #9.
Its revision is `ac23b992d1ca48c0fff70aec2f7d03caea9503d1`.
The eight-channel profile has digest `0xffdc84ff`.

`KL_usbaudio_record` stages complete socket 3 records.
It validates magic, digest, flags and payload length.
It retains every payload bit and both independent epochs.
It drains refused records through their declared lengths.
A consumer must apply epochs before releasing the record.
The consumer must also implement queue flushing and prefill.

`KL_usbaudio_status` serializes one coherent snapshot onto socket 1.
It emits exactly twenty bytes, with a final-word marker.
Sequence advances at completed records, including modulo wrap.
The caller supplies an already-applied capture epoch.
Serialization alone does not implement the acknowledgement fence.
The caller must cross snapshots atomically between clock domains.
It must also request status at least every millisecond.

`KL_usbaudio_feedback` implements the specified measurement window arithmetic.
Its input is an independently qualified USB microframe boundary.
Each boundary carries a coherent cumulative media-event count.
At 8192 intervals, 49152 events produce `0x00060000`.
49153 events produce `0x00060008`.
Unlocked output is zero; locked startup reports nominal.
This module does not establish the interval reference.
Its local clock must never substitute for that reference.

All three modules require synchronous session reset.
They implement no clock-domain crossings or reset-release synchronization.
Those functions belong to the unfinished integration.

## Unresolved integration

The pinned firmware exposes no explicit USB interval counter.
Its application forwards playback records after queue service.
State records report transitions, rather than each microframe.
Capture readiness is a level across four DMA buffers.
Counting its edges requires an independently validated qualification rule.
No such rule is established by these component tests.

The shared network sockets require address line A2.
The documented harness wires A1 and A0 only.
NETWORK.md explicitly leaves the additional assignment unresolved.
The network PR also leaves its bus connection terminated.
These components neither alter nor replace that interface.

The existing render queue stores twenty-four sample bits.
It reconstructs the remaining byte as zero.
The bridge contract requires copying all thirty-two bits.
An optional wider media path remains necessary.

## Component verification

The `usbaudio` RTL suite checks these components independently.
Its simulator executable is supplied through `RTL_SIMULATOR`.
`MDIR` selects build storage; `JOBS` limits compilation parallelism.
The source-defect runner accepts `--engine`, `--out` and `--jobs`.
It requires a new output directory and performs no cleanup.
Each planted defect requires its named runtime assertion.
Compilation failures never count as detected defects.

The record test checks 120000 variable-length records.
Every sample bit, including its low byte, varies.
The status test crosses the complete sequence wrap.
Both tests exercise stalls and interrupted session boundaries.
Feedback tests use deliberately irregular local-clock spacing.

These tests do not establish integrated transport acceptance.
Media queues, capture packets and shared-bus scheduling remain untested.
Every interface rule still needs an integration-level planted defect.
No routed image, resource cost or image identity is claimed.
