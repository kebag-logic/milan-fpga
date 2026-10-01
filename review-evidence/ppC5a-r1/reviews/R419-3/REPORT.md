[R419] POSITIVE - exact head ee0e2b72ea10c83f983ec9e35878fb0193223ccb

# R419-3 external review: processor PR #140 (lane C5a, AECP deadlines and the scoreboard), rounds 3 and 3b

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #140 (`c5a-aecp-deadlines` into `main`). Closes #57; relates to #81 and #84.
- Exact head `ee0e2b72ea10c83f983ec9e35878fb0193223ccb`, tree `3eb7d8ec80192da62a2c2c3966628782c5d93854`. It is a merge commit with parents `d4ca85c` and main `16ea10ac`.
- Previous head reviewed by this reviewer: `44a6bb90` (R419-2, NEGATIVE on one MINOR, F5). Only the delta is judged here:
  - 97fe22f, the merge of main 3f3ea56b (#135, #137);
  - e4c70b5, the F5 ruling;
  - d4ca85c, the 08 §4 hold bounds and the DL8 label;
  - ee0e2b7, the merge of main 16ea10ac (#138, lane C5b).
- Assignments: #81 comments 5929634478 (round 3) and 5936567141 (round 3b). Review start: PR #140 comment 5940967371.

**Verdict: POSITIVE.**

- R419-2 F5 is resolved under the ruled option. The classifier comment is now true. 03 §6 records the limitation, and the PR body's #84 remainder names it. My round-2 probe, re-run unchanged at this head, gives the documented result: G0 waits, G1 is admitted beside the held step.
- Both merges keep both sides. Every line either side added is carried, except resolution edits, and every resolution edit is one of these:
  - a build count (three or two becoming four);
  - a union (`.PHONY`, `one_section`, `load_descriptor_image`, the µCPU batch flag);
  - one of the two re-cut patches.
- The lane's non-comment RTL change is identical before and after both merges. The top's port and parameter header is byte-identical to main's.
- The re-cut C5b arms fail exactly the same checks as main's originals do on main.
- The lane's whole campaign gives 5 controls PASS and 55 of 55 arms KILLED, every count equal to the README.
- The whole `tb/pp_top` suite gives 8,901 checks with 0 failing, over four builds. `tb/ucpu` gives 427 of 427.
- I found no BLOCKER, MAJOR or MINOR finding. There are two SUGGESTIONs.

## 1. Reconstruction, in the prescribed order

1. **Workflow rules.** This repository has no AGENTS.md or CONTRIBUTING.md (searched the tree). I read `docs/README.md`: its single-source rules (timing only in F08.1, layouts only in 07, `Δn` deltas), its citation rules, and "`make check` must pass".
2. **Issue scope.**
   - Frozen acceptance: #81 1-4, #57 1-3 and #84 1-4. Lane assignment 5915626788.
   - Round-2 ruling 5923634905.
   - Round-3 ruling 5929634478. It rules F5 with the reviewer's first outcome and no RTL change: the comment made true, the limitation in 03 §6, and the #84 remainder in the PR body. It also orders the merge of 3f3ea56b and asks for S1, S2 and S6 where cheap.
   - Round-3b ruling 5936567141. It orders a `--no-ff` merge of 16ea10ac that keeps both sides. Both campaigns (`aecp_mutants.py` and `aecp_dispatch_mutants.py`) are to be kept, and the work stops on any port, parameter or parent-visible change.
   - The executors' TAKEN and REVIEW READY comments: 5936548637 (d4ca85c) and 5940939453 (ee0e2b72).
3. **Authorities.**
   - 03 §6: F03.7, rule (5) the MAP_CFG cross-lock, and the RO_SNAPSHOT rule "blocked only vs in-flight write on the same key".
   - 08 §4: F08.3 and the ACMP-wait paragraph.
   - 06 §8.1; 09 §8.3.
   - IEEE 1722.1-2021 §7.4.76.1 and .2, §7.2.3, §7.2.6, §7.2.32 and §9.2.2.6 (cdl ≤ 524); Milan v1.2 §5.4.2.10 and §5.4.3.3 Table 5.19. These were read through their in-tree quotations, because the specification PDFs are not in the tree.
4. **Diff and history.**
   - `git diff 16ea10ac..ee0e2b72`: 65 files, +3,918/−101. That is the whole lane against current main.
   - `git show --remerge-diff` of both merges (every conflict hunk and its resolution).
   - `git show` of e4c70b5 and d4ca85c.
   - The commit shape: one-line subjects, no bodies, merges with two parents.
5. **Public evidence.**
   - The pinned evidence commit `4fe37ada` is the round-2 archive (07:46Z) and has no `author-r3` or `author-r3b`. Those packets are on the same evidence branch at `cbba1828` (21:26Z), which I used.
   - Their sha256 values equal `MANIFEST.json`'s `published_sha256` (HANDOFF files path-redacted).
   - `author-r3b/PR-BODY.md` equals the live PR body apart from a trailing newline.
   - `parent-adaptation-137-acmp-disposition.patch` is exactly #137's four-line `DUT_READER_DISPOSITIONS` entry.
   - Manager evidence comments: PR #140 comment 5921897578 (banks at f963fe9a). The #81 ruling 5929634478 states the banks at 44a6bb90. I found no manager bank comment for ee0e2b72 on the PR or the issue (section 8).
6. **Prior findings.** I read them only after my independent pass and after this verdict and ledger were drafted:
   - R419-2, my own report;
   - R418-2, the round-2 internal review, archived at `cbba1828`: its findings section only.
   - I did not read the parallel round-3 internal review.

## 2. Independent pass over the delta

### 2.1 F5 ruling (e4c70b5, then the widening in ee0e2b7)

- `hdl/top/protocol_processor_top.sv:1464-1476`: READ_DESCRIPTOR "loses nothing" by the no-descriptor key; GET_DYNAMIC_INFO "does, a known gap". Its GET_STREAM_INFO records of a STREAM_INPUT read `lstn_gsi_status_r`, which ACMP listener steps write, so the batch is not serialized against them.
  - Checked against the RTL. `gsi_owner_read` (`:3387-3398`) serves selector 7 of a STREAM_INPUT from `lstn_gsi_status_r[sink]`, which is written only by the listener record write (`:3347-3362`).
- `docs/architecture/03_packet_engine.md:229-239` states the same limitation, cites IEEE 1722.1-2021 §7.4.76.1 and Milan §5.4.2.10, and contrasts it with HZ6. It leaves serialization to a later #84 item.
- The PR body's "What remains" (#84) names it, and #84 stays "Relates to".
- **The widened READ_DESCRIPTOR statement holds.**
  - Since main's #82, READ_DESCRIPTOR overlays the current sampling rate, clock source index and stream format: `E_RDESCAU`, `E_RDESCCD`, `E_RDESCSI` and `E_RDESCSO` in `hdl/aecp/ucode/gen_ucode.py:1114-1180`. Each reads `RGN_DYN`/`RGN_DYNV` rows of `KL_aecp_dyn_state`.
  - That store has one state port (`KL_aecp_dyn_state.sv:82-118`). It is instantiated only inside `KL_aecp_engine` (`:1915-1945`), driven by the µCPU or by the D3 restore writer through the engine's state-bus selection.
  - No ACMP path reaches it, so the no-descriptor key loses no conflict for READ_DESCRIPTOR under F03.7's RO_SNAPSHOT rule.

### 2.2 08 §4 hold bounds and the DL8 label (d4ca85c)

I checked each number in `docs/architecture/08_timing.md:186-210` against the RTL:

- **Not preempted.** `ucpu_preempt_w = dl_kill_r && (a_st_r == A_RUN) && !regun_r && !lockc_r && !amap_edit_r` (`KL_aecp_engine.sv:1749-1750`). So REGISTER/DEREGISTER, LOCK_ENTITY and the map edits are never preempted.
- **The watchdog.** The shared `gather_watchdog` (`:2373-2386`) counts each continuous face hold up to `MEM_TIMEOUT_CYC_P`, which is `DESC_MEM_TMO_CYC_P` = 4,096 at the top (`protocol_processor_top.sv:133`, `:3671`). After it fires, every later hold is masked by `!gxf_fail_r` (`:2315-2328`), so one wedged face cannot stall twice.
- **LOCK_ENTITY.** `E_LOCKEN` (`gen_ucode.py:1062`) makes two registry-face gathers (RG_OP, RG_STATE). That is 2 × 4,096 = 8,192 clocks, 81.9 µs at 100 MHz.
- **The map edits.** `E_AMADD` (`gen_ucode.py:1997`) makes one BEGIN, N validations, one COMMIT_BEGIN, N commit records and one FINISH, which is 2N + 3 edit-face waits.
  - The cdl gate (`KL_aecp_engine.sv:3270-3273`) refuses cdl ≠ 20 + 8N and cdl > 524, so N ≤ 63.
  - 129 × 4,096 = 528,384 clocks, about 5.3 ms. Correct.
- **The hold list.** It is complete for ACMP's two classes (RO_SNAPSHOT and STREAM_CFG on stream keys): the barrier, LOCK_OP against a step, the MAP_CFG cross-lock, and same-key AECP commands. REGISTRY_OP meets no ACMP transaction (03 §6).
- **The DL8 label.** "a command padded to 540 payload bytes" appears in `tb/pp_top/sim_main.cpp:12153`, `aecp_mutants.py:68` and the 09 §8.3 row. The harness frame is 38 + payload bytes (`aecp_frame`), so 8 + 532 payload bytes give the "578-byte echo" the row names. The arm `mvu-echo-slot-std` is still KILLED, with its named check (1 failure).

### 2.3 The merges (97fe22f, ee0e2b7)

- **Remerge-diff.** 97fe22f had two conflicts, both unions: `.PHONY` and `one_section`. ee0e2b7 had eight conflicted files. Each resolution keeps both sides:
  - `.gitattributes` keeps both exemptions;
  - `hdl.yml` keeps both campaign steps, `aecp-mutants` then `aecp-dispatch-mutants`;
  - the Makefile has four builds, a tally expecting 4, both mutant output variables, every target of both sides in `.PHONY`, and `clean` removing `obj_line` and `obj_tim`;
  - the wrap has both tap groups and both define-driven overrides;
  - `sim_main.cpp` has `load_descriptor_image(entity_cfg, extra_ents, extra_bodies, sigmux_len)`, AX beside DL, TB and HZ, and `main()` with the fixture, line and timebase builds and all nine focus flags;
  - both READMEs keep both campaign tables and a four-row build table;
  - the µCPU bench has `disp_batch_i = batch || batch_base >= 0`.
- **Mechanical side check.** `scripts/merge_side_check.py` compares the multiset of lines each side changed against what the merge carried to the other side (`merge_*_side_*.txt`).
  - For both merges and both sides, every line not carried is replaced by a resolution edit of the kinds listed above.
  - No hunk of #135, #137 or #138 is lost against main 16ea10ac: 97fe22f checked against base 0451d83d, ee0e2b7 against base 3f3ea56b. #136 is the lane's own base (0451d83d is "Merge pull request #136"), so it is in the branch by construction.
- **RTL unchanged by the merges.** `receipts/rtl-delta-check.txt` compares the lane's non-comment RTL lines, `0451d83d..44a6bb9` against `16ea10ac..ee0e2b7`, and they are IDENTICAL. Rounds 3 and 3b add 6 RTL lines and remove 1, all comments.
- **Interfaces** (`receipts/interface-checks.txt`):
  - The top's header is byte-identical to main's (677 lines, sha `7b5c29f7…`).
  - With comments stripped, it is identical at 0451d83d, 3f3ea56b, 44a6bb9, d4ca85c, 16ea10ac and the head.
  - The engine's header equals round 2's. The µCPU's header is the union of main's `RESP_D8_CAP_BYTES_P` and the lane's preempt ports. Both are internal.
  - No RTL file was added, deleted or renamed.
- **The two re-cut C5b patches plant the same defect.**
  - At the merge, `txs_oversize_o` is `(frame_len_r > TX_STD) || (st_echo_w && echo_len_w > TX_STD)` (`KL_aecp_engine.sv:2583-2585`).
  - `ov-oversize-never` forces the whole request to `1'b0`, as on main.
  - `ov-oversize-at-576` changes `>` to `>=` on the frame-length term, the only term main had.
  - Executed: both arms are KILLED at 18 and 4 at the head. Main's original patches on main 16ea10ac are also KILLED at 18 and 4. **The failing-check lists are identical line for line** (`receipts/dispatch-arms-main-vs-head.txt`), and both counts equal the README.

## 3. Executed evidence (exact-head exports under scratch; the reviewed clone was never built in)

The simulator is Verilator 5.050, rev v5.050 (pinned wrapper, sha256 `905795b9…`). Every heavy run used an eight-CPU mask, one at a time.

| Receipt | What | Result |
|---|---|---|
| `receipts/pp_top-run.log` | `make -C tb/pp_top run` (four builds) | rc 0. **8,901 checks, 0 failing**: default 8,607, fixture 20, line 218 (DESC_LINE_BYTES_P 584), timebase 56. Sections DL 64, HZ 176, D3 133, AX 218, TB 56, ACMP 43 and AD 55, all with 0 failures. These equal the PR body's figures |
| `receipts/ucpu-run.log` | `make -C tb/ucpu run` | rc 0, **427 of 427** |
| `receipts/probe-gdi-stream-info.log`, `scripts/probe_gdi_stream_info.py` (byte-identical to R419-2's, sha `6cfd0162…`) | the F5 probe, unchanged | **G0** (a stand-alone GET_STREAM_INFO of STREAM_INPUT 1 against a held UNBIND_RX of sink 1) WAITED, refused 498 clocks. **G1** (a GET_DYNAMIC_INFO carrying that record) was ADMITTED BESIDE: refused 0 clocks, class 0, key 0xFC00. G2 (beside a held GET_RX_STATE) was admitted beside. HZ: 179 checks, 0 failures. This equals 03 §6 and the PR body |
| `receipts/aecp-mutants-head.log`, `receipts/aecp-mutants-vs-readme.txt` | the lane's `aecp_mutants.py`, all arms | rc 0: **5 controls PASS, 55 of 55 KILLED, each with exactly one named failing check**. `scripts/compare_campaign_counts.py`: 55 of 55 counts equal the `tb/pp_top/README.md` cells, the "the same N" cells included |
| `receipts/dispatch-recut-arms-head.log`, `receipts/dispatch-orig-arms-main16ea10ac.log`, `receipts/dispatch-arms-main-vs-head.txt`, `receipts/dispatch-recut-vs-readme.txt` | C5b's two re-cut arms at the head; main's originals at 16ea10ac | Both runs: control PASS, `ov-oversize-never` 18, `ov-oversize-at-576` 4, each named. Identical failing-check lists. Both equal the README |
| `receipts/lint_hdl.log` | `scripts/lint_hdl.sh` | rc 0, 41 modules LINT OK |
| `receipts/docs-*.log`, `receipts/gen_matrix-check.log` | `make links matrix modmatrix params`; `gen_matrix.py --check` | rc 0: 1,017 links; 115 REQ rows, 17 GAPs; 94 rows, 0 untested; parameters 26/26/26 |
| `receipts/git-checks.txt` | `git diff --check` from 0451d83d, 44a6bb9, 3f3ea56b, d4ca85c and 16ea10ac; commit shape; ancestry | All clean. The two merges have two parents each; subjects only, no body or trailer. 44a6bb9, 3f3ea56b, 16ea10ac and 0451d83d are ancestors |
| `merge_*_side_*.txt`, `scripts/merge_side_check.py` | each side of each merge, carried | Section 2.3 |
| `receipts/rtl-delta-check.txt`, `receipts/interface-checks.txt` | RTL and interface identity | Section 2.3 |
| `receipts/hosted-exact-head-snapshot.txt` | read-only, 21:59Z | Runs 36928701582 (pull_request) and 36928699036 (push), both at ee0e2b72. `docs-gates` and `portability` succeeded. In `suites`, "Lint (zero tolerance) + every suite" succeeded; the SRP campaign was in progress, and the MAAP, ADP, AECP-deadline and AECP-dispatch campaign steps, the matrix step and the nvm_port step were pending. "Build Verilator" was skipped on a cache hit. Closing references: **[57]** only. Mergeable, not a draft |
| `receipts/tree-integrity-final.txt` | the clone after every run | HEAD, HEAD tree and index tree are exact. Detached. `status --porcelain --ignored` is empty. 468 of 468 tracked blobs rehash equal, with no mode drift and no assume-unchanged or skip-worktree flags. **0 gitlinks**: this repository has no submodules |
| `receipts/tool-identity.txt`, `scripts/run-r419-3.sh` | tools; every step in order | Two build logs had the local simulator install prefix replaced by `<PINNED_VERILATOR_PREFIX>`; nothing else was edited |

## 4. Prior public findings, resolved or retained at this head

| Finding | Status | Evidence at ee0e2b72 |
|---|---|---|
| **R419-2 F5** (MINOR; RTL, Robustness, Docs): a GET_STREAM_INFO inside GET_DYNAMIC_INFO is not serialized against an ACMP step on the same sink, and the comment said otherwise | **RESOLVED under the ruled option** (comment and docs only; serialization stays a #84 remainder) | The comment is true (`protocol_processor_top.sv:1464-1476`), 03 §6 records the limitation (`03_packet_engine.md:229-239`), and the PR body's #84 remainder names it. The probe reproduces exactly what both say (G0 waits; G1 admitted, key 0xFC00). The verification my round-2 report asked for is met |
| R419-2 S6 (08 §4 ACMP-wait wording) | taken | `08_timing.md:186-210` bounds never-preempted commands by their own watchdog-bounded program |
| R418-2 S1 (hold bound for LOCK_ENTITY and the map edits; MAP_CFG cross-lock listed) | taken | Same paragraph. Its numbers are checked in section 2.2 |
| R418-2 S2 ("540 payload bytes") | taken | DL8 label, campaign check name and 09 §8.3 row. The arm is still KILLED |
| R418-2 S3 (tracking issue for the `KL_aecp_notify` fan-out hold) | **retained, the manager's** (round-3 ruling: residue checklist at merge) | A search of the open issues finds no dedicated issue yet. The finding is recorded in 08 §4 and in "What remains" |
| R418-1 F1-F4 and R419-1 F1-F4 (round 1; resolved at round 2 per R419-2) | **still resolved** | The lane's non-comment RTL is unchanged since 44a6bb9 (section 2.3). Every arm tied to them is KILLED at its README count at this head (DL1, DL8-DL11, HZ2-HZ12, P20) |

## 5. Findings

No BLOCKER, MAJOR or MINOR finding.

**S1 - SUGGESTION - Docs - `docs/architecture/08_timing.md:197-206`: the never-preempted bound counts face waits, not the whole hold**
- Evidence:
  - "LOCK_ENTITY makes two registry-face waits, about 82 µs", and a mapping edit's 2N + 3 waits are "at most 528,384 clocks, about 5.3 ms". Both are exact as face-wait totals (section 2.2).
  - The ACMP transaction's wait, though, runs to the hold's release. That also covers the program's non-face ops, the response build and the TX hand-off: response memory under `KL_aecp_resp_buf`'s own watchdog, and `A_TXW` waiting on `txreq_ready_i`. Each of these is separately bounded.
- Impact: none on the conclusion (later than the 50 ms design budget, inside `T-ACMP-CMD`). A reader may take the face-wait figure for the whole hold.
- Suggested outcome: say "face waits of at most …, plus the program's own response build and hand-off".
- Verification: a read against `E_LOCKEN` and `E_AMADD` and the engine's `A_TXW` state.

**S2 - SUGGESTION - Docs, Robustness - `docs/architecture/03_packet_engine.md:229-239`, `protocol_processor_top.sv:1472-1476`, PR body "What remains" (#84): STREAM_OUTPUT records are not named**
- Evidence:
  - GET_DYNAMIC_INFO serves GET_STREAM_INFO records for STREAM_OUTPUT as well, and the whole batch takes the no-descriptor key (G1/G2: key 0xFC00).
  - A stand-alone GET_STREAM_INFO of STREAM_OUTPUT k is keyed by source k and serialized against talker steps (HZ10e, `tb/pp_top/sim_main.cpp:13445`). The same record inside a batch is not.
  - Those words come from the integrator's `gsi_data_i` (`protocol_processor_top.sv:3400-3407`). So whether a talker step changes one is integrator-defined, which is why this is not a finding.
- Impact: the later #84 item may be scoped to sinks only.
- Suggested outcome: one clause naming STREAM_OUTPUT records against the talker's steps beside the STREAM_INPUT sentence, or in the #84 remainder.
- Verification: a read against the classifier default and HZ10e.

## 6. Per-lens results at ee0e2b72ea10c83f983ec9e35878fb0193223ccb

- **Conformance: CLEAN.**
  - The F5 record cites the right clauses: IEEE 1722.1-2021 §7.4.76.1 (each record as an independent command) and Milan §5.4.2.10 (probing and ACMP status).
  - The READ_DESCRIPTOR statement now covers #82's §7.2.3, §7.2.6 and §7.2.32 overlays, and it holds.
  - No wire behaviour of this lane changed in rounds 3 and 3b. The lane's non-comment RTL is identical, and DL, TB, HZ, D3 and AX are all green at the head.
  - Closes #57 still rests on DL3, DL8, TB1, TB3 and TB4, re-run green. The Relates #81 and #84 remainders are exact.
- **RTL: CLEAN.**
  - The only lane RTL edits in rounds 3 and 3b are comments (+6/−1), and their statements are true against `gsi_owner_read`, `lstn_gsi_status_r` and `KL_aecp_dyn_state`'s single port.
  - Both merges carry every RTL line of both sides. The re-cut patch targets are correct. No port, parameter or RTL file change.
- **Robustness: CLEAN.**
  - The F5 gap is recorded where a maintainer will look, and it is bounded: a read-only snapshot inconsistency, with no state change.
  - Every 08 §4 hold bound checked is right (2 × 4,096; 2N + 3 with N ≤ 63; the watchdog masks after the first expiry).
  - S1 and S2 are wording only.
- **Tests: CLEAN.**
  - The whole `tb/pp_top` suite (8,901), `tb/ucpu` (427) and every focus section are green.
  - The lane's campaign: 55 of 55 KILLED, counts equal to the README. C5b's re-cut arms fail the identical checks main's originals fail.
  - Both campaigns are wired in the Makefile and CI. The F5 limitation is graded by HZ6 for the stand-alone getter, and the batch behaviour is pinned by my probe. The ruling required no new test.
- **Docs: CLEAN.**
  - 03 §6, 08 §4, 09 §8.3, both READMEs and the bench banners name four builds, with no stale "third build" for TB.
  - `make links matrix modmatrix params` and `gen_matrix.py --check` are rc 0.
  - The PR body equals the author-r3b packet and states the #84 remainder exactly.
  - S1 and S2 are optional.

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | top classifier banner `:1464-1476`; 03 §6 `:229-239`; `gen_ucode.py` #82 overlays `:1114-1180`; `KL_aecp_dyn_state` port; PR body #57/#81/#84 lines; DL/TB/HZ/AX run | R419-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |
| RTL | CLEAN | remerge-diffs of 97fe22f and ee0e2b7; `merge_side_check.py` (4 directions); non-comment RTL delta identity; top/engine/µCPU headers; `txs_oversize_o` `:2583-2585` and both re-cut patches | R419-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |
| Robustness | CLEAN | `ucpu_preempt_w` `:1749-1750`; `gather_watchdog` `:2373-2386` and hold masks `:2315-2328`; cdl gate `:3270-3273`; `E_LOCKEN`, `E_AMADD`; 08 §4 `:186-210`; GDI probe G0-G2 | R419-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |
| Tests | CLEAN | `tb/pp_top` four builds 8,901/0; `tb/ucpu` 427/427; `aecp_mutants.py` 5 + 55/55 with README equality; `ov-oversize-never`/`-at-576` at head and at main, identical lists; Makefile targets and CI steps | R419-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |
| Docs | CLEAN | 03 §6, 08 §4, 09 §8.3 DL8 row, `tb/pp_top`/`tb/ucpu` READMEs, bench and wrap banners, PR body vs the author-r3b packet; links/matrix/modmatrix/params/gen_matrix rc 0 | R419-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |

## 8. Real limits

- **Not run (out of scope):**
  - the full processor bank (`run_suites.sh`, 33 suites);
  - the other campaigns (C5b's other 33 arms, ACMP, D3, MAAP, ADP, SRP and the rest);
  - Yosys, the parent consumer set at milan-fpga dev 7f0927bb with #137's disposition line, the donor bank, act and hardware.
- **The author's figures are not independently re-measured** (33 suites and 1,018,843 checks; AECP-dispatch 35/35; ACMP 19/19; D3 83/83; MAAP 32/32; ADP 32/32; SRP 90/90; parent 16/16). The parts I re-measured agree with them:
  - `tb/pp_top`;
  - `tb/ucpu`;
  - the AECP campaign;
  - the two re-cut arms.
- **Hosted CI was in progress at my snapshot.** The four mutation-campaign steps were not yet executed, so there is no hosted proof of them at this head yet.
- **The evidence pin.** The pinned evidence commit `4fe37ada` predates round 3. The r3 and r3b packets were read at `cbba1828` on the same evidence branch.
- **No manager bank comment for ee0e2b72.** I found none on the PR or the issue, so the manager's static, builder and native banks at this head are taken from the assignment's statement, not from a public receipt.
- **No physical-calibration or hardware claim** is made or implied.
- **The specification PDFs are not in the tree.** Clauses were read through their in-tree quotations.

## 9. Pending manager duties

- Confirm that the hosted `suites` job at ee0e2b72 completes, including the "AECP deadline and hazard-class" and "AECP dispatch" campaign steps (runs 36928701582 and 36928699036).
- Publish or link the manager's bank receipts for ee0e2b72. At the merge turn, build the final current-dev candidate (source base 16ea10ac, live dev 7f0927bb) and run the donor bank and the parent consumer set with #137's `acmp_mutants.py` disposition line.
- R418-1 S4 / R418-2 S3: open the `KL_aecp_notify` fan-out tracking issue (residue checklist at merge).
- At pin adoption, apply #137's `DUT_READER_DISPOSITIONS` line, and #138's and #135's parent-visible lists, as the PR body records.
- Optionally ask for S1 and S2. Neither affects the verdict.

R419-3 FINISHED
