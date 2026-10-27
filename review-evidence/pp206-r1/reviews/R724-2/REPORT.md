[R724] POSITIVE - exact head c836105351297947a7660952df7c4d92500a09ec

# R724-2: independent review of processor PR #208 (issue #206), round 2

- **PR:** Mister-M-alt/protocol-processor-control-plane-avb-milan#208, head `c836105351297947a7660952df7c4d92500a09ec`, tree `1a4a8fe48ece11f134a6a03dbfbb6990451b86ed`. Both are confirmed in the detached reviewer clone, as is the index tree (`receipts/CLONE-RESTORE.txt`).
- **Base and delta:** base is main `097a7987`; the previously reviewed head is `e9272b5`. The round-2 delta `e9272b5..c836105` is two commits (`7919c9a`, `c836105`) touching 5 files (+54/-24). It changes no `hdl/` file.
- **Scope**, reconstructed from public sources:
  - the issue #206 body ("Required", "Acceptance");
  - the manager's assignment and round-2 assignment comments on #206;
  - the PR body;
  - the diff and history `097a7987..c836105`;
  - the author's evidence packet at milan-fpga `5bd31989`, `review-evidence/pp206-r1/author-r2`.

  The processor repository has no AGENTS.md or CONTRIBUTING.md.
- **Prior public findings** on this PR (R723-1, R724-1) were read only after this round's own pass over the delta. Each one is resolved or retained below.

## Verdict

POSITIVE. All five lenses are CLEAN, and no BLOCKER, MAJOR or MINOR finding is open.

- The one prior MINOR, R724-1-F1, is fixed at its cause. The author's receipts show this, and so do four extra over-clearing masks this reviewer planted.
- This round adds one RESIDUE: wording in the S1 rationale.
- One prior SUGGESTION, R723-1-SUG-01, is retained.

Neither the RESIDUE nor the SUGGESTION affects the verdict.

## Acceptance (issue #206), checked at this head

| # | Acceptance item | State | Evidence |
|---|---|---|---|
| 1 | Processor-top tests cover four cases: bound and probing; PROBING_PASSIVE after a timeout with a stale ID; settled; unbound | holds | `tb/pp_top/gsi_internal.hpp:705` `settled_gate` covers RESET, PROBING, PROBING-SENT, SETTLED, REPROBE, REPROBE-SENT, SETTLED-AGAIN, PASSIVE-STALE and UNBOUND. This reviewer's golden run at head used an independent simulator version (5.050; the author used 5.052): section GI ran 6,388 checks with 0 failures (`receipts/probes/out/golden-run.log`) |
| 2 | A mutant that restores the pass-through is caught | holds | In the author campaign at c836105, `settled-gate-removed` is killed by `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero`. All 30 arms are killed; golden and restored PASS; rc 0 (`author-r2/receipts/campaigns/gsi-c836105/mut.{log,rc}`) |
| 3 | The docs row for GET_STREAM_INFO is updated | holds | `docs/architecture/06_aecp_engine.md:384-397` and `:492-494`; 02 §4.4; integrator §8; 00 REQ-AEM-010. These are unchanged since R724-1 except for the R723-1-RES-01 rewrap |
| 4 | The parent consumer gates pass | holds (author receipts) | `author-r2/receipts/parent-static-0dea6860`: 16 commands, all rc 0, with gitlink `protocol-processor` = c836105 (`GITLINK.txt`). The heavier parent rows are carried from `9abb41f`, which has identical RTL. The final current-dev candidate is the manager's |
| - | No top-level port, parameter or register-map change | holds | The `hdl/` diff `097a7987..c836105` touches only `protocol_processor_top.sv:3532-3588`, which is internal wires and combinational logic. `git diff e9272b5..c836105 -- hdl` is empty |

## Prior findings: disposition at this head

### R724-1-F1 (MINOR; Tests, Robustness): RESOLVED

**Cause:** the harness integrator claimed only `0x52000000`. A gate that over-cleared BOUND or MSRP_ACC_LAT_VALID therefore survived the suite.

**Fix:** the delta addresses the cause directly:
- `tb/pp_top/sim_main.cpp:1297` sets `GSI_FOLD_FLAGS = 0xFFFFFFFF`.
- `:2059`: in settled-gate mode the integrator ORs that value into every STREAM_INPUT selector 0 word.
- `tb/pp_top/gsi_internal.hpp:631` and `:633`: `gate_expected` keeps every other flag, in both the unsettled body and the settled body.
- `:659-663`: a new named check, `GI GATE <step> <kind>: every other flag the integrator claims passes ...`, runs on each of the 15 graded responses.
- `tb/pp_top/gsi_mutants.py:60-64` adds the arm `settled-gate-mask-overclears` (`~0x5600_0000`).

**Verification from the author's receipts:**
- In the author campaign at c836105, the new arm fails 22 named lines: 11 unsettled responses, each failing the other-flags check and the byte-exact check.
- The author ran R724-1's `reviewer_probes.py` unchanged; its sha256 is recorded in `reviewer-probes/INPUTS.txt`. Both `R-mask-overclears-bound` and `R-mask-overclears-acclat` now fail with rc 1, and 22 of 22 FAIL lines are `GI GATE` (`author-r2/receipts/reviewer-probes/out/`).
- The full `make -C tb/pp_top run` at c836105 returns rc 0: 10,887 checks, 0 failures (`author-r2/receipts/processor/head-c836105/pp_top_run.log`, tail).

**Verification from this reviewer's own probes**, beyond the author's arms: `probes.py` (`receipts/probes/`) returned rc 0, with 8 of 8 verdicts as expected.

| Arm (selector 0 mask while unsettled) | Purpose | Result |
|---|---|---|
| `~0x5A000000` (also MSRP_FAILURE_VALID) | over-clear of the third integrator-owned flag named by F1 | killed by `GI GATE RESET solicited: every other flag ...`, 22 FAIL |
| `~0xD2000000` (also STREAM_FORMAT_VALID, bit 31) | over-clear of the top bit | killed by the same named check, 72 FAIL |
| `~0x52000001` (also bit 0) | over-clear of the bottom bit | killed by the same named check, 43 FAIL |
| `~0x52000002` (also FAST_CONNECT) | over-clear of a low flag | killed by the same named check, 22 FAIL |
| `~0x50000000` (STREAM_VLAN_ID_VALID left set) | under-clear of one gated flag | killed by `GI GATE RESET solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear for sink 0`, 22 FAIL |
| `~0xFFFFFFFF52000000` (also clears selector 0 [63:32]) | bounds the "every flag" claim | survives (6,388 / 0), as predicted. Bits [63:32] are not part of the 32-bit flags field, so "every flag in every flags word" means that 32-bit word, which is also what the docs say |
| selector 4 zeroed whole while unsettled | tries to falsify S1's claim that no graded unsettled response carries a failure code | survives (6,388 / 0), which is consistent with the claim |

### R724-1-S1 (SUGGESTION; Tests): ANSWERED, closed

The author states why no step can grade selector 4's failure-code byte while the input is unsettled. This reviewer checked each link of the argument against the cited source:

- **SRP failure code:** in `hdl/srp/KL_srp_listener_fsm.sv:1268-1275`, `msrp_fail_code_o` is non-zero only when `tk_reg_state_o == 2`. That state requires `armed_r`, which is set only on `ctl_settle_i` (`:935`) and cleared on teardown (`:966`).
- **Settle and teardown actions:** in `hdl/acmp/KL_pp_acmp_listener.sv`, A15 (`:1311`) is the only writer of `PB_COMPLETED_C`; the other `pbsta` writers are at `:1273`, `:1280`, `:1327`, `:1344` and `:1352`. A8 (`:1204`) asserts `act_teardown_o`.
- **ROM arcs:** in `hdl/acmp/rom/gen_ltn_rom.py`, every arc that takes SNR or SOK to an unsettled state carries A8: BIND_NEW (`:54-55`), UNBIND (`:63-64`), TMR_NOTK (`:83`) and TK_UNREG (`:97`).

The PR body's line citations are accurate, and the probe that survived (above) is consistent with the argument. One wording imprecision in the restated rationale is recorded as R724-2-RES-01.

### R724-1-W1 (RESIDUE; Docs): RESOLVED

`tb/pp_top/README.md:515-516` now reads "Premise checks read the binding view at RESET, PROBING, SETTLED, REPROBE, PASSIVE-STALE and UNBOUND". That is the exact fix.

### R723-1-RES-01 (RESIDUE; Docs): RESOLVED

- `docs/architecture/06_aecp_engine.md:394-401` are all at most 79 columns. The line now breaks after "owners.", and the author's record shows the paragraph's words are unchanged (`author-r2/receipts/records/residue-and-length-checks.txt`).
- Line `:402` is 126 columns ("([05 F05.12]... Selector 15 ..."). It is the same length at base `097a7987`, so it does not come from this PR.

### R723-1-SUG-01 (SUGGESTION; Tests): RETAINED

The settled-gate section still reads no STREAM_OUTPUT. As a result, `settled_gate` (`gsi_internal.hpp:705`) has no named check that outputs are left untouched. Round 2 neither took up this suggestion nor was assigned it. It remains a suggestion and does not affect the verdict.

## Findings (this round)

### R724-2-RES-01 - RESIDUE - Docs, Tests (comment wording only)

- **Where:**
  - `tb/pp_top/README.md:517-519`: "disarmed by A8, which every F05.3 arc out of SNR or SOK runs, so no Talker Failed registers while the input is unsettled".
  - `tb/pp_top/gsi_internal.hpp:615-617`: "disarmed by A8, which every F05.3 arc out of SNR/SOK runs, so no Talker Failed registers while unsettled".
  - The PR body, section Tests: "Every F05.3 arc out of SNR or SOK carries A8".
- **Fact:** two kinds of arc leave SNR or SOK without A8, and both stay settled, so the conclusion still holds:
  - EVT_TK_REGISTERED takes SNR to SOK with A11 alone (`gen_ltn_rom.py:95`).
  - BIND_SAME keeps SNR and SOK with A1 A6 A3 (`:38-46`).

  In addition, a Talker Failed can still register in the MSRP registrar while the input is unsettled. What A8 prevents is the matcher reporting it, because `tk_reg_state_o` requires `armed_r`.
- **Impact:** wording only. No code, test, measurement or verdict changes, and the S1 conclusion is unchanged.
- **Exact fix:**
  - In both source comments, replace "which every F05.3 arc out of SNR or SOK runs" (or "out of SNR/SOK runs") with "which every F05.3 arc from SNR or SOK to an unsettled state runs".
  - In both source comments, replace "no Talker Failed registers while [the input is] unsettled" with "SRP reports no Talker Failed while [the input is] unsettled".
  - In the PR body, change the sentence to "Every F05.3 arc from SNR or SOK to an unsettled state carries A8".
- **Verification:** `grep -n "arc out of SNR" tb/pp_top/README.md tb/pp_top/gsi_internal.hpp` prints nothing.

There is no other finding. The comment rule holds: the source comments added in `e9272b5..c836105` cite issue #206, Milan clauses and design action IDs (A8, A15, F05.3). None carries a bench lane label, lane name, review round, reviewer ID or issue-comment ID.

## Lens results

### Conformance - CLEAN

- **Authorities:** Milan v1.2 5.4.2.10.1 / Table 5.9 and 5.3.8.5 / Table 5.5; IEEE 1722.1-2021 7.4.16.2.
- **Settled test:** `gsi_settled_w` (`protocol_processor_top.sv:3563-3564`) is the in-range index AND `lstn_gsi_status_r[sink][7:5] == PB_COMPLETED_C`. This is the same committed byte that selector 7 returns as pbsta (`:3575`).
- **Gating while unsettled** (`:3581-3587`): selector 0 is ANDed with `~0x52000000`, selector 2 answers 0, and selector 4 `[63:16]` answers 0. Selector 6 shares the same wire.
- **Carried verdict:** these lines are unchanged since `9abb41f`, and round 2 changes nothing they depend on, so the R724-1 Conformance verdict (CLEAN) carries.
- **Re-executed:** section GI at head passes on 5.050 (6,388 / 0). The new tests now also pin that only `0x52000000` is cleared (this reviewer's four over-clear probes).

### RTL - CLEAN

There is no `hdl/` delta since the previously reviewed head. A re-read of `protocol_processor_top.sv:3520-3590` confirms:
- The gate sits inside `if (gsi_input_w)`, so outputs and other kinds are untouched.
- `gsi_req_o` and `aecp_gsi_wait_w` are unchanged, so selectors 0, 2 and 4 keep the external request and wait.
- An out-of-range index reads as unsettled.

The R724-1 RTL verdict (CLEAN) carries.

### Robustness - CLEAN

- The R724-1-F1 gap is closed: an edit that over-clears no longer passes every guard.
- Clearing any bit of the 32-bit flags word outside `0x52000000` now fails a named `GI GATE` check at every unsettled response. Bits 0, 1, 26, 27, 29 and 31 were exercised by the author's arms and this reviewer's probes.
- An under-clear of one gated flag also fails by name.
- The handshake and the gather watchdog are untouched.

### Tests - CLEAN

- **Delta examined line by line:** `sim_main.cpp:1287-1297` and `:2058-2062`; `gsi_internal.hpp:604-640` and `:656-663`; `gsi_mutants.py:28-65`.
- **Scope of the new flags:** `GSI_FOLD_FLAGS` applies only when `gsi_fold_identity` is set, and only for kind 0, type 0x0005, index < 2, so the integrator words of other sections are unchanged. The author's full-suite tally rose by exactly the 15 new checks (10,872 + 15 = 10,887).
- **Mutant driver:** it kills the new arm by its named check (30 of 30).
- **Idiom limits:** function lengths are 38 and 100 lines, the latter exactly at the parent idiom bound. The parent `check_py_idiom.py` and `check_cpp_idiom.py` pass with this head as gitlink.
- **Discrimination:** the head's tests still fail 82 lines on the base RTL (author record).

### Docs - CLEAN

- **Docs delta:** the README GI paragraph and mutant row (`tb/pp_top/README.md:494-521`, `:589`) and the rewrapped `06_aecp_engine.md:394-401`.
- **Accuracy:** these state the claimed flags, the named check, the six premise steps and the arm's failing line, all as the code does.
- **PR body:** its gate counts match the receipts: 10,887 / 0; 30 of 30; 22 lines for the over-clear arm and for both reviewer masks; 32 `GI GATE` lines for the first arm; function lengths 38 and 100.
- One wording RESIDUE (R724-2-RES-01) does not leave the lens unclean.

## Evidence verification

- **Author packet integrity:**
  - `verify_manifest.py` was run against `5bd31989:review-evidence/pp206-r1/MANIFEST.json`. All 127 `author-r2/` blobs are listed, and each matches its `published_sha256` (`receipts/evidence/manifest-author-r2.log`, rc 0).
  - Across the whole packet, 1,369 listed entries all match. The only unlisted blob is `MANIFEST.json` itself (`receipts/evidence/manifest-all.log`).
  - The packet commit is not GPG-signed, so integrity rests on the manifest digests.
- **Receipt heads:** `suite-HEAD.txt`, `check-HEAD.txt` and `mut-HEAD.txt` all name c836105, and the rc files are 0. The memory record shows a peak of 8.1 GB for the mutant campaign.
- **Hosted CI at this head** (`receipts/HOSTED-CHECKS.txt`, snapshot 16:33 UTC):
  - `docs-gates` (2 runs) and `portability` (2 runs) completed with success.
  - `suites` (2 runs) was still `in_progress`: neither executed-passed nor skipped.

  Hosted and act acceptance remain the manager's.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `protocol_processor_top.sv:3526-3590` (unchanged since 9abb41f); Milan 5.4.2.10.1/T5.9, 5.3.8.5/T5.5; 1722.1 7.4.16.2; GI golden 6,388/0 on 5.050; four over-clear and one under-clear probes | R724-2 (delta); RTL clauses carried from R724-1 | c836105351297947a7660952df7c4d92500a09ec |
| RTL | CLEAN | empty `hdl/` delta e9272b5..c836105; gate block re-read; no port, parameter or register-map change since base | R724-2 (carried from R724-1) | c836105351297947a7660952df7c4d92500a09ec |
| Robustness | CLEAN | R724-1-F1 cause closed: `sim_main.cpp:1297`, `:2059`; `gsi_internal.hpp:631-663`; author arm and R724-1 reviewer probes (22 named FAIL each); this reviewer's 7 probe arms | R724-2 | c836105351297947a7660952df7c4d92500a09ec |
| Tests | CLEAN | round-2 test delta; author campaign 30/30; full-suite receipt 10,887/0; base-RTL discrimination record; this reviewer's probes 8/8 as expected; S1 chain verified in SRP, ACMP and ROM source | R724-2 | c836105351297947a7660952df7c4d92500a09ec |
| Docs | CLEAN (1 RESIDUE) | README GI paragraph and mutant table; 06 §6.2 rewrap; PR body tables vs receipts; comment rule over the delta | R724-2 | c836105351297947a7660952df7c4d92500a09ec |

## Real limits

- **Full suite not re-run by this reviewer.** This reviewer did not re-execute the full `make -C tb/pp_top run`: permission for that long run was denied twice in this session, once as a detached job and once as a concurrent split. This reviewer's own execution covers section GI only, via the probe driver's golden and arm builds. The full-suite verdict rests on the author's published receipt at c836105 (rc 0, 10,887 / 0).
- **Earlier run killed.** An earlier attempt in this unit ran the full suite beside the probe campaign and was killed by the memory cap before it completed. Its partial log is not evidence and is not published.
- **Parent gates rest on author receipts.** They come from a scratch parent (`0dea6860`, gitlink c836105). The heavier parent rows (full sweep, `[GSI]` cases, OOC) are carried from `9abb41f`, which has identical RTL.
- **No manager source bank.** None ran at this exact head, and none is claimed.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Hosted `suites` jobs** were still in progress when sampled.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base 097a7987, live dev 97aab1d0f28bd753a3e11df6278d5cac54f964dd) with the builder and native banks, and link the receipts on the PR.
- Confirm the hosted `suites` contexts at this head, and hosted and act acceptance.
- Carry R724-2-RES-01 to the residue checklist. R723-1-SUG-01 stays open as a suggestion, at the author's discretion.
- Track the parent adoption under milan-fpga #790: the `[GSI]` cases in `milan_dp` and `pp_shadow`, and the parent `gsi_mutants.py` arm.

## Packet

- **Scripts:**
  - `probes.py`: the reviewer's mutation probes. They reuse the clone's own `gsi_mutants.check_variant` in private temporary copies.
  - `verify_manifest.py`: checks the evidence manifest.
  - `vl-capped.sh`: caps each simulator build's job count to stay within memory. After the run, its default binary was changed to a portable `verilator` on PATH. The run itself used the pinned 5.050, as `receipts/probes/probes.cmd` and `receipts/VERILATOR-IDENTITY.txt` record.
- **Receipts:** everything under `receipts/` is listed in `MANIFEST.sha256`. Compile logs carry host paths, so they are recorded by size and sha256 in `receipts/probes/BUILD-LOGS.csv` and not published.
- **Clone restored after the probes:** the worktree equals HEAD in bytes and modes, the index tree equals `1a4a8fe4...`, there is nothing untracked or ignored, and the repository has no submodule gitlinks (`receipts/CLONE-RESTORE.txt`).

R724-2 FINISHED
