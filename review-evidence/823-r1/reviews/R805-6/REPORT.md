[R805] POSITIVE - exact head 2905c8749a4573450b9999dd546bb20ae5c7fc38

Internal cleared-context review of #823 / PR #880 (`823-format` -> `dev-soft-core`), round R805-6.
Head `2905c8749a4573450b9999dd546bb20ae5c7fc38`, tree `c28f687748dec7d97d4346844d5bfce183aa010d`.
Merge base `dev-soft-core` `1d6bf555`. The previously reviewed head of this content is `30ca4b21` (R805-4, NEGATIVE on two Docs MINORs).
This round judges the delta `30ca4b21..2905c874` (7 commits, 21 files, +215/-80) and every named prior finding. Code outside that delta keeps its R805-4 lens verdict unless the delta changes what it depends on.

No BLOCKER, MAJOR or MINOR is open. Two RESIDUE items and three SUGGESTIONs are recorded below. All five lenses are covered clean at this head.

## Scope, reconstructed from public state

- Issue #823 body and its 2026-10-30 amendment. Rulings: round 2 (issuecomment-6730773797, decisions 1-7), round 3 (issuecomment-6730985093: the format is the split placement's only, no processor or `KL_nvm_backend` change, no RTL `$error`), the VERSION ruling (issuecomment-6739542795: the gateware CSR is not moved), round 4 (issuecomment-6742264763), round 5 (issuecomment-6754858510, items 2-5), and the round 6 ruling (PR #863 issuecomment-6767385787).
- Round 6 makes #823 the format only, in a new PR from `30ca4b21`. It adds round 5 items 2-5 (N1, N2, RS5, RS6, RS-a, RS-b, SG3/S-a, SG4/S-b, S-c), RS-d and R806-5 R2, and nothing of the save path. The page and the PR body must say section 4 is designed here and built under #876. #818's route is waived while the head changes no HDL, gitlink or generated SoC RTL, and the memory table at `30ca4b21` is the area evidence (57.5 RAMB36). The PR closes #823.
- Out of scope by ruling: the append-only save path (#876), the 32x32 save bound (#877), the RTL `$error` (the split has no RTL for this space), the gateware VERSION CSR, and the TDM8 32x32 AEM ROM limit (#859).

## Evidence examined and probes run

All logs below are in this packet. Every probe ran in my clone at the exact head. The clone was verified as restored afterwards (`receipts/restore_check.txt`).

| Check | Result | Receipt |
|---|---|---|
| `scripts/nvm_layout3.py` | rc 0 | `receipts/gates/layout3.*` |
| `scripts/check_nvm_klj3.py --self-test` | rc 0, `all 6 planted defects caught` | `receipts/gates/klj3_selftest.*` |
| `scripts/check_nvm_format_32x32.py` | rc 0, `0 finding(s)` | `receipts/gates/fmt_gate.*` |
| `scripts/check_nvm_format_32x32.py --self-test` | rc 0. Each of the six line-number plants is caught by the whole citation it names. `control moved-lines: 0 finding(s)`. `self-test: PASS` | `receipts/gates/fmt_selftest.*` |
| `sw/litex/flash_map.py` | rc 0. `journal_klj3` at `0x0E40000`, 640 KiB. `journal` at `0x0EE0000`, 128 KiB | `receipts/gates/flash_map.*` |
| `sw/firmware/gtest/fw_coverage.py --check` | rc 0, `firmware coverage: PASS (35 files)` | `receipts/gates/fw_cov.*` |
| Builder gates 38 and 39 (`--gates`) | rc 0. Gate 39 `10/10 planted defects`. Subset verdict only | `receipts/gates/builder_g38_39.*` |
| `test_ctrl_nvm.py --self-test --jobs 16` | rc 0. `OK across 5 shape(s), 506 tests, and all 132 planted defects reddened`. `at width: MILAN_NVM3_MAPIN_ENTRIES_0 = 255 ... compiles`. `doctored build outside the host test: refused at compile time`. Controls `mapin_limit_one_early` and `doctored_error_removed` caught. The RV32 arm ran: stage 3,454 B at 1x1 and 13,594 B at 8x8 two-interface | `receipts/store/test_ctrl_nvm_selftest.*` |
| HDL, gitlink and generated-RTL diff against `1d6bf555` | Empty. The six gitlinks hash equal at both commits | `receipts/gates/hdl_diff.*`, `receipts/gitlinks_head.txt` |
| Line-citation regex probe | All 11 claimed forms match. Gaps outside the claim: see SG1 | `scripts/probe_line_cite.py`, `receipts/probe_line_cite.log` |
| `git diff --check 1d6bf555 HEAD` | rc 0 | this report |
| Commit hygiene `30ca4b21..HEAD` | 7 commits, each one line, one parent, no trailer | this report |
| Published author evidence (`review-evidence/823-r1` at `12ebd8b9`) | 7 receipts recomputed. Every one matches its `MANIFEST.json` `published_sha256`. `verify.md` tallies 152 rc 0 (145 at `2905c874`, 7 carried from `e0adcc09`), 198 NOT RUN with a reason, and no other rc. `e0adcc09..2905c874` changes only one line of `scripts/check_nvm_format_32x32.py`. `firmware-unit`'s steps neither run nor scan that file, so the carry holds | `receipts/evidence_hashes.txt` |

The evidence commit `12ebd8b9` carries no git signature. I took "signed" to mean the manifest's digests and checked those.

## Findings

### RS1 - RESIDUE - Docs - `scripts/nvm_format_32x32_tables.py:427` - lane label left in a source docstring

- **Evidence:** `"""Section 3: the ppmem window and the F1 stage."""`. F1 is #665's lane label. RS-a (R806-4, ruled in round 5 item 4) asked for "(#665, the split placement's saved-state store)" in the three named headers "and the other comment instances". REVIEW READY says the same wording replaced the lane label in the branch's other comments, and lists six files. This file is not among them, and the docstring is the one source-comment instance left in the PR's additions. The other "F1" strings in that file are the page's generated labels and anchors, which the author kept unchanged, as R806-5 also read them.
- **Authority:** the owner comment rule of 2026-10-15.
- **Impact:** wording only. It changes no figure, test, code path or generated output, because the docstring is not rendered.
- **Exact fix:** `"""Section 3: the ppmem window and the split store's stage."""`.
- **Verification:** `rg -n '"""[^"]*\bF1\b|#.*\bF1\b' scripts/nvm_format_32x32_tables.py` prints nothing, and the drift gate stays at 0 findings.

### RS2 - RESIDUE - Tests (wording) - `sw/firmware/ctrl_nvm/test/nvm_bench.py:114` - the Bench docstring names the KLJ2 reference

- **Evidence:** `"""One shape's reference side: its frames and how nvm_klj2.py packs them."""`. The class's methods call `klj3_assemble` and `klj3_decode` (lines 129-140), and the module header (line 6) names `scripts/nvm_klj3.py`. This round edited the file. The author reported the line as found and not changed, because it is outside the ruled lists.
- **Impact:** wording only. No assertion or verdict depends on it.
- **Exact fix:** "how nvm_klj3.py packs them".
- **Verification:** read line 114 against `assemble` and `decode`.

### SG1 - SUGGESTION - Tests - `scripts/check_nvm_format_32x32.py` `LINE_CITE_RE`

- `receipts/probe_line_cite.log` shows that every form the docstring claims is refused: `path:N`, a range, a list (each quoted or not), "`path` line(s) N" and `#L` links.
- Not refused, and not claimed:
  - an extensionless file, `Makefile:12`;
  - an unquoted "path line 12";
  - "`path`, line 12";
  - "path lines 12 to 34".
- One false positive, which fails closed: a URL with a port, `https://example.com:8080/x`, matches as `//example.com:8080`.
- The page carries none of these today.
- Optional: widen the pattern if the page may ever cite such forms. The PR body's "no line number in any form" could also read "in any of these forms".

### SG2 - SUGGESTION - Tests - `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py` `at_width_control`

- The control counts as caught on any compile failure (`"does not compile" in x`), not on the input-width refusal's own words.
- The planted mutant is narrow, so this cannot mask a defect today.
- Requiring the message "an input map's entries outgrow the codec's byte table" would match how `doctored_outside` and `over_width` grade theirs.

### SG3 - SUGGESTION - Docs/process - the #818 waiver's generated-RTL comparison

- The waiver compares only the AX7101 shipping SoC. The author discloses this.
- At this head `milan_soc.py` adds only `soc.add_constant` values and a `FLASHBOOT_RESERVED` entry, which feed the firmware header and the flash layout, not the Verilog. The delta since `30ca4b21` does not touch `sw/litex`.
- So the waiver's condition holds by inspection. I did not elaborate the split SoC myself.
- Optional: one sentence in the PR body saying why the split SoC's Verilog cannot change would close the gap for a cold reader.

## Delta verification by ruled item (`30ca4b21..2905c874`)

| Item | Status at this head | Evidence |
|---|---|---|
| N1 (R805-4 N1 = R806-4 N1, MINOR Docs) | **Resolved** | `SPLIT_CONTROL_MEMORY.md:144` reads "3,344 against 13,264 bytes", and lines 146-147 say they are KLJ2 sizes as `c20ed894` linked them. That agrees with section 5 line 176 ("3,344 / 13,264 B in KLJ2 ... 3,454 / 13,594 B in the split's KLJ3"). The KLJ3 figures match my RV32 arm output (stage 3,454 and 13,594). `c20ed894` is an ancestor of the head. |
| N2 (R805-4 N2 = R806-4 N2, MINOR Docs) | **Resolved** | `QSPI_FLASHBOOT.md:58-69` points to FASTCONNECT section 5 and names each owner. That matches FASTCONNECT lines 543-545 and 555-558. `milan_baremetal.c:329-331` addresses the `journal` slots. `nvm_legacy_check` in `nvm_store.c` (line 415) only calls `f->read` on `NVM_LEGACY_A + i * slot`. No "nothing writes or reads" or blank-flash sentence is left. |
| RS5, RS6 (R805-4) | **Resolved** | FASTCONNECT line 101 names "three reserved slots" and both journals. Line 118 adds `journal_klj3` at `0xE4_0000`, 640 KiB. `0xE40000 + 0xA0000 = 0xEE0000`, so it sits directly below `journal`. |
| RS-a (R806-4) | **Resolved in the named places**, one instance left (RS1) | `nvm_klj2.c:3-5`, `nvm_klj2.h:4-5` and `nvm_shape.h:4-5` now read "(#665, the split placement's saved-state store)". So do the comments of `nvm_layout3.h`, `nvm_layout3.py`, `nvm_klj3.py`, `check_nvm_klj3.py`, `endstation_builder.py` and `test_builder.py`. |
| RS-b (R806-4) | **Resolved** | The six places in `test_nvm_write.cpp` say `nvm_klj3.py`. `nvm_rig.cpp:179` and `test_nvm_boot.cpp:12` keep `nvm_klj2.py`, as ruled. |
| RS-c = SG5 | **Retained, out of lane** | Carried to #495 by the round 5 ruling. FASTCONNECT section 5.1 is not in this delta. |
| RS-d (R805-5) = R1 (R806-5) | **Resolved** | `nvm_rig.hpp:18` and `nvm_suite.hpp:9` say `scripts/nvm_klj3.py`. |
| R2 (R806-5) | **Resolved** | Page section 4, A3: "The room, taken from the all-fabric worst case (404.71 ms) and so conservative for the split, is 95.29 ms". Both figures are drift-gated (`fig:fabric_ms`, `fig:susp_allow_ms`). The arithmetic holds: 500 - 404.71 = 95.29, and 95.29 ms / 15 us = 6,352.7, so 6,352 is right. The PR body's item table uses the same wording. |
| SG3 = S-a | **Done** | The regex is widened and has six plants, each checked against the whole citation it names. A plant that matched only a prefix would therefore not pass. I confirmed this with the probe. `2905c874` moves the list-form plant to `scripts/nvm_klj3.py:408,465`, which the firmware boundary does not read as a firmware builder (`ctrl_boundary: PASS` in the author's receipts). |
| SG4 = S-b | **Done** | `at_width` compiles `nvm_klj2.c` with `MAPIN_ENTRIES_0 = 255` and every warning as an error. Control `>= 255u` is caught (my run). `over_width` already shows index 0 is in `NVM_SUM32`, so the boundary is a real one. |
| S-c | **Done** | `nvm_shape.h:180-182` adds an `#error` after `nvm_shape_gen.h` is included (line 35). `NVM_HOST_TEST` is defined only by `nvm_bench.shape_header(host_test=True)`, which only `build_suite` passes. Nothing else in the tree defines it (`rg`). `doctored_outside` requires the error's words, and its control is caught by an exact-match check. The doctored suite binary still builds, because the full gate is green. |
| Section 4 under #876 | **Done** | Changed: the status lines 6-7, the contents entry, the section 4 lead (lines 240-242), section 3 line 208, section 9 and the generated T7-T13 and T15 cells ("built under #876", through `nvm_format_32x32_tables.py`). No claim says the append path is built. `nvm_store.c` and `nvm_store.h` are unchanged since `30ca4b21`, and the store has no suspend or resume code. |
| #818 waiver | **Done, condition verified** | Page section 7 states the waiver, links `SPLIT_CONTROL_MEMORY.md#5-fit` (the heading exists) and gives 57.5 RAMB36, which agrees with line 228. The HDL, gitlink and generated diff is empty (my run). |
| Comment rule on the delta | **Clean** | Every added non-Markdown line of `30ca4b21..HEAD` was scanned for lane labels, round labels, reviewer IDs and comment IDs. The only hit is "DR3b", a design-rule ID already on the re-wrapped line, so it is not a lane label. RS1 is earlier in the PR, not in this delta. |

The prior MAJORs of R805-5 and R806-5 are on the append path at `7c97e99f`. The round 6 ruling moved them with #876, and none of that code is on this head, so they do not apply here. They stay open under #876.

## Lens results

- **[R805] PASS Conformance** - artifacts: the round 3 and round 6 rulings against the page's sections 2, 4, 5, 7 and 9. Gate 39 (907 names accepted, 908 refused, the all-fabric header still refuses). The store suite's NAME first, last and one-past tests and its KLJ2 refusal tests (506 tests, rc 0). The VERSION wording against issuecomment-6739542795. The R2 room arithmetic against the owner's 0.5 s bound. Every frozen acceptance item that the rulings left in #823 is met or ruled out, and the delta adds no conformance claim beyond them.
- **[R805] PASS RTL** - artifact: `git diff --name-only 1d6bf555 HEAD` filtered to HDL, `syn`, submodules and `configs/generated` is empty. The six gitlinks are equal at both commits. The delta since `30ca4b21` touches no `sw/litex` file, and the `milan_soc.py` change in the PR adds firmware constants and a flash-map entry only. The processor, `KL_nvm_backend` and `milan_baremetal.c` are unchanged.
- **[R805] PASS Robustness** - artifacts: `nvm_shape.h:170-188`, the refusal ordering and the new `#error` placed after the generated header. `at_width` (the 255 boundary) and `doctored_outside` (the seam is test-only), each with a caught control in my run. The `legacy` read-only path in `nvm_store.c` was re-checked for N2. Nothing in the delta changes run-time store behaviour (`nvm_store.c` and `nvm_klj2.c` code are unchanged; `nvm_klj2.c` changes in comments only).
- **[R805] PASS Tests** - artifacts: `test_ctrl_nvm.py` (`at_width`, `doctored_outside`, their controls, `CONTROLS` = 5, total 132), and `nvm_bench.py` `host_test`. `check_nvm_format_32x32.py` has six plants, each graded on the whole citation, plus my regex probe. My run of the store self-test rc 0, with 132 of 132 reddened. Each new test can fail for its defect: every control is caught. RS2 is wording only, and SG2 is optional.
- **[R805] PASS Docs** - artifacts: `SAVED_STATE_FORMAT_32X32.md` (the delta hunks, drift gate 0 findings), `SAVED_STATE_FASTCONNECT.md:101,118,533-558`, `QSPI_FLASHBOOT.md:58-69`, `SPLIT_CONTROL_MEMORY.md:140-147,172-228`, `sw/firmware/ctrl_nvm/README.md:451-457,556-559`, and the PR #880 body. N1 and N2 are resolved, and RS1 is wording only.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | rulings vs page sections 2, 4, 5, 7 and 9; gate 39; the store's NAME and KLJ2 tests; VERSION wording; R2 arithmetic | R805-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |
| RTL | CLEAN | HDL, gitlink and generated diff vs `1d6bf555` (empty); gitlink hashes; `milan_soc.py` PR hunks | R805-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |
| Robustness | CLEAN | `nvm_shape.h:170-188`; `at_width` and `doctored_outside` plus their controls; `nvm_legacy_check` read path | R805-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |
| Tests | CLEAN | `test_ctrl_nvm.py` and `nvm_bench.py` delta; drift gate plants and regex probe; store self-test 132/132 (my run) | R805-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |
| Docs | CLEAN | format page delta; FASTCONNECT 101, 118 and section 5; QSPI_FLASHBOOT 58-69; SPLIT_CONTROL_MEMORY 140-147 and section 5; store README; PR body | R805-6 | `2905c8749a4573450b9999dd546bb20ae5c7fc38` |

All five lenses were applied at this exact head, against the delta and the code it depends on. Code the delta does not touch keeps R805-4's clean verdicts at `30ca4b21` for Conformance, RTL, Robustness and Tests. Docs was R805-4's only unclean lens, and it is clean here.

## Real limits

- No RV32 compiler is on this host's PATH, and I did not pass `--require-rv32`. The gate's RV32 arm still ran and printed section sizes. The author's `--require-rv32` run is the receipt for that flag.
- I did not run the full sweep, the full builder bank, the workflows step by step, the LiteX simulations, the twin, the AX7101 elaboration or any Vivado run. For those I relied on the author's receipts, whose hashes I verified, and I spot-checked `verify.md`, `SUMMARY.md`, the store self-test log, the `capture_coherence` re-run and the waiver's diff file.
- Hosted CI at this head was still queued or in progress when checked: 2 completed successfully, 12 queued or in progress (`receipts/hosted_check_runs.tsv`). I make no hosted claim.
- No manager source bank ran at this head, and I claim none. The current-dev merge candidate (`dev-soft-core` live tip against base `1d6bf555`) is not validated here.
- Physical calibration was NOT RUN. The 15 us suspend latency is a datasheet typical value. No field or hardware proof exists, and none is claimed.

## Pending manager duties

- Validate the current `dev-soft-core` merge candidate (builder and native banks) at the merge turn, and link its receipts on PR #880.
- Own the hosted and act acceptance at the exact head: `rtl-fast`, plus `verilator-suites` and `yosys-portability` once the PR is ready.
- Carry RS1 and RS2 to the residue checklist. RS-c/SG5 is already on #495.
- Keep the R805-5 and R806-5 append-path MAJORs on #876 and PR #863.
- Merge needs the external positive review and explicit maintainer authorization.

R805-6 FINISHED
