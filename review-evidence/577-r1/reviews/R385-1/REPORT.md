[R385] NEGATIVE - exact head a53682ed38720de758006602a19f78c8e40d69da

Round R385-1, external independent review of PR #612 for issue #577 (F6 of `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`).
Head a53682ed38720de758006602a19f78c8e40d69da, tree e434badd5de9c04bebc451f8abbde187c06b8cae, source base 54ce877371ee6e8878cf67294e86c2a8481b62f6.
Contract read: AGENTS.md, CONTRIBUTING.md (sections 2, 3, 6), docs/README.md, issue #577 body, assignment comment 5865331676 with its six manager decisions, takeover 5865349318, handoff 5865874116, processor rule table `protocol-processor/docs/architecture/07_memory_maps.md` L6/L10, and the SET_SAMPLING_RATE / SET_CLOCK_SOURCE microprogram in `protocol-processor/hdl/aecp/ucode/gen_ucode.py` at the pinned gitlink 16be6768.

## Verdict summary

The checker itself is correct and well tested: every required acceptance and refusal behaves as the frozen decisions state, each of the eight required refusal classes has a removed-check mutant that the committed gate 36b kills, and all five shipping images are byte-identical to the base.
One MAJOR finding stops the verdict. The check is wired into `endstation_builder._entity_model_image`. That function is not on the path that produces the shipped `aem_desc.bin`. The builder's own `build()` never calls it. The gateware generator that writes the image beside the bitstream packs its own copy and never calls the checker. A fault planted in the image generator passes the loader, is refused by `_entity_model_image`, and is shipped by the gateware producer. The ownership document states the opposite.
A MINOR finding (F2, retained from the prior round and confirmed by this round's sweep) remains: count 0 passes the L10 check.

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests, Docs - the parent check does not guard the image that ships

Artifacts:
- `sw/builder/endstation_builder.py:2310` (the hook).
- `sw/builder/endstation_builder.py:5797` (`build()`). This is the pipeline `sw/litex/build.sh:315` runs, and it contains no call to `_entity_model_image`.
- `sw/litex/milan_soc.py:3331-3366` (`build_desc_image`), which calls `gen_desc_image.build` directly.
- `sw/litex/milan_soc.py:4012`, which writes the shipped `aem_desc.bin`. `sw/litex/build.sh:499` runs `milan_soc.py`, and `sw/litex/deploy.sh:153,384` flashes that file.
- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:318`, the F6 row: "Enforced by `I.validate_shipping_image` after `B._entity_model_image` packs the shipping image".
- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:181-182`, `:6`, and the L6/L10 rows at `:89` and `:93`.
- `sw/builder/aem_image_checks.py:83`: "Check every packed AUDIO_UNIT and CLOCK_DOMAIN before shipping the image".

Authority:
- Manager decision 1 on issue #577 (comment 5865331676): the check runs "on the packed descriptor image the builder emits for a shipping configuration ... so a fault planted in the image is caught even when the loader-side checks pass".
- The issue title and the F6 row place the check "at the shipping image boundary".
- AGENTS.md section 6, Tests lens: "Real integration wiring is tested where practical".

Evidence, executed at head in a scratch copy (`scripts/probe_shipping_path.py`):
- `receipts/probe_shipping_path_head.log`:
  - `endstation_builder.build()` completes with 0 checker calls.
  - `milan_soc.build_desc_image` contains no reference to the checker and makes 0 checker calls. Its body was extracted verbatim by AST, because the host has no litex.
  - At head its bytes equal `_entity_model_image`'s.
- `receipts/probe_shipping_path_planted.log` plants a reversed clock-source list in `avdecc/aem_descriptors.py:472` (`receipts/planted_fault.diff`):
  - The loader accepts it and `build()` completes.
  - The gateware producer returns an image carrying sources `[1, 0]` with no refusal.
  - Only `_entity_model_image` refuses it (`L6_ORDER`).
- Repository search:
  - `validate_shipping_image` and `aem_image_checks` are referenced only in `sw/builder/endstation_builder.py` and `sw/builder/test_builder.py`.
  - Outside tests, only `scripts/audit_pp_descriptors.py:136` calls `_entity_model_image`.
  - No test compares `milan_soc.build_desc_image` output with `_entity_model_image` output. The two producers are separate copies of the same join and are only assumed equivalent.

Impact:
- For the five tracked configurations, gate 36b's per-configuration loop in the builder test bank catches a generator regression. That is test-time detection through a proxy function, not a refusal at the shipping boundary.
- The gateware build and deploy flow ships a faulty image in three cases: a configuration the bank does not run, a build run without the bank, or the two producers diverging.
- The document tells the next reader that the shipped image is enforced, and that is not true.

Required outcome: one of the following.
- (a) The producer of the shipped image refuses a planted L6/L10 fault with the named reason. Either it runs the same validator or it delegates to the checked emitter. An executed test plants a fault on that path and shows the refusal, and the equivalence of the two producers is gated or removed.
- (b) The manager publicly decides that the builder-internal function plus the test bank is the accepted boundary. These then state exactly where the check runs and that the gateware producer is not guarded:
  - the F6, L6 and L10 rows;
  - the narrative at `:181-197`;
  - the checker docstring.

  A follow-up issue records the unguarded path.

Verification: re-run `scripts/probe_shipping_path.py` on the corrected head, with and without the planted fault. Under (a) the gateware path must refuse. Under (b), re-read the corrected rows against the probe result.

Lens attribution:
- Conformance: decision 1 and the F6 row are not met for the shipped artifact.
- Robustness: a planted fault reaches the shipped artifact.
- Tests: no test exercises the real producer or binds it to the checked function.
- Docs: the F6/L6/L10 rows and the narrative overstate the enforcement.

This is not a hardware or RTL-interface defect. No HDL, CDC, FSM or processor contract is affected, so the RTL lens is not attributed.

### F2 - MINOR - Conformance, Robustness, Tests - a zero-entry sampling-rate list passes the image check (retains prior finding [R384] F2)

Artifacts: `sw/builder/aem_image_checks.py:46-57` and `sw/builder/test_builder.py:27257-27275`. The fixture list has no zero-count case.

Authority:
- Decision 2 names the one-entry and eight-entry boundaries as the legal ones.
- The L10 row (`PP_DESCRIPTOR_OWNERSHIP.md:93`) cites Milan 5.3.3.3, which requires `current_sampling_rate` to be one of the listed rates. An empty list cannot satisfy that.
- The sibling L6 check refuses an empty list (`L6_EMPTY`).

Evidence: `receipts/checker_sweep.log`, "L10 matched count/extent: {0: 'ACCEPT', ...}". In my independent pass I recorded this under a suggestion. The prior public finding cites the Milan clause text, which the clone does not carry, and I retain it at MINOR on that clause and decision 2's lower boundary.

Impact: count 0 is below the legal one-entry boundary. The loader rejects an empty rate list today, but this check exists to catch image faults that the loader does not see. For such an image the processor walk refuses every SET_SAMPLING_RATE (`gen_ucode.py:1385-1386`, count == 0 at k = 0).

Required outcome: one of the following.
- Count 0 is refused with its own named reason, backed by a committed fixture and a removed-check mutant.
- A recorded public decision places zero outside L10, and the L10 row says so.

Verification: re-run `scripts/checker_sweep.py`; count 0 must be refused. The committed gate 36b must fail with that refusal removed.

### S1 - SUGGESTION - Conformance, Robustness - structural gaps outside the frozen acceptance

Evidence: `receipts/checker_sweep.log` accepts both of the following:
- a CLOCK_DOMAIN whose identity list sits at offset 78 instead of 76;
- a CLOCK_DOMAIN with trailing bytes after the list.

An image with no AUDIO_UNIT or CLOCK_DOMAIN row also passes vacuously, because `sw/builder/aem_image_checks.py:99` skips other types. `current_sampling_rate` membership in the list is not checked. None of these is in decision 3 (identity list), so none is a finding. Consider a separate issue if the parent wants the image check to be self-sufficient.

## Acceptance judgement, points (1)-(6)

1. Derivation: met for the function it guards, and not met for the shipped artifact (F1).
   - Index offset, row count, lengths, strides and list fields are read from bytes (`aem_image_checks.py:92-110`). The row layout matches the packer's documented v1 index map (`protocol-processor/hdl/aecp/desc/gen_desc_image.py:52-76`, `:384-390`).
   - `SSR_LIST_OFF`/`SSR_WALK_MAX` are parsed from `gen_ucode.py:1329-1330` without execution. The identity sequence comes from the served count.
   - No builder constant is imported. The test fixtures pin 144/76 independently: the `consumer_offset_146` and `consumer_walk_9` mutants are killed, so the test does not merely mirror the consumer either.
   - IEEE field positions were checked by field arithmetic. AUDIO_UNIT (7.2.3): `current_sampling_rate` at 136, offset at 140, count at 142, list at 144. CLOCK_DOMAIN (7.2.32): `clock_source_index` at 70, offset at 72, count at 74, list at 76. Both agree with `avdecc/aem_descriptors.py:464-482` and the microprogram lane comments.
2. L10: met for every named case. Count 0 is also accepted, which is below the legal one-entry boundary (F2). `receipts/checker_sweep.log`:
   - Counts 0-8 are accepted with matched extent. The 1- and 8-entry cases go through the emitter in `receipts/gate36b_head.log`, and the 8-entry fixture includes pull-bearing word 0x2000BB80.
   - All 299 other offsets in 0..299 give `L10_OFFSET`, and 9 gives `L10_COUNT`.
   - Count above extent gives `L10_COUNT_EXTENT`, extent above count gives `L10_EXTRA_WORDS`, and every tail of ±1..3 bytes gives `L10_PARTIAL_WORD`.
3. L6: met. Over every tuple of length 1..4 drawn from 0..k, only the four identity lists are accepted. The rest split into `L6_DUPLICATE` 548, `L6_GAP` 119 and `L6_ORDER` 29. Gate 36b pins `[1,0]`, `[0,2]` and `[0,0]` to `L6_ORDER`, `L6_GAP` and `L6_DUPLICATE` through the emitter. The rule matches the processor's range check `gen_ucode.py:1435-1437` and rule L6 in `07_memory_maps.md`.
4. Mutants and images: met. `receipts/mutants.tsv` has 22 rows:
   - All 8 required removed-check mutants are killed by the committed gate 36b.
   - Also killed: 4 defensive-refusal removals, hook removal, 5 walk mutants (index 0 only, length used as stride, stride used as length, configuration 0 only, first run per type) and 2 consumer-drift mutants.
   - The no-op control survives, as intended.
   - The partial-word and duplicate removals are killed as wrong-reason refusals, which shows the reasons are distinct.
   - `receipts/images_compare.txt`: the `aem_desc.bin/json/map` for all five configurations are byte-identical between the base (checker removed, base builder files) and the head.
5. Scope: met.
   - `git diff 54ce8773..a53682ed` touches four files. `endstation_builder.py` gains 6 lines only (import and hook), so `_load_clocking` (`:3844`) and `_validate_output_clock_sources` (`:4232`) are unchanged.
   - `git ls-tree` shows identical gitlinks at base and head: protocol-processor 16be6768, gptp-processor 5dce647a, external efeb541a, third_party/verilog-axis 48ff7a7e. No processor source changes.
6. Docs: not met (F1). The case table at `PP_DESCRIPTOR_OWNERSHIP.md:199-213` matches the executed verdicts exactly. The rows claim enforcement of the shipped image, which the probe refutes.

## Lens results

```text
[R385] PASS RTL - protocol-processor/hdl/aecp/ucode/gen_ucode.py:1329-1437 at gitlink 16be6768; git ls-tree of all four gitlinks at base and head - no HDL, CDC or processor file is in the diff; the checker's model of the SET_SAMPLING_RATE walk (fixed offset 144, fail-closed on another offset, at most 8 entries, full 32-bit words with pull bits) and of the SET_CLOCK_SOURCE index < count range check matches the microprogram; the identity-list rule is exactly the condition under which that range check is the IEEE 7.4.23.1 membership test; the 16-bit count widths agree
```

- Conformance: UNCLEAN (F1, F2). Points 1-5 were checked against decisions 1-5 with the evidence above.
- Robustness: UNCLEAN (F1, F2). Otherwise clean. `receipts/checker_sweep.log` covers:
  - 3000 random header and index corruptions, which gave only `ImageCheckError` or acceptance, with 0 other exception types;
  - 7 truncations, which all gave `IMAGE_STRUCTURE`;
  - header-length boundaries.
- Tests: UNCLEAN (F1: the real producer is not exercised; F2: no zero-count fixture). Otherwise clean: 22 mutant rows including a surviving control, fixtures independent of the constructors, every required boundary and refusal present, and gate 36a still green.
- Docs: UNCLEAN (F1). At head, `scripts/docs_check.py`, `scripts/check_doc_style.py` and `scripts/check_doc_paths.py` all return rc 0 (logs in `receipts/`). There is no U+2014 in added lines. The clause citations are consistent (see limits).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | issue #577 decisions 1-6; `sw/builder/aem_image_checks.py:39-112`; `sw/builder/endstation_builder.py:2282-2331,5797-5852`; `sw/litex/milan_soc.py:3331-3366,4011-4012`; `gen_ucode.py:1305-1437`; `07_memory_maps.md` L6/L10; `receipts/probe_shipping_path_*.log`, `receipts/checker_sweep.log` | R385-1 | a53682ed38720de758006602a19f78c8e40d69da |
| RTL | CLEAN | `gen_ucode.py:1329-1437` at 16be6768; gitlinks at base and head; diff file list (no HDL) | R385-1 | a53682ed38720de758006602a19f78c8e40d69da |
| Robustness | UNCLEAN (F1, F2) | `aem_image_checks.py` whole file; `receipts/checker_sweep.log` (boundary sweep, 3000-case index fuzz, truncations); `receipts/probe_shipping_path_planted.log` | R385-1 | a53682ed38720de758006602a19f78c8e40d69da |
| Tests | UNCLEAN (F1, F2) | `sw/builder/test_builder.py:27231-27373,27781`; `receipts/gate36b_head.log`; `receipts/mutants.tsv` (22 rows); `receipts/images_*.txt` | R385-1 | a53682ed38720de758006602a19f78c8e40d69da |
| Docs | UNCLEAN (F1) | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:6,89,93,99,178-216,307,318`; `receipts/docs_check.log`, `receipts/check_doc_style.log`, `receipts/check_doc_paths.log` | R385-1 | a53682ed38720de758006602a19f78c8e40d69da |

## Prior public findings on PR #612

These were read only after the independent pass, verdict and ledger above were written. The only prior review round is [R384] R384-1 (PR comment 5866336473, NEGATIVE, same head).

| Prior finding | Disposition at a53682ed | Basis |
|---|---|---|
| [R384] F1 MAJOR: the check does not run on the emitter of the deployed image | RETAINED, as this round's F1 (found independently) | `receipts/probe_shipping_path_head.log`, `receipts/probe_shipping_path_planted.log` |
| [R384] F2 MINOR: a zero-entry rate list passes | RETAINED, as this round's F2 | `receipts/checker_sweep.log` count 0 ACCEPT |
| [R384] F3 SUGGESTION: optional reader hardening | Same content as this round's S1; optional | `receipts/checker_sweep.log` |

The ledger labels F2 alongside F1. F2 changes no lens result, because its lenses (Conformance, Robustness, Tests) were already UNCLEAN under F1.

## Reproduction

Each command runs from this packet directory against `<tree>`, a disposable copy of the exact head with submodules checked out. Never point them at a live clone: `build()` writes generated files.

- `python3 scripts/run_gate36b.py <tree> test_audio_unit_shipping_rates test_shipping_image_contract test_shipping_image_contract_index_walk` produces `receipts/gate36b_head.log`.
- `python3 scripts/mutants.py --list | xargs -P 8 -I{} python3 scripts/mutants.py <tree> <workdir> {}` produces `receipts/mutants.tsv`.
- `python3 scripts/probe_shipping_path.py <tree>` produces `receipts/probe_shipping_path_head.log`. Apply `receipts/planted_fault.diff` to a copy of the tree to produce `receipts/probe_shipping_path_planted.log`.
- `python3 scripts/image_hashes.py <tree>` produces the head hashes. For the base hashes, run it on a copy with the three base versions of the changed builder and doc files and without `aem_image_checks.py`. The results are in `receipts/images_*.txt`.
- `python3 scripts/checker_sweep.py <tree>` produces `receipts/checker_sweep.log`.
- `receipts/clone_integrity.txt` records the review clone's restoration check after the probes: index and worktree match the HEAD tree, all four gitlinks match, and there are no untracked or ignored files.

## Real limits

- No licensed IEEE 1722.1 or Milan text is in the clone.
  - Field positions were verified by arithmetic from the IEEE descriptor layouts. They were cross-checked against three independent encodings in the tree: the constructors, the microprogram lane comments, and the gate 36a readback.
  - Clause numbers (IEEE 7.2.3, 7.2.32, 7.4.21.1, 7.4.23.1; Milan 5.3.3.3, 5.3.3.6) were checked for consistency with the processor compliance documents, not against the standard text.
- The gateware producer was exercised by verbatim AST extraction, because litex is not installed. A full `milan_soc.py` elaboration was not run.
- The scoped Verilator path in the assignment does not exist on this host. No RTL changed, so no simulation was needed.
- Probes ran in scratch copies. The full builder, processor, gPTP and Yosys banks were not run, as assigned. The author's published full builder log (`review-evidence/577-r1/author/builder-01.log`) shows the same gate 36b lines and reports only the gate 11 calibration arm NOT RUN.
- Hosted exact-head checks were observed, not accepted (`receipts/hosted_checks.tsv`):
  - most contexts had succeeded;
  - Verilator shards 1/5 and 4/5 were still in progress;
  - "Physical gPTP" was skipped.
- Physical calibration was NOT RUN, and a skip is not hardware proof.

## Pending manager duties

- Decide F1 between outcome (a) and outcome (b), and F2 between refusal and a recorded exclusion, and record both decisions on issue #577.
- Run hosted/act acceptance and the final current-dev candidate at the merge turn.
- Reconcile this ledger with the internal reviewer's.

R385-1 FINISHED
