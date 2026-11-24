[A835] REVIEW READY
Commit: f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 (branch 994-gptp-pin-1213ac5b; PR #995 against dev-soft-core)

Delta from round 1's head bbfdb6746d585e490508783dc8a88c79fbab02c0: three commits, eight paths, all under tb/verilator/gptp_shadow or Markdown.
- 3a8bdbf0 merges dev-soft-core at 2509db68 (the #988 train's merge, second parent 300da99b). Its tree eb8282df equals bbfdb674's, so the merge changes no file.
- d616b1c6: the platform regression (R916-1-F1 and R915-1-F1, MAJOR).
- f97e49fe: the records (R915-1-F2, R915-1-R1 and R3; R916-1-R1, R915-1-R2 and S1 are in PR-BODY.md).

Changed:
- tb/verilator/gptp_shadow/sim_main.cpp: three phases at the end of the run, through the slice's transport and the real timestamp_counter. Each starts from a quiet master (unsealed, capable, no egress result owed) and otherwise records why and grades nothing further.
  - 18, #107: four masterships by the sync receipt timeout, from slaves settled at +100 ppm and -100 ppm, a -100 ppm slave mid-slew (1,500 ns), and an elected grandmaster lost before any pair. Each: latched rate 0, slew retired, no adjtime, the real counter advancing exactly 8 ns a clock. The TLV: gmTimeBaseIndicator +1, lastGmPhaseChange the last slave offset, and scaledLastGmFreqChange rate 0 less the settled trim (5 %, both signs), nonzero after the slewing slave, 0 with no slave rate since the last mastership.
  - 19, #106: GMID's 1 s Announce, then its pairs only. The announce receipt timeout makes the plane master 3 s after it. The first master Announce leaves at once (ends 285 clocks after the instant; < 2,000 required; the deferred beat is 4,000), and two more follow 1 s apart. Race: GMID's next Announce exactly 3.000 s after the elect, at the same millisecond phase. The plane is master at the instant, exactly one master Announce reaches the lane, then that Announce re-elects GMID (within 2 ms).
  - 20, #106: the credit is withheld by the ledger's seal (a generation-zero record's barrier, the observer held in reset) across a sync-receipt takeover. No master Announce while sealed; released, the first leaves 1 s after the instant ([2,000,000, 2,002,000) clocks), and the next 1 s after it.
  - Harness: every frame's last-beat clock, every published master-bit edge, the adjtime count. The aged-head phase now drops rechold_en_i before its release pulse; before, the release re-armed the gate, which then held the next Pdelay_Req record for good. That was harmless only while the phase was last.
- gptp_shadow_wrap.sv: two observation outputs, dbg_phc_slew_o (the slice's phc_slew_active_o, unconnected before) and dbg_phc_step_v_o. No product RTL changes; gptp_tables and tsn_fuzz build this wrapper and leave both unconnected.
- mutants.py: two controls with the donor's anchors (FPGA-gPTP p106_mutants.py, p107_mutants.py). `first_master_announce_waits_for_a_beat` (generator: SELF ends in END, BECOME arms a 2 ms beat) must fail "#106 race: one master Announce reaches the lane before the re-election". `word3_applies_only_during_a_slew` (engine) must fail "#107 settled +100 ppm: the mastership's PHC rate is this oscillator's, 0". A control may give a tuple of anchors (planted()).
- test_mutant_lifecycle.py: installs the real bytes of a dependency file a control plants in; hashes through planted(); expects 11 controls.
- README.md (gptp_shadow): phases 18 to 20 and the two controls. docs/guides/gptp/TEST_DEVELOPER.md: gptp_shadow's boundary row.
- docs/reference/SUBMODULES.md #994 record: the regression paragraph; #997 linked (R915-1-F2). The selection rule follows R915-1-R1; see the open question below.
- CHANGELOG.md: the regression and #997; the figure citation names its edition (R915-1-R3).

Validation (pinned Verilator 5.050; clean shared clones; host load 110 to 165 on 96 CPUs; receipts/INDEX.md):
- gptp_shadow at f97e49fe: `make run` 408 checks, 0 FAIL (326 at bbfdb674). `make lifecycle`: "mutant lifecycle: PASS (... eleven named defects ...)".
- gptp_shadow campaign, `mutants.py`'s own main() in three slices of MUTATIONS (tools/mutants_slice.py; the whole list exceeds one ten-minute window) at d616b1c6, whose campaign inputs equal f97e49fe's: 4 + 4 + 3 = 11 controls, 0 failures. The new two: caught by "#106 race: one master Announce reaches the lane before the re-election" and by "#107 settled +100 ppm: the mastership's PHC rate is this oscillator's, 0".
- R916-1's own disposable patches at f97e49fe (tools/probe_r916.py): control 408/408 rc 0.
  - delayed-announce rc 2, 4 FAIL: "#106: the first master Announce leaves at once", "#106 race: one master Announce reaches the lane before the re-election", "#106 credit: two master Announces once the credit returns" and "#106 credit: the withheld Announce leaves 1 s after the instant".
  - retained-slave-rate rc 2, 4 FAIL: "#107 settled +100 ppm: the mastership's PHC rate is this oscillator's, 0" (0x345a), its "real counter advances 8 ns a clock", and both again for -100 ppm (0xffffcb86).
- gptp_plane: run 31/31. phc-step: clean 62 checks 0 failures, and all 8 arms pass: 4 in `make phc-step`'s window, 4 through phc_step_slice.py (phc_step.py plus an arm filter).
- gptp_tables: limits rc 0, run 36 checks 0 failures, mutants 13 + 13 = 26 controls, 0 failures (two slices).
- gptp_txts: `make` rc 0, controls 13, failures 0.
- tsn_fuzz with TSN_GEN_ROOT at tsn-gen deca300c: rc 0, gPTP 675 pass and AAF/AVTP 164 pass. Only the two TEST_RESULTS.md timestamps moved, restored in the clone and not committed.
- milan_dp gptp 212/212, [CA] 0xF822436A. gptp-lat 212/212, [CA] 0xF8FE436A.
- lint_rtl.py --check --self-test: PASS (89 <= 89).
- Docs workflow at f97e49fe, every run: step in ten-minute windows (tools/docs_steps.py, em-dash base 2509db68): all rc 0, including the em-dash (0 findings over 195 added lines), style, SV/C/C++/Python/shell idiom, test-evidence, cited-path, TOC and inventory gates. Three RV32 SDK install-verify refusals ("missing regular SDK provenance receipt"), as on every base. NOT RUN: both builder legs and docs-gates-0's compiler-absent firmware controls. Each exceeds a window, and none reads a changed path: sw/builder/test_builder.py names no tb/verilator/gptp_shadow file and no changed page. Round 1 passed all three at bbfdb674.
- Image inputs (item 4): unchanged, so nothing was re-routed.
  - From 973f2f20 (the routed commit) to f97e49fe, every changed path is under docs/, a *.md, tb/, or syn/yosys/rom_digests.tsv (the ledger). The gitlinks are identical.
  - Outside tb/, only check_gptp_docs.py, measure_test_evidence_readers.py and docs_inventory.json name tb/verilator/gptp_shadow. None is a build, synthesis or firmware reader.
  - The regenerated default gptp_ucode.hex is 4eb21cef..., the ledger row.
  - plat_ledger at f97e49fe: PASS, 0 findings, and the 24 image digests equal round 1's at 39e9c9d2 (ledger/image-hashes-vs-round1.txt).
- `git diff --check 2509db68 HEAD` clean.

Acceptance criteria (#994, frozen): 1 MET (no pin site moved; check_submodule_docs "6 exact gitlinks", check_gptp_docs "8 current pages"). 2 MET (above). 3 MET (round 1's routes; no synthesis input changed since 973f2f20).

Findings addressed: R916-1-F1 and R915-1-F1 (MAJOR): the platform regression and both planted defects. R915-1-F2 (MINOR): #997 linked from the PR's known limitations and the #994 record. R916-1-R1, R915-1-R1, R2 and R3, and S1: done.

Open risks/questions:
- R915-1-R1's exact sentences have 12 and 11 words; check_doc_style.py allows 10, and R1 also asks for its gate. Kept R915's words: "An image meeting the floor on the first directive ships." (dropped "from it"), and the second split at its semicolon into "Otherwise all three are routed." and "The best worst-corner WNS ships (#818)." The style gate passes. R915's R3 sentence (11 words) reads "The 1 s cadence starts there (802.1AS-2011 Figure 10-15)." Reviewer to confirm.
- R916-1-R1's exact text ("the three later commits") is stale after this round's commits. The table now says "the six later commits", which is the count from 973f2f20 to the head.
- gptp_shadow's runtime about doubles (simulation 47 s at bbfdb674 against 94 s at the head, same loaded host), and its default target runs it 12 times. scripts/suite_shards.py still registers 393 s (measured hosted). That needs a hosted re-measurement for the worker balance; the 1,800 s suite timeout is far off. Not edited here: the table is measured data.
- Pre-existing, not changed: the credit_never_withheld control's expected name ("credit: the engine is held off at the reserve") matches no check in sim_main.cpp. At bbfdb674 and at the head it is "caught, though not by" that name. Worth its own Issue.
- R916-1's "cover ... both rate signs": both signs are graded settled. The slewing case is -100 ppm only. Its TLV frequency is graded as present, not against a value, because the slewing pair itself moves the integrator.
