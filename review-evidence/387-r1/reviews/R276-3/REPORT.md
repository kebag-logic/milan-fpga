[R276] POSITIVE - exact head 70da0bcdf7896b26efb4cc3f854c17a02f2c4126

Round R276-3 is the composition acceptance review of PR #540 (Relates to #387, partial) on the merge-train candidate. The exact head is `70da0bcdf7896b26efb4cc3f854c17a02f2c4126`, tree `914e656656594789e48c8ab7cfde34abb79ec032`. The review ran in a cleared context and used public state only. All five lenses were applied, each against the composition. No BLOCKER, MAJOR or MINOR finding is open. The composed tree introduces no defect beyond the reviewed sources.

## Contents

- [Scope and reconstruction](#scope-and-reconstruction)
- [Composition map](#composition-map)
- [Evidence at this head](#evidence-at-this-head)
- [Findings](#findings)
- [Prior public review findings](#prior-public-review-findings)
- [Per-lens results](#per-lens-results)
- [Reviewer-owned ledger](#reviewer-owned-ledger)
- [Limits](#limits)
- [Pending manager duties](#pending-manager-duties)
- [Clone state after the probes](#clone-state-after-the-probes)
- [Receipts](#receipts)

## Scope and reconstruction

I read the sources in this order:

1. AGENTS.md sections 3 and 5 to 8, and CONTRIBUTING.md section 6 (the wording and em-dash rules).
2. Issue #387's body and frozen acceptance.
3. The decisions and rulings on #387: 5606198212 (parts a and b), 5794731090 (the step rule that supersedes part a), 5800693336 (the assignment), 5802264260 (rulings 1 to 3), 5804878668 (the correction assignment), and the two author REVIEW READY comments, 5802234836 and 5805175917.
4. PR #540's body and the manager's review-start comments, including 5807262514 for this round.
5. The public evidence tree `review-evidence/387-r1` at `37d91083`.
6. The composition diffs and history.

I read the prior reviews' findings only after my own pass was complete. No private author material was read.

Focus: composition only. The PR source head `021b2e07b009158bcb0ce19529126eb1d330bba5` has two independent POSITIVE source reviews, R276-2 and R277-2. This round asks one question: does merging that source onto the queued base add a defect?

## Composition map

| Commit | Role | Verified |
|---|---|---|
| `50e78097` | live dev | parent of the #117 step |
| `5c51569b` | dev + #117 source `b71061d7` | `git merge-tree` recomputes its tree `ad69eb9f` exactly |
| `70da0bcd` | `5c51569b` + #387 source `021b2e07` | `git merge-tree` recomputes its tree `914e6566` exactly; one-line subject, no body |

Both merge commits are pure merges with no hand edits. The dev-to-candidate delta is 23 files, exactly the union of the two PRs' files (receipt `composition-preservation.txt`).

The #387 source is based on `759da623`. Dev has moved 27 files past that base, and the #117 predecessor adds 3 more.

**Textual overlaps.** Each file below is changed both by this PR and by something else in the candidate:

| File | Other writer | Result |
|---|---|---|
| `docs/design/GM_LOSS_RECOVERY.md` | #117 predecessor: "Recovery bound" section, a TOC entry, and a findings link | Both sides' `-U0` hunk bodies survive byte-identical |
| `docs/design/TIME_SYNC.md` | dev: the "Grid-aligner lock target" row | Both sides' hunks survive byte-identical |
| `tb/verilator/milan_dp/README.md` | dev: the `[CTRS-CRF]` paragraph (#529) | Both sides' hunks survive byte-identical |

The other 18 PR files are blob-identical to the source head, including `sim_gmstep.cpp`, the Makefile, `rom_digests.tsv` and the gitlink.

**Semantic interactions examined.** None of these files is textually shared, but each is read by what this PR adds:

| Interaction | Why it matters | Result |
|---|---|---|
| Dev's `milan_datapath.sv` (#534: CRF Stream Input GET_COUNTERS at index `N_STREAMS`, CRF notifications) × the gmstep leg | The leg drives AECP GET_COUNTERS and SET_CLOCK_SOURCE through this datapath | The composed leg's simulation output is byte-identical to the source head's published log (delay 0). It shows the same 44/48 and the same 4 documented failures at delays 0 and 12 |
| Same datapath × the leg's passing side | The README claims the #387 edit makes the leg pass | The published patch applies to the composed datapath without fuzz (offsets +5 and +39). The leg then passes 48/48 at delays 0, 5, 12, 20, 29 and 41, and the output is byte-identical to the source's published sweep logs at delays 0 and 12 |
| New gPTP pin `e5dcea6e` × dev's datapath | No earlier run built this pairing: the source ran the new pin on the old datapath, and dev ran the new datapath on the old pin | `milan_dp gptp` 181/181 and `gptp-lat` 181/181 at this head |
| Dev's `KL_media_grid_align.sv` (#74 lock keep-off) × the GM_LOSS_RECOVERY aligner row ("no PHC or step input") | The row's tree claim | Still true: the port list is unchanged (`KL_media_grid_align.sv:119-128`). The change clamps the single engagement capture only (`:267`) |
| Dev's comment-only edits to three configs × the ROM ledger and the per-config ROMs | The ROM pin bump | The ledger is keyed by pin, not by config. The builder regenerates `gptp_ucode.hex` for all four touched configs at the digests the source published for `e5dcea6e` |
| The #117 "Recovery bound" (5 s, "Media: recovers within one further stream restart") × the #387 step policy | The two sections sit on one page | Consistent: a return after link loss re-arms link-up, and a locked return either slews in at most 0.5 s or steps once. Either way the page's one-counted-event rule gives at most one restart, inside the 1.625 s margin |
| The README statement that the datapath edit "waits behind the lane holding `milan_datapath.sv`", now that #529 is closed and merged | Could be stale | Still accurate: open PR #549 changes `milan_datapath.sv` |
| Makefile source lists × dev | The PR's `CLKV_SRC` substitution | `print-srcs`, `print-pp-srcs` and `print-dp-vflags` are byte-identical to dev's Makefile. In the `run` dry run, the only difference is the PR's own `-DCLKV_QTICK_CYC_TB` on the two gptp legs, and both legs were run |
| Old pin `c1b61743` references | Pin-following docs | Only two dated "Source examined" records remain. Both are already present at the source base |

## Evidence at this head

The tool was Verilator 5.050 through the scoped wrapper (sha256 `905795b9...`; `--version` gives rev v5.050), with at most 8 jobs.

| Gate | Result | Receipt |
|---|---|---|
| 41 static gates from the docs workflow: `docs_check.py`; `check_em_dash.py --base` the parent `5c51569b`, dev `50e78097` and the source base `759da623`, plus `--selftest`; `check_doc_style`; `check_gptp_docs` (plain, `--with-submodule`, `--selftest`); the DOC_MAP, timesync_chain and submodule_boundaries generators `--check`/`--selftest`; `check_solution_docs`; `check_submodule_docs`; `check_diagram_pngs`; `gen_toc.py --selftest/--verify-anchors/--check`; `check_feature_status`; `check_doc_paths`; `measure_test_evidence --check`; `check_rtl_source_lists`; `check_port_contracts`; the cpp and py idiom checks; hygiene; todo ownership; naming; fail-fast; `check_baremetal_only --check`; `check_archive`; `ci_events.py --check/--selftest`; `git diff --check` against the parent and against dev | all exit 0 | `static-gates.log` |
| `check_sweep_shape`, `check_sv_idiom`, `check_sh_idiom`, `lint_rtl --check`, `pp_srcs --check`, `suite_shards --selftest`, `check_wire_accountability`, `check_entity_shape`, `xvlog_gate --check`, `gen_module_matrix.py --check` | all exit 0 | `static-gates-extra.log` |
| `make gmstep-build` at head; run at delays 0 and 12 | 48 checks, 4 failures at each delay: the 4 documented ones (two counted re-bases, one outside the step window; no `mr` toggle; no MEDIA_RESET). The delay-0 output is byte-identical to the source's published log | `gmstep-composed/` |
| The same leg with `DP_SRC` set to a scratch copy of the composed datapath plus the published patch | 48/48 at 6 delays; byte-identical to the source's published sweep at delays 0 and 12 | `gmstep-composed-plus-published-edit/`, `edit-probe-provenance.txt` |
| `make gptp`, `make gptp-lat` | 181/181 each | `milan_dp-gptp-composed.log`, `milan_dp-gptp-lat-composed.log` |
| Builder `gptp_ucode.hex` for arty_4x4, arty_8ch, ax7101_8x8 and ax7101_1x1_tdm8 | equal to the source's published `e5dcea6e` column | `builder-gptp-rom-digests-composed.txt` |
| Makefile equivalence against dev | identical source lists and flags | `makefile-print-equivalence.txt` |
| Hosted contexts | Source head `021b2e07`: 21 success, and 1 skipped (Physical gPTP, nightly and manual). A skipped context is not hardware proof. Candidate `70da0bcd`: not on the host | `hosted-check-runs.txt` |

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head. This round raises no new SUGGESTION.

## Prior public review findings

I read these after my own pass. Every #387 hunk is carried into the candidate byte-for-byte (receipt `composition-preservation.txt`), and the carried lines were re-read at their composed positions.

| Prior item | Lens | State at this head | Evidence |
|---|---|---|---|
| R276-1 F1 = R277-1 finding 1 (MINOR): the aligner's Decided cell | Conformance, Docs | RESOLVED, still resolved | `GM_LOSS_RECOVERY.md:152` quotes part (b). The tree claim still holds against dev's aligner change |
| R276-1 F2 (MINOR): ruling 5802264260 item 2 | Conformance, Docs | RESOLVED, still resolved | `GM_LOSS_RECOVERY.md:157` |
| R276-1 F3 = R277-1 finding 2 (MINOR): the "measures all of this" overclaim | Docs, Tests | RESOLVED, still resolved | `GM_LOSS_RECOVERY.md:168-185,212`. The composed leg grades exactly those rows |
| R276-1 F4 (MINOR): the counted event is not tied to the step | Tests | RESOLVED, still resolved | The step-window checks run and discriminate at this head: the head's identity re-base fails "every counted re-base lands at a PDU end right after the step" |
| R276-1 F5 (MINOR): a talker that stops for good | Tests, Robustness | RESOLVED, still resolved | The trailing-silence pause and rate checks run at this head (`gmstep-composed/delay-0.log`, TALKER line) |
| R277-1 finding 3 (MINOR): start-phase dependence | Tests, Robustness, Docs | RESOLVED, still resolved | The edited composed datapath passes at 6 delays |
| R276-1 S1 to S3, and R277-1's three suggestions | various | Resolved at the source, carried unchanged | Blob-identical Makefile and `sim_gmstep.cpp`; hunk-identical docs |
| R276-2 and R277-2 SUGGESTION: the render row's tree column opens "Yes" while a GM change that steps counts two | Docs | RETAINED as a SUGGESTION, unchanged by the composition | `GM_LOSS_RECOVERY.md:151` |
| R276-2 SUGGESTION: the decision and ruling are cited by bare identifier | Docs | RETAINED as a SUGGESTION, unchanged | `GM_LOSS_RECOVERY.md:150-151,157` |
| R277-2 SUGGESTION: the start-phase claim is approximate, and the feed delay never moves the step against the listener's PDU grid | Tests, Docs | RETAINED as a SUGGESTION, unchanged | `tb/verilator/milan_dp/README.md:371-374`; `Makefile:280-284` |

SUGGESTIONs are optional and do not affect coverage.

## Per-lens results

[R276] PASS Conformance - `GM_LOSS_RECOVERY.md:88-114,142-186` and `TIME_SYNC.md:75-107,149` at `70da0bcd`, against decisions 5606198212(b), 5794731090 and 5802264260, and against the composed `KL_media_grid_align.sv:119-128,267`, `milan_datapath.sv` (`mcr_restart_p_w`, `gm_recentre_p_r`), `KL_render_setpoint.sv:58` and `KL_mmcm_drp_servo.sv:267` - the #117 recovery bound and the #387 step policy are consistent on the one page, and every tree-column claim still holds against the RTL that dev changed.

[R276] PASS RTL - composed `hdl/milan/milan_datapath.sv` (blob `2bfbb3e7`), `KL_media_grid_align.sv`, `KL_crf_rx.sv`, the gitlink `e5dcea6e` and `syn/yosys/rom_digests.tsv` - the PR changes no RTL. The new pin elaborates with dev's datapath and passes `gptp` and `gptp-lat` at 181/181. The builder and suite ROMs regenerate at the published digests. The ledger row is pin-keyed and untouched by the other writers.

[R276] PASS Robustness - `gmstep-composed/`, `gmstep-composed-plus-published-edit/` (delays 0, 5, 12, 20, 29 and 41) - dev's CRF counter and notification traffic does not perturb the leg's failure paths (pause, rate, counter validity, step window). The delay-0 output is byte-identical to the source head's.

[R276] PASS Tests - `tb/verilator/milan_dp/sim_gmstep.cpp` (blob `c7c61dc5`) and `Makefile` (blob `a9504cb5`) at the composed head - the leg builds and grades the same 48 checks, with the same 4 failures the tree documents. The published edit still turns it green. The gptp legs pass. The sweep shape and suite-shard gates are clean.

[R276] PASS Docs - the three merged pages, the 18 blob-identical PR files, and the 51 static gates in `static-gates.log` and `static-gates-extra.log` - TOC, anchors, the em dash against the parent, dev and the source base, gPTP docs, pin tables, diagrams, the module matrix, test evidence and wording all pass on the composed tree. The README's lane-blocking sentence is still accurate (PR #549).

## Reviewer-owned ledger

Every lens's scope is touched by the composition, through the shared pages or through the dev RTL that the PR's leg and pin exercise. So each lens is covered here at the candidate head. The source-internal scope of each lens remains covered by the two source rounds, R276-2 and R277-2, at `021b2e07b009158bcb0ce19529126eb1d330bba5`. Every PR file at this head is blob-identical to that source head or hunk-identical to it.

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merged GM_LOSS_RECOVERY.md and TIME_SYNC.md against decisions 5606198212(b), 5794731090 and 5802264260 and the composed RTL; the #117 bound versus the step policy | R276-3 (composition); R276-2 and R277-2 (source) | `70da0bcdf7896b26efb4cc3f854c17a02f2c4126`; source `021b2e07b009158bcb0ce19529126eb1d330bba5` |
| RTL | CLEAN | composed datapath, aligner and CRF RX; the gitlink; the ROM ledger; builder and suite ROMs; gptp and gptp-lat legs | R276-3; R276-2 and R277-2 | same |
| Robustness | CLEAN | gmstep failure paths at 2 delays on the tree and at 6 delays with the edit | R276-3; R276-2 and R277-2 | same |
| Tests | CLEAN (1 SUGGESTION carried) | gmstep on the tree and with the edit; gptp legs; sweep, shard and evidence gates | R276-3; R276-2 and R277-2 | same |
| Docs | CLEAN (3 SUGGESTIONs carried) | three merged pages and 18 identical files; 51 static gates | R276-3; R276-2 and R277-2 | same |

## Limits

- **Banks not run.** No full parent, protocol-processor, gPTP, Yosys or builder bank was run. Act, host act_ci and hardware were not run either. The full `milan_dp run` recipe was not run: its source list and flags equal dev's, except the PR's own define on the two gptp legs, which were run. `ooc.sh` was not run. The ledger row and the pin are blob-identical to the source head, and no other writer touches either.
- **Delays sampled.** gmstep ran at 2 delays on the tree and 6 with the edit, not all 42.
- **The edit is a probe.** It ran on a scratch copy of the published patch. That patch belongs to the follow-up lane and is not reviewed here.
- **No physical evidence.** Physical calibration was NOT RUN. Acceptance 4 (the #117 bench) was not attempted.
- **Hosted evidence.** The skipped nightly physical gPTP context is not hardware proof. The candidate SHA has no hosted runs. Hosted and act acceptance belong to the manager.
- **Scope of this verdict.** It covers the composition at `70da0bcd` only. The final current-dev candidate is a separate object.

## Pending manager duties

1. Build and validate the final current-dev candidate at the merge turn. Live dev was `50e78097` for this round, and a later dev tip needs its own composition check.
2. Hosted and act acceptance for the exact merge head.
3. Queue interactions to recheck when these PRs precede or follow this one:
   - PR #547 (the CRF servo step window, #539) makes the CRF-servo row at `GM_LOSS_RECOVERY.md:154` stale when it lands.
   - PR #549 changes `milan_datapath.sv`, where the published #387 edit applies.
   - PR #538 changes how Contents headings are read.
4. #387 stays open after this merge. Still to come:
   - the datapath edit (acceptance 3), including the ruling-2 merge arm;
   - gmstep and its runner in the sweep;
   - the owner's ruling on the aligner re-centre;
   - acceptance 4 on the #117 bench.

   The #117 findings linked from `GM_LOSS_RECOVERY.md:218` were measured on an image built before this pin bump. Acceptance 4 measures the post-bump image.

## Clone state after the probes

The clone is restored to exact head `70da0bcd`, tree `914e6566`:

- The index writes that tree.
- All 874 tracked non-gitlink files hash to their index blobs (0 mismatches). Modes are intact: 832 files at 100644 and 42 at 100755, with every executable bit present.
- There are no untracked files. The only ignored path is the pre-existing `scripts/__pycache__/`.
- The gitlinks `gptp-processor e5dcea6e`, `protocol-processor 424c688f` and `third_party/verilog-axis 48ff7a7e` match their checkouts, each with 0 dirty entries.

Probe objects and the edited datapath copy stayed under the packet's `scratch/`. The receipt is `restore-verification.txt`.

## Receipts

Every receipt is listed in `MANIFEST.sha256`. Two scripts reproduce the probes:

- `static_gates.sh <clone> <log>`
- `gmstep_composed.sh <clone> <verilator> <outdir> <mdir> [DP_SRC] [delays...]`

Local paths in the build logs are redacted to `$WORKSPACE_HOME`, `$PACKET`, `$CLONE` and `$DATA`.

R276-3 FINISHED
