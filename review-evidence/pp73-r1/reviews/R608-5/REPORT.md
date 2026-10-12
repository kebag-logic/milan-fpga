[R608] POSITIVE - exact head 4bee75b2e647507a71ece50359fceb135c334757

# R608-5: internal independent delta review of issue #73 / PR #174 (round 5, merge of main)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #174, issue #73.
- Exact head `4bee75b2e647507a71ece50359fceb135c334757`, tree `6bca4f9099adb67e6ca3758f9738975bba32d2d4`.
  Merge commit with parents `4029dc5de2a0a540d6a015c747319fbee7abba2e` (the round-4 head, R608-4 and R609-4 POSITIVE)
  and `6d536868ee2a4762ab307d5ed51ff09c01130942` (processor main: #173 traceability gate, #151 elaboration guards).
  Merge base and source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`.
- Scope of this round: the manager's round-5 instruction (issue #73 comment 6114909820). The command model was reviewed
  POSITIVE at `4029dc5d`; this review covers what the merge changes and whether everything round 4 held still holds.
- Order followed: repository conventions (no AGENTS.md or CONTRIBUTING.md exist at this head; README.md, docs/README.md
  and hdl/README.md were read), the issue body and every manager comment, the requirement row REQ-VER-002 and the
  #173 rules (09 section 8.10, `scripts/check-req-tags.py`), the merge diff and history, then the author's round-5
  public receipts. Prior public review reports were read only after the verdict and ledger below were written.

## Verdict

POSITIVE. The merge is a plain merge of `4029dc5d` and `6d536868` plus exactly the edits the round-5 instruction asks
for: the three conflicts resolved with both sides kept, the command-model section renumbered to 09 section 8.11 through
this PR's generator, one REQ-VER-002 execution tag added under #173's rules, and the five swept-input digests that
#151's HDL edits moved. Production SystemVerilog equals main byte for byte; both ROM images equal base, round 4 and main.
`make check` passes (all 231 command-gate plants caught by name; #173's static half passes). The new suite tag runs and
its removal from the evidence fails by name. #151's guard suite and its 160-arm mutation bench pass. The 16 command
controls, R608-3's echo-hide drift and every field-registry plant still fail by name.

There are no open MINOR, MAJOR or BLOCKER findings. One RESIDUE (prose placement and wording in 09 section 8.11) and one
SUGGESTION (the standing controls no longer exercise the suite's new verdict path) are recorded.

## What the merge is

Receipts: `receipts/merge_analysis.txt`, `receipts/plain_merge_vs_head.diff`.

`git merge-tree --write-tree 4029dc5d 6d536868` conflicts in exactly `Makefile`, `docs/00_MILAN_COMPLIANCE_REVIEW.md`
and `docs/architecture/09_verification.md`. `.github/workflows/hdl.yml` auto-merges. The head tree differs from that
plain-merge tree in nine files, and each difference is accounted for:

| File | Difference from the plain merge | Disposition |
|---|---|---|
| `Makefile` | conflict: `.PHONY` and `check` carry both `reqtags` (#173) and `aecpcmd` (#174); both recipes kept | both sides' targets and gates run (the `make check` receipt shows both) |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md` | conflict: main's rows taken (#173's `A; <state>` Cov form); REQ-VER-002 keeps this PR's generated Arch cell, renumbered to 09 §8.11; Doc cell `09 §1, 09 §8.11` | required: #173's `COV` pattern `^([CPAI])(?:; (.*))?$` refuses the PR's former `A (the tree: P, per Arch)` (probe `cov-pre-merge-form`); the partial-realization statement moved into 09 §8.11 |
| `docs/architecture/09_verification.md` | conflict: #173's section 8.10 kept byte for byte; this PR's section becomes 8.11 (one new paragraph); references 8.10 to 8.11 | #173's prose, waiver table and record sets equal main's (see Docs); the registry block is the generator's output |
| `docs/architecture/06_aecp_engine.md` | three cross-references 09 §8.10 to §8.11 | consequential renumbering |
| `scripts/aecp_gate/field_docs.py` | the generated Arch text names 09 §8.11 | the generator change that regenerates the Arch cell |
| `tb/aecp_cmds/Makefile`, `check_observed.py` (new), `README.md` | the suite's verdict runs through a 34-line wrapper carrying `REQ_TAG("REQ-VER-002", "DIR", "ObservedCommands.test_sweep")` | the round-5 tagging requirement |
| `tb/aecp_cmds/decode.json` | five input digests (`KL_aecp_ucpu.sv`, `KL_aecp_desc_store.sv`, `KL_aecp_nvm_writer.sv`, `KL_aecp_resp_buf.sv`, `KL_aecp_engine.sv`) | these five files are #151's code edits; every behavioral record line is unchanged (`receipts/decode_json_vs_round4.diff`), and a fresh sweep reproduces the record |

No other file differs. The command table `aecp_commands.json`, the registry `aecp_fields.json` and `gen_ucode.py` are
byte-identical to `4029dc5d`. Every `hdl/**/*.sv` file is byte-identical to main `6d536868`. Repository-wide, no `09 §8.10`
reference to the command model remains, and every §8.10 reference is to #173's section.

## Findings

### R608-5-R1 - RESIDUE (Docs) - 09 section 8.11's new paragraph splits the sentence that introduces the consumer table

- Where: `docs/architecture/09_verification.md:557-568`.
- Evidence: line 558 ends "...and so does the suite `tb/aecp_cmds` (CI's suites job):". The new tagging paragraph
  (lines 560-568) now sits between that colon and the `| Consumer | Form | Held to the table by |` table it introduces
  (at `4029dc5d` the table followed directly). The paragraph also says "its generated coverage state". #173's coverage
  record is a hand-kept table that the gate holds to what it derives, not a generated one (`check-req-tags.py` has no
  write mode; §8.10 itself says the Cov cells and the record "must equal what the gate finds").
- Impact: wording and placement only. No measurement, test, gate, generated artifact or claim changes. The registry
  block, the Arch cell and the gate are unaffected.
- Exact fix: move the paragraph that starts "The suite's `ObservedCommands.test_sweep`" so that it follows the consumer
  table rather than preceding it, and replace "so its generated coverage state is `no check`" with "so the coverage state
  the gate derives for it is `no check`".
- Verification: `make check` still passes, and line 558's colon is followed directly by the table.

### R608-5-S1 - SUGGESTION (Tests, Robustness) - the standing controls bypass the suite's new verdict path

- Where: `tb/aecp_cmds/Makefile:31-32` (`run` now executes `check_observed.py`); `tb/aecp_cmds/mutants.py:14` ("an arm
  is detected only when the suite fails") and `:156` (each arm runs `scripts/check_aecp_commands.py --observed` directly).
- Evidence: `receipts/wrapper_probe.log`. At this head, with R608-1's q1 engine edit, `make` in `tb/aecp_cmds` exits
  non-zero, prints the named FAIL lines and still writes the tag evidence: the published wrapper is correct. With the
  same edit and the wrapper planted to drop the gate's status (`...returncode and 0`), `make` exits 0. That suite would
  then be counted PASS by `run_suites.sh`, which reads exit status, and the executed traceability half would accept the
  tag. No existing control runs the `run` target, so nothing would catch it.
- Impact: none at this head. Before the merge the suite's `run` recipe and the controls' command were the same gate
  invocation; the merge adds a wrapper layer that only the probe above exercises.
- Suggested outcome: have `mutants.py` judge one arm (or all) through `make run` / `check_observed.py`, or add a
  wrapper-status plant to a self-test; adjust the docstring at `:14` to say what is run.

No other defect was found.

## Lenses

### Conformance - CLEAN

- Acceptance 1-4 of issue #73 and the manager's lane scope still hold at the merge head:
  - the table and registry are unchanged from round 4;
  - F06.14 and the registry references regenerate as a no-op: `check_aecp_commands.py --write` on a clone leaves no
    diff (`receipts/gate_probes.log`, "regen diff");
  - the gate runs in `make check` and in CI (the docs-gates and suites jobs, plus the standing-controls step,
    `.github/workflows/hdl.yml`);
  - REQ-VER-002's Arch cell and 09 §8.11 record what is generated and what is hand-written.
- #173's rule applied to this PR: REQ-VER-002 is a `lint` row, so it needs no check, and the gate derives `no check`.
  The DIR tag on `ObservedCommands.test_sweep` "labels its check and traces nothing" (09 §8.10), and a waiver on this
  row would be refused as being on a row needing no check. The Cov cell reads `A; no check`, as the gate requires. 09 §8.11
  states that the original architecture's grade remains A and that the realization is partial, which carries the
  information the old `(the tree: P, per Arch)` text held.
- `check-req-tags.py --table` lists REQ-VER-002 | lint | no check | `tb/aecp_cmds/check_observed.py:28` | DIR.
  Totals: 115 rows (101 traced, 8 waived, 6 no check), 226 tags in 19 files. Main had 225 tags in 18 files.
- No change to #173's or #151's rules was needed, and none was made: `check-req-tags.py`, `tb/common/req_tag.*` and
  `tb/elab_guards/*` equal main.

### RTL - CLEAN

- Production HDL: `git diff 6d536868 4bee75b2 -- 'hdl/*.sv'` is empty, so the elaborated engine is main's by
  construction. Under `hdl/`, only `aecp_commands.json`, `aecp_fields.json` and `gen_ucode.py` differ from main, and all
  three equal round 4.
- ROMs (`receipts/rom_digests.txt`): `gen_ucode.py` output is `518b900c…37f8` at `2cbed0a9`, `4029dc5d`, `6d536868`
  and `4bee75b2`. `gen_ltn_rom.py` output is `23cc67ee…e956` at base, main and head.
- `tb/aecp_cmds/aecp_cmds_wrap.sv` is unchanged by the merge. The sweep it elaborates is held by the digests in
  `decode.json`: the gate recomputes them and refuses a stale one by name (probe `stale-engine-digest`: "decode.json was
  swept from another hdl/aecp/KL_aecp_engine.sv").

### Robustness - CLEAN (S1 recorded, non-blocking)

Reviewer probes on a disposable clone, restored after each (`scripts/gate_probes.sh`, `receipts/gate_probes.log`):

| Probe | Result |
|---|---|
| R608-3 echo-hide, exact file edit (EAVL's three BUILD_FLD words NOPed, EAVL added to `echo_entries`) | rc 1, "schema: echo_entries: EAVL is neither a shared program without a first-entry owner nor listed in shared_entries" |
| echo-hide with EAVL also declared in `shared_entries` (membership passes) | rc 1, "rom: ENTITY_AVAILABLE: E_EAVL answers SUCCESS at cdl 12, the table's response is 32" |
| a pre-merge engine digest put back in `decode.json` | rc 1, named stale-record refusal |
| GET_STREAM_INFO opcode renumbered in the table only | rc 1, "decode: GET_STREAM_INFO: the table's entries name …, which the engine never dispatches AEM 0x004F to" |
| 09 §8.11 registry block hand-edited | rc 1, "fields: docs/architecture/09_verification.md: registry reference differs (run --write)" |
| REQ-VER-002 Arch cell given the pre-merge section number | rc 1, "fields: docs/00_MILAN_COMPLIANCE_REVIEW.md: registry reference differs" |
| Cov cell in the PR's pre-merge form | rc 1, "COV RECORD REQ-VER-002" |
| tag name no longer the test it heads | rc 1, "NAME NOT AT CHECK tb/aecp_cmds/check_observed.py:28" |
| REQ-VER-002 dropped from the coverage record | rc 1, "COVERAGE RECORD no check lint: 09 section 8.10 lacks REQ-VER-002" |
| PR body field reference, `--pr-body` check | rc 0 (the published reference equals the registry) |

### Tests - CLEAN (S1 recorded, non-blocking)

The simulator was the pinned build: its wrapper prints "Verilator 5.050 2026-07-01 rev v5.050", wrapper sha256
`905795b9…e92f`. Campaigns ran concurrently, each with its own log and rc file (`scripts/launch.sh`).

| Run | Receipt | Result |
|---|---|---|
| `make check` at head | `receipts/make_check.log` | rc 0. Lint, wavedrom, links 1192, matrix, req-tags selftest 29 plus static half OK (226 tags), modmatrix 94 rows 0 untested, params, aecp selftest 231 of 231 caught by name, aecp gate OK, ids, figures, stale |
| focused suites (`run_suites.sh` loop) with `REQ_TAG_LOG` | `receipts/suites_subset.log`, `.summary.txt`, `.req-tags.txt` | aecp_cmds 176/176 (585760 trials, 0 timeouts), elab_guards 155/155, ucpu 437/437, pp_top 10470/10470; rc 0 |
| `make -C tb/aecp_cmds mutants` | `receipts/aecp_mutants.log` | 16 of 16 detected by named failures; golden and restored PASS (q1, q2, floor, MVU, unsolicited, response-field arms included) |
| `make -C tb/elab_guards mutants JOBS=8` | `receipts/guard_mutants.log` | 160 of 160 killed, rc 0 |
| executed half, restricted to tb/aecp_cmds (`scripts/exec_probe.py`, the gate's own `check_executed`) | `receipts/gate_probes.log` | as recorded: 0 problems; with the check_observed.py evidence line removed: "DEAD TAG REQ-VER-002 tb/aecp_cmds/check_observed.py:28" |
| executed half on the author's published round-5 suites log and evidence | `receipts/exec_half_on_author_receipts.log` | rc 0, "226 evidence lines, 14 suites, OK" |
| wrapper exit status | `receipts/wrapper_probe.log` | see S1 |

The reviewer's pp_top and aecp_cmds evidence lines (129 unique) equal the author's for those two suites.

### Docs - CLEAN (R1 recorded as RESIDUE)

- #173's 09 section 8.10 is byte-identical to main from its heading to the coverage anchor. Its waiver table is
  byte-identical to main's. Its coverage record is set-equal per (state, Ver) to main's: 107 rows on each side, checked
  programmatically. The only difference is that the head re-wraps the three `traced | DIR` lines differently (REQ-MDL-001
  to 003 joined to the AEM line), which the gate reads as a union.
- This PR's section, now 8.11, differs from round 4's 8.10 only in its heading and the new tagging paragraph. Its
  registry block is the generator's output.
- The REQ-VER-002 Arch cell, the gate docstring and the PR body field reference are checked against the registry
  (probes above). The 06 cross-references, `tb/aecp_cmds/README.md`, `field_docs.py` and the PR body's round-5 section
  agree with the tree.
- The round-5 PR body claims checked directly: the table, registry and imported rules are unchanged; the 585,760-trial
  sweep gives 176 of 176; only the five digests changed in the record; the ROMs match main; there are 231 plants; the
  execution tag and its removal behave as stated (tested on the evidence line, as the body says).

## Prior public findings (read after the verdict and ledger above were written)

Every earlier finding is disposed of below at this head. The merge leaves the command model's code byte-identical to
round 4: the table, the registry, `gen_ucode.py`, `scripts/aecp_gate/*` except `field_docs.py`, `tb/aecp_cmds/sim_main.cpp`,
`aecp_cmds_wrap.sv` and `mutants.py` are unchanged. The ROMs are identical, so the resolutions accepted at `4029dc5d`
carry forward. Where a control exists, it was re-run above.

| Prior finding | Status at 4bee75b2 | Evidence this round |
|---|---|---|
| R608-1-F1 (decode/dispatch held to no table) | RESOLVED, unchanged | fresh sweep 176/176; q1, q2 and the other 14 standing controls detected by name (`aecp_mutants.log`); opcode-only table drift named (`gate_probes.log`) |
| R608-1-F2 (generator-read defects only in memory) | RESOLVED, unchanged | self-test file-copy and generator-alone plants within 231 of 231 (`make_check.log`) |
| R608-1-F3 = R609-1-F3 (doubled plurals) | RESOLVED, unchanged | `--write` regeneration is a no-op; F06.14 gate OK |
| R608-1-F4 = R609-1-F2 (`ucode.hex` prerequisites) | RESOLVED, unchanged | `tb/pp_top/Makefile`, `tb/ucpu/Makefile` and `tb/aecp_cmds/Makefile` list `aecp_commands.json` (merge leaves the rules unchanged) |
| R609-1-F1 (MAJOR: response and command sizes) | RESOLVED within disclosed scope, unchanged | size plants in the 231; `response-field-dropped` and floor controls detected |
| R608-2-F1 (echo `per` one way) | RESOLVED, unchanged | `commands[].command.per` field drift caught (`make_check.log`) |
| R608-2-F2 (`common_status`, `engine_status`, `oversize`) | RESOLVED by declaration, unchanged | registry entries held to nothing; generated references current |
| R608-2-F3 (generator refusals) | RESOLVED, unchanged | generator plants within the 231 |
| R609-2-F1 (`documented[]` semantics) | RESOLVED, unchanged | `documented[].opcode/rtl/gdi` drifts caught |
| R608-3-F1 (`echo_entries` held to nothing) | RESOLVED, unchanged | the exact echo-hide edit and the shared-key variant both fail by name (`gate_probes.log`) |
| R608-1-S1/S2, R609-1-S1..S4, R608-2-S2 | TAKEN earlier, unchanged | as recorded by R608-4 and R609-4 |
| R608-4-S1 (`shared_entries` key admits a single-use first entry to the non-SUCCESS exemption) | RETAINED as SUGGESTION | `table.py` unchanged |
| R608-3-S1, R608-2-S1 = R608-3-S2, R608-2-S3 = R608-3-S3 | RETAINED as SUGGESTIONS | `sim_main.cpp` and `aecp_cmds_wrap.sv` unchanged |
| R608-4-R1 (two hand-written size claims omit the `echo_entries` exemption) | RETAINED as RESIDUE (manager checklist) | still at `tb/aecp_cmds/README.md:69-70` and `docs/architecture/09_verification.md:581` (was :488); R608-4's exact fix applies unchanged |
| R608-4-R2 (PR body: "no existing public text is edited") | RETAINED as RESIDUE (manager checklist) | the sentence is still in the body's Round 4 section; R608-4's exact replacement applies |
| R608-2-R1 / R609-2-R1, R608-3-R1 / R609-3-R1 | Corrected in the body; historical record carried to milan-fpga #495 at merge (manager duty) | unchanged |

No earlier finding is reopened by the merge.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #73 acceptance and manager scope (rounds 1-5), REQ-VER-002 row, #173 rules (09 §8.10, `check-req-tags.py`), `--table` output, Cov/Arch cells | R608-5 | 4bee75b2e647507a71ece50359fceb135c334757 |
| RTL | CLEAN | `hdl/**/*.sv` vs main, `gen_ucode.py`/table/registry vs round 4, ROM digests at four commits, ACMP ROM at three, decode.json digests | R608-5 | 4bee75b2e647507a71ece50359fceb135c334757 |
| Robustness | CLEAN (S1) | 10 reviewer gate and traceability probes, wrapper-status probe, echo-hide in two forms, stale-digest refusal | R608-5 | 4bee75b2e647507a71ece50359fceb135c334757 |
| Tests | CLEAN (S1) | `make check`; aecp_cmds, elab_guards, ucpu and pp_top suites with tag logging; 16 command controls; 160 guard arms; executed half (subset and author receipts) | R608-5 | 4bee75b2e647507a71ece50359fceb135c334757 |
| Docs | CLEAN (R1 RESIDUE) | 09 §8.10/§8.11, 00 §6 REQ-VER-002, 06 cross-references, tb/aecp_cmds README, Makefile, hdl.yml, PR body round-5 section and field reference | R608-5 | 4bee75b2e647507a71ece50359fceb135c334757 |

## Real limits

- No full processor suite bank, Yosys bank, parent or builder bank was run (not allowed in this role). Full-bank totals
  come from the author's published round-5 receipts (head 1,029,951 checks, rc 0). The reviewer ran only the four
  suites the merge bears on. No manager source bank exists at this exact head; none is claimed or inferred.
- #151's Yosys leg was exercised only through the elab_guards suite and mutants on this host's sv2v and Yosys. The CI
  portability job (`syn/yosys/run.sh`, `guards.py --frontend yosys`) was not run here. Vivado legs were not run.
- The parent consumer's Python-style ratchets and scratch-parent gates were not run. They are author receipts
  (`comparisons/parent.txt`) and the manager's consumer bank.
- `make check`'s wavedrom freshness ran against wavedrom 2.0.3.post3, put on the module path from a local
  environment. A first attempt without it failed on the missing module and is not a repository result.
- Hosted CI at this exact head was not inspected for acceptance; the manager owns hosted and act acceptance.
- No hardware was used. Physical calibration NOT RUN; field skips are not hardware proof.
- The review clone was verified after all probes: HEAD and tree exact; index equals the HEAD tree in mode, blob and path;
  worktree bytes and modes re-hash to the index for all 618 tracked files; no untracked or ignored files; the tree has
  no gitlinks (`receipts/clone_integrity.txt`). Probes ran only in disposable clones under the packet's scratch/.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `2cbed0a9`, live dev `c20c85bd`) with the builder and
  native banks at the merge turn, and link those receipts on the PR.
- Hosted/act acceptance at the exact head.
- Carry R608-5-R1, R608-4-R1 and R608-4-R2 to the residue checklist. Carry the round-2 and round-3 wording residue
  record to milan-fpga #495 at merge, as already assigned.
- Parent consumer bank at the new pin: Python-style ratchets and the AECP/ROM-digest gates.

R608-5 FINISHED
