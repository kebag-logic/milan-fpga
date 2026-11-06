[A738] REVIEW READY
Commit: 519d9c2be139d2f777127a4aa19ea9ed251392a5
Changed: the protocol-processor gitlink a9e84b66 -> 92100657, its pin-derived records (ROM ledger through its recorder, pin table, boundary diagram), the pin page, CHANGELOG and integration contract, pp_shadow row U and the documentation inventory. New since the STOP, per the manager's ruling on it: a test-only commit re-anchors the first arm of `unb-mutants` from `arb_req_w` to `arb_want_w` (the lane's request since processor #203) and records that campaign at 499 checks. What the arm plants is unchanged.
Validation, every gate on a clean clone of this exact head:
- Full sweep, 4 shards: rc 0 each, 65 suites passed, 0 failed, 0 timed out; 2,192,435 checks, 0 in-suite failures. No #833 preflight failure.
- `make -C tb/verilator/milan_dp unb-mutants`: 6 checks, 6 PASS, 0 FAIL, clean leg 499 of 499. The first arm fails exactly its four named U2 order checks (to A and to B, on the AAF input and the CRF input), 4 of 499, and its four holds pass. `gsi-mutants`: 15 of 15.
- Firmware self-test: rc 0, all four shards PASS, 523 of 523 control mutants caught. `fw_coverage.py --check`: PASS, 30 files.
- `test_builder.py --require-rv32`: rc 0, "ALL GATES PASS EXCEPT 17 NOT RUN" (2 not run with a LiteX interpreter).
- `cd tests && behave`: 14 features, 508 scenarios, 2,330 steps passed.
- `docs.yml`: verifier rc 0, 72 steps ran rc 0, 0 bad; the other 24 are hosted-run or sudo install steps, each with its reason on record.
- `docs_inventory.py --check`: rc 0. `git diff --check` against the merge base: rc 0. rtl-fast's gates and `check_cpp_idiom.py`: rc 0.
- Shipping route, one directive, ExtraPostPlacementOpt, at this head: 52,497 LUT, 54,579 FF, 15,780 of 15,850 slices, WNS +0.198 ns, WHS +0.015 ns, floor met at every corner, 0 routing errors. Every figure equals the earlier measurement at a29a7411.
Acceptance criteria: met. The sweep, firmware self-test, builder, behave, docs gates and docs inventory are green, and the route meets the WNS floor. Required items 1 to 4 are done; no campaign count moved.
Open risks/questions:
1. Owner decision wanted: the resource gate has no verdict on this route. `docs/integration/BUILDING.md` section 5 has it judge an adoption, but the assigned one-directive route is not in its recipe form, so it exits 2, not comparable. By arithmetic against its `route-1x1` record, LUT is +485 of +500, slices 0 of +80, and FF +872 of +600: dev alone is +394, so this adoption's +478 crosses the tolerance. The record used single-thread synthesis, so a recipe measurement may differ. `docs/design/AREA_BUDGET.md` also says the next growth needs its own owner decision. #845's acceptance names the WNS floor only, so `Closes #845` stands in the draft on that reading.
2. dev moved to 87e9d03a (PR #834) during this run. A trial merge conflicts only in the generated `docs/DOCUMENTATION_AUDIT.md`, which `scripts/docs_inventory.py --write` regenerates.
3. The CI image declarations were not refreshed. `ci_tool_inventory.py --check` refuses alike on dev and here, on an unrelated script; 34 of 150 reviewed pins already differ on dev, and `unb_mutants.py` makes 35. No workflow runs it. It needs its own issue.
4. The route's unit peaked at 18.1 GB: under the 24 GB cap, over the 12 GB target.
5. No parent harness drives a Talker registered before the settle through `milan_datapath`; the processor's suites grade it.
