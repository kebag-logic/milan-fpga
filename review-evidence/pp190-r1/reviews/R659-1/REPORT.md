[R659] POSITIVE - exact head 83405d192c451e9fba0ea1fe4e051aafdbb332cc

# R659-1: internal independent review of processor PR #194 (Refs #190)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #194, branch `190-per-source-tspec`
- Exact head `83405d192c451e9fba0ea1fe4e051aafdbb332cc`, tree `44576716500222854dc3c8271d5987abbaebcb1b`
- The head is the author commit `90321bff` on main `5addf297` plus the manager's merge of main `246cbc22`. The reviewed delta is `git diff 246cbc22..83405d19`.
- Scope authority: ruling issue #190 comment 6256563927, PART 1 only. It approves exactly one top-level port change: `cfg_tspec_max_frame_i[N_STREAM_OUT_P*16-1:0]`, indexed like `cfg_stream_id_i`.
- Prior public review findings on PR #194: none. At review time the PR had two REVIEW STARTED notices (R659-1 and R660-1), no review objects and no review comments, so nothing is carried forward to resolve or retain.

## Verdict

POSITIVE. There are no open BLOCKER, MAJOR or MINOR findings, and all five lenses are CLEAN. The review recorded two RESIDUE items (wording in the PR body only, with their exact fixes) and one SUGGESTION.

## What was checked, against the ruling's checklist

| Ruling item | Result | Evidence |
|---|---|---|
| `cfg_tspec_max_frame_i` is `[N_STREAM_OUT_P*16-1:0]`, source *s* at `[16*s +: 16]`, the `cfg_stream_id_i` layout | holds | `hdl/top/protocol_processor_top.sv:300-303`. The slot read is at `:2703`, `cfg_tspec_max_frame_i[32'(tkr_gate_src_w) * 16 +: 16]`. `cfg_stream_id_i` (`:308`) has the same flat `[W*s +: W]` packing. |
| Every engine-driven DECLARE_TALKER, gate open and gate close, captures its own source's slot | holds | One capture expression, `protocol_processor_top.sv:2694-2705`. It is under `tkr_gate_open_w \|\| tkr_gate_close_w`, with `index: 8'(tkr_gate_src_w)` and `mfs` taken from that same source's slot. Downstream: `KL_srp_top.sv:852`, then `:918` `adm_mfs_r[idx]`, which prices admission, and `KL_srp_talker_fsm.sv:500-504` `wtsp_r[gate_src_i]`, the wire TSpec. Both store the TSpec on gate open only. The reviewer probe `rv_close_slot0` (gate close takes slot 0) survives as expected, which confirms that a close carries no TSpec. |
| The tied-off service path follows | holds | The processor's service face already carries MaxFrameSize per request (`svc_max_frame_i`, `:628`, captured at `:2730`) and is unchanged. In the parent at dev e9cbb676, `KL_pp_shadow.sv:1285-1293` keeps it tied off (`svc_valid_i 1'b0`, `svc_max_frame_i '0`), and nothing there needs to move (`receipts/parent-patch-check.txt`). |
| No other port, parameter or register-map change | holds | `receipts/rtl-scope.txt`: the only RTL hunks are the port declaration and the slot read. Among the top's input/output/parameter declarations, only that one line differs. No file outside `hdl/`, `docs/` and `tb/` changed, and `docs/architecture/07_memory_maps.md` is untouched. |
| Suite cases for two sources with different values, each with a planted mutant | holds | Section `tb/pp_top` TS gives eight different Milan Table 4.4 values: source 0 = 217 and source 1 = 29. `tspec_slot_zero` fails source 1's check and `tspec_slot_last` fails source 0's. `tspec_no_allocator` fails TS0. I re-ran all three at the exact head: KILLED, golden PASS (`receipts/ts-arms-results.json`). My own probes at the exact head (`receipts/reviewer-probes-results.json`): `rv_slot_xor1` (neighbours swapped), `rv_stride8` and `rv_low_byte_dropped` are all KILLED, and `rv_close_slot0` SURVIVED as expected (an equivalent mutant). |
| With the old scalar on every slot, parent behaviour is unchanged | holds on the author's evidence | Inside the processor, the main model drives 1024 on every slot. The full `tb/pp_top` run at the exact head gives 10,528/10,528 PASS. At `246cbc22` it gives 10,519/10,519. The only difference is in the default build (10,017 → 10,026, the 9 TS checks). The Verilator warning multiset is identical (`receipts/run/pp_top_{head,base}.log`). For the parent, the author's scratch patch drives `{N_STREAM_OUT_P{cfg_tspec_max_frame_i}}`. It applies cleanly to the e9cbb676 file (blob `50455d46` → `5e84f1ed`), and the processor instance takes `N_STREAM_OUT_P` from the wrapper. The author's records show 23 of 24 consumer gates at rc 0 at both base and head, with identical records apart from normalised noise. `check_submodule_docs` fails identically at both, and the head-without-patch control fails `lint_rtl` on the width mismatch (published `records/cons/*`). |
| The TSpec value is a MaxFrameSize per IEEE 802.1Q-2018 35.2.2.8.4 and Milan v1.2 4.3.3.2 Table 4.4; the parent sets the CRF value later | holds | 802.1Q-2018 35.2.2.8.4 a) says MaxFrameSize "represents the maximum frame size that the Talker will produce". Milan v1.2 4.3.3.2 Table 4.4 gives AAF PCM32 48 kHz as 24·N+24+1 and CRF at 1 ts/pdu as 28+1. The bench values 217, 29 and 73…193 match. My recomputed TS admission sum, using Table 4.4's four-step rule, is 74.368 Mb/s for sources 0-6, and source 7 is refused at 75 Mb/s. The PR is "Refs #190", and the CRF slot = 29 is left to part 2 in the parent. |
| The receipts index matches its files | holds | `receipts/evidence-index-check.txt`. All 242 MANIFEST.json entries match their published sha256, and every file is listed. `author/INDEX.md` (240 lines) and `author/round1/INDEX.md` (8 lines) match bytes and sha256. The three path-redacted files match their `original_sha256`. |
| Comment rule (owner 2026-10-15) | holds | I scanned the 235 added lines for lane labels, lane names, review rounds, reviewer IDs and comment IDs, and found no new instance. "admission round" and "greedy round" are the design's own terms. "at the lane head" in the README is the file's established measurement phrase (five instances at base) and names no lane. |

The merge is clean (`receipts/merge-check.txt`). `git merge-tree --write-tree 90321bf 246cbc2` reproduces the head tree `44576716…` exactly. `diff 246cbc22..83405d19` equals `diff 5addf297..90321bff` except for two blob-index lines (`docs/architecture/10_srp_engine.md` and `tb/pp_top/README.md`, which both sides touch in non-overlapping hunks).

## Findings

### R659-1-R1: RESIDUE (Docs)
- Artifact: PR #194 body, the opening ("Branch `190-per-source-tspec`, one commit on main `5addf297`") and "Gates" ("Every gate and campaign ran at base `5addf297` and at this head `90321bff`").
- Evidence: the PR head is now `83405d19`, which is `90321bff` plus the manager's clean merge of main `246cbc22` (`receipts/merge-check.txt`).
- Impact: wording only. The measurements are correctly attributed to `90321bff`, but "this head" no longer names the PR head.
- Exact fix: replace "at this head `90321bff`" with "at the author head `90321bff` (the PR head `83405d19` adds the clean merge of main `246cbc22`, whose tree equals the automatic merge)". Replace "one commit on main `5addf297`" with "one commit on main `5addf297`, then a merge of main `246cbc22`".
- Verification: read the PR body.

### R659-1-R2: RESIDUE (Docs)
- Artifact: PR #194 body, "Gates", the `check_submodule_docs.py` bullet ("fails identically at both (`documented pin differs from Git`)").
- Evidence: the published `records/cons/{base,head}/submodule_docs.log` shows two findings at both revisions: `documented pin differs from Git` and `submodule diagram stale: docs/diagrams/submodule_boundaries.{svg,drawio,png}` (FAIL, 2 findings). The cmp diff is empty, and HANDOFF.md names both.
- Impact: wording only. The "identical at both" claim holds.
- Exact fix: "`check_submodule_docs.py` fails identically at both, with the same two findings (`protocol-processor: documented pin differs from Git` and the stale `docs/diagrams/submodule_boundaries` diagram)".
- Verification: read the PR body.

### R659-1-S1: SUGGESTION (Docs)
- Artifact: `tb/pp_top/README.md:2195-2196` ("Sources 0 to 6 take 74.368 Mb/s of the 75 Mb/s ceiling (Milan v1.2 4.3.3.2's bandwidth rule)"), and the matching comment in `tb/pp_top/sim_main.cpp` section TS.
- Evidence: the 74.368 Mb/s figure follows Milan v1.2 4.3.3.2's four-step bandwidth rule. The 75 % ceiling comes from IEEE 802.1Q-2018 34.3.1 (default deltaBandwidth), and `hdl/srp/KL_srp_admission.sv:27-28` cites it that way. The parenthetical can be read as attributing the ceiling to Milan.
- Suggested outcome: put the Milan citation beside 74.368 and cite 802.1Q-2018 34.3.1 for the 75 % ceiling. The suggestion does not affect the verdict.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 802.1Q-2018 35.2.2.8.4 a) and 35.2.2.8 (FirstValue increment), and 34.3.1, read in the standard. Milan v1.2 4.3.3.2 Table 4.4 and its bandwidth note, read in the spec. The value formulas in docs/bench/PR, and the TS admission arithmetic, which I recomputed. Ruling 6256563927 part 1 against the delta. | R659-1 | 83405d192c451e9fba0ea1fe4e051aafdbb332cc |
| RTL | CLEAN | `protocol_processor_top.sv:297-308`, `:2257-2290`, `:2669-2768`. The SRP core's consumption (`KL_srp_top.sv:840-925`, `KL_srp_talker_fsm.sv:495-506`, `KL_srp_admission.sv:74,127`). The port/parameter scope diff. `lint_hdl.sh` at the head with pinned Verilator 5.050: 41 LINT OK, rc 0. | R659-1 | 83405d192c451e9fba0ea1fe4e051aafdbb332cc |
| Robustness | CLEAN | Lint of the top at N_STREAM_OUT_P = 1, 2, 3, 4, 6, 8, 16 at head and base: 0 warnings at every shape (`receipts/run/lint_shapes_*.log`). At N=1 the port is `[15:0]`, the shipping parent's shape. The gate-close path is inert for the TSpec by design (probe). The parent patch applies to the e9cbb676 file, and the service face tie-off is unchanged. Breaking-port impact: the parent must drive the wide port, as the author's head-nopatch `lint_rtl` control shows and the integrator guide states. | R659-1 | 83405d192c451e9fba0ea1fe4e051aafdbb332cc |
| Tests | CLEAN | `tb/pp_top/sim_main.cpp` TS (TspecPhase, run_tspec, `--tspec-only`), `pp_top_wrap.sv`, `Makefile` `tspec`, and the `acmp_mutants.py` TSPEC group and TALLY. Full `make run` of `tb/pp_top` at head (10,528 PASS, rc 0) and at base 246cbc22 (10,519 PASS, rc 0). TS arms at head: 3/3 KILLED with golden PASS. Four reviewer probes, as expected. | R659-1 | 83405d192c451e9fba0ea1fe4e051aafdbb332cc |
| Docs | CLEAN (R1, R2 RESIDUE; S1 SUGGESTION) | `02_interfaces.md` §4.1 and the new anchor, `09_verification.md` §8.12, `10_srp_engine.md` F10.7 text, `integrator.md` §6, the `tb/pp_top/README.md` section TS, and the PR body. `make check` at head in a separate clone: rc 0, links 1206 OK. `gen_matrix.py --check`: 94 rows, 0 untested. Comment-rule scan of the delta. Published evidence MANIFEST/INDEX verified. | R659-1 | 83405d192c451e9fba0ea1fe4e051aafdbb332cc |

## Receipts (paths relative to this packet; listed in MANIFEST.sha256)

- `receipts/tool-identities.txt`: the pinned Verilator 5.050 wrapper and binary sha256 (they match the author's r11), g++ and Python.
- `receipts/merge-check.txt`: the head, its parents, the recomputed merge tree, and the patch-identity check.
- `receipts/rtl-scope.txt`: the full hdl delta and the port/parameter declaration diff.
- `receipts/run/*.log|*.rc`: pp_top full at head and base, TS arms, reviewer probes, lint_hdl, lint shapes at head and base, make check, gen_matrix (home paths redacted to `<container-layer>`/`<home>`).
- `receipts/ts-arms-results.json` and `receipts/reviewer-probes-results.json`: the per-mutant records.
- `receipts/evidence-index-check.txt`: the published evidence MANIFEST/INDEX verification.
- `receipts/parent-patch-check.txt`: the scratch parent patch against the dev e9cbb676 `KL_pp_shadow.sv`.
- `receipts/hosted-check-runs.txt`: the hosted check runs at the exact head, as observed.
- `receipts/clone-integrity.txt`: the review clone after the review. HEAD and tree are exact, 0 status entries, 648 tracked blobs re-hashed with 0 blob or mode mismatches, and the repository has no gitlinks.
- `scripts/launch.sh`, `scripts/reviewer_probes.py`, `scripts/lint_shapes.sh` and `scripts/check_evidence_index.py`: portable scripts that reproduce the runs above.

Every build and probe ran on exported trees under the packet's `scratch/`, which is not published. The review clone was never modified.

## Real limits

- I ran no full processor bank at the exact head: no `run_suites.sh` over every suite, no Yosys `syn/yosys/run.sh`, and no campaigns other than the TS arms. The author's base/head gate and campaign records are for `90321bff` (on main `5addf297`). The exact head adds only the clean merge of `246cbc22`, and I re-ran `tb/pp_top` (full), lint, make check and the matrix at the exact head myself.
- I ran no parent consumer gates. The "parent unchanged" item rests on the author's published scratch-parent records at `90321bff` against dev e9cbb676. I checked their integrity and the patch's applicability; I did not re-execute them.
- Hosted CI at the exact head, as observed: `docs-gates` and `portability` completed with success, twice each, and `suites` was still in progress in both runs. The combined status was pending. I assert nothing about the hosted suites outcome.
- No manager source bank ran at this head. Physical calibration NOT RUN; no hardware; field skips are not hardware proof.
- The Milan Base Audio Formats specification was not needed for part 1 and was not consulted. The CRF value 29 is settled by the ruling and checked against Milan v1.2 Table 4.4.

## Pending manager duties

- Validate the current-dev merge candidate (source base 246cbc22, live dev e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f) with the builder and native banks at the merge turn, and link the receipts on the PR.
- Hosted and act acceptance, including the in-progress hosted `suites` job at this head.
- Carry R659-1-R1 and R659-1-R2 to the residue checklist.
- Keep issue #190 open for part 2 (the parent pin adoption): drive the CRF slot with 20 + 8 × timestamps_per_pdu + 1 and the AAF slots as today; add a suite case pinning it against the PDU length, with a planted mutant; correct `KL_crf_tx.sv:206-211`; record the new pin for `check_submodule_docs`.
- Merge still requires the second independent review.

R659-1 FINISHED
