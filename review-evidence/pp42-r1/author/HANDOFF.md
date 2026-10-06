# [A545] #42 lane handoff

- Repository: processor, branch `pp42-domain-notify` (not pushed; no PR opened).
- Base: `main` `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`. Head: `72facc6d48807808e4d97a454a0ecceb2769ac9e`.
- Assignment: processor issue #42, comment 6008771904. TAKEN: comment 6008782595 (2026-10-06 03:33 UTC). REVIEW READY:
  comment 6011206696 (2026-10-06 07:05 UTC).
- Status: **REVIEW READY** at head `72facc6d`. Every acceptance item of #42 and every item of the assignment is met; every
  processor gate, every campaign that builds a changed file and the parent consumer set of 17 are rc 0 at base and head; the
  only record that moves is the pp_top count (10,444 to 10,459) and the `notify_mutants.py` record's nine new controls.
- A test-only lane: no RTL, register-map, port or parameter change. The RTL passes items 1, 2 and 3, so no STOP applies.
- Pinned Verilator 5.050 (wrapper sha256 `905795b9...`) on PATH; the host default 5.052 was not used. A local front end
  (`$VALIDATION_STORAGE/pp42-a545/bin/verilator`, sha256 `3e582a25...`) admitted at most N Verilator `--build` runs at once
  (N = 2 to 4, tuned to the 12 GB cap) and set their C++ build's `-j 0` to `-j 5`. It changes only build parallelism.
- Scratch directory: `$VALIDATION_STORAGE/pp42-a545` (`base/`, `head/`: gate and campaign logs with rc files; `pgates/`: parent
  gates; `dev/`: a scratch copy of `hdl/`, `tb/common/` and `tb/pp_top/` where DN and its controls were first built and
  planted; `parent/`: the scratch parent; `bin/`: the scripts). Nothing of it is in the tree or in this output directory. The
  lane tree's ignored build products were removed (`git clean -fdX`, ignored files only) before the base suites restart,
  before the head runs and at the end; at the head `git status --porcelain --ignored` is empty.

## Commits (base..head)

| Commit | What |
|---|---|
| `bc74bc3` | `tb/pp_top` section DN (`notify_phases.hpp` `DomainNotifyPhase`, `run_domain_notify`) and the `--domain-notify-only` flag (`sim_main.cpp`) |
| `5cd4082` | the nine controls in `tb/pp_top/notify_mutants.py` (`DOMAIN_NOTIFY`, suite `--domain-notify-only`) |
| `72facc6` | the pp_top README (Lane C6 intro, section DN, the `notify_mutants.py` record and nine rows) and 09 section 8.4 (one row, one flag) |

Diffstat: 5 files, +297 -12.

## Items

| Item | Delivered by | At head |
|---|---|---|
| 1 notify on an adopted Domain | <bench-switch-model> (premise), DN1b (exactly one frame at A, a u = 1 GET_AVB_INFO, no GET_AS_PATH), DN1c (byte-exact, `sequence_id` 2) | PASS |
| 2 notify on revert | DN2 (premise), DN2b, DN2c (byte-exact, `sequence_id` 3) | PASS |
| 3 no change, no notification | DN3 (adopted {3, 5} again), DN3b (default {3, 2} again): no DOMAIN_CHANGE and no frame in 1.2 s | PASS |
| 4 link edge | DN4b-DN4e (link down, link up: one byte-exact GET_AVB_INFO each), DN4 (premise: no DOMAIN_CHANGE at DEFAULTS) | PASS; the bench can drive it |
| 5 mutation | nine controls, 9 of 9 KILLED; `avb_domain_term_dropped` fails DN1b, DN1c, DN2b and DN2c; every existing arm still plants and keeps its base record | done |
| 6 rate limit | 06 section 7's only notification limit is GET_COUNTERS' `T-CTR-NOTIF` (1 s per descriptor); GET_AVB_INFO has none (one pending bit, `pe_avb_r`). The bench waits 1,000 ms after the latest frame to A before every stimulus (`space_out`); RTL untouched | done |

**Item 2's citation.** `KL_srp_domain.sv:157` is the LINK_DOWN revert and strobes only from ADOPTED. A declaration of the
default values strobes from the adoption arm (`:184`), and `srp_domain_adopted_o` stays 1 (DN2's `[i]` line). DN2 grades the
declaration, as the item's text asks. The `:157` revert fires on the edge that also raises the link term of the same OR, so it
cannot be told apart at `ev_avb_i`; DV5 grades its DOMAIN_CHANGE. Recorded in the README and the PR body.

## New checks and their failing mutants

Section DN adds 15 checks to the pp_top count (10,444 to 10,459): the shared bench boot premise and DN0 to DN4e. Every one
fails under at least one planted control (`notify_mutants.py --only ...`, `--domain-notify-only`; dev copy and head runs give
identical records):

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

| Control | Edit | Failing checks (head) |
|---|---|---|
| `avb_domain_term_dropped` | `|| srp_evt_domain_change_w` removed from `.ev_avb_i` (top) | 4: DN1b, DN1c, DN2b, DN2c |
| `avb_link_term_dropped` | `|| (link_up_i != link_q_r)` removed from `.ev_avb_i` | 4: DN4b, DN4c, DN4d, DN4e |
| `asp_takes_domain` | `.ev_asp_i (gsi_asp_chg_i || srp_evt_domain_change_w)` | 2: DN1b, DN2b (2 frames: 1 GET_AVB_INFO, 1 GET_AS_PATH) |
| `avb_notify_not_interface` | the AVB pick's `pick_dt_w` 16'h0009 to 16'h0024 (`KL_aecp_notify`) | 4: DN4c, DN4e, DN1c, DN2c (SUCCESS, cdl 32) |
| `domain_same_readopted` | the `!=` filter of `KL_srp_domain:145` dropped | 2: DN3, DN3b (1 strobe, 1 frame each) |
| `adoption_no_strobe` | `evt_domain_change_o <= 1'b1` of the adoption arm (`:184`) removed | 6: <bench-switch-model>, DN1b, DN1c, DN2, DN2b, DN2c |
| `revert_strobes_at_defaults` | `if (adopted_r)` of `:157` dropped | 1: DN4 (saw 1) |
| `registry_never_claims` | the walk's free-row claim `if (1'b0)` | 9: DN0, DN4b-DN4e, DN1b, DN1c, DN2b, DN2c |
| `restore_never_done` | `restore_done_o` tied 0 | 1: the boot premise |

Measured on the wire (head): each link-edge notification leaves 466 clocks after the edge, each Domain's 495 after the
MRPDU's last byte; `sequence_id` 0, 1, 2, 3; the section spans 8,167 ms of the timebase after the registration (under the
monitor's 30 s floor).

## Suites (lane tree, rc 0 at both)

| Gate | Base `e6a759de` | Head `72facc6d` |
|---|---|---|
| `./scripts/run_suites.sh` | 33 suites, 1,021,651 checks (log sha256 `299897e7...`) | 1,021,666; `diff` shows only pp_top 10,444 to 10,459 and the total |
| `make -C tb/pp_top` | 10,444 (six builds) | 10,459; first build 9,956 to 9,971; graded lines identical except DN's seven lines, the tallies and one unittest timing line (`Ran 1 test in 0.006s` / `0.007s`) |
| `./scripts/lint_hdl.sh` | rc 0 | rc 0, byte-identical log (`9a3703ba...`) |
| `make check` | rc 0 (retry; first try rc 2: the Mermaid lint's browser launch timed out at 30 s under host load) | rc 0, byte-identical to base's passing log (`a0e958b5...`) |
| `python3 scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | byte-identical |
| `./syn/yosys/run.sh` | rc 0 | byte-identical (`5918894a...`) |

`make check` used a scratch virtualenv carrying wavedrom 2.0.3.post3 (the CI pin) first on PATH, so the gate did not
bootstrap `.venv-wavedrom` in the tree.

## Campaigns (every campaign that builds a changed file)

Compared arm by arm on every FAIL, `[i]`, tally, verdict and JSON line (`bin/cmp_camp.py`; scratch names masked; driver logs
compared sorted because worker completion order varies):

| Driver (`--jobs`) | Base | Head | Records |
|---|---|---|---|
| `tb/pp_top/notify_mutants.py` (3) | rc 0, 56 of 56 KILLED, 7 goldens PASS | rc 0, 65 of 65 KILLED, 8 goldens PASS | the 63 base arm logs identical; `results.json`: 63 records identical in verdict and every failing check; 10 new (9 controls, DN's golden) |
| `tb/pp_top/d3_mutants.py` (3) | rc 0, 110 of 110, goldens PASS | the same | 116 of 116 identical |
| `tb/pp_top/aecp_mutants.py` (2) | rc 0, 67 of 67 | the same | 67 of 67 identical |
| `tb/pp_top/aecp_dispatch_mutants.py` (2) | rc 0, 44 of 44 | the same | 44 of 44 identical with the unbound `%d` integer of `d3_phases.hpp:2963`/`:2993` masked (`sclks-bound-inclusive`, `sclks-bound-three` print different garbage at each run) |
| `tb/pp_top/acmp_mutants.py` (2) | rc 0, 33 of 33, goldens PASS | the same | 37 of 37 identical |
| `tb/pp_top/ctr_mutants.py` (2) | rc 0, 18 of 18 | the same | 18 of 18 identical |
| `tb/pp_top/gsi_mutants.py` (1) | rc 0, 20 detected, golden and restored PASS | the same | 44 of 44 identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0, decode killed, golden and restored PASS | the same | 6 of 6 identical |
| `tb/adp_engine/mutants.py` (1) | rc 0, 43 of 43 | the same | 43 of 43 identical |
| `tb/maap/mutants.py` (1) | rc 0, 32 of 32 | the same | 32 of 32 identical |

`fixture_guards.py` and `line_guards.py` run inside `make -C tb/pp_top` (both green at both). No arm was refused at head, so
every existing arm still plants. The base campaigns were restarted once, about seven minutes in, to put them behind the
bounded front end (memory had reached 11 of the 12 GB cap). The base `run_suites.sh` was restarted too: a launcher slip
started a second copy in the same tree, so both were stopped, the tree's ignored build products were removed, and one
clean run made the record. The records above are all from complete runs.

## Parent consumer set (17)

Scratch parent: milan-fpga cloned under the scratch directory, branch `scratch-pp42` at dev
`28f9666feab2b2ba287643c63ed3a16b1e0bb863`, never committed or pushed. Submodules at their gitlinks: `external` `efeb541a`,
`gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`; `protocol-processor` worktree and index gitlink
(`git update-index --cacheinfo`) moved to base, then head, by `bin/pin.sh`, which first checks
`git -C <dir> rev-parse --show-toplevel` for the parent and the submodule. Only `parent-adoption-148-6c22d3ca.patch`
(sha256 `bbd0301dc7e576f51f92d24c8d140eda0666f9c6699806649365110e7ecfea83`, 966 bytes) applied, `git apply --check` clean.
GNU Make 4.4.1, system Python, the bounded front end as `VERILATOR`. Base ran first, then head.

| # | Command | Base: rc, s | Head: rc, s | Result |
|---:|---|---|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0, 3 | 0, 2 | identical; every ratchet held (it scans `protocol-processor/tb/`, DN included) |
| 2 | `python3 scripts/check_py_idiom.py` | 0, 8 | 0, 8 | every ratchet held (over-long line 0 <= 0); the module line count moves 199,989 to 200,035 (`notify_mutants.py` +46), the only difference |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0, 3 | 0, 3 | identical |
| 3b | `python3 scripts/check_rtl_source_lists.py --selftest` | 0, 6 | 0, 5 | identical |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0, 1 | 0, 1 | identical |
| 5 | `python3 scripts/check_port_contracts.py` | 0, 5 | 0, 3 | identical: 3,824 first-party ports, protocol-processor 1,759 (no port change), undocumented 111 <= 111 |
| 6 | `python3 scripts/measure_naming.py --check` | 0, 1 | 0, 1 | identical |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0, 11 | 0, 7 | identical: 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |
| 8 | `python3 scripts/docs_check.py` | 0, 7 | 0, 7 | identical, 0 findings |
| 9 | `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` | 0, 245 | 0, 146 | PASS, 2 findings == ratchet (`KL_pp_originator.sv:194`, `KL_pp_rx_validator.sv:383`); identical but for the pinned sha line |
| 10 | `python3 sw/builder/test_builder.py` | 0, 1,693 | 0, 1,294 | "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11: its external build tree is not on this host) at both; identical but for timing figures and temporary directory names |
| 11 | `python3 scripts/lint_rtl.py --check` | 0, 13 | 0, 12 | identical, 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0, 435 | 0, 362 | legs of 606, 606, 646 and 311 checks, 0 failures, no `[FAIL]` at both; the base run compiled and the head run reused the build, so `-j16` interleaves differently (token counts are not comparable) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0, 1 | 0, 1 | identical but for Verilator's timing lines |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0, 48 | 0, 91 | 315 of 315; byte-identical logs |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0, 1,966 | 0, 1,739 | every leg passes; all 1,313 pass, fail, check, verdict and result lines identical (sorted; `-j` interleaves them) |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 0, 810 | 0, 776 | identical tallies and graded lines; the image's two `checksum` lines print only in the base run, where make regenerated it |

The 148 patch's file is the only modified file in the parent's worktree; the processor submodule worktree stayed clean
(`git status --porcelain --ignored` empty) throughout.

## Not done

- Nothing pushed, no PR opened, no hardware or bench access.
