[R913] NEGATIVE - exact head 507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698

# R913-4: internal review of kebag-logic/milan-fpga PR #992 (issue #991), the sync merge

- Head `507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698`, tree `bb8ac51a1ab36184c9e0fddd6a335473c16a0b4a`.
- It is one merge commit. First parent `30796098` is the pin, the reviewed head (R913-3 POSITIVE, R914-2 POSITIVE at
  `ed7df79c`). Second parent `2509db68` is dev-soft-core, the flip train from PR #988.
- The merge base is `aa30d77f75cd97b3a29878ca0ed68010a7629266`. The PR's base branch is `dev-soft-core`, whose tip
  is still `2509db68` when this review was written.
- Scope: a narrow re-review of the merge only, against the author-r3 packet
  (`review-evidence/lwsrppin-r1/author-r3` at `ea4c94d0`).

## Verdict summary

The merge itself is correct, and this review checked that at the merge's cause.

- Both conflicts keep both sides verbatim.
- The six automatically merged paths are byte-identical to git's own merge of the two parents.
- Every one-sided path equals its own side.
- Every pin site names lwSRP `d1bb4f4e`.
- The gate inventory at the head is exactly the train's inventory plus the pin's two own-LeaveAll arms.
- The firmware image moves against the train only by lwSRP's +60 B of `.text`.

Two MINOR findings make the verdict NEGATIVE. Neither is a defect in the merged code:

- **F1** (Conformance, RTL, Tests): issue #991's acceptance criterion 2 names the CPU budget harness. Every firmware
  ELF changed at this head, against both parents. Both earlier harness verdicts were measured on images this head
  replaces, and none is shown on the merged image.
- **F2** (Docs): the PR body was last edited before the merge existed. It still says, "at this head", that the
  images are byte-identical and that round 2's route stands. Both are false at `507bce7f`.

## How the task was reconstructed

1. I read AGENTS.md, issue #991 (body only; it has no comments), the PR #992 manager start comment for this round,
   and the author-r3 packet.
2. I made an independent pass over `git diff aa30d77f..507bce7f` and over each parent, starting from the merge's
   cause.
3. Only after that pass did I read the prior public findings on PR #992, from R913-1/2/3 and R914-1/2. Each is
   resolved or retained below.

Probes ran in this clone and in disposable scratch trees. The clone was restored and checked afterwards
(`receipts/restore-check.txt`).

## Evidence produced by this round

| Check | Result | Receipt |
|---|---|---|
| Packet integrity | 131 of 131 published files match the publisher's `MANIFEST.json` `published_sha256`. 14 are path-redacted; for each, `original_sha256` begins with the author's `INDEX.md` prefix and size. The 117 others match `INDEX.md` directly. Read alone, `INDEX.md` shows 14 mismatches, all of them those redacted files | `receipts/manifest-verify.txt`, `receipts/index-verify.txt`; scripts `verify_manifest.py`, `verify_index.py` |
| Merge reproduction | 18 pin paths, 145 train paths, 8 changed by both. Every one-sided path equals its own side. No path changed that neither side changed. `git merge-tree` (git 2.56.1) of the two parents conflicts on exactly `srp_arms.py` and `test_ctrl_firmware.py`, and the other six both-changed paths are byte-identical to the head. Gitlinks equal the pin's; they differ from the train's only in `third_party/lwSRP` (`08ee86e8` -> `d1bb4f4e`). The message is one line with no trailers | `receipts/merge-reproduction.txt`; script `merge_checks.sh` |
| Conflict resolutions | `srp_arms.py:119-135`: the pin's `own_leaveall_arms`, then the train's `LINK_PASS` and `link_pass_arms`, all verbatim. `test_ctrl_firmware.py:220-221`: both `outcomes.extend` calls, before `mbx_entity_arms`. `test_ctrl_firmware.py:77-87`: both clauses of the `srp` entry, re-wrapped and with unchanged words | `receipts/merge-reproduction.txt` (diff of the conflicted merge against the head) |
| Gate inventory | Head: 2,005 live invocations, shards [98, 845, 399, 663], equal to the packet. Train `2509db68`: 2,003. Pin `30796098`: 1,858. Head minus train is exactly the two `srp_own_leaveall.cpp` arms, and train minus head is empty. Nothing at the head is in neither parent. Pin minus head is `control:plat-phy-boot-restart-dropped`, which the train removed on purpose in `1d8bcfa2` (#972); the merge keeps that removal | `receipts/shards-*.txt`, `receipts/census/*.json`, `receipts/census-compare.txt`; script `census_compare.py` |
| The merged SRP arms at the head | `srp_own_leaveall` 8x8/1if 44 of 44 and 1x1/1if 44 of 44; `srp_link_pass` 1x1/1if 9 of 9 and 8x8/1if 9 of 9. Run through the gate's own `Tree`, `arm_srp` and lwSRP pin check (`d1bb4f4e`, clean) | `receipts/merged-srp-arms.log`; script `run_merged_srp_arms.py` |
| `twin_mrp.py --selftest` | `OK (11 checks)`, rc 0 | `receipts/gates/twin_mrp-selftest.log` |
| Budget model | `load_grade.py --check` PASS, `flip_grade.py --check` PASS at 1x1/1if and at 8x8/1if (8x8/1if: `CTRL_LOOP_TX_MS` 77 against 76.86). The output is byte-identical to the train's at `2509db68`. The model reads tsn-c-stack headers only, so nothing the pin changed | `receipts/gates/{load_grade-check,flip-*}.log`, `receipts/gates/train-2509db68-*.log`, `receipts/gates/budget-model-vs-train.txt` |
| Docs and Python gates | `docs_check.py`: 0 findings over 223 md files. `check_py_idiom.py`: PASS. `py_compile` of both resolved files: rc 0. `check_em_dash.py` could not run here (rc 2, the pinned renderer is not installed; see limits) | `receipts/gates/` |
| Image delta (packet, recomputed) | Against `2509db68`, the only non-zero section delta in all 8 ELFs is `.text` +60, with `mrp_mad.o` going from 13,155 to 13,219. ROM = `.text + .rodata + .data` rounded up to 8 B gives 127,568 / 129,352 / 141,680 / 143,432, matching the packet's +56/+56/+64/+64 exactly | packet `receipts/ledger/image-deltas.txt`, `image-hashes.txt` |
| Routed 8x8/1if (packet) | Post-route LUTs 45,958 at the merge and 45,982 at `2509db68`, so -24 (bound +50). FF, RAMB36/18, tiles and DSP are equal. Worst WNS +0.038 and worst WHS +0.036 at every corner, 0 failing endpoints, 0 routing errors. #818 floor met. Merge-side identity: repo `507bce7f`, lwSRP `d1bb4f4e` | packet `receipts/route/{head,base}/summary.txt`, `baseline_utilization.rpt`, `fw-identity.txt`, `hier-delta.txt` |
| Firmware shards (packet) | 4 of 4 rc 0 at `507bce7f`. Shard 0's log has `[ok] arm` lines for both `srp_own_leaveall` arms and both `srp_link_pass` arms (`gate-0.log:499-511`). 844 of 844 mutants caught. The pin controls name `d1bb4f4e` | packet `receipts/firmware/` |
| Stale pin strings | `08ee86e` survives only at `ci/image/exec-audit-receipt.json:4184` and `docs/design/SPLIT_CONTROL_MEMORY.md:509`. Both are measurement records and are byte-for-byte present at the base and at both parents. `LWSRP_REV` is `d1bb4f4e` (`sw/firmware/ctrl/test/ctrl_arms.py:438`) | this review's `git grep` (recorded in this report) |
| Hosted contexts at the exact head (snapshot) | 13 success, 1 skipped (Physical gPTP, nightly/manual), 39 queued or in progress, 0 failed. The manager owns acceptance | `receipts/hosted-checks-snapshot.tsv` |

## Findings

### F1 - MINOR - Conformance, RTL, Tests - issue #991 acceptance criterion 2 ("... harness ... pass"); PR #992 body `:30`; packet `HANDOFF-r3.md` note 5

- **Authority and evidence:**
  - Issue #991 AC2 requires that "the firmware gate, twin and plants, load and flip grades, harness and docs gates
    pass".
  - The PR body (`:30`) says the harness rows "stand from `402834ac`" because "the firmware ELFs ... are
    byte-identical to the previous head's".
  - At this head that premise is false. Every `ctrl_app.elf` changed against both parents, and against the pin the
    8x8 AEM and NVM images changed too (packet `receipts/ledger/image-hashes.txt`: 8 of 8 ELFs `CHANGED CHANGED`).
  - The packet says the harness was not re-run (`HANDOFF-r3.md` note 5). The pin's harness ran at `402834ac`, on an
    image without the train's firmware. Any train-side harness result was on an image without the lwSRP fix.
  - Under AGENTS.md section 7 and the owner's rule for later rounds, a verdict does not carry once the delta changes
    what it depends on. The packet applies that rule to the route ("re-shown because the image changed"), and the
    harness depends on the same image.
  - The budget model and the routed condition were re-shown or carry (see the evidence table). The harness is the
    one AC2 gate with neither an exact-head result nor a public carry decision.
- **Impact:**
  - The per-pass share is THE SHARE: 200,000 cycles, with the longest 8x8/1if pass at 163,158 at the pin. Neither
    it nor the MRPDU and own-LeaveAll probe budgets is shown for the image that lands.
  - The lwSRP fix now sends the Lv for a withdrawal after the own LeaveAll that `08ee86e8` never sent. That is new
    transmit traffic, and it now runs under the train's changed SRP transmit path (#956, #973). A plausible
    interaction is therefore unmeasured.
  - The margins make an overrun unlikely, but a rule-level carry has not been decided.
- **Required outcome:** one of these two.
  - (a) Harness arm A and `answering-every-port` at 1x1/1if and 8x8/1if (plus `answering-later` if the AC is read to
    include it) run on images whose sha256 equals the merge head's mapped images. Those are the ledger's
    `endstation_ax7101_1x1_tdm8/split-soc/mapped/image/ctrl_app.elf` (`79c5326c…`) and
    `endstation_ax7101_8x8/split-soc/mapped/image/ctrl_app.elf` (`eed56acc…`). They are graded as in round 1, and
    0 passes may exceed THE SHARE.
  - (b) A public owner or maintainer decision on #991 or #992 that the harness criterion carries for the composed
    image. It must name the exact-head harness evidence it carries from (the pin's `402834ac` and the train's own
    head), and why.
- **Verification:** the published `grade-*.txt` and `times.txt` show the image identity, rc 0 and 0 over THE SHARE.
  If (b) is chosen, the decision comment is linked from the PR.

### F2 - MINOR - Docs - PR #992 body (last edited 2026-11-24T05:49:41Z, before the merge commit): `:28-30`, the gate rows `:39-40` and `:51`, and the route paragraph and table `:86-98`

- **Authority and evidence:** (the body as read is `receipts/pr-body-live.md`; its first line is a header, so body line N is file line N+1)
  - AGENTS.md section 6 (`Docs`) requires that the PR contain enough evidence for a cold reviewer.
  - The body does not name the merge, its parents, either conflict resolution, the gates run at `507bce7f`, or the
    image deltas against `2509db68` and `30796098`.
  - Its "Evidence at the head" says the firmware ELFs are byte-identical and that the reproduction, firmware gate,
    budget model, harness, ledger and mapping rows "stand from `402834ac`".
  - The `make twin`, `make twin-plants` and `docs.yml` rows say "at this head" for runs made at `ed7df79c`.
  - The route table compares base `aa30d77f` with head `dbba60e6`, and ends "Round 2's images are byte-identical to
    `dbba60e6`'s ..., so the route stands for this head".
  - At `507bce7f` the images changed. The route that holds is the packet's merge-head route against `2509db68`:
    LUT 45,958 against 45,982, WNS +0.038, WHS +0.036.
- **Why MINOR and not RESIDUE:** the body states figures and the basis for a merge condition that are false at this
  head. Fixing it changes a figure claim, not only wording.
- **Impact:** a cold reader of the PR would take the route and harness as standing on byte-identical images. The
  published packet is the only correct record of the merge.
- **Required outcome:**
  - The body describes the sync merge (parents, base, the two conflicts and how both sides were kept).
  - It describes the gates at `507bce7f` and their results, the image deltas against `2509db68` (`.text` +60, ROM
    +56/+64, tiles and SRAM unchanged) and against `30796098` (the train's content), and the merge-head route table.
  - "stand from `402834ac`" and "the route stands for this head" are removed or qualified, along with any harness
    row, to match F1's outcome.
  - This supersedes R913-2-R1 and R913-3 N-R1, which are folded in here.
- **Verification:** reread the body against `git log aa30d77f..507bce7f` and the author-r3 packet.

### R1 - RESIDUE - Docs - `sw/firmware/ctrl/test/test_ctrl_firmware.py:81-82` (R913-2-R2, retained)

- The merge re-wrapped this entry but kept its words: "a Listener withdrawn 5 to 200 ms after the board's own
  LeaveAll sent as Lv within 240 ms". The sentence still parses ambiguously.
- **Exact fix:** "... after the board's own LeaveAll is sent as Lv within 240 ms ...", re-wrapped to the entry's
  column.
- This is wording only. No arm, count or claim changes.

### S1 - SUGGESTION - Tests - `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:137-157`, `sw/firmware/ctrl/test/test_ctrl_firmware.py:199-222`

- The shard proof builds its expected inventory from the same `run_suites`, so it cannot see a suite call that a
  resolution drops.
- Nothing in the gate requires each `srp_*.cpp` under `sw/firmware/ctrl/test` to be named by at least one arm. A
  search for such a guard found none.
- This merge kept both families, as `receipts/census-compare.txt` shows, but only an external comparison shows it.
- **Optional:** add an inventory check that each SRP suite file is run by at least one live arm.
- A mutation probe that drops the call was planned but not run in this session. The claim rests on reading the code.

### S2 - SUGGESTION - Tests - `sw/firmware/ctrl/test/test_ctrl_firmware.py:279-300` (`coverage()`)

- The gcov run includes the talker and listener arms but neither `own_leaveall_arms` nor `link_pass_arms`.
- Both sides left it this way, so it is not a merge defect.
- **Optional:** include both families so that the coverage census reaches the new LeaveAll and link-pass paths.

### Notes (no action needed on the PR)

- **N1.** The packet's own text is stale about the push. `REVIEW-READY.md:3-4` and `receipts/INDEX.md:3` say the
  merge is "local, not pushed", and it is now the published PR head. These are historical receipts and are recorded
  only for the reader.
- **N2.** In the published `receipts/tools/penv.sh`, the publisher's path redaction cut a path mid-component
  (`SDK=/data-2/milan/tmp/s12b-a783<home-path>`). The manifest records it as redacted, so integrity holds. This is
  for the publication tooling only.
- **N3.** The packet's merge check (`merge-checks.txt`, sorted +/- lines) is weaker than a reproduction. This round
  adds the `git merge-tree` reproduction, which is byte-exact for all six automatically merged paths.

## Prior public findings at this head

| Finding | Status at `507bce7f` | Evidence |
|---|---|---|
| R913-1-F1 (MINOR, Tests) and R914-1-F1 (MINOR, Tests and Docs) | **RESOLVED**, still | `tb/verilator/milan_dp/twin_mrp.py` is a pin-only path and equals the pin's blob (`receipts/merge-reproduction.txt`). The self-test prints `OK (11 checks)` at the head (`receipts/gates/twin_mrp-selftest.log`) |
| R913-1-S1 (SUGGESTION, Docs) | **TAKEN**, still | The `srp` docstring entry keeps the own-LeaveAll clause verbatim (`test_ctrl_firmware.py:79-85`) |
| R913-2-F1 (MINOR, Docs) | **RESOLVED**, still | `tb/verilator/milan_dp/README.md:1408-1410` keeps "holds the txLA! case with the Registrar MT, and the txLAF! case with the Registrar MT and with it IN". The README is byte-identical to git's automatic merge |
| R913-2-R1 (RESIDUE, Docs): the PR body's routed-image paragraph | **Superseded by F2** | At this head the sentence is false, not only badly worded |
| R913-2-R2 (RESIDUE, Docs): the docstring's "sent as Lv" | **RETAINED** as R1 | `test_ctrl_firmware.py:81-82` |
| R913-2-S1 (SUGGESTION): `OK (0 checks)` on the failing zero-check exit | open, optional | `twin_mrp.py:463-465` unchanged |
| R913-2-S2 (SUGGESTION, Tests): Table 10-4's txLA! Registrar row is uncovered | open, optional | `twin_mrp.py` unchanged |
| R913-3 N-R1 (RESIDUE, Docs): PR body not updated for `30796098` | **Superseded by F2** | The body is still the 05:49Z text |
| R913-3 N-S1 (SUGGESTION, Docs): the README list omits `mt-at-own-leaveall` | open, optional | `README.md:1408-1411` unchanged in words |
| R914-2 (POSITIVE at `ed7df79c`, no findings) | stands for what it examined | The merge changes none of the pin's files beyond the resolved test files, and those are covered above |

## Comment rule (source comments in the delta)

- The delta against each parent is the other side's reviewed content, and the hand-resolved lines are both sides'
  words.
- No new lane label, lane name, review round, reviewer ID or issue-comment ID appears in source comments. The
  `#665` ruling citation in the `srp` entry is already present on both sides.

## Lens results

```text
[R913] MINOR Conformance — issue #991 AC2; PR body :30; packet image-hashes.txt — harness not shown on the merged image (F1)
[R913] MINOR RTL — packet image-hashes.txt (8/8 ELFs changed); route/head/summary.txt — the image's CPU-latency effect against THE SHARE is not measured; the route is re-shown and met (F1)
[R913] PASS Robustness — receipts/merged-srp-arms.log (srp_link_pass 9/9 at 1x1/1if and 8x8/1if: link at each phase of a loop pass, behind a full event ring, across a DOWN that elides an UP; srp_own_leaveall 44/44 at both points, including the no-withdrawal leg); packet twin/plants-{1,2}.log (16/16 plants refused, twice) — no input-handling code changes in the merge beyond the reviewed lwSRP fix
[R913] MINOR Tests — issue #991 AC2 harness regression not shown at the head (F1); otherwise clean: receipts/census-compare.txt (inventory = train + 2 own-LeaveAll arms), receipts/merged-srp-arms.log, packet firmware/summary.txt
[R913] MINOR Docs — PR #992 body :28-30, :39-40, :51, :86-98 — stale "this head" figures and route basis (F2); the docs in the tree are clean: receipts/merge-reproduction.txt (6 auto-merged docs = git merge), receipts/gates/docs_check.log
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #991 AC1/AC2; pin sites (`ctrl_arms.py:438`, `SUBMODULES.md:26`, `MAILBOX_SPLIT.md:454`, `sw/firmware/ctrl/README.md:647-649`, `srp/README.md:80-81,729`); gitlink `d1bb4f4e`; `srp_own_leaveall` 44/44 at both points (mine); packet route summary (#818 floor) | R913-4 | `507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698` |
| RTL | UNCLEAN (F1) | merge against train touches no `hdl/` path (`receipts/merge-reproduction.txt`); gitlinks; packet `image-deltas.txt` (recomputed ROM), `route/{head,base}/summary.txt`, `baseline_utilization.rpt`, `hier-delta.txt`, `fw-identity.txt` | R913-4 | `507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698` |
| Robustness | CLEAN | `receipts/merged-srp-arms.log` (link-pass and own-LeaveAll arms, both points); packet `twin/plants-{1,2}.log`, `own-leaveall/summary.txt` | R913-4 | `507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698` |
| Tests | UNCLEAN (F1) | `receipts/census-compare.txt`, `shards-*.txt`; `merged-srp-arms.log`; `gates/twin_mrp-selftest.log`; budget model against the train; packet `firmware/` shards and `.results.txt` | R913-4 | `507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698` |
| Docs | UNCLEAN (F2) | PR #992 body (05:49:41Z edit); the six auto-merged docs; resolved docstring `test_ctrl_firmware.py:77-87`; `gates/docs_check.log`, `py_idiom.log`; packet `docs/summary.txt` | R913-4 | `507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698` |

## Real limits

- **Not re-run by this round.** I did not run the firmware shards, `make twin` or `twin-plants`, `ctrl_boundary`,
  `plat_ledger`, the full `docs.yml` steps, or the route. For those I relied on the packet's receipts, whose
  integrity is verified above, and spot-checked them.
- **Em-dash gate.** `check_em_dash.py` was not run here because its pinned renderer is not installed and shared
  installs are not allowed. The packet reports 0 findings for pushes from both parents.
- **Harness.** The CPU budget harness was not run: one point takes about 3.5 hours. That gap is F1.
- **Mutation probe.** The S1 probe was planned but not run in this session.
- **Parent censuses.** The parent-tree censuses ran in scratch extractions whose submodule directories link to this
  clone's checkouts, which match the head's gitlinks (lwSRP `d1bb4f4e` for both). The inventory does not depend on
  lwSRP's revision.
- **Clone state.** This round's evidence fetch temporarily added partial-clone keys to this clone's local config and
  three packs. Both were removed and the packs deleted. All objects reachable from the head and both parents are
  present (68,977, 0 missing). Index, worktree, modes and the five checked-out gitlinks equal the head
  (`receipts/restore-check.txt`). `external` was never initialized in this clone.
- **No manager source bank** runs at this head, and none is claimed or inferred. Physical calibration was NOT RUN.
  Field skips are not hardware proof.
- **Hosted contexts** were in progress at the snapshot. Their acceptance belongs to the manager.

## Pending manager duties

- Hosted and act acceptance at `507bce7f`. The snapshot had 39 contexts queued or in progress.
- The current-dev merge candidate (builder and native banks) at the merge turn. Live dev `e275d795` has diverged
  from `2509db68`: it carries 4 commits the train lacks, touching `AGENTS.md`, `CONTRIBUTING.md` and
  `docs/testing/CI_WORKFLOWS.md`.
- The F1 route of choice: an exact-image harness run, or a public carry decision.
- Carry R1, and the residue F2 folds in, to the residue checklist once F2 is fixed.
- Publish this report and the files in `MANIFEST.sha256`.

R913-4 FINISHED
