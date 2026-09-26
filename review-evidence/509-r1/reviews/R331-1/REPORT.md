[R331] POSITIVE - exact head 20423082f221a02f3de72952cec4e1ac0c839b1d

# R331-1: external independent review of issue #509 / PR #568

- Head `20423082f221a02f3de72952cec4e1ac0c839b1d`, tree `48c142d96a9a0333f921073e848ed2bbabf5e43c`.
- Base `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`; processor pin `990f96526bb89356c963a260ebbdcf2a77e6623a`; gPTP pin `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`.
- Diff under review: `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (new), `scripts/audit_pp_descriptors.py` (new), `docs/ENDSTATION_BUILDER.md`, `docs/README.md`.
- Role: external reviewer, cleared context. Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the #509 body, decision comment 5844867005, the executor's TAKEN and REVIEW READY comments, REQUIREMENTS.md section 8, processor `docs/architecture/07_memory_maps.md` section 3.1 at the pin, processor issues 38/39/60/82/89, parent #478/#464/#495, then the diff, then public evidence tree `ce614404.../review-evidence/509-r1`.
- All five lenses were applied independently. No BLOCKER, MAJOR or MINOR finding. Five SUGGESTIONs follow.

## Prior public review findings

No review round had published findings on PR #568 or issue #509 before this report. PR #568 has two review-start notices and no review bodies or inline comments. Nothing needs to be resolved or retained.

## Findings

### R331-1-S1 SUGGESTION - Robustness, Tests - `scripts/audit_pp_descriptors.py:43-45,57-58,126,178`
- **Evidence:** The audit's integrity checks are all `assert` statements. That covers the header magic and checksum, the directory-versus-wire type/index check, the builder-equality cross-check and the byte-survival proof for accepted probes. The page says "Packer acceptance also verifies the mutated bytes survive packing" (`PP_DESCRIPTOR_OWNERSHIP.md:147`). I planted a mutant packer that silently normalizes a zero or all-ones model ID:
  - The documented command exits 1 on the assertion (`receipts/mutation_M3.log`).
  - `python3 -O` exits 0 and reports both L9 probes as `accepted` (`receipts/mutation_M3_optimized.log`, `receipts/reproduce.log`).
- **Impact:** None under the documented invocation. Under `-O` or `PYTHONOPTIMIZE`, an "accepted" row loses the proof the page attributes to it.
- **Optional outcome:** Raise explicit exceptions, or refuse to run when `sys.flags.optimize` is set.
- **Verification:** The M3 mutant fails under both invocations.

### R331-1-S2 SUGGESTION - Conformance, Docs - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:63`
- **Evidence:** Processor L6 (`07_memory_maps.md:88` at the pin) has sub-rules the L6 row does not name:
  - at least one CLOCK_SOURCE per CLOCK_DOMAIN;
  - one INPUT_STREAM per CRF-capable input, or the single AAF input;
  - gPTP as media clock only in non-redundant single-interface models.

  The parent handles each one today:
  - the loader admits only `internal`/`crf` (`endstation_builder.py:3780-3805`), so the gPTP arm is unreachable;
  - the builder constructs exactly one CRF INPUT_STREAM source (decoded for all five images);
  - an empty source list crashes the loader (S3).
- **Impact:** None on ownership. The row's owners (PP60, F4, F6) cover these sub-rules, so no rule is unowned.
- **Optional outcome:** Add one sentence recording these dispositions.
- **Verification:** Reread the row.

### R331-1-S3 SUGGESTION - Robustness - `sw/builder/endstation_builder.py:3805` (pre-existing, outside the diff)
- **Evidence:** `dflt = clk.get("default_source", srcs[0])` is evaluated eagerly. So `clocking.media_clock_sources: []` raises `IndexError`, not `ConfigError`, even when `default_source` is given. I reproduced this with a disposable loader probe in a scratch clone at this head.
- **Impact:** The failure is closed: no image is produced. But the L6 at-least-one-source rule is enforced by a crash, not by a named refusal.
- **Outcome:** New work for the maintainer's follow-up list, for example next to F4. Not for this lane, per AGENTS.md section 4.
- **Verification:** An empty list is refused with a `ConfigError` naming the rule, and `[internal]` is still accepted.

### R331-1-S4 SUGGESTION - Conformance, Docs - public `review-evidence/509-r1/author/HANDOFF.md:141-160`
- **Evidence:** The proposed processor wording makes the parent authoritative for the decision's four configuration-dependent classes: identity/evolution, AUDIO_UNIT offset/count/length, clock-source construction/shape and ADP maxima. That matches decision 5844867005. The parent page goes further (`PP_DESCRIPTOR_OWNERSHIP.md:36-38`): parent shipping checks are authoritative for all generated model content. The proposed processor text says nothing about authority for the remaining PP60 semantic rules (L3/L4/L5/L7/L8 and the L1 partition).
- **Impact:** None today. If PP60 later adds packer semantics, the two contracts would state authority for those rules differently.
- **Optional outcome:** In the separate processor change, state the same authority split for the PP60 rules.
- **Verification:** Compare the processor PR text with the parent page.

### R331-1-S5 SUGGESTION - Docs - `docs/ENDSTATION_BUILDER.md:262`, `:992` (pre-existing, outside the diff)
- **Evidence:** Two lines contradict the census this PR corrected, in which input ports own zero maps and arty_current has one map (`receipts/descriptor-audit.json`):
  - D1 says every STREAM_PORT owns "one AUDIO_MAP";
  - row 20 lists an "identity AUDIO_MAP" for listener clusters.
- **Outcome:** A #495 residue candidate. Not this lane.
- **Verification:** The text matches the decoded map counts.

## Per-lens results (clean lenses, with evidence)

```text
[R331] PASS Conformance - docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:56-68,82-137,185-221 vs 07_memory_maps.md:81-92 @990f9652, decision 5844867005, receipts/descriptor-audit.json - every L1-L10/ADP row names clause, producer/consumer, enforcing path, boundary and open owner; C/R/T is distinguished; 11 rows spot-checked against source; all five configurations decoded independently and 0 mismatches against the page (receipts/page_vs_receipt.log); allocation matches the decision
[R331] PASS RTL - hdl/common/csr/milan_csr.sv:316,1308,1582,2816 and hdl/milan/milan_datapath.sv:2462,7520 (no RTL in diff) - L8 row claim verified: ADP_IDX0 resets to 0, [31:16] drives identify_index_i, and firmware never writes 0x630; no HDL, CDC or interface change at this head
[R331] PASS Robustness - scripts/audit_pp_descriptors.py (probes, fail-closed paths), receipts/mutation_M1/M2/M3*.log, receipts/reproduce.log - YAML probes verified non-vacuous (each mutation reaches packed bytes); relocated control reproduces tracked image; clean-clone rerun byte-identical; missing gPTP submodule refuses by name; normalizing packer fails closed (S1 records the -O limit)
[R331] PASS Tests - receipts/focused_builder_gates.log, gen_aem_store_selftest.log, check_entity_shape_selftest.log, reproduce.log - cited gates 6/8/28/29/33/36a/37 pass individually with no skips; generator self-test 20 checks, 6 recorded deviations; entity-shape 136/0; simulated processor L10/L6 refusal flips exactly the claimed probes while the 8-entry boundary stays accepted; raised loader bound flips the ninth-rate loader row
[R331] PASS Docs - docs/ENDSTATION_BUILDER.md diff, docs/README.md:63, receipts/gates-summary.txt - census corrections (8/8, 25, 1 map, 18,288 B) and D4 identity limits verified against YAML, decoded bytes and endstation_builder.py:4300-4320; docs_check (git and no-git), em-dash (+selftest), doc style, TOC, anchors, doc paths, py idiom, pp_srcs, ci_events, module matrix and diff --check all exit 0
```

## Required verification items

1. **Matrix rows and source checks: verified.** I checked 11 rows against source at the pins:
   - **L1:** `A._entity_descriptors`/`_port_descriptors`; gate 6 covers three shapes. The base_cluster=0 probe packs.
   - **L2:** `P._grouped_descriptors:219-221` refuses duplicates and `P._index_entries:333-335` refuses gaps. Wire type/index disagreement is accepted.
   - **L3:** `B._streams:1369-1370` refuses an empty direction.
   - **L4:** `A._entity_descriptors` flags `0x0003`/`0x0002`; `d_stream` sets current = first format. The CRF-word, buffer, 48-entry and mixed-family YAML probes all reach the image.
   - **L5:** `d_avb_interface` emits index 0. Gate 37 parses `OUR_PORTNUM_C`.
   - **L6:** `d_clock_domain:452-470` builds the identity list. `_load_clocking:3795,3858-3871` refuses `input_stream` and CRF without its sink (gate 33).
   - **L7:** `_streams:1429-1433` refuses static listener maps. `_map_duplicate_rule` is exercised by the map probes. `d_audio_cluster` builds channel_count=1.
   - **L8:** the CSR path (see RTL above).
   - **L9:** `_eui64:1327-1334` checks width only, and the pin overrides at `:4306-4312` with no comparison.
   - **L10:** `_load_clocking` refuses more than 8 entries and duplicates. `test_audio_unit_shipping_rates` checks offset, count and words, not length. `aem_specs.spec_from_overlay:219-221` limits rates to 48/96/192 kHz.
   - **ADP:** `adp_shape` is the single source. Gate 28 covers four configurations, matching the #495 checklist line on gate 28 coverage.

   Construction (C), refusal (R) and test comparison (T) are labelled correctly in every row I checked.
2. **Audit rerun: verified.**
   - The receipt is byte-identical to the published one: sha256 `8233f515e8e469570314fdfea9437db5d082a6441f04a75ff840efe5444f4779`.
   - A clean clone with only the processor and gPTP submodules initialised gives the same bytes.
   - Descriptor, byte, offset, count, length, source-list and metadata values match the page for all five configurations, by an independent checker with hand-transcribed expectations and a planted negative control (`scripts/check_page_vs_receipt.py`).
   - Probe outcomes match the page: 30 packer, 13 YAML and 2 map probes. Refusals: density, duplicate, name binding, 577-byte extent, empty listener, static input map, ninth rate, duplicate rate, and eight rates at conversion. Every other probe is accepted, including every "accepted invalid" model the page reports.
   - The page's CLI commands give image hashes equal to the audit's for all five configurations (15 invocations, all exit 0).
3. **Identity residue: reproduced independently** through the real builder and image CLIs. I edited `reset_time` 0->3 in a copy. Only arty_4x4 image byte 6741 changes (`CONTROL+93`, the low byte of reset_time). The overlay and model ID `0x001BC557FC6ABBC8` are unchanged, and the hashes equal the page's `1b288e13...15ff` and `bb036e26...0562`.
4. **Follow-ups F1-F6: real, bounded and not duplicates.**
   - F1 is parent refusal of invalid IDs. PP38 is the processor side; #495 keeps evolution.
   - F2, F3 and F4 are parent L4 and L6 loader gaps, each backed by an accepted YAML probe that reaches the image.
   - F5 is the F07.2 `1..*` edge against the zero-cluster 8x8 input ports; I decoded all eight at (0,0).
   - F6 is the parent image-boundary L6/L10 check. PP89 stays processor-side, and #478's loader scope is kept.
   - #478 and #464 are closed and unextended. PP82 runtime work and #76 are excluded. Nothing is silently fixed: no validator, config, RTL or pin changed.
5. **Proposed processor wording: consistent with the decision.** Generic structure stays with the processor, the four configuration-dependent classes go to the parent, and processor checks are defence in depth. S4 is an optional alignment.
6. **Idiom, privacy and docs gates: pass.**
   - `check_py_idiom.py` passes. Every function has a signature and docstring, paths use `Path`, and there is no shell string or bare except.
   - The privacy scrub is clean.
   - The docs gates pass. Three runs first exited 2 only because the pinned renderer was absent; they were rerun in a private venv built from `tools/markdown/requirements.txt`, and both results are in `receipts/gates-summary.txt`.

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ownership page matrix/tables/probes/identity/follow-ups vs 07 section 3.1, decision 5844867005, PP38/39/60/82/89, #478/#464/#495, decoded receipt | R331-1 | `20423082f221a02f3de72952cec4e1ac0c839b1d` |
| RTL | CLEAN | No HDL in diff; L8 CSR claim traced in `milan_csr.sv`, `milan_datapath.sv`, bare-metal firmware | R331-1 | `20423082f221a02f3de72952cec4e1ac0c839b1d` |
| Robustness | CLEAN | Audit script failure paths, non-vacuous YAML probes, clean-clone rerun, missing-submodule refusal, mutation M3 (S1, S3 are SUGGESTION) | R331-1 | `20423082f221a02f3de72952cec4e1ac0c839b1d` |
| Tests | CLEAN | Cited builder gates run individually, generator and entity-shape self-tests, mutations M1/M2/M3, page-vs-receipt checker with negative control | R331-1 | `20423082f221a02f3de72952cec4e1ac0c839b1d` |
| Docs | CLEAN | Ownership page, ENDSTATION_BUILDER diff, README row, handoff wording, docs/idiom/privacy gates (S2, S4, S5 are SUGGESTION) | R331-1 | `20423082f221a02f3de72952cec4e1ac0c839b1d` |

## Limits

- **Not run by this reviewer** (the assignment excluded them): the full builder bank (`test_builder.py`, SDK or compiler-absent), the full parent/processor/gPTP/Yosys banks, behave, xvlog, RTL lint, NVM and bare-metal checks, and act. For these I rely on the manager's public evidence and did not re-execute them.
- **Hosted checks:** when I read them, several exact-head hosted contexts were still `in_progress`: docs-check, elaborate, Verilator shards 0-4 and yosys-elaboration. Physical gPTP was `skipped`, which is not execution. Completed successes: bdd-conformance, changes, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability and Yosys shards 0-3.
- **Hardware:** physical calibration was not run, and no hardware claim is made.
- **Multi-configuration:** the page makes no multi-configuration claim, and no multi-configuration behaviour was tested.
- **Review clone:** after the probes it is exact. HEAD and tree match; the index equals the HEAD tree; every blob rehashes to 0 mismatches; there are no non-`H` index flags; the processor, gPTP and axis gitlinks match their checkouts; and `external` is uninitialised as expected (`receipts/clone_integrity.txt`). The only residue, my `__pycache__` directories, was removed.

## Pending manager duties

- Hosted/act acceptance at the exact head, including the in-progress contexts listed above.
- Final current-dev candidate construction and validation at the merge turn.
- Filing F1-F6, and optionally S3/S5, as the page and handoff direct.
- The separate processor contract change (optionally applying S4).
- Merge authorization, containment and board state.

R331-1 FINISHED
