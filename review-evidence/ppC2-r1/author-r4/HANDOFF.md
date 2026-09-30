# [A459] Round 4 of lane C2 (MAAP), PR #135: handoff

Status: **REVIEW READY** at `47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346`, tree
`329ff52af9e1f56d408f88182f577f14ed0a7f31`. Not pushed: pushing is the manager's.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch
  `c2-maap-coverage`. `origin` was checked to be
  `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.
- Start head: `921fff59d6e1243284e477f7a368173018420d35` (PR #135, round 3).
- Main merged: `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff` (`git fetch origin main`;
  the merge of PR #136, lane C3).
- Assignment: #66 comment 5910732518 (round 4, merge only). Also read: the
  round-2 assignment 5887951933, the ruling 5890772857, both round-2 reviews
  (R401-2 5893508851 POSITIVE, R400-2 5893604815 NEGATIVE), the round-3
  assignment 5903309279 (whose gates this round repeats), and the round-3
  review packets (R400-3 and R401-3, both POSITIVE at `921fff59`).
- Issue #66 comments by this role: TAKEN 5910743406, and REVIEW READY
  5914787967 (this head). No other comment was posted, edited or deleted.
- Both items were done in the assignment's order. No STOP condition was met:
  the resolution keeps both sides and needs nothing beyond that; no module,
  top or parent port changes; nothing under `hdl/` is edited by the
  resolution (the merged `hdl/` is main's plus this branch's
  `KL_pp_maap.sv`).
- The lane checkout is left clean at `47afa74`: 0 untracked or ignored
  entries. The only build product this session made in it
  (`tb/nvm_port/__pycache__`, from the NVM figures run) was removed.

Commits (one-line subject, no body, no trailers):

| Commit | Item | Subject |
|---|---|---|
| `47afa74` | 1, the merge (parents `921fff59`, `0451d83d`) | Merge main 0451d83d (#136) into the MAAP lane, keeping both sides: the MAAP and ADP mutation campaigns and .gitattributes entries, and pp_top's maap-internal and adp-config modes (#66) |
| (PR body) | 2, the Round 4 note | `PR-BODY.md` beside this file |

## 1. Merge resolution (item 1), file by file

Merge commit `47afa74d`: parents `921fff59` (this branch) and `0451d83d` (main).
No rebase. Main brings 11 commits over the merge base `b2db3a97` (PR #136's
ten and its merge), in 45 files. Five files changed on both sides. One merged
by itself; four conflicted, as the assignment said. `git show --remerge-diff`
of the merge shows only those four.

| File | Main's side (C3, PR #136) | This branch's side (MAAP) | Resolution |
|---|---|---|---|
| `.gitattributes` | `tb/adp_engine/mutations/*.patch whitespace=-blank-at-eol,-blank-at-eof` | `tb/maap/mutations/*.patch` with the same attribute | Both lines, after the SRP line: MAAP, then ADP |
| `.github/workflows/hdl.yml` | step "ADP mutation campaign" (`make -C tb/adp_engine mutants`) after the SRP campaign | step "MAAP mutation campaign" (`make -C tb/maap mutants`) at the same place | Both steps, MAAP then ADP, both after the SRP campaign and before the traceability step |
| `tb/pp_top/Makefile` | target `adp-config` (`--adp-only`, section AD alone); `.PHONY` | target `maap-internal` (`--maap-internal-only`, section MP alone, with its comment); `.PHONY` | Both targets, `maap-internal` then `adp-config`; `.PHONY` names both |
| `tb/pp_top/sim_main.cpp`, after `run_name_writes` | section AD (`AdpConfigPhase`) and `run_adp_config` | `run_maap_internal` (MP alone on a fresh `Suite` with the image loaded) | Both: `run_maap_internal`, closed, then main's whole section AD and `run_adp_config` |
| `tb/pp_top/sim_main.cpp`, `main()` switches | `adp_only` (`--adp-only`) | `maap_only` (`--maap-internal-only`) | Both declarations |
| `tb/pp_top/sim_main.cpp`, `main()` dispatch | rewrote the section gates into `one_section = gsi_only \|\| name_only \|\| d3_only \|\| adp_only` with `if (!one_section \|\| X)` per section, plus `run_adp_config` | round 3's form: `if (maap_only) run_maap_internal(h);`, and `!maap_only` in every other gate | Main's `one_section` form, with `maap_only` added to it, and `if (maap_only) run_maap_internal(h);` kept. MP is graded inside `Suite::run` in the default run, so it keeps its own line instead of an `!one_section \|\| maap_only` gate, which would run it twice |
| `tb/pp_top/README.md` (merged by itself) | S3's new queue check; section AD's paragraph | section MP's paragraph (MP0, MP4, MP7, 34 checks) | Both kept by git; no edit |

The truth table of the merged `main()` (each row run at the merged tree, 7.1):

| Invocation | Sections run |
|---|---|
| (default) `make run` | Suite (with MP), ISI, NW, D3, AD; then the fixture build's DV |
| `--maap-internal-only` (`make maap-internal`) | MP |
| `--adp-only` (`make adp-config`) | AD |
| `--gsi-internal-only` (`make gsi-internal`) | ISI |
| `--name-writes-only` (`make name-writes`) | NW |
| `--d3-only` | D3 |
| `--dr3a` | the DR3a measurements, then return |

**Mutation patches.** None moves, so none is re-anchored. The merged `hdl/` is
byte-identical to main's except `hdl/maap/KL_pp_maap.sv`, which is this
branch's (`git diff --stat` of `hdl/` against each parent). The 27 MAAP patch
files touch only `KL_pp_maap.sv` and `KL_pp_rx_validator.sv`, which main does
not change; the 28 ADP patch files touch `KL_adp_engine.sv`, `KL_aecp_engine.sv`
and `protocol_processor_top.sv`, which this branch does not change. All 55 pass
`git apply --check` at the merged tree, and both campaigns plant them there
(section 5).

**Tallies the merge changes, none written in this branch's files.**
`tb/pp_top` goes to 7,949 (default build 7,929: this lane's 7,873 plus S3's
one new check and AD's 55; fixture 20). MP stays 34, so the `tb/maap` ledger's
pp_top rows (MP7 4 of 34, MP4 5 of 34) and `tb/pp_top/README.md`'s "34 checks"
stay true. `run_suites.sh` goes to 1,017,348.

**Tested before the commit.** The staged resolution (`git write-tree` =
`329ff52a`, the tree the commit then recorded) was exported and graded first:
`tb/pp_top` `make run` 7,949/7,949, and every focused mode rc 0 (MP 34, AD 55,
D3 133, NW 85, ISI 6,182, DR3a).

**Clause.** The merge changes no behaviour of this lane. The MAAP engine and its
tests are byte-identical to the round-3 head, so every Annex B claim that
round 3 graded still rests on the same RTL and the same checks: Table B.7,
B.3.2, B.3.5.2, B.3.6.1, B.3.6.4, B.2.3.2 and B.2.3.4, and the ruling
5890772857. The gate for the merge is therefore that each section and each
campaign still runs and fails where it should at the merged head (section 5).

**What "keeping both sides" costs, and what it does not.** In the dispatch of
`main()` the two sides wrote different forms of the same rule ("a focused mode
runs only its own section"). Main's `one_section` form is taken whole, and this
branch's mode joins it. Across the four files, two lines of the result are in
neither parent verbatim (checked line by line against both):
`tb/pp_top/sim_main.cpp:10421`, the `one_section` line with `maap_only` added,
and `tb/pp_top/Makefile:104`, the `.PHONY` line naming both targets. Neither
changes a mode's behaviour: the truth table above is round 3's, plus AD.
Nothing else needed an edit. The files that quote tallies the merge moves
name the head they were measured at (C3's `tb/adp_engine/README.md`: "7,924
checks after the merge of PR #132"), so they stay true and were left alone.
Measured at the merged tree for the record: `gate-enable-dropped` fails 4 of
7,929 in the full default pp_top run (AD0 twice, AD1b and D3R14), with MP green,
which is the same "4 in all" that line records.

**Failing arms at the merged head.** No arm is new in this round. Every arm of
both lanes is still KILLED on its named check with the tallies its ledger
records: the MAAP campaign 29 of 29, the ADP campaign 30 of 30 (section 5).

## 2. The PR body (item 2), `PR-BODY.md` beside this file

- **The header** now says that round 3's head `921fff5` merged `b2db3a97` and
  that the current head `47afa74` merges `0451d83d`, and that the Round 2, 3
  and 4 sections follow.
- **A new section, "Round 4 ([A459]): the merge of `main` `0451d83d`"**, with:
  - "The merge": the four conflicts and the auto-merged README, each
    resolution, the unchanged patches (55 of 55 apply), and the line
    references and ledger tallies that stay true;
  - "Validation (round 4, head `47afa74`)": the processor gates and the
    sixteen parent commands, with the table;
  - "Parent-visible for pin adoption (round 4)": this lane's list unchanged,
    and what the merge brings (C3's list, section 4 here);
  - "Suggestions retained (round 4)" and "What remains (round 4)".
- **Unchanged:** the `[A439]` first line, the three `Closes` lines, and every
  earlier section. There are no absolute home paths, tool names or model
  names, and no attribution footer.

## 3. Suggestions taken or retained

The assignment says "No other change", so none is taken in this round.

| Suggestion | Disposition | Reason |
|---|---|---|
| R400-3-S1, R401-3-S1 (re-flow an over-long line in `11` §6 and in `tb/maap/README.md`) | Retained | Merge-only round. Cosmetic; `make check` passes |
| R401-2 S1 (a) (timers during a drain) | Retained | As round 3: `11` §6 and the banner already carry the qualifier |
| R401-2 S2 (a stalled-drain expiry arm) | Retained | As round 3: no surviving mutant is known |
| R401-2 S3, second half (comment re-flow at `KL_pp_maap.sv:619-623`) | Retained | Merge-only round, and the resolution edits nothing under `hdl/` |
| R400-1 S1 (compare_MAC pair with equal low octets), R400-1 S2 (`MUTANT_OUTPUT` default) | Retained | As rounds 2 and 3 |

This round's own runs set `MUTANT_OUTPUT` (and each campaign's `--output`) to
paths outside `/tmp`, so R400-1 S2's shared default was not exercised.

## 4. Parent-visible list, re-read at the merged head `47afa74`

**A. This lane (rounds 1 to 3; unchanged by round 4)**

1. No port, parameter or interface change by this lane. The MAAP engine acts
   only with `cfg_maap_internal_i = 1`, which the parent ties to 0
   (`hdl/milan/milan_datapath.sv:7769`, the same line at dev `ccdd07b5` as at
   `ec0cc0c1`).
2. One test-only hierarchical observation (`tb/maap/maap_wrap.sv` `walker_o`).
   The port-contract gate passes; its inventory is now 177 with C3's.
3. Tallies at this head: `tb/maap` 196, `tb/rx_validator` 497, `tb/pp_top`
   7,949 (MP 34), `run_suites.sh` 1,017,348, the MAAP campaign 32. No parent
   file pins these counts, and no parent file cites `tb/maap`,
   `maap-internal`, `adp-config`, the ADP campaign, `dyn_cur_config_v_o`, or
   the rx_validator section names (grep of the trusted checkout).
4. Docs: REQ-MAAP-007 (round 2) and `11` §6 (round 3). The parent's
   `docs/reference/MILAN_COMPLIANCE_MATRIX.md` at `ccdd07b5` has no MAAP row.
5. The round-4 merge resolution adds nothing parent-visible: it changes
   processor tests, `tb/pp_top/Makefile`, the CI workflow and
   `.gitattributes`.

**B. What the merge brings** (C3's change through `main` `0451d83d`; PR #136's
"Round 2 parent-visible list")

1. `KL_aecp_engine` gains one output, `dyn_cur_config_v_o`, which only the
   processor top instantiates. No port or parameter of
   `protocol_processor_top`, or of any processor module the parent instantiates
   by name, changes. The port-contract gate counts the processor at 1,748
   ports (1,747 at round 3), 111 <= 111 undocumented.
2. The ADPDU's current_configuration_index is the set or restored
   configuration, and `current_cfg_i` only while the configuration row is
   unset (from reset, and after a D3 roll-back). The parent drives
   `current_cfg_i` from ADP_IDX0 and declares one configuration, so the wire is
   unchanged while ADP_IDX0 is 0.
3. The test-evidence ratchet: 73 <= 77 at this head (74 at each side's own
   head). Its armed list now names both `tb/adp_engine` and `tb/maap`. It can be
   lowered to 73.
4. Entry points: `make -C tb/adp_engine mutants` (in CI, beside the MAAP
   campaign after this merge) and `make -C tb/pp_top adp-config`.
5. Optional matrix citations: the parent's 5.6.3/5.6.4 row can cite the MTXW
   walk, and a 5.6.1/5.6.2 citation can use P12/AD0 and P11/AD1 to AD7.
6. C3 adds no parent edit. The sixteen consumer commands pass with the
   manager's combined #132 + C1 adaptation alone (section 6).

**C. Unchanged from round 3:** PR #132's consolidated list and C1's section 4
(round 3 handoff, section 6 B), and the combined adaptation
`parent-adaptation-132-c1.patch` (beside this file; 18,135 bytes, sha256
`2ba66803…ddc420`, byte-identical to round 3's). It applies cleanly at
`ccdd07b5` (13 files). The parent documents in those lists are the adoption
lane's.

## 5. Processor gates at `47afa74`

**Tools.** Verilator 5.052 (`/usr/bin/verilator`, sha256 `098b09b1…7581`, the
same binary as rounds 2 and 3). Every build went through the wrapper
`$VALIDATION_STORAGE/ppC2-a459/bin/verilator` (sha256 `58b08717…fbcf`, the same
content as round 3's), which rewrites `-j 0` to `-j 8`. `make check` used a
wavedrom venv at `$VALIDATION_STORAGE/ppC2-a459/venv-wavedrom`, first on `PATH`,
outside the tree. Heavy jobs ran one at a time. No command was piped; each
wrote its log to a file.

**Where.** A `git archive` export of the head, `$VALIDATION_STORAGE/ppC2-a459/head`
(tree `329ff52a`), for the suites, the campaigns, Yosys and the pp_top
targets. In the lane, with a clean worktree: `make check`, `git diff --check`,
and `make -C tb/nvm_port figures`, which reads old revisions through git.
Runs over one 10-minute call (`run_suites.sh`, the four campaigns and two
parent commands) ran detached with their rc written by the wrapping shell,
and were awaited in consecutive foreground calls, never beside another build.

### 5.1 Before the commit (the staged tree `329ff52a`, exported)

| Run | rc | Result |
|---|---|---|
| `make -C tb/pp_top maap-internal` | 0 | 34 checks, 0 failures |
| `--adp-only`, `--d3-only`, `--name-writes-only`, `--gsi-internal-only`, `--dr3a` | 0 each | AD 55, D3 133, NW 85, ISI 6,182, DR3a measurements |
| `make -C tb/pp_top run` | 0 | 7,949/7,949 (default build 7,929: the Suite with MP, ISI, NW 85, D3 133, AD 55; fixture build 20) |

### 5.2 Suites and entry points at the head

| Entry point | rc | Result |
|---|---|---|
| `./scripts/run_suites.sh` (export; 683 s) | 0 | 33 suites, **1,017,348 checks**, 0 failing. maap 196, rx_validator 497, adp_engine 1,367, pp_top 7,949, acmp_nvm 360, srp_top 2,200, srp_encoder 581, srp_stream_fsms 1,219 |
| `./scripts/lint_hdl.sh` (export) | 0 | 41 LINT OK |
| `python3 scripts/gen_matrix.py --check` (export) | 0 | 94 rows, 0 untested |
| `make check` (lane) | 0 | mermaid 41 + wavedrom 18, wavedrom-check 18, links 981, matrix 115 REQ / 17 GAP, modmatrix 94, params 26/26/26 |
| `git diff --check <base> 47afa74d` for `c951a9ff`, `921fff59`, `b2db3a97`, `0451d83d` | 0, 0, 0, 0 | |
| `make -C tb/maap mutants` (250 s) | 0 | **32/32**: 3 controls PASS (196, 34, 497), 29 of 29 KILLED (5.3) |
| `make -C tb/adp_engine mutants` (C3's; 340 s) | 0 | **32/32**: 2 controls PASS, 30 of 30 KILLED (5.4) |
| `make -C tb/srp_top mutants` (C1's; 1,768 s) | 0 | **90/90**: 11 controls PASS, 78 arm runs KILLED, assertion coverage 65/65 |
| `python3 tb/pp_top/d3_mutants.py --jobs 1` (#132's; 4,938 s) | 0 | **83 of 83 KILLED** by their named checks; goldens acmp_nvm, pp_top, rx_validator PASS |
| `python3 tb/pp_top/gsi_mutants.py` (784 s) | 0 | 20 mutations detected by named checks; golden and restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | the decode mutant killed (34 named failures); golden and restored PASS |
| `make -C tb/nvm_port figures` (lane) | 0 | "all measured figures agree with the tree" |
| `./syn/yosys/run.sh` | 0 | 36 YOSYS OK, plus `KL_aecp_engine` YOSYS XILINX OK |
| `make -C tb/pp_top maap-internal` / `adp-config` / `gsi-internal` / `name-writes` | 0 each | 34 / 55 / 6,182 / 85 checks, 0 failures |
| `tb/pp_top`: `./obj_dir/Vpp_top_sim --d3-only`, `--dr3a` | 0, 0 | D3 133, 0 failures; DR3a measurements |

Two first attempts failed for reasons outside the tree, and each was rerun
where it belongs:

- `make -C tb/nvm_port figures` in the export: rc 2. Every measured figure
  agreed, and only its git-form pins failed ("cannot read dc354be~1": the export
  has no repository). Rerun in the lane: rc 0.
- `--d3-only` launched from the export root instead of `tb/pp_top`: rc 1, 55 of
  133 failing, because the binary loads `ucode.hex` and `ltn_rom.hex` and
  writes `obj_dir/build_tally.txt` by relative path. Rerun from `tb/pp_top`:
  133/0, as at 5.1.

### 5.3 MAAP mutant table (`make -C tb/maap mutants` at `47afa74`)

Every row equals round 3's table and `tb/maap/README.md`'s ledger.

| Arm | Named failures / suite checks |
|---|---|
| (controls) maap / pp_top `maap-internal` / rx_validator | 196/0, 34/0, 497/0 PASS |
| `fit-compare-forced-true` | 5 of 196 (U17 named 4) |
| `fit-compare-off-by-one` | 7 of 195 |
| `seed-clamp-removed` | 6 of 196 |
| `release-keeps-draw-mark` | 9 of 194 |
| `validator-maap-version-1-only` | rx_validator F29 47 of 497; pp_top MP7 4 of 34 |
| `compare-mac-forward` | maap 9 of 194; pp_top MP4 5 of 34 |
| `probe-rprobe-never-yields` | 2 of 196 |
| `defend-rdefend-ignored` | 8 of 194 |
| `defend-rdefend-no-tiebreak` | 2 of 196 |
| `probe-rannounce-tiebreak` | 7 of 196 |
| `yield-reuses-range` | 8 of 196 |
| `ival-sends-after-release` | 8 of 196 |
| `post-publishes-after-release` | 4 of 194 |
| `tx-path-absorbs-release` | 10 of 190 |
| `off-waits-for-an-edge` | 9 of 189 |
| `rx-release-returns-to-idle` | 3 of 195 |
| `seed-rearmed-on-idle-release-only` | 2 of 196 |
| `seed-clamp-off-by-one` | 2 of 196 |
| `release-waits-for-draw` | 1 of 196 |
| `idle-serves-a-latched-expiry-first` | 3 of 196 |
| `teardown-keeps-announce-timer` | 1 of 196 |
| `drain-waits-for-the-link` | 5 of 196 |
| `tx-set-omits-alloc` / `-gwait` / `-commit` | 3 of 196 each (U29 x3) |
| `tx-set-omits-write` | 7 of 192 |
| `tx-set-omits-lane` | 6 of 194 |

### 5.4 ADP mutant table (`make -C tb/adp_engine mutants` at `47afa74`)

Every failure count equals `tb/adp_engine/README.md`'s ledger ("Failing
checks"): `cfg-read-live` 1, `cfg-dependent-field` 14, `cfg-dependent-field-top`
7, `cfg-frozen-at-top` 4, `cfg-overlay-only` 4, `cfg-nonzero-for-valid` 3,
`cfg-valid-not-sticky` 7, `cfg-valid-any-selector` 1, `cfg-valid-ucpu-bus` 3,
`cfg-valid-hard-reset` 2, `cfg-valid-no-reset` 5, `gate-enable-dropped` 30,
`gate-enable-dropped-top` 3, `walk-down-answers-discover` 16,
`walk-delay-ignores-link-down` 4, `walk-down-answers-gm-change` 8,
`walk-down-shutdown-departs` 1, `walk-delay-answers-discover` 9,
`walk-delay-shutdown-silent` 4, `walk-stale-draw-arms` 4,
`walk-departing-keeps-index` 6, `walk-foreign-discover-answered` 8,
`walk-link-down-keeps-timer` 3, `disc-fresh-checks-gm` 3,
`disc-not-discovered-checks-index` 14, `disc-not-discovered-checks-interface` 3,
`disc-restart-not-rediscovered` 4, `disc-departing-ignores-interface` 3,
`disc-stray-noadp-departs` 2, `disc-unbind-keeps-timer` 2. All 30 KILLED on
their named checks; the pp_top arms ran through the merged `adp-config` target.

## 6. Parent consumer gates (the manager's sixteen commands)

**The command set.** The manager's sixteen commands, in the manager's order, as
listed in PR #133's body (Round 2 validation) and used in round 3.

**Scratch parent** (`$VALIDATION_STORAGE/ppC2-a459/parent`):

- A `git archive` of the trusted read-only checkout at `ccdd07b5`, committed
  into a scratch repository. Its tree equals `ccdd07b5`'s except the
  `protocol-processor` gitlink (`git ls-tree -r` compared: one line differs).
  Dev moved from `ec0cc0c1` to `ccdd07b5` by two docs-only commits
  (`docs/findings/`).
- Submodules: `protocol-processor` a clone of this lane at `47afa74`;
  `gptp-processor` (`5dce647`) and `third_party/verilog-axis` (`48ff7a7`) fresh
  public clones at their pins; `external` uninitialised (SSH-only, read by no
  gate). Registered with `git submodule init`.
- `parent-adaptation-132-c1.patch` applied with `git apply --check`, then
  `git apply` (13 files), and committed in the scratch repository only. No other
  parent edit: C3 adds none.
- The trusted checkout was not modified (HEAD `ccdd07b5`, 0 porcelain entries
  after the run).

| # | Command (from the scratch parent root) | rc | Result |
|---|---|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet within budget (multi-declarator 0 <= 0, long function 0 <= 0) |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | all ratchets within budget |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | PASS, 4 findings == ratchet (0 in `hdl/`, 4 in pinned processors) |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | OK: 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 6 | `python3 sw/builder/test_builder.py` (968 s, detached and awaited) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 (placement calibration), whose build report is not on this host, as in rounds 1 to 3. The two `disabled-writer ... FAIL` lines are its mutant being caught ("caught in both states") |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 | 4 legs: 595 + 635 + 595 + 295 checks, 0 failures, 0 PINMISSING |
| 8 | `python3 scripts/check_port_contracts.py` | 0 | OK: 3,781 first-party ports (processor 1,748); undocumented processor 111 <= 111; 0 wildcard, positional or hierarchical binding; inventory 177 test-only hierarchical observations |
| 9 | `python3 scripts/measure_naming.py --check` | 0 | PASS, 96 recorded |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS: 73 <= 77 without a mutation arm, 10 <= 10 unseeded, 0 <= 0 unexplained readers, 3 <= 3 wall-clock; "can be lowered to 73" |
| 11 | `python3 scripts/docs_check.py` | 0 | 0 findings across 181 md files |
| 12 | `python3 scripts/lint_rtl.py --check` | 0 | PASS, 90 <= ratchet 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | 85 warnings, none fatal, 0 PINMISSING |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` (1,495 s, detached and awaited) | 0 | every leg PASS: gptp 181, gptp-lat 181, gmstep 103, main 234, notify 378, crflic 415 (3 DUT and 3 switch LeaveAll MRPDUs), nxn 1,841, nxndv 1,843, nxn8 3,521, nxn4c 1,841, nolpf 234, prune 33, ax1x1 231, aclk 190; 30 `[AECP-WTMO]` passes; render and gmstep mutation controls 6/6 each |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | tdm8_render 65/65 and 152/152; `--leg-defects` 5/5 |

**16 of 16 rc 0.** Every tally equals round 3's, except the two C3 moves
(port count 1,748, observations 177) and the ratchet's 73.

## 7. Receipts

`receipts/` beside this file (no file over 200 KB; `SHA256SUMS` lists every
file in it):

- `tool-identity.txt`, `scratch-parent.txt`, `scratch-tree.txt`,
  `trusted-tree.txt`;
- `merge/`: `remerge-diff.txt` (the four resolved files) and `both-sides.txt`;
- `premerge/`: the staged tree's pp_top runs (5.1);
- `head/`: `summary.txt`, and one log per entry point of 5.2, with the rc,
  start and end files of the detached runs and each campaign's output
  directory (`maap-mutants/`, `adp-mutants/`, `srp-mutants/`, `d3-mutants/`,
  `gsi-mutants/`, `name-wr-mutant/`), plus
  `gate-enable-dropped-pp_top-run.log` (section 1);
- `parent-gates/`: `summary.txt`, one log per command, the rc, start and end
  files of commands 6 and 15, and extracts of the two logs over 200 KB;
- `OVERSIZE.txt`: the 8 logs over 200 KB kept only under
  `$VALIDATION_STORAGE/ppC2-a459/logs/`, each with its sha256 and size (six
  gsi-mutant run logs, `milan_dp` 1.96 MB, `pp_shadow` 288 KB).

The scratch area `$VALIDATION_STORAGE/ppC2-a459/` holds the two exports, the
scratch parent, the capping wrapper, the wavedrom venv and the full logs. It is
outside the tree and outside this directory.
