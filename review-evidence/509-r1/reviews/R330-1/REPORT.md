[R330] NEGATIVE - exact head 20423082f221a02f3de72952cec4e1ac0c839b1d

Round R330-1, internal independent review of issue #509 / PR #568.
Head `20423082f221a02f3de72952cec4e1ac0c839b1d`, tree `48c142d96a9a0333f921073e848ed2bbabf5e43c`,
base `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, processor pin `990f96526bb89356c963a260ebbdcf2a77e6623a`.
All five lenses applied. Three MINOR findings are open, so Conformance, Tests and Docs are not clean
and the verdict is NEGATIVE. RTL and Robustness are covered clean at this head. No BLOCKER or MAJOR.

Reconstruction order: AGENTS.md, CONTRIBUTING.md (sections 5 and 6, Rule 12 in
docs/development/CODE_QUALITY.md), docs/README.md, the #509 body, assignment/decision comment
5844867005, TAKEN and REVIEW READY comments, processor `docs/architecture/07_memory_maps.md`
section 3.1 at the pin, processor issues 38/39/60/82/89 and parent #464/#478/#495 (states and
bodies), then the diff `7eb3b0d4..20423082` (one commit, four files), then the public evidence
tree `ce614404:review-evidence/509-r1`. There were no prior public review findings on PR #568
(only the two review-start notices), so nothing needed to be resolved or retained.

## Findings

### R330-1-M1 MINOR - Tests - scripts/audit_pp_descriptors.py:306-325 (with :343-349) - the identity probe cannot observe the fix it is evidence for
- Authority/evidence: #509 acceptance 3. AGENTS.md section 6 Tests ("Each new test can fail for
  the defect it claims to detect"; "Tests do not merely reproduce implementation assumptions").
  `main()` loads the arty_4x4 config (so `model_shape()` and `derive_model_id()` have already run)
  before `identity_probe()` patches `assemble.d_control_identify`. The probe then compares
  `cfg["entity"]["entity_model_id"]` and the ENTITY bytes that are generated from that pre-resolved
  config. The model ID therefore cannot move, whatever `model_shape()` covers.
  Reviewer mutation M3 (`receipts/mutation-probes.json`, `receipts/m3-fresh-process.json`) simulates
  a #495-style repair: `model_shape()` also hashes the IDENTIFY CONTROL bytes. A fresh-process CLI run
  with the same on-disk reset_time edit then changes the ID, from `0x001BC5F531E6A9DA` to
  `0x001BC572445BE3EA` (image offsets 303-307 and 6741 differ). The committed audit still reports
  "offset 6741 changed, model ID unchanged" (`0x001BC5F531E6A9DA` both sides).
- The claim itself is true at this head. The reviewer reproduced it by a different route: an on-disk
  edit of `avdecc/aem_descriptors.py` in a disposable copy, then all three CLIs in fresh processes.
  The result was byte 6741 changed, ID `0x001BC557FC6ABBC8` unchanged, and after-image SHA-256
  `bb036e26...0562`, identical to the page (`receipts/cli-identity-probe.json`).
- Impact: the page's Reproduction section offers this script as the way to regenerate the evidence.
  After #495 or processor 38 is repaired in the natural way, the script would keep reporting that the
  residue reproduces. That result would be false.
- Required outcome: the identity probe re-derives the model identity with the generator change in
  force. For example, it could load the config inside the patch context or run a fresh process on a
  mutated copy. A repaired builder must then produce a changed ID.
- Verification: rerun M3 (`scripts/mutation_probes.py`) against the corrected script. The audit's
  identity probe must report a changed model ID under M3, and the unchanged result at the pristine head
  must remain.

### R330-1-M2 MINOR - Conformance, Docs - docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:59 and :237 - a newly measured processor-owned gap (body type/index vs directory key) has no bounded follow-up
- Authority/evidence: decision 5844867005 says "The processor keeps ... descriptor type/index
  consistency". #509 acceptance 4 requires a bounded follow-up with evidence for newly established
  defects, and forbids silently expanding existing criteria. The audit's own packer probes ("wire index
  differs from metadata", "wire type differs from metadata") are both `accepted`. This was reproduced
  in `receipts/audit-run1.json` and confirmed against `gen_desc_image.py:199-225,327-337`, which
  never read the body's type/index. The page routes this to processor 60 as "Generic gap remains [PP60]"
  (:59) and "Generic metadata/body consistency remains processor-owned" (:237). Processor 60's
  published missing checks and acceptance (L1-L8 semantic lint; negative models for L3-L8; tests for
  the existing refusals) never name body/key consistency. The required-evidence cell at :237 names no
  mismatched type/index fixture either. The author handoff wording for the processor contract also
  states the gap explicitly.
- Impact: processor 60 can close against its published acceptance with this gap still in the packer.
  That leaves a decision-assigned generic check without an execution contract. The alternative is
  silently widening processor 60's criteria.
- Required outcome: add a bounded record for maintainer filing, for example F7: the processor packer
  refuses a body whose type or index disagrees with its directory key. It needs a legal control plus
  independent refusals of a mismatched type and a mismatched index. Alternatively, record a public
  owner decision that adds this to processor 60 explicitly. Correct the :59 and :237 wording to match.
- Verification: the page names the record and its discriminating evidence; the receipt still shows
  both probes accepted at the pin.

### R330-1-M3 MINOR - Conformance, Docs - docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:139-142 and :64 - six static-map deviations in the shipping arty_current image are disclosed with only a closed issue as owner, and the L7 row overstates the parent bound
- Authority/evidence: the #509 "Validation and readiness" expected result says "no unowned rule ...
  every discovered gap linked to its execution contract". The decoded arty_current image
  (`receipts/audit-summary.txt`, arty_current section) has AUDIO_MAP[0] mapping stream channels 0..7
  of STREAM_OUTPUT[0], and that stream advertises only `0x0205022000806000` (2 channels). These are the
  six `KNOWN_MAP_DEVIATIONS` (`avdecc/aem_maps.py:107-112`). `avdecc/aem_maps.py:233-241` records
  this bound and does not raise it ("the fix is a product decision owned elsewhere"). The same holds
  for any configuration, because only the self-test calls `assert_no_map_deviations`
  (`avdecc/gen_aem_store.py:302,316`). The page links only #464, which is closed and repaired fixture
  indices, and says they "do not become resolved through this ownership audit". It names no live
  owner. The #464 thread refers to a separate "existing product-policy owner" but does not identify
  it. The L7 matrix row (:64) says "Parent checks map bounds before packing" without noting that
  stream-channel width is recorded, not refused.
- Impact: a known gap in a shipping image is left without a traceable execution contract, and the L7
  row reads as a stronger bound than the builder enforces.
- Required outcome: link the live owner of the six deviations, or add a bounded follow-up record for
  maintainer filing. State that the arty_current shipping image carries them. Qualify the L7 row's
  "map bounds" claim for stream-channel width.
- Verification: the page names an open issue or new record, and the L7 row matches
  `aem_maps.py:233-241`. `gen_aem_store.py --self-test` still reports the same six deviations
  (`receipts/gen_aem_store_selftest.log`).

### Suggestions (optional, do not affect coverage)
- S1 (Tests): the audit records outcomes but asserts none of the page's expected results. An optional
  `--check` against the stated probe outcomes would catch drift between the page and the tree.
- S2 (Robustness): `packed_rows`, `generate` and `assert_packed_bytes` use `assert` for input
  validation, which `python3 -O` removes. Explicit exceptions would keep the decoder strict.
- S3 (Docs): the probe table at :150-165 omits the packer probes "CLASS_A cleared", "current format
  outside list" and "mixed AAF and CRF formats", which are all accepted and present in the receipt. It
  could list them next to the L4 row.

## Per-lens results (clean lenses in finding format)

[R330] PASS RTL - hdl/common/csr/milan_csr.sv:1582,:1751,:2816; hdl/milan/milan_datapath.sv:2462,:7520; hdl/milan/KL_pp_shadow.sv:258; protocol-processor hdl/adp/KL_adp_engine.sv:117,:871 at 990f9652; diff stat 7eb3b0d4..20423082 - The diff changes no RTL, HDL source list or pin (four files: two docs pages, the README row and one script). The only RTL claim, L8 (ADP_IDX0 resets to zero, and its upper half drives `identify_index_i` through `o_adp_identify_index` and `cfg_adp_identify_index`), matches the source. The submodule gitlinks are unchanged. There was no RTL to simulate, so the scoped simulator was not used.

[R330] PASS Robustness - scripts/audit_pp_descriptors.py:34-38,120-127,167-179,239-284; receipts/mutation-probes.json (M1, M2); receipts/control-relocation.txt; receipts/probe-reach.txt; receipts/audit-clean.json - The boundary pairs are present and discriminate: 2126000/2125999 ns, 47/48 formats (sizes 514/522), 8/9 rates, and 576/577-byte rows. M1 (the packer normalizes the last body byte) makes the audit fail at `assert_packed_bytes`, so "accepted" is never reported for normalized bytes. M2 (a planted L10 offset refusal) flips only "offset 143" to refused. The relocated-YAML control decodes identically to the tracked arty_current image (32 rows). Every accepted YAML mutation is visible in its packed rows (buffer 2125999, CRF word BB81, 48 formats/length 522, mixed list, CLOCK_DOMAIN `[0]` with CRF only, zero and all-ones IDs). A clean clone at the head reproduces the receipt byte-for-byte, and `-B` leaves no residue.

[R330] UNCLEAN Conformance - R330-1-M2, R330-1-M3. Everything else examined under this lens held; the evidence is listed below.

[R330] UNCLEAN Tests - R330-1-M1.

[R330] UNCLEAN Docs - R330-1-M2, R330-1-M3.

### Conformance evidence (what held)
- Matrix spot-check, all 11 rows (more than the 10 required), against source at parent 7eb3b0d4 (same
  content at head) and processor 990f9652. Each cited path exists and does what the row says:
  - L1: `aem_assemble._entity_descriptors`/`_port_descriptors`, `cluster_layout`, gate 6.
  - L2: `gen_desc_image._grouped_descriptors` duplicate refusal and `_index_entries` density refusal
    (reproduced), plus `two_level_directory`/`check_two_level`.
  - L3: `_streams` "needs at least one {direction} stream" (:1370), `base_format_complete`, gate 29.
  - L4: `d_stream` Table 7-8 layout, flags 0x0003/0x0002, current = formats[0].
  - L5: gate 37 port_number.
  - L6: `_overlay_clock_sources`, `d_clock_domain` identity list, `_load_clocking` :3858/:3868, and
    gate 33 retired-source arms.
  - L7: `_streams` static-map refusal (:1431), `_map_duplicate_rule`, `d_audio_cluster`.
  - L8: `d_control_identify` and the CSR wiring (see RTL).
  - L9: `model_shape` and `derive_model_id`, pin > hash > literal with `_eui64` width check only
    (:4299-4320); gate 8 and gate 28, whose identity loop covers four configurations (:25366).
  - L10: loader bound and duplicates (:3833/:3836), gate 36a checks offset/count/words only
    (:27213), `spec_from_overlay` 48/96/192 restriction.
  - ADP: `adp_shape`, `check_entity_shape.py`.
  - Construction (C), refusal (R) and test comparison (T) are labeled consistently with the source.
- Five configurations: the audit rerun is byte-identical to the author's receipt (sha256 `8233f515...4779`).
  The decoded counts, sizes, AUDIO_UNIT/CLOCK_DOMAIN image offsets, rate and source lists,
  per-class lengths, flags, formats, CRF location indices 1/4/4/1/8, ADP and ENTITY capabilities and
  model IDs all match page tables :88-132. All 15 generator CLI invocations reproduce the five
  image hashes (`receipts/cli-identity-probe.json`).
- The probes do what the page claims. There are 30 packer, 13 YAML and 2 map probes, and each
  refusal cause, boundary and "accepted invalid" row at :150-180 matches the receipt.
- Identity reconciliation: reproduced independently (see R330-1-M1 for the instrument weakness only).
- F1-F6 are real (each has a reproducing probe or decode), bounded, and distinct from #478 (closed,
  loader bound only), #464 (closed, self-test), #495 (evolution, gate-28 coverage and snapshot
  items), processor 38/39/60/82/89 and #76. None is silently fixed: no validator, config, pin or
  generated byte changed. F5 correctly asks for a clause-backed decision on processor F07.2 `1..*`
  against the decoded 8x8 zero-cluster input ports.
- The proposed processor contract wording (published handoff, "Processor contract wording") is
  consistent with decision 5844867005. It covers the processor's generic extents, directory,
  density, name binding, line buffer and type/index duties, and the parent's authoritative identity,
  L10 offset/count/length, clock-source shape and ADP maxima, with processor semantic checks as
  defence in depth. It explicitly states the unimplemented type/index comparison.

### Docs evidence (what held)
- `docs/ENDSTATION_BUILDER.md` corrections match the decode and the configs: tdm8 physical 8/8
  (config capture 8, render 8), AUDIO_CLUSTER 25, arty_current AUDIO_MAP 1 (also at :1054), 8x8
  image 18,288 B. The identity paragraph correctly withdraws "verify the pin". No pin verification
  exists (`endstation_builder.py:4306-4308`).
- `docs/README.md` row added. Gates at the head, run in a clean clone with the hash-pinned Markdown
  lock, all exit 0 (`receipts/gate_*.log`): docs_check with git and without git (inventory-parity
  skip as expected), check_em_dash `--base 7eb3b0d4` (0 findings over 309 added lines), gen_toc
  `--check` and `--verify-anchors`, check_doc_style and check_doc_paths. `git diff --check 7eb3b0d4`
  is clean.
- Python idiom and privacy: `check_py_idiom.py` exit 0 with all six refusals at 0 and every ratchet at
  budget. The script has full signatures and docstrings, uses `Path`, runs no shell, and contains no
  host paths or bench identifiers (docs_check scrub, 886 files).

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (M2, M3) | #509 body and decision; processor 07 section 3.1 at 990f9652; all 11 matrix rows vs source; audit/CLI receipts; follow-up issue scopes | R330-1 | 20423082f221a02f3de72952cec4e1ac0c839b1d |
| RTL | CLEAN | milan_csr.sv:1582/1751/2816; milan_datapath.sv:2462/7520; KL_pp_shadow.sv:258; processor KL_adp_engine.sv:117/871; diff stat (no RTL) | R330-1 | 20423082f221a02f3de72952cec4e1ac0c839b1d |
| Robustness | CLEAN | audit_pp_descriptors.py boundaries and error paths; mutation M1/M2; relocation control; clean-clone rerun | R330-1 | 20423082f221a02f3de72952cec4e1ac0c839b1d |
| Tests | UNCLEAN (M1) | audit_pp_descriptors.py identity/packer/config/map probes; mutation M1-M3; gen_aem_store --self-test (20 ok, six deviations) | R330-1 | 20423082f221a02f3de72952cec4e1ac0c839b1d |
| Docs | UNCLEAN (M2, M3) | PP_DESCRIPTOR_OWNERSHIP.md; ENDSTATION_BUILDER.md diff; docs/README.md; docs gates; py idiom gate | R330-1 | 20423082f221a02f3de72952cec4e1ac0c839b1d |

## Real limits
- The review did not run the full builder bank, entity-shape self-test, NVM, behave, xvlog, RTL lint
  or other author and manager banks. It relies on the manager's public source evidence for those.
  Only the generator self-test, audit, CLIs, docs gates and Python idiom gate were rerun.
- Milan/IEEE clause text was not read from the standards themselves. Rule content was judged against
  processor 07 section 3.1 and in-tree clause citations.
- Hosted checks were only a snapshot at 2026-09-26T10:03:32Z (`receipts/hosted-snapshot.txt`). Some
  Verilator shards, docs-check and elaborate were in progress and rtl-fast was queued. The snapshot is
  not acceptance evidence.
- No hardware and no physical calibration. Multi-configuration behavior cannot be measured, because
  every tracked image has one configuration (the page claims none).

## Pending manager duties
- Hosted and act acceptance at the exact head, and final current-dev candidate build and validation at
  the merge turn.
- External review R331. Re-review of fixes for M1-M3 at a new head, which un-covers Conformance,
  Tests and Docs for that head.
- Filing F1-F6 (and any record added for M2/M3) after acceptance. The processor contract change
  follows separately.

## Receipt restoration
The review clone was verified after all probes: HEAD, tree, index and worktree have no diff, the
index-stage hash equals the HEAD-tree hash, all four gitlinks are unchanged, and there are no
untracked or ignored entries. The interpreter caches created by the first audit run were removed
(`receipts/head-verification.txt`). All mutations ran in disposable copies under scratch.

R330-1 FINISHED
