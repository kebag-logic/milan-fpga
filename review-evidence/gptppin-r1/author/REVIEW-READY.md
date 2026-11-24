[A835] REVIEW READY
Commit: bbfdb6746d585e490508783dc8a88c79fbab02c0 (branch 994-gptp-pin-1213ac5b, 4 commits on 300da99beed5bb1c77e4b04af0bb4f9369856e0d; PR base dev-soft-core)

Changed:
- `gptp-processor` gitlink 1616fc8f -> 1213ac5b9e09b8759ba76cc70c53652b5e108996 (FPGA-gPTP PR #108: #106 first master Announce at once,
  #107 each mastership on this oscillator; plus #103/#105, test infrastructure only). 1213ac5b's tree 7b579e33 = the reviewed head
  331e27de's tree (R905-2 and R906-2 POSITIVE at that head). No engine port/parameter/generator-option change.
- Pin sites (`39e9c9d2`): SUBMODULES pin row; every engine-guide permalink (GPTP_PLANE, TIME_SYNC, docs/guides/gptp x4,
  traceability/ieee8021as, the SUBMODULES conflict list); submodule_boundaries and timesync_chain diagrams by their generators;
  rom_digests.tsv's gptp_ucode.hex row by `ooc.sh --record-rom-digests` (4eb21cef..., the donor's tracked image).
  Historical records naming 1616fc8f stay.
- Behaviour docs and records (`8c5a51e1`, `bbfdb674`): GPTP_PLANE (the mastership's rate-0 PHC write), GM_LOSS_RECOVERY (first
  Announce at once, mastership on this oscillator), STRICTER_READINGS (the Announce-at-the-instant row at 1213ac5b), SUBMODULES
  #994 adoption record with the route figures, CHANGELOG. `bbfdb674` only shortens sentences for the style gate.

Validation (sweep, legs and gates on clean clones; the code-relevant tree is identical from 973f2f20 to bbfdb674: later commits
change Markdown only):
- Routes (release recipe, split image, one interface; at 973f2f20; <=2 at once via the slot script; MemAvailable >= 20 GB):
  - 8x8/1if ExtraPostPlacementOpt (first directive, meets): WNS/WHS worst +0.066/+0.036 ns; 46,246 LUT, 53,381 FF, 15,622 slices,
    98.5 BRAM tiles, 13 DSP. Base 300da99b (its inputs routed at c2b2ba1a): 46,621 / 53,338 / 15,570 / 98.5 / 13, +0.105/+0.036.
    Change -375 LUT, +43 FF, +52 slices, BRAM/DSP 0.
  - 1x1/1if: ExtraPostPlacementOpt misses (+0.007 ns; the base's missed too, +0.019), so best of 3: ExtraTimingOpt selected
    +0.170/+0.024 ns, 32,639 LUT, 42,805 FF, 14,147 slices, 80.5, 13 (AltSpreadLogic_high +0.072/+0.024, 32,633 LUT).
    Base ExtraTimingOpt 32,680 / 42,805 / 14,297 / 80.5 / 13, +0.384/+0.036. Change -41 LUT, 0 FF, -150 slices.
  - #818 floor (WNS >= +0.030, WHS >= 0 at every corner) met by both selected images; 0 failing endpoints, no routing error;
    image identity PASS on all four images. No growth: the owner-accepted +455 LUT at 8x8/1if (FPGA-gPTP PR #108
    issuecomment-7121892317) does not appear on this base. No STOP condition.
- Full sweep at 8c5a51e1, `scripts/run_all_suites.sh --wait --shard K/4`, K = 0..3: 65 suites, 2,715,829 checks, 0 in-suite
  failures. 64 PASS in the sweep; `mbx` failed only in its dma-mutants harness (make's 'Entering directory' line parsed as a
  path: this harness lacked the CI's MAKEFLAGS --no-print-directory) and passes re-run alone with that flag (523,212 checks,
  0 failures). Shard 2 was OOM-killed once at a 12 GB cap in capture_coherence (peak 16.9 GB) and passed whole on re-run.
  The gPTP consumers in it: gptp_plane 101, gptp_shadow 326, gptp_tables 36, gptp_txts 285, milan_dp 14,379,
  milan_dp_gm_steps 202, clkvalid 55, ptp 201,308, ptp_sync 30, ptp_ts 495, capture_coherence 21,721, fw_service_budget 74.
- tsn_fuzz with its tsn-gen field campaigns (the sweep's environment skipped them): rc 0, 897 checks; gPTP/802.1AS campaign
  675 pass, 0 fail, AAF/AVTP 164 pass, 0 fail, equal to the tracked TEST_RESULTS.md (only their timestamps move; not committed).
- milan_dp gptp 212/212 (`[CA]` 0xF822436A, clockAccuracy 0x22) and gptp-lat 212/212 (0xF8FE436A, 0xFE), at 39e9c9d2.
- milan_dp_gptp (physical, --physical-gptp's suite) at 39e9c9d2: PASS, 205 checks (151 + 6 + 20 + 14 + 14), 0 failures; 9,301 s
  wall on the loaded shared pool, over the runner's 6,900 s default (run under an 18,000 s cap).
- plat_ledger at 39e9c9d2: PASS, 0 findings at every point; all 24 firmware image digests equal the base 300da99b's, so no
  firmware input moves and the firmware gate's four shards are not owed.
- Builder: legs 0 and 1 (test_builder.py --require-rv32) rc 0, each "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 1b's MAKEFLAGS arm,
  gate 11's absent calibration tree: dev's two), union "113 gates exactly once", at 39e9c9d2; both legs pass again inside the
  docs workflow at bbfdb674.
- Docs workflow, every `run:` step at bbfdb674: 56 rc 0, 24 SKIP (installs, hosted recorders), 3 refusals that are this host's
  RV32 SDK install-verify ("missing regular SDK provenance receipt", as on the train's bases). Style gate 0 findings (18 at
  8c5a51e1, fixed in bbfdb674); em-dash 0 over 152 added lines; imported gPTP docs, submodule docs, diagram no-drift, traceability
  all rc 0.
- Hosted-gate equivalents at bbfdb674: lint_rtl.py --check --self-test rc 0; Yosys elaborate of milan_datapath, KL_pp_shadow,
  KL_gptp_shadow PASS; Yosys open synthesis of KL_gptp_txticket, KL_gptp_txret, KL_gptp_gmii_launch, KL_gptp_shadow and milan_datapath PASS;
  ooc_selftest.py rc 0; milan_dp split-cdc rc 0 (13 checks).
- `git diff --check 300da99b HEAD` clean.

Acceptance criteria (#994):
1. Every pin site names 1213ac5b: MET (pin row, permalinks, diagrams, ROM ledger row; check_submodule_docs "6 exact gitlinks",
   check_gptp_docs "8 current pages").
2. The gPTP consumer suites and the milan_dp gptp/gptp-lat legs pass: MET (above).
3. Both routes fit and meet the #818 floor; the 8x8/1if LUT total is recorded against the base: MET (46,246 vs 46,621).

Open risks/questions:
- The resource gate's endpoints (all-fabric route-1x1, ooc-1x1, ooc-8x8) were not re-measured; the issue names the release
  images. Say so if a reviewer wants route-1x1 re-recorded.
- No platform test grades #106/#107 directly; the donor grades them (phases 57-61, nine planted defects). The donor review's
  suggestion to adopt a +-100 ppm takeover phase into the parent regression is follow-up for a new Issue.
- Receipts: receipts/INDEX.md.
