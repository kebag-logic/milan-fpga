[R435] NEGATIVE - exact head e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df

# R435-1: external review of PR #144 (lane C8, descriptor model lint), issues #38, #39, #60, #89

- Head `e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df`, tree `6abcaef4b82fffccc3e46a8ac51a5448ce17e741`. It is three commits on `main` `03c842a780064048b0a1a3de29214174a1c13934`.
- The detached review clone was verified at that head before and after every probe: HEAD, `write-tree` equal to the tree, `git status --porcelain --ignored` empty, `diff-index` empty. This repository records no gitlinks (`receipts/clone-integrity.txt`).
- Round 1. No public review findings, reviews or review comments existed on PR #144 when this verdict was written. The only PR comments are the two review-start notices.

## Verdict in one paragraph

The lint is real and well built:

- It runs by default inside `build()`, with an explicit `lint=False` / `--no-lint` opt-out.
- Every finding line names the rule, check, descriptor and clause. The CLI exits 1 and writes nothing on a refusal.
- The pre-existing structural refusals keep their text and order: 22 of 22 cases match the base packer byte for byte.
- The waiver mechanism refuses whole-rule, reason-less, malformed and stale waivers, and reports every waiver it applies.
- I independently reproduced:
  - the gate: 32 tests, rc 0;
  - the 53-of-53 check-suppression proof;
  - the parent's five models at dev `cdf49d1a` and at PR #634's heads `57f4b742` and `d81198c2`: four pack clean, and `ax7101_8x8` packs only with its reported #584 waiver;
  - the parent's builder test at dev `cdf49d1a` with both patches: rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`.

The verdict is still NEGATIVE, on six MINOR findings:

- **F1:** two checks are stricter than their cited clause and refuse conformant models. L2 `parent-order` applies the IEEE §7.2 multi-level numbering rule to single-level types.
- **F2:** L5 `interface-index` refuses a configuration that holds a subset of the interfaces at unchanged indices.
- **F3:** the L9 model digest over-excludes CONTROL value details. A structural selector change keeps the digest, so #38 item 3 does not hold in general.
- **F4:** the gate does not pin several refusal arms or the waiver's type and configuration scope. 8 of my 32 planted lint defects survive.
- **F5:** Milan §5.3.3.x "shall have the format of [ATDECC 7.2.x]" (descriptor extents), the §7.5.2 gPTP source format and the IEEE §7.2 508-octet maximum are neither linted nor listed in 07 §3.1's "Not linted" list.
- **F6:** the 47→46 format-cap correction that the PR body says was made "throughout" survives in three places: F01.5 `P-N-FORMATS-MAX`, 07 §3.3.1 and a `KL_aecp_desc_store.sv` comment.

## Findings

### F1: MINOR. L2 `parent-order` orders single-level child types, which IEEE §7.2 does not require

- **Lenses:** Conformance, Tests, Docs.
- **Where:**
  - `hdl/aecp/desc/model_rules.py:436-457` (`_rule_order`: the range-order loop applies to every child type except AVB_INTERFACE-owned CONTROLs);
  - `model_rules.py:80` (the `parent-order` clause, "IEEE 1722.1-2021 §7.2");
  - `tb/desc_store/lint_mutations.py:201-203` (the negative "output clusters before input clusters");
  - `docs/architecture/07_memory_maps.md:163` (L2 row).
- **Authority:**
  - IEEE 1722.1-2021 §7.2 states a walk-order numbering only "for descriptors which can appear at multiple levels of the hierarchy, such as the CONTROL descriptors".
  - §7.2.3 requires only "consecutively increasing indices for the Ports and Controls of the Unit".
  - §7.2.13 gives `base_cluster` / `base_map` per port and no order between ports.
  - The frozen L2 at the base (`03c842a7` 07 §3.1) reads "IEEE ordering for multi-level types".
- **Evidence:**
  - Probe B (`receipts/conformance-probes.txt`): a milan_min model whose output port owns AUDIO_CLUSTER 0..1 and whose input port owns 2..3 is refused: `L2 parent-order: cfg 0 STREAM_PORT_OUTPUT 0: its AUDIO_CLUSTER range starts at 0, before the end 4 of the range of STREAM_PORT_INPUT 0 (IEEE 1722.1-2021 §7.2)`. No CONTROL is involved.
  - The planted defect `order-control-only` restricts the order check to CONTROL, which is the IEEE §7.2 wording, and it is KILLED by the gate (`receipts/lint-planted-defects.txt`). The gate therefore pins the over-strict behaviour.
- **Impact:**
  - A consumer whose IEEE-conformant model numbers Stream Ports, AUDIO_CLUSTERs or AUDIO_MAPs in another order than the lint's walk is refused by default, under a clause that does not say so.
  - The consumer would have to carry a waiver, and that waiver's reason would track no real defect.
- **Required outcome:** do one of the following.
  - Apply the range-order part of `parent-order` only to multi-level types (CONTROL, and the other multi-level types if they are ever surveyed). Replace the cluster-order mutation with a CONTROL-order negative, for example a unit-owned CONTROL range before a configuration-level one, or two units' CONTROL ranges out of unit order.
  - Or keep the stricter order as a stated processor design restriction with its reason, cited as 07 §3.1 rather than IEEE §7.2, and amend the L2 row and `CHECKS["parent-order"]` to say so.
- **Verification:**
  - Probe B packs.
  - A CONTROL-order negative is refused with `L2 parent-order`.
  - The gate and the suppression proof stay green: 53 of 53.

### F2: MINOR. L5 `interface-index` refuses a configuration with a subset of the interfaces at unchanged indices

- **Lenses:** Conformance, Docs.
- **Where:**
  - `hdl/aecp/desc/model_rules.py:550-562` (`_rule_interfaces` requires each configuration's whole `{index: port_number}` map to equal configuration 0's);
  - `model_rules.py:96-97`;
  - `docs/architecture/07_memory_maps.md:166`.
- **Authority:** Milan v1.2 §5.3.3.5: "The PAAD-AE shall always use the same index, in all Configurations, for the AVB_INTERFACE descriptors that represent the same physical AVB interface". Nothing requires every configuration to hold every interface. F01.5 `P-N-AVB-INTERFACES` is "≥1", so multi-interface models are in the parameter's range.
- **Evidence:**
  - Probe C: configuration 0 holds AVB_INTERFACE 0 (port 1) and 1 (port 2). Configuration 1 holds only AVB_INTERFACE 0 (port 1, same index).
  - That model is refused: `L5 interface-index: cfg 1 AVB_INTERFACE: index-to-port_number {0: 1}; configuration 0 has {0: 1, 1: 2} (Milan v1.2 §5.3.3.5)`.
  - The planted defect `iface-subset` compares only indices both configurations hold. It survives, so the strict reading is not a pinned design choice.
- **Impact:** a §5.3.3.5-conformant multi-interface model is refused by default under that clause.
- **Required outcome:** do one of the following.
  - Compare per physical port: a `port_number` present in two configurations must sit at the same index. A configuration lacking a port is not a finding. Add a positive and a negative case for it.
  - Or state the stricter "same interface set in every configuration" rule as a processor restriction with its reason, not as §5.3.3.5.
- **Verification:** probe C packs; a model that moves a port to another index is still refused (the existing mutation).

### F3: MINOR. The L9 model digest does not apply IEEE 1722.1-2021 §6.2.2.8's exclusions as the docs claim; a structural CONTROL change keeps the digest

- **Lenses:** Conformance, Robustness, Docs.
- **Where:**
  - `hdl/aecp/desc/model_lint.py:117-125`. For any CONTROL whose `control_value_type` is not linear (0..9), it zeroes the whole `value_details` from `values_offset` to the end.
  - `model_lint.py:51-54`. `UNNAMED` omits MATRIX_SIGNAL (0x1E), which has no `object_name` (§7.2.26), so its structural bytes 4..67 are zeroed.
  - The claim in `docs/architecture/07_memory_maps.md:146-147`, `model_lint.py:33-35`, `docs/guides/integrator.md` §6 and the PR body: "SHA-256 over every descriptor, with the IEEE 1722.1-2021 §6.2.2.8 exclusions".
- **Authority:**
  - IEEE 1722.1-2021 §6.2.2.8 excludes, for selector types, only the `current` subfield of the value details (Table 7-123), and for array types only `current[X]`.
  - It excludes the whole `value_details` only for CONTROL_UTF8, SMPTE_TIME, SAMPLE_RATE, GPTP_TIME and VENDOR.
  - Milan v1.2 §5.3.1: a changed static model reports a different Entity Model ID.
- **Evidence:** probe F adds a configuration-level CONTROL_SELECTOR_UINT8 to milan_min.
  - Changing `option[2]` 3→7 leaves the digest UNCHANGED.
  - Changing `current` also leaves it unchanged, which is correct.
  - Changing the IDENTIFY control's linear `maximum[0]` changes it, which is correct.
- **Impact:**
  - `model-digest` (L9) accepts a structurally changed model under the same recorded `entity_model_id` whenever the change is in a non-linear CONTROL's options or limits. That is exactly the failure #38 item 3 exists to catch.
  - The secondary effect runs the other way: non-Milan dynamic fields that §6.2.2.8 excludes are not zeroed, so they would move the digest. These are MEMORY_OBJECT `length`, SIGNAL_SELECTOR `current_*`, VIDEO/SENSOR_CLUSTER `current_*`, and MIXER/MATRIX/SIGNAL_TRANSCODER current values.
  - The only recorded model (`milan_min.json`) has no selector CONTROL, so its recorded digest is unaffected. Its value is only as good as the function.
- **Required outcome:**
  - Zero exactly the §6.2.2.8 fields per value-type family (Tables 7-121 to 7-124, and the bode and array layouts), and restrict the `object_name` zeroing to types that carry one.
  - Either add the listed non-Milan exclusions or state in 07 §3.1 that the digest covers the Milan subset only.
  - Add a gate test: a selector option change moves the digest, and a selector `current` change does not.
- **Verification:**
  - Re-run probe F: option change → changed, current change → unchanged.
  - `IdentityTest.test_record_is_current` stays green: milan_min's digest is unchanged by the fix.

### F4: MINOR. The gate does not pin several refusal arms or the waiver's type/configuration scope; 8 of 32 reviewer-planted lint defects survive

- **Lenses:** Tests, Robustness.
- **Where:**
  - `tb/desc_store/test_gen_desc_image.py` (`LintTest` :233-280, `WaiverTest` :283-…);
  - `tb/desc_store/lint_mutations.py`;
  - the claims in `tb/desc_store/README.md:96-103` and `docs/architecture/09_verification.md` §8.4.
- **Authority:**
  - The ruling (#60 comment 5948872196) says a waiver "names the rule, the check and the descriptor scope", and is refused when it matches no descriptor.
  - Milan v1.2 §5.3.3.6 requires "exactly one" INPUT_STREAM source per CRF input, or on the single AAF input.
  - IEEE 1722.1-2021 Table 7-8 sets N ≤ 46.
  - #60 acceptance item 2 and #89 item 3 call for a negative case per refusal.
- **Evidence:** `receipts/lint-planted-defects.txt`, run by `scripts/lint_planted_defects.py`, one textual defect per isolated copy, with the whole gate run on each. 24 of 32 are KILLED. These SURVIVE:

  | Defect | What the gate does not pin |
  |---|---|
  | `cap45` | N cap 46→45: the corrected cap has no positive at 46. Probe E shows the head accepts 46. |
  | `rates7` | rate cap 8→7: no positive with 8 rates. Probe E shows the head accepts 8. |
  | `crf-ge1` | `crf-input-source` "exactly one" weakened to "at least one". Probe A shows the head refuses two sources; the gate has no such negative. |
  | `aaf-ge1` | the same for `aaf-input-source`. |
  | `waiver-anytype` | a waiver excusing its check on every descriptor type of its configuration. |
  | `waiver-anycfg` | a waiver excusing its check in every configuration. |
  | `entity-cfg` | an ENTITY outside configuration 0 accepted: the second arm of `entity-count`. |
  | `iface-subset` | see F2. |

  - The 53-of-53 suppression proof is reproduced (`receipts/probe-check-suppression.txt`), but it removes whole checks only. It cannot detect these partial weakenings.
  - Seven of the 56 mutations also trip other checks (`receipts/probe-mutation-exclusivity.txt`). Every one still requires its named check, and the docs do not claim exclusivity, so that is recorded, not a finding.
- **Impact:**
  - A future edit that lets a waiver silently excuse findings on another descriptor type or another configuration, or that breaks the "exactly one" arms or the cap boundaries, passes the gate that CI runs.
  - The waiver-scope property is the ruling's central safeguard.
- **Required outcome:** add these cases:
  - positives at the boundaries: 46 formats, 8 rates;
  - negatives for two INPUT_STREAM sources at one CRF input, and for one source on each of two AAF inputs with no CRF input;
  - an ENTITY in configuration 1;
  - waiver tests where the finding differs from the waiver only by descriptor type, and only by configuration (the waiver must be stale and the finding must be refused).
- **Verification:** re-run `scripts/lint_planted_defects.py`. All mutants except an F2 resolution are KILLED.

### F5: MINOR. Model "shall"s that are neither linted nor named in 07 §3.1's "Not linted" list

- **Lenses:** Conformance, Docs.
- **Where:**
  - `docs/architecture/07_memory_maps.md:174-178` ("Not linted, and left to the consumer's shipping checks: …");
  - `hdl/aecp/desc/model_rules.py`, which has no per-type extent check outside STREAM (L4), AUDIO_UNIT (L10) and CLOCK_DOMAIN (L6), and no general 508-octet bound.
- **Authority:**
  - Milan v1.2 §5.3.3.1, .2, .3, .5, .6, .7, .8, .9 and .11 each say the descriptor "shall have the format specified in [ATDECC, Clause 7.2.x]". §5.3.3.10 adds "[ATDECC, Clause 7.3.5.2]" for IDENTIFY.
  - Milan v1.2 §5.3.3.6 says that a gPTP source "shall be formatted as defined in Section 7.5.2": `clock_source_flags` = 0, location TIMING referencing a PTP_INSTANCE (§7.5.3, §7.5.4).
  - IEEE 1722.1-2021 §7.2: "The maximum length of a descriptor shall be 508 octets".
  - The question in scope is whether any Milan §5.3.2/§5.3.3 "shall" on the model is missing.
- **Evidence:**
  - Probe D: these all pack with the lint on: ENTITY 320 octets (312), CLOCK_SOURCE 90 (86), AUDIO_CLUSTER 94 and 86 (90), AVB_INTERFACE 104 (102), STREAM_PORT_INPUT 22 (20).
  - Probe I: an AUDIO_MAP of 520 octets packs. The packer's line bound is 576.
  - `receipts/milan-min-planted-defects.txt` `cluster-pad-rerec`: an AUDIO_CLUSTER padded by 4 octets, with the digest re-recorded, passes the gate.
  - `interface_flags` and `entity_capabilities`, by contrast, survive the same way (`ifflags-rerec`, `caps-rerec`) but ARE disclosed.
- **Impact:** the docs and the PR body present the "Not linted" list as the full residue of the processor lint. A consumer relying on the default lint as defence in depth would assume these shalls are covered.
- **Required outcome:** do one of the following.
  - Add the fixed-extent and 508-octet checks: one check per type, or one `descriptor-extent` check, with negatives.
  - Or add "descriptor formats and extents other than STREAM, AUDIO_UNIT and CLOCK_DOMAIN, the 508-octet descriptor maximum (IEEE §7.2), the IDENTIFY value format (IEEE §7.3.5.2) and the gPTP source chain format (Milan §7.5.2 to §7.5.4)" to the "Not linted" list, and to REQ-MDL-001's arch cell if needed.
- **Verification:** probe D/I outcomes match the chosen text. `make check` stays rc 0.

### F6: MINOR. The 47→46 format-cap correction is not done "throughout"

- **Lenses:** Docs, Conformance, RTL.
- **Where:**
  - `docs/architecture/01_overview.md:158`. F01.5, the single source of parameter values, reads `P-N-FORMATS-MAX | 16 | ≤47 (IEEE 1722.1-2021 Table 7-8)`.
  - `docs/architecture/07_memory_maps.md:326-327`: "Even the field limits alone, F ≤ 47 formats and R ≤ 8 redundant streams, give 138 + 8·47 + 2·8 = 530 B … (528 B)".
  - `hdl/aecp/KL_aecp_desc_store.sv:105-107` comment: "N capped at 47 formats and R at 8 redundant streams, so 530 B … 528 B".
- **Authority:**
  - IEEE 1722.1-2021 Table 7-8, `number_of_formats`: "The maximum value for this field is 46 for this version of AEM".
  - #60 comment 5854263065 asked that the processor statements be corrected under this issue.
  - The PR body states "The N cap is corrected from 47 to 46 throughout".
- **Evidence:** a repository search for `47` beside formats returns exactly these three sites. 07 §3.2 F07.3, 07 §3.1 L4, 00 REQ-MDL-003 and the lint (`FORMATS_MAX = 46`) are corrected.
- **Impact:**
  - A figure and a clause claim stay wrong in the parameter registry and in the sizing argument: 530/528 B where the 2021 field caps give 522/520 B.
  - The PR's "throughout" claim is not true at this head.
  - The `LINE_BYTES_P` = 576 conclusion is unaffected.
- **Required outcome:**
  - F01.5: ≤46.
  - 07 §3.3.1 and the RTL comment: F ≤ 46, 138 + 8·46 + 2·8 = 522 B, Annex C 520 B, conclusion unchanged.
- **Verification:**
  - A search for `47` beside formats in `docs/` and `hdl/` is empty.
  - `make check` (params, links, matrix) is rc 0.
  - `lint_hdl.sh` is rc 0. The RTL change is comment-only.

### RESIDUE, wording only (carried to the residue checklist; not verdict-bearing)

- **R1:** `hdl/aecp/desc/model_rules.py:222`. The `_family` docstring cites "IEEE 1722.1-2021 §7.3.2", which is Sampling Rate Ranges. Exact fix: "§7.3.3" (Stream Formats).
- **R2:** the PR body's "No caller of `build()` changes" (parent-adoption paragraph). The adoption patch does change gate 36b's test callers, by design. Exact fix: "No production caller of `build()` changes; gate 36b's test callers pass `lint=False` for its deliberate negatives and its index-walk and presence documents."

### SUGGESTION (not verdict-bearing)

- **S1:** a malformed recorded-digest map leaks a non-`ImageError` out of `build()`. `model_ids={"not-hex": …}` raises ValueError, and a list raises AttributeError (`receipts/model-ids-input-probe.txt`). The CLI then prints a traceback instead of `gen_desc_image: …`. Wrap the parsing of the map in `ImageError`.
- **S2:** waiver input types are coerced instead of refused:
  - `first: 0.2, last: 0.9` is accepted as 0..0;
  - `configuration: true` is read as configuration 1;
  - a list `reason` is accepted through `str()`;
  - two identical waivers are both applied and reported.

  Each is still reported and still subject to the stale test, so no waiver is silent. Strict JSON types and a duplicate-waiver refusal would match the ruling's "malformed is refused" more closely.
- **S3:** `gen_desc_image.py:128-131` prepends the packer's directory to `sys.path` for the whole consumer process. Importing `model_lint` / `model_rules` by path, as consumers import the packer, would avoid shadowing a consumer's own modules.
- **S4:** the 53-of-53 check-suppression proof is recorded in prose (README, 09 §8.4) but has no committed driver. A small committed driver would make the record re-runnable. `scripts/probe_check_suppression.py` here is one way.

## The four issues' own acceptance lists

- **#89: met in full.**
  1. L10 refuses an offset other than 144, a count above 8 and a length other than 144 + 4·count, each with an `ImageError` naming the rule.
  2. L6 refuses a non-identity `clock_sources` list.
  3. Each refusal has a negative case, run by `generator-check`, which `tb/desc_store`'s default `make` target runs. `scripts/run_suites.sh` runs that for every `tb/*/`, and the `hdl` workflow runs `run_suites.sh`.
  4. `example_milan_8.json` still packs, with `--no-lint` per the ruling.
- **#39: met in full.**
  1. L11 computes the maxima over every configuration. The two-configuration negative is "configuration 1 has two talkers".
  2. The report prints `talker_sources_i` / `listener_sinks_i`, and `adp=` checks them.
  3. `integrator.md` §6 states the §5.3.3.1 rule for both ports.
- **#38: items 1, 2 and 4 met; item 3 not met in general (F3).** Items 1, 2 and 4 are met: the 0 / all-ones negatives, the reported and checked `entity_model_id_i`, and `integrator.md` §6. Item 3, the recorded digest that refuses a structural change kept under the same id, holds for `milan_min.json`, the only recorded model, with a test that edits `buffer_length`. It fails for structural changes inside non-linear CONTROL value details (F3).
- **#60: acceptance items 1 to 4 met, with F1, F2, F4 and F5 as conformance and test caveats.** The in-issue correction request (comment 5854263065, N cap 46) is not fully met (F6).
  1. The lint refuses violations of L1 to L8.
  2. There is a negative per rule, including L6's identity permutation, CI-wired. The example builds.
  3. The four pre-existing refusals plus the configuration gap each gain a negative (`LayoutRefusalTest`). I re-checked their text against the base packer: `receipts/structural-refusal-parity.txt`, 22/22 identical.
  4. One ticket covers the REQ-MDL rows.

  So the PR's `Closes #38` and `Closes #60` are premature until F3 and F6 are resolved.

## Ruling points (5948872196) and the focus items

1. **Checks against clauses.**
   - Clauses were checked against the IEEE 1722.1-2021 and Milan v1.2 text: §5.3.1, §5.3.2, §5.3.3.1 to .11, §5.6.2, §6.2 to §6.4, §7.3, §7.5, IEEE §6.2.2.8, §7.2, §7.2.2, Tables 7-8, 7-9, 7-121 to 7-123.
   - Correct: the 46-format cap (Table 7-8 states it); the CRF word `0x041060010000BB80` (Milan Table 7.1); CLASS_A = 0x0002 (Table 7-9, bit 14 MSB-first); the AAF/`ut` decoding (Milan Table 6.2 words decode as intended); the Base-format rules (§6.3, §6.4); the IDENTIFY requirement (Milan §5.6.2 sets AEM_IDENTIFY_CONTROL_INDEX_VALID); and the CONTROL linear current offset (4V of 5V+4).
   - L6 against PR #142: the D1 shape (INTERNAL 0, CRF 1, one INPUT_STREAM source per AAF input) is accepted. It is accepted on PR #634's real 8×8 model, which has 10 sources, and in probe A.
   - The no-CRF case with one source on each of two AAF inputs is refused. That matches both §5.3.3.6 and PR #142's own L6 text ("exactly one … on the single AAF input when no CRF input exists").
   - Stricter or looser than the clause: F1, F2, F3. Missing shalls: F5.
   - The Table 7-8-only stream layout (Annex C refused) is a recorded design restriction (REQ-MDL-003, 07 §3.2 Δ note), not a finding.
2. **Refusal path.** Every lint line has the form `L<n> <check>: cfg … <TYPE> [<index>]: <detail> (<clause>)` (probe H). Waiver refusals name the waiver, its rule, check and scope. The CLI exits 1 and writes neither file (gate `CommandLineTest`). Structural refusals keep their order and text (22/22 parity). The exception is S1.
3. **Waivers.**
   - A waiver names one check only; the rule must match the check, so a whole rule cannot be waived.
   - The reason must cite `repo#N`.
   - Every applied waiver is reported.
   - A waiver is stale and refused if any descriptor in its scope is missing or passes its check, including when its range is widened by one port on the real 8×8 model.
   - A range-less waiver cannot cover indexed findings.
   - Gaps: test coverage of scope (F4) and input strictness (S2).
4. **ADP report and digest.** The four values are reported, and `adp=` checks them; the parent's overlay values agree on all five models at all three parent heads. The digest exclusions are the §6.2.2.8 list plus `entity_id` and `entity_model_id` themselves, which is justified as per-unit identity and the key. F3 covers the CONTROL and MATRIX_SIGNAL errors. No `.sv`/`.svh`/ucode file changed: there are no port, parameter or register changes (`git diff --stat 03c842a7..HEAD -- '*.sv' '*.svh' 'hdl/aecp/ucode/*'` is empty).
5. **Gate.**
   - `milan_min.json` packs, with its recorded digest.
   - There are 56 mutations over 53 checks; 49 trip only their check and 7 also trip cascades.
   - Suppression is 53/53, with the control passing.
   - The gate is CI-run through `run_suites.sh`. The hosted `suites` job at this head was still in progress at my last look; `docs-gates` and `portability` succeeded.
   - Planted `milan_min.json` defects: every linted defect is KILLED, including with the digest re-recorded. The disclosed unlinted fields (`interface_flags`, `entity_capabilities`) and the undisclosed extent (F5) survive once the digest is re-recorded.
6. **Parent patch.** `parent-adoption-c8-cdf49d1a.patch` (sha256 `aa5a88eb…`, equal to the manifest) touches seven files:
   - gate 36b's `_assert_image_contract_case` passes `lint=reason is None`, so only deliberate negatives pack lint-off;
   - the index-walk and presence documents pack with `lint=False`;
   - the 8×8 waiver travels config → builder → overlay (emitted only when declared) → `aem_specs` → `aem_assemble` → `model_to_document`;
   - one `ENDSTATION_BUILDER.md` §3 row (72 rows), which the manager accepted.

   Nothing else changes.

   With `parent-c4-disposition.patch` then the adoption patch on dev `cdf49d1a`, the processor at this head, and `gptp-processor` / `verilog-axis` at their gitlinks:
   - the parent's `sw/builder/test_builder.py` is rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`, the one being gate 11, which needs a board utilisation report not on this host;
   - gate 36b's six accepted cases, including "eight rates", pack with the lint on.

   At PR #634's heads `57f4b742` and `d81198c2`, the adoption patch's first `aem_assemble.py` hunk does not apply: context drift from #634's `CLKSRC_TABLE` line. I applied that one line by hand. The patch is named for `cdf49d1a`, so this is a note for the pin-adoption lane, not a finding.

## Lens evidence (artifact-specific)

- **Conformance:** clause-by-clause reading of `model_rules.py` `CHECKS` and rules against the standards text, plus probes A to I. Result: F1, F2, F3, F5, F6.
- **RTL:**
  - No RTL changed.
  - `tb/desc_store` built with Verilator 5.050 (wrapper identity in `receipts/verilator-identity.txt`): gate 32 tests OK, then RTL 584 checks, 584 PASS (`receipts/desc-store-suite.log`).
  - The L6 identity list and the L10 offset 144 / ≤ 8 match the SET_CLOCK_SOURCE / SET_SAMPLING_RATE contracts the docs cite.
  - F6 touches an RTL source comment.
- **Robustness:**
  - malformed waivers, stale waivers, a widened real waiver;
  - truncated descriptors (findings, not crashes);
  - malformed `model_ids` (S1);
  - the default-on path in three parent callers (builder path, adp check and CLI document, at three parent heads).
  - Result: F3, F4.
- **Tests:**
  - the gate (rc 0);
  - the suppression proof reproduced at 53/53;
  - my 32 planted lint defects (24 KILLED) and 12 planted `milan_min.json` defects (9 KILLED, 3 expected survivors);
  - the mutation-exclusivity table;
  - structural parity;
  - the parent builder test.
  - Result: F1, F4.
- **Docs:**
  - 07 §3.1 to §3.3, 00 REQ rows and GAP-08, 04 sourcing rows, 09 §8.4, `integrator.md` §6, the two READMEs, the PR body;
  - `make check` rc 0 and `gen_matrix.py --check` rc 0 in a scratch copy.
  - Result: F1, F2, F3, F5, F6, R1, R2.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F5, F6) | `model_rules.py` CHECKS and rules, `model_lint.py` digest and waivers, the standards text, probes A to I, parent models at 3 heads | R435-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |
| RTL | UNCLEAN (F6, comment only) | no RTL diff; `KL_aecp_desc_store.sv` comment; `tb/desc_store` RTL 584/584 with pinned Verilator 5.050 | R435-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |
| Robustness | UNCLEAN (F3, F4) | refusal path, CLI no-write, waiver edge probes, `model_ids` probe, default-on lint in the parent's builder test and models | R435-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |
| Tests | UNCLEAN (F1, F4) | gate 32/32, suppression 53/53, 32 planted lint defects, 12 planted model defects, exclusivity table, structural parity 22/22, parent builder test rc 0 | R435-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |
| Docs | UNCLEAN (F1, F2, F3, F5, F6; R1, R2 residue) | 07, 00, 04, 09, `integrator.md`, READMEs, PR body; `make check` rc 0, `gen_matrix --check` rc 0 | R435-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |

## Real limits

- **Not run:**
  - `./scripts/run_suites.sh` in full, `lint_hdl.sh`, the RTL mutation campaigns and the yosys flow;
  - the parent consumer set beyond the builder test;
  - the donor bank;
  - the builder test at PR #634's heads. There I only packed the five models, through the builder path and the `adp=` path.
- **Source copies:** the parent trees were scratch copies:
  - `git archive` of dev `cdf49d1a` from a local object store, and GitHub tarballs of `57f4b742` and `d81198c2`;
  - submodules from the recorded gitlinks; `external/` left empty, and nothing used it.
- **Standards text:** read from local text extractions of IEEE 1722.1-2021 and Milan v1.2. Clause numbers were checked against those extractions.
- **Hosted CI:** the hosted `suites` job at this head was in progress when last read (`receipts/hosted-check-runs.txt`). Its conclusion is not covered here.
- **Not hardware proof:** physical calibration was NOT RUN, and builder gate 11 was skipped for a missing board report. Skips are not hardware proof.

## Pending manager duties

- Run the donor bank (9) and the parent consumer set (16) at this head with `parent-c4-disposition.patch` and `parent-adoption-c8-cdf49d1a.patch`.
- Record the hosted `suites` conclusion for `e6cca1ff`.
- Build and validate the final current-dev candidate at the merge turn: source base `03c842a7`, live dev `cdf49d1a`.
- Carry R1 and R2 to the residue checklist.
- Note the adoption patch's one-hunk context drift at PR #634 for the pin-adoption lane.
- Reconcile with the internal reviewer's round.

## Receipts (all listed in MANIFEST.sha256)

`receipts/`:

- `gate-generator-check.{log,rc}`, `desc-store-suite.{log,rc}`, `verilator-identity.txt`;
- `probe-check-suppression.txt`, `probe-mutation-exclusivity.txt`, `lint-planted-defects.txt`, `milan-min-planted-defects.txt`;
- `conformance-probes.txt`, `structural-refusal-parity.txt`, `model-ids-input-probe.txt`;
- `parent-dev-builder-test.{log,rc}`, `parent-dev-models-lint.txt`, `parent-634-57f4b742-models-lint.txt`, `parent-634-d81198c2-models-lint.txt`, `parent-dev-patched-status.txt`, `parent-634-patched-status.txt`;
- `make-check.{log,rc}`, `gen-matrix-check.{log,rc}`, `hosted-check-runs.txt`, `clone-integrity.txt`.

`scripts/`: `run_desc_store_suite.sh`, `run_parent_builder_test.sh`, `probe_check_suppression.py`, `probe_mutation_exclusivity.py`, `lint_planted_defects.py`, `milan_min_planted_defects.py`, `conformance_probes.py`, `structural_refusal_parity.py`, `model_ids_input_probe.py`, `parent_models_lint.py`.

R435-1 FINISHED
