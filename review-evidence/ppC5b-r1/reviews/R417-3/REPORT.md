[R417] POSITIVE - exact head 441d64630aa0143fa43f1049a6860cd9ed60e71e

# R417-3: external independent review of PR #138 (lane C5b, AECP dispatch and response), round 3

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #76 / PR #138.
- Exact head `441d64630aa0143fa43f1049a6860cd9ed60e71e`, tree `452670bf352d425c5eb8eda9eaf8cac88a9219fa`, verified in a detached clone (`receipts/00_environment.txt`, `receipts/clone_verify.txt`).
- Round-3 assignment: #76 comment 5927100611. Review start: PR #138 comment 5932647084.
- Scope: the five commits on the round-2 head `2acd4025`:
  - `a8fe574`, the merge of processor main `3f3ea56b` (#137, lane C4);
  - `0de4234` (R417-2 F1);
  - `d6b2a23` (R417-2 S3);
  - `d2b3326` (R417-2 S1);
  - `441d646` (R417-2 S2).
- I also checked that the closed issues' acceptance still holds at this head. The suites and the lane's whole campaign were re-run here.

## Verdict

**POSITIVE.** No MINOR, MAJOR or BLOCKER is open at this head, and all five lenses are CLEAN.

- **The merge keeps both sides whole.** I re-derived it independently:
  - The automatic merge conflicts in exactly `tb/pp_top/README.md` and `tb/pp_top/sim_main.cpp`.
  - Every main-only and lane-only file equals its side.
  - Every line either side added is in the merge, except the two `one_section` lines that their union replaces.
  - `hdl/` is byte-identical to `2acd4025`.
  - All 163 campaign patches apply.
  - Main's ACMP campaign is 19 of 19 KILLED at the head. Section AC runs alone (43 checks) and inside the default build.
- **R417-2 F1 is resolved.** The `lk-prefix-zero-body` row has four cells and reads 7. All 35 README counts equal my own campaign run at the head: 35 of 35 KILLED, three controls PASS.
- **All three suggestions are taken.**
  - S3: the CI step has the same form as the other campaign steps, and both hosted runs at this head executed it: 35/35 KILLED in about 15 minutes, with the job well inside its time limit.
  - S1: the gate refuses a `parameter`-keyword `OP_*_C`, and the new fixture is load-bearing.
  - S2: a pure sentence move.
- **Suites.** Every processor suite is rc 0: 33 suites and 1,018,518 checks, with `tb/pp_top` at 8,605 = 8,367 + 20 + 218.

## Reconstruction (order followed)

1. **Contributor guidance.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md` and `docs/README.md`: the conventions, the single-source rules, the citation rules, and `make check`.
2. **Scope.**
   - Issue #76: body, with GAP-01 acceptance 1 to 4.
   - Lane assignment: 5906184962.
   - Round-2 assignment: 5921225908.
   - Round-3 assignment: 5927100611. It sets the item order, and the gate "every ... campaign KILLED in full at the merged head".
   - Issues #50, #53, #74 and #82: bodies and acceptance lists. None has comments.
   - The PR body at the head.
   - The manager's PR comments: 5915872144, 5925466380, and the review-start notice 5932647084.
3. **Interface and requirement authorities.**
   - F01.5, 03 §7, 06 §3, 06 §6.8 and the F06.14 rows, 07 §3.1 to §3.3.2, 00 §6.6, and the integrator guide's `DESC_LINE_BYTES_P` row.
   - IEEE 1722.1-2021 §7.4.21.1, §7.4.23.1, §7.4.25.1 and §9.3.5.3.3, and Milan v1.2 §5.4.1, §5.4.2.13/.15/.17 and §5.4.2.26, all as quoted in-tree and in the issues.
4. **Diff and history.**
   - `git diff 3f3ea56b..441d646`, which is the lane's whole diff against the new base: 60 files.
   - `git diff 2acd4025..441d646`: 15 files, `hdl/` empty.
   - Each round-3 commit on its own.
   - An independent re-merge (`scripts/merge_check.sh`).
5. **Public evidence.**
   - The milan-fpga tree at `28314916` named in the assignment, `review-evidence/ppC5b-r1`, is the round-2 archive and has no `author-r3`.
   - The round-3 author packet `author-r3/` is at `kebag-logic/milan-fpga@1caf41611220bcfd2c05032c46d9d49fea5842e7` (branch `ppC5b-review-evidence`, "Archive A471 round-3 packet"). I read its `HANDOFF.md`, `parent-c4-disposition.patch` and the `receipts/*` files there.
   - I did not open `reviews/`.
   - No manager evidence comment for this head exists on the issue or the PR yet. I took the stated static/builder and native bank passes as given.
6. **Prior findings.** I read the public R417-2 and R416-2 reports on the PR only after my own pass over the diff and my own probes.

## Round-3 items

### (1) The merge `a8fe574` of main `3f3ea56b` (#137)

**Clean.** Receipts: `receipts/merge_check.txt`, `receipts/patch_apply.txt`, `receipts/acmp_mutants.txt` and `receipts/pp_top_modes.txt`.

**Structure.** The parents are `2acd4025` and `3f3ea56b`, and the merge-base is `d5f73bac`. An independent `git merge` in a disposable worktree conflicts in exactly `tb/pp_top/README.md` and `tb/pp_top/sim_main.cpp`. Every other path of the automatic result is byte-equal to the published merge.

**One-sided paths.**
- The 7 main-only paths equal `3f3ea56b`: `tb/acmp_listener` (README, bench), `tb/acmp_nvm/sim_main.cpp`, `tb/maap/README.md`, `tb/pp_top/acmp_mutants.py`, and `tb/rx_validator` (README, bench).
- The 54 lane-only paths equal `2acd4025`.
- No path differs from both parents except the five both-sided files.

**Both-sided files.** In 00, 09, `pp_top_wrap.sv`, the pp_top README and `sim_main.cpp`, every line either side added (against the base) is present in the merge, with one exception. Each side's `one_section` line is replaced by their union, which is the only line in the merge that is in neither parent:

```
const bool one_section = gsi_only || name_only || d3_only || acmp_only || adp_only
                         || maap_only || aecp_only;
```

This is `tb/pp_top/sim_main.cpp:11706-11707`.
- Main's `run_acmp` call is kept (`:11714`). So are the lane's `run_aecp_dispatch_focus` and `run_aecp_response` calls (`:11710`, `:11716`).
- The default order is D3, then AC, then AD, then AX, as the README tail says.

**Nothing of #137 lost, executed at the head.**
- `--acmp-only` runs 43 checks, 0 failing.
- The default build runs 8,367: the lane's 8,324 plus AC's 43.
- `tb/acmp_listener` passes 2,988, `tb/acmp_nvm` 360 and `tb/rx_validator` 555.
- `tb/pp_top/acmp_mutants.py --jobs 1` gives 19 of 19 KILLED with goldens PASS. This also proves that every one of its exact-text edits still finds its anchor once.
- `--aecp-dispatch-only` (915), `--maap-internal-only` (34) and `--adp-only` (55) each pass alone.

**Patches.** No campaign patch anchor moved: `hdl/` is unchanged by the merge. All 163 patches pass `git apply --check` on a clean export of the head: 28 adp_engine, 27 maap, 35 aecp_dispatch and 73 srp_top. The author's receipt `merge-a8fe574.txt` reports the same partition and the same offsets on both sides.

### (2) R417-2 F1 at `0de4234`

**Resolved.** Receipt: `receipts/table_check.txt`, from `scripts/table_check.py`.

- `tb/pp_top/README.md:839` now ends `` ...ENTITY_LOCKED byte-exact` | 7 | ``. It has four cells under the four-column header at `:823`.
- I re-ran the lane's whole campaign at the head in three chunks of the driver's own `--only` (`receipts/adm_c1.txt`, `adm_c2.txt`, `adm_c3.txt` and their `*_results.json`). The result is 35 of 35 KILLED, and the `aecp-dispatch`, `aecp-line` and `line-guards` controls all PASS.
- **Table check.**
  - Every one of the 35 rows names an arm of the driver's `MUTANTS`, with the driver's named-check prefix.
  - Every last cell equals that arm's failure count in my `results.json`: 0 differing.
  - `lk-prefix-zero-body` fails 7.
  - My counts also equal the author's `aecp-dispatch-mutants-441d646.json` arm for arm.
- One other row in that README is off its header: the M12 row at `:672`, which a `||` inside a code span splits. That row predates the lane base `0451d83d` (blame `2ca3e9b8`), and the PR body discloses it. It is not this lane's.

### (3) S3 at `d6b2a23`: the CI step

**Clean.**

- `.github/workflows/hdl.yml:67-70` adds "AECP dispatch mutation campaign" to job `suites`, after the ADP campaign. Its form is the same as the SRP, MAAP and ADP steps: it puts the cached pinned Verilator v5.050 on `PATH`, then runs `make -C tb/pp_top aecp-dispatch-mutants`.
- **It runs on a hosted runner.**
  - The target needs only `python3`, `make`, `git apply` and Verilator, and the job already has all of them. `run_suites.sh` in the same job already builds `tb/pp_top` on that runner.
  - The driver copies `hdl/`, `tb/common` and `tb/pp_top` into a temp dir, ignoring `obj_*` and `*.hex`, so the earlier step's build products cannot leak in.
  - Its output defaults to `/tmp/aecp-dispatch-mutants`.
- **Its time budget.**
  - Here, with pinned 5.050 and eight build jobs, the 35 arms and three controls took about 9 minutes in three chunks (1:11, 6:55 and 1:03). The author reports 7 min 50 s as one invocation.
  - The round-2 hosted `suites` job (run 36816532863) took 75 min 24 s with the SRP, MAAP and ADP campaigns.
- **Hosted, at this exact head** (`receipts/hosted_ci.txt`): the step ran as one invocation on `ubuntu-24.04` in both `hdl` runs.
  - Push run 36870299862: 14:51:41 to 15:06:59 UTC, 15 min 18 s.
  - Pull-request run 36870303632: 14:52:46 to 15:08:06 UTC, 15 min 20 s.
  - Each printed the three controls PASS, 35 of 35 arms KILLED (0 UNPROVEN), and `38 checks: 38 PASS, 0 FAIL`. Every arm's failure count is the README's.
  - The whole `suites` job took 91 min 40 s and 92 min 47 s, within the 360-minute default job limit with large headroom. The step added about 15 minutes, about twice the local time.
- The README's campaign paragraph (`tb/pp_top/README.md:813`) says the workflow runs it. No other document lists the workflow's campaigns, so none is stale.

### (4) S1 at `d2b3326`: the opcode gate

**Clean.** Receipt: `receipts/probe_m9_gate.txt`, from `scripts/probe_m9_gate.py`.

- `RE_DECLARED` (`scripts/check_m9_opcodes.py:45`) now counts `localparam` or `parameter`. A `parameter` `OP_*_C` is then refused as unparsed, because `RE_ENGINE` reads only the canonical `localparam logic [15:0] ... = 16'hXXXX;` form.
- I probed 15 forms on disposable copies of the gate, the engine and the bench:

| Form | Result |
|---|---|
| canonical new opcode | refused, missing from `kOpcodes` |
| `parameter` (also as an alias of an existing opcode, and in a comma list) | refused, unparsed |
| untyped, `int`, uppercase radix, `bit`, comma list | refused |
| multi-line canonical | refused, missing |
| a line-commented declaration | passes, correctly |
| a comparison | passes, correctly |
| an `enum` member, a macro | pass, outside the gate's stated scope (`localparam`/`parameter`) |

- The engine declares no enum or macro opcode. Every opcode compare in `KL_aecp_engine.sv` goes through one of its 30 `OP_*_C` names.
- The selftest is 9 of 9: one parse check and eight cases, seven of which must fail, as both docstrings say.
- The round-2 pattern put back into a copy fails the new selftest ("an OP_*_C parameter fails", 8 of 9), so the new fixture is load-bearing.

### (5) S2 at `441d646`: 07 §3.3.1

**Clean.**
- The legal-line sentences now follow the 530-byte worst case and the Annex C comparison (`docs/architecture/07_memory_maps.md:287-295`). "That worst case" again follows "the largest descriptor §3.2 can produce".
- The word multisets before and after are identical: it is a pure move.
- `make check` is rc 0.

## Closed issues: acceptance at this head

Round 3 changes no RTL (`git rev-parse 2acd402:hdl` = `HEAD:hdl` = `aec2a3b7`), and each acceptance below is re-executed at the head.

| Issue | Acceptance | At `441d646` |
|---|---|---|
| #76 | 1. kOpcodes checked against every OP_*_C | Gate PASS, 30 opcodes; selftest 9 of 9; run by `run_suites.sh` before any suite |
| #76 | 2. A guard removed turns M9 red, recorded | The seven `m9-guard-*` arms are KILLED (9, 9, 9, 7, 7, 7, 7), matching the README |
| #76 | 3. 03 §7 promises no size ROM | `03_packet_engine.md:291` "response-size ROM: none ships" |
| #76 | 4. Suites green | 33 suites rc 0 |
| #74 | 1 and 2. A5b sends the six opcodes; REBOOT SUCCESS arm red | `a5b-reboot-success-arm` KILLED (1); A5b runs inside `aecp-dispatch` |
| #53 | 1 to 4. Locked arms, nothing moved, body decided (06 §6.8, value in force), CHECK_LOCK NOPs red | The six `lk-*` NOP arms and `lk-prefix-zero-body` are KILLED; 06 §6.8 and the F06.14 rows state the current-value body |
| #50 | 1 to 4. >524 via slot 4; oversize forced 0 red; page above 62 whole; 06 §3 | `ov-*`, `pg-*` KILLED (18, 4, 18, 14, 10, 4); PG arms pass in the suite |
| #82 | 1 to 4. RD after SETs; >576 frame via slot 4; model rules re-dispositioned; ceiling stated | `rd-*` KILLED; 00 §6.6 REQ-MDL rows; 07 `:211` and 03 `:280` state cdl 592 / frame 618 |

## Findings

No MINOR, MAJOR or BLOCKER finding is open.

### S1 [SUGGESTION]: hold markdown tables to their header's cell count in `make check`

- **Lenses:** Docs, Tests.
- **Where:** the root `Makefile` `check` target and `scripts/`. The gate is absent.
- **Authority and evidence:**
  - R417-2 F1 was a five-cell row under a four-column header, and `make check` stayed green.
  - At this head, `scripts/table_check.py` finds one remaining such row in `tb/pp_top/README.md` (`:672`, M12, older than the lane). The PR body names a second, `docs/guides/integrator.md:365`.
- **Impact:** none at this head. A recurrence would again hide a cell from the rendered record without any gate noticing.
- **Suggested outcome:** a small gate in `make check` that counts unescaped `|` per row against the header. The two older rows would first need their in-span `||` escaped as `\|\|`. This is optional, and could belong to the documentation-hygiene lane.

## Prior public review findings at this head

| Finding | Status at `441d646` | Evidence |
|---|---|---|
| R417-2 F1 (MINOR): the `lk-prefix-zero-body` row drops its count | **Resolved** | The row has four cells and reads 7; 35 of 35 counts equal my campaign (`table_check.txt`) |
| R417-2 S1: a `parameter` `OP_*_C` passes the gate | **Resolved** | `d2b3326`; probe 15 forms, 0 unexpected; the round-2 pattern fails the new selftest |
| R417-2 S2: 07 §3.3.1's lost antecedent | **Resolved** | `441d646`, a pure move |
| R417-2 S3: no CI step for the campaign | **Resolved** | `hdl.yml:67-70`; both hosted runs at the head executed it (35/35 KILLED, about 15 min) |
| R416-2 S-R2: the AUDIO_UNIT and CLOCK_DOMAIN short-lane guards stay ungraded | **Retained by the author, with a reason (SUGGESTION)** | The PR body's "What remains (round 3)" says no SET or restore can reach them. I accept this; it is unchanged since round 2, and `hdl/` is identical |
| R417-1 F1, F2 / R416-1 F1, F2, F3 (MINOR, round 1) | **Still resolved** | Resolved at `2acd4025` per R417-2 and R416-2. At this head `line-floor-rounded`, `line-ceiling-dropped`, `line-buffer-fixed-592`, `rb-rounded-buffer-no-page-cap` and `sctrl-badarg-zero-body` are KILLED, line guards pass 6 cases, and `git diff --check 0451d83d HEAD` is rc 0 |
| R417-1 S1, S2 / R416-1 S1, S2 (round 1) | **Still resolved or retained as recorded at round 2** | No change in round 3 touches them; RD3 and RD4 pass in the default build |

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The closed issues' acceptance re-executed at the head (table above). The IEEE 1722.1-2021 §7.4.21.1/.23.1/.25.1 value-in-force bodies (LK arms), §9.3.5.3.3 (M9, A5b), and Milan §5.4.1 / §5.4.2.26 (OV, PG) graded and mutation-proven at the head. Round 3 changes no behaviour | R417-3 | `441d64630aa0143fa43f1049a6860cd9ed60e71e` |
| RTL | CLEAN | `hdl/` tree `aec2a3b7` identical at `2acd4025` and the head (the merge brought no RTL); `lint_hdl.sh` 41 modules rc 0; every campaign patch applies to the head's `hdl/`; no port or parameter change | R417-3 | `441d64630aa0143fa43f1049a6860cd9ed60e71e` |
| Robustness | CLEAN | Independent re-merge (both sides whole, one union line); section modes `--acmp-only`, `--aecp-dispatch-only`, `--maap-internal-only` and `--adp-only` each alone; the CI step's environment, isolation and hosted execution (about 15 minutes, job about 92 of 360 minutes); the gate's 15 declaration forms; clone integrity after probes | R417-3 | `441d64630aa0143fa43f1049a6860cd9ed60e71e` |
| Tests | CLEAN | 33 suites, 1,018,518 checks, 0 failing (pp_top 8,367 + 20 + 218, fixture guards 4, line guards 6); pre-gates (58/86; selftest 9/9; 30 opcodes); AECP dispatch 35/35 with three controls, here and in both hosted runs; ACMP 19/19 with goldens; D3 sample 22/22 with goldens; name-write mutant killed; S1 is a suggestion only | R417-3 | `441d64630aa0143fa43f1049a6860cd9ed60e71e` |
| Docs | CLEAN | The pp_top README (campaign paragraph, table, AC and AX tails), 07 §3.3.1, the gate docstrings, `hdl.yml`, 00 and 09 merge lines; the PR body's round-3 sections; `make check`, `gen_matrix.py --check` and `git diff --check` (against `3f3ea56b`, `0451d83d` and `2acd402`) all rc 0 | R417-3 | `441d64630aa0143fa43f1049a6860cd9ed60e71e` |

## Commands run

All ran in the foreground, on a `git archive` export of the head in packet scratch. Builds used the pinned Verilator 5.050 through `scripts/vbin/verilator`, which rewrites `--build -j 0` to `-j 8`, one bench at a time.

| Command | rc | Result / receipt |
|---|---:|---|
| `check_upc_map.py`; `check_m9_opcodes.py --selftest` and plain | 0 | 58 constants / 86 entry points; 9 of 9; 30 opcodes (`pregates.txt`) |
| `scripts/run_some_suites.sh` (run_suites.sh's per-suite verdict) over all 33 suites, 4 chunks | 0 | 33 PASS, 1,018,518 checks (`suites.txt`, `pp_top_builds.txt`) |
| `make check`, `gen_matrix.py --check`, `./scripts/lint_hdl.sh` | 0 | docs gates OK; 94 rows, 0 untested; 41 modules (`docs_lint.txt`) |
| `git diff --check` against `3f3ea56b`, `0451d83d` and `2acd402` | 0 | (`docs_lint.txt`) |
| `aecp_dispatch_mutants.py --only ...`, 3 chunks | 0 | 35/35 KILLED, 3 controls PASS (`adm_c*.txt`, `adm_c*_results.json`) |
| `table_check.py` | 0 | 35 rows, 0 differing; 1 older row off its header (`table_check.txt`) |
| `acmp_mutants.py --jobs 1` | 0 | 19/19 KILLED, goldens PASS (`acmp_mutants.txt`) |
| `name_wr_mutant.py` | 0 | decode killed; golden and restored PASS (`name_wr_mutant.txt`) |
| `d3_mutants.py --jobs 1 --only ...`, 4 chunks (a sample) | 0 | 22 of 83 arms KILLED, goldens PASS (`d3_sample.txt`) |
| `Vpp_top_sim` with each single-section flag | 0 | AC 43, aecp-dispatch 915, MP 34, AD 55 (`pp_top_modes.txt`) |
| `merge_check.sh` | 0 | (`merge_check.txt`) |
| `patch_apply_check.sh` | 0 | 163 apply (`patch_apply.txt`) |
| `probe_m9_gate.py` | 0 | 15 forms, 0 unexpected (`probe_m9_gate.txt`) |
| `hosted_ci.sh` (read-only GET) | 0 | (`hosted_ci.txt`) |
| `clone_verify.sh` | 0 | HEAD, tree and index exact; 425 of 425 tracked entries byte- and mode-equal; no gitlinks (`clone_verify.txt`) |

## Hosted CI at the exact head (inspected, not judged)

Two `hdl` runs exist at `441d646`: 36870299862 (push) and 36870303632 (pull_request). Both completed with conclusion **success** (`receipts/hosted_ci.txt`, read-only API queries).

- `docs-gates` and `portability` succeeded.
- In `suites`, every step ran and succeeded:
  - lint and every suite (about 16 minutes);
  - the SRP, MAAP and ADP campaigns;
  - the new AECP dispatch campaign (35/35 KILLED, 38 of 38 PASS);
  - the traceability matrix;
  - the `nvm_port` figures.
- The only skipped step is "Build Verilator v5.050", skipped on a cache hit. That is the workflow's design, not a skipped gate.

I record this as inspected evidence only. Hosted and act acceptance belong to the manager.

## Real limits

- **Not re-run here.**
  - **D3 campaign: sampled, 22 of 83 arms** (`d3_sample.txt`). One first 14-arm chunk and the GSI campaign (which has no `--only`) ran past this session's 10-minute foreground bound per command, and were stopped. Their scratch temp dirs were removed, and they count as evidence neither way (`gsi_not_rerun.txt`).
  - Both campaigns edit only `hdl/` and run the `--d3-only` / `--gsi-internal-only` sections. Round 3 changes neither section's code (`d3_phases.hpp`, `gsi_internal.hpp`) nor `hdl/`. The D3 golden passes at the head in each chunk.
  - The SRP, MAAP and ADP campaigns; `srp_admission`, `acmp_talker` and `desc_mem_guard` mutants; the `nvm_port` figures; Yosys; `tb/ucpu`'s hand mutants. These belong to the manager's banks and the hosted job.
- **I ran the whole campaign in three `--only` chunks,** not as the CI step's single invocation, because of the same per-command bound. The hosted step at this head is that single invocation, and it passed.
- **The host is shared** with other lanes' builds, so wall-clock times here are indicative only.
- **Evidence pointer.** The milan-fpga commit named in the assignment (`28314916`) has no `author-r3`. The round-3 packet is at `1caf4161` on `ppC5b-review-evidence`.
- **Parent consumer set and donor bank.** Not run here. They are the manager's, at milan-fpga dev `ea3fb388` with #137's `acmp_mutants.py` disposition line (`author-r3/parent-c4-disposition.patch`).
- **Hardware.** No hardware was used. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Specification text.** The IEEE and Milan clauses are as quoted in-tree and in the issues. The PDFs are not distributed, and I did not re-read them.

## Pending manager duties

- Hosted/act acceptance at this head. Both hosted `hdl` runs completed with success, including the new AECP dispatch step. The PR body's "no hosted run of it exists yet" predates the push.
- The donor bank, and the parent consumer set at milan-fpga dev `ea3fb388` with the C4 `DUT_READER_DISPOSITIONS` line.
- Publish the manager's bank evidence for this head. None is on the issue or PR yet.
- The final current-dev candidate at the merge turn: source base `3f3ea56b`, live dev `ea3fb388`.
- Decide on S1 (optional).

R417-3 FINISHED
