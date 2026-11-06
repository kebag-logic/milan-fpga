[R785] NEGATIVE - exact head b16f0175ac402e124314a40d1ea9573e431684dc

Round R785-1, internal cleared-context review of issue #845 / PR #847. Tree `e359cb69d58bb83ddc221b78cf6f633cd0ead037`. Base for the delta: dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`.

The adoption mechanics are sound: the gitlink, the ROM ledger, the re-anchored arm, the dev sync and the audit all check out, and the recorded route figures match their receipts. The verdict is NEGATIVE for one MAJOR and three MINOR findings. The MAJOR is an open owner decision: this adoption's growth has no resource-gate verdict, FF is past its tolerance by arithmetic, and the standing rule says the next growth needs its own owner decision. The PR says so itself.

## Results on the six focus items

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Gitlink and ROM digests | PASS | Gitlink is `9210065779b0f698fd7bdb22323a1ed5b8482677`, public processor main at review time; processor PR #213 is merged with that merge commit. Its tree `16b9d3fa` equals reviewed head `6162885f`'s. The five other gitlinks are unchanged from dev. `./syn/yosys/ooc.sh --record-rom-digests` on a disposable copy left the ledger unchanged. `ucode.hex` and `ltn_rom.hex` built at the pin hash to the new rows, which equal the `a9e84b66` rows. Pin table, drawio, SVG, PNG and manifest pass their generator and checkers. `receipts/merge_sides.log`, `receipts/rom_recorder.log`, `receipts/docs_gates.log` |
| 2 | Campaign counts | PASS | Clean `obj_notify` leg 499 checks, 0 failures, re-measured at this head. `unb-mutants` 6 of 6; its five arms report 4, 2, 2, 2 and 2 failures of 499, exactly the README's rows. `gsi-mutants` 15 of 15. The pp_shadow base leg passes 719 checks, 0 failures. A scan of parent mutant drivers found no string anchor moved by the pin (47 strings, 3 count changes, all prose or whitespace, none a planted pattern). `receipts/unb_mutants.log`, `receipts/pp_shadow_base.log`, `receipts/anchor_delta.log` |
| 3 | Pin page, CHANGELOG, integration contract, U row | PASS for the pre-settle path, N of 2, re-bind and the ROM statements. FAIL for the link-change recovery sentence, see F2 | Text compared with processor `docs/architecture/10_srp_engine.md` 6.4, `docs/guides/integrator.md`, `hdl/srp/KL_srp_listener_fsm.sv` and `05_acmp_engine.md`. A disposable probe measured it through the real `milan_datapath` |
| 4 | Re-anchored arm | PASS | `arb_want_w` feeds only `arb_req_w = arb_want_w & rbt_tx_open_w`, and the old lane assign matched 0 times at both pins while the new anchor matches once at both, so the stated dev failure is confirmed. Equivalence probe: the same 6,000-cycle hold planted at the arbiter's `arb_req_w` input and at `arb_want_w` gives the same result, 4 of 499, the same four named U2 order checks, verdict `caught`. `receipts/unb_arm_equiv.log`, `receipts/arm_anchor_pins.log` |
| 5 | Dev sync and audit | PASS | Merge `7f56ef8e` has parents `519d9c2b` and `87e9d03a`. Every dev-side file keeps dev's blob and every lane file keeps the lane's blob at this head; only the generated audit differs from either side. `docs_inventory.py --write` on a full copy reproduces `docs/DOCUMENTATION_AUDIT.md` byte for byte, and `--check` passes. `receipts/merge_sides.log`, `receipts/audit_regen.log` |
| 6 | Route record | Figures PASS; the gate position does not, see F1 | Receipts `route-519d9c2b`: 52,497 LUT, 54,579 FF, 15,780 of 15,850 slices, BRAM 87.5, DSP 13, WNS +0.198 ns, WHS +0.015 ns, 0 routing errors, `N_STREAM_IN_P` 2. Every delta in the page's table recomputes from `route-a29a7411/dev-cc204c6f.json`. The worst path is in the SDRAM controller. No file since `a29a7411` is a synthesis input |

## Findings

### F1 - MAJOR - Conformance, RTL, Docs

**Artifact:** `docs/design/AREA_BUDGET.md:154-156`, `docs/integration/BUILDING.md:575-580`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:568-576`, `docs/reference/SUBMODULES.md:554-584`, `CHANGELOG.md:82-84`, evidence `route-519d9c2b/resource-gate.txt`.

**Title:** the adoption's growth has no resource-gate verdict and no owner decision, and the durable records do not say so.

**Authority and evidence:**

- `BUILDING.md` section 5 says that for an adoption the resource gate enforces the thresholds on its route set. The recipe runs the route, its comparison directives and both standalone syntheses, so three endpoints are judged.
- The gate's only run here exited 2, NOT COMPARABLE: the one-directive route holds no recipe scripts. The evidence tree and the PR hold no `ooc-1x1` or `ooc-8x8` measurement at all.
- Recomputed from `syn/ooc/pp_resource_baseline.json`: FF 54,579 against the 53,707 record is +872, past the +600 tolerance. `AREA_BUDGET.md` states growth beyond a tolerance exits 1. LUT is +485 of +500, inside by 15.
- `AREA_BUDGET.md:156` and the owner decision it cites (PR #770, comment 6357449062) say the next growth on the shipping image needs its own owner decision. Issue #845 has three comments and none is that decision.
- Issue #845's acceptance names the WNS floor only. Under AGENTS section 2 an Issue cannot silently override this, and the author correctly published the conflict, but it stands undecided. The PR's own Status says an owner's answer is needed before merge.
- `AREA_BUDGET.md` is untouched by this PR and still ends at the `a9e84b66` route. The previous adoption recorded its route and gate result there (`cbc7c6043e`). `SUBMODULES.md` and the CHANGELOG give the route but neither the missing verdict nor the FF crossing, which appear only in the PR body.

**Impact:** a route that a comparable gate run would, by arithmetic, refuse on FF would merge unjudged, and a reader of the durable pages sees only that the floor is met.

**Required outcome:** a public owner ruling on this growth and on the gate's form for this route. Then either a verdict on all three endpoints or a cited exemption, with the baseline re-recorded if the ruling requires it, and `AREA_BUDGET.md`, the pin page and the CHANGELOG stating the position.

**Verification:** `pp_resource_gate.py check` exits 0 on the three endpoints, or the ruling is cited for each one not judged; `check-baseline` passes; the pages state it.

### F2 - MINOR - Conformance, Docs

**Artifact:** `docs/reference/SUBMODULES.md:542`, `docs/integration/INTEGRATION_GUIDE.md:78-79`, `CHANGELOG.md:75-77`.

**Title:** the link-change text says a settled input waits for the talker's next declaration; a reserved input actually leaves settled.

**Authority and evidence:**

- Processor `docs/architecture/05_acmp_engine.md` takes `EVT_TK_UNREGISTERED` in SETTLED_RSV_OK through A8 to PRB_W_DELAY or PRB_W_AVAIL.
- At `a9e84b66` the SRP listener has no `link_up_i`, so this consequence of a link change is new at this pin, and no parent page states it.
- Measured through `milan_datapath` (`receipts/presettle_probe_head4.log`), a sink settled on a pre-settle Talker: `probing_status` 3 with stream flags `0x52` before the link change, `probing_status` 1 with flags `0x00` after LINK_DOWN and LINK_UP.
- `receipts/presettle_probe_head2.log`: 200 further Talker declarations over the settled record registered nothing. So the page's "Every input then waits for its talker's next declaration" is not the recovery for this input: it must settle again first.

**Impact:** an integrator expects a link flap to cost one declaration. It also clears the input's probing status and its stream-valid fields until it re-settles, and the page gives no sign of that.

**Required outcome:** the three pages state that a registered, settled input leaves settled at a link change, and how it returns. The processor's `docs/guides/integrator.md` carries the same sentence, so a processor follow-up is needed as well. This finding judges the parent's text. Whether the transition itself is right belongs to the processor repository and is not judged here.

**Verification:** the text agrees with the ACMP table, and a cold reader can predict `probing_status` across a link change.

### F3 - MINOR - Docs, Tests

**Artifact:** `tb/verilator/pp_shadow/sim_main.cpp:3739-3741`.

**Title:** the source twin of the sentence corrected in row U still states the old behaviour.

**Authority and evidence:** commit `151cc49c` removed "the processor's registrar ignores every attribute until the sink is armed" from `tb/verilator/pp_shadow/README.md` because this pin makes it false. The same claim stands in the comment explaining why the U group binds first. The probe shows it false at this head: a Talker declared before the bind reads Advertise at the settle (`ACMPL_STATE` `0x00020058`). It is not in the reviewed delta, but the delta is what falsified it.

**Severity note:** this is comment text, but it sits in compiled test source and states a behaviour, so under the "if unsure" rule it is MINOR and not RESIDUE.

**Required outcome:** the comment matches row U, with the reason given by behaviour and issue ID.

**Verification:** read the comment; re-run pp_shadow.

### F4 - MINOR - Docs

**Artifact:** PR #847 body, Status and the route paragraph.

**Title:** the PR claims results at `b16f0175` that were measured at `519d9c2b`.

**Authority and evidence:** Status reads "GREEN at `b16f0175...`: 65 suites pass..." and the route is "measured at this head". All four sweep receipts record head `519d9c2b`, the route receipts are `route-519d9c2b`, the evidence tree has no path naming `b16f0175`, and the PR's own "How to validate" says "Measured at `519d9c2b`". The risk is low: item 5 shows the two commits since add only dev's six reviewed files and the regenerated audit, none a synthesis input.

**Severity note:** this attaches a verdict to a head, so it is MINOR and not RESIDUE.

**Required outcome:** the Status and route paragraph name the head actually measured and say what `b16f0175` adds, or receipts at `b16f0175` are published.

**Verification:** each claimed result names a head that has a receipt.

### Suggestions (not blocking)

- **S1 - Tests.** A pre-settle arm in pp_shadow group U looks practical: the planted probe needed about fifteen lines and passes through the real wiring. It would replace the PR's "no parent harness" limitation with a graded row.
- **S2 - Docs.** `tb/verilator/milan_dp/README.md:1515` still ends its dated `obj_notify` row at 421. The row is dated, so it is not false, but it no longer agrees with line 822.

## Prior public findings

None to resolve or retain: at the time of this report PR #847 had no reviews and no inline comments, and its issue comments are the two review-start notices. No other reviewer's report was read.

## Lens results

Clean lens, and the clean parts of the unclean lenses, in the section 6 format:

```text
[R785] PASS Robustness - receipts/presettle_probe_head4.log, receipts/unb_mutants.log, hdl/milan/milan_datapath.sv:3231 - link down and up on a settled input through eff_link_w, pre-settle ordering, an unanswered re-bind after the link change, a refused stale anchor (plant() count check, unb_mutants.py:189-207), checked against 10 6.4 and the ACMP table; behaviour is as the processor authority states
[R785] PASS RTL (delta other than F1) - protocol-processor diff a9e84b66..92100657 -- hdl - only KL_srp_listener_fsm.sv and one line of KL_srp_top.sv change; top ports and parameters unchanged, link_up_i reaches the listener from eff_link_w, N_STREAM_IN_P 2 in the route log, JOIN_MS_P default 200 not overridden by the parent
[R785] PASS Tests (delta other than F3) - receipts/unb_arm_equiv.log, receipts/unb_mutants.log - the arm can fail and fails by name; unb-mutants 6 of 6 and pp_shadow base 719/0 at this head
[R785] PASS Conformance (other than F1, F2) - issue #845 items 1 to 3, docs/reference/SUBMODULES.md:531-546 - pre-settle reach, the bound at N of 2, re-bind and Table 10-4 statements agree with processor 10 6.4 at the pin
[R785] PASS Docs (other than F1 to F4) - receipts/docs_gates.log - docs_check, diagram and PNG checks, anchors, inventory, check_submodule_docs; comment rule: the delta's only new source comment, unb_mutants.py:63, carries no lane label, round or reviewer ID
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Issue #845 and its comments; `BUILDING.md` 5; `AREA_BUDGET.md`; recipe; processor 10 6.4, 05 ACMP table, integrator guide; pin page, CHANGELOG, contract | R785-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |
| RTL | UNCLEAN (F1) | Processor `hdl` diff; `milan_datapath.sv` link path; `KL_pp_shadow.sv`; route receipts; `pp_resource_baseline.json` | R785-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |
| Robustness | CLEAN | Link-change and pre-settle probes through `milan_datapath`; `unb_mutants.py` plant guard; anchor scan | R785-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |
| Tests | UNCLEAN (F3) | `unb_mutants.py`; `unb-mutants` run; equivalence probe; `gsi-mutants` 15 of 15; pp_shadow base leg; `sim_main.cpp` group U | R785-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |
| Docs | UNCLEAN (F1 to F4) | CHANGELOG; pin page; contract; both READMEs; audit; diagrams; PR body; docs gates | R785-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |

## Limits

- **Not re-executed:** the full sweep, firmware self-test, builder, behave, the whole of `docs.yml` and the route. Those results are the author's receipts, at `519d9c2b`, not this head (F4). I checked the sweep heads and the route figures in those receipts, not their execution. No manager source bank ran at this head, and none is claimed.
- **Executed at this head:** pinned Verilator 5.050 (identity checked), `unb-mutants`, `gsi-mutants` (15 of 15, rc 0), the pp_shadow base leg, the ROM recorder on a copy, the inventory, the docs gates named above and `check_cpp_idiom.py`.
- **Probe scope:** the probe's talker was never discovered over ADP, so only the PRB_W_AVAIL path (`probing_status` 1) was measured. The discovered-talker path is read from the ACMP table. The return to settled after a link change was not measured: the harness's bind helper found no probe to answer, and the U arms that follow therefore fail in the probe build, as that state predicts. Those failures belong to the planted probe, not to the head.
- **Old-pin control not run:** a probe run at `a9e84b66` was dropped when the session's permission mode refused the command carrying its checkout. The old behaviour in F2 rests on source (no `link_up_i` in the listener at `a9e84b66`) and processor 10 6.4, not on a run.
- **Spec text:** Milan and 802.1Q clauses were compared through the processor's authority documents; the standards themselves were not opened.
- **Processor review:** the processor's four rounds were not repeated, and no SRP RTL defect is claimed.
- **Hardware:** physical calibration NOT RUN; nothing here is hardware proof.
- **Hosted:** when last read, the exact-head contexts were 27 pass, 27 pending and 1 skipping, so none is used as evidence and the manager owns acceptance.
- **Run incidents:** a first pair of campaign copies without git metadata failed at once and was discarded. Three duplicate `gsi-mutants` slices launched in error were stopped and their logs removed; the reported campaign is the single full run.

## Pending manager duties

- Obtain and publish the owner ruling F1 needs.
- Current-dev candidate validation and the hosted and act acceptance.
- A follow-up Issue for the CI tool inventory refresh: the PR says it belongs to its own Issue, and a search found none.
- A processor follow-up for the sentence in F2.
- The external review, and a re-review of the corrected head.

R785-1 FINISHED
