<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Bare-metal MSRP and MVRP

F4 implements SRP on the mailbox using the pinned lwSRP submodule.
The firmware owns interface identity, static storage, admission and output ports.
lwSRP owns the MRP parser, Applicant, Registrar and timers.
The default fabric build and shipping image are unchanged.

## Contents

- **[Composition](#composition)** -- Boot order, allocation and asynchronous ports.
- **[Protocol commitments](#protocol-commitments)** -- Declarations, timers and output ordering.
- **[Evidence](#evidence)** -- Host, freestanding, coverage, mutation and timing checks.
- **[Publication for the split datapath](#publication-for-the-split-datapath)** -- The licence, declarations, slope and Domain written before what promises them.
- **[Processor comparison](#processor-comparison)** -- Reused stimuli and normative differences.
- **[Integration still owed](#integration-still-owed)** -- Application wiring and target release evidence.

## Composition

Generate `srp_entity_gen.h` with `srp_entity.py` from the selected builder config.
Force-include it in every SRP translation unit; there is no fallback shape.
The source and sink counts equal the entity's advertised counts, including CRF.
The shape tests independently compare them with the builder's fabric constants.

Statically allocate `srp_mbx`, `ctrl_pool`, an aligned `SRP_POOL_ARENA_BYTES`
arena and one `srp_source` array per interface.
Initialize the pool with `srp_pool_classes`, then bind it with
`shlan_port_bind_pool` before creating SRP.
Do not rebind or destroy the pool while any participant owns storage.
`shlan_printf` uses the existing optional debug sink.
There is no firmware heap or operating-system dependency.

The pool has two small and two large blocks per interface, plus
`16 + 3 * sources + 4 * sinks` medium blocks per interface.
The arena includes conservative allocator overhead for each block.
Receive-interest filters retain every valid Class A Domain value, output Listener
IDs, bound input Talker IDs and required VLANs.
Quiescent, undeclared MT attributes are reclaimed under Table 10-3 note 11.
`refused` counts unsuccessful attempts, including retries, rather than records.
Exhaustion is counted and refused; it cannot overwrite another reservation.
The pool is a finite capacity, not a claim that arbitrary peer churn always fits.

Initialize the adapter with interface MACs, source TSpecs/allocation state,
link rate, and a licence output callback.
The explicit application composition starts with `ctrl_app_start_maap`.
Initialize SRP on that application's pool using the same interface MACs.
Then call `ctrl_app_attach_srp` before servicing the loop.
Supply ACMP through the application configuration when composing all four modules.
Attachment follows ADP, ACMP and MAAP, retaining each receive and event enable.
It opens SRP reception and its interrupt, and enables centisecond delivery.
SRP owns no one-shot fabric timer slot: lwSRP timers use the shared tick.
The other three modules retain disjoint runs of `MBX_N_IF` slots.
The isolated adapter uses `srp_mbx_attach` before opening its loop.
The composition consumes retained per-sink feedback after SRP returns.
A matching Advertise calls `acmp_tk_registered(sink, false)` and a matching
Failed calls it with `true`, when the sink is SETTLED_NO_RSV.
A continuous kind change calls `acmp_tk_kind_changed(sink, failed)`.
This updates SETTLED_RSV_OK's REGISTERING_FAILED view (Milan Table 5.23).
It neither reprobes nor repeats Table 5.30's EVT_TK_REGISTERED.
Unchanged kinds remain idempotent.
Withdrawal calls `acmp_tk_unregistered(sink)` from SETTLED_RSV_OK.
Each uses the accepted binding on the sink's configured interface.

Feedback retains the latest continuous kind before the first withdrawal.
Consecutive kind changes coalesce as view updates.
The first withdrawal remains latched until composition consumption.
Later registration cannot erase it or replace its preceding kind.
Registration precedes withdrawal when both await delivery.
Withdrawal terminates the binding; subsequent feedback belongs to that retired epoch.
This bounded representation cannot overflow.

Observation follows each wire AttributeEvent and centisecond tick.
Talker indications copy registration kinds into per-sink adapter state.
The receive-interest callback observes the preceding event from those copies.
It never calls its owning application.
This obeys lwSRP's [integrator contract](https://github.com/kebag-logic/lwSRP/blob/08ee86e812a0eb5e1dc6cd61b494d8baf3491348/doc/integrator.md#L324-L326)
and [filter contract](https://github.com/kebag-logic/lwSRP/blob/08ee86e812a0eb5e1dc6cd61b494d8baf3491348/src/include/shish_lan/mrp.h#L292-L294).
Registrar visits run outside callbacks, before and after receive.
A visit walks the registrar only after a change to what it copies (#665).
Such a change is a Talker's indication, a binding, or one of the adapter's own declarations, which rewrite the value of an attribute a registration may share.
A Registrar state change owes no walk (#930): each change of what the walk copies, whether a Talker or a Listener registers and what it registers, comes with an indication, since every Registrar change into or out of MT does (IEEE 802.1Q-2018 Table 10-4) and lwSRP indicates a value changed while it registers.
A Listener's change is copied where lwSRP reports it, as the walk copies that Listener, so it owes no walk either: its indication copies its declaration, and lwSRP's transition observer its presence.
Otherwise it keeps the copies and runs each sink's capture, as a walk would, so a record that changes no registration walks nothing (`srp_mbx.walks` counts the walks).
The receive filter, the indications and the walk compare each StreamID and destination MAC with `same`, an equality test that stops at the first byte that differs, from the last: one talker's StreamIDs differ in their unique ID, the last two bytes (IEEE 802.1Q-2018 35.2.2.8.2), so a record's comparisons no longer pay `memcmp`'s alignment checks and the byte loop that orders a difference (#665).
A Listener is looked up among the sources once a use (`sources_of`), its StreamID compared with a source's only where their last bytes agree, so each other source of the shape costs that one compare and no call ([#665's ruling of 2026-11-20](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7029526172), item 3).
The receive filter recomputes each sink's declaration from the first Talker indication of the receive on, the only change it reads, which marks the interface stale; before it every sink holds what the snapshot before the receive left (same ruling).
The reclaim of freeable attributes is owed only where one may arise, and stays owed while the participant holds the owed frame (same ruling).
lwSRP frees an attribute whose Registrar is MT and whose Applicant is VO, AO or QO, and reports every change of either state to the adapter's observer but an attribute's creation, at VO and MT.
So a change into such a state owes it, and a receive owes it when it created more attributes than left that state, counted by the room for attributes `mrp_rx` took from the pool (an attribute takes a medium or a large block); any other change and receive frees nothing, and makes no walk of the participant's attributes.
Receive return observes the last event, including partial allocation refusal.
Thus atomic JoinIn/JoinMt replacements remain continuous registrations.
Lv then New remains two transitions, even inside one PDU.
Expiry before receive remains visible, as does interface reset.
Poll observation covers a newly accepted binding's existing registrations.
No observer calls ACMP or delivers a port action.

Pending ACMP intent gates obsolete feedback immediately.
Accepted intent retires feedback, even for identical stream identities.
A refused replacement cannot settle from the previous binding's registration.
These serialized entries obey #678 and Milan v1.2 5.5.3.5.42/5.5.3.5.48.
A refreshed healthy Talker keeps the listener settled past TMR_NO_TK.
VID 0 and VID >= 4095 park the request, visible through
`ctrl_app.srp_requests[sink].parked`, until ACMP replaces or withdraws it.
Parking does not keep the loop awake; transient SRP refusals still retry.

Only one adapter may own the library's global centisecond dispatch.
Each fabric TICK record counts elapsed centiseconds; NOW_MS is a separate
millisecond timestamp. Coalesced ticks are drained without dropping elapsed time.
Destroy detaches the adapter, releases all participants and revokes active licences.
Destroy before reinitializing an already initialized instance.
Attach reads each interface's current mailbox link level.
Polling reconciles that level even without another LINK record.
A held DOWN record can disappear when the level recovers.

`ctrl_app_attach_srp` wires the ACMP environment's SRP port into a static
latest-request slot per sink. It refuses a sink count beyond the generated
SRP shape or insufficient loop-poll capacity before attaching anything.
The callback copies bind/unbind intent and forwards it to the original observer.
The observer must not deliver the binding itself or reenter a protocol.
Other ACMP environment callbacks keep their original context.
After SRP's poll returns, a composition poll calls
`srp_mbx_bind(interface, sink, identity, destination, VID)` for pending requests.
The sink index and its configured interface are preserved independently.
An accepted request retires; transient refusal stays pending and keeps the loop awake.
Permanent VID refusal parks until a new ACMP request, as described above.
Unbind or replacement supersedes that sink's previous pending request.
Keep both objects alive until loop service stops, then destroy SRP and the pool.
Recompose the application before attaching another adapter.
A null identity removes a binding; false leaves the old binding unchanged.
Retry after owed transmission commits and retained reception completes or expires.
Bindings may share a StreamID while differing in destination or VID.
The interface reconciles one Listener declaration from all eligible bindings:
Ready contributes 2, AskingFailed contributes 1, and their union is ReadyFailed.
An ineligible binding contributes nothing and cannot withdraw another's request.
Ready contributes only after its own VLAN membership commits.
Shared bindings retain their Listener and VLAN until the final user leaves.
Replacement preserves the shared Applicant state until reconciliation.
Consecutive replacements before service preserve that state too.
Reconciliation withdraws Ready when its last eligible binding disappears.
The final binding preserves the current Domain VID.
Otherwise, it releases its VID regardless of prior eligibility.
All ports are serialized. Output callbacks must enqueue work and return;
they must not synchronously call an input port or advance the loop.
The adapter asserts on reentry in debug builds and counts/refuses it in release.

## Protocol commitments

Each physical interface has independent MSRP and MVRP participants.
The adapter accepts the FC SRP mailbox channel's untagged Ethernet records,
validates destination, EtherType, length and interface, and preserves interface
identity on transmission. The library validates a whole PDU before applying events.
Malformed PDUs increment `malformed`; local allocation refusals increment `refused`.
A refusal retains the complete record in one static buffer.
A link change withdraws the interface's declarations and destroys its participants
in the pass that takes it; the next pass's poll builds new ones, and any number of
resets in a pass builds once. SRP's receive waits until then, so no record meets an
interface with no participants: both halves in one pass cost 110,000 of the 200,000
cycles a pass may take at 8x8/2if (#665, `srp_bounds.h`, the share in `ctrl_loop.h`).
A poll builds one interface at most: both links changing together built both in one
pass of 2.08 ms. The other is built on the next pass, and the interface whose build
waited goes first after that, so neither waits more than one pass for the other, and
SRP's receive waits until both are built. The poll reads whether the interface with the
turn builds before it visits any interface, so this holds whichever index has the turn. The reset also clears `listener_present`,
which the registrar it destroys supplied, so delivery reads no Listener the new
participants have not registered.
Its interface, arrival timestamp and payload remain unchanged.
Later SRP records and binding changes wait behind it.
A poll retries after pending events, ticks and owed output, and only once what
the refusal depends on changed since it (#665): a block the pool returned
(`ctrl_pool_returned`) or an Applicant or Registrar change of the interface's
participants that lwSRP reports (`moved`).
lwSRP refuses a receive only where an allocation fails, and which allocations a
replay asks for follows from the receive filter's answers and the attributes'
existence, values and states. While a receive waits no binding changes and no
declaration or Domain is made, so the filter's inputs hold; an attribute is freed
only by a block returned and created only by one taken, and its value changes only
by a receive or a declaration. A retry with neither changed would meet the same
refusal, so none is made. Even then a retry is made at most once a centisecond
(a TICK dispatched since the last retry), so the retries come at the TICK's rate,
not the passes'. Earlier applied attributes remain applied; replay includes every
later attribute.
Storage recovery completes the payload on the first eligible poll after the pool
frees, or after the next centisecond when a retry was already made in this one.
A continuing allocation refusal expires after 1000 ms from the original arrival.
This local recovery policy allows one periodic interval.
It is checked at each eligible receive attempt, and at each eligible poll with
nothing changed, as the refusal a retry would meet would check it.
A record already delayed in the RX ring gets no fresh retry window.
A failed participant recreation checks the same deadline.
A successful retry takes precedence over expiration; pending events and owed
output still precede that retry.
Expired refusal clears the retained record and increments `rx_discarded` once,
without incrementing `received` or `malformed`.
Earlier applied attributes remain; MRP refresh and aging recover the lost suffix.
Later input on every interface and binding calls can then proceed.
This recovery limit does not enlarge the service bound.
Destroy cancels it; link reset cancels only its interface's record.

A declared output's first declaration is Talker Advertise or Talker Failed
(Milan 5.5.2.7). Admission charges Ethernet overhead and a 75% link-rate
ceiling. Without a DA gate (`sources_valid`), unallocated outputs report
insufficient resources (code 2); bandwidth failures report insufficient
bandwidth (code 1), each with the interface's MAC as the system identifier
(IEEE 802.1Q-2018 35.2.2.8.7, Table 35-6). A registered Ready
or ReadyFailed Listener can enable an admitted output only after the applicable
MVRP Join commits (Milan 4.3.2).

A source declares a Talker attribute only while its SRP parameters are valid
(#895; Milan v1.2 4.3.3.1, 5.3.7.4): MAAP holds its interface's range with no
conflict, and a PROBE_TX_COMMAND for the output was answered in the last 15 s
or a matching Listener is registered. That is the MAAP adapter's DA gate
(`maap_mbx.c`, ACMP's `acmp_declaring`), which the composition's delivery poll
(`ctrl_app_srp.c`) passes each pass to `srp_mbx_gate` with the range's base; the
source's destination is base + n, on its own interface. The entry records a
change and owes THE TRANSMIT's declarations; it calls no lwSRP function and
makes no mailbox access. A call with the gate and base its last call left
returns at once: only init and the entry write the gate and the sources'
destinations, so it would change nothing (`gate_seen`, `gate_base`; the plant
`talker-gate-repeat-ignores-its-base` drops the base from that test). A composition with no gate (the unit fixture) sets
`sources_valid` and declares every source from creation.

A valid source declares at once: Talker Advertise with its destination and
TSpec once admitted, or Talker Failed, code 1, when its bandwidth does not fit.
A source not valid declares nothing. When its parameters lapse, it withdraws:
its licence closes first, its `TALKER_DECL` bit and bandwidth go before the
Leave is sent. MSRP does not support a changed FirstValue on a StreamID (IEEE
802.1Q-2018 35.2.2.8): a source valid again with an unchanged destination
declares at once, while a changed destination waits `SRP_REDECLARE_CS` after
the Leave's request: two nominal longest LeaveAll periods less a JoinTime and
THE TRANSMIT's MRPDU by every source, `CTRL_LOOP_TX_MS`, the most the count's
end leaves before the declaration is on the wire. Both terms are counted inside
the two periods (#956, the owner's decision of 2026-11-21), so the declaration
is made two longest periods less both terms after the request and reaches the
wire no later than 30 s after it. That is 2,977 cs at 1x1/1if (35 ms), 2,973 at
8x8/1if (77 ms) and 2,970 at two interfaces (105 ms), each figure stated for its
shape (THE SHAPES, `ctrl_loop.h`) and held to its row by `flip_grade.py --check`
(`rows_tiers.tx_statements`, and at 8x8/1if `tx_held`, apart from that point's
reported rows;
[#895's ruling of 2026-11-15 on that figure](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6895331865),
items 1 and 2). A destination that changes while valid withdraws the old one
first. 35.2.2.8 asks for at least two LeaveAllTime periods, and 10.7.4.3 draws
each LeaveAll period, nominally, between LeaveAllTime and 1.5 times it, so two
nominal periods span 20 to 30 s. The hold-off spans the nominal longest two,
1.5 times the LeaveAllTime the participants are configured with
(`SRP_LEAVEALL_CS`, 1000 cs, Table 10-7 and Milan v1.2 Table 4.3) each, 3,000 cs
([#665's ruling of 2026-11-19](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7007273447),
item 2; #951), from the request to the wire. #951 added both terms past the two
periods, 3,023 cs at 1x1/1if, so its declaration reached the wire about 30.26 s
after the Leave at 8x8/1if on the flip bench (#956). Milan v1.2 Table 4.3 also
tolerates a leavealltimer up to 15.5 s. The hold-off does not cover that
tolerance: two periods at its upper edge reach 31 s, past the nominal 30 s the
ruling sets. Before #951 the hold-off covered the shortest two, 2,000 cs, and
both terms, as acceptance 2 of #895 words it; any of these still meets
35.2.2.8, which sets only the least. Each source counts its
hold-off down in `held_cs`, 16 bits, and the adapter does not compile with a
hold-off the count cannot hold. An admission change swaps the type in place,
the new type joined
before the old leaves, so a refused join keeps the old. A link reset destroys
the participants with no Leave sent, so the new ones hold a source whose
destination changed before it as its Leave would; an unchanged source declares
again at once. A refused join is declared again with THE TRANSMIT's next
declarations. lwSRP refuses a Leave while the participant holds an MRPDU the
ring refused, which the declarations after THE TRANSMIT's build may meet (a
Domain adoption refused for storage before the build, made after it): the
source then stays declared, its `TALKER_DECL` bit and bandwidth too, and its
withdrawal is owed. THE TRANSMIT's next call meets no frame owed, so its first
declarations take the Leave, and the hold-off starts at the Leave lwSRP took.

Each change of a source's declaration owes its STREAM_OUTPUT's GET_STREAM_INFO
notice (#936). Milan v1.2 5.4.5.2 and Table 5.22 name the Talker declaration
state, the failure code and the stream VLAN ID. IEEE 1722.1-2021 7.5.2 names
"MSRP Talker Advertisements or Failures". The release processor sends one at
each declaration and withdrawal. `declare_sources` compares what it published
with what the output last showed (`shown`, `shown_advertise`, `shown_vid`):

- a source declared or withdrawn;
- a source still declared, its type swapped in place, once the swap is made;
- a source still declared on another VID, an adopted Domain's.

It records each such source in `noticed`. A reset that declares an unchanged
source again records nothing, since the output shows the same. A failed
creation returns before the record, so what it joined is recorded once it
succeeds. A Talker Failed's code follows the source's allocation, which only a
withdrawal changes. The composition's delivery poll takes `noticed` each pass
into `ctrl_app.srp_noticed`, which an attach of SRP clears, so a recomposition
keeps no earlier record. A pass that takes a record reports output owed, so the
loop does not sleep on it (`ctrl_loop.h`, the polls). In the next pass the AECP
bridge raises each source's STREAM_OUTPUT GET_STREAM_INFO event
(`aecp_changed`, type 6). The notice then takes AECP's own path and pacing to
every registered controller (Milan v1.2 5.4.5.1). The CPU budget harness's
`talker-notices` arm times it from the PROBE_TX or the range-losing ANNOUNCE to
the last controller's commit ([`talker_notice.py`](../../../../tb/verilator/ctrl_service_budget/talker_notice.py)).
Tests: `srp_talker.cpp` (`DeclarationAndWithdrawalAreNoticed`,
`TypeSwapIsNoticed`, `AdoptedDomainVidIsNoticed`,
`ResetNoticesNothingUnchanged`), `test_acmp_mbx.cpp`'s
`F936AProbeAndItsExpiryEachNoticeTheSource` and
`F936BThePassThatTakesTheRecordOwesItsNotice`, and `test_aecp.cpp`'s
`SrpDeclarationChangeIsItsStreamOutputsNotice` and
`NoPassIsIdleWhileAStreamOutputsNoticeIsOwed`; plants `talker-notice-*`
(`srp_talker_mutants.py`) and `app-output-notice-*` (`aecp_notice_mutants.py`).

A STREAM_OUTPUT's GET_STREAM_INFO also shows the Listener registered for its
stream on its own interface (#943: REGISTERING, and REGISTERING_FAILED for
Asking Failed) while the face reports the output declaring, its DA gate, and
Table 5.22 names that registration state too, so each change of it owes the
output's notice (#957). lwSRP indicates every registration's start and end,
Ignore at the end (`left`), and every change of a registered Listener's
declaration, so the declaration the indication copies (`listener`, into
`declaration`: Asking Failed, Ready or Ready Failed, Ignore with none) is what
the output shows while its gate is open. Each change of it while the source's
bit of `gate` is set on the interface is recorded in `noticed`, the record a
Talker declaration's change is, so the composition and AECP take it the same
way. MAAP opens a source's gate on its own interface only (`maap_mbx.c`), so a
Listener on another interface records nothing, and behind a closed gate the
face shows neither flag. A Listener declared again unchanged, New or JoinIn,
records nothing, and one registered again after a LeaveAll is not indicated. A
Ready replaced by a Ready Failed is recorded, though its flags are the same,
since the release processor's LISTENER_REG_CHANGE follows the registration
state. A link reset is not recorded here: it closes the output's declaration as
a reset does for the Talker (above). It destroys the interface's participants
and the Listener registrations they hold with no indication, so
`reset_interface` clears `declaration` with `listener_present`: the record then
agrees with what the answer shows, no Listener, and the first registration after
the reset is recorded whatever it declares, the destroyed one's declaration
included. The record and that clear take 44 bytes of code at 8x8/1if (#957).
With THE TRANSMIT's sliced build keeping what came due between its slices
(#956, below), whose build is of interface 0 at compile time at one interface,
the image has 128 bytes of its 34 RAMB36 of `rom` left (139,136 bytes).
Tests: `srp_talker.cpp`'s `ListenerRegistrationChangeIsNoticed` and
`ListenerRegistrationAfterAResetIsNoticed` (each declaration, the link's edges
apart, coalesced into one service and twice over, the other interface's record
kept; at 1x1/1if, 8x8/1if and 8x8/2if) and `test_aecp.cpp`'s
`ListenerRegistrationChangeIsItsStreamOutputsNotice` and
`ListenerRegistrationAfterALinkResetIsItsStreamOutputsNotice` (real Listener
MRPDUs, the notices read on the wire, one with the new flags to every registered
controller, at every output of the 1x1 shape at one and two interfaces and of
the 8x8 at one, and across a link reset at the first output); plants
`talker-registration-*` (`srp_talker_mutants.py`) and `registration-notice-*`
(`aecp_registration_mutants.py`).

A binding declares Ready for a matching Advertise, AskingFailed for a matching
Failed, and withdraws when its retained registration expires.
A talker declares one of the two for a stream and moves directly between them
(IEEE 802.1Q-2018 35.1.2.1). A received JoinIn or JoinMt of one kind replaces a
registered other (35.2.6), as lwSRP does, but lwSRP registers a New beside it.
35.2.6's informative NOTE gives the Talker Failed precedence while both are
registered. Milan v1.2 5.3.8.5 is normative: a Listener declares Ready while a
matching Talker Advertise is received. The
[ruling on #925](https://github.com/kebag-logic/milan-fpga/issues/925#issuecomment-6930043105)
follows it, and the NOTE is a documented departure: while both are registered
the kind registered latest, the talker's current state, decides the declaration
and the kind ACMP sees, and the other decides once the latest leaves. Each New
in turn decides, also one of a kind already registered beside the other.
A Talker Advertise's New over a registered Talker Failed is Ready on the wire
within a JoinTime, as a first registration is, not at the talker's next MRPDU,
whatever other messages follow it in the MRPDU: a change the receive filter's
copy makes owes its transmission as one the registrar walk finds does.
Every binding of a StreamID holds which kind its latest registration was,
whatever its destination, and a binding made later, or one replaced in place,
takes it from them. A StreamID whose last binding ends while both kinds stay
registered is held with its latest (`srp_held`) for its interface's next
binding of it, until either kind leaves or the interface resets; its
registrations' leave timers still run, as the talker's messages for a StreamID
no binding has are ignored. Each registration is an lwSRP attribute in a medium
or large pool block, so half those blocks bound the StreamIDs held, and the
table does not fill. `srp_mbx.cpp`'s `SrpTalkerKinds` and `test_acmp_mbx.cpp`'s
`SrpFeedback` tests hold both replacements, each New in turn, either leave,
coincident registrations in one MRPDU, a replacement before a message that
changes nothing (the Listener declaration and ACMP's GET_RX_STATE), a later
binding, one replaced in place, a final unbinding, the hold's ends and its
interface, each with a planted defect in `srp_kind_mutants.py`. No SRP timer
changes.
Ready follows the accepted MVRP membership request (802.1Q 35.1.2.2).

Startup declares Domain class 6, priority 3, VID 2 and MVRP membership in VID 2.
A valid peer Class A Domain changes the priority and VID; link restart restores
the defaults. A changed VID is reserved before old declarations are withdrawn.
A bound sink retains an old VID it still needs.

| Timer | Configured value | Authority |
|---|---|---|
| JoinTime | 20 centiseconds | IEEE 802.1Q-2018 10.7.11; Milan Table 4.3 |
| LeaveTime | 500 centiseconds | Milan Table 4.3 |
| Periodic | 100 centiseconds | IEEE 802.1Q-2018 10.7.11; Milan Table 4.3 |
| LeaveAll | Integer draw strictly between 1000 and 1500 centiseconds | IEEE 802.1Q-2018 10.7.11 |

Build lwSRP with `LWSRP_MILAN=1` for Milan v1.2 4.2.7.2.2.
Only MSRP opts in: IN/rLv issues Lv and enters MT immediately.
The corresponding Talker licence or Listener request is revoked in that pass.
MVRP retains the generic IEEE 802.1Q Table 10-4 Registrar behavior.
A withdrawal in LV does not restart LeaveTime (#608 and processor #134).
The original five-second deadline revokes the Talker licence.
Temporary storage refusal defers application until capacity returns or the
receive recovery limit expires.
Timer withdrawals retry at each centisecond; retained RX retries at polls.
That delay is measured from the original deadline or arrival.
Exhaustion never grants a fresh service or protocol timing budget.
An over-budget recovery remains a timing failure.
Expiry processing precedes later RX, including a tick still in the event ring.
A subsequent same-pass registration cannot erase the owed stop notification.

An accepted `TX_HEAD` write commits the complete frame and Applicant transition.
A refused send retains identical bytes and interface until accepted.
lwSRP builds each MRPDU in the owed frame itself, after its Ethernet header, so no frame is copied (#665).
The poll builds no MRPDU and declares nothing: THE TRANSMIT does both (`ctrl_loop.h`, #665).
An MRPDU owed takes a tier-2 slice of a pass given whole, the first the loop gives after a pass that left tier 1 no record to take (THE TIERS, `ctrl_loop.h`, #894), so no pass that takes a record carries a build.
What owes that pass: a participant's join count ending, a LeaveAll where no join timer holds it (IEEE 802.1Q 10.7.4.1, Table 10-5), an Applicant moved outside a build with its own join timer idle, a walk that changes a binding's declaration, an unbinding that withdraws a declared Listener or VLAN, a new participant, or the first link up (a binding itself owes none: the walk that finds its declaration does).
lwSRP arms a join timer as it sends and reports no expiry, so the adapter keeps the same count, restarted by what a build sent and by nothing else.
The call makes every interface's declarations, then sends both MRPDUs of the first interface that owes one (`SRP_MBX_TRANSMIT_FRAMES`, `srp_bounds.h`), and the next such pass takes the next interface; then it makes that interface's declarations again, for what a first VLAN send licensed.
A slice holds `CTRL_LOOP_BUILD_MOST` MRPDUs, one at every point (a 950 us slice at 1x1/1if, against 1,010 us for both of an interface's MRPDUs, `CTRL_LOOP_BUILD_PASS_US`; 1,475 us at 8x8/1if against 1,795, each stated for its shape, THE SHAPES in `ctrl_loop.h`): a build the slice cannot hold stops after them, reclaims as the next build would, and resumes in the next slice at the next participant (`tx_resume`) with its declarations already made, so the frames are those of the build made whole (`Srp.ABuildResumedAcrossSlicesSendsTheFramesOfTheBuildMadeWhole`); an interface reset ends the build it was resuming. The pause takes its interface's due, and the build waiting for its next slice is THE TRANSMIT's due and the poll's owed (`tx_owed`, the due and `tx_resume` read whole), so what comes due between the two slices, a join timer's end among the centiseconds dispatched there or a declaration another pass made owed, is owed again once the build ends, as after a build made whole, a build with nothing due between its slices ends owing nothing, what its own sends moved included, and a frame the ring refuses in the second slice stays the poll's with its interface due, as in a build made whole (A3) (#956; `Srp.ABuildPausedBetweenSlicesStaysOwedAndKeepsWhatCameDue`). Before it, the resumed slice's end cleared a due a join timer's end set again between the slices, so a declaration that timer held waited for the next periodic MRPDU, past two longest LeaveAll periods after a withdrawal with the loop held (`Talker.ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsWithTheJoinTimerRunning`, and `EveryPhase/TalkerPhase.*`, every centisecond of a second, the loop held and serviced).
An MRPDU a join, periodic or LeaveAll timer owes now waits for tier 1's records. At 1x1/1if it is held within 49 ms of the centisecond that owes it ([#894's ruling of 2026-11-13](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6840564634), item 1; [its contingent ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6858269025), item 3; [its egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126), item 1): `CTRL_LOOP_TX_BOUND_MS`, the most lateness the MRP timer budget holds, since the join timer is armed as an MRPDU is committed and the armed join time (`CTRL_LOOP_JOIN_CS`, 190 ms, which `SRP_JOIN_CS` configures lwSRP with) plus the lateness and the frame's `T_egress` (`CTRL_LOOP_T_EGRESS_MS`, 1 ms) must stay within Milan Table 4.3's 240 ms. By every source it is 34.00 ms there at the slice rule's 900 us, the last queued notice's bound at 140 ms, at the Talker declarations' costs composed with #894's SET_CONFIGURATION cut and measured again, which `CTRL_LOOP_TX_MS` states as 34 ms, and 35 ms since GET_AS_PATH's read composed with them puts the row at 34.20 (#897) (34.05 at 950 us after the one cut, 33.88 at the composed tables, 33.69 before that cut, 33.64 at 900 us, 33.39 at the edit cut's composed tables, 33.20 before that cut, 33.01 at its own; `rows_tiers.py`, the tx row, which `CTRL_LOOP_TX_MS` states as 35 ms; `ctrl_loop.c` holds it to the bound at compile time; #895), and the flip check holds it with every AECP notice the largest legal one too (txL) ([FR_NFR.md 3.4.1](../../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing)).
Where a slice holds both MRPDUs (`CTRL_LOOP_BUILD_MOST` 2, a slice of at least `CTRL_LOOP_BUILD_PASS_US`; no point's at this tree), a Domain adopted in that call is sent in it, so no poll sees the new VID unlicensed between the adoption and its MVRP commit.
Where a slice holds one (every point), the MVRP MRPDU follows in the next slice and an ordinary pass and its polls may run between the two; the Talker's licence still waits for the MVRP commit (`vlan_sent`; Milan v1.2 4.3.2), as `Srp.ASlicedAdoptionLicensesItsTalkerOnlyOnceItsVlanIsSent` checks with a poll between the slices.
No declaration is made while a retained receive waits, so none takes the room it waits for, and a refused or waiting one is tried again when the join count ends.
A frame a build left owed is the poll's: it sends it, one a pass, in every pass, and no pass goes to a build until it is sent.
The poll reclaims the attributes lwSRP may free, so a record the next pass takes finds the room.
SRP's records are tier 2's first (THE TIERS, `ctrl_loop.h`, #894): a pass takes them only once tier 1's takes left none, in a slice ending `CTRL_LOOP_SLICE_US` after the pass started, a record started only while the slice holds `CTRL_LOOP_SRP_UNIT_US`, stated for each shape (THE SHAPES; at 8x8/1if 375 us, its heaviest record plus 5 %, on #665's final head with its cuts, [#665's ruling of 2026-11-18, re-ruled](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6972255348), item 2b), and a record follows only the events posted before it, by ring position.
The composed burst's last record is a row by every source against SRP's 90 ms (R5, R6; decision D, [`rows_tiers.py`](../../../../tb/verilator/ctrl_service_budget/rows_tiers.py)).
lwSRP's periodic transmission had built all four MRPDUs at two interfaces in one pass of 8.7 ms on the split core, against the share of 2.0 ms (`ctrl_loop.h`).
SRP RX waits behind that owed record; Registrar clocks continue to run.
Each LINK event preserves the lifecycle, including down/up between service passes.
Observed level changes apply the same reset and receive fence.
A repeated UP also recreates state because event coalescing may hide the down edge.
Reset cancels only that interface's owed output and restores the default Domain.
It fences that interface's already published RX prefix at the current RX_HEAD.
Those records are consumed without registration; other interfaces keep their input.
Frames published before lifecycle service are conservatively discarded for that
interface, including frames received after the physical recovery.
Fresh declarations after that fence are required before a licence can restart.
A failed recreation owns neither participant, counts a refusal and retries later;
the surviving interface continues service.

## Evidence

Run the common firmware gate from the repository root:

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
```

The gate requires the exact lwSRP gitlink and compiled source bytes.
`srp_mbx.cpp` runs at the 1x1 and the 8x8 entity, each at one and two
interfaces (#929). Its startup test holds every source of the compiled shape
to its own declaration, Talker Advertise for the allocated one and Talker
Failed, code 2, for each other. Its dispatch test gives its two adapters two
of the shape's pools. The two-interface campaign plants three defects at the
8x8 entity that its two-source 1x1 shape cannot catch.
The pinned SDK distribution is named `ilp32d`; the cacheless core build uses
`-march=rv32i -mabi=ilp32`, as required by #679. The split image
(`ctrl_srp_image.py --layout split`) uses `-march=rv32im`, the split hart's
multiply and divide (#665), and calls no software multiply or divide helper.
Minimal freestanding headers and ELF/runtime checks prevent hosted-libc leakage.
Object totals include the library and adapter; compiler stack frames are reported
separately and do not establish a whole call-chain bound.
`ctrl_srp_image.py` also links a size fixture containing the reachable control loop,
ADP, ACMP, MAAP, mailbox, SRP, binding-delivery queue and their static storage.
`ctrl_image_runtime.py` builds its memory primitives and integer helpers with the
same compiler from externally provisioned Picolibc, compiler-rt and LiteX sources.
Their hashes, commands, ELF sections and symbol sizes accompany the measurement.
The fixture has no board reset entry and observes licences in static storage.
It is size evidence, not a boot or routed-resource result.

```sh
python3 sw/firmware/ctrl/test/ctrl_image_runtime.py --picolibc "$PICOLIBC" \
  --compiler-rt "$COMPILER_RT" --litex-software "$LITEX_SOFTWARE" --output "$RUNTIME"
python3 sw/firmware/ctrl/test/ctrl_srp_image.py \
  --config configs/endstation_ax7101_1x1_tdm8.yaml --interfaces 1 --output "$IMAGE" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
```

Repeat for `endstation_ax7101_8x8.yaml` and two interfaces.
For the base comparison, export its control sources and pass `--without-srp`
with `--ctrl-source "$BASE_CTRL"` to the same fixture and runtime.
The report separates text, read-only data, initialized data, BSS, reserved stack
and alignment; the arena is already in BSS and must not be added twice.
The reserved 8192-byte stack is a measurement assumption, not a call-chain proof.

GoogleTest/GoogleMock exercise one and two interfaces, every shipped entity shape
`ctrl_loop.h` lists (THE SHAPES; at every other the build must be refused in its
`#error`'s words, `srp_arms.all_shapes`), allocation failures, malformed inputs, declaration changes, reset, reentry,
backpressure and timer ordering. The adapter has no coverage exclusions.
`srp_mutants.py` ties each named case to a defect and its failed observable;
build failures do not count as catches.
`srp_binding.hpp` feeds real BIND_RX and PROBE_TX_RESPONSE records through
all four modules, checks deferred delivery, refusal/recovery, expiry, unbind,
replacement and interface/sink isolation, with named plants at both interface counts.
`srp_feedback.hpp` checks both kind changes through GET_RX_STATE responses.
It also checks retained withdrawal and expiry/receive ordering.
Identical-identity supersession cannot reuse an undelivered withdrawal's old kind.
Settled link resets reprobe, including down/up before delivery.
Post-withdrawal kind changes cannot produce obsolete view notifications.
Discovered-talker withdrawals measure the per-sink feedback allowance.
Named plants understate that allowance and remove each delivery guarantee.
`srp_app.cpp` counts actual mailbox accesses in the event, refused-receive,
retained-receive poll, transmitting poll, maximum RX/TX record and full-pass paths.
Each bound term has a named planted understatement at one and two interfaces.
The fixed poll envelope separately measures idle link reads, reset increments
and retained-receive increments: four per interface. Reset and retained receive
are alternative paths, so their conservative sum is not a simultaneous trace.
The publication term (lane F-INT) is measured apart, through the same callbacks:
a reset writes five registers, two as it withdraws and three in the poll of the
next pass that builds, a Domain adoption three and each licence change one,
funded as one reset, one adoption and two changes for each of 16 sources
(`SRP_MBX_PUB_POLL_MAX`, 40 per interface); a LINK event now costs three.
The transmit observer wraps the real `send_pdu` callback and pads library output
to the channel maximum. It measures 383 accesses for the one frame a poll sends,
poll after poll until every participant on every interface has sent once,
preserving the firmware callback and the mailbox driver (#665).
A pass drains eight real event records and another drains two maximum RX records.
Subtracting unrelated published terms checks their funding independently.
The SRP envelope is 1,269 / 1,313 accesses at IF=1/2.
Adding one read in either poll or send fails a named test.
Poll-allocation tests exhaust storage after successful reception.
Separate receive tests exhaust it before accepting a mailbox record.
They cover mixed attributes, partial completion, repeated refusal and recovery.
They also cover interface ordering, link fences and destruction.
The retry-removal plant must fail the retained-payload regressions.
Wire-valid Domain floods exceed the actual pool without artificial exhaustion.
They check later withdrawal and binding progress at one and two interfaces.
Boundary, clock-wrap and failed-recreation cases grade the original deadline.
The bound-removal plant must fail the oversized-record regression.
Higher-version messages and atomic invalid-value rejection have wire cases.

The published lwSRP [Applicant tests](https://github.com/kebag-logic/lwSRP/pull/15)
merged as PR #15 at `9197193e`.
The current pin descends from it and includes branch `f4-applicant-notes`.
`applicant_receive_conditions_follow_link_mode` tests Table 10-3 notes 4/5.
`pending_applicant_joinin_obeys_note_four` adds both link modes in VP.
The `point-to-point-condition`, `pending-point-to-point-condition` and
`shared-in-condition` reversals must fail their named tests.

The H-SRP desk test timestamps the actual mailbox access path at 100 ns per access.
It adds one aggregate 1 ms CPU/preemption allowance and 100 ns uncertainty per
action. It records full elapsed time and subtracts only the applicable normative
Join wait; periodic and Leave expiry start at their original deadlines.
All overhead shares one 10 ms service allowance, the T_svc first proposed in
[FR_NFR 3.4.1](../../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing),
tighter than the 20 ms bound SRP has under the approved budget.
An 11 ms full-ring stall deliberately fails that budget predicate without
restarting the origin when space becomes available.
These are explicit host-envelope assumptions, not measured target execution or
wire-departure latency. Target scheduling, ingress, egress and arbitration must
validate those assumptions and the remaining normative margin before release.

## Publication for the split datapath

The adapter writes the class-D state the split placement's datapath reads in
each interface's publication block of the mailbox (lane F-INT; the
[design page](../../../../docs/design/MAILBOX_SPLIT.md#the-publication-block)):

- `LICENCE`: bit s while source s holds its licence, written before each
  licence change is reported, and cleared before a reset's or destroy's
  revocations are reported.
- `IDLE_SLOPE`: the bandwidth admitted for the interface's sources, Ethernet
  overhead included, written once the sources are declared, before those
  declarations are sent (participant creation, Domain adoption and a moved
  destination's declarations).
- `SR_DOMAIN`: the default Domain, not adopted, at participant creation; the
  adopted one, with ADOPTED set, before the declarations that carry it.
- `TALKER_DECL`: bit s while source s's Talker Advertise or Talker Failed is
  declared, written once every source joined, before those declarations are
  sent (participant creation, Domain adoption and a validity change's
  declarations), cleared for a withdrawn source before its Leave is sent (kept
  while lwSRP refuses that Leave), and cleared before a reset or destroy
  removes the participants holding them. The
  datapath's CRF talker tags its frames only while its bit is set (802.1Q
  35.1.2). A source is declared only while its DA gate is open, as the
  processor declares it (the design page's choices; #895).

The tests read the block as the fabric held it at each SRP record's commit, so
an MRPDU that left before its Domain, slope or declarations were published
fails a named test, a Domain adoption's and a withdrawal's included
(`srp_talker.cpp`, at 1x1/1if and 8x8/2if, with `srp_talker_mutants.py`'s
planted defects, one a rule), a refused withdrawal's Leave on the wire once
lwSRP takes it, and THE TRANSMIT's publications counted within one call
against `srp_bounds.h`'s terms. Through the composition, `test_acmp_mbx.cpp`'s
`SrpGate` tests run at 8x8/2if: a probe declares its source at MAAP's base + n
and the 15 s expiry withdraws it, a registered Listener keeps it declared past
the window, and a range MAAP loses to a peer's ANNOUNCE withdraws it, the new
range's destination declared only after the hold-off, held at 29 s and on
the wire by two nominal longest LeaveAll periods after the conflict, neither at
the two LeaveAllTime periods it was before #951 nor with #951's terms added. A named test refuses each
allocation of a link restart's re-creation in turn, a source's join among
them, so a creation that fails part way and still shows a declaration fails
it too.

## Processor comparison

`srp_reuse.py` verifies each source blob against the processor gitlink before
extracting the SRP-top wire builders and stream-FSM Applicant tables.
`srp_walk.cpp` applies their two-class Domain vector, stream near misses,
Advertise/Failed replacement, Run-B LeaveAll lanes, Applicant startup/received
rows, per-interface Listener registration and truncated frames through the
firmware mailbox. This is a selected wire differential, not an exhaustive walk
of every processor state. The complete original processor suites run separately.

| Difference | Processor stimulus/expectation | Firmware result and authority |
|---|---|---|
| D1, resolved | `srp_stream_fsms` section E expects immediate loss on Talker Lv from IN | Firmware agrees under Milan v1.2 4.2.7.2.2. A later Lv in LV retains the original LeaveTime deadline; the #608 cases remain covered. |
| D2 | Sections B/E encode Listener withdrawal with FourPackedEvent Ignore (0) | Retain the last declaration subtype on Lv. IEEE 802.1Q-2018 35.2.2.7.2: Ignore is not a Listener declaration to register or withdraw. |
| D3 | `KL_srp_listener_fsm.sv` holds one Talker registrar a sink, whose type a registering event of either swaps in place: a Talker Lv of either type on IN unregisters it | With both kinds registered the latest decides; its Lv hands the declaration to the older kind, still registered, and the older's Lv changes nothing (`SrpTalkerKinds.LeaveOfEitherKindLeavesTheOtherDeciding`). The registrations that remain decide (IEEE 802.1Q-2018 35.2.6, Milan v1.2 5.3.8.5, the ruling on #925). |

Milan v1.2 4.2.7.2.2 governs D1; IEEE 802.1Q-2018 35.2.2.7.2 governs D2.
JoinIn/JoinMt replacing Advertise with Failed or the reverse uses 35.2.6. Of a
New beside a registered other kind the latest decides while it stays registered
(Milan v1.2 5.3.8.5 and the ruling on #925, a documented departure from 35.2.6's
informative NOTE), as the processor's in-place type swap takes every
registering event; once one of the two leaves, the two differ (D3).

## Integration still owed

F3 is present in the Round 8 merge base.
The explicit composition now runs ADP, ACMP, MAAP and SRP.
The composition owns ACMP binding-port delivery, cancellation and retries,
plus deferred per-sink SRP registration feedback to ACMP. Neither direction
needs target wiring; the remaining items below do.
Target integration still supplies live stream configuration.
It also connects the existing fabric licence output.
The [target platform](../plat/README.md#the-ports) configures every source at boot from the generated stream table and records each licence; the composition passes MAAP's DA gate to `srp_mbx_gate` (#895).
The desk callback proves output ordering, not a connected target licence register.
The mailbox SoC skeleton also needs its separate target integration and timing
validation. No register-map change is made here.

The split build's transmit path to the wire is held in the RTL
([`make srptx`](../../../../tb/verilator/milan_dp/README.md#the-split-builds-srp-transmit-path-obj_srptx-867), #867).
That covers this adapter's MRPDUs through the SRP transmit ring, `KL_mbx_tx` and
`ctl_tx_mux`: their 10.8 form, the port's source address from reset, the Join
and LeaveAll spacing at egress within T_svc (20 ms) on each side, each requested
transmit opportunity within JoinTime and T_svc, and a full ring that loses
nothing and keeps the order. It also covers the #608 stop and the `LICENCE`
at the policer, the last two only under that check's fixture, which gives
source 0 its allocation at creation. Until the entry above re-declares a
source MAAP has allocated, no split source holds a licence. Each source's
`SRC_SID` is the MAAP adapter's, written before its DA gate opens (#905,
[maap README](../maap/README.md)), and that check's `[SID]` holds a split
talker's stream frames to the stream_id its Talker Advertise declares.

The lwSRP pin is public `main` at `08ee86e8`.
Its PR #18 sends one Message per AttributeType in each MRPDU (IEEE 802.1Q-2018 10.8.1.2).
Decoded events are unchanged; the H-SRP LeaveAll walk reads every vector to each EndMark.
Round 6 adapts to its recoverable receive-allocation contract.
The earlier claim that production needed no adaptation was incorrect.
Two independent reviews, candidate-merge gates and deployment
remain separate obligations; this lane changes neither shipping ownership nor RTL.
