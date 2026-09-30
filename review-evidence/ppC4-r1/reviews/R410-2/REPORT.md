[R410] POSITIVE - exact head 616cbdf1e54a56420e35b53cd161116702f7172d

# R410-2: internal independent review, round 2, of processor PR #137 (lane C4, ACMP; closes #45, #47, #48)

- Exact head `616cbdf1e54a56420e35b53cd161116702f7172d`, tree `d01536e57ea12cfd0f53ab4ff5cbf5178452a5d9`. Six commits on the round-1 head `a9ce0fa2`: `9151e8b`, `f55a25f`, `dbd8624`, `06a84f5`, `bf764ac`, `616cbdf`.
- Base `b2db3a970cedbbff2f8ba813acb96122c442bc58`. The review ran in a detached clone at the exact head. All builds and probes ran in disposable exports.

## Verdict

POSITIVE. At this head no finding is open at BLOCKER, MAJOR or MINOR.

- My round-1 MINOR, R410-1 F-1, is resolved.
- R410-1 S-1 and S-2, and R411-1 S1, are resolved.
- R411-1 S2 is resolved by the manager's F-1 ruling.
- R411-1 S3 and S4 are retained, each under a public manager ruling with its reason recorded in the PR body.

This round adds two suggestions, S-3 and S-4. Neither affects the verdict. Every lens is CLEAN.

## Reconstruction (order followed)

1. **Contributor rules.** This repository has no `AGENTS.md` or `CONTRIBUTING.md`. The repository `README.md`, `docs/README.md` and the suite READMEs were used. The parent's rules were used only where the PR touches them: the parent C++/Python idiom column limit of 120, and the `DUT_READER_DISPOSITIONS` form.
2. **Issue #45.** Read the frozen acceptance items 1-3 and the GAP-15 residue sentence.
3. **Manager comments on #45.** Read the lane assignment (5891906554), the round-2 assignment (5903960934) and the ruling on the STOP (5906539259, option (b)).
4. **PR #137.** Read the body at this head and the manager comments: the bank at `a9ce0fa2` (5903837095) and the review start (5910786066).
5. **Requirements and interfaces.**
   - REQ-ACMP-001 (Milan v1.2 §5.5.2.2) and GAP-15, from `docs/00_MILAN_COMPLIANCE_REVIEW.md` §5-§7 and the F00.2 caption at `:513-517`.
   - 03 V3, 05 F05.3 and F05.14, and 09 F09.4.
   - The listener transition ROM (`hdl/acmp/rom/gen_ltn_rom.py`) and the action executor order (`hdl/acmp/KL_pp_acmp_listener.sv:596-616`).
6. **Diffs and history.**
   - `git diff b2db3a97..616cbdf` (11 files, no file under `hdl/`, `syn/` or `scripts/`).
   - `git diff a9ce0fa..616cbdf`, commit by commit.
   - The revert `616cbdf` compared against `dbd8624`.
7. **Public evidence.**
   - `kebag-logic/milan-fpga@2650a1e5:review-evidence/ppC4-r1`: `author-r2/` (PR body, handoff, both parent adaptation patches, the ratchet option patch, the AS6 and timeout probes with their results) and `MANIFEST.json`.
   - The hosted check runs at the exact head.
8. **Prior reviews, read last.** The R410-1 and R411-1 findings were read only after my own pass. My independent conclusions were recorded first (receipt `60-independent-pass-notes.txt`, 12:29Z).

## Round-2 items, judged

| Item | Commit | Judgement | Evidence |
|---|---|---|---|
| R410-1 F-1: the F00.2 GAP-15 cell | `9151e8b` | **Resolved** | See below |
| PR body wording that R411-1 S2 noted | body | **Resolved** | See below |
| Parent disposition line for `protocol-processor/tb/pp_top/acmp_mutants.py` | PR body only | **Accurate; the parent-side proof is pending with the manager** | See below |
| R411-1 S1 / R410-1 S-2: the IEEE 1722.1 editions | `f55a25f` | **Resolved** | See below |
| R411-1 S4: the per-run timeout | `dbd8624`, reverted by `616cbdf` | **Retained by ruling; the revert is clean** | See below |
| R410-1 S-1: AS6 from the unbind on | `06a84f5` | **Resolved** | See below |
| Re-measured ACMP mutation table | `bf764ac` | **Reproduced exactly** | See below |

**R410-1 F-1: the F00.2 GAP-15 cell.**
- `docs/00_MILAN_COMPLIANCE_REVIEW.md:509` now reads "none found". It is the only line of 00 that changes (`git diff b2db3a97..616cbdf -- docs/00*`: +1/-1).
- The table's rule (`:513-516`) defines "none found" as "resolution implemented and a suite of the named category grades it". GAP-15's category is TOL, and F29 and AL grade that residue.
- A search of the processor issues finds no other issue that names GAP-15 as its residue. #45's body is the only carrier.
- This matches the ruling in #45 5903960934, which cites the GAP-03 precedent `05fd9e1`.
- `make check` is rc 0.

**PR body wording that R411-1 S2 noted.** The body's §1 under Round 2 now says that round 1's "per that table's own rule" overstated the rule, and that the ruling is what applies it.

**Parent disposition line for `acmp_mutants.py`.**
- The line is in the `d3_mutants.py` form. Each claim in it matches the driver:
  - it plants one listener, validator, top `st_ls_r`, bound-view or SRP-matcher defect from its own table into an isolated copy;
  - it requires every named check to fail in a completed run;
  - it reads the DUT text only to plant, and no expected value comes from that text.
- `author-r2/parent-adaptation-132-c1-c4.patch` differs from the `-c1` patch only by this 4-line entry.
- The longest line is 100 columns, within the parent's 120.
- Whether the parent consumer set passes with this line is a manager duty (see Pending).

**R411-1 S1 / R410-1 S-2: the IEEE 1722.1 editions.**
- Every IEEE table or clause citation that the lane added now names its edition. I grepped the lane's added lines, and none lacks an edition.
- `tb/acmp_nvm:176,185` is aligned.
- 09 F09.4 now reads "96-B IEEE 1722.1-2021 ACMPDU (cdl 84) and 56-B Milan ACMPDU (cdl 44, the IEEE 1722.1-2013 length)".
- The numbering agrees with independent 2021 citations:
  - the processor's own `hdl/acmp/pp_acmp_pkg.sv:119`: 2021 Table 8-3 for status;
  - the parent's 2021 traceability (8.2.1.4 message types, 8.2.1.5 status, 8.2.1.6 cdl, 8.2.1.16 flags);
  - the parent compliance matrix (Tables 8-1/8-2/8-3).
- The 96-B arithmetic holds: 56 + 2 + 2 + 2 + 2 + 16 + 16 = 96, and cdl = 84.
- Comments and one table row only. Every suite tally is unchanged.

**R411-1 S4: the per-run timeout.**
- `616cbdf` is a new commit, with no history rewrite.
- `tb/pp_top/acmp_mutants.py` is blob `cefbbeb5`, mode 100755. That is byte- and mode-identical to `a9ce0fa`.
- The README usage paragraph is textually identical to round 1's. The only README differences from `a9ce0fa` are the S-1 wording, the edition text and the re-measured table.
- S4 is recorded as retained with the ruling's reasons (#45 5906539259). I agree that a hang cannot produce a false KILLED: `judge()` counts KILLED only when the run completes with a tally.

**R410-1 S-1: AS6 from the unbind on.**
- `sim_main.cpp:9257-9261` checks `q_acmp` empty before the GET_RX_STATE feed and counts a stray frame once.
- `get_rx_state(seq, true)` (`:8916-8919`) reads the answer as the next ACMP frame.
- The author's probe plants A5 in the UNBIND×SOK cell. On a different defect, reviewer probe P4 plants A5 in GETRX×UNB: on both benches the existing 1.5-s window catches the probe that follows the answer. Residual: S-3.

**Re-measured ACMP mutation table.**
- 19 of 19 are KILLED and the three goldens PASS.
- Every build, run, completion and missing record, and every failing count, equals `tb/pp_top/README.md:1219-1232` and the `acmp_listener` and `rx_validator` READMEs:
  - pp_top AC: 1, 19, 7, 1, 7, 7, 7, 6, 2, 2, 2, 1, 5 and 5, each of 43;
  - listener: 93 of 2988; 50, 40 and 30 of 2984;
  - validator: 27 of 495.

## Findings

No BLOCKER, MAJOR or MINOR.

### S-3: SUGGESTION. Lenses: Tests, Robustness

- **Where:** `tb/pp_top/sim_main.cpp:9233`, `auto u = wait_acmp(9, 0x4815, 400);`. The same discard-while-waiting pattern appears at the other `wait_acmp` call sites in section AC.
- **Evidence:**
  - `wait_frame` pops and discards every non-matching frame. So an ACMP frame emitted after the UNBIND_RX feed but ahead of its response is never graded.
  - The listener executor runs A16 (step 11) before A7 (step 14), so such a frame is reachable.
  - Reviewer probe P2 adds A16 to the UNBIND×SETTLED_RSV_OK cell. The unbound sink then emits an unsolicited GET_RX_STATE_RESPONSE (type 0x0b, stream fields cleared, the unbind's sequence_id) ahead of the UNBIND_RX_RESPONSE.
  - P2 SURVIVES section AC on both the round-1 and the round-2 bench (43 of 43 pass).
  - A scratch-only bench edit reads the unbind response with `wait_any`. On correct RTL that stricter bench passes all 43 checks. It kills P2 on "AS6: UNBIND_RX_RESPONSE SUCCESS byte-exact", and the got/expected dump shows the 0x0b frame first.
  - Receipts: `reviewer-probes/results*.json`, `20-*` and `21-*` logs.
- **Impact:** the round-2 claim holds as written. That claim is "nothing probes the sink from the unbind on", with no ACMP frame from the UNBIND_RX_RESPONSE on. A5 is the last executor step, so a probe from the unbind cell always follows A7. However, an extra non-probe frame ahead of the response is not graded. #48's acceptance does not require it.
- **Suggested outcome:** at a later touch, read AS6's UNBIND_RX_RESPONSE, and optionally the other AC command answers, as the next ACMP frame after a `q_acmp` emptiness check, as `06a84f5` already does for the GET_RX_STATE.
- **Verification:** P2 is KILLED by a named AS6 check, and the golden passes.

### S-4: SUGGESTION. Lenses: Docs, Conformance (pre-existing text, outside the manager's item-3 list)

- **Where:**
  - `tb/rx_validator/README.md:37`: "IEEE 2013 short form accepted with tail fields ... read as 0 (F4)". The lane extended this V3 bullet with F29.
  - `tb/rx_validator/sim_main.cpp:463`: "F4: IEEE 2013 short-form ACMPDU, cdl 24", from `0b6dda19`, before the lane.
- **Evidence:** this round's 09 F09.4 row and the PR body state that the IEEE 1722.1-2013 ACMPDU is 56 B (cdl 44). So the same bullet now calls a cdl-24 frame the "IEEE 2013 short form" and, through 09, calls the 56-B form the 2013 length. I could not read either edition's text to say what F4's cdl-24 form models. The PR body's "What remains" already lists 03 V3's "2013 short forms" as out of scope.
- **Impact:** a compliance reader finds two different frames both called "the 2013 form". Behaviour and grading are unaffected.
- **Suggested outcome:** relabel F4 (for example, "a truncated short ACMPDU, cdl 24"), or add it to the manager's documentation residue with 03 V3.

## Lens analysis

**Conformance (CLEAN).**
- REQ-ACMP-001 (Milan v1.2 §5.5.2.2): F29 and AL1-AL4 pass at this head, and `cdl_not_44_rejected` is KILLED in both suites. That meets #45 acceptance items 1-3.
- The F00.2 GAP-15 cell now follows the table's own rule.
- The edition citations are consistent with the independent 2021 citations in both repositories.
- No RTL changed (`git diff b2db3a97..616cbdf -- hdl` is empty), so no behavioural conformance moved.
- S-4 is a label suggestion only.

**RTL (CLEAN).**
- No file under `hdl/` changes, and no port, parameter or register changes.
- The only non-suite source is `tb/pp_top/pp_top_wrap.sv`, which is unchanged in round 2. It connects the top's existing `acmp_bound_eid/sid/dmac/vlan_o` (`protocol_processor_top.sv:611-619,921-924`).
- `scripts/lint_hdl.sh` passes on 41 modules with both the pinned 5.050 and the system 5.052.

**Robustness (CLEAN).**
- The revert restores the round-1 driver byte for byte.
- A hang cannot turn into a false KILLED: that needs a completed tally, a non-zero exit and every named check failing.
- The S4 wall-time cost is retained by ruling.
- AS6 now fails on any ACMP frame from the unbind response to the GET_RX_STATE answer. S-3 records the pre-response residue.

**Tests (CLEAN).** At the exact head, with the pinned Verilator 5.050 and builds capped at 8 jobs:
- `tb/acmp_listener` 2988/0, `tb/rx_validator` 495/0, `tb/acmp_nvm` 360/0.
- `tb/pp_top` `make run` 7931/0, with section AC 43/0 and the build fixture 20/0.
- `acmp_mutants.py` 19/19 KILLED, with the goldens PASS.
- `gsi_mutants.py` 20 detected, golden and restored PASS.
- `name_wr_mutant.py`: decode killed, golden and restored PASS.
- Cross-check with the system 5.052: pp_top `--acmp-only` 43/0.
- The reviewer probes are described under S-3 and in `20-*`/`21-*`.

**Docs (CLEAN).**
- `make check` is rc 0 (41 mermaid + 18 wavedrom, links 976, 115 REQ / 17 GAP, 94 rows 0 untested, parameters 26), and `gen_matrix.py --check` is rc 0.
- `git diff --check` is rc 0 on `b2db3a97..616cbdf` and on `a9ce0fa..616cbdf`.
- The suite README tallies and mutation tables equal the measured values.
- The PR body's round-2 table, the parent-visible list and "What remains" match the tree.
- S-4 is a suggestion.

## Prior public review findings at this head

| Finding | Round-2 disposition | Status at `616cbdf` |
|---|---|---|
| R410-1 F-1 (MINOR) | `9151e8b`, GAP-15 cell "none found", nothing else in 00 changed | **Resolved** |
| R410-1 S-1 | `06a84f5` | **Resolved** (residue as new S-3) |
| R410-1 S-2 | `f55a25f`, F09.4 row names both editions | **Resolved** |
| R411-1 S1 | `f55a25f` | **Resolved** |
| R411-1 S2 | not taken, per the F-1 ruling (#45 5903960934); body wording corrected | **Resolved by ruling** |
| R411-1 S3 | pre-existing port-visible behaviour, on the manager's residue checklist | **Retained by ruling** (out of lane) |
| R411-1 S4 | `dbd8624` reverted by `616cbdf` (#45 5906539259) | **Retained by ruling** |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #45 acceptance; 00 F00.2 and its caption, GAP-15; 03 V3; 09 F09.4; IEEE edition citations against the in-repo and parent 2021 citations; F29/AL results; `cdl_not_44_rejected` | R410-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |
| RTL | CLEAN | `hdl/` diff (empty); `pp_top_wrap.sv`; top bound-view ports; listener ROM and executor order; `lint_hdl.sh` (5.050 and 5.052) | R410-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |
| Robustness | CLEAN | `acmp_mutants.py` (blob identity, judge rules); the revert against `dbd8624`; AS6 queue grading; probes P2/P4/strict | R410-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |
| Tests | CLEAN | 4 changed suites run; `acmp_mutants` 19/19; `gsi_mutants`; `name_wr_mutant`; 5.052 cross-check; reviewer probes on both benches | R410-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |
| Docs | CLEAN | 00 cell; 09 row; three suite READMEs; PR body round-2 text; parent disposition line; `make check`; `gen_matrix --check`; `git diff --check` | R410-2 | 616cbdf1e54a56420e35b53cd161116702f7172d |

## Commands and receipts

All commands ran in the foreground, in exports under `scratch/`, with at most 8 concurrent compile jobs.

| Receipt | Content |
|---|---|
| `receipts/00-tool-identity.txt` | Verilator identity |
| `receipts/10-*` | acmp_listener, rx_validator and acmp_nvm runs |
| `receipts/12-pp_top-5050.log` | pp_top `make run` |
| `receipts/13-*`, `receipts/14-*`, `receipts/acmp-mutants/` | ACMP mutation driver, tabulated table and per-mutant logs |
| `receipts/20-*`, `receipts/21-*`, `receipts/reviewer-probes/` | reviewer probes, via `scripts/r410_as6_probes.py` |
| `receipts/30-*` to `receipts/34-*` | diff check, matrix, `make check`, lint (5.052 and 5.050) |
| `receipts/35-*` | pp_top AC with the system 5.052 |
| `receipts/36-*`, `receipts/37-*`, `receipts/name-wr/`, `receipts/gsi/` | name_wr and gsi mutation drivers |
| `receipts/40-hosted-check-runs.txt` | hosted check runs at the exact head |
| `receipts/50-clone-integrity.txt` | clone integrity |
| `receipts/60-*` | independent-pass notes |

## Real limits

- **Verilator path.** The named path `372-manager-candidate1/pinned-tool-bin/verilator` is absent on this host. I used the manager's `372-manager-r2` wrapper instead. It has the same wrapper sha256 as in round 1 and the same Verilator 5.050 binaries: `verilator` fb2cc573…, `verilator_bin` 44898b22….
- **IEEE text.** The IEEE 1722.1-2013 and -2021 texts were not available to me. I checked edition and table numbers for consistency against independent in-repo and parent citations, not against the standard. I could not verify the 2013 table numbers (8.1/8.2/8.3) independently.
- **Not run (manager banks).** The full `run_suites.sh` sweep, `d3_mutants.py` (83 mutants), the parent consumer set, Yosys and builder banks, and hosted or act runs.
- **Hosted checks.** `docs-gates` and `portability` succeeded at the exact head. `suites` was still in progress when I checked; it is a context I only observed, not executed evidence.
- **Shared host.** Another review session was building on the same host at the same time, in separate directories. Wall times are not comparable.
- **Detached command.** One command, `gsi_mutants.py`, exceeded the session's per-command limit and was detached by the runner. I waited for it in the foreground until it completed (rc 0) before going on.
- **Clone integrity.** The clone was never modified. HEAD, tree, index and worktree are byte- and mode-identical to the exact head. This repository has no `.gitmodules` and no mode-160000 gitlinks.
- **Hardware.** Physical calibration was NOT RUN and no hardware was used. Field skips are not hardware proof.
- **Scope.** The composition with processor main (`0451d83d`, C3) and the coming C2 merge is not judged here, per the assignment.

## Pending manager duties

- Post the parent consumer bank at milan-fpga dev `ccdd07b5`, with the combined #132 + C1 adaptation and the `acmp_mutants.py` disposition line, 16 commands. `measure_test_evidence.py --check` must be rc 0 with 0 unexplained readers and `test_evidence.budget` untouched.
- Record the hosted `suites` conclusion at `616cbdf`.
- Build the final current-dev candidate at the merge turn, with source base `b2db3a97` and live dev `ccdd07b5`. Distinguish it from this source validation.
- Run the delta review after this branch merges main once C2 lands.
- Keep R411-1 S3 on the residue checklist, and optionally add S-4 there.

R410-2 FINISHED
