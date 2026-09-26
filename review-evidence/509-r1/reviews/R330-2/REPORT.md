[R330] POSITIVE - exact head 04c9802d852befba3b5d854ba5f3faf3ddfc59a7

Round R330-2, internal independent delta review of issue #509 / PR #568.
Head `04c9802d852befba3b5d854ba5f3faf3ddfc59a7`, tree `12680eef320eebd3602e062e6c7fcda9d192a31a`,
parent `20423082f221a02f3de72952cec4e1ac0c839b1d` (covered in full by R330-1), source base
`7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, processor pin `990f96526bb89356c963a260ebbdcf2a77e6623a`.
All five lenses were applied at this head. No BLOCKER, MAJOR or MINOR is open. R330-1 M1, M2 and M3
are resolved, and round-2 items 4 and 5 (from the external round's S1 and S2) are verified. Two new
SUGGESTIONs are recorded; neither affects coverage.

Reconstruction order: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #509 body, decision comment
5844867005, round-2 assignment 5845357621 (items 1-5), the [A333] REVIEW READY comment 5845571616,
processor `docs/architecture/07_memory_maps.md` section 3.1 (L6 row, line 88) at the pin, then
`git diff 20423082..04c9802d` (one commit, two files: `scripts/audit_pp_descriptors.py` +42/-12 and
`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` +13/-6), then the full `7eb3b0d4..04c9802d` stat (same
four files as round 1, no gitlink change). After that came the public evidence tree
`1f789d8e:review-evidence/509-r1` (author-r2 manifest, `gates.jsonl`, `final-state.json`;
`receipts/public-evidence-hashes.txt`). The author-r2 audit receipts carry the same sha256 as this
round's. The external round's report was not read before this verdict and ledger were fixed. Its
findings are resolved in the last findings section, which was written afterwards.

## R330-1 findings: disposition at this head

### R330-1-M1 (Tests) - RESOLVED
- Change: `identity_probe()` now reloads the config inside the patch
  (`scripts/audit_pp_descriptors.py:331-333`). It patches both the descriptor module and the
  assembler binding. `check_identity_probe()` (:343-354) plants a model_shape that also hashes the
  IDENTIFY bytes and raises `AuditError` unless the packed model ID then changes. `main()` runs it
  before the report (:374).
- Round-1 probes rerun unchanged (script hashes identical to the R330-1 manifest). M3, the simulated
  #495-style repair, now makes the audit's own identity probe report `0x001BC5F531E6A9DA` ->
  `0x001BC572445BE3EA`, with changed offsets 303-307 and 6741 and before/after image SHA-256 `8b6cbc46...`
  / `8f363c56...` (`receipts/m3-audit-identity.json`). A fresh-process CLI regeneration of the same M3
  tree produces exactly those IDs, offsets and hashes. Its receipt is byte-identical to R330-1's
  (`receipts/m3-fresh-process.json`, sha256 `e9a35626...80c7`). The in-process probe and the
  fresh-process route now agree.
- The unchanged result at the pristine head is kept. `receipts/audit-run1.json` is byte-identical to
  the R330-1 receipt (sha256 `8233f515...4779`), and its identity probe still reports byte 6741 changed
  with `0x001BC557FC6ABBC8` on both sides. The on-disk reset_time route through all three CLIs again
  gives after-image `bb036e26...0562` with the ID unchanged, and all five CLI image hashes match
  (`receipts/cli-identity-probe.json`).
- The control discriminates (`scripts/round2_mutants.py`, `receipts/round2-mutants.json`):
  - K1 reverts to the round-1 defect (`after` generated from the pre-loaded config). The audit
    refuses with `AuditError: identity probe missed changed generator bytes in model identity`, rc 1,
    both normally and under `-O`.
  - K2 makes the control's derivation ignore the changed field. The audit refuses with rc 1.
  - K3 drops the descriptor-module patch. The audit refuses with rc 1.

### R330-1-M2 (Conformance, Docs) - RESOLVED
- The L2 row (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:59`) now says "Body/key consistency needs F7;
  PP60 retains its published scope". The debt row (:244) says "Generic metadata/body consistency is
  allocated separately to F7". F7 (:242) is bounded: refuse descriptor body type/index disagreement
  with the directory key, separate from PP60's published acceptance. Its evidence is a legal pair plus
  independent refusals of a mismatched body type and a mismatched body index. This matches decision
  5844867005 ("the processor keeps ... descriptor type/index consistency") and does not widen PP60.
- The claim "both invalid probes currently pack unchanged" holds. The receipt has "wire index differs
  from metadata" and "wire type differs from metadata" both `accepted`, after `assert_packed_bytes`
  proved the packed bytes equal the document (:178-192). The pin is unchanged.

### R330-1-M3 (Conformance, Docs) - RESOLVED
- :139-143 now say "The shipping `arty_current` image retains six static-map coherence deviations" and
  "F8 owns their remaining product-policy disposition". F8 (:243) is a bounded parent record. It asks
  for a clause-backed policy with image validation and model changes, and its evidence is to decode
  AUDIO_MAP[0] channels 0..7 against stereo STREAM_OUTPUT[0], keep a legal in-range control, detect
  each channel 2..7 deviation, and use positive/negative fixtures. #464 stays closed.
- Verified at the head: the decoded arty_current AUDIO_MAP[0] maps stream channels 0..7 of stream 0.
  STREAM_OUTPUT[0] advertises only `0x0205022000806000` (`receipts/audit-run1.json`).
  `gen_aem_store.py --self-test` reports "the 6 open stream_channel deviation(s) are exactly the
  recorded ones", 20 ok, PASS, and is otherwise identical to R330-1
  (`receipts/gen_aem_store_selftest.log`).
- The L7 row (:64) now reads "Parent checks map indices and cluster bounds before packing. Stream-channel
  width deviations are recorded, not refused (`M._map_row_bounds`)". That matches
  `avdecc/aem_maps.py:179-241`: cluster_offset, cluster_channel and stream_index raise `ValueError`, and
  the width bound returns a deviation string (:233-241).
- The live owner is the F8 record under open #509 until the maintainer files it. The page says so
  (:230-232), and the round-1 required outcome allowed this form. PR #568 carries `Closes #509`, so F7
  and F8 must be filed before or at that closure (see Pending manager duties).

### Round-2 items 4 and 5 (from the external round's S1 and S2) - VERIFIED
- Item 4. `grep assert scripts/audit_pp_descriptors.py` matches only the function name
  `assert_packed_bytes`; no `assert` statement remains. The seven integrity checks are explicit
  `raise AuditError` (:49, 51, 53, 66, 68, 137, 190). `AuditError` derives from `RuntimeError`
  (:35), so none of the measured-outcome handlers (`ImageError`, `ConfigError`, `ValueError`,
  :237/246/287/294/314) can swallow it and record it as a "refused" probe.
  - `scripts/integrity_refusals.py` feeds tampered arty_current images to `packed_rows()`. Magic,
    version, trailing byte, header checksum, body type, body index and row-beyond-image each raise
    `AuditError`, and the pristine image decodes. The results are identical under normal and `-O`
    Python (`receipts/integrity-normal.json`, `receipts/integrity-optimized.json`).
  - R330-1 M1 (the packer normalizes the last byte) now fails under `-O` with
    `AuditError: packer changed descriptor bytes` (K5).
  - The whole audit under `-O` is byte-identical to the normal receipt (`receipts/audit-optimized.json`).
- Item 5. The L6 row (:63) now enumerates all five processor sub-rules from
  `protocol-processor/docs/architecture/07_memory_maps.md:88` at the pin:
  - one INPUT_STREAM per CRF input, or the sole AAF input without CRF;
  - INTERNAL with outputs;
  - at least one source per domain;
  - the identity list;
  - the restricted gPTP chain.

  Its new measured claims hold (`scripts/l6_empty_sources.py`, `receipts/l6-empty-sources.json`):
  - An empty `media_clock_sources` fails with `IndexError`, with or without `default_source`. The
    cause is `clk.get("default_source", srcs[0])` in `sw/builder/endstation_builder.py:3805`.
  - A `gptp` source is refused as unknown, because the loader admits only internal/crf (:3802-3804).
    The gPTP arm is therefore unreachable, as stated.

## New findings

### R330-2-S1 SUGGESTION - Tests - scripts/audit_pp_descriptors.py:319-354 - the identity evidence does not refuse a vacuous probe
- Evidence: K4 (`receipts/round2-mutants.json`) patches only the descriptor module, so the planted
  reset_time change never reaches the packed image. The control still passes, because it reads the
  descriptor module. The audit exits 0 and reports `changed_image_offsets: []` with the ID unchanged.
  Only a reader comparing the receipt with the page's "byte 6741 changes" would notice.
- Impact: a refactor of how the assembler binds `d_control_identify` could make the "ID unchanged"
  half of the evidence vacuous without a refusal. A rename is safe, because `patch.object` fails
  loudly on a missing attribute.
- Optional outcome: also raise `AuditError` when the probe's image does not change.

### R330-2-S2 SUGGESTION - Robustness - scripts/audit_pp_descriptors.py:291-295 - a decoder truncation inside a config probe would be recorded as a model refusal
- Evidence: `packed_rows(blob)` runs inside the `try` that catches `ValueError`. `uint()` (:41-42)
  raises `ValueError` when the decoder itself reads outside a descriptor, so such an evidence
  failure would appear as `image: refused`. This is latent. The only image refusal in the receipt
  ("eight distinct rates") carries the generator's own "unsupported sampling rates" reason.
- The code is unchanged from 20423082, and this is adjacent to item 4. Optional outcome: decode
  outside the `try`, or raise `AuditError` from `uint()`.

Retained optional suggestion from R330-1: S3, the probe table omits three accepted packer probes. It
is unaddressed; the assignment routes non-adopted suggestions to #495. It does not affect coverage.

## Per-lens results (clean lenses in finding format)

[R330] PASS Conformance - docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:59,63,64,139-143,209-214,228-248; protocol-processor docs/architecture/07_memory_maps.md:88 at 990f9652; avdecc/aem_maps.py:107-112,179-241; sw/builder/endstation_builder.py:3788-3807; receipts/audit-run1.json, l6-empty-sources.json, gen_aem_store_selftest.log - Checked the delta's rule and ownership claims against the processor L6 clause, decision 5844867005 and #509 acceptance 4 and its readiness clause ("every discovered gap linked to its execution contract"). F7 and F8 are bounded and discriminating. The L2, L6 and L7 rows match the source and the measured outcomes. Matrix rows L1, L3-L5 and L8-L10 and the five-configuration tables are unchanged from R330-1 and reproduce byte-identically (audit sha256 8233f515...4779, five CLI image hashes).

[R330] PASS RTL - git diff --stat/--raw 7eb3b0d4..04c9802d (four files: two docs pages, the README row, one script; zero 160000 entries); hdl/common/csr/milan_csr.sv:315-316,1308; hdl/milan/milan_datapath.sv:2462,7520 - The delta changes no RTL, HDL list or pin. The L8 CSR claim (ADP_IDX0[31:16] drives identify_index_i) still matches the source. There was no RTL to simulate, so the scoped simulator was not used.

[R330] PASS Robustness - scripts/audit_pp_descriptors.py:35,46-73,131-138,178-192,319-354; receipts/integrity-normal.json, integrity-optimized.json, audit-optimized.json, mutation-probes.json, round2-mutants.json (K1-O, K5), probe-reach.txt - Tampered images are refused by explicit exceptions with or without optimization. R330-1 M1 and M2 keep their outcomes: M1 now fails via AuditError, and M2 flips only "offset 143". The accepted-probe reach check is identical to R330-1. `-B` runs leave the clean clone without residue. S2 is optional.

[R330] PASS Tests - scripts/audit_pp_descriptors.py:319-354,374; receipts/mutation-probes.json (M3), m3-audit-identity.json, m3-fresh-process.json, cli-identity-probe.json, round2-mutants.json (K1-K4) - The identity probe observes a simulated identity-coverage repair exactly as the fresh-process CLI does. The control fails for a stale config, for a derivation that ignores the field and for a missing module patch. The pristine outcome is retained. The generator self-test passes with the six recorded deviations. S1 is optional.

[R330] PASS Docs - docs/reference/PP_DESCRIPTOR_OWNERSHIP.md (delta :59,63,64,139-143,209-214,229,242-244); receipts/gate_docs_check.log, gate_docs_check_nogit.log, gate_em_dash.log (--base 7eb3b0d4, 316 added lines, 0 findings), gate_toc_check.log, gate_toc_anchors.log, gate_doc_style.log, gate_doc_paths.log, gate_py_idiom.log; `git diff --check 7eb3b0d4` clean - The page's new identity text (reload, control, refusal, optimized Python) describes the code exactly. The F7/F8 anchors resolve. Every docs gate exits 0 from a clean clone with the hash-pinned renderer, and the no-git mode skips only inventory parity. The idiom gate is at budget, with all refusals at 0.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ownership page L2/L6/L7/F7/F8/identity text; processor 07 section 3.1 L6 at 990f9652; aem_maps.py bounds; loader clocking; audit and self-test receipts | R330-2 | 04c9802d852befba3b5d854ba5f3faf3ddfc59a7 |
| RTL | CLEAN | full diff stat and raw (no RTL, no gitlink); milan_csr.sv:315-316/1308; milan_datapath.sv:2462/7520 | R330-2 | 04c9802d852befba3b5d854ba5f3faf3ddfc59a7 |
| Robustness | CLEAN | audit integrity refusals under normal and -O; tampered-image probe; M1/M2/K5; reach check | R330-2 | 04c9802d852befba3b5d854ba5f3faf3ddfc59a7 |
| Tests | CLEAN | identity probe and control; M3 vs fresh-process CLI; K1-K4; CLI hashes; generator self-test | R330-2 | 04c9802d852befba3b5d854ba5f3faf3ddfc59a7 |
| Docs | CLEAN | ownership page delta; docs_check (git and no-git), em-dash, TOC, anchors, doc style, doc paths, py idiom; diff --check | R330-2 | 04c9802d852befba3b5d854ba5f3faf3ddfc59a7 |

All rows are at the merge candidate head itself, so no ancestor-coverage argument is needed. The
ledger is reviewer-published.

## Real limits
- Not run by this reviewer: the full builder bank, entity-shape self-test, NVM, behave, xvlog, RTL
  lint, and the parent/PP/gPTP/Yosys banks. These rely on the manager's public evidence at this head.
  `author-r2/gates.jsonl` lists 30 gates with exit 0; `final-state.json` records head 04c9802d and a
  clean worktree. Only the audit (normal and -O), the three generator CLIs, the generator self-test,
  the docs gates and the Python idiom gate were rerun here.
- Milan and IEEE clause text was not read from the standards. The rule content was judged against
  processor 07 section 3.1 at the pin and the in-tree clause citations.
- Hosted checks were only a snapshot at 2026-09-26T10:55:45Z (`receipts/hosted-snapshot.txt`).
  - Completed with success: bdd-conformance, changes, docs-check-no-git, elaborate, full-ci-gate,
    verilator-lint, wire-accountability and Yosys shards 0-3.
  - Still in progress: docs-check, Verilator shards 0-4 and yosys-elaboration.
  - Skipped: "Physical gPTP (nightly and manual)". The skip is not hardware proof.

  This snapshot is not acceptance evidence.
- No hardware and no physical calibration. Multi-configuration behavior remains unmeasured, because
  every tracked image has one configuration.
- The py idiom gate needs initialized submodules. It was run read-only with `-B` in the review clone,
  and the clone was reverified afterwards. Every other probe ran in disposable copies under scratch.

## Pending manager duties
- Hosted and act acceptance at the exact head. The final current-dev candidate build and validation at
  the merge turn (source base and live dev are both 7eb3b0d4 at assignment).
- File F1-F8 as public issues. F7 is processor-side and F8 is the parent static-map policy. Because
  PR #568 says `Closes #509`, and the page names #509 as the owner "until filing", this must happen
  before or at that closure. Otherwise F7 and F8 fall back to a closed owner, which is the state M3
  objected to.
- The external review position (R331-1 POSITIVE at ancestor 20423082 per assignment 5845357621)
  and its acceptance for the delta are the manager's determination.

## Prior public review findings (read after the verdict and ledger above were fixed)

R330-1 M1-M3 are resolved above. The external round R331-1 (comment 5845356060, POSITIVE at
20423082) published five SUGGESTIONs and nothing that is MINOR or above:
- **R331-1-S1** (the audit's integrity checks were `assert`s). RESOLVED at this head. No `assert`
  statement remains. The planted normalizing-packer mutant (K5) fails under `-O`, and the tampered
  images are refused under `-O` (see item 4 above).
- **R331-1-S2** (the L6 row did not name the processor sub-rules). RESOLVED. :63 names all five
  sub-rules and records the dispositions (see item 5 above).
- **R331-1-S3** (an empty `media_clock_sources` raises `IndexError`, not `ConfigError`). RETAINED as
  a SUGGESTION. It is pre-existing and outside the diff. The page now discloses it accurately at :63,
  and this round reproduced it (`receipts/l6-empty-sources.json`). No follow-up record names it; the
  failure is closed and no image is produced. The maintainer may file it next to F4.
- **R331-1-S4** (the processor wording does not state the PP60 authority split). RETAINED as a
  SUGGESTION for the separate processor contract change. It is outside this delta.
- **R331-1-S5** (`docs/ENDSTATION_BUILDER.md:262`, `:992` contradict the corrected map census). RETAINED
  as a SUGGESTION. It is pre-existing and outside the delta, and assignment 5845357621 routes it to #495.

None of these changes the verdict or the ledger above.

## Receipt restoration
After all probes, the review clone was verified (`receipts/head-verification.txt`):
- HEAD is 04c9802d and the tree is 12680eef.
- Worktree and index show no diff against HEAD.
- The index-stage hash equals the HEAD-tree hash (`2ef7aee9...41bc`).
- All four gitlinks are unchanged, and the processor HEAD is 990f9652.
- There are zero untracked or ignored entries in the parent and in the processor.

All mutants ran in disposable copies under scratch.

R330-2 FINISHED
