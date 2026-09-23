[R271] POSITIVE - exact head 5f8cb1325312002c2c8bda45f30d98abc750ca7c

R271-3 is the external independent re-review of issue #106 / PR #107 after correction round 2 (A221).

- Head: `5f8cb1325312002c2c8bda45f30d98abc750ca7c`, tree `495bfb5d5fbcf7c73cb347b0e5f8b4420be9842c`.
- Source base: `fbc1f7156d711e5b7f511da8a16d9494256b017b`, the protocol-processor `main` tip, which has not moved. The head descends directly from it with no merges, so the head tree is the candidate merge tree in this repository.
- History: ten one-line commits, no trailers. This round's delta is three commits on `27763677` (where R270-2 is POSITIVE). It touches `tb/srp_decoder/{sim_main.cpp,README.md}` and `tb/srp_top/{sim_main.cpp,README.md}` only. `git diff 27763677 5f8cb132 -- hdl/` is empty, and every SRP RTL blob id is identical at both commits (receipt 01).
- Method: reconstructed with a cleared context from public state. My plants were written from the assignment's descriptions, not copied. My draft verdict was on disk (receipt 05) before I read any prior review text.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open under any lens at this head.
- **R271-2 F1 is resolved.** Each of the four gate plants K5-K8 survives at `27763677` and is killed at this head, by exactly the new decoder checks V1, V2 and V3. The control passes at both commits.
- **R271-2 S1 was taken.** K13 and K14 (the Domain participant also takes a talker lane) survive at `27763677` and are killed at this head by the two new F5c negatives.
- **No RTL changed.** The RTL reviewed clean in R271-2 and R270-2 is byte-identical here.
- Three suggestions remain open. All three predate this PR (section 4).

## 1. Reconstruction, in order

1. **Governance.** This repository has no AGENTS.md or CONTRIBUTING.md, so the parent's apply (kebag-logic/milan-fpga): the five lenses, severities, the ledger rule, and one-line commits. Then this repository's `README.md` and `docs/README.md`.
2. **Issue #106.**
   - The body: tasks 1-3 and the frozen acceptance.
   - The evidence decision 5797308575.
   - The receive-half scope decision 5798176959.
   - The manager's correction 5801278433: the timer is a deviation, tracked in #108; call #2 accepted; call #1 stands.
   - The assignments 5801860334 and 5803173950. The second is this round's scope: tests that kill K5-K8, S1 (K13/K14), no RTL change.
   - The author's REVIEW READY 5804048297 and the PR body.
3. **Authorities.** The IEEE 802.1Q-2014 clauses quoted in the issue, the PR and docs 10 §6.5: §10.6, §10.7.5.20 NOTE and b)2), §10.7.9 with Table 10-5, §10.8, §10.8.1.2, §10.8.2.6, §10.8.2.8 f/g and §10.8.2.10.1 NOTE. Also Milan v1.2 §4.2.7.1.2 and Table 4.3.
4. **Diff and history.**
   - The full range `fbc1f715..5f8cb132` (17 files).
   - The delta `27763677..5f8cb132`, commit by commit.
   - The whole of `hdl/srp/KL_srp_decoder.sv`, and the full-range diffs of the encoder, top, both stream FSMs and `srp_pkg.sv`.
   - The V9 path into the decoder (`KL_pp_rx_validator.sv:585-668`, then `KL_mrp_strip` in `protocol_processor_top.sv:2088-2106`).
5. **Executable evidence.**
   - My own runs (sections 2-3).
   - The manager's exact-head banks at `$VALIDATION_STORAGE/pp106-manager-r3` (receipt 24).
   - The public tree kebag-logic/milan-fpga @ `10673f47` `review-evidence/pp106-r1`, including the A221 packet.
   - The exact-head hosted runs (receipt 22).
6. **Prior public findings** (R270-1, R271-1, R270-2, R271-2): read only after receipt 05 was written (section 6).

## 2. What correction round 2 changed, and what I checked

| Commit | Change | My check at head |
|---|---|---|
| `c6149b25` | `tb/srp_decoder` V1-V3, 177 → 190 checks (`sim_main.cpp:956-1032`) | Recomputed every octet by hand:<br>- **V1:** list lengths 14, 9 and 14; `36` = JoinIn, `126` = JoinMt JoinMt, `108` = JoinMt, `0x80` = Ready. Expected `L3 E3 L4 E4 E4 E3`.<br>- **V2:** list 38 = 3 × 12 + 2, expected `L3 E3 E3 E3`.<br>- **V3:** 19 octets = 1+1+1+2+2+8+2+2 with list 12, padded to 46 (64 − 14 − 4).<br>`Harness::clear()` does not reset the DUT (`:88-92`), so the second V3 MRPDU really tests the re-arm across `S_PAD` (`KL_srp_decoder.sv:334,355,506-508`). Every expectation is a hand-written constant, checked as the full strobe timeline. |
| `4f240356` | `tb/srp_top` F5c extended to the Talker Advertise and Talker Failed lanes, 253 → 255 checks (`sim_main.cpp:978-996`) | Each negative runs in its own `sync()` slot (phase 250-350 ms, window 400 ms, so it never reaches the periodic boundary). It uses the F5b positive's predicate (`frame_has(fr, true, 4, 6, EV_JOININ)`).<br>Timing probe (receipt 15): F5c's own LeaveAll at 59007 ms, the windows open at 65250 and 66250 ms, F5 ends at 66651 ms (7.64 s), and the next own LeaveAll comes at 70807 ms (11.8 s). The comment at `:895-900` is right, and a stray own LeaveAll could only make the check fail, never pass vacuously. |
| `5f8cb132` | Suite READMEs record V and the two F5c negatives, with their arm tables | `tb/srp_decoder/README.md:8,73-81,116-125` and `tb/srp_top/README.md:14,79-84,126-133` agree with my measured tallies and kill counts. |

**Suites at head** (pinned simulator 5.050, `git archive` exports): srp_decoder 190/190, srp_encoder 556/556, srp_stream_fsms 1068/1068, srp_top 255/255 (receipt 10). The same four suites give 177/556/1068/253 at `27763677` and 113/180/1005/235 at `fbc1f715` (receipts 12, 16), which matches the PR body.

## 3. Plants: every assigned plant is killed, and the control survives

`scripts/plants.py` is my independent implementation. It puts each plant exactly once into a fresh `git archive` export and runs all four SRP suites. The kills are pinned to the new checks, because the same planted RTL bytes survive at `27763677` (receipts 11, 12).

| Plant | Planted behaviour | at `27763677` | at `5f8cb132` (failing checks) |
|---|---|---|---|
| K0 | control, no change | CONTROL PASSES (177/556/1068/253) | **CONTROL PASSES** (190/556/1068/255) |
| K5 | gate re-armed at a malformed or an unpadded clean end, never after a padded MRPDU | SURVIVED | **KILLED**: srp_decoder 1 (V3, the second padded MRPDU) |
| K6 | gate remembers only the last type that fired | SURVIVED | **KILLED**: srp_decoder 2 (V1) |
| K7 | an unflagged VectorHeader re-opens its type's gate | SURVIVED | **KILLED**: srp_decoder 2 (V2) |
| K8 | gate re-armed at every message whose AttributeType differs from the previous one | SURVIVED | **KILLED**: srp_decoder 2 (V1) |
| K13 | Domain participant also takes the Talker Advertise lane | SURVIVED | **KILLED**: srp_top 1 (F5c Talker Advertise LeaveAll) |
| K14 | Domain participant also takes the Talker Failed lane | SURVIVED | **KILLED**: srp_top 1 (F5c Talker Failed-only LeaveAll) |

Additional boundary plants of this round, all at head (receipt 11):

| Plant | Planted behaviour | Result |
|---|---|---|
| X-A | re-armed at every message | KILLED, 8 (S, V1) |
| X-B | re-armed only after a padded or a malformed MRPDU | KILLED, 26 + 4 |
| X-C | never re-armed | KILLED, 38 + 4 |
| X-D | Domain also takes the Listener lane | KILLED, F5c |

**Cross-check with R271-2's own script.** I ran R271-2's published `mutants.py` unmodified. Its SHA-256 `f15d1953…c237` equals R271-2's `MANIFEST.sha256` and the A221 packet copy. At head (receipts 20, 21):
- K0 passes.
- K5, K6, K7, K8, K13 and K14 are KILLED by the same checks.
- The earlier kills still hold: K1 6 (T1-T3), K3 4 (U1-U4), K10 1 (U4), K12 1 (F5c Listener-only).
- K15, K16 and K17 SURVIVE (section 4, S1).

My independent K6, K8, K13 and K14 plants, and X-D and X-E, produce planted files byte-identical (same SHA-256) to that script's K6, K8, K13, K14, K12 and K15.

## 4. Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### S1 - SUGGESTION - Tests, Conformance - two inherited routing properties are still unpinned by any suite (retained)

- **Where:** `hdl/srp/KL_srp_top.sv:406` (the VLAN participant takes `dec_la_mvrp_w || p_la_mvrp_r`); `hdl/srp/KL_srp_talker_fsm.sv:630` and `hdl/srp/KL_srp_listener_fsm.sv:416` (an own LeaveAll ages every registrar).
- **Authority / evidence:**
  - 10 §6.5 (`docs/architecture/10_srp_engine.md:372-375`) and §10.7.9: an own LeaveAll generates LeaveAll events against every Registrar of the participant. 10 §6.5 also says the MSRP and MVRP LeaveAlls never mix.
  - My plants X-E (VLAN also takes every MSRP lane), X-F (own LeaveAll dropped from the talker registrar) and X-G (the same for the listener registrars) pass all four suites at head (receipts 11, 17).
  - Their base spellings pass at `fbc1f715` (receipts 16, 18). The R271-2 script's K15-K17 agree (receipt 21).
  - The RTL is correct on all three lines. The gap predates this PR, and no correction round's assignment covered it.
- **Impact:** a later regression on these lines would go unseen. The own-LeaveAll case would leave an unanswered registration IN until the peer's own per-type LeaveAll ages it.
- **Required outcome:** optional, in a follow-up issue rather than here:
  - an srp_top or srp_stream_fsms check that an own LeaveAll moves an unanswered registration to LV and then MT;
  - a check that an MSRP-only LeaveAll produces no MVRP re-join before the next periodic.
- **Verification:** X-E, X-F and X-G (K15-K17) go red.

### S2 - SUGGESTION - Docs - one pronoun in the timer sentence can be misread (retained R271-2 S2 = R270-2 S4, first part)

- **Where:** `docs/10_RESOURCE_AND_EFFORT.md:561-562`, "that is not a point where this spec is right: its leavealltimer does not restart on a received LeaveAll either".
- **Evidence:** earlier in the paragraph "its" names the consumer. The line is unchanged at this head.
- **Impact:** a cold reader's accuracy only.
- **Required outcome:** optional: "this spec's leavealltimer".
- **Verification:** reading.

### S3 - SUGGESTION - Docs - the T-MRP-LEAVE pool sizing still counts Domain and VID registrars (retained R270-2 S3)

- **Where:** `docs/architecture/08_timing.md:119` (F08.4: "the Domain and MVRP VID registrars"), `hdl/common/pp_pkg.sv:179` (`PP_SRP_CAD_SLOTS_C = 7`) and `tb/timer_map/sim_main.cpp:45-46`.
- **Evidence:**
  - The routing table this PR adds to 10 §6.5 says the Domain and VID types have no registrar here.
  - `KL_srp_top.sv:242` uses `N_CAD_C = 5`.
  - The sizing text predates the PR.
- **Impact:** two timer slots reserved and unused, which is harmless. But two authoritative pages answer "does the Domain type have a registrar" differently.
- **Required outcome:** optional, in a follow-up issue: record the two slots as reserved, or drop them.
- **Verification:** F08.4 and 10 §6.5 agree, and the timer_map suite passes.

## 5. Clean-lens lines

```text
[R271] PASS Conformance - docs/architecture/10_srp_engine.md:329-415; hdl/srp/KL_srp_decoder.sv:41-54,205-210,334,402-409; hdl/srp/KL_srp_top.sv:55-75,348,406,512,595; hdl/srp/KL_srp_talker_fsm.sv:411-421,630; hdl/srp/KL_srp_listener_fsm.sv:401-420; hdl/srp/KL_srp_encoder.sv:32-43,146-156,401-419,534-556,677-693 - checked against issue #106 tasks 1-3 and decisions 5797308575, 5798176959 and 5801278433:
  - every supported type (MSRP 1-4, MVRP VID) is flagged by the §10.7.5.20 NOTE criterion, with NumberOfValues-0 vectors (§10.8.2.8 f/g);
  - a received LeaveAll is routed per type, once per MRPDU, ahead of its type's events in DLSDU order (§10.7.5.20 b)2), §10.8.2.6, §10.8), with call #2 as accepted;
  - the once-per-MRPDU gate stays closed to the MRPDU's end and re-arms at the next MRPDU's first byte, now pinned by V1-V3;
  - the timer is stated as a deviation from Table 10-5/§10.6, tracked in #108.
  - The out-of-source acceptance items (parent adoption, #530 silicon rerun) are manager duties (section 10).
[R271] PASS RTL - hdl/srp/*.sv and srp_pkg.sv blob ids identical at 27763677 and 5f8cb132 (receipt 01); KL_srp_decoder.sv:145,207-210,273,331-337,349-361,386-426,506-508 read in full - checked:
  - lane index = type-1 reachable only past len_ok_w;
  - la_done_r reset, set at the first flagged VectorHeader and cleared only at an MRPDU's first byte, whatever ended the previous MRPDU;
  - the shared bit 0 (MSRP Talker Advertise / MVRP VID) is safe because an MRPDU is one application;
  - encoder LeaveAll-only path writes a zero FirstValue (fv_byte_f on run_first_r = 0, :202-205, :684-687);
  - focused lint of the five changed SRP tops OK (receipt 13); manager lint 37 OK and the Yosys gate at head (receipt 24).
[R271] PASS Robustness - tb/srp_decoder/sim_main.cpp:872-1032 (U1-U4, V1-V3) against KL_srp_decoder.sv:334,355,405-409,506-508 - gate re-arm after truncated, single-EndMark, bad-AttributeLength and out-of-alphabet MRPDUs, and after a well-formed MRPDU followed by minimum-frame padding; no re-open after another type's message or after an unflagged vector of the type; plants K5-K8, X-A..X-C and K1/K3/K10 killed at head (receipts 11, 20, 21).
[R271] PASS Tests - tb/srp_decoder/sim_main.cpp:956-1032 and tb/srp_top/sim_main.cpp:893-998 - the new checks fail for exactly the defects they claim (K5-K8, K13, K14: SURVIVED at 27763677, KILLED at head, planted RTL bytes identical); positive and negative controls (K0, F5b positive vs F5c negatives); four SRP suites 190/556/1068/255 locally, and 30 suites with 15,479 checks, 0 failing, in the manager's exact-head bank and in both exact-head hosted runs (receipts 10, 22, 24); S1 is optional.
[R271] PASS Docs - tb/srp_decoder/README.md:8,73-81,116-125; tb/srp_top/README.md:14,79-84,126-133; tb/srp_top/sim_main.cpp:895-900; docs/architecture/10_srp_engine.md:307-415; docs/10_RESOURCE_AND_EFFORT.md:552-565 - checked:
  - the README tallies and arm tables equal my measurements;
  - make check OK (lint 41+18, links 810, matrix 115 REQ, module matrix 86 rows / 0 untested, stale);
  - git diff --check fbc1f715..head clean, and no U+2014 in any line this round adds (receipt 14);
  - no host-identifying text in the added lines;
  - the PR body and the A221 issue comment are accurate against my runs;
  - S2 and S3 are optional.
```

## 6. Prior public findings on PR #107, resolved or retained at this head

Read after receipt 05 was on disk.

| Prior finding | Status at `5f8cb132` | Evidence |
|---|---|---|
| **R271-2 F1**, MINOR, Tests/Robustness: the once-per-MRPDU gate pinned on only part of its boundary; K5-K8 survive | **RESOLVED** | V1 kills K6 and K8, V2 kills K7, and V3 kills K5. All four survive at `27763677`. Confirmed with my own plants (receipts 11, 12) and with R271-2's script unmodified (receipt 20). The required outcome's three cases are exactly V1, V2 and V3. The T and U checks stay, and their kills still hold (receipt 21). |
| **R271-2 S1**, SUGGESTION, Tests: the Domain negative covers the Listener lane only (K13/K14) | **RESOLVED** (taken) | The F5c Talker Advertise and Talker Failed-only negatives kill K13 and K14. Both survive at `27763677`. |
| **R271-2 S2** = R270-2 S4 (first part), SUGGESTION, Docs: "its leavealltimer" | **RETAINED** as S2 | Unchanged at `docs/10_RESOURCE_AND_EFFORT.md:561-562` (tests-only round). |
| R270-2 S4 (second part): PR body base count 236 | **RESOLVED** | The PR body now states 235 at `fbc1f715`, which matches receipt 16. |
| **R271-1 S2** = R270-2 S4 (third part), SUGGESTION: #29 and #108 track one deviation | **RESOLVED** | The manager closed #29 on 2026-09-23 22:34 UTC as a duplicate of #108 (not planned). #108 is open (receipt 23 and the issue record). |
| **R271-1 S1** R5/R10/R11 = R270-2 S1/S2 = R271-2 K15-K17, SUGGESTION: inherited routing gaps | **RETAINED** as S1 | Survive at head and at base (receipts 11, 16-18, 21). |
| **R270-2 S3**, SUGGESTION, Docs: F08.4 counts Domain and VID registrars | **RETAINED** as S3 | Unchanged at head. |
| R270-1 F1 = R271-1 F1 (gate boundaries X1/X7, R1/R8), R270-1 F2 = retained R270-F2 (timer doc), R270-1 S1-S3 | **RESOLVED** at `27763677` (R270-2, R271-2), and they still hold | K1, K3, K10 and K12 are killed at head (receipt 21). `docs/` and `hdl/` are unchanged since `27763677` (receipt 01). |
| R271-1 S3 | Withdrawn in R271-1 | none |

## 7. Ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #106 body and decisions 5797308575, 5798176959, 5801278433, 5803173950. 10 §6.5 `:329-415`. Decoder `:41-54,205-210,334,402-409`. Top `:55-75,348,406,512,595`. Talker FSM `:411-421,630`. Listener FSM `:401-420`. Encoder `:32-43,146-156,401-419,534-556,677-693`. | R271-3 | 5f8cb1325312002c2c8bda45f30d98abc750ca7c |
| RTL | CLEAN | Decoder read in full. Full-range RTL diffs of encoder, top, FSMs and `srp_pkg.sv`. Blob ids equal at `27763677` and head (receipt 01). Focused lint (receipt 13). Manager lint and Yosys gate at head (receipt 24). | R271-3 | 5f8cb1325312002c2c8bda45f30d98abc750ca7c |
| Robustness | CLEAN | U1-U4 and V1-V3 against the gate's set and clear points. Padded, malformed, interleaved-type and repeated-flag MRPDUs. Plants K5-K8, X-A..X-C, K1/K3/K10 (receipts 11, 20, 21). | R271-3 | 5f8cb1325312002c2c8bda45f30d98abc750ca7c |
| Tests | CLEAN (S1 optional) | Four SRP suites at head, `27763677` and `fbc1f715` (receipts 10, 12, 16). 12 own plants at head, 8 at `27763677`, 4 at base (receipts 11, 12, 16-18). R271-2 script unmodified, 14 plants (receipts 20, 21). F5c timing probe (receipt 15). Hosted and manager 30-suite tallies (receipts 22, 24). | R271-3 | 5f8cb1325312002c2c8bda45f30d98abc750ca7c |
| Docs | CLEAN (S2, S3 optional) | Both suite READMEs, the `srp_top` F5 comment, 10 §6.5, the effort doc §11, the banners. `make check`, diff-check and em-dash (receipt 14). PR body and the A221 issue comment. | R271-3 | 5f8cb1325312002c2c8bda45f30d98abc750ca7c |

## 8. Receipts and reproduction

Every file below is listed in `MANIFEST.sha256`. Host paths are written `$PACKET`, `$CLONE` and `$VALIDATION_STORAGE`.

| file | content |
|---|---|
| `receipts/00-tools.txt` | pinned simulator 5.050: launcher and binary SHA-256; compiler, interpreter, git and make versions |
| `receipts/01-scope-and-history.txt` | commits, trees, one-line messages; delta name-status; empty `hdl/` diff; SRP RTL blob ids at `27763677` and head |
| `receipts/05-draft-verdict-before-prior-findings.txt` | draft verdict, written before any prior review text was read |
| `receipts/10-control-head.txt` | the four SRP suites at head (K0) |
| `receipts/11-plants-head.txt` | K0, K5-K8, K13, K14 and X-A..X-E at head, with planted SHA-256 and FAIL lines |
| `receipts/12-plants-parent-27763677.txt` | K0, K5-K8, K13, K14 and X-E at `27763677`: all survive |
| `receipts/13-focused-srp-lint-head.txt` | lint of the five changed SRP tops |
| `receipts/14-docs-gates-head.txt` | `make check`, `git diff --check fbc1f715..head`, em-dash count of the delta's added lines |
| `receipts/15-f5c-timing-probe.txt` | F5 timeline at head (harness-only prints in a disposable export) |
| `receipts/16-control-base-fbc1f715.txt` | control and X-E at the source base |
| `receipts/17-inherited-gaps-head.txt`, `receipts/18-inherited-gaps-base.txt` | own-LeaveAll registrar-aging plants at head and at base |
| `receipts/20-r271-2-mutants-unmodified-head-a.txt`, `receipts/21-r271-2-mutants-unmodified-head-b.txt` | R271-2's published script, unmodified, at head: K0, K5-K8, K13, K14 / K1, K3, K10, K12, K15-K17 |
| `receipts/22-hosted-exact-head.txt` | exact-head hosted runs, jobs, steps and suite tallies |
| `receipts/23-refs-and-parent.txt` | PP `main` and PR branch tips; parent dev, its gitlink, and the MRP-5 row |
| `receipts/24-manager-r3-bank-read.txt` | the manager's exact-head banks: commands, exit codes, key lines, and SHA-256 of every file read |
| `receipts/90-clone-integrity.txt` | the clone after every probe |
| `scripts/plants.py`, `scripts/verilator_capped.sh` | independent plants; build-job cap |
| `scripts/focused_srp_lint.sh`, `scripts/f5c_timing_probe.py`, `scripts/verify_clone.sh` | lint, timing probe, clone verification |
| `scripts/r271-2-published/*` | R271-2's published scripts, byte-identical to its manifest |

Reproduce with the following (8 build jobs in total):

```sh
PINNED_VERILATOR=<pinned 5.050 launcher> VL_JOBS=2 PLANT_POOL=4 python3 scripts/plants.py $CLONE <rev> <scratch> <receipt> [ids]
REAL_VERILATOR=<pinned 5.050 launcher> VL_JOBS=2 python3 scripts/r271-2-published/mutants.py $CLONE <rev> <scratch> <receipt> [ids]
```

**Clone integrity** (receipt 90, run after every probe):
- HEAD and tree are the reviewed ones, and the index equals the HEAD tree;
- all 224 tracked entries were re-hashed from disk with their modes: 0 mismatches;
- status is clean, with no modified, untracked or ignored entries.

This repository has no `.gitmodules` and no gitlink, so no submodule pin is required. Every build and probe ran in disposable exports under `scratch/`, which is not published. Nothing in the clone or any other checkout was written.

## 9. Real limits

- **No full banks.** By rule I ran no full protocol-processor bank, Yosys, nvm figures, parent, gPTP or builder bank, act, Docker or hardware. For those I rely on:
  - the manager's exact-head donor-full bank: 9/9 exit 0. Lint 37 OK; 30 suites, 15,479 checks, 0 failing; `make check`; matrix; Yosys 32 tops OK plus the Xilinx map; nvm figures; `git diff --check fbc1f715 HEAD` clean.
  - the parent-consumer bank at `f2b32428` (dev `26d855a9` plus one local gitlink commit to this head, per the manager's note): 7/7 exit 0. xvlog PASS; pp_shadow 371/0; builder with **gate 11 (physical calibration) NOT RUN**.

  These banks are read from `$VALIDATION_STORAGE`. They are not yet in the public evidence tree, whose latest bank at `10673f47` is `manager-r2` at `27763677`. I did not open the parent-consumer checkout, so the gitlink claim rests on the manager's note.
- **Hosted runs.** At the exact head, the `hdl` workflow ran on push (35929006641) and pull_request (35929011873). docs-gates, suites and portability all executed and succeeded, and both suites jobs report 15,479 checks, 0 failing. Only the "Build Verilator v5.050" step was skipped, on a cache hit. The hosted/act acceptance belongs to the manager.
- **Hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof. The #530 end-to-end harness was last run at `9370f8ab`, not at this head. No post-change silicon run exists.
- **Standard text.** The standard texts are not in the repositories. Clause wording was judged as quoted by the issue, the PR and the docs.
- **Plants are a sample.** They are single-point substitutions. Survivors were analysed, not proved equivalent.
- **Disk full, handled.** One run of R271-2's script aborted mid-K12 with "No space left on device" on the shared review filesystem, which was at 100%. That run wrote no receipt. I deleted only my own scratch build directories and re-ran the full list in two batches (receipts 20, 21). The event may have affected other jobs on that filesystem at the same time.

## 10. Pending manager duties

1. **Second positive and merge bar.** R270-2's positive is at `27763677`. This round changes `tb/` only, which is within the Tests and Docs lenses, so the manager decides whether R270's ledger needs those two lenses re-banked at this head, or accepts this round's coverage. No merge while a round is in flight.
2. **Final current-dev candidate.** Build and gate it at the merge turn, with source base `fbc1f715` and live parent dev `26d855a9`, whose gitlink is still `424c688f`, an ancestor of the base (receipt 23). This round's evidence is source validation, not that candidate. Builder gate 11 is NOT RUN.
3. **Publish the exact-head manager banks** (`pp106-manager-r3`) in the public evidence tree, next to `manager` and `manager-r2`.
4. **Parent traceability.** At adoption, `docs/traceability/ieee8021q.md` row MRP-5 at dev `26d855a9` still reads "on rx/tx LeaveAll, all registrations enter leave-pending". This head replaces those per-application receive semantics.
5. **Acceptance outside source.** The parent must adopt the exact reviewed head, and a #530 silicon rerun must show a bound CRF talker streaming continuously across LeaveAll cycles. `Closes #106` closes the issue at merge, so these need an explicit tracker. The evidence decision records that the #108 timer deviation may still end about 2 % of cycles; that is arithmetic, not a measurement.
6. **Optional follow-ups:** S1 and S3 as new issues, and S2's one-word fix.

R271-3 FINISHED
