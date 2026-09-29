[A433]
Relates to #495

## Contents

- **[Status](#status)** -- Items 1-7 and the item 1 README follow-up committed; the gate set is green at the head.
- **[Linked Issue / roles](#linked-issue--roles)** -- The #495 checklist, which stays open, and the lane's roles.
- **[Description](#description)** -- One commit per checklist item, with its review references.
- **[Authoritative references](#authoritative-references)** -- The assignment, the disposition, the checklist comments and the reviews they cite.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Branch, submodules and the pinned environments.
- **[How to validate](#how-to-validate)** -- The gate set and its results at the head.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What each item leaves, and what the lane did not run.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

Ready for review at `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0` (`495-builder-residue` -> `dev`, base `eaa88a32`).
Items 1-7 are committed one commit each, plus a separate one-line commit for
the item 1 README wording the item 6 disposition asked for. Nothing on #495 is
ticked; the manager ticks the items at merge. The executor did not push the
branch; this body is for the PR opened once it is pushed at that head.

## Linked Issue / roles

Relates to #495 (the review-leftover checklist stays open for its other items).
Assignment: #495 comment 5880790651. Item 6 disposition: #495 comment 5882165062.

Executor: `[A433]`
Internal cleared-context reviewer: `[R396]`
External reviewer: `[R397]`

## Description

| # | Commit | Checklist / review | Change |
|---|---|---|---|
| 1 | `9e53b116` | 5863211190 item 1; PR #596 R354-1 S3 (groups 4-5), R355-2 SG3 | `tb/verilator/milan_dp/Makefile` reads `AX_GPTP_HZ` from `CPU_HZ` in `tb/verilator/nvm_capture_cpu/recipe.py` (by path, status taken) and passes it to the ROM generator, `-GMILAN_CLK_FREQ_HZ` and a new `-DMILAN_CLK_HZ_TB`; `sim_ax1x1gptp.cpp` takes `kHz` from that define and derives its period for every cycle/time conversion; a `static_assert` stops a build at a period its check labels (read by `verify_abort.py`) do not spell. The present-tense "50 MHz" in the `test_builder.py` print text and at `BAREMETAL_FIRMWARE.md:2036` now names the contract clock (PR #609 does not edit that hunk). New bank check `test_sim_clock`. |
| 2 | `e4197dc9` | 5863211190 item 2; PR #596 R355-2 SG8, SG4 (R355-1 SG4) | `sw/litex/sweep_extra.sh` passes `--entity-gen-dir` derived from the builder (a launch rebuilds the configuration first and refuses one whose entity definition the builder writes elsewhere), accepts `--dry-run` anywhere and refuses unknown options and missing, extra or empty arguments before anything runs, exports the build interpreter before reading the configuration, and keeps its launch line as an array. New bank check `test_extra_sweep_invocation`; every sweep test runs under an empty HOME. |
| 3 | `a71b3bec` | 5863211190 item 3; PR #596 R355-2 SG1 (R355-1 SG1) | `endstation_builder.py` and `milan_soc.py` read `CPU_HZ` from recipe.py by path, so a regular `tb` package on `PYTHONPATH` cannot replace it. New checks import each tool below such a package with recipe.py's bytes planted in memory; B5 and S7 (literal mirrors) are killed in that environment. |
| 4 | `8c62982f` | 5863211190 item 4; PR #596 R354-3 S1 | The equal-clock ROM control is reported through the builder bank's skip ledger, so the verdict names it. New bank self-check plants an equal-clock shape and requires the ledger entry and the run-list wiring. |
| 5 | `51ca45c7` | 5863211190 item 5; PR #596 R354-3 S2 | `docs/testing/CI_WORKFLOWS.md:43-50` states the classifier's rule (gated modules exclude only the builder bank), so the tap page no longer reads as documentation only. `scripts/ci_scope.py` is not edited. |
| 6 | `eb23f044` | 5868165584; PR #614 R388-1 S1 = R389-1 S1; disposition 5882165062 (option 2) | Quoted hex text is an optional `0x`/`0X`, then ASCII hex digits with single underscores between digits, no sign or whitespace, and at most as many digits as the field's width holds (leading zeros included). A quoted MAC is six two-digit octets with one uniform `:` or `-`, or exactly twelve digits of hex text. Signs, whitespace, short or long digit strings, short or unpadded octets, mixed separators, underscores beside separators and leading, trailing or doubled underscores are refused before any value exists; `"2"`, `"-2"` and `"0:2"` no longer become `00:00:00:00:00:02`. New named refusal tests `test_mac_shape_contract` (nine rules, 30 spellings) and `test_hex_shape_contract` (all ten quoted hex fields, eight rules plus the width). Every accepted-form pin from #595 and PR #585 stays green; `README-parameters.md:161-171`, `ENDSTATION_BUILDER.md:890-893` and `PP_DESCRIPTOR_OWNERSHIP.md:289` state the forms. Width per field: MAC and stream DMAC 12 digits (MAC-48), identities and format words 16 (EUI-64), `vendor_oui` 6, `entity_capabilities` 8 (`ADP_ENTITY_CAPS_C` is 32 bits). |
| 7 | `a9cecd23` | 5880770002 S1; PR #615 R382-4 S1 | `sw/builder/test_shipping_clock_constraints.py` also requires, in the real emitted build Tcl, one `kl_timing_grade_configure` before `place_design` and one `kl_timing_grade_reports` after the last `route_design` and before `write_bitstream`. R382-4's MD and ME mutants (verbatim from its packet) now turn the probe red; `docs/testing/RUNNING_TESTS.md` states the two checks. |
| 1b | `859fa5d5` | item 1 wording, per disposition 5882165062 | `tb/verilator/milan_dp/README.md:85` names the contract clock instead of "50 MHz" for `obj_ax1x1gptp`. |

## Authoritative references

- #495 assignment 5880790651; checklist comments 5863211190, 5868165584, 5880770002; item 6 STOP 5882153376 and disposition 5882165062.
- PR #596 reviews R354-1 (5858016029), R354-3 (5859474839), R355-1 (5858120015), R355-2 (5859061727), R355-3 (5859597477).
- PR #614 reviews R388-1 (5868119667), R389-1 (5868161494); the #595 decision 5867362523.
- PR #615 review R382-4 (5878000673) and its packet on `607-review-evidence` (`review-evidence/607-r1/reviews/R382-4`, receipt 07 and `scripts/merge_mutants.py`).
- `docs/integration/BAREMETAL_FIRMWARE.md` build contract; `docs/testing/CI_WORKFLOWS.md` gate-read policy; `sw/builder/README-parameters.md` quoted hex rule.

## How to get into the same state

```sh
git fetch origin 495-builder-residue && git checkout 859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
# Markdown gates: python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
# Pins-only builder environment (as elaborate.yml): Python 3.12, pyyaml==6.0.3,
#   python3 -m pip install -r sw/litex/litex_pins.txt; python3 scripts/ci_litex_env.py;
#   sw/litex/patches/apply.sh; sv2v v0.0.12 (digest as in elaborate.yml)
# Verilator 5.050 for milan_dp.
```

## How to validate

```sh
python3 sw/builder/test_builder.py --require-rv32 --require-elaboration   # compiler present
# compiler absent: the same bank with the three RV32 candidates hidden, and
python3 sw/builder/test_firmware_compiler.py --selftest
python3 sw/builder/test_firmware_compiler.py --absent --audit "$TMPDIR/rv32-absent.jsonl"
python3 sw/builder/test_clock_constraints.py            # pins-only: four shipping arms, with the #395 hooks
python3 sw/builder/test_timing_grade.py "$(command -v python3)"
python3 sw/builder/test_clock_contract.py --soc          # pins-only
python3 sw/builder/test_declarations.py                  # the #495 MAC and hex shape tests
python3 sw/litex/test_pp_mem_bridge.py
make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4     # milan_dp ax1x1gptp + verify_abort.py
```

Results at `859fa5d5` (all rc 0; every gate rerun at this head, none carried over from `51ca45c7`):

| Gate | Result |
|---|---|
| Builder bank, compiler present (`--require-rv32 --require-elaboration`) | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11: the historical Arty calibration report is not on this host) |
| Builder bank, compiler absent (three RV32 candidates hidden, `--require-elaboration`) | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 11, and gate 1b's compiled census, which needs the compiler) |
| `test_firmware_compiler.py --selftest` / `--absent --audit` | rc 0 / rc 0 |
| Pins-only: `test_clock_constraints.py` (four shipping arms, with the #395 hooks), `test_timing_grade.py`, `test_clock_contract.py --soc` | rc 0 each |
| `test_clock_contract.py`, `test_declarations.py` (nine MAC rules over 30 spellings; ten hex fields), `test_pp_mem_bridge.py` (113/113) | rc 0 each |
| `milan_dp_gptp` (ax1x1gptp, 137 checks, and `verify_abort.py`) | rc 0: 137 checks, 0 failures; `verify_abort.py` 6/0, 20/0, 14/0 |
| Markdown gates in the pinned renderer environment (19) | rc 0 each |
| Code-quality gates, Rules 3-13 with `--selftest`, and both measurement self-tests (24) | rc 0 each |
| `ci_scope.py --selftest`, `ci_events.py --check/--selftest`, `pp_srcs.py --check --selftest`, bare-metal, capture, SoC-source, sweep/deploy/entity-shape self-tests, `bash -n` (13) | rc 0 each |
| Mutants, every item (before-state and each mutant killed, controls pass; item 6: 17 mutants, item 7: R382-4's MD and ME plus four ordering mutants) | 0 expectation mismatches |

Evidence (commands, logs by sha256, mutation specs and results) is in the lane
handoff; the self-test results go in a PR comment.

## Known limitations / out of scope

- Item 5 leaves `scripts/ci_scope.py:12-13`, `:18-20` and `:66-68`, which still state the #444 criterion (not edited, as assigned: a CI-definition change invalidates queued act replays).
- Item 1 leaves three other clock mentions in `tb/verilator/milan_dp/README.md` that the disposition did not name: `:121` (the `obj_ax1x1` table), `:160` ("50 MHz aliases; nominal PHC increment 20 ns") and `:502` (a conditional "At 50 MHz"). The harness's check labels still spell 20 ns, 200 MHz and 28 ns; a `static_assert` ties them to the derived period.
- Item 6 changes three refusal pins' expected reasons (all still refused): `"0"` and `"1000000000000"` moved from "out of MAC-48 range" to the named digit-count rules, and `"-1"` (OUI and capabilities, and gate 25b's "vendor_oui negative" row) is now refused as a sign rather than as out of range. The `maap` selector of `srp.stream_dmac_base` is still matched after `strip().lower()`; it is a selector, not hex text.
- Out of scope by the assignment: `tb/verilator/fw_service_budget/run.py` and its README, `docs/findings/397_SERVICE_BUDGET.md` (after PR #609), 5880770002 S3, and every other #495 item. No processor, firmware, RTL or CI-definition change.
- No hardware, Vivado implementation or act replay was run in this lane.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (items 1-7 of the assignment)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (at the head, below)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
