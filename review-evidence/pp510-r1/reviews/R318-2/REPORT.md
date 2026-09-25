[R318] POSITIVE - exact head 490e4309749c83f92d794a8ff10d3043e0f5f080

# R318-2 internal independent delta review: processor PR #118 (issues #55, #56, #77; parent milan-fpga #510)

- Exact head: `490e4309749c83f92d794a8ff10d3043e0f5f080`, tree `84028b430d19317b6bfae8931ebd15cee68388d6`. I verified both in the review clone before and after the probes.
- Round-1 head: `b51bc3893b06f4d39be49726c1b8f4ed6c65573d`, which is the merge of main `990f9652` into author commit `05fd9e1b`. Source base: `265d6762a58d9d9e545624d6d3f1a34e7006d171`.
- Round-2 authored commit: `490e430`, whose single parent is `b51bc38`. It touches four files: `docs/00_MILAN_COMPLIANCE_REVIEW.md`, `docs/architecture/06_aecp_engine.md`, `tb/pp_top/README.md` and `tb/pp_top/sim_main.cpp`.
- Review role: internal reviewer, cleared context, round R318-2 (delta). The round-2 assignment is issue #77 comment 5824629677. My round-1 ledger stands for everything the delta does not touch.

## Verdict

**POSITIVE.** No MINOR, MAJOR or BLOCKER finding is open. All five lenses are clean at this head.

- **Round-1 F1 (MINOR) is closed.** The waiver mutation section now ties every count to merged head `b51bc38` and says they are "measurements of that commit, not live suite totals". A later merge therefore cannot silently make the figures stale. I re-measured every quoted figure at `b51bc38` and each one reproduces exactly: 7,660 total, 7,640 default, 20 fixture, 197 of 7,640, 3 of 7,640, and M4's 10.
- **All three taken suggestions are in place and verified:**
  - The whole Milan note is quoted, with its spelling normalized, and a revision trigger is recorded. I checked it against the PDF.
  - 06 §11 has no phantom P-ID left.
  - The new M4L arm pins the "no lock check" claim at response level. A lock-checking RTL mutant is rejected by exactly M4L's two refusal checks.
- **Scope:** there is no RTL, microcode, synthesis, script or CI change, either in the round-2 delta or in the PR's net diff over main.
- **Probes:** my round-1 probes, re-run unchanged at this head, all behave as before.

## Findings

No open MINOR, MAJOR or BLOCKER findings.

### R318-2-S1: SUGGESTION (Tests, Docs): record the fault that M4L exists to kill

- **Where:** `tb/pp_top/README.md:503-525`, the October MVU waiver mutation section.
- **Evidence:**
  - The section's two ROM mutants are measured at `b51bc38`, before M4L existed. By design, it records nothing that M4L alone detects.
  - The generated-ROM SUCCESS mutant also turns M4L red at this head (199 of 7,646: 10 in M4 and 2 in M4L). However, it does not exercise the lock-check path that M4L guards.
  - My disposable RTL mutant makes the waived SETs 0x0001 and 0x0003 lock-checked. When another controller holds the ENTITY lock, the mutant sends them to the existing ENTITY_LOCKED refusal. It fails exactly 2 of 7,646 checks, both M4L refusal checks. No other check notices it (`receipts/13-rtl-mutant-lock-checked-waived-sets.*`).
- **Suggestion:** if the section is next refreshed, add that mutant as a row, with the head it was measured at. That way the tracked record shows M4L is the sole pin for the 06 §6.8 sentence at `docs/architecture/06_aecp_engine.md:615-616`.
- **Verdict impact:** none. The pin exists, and it is effective.

### Prior public review findings at this head

I read these only after completing my own pass over the delta. All four are resolved.

| Prior finding | Status at 490e430 | Evidence |
|---|---|---|
| R318-1-F1 = R319-1-F1 (MINOR, Tests/Docs): waiver mutation section quoted pre-merge counts | **Resolved** (see detail below) | `receipts/01b-*`, `02b-*`, `03b-*` |
| R318-1-S1 = R319-1-S1 (SUGGESTION): quote the whole note and add a revision trigger | **Resolved** (see detail below) | `receipts/00-milan-note-check.txt` |
| R319-1-S2 (SUGGESTION): last phantom P-ID in 06 §11 | **Resolved** (see detail below) | `receipts/14-p-id-audit.txt` |
| R318-1-S2 = R319-1-S3 (SUGGESTION): pin the "no lock check" behaviour | **Resolved** (see detail below) | `receipts/01-*`, `08-*`, `13-*` |

- **R318-1-F1 = R319-1-F1.**
  - `tb/pp_top/README.md:505-511` names `b51bc3893b06f4d39be49726c1b8f4ed6c65573d`, says the counts predate M4L, and says they are "measurements of that commit, not live suite totals; re-run … before quoting counts for any later head".
  - My run at `b51bc38` gives `7640 checks, 0 failures` for the default build, 20 of 20 for the fixture build, and 7,660 in total.
  - ROM word 560 gives 197 of 7,640, with the 10 M4 status and byte-exact checks failing and every length and cdl check passing. ROM word 741 = 3 gives 3 of 7,640 (M1, M2 and M5b).
  - `grep '1,966\|1,946'` over the repository returns nothing.
  - The live PR body quotes head-qualified figures that I also reproduced at `490e430`: 7,666 total, 199 of 7,646 and 3 of 7,646.
- **R318-1-S1 = R319-1-S1.**
  - `00_MILAN_COMPLIANCE_REVIEW.md:118-120` and `06_aecp_engine.md:624-626` quote both sentences, followed by "(Spelling normalized.)".
  - The printed text reads "recomendation" and "specificaiton", identically at all five clauses (§5.4.4.2 to §5.4.4.5 and §7.6).
  - The trigger "or a targeted Milan revision makes it mandatory" appears at 00:123, REQ-MVU-003/004 (00:384-385) and 06:632. No trigger wording anywhere else is inconsistent with it.
- **R319-1-S2.**
  - `06_aecp_engine.md:1241-1250`: `P-EN-TALKER-DYN-MAPPINGS-RUNNING` is removed. The line now names the F01.5 row key `MILAN_FEATURES_FLAGS.TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING` (`01_overview.md:174`) and points to §8.1, whose honesty note at 06:1092-1105 covers it.
  - Every P-ID used in 06 is now an F01.5 key.
- **R318-1-S2 = R319-1-S3.** M4L (`tb/pp_top/sim_main.cpp:2527-2574`, README:199-203, 06:615-616) does the following:
  - grades the LOCK grant byte-exact;
  - sends the complete SETs 0x0001 and 0x0003, with nonzero data, from a second controller, and checks each byte-exact NOT_IMPLEMENTED echo;
  - checks that no extra AECP frame appears in 20 ms;
  - grades the UNLOCK byte-exact.

  It passes at head (7,666 of 7,666). The lock-check mutant is rejected by exactly these two refusal checks, which also proves the lock was really held when the SETs arrived. My unchanged round-1 lock probe still passes alongside it (7,652 of 7,652).

## Scope reconstructed (public sources, in order)

1. **Repository conventions.** There is no `AGENTS.md` or `CONTRIBUTING.md` at this head; they are not among the 246 tracked files. I used `README.md` ("Building and checking") and `docs/README.md` instead:
   - §2: single-source ID registries, with F01.5 as the only P-ID home;
   - §4: citation rules;
   - §6: `make check` before commit.
2. **Issue #77.**
   - Body: GAP-03, with acceptance 1-4 including the alternative "F01.5 and F00.2 are corrected to the shipped state".
   - Scope comment 5823862684: the owner decision of 2026-09-23 waives both recommended pairs for October, no RTL change, and assignment items 1-4.
   - Round-2 assignment 5824629677: re-measure the counts or commit-qualify them, adopt S1/S2/S3, no RTL change.
   - The two REVIEW READY notes.
3. **PR #118.** The live body (head `490e430`, round-2 counts); review starts 5824213406 and 5824858884. There are no PR reviews or review comments.
4. **Authority.** Milan v1.2 Consolidated, Final Approved 2023-11-30, from a local licensed copy with the same sha256 as in round 1 (`receipts/00-milan-note-check.txt`). Only the note and the Table 5.19 rows, which the repository already quotes, are reproduced.
5. **Diff and history.**
   - `git diff 265d676..490e430`, 18 files, is the PR plus main's #115 brought in by the merge.
   - `git diff 990f965..490e430`, 8 files, is the PR's net content over main.
   - `git diff b51bc38..490e430`, 4 files, is the round-2 delta (`receipts/07-scope-and-history.txt`).
   - Live `main` is still `990f965`, so the head descends from it.
6. **Public evidence.**
   - `kebag-logic/milan-fpga@6d48f9cf…/review-evidence/pp510-r1`: I fetched `MANIFEST.json` and seven `author-r2` files, and each matches its published sha256. I did not open the `reviews/` subtree or the copied round-1 review files.
   - Hosted runs at the exact head.

## Lens evidence

### Conformance: CLEAN
- **The note quotation is exact modulo the two declared spelling fixes.** This holds in both 00 GAP-03 and 06 §6.9 (`scripts/milan_note_check.py`, `receipts/00-*`).
  - All five clause notes are textually identical.
  - Their clause mapping (§5.4.4.2 to §5.4.4.5 and §7.6) matches the citations.
- **The M4L code comment's premise is correct.** Table 5.19 gives 0 SUCCESS, 1 NOT_IMPLEMENTED, and reserves 2 to 31. So an AEM ENTITY_LOCKED status on an MVU response would be a reserved code, and the NOT_IMPLEMENTED echo under a foreign lock is the conformant answer for an unsupported command type.
- **The revision trigger reflects the note's second sentence.** It is consistent across GAP-03, REQ-MVU-003/004 and 06 §6.9. F06.14 rows 193-194 keep Lock-prot. "-", which is consistent with 06:615-616.
- **Round-1 conformance ledger stands:** Figures 5.3/5.5/5.6/5.7 lengths, Table 5.20 flags, and the waiver recorded across 00/01/02/03/07. The round-2 delta did not touch any of it.

### RTL: CLEAN
- **No RTL change.**
  - `git diff b51bc38 490e430 -- hdl syn scripts .github Makefile tb/pp_top/Makefile` is empty.
  - `git diff 990f965 490e430 -- hdl syn scripts .github Makefile` is empty.
  - The generated ROM is byte-identical at both heads (sha256 `23605682…`) (`receipts/07-*`, `15-*`).
- **The documented behaviour is what the RTL does.**
  - Only an exact MVU GET_MILAN_INFO match leaves the echo (`hdl/aecp/KL_aecp_engine.sv:1290-1296, 2827-2830`).
  - E_NOTIMPL (`hdl/aecp/ucode/gen_ucode.py:92, 567`) has no CHECK_LOCK. That is the path 06:615 describes.
  - CHECK_LOCK branches on `lock_held_i && lock_ctlr_i != controller` (`hdl/aecp/KL_aecp_ucpu.sv:309`), which is the condition my lock mutant reuses.
- **Static checks at head with the pinned simulator 5.050, identity verified** (`receipts/16-*`):
  - `scripts/lint_hdl.sh` exits 0, with 40 modules OK;
  - `scripts/check_upc_map.py` passes: 56 constants, 80 entry points (`receipts/09-*`).

### Robustness: CLEAN
- **M4L exercises the realistic adversary.** A second controller, with a different MAC and entity ID, sends complete SET forms with nonzero data while the lock is held. The 20 ms quiet window rules out a stray or second response.
- **The lock-check mutant shows the lock was really held when the SETs arrived.** The mutant fires only under `lock_held_i` by another controller. So M4L's refusal checks are not vacuous, even though the UNLOCK response alone could not prove it.
- **Round-1 robustness probes, re-run unchanged at this head:**

  | Probe | Result | Receipt |
  |---|---|---|
  | Waived-types-only SUCCESS RTL mutant | exit 1, 10 of 7,646: M4 status and byte-exact for 0x0001-0x0004 (8), plus the 2 new M4L refusals | `04-*` |
  | Any MVU type 0x0000-0x0007 answered as GET_MILAN_INFO | exit 1, 19: 16 M4, 2 M4L and M5 | `05-*` |
  | Round-1 foreign-lock probe | passes, 7,652 of 7,652 | `08-*` |

### Tests: CLEAN
- **Baselines** (pinned simulator, 8 build jobs, `git archive` extracts whose tracked bytes equal the HEAD blobs):
  - At `490e430`: `make -C tb/pp_top run` exits 0, with 7,646 default, 20 fixture and 7,666 in total (`01-*`).
  - At `b51bc38`: exit 0, with 7,640 default, 20 fixture and 7,660 in total (`01b-*`).
- **ROM mutants, using the round-1 script unchanged:**

  | Mutant | Head | Result | Receipt |
  |---|---|---|---|
  | Word 560 SUCCESS | `490e430` | exit 1, 199 of 7,646 (10 M4 and 2 M4L) | `02-*` |
  | Word 560 SUCCESS | `b51bc38` | exit 1, 197 of 7,640 (10 M4) | `02b-*` |
  | Word 741 = 1, 2 or 3 | `490e430` | each exit 1, 3 of 7,646 (M1, M2 and M5b) | `03-*` |
  | Word 741 = 3 | `b51bc38` | exit 1, 3 of 7,640 | `03b-*` |

  Every README row, its denominator and the M4 attribution reproduce exactly at the head the README names. The PR body's head figures reproduce at `490e430`.
- **The README's reproduction recipe works as written.** It uses a disposable ROM copy with `ltn_rom.hex` and `obj_dir` in the working directory, running the built binary. That is exactly what `scripts/rom_mutant.sh` does.
- **M4L's expected frames are independent of the device under test.** They are built with `aecp_frame()` and `mvu_cmd_pl()` from the figure offsets. The SUID sits at payload offset 8 (@32), the MCR user priority at offset 11 (@35), and the name at offset 16 (@40).
- **Hosted CI at the exact head:** push run 36079817702 and pull_request run 36079820839. Each executed docs-gates, suites and portability, all completed with success, and none were skipped. The hosted suites job reports `PASS pp_top (7666 checks …)` and `1014637 checks total, 0 failing` (`receipts/10-*`, `11-*`).

### Docs: CLEAN
- `make check` at head exits 0: 41 mermaid and 18 wavedrom blocks, 872 links, 115 REQ rows, 17 GAP findings, 92 module rows, 0 untested (`receipts/06-*`).
- **Round-2 prose is accurate:**
  - README M4L bullet (README:199-203);
  - 06:615-616;
  - 06 §11 (06:1241-1250);
  - the 00 and 06 note quotations.
- **The mutation section is now commit-qualified and self-describing.** No other tracked text quotes a pp_top or bank total (repo-wide search for 1,966, 1,946, 7,6xx and 1,014,6xx).
- **P-ID audit** (`scripts/p_id_audit.py`, `receipts/14-*`): 06 uses 12 P-IDs, and all are F01.5 keys.
  - Out-of-scope observation, not a finding against this PR: `P-MAAP-ACCEPT-CYC` and `P-MAAP-RSP-MS` in 02, 05 and 11 are not F01.5 keys. They predate this PR (present at base `265d676`, introduced in August) and are untouched by it.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 §5.4.4.2-.5 and §7.6 notes, Table 5.19; 00 GAP-03 and REQ-MVU-003/004; 06 §6.8 F06.9, §6.9, F06.14 rows 193-194, §11; 01 F01.5:173-174. Round-1 items stand | R318-2 (delta), R318-1 (rest) | 490e4309749c83f92d794a8ff10d3043e0f5f080 |
| RTL | CLEAN | delta and net scope, empty in hdl/syn/scripts/.github; ROM identity; `KL_aecp_engine.sv` MVU decode; `gen_ucode.py` E_NOTIMPL; `KL_aecp_ucpu.sv` CHECK_LOCK; lint_hdl; check_upc_map | R318-2 | 490e4309749c83f92d794a8ff10d3043e0f5f080 |
| Robustness | CLEAN | M4L arm; lock-checked-SET RTL mutant; round-1 RTL mutants 04/05 and lock probe 08, re-run unchanged | R318-2 | 490e4309749c83f92d794a8ff10d3043e0f5f080 |
| Tests | CLEAN | `sim_main.cpp:2388, 2527-2574`; README M4L bullet and mutation section; pp_top baselines at 490e430 and b51bc38; 6 ROM mutants; 3 RTL mutants; 1 probe; hosted runs at head | R318-2 | 490e4309749c83f92d794a8ff10d3043e0f5f080 |
| Docs | CLEAN | all 4 delta files; PR body counts; `make check`; P-ID audit; count-staleness search | R318-2 | 490e4309749c83f92d794a8ff10d3043e0f5f080 |

## Real limits

- **My executions** were:
  - pp_top, both builds, at `490e430` and `b51bc38`;
  - 6 ROM-mutant runs;
  - 3 RTL-mutant builds and 1 harness-probe build, default build only;
  - `make check`, `lint_hdl.sh` and `check_upc_map.py`.

  I did not run the full PP, parent, gPTP, Yosys or builder banks; the assignment did not allow them. The other 32 suites are covered by the hosted exact-head runs (executed, not skipped) and by the manager's banks.
- **Parent consumer:** not executed by me, and not allowed. The author's parent commit `d1d1fbba` is local and unpublished.
- **Manager evidence:** I verified the hashes of seven published `author-r2` files and cross-checked their mutation figures against my own runs. I did not re-execute the manager's static, builder or native banks.
- **A labeling quirk in that evidence:** `round2-mutation-results.json` labels its head `b51bc38`, but its harness blob `6f97ab99…` is the `490e430` `sim_main.cpp`. With `hdl/` and the ROM identical, it is content-equivalent to this head, and its figures (199 of 7,646, 3 of 7,646) match mine.
- **Hardware:** physical calibration NOT RUN. Field skips are not hardware proof. No hardware was used.
- **Specification text:** read from a locally held licensed PDF. Only text the repository already quotes is reproduced.

## Pending manager duties

1. Build the final current-dev candidate at the merge turn (source base `265d6762…`, live dev `c266432d…`), and own hosted and act acceptance.
2. Run the parent consumer check on the `508-pp-pin-adopt` line, with the gitlink at the final processor head.
3. Carried from R318-1: retire or update the parent `docs/reference/SUBMODULES.md` known-conflict row about F01.5 `P-EN-MVU-*` = 1/1 once the pin includes this change.
4. Keep REQ-MVU-005 timing in #57. It is outside this waiver.
5. Optional: R318-2-S1. Optional follow-up ticket: register or rename the pre-existing `P-MAAP-*` IDs, which are outside this PR.

## Receipts and reproduction

- **Scripts** (`scripts/`):
  - The round-1 scripts are byte-identical to the round-1 packet: `run_pp_top.sh`, `build_default_and_run.sh`, `rom_mutant.sh`, `rtl_mutant.py` and `lock_probe.py`.
  - New in this round: `rtl_lock_mutant.py`, `p_id_audit.py` and `milan_note_check.py`.
  - All scripts take tree paths as arguments. The pinned simulator is passed as `VERILATOR` or on `PATH`.
- **Receipts** (`receipts/`, numbered 00 to 16): local absolute paths are replaced by `<packet>`, `<clone>`, `<home>` and `<pinned-bin>`. Disposable trees lived only under `scratch/`, which is not published.
- **Clone integrity after all probes** (`receipts/12-clone-integrity.txt`):
  - HEAD and tree are exact;
  - status, including ignored files, is empty;
  - the index is identical to the HEAD tree (mode, blob and path);
  - all 246 worktree files re-hash to their index blobs, with modes matching;
  - there are no required gitlinks: no `.gitmodules` and zero mode-160000 entries.

R318-2 FINISHED
