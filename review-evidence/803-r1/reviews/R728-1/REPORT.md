[R728] NEGATIVE - exact head fb182b19925b9ea24443d48d0e71b656de52b8ae

# R728-1: external review of PR #805 (issue #803, gPTP pin adoption f97c1803)

- Exact head `fb182b19925b9ea24443d48d0e71b656de52b8ae`, tree `009f0da63b66a9a358570585781ccb747e8adfa3`; base dev `5fcec84b1aa72c43048eff28bb63a982add830dd` (also the live dev tip the manager named).
- Reconstructed from AGENTS.md, CONTRIBUTING.md, the issue body and its assignment, TAKEN and REVIEW READY comments, the PR body, the diff `5fcec84b..fb182b19`, the FPGA-gPTP diff `55680bff..f97c1803`, FPGA-gPTP PRs 92 and 93, the two companion patches named in the assignment, and the public evidence tree at `f75a2421` (`review-evidence/803-r1`).
- Verdict: NEGATIVE. One MINOR (F1, Tests) is open. Every other lens is clean, and nothing else blocks.
- Prior public review findings on PR #805: none. The PR and the issue carry only the two review-start notices, and no inline comment or review body exists. There is nothing to resolve or retain.

## Findings

### F1: MINOR, Tests: no test can fail when the GET_AS_PATH response snapshot is bypassed

- **Lenses:** Tests. I did not attribute it to Robustness. The RTL does snapshot entry 0, the count and the tail at the first count request (`hdl/milan/milan_datapath.sv:6069-6073`), and the entry pick reads only those registers (`:6304-6310`). The behaviour is correct by inspection. Only the evidence for it is missing.
- **Where:** `hdl/milan/milan_datapath.sv:6070` (`asp_resp_head_r <= asp_live_head_w;`) and `:6305` (entry 0 from `asp_resp_head_r`). This PR changed both lines.
- **Test and comment:** the in-flight cut arm at `tb/verilator/milan_dp/sim_gptp.cpp:1450-1501`. The RTL comment at `milan_datapath.sv:6032-6036` says the harness watches `asp_resp_entry_w`.
- **Evidence:**
  - Mutant M5 serves entry 0 from the live head instead of `asp_resp_head_r`. It passes all 200 checks (`receipts/mutants/M5.json`, `logs/M5.log`).
  - Mutant M5b does the same for the tail entries (`asp_live_path_w` instead of `asp_resp_path_r`). It also passes 200/200 (`M5b.json`).
  - The instrumented harness (`scripts/probe_cut_timing.py`, `receipts/probes/cut_timing_head.log`) shows why. The first path-entry request fires at cycle 13 of the cut loop, and the cut's publication commits at cycle 462. The whole response is therefore gathered before the new path exists. The RTL comment at `:6032-6036` calls exactly this "a false-green consequence of publishing after the gather had already finished", but no harness reads `asp_resp_entry_w`, either at the head or on dev.
  - The gap predates this PR. The same probe on dev `5fcec84b` gives cycle 14 against 394 (`cut_timing_dev5fcec84b.log`).
  - It is still within this PR's delta, for three reasons:
    - The companion re-sourced entry 0 from the grandmaster to the engine's received head, on the two mutated lines.
    - It rewrote this arm's cut so that, for the first time, the old and new entry 0 differ (GMID_EMPTY and thisClock).
    - The delta's `README.md` and `REGISTER_MAP.md` text restates the in-flight coherence.
  - So the check "in-flight response remains wholly old GM" now has a distinguishable value and still cannot fail.
- **Impact:** a regression that splices a torn GET_AS_PATH response would pass every gate. Examples are a live entry 0 or tail behind a snapshotted count, or a snapshot dropped during a later edit. Such a response pairs the old count with new entries, which violates the coherent count and path_sequence of IEEE 1722.1-2021 7.4.41.2. This matters more now that entry 0 can change without a grandmaster change (FPGA-gPTP #88).
- **Required outcome:**
  - M5 and M5b each fail at least one named check at the merge candidate.
  - The RTL comment's ordering claim about `asp_resp_entry_w` either becomes true (the harness asserts that the cut publishes after the count snapshot and before the first entry request) or is corrected.
- **Verification:** re-run M5 and M5b with `scripts/mutant_probe.py` (the arguments are in their JSON) and `scripts/probe_cut_timing.py` on the corrected head. Both mutants must be KILLED, and the clean `milan_dp gptp` leg must stay 0 FAIL.

### S1: SUGGESTION, Tests: the #207 full-queue arm's residue comment

- **Where:** `tb/verilator/milan_dp/sim_gptp.cpp:1677-1680`.
- The arm forces `evq_lvl_r` to 4 on every cycle of a 400-cycle window, and its comment allows that dispatch can pop stale entries inside it. The comment says this is benign "only because nothing after this arm grades the queue or the events it would run".
- After this PR, two new arms run after it (`:1885-1886`, the received head and the entry-0 change), and they grade publications driven by events. They pass at this head.
- Suggested change: gate the restore on `dbg_busy_o` or on an unmoved `evq_rp_r`, or move the arm last, so the stated invariant does not depend on arm order.
- This is non-blocking. I did not probe whether a pop actually occurs.

No RESIDUE item. The added-line scan of the delta (688 lines, excluding the gPTP submodule and diagram binaries) found no lane label, lane name, review round, reviewer ID, issue-comment ID, private path, or tool or model name.

## Requested checks

### (1) Gitlink, companions and pin-derived records: confirmed

**Gitlink**
- `gptp-processor` is at `f97c18035be6ef5345e5af27db2124c5697c1b40`.
- The public FPGA-gPTP compare `f97c1803...main` is identical, so it is the main tip.
- PR #92 merged as `3426089a`, and PR #93 merged as `f97c1803`. The first-parent chain from `55680bff` is exactly those two merges.

**Companions**
- The sha256 values match in full: `b53944d52a51…1b7a` and `3a3db51805985df7…6376451` (`receipts/static/companion_sha256.txt`).
- On dev `5fcec84b`, both applied in order with `git apply --index`, clean.
- The resulting tree (`34756a2f`) differs from the head only in 24 files, all records, docs and two comment or harness-text edits (`companions_vs_head.txt`).
- Every RTL and test byte at the head is therefore the companions' own.

**Pin-derived records, regenerated by their generators at the head (static copy)**
- `bash syn/yosys/ooc.sh --record-rom-digests` returned rc 0, and then `git diff --exit-code syn/yosys/rom_digests.tsv` was empty.
- Independently, `gen_gptp_ucode.py` produces `b21b244f…ba56` (`gptp_ucode_regenerated.hex`). That equals the new ledger row and the donor's tracked `syn/ooc/work/gptp_ucode.hex`.
- `check_port_contracts.py --write-budget` and `measure_naming.py --write-budget` left both budgets byte-identical.
- These all returned OK:
  - `submodule_boundaries.gen.py --check` and `timesync_chain.gen.py --check`
  - `check_diagram_pngs.py`
  - `check_submodule_docs.py` (6 exact gitlinks)
  - `check_gptp_docs.py`, with and without `--with-submodule`
  - `docs_check.py` (0 findings)
  - `check_feature_status.py` (0)
  - `check_doc_style.py`
  - `gen_toc.py --check`, under the pinned Markdown venv
  - `pp_resource_gate.py check-baseline` (3 endpoints)
- A fresh `make -C tb/verilator/tsn_fuzz ptp` at the pinned tsn-gen `deca300c` printed `675 pass, 0 fail, 0 known gaps`, with freshness PASS. The regenerated `TEST_RESULTS.md` differs from the committed one only in its date stamp.

### (2) Clause-by-clause conformance of the milan-fpga side: correct

**Entry zero and its compare (`KL_gptp_shadow.sv:199-200, 632-666`)**
- Eight entries are published from entry 0, and only entries below the clamped count (8 or fewer) are copied.
- The path generation compares the count and all eight entries, entry 0 included. The retired `count ? GM : 0` head term is gone, and the GM gate (`|pub_gm_raw_w`) is kept.
- This matches 802.1AS-2011 10.3.10.2.1 d), where pathTrace is the received pathSequence plus thisClock, and Milan v1.2 Table 5.22, where a path change is any change of the served sequence.
- A GM change on a TLV-less Announce leaves the served sequence alone, and the scalar GM publication stays independent.

**GET_AS_PATH (`milan_datapath.sv:1630-1636, 2278-2311, 2700, 6070, 6305`)**
- Entry 0 is the engine's head under the same owner selection: option-off gives zero (`g_gptp_off` drives the full 8*64 wire to `'0`), and no GM gives empty.
- Entries 1 to 7 reach the unchanged 7-wide CSR face.
- There is no timing skew between the head path and the count and tail path, because `milan_csr.sv:2851-2853` is a combinational pass-through.
- This matches IEEE 1722.1-2021 7.4.41.2: count plus path_sequence, with entry 0 the head of pathTrace.

**AS_PATH notification (`:6466-6512`)**
- The comparator watches entry 0, the count and the tail. This matches Milan v1.2 Table 5.22.

**Parser (FPGA-gPTP `KL_gptp_rx_parser.sv`)**
- The retired strict rules (path head equal to GM, N equal to stepsRemoved+1, non-empty TLV) are removed.
- What remains: 8N framing, a single PathTrace, and the all-hop loop test, which is c).
- A presence bit in w12[63] distinguishes an empty TLV from an absent one.
- 10.3.10.2.1 a) to c) are the only disqualifiers, which agrees with that clause and with N = stepsRemoved+1 being a NOTE to 10.5.3.3.4 (the 10.3.8.23 and 10.6.3.3 pathTrace and TLV text).
- stepsRemoved 255 is still refused by b), and the tsn_fuzz probe exercises this.

**Engine (`KL_gptp_engine.sv`)**
- Address 7 copies only when the TLV is present, from entry 0, and appends thisClock below eight entries. Without a TLV, pathTrace is unchanged (#87).
- Reset and BECOME load `{thisClock}`, which is 10.3.12.1.4 i) with Cor1.

**uCPU microcode (`gen_gptp_ucode.py`)**
- Sync receipt timeout ages the port only under gmPresent, meaning priority1 below 255. This matches 802.1AS-2011 Figure 10-13 with Cor1 and 10.3.12.1.4 g).
- `LOST_CLEARS_AT_C = allowedLostResponses + 2`, so the fifth consecutive loss clears asCapable. This matches Figure 11-8 RESET, where the count increments while it is at or below 3.
- A duplicate Pdelay_Resp for the outstanding sequenceId goes to RESET, per Figure 11-8 (#91).
- The ROM growth is the uCPU's +71 LUT in the placed hierarchy receipt.

The parent docs state these rules consistently: `GM_LOSS_RECOVERY.md:34-49`, `REGISTER_MAP.md` 0x7DC, `REGISTER_MAP_CLASSES.md`, `README.md`, the pin page and the changelog.

### (3) New checks fail on their planted defects with the words HANDOFF records: confirmed on a sample

I planted each defect alone in a fresh copy (`scripts/mutant_probe.py`, receipts in `receipts/mutants/`).

**gptp_shadow**
- M1s (P1, generation ignores entry 0): KILLED with `FAIL entry-0-only change spends one path generation got …05 exp …06`.
- M2s (copy loop off by one, my own): KILLED, including `maximum bounded PathTrace reaches final tail slot`.

**milan_dp `gptp`**
- M3 (P3, entry 0 is the GM again): KILLED on `#87 TLV-less GM switch: GET_AS_PATH entry 0 is still GMID`, `#88 post-cut response is {thisClock}` and `#88 GET_AS_PATH entry 0 is the received head`.
- M4 (P4): KILLED on `entry-0-only change emits one GET_AS_PATH push`.
- M6 (CSR face takes entries 0..6): KILLED on 13 FAIL lines, including `GET_AS_PATH ends with thisClock`.
- M7 (head snapshot never updated, my own): KILLED.

**gptp_plane phc_step (D7, the donor's planted text `LOST_CLEARS_AT_C = LOST_N_C + 1`)**
- KILLED with `[FAIL] asCapable falls at the fifth unanswered request after a crossing exchange got=4 exp=5` and `[FAIL] asCapable falls at the fourth unanswered request after an unanswered crossing request got=3 exp=4`.
- Both lines match HANDOFF word for word.

M5 and M5b survive. That is F1.

### (4) Area receipts: figures confirmed

All figures come from the raw placed utilization reports in the public evidence. I did not rule on the slice-headroom acceptance; that is an owner decision.

| | LUT | FF | Slice |
|---|---:|---:|---:|
| Record (`pp_resource_baseline.json`) | 51,259 | 53,208 | 15,835 |
| Dev nightly `97aab1d0` | 51,430 | 53,236 | 15,823 |
| Head (`route-1x1-…utilization_place.rpt:35,40,76`) | 51,740 | 53,391 | 15,843 |

- **Against the record:** +481 LUT (tolerance 500), +183 FF (600) and +8 slices (80).
- **Against dev:** +310 LUT, +155 FF and +20 slices.
- **Free slices:** 15,850 − 15,843 = 7.
- **Gate checks:** `route-1x1-check-against-record.log` reports WNS +0.333 and WHS +0.020 ns, route complete, `RESULT: PASS`. The ooc-1x1 (+17) and ooc-8x8 (+63) check logs also report PASS. `bank-timeline.txt` shows Vivado rc=0 for all four runs.
- **Placed hierarchy delta:** `KL_gptp_shadow` +251/+119, its own logic +231/+64, u_ucpu +71, and the parser −65/−80, as the PR states.
- **AREA_BUDGET.md:** it is consistent with the receipts. It still describes the committed record (`:132-141`: 15,835 used, 15 free, and an owner decision needed for further growth), which this PR does not rewrite. The head's 7 free slices are stated on the pin page, in the changelog and in the PR as an open owner decision.

### (5) Docs, changelog and pin page match the head

- `CHANGELOG.md` "Unreleased - gPTP pin f97c1803" and the `SUBMODULES.md` #803 section match the head and the receipts: 17.992742740 simulated s, +481 and +310 LUT, 20 slices, 7 free, +0.333 ns.
- The milan_dp README re-scaled projection checks out: 4,265.7 × 899637137/849624822 + 830 = 5,347 s, and the 5,225 s arm gives 5,484 s, which are 99.0 % and 101.6 % of the deadline. The margins are 30.9 and 28.6 min.
- The source comments in the delta carry only behaviour, clause and issue IDs.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_gptp_shadow.sv:199-200,629-666`; `milan_datapath.sv:1630-1636,2278-2311,2697-2700,6066-6073,6291-6311,6450-6512`; FPGA-gPTP `KL_gptp_engine.sv`, `KL_gptp_rx_parser.sv`, `gen_gptp_ucode.py` diffs `55680bff..f97c1803`, against 802.1AS-2011 + Cor1/Cor2 10.3.10.2.1 a)-d), 10.3.11/Fig 10-13, 10.3.12.1.4 g)/i), 11.2.15/Fig 11-8, 1722.1-2021 7.4.41.2, Milan v1.2 Table 5.22 | R728-1 | `fb182b19925b9ea24443d48d0e71b656de52b8ae` |
| RTL | CLEAN | Same RTL lines: widths 8*64 and 7*64, slices `[63:0]` and `[8*64-1:64]`, count clamp, reset values, option-off `g_gptp_off` (`milan_datapath.sv:8906,8927`), CSR pass-through `milan_csr.sv:2851-2853` (no head/tail skew), all `pub_path_o` consumers (`gptp_txts_wrap.sv:266`, `gptp_shadow_wrap.sv:329`), placed-hierarchy and utilization receipts | R728-1 | `fb182b19…` |
| Robustness | CLEAN | Received-head, empty-TLV, absent-TLV, 8+-entry clamp and GM-zero paths in shadow, datapath and engine; response snapshot registers `milan_datapath.sv:6069-6073`; clean legs gptp_shadow 325/325, milan_dp `gptp` 200/200 and `gptp-lat` 200/200, tsn_fuzz ptp 675/0, phc_step 62/0 + 8/8 controls (`receipts/clean/`) | R728-1 | `fb182b19…` |
| Tests | UNCLEAN (F1 open) | `sim_gptp.cpp`, `gptp_shadow/sim_main.cpp`, `gptp_shadow_wrap.sv`, `sim_phc_step.cpp`, `phc_step.py`, `sim_ax1x1gptp.cpp`, `fuzz_ptp_timing.py`, `wire.py` diffs; removed checks replaced (`sim_gptp.cpp:1306-1411`, `sim_main.cpp:957-995`); 9 mutants (`receipts/mutants/`); cut-timing probes (`receipts/probes/`) | R728-1 | `fb182b19…` |
| Docs | CLEAN | `CHANGELOG.md`, `SUBMODULES.md`, `README.md`, `REGISTER_MAP.md`, `REGISTER_MAP_CLASSES.md`, `GM_LOSS_RECOVERY.md`, `GPTP_PLANE.md`, `TESTING.md`, `milan_dp/README.md`, `tsn_fuzz/README.md`, `milan_feature_status.json`, the 8 gPTP link pages; docs gates in `receipts/static/`; added-line identifier scan | R728-1 | `fb182b19…` |

## Real limits

- **Not run here, read from the author's published receipts only:**
  - the full sweep
  - the physical `milan_dp_gptp` leg (205 checks; about 1.5 h on this host)
  - Vivado (route-1x1, ooc-1x1, ooc-8x8)
  - the full Yosys bank, the rtl-fast replica, RTL lint, xvlog and the idiom gates
  - the complete docs workflow and the builder bank
- **How the clean `milan_dp gptp` result was obtained:** the first in-copy `make … gptp` lost its console output to a redirect error in my launcher. The 200/200 result is from re-executing the same built binary (`receipts/clean/dpgptp-exec.log`).
- **Engine mutants:** I reproduced only D7. I did not re-plant D1 to D6, X7 or X8.
- **Standards text:** the clause readings rely on my knowledge of the cited editions, not a quoted copy of the standards.
- **Hosted evidence:** the exact-head hosted contexts were mostly pending when I took the snapshot (`receipts/hosted/pr805-checks-snapshot.txt`). I claim no hosted result and no manager source bank.
- **Hardware:** physical calibration was NOT RUN, and no image was built or flashed.

## Pending manager and owner duties

- The owner decision on slice headroom: 7 of 15,850 free, +20 over dev's route, against `AREA_BUDGET.md:140-141`.
- The physical leg's hosted deadline (projection 99.0 to 101.6 % of 5,400 s), already flagged by the author.
- Exact-head hosted `verilator-suites` and `yosys-portability` acceptance.
- The current-dev candidate merge validation (builder and native banks) at the merge turn, against the parallel #799 / PR #802 adoption.
- Closing FPGA-gPTP #87 to #91 only after an image passes the in-house gPTP scenarios.
- Re-review of F1's fix at a new head.

The exact clone was verified after all probes: HEAD and tree match, index modes and blobs equal the tree, all submodule gitlinks are at their pins, and no tracked file is dirty. Every probe ran in disposable copies under `scratch/`.

R728-1 FINISHED
