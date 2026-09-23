[R271] NEGATIVE - exact head fc155c3ca28b04c2220bf41ebea9214379210452

R271-1, external independent review of issue #106 / PR #107 (protocol-processor-control-plane-avb-milan),
exact head `fc155c3ca28b04c2220bf41ebea9214379210452`, tree `6bd2fef51217a82f281deb14f3f975e39a6efdc5`,
source base `fbc1f7156d711e5b7f511da8a16d9494256b017b`. Cleared context; reconstructed from public
state only.

**Verdict: NEGATIVE, on two open MINOR findings.** The RTL is conformant and I found no defect in
it. Both halves do what 802.1Q-2014 §10.7.5.20 and §10.8.2.6 require, and the Run B shape is fixed
end to end.

- **R271-F1 (Tests, Robustness), this round's own finding.** Two behaviours of the new
  once-per-MRPDU decoder gate have no test: the unflagged-vector-first layout, whose behaviour docs
  10 §6.5 states, and re-arming the gate after a tolerance discard. A mutant that loses the received
  LeaveAll in either case passes all four SRP suites.
- **R270-F2 (Docs), a concurrent round's finding, retained at this head.**
  `docs/10_RESOURCE_AND_EFFORT.md:554-557` contradicts the new §6.5 on restarting the timer after a
  received LeaveAll. See section 7.

Conformance and RTL are covered clean at this head. Tests, Robustness and Docs stay unclean until
F1 and R270-F2 are closed.

## 1. What was reconstructed, in order

1. Governance: parent `AGENTS.md` and `CONTRIBUTING.md` (milan-fpga @ `5e7eb309`). This donor has
   neither file of its own. Then this repository's `README.md` and `docs/README.md` conventions.
2. Issue #106 body (frozen acceptance) and every comment. That covers the assignment, the author's
   evidence DECISION, the first REVIEW READY, the manager's scope DECISION adding the receive half,
   and REVIEW READY (both halves) with its three points for reviewers. Also PR #107 body.
3. Authorities, read in the 2014 edition text:
   - IEEE 802.1Q-2014: §10.6, §10.7.1, §10.7.4.3, §10.7.5.20 (NOTE and b)1-3), §10.7.6.6, §10.7.9
     with Table 10-5, §10.8 (DLSDU order, NOTE 2), §10.8.1.2 (structure and BNF), §10.8.2.6,
     §10.8.2.8 a-g, §10.8.2.10.1 NOTE, and §5.18.3 (end-station MSRP).
   - Milan v1.2: §4.2.7.1.1 Table 4.3, §4.2.7.1.2, §4.2.7.1.3.
4. `git diff fbc1f715..fc155c3c`: 16 files, +1325/-98, two one-line commits, no trailers. The base is
   an ancestor of the head.
5. Public executable evidence:
   - `kebag-logic/milan-fpga@5e7eb309:review-evidence/pp106-r1/`, both the author and manager
     subtrees.
   - The #117 archive branch, for the capture's provenance.
   - Hosted check runs at the exact head.
6. Prior public review findings on PR #107: read after this verdict and ledger were written
   (section 7).

## 2. Conformance judgement (applied first)

**Transmit (`9370f8ab`, `hdl/srp/KL_srp_encoder.sv`).**

- **Every type flagged.** §10.7.5.20 NOTE: a LeaveAll "must generate a LeaveAll Attribute for each
  Attribute Type supported by the application". `LA_TYPES_MSRP_C = 4'b1111` and
  `LA_TYPES_MVRP_C = 4'b0001` (`:153-154`). The MSRP application supports all four types whatever
  the elaboration, so the constant is right.
- **Where the flag goes.** `la3_w` (`:407`) flags the first VectorHeader of each type.
- **LeaveAll-only messages.** Each registered type with no vector in the drain gets its own message
  (`:411-417`, `:679-686`):
  - NumberOfValues 0;
  - a zero FirstValue at the full AttributeLength (§10.8.2.8 f);
  - LeaveAll set, which is what makes a count of 0 legal (§10.8.2.8 g);
  - no packed octets (§10.8.2.10.1 NOTE; `E_VFV` goes straight to `E_MSGCLOSE`, `:625`);
  - AttributeListLength = AttributeLength + 4.
- **Matches the switch.** These are the bench switch's bytes: `srp_encoder` L2 compares them with
  the capture.
- **Order per type.** Within each type the LeaveAll precedes that type's events, so the per-type
  reading of §10.8 NOTE 2 holds.
- **Unchanged cases.** The no-LeaveAll MRPDU and the MVRP LeaveAll MRPDU are unchanged. I planted
  the base `tb/srp_encoder` against the head RTL: 177/180 pass. The 3 failures are all E7, the
  LeaveAll shape: +75 octets, exactly the two added LeaveAll-only messages (receipts/08).
- **Mid-drain LeaveAll.** A LeaveAll requested mid-drain now waits for the next MRPDU instead of
  being cleared at commit. The start-cycle handshake is correct for both participants, including
  cross-application same-cycle requests (`:539-543`, `:709-712`).
- **Considered, no finding: message order.** The LeaveAll-only messages sit after the declared
  messages rather than at the head of the MRPDU. §10.6 ("at the beginning of the MRPDU") is
  informative, and the normative text (§10.8, §10.7.5.20 b)) is met per type. It is also the bench
  switch's own order: all 9 switch LeaveAll MRPDUs in Run B use it (receipts/02).

**Receive (`fc155c3c`).**

- **Decoder lanes.** `KL_srp_decoder` strobes one lane per Attribute Type (`:205-210`, `:403-409`),
  once per MRPDU. The gate is re-armed at the MRPDU's first byte (`:334`), and the lane fires at the
  first flagged VectorHeader of its type.
  - §10.7.5.20 b) makes rLA! a per-PDU condition on "a Message in which the Attribute Type is the
    type associated with the state machine".
  - §10.8.2.6 scopes it to "all Attributes of the type defined by the AttributeType field".
- **Routing in `KL_srp_top`.** Each lane goes only to its own type's machines: `:347` (Domain lane),
  `:405` (MVRP, unchanged), `:511`, `:594`.
- **FSM planes.** In `KL_srp_talker_fsm.sv:415-420,630` and `KL_srp_listener_fsm.sv:406-420`, each
  applicant takes the lane of the type it declares, and each registrar the lane of the type it
  holds. An own LeaveAll still ages every registrar (§10.7.9).
- **No reordering.** Decoder events and lanes reach the FSMs directly, with no queue between them
  (`KL_srp_top.sv:501-512,582-595`). Within one MRPDU a lane and an event never share a cycle.

**The author's calls for reviewers.**

1. *Applicants routed per type too.* **Confirmed, and required.** §10.7.5.20 defines rLA! "for an
   instance of the Applicant state machine, the Registrar state machine, or the LeaveAll state
   machine", under the same b)2) type condition. The scope decision's word "registrars" does not
   narrow the clause.
2. *The unflagged-vector-first layout is handled in wire order.* **Confirmed conformant.**
   - §10.8 normatively orders processing by DLSDU position. The decision's literal "before that
     MRPDU's attribute events" holds for every layout a sender following §10.6 and §10.8 NOTE 2
     produces.
   - In Run B, 0 of the 18 LeaveAll MRPDUs (9 from the DUT, 9 from the switch) use this layout
     (receipts/02).
   - Exact LeaveAll-first semantics would need the whole MRPDU buffered in front of an
     unback-pressured event path.
   - The head RTL does what §6.5 says for the layout: my probe U1-U3 passes at head (receipts/06).
     It is untested in the PR, though: see F1.
3. *Timer.* The author's reading is correct. Table 10-5 maps rLA! to "Start leavealltimer" and
   Passive, and §10.6 says a received LeaveAll restarts the timer. The scope decision's premise ("as
   the standard's timer rules require") does not hold. The behaviour is unchanged by this PR, open
   issue #29 already tracks it, and §6.5 now documents it as an open deviation. The deviation itself
   is not a finding against the PR. The manager has since corrected the premise and opened #108 as
   its tracker (section 7). The doc contradiction it leaves is R270-F2, retained in section 7.

**Issue acceptance.**

- (1) Scope from the Run B capture. I decoded the published capture independently (receipts/02):
  - 189 MSRP PDUs, 145 from the DUT and 44 from the switch, none malformed;
  - the DUT's 9 LeaveAll MRPDUs flag Domain only;
  - the switch's 9 flag all four types, with NumberOfValues-0 vectors for the types it does not
    declare.

  The `srp_decoder` P transcription equals the switch MRPDU at 47.029619 s byte for byte (109 B).
- (2) Encoding: met, as above.
- (3) Encoder tests with a failing arm per property: met. L1 covers all 15 type subsets, L2 the
  NumberOfValues-0 bytes, and `check_only_flags_differ` the "0 octets added" case. The author's
  arms map M5-M8 to those properties and M9-M12 to the remaining ones.
- Parent consumer gates at the pin: run by the manager (section 9).
- Parent adoption and the #530 silicon rerun: pending, outside this round.

**The 15 receive arms and the transmit arms.** I rebuilt the headline arms myself by planting the
earlier files into copies of the head tree (receipts/05):

- base encoder: `srp_encoder` 146 FAIL;
- the previous decoder: `srp_decoder` 19 FAIL;
- the previous receive side (decoder, both FSMs, top, package): `srp_top` 5 FAIL, exactly F5a, F5b
  and F5c.

All three match the PR. The rest of the author's arm logs are consistent with the PR tables.

**The two changed `srp_top` stimuli (F2, F4).** Justified.

- The old stimuli encoded the per-application reading that the scope decision superseded.
- The base `tb/srp_top` run against the head RTL fails exactly those 5 checks (F2 ×4, F4 ×1), and
  nothing else (receipts/08).
- The assertions are kept.
- F5 now separates the old and new routing, as the RX0-top reproduction shows.

**Donor gates.**

- Manager, at this head:
  - lint: 37 OK, 0 FAIL;
  - `run_suites`: 30/30 suites, 15,436 checks, 0 failing;
  - `make check`: OK, 809 links;
  - `gen_matrix --check`: OK;
  - Yosys: 32 tops OK plus Xilinx, 0 FAIL.
- Hosted, at the exact head: all 6 check runs executed and succeeded (portability, suites and
  docs-gates, once per trigger event). None was skipped.
- Mine, focused:
  - the four SRP suites at head: 150, 556, 1068 and 252 checks, 0 FAIL;
  - the same suites at base: 113, 180, 1005 and 235;
  - lint of the five changed modules: OK;
  - `git diff --check fbc1f715 fc155c3c`: clean.

## 3. Findings

### R271-F1 - MINOR - Tests, Robustness

**Where:**
- `hdl/srp/KL_srp_decoder.sv:205-210` (`la_lane_w`, `la_first_w`), `:334` (gate re-armed at the
  MRPDU's first byte), `:403-409` (lane strobe, `la_done_r` set);
- `docs/architecture/10_srp_engine.md:390-393` (the documented DLSDU-order layout);
- `tb/srp_decoder/sim_main.cpp` P/Q/R/S (`:619-800`), which never feed either case.

**Title:** two behaviours of the new once-per-MRPDU LeaveAll gate are held by no test.

**Authority / evidence:**
- AGENTS.md §6: Tests ("each new test can fail for the defect it claims to detect"; "positive,
  negative, and boundary behavior is covered") and Robustness ("malformed and truncated input";
  "invalid ordering/state").
- 802.1Q-2014 §10.7.5.20 b): rLA! occurs when the PDU contains a Message of the type carrying
  LeaveAll. §10.8: DLSDU order.
- Milan §4.2.7.1.2: tolerance discard.
- The author asked reviewers to judge exactly this layout: point 3 of issue comment 5798883942,
  which the manager's rulings call "call #2".
- Probe R1 (an unflagged vector of type T consumes T's per-MRPDU budget) and probe R8 (the gate is
  re-armed only by a clean dual EndMark) both **survive** all four SRP suites at head: 0 FAIL of
  150, 556, 1068 and 252 (receipts/03_mutants.txt).
- A 9-check disposable decoder probe **passes at head** (receipts/06_decoder_probe.txt). It fails
  under R1 at U1, U2 and U3, where the timeline shows `E3 E3` instead of `E3 L3 E3`. It fails under
  R8 at A2 and A3, where the lane is missing after a truncated MRPDU and after a bad
  AttributeLength.

**Impact:**
- The behaviour §6.5 promises for that layout, and the gate's re-arm after a tolerance discard, have
  no executable check.
- A regression in either would silently lose a peer's LeaveAll for one attribute type: every
  LeaveAll in that layout under R1, and the next MRPDU's LeaveAll after a malformed one under R8.
- Stale registrations would then outlive a LeaveAll cycle while every suite stays green.

**Required outcome:** a suite checks, through the strobe timeline:
- (i) a type-T vector without LeaveAllEvent ahead of the first flagged type-T vector in one MRPDU
  gives the unflagged vector's events, then the lane once, then the flagged vector's events. This
  must be checked within one message, across messages, and for MVRP.
- (ii) after an MRPDU that strobed a lane and was then tolerance-discarded, by truncation and by a
  bad AttributeLength, the next well-formed MRPDU's LeaveAll of that type strobes its lane again.

The suite README tally follows.

**Verification:**
- The new checks pass at the corrected head.
- Planting R1 and R8 with `scripts/03_mutate.py` turns them red.
- The four SRP suites stay otherwise unchanged.
- Coverage of Tests and Robustness is re-banked at that head.

### R270-F2 (retained at this head) - MINOR - Docs

**Where:** `docs/10_RESOURCE_AND_EFFORT.md:554-557`, against `docs/architecture/10_srp_engine.md:402-411`
and `hdl/srp/KL_srp_top.sv:71-74`.

**Title:** the doc set contradicts itself on restarting the timer after a received LeaveAll.

**Authority / evidence:**
- The resource document lists, among the consumer's defects "where this spec is right", that it has
  "no restart or Passive behaviour on a received LeaveAll (802.1Q Table 10-5)".
- At this head, §6.5 and the `KL_srp_top` banner say this processor does not restart the timer, and
  call that an open deviation from the same table.
- The manager's correction confirms the deviation (issue comment 5801278433, item 1; tracker #108).
- AGENTS.md §6 Docs ("changed contracts are reflected in authoritative docs") and §7
  ("authoritative documentation is current").
- I read both passages at this head.

**Impact:** two documents at one head give opposite answers on Table 10-5 conformance. The PR's own
§6.5 text is what now contradicts the older sentence, and the PR body leaves it on purpose ("Open,
for the owner", item 1).

**Required outcome:** the resource document no longer credits this spec with restart or Passive on a
received LeaveAll. The 10-15 s randomisation claim may stay, and pointing to §6.5 or #108 is
enough.

**Verification:** the edited sentence agrees with §6.5, and `make check` passes.

## 4. Suggestions (do not affect the verdict)

**S1 - SUGGESTION - Tests - routing negatives beyond the FSM planes, and an inherited gap.** The
four mutants below all survive at head (receipts/03).

- **R4:** the Domain participant takes every MSRP lane (`KL_srp_top.sv:347`). F5c does not check
  that our Domain stays quiet after a Listener-only LeaveAll. The impact is only an extra idempotent
  Domain declaration.
- **R5:** the VLAN participant also takes the MSRP lanes (`:405`). This line is unchanged by the PR,
  so the gap is inherited.
- **R10 and R11:** the own LeaveAll is dropped from the talker registrar's aging
  (`KL_srp_talker_fsm.sv:630`) and from the listener registrar's (`KL_srp_listener_fsm.sv:416`).
  The base analogues B10 and B11 also survive the base suites (receipts/04), so this gap is
  inherited too. The PR did rewrite both expressions, and §6.5 restates the §10.7.9 rule.

Worth adding: a Domain-quiet check in F5c; an MSRP LeaveAll leaving MVRP joins untouched; and
`la_own()` taking an IN registrar to LV with ARM in both FSMs.

**S2 - SUGGESTION - Docs.** Two parts of the original S2 have moved on; see section 7.

- `docs/architecture/10_srp_engine.md:402-411` says the timer deviation is "recorded there as open",
  that is, in issue #106, which this PR closes with `Closes #106`. This round's own pass suggested
  citing the open issue #29. The manager has since ruled that §6.5 must point to #108 instead
  (section 7).
- The resource-document contradiction at `docs/10_RESOURCE_AND_EFFORT.md:554-557` was this round's
  own observation at SUGGESTION. It is now tracked as the retained R270-F2 (MINOR).
- Still open as a suggestion: #29's "fix shape" names a single `dec_la_msrp_w` bit, which is now four
  lanes. #29 and #108 track the same deviation; one should be closed or linked to the other.

**S3 - WITHDRAWN.** I first reported that the author's `runB.sha256` does not verify
`tap-runB.pcap` or `tcpdump.log`. That is correct but not a defect: the packet's own
`review-evidence/pp106-r1/MANIFEST.json` discloses both files as path-redacted. It gives
`original_sha256` values equal to `runB.sha256` and `published_sha256` values equal to the published
bytes (receipts/10). I had not read the MANIFEST before drafting S3. The DECISION's `160debeb` /
`bf2e79ee` identify the unredacted original. My decode of the published, redacted capture reproduces
every MSRP claim and test P's 109 bytes.

**Considered, no finding (RTL).** The `WORST_BYTES_C` comment assumes "four message shells", which a
drain alternating between types can exceed. That assumption is inherited. The bound still dominates
the true worst case: at `DEPTH_P` 12 the real maximum with LeaveAll-only vectors is 528 B, against
a bound of 558 and a 576 B slot. Only the default depth of 12 is instantiated (`KL_srp_top.sv:99`).

## 5. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_encoder.sv:149-154,402-417,539-543,615-627,675-691,709-712`; `KL_srp_decoder.sv:41-54,101-103,205-210,330-335,401-425`; `KL_srp_top.sv:55-74,347,405,511,594`; `KL_srp_talker_fsm.sv:411-420,620-630`; `KL_srp_listener_fsm.sv:401-420`; `srp_pkg.sv:70-76`; against 802.1Q-2014 §10.6, §10.7.4.3, §10.7.5.20, §10.7.9 with Table 10-5, §10.8, §10.8.1.2, §10.8.2.6, §10.8.2.8, §10.8.2.10.1 and Milan §4.2.7.1.1-3; issue acceptance and both scope decisions; independent capture decode (receipts/02) | R271-1 | fc155c3ca28b04c2220bf41ebea9214379210452 |
| RTL | CLEAN | the same RTL ranges, for widths and indexing (`la_bit_w`, `la_lane_w`, per-sink `leaveall_any_w`), reset of the new registers, the `E_VFV`/`E_PATCH` loop (it terminates: at most 3 added messages), the slot bound, no CDC or backpressure change, and the direct event and lane path into the FSMs; focused lint of the 5 changed modules (receipts/07); manager lint 37 OK and Yosys 32+1 OK at head | R271-1 | fc155c3ca28b04c2220bf41ebea9214379210452 |
| Robustness | UNCLEAN (R271-F1) | decoder malformed and truncated paths with the new gate (`:253-259,334,403-409`); encoder mid-drain and start-cycle LeaveAll, and reset; probes A1-A3 and mutant R8 (receipts/03, /06) | R271-1 | fc155c3ca28b04c2220bf41ebea9214379210452 |
| Tests | UNCLEAN (R271-F1) | `tb/srp_decoder`, `tb/srp_encoder`, `tb/srp_stream_fsms`, `tb/srp_top` `sim_main.cpp` and the wrap; 4 suites at head and base; 3 headline arms reproduced (receipts/05); 11 reviewer mutants, 5 killed and 6 survivors analysed (receipts/03, /04); old tests against new RTL (receipts/08) | R271-1 | fc155c3ca28b04c2220bf41ebea9214379210452 |
| Docs | UNCLEAN (R270-F2 retained) | `docs/architecture/10_srp_engine.md:309-411` (F10.9 note, §6.5); `docs/10_RESOURCE_AND_EFFORT.md:554-557`; the encoder, decoder and top banners; `srp_pkg` header; the 4 `tb/*/README.md` tallies against measured counts; PR body and issue evidence against the capture and the evidence MANIFEST; the docs' old "§10.7.1" citation, which is in fact notational conventions. The ledger drafted before section 7 had this lens CLEAN, with the resource-document contradiction as a suggestion; it is UNCLEAN after weighing R270-F2 | R271-1 | fc155c3ca28b04c2220bf41ebea9214379210452 |

The same result in the AGENTS §6 line format:

```text
[R271] PASS Conformance - hdl/srp/KL_srp_{encoder,decoder,top,talker_fsm,listener_fsm}.sv + srp_pkg.sv at fc155c3c - per-type LeaveAll on transmit and receive against 802.1Q-2014 §10.7.5.20 NOTE/b), §10.8, §10.8.2.6, §10.8.2.8 f/g; the author's calls 1 and 2 confirmed; decoded Run B capture
[R271] PASS RTL - the same files - widths, indexing, reset, FSM termination, slot bound, lint of the changed modules, event/lane ordering into the FSMs
[R271] MINOR Robustness - hdl/srp/KL_srp_decoder.sv:334,403-409 - gate re-arm after a tolerance-discarded MRPDU untested (R271-F1)
[R271] MINOR Tests - tb/srp_decoder/sim_main.cpp:619-800 vs docs/architecture/10_srp_engine.md:390-393 - unflagged-first layout and gate re-arm unpinned; mutants R1/R8 survive (R271-F1)
[R271] MINOR Docs - docs/10_RESOURCE_AND_EFFORT.md:554-557 vs docs/architecture/10_srp_engine.md:402-411 - the doc set contradicts itself on restarting the timer after a received LeaveAll (R270-F2, retained)
```

## 6. Receipts (publishable; listed in MANIFEST.sha256)

| receipt | what it shows |
|---|---|
| `receipts/00_export_trees.txt`, `00_tool_identity.txt` | head, mid and base trees exported by `git archive`; simulator 5.050 identity, wrapper and binary SHA-256, job cap |
| `receipts/01_head_srp_suites.txt`, `04_base_srp_suites.txt`, `logs/head_*.log`, `logs/base_*.log` | the four SRP suites at head and at base |
| `receipts/02_decode_runb.txt` | independent decode of every MSRP MRPDU in the capture; LeaveAll layouts; test P byte equality |
| `receipts/03_mutants.txt`, `03_mutants_detail.txt` | reviewer mutants R1-R11 and their FAIL lines |
| `receipts/04_base_mutants.txt` | base analogues B10 and B11 (the inherited own-LeaveAll gap) |
| `receipts/05_plant_previous.txt` | headline arms reproduced: 146, 19 and 5 FAIL |
| `receipts/06_decoder_probe.txt`, `logs/probe_*.log` | F1 probe: head passes 159/159; R1 fails U1-U3; R8 fails A2 and A3 |
| `receipts/07_lint_changed.txt` | lint of the 5 changed modules |
| `receipts/08_old_tests_new_rtl.txt` | base testbenches against head RTL: E7, F2 ×4 and F4 ×1 only |
| `receipts/09_clone_integrity.txt` | clone at exact head: 224 files, 0 byte/mode mismatches, index = tree, no gitlinks |
| `receipts/10_evidence_sums.txt` | `runB.sha256` against the published capture, the capture's provenance, and the MANIFEST's path-redaction disclosure that resolves the mismatch |
| `scripts/*` | every command above, portable (paths as arguments; `PINNED_VERILATOR` for the wrapper) |

Nothing in the review clone was modified. All builds, probes and mutants ran in disposable copies
under `scratch/`, which is not published. The copyrighted standard texts are not published.

## 7. Prior public review findings on PR #107

**Order.** When this round started (review-start notice 5801122287, 19:04:58), PR #107 had no
review findings. I read the ones below only after sections 1-6, the verdict and the ledger were on
disk:

- a concurrent internal round, `[R270] NEGATIVE` (PR comment 5801267950, 19:14:54);
- the manager's rulings on it (issue #106 comment 5801278433, 19:15:38).

The PR head is unchanged at `fc155c3c`, so nothing below has been fixed. Each finding is either
retained, or retained and superseded by a manager ruling.

| prior finding | status at `fc155c3c` | this round's position |
|---|---|---|
| R270-F1 MINOR Tests: the once-per-MRPDU gate's two boundaries are unpinned (its X1 and X7) | **Retained** (open) | Found independently as R271-F1. My R1 is its X1 and my R8 its X7; both survive every SRP suite, and the head passes the boundary probes. The manager's ruling (item 2) requires the same tests with X1-class and X7-class failing arms. I record the finding under Robustness as well as Tests, because the unguarded behaviour is the gate's recovery from malformed input. |
| R270-F2 MINOR Docs: the resource document contradicts §6.5 on the timer restart | **Retained** (open), see section 3 | My own pass noted the same contradiction at SUGGESTION (S2). I now concur with MINOR: the PR's §6.5 text sets the statement, the contradicting sentence stays at the same head, and the fix is one sentence. Docs is UNCLEAN in this ledger as a result. |
| R270-S1 SUGGESTION Tests: the Domain row has no negative check (its X2) | Retained as a suggestion | Same as my S1 R4, which also survives here. |
| R270-S2 SUGGESTION Docs: the timer deviation needs a live tracker | Superseded by the manager ruling (item 1: tracker #108, and §6.5 must point to #108), not yet met at this head | §6.5 still points to #106. The ruling makes this a required edit for the correction round. #29 is an older open issue for the same deviation; close one or link them. |
| R270-S3 SUGGESTION Docs: justify `4'b1111` by §10.7.5.20 NOTE's "supported by the application" rather than by elaboration shape (`KL_srp_encoder.sv:149-152`, §6.5 `:343-344`) | Retained as a suggestion | Agreed. The banner (`:35-38`) already quotes the clause, but the localparam comment and §6.5 say "registers". |

**Manager rulings on the author's calls.** Call 1 (applicants routed per type) stands, and call 2
(the unflagged-first layout handled in wire order) is accepted. Both agree with section 2. The
donor-full bank will use this PR's own range for `git diff --check`.

**Correction to this round.** Section 4 now marks S3 withdrawn: the MANIFEST discloses the
redaction.

## 8. Real limits

- I did not run the full protocol-processor suite bank, Yosys, xvlog, the parent banks, the builder,
  act or Docker; these are outside what this round allows. My runs were the four SRP suites, the
  probes, the mutants and a focused lint. The manager's receipts cover the full banks (section 9).
- The #530 end-to-end harness was not rerun at `fc155c3c`, by the author or by me. The receive-side
  mechanism is covered by `srp_top` F5 through the real decoder, FSMs, timer service and PRNG. No
  hardware was used. Physical calibration was NOT RUN, and field skips are not hardware proof.
- Interoperability with a peer that applies received LeaveAll per application is not assessed
  beyond the clause reading and the bench switch's own layout.
- Standard text was read from the 2014 edition, the edition this repository targets.

## 9. Pending manager duties

- The scope decision's wording has been reconciled by the manager's correction (5801278433): call 2
  accepted, timer premise corrected, tracker #108. Still to do:
  - §6.5 must point to #108 (required edit, not yet at this head);
  - close #29 or link it to #108, since both track the same deviation.
- Close R271-F1 (R270-F1) and R270-F2, then re-review the corrected head. Coverage for Tests,
  Robustness and Docs is banked only there, together with any lens whose artifacts the correction
  touches. Two positive independent reviews are still required.
- At parent adoption, the parent's `docs/traceability/ieee8021q.md` row MRP-5 ("on rx/tx LeaveAll,
  all registrations enter leave-pending") still states per-application receive semantics. I
  confirmed the wording at `759da623` and `5e7eb309`.
- The final current-dev candidate at the merge turn: source base `fbc1f715`, live dev `26d855a9`.
  Hosted and act acceptance.
- Parent adoption of the exact reviewed head. Consumer gates at the final parent candidate: the
  receipts at `759da623` with the gitlink staged at `fc155c3c` all exit 0, with the builder's
  calibration gate NOT RUN. Then the #530 silicon rerun for acceptance.
- The manager's donor-full command list carries three stale template steps:
  - a fetch of `refs/pull/13/head`;
  - `make -C tb/nvm_port figures`;
  - `git diff --check f70ba36e..e0c43b03`.

  So its whitespace receipt does not cover this PR. I ran `git diff --check fbc1f715 fc155c3c`
  myself: clean. The manager has committed to using this PR's range from now on (ruling item 4).

R271-1 FINISHED
