[R435] NEGATIVE - exact head 9610098a47ce070235df17c2846b48d29cc2ce53

# R435-2: external review of PR #144 (lane C8, descriptor model lint), round 2

- Repository Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #144 (issues #38, #39, #60, #89). Review start: PR #144 comment 5955472885.
- Exact head `9610098a47ce070235df17c2846b48d29cc2ce53`, tree `949cb1b0144445fcdb061562af371f5588f9a5fe`. This is the round-1 head `e6cca1ff` plus nine item commits, the `--no-ff` merge `69c7692` of `main` `2ebd4fe8` (PR #139, C6) and one parent-gate fix (`9610098`).
- I verified the detached review clone at the head before and after the review: HEAD, `write-tree` equal to the tree, `git status --porcelain --ignored` empty, `diff-index` empty, and index modes and blobs identical to the HEAD tree. The repository records no gitlinks, so no submodule pin applies (`logs/clone_integrity.txt`). Every probe ran in a disposable copy under `scratch/`.
- Scope was rebuilt in this order:
  - README.md and docs/README.md (the repository has no AGENTS.md or CONTRIBUTING.md);
  - the issue #60 body and acceptance, the 46-cap report (5854263065), the assignment (5948562638), the STOP and ruling (5948825547, 5948872196), the round-2 assignment and rulings (5952457756) and the review-ready note (5954510064);
  - IEEE 1722.1-2021 and Milan v1.2, read from the text (§6.2.2.8, §7.2 and its subclauses, §7.3.5.2, Tables 7-121 to 7-126; Milan §5.3.2, §5.3.3.1 to .11, §5.6.2, Annex C);
  - `git diff 2ebd4fe8..9610098` and the history;
  - the public author packet `review-evidence/ppC8-r1/author-r2` at milan-fpga `36f0c671`.
- I read the prior public findings (R434-1 and R435-1) only after my own pass over the diff. Each one is dispositioned below.

## Verdict

**NEGATIVE, on two MINOR findings.** All ten round-1 MINOR findings are closed at this head (six from R435-1, four from R434-1). So are both round-1 residue items and the suggestions the assignment took.

What holds at this head:
- **Digest:** it zeroes exactly the §6.2.2.8 exclusions. I checked it field by field against the clause text and the Table 7-121 to 7-126 layouts.
- **L12:** neither of its checks refuses a conforming descriptor.
- **L8 `identify-format`:** it matches §7.3.5.2 and Milan §5.3.3.10, and refuses no conforming IDENTIFY.
- **Waivers:** strict types and the overlap refusal behave as documented.
- **Loading:** the lint loads by path.
- **Suppression driver:** the committed driver reproduces 56 of 56.
- **Merge:** clean.
- **Parent models:** all five behave as required at dev `cdf49d1a` and at PR #634's head `d81198c2`.

The two findings:
- **F1 (new this round):** L4 `stream-layout` refuses the Milan v1.2 Annex C stream layout, which Milan §5.3.3.4 permits for any stream. The processor does not need that restriction, and the check cites as its authority the clause that permits Annex C. Under the round-2 ruling (conform by default; a stricter check only where the processor needs it, cited as a processor restriction) this is a defect. In round 1 I accepted it as a recorded design restriction; the round-2 ruling sets the stricter bar, and I apply it.
- **F2:** the round-2 claim that "every arm has one" mutation does not hold for the new `identify-format` check. 7 of its 8 refusal arms can each be deleted with the gate still green. Two digest arms are unpinned in the same way.

## Findings

### F1: MINOR. L4 `stream-layout` refuses Milan's Annex C stream layout, which Milan v1.2 §5.3.3.4 permits, and cites that clause as its authority

- **Lenses:** Conformance, Tests, Docs.
- **Where:**
  - `hdl/aecp/desc/model_rules.py:163-164`: `CHECKS["stream-layout"]`, clause "Milan v1.2 §5.3.3.4; IEEE 1722.1-2021 §7.2.6 Table 7-8", requirement "formats at 138, no redundancy tail".
  - `hdl/aecp/desc/model_rules.py:623-638`: `_stream_layout` refuses `formats_offset` ≠ 138, `redundant_offset` ≠ 138+8N and a length ≠ 138+8N.
  - `docs/architecture/07_memory_maps.md:184`: the L4 row cites "Milan §5.3.3.4; IEEE 1722.1-2021 §7.2, Table 7-8".
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:448`: REQ-MDL-003's Arch cell credits "packer model lint L4 stream-layout".
- **Authority:**
  - Milan v1.2 §5.3.3.4: "A PAAD-AE may use the extension of the STREAM_INPUT/OUTPUT descriptors as defined in Section C for any of its Streams and shall use it for the Streams that are part of the redundant pair."
  - Milan Annex C (normative), Table C.1: `formats_offset` "is 136", `redundant_offset` "is 136+8*N"; the format "can be used by any ATDECC entity for any STREAM_INPUT/OUTPUT descriptor".
  - Round-2 ruling, #60 comment 5952457756: "The default is to conform to the standard; strictness beyond the standard is kept only where the processor needs it, and then it is cited as a processor restriction (07 §3.1), never as the standard."
- **The processor does not need the restriction.** Its own text and code say so:
  - 07 §3.2 Δ note (`07_memory_maps.md:243`): the processor "reads only `current_format` (@74, the same offset in both layouts)".
  - `hdl/aecp/KL_aecp_desc_store.sv:106-109`: "576 covers a model assembled either way".
  - `hdl/aecp/ucode/gen_ucode.py:1241-1249`: READ_DESCRIPTOR's stream path copies `formats_offset` through verbatim.
  - The lint itself reads every format list through `formats_offset` (`model_rules.py:338-349`).
- **Evidence:** `logs/r2_probes.log`, probes A1 and A2 (`scripts/r2_probes.py`).
  - milan_min's output stream re-laid in Table C.1 form, with R = 0, `formats_offset` 136, `redundant_offset` 136+8N and length 136+8N, is refused: `L4 stream-layout: cfg 0 STREAM_OUTPUT 0: formats_offset 136, not 138 (Milan v1.2 §5.3.3.4; IEEE 1722.1-2021 §7.2.6 Table 7-8)`, plus the matching `redundant_offset` and length lines.
  - With all three streams in that layout, every stream is refused the same way.
  - No other check objects: L3/L4's format, CRF and current-format checks all pass on the Annex C bytes.
- **Impact:**
  - The lint runs by default for every consumer of the packer. A Milan model that uses the Annex C layout, which Milan permits, is refused under a citation of the clause that permits it.
  - The consumer must either carry a waiver whose reason tracks no real defect or switch the lint off.
  - No parent model is affected: all five emit Table 7-8.
- **Required outcome:**
  - The default, per the ruling: accept the Annex C layout with R = 0 (`formats_offset` 136, `redundant_offset` 136+8N, length 136+8N), as well as Table 7-8.
  - Keep refusing a redundancy tail (R > 0). Cite that refusal as the non-redundant-PAAD processor restriction (07 §3.1), not as §5.3.3.4.
  - Add an Annex C positive case to the gate, and keep the existing negatives (moved list, short or long body, redundant tail).
  - Update the 07 §3.1 L4 row and REQ-MDL-003's Arch cell to match.
  - Alternative: the owner may rule that Table 7-8 only is a processor restriction. In that case the check, the L4 row and REQ-MDL-003 must cite it as that restriction (07 §3.1 / §3.2), with its reason, and not as Milan §5.3.3.4.
- **Verification:**
  - `scripts/r2_probes.py` A1 and A2 pack (or, under the alternative, are refused with a 07 §3.1 restriction citation).
  - The gate, the suppression driver and `make check` stay rc 0.
  - milan_min's recorded digest is unchanged.

### F2: MINOR. The new `identify-format` check has 7 of 8 refusal arms unpinned, and two digest arms are unpinned, contrary to the round-2 "every arm has one" claim

- **Lenses:** Tests, Docs.
- **Where:**
  - `hdl/aecp/desc/model_rules.py:104-106` (`IDENTIFY_FORMAT`) and `:755-768` (`_identify_format`). The arms are: the 113-octet length, `control_value_type` (flag bits masked), `values_offset`, `number_of_values`, `minimum`, `maximum`, `step` and `unit`.
  - `tb/desc_store/lint_mutations.py:445`: the only `identify-format` mutation, "IDENTIFY maximum 1".
  - `hdl/aecp/desc/model_lint.py:94-97` (`VALUED`, the MIXER family set) and `:169-180` (`_current_spans`, the array span).
  - `tb/desc_store/test_gen_desc_image.py:608-638` (`test_exclusions_are_the_clause`).
  - The claims: the PR body's Round 2 → Findings item 5 ("A mutation's `detail` names the arm of a check with several; every arm has one (78 mutations over 56 checks)"), `docs/architecture/09_verification.md:308` (the row "on the arm its `detail` names where a check has several") and the `tb/desc_store/README.md` lint section ("Where a check has several arms, the mutation's `detail` names the arm").
- **Authority:**
  - Round-2 assignment item 5 (#60 comment 5952457756): "pin every refusal arm".
  - The issue acceptance asks for a negative case per refusal.
- **Evidence:** `logs/r2_plants.log` (`scripts/r2_plants.py`): 37 one-line plants on the round-2 code, each in its own copy, with the whole gate run on each. 27 are KILLED. These SURVIVE:
  - `id-no-length`, `id-type-any`, `id-offset-any`, `id-nvalues-any`, `id-min-any`, `id-step-any`, `id-unit-any`: each deletes one `identify-format` arm. Only `id-max-any` is KILLED.
  - `id-no-mask`: the value-type comparison without the flag mask. No positive case carries a flag bit.
  - `dig-array-off`: the array exclusion starts at `unit` instead of `current[0]`. The case set moves `default`, never the `unit`/`string` neighbours right before `current[0]`.
  - `dig-mixer-all`: MIXER is credited with the selector and array families, which §6.2.2.8 names only for CONTROL, MATRIX and SIGNAL_TRANSCODER. There is no MIXER case.
  - Every other round-2 arm I planted is KILLED: L12's maximum, fixed-extent and offset arms; the digest's selector, linear-stride, INT8, MATRIX_SIGNAL, AVB_INTERFACE, CLOCK_SOURCE and ENTITY arms; strict waiver types; overlap, including its configuration scope; per-port L5; both L2 arms; the CRF word; JACK ownership; cross-map uniqueness; the stream length arm; and a waiver on a missing configuration.
- **Impact:**
  - A later edit that drops any IDENTIFY format arm except `maximum` passes the gate that CI runs. The IDENTIFY format is part of this round's delta and the primary IDENTIFY check depends on it.
  - In the digest, an over-exclusion of an array control's `unit`/`string`, or of a MIXER's non-linear values, would accept a structural change under a recorded id without failing any test.
  - The docs and the PR body state that every arm is pinned.
- **Required outcome:**
  - One named mutation per `identify-format` arm, each whose `detail` names the arm: the length, value type, `values_offset`, `number_of_values`, `minimum`, `step` and `unit`.
  - A positive IDENTIFY whose `control_value_type` carries a flag bit, if the mask is intended (otherwise drop the mask and say so).
  - In `test_exclusions_are_the_clause`, the array `unit` and `string` as moving neighbours, and a MIXER case whose non-linear value change moves the digest.
- **Verification:** re-run `scripts/r2_plants.py`. All 37 must be KILLED. The suppression driver must stay 56 of 56.

### RESIDUE, wording only (carried to the residue checklist; not verdict-bearing)

- **R1:** the PR title still reads "rules L1 to L11"; the lint now has L12. Exact fix: replace "rules L1 to L11" with "rules L1 to L12" in the title.

### SUGGESTION (not verdict-bearing)

- **S1:** `gen_desc_image._load_model_lint` (`hdl/aecp/desc/gen_desc_image.py`, the new loader) does not check for a `None` spec. `model_lint.beside` does, and the two loaders could share that guard.

## Prior public findings at this head

| Finding | Severity | Status at 9610098 | Evidence |
|---|---|---|---|
| R435-1 F1: L2 orders single-level types | MINOR | **Closed.** L2 orders CONTROL only, in IEEE §7.2's walk (I checked it against the §7.2 text). Probe B packs. Two CONTROL-order negatives exist, and the plants `l2-no-range` and `l2-no-top` are KILLED. | `logs/r1_conformance.log` B, `logs/r2_plants.log` |
| R435-1 F2: L5 refuses a subset configuration | MINOR | **Closed.** L5 compares per `port_number`. Probe C packs; the move negative and `l5-any-move` are KILLED. | `logs/r1_conformance.log` C |
| R435-1 F3: the digest over-excludes | MINOR | **Closed.** The exclusions equal the §6.2.2.8 list (spans checked against Tables 7-121 to 7-126 and the descriptor layouts). Probe F: option change → changed, current change → unchanged. MATRIX_SIGNAL is hashed. Digest probes D1 to D15 behave per the clause. Two arms are unpinned (F2). | `logs/r1_conformance.log` F, `logs/r2_probes.log` D |
| R435-1 F4: unpinned arms; 8 of 32 plants survive | MINOR | **Closed.** My round-1 campaign, re-run unchanged: 30 KILLED and 2 INVALID (the two patterns the F1/F2 fixes rewrote). Each applicable round-1 survivor fails a named test: `cap45`/`rates7` → `LintTest.test_boundaries_pack`; `crf-ge1`/`aaf-ge1`/`entity-cfg` → named `test_mutations` cases; `waiver-anytype` → `WaiverTest.test_waiver_scope_is_its_type`; `waiver-anycfg` → `WaiverTest.test_waiver_scope_is_its_configuration`. `iface-subset` is now the rule (F2's resolution). | `logs/r1_lint_planted.log`, `logs/r1_survivors_named.log` |
| R435-1 F5: unlisted model shalls | MINOR | **Closed.** L12 `descriptor-extent` and `descriptor-maximum` and L8 `identify-format` are linted. The gPTP source chain and non-subset extents are on 07 §3.1's "not linted" list with reasons. Probes D and I are refused; `cluster-pad-rerec` is KILLED. | `logs/r1_conformance.log` D, I; `logs/r1_min_planted.log` |
| R435-1 F6: 47 left in three places | MINOR | **Closed.** F01.5 reads ≤46; 07 §3.3.1 and the store comment give 522 B / 520 B. A search finds no 47 stated as the 2021 cap in `docs/*.md` or `hdl/`. | grep in this report's limits |
| R435-1 R1, R2 (wording) | RESIDUE | **Closed.** `_family` cites §7.3.3; the PR body now reads "No production caller of `build()` changes; …". | source, PR body |
| R435-1 S1 to S4 | SUGGESTION | **Taken.** A malformed map raises `ImageError` (`logs/r1_model_ids.log`). Waivers have strict types and refuse overlaps (`logs/r1_conformance.log` G, `logs/r2_probes.log` E). The lint loads by path (`r2_probes` F1). The driver is committed (56/56, `logs/suppression.log`). | as listed |
| R434-1 F1: CRF check too loose | MINOR | **Closed.** `crf-format` refuses any CRF word but `0x041060010000BB80`. The round-1 behaviour, planted back (`crf-any-word`), is KILLED. | `logs/r2_plants.log` |
| R434-1 F2: JACK-owned CONTROL counted top-level | MINOR | **Closed.** Every §7.2 count/base owner is surveyed. A JACK-owned IDENTIFY packs (probe B8); `owners-no-jack` is KILLED. TOP_LEVEL equals §7.2.2's list. | `logs/r2_probes.log` B8, `logs/r2_plants.log` |
| R434-1 F3: 46 missing in F01.5 | MINOR | **Closed** (same as R435-1 F6). | |
| R434-1 F4: five unpinned arms | MINOR | **Closed.** `waiver-anytype` (type scope), `unique-per-map`, `l2-no-top` and `layout-no-length` are KILLED. The `ut`-current arm was removed as redundant: a `ut`-carrying `current_format` is covered only by an equal entry, and the gate pins that case. | `logs/r2_plants.log`, `logs/r1_lint_planted.log` |
| R434-1 S1, S2 | SUGGESTION | **Taken** (as R435-1 S1, S2). | |
| R434-1 S3: `ut` in `current_format` listed verbatim accepted | SUGGESTION | **Retained, not taken.** Not verdict-bearing. | |
| R434-1 S4: exclusivity per mutation | SUGGESTION | **Retained.** 68 of 78 mutations trip only their check; 10 also trip cascading checks, recorded here. | `logs/r1_exclusivity.log` |

## The focus items, at this head

1. **L12 (`descriptor-extent`, `descriptor-maximum`).**
   - The extents match the IEEE 1722.1-2021 layouts of §7.2.1, §7.2.2, §7.2.8, §7.2.9, §7.2.13, §7.2.16 and §7.2.19: ENTITY 312, CONFIGURATION 74 + 4N at offset 74, AVB_INTERFACE 102, CLOCK_SOURCE 86, STREAM_PORT 20, AUDIO_CLUSTER 90, AUDIO_MAP 8 + 8N at offset 8.
   - The fixed offsets are the ones the tables state ("This field is set to 74 / 8 for this version of AEM").
   - §7.2: "The maximum length of a descriptor shall be 508 octets." A 508-octet CONTROL packs and a 509-octet one is refused (C1, C2).
   - A CONFIGURATION listing a zero count packs (C3).
   - **No conforming model is refused.**
2. **L8 `identify-format`.**
   - It matches §7.3.5.2 (CONTROL_LINEAR_UINT8, minimum 0, maximum 255, step 255, unit multiplier 0 and code UNITLESS), §7.2.22 (`values_offset` 104) and "a boolean value", hence one value and 113 octets.
   - It ignores the fields Milan §5.3.3.10 waives (latency, `signal_*`), as well as default, current and string (B1, B2).
   - It masks the r/u flags (B3) and accepts a second, JACK-owned IDENTIFY (B8).
   - The refusing arms work (B4 to B7).
   - The "no IDENTIFY ⇒ refusal" rule follows from Milan §5.6.2 (AEM_IDENTIFY_CONTROL_INDEX_VALID shall be 1, the clause 07 §3.1 cites) read with IEEE §6.2.2.19 (the index then names the primary IDENTIFY control).
   - **No conforming IDENTIFY is refused.** Arm coverage: F2.
3. **Digest against §6.2.2.8:** exact, as stated in the prior-findings table above. `entity_id` and `entity_model_id` are zeroed beyond the clause, and that is disclosed.
4. **Strict waiver types and overlap:**
   - wrong JSON types for every key are refused;
   - a numeric type code is accepted;
   - a duplicate and an overlapping range are refused;
   - a waiver of another check is not an overlap, and is judged stale (E1 to E5).
5. **Lint loaded by path:** `sys.path` is unchanged, no `model_lint` or `model_rules` module is registered, and consumer modules of those names on `sys.path` are never used (F1 probe).
6. **Check-suppression driver:** `python3 -B lint_suppression.py --jobs 12` gives "56 of 56 checks killed", with the control passing (`logs/suppression.log`). The make target `lint-suppression` hard-codes `--jobs 8`, which is fine.
7. **Merge `69c7692`.**
   - It has one conflict resolution (remerge-diff): main's 09 §8.4 stays, and the lint's section is §8.5. A search finds every lint citation at §8.5 and none left at §8.4.
   - Every line main added in the five files both sides touched is present at the head. The other main files are byte-equal to `2ebd4fe8` (the diff `2ebd4fe8..HEAD` touches only the 19 lane files).
   - `git apply --check`: 205 of 205 campaign patches apply (`logs/campaign_apply_check.log`).
8. **Parent.**
   - `parent-adoption-c8-cdf49d1a.patch` is byte-identical to round 1 (sha256 `aa5a88eb…`). At dev `cdf49d1a`, `parent-adoption-c4c6-ea3fb388.patch` and then the C8 patch apply cleanly.
   - At PR #634's head `d81198c2`, the C8 patch's one `aem_assemble.py` hunk needs its identical one-line port (context moved), as disclosed.
   - At both heads, with this head as `protocol-processor` and `gptp-processor` at its gitlink, my round-1 parent script, run unchanged, gives:
     - `arty_current`, `arty_4x4`, `arty_8ch` and `ax7101_1x1_tdm8` pack with no waiver, and their driven ADP values agree;
     - `ax7101_8x8` packs only with its reported #584 waiver (`L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0..7: 8 finding(s) waived`);
     - without the waiver, `ax7101_8x8` is refused on exactly those 8 ports;
     - with the waiver widened by one port, it is refused as stale.

     (`logs/parent_dev_models_lint.txt`, `logs/parent_634_models_lint.txt`, `logs/parent_setup.txt`.)

## Executed checks at this head

| Check | Result | Receipt |
|---|---|---|
| packer gate `test_gen_desc_image.py` | rc 0, 50 tests OK | `logs/gate.log` |
| `tb/desc_store` suite (`make run`, pinned Verilator 5.050) | rc 0, gate then 584 PASS, 0 FAIL | `logs/desc_store_run.log` |
| check-suppression driver | rc 0, control passes, 56 of 56 killed | `logs/suppression.log` |
| `make check`, `gen_matrix.py --check`, `lint_hdl.sh` | rc 0 each | `logs/make_check.log`, `logs/gen_matrix.log`, `logs/lint_hdl.log` |
| campaign patches `git apply --check` | 205 of 205 | `logs/campaign_apply_check.log` |
| round-2 delta probes | 45 probes; 43 as the clauses require; A1/A2 refused (F1) | `logs/r2_probes.log` |
| round-2 plants | 37: 27 KILLED, 10 SURVIVED (F2) | `logs/r2_plants.log` |
| round-1 campaigns re-run unchanged | lint plants 30 KILLED / 2 INVALID (rewritten); milan_min plants 10 KILLED, the 2 disclosed fields survive; probes A to I as required; model-ids input all `ImageError` | `logs/r1_*.log` |
| parent five models, dev and PR #634 | as in focus item 8 | `logs/parent_*` |
| hosted runs at the head (read-only) | `docs-gates` and `portability` succeeded (two each); `suites` was in progress at my look | `logs/hosted_check_runs.txt` |

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `model_rules.py` all 56 checks against IEEE 1722.1-2021 §6.2.2.8, §7.2, §7.2.1 to §7.2.36 layouts, §7.3.5.2, Tables 7-121 to 7-126, and Milan v1.2 §5.3.2, §5.3.3.1 to .11, §5.6.2, Annex C; `model_lint.py` digest spans; probes A to F; parent models | R435-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |
| RTL | CLEAN | `KL_aecp_desc_store.sv` (comment-only change, 46-cap figures 522/520 B); `gen_ucode.py` stream READ_DESCRIPTOR path (unchanged); no port, parameter or register change; `lint_hdl.sh` rc 0; `tb/desc_store` 584/584; main's RTL equal to `2ebd4fe8` | R435-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |
| Robustness | CLEAN | refusal path (`ImageError` per finding, CLI exit 1, no file), malformed `adp`/`model_ids`, strict waiver types, overlap and stale refusals, by-path loading beside shadowing modules, short descriptors (probe H), the lint-off note | R435-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |
| Tests | UNCLEAN (F1, F2) | gate 50 tests; 78 mutations over 56 checks; suppression 56/56; round-1 campaigns re-run; 37 round-2 plants; named tests for every applicable round-1 survivor | R435-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |
| Docs | UNCLEAN (F1, F2) | 07 §3.1 (rules table, "not linted" list), §3.2 Δ note, §3.3.1; 00 REQ-MDL-001 to 011, REQ-ADP-003/004, GAP-08; 01 F01.5; 09 §8.4/§8.5; `tb/desc_store` README; integrator.md; PR body Round 2 | R435-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |

## Real limits

- I did not run the full `run_suites.sh`, the parent consumer set (16), the parent builder test or the donor bank. Those belong to the manager. I ran the focused suite (`tb/desc_store`), the gate, the suppression driver, `make check`, `gen_matrix.py --check` and `lint_hdl.sh`.
- The parent trees are scratch extractions of dev `cdf49d1a` and PR #634 `d81198c2`, limited to the paths the model-packing path reads, with `gptp-processor` at its gitlink. They are not full checkouts.
- Clause checks were made against the reviewer's copies of IEEE 1722.1-2021 and Milan v1.2. The spec text is not distributed in this packet.
- The 47-cap search covered `docs/*.md` and `hdl/` for "≤ 47", "capped at 47", "F ≤ 47", "N ≤ 47" and the old 530/528 B figures: none remain.
- Hosted `suites` was still in progress at my look. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- The donor bank (9) and the parent consumer set (16) at this head; hosted and act acceptance.
- The final current-dev candidate at the merge turn (source base `2ebd4fe8`, live dev `cdf49d1a`).
- Carry R1 to the residue checklist.
- Owner choice for F1: the default is to accept the Annex C layout; the alternative is a ruling that records Table 7-8 only as a processor restriction.

R435-2 FINISHED
