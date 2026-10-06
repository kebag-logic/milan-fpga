[A545] Grade the Domain and link-edge GET_AVB_INFO notification at pp_top (#42)

Closes #42

Base `main` `7e5415e0`, head `9be9cd7a`, five commits: round 1's three, the `--no-ff` merge of processor main `7e5415e0`
(#134), and round 2's correction. This lane only adds tests. It changes no RTL, register map, port or parameter.

## Round 2

The round-1 review (R502-1, R503-1) found that two timing statements of section DN did not match the bench. Both are
now corrected in `tb/pp_top/README.md` and in the bench's comments (`notify_phases.hpp`). The checks and the code paths
are unchanged:

- **Latency.** The section's `[i]` lines time a Domain notification from the return of `feed()`. `feed()` returns four
  idle clocks after the MRPDU's last byte. So each Domain notification leaves 495 clocks after `feed()` returns, which is
  499 clocks after the MRPDU's last byte. Each link-edge notification leaves 466 clocks after the edge.
- **Spacing.** `space_out` waits 1,000 ms after the latest *notification* to A. It does not count the REGISTER response,
  because that is a solicited answer, not a notification. So the first stimulus comes at the bench's clock 100,000, which
  is 96,536 clocks (965 ms) after that response. Each window is 1.2 s, so every later stimulus follows the previous window
  directly, at least 1,000 ms after the latest notification.

R502-1's print-only probe, run on the head tree, prints exactly these clocks. The REGISTER response to A leaves at 3,464,
and link down comes at 100,000. Last byte and `feed()` return fall at 340,030 and 340,034, then at 580,098 and 580,102. The
`[i]` lines read 466, 466, 495 and 495, and the span is 8,167 ms. Section DN still passes all 15 checks with 0 failures.

The merge of processor main `7e5415e0` (#134) had no conflicts. #22 (PR #162) was still open when round 2 started, so it is
not included. It merged later, at 09:31 UTC (main `86a7b0c5`), so this head does not contain it.

## What changes

- **`tb/pp_top` section DN** (`notify_phases.hpp`, `DomainNotifyPhase`; flag `--domain-notify-only`). It runs in the first
  build's full run, on a fresh processor of its own, so the main timeline does not move. The top ORs four triggers into
  `KL_aecp_notify`'s `ev_avb_i` (`protocol_processor_top.sv:4018`). Section V already grades `gm_change_i` and
  `gsi_avb_chg_i`. DN grades the other two: the SRP Domain machine's DOMAIN_CHANGE (`srp_evt_domain_change_w`) and the edge
  of `link_up_i`. One controller A registers. A bridge then feeds its Class A Domain in S8's certified two-class shape:
  FirstValue {5, 2, VID}, NumberOfValues 2.
- **Nine controls** in `tb/pp_top/notify_mutants.py` (`DOMAIN_NOTIFY`), each run against `--domain-notify-only`.
- **Records**: the pp_top README (the Lane C6 intro, section DN, and the `notify_mutants.py` record with nine new rows) and
  one row in 09 section 8.4.

## Acceptance

| Item | Check | At head |
|---|---|---|
| 1. A differing Domain with a controller registered: exactly one u = 1 GET_AVB_INFO for AVB_INTERFACE 0, byte-exact, no GET_AS_PATH | <bench-switch-model> (premise: one DOMAIN_CHANGE, class-D {3, 5}), DN1b (exactly one frame reaches A, a u = 1 GET_AVB_INFO, no GET_AS_PATH), DN1c (byte-exact at `sequence_id` 2) | PASS |
| 2. The declaration that returns the Domain to its default: exactly one more, byte-exact | DN2 (premise), DN2b, DN2c (`sequence_id` 3) | PASS |
| 3. An identical re-declaration: no DOMAIN_CHANGE, nothing sent | DN3 (the adopted {3, 5} again), DN3b (the default again) | PASS |
| 4. The link-edge leg of the same OR term | DN4b-DN4e (link down, then up: one GET_AVB_INFO each, byte-exact at 0 and 1), DN4 (premise: neither edge raises DOMAIN_CHANGE at DEFAULTS, so the link term is the only trigger) | PASS |
| 5. Every new check fails under a planted control; removing `srp_evt_domain_change_w` from `ev_avb_i` turns items 1 and 2 red | `avb_domain_term_dropped` fails DN1b, DN1c, DN2b and DN2c; the table below covers every check | 9 of 9 KILLED |
| 6. The notification rate limit is respected, never weakened | each stimulus comes at least 1,000 ms after the latest notification to A left. The first comes at clock 100,000, 965 ms after the REGISTER response, which is not a notification. No RTL change | yes |

The RTL passes items 1, 2 and 3, so no STOP condition applies.

**Item 2's line reference.** The assignment cites `KL_srp_domain.sv:157` for the revert. That line is the LINK_DOWN revert, and
it strobes only from ADOPTED. A *declaration* of the default values strobes from the adoption arm at `:184` instead: a received
Domain that differs from the operating one is adopted, even when it carries the default's values. So `srp_domain_adopted_o`
stays 1 after DN2 (the section prints it). DN2 grades the declaration, as item 2 asks. The `:157` revert is not graded on its
own at `ev_avb_i`. It fires on the same edge that raises the link term of this OR, so removing `srp_evt_domain_change_w` still
leaves a notification on that edge. DV5 already grades the revert's DOMAIN_CHANGE.

**Item 6, the rate limit.** The only notification rate limit 06 section 7 defines is GET_COUNTERS': `T-CTR-NOTIF`, one second
per descriptor from the previous round's last send. GET_AVB_INFO coalesces into one pending bit (`pe_avb_r`) and has no limit.
The bench still waits out that second after every notification, and each observation window is 1.2 s. So no count depends on
coalescing or on a limiter. The section takes 8,167 ms of the timebase after the registration, under the controller
monitor's 30 s floor, so no CONTROLLER_AVAILABLE reaches A.

**What "byte-exact" covers.** The body is the integrator's face answer (06 section 6.10), here the bench's static words from
V1. So the check grades the trigger, the header (u = 1, A's DA and entity_id, SUCCESS, cdl 40), the entry's `sequence_id` and
AVB_INTERFACE 0. It does not grade the msrp_mappings content, which #42 places outside this repository's scope.

## New checks and their controls

Section DN adds 15 checks to the tally: the bench's shared boot premise and DN0 to DN4e. Each control was planted in a
private copy and run with `--domain-notify-only`:

| Control | Planted | Fails |
|---|---|---|
| `avb_domain_term_dropped` | `srp_evt_domain_change_w` removed from `ev_avb_i` (#42 acceptance 3) | DN1b, DN1c, DN2b, DN2c |
| `avb_link_term_dropped` | the `link_up_i` edge removed from `ev_avb_i` | DN4b, DN4c, DN4d, DN4e |
| `asp_takes_domain` | `ev_asp_i` takes DOMAIN_CHANGE too | DN1b, DN2b (a GET_AS_PATH follows each GET_AVB_INFO) |
| `avb_notify_not_interface` | the GET_AVB_INFO job names CLOCK_DOMAIN 0 | DN4c, DN4e, DN1c, DN2c (SUCCESS, cdl 32, an empty face answer) |
| `domain_same_readopted` | `KL_srp_domain` adopts an identical declaration (the `!=` dropped) | DN3, DN3b |
| `adoption_no_strobe` | the adoption arm raises no DOMAIN_CHANGE | <bench-switch-model>, DN1b, DN1c, DN2, DN2b, DN2c |
| `revert_strobes_at_defaults` | the LINK_DOWN revert strobes from DEFAULTS too | DN4 |
| `registry_never_claims` | a REGISTER never claims a free row | DN0, DN4b-DN4e, DN1b, DN1c, DN2b, DN2c |
| `restore_never_done` | `restore_done_o` tied 0 | the bench's boot premise |

## Validation

Pinned Verilator 5.050. Every gate below ran at base (`main` `7e5415e0`) and at head, all rc 0. Nothing was piped. A local
front end admitted three or four Verilator builds at once, tuned to the host's memory cap, and set their C++ build's `-j 0` to
`-j 5`. This changes only build parallelism.

| Gate | Base `7e5415e0` | Head `9be9cd7a` |
|---|---|---|
| `./scripts/run_suites.sh` | 33 suites, 1,028,235 checks | 1,028,250. The only lines that differ are pp_top's tally (10,444 to 10,459) and the total |
| `make -C tb/pp_top` (six builds) | 10,444 | 10,459 (first build 9,956 to 9,971). Every other graded line is identical. The only extra lines are DN's seven, and they print the figures above |
| `./scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check`, `./syn/yosys/run.sh` | rc 0 | rc 0. All four logs are byte-identical to base |

The merge of #134 moves srp_stream_fsms from 1,219 to 1,347 checks and srp_top from 2,200 to 8,656. Both counts are the same
at base and head. pp_top stays at 10,444 at both bases, and every campaign below gives the same record at `e6a759de` and at
`7e5415e0`.

**Campaigns.** These are every campaign that builds a changed file: the eight `tb/pp_top` drivers, plus the pp_top arms of
`tb/adp_engine` and `tb/maap`. Records were compared arm by arm, on every FAIL, `[i]`, tally and verdict line:

| Driver (`--jobs`) | Base | Head | Records |
|---|---|---|---|
| `notify_mutants.py` (3) | 56 of 56 KILLED, 7 goldens PASS | 65 of 65 KILLED, 8 goldens PASS | The 63 base records are identical in verdict and in every failing check. The 9 controls and DN's golden are new |
| `d3_mutants.py` (3) | 110 of 110 KILLED, goldens PASS | the same | 116 of 116 identical |
| `aecp_mutants.py` (2) | 67 of 67 | the same | 67 of 67 identical |
| `aecp_dispatch_mutants.py` (2) | 44 of 44 | the same | 44 of 44 identical, unmasked. #134 bound the integer that `d3_phases.hpp:2963` and `:2993` print |
| `acmp_mutants.py` (2) | 33 of 33 KILLED, goldens PASS | the same | 37 of 37 identical |
| `ctr_mutants.py` (2) | 18 of 18 | the same | 18 of 18 identical |
| `gsi_mutants.py` (1), `name_wr_mutant.py` | 20 detected; decode killed; goldens and restored PASS | the same | 44 and 6 identical |
| `tb/adp_engine/mutants.py` (1), `tb/maap/mutants.py` (1) | 43 and 32 | the same | 43 and 32 identical |

Every existing arm still plants at head: none was refused, and each one gives its base verdict.

**Parent consumer set (17)** at milan-fpga dev `28f9666f` with only the #148 adoption patch (sha256 `bbd0301d…ecfea83`,
966 bytes). The scratch parent is uncommitted. Its processor worktree and index gitlink were set to base `7e5415e0`, then to
head:

| # | Gate | Result |
|---:|---|---|
| 1-8, 3b, 11 | C++ and Python idiom, RTL source lists and their self-test, `pp_srcs`, port contracts, naming, test evidence, docs, `lint_rtl` | rc 0 at both. Logs are identical except gate 2's Python line count, 199,997 to 200,043 (`notify_mutants.py` +46) |
| 9 | `scripts/xvlog_gate.py --check`, under the shared lock | rc 0 at both. Identical except the pinned sha line |
| 10 | `sw/builder/test_builder.py` | "ALL GATES PASS EXCEPT 1 NOT RUN" at both (gate 11: its external build tree is not on this host). Identical except timings and temporary names |
| 12 | `make -C tb/verilator/pp_shadow -j16` | Legs of 606, 606, 646 and 311 checks, 0 failures and no `[FAIL]` at both |
| 13, 14 | `nvm_cosim` lint, quick | rc 0 at both. Lint is identical except Verilator's timing lines; quick is byte-identical |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | Every leg passes at both. All 1,313 pass, fail, check, verdict and result lines are identical (sorted, because `-j` interleaves them) |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0 at both, with identical tallies and graded lines |

## What remains

- **The LINK_DOWN revert (`KL_srp_domain.sv:157`) is not separately graded at `ev_avb_i`**, for the reason given under item 2.
- **The msrp_mappings words are not graded.** They are the integrator's answer, so this repository grades only the trigger.
- **Review suggestions not taken.** R502-1 S1 (a trailing quiet window after DN3b) and S2 (grading how the ADOPTED LINK_DOWN
  edge's two terms coalesce) are optional and outside #42's acceptance.
- **Not run.** No hardware or bench access; physical behaviour is not tested.
