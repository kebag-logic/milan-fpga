[R418] POSITIVE - exact head 44a6bb9082d31dbf933087ef007ad78a110e7053

# R418-2: internal independent review of PR #140, round 2 (lane C5a, issues #81 / #57 / #84)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #140.
  - Head `44a6bb9082d31dbf933087ef007ad78a110e7053`, tree `1b3a46226efb78feb6d41f4d84c4aa1e46cfc03d`.
  - Judged on base `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff`: 13 commits, eight of them new in round 2 (44db34b, 9f0299a, a2d2a24, 5107327, bf9b32d, 49041e6, 88e3459, 44a6bb9).
- Round R418-2. Reviewer: internal independent reviewer, in a cleared context with its own detached clone.
- Verdict: **POSITIVE**.
  - No BLOCKER, MAJOR or MINOR finding is open. All five lenses are CLEAN at this head.
  - Three SUGGESTIONs follow; they do not affect coverage.
- Every round-1 finding of both reviewers is resolved at this head (section 4).
  - My round-1 probes reproduce the corrected behaviour.
  - The one sub-probe that cannot set itself up is explained by a measured property. The substitute checks grade the same pair (section 4, F1).
- What reproduced at this head:
  - `tb/pp_top` 8,240/8,240 and `tb/ucpu` 415/415;
  - the lane campaign: 5 controls PASS and 55/55 arms KILLED, every per-arm failure count equal to the README record;
  - 10 reviewer-designed arms, all KILLED;
  - the other reviewer's round-1 mutant script: the two arms of its F2 are now KILLED.

## 1. Reconstruction (inputs, in the prescribed order)

1. **AGENTS.md / CONTRIBUTING.md.** Neither file is in this repository. I read them from the parent at milan-fpga dev
   `e4b771f9` instead: the five lenses, the severity rules, coverage banked per head, one-line commits with no
   trailers, and the HDL style.
   - The processor repository's own `README.md` and `docs/README.md` supply the single-source and ID rules and
     `make check`.
   - The parent's em-dash rule is not applied in this repository: its pages use U+2014 throughout, for example 36
     times in `tb/pp_top/README.md`. So I did not apply it.
2. **Frozen scope** (snapshots in `receipts/public-inputs/`):
   - the bodies and acceptance lists of issues #81, #57 and #84;
   - lane assignment #81 comment 5915626788;
   - round-2 assignment #81 comment 5923634905, with its rulings:
     - F1: grade every reachable class and key pair with a pp_top arm and a mutant, remove the false statement, and
       re-judge #84 acceptance 2;
     - REQ-MVU-005: fix the MVU fault path in this lane; #57 closes only with that fix;
     - items 3 to 6;
     - STOP before any port, parameter or parent-visible change.
   - TAKEN 5923637418 and REVIEW READY 5927089371 at this head.
3. **Authorities.**
   - 03 §6 F03.7 and rules (d) and (e); 06 §6.9, §8 and §8.1; 08 §4 F08.3; 09 §8.3; the 00 REQ-MVU-005 and GAP-03 rows.
   - `KL_pp_scoreboard.sv`, the matrix as encoded (rules 1 to 6).
   - IEEE 1722.1-2021: Table 7-141 (status 10 is AEM's), Table 9-2 (the codes common to every AECP message type),
     §7.4.17, §7.4.21.1, §7.4.25.1 and §7.4.45.1; §9.3.2.6.
   - Milan v1.2 §5.4.3.3 Table 5.19 and §5.4.3.4.
   - The specification PDFs are not distributed. The clause readings are mine.
4. **Diff and history.**
   - I read `git diff 0451d83d..44a6bb90` (63 files) with the round-2 slice `f963fe9a..44a6bb90` in full.
     - RTL: one logic change, in `KL_aecp_engine.sv`. The `KL_aecp_ucpu.sv` and top hunks are comments only.
     - Also read: the `tb/pp_top` DL8 to DL11 and HZ8 to HZ12 code, the wrapper taps, the campaign driver and all 34
       patches, every docs hunk, and `syn/ooc/README.md`.
   - Every commit message is one line with no body (receipt 51).
5. **Public executable evidence.** `kebag-logic/milan-fpga@4fe37ada review-evidence/ppC5a-r1`.
   - The five files this round read (author-r2 HANDOFF.md and PR-BODY.md, and three files of the other reviewer's
     round-1 packet) match their `published_sha256` values in MANIFEST.json (receipt 61).
   - The PR body is byte-identical to author-r2/PR-BODY.md.
   - The tree holds author and round-1 reviewer material only. It has **no manager bank receipt for this head**. The
     only manager bank comment on #140 is for `f963fe9a`.
6. **Prior public review findings.** These are R418-1 and R419-1, both NEGATIVE at `f963fe9a`. I read them only
   after my own pass over the round-2 diff (RTL, docs and tests). Each one is resolved or retained in section 4.
   Nothing from the concurrent round of the other reviewer was read.

## 2. Independent pass over the round-2 change

**RTL.** The change is in `hdl/aecp/KL_aecp_engine.sv`.
- `st_echo_w` (`:1705-1707`) is true for every AECP message type except AEM_COMMAND (validator bucket AEM and
  message_type 0).
  - This is the right test. The AEM bucket also carries AVC (4), HDCP APM (8), the reserved band and EXTENDED (14).
  - Odd (response) message types never reach a build, because `drop_w = msg_type[0] || ...` (`:1281`).
  - The unsolicited job forces AEM/0 (`:2802-2803`), so it keeps its old answer.
- The A_RUN remap (`:3644`) and both fault rebuilds use `st_echo_w`: A_ALLOC (`:3696`) and A_WR (`:3726`). Each
  answers NOT_IMPLEMENTED with the command echoed. The echo is read from the command's RX slot.
  - That slot is returned only at A_FREE (`:2567`), after the hand-off, so the echo never reads a slot the engine
    has given up.
  - `err_mode_r` blocks a second rebuild.
- `echo_len_w` (`:2548-2550`) cannot overflow its 11 bits.
  - The validator bounds `cdl + 12` by the slot capacity, and `pld_cap_w` caps the payload (`:1421-1422`).
- `txs_oversize_o` (`:2552-2554`) also requests the oversize slot when a non-AEM echo would need it. The request is
  then already right if the failure comes after the grant.
  - A legal command has cdl at most 524, so its echo is at most 550 bytes and fits `TX_STD_BYTES_P` = 576.
  - So only an over-long command takes the oversize slot.

**Interfaces.**
- `protocol_processor_top`'s port and parameter declarations are identical to the base.
- Round 2 changes no port line anywhere.
- The round-1 internal ports are on `KL_aecp_engine` and `KL_aecp_ucpu`, which only the processor instantiates.
- No RTL file is added or renamed. This repository has no gitlinks (receipt 54).
- No STOP was needed. I agree.

**The reachable-pair table** (PR body and HANDOFF §1), derived independently from `hz_classify`
(`protocol_processor_top.sv:1499-1556`) and the scoreboard matrix.
- ACMP presents RO_SNAPSHOT for GET_TX_STATE, GET_TX_CONNECTION and GET_RX_STATE, and STREAM_CFG for every other
  message. Both are keyed `{STREAM_OUTPUT|STREAM_INPUT, unique_id}`.
- Against those, the matrix gives exactly the author's table:
  - CFG_BARRIER: everything.
  - LOCK_OP: the steps. Its key 0 is no stream key.
  - STREAM_CFG and RO_SNAPSHOT: per key.
  - MAP_CFG: the class-wide cross-lock, plus a read only through a command naming a stream descriptor.
  - CLOCK_CFG and IDENTIFY: a read only through such a command.
  - NAME_WR: a read, with a legal SET_NAME.
  - REGISTRY_OP: nothing. Its key `{0x3F, 1}` has a type no ACMP key carries, and rule (6) puts it beside every step.
- HZ1 to HZ12 cover every listed pair. Where the pair is reachable, the listener's key is graded with either side
  held, and the talker's key with the AECP side held.

**Docs.**
- 03 §6, 06 §6.9 and §8.1, 08 §4, 09 §8.3, the 00 REQ-MVU-005 and GAP-03 rows, both guides, the two READMEs and
  `syn/ooc/README.md` describe the landed RTL.
- Every PR-body line citation I spot-checked matches the head: `:1705-1707`, `:1719-1720`, `:2548-2554`, `:3644`,
  `:3696`, `:3726`, top `:3581`, `:1453-1458`, ucpu `:480-484`, engine `:1709-1712`, and scoreboard `:133-157`.

## 3. Executed evidence (this reviewer, exact head, scratch exports only)

- **Simulator.** The prescribed `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does **not
  exist** on this host.
  - I used the sibling manager wrapper `372-manager-r2/pinned-tool-bin`, copied byte-identical. It reports 5.050, the
    CI pin, and its wrapper and binary hashes are in receipt 00.
  - The host default (5.052) was not used.
- **Builds.** Every build ran from a `git archive` of the head under `scratch/`, with the C++ build capped at `-j 8`.
  Every command ran in the foreground.

| Receipt | What | Result |
|---|---|---|
| 10-16 | `tb/ucpu run`; `tb/pp_top` all three builds, and sections DL, HZ, D3 and TB | rc 0: ucpu 415/415; pp_top **8,240/8,240** (default 8,164, fixture 20, timebase 56); DL 64, HZ 176, D3 133, TB 56, 0 failures. DL timings as in round 1 (kill 9,943 clocks; forced first byte 13,354). TB worst case 24,681 clocks, 0.103 % of T-AECP-RESP |
| 20-21 | `aecp_mutants.py`, run in four chunks | rc 0 each: 5 distinct controls PASS; **55/55 KILLED**, 0 unproven. All 55 per-arm failure counts equal `tb/pp_top/README.md`: 38 parsed, and the 17 shared-row arms checked by hand |
| 22-23 | `scripts/reviewer_mutants.py`: 10 reviewer-designed arms | **10/10 KILLED** (table below) |
| 24 | the other reviewer's round-1 `reviewer_mutants.py`, unchanged | `r-registry-lock-preempted` KILLED (pp_top, 4 DL10); `r-kill-ack-keeps-owner` KILLED (DL1, DL11); `r-mvu-no-echo` KILLED; the three arms classed equivalent in round 1 still survive (see S1 of that round, below) |
| 25 | µprogram effect-order scan of `gen_ucode.py` | only E_AMADD (and E_AMREMOVE, which branches into it) leads with COMMIT. It is exempt at the engine. Every other program writes (WRITE_ST or NAME_WR) before any COMMIT, NVM_MARK or NOTIFY_ENQ. So the defence-in-depth comment at `KL_aecp_ucpu.sv:480-484` is true |
| 30-32 | my round-1 probes P-A and P-B re-run verbatim, plus new P-C and P-D | see section 4, F1 and F2 |
| 33-34 | the other reviewer's round-1 reachability probe, with only its anchor moved to the HZ12 call | P0 and P1 status 0 (P1 after waiting); P3 and P4 status 11; P2 fails its own premise (`GET_TX_STATE` not held) |
| 40 | `d3_mutants.py --only hold_released_at_go dispatch_not_held`, at head and with `dl-kill-tied-off` | KILLED both ways; **17 / 6 at head, 16 / 5 tied off**; the difference is D3O6. Equal to the README record |
| 50-55 | `lint_hdl.sh`; `make check`; `gen_matrix.py --check`; `git diff --check` from 0451d83d and from f963fe9a; the interface diff; check-ID uniqueness | rc 0: 41 LINT OK; 41 mermaid + 18 wavedrom blocks; 1,003 links; 115 REQ / 17 GAP; 94 rows, 0 untested; parameters 26/26/26; whitespace clean; P19 (lines 1087-1152) and P20 (lines 1520-1608) disjoint |
| 56 | the area record's register explanation, checked structurally | `u_scoreboard` 169 = 8 holds x (4 + 16) + 8 + 1 exactly; the top's +33 = `aecp_dl_r` (32 bits) + `aecp_boot_held_r` |
| 60 | exact-head hosted run 36832325836, read-only | `docs-gates` success and `portability` success. In `suites`, the step "Lint (zero tolerance) + every suite" succeeded; the campaign steps (SRP, ADP, AECP), matrix and nvm figures were in progress or pending at 08:31 UTC. This is not an acceptance |
| 90 | clone integrity after all probes | HEAD 44a6bb90, tree 1b3a4622, detached; index tree equal; `status --ignored` empty; 401/401 tracked entries hash- and mode-exact; no skip or assume flags; no gitlinks (none in this repository) |

Reviewer arms. Each is a literal replacement in a scratch tree, matched exactly once. Each must fail a check whose
label starts with one of the arm's expected IDs.

| Arm | Breaks | Killed by |
|---|---|---|
| `r-fault-echo-alloc-removed` | the A_ALLOC fault rebuild loses the echo; A_WR keeps it | DL8 write error and DL8 tied-off memory (status 10) |
| `r-fault-echo-wr-removed` | the A_WR fault rebuild loses the echo; A_ALLOC keeps it | DL8 read error and DL8 540-byte command (status 10) |
| `r-fault-echo-len-60` | both rebuilds keep the 60-byte length | DL8 540-byte command (status 1, 60 bytes) |
| `r-st-echo-bucket-only` | the guard reads the validator bucket and not the message type | DL9 AVC, HDCP_APM and EXTENDED (status 10) |
| `r-registry-and-lock-preempted` | both registry-face exemptions removed together | DL10 x4 |
| `r-kill-not-gated-by-owner` | the kill stays raised after the hold has ended | DL1 x2, DL2 |
| `r-hz-key-index-dropped` | every key loses its index | HZ1, HZ9b, HZ9e, HZ10d, HZ12 (22 failures) |
| `r-acmp-key-uid-dropped` | ACMP keys lose the unique_id | HZ1, HZ2, HZ5, HZ6 and later (43 failures) |
| `r-name-keyed-as-output` | SET_NAME is always keyed STREAM_OUTPUT | HZ1, HZ9a x2, HZ9f x2 |
| `r-wrap-refused-tap-zero` | the new wrapper refusal taps blinded | 17 "waits" checks in HZ4 to HZ12. This shows that every "waits" check now depends on an observed refusal |

The fault-path arms also show which DL8 case reaches which rebuild. A read error is rebuilt at A_WR. A write error
and a tied-off master are rebuilt at A_ALLOC. So both new branches are graded independently.

## 4. Round-1 findings: resolved or retained at this head

### R418-1 F1 / R419-1 F1 (MAJOR): every reachable class and key pair graded; the four-class statement removed. RESOLVED

**My probes, re-run at head.** P-B is unchanged from round 1 (receipt 32).
- SET_NAME on STREAM_INPUT 1 is refused while a GET_RX_STATE of sink 1 holds. It is admitted after release and
  answers SUCCESS.
- SET_SAMPLING_RATE and SET_CONTROL naming STREAM_INPUT 1 are refused the same way, then answered NOT_SUPPORTED (11).
- REGISTER is admitted beside the read.
- These four sub-probes behave as the corrected 03 §6 says.
- The fifth sub-probe (SET_NAME on STREAM_OUTPUT 1 against a held GET_TX_STATE) fails its own premise again, as the
  author reports. So does the other reviewer's P2 (receipt 33).

**Judging the substitution.** Two new probes measure why the talker side cannot be held.
- **P-C** (receipt 32). Each talker command keeps its scoreboard key for **3 clocks** (GET_TX_STATE) or **16 clocks**
  (DISCONNECT_TX, GET_TX_CONNECTION, PROBE_TX), idle and with the TX pool filled alike. This is because the talker
  returns its RX slot once it has parked its answer.
  - The listener controls hold 90 to 103 clocks idle, and indefinitely while the TX pool is full.
- **P-D.** A SET_NAME on STREAM_OUTPUT 1 fed directly behind a GET_TX_STATE of source 1 on the serial ingress, at gaps
  of 0, 16 and 64 clocks, is first presented about 100 clocks after the talker's hold has ended. It is never refused.
- So the talker-held direction cannot be staged at this top's single ingress.
- The matrix function is symmetric, and the classification and key under test are the same either way. Grading the
  talker-side pairs with the AECP side held is therefore the right substitute:
  - HZ9d (refused, then SUCCESS) and HZ9e (another source admitted beside);
  - HZ10b to HZ10f, HZ11 and the third row of HZ12;
  - with the arms `hz-name-key-none-talker`, `hz-talker-keyed-as-listener` and the other `-talker` arms.
- The one window I did not stage is an AECP head already queued behind a busy engine that becomes ready inside a
  talker's 3 to 16 clock hold. Section 6 records it as a limit. It exercises the same symmetric pair.

**The statement and the #84 line.**
- 03 §6 (`:236-251`) now states the true reachability: NAME_WR with a legal command; CLOCK_CFG, IDENTIFY and MAP_CFG
  only through a stream descriptor (still waited on, then refused); REGISTRY_OP the one class with no reachable
  conflict.
- The HZ8 banner and 09 §8.3 agree.
- The PR's #84 line is exact:
  - "Relates to #84";
  - REGISTRY_OP has no reachable admission conflict, so it is graded by HZ1 and HZ8 only;
  - every other class is graded against ACMP;
  - acceptance 4 (02 §2 rule 5) is not done.
- This matches the ruling: close only if every class is graded.

### R418-1 F2 (MINOR): forced answer for the residual-bucket types. RESOLVED

- P-A re-run verbatim (receipt 31): an ADDRESS_ACCESS and an AVC queued past their deadline now answer **status 1,
  command echoed**, 13,398 clocks after reception. In round 1 they answered status 10.
- DL9 grades four types (ADDRESS_ACCESS, AVC, HDCP_APM, EXTENDED), byte-exact, idle and preempted.
- `dl-non-aem-forced-status-10` (4) and my `r-st-echo-bucket-only` (3) fail it.
- 03 §6, 06 §8.1, both guides and 09 §8.3 are aligned.

### R418-1 F3 / R419-1 F3 (MINOR): the MVU fault path. RESOLVED by the ruled fix, so #57 closes

- An MVU response whose memory fails answers MVU NOT_IMPLEMENTED with the command echoed (Milan Table 5.19). This
  covers a read error, a write error, a tied-off master, and a 540-byte payload whose 578-byte echo takes the oversize
  slot.
- Each void is counted. An AEM command under the same fault still answers ENTITY_MISBEHAVING.
- The checks are DL8. The arms are `mvu-fault-status-10` (4), `mvu-echo-slot-std` (1: clipped to 576) and my three
  fault-path arms.
- The REQ-MVU-005 and GAP-03 rows, 06 §6.9 and both guides record it.
- R419-1 F3's alternative (tracking issues for both findings) applied only if the path was not fixed. The 08 §4
  notification-hold finding is recorded in the tree, and the F08.3 row now says "not met as written". Its tracking
  issue is a manager duty (S3).

### R418-1 F2 assignment item / R419-1 F2 (MINOR): the two surviving kill-seam mutants. RESOLVED

- **DL10.** A REGISTER_UNSOLICITED_NOTIFICATION and a LOCK_ENTITY, each queued past its deadline, answer their own
  SUCCESS byte-exact with no redirect. Their effects are visible: the lock is held, and another controller's SET_NAME
  is pushed to the registered controller.
  - `dl-registry-preempted` and `dl-lock-preempted` each fail 2. The other reviewer's `r-registry-lock-preempted` and
    my combined arm fail 4.
  - Under the arms, the preempt lands before the registry op (status 10 and no effect). So DL10 kills them by the
    documented "never preempted" contract, which is exactly the check the round-1 finding asked for.
- **DL1 and DL11.** The RX-slot return after an honoured kill releases no hold id, and across the section every
  normal release names a live hold.
  - `dl-kill-ack-keeps-owner` and the other reviewer's `r-kill-ack-keeps-owner` fail DL1 and DL11 (19 stray
    releases).
- The three arms classed as equivalent in round 1 still survive. Receipt 25 confirms the effect-order argument behind
  `r-effects-short`. The two `!uns_r` guards are dead at this top, because only a solicited command holds a key.
  Both are now commented as defence in depth.

### R418-1 F4 / R419-1 F4 (MINOR): check IDs and the HZ banner. RESOLVED

- The `tb/ucpu` deadline checks are P20a to P20h, disjoint from P19 (GET_AUDIO_MAP). `"P20a completes: one redirect"`
  occurs at exactly one site (receipt 55). The campaign, the README, 09 §8.3 and 06 §8.1 follow.
- The HZ banner describes the TX-pool stall in both directions.
- `io.maap_on = true` (`sim_main.cpp:11559`) is justified at the line. Without an allocator the talker sits in its
  MAAP wait, which the round-1 talker-side probes hit.
- No doubled `"HZ HZ` prefix remains.

### Suggestions of round 1 (taken or retained with reasons; none affects coverage)

- **R418-1 S1** (the MVU preempt trade-off): taken, recorded in 06 §8.1.
- **R418-1 S2** (LOCK_OP's key 0 equals `{ENTITY,0}`): taken, comment at `protocol_processor_top.sv:1453-1458`.
- **R418-1 S3** (ACMP waiting behind a conflicting AECP hold): taken as a statement in 08 §4, not measured. See S1
  below for a precision point.
- **R418-1 S4** (the fan-out row): partly taken. The row now says "not met as written". The tracking issue is
  retained for the manager, because this round could post only TAKEN, REVIEW READY or STOP. I accept the reason.
- **R419-1 S1:** taken (the comments).
- **R419-1 S2:** taken ("all thirteen getters", in 08 §4 and the TB2 and TB3 check names).
- **R419-1 S3** (vendor out-of-context area): taken, at 44a6bb9 (+311 Slice LUTs, +174 registers, BRAM and DSP
  unchanged). **The register explanation holds** (receipt 56):
  - `u_scoreboard`'s 169 registers are exactly its hold table with all 20 class and key bits live
    (`MAX_HOLDS_P` 8 x 20, plus 8 valid and 1 pending). The base's 73 reflects the stub's mostly constant class and
    key.
  - The top's +33 is the deadline register and the boot-hold bit.
  - The named deltas sum to 173 of the 174.
  - I did not re-run the vendor tool. The "+16 LUT as distributed RAM" line and `u_aecp`'s unchanged 4,528 registers
    beside `u_ucpu`'s +3 are reported without attribution. That is synthesis-level detail, and no claim rests on it.

## 5. Findings of this round

No BLOCKER, MAJOR or MINOR finding.

**[R418] SUGGESTION Docs - `docs/architecture/08_timing.md:187-196` - S1: the ACMP-wait paragraph names one bound for
every conflicting AECP hold**
- **Evidence.** The paragraph lists the barrier, LOCK_ENTITY and same-stream-key commands as the holds an ACMP
  transaction can wait for. It bounds each hold by "`T-BUDGET-AECP-WC` from the AECP command's reception plus its
  forced response".
  - LOCK_ENTITY and ADD/REMOVE_AUDIO_MAPPINGS are never preempted (`KL_aecp_engine.sv:1719-1720`). Their hold ends at
    their own END, bounded by each op's watchdog. Those programs are short, so the figure still holds numerically.
  - The MAP_CFG class-wide cross-lock against every ACMP step is not in the list.
- **Impact.** The text is accurate as an upper bound but names the wrong mechanism for two classes.
- **Suggested change.** Name the never-preempted commands' own bound and add the MAP_CFG cross-lock to the list.
- **Verification.** Read the paragraph against `ucpu_preempt_w` and F03.7 rule (5).

**[R418] SUGGESTION Tests, Docs - `tb/pp_top/sim_main.cpp` DL8 label and `docs/architecture/09_verification.md` DL8
row - S2: "a 540-byte command"**
- **Evidence.** The command is a GET_MILAN_INFO padded to 540 **payload** bytes, a 578-byte frame whose echo needs
  the oversize slot. The code comment says exactly that.
- **Suggested change.** "a command padded to 540 payload bytes" would remove the ambiguity.

**[R418] SUGGESTION Docs - 08 §4 `KL_aecp_notify` finding - S3: tracking issue**
- **Evidence.** The finding is correctly recorded in the tree, and F08.3 now says "not met as written". But it still
  has no public issue (AGENTS §4: newly discovered work becomes an issue).
- **Suggested change.** The manager opens one and links it from the PR's What remains.

### Clean lenses, in the findings format

- `[R418] PASS Conformance` - checked against #81 acceptance 1 to 4, #57 acceptance 1 to 3 plus the ruled fault-path
  fix, #84 acceptance 1 to 4, Milan Table 5.19, IEEE Tables 7-141 and 9-2, and F03.7 rules (2) to (6). Artifacts:
  - `hdl/aecp/KL_aecp_engine.sv:1696-1720, 2544-2554, 3630-3735` and `protocol_processor_top.sv:1439-1556`;
  - DL3, DL8, DL9 and HZ1 to HZ12, and probes P-A, P-B, P-C and P-D;
  - the PR's closure lines: Closes #57; Relates to #81 (acceptance 4 not done); Relates to #84 (REGISTRY_OP graded
    only by HZ1 and HZ8, acceptance 4 not done).
- `[R418] PASS RTL` - checked against the engine's FSM contract and the scoreboard's port contract. Artifacts:
  - `KL_aecp_engine.sv` `st_echo_w`, `echo_len_w` and its width, `txs_oversize_o`, the A_RUN/A_ALLOC/A_WR rebuilds,
    `rsp_fail_w` with `err_mode_r`, and RX-slot ownership to A_FREE (`:2567`);
  - the top's admission pick and refusal semantics (`:3483-3517`);
  - no port, parameter or file change (receipt 54); lint 41/41.
- `[R418] PASS Robustness` - artifacts:
  - read, write and tied-off memory faults, and an over-long command (DL8);
  - residual-bucket types under the deadline (DL9);
  - exempt commands past the deadline (DL10), and stray releases after a kill (DL1, DL11);
  - a stale-kill arm, the talker hold length and the ingress race (P-C, P-D);
  - the D3 boot-hold controls at 17/6 and 16/5.
- `[R418] PASS Tests` - artifacts:
  - `aecp_mutants.py` at 55/55 with every count equal to the README, plus 10 reviewer arms and the other reviewer's
    round-1 script;
  - the refusal-tap arm, which proves the "waits" checks need observed refusals;
  - P19/P20 uniqueness; `tb/pp_top` 8,240 and `tb/ucpu` 415. Suggestion S2 only.
- `[R418] PASS Docs` - artifacts: 03 §6 (`:236-251, :318-335`), 06 §6.9 and §8.1, 08 §4, 09 §8.3, the 00
  REQ-MVU-005 and GAP-03 rows, both guides, `tb/pp_top/README.md`, `tb/ucpu/README.md`, `syn/ooc/README.md`, the PR
  body and author-r2 HANDOFF, and `make check`. Suggestions S1 to S3 only.

## 6. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #81/#57/#84 acceptance against the round-2 rulings; Milan Table 5.19 and §5.4.3.4; IEEE Tables 7-141 and 9-2, §7.4.17/.21.1/.25.1/.45.1; F03.7 and the reachable-pair table; DL3, DL8, DL9, HZ1-HZ12; probes P-A to P-D and the other reviewer's P0-P4; the PR's Closes/Relates lines and remainders | R418-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |
| RTL | CLEAN | `KL_aecp_engine.sv` (`st_echo_w`, `echo_len_w`, `txs_oversize_o`, A_RUN/A_ALLOC/A_WR, `rsp_fail_w`, RX-slot lifetime); `KL_aecp_ucpu.sv` and top comment hunks; `hz_classify` and the admission pick; `KL_pp_scoreboard.sv` matrix; interface diff; lint | R418-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |
| Robustness | CLEAN | DL8 fault matrix and over-long echo; DL9; DL10 exemptions; DL1/DL11 owner clear; `r-kill-not-gated-by-owner`; talker hold length and ingress race (P-C, P-D); D3 boot-hold controls | R418-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |
| Tests | CLEAN (S2) | `tb/pp_top/sim_main.cpp` DL8-DL11, HZ8-HZ12, wrapper taps; `aecp_mutants.py` and its 34 patches (55/55, counts equal); 10 reviewer arms; the other reviewer's round-1 scripts; `tb/ucpu` P20; suites 8,240 + 415 | R418-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |
| Docs | CLEAN (S1, S3) | 00, 03 §6, 06 §6.9/§8.1, 08 §4, 09 §8.3, integrator and operator guides, `tb/pp_top` and `tb/ucpu` READMEs, `syn/ooc/README.md` (register explanation checked), PR body, author-r2 HANDOFF; `make check`, `gen_matrix --check` | R418-2 | 44a6bb9082d31dbf933087ef007ad78a110e7053 |

## 7. Real limits

- **Simulator path.** The prescribed path is absent, so I used the sibling wrapper. It reports 5.050, the CI pin
  (receipt 00).
- **Not run, by rule or scope:**
  - `run_suites.sh` over all 33 suites. The exact-head hosted step "Lint (zero tolerance) + every suite" succeeded,
    and the author reports 33 suites rc 0. My own suite runs are `tb/pp_top` and `tb/ucpu`.
  - The other processor campaigns: SRP, ADP, gsi, name_wr, retry, srp_admission, desc_mem_guard, the nvm_port figures
    and the full D3 campaign. Of D3 I ran only the two moved controls. Round 2's only RTL logic change is the
    AECP engine's answer path.
  - The open-source synthesis flow, the vendor area run, and any parent or builder gate.
- **Manager bank evidence.** The named evidence tree carries no manager bank receipt for this head. I relied on the
  assignment's statement that the source static/builder and native banks passed.
- **Talker-held window.** The window where a queued AECP head becomes ready inside a talker's 3 to 16 clock hold was
  not staged. The same symmetric pair is graded from the AECP side.
- **Hosted CI.** Seen at a snapshot only. The campaign steps of `suites` were in progress or pending.
- **Branch base.** The branch is judged on `0451d83d`. Processor main has moved to `3f3ea56b`, and the branch
  conflicts with it. This review says nothing about the merge result.
- **Specifications and hardware.** Clause readings are the reviewer's. Physical calibration NOT RUN; field skips are
  not hardware proof.

## 8. Pending manager duties

- Hosted and act acceptance at the exact head, including the `suites` campaign steps that were pending at the
  snapshot.
- The donor bank and the parent consumer set at milan-fpga dev `e4b771f9` for this head, posted publicly. No receipt
  for this head is in the evidence tree yet.
- The merge-main round against processor main `3f3ea56b` (C2 + C4) and a re-review of the merge head. Then the final
  current-dev candidate at the merge turn (source base `0451d83d`, live dev `e4b771f9`), which is distinct from this
  source validation.
- Open the tracking issue for the 08 §4 `KL_aecp_notify` fan-out finding (S3; R418-1 S4 retained).
- Merge still needs a second independent positive review at this head.
- Publish `REPORT.md` plus the files listed in `MANIFEST.sha256`.

R418-2 FINISHED
