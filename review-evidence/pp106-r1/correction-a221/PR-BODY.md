[A221] LeaveAll per attribute type, on transmit and on receive

Closes #106

Branch `106-leaveall-scope`, head `5f8cb1325312002c2c8bda45f30d98abc750ca7c`, ten commits on main `fbc1f715`:
- `9370f8ab` Signal LeaveAll for every registered MSRP attribute type (transmit half)
- `fc155c3c` Route a received LeaveAll to its own attribute type, once per MRPDU (receive half)
- `87121354` Pin both boundaries of the once-per-MRPDU LeaveAll gate in the decoder suite (correction round 1: R270-F1 = R271-F1)
- `039ec326` Check that a Listener-only LeaveAll never re-declares our Domain (correction round 1: R270-S1)
- `90f4a0f1` Stop crediting a timer restart on a received LeaveAll and track the deviation in #108 (correction round 1: R270-F2, retained by R271)
- `acd44d7f` State the 10.7.5.20 NOTE criterion for the LeaveAll attribute-type constant (correction round 1: R270-S3)
- `27763677` Record the gate-boundary and Domain-negative failing arms in the suite READMEs
- `c6149b25` Pin the LeaveAll gate closed to the MRPDU end and re-armed after a padded MRPDU (correction round 2: R271-2 F1)
- `4f240356` Check that neither talker lane's LeaveAll re-declares our Domain (correction round 2: R271-2 S1)
- `5f8cb132` Record the gate-closure, padding re-arm and talker-lane Domain-negative arms in the suite READMEs

Evidence decision: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5797308575
Scope decision adding the receive half: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5798176959
Manager correction (timer premise; call #2 accepted; tracker #108): https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5801278433
Reviews answered by correction round 1: R270-1 https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/107#issuecomment-5801267950 and R271-1 https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/107#issuecomment-5801727037
Reviews of `27763677`: R270-2 POSITIVE https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/107#issuecomment-5803079167 and R271-2 NEGATIVE on F1 (MINOR), answered by correction round 2: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/107#issuecomment-5803168166

## The rule (IEEE 802.1Q-2014, the edition this repository targets)

- §10.7.5.20 NOTE: "The LeaveAll state machine operates on a per-application (not per-Attribute Type) basis, but the LeaveAll message operates on a per-Attribute Type basis. Hence, when the LeaveAll state machine issues a LeaveAll, it must generate a LeaveAll Attribute for each Attribute Type supported by the application concerned."
- §10.8.2.6: "The LeaveAllEvent is interpreted on receipt as a MAD Leave All event to be applied to the state machines for all Attributes of the type defined by the AttributeType field."
- §10.7.5.20 b): rLA! occurs for an Applicant, Registrar or LeaveAll state machine when an MRPDU is received and "2) The PDU contains a Message in which the Attribute Type is the type associated with the state machine."

## Transmit half (`9370f8ab`)

**Before:** an own MSRP LeaveAll MRPDU set LeaveAllEvent on its first VectorHeader only. In the #117 Run B capture that PDU is `[Domain LA=1] [TalkerAdvertise LA=0]`. A bridge that scopes a received LeaveAll by type re-declares only its Domain, and its Listener Ready ages out of our registrar 5 s later.

**Now:**
- The first VectorAttribute of every Attribute Type the application supports carries LeaveAllEvent: MSRP Talker Advertise, Talker Failed, Listener and Domain; MVRP VID. The criterion is the §10.7.5.20 NOTE's "each Attribute Type supported by the application", whatever this participant declares or registers (the Domain type has no registrar here). The `LA_TYPES_MSRP_C = 4'b1111` comment, the encoder and top banners and docs 10 §6.5 now say so (`acd44d7f`; comments and prose only).
- A supported type with no vector in the drain gets its own LeaveAll-only message, after the drained ones and in ascending type order: NumberOfValues 0, a zero FirstValue of the full AttributeLength, no packed events, AttributeListLength = AttributeLength + 4 (§10.8.1.2 BNF; §10.8.2.8 f and g; §10.8.2.10.1 NOTE). These are the bench AVB switch's own bytes and order.
- When the drain already carries every type, only flag bits change; no octet is added.
- An MRPDU without LeaveAll, and the MVRP LeaveAll MRPDU, are byte-identical to before.
- A LeaveAll requested while a drain is writing now goes whole into the next MRPDU. The base encoder cleared it at commit and dropped it.
- The docs' "§10.7.1" citation for LeaveAll scope was wrong; that clause is notational conventions. Fixed in three places.

## Receive half (`fc155c3c`)

**Before:** `KL_srp_decoder` raised one application-wide rLA! at every VectorHeader carrying LeaveAllEvent. The bench AVB switch's LeaveAll MRPDU is `[Listener LA JoinMt/Ready] [Domain LA n=2] [TalkerAdvertise LA n=0] [TalkerFailed LA n=0]`. So the Listener JoinMt re-registered our stream's Listener, the Domain message's strobe moved it back to LV, and it aged out 5 s later. That is Run B burst 2, which ended 5.000 s after the switch's LeaveAll.

**Now:**
- The decoder strobes one lane per Attribute Type: `la_msrp_o[type − 1]`, and `la_mvrp_o` for the VID type. Each lane fires **once per MRPDU**, at the first VectorHeader of its type that carries LeaveAllEvent.
- `KL_srp_top` routes each lane only to the state machines of that type (§10.7.5.20 b)2)):

| Lane | Applicant: rLA! | Registrar: IN → LV |
|---|---|---|
| Talker Advertise | talker source declaring Advertise | listener sink holding an Advertise registration |
| Talker Failed | talker source declaring Failed | listener sink holding a Failed registration |
| Listener | listener sink declaring Listener | talker source's Listener registration |
| Domain | Domain participant re-declares | none (the Domain FSM keeps no registrar) |
| MVRP VID | VLAN participant re-joins | none |

- Applicants are routed by type as well as registrars: §10.7.5.20 b)2) scopes rLA! for "an instance of the Applicant state machine, the Registrar state machine" alike. Both reviews confirmed this (call #1), and the manager's correction lets it stand.
- An own LeaveAll still ages every registrar of its participant (§10.7.9: "Leave All messages generated by this state machine also generate LeaveAll events against all the Applicant and Registrar state machines associated with that Participant").
- The MRP state machines are unchanged: the Table 10-3 and 10-4 transcriptions, Δ13 and the leave-timer plane are untouched. Only the strobe feeding each machine's rLA! changed. MSRP and MVRP lanes still never merge.

**Order within an MRPDU.**
- A type's lane fires at its first flagged VectorHeader. That header precedes its FirstValue and Vector (§10.8.1.2: `VectorAttribute ::= VectorHeader, FirstValue {, Vector}`). §10.8: "A given MRP Participant shall process MRPDUs in the order in which they are received, and shall process the MRP Messages in a PDU in the order in which they were put into the Data Link Service Data Unit (DLSDU)." So the LeaveAll is applied before the events of its own VectorAttribute and of every later one.
- A conformant sender puts the LeaveAll first (§10.6; §10.8 NOTE 2), so for its MRPDUs each type's LeaveAll precedes all of that MRPDU's events of its type.
- **Call #2, accepted by the manager's correction:** a VectorAttribute of type T without LeaveAllEvent ahead of the first one of type T with it, in the same MRPDU, is processed in DLSDU order. Its events come first, then the lane at the flagged VectorHeader, then the flagged vector's events. §10.7.5.20 does not require buffering the MRPDU, and our encoder never sends that layout. `srp_decoder` T pins it.
- Once a type's lane has fired, nothing later in the same MRPDU re-opens its gate: not a message of another type, not a vector of the type without LeaveAllEvent. `srp_decoder` V pins both (correction round 2).
- The gate re-arms at every MRPDU's first byte: after a malformed or tolerance-discarded MRPDU (`srp_decoder` U), and after a well-formed MRPDU followed by minimum-frame padding (`srp_decoder` V3, correction round 2). The V9 route forwards an MRP frame byte-exact to its last octet, so a short LeaveAll MRPDU reaches the decoder padded.

**The LeaveAll timer on receipt: an open deviation, tracked in #108.**
- The own leavealltimer re-arms only at its own expiry; a received LeaveAll does not restart it. That is a deviation from 802.1Q-2014: Table 10-5 (§10.7.9) maps rLA! to "Start leavealltimer" and Passive, and §10.6 says "Reception of a LeaveAll message from another Participant causes the timer to be restarted without generating a message". Milan v1.2 Table 4.3 sets only the timer's range.
- The manager's correction confirms it is a deviation and keeps it out of #106's scope. It is tracked in #108. This PR does not change the timer behaviour.
- docs 10 §6.5 states the deviation with those clauses and points to #108. The `KL_srp_top` banner points to #108 as well.
- `docs/10_RESOURCE_AND_EFFORT.md` no longer lists "no restart or Passive behaviour on a received LeaveAll" among the consumer's defects "where this spec is right". It keeps the 10-15 s randomisation point and says that this spec does not restart the timer either, pointing to 10 §6.5 and #108 (`90f4a0f1`, R270-F2).

**Docs.**
- docs 10 §6.5 states the per-type routing, its order and the timer deviation with the clauses above. The F10.9 note reads "registrars of every flagged Attribute Type enter LV".
- The `KL_srp_top` and `KL_srp_decoder` banners state the per-type routing with the clause.

## Tests

**Transmit half**
- `srp_encoder`, 180 → 556 checks: E7 expects one flag per type; L1 covers all 15 declared-type combinations byte-exact against an independent packer and parser, each compared with the same drain sent without LeaveAll; L2 the switch's wire bytes; L3 to L6 repeated types, MVRP unchanged, mid-drain and start-cycle requests.
- `srp_top` F1: the real own-LeaveAll MRPDU flags every MSRP type once.
- Ten failing arms: 146, 128, 115, 81, 50, 128, 3, 2, 2 and 2 FAIL. Still 556 of 556 at this head.

**Receive half**
- `srp_decoder`, 113 → 190 checks. The harness records every lane strobe and every value event in one timeline, and checks it in full.
  - **P (a):** the bench AVB switch's LeaveAll MRPDU, transcribed byte for byte from the Run B capture (switch port, 47.029619 s, FCS dropped, 109 B): exactly `L3 E3 L4 E4 E4 L1 L2`.
  - **Q (b):** a Domain-only LeaveAll behind a Listener re-declaration: only the Domain lane fires.
  - **R (c):** a Listener-only LeaveAll-only vector: only the Listener lane fires, and there are no events.
  - **S:** two flagged Listener vectors plus a flagged second Listener message fire the lane once; the next MRPDU fires it again; MVRP likewise.
  - **T (correction round 1): only a LeaveAllEvent closes the gate.** T1, one Listener message `[JoinIn] [LA JoinIn] [LA JoinMt]`: `E3 L3 E3 E3`. T2, across messages `[L JoinIn] [Domain LA n=2] [L LA JoinMt]`: `E3 L4 E4 E4 L3 E3`. T3, MVRP `[VID JoinIn] [VID LA JoinIn]`: `E1 M1 E1`.
  - **U (correction round 1): the gate re-arms at the MRPDU after a malformed one.** U1, a flagged Listener vector truncated mid-FirstValue (`L3`, malformed); U2, the AttributeList EndMark alone (`L3 E3`, malformed); U3, a bad AttributeLength after a flagged Listener message, whose discarded Domain LeaveAll never fires (`L3 E3`, malformed); U4, MVRP, an out-of-alphabet digit after a flagged vector (`M1 E1`, malformed). After each, the next well-formed MRPDU's LeaveAll of that type gives its lane again (`L3`, or `M1 E1`).
  - **V (correction round 2): a closed gate stays closed to the MRPDU's end, and re-arms after padding.** Hand-computed:
    - V1, `[L LA JoinIn] [Domain LA n=2] [L LA JoinMt]` (lists 14, 9, 14): `L3 E3 L4 E4 E4 E3`, the Listener and Domain lanes once each. Another type's message does not re-open the Listener gate.
    - V2, one Listener message `[LA JoinIn] [JoinIn] [LA JoinMt]` (list 38 = 3 × 12 + 2): `L3 E3 E3 E3`, the three values in wire order. A vector without LeaveAllEvent after the flagged one does not re-open the gate.
    - V3, a Listener-only LeaveAll MRPDU of 19 octets (ProtocolVersion 1 + AttributeType 1 + AttributeLength 1 + AttributeListLength 2 + VectorHeader 2 + FirstValue 8 + two EndMarks 4; list 12 = 2 + 8 + 2), zero-padded with 27 octets to the 46-octet minimum payload of an untagged frame (64 − 14 header − 4 FCS), fed twice. Each time: exactly `L3` (one Listener lane strobe, no value event, no MVRP strobe), and exactly one done with `pdu_ok` set and `pdu_malformed` clear at the dual EndMark, the 27 pad octets inert, no AttributeListLength mismatch.
- `srp_stream_fsms`, 1005 → 1068 checks: H (each lane alone against every plane), I (a), J (b), K (c).
- `srp_top`, 235 → 255 checks, through the real decoder, FSMs, timer service and PRNG. (The previous body gave the base as 236; it measures 235 at `fbc1f715`, receipt `base-fbc1f715-srp-suites.txt`.) F5 (a), (b) and (c) as before. (c) checks the Domain row's negative: after `sync()` into a clean 200 ms slot, no Domain JoinIn follows a Listener-only LeaveAll before the next periodic re-join (correction round 1, R270-S1). **Correction round 2 (R271-2 S1)** extends it to the two talker lanes, each in its own clean slot: a Talker Advertise LeaveAll (sink 0's Advertise re-declared in the flagged vector, so it stays registered) and a Talker Failed-only LeaveAll are each followed by no Domain JoinIn for 400 ms. Step (c) now ends 7.64 s after the own LeaveAll it starts from. The next own LeaveAll cannot come sooner than about 10 s after that one (the T-MRP-LEAVEALL draw is 10-15 s; here it measures 11.8 s).
- Two existing `srp_top` stimuli (F2, F4) flag every MSRP type, as a conformant peer does; every check was kept.

**Failing arms, correction round 2.** The reviewer's `mutants.py` from R271-2, unmodified (SHA-256 `f15d1953…`, equal to the review's `MANIFEST.sha256`). Each plant goes exactly once into a `git archive` export and runs all four SRP suites (receipts `mutants-base-27763677.txt`, `mutants-head-4f240356.txt`; `4f240356..5f8cb132` changes the two READMEs only):

| Plant | What it plants | at `27763677` | at `4f240356` |
|---|---|---|---|
| K0 | control, no change | CONTROL PASSES (177/556/1068/253) | **CONTROL PASSES** (190/556/1068/255) |
| K5 | gate re-armed at a malformed or unpadded clean end, never after a padded MRPDU | SURVIVED | **KILLED**: srp_decoder 1 of 190 (V3 second MRPDU) |
| K6 | the gate remembers only the last type that fired | SURVIVED | **KILLED**: srp_decoder 2 of 190 (V1) |
| K7 | an unflagged VectorHeader re-opens its type's gate | SURVIVED | **KILLED**: srp_decoder 2 of 190 (V2) |
| K8 | gate re-armed at every message whose type differs from the previous one | SURVIVED | **KILLED**: srp_decoder 2 of 190 (V1) |
| K13 | Domain participant also takes the Talker Advertise lane | SURVIVED | **KILLED**: srp_top 1 of 255 (F5c Talker Advertise LeaveAll) |
| K14 | Domain participant also takes the Talker Failed lane | SURVIVED | **KILLED**: srp_top 1 of 255 (F5c Talker Failed-only LeaveAll) |

The earlier rounds' kills still hold at `4f240356` (receipt `mutants-head-4f240356-prior-kills.txt`): K1 6 of 190 (T1-T3), K3 4 (U1-U4), K10 1 (U4), K12 1 of 255 (F5c Listener-only). Each planted `KL_srp_decoder.sv` SHA-256 for K5-K8 equals the one in R271-2 receipt 03, so the RTL under test is the one reviewed.

**Failing arms, correction round 1** (`scripts/arms.py` of that round, measured at `acd44d7f`/`27763677`): X1/R1 6 of 177 (T1-T3); Y2 2 (T1); X7 4 (U1-U4); R8 4 (U1-U4); Y1 1 (U4); X2/R4 1 of 253 (F5c). Every one survived at `fc155c3c`.

**Failing arms, receive half (`fc155c3c`, measured at 150/1068/252 checks):** RX0-dec 19, RX0-top 5 (F5a, F5b, F5c), D1 21 and 5, D2 8, D3 18, D4 11, T1 13, T2 16, T3 6, T4 2, L1 6, L2 2, L3 3, P1 5, P2 1.

## Gates at `5f8cb132`, with the CI simulator pin 5.050

- `make check`: OK (lint 41 mermaid + 18 wavedrom, links 810, matrix 115 REQ rows, module matrix 86 rows, 0 untested, stale OK).
- `scripts/lint_hdl.sh`: 37 OK, 0 FAIL.
- `scripts/run_suites.sh`, from clean build directories: 30 of 30 suites, 15,479 checks, 0 failing (15,464 at `27763677`; +13 srp_decoder, +2 srp_top).
- `scripts/gen_matrix.py --check`: OK.
- `syn/yosys/run.sh`: 32 tops OK, plus the Xilinx memory map.
- `python3 scripts/check-links.py`: 810 checked, OK.
- `git diff --check fbc1f715..HEAD`: clean. No line added by a correction round carries U+2014.

**RTL:** `git diff 27763677..5f8cb132 -- hdl/` is empty, so correction round 2 changes testbenches and suite READMEs only. Correction round 1 changed RTL comments only.

**Parent consumer gates:** run by the manager at the final parent candidate.

## End-to-end simulation

The #530 harness runs were made at `9370f8ab` (type-scoped bridge: no loss in 60 s; switch-layout bridge: continuous for 300 s). They were not rerun at `fc155c3c` or later. The receive-side mechanism is covered by `srp_top` F5.

## Open, for the owner

1. **Own leavealltimer restart on rLA!** (Table 10-5, §10.6): an open deviation, tracked in #108, not changed here. #29 is an older open issue for the same deviation; linking or closing one of them is the manager's call (R271-1 S2, R270-2 S4).
2. **Not taken; outside the correction rounds' assignments:**
   - the inherited routing gaps, which also survive the base suites:
     - R271-1 S1 R5 = R270-2 S2 = R271-2 K15: the VLAN participant takes the MSRP lanes;
     - R271-1 S1 R10/R11 = R270-2 S1 = R271-2 K16/K17: own LeaveAll dropped from registrar aging;
   - R270-2 S3: 08 F08.4 counts Domain and VID registrars in the T-MRP-LEAVE pool;
   - R271-2 S2 = R270-2 S4: the "its leavealltimer" wording in `docs/10_RESOURCE_AND_EFFORT.md:562`, which should read "this spec's". Round 2 was tests only.
3. **#530 item 2** (the fabric licence from `sr_admitted`): unchanged, per the parent decision.
4. **Parent adoption:** pin the reviewed head only after review, under the standing pin rule. The parent's `docs/traceability/ieee8021q.md` row MRP-5 still states per-application receive semantics.
