[R661] POSITIVE - exact head 2022d363fc622f6bbf4c312239fc3db741b4d29a

# R661-2: independent review of FPGA-gPTP PR #86 (issues #84 and #85)

- Exact head: `2022d363fc622f6bbf4c312239fc3db741b4d29a`, tree `249bdbe6209bbc7ec17a816c26823ad97bb6d748`.
- Base: main `43acfbcc`, which includes #82. The previously reviewed head was `53ac2e9d`.
- Round 2 adds three commits (`601b298a`, `31f7a627`, `2022d363`). They touch only comments, guides and one test-header comment. The RTL and all four ROM images are byte-identical to `53ac2e9d`.

## Verdict

**POSITIVE.**

- No BLOCKER, MAJOR or MINOR finding is open at this head.
- All four Round 1 MINOR/MAJOR findings and the Round 1 RESIDUE are resolved at their cause (see "Prior findings").
- One new RESIDUE (wording only) and five SUGGESTIONs are recorded below. None of them leaves a lens unclean.

## Scope reconstructed

I read these, in this order:

1. The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `docs/README.md` (truth order), `README.md`, `docs/MANAGER.md`, and the changed sections of the integration, HDL, test and source-evidence guides.
2. Issue #84 (frozen *Done when*):
   - tu is 0 while grandmaster;
   - the Annex B.1.1 0.25 s holdover on a grandmaster change stays;
   - a simulation case and a mutant;
   - parent consumer gates pass.
3. Issue #85 (frozen *Done when*):
   - when a slave port takes an Announce, the path is the received path plus thisClock (count + 1);
   - it stays consistent with the grandmaster at every #82 transition;
   - a direct and a multi-hop case, each with a mutant;
   - parent gates pass.
4. The manager's assignment (issuecomment-6257168490). Its item 5 is a STOP on any port or parameter change seen by the parent.
5. The author's STOP and the manager's STOP ruling (issuecomment-6259159680): land both issues, with a parent companion that cites the clause on each row.
6. The Round 2 assignment (issuecomment-6259958948).
7. The Round 2 ruling (issuecomment-6264025745):
   - it accepts `parent-adoption-milan_dp-82.patch`;
   - it accepts `parent-adoption-milan_dp_gptp-84.patch`, harness change included, and asks reviewers to grade that logic against IEEE 1722-2016 4.4.4.7 and 10.4 and Milan v1.2 4.3.5.2;
   - it accepts the surviving parent mutant `&& gm_r != 0` as redundant.
8. Interface authority:
   - parent `KL_ptp_clock_validity.sv` at `e9cbb676`: `ts_uncertain_o = ~sync_ok | hold | disc_p` (`:211`);
   - the hold is armed on a grandmaster-id change, a discontinuity pulse or a PHC step;
   - `milan_datapath.sv:2040` wires `fabric_sync_ok_i` to `pub_flags_o[3]`.

I did my own pass over `git diff 43acfbcc..2022d363` before reading the Round 1 review findings.

## Lens results

### Conformance: CLEAN

**#84: the grandmaster role counts as synchronised.**
- `prog_become` (`hdl/ucode/gen_gptp_ucode.py:1744`) sets sync-ok (bit 3) together with the master bit. So the parent's tu is `~bit3 | hold`, and it is 0 during mastership outside a holdover. This matches IEEE 1722-2016 4.4.4.7: tu marks a discontinuity, not the role.
- The Milan v1.2 Annex B.1.1 holdover is kept. The takeover from a peer changes the published grandmaster id in the same commit that sets sync-ok, and that change arms the parent's hold.
  - The engine test "#84 takeover: its commit names thisClock with sync-ok" pins that single-commit shape.
  - The accepted parent companion grades the hold itself: ≥ 0.25 s − 4 ms, and cleared within 0.5 s + 4 ms.
- From reset, or after a self publication, the published grandmaster is already thisClock. So mastership arms no new hold.
  - Reset's own first publication of thisClock already armed one (`parent-adoption-milan_dp-82.patch` header; CLKV "first publication of a real grandmaster id IS a change").
  - This is now stated exactly in the generator (`:1737-1743`), in the phase-37 header and in the PR text.
- Handing mastership to a peer clears sync-ok in the commit that names the new grandmaster (`:1665`, unchanged). The first consumed Sync pair sets it again.

**#85: received pathSequence plus thisClock.**
- Region 3 word 7 (`hdl/top/KL_gptp_engine.sv:716-730, 973-993`) publishes the received entries, then thisClock, with count + 1 (IEEE 802.1AS-2020 10.3.13.2.4 f) 5), 10.3.9.23).
- A directly attached grandmaster publishes [GM, thisClock]. An absent TLV stays at count 0.
- A present TLV always carries at least the grandmaster. The parser enforces N == stepsRemoved+1 with the GM at the head (`gen_gptp_ucode.py:63-69`), so "nonempty" and "present" coincide.
- Loop prevention (qualification rule (c), every declared hop) rejects a received pathSequence that already contains thisClock. So the append can never duplicate thisClock.
- Eight or more received entries publish the first eight, without thisClock. This is the eight-entry ABI bound, which the PR and the integration guide disclose (see S2).

**#82 transitions.** Every commit of the run naming a peer grandmaster with a path ends with thisClock exactly once (phase 38: 365 commits graded on each shipping pass, plus 48 on the priority1 255 pass). Reset, departures and Pdelay loss still publish {thisClock}.

**Graded parent harness logic (the Round 2 ruling asked for this).**
- In `parent-adoption-milan_dp_gptp-84.patch`:
  - `Until::Healthy` now also requires the peer's grandmaster id. This is necessary, because a self-grandmaster now also reads sync=1, tu=0.
  - `Until::PeerLost` keys on asCapable alone.
  - The loss window is split into: tu 1 until this station is grandmaster, then the holdover (not compared), then tu 0.
  - New checks grade the 0.25 s minimum and the 0.5 s maximum (HOLD_QTICK_P = 2 quarter-ticks), and that the station is grandmaster after the loss.
- This agrees with IEEE 1722-2016 4.4.4.7 and Milan v1.2 4.3.5.2 / Annex B.1.1, as read through the parent CLKV equation above.
- The extended mode does not compare tu across the whole window (see S3).

**Port and parameter contract.** No port or parameter change. The engine diff changes only the comments on `pub_path_count_o` and `pub_path_o`, plus internal wires. Parent `check_port_contracts.py` passes on the adoption snapshot (`07.log`). The meaning of the count changes, as #85 requires.

### RTL: CLEAN

- `path_append_w` is true for clamped counts 1..7. `path_trace_count_w` is at most 8 and fits 4 bits.
- Slot `pk` copies a received tail when `pk+2 <= n`, takes `rom_clock_id_w` when `pk+1 == n`, and is cleared otherwise.
  - So thisClock occupies 0-based entry `n`, and every inactive slot is zeroed on the same edge.
  - The existing single-edge stage and COMMIT atomicity is preserved.
- `rom_clock_id_w` is the image-constant thisClock (`:171`). It is the same source as the reset `pub_gm_r` and the S_CID equality assertion.
- The flags RMW in the Sync-receipt-timeout leg (`gen_gptp_ucode.py:2008-2013`) computes `flags & ((flags << 2) | 0x7)`:
  - every write to publish word 2 is an AND/OR with masks ≤ 0xF, or a zero store, and reset clears it, so bits 4..31 are always 0;
  - bit 0 shifts onto bit 2, which is already in the mask;
  - so the leg clears sync-ok exactly when the master bit is clear, as documented. It is branch-free, at +2 words.
- The `SYNCOK_BY_AMGM_C` assert (`:509`) ties the shift to the flag layout.
- The RTL flags hook (`KL_gptp_engine.sv:938-958`) is unaffected:
  - BECOME retires the slew on its PHC word 3 write before the flags write;
  - the falling-bit-2 timer expiry behaves as before.

### Robustness: CLEAN

- **Queued receipt timeout.** A Sync receipt timeout queued behind BECOME (the disarm cannot recall it) keeps sync-ok. The engine case stalls dispatch behind a Pdelay response until the 375 ms watch expires.
- **Pdelay loss during mastership.** All three Pdelay-driven asCapable-fall paths keep bit 3 (`:1494, :1543, :1978`).
- **My probes P1 and P2.** Each mis-shifts the new mask, so asCapable (shift 1) or gmPresent (shift 3) lands on sync-ok. Both are caught by 11 and 13 failing checks, including the slave receipt-timeout checks (`receipts/probe-summary.txt`). The new mask therefore cannot silently keep a slave's sync-ok.
- **Path boundaries.** 7 entries put thisClock in slot 8. 8 entries and longer clamped paths publish the first eight. Count 0 publishes no tail; the engine's own simulation assertion guards that.

### Tests: CLEAN

- **New engine cases:**
  - #84: first mastership, takeover with a queued timeout, every master cycle (108,614,414 graded), every handover (16);
  - #85: direct, four-bridge, 7, 8 and absent, plus every committed peer path;
  - #82 expectations updated to expect thisClock last.
- **Mutation arm:** 72/72 at head (base 58/58). It adds 7 arms for #84 and 9 for #85, and each must fail every check it names (author receipt `round2/lane-head-2022d363/engine-mutants/mut-summary.txt`: 24 slices, all rc 0).
- **My reproduction at the exact head with the pinned simulator 5.050:**
  - the engine suite gives 1703/1703 ×3 and 53/53 on the priority1 255 pass, matching the author;
  - `make contract lint docs diagrams-check` all rc 0;
  - all four tracked ROM images regenerate byte-identically: 1,015 of 1,024 words.
- **Parent evidence (author receipts, adoption snapshot `564466ea` = dev `e9cbb676` + gitlink `2022d363` + four companions):**
  - consumer gates 01-11 all rc 0;
  - gptp_shadow 310/310;
  - builder union of 103 gates, both legs rc 0;
  - milan_dp `gptp` and `gptp-lat` 185/185 each;
  - milan_dp_gptp harness 155/155 and four verifiers;
  - gm_steps 190/190 with 6/6 controls.
- **Companion apply check:** all four patches apply cleanly in order to clean `e9cbb676`, and the result is identical to the snapshot's tests. The patch hashes match the published files.
- **Parent mutants:** every new parent check has a planted defect. The one survivor (`&& gm_r != 0`) is accepted by the ruling and recorded in `author-r2/HANDOFF.md:132`.

### Docs: CLEAN (one RESIDUE)

- The ROM budget now reads 1,015/1,024 (99.1%), nine free (`docs/MANAGER.md:103,107`). That matches the generator for all four images. No other current page states a figure.
- The clause note (`gen_gptp_ucode.py:72-77`), the holdover wording (`:1737-1743`, `sim_main.cpp` phase 37) and the phase order (37 before 38) are corrected.
- The integration guide's new "Path of an elected peer" and "Grandmaster synchronization" sections are correct.
- The `SOURCE_EVIDENCE.md` anchors resolve (`make docs`: 20 exact, 0 findings). For example, `gen_gptp_ucode.py#L896` is `prog_leg_slew`.
- **Comment rule:** the reviewed delta's source comments carry no lane labels, lane names, round or reviewer IDs, or comment IDs. `B1..B3` in `sim_main.cpp` are bridge-identity constants, not labels.
- One wording residue is recorded as R661-2-R1.

## Findings

### R661-2-R1 - RESIDUE - Docs

- **Location:** `docs/INTEGRATION.md:296-302`.
- **Defect:** the list "These events clear the synchronization verdict and keep the lock:" still names "A 375 ms Sync receipt timeout." (line 299) without qualification. Since #84, a timeout that reaches a master does not clear it. `docs/INTEGRATION.md:546` states the correct rule.
- **Authority:** `gen_gptp_ucode.py:2008-2013`, and the engine check "#84 takeover: a queued receipt timeout keeps sync-ok".
- **Impact:** prose only. It changes no figure, test, code or clause claim, and the correct rule is stated in the same guide.
- **Exact fix:** replace line 299 with `- A 375 ms Sync receipt timeout outside mastership.`
- **Verification:** reread the list, then run `make docs`.

### R661-2-S1 - SUGGESTION - Conformance, Docs

- **Topic:** a master that is not grandmaster-capable also claims sync-ok.
- **Behaviour:**
  - with priority1 255, gmPresent stays clear, but mastership still sets bit 3, so the parent's tu reads 0;
  - the priority1 255 pass grades this deliberately ("p1 255 #84 every master cycle publishes sync-ok");
  - the parent builder passes the configured priority1 to the generator.
- **Why it matters:** issue #84 is framed as "while the instance is the gPTP grandmaster". With gmPresent clear, IEEE 802.1AS-2020 10.3.13.2.4 g) reports that no grandmaster is present.
- **Suggestion:**
  - the owner confirms that tu = 0 is intended for a non-grandmaster-capable master;
  - the integration guide's "Grandmaster synchronization" section (`docs/INTEGRATION.md:536-560`) states the gmPresent-clear case either way.
- I found no authority text that makes the current choice a defect, so this is not graded as one.

### R661-2-S2 - SUGGESTION - Conformance, Docs

- **Topic:** a received path of eight or more entries publishes its first eight entries without thisClock.
- **Background:** the ABI bound is disclosed (`docs/INTEGRATION.md:482-486`, PR text), and widening it would be a port change.
- **Suggestion:** track it as an explicit parent-visible limitation, for example on the parent's GET_AS_PATH page, so a 9+ entry GET_AS_PATH response is not read as a #85 regression.

### R661-2-S3 - SUGGESTION - Tests

- **Topic:** the parent companion `parent-adoption-milan_dp_gptp-84.patch`, extended mode (`make extended`).
- **Current state:** extended mode marks the whole 4.6 s peer-loss window as not compared (`tu = -1`). Only the default mode grades the three-window split.
- **Suggestion:** when that harness is next touched, grade at least the tu-1 segment before the grandmaster change in extended mode too.

### R661-2-S4 - SUGGESTION - Tests

- **Origin:** carried from R661-1-S1, unchanged by the Round 2 delta.
- **Gap:** an out-of-threshold Pdelay verdict during mastership (the `gen_gptp_ucode.py:1968-1978` path) is not exercised by a master-side case.
- **Suggestion:** add one, so that all three asCapable-fall paths are graded for "#84 every master cycle publishes sync-ok".

### R661-2-S5 - SUGGESTION - RTL, Docs

- **Topic:** the out-of-context resource snapshot in `docs/MANAGER.md` (main `5dce647a`) predates the per-slot thisClock mux this PR adds.
- **Suggestion:** record the engine delta at the next out-of-context measurement.
- No timing risk is expected: the mux input is an image constant.

## Prior findings at this head

| Finding | Round 1 class | Status at `2022d363` | Evidence |
|---|---|---|---|
| R661-1-F1 (parent companion incomplete) | MAJOR | **Resolved** | `parent-adoption-milan_dp-85.patch` covers the eight milan_dp `sim_gptp.cpp` rows and the physical-leg rows. There is a whole-parent search (`round2/search/path-shape-search.md`) and a suite inventory. milan_dp gptp/gptp-lat pass 185/185 and milan_dp_gptp 155/155 on snapshot `564466ea`. |
| R662-1-F01 / R661-1-F2 (ROM budget stale) | MINOR | **Resolved** | `docs/MANAGER.md:103,107` now reads 1,015 (99.1%), nine free. My regeneration agrees for all four images, and the "88 percent" comment no longer carries a number. |
| R661-1-F3 (holdover overgeneralised) | MINOR | **Resolved** | The generator (`:1737-1743`), the phase-37 header and the PR text now say the holdover arms only when a peer grandmaster is replaced. |
| R661-1-F4 (stale clause note) | MINOR | **Resolved** | `gen_gptp_ucode.py:72-77` |
| R661-1-R1 (phase order) | RESIDUE | **Resolved** | Phase 37 now precedes phase 38 in the header. |
| R661-1-S1 (master-side bad-delay case) | SUGGESTION | Retained as R661-2-S4 | Not required |

## Executions (this review)

All runs used disposable copies of the exact head under `scratch/`. The pinned simulator identity was verified as 5.050. Builds ran concurrently under one foreground driver.

| Run | Result | Receipt |
|---|---|---|
| Engine suite (`make -C tb/verilator/engine run`, four passes) | rc 0; 1703/1703 ×3, 53/53 | `receipts/head-engine.log`, `.rc` |
| P1: timeout leg shifts flags by 1 (asCapable → sync-ok) | caught, rc 2, 11 FAIL | `receipts/p1-engine.log` |
| P2: timeout leg shifts flags by 3 (gmPresent → sync-ok) | caught, rc 2, 13 FAIL | `receipts/p2-engine.log` |
| Four ROM images regenerated | all byte-identical; 1,015 words | `receipts/images.log` |
| `make contract`, `lint`, `docs`, `diagrams-check` | all rc 0 | `receipts/make-*.log`, `make-gates.rc` |
| Published evidence `kebag-logic/milan-fpga@c3f1d08d:review-evidence/gptp84-r1` | MANIFEST.json 822/822 digests match, 0 unlisted, 0 redacted outside `reviews/`. `author-r2/receipts/INDEX.md` 414/414 rows match the files present. | `receipts/evidence-verify.txt` |
| Review clone restored and verified | HEAD, tree, index modes and blobs, on-disk bytes all equal the head; no untracked or ignored files; no gitlinks in this repository | `receipts/clone-integrity.txt` |

The scripts are `scripts/probes.sh` and `scripts/verify_evidence.py`. Host paths in the receipts are replaced by placeholders.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `gen_gptp_ucode.py` (`prog_become`, `prog_leg_resume`, `prog_btca` stage, qualification notes); `KL_gptp_engine.sv:700-730, 960-993`; parent CLKV and datapath wiring at `e9cbb676`; the four companion patches and the #84 harness logic | R661-2 | 2022d363fc622f6bbf4c312239fc3db741b4d29a |
| RTL | CLEAN | `KL_gptp_engine.sv` append and count logic, flags hook; flags-word bit inventory; port list diff | R661-2 | 2022d363fc622f6bbf4c312239fc3db741b4d29a |
| Robustness | CLEAN | Queued-timeout ordering, Pdelay-loss paths during mastership, path boundaries 0/1/5/7/8/9+, probes P1 and P2 | R661-2 | 2022d363fc622f6bbf4c312239fc3db741b4d29a |
| Tests | CLEAN | `sim_main.cpp` phases 8n, 19, 37, 38 and the updated #82 rows; `mutants.py` (16 new arms); my engine run; author head and parent receipts; companion apply check | R661-2 | 2022d363fc622f6bbf4c312239fc3db741b4d29a |
| Docs | CLEAN (R661-2-R1 RESIDUE) | `docs/MANAGER.md`, `INTEGRATION.md`, `HDL_DEVELOPER.md`, `TEST_DEVELOPER.md`, `SOURCE_EVIDENCE.md`; source comments in the delta; PR body | R661-2 | 2022d363fc622f6bbf4c312239fc3db741b4d29a |

## Real limits

- **Parent results come from author receipts.** I did not re-execute any parent suite (a full parent bank is out of scope). The parent results above are the author's published receipts, verified by digest and index, not by my execution.
- **No manager source bank** exists at this head, and none is claimed.
- **The evidence commit `c3f1d08d` carries no cryptographic signature.** Its integrity rests on the MANIFEST.json and INDEX.md digests, which I verified.
- **No hosted jobs ran.** At the exact head, the hosted check-run API reports 0 check runs and a pending combined status with 0 contexts. No hosted execution is inferred.
- **tsn_fuzz was not exercised.** Its field campaigns were SUITE-SKIP in the author's runs, because the external generator was absent.
- **Builder gate 11** is NOT RUN in both legs: the calibration build tree is absent. That matches the base verdict digest.
- **No physical evidence.** Physical calibration and hardware acceptance were NOT RUN, and field skips are not hardware proof.
- **Standards text.** Clause readings rely on the issue-cited clauses and on in-repository and parent clause notes. The standards text itself was not available in this environment.

## Pending manager duties

- Build and validate the current-dev merge candidate: source base `43acfbcc`, live dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. That means the builder and native banks, plus hosted/act acceptance at the merge turn.
- Land the four parent companions with the next gptp-processor pin adoption in milan-fpga, in the handoff order: gptp_shadow-85, milan_dp-85, milan_dp-82, milan_dp_gptp-84.
- Widen the parent consumer list, as the author's suite inventory records: milan_dp `gptp`/`gptp-lat`, milan_dp_gptp, milan_dp_gm_steps, gptp_plane, gptp_tables, gptp_txts, tsn_fuzz.
- Carry R661-2-R1 to the residue checklist.
- Rule on S1: is a non-grandmaster-capable master synchronised?

R661-2 FINISHED
