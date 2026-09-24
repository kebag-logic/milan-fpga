[R275] POSITIVE - exact head 8b7be584da62657f9767ad07e294d278144869c5

Round R275-3. This is the composition review for issue #511 / PR #537 (Closes #511; Relates to #394 and #510). It covers only whether the merge-train candidate is acceptable as composed.

- Candidate `8b7be584da62657f9767ad07e294d278144869c5`, tree `4420741a4517de5189ae8f5d330db488a63eba91`.
- The candidate's parents are `70da0bcdf7896b26efb4cc3f854c17a02f2c4126` (the queued predecessor candidate: dev `50e78097`, then the issue 117 merge, then the issue 387 merge) and the PR source head `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6`.
- The PR source's base is `759da623072358afdb0e9d570a7b4b6a788492c9`, which is merge-base(parent, source).
- `git merge-tree --write-tree 70da0bcd 70f2c50d` reproduces tree `4420741a…` exactly, with exit 0. The candidate is therefore the clean automatic merge, and no resolution work was added.

## Verdict

**POSITIVE.** The composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR, MINOR or SUGGESTION is raised. All five lenses were applied to the composition, and each is covered clean at the exact head.

The PR source head already has two independent POSITIVE source reviews: R274-2 and R275-2, both at `70f2c50d`. This round does not repeat their standards-text verification. The composition does not change any clause claim's wording (see Conformance).

## Reconstruction order

1. I read AGENTS.md, CONTRIBUTING.md (Sections 2.1 and 3, candidate-merge validation, and the documentation and em-dash rules) and docs/README.md.
2. I read the bodies of #394, #510 and #511 and their public comments. These include the three 2026-09-23 owner decisions (#394 comment 5789765478, #510 comment 5789766089, #511 comment 5789766257), the manager's assignments, and the executor REVIEW READY comments (A215, then A226).
3. I read the linked authorities: REQUIREMENTS.md (REQ-PTP-06/09), FR_NFR.md, the compliance matrix, the feature-status ledger, SUBMODULES.md and the 802.1AS traceability page.
4. I read `git diff 70da0bcd..8b7be584` and its history, and compared it against the source diff `759da623..70f2c50d`.
5. From the public evidence tree at `9c71d05f` (`review-evidence/394_510_511-r1`), I read only the `author/` and `correction-a226/` material. The receipt I used is `511-gptp-pin-asymmetry-grep.txt`.
6. I read the exact-head hosted check runs.
7. Only after this independent pass did I read the prior review findings on PR #537 (R274-1, R275-1, R274-2 and R275-2, as PR comments). They are resolved below. I did not open the review packets under `reviews/`.

## Composition map

Receipt: `receipts/composition_overlap.txt`, produced by `scripts/composition_overlap.sh`.

The PR changes 11 Markdown files (+230/-26). It changes no gitlink and no non-Markdown file.

The predecessor side (`759da623..70da0bcd`) changes 48 files, including the `gptp-processor` gitlink `c1b61743 → e5dcea6e`, which comes from #387.

Eight files overlap:

| Overlap file | Predecessor edit | PR edit | Interaction |
|---|---|---|---|
| `docs/design/GPTP_PLANE.md` | Engine-guide links re-pinned to `e5dcea6e` | New section "Propagation asymmetry is not modelled" (line 348 onward) | Disjoint hunks, same patch-id. The record's claims about "the pinned gPTP processor" now refer to `e5dcea6e` and were re-verified there |
| `docs/design/TIME_SYNC.md` | "Step policy" section and one bullet | One bullet at line 63 | Disjoint. The composed list at lines 56-68 reads coherently |
| `docs/guides/gptp/MANAGER.md` | Engine-guide links re-pinned | One status row at line 34 | Disjoint, same patch-id |
| `docs/MILAN_V12_ROADMAP.md` | CRF-counter paragraph (#529) | Section 3 table rows at lines 471-476 | Disjoint, same patch-id |
| `docs/reference/FR_NFR.md` | FR-CTRL-01..05 row (#529) | Contents entry, ledger note, FR-MVU rows, Section 2.6 note, Section 5 and Section 6 rows | This is the only file whose patch-id differs. The difference is only the adjacent FR-CTRL context line, which the predecessor rewrote. Both edits survive |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md` | Rows 5.4.2.25 and 5.4.5.1/.2 (#529) | Profile row, rows 5.4.4.2-.5, row 8.x, row 8.3/10.2.4.8/14.6.9 | Disjoint, same patch-id |
| `docs/reference/SUBMODULES.md` | Generated pin table and engine-guide links re-pinned | One donor-contradiction row, about the protocol processor at unchanged `424c688` | Disjoint, same patch-id. `check_submodule_docs.py` reports 4 exact gitlinks |
| `docs/traceability/ieee8021as.md` | Engine-ledger link re-pinned | Excluded state, AS-13 row, REQ-PTP-06 mapping, open-items bullet | Disjoint, same patch-id |

`README.md`, `REQUIREMENTS.md` and `docs/reference/MILAN_FEATURE_STATUS.md` are byte-identical to the PR source (`receipts/composition_identity.txt`).

## Gates run on the candidate

Receipt: `receipts/gates_candidate/`, produced by `scripts/run_gates.sh`. All 32 gates exited 0.

The composition-relevant results:

- `check_em_dash.py --base 70da0bcd` (the candidate's parent): 0 findings over 230 added lines in 11 pages, arms 57/57. The 230 added lines equal the PR's insertions exactly. `--selftest` also passes.
- `gen_toc.py --verify-anchors`: 161 cross-page fragment links reproduced. `--check`: OK for 107 pages. `--selftest` passes.
- `docs_check.py`: 0 findings over 165 md files.
- `check_gptp_docs.py`, both plain and with `--with-submodule`, verified against the donor checkout at `e5dcea6e`. `--selftest` passes.
- `check_submodule_docs.py`: 4 exact gitlinks. Its self-test passes, and so does `submodule_boundaries.gen.py --check`.
- `check_feature_status.py`: 0 findings. `--self-test` passes.
- `check_doc_style.py`, `DOC_MAP.gen.py --check`, `timesync_chain.gen.py --check`, `check_solution_docs.py`, `check_diagram_pngs.py`, `gen_module_matrix.py --check`, `check_doc_paths.py`, `check_archive.py`, `check_hygiene.py --check`, `check_baremetal_only.py --check`, `check_port_contracts.py`, `measure_test_evidence.py --check` and `check_todo_ownership.py` all pass.
- `ci_events.py --check` reports 1631 contract items. `ci_events.py --selftest` passes. The PR changes no workflow file and no CI policy page.

## Fault probes

Receipt: `receipts/probes/PROBES.tsv`, produced by `scripts/probes.sh`. Each probe seeds one composition-shaped defect, runs a gate, and restores the file with `git checkout`.

| Probe | Seeded defect | Gate | Result |
|---|---|---|---|
| p1 | SUBMODULES pin table set back to the source's `c1b61743` | `check_submodule_docs.py` | KILLED |
| p2 | A GPTP_PLANE engine link left at `c1b61743` | `check_gptp_docs.py` | KILLED |
| p3 | The PR's anchored heading renamed | `check_doc_paths.py` | Survived. This gate does not check fragments; p3b is the gate that does |
| p3b | The same rename | `gen_toc.py --verify-anchors` | KILLED |
| p4 | An em dash on the PR's added TIME_SYNC line, in the working tree only | `check_em_dash.py --base 70da0bcd` | Survived by design. The gate judges `base..HEAD` commits and this round may not commit. Evidence it judged the PR's lines is the 230-line count and its 57/57 planted arms |
| p5 | `GET_SYSTEM_UNIQUE_ID` claimed served in the generated fact block | `check_feature_status.py` | KILLED |
| p6 | FR_NFR contents link out of sync with its heading | `gen_toc.py --check` | KILLED |

## Semantic checks beyond the gates

**The #511 record's claims about the donor still hold at the composed pin.** Receipt: `receipts/pin_asymmetry_recheck.txt`, produced by `scripts/pin_asymmetry_recheck.sh`.

- `c1b61743` is an ancestor of `e5dcea6e`. The bump is four commits, all on the #68 step policy.
- The source lane's own searches were re-run at both pins:
  - `delayAsymmetry|delay_asymmetry|asymmetry|asym|cfg_asym|bench_uart_tune|uart_tune` outside `docs/history` and svg: exit 1 (no match) at both pins.
  - Any `asym` substring: exit 1 at both pins.
  - Files naming "asymmetr": the same nine `docs/history/v1/prototype` pages at both pins.
- Across the whole bump, zero changed lines name asym, uart, tune, latch or ingress. The eight "egress" lines are about the trim envelope.
- The only `hdl`/`bench` file changed is `hdl/ucode/gen_gptp_ucode.py`.

So these statements remain true at `e5dcea6e`: "The pinned gPTP processor has no asymmetry input", "outside its historic prototype pages the pinned tree never names it", the tuner being donor-bench-only, and the latch compensation not being adopted. Live dev `615b5a5d` still pins `c1b61743`, where the same results hold. The record is therefore correct whichever pin the final candidate carries.

**The parent identifiers the record cites survive composition.** Receipt: `receipts/parent_identifier_check.txt`.

- `INGRESS_LAT_NS_P`, `EGRESS_LAT_NS_P`, `_known_gp` and `--eth-port` have the same counts at the source and at the candidate.
- `GPTP_LAT` is still `0x7F0`: REGISTER_MAP.md:1450 and TIME_SYNC.md:62.
- The predecessors changed nothing under `hdl/ieee8021as` or `sw/builder`.

**The builder refusal was re-probed on the composed tree.** Receipt: `receipts/probe_builder_asymmetry_key.txt`. The configuration was copied to scratch.

- The shipping `endstation_ax7101_1x1_tdm8.yaml` builds with exit 0.
- The same file with `gptp: delay_asymmetry_ns: 0` added is refused with `CONFIG ERROR: gptp: unknown keys ['delay_asymmetry_ns']` and exit 1.
- The one tracked file the builder rewrote in the clone, `configs/generated/sweep_opts_ax7101.sh`, is byte-identical to HEAD.

**The predecessors do not contradict any of the three decisions.** Receipt: `receipts/term_inventory_src_vs_candidate.txt`.

- Outside `docs/history`, the file:count inventories for `SYSTEM_UNIQUE|MEDIA_CLOCK_REFERENCE`, `redundan`, `features_flags` and `NOT_IMPLEMENTED` are identical at the source and at the candidate.
- The `asymmetr` inventory differs in one place: #528 removed the word "asymmetrically" from a media-grid comment in `KL_chan_map_capture.sv`. That is unrelated to gPTP.
- #510 acceptance 2 (every occurrence of the command names consistent) is therefore not disturbed by composition.

## Prior public review findings

- **R274-1 F1 and R275-1 F1 (MINOR; Conformance, Docs).** The record named only two of the three places delayAsymmetry enters the arithmetic. This stays **resolved at this head**. The fix is `docs/design/GPTP_PLANE.md:378` "Where the term enters", which lists 11.2.13.2.1 f) and both 10.2.12 assignments, and the row at line 359. GPTP_PLANE's PR patch-id is identical between source and candidate.
- **R274-1 F2 and R275-1 F2 (MINOR; Conformance, Docs).** The Table 14-6 management statement and the management revisit condition. This stays **resolved at this head**. The evidence is `GPTP_PLANE.md:360` (the Table 14-6 read-write `Tdot3FD` row and PICS `MGT` `O`), `:402-404` (the management revisit trigger), `REQUIREMENTS.md:143` (byte-identical to the source), `FR_NFR.md:422` and `MILAN_COMPLIANCE_MATRIX.md:226`.
- **R274-2 and R275-2 (POSITIVE at `70f2c50d`, no open finding).** Their SUGGESTIONs are optional. Composition neither introduces nor worsens anything they name, because every PR hunk lands unchanged.

## Findings

None.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The composition touches this scope only through the gitlink that the #511 record's donor claims name. Re-verified at `e5dcea6e` and `c1b61743` (`receipts/pin_asymmetry_recheck.txt`). The #394/#510 term inventories are unchanged (`receipts/term_inventory_src_vs_candidate.txt`). `check_feature_status.py` reports 0 findings. The clause-text verification is carried by R274-2 and R275-2 at `70f2c50d`, whose hunks land unchanged | R275-3 (composition); R274-2 and R275-2 (source) | `8b7be584da62657f9767ad07e294d278144869c5`; source `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` |
| RTL | CLEAN | The PR changes no RTL, gitlink or test file (`receipts/composition_overlap.txt`). The RTL facts the record asserts were checked at the composed pin: the engine has no asymmetry input, the bump's only `hdl` change is `hdl/ucode/gen_gptp_ucode.py` with no asym, latch or ingress line, and `KL_gptp_shadow` is untouched by the predecessors (`receipts/parent_identifier_check.txt`) | R275-3; R274-2 and R275-2 (source) | `8b7be584da62657f9767ad07e294d278144869c5` |
| Robustness | CLEAN | The composition changes no behavior. The one malformed-input path the record relies on, the builder refusing an unknown `gptp` key, was re-probed on the composed tree (`receipts/probe_builder_asymmetry_key.txt`) | R275-3; R274-2 and R275-2 (source) | `8b7be584da62657f9767ad07e294d278144869c5` |
| Tests | CLEAN | No test file is in the PR. The executable checks for this documentation are the gates: 32 of 32 pass on the candidate, including their self-tests (`receipts/gates_candidate/SUMMARY.tsv`). Five of seven fault probes were killed, and both survivors are explained above (`receipts/probes/PROBES.tsv`) | R275-3; R274-2 and R275-2 (source) | `8b7be584da62657f9767ad07e294d278144869c5` |
| Docs | CLEAN | All eight overlap files were read as composed. The patch-ids are identical except FR_NFR's context line. Anchors, TOC, em dash, gPTP-doc pins, submodule pins, DOC_MAP and the feature facts all pass. The inbound anchors to `#propagation-asymmetry-is-not-modelled` resolve, and p3b proves the gate sees them. The composed text agrees with the predecessors' #529 and #387 edits | R275-3 | `8b7be584da62657f9767ad07e294d278144869c5` |

Integrity after the probes: `receipts/integrity_after_probes.txt`.

- HEAD and the tree are unchanged.
- `git status --porcelain=v2 --ignored` is empty. A `scripts/__pycache__` created by this round's gate runs was removed.
- The index equals HEAD (878 entries), and all 874 regular blobs rehash to their index oids. The on-disk modes match.
- The required gitlinks are clean at their pins: `gptp-processor e5dcea6e`, `protocol-processor 424c688`, `third_party/verilog-axis 48ff7a7`. `external` is uninitialized, as it was at the start.

## Limits

- This covers documentation-scope composition only. Per the brief, no full parent, processor, gPTP, Yosys or builder bank was run, and no Verilator probe was needed because the PR changes no RTL. The scoped Verilator binary was not used, so its identity was not checked.
- The candidate `8b7be584` does not exist on the hosting service (the check-runs query returns 422). The hosted evidence is for the PR source head `70f2c50d`, from GitHub's own merge ref at that time. There, 8 contexts executed and succeeded (`docs-check`, `docs-check-no-git`, `rtl-fast`, `elaborate`, `full-ci-gate`, `bdd-conformance`, `wire-accountability`, `changes`). 7 contexts were skipped: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, both shard matrices, and the physical gPTP job. Skips are not executions (`receipts/hosted_check_runs.tsv`).
- The em-dash gate could not be fault-probed without a commit (p4).
- I did not re-read the IEEE and Milan texts. The composition changes no clause wording, and the source rounds verified it.
- Physical calibration was NOT RUN. No hardware claim is made.

## Pending manager duties

- Build the final current-dev candidate from live dev `615b5a5d` (read-only delta: `receipts/live_dev_delta_readonly.txt`; #531 changed only `GM_LOSS_RECOVERY.md`, the #117 findings page and the findings README, none of this PR's files), the queued predecessors and this PR. Then re-run the documentation gates above on that exact tree, with `check_em_dash.py` using the derived merge base.
- Own the hosted and act acceptance at the head that merges.
- Handle the merge authorization, post-merge containment (`check_merge_containment.py`) and issue closure. The PR body says `Closes #511` and only relates #394 and #510, but the assignment comments say one PR "closes all three". The manager should settle whether #394 and #510 are closed by hand once their remaining acceptance is dispositioned (#394 acceptance 2 is a hardware item recorded as not met).

R275-3 FINISHED
