[R701] NEGATIVE - exact head 0052e62e46582b701aa91d879c766b41682bfd3e

# R701-7: internal cleared-context delta review of PR #795 (issue #665, lane S1), merge round

Head `0052e62e46582b701aa91d879c766b41682bfd3e`, tree `9f5a1c62ca3e18e4729b85ab3c7ca86525ff9e40`, branch `665-s1-faces` -> `dev-soft-core`. Merge commit with parents `424b1489` (round 6, R701-6 and R702-6 POSITIVE) and `dev-soft-core` `6660a1a0` (PR #792, lane S2). Source base `e76a755a`.

**Verdict: NEGATIVE.** The textual merge is correct, and S1's own artifacts are byte-identical to the reviewed round-6 head. But the merge brings S2's CPU budget harness (`tb/verilator/ctrl_service_budget/`) into a tree it was never adapted to:

- **F1 (MAJOR).** The harness's 8x8 point is refused by S1's memory planner, both at the image step and at the SoC build.
- **F2 (MINOR).** Arm B no longer applies. The harness's `KL_mbx` instance leaves contract 2.3's 18 face inputs unconnected. The README describes the pre-S1 fixture.

The merge round's gates did not catch either finding, because the harness's only gate (`run.py --self-test`) grades fixed logs and builds nothing. F1 needs a manager decision, because it sits where ruling 6412739248 item 1 meets a harness that came after it. The report also carries one retained RESIDUE and two SUGGESTIONs.

## Scope reconstructed

- **Lane S1 acceptance:** assignment 6409739310. Rulings 6410169666, 6412739248, 6421238472 and 6425357821 apply, with the round-6 assignment 6426858104. R701-6 and R702-6 judged it POSITIVE at `424b1489`.
- **The merge round:** assignment 6447669608.
  1. Merge `origin/dev-soft-core` `6660a1a0` as a merge commit, with no rebase.
  2. Resolve `sw/firmware/ctrl/test/ctrl_configs.py` by keeping both sides, each with its reason. No other change.
  3. Run the named gates, including "S2's harness self-test".
  4. A delta review of the merge resolution follows.
- **The executor's claim:** REVIEW READY 6450366910. The merge differs from `424b1489` only in S2's 36 files and from `6660a1a0` only in S1's files. Every gate it names is rc 0.
- **Judged here:**
  - the merge's structure and its conflict resolution;
  - every semantic interaction between S1's 58 files and S2's 36 files;
  - the published merge-round evidence;
  - the prior findings.
- **Prior verdicts held:** S1's own artifacts are byte-identical to `424b1489`, so R701-6's lens verdicts on them still hold, unless an S2 file reads them. Two S2 files do: the harness reads S1's planner, fixture, `KL_mbx` and AECP sources. That interaction is where F1 and F2 sit.

## Independent pass over the delta

**Merge structure** (`receipts/01_merge_structure.txt`, `receipts/02_ctrl_configs_resolution.txt`)

- Parents are `424b1489` and `6660a1a0`, with merge base `e76a755a`. The subject is one line with no trailers.
- File sets: S1 changes 58 files, S2 changes 36, and the head changes 93. The union equals the head's set. The only overlap is `ctrl_configs.py`.
- `git diff 6660a1a0 0052e62e -- <S2-only files>` is 0 bytes, and so is `git diff 424b1489 0052e62e -- <S1-only files>`. Every file equals the side that changed it, including its mode.
- `ctrl_configs.py`: `git show --remerge-diff` shows the one conflict hunk (`OUTSIDE`, `:176-202`). It was resolved as S1's `census_ports.py` entry followed by S2's comment and five harness entries, both verbatim. S2's `SUITES` entry merged cleanly. Nothing else changed.

**Semantic interactions.** S2's harness uses these S1-changed inputs:

- `ctrl_srp_image.py`, `ctrl_memory.py` and `milan_soc.add_ctrl_memory`: the image and its plan;
- `hdl/milan/mailbox/KL_mbx.sv` and `gen_mailbox.py`: the harness's own `KL_mbx` instance;
- `ctrl_aecp_image.c`: the size fixture its arm B edits;
- `aecp.h` (`AECP_REGISTRATIONS`) and `aecp.c`: the README's citations.

Each was probed through the harness's own code, at the head and at `6660a1a0` as a control:

| Probe (the harness's own code path) | At `6660a1a0` (S2, before S1) | At `0052e62e` (merge) | Receipt |
|---|---|---|---|
| `build.firmware()`, 8x8, two interfaces: `ctrl_srp_image.py --with-aecp --layout split`, no override | builds; plan 56.0 RAMB36 | **REFUSED**, rc 2: "57.5 RAMB36 ... exceeds the 56-RAMB36 budget"; `build.run` raises | `03c`, `03a` |
| `ctrl_memory.plan()` on that ELF, as `split_soc.py:309` -> `milan_soc.add_ctrl_memory` (`milan_soc.py:2807`) calls it | OK, 56.0 | **REFUSED**, 57.5 | `03c`, `03a` |
| `build.firmware()`, 1x1, one interface (control) | n/a | builds, 37.0. The ELF is byte-identical to the author's published 1x1 ELF (`fe939fff...`) | `03b`, `07` |
| `build.variant_fixture('answering-ports')` (arm B) | applies | **FAILS**: "an anchor is not unique in ctrl_aecp_image.c" (`a_avb` was removed) | `04` |
| `build.variant_fixture('shutdown-entry')`, and both `MUTATIONS` controls | apply | apply | `04` |
| `KL_mbx` declared ports against those `split_soc.py`'s instance connects | 35 of 35 | 36 of 112. Unconnected: 18 inputs (`fw_ack_p_i`, the four windows' `*_ans_p_i`/`_tag_i`/`_data_i`, `ctr_chg_*`, `avb_chg_p_i`, `asp_chg_p_i`) and 58 outputs | `05` |
| `run.py --self-test` | n/a | 0 failures, rc 0 (grades `fixture.log` only; builds nothing) | `08a` |

About the control tree:

- It is a local clone of this review clone, checked out at `6660a1a0`.
- The checkouts of `protocol-processor`, `gptp-processor`, `lwSRP`, `tsn-c-stack` and `verilog-axis` were copied in. Each sits at the same gitlink at both heads.
- The tracked tree is therefore the only difference between the two arms.

**The rest of the delta**

- S2's CI edits (`.github/`, `scripts/ci_*`) only pin `runs-on` to `ubuntu-24.04`. They touch no step of S1's jobs and no timeout, including `publication-census` (45 min).
- At the head these all pass:
  - `gen_mailbox.py --check`: 0 findings;
  - `docs_check.py`: 0 findings in 211 md files;
  - `check_doc_style.py`: OK (`08b`-`08d`).
- The merge adds no source comment of its own.
- The comment-rule scan (`09`) finds no new reviewer ID, round or comment ID in the merge's resolution hunk. The only lane label is the one S1 below names, which is in a reason string, not a comment.

## Findings

### R701-7-F1 - MAJOR - Conformance, Tests, Docs - the merged CPU budget harness cannot build its 8x8 point

- **Where:**
  - `tb/verilator/ctrl_service_budget/build.py:137-143`: the image, with no `--ledgered-point`;
  - `tb/verilator/ctrl_service_budget/split_soc.py:309`: `add_ctrl_memory`, with no override;
  - `README.md:36-37` and `:40-41`: the 8x8 point, with two interfaces;
  - `sw/litex/ctrl_memory.py:196-207`.
- **Authority and evidence:**
  - Ruling 6412739248 item 1 says the over-budget point's override is "used only by that point's measurement; the default build path stays refusing". Ruling 6425357821 set that point at 57.5.
  - `ctrl_memory.py:197-198` says "the SoC build names none".
  - S2's harness is a measurement of exactly that point (8x8, two interfaces). It builds the image without the override and the SoC through the default `add_ctrl_memory`.
  - At `6660a1a0` both steps pass at 56.0 (`03c`). At the merge head both are refused at 57.5 (`03a`), so `run.py --point 8x8`, and with it every 8x8 group and control, stops at its first build step.
  - The merge round's gates cannot see this. The only harness gate named, `run.py --self-test`, builds nothing (`08a`; the author's `gates/harness-selftest.txt` ran in 6 s).
  - The PR body (`:152`) reports that self-test as the harness's evidence.
  - No public ruling decides whether the harness's 8x8 SoC may name the override. The rulings predate the harness's merge.
- **Impact:**
  - Once this PR merges, `dev-soft-core` carries a #665 measurement harness that refuses one of its two documented points.
  - S2's recorded 8x8 figures (README "Results", columns A8, B8 and S8) can no longer be reproduced on the branch.
  - Lanes still working on the harness (S2b, on S2c) inherit the refusal when they next sync with `dev-soft-core`.
  - The tree states two contradictory things: "the SoC build names none" and the harness's command for the 8x8 SoC.
- **Required outcome:**
  - The manager publicly decides whether the harness's 8x8 two-interface build is "that point's measurement". If it is, the harness may name `8x8-two-interfaces` for its image and its SoC plan, and the planner's test still proves the default SoC path refuses. If it is not, the harness states the point as unavailable until S14, with the cause, and its README and the PR body say so.
  - At the candidate head, every command the harness README documents either runs past its build step or is refused by name, as documented.
  - The PR body's evidence for the harness says what the self-test does not cover.
  - Per AGENTS.md section 7, moving this to another Issue does not resolve it while the tree still carries the contradiction.
- **Verification:**
  - At 8x8 with two interfaces, `scripts/probe_harness_8x8.py <checkout> <out> endstation_ax7101_8x8 2` reaches `FIRMWARE-STEP OK`, and the SoC plan the harness uses accepts the image. Otherwise, the documented refusal is what the README states.
  - `test_ctrl_memory.py` still refuses the ledgered image through the default `add_ctrl_memory`.
  - At 8x8, `run.py --point 8x8 --build-dir <dir>` gets past `image.log` and the SoC export.

### R701-7-F2 - MINOR - RTL, Tests, Docs - the merged harness is not adapted to contract 2.3 or to S1's size fixture

- **Where:**
  - `tb/verilator/ctrl_service_budget/build.py:66-77`: the `answering-ports` anchors;
  - `split_soc.py:182-193`: the `KL_mbx` instance;
  - `README.md:65`, `:81`, `:322` and `:492-493`: the claims about the fixture's ports and hookup;
  - `README.md:476` and `:492`: line citations.
- **Evidence:**
  1. **Arm B fails.** S1 replaced the fixture's `a_stream`, `a_avb`, `a_counters`, `a_changed` and `a_format` with `aecp_face_init(&image_face, ...)` (`ctrl_aecp_image.c`, `11`). Arm B's anchors are gone, so `variant_fixture('answering-ports')` raises (`04`). The README's documented arm-B command fails at its first step.
  2. **Unconnected face inputs.** The harness's `KL_mbx` instance connects 36 of the 112 ports at the merge head (`05`). It leaves the 18 face inputs contract 2.3 added unconnected: the commit acknowledgement `fw_ack_p_i`, the window answers and the face events.
     - `milan_soc.CtrlMailbox` ties those same inputs idle by name (`milan_soc.py`, `ctrl_mailbox_face_ports`).
     - `README.md:81` still calls the instance "CtrlMailbox's hookup".
     - The harness compiles with `-Wno-fatal` (`build.py:337`), so this passes silently as a pin warning.
     - Static comparison only: no model was built here.
  3. **The README describes the old fixture.**
     - `README.md:65`, `:322` and `:493` say the fixture's observation callbacks "always report unavailable". At the merge head they are the face block's window reads, which in the harness are never answered.
     - The arm-A results and findings describe the pre-S1 firmware, but the README does not name the firmware head they were measured at.
     - The citations `aecp.c:58`, `aecp_commands.c:555` and `aecp.c:461-495` point at other code at the head. The cited `memset` lines are now `aecp.c:66` and `aecp_commands.c:593`, and `retry_at = a->now + 1u` is now `aecp.c:569` (`11`).
- **Impact:**
  - One documented arm cannot run.
  - The formal arm A at 1x1 now measures S1's face-backed firmware against a mailbox instance whose answers and acknowledgements float. That is not the documented hookup, and it is not tied idle by name the way the product's `CtrlMailbox` is.
  - A reader of the merged README is told the firmware behaves as it did before S1.
  - This is test code and documentation, not shipping RTL. That is why it is MINOR rather than MAJOR.
- **Required outcome:**
  - The harness's `KL_mbx` instance connects every contract 2.3 port the way `CtrlMailbox` does (outputs named, inputs idle), or the README states the difference and why.
  - Arm B is either re-anchored to the face-block observation or withdrawn by decision.
  - The README states which firmware head its figures were measured at. Its claims about the fixture and its line citations match the merge head.
  - The manager may assign this together with F1.
- **Verification:**
  - `scripts/probe_harness_ports.py` reports no unconnected input.
  - `scripts/probe_harness_anchors.py` reports `VARIANT answering-ports APPLIES`, or the arm is gone from both `build.py` and the README.
  - The README's citations resolve at the head.

### R701-7-W1 - RESIDUE - Docs - PR #795 body, "How to validate" (`:141`). This retains R701-6-W1, which was not applied.

- **Text:** "Rounds 5 and 6 and the merge change no file the following gates read, so their round-4 and round-5 receipts stand".
- **Evidence:** Round 5 (`0cce152582`) changed a comment in `sw/mailbox/mailbox.yaml:447-449`, which `gen_mailbox.py` reads. No generated byte moved: `gen_mailbox.py --check` reports 0 findings at this head (`08b`).
- **Exact fix:** "Rounds 5 and 6 and the merge change no input of the following gates except a comment in `sw/mailbox/mailbox.yaml` (round 5), which changes no generated byte (`gen_mailbox.py --check`: 0 findings), so their round-4 and round-5 receipts stand: ..."

### SUGGESTIONs (optional)

- **R701-7-S1 - Docs - `sw/firmware/ctrl/test/ctrl_configs.py:180`.** S1's reason string reads "(#665 S1)". That is a lane label in classification text the gate prints, inside the hunk this merge resolved. S2's adjacent entries cite "(#665)" alone. Runtime strings are outside the comment rule (R702-5-S3's precedent), so this is optional. Write "(#665)".
- **R701-7-S2 - Tests - the merge-round gate list.** A merge that brings in a harness reading the other side's sources should include at least that harness's build step at each documented point, not only its self-test. `scripts/probe_harness_8x8.py` and `probe_harness_anchors.py` here take under two minutes in total.

## Prior findings at this head

S1's files are byte-identical to `424b1489` (`01`). So no finding that was resolved at `424b1489` is reopened, and no carried suggestion has changed.

| Prior item | Disposition at `0052e62e` |
|---|---|
| R701-5-F1, R702-5-F1, F2, F3 (MINOR; resolved at `424b1489`) | **Remain resolved.** Their causes and tests are in S1's files, which are unchanged by the merge. The author's four-shard firmware self-test at this head catches 137 of 137 AECP plants (shard 2), as at `424b1489`. |
| R701-4 and R702-4 findings, and earlier ones | **Remain resolved**, as R701-6 recorded. The merge does not touch their causes. |
| R701-6-W1 (RESIDUE, PR body) | **Retained** as R701-7-W1. The PR body `:141` still carries the wording, now with "and the merge". |
| R701-6-S1 to S4 (SUGGESTION) | Carried, unchanged (`aecp.c`, `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md:188`, `test_aecp.cpp:950`). |
| R701-5-S1, S2, S4, R701-4-S1, R701-4-S2 bullets 1-2 (SUGGESTION) | Carried, unchanged. |
| R702-6 SG1 to SG4 (SUGGESTION) | Carried, unchanged. `coverage.ratchet` and the docs they name are S1 files that the merge leaves unchanged. |

## Published evidence verified

The evidence commit is `6df78cedad42eb9c38b1501dc83755daa49773a4`, `review-evidence/665s1-r1/author-r7/` (sparse fetch, `07`).

- **Integrity.** All 146 files match `MANIFEST.json` `published_sha256`. None is unlisted and none is missing. Two are path-redacted. All 135 rows of `receipts/INDEX.md` match their byte length and sha256. The commit has no signature (`%G?` = N), so integrity rests on the manifest and the index.
- **Head.** `fw/head.txt` and `gates/head.txt` read `0052e62e46582b701aa91d879c766b41682bfd3e`.
- **Spot-checked receipts:**
  - the four firmware shards: `test_ctrl_firmware: PASS`, each rc 0;
  - `firmware-boundary.txt`: `ctrl_boundary: PASS`, 2,864 of 3,094 compiled, 0 findings;
  - `harness-selftest.txt`: 0 failures, rc 0, 6 s;
  - `images/elf-sha256.txt`: the 1x1 one-interface ELF, `fe939fff...`, equals the image this review built independently through the harness's own path (`03b`).

## Lens results

```text
[R701] UNCLEAN Conformance - F1 - tb/verilator/ctrl_service_budget/build.py:137-143, split_soc.py:309, sw/litex/ctrl_memory.py:196-207 against rulings 6412739248 item 1 and 6425357821 - the merged tree's measurement of the ledgered point cannot run, and no ruling says whether it may name the override.
[R701] UNCLEAN RTL - F2 - split_soc.py:182-193 against hdl/milan/mailbox/KL_mbx.sv at 0052e62e (receipts/05) - the harness instance leaves 18 contract 2.3 inputs unconnected, which CtrlMailbox ties idle.
[R701] PASS Robustness - receipts/01, 03a-03c; S1's files byte-identical to 424b1489; the author's four ELFs byte-identical to 424b1489's - the merge changes no firmware, RTL or planner behaviour. The 8x8 refusal is the planner's ruled behaviour (it refuses by name and builds nothing), not a robustness defect, and the 1x1 control builds. S1's malformed, boundary, reset, expiry and late-acknowledgement paths are unchanged from R701-6's covering probes.
[R701] UNCLEAN Tests - F1, F2 - receipts/03a, 04, 08a; the author's gates/harness-selftest.txt - the merged harness fails at its 8x8 point and in arm B, and the merge gates exercised only its log grader.
[R701] UNCLEAN Docs - F1, F2 - tb/verilator/ctrl_service_budget/README.md:36-41,65,81,322,476,492-493; PR body :141,:152 - the README documents commands that fail and describes the pre-S1 fixture; W1 is RESIDUE.
```

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | merge-round assignment 6447669608; rulings 6412739248 and 6425357821; `ctrl_memory.py:196-207`; harness `build.py:137-143`, `split_soc.py:309`; receipts `01`, `02`, `03a`, `03c` | none at this head (R701-6 covered S1's own scope at `424b1489`) | 0052e62e46582b701aa91d879c766b41682bfd3e (unclean) |
| RTL | UNCLEAN (F2) | `KL_mbx.sv` ports against the harness's `split_soc.py:182-193`; `milan_soc.ctrl_mailbox_face_ports`; receipt `05`; S1's HDL byte-identical to `424b1489` | none at this head | 0052e62e46582b701aa91d879c766b41682bfd3e (unclean) |
| Robustness | CLEAN | receipts `01`, `03a`-`03c`; ELF identity with `424b1489` (author `images/elf-sha256.txt`) and with this review's own 1x1 build; S1's files unchanged | R701-7 | 0052e62e46582b701aa91d879c766b41682bfd3e |
| Tests | UNCLEAN (F1, F2) | harness `build.py`, `run.py --self-test` (`08a`), probes `03a`-`03c`, `04`; author's four firmware shards, boundary and self-test receipts | none at this head | 0052e62e46582b701aa91d879c766b41682bfd3e (unclean) |
| Docs | UNCLEAN (F1, F2; W1 RESIDUE) | harness `README.md`; PR body; `ctrl_configs.py:176-202`; `docs_check.py`, `check_doc_style.py` (`08c`, `08d`) | none at this head | 0052e62e46582b701aa91d879c766b41682bfd3e (unclean) |

S1's own artifacts (census, contract 2.3, `KL_mbx`/`KL_mbx_evt`, `CtrlMailbox`, the face writer, the AECP core, the planner and its tests and docs) are byte-identical to `424b1489`. R701-6's clean coverage of them stands at that ancestor, because nothing in their scope changed between `424b1489` and this head. The unclean lenses above are unclean because of what the merge adds beside them.

## Real limits

- **Harness depth.** The full harness was not run: no SoC export, no CPU netlist, no Verilator model, no simulation. The probes stop at the harness's image step and at the memory plan its SoC export calls. The F2 port finding is a static comparison of declared and connected ports. The pin-warning behaviour was not observed in a build.
- **The control arm** is `6660a1a0`, rebuilt here as a local clone with identical submodule gitlinks. The tracked tree is its only difference from the head.
- **Relied on from the author's exact-head receipts,** verified by manifest and index hashes and not re-run here:
  - the four-shard firmware self-test;
  - `fw_coverage.py --check`;
  - `ctrl_boundary.py` (both partitions);
  - `test_ctrl_nvm.py`;
  - `test_builder.py`, which has gate 11 NOT RUN (no local Arty build report);
  - the linked images at four points;
  - the 69 docs-workflow commands;
  - `behave`;
  - the 64-suite Verilator sweep.
- **Not run:** no full parent, PP, gPTP, Yosys or builder bank; no `KL_mbx` out-of-context build; no Docker or act; no host `act_ci`.
- **Physical calibration NOT RUN.** Field-campaign skips (`tsn_fuzz` without tsn-gen, "Physical gPTP" skipped) are not hardware proof.
- **No manager source bank** exists at this head, and none is claimed or inferred.
- **Hosted checks:** a read-only snapshot at this head (`06`) shows 8 success, 1 skipped ("Physical gPTP") and 38 in progress or queued, including the `firmware-*` jobs, `publication-census`, the Verilator and Yosys shards. It shows no failures. This is not acceptance.
- **Checkout integrity** after the probes (`10`):
  - The index equals HEAD and the worktree equals the index. `write-tree` equals tree `9f5a1c62`.
  - All 1,463 tracked blobs hash to their index entries, with 0 mode mismatches.
  - Five submodules sit clean at their gitlinks. The optional `external` is not initialized.
  - The six `__pycache__` directories this review's probes created were removed. No ignored entry remains.

## Pending manager duties

- Decide F1: may the harness's 8x8 two-interface build name the ledgered override, or is the point unavailable until S14? Assign F1 and F2, here or with the harness's owning lane, and make sure the fix is in the tree before merge (AGENTS.md section 7).
- Accept the exact-head hosted and act results. Most hosted jobs were still running at the snapshot.
- Build and validate the current-dev merge candidate with the builder and native banks, and publish their receipts. The source base is `e76a755a`; live dev is `97aab1d0f28bd753a3e11df6278d5cac54f964dd`. This review does not validate that merge result.
- Carry R701-7-W1 (R701-6-W1) to the residue checklist. S1 and S2 are optional.
- Obtain the external review's verdict at the head that answers F1 and F2. Merge needs two independent positives and the full completion bar.
- Carry the owed items:
  - S14 owes 1.5 tiles at 8x8 with two interfaces before the flip (S13);
  - the placement switch wires the datapath side and closes the undone-value window.
- Issue #665 stays open; this PR must not close it.

R701-7 FINISHED

