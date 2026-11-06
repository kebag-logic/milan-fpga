[R786] NEGATIVE - exact head b16f0175ac402e124314a40d1ea9573e431684dc

External independent review, round R786-1, of issue #845 / PR #847. Head `b16f0175ac402e124314a40d1ea9573e431684dc`, tree `e359cb69d58bb83ddc221b78cf6f633cd0ead037`, source base and live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`.

## Verdict

The adoption's mechanics are correct. The gitlink, the ROM ledger, the diagram, the audit, the dev merge and the re-anchored arm all reproduce. Every case in the pin page's table holds when driven through the real `milan_datapath`, and the route record matches its receipts.

The verdict is NEGATIVE for four open findings:

- **R786-F1 (MAJOR):** the adoption grows the shipping image with no resource-gate verdict and no owner decision, which `docs/design/AREA_BUDGET.md:156` requires. The executor disclosed this and the PR calls it open, but nothing has answered it.
- **R786-F2 (MINOR):** the three link-change statements leave out the largest parent-visible effect. A link change now takes a registered settled input out of the settled state.
- **R786-F3 (MINOR):** the sentence that row U dropped survives in the harness.
- **R786-F4 (MINOR):** the PR status claims exact-head gate results that were measured at the parent commit.

No defect was found in the behaviour under review. F1 needs a decision and a record, and F2 to F4 need text only.

## The six focus items

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Gitlink moves exactly to `92100657`; ROM digests and pin-derived records through their recorders | Holds | Only the `protocol-processor` gitlink differs from base, and the other five are unchanged. Processor `main` is `92100657`, the merge commit of PR #213, with the same tree `16b9d3fa` as `6162885f` (`receipts/gitlink_audit.txt`). `./syn/yosys/ooc.sh --record-rom-digests` in a copy leaves `rom_digests.tsv` unchanged (`receipts/rom_record.log`). `submodule_boundaries.gen.py --check` passes and a regeneration leaves no diff (`receipts/diagram_regen.log`). `check_submodule_docs.py`: OK, 6 exact gitlinks |
| 2 | Campaign counts re-recorded | Holds | `make -C tb/verilator/milan_dp unb-mutants`: 6 checks, 6 PASS, clean leg 499, arms 4, 2, 2, 2, 2 of 499, equal to `tb/verilator/milan_dp/README.md:822-830` (`receipts/unb_mutants.log`). `gsi-mutants` was not re-run; the author's receipt is 15 of 15. The other counts in that README were not re-derived |
| 3 | Pin page, CHANGELOG, integration contract, row U truthful | Pre-settle text holds, link-change text does not | Rows 1 to 3 of the pin page's table and row U hold through `milan_datapath` (`receipts/probe3_head.log`). The link-change row is incomplete: R786-F2 |
| 4 | `unb_mutants` arm re-anchored on `arb_want_w` | Holds | Anchor matches once at the pin. `arb_want_w` feeds only `arb_req_w = arb_want_w & rbt_tx_open_w` (`protocol_processor_top.sv:4692`). The old anchor is absent at `a9e84b66`, so the arm did fail on dev. Planting the hold after the mask gives the identical four named U2 failures, 4 of 499 (`receipts/arm_equiv.log`) |
| 5 | Dev sync keeps both sides; audit is the generator's | Holds | `7f56ef8e` has parents `519d9c2b` and `87e9d03a`, and its tree differs from `git merge-tree`'s only in `docs/DOCUMENTATION_AUDIT.md`. `docs_inventory.py --write` reproduces the head's audit byte for byte, sha256 `0dcaa73f...` (`receipts/docs_inventory_write.log`) |
| 6 | Route record: 52,497 LUT (+503), 15,780 of 15,850 slices, WNS +0.198 ns | Figures hold; judgment open | Every figure and delta matches the published reports, and `a29a7411` equals `519d9c2b` in every figure (`receipts/route_audit.txt`). No synthesis input moved after `a29a7411` (`receipts/gitlink_audit.txt`). The route was not re-run here. Its resource judgment is R786-F1 |

## Findings

### R786-F1 MAJOR - lenses Conformance, RTL, Docs

**Artifact:** `docs/design/AREA_BUDGET.md:154-156`; `docs/reference/SUBMODULES.md:556-584`; `CHANGELOG.md:81-84`. Not changed for this purpose: `syn/ooc/pp_resource_baseline.json`.

**Title:** the shipping image grows with no resource-gate verdict, no owner decision and no area record.

**Authority and evidence:**

- `docs/design/AREA_BUDGET.md:156`: "The next growth on the shipping image therefore has no slice room and needs its own owner decision". This adoption is that growth: +503 LUT and +478 FF on one flow. No decision is on #845 or PR #847 at this head.
- `docs/integration/BUILDING.md:575`: for an adoption, the resource gate enforces the thresholds. `docs/design/AREA_BUDGET.md:607-609`: the manager's merge bank runs the gate for every PR that changes the processor pin, on the route and the 1x1 standalone synthesis.
- `author/receipts/route-519d9c2b/resource-gate.txt`: the gate exits 2, NOT COMPARABLE. So no verdict exists yet.
- Route arithmetic against the record, reproduced from `pp_resource_baseline.json` (`receipts/route_audit.txt`): FF 54,579 against 53,707 is +872, over the +600 tolerance by 272. LUT is +485 of +500, slices 0 of +80.
- A point the published arithmetic does not cover: `AREA_BUDGET.md:464-465` gives `ooc-1x1` +250 LUT and +250 FF, and `ooc-8x8` +316 and +339. The route's same-flow growth is already +503 and +478. The processor's own 10 §5.1 (`10_srp_engine.md:270-272`) gives +1,555 LUT and +522 FF at two sources and two sinks, and +5,434 LUT and +1,988 FF at the default shape, on its Yosys flow. Those are estimates from other flows, not measurements of these endpoints, but they make a refusal on the standalone endpoints likely, not only on route FF.
- `AGENTS.md` section 2: an Issue cannot silently override a normative requirement, and a conflict must be published and marked as needing a decision. #845's acceptance names only the WNS floor.
- Earlier resource-moving adoptions state the gate outcome on the pin page (`SUBMODULES.md:204`, `:246`, `:302`, `:517`) and in `AREA_BUDGET.md`. This entry states neither, so a reader of `SUBMODULES.md:556-584` cannot tell that no gate judged it.

**In fairness:** the executor disclosed this as an open owner question, the gate run belongs to the manager's merge bank, and the route's figures are true. The record's single-worker synthesis means the route arithmetic is not a verdict. This finding is about the unmet precondition and the missing record, not about concealment.

**Impact:** with `Closes #845`, a merge would land growth the budget says needs an owner decision. If the merge-bank gate exits 1, no exception is on record, and precedents #771, #632 and #799 each needed one. `AREA_BUDGET.md` would also keep `a9e84b66` as the latest route.

**Required outcome:** an owner or manager ruling on #845 that either accepts this growth, with the re-baseline if the gate refuses it, or rules the gate inapplicable and says why. A gate verdict in its own form for `route-1x1` and `ooc-1x1`, or that ruling in its place. `docs/design/AREA_BUDGET.md` and the pin page must state this route and its outcome.

**Verification:** the gate's exit code on recipe-form receipts, `pp_resource_gate.py check-baseline`, the `AREA_BUDGET.md` diff, `docs_inventory.py --check`.

### R786-F2 MINOR - lenses Conformance, Docs

**Artifact:** `docs/reference/SUBMODULES.md:542`; `CHANGELOG.md:75-77`; `docs/integration/INTEGRATION_GUIDE.md:78-79`.

**Title:** the link-change text omits that a registered settled input leaves the settled state and must re-probe.

**Authority and evidence:** #845 required item 3 asks for "the link-change behaviour". The processor's ACMP table (`05_acmp_engine.md:280`) takes `EVT_TK_UNREGISTERED` from SETTLED_RSV_OK through A8 to PRB_W_DELAY or PRB_W_AVAIL. Measured through `milan_datapath`:

| Observation | Old RTL, `a9e84b66` listener, talker not discovered | Head, talker discovered | Head, talker not discovered |
|---|---|---|---|
| `probing_status` after `i_link_up` falls | 3, settled | 2, active | 1, passive |
| The three stream-valid flags | 0x52, set | 0x00, clear | 0x00, clear |
| `ACMPL_STATE[6]` | 1, kept | 0 | 0 |
| The talker's next declaration alone | not needed | `[6]` stays 0, `probing_status` stays 2 | `[6]` stays 0, `probing_status` stays 1 |
| A re-probe | none | at +930 ms; once answered, status 3, flags 0x52, `[6]` = 1 | none within 8 s |

Receipts: `receipts/probe2_oldrtl.log`, `receipts/probe3_head.log`, `receipts/probe2_head.log`.

So "Every input then waits for its talker's next declaration" (`SUBMODULES.md:542`) does not describe a registered settled input, which waits for a probe and a settle as well. The change from "stays settled" to "leaves settled" is the largest parent-visible effect of the link-change half of this adoption, and none of the three statements names it. `NFR-REL-01` is not contradicted: the input does recover without a reboot.

**Why not RESIDUE:** the fix changes an integrator contract statement and regenerates `docs/DOCUMENTATION_AUDIT.md`.

**Impact:** an integrator or controller author expects an input to stay settled across a link change while its reservation returns. It reads instead as unsettled, with its stream identity flags clear.

**Required outcome:** the three statements say that a registered settled input leaves the settled state at a link change, that its stream-valid flags clear, that `probing_status` becomes active when its talker is discovered and passive otherwise, and that it must re-probe and settle again, a value held meanwhile applying at that settle.

**Verification:** re-read the three statements against `receipts/probe3_head.log`; `docs_inventory.py --check`.

### R786-F3 MINOR - lens Docs

**Artifact:** `tb/verilator/pp_shadow/sim_main.cpp:3739-3741`.

**Title:** the harness keeps the sentence that row U removed.

**Authority and evidence:** the comment still says the processor's registrar "ignores every attribute until the sink is armed". Commit `151cc49c` removed that claim from the same group's README row, and the PR says row U "no longer says the processor ignores every attribute before the settle". At the pin it is false: the port registrars take every value, and head probe C1 shows one applied at the settle.

**Why not RESIDUE:** it is a behavioural claim in a source file, so under the owner's rule the doubt resolves to MINOR.

**Impact:** the comment gives a wrong reason for the group's real bind, beside a test group a later reader will extend.

**Required outcome:** the comment states what row U now states.

**Verification:** `git grep "ignores every attribute"` finds nothing current.

### R786-F4 MINOR - lens Docs

**Artifact:** PR #847 body, Status and Description.

**Title:** the PR status attributes gate results to a head they were not run on.

**Authority and evidence:** the body says "GREEN at `b16f0175...`: 65 suites pass...", that the firmware self-test, builder, behave and docs gates "pass at this head", and that the route was "measured at this head". Its own validation section says "Measured at `519d9c2b`". No published receipt names `b16f0175`: in the evidence tree at `05fd3fff` it appears only in the PR body's own copy. The two heads differ by dev's PR #834, which changes `scripts/owned_process.py`, the process owner `scripts/run_all_suites.sh:121` runs the suites under, plus the audit.

**Why not RESIDUE:** the sentence asserts a verdict at a head, so under the owner's rule the doubt resolves to MINOR.

**Impact:** a cold reader takes `519d9c2b` receipts as exact-head evidence for `b16f0175`.

**Required outcome:** the Status and Description name `519d9c2b` as the measured head, or exact-head receipts are published.

**Verification:** re-read the PR body against the receipts' `# head` lines.

### R786-R1 RESIDUE - pure wording

**Artifact:** `docs/reference/SUBMODULES.md:558`, `:560`, `:566`.

"Recipe" here names the one-directive build, while `PP_SHADOW_BASELINE_RECIPE.md` and the gate use the same word for the form this route is not in. Exact fix: "the settings below", "Setting" and "same settings".

### R786-S1 SUGGESTION - pin page and integration contract

"A link down or up" in the parent means an edge of `eff_link_w` (`hdl/milan/milan_datapath.sv:3231`), not the PHY alone. Head probe C5 shows `LINK_CTRL[0]` alone ends a registration and un-settles the input. `milan_datapath.sv:3233-3240` also records that one flap can give a second, later firmware pair on that signal, and `PHY_POLL_NS` is half the 250 ms service allowance. A short flap could therefore flush a re-declaration that arrived between the pairs. This is a reasoned hazard and was not measured. Naming the signal once would help an integrator.

### R786-S2 SUGGESTION - parent harness

No parent suite drives a pre-settle Talker or a link change through `milan_datapath`, as the PR says. `scripts/pp_parent_probe.py` shows it takes one `pp_shadow` group and fails 12 checks on the old listener, so a new Issue for it is practical. It is not a #845 acceptance item.

## Lens results at this head

```text
[R786] MAJOR Conformance - docs/design/AREA_BUDGET.md:156 - growth with no owner decision (R786-F1)
[R786] MINOR Conformance - docs/reference/SUBMODULES.md:542 - link-change behaviour incomplete (R786-F2)
[R786] MAJOR RTL - author/receipts/route-519d9c2b/resource-gate.txt - resource effect not judged by the gate (R786-F1)
[R786] PASS Robustness - receipts/probe3_head.log, tb/verilator/pp_shadow/sim_main.cpp group U through milan_datapath - full registrars, link down and up, LINK_CTRL[0] alone, re-bind, Failed variant and re-probe recovery, against the pin page's cases: 0 failures
[R786] PASS Tests - receipts/unb_mutants.log, receipts/arm_equiv.log, receipts/pp_shadow.log, tb/verilator/milan_dp/unb_mutants.py:64 - arm catches its four named checks on either side of the mask, 6 of 6; pp_shadow 4 legs, 719, 759, 719 and 317 checks, 0 failures; the probe fails 12 checks on the old listener
[R786] MAJOR Docs - docs/design/AREA_BUDGET.md:154-156 - no area record for this route (R786-F1)
[R786] MINOR Docs - R786-F2, R786-F3, R786-F4
```

Checked and clean within the unclean lenses:

- **RTL:** `link_up_i` reaches the listener through `KL_pp_shadow.sv:1275` and `KL_srp_top.sv:622`, on the existing synchronised `eff_link_w`. `KL_pp_shadow` and `milan_datapath` are unchanged. Only two processor HDL files moved. The integrator parameter check passes, 29 of 29.
- **Conformance:** pre-settle Advertise and Failed apply at the settle, and a Listener declaration reaches the wire within the bind's 20,000-cycle window, 200 ms on the harness's scale. The old listener sends none.
- **Docs:** the audit, diagram, ROM rows and pin table are current. The owner's comment rule: the reviewed delta's one changed source comment (`unb_mutants.py:63`) shows no lane label, round, reviewer ID or comment ID. Commits are one line with no trailers, and `git diff --check` is clean.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #845 body and comments; `AREA_BUDGET.md`; `BUILDING.md` section 5; processor `05_acmp_engine.md` and `10_srp_engine.md` 6.4; `receipts/probe3_head.log`, `probe2_oldrtl.log` | R786-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |
| RTL | UNCLEAN (F1) | `KL_srp_listener_fsm.sv` and `KL_srp_top.sv` delta; `milan_datapath.sv:3231`, `:9596`; `KL_pp_shadow.sv:1275`; route receipts; `receipts/route_audit.txt` | R786-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |
| Robustness | CLEAN | `receipts/probe2_head.log`, `probe3_head.log`, `probe2_oldrtl.log`; `tb/verilator/pp_shadow/sim_main.cpp` group U; `KL_link_guard.sv`; `milan_baremetal.c:1048-1081` | R786-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |
| Tests | CLEAN | `tb/verilator/milan_dp/unb_mutants.py`; `receipts/unb_mutants.log`, `arm_equiv.log`, `anchor_scan_r786.log`, `pp_shadow.log` | R786-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |
| Docs | UNCLEAN (F1 to F4) | `SUBMODULES.md`; `CHANGELOG.md`; `INTEGRATION_GUIDE.md`; `tb/verilator/pp_shadow/README.md`; `tb/verilator/milan_dp/README.md`; `AREA_BUDGET.md`; `DOCUMENTATION_AUDIT.md`; PR body; published receipts | R786-1 | `b16f0175ac402e124314a40d1ea9573e431684dc` |

## Prior public findings

None to resolve or retain. Read after this verdict and ledger were written: the PR has 0 reviews, 0 inline comments and two review-start lines, and the issue holds only the executor's TAKEN, STOP and REVIEW READY posts.

The executor's own published open risks, for the record:

| Risk | State at this head |
|---|---|
| 1. Resource gate has no verdict | Retained and widened as R786-F1 |
| 2. dev moved to `87e9d03a` | Resolved by `7f56ef8e` and `b16f0175`, focus item 5 |
| 3. CI image declarations stale | Tracked publicly by open issue #838, outside this PR |
| 4. Route memory over the 12 GB target | A process note, under the 24 GB cap; no product effect |
| 5. No parent harness | Retained as R786-S2 |

## Probe notes

- `scripts/pp_parent_probe.py` rewrites group U in a disposable copy. The tree under review was not edited.
- Head with the talker discovered: 0 failures (`probe3_head.log`). Head with it undiscovered, using `--no-adp`: 4 failures, all from the probe's own expectation of a re-probe, which the processor's table sends to PASSIVE when no talker is discovered (`probe2_head.log`).
- Old listener control, using `--no-adp`: 12 failures, in C1 (2), C1f (3), C3 (2), C4 (4) and C5 (1), so the probe can fail (`probe2_oldrtl.log`).
- A first control was invalid and is not published: `PP_DIR` does not reach `print-srcs` in the `pp_shadow` Makefile, so that build elaborated head RTL. The published control overlays the two old-pin listener files in the copy.
- Local paths in receipts are masked as `<packet>`, `<clone>`, `<home>` and `<toolroot>`; nothing else was changed.
- The published evidence manifest checks out: 797 files, none missing, no hash mismatch.
- The review clone was verified after the probes: HEAD, tree and index tree exact, no tracked change, the five populated gitlinks at their pins and clean (`receipts/clone_integrity.txt`).

## Real limits

- Not run here, by rule or by choice: the full sweep, firmware, builder, behave, `docs.yml`, `gsi-mutants` and any route. Those results are the author's receipts at `519d9c2b`, not this head and not a manager bank.
- `gsi` and `dynmap` anchors were not counted by my scan, whose reader only understands `unb_mutants.py`'s edit form. By inspection they target files this pin does not change, and the author's receipt reports 109 patterns, 0 stale.
- Route and slice figures were checked against published reports, not reproduced.
- Standards were not read. Clause citations were checked only against the processor's documents and `docs/traceability/ieee8021q.md`. Conformance of the SRP RTL itself belongs to the processor repository.
- The harness has no real peer and a compressed timebase, with the link guard disabled for the link cases. The +400 to +930 ms re-probe times are this run's draws.
- Physical calibration NOT RUN. Field skips are not hardware proof, and no hardware was touched.
- Hosted state at 2026-11-06T15:16:29Z on this head: 27 success, 1 skipped, 20 in progress, 7 queued (`receipts/hosted_snapshot.txt`). The skipped context is the physical gPTP job. This is not an acceptance result.

## Pending manager duties

- R786-F1's ruling and the merge bank's gate run on the route and `ooc-1x1`.
- Current-dev candidate build and native banks, with receipts linked on the PR.
- Hosted and act acceptance at the final head.
- Re-review at the corrected head. A change to `AREA_BUDGET.md`, the pin page or the harness comment un-covers Docs, and it must be covered again at a head that includes the change.
- The second independent positive review, and merge authorization.

R786-1 FINISHED
