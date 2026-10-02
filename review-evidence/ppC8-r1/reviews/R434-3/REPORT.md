[R434] POSITIVE - exact head 97f6eace064901f223e13abed7026f96bc4df805

# R434-3: internal independent review of processor PR #144 (lane C8, descriptor model lint), round 3

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. PR #144 serves issues #38, #39, #60 and #89.
- Exact head `97f6eace064901f223e13abed7026f96bc4df805`, tree `4ce73f7e28cded098788e23a7a056c976d9650aa`. It adds three commits on my round-2 head `9610098a`:
  - `b92f762`: L4 `stream-layout` accepts Milan Annex C;
  - `8b28ab4`: the arms are pinned, and the digest is tested field by field;
  - `97f6eac`: the one guarded loader.
- Review start: PR #144 comment 5957945930.
- I reconstructed scope in this order:
  1. README.md and docs/README.md. This repository has no AGENTS.md or CONTRIBUTING.md.
  2. Issue #60's body and acceptance, and every #60 comment: the 46-cap report, the lane assignment, the STOP and its ruling, the round-2 and round-3 assignments (5952457756, 5956187186) and the three REVIEW READY notes.
  3. The PR body, including its Round 3 section.
  4. The cited clauses, read in the standards themselves:
     - Milan v1.2 §5.3.3.4 and Annex C Table C.1;
     - IEEE 1722.1-2021 §7.2.6 Table 7-8, §6.2.2.8, and Tables 7-122 to 7-126 for the value-detail layouts;
     - the §7.2.17, §7.2.18, §7.2.24, §7.2.25 and §7.2.31 field offsets.
  5. The diffs `9610098a..97f6eace` and `2ebd4fe8..97f6eace`, and their history.
  6. The public author-r3 packet at milan-fpga archive `ed074116` (`review-evidence/ppC8-r1/author-r3`). All 54 files match that archive's MANIFEST.json, and `parent-adoption-c8-cdf49d1a.patch` is still `aa5a88eb…`.
- Order of work:
  - I fixed my verdict and ledger before reading any other reviewer's report.
  - I re-read my own round-2 findings only after my independent pass over the delta.
  - The other reviewer's round-2 findings are resolved in the last section, which I wrote after the verdict.

## Verdict

POSITIVE. Both of my round-2 MINOR findings are closed at this head under their original severity. Every plant in my unchanged round-1 and round-2 scripts, and in 40 new round-3 plants, is KILLED. No finding of MINOR or higher is open.

- **R434-2 F1 (L4 Annex C) is closed.** `stream-layout` accepts two layouts and still refuses every inconsistent one:
  - IEEE 1722.1-2021 Table 7-8: formats at 138, no tail;
  - Milan v1.2 Annex C Table C.1: formats at 136, `redundant_offset` 136 + 8N, length 136 + 8N + 2R, with R ≤ 8.
  - **The author's change to 2R is correct.** Table C.1 gives `redundant_streams` as "2\*R" octets of descriptor indices, and so does Table 7-8. The assignment's "8R" was the error.
  - **The R ≤ 8 bound is the standard's.** Table C.1 and Table 7-8 both say "The maximum value for this field is 8 for this version of AEM", and IEEE §7.2.6 says "between 0 and 8".
  - **Refusing a tail in Table 7-8 layout is grounded in Milan v1.2 §5.3.3.4:** "shall use it for the Streams that are part of the redundant pair".
  - **The microcode does not depend on the layout.** It reads only octets 74 to 87 of a stream (`gen_ucode.py` E_RDESCSF), and those are the same in both layouts.
  - **milan_min's digest is unchanged** at `6d7982fb…`. It is equal at both heads and to `model_ids.json`.
- **R434-2 F2 (unpinned arms, "field by field") is closed:**
  - each `identify-format` arm has its own named mutation;
  - the r and u flag positives exist;
  - a 508-octet descriptor packs;
  - a partial waiver overlap is refused;
  - the digest test is now literally field by field. My own octet-by-octet partition of 43 descriptor shapes against §6.2.2.8 agrees exactly with the code.
- **The loader change is sound.** `model_lint` and `model_rules` load only through `gen_desc_image._beside` and its `None`-spec guard. The five parent models pack byte-identically to round 2, at dev `cdf49d1a` and at #634 `d81198c2`.

Issue acceptance:

- #38, #39 and #89 are met in full, as in rounds 1 and 2, and round 3 regresses nothing.
- #60 items 1 to 4 are met, and so is the 46-cap correction:
  - L1 to L8 each refuse their negatives (89 mutations over 56 checks);
  - the layout refusals have negatives;
  - `example_milan_8.json` still packs, byte-identical to main `2ebd4fe8`.
- The four `Closes` lines stand.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding is open at this head.

### Suggestions (do not affect the verdict)

- **S1 (Robustness):** `model_lint.py` loaded directly, not through the packer, now fails with `NameError: name 'beside' is not defined` (`hdl/aecp/desc/model_lint.py:50-51`, `receipts/example_image_and_loader.txt`).
  - The PR body discloses that the module no longer loads on its own, and no caller loads it that way. That includes `tb/`, `lint_suppression.py` and, by the author's parent receipts, the parent.
  - A one-line guard would turn a future direct import into a self-explaining `ImportError`. For example: `if "beside" not in globals(): raise ImportError("load model_lint through gen_desc_image")`.
- **Carried, not adopted (the assignment did not ask for them):**
  - R434-2 S2: prefer a top-level IDENTIFY for the reported `identify_index_i`;
  - R434-1 S3: a `ut`-carrying `current_format` listed verbatim is accepted;
  - R434-1 S4: mutations pin their named check, not their exact check set.

## Prior public findings at this head (my own)

| Finding | Original severity | Status at 97f6eace | Evidence at this head |
|---|---|---|---|
| R434-2 F1 L4 `stream-layout` refuses Milan Annex C | MINOR | CLOSED | `model_rules.py:625-652`. The clause cites "Milan §5.3.3.4, Annex C Table C.1; IEEE §7.2.6 Table 7-8" (`:165-167`). My unchanged round-2 probe A1 (Annex C, R = 0) was REFUSED and is now ACCEPTED; every other line of `probe_r2.py` is identical (`receipts/r2_probes_rerun.txt`). Independent probes A0 to A17 (`receipts/probe_r3.txt`):<br>- **Packs:** R = 0 on every stream; R = 1 naming itself; a redundant output pair on two interfaces; R = 8; N = 44 with R = 8 (504 octets); N = 46 with R = 0.<br>- **Refused:** R = 9; N = 45 with R = 8 (512 octets, L12); formats_offset 136 with `timing` kept; Table 7-8's `redundant_offset` in Annex C; an R = 0 tail; R = 1 with two indices; a Table 7-8 tail of consistent length; Annex C's `redundant_offset` in Table 7-8; formats_offset 137; Table 7-8 with R = 9 (both arms).<br>- **List read at 136:** an Annex C input whose `current_format` is outside its list is refused with `current-format`.<br>The `test_example_is_a_layout_vector` assertion is inverted, as required. The L4 row (`07:184`), the 07 §3.1 "not linted" list (`07:212-214`, #69), the §3.2 Δ note (`07:259-262`) and REQ-MDL-003 (`00:448`) cite what is accepted. |
| R434-2 F2 unpinned arms; "field by field" broader than the tests | MINOR | CLOSED | My unchanged `plant_r2.py` kills **37 of 37** (17 at round 2). That includes every `N-identify-*` plant, `N-identify-no-mask`, `N-max-refuses-507-508`, `N-overlap-identical-only` and the five `N-digest-keeps-*` survivors (`receipts/plants_head_plant_r2.txt`). New `plant_r3.py`, 40 of 40 KILLED (`receipts/plants_head_plant_r3.txt`):<br>- each mask flag alone;<br>- the 508 boundary;<br>- nested-only overlap;<br>- 24 digest plants: each span dropped, narrowed or widened, NAMED ± one type, each WHOLE type, the UINT8 start, the selector STRING, MIXER and MATRIX families, the array, linear and Bode current offsets;<br>- the guard and loader plants.<br>Octet-partition probe D (`receipts/probe_r3.txt`): 27 fixed-offset types and 16 value-family shapes. The set of octets that keep the digest equals my own §6.2.2.8 field table exactly in all 43, and every other octet moves the digest. The README, 09 §8.5 and PR body claims now match the tests. |
| R434-2 S1 other CONTROL owners, interface first in configuration 1 | SUGGESTION | ADOPTED | `ConformingModelTest.test_other_control_owners` and `test_interface_first_in_a_later_configuration`. `N-owners-no-avb`, `N-owners-no-ptp`, `N-owners-no-control-block`, `N-unit-no-ext-port-ranges` and `N-l5-missing-port-finding` are KILLED. |
| R434-2 S2 top-level IDENTIFY preference | SUGGESTION | not adopted (carried) | Unchanged at `model_rules.py:796-797`. |
| R434-2 S3 r-flag positive | SUGGESTION | ADOPTED | `test_identify_value_type_flags`. Probe B: 0x8001, 0x4001 and 0xC001 pack; 0x2001 and 0x0002 are refused. |
| R434-1 F1 to F4, R435-1 F1 to F6 (closed in round 2) | MINOR | still CLOSED | My unchanged round-1 `plant.py`: 24 KILLED. Its 4 BADPLANT targets were rewritten in round 2; they are ported in `plant_r2.py` and KILLED there. The expected-pass control stays green. `plant_r435_titles.py`: 8 of 8 KILLED. `probe_edges.py` output is byte-identical to round 2 (`receipts/r1_probe_edges_rerun.txt`). |
| R434-1 S3, S4 | SUGGESTION | not adopted (carried) | As above. |

## Lens evidence

### Conformance

- **L4 against the clauses.** Checked against Milan v1.2 §5.3.3.4 and Annex C Table C.1, and IEEE 1722.1-2021 §7.2.6 Table 7-8, from the standards' own text:
  - offsets 82, 132 and 134;
  - formats at 136 or 138;
  - `redundant_streams` of 2·R octets, with R ≤ 8 in both tables.
  - Both layouts are identical below octet 136, so every other stream rule reads the same field in both. The format list is read through `formats_offset` (`model_rules.py:341-352`). Probes A1, A16 and A9 prove that the Annex C list is read at 136.
- **The N cap.** Table C.1 states N ≤ 47, but 136 + 8·47 = 512 is above §7.2's 508. The lint's 46 is therefore the binding bound in both layouts (A8 packs at 46).
- **Not linted.** The redundant-pair rules sit on 07 §3.1's "not linted" list, citing processor #69, as the ruling requires. A3 shows that a redundant output pair on two interfaces packs, so the redundancy path stays open.
- **L8 `identify-format`.** Its eight arms are unchanged and each is now pinned. The 0x3FFF mask follows §7.3.6.1's r/u flags.
- **Digest.** It matches §6.2.2.8 exactly, by the octet partition. `entity_id` and `entity_model_id` are excluded as well, and that is disclosed (`model_lint.py:33-35`).
- **Parent models**, at milan-fpga dev `cdf49d1a` and at PR #634 head `d81198c2`:
  - Setup: `parent-adoption-c4c6-ea3fb388.patch` then `parent-adoption-c8-cdf49d1a.patch`. At #634 the one `aem_assemble.py` hunk was ported by its identical one-line edit, as disclosed. gPTP is at its gitlink `5dce647a` (`receipts/parent_setup.txt`).
  - **Byte identity with round 2.** With the processor at `97f6eace` and at `9610098a`, `parent_pack_bytes.py` output is byte-identical at both parent heads. That covers the image sha256 with the lint on and off, the report sha256 and the digest (`receipts/parent_pack_bytes.txt`). My unchanged round-1 `parent_models_lint.py` output equals my R434-2 receipts line for line (`receipts/parent_models_lint_vs_r2.txt`).
  - **Results.** Four models pack with no waiver. `ax7101_8x8` packs only with its #584 waiver. Without the waiver it is refused on STREAM_PORT_INPUT 0..7, and with the waiver widened by one it is refused as stale.
  - The five dev digests equal the author's `pack-dev-97f6eac.txt`.
- Clean.

### RTL

- Round 3 touches no RTL, microcode or C++. The PR's only RTL change since `2ebd4fe8` is comment text in `KL_aecp_desc_store.sv`.
- `tb/desc_store` with pinned Verilator 5.050 (`receipts/tool_identity.txt`): rc 0. The gate (58 tests OK) runs first, then 584 checks, 584 PASS (`receipts/desc_store_make.log`).
- `./scripts/lint_hdl.sh` rc 0 (`receipts/lint_hdl.log`).
- `example_milan_8.json` packs to sha256 `20356f59…`, 1880 bytes, at main `2ebd4fe8` (old packer), at `9610098a` and at head with `--no-lint` (`receipts/example_image_and_loader.txt`).
- Clean.

### Robustness

- **The loader.** `_beside` raises `ImportError` naming the file when the spec or its loader is `None`. It binds itself as the module's `beside` before running it, so `model_lint.beside` and `model_rules.beside` are both `_beside` (`receipts/example_image_and_loader.txt`).
  - Removing the guard is KILLED (`S1-no-guard`), and so is restoring a private loader (`S1-own-loader`).
  - A direct load of `model_lint.py` fails with `NameError` (S1, a suggestion).
- **L4 on malformed input.** A short stream reads `tail` as 0 (`or 0`), and the length and offset arms then report findings, not exceptions. A huge R gives two findings (A17), not an exception.
- **Refusal paths.** I found every refusal statement in `model_rules.py` and `model_lint.py` by AST: each `ctx.bad`, each `raise ValueError`, and each append to `refusals`, `stale` or `problems`. That is 85 statements. Each was replaced alone by `pass`, and **85 of 85 are KILLED** (`receipts/refusal_statements.txt`). The author's count is 84, under a narrower classification. No statement survives.
- Clean.

### Tests

- **The gate:** 58 tests OK.
- **Suppression:** `lint_suppression.py` passes the control, and 56 of 56 checks are killed. `stream-layout` is killed by 9 mutations and `identify-format` by 8 (`receipts/lint_suppression.log`).
- **Plants run unchanged** (`receipts/plants_head_summary.txt`; 114 plants, 12 at a time):
  - R434-2 `plant_r2.py`: 37 of 37 KILLED;
  - `plant_r435_titles.py`: 8 of 8 KILLED;
  - R434-1 `plant.py`: 24 KILLED, plus the control and the 4 ported targets.
- **New plants:** `plant_r3.py`, 40 of 40 KILLED, each on the intended named test.
- **The scripts are the round-2 originals.** The 11 published round-1 and round-2 scripts are byte-identical to my R434-2 `MANIFEST.sha256` (`receipts/r2_scripts_unchanged.txt`).
- **The new tests are correct against the clauses:**
  - `FIXED_EXCLUSIONS` offsets match §7.2.6, §7.2.8, §7.2.9, §7.2.17, §7.2.18, §7.2.23 and §7.2.32;
  - the `VALUE_EXCLUSIONS` offsets match Tables 7-122 to 7-126;
  - the Annex C helper writes Table C.1's layout.
- Clean.

### Docs

- Each count the docs give matches what I measured:
  - 89 mutations;
  - 56 checks;
  - 58 tests;
  - `stream-layout` 9 and `identify-format` 8 under suppression;
  - 24 of 29 for the round-1 script, with its control and 4 ported targets;
  - 37/37 and 8/8 for the round-2 scripts.
- The L4 row, the "not linted" item, the §3.2 Δ note, REQ-MDL-003 and the `CHECKS` text agree with the code and the clauses. The F07.3 row and the Δ note still describe what this design's images carry, Table 7-8 with R = 0, which stays true.
- `make check` rc 0 (wavedrom 18, links 1050, matrix 115 REQ / 17 GAP, module matrix 94 rows / 0 untested, parameters 27). `gen_matrix.py --check` rc 0.
- `git diff --check` is clean over `9610098a..` and `2ebd4fe8..`.
- `git apply --check`: all 205 campaign patches apply (`receipts/campaign_patches_apply_check.txt`).
- The PR body's Round 3 claims are each reproduced above.
- Clean.

## Reviewer ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `model_rules.py` `_stream_layout`, `CHECKS`, `IDENTIFY_FORMAT`; `model_lint.py` `SPANS`, `VALUED`, `value_family`, `_current_spans` against Milan v1.2 §5.3.3.4 and Annex C Table C.1, and IEEE 1722.1-2021 §7.2.6 Table 7-8, §6.2.2.8 and Tables 7-122 to 7-126; `gen_ucode.py` E_RDESCSF; probes A0-A17, B, C, D (43 shapes), E; five parent models at dev `cdf49d1a` and #634 `d81198c2`, byte-identical to round 2 | R434-3 | 97f6eace064901f223e13abed7026f96bc4df805 |
| RTL | CLEAN | diff file list (no RTL in round 3; one comment-only `.sv` change in the PR); `tb/desc_store` 584/584 with pinned Verilator 5.050; `lint_hdl.sh`; `example_milan_8.json` image byte-identical to main `2ebd4fe8` | R434-3 | 97f6eace064901f223e13abed7026f96bc4df805 |
| Robustness | CLEAN (S1 suggestion) | `gen_desc_image._beside`, `model_lint` module head; L4 malformed-input paths; 85 refusal statements deleted one at a time | R434-3 | 97f6eace064901f223e13abed7026f96bc4df805 |
| Tests | CLEAN | `test_gen_desc_image.py` (58 tests), `lint_mutations.py` (89 mutations), `lint_suppression.py` (56/56); 114 unchanged reviewer plants plus 40 new, every applicable plant KILLED | R434-3 | 97f6eace064901f223e13abed7026f96bc4df805 |
| Docs | CLEAN | 07 §3.1 (L4 row, "not linted"), §3.2 Δ note and F07.3, 00 REQ-MDL-003, 09 §8.5, `tb/desc_store` README, the PR body Round 3 section; `make check`, `gen_matrix --check`, `git diff --check`, 205 campaign patches | R434-3 | 97f6eace064901f223e13abed7026f96bc4df805 |

## Real limits

- **Not run, by assignment:**
  - `run_suites.sh` (the full bank), the RTL mutation campaigns and the Yosys/builder banks;
  - the parent consumer set of 16, the donor bank of 9 and the parent builder test.
  - Instead I ran `tb/desc_store`, `lint_hdl.sh`, the docs gates, the campaign-patch apply check and my own model packing through the parent's builder path.
- **The parent CLI caller was not run.** My parent packing uses the builder path without `adp=`. The author's receipts cover the CLI caller and the driven ADP values.
- **Hosted CI at this head** (`receipts/hosted_checks_97f6eace.txt`): `docs-gates` and `portability` succeeded in both runs, 37042332246 and 37042326302. Both `suites` jobs were still in progress when I looked, so they are not evidence here.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Hosted/act acceptance of the exact head, including both `suites` jobs.
- The parent consumer set (16) and the donor bank (9) at this head, with `parent-adoption-c4c6-ea3fb388.patch` and then `parent-adoption-c8-cdf49d1a.patch`. At #634 the `aem_assemble.py` hunk needs its one-line port.
- The final current-dev candidate at the merge turn: source base `2ebd4fe8`, live dev `cdf49d1a`.

## Other reviewer's round-2 findings at this head

I read the R435-2 report (milan-fpga archive `ed074116`, `review-evidence/ppC8-r1/reviews/R435-2`) only after the verdict and ledger above were written. Its scripts match that report's `MANIFEST.sha256` and were run unchanged at this head.

| Finding | Original severity | Status at 97f6eace | Evidence |
|---|---|---|---|
| R435-2 F1 L4 refuses Annex C | MINOR | CLOSED | Its probes A1 and A2 (Annex C, R = 0) now PACK, and `r2_probes.py` reports 0 unexpected of 45 (`receipts/other_r2_probes_rerun.txt`).<br>That report's "keep refusing a redundancy tail" outcome was superseded by the round-3 ruling (#60 comment 5956187186). The ruling accepts the Annex C tail, and the lint does so, within Table C.1's R ≤ 8.<br>The Table 7-8 tail is refused, citing Milan §5.3.3.4's shall. The L4 row and REQ-MDL-003 are updated (see R434-2 F1 above). |
| R435-2 F2 identify-format arms, the array and MIXER digest arms | MINOR | CLOSED | `r2_plants.py`: 37 of 37 KILLED, 0 SURVIVED, 0 INVALID (`receipts/other_r2_plants_rerun.txt`; 27 at round 2). |
| R435-2 R1 the PR title said "L1 to L11" | RESIDUE | CLOSED | The title now reads "rules L1 to L12" (the manager's fix). |
| R435-2 S1 shared `None`-spec guard | SUGGESTION | ADOPTED | `gen_desc_image._beside` is the one loader (`test_one_guarded_loader`; plants `S1-no-guard` and `S1-own-loader` KILLED). |

The other report changes nothing in my verdict or ledger.

## Restore check

- The review clone is at `97f6eace064901f223e13abed7026f96bc4df805`, and `write-tree` equals tree `4ce73f7e28cded098788e23a7a056c976d9650aa`.
- `status --porcelain --ignored`, `diff-index HEAD` and `diff-files` are all empty.
- The index equals the HEAD tree in mode, blob and path for all 476 entries.
- The repository records no gitlinks (mode 160000: 0), so there are no submodule pins to verify (`receipts/restore_check.txt`).
- Every probe and plant ran in copies under `scratch/`, which is not published.

R434-3 FINISHED
