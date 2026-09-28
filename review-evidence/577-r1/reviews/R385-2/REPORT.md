[R385] POSITIVE - exact head be6b48c140db1692caedbdf997495b43ff1a56a2

Round R385-2, external independent re-review of PR #612 for issue #577 (F6 of `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`).

- Head: be6b48c140db1692caedbdf997495b43ff1a56a2, tree cc7578edeefdba3f871e6924de2477dc513420e5.
- Delta under review: a53682ed..be6b48c1, one commit.
- Source base: 54ce877371ee6e8878cf67294e86c2a8481b62f6. The whole-lane diff from the base was also read.

Contract read:
- AGENTS.md and CONTRIBUTING.md sections 3 and 6.
- docs/README.md.
- The issue #577 body, the round-1 assignment (comment 5865331676, decisions 1-6), and the F1 decision (5866340517, option (a)).
- The round-2 assignment (5866376116), the takeover (5866393673) and the handoff (5866843098).
- The PR #612 body at this head.
- The pinned processor consumer `protocol-processor/hdl/aecp/ucode/gen_ucode.py` at gitlink 16be6768.

My round-1 packet was used as read-only input. This round's scripts are copies of its scripts, extended for round 2.

## Verdict summary

Round 1 found F1 (MAJOR) and F2 (MINOR). Both are resolved at this head. All three taken suggestions are implemented. The frozen constraints still hold.

- **F1.** The deployed-image emitter `sw/litex/milan_soc.py:build_desc_image` now runs `validate_shipping_image` on the exact bytes that `main()` CRC-binds and writes.
  - The call is at `:3368-3372`. `main()` calls the emitter at `:3954`, binds the CRC at `:3965` and writes `aem_desc.bin` at `:4018`.
  - The round-1 plant (reversed sources `[1, 0]`) is now refused by the SoC path with `L6_ORDER`.
  - A committed test executes the repository's own emitter function. It fails when the hook is removed, when the refusal is swallowed, and when the checked bytes are replaced.
  - The PR body's reproduction command reaches the check from both emitters.
  - The ownership document names both enforcing emitters.
- **F2.** A zero-entry rate list is refused as `L10_EMPTY`. The refusal has a committed fixture and a killed removed-check mutant.
- **Frozen constraints.** All five shipping images are byte-identical to the base. The SoC and builder emitters produce identical bytes. No processor source or gitlink changed.

No BLOCKER, MAJOR or MINOR finding is open. Four SUGGESTIONS are recorded below; they are optional and do not affect coverage.

## Round-1 findings re-verified at this head

### F1 (MAJOR, round 1) - RESOLVED

Each requirement of the F1 decision (option (a)), with its evidence at this head:

**Validator runs on the exact bytes every deployed-image emitter writes, including `build_desc_image`.**
- `sw/litex/milan_soc.py:3358` imports the checker, and `:3368-3372` validates `blob`, the value returned at `:3373`. The import resolves because `REPO_ROOT` is put on `sys.path` at `:72`. Nothing earlier on `sys.path` shadows `sw`: I checked `sw/litex`, `platforms`, `scripts`, `avdecc` and the processor `desc` directory.
- `receipts/probe_shipping_path_head.log`: at head, the SoC function makes 1 checker call and returns sources `[0, 1]`. Its bytes are identical to `_entity_model_image`'s.
- `receipts/images_head.txt`: for all five configurations, the SoC `aem_desc.bin` and `aem_desc.map` equal the builder's.
- Other writers of `aem_desc.bin` were searched. The builder CLI `build()` writes no image; it makes 0 checker calls, which is consistent with `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:189`.
- `avdecc/gen_aemi_image.py` `main()` is a developer CLI and is not on the `build.sh`, `milan_soc.py` or `deploy.sh` path. `scripts/nvm_shape.py:82` uses it only for a temporary image whose header it reads. On the bare-metal profile, boot refuses any bytes other than the CRC-bound ones (`sw/firmware/milan_baremetal/milan_baremetal.c:1423`), and the SoC checks those bytes first.

**It refuses before the image is written or CRC-bound.**
- The hook raises `RuntimeError`, and `main()` has no handler around the call (`:3952-3955`).
- The CRC constant (`:3965`) and the file write (`:4018`) both use the returned `_desc_blob`, and both run after the call.
- `receipts/probe_shipping_path_planted.log`: with `receipts/planted_fault.diff` applied, the SoC path gives `RAISED RuntimeError: aem_desc.bin: L6_ORDER: configuration 0, type 0x0024, image byte 3920: source list [1, 0] is not in index order`. That is the refusal. The builder path refuses with the same reason.

**A committed test fails if the SoC emitter bypasses the check.**
- `sw/builder/test_builder.py:27385-27423` (`_soc_image_emitter`, `test_soc_shipping_image_contract`) copies the function body verbatim from the tree. Only the module globals are supplied, and only the overlay lookup is substituted. The test runs all 23 planted cases through that function and binds its bytes to the builder's for the five configurations.
- `receipts/mutants.tsv`, all KILLED:
  - `rm_soc_hook`;
  - `soc_hook_swallows` (the refusal is printed and the build continues);
  - `soc_repack_after_check` (bytes other than the checked ones are returned).
- The same-bytes control `noop_control_soc` SURVIVED, as intended.

**The PR body's reproduction command reaches the check.**
- `receipts/cli_reach_probe.log`: the command runs verbatim at the head root and returns rc 0.
- Instrumented, it makes 35 checker calls from `_entity_model_image` and 28 from `build_desc_image`.
- With the checker forced to refuse every call, the command returns rc 1.

**The ownership document names the enforcing emitters.**
- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` names both emitters at:
  - the L6 row `:89`;
  - the L10 row `:93`;
  - the new source key G `:99`;
  - the narrative `:182-189`;
  - the F6 row `:341`.
- The decision is linked at `:399`.
- `docs/ENDSTATION_BUILDER.md:137-141,213-214,580-587` now describe the SoC as the deployed-image emitter.

### F2 (MINOR, round 1) - RESOLVED

- `sw/builder/aem_image_checks.py:48-49`: count 0 gives `L10_EMPTY` and cites Milan 5.3.3.3.
- The committed fixture "empty rates" is at `test_builder.py:27266`.
- `rm_L10_EMPTY` is KILLED. Without the check an empty list is refused as `L10_CURRENT`, and the test requires the `L10_EMPTY` name.
- `receipts/checker_sweep.log` now gives `{0: 'L10_EMPTY', 1..8: 'ACCEPT', 9: 'L10_COUNT'}`.
- `receipts/edge_probe.log`: count 0 gives `L10_EMPTY` with or without a trailing word. A wrong offset is still reported first (`L10_OFFSET`).

### S1 (SUGGESTION, round 1) - three of four parts taken; one remains optional

1. **`clock_sources_offset` pinned at 76 (taken).**
   - `aem_image_checks.py:74-75` refuses any other offset with `L6_OFFSET`.
   - `receipts/edge_probe.log`: offsets 0..199 accept only 76.
   - Fixtures for offset 70 and a padded list at offset 78 are at `test_builder.py:27281-27283`.
   - `rm_L6_OFFSET` and the relaxed `>=` mutant are KILLED.
2. **At least one checked AUDIO_UNIT and CLOCK_DOMAIN per configuration (taken).**
   - The code is at `:103-106`, `:112-113` and `:126-131`, and descriptors are counted only once checked, so a zero-count row does not count.
   - On all five real images: `n_config` 0 gives `IMAGE_CONFIGS`; `n_config` + 1, a zero-count row and a retyped row each give `L10_MISSING` or `L6_MISSING` (`receipts/edge_probe.log`).
   - `rm_L10_MISSING`, `rm_L6_MISSING`, `rm_IMAGE_CONFIGS`, `presence_counts_rows` and `presence_config0_only` are all KILLED by `test_shipping_image_contract_presence` (`test_builder.py:27426-27467`).
3. **`current_sampling_rate` membership checked at the image (taken).**
   - `:61-64` compare the complete 32-bit words. Offset 136 agrees with the consumer's `AU_RATE_OFF = 136` (`gen_ucode.py:279,290`).
   - `receipts/edge_probe.log`: every position 0..7 is accepted, and every absent case from 1 to 8 entries gives `L10_CURRENT`. A pull-bit mismatch in either direction also gives `L10_CURRENT`.
   - `rm_L10_CURRENT`, `current_masks_pull` and `current_first_only` are KILLED.
4. **Trailing bytes after the CLOCK_DOMAIN list are still accepted.** This part was not adopted. The handoff publicly records it as outside this round. It remains optional and is carried as S3 below.

### Constraints

- **Byte identity.** `receipts/images_compare.txt` compares 25 lines: five configurations, three builder artifacts and two SoC artifacts each. The base (the 54ce8773 versions of the changed files, with the checker removed) and the head are identical. The builder artifacts also equal both the round-1 base and head hashes in my round-1 packet.
- **No processor or gitlink change.** `git diff 54ce8773..be6b48c1 --name-only` lists two docs, the checker, `endstation_builder.py` (+6 lines, import and hook only, unchanged in this delta), `test_builder.py` and `milan_soc.py`. `receipts/clone_integrity.txt` shows all four gitlinks equal at base and head. The loader functions `_load_clocking` and `_validate_output_clock_sources` are untouched, so #478's scope is preserved.

## Findings at this head

No BLOCKER, MAJOR or MINOR finding.

### S1 - SUGGESTION - Tests, Robustness - `sw/builder/aem_image_checks.py:112-113` - the new configuration-range refusal has no fixture

- **Evidence.**
  - `receipts/mutants.tsv`: `rm_cfg_range` SURVIVED.
  - `receipts/rm_cfg_range_edge.log`: without the check, an AUDIO_UNIT row whose configuration equals the header count escapes as `IndexError` instead of a named refusal, and an ENTITY row with the same fault is accepted.
  - `receipts/mutants_structure.tsv`: the pre-existing generic refusals are also unpinned. These are the magic/version check (`:101-102`) and the descriptor-beyond-image check (`:119-120`); their removed mutants SURVIVE.
- **Scope.** These are generic structure checks that the processor packer also owns, and none is in the frozen refusal classes. The ownership document's claim is "each removed semantic refusal", and that claim holds. The PR body's "each named refusal deletion" is broader than the evidence.
- **Impact.** Low. Both emitters still fail closed on the AUDIO_UNIT and CLOCK_DOMAIN rows the check exists for.
- **Optional outcome.** Add a fixture with a row configuration at or above the header count, or narrow the PR-body sentence to semantic refusals.

### S2 - SUGGESTION - Tests - `sw/litex/milan_soc.py:3952-4018` - `main()`'s use of the checked bytes is verified by reading, not by a test

- The committed test binds `build_desc_image`, which is the emitter the decision names.
- That `main()` CRC-binds and writes only that function's return value is true at this head, but only by inspection.
- A small static assertion would make a future re-packing emitter inside `main()` fail a test, for example: the only producer of `_desc_blob` is the `build_desc_image` call, and it precedes the CRC constant and the write.

### S3 - SUGGESTION - Conformance, Robustness - `sw/builder/aem_image_checks.py:67-88` - optional CLOCK_DOMAIN self-sufficiency

- Trailing bytes after the source list are still accepted (`receipts/edge_probe.log`, `receipts/checker_sweep.log`).
- `clock_source_index` (IEEE 7.2.32 byte 70) is not checked against `clock_sources_count`. That would be the L6 analogue of the new `L10_CURRENT`.
- Neither check is in the decisions or the taken suggestions. Consider a separate issue.

### S4 - SUGGESTION - Docs - `sw/builder/endstation_builder.py:3136-3137` - stale pre-existing docstring

- The docstring of `emit_aem_rom_svh` still says the processor serves "the flat DRAM image emitted by `_entity_model_image()`".
- The deployed emitter is now documented as `build_desc_image`. The bytes are identical and gated, so nothing is wrong on the wire.
- The text predates this lane, which did not touch it. Any update belongs in a later docs change.

## Lens results

```text
[R385] PASS Conformance - sw/litex/milan_soc.py:3331-3373,3952-3966,4016-4018; sw/builder/aem_image_checks.py:39-133; issue #577 decisions 1-6, F1 decision 5866340517 and round-2 assignment 5866376116; receipts/probe_shipping_path_{head,planted}.log, receipts/cli_reach_probe.log, receipts/edge_probe.log, receipts/images_compare.txt - every F1 (a) requirement, F2, the three taken suggestions and the byte-identity/no-gitlink constraints hold at this head; L10/L6 field positions agree with the pinned consumer (gen_ucode.py:279-292,1329-1330,1425-1437)
[R385] PASS RTL - git diff 54ce8773..be6b48c1 --name-only (no hdl/, tb/, syn/ or submodule path); receipts/clone_integrity.txt gitlinks; protocol-processor/hdl/aecp/ucode/gen_ucode.py:279-292,1329-1330,1425-1437 at 16be6768 - no HDL, CDC, FSM or processor interface change; the checker's model of the consumer (current rate lane @136, source offset/count lane @72/74, identity-range SET_CLOCK_SOURCE check, 144/8 rate walk) matches the microprogram
[R385] PASS Robustness - sw/builder/aem_image_checks.py whole file; receipts/checker_sweep.log (boundary sweep, 3000-case index fuzz: 0 non-ImageCheckError, truncations all IMAGE_STRUCTURE), receipts/edge_probe.log (presence and header corruptions on five real images, offsets 0..199, pull-bit and position cases), receipts/probe_shipping_path_planted.log - malformed, boundary, empty and header-inconsistent images are refused by name; the SoC refusal aborts before Vivado, CRC binding and write (S1/S3 optional)
[R385] PASS Tests - sw/builder/test_builder.py:27233-27467,27878; receipts/gate36b_head.log (5 functions PASS); receipts/mutants.tsv (37 rows: 34 KILLED incl. every required and new refusal class, both real emitter hooks, swallow and repack; 2 no-op controls SURVIVED; rm_cfg_range SURVIVED, S1) - each new named refusal has a fixture that fails when it is removed, and both emitters are exercised on their own source (S1/S2 optional)
[R385] PASS Docs - docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:6,89,93,99,178-237,341,399; docs/ENDSTATION_BUILDER.md:134-141,213-214,576-587; receipts/docs_check.log, receipts/check_doc_style.log, receipts/check_doc_paths.log (all rc 0); no U+2014 in added lines; the case table matches receipts/gate36b_head.log and receipts/edge_probe.log verdict for verdict (S4 optional, pre-existing)
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #577 decisions 1-6, F1 decision, round-2 assignment; `sw/litex/milan_soc.py:3331-3373,3952-3966,4016-4018`; `sw/builder/aem_image_checks.py:39-133`; `gen_ucode.py:279-292,1329-1437` at 16be6768; `receipts/probe_shipping_path_*.log`, `receipts/cli_reach_probe.log`, `receipts/edge_probe.log`, `receipts/images_compare.txt` | R385-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |
| RTL | CLEAN | diff name list base..head (no HDL); gitlinks in `receipts/clone_integrity.txt`; `gen_ucode.py:279-292,1329-1330,1425-1437` at 16be6768 | R385-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |
| Robustness | CLEAN | `aem_image_checks.py` whole file; `receipts/checker_sweep.log`, `receipts/edge_probe.log`, `receipts/rm_cfg_range_edge.log`, `receipts/probe_shipping_path_planted.log`; `milan_soc.py:3952-3955` (no handler) | R385-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |
| Tests | CLEAN | `sw/builder/test_builder.py:27233-27467,27878`; `receipts/gate36b_head.log`; `receipts/mutants.tsv` (37 rows), `receipts/mutants_structure.tsv`; `receipts/cli_reach_probe.log` | R385-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |
| Docs | CLEAN | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:6,89,93,99,178-237,341,399`; `docs/ENDSTATION_BUILDER.md:134-141,213-214,576-587`; PR #612 body; `receipts/docs_check.log`, `receipts/check_doc_style.log`, `receipts/check_doc_paths.log` | R385-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |

Every lens is covered at the exact merge-candidate source head, and no lens is covered at an earlier head. Round R385-1 left Conformance, Robustness, Tests and Docs UNCLEAN at a53682ed. This round re-applied all five lenses at be6b48c1, the head that contains the fixes.

## Prior public findings on PR #612

These were read only after the independent pass, verdict and ledger above were written. The prior public review rounds are:
- [R384] R384-1 (PR comment 5866336473, NEGATIVE, head a53682ed);
- [R385] R385-1 (PR comment 5866373356, NEGATIVE, head a53682ed).

No other reviewer's round-2 report was read.

| Prior finding | Disposition at be6b48c1 | Basis |
|---|---|---|
| [R384] F1 MAJOR: the check does not run on the emitter that writes the deployed image; the PR body's reproduction command does not reach the check | RESOLVED | `receipts/probe_shipping_path_planted.log` (SoC path refuses with `L6_ORDER`); `receipts/mutants.tsv` (`rm_soc_hook`, `soc_hook_swallows`, `soc_repack_after_check` KILLED); `receipts/cli_reach_probe.log` (the new command reaches both emitters, and a forced refusal gives rc 1); ownership rows `:89,93,99,182-189,341`; `ENDSTATION_BUILDER.md` drift corrected at `:137-141,213-214,580-587` |
| [R384] F2 MINOR: a zero-entry rate list passes | RESOLVED | `L10_EMPTY` at `aem_image_checks.py:48-49`; fixture `test_builder.py:27266`; `rm_L10_EMPTY` KILLED |
| [R384] F3 SUGGESTION: reader hardening | Offset 76, per-configuration presence and current-rate membership are taken, see above. Trailing CLOCK_DOMAIN bytes remain optional (this round's S3) | `receipts/edge_probe.log` |
| [R385] F1 MAJOR (round 1) | RESOLVED | section "F1 (MAJOR, round 1)" above |
| [R385] F2 MINOR (round 1) | RESOLVED | section "F2 (MINOR, round 1)" above |
| [R385] S1 SUGGESTION (round 1) | Three parts taken; one part optional (S3) | section "S1 (SUGGESTION, round 1)" above |

The prior findings add no open item. R384-1's F1 has one point beyond my round-1 F1: the old PR-body reproduction command did not reach the checker. The new command does (`receipts/cli_reach_probe.log`).

## Reproduction

Each command runs from this packet directory against `<tree>`, a disposable copy of the exact head with submodules checked out. Never point them at a live clone: `build()` writes generated files.

- `python3 scripts/probe_shipping_path.py <tree>` produces `receipts/probe_shipping_path_head.log`. Apply `receipts/planted_fault.diff` to a copy of the tree and run the same command to produce `receipts/probe_shipping_path_planted.log`.
- `python3 scripts/run_gate36b.py <tree>` produces `receipts/gate36b_head.log`. It runs gate 36a plus the four gate 36b functions.
- `python3 scripts/mutants.py --list | xargs -P 8 -I{} python3 scripts/mutants.py <tree> <workdir> {}` produces `receipts/mutants.tsv`. `rm_IMAGE_magic_version` and `rm_IMAGE_desc_beyond`, run singly, produce `receipts/mutants_structure.tsv`.
- `python3 scripts/checker_sweep.py <tree>` produces `receipts/checker_sweep.log`.
- `python3 scripts/edge_probe.py <tree>` produces `receipts/edge_probe.log`. Run it on a copy with the `cfg >= config_count` refusal removed to produce `receipts/rm_cfg_range_edge.log`, which records the `arty_current` line.
- `python3 scripts/cli_reach_probe.py <tree> <workdir>` produces `receipts/cli_reach_probe.log`.
- `python3 scripts/image_hashes.py <tree>` produces `receipts/images_head.txt`. For `receipts/images_base.txt`, run it on a copy where the five changed files are at their 54ce8773 versions and `sw/builder/aem_image_checks.py` is absent. `receipts/images_compare.txt` is the comparison.
- Docs gates were run in the clone at head with `PYTHONDONTWRITEBYTECODE=1`:
  - `python3 scripts/docs_check.py`;
  - `python3 scripts/check_doc_style.py`;
  - `python3 scripts/check_doc_paths.py`.

  They produce `receipts/docs_check.log`, `receipts/check_doc_style.log` and `receipts/check_doc_paths.log`, all rc 0.
- `receipts/clone_integrity.txt` records the restoration check:
  - index and worktree match the HEAD tree (mode/blob/path digest equal);
  - there are no untracked or ignored files;
  - all four gitlinks match at HEAD and in the index;
  - all three checked-out submodules sit at their pins with clean status.

## Real limits

- **Standard text.** No licensed IEEE 1722.1 or Milan text is in the clone.
  - Field positions (current rate at 136, rate list fields at 140/142, source fields at 72/74 with the list at 76) were checked by descriptor field arithmetic and against the pinned microprogram's lane comments. They were not checked against the standard text.
  - The citation "Table 7-61" (`PP_DESCRIPTOR_OWNERSHIP.md:199`) and the Milan 5.3.3.3 wording were not verified against the standard.
- **SoC emitter scope.** The SoC emitter was executed by verbatim AST extraction, both in my probes and in the committed test, because litex is not installed. `main()` was checked by reading `milan_soc.py:3952-4018`, not by executing it. No full SoC elaboration, Vivado build or deploy ran.
- **Gates not run.**
  - `python3 scripts/gen_toc.py --check` returned rc 2 here because the pinned Markdown renderer is not installed, and shared installs are not allowed (`receipts/gen_toc_check.log`). That gate is not evidenced by this round.
  - The full builder, processor, gPTP and Yosys banks were not run, as assigned.
- **Manager evidence.** The manager's round-2 static/builder/native bank receipts at this head were not yet published when observed. The public evidence tree `d13de9c5:review-evidence/577-r1` holds round-1 author evidence only. I have not independently observed the statement that the banks passed at this head.
- **Hosted checks** were observed at 2026-09-28T09:18:07Z (`receipts/hosted_checks.tsv`). This is an observation, not acceptance.
  - Succeeded: `rtl-fast`, `full-ci-gate`, all four Yosys shards, `yosys-elaboration`, `verilator-lint` and Verilator shard 3/5.
  - Still in progress: Verilator shards 0, 1, 2 and 4, `docs-check` and `elaborate`.
  - "Physical gPTP" was skipped, and a skip is not an executed job.
- **Verilator.** The scoped Verilator path in the assignment does not exist on this host. No RTL changed, so no simulation was needed.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Publish and accept the round-2 builder/native bank receipts at be6b48c1, including the TOC gate this round could not run.
- Complete hosted and act acceptance at the exact head. Several Verilator shards, `docs-check` and `elaborate` were still in progress when observed.
- Build and validate the final current-dev candidate at the merge turn. The source base is 54ce8773; live dev is 1fa2357f.
- Reconcile this ledger with the internal reviewer's round-2 ledger.
- Optionally, route S1-S4 to a new issue or note them for a later change.

R385-2 FINISHED
