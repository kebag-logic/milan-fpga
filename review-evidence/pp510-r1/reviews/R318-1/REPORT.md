[R318] NEGATIVE - exact head b51bc3893b06f4d39be49726c1b8f4ed6c65573d

# R318-1 internal independent review: processor PR #118 (issues #55, #56, #77; parent milan-fpga #510)

- Exact head: `b51bc3893b06f4d39be49726c1b8f4ed6c65573d`, tree `aca3aeea278c88cc1fca5495ea6e74eea6794d35`. The head was verified in the review clone before and after the probes.
- Base `265d6762a58d9d9e545624d6d3f1a34e7006d171`. The authored commit is `05fd9e1b` and the merge of main is `990f9652`.
- Review role: internal reviewer, cleared context, round R318-1.

## Verdict

**NEGATIVE.** One open MINOR finding, R318-1-F1, leaves the Tests and Docs lenses unclean. Conformance, RTL and Robustness are clean.

The substance of the waiver is correct, consistent and well pinned:
- The waiver text matches Milan v1.2.
- No MUST or "implemented" wording remains for either pair.
- F01.5 marks the phantom enables reserved, and `make check` is green.
- M4 fails under every SUCCESS mutant I tried, including a mutant confined to the waived types.
- There is no RTL change.
- The merge of main is git's own automatic merge.

The one defect: a tracked test-evidence paragraph in `tb/pp_top/README.md` was measured before the merge of main. It states check counts that are false at this head.

## Findings

### R318-1-F1: MINOR (Tests, Docs): waiver mutation section states pre-merge check counts as current

- **Where:**
  - `tb/pp_top/README.md:500-501`: "The unmodified `make -C tb/pp_top run` passes **1,966 checks**: 1,946 in the default build … plus 20".
  - `tb/pp_top/README.md:511`: "197 of 1,946 default-build checks fail".
  - `tb/pp_top/README.md:512`: "3 of 1,946 default-build checks fail".
- **Evidence:**
  - At this exact head the unmodified suite gives `7640 checks, 0 failures` for the default build and `7660 checks: 7660 PASS, 0 FAIL` in total (`receipts/01-pp_top-baseline.txt`).
  - The hosted push run at this head independently reports `PASS pp_top (7660 checks: 7660 PASS, 0 FAIL)` (`receipts/11-hosted-push-suites-excerpt.txt`).
  - Reproducing the author's two ROM mutants at this head gives 197 of **7,640** and 3 of **7,640** (`receipts/02-mutant-E_NOTIMPL-success.txt`, `receipts/03-mutant-features_flags-3.txt`).
  - The 1,946 and 1,966 figures are the counts at `05fd9e1`, before main's PR #115 added the GI latency walks (5,568 checks) and other checks. The merge brought those in without any edit to this section.
  - The section names a date but no commit, and it is written in the present tense. The rest of this README's mutation notes quote counts as "measured at N checks", tied to a date or commit. The repository treats stale suite figures as defects (for example, the `nvm_port` figures CI gate and the README's own "re-run a mutation before quoting its blast radius").
- **Authority:**
  - `README.md` "Building and checking": the pin moves only where everything here is green and agrees.
  - `docs/README.md` §6: `make check` must pass, and figures must describe the tree.
  - Assignment item: "the merge of main composes cleanly (tb/pp_top README …)".
- **Impact:**
  - A reader, or the parent pin review, is told the unmodified suite passes 1,966 checks when it passes 7,660.
  - The mutant blast radius is quoted against the wrong denominator.
  - The failing counts themselves (197, 3, and M4's 10) are still right, so this does not weaken the pin. It does make the recorded evidence wrong at the head being merged.
- **Required outcome:** make lines 500-501 and 511-512 true at the merge head. Either:
  - re-measure there and quote those counts (this head: 7,660 total, 7,640 default, 197 of 7,640 and 3 of 7,640), naming the commit; or
  - explicitly frame the section as measured at `05fd9e1b`, before the merge of main, as the neighbouring mutation notes do.

  No test or RTL change is needed.
- **Verification:**
  - Run `grep -n '1,966\|1,946' tb/pp_top/README.md`: it should either return nothing or show only commit-qualified historical text.
  - `scripts/run_pp_top.sh <tree>` should print a total equal to the README figure.
  - `scripts/rom_mutant.sh <built-tree> <workdir> 560 c00000000000` and `… 741 230000000003` should print failure counts and denominators equal to the README rows.

### R318-1-S1: SUGGESTION (Conformance, Docs): quote the whole recommendation note

- **Where:** `docs/architecture/06_aecp_engine.md:622-623`; `docs/00_MILAN_COMPLIANCE_REVIEW.md:117-118`.
- **Evidence:** every note (5.4.4.2 to 5.4.4.5 and 7.6) continues: "This recommendation will become a requirement in a future revision of this specification." The parent's FR-MVU-02 already records this.
- **Suggestion:** add that sentence to the waiver. It is the reason the P4 revisit trigger exists.
- This does not affect the verdict.

### R318-1-S2: SUGGESTION (Tests, Robustness): pin the new "no lock check" claim

- **Where:** `docs/architecture/06_aecp_engine.md:615` ("The waived MVU SETs (§6.9) take the unsupported-command path without a lock check.").
- **Evidence:** the claim is new in this PR and is not graded by the tracked suite. It matters because Milan Table 5.19 has no ENTITY_LOCKED code for MVU (2 to 31 are reserved).
- **My probe:** controller 1 took the ENTITY lock, then a second controller sent the complete SET_SYSTEM_UNIQUE_ID and SET_MEDIA_CLOCK_REFERENCE_INFO. Both got the byte-exact NOT_IMPLEMENTED echo, with no extra AECP frame; controller 1 then unlocked. Result: 6 added checks, 7,646 of 7,646 pass (`receipts/08-lock-probe.*`).
- **Suggestion:** adopt such an arm into M4.
- This does not affect the verdict: the claim is true at this head.

### Prior public review findings

- This is round 1. PR #118 has no reviews and no review comments.
- Issues #55, #56 and #77 have no review-finding comments. The PR's issue comments are the two review-start notices and a concurrent round-1 report from the other reviewer.
- I did not read that concurrent report, to keep this review independent. There are no prior-round findings to resolve or retain.

## Lens evidence

### Conformance: CLEAN
- **Milan v1.2 wording:** I read the Final Approved 2023-11-30 PDF myself (sha256 in `receipts/00-milan-clause-check.txt`).
  - §5.4.4.2, .3, .4 and .5 and §7.6 each open with "Support for this feature is a recommendation for Milan compliant PAADs."
  - Printed pages: §5.4.4.2 on p.58 through §5.4.4.5 on p.61, and §7.6 on p.115. These match the citations at `06_aecp_engine.md:620-623` and `00_MILAN_COMPLIANCE_REVIEW.md:117-118`.
- **Tables:**
  - Table 5.18 reserves 0x0005 to 0x7fff.
  - Table 5.19 gives 0 SUCCESS and 1 NOT_IMPLEMENTED.
  - Table 5.20 defines only REDUNDANCY and TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING, so `features_flags` = 0 advertises neither pair. That matches `06_aecp_engine.md:659-661`.
- **Command forms** (Figures 5.3, 5.5, 5.6, 5.7) give 32, 40, 104 and 32 B AECPDUs, which is cdl 20, 28, 92 and 20. This matches:
  - the §6.9 length table (`06_aecp_engine.md:647-652`);
  - F06.14 (`06_aecp_engine.md:193-194`);
  - the harness payloads (`tb/pp_top/sim_main.cpp:2480` onward: SUID @32, flags @32, user_mcr_prio @35, name @40).
- **Waiver recorded consistently in:**
  - §6.9 and F06.14;
  - 00 GAP-03 prose (`00:110-127`), F00.2 row (`00:479`) and §8 item 4 (`00:509`);
  - REQ-MVU-003 and REQ-MVU-004 (`00:380-381`);
  - 07 (`07_memory_maps.md:273-274, 358-360, 369-370, 462-463`);
  - F01.5 (`01_overview.md:151, 173`), 02 (`02_interfaces.md:51, 360`), 03 (`03_packet_engine.md:204`) and 06 §11 (`06_aecp_engine.md:1243`).
- **No leftover support claims:** a repo-wide search for SYSTEM_UNIQUE, MEDIA_CLOCK_REF, SUID, MCR, P-EN-MVU, system_unique and mcr_prio finds no MUST or "implemented" wording for either pair. Every hit is waived, deferred or reserved.
- **Parent consistency:** the parent FR-MVU-02 at dev `ffcbd33` states the same fallback: SHOULD, NOT_IMPLEMENTED with the command echoed.

### RTL: CLEAN
- **No RTL change:**
  - `git diff 265d676 05fd9e1` touches only `docs/` and `tb/pp_top/{README.md,sim_main.cpp}`.
  - `git diff 990f965 b51bc38 -- hdl syn scripts .github` is empty.
  - The RTL in 265d676..b51bc38 is main's PR #115, brought in by the merge (`receipts/07-merge-and-rtl-scope.txt`).
- **The documented behaviour is what the RTL does:**
  - Only `desc_ty_r == MVU_GET_MILAN_INFO_C` leaves the echo (`hdl/aecp/KL_aecp_engine.sv:1290-1296, 2827-2830`).
  - E_NOTIMPL is SET_STATUS NOT_IMPLEMENTED, BUILD_HDR, SEND_RESP, END, with no CHECK_LOCK (`hdl/aecp/ucode/gen_ucode.py:567-572`).
  - `MILAN_FEATURES_FLAGS = 0` (`gen_ucode.py:112`).
  - `hdl/` has no SUID or MCR parameter, storage or `GET_MCR_DEFAULTS` face.
- **Static checks at head with the pinned 5.050:** `./scripts/lint_hdl.sh` returns 0 and `scripts/check_upc_map.py` returns 0 (`receipts/09-static-lint-upcmap.txt`).

### Robustness: CLEAN
- M4 sends the complete command forms, including nonzero SET data (a 64-bit ID, both flags, a priority and a UTF-8 name).
- The reserved type 0x0005 keeps generic refusal covered independently of the waiver. M3, M6, M8 and M9 cover a foreign protocol_id, a truncated command and OUI collisions.
- The foreign-lock probe (S2) shows the waived SETs never emit a Table 5.19-reserved status and never produce an extra frame.
- A future MVU decode that widened past 0x0000 is caught. The any-type mutant turns 16 M4 checks and M5 red (`receipts/05-rtl-mutant-any-type-milan-info.*`).

### Tests: UNCLEAN (R318-1-F1)
- **Baseline at head** (pinned Verilator 5.050, 8 build jobs): exit 0; default build 7,640 of 7,640, fixture build 20 of 20, total 7,660 (`receipts/01-pp_top-baseline.txt`).
- **SUCCESS and feature mutants, reproduced at head:**

  | Mutant | Result | Receipt |
  |---|---|---|
  | Generated-ROM word 560 (E_NOTIMPL) set to SET_STATUS SUCCESS | exit 1, 197 of 7,640. M4 fails its status and byte-exact checks for each of 0x0001-0x0005 (10); the length and cdl checks pass, as the README states | `receipts/02-*` |
  | Waived types only: MVU 0x0001-0x0004 sent to an existing SET_STATUS SUCCESS echo routine (ROM word 135), everything else untouched | exit 1, exactly 8 of 7,640: M4 status and byte-exact for 0x0001-0x0004. 0x0005 and every other check pass, so the pin is specific to the waived pairs | `receipts/04-*` |
  | Any MVU type 0x0000-0x0007 answered with the Figure 5.4 SUCCESS body | exit 1, 17: 16 in M4 (status, cdl, length, byte-exact), plus M5 | `receipts/05-*` |
  | `features_flags` set to 3, 1 or 2 | exit 1 each: M1, M2 and M5b | `receipts/03-*` |

- **Harness independence:** the expected frames come from `aecp_frame()` and `mvu_expect()`, rebuilt from the figure offsets, not from DUT output.
- **Open finding:** F1. The test-evidence README section quotes pre-merge counts.

### Docs: UNCLEAN (R318-1-F1)
- `make check` at head returns 0: 41 mermaid and 18 wavedrom blocks, 872 links, 115 REQ rows, 17 GAP findings, 92 module rows, 0 untested (`receipts/06-make-check.txt`).
- Anchors `#69-mvu-commands` and `#fig-01-params` resolve. The §8.1 and §8.2 cross-references exist and match.
- **Merge composition:**
  - `git merge-tree --write-tree 05fd9e1 990f965` equals the head tree `aca3aeea…`, so the merge has no hand-authored content.
  - The authored +/- lines are identical before and after the merge.
  - Main's additions to 00, 02, 06, 10, `sim_main.cpp` and the README compose without conflict, and the composed suite passes.
- The single composition defect is F1.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 §5.4.3-5.4.4.5, §7.6, Tables 5.18-5.20, Figures 5.3/5.5/5.6/5.7; 06 §6.9/F06.14/F06.9/§11; 00 GAP-03/F00.2/REQ-MVU-003/004/§8; 01 F01.5; 02; 03; 07; parent FR-MVU-02 @ffcbd33 | R318-1 | b51bc3893b06f4d39be49726c1b8f4ed6c65573d |
| RTL | CLEAN | authored delta scope; `KL_aecp_engine.sv` MVU decode and dispatch; `gen_ucode.py` E_NOTIMPL/E_MVUINFO; lint_hdl; check_upc_map | R318-1 | b51bc3893b06f4d39be49726c1b8f4ed6c65573d |
| Robustness | CLEAN | M3-M9 arms; foreign-lock probe; any-type decode mutant | R318-1 | b51bc3893b06f4d39be49726c1b8f4ed6c65573d |
| Tests | UNCLEAN (F1) | `sim_main.cpp` M1/M2/M4; `tb/pp_top/README.md` M3/M4 bullets and waiver mutation section; baseline and 6 mutant/probe runs at head; hosted suites log at head | R318-1 | b51bc3893b06f4d39be49726c1b8f4ed6c65573d |
| Docs | UNCLEAN (F1) | all 8 authored files; merge composition of 00/02/06/10/README/sim_main.cpp; `make check` | R318-1 | b51bc3893b06f4d39be49726c1b8f4ed6c65573d |

## Real limits

- I did not run the full PP, parent, gPTP, Yosys or builder banks; the assignment did not allow them. My executions were:
  - pp_top (both builds);
  - 6 disposable mutant or probe runs (default build);
  - `make check`, `lint_hdl.sh` and `check_upc_map.py`.

  Other suites are covered only by the hosted exact-head runs: push run 36074622718 and pull_request run 36074626074, each with docs-gates, suites and portability executed and successful, none skipped (`receipts/10-hosted-ci-head.txt`). Hosted and act acceptance belongs to the manager.
- The public evidence bundle `kebag-logic/milan-fpga@e63b4124…/review-evidence/pp510-r1` contains author evidence only. It was recorded at `05fd9e1` or with base-HEAD cwd entries, and its parent consumer commit `65bc81ed` pins `05fd9e1`. That commit is local and not published. I found no public manager receipt for banks at `b51bc389`. I relied on my own and the hosted executions instead.
- **Parent consumer:** not executed by me, and not allowed. The public `508-pp-pin-adopt` branch head is `35f06958`, which pins the processor at `a8f8ce81`.
- Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware was used.
- The Milan text was read from a locally held licensed PDF. Only citations and a one-sentence note are reproduced.

## Pending manager duties

1. Resolve F1: refresh or commit-qualify `tb/pp_top/README.md:500-501,511-512`.
2. Refresh the PR body's head, check counts and link count. It still quotes `05fd9e1`, 1,966 checks and 871 links; at this head the counts are 7,660 checks and 872 links.
3. Run the parent consumer check with the gitlink at the final processor head, not `05fd9e1`.
4. Retire or update the parent `docs/reference/SUBMODULES.md:111` known-conflict row ("F01.5 lists P-EN-MVU-SUID / P-EN-MVU-MCR at 1 / 1") once the pin includes this change.
5. Build the final current-dev candidate at the merge turn (source base `265d6762…`, live dev `ffcbd33d…`) and own hosted and act acceptance.
6. Keep REQ-MVU-005 timing in #57. It is outside this waiver.

## Receipts and reproduction

- Scripts are in `scripts/`. All of them take tree paths as arguments. The pinned Verilator is passed as `VERILATOR` or on `PATH`, and I verified its version as `Verilator 5.050 2026-07-01 rev v5.050`.
- Receipts are in `receipts/`. Local absolute paths are replaced by `<packet>`, `<home>` and `<pinned-bin>`.
- Disposable copies lived only under `scratch/`, which is not published.
- The review clone was verified afterwards (`receipts/12-clone-integrity.txt`):
  - HEAD and tree are exact;
  - status, including ignored files, is empty;
  - the index is identical to the HEAD tree (mode, blob and path);
  - all 246 worktree files re-hash to their index blobs;
  - the processor repository has no gitlinks (no `.gitmodules`, zero mode-160000 entries).

R318-1 FINISHED
