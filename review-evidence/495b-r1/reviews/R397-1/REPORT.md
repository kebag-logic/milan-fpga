[R397] POSITIVE - exact head 859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0

# R397-1: external review of PR #619 (issue #495, builder and tooling residue)

- **Head:** `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0`, tree `ca4085da7d014dbeeedaffa51f185d520ed70c66`.
- **Source base:** dev `eaa88a32eb77adeba9c1c631198c7fb516a11095`.
- **Diff:** eight commits, 16 files, +587/-145. No RTL, processor, firmware or CI-definition file is touched.
- **How the task was rebuilt:** from AGENTS.md, CONTRIBUTING.md, docs/README.md and the #495 body. Also from the scope comments on #495:
  - checklist 5863211190, 5868165584 and 5880770002;
  - assignment 5880790651;
  - STOP 5882153376 and disposition 5882165062 (option 2);
  - REVIEW READY 5883137691.
- **Also read:** the PR body, the diff and history, and the public evidence at `f5de5de1…/review-evidence/495b-r1`.
- **Not read:** private lane material, and no other reviewer's report for this round.
- **Probes:** they ran in disposable copies under the packet's `scratch/`. The review clone was cleaned and proved byte-exact afterwards (receipt 99).

## Verdict

- **Result:** POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. All five lenses are covered clean at the exact head.
- **Suggestions:** four SUGGESTIONs are listed below. None affects coverage.

## Per-item judgement against the checklist and the disposition

| # | Commit | Checklist entry / review | Result at head | Evidence |
|---|---|---|---|---|
| 1 | 9e53b116 + 859fa5d5 | 5863211190 item 1; R354-1 S3, R355-2 SG3; disposition (README:85) | **Met** | See item 1 below. |
| 2 | e4197dc9 | 5863211190 item 2; R355-2 SG8, SG4 | **Met** | See item 2 below. |
| 3 | a71b3bec | 5863211190 item 3; R355-2 SG1 | **Met** | See item 3 below. |
| 4 | 8c62982f | 5863211190 item 4; R354-3 S1 | **Met** | See item 4 below. |
| 5 | 51ca45c7 | 5863211190 item 5; R354-3 S2 | **Met as assigned (partial item)** | See item 5 below. |
| 6 | eb23f044 | 5868165584; R388-1 S1 = R389-1 S1; disposition 5882165062 option 2 | **Met** | See item 6 below. |
| 7 | a9cecd23 | 5880770002 S1; R382-4 S1 | **Met** | See item 7 below. |

**Item 1 (AX 1x1 simulation clock).**
- **Makefile:** `tb/verilator/milan_dp/Makefile:420` derives `AX_GPTP_HZ` from `CPU_HZ` in `recipe.py`. It runs the recipe by path under `python3 -I`, and `:423` checks the status. The one value feeds `--clk-hz`, `-GMILAN_CLK_FREQ_HZ` and `-DMILAN_CLK_HZ_TB` (`:480`).
- **Harness:** `sim_ax1x1gptp.cpp:64` takes `kHz` from the define. `:73` has a `static_assert` that stops a build at any period its 20 ns / 28 ns labels do not spell.
- **Prose:** the prose names the contract clock at `BAREMETAL_FIRMWARE.md:2036`, the `test_builder.py` print text and `milan_dp/README.md:85`.
- **Planted recipe:** `make -n` follows a planted recipe on all three uses, and an absent recipe is refused (receipt 11).
- **Mutants:** I1-M1..M5 are killed. I1-M6 (`observer{20}`) survives, but it is equivalent, because the `static_assert` pins the period to 20 ns.
- **Compile probe:** C++ was emitted with Verilator 5.050 for the exact `ax1x1gptp` command. The harness compiles at the derived clock. The planted `50000001` Hz trips the `static_assert`, and building with no define trips the `#error` (receipt 44).
- **Equivalence:** at 50 MHz every substituted expression equals its old literal. Examples: `kAafPeriod` is 6250, the Sync departure is `+10`, and the PHC increment is `0x14000000`.

**Item 2 (`sweep_extra.sh`).**
- **Argument parsing:** `parse_args` (`sw/litex/sweep_extra.sh:40`) accepts `--dry-run` in any position. It refuses unknown options, missing, extra or empty arguments, and an unknown board, all before anything launches.
- **Entity directory:** the configuration step prints `--entity-gen-dir` (`:31`). A launch rebuilds the configuration first and refuses a mismatched entity directory (`:27`).
- **Build interpreter:** `PATH` is exported before the configuration is read (`:67`).
- **Launch line:** it is an argv array.
- **Old invocation:** the old script, run under the new test, fails ("unknown board --dry-run", mutant I2-BASE). I2-M1..M6 are all killed (receipt 40).
- **Real launch path:** a stubbed `setsid` recorded argv (receipt 12, `scripts/sweep_launch_probe.sh`). The build runs, the entity-directory guard passes for the tracked configuration, and the 38-token argv carries `--entity-gen-dir <root>/configs/generated/endstation_ax7101_1x1_tdm8`. No builder text leaks into argv, and the tree was unchanged.

**Item 3 (clock import shadowing).**
- **Change:** `endstation_builder.py:73` and `milan_soc.py:76` use `runpy.run_path` on the recipe path.
- **Test:** `_assert_clock_source` (`test_clock_contract.py:44`) proves two things under a live shadowing `tb` package: the shadow is live, and the tool reads the planted recipe bytes.
- **Mutants, builder:** B5 (literal) and the restored namespace import are killed (receipt 40).
- **Mutants, SoC:** S7 (literal) and the restored namespace import are killed in the pinned LiteX environment (receipt 41).

**Item 4 (equal-clock skip ledger).**
- **Change:** `test_gptp_rom_clock(skip=...)` records the equal-clock decline through the bank's `skip()`.
- **Self-check:** `test_rom_clock_skip_reaches_the_ledger` (`test_builder.py:27828`) plants an equal-clock shape. It requires one `("clock contract", "row")` ledger entry, and it requires the run list to reach the ROM contract only through the ledger wrapper.
- **Mutants:** I4-M1 (print instead of record) and I4-M2 (wrapper drops the ledger) are killed.

**Item 5 (CI wording).**
- **Text:** `docs/testing/CI_WORKFLOWS.md:43-50` now states the classifier's rule, and I checked it against the code:
  - documentation, less `GATE_READ_DOCS`;
  - gated modules are `GATED_ROOTS`, the six roots, less `DOCS_JOB_PY`;
  - a gate-read page stays relevant even when `docs-check` runs the same check (`scripts/ci_scope.py:47-75`, `is_doc_only_path`).
- **Retained, by assignment:** `scripts/ci_scope.py` is untouched. Its docstring (`:12-20`) still carries the older wording, as the executor reported. The checklist item stays open for that remainder.

**Item 6 (strict quoted MAC and hex).**
- **Hex rule:** `HEX_TEXT` (`endstation_builder.py:1340`) and `_hex_text` (`:1345`) implement: an optional `0x`/`0X`, ASCII hex digits, and single underscores strictly between digits. There is no sign and no whitespace. The digit count, leading zeros included, must be at most the width.
- **MAC rule:** `_mac48` (`:3210`) accepts `MAC_OCTETS`, which is six two-digit octets with a backreferenced uniform `:`/`-`, or twelve digits of hex text (`:3227`).
- **Widths, checked at each source:**

  | Field | Width | Source |
  |---|---|---|
  | `platform.mac_address` | 12 digits | MAC-48 |
  | `srp.stream_dmac_base` | 12 digits | `_srp_dmac`, MAC-48 |
  | identities (`entity_id`, `entity_model_id`, `model_id_pin`) | 16 digits | `_eui64` / `_fmt64`, EUI-64 |
  | AAF `formats`, `crf_format`, `crf_output.format` | 16 digits | `_eui64` / `_fmt64`, 64-bit stream format word |
  | `entity.vendor_oui` | 6 digits | `_declared_uint(…, 24)` |
  | `entity.entity_capabilities` | 8 digits | `_declared_uint(…, 32)`; the test's legal value is `ADP_ENTITY_CAPS_C` |

- **Downstream consumers:** they read normalised values only (colon MAC, `0x%016X` words), so the stricter shapes reach no later `int(…, 16)` path unvalidated.
- **Independent oracle (receipts 30 and 31):** I wrote my own oracle from the disposition text, without regular expressions. It agrees with the parser on all **210,975** spellings, for the MAC shape and for hex at 24/32/48/64 bits. The spellings cover structured edits of legal forms, and every insertion, deletion and substitution of whitespace, signs, underscores, separators, prefixes, NUL, NBSP, U+2028, Arabic-Indic, fullwidth, superscript and mathematical digits. They also include 200,000 random strings. The result is **0 disagreements**. The same oracle disagrees with the base parser on 3,156 of the structured spellings (for example `"2"`, `"-2"`, `"0:2"` and `" 020000000002"`), which shows the comparison can fail. **I found no spelling the parser mis-judges.**
- **Tracked YAML (receipt 32):**
  - My inventory covers 16 tracked YAML files and 26 values in the ten fields. Verdicts are the same at base and head, with 0 changes. `sw/trace/milan_trace.yaml` uses custom tags; its only hit, `entity_id: x64`, is a trace type and not a builder input.
  - `load_config` output for all five tracked configurations is identical at base and head.
- **Documented examples (receipt 33):** every quoted example in tracked Markdown keeps its documented verdict.
- **Pins:** the #595 accepted-MAC pins and PR #585's `"0x001B_C50A_C100_0005"` pins are unchanged and green (receipt 10).
- **Mutants (receipt 40):** 14 non-equivalent parser mutants are all killed:
  - sign, whitespace (hex and MAC), doubled, trailing and leading underscores;
  - the width check replaced by a value check, and width removed;
  - MAC digit count loosened, the old lenient MAC path, all-zero removed;
  - Unicode digits, DMAC at 64 bits, OUI at 32 bits.
- **Equivalent survivors:** three mutants survive, and all three are equivalent, because the twelve-digit count still refuses what they admit: the backreference dropped, octets widened to `{1,2}`, and `0x` allowed on octets.
- **Docs:** `README-parameters.md:161-171` and `ENDSTATION_BUILDER.md:890-893` state the disposition's forms exactly. For `PP_DESCRIPTOR_OWNERSHIP.md:289`, see S1.

**Item 7 (timing-grade hooks).**
- **Check:** `assert_timing_grade_hooks` (`test_shipping_clock_constraints.py:30-44`) requires exactly one `kl_timing_grade_configure`, placed before the first `place_design`. It also requires exactly one `kl_timing_grade_reports`, placed after the last `route_design` and before `write_bitstream`.
- **Emitted Tcl order (control, 1x1 e1):** `opt_design`@241, configure@243, `place_design`@244, `route_design`@254, post-route `phys_opt_design`@255, reports@262, `write_bitstream`@270.
- **Reviewer-built mutants (receipt 42):** each was elaborated for real on 1x1 e1 and 8x8 e2.
  - H1 (configure dropped), H3 (configure moved to pre-routing), H4 (reports dropped), H5 (reports duplicated) and H6 (reports moved to pre-routing) are all killed by the new assertions.
  - H2 and H7 are invalid: the toolchain has no post-placement hook.
- **Base probe (receipt 43):** the base probe passes H1 and H6, so the new check is what detects them.
- **R382-4's packet:** I did not use its verbatim MD/ME. My H1 and H6 are the same fault classes.

## Findings

No BLOCKER, MAJOR or MINOR.

```text
[R397] SUGGESTION Docs - docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:289 - third statement of the hex rule is a partial summary
Requirement/evidence: disposition 5882165062 accepts an optional 0x/0X and bounds the digit count by the field width.
  The line names only "an optional `0x` prefix and single underscores between digits". It is true as far as it
  goes, but it omits 0X, the sign and whitespace refusals and the width rule. The two pages the disposition named
  state the rule exactly.
Impact: a reader of this page alone could take 0X as refused or miss the width rule. No behaviour is affected.
Required change (optional): state the full form, or point to sw/builder/README-parameters.md:161-171.
Verification: read the line against the disposition.
```

```text
[R397] SUGGESTION Docs - docs/testing/CI_WORKFLOWS.md:46 - "the six roots named below" is first followed by a seven-item list
Requirement/evidence: the next list (:51) names tb/, hdl/, sw/, syn/, scripts/, tests/ and configs/ (seven, not the
  classifier's roots). The six GATED_ROOTS (tests, tb, syn, sw, hdl, avdecc) appear only in the paragraph after that (:67-68).
Impact: readability only; the rule stated is correct against scripts/ci_scope.py.
Required change (optional): name the six roots inline or reference the later list.
Verification: read :43-68.
```

```text
[R397] SUGGESTION Docs - tb/verilator/milan_dp/README.md:121, :160, :502 - three remaining "50 MHz" statements
Requirement/evidence: :160 is in the obj_ax1x1gptp model table ("Milan and PHC | 50 MHz aliases"). The executor
  disclosed all three. The disposition named only :85, so they are outside this lane's frozen scope. The harness
  static_assert keeps :160 true while the contract clock is 50 MHz.
Impact: a future contract-clock change would leave these statements stale. The build would stop at the
  static_assert, so nothing would pass silently.
Required change (optional): carry them as a #495 checklist line.
Verification: grep "50 MHz" in the README.
```

```text
[R397] SUGGESTION Tests - sw/builder/test_shipping_clock_constraints.py:44 - reports are bounded by the last route_design, not by the post-route phys_opt_design that follows it
Requirement/evidence: the checklist wording ("after the last route_design") is implemented exactly. In the emitted Tcl
  a post-route phys_opt_design (@255) follows route_design (@254), and the reports come after both (@262).
  No platform hook sits between those two commands today, so a misplacement there needs a toolchain template change.
Impact: none reachable through the platform's hook lists.
Required change (optional): bound the reports by the last design-modifying command.
Verification: a mutant that inserts the reports between route_design and phys_opt_design must turn red.
```

**Checklist findings (items 1-7):** each is resolved at this head as recorded above. Item 5's `scripts/ci_scope.py` docstring is **retained**, by the assignment's instruction. The `maap` selector's `strip().lower()` match is retained as a selector, not hex text, and was disclosed.

**Prior findings on PR #619:** none were published before this round. The PR carried only the two review-start comments.

## Lens results

```text
[R397] PASS Conformance - issue 495 comments 5880790651 / 5882165062 vs diff eaa88a32..859fa5d5 (16 files) - items 1-7 each met as assigned and disposed (table above); item 6 shapes vs disposition by the reviewer's own oracle (210,975 spellings, 0 disagreements) and widths vs each field's source; the 26 tracked values and 5 config loads unchanged; the #595 and #585 pins green
[R397] PASS RTL - tb/verilator/milan_dp/Makefile:420-480, sim_ax1x1gptp.cpp:64-80, emitted alinx_ax7101.tcl (control order), receipt 44 - no HDL changed; one clock value feeds the ROM generator, the MILAN_CLK_FREQ_HZ elaboration and the harness; Verilator 5.050 emission of the exact target command and the harness compile clean; the static_assert and #error guards fire; the #395 hooks sit at pre-placement and post-route/pre-bitstream in the real Tcl
[R397] PASS Robustness - sw/litex/sweep_extra.sh:14-94, endstation_builder.py:1340-1368 and :3210-3240, receipts 12/30/40 - argument order, unknown, extra and empty arguments, an ungenerated entity and a stubbed real launch; malformed, whitespace, sign, Unicode, width-boundary and all-zero spellings; the absent-recipe refusal; no regex backtracking hazard (each iteration consumes one digit)
[R397] PASS Tests - test_clock_contract.py:44/279/342, test_declarations.py:287/331, test_builder.py:27816-27860, test_shipping_clock_constraints.py:30-44, receipts 40-43 - every changed check fails on its defect: 42 reviewer mutants (33 in items 1-4 and 6, 2 SoC-side, 7 hook placements) plus the base script and base probe; 6 not killed, each shown equivalent (4) or invalid (2); changed tests, the bank with and without the compiler, and the pins-only tests all green
[R397] PASS Docs - README-parameters.md:158-176, ENDSTATION_BUILDER.md:887-893, PP_DESCRIPTOR_OWNERSHIP.md:288-290, CI_WORKFLOWS.md:43-50, RUNNING_TESTS.md:185-192, BAREMETAL_FIRMWARE.md:29-49/2036, milan_dp/README.md:85, receipt 61 - statements match the code and the disposition; documented examples keep their verdicts; 52 docs and code-quality gates rc 0 in the pinned renderer environment; only SUGGESTIONs S1-S3 remain
```

## Executed evidence (this review)

| Receipt | What | Result |
|---|---|---|
| 00 / 99 / 98 | Integrity before and after: HEAD, index = tree, all 958 tracked blobs (bytes and mode), gitlinks, no stray files; plus a negative control | OK / OK / control FAILS as required |
| 01 | Tool identities: scoped Verilator 5.050 (`verilator_bin` sha256 `44898b22…`), Python 3.14 host, 3.12 venvs, RV32 SDK gcc 14.3.0 | recorded |
| 10, 11 | `test_declarations.py`, `test_clock_contract.py` | rc 0 |
| 12 | `sweep_extra.sh` real launch path with stubbed `setsid`/`sleep` under a scratch HOME | builds, guard passes, 38-token argv with `--entity-gen-dir`, tree clean |
| 20 | Full builder bank, compiler present (`--require-rv32`), all 100 gates | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11) |
| 21 | The same bank, run by the reviewer's chunk driver, with gate 1b held back | rc 0, the same verdict |
| 22 | Bank, compiler absent (three RV32 candidates hidden), all 100 gates in two chunks | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b census, gate 11) |
| 23 | `test_firmware_compiler.py --selftest` / `--absent --audit` | rc 0 / rc 0 |
| 30-33 | Shape oracle, base control, YAML inventory, documented examples | 0 disagreements; control discriminates; 0 verdict changes; examples agree |
| 40-44 | Mutants (items 1-4, 6), SoC mutants, hook mutants (item 7), base-probe control, harness compile probe | all non-equivalent mutants killed |
| 50-54 | Pins-only environment (Python 3.12, `litex_pins.txt`, pyyaml 6.0.3, VexiiRiscv pin, patch series); `test_clock_contract.py --soc`, `test_timing_grade.py`, `test_clock_constraints.py` (four shipping arms) | rc 0 each |
| 60, 61 | Pinned Markdown renderer (hash-locked); 52 docs, Markdown and code-quality gates (em-dash `--base eaa88a32`, `gen_toc --check`, `docs_check`, Rules 3-13 with `--selftest`, `ci_scope --selftest`, `ci_events`, `pp_srcs`, `bash -n`) | 52 of 52 rc 0 |
| 70-72 | `gh pr checks 619` and check runs bound to `859fa5d5` | 21 executed success; "Physical gPTP (nightly and manual)" skipped |
| 72 | Hosted log extracts | `elaborate` `ALL GATES PASS EXCEPT 3 NOT RUN`; `docs-check` `EXCEPT 15 NOT RUN` (LiteX-less rows) |

**Hosted checks.** Executed jobs are separate from skipped contexts. Of the 22 contexts, 21 executed and 1 was skipped (Physical gPTP). The `verilator-suites` and `yosys-portability` contexts are aggregators over the executed shards. The manager owns hosted and act acceptance.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue scope comments; diff `eaa88a32..859fa5d5`; oracle, inventory and pins (receipts 10, 30-33) | R397-1 | 859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0 |
| RTL | CLEAN | milan_dp Makefile and harness; Verilator 5.050 emission and compile probe; emitted shipping Tcl order (receipts 42-44) | R397-1 | 859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0 |
| Robustness | CLEAN | `sweep_extra.sh` probes and stubbed launch; parser edge spellings; absent recipe (receipts 11, 30, 40) | R397-1 | 859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0 |
| Tests | CLEAN | Changed tests and 42 mutants plus controls; banks with and without the compiler; pins-only tests (receipts 20-23, 40-43, 52-54) | R397-1 | 859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0 |
| Docs | CLEAN (S1-S3 optional) | Six changed pages and the README; 52 docs and code-quality gates (receipt 61) | R397-1 | 859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0 |

## Real limits

**Receipt 20 (full bank, compiler present).**
- It ran as a detached process, because the bank outlasts one ten-minute call. It completed rc 0 in 750 s.
- It shared the review clone with the start of the chunked run (receipt 21), which I started after wrongly concluding the detached run had died. Both passed, but receipt 20 is not an isolated run.
- The chunked runs cross process boundaries between gates. The bank itself runs them in one process.

**Tool versions.**
- All bank runs used the host sv2v 0.0.13, not the pinned 0.0.12. The pinned 0.0.12 was used for the docs gates.
- The bank used the bench LiteX interpreter, found through `sweep.sh`. The pins-only tests and the item 3 and item 7 mutants used the reviewer's pinned LiteX venv.
- The brief's scoped Verilator path does not exist on this host. I used the same 5.050 binary through my own wrapper; its identity and hash are in receipt 01.

**Not run by me.**
- I did **not run** the `milan_dp_gptp` / `ax1x1gptp` simulation, which takes about 58 minutes. I ran only a C++ emission and compile probe. At 50 MHz the harness is expression-equivalent to base. Run evidence is the executor's 137/0; no hosted job executes this target at this head.
- R382-4's verbatim MD/ME mutants: I used my own equivalents instead.
- act or Docker replay, Vivado implementation, hardware and physical calibration: **not run**. Field skips are not hardware proof.

## Pending manager duties

- Validate the final candidate merge on live dev (source base `eaa88a32`), including the native banks and `ax1x1gptp` if required.
- Accept the hosted and act results.
- Tick #495 items 1-7 at merge, leaving item 5's `scripts/ci_scope.py` remainder and the other residue open.
- Obtain explicit maintainer authorization for the merge.

R397-1 FINISHED
