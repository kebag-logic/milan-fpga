[R420] NEGATIVE - exact head 95a78c099ee5aa914521975355adc1dfef99d01c

# R420-4: delta review of PR #139 (lane C6) at `95a78c09`

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #80 / PR #139, round R420-4.
- Exact head: `95a78c099ee5aa914521975355adc1dfef99d01c`, tree `d0be0f91665f4e6b8e16bfa3aa8f53bbeaff518f`.
- Scope: only the two merge commits on round 3's `9624ef4c`, where R420-3 was POSITIVE:
  - `651839e1`, which merges main `16ea10ac` (#138, C5b), round 4;
  - `95a78c09`, which merges main `03c842a7` (#140, C5a), round 4b.

## Verdict

**NEGATIVE: one MINOR finding is open (R420-4-F1, Docs).**

The merges themselves are sound:
- Every conflict keeps both sides, and nothing of #138 or #140 is lost.
- The ROM relocation is byte-exact, and nothing overlaps.
- No top port or parameter changed.
- All five builds are numbered consistently.
- 09 keeps main's §8.3, and the lane's section is §8.4.
- Every campaign reproduces at the head, with every failing-check count equal to its README record.
- My round-3 probes reproduce byte for byte.

The one open defect is in the PR body. Round 4b condensed rounds 1 to 4 and dropped figures from them. The manager's check asks that the condensed body keep every figure, so this cannot be RESIDUE: it removes figures rather than rewording them.

One new SUGGESTION (S1) and the still-open R420-3-S1 do not gate the verdict.

## 1. How the task was reconstructed

1. **Contributor rules.** The repository has no AGENTS.md or CONTRIBUTING.md. `docs/README.md` holds the authors' conventions: single-source rules, ID registries and `make check`.
2. **Scope.** Issue #80's frozen acceptance (items 1-4) and the manager's comments: the lane assignment 5915639621, the STOP ruling 5915765717, the round 2/3 assignments, round 4 (5939839032) and round 4b (5944153047). Both rounds are "merge only; STOP on any port, parameter or parent-visible change".
3. **The diff.** `git diff 03c842a7..95a78c09` and its history. Each merge was re-done with `git merge-tree --write-tree`, and its conflict set and resolution compared against both parents (section 2).
4. **Public evidence.**
   - The pinned evidence commit in the assignment (`kebag-logic/milan-fpga@2c532827`, `review-evidence/ppC6-r1`) holds only the round-1 packet. The `author-r4` and `author-r4b` packets are at `ppC6-review-evidence` `7d8194b5` (commits `72483b72`, `7d8194b5`), and I read them there.
   - The live PR body is byte-identical to `author-r4b/PR-BODY.md`, apart from one trailing blank line.
   - My own R420-2 and R420-3 packets were read for their probes after my own pass over the diff.
   - No other reviewer's report was read before this verdict and ledger were written (section 9).

## 2. The merges keep both sides

Both trial merges reproduce exactly the conflict sets the author named:
- round 4: `tb/pp_top/{Makefile,README.md,pp_top_wrap.sv,sim_main.cpp}`;
- round 4b: the same four files plus `tb/ucpu/sim_main.cpp` and `docs/architecture/09_verification.md`.

The diff from each auto-merge tree (with conflict markers) to the committed tree is the whole resolution:
- round 4: 8 files;
- round 4b: 8 files.

I read both diffs in full.

`both_sides.py` is a multiset check over every file both sides changed: 14 files in round 4 and 15 in round 4b. It lists every line a side added that the merge lacks, and every line a side removed that the merge still carries.
- **Round 4, 55 entries** (`receipts/both_sides-651839e1.txt`). Each is one of:
  - a build-count word (three -> four);
  - a line merged with the other side's (`one_section`, `.PHONY`, `clean`, the tally `awk` and the wrap banner);
  - the ROM relocation (2000/2016 -> 464/480 in `gen_ucode.py`, `KL_aecp_engine.sv:914,916` and `tb/ucpu/sim_main.cpp:53-54`).
  - In README section AX, main's only lost line is "The third build" -> "The fourth build".
- **Round 4b, 46 entries** (`receipts/both_sides-95a78c09.txt`). Each is one of:
  - a build-count word (four -> five; "the fourth build" -> "the fifth" for TB in the bench, wrap, README, 08 §4, 09 §8.3 and `aecp_mutants.py:57`);
  - a merged line;
  - the 09 heading renumber, 8.3 -> 8.4.
  - Nothing of C5a's DL, HZ and TB sections, its `aecp_mutants.py` or its 42 patches is lost.
  - `tb/ucpu` keeps main's P19/P20 and calls the lane's `the_identify_and_stream_info_notification_bodies()` after them (declaration and call).

Patch-id equality (`receipts/patch-ids.txt`):
- `hdl/`, `syn/`, `.github/` and `.gitattributes` from round 4 to the head equal main's own `16ea10ac..03c842a7` change.
- `hdl/` from main to the head equals the lane's `16ea10ac..651839e1` change. So round 4b adds no RTL edit of its own.
- In round 4, `scripts/`, `.github/` and `.gitattributes` equal main's change. Its `hdl/` differs from main's change only by the two relocated constants and the `gen_ucode.py` comment.

## 3. Builds, numbering and 09 sections

`tb/pp_top` builds five times: default, fixture, identify (third), line (fourth) and timebase (fifth). The numbering is consistent in every place:
- `Makefile:4-14,88,149,152-154`, with the tally requiring `NR != 5`;
- `sim_main.cpp:20-26,13577,13586,13626-13629`;
- `pp_top_wrap.sv:29-38,483,523-532`;
- `README.md:20-22,706,729,1416-1427,1705,1728-1736`;
- `08_timing.md:167`;
- `09_verification.md:258,279,284`;
- `aecp_mutants.py:57`;
- `notify_mutants.py:14`.

A repository-wide search finds no stale build count. `clean` and `.PHONY` carry every target of both sides.

09 keeps main's `### 8.3` (`:217`). Its six links resolve: 03 twice, 06, 08, 09 itself and 00. The lane's section is `### 8.4` (`:276`), and nothing links it. `make links`: 1,035 checked, OK.

## 4. ROM relocation and overlap (regenerated)

`gen_ucode.py` was regenerated at five revisions (`receipts/rom-compare.txt`):
- every image is 2048 words;
- the hashes equal the author's `ucode-merge-compare.txt`: head `518b900c…`, main `3559d0a6…`, round 4 `23d2213d…`.

The head equals main except at words 464..469 and 480..500. It equals round 4 except at words 6..7.
- head[464..469] equals round 3's [2000..2005]: `E_IDNOTIF`, 6 words.
- head[480..500] equals round 3's [2016..2036]: `E_SINFOUNS`, 21 words.

The occupancy map (`rom_occupancy.py`, `receipts/rom-occupancy-*.txt`) shows:
- `E_DLKILL` at 6..7, then `E_FAILSAFE` at 8;
- 448..455 `E_COPYT`, 464..469 `E_IDNOTIF`, 480..500 `E_SINFOUNS`, 512.. `E_FMT`;
- `E_RDESCAU` at 2000 and `E_RDESCCD` at 2024.

Nothing of C5a's microcode sits at 464..511. `check_upc_map.py` passes with 61 engine constants and 89 entry points, and `check_m9_opcodes.py` with 30 opcodes.

**Probe** (`probes/stale_upc_probe.sh`): a stale `UPC_IDNOTIF_C = 2000` or `UPC_SINFOUNS_C = 2016` left in a private copy, as if the relocation had been missed.
- `check_upc_map.py` refuses both.
- The idnotif plant fails ID1b and ID2b (the IDENTIFY_NOTIFICATION frames).
- The sinfouns plant fails NP3 and NP4, which find no unsolicited SET_STREAM_INFO response.

So the relocation is graded, not just carried (`receipts/stale_upc_probe.log`).

## 5. No top port or parameter change

The `protocol_processor_top` header at the head equals round 3's port and parameter list line for line: 212 ports, 27 parameters. Against main `03c842a7` it differs only by the lane's authorized `EN_IDENTIFY_NOTIF_P` and `identify_button_i`.

`git diff 651839e1 95a78c09 -- hdl` adds exactly main's five internal ports:
- `KL_aecp_engine`: `dl_kill_i`, `dl_queued_o`;
- `KL_aecp_ucpu`: `preempt_i`, `preempt_upc_i`, `preempted_o`;
- plus the `ix` argument of C5a's `hz_key` function.

These are the same lines as `git diff 16ea10ac 03c842a7 -- hdl`, which accounts for the parent's 1,752 -> 1,757.

## 6. Re-measured at the head (Verilator 5.050, at most 8 parallel jobs)

### Suites and gates

| Command (on a `git archive` export of the head) | rc | Result |
|---|---:|---|
| `make -C tb/pp_top` (five builds) | 0 | 9,151 = default 8,679 + fixture 20 + identify 178 + line 218 + timebase 56 |
| same at main `03c842a7` / round 4 `651839e1` | 0 / 0 | 8,901 (8,607/20/218/56) / 8,855 (8,439/20/178/218) |
| every section line of main's and of round 4's run present at the head | - | 0 missing, 0 new (`receipts/sections-*.txt`) |
| `make -C tb/ucpu` | 0 | 437 = 398 + 29 (P19/P20) + 10 (N6/N7) |
| `make -C tb/aecp_notify`, `tb/originator` | 0, 0 | 14; 107 |
| `scripts/lint_hdl.sh` | 0 | 41 LINT OK |
| `EN_IDENTIFY_NOTIF_P=1` lint of `protocol_processor_top`, `KL_aecp_engine`, `KL_aecp_notify` | 0 | 0 findings each |
| `make links matrix modmatrix params stale lint wavedrom-check`, `gen_matrix.py --check` | 0 | 1,035 links; 115 REQ / 17 GAP; 94 rows, 0 untested; 27 = 27 = 27; 41 mermaid + 18 wavedrom |
| `git diff --check`: `9624ef4c..651839e1`, `16ea10ac..651839e1`, `651839e1..95a78c09`, `03c842a7..95a78c09`, `3f3ea56b..95a78c09` | 0 | |
| `git apply --check` of every tracked patch | 0 fail | adp 28, maap 27, aecp-dispatch 35, C5a 42, srp_top 73 (205) |

The default build is main's 8,607 plus the lane's 72 (ID0 3 + NP 47 + ST 18 + RN 4). It is also round 4's 8,439 plus C5a's 240 (DL 64 + HZ 176).

### Campaigns

| Campaign | Result | Failing-check counts against the README record |
|---|---|---|
| `notify_mutants.py` | goldens pass; **40/40 KILLED** | 40 of 40 equal (`receipts/notify-campaign-counts.txt`) |
| `aecp_mutants.py` (C5a) | 5 controls pass; **55/55 KILLED** | 55 of 55 equal; the 17 multi-arm rows checked by hand |
| `aecp_dispatch_mutants.py` (C5b) | 3 controls pass; **35/35 KILLED** | 35 of 35 equal |
| `acmp_mutants.py` | 3 goldens pass; **19/19 KILLED** | pp_top 14 of 14 and listener 4 of 4 equal |
| `d3_mutants.py` | goldens pass in every chunk; **83/83 KILLED** | 83 of 83 equal, `validator_admits_held_aecp` (rx_validator M4, 4) by hand |

Each campaign was run in chunks with `--only`; there are no partial verdicts. The README totals agree:
- `README.md:1926` 40 of 40;
- `:956` 5 controls and 55 arms;
- the record at `:1008` lists 35 rows;
- `:1598` all 19;
- `:865` all 83.

### Both adaptations of the notify campaign keep their planted defect

- **The tally pattern** (`notify_mutants.py:262-265`) accepts main's `DESC_LINE_BYTES_P` build line. All 40 runs completed with a tally: none was refused or incomplete.
- **`set_control_ignores_lock`** (`:236-239`) NOPs the found-control lock check `u('CHECK_LOCK', ra=15, imm=SCTRL_EMIT)` at `gen_ucode.py:1852`, the line followed by its comment "held by another controller?". This is the same word main's own `aecp_dispatch_mutations/lk-sctrl-lock-nop.patch` NOPs.
  - The miss path's lock check at `:1870` stays.
  - Section RN still kills it ("RN: 720 seeded steps").

### My round-3 probes, re-run unchanged at the head

| Probe | Result at round 3 | Result at the head |
|---|---|---|
| `run_probes.sh` (RP3a-RP3j) | 600 checks, 0 failures | identical, line for line, except the build line (`receipts/r420_3_probes_head95a78c0.log`) |
| `boundary_control.sh` (R420-3-S1 control) | section ID 178/0; probes 597/1 (RP3j k = -2) | identical except the build line |
| `r420_2_probes_unchanged.py` | 4 records | identical, all four (RP1 15,301; RS1/RS2; `hold_ignores_gap` 4 FAIL; `burst_deadline_one_tick_short` passes ID) |

### New robustness probe (`probes/en1_c5a_probe.sh`)

C5a's sections had run only at the default `EN_IDENTIFY_NOTIF_P` = 0. With the sequencer built (1) and the button idle, in a private copy:
- ID 178/0, DL 64/0 and HZ 176/0 in the identify build;
- TB 56/0 in a build that sets both `PP_TOP_EN_IDENT` and `PP_TOP_TIM_REAL`.

This agrees with the RTL: `KL_aecp_engine.sv:1755-1767` gates `dl_kill_r` and `dl_queued_o` by `!uns_r`.

### Hosted CI at the exact head (read-only)

Six check runs, all `success`: `suites`, `docs-gates` and `portability`, each twice. Steps 5-12 of `suites` executed: lint and every suite, the SRP, MAAP, ADP, AECP-deadline and AECP-dispatch campaigns, the traceability matrix and the nvm_port figures. "Build Verilator" was skipped on a cache hit (the pinned build was restored), which is not a skipped context. The manager owns hosted acceptance.

### Clone integrity after every probe

`receipts/clone_integrity.txt`:
- HEAD and tree exact;
- worktree == index == HEAD;
- 0 porcelain entries, ignored files included;
- 470 index entries, with modes and blobs equal to the HEAD tree;
- re-hashing every tracked file gives 0 mismatches;
- executable bits as recorded.

The repository has no submodule gitlink and no `.gitmodules`. Every build and probe ran on exports under `scratch/`.

## 7. Findings

### R420-4-F1 MINOR: the condensed PR body drops figures from rounds 1 to 4

- **Lenses:** Docs.
- **Where:** the live PR #139 body, which equals `author-r4b/PR-BODY.md` at `ppC6-review-evidence` `7d8194b5`. Affected sections: "Validation" (round 1), "Validation, round 2", "Validation, round 3" and "Validation, round 4".
- **Authority:** round 4b assignment (#80 5944153047), "add a Round 4b section to PR-BODY.md"; the review brief's check "the condensed PR body keeps every figure".
- **Evidence:** `figures_dropped.py` compares each round's section of the last full bodies (`author-r3/PR-BODY.md` for rounds 1-3, `author-r4/PR-BODY.md` for round 4) with the same section of the live body. Figures present before and now absent from that section (`receipts/prbody-figures-dropped.txt`):
  - **Round 1:**
    - lint 41 modules;
    - yosys 36 tops;
    - parent gate 3: 107 files, 4 of 4 consumer lists, 36/42 tops, 6 recorded;
    - gate 5: 52 literal-bound and 62 without local rationale;
    - gate 14: nvm_cosim 315 of 315;
    - gate 16: 65 + 152 checks, 5 leg-defect arms.
  - **Rounds 2 and 3:**
    - `make check`: 41 mermaid + 18 wavedrom, links (999), parameters 27 = 27 = 27;
    - 94 rows, 36 tops, lint 41 modules;
    - srp_top assertion coverage 65/65;
    - every per-gate parent figure except the ratchet 73 <= 77 and (round 3) 1,752/111: 107 files, 36/42, 96 candidates, 10 <= 10 / 0 <= 0 / 3 <= 3, 90 <= 90, `pp_shadow` 311, 315 of 315, 65 + 152 and 5 leg-defect arms;
    - round 2's ratchet sub-figures (multi-declarator, long function, over-long line).
  - **Round 4:**
    - `originator` 107, lint 41 modules, 94 rows, 36 tops;
    - srp_top 11 controls, adp 2 controls;
    - M9 selftest 9/9;
    - RS1/RS2 15,232 and R421 15,230;
    - parent gate 5: 3,793 first-party ports; gate 8: 184 md + 955 scrubbed files; gate 9: 0 in `hdl/`, 4 in the pinned processors;
    - ratchets: 7 <= 7, build without warnings;
    - `pp_shadow` 311, 315 of 315, 65 + 152.
  - Some appear again in the round-4b section as that round's own measurements, but no longer as the earlier rounds' records.
  - The dropped figures survive only in the archived `author-r3` and `author-r4` PR-BODY.md files, which the live body does not link.
- **Impact:** the PR body is the merge record of this PR. Its earlier rounds' validation now reads as a summary whose numbers can no longer be checked there. No measurement is wrong, and no code, test or conformance claim changes.
- **Required outcome:** restore the dropped figures to the PR body, for example by putting back rounds 1-4's command and parent-gate tables verbatim (a collapsed block is fine). If the manager rules otherwise, link each condensed section to the archived full body at a pinned evidence commit, and record that ruling.
- **Verification:** `python3 figures_dropped.py OLD NEW` against the new body reports only table row indices (the bare 5, 8, 9, 11, 12, 13 and 15 of the `#` column), or the ruling is recorded on the PR.

### R420-4-S1 SUGGESTION: the harness comment in `main()` names two of the four single-section builds

- **Lenses:** Docs.
- **Where:** `tb/pp_top/sim_main.cpp:13566-13568`: "Sections DV and AX run on models of their own in two builds each … in the fixture and line builds this model is never clocked."
- **Evidence:** the identify build (`run_identify`, an `IdentifyPhase` with its own model, `notify_phases.hpp:1579-1587`) and the timebase build (`BudgetPhase`, `sim_main.cpp:12389`) never clock it either. Each parent already had half of the gap: round 3 named only DV, and main names DV and AX but not TB. The merge took main's text.
- **Proposal:** "Sections DV, ID, AX and TB run on models of their own, so in the fixture, identify, line and timebase builds this model is never clocked."

### Prior R420 findings at this head

| Finding | Status at `95a78c09` | Evidence |
|---|---|---|
| R420-1-F1 MINOR (frames bunch under stall) | still resolved | round-2 driver records identical (RS1/RS2 min 15,233/15,232) |
| R420-1-F2 MINOR (CDC rule) | still resolved | the two merges change no line of the HDL contract (`docs/guides/hdl-engineer.md` is not in either resolution, and the both-sides check finds nothing lost) |
| R420-2-F1 MINOR (press in the post-burst gap) | still resolved | RP3a-RP3j 600/0 identical; `ident_press_not_latched`, `ident_wait_ignores_gap` and `ident_next_burst_at_once` KILLED |
| R420-1-S1, R420-1-S4 | retained, recorded | `tb/pp_top/README.md:1975` and `:1891` |
| R420-2-S1, R420-2-S2 | taken (round 3), still in place | FT2 kills `ident_burst_deadline_one_tick_short`; `sim_main.cpp:20` now says five |
| R420-3-S1 SUGGESTION (latch boundary cycle) | **open, retained** (merge-only rounds; the PR body records it) | boundary control still passes ID 178/0 and RP3j k = -2 still kills it |

## 8. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | both relocated bodies (IEEE 1722.1-2021 §7.4.39.1 Fig 7-61, §7.4.15.1 Fig 7-40) byte-exact at 464/480 (ROM compare; ID1/NP3 and tb/ucpu N6/N7 pass; the stale-UPC probe fails them); `set_control_ignores_lock` against main's `lk-sctrl-lock-nop.patch`; C5a's IDENTIFY classification next to the lane's BAD_ARGUMENTS command form; 08 §4 fan-out finding against 09 §8.4's ST row | R420-4 | `95a78c09` |
| RTL | CLEAN | `KL_aecp_engine.sv:914,916`, `gen_ucode.py:230-237`; patch-id identity of both merges' `hdl/`; top header against round 3 (212 ports, 27 params); 5 new internal ports = main's; `dl_kill_r`/`dl_queued_o` `!uns_r` gating `:1755-1767`; lint 41/41 and three modules at EN = 1 | R420-4 | `95a78c09` |
| Robustness | CLEAN | ROM occupancy (no overlap; `E_DLKILL` 6..7); `place()` overlap assert; stale-UPC probe (gate and suites refuse it); C5a DL/HZ/TB with the sequencer built (EN = 1 probe); round-3 boundary and stall/fan-out probes identical | R420-4 | `95a78c09` |
| Tests | CLEAN | five builds 9,151/0 and section lines against both parents; ucpu 437, aecp_notify 14, originator 107; notify 40, AECP 55, dispatch 35, ACMP 19, D3 83 all KILLED with every count equal to its record; 205 patches `git apply --check`; tally pattern and the re-anchored arm; R420-3-S1 (SUGGESTION) still open | R420-4 | `95a78c09` |
| Docs | **UNCLEAN** (R420-4-F1) | `tb/pp_top/README.md`, Makefile, wrap and bench comments; 08 §4, 09 §8.3/§8.4 and their links; `make` docs gates; the PR body against `author-r3`/`author-r4` bodies (F1); `sim_main.cpp:13566` (S1) | R420-4 | `95a78c09` |

## 9. Prior public review findings from the other reviewer

I read these only after sections 1-8 (verdict and ledger) were written. I used only their findings and statuses, from `reviews/R421-1..3/REPORT.md` at `7d8194b5`.

Against round 3 (`git diff 9624ef4c 95a78c09`), the two merges leave these byte-identical:
- `hdl/aecp/KL_aecp_notify.sv`;
- `hdl/packet_engine/KL_pp_originator.sv`;
- `tb/pp_top/notify_phases.hpp`;
- `tb/aecp_notify/` and `tb/originator/`;
- `docs/guides/hdl-engineer.md`.

Main's own integrator-guide edits (the response reservation, the AECP deadline paragraph) do not touch the lane's §6.

| Finding | Status at `95a78c09` | Evidence (this review) |
|---|---|---|
| R421-1-F1 MINOR (frame 3 scheduled from t0) | still resolved | `ident_burst_from_t0` KILLED; section ID 178/0; my RS1/RS2 stall and fan-out sweeps identical (min 15,233/15,232) |
| R421-1-S1 to S4 | still resolved | taken at round 2; no file they touched is changed by either merge |
| R421-2-F1 MINOR (short press in the post-burst gap lost) | still resolved | ID8 passes in section ID 178/0; `ident_press_not_latched` and `ident_burst_press_not_latched` KILLED; RP3a-RP3j 600/0 |
| R421-2-S1 (departure `ready` term) | still resolved | `ident_departure_ignores_ready` KILLED (ID9d, ID9h) |
| R421-2-S2 (one-tick floors) | still resolved | `tb/aecp_notify` 14/0; `ident_burst_deadline_one_tick_short` (FT2) and `ident_t0_same_ms` (FT4) KILLED |
| R421-3-S1 SUGGESTION (FT4 at phase 99,999) | **open, retained** (not taken in the merge-only rounds; the PR body records it) | `tb/aecp_notify` is byte-identical to round 3, so its FT margins are unchanged. I did not re-run the other reviewer's sweep. The author's round-4b receipt (`author-r4b/receipts/reviewer-probes/ft_sweep.txt`) reports it holding. |

## 10. Real limits and pending manager duties

- **Not run by this review** (not allowed): the processor-wide `run_suites.sh` bank, the yosys bank, the parent consumer set (16 commands) at milan-fpga dev `cdf49d1a` with the combined C4 + C6 patch, and the donor bank. Their figures here are the author's and the manager's (1,019,110 checks; 16/16 rc 0; parent ports 1,757). The manager owns them, and the final current-dev candidate at the merge turn: source base `03c842a7`, live dev `cdf49d1a`.
- **Re-run, but not every campaign:** I re-ran the five campaigns the merges touch (notify, AECP, dispatch, ACMP, D3). adp, maap, srp_top, gsi, retry, srp_admission, name_wr and the nvm_port figures were checked only through `git apply --check` (adp, maap, srp_top) and the author's receipts. The hosted job ran SRP, MAAP and ADP at this head.
- **Evidence location:** the assignment's evidence link (`2c532827`) holds no `author-r4`/`author-r4b`. I used the `ppC6-review-evidence` branch at `7d8194b5`.
- **Physical calibration NOT RUN.** No hardware was used. Field skips are not hardware proof. The identify sequencer is graded in simulation only, and the parent keeps `EN_IDENTIFY_NOTIF_P` = 0.
- **Hosted/act acceptance** is the manager's. I only read the exact-head check runs.

## 11. Packet

Every file below is listed in `MANIFEST.sha256`.

- **Scripts:**
  - `both_sides.py`: the multiset both-sides check;
  - `romcmp.py`, `rom_occupancy.py`: the ROM compare and occupancy;
  - `figures_kept.py`, `figures_dropped.py`: the PR-body figure checks;
  - `notify_counts.py`, `aecp_counts.py`, `d3_counts.py`: campaign counts against the README records;
  - `vl_cap8.sh`, `vl_cap4.sh`: the pinned Verilator 5.050 with build jobs capped at 8 or 4. The D3 campaign ran `--jobs 2` with the 4-job cap, so 8 parallel jobs at most.
- **Probes** (`probes/`):
  - my round-3 probes, unchanged: `run_probes.sh`, `r420_3_probes.hpp`, `boundary_control.sh`, `r420_2_probes_unchanged.py`, `vl8.sh`;
  - this round's `stale_upc_probe.sh` and `en1_c5a_probe.sh`.
- **Receipts** (`receipts/`, campaign result files in `receipts/campaigns/`): see `receipts/REDACTION.txt` for the one redaction, the private install prefix of the pinned tool in the build logs.
- **Not published:** `scratch/`, which holds the exports, builds, campaign trees and downloaded evidence.

R420-4 FINISHED
