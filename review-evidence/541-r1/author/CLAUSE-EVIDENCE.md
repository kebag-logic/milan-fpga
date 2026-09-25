[A304] Clause verification for #541

Read directly from Milan Specification v1.2, final approved 2023-11-30,
printed pages 36-37 and 112-113, and IEEE 1722-2016, printed pages
112-119 and 171. Local standards copies were used, not prior discussions.

Milan Section 5.3.8.10 requires the Table 5.6 counters for each Stream
Input. Table 5.6 leaves synchronization criteria to the manufacturer.
Its MEDIA_UNLOCKED entry says:

> the definition of “unsynchronized” is left open to each manufacturer.

MEDIA_LOCKED records synchronization events; MEDIA_UNLOCKED records loss
events. Their difference must be zero while unsynchronized, or one while
synchronized. UNSUPPORTED_FORMAT is an observation-interval counter:
an interval containing a format mismatch increments it once. The interval
must not exceed one second. A new binding resets the counters.

Milan Section 7.3.2 says:

> Each PDU shall contain 1 timestamp

Sections 7.3.2-7.3.4 and Table 7.1 select IEEE 1722 Clause 10 CRF,
48 kHz base frequency, interval 96, pull 0, subtype 4, and audio-sample
type 1. Section 7.3.3 requires a Class A reservation. These transport
rules impose no immediate unlock on a malformed PDU.

IEEE 1722-2016 Clause 10.6 describes packet loss:

> the media clock free-wheels until the CRF stream resumes and new CRF timestamps are available.

Clause 10.7 places timestamps ahead by transit and accumulation time,
with clock-period rounding. Its uncertainty note permits free-wheeling
while CRF timestamps and gPTP stabilize. Clauses 10.4.3 and 10.4.5
separately define restart and uncertainty behavior. Informative Annex E.2.1
and E.2.2 also leave lock-event specifics implementation dependent.

Conclusion: the assignment's stop condition is not met. A single profile
validation failure need not clear an established lock. The existing 100 ms
timeout is this implementation's policy, not a Milan-mandated duration.
The rejected PDU sets the UNSUPPORTED_FORMAT interval flag; `fmt_err_o`
increments at interval close. `CRF_STATUS[15:8]` exposes its low eight bits;
AECP GET_COUNTERS exposes all 32 bits. Rejection breaks settling and does
not refresh the accepted-PDU timeout.
