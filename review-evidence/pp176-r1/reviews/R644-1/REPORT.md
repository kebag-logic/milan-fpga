[R644] NEGATIVE - exact head 29f58ad30a97327d92b50f17f49d085cd97066a5

# Internal independent review R644-1: processor PR #183 (Refs #176)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #183.
- Head `29f58ad30a97327d92b50f17f49d085cd97066a5`, tree `c6fbf3914e940bf129152ba341b80d686ba30247`, one commit on processor main `22c139a4323bc96c779d13e3f6774480c5fb9b75`.
- Scope: SET_STREAM_INFO accepts the IEEE 1722.1-2013 48-byte body (cdl 60) beside the 2021 84-byte body (cdl 96). The answer is always the 2021 form. Owner decision 2026-10-17.
- Clauses: IEEE 1722.1-2021 7.4.15.1, Figure 7-40 and its NOTE; Milan v1.2 5.4.2.9.
- Verdict: **NEGATIVE**. Two findings stay open at this head.
  - F1 (MINOR, Tests), new in this round: a mutant in the PR's own new discriminator survives every suite.
  - R645-F1 (MAJOR), a prior external finding, retained after my own probe. A valid SET_STREAM_INFO longer than cdl 96 is still accepted with a response of the command's own length. That contradicts "every other length is refused" and "the response always uses the 2021 form". The behaviour is inherited from base, and the public scope has not ruled on it.
- The two-form behaviour this PR adds is correct, and the 2013-body RTL is sound.

## Reconstruction order followed

1. The processor repository has no AGENTS.md or CONTRIBUTING.md. I read the reference platform's AGENTS.md and CONTRIBUTING.md at `kebag-logic/milan-fpga@6e9bd7b5`: lenses, severities, commit rule, comment and privacy rules, and the em-dash rule.
2. Processor README.md and docs/README.md.
3. Issue #176: the body (frozen "Done when"), the owner decision 2026-10-17, the manager assignment, TAKEN and REVIEW READY.
4. Authorities in the tree: docs/architecture/06_aecp_engine.md F06.14, §6.3 and §8.1; 09_verification.md §8.1 and §8.11; 00_MILAN_COMPLIANCE_REVIEW.md REQ-AEM-009; the RX validator's V1/V2 length contract (`hdl/packet_engine/KL_pp_rx_validator.sv:39-42`).
5. `git diff 22c139a4..29f58ad3` (12 files, +210/-68) and the history.
6. Public evidence `kebag-logic/milan-fpga@6e9bd7b5:review-evidence/pp176-r1/`. All 13 files match MANIFEST.json `published_sha256`.
7. The live PR body: identical to the evidence `author/PR-BODY.md` except for one trailing newline.

I read no prior review findings and no other reviewer's report before the verdict and ledger below were written.

## Findings

### F1 - MINOR - Tests - `tb/pp_top/sim_main.cpp:8124-8131` (the 2021 `si_pl` stimulus) against `hdl/aecp/KL_aecp_engine.sv:2575-2577` (`si13_pad_w`)

- **Authority / evidence.**
  - The PR adds a new zeroing path to the echo: `si13_pad_w` zeroes every echoed payload byte from @70 when `si13_w` holds.
  - The PR states that "a 2021 command keeps its byte-exact echo, as today". 06 §6.3 says the ip fields are "echoed, never interpreted".
  - Nothing tests the negative side of the new discriminator, namely that a 2021 body is not padded. The 2021 stimulus `si_pl` leaves @70..@107 (ip_flags, both ports, both addresses) all zero. The aecp_cmds templates are zero past @52 too.
  - Reviewer mutant MUT=8 widens the pad from `si13_w` to `ssinfo_r`, so every SET_STREAM_INFO echo is zeroed from @70. It passes the default pp_top build, 9,985 checks with 0 failures (`receipts/runs/mux-pp_top-8.log`). It also leaves the aecp_cmds sweep unchanged: its only FAIL line is the planted engine's input digest, the same as the MUT=0 control (`receipts/runs/mux-aecp_cmds-8.log`, `mux-aecp_cmds-0.log`).
  - Probe (`receipts/probe-ipblock.diff`): the only change is a non-zero pattern in `si_pl`'s ip block.
    - Head behaviour (MUT=0) still passes 9,985 of 9,985 (`receipts/runs/probe-pp_top-0.log`). So the RTL is correct at this head.
    - MUT=8 then fails `W24a: SET_STREAM_INFO(ACC_LAT) byte-exact echo` (`receipts/runs/probe-pp_top-8.log`).
- **Impact.** A later edit can widen the 2013 pad to the 2021 body. One example is any of the lanes that touch the same engine (#177, #178, #181) re-gating `frame_byte`. Such an edit silently stops echoing a 2021 controller's ip fields, and no suite would notice. That breaks the claim this PR makes and leaves the confinement of the new logic to the 2013 body unpinned.
- **Required outcome.** A suite check that sends a 2021 (cdl 96) SET_STREAM_INFO with a non-zero ip block (@70..@107) and grades its echo byte-exact. Also a planted mutant recorded beside M38-M44 that widens `si13_pad_w` to every SET_STREAM_INFO and fails that check.
- **Verification.** At the new head, the default pp_top build passes. The widened-pad mutant fails the new or extended check by name.

### R1 - RESIDUE - Docs - `docs/architecture/09_verification.md:184`

- The §8.1 presentation-offset row lists the no-write refusals as "W24c-W24f, W24h, W24j-W24m, W25b, W25b3". That list leaves out W24i, the 2013-form Stream Input refusal, whose no-write is graded with the others by W24l2.
- This is wording only. No check, code or measurement changes.
- Exact fix: replace "W24h, W24j-W24m" with "W24h-W24m".

No other finding. The comment rule is clean: the raw added lines of the delta contain no bench lane label, lane name, review round, reviewer ID or issue-comment ID. Comments cite issue #176 and IEEE figures. The added lines also contain no U+2014.

## Independent lens results (before prior findings were read; the final ledger below adds R645-F1)

| Lens | Result | Evidence |
|---|---|---|
| Conformance | PASS | See the five checks after this table |
| RTL | PASS | See the RTL notes after this table |
| Robustness | PASS | See the robustness notes after this table |
| Tests | **UNCLEAN** (F1) | See the tests notes after this table |
| Docs | PASS (R1 RESIDUE only) | See the docs notes after this table |

**Conformance.** Examined `KL_aecp_engine.sv:803-813, 1558-1563, 2573-2584, 3585-3628, 3709-3718, 3756-3762` against 7.4.15.1 / Figure 7-40 and Milan 5.4.2.9, using the field offsets given in 06 §6.3 and the PR.

1. Both lengths are accepted. `si13_w` is exactly cdl 60 with 48 bytes walked, and is gated on `ssinfo_r`. The 2021 path is unchanged.
2. Both lengths share every route in the same order:
   - Stream Input: NOT_SUPPORTED;
   - streaming output: STREAM_IS_RUNNING;
   - flags not exactly MSRP_ACC_LAT_VALID (`setval_r[63:32] != SIF_ACC_LAT_C`): NOT_SUPPORTED;
   - latency bit 31: BAD_ARGUMENTS;
   - then lock and locate.
3. flags @28 and latency @48 are captured by the same walk arms for both bodies.
4. The answer is always the 2021 form: `pld_r <= SI21_PLD_C` at A_RUN, and zero from @70.
5. Every other length below cdl 96 still goes to E_SIBAD. The recorded sweep has SIBAD at "12-59, 61-95".

All of this is executed in `receipts/runs/head-pp_top-none.log` (9,985/0) and `head-aecp_cmds-none.log` (176/0).

**RTL.**
- The edits are confined to the SET_STREAM_INFO arm. Every new term is conjoined with `ssinfo_r` through `si13_w`. `ssinfo_r` is reloaded at each command pop (`:2832`) and cleared for unsolicited jobs (`:2931`). E_SINFOUNS builds its body from state (`pp_pkg.sv:275`).
- No new state, FSM arc, port, parameter or CDC. Four module-internal localparams are added. The 11-bit widths cannot overflow: 38 + 46 < 2048.
- The prefetch for a 2013 answer reads RX-slot bytes 70..107, as the 2021 path already does, inside the slot. The zero mux discards them, so no stale slot byte reaches the wire.
- The ROM is byte-identical: generated `ucode.hex` sha256 `518b900c...d37f8` at base and head, as decode.json records.
- `scripts/lint_hdl.sh` (pinned 5.050) is rc 0 and byte-identical at base and head (`receipts/gates/*-lint_hdl.*`).

**Robustness.**
- Malformed lengths: cdl 12-59 and 61-95 refuse (sweep). The neither-form 72-byte body refuses (W24m/W24m1/W24m2).
- Off-by-one recognisers are killed: cdl 59 (MUT=13) and cdl 61 (MUT=14).
- Repeated command: W24g2.
- Real streaming refusal: W25b3. Skipping it for the 2013 body (MUT=15) fails W25b3.
- The two walk-length conjuncts are mutually redundant at the top. The RX validator stores exactly cdl+12 octets and drops shorter frames (`KL_pp_rx_validator.sv:39-42`), so MUT=10 and MUT=11 are equivalent mutants there, not missing coverage.

**Tests.**
- The 7 published arms were reproduced at this head as runtime-selected mutants in one planted build (`scripts/plant_mux.py`, MUT=1..7). The FAIL lists are identical to `author/mutants/RESULTS.txt`: 8 / 7 / 6 / 6 / 6 / 8 / 9 failures.
- Every new check (W24g, W24g1, W24g2, W24i, W24j, W24k, W24l, W24l2, W24m, W24m1, W24m2, W25b3) fails under at least one arm.
- Reviewer arms 9 and 12-17 are killed. MUT=9 is killed by the aecp_cmds NSUPPE record at cdl 97-100.
- The control MUT=0 passes 9,985/0.
- Base runs 9,976 checks with 0 failures; head runs 9,985 with 0 failures (+9).
- Open: F1 (MUT=8 survives everything).

**Docs.**
- F06.14 row, 06 §6.3 and §8.1, 09 §8.1 and §8.11, `tb/aecp_cmds/README.md`, `tb/pp_top/README.md` M38-M44, `aecp_fields.json` and its two generated copies.
- `make check` is rc 0 with byte-identical logs at base and head (`receipts/gates/*-make_check.*`).
- No stale 2013-refusal text remains in the processor tree.
- The commit is one line with no trailers.

## Independent ledger (written before reading any prior finding; superseded by the final ledger below)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `hdl/aecp/KL_aecp_engine.sv` SET_STREAM_INFO arm, `si13_w`, `si13_pad_w`, A_RUN length; `tb/aecp_cmds/decode.json` 0x000E; pp_top W24/W25 runs | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| RTL | CLEAN | `hdl/aecp/KL_aecp_engine.sv` full delta and the paths it gates; `gen_ucode.py` (comments only, ROM byte-identical); lint at base and head | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| Robustness | CLEAN | length boundaries (sweep, W24m, MUT=13/14), streaming refusal (W25b3, MUT=15), validator V1 contract | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| Tests | UNCLEAN (F1) | `tb/pp_top/sim_main.cpp` W24g-W24m and W25b3, `tb/aecp_cmds/sim_main.cpp`, 18-arm mutant run, probe | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| Docs | CLEAN (R1 RESIDUE carried) | `docs/architecture/06_aecp_engine.md`, `09_verification.md`, `tb/*/README.md`, `aecp_commands.json`, `aecp_fields.json`, `check_aecp_commands.py`; `make check` | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |

## Prior public review findings at this head (read after the verdict and ledger above)

- Snapshot of PR #183: three conversation comments, no review submissions, no inline comments.
  - two review-start notices (6243620908, 6243625017);
  - the external round R645-1 (6243715823, NEGATIVE at this same head).
- Issue #176 carries no review findings.

### R645-F1 (MAJOR): longer bodies are accepted and answered at their own length. RETAINED at this head.

- **Independent check.** `receipts/probe-length.diff` adds cdl 97, 100 and 140 (plus 60 at base) to the aecp_cmds MSRP_ACC_LAT_VALID template, at both base and head. `scripts/sinfo_lengths.py` then extracts the SET_STREAM_INFO outcomes (`receipts/probe-length-{base,head}.txt`).
  - At both revisions, cdl 97, 100 and 140 dispatch to E_SINFO and answer SUCCESS at cdl 97, 100 and 140.
  - BADARG and NSUPPE answer at the command's length as well.
  - cdl 59, 61 and 95 refuse at cdl 96.
  - cdl 60 is refused at base and SUCCESS at cdl 96 at head.
- **Assessment.**
  - The PR does not introduce the behaviour. It comes from the unchanged guard `(cmd_r.cdl < 11'd96) || (pld_cmd_r < 11'd84)` (`hdl/aecp/KL_aecp_engine.sv:3612-3614`) and the echo length `pld_cmd_r` (`:3761`).
  - The longer-body echo is bounded by the RX validator, so no stale slot byte is exposed.
  - But the frozen issue says "the response always uses the 2021 form". The public assignment says "Any other length is still refused, exactly as today". The manager's review focus asks to check that "every other length is refused".
  - The PR and 06 §6.3 narrow the refusal to "any other length below cdl 96", and still claim that "every response, whichever shape the command had, is the 2021 form". The recorded sweep contradicts that claim: `tb/aecp_cmds/decode.json` NSUPPE answers "96, 97, 98, 99, 100".
  - Both the issue body and the assignment describe the base as accepting "only" cdl 96, which is not what the base does. So the literal acceptance text and the "exactly as today" wording conflict. No public ruling resolves the conflict. Under AGENTS §2 it has to be published and decided, not settled privately by the author or by a reviewer.
- My independent pass missed this. I treated the longer-body path as inherited and out of the delta, and did not test it against "every other length is refused". I correct that here.
- **Lenses.** Retained under Conformance, RTL, Robustness, Tests and Docs, as published. The length gate is RTL. Oversized input is Robustness. No valid-flag case above cdl 96 pins either outcome, which is Tests. The narrowed contract and the "always the 2021 form" claim are Docs.
- **Required outcome.** One of these two:
  - (a) Refuse every SET_STREAM_INFO length other than cdl 60 and 96 at cdl 96. Add valid-flag upper-bound checks with planted mutants, and re-record the sweep and the docs.
  - (b) Obtain an explicit public owner/manager ruling that longer bodies keep the inherited echo. Then state it in the issue scope, the PR body and 06 §6.3 / F06.14, without claiming "always the 2021 form" for them, and pin it with a valid-flag case above cdl 96.
- **Verification.** Rerun the length probe, or its in-tree successor, at the corrected head and check the decided outcome at cdl 95, 96, 97, 100 and 140.

### R645-F2 (RESIDUE): comment traceability. RETAINED IN PART as RESIDUE.

- Retained: add the requirement ID `REQ-AEM-009` beside `issue #176` at the new behavioural comment anchors (`hdl/aecp/KL_aecp_engine.sv:803`, `:1558`, `:2573`, `:3759`; `tb/pp_top/sim_main.cpp:8093`, `:8200`). This is wording only.
- Not retained: the W24 and W25 check identifiers in the new test comments. They are the suite's own check IDs. Its assertion strings, its README mutation table and 09 §8.1 already use them. They are not bench lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs under the 2026-10-15 rule.

## Final reviewer-owned ledger (after resolving prior findings)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R645-F1 retained) | engine SET_STREAM_INFO arm, `si13_w`, `si13_pad_w`, A_RUN length; decode.json 0x000E; pp_top W24/W25; length probe at base and head | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| RTL | UNCLEAN (R645-F1 retained: length guard `:3612-3614` and echo length `:3761`). The 2013-body logic itself is clean | engine full delta and gated paths; ROM byte-identical; lint base and head | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| Robustness | UNCLEAN (R645-F1 retained) | sweep 12-100, W24m, MUT=13/14/15, validator V1, cdl 97/100/140 probe | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| Tests | UNCLEAN (F1; R645-F1 retained) | pp_top W24g-W24m and W25b3, aecp_cmds templates, 18-arm mutant run, ip-block probe | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| Docs | UNCLEAN (R645-F1 retained; R1 and R645-F2 in part carried as RESIDUE) | 06 F06.14, §6.3 and §8.1; 09 §8.1 and §8.11; suite READMEs; command JSON and generated copies; PR body; `make check` | R644-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |

## Parent consumer gates (milan_dp section #67)

- The published two-row patch `review-evidence/pp176-r1/author/parent-adoption-milan_dp-67.patch` (sha256 `e142e2e7...6d3`) changes the 2013 row to expect SUCCESS at cdl 96. It also sends the already-stored 750000, so the following offset row is unchanged.
- I did not run milan_dp: a full parent bank is outside this review's allowance. The pass with the patch and the identical base/head failures rest on the author's records, which are published as hashes only (`EXTERNAL-RECORDS.csv`).
- What I checked independently:
  - The patch applies cleanly (`git apply --check`) to `tb/verilator/milan_dp/sim_nxn.cpp` at live dev `e9cbb676`.
  - Between the author's dev `7d79ffb2` and `e9cbb676`, only `docs/README.md`, `docs/testing/CI_IMAGE.md`, `scripts/check_baremetal_only.py` and `scripts/ci_*` change. `tb/verilator/milan_dp` and `tests/` are identical. Both commits pin processor `2cbed0a9`.
  - In the parent tree, only `sim_nxn.cpp` #67 grades the 2013 SET_STREAM_INFO as behaviour.
  - The two failures the author reports at both base and head (`measure_test_evidence.py --check`, `check_submodule_docs.py`) are consistent with pin lag:
    - `tb/aecp_cmds/mutants.py`, `tb/elab_guards/guards.py` and `tb/elab_guards/mutants.py` are absent at the pin `2cbed0a9` and present at base `22c139a4`;
    - this PR adds or removes no file.
- So for gates, the two-row patch is the only parent change needed. Two parent comments become false and are not touched by the patch: `tests/steps/aecp_engine_steps.py:186-190` ("the 2013 60-byte shape is itself a truncated command on the real engine; pp_top W24g pins that") and `tb/verilator/milan_dp/sim_nxn.cpp:6861-6862`. This is an adoption duty below, not a finding on this PR.
- SUGGESTION, for the adoption, not this PR: the patched #67 2013 row re-sends the stored value. So the parent cannot see that the 2013 latency is applied; only the processor suite (W24g1/W24g2) can. Sending a distinct value and restoring it would grade the effect in the parent.

## Executed by this reviewer (receipts in this packet)

- Pinned Verilator 5.050 (`--version`: "Verilator 5.050 2026-07-01 rev v5.050"). Exact-head and base trees were exported with `git archive`. Doc gates ran in local clones of this review clone.
- Builds, all rc 0 (`receipts/build/`): default pp_top at base, head, mux and probe; aecp_cmds at head and mux.
- Runs: see `receipts/SUMMARY-runs.txt`.
  - base pp_top 9,976/0;
  - head pp_top 9,985/0;
  - head aecp_cmds 176/0;
  - mux pp_top MUT=0..17 and aecp_cmds MUT=0,1,2,5,8,9,10,11,13-17;
  - probe pp_top MUT=0 and MUT=8;
  - the aecp_cmds length probe at base and head (`receipts/runs/len-*-aecp_cmds-none.*`, `receipts/probe-length-*.txt`). Its rc 2 only means the gate refused to compare: the stripped probe tree has no `docs/`. The outcomes come straight from observed.json through `scripts/sinfo_lengths.py`.
- `make check` and `scripts/lint_hdl.sh` at base and head: rc 0 and identical.
- Scripts: `scripts/plant_mux.py` (the 17 arms, with their meanings in its header), `scripts/build_tree.sh`, `scripts/run_one.sh`, `scripts/summarize.py`. Paths in receipts are rewritten to `$HOME`, `$PACKET`, `$CLONE` and `$TOOLS`.
- Not run here: `scripts/run_suites.sh` in full, the six other pp_top builds, `gen_matrix.py --check` on its own (it runs inside `make check` as `modmatrix`), `syn/yosys/run.sh`, the author's campaign set, and any parent gate. For those, source-head execution evidence is the author's published records.

## Hosted evidence at the exact head (observed 2026-10-18 01:09 UTC; the manager owns acceptance)

- Runs 39081905008 and 39081901583: `docs-gates` success and `portability` success, two contexts each. `suites` was still in progress in both, so it has no verdict yet.

## Real limits

- I had no access to the specification PDFs. The 2013 Figure 7.46 and 2021 Figure 7-40 offsets, and the identical MSRP_ACC_LAT_VALID bit, are taken from the repository's architecture text and the PR. The wording of the Figure 7-40 NOTE is not quoted or checked here.
- Physical calibration was not run. No hardware or field result is claimed.
- No manager source bank runs at this head, and none is claimed.
- The milan_dp result with the adoption patch is the author's record, not re-executed.

## Pending manager duties

- Publish a scope ruling on SET_STREAM_INFO bodies longer than cdl 96 (R645-F1, outcome (a) or (b)) before the re-review.
- Carry R1 and the retained part of R645-F2 to the residue checklist.
- The current-dev merge candidate (source base `22c139a4`, live dev `e9cbb676`): builder and native banks at the merge turn.
- Hosted `suites` verdict at the exact head.
- Textual overlap with the lanes on the same engine (#177, #178, #181). This PR edits the localparam block, `frame_byte`, the A_RUN echo branch and the SET_STREAM_INFO dispatch arm.
- Parent pin adoption. It must:
  - carry the two-row #67 patch;
  - correct the two stale parent comments named above;
  - classify the three pin-lag readers for `measure_test_evidence.py`;
  - record the pin for `check_submodule_docs.py`;
  - run `scripts/check_baremetal_only.py`, which changed on dev after the author's scratch parent.
- Issue #176 stays open until the adoption lands: the PR says "Refs".

## Clone state after probes

- No probe touched the review clone. All planted, probe and build trees live under this packet's `scratch/`, which is not published.
- Final check (`receipts/clone-state.txt`):
  - HEAD `29f58ad3` with tree `c6fbf391`; the index tree equals it;
  - porcelain status (ignored and untracked included) is empty;
  - 618 tracked entries match their raw blobs and executable modes, with 0 mismatches and none at a nonzero stage;
  - 0 gitlinks: the processor tree has no required submodule.

## Reproduction

1. Export the two revisions with `git archive 22c139a4` and `git archive 29f58ad3`. Copy the head export to `mux`, then run `python3 -I scripts/plant_mux.py <mux>`.
2. With `VERILATOR_PIN` set to the pinned 5.050 executable, run `scripts/build_tree.sh <tree> pp_top|aecp_cmds <jobs> <log> <rc>`.
3. Run `scripts/run_one.sh <tree> <suite> <MUT|none> <outdir>`, then `scripts/summarize.py <outdir>`.
4. Probes: apply `receipts/probe-ipblock.diff` to a copy of the mux tree, and `receipts/probe-length.diff` to copies of the base and head exports. Then run `scripts/sinfo_lengths.py` on the length probe's `observed.json`.

R644-1 FINISHED
