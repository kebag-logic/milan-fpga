[R413] NEGATIVE - exact head 5b4a47e99f5a453832ccabccfbf4aae116d6fea0

Round R413-4, external independent review of kebag-logic/milan-fpga issue #70 / PR #623 (lane 2), exact head `5b4a47e99f5a453832ccabccfbf4aae116d6fea0`, tree `4da3a4345786338298d728d06b82fe9d35bc2e2a`. That is two commits on the round-3 head `0a80abcb`: `fa1d6e03` (R412-3 F1) and `5b4a47e9` (R412-3 F2).

Summary: both round-4 items are implemented as ruled. The rule comment, the `verdict_image_pins()` docstring, the verdict section, the refusal row, the closing line, the CHANGELOG and the PR body now state only what the pins prove, and they name both limits. R412-3's `nbr_runtime_sscanf` and `pre_overrun_sscanf` land on the verdict exactly as the second limit's words say. Both pass the whole gate 1b with the slot kept. The new interior-byte break is refused on the escape pin. Census mutant M9 is killed by it, M1-M8 stay killed, and the unplanted head passes with the slot kept and "refused 15/15".

One new MINOR remains open (F1 below, Tests and Docs). The new break reaches the verdict only at byte +1. A census narrowed to the verdict's first two or three bytes passes all fifteen verdict controls. Under such a census, a `sscanf()` write reaching byte +2 or +3 keeps the slot. Yet the test comment, the closing line and the firmware page say this break "measures the census's four-byte range". The census at this head is correct: the same +2 and +3 writes are refused on escape. The defect is that a test claims more discriminating power than it has. That is the same class as R412-3 F2, one byte further along. An open MINOR makes the verdict NEGATIVE.

## Sources reconstructed, in order

1. `AGENTS.md` and `CONTRIBUTING.md` (review lenses, severity, ledger rules), and `docs/README.md`.
2. Issue #70 body (frozen acceptance, scope). The round-4 assignment #70 comment 5909983141 (ruling: R412-3 F1 accepted as a second stated limit; F2 closed by a control that kills M9). The #495 record 5909985902. The review-start comment 5910884191. The PR body at this head: round 4 items 1-2 and validation, with the round-1 to round-3 sections read for residual claims.
3. `git diff 79c36963..5b4a47e9` (53 files; round-4 delta `0a80abcb..5b4a47e9` is `CHANGELOG.md`, `docs/integration/BAREMETAL_FIRMWARE.md`, `sw/builder/test_builder.py` only) and the two commits.
4. Public executable evidence at `3f26cbbabb75900e83ce947c90a0e658d0cffee0/review-evidence/70L2-r1`: `author-r4` (gate receipts, probe and premise-mutant receipts), and the prior round's scripts under `reviews/R412-3/scripts` (verified against that round's `MANIFEST.sha256`, all OK, and run unchanged).
5. Prior public review findings (R412-3 F1, F2) were read only after my own pass over the diff.

## Method (all at the exact head, disposable copies under the packet's scratch tree)

- Clone integrity checked before and after every probe: HEAD, index tree, empty status (untracked and ignored included), every tracked blob's bytes and mode, and submodule gitlinks `gptp-processor 5dce647a`, `protocol-processor b2db3a97`, `third_party/verilog-axis 48ff7a7e` clean (`external` not initialised). The result is `INTEGRITY OK` both times (`receipts/clone_integrity_start.log`, `receipts/clone_integrity_end.log`).
- Census compiler: the pinned RV32 SDK compiler (`riscv32-linux-gcc.br_real (Buildroot 2026.05) 14.3.0`), the same argv[0] the author's builder-present receipt names.
- R412-3's scripts run unchanged (`scripts/r412-3/`): all 25 probes through gate 1b early-stopped (`probe_all.sh`), base and the two F1 probes through the whole gate 1b (`R412_MODE=full`), and census mutants M1-M9 through the whole gate 1b (`census_mutants_run.sh`). Receipts are in `receipts/r412-3-rerun/`.
- My own probes (`scripts/r413_plants.py`, `scripts/r413_probe.sh`): nine plants asking each sentence of the bounded claim. Receipts are in `receipts/r413/gate1b_early_*.log`.
- My own census range mutants N1-N4 (`scripts/r413_census_mutants.py`), run with gate 1b stopped right after its verdict controls (`scripts/r413_stop_after_breaks.py`, `scripts/r413_census_stop_run.sh`). The stop point comes after the premise check, the AEM-first base with the slot kept, the forget-on-call refusal and all 15 breaks graded. The unmutated head was run the same way as the reference. Mutant N1 was also run with the +2 and +3 plants (`scripts/r413_mutant_probe.sh`).
- Docs, idiom and capture gates in the pinned Markdown environment: `docs_check`, `check_doc_paths`, `check_doc_style`, `check_archive`, `gen_toc --check`, `check_em_dash --base 79c36963`, `check_py_idiom`, `measure_test_evidence --check`, `git diff --check 79c36963 HEAD` and `check_nvm_capture`. All ten are rc 0 (`receipts/docs_gates.log`).
- Scope and firmware digest (`receipts/scope_and_digest.log`), and the exact-head hosted check-run snapshot (`receipts/hosted_checks.log`).

## Judgment of the round-4 items

### Item 1 (R412-3 F1, `fa1d6e03`): the verdict's pins claim only what they prove, and name two limits

Resolved as ruled.

- Rule comment `sw/builder/test_builder.py:1631-1677`: "That is all the pins prove: of the writes that reach the static through a relocation on its bytes, milan_init()'s one store is the only one, so outside the two limits below …". It names both LIMITS (a literal address, #495; another object's address carried outside that object, with `sscanf()` overrunning a neighbouring static and `&neighbour + k` with k known only at run time), and ends "this gate does not prove memory safety".
- `verdict_image_pins()` docstring `test_builder.py:6899-6933`: the escape pin now reads "no relocation on those bytes forms their full address", and LIMITS names both.
- `docs/integration/BAREMETAL_FIRMWARE.md:933-998`: the bullet "An address formed from another object's relocation is not a reference to those bytes". Then ":966-972: the pins prove this much and no more", and ":974-998" names both limits. The cross-reference "the first entry under What the census does NOT observe" resolves to `:808-821`, "A store made inside a CALLED function" (correct).
- Refusal row `BAREMETAL_FIRMWARE.md:1638` names both writes as outside the pins. The closing line (`test_builder.py:17209-17222`), CHANGELOG `:65-66` and PR body round 4 item 1 carry the same bounded claim. The earlier PR-body sections are marked as superseded ("Round 4 (above) bounds the claim these texts made"). A repository-wide search finds no remaining sentence claiming that nothing else writes the verdict.

The two probes match the second limit's words:

| Probe | Layout in the census image | Outcome at head | Stated limit's words |
|---|---|---|---|
| `nbr_runtime_sscanf` | `r412_pad` 0x158e4, `aem_loaded` 0x158e0; `&r412_pad + k`, `k = -1` volatile; relocations on the neighbour only | accepted early and through the whole gate 1b (`GATE1B PASS`, slot kept, "refused 15/15") | "`sscanf()` handed `&neighbour + k` with `k` known only at run time" (a pointer carried before the neighbour's start) |
| `pre_overrun_sscanf` | `r412_line[4]` 0x158c8-0x158cb, `aem_loaded` 0x158cc; `"%s"` of five characters plus NUL | accepted early and through the whole gate 1b, as above | "`sscanf()` with `"%s"` overrunning a four-byte static declared just before the verdict" |

All 25 R412-3 probes give the same rc and the same first refusal or acceptance line as that round's receipts at `0a80abcb`, with hex addresses normalised. The accepted ones are `base`, `nbr_after_sscanf`, `arr_overrun_sscanf`, `nbr_runtime_sscanf` and `pre_overrun_sscanf`. The two unnamed overruns land away from the verdict or inside the second limit's words.

My own probes of the bounded claim's other sentences (`receipts/r413/`):

| Probe | Outcome | Sentence it checks |
|---|---|---|
| `own_local_under_store` (local `int *p = &nbr; p[-1] = 0;`, nbr just after the verdict) | ACCEPTED, slot kept | "Nor is a store this unit makes … such as a local pointer to the neighbour indexed outside it": inside the limit |
| `own_callee_store` (unit-defined callee writes `p[-1]` through `&nbr`) | ACCEPTED, slot kept | "A called function that writes through it is not seen": inside the limit |
| `data_word_nbr_sscanf` (neighbour's address in a static data word, `- 1` handed to `sscanf()`) | ACCEPTED, slot kept | "A pointer formed from a neighbouring object's relocation and carried … before its start": inside the limit |
| `own_folded_store` (`(&nbr)[-1] = 0;`) | refused: the store pin and the escape pin (`%lo` on an `addi`) | "An offset the compiler folds into the relocation … is refused by address" |
| `own_runtime_store` (`(&nbr)[k] = 0;`, k volatile) | refused: "a STORE this gate cannot PLACE" | "A store through an offset known only at run time is refused by rule 1b" |
| `data_word_nbr_store` (`word[-1] = 0;`) | refused: unplaced store | rule 1b |
| `interior_b1_store` (a one-byte store in the unit at byte +1) | refused: the store pin and the escape pin | store pin by address |
| `interior_b2_sscanf`, `interior_b3_sscanf` (the round-4 break shape at +2, +3) | refused on the escape pin | the head's census reads all four bytes |

Every accepted write is inside the words of the second limit. Every refused one is refused where the text says it is. I found no third class of write that the bounded claim misses.

### Item 2 (R412-3 F2, `5b4a47e9`): a break on an interior byte

Resolved as ruled, with one residual (F1 below).

- `test_builder.py:14646-14650` plants `static int milan_verdict_next;` just after the verdict and hands `sscanf("%c")` the address `(char *)(&milan_verdict_next - 1) + 1`. The break table entry at `:14726-14728` expects the escape pin.
- The premise check at `:14733-14757` reads relocation targets directly, not through the range function under test. It requires at least one `nvm_boot()` reference on the verdict's bytes and none on byte 0. The head reports `interior_bytes=[1]`.
- M9 is killed by name: "the resolver accepted a neighbour's address folded onto an interior byte of aem_loaded" (`receipts/r412-3-rerun/census_mutant_M9_by_name_only.log`). M1-M8 are each killed by the control that names their pin (M1, M7: `&aem_loaded` escape; M2: alias one-name; M3: external linkage; M4: bare AUIPC; M5: `#ifndef __PIE__` write; M6: resolver store; M8: second assignment).
- The unplanted head passes the whole gate 1b with the slot kept and "refused 15/15 … one of them reaching it only at byte(s) +1 of its storage" (`receipts/r412-3-rerun/gate1b_full_base.log`). BAREMETAL_FIRMWARE.md's table now has fifteen rows and says "fifteen breaks".
- No firmware change: `git diff 597dba85..HEAD -- sw/firmware` is empty. `milan_baremetal.c` sha256 `a73ecc25…0eb3` equals the capture receipt's `product_firmware_sha256`.

## Findings

### R413-4 F1 - MINOR - Tests, Docs - the interior-byte break measures byte +1 only, but is described as measuring the census's four-byte range

- Where: `sw/builder/test_builder.py:14616-14620` ("so it is the break that measures the census's four-byte range") and `:17213-17215` (the printed closing line: "one of them reaching it only at byte(s) +1 of its storage, which measures the census's four-byte range"). Also `docs/integration/BAREMETAL_FIRMWARE.md:1026-1030` ("It is the one break that measures the census's four-byte range").
- Authority: AGENTS.md section 6, Tests lens: "Each new test can fail for the defect it claims to detect". Round 4's ruled standard is that the texts claim only what is proven (#70 5909983141 item 1). R412-3 F2 (MINOR, accepted for fix) was this defect class: "a census narrowed to the verdict's first byte passes gate 1b".
- Evidence:
  - Census mutants that narrow `rv32_image_references()`'s range at `test_builder.py:2149` pass every verdict control of gate 1b: premise `interior_bytes=[1]`, base kept, forget-on-call refused, "refused=15/15". These are N1 `[low, low+2)`, N2 `[low, high-1)` and N4 `{low, low+1}` (`receipts/r413/census_stop_N1_first_two_bytes.log`, `census_stop_N2_first_three.log`, `census_stop_N4_second_byte_only.log`). The reference run of the unmutated head gives the same line (`census_stop_none.log`). N3 `(low, high)` is killed by the base (`census_stop_N3_skip_first_byte.log`).
  - Under N1, the `interior_b2_sscanf` and `interior_b3_sscanf` plants are ACCEPTED with the slot kept (`receipts/r413/mutant_probe_N1_first_two_bytes_interior_b2_sscanf.log`, `…_b3_sscanf.log`). At the unmutated head both are refused on escape (`receipts/r413/gate1b_early_interior_b2_sscanf.log`, `…_b3_sscanf.log`).
- Impact: no product or soundness defect at this head, because the census reads all four bytes. But a future edit that narrows the census so it drops the verdict's upper bytes would pass gate 1b, while the gate's own line says the range is measured. A write through a folded address at byte +2 or +3 would then keep the slot with the verdict unproven. That is the regression R412-3 F2 asked a control to catch, and the control catches only its first-byte instance.
- Required outcome: either (a) a planted control whose only verdict reference is at the verdict's last byte, +3, or controls at +2 and +3. Its premise is checked as now, so every range narrowing that starts at the first byte (M9, N1, N2, N4) is killed. Or (b) the three texts are bounded to what the +1 break measures, that the census reads past the verdict's first byte, and do not say "four-byte range". Either suffices. (a) is expected to kill N1, N2 and N4, since the +3 plant is refused at the head and accepted under N1; that prediction is not yet measured.
- Verification: rerun `scripts/r413_census_stop_run.sh` (N1-N4, `none`) and R412-3's `census_mutants_run.sh` (M1-M9) at the new head. For (a), M9, N1, N2 and N4 are killed and the head passes with the slot kept. For (b), a text search of `test_builder.py`, `BAREMETAL_FIRMWARE.md` and the closing line finds no "four-byte range" claim for this break. Rerun the docs gates.

No other finding. Considered and not raised:

- The round-1 PR-body summary "three pins hold (one write, the verifier's; …)" names a pin and is historical. Its section points forward to round 4's bound.
- The CHANGELOG line "So does an overrun of another object onto the verdict." is a one-line summary of limit 2, consistent with the page.
- The refusal row at `BAREMETAL_FIRMWARE.md:1634` ("The address of `aem_loaded` may not be taken") describes the early diagnostic, not the verdict's proof.

## Disposition of prior public review findings at this head

| Prior finding | Status at `5b4a47e9` | Evidence |
|---|---|---|
| R412-3 F1 (MINOR; Docs, Conformance, Robustness): a called function writing through another object's pointer reaches the verdict, and the texts claimed nothing else writes it | RESOLVED as ruled (accepted as a second stated limit, recorded on #495 5909985902). Every text named in the ruling now claims only the bounded proof and names both limits. Both probes match the limit's words. | Item 1 above; `receipts/r412-3-rerun/gate1b_{early,full}_{nbr_runtime,pre_overrun}_sscanf.log` |
| R412-3 F2 (MINOR; Tests): no control measures the four-byte range; M9 survives | RESOLVED as ruled: M9 is killed by the new break, M1-M8 stay killed, and the head passes. The residual narrowing (bytes +2 and +3 unmeasured, while the text says four-byte range) is raised as the new R413-4 F1, not retained as this finding. | `receipts/r412-3-rerun/census_mutant_M*.log`; `receipts/r413/census_stop_*.log` |
| Findings of rounds 1-3 (R412-1/2, R413-1/2) | Resolved at round 3 (R413-3 POSITIVE at `0a80abcb`). Nothing in their scope moved except the gate-1b texts judged above. All 25 R412-3 probes, which include the earlier rounds' spellings, give their round-3 outcomes. | `receipts/r412-3-rerun/gate1b_early_*.log` |

## Per-lens results at this head

[R413] PASS Conformance - #70 5909983141 items 1-2 against `sw/builder/test_builder.py:1631-1677,6899-6933,14616-14757,17209-17222`, `docs/integration/BAREMETAL_FIRMWARE.md:933-1032,1638`, `CHANGELOG.md:65-66` and the PR body round 4 - Every ruled item is implemented: the bounded claim, both limits named at every listed text, a planted control on an interior byte refused on escape, M9 killed, M1-M8 killed, the head passes with the slot kept, and no firmware, RTL or bitstream change (`receipts/scope_and_digest.log`). #70's saved-state acceptance scope is unchanged since round 3.

[R413] PASS RTL - `receipts/scope_and_digest.log` - `git diff 0a80abcb..5b4a47e9 -- hdl protocol-processor gptp-processor third_party external sw/firmware sw/litex syn .github tb` is empty and the gitlinks are unchanged. The round-4 hunks in `test_builder.py` (rule comment, docstring, one planted break, a premise check and the closing line) touch no RTL-reading rule. RTL was covered clean by R413-3 at `0a80abcb`, an ancestor, and nothing in RTL scope changed since.

[R413] PASS Robustness - `receipts/r412-3-rerun/gate1b_early_*.log` (25), `receipts/r412-3-rerun/gate1b_full_*.log` (3), `receipts/r413/gate1b_early_*.log` (9) - Malformed and hostile firmware edits against gate 1b: every accepted write is inside the stated limits' words, and every refusal happens where the texts say it does. The firmware is byte-identical to `597dba85` (digest equals the capture receipt).

[R413] UNCLEAN Tests - R413-4 F1. Artifacts: whole gate 1b at the head, base and the two F1 probes (`GATE1B PASS`, 15/15); census mutants M1-M9, all killed; the premise check (`interior_bytes=[1]`); range mutants N1-N4, with N1, N2 and N4 surviving every verdict control; N1 with the +2 and +3 plants; `check_nvm_capture` rc 0.

[R413] UNCLEAN Docs - R413-4 F1. Artifacts: `BAREMETAL_FIRMWARE.md:808-821,933-1032,1634-1643`, `test_builder.py:1631-1677,6899-6933,14595-14620,14733-14757,17209-17222`, `CHANGELOG.md:58-70`, the PR body (all rounds). The docs gates are rc 0 (`receipts/docs_gates.log`). The F1 texts are correct and bounded; the "four-byte range" sentence overclaims.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #70 assignment 5909983141 and #495 record 5909985902 against the round-4 texts and controls; PR body; scope diff | R413-4 | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |
| RTL | CLEAN | Scope diff since `0a80abcb` empty in RTL, firmware, SoC and CI scope; round-4 builder hunks read; gitlinks | R413-4 (RTL first covered clean by R413-3 at ancestor `0a80abcb`, untouched since) | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |
| Robustness | CLEAN | 25 R412-3 probes, 3 whole-gate probe runs, 9 own probes of the bounded claim; firmware digest | R413-4 | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |
| Tests | UNCLEAN (R413-4 F1) | Whole gate 1b on the head and the F1 probes; M1-M9; premise check; N1-N4; N1 with the +2 and +3 plants; `check_nvm_capture` | R413-4 | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |
| Docs | UNCLEAN (R413-4 F1) | `BAREMETAL_FIRMWARE.md` verdict section, table and refusal rows; rule comment, docstring and closing line; CHANGELOG; PR body; 10 docs, idiom and capture gates rc 0 | R413-4 | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |

## Real limits of this round

- N1-N4 were run with gate 1b stopped immediately after its verdict controls, not through the whole gate. Their survival is shown for every verdict control (the premise, the base, forget-on-call and all 15 breaks). It is not shown for gate 1b's later, unrelated controls. A first whole-gate attempt on N1 and N2 was stopped by the session's time limit before finishing. Its incomplete logs are kept, clearly marked, in `receipts/r413/invalid/` and are not evidence.
- The prediction that a +3 control kills N1, N2, N4 and M9 is inferred (the +3 plant is refused at the head and accepted under N1), not measured.
- All layouts are the census image's own: one unit linked alone at the gate's layout. The product's link is not built here, as the stated literal limit already says.
- I did not run the full builder bank (with or without the compiler), the grader mutants or the service-budget self-test. I rely on the author and manager receipts at this head for those (`author-r4/receipts/gates-5b4a47e9/`: builder-present rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN"; builder-absent rc 0).
- Hosted checks at the exact head (snapshot in `receipts/hosted_checks.log`): 17 completed with success, including rtl-fast, full-ci-gate, docs-check, elaborate, Yosys shards 0-3 and Verilator shards 0, 2 and 3. Verilator shards 1/5 and 4/5 were still in progress at the snapshot. "Physical gPTP (nightly and manual)" was skipped, which is not execution.
- Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware, Docker or act was used.

## Pending manager duties

- Rule on R413-4 F1: remedy (a), a control at the verdict's last byte, or (b), text bounded to what the +1 break measures.
- Hosted and act acceptance at the exact head, including the two Verilator shards in progress at the snapshot.
- Build and validate the final current-dev candidate at the merge turn (source base `79c36963`, live dev `ccdd07b5` at assignment). Then post-merge containment.
- Keep the #495 residue record (literal address; neighbour overrun) current.
- A second independent positive review at the merge head is still required.

R413-4 FINISHED
