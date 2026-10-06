# [A545] #42 lane handoff (round 2)

- Repository: processor, branch `pp42-domain-notify` (not pushed by this lane; PR #164 exists from round 1).
- Base: processor `main` `7e5415e069cae46b63cafcc9e6ac9f68e058d9d0` (#134). Head: `9be9cd7af428a9497a9ca2a8dad716823ca3bb6a`.
- Round-2 assignment: processor issue #42, comment 6011607356, on reviews R502-1 (6011601546) and R503-1 (6011470805), both
  NEGATIVE on one shared MINOR. TAKEN (round 2): comment 6011627708 (2026-10-06 07:35 UTC). REVIEW READY (round 2): comment 6014791867
  (2026-10-06 10:59 UTC).
- Status: **REVIEW READY** at head `9be9cd7a`. Both round-2 items are corrected and processor main is merged. Every
  processor gate, every campaign that builds a changed file and the parent consumer set of 17 are rc 0 at base and head; the
  only records that move are the pp_top count (10,444 to 10,459, total 1,028,235 to 1,028,250), the `notify_mutants.py`
  record's nine new controls and golden, and the parent's Python line count (+46).
- A test-only lane: no RTL, register-map, port or parameter change. Round 2 changed only comments and README text on top of the
  `--no-ff` merge of processor main. No STOP condition applies.
- Pinned Verilator 5.050 (wrapper sha256 `905795b9...`) on PATH; the host default 5.052 was not used. A local front end
  (`bin/verilator` in the scratch directory) admitted at most N Verilator `--build` runs at once (N = 3 or 4, tuned to the
  12 GB cap; the unit's peak was 10,031 MiB) and set their C++ build's `-j 0` to `-j 5`. It changes only build parallelism.
- Scratch directory: `$VALIDATION_STORAGE/pp42-a545` (`base2/`, `head2/`: round-2 gate and campaign logs with rc files;
  `pgates/base2`, `pgates/head2`: parent gates; `probe/`: the timing-probe copy; `parent/`: the scratch parent; `bin/`: the
  scripts). Nothing of it is in the tree or in this output directory. Base and head ran in the lane tree one after the other
  (the tree detached at `7e5415e0` for the base runs, then back on the branch); its ignored build products were removed
  (`git clean -fdX`, ignored files only) between the phases and at the end.

## Round 2 assignment items

| Item | Done | Where |
|---|---|---|
| 1. The latency figure | The README now names both starting points. The `[i]` lines time from the stimulus: the link edge, or the return of `feed()`, four idle clocks after the MRPDU's last byte. Each Domain notification leaves 495 clocks after `feed()` returns, so 499 after the last byte; each link-edge one 466 after the edge. `one_notification`'s comment says what `t0` is | `tb/pp_top/README.md:2497-2500`, `notify_phases.hpp:1709-1710`; PR body Round 2 section |
| 2. The spacing statement | Corrected text, bench unchanged. `space_out` holds a stimulus until 1,000 ms after the latest *notification* to A; the REGISTER response (solicited, not a notification) is not counted, so the first stimulus comes at the bench's clock 100,000, 96,536 clocks (965 ms) after it. Each window is 1.2 s, so every later stimulus follows the previous window directly, at least 1,000 ms after the latest notification. The `last_sent` and `space_out` comments say the same | `tb/pp_top/README.md:2506-2517`, `notify_phases.hpp:1663-1665`, `:1689`; PR body item 6 row, item 6 paragraph and Round 2 section |
| 3. Merge processor main | `7e5415e0` (#134) merged with `--no-ff` as `0f5562b`, no conflicts. #22 (PR #162) was OPEN at the start of round 2 (checked 07:35 UTC), so it is not taken. It merged later, at 09:31 UTC (processor main is now `86a7b0c5`); this head does not contain it, so the final merge turn must take that delta. pp_top campaign, notify mutants and every suite re-run (the merge's files feed srp_top, srp_stream_fsms and every suite that builds the SRP stream FSMs, pp_top included) | tables below |
| Gates and consumer set at the head | every processor gate, every campaign that builds a changed file, and the parent set of 17 (dev `28f9666f`, 148 patch), at base `7e5415e0` and head `9be9cd7a`, all rc 0 | tables below |

**Timing evidence.** R502-1's print-only probe (`receipts/probe_timing_statements.patch` of that review, sha256 `13e67662...`)
was applied to a copy of the head tree (identical to `git archive 9be9cd7a` except the probed file). Its log is
`probe-timing-head.log` in this directory (1,176 bytes, sha256 `2044cc6c...`): REGISTER response to A at 3,464, link down at
100,000 (gap 96,536); MRPDU last byte 340,030, `feed()` return 340,034, frame 495 later (= 499 after the last byte); 580,098,
580,102, 495 later; link edges 466; 8,167 ms; DN 15 checks, 0 failures. Every figure the README states is one the probe prints.

Not taken (optional, outside the round-2 assignment): R502-1's S1 (a trailing quiet window after DN3b) and S2 (grading the
coalescing of the ADOPTED LINK_DOWN edge).

## Commits (base..head)

| Commit | What |
|---|---|
| `bc74bc3` | `tb/pp_top` section DN (`notify_phases.hpp` `DomainNotifyPhase`, `run_domain_notify`) and the `--domain-notify-only` flag (`sim_main.cpp`) |
| `5cd4082` | the nine controls in `tb/pp_top/notify_mutants.py` (`DOMAIN_NOTIFY`, suite `--domain-notify-only`) |
| `72facc6` | the pp_top README (Lane C6 intro, section DN, the `notify_mutants.py` record and nine rows) and 09 section 8.4 (one row, one flag) |
| `0f5562b` | `--no-ff` merge of processor main `7e5415e0` (#134) |
| `9be9cd7` | round 2: section DN's latency and spacing statements (README) and the matching bench comments |

`git diff 7e5415e0 9be9cd7a`: 5 files, +309 -12 (round 2's own commit: 2 files, +21 -9, comments and README only).

## Items of #42

| Item | Delivered by | At head |
|---|---|---|
| 1 notify on an adopted Domain | <bench-switch-model> (premise), DN1b (exactly one frame at A, a u = 1 GET_AVB_INFO, no GET_AS_PATH), DN1c (byte-exact, `sequence_id` 2) | PASS |
| 2 notify on revert | DN2 (premise), DN2b, DN2c (byte-exact, `sequence_id` 3) | PASS |
| 3 no change, no notification | DN3 (adopted {3, 5} again), DN3b (default {3, 2} again): no DOMAIN_CHANGE and no frame in 1.2 s | PASS |
| 4 link edge | DN4b-DN4e (link down, link up: one byte-exact GET_AVB_INFO each), DN4 (premise: no DOMAIN_CHANGE at DEFAULTS) | PASS |
| 5 mutation | nine controls, 9 of 9 KILLED; `avb_domain_term_dropped` fails DN1b, DN1c, DN2b and DN2c; every existing arm still plants and keeps its base record | done |
| 6 rate limit | 06 section 7's only notification limit is GET_COUNTERS' `T-CTR-NOTIF`; GET_AVB_INFO has none (one pending bit, `pe_avb_r`). The bench waits 1,000 ms after the latest notification to A before every stimulus (`space_out`); the first stimulus comes 965 ms after the REGISTER response, which is not a notification. RTL untouched | done |

**Item 2's citation.** `KL_srp_domain.sv:157` is the LINK_DOWN revert and strobes only from ADOPTED. A declaration of the
default values strobes from the adoption arm (`:184`), and `srp_domain_adopted_o` stays 1 (DN2's `[i]` line). DN2 grades the
declaration, as the item's text asks. The `:157` revert fires on the edge that also raises the link term of the same OR, so it
cannot be told apart at `ev_avb_i`; DV5 grades its DOMAIN_CHANGE.

## New checks and their failing mutants

Section DN adds 15 checks to the pp_top count (10,444 to 10,459): the shared bench boot premise and DN0 to DN4e. Every one
fails under at least one planted control (`notify_mutants.py`, `--domain-notify-only`; head run, identical to round 1's):

| Check | What | Failing controls |
|---|---|---|
| notify bench boot premise | blank NVM, both restore walks reach done | `restore_never_done` |
| DN0 | controller A registered (premise) | `registry_never_claims` |
| DN4 | neither link edge raises DOMAIN_CHANGE at DEFAULTS (premise) | `revert_strobes_at_defaults` |
| DN4b | link down: exactly one frame at A, a u = 1 GET_AVB_INFO, no GET_AS_PATH | `avb_link_term_dropped`, `registry_never_claims` |
| DN4c | ...byte-exact at `sequence_id` 0 | `avb_link_term_dropped`, `avb_notify_not_interface`, `registry_never_claims` |
| DN4d | link up: exactly one more | `avb_link_term_dropped`, `registry_never_claims` |
| DN4e | ...byte-exact at 1 | `avb_link_term_dropped`, `avb_notify_not_interface`, `registry_never_claims` |
| <bench-switch-model> | {3, 5} adopted with one DOMAIN_CHANGE (premise) | `adoption_no_strobe` |
| DN1b | exactly one frame at A, a u = 1 GET_AVB_INFO, no GET_AS_PATH | `avb_domain_term_dropped`, `asp_takes_domain`, `adoption_no_strobe`, `registry_never_claims` |
| DN1c | ...byte-exact at 2 | `avb_domain_term_dropped`, `avb_notify_not_interface`, `adoption_no_strobe`, `registry_never_claims` |
| DN3 | the adopted {3, 5} again: no DOMAIN_CHANGE, nothing at A | `domain_same_readopted` |
| DN2 | the default {3, 2} in force with one DOMAIN_CHANGE (premise) | `adoption_no_strobe` |
| DN2b | exactly one more | `avb_domain_term_dropped`, `asp_takes_domain`, `adoption_no_strobe`, `registry_never_claims` |
| DN2c | ...byte-exact at 3 | `avb_domain_term_dropped`, `avb_notify_not_interface`, `adoption_no_strobe`, `registry_never_claims` |
| DN3b | the default again: nothing | `domain_same_readopted` |

| Control | Edit | Failing checks (head `9be9cd7a`) |
|---|---|---|
| `avb_domain_term_dropped` | `|| srp_evt_domain_change_w` removed from `.ev_avb_i` (top) | 4: DN1b, DN1c, DN2b, DN2c |
| `avb_link_term_dropped` | `|| (link_up_i != link_q_r)` removed from `.ev_avb_i` | 4: DN4b, DN4c, DN4d, DN4e |
| `asp_takes_domain` | `.ev_asp_i (gsi_asp_chg_i || srp_evt_domain_change_w)` | 2: DN1b, DN2b |
| `avb_notify_not_interface` | the AVB pick's `pick_dt_w` 16'h0009 to 16'h0024 (`KL_aecp_notify`) | 4: DN4c, DN4e, DN1c, DN2c |
| `domain_same_readopted` | the `!=` filter of `KL_srp_domain:145` dropped | 2: DN3, DN3b |
| `adoption_no_strobe` | `evt_domain_change_o <= 1'b1` of the adoption arm (`:184`) removed | 6: <bench-switch-model>, DN1b, DN1c, DN2, DN2b, DN2c |
| `revert_strobes_at_defaults` | `if (adopted_r)` of `:157` dropped | 1: DN4 |
| `registry_never_claims` | the walk's free-row claim `if (1'b0)` | 9: DN0, DN4b-DN4e, DN1b, DN1c, DN2b, DN2c |
| `restore_never_done` | `restore_done_o` tied 0 | 1: the boot premise |

## Suites (lane tree, rc 0 at both)

| Gate | Base `7e5415e0` | Head `9be9cd7a` |
|---|---|---|
| `./scripts/run_suites.sh` | 33 suites, 1,028,235 checks (pp_top 10,444) | 1,028,250; the only differing lines are pp_top's tally (10,444 to 10,459) and the total |
| `make -C tb/pp_top` | 10,444 (six builds) | 10,459; first build 9,956 to 9,971; every graded line identical except DN's seven added lines and the two tallies |
| `./scripts/lint_hdl.sh` | rc 0 | rc 0, byte-identical (`9a3703ba...`) |
| `make check` | rc 0, first try | rc 0, byte-identical (`fad87ccf...`) |
| `python3 scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | byte-identical |
| `./syn/yosys/run.sh` | rc 0 | byte-identical (`5918894a...`) |

`make check` used a scratch virtualenv carrying wavedrom 2.0.3.post3 (the CI pin) first on PATH, so the gate did not
bootstrap `.venv-wavedrom` in the tree.

What the merge of #134 moved (round-1 base `e6a759de` against round-2 base `7e5415e0`): srp_stream_fsms 1,219 to 1,347 and
srp_top 2,200 to 8,656 checks; pp_top unchanged at 10,444; all ten campaigns below record-identical between the two bases.

## Campaigns (every campaign that builds a changed file)

Compared arm by arm on every FAIL, `[i]`, tally, verdict and JSON line (`bin/cmp_camp.py`; scratch names masked; driver logs
compared sorted because worker completion order varies):

| Driver (`--jobs`) | Base `7e5415e0` | Head `9be9cd7a` | Records |
|---|---|---|---|
| `tb/pp_top/notify_mutants.py` (3) | rc 0, 56 of 56 KILLED, 7 goldens PASS | rc 0, 65 of 65 KILLED, 8 goldens PASS | the 63 base arm logs identical; `results.json`: 63 records identical in verdict and every failing check; 10 new (9 controls, DN's golden) |
| `tb/pp_top/d3_mutants.py` (3) | rc 0, 110 of 110, goldens PASS | the same | 116 of 116 identical |
| `tb/pp_top/aecp_mutants.py` (2) | rc 0, 67 of 67 | the same | 67 of 67 identical |
| `tb/pp_top/aecp_dispatch_mutants.py` (2) | rc 0, 44 of 44 | the same | 44 of 44 identical; #134 bound the `%d` of `d3_phases.hpp:2963`/`:2993`, so its D3C3/D3C4 lines are now identical unmasked |
| `tb/pp_top/acmp_mutants.py` (2) | rc 0, 33 of 33, goldens PASS | the same | 37 of 37 identical |
| `tb/pp_top/ctr_mutants.py` (2) | rc 0, 18 of 18 | the same | 18 of 18 identical |
| `tb/pp_top/gsi_mutants.py` (1) | rc 0, 20 detected, golden and restored PASS | the same | 44 of 44 identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0, decode killed, golden and restored PASS | the same | 6 of 6 identical |
| `tb/adp_engine/mutants.py` (1) | rc 0, 43 of 43 | the same | 43 of 43 identical |
| `tb/maap/mutants.py` (1) | rc 0, 32 of 32 | the same | 32 of 32 identical |

`fixture_guards.py` and `line_guards.py` run inside `make -C tb/pp_top` (green at both). No arm was refused at head, so every
existing arm still plants. `tb/srp_top/mutants.py` builds none of the lane's files (it is #134's campaign, identical at base and
head by construction) and was not run.

## Parent consumer set (17)

Scratch parent: milan-fpga cloned under the scratch directory, branch `scratch-pp42` at dev
`28f9666feab2b2ba287643c63ed3a16b1e0bb863`, never committed or pushed. Submodules at their gitlinks: `external` `efeb541a`,
`gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`; `protocol-processor` worktree and index gitlink
(`git update-index --cacheinfo`) moved to base `7e5415e0`, then head `9be9cd7a`, by `bin/pin.sh`, which first checks
`git -C <dir> rev-parse --show-toplevel` for the parent and the submodule. Only `parent-adoption-148-6c22d3ca.patch`
(sha256 `bbd0301dc7e576f51f92d24c8d140eda0666f9c6699806649365110e7ecfea83`, 966 bytes) applied (`git apply --check -R`
clean). GNU Make 4.4.1, system Python, the bounded front end as `VERILATOR`. Base ran first, then head.

| # | Command | Base: rc, s | Head: rc, s | Result |
|---:|---|---|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0, 2 | 0, 3 | identical; every ratchet held |
| 2 | `python3 scripts/check_py_idiom.py` | 0, 5 | 0, 5 | every ratchet held; the module line count moves 199,997 to 200,043 (`notify_mutants.py` +46), the only difference |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0, 2 | 0, 2 | identical |
| 3b | `python3 scripts/check_rtl_source_lists.py --selftest` | 0, 5 | 0, 3 | identical |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0, 0 | 0, 0 | identical |
| 5 | `python3 scripts/check_port_contracts.py` | 0, 3 | 0, 3 | identical |
| 6 | `python3 scripts/measure_naming.py --check` | 0, 1 | 0, 1 | identical |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0, 8 | 0, 7 | identical |
| 8 | `python3 scripts/docs_check.py` | 0, 7 | 0, 5 | identical |
| 9 | `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` | 0, 222 | 0, 1,389 (shared-lock wait) | identical but for the pinned sha line |
| 10 | `python3 sw/builder/test_builder.py` | 0, 2,034 | 0, 1,715 | "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11: its external build tree is not on this host) at both; identical but for timings and temporary directory names |
| 11 | `python3 scripts/lint_rtl.py --check` | 0, 18 | 0, 11 | identical |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0, 309 | 0, 229 | legs of 606, 606, 646 and 311 checks, 0 failures, 2,167 `[PASS]` and no `[FAIL]` at both (`-j16` interleaves lines) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0, 0 | 0, 0 | identical but for Verilator's timing and allocation lines |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0, 37 | 0, 32 | byte-identical |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0, 2,002 | 0, 1,775 | every leg passes at both; all 1,313 pass, fail, check, verdict and result lines identical (sorted; `-j` interleaves them) |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 0, 751 | 0, 710 | identical tallies and graded lines; only the base log carries Verilator's warnings, because the base run recompiled after #134's RTL change and the head run reused that build |

The 148 patch's file is the only modified file in the parent's worktree (besides the moved gitlink); the processor submodule
worktree stayed clean (`git status --porcelain --ignored` empty) throughout.

## Hygiene

- Lane tree at the end: on branch `pp42-domain-notify` at `9be9cd7a`, `git status --porcelain --ignored` empty.
- Output directory: `HANDOFF.md`, `PR-BODY.md`, `parent-adoption-148-6c22d3ca.patch` (unchanged) and `probe-timing-head.log`.

## Not done

- Nothing pushed, no PR created or edited, no hardware or bench access.
- Round 1's record (base `e6a759de`, head `72facc6d`) is in the round-1 handoff; every figure above supersedes it.
