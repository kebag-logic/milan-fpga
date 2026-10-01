[R417] NEGATIVE - exact head 2acd4025782bff4aabbae73252476be34ea8b00d

# R417-2: external independent review of PR #138 (lane C5b, AECP dispatch and response), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #76 / PR #138.
- Exact head `2acd4025782bff4aabbae73252476be34ea8b00d`, tree `f48cee13fd42ee303ec28e488277a3b0f17be65f`, verified in a detached clone (receipt `receipts/00-environment.txt`).
- Round-2 assignment: #76 comment 5921225908. Review start: PR #138 comment 5924932669.
- Scope: the seven commits on my round-1 head `54c1e2b1`: the merge `a4ba9f7` of main `d5f73bac`, then `b0b30ea`, `f7fa70b`, `a91fe0e`, `9437b16`, `44fda60` and `2acd402`. I also re-read the whole diff `d5f73bac..2acd4025`.
- Not judged, as instructed: the later merge of processor main `3f3ea56b` (C4).

## Verdict

**NEGATIVE, on one MINOR documentation finding.**

All six round-2 items are met in substance:
- the merge;
- SET_CONTROL's out-of-range body;
- the line-size contract (an RTL change);
- the whitespace exemption;
- the rename;
- the suggestions.

Every prior finding from R416-1 and R417-1 is resolved at this head. Every processor suite and entry point I ran is rc 0. Every arm of the lane's campaign, and of the #135 and #136 campaigns, is KILLED, with counts identical to the author's receipts.

The one open item is in the mutation record. Round 2 rewrote the README row of the issue #53 reproduction arm with a stray `|`. As a result, the table no longer renders that arm's failing-check count (F1). The fix is a one-character deletion.

## Reconstruction (order followed)

1. **Contributor guidance.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md` and `docs/README.md` (conventions, single-source rules, citation rules, and `make check` before commit).
2. **Scope decisions.**
   - Issue #76: body (GAP-01 acceptance 1 to 4).
   - Lane assignment: comment 5906184962.
   - Round-2 assignment: comment 5921225908. It sets the item order and R417-1 F1's first option (a floor of 576). It rules the rename. It makes the CI step "if any".
   - Manager's round-1 donor-bank comment on the PR: 5915872144.
   - The PR body at the head.
3. **Interface authorities.**
   - The integrator guide's `DESC_LINE_BYTES_P` row and section 5.
   - F01.5.
   - 07 §3.3.1 and §3.3.2.
   - 06 §3 and §6.8.
   - The top's parameter banners.
   - IEEE 1722.1-2021 §7.4.25.1 as quoted in-tree (the specification PDFs are not distributed).
4. **Diff and history.** `git diff d5f73bac..2acd4025`, then each round-2 commit. I re-derived the merge myself (below).
5. **Public evidence.** `kebag-logic/milan-fpga@28314916:review-evidence/ppC5b-r1`: `author-r2/HANDOFF.md`, the `author-r2/receipts/*` files, and `MANIFEST.json`. No manager evidence comment exists on the issue or PR at this head beyond the review-start notices. I took the manager's statement that the static/builder and native banks passed at this head as given, and did not re-run those banks.
6. **Prior findings.** I read the R416-1 and R417-1 findings only after my own verdict and ledger draft were written. I did not read R416-2.

## Findings

### F1 [MINOR]: the README's mutation record drops the #53 reproduction arm's failing-check count

- **Lenses:** Docs.
- **Where:** `tb/pp_top/README.md:838`, the `lk-prefix-zero-body` row of the AECP dispatch campaign table (header at `:822`; `:820` says "The last column is how many checks each arm failed at the lane head").
- **Authority:**
  - The GFM tables extension: a row with more cells than the header has the excess ignored.
  - Issue #76 acceptance 2 and the lane assignment both ask for the mutation record in `tb/pp_top/README.md`.
- **Evidence:**
  - Commit `b0b30ea` changed the row's tail from `` byte-exact` | 5 | `` to `` byte-exact` || 7 | ``. The row now has five cells under a four-column header.
  - When rendered, the "Failing checks" cell of the issue #53 reproduction is empty, and the 7 is dropped.
  - `scripts/check_md_table_cells.py` over every markdown file the PR changes finds exactly this one row (`receipts/10-md-table-cells.txt`). The same file at `54c1e2b` had no such row.
  - `make check` does not lint table shape, so it stays green.
  - The campaign itself is unaffected: the arm is KILLED with 7 failures (`receipts/04-mutants-c1.txt`), as the PR body says.
- **Impact:** the canonical, rendered mutation record no longer shows the count for the arm that reproduces issue #53. A reader of the README cannot see that the reproduction fails 7 checks.
- **Required outcome:** remove the stray `|` so the row reads `` ...ENTITY_LOCKED byte-exact` | 7 | ``.
- **Verification:** `python3 scripts/check_md_table_cells.py tb/pp_top/README.md` reports 0 rows off their header (this script is in the packet), and the rendered table shows 7 in that row.

### S1 [SUGGESTION]: the opcode gate still drops a `parameter`-keyword `OP_*_C`

- **Lenses:** Tests.
- **Where:** `scripts/check_m9_opcodes.py:44` (`RE_DECLARED` keys on `localparam`) and `:21`.
- **Evidence:** `scripts/probe_m9_gate_forms.py` (`receipts/05-probe-m9-gate-forms.txt`) tries nine forms.
  - Each form the docstring promises to refuse is refused: a comma list, a spaced radix, another width, a decimal radix, a multi-line declaration and a block comment.
  - `parameter logic [15:0] OP_GET_NAME_C = 16'h0011;` passes silently.
- **Why a suggestion:** the docstring promises "every `OP_*_C` localparam", which this meets. A body `parameter` is unlikely in this engine.
- **Suggested outcome:** match `\b(?:local)?param(?:eter)?\b`, or `OP_[A-Z0-9_]+_C\s*=` anywhere outside comments.

### S2 [SUGGESTION]: 07 §3.3.1's "That worst case" lost its antecedent

- **Lenses:** Docs.
- **Where:** `docs/architecture/07_memory_maps.md:291`.
- **What:** `f7fa70b` inserted the legal-range sentences between "the largest descriptor §3.2 can produce" and "That worst case is a STREAM_INPUT/OUTPUT ...". The sentence now reads as if it refers to the 1008 ceiling.
- **Suggested outcome:** move the range sentences after the 530-byte worst-case sentence, or open with "The largest descriptor is a ...".

### S3 [SUGGESTION]: the AECP dispatch campaign has no CI step

- **Lenses:** Tests.
- **Where:** `.github/workflows/hdl.yml:56-67`. The workflow runs the srp_top, maap and adp_engine campaigns, but not `make -C tb/pp_top aecp-dispatch-mutants`.
- **Why a suggestion:** the round-2 assignment made the CI step "if any", and the PR body says none ran. The donor bank runs the campaign. Adding it to CI (it took about 8.5 minutes here in two chunks) would keep 35 arms honest between rounds.

## Round-2 items

### (1) The merge of main `d5f73bac` (`a4ba9f7`)

**Clean.** Receipt: `receipts/14-merge.txt`, from `scripts/check_merge.sh`.

- `a4ba9f7` is a true merge with parents `54c1e2b1` and `d5f73bac`.
- `git merge-tree --write-tree 54c1e2b d5f73bac` reproduces exactly three conflicts: `tb/pp_top/Makefile`, `README.md` and `sim_main.cpp`. The published merge differs from the automatic result only in those three files.
- Each resolution keeps both sides:
  - Makefile `.PHONY`: `maap-internal` and the lane's targets together.
  - `sim_main.cpp` `main()`: `one_section` includes `maap_only` and `aecp_only`, and `run_maap_internal` is kept.
  - README: section MP, then section AX.
- `hdl/maap`, `tb/maap`, `tb/rx_validator`, `tb/adp_engine`, `tb/srp_top` and `.github` at the head equal main `d5f73bac`.
- `hdl/aecp`, `hdl/top` and `tb/ucpu` at the merge equal the lane's `54c1e2b`.
- No patch re-anchoring was needed. Every patch of every campaign passes `git apply --check` at the head (`receipts/06-patch-apply.txt`): 28 adp_engine, 27 maap, 35 aecp_dispatch and 73 srp_top.
- **#135/#136 suites:**
  - `tb/maap` 196/0, `tb/rx_validator` 497/0, `tb/adp_engine` 1367/0 (`receipts/07-*`).
  - pp_top's MP section runs inside the full pp_top run.
- **#135/#136 campaigns:**
  - MAAP campaign: 29/29 arm rows KILLED, with all three controls PASS (`receipts/08-*`).
  - ADP campaign: 30/30 KILLED, with both controls PASS (`receipts/09-*`).

### (2) SET_CONTROL out-of-range (`b0b30ea`)

**Clean.**

- **Microcode.** E_SCTRL's out-of-range arm branches to `SCTRL_EMIT`, which emits r6 (`READ_ST RGN_DYN+SEL_IDENT`, read before the lock check). This is the value in force, as IEEE 1722.1-2021 §7.4.25.1 requires ("the old value if it fails"). No RTL changed in this commit.
- **LK3b and LK3c.** Both run after LK3, with IDENTIFY at 255:
  - LK3b: the holder, under its own lock, sends SET_CONTROL(128).
  - LK3c: with the lock released, a second controller sends the same.
- Each demands, through the shared `refused()` helper:
  - BAD_ARGUMENTS byte-exact at cdl 17, carrying 255;
  - unchanged write, mark and notify counters;
  - for the second controller, no unsolicited frame at the registered holder.
- A GET and the face still read 255.
- **Mutation.** `sctrl-badarg-zero-body` (branch to `E_BADARG1`) is KILLED with 2 failures, on its named LK3b check (`receipts/04-mutants-c1.txt`).
- The parent-visible list names the change.

### (3) The line-size contract (`f7fa70b`, an RTL change)

**Clean in RTL and tests; the documentation is correct (F1 is elsewhere).**

- **RTL changes:**
  - `RESP_BUF_C = 16 + LINE_BYTES_P`, with no rounding. The uCPU's Δ8 cap is the same value.
  - Three elaboration guards refuse the line: not a multiple of 8, below 576 (`24 + 8·71 − 16`), and above 1008 (`1024 − 16`). Each message names `DESC_LINE_BYTES_P`.
  - `hdl/top` changes are comments only. No port or parameter of `protocol_processor_top` changes.
- **Tests:**
  - `line_guards.py` lints the real top. 576, 584 and 1008 lint clean. 568, 1016 and 580 are refused by name.
  - The line build (584) runs AX at 218/0. Its RB checks that the top elaborated 584, that no strobed byte lands past 600, and that the whole-line read reaches byte 600.
  - The default build runs the same RB at 592.
- **Mutation.**
  - `line-floor-rounded`, `line-ceiling-dropped`, `line-buffer-fixed-592` and `rb-rounded-buffer-no-page-cap` are all KILLED on their named checks (`receipts/04-mutants-c2.txt`).
  - My own probe removed the multiple-of-8 guard. The bench's `line guard 580` case fails, so the guard is not dead (`scripts/probe_line_step_guard.sh`, `receipts/12-probe-line-step-guard.txt`).
- **Robustness probe at the ceiling.** I built the bench's line build at `LINE_FIXTURE=1008` (`scripts/probe_line1008.sh`, `receipts/03-probe-line1008.log`).
  - AX passes at 218/0. OV1 reads a 1008-byte whole-line AUDIO_MAP (cdl 1024, frame 1050) byte-exact.
  - RB holds at 1024: the top elaborated 1008, nothing past the reservation, and the top byte reached.
  - So the documented ceiling works in simulation, including the 10-bit cursor's wrap after the final byte.
- **The parent's 576** is the floor, lints clean and runs the full default build.
- **Documentation:** the range is stated in:
  - the integrator guide row and section 5;
  - F01.5 `P-DESC-LINE-BYTES`;
  - 07 §3.3.1 and §3.3.2;
  - 06 §3;
  - the top banner;
  - the parent-visible list.

### (4) The `.gitattributes` exemption (`a91fe0e`)

**Clean.** Receipt: `receipts/13-whitespace.txt`.

- The entry `tb/pp_top/aecp_dispatch_mutations/*.patch whitespace=-blank-at-eol,-blank-at-eof` has the same form as the srp_top, maap and adp_engine entries. `git check-attr` confirms it applies to the patches and not to sources.
- `git diff --check 0451d83d HEAD` is rc 0, and `git diff --check d5f73bac HEAD` is rc 0. At the round-1 head, `git diff --check 0451d83d 54c1e2b` is rc 2.
- Every patch still applies.

### (5) The rename (`9437b16`)

**Clean.**

- The driver is now `tb/pp_top/aecp_dispatch_mutants.py`, the patches are in `aecp_dispatch_mutations/` (35 files), the target is `aecp-dispatch-mutants` and the output variable is `AECP_DISPATCH_MUTANT_OUTPUT`.
- `git grep` finds no `aecp_mutants`, `aecp_mutations`, `aecp-mutants` or `AECP_MUTANT_OUTPUT` anywhere at the head, so lane C5a's names are free. No CI step referenced the old names.
- All 35 arms are KILLED, with the three controls PASS. Every failure count equals the author's `author-r2/receipts/aecp-dispatch-mutants-2acd402.txt`.

### (6) The suggestions taken (`44fda60`, `2acd402`)

**Clean.**

- **`check_m9_opcodes.py`:**
  - It counts every `OP_*_C` localparam with comments stripped.
  - It refuses an unparsed form, and it refuses one opcode under two names.
  - The selftest is 8 of 8: one parse check and seven cases, six of which fail, as the docstrings now say.
  - The gate passes on 30 opcodes.
  - My probe confirms the refusals; one residual form is S1.
- **AX RD3:**
  - Its premise is that RD1's rows reach the device.
  - After a power cycle, both restore walks bring the GETs back to 48000, clock source 1 and the 2ch format.
  - Each READ_DESCRIPTOR then carries them, and the never-set STREAM_OUTPUT 0 stays its image.
  - `rd-base-no-overlay`'s 9 failures include the four RD3 reads.
- **AX RD4:**
  - It sets an 80-byte STREAM_OUTPUT's row, and READ_DESCRIPTOR serves the image whole.
  - `rd-str-short-guard-nop` is KILLED with 1 failure.
  - The AUDIO_UNIT and CLOCK_DOMAIN guards are retained with a stated reason: no SET or restore can set a row over a descriptor that lacks the list or count the judgment reads. I accept that reason.
- **RB counters:** RB's counters are never reset by `io.reset()`, so RB covers the whole AX run, across RD3 and RD4's power cycles.

## Prior public review findings at this head

| Finding | Status at `2acd4025` | Evidence |
|---|---|---|
| R417-1 F1 (MINOR): a 561-byte floor writes past `16 + LINE` | **Resolved** | The floor is 576 on the unrounded `16 + LINE`; the D8 cap is `16 + LINE`; RB is graded at 584 in-tree; 568 is refused by name; my 1008 probe passes |
| R417-1 F2 (MINOR): SET_CONTROL's out-of-range body is ungraded and missing from the parent-visible list | **Resolved** | LK3b/LK3c; `sctrl-badarg-zero-body` KILLED (2); listed in the parent-visible list |
| R417-1 S1: the selftest count in the docstrings | **Resolved** | The docstrings say eight fixtures, six failing; the selftest prints 8 of 8 |
| R417-1 S2: D3-restore READ_DESCRIPTOR is ungraded | **Resolved** | AX RD3 |
| R416-1 F1 (MINOR): same as R417-1 F2 | **Resolved** | As above, with the store write, mark and notify all checked |
| R416-1 F2 (MINOR): an undocumented 1008 ceiling, and "At least 561" | **Resolved** | The range 576..1008 in steps of 8 is stated in the guide, F01.5 and 07 §3.3.1; the ceiling is refused naming `DESC_LINE_BYTES_P`; the parent-visible list carries it (the floor is 576 by the manager's ruling, not the 568 R416-1 proposed) |
| R416-1 F3 (MINOR): `git diff --check` rc 2 | **Resolved** | rc 0 (`receipts/13-whitespace.txt`) |
| R416-1 S1: the overlays' short guards are ungraded | **Taken in part** | The STREAM guard is graded (RD4, KILLED); the AUDIO_UNIT and CLOCK_DOMAIN guards are retained with a reason I accept |
| R416-1 S2: gate robustness and wording | **Resolved** | 44fda60; the residual form is my S1 |

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | E_SCTRL microcode and the IEEE 1722.1-2021 §7.4.25.1 body rule (LK3b/LK3c); the Milan §5.4.1 Δ8 ceiling and §5.4.2.26 page bound at the new line contract; RD3 against 06 §6.1 / 07 §3.3 "a SET or the D3 restore"; no other behaviour changes in round 2 | R417-2 | `2acd4025782bff4aabbae73252476be34ea8b00d` |
| RTL | CLEAN | `KL_aecp_engine.sv:895-940` (buffer, three guards), the `KL_aecp_ucpu.sv` D8 cap and cursor, `ucpu_pkg.sv`, `KL_aecp_resp_buf.sv` drop fence; the top's changes are comment-only; lint_hdl 41 modules clean (`receipts/01b-lint_hdl-full.txt`); AX at 576, 584 and 1008 | R417-2 | `2acd4025782bff4aabbae73252476be34ea8b00d` |
| Robustness | CLEAN | Ceiling simulated (1008 probe); the step guard's removal caught; merge sides byte-equal; every campaign patch applies; the clean `git archive` export builds; RB counters persist across power cycles | R417-2 | `2acd4025782bff4aabbae73252476be34ea8b00d` |
| Tests | CLEAN | pp_top 8562/0 over three builds plus fixture and line guards; ucpu 398/0; maap, rx_validator and adp_engine suites; 35/35 dispatch, 29/29 MAAP and 30/30 ADP KILLED; pre-gates and selftest; `git diff --check`; S1 and S3 are suggestions only | R417-2 | `2acd4025782bff4aabbae73252476be34ea8b00d` |
| Docs | **UNCLEAN** (F1) | Integrator guide, F01.5, 06 §3/§6.1/§6.8, 07 §3.3.1/§3.3.2, 09, 00 GAP-08 row, the top banners, the pp_top README (AX, campaign table and prose), the PR body's parent-visible list; `make check` rc 0; table-shape scan finds F1; S2 is wording only | R417-2 | `2acd4025782bff4aabbae73252476be34ea8b00d` |

## Commands run (foreground; builds in packet scratch on a `git archive` export of the head)

| Command | rc | Result / receipt |
|---|---:|---|
| `scripts/check_upc_map.py`; `check_m9_opcodes.py --selftest` and plain | 0 | 58 constants / 86 entry points; 8 of 8; 30 opcodes (`01-gates.txt`) |
| `git diff --check d5f73bac HEAD`, `git diff --check 0451d83d HEAD` | 0, 0 | `01-gates.txt`, `13-whitespace.txt` |
| `./scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check` | 0 | 41 modules (`01b-lint_hdl-full.txt`; `01-gates.txt` keeps only the last 25 lines); docs gates OK (`01-gates.txt`) |
| `make -C tb/pp_top` (fixture guards, line guards, three builds) | 0 | 8562 = 8324 + 20 + 218, 0 failing (`02-pp_top-make.log`) |
| `make -C tb/pp_top LINE_FIXTURE=1008 aecp-line` (probe) | 0 | AX 218/0 at 1008 (`03-probe-line1008.log`) |
| `aecp_dispatch_mutants.py --only ...`, 2 chunks | 0, 0 | 35/35 KILLED, three controls PASS (`04-mutants-c*.txt`, `04-mutants/`) |
| `probe_m9_gate_forms.py` | — | 8 of 9 forms as expected; `parameter` form silent (S1) (`05`) |
| `git apply --check` on every campaign patch | 0 | 163 patches apply (`06`) |
| `make` in `tb/maap`, `tb/rx_validator`, `tb/adp_engine`, `tb/ucpu` | 0 | 196, 497, 1367, 398 checks, 0 failing (`07-*`) |
| `tb/maap/mutants.py --only ...`, 2 chunks | 0, 0 | 29/29 rows KILLED (`08-*`) |
| `tb/adp_engine/mutants.py --only ...`, 2 chunks | 0, 0 | 30/30 KILLED (`09-*`) |
| `check_md_table_cells.py` over the changed markdown | — | 1 row (F1) (`10`) |
| `probe_line_step_guard.sh` | 2 (expected) | `line guard 580` fails with the guard removed (`12`) |
| `check_merge.sh` | 0 | (`14-merge.txt`) |
| Clone integrity | — | index, modes and blobs equal HEAD; 0 mismatching blobs of 424; no gitlinks (`15-clone-verify.txt`) |

## Real limits

- **Verilator identity.** The scoped Verilator path named in the assignment does not exist on this host. I used the Verilator 5.050 binary that another pinned wrapper in the same tool area execs, through my own wrapper in packet scratch. Its identity (version string and sha256) is in `receipts/00-environment.txt`. The author used 5.052; the results agree.
- **Parallelism.** The first pp_top run, the 1008 probe and the first mutation chunk used the bench's own `--build -j 0` without a CPU pin, so their C++ compiles could use more than 8 cores. Every later run was pinned to 8 CPUs. Only one bench ran at a time.
- **Banks not run.** I did not run the full processor bank (`run_suites.sh` over all 33 suites), Yosys, the D3/gsi/name/srp_top/srp_admission/acmp/desc_mem_guard campaigns, or `tb/ucpu`'s hand mutants. Those are the manager's banks. The suites I did run are the ones the round-2 commits and the merge touch.
- **Parent consumer set.** Not run: it is the manager's, at milan-fpga dev `e4b771f9`.
- **Hosted CI at the exact head.** `docs-gates` and `portability` completed with success. `suites` was still `in_progress` when I last checked (`receipts/11-hosted-checks-final.txt`). I did not judge hosted or act acceptance; that belongs to the manager.
- **Hardware.** No hardware was used. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Specification text.** The IEEE and Milan clauses are as quoted in-tree and in the issue. The PDFs are not distributed, and I did not re-read them.

## Pending manager duties

- Return F1 to the author: a one-character fix in `tb/pp_top/README.md:838`.
- Re-run, at the fixed head:
  - the donor bank;
  - the parent consumer set at milan-fpga dev `e4b771f9`;
  - the hosted `suites` job.
- The later merge-only round onto processor main `3f3ea56b` (C4), which conflicts in `tb/pp_top`.
- Hosted/act acceptance and the final current-dev candidate build (source base `d5f73bac`, live dev `e4b771f9`).

R417-2 FINISHED
