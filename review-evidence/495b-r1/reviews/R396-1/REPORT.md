[R396] POSITIVE - exact head 859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0

# R396-1: internal cleared-context review of PR #619 (issue #495, builder and tooling residue)

- **Head:** `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0`, tree `ca4085da7d014dbeeedaffa51f185d520ed70c66`.
- **Base:** dev `eaa88a32eb77adeba9c1c631198c7fb516a11095`, eight commits.
- **Verdict:** POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. There are six SUGGESTIONs (S1-S6). All five lenses are covered clean at this head.
- **Receipts:** every receipt and script is listed in `MANIFEST.sha256`, with paths relative to this packet. Host paths inside the receipts are written as `$CLONE`, `$PACKET`, `$HOME` and `$STORAGE`.

## Scope reconstructed

I read the sources in this order:

- AGENTS.md, CONTRIBUTING.md (workflow, verification bar, code quality, documentation wording) and docs/README.md;
- the #495 checklist body;
- the assignment 5880790651;
- the item-6 STOP 5882153376 and disposition 5882165062 (option 2);
- the checklist comments 5863211190, 5868165584 and 5880770002;
- the #595 decision 5867362523;
- the cited reviews:
  - PR #596: R354-1 S3, R355-1 SG1 and SG4, R355-2 SG1, SG3, SG4 and SG8, R354-3 S1 and S2;
  - PR #614: R388-1 S1 and R389-1 S1;
  - PR #615: R382-4 S1, with its MD/ME table;
- the PR body and the [A433] REVIEW READY comment 5883137691;
- `git diff eaa88a32..859fa5d5` and each commit.

From the public evidence tree (`f5de5de1`, `review-evidence/495b-r1`), I consulted only the gate command lists and the compiler-absent runner, to match the bank invocation. I did not read the lane handoff or any other reviewer's report before writing this verdict.

The assignment is items 1-7, one commit per item, plus the item-1 README line the disposition added (`859fa5d5`). The lane changes no RTL under `hdl/`, no processor, no firmware and no CI definition. `scripts/ci_scope.py` is deliberately left untouched.

## Item judgements

1. **AX 1x1 gPTP simulation clock (`9e53b116`, `859fa5d5`). MET.**
   - **Single source.** `tb/verilator/milan_dp/Makefile:419-426` runs `recipe.py` by path (`python3 -I`, runpy) and takes the shell status.
     - `AX_GPTP_HZ` feeds the ROM generator (`:433`), `-GMILAN_CLK_FREQ_HZ` and `-DMILAN_CLK_HZ_TB` (`:479-480`).
     - The ROM rule depends on the recipe.
   - **Harness.** `sim_ax1x1gptp.cpp:64` sets `kHz = MILAN_CLK_HZ_TB`. Every cycle-to-time conversion now uses `kPeriodNs`.
     - An `#error` refuses a build without the define.
     - The `static_assert` (`:73`) stops any period other than 20 ns, whose check labels (20 ns, 200 MHz, 28 ns) `verify_abort.py` reads.
     - Receipt 35 (g++ on `:55-81`): no define gives the `#error`; 50 MHz compiles; 100 MHz, 50 MHz + 1 Hz and 62.5 MHz stop at the `static_assert`.
   - **Prose.** The present-tense prose now names the contract clock:
     - `BAREMETAL_FIRMWARE.md:2037-2039` links `#build-contract` (`:2038`), whose heading is `## Build contract` at `:29`;
     - `test_builder.py:17097`;
     - `tb/verilator/milan_dp/README.md:85`.
   - **Test.** `test_sim_clock` (`test_clock_contract.py:342`) expands `make -n -B ax1x1gptp`. It requires each of the three uses under the real recipe and under a planted recipe (+1 Hz), and it refuses an absent recipe by name.
   - **Mutants.** 1-A to 1-G are all KILLED by named assertions (receipt 30): a Makefile literal, a ROM literal, the `-D` dropped, an elaboration literal, the status check removed, a harness literal and a report literal.
2. **`sweep_extra.sh` (`e4197dc9`). MET.**
   - **Arguments.** `--dry-run` is accepted in any position. Unknown options, missing, extra or empty arguments and unknown boards are refused (rc 2) before anything runs.
   - **Entity directory.** `--entity-gen-dir` is derived from the builder.
     - A launch first rebuilds the configuration and refuses one whose entity definition lands elsewhere (`:27-28`).
     - The build interpreter is exported before the configuration is read.
     - The launch line is an array.
   - **Before-state.** The base script fails both of the head's sweep tests (receipt 36: "unknown board --dry-run", and a missing `--entity-gen-dir`).
   - **Mutants.** 2-A to 2-H are KILLED. 2-I SURVIVES, see S1.
   - **Real launch.** Launches of the two tracked default configurations under an empty HOME pass the guard and stop only at the absent Vivado settings file (receipt 31). No build starts, HOME stays empty and the tree stays clean.
3. **Contract clock not shadowable (`a71b3bec`). MET.**
   - **Readers.** `endstation_builder.py:73` and `milan_soc.py:76` read `CPU_HZ` through `runpy.run_path`.
   - **Checks.** `_assert_clock_source` (`test_clock_contract.py:44`) imports each tool below a regular `tb` package that declares another clock, with `recipe.py`'s bytes planted in memory. It first proves the shadow is live.
   - **Mutants.**
     - B5 (builder literal) and S7 (SoC literal) are KILLED in that environment, as are my two namespace-import reverts (receipt 30).
     - S7 and its control run in the pins-only interpreter.
   - **Other readers.** `check_nvm_capture.py` and `nvm_capture_cpu/run.py` still import by directory, which a `tb` package cannot shadow.
4. **Equal-clock SKIP in the ledger (`8c62982f`). MET.**
   - **Ledger.** `test_gptp_rom_clock` takes a `skip` callable. The bank passes its own `skip` through `test_rom_clock_contract` (`test_builder.py:27816`).
   - **Self-check.** `test_rom_clock_skip_reaches_the_ledger` (`:27828`) plants an equal-clock shape and requires one `("clock contract", ..., "row")` entry. It then removes the entry, and it pins the run list by AST.
   - **Bank log.** Receipt 21a shows the planted SKIP line, and the verdict counts only gate 11.
   - **Mutants.** 4-A to 4-D are KILLED.
5. **CI documentation-only wording (`51ca45c7`). MET.**
   - `CI_WORKFLOWS.md:43-50` now defines documentation by the classifier's own rule: pages a gated module reads, a gated module being code under the six `GATED_ROOTS` other than `DOCS_JOB_PY`. It says the tap page stays relevant.
   - This matches `scripts/ci_scope.py:52-73` (`GATE_READ_DOCS`, `GATED_ROOTS`, `DOCS_JOB_PY`).
   - `scripts/ci_scope.py:12-13`, `:18-20` and `:66-68` still carry the #444 wording. They are disclosed, and they are left for the checklist as assigned.
   - See S2 for a wording point.
6. **Quoted MAC and hex shapes (`eb23f044`). MET per disposition 5882165062.**
   - **Hex text.** `HEX_TEXT` (`endstation_builder.py:1340`) is an optional `0x`/`0X`, then ASCII hex digits with at most one `_` between two digits. It uses `fullmatch`.
   - **Width.** `_hex_text` (`:1345-1363`) refuses a digit count, leading zeros included, above `bits // 4`. The width sources are:

     | Field | Width | Source |
     |---|---|---|
     | identities and format words (`_eui64`) | 64 bits | `EUI64_MAX` |
     | `srp.stream_dmac_base` | 48 bits | `MAC48_MAX` |
     | `vendor_oui` | 24 bits | literal, OUI-24 |
     | `entity_capabilities` | 32 bits | literal; `ADP_ENTITY_CAPS_C` is `32'h`, read by `_adp_caps` |

   - **MAC.** `_mac48` (`:3210`) accepts `MAC_OCTETS` (six two-digit octets sharing one `:` or `-`, by backreference) or `HEX_TEXT` with exactly twelve digits.
   - **Tests.** Two named refusal tests: `test_mac_shape_contract` (9 rules, 30 spellings) and `test_hex_shape_contract` (all 10 quoted hex fields, 8 rules plus the width, and the accepted `0X` and grouping).
   - **Inventory (my own, receipt 10).** It walks every tracked YAML (16 files, custom tags tolerated) and harvests the quoted spellings of the three rule pages and every documented YAML field line: 112 cases. Each case is judged with the base and head parsers and with an independent oracle written from the disposition.
     - All five configurations keep their values: MACs `02:00:00:00:00:0{1,2}`, DMAC `0x91E0F000FE01`, CRF and listener formats, and the model pin.
     - Every documented example keeps its documented verdict.
     - The one flagged row is harvest noise: `soc.xlen` `32` on a line containing "machine".
     - The #595 and PR #585 accepted-form pins pass (`test_declarations.py` rc 0).
   - **Adversarial spellings.** I wrote 111 spellings of my own and could not produce a mis-judgement. They include fullwidth and Arabic-Indic digits, NBSP, zero-width space, U+2212, CR/LF/tab/NUL, dotted and space separators, `0x0x`, `0x_`, `0x` on octets, 13 and 14 digits, and leading zeros past each width. Result: 0 oracle disagreements, 0 crashes.
   - **Mutants.** 13 of 15 are KILLED (receipt 32).
     - 6-E (backreference replaced by `[:-]`) and 6-G (`{1,2}` octets) are not killed.
     - Both are **equivalent**: the twelve-digit count refuses every extra spelling they admit. Receipt 33 shows 0 verdict or value differences from the head over 110,514 spellings. That is the 223-case probe set plus an exhaustive `{0,2,:,-,_}` enumeration to length 7, and grouped spellings with 5-7 groups of 1-3 digits and uniform or mixed separators.
     - Neither is a test gap.
   - **Docs.** `README-parameters.md:161-171` and `ENDSTATION_BUILDER.md:890-893` state exactly these forms. `PP_DESCRIPTOR_OWNERSHIP.md:289` is true but partial, see S3.
7. **Shipping probe asserts #395 hooks (`a9cecd23`). MET.**
   - `assert_timing_grade_hooks` (`test_shipping_clock_constraints.py:30-44`) runs inside the real `milan_soc.main()` elaboration (`:97`). It requires:
     - exactly one `kl_timing_grade_configure`, before the first `place_design`;
     - exactly one `kl_timing_grade_reports`, after the last `route_design` and before the first `write_bitstream`.
   - **Mutants (receipt 34).** These are my SoC-level equivalents of R382-4's MD and ME, not its packet scripts:
     - `bitstream_commands` replaced: KILLED on 1x1 e1 and on 8x8 e2;
     - `pre_placement_commands` cleared: KILLED on 1x1 e1 and on 8x8 e2;
     - configure moved after placement: KILLED;
     - reports moved before routing: KILLED;
     - configure duplicated: KILLED;
     - control: passes;
     - the old probe (hook check removed) under MD: passes. This shows the new check is what kills.
   - `RUNNING_TESTS.md:188-189` states both checks.

## Findings

No BLOCKER, MAJOR or MINOR. Six SUGGESTIONs follow. None affects coverage.

### S1 - SUGGESTION - Tests - `sw/builder/test_clock_contract.py:279-299`, `sw/litex/sweep_extra.sh:27-28` - the launch guard's accepting side is ungraded

- **Evidence.** Mutant 2-I (`if built != gen:` becomes `if True:`) makes every launch refuse, and it SURVIVES `test_extra_sweep_invocation` (receipt 30). The committed arm only plants a configuration outside `configs/` and expects the refusal.
- **Head behaviour is correct.** Tracked configurations pass the guard and reach the Vivado settings step (receipt 31).
- **Impact.** A regression would fail loudly at the operator's first launch. It cannot produce a wrong build.
- **Suggested outcome.** Add an arm that launches a tracked configuration under an empty HOME and requires the failure to come after the guard, at the missing settings file.
- **Verification.** 2-I turns red.

### S2 - SUGGESTION - Docs - `docs/testing/CI_WORKFLOWS.md:46` - "the six roots named below" points past a seven-root list

- **Evidence.** The next roots named (`:51`) are the seven relevant roots, including `scripts/` and `configs/`. The six `GATED_ROOTS` appear only at `:71-72`.
- **Impact.** A reader who takes the first list could believe a page read only by a `scripts/` reader is relevant. `:88-93` corrects this later.
- **Suggested outcome.** Name the six inline, or point at the self-test paragraph.

### S3 - SUGGESTION - Docs - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:289` - a third statement of the rule is partial

- **Evidence.** The line says an optional `0x` prefix and single underscores are accepted. It does not mention `0X`, the width rule or the sign and whitespace refusals, and `:291` ("String digits retain their hexadecimal value") can read as if `"0x0001BC50AC1000005"` were accepted.
- **Suggested outcome.** Point at `sw/builder/README-parameters.md` for the complete forms, or add the width sentence.

### S4 - SUGGESTION - Docs (disclosed, out of the assigned lines) - `tb/verilator/milan_dp/README.md:121`, `:160`, `:502` - remaining 50 MHz, 20 ns and 200 MHz restatements

- **Evidence.** These lines still restate the clock values. They stay true while the `static_assert` holds (receipt 35), and the PR body discloses them.
- **Suggested outcome.** A future checklist line may name the contract clock there too.

### S5 - SUGGESTION - Robustness (disclosed, pre-existing) - `sw/builder/endstation_builder.py:2060-2062` - the `maap` selector is lenient

- **Evidence.** The selector is matched after `strip().lower()`, so `" MAAP"` is accepted (receipt 10). `hash-derived` and `mac-derived` are matched exactly.
- **Scope.** The selector is not hex text, so the disposition does not cover it.
- **Suggested outcome.** Match all three selectors exactly, for consistency.

### S6 - SUGGESTION - Robustness, RTL (widths) - `sw/builder/endstation_builder.py:1345-1363` - `_hex_text` states "bits a multiple of four" and does not enforce it

- **Evidence.** The old `_declared_uint` checked `n < 1 << bits`. The new code checks only the digit count, which bounds the value only when `bits % 4 == 0`. All current callers pass 24, 32, 48 or 64.
- **Impact.** None today. A future 10-bit caller would accept `0xFFF`.
- **Suggested outcome.** Assert the precondition, or keep a value bound.

## Lens results

- [R396] PASS Conformance - checklist entries 5863211190 items 1-5, 5868165584, 5880770002 S1; assignment 5880790651; disposition 5882165062 - checked against `git diff eaa88a32..859fa5d5` (16 files) and receipts:
  - items 1-7 and 1b judged above against R354-1 S3, R355-1/2 SG1, SG3, SG4 and SG8, R354-3 S1 and S2, R388-1 S1 = R389-1 S1, and R382-4 S1 MD/ME;
  - item-6 inventory and oracle: receipt 10;
  - before-states: receipts 34 (7-OLD) and 36.
- [R396] PASS RTL - diff stat has no `hdl/` path, and the clock and elaboration parameter chain was checked:
  - `tb/verilator/milan_dp/Makefile:419-426,433,479-480` (`-GMILAN_CLK_FREQ_HZ` and the ROM `--clk-hz` from one derivation; dry-run expansion in receipt 30, 1-CTL);
  - `sim_ax1x1gptp.cpp:55-81` period and bound arithmetic (compile probe, receipt 35);
  - width, truncation and range logic in `endstation_builder.py:1340-1363,2063,3210-3240,3704-3736` against 1722.1 EUI-64, MAC-48, OUI-24 and `ADP_ENTITY_CAPS_C`;
  - hosted `verilator-lint`, `yosys-elaboration`, Yosys 0-3 and Verilator 0-3 success at the exact head (receipt 50).
- [R396] PASS Robustness - probes:
  - receipt 10: 111 adversarial and 112 tracked or documented spellings;
  - receipt 33: 110,514-spelling enumeration;
  - receipts 30, 31 and 36: sweep argument orders, empty, extra and unknown arguments, a path with a space, empty HOME, a real launch past the guard, and the base script;
  - receipt 30, items 1 and 3: the `tb`-package shadow environment and the unreadable recipe;
  - receipt 35: harness build without the define and at other clocks.
  - S5 and S6 are suggestions only.
- [R396] PASS Tests:
  - my own 54-entry mutation campaign (`scripts/mutants.py`; receipts 30, 32, 34): 7 controls pass, 43 mutants killed with named assertions, 2 equivalent (receipt 33), 1 survivor (S1, suggestion), and 1 before-state control (7-OLD) passing as expected;
  - builder bank with the compiler present (rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`, gate 11) and absent (rc 0, `EXCEPT 2 NOT RUN`, gates 1b and 11) (receipts 21, 21a, 21b);
  - `test_firmware_compiler.py --selftest` and `--absent` (receipt 22);
  - pins-only `test_clock_constraints.py`, `test_timing_grade.py` and `test_clock_contract.py --soc` (receipt 20);
  - `test_clock_contract.py`, `test_declarations.py` (host and pins) and `test_pp_mem_bridge.py` 113/113 (receipt 23).
- [R396] PASS Docs:
  - `README-parameters.md:155-176`, `ENDSTATION_BUILDER.md:885-896`, `PP_DESCRIPTOR_OWNERSHIP.md:286-291`, `CI_WORKFLOWS.md:43-93`, `RUNNING_TESTS.md:185-192`, `BAREMETAL_FIRMWARE.md:45-46,2036-2040` and `tb/verilator/milan_dp/README.md:85`, read against the code they describe;
  - 19 Markdown gates rc 0 in a `--require-hashes` renderer environment built from `tools/markdown/requirements.txt` (receipt 40);
  - `git diff --check` is clean, and every commit is one line with no trailers;
  - S2, S3 and S4 are suggestions only.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #495 assignment 5880790651, disposition 5882165062, checklist comments; cited reviews R354-1/3, R355-1/2, R388-1, R389-1, R382-4; full diff `eaa88a32..859fa5d5`; receipts 10, 20-23, 30-36 | R396-1 | `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0` |
| RTL | CLEAN (S6 is a suggestion) | No `hdl/` change; milan_dp `Makefile:419-480`; `sim_ax1x1gptp.cpp:55-81`; builder width logic `endstation_builder.py:1340-1363,2063,3210-3240,3704-3736`; hosted lint, Yosys and Verilator 0-3 (receipt 50) | R396-1 | `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0` |
| Robustness | CLEAN (S5 and S6 are suggestions) | Receipts 10, 30, 31, 33, 35, 36: adversarial spellings, exhaustive enumeration, shadow environment, argument orders, empty HOME, real launch, missing define | R396-1 | `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0` |
| Tests | CLEAN (S1 is a suggestion) | 54-entry mutation campaign (receipts 30, 32-34); builder bank present and absent (21, 21a, 21b); firmware compiler (22); pins-only (20); changed tests (23) | R396-1 | `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0` |
| Docs | CLEAN (S2, S3 and S4 are suggestions) | The eight changed Markdown pages at the lines above; Markdown, quality and policy gates (receipt 40) | R396-1 | `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0` |

## Prior public review findings on this PR

None exist. At the time of this pass, PR #619 carries only the two review-start notes (5883161298, 5883165652), with 0 reviews and 0 inline comments. The cited reviews' suggestions that this lane addresses are:

- R354-1 S3 groups 4-5: taken;
- R355-2 SG1, SG3, SG4 and SG8: taken;
- R354-3 S1 and S2: taken; S2 keeps the disclosed `ci_scope.py` comment;
- R388-1 S1 = R389-1 S1: taken;
- R382-4 S1: taken.

## Gates and probes run

All commands ran in the foreground on this clone, and each result is in the receipts.

- **Pins-only environment.** Built fresh:
  - CPython 3.12.13 and `pyyaml==6.0.3`;
  - `pip install -r sw/litex/litex_pins.txt`, then `scripts/ci_litex_env.py` (VexiiRiscv `235753e2`) and `sw/litex/patches/apply.sh` (three patches).
- **Builder bank, compiler present.** RV32 compiler `riscv64-elf-gcc` 15.2.0 on PATH. rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`, 576 s.
- **Builder bank, compiler absent.** My own method: a PATH of symlinks without any `riscv*` tool, and an empty HOME, which removes the `~/br-milan-rv32` candidate. rc 0, `EXCEPT 2 NOT RUN`, 438 s. `test_firmware_compiler.py --selftest` and `--absent --audit` are rc 0.
- **Pins-only builder tests.** All rc 0.
- **Changed tests.** All rc 0.
- **Mutation campaign.** 54 entries.
- **Item-6 probes.** The inventory and oracle, and the equivalence proof.
- **Other probes.** The harness guard compile probe, the sweep launch and base-script probes.
- **Markdown gates.** 19 Markdown gates, all rc 0.
- **Quality and policy checks.** 14 checks, all rc 0. Two of them, `ci_events.py --check` and `check_nvm_capture.py`, first stopped because the renderer environment has no pyyaml (rc 2 and rc 1, recorded in receipt 40). Both are rc 0 under the host interpreter with pyyaml 6.0.3.
- **Hosted checks at the exact head** (receipt 50, polled 2026-09-29T04:19Z):
  - success: `rtl-fast`, `changes`, `bdd-conformance`, `verilator-lint`, `yosys-elaboration`, Yosys 0-3, Verilator 0-3, `elaborate`, `docs-check`, `docs-check-no-git`, `wire-accountability` and `full-ci-gate`;
  - `Verilator shard 4/5` was **in progress**;
  - `Physical gPTP (nightly and manual)` was **skipped**, which is not executed evidence.
- **Clone restoration.** Tracked blobs, modes, index and gitlinks were identical before and after (receipts 00 and 90):
  - 958 tracked entries, 0 mismatches;
  - write-tree equals `ca4085da`;
  - gitlinks `gptp-processor` `5dce647a`, `protocol-processor` `c951a9ff` and `third_party/verilog-axis` `48ff7a7e` are clean;
  - `external` `efeb541a` is uninitialised, as it was at the start;
  - the ignored outputs my runs created were removed.

## Limits

- **Verilator.** The Verilator path named in the brief (`.../372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host, so I ran no Verilator.
  - The `milan_dp_gptp` `ax1x1gptp` simulation (137 checks and `verify_abort.py`) was **not rerun** by this review.
  - Item 1's runtime behaviour at the contract clock rests on the manager's native bank and the executor's published result. My own evidence for it is the make dry-run expansion, the harness compile probe and the source reading.
  - The hosted `Physical gPTP` context was skipped.
- **sv2v.** The host `sv2v` is v0.0.13. `elaborate.yml` pins v0.0.12, and the bank's elaboration arms ran with v0.0.13.
- **Compiler-absent method.** My compiler-absent method changes HOME for the whole bank, which only moves gate 11's missing-report path.
- **R382-4 mutants.** R382-4's MD and ME were reproduced as SoC-level equivalents, not from its packet scripts.
- **Not run.** No act or Docker replay, no Vivado implementation, no hardware and no physical calibration. Field skips are not hardware proof.
- **Receipt hashes.** Receipt 21 lists sha256 values of the bank logs taken before host paths were scrubbed. `MANIFEST.sha256` hashes the published, scrubbed files.

## Pending manager duties

- Confirm `Verilator shard 4/5` completes successfully at `859fa5d5`. It was in progress at my poll.
- Run the native bank, including `milan_dp_gptp` `ax1x1gptp` at the exact head, and the act replay.
- At the merge turn, validate the candidate merge result against live dev. The source base is `eaa88a32`.
- Tick the #495 items at merge. Carry forward the disclosed residue as desired:
  - the `ci_scope.py:12-13,18-20,66-68` comment (item 5's remaining part);
  - `tb/verilator/milan_dp/README.md:121,160,502`;
  - the `maap` selector leniency;
  - S1-S6.
- Obtain the external review. Merge requires two independent positive reviews and the full completion bar.

R396-1 FINISHED
