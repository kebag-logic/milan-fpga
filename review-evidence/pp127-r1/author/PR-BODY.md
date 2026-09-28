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
no-storm limits remain unchanged. All 33 donor suites pass (1,015,233 checks),
including 1,914 SRP top and 1,215 stream-FSM checks. All 36 mutation runs are detected, covering all 41 new
integration check families. Lint, documentation, matrix, NVM figures and
portability gates return 0.

The parent harness was rebuilt in scratch against `cf4e5c63ab12` without
an RTL counterfactual. Leaves in the early expiry window stop the source for the full
two-second hold. Its original helper that waits for LV still exercises legitimate
LV retention; the deadline-anchored replay tests the reported defect. The parent
consumer needs pin adoption and its CRF frame/STREAM_STOP regression as specified
in the issue; no parent files or hardware were changed.
