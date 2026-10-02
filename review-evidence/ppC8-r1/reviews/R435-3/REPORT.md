[R435] POSITIVE - exact head 97f6eace064901f223e13abed7026f96bc4df805

# R435-3: external review of PR #144 (lane C8, descriptor model lint), round 3

- **Scope:** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #144 (issues #38, #39, #60 and #89). Review start: PR #144 comment 5957946831.
- **Exact head:** `97f6eace064901f223e13abed7026f96bc4df805`, tree `4ce73f7e28cded098788e23a7a056c976d9650aa`. That is the round-2 head `9610098a` plus three commits:
  - `b92f762`: L4 accepts Annex C;
  - `8b28ab4`: the arms are pinned and the digest is tested field by field;
  - `97f6eac`: one shared loader.
- **Clone integrity:** I checked the detached review clone at the end of the review. HEAD and `write-tree` equal the head and its tree. `git status --porcelain --ignored` and `diff-index` are empty. Index modes, blobs and paths are identical to the HEAD tree. The repository records no gitlinks, so no submodule pin applies (`receipts/clone_integrity_end.txt`). Every probe ran in a disposable `git archive` extraction under `scratch/`; nothing in the clone was written.
- **Reconstruction order:**
  1. README.md and docs/README.md. The repository has no AGENTS.md or CONTRIBUTING.md.
  2. Issue #60: its body and acceptance, the 46-cap report (5854263065), the assignment, STOP and ruling (5948562638, 5948825547, 5948872196), the round-2 assignment (5952457756), and the round-3 assignment and ruling (5956187186) with its REVIEW READY (5957709319).
  3. The PR body's Round 3 section.
  4. IEEE 1722.1-2021 §6.2.2.8, §7.2 and §7.2.6 Table 7-8, and Milan v1.2 §5.3.3.4, Annex C Table C.1 and the "Redundant Pair" definition, all read from the text.
  5. `git diff 2ebd4fe8..97f6eace` and `git diff 9610098a..97f6eace`, and the history.
  6. The public author packet `review-evidence/ppC8-r1/author-r3` (milan-fpga archive `ed074116`).
- **Prior findings:** I read the prior public findings (R435-2 and R434-2) only after my own pass over the diff and my own round-3 probes (`scripts/r3_probes.py`). Each one is dispositioned below.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head, and every lens is CLEAN. There is no RESIDUE, and one SUGGESTION (S1).

Both round-2 MINOR findings are closed under their original severity:
- **R435-2 F1 (Annex C):** L4 `stream-layout` now accepts the Milan v1.2 Annex C Table C.1 layout, redundancy tail included, beside IEEE Table 7-8. It still refuses every inconsistent layout.
- **R435-2 F2 (unpinned arms):** every `identify-format` arm and both digest arms are pinned. My round-2 plant script, run unchanged, kills 37 of 37.

R435-2 R1 (the PR title) and S1 (one guarded loader) are closed. R434-2's F1 and F2 are closed as well, and its S1 and S3 were taken.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding.

### S1: SUGGESTION. `test_one_guarded_loader` does not pin that `model_rules` loads through the shared loader

- **Lenses:** Tests, Robustness.
- **Where:**
  - `tb/desc_store/test_gen_desc_image.py:903-911` (`CommandLineTest.test_one_guarded_loader`);
  - `hdl/aecp/desc/model_lint.py:50-51`;
  - `hdl/aecp/desc/gen_desc_image.py:131-145`.
  - The claim is in `docs/architecture/09_verification.md:315` ("both load through the packer's one guarded loader", credited to `CommandLineTest`) and in `tb/desc_store/README.md:132`.
- **Evidence:**
  - The test asserts two things: `model_lint.beside is gen_desc_image._beside`, and that `_beside` raises `ImportError` when no spec is found.
  - My plant `g-own-loader` (`scripts/r3_plants.py`, `receipts/r3_plants_head.log`) gives `model_lint` its own unguarded loader for `model_rules` again. The gate stays green (SURVIVED).
  - At this head the code does route `model_rules` through `_beside`: `model_lint.model_rules.beside is _beside` is True (`receipts/loader_route_head.txt`).
- **Why it is not MINOR:**
  - The shared guard is round-2 suggestion S1. The assignment took it, but it is not an acceptance item.
  - The code at this head is correct.
  - A regression would only change the exception raised for a missing sibling file that ships beside the packer, from `ImportError` to `AttributeError`. No lint result, figure, digest or conformance claim depends on it.
- **Suggested outcome:** add `self.assertIs(gen_desc_image.model_lint.model_rules.beside, gen_desc_image._beside)` to the test. The loader binds itself into every module it loads, so this one line pins the route, and `g-own-loader` then dies.

## Prior public findings at this head

| Finding | Original severity | Status at 97f6eace | Evidence |
|---|---|---|---|
| R435-2 F1: L4 refuses Milan Annex C | MINOR | **Closed.** `_stream_layout` (`hdl/aecp/desc/model_rules.py:626-652`) accepts Table 7-8 (138) and Annex C (136, `redundant_offset` 136+8N, length 136+8N+2R, R ≤ 8). It still refuses a moved list, offsets that disagree, a Table 7-8 tail and R > 8. The clause (`:165-167`), the 07 §3.1 L4 row, the 07 §3.2 Δ note and REQ-MDL-003 cite Milan §5.3.3.4 and Annex C Table C.1. The round-2 probes A1 and A2 now pack. The resolution follows the round-3 ruling (5956187186), which superseded my round-2 "keep refusing R > 0" outcome. | `receipts/rerun_r435_r2_probes.log` (0 unexpected of 45), `receipts/r3_probes_head.log` |
| R435-2 F2: `identify-format` 7 of 8 arms and 2 digest arms unpinned | MINOR | **Closed.** There are 8 `identify-format` mutations, one per arm, each with a `detail` naming its arm. The r and u flag positive is `test_identify_value_type_flags`. The array `unit`/`string` neighbours and the MIXER selector and array cases are in `VALUE_EXCLUSIONS`. `scripts/prior-r435-2/r2_plants.py`, run unchanged (sha256 equal to the published R435-2 manifest), kills **37 of 37**. | `receipts/rerun_r435_r2_plants.log`, `receipts/prior_scripts_sha256.txt` |
| R435-2 R1: PR title "L1 to L11" | RESIDUE | **Closed.** The title reads "rules L1 to L12". | PR #144 title |
| R435-2 S1: share the None-spec guard | SUGGESTION | **Taken.** `_beside` is the one loader and `model_lint` loads `model_rules` through it. The test's coverage of that route is S1 above. | `receipts/loader_route_head.txt`, `receipts/r3_plants_head.log` (`g-no-guard` KILLED) |
| R434-2 F1: Annex C refused | MINOR | **Closed** (as R435-2 F1). | as above |
| R434-2 F2: identify arms, 508 boundary, partial overlap, digest "field by field" | MINOR | **Closed.**<br>- A 508-octet CONTROL packs (`test_boundaries_pack`).<br>- Waivers 1..2 and 2..3 are refused as overlapping, and cluster 3's finding stands (`test_partly_overlapping_waivers_are_refused`).<br>- `FIXED_EXCLUSIONS` lists every fixed-offset field of §6.2.2.8. I checked it against the clause text.<br>- That reviewer's `plant_r2.py` and `plant_r435_titles.py`, run unchanged, kill 37 of 37 and 8 of 8. | `receipts/rerun_r434_plant_r2.log`, `receipts/rerun_r434_plant_r435_titles.log`, `receipts/rerun_r434_probe_r2.log` |
| R434-2 S1 (other CONTROL owners, interface first in configuration 1) and S3 (flag positive) | SUGGESTION | **Taken:** `test_other_control_owners`, `test_interface_first_in_a_later_configuration`, `test_identify_value_type_flags`. | gate log |
| R434-2 S2; R434-1 S3, S4 | SUGGESTION | **Retained, not taken** (not asked by the assignment). Not verdict-bearing. | PR body "What remains (round 3)" |
| R435-1 F1 to F6, R434-1 F1 to F4 (round 1) | MINOR | **Remain closed.**<br>- My round-1 conformance probes, run unchanged, give output byte-identical to round 2.<br>- My round-1 lint plants give 29 KILLED and 3 INVALID. The third INVALID is `tail-off`: its target text `if tail:` was rewritten this round. The new arm is pinned by my round-3 plants `c-tail-in-78` and `c-tail-in-c-refused`, both KILLED.<br>- milan_min plants: the same 10 KILLED and 2 disclosed not-linted survivors as round 2.<br>- model-ids inputs: identical to round 2. | `receipts/rerun_r435_r1_*.log` |

## The five lenses

### Conformance: CLEAN

- **IEEE 1722.1-2021 §7.2.6 Table 7-8:**
  - `formats_offset` "is 138", N max 46;
  - `redundant_offset` "138 + 8*N", `number_of_redundant_streams` R max 8;
  - `timing` at 136;
  - `redundant_streams` 2*R octets at 138+8*N.
- **Milan v1.2 Annex C Table C.1:**
  - `formats_offset` "is 136", no `timing`;
  - `redundant_offset` "136+8*N", R max 8;
  - `redundant_streams` at 136+8*N, "2*R" octets.
- **2R, not 8R:** the author was right to take 2R where the assignment wrote 8R. Both tables give two octets per redundant stream. Plant `c-tail-8r` (the assignment's reading) is KILLED.
- **R ≤ 8** is the bound in both tables. `c-rmax-9`, `c-rmax-7`, `c-rmax-ge` and `c-rmax-any` are KILLED.
- **A Table 7-8 tail is refused.** Milan v1.2 §5.3.3.4 says a PAAD-AE "shall use [Annex C] for the Streams that are part of the redundant pair". The Milan "Redundant Pair" definition and Annex C's "redundant association" make any stream that names redundant streams part of such a set. The refusal is therefore Milan's rule, cited as §5.3.3.4, and not a processor-only restriction.
- **The N cap of 46 holds for Annex C too.** Table C.1 states 47, but 136 + 8·47 = 512 exceeds §7.2's 508-octet maximum (probe B2). The L4 row states "formats at 138 or 136" under the 508-octet cap.
- **Probes** (`scripts/r3_probes.py`, built with its own layout helper rather than the gate's; `receipts/r3_probes_head.log`: 31 probes, 0 unexpected):
  - **Positives:** every stream in Annex C with R = 0; an Annex C output with R = 1; R = 8; an input pair with each stream naming the other; N = 46 with R = 0 (504 octets); N = 46 with R = 2 (508 octets).
  - **Negatives:**
    - N = 46 with R = 3 (510 octets, L12);
    - N = 47 (L4 `format-count`, L12);
    - R = 9 and R = 32768;
    - a Table 7-8 tail;
    - each layout with the other's `redundant_offset`;
    - R counted with no tail;
    - stray tail octets, at R = 0 and at R = 1;
    - a Table 7-8 body whose offset alone changed to 136;
    - offsets 137 and 140.
  - **Lists read through `formats_offset`:** an Annex C list's `current-format`, `format-family` and `format-count` are all read through the offset.
  - **Discrimination:** the same probes against the round-2 tree give 12 unexpected (`receipts/r3_probes_at_r2_base.log`).
- **Digest:**
  - milan_min's recorded digest is unchanged at `6d7982fb…`, identical to round 2. The images and maps of milan_min and example_milan_8 are byte-identical to round 2 (`receipts/example_and_milan_min_images.txt`).
  - In an Annex C stream, `current_format` stays excluded, while `formats_offset`, the formats at 136 and the `redundant_streams` move the digest (probe D2). A relayout moves the digest (D1).
  - The round-3 test tables (`FIXED_EXCLUSIONS`, `VALUE_EXCLUSIONS`, `test_object_name_is_the_clause`) match the §6.2.2.8 list:
    - ENTITY: the seven fields;
    - AUDIO_UNIT, the streams, CLOCK_SOURCE, CLOCK_DOMAIN, SIGNAL_SELECTOR, VIDEO_CLUSTER, SENSOR_CLUSTER, MEMORY_OBJECT and AVB_INTERFACE;
    - linear in CONTROL, MIXER, MATRIX and SIGNAL_TRANSCODER; selector and array in CONTROL, MATRIX and SIGNAL_TRANSCODER only; Bode; the whole UTF8, SMPTE, sample-rate, gPTP and vendor values in CONTROL.
  - The docs' "field by field" now holds at the granularity they state.
- **The ruling's other items:**
  - The redundant-pair rules are on 07 §3.1's "Not linted" list, citing processor #69 (wave 3). An unpaired R = 1 tail packs (probe A2), as that ruling requires.
  - The L4 row and REQ-MDL-003 cite what is accepted.
- **Parent models (my scripts):**
  - At dev `cdf49d1a` (C4C6 patch, then C8 patch, both clean) and at PR #634 `d81198c2` (the C8 `aem_assemble.py` hunk ported, one line, as disclosed), every artifact of the builder path, and the direct `build(..., adp=)` image and report, of the five parent models are **byte-identical** between the round-2 and round-3 processor trees, model digests included (`receipts/parent_pack_*`).
  - My round-1 parent script, run unchanged at this head, prints output identical to my round-2 logs at both heads:
    - four models pack with no waiver;
    - `ax7101_8x8` packs only with its #584 waiver, is refused on STREAM_PORT_INPUT 0..7 without it, and is refused as stale when it is widened.
  - The C8 patch is unchanged (sha256 `aa5a88eb…`).

### RTL: CLEAN

- No `.sv`, `.cpp` or microcode file changes between `9610098a` and the head.
- From base `2ebd4fe8`, the only RTL change is comment lines in `KL_aecp_desc_store.sv` (0 non-comment lines changed).
- `gen_ucode.py`'s READ_DESCRIPTOR stream path copies `formats_offset` through verbatim and reads only `current_format` @74, so an Annex C image is served unchanged. No port, parameter or register changes.
- `lint_hdl.sh` (pinned Verilator 5.050, identity in `receipts/tool_identity.txt`) is rc 0.
- The `tb/desc_store` suite (`make run`) is rc 0: the gate, then 584 checks, 584 PASS.

### Robustness: CLEAN

- **Short descriptors:** `_stream_layout` reads R as 0 when the field is absent (`or 0`), and runs only when the list was read through `formats_offset`.
- **A huge R** (32768) is refused on both the bound and the length, without an exception.
- **The loader:**
  - `_beside` raises `ImportError` naming the file on a `None` spec (`g-no-guard` KILLED).
  - Loading by path leaves `sys.path` unchanged and registers no `model_lint` or `model_rules` module (probes E1 and E2, round-2 probe F1).
  - A direct `import model_lint` now fails with `NameError` (`receipts/loader_route_head.txt`). The PR body discloses this ("loads only through `gen_desc_image`"). Neither parent head references `model_lint` or `model_rules` outside the processor (`git grep` at `cdf49d1a` and `d81198c2`: no match).
- **Malformed waiver and model-ids inputs:** the round-1 probe results are identical to round 2.

### Tests: CLEAN (S1 is a suggestion)

- **The gate:** 58 tests OK (`receipts/gate_head.log`).
- **The mutations:** 89, over 56 checks, equal as a set to `CHECKS`. `stream-layout` has 9 and `identify-format` has 8 (`receipts/mutation_counts_head.txt`).
- **Check suppression:** the committed driver passes its control and kills 56 of 56 checks.
- **My statement deletion** (`scripts/r3_statement_kill.py`): I selected by AST every `*.bad(...)` statement in `model_rules.py` and `model_lint.py` and every `raise` in `model_lint.py`. Each replaced alone by `pass` fails the gate: **79 of 79 KILLED**.
- **My round-3 plants** (`scripts/r3_plants.py`): 16 one-line plants on the delta (offset arms, Annex C end, `redundant_offset`, the Table 7-8 tail, both directions of the R bound, 8R, a dropped tail, a longer body, the Annex C offset, the loader guard). **15 KILLED.** `g-own-loader` survives (S1).
- **Prior scripts run unchanged:**
  - R435-2: `r2_plants.py` 37/37, `r2_probes.py` 0/45 unexpected;
  - R434-2: `plant_r2.py` 37/37, `plant_r435_titles.py` 8/8, `probe_r2.py` as expected;
  - R435-1 round-1: see the table above.

### Docs: CLEAN

- **07 §3.1:**
  - The L4 row matches the code: both layouts, R ≤ 8, 2R, 508.
  - The clause column cites Milan §5.3.3.4, Annex C Table C.1, and IEEE §7.2 and Table 7-8.
  - The "Not linted" list has the redundant-pair item with #69.
- **The 07 §3.2 Δ note** gains the lint sentence. F07.3 still describes what this design's images carry (Table 7-8, R = 0), which is consistent.
- **REQ-MDL-003's Arch cell** states both accepted layouts.
- **09 §8.5 rows** match the tests and counts (89 mutations, 56/56, the 508 positive, the eight IDENTIFY arms, the Annex C positives, partial overlap, the §6.2.2.8 tables). The "both load through the packer's one guarded loader" claim is literally true of the code. Its test coverage is S1.
- **The `tb/desc_store` README:** the round-3 rows match my reruns.
- **The PR body Round 3** matches the measured results. It discloses:
  - the 2R reading;
  - the R ≤ 8 negative;
  - the `example_milan_8.json` change (still refused with the lint on, now not for L4);
  - the Round 2 item 5 correction;
  - the no-own-loader change.
- **Gates:** `make check`, `gen_matrix.py --check` and `git diff --check 2ebd4fe8..97f6eace` are rc 0. `git apply --check` passes on 205 of 205 campaign patches.

## Executed checks at this head

| Check | Result | Receipt |
|---|---|---|
| packer gate `test_gen_desc_image.py` | rc 0, 58 tests OK | `receipts/gate_head.log` |
| `tb/desc_store` `make run` (pinned Verilator 5.050) | rc 0; 584 PASS, 0 FAIL | `receipts/desc_store_run_head.log` |
| `lint_suppression.py --jobs 8` | rc 0; control passes; 56 of 56 killed | `receipts/suppression_head.log` |
| `make check`, `gen_matrix.py --check`, `lint_hdl.sh` | rc 0 each | `receipts/make_check_head.log`, `receipts/gen_matrix_head.log`, `receipts/lint_hdl_head.log` |
| `git diff --check 2ebd4fe8..97f6eace`; campaign `git apply --check` | rc 0; 205 of 205 | `receipts/diff_check.log`, `receipts/campaign_apply_check_head.log` |
| round-3 probes (own) | 31 probes, 0 unexpected (12 unexpected against the round-2 tree) | `receipts/r3_probes_head.log`, `receipts/r3_probes_at_r2_base.log` |
| round-3 plants (own) | 15 of 16 KILLED; `g-own-loader` SURVIVED (S1) | `receipts/r3_plants_head.log` |
| refusal-statement deletion (own, AST-selected) | 79 of 79 KILLED | `receipts/r3_statement_kill_head.log` |
| R435-2 `r2_plants.py` / `r2_probes.py`, unchanged | 37 of 37 KILLED / 0 of 45 unexpected | `receipts/rerun_r435_r2_*.log` |
| R434-2 `plant_r2.py` / `plant_r435_titles.py` / `probe_r2.py`, unchanged | 37 of 37 / 8 of 8 KILLED / as expected | `receipts/rerun_r434_*.log` |
| R435-1 round-1 scripts, unchanged | conformance byte-identical to round 2; lint plants 29 KILLED, 3 INVALID (rewritten targets); milan_min 10 KILLED, 2 disclosed; model-ids identical | `receipts/rerun_r435_r1_*.log` |
| parent five models, round-2 vs round-3 processor, at dev `cdf49d1a` and PR #634 `d81198c2` | byte-identical artifacts and digests at both heads | `receipts/parent_pack_*`, `receipts/parent_setup.txt`, `receipts/parent_patches_sha256.txt` |
| round-1 parent script, unchanged, at this head | identical to round 2 at both heads | `receipts/rerun_parent_models_lint_*` |
| hosted runs at the head (read-only) | `docs-gates` and `portability` succeeded (2 runs each); `suites` was in progress at my look (17:54Z) | `receipts/hosted_check_runs_97f6eace.txt` |

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `model_rules.py` `_stream_layout`, `CHECKS["stream-layout"]`, constants, against IEEE 1722.1-2021 §7.2, §7.2.6 Table 7-8 and Milan v1.2 §5.3.3.4, Annex C Table C.1, "Redundant Pair"; `model_lint.py` digest against §6.2.2.8; 31 own probes; parent five models at two parent heads | R435-3 | 97f6eace064901f223e13abed7026f96bc4df805 |
| RTL | CLEAN | `KL_aecp_desc_store.sv` (comment-only from base), `gen_ucode.py` stream READ_DESCRIPTOR path, no port/parameter/register change; `lint_hdl.sh`; `tb/desc_store` 584/584 | R435-3 | 97f6eace064901f223e13abed7026f96bc4df805 |
| Robustness | CLEAN | short/huge-R stream inputs, `_beside` guard and binding, by-path load isolation, direct-import behaviour and parent references, malformed waiver/model-ids inputs | R435-3 | 97f6eace064901f223e13abed7026f96bc4df805 |
| Tests | CLEAN | gate (58), 89 mutations, suppression 56/56, own statement deletion 79/79, own plants 15/16 (S1), both reviewers' round-2 scripts and my round-1 scripts unchanged | R435-3 | 97f6eace064901f223e13abed7026f96bc4df805 |
| Docs | CLEAN | 07 §3.1 L4 row and "Not linted", §3.2 Δ note and F07.3, 00 REQ-MDL-003, 09 §8.5, `tb/desc_store` README, PR body Round 3; `make check`, `gen_matrix --check` | R435-3 | 97f6eace064901f223e13abed7026f96bc4df805 |

## Real limits

- I did not run the full `run_suites.sh`, the parent consumer set (16), the parent builder test or the donor bank. Those belong to the manager. I ran the focused suite (`tb/desc_store`), the gate, the suppression driver, `make check`, `gen_matrix.py --check` and `lint_hdl.sh`.
- The parent trees are scratch extractions of dev `cdf49d1a` and PR #634 `d81198c2`, limited to the paths the packing path reads: `sw`, `avdecc`, `configs`, `docs`, `scripts`, `hdl/milan/KL_pp_shadow.sv`, `hdl/common/csr` and `tb/verilator/nvm_capture_cpu`. `gptp-processor` sits at its gitlink `5dce647a`. They are not full checkouts.
- PR #634's head has moved past `d81198c2` (it read `0b066b6e` at my look). I used the head the assignment names.
- Clause checks were made against the reviewer's copies of IEEE 1722.1-2021 and Milan v1.2. The spec text is not distributed in this packet.
- `scripts/prior-r435-2/round1/run_desc_store_suite.sh` was not used. Its published blob differs from the hash in the R435-2 manifest, consistent with that packet's path redaction. Every Python script I re-ran matches its published manifest hash.
- Hosted `suites` was still in progress at my look. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- The donor bank (9) and the parent consumer set (16) at this head; hosted and act acceptance, including the in-progress `suites` jobs.
- The final current-dev candidate at the merge turn (source base `2ebd4fe8`, live dev `cdf49d1a`). Note that PR #634 has advanced to `0b066b6e`.
- Optional: S1 (one assertion in `test_one_guarded_loader`).

R435-3 FINISHED
