[R384] NEGATIVE - exact head a53682ed38720de758006602a19f78c8e40d69da

# [R384] Review round R384-1: PR #612 / issue #577 (F6: L6 identity list and L10 AUDIO_UNIT offset/count/length at the shipping image boundary)

- Role: internal independent reviewer, cleared context. Executor of the lane: [A410].
- Exact head reviewed: `a53682ed38720de758006602a19f78c8e40d69da`, tree `e434badd5de9c04bebc451f8abbde187c06b8cae`.
- Source base: `54ce877371ee6e8878cf67294e86c2a8481b62f6` (one commit, four files: `sw/builder/aem_image_checks.py` new, `sw/builder/endstation_builder.py` +6, `sw/builder/test_builder.py` +144, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` +45/-6).
- Authorities read: AGENTS.md, CONTRIBUTING.md (by reference), issue #577 body and assignment comment 5865331676 (manager decisions 1-6), TAKEN and REVIEW READY comments, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (L6, L10, F6 and the measurement section), `docs/ENDSTATION_BUILDER.md` (image supply-chain text and row 8), pinned processor `protocol-processor/hdl/aecp/ucode/gen_ucode.py` (SET_SAMPLING_RATE walk and SET_CLOCK_SOURCE range check) and `protocol-processor/hdl/aecp/desc/gen_desc_image.py` (AEMI v1 layout).
- Clauses I checked myself: IEEE 1722.1-2021 7.2.3 (Table 7-5: 136 current_sampling_rate, 140 sampling_rates_offset "144 for this version of AEM", 142 count, 144 4*S list), 7.2.32 (Table 7-61: 70 clock_source_index, 72 clock_sources_offset "76 for this version of AEM", 74 count, 76 2*C list), 7.4.21 and 7.4.23; Milan v1.2 5.3.3.3 (current_sampling_rate shall be one of the listed rates) and 5.3.3.6.
- Public executable evidence: `review-evidence/577-r1` at `d13de9c5f2f03f8c4cb7327f46ae9e508e94b29e` (read: `mutants.json`, `check_mutants.py`, `images.json`, `processor-integrity.json`, `PR-BODY.md`, `builder-gates.json`).

## Verdict

NEGATIVE. The checker itself is correct and well tested for every refusal the assignment names, but it does not guard the image that is actually shipped (F1, MAJOR). It also accepts a zero-entry rate list below the legal one-entry boundary (F2, MINOR). Four lenses are UNCLEAN. RTL is CLEAN.

## What I verified (independently, at the exact head)

| Question from the brief | Result | Receipt |
|---|---|---|
| (1) The check reads packed bytes, independently of `_load_clocking` / `_validate_output_clock_sources`, and a planted image fault is caught after the loader passes | Yes, for the builder function `_entity_model_image` (`sw/builder/endstation_builder.py:2308-2312`). Field positions are IEEE wire positions (140/142, 72/74), and I checked them against Tables 7-5 and 7-61. Descriptor locations, lengths, strides and runs come from the AEMI v1 index (`gen_desc_image.py:53-80`: 16-byte rows `>HHHHIHH`, header +4 version, +8 n_entries, +0x0C index_off). The walk offset 144 and bound 8 are parsed with `ast` from the pinned consumer (`gen_ucode.py:1329-1330`), not imported from builder constants. **But** the deployed `aem_desc.bin` is produced by a second emitter that does not call the check (F1) | `receipts/gate36b_head.log`, `receipts/soc_path_probe.log`; mutants "consumer walk bound 9" and "consumer list offset 148" in `receipts/mutants.log` prove the consumer values are live |
| (2) L10 accept 1 and 8 entries at 144+4N; refuse wrong offset, count 9, count>extent, one byte short, one word long, each with its own name | Yes: `L10_OFFSET`, `L10_COUNT`, `L10_COUNT_EXTENT`, `L10_PARTIAL_WORD`, `L10_EXTRA_WORDS`. Count 0 is accepted (F2) | `receipts/gate36b_head.log`, `receipts/edge_probe.log` |
| (3) L6 accept `[0,1]` (and `[0]`); refuse `[1,0]`, gap, duplicate with names | Yes: `L6_ORDER`, `L6_GAP`, `L6_DUPLICATE`, plus `L6_EMPTY` and `L6_EXTENT` | `receipts/gate36b_head.log` |
| (4) One removed-check mutant per refusal class, killed; five configurations pass with unchanged images | 19 of 19 of my own mutants are killed. They cover the 8 named refusals, the 4 defensive refusals, hook removal, index-0-only and configuration-0-only walks, CLOCK_DOMAIN skip, stride used as length, and 2 consumer-constant drifts. My mutants delete the condition. In that form, removing `L10_PARTIAL_WORD`, `L6_DUPLICATE` or `L6_GAP` is killed by a *different* named refusal, not by acceptance, so the refusals are layered. The published campaign replaces `raise` with `pass` and is killed by acceptance. Both forms fail the committed test. Base and head `aem_desc.bin` for all five configurations are byte-identical | `receipts/mutants.log`, `receipts/images_base.txt`, `receipts/images_head.txt`, `receipts/images_compare.txt` |
| (5) #478 loader scope not widened; no processor source or gitlink change | Yes. `endstation_builder.py` gains only the import (line 72) and the hook (2308-2312). `_load_clocking` and `_validate_output_clock_sources` have identical source hashes at base and head. Gitlinks are identical, and the diff touches no submodule | `receipts/scope.txt` |
| (6) F6 and L6/L10 matrix rows record the check and its evidence accurately | The case table (`PP_DESCRIPTOR_OWNERSHIP.md:199-213`) matches the executed outcomes line for line. The claim that `_entity_model_image` "packs the shipping image" (`:181-182`, `:318`) does not match the code path that writes the deployed image (F1) | `receipts/gate36b_head.log`, `receipts/soc_path_probe.log` |

## Findings

### F1: MAJOR: Conformance, Robustness, Tests, Docs: the check does not run on the emitter that writes the deployed `aem_desc.bin`

- Where: `sw/litex/milan_soc.py:3331-3366` (`build_desc_image`: its own `gen_aem_store` -> `gen_aemi_image` -> `gen_desc_image.build(..., 576)` join); `sw/litex/milan_soc.py:3946-3960` (the blob's length and CRC32 become firmware constants); `sw/litex/milan_soc.py:4010-4012` (writes `aem_desc.bin` beside the bitstream, which `sw/litex/deploy.sh` installs). The hook is only in `sw/builder/endstation_builder.py:2308-2312` (`_entity_model_image`). At this head that function has no production caller: its callers are `sw/builder/test_builder.py` and `scripts/audit_pp_descriptors.py:136`. `build()`, `--write-rtl` and `--write-fragment` do not call it, and `sw/litex/build.sh:315` runs the builder CLI, which emits no image. New docs text: `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:181-182` and `:318` ("after `B._entity_model_image` packs the shipping image").
- Authority: issue #577 title and body ("at the shipping image boundary"), and F6 in the ownership document. Assignment decision 1 places the check on "the packed descriptor image the builder emits for a shipping configuration ... so a fault planted in the image is caught even when the loader-side checks pass". AGENTS.md section 2: a conflict between the issue's wording and the implementation must be published, not resolved privately.
- Evidence: `receipts/soc_path_probe.log` (script `scripts/soc_path_probe.py`). At this head, one `[1,0]` CLOCK_DOMAIN fault is planted at the packer. The builder function refuses it (`L6_ORDER`). The SoC emitter, executed from its own source text with only the overlay-path lookup stubbed, **accepts** it and returns the `[1,0]` image it would write as `aem_desc.bin`. Without a fault, the two emitters produce byte-identical images for all five configurations. So the shipped bytes at this commit do satisfy L6/L10. What the probe shows is that nothing on the deployment path enforces it.
- Further evidence: `receipts/cli_reach_probe.log` (script `scripts/cli_reach_probe.sh`). The PR body's "How to reproduce" command is `python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml -o ...`. I ran it with the checker forced to raise on every call, and it still returns rc 0, never reaches the checker, and emits no `aem_desc*` file. The same forced checker makes `_entity_model_image` refuse (control). So the documented reproduction does not exercise the change.
- Impact: the new refusals are enforced only when the builder test bank (or the audit script) runs. They are not enforced where the product image is created, CRC-bound into firmware and flashed. A producer or overlay fault that reaches the SoC path (for example a stale or hand-edited `aem_overlay.json` in the entity-gen directory, which `build_desc_image` reads, or a build run without the builder bank) ships silently. The ownership document now states that F6 is enforced at the shipping image, which overstates that boundary for a cold reader. `docs/ENDSTATION_BUILDER.md:213` and `:578-582` already say that `_entity_model_image()` generates the deployed set under `--write-rtl`/`--write-fragment`, and the code does not. That drift predates this PR, but the new F6 text relies on it.
- Required outcome: one of the following.
  - (a) Every emitter of the deployed image runs `validate_shipping_image` on the exact bytes it writes, and it refuses before the image is written or CRC-bound. A committed test must fail if the SoC emitter bypasses the check.
  - (b) A recorded public maintainer or manager decision that the builder-side image and bank are the enforcement boundary for F6. In that case, `PP_DESCRIPTOR_OWNERSHIP.md:181-182` and `:318` must state that the check guards the builder's image and that the SoC emitter is equivalent by construction, not by check, and must cite the evidence for that equivalence.
- Verification: re-run `scripts/soc_path_probe.py` at the new head. Under (a), branch B must report `REFUSED` with `L6_ORDER`. Under (b), the decision link and the corrected text must be present and the probe result must be stated in the document or PR.

### F2: MINOR: Conformance, Robustness, Tests: a zero-entry sampling-rate list passes the shipping check

- Where: `sw/builder/aem_image_checks.py:39-57` (`_audio_unit`). With offset 144 and count 0 at length 144, every test passes: the count is at most 8, and the extent of 0 words equals the count. The gate 36b fixture list (`sw/builder/test_builder.py:27257-27275`) has no zero-count case.
- Authority: Milan v1.2 5.3.3.3: "An AUDIO_UNIT descriptor shall always report a sampling rate in the current_sampling_rate field that is one of the supported sampling rates described by the sampling rates list". An empty list cannot satisfy that. The L10 matrix row (`PP_DESCRIPTOR_OWNERSHIP.md:93`) cites Milan 5.3.3.3. Assignment decision 2 names the one-entry boundary as the legal lower boundary. The sibling L6 check refuses an empty list (`L6_EMPTY`), so the two lists are handled asymmetrically.
- Evidence: `receipts/edge_probe.log`, "rate count 0, length 144 ...: ACCEPTED".
- Impact: an image whose AUDIO_UNIT advertises no rates passes the parent check. The processor walk then answers BAD_ARGUMENTS to every SET_SAMPLING_RATE (`gen_ucode.py:1385`, "count == k: list spent" at k=0), and a controller reads a descriptor that does not conform to Milan 5.3.3.3. Today the loader refuses an empty `audio_unit_rates_hz` (gate 36a), so the five shipping configurations cannot reach this. But this check exists to catch image faults that pass the loader.
- Required outcome: count 0 is refused with its own named reason, and a committed fixture plus a removed-check mutant prove it. Alternatively, a recorded public decision places zero outside L10, and the L10 row says so.
- Verification: `scripts/edge_probe.py`, the zero-count line must read REFUSED; the committed gate 36b must fail when that refusal is removed.

### F3: SUGGESTION: Robustness, Conformance: optional hardening of the image reader

These are not required by the frozen acceptance and do not affect coverage (`receipts/edge_probe.log`):
- `clock_sources_offset` 78 with padding is accepted, although IEEE Table 7-61 fixes it at 76 for this AEM version.
- Trailing bytes after the CLOCK_DOMAIN list are accepted.
- An image whose index has no AUDIO_UNIT or CLOCK_DOMAIN row passes vacuously.
- `current_sampling_rate` membership in the list (Milan 5.3.3.3) is not checked at the image.

Consider pinning offset 76, requiring at least one checked row of each type per configuration, and recording where current-rate membership is enforced.

## Clean-lens evidence

[R384] PASS RTL - `protocol-processor/hdl/aecp/ucode/gen_ucode.py:1317-1420` at gitlink `16be6768f710e79450aace277abacd6c2c3336e5`, `protocol-processor/hdl/aecp/desc/gen_desc_image.py:53-80,382-390`, and `sw/builder/aem_image_checks.py:20-36,82-112`. The diff contains no HDL and no gitlink change (`receipts/scope.txt`). I checked the consumer contract the checker relies on against the microprogram. The walk reads `RGN_DATA + 144 + 4k` for k<8, requires `sampling_rates_offset == SSR_LIST_OFF`, and compares whole 32-bit words. SET_CLOCK_SOURCE accepts `index < clock_sources_count` on the stated identity-permutation premise. The checker enforces exactly those premises: offset equals `SSR_LIST_OFF`, count at most `SSR_WALK_MAX`, full 4-byte words, and an identity list. Its widths (u16 offset/count, u32 words, u16 source indices) match IEEE Tables 7-5 and 7-61. Both consumer constants are live (the drift mutants are killed). The AEMI v1 index decode matches the packer's rendering, including repeated runs and stride versus length (mutants "only index 0", "only configuration 0" and "padded stride used as length" are killed).

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MINOR) | issue #577 and assignment decisions 1-6; IEEE 1722.1-2021 7.2.3/Table 7-5, 7.2.32/Table 7-61, 7.4.21, 7.4.23; Milan v1.2 5.3.3.3, 5.3.3.6; `aem_image_checks.py`; `endstation_builder.py:2282-2331`; `milan_soc.py:3331-3366,3946-3960,4010-4012`; `receipts/soc_path_probe.log`, `receipts/edge_probe.log` | R384-1 | a53682ed38720de758006602a19f78c8e40d69da |
| RTL | CLEAN | `gen_ucode.py:1317-1420` (SET_SAMPLING_RATE walk, SET_CLOCK_SOURCE range check) and `gen_desc_image.py:53-80,293-400` at gitlink 16be6768; `aem_image_checks.py`; `receipts/scope.txt`; consumer-drift mutants in `receipts/mutants.log` | R384-1 | a53682ed38720de758006602a19f78c8e40d69da |
| Robustness | UNCLEAN (F1 MAJOR, F2 MINOR) | truncated, empty, extent, header, stride, run, multi-configuration and zero-count probes; `receipts/edge_probe.log`, `receipts/mutants.log`, `receipts/soc_path_probe.log` | R384-1 | a53682ed38720de758006602a19f78c8e40d69da |
| Tests | UNCLEAN (F1 MAJOR, F2 MINOR) | `test_builder.py:27232-27372` (gate 36b) and runner registration at `:27782`; focused 36a/36b run rc 0 (`receipts/gate36b_head.log`); 19/19 mutants killed (`receipts/mutants.log`); published `mutants.json`/`check_mutants.py`; no test binds the SoC emitter (F1) or zero count (F2) | R384-1 | a53682ed38720de758006602a19f78c8e40d69da |
| Docs | UNCLEAN (F1 MAJOR) | `PP_DESCRIPTOR_OWNERSHIP.md:3-7,89,93,99,176-216,307,318`; `ENDSTATION_BUILDER.md:137-140,212-213,578-582,973`; PR #612 body (reproduction command, `receipts/cli_reach_probe.log`); case table checked against executed outcomes; F6/L6/L10 wording checked against code paths | R384-1 | a53682ed38720de758006602a19f78c8e40d69da |

## Prior public review findings on PR #612

I read these only after the verdict, findings and ledger above were written. At report time PR #612 has no review objects, no inline review comments, and two issue-thread comments. Both are manager review-start notices (5866173588 for this round, 5866181490 for the external round), and neither carries a finding. Issue #577 has the assignment, TAKEN and REVIEW READY comments, and none of them carries a review finding. There are no prior public findings to resolve or retain at this head. This round is the first to publish findings on this PR.

## Real limits

- I ran only the focused gates 36a/36b (four functions) and disposable probes. I did not run the full builder, docs, parent/processor/gPTP, Verilator or Yosys banks, per instructions. Where I cite docs-gate status, it comes from exact-head hosted contexts (see below).
- The SoC emitter was executed from its own function source, extracted with `ast`, because LiteX is not installed here. Its only stub is the overlay-path helper, which points at the overlay the builder emits. No bitstream, deploy or firmware flow was run. Physical calibration NOT RUN; no hardware claim is made.
- Scoped Verilator was not used: the diff contains no HDL.
- The mutants are my own condition-removal forms. I read the published raise-removal campaign but did not re-execute it.

## Pending manager duties

- Hosted exact-head contexts, observed read-only at report time. Executed and successful: `rtl-fast`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, Verilator shards 0 and 3, `full-ci-gate`, `elaborate`, `changes`, `bdd-conformance`, `wire-accountability`, `docs-check`, `docs-check-no-git`. Still in progress: Verilator shards 1, 2 and 4. `Physical gPTP (nightly and manual)` was skipped, which is not an executed pass. Hosted and act acceptance remain with the manager.
- Candidate-merge validation on current `dev` and post-merge containment remain with the manager.
- Resolution of F1 needs either a code change on the SoC emitter or a public decision (see F1's required outcome).

## Probe hygiene

All probes ran on symlink-farm copies under `$REVIEWS/577-r384-1-packet/scratch/`, or as in-process imports of the review clone that wrote nothing to it. Disclosure: the first run of the CLI probe wrote `configs/generated/endstation_arty_current/gen/adp_shape_defaults.svh` and `hdl/common/csr/gen/lwsrp_csr_defaults.svh` through farm symlinks into the review clone. The bytes were identical to the HEAD blobs; only mtimes changed. The published script now copies those paths first, and its re-run left clone mtimes unchanged. Interpreter bytecode caches created during the session were removed. `receipts/restore.txt` records the checks against the exact head: tracked blob bytes, modes and index versus `HEAD`, a clean worktree, and submodule gitlinks and cleanliness.

R384-1 FINISHED
