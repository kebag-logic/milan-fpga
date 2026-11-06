[R786] POSITIVE - exact head 853ca25ae00fe26b09e019fbfe70893666617fc1

External independent review, round R786-2, of issue #845 / PR #847. Head `853ca25ae00fe26b09e019fbfe70893666617fc1`, tree `bf3105f580d47a197a1e0d0af49ff343d78a6b1b`, source base and live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. This round covers rounds 2 and 3, the delta from `b16f0175ac402e124314a40d1ea9573e431684dc`.

## Verdict

POSITIVE. R785-1 F1 and R786-1 F1 to F4 are resolved at their cause, and all five lenses are clean at this head. Three RESIDUE items and two SUGGESTIONs are new, and none blocks. This verdict covers source review only. It is not hosted or act acceptance, it is not a candidate-merge validation, and it is not merge authorization.

As assigned, the area growth itself is not reported. The non-reproducing `inputs_sha256` is a separate issue and is listed only as a manager duty.

## The focus items

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | R785-1 F1, R786-1 F1 to F4 | All resolved | Section "Prior findings" |
| 2 | Thirteenth record written through `pp_resource_gate.py` | Holds, on strong indirect evidence | The file equals the gate's writer form, `json.dumps(baseline, indent=1) + "\n"`, at `83d837c0` and at the head. `83d837c0` touches that one file. Every utilization figure and all 51, 52 and 52 scopes (LUT, FF, RAMB36, RAMB18, DSP) of the three records come back from the published reports through the gate's own parsers with 0 mismatches, and each record's scopes are in the report's row order. The only identity change is `place_design -directive ExtraPostPlacementOpt` to `ExtraTimingOpt`. Outside `record`, only the `measured` notes changed, and the gate's write path replaces only `record`, so it leaves those notes to the author. No tolerance, floor or ceiling moved. `record.rc` shows rc 0 on all three. `receipts/baseline_audit.log`, `receipts/report_audit.log`, `receipts/writer_form.log`. Limit: I could not re-run `record` (see "Real limits") |
| 3 | `check` exits 0 on three endpoints, `check-baseline` exits 0 | Holds | Published `after-*.rc` are 0 and `before-*.rc` are 1 on all three. The `after` logs show delta 0 on every gated figure. `check-baseline` rerun here at the head: rc 0, "baseline PASS: 3 endpoints". `--selftest` rc 0. `--fuzz 1500 --seed 786`: 0 failures. `receipts/head_gates.log`, `receipts/record_inputs_checks.log` |
| 4 | Decision, figures, three directives and 15 free slices on the three pages | Truthful | The decision is quoted fairly on all three pages, with its link. All figures, deltas and percentages were recomputed from the record and reports: LUT 82.85 %, FF 43.05 %, slice 99.91 %, 15 free, 39.4 % and 69.3 %. Route LUT, FF and slice equal the record, and the three directive rows match the reports. Two wording items are recorded as R1 and R2 |
| 5 | Measurement reuse: no synthesis input changed | Holds | `git diff b16f0175 HEAD` outside `docs` and `CHANGELOG.md` touches only `syn/ooc/pp_resource_baseline.json`, which no synthesis reads, and `tb/verilator/pp_shadow/sim_main.cpp`, whose code is identical once comments are stripped. No gitlink moved. The ledger rows for `ucode.hex` and `ltn_rom.hex` at `92100657` equal the images in all three measurement sets, so the sets measured this pin. `ooc-8x8` was elaborated with `N_STREAM_IN_P` 9. `receipts/delta_checks.log`, `receipts/record_inputs_checks.log` |
| 6 | Definition of Done box and `519d9c2b` results | Honest | See below |

**The Definition of Done box.** The box reads "at the head: the docs gates, `check` on all three endpoints, `check-baseline`; the sweep, firmware self-test, builder and behave at `519d9c2b`, see Status". That is true.

- All four sweep `complete.json` files record head `519d9c2b` and exit code 0. Behave, builder, firmware and both campaign receipts are rc 0, and behave reports 14 features, 508 scenarios and 2,330 steps (`receipts/sweep_spotcheck.log`).
- The body names what falls between `519d9c2b` and the head. The list of six changed files from `b16f0175`'s merge matches `git diff 519d9c2b b16f0175`.
- Known limitations says the dev merge changed the process owner the suites run under, and that no sweep exists after `519d9c2b`.
- `check` at the head reads measurement directories from earlier commits. Status and "How to validate" both say so.
- The unticked boxes are honestly unticked.

## Findings

There is no BLOCKER, MAJOR or MINOR.

### R786-2-R1 RESIDUE - lens Docs

**Artifact:** `docs/reference/SUBMODULES.md:615`.
**Authority and evidence:** "Against that record, `check` exits 0 on every endpoint." directly follows a table whose column is "Exit, twelfth record" and whose rows all read 1. The record meant is the thirteenth, named above that table. `CHANGELOG.md` and `docs/design/AREA_BUDGET.md:169` are unambiguous.
**Impact:** the nearest antecedent makes the sentence appear to contradict the table above it. No figure or result is affected.
**Required outcome, exact fix:** "Against the thirteenth record, `check` exits 0 on every endpoint."
**Verification:** a disposable copy with this fix keeps `docs_inventory.py --check` at rc 0, leaves `docs/DOCUMENTATION_AUDIT.md` byte-identical and passes `check_doc_style.py` (`receipts/residue_fix_probe.log`).

### R786-2-R2 RESIDUE - lens Docs

**Artifact:** `CHANGELOG.md:89-91`.
**Authority and evidence:** these lines give the ExtraPostPlacementOpt figures as "the shipping route" and name no directive. `CHANGELOG.md:93-94` then gives the selected route's 15 free slices. `docs/integration/BUILDING.md` section 5 says the shipping image is built from the selected directive, so 70 and 15 read as one route. The pin page and the budget both name the directive.
**Impact:** a reader of the CHANGELOG alone cannot tell which route has 70 free slices. The figures are true.
**Required outcome, exact fix:** line 89 becomes "- On ExtraPostPlacementOpt the route grows 503 LUTs and 478 FFs."
**Verification:** same probe as R1.

### R786-2-R3 RESIDUE - lens Docs

**Artifact:** PR #847 body, Round 2 table, F1 row.
**Authority and evidence:** the row reads "The gate ran in its own form Answered in [Round 3](#round-3): ...". A cell separator is missing, so the row has two cells in a three-column table, its State cell is empty and the sentence runs on.
**Impact:** rendering and reading only.
**Required outcome, exact fix:** "The gate ran in its own form | Answered in [Round 3](#round-3): ...".
**Verification:** read the rendered table.

### R786-2-S1 SUGGESTION - lenses Conformance, Docs

**Artifact:** `docs/design/AREA_BUDGET.md:606`; `syn/ooc/pp_resource_baseline.json`, the `ooc-8x8` `measured` note.
**Authority and evidence:** both say the decision accepts the 8x8 growth. Issuecomment-6689114981 names "the shipping image", and 8x8 is not that image, as the PR body says. The authority is sound: the decision covers this pin and re-baselines "if the gate refuses", and the round 3 ruling, issuecomment-6692097382, orders all three endpoints re-baselined. So this is not a false statement.
**Impact:** a cold reader of the record finds only the decision and may ask what accepted 8x8.
**Suggested outcome:** cite the round 3 ruling beside the 8x8 figures, at the next edit of these lines.

### R786-2-S2 SUGGESTION - lens Docs

**Artifact:** `docs/design/AREA_BUDGET.md:188-189`; `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:123-126`, `:139-142`.
**Authority and evidence:** the selected route's worst setup and hold paths, the two `Synth` diagnostic statements and the 8,827 MB peak have no published receipt. The published ExtraTimingOpt reports hold timing summaries only, and full logs are given by digest. The prose is not a copy of the ExtraPostPlacementOpt path, whose receipt shows 16 levels and 9.177 ns against the stated 15 and 9.170 ns. None of these figures is gated.
**Impact:** these statements cannot be falsified from public evidence.
**Suggested outcome:** add a worst-path extract and the log lines to a later evidence packet.

## Prior findings

Read only after the independent pass above, whose candidates are saved in `receipts/independent_pass_notes.txt`.

| Finding | State | Basis at this head |
|---|---|---|
| R785-1 F1 / R786-1 F1, MAJOR | Resolved | Decision issuecomment-6689114981 and round 3 ruling. The gate ran in its own form on all three endpoints: exit 1 against the twelfth record, exit 0 against the thirteenth. `check-baseline` rc 0. `AREA_BUDGET.md`, the pin page and the CHANGELOG state the position. No page says "pending" |
| R785-1 F2 / R786-1 F2, MINOR | Resolved | All three pages now state that the input leaves the settled state, its stream-valid flags clear, `probing_status` goes active or passive, it must probe and settle again, and a held value applies at that settle. Checked against processor `gen_ltn_rom.py` row 14 and `05_acmp_engine.md:280` (`EVT_TK_UNREGISTERED`: A8, then PWD/A12 or PWA/A17), and `KL_srp_listener_fsm.sv:1434-1444`. The new row for an input with no settled registration also agrees, because that path strobes only when `reg_r` is not MT |
| R785-1 F3 / R786-1 F3, MINOR | Resolved | `tb/verilator/pp_shadow/sim_main.cpp:3739-3745` matches row U. `git grep "ignores every attribute"` finds nothing. Published `pp_shadow` receipt at `bf0d7d10`: 719, 317, 759 and 719 checks, 0 failures. Code is unchanged from `b16f0175` |
| R785-1 F4 / R786-1 F4, MINOR | Resolved | Status and Description name the head of each result, and receipts agree: `519d9c2b` sweep and docs, `b16f0175` and `bf6c5a67` measurements, `853ca25a` docs gates. The round 2 ExtraPostPlacementOpt route reproduces the stated LUT, FF, slice, WNS and WHS figures |
| R786-R1, RESIDUE | Retained by ruling | Round 3 ruling sends it to #495. The "Recipe" wording stands at `docs/reference/SUBMODULES.md:559-567` |
| R785-1 S1, S2; R786-S1, S2 | Retained, optional | No change required. The `tb/verilator/milan_dp/README.md:1515` row still ends at 421, and R786-S2 is disclosed in the PR body |

## Lens results at this head

```text
[R786] PASS Conformance - issue #845 body and rulings 6689114981, 6692097382; docs/reference/SUBMODULES.md:531-546; protocol-processor hdl/acmp/rom/gen_ltn_rom.py row 14 - acceptance items and the four ruling items, and link-change statements against the processor's ACMP table
[R786] PASS RTL - syn/ooc/pp_resource_baseline.json; published route reports; protocol-processor hdl/srp/KL_srp_listener_fsm.sv:1434-1444 - no RTL or gitlink changed since b16f0175; resource effect now judged by the gate; floors met at every corner on all three directives; routing errors 0; the listener's +443 / +522 is #212's, since hdl/srp is unchanged from f65c8ff7 to a9e84b66
[R786] PASS Robustness - receipts/directive_probe.log; syn/ooc/pp_resource_gate.py recipe(), judge() - the record's new directive stays comparable: another recipe directive is judged, +501 LUT exits 1, a directive outside the recipe exits 2; fuzz 1500 cases, 0 failures
[R786] PASS Tests - tb/verilator/pp_shadow/sim_main.cpp; receipts/delta_checks.log; receipts/sweep_spotcheck.log - the only test-file change since b16f0175 is a comment, code identical after stripping; gate --selftest rc 0; existing regressions as published at 519d9c2b
[R786] PASS Docs - docs/design/AREA_BUDGET.md, docs/reference/SUBMODULES.md, CHANGELOG.md, docs/findings/234_PP_SHADOW_AREA_BASELINE.md, docs/design/MARK_II_AREA_PLAN.md; receipts/head_gates.log - figures against the record and reports; no stale current-record claim found; docs_inventory and check_submodule_docs rc 0 here; published docs.yml at this head 72 rc 0, 24 not run with a reason, 0 bad; comment rule holds; RESIDUE R1 to R3 do not leave the lens unclean
```

Also checked:

- The commits since `b16f0175` are one line each with no trailers.
- `git diff --check` is clean.
- The delta's added lines show no private path and no comment-rule label.
- The published privacy check reports 0 private lines.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #845 body and comments; decision and rulings; `AREA_BUDGET.md`; `BUILDING.md` section 5; processor `05_acmp_engine.md`, `10_srp_engine.md` 6.4, `gen_ltn_rom.py`; `SUBMODULES.md`, `CHANGELOG.md`, `INTEGRATION_GUIDE.md` | R786-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |
| RTL | CLEAN | `git diff b16f0175 HEAD`; gitlinks; `KL_srp_listener_fsm.sv`; `pp_resource_baseline.json`; published utilization, hierarchy, timing, route status and IOB reports | R786-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |
| Robustness | CLEAN | `pp_resource_gate.py`; `receipts/directive_probe.log`; fuzz receipt; unchanged RTL keeps R786-1's probes at `b16f0175` | R786-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |
| Tests | CLEAN | `sim_main.cpp` comment-only check; gate `--selftest`; published `pp_shadow`, sweep, firmware, builder, behave and campaign receipts | R786-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |
| Docs | CLEAN | `AREA_BUDGET.md`; `SUBMODULES.md`; `CHANGELOG.md`; `234_PP_SHADOW_AREA_BASELINE.md`; `findings/README.md`; `MARK_II_AREA_PLAN.md`; `INTEGRATION_GUIDE.md`; `DOCUMENTATION_AUDIT.md`; PR body; published `docs.yml` receipts | R786-2 | `853ca25ae00fe26b09e019fbfe70893666617fc1` |

## Real limits

- **The packet is not signed.** The review assignment calls it a signed packet, but commit `a3149b014211f8d8bb15d601a41b8e4623b36dee` is unsigned and `MANIFEST.json` holds digests only. I verified the digests: 1,308 entries, 0 bad, 0 missing, 0 unlisted (`receipts/evidence_manifest.log`). That proves the published bytes match their manifest, not who wrote them.
- **`record --write` was not re-executed.** The measurement directories are not public. CARRY4 and `inputs_sha256` cannot be recomputed from the published reports, so those fields rest on the author's receipts, including `digest-at-head.txt`. The "not by hand" conclusion rests on the evidence in focus item 2.
- **Nothing was re-measured.** No route or synthesis ran here. No sweep, firmware, builder, behave or `docs.yml` run was made. Those results are the author's published receipts, at the heads they name, and no manager bank at this head exists or is claimed.
- **No Verilator run this round.** The scoped binary reports 5.050 but was not needed. `pp_shadow` was not re-run, because its code is unchanged. Behaviour through `milan_datapath` rests on the round 1 probes at `b16f0175`, whose RTL is unchanged.
- **Standards were not read.** The Milan and 802.1Q text is not in the repository. Clause citations were checked against the processor's documents only.
- **Physical calibration NOT RUN.** Field skips are not hardware proof, and no hardware was touched.
- **Hosted state is not acceptance.** At 2026-11-06T20:04:26Z on this head: 3 success, 1 skipped, 8 in progress, 26 queued (`receipts/final_state.log`). The manager owns hosted and act acceptance.
- The review clone was left exact: HEAD, tree and `git write-tree` match, no tracked change, and the five populated gitlinks are at their pins. `external` was already unpopulated.

## Pending manager duties

- Current-dev candidate build and native banks, with receipts linked on the PR, and post-merge containment.
- Hosted and act acceptance at the final head.
- The other independent review, R785-2, and maintainer merge authorization.
- If dev moves past `87e9d03a` before the merge, decide whether the record still describes the merge result, since `AREA_BUDGET.md` requires measuring on it.
- Carry to #495: R786-R1 and the processor `docs/guides/integrator.md` sentence, which I did not find there at review time, plus R786-2-R1 to R3.
- A new Issue for the non-reproducing `inputs_sha256`.
- Route the integrated image with every lab fix before the release build, as the decision requires. Merge order is this PR, then #846.

R786-2 FINISHED
