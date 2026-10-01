[R418] POSITIVE - exact head ee0e2b72ea10c83f983ec9e35878fb0193223ccb

# R418-3: internal independent review of PR #140, round 3 (rounds 3 and 3b), lane C5a (issues #81 / #57 / #84)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #140, branch `c5a-aecp-deadlines`.
- Exact head `ee0e2b72ea10c83f983ec9e35878fb0193223ccb`, tree `3eb7d8ec80192da62a2c2c3966628782c5d93854`, verified in the
  reviewer's own detached clone (`receipts/clone_integrity.txt`).
- Delta judged: from my round-2 head `44a6bb90` (R418-2 POSITIVE) to this head. That is four commits:
  - `97fe22f`, the merge of main `3f3ea56b` (#135, #137);
  - `e4c70b5`, the R419-2 F5 ruling;
  - `d4ca85c`, the 08 §4 hold bounds and the DL8 label;
  - `ee0e2b7`, the merge of main `16ea10ac` (#138, lane C5b).
- Assignments: issue #81 comments 5929634478 (round 3) and 5936567141 (round 3b).
- Review start: PR #140 comment 5940966539.
- Verdict: **POSITIVE**. There is no open BLOCKER, MAJOR or MINOR finding. One SUGGESTION (S1) is recorded below, and it does
  not affect any lens.
- The verdict and ledger were written to this file before any prior review finding was read. Section 5 was added after
  that.

## 1. Reconstruction, in the prescribed order

1. **AGENTS.md / CONTRIBUTING.md.** Neither is tracked in this repository at the head (`git ls-files` finds none). The
   conventions came from the top-level `README.md` and `docs/README.md`: single-source rules, the ID registries, the
   citation style, and `make check` as the documentation gate.
2. **Issue #81.** The frozen acceptance is in the body (items 1-4). The manager comments were read:
   - the lane opening, 5915626788;
   - round 2, 5923634905;
   - round 3, 5929634478: the F5 ruling (option one, comment and docs only, #84 remainder), merge `3f3ea56b`, suggestions
     R418-2 S1/S2 and R419-2 S6, and S3 as the manager's;
   - round 3b, 5936567141: merge `16ea10ac` with `--no-ff`, keep both sides, keep both campaign drivers, re-measure.
   - No port, parameter or parent-visible change is allowed without a STOP.
3. **Authorities.** 03 §6 F03.7 (RO_SNAPSHOT "blocked only vs in-flight write on the same key", rule 5 the MAP_CFG
   cross-lock), 08 §4, 06 §8.1, and F01.5 (`P-CLK-HZ` 100 MHz). The specification clauses are cited as the tree cites
   them: IEEE 1722.1-2021 §7.4.76.1/.2 (GET_DYNAMIC_INFO records as independent commands), §7.2.3/§7.2.32/§7.2.6, and
   Milan v1.2 §5.4.2.10, §5.4.1 and §5.4.3.3 Table 5.19. The specification PDFs are not distributed, so I checked these
   as the tree's citations against the RTL behaviour, not against the PDF text.
4. **Diff and history.**
   - `git diff 16ea10ac..ee0e2b72` and first-parent history.
   - Both merges were re-run as trial merges (`git merge-tree --write-tree`) and the trial trees compared with the
     committed merges (section 2).
5. **Public executable evidence.**
   - The pinned evidence commit `kebag-logic/milan-fpga@4fe37ada` carries only `author`, `author-r2` and the round-1
     reviews under `review-evidence/ppC5a-r1/`.
   - The assigned `author-r3` and `author-r3b` packets exist on the public branch `ppC5a-review-evidence` at `cbba1828`.
     They were read there (HANDOFF.md, PR-BODY.md, the #137 disposition patch).
   - `author-r3b/PR-BODY.md` equals the live PR body apart from one trailing newline.
   - Manager evidence comment read: PR #140 5921897578 (banks at `f963fe9a`). No manager evidence comment exists yet at
     this head.

## 2. Independent pass over the delta

### 2.1 Merge `97fe22f` (main `3f3ea56b`: #135, #137)

- **Trial merge.** `git merge-tree 44a6bb9 3f3ea56` conflicts in exactly `tb/pp_top/Makefile` and
  `tb/pp_top/sim_main.cpp`. The committed merge differs from the trial tree only at those two conflicts:
  - `.PHONY` carries `maap-internal` beside `deadline d3 hazards budget budget-build aecp-mutants`;
  - `one_section` is the union of every flag of both sides, and `run_maap_internal` is kept.
- **Line accounting** (`both_sides_kept.py`, `deleted_not_resurrected.py`; receipts `merge3_both_sides.txt`,
  `merge3_deleted.txt`):
  - every line either side added is in the merge, except the two conflict lines, which are each replaced by their union;
  - no line either side deleted is resurrected.

### 2.2 Commit `e4c70b5` (R419-2 F5, as ruled)

- **The classifier banner** (`hdl/top/protocol_processor_top.sv:1463-1477` at the head) now says three things, all true:
  - READ_DESCRIPTOR loses nothing by the NONE key;
  - GET_DYNAMIC_INFO does, a known gap;
  - its GET_STREAM_INFO records of a STREAM_INPUT read `lstn_gsi_status_r`.
- **The writer of that record.** `lstn_gsi_status_r` is written only at `:3360`, by the listener record write
  (`lstn_recwr_sink_w`), and read for GET_STREAM_INFO at `:3396`.
- **03 §6** (`docs/architecture/03_packet_engine.md:229-240`) records the limitation:
  - beside the no-descriptor-key sentence;
  - with IEEE §7.4.76.1 and Milan §5.4.2.10;
  - with the HZ6 contrast. HZ6 at `tb/pp_top/sim_main.cpp:13335-13341` is ACMP message 8, UNBIND_RX, against
    GET_STREAM_INFO STREAM_INPUT 1, and message 10, GET_RX_STATE, as the two-read control;
  - with "left to a later issue #84 item".
- **The PR body's "What remains"** names it under #84, which stays "Relates to".

### 2.3 Commit `d4ca85c` (R418-2 S1/S2, R419-2 S6)

The 08 §4 paragraph (`docs/architecture/08_timing.md:187-210`) was checked against the RTL.

- **Holds listed.** It lists the barrier, LOCK_ENTITY, the MAP_CFG class-wide cross-lock and the same-stream-key command
  (F03.7 rule 5).
- **Never preempted.** `ucpu_preempt_w` (`hdl/aecp/KL_aecp_engine.sv:1749-1750`) excludes `regun_r`, `lockc_r` and
  `amap_edit_r`.
- **Watchdog.**
  - The shared gather watchdog (`:2373-2386`) bounds the `rgy_hold_w` and `amap_edit_hold_w` waits at
    `MEM_TIMEOUT_CYC_P`.
  - The top binds that to `DESC_MEM_TMO_CYC_P` (`protocol_processor_top.sv:3671`), whose default is 4,096 (`:133`).
- **LOCK_ENTITY.**
  - `E_LOCKEN` (`hdl/aecp/ucode/gen_ucode.py:1062`) makes exactly two GATHER_EXT on the registry face.
  - 2 × 4,096 = 8,192 clocks, which is 81.9 µs at 100 MHz.
- **Mapping edit.**
  - `E_AMADD` (`gen_ucode.py:1997`) makes 1 begin, N validates, 1 commit-begin, N commits and 1 finish, so 2N + 3 waits.
    The abort path makes N + 2 or fewer.
  - The engine refuses `cdl != 20 + 8N` or `cdl > 524` before dispatch (`KL_aecp_engine.sv:3270-3275`), so N ≤ 63.
  - 129 × 4,096 = 528,384 clocks, which is 5.28 ms.
- **No unbounded stall.** I checked the µCPU stall sources (`KL_aecp_ucpu.sv:327-356`): `SEND_RESP`'s `tx_ready_i` is
  tied to 1 at the engine (`KL_aecp_engine.sv:1802`), and the response-buffer stall has its own watchdog. Neither
  program waits outside a watchdog.
- **S1 below** is one precision point: the figures count face waits only.
- **DL8 label.** It is renamed in the bench, the campaign's named check and the 09 §8.3 row. `mvu-echo-slot-std` still
  kills on it (1 failing check).

### 2.4 Merge `ee0e2b7` (main `16ea10ac`: #138, C5b)

- **Trial merge.** `git merge-tree d4ca85c 16ea10a` conflicts in exactly the eight files the assignment names:
  - `.gitattributes`, `hdl.yml`;
  - `tb/pp_top/{Makefile, README.md, pp_top_wrap.sv, sim_main.cpp}`;
  - `tb/ucpu/{README.md, sim_main.cpp}`.
- **Edits outside the textual conflicts** (trial tree against the committed merge, `git diff 3d55137 ee0e2b7`): the three
  semantic edits the PR body declares (the two patches; the READ_DESCRIPTOR wording in 03 §6 and the banner; "fourth
  build" in 08 §4, 09 §8.3 and `aecp_mutants.py`), and nothing else. The merge resolution changes no RTL logic.
- **Line accounting at the head** (receipts `merge3b_both_sides.txt`, `merge3b_deleted.txt`, `union_0451_vs_head.txt`):
  - Every line #135-#138 added in their 100 files is present at the head, except reworded or unioned lines.
  - The same holds for this lane's 103 files.
  - I read each shortfall line by hand. Each one is "three builds" becoming "four builds", a flag list or `.PHONY` union,
    a count re-measure (`tb/ucpu` 415 and 398 become 427), the `load_descriptor_image` signature union, or the re-cut
    patch.
  - No deleted line is resurrected.
- **Four builds.**
  - The Makefile has default, DV fixture, C5b's line build (AX, `LINE_FIXTURE` 584) and this lane's timebase build (TB).
  - The tally awk requires `NR == 4`. `clean` removes `obj_line` and `obj_tim`.
  - Every target of both sides is in `.PHONY`.
  - Both campaign targets and both output variables are kept.
- **sim_main `main()`.** Compared with both parents, the section set is the union:
  - DV, AX and TB are each alone in their build;
  - the default build runs Suite, GSI, NW, D3, AC, AD, AX, DL and HZ;
  - every focus flag is kept: `--aecp-dispatch-only`, `--deadline-only`, `--hazards-only`, `--acmp-only`,
    `--maap-internal-only`, `--adp-only`, `--d3-only`, `--name-writes-only`, `--gsi-internal-only`, `--dr3a`.
  - `load_descriptor_image(entity_cfg, extra_ents, extra_bodies, sigmux_len)` serves C5b's appended rows (`:11278`) and
    TB's 576-byte SIGNAL_MULTIPLEXER (`:12515`).
- **Wrap.** Both define-driven overrides are kept: `PP_TOP_DESC_LINE_BYTES` (`:513-516`) and `PP_TOP_TIM_REAL`
  (`:469-479`). Both tap groups are kept (`dbg_sb_barrier_o` `:452`, `:826`).
- **Both campaigns.**
  - `aecp_mutants.py`'s arm table is byte-identical at `44a6bb9`, `d4ca85c` and the head (55 arms, 42 patches).
  - `aecp_dispatch_mutants.py`'s table is identical at `16ea10a` and the head (35 arms, 35 patches).
  - CI runs both steps (`hdl.yml`). `.gitattributes` exempts both patch directories.
  - Both READMEs carry both tables. The `tb/pp_top` build table has four rows.
- **The two re-cut C5b patches.**
  - Main's originals no longer apply at the head (`receipts/orig_patches_at_head.txt`). This lane's `txs_oversize_o`
    (`KL_aecp_engine.sv:2583-2585`) gained the MVU-echo term.
  - The re-cuts plant the same defect: `ov-oversize-never` forces the whole request to 0, and `ov-oversize-at-576` uses
    `>=` on the frame-length term with the echo term kept.
  - Executed: the original patches on main's own tree and the re-cut patches at the head print **identical failing-check
    sets** (18 and 4; `recut_vs_main_*.diff` are empty).
  - All 77 patches of both campaigns apply at the head (`all_patches_apply_at_head.txt`).
- **The widened READ_DESCRIPTOR statement** (#82's overlays: sampling rate, clock source, stream format).
  - `KL_aecp_dyn_state` has one state port, instantiated once, inside `KL_aecp_engine` (`:1915-1930`).
  - Its request mux is the µCPU's or the D3 writer's (`:1603-1604`), both inside the engine.
  - No ACMP module reaches it.
  - The statement "rows only the AECP engine writes" is true.
- **Ports and parameters.**
  - The top's module header (parameters and ports) is byte-identical to main `16ea10a`.
  - With comments stripped it equals `0451d83` and `d4ca85c`: main changed two parameter comments.
- **#82 / C5b interaction with the deadline kill.** C5b's µCPU change is an APPEND cap and a COPY_BUF tail count
  (`git diff 3f3ea56 16ea10a -- hdl/aecp/KL_aecp_ucpu.sv`). It adds no stall source and no effect op. The preempt's
  "first effect" rule and the watchdog list are unchanged. Both campaigns kill fully at the head (section 3).
- **`tb/ucpu` resolution.**
  - `disp_batch_i = batch || batch_base >= 0`, and the response base comes from `batch_base`, otherwise 12.
  - Both sides' dispatch paths are kept. Measured: 427.

## 3. Executed evidence (this reviewer, exact head, scratch exports only)

Every build ran in a `git archive` export under `scratch/`. The tracked bytes of the export were verified equal to the
head before and after (`export_trees_vs_rev.txt`; the F5 copy differs only by the probe's planted arms). The tool was
Verilator 5.050 rev v5.050 (`verilator_identity.txt`), with at most 8 CPUs (`taskset -c 0-7`) and every command in the
foreground. Reproduction: `run-r418-3.sh`.

| Step | rc | Result | Receipt |
|---|---|---|---|
| `make -C tb/pp_top run` (four builds) | 0 | 8,901 / 8,901: default 8,607, fixture 20, line 218, timebase 56; sections AX 218, DL 64, HZ 176, TB 56, ACMP 43, D3 133, NW 85, AD 55 | `pp_top_make_run.log` |
| `make -C tb/ucpu run` | 0 | 427 / 427 | `ucpu_run.log` |
| `./scripts/lint_hdl.sh` | 0 | LINT OK, every module | `lint_hdl.log` |
| `make check` | 0 | wavedrom 18, links 1,017, 115 REQ / 17 GAP, matrix 94 rows 0 untested, parameters 26 | `make_check.log` |
| `scripts/gen_matrix.py --check`, `check_upc_map.py`, `check_m9_opcodes.py --selftest` and plain | 0 | 94 rows / 59 constants, 87 entry points / 9 of 9 / 30 opcodes | `gen_matrix.log`, `upc_map.log`, `m9*.log` |
| `aecp_mutants.py`, all 55 arms in 4 chunks | 0 | every control PASS (d3, deadline, budget, hazards, ucpu); **55 / 55 KILLED** | `lane_campaign_chunk1-4.log` |
| `aecp_dispatch_mutants.py`, all 35 arms in 2 chunks | 0 | 3 controls PASS (aecp-dispatch, aecp-line, line-guards); **35 / 35 KILLED** | `dispatch_campaign_chunk1-2.log` |
| every arm's failing count against its `tb/pp_top/README.md` cell | 0 | 90 arms, 0 mismatches (shared rows expanded) | `readme_counts_vs_run.txt` |
| re-cut arms against main's originals on main's tree | 0 | identical failing-check sets, 18 and 4 | `dispatch_main16_arms.log`, `recut_vs_main_*.diff`, `*.fails` |
| `probe_gdi_stream_info.py` (R419-2's, unchanged; sha256 in MANIFEST) on a head export | 0 | **G0** stand-alone GET_STREAM_INFO SI 1 vs a held UNBIND_RX of sink 1: WAITED, refused 498 clocks. **G1** GET_DYNAMIC_INFO{GET_STREAM_INFO SI 1}: ADMITTED BESIDE, class 0, key 0xFC00, refused 0. **G2** the same beside a held GET_RX_STATE: admitted. HZ 179 / 0 | `probe_gdi_stream_info_head.log` |
| merge accounting (both merges) | — | as in section 2 | `merge3*_both_sides.txt`, `merge3*_deleted.txt`, `union_0451_vs_head.txt`, `campaign_tables.txt` |

**Not run, by rule:** the full `run_suites.sh` sweep (33 suites, 1,018,843 checks), the other processor campaigns (ACMP
19/19, D3 83/83, MAAP 32/32, ADP 32/32, SRP 90/90 and the rest), Yosys, and the parent consumer bank. The author records
them rc 0 at this head (author-r3b HANDOFF), and the manager's source banks are recorded as passed. This review's
coverage of them is the static evidence that the merge changes none of their inputs beyond `tb/pp_top`. The MAAP, ACMP,
ADP and D3 arms that run on `tb/pp_top` sections are exercised by the default build above.

## 4. Findings of this round

No BLOCKER, MAJOR or MINOR finding.

**S1 - SUGGESTION - Docs - `docs/architecture/08_timing.md:198-206`: the never-preempted hold figures count face waits
only**

- **Evidence.**
  - The figures (about 82 µs for LOCK_ENTITY; 528,384 clocks, about 5.3 ms, for a mapping edit) are the sum of
    watchdog-bounded face waits. I reproduced them from `E_LOCKEN`, `E_AMADD`, the gather watchdog and the cdl refusal
    (section 2.3).
  - The hold also includes:
    - the µprogram's own cycles;
    - the response hand-off after END: response-memory writes under that memory's watchdog, and TX-slot allocation.
  - The AECP key is released only at the response's hand-off.
  - The text says "bounds each face wait in it", which is accurate. A reader could still take "about 5.3 ms" as the
    whole hold.
- **Impact.** None on the conclusion. The extra terms are bounded and small against `T-ACMP-CMD`, so the ACMP answer is
  still inside it.
- **Suggested change.** Add "the face waits alone; the response hand-off after END adds its own bounded time".
- **Verification.** Read the paragraph against `KL_aecp_engine.sv` A_ALLOC/A_WR/A_TXW and `dl_queued_o`.

## 5. Prior public findings on this PR, resolved or retained at this head

These were read after the verdict and ledger above were written.

| Finding | Status at ee0e2b72 | Evidence |
|---|---|---|
| R418-1 F1 / R419-1 F1 (MAJOR): reachable NAME_WR conflict, false four-class statement | **RESOLVED, still holds** | Resolved at `44a6bb9` per R418-2 and R419-2. No classifier, scoreboard or HZ logic changed since. Only the banner comment changed in `hdl/top` (`git diff 3d55137 ee0e2b7 -- hdl`). HZ is 176/0 in the default build. All HZ arms are KILLED with README counts (`hz-name-*` 7, `hz-talker-keyed-as-listener` 18, and the rest) |
| R418-1 F2 (MINOR): status 10 for deadline-killed non-AEM types | **RESOLVED, still holds** | `st_echo_w` is unchanged. DL 64/0. `dl-non-aem-forced-status-10` KILLED (4) |
| R419-1 F2 (MINOR): two surviving kill-seam mutants | **RESOLVED, still holds** | `dl-registry-preempted` (2), `dl-lock-preempted` (2), `dl-kill-ack-keeps-owner` (2) KILLED at the head |
| R418-1 F3 / R419-1 F3 (MINOR): REQ-MVU-005 fault path | **RESOLVED, still holds; Closes #57 stays justified** | `mvu-fault-status-10` (4) and `mvu-echo-slot-std` (1) KILLED. The echo term of `txs_oversize_o` survives the merge (`:2583-2585`) |
| R418-1 F4 / R419-1 F4 (MINOR): check IDs, HZ banner | **RESOLVED, still holds** | Every campaign arm printed at least one named FAIL line: `named=1` for all but three `m9-guard` arms (set-stream-format, set-stream-info, set-name), which print `named=2` because two lines share their prefix |
| **R419-2 F5** (MINOR): GET_STREAM_INFO inside GET_DYNAMIC_INFO not serialized against an ACMP step on the same sink | **RESOLVED under the ruled option** (comment and docs, #84 remainder) | The banner is true (section 2.2). 03 §6 records the limitation with §7.4.76.1, Milan §5.4.2.10 and HZ6. The PR's #84 remainder names it. The probe re-run gives G0 waits, G1 admitted. The RTL gap remains by ruling, tracked as #84's remainder |
| R418-2 S1 (08 §4 hold bound, cross-lock listed) | **taken** | Section 2.3. One precision point is S1 of this round (SUGGESTION) |
| R418-2 S2 (DL8 "540 payload bytes") | **taken** | Bench label, campaign named check and 09 §8.3 row. The arm is KILLED |
| R418-2 S3 (`KL_aecp_notify` tracking issue) | **retained, manager's by ruling** | No tracking issue exists yet (issue search: none). The PR's "What remains" names it for the residue checklist at merge |
| R419-2 S6 (08 §4 ACMP-wait wording) | **taken** | The "never preempted ... rest of their own program" bullet |
| R419-1 S1-S3, R418-1 S1-S4 | as R418-2 and R419-2 recorded; unchanged | No text or arm they rest on changed in the delta, apart from the 08 §4 paragraph above |

## 6. Per-lens results

- **Conformance: CLEAN.**
  - Ruled F5 outcome: F03.7's RO_SNAPSHOT rule against IEEE §7.4.76.1 and Milan §5.4.2.10, recorded as a limitation
    rather than claimed conformant.
  - READ_DESCRIPTOR's NONE key loses no F03.7 conflict, including #82's overlays (single state port).
  - The REQ-MVU-005 echo slot survives the merge (Milan §5.4.1, Table 5.19).
  - Closes #57, Relates #81 (acceptance 4 open) and Relates #84 (REGISTRY_OP, acceptance 4, the GDI record) are exact.
  - Artifacts: `protocol_processor_top.sv:1463-1477, 3347-3396`, `KL_aecp_dyn_state` instance, 03 §6, the PR body's
    "What remains".
- **RTL: CLEAN.**
  - No RTL logic change in the delta beyond main's. The top header is byte-identical to main's.
  - The merged `txs_oversize_o`, `ucpu_preempt_w` and gather watchdog were read.
  - C5b's µCPU change adds no stall source.
  - Lint passes.
  - Artifacts: `KL_aecp_engine.sv:1749-1750, 1802, 2373-2386, 2583-2585, 3270-3275`, `KL_aecp_ucpu.sv` diff.
- **Robustness: CLEAN.**
  - Every hold an ACMP transaction meets has a stated bound. I reproduced the bounds from microcode and watchdog (S1 is
    precision only).
  - The deadline kill is intact across the merge: DL 64/0, and the 55 arms are killed.
  - No new unbounded wait.
- **Tests: CLEAN.**
  - `tb/pp_top` 8,901 over four builds, `tb/ucpu` 427.
  - Both campaigns ran in full: 55/55 and 35/35, all controls pass, 90 counts equal their README cells.
  - The re-cut arms are proven equivalent to main's originals by identical failure sets.
  - No check lost: the measured 8,607 default checks equal 8,212 (lane) + 8,367 (main) − 7,972 (base). Those three
    per-side defaults come from the recorded totals (8,288, 8,605 and 7,992), minus their fixture, line and timebase
    builds. I did not measure them here.
- **Docs: CLEAN.**
  - 03 §6, 08 §4 and 09 §8.3 are consistent with the RTL. No stale "third build" for TB remains (repository grep).
  - The `tb/pp_top` README has a build table of four rows and both mutation tables. The `tb/ucpu` README says 427.
  - `make check` passes.
  - S1 is a SUGGESTION.

## 7. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | classifier banner and `lstn_gsi_status_r` (`protocol_processor_top.sv`), 03 §6 F03.7 text, `KL_aecp_dyn_state` write path, the PR body's Closes/Relates and "What remains", F5 probe G0/G1/G2 | R418-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |
| RTL | CLEAN | trial merge against the committed merge for `hdl/`, top header byte compare, `KL_aecp_engine.sv` preempt/watchdog/oversize/cdl gate, `KL_aecp_ucpu.sv` C5b diff, `lint_hdl.sh` | R418-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |
| Robustness | CLEAN | 08 §4 bounds re-derived from `E_LOCKEN`/`E_AMADD` and the watchdog, µCPU stall sources, DL section and the deadline arms | R418-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |
| Tests | CLEAN | `tb/pp_top` four builds (8,901), `tb/ucpu` (427), both AECP campaigns in full (55/55, 35/35), README count cross-check (90/90), re-cut equivalence run, merge line accounting | R418-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |
| Docs | CLEAN | 03 §6, 08 §4, 09 §8.3, `tb/pp_top/README.md`, `tb/ucpu/README.md`, Makefile banner, wrap banner, `make check`, stale-wording grep; S1 SUGGESTION | R418-3 | ee0e2b72ea10c83f983ec9e35878fb0193223ccb |

## 8. Real limits

- Not run, by rule: the full `run_suites.sh` sweep, the non-AECP campaigns, Yosys, builder, the parent consumer set, hosted
  CI and act. Their results are the author's and the manager's. Section 3 records what this review covers instead.
- Hosted CI at the exact head: at the time of reading, `docs-gates` and `portability` were success (twice), and both
  `suites` jobs (push and pull_request runs 36928699036 and 36928701582) were **in progress**
  (`receipts/hosted_check_runs.txt`). Hosted acceptance is the manager's.
- The F5 probe demonstrates the admission gap, not a torn record. By ruling the gap remains in RTL as #84's remainder.
- I did not check specification clause text against the PDFs, which are not distributed. Citations were checked for
  consistency with the tree and the RTL behaviour.
- The 08 §4 hold bounds were derived statically and not measured in simulation. The doc itself says how long the ACMP
  wait lasts is not measured.
- The evidence pointer given for this round (`milan-fpga@4fe37ada`) does not contain `author-r3` or `author-r3b`. I read
  them at `cbba1828` on branch `ppC5a-review-evidence`.
- Physical calibration: NOT RUN. No hardware evidence.

## 9. Pending manager duties

- The donor bank and the parent consumer set at milan-fpga dev `7f0927bb`, with #137's `acmp_mutants.py` disposition line
  (`author-r3b/parent-adaptation-137-acmp-disposition.patch`, +4 lines in `scripts/measure_test_evidence.py`), owed by
  the pin bump.
- The final current-dev candidate at the merge turn (source base `16ea10ace6c755c91bb9e864b2b855acb240b09b`, live dev
  `7f0927bb3377d67d5455ef7cc336ab93adb58dcd`).
- Hosted CI acceptance at the exact head: both `suites` jobs were still running when read.
- R418-2 S3 / R418-1 S4: open the `KL_aecp_notify` fan-out tracking issue and add it to the residue checklist at merge,
  as ruled.
- Refresh the public evidence pointer so the round-3 packets (`cbba1828`, branch `ppC5a-review-evidence`) are reachable
  from the cited tree.
- The second independent review (R419-3) and the completion bar before merge.

R418-3 FINISHED
