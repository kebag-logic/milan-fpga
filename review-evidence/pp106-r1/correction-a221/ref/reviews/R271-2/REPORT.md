[R271] NEGATIVE - exact head 27763677d83d4df7237389ffc0945ef9e224aa31

R271-2 is the external independent re-review of issue #106 / PR #107 after correction round 1 (A217).

- Head: `27763677d83d4df7237389ffc0945ef9e224aa31`, tree `7bfd82de512acd31a3378cf69a6bb30931395a56`.
- Source base: `fbc1f7156d711e5b7f511da8a16d9494256b017b`, the protocol-processor `main`, which has not moved. The head descends directly from it, so the head tree is the candidate merge tree in this repository.
- History: seven one-line commits with no trailers.
- Method: reconstructed with a cleared context from public state. The verdict, findings and ledger below were on disk before any prior review text was read.

**Verdict: NEGATIVE, on one open MINOR (F1: Tests, Robustness).**
- Both prior MINORs are resolved at this head: R270-F1 = R271-F1 (the gate tests) and R270-F2 (the timer doc).
- The RTL is unchanged by this round (comments only) and is correct.
- One weakness remains in the new receive gate's tests. Four plausible regressions of the once-per-MRPDU rule still pass all four SRP suites. Two of them reproduce the #530 burst-2 mechanism on a legal MRPDU, and one breaks the gate's re-arm after a padded MRPDU, the common framing for a short LeaveAll.
- Conformance, RTL and Docs are covered clean at this head.

## 1. Reconstruction, in order

1. **Governance.** This repository has no AGENTS.md or CONTRIBUTING.md, so the parent's apply (kebag-logic/milan-fpga @ live dev `26d855a9`): lenses, severities, ledger rule, one-line commits. Then this repository's `README.md` and `docs/README.md`.
2. **Issue #106.** The body (frozen acceptance) and every comment:
   - the evidence DECISION 5797308575;
   - the receive-half scope decision 5798176959;
   - the manager's CORRECTION 5801278433 (timer premise wrong, deviation tracked in #108; call #2 accepted; the gate tests still required);
   - the A217 assignment 5801860334 and REVIEW READY 5802202552.

   Also read: the PR #107 body and the manager's review-start notices.
3. **Authorities.** The IEEE 802.1Q-2014 clauses quoted in the issue, PR and docs 10 §6.5: §10.6, §10.7.5.20 NOTE and b)2), §10.7.9 Table 10-5, §10.8, §10.8.1.2, §10.8.2.6, §10.8.2.8 f/g. Also Milan v1.2 Table 4.3 and §4.2.7.1.2.
4. **Diff and history.** `git diff fbc1f715..27763677` (17 files), then the correction range `fc155c3c..27763677` (8 files) commit by commit, plus the full RTL files at head.
5. **Executable evidence.**
   - kebag-logic/milan-fpga @ `abd34a36`, `review-evidence/pp106-r1/manager-r2`: donor-full and parent-consumer.
   - The local parent-consumer receipts for the same run.
   - Hosted check runs at the exact head.
6. **Prior public findings** (R270-1 5801267950, R271-1 5801727037): read only after this report's verdict, findings and ledger were written (section 6). The concurrent R270-2 round had published nothing and was not read.

## 2. What the correction round changed, and what I checked

| Commit | Change | My check at head |
|---|---|---|
| `87121354` | srp_decoder T (flagged after unflagged, same message, across messages, MVRP) and U (re-arm after truncated, single-EndMark, bad-AttributeLength and out-of-alphabet MRPDUs): 150 → 177 checks | Read line by line: the byte layouts, the list lengths and every expected timeline are right. My own X1-class plant K1 fails T1-T3 (6 FAIL). My X7-class plants K3 and K10 fail U1-U4 (4) and U4 (1). At `fc155c3c` all three survive (receipts 02, 10). |
| `039ec326` | srp_top F5c Domain negative: 252 → 253 checks | My plant K12 (Domain also takes the Listener lane) fails exactly F5c and survives at `fc155c3c`. The added `sync()` keeps the LV/MT checks at 4.5 s and 5.4 s after the feed. |
| `90f4a0f1` | The effort doc no longer credits a restart. §6.5 and the top banner point to #108. | `docs/10_RESOURCE_AND_EFFORT.md:554-565` and `docs/architecture/10_srp_engine.md:404-415` agree. #108 is open, titled for this deviation. |
| `acd44d7f` | The §10.7.5.20 NOTE criterion ("supported by the application") replaces "registers" | Encoder `:35-38`, `:149-156`, `:404`, `:411` and `:682`; top banner `:62`; §6.5 `:343-347` |
| `27763677` | Suite READMEs record the arms | The counts (177, 253) match my runs (receipt 01). |

- **RTL is comments only.** Every changed `hdl/` line in `fc155c3c..27763677` is a comment, and the decoder and both FSMs are byte-identical (receipt 05).
- **Suites at head,** under the CI simulator pin 5.050 in `git archive` exports: srp_decoder 177/177, srp_encoder 556/556, srp_stream_fsms 1068/1068, srp_top 253/253 (receipt 01).

## 3. Findings

### F1 - MINOR - Tests, Robustness - the once-per-MRPDU LeaveAll gate is still pinned on only part of its boundary

**Where:**
- the gate: `hdl/srp/KL_srp_decoder.sv:334` (re-armed at each MRPDU's first byte) and `:405-409` (closed at the first flagged VectorHeader of a type);
- the tests: `tb/srp_decoder/sim_main.cpp:761` (S), `:811` (T), `:874` (U), plus the padding test at `:572` (N).

**Authority / evidence:**
- Docs 10 §6.5, `docs/architecture/10_srp_engine.md:377-379`: a lane fires "once per MRPDU ...; a later LeaveAllEvent of the same type in the same MRPDU is not applied again". The decoder banner `:52-54` gives the reason: it "would re-age registrations that MRPDU had just re-declared".
- Parent AGENTS.md §6: Tests ("each new test can fail for the defect it claims to detect"; boundary behaviour covered) and Robustness (min/max values, ordering, repeated events).
- Manager correction 5801278433 item 2: the tests must pin both boundaries of the gate.
- T and U do what the prior findings asked (section 6). But four other gate implementations, none of them equivalent, each pass **all four** SRP suites at this head, 0 FAIL of 177/556/1068/253 (receipt 02):

| Plant | Gate behaviour | Result at head |
|---|---|---|
| K6 | remembers only the last type that fired: one register instead of one bit per type | survives |
| K8 | re-armed at every message whose AttributeType differs from the previous message's | survives |
| K7 | an unflagged VectorHeader of a type re-opens that type's gate | survives |
| K5 | re-armed after a malformed or an unpadded clean MRPDU, but not after a well-formed MRPDU followed by padding | survives |

- I added three hand-computed checks to a disposable export's decoder suite (`scripts/gate_probe.py`, receipt 03). They pass on the unmodified head (185/185), and each one kills a survivor:
  - **G1**, `[L LA JoinIn] [Domain LA n=2] [L LA JoinMt]`, wants `L3 E3 L4 E4 E4 E3`. K6 and K8 give `L3 E3 L4 E4 E4 L3 E3`.
  - **G2**, one Listener message `[LA JoinIn] [JoinIn] [LA JoinMt]`, wants `L3 E3 E3 E3`. K7 gives `L3 E3 E3 L3 E3`.
  - **G3**, a Listener-only LeaveAll MRPDU of 19 octets padded to the 46-octet minimum payload and fed twice, wants `L3` both times. K5 gives no lane the second time.
- Why the suite misses them:
  - S repeats a type only in adjacent messages;
  - T puts the unflagged vector before the flagged one, never after it;
  - U re-arms only after malformed MRPDUs;
  - N, the only padded MRPDU, carries no LeaveAll.
- Padding is the real case. The V9 route forwards each MRP frame byte-exact up to its last octet (`hdl/packet_engine/KL_pp_rx_validator.sv` banner). That is why the decoder has `S_PAD`, and why a short LeaveAll MRPDU, such as a peer's Listener-only one, reaches it padded.

**Impact:** the suite would not detect two kinds of regression of the rule this PR introduces.
- **K6, K7 or K8** would re-apply a type's LeaveAll later in the same MRPDU. The Listener registration that the MRPDU's earlier vector had just re-declared would then age out T-MRP-LEAVE later. That is the #530 burst-2 mechanism this PR exists to remove, and the MRPDU that triggers it is legal (§10.8.1.2 allows any number of Messages of a type).
- **K5** would stop applying a peer's LeaveAll of a type after any padded MRPDU that carried it, until an unpadded or malformed MRPDU arrived. Registrations of that type would then no longer be aged by LeaveAll.

In both cases every gate stays green.

**Required outcome:** the decoder suite fails when:
- a type's gate re-opens later in the same MRPDU, both after a message of another type and after an unflagged vector of that type that follows the flagged one;
- the gate is not re-armed after a well-formed MRPDU followed by minimum-frame padding.

The existing T and U checks stay. No RTL change is needed, because the head passes G1-G3.

**Verification:**
- `scripts/mutants.py <clone> <new head> <scratch> <receipt> K0 K5 K6 K7 K8` reports K0 CONTROL PASSES and KILLED for K5, K6, K7 and K8.
- The four SRP suites pass at the new head.
- Tests and Robustness are re-banked at that head.

### S1 - SUGGESTION - Tests - the Domain row's negative covers the Listener lane only

`tb/srp_top/sim_main.cpp:958-968` (F5c) kills K12. It does not check the Domain row against the two talker lanes:
- **K13**, where the Domain participant also takes the Talker Advertise lane at `hdl/srp/KL_srp_top.sv:348`, passes all four suites (receipt 02);
- **K14**, the same for the Talker Failed lane, also passes all four.

The impact is low: at worst an extra Domain re-declaration. Adding a Talker Advertise-only and a Talker Failed-only LeaveAll to F5c's negative is optional.

### S2 - SUGGESTION - Docs - one pronoun in the timer sentence can be misread

`docs/10_RESOURCE_AND_EFFORT.md:561-562`: "that is not a point where this spec is right: its leavealltimer does not restart on a received LeaveAll either."
- Elsewhere in this paragraph "its" names the consumer, so a reader can take the sentence as another statement about the consumer. Only "either" and the §6.5/#108 link show that it means this spec.
- Optional fix: "this spec's leavealltimer".

### Retained suggestions from R271-1 (status at this head)

- **R271-1 S1 R5, R10, R11** (inherited routing gaps, which the author declined): still open.
  - My plants K15 (the VLAN participant also takes every MSRP lane), K16 (own LeaveAll dropped from the talker registrar's aging) and K17 (the same for the listener registrar) each pass all four suites (receipt 06).
  - They stay SUGGESTION, as graded in R271-1: the base suites miss the same gaps, and nothing in this round touches them.
- **R271-1 S2** (#29 and #108 both track the timer deviation; both are open): a manager decision, still open (section 8).

## 4. Clean-lens lines

```text
[R271] PASS Conformance - docs/architecture/10_srp_engine.md:329-415, hdl/srp/KL_srp_encoder.sv:35-38,146-156,401-419, hdl/srp/KL_srp_top.sv:54-76,264,348,406,512,595, docs/10_RESOURCE_AND_EFFORT.md:554-565 - checked against issue #106 acceptance, decisions 5797308575 and 5798176959, and the correction 5801278433:
  - every MSRP type and MVRP VID is flagged by the §10.7.5.20 NOTE criterion, with NumberOfValues-0 vectors (§10.8.2.8 f/g);
  - a received LeaveAll is routed per type, once per MRPDU, in DLSDU order (§10.7.5.20 b)2), §10.8.2.6, §10.8), with call #2 as accepted;
  - the timer is stated as a deviation from Table 10-5/§10.6 and points to #108, and no document credits a restart.
[R271] PASS RTL - hdl/srp/KL_srp_decoder.sv:205-210,330-426; KL_srp_top.sv:264,348,406,512-513,595-596; KL_srp_talker_fsm.sv:408-421,620-630; KL_srp_listener_fsm.sv:398-420,696; KL_srp_encoder.sv:122-131,315-326,401-419,534-556,616-716; srp_pkg.sv:70-76 - checked:
  - lane index = type - 1, guarded by len_ok_w;
  - la_done_r set and clear, and the shared bit 0 (MSRP Talker Advertise / MVRP VID) cleared at every MRPDU start;
  - per-type applicant and registrar selection (fail_r, rtype_r);
  - the encoder takes a LeaveAll at drain start with no abort path before commit, and its same-cycle latches;
  - WORST_BYTES_C: all-Talker-Failed with three LeaveAll-only messages is 528 B, under the 558 B guard and the 576 B slot;
  - comments only in this round (receipt 05); scoped lint 37 OK (receipt 04); head passes G1-G3.
[R271] PASS Docs - docs/architecture/10_srp_engine.md:307-415, docs/10_RESOURCE_AND_EFFORT.md:554-565, tb/srp_decoder/README.md:5-9,57-73,92-105, tb/srp_top/README.md:11-14,78-82,113-122, and the encoder, decoder and top banners - checked:
  - §6.5, the effort doc, the banners and the RTL agree;
  - the #108 pointer is in place;
  - the README tallies match my runs;
  - links 810 OK, matrix 115 REQ OK, module matrix 86/0 untested, stale OK, git diff --check fbc1f715..head clean (receipt 04);
  - the PR body and issue evidence are sufficient for a cold reviewer;
  - S2 is optional.
[R271] MINOR Tests - tb/srp_decoder/sim_main.cpp:761,811,874 - the once-per-MRPDU gate is pinned only in part; K5-K8 survive (F1)
[R271] MINOR Robustness - hdl/srp/KL_srp_decoder.sv:334,405-409 - gate idempotence across messages and re-arm after a padded MRPDU are unguarded by any test (F1)
```

## 5. Ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #106 acceptance and decisions 5797308575, 5798176959, 5801278433. §6.5 `:329-415`. Encoder `:35-38,146-156,401-419`. Top `:54-76,348,406,512,595`. Talker FSM `:408-421,630`. Listener FSM `:413-420`. Effort doc `:554-565`. | R271-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |
| RTL | CLEAN | Decoder gate and lanes `:205-210,330-426`. Top routing. FSM lane selection. Encoder LeaveAll path, latches and size guard. Comment-only proof (receipt 05). Lint 37 OK (receipt 04). Manager yosys OK (receipt 09). | R271-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |
| Robustness | UNCLEAN (F1) | Gate on malformed (U), padded (G3), interleaved-type (G1) and repeated-flag (G2, S) MRPDUs. Receipts 02, 03, 10. | R271-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |
| Tests | UNCLEAN (F1; S1 optional) | The four SRP suites at head (receipt 01). 13 plants at head, each with a passing control (receipts 02, 06), and 4 of them replayed at `fc155c3c` (receipt 10). G1-G3 (receipt 03). T, U and F5c read line by line. | R271-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |
| Docs | CLEAN (S2 optional) | §6.5, the effort doc §11, the decoder and top READMEs, the banners, doc gates (receipt 04), the PR body and issue evidence. | R271-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |

## 6. Prior public findings on PR #107, resolved or retained at this head

Read after sections 1-5 were on disk.

| Prior finding | Status at `27763677` | Evidence |
|---|---|---|
| R270-F1 = R271-F1, MINOR, Tests/Robustness: the unflagged-first layout (same message, across messages, MVRP) and the re-arm after a tolerance-discarded MRPDU (truncation, bad AttributeLength) are untested; X1/R1 and X7/R8 survive | **RESOLVED** as scoped | T1-T3 and U1-U4 cover every required case. My own plants of both classes are killed at head and survive at `fc155c3c` (receipts 02, 10). **F1 above is a new, separate finding**: other points of the same gate that the prior required outcome did not name. |
| R270-F2, MINOR, Docs (retained by R271-1): the effort doc credits a timer restart that §6.5 calls a deviation | **RESOLVED** | `docs/10_RESOURCE_AND_EFFORT.md:554-565` no longer credits a restart, and points to §6.5 and #108. Only the optional wording S2 remains. |
| R270-S1 = R271-1 S1 R4, SUGGESTION: no negative check on the Domain row | **RESOLVED** as scoped | F5c kills K12 (Domain also takes the Listener lane). Its talker-lane extension is my S1. |
| R270-S2, SUGGESTION: the timer deviation needs a live tracker | **RESOLVED** | §6.5 `:411-413` and the top banner `:74-75` point to open #108. |
| R270-S3, SUGGESTION: state the §10.7.5.20 NOTE criterion | **RESOLVED** | "supported by the application" appears in the encoder `:35-38,149-154`, the top banner `:62` and §6.5 `:343-347`. |
| R271-1 S1 R5, R10, R11, SUGGESTION: inherited routing gaps | **RETAINED** (SUGGESTION) | K15, K16 and K17 survive at head (receipt 06). |
| R271-1 S2, SUGGESTION: #29 and #108 track one deviation | **RETAINED**, the manager's call | Both issues are open (receipt 08, section 9). |
| R271-1 S3 | Withdrawn in R271-1 | n/a |
| R271-1 duty: the donor-full `git diff --check` must use this PR's range | **MET** | manager-r2 donor-full step 09 is `git diff --check fbc1f715 HEAD`, exit 0 (receipt 09). The `refs/pull/13/head` fetch and the `tb/nvm_port figures` steps mirror `.github/workflows/hdl.yml`, so they are not stale. |

## 7. Receipts and reproduction

All files are under this packet and listed in `MANIFEST.sha256`. Host paths are shown as `$PACKET`, `$CLONE`, `$VALIDATION_STORAGE`, `$LANES` and `$WORKSPACE_HOME`.

| receipt | content |
|---|---|
| `receipts/00-tools.txt` | simulator 5.050 identity: wrapper and binary SHA-256, compiler, git |
| `receipts/01-head-srp-suites.txt` | the four SRP suites at head in a `git archive` export |
| `receipts/02-mutants-head.txt` | K0 control plus K1, K3, K5-K8, K10 and K12-K14 at head, with planted-file SHA-256 and FAIL lines |
| `receipts/03-gate-probes-head.txt` | G1-G3 on the head (185/185) and against K5-K8 |
| `receipts/04-doc-lint-gates.txt` | links, matrix, scoped lint (37 OK), module matrix, stale, `git diff --check` |
| `receipts/05-hdl-comment-only.txt` | `fc155c3c..27763677` `hdl/` changes are comment lines only; SRP blob ids at head |
| `receipts/06-inherited-gaps-head.txt` | K15-K17, the status of the retained R271-1 suggestions |
| `receipts/07-clone-integrity.txt` | the clone after every probe |
| `receipts/08-hosted-and-refs.txt` | hosted runs and steps at the exact head; PP `main`, the PR head, parent dev and its gitlink |
| `receipts/09-manager-evidence-read.txt` | manager-r2 donor-full and parent-consumer exit codes and key lines, with SHA-256 of what was read |
| `receipts/10-mutants-at-fc155c3c.txt` | K0, K1, K3, K10 and K12 at `fc155c3c`: all survive there |
| `scripts/run_srp_suites.sh` | export a revision and run the SRP suites |
| `scripts/verilator_capped.sh` | pass-through wrapper that caps build parallelism (8 jobs in total) |
| `scripts/mutants.py` | plant one mutant exactly once per export and run the four suites |
| `scripts/gate_probe.py` | add G1-G3 to an export's decoder suite and run it, optionally with a mutant |
| `scripts/verify_clone.sh` | head, tree, index, per-blob bytes and modes, gitlinks, clean status |

Reproduce with `REAL_VERILATOR=<pinned wrapper> VL_JOBS=2 python3 scripts/mutants.py <clone> <rev> <scratch> <receipt> [ids]`, and `VL_JOBS=8 python3 scripts/gate_probe.py <clone> <rev> <scratch> <receipt> [ids]`.

**Clone integrity** (receipt 07, re-run last):
- HEAD, tree and index tree equal the reviewed head;
- all 224 tracked entries are byte- and mode-identical;
- the status is clean, with no untracked or ignored files.

This repository has no `.gitmodules`, so no submodule gitlink is required here. Every build, probe and mutant ran in disposable exports under `scratch/`, which is not published. Nothing in the clone or in any other checkout was written.

## 8. Real limits

- **No full banks.** By rule I ran no full protocol-processor suite bank, Yosys, nvm figures, parent or builder banks, act, Docker or hardware. For those this round relies on:
  - the manager-r2 donor-full receipts: lint 37 OK; 30 suites, 15,464 checks, 0 failing; `make check` OK; Yosys OK; nvm figures OK; diff-check clean;
  - the parent-consumer receipts: 7/7 exit 0; xvlog PASS pinned at `27763677`; pp_shadow 371/0; builder gate 11 (calibration) NOT RUN;
  - the hosted runs.
- **Hosted runs.** At the exact head, `hdl` push and pull_request each executed docs-gates, suites and portability, all successful. Only the "Build Verilator" step was skipped, on a cache hit. The hosted/act acceptance belongs to the manager.
- **Hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof. The #530 end-to-end harness was last run by the author at `9370f8ab` and was not rerun at `fc155c3c` or at this head. No post-change silicon run exists.
- **Standard text.** The specification texts are not in the repositories. Clause wording was judged from the text quoted by the issue, PR and docs.
- **Mutants are a sample.** They are single-point plants, not an exhaustive set. The author's arm receipts were not replayed beyond my own plants of the same classes.

## 9. Pending manager duties

1. **F1.** Route it to a correction round. A new head un-covers Tests and Robustness, and any lens whose artifacts it touches, until re-reviewed there. Two independent positive reviews are still required.
2. **Final current-dev candidate.** Build and gate it at the merge turn: source base `fbc1f715`, live parent dev `26d855a9`, whose gitlink is still `424c688f`, an ancestor of the base. The parent-consumer receipts at `27763677` are source-validation evidence, not the final candidate. Builder gate 11 is NOT RUN.
3. **#29 and #108.** Close one or link them; both track the leavealltimer deviation.
4. **Parent traceability.** At parent adoption, `docs/traceability/ieee8021q.md` row MRP-5 at dev `26d855a9` (receipt 08) still reads "on rx/tx LeaveAll, all registrations enter leave-pending". This head replaces those per-application receive semantics.
5. **Acceptance outside source.** The parent adopts the exact reviewed head, and a #530 silicon rerun shows a bound CRF talker streaming continuously across LeaveAll cycles.

R271-2 FINISHED
