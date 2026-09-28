[R366] NEGATIVE - exact head 6c5ca18f12191a252447ec7c7c75363b851f2771

# R366-4: internal independent delta review of PR #603 (issue #602), merge-dev round

- **Head:** `6c5ca18f12191a252447ec7c7c75363b851f2771`, tree `90653220be7a737e3239a56f5621554081c9a8c1`. Source base `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
- **Delta under review:** `6b2ebd1c..6c5ca18f`, three commits:
  - `b2f48e0c`, the merge of dev `0eff6d2e` (after #593 / PR #601);
  - `45e6cf1a`, the `docs/testing/TESTING.md:941-943` rewording;
  - `6c5ca18f`, the `REQUIREMENTS.md:281-283` rewording.
- **Reconstructed from the public record, in this order:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - Issue #602: the ruling 5859297355, and assignments 5859299480, 5860151273 and 5861304608. The merge-dev assignment 5866438374. The three [A414] STOPs, with dispositions 5866546855, 5866668156 and 5868109315. [A414] REVIEW READY 5868218878. Issue #387's acceptance list.
  - REQ-VER-06 and TESTING.md 6d, `GM_LOSS_RECOVERY.md`, and the RTL at `milan_datapath.sv:3088-3140`.
  - The diff and its history, then the executable evidence below.
- **Independence:** the verdict, finding and ledger were written into this report first. Only then did I read the prior public review findings on this PR, which are resolved below.
- **Read-only inputs:** my round-3 packet and the public `review-evidence/602-r1` tree at `1dab2e7c`, which holds the round-1 author packet. Neither was relied on for any result at this head.

## Verdict

**NEGATIVE, on one MINOR finding (F1).** The merge itself is correct, and so are both rewordings. However, the merge brings in a current finding page that still states, as the live contract, the PHC-step `mr` and MEDIA_RESET obligation that #602 superseded. That falsifies the round-2 acceptance "at the merge head, no current document says that a PHC-only step or re-base toggles `mr` or counts MEDIA_RESET". It also falls within the widened scope of disposition 5866668156: "every statement in the merged tree that #602 falsifies".

| Focus item | Result |
|---|---|
| (1) The only conflict keeps both lanes' content, and #602 wins wherever they disagree | **MET** |
| (2) The delta is exactly the resolution plus the two rewordings; no other statement in the merged tree is falsified by #602 | Delta **MET**; tree search **NOT MET (F1)** |
| (3) The merged #593 soak rule grades a PHC-only step correctly against #602's RTL | **MET** |
| (4) Every generated artifact equals dev `0eff6d2e`'s | **MET** |

### (1) Conflict resolution: MET

- **The merge reproduces cleanly.** `git merge-tree --write-tree 6b2ebd1c 0eff6d2e` conflicts in one file only, `docs/design/GM_LOSS_RECOVERY.md`. The committed merge tree differs from that automatic merge in that file alone (`receipts/verify-merge.log`).
- **The resolution is the lane's text, byte for byte.** The merge's `GM_LOSS_RECOVERY.md` blob equals `6b2ebd1c`'s.
- **Nothing of dev's is lost.** Dev changed exactly one row of that file: the "Outgoing `mr`" row, `0eff6d2e:docs/design/GM_LOSS_RECOVERY.md:155`. That row's only new content was a pointer to the #602 ruling, plus "The current image still toggles ... until #602's RTL change lands". #602 falsifies the second part. The two other conflicted rows, MEDIA_RESET and pending-step, are unchanged from base on dev's side. So taking #602's rows drops only pre-#602 text.
- **#593's soak rule is intact.** Its mr/tu soak rule and two-sided resolution model live outside the conflicted file, and they stay exactly as merged:
  - REQ-VER-06 at `REQUIREMENTS.md:262-310`;
  - TESTING.md 6d at `docs/testing/TESTING.md:914-1000`;
  - `tb/tools/torture_campaign.py`, `tb/tools/torture_release_mutants.py`, `tests/features/torture_campaign_plan.feature` and `tests/steps/torture_release_steps.py`.
  - All four soak files are byte-identical to dev (`receipts/verify-merge.log`).

### (2) Delta and tree search: delta MET; tree search NOT MET (F1)

- **The delta is exactly the merge plus the two rewordings** (`verify_merge.py`, 0 failed assertions):
  - After the merge, only `REQUIREMENTS.md` and `docs/testing/TESTING.md` change. Each commit is one hunk that replaces the same three stale lines with the same three post-#602 lines.
  - Every dev-only path (49) equals dev at the head, and every lane-only path (13) equals `6b2ebd1c`.
  - Five shared paths equal the automatic three-way merge: `CHANGELOG.md`, `BAREMETAL_FIRMWARE.md`, `CI_WORKFLOWS.md`, `milan_datapath.sv` and `test_builder.py`.
  - The head differs from dev only on lane paths. All four gitlinks equal dev, including `protocol-processor 16be6768`.
  - All three commit messages are one line with no trailers.
- **Semantic check of the auto-merged shared files.** In each, dev's hunks are independent of #602:
  - `milan_datapath.sv`: `N_CONTROL_P` on `pp_shadow`, at `:7424-7426`.
  - `test_builder.py`: the clock-contract gate.
  - `BAREMETAL_FIRMWARE.md`: the clock contract and the service budget.
  - `CI_WORKFLOWS.md`: the tap-page reader.
  - `CHANGELOG.md`: the processor-pin entry.
  - The RTL diff from dev to the head is exactly #602's: one OR term removed from `mcr_restart_p_w` (`milan_datapath.sv:3132-3134`), plus comments in `milan_datapath.sv` and `KL_media_clock_restart.sv`.
- **The rewordings are exact to the ruling.** The new lines at `REQUIREMENTS.md:281-283` and `TESTING.md:941-943` read: "A PHC-only re-base leaves `mr` unchanged. The existing `tu` path signals that gPTP discontinuity. It adds no step-only MEDIA_RESET increment."
  - This is the dispositions' "a PHC-only re-base is not an `mr` cause, and `tu` signals it".
  - The MEDIA_RESET sentence is the ruling's own supersession scope: "the step-only MEDIA_RESET that follows from it".
  - Neither rewording contradicts #593's cause list, its "GM change alone" rule or its tu kinds. Each such kind already names "PHC settime/adjtime" as a tu discontinuity.
- **Tree search** (`stale_scan.py`, outside `docs/history/**`):
  - Three strict hits at the head. `GM_LOSS_RECOVERY.md:220`, `BAREMETAL_FIRMWARE.md:1528,1530`, the README and the mutants lines are all consistent with #602.
  - I read all 69 broad co-mention hits in context. Every current statement agrees with #602 except `docs/findings/394_387_E1_SWITCH_CYCLES.md:173` and its dependant `:349`; see F1.
  - That page was added on dev (`fddc58e4`, `6f2cdab6`, both before the ruling) and is absent at `6b2ebd1c`. The same scan at `6b2ebd1c` has no such hit (`receipts/stale-scan-lane.log`).

### (3) The #593 soak rule against #602's RTL at this head: MET

- **Clean gmstep leg** (`make gmstep`, `receipts/gmstep-clean.log`): rc 0, **103 checks, 0 failures**. The checks include:
  - `restart: a PHC-only step leaves outgoing mr unchanged got=0`;
  - `restart: a PHC-only step adds no MEDIA_RESET got=0`;
  - `source control: a real source change toggles mr once got=1`;
  - `CRF control: selected CRF mr propagates exactly once got=1`;
  - tu rising at GM B, and held 224,891 cycles past the step against a quarter tick of 131,072;
  - one counted render re-base, at step pulse +132.
- **Full `gmstep_mutants.py --all` inventory, in foreground slices** through the clone's own `run_control` (`gmstep_chunk.py`): **2 clean legs pass and all 20 controls are caught, 22/22.**
  - The receipts are `receipts/gmstep-campaign-*.log`.
  - Control 3, the restored re-base term, breaks exactly the two PHC-only checks.
  - Control 19, suppression, breaks only the coincident check.
  - Controls 14-18, the option-off settime and adjtime causes including the 16- and 256-cycle delays, break exactly their named checks.
- **The option-off eight-channel leg** (`make ax1x1`): 231 checks, 0 failures. All three `CLKV ... (#602)` checks pass.
- **tkdiag:** 96/0, with all four restart-engine mutants caught (`receipts/tkdiag.log`).
- **Soak self-tests at the head** (the #593 oracles as merged):
  - `torture_campaign.py --self-test`: 78 tests OK.
  - `torture_release_mutants.py`: 132 mutations killed, source unchanged.
  - The behave feature `torture_campaign_plan.feature`: 87 scenarios passed.
- **The oracle graded against the leg's own timeline** (`soak_phc_probe.py`, `receipts/soak-phc-probe.log`, 7/7 as expected). The probe takes the GM edge, the step, tu rise and fall, and the talker interval from the clean log. It maps compressed time by the leg's quarter tick = 0.25 s, then calls the merged `check_release_mr` and `check_release_tu_history`:

| Case | Result |
|---|---|
| Post-#602 wire (constant `mr`, flat MEDIA_RESET) | PASS |
| The same, with a PHC or GM record offered as a cause | PASS; the record is ignored |
| Pre-#602 wire (one toggle 116 cycles after the step, +1 MEDIA_RESET, only PHC and GM recorded) | FAIL, "mr toggle without a recorded media-clock cause" |
| That toggle, excused by a genuine CRF `mr` toggle | PASS |
| tu, with the PHC step recorded as a discontinuity | PASS |
| tu, with the GM edge only | FAIL: the clear is 0.734 s after the edge, above 0.5 s |
| tu, with no recorded discontinuity | FAIL |

  So at this head the merged rule passes a PHC-only step, which leaves `mr` and MEDIA_RESET alone. It needs the step recorded as a tu discontinuity, exactly as REQ-VER-06 lists it, and it would still reject the pre-#602 toggle.

### (4) Generated artifacts: MET

- **Regenerated at both commits** (`regen_compare.py`, `receipts/regen-compare.log`). I exported `git archive` trees at dev `0eff6d2e` and at the head, with both processors exported at their identical pins. I then ran `endstation_builder.py` for all five configurations.
  - **50/50 emitted artifacts are byte-identical.**
  - Each emitted `adp_shape_defaults.svh` equals the committed copy at the head.
- **All 10 committed generated files equal dev's** (`configs/generated/**`, `hdl/common/gen/**`; `receipts/verify-merge.log`).

## Finding

### F1 - MINOR - Conformance, Docs - `docs/findings/394_387_E1_SWITCH_CYCLES.md:165-173,349` - a current finding still states the superseded PHC-step `mr` / MEDIA_RESET contract

- **Requirement/evidence:**
  - At the head, lines 165-173 say that "#387 item 2 records the media re-base contract" and that "The contract requires one counted event per step". The page links that contract to `GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step`. It then says: "One `mr` toggle and one MEDIA_RESET record that event."
  - Line 349 then says that the pending #387 acceptance-4 measurement "must observe the step's counted media event".
  - The linked authority now says the opposite: "It signals `tu`, without changing `mr` or MEDIA_RESET" (`GM_LOSS_RECOVERY.md:142-150`). The #602 ruling 5859297355 supersedes exactly that obligation.
  - `docs/findings/README.md:3-4` defines the directory as "current hardware findings that still inform the shipping Milan v1.2 design". So this is a current document, not history.
  - Two published requirements are unmet:
    - the round-2 acceptance (5860151273 item 1): "at the merge head, no current document says that a PHC-only step or re-base toggles `mr` or counts MEDIA_RESET", with every stale hit outside `docs/history/**`;
    - the widened scope of disposition 5866668156.
  - The page came from dev. It was written on 2026-09-27, before the ruling, and is absent at `6b2ebd1c`. So no earlier round could have seen it. The manager's search at `45e6cf1a` found only `REQUIREMENTS.md`.
  - Evidence: `receipts/f1_evidence.txt`, `receipts/stale-scan.log` and `receipts/stale-scan-lane.log`.
- **Impact:**
  - #387 acceptance 4 is still open, and this page is the guidance for it.
  - A bench run that follows the page on the post-#602 image would look for an `mr` toggle and a MEDIA_RESET increment that the RTL correctly no longer produces. It could therefore grade a correct image as missing its "counted media event".
  - Under the merged #593 soak rule, such a toggle would itself be an uncaused-toggle FAIL.
  - Once merged, the page contradicts the contract it links to.
- **Required change:** at the merge head, the page no longer presents the PHC-step `mr` toggle and MEDIA_RESET as the current contract. One way is to mark lines 165-173 as the contract of the measured pre-#602 image, with a pointer to the #602 ruling. Another is to state line 349's pending measurement in post-#602 terms: the counted render re-base and `tu`, with `mr` and MEDIA_RESET unchanged by a PHC-only step. Either way, the dated measurements stay as they are. If the manager instead rules that dated findings are exempt, that exemption needs a public disposition that names this page.
- **Verification:**
  - Re-run `stale_scan.py <clone> <new head>`. No strict hit, and no broad hit outside `docs/history/**`, may present a PHC-only step as toggling `mr` or counting MEDIA_RESET.
  - `check_em_dash --base 6d5ebd73`, `docs_check`, `check_doc_style`, `gen_toc --check` and `check_doc_paths` must stay rc 0.
  - The finding's measurement tables must be unchanged.

## Observation, not a finding

- `docs/findings/README.md` does not list `394_387_E1_SWITCH_CYCLES.md`, although it is described as the index of current findings. This came from dev and does not concern #602, so it belongs in a separate Issue if the manager wants it tracked.

## Prior public findings on this PR, resolved or retained at this head

Merge ancestry proves this table (`verify_merge.py`):

- Every lane-only file those findings concerned is byte-identical to `6b2ebd1c`.
- The shared files keep the fixed text at this head: `TESTING.md:273` ("fifteen gmstep controls and five option-off controls"); `BAREMETAL_FIRMWARE.md:1475,1477`, which moved from `:1469,1471` by dev's insertions; and the CHANGELOG #602 entry.

| Prior finding | Status at `6c5ca18f` | Evidence |
|---|---|---|
| R366-1 F1 (MAJOR, Docs) = R367-1 F1: current documents state the superseded rule | The lane's own documents stay **RESOLVED**. The acceptance's merge-head outcome is **re-opened by a dev-introduced page and tracked as F1** | Stale scan; `receipts/f1_evidence.txt` |
| R366-1 F2 (MINOR) = R367-1 F2: the campaign inventory and harness narratives | **RESOLVED**, still intact | Lane-only files are unchanged; `TESTING.md:273` is intact |
| R366-1 F3 (MINOR): option-off event-relative checks | **RESOLVED**, still intact | Controls 14-18 caught, `ax1x1` 231/0 |
| R366-1 F4 (SUGGESTION) = R367-1 F3: dynamic coincidence | **TAKEN**, still intact | Control 19 caught; the clean coincident checks pass |
| R367-1 F4 (SUGGESTION, RTL): rename control | **Closed** by assignment 5860151273 (area) | Unchanged |
| R366-2 F1 (MINOR): delayed adjtime cause | **RESOLVED**, still intact | Controls 17 and 18 break only the adjtime check |
| R366-2 F2, F3 = R367-2 F2, F3 (SUGGESTIONS) | **TAKEN**, still intact | Lane-only files are unchanged |
| R367-2 F1 (MINOR): firmware gate description | **RESOLVED**, still intact | `BAREMETAL_FIRMWARE.md:1475,1477` |
| R366-3 S1, S2 and R367-3 S1 (SUGGESTIONS): even-toggle adjtime level check; section-order default | **Retained as optional**; not taken | `sim_main.cpp` is unchanged from `6b2ebd1c` |

## Reviewer-owned lens ledger (R366-4)

| Lens | Status | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN (F1)** | Ruling 5859297355 and merge-dev assignment 5866438374, with dispositions 5866546855, 5866668156 and 5868109315, against: the conflict resolution (`GM_LOSS_RECOVERY.md:142-179`), the two rewordings (`REQUIREMENTS.md:280-283`, `TESTING.md:940-943`), the RTL (`milan_datapath.sv:3132-3134`), gmstep 103/0 and the soak probe 7/7. The tree search found F1 (`docs/findings/394_387_E1_SWITCH_CYCLES.md:173,349`). | R366-4 | `6c5ca18f12191a252447ec7c7c75363b851f2771` |
| RTL | CLEAN | The dev-to-head RTL diff is exactly #602's term removal plus comments (`milan_datapath.sv:3094-3134`, `KL_media_clock_restart.sv:60-64,102-109,168-172`). Dev's `pp_shadow` `N_CONTROL_P` hunk (`:7424-7426`) is independent. `lint_rtl.py --check --jobs 8` PASS, 90 <= 90 (`receipts/rtl-lint.log`). tkdiag 96/0 with 4/4 engine mutants. gmstep 103/0 and `ax1x1` 231/0, at the dev processor pin `16be6768`. | R366-4 | `6c5ca18f12191a252447ec7c7c75363b851f2771` |
| Robustness | CLEAN | Coincident CRF plus PHC-step trials (control 19, clean coincident checks). Delayed adjtime causes at 16 and 256 cycles (controls 17, 18). Combined causes (control 16). The talker-stop and holdover controls (10-12). Soak oracle negative paths: pre-#602 toggle, GM-only tu and uncorrelated tu (`receipts/soak-phc-probe.log`). The self-test's NOT RUN and resolution boundaries, 78 OK. | R366-4 | `6c5ca18f12191a252447ec7c7c75363b851f2771` |
| Tests | CLEAN (prior S1/S2 remain optional) | Full `gmstep_mutants.py --all` inventory, 22/22 (`receipts/gmstep-campaign-*.log`). `torture_release_mutants.py`, 132 killed. `torture_campaign.py --self-test`, 78 OK. behave, 87 scenarios. `soak_phc_probe.py`, whose FAIL cases show that the oracle can reject the pre-#602 wire. The soak test files are byte-identical to dev. | R366-4 | `6c5ca18f12191a252447ec7c7c75363b851f2771` |
| Docs | **UNCLEAN (F1)** | `GM_LOSS_RECOVERY.md:142-220`, `REQUIREMENTS.md:250-310`, `TESTING.md:914-1000`, `BAREMETAL_FIRMWARE.md:1473-1478`, `CHANGELOG.md:132-157`, `TIME_SYNC.md:113,354` and `docs/findings/394_387_E1_SWITCH_CYCLES.md` (F1). Stale scan: 3 strict and 69 broad hits read. Docs gates rc 0 with the pinned Markdown environment: `check_em_dash --base 6d5ebd73` (0 findings over 24 pages), `docs_check`, `check_doc_style`, `gen_toc --check`, `check_gptp_docs --with-submodule`, `check_doc_paths`, and `git diff --check 6d5ebd73 HEAD`. | R366-4 | `6c5ca18f12191a252447ec7c7c75363b851f2771` |

## Commands and receipts (all run in the foreground)

- **Receipts.** `run_receipt.py NAME TIMEOUT CWD -- CMD` records the head, command, environment overrides, rc, elapsed time, and the log's size and SHA-256 (`receipts/*.json`, `receipts/*.log`).
- **Tool identity** (`receipts/tools_identity.txt`):
  - The assigned simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` is **absent** on this host.
  - I used a copy of the #602 round-4 manager wrapper instead. Its sha256 is `905795b9...`, and it reports `Verilator 5.050 2026-07-01 rev v5.050`, the project pin (`rtl-fast.yml:18`). The binary's sha256 is `44898b22...`.
  - Builds used `VERILATOR_JOBS=8` and ran sequentially.
- **Merge integrity:** `python3 -B verify_merge.py <clone>`.
- **Tree search:** `python3 -B stale_scan.py <clone> <commit>`, at the head and at `6b2ebd1c`.
- **gmstep:**
  - `make gmstep`;
  - `python3 gmstep_chunk.py <clone> clean`, then `0 5`, `6 11`, `12 16` and `17 19`. These run the clone's unmodified inventory in slices, so that each call stays under the foreground limit.
  - `make ax1x1`, then `make` in `tb/verilator/tkdiag`.
- **Soak:**
  - `torture_campaign.py --self-test`;
  - `torture_release_mutants.py`;
  - `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain`;
  - `soak_phc_probe.py <clone> receipts/gmstep-clean.log`.
- **Artifacts:** `regen_compare.py <clone> scratch/regen`.
- **Lint and docs gates:** as listed in the ledger.
- **Hosted checks at the head** (read-only, at 11:02Z; `receipts/hosted_check_runs_at_head.txt`):
  - Success: rtl-fast, docs-check, docs-check-no-git, wire-accountability, elaborate, full-ci-gate, verilator-lint, yosys-elaboration, Yosys shards 0-3, and Verilator shards 0, 2 and 3.
  - Still in progress: Verilator shards 1 and 4.
  - Not yet emitted when read: the `verilator-suites` and `yosys-portability` aggregates.
  - Skipped by design: Physical gPTP.
- **Clone restoration** (`audit_clone.py`, `receipts/clone-audit.log`, AUDIT CLEAN):
  - I removed only the ignored build products my runs created.
  - HEAD, the tree and the index-written tree equal the reviewed ids.
  - All 942 tracked blobs and modes match.
  - The gitlinks `protocol-processor 16be6768`, `gptp-processor 5dce647a` and `third_party/verilog-axis 48ff7a7e` are at their pins, with no untracked, ignored or modified entry.
  - `external` is uninitialised, as before.

## Real limits

- **Not run, by assignment:**
  - the full `milan_dp` `run`; the builder banks in either compiler mode; the full parent, PP, gPTP and Yosys banks; OOC;
  - act, and the hosted aggregates.
- I relied on the manager's published statement that its builder and native banks passed at this head. I did not re-execute them.
- **The soak probe is a model,** not a capture. It uses recorded evidence derived from the leg's graded outcome and timeline, in compressed time, for one stream. It is not hardware evidence.
- **Nothing here is physical proof:** there was no physical calibration, bench, lwSRP reservation or placed-area measurement. The gmstep leg is compressed time.
- The assigned simulator path was absent. The substitute's identity is recorded above.

## Pending manager duties

- Disposition F1: the fix in the lane, or a public exemption naming the page. Then re-review at the new head.
- Build and gate the final current-dev candidate at the merge turn: source base `6d5ebd73`, live dev `7a7582f0`. That includes any further dev overlap with the recovery, testing or requirements documents, and the candidate banks.
- Accept the exact-head hosted `verilator-suites` and `yosys-portability` aggregates once they are emitted, and run the act replica.
- Obtain the external review for the merge bar, and run post-merge containment.

R366-4 FINISHED
