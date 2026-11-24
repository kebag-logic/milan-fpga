[R915] NEGATIVE - exact head bbfdb6746d585e490508783dc8a88c79fbab02c0

# R915-1: internal cleared-context review of PR #995 (Closes #994)

- Head `bbfdb6746d585e490508783dc8a88c79fbab02c0`, tree `eb8282dfbfa9d8dc2e1c87bc3c09b5c010d30263`, verified in the review clone (`receipts/published/clone_integrity_final.txt`).
- Reviewed delta: the four commits `300da99b..bbfdb674` (`973f2f20` gitlink, `39e9c9d2` pin sites, `8c5a51e1` records, `bbfdb674` style). The train (PR #988 at `300da99b`) is reviewed separately and is not judged here.
- Order followed: AGENTS.md and CONTRIBUTING.md, docs/README.md, the #994 body (no comments on the Issue), the cited authorities (GPTP_PLANE.md, SUBMODULES.md, BUILDING.md section 5, #818, the FPGA-gPTP PR #108 owner decision), the raw diff, the donor delta `1616fc8f..1213ac5b`, then the evidence packet at `3779446004dfb5ea4b18088bed83637e49139754/review-evidence/gptppin-r1`.
- No reviewer report on PR #995 was read before this verdict and the ledger below were written. The section "Prior public findings on this PR" was added after.

## Verdict basis in one paragraph

The pin move is correct and complete. `1213ac5b` is a fast-forward of `1616fc8f` on the donor `main`. Its tree is `7b579e33`, the reviewed head `331e27de`'s tree. Every current pin site names it. The ROM ledger row equals an independent regeneration, and the routes and their receipts support every figure in the PR. But the change alters published platform behaviour: the time base's frequency at every grandmaster takeover, and which frame wins the receipt-timeout race. No parent test grades either change. I ran every parent gPTP consumer suite at this head and again with only the gitlink reverted to `1616fc8f`, and all of them pass identically. The PR states "No platform test is added". The donor review asked for the takeover phase to be adopted into parent regression with this bump, and the follow-up Issue the PR names does not exist. That gap is F1 (MAJOR), so the verdict is NEGATIVE.

## What I verified (the four focus items)

### (1) Every pin site names `1213ac5b`; historical records left

- Index gitlink `160000 1213ac5b9e09b8759ba76cc70c53652b5e108996 0 gptp-processor` (`receipts/published/clone_integrity_final.txt`).
- The donor ancestry and identity are in `receipts/published/donor_identity.txt`. `merge-base --is-ancestor 1616fc8f 1213ac5b` succeeds. Its first-parent merges are #103 (`a64be73`), #105 (`7cfd6a0`) and #108 (`1213ac5`, second parent `331e27de`). `331e27de^{tree}` = `1213ac5b^{tree}` = `7b579e33a97ff4f2bec8c0064f0f73c862bbb135`.
- #103 and #105 change no `hdl/` or `syn/` file (`receipts/published/donor_rom.txt`: empty `--stat` for those paths over `1616fc8f..7cfd6a0`). Only #108 touches `hdl/top/KL_gptp_engine.sv`, `hdl/ucode/gen_gptp_ucode.py` and `syn/ooc/work/gptp_ucode.hex`.
- The pin-site gates, run in a scratch clone of this head (`receipts/published/doc_gates_head.txt`), all exit 0:
  - `check_gptp_docs.py`: OK, 8 current pages.
  - `check_submodule_docs.py`: OK, 6 exact gitlinks.
  - `submodule_boundaries.gen.py --check`: OK, decoded PNG.
  - `timesync_chain.gen.py --check`: OK.
  - `docs_inventory.py --check`, `check_doc_style.py` (and its `--selftest`), `docs_check.py` (0 findings, scrub 23/23) and `git diff --check 300da99b HEAD`.
- ROM ledger row `syn/yosys/rom_digests.tsv:17`: `1213ac5b… gptp_ucode.hex 4eb21cef…`. An independent `gen_gptp_ucode.py -o` at this head gives `4eb21cef…`, 1024 words, 1013 real. At `1616fc8f` it gives `e83709d9…` (the existing row), 1015 real (`receipts/published/romgen_head.txt`, `romgen_oldpin.txt`). So the "two words fewer, 1,013 of 1,024" claim holds.
- Residual `1616fc8f` references at the head: 45 lines, listed in `receipts/published/residual_1616fc8f.txt`. Each is a dated historical record: earlier CHANGELOG entries, the #843/#851/#883 SUBMODULES records and the #883 table, AREA_BUDGET.md, MARK_II_AREA_PLAN.md:1104, the #234 finding, the `measured` strings in `pp_resource_baseline.json`, the milan_dp README's pre-#883 rows, the old ledger row and the "merged in `1616fc8f`, PR #101" sentence in STRICTER_READINGS.md:100. None of them is a current pin site.

### (2) Consumer gates pass; is the behaviour change covered at platform level?

These are my executions. Scoped Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`) ran with `MAKEFLAGS=--no-print-directory`, in two scratch clones of this head: one with every gitlink at its pin, one identical except `gptp-processor` at `1616fc8f`. The script is `scripts/run_platform_gptp.sh`, and the sanitized logs and rc files are in `receipts/published/suites_head/` and `receipts/published/suites_oldpin/`.

| Suite (target) | Head `1213ac5b` | Gitlink reverted to `1616fc8f` |
|---|---|---|
| `gptp_shadow` (`run`) | 326/326 PASS, rc 0 | 326/326 PASS, rc 0 |
| `gptp_plane` (`all`: run, phc-step, planted defects) | 31/31, phc_step 62/0, campaign 8/8, rc 0 | identical, rc 0 |
| `gptp_tables` (`run`) | 36 checks, 0 failures, rc 0 | identical, rc 0 |
| `gptp_txts` (`run`) | 95 checks, 0 failures, rc 0 | identical, rc 0 |
| `milan_dp gptp` | 212/212; `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A` | identical |
| `milan_dp gptp-lat` | 212/212; `[CA] … 0xF8FE436A` | identical |

- The control is real. The two trees built different images: 1013 against 1015 real words, BECOME@309/SELF@975 against BECOME@975/SELF@309. The runs differ observably too: `gptp_shadow` sends 25 Syncs at the head and 24 at `1616fc8f` (`receipts/published/head_vs_oldpin_logdiff.txt`). Every check still passes at both pins. This is finding F1.
- The author's published receipts agree for the head (`author/receipts/rtl/`):
  - The four shards hold 65 suites and 2,715,829 checks (361,761 + 2,046,723 + 286,399 + 20,946), with 0 in-suite failures. The `mbx` harness refusal is a missing `--no-print-directory`, re-run green with it.
  - `tsn_fuzz` field campaigns: 675 and 164 pass.
  - The physical `milan_dp_gptp` leg: rc 0, 9,301 s.
  - Their heads `39e9c9d2` and `8c5a51e1` differ from this head only in Markdown (`receipts/published/post_receipt_changes.txt`).

### (3) Routes, floor, image identity, the owner's exception

- Packet integrity: 89 of 89 files hash to `MANIFEST.json` (`receipts/published/evidence_manifest_check.txt`).
- `route/8x8-ExtraPostPlacementOpt`:
  - `utilization.txt`: Slice LUTs 46,246; base (`utilization-base-300da99b.txt`) 46,621, so -375.
  - FF 53,381 against 53,338 (+43); Slice 15,622 against 15,570 (+52); BRAM 98.5; DSP 13.
  - `signoff.txt`: worst +0.066 / +0.036 ns, 0 failing at every corner; `build.rc` 0.
  - `identity.log`: a split image whose manifest, ident, firmware, bitstream and placement agree.
- `route/1x1-ExtraTimingOpt`:
  - 32,639 against 32,680 (-41); FF 42,805 (equal); Slice 14,147 against 14,297 (-150).
  - Worst +0.170 / +0.024 ns, 0 failing; identity agrees.
- The 1x1 ExtraPostPlacementOpt image misses at +0.007 ns, and AltSpreadLogic_high reaches +0.072 / +0.024 ns. The selection is the best worst-corner WNS of three. That satisfies #818: the gate takes the three routes, or one route marked as the shipping selection (#818 body; PP_SHADOW_BASELINE_RECIPE.md:599). It also satisfies BUILDING.md:624-626 and :775-777.
- The 8x8 image is a single shipping selection that meets the floor, which #818 admits.
- The #818 floor (WNS >= +0.030 ns, WHS >= 0, BUILDING.md:617-618) is met at all four corners by both selected images.
- The base figures (+0.105 and +0.384 ns, 46,621 and 32,680) come from the train's public review comment on PR #988. Its round shows the same figures.
- The owner's decision (FPGA-gPTP PR #108 issuecomment-7121892317) measured 43,022 -> 43,477 LUT (+455) at 8x8/1if on an older parent. On this base the selected 8x8/1if image is 375 LUT smaller, so the claim "the growth does not appear" holds as a measured whole-image statement.
- The per-instance hierarchy (`hierdiff-vs-base.txt`) shows logic moving across the wrapper/engine boundary: wrapper -1,397, engine +912, plane net -294. The PR reports this rather than claiming a recovery.
- The worst paths are `KL_mbx` read data at 8x8 and the SoC bus bridge into the UART FIFO at 1x1. The 1x1 worst hold is a zero-level `chan_map_render` pair. None is in the gPTP plane.

### (4) PR body against the packet

- The live body differs from `author/PR-BODY.md` only by the added stacking paragraph, which is accurate (`receipts/published/pr_body_vs_packet.diff`).
- Every figure I checked matches its receipt: the sweep totals, the leg tallies, the route tables, the corner table, the 24 identical image digests (`ledger/image-hashes-vs-300da99b.txt`), and the docs workflow tally of 56 rc 0, 24 skipped and 3 SDK refusals.
- The wording exceptions are R2 and S1.

## Findings

### F1: MAJOR. Lenses: Tests, Robustness. No parent test grades the published behaviour change.

- **Where:** `docs/design/GPTP_PLANE.md:94-101`, `docs/design/GM_LOSS_RECOVERY.md:46-59`, `docs/reference/STRICTER_READINGS.md:108` (last column), `CHANGELOG.md:65-86`; PR body "Known limitations", fourth bullet; `receipts/published/suites_*`.
- **Authority and evidence:**
  - This PR newly publishes two platform behaviours:
    - Taking the grandmaster role always writes rate 0 to the PHC, so the time base's frequency steps by the departed grandmaster's rate at every takeover.
    - With transmit credit, the new master's Announce leaves before an Announce queued at the receipt-timeout instant re-elects.
  - The parent path is wired through. `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:784-785` latches every engine addend write, and `hdl/milan/milan_datapath.sv:3260` feeds that level to `ts_counter`. So this is the product's PHC behaviour, not only the engine's.
  - AGENTS.md section 5 requires adding or updating self-checking tests for changed behaviour. The `Tests` lens in section 6 asks for real integration wiring where practical. CONTRIBUTING section 3 says to prefer real-wiring-path tests.
  - The PR's own Definition of Done leaves "New or changed behavior has self-checking tests" unchecked, and its body says "No platform test is added".
  - The precedent adoption, #883 (`docs/reference/SUBMODULES.md:883-890`), graded its donor change in the parent's legs and showed them failing at the old pins.
  - The donor review asked for the same here. FPGA-gPTP PR #108 R905-1-S3 (issuecomment-7110828786) says to adopt the takeover phase "into the parent's regression with the gitlink bump". R906-2 (issuecomment-7122103806) retained it for the parent owner.
  - The PR defers this to "a new Issue". A search of this repository for that Issue finds none.
  - The decisive measurement: every parent gPTP consumer suite passes identically with the gitlink reverted to `1616fc8f` (table in (2)). No parent check can fail for either behaviour.
- **Impact:**
  - A later parent change could undo the takeover-rate behaviour at the platform level, or a later pin could regress it, and every parent gate would stay green. Examples: a wrapper that gates addend writes, or a PHC that ignores a rate write outside a slew.
  - The same holds for the receipt-timeout race, the ordering path Robustness covers.
  - The parent consumers of a PHC frequency step at takeover are ungraded: the media clock, CRF and uncertainty publication. The step is up to the departed grandmaster's rate, which the donor bounds at +-200 ppm.
- **Required outcome:** one of the two below.
  - A parent self-checking test, in `gptp_shadow` or the `milan_dp` gptp leg, that both:
    - drives the station as slave with a nonzero rate trim into the grandmaster role and requires the PHC adjust level (`phc_adj_o`, or the effective `ts_counter` addend) to read 0 after the takeover with no phase step;
    - places a peer Announce at the receipt-timeout instant and requires a DUT Announce carrying this station's grandmaster identity to reach the MAC, with transmit credit, before the re-election.
    - Each check must fail with the gitlink at `1616fc8f`.
  - Or a recorded owner or manager decision on #994 that donor-only grading suffices for this adoption, with the follow-up Issue opened and linked from the PR.
- **Verification:** the new checks pass at the fix head and fail in a scratch tree with only the gitlink at `1616fc8f`. Alternatively, the decision comment and the Issue link exist publicly.

### F2: MINOR. Lenses: Robustness, Docs. A retained parent-level anomaly after a takeover is untracked.

- **Where:** the PR body "Known limitations" (fourth bullet); `docs/reference/SUBMODULES.md:949-1029` (the #994 adoption record).
- **Authority and evidence:**
  - FPGA-gPTP PR #108 R905-1-S3 reports that after the -100 ppm takeover "the station sends no AECP frame for two GET_COUNTERS windows", reproducing at the donor's base. It asks for a parent Issue "so the retry does not normalise a missing AEM response".
  - R906-2 retained it "for the parent owner".
  - AGENTS.md section 4 says newly discovered work becomes another public Issue, and section 1 says project state must be public.
  - No Issue in this repository tracks it (searches for "takeover" and "mastership" return #994 only for this subject). Neither the PR nor the adoption record mentions it.
  - I did not reproduce the anomaly. The finding is the missing public tracking, which the adopting lane owes now that it carries the pin the observation was made against.
- **Impact:** a controller-visible AEM silence after a grandmaster takeover at a large rate offset stays private to the donor thread. It concerns exactly the transition this adoption changes.
- **Required outcome:** a parent Issue that records the reproduction and the donor receipts it came from, linked from the PR's known limitations.
- **Verification:** the Issue exists and the PR body links it.

### R1: RESIDUE. Lens: Docs. The adoption record states the selection rule loosely.

- **Where:** `docs/reference/SUBMODULES.md:982-988`.
- **Evidence:**
  - The text reads "Each image takes the first that meets the build floor. At 1x1 the first missed, as on the base. So all three were routed there."
  - The image actually selected at 1x1 is the best worst-corner WNS of the three (ExtraTimingOpt +0.170 ns), which is the #818 / BUILDING.md:624-626 rule. Under a literal "first that meets", in the recipe order (`sw/litex/build.sh:424`, `syn/ooc/pp_resource_gate.py:133`: ExtraPostPlacementOpt, AltSpreadLogic_high, ExtraTimingOpt), AltSpreadLogic_high would have shipped.
  - The table, the figures and the selection are correct, so this is wording.
- **Exact fix:** replace line 984 with "An image meeting the floor on the first directive ships from it." Replace line 988 with "Otherwise all three are routed; the best worst-corner WNS ships (#818)."
- Keep each sentence within the style gate's ten words, and re-run `check_doc_style.py`.

### R2: RESIDUE. Lens: Docs. The PR body names the wrong directive order.

- **Where:** PR body, "The release routes", first paragraph.
- **Evidence:** it says the recipe's order is "ExtraPostPlacementOpt, ExtraTimingOpt, AltSpreadLogic_high", and the recipe order is ExtraPostPlacementOpt, AltSpreadLogic_high, ExtraTimingOpt (the same two sources as R1). The 1x1 selection is best of three, so no figure or selection changes.
- **Exact fix:** "in the recipe's order, ExtraPostPlacementOpt, AltSpreadLogic_high, ExtraTimingOpt; an image meeting the floor on the first directive ships from it, otherwise the best worst-corner WNS of the three ships."

### R3: RESIDUE. Lens: Docs. The figure citation has no edition.

- **Where:** `CHANGELOG.md:71`, "The 1 s cadence counts from that Announce (Figure 10-15)."
- **Evidence:** the same entry cites "802.1AS-2020 10.1.2.1" two lines later. The figure meant is IEEE 802.1AS-2011 Figure 10-15, as `SUBMODULES.md` and the PR body say.
- **Exact fix:** "The 1 s cadence counts from it (802.1AS-2011 Figure 10-15)." Re-run `check_doc_style.py`.

### S1: SUGGESTION. Lens: Docs. Explain the second signoff line in the receipts.

- `author/receipts/route/1x1-ExtraTimingOpt/signoff.txt` (and `chain.log`) prints "ruling floors NOT met" and rc=1 for the selected 1x1 image.
- That second line is the author tool's check of #870's lane-specific gate (issuecomment-6779934014 item 4: WHS >= +0.030 ns). It is not the #818 floor this Issue names, which the image meets.
- One sentence in the PR stating this would stop a cold reader from taking rc=1 as a floor miss. It would also note that the 1x1 WHS fell 0.012 ns, to +0.024 ns.

## Clean-lens lines

```text
[R915] PASS Conformance - #994 AC1-AC3; gptp-processor gitlink; syn/yosys/rom_digests.tsv:17; docs/reference/SUBMODULES.md:24; receipts/published/doc_gates_head.txt, romgen_head.txt, donor_identity.txt, residual_1616fc8f.txt; author/receipts/route/{8x8-ExtraPostPlacementOpt,1x1-ExtraTimingOpt}/{utilization,signoff,identity}; receipts/published/suites_head/* - AC1 every current pin site names 1213ac5b (three checkers plus an independent grep of 45 historical residuals); AC2 consumer suites and both milan_dp legs pass (my reruns plus the author's sweep); AC3 both images fit and meet #818 at all four corners, and the 8x8/1if total is recorded against the base (-375). The owner's +455 is checked against the receipts. The doc claims (rate 0 at BECOME, the TLV as the negated estimate, the first Announce from SELF->ANNTX with the role, asCapable and credit gates kept, re-arm before the gates) match the donor RTL and ucode at 1213ac5b.
[R915] PASS RTL - gptp-processor 1616fc8f..1213ac5b hdl/top/KL_gptp_engine.sv (word-3 write now unconditional; slave_rate_seen_r set by PHC word 0, cleared by BECOME, set wins; tlv_dlt_r 25-bit from st_wdata_w[63:32]; reset values) and hdl/ucode/gen_gptp_ucode.py (prog_become, prog_self BR ANNTX, prog_leg_anntx re-arm before the gates); parent hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:717-718,784-785 and hdl/milan/milan_datapath.sv:1831,3260,9265,9363 - no engine port or parameter change, so the parent wrapper and datapath contracts hold. Every addend write reaches ts_counter as a level. The ROM stays 1024 words, 1013 real. The parent RTL is unchanged in the delta, and the routes show no gPTP-plane critical path.
```

The Tests, Robustness and Docs lenses were applied and are UNCLEAN.

- **Tests (F1):** I examined the six suites at both pins (logs in `receipts/published/suites_*`), the author's sweep, leg and physical receipts, and the check inventory of `tb/verilator/milan_dp/sim_gptp.cpp` (`[CA]`, the ungated become-master hold at :994-997, the #89 aging at :1607) and of `sim_ax1x1gptp.cpp:1067-1107`. That Sync-loss takeover grades the holdover of the time-uncertain (tu) flag and the audio path, not the PHC rate or the Announce race.
- **Robustness (F1, F2):** the receipt-timeout ordering race, the PHC frequency step at takeover, the ANNTX credit-gate retry (re-arm before the gates, so a skipped beat retries 1 s later, which holds), and reset values of `slave_rate_seen_r`.
- **Docs (F2, R1 to R3):** every changed page in the delta was checked against the donor RTL and the receipts, and the docs gates were run.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #994 AC1-AC3; gitlink and donor ancestry; `rom_digests.tsv:17` against regeneration; pin-site checkers; residual grep; the route receipts; #818 and BUILDING.md section 5; the owner decision | R915-1 | `bbfdb6746d585e490508783dc8a88c79fbab02c0` |
| RTL | CLEAN | Donor `KL_gptp_engine.sv` and `gen_gptp_ucode.py` delta; parent `KL_gptp_shadow.sv:784-785`, `milan_datapath.sv:3260`; ROM shape; route worst paths | R915-1 | `bbfdb6746d585e490508783dc8a88c79fbab02c0` |
| Robustness | UNCLEAN (F1, F2) | Takeover race, PHC rate step at takeover, credit-gate retry, reset of the seen flag; donor R905-1-S3 observation | R915-1 | `bbfdb6746d585e490508783dc8a88c79fbab02c0` |
| Tests | UNCLEAN (F1) | Six parent suites at the head and with the gitlink reverted to `1616fc8f`; the author's sweep, leg and physical receipts; `sim_gptp.cpp`, `sim_ax1x1gptp.cpp` check inventories | R915-1 | `bbfdb6746d585e490508783dc8a88c79fbab02c0` |
| Docs | UNCLEAN (F2; R1-R3 are residue only) | CHANGELOG, GM_LOSS_RECOVERY, GPTP_PLANE, TIME_SYNC, STRICTER_READINGS, SUBMODULES, the four guides, the traceability page, both diagrams and the manifest; PR body against the packet; docs gates | R915-1 | `bbfdb6746d585e490508783dc8a88c79fbab02c0` |

## Real limits

- I did not run Vivado. The route figures, corners and image identity are the author's receipts, checked file by file against the packet manifest, not re-derived from raw reports.
- I did not run the physical `milan_dp_gptp` leg (about 2.6 h on this host) at either pin. Its head result is the author's receipt (rc 0). Whether it passes at `1616fc8f` is untested by me.
- I did not run the full sweep, the builder bank, `plat_ledger`, Yosys/OOC or `ooc.sh --record-rom-digests`. The ROM row is checked by independent regeneration instead.
- `check_em_dash.py` and `gen_toc.py` refused on this host: the pinned Markdown renderer is not installed. Instead I scanned the added lines for U+2014 and found 0 (`receipts/published/emdash_check.txt`). The author's head receipt records both gates rc 0.
- I did not open the IEEE 802.1AS text. Clause numbers are checked for consistency against the donor's ruling and RTL, not against the standard.
- The anomaly in F2 is the donor reviewers' published observation, which I did not reproduce.
- Hosted CI at this head, snapshot 2026-11-24T10:41Z (`receipts/published/hosted_checkruns_final.txt`): 57 check runs. 31 succeeded, 20 were in progress, 5 queued, and 1 skipped ("Physical gPTP (nightly and manual)", a skipped context, not an execution). It is not complete, and its acceptance stays with the manager.
- No manager source bank ran at this head, and none is claimed or inferred. Physical calibration was NOT RUN, field skips are not hardware proof, and no hardware was used.
- For context I read FPGA-gPTP PR #108's public review comments: R905-1, R906-1/2 and the owner decision, which the Issue and PR cite as authority. These are reviews of the donor PR, not of PR #995.

## Pending manager duties

- Build and validate the current-dev merge candidate: source base `300da99beed5bb1c77e4b04af0bb4f9369856e0d`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, builder and native banks. Link its receipts on the PR.
- Hosted and act acceptance at the exact head, including the exhaustive Verilator and Yosys contexts still running at the snapshot.
- Carry R1 to R3 to the residue checklist.
- Route F1 and F2 to the executor for a fix head or a recorded decision. A fix head needs a new review round over every lens its change touches.

## Prior public findings on this PR

I read the PR discussion after the verdict and ledger above were written. It holds two review-start comments and one prior review, the external round's `[R916] NEGATIVE` at this same head (issuecomment-7128636852). It has no formal reviews and no inline comments. #994 has no comments.

### R916-1-F1 (MAJOR): RETAINED, concurred

- This is the same defect as my F1, reached independently. My evidence reverts the whole gitlink to `1616fc8f`. R916's evidence is two targeted disposable faults (the delayed first Announce, and a rate write applied only during a slew), both green in the parent `gptp_plane` and `gptp_shadow` runs.
- R916 records it under Conformance, Robustness and Tests. I record F1 under Tests and Robustness. #994's frozen acceptance criteria are each met, so I do not hold Conformance unclean on it.
- Under AGENTS.md section 6, a finding attributable to several lenses is recorded under each. So the conservative reading for the completion ledger is the union: Conformance, Robustness and Tests, none of them covered clean until F1 is fixed and re-reviewed.
- The verdict is NEGATIVE either way.

### R916-1-R1 (RESIDUE, Docs): RETAINED, verified

- The PR body's commit table, `973f2f20` row, says "the two later commits change no synthesis input". `git log 973f2f20..bbfdb674` lists three commits.
- The conclusion itself holds (`receipts/published/post_receipt_changes.txt`: only Markdown, diagrams and the ROM ledger change). The ledger is not a Vivado input.
- Exact fix: "the three later commits". It goes on the residue checklist with R1 to R3 above.

My F2, R1, R2, R3 and S1 do not appear in R916. They stand as written above. My own verdict, findings and ledger were not changed by reading R916.

R915-1 FINISHED
