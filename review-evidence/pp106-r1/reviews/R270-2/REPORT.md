[R270] POSITIVE - exact head 27763677d83d4df7237389ffc0945ef9e224aa31

Round R270-2: internal, cleared-context, independent re-review of protocol-processor issue #106 / PR #107. The head is `27763677d83d4df7237389ffc0945ef9e224aa31`, tree `7bfd82de512acd31a3378cf69a6bb30931395a56`, source base `fbc1f7156d711e5b7f511da8a16d9494256b017b`, which is the live PP `main`. The round covers correction round 1: five commits on the reviewed head `fc155c3c`, which answer R270-1 F1/F2 and R271-1 F1 (with R270-F2 retained).

**Verdict: POSITIVE.** At this head, no BLOCKER, MAJOR or MINOR is open under any lens:
- Both boundaries of the once-per-MRPDU LeaveAll gate are now pinned by decoder tests, and each test fails under X1-, R1-, X7- and R8-class arms. I checked this with my own arms and with both prior reviewers' scripts, run unmodified. The same arms survive at `fc155c3c`.
- The resource document no longer credits a timer restart on a received LeaveAll, and 10 §6.5 points to #108.
- The Domain negative (R270-S1) and the §10.7.5.20 NOTE criterion (R270-S3) are in.
- The RTL change in this round is comments only, which I checked mechanically.

The four suggestions in section 4 do not affect the verdict. Three of them are gaps that predate this PR.

## 1. Reconstruction order and inputs

1. Parent governance at dev `26d855a9` (`AGENTS.md`, `CONTRIBUTING.md`: lenses, severities, completion ledger, commit rules). The PP repo has no AGENTS or CONTRIBUTING file of its own. I then read `docs/README.md` (reading order, single-source rules).
2. The issue #106 body (tasks 1-3, acceptance) and the manager comments on the issue:
   - evidence decision 5797308575;
   - scope decision 5798176959 (receive half);
   - correction 5801278433: the timer premise was wrong, so not restarting is a deviation, tracked in #108; call #2 accepted; call #1 stands;
   - assignment 5801860334.
3. Authorities as quoted in the repository and in those comments: 802.1Q-2014 §10.6, §10.7.5.20 (NOTE and b)2)), §10.7.9 with Table 10-5, §10.8, §10.8.1.2, §10.8.2.6, §10.8.2.8 f/g and §10.8.2.10.1 NOTE; Milan §4.2.7.1.2. Architecture: `docs/architecture/10_srp_engine.md` §6.5, `08_timing.md` F08.4, `docs/10_RESOURCE_AND_EFFORT.md` item 11. Trackers: #108 (open) and #29 (open, same deviation).
4. The diff `fbc1f715..27763677` (17 files) and `fc155c3c..27763677` (8 files), with history: 7 one-line commits, no trailers, linear on the base.
5. Executable evidence:
   - exact-head hosted runs of the `hdl` workflow (push and pull_request): every job executed and succeeded, none skipped;
   - the manager's public `manager-r2` bank at milan-fpga `abd34a36` `review-evidence/pp106-r1`;
   - my own suites, lint and mutation probes.

My verdict draft was written to disk (receipt `05`) before I read the prior reports R270-1 and R271-1. I have read no R271-2 material.

## 2. What was checked, per lens

```text
[R270] PASS Conformance - hdl/srp/KL_srp_decoder.sv:41-54,205-210,334,402-409; hdl/srp/KL_srp_top.sv:52-75,348,406,512,595; hdl/srp/KL_srp_talker_fsm.sv:411-421,620-630; hdl/srp/KL_srp_listener_fsm.sv:401-420; hdl/srp/KL_srp_encoder.sv:32-43,149-156,401-419 - per-type LeaveAll on transmit and receive against 802.1Q-2014 §10.7.5.20 NOTE and b)2), §10.8.2.6, §10.8 DLSDU order (call #2 layout processed in wire order, T1-T3), §10.7.9 own-LeaveAll scope; timer deviation documented and tracked (#108), RTL unchanged by this round (receipt 16); #106 tasks 1-3 met in-PR
[R270] PASS RTL - hdl/srp/KL_srp_decoder.sv:145,207-210,273,334,402-409 and KL_srp_top.sv:279-297,502-512,583-596 - 4-bit gate reset and re-armed at each MRPDU's first byte; lane index only reachable for types admitted by len_ok_w; lane and value strobes never share a cycle and reach the FSMs with no pipeline, so wire order is kept; correction-round hdl diff is comment-only; focused lint of 6 tops, 0 warnings (receipt 13)
[R270] PASS Robustness - tb/srp_decoder/sim_main.cpp:870-952 (U1-U4) and :806-868 (T1-T3) against KL_srp_decoder.sv:334,405-409 - gate re-armed after truncation mid-FirstValue, a single-EndMark PDU, a bad-AttributeLength discard (whose discarded Domain LeaveAll never fires) and an MVRP out-of-alphabet digit; invalid ordering (unflagged before flagged) within a message, across messages and on MVRP; arms A3, A4, A6, A9 killed (receipt 20)
[R270] PASS Tests - tb/srp_decoder/sim_main.cpp:629-639,806-952; tb/srp_top/sim_main.cpp:942-977 - exact full-timeline checks on hand-built byte-exact MRPDUs; the F5c Domain negative uses the same predicate and window as F5b's positive; fail-before/pass-after shown (arms survive at fc155c3c, receipt 21; killed at head, receipts 20 and 23); 4 SRP suites 177/556/1068/253 and pp_top 1411 all PASS locally and hosted (receipts 10, 14, 31)
[R270] PASS Docs - docs/10_RESOURCE_AND_EFFORT.md:552-565; docs/architecture/10_srp_engine.md:329-415; KL_srp_top.sv:52-75; KL_srp_encoder.sv:149-156; tb/srp_decoder/README.md:8,60-72,96-105; tb/srp_top/README.md:14,81-82,117-122 - the resource document no longer credits a restart; 10 §6.5 and the top banner point to #108; the NOTE criterion is stated; README tallies and mutation tables equal my measurements; links 810 OK, matrices OK (receipt 15); git diff --check clean; no U+2014 in lines this round adds
```

Notes behind these lines:

- **Gate semantics (decoder).**
  - `la_first_w = LeaveAllEvent==1 && !la_done_r[type-1]` at `S_VHDR2`. So the lane fires at the first flagged VectorHeader of its type, ahead of that vector's FirstValue and events. A later flagged header of the same type in the same MRPDU is not applied again.
  - An unflagged header never closes the gate. T1 (`E3 L3 E3 E3`), T2 (`E3 L4 E4 E4 L3 E3`) and T3 (`E1 M1 E1`) pin this.
  - Every MRPDU's first byte clears the gate, whatever ended the previous PDU (U1-U4).
  - Arm A6 moves the strobe to FirstValue completion. U1 alone kills it (1 FAIL), which pins that the LeaveAll of a vector truncated inside its FirstValue is still applied. The decoder banner's tolerance rule ("processed up to the bad field") allows this.
- **Routing (top and FSMs).**
  - Talker Advertise and Talker Failed lanes go to the talker applicants (by `fail_r`) and to the listener registrars (by `rtype_r`).
  - The Listener lane goes to the listener applicants and the talker registrar.
  - The Domain lane goes to `KL_srp_domain` only. MVRP goes to VLAN only.
  - An own LeaveAll still ORs into every registrar (`KL_srp_talker_fsm.sv:630`, `KL_srp_listener_fsm.sv:416`).
- **Transmit half.** The `fc155c3c..27763677` hdl change is comment-only (receipt 16). Arms E1-E3 are still killed at this head: LeaveAllEvent on the PDU's first VectorHeader only, no LeaveAll-only message, and the Domain type dropped from the set. They fail 128, 115 and 68 encoder checks, plus srp_top F1 (receipt 20).
- **Gate evidence.**
  - Exact-head hosted `hdl` runs 35914728215 (push) and 35914731568 (pull_request): docs-gates, suites and portability all executed and succeeded. The suites job reports 15464 checks, 0 failing, lint 37 OK and the nvm_port figures agreeing (receipts 30-31).
  - Manager `manager-r2`: donor-full bank at this head, 9 commands, all exit 0. Parent-consumer bank at `c088b4cf`, which is dev `26d855a9` plus a local gitlink commit, 7 commands, all exit 0 (receipt 32).
  - Builder gate 11 (physical calibration) did **not run**.

## 3. Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

## 4. Suggestions (do not affect the verdict)

**R270-2-S1**
- **Severity:** SUGGESTION. **Lenses:** Tests, Conformance.
- **Where:** `hdl/srp/KL_srp_talker_fsm.sv:630` and `hdl/srp/KL_srp_listener_fsm.sv:416`. No test observes registrar aging by an own LeaveAll.
- **Evidence:** §10.7.9, as restated in 10 §6.5:372-375, says an own LeaveAll generates LeaveAll events against every Registrar of the participant.
  - Arms C1 and C2 (the own term dropped from the talker or the listener registrar) survive all four suites at head (receipt 20).
  - Their base spellings survive at `fbc1f715` (receipt 22), so the gap is inherited. It was raised as R271-1 S1 (R10/R11), and the author's PR body lists it as not taken.
  - `la_own()` in `tb/srp_stream_fsms` is used only for the applicant txLA! walks (`sim_main.cpp:474,513,654`).
- **Impact:** a regression on these rewritten lines would go unseen. A registration whose peer never answers our own LeaveAll would then stay IN until the peer's own LeaveAll. The peer's per-type LeaveAll still ages it, so the exposure is bounded.
- **Outcome:** a follow-up issue adds `la_own()` IN→LV plus ARM checks for both FSMs, and/or an srp_top step in which the peer does not answer our own LeaveAll and the registration reaches MT.
- **Verification:** C1 and C2 go red.

**R270-2-S2**
- **Severity:** SUGGESTION. **Lenses:** Tests.
- **Where:** `hdl/srp/KL_srp_top.sv:406`, where the VLAN participant is fed `dec_la_mvrp_w || p_la_mvrp_r`.
- **Evidence:** arm B3 (the VLAN participant also takes every MSRP lane, R271-1 R5) survives at head (receipts 20, 23) and at base (receipt 22). The line is unchanged by the PR, so the gap is inherited.
- **Impact:** only a spurious MVRP re-join after an MSRP LeaveAll. But 10 §6.5 says the two applications' LeaveAlls never mix, and nothing checks it at the top level.
- **Outcome:** an srp_top check that an MSRP-only LeaveAll produces no MVRP re-join before the next periodic.
- **Verification:** B3 goes red.

**R270-2-S3**
- **Severity:** SUGGESTION. **Lenses:** Docs.
- **Where:** `docs/architecture/08_timing.md:119` (F08.4), `tb/timer_map/sim_main.cpp:45-46` and `hdl/common/pp_pkg.sv:179` (`PP_SRP_CAD_SLOTS_C = 7`).
- **Evidence:**
  - These count "the Domain and MVRP VID registrars" in the T-MRP-LEAVE pool.
  - 10 §6.5:347-348 and :369-370, together with the routing table this PR adds, say those types have no registrar. The RTL agrees: `KL_srp_top.sv:242` `N_CAD_C = 5`, and there is no Domain or VID registrar.
  - The sizing text predates the PR (it arrived 2026-08-11/12).
- **Impact:** two slots are reserved and never used, which is harmless. But two authoritative documents now answer "does the Domain type have a registrar" differently.
- **Outcome:** a follow-up issue that either records the two slots as reserved or drops them. Not in #106's scope.
- **Verification:** 08 F08.4 and 10 §6.5 agree, and the timer_map suite passes.

**R270-2-S4**
- **Severity:** SUGGESTION. **Lenses:** Docs.
- **Where:** `docs/10_RESOURCE_AND_EFFORT.md:562`, and the PR body.
- **Evidence:**
  - "its leavealltimer does not restart ... either" leaves the reader to resolve "its" to this spec. Writing "this spec's leavealltimer" would remove the ambiguity.
  - The PR body's "srp_top, 236 → 253 checks" gives a base count that measures 235 at `fbc1f715` (receipt 11). The base README said 230. The head count of 253 is correct.
  - #29 and #108 track the same deviation. Linking or closing one of them is the manager's call, as R271-1 S2 said.
- **Impact:** only a cold reader's accuracy.
- **Outcome:** optional wording fix; link #29 and #108.
- **Verification:** reading.

## 5. Prior public findings on PR #107, at this head

| prior finding | status at `27763677` | evidence |
|---|---|---|
| R270-1 F1 MINOR Tests: the gate's two boundaries are unpinned (X1, X7) | **Resolved** | T1-T3 and U1-U4 (`tb/srp_decoder/sim_main.cpp:806-952`). R270-1's own script, unmodified (SHA-256 equal to its manifest): X1 6 FAIL, X7 4 FAIL (receipts 23-24). My A1/A2 (X1-class) and A3/A9 (X7-class) are killed at head and survive at `fc155c3c` (receipts 20-21). |
| R270-1 F2 MINOR Docs: the resource document contradicts §6.5 on the timer restart | **Resolved** | `docs/10_RESOURCE_AND_EFFORT.md:552-565` keeps only the randomisation point. It states that this spec does not restart the timer either, and points to 10 §6.5 and #108. This agrees with `10_srp_engine.md:404-415` and `KL_srp_top.sv:71-75`. |
| R270-1 S1 SUGGESTION Tests: no Domain negative (X2) | **Taken** | F5c now asserts that no Domain JoinIn follows a Listener-only LeaveAll (`tb/srp_top/sim_main.cpp:963-968`). X2 and R4 give 1 FAIL at head and survive at `fc155c3c` (receipts 20, 21, 23). |
| R270-1 S2 SUGGESTION Docs: live tracker for the timer deviation | **Taken** (superseded by the manager ruling) | 10 §6.5:411-413 and the top banner cite #108, which is open with the Table 10-5 and §10.6 authority. |
| R270-1 S3 SUGGESTION Docs: state the §10.7.5.20 NOTE criterion for `4'b1111` | **Taken** | `KL_srp_encoder.sv:149-156` and 10 §6.5:343-348 say "supported by the application", whatever this participant declares or registers. |
| R271-1 F1 MINOR Tests, Robustness: unflagged-first layout and re-arm after a tolerance discard unpinned (R1, R8) | **Resolved** | R271-1's own script, unmodified: R1 KILLED 6, R8 KILLED 4 (receipt 23). Its required cases (i) within one message, across messages and on MVRP, and (ii) after truncation and after a bad AttributeLength, are T1-T3 and U1/U3, with U2 and U4 in addition. |
| R270-F2, retained by R271-1 | **Resolved** | as R270-1 F2 above. |
| R271-1 S1 SUGGESTION: R4 / R5 / R10-R11 | R4 **taken**. R5, R10 and R11 are **retained as suggestions** (R270-2-S2 and S1). | receipt 23: R4 KILLED; R5, R10, R11 SURVIVED at head, and inherited at base (receipt 22). |
| R271-1 S2 SUGGESTION Docs: §6.5 tracker; #29 vs #108 | The tracker part is **taken**. #29/#108 linking is **retained** (R270-2-S4, manager's call). | issue #108 and #29 are both open. |
| R271-1 S3 | Withdrawn by R271-1 | none |

## 6. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_decoder.sv:41-54,205-210,334,402-409`; `KL_srp_top.sv:52-75,348,406,512,595`; `KL_srp_talker_fsm.sv:411-421,620-630`; `KL_srp_listener_fsm.sv:401-420`; `KL_srp_encoder.sv:32-43,149-156,401-419`; issue #106 tasks and acceptance; manager decisions 5798176959 and 5801278433; clauses as quoted in 10 §6.5 | R270-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |
| RTL | CLEAN | decoder gate state, reset and re-arm (`:145,:207-210,:273,:334,:402-409`); strobe ordering into the FSMs (`KL_srp_top.sv:279-297,502-512,583-596`; `KL_srp_talker_fsm.sv:680-700`); comment-only proof `fc155c3c..head` (receipt 16); focused lint of 6 tops (receipt 13); hosted lint and portability, manager Yosys (receipts 31-32) | R270-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |
| Robustness | CLEAN | U1-U4 and T1-T3 (`tb/srp_decoder/sim_main.cpp:806-952`); arms A3, A4, A6, A9 (receipt 20); reset and first-byte re-arm | R270-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |
| Tests | CLEAN | `tb/srp_decoder/sim_main.cpp:20-195,629-639,806-975`; `tb/srp_top/sim_main.cpp:296-445,893-978`; `tb/srp_stream_fsms/sim_main.cpp:185-285,763-905`; `tb/srp_encoder` (arms E1-E3); 4 SRP suites plus pp_top at head, the 4 SRP suites at `fc155c3c` and `fbc1f715` (receipts 10-12, 14); 21 own arms, 18 killed, 3 inherited survivors (receipts 20-22); prior reviewers' scripts unmodified (receipts 23-24); hosted tallies (receipt 31) | R270-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |
| Docs | CLEAN | `docs/10_RESOURCE_AND_EFFORT.md:552-565`; `docs/architecture/10_srp_engine.md:307-415`; `08_timing.md:40,119`; the encoder, decoder and top banners; `tb/srp_decoder/README.md`, `tb/srp_top/README.md`, `tb/srp_stream_fsms/README.md`, `tb/srp_encoder/README.md` tallies against measured counts; PR body and issue evidence; link and matrix checks (receipt 15); `git diff --check`; em-dash count of added lines | R270-2 | 27763677d83d4df7237389ffc0945ef9e224aa31 |

## 7. Receipts (listed in `MANIFEST.sha256`)

| receipt | what it shows |
|---|---|
| `receipts/00_tool_identity.txt` | pinned simulator 5.050 wrapper and binary SHA-256; compiler and interpreter versions |
| `receipts/01_pre_probe_snapshot.txt`, `receipts/90_clone_integrity_after_probes.txt` | the clone before and after the probes: HEAD, tree, index == tree, all 224 tracked blobs re-hashed with 0 byte or mode mismatches, 0 untracked or ignored entries, index SHA-256 unchanged, 0 gitlinks (the PP repo has none) |
| `receipts/05_draft_verdict_before_prior_findings.txt` | my verdict and ledger draft, written before any prior report was read |
| `receipts/10_head_srp_suites.txt`, `11_base_fbc1f715_srp_suites.txt`, `12_fc155c3c_srp_suites.txt`, `14_head_pp_top_suite.txt` | suite tallies at head, at the source base and at the prior reviewed head |
| `receipts/13_focused_lint_head.txt`, `15_docs_checks_head.txt`, `16_hdl_comment_only.txt` | lint of the touched tops; link and matrix checks; the proof that the correction-round hdl change is comments only |
| `receipts/20_mutation_probes_head.txt`, `21_mutation_probes_fc155c3c.txt`, `22_inherited_arms_fbc1f715.txt` | 21 reviewer arms at head, 5 key arms at `fc155c3c`, and 3 survivors planted at base |
| `receipts/23_prior_reviewer_scripts_at_head.txt`, `24_prior_reviewer_script_sums.txt` | R270-1 X1/X7/X2 and R271-1 R1/R4/R8/R5/R10/R11 re-run unmodified at head, with their manifest checks |
| `receipts/30_hosted_check_runs_head.txt`, `31_hosted_suites_job_tallies.txt`, `32_manager_r2_public_evidence.txt` | exact-head hosted runs (executed, not skipped) and the manager's public bank results |
| `scripts/*` | every command above, portable: paths are arguments, `VERILATOR` comes from the environment (this round used the pinned 5.050 wrapper) |

All builds and probes ran in `git archive` exports under `scratch/`, which is not published. The review clone was only read, and it was verified byte-exact afterwards.

## 8. Real limits

- I did not run the full PP suite bank, Yosys, the nvm_port figures gate, or any parent, builder or gPTP bank. For those I rely on the manager's public `manager-r2` evidence and the exact-head hosted logs.
- I did not read the parent consumer checkout. It is a lane directory. The claim that `c088b4cf` sets the `protocol-processor` gitlink to this head comes from the manager's published JSON note, and the commit is not public. Parent dev `26d855a9` still pins `424c688f`, which is an ancestor of the source base.
- I checked clause wording only as quoted in the repository docs and the public comments. I did not consult the standards texts directly.
- The #530 end-to-end harness was last run at `9370f8ab` (PR body). I did not re-run it.
- Mutation probes are single-point text substitutions. I analysed each survivor rather than proving it equivalent.
- Physical calibration was NOT RUN: builder gate 11 was skipped, so there is no hardware or field evidence here. Skipped field gates are not hardware proof.

## 9. Pending manager duties

- Build and gate the final current-dev candidate at the merge turn: source base `fbc1f715` and live parent dev `26d855a9`. This is distinct from the source validation above. Own the hosted/act acceptance.
- Obtain the second independent positive review (the external round) at this exact head. No merge while a round is in flight.
- The #106 acceptance items that cannot be shown before merge:
  - the parent adopting the exact reviewed head;
  - a #530 silicon rerun showing a bound CRF talker streaming across LeaveAll cycles.

  `Closes #106` will close the issue at merge, so these need an explicit tracker (for example on #530). At adoption, update the parent's `docs/traceability/ieee8021q.md` row MRP-5, which still states per-application receive semantics (PR body, open item 4).
- Decide the #29/#108 duplicate. Optionally open issues for S1-S3.

R270-2 FINISHED
