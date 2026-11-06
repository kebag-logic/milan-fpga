[R782] POSITIVE - exact head 1105f54546b2f19d9577b7fad902c908e34f88ee

# R782-1 external independent review: PR #846 / issue #843

- Head `1105f54546b2f19d9577b7fad902c908e34f88ee`, tree `94be1980e4b837611cb08bc30b0d5dee1b5ecc7f`, eight commits on dev `cc204c6fd2349b543d73f15c97162a2c4434c86e` (the live dev tip as well).
- Scope I reconstructed: the issue #843 body ("Required in the parent" items 1 to 4 and Acceptance), the executor's TAKEN and REVIEW READY comments, the live PR body, AGENTS.md, CONTRIBUTING.md sections 3 and 6, then the diff, then the author's public receipts at `review-evidence/843-r1` (tree `3b2b1ef2`).
- Requirements checked: IEEE 802.1AS-2011 8.6.2.3 a) and b); IEEE 1588-2008 7.6.2.5 and Table 6; 802.1AS-2011 10.5.3.2.3 (Announce grandmasterClockQuality, message offset 48); IEEE 1722.1-2021 7.2.8 (AVB_INTERFACE clock fields, octets 86 to 96) and 6.2.2.8 (entity_model_id).
- I applied all five lenses independently. Open BLOCKER, MAJOR or MINOR findings: **none**. There are two SUGGESTIONs and no RESIDUE.
- The one earlier public finding on this PR (R781-1 F1, MINOR) is resolved in the live PR body; see "Prior public findings".

## Directive checks (focus items 1 to 6)

| # | Claim | Evidence at this head | Result |
|---|---|---|---|
| 1 | The gitlink moves exactly to 1616fc8f, and the ROM digest is re-recorded through its recorder | The `gptp-processor` index record is mode 160000 at `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, stage 0. FPGA-gPTP PR #101 is merged, and its merge commit is `1616fc8f` on `main`. PR #99's merge `5184fb36` is an ancestor, and so is the old pin `135afd04`. `syn/yosys/rom_digests.tsv:16` `e83709d9...` is byte-equal to the generator's default image as `ooc.sh` runs it (`python3 gen_gptp_ucode.py -o <stage>`, `syn/yosys/ooc.sh:435`). It also equals the donor's tracked `syn/ooc/work/gptp_ucode.hex` at the pin. The ledger diff is that one added row, and every other pin's rows are retained, which is the recorder's rewrite shape. Receipt: `receipts/rom_and_route_image.txt` | met |
| 2 | Each config's `gptp.clock_accuracy` reaches `--clock-accuracy`: AX7101 0x22, Arty 0xFE | Builder: `gptp_ucode_args` is at `sw/builder/endstation_builder.py:3705` and is used by the build at `:5983`; the key is resolved at `:3717`/`:4233`. Configs: `configs/endstation_ax7101_1x1_tdm8.yaml:98` and `endstation_ax7101_8x8.yaml:116` are 0x22; the three Arty configs (`:200`, `:222`, `:242`) are 0xFE. Each AX7101 config's image (`--clock-accuracy 0x22`) hashes to `5a1d6d19...`. That equals the image the head route actually used, per `route-head/large-files.sha256` | met |
| 2 | The pin is relaxed only as far as needed | `GPTP_ENGINE_CONSUMED` (`:3567`) adds only `clock_accuracy`. `gptp_engine_pins` no longer returns it, while the six other fields stay refused (gate 1b's pinned list, `test_builder.py:17989ff`). Accepted values are limited to Table 6's 0x20..0x31 and 0xFE (`:3577`), and an omitted key gives 0xFE (8.6.2.3 b)) | met |
| 2 | Gate 26c and the gptp/gptp-lat legs show each value on the wire | I ran both legs. `gptp`: `[CA] 4 DUT Announce frame(s); last clockQuality 0xF822436A, expected clockAccuracy 0x22`, 212/212. `gptp-lat`: `... 0xF8FE436A, expected clockAccuracy 0xFE`, 212/212. Each leg image is byte-equal to the generator run with that config's options (`receipts/leg_images.txt`). Gate 26c passes (`receipts/runs/builder_26b_26c.log`) | met |
| 3 | `OUR_CQ` in gptp_shadow/gptp_plane comes from the generator | `tb/verilator/gptp_shadow/Makefile:13,22` and `tb/verilator/gptp_plane/Makefile:11,18` read `CQ_C` from the generator the image is built with; a missing define is a `#error`. The new grades are at `gptp_shadow/sim_main.cpp:1468` and `gptp_plane/sim_main.cpp:532-544`. I ran both: 326/326 and 31/31 | met |
| 4 | The service-budget oracle and receipts are re-measured through their generators, not edited | All three oracle rows equal the published receipts field by field: shape, raw_log, log_sha256 (recomputed), media, rows, budget_findings, heartbeat and liveness (`receipts/oracle_vs_receipts.txt`). All 141 tracked build inputs hashed in each receipt equal this head's bytes, including both configs (`receipts/receipt_hashes_vs_head.txt`). The dev re-measure has the same rows, heartbeat, liveness and findings; only the media differs, so the timing drift is already on dev. Verdicts and budget findings are unchanged from dev's oracle. `make -C tb/verilator/fw_service_budget` passes at the head (55 + 14 checks, 0 failures). With the previous oracle restored it refuses: "oracle image changed; rebuild and regenerate the trace fixture" (`receipts/runs/fwsb_at_4c4c5982_oracle.log`) | met |
| 5 | The docs inventory is regenerated | `python3 scripts/docs_inventory.py --check`: "OK (540 lines, docs/DOCUMENTATION_AUDIT.md is fresh)" | met |
| 6 | The area/timing record states the figures exactly and the gate's refusal honestly | Against `route-dev` and `route-head` (`timing-summary.txt`, `alinx_ax7101_utilization_place.rpt`, `route-1x1-check-shipping.log`): LUT 51,994 to 52,695 (+701); FF 54,101 to 54,288 (+187); slices 15,841 to 15,846, leaving 4 of 15,850; DSP 13 to 15; slow-corner WNS +0.236 to +0.018 ns; fast-corner WHS +0.036 to +0.015 ns. The gate rows read LUT +683 over 52,012 "REGRESSION: grew by more than 500", DSP +2 "grew by more than 0", and WNS "below the floor 0.03 at Slow_0C, Slow_85C". The gate ends `RESULT: MATERIAL REGRESSION`. `CHANGELOG.md:102-123`, `docs/design/AREA_BUDGET.md:151-154`, `docs/reference/SUBMODULES.md:472-494` and the PR body all match these values. Each says the gate refuses, the decision is open and only the shipping directive was routed. The route was built at `8210abaa`; every later commit touches tests, docs or the oracle only, so the gateware equals the head's (and the route's gPTP image digest equals this head's builder image) | met (the timing decision is the manager's) |

## Findings

### S1 - SUGGESTION - Robustness, Conformance - `sw/builder/endstation_builder.py:3725` - clockAccuracy is coerced with `int()`

- **Evidence:** `receipts/probe_clock_accuracy_types.txt`. A float `34.7` is accepted and announced as 0x22. A quoted `"0x22"` and a `null` raise an unnamed `ValueError`/`TypeError` traceback rather than a `ConfigError`. A `true` is refused only because `int(True)` is 1, which falls outside Table 6.
- **Impact:** small. Every case except the float fails closed, and the coercion is exactly that of the existing consumed `priority1` (`_gp_u8`). Even so, the key now reaches the wire, and a truncated float becomes a clock claim.
- **Suggested outcome:** accept only a YAML integer that is not a bool, and refuse anything else with a named `ConfigError`.
- **Verification:** extend `_assert_clock_accuracy_refusals` with a float, a string and a null arm.

### S2 - SUGGESTION - Docs - `docs/design/AREA_BUDGET.md:153`, `docs/reference/SUBMODULES.md:492`, PR body "Known limitations" - the worst-path attribution is published only by hash

- **Evidence:** the records say the slowest path is "the SoC's SDRAM controller" (the PR body adds "16 levels, 6.4 ns of routing"). The report behind this, `alinx_ax7101_timing.rpt`, is listed only by sha256 in `route-head/large-files.sha256`, so a cold reviewer cannot check it. The WNS/WHS figures themselves are in the published `timing-summary.txt`.
- **Impact:** the owner's route decision leans on "placement pressure outside the engine", and that statement is not publicly checkable.
- **Suggested outcome:** publish the worst-path section of the timing report, or quote it in the evidence packet.
- **Verification:** the excerpt names the path's startpoint, endpoint, levels and routing delay.

Comment rule (owner 2026-10-15): the delta adds no new lane label, lane name, review round, reviewer ID or issue-comment ID. Per changed source file, the count of such labels is equal at dev and head (17 files; the `[R-parallel] on #228` lines in the delta are existing instances, reflowed). That is not RESIDUE.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts (at the exact head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #843 items 1 to 3 and Acceptance against `endstation_builder.py:3567,3577,3705,3717,4233,5983`; the five configs' `clock_accuracy`; `avdecc/aem_descriptors.py:352` and the AVB_INTERFACE octets 86..96 (gate 26b); Table 6 range; `sim_gptp.cpp:2066` octet 63 (offset 48 + 14); `rom_digests.tsv:16`; the gitlink; model ids (AX7101 moved `0x1bc5c1935893e1` to `0x1bc5cd179523ab` and `0x1bc5572467af35` to `0x1bc5f6cb4a37d1`; the three Arty ids unchanged), so 1722.1-2021 6.2.2.8 holds. S1 is a SUGGESTION | R782-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| RTL | CLEAN | No parent HDL in the diff (`git diff --stat` shows no `hdl/` path). Engine HDL delta `135afd04..1616fc8f`: `KL_gptp_engine.sv`, `KL_gptp_rx_parser.sv` and the generator, all owned by FPGA-gPTP PR #99/#101. `milan_datapath.sv:76,8883` `GPTP_UCODE_HEX_P` is the existing parameter that `build-gptp-lat` (`milan_dp/Makefile:541`) sets. Route receipts show both routes complete with no failing endpoint; the WNS floor is the manager's decision | R782-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| Robustness | CLEAN | `_gptp_clock_accuracy_key` refusals (gate 26c arms 0x00, 0x1F, 0x32, 0x7F, 0x80, 0xFD, 0xFF; ends 0x20, 0x31 accepted); omitted-key default; type probe (S1, SUGGESTION); `gen_gptp_leg_ucode.py:33,37` refuses an unexpected builder option set; the `#error` guards for `OUR_CQ_TB` and `GPTP_CLOCK_ACCURACY_TB`; an empty `$(shell)` result cannot compile | R782-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| Tests | CLEAN | I ran milan_dp `gptp` and `gptp-lat` (212/212 each), gptp_shadow 326/326, gptp_plane 31/31, builder gates 26b/26c/model-id/doc-key-map and the ROM clock contract (all pass), and fw_service_budget (pass). Five reviewer mutants, all caught by name (`receipts/mutants/`). MR1: the builder hard-codes 0x22, caught by gate 26c and gptp-lat `[CA]`. MR2: the builder ignores the key, caught by gate 26b and gptp `[CA]`. MR3: gptp_shadow keeps dev's `0xF8FE436A`, caught by "every Announce carries this image's clockQuality". MR4: the gptp_plane image gets 0xFE, caught by "grandmaster Announce carries this image's clockQuality". MR6: the descriptor ignores the key, caught by gate 26b. Gate 1b exceeded my 10-minute window; for it I rely on the author's `final-gates-1105f545/builder.log:129` and my own image-difference check (`receipts/leg_images.txt`) | R782-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |
| Docs | CLEAN | `CHANGELOG.md:102-123`, `docs/design/AREA_BUDGET.md:151-154` and `docs/reference/SUBMODULES.md:24,439-494`, against the route receipts; `docs/ENDSTATION_BUILDER.md:1067` row 31a; `tb/verilator/milan_dp/README.md` rows; the diagram generators' `--check` and `check_diagram_pngs.py`, `check_submodule_docs.py`, `docs_check.py` and `docs_inventory.py --check` (all rc 0); no em dash in the added lines; `git diff --check` rc 0; the comment rule. S2 is a SUGGESTION | R782-1 | `1105f54546b2f19d9577b7fad902c908e34f88ee` |

## Prior public findings

I read these only after the verdict and ledger above were written. The one earlier round is R781-1 (`[R781] NEGATIVE`, issue comment of 2026-11-06T09:13:48Z on #846).

- **R781-1 F1 - MINOR - Docs:** the PR body's "GATES GREEN" Status head and its reproduction checkout named `4c4c5982`. **Resolved at this head.**
  - The live PR body (re-fetched; `receipts/live_pr_body_head_refs.txt`) now names `1105f54546b2f19d9577b7fad902c908e34f88ee` on the Status line and in the `git checkout --detach` command. No line names `4c4c5982`.
  - I agree with the finding's substance. At `4c4c5982` the fw_service_budget gate does refuse its oracle (`receipts/runs/fwsb_at_4c4c5982_oracle.log`). At this head it passes, and the author's `final-gates-1105f545/fw_service_budget.log` agrees.
  - The author's evidence snapshot `review-evidence/843-r1/author/PR-BODY.md` still shows the old head. It is an archived copy, not the PR text.
- **R781-1 S1 - SUGGESTION - Robustness:** `int()` coercion of `gptp.clock_accuracy`. **Retained.** It is my S1 above. It is optional by definition and does not affect coverage.
- R781-1 also asks the manager to confirm whether any upstream FPGA-gPTP review items addressed to the parent re-pin belong in #843's scope. That is a manager duty, not a finding against this head; it is carried below.

## Real limits

- I ran no full sweep, Yosys or builder bank, Vivado route or physical/hardware run. Gate 1b (`test_baremetal_profile_contract`) ran past my 590 s window twice; partial logs are kept as `*_TIMEOUT*`. For it I rely on the author's receipt.
- The route figures come from the author's published small reports. I did not re-route, and the large timing reports are published by hash only (S2).
- `check_em_dash.py --base` could not judge here: its pinned Markdown renderer is not installed. I substituted a direct search for U+2014 in the added lines.
- Physical calibration is NOT RUN. The 0x22 claim rests on the maintainer's 2026-11-05 decision; nothing measures the AX7101 oscillator.
- Hosted checks at this head when I looked: rtl-fast success; several Verilator shards and Yosys shards 0-2 in progress; Physical gPTP skipped (`receipts/hosted_check_runs_snapshot.txt`). These are observations, not acceptance.

## Pending manager duties

- Issue #843 item 4 (the stricter-readings page) is NOT MET on this base. It depends on PR #842. The PR says "Relates to #843" and does not close it; the item needs tracking until whichever PR lands second.
- The owner's route decision: the WNS floor miss and the resource-gate refusal (LUT, DSP, WNS) under the best-of-three directive rule (#818).
- Exact-head hosted `verilator-suites` and `yosys-portability` evidence and act acceptance; the current-dev merge-candidate builder and native banks; post-merge containment.
- R781-1's open question: whether any upstream FPGA-gPTP review items addressed to the parent re-pin belong in #843's scope.
- The Docs lens rests partly on the live PR body (R781-1 F1's fix). A later edit to that body is not tied to the head, so the manager should check that the Status head and the checkout command still name the merge candidate.

R782-1 FINISHED
