[A744b] REVIEW READY
Commit: dafd49c1f9b79d3cc29534a9ab43d98360079d2b (branch 851-adopt-pp-044cb25f, round 2 on round 1's 2d939d2d; merge base dev 0a75aa77; not pushed by this session)
Changed:
- sync: git merge --no-ff origin/dev 0a75aa77 (PR #846, FPGA-gPTP 1616fc8f) as e44a4d20, no rebase; both adoptions kept in the pin table, the pin page and the area pages; the baseline JSON taken from this side and re-recorded by its recorder; the boundary diagram and manifest by their generator; the ROM ledger reproduced by its recorder
- R790-S1: milan_dp's crflic leg grades [ONEVEC], every MSRP and MVRP MRPDU the DUT sends carries each attribute value at most once (IEEE 802.1Q-2022 10.7.7, 10.7.5.13 c), 10.8.2.10.1; increments 35.2.2.8 a), 35.2.2.9, 11.2.3.1.7); crflic-mutants plants an encoder that never merges, which fails "no DUT MRPDU carries one attribute value in two VectorAttributes (802.1Q-2022 10.7.7, 10.7.5.13 c)) got=3 exp=0"
- R789-F1 = R790-F1: every committed timing path now comes from report_timing of the routed checkpoint, worst setup and hold per corner, each excerpt's slack checked equal to that corner's WNS/WHS; round 1's five checkpoints reported the same way (its path figures were right; its worst-setup-path receipt was not the worst path); the #841 daily-route figure removed
- R789-F2 = R790-S2: the adoption's share stated as measured: on dev 1eb5289d +77 LUT, +134 FF, +14 slices (ExtraTimingOpt both); on dev 0a75aa77 against #843's record +207 LUT, +83 FF, -5 slices, 0 DSP, WNS -0.032 ns (AltSpreadLogic_high both)
- R789-S1 = R790-RS1: one "All these measurements use the same recipe identity and policy."
- the combined route (all four lab fixes) at e44a4d20, recipe form, the three directives one at a time under the Vivado slot; route-1x1, ooc-1x1 and ooc-8x8 re-recorded by pp_resource_gate.py record --write; the fifteenth record on the pin page, the CHANGELOG and the area pages
Validation (each group on a clean clone of the head, every rc 0):
- full sweep, four shards: 65 suites passed, 0 failed, 0 timed out, 2,192,512 checks, 0 in-suite failures; suite cancellation PASS in every preflight (no #833 case); capture_coherence on 4 CPUs, about 2,342 s of 2,400; milan_dp's [ONEVEC] 0 doubled over 285 MSRP and 184 MVRP MRPDUs
- firmware self-test, shards 0/4 to 3/4: test_ctrl_firmware PASS each (control campaign 523 of 523); fw_coverage.py --check PASS (30 files); tally, SDK (verified), fw_rv32 and ctrl_nvm self-tests and both ctrl_boundary legs PASS
- test_builder.py --require-rv32: ALL GATES PASS EXCEPT 17 NOT RUN; with the LiteX interpreter: EXCEPT 2 NOT RUN
- cd tests && behave: 14 features, 508 scenarios, 2,330 steps passed
- every run: step of docs.yml on fresh clones: 65 rc 0, 31 not run with a stated reason, 0 bad, every tree clean; the act runner contract gate and act_ci.py --selftest PASS; docs_inventory.py --check fresh; git diff --check 0a75aa77 HEAD clean
- rtl-fast steps (lint 89 <= 89, pp_srcs, yosys elaborate, ooc/guard/cache self-tests, publication census), check_cpp_idiom.py and check_py_idiom.py within every ratchet, xvlog gate, ROM recorder reproduces the committed rows
- milan_dp crflic-mutants 11 of 11 (the new encoder arm caught), gsi-mutants 15 of 15, unb-mutants 6 of 6; every recorded campaign count unchanged
- shipping route at e44a4d20 (later commits change no synthesis input): AltSpreadLogic_high selected, 53,428 LUT, 54,837 FF, 15,829 of 15,850 slices (21 free), 87.5 BRAM tiles, 15 DSP, WNS +0.210 ns, WHS +0.036 ns, 0 routing errors; ExtraPostPlacementOpt +0.112 ns (2 slices free); ExtraTimingOpt +0.018 ns, under the WNS floor at its slow corners
- resource gate: against dev's fourteenth record check rc 0 on all three endpoints (route +207 of +500 LUT; ooc-1x1 +203 of +250; ooc-8x8 +184 of +316); after the re-record check rc 0 on each and check-baseline rc 0; no tolerance, floor or ceiling moved
Acceptance criteria: met. The full sweep, the firmware self-test, the builder, behave, the docs gates and the docs inventory are green; the route fits and meets the WNS floor at every corner on its best directive.
Open risks/questions:
1. All three endpoints were re-recorded although the gate passes all three against dev's record, so the record measures the merged tree; no decision is needed for it.
2. The route is the recipe's three-directive route set, the seed selection BUILDING.md section 5 names, as PR #846 measured its shipping route; no bitstream was built. The release build takes AltSpreadLogic_high.
3. capture_coherence passed with about 58 s of its 2,400 s budget left on 4 CPUs of a loaded host.
4. The shared RV32 SDK the firmware gates first used was deleted mid-run by something outside this lane; every firmware group was re-run on fresh clones with a verified SDK installed in this lane's gate HOME, and only the re-runs are reported.
