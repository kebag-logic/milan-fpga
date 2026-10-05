[R486] NEGATIVE - exact head 42f654478c11bd8f2b070969d83140587190f276

# R486-1: internal cleared-context review of PR #663 (issue #661)

- **Head under review:** `42f654478c11bd8f2b070969d83140587190f276`, tree `1772c37de75f39a15a5491d0ecfe9ba045c929b9`, 21 one-line commits on dev `506d91dbeeba585d72d2e80d92fca799c719f8ee`.
- **Live dev at review:** `fa450d301805881ad713b67521477bf042ddadfd` (#652 and #656 since the base). `git merge-tree --write-tree` of head and live dev is clean: tree `57cc8b8afa04c315e99e5aa2f4bb84469f24df06`. The disposable candidate commit built from it for this review is `cdb185175b858a3ebea71437aaa485cb2697cb1d` (never pushed).
- **Role:** internal reviewer, separate cleared-context session. Inputs were the public issue, PR body, authorities, diff, history and the public evidence tree at `0010a410b0150c2c7043142fb64036a7d2655799/review-evidence/661-r1`. Its 20 files hash to its `MANIFEST.json` published digests.
- **Prior public review findings on PR #663:** none, checked after this pass was written. The PR thread holds only the two review-start comments (this round and the external R487-1), with no review objects, and #661 holds no reviewer findings. Nothing is carried forward.

## Verdict

NEGATIVE. The adoption itself is correct and well evidenced:

- the four adaptations are exactly the supplied patches;
- every pin-derived record re-derives at the new pin;
- the baseline D arithmetic, policy and gate check hold;
- the closing claims are supported;
- no parent RTL, firmware or SoC interface changed.

Two MINOR findings remain open, both in the live PR body and both under `Docs`:

- **F1:** host storage paths and a local account name, which the manager's own published copy redacts.
- **F2:** a top-port count of 213 where the repository's parser counts 212.

Under the owner rule neither can be RESIDUE: F1 touches a privacy rule and F2 is a figure. Every other lens is CLEAN. Three RESIDUE items and one SUGGESTION follow and do not affect the verdict.

## Findings

### F1 - MINOR - Docs - PR #663 body, sections "How to get into the same state" and "How to validate" (body lines 70-81 and 113-118 as fetched)

- **Authority/evidence:**
  - CONTRIBUTING section 6: no bench-identifying information such as hostnames or home paths; use placeholders. `scripts/docs_check.py:285-291` records that its rules stopped spelling the bench account so that no tracked file carries it.
  - AGENTS section 6, `Docs`: the PR and Issue must contain enough evidence for another cold reviewer.
  - The live body spells absolute host storage and tool paths on 7 lines: its `export` lines and its suite and synthesis commands.
  - The manager's published copy of the same file (`review-evidence/661-r1/author/PR-BODY.md`, `"path_redacted": true` in its `MANIFEST.json`) replaces every one of those paths with `$VALIDATION_TOOLS` / `$VALIDATION_STORAGE`. So the publication policy treats them as non-public, and the live body was not brought into line.
  - In both the live body and that published copy, the synthesis replay is a privileged mount-namespace command that ends by switching to a named local account. No other published evidence file names it.
  - Receipt: `receipts/pr-body-vs-published.txt`. It is redacted, so it republishes neither the paths nor the account.
- **Impact:** a public PR body exposes host layout and an account name. Its reproduction steps also depend on private host paths, so a cold reviewer cannot follow them as written.
- **Required outcome:**
  - The live PR body carries placeholders for every host path and names no local account.
  - The privileged ABC-selector step is described by what it selects (the ABC revision `syn/yosys/README.md` requires), not by host paths or an account.
  - The published evidence copy is brought into line the same way.
- **Verification:** fetch the PR body and the published copy, and confirm neither holds an absolute host path or an account name.

### F2 - MINOR - Docs - PR #663 body line 52, "its 213 ports are unchanged" (also `review-evidence/661-r1/author/HANDOFF.md`, "The declared top port count stays 213")

- **Authority/evidence:**
  - The repository's own port parser, `scripts/sv_ports.py` (the one `check_port_contracts.py` uses), counts **212** ports and 41 → 42 parameters on `protocol_processor_top` at both `631eeb34` and `ead80360`.
  - An independent header scan (`ports_delta.py`) also counts 212 at both pins. It finds no added, removed or re-typed port, and one added parameter, `NVM_MEM_TMO_CYC_P`.
  - Receipts: `receipts/pp-top-sv_ports.txt`, `receipts/pp-top-port-delta.txt`.
  - The substantive claim, no port change, is TRUE. The figure is not reproducible.
- **Impact:** a stated count no reviewer can reproduce, in the PR's interface-change statement.
- **Required outcome:** the figure is corrected to the measured 212, or the body names the counting method that yields 213.
- **Verification:** rerun `ports_delta.py` / the `sv_ports` count at both pins and compare with the stated figure.

### R1 - RESIDUE - Docs - PR #663 body lines 70-71

- **Defect:** "The implementation branch is local and has not been pushed by this lane." and "From the supplied repository: `git switch 661-pp-pin-ead80360`" are stale now that the branch is published as the PR head.
- **Exact fix:** "The branch is published as `661-pp-pin-ead80360`. From a clone of this repository: `git fetch origin 661-pp-pin-ead80360 && git switch --detach FETCH_HEAD`."

### R2 - RESIDUE - Docs - `docs/reference/SUBMODULES.md:148`

- **Defect:** the parent-position cell "A parent lane transfers names to `d3_unflushed_o`" reads in the present tense as done. The D3 page's header (`docs/design/SAVED_STATE_MATERIALIZATION.md:15`) and `CHANGELOG.md:54` say name pending is not yet transferred.
- **Exact fix:** "Not yet adopted: a later parent lane (D3 section 18.3, lane 3) moves name pending to `d3_unflushed_o`; until then the sticky term stays."

### R3 - RESIDUE - Docs - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:333` (row F5)

- **Defect:** the row still ends "successful packing grants no waiver". Since this adoption, the 8x8 image packs only because `configs/endstation_ax7101_8x8.yaml` declares an explicit model-lint waiver for exactly this defect, and the row does not say so.
- **Exact fix:** append "The 8x8 configuration's `model_lint_waivers` entry (L1 `port-cluster-minimum`, STREAM_PORT_INPUT 0 to 7, #584) lets the default lint pack it; the packer refuses the waiver once any of those ports passes. The waiver is not a conformance claim."

### S1 - SUGGESTION - Docs/RTL - `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:38-40,49`

- **Observation:** the standalone synthesis WNS estimate falls from -1.616 to -2.580 ns at 1x1 and from -1.947 to -4.095 ns at 8x8.
  - That is a larger fall than any contributing processor lane recorded. For example, processor PR #154's own estimates moved -2.059 → -1.874 at 1x1 and -2.161 → -1.495 at 8x8, and PR #155's moved -2.059 → -0.743 at 1x1.
  - The finding tabulates the values and states they are not a route verdict, which is correct, and the gate does not grade standalone timing (`GATED["ooc"]`).
- **Suggestion:** one sentence naming the 8x8 fall, and pointing to whichever issue owns an integrated 8x8 route, would stop a later reader mistaking it for noise. No route claim in this PR depends on it.

## The six focus checks

### 1. The four adaptations, the P2 amendment and the L6/L10 cleanup

**Patch-tree equivalence.**
- I applied the four supplied patches in the order c8, p2-p1, c10, 232 to an index read from the pin commit `4a2f8ae41`. Each patch applied cleanly.
- Each intermediate tree equals the corresponding commit's tree exactly:
  - c8 → `6298dd24` = `dbd9e2467`;
  - p2-p1 → `e7afc773` = `eefffe50f`;
  - c10 → `dd9ff6fb` = `880a40fc6`;
  - 232 → `35a2525f` = `42c63ebc9`.
- Receipt: `receipts/patch-equivalence.txt`.

**P2 amendment.**
- The D3 pages state the port deadline `NVM_MEM_TMO_CYC_P = CLK_HZ_P`, 1,000 ms. This is derived as 20 times the backend's 50 ms grant hold, and checked as follows:
  - `KL_nvm_backend` defaults `T_HOLD_MS_P = 50`, and no parent instance overrides it;
  - `KL_pp_shadow` passes `CLK_HZ_P` and leaves the new parameter at its default;
  - the err carries cause DEADLINE;
  - the abandoned command stays owed until the device's terminal or a reset;
  - a later change ends after three attempts with `nvm_alarm`, matching DR2c in the processor top's parameter documentation;
  - the alarm revokes `nvm_backed`, matching `KL_nvm_backend.sv:95-96` and `:642`.
- Processor #15 and #20 are closed by PR #145 (merged `ddb3119d`), as the pages say.
- The W13 amendment is labelled "not re-executed here", which is honest.

**L6/L10 cleanup.**
- `sw/builder/aem_image_checks.py` is deleted, and both emitters now rely on `gen_desc_image.build()`'s default lint.
- The lint covers every retired check:
  - L6: offset 76, count ≥ 1, length, identity list, existence;
  - L10: offset 144, count ≤ 8, empty, length `144+4N`, current-rate membership;
  - per-configuration presence through L1 `required-type` and `audio-unit-for-aaf`.
- Its checks are equal or stricter, and it reads the descriptor bodies that are packed unchanged.
- `avdecc/gen_aemi_image.py` also packs with the lint on.
- No stale reference to the deleted checker remains outside history.

### 2. Pin-derived records

- **ROM digests:** re-generating `ltn_rom.hex`, `ucode.hex` and `gptp_ucode.hex` at the pins gives `23cc67ee…`, `518b900c…` and `c496ed8a…`. These equal the new `ead80360` rows and the gPTP row, and equal the `631eeb34` rows, so both processor ROMs are unchanged (`receipts/rom-digests.txt`).
- **Submodule page and diagram:** the pin table, the eleven-lane table and the boundary diagram pass `check_submodule_docs.py` and `submodule_boundaries.gen.py --check`. The eleven merges and their SHAs equal processor `git log --first-parent 631eeb34..ead80360`.
- **Other records:**
  - the port budget (1,757 → 1,759) passes `check_port_contracts.py`;
  - naming passes `measure_naming.py --check`;
  - the two re-recorded DUT-reader dispositions match the pinned `acmp_mutants.py` (the arm-queue ring table) and `test_gen_desc_image.py` (packaged models and `model_ids.json`), and `measure_test_evidence.py --check` passes.
- **xvlog budget:** the two retired findings (`pd_ix_w`, `srp_class_a_prio_w`) are now declared at first use. The two kept findings sit at the recorded lines 194 and 383 (`receipts/xvlog-decl-order.txt`). Vendor analysis itself was not run here.
- **Census, firmware digest and NVM capture:** `check_nvm_capture.py` passes, with census, clocks, both timing arms and receipt agreeing. Across all five configurations, every builder output and every packed `aem_desc.bin` is byte-identical at base and head. The one exception is the 8x8 `aem_overlay.json`, which gains the waiver key (`receipts/builder-compare/`). So no capture re-measure was owed.

### 3. Resource baseline D

- **Recorded figures:** `syn/ooc/pp_resource_baseline.json` records the route at 50,318 LUT, 54,214 FF, 15,789 slices, 87.5 BRAM tiles and 74 RAMB36, with WNS +0.108 ns and WHS +0.036 ns. Standalone 1x1 is 23,178 LUT / 19,776 FF, and standalone 8x8 is 29,853 / 27,370.
- **Policy unchanged:** at all three endpoints the tolerance, floor, ceiling, identity and kind are unchanged from C. Only the record figures, scopes, input digest and `measured` note moved (`receipts/baseline-diff.txt`).
- **Per-block table:** every per-block cell in the finding's table equals JSON D minus JSON C for all eleven scopes and three endpoints.
- **Derived figures:** every one recomputes:
  - -449 / -5,420 / -43 / -5 RAMB36, and 61 slices free;
  - 79.37 %, 12,278 over target, 10,608 wrapper ceiling and 54 %;
  - outside-wrapper +569 / +90, datapath 41,657 and +475 / +83.
- **Processor PR deltas:** the cited deltas match those PRs' own records (#153 -927 / -2,012; #154 -629 / -2,424 and 8x8 -1,392 / -3,445; #155 -282 / -1,093 and listener +123 / -55; #150 +683 / +94 and 8x8 +1,520 / +217).
- **Gate checks:** `pp_resource_gate.py check-baseline` passes (3 endpoints), and the gate `--selftest` passes (260 arms, 500 fuzz cases).
- **Route WNS:** it fell 0.085 ns, within the 0.25 ns limit and above the +0.030 ns floor.

### 4. Closing claims

- **#639:** its remaining item is "the resource gate's baseline is re-recorded". Its levers landed in processor PR #155, carried by this pin, and this PR records D. `Closes #639` is supported.
- **#234:** the 2026-10-03 rulings mark criterion 1 met at the 50 MHz shipping clock (comment 5967852698). The manager's record (5974629836) leaves only criterion 2. The finding shows the notification, SRP and arm-queue payloads mapped to distributed RAM. `Closes #234` matches the assignment's condition.
- **#661:** the acceptance is met within author scope; criterion 5 (bench soak) is the manager's after merge.
- **The 60 % target:** neither the PR nor any page implies it is met. The PR body, `AREA_BUDGET.md` and the finding each say the image is 12,278 LUT over and that the redesign is #640's.

### 5. The #656 and #657 exceptions, and `milan_dp_gptp` once merged

- **Base and head equality:** the public `exception-comparison.json` records both campaigns equal at base and head. The physical leg is 139 checks / 3 failures, rc 2 at both, and the same three audio-order verdicts. The render leg is the same 28 PASS / 4 FAIL list, rc 2 at both.
- **What this PR touches:** nothing in `tb/verilator/milan_dp/`. #656's fix on dev touches only `sim_ax1x1gptp.cpp` and its README (peer-talker pacing). The descriptor image the leg builds (`ax1x1gptp-aemi`) is byte-identical at base and head.
- **Candidate run:** I built the disposable candidate (this head merged with live dev `fa450d30`, commit `cdb18517`, pinned submodules at their gitlinks) and ran `make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4` under the pinned Verilator 5.050. The result:
  - the physical leg gives **139 checks, 0 failures, RESULT: PASS**, with the simulation exiting 0 (3,803.91 wall seconds);
  - `verify_abort.py` passes setup abort 6/0, no-TX accounting 20/0 and no-Pdelay accounting 14/0;
  - make rc 0;
  - the candidate's `aemi.bin` digest `4fc8d615…` equals the head's packed 1x1 TDM8 image.
- **Answer:** nothing in this PR stops `milan_dp_gptp` passing once merged. On the merged tree it passes (`receipts/candidate-gptp/`).

### 6. No parent RTL, firmware or SoC interface change beyond the adaptations

- **Diff scope:** the diff touches no file under `hdl/` and no firmware source. `sw/litex/milan_soc.py` only drops the retired checker call.
- **Processor top:** it gains only `NVM_MEM_TMO_CYC_P`, left at its default.
- **Generated artifacts:** builder outputs and packed images are byte-identical at base and head for all five configurations, apart from the 8x8 overlay's waiver key, which the c8 patch carries.

## Lens results

```text
[R486] PASS Conformance - focus 1 to 6 above; protocol-processor@ead80360 hdl/adp/KL_adp_engine.sv:33-41 and tb/adp_engine/README.md:174-212 against docs/reference/REGISTER_MAP.md:1032-1037 (IEEE 1722.1-2021 Section 6.2.2.15 increment after ENTITY_AVAILABLE, reset at ENTITY_DEPARTING); model_rules.py CHECKS L6/L10/L1 against the deleted sw/builder/aem_image_checks.py; #639/#234/#640 issue text and rulings against the PR's closing keywords
[R486] PASS RTL - git diff 506d91db..42f65447 has no hdl/ path; receipts/pp-top-port-delta.txt (no port added, removed or re-typed; one parameter added); hdl/milan/KL_pp_shadow.sv:1087 passes CLK_HZ_P, NVM_MEM_TMO_CYC_P left at default; KL_nvm_backend.sv:145 T_HOLD_MS_P 50 unoverridden; receipts/xvlog-decl-order.txt; pp_shadow at head 606+606+646+311 = 2,169 checks, 0 failures
[R486] PASS Robustness - silent-device path: processor top parameter documentation (deadline, owed command, three attempts, alarm) against SAVED_STATE_MATERIALIZATION.md sections 8.8/15 item 4 and KL_nvm_backend.sv:642 (alarm revokes nvm_backed); waiver pass-through probes (receipts/probe-36b) show a dropped waiver is refused by name at 8x8; nvm_cosim lint and quick (315/315) at head; receipts/candidate-gptp: head merged with live dev passes the physical leg 139/0 and accounting 40/0
[R486] PASS Tests - receipts/probe-36b: control passes, five mutants killed (either emitter lint=False; waiver dropped at overlay, spec or document); receipts/probe-tops: control passes, stale and unrecorded planted defects killed, including the new live STALE RECORD arm; receipts/gates-head: 17 consumer gates rc 0; resource gate --selftest and check-baseline rc 0
```

`Docs` is UNCLEAN at this head under F1 and F2. It was applied to every changed page and to the PR body, and apart from F1, F2 and the RESIDUE/SUGGESTION items above it found the pages accurate. That covers the CHANGELOG, `SUBMODULES.md`, the D3 pages, `REGISTER_MAP.md`, `PP_DESCRIPTOR_OWNERSHIP.md`, `ENDSTATION_BUILDER.md` (72 rows counted), `AREA_BUDGET.md`, the finding and its README row, `CODE_QUALITY.md` and the `pp_shadow` README.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REGISTER_MAP `0x644` note vs `KL_adp_engine.sv` and the §6.2.2.15 text; lint L1/L6/L10 vs retired checker; P2/P1 contract text vs processor top; #639/#234/#640 closures | R486-1 | `42f654478c11bd8f2b070969d83140587190f276` |
| RTL | CLEAN | no parent `hdl/` change; processor top port/parameter delta; `KL_pp_shadow` parameterisation; xvlog declaration order; `pp_shadow` 2,169 checks | R486-1 | `42f654478c11bd8f2b070969d83140587190f276` |
| Robustness | CLEAN | silent-device deadline and alarm path; waiver pass-through refusals; `nvm_cosim` lint/quick; candidate-merge physical leg | R486-1 | `42f654478c11bd8f2b070969d83140587190f276` |
| Tests | CLEAN | gate 36b mutation probes; tops self-test probes; 17 consumer gates; resource gate self-test and baseline check | R486-1 | `42f654478c11bd8f2b070969d83140587190f276` |
| Docs | UNCLEAN (F1, F2) | every changed page; PR body; public evidence packet | R486-1 | `42f654478c11bd8f2b070969d83140587190f276` |

## Real limits

- No Vivado run. Baseline D's figures, the routed-net count, the critical-path description and the RAM mappings are the author's measurements. I checked their internal consistency, policy, gate validity and arithmetic, not by re-measuring. The raw reports are not public and are represented by digests only.
- No vendor analysis (`xvlog_gate.py`): no Vivado is on this host's path. The ratchet entries were checked by declaration order in the pinned sources.
- Full banks were not run by this reviewer, as assigned: the parent sweep, processor and gPTP suites, Yosys, the whole builder, BDD/LiteX, the docs workflow under GNU Make 4.3, and the #657 render campaign. For those I rely on the manager's public evidence, which I read.
- The #656 base/head equality is the author's measurement. I ran only the candidate-merge physical leg.
- No hardware. Physical calibration NOT RUN, and the bench soak is the manager's after merge.
- The processor PRs' internal correctness is outside this lane. I verified only their parent-visible effects and cited figures.
- **Hosted evidence at this exact head, read at the end of the round:** 21 executed contexts concluded `success`, including `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, all five Verilator and four Yosys shards, and the `verilator-suites` and `yosys-portability` aggregates. One context, "Physical gPTP (nightly and manual)", is `skipped`: it is not executed evidence. Acceptance of hosted and act results is the manager's (`receipts/hosted-check-runs.tsv`).
- Suite build products from my focused runs remain in the clone's ignored output directories. Tracked bytes, modes, index and gitlinks were re-verified exact after all probes (`receipts/clone-restore-check.txt`).

## Pending manager duties

- Correct the live PR body (F1, F2), then carry R1 to R3 to the residue checklist.
- The external review ([R487]) and the re-review of the corrected PR body.
- Hosted acceptance (the aggregates concluded `success` at this head) and act replication.
- The final current-dev candidate build with the full local bar at merge (base `506d91db`, live dev `fa450d30` at this review; the merge is textually clean).
- Merge only with explicit maintainer authorization, then containment, then the bench flash and soak (#661 criterion 5).

## Receipts

Paths are relative to this packet, and host paths inside the receipts are rewritten to `$PACKET`, `$CLONE`, `$TOOLS`, `$HOSTPATH` and `$HOME`. Every published file is listed in `MANIFEST.sha256`.

**Portable scripts:**
- `run_gates.sh <repo> <out>`: the 17 light consumer gates in parallel, one log and rc each.
- `probe_36b.py <clone> <scratch> <out>`: gate 36b control plus five mutants, each in a disposable worktree.
- `probe_tops.sh <clone> <scratch> <out>`: tops self-test control plus two mutants.
- `compare_builder_outputs.sh <clone> <scratch> <out> <base> <head>`: all builder outputs and packed images at two revisions.
- `run_candidate_gptp.sh <clone> <worktree> <log> <head> <dev>`: candidate merge and physical gPTP leg.
- `ports_delta.py <old> <new>`: processor top port and parameter delta.

**Receipts:**
- `receipts/patch-equivalence.txt`: focus 1.
- `receipts/rom-digests.txt` and `receipts/xvlog-decl-order.txt`: focus 2.
- `receipts/baseline-diff.txt`, `receipts/gate-check-baseline.log` and `receipts/gate-selftest.log`: focus 3.
- `receipts/candidate-gptp/`: focus 5.
- `receipts/builder-compare/`, `receipts/pp-top-port-delta.txt` and `receipts/pp-top-sv_ports.txt`: focus 6 and F2.
- `receipts/pr-body-vs-published.txt`: F1.
- `receipts/gates-head/`, `receipts/probe-36b/`, `receipts/probe-tops/`, `receipts/head-pp_shadow/` and `receipts/nvm_cosim_*.log`: Tests, RTL and Robustness.
- `receipts/hosted-check-runs.tsv` and `receipts/clone-restore-check.txt`: limits.

R486-1 FINISHED
