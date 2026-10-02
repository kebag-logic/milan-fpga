[R421] NEGATIVE - exact head 95a78c099ee5aa914521975355adc1dfef99d01c

# R421-4: external delta review of processor PR #139 (lane C6, notifications and Identify), rounds 4 and 4b

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #80, PR #139 (closes #54, #58, #80, #86).
- Exact head `95a78c099ee5aa914521975355adc1dfef99d01c`, tree `d0be0f91665f4e6b8e16bfa3aa8f53bbeaff518f`.
- Scope: a delta review of the two merge commits on my round-3 head `9624ef4c` (R421-3 POSITIVE):
  - `651839e1`: merges main `16ea10ac` (#138, lane C5b, AECP dispatch), assignment #80 comment 5939839032;
  - `95a78c09`: merges main `03c842a7` (#140, lane C5a, AECP deadlines), assignment #80 comment 5944153047.
- Public review start: PR #139 comment 5947338113.

## Verdict

**NEGATIVE**, on one MINOR finding in the Docs lens. The finding concerns the PR body only.

The merges themselves are clean:
- Both merges keep both sides. I re-did both, and a line-level check over every file either side touched loses nothing.
- The ROM relocation is correct and graded. The lane's two bodies moved to words 464 and 480 unchanged, and main's new `E_DLKILL` (words 6..7) does not overlap them.
- The five `tb/pp_top` builds are numbered the same way everywhere.
- 09 keeps main's §8.3, and the lane's section is §8.4.
- The top's ports and parameters are main's plus the lane's authorised two.
- Every assigned campaign reproduces at the head, with every per-arm count equal to its README record.
- Every round-3 probe of mine gives the same result as at round 3.

**R421-4-F1 (MINOR, Docs).** The assignment asks that the condensed PR body keep every figure. It does not. To stay under GitHub's 65,536-character limit, round 4b turned rounds 1-4's validation tables into paragraphs. Those paragraphs drop recorded figures: the per-gate parent figures of every round, links 999, the 3,793 first-party ports, docs_check 184 md + 955 files, and the probe figures 15,230 / 15,301 / 15,232. The author's packet says the paragraphs carry "the same figures".

I fixed my verdict and ledger before reading any prior-round finding text of the other reviewer (`receipts/verdict_before_prior_findings.txt`, 08:50:13Z). I read no R420-4 material. I opened my own R421-3 report only after my independent pass over both merges, to take its probe scripts.

## How the task was reconstructed

- **Repository rules.** The head has no `AGENTS.md` or `CONTRIBUTING.md`. I used `README.md` and `docs/README.md` (conventions, ID registries, figure rules, editing workflow).
- **Scope.** The #80 body and its frozen acceptance, and the design STOP and its ruling (5915752457, 5915765717). The `uns_tx_busy_i` ruling (5929618372). The round-3 ruling (5932649053). The round-4 assignment (5939839032) and the round-4b assignment (5944153047).
- **Authorities.** IEEE 1722.1-2021 §7.4.39.1 (Figure 7-61), §7.4.15.1 (Figure 7-40), §7.4.25.1, §7.5.1 and Figure 7-142. Milan v1.2 §5.4.5. The repository's 03 §6, 06 §7, 08 §4 and 09 §8.
- **History.** `git diff 03c842a7..95a78c09`, `9624ef4c..95a78c09` and both merges' parents and bases:
  - `651839e`: parents `9624ef4c` and `16ea10ac`, base `3f3ea56b`;
  - `95a78c0`: parents `651839e` and `03c842a7`, base `16ea10ac`.
- **Public evidence.** The assignment pins milan-fpga `2c532827`, but that commit holds only round 1's author packet. I read `author-r4` and `author-r4b` on branch `ppC6-review-evidence` at `7d8194b5` (its two newest commits archive them). I found no manager source-bank receipt for this head in that tree or in the issue and PR comments; see Real limits.

## What the merges change, and what I checked

### 1. Both sides kept (re-done merges)

I re-ran `git merge --no-ff 16ea10ac` on `9624ef4c` in a scratch clone. The four conflicted files are exactly the author's four: `tb/pp_top` Makefile, README, `pp_top_wrap.sv` and `sim_main.cpp`. The auto-merged files differ from `651839e` only by the relocation edits and the two `notify_mutants.py` adaptations.

`scripts/keep_both_sides.py` then checks, for every file either side touched, that every line a side added is still in the merge. Results:
- **`651839e`**: `receipts/keep_both_sides_651839e.txt`;
- **`95a78c0`**: `receipts/keep_both_sides_95a78c0.txt`. Its six conflicted files are the `tb/pp_top` four, `tb/ucpu/sim_main.cpp` and 09.

No code line of either side is lost. Every line the check flags is one of these:
- a build ordinal (three, four or five builds; "fourth" to "fifth");
- the `.PHONY`/`clean` re-wrap;
- the section-flag union in `sim_main.cpp`;
- 09 §8.3 renumbered to §8.4;
- the relocated ROM constants (2000/2016 to 464/480);
- `notify_mutants.py`'s tally pattern and `set_control_ignores_lock` anchor.

Other checks:
- `tb/ucpu/sim_main.cpp` keeps main's P19/P20 and the lane's N6/N7.
- The binary `21-integration-faces.png` is the lane's (main did not touch it).
- `hdl.yml` keeps main's `aecp-mutants` and `aecp-dispatch-mutants` steps.
- `git diff --check` is clean against both parents.

### 2. Build numbering (bench, README, 08/09, campaigns)

`receipts/build_ordinals_grep.txt` greps every build ordinal and count. All of them agree on: default, fixture (second), identify (third), line (fourth), timebase (fifth).
- `Makefile:4-14,149` requires five tallies.
- The `sim_main.cpp` header and tally comment say five.
- The wrap banner (`pp_top_wrap.sv:30-36,483,523-532`), `README.md:20,1416-1427,1705,1728-1739`, `08_timing.md:167`, `09_verification.md:258,279,284` and `aecp_mutants.py:57` all match.
- `notify_mutants.py:14` says third.

The run prints exactly the five build lines (`receipts/pp_top-make-95a78c0.log`).

### 3. 09 section numbers

`09_verification.md:217` keeps main's §8.3 (deadline and hazards), and `:276` makes the lane's notifications section §8.4. All six links to the §8.3 anchor still name the deadline section:
- `00:526`;
- `03:293` and `03:380`;
- `06:1271`;
- `08:164`;
- `09:79`.

Nothing links the lane's old §8.3 anchor. `check-links.py` reports 1,035 links OK.

### 4. ROM relocation and overlap (regenerated)

`scripts/rom_compare.py` regenerates `ucode.hex` from `gen_ucode.py` at five revisions (`receipts/rom_compare.txt`). Its sha256 figures equal the author's at main `16ea10ac`, the lane, `651839e`, main `03c842a7` and the head.

- **Against main.** The head differs from main `03c842a7` only at words 464..469 and 480..500. `651839e` differs from main `16ea10ac` at the same words.
- **The lane's bodies.** At the head they equal round 3's word for word: `E_IDNOTIF` (6 words, from 2000 to 464) and `E_SINFOUNS` (21 words, from 2016 to 480). Neither body branches, so neither depends on where it sits.
- **No collision.** Words 464..500 are unoccupied in both mains, and words 2000 and 2016 are occupied in both mains (`E_RDESCAU`/`E_RDESCCD`).
- **Main's new program.** `E_DLKILL` (words 6..7) is the only change from `651839e` to the head and does not touch the lane's words.
- **Nothing dropped.** Every word occupied in either parent is occupied in the head. `place()`'s overlap assert passes.
- **Program counts.** 82 (lane), 86, 88, 87 and 89 (head) programs. `check_upc_map.py` passes: 61 constants, 89 entry points.

**Fault probe** (`scripts/relocation_probe.sh`, `receipts/relocation_fault_probes.txt`). I put the entry points back at 2000/2016, and every grading layer fails:
- `tb/ucpu` N6/N7: 8 failures out of 437 checks;
- `check_upc_map.py`: rc 1;
- `tb/pp_top` section ID: 84 failures out of 178, ID1b byte-exact among them;
- `--notify-only`: NP3 fails (no unsolicited SET_STREAM_INFO).

### 5. The notify campaign's two adaptations

- **The tally pattern.** `notify_mutants.py:262` accepts main's build line, `[build X, SRP_DOM_DEF_VID_P 0x…, DESC_LINE_BYTES_P N]`, exactly as `sim_main.cpp` prints it.
- **`set_control_ignores_lock`.** Main rewrote `E_SCTRL` (#53) and moved the found-control lock check to `CHECK_LOCK ra=15, imm=SCTRL_EMIT`.
  - The control NOPs exactly that word. The planter refuses unless the text occurs exactly once, and the miss arm's `CHECK_LOCK` carries a different comment, so it is untouched.
  - `CHECK_LOCK` sets ENTITY_LOCKED and branches only while another controller holds the lock (`KL_aecp_ucpu.sv:350,707`). Removing it is therefore the same planted defect: SET_CONTROL ignores a foreign lock.
  - It is KILLED by RN alone: 395 of 2,251 frame comparisons diverge (`receipts/notify/chunk_B.results.json`).
  - SET_CONTROL's `NOTIFY_ENQ 4` predates the lane, and main's rewrite keeps it. NP4 grades it at the head.

### 6. Top ports and parameters

`scripts/top_ports.py` (`receipts/top_ports.txt`) compares the top's declarations:
- The head equals round 3 exactly: 27 parameters and 212 port names, with identical declarations.
- The head equals main plus exactly `EN_IDENTIFY_NOTIF_P` and `identify_button_i`.

The parent's 1,752 to 1,757 count is main's five internal C5a ports: `dl_kill_i` and `dl_queued_o` on `KL_aecp_engine`, and `preempt_i`, `preempt_upc_i` and `preempted_o` on `KL_aecp_ucpu`. No merge adds or changes a top port or parameter.

`KL_aecp_notify.sv`, the originators, `pp_pkg.sv`, `notify_phases.hpp` and `tb/aecp_notify` are byte-identical to round 3. The engine's deadline kill is gated by `!uns_r` (`KL_aecp_engine.sv:1755-1767`, main's own), so it never preempts an unsolicited job.

### 7. Executed at the head

All runs used Verilator 5.050 rev v5.050 (the CI pin; wrapper sha256 `905795b9…`, `receipts/00_tool_identity.txt`), with at most 8 jobs at once, in scratch clones or exports. The reviewed clone was only read.

| What | Result | Receipt |
|---|---|---|
| `tb/pp_top` `make`, five builds | rc 0, **9,151 / 0**: default 8,679, fixture 20, identify 178, line 218, timebase 56 | `pp_top-make-95a78c0.log` |
| `tb/pp_top` at main `03c842a7` (independent side run) | rc 0, 8,901 = 8,607 + 20 + 218 + 56. The head is main + the lane's ID0 3, NP 47, ST 18, RN 4 (default) + ID 178 (identify) = 9,151, with every main section line unchanged | `pp_top-make-main-03c842a7.log` |
| `tb/ucpu`, `tb/aecp_notify`, `tb/originator` | 437/0, 14/0, 107/0 | `suite-*-95a78c0.log` |
| `scripts/lint_hdl.sh` | rc 0 | `lint_hdl-95a78c0.log` |
| `make check`; `gen_matrix.py --check`; parameter, matrix and M9 gates | rc 0: links 1,035, parameters 27 = 27 = 27, 94 rows with 0 untested, 115 REQ rows, M9 30 opcodes | `make_check-…`, `gen_matrix_check-…`, `docs_gates_extra-…` |
| `git apply --check`, every tracked patch | **205 of 205 apply**: C5a 42, dispatch 35, adp 28, maap 27, srp_top 73 | `git_apply_check.txt` |
| notify campaign (`notify_mutants.py`, three `--only` chunks, 5 goldens) | **40 of 40 KILLED**; all 40 per-arm counts equal the README | `notify/`, `readme_counts.txt` |
| C5a AECP campaign (`aecp_mutants.py`, six chunks) | **55 of 55 KILLED**; the 5 distinct controls pass in every chunk | `aecp/` |
| dispatch campaign (`aecp_dispatch_mutants.py`, five chunks) | **35 of 35 KILLED**; controls pass; all 35 counts equal the README | `dispatch/`, `readme_counts.txt` |
| ACMP campaign (`acmp_mutants.py --jobs 8`) | **19 of 19 KILLED**, 3 goldens pass; the 14 pp_top counts equal the README | `acmp/` |
| D3 campaign (`d3_mutants.py`'s own `judge()`, goldens once, then six slices; `scripts/d3_chunk.py`) | **83 of 83 KILLED**, 3 goldens pass; all 71 pp_top counts equal the README (the other 12 are recorded in `tb/acmp_nvm` and `tb/rx_validator`) | `d3/`, `readme_counts.txt` |
| My round-2 arms (`r421_arms.py`) | 188/0. R421a gaps 15,232 / 15,300; R421b 55,267 / 15,299; R421c and R421d 6 frames, 15,301. Equal to round 3 | `probes/r421_2_arms_at_head.log` |
| My seeded random-press probe, 16 campaigns | all rc 0. **Every summary line equals round 3's**: 3,200 press edges, 3,217 bursts, 974 MAC stalls, smallest gap 15,230 | `probes/random/`, `probes/random_probe_vs_r3.txt` |
| My latch mutants (`r421_3_probes.py`) | the same nine records as round 3 (as a set): 7 KILLED by section ID; `c_press_not_latched` survives the probe only; `p_wait_latch_always` equivalent | `probes/latch/`, `probes/latch_probes_vs_r3.txt` |
| FT departure-phase sweep | identical to round 3 at all nine phases; both lower bounds hold | `probes/ft_phase_sweep_head.txt` |
| Hosted checks at the head (read-only, 08:49Z) | `docs-gates` and `portability` success (both events). `suites` **in_progress**: not executed to a conclusion | `hosted_checks_95a78c0.txt` |

## Findings

### R421-4-F1 [MINOR] (Docs): the condensed PR body drops recorded earlier-round figures

- **Where:** the PR #139 body at review time (`receipts/pr_body_live_at_review.md`, equal to the author's `author-r4b/PR-BODY.md`). The condensed paragraphs are:
  - round 1 validation, `:104-118`;
  - round 2, `:236-251`;
  - round 3, `:323-333`;
  - round 4, `:378-390`.

  The claim is in the author's packet, `author-r4b/HANDOFF.md:224-228`: "the older rounds' validation tables became paragraphs carrying the same figures".
- **Authority:** this review's assignment ("the condensed PR body keeps every figure"). The round-4 body (`author-r4/PR-BODY.md`, archived; copy in `receipts/pr_body_round4_author_packet.md`) is the record it condenses.
- **Evidence:** `scripts/pr_body_figures.py` (`receipts/pr_body_figures_per_round.txt`) compares each round's section. Measured figures in round 4's body that no longer appear anywhere in the same round's section of the live body:
  - **Round 1:** lint 41 modules; `check_rtl_source_lists` 36/42 tops; port contracts "52 literal-bound and 62 without local rationale"; `nvm_cosim quick` 315 of 315; `milan_dp_render` 65 + 152 checks.
  - **Rounds 2 and 3:** links 999; lint 41 modules; srp_top assertion coverage 65/65; gen_matrix 94 rows; naming 96 candidates; 107 files and 36/42 tops; port contracts 52/62 (round 2); `lint_rtl` 90 <= 90; `pp_shadow` 311; `nvm_cosim` 315; `milan_dp_render` 65 + 152; yosys 36 tops (round 3).
  - **Round 4:** 3,793 first-party ports; docs_check "184 md + 955 scrubbed files"; srp_top 11 controls; yosys 36 tops; lint 41; and the same parent gate figures. Also the probe figures: R421-3's smallest random-probe gap 15,230, and R420-3's round-2 driver RP1 15,301 and smallest gap 15,232.

  Each dropped figure is from a table row that the paragraphs summarise as "all rc 0" or "all 16 rc 0". Round 4b's own section is complete, and I re-measured its figures above.
- **Impact:** the PR body is the merge record. Measured per-gate figures of four rounds no longer appear in it, and the author's packet says they do. No figure is misstated, and no code, test, generated artifact or conformance claim is affected.
- **Why MINOR, not RESIDUE:** the defect removes recorded figures from the PR body, so it is not purely wording. Under the owner rule an uncertain case is MINOR.
- **Required outcome (one of):**
  - (a) restore the dropped figures compactly in the condensed paragraphs (the list is in the receipt; the body has about 1,220 characters of headroom); or
  - (b) if the 65,536-character limit forbids (a), make each condensed round's validation paragraph name where its full tables are kept verbatim (the archived `review-evidence/ppC6-r1/author-rN/PR-BODY.md` at a named evidence commit), and correct the "carrying the same figures" sentence in the round's handoff.

  The manager rules whether (b) satisfies "keeps every figure".
- **Verification:**
  - for (a), `scripts/pr_body_figures.py receipts/pr_body_round4_author_packet.md <new body>` lists no measured figure as missing (round numbers and comment IDs aside);
  - for (b), each of the four paragraphs carries the pointer and the pointed files hold the tables.

No other finding. Two candidates were checked and dropped:
- The `sim_main.cpp` `main()` comment names only the fixture and line builds as leaving the harness model unclocked. That text is main's and identical on both sides, so no merge changed it.
- The notify campaign has no CI step. It had none at round 3 either, and it is outside this delta.

## Prior public review findings at this head

All were read after my verdict and ledger were fixed. The lane's RTL (`KL_aecp_notify.sv`), its bench phases (`notify_phases.hpp`) and `tb/aecp_notify` are byte-identical to `9624ef4c`. Every resolution therefore carries over, and the re-runs above confirm it.

| Finding | State at 95a78c09 | Evidence |
|---|---|---|
| R420-1 F1 / R421-1 F1 (MINOR: frames bunch under a stall) | **Resolved** (unchanged) | random probe smallest gap 15,230 with 974 stalls; R421a/b 15,232 / 15,299; `ident_burst_from_t0` KILLED |
| R420-1 F2 (MINOR: the CDC rule) | **Resolved** (unchanged) | `docs/guides/hdl-engineer.md:64`; `ASYNC_REG` at `KL_aecp_notify.sv:718-719` |
| R420-2 F1 / R421-2 F1 (MINOR: a press in the post-burst gap is lost) | **Resolved** (unchanged) | ID8 in 178/0; R421c and R421d 15,301; all 16 random campaigns lose no press; `ident_press_not_latched`, `ident_wait_ignores_gap` and `ident_burst_press_not_latched` KILLED |
| R420-1 S1, R420-1 S4 | **Retained, recorded** | `tb/pp_top/README.md:1975` and `:1891`, kept through both merges |
| R420-1 S2/S3; R421-1 S1-S4; R420-2 S1/S2; R421-2 S1/S2 | **Taken** at rounds 2 and 3 (unchanged) | FT 14/0 and the FT sweep; ID9 (`ident_departure_ignores_ready` KILLED); the five-build comments |
| R420-3 S1 (the latch's boundary cycle has no discriminating check) | **Not taken; retained** in this merge-only round. The PR body records why ("What remains, round 4b") | SUGGESTION; the RTL it concerns is unchanged |
| R421-3 S1 (FT4 at phase 99,999) | **Not taken; retained**, as above | SUGGESTION; my sweep still holds at 99,999 (t14 = 100,000,003) |

## Lens results (artifact-specific)

- **Conformance: CLEAN.**
  - IEEE 1722.1-2021 §7.4.39.1 (Figure 7-61): the IDENTIFY_NOTIFICATION body is graded byte-exact at word 464 (ucpu N6, pp_top ID1b).
  - §7.4.15.1 (Figure 7-40): the 84-byte unsolicited SET_STREAM_INFO body is graded at word 480 (N7, NP3).
  - §7.5.1 and Figure 7-142: on the wire, the smallest gap is 15,230 clocks over 16 seeded campaigns. FT holds both floors at the full timebase.
  - §7.4.25.1: main's value-in-force rewrite of SET_CONTROL keeps the lane's push (NP4) and lock (RN) behaviour.
  - Milan §5.4.5: NP, ST and RN pass in the default build.
- **RTL: CLEAN.**
  - The merges change in `hdl/` only main's own code and the two `UPC_*_C` constants.
  - The ROM is regenerated and overlap-free; main's `E_DLKILL` is disjoint from the lane's words.
  - The top's ports and parameters are main's plus the authorised two.
  - Lint is clean.
- **Robustness: CLEAN.**
  - The 16 random-press campaigns (8 with MAC stalls) and the eof-beat stall arms are identical to round 3.
  - The deadline kill never reaches an unsolicited job (`!uns_r`).
  - Main's TB3 and HZ pass beside the lane's sections in the same default build.
- **Tests: CLEAN.**
  - Five builds give 9,151/0, and the arithmetic against an independent main run loses no check.
  - Campaigns: notify 40/40, AECP 55/55, dispatch 35/35, ACMP 19/19, D3 83/83. Every recorded per-arm count is equal.
  - 205 of 205 patches apply.
  - The relocation is graded at three layers (fault probe).
- **Docs: UNCLEAN (R421-4-F1).**
  - These artifacts are correct: 09 §8.3/§8.4 and their anchors, the build ordinals everywhere, `make check`, the matrix gate, and round 4b's own PR-body section.
  - The condensed earlier-round paragraphs of the PR body drop recorded figures.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `gen_ucode.py` `E_IDNOTIF`/`E_SINFOUNS`/`E_SCTRL`/`E_DLKILL` at five revisions; ucpu N6/N7; pp_top ID, NP, ST and RN output; random probe; FT sweep; against IEEE 1722.1-2021 §7.4.39.1, §7.4.15.1, §7.4.25.1, §7.5.1, Figure 7-142 and Milan §5.4.5 | R421-4 | 95a78c099ee5aa914521975355adc1dfef99d01c |
| RTL | CLEAN | `git diff 9624ef4c..95a78c0 -- hdl` (engine UPC constants, main's C5a/C5b code); `KL_aecp_engine.sv:914,916,1755-1767`; top declarations at four revisions; ROM occupancy; lint | R421-4 | 95a78c099ee5aa914521975355adc1dfef99d01c |
| Robustness | CLEAN | 16 seeded random-press campaigns (8 with stalls); R421a-d eof-stall and gap-press arms; FT phase sweep; deadline-kill gating of unsolicited jobs | R421-4 | 95a78c099ee5aa914521975355adc1dfef99d01c |
| Tests | CLEAN | `tb/pp_top` Makefile, `sim_main.cpp`, `pp_top_wrap.sv`, README records; `notify_mutants.py` adaptations; five campaigns (232 arms); 205 patches; main-side pp_top run; relocation fault probe; latch mutants | R421-4 | 95a78c099ee5aa914521975355adc1dfef99d01c |
| Docs | UNCLEAN (R421-4-F1) | `09_verification.md` §8.3/§8.4 and its six inbound anchors; `08_timing.md:167`; `tb/pp_top/README.md` build tables and records; `make check`; `gen_matrix.py --check`; PR body rounds 1-4b against the round-4 body; `author-r4b/HANDOFF.md:224-228` | R421-4 | 95a78c099ee5aa914521975355adc1dfef99d01c |

## Real limits

- **Simulation only.** Physical calibration was NOT RUN and no hardware was used; field skips are not hardware proof. The identify sequencer exists only at `EN_IDENTIFY_NOTIF_P` = 1, which the parent does not use.
- **Not run here.** The full `run_suites.sh` sweep (805 s on the author's host, above my ten-minute foreground cap). I ran its gates and the suites the merges touch: `tb/pp_top`, `tb/ucpu`, `tb/aecp_notify`, `tb/originator` and lint. Also not run:
  - the adp, maap, srp_top, gsi, retry, srp_admission and name_wr campaigns and the nvm_port figures (their sources are not touched by either merge's lane side; their patches all apply);
  - yosys;
  - the parent consumer set and the donor bank;
  - Docker/act and the hosted jobs.
- **How the D3 campaign ran.** It ran through its own `judge()` in six slices with the goldens once (`scripts/d3_chunk.py`), not as one driver invocation. Planting, building and grading are the driver's own.
- **Evidence pointer and manager banks.** The assignment's evidence commit (`2c532827`) holds only round 1's author packet. I read rounds 4 and 4b at `7d8194b5` on `ppC6-review-evidence`. The assignment says the manager's source static/builder and native banks passed at this head. I found no public receipt for that at this head, so I could not verify it.
- **Harness incidents, all corrected:**
  - One AECP chunk launch passed a malformed arm list and refused to run. The six real chunks ran, and I waited for them in the foreground.
  - The first random-probe run executed outside `tb/pp_top`, did not find `ucode.hex`, and failed for that reason. I re-ran it from the bench directory, and only that run is published.
  - Importing the drivers wrote an ignored `tb/pp_top/__pycache__/` into the reviewed clone. I removed it, and the clone was re-verified.
- **Clone integrity** (`receipts/clone_verification.txt`). HEAD and tree are exact, and the status (including ignored files) is empty. The index equals HEAD in modes and blobs, and the work-tree blobs equal the index. There is no `.gitmodules` and no gitlink, so no submodule gitlink applies.
- **Receipt paths.** Host paths are replaced by `<PINNED_VERILATOR_PREFIX>`, `<PINNED_VERILATOR>`, `<PACKET>`, `<CLONE>` and `<HOME>`.

## Pending manager duties

- R421-4-F1: a ruling on outcome (a) or (b), and the PR-body edit.
- Hosted acceptance at the head: `suites` was in progress at 08:49Z. Hosted and act acceptance belong to the manager.
- The donor bank, and the parent consumer set at milan-fpga dev `cdf49d1a` with the combined C4 + C6 patch (`parent-adoption-c4c6-ea3fb388.patch`).
- The merge-turn final current-dev candidate (source base `03c842a7`, live dev `cdf49d1a`), which is separate from this source validation.
- A second independent positive review before merge.

## Receipts

`MANIFEST.sha256` lists every published file besides this report.

Scripts:
- `keep_both_sides.py`, `rom_compare.py`, `top_ports.py`: merge, ROM and port checks;
- `run_campaigns.sh`, `d3_chunk.py`: campaigns;
- `readme_counts.py`: per-arm counts against the README;
- `pr_body_figures.py`: F1;
- `relocation_probe.sh`: the fault probe;
- `run_r421_4_probes.sh`: re-runs my round-3 probes, using `r421_arms.py`, `r421_3_random.py`, `run_random.sh`, `r421_3_probes.py`, `r421_3_ft_sweep.sh` and `verilator-j8.sh`.

R421-4 FINISHED
