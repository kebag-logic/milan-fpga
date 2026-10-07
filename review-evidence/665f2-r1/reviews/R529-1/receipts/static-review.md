R529-1 independent static examination, exact head 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70.

The normative source was IEEE Std 1722-2016 Annex B, printed pages 154-163, identified by SHA-256 in identity.json. The fabric engine was read only as the differential subject and CSR consumer, not as the protocol authority. This receipt records conclusions, not a reasoning transcript.

Table B.7 examination (all cells, including inapplicable ones):

| Event | INITIAL | PROBE | DEFEND | Implementation / executable evidence |
|---|---|---|---|---|
| Begin | Draw/use preferred range; reserve | Ignore | Ignore | maap.c:176-200; InitAndPreferredRangeBounds; public initialization precedes binding |
| Release | No state-table action | Stop probe timer, INITIAL | Stop announce timer, INITIAL | maap.c:203-222; ReleaseLossAndRetry; QueueBoundAndWithdrawal |
| Restart | Draw; ReserveAddress | Inapplicable | Inapplicable | Internal restart at maap.c:113-119 enters INITIAL before reserve; receive-cell tests |
| ReserveAddress | Init count, arm, initial PROBE, enter PROBE | Inapplicable | Inapplicable | Internal reserve at maap.c:103-111; InitialAndThreeRetransmissions |
| rProbe | Ignore | Compare reversed MAC; local lower ignores; otherwise stop/restart | Send DEFEND | maap.c:273-292; TableB7 cases 0/3/6/9/12/15; DefendEchoAndIntersection |
| rDefend | Ignore | Stop/restart irrespective of MAC priority | Compare reversed MAC; local lower ignores; otherwise stop/restart | maap.c:273-292; TableB7 cases 1/4/7/10/13/16 |
| rAnnounce | Ignore | Stop/restart irrespective of MAC priority | Compare reversed MAC; local lower ignores; otherwise stop/restart | maap.c:273-292; TableB7 cases 2/5/8/11/14/17 |
| probeCount zero | Inapplicable | Stop probe, start announce, ANNOUNCE, DEFEND | Inapplicable | maap.c:129-135; exhaustion follows final retransmission; InitialAndThreeRetransmissions |
| announce timer | Inapplicable | Inapplicable | Start timer, ANNOUNCE | maap.c:137-139; InitialAndThreeRetransmissions; one live timer makes wrong-kind expiries unreachable through the adapter |
| probe timer | Inapplicable | Start timer, PROBE, decrement | Inapplicable | maap.c:126-135; stale-expiry guard at :302; adapter slot/tag checks |
| PortOperational | Draw or supplied range; reserve | Stop/restart | Stop/restart | maap.c:224-242; ReleaseLossAndRetry; the application lifetime gate suppresses released instances |

Private Restart/ReserveAddress and count-exhaustion events are folded into helpers; no public entry can inject them in an inapplicable state. The interface adapter supplies only the live timer kind. Eighteen parameterized receive cases are not described here as thirty-three separately executed tests; all thirty-three table cells were inspected, while executable coverage is the named receive matrix plus lifecycle/timer cases.

| Authority | Examined result | Evidence |
|---|---|---|
| B.2.1/Table B.1 | PROBE/ANNOUNCE multicast; DEFEND unicast to PROBE source; source MAC and EtherType; defined type; 16-byte control payload | maap.c:73-94 and :288; complete byte-array tests |
| B.2.3 | Version 1 emitted; known current, older and higher-version messages handled; unknown types discarded; higher-version extensions bounded by actual length | maap.c:254-267; MalformedAndVersionCompatibility |
| B.2.4-.8 | Zero stream ID on TX; requested range echoed; DEFEND contains exact intersection; unused conflict fields zero | maap.c:81-94 and :279-288; DefendEchoAndIntersection; DisjointAdjacentZeroAndDefendRange |
| B.3.3/Table B.8 and B.3.4 | Initial send plus three retransmissions; 500/100 ms and 30000/2000 ms constants; draws 511..589 and 30011..31989 reserve service margins | maap.h:22-28; maap.c:61-70 and :121-140; ConstantsStrictTimersAndSeed; differential timing gap is F2 |
| B.3.5/B.3.6 | Matching range event selection, half-open intersections, DEFEND conflict fields, reversed-octet unsigned priority (equal is not lower); loss cancels stale output | maap.c:244-294; 18 TableB7 cases; ReverseOctetPriority; QueueBoundAndWithdrawal |
| B.3.6.1/B.4 | Seed from low MAC-plus-clock sum; nonzero maximal-period xorshift32; incomplete-bucket rejection; full dynamic pool and last fitting block | maap.c:23-47 and :103-109; UniformDrawRejectsIncompleteBucket; InitAndPreferredRangeBounds |

Bare-metal and architecture examination: all three new C sources use static caller-owned state, fixed-size queues, no heap, no OS API and byte-order-explicit operations. Each send/poll attempts at most two frames. Queue copies are capped by sixteen frames; interface and CSR loops are bounded by generated interface count and eight AAF outputs. Rejection sampling has a finite bound as documented; the host access-count metric does not measure its CPU cost. Public event entries guard reentry; release counts and ignores, debug asserts. The separate debug assertion and release tests were executed.

Mailbox examination: maap_mbx.c uses the FC MAAP channel, each interface's core, timer slot/tag and link state; foreign indices, stale tags and duplicate levels are rejected. Tentative ranges feed the shared hardware envelope, with exact overlap still performed by the indexed core. One/two-interface host tests and the interface-zero planted defect were examined. The actual ctrl_app_start_maap composition omits the MAAP receive IRQ enable: F1.

CSR examination: maap_csr.c:43-69 first clears AAF_CTRL and CRFT_CTRL enables, then clears only fabric MAAP enable; mismatch returns with admission closed. It programs stream zero at 0x658/0x65c, later outputs through STRM_SEL and 0x81c/0x820, CRF at 0x75c/0x760, restores selection, then controls. Checked against REGISTER_MAP.md:950-954,1085-1087,1541-1547,1611-1633; milan_csr.sv:1834-1870; milan_datapath.sv:1939-1999,2104-2113; KL_aaf_packetizer.sv:423-433. Higher-stream words reach the TCTX write port and packetizer; all AAF admissions use the common enable. The register spy and allocation seam tests establish ordered writes and closure. They do not prove target bus completion or in-flight media quiescence, both explicitly deferred in the MAAP README.

Default-build examination: f2-delta.json lists 23 files. No F2 changes touch RTL, register definitions, configurations, placement glue, shipping firmware, or submodule pins. ctrl_app_start remains ADP-only; the MAAP composition is an explicit additional API. The wider 021b9c1f..head diff includes FC changes and was separated at db9aa8c9. No FC-only change was charged to this review.

Documentation examination: frozen issue acceptance and scope decisions; REQUIREMENTS.md:24-52 and MAAP ingress row; FR_NFR.md:368-389,409; MAILBOX_SPLIT.md; ctrl and MAAP READMEs; coverage exclusion table and ratchet; public author HANDOFF/PR body at archive ee59ec82. Claims distinguish model-time assumptions from target, wire, physical calibration and bench proof. No new coverage exclusion is present. The differential's omission of the #686 probe interval delta leaves F2 open under Docs as well as Tests/Conformance. This is a coverage/conformance claim, not wording-only residue.
