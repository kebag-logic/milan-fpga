[R727] NEGATIVE - exact head fb182b19925b9ea24443d48d0e71b656de52b8ae

# R727-1: internal cleared-context review of PR #805 (issue #803, gPTP pin adoption f97c1803)

- Head `fb182b19925b9ea24443d48d0e71b656de52b8ae`, tree `009f0da63b66a9a358570585781ccb747e8adfa3`; base dev `5fcec84b1aa72c43048eff28bb63a982add830dd` (live dev unchanged).
- Executor `[A693]`. Reviewer role: internal, cleared context. Round R727-1. All five lenses applied.
- Verdict NEGATIVE: two open MINOR findings (F1 Tests/Robustness, F2 Docs). No BLOCKER or MAJOR. The RTL is correct as read and as exercised, and the area figures reproduce.
- Receipts and scripts are listed in `MANIFEST.sha256`. Paths in receipts are redacted to `<packet>`, `<review-clone>`, `<tools>`, `<home>`.

## Reconstruction order

1. AGENTS.md, CONTRIBUTING.md, docs/README.md.
2. Issue #803 body (Required list, Acceptance), the `[A10]` assignment (STOP rules: no top-level port or register-map change beyond the companions; route-1x1 move under 2 %), `[A693]` TAKEN and REVIEW READY.
3. FPGA-gPTP PR #92 / #93 bodies (author text) for the companion scope; the merged donor range `55680bff..f97c1803`.
4. `git diff 5fcec84b..fb182b19` and its eight commits.
5. The public evidence tree `review-evidence/803-r1` at `f75a2421`: 157 blobs downloaded, every one hash-verified against its git blob id (0 mismatches).

PR #805 had no prior review findings to resolve or retain: no PR reviews, no review comments, and only the two `[A10]` review-start comments. I did not read the parallel external review (R728).

## Reproduced evidence (this round, exact head)

| What | Command / probe | Result | Receipt |
|---|---|---|---|
| Gitlink | `git ls-tree` base vs head; donor first-parent; GitHub `branches/main`, PR #92/#93 merge SHAs, compare | `55680bff -> f97c1803`. f97c1803 is the PR #93 merge; its first parent 3426089a is the PR #92 merge. Donor main == f97c1803 (ahead 0 / behind 0); tree 0b2113f4 equal | `receipts/companions.txt`, `receipts/review-clone-integrity.txt` |
| Companions | sha256 of the copies the public assignment names; `git apply --cached` on a temporary index | `b53944d52a51...1b7a` and `3a3db518059...6451`. `1d68756c + b53944d5` gives tree `2bd62f79` == `a701de12`'s; `a701de12 + 3a3db518` gives tree `77cc055d` == `3ef8d86d`'s. Byte-exact. `1d68756c` changes only the gitlink | `receipts/companions.txt` |
| Pin-derived records through their generators (clean clone) | `ooc.sh --record-rom-digests` + `git diff --exit-code`; both diagram `.gen.py --check`; `check_submodule_docs.py`; `check_gptp_docs.py` with and without `--with-submodule`; `check_port_contracts.py --write-budget` + diff | all rc 0, all byte-identical. ROM row `b21b244f...` == the donor's tracked `syn/ooc/work/gptp_ucode.hex`; port census header `hdl 2158` regenerates identically | `receipts/gates/` |
| `TEST_RESULTS.md` | `make -C tb/verilator/tsn_fuzz ptp`, tsn-gen built at `TSN_GEN_REV deca300c` | 675 pass, 0 fail, 0 known gaps; freshness 1/1. The regenerated file differs from the committed one only in its date stamp | `receipts/runs/tsn_fuzz_ptp.*` |
| gptp_shadow | `make` (run + mutation lifecycle) | 325 checks, 325 PASS; lifecycle PASS | `receipts/runs/gptp_shadow.*` |
| milan_dp `gptp`, `gptp-lat` | `make gptp && make gptp-lat` | 200/200 each | `receipts/runs/milan_dp_gptp_legs.*` |
| gptp_plane | `make phc-step` (with `--mutants`) | 62 checks, 0 failures; its planted controls pass | `receipts/runs/gptp_plane.*` |
| Physical leg (partial) | `make -C tb/verilator/milan_dp ax1x1gptp`, stopped for wall time | Reached 3.75 of 17.99 simulated s: 75 ok, 0 FAIL. Both #89 checks pass: `the 375 ms Sync timeout makes this station grandmaster`, and `375 ms Sync timeout asserts tu in the synchronised master role got=0x3 exp=0x3` | `receipts/runs/physical_ax1x1gptp.*` |
| Lint and idiom gates | `lint_rtl.py --check`; the sv/cpp/py/sh idiom gates | all rc 0; lint 89 <= 89 | `receipts/gates/` |
| Docs gates | `docs_check.py`; `check_em_dash.py --base 5fcec84b` (pinned renderer); `gen_toc.py --check`; `check_doc_style.py`; `check_feature_status.py` | all rc 0; em dash 0 findings over 209 added lines | `receipts/gates/` |
| Area | `scripts/verify_area.py` over the published Vivado reports and `pp_resource_baseline.json` (tolerances read back from its policy fields) | route-1x1 LUT 51,259 -> 51,740 (+481, tol 500), FF +183 (600), slices 15,835 -> 15,843 (+8, tol 80); ooc-1x1 +17 / 0; ooc-8x8 +63 / +2. Against dev's own route: +310 LUT / +155 FF / +20 slices. **7 of 15,850 slices free**. Route status: 101,739 nets routed, 0 routing errors | `receipts/area-recompute.txt` |

Tool identity: the pinned wrapper reports `Verilator 5.050 2026-07-01 rev v5.050`; every build used it (`receipts/runs/verilator-version.txt`).

### Planted defects (one per clean clone, fresh build)

| ID | Planted | Suite | Result in the suite's own words |
|---|---|---|---|
| D1 (donor text) | a TLV-less Announce publishes {thisClock} | gptp_shadow | KILLED: `FAIL TLV-less selected PathTrace keeps its count got ..01 exp ..04`, plus the rest of HANDOFF's D1 list |
| D4 (donor text) | the path-head refusal restored | tsn_fuzz ptp | KILLED: `[FAIL] better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): adopted` and `...: parser drop counter unmoved` |
| D5 (donor text) | the path-count refusal restored | tsn_fuzz ptp | KILLED: `...one path-trace hop against stepsRemoved 1 (10.3.10.2.1): adopted`, `...drop counter unmoved`, `stepsRemoved 255 on a one-hop path trace (10.3.10.2.1b): parser drop counter unmoved` |
| D7 (donor text) | lost responses clear asCapable at the fourth | phc_step | KILLED: `asCapable falls at the fifth unanswered request after a crossing exchange got=4 exp=5` and `...fourth ... got=3 exp=4` |
| P4 (author text) | the AS_PATH comparator drops entry 0 | milan_dp gptp | KILLED: `entry-0-only change emits one GET_AS_PATH push got 0 exp 1` |
| M5 (mine) | the shadow copies only entries 0..6 | gptp_shadow; milan_dp gptp | KILLED: `maximum bounded PathTrace reaches final tail slot`; `maximum GET_AS_PATH final identity` |
| M16 (mine) | the shadow substitutes the GM for entry 0 | gptp_shadow; milan_dp gptp | KILLED: 9 and 10 FAILs (`path headed elsewhere publishes the received head`, `#88 GET_AS_PATH entry 0 is the received head`, ...) |
| M10 (mine) | the AS_PATH comparator's entry-0 state never updates | milan_dp gptp | KILLED: push storm; GET_AVB_INFO and GET_AS_PATH responses fail |
| **M9** (mine) | GET_AS_PATH entry 0 served from the live head, not the first-count snapshot | milan_dp gptp | **SURVIVED: 200/200** (F1) |
| **M9b** (mine) | GET_AS_PATH entries 1..7 served live, not from the snapshot | milan_dp gptp | **SURVIVED: 200/200** (F1) |
| I207 (instrumentation only) | print the engine queue pointers around the #207 forced-full window | milan_dp gptp | 200/200; `rp 0->3 wp 0->0`, restored level 1 (S1) |

Every HANDOFF word I reproduced matched what the suite printed. The probe diffs are `receipts/probe-*.diff`.

## Findings

### F1 - MINOR - Tests, Robustness - `tb/verilator/milan_dp/sim_gptp.cpp:1414-1419, 1448-1482`; `hdl/milan/milan_datapath.sv:6069-6072, 6305, 6309`

- **Authority:** `docs/reference/REGISTER_MAP.md:333` says the response snapshots the selected path before gathering entries, so it stays on one generation. IEEE 1722.1-2021 7.4.41.2 pairs `count` with `path_sequence`. AGENTS.md section 6 (Tests): each test can fail for the defect it claims to detect. This PR rewrote the arm and its comment, which still claims "These checks kill torn-response mutations" (`:1419`). The PR also gives the entry-0 snapshot `asp_resp_head_r` a new source: the engine head, where it was the grandmaster.
- **Evidence:** M9 (entry 0 from `asp_live_head_w`) and M9b (entries 1..7 from `asp_live_path_w`) each pass the leg 200/200. Nothing else in the tree reads the snapshot (`gsi_mutants.py` included). The processor gathers every entry within cycles of `asp_resp_capture_w`. The cut Announce commits thousands of cycles later, behind the held MAC, so "in-flight response remains wholly old" holds for any buffering.
- **Impact:** removing the first-count snapshot for entry 0 or for the tail passes every gate. A response whose gather overlaps a publication could then pair the old count with new entries, and nothing would catch it. The RTL at this head is correct.
- **Required outcome:** a check that fails under M9 and under M9b, with the commit landing between the first-count capture and the entry gather. Anything else is an owner decision recorded publicly, with the arm's claim corrected.
- **Verification:** re-plant `receipts/probe-m9.diff` and `receipts/probe-m9b.diff`, one at a time. Each must print FAIL on a named check, and the clean leg must stay 200/200.

### F2 - MINOR - Docs - `docs/reference/SUBMODULES.md:310`, `CHANGELOG.md:72`

- **Authority:** AGENTS.md section 7, "no undocumented requirement/interface change remains"; CONTRIBUTING section 1, "the port list IS the spec".
- **Evidence:** both lines say "No parent port, parameter or register changes." The parent module `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:199-200` changes its `pub_path_o` port from `[7*64-1:0]` to `[8*64-1:0]` and redefines `pub_path_count_o`. `tb/verilator/gptp_shadow/gptp_shadow_wrap.sv` gains a port. The same page (`SUBMODULES.md:294`) says the shadow publishes all eight entries, so the record contradicts itself. The PR body and the assignment use the accurate scope, "top-level".
- **Impact:** the authoritative adoption record tells an integrator who instantiates `KL_gptp_shadow` that no parent interface moved.
- **Required outcome:** both lines state the true scope, for example "No top-level port, parameter or register changes; `KL_gptp_shadow.pub_path_o` widens with the engine's to eight entries from entry 0."
- **Verification:** read both lines at the fixed head; `check_doc_style.py`, `docs_check.py` and `check_em_dash.py` rc 0.

### R1 - RESIDUE - Docs - `docs/reference/SUBMODULES.md:326`

"Its shipping route keeps +0.333 ns WNS." The figure is right, but "keeps" implies it is unchanged. The record was +0.236 ns and dev's own route +0.233 ns. Exact fix: "Its shipping route meets timing at +0.333 ns WNS."

### S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_gptp.cpp:1644-1688, 1882-1886`

- The rewritten #207 arm forces the queue level every cycle.
- Instrumented at this head, three stale entries pop inside the window (`rp 0->3`, `wp 0->0`). The `(wp - rp) & 3` restore then leaves level 1, a phantom entry.
- The arm's own comment (`:1677`) says the restore is exact only without such a pop.
- The full-queue check stays valid, because a push is refused on every forced cycle. But four graded arms now run after an engine that executed stale events, including this PR's two new ones.
- Suggest restoring exactly (for example by gating on `dbg_busy_o` or restoring the pointers), or running the arm last, so later verdicts are taken on an unperturbed engine.

## Lens results (clean lenses in the finding format)

- `[R727] PASS Conformance -- KL_gptp_shadow.sv:647-666; milan_datapath.sv:1633-1635, 2296-2311, 6069-6072, 6291-6311, 6503-6511; fuzz_ptp_timing.py:66-91, 171-184; sim_phc_step.cpp:320-390; sim_ax1x1gptp.cpp:1057-1090; the gitlink and both companions -- each checked against IEEE 802.1AS-2011 with Cor1/Cor2:`
  - Entry 0 is pathTrace's head as copied by 10.3.10.2.1 d), never the grandmaster put in its place, and GET_AS_PATH serves it per 1722.1-2021 7.4.41.2.
  - Without a TLV nothing is written (d)), so the served path and its generation hold across a grandmaster change.
  - Only a) to c) disqualify. The parent fixtures now expect adoption for a head other than the grandmaster and for a count other than stepsRemoved+1 (10.5.3.3.4 states N = stepsRemoved+1 only as a NOTE). stepsRemoved 255 is refused by b).
  - The fifth lost response clears asCapable: in Figure 11-8 RESET, lostResponses increments while it is at most allowedLostResponses = 3. Benches and docs say fifth, and fourth after an unanswered crossing request.
  - A Sync receipt timeout ages the port while gmPresent holds (10.3.11 / Figure 10-13). The physical leg, partly reproduced here, and the loss page agree, with priority1 255 split out.
  - The uCPU change reaches the parent only as the regenerated `gptp_ucode.hex` (ledger row == donor image).
  - Table 5.22 compares the count and every served entry, entry 0 included.
  - D1/D4/D5/D7/P4 killed with the recorded words. No finding under this lens.
- `[R727] PASS RTL -- KL_gptp_shadow.sv:196-201, 629-666, 735-760; milan_datapath.sv:1627-1636, 2278-2311, 2697-2700, 6013-6075, 6291-6311, 6450-6511; milan_csr.sv:292-293, 603-604, 2851-2853 -- checked:`
  - Widths and slices: the 8x64 head/tail split; the CSR face stays 7x64 and combinational, so head, count and tail are same-cycle.
  - The clamp at 8; the copy bound `pk+1 <= count`; the atomic commit of GM, path and count on `pub_commit_raw_w`.
  - Reset values of the renamed registers; option-off zeros (`GPTP_PLANE_EN_P` gating, `gptp_pub_path_w = '0`); GM=0 gating.
  - The other engine consumers (`gptp_plane_wrap`, `gptp_txts_wrap`) leave `pub_path_o` unconnected.
  - Lint 89 <= 89 under the pinned Verilator; sv idiom OK.
  - Area recomputed from the reports: route-1x1 +481 / +183 / +8 within 500 / 600 / 80, +310 LUT / +20 slices over dev, 7 slices free; ooc-1x1 +17, ooc-8x8 +63. AREA_BUDGET.md still states the unchanged record (15,835 slices, 15 free) and its owner-decision sentence, which is consistent with a record that was not rewritten. The slice-headroom acceptance is not ruled here.
  - M5/M16/M10 killed. No finding under this lens.
- `[R727] UNCLEAN Robustness -- F1`. Also examined: the hostile-count clamp, GM=0 and option-off aliasing, an empty TLV (now a present TLV), misaligned or duplicate TLVs still refused by the parser (`len[2:0] || pt_seen_r`), the in-flight cut test, and the #207 backpressure arm (S1).
- `[R727] UNCLEAN Tests -- F1`. Otherwise the new checks fail on their planted defects with the HANDOFF words (D1, D4, D5, D7 and P4 reproduced; M5, M16 and M10 mine), and the clean suites pass at the head.
- `[R727] UNCLEAN Docs -- F2` (R1 is residue). Otherwise checked:
  - Every pin-derived record regenerates byte-identically through its generator.
  - The physical-leg projection follows the README's own method: 4265.7 x 899637137/849624822 + 830 = 5347 s, and the 1.3476-slowdown branch gives 5484 s, so 99.0 / 101.6 % with 30.9 / 28.6 min of margin.
  - TESTING.md's 17.992742740 s / 899637137 cycles match the author's physical receipt.
  - The CHANGELOG and pin-page figures match the reports.
  - The comment-rule and privacy scan over all 693 added lines finds no lane label, lane name, review round, reviewer ID, issue-comment ID, private path, or tool or model name in source comments.
  - The docs gates are rc 0.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | KL_gptp_shadow.sv, milan_datapath.sv, milan_csr.sv, fuzz_ptp_timing.py, wire.py, sim_phc_step.cpp, phc_step.py, sim_ax1x1gptp.cpp, sim_gptp.cpp, gitlink, both companions, REGISTER_MAP.md, REGISTER_MAP_CLASSES.md, GM_LOSS_RECOVERY.md; D1/D4/D5/D7/P4 runs; the partial physical run | R727-1 | fb182b19925b9ea24443d48d0e71b656de52b8ae |
| RTL | CLEAN | the three changed RTL files, the other engine consumers, lint, sv idiom, the published Vivado reports and the record, M5/M16/M10 | R727-1 | fb182b19925b9ea24443d48d0e71b656de52b8ae |
| Robustness | UNCLEAN (F1) | clamp, GM=0 / option-off, TLV framing, cut coherence (M9/M9b), the #207 arm (I207) | R727-1 | fb182b19925b9ea24443d48d0e71b656de52b8ae |
| Tests | UNCLEAN (F1) | gptp_shadow, milan_dp gptp/gptp-lat, tsn_fuzz ptp, gptp_plane phc-step, eleven probes | R727-1 | fb182b19925b9ea24443d48d0e71b656de52b8ae |
| Docs | UNCLEAN (F2; R1 residue) | CHANGELOG, SUBMODULES, README, REGISTER_MAP.md, REGISTER_MAP_CLASSES.md, GM_LOSS_RECOVERY, GPTP_PLANE, TIME_SYNC, TESTING, the gPTP guides, traceability, the feature ledger, the milan_dp and tsn_fuzz READMEs, TEST_RESULTS.md, diagrams, rom_digests.tsv, port_docs.budget; docs gates; comment-rule scan | R727-1 | fb182b19925b9ea24443d48d0e71b656de52b8ae |

## Real limits

- **Not run here; author receipts only:** the full suite sweep, Yosys, Vivado, rtl-fast, behave, the builder bank and the docs-workflow replica. These are bank-scale and not allowed in this round. I checked their contents:
  - shard sums 15 + 17 + 16 + 16 = 64 suites and 250,958 + 1,536,446 + 380,086 + 23,927 = 2,191,417 checks;
  - Yosys `tops: 60 pass: 60 fail: 0` at `fb182b19`;
  - the Vivado report rows above.
- **Physical leg not completed here.** I stopped it at 3.75 of 17.99 simulated seconds, past the #89 checks (both pass) and before the five-interval check. Its 205-check pass and the X7/X8 kills rest on the author's receipt.
- **Standard text:** no IEEE or Milan text was opened in this round. The clause judgments rest on the clause structure of IEEE 802.1AS-2011 with Cor1/Cor2 and 1722.1-2021 as the issue, the donor and the parent cite them.
- **Companion inputs:** read from the copies the public assignment comment names. Their SHA-256 values equal the issue's and HANDOFF's.
- **Incidental read:** a keyword search for the companion hashes over the FPGA-gPTP PR #92/#93 threads surfaced a few lines of earlier review text there. Those PRs are in a different repository. Nothing from them was used as evidence.
- **Hosted contexts:** at snapshot time most exact-head jobs were in progress, and `Physical gPTP (nightly and manual)` was a skipped context. That is not proof (`receipts/hosted-checks-snapshot-1.tsv`). No manager source bank was run or inferred.
- **No hardware.** Physical calibration NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Current-dev merge-candidate validation (builder and native banks) at the merge turn.
- Exact-head hosted `verilator-suites` / `yosys-portability` and act acceptance.
- Owner decision on slice headroom: 7 of 15,850 free, +20 over dev. Figures verified, not ruled.
- The physical leg's hosted deadline projection, 99.0-101.6 % of 5,400 s.
- Carry R1 to the residue checklist.
- External review R728.
- FPGA-gPTP #87-#91 close only after an image passes the in-house scenarios.

R727-1 FINISHED
