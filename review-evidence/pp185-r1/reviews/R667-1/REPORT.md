[R667] NEGATIVE - exact head b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad

# R667-1: independent review of processor PR #196 (Closes #185, #186)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #196, branch `185-186-control-unlock`
- Exact head `b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad`, tree `6ecc64cb8c3434106e71bbb191aebe9a0249db1e` (verified in the clone and in the reviewer's export)
- Reviewed delta: `git diff b48312e1..b0f6f9c3` (28 files, +982/-60), the author commits 198f1b1 (#185), c826171 and fcb6b51 (#186), the author merge a2cf652 of main 246cbc22, f42c886, and the manager merge b0f6f9c of main b48312e1 (#190)
- Round: R667-1 (first round of this reviewer). Prior public review findings on PR #196 and on issues #185/#186: none were published before this pass (the PR carries only two review-start notices), so there is nothing to resolve or retain.

## Verdict

NEGATIVE. Both issues' headline behaviours are implemented and verified at the exact head: READ_DESCRIPTOR of the IDENTIFY CONTROL carries GET_CONTROL's value before any SET_CONTROL, after every SET_CONTROL and after a power cycle (#185), and both unlock notifications, the UNLOCK command's and the automatic one, carry flags UNLOCK with locked_id 0 in the graded sequences, with a LOCK notification echoing the LOCK's word (#186). Every new check has a planted mutant that is killed, the merges kept #181's behaviour, and the affected suites and gates pass at the exact head. Three MINOR findings remain open:

- **F1**: a lock change during a running lock round sends frames whose flags come from the earlier cause while locked_id is read live. The probe shows "UNLOCK, locked_id = the new holder".
- **F2**: the CONTROL overlay ignores `control_type`, so a non-IDENTIFY one-octet linear CONTROL is served the IDENTIFY value.
- **F3**: a stale campaign total in the `tb/pp_top` mutation record.

There is also one RESIDUE and five SUGGESTIONS.

## Reconstruction

1. Contributor rules. The processor has no AGENTS.md or CONTRIBUTING.md at this head. The conventions are the README and `docs/README.md`: ID registries, single-source rules (timing values only in F08.1), citation style, and `make check` before commit. The owner's comment rule from the assignment applies to source comments.
2. Frozen scope:
   - The issue #185 body.
   - The issue #186 body.
   - The assignment (issue #185 comment 6249574548): one lane, two commits, suite cases with planted mutants, 06 and command records updated, all processor and parent gates, STOP on register-map/top-port/parameter change.
   - The correction (issue #186 comment 6253571045): the lock-timeout notification also carries UNLOCK with locked_id 0, because Milan v1.2 Table 5.22 is silent and IEEE 1722.1-2021 §7.5.2 and §7.4.2.1/Table 7-143 decide. The branch follows the correction (fcb6b51).
3. Authorities read against the code:
   - IEEE 1722.1-2021 §7.2.22 (CONTROL layout, value_details at values_offset 104), §7.3.5.2/§7.3.6 (linear values: minimum, maximum, step, default, current, unit, string; current[0] at 4V), §7.4.2.1/Table 7-143 (LOCK_ENTITY flags, UNLOCK = 0x00000001), §7.5.2.
   - Milan v1.2 §5.3.12 (IDENTIFY 0 after reset, 255 identifying), §5.4.5.1, Table 5.22.
   - In tree: 06 §6.1/§6.8/F06.14, 08 F08.1 (`T-LOCK-UNLOCK`), and model rule L8 (`hdl/aecp/desc/model_rules.py:784-806`).
4. The delta, the history and both merges (`git show --remerge-diff`):
   - a2cf652 resolves the five conflicts by keeping both sides. `KL_aecp_notify.sv` takes #181's `cmdq_nempty_r` arm (`:846`), and the lock arm's arguments are added above it.
   - b0f6f9c's only conflict is the `tb/pp_top/README.md` section heading, resolved to the merged heading.
5. Public executable evidence: `kebag-logic/milan-fpga@baba38e7 review-evidence/pp185-r1`. This reviewer fetched `receipts/INDEX.md` (908 rows = 897 published files + the 11 over-200 KB rows in `OVER-200KB.sha256`) and the round-1c head-final gate and comparison receipts. Each fetched file's bytes and sha256 match its INDEX.md row (`receipts/evidence-hash-check.txt`). The author's last gate head is `f42c886`. There are no author receipts at `b0f6f9c` (the manager merge), and no manager source bank runs at this head. This reviewer does not claim one.

## Executions at the exact head (this reviewer)

Pinned Verilator 5.050 (`rev v5.050`, wrapper sha256 `905795b9…e92f`, `receipts/tools.txt`). All runs were on a disposable `git archive` export whose tree equals `6ecc64cb`. The clone was only read.

| Run | Result | Receipt |
|---|---|---|
| `tb/ucpu` | 445 checks, 0 FAIL (RC1, RC2, L3, L3b) | `receipts/suite-ucpu.log` |
| `tb/aecp_notify` (all five runs) | 86 checks, 0 FAIL (LF 6, CQ, OC1 in every run) | `receipts/suite-aecp_notify.log` |
| `tb/aecp_cmds` | 617,916 trials, 176 checks, 0 FAIL | `receipts/suite-aecp_cmds.log` |
| `tb/pp_top` (every build) | 10,608 checks, 0 FAIL (the author's 10,599 at f42c886 plus #190's section TS) | `receipts/suite-pp_top.log` |
| `check_upc_map.py`, `check_m9_opcodes.py` (+selftest), `gen_matrix.py --check` | PASS (62 constants / 91 entries; 30 opcodes; 94 rows, 0 untested) | `receipts/gate-*.log` |
| `scripts/lint_hdl.sh` | rc 0 | `receipts/gate-lint.log` |
| `make check` | rc 0 (aecp 85 entries; ids 617 files) | `receipts/gate-makecheck.log` |
| `notify_mutants.py`: the 16 lock controls and #181's 11 occupancy controls | goldens PASS, 27 of 27 KILLED by their named checks. Every failing set equals the README records, including `occupancy_push_unseen` (9) and `occupancy_reset_set` (17) | `receipts/camp-notify.log`, `camp-notify-results.json` |
| `aecp_dispatch_mutants.py`: the 9 `rdc-*` arms and the 3 earlier arms whose counts moved | control PASS, 12 of 12 KILLED; failure counts as the README records (13, 16, 6; 7, 2, 1, 1, 1, 2, 7, 5, 11) | `receipts/camp-dispatch.log`, `camp-dispatch-results.json` |
| Probe `tail`: AX CONTROL fixture grown to the conformant 113 bytes with a distinct byte @112, plus PROBE-NSD (READ_DESCRIPTOR of absent CONTROL 1) | AX 280 checks, 0 FAIL: the non-empty TAIL passes end to end and the stub is NO_SUCH_DESCRIPTOR | `receipts/probe-tail.log` |
| Probe `missnop`: `tail` plus E_RDESCCT's locate-miss branch replaced with NOP | AX 280, 0 FAIL: the arm is masked (S1) | `receipts/probe-missnop.log` |
| Probe `vendor`: `tail` plus CONTROL 0 given a non-IDENTIFY `control_type` | **FAIL**: @108 carries the IDENTIFY 255, not the image's 0x5A (F2) | `receipts/probe-vendor.log` |
| Probe `midround`: `tb/aecp_notify`, Y locks while X's UNLOCK round is running | the round's remaining jobs carry args 0000/0001 after Y holds the lock (F1) | `receipts/probe-midround.log` |
| Hosted checks at b0f6f9c (read only, 09:54Z and 09:58Z) | docs-gates and portability: success in both runs; suites: in progress (not executed to completion when read) | `receipts/hosted-checks-b0f6f9c.txt` |

Clone integrity after all work: HEAD, tree and index tree are all `b0f6f9c3…`/`6ecc64cb…`, `git status --ignored` is empty, the worktree equals HEAD, and there are no gitlinks (the processor has no submodules) (`receipts/clone-integrity.txt`). Host paths in the receipts are replaced by `$PKT`, `$CLONE`, `$VROOT`, `$TOOLS` and `$HOME`. `scripts/run_review.sh` replays every execution.

## Findings

### F1. MINOR: a lock change during a running lock round gives a notification whose flags and locked_id disagree

- **Lenses:** Conformance, RTL, Tests, Docs.
- **Where:**
  - `hdl/aecp/KL_aecp_notify.sv:842-845` (the lock arm picks `lockf_r`).
  - `hdl/aecp/KL_aecp_notify.sv:1510-1511` (`em_arg*_r` latched at the pick and held for the whole round).
  - `hdl/aecp/KL_aecp_notify.sv:1450` and `:1466` (a later change re-latches `lockf_r` and re-pends the class for the next round only).
  - `hdl/aecp/ucode/gen_ucode.py:1180-1189` (`E_LOCKUNS`: locked_id from `GATHER_EXT RG_STATE`, "the holder right now"; flags from r14, the job's arguments).
- **Authority:** IEEE 1722.1-2021 §7.5.2 (a notification is the unsolicited response to the command) and §7.4.2.1/Table 7-143. The frozen acceptance requires that "both unlock notifications ... carry flags UNLOCK with locked_id 0" and that a LOCK notification echoes LOCK.
- **Evidence:** `receipts/probe-midround.log`. Setup: C and D registered. X locks (round: 0000/0000 to C and D), then X unlocks with flags 1. While the UNLOCK round's first job (to C) is presented, Y's LOCK succeeds; the block serves it by withdrawal, as its banner provides.
  - The job then re-presented to C carries 0000/0001, and so does the round's job to D. Both run after Y holds the lock.
  - Only the next round carries 0000/0000.
  - `E_LOCKUNS` reads the live holder, so C and D each receive LOCK_ENTITY with flags UNLOCK and locked_id = Y, followed by flags 0 and locked_id Y.
- **Impact:** The frame is the response to neither command. X's UNLOCK answered locked_id 0, and Y's LOCK answered flags 0. The interleaving is natural: a controller that receives the unlock notification early in the walk locks at once while the round continues to the controllers after it. Before this delta, the same interleaving produced a self-consistent current-state frame (flags 0, locked_id Y). The final state is still delivered by the following round. No suite case covers a lock change during a running lock round. The PR's cause table gives "an UNLOCK that released it → UNLOCK, locked_id 0", which this path contradicts.
- **Required outcome:** Every emitted LOCK_ENTITY notification carries flags and locked_id of one cause or one state. For example, a lock change during a running lock round could re-latch the remaining jobs' arguments, or the flags could be reconciled with the locked_id the program reads. Add a suite case that reproduces this interleaving and a planted mutant that the case kills. Alternatively, obtain an owner decision that accepts the transient frame, and record it in 06 §6.8, the compliance review's row 16 and the PR text.
- **Verification:** Re-run `scripts/probe_midround.py` (or the new in-tree case) at the fixed head. No job may carry UNLOCK flags once the registry reports a non-zero holder for that job, and the new case's mutant must be killed.

### F2. MINOR: the READ_DESCRIPTOR CONTROL overlay serves the IDENTIFY value for any one-octet linear CONTROL, whatever its control_type

- **Lenses:** Conformance, RTL, Tests, Docs.
- **Where:**
  - `hdl/aecp/KL_aecp_engine.sv:3303-3314` (re-dispatch on `DT_CONTROL_C` and configuration 0 alone).
  - `hdl/aecp/ucode/gen_ucode.py:1310-1344` (`E_RDESCCT` tests length, `values_offset` and `control_value_type`, never `control_type` @82).
  - `docs/architecture/06_aecp_engine.md:1297` (the answer row says "the IDENTIFY CONTROL's value") and `:315`/§6.1.
- **Authority:** IEEE 1722.1-2021 §7.2.22 and §7.3.6.2: value_details carries that control's own current values. Milan v1.2 §5.3.12 defines the IDENTIFY value only. Model rule L8 (`model_rules.py:784-806`) admits CONTROLs other than the IDENTIFY: it checks the format only of those whose `control_type` is IDENTIFY, at the index `identify_index_i` names.
- **Evidence:** `receipts/probe-vendor.log`. CONTROL 0 is given a vendor `control_type` (0x0011223344556677) and keeps CONTROL_LINEAR_UINT8 at values_offset 104. With IDENTIFY at 255, READ_DESCRIPTOR returns 0xFF at @108 where its image holds 0x5A (PROBE-VENDOR FAIL; every other byte, including the TAIL byte @112, matches).
- **Impact:** For a lint-valid model with a vendor one-octet linear CONTROL beside the IDENTIFY, READ_DESCRIPTOR of that CONTROL reported its image's value before this delta and now reports the IDENTIFY state. This is a regression introduced by the delta. (GET/SET_CONTROL already treat every existing CONTROL as the IDENTIFY row. That is pre-existing, outside the delta and noted under S5.) No suite case uses a non-IDENTIFY CONTROL.
- **Required outcome:** Restrict the overlay to the IDENTIFY CONTROL, for example by comparing `control_type` @82..@89 with the IDENTIFY value (IEEE Table 7-98, as model rule L8 does) or by using the index `identify_index_i` names, inside the engine with no top-level change. Add a suite case in which a non-IDENTIFY one-octet linear CONTROL is served whole, and a planted mutant that the case kills. Alternatively, obtain an owner decision that every CONTROL is the IDENTIFY row, and make 06 (§6.1 and the answer row) and the PR text say so.
- **Verification:** `scripts/probe_rdc.py TREE vendor` then `make aecp-dispatch` passes (AX PROBE-VENDOR byte-exact against the image), and RDC0 to RDC6 still pass.

### F3. MINOR: the `tb/pp_top` notification-campaign record gives a total the merged head does not have

- **Lenses:** Tests, Docs.
- **Where:** `tb/pp_top/README.md:2853`: "Issue #186 adds sixteen controls for 114".
- **Evidence:** At this head `notify_mutants.MUTANTS` has 125 controls (main 246cbc22: 109, including #181's 11 `OCCUPANCY` controls). The PR text and the author's comparison table (`r1c/compare/campaigns-table.md`) say 125 of 125.
- **Impact:** The record states a campaign size that matches no head on this branch after the merge. A reader summing the chain gets 114. The 11 occupancy controls are never counted in this README's chain.
- **Required outcome:** State the merged total and its parts, for example "for 125 at this head with #181's eleven occupancy controls (recorded in `tb/aecp_notify/README.md`)", or add the merge sentence the chain uses for earlier merges.
- **Verification:** The README's stated total equals `len(MUTANTS)` at the head (125).

### R1. RESIDUE: a timing value outside F08.1 in 06 §6.8

- **Lenses:** Docs.
- **Where:** `docs/architecture/06_aecp_engine.md:806`: "Table 5.22's automatic unlock after the one-minute timeout is an unlock".
- **Why:** `docs/README.md` §2 keeps timing values in F08.1 only, and `T-LOCK-UNLOCK` exists. This is wording only and changes no figure, test or claim.
- **Exact fix:** Replace "after the one-minute timeout" with "on `T-LOCK-UNLOCK` expiry".

### SUGGESTIONS (do not affect the verdict)

- **S1:** `E_RDESCCT`'s locate-miss branch (`gen_ucode.py:1315-1316`) is redundant. With it replaced by NOP, a miss falls to `E_RDESC` through the length test, re-locates and answers the stub (`receipts/probe-missnop.log`). The behaviour the PR claims (absent CONTROL → NO_SUCH_DESCRIPTOR stub) holds (`receipts/probe-tail.log` PROBE-NSD) but has no in-tree check. Add a check, or drop the arm.
- **S2:** The AX CONTROL fixture is 112 bytes, so the overlay's TAIL is empty on the wire. Only the `tb/ucpu` model exercises the 113-byte form. With the fixture at 113 bytes and a distinct byte @112, every RDC grade passes (`receipts/probe-tail.log`). Consider adopting the conformant length in-tree.
- **S3:** The `control_value_type` test (`gen_ucode.py:1324-1328`) compares the whole 16-bit field with 0x0002. If the 2021 field's top bits carry flags (read-only/unknown), a flagged one-octet linear value is served whole. Check this against §7.2.22 and record the intent.
- **S4:** Pre-existing comments now contradicted by the new program: `gen_ucode.py:356`, `:723` and `:966` ("the µISA has no shift") and `:1933` (the image's IDENTIFY byte "unreachable to a µISA with no shift"), while `E_RDESCCT` uses `SHIFT_R` and reads lane 104..111. These are outside the delta lines; refresh them.
- **S5:** Pre-existing and outside the delta: GET_CONTROL and SET_CONTROL serve and write the IDENTIFY row for any existing CONTROL index (`KL_aecp_engine.sv:3556-3567`; `E_GCTRL`/`E_SCTRL`). Consider an issue.

## Lens notes (artifact-specific)

- **Conformance:**
  - #185: `current[0]` sits at 104 + 4V = 108 for V = 1 (Table 7-122 order: min, max, step, default, current, unit, string), and the shipped `milan_min.json` IDENTIFY (113 bytes, 0x0001, values_offset 104) takes the overlay.
  - #186: the LOCK/UNLOCK notification echoes the command's whole word, and the timeout (coalesced or not) latches 0x00000001. LN1 to LN4, L5b, L6d, TD1 and LF are graded byte-exact or by job arguments.
  - Open: F1 and F2.
- **RTL:**
  - New state is 32 flops (`lockf_r`, reset 0) and a mux arm.
  - The engine lands the LOCK job's arguments in `cfg_ix_r`/`desc_ix_r`, which during an unsolicited LOCK job feed only `opd0_w` (r14) and `rgy_flags_o`. That job's other readers (rgy op, dynamic-store row, effect strobes, faces) are gated by flags it clears.
  - `lockf_w` adds `uns_r && regun_r`, and `regun_r` is set at the job load only for `PP_UNS_LOCK_C` (`KL_aecp_engine.sv:2929`).
  - Two internal ports are wired in the top; there is no top-level port, register-map or parameter change. `tb/aecp_cmds` ties `rgy_flags_o` open.
  - Lint passes.
  - Open: F1 and F2.
- **Robustness:**
  - Coalescing follows the last cause, as the exclusion does.
  - Layout guards fall back to the whole image. A too-short CONTROL (111 bytes) is served whole, and the arm that floors it at 111 is killed.
  - The redundant miss arm is masked safely (S1).
  - The mid-round case (F1) is a robustness gap in how the round's arguments are frozen, attributed under F1.
- **Tests:**
  - Each new check has a planted mutant, killed by its named check at this head: 9 `rdc-*` arms and 16 lock controls.
  - #181 is retained: `cmdq_nempty_r` is written beside every count update (`:1314`, `:1532`, reset `:1210`) and read by the pick (`:846`) and by `amap_busy_o`'s scan (`:1179`). These lines are unchanged from main b48312e1 (the notify diff is the lock-flag lines only). OC1 runs last in every run and passes, and all 11 occupancy controls are killed.
  - Open: F1 (no interleaving case), F2 (no non-IDENTIFY CONTROL case), F3.
- **Docs:**
  - 06 §6.1/§6.8/F06.14/answers, 00 rows 15 and 16, 09 (Identify row; §8.4 "ten", counted: ten `tb/aecp_notify` rows), the suite READMEs and the command records agree with the code, except F2's scope wording, F3 and R1.
  - `make check` passes.
  - Comment-rule scan of the source delta (`hdl/`, `tb/` sources, scripts): no new lane label, lane name, review round, reviewer ID or issue-comment ID. "round" there means a notification round and "lane" a memory lane. The README record lines that say "at the lane head" and "R416-1 S1" are existing idioms in prose records and edited existing rows, not new source comments.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | issue #185/#186 bodies, assignment and correction; IEEE 1722.1-2021 §7.2.22, §7.3.5.2/§7.3.6, §7.4.2.1/Table 7-143, §7.5.2; Milan v1.2 §5.3.12, §5.4.5.1, Table 5.22; `E_RDESCCT`, `E_LOCKUNS`, `KL_aecp_notify` latches; `milan_min.json`; probes vendor and midround | R667-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |
| RTL | UNCLEAN (F1, F2) | `KL_aecp_engine.sv`, `KL_aecp_notify.sv`, `protocol_processor_top.sv`, `gen_ucode.py`, `KL_aecp_ucpu.sv` (compare/branch semantics); remerge diffs of a2cf652 and b0f6f9c; lint at the head | R667-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |
| Robustness | CLEAN (no finding of this lens alone; F1's frozen round arguments are attributed to Conformance/RTL/Tests/Docs) | coalescing paths (timeout over LOCK, LOCK over timeout), layout guards and fallbacks, miss path (probe missnop), 113-byte TAIL (probe tail), reset values | R667-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |
| Tests | UNCLEAN (F1, F2, F3) | `tb/pp_top` RDC/LN/L5b/L6d/TD1/RN, `tb/aecp_notify` LF/CQ/OC, `tb/ucpu` RC/L3/L3b; 4 suites run; 27 notify and 12 dispatch controls run; author receipts at f42c886 | R667-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |
| Docs | UNCLEAN (F2, F3; R1 is RESIDUE) | 06, 00 rows 15/16, 09, `tb/pp_top`, `tb/aecp_notify`, `tb/ucpu` READMEs, `aecp_commands.json`, `decode.json`, PR text; `make check`; comment-rule scan | R667-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |

## Real limits

- **Not run by this reviewer:**
  - The full processor bank (`run_suites.sh` over all suites).
  - Yosys synthesis and the Yosys elaboration guards.
  - The other campaigns: acmp, d3, aecp, ctr, gsi, name_wr, name_state, maap, adp, elab_guards, aecp_cmds mutants.
  - The parent consumer gates.
  These were excluded by the assignment's limits. At this head they rest on the author's receipts at `f42c886`, before the manager's merge of #190, which touched `protocol_processor_top.sv` (7 lines) and `tb/pp_top`. This reviewer's full `tb/pp_top` run and lint at `b0f6f9c` pass.
- No author or manager gate receipt exists at the exact head `b0f6f9c`.
- **Hosted CI at the head:** docs-gates and portability succeeded. Suites were still in progress when read, so no hosted suite result is claimed.
- **Evidence packet:** only the round-1c head-final gates, the comparison tables, INDEX.md and OVER-200KB.sha256 were fetched and hash-checked. The 11 over-200 KB files are in the author's scratch and were not inspected.
- Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware was used.
- F1's end-to-end frame is inferred from the notify-level probe plus `E_LOCKUNS`'s live holder read (`tb/ucpu` L3 grades flags from r14 and locked_id from the holder independently). No `tb/pp_top`-level reproduction was built.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base b48312e1, live dev e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f) with the builder and native banks at the merge turn, and link those receipts.
- Hosted and act acceptance at the final head, including the `suites` job still in progress at b0f6f9c.
- Carry R1 to the residue checklist.
- Route F1 to F3 to the author for round 2, or record owner decisions where a finding offers one.
- Consider an issue for S5 (pre-existing).

R667-1 FINISHED
