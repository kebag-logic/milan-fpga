[R691] POSITIVE - exact head 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33

# R691-1: issue #200 / PR #201, independent internal review

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Head: 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33, tree 1279c09f5b690c5e94969036baa57ccfa99eccf8 (verified in `receipts/clone-integrity.txt`)
- Base: processor main 93fb0b2d736b36588ea7321e25fba2f8819ea41f
- Parent consumer: milan-fpga dev a032c6d6e3775f145349d5a495c1e1ad12294936
- Round: R691-1, the first review round on this PR. This review started from a cleared context.

## Verdict

**POSITIVE.** There is no open BLOCKER, MAJOR or MINOR finding and no RESIDUE. All five lenses are CLEAN. One SUGGESTION (S1) is recorded below. It does not affect the verdict.

The change does what the frozen acceptance asks, and I reproduced each of the following:

- A GET_AVB_INFO with a descriptor_type other than AVB_INTERFACE answers NOT_SUPPORTED (11), echoed byte-exact at its own length. That holds whether or not the descriptor exists.
- A command under cdl 16 still answers BAD_ARGUMENTS, and an absent AVB_INTERFACE index still answers NO_SUCH_DESCRIPTOR.
- The order is unchanged: length, then type, then existence.
- The only synthesised change is one constant.
- The microcode ROM is byte-identical.
- The parent consumer gate gives identical check lines at both pins.
- `protocol_processor_top`'s area moves by −53 LUT (−0.09 %), with nothing else moving.

## Scope reconstructed

Authority order followed:

1. The repository contains no AGENTS.md or CONTRIBUTING.md. I used `README.md` and `docs/README.md` (citation and ID conventions, `make check` scope).
2. Issue #200's body and its assignment comment (issuecomment-6379943177) are the frozen acceptance. It requires:
   - the wrong-type answer NOT_SUPPORTED, echoed at its own length;
   - NO_SUCH_DESCRIPTOR and BAD_ARGUMENTS kept, in the order length, type, existence;
   - the command model, F06.14 (generated), `tb/aecp_cmds/decode.json` (re-recorded), the compliance review section 8 entry and the `tb/pp_top` V5 rows updated;
   - the ROM byte-identical or explained;
   - `make check` plus the parent milan_dp gate, with the `protocol_processor_top` area delta near 0.
3. PR #182 (merge 77cf6fb, first parent f0b1b9d) and issue #177 are the change this PR reverses.
4. Clauses, read in the standards texts:
   - IEEE 1722.1-2021 §7.4.40.1 (descriptor_type is AVB_INTERFACE), §7.4.40.3 (only NOT_AUTHENTICATED), Table 7-141 (status 1 and status 11 wording), §9.3.5.3.3 ("Any command that is received and not implemented shall be responded to with a correctly sized response and a status of NOT_IMPLEMENTED").
   - Milan v1.2 §5.4.2.2 (NOT_SUPPORTED for LOCK_ENTITY on a non-ENTITY descriptor), §5.4.2.9 (NOT_SUPPORTED for SET_STREAM_INFO on a Stream Input), §5.4.2.23 (the PAAD-AE shall implement GET_AVB_INFO per ATDECC 7.4.40).
5. `git diff 93fb0b2d..33d3010c`: 1 commit, 19 files, +141/−113 (`receipts/pr201.diff`).
6. Public evidence: milan-fpga `review-evidence/pp200-r1` at 36defd6f, which holds the author's base, head and comparison receipts, the consumer receipts and the ROM identity.

### Clause reading (focus item 5)

NOT_SUPPORTED is the right reading.

- Table 7-141 defines NOT_IMPLEMENTED by the *command type* ("does not support the command type"). It defines NOT_SUPPORTED by the *target* ("The command is implemented but the target of the command is not supported").
- Milan §5.4.2.23 makes GET_AVB_INFO a command the PAAD-AE shall implement. A GET_AVB_INFO naming another descriptor_type is therefore an implemented command with an unsupported target.
- §9.3.5.3.3 governs a command that is "received and not implemented". It does not reach this case.
- Milan uses NOT_SUPPORTED for exactly this pattern in §5.4.2.2 and §5.4.2.9, and so does this engine already for GET_STREAM_INFO and LOCK_ENTITY.
- Neither standard fixes the *size* of a non-NOT_IMPLEMENTED refusal for GET_AVB_INFO. The issue's acceptance fixes it as the command echoed at its own length, and the PR follows that. See S1 for the interoperability side, which the PR body already raises.

## Findings

### S1: SUGGESTION. Record the reference-controller sizing consequence of the command-sized NOT_SUPPORTED echo beside the decision

- **Lenses:** Conformance, Docs.
- **Where:**
  - `docs/architecture/06_aecp_engine.md:997-1013` (§6.10, "GET_AVB_INFO on another descriptor type")
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:598` (section 8, row 14)
- **Evidence:**
  - 06 §6.6 (`06_aecp_engine.md:648-655`) records that the reference controller stack accepts a command-length reflection only for NOT_IMPLEMENTED. It sizes every other non-success answer against the response form. That is why GET_COUNTERS' wrong-type NOT_SUPPORTED was moved to its full fixed body.
  - The parent's superseded traceability row CMD-15a (`docs/history/v1/traceability/ieee1722_1-2021.md:291` at a032c6d6) records that stack's GET_AVB_INFO minimum response payload of 20 bytes.
  - This PR's NOT_SUPPORTED echo is cdl 16, a 4-byte payload. The PR body's "Note for review" states this consequence, and so does the existing GET_STREAM_INFO echo.
  - The `gavb-other-type-full-body` arm shows that the V5 rows tell the two forms apart.
- **Impact:** none against the frozen acceptance, which explicitly requires the echo at its own length. A reader of 06 §6.10 or the compliance row does not learn that a reference controller may report this refusal as an incorrect payload size. A controller only sees this refusal after it sends GET_AVB_INFO to a non-AVB_INTERFACE target.
- **Suggested outcome (optional):** one sentence in 06 §6.10 that points to §6.6's sizing note. The manager may also decide whether a follow-up issue chooses the fixed-body form for GET_AVB_INFO and GET_STREAM_INFO.
- **Verification:** a doc read. No test change is needed.

### Observations (no action)

- **O1 (RTL).** The wrong-type arm's explicit `echo_r <= 1'b1` (`hdl/aecp/KL_aecp_engine.sv:3458`) is behaviourally redundant: `echo_r` is already 1 on that path. My `noecho` probe without it:
  - changed nothing in `tb/aecp_cmds` apart from the engine source digest (`receipts/probe-noecho.log`);
  - passed `tb/pp_top` aecp-dispatch with 1008 checks and 0 failures.

  The explicit assignment is harmless and arguably clearer, so I raise no finding.
- **O2 (Docs).** The issue says "section 8, item 12". In the table, the GET_AVB_INFO entry is row 14; row 12 is the SET_CONFIGURATION notification decision. The PR updates row 14 and says so in its body. That is the correct reading of the issue's intent.
- **O3 (residue scan).** The added lines name no bench lane label, lane name, review round, reviewer ID or issue-comment ID in source comments. The engine and testbench comments cite issue #200 and the clause IDs. The only nearby round or lane wording sits in docs, not in source comments, and predates this PR: "R608-1's q1" in 09, and "the round-2 head" and "the lane head" in the tb/pp_top README.

## Evidence per focus item

### (1) Behaviour

- `hdl/aecp/KL_aecp_engine.sv:3454-3463`: in the `gavb_r` arm, `cdl < 16` goes to BADARG first. Otherwise a type other than AVB_INTERFACE goes to `UPC_NSUPPE_C` with `echo_r` 1, and AVB_INTERFACE goes to `UPC_GAVB_C`, whose locate miss gives NO_SUCH_DESCRIPTOR.
- `tb/pp_top/sim_main.cpp:5748-5783` (V5): 13 byte-exact rows expect `AECP_NOT_SUPPORTED` (11) and the command echoed:
  - 11 types at cdl 16;
  - an absent CLOCK_DOMAIN 5;
  - a CLOCK_DOMAIN padded to cdl 20.
- V1, V1b, V3 and V4 are unchanged. V4 sends a 2-byte payload of type 0 (ENTITY), so it is a wrong-type short command that pins length-before-type.
- My own runs:
  - `pptop-aecp-dispatch`: A5b+M9+V 716 checks, AX 292, total 1008 with 0 failures.
  - `pptop-run` (the whole `tb/pp_top` suite, `make run`): 10,741 checks, 10,741 PASS. This equals the author's base and head figure.
- My `order` probe judges the type before the length (`receipts/probe-order.diff`). It is killed twice:
  - `tb/pp_top` fails "V4: short GET_AVB_INFO answers BAD_ARGUMENTS";
  - `tb/aecp_cmds` reports that NSUPPE becomes reachable at cdl 12-15.

  So the order is graded by both benches.

### (2) Synthesised change and ROM

- Ignoring comments, the HDL diff is the single line `UPC_NOTIMPL_C` → `UPC_NSUPPE_C`. The model's `status` and `entries` also change (`aecp_commands.json:313,317`). This is the existing E_NSUPPE program, which GET_STREAM_INFO and LOCK_ENTITY already reach.
- `receipts/rom-ident.log`: `gen_ucode.py` at base and head gives 2048 words and 92 programs each, with sha256 1f78804e…a80a8e for both and `cmp` identical. This agrees with the author's `rom-identity.txt`.
- The parent `ooc.sh --record-rom-digests` at the head pin records the same ucode and latency-ROM digests as 93fb0b2d's rows (`receipts/ooc-record-digests-head.log`).
- The `UPC_NOTIMPL_C` bound comment (`KL_aecp_engine.sv:1300-1308`) is restored to its pre-#182 text, "exactly TWO places", plus two lines on GET_AVB_INFO's NOT_SUPPORTED arm. The two assignment sites are `:1337` and `:3354`. The two `g_sub_upc_w` defaults (`:1130`, `:1200`) are record-level and predate #182, which still counted them out.

### (3) Model, generated and recorded artifacts, docs, tests

- The F06.14 row (`06_aecp_engine.md:276`) is byte-identical to the pre-#182 row at f0b1b9d.
- `make check` passes (`receipts/make-check.log`). It includes `aecpcmd`: 231 planted defects caught, 31 commands, 85 entries walked and observed, F06.14 41 rows OK. The `ids` gate scans 664 files.
- `tb/aecp_cmds`:
  - `make run`: 617,916 trials and 176 checks, all PASS.
  - `make record` re-records `decode.json` byte-identical to the committed file (`receipts/aecp-cmds-record.log`, "DECODE_JSON_UNCHANGED"). The only recorded move is AEM 0x0027's NSUPPE `{11: echo}`, cdl 16-100, floor 16 (`decode.json:159`), plus the engine digest.
- Standing controls (`tb/aecp_cmds` mutants, `--jobs 4`): 17 of 17 detected, and golden and restored both PASS. `gavb-other-type-not-implemented` fails with "decode: GET_AVB_INFO: the table's entries name NSUPPE, which the engine never dispatches AEM 0x0027 to" (`receipts/aecp-cmds-mutants.results.json`).
- Dispatch campaign, the ten GET_AVB_INFO arms plus the control (`--jobs 4`): 11 of 11 PASS. Each arm is killed by its named check, with failing counts identical to the PR body and the tb/pp_top README table:

  | Arm | Failing checks |
  |---|---|
  | m9-guard | 14 |
  | not-implemented | 13 |
  | header-only | 13 |
  | full-body | 13 |
  | gate-dropped | 13 |
  | low-byte | 2 |
  | interface-not-supported | 16 |
  | locate-miss | 1 |
  | padded-refused | 2 |
  | floor-14 | 1 |

  Source: `receipts/aecp-dispatch-gavb-arms.results.json`.
- Compliance review row 14, 06 §6.10 and §8.1, 09, the tb READMEs and the mutant driver docstrings are consistent with each other and with the RTL. A repository-wide search finds no stale NOT_IMPLEMENTED claim for GET_AVB_INFO's wrong-type answer.

### (4) Gates, campaigns, parent consumer and area

- **Parent milan_dp.** I built scratch parents from milan-fpga dev a032c6d6: one at dev's own pin 93fb0b2d, and one with a local, never-pushed commit moving the gitlink to 33d3010c. Each ran `make -j8 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2` with the pinned 5.050.
  - Both give rc 0, with `[ok]` 11,630, `[PASS]` 1,127 and `[FAIL]` 0.
  - The sorted, time-normalised check-line lists are identical: 12,764 lines, sha256 d3c036cc…8003c0, and a 0-line diff (`receipts/milan-dp.summary.txt`).
- **Area** (parent `syn/yosys/ooc.sh protocol_processor_top`, with one list row added in scratch):

  | | LUT | LUTRAM | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
  |---|---|---|---|---|---|---|---|
  | base | 57,221 | 4,076 | 26,437 | 16 | 1 | 4 | 2,369 |
  | head | 57,168 | 4,076 | 26,437 | 16 | 1 | 4 | 2,369 |

  The delta is −53 LUT (−0.09 %), about 0 as required. Both rows reproduce the author's figures exactly (`receipts/ooc-pptop-{base,head}.log`).
- **Author receipts I inspected but did not re-run:**
  - all suites: 1,030,399 checks at both ends, 0 normalised diff lines;
  - lint, the elaboration guards, the requirement-tag execution check;
  - the ACMP, AECP, counters, GSI, name-write, name-state and elaboration-guard mutant campaigns at base and head, each with 0 normalised diff;
  - notifications and D3 at the head only;
  - the `KL_pp_shadow` area: +467 LUT, explained by the author's const-only and alternative-address controls.

  Void runs are listed separately under `void/` with reasons and are not used as records.
- **Hosted checks at 33d3010c**, read-only, at the time of writing:
  - docs-gates: success, in both runs;
  - portability: success, in both runs;
  - suites: in progress, not concluded (`receipts/hosted-checks.txt`).

  Hosted and act acceptance belong to the manager.

## Prior public findings

No review finding on PR #201 predates this round: the only PR comments are the review-start notes, so nothing is resolved or retained. Issue #200's comments are the assignment, TAKEN and REVIEW READY. I did not read the concurrent round's report.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | IEEE 1722.1-2021 §7.4.40.1/.3, Table 7-141, §9.3.5.3.3; Milan v1.2 §5.4.2.2, §5.4.2.9, §5.4.2.23; compliance review row 14; 06 §6.6/§6.10; V5 expected status 11; S1 (SUGGESTION) | R691-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |
| RTL | CLEAN | `KL_aecp_engine.sv` A_PLD-exit `gavb_r` arm (3442-3466), the NOTIMPL bound comment (1298-1308), the NOTIMPL and NSUPPE sites; the HDL diff without comments is one constant; ROM identical; order and noecho probes; parent milan_dp identical; `protocol_processor_top` OOC −53 LUT | R691-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |
| Robustness | CLEAN | length, type and existence order under short (V4, wrong type), padded (V1b, V5 padded), absent index (V3, V5 CLOCK_DOMAIN 5), high-byte aliases 0x0109 and 0x8009 and 0xFFFF; message-type guard M9 with a real AVB_INTERFACE body; the aecp_cmds sweep over every cdl 12-100 and every type; order probe killed | R691-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |
| Tests | CLEAN | `tb/pp_top` V1/V1b/V3/V4/V5, aecp-dispatch 1008/0, full run 10,741/0; `tb/aecp_cmds` run 176/176 and re-record unchanged; aecp_cmds controls 17/17; ten GET_AVB_INFO dispatch arms killed by name with the documented counts; the ten patches regenerated against the head source | R691-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |
| Docs | CLEAN | `make check` pass; F06.14 equal to the pre-#182 row; 06 §6.10 and §8.1; 00 section 8 row 14; 09 decode row; tb/aecp_cmds and tb/pp_top READMEs; mutant docstrings; comment-rule scan of the delta (no new instance); S1 (SUGGESTION) | R691-1 | 33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33 |

## Real limits

- Not re-run by me (I relied on the author's published receipts):
  - the full processor suite bank (`run_suites.sh`), lint, the portability elaboration, the elaboration guards and the requirement-tag execution check;
  - the ACMP, AECP, counters, GSI, name, notification, D3 and elaboration-guard mutant campaigns;
  - the `KL_pp_shadow` OOC figures.

  None of these builds anything this PR changes beyond the engine constant already graded above.
- The consumer gate ran in my own scratch parents, not in the manager's current-dev merge candidate. No manager source bank ran at this head, and none is claimed.
- No hardware, physical calibration or field runs: physical calibration is NOT RUN. Interoperability with a reference controller (S1) is argued from the repository's own records and was not measured.
- The hosted suites job had not concluded when I checked it.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR. Accept the hosted and act results, including the suites job still in progress at 33d3010c.
- At the parent pin move, update the parent's records that still describe #177's status: `CHANGELOG.md:128` and `docs/reference/SUBMODULES.md:228` at a032c6d6. Re-record `syn/yosys/rom_digests.tsv` for the new pin; the digests are unchanged.
- Decide on S1: a one-line pointer in 06 §6.10, and whether a follow-up issue takes the fixed-body NOT_SUPPORTED form for GET_AVB_INFO and GET_STREAM_INFO.

## Receipts

The receipts are listed in `MANIFEST.sha256`. How each was produced is in `scripts/RUN.md`, and the probe edits are in `scripts/probe_edits.py`. Host roots are tokenised as `<PKT>`, `<CLONE>`, `<HOME>`, `<TOOLS>` and `<VERILATOR-5.050-ROOT>`.

R691-1 FINISHED
