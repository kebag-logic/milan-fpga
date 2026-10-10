<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# mbx: the packet-mailbox fabric skeleton, through both bus adapters

`make` builds and runs four things, exit 0 = all green:

1. `run-wb`: the checks of [`suite.hpp`](suite.hpp) on `KL_mbx` behind
   `KL_mbx_wb` (Wishbone, the on-chip RISC-V's bus), then the bound-talker
   table's timing checks, which need a stream that can stall;
2. `run-axil`: the same checks on `KL_mbx` behind `KL_mbx_axil` (AXI4-Lite,
   a hard core's bus), then the adapter's own handshake checks
   ([`axil_checks.hpp`](axil_checks.hpp));
3. `run-cosim`: the control-plane firmware (ADP and ACMP) run on the RTL
   and on the host model, one scenario, compared frame by frame; the
   firmware library is rebuilt when any firmware source or header changes,
   and the binary relinked whenever the library is newer, so a firmware-only
   change never runs a stale binary;
4. `run-if2`: the same checks on the contract elaborated for two AVB
   interfaces (`gen_mailbox.py --variant-interfaces 2`, written into
   `obj_if2/gen`, never the tree), through both adapters and on the host
   model ([`model_main.cpp`](model_main.cpp)), so the own-MAC and
   bound-talker checks run on two real interfaces.

`make census` runs [`publication_census.py`](../../../sw/mailbox/publication_census.py)
`--check --selftest` (#665, comments 6092086337, 6094461419, 6097292237 and
6100024293). It elaborates `milan_datapath.sv` with the recipe, the sv2v and
the Yosys of CI's elaboration gate
([`census_elab.py`](../../../sw/mailbox/census_elab.py)), every other module a
blackbox cell, in every shape the builder builds: run.sh's recipe at the
module's default parameters, and each `configs/*.yaml` (five at this head,
from one to eight streams) with its generated header directory, the
parameters `endstation_builder.datapath_params()` states for it and the
define `SYNTHESIS`. It reads each netlist, never the
text, so the form a read is written in does not matter. Its population is the nets
the processor wrapper cell's class-D ports (checked against the wrapper's own
class-D sections) and its started level drive, each with that port as its only
driver. From each net it follows every cell to the first named net, the
read's consumer, and from there every cell and net onward. Only the CSR cell's
read-back inputs and the wrapper cell's GET_STREAM_INFO face, each named by
cell and port, stop it; every other input, every datapath output and a cell
with no output are the wire. Each read must map to a block field or a ruled
exclusion, and a status or answer-face read must stay off the wire, in every
shape; the shapes must agree on the population, the reads and each read's
classes of cone end. Its self-test elaborates a planted copy for each of 116
defects, among them every escaping probe of the reviews and the reads only a
multi-stream or loopback shape builds, each at a shape that builds it, and
plants two in its table; each must be refused by its own words. It then
removes each rule of [`census_rules.py`](../../../sw/mailbox/census_rules.py)
in turn and requires the arms planted against it to be let through. It needs
sv2v and Yosys on `PATH` (or named by `SV2V=` and `YOSYS=`) at the versions
`rtl-fast.yml` pins, and refuses any other, which is why `make` does not run
it and CI runs it in `rtl-fast`'s `publication-census` job; `CENSUS_JOBS=`
sets how many copies elaborate at once (2).

`make mutants` runs [`mutants.py`](mutants.py), every planted RTL defect in
its table; the default `make` runs six of them (one per leaf, one in the
filter's tuple and one in the publication block, `--quick`).

The contract is [`sw/mailbox/mailbox.yaml`](../../../sw/mailbox/mailbox.yaml);
the design is [MAILBOX_SPLIT.md](../../../docs/design/MAILBOX_SPLIT.md).

## Contents

- **[The top and the bench](#the-top-and-the-bench)** -- One KL_mbx behind the adapter HOST_P selects, driven a clock at a time through real bus handshakes.
- **[What the checks expect](#what-the-checks-expect)** -- Each check group and the contract sentence it grades; the same checks also grade the host model; the AXI4-Lite build adds the handshake rules.
- **[The co-simulation](#the-co-simulation)** -- The firmware on the RTL and on the model, one scenario, the same frames at the same millisecond.
- **[Planted defects](#planted-defects)** -- Every RTL defect of the table in a scratch copy, each caught by the check it names, after two positive controls; six run in the default make.
- **[Run](#run)** -- The make targets.

## The top and the bench

[`tb_mbx_top.sv`](tb_mbx_top.sv) is wiring only: one `KL_mbx` and the one
adapter `HOST_P` selects; the other adapter's outputs are driven to zero, so
a check cannot pass through the wrong one. [`bench.hpp`](bench.hpp) drives it
a clock at a time: every host access is a Wishbone or AXI4-Lite transaction
with the bus's own handshake, the ingress stream offers one byte per cycle at
the RTL's pace, the TX sink takes bytes under a programmable ready pattern,
and a modeled millisecond is one `ms_tick_p_i` pulse and 23 idle clocks.
On the AXI4-Lite build every clock is also a structural probe: before the
edge, each AXI input is moved in turn with the clock held (every VALID and
READY flipped, addresses, data and strobes scrambled) and every AXI output
must stay where it was (AMBA AXI, IHI0022H, A3.1.1 and A3.2.1).

## What the checks expect

The expectations are the contract's sentences, and the frames are written
from the clauses ([`frames.hpp`](frames.hpp)), never from the RTL or the
filter table. Register offsets and field positions are the generated
`mbx_contract.h`.

| Group | What is checked |
|---|---|
| R0, R1 | identity and capabilities, reset values (every bound-talker entry included), each writable register's mask (each entry's `BOUND_EID` every bit, `BOUND_EN` one bit, each at its own address), read-only registers ignore writes |
| R2 | a partial-strobe write is refused, counted in BUS_ERR and raises a sticky ERR; a disabled cause leaves the line low; write-1-to-clear |
| F0 to F2 | a closed channel stores nothing; ENTITY_DISCOVER for entity_id 0 or this entity passes, whole, byte k in word 2 + k/4 at bits 8*(k%4); foreign and truncated ADPDUs, and AVAILABLE or DEPARTING with the bound-talker table empty, do not; the RX level and the interrupt follow RX_TAIL |
| C0 to C4 | ACMP by talker or listener entity_id, AECP by target, MAAP range overlap with message types, MSRP and MVRP whole (the MRPDU at byte 14), tagged, foreign and too-short frames nowhere |
| Q0 | the full tuple (lane FC, [product ownership](../../../REQUIREMENTS.md#1-product-ownership)): one valid frame per table row (ADP, ACMP multicast and own unicast, an AECP command and a response, MAAP multicast and a DEFEND to own unicast, MSRP, MVRP) reaches its channel whole and counts nothing |
| Q1 to Q5 | each row's frame changed one element at a time: tagged (no ring, no count); to another destination, under another control EtherType, with the unassigned AVTP subtype `0xFD`, or for MSRP and MVRP as AVTP (no ring, counted once each in `FILTER_MISMATCH`); a non-control EtherType (no count); the identity term refused, both AECP directions included (no ring, no count) |
| Q6 | untagged AAF and CRF, to a stream address, the ADP address and the own MAC, never delivered and counted once each; tagged AAF and CRF counted nothing |
| Q7 | the CONTROLLER_AVAILABLE response for this controller delivered whole; one for another controller dropped even to this target; every message_type sent both ways: even ones pass on target_entity_id only, odd ones on controller_entity_id only |
| Q8 | the own MAC per interface: on every interface index the stream can name, each interface's own MAC passes AECP, the ACMP tolerance and a MAAP DEFEND only on its own interface, with the record's IF that index, and counts once elsewhere; a MAC differing in its high or low part; a rewritten own MAC |
| Q9 | `FILTER_MISMATCH` judges the tuple whatever `FILTER_EN` holds, counts five failures as five, and sets `IRQ_STATUS.ERR`; valid, tagged, identity-refused and short frames leave it and ERR alone |
| Q10 | tuple and identity refusals take no token: a full burst passes after them, the frame past it counts in RATE_DROP |
| Q12 | the adp channel's bound talkers (lane F3 round 2, #665 comment 6029368753): with the table empty no ENTITY_AVAILABLE passes; an enabled entry's talker passes as ENTITY_AVAILABLE and ENTITY_DEPARTING, whole and uncounted, and under no other message_type, ENTITY_DISCOVER included; another talker, an identity differing in either half, a frame that ends inside entity_id (even when its bytes, right-aligned, are an entry) and an entry with `BOUND_EN` clear are dropped uncounted; the last entry, a rewritten entry and every entry at once; DISCOVER's own terms unchanged |
| Q13 | the table read is the arrival interface's: a talker bound on interface i passes there only, with the record's IF i, and on another interface or an index with no interface reaches no ring and counts nothing |
| Q14 to Q17 | the table compared byte by byte as the identity arrives (lane F3 round 3, #665 comment 6032450078): the bound talker right after another talker's frame passes, and right after that one differing in its first identity byte only does not; an identity differing from the entry in any one of its eight bytes is refused; `BOUND_EID_LO`, then `BOUND_EID_HI`, rewritten with `BOUND_EN` still set takes effect; after a reset every entry reads 0 again, an entry enabled with no identity written holds talker 0, and one with `BOUND_EID_HI` alone written holds that word and 0 |
| Q18 to Q21 | the table's timing, on the RTL only (the model's frames arrive whole): a frame stalled inside its identity passes, but not while its entry's `BOUND_EN` is cleared and set again, or set again alone, even with the copy made by the verdict; another entry's words read back while an entry is copied, and both then pass; `BOUND_EID_LO` rewritten at each of 32 clocks after `BOUND_EN` is set again, the new talker passing and the old never |
| Q22, Q23 | the table's interface, on the RTL only (lane F3 round 4, R530-2-F1): on each interface, a bound talker's ENTITY_AVAILABLE with another talker's frame on another index right behind it, so the next frame is presented at the verdict, passes alone with the record's IF its own; with two interfaces, Q19 again on every interface past the first, the owed copy gating that interface's entry |
| Q11 | the MAAP DEFEND (IEEE 1722-2016 B.2.1): a DEFEND to the own MAC delivered whole and uncounted; a PROBE, an ANNOUNCE and every reserved message_type there, and a DEFEND to a foreign unicast, never delivered and counted once each; a DEFEND to the own MAC for a range beside this entity's dropped uncounted; a multicast DEFEND still delivered; a DEFEND cut at byte 14 (no message_type: counted) and at byte 15 (no range: uncounted), then the next DEFEND delivered |
| D0, D1 | the ring fills to its last whole record; a frame the space cannot hold, or one over the channel's limit, counts in RX_DROP and never touches an unread record |
| T0, T1 | the token bucket: a burst of its depth, then one frame per refill period |
| X0, X1 | TX records leave byte for byte under backpressure, in commit order between channels; a wrong KIND, non-zero reserved bits in word 1, an unknown interface, a short or long LEN, or a payload past TX_HEAD is refused once and flushes the ring |
| X2 | commit order across channels: ACMP, ACMP, then AECP committed behind a stalled ACMP frame leave 1, 1, 2; after an SRP frame, AECP, ACMP, ADP leave as committed; SEQ 0xFFFF before 0x0000; equal SEQs round-robin from the channel served last |
| H0 to H2 | a wrong host counter: an RX_TAIL ahead of RX_HEAD stores nothing (RX_DROP), a TX_HEAD a ring ahead of TX_TAIL is refused (TX_ERR), an EVT_TAIL ahead of EVT_HEAD posts nothing; each recovers once back in range |
| E0 to E2 | LINK and GM events with their fields and sequence; a link that flaps while the ring is full posts once, with its level at posting |
| M0 to M2 | a timer expires at its deadline with its arm's tag; a cancel and a replaced arm post nothing; a past deadline expires at once |
| K0 to K2 | no TICK while TICK_CTL.EN is clear; one per period; ticks counted while the ring is full post as one record with the count; clearing EN stops them |
| G0 | GM_HI and DOMAIN read the snapshot GM_LO took |
| P0 to P5 | the publication block (lane F-INT, #665 comments 6088423771 and 6092086337): every register and every `pub_*_o` output 0 after reset; each register keeps its fields only, at its own interface and sink; each field drives its own output, one source's DA gate, licence or declaration bit or one sink's bound or started bit moving only its own; the stream_id taken (`pub_sid_o` while `pub_sid_valid_o`) only while `SID_VALID` is set, `BOUND` apart, in the firmware's write order never half written, and kept through a write that moves `STARTED` alone; a hole of every interface block, an entry's fourth word and the blocks of interface indices the build lacks read 0 and move nothing, uncounted; a partial strobe refused and counted; a reset clears the block |

The AXI4-Lite build then runs the adapter's handshake rules, which a polite
master (AW and W together, BREADY and RREADY high) never exercises:

| Group | What is checked |
|---|---|
| A1, A2 | AW before W and W before AW: each is taken alone, no B before the other half, a read beside the half write sees the old value, and the late half completes the write with one B at the right address |
| A3 | AW, W and AR in one cycle are all taken; one B, one R with the read's own data; a read is answered within 8 clocks while writes keep coming |
| A4 | BVALID and BRESP hold 10 clocks under BREADY low; a second write is taken meanwhile; each write gets exactly one B |
| A5 | RVALID, RDATA and RRESP hold 10 clocks under RREADY low while a second read waits; each read answered once, in order |
| A6 | a reset forgets an AW taken without its W, and a waiting B and R; the bus works after it |
| A7 | four back-to-back writes to four registers, each channel offering its next beat the cycle after its last was taken, with W beside AW and with W 3 clocks ahead: four B each time, and every register reads back its own write's data |
| A0 | no AXI output followed an AXI input inside a cycle, over every clock of the AXI4-Lite run |

The host test runs the same `suite.hpp` on the firmware's mailbox model
([`sw/firmware/ctrl/test`](../../../sw/firmware/ctrl/README.md), arm
`model`), so the model and the RTL answer to one set of expectations; only
Q18 to Q23 are the RTL's alone.
`run-if2` does the same on two interfaces with the RTL and the model built
against one generated header.

## The co-simulation

[`cosim_main.cpp`](cosim_main.cpp) links the firmware (driver, loop, port
layer, ADP, ACMP, the app), compiled as C11 exactly as the target builds it, and
answers `mbx_hal.h` once with Wishbone transactions on the RTL and once with
the host model. One scenario runs on each: a link rise, two advertising
cycles, an ENTITY_DISCOVER, a grandmaster change and a shutdown, 21 modeled
seconds. Lane F3 adds ACMP to it: a BIND_RX the talker never answers (its
response and probe in one pass, the duplicate after TMR_NO_RESP, then
TMR_RETRY), the bound talker's ENTITY_AVAILABLE, which both filters pass
through the bound-talker table the firmware wrote, so TMR_RETRY delays and
probes again (5.5.3.5.30 step 2), GET_TX_STATE, PROBE_TX, GET_RX_STATE and
UNBIND_RX, and two frames both filters refuse, a BIND_RX for another
listener and another talker's ENTITY_AVAILABLE. The firmware's random delays
are seeded from NOW_MS, so the two runs must commit the same frames at the
same millisecond; they do, fourteen frames (five ADP, nine ACMP), and the
model run must carry the nine ACMP frames in the scenario's order. When two frames are committed
in one pass, the RTL run waits for the second one too. It starts on the
stream about 13 clocks after the first one's last byte.

## Planted defects

`mutants.py` copies the RTL to a scratch directory, writes one defect into
the copy, builds this suite with the Makefile's own recipe
(`make print-vflags`) through the adapter the arm names, and requires exit 1
with a `[FAIL]` naming the arm's check. Both adapters' unmodified builds run
first as positive controls. An arm can name two interfaces: its copy then
holds the contract's two-interface package, skeleton and header, which the
generator writes over it, and that variant's two unmodified builds run as
controls too.

| Arm | Defect | Caught by |
|---|---|---|
| `rx-msg-type-ignored` | accept terms ignore message_type | F2, AVAILABLE and DEPARTING not passed |
| `rx-eq-own-is-eq-zero` | eq_own compares with zero | F2, DISCOVER for this entity passes |
| `rx-field-length-unchecked` | a term holds on a truncated field | F2, truncated DISCOVER |
| `rx-writes-past-free-space` | speculative writes ignore the free space | D0, every unread record survives |
| `rx-bucket-never-drains` | a commit takes no token | T0, RATE_DROP |
| `rx-lanes-big-endian` | ring lanes reversed | F1, byte k in word k/4 |
| `rx-subtype-ignored` | classification ignores the tuple's subtype | C0, ACMP by entity_id |
| `tx-reserved-word-unchecked` | a non-zero reserved word is sent | X1, counted once |
| `tx-refusal-no-flush` | a refusal leaves the ring | X1, counted once and flushed |
| `tx-round-robin` | the merge ignores SEQ: round-robin | X2, 1, 1, 2 |
| `tx-seq-wrap-unsigned` | SEQ compared without the modulo | X2, 0xFFFF before 0x0000 |
| `tx-ties-fixed-priority` | equal SEQs from channel 0, not the last served | X2, equal SEQs |
| `evt-rearm-keeps-tag` | a re-arm keeps the old tag | M1, the second arm's tag |
| `evt-cancel-arms` | a cancel arms | M0, no event by +4 ms |
| `evt-tick-count-lost` | the coalesced count restarts at 1 | K1, every tick |
| `top-tick-always-enabled` | TICK_CTL.EN ignored | K0, no TICK while clear |
| `top-gm-hi-live` | GM_HI read live | G0, the snapshot |
| `top-partial-strobe-accepted` | partial strobes written | R2, the register is left |
| `top-irq-ignores-enable` | IRQ_ENABLE ignored | R2, a disabled cause |
| `rx-maap-empty-count-overlaps` | a requested count of 0 overlaps | C2, MAAP overlap |
| `rx-drop-uncounted` | RX_DROP never moves | D0, counts in RX_DROP |
| `rx-refill-slow` | a token per two refill periods | T1, one refill period |
| `tx-lanes-reversed` | TX byte lanes reversed | X0, byte for byte |
| `evt-link-never-posts` | the LINK source never posts | E0, a LINK event |
| `evt-gm-domain-dropped` | the GM event loses its domain | E1, GM DOMAIN |
| `evt-expires-late` | an expiry one millisecond late | M0, at its deadline |
| `top-irq-enable-unmasked` | IRQ_ENABLE keeps undefined bits | R1, IRQ_ENABLE mask |
| `rx-closed-channel-stores` | FILTER_EN ignored | F0, a closed channel stores nothing |
| `rx-second-ethertype-ignored` | a channel's second match tuple (MVRP's EtherType and address) never classifies | C3, MSRP and MVRP |
| `evt-only-exact-deadline` | a deadline already past never expires | M2, at once |
| `wb-address-shifted` | the Wishbone adapter shifts the address | R0, CAPS |
| `axil-read-uses-write-address` | the AXI4-Lite adapter reads at AWADDR | R0, CAPS |
| `axil-arready-follows-awvalid` | ARREADY low while AWVALID is high (combinational) | A0, no output followed an input |
| `axil-awready-waits-for-wvalid` | AWREADY only with WVALID (combinational) | A0, no output followed an input |
| `axil-write-without-w` | a write issued on its AW alone | A1, no B before its W |
| `axil-write-ignores-b-slot` | a write issued while its B waits | A4, one B per write |
| `axil-b-dropped-without-bready` | BVALID lasts one clock | A4, BVALID holds |
| `axil-r-dropped-without-rready` | RVALID lasts one clock | A5, RVALID holds |
| `axil-rdata-follows-port` | RDATA is the mailbox's live port | A5, RDATA holds |
| `axil-read-before-write` | a read and a write issued together | A3, the read's own data |
| `axil-reset-keeps-aw` | a reset keeps a half-taken AW | A6, the AW is forgotten |
| `axil-wready-while-issuing` | WREADY also on the cycle the W slot drains, which then drops the beat | A7, each write's data at its own address |
| `axil-awready-while-issuing` | AWREADY also on the cycle the AW slot drains, which then drops the address | A7, each write's data at its own address |
| `rx-tail-unguarded` | no guard on an RX_TAIL out of range | H0, nothing stored |
| `tx-head-unguarded` | no guard on a TX_HEAD a ring ahead | H1, refused |
| `evt-tail-unguarded` | no guard on an EVT_TAIL out of range | H2, nothing posted |
| `rx-tpid-matches-a-tuple` | a C-tag's TPID taken for any tuple's EtherType | Q1, a tagged MSRP frame reaches no ring |
| `rx-dst-ignored` | the destination MAC never compared | Q2, ADP to another address |
| `rx-multicast-dst-ignored` | a fixed destination never compared | Q2, MSRP at MVRP's address |
| `rx-ethertype-ignored` | the tuple's EtherType never compared | Q3, ADP under another control EtherType |
| `rx-own-any-unicast` | any unicast destination taken for own | Q2, AECP to a foreign unicast |
| `rx-own-mac-of-interface-0` | interface 0's own MAC used on every interface | Q8, another interface's MAC |
| `rx-own-mac-low-word-only` | the own MAC compared on MAC[31:0] only | Q8, a MAC differing in MAC[47:32] |
| `top-own-mac-halves-swapped` | the skeleton hands the filter OWN_MAC's halves in the wrong order | Q0, ACMP own unicast |
| `top-own-mac-hi-read-from-lo` | OWN_MAC_HI reads OWN_MAC_LO | R1, OWN_MAC masks |
| `pkg-aecp-command-only` | the AECP response term dropped from the package (F0's command-only rule) | Q7, CONTROLLER_AVAILABLE response |
| `pkg-aecp-target-term-any-type` | the target term takes any message_type | Q5, a response for another controller |
| `pkg-aecp-controller-term-any-type` | the controller term takes any message_type | Q5, a command for another target |
| `rx-mismatch-never-counted` | FILTER_MISMATCH never moves | Q2, counted once |
| `rx-mismatch-counts-valid` | a frame whose tuple matched counts too | Q0, a valid frame never counts |
| `rx-mismatch-counts-any-ethertype` | every frame matching no tuple counts, tagged ones included | Q1, a tagged frame counts nothing |
| `rx-mismatch-counts-identity-refusals` | an identity refusal counts | Q5, a foreign DISCOVER counts nothing |
| `rx-mismatch-counted-twice` | FILTER_MISMATCH moves by two | Q9, five count five |
| `rx-mismatch-needs-an-open-channel` | nothing counts while every channel is closed | Q9, AAF with every channel closed |
| `rx-short-frame-counted` | a frame that ends before byte 14 counts | Q9, the short frame leaves it |
| `rx-mismatch-sets-no-err` | a mismatch does not set IRQ_STATUS.ERR | Q9, ERR set |
| `rx-refusal-takes-a-token` | a frame refused by the identity term spends a token | Q10, a full burst after the refusals |

The MAAP DEFEND to own unicast (lane FC round 2) adds seven defects, each
planted twice, through Wishbone (the name below) and through AXI4-Lite (the
name with `-axil`), and each caught by Q11 on both:

| Arm | Defect | Caught by |
|---|---|---|
| `pkg-maap-defend-tuple-dropped` | the package drops the DEFEND tuple | Q11, a DEFEND to the own MAC delivered |
| `rx-msg-type-off-by-one` | the tuple's message_type read from byte 14 | Q11, a DEFEND to the own MAC delivered |
| `rx-classified-before-msg-type` | the channel decided at byte 14, before the message_type arrives | Q11, a DEFEND to the own MAC delivered |
| `rx-tuple-msg-type-ignored` | the tuple's message types never compared | Q11, a PROBE to the own MAC reaches no ring |
| `rx-own-unicast-never-counted` | a frame to the own MAC never counts | Q11, a PROBE to the own MAC counted once |
| `rx-defend-any-unicast` | the DEFEND tuple takes any unicast destination | Q11, a DEFEND to a foreign unicast reaches no ring |
| `rx-short-frame-never-classified` | a frame that ends at byte 14 is never decided, so the receive path waits | Q11, the DEFEND cut at byte 14 counted once |

The adp channel's bound talkers (lane F3) add thirty defects, each planted
through both adapters as above; the ones marked so build the two-interface
variant, where only another interface shows them. Round 3 put the table in
distributed RAM, compared byte by byte as the identity arrives: the first
fifteen rows are round 2's twelve rules, planted on the lines that now carry
them, with the skeleton's entry decode and the arrival interface's identity
bytes and copies; the rest are round 3's. The twins in the host model are in
`ctrl_mutants.py`'s table (lane F3's `acmp_mutants.py`):

| Arm | Defect | Caught by |
|---|---|---|
| `pkg-adp-bound-term-dropped` | the package drops the eq_bound term | Q12, a bound talker's AVAILABLE delivered |
| `rx-bound-copy-halves-swapped` | the copier takes BOUND_EID's halves in the wrong order | Q12, a bound talker's AVAILABLE delivered |
| `pkg-adp-bound-term-any-type` | the term takes any message_type | Q12, no other message_type passes |
| `rx-bound-low-word-only` | the flag armed at the fifth identity byte: the entry compared on its low word only | Q12, an identity differing in [63:32] |
| `rx-bound-enable-ignored` | BOUND_EN never read | Q12, an entry with BOUND_EN clear (and F2) |
| `rx-bound-field-length-unchecked` | the term holds on a truncated entity_id | Q12, a frame that ends inside entity_id |
| `rx-bound-first-entry-only` | only entry 0's flag read | Q12, the last entry |
| `rx-bound-entry-write-lands-in-entry-0` | every entry's BOUND_EID words land in entry 0's | R1, each entry at its own address |
| `top-bound-entry-decoded-as-0` | the skeleton decodes every entry as entry 0 | R1, each entry at its own address |
| `top-bound-en-read-from-eid` | BOUND_EN reads BOUND_EID_LO | R1, BOUND_EN keeps EN only |
| `rx-bound-table-of-interface-0` | interface 0's table for every interface index | Q13, an index with no interface |
| `rx-bound-enable-of-interface-0` (two interfaces) | interface 0's BOUND_EN read for every interface | Q13, a talker bound on interface 1 |
| `top-bound-write-ignores-interface` (two interfaces) | the skeleton decodes every interface as interface 0 | Q13 and R1 |
| `rx-bound-taps-of-interface-0` (two interfaces) | interface 0's identity bytes compared for every interface | Q13, a talker bound on interface 1 |
| `rx-bound-copy-into-interface-0` (two interfaces) | the copier shifts interface 1's entries into interface 0's | Q13, a talker bound on interface 1 |
| `rx-bound-byte-index-off-by-one` | identity byte b compared with the entry's byte b + 1 | Q12, a bound talker's AVAILABLE delivered |
| `rx-bound-copy-lanes-reversed` | the copier takes a word's bytes in the wrong lanes | Q12, a bound talker's AVAILABLE delivered |
| `rx-bound-last-byte-uncompared` | the eighth identity byte never compared | Q15, one identity byte differing |
| `rx-bound-flag-never-rearmed` | the match flag never armed again: a refused frame's flag carries into every later frame | Q14, the bound talker right after another talker |
| `rx-bound-flag-carried-into-the-next-frame` | a matched frame's flag stands in for the next frame's first identity byte | Q14, one differing in its first identity byte only |
| `rx-bound-liveness-at-the-verdict-only` | BOUND_EN and the owed copy read at the verdict only | Q18, BOUND_EN cleared and set inside the identity |
| `rx-bound-live-while-owed` | an entry takes part while its copy is owed | Q19, BOUND_EN set again inside the identity |
| `rx-bound-verdict-of-the-presented-interface`, and `-if2` (two interfaces) | the verdict reads the table of the interface presented with the next frame | Q22, the bound talker's frame passes alone |
| `rx-bound-live-reads-interface-0-owed` (two interfaces) | every interface's entries gated by interface 0's owed copies | Q23, interface 1's frame stalled while its copy is owed |
| `rx-bound-copy-not-owed-on-enable` | setting BOUND_EN owes no copy | Q12, a bound talker's AVAILABLE delivered |
| `rx-bound-copy-not-owed-on-rewrite` | a BOUND_EID word written while BOUND_EN is set owes no copy | Q16, the new talker passes |
| `rx-bound-copy-ignores-the-host` | the copier steps while the host holds the read-back memory | Q20, the entry copied meanwhile |
| `rx-bound-copy-not-restarted` | a rewrite during a copy does not start it over | Q21, the new talker passes |
| `rx-bound-scan-skips-the-last-entry` | the copier's scan wraps before the last entry | Q12, the last entry |
| `rx-bound-unwritten-word-copied-raw` | a word not written since the reset copied as stored | Q17, an entry enabled with no identity written |
| `top-bound-unwritten-word-read-raw` | a word not written since the reset read as stored | Q17, every entry reads 0 after a reset |
| `rx-bound-valid-kept-through-reset` | BOUND_EID_LO's written flag kept through a reset | Q17, every entry reads 0 after a reset |

The publication block (lane F-INT) adds fourteen defects in the generated
skeleton, each planted through both adapters; the twins in the host model
are in `ctrl_mutants.py`'s table:

| Arm | Defect | Caught by |
|---|---|---|
| `top-pub-sid-valid-held-high` | `pub_sid_valid_o` held high | P3, the stream_id 0 while SID_VALID is clear |
| `top-pub-sid-halves-swapped` | `pub_sid_o` joins SID_LO above SID_HI | P3, SID_HI:SID_LO with SID_VALID set |
| `top-pub-priority-from-vid` | the priority output takes the VID's bits | P2, every field on its own output |
| `top-pub-bound-from-sid-valid` | `pub_bound_o` takes SID_VALID | P3, BOUND alone on its output |
| `top-pub-domain-unmasked` | SR_DOMAIN keeps the bits between its fields | P1, each register's fields only |
| `top-pub-sink-index-dropped` | every sink's BINDING lands in sink 0's | P1, each entry its own |
| `top-pub-hole-aliases-a-register` | an interface block's holes alias its registers | P4, every hole reads 0 |
| `top-pub-interface-unchecked` (two interfaces) | an interface index past the build aliases another's block | P4, nothing moved |
| `top-pub-partial-strobe-accepted` | a partial strobe writes the block | P4, the partial strobe refused |
| `top-pub-licence-kept-through-reset` | LICENCE not reset | P5, a reset clears the block |
| `top-pub-started-from-bound` | `pub_started_o` takes BOUND | P2, every field on its own output |
| `top-pub-started-not-stored` | BINDING drops STARTED on a write | P1, each register's fields only |
| `top-pub-declarations-from-licence` | `pub_talker_decl_o` takes LICENCE | P2, every field on its own output |
| `top-pub-declarations-kept-through-reset` | TALKER_DECL not reset | P5, a reset clears the block |

## Run

```sh
make -C tb/verilator/mbx
make -C tb/verilator/mbx run-if2
make -C tb/verilator/mbx mutants
make -C tb/verilator/mbx census
```

The pinned Verilator is the repository's (5.050); `VERILATOR=` selects
another.
