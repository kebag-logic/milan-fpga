[R418] NEGATIVE - exact head f963fe9ac591b8a42547700468fc875db27ae5ab

# R418-1: internal independent review of PR #140 (lane C5a, issues #81 / #57 / #84)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #140, head
  `f963fe9ac591b8a42547700468fc875db27ae5ab`, tree `032d052c6fc98564760fd0fc1b33872227ff22a1`,
  base `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff` (five commits: 04c2f5c, 9a82661, fb0c13c, f1898da, f963fe9).
- Round R418-1, round 1 of this PR. Reviewer: internal independent reviewer (cleared context, own detached clone).
- Verdict: **NEGATIVE**. One MAJOR and three MINOR findings are open. Every lens is unclean.
- The lane's own evidence reproduces exactly at this head:
  - DL 29/29, HZ 83/83, TB 56/56, D3 133/133 and `tb/ucpu` 415/415;
  - the `aecp-mutants` campaign: 5 controls PASS and 30 arms KILLED, every per-arm count equal to the author's record;
  - the two moved D3 controls: 17 and 6 at head, 16 and 5 with the kill tied off.
- The findings are about what the PR claims and leaves ungraded:
  - "the four classes admit no conflict" is false for NAME_WR (probe);
  - the forced response gives status 10 to AECP message types whose status tables do not define it (probe);
  - a disclosed REQ-MVU-005 status defect is left untracked while the PR closes #57;
  - a test banner describes a mechanism the test does not use.

## 1. Reconstruction (inputs, in the prescribed order)

1. **AGENTS.md / CONTRIBUTING.md.** Neither exists in this repository at the head (`git ls-files` has no match). The
   contributor conventions used instead are `README.md` and `docs/README.md`: the ID registries and single-source
   rules, the citation rules, and `make check` before commit.
2. **The issues' frozen scope.**
   - Issues #81, #57 and #84: body and acceptance (snapshots in `receipts/public-inputs/`).
   - Assignment #81 comment 5915626788. Design first, with a STOP for any port, parameter or parent-visible change;
     items #81, #57 and #84 each carry mutants and an out-of-context resource cost; plus the parent-visible list.
   - TAKEN 5915631591; REVIEW READY 5921217255 at `f963fe9`.
   - The PR body is byte-identical to the published `author/PR-BODY.md`.
3. **Authorities used.**
   - 03 §6 F03.7 and rules (d)/(e); 08 §4 F08.3 and F08.1; 06 §8/§8.1 and F06.14; 09 F09.4.
   - `KL_pp_scoreboard.sv`: the F03.7 matrix as encoded.
   - IEEE 1722.1-2021 §9.3.2.6 (respond within 240 ms), Table 7-141 (ENTITY_MISBEHAVING = 10, an AEM status), and
     the clause 9 status tables for ADDRESS_ACCESS (codes 0 to 7) and AVC (codes 0 to 2).
   - Milan v1.2 §5.4.3.3 Table 5.19 and §5.4.3.4. The specification PDFs are not in the repository; clause readings
     are the reviewer's.
4. **Diff and history.** `git diff 0451d83d..f963fe9a`: 49 files, +2906/−82. Every RTL hunk was read in full: top,
   engine, µCPU and generator. So were every test section (DL, TB, HZ, P19), the campaign driver, the CI step and every
   docs hunk. `git diff --check` is clean.
5. **Public executable evidence.**
   - `kebag-logic/milan-fpga@c530a48e review-evidence/ppC5a-r1` holds MANIFEST.json, `author/HANDOFF.md`,
     `author/PR-BODY.md` and `author/parent-adaptation-132-c1.patch`. All three published sha256 values match the
     manifest (receipt 60).
   - The tree holds author material only. No manager bank receipts were found in it, and no manager evidence comment
     was on #81 or #140 when read.
6. **Prior public review findings on this PR.** None. At fetch time #140 carried only the two "INDEPENDENT REVIEW
   STARTED" notices, no review objects and no inline comments. There is nothing to resolve or retain.

## 2. Design judgement (HANDOFF §0 against 08 §4, F03.7 and the response-time clauses)

**Deadline read.** Sound. `aecp_deadline` (`hdl/top/protocol_processor_top.sv:3608-3624`) latches `pp_txn_t.deadline`
at `aecp_sb_accept_w`.
- The comparison is `!(now_ms - dl)[31]`, mod 2^32, the normalizer's arithmetic.
- One register is correct: the engine is single-issue, and admission requires the engine ready and the owner free.
- The boot-hold re-arm (`aecp_boot_held_r`) applies only to the head resident before `d3_done_w`. Rule (d) allows at
  most one resident AECP record at boot, so this matches rule (d).

**Kill face.**
- `kill_valid_i` is the live hold past its deadline, excluding `done_pending`. `kill_id_i` is `aecp_sb_id_r`.
  `kill_resp_queued_i` is `dl_queued_o` (A_TXW with `txreq_ready_i`, solicited only).
- `kill_ack_o` clears the owner, so the RX-slot return cannot re-release a reused id (`:3577`).
- The scoreboard handles a normal release and a kill in the same clock independently
  (`KL_pp_scoreboard.sv:203-226`).
- A dropped frame queues nothing and retires normally.
- Rule (e) "key released only after the forced response is queued" holds. DL1 checks it, and the
  `dl-released-before-queued` arm fails DL1.

**Preempt.**
- `KL_aecp_ucpu.sv:480-485, 716-731` redirect only at an instruction boundary, before any effect op, never as one
  retires, and once per dispatch. The cursor returns to 12 outside a batch.
- The effect set (WRITE_ST, NAME_WR, COMMIT, NVM_MARK, NOTIFY_ENQ, SEND_RESP) covers every op with state effect in
  the µISA except the registry and edit gathers. Those are excluded at the engine (`regun_r`, `lockc_r`,
  `amap_edit_r`, `KL_aecp_engine.sv:1699-1700`). I checked every `RG_OP` gather in `gen_ucode.py`: E_REGUN, E_DEREG
  and E_LOCKEN.
- `E_DLKILL` (`gen_ucode.py:376`) keeps an already-chosen refusal and otherwise sets 10, then falls into the unchanged
  `E_FAILSAFE`.

**Bound.**
- A preempted program answers within one watchdog-bounded op after expiry, and the 08 §4 bound is stated for it.
- A program past its first effect, and the three gather commands, are bounded only per op. That is honestly worded
  ("each op it has left is bounded the same way"). At `P-CLK-HZ` the per-op watchdogs are microseconds, so this is
  not a finding.

**MVU and Table 5.19.**
- The reading is correct. Table 5.19 defines SUCCESS and NOT_IMPLEMENTED only, and status 10 is AEM's (Table 7-141).
  NOT_IMPLEMENTED with the command echoed is the only legal failure answer. DL3 checks it, and the
  `dl-mvu-forced-status-10` arm fails DL3.
- The same reasoning was not carried to the other non-AEM message types (**F2**).
- A design suggestion on answering an implemented mandatory MVU command NOT_IMPLEMENTED is **S1**.

**Classifier.**
- `hz_classify` (`:1495-1556`) reads the header latch. That latch is the very register the normalizer's rx beat and
  seam are driven from (`:1381-1437`, `:1570-1585`), so the class and key are coherent with the beat.
- Keys `{type[5:0], index[9:0]}` only alias toward spurious conflicts. The ACMP talker/listener split matches the
  validator's term for term.
- Only an AEM_COMMAND for this entity takes its opcode's class.
- The barrier-priority fix (`:3492-3495`) is right and necessary: the `hz-barrier-no-priority` arm wedges the port,
  with 33 failures.
- I checked that an AECP head can no longer be held long behind ACMP. ACMP holds are short: the talker does not hold
  a command across MAAP allocation (`KL_acmp_talker.sv:130-150`), and the listener is a finite walk. So admission
  waits outside the kill's reach are bounded.

**Four-class limit.** Not truly unreachable; this is a missing test (**F1**).
- Scoreboard rule (2) (`KL_pp_scoreboard.sv:133-139`) makes RO_SNAPSHOT conflict with any other class on the same
  key.
- ACMP presents RO_SNAPSHOT on `{STREAM_INPUT,k}` and `{STREAM_OUTPUT,k}`. A SET_NAME on STREAM_INPUT k is NAME_WR on
  `{STREAM_INPUT,k}`.
- Probe P-B shows the conflict with a legitimate, served command. Only REGISTRY_OP (fixed registry key, not
  lock-protected) has no reachable conflict.

**STOP check.**
- No top-level port, parameter or register-map change: every top hunk is internal.
- The new ports are on `KL_aecp_engine` and `KL_aecp_ucpu`, which only the processor instantiates. Lint is
  zero-warning with them.
- No STOP was needed. Agreed.

## 3. Executed evidence (this reviewer, exact head, scratch exports only)

Tool: Verilator **5.050** (the CI pin, `hdl.yml VERILATOR_VERSION`).
- The prescribed path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does **not exist** on this
  host.
- I used the sibling manager wrapper `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, which reports
  `Verilator 5.050 2026-07-01 rev v5.050`. Hashes are in receipt 00. The host default (5.052) was not used.
- Every build ran from a `git archive` of the head under `scratch/`, with the C++ build capped at `-j 8`.

| Receipt | Command | Result |
|---|---|---|
| 10-15 | `make -C tb/ucpu run`; `tb/pp_top` `gsi-build`, `deadline`, `hazards`, `d3`, `budget` | rc 0: ucpu 415/415, DL 29/29, HZ 83/83, D3 133/133, TB 56/56. DL timings as in the PR: kill 9,943, forced first byte 13,354, DL3 13,396. The TB histogram equals 08 §4 (worst 24,681 clocks, 0.103 %) |
| 20 | `aecp_mutants.py` (`make aecp-mutants` equivalent, temp trees in scratch) | rc 0, 465 s: 5 controls PASS, **30/30 KILLED**, failure counts identical to the README table (for example `hz-stub-restored` 46, `hz-barrier-no-priority` 33, `ucpu-preempt-repeats` 18) |
| 40, d3/ | `d3_mutants.py --only hold_released_at_go dispatch_not_held`, at head and with `dl-kill-tied-off` applied | both KILLED; **17 / 6 at head, 16 / 5 tied off**; the extra failure is D3O6 in both |
| 31 | probe P-A (DeadlinePhase, observation only) | ADDRESS_ACCESS idle: status 1; queued past its deadline: **status 10, command echoed**, 13,398 clocks. AVC: the same (idle 1, killed **10**) |
| 32 | probe P-B (HazardPhase) | **SET_NAME STREAM_INPUT 1 is refused while an ACMP GET_RX_STATE of sink 1 holds**, admitted after the key frees, answers SUCCESS. SET_SAMPLING_RATE and SET_CONTROL addressed at STREAM_INPUT 1: refused while held, then answered NOT_SUPPORTED. REGISTER: admitted beside. (The STREAM_OUTPUT sub-probe's premise failed, because GET_TX_STATE was not held: inconclusive, not used.) HZ 97 checks, only those 2 premise/sub-probe failures |
| 50 | `scripts/lint_hdl.sh` | rc 0, 41 LINT OK |
| 51 | `git diff --check 0451d83d..f963fe9a` | rc 0 |
| 52 | `make links matrix modmatrix params` | rc 0: 1,002 links; 115 REQ / 17 GAP; 94 rows, 0 untested; parameters 26/26/26 |
| 60 | hosted snapshot (read-only) | at f963fe9a: `docs-gates` success, `portability` success, `suites` **in progress** (run 36789123922). Not an acceptance; the manager owns hosted acceptance |
| 90 | clone integrity after all probes | HEAD f963fe9a, tree 032d052c, detached, `status --ignored` empty, index equals the HEAD tree (mode/blob/path digest equal), 388/388 tracked blobs rehash equal. This repository carries no gitlinks |

**The D3 control drift is expected.**
- `hold_released_at_go` and `dispatch_not_held` break the boot hold. The held command is admitted during the slowed
  restore, re-armed at that admission, and outlives 100 ms inside the restore. The deadline then answers it with the
  forced response, so D3O6's byte-exact expectation fails.
- Rule (d) exempts a command held until the terminal, not one a broken hold lets run.
- Tying the kill off restores 16 and 5. The README record (`tb/pp_top/README.md`) is correct.

## 4. Findings

### F1 - MAJOR - Tests, Docs, Conformance

**What is wrong.** "The F03.7 matrix admits no conflict between CLOCK_CFG, NAME_WR, REGISTRY_OP or IDENTIFY and any
class ACMP presents" is false. #84 acceptance 2 is declared unmeetable for four classes on that basis.

**Where.**
- `docs/architecture/03_packet_engine.md:234-237`.
- `tb/pp_top/sim_main.cpp:11674-11677`: the HZ8 banner, "share no key or class with a stream step".
- `docs/architecture/09_verification.md:247`.
- The PR body's What remains, and HANDOFF §0.4, §3 and §6.

**Authority.**
- F03.7 RO_SNAPSHOT: "blocked only vs in-flight write on the same key".
- The scoreboard encodes it as rule (2), before every other rule (`hdl/packet_engine/KL_pp_scoreboard.sv:133-139`).
- The classifier keys NAME_WR, CLOCK_CFG and IDENTIFY by the command's own `{descriptor_type, descriptor_index}`
  (`protocol_processor_top.sv:1529-1544`).
- ACMP GET_RX_STATE / GET_TX_STATE / GET_TX_CONNECTION present RO_SNAPSHOT on `{STREAM_INPUT,k}` / `{STREAM_OUTPUT,k}`
  (`:1498-1509`).

**Evidence.** Probe P-B (receipt 32; `scripts/probe_patch.py`).
- A legitimate SET_NAME on STREAM_INPUT 1 (served by E_SNAME's generic locator) is **refused at admission while an
  ACMP GET_RX_STATE of sink 1 is held**, and admitted and answered SUCCESS once the key frees.
- CLOCK_CFG and IDENTIFY commands whose descriptor fields name a stream are also refused beside that read. They are
  then answered NOT_SUPPORTED.
- Only REGISTRY_OP has a key (the 0x3F registry key) no ACMP transaction can present, and it is not lock-protected.
  It is the only one of the four with no reachable conflict at this top.

**Impact.**
- A normative architecture statement is wrong.
- A newly reachable class conflict (NAME_WR against an ACMP read of the same stream) is ungraded. None of the 30 arms
  would notice it breaking: `hz-name-as-ro` is killed by HZ1 alone.
- The manager's closure accounting for #84 acceptance 2 rests on the false premise.

**Required outcome.**
- Grade at pp_top the NAME_WR admission conflict: SET_NAME on a stream descriptor against a held ACMP read of that
  stream, refused, then admitted after release. Add a failing arm, for example NAME_WR keyed NONE.
- Either grade the CLOCK_CFG/IDENTIFY conflicts the classifier admits for stream-addressed descriptors, or state
  precisely that they arise only from commands the engine refuses.
- Correct 03 §6, the HZ8 banner, 09 §8.3's claim wording and the PR's What remains, so that only REGISTRY_OP is
  recorded as having no reachable conflict.

**Verification.**
- The new HZ check passes at head and fails under its arm in `aecp_mutants.py`.
- The docs no longer state the four-class invariant.

### F2 - MINOR - Conformance, RTL, Robustness, Tests, Docs

**What is wrong.** A deadline-killed ADDRESS_ACCESS or AVC command, like any residual-bucket AECP type the engine
answers through E_NOTIMPL, is answered with **status 10 and the command echoed**. Status 10 is not a code of those
message types' status tables.

**Where.**
- `hdl/aecp/KL_aecp_engine.sv:3609-3616`: only `PP_PROTO_MVU` is remapped.
- `hdl/aecp/ucode/gen_ucode.py:376-380`: E_DLKILL sets 10 whenever status is SUCCESS. E_NOTIMPL's first op is
  SET_STATUS, so a preempt at the first boundary always lands before NOT_IMPLEMENTED is chosen.
- The docs that describe only the AEM and MVU answers: 03 §6 (`:311-314`), 06 §8.1 (`:1117`), `docs/guides/operator.md:55`
  and `docs/guides/integrator.md:321-324`.

**Authority.**
- IEEE 1722.1-2021 Table 7-141: ENTITY_MISBEHAVING is an AEM status.
- The clause 9 ADDRESS_ACCESS status table defines 0 to 7; the AVC table defines 0 to 2. NOT_IMPLEMENTED (1) is the
  status common to every AECP message type.
- This is the same reasoning the PR itself applies to MVU through Milan Table 5.19.

**Evidence.** Probe P-A (receipt 31).
- ADDRESS_ACCESS idle: 60 bytes, message_type 3, status 1.
- Queued behind the DL1-style stall: message_type 3, **status 10**, echoed, 13,398 clocks after reception. AVC is the
  same (message_type 5).

**Impact.**
- Under a slow-but-live face, the forced-response path this PR adds emits a response with an undefined status for
  every non-AEM, non-MVU AECP type. Before the lane these were answered NOT_IMPLEMENTED.
- No DL check or arm covers it.

**Required outcome.**
- Give every non-AEM message type the NOT_IMPLEMENTED echo form as its forced answer. Alternatively, never preempt a
  refusal-only dispatch (E_NOTIMPL / E_BADARG).
- Add a DL check (for example an ADDRESS_ACCESS queued past its deadline) with a failing arm.
- Align 03 §6, 06 §8.1 and both guides.

**Verification.** The DL check fails with the remap removed and passes at the new head.

### F3 - MINOR - Conformance, Docs

**What is wrong.** The PR closes #57 (REQ-MVU-005) while disclosing, "found here and not acted on", that an MVU
response whose memory fails is still answered status 10. Nothing tracks that.

**Where.**
- `hdl/aecp/KL_aecp_engine.sv:3650-3653` and `:3672-3675`: `rsp_fail_w` sets ENTITY_MISBEHAVING regardless of
  protocol.
- PR body, What remains; HANDOFF §6.
- `docs/00_MILAN_COMPLIANCE_REVIEW.md:400` (REQ-MVU-005 row, status {SUCCESS, NOT_IMPLEMENTED}) and `:497` (the GAP-03
  row now cites #57 as the timing evidence).

**Authority.** Milan v1.2 §5.4.3.3 Table 5.19. REQ-MVU-005's own text: MVU responses use only SUCCESS and
NOT_IMPLEMENTED.

**Impact.**
- Closing #57 removes the only open ticket on REQ-MVU-005 while a known status violation of that requirement remains.
- The compliance review row gives no pointer to it, so the defect is recorded only in a PR body.

**Required outcome.** Before merge, do one of the following:
- fix the fault path for MVU (the NOT_IMPLEMENTED echo, as the deadline path does) with a check; or
- have a tracking issue opened, and linked from the PR's What remains and the REQ-MVU-005 / GAP-03 rows.

**Verification.** A linked open issue, or a pp_top check with a failing arm.

### F4 - MINOR - Tests, Docs

**What is wrong.** Section HZ's banner describes a hold mechanism the section does not use.

**Where.** `tb/pp_top/sim_main.cpp:11215-11217` says "an ACMP transaction is held in flight by a PROBE_TX the talker
cannot answer yet: with no MAAP allocator the talker holds its DA request for P-MAAP-ACCEPT-CYC". The vestigial
`io.maap_on = false; // no allocator: PROBE_TX waits` is at `:11318`.

**Evidence.**
- The section holds ACMP by stalling the MAC and filling the standard TX slots (`fill_tx_pool`, `:11469`).
- `tb/pp_top/README.md` (HZ) and HANDOFF §3 both say the PROBE_TX approach was abandoned because the talker held its
  key for 16 clocks only.

**Impact.** A maintainer reading the test's own banner gets the wrong mechanism for every HZ premise.

**Required outcome.** Correct the banner to the TX-pool stall, and remove the vestigial `maap_on` line or justify it.

**Verification.** Read the banner against `fill_tx_pool` and `hold_acmp`.

### Suggestions (do not affect the verdict)

- **S1 (Conformance).** The Table 5.19 reading is correct. Still, answering a queued, implemented, mandatory
  GET_MILAN_INFO NOT_IMPLEMENTED (DL3) may lead a controller to treat the entity as non-Milan. MVU programs are short
  and watchdog-bounded (TB4: 16,174 clocks at 4,000 clocks per access). Consider exempting MVU from preemption, or
  recording the trade-off in 06 §8.1.
- **S2 (Docs, RTL comment).** `protocol_processor_top.sv:1453-1454` says CFG_BARRIER and LOCK_OP are global "so their
  key is not read". Scoreboard rule (2) does compare a LOCK_OP hold's key (0) with RO_SNAPSHOT keys, and
  `{ENTITY,0}` = 0x0000 equals it, so ENTITY-addressed GETs conflict with LOCK_OP by key. This is unreachable at this
  top (AECP is single-issue); say so.
- **S3 (Tests, Docs).** TB5 measures ACMP beside AECP loads that cannot conflict: a NONE-keyed READ_DESCRIPTOR and a
  fan-out. With the new classifier, an ACMP step can wait for a conflicting AECP hold (a barrier, LOCK_ENTITY, or a
  stream-keyed command near its deadline) up to `T-BUDGET-AECP-WC` plus the forced response. That exceeds the 50 ms
  design budget. State it in 08 §4, or measure it.
- **S4 (Docs).** The 08 §4 fan-out finding (`KL_aecp_notify` holds the command path for a whole class) contradicts the
  F08.3 row that stays in place (`08_timing.md:146` against `:180-185`). Give it a tracking issue.

## 5. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | IEEE §9.3.2.6 and Table 7-141; the clause 9 ADDRESS_ACCESS/AVC status tables; Milan Table 5.19 and §5.4.3.4; F03.7 and rules (d)/(e); F08.3; #81/#57/#84 acceptance against the assignment; probes P-A and P-B | R418-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |
| RTL | UNCLEAN (F2) | the `protocol_processor_top.sv` classifier, admission pick, owners and deadline block; the `KL_aecp_engine.sv` kill, A_GDEC/A_RUN voids and dl_queued; `KL_aecp_ucpu.sv` preempt; `gen_ucode.py` E_DLKILL; the scoreboard matrix and kill port; header-latch/seam coherence; lint 41/41 | R418-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |
| Robustness | UNCLEAN (F2) | same-clock kill/release; the kill ack against RX-slot return and id reuse; dropped frames; the barrier wedge and its fix; boot-hold re-arm and D3 drift; TX-pool starvation; admission wait behind ACMP (talker/listener hold bounds); mod-2^32 compare; the forced path under a slow face (P-A) | R418-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |
| Tests | UNCLEAN (F1, F2, F4) | sections DL, TB, HZ and `tb/ucpu` P19, re-run; `aecp_mutants.py` logic and its full campaign (35/35); both moved D3 controls, re-run both ways; the probes; the CI step | R418-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |
| Docs | UNCLEAN (F1, F2, F3, F4) | 00 GAP-03/REQ-MVU-005; 03 §6; 06 F06.14 and §8/§8.1; 08 §4; 09 F09.4 and §8.3; integrator and operator guides; `tb/pp_top` and `tb/ucpu` READMEs; the PR body and HANDOFF; `make links/matrix/modmatrix/params` | R418-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |

## 6. Real limits

- **Pinned simulator.** The prescribed `372-manager-candidate1` path is absent. I used the 372-manager-r2 wrapper,
  which reports Verilator 5.050, the CI pin. The author recorded campaign counts with 5.052. Mine are identical.
- **Scope of what I ran.**
  - I did not run the full processor bank (`run_suites.sh`), yosys/resource figures, `make lint` (diagrams), wavedrom,
    `make stale`, or any parent/consumer gate. That was by rule.
  - The resource figures (yosys, not the Vivado instrument of record) and the parent ratchet movements are the
    author's and were not reproduced.
- **Manager evidence.** The public evidence tree holds only author material. I did not find the manager's
  static/builder/native bank receipts in it and relied on the assignment's statement that they passed.
- **Hosted CI.** Observed at a snapshot only. `suites` was still in progress.
- **Specification clauses.** Read from the standards, not from repository text; the PDFs are not distributed. The
  ADDRESS_ACCESS and AVC status-table ranges in F2 are the reviewer's reading.
- **P-B STREAM_OUTPUT sub-probe.** Inconclusive, because GET_TX_STATE could not be held by the TX-pool stall. F1
  rests on the STREAM_INPUT case.
- **Hardware.** Physical calibration was NOT RUN. Nothing here is hardware proof.

## 7. Pending manager duties

- Run the donor bank and the parent consumer bank at dev `e4b771f9` (gitlink only, carrying the #132 + C1
  adaptation), post both, and build the final current-dev candidate at the merge turn. The source base is `0451d83d`.
- Hosted/act acceptance at the exact head. The `suites` job was in progress at the snapshot.
- Rule on F1 to F4 (and S1 to S4) with the author. In particular, #84's acceptance-2 accounting (F1) and a tracking
  issue for the REQ-MVU-005 fault path before closing #57 (F3).
- Publish this packet: `REPORT.md` plus the files listed in `MANIFEST.sha256`.

R418-1 FINISHED
