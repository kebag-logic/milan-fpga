[A744] REVIEW READY
Commit: 2d939d2dcb9664c08f7d2dc7b584987a1e0c0f8a (branch 851-adopt-pp-044cb25f, on dev 1eb5289d; not pushed by this session)
Changed: the protocol-processor gitlink 92100657 -> 044cb25f (processor PR #215, issue #214: each attribute value at most once per MRPDU; only hdl/srp/KL_srp_encoder.sv changes, no port or parameter change). ROM digests re-recorded by ./syn/yosys/ooc.sh --record-rom-digests (both images equal the 92100657 rows); pin-table row and boundary diagram by their generator; syn/ooc/pp_resource_baseline.json re-recorded by pp_resource_gate.py record --write under the maintainer decision of 2026-11-06; pin page, CHANGELOG, integration contract, the fourteenth resource record in the area pages; documentation audit by its generator. No synthesis input changes after a566d4f9.
Validation (each group on a clean clone of the head, every rc 0):
- full sweep, four shards: 65 suites passed, 0 failed, 0 timed out, 2,192,502 checks, 0 in-suite failures; capture_coherence on 4 CPUs, about 2,100 s of 2,400; no preflight failure
- firmware self-test, shards 0/4 to 3/4: test_ctrl_firmware PASS each (control campaign 523 of 523; shard 3 holds both SRP campaigns); fw_coverage.py --check PASS (30 files); test_ctrl_nvm, fw_rv32_selftest, tally and SDK self-tests, both ctrl_boundary legs PASS
- test_builder.py --require-rv32: ALL GATES PASS EXCEPT 17 NOT RUN; with the LiteX interpreter: EXCEPT 2 NOT RUN
- cd tests && behave: 14 features, 508 scenarios, 2,330 steps passed
- every run: step of docs.yml on fresh clones: 65 rc 0, 31 not run with a stated reason, 0 bad; docs_inventory.py --check fresh; git diff --check 1eb5289d HEAD clean
- rtl-fast steps (lint 89 <= 89, pp_srcs, yosys elaborate, ooc/guard/cache self-tests, publication census), check_cpp_idiom.py 0 <= 0 for every rule, xvlog gate, ROM recorder reproduces the committed rows
- milan_dp crflic-mutants 10 of 10, gsi-mutants 15 of 15, unb-mutants 6 of 6; every recorded campaign count unchanged
- shipping route, AX7101 1x1 TDM8, one directive (ExtraPostPlacementOpt), under the Vivado slot: 53,033 LUT, 54,729 FF, 15,792 of 15,850 slices (58 free), WNS +0.044 ns, WHS +0.035 ns, 0 routing errors; the run at the head equals the run at a566d4f9 in every figure
- resource gate (recipe form): route-1x1 rc 1 against the thirteenth record, LUT 53,050 (+521 of +500), ExtraTimingOpt selected at WNS +0.258 ns; ooc-1x1 (+203 of +250) and ooc-8x8 (+184 of +316) rc 0. All three re-recorded; check rc 0 on each and check-baseline rc 0 afterwards
Acceptance criteria: met. The full sweep, the firmware self-test, the builder, behave, the docs gates and the docs inventory are green; the route fits and meets the WNS floor at every corner.
Open risks/questions:
1. Both standalone endpoints were re-recorded although they passed, so the record holds one processor pin as every earlier record does; re-recording the route alone is the alternative if review prefers it.
2. The adoption's own share of the route growth is not measured: no route of dev 1eb5289d exists on this recipe, so the route deltas include dev's PRs #841 and #842.
3. The one-directive route meets the WNS floor by 0.014 ns; the gate's AltSpreadLogic_high comparison misses it by 0.002 ns; the selected ExtraTimingOpt route has 0.228 ns and 19 slices left.
4. PR #846 (the gPTP pin) touches the same baseline and area pages; whichever merges second re-measures on the other.
