[A394]

Closes #127

An own MSRP LeaveAll timer expiry previously moved registrations from IN to LV
before the queued transmission. A valid Listener Leave in that window retained
the streaming licence. Keep expiry intent pending until the encoder accepts the
`sLA` preparation with a reserved transmit slot. That action ages both registrar
arrays and starts both applicant walks; the encoder then collects and emits the
round.

Peer LeaveAll supersedes an unaccepted own action with type-scoped receive
effects. Blocked rounds preserve each walk’s completion, drain full tables and
coalesce repeated expiries. Empty canceled reservations wait for real content or
a later own action. LV + rLv semantics, #108’s timer behavior and processor
top-level ports remain unchanged.

Validation: the phase sweep covers Ready/Ready Failed, sources 0/3/7, both sink
types, exact acceptance edges, peer supersession, reset, mismatched and malformed
input, allocation/TX stalls, full tables, renewal and expiry. Both applicant
tables cover same-edge sLA/join. The original periodic-declaration and six-cycle
no-storm limits remain unchanged.

## Round 2

The default SRP suites now cover encoder-busy peer cancellation, a newer expiry
behind canceled preparation, peer decode at the join opportunity and retained
reservation reuse, and sink-plane Talker Leave at -1/0/+1 acceptance clocks.
They also pin join-tick coalescing and simultaneous MVRP/preparation arbitration.
The canceled empty reservation's shared-slot cost and conditional drain bound
are documented; the link-up case drains in 649 ms against a 1,200 ms bound.

The test driver uses explicit reviewed mutation patches, typed/documented
functions and DUT-cycle bounds. C++ declarations follow the parent rule.
The current default suites pass 1,987 SRP top checks and 562 encoder checks;
all 33 donor suites pass 1,015,312 checks. Lint, documentation, matrix, NVM
figures and portability gates return 0. All 56 mutation arms are killed,
including every reviewer arm, with seven positive controls and all 49 assertion families covered (64/64 campaign checks).
The unchanged parent rule-11, rule-12 and test-evidence gates pass against
`00b5c6c96af5`; no ratchet was raised.

The accepted deadline-anchored parent replay returns 0 at that head: a Leave
in the early expiry window clears ACTIVE throughout the two-second hold.
The original LV-anchored helper remains the documented legitimate post-sLA
control. The original sources, deadline patch, portable runner and recorded
SHA256 hashes are included in the author packet. The full parent consumer set
and CRF frame/STREAM_STOP integration remain with the manager.
