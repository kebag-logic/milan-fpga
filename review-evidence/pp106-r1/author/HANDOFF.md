[A206] HANDOFF: protocol-processor issue #106, lane `106-leaveall-scope`

## State

- **Outcome: REVIEW READY, both halves.** Two commits on main `fbc1f715`, one-line subjects, no trailers:
  - `9370f8ab80231bbf1a6a833312e6b4ffbd0a4f9b` "Signal LeaveAll for every registered MSRP attribute type" (transmit).
  - `fc155c3ca28b04c2220bf41ebea9214379210452` "Route a received LeaveAll to its own attribute type, once per MRPDU" (receive).
- The worktree is clean. Nothing was pushed, no PR exists, nothing was merged.
- PR body: `PR-BODY.md` (starts `[A206]`, contains `Closes #106`, covers both halves). Receipts: `receipts.txt`.
- Public record on #106:
  - TAKEN: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5797290433
  - DECISION: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5797308575
  - REVIEW READY, transmit half: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5798150193 (text: `REVIEW-READY.md`)
  - Scope decision adding the receive half (manager): https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5798176959
  - REVIEW READY, both halves: the last `[A206]` comment on #106, posted after this file was written (text: `REVIEW-READY-RX.md`).

## Receive half: what changed (`fc155c3c`)

- **Decoder.** `la_msrp_o` is now four lanes, one per MSRP AttributeType (`srp_pkg` `SRP_LA_*_C`), plus `la_mvrp_o`. A lane fires once per MRPDU, at the first VectorHeader of its type with LeaveAllEvent set. `la_done_r` is cleared at each ProtocolVersion byte.
- **Routing** (`KL_srp_top`):
  - Talker Advertise/Failed lanes go to the talker applicants and the listener registrars. The applicant takes the lane of the variant it declares (`fail_r`); the registrar takes the lane of the type it holds (`rtype_r`).
  - The Listener lane goes to the listener applicants and the talker registrars.
  - The Domain lane goes to `KL_srp_domain` (re-declare). `la_mvrp_o` goes to VLAN, unchanged.
  - An own LeaveAll still ages every registrar (§10.7.9).
- **Unchanged:** the Table 10-3/10-4 transcriptions, Δ13, the leave-timer plane, the encoder, and the leavealltimer.
- **Docs.** docs 10 §6.5 is rewritten (receive routing table, order, timer). The F10.9 note, the `KL_srp_top` and `KL_srp_decoder` banners, and three tb READMEs are updated.

## Judgement calls a reviewer should check

1. **Applicants are routed per type too.** The scope decision says "registrars". §10.7.5.20 b)2) scopes rLA! for applicants and registrars alike, so both follow the lane of their own type.
2. **Order.** "Before that MRPDU's attribute events" holds for every layout a conformant sender produces: LeaveAll first (§10.6), with the provoked messages after it (§10.8 NOTE 2). It also holds for all 9 switch LeaveAll MRPDUs in Run B and for our own encoder. The exception is a type-T vector without LeaveAll ahead of the first flagged type-T vector in the same MRPDU. That layout is processed in DLSDU order (§10.8), because the streaming decoder has already emitted those events. Exact LeaveAll-first semantics there would need the whole MRPDU buffered.
3. **Timer.** The scope decision says the no-restart behaviour "stays as the standard's timer rules require; state the clause." The clauses read the other way: Table 10-5 rLA! → "Start leavealltimer"; §10.6 "Reception of a LeaveAll message from another Participant causes the timer to be restarted". Milan v1.2 Table 4.3 sets only the range. The behaviour is unchanged as directed, and it is documented as an open deviation. No clause is cited as justifying it, because none does.
4. **Two existing `srp_top` stimuli changed** (F2, F4). Their Domain-only and Talker-Advertise-only LeaveAll encoded the per-application reading; 5 checks failed under per-type routing. Both now flag every MSRP type; every check is kept. They pass under both routings, and the new F5 is what separates them.

## Tests and gates (details in `receipts.txt`)

- New checks: srp_decoder 113 → 150; srp_stream_fsms 1005 → 1068; srp_top 236 → 252. srp_encoder stays at 556, and every other suite is identical.
- The scenarios the scope decision asked for, each as a decoder test and a talker-FSM test:
  - (a) the Run B PDU shape: decoder P (the capture's 109 bytes), FSM I, and end to end srp_top F5a;
  - (b) Domain-only LeaveAll: decoder Q, FSM J, and srp_top F5b;
  - (c) Listener-only LeaveAll: decoder R, FSM K, and srp_top F5c.
- 15 failing arms (`mutate_rx.py`, `mutations_rx/SUMMARY.txt`), each shown failing and restored under a SHA-256 check.
- Repository gates at `fc155c3c`, with the CI's pinned simulator 5.050: make check, lint (37), run_suites (30/30, 15,436 checks), gen_matrix --check and yosys (32 + Xilinx) are all green. Logs are in `gates_rx/`.
- Parent consumer: a disposable clone at `574c29fa` with the gitlink staged at `fc155c3c`. check_cpp_idiom, check_py_idiom, xvlog_gate --check (PASS, 4 = ratchet, pinned @fc155c3c), pp_srcs --check --selftest and pp_shadow (371, 0 failures) are all green; check_sv_idiom and check_hygiene are OK too. Logs are in `parent_rx/`. The clone was deleted.
- The #530 end-to-end harness was **not** rerun at `fc155c3c`. The first-half runs at `9370f8ab` stand, and the receive mechanism is covered by srp_top F5a.

## Open, for the owner

1. Own leavealltimer restart on rLA! (Table 10-5): an open deviation, documented. `docs/10_RESOURCE_AND_EFFORT.md` (the consumer-comparison bullet) still implies this spec restarts it.
2. #530 item 2 (the fabric licence from `sr_admitted`) is unchanged.
3. Parent adoption: pin `fc155c3c` only after review, under the standing pin rule.

## Reproduce

- Suites: `./scripts/run_suites.sh` with the 5.050 simulator first on PATH.
- One arm: `python3 mutate_rx.py D1` (restores `hdl/srp` and checks each hash).
- Run B bytes: `evidence/decode_runB.txt` line 79 (47.029619 s); the raw record is in `evidence/runB/tap-runB.pcap`.
