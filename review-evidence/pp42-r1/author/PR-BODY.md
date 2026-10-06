[A545] Grade the Domain and link-edge GET_AVB_INFO notification at pp_top (#42)

Closes #42

Base `main` `e6a759de`, head `72facc6d`, three commits. This lane only adds tests. It changes no RTL, register map, port or
parameter.

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
| 6. The notification rate limit is respected, never weakened | each stimulus comes at least 1,000 ms after the latest frame to A left; no RTL change | yes |

The RTL passes items 1, 2 and 3, so no STOP condition applies.

**Item 2's line reference.** The assignment cites `KL_srp_domain.sv:157` for the revert. That line is the LINK_DOWN revert, and
it strobes only from ADOPTED. A *declaration* of the default values strobes from the adoption arm at `:184` instead: a received
Domain that differs from the operating one is adopted, even when it carries the default's values. So `srp_domain_adopted_o`
stays 1 after DN2 (the section prints it). DN2 grades the declaration, as item 2 asks. The `:157` revert is not graded on its
own at `ev_avb_i`. It fires on the same edge that raises the link term of this OR, so removing `srp_evt_domain_change_w` still
leaves a notification on that edge. DV5 already grades the revert's DOMAIN_CHANGE.

**Item 6, the rate limit.** The only notification rate limit 06 section 7 defines is GET_COUNTERS': `T-CTR-NOTIF`, one second
per descriptor from the previous round's last send. GET_AVB_INFO coalesces into one pending bit (`pe_avb_r`) and has no limit.
The bench still waits out that second before every stimulus, and each observation window is 1.2 s. So no count depends on
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

Pinned Verilator 5.050. Every gate below ran at base and at head with rc 0; nothing was piped. A local front end admitted two
to four Verilator builds at once (tuned to the host's memory cap) and set their C++ build's `-j 0` to `-j 5`. It changes only
build parallelism.

| Gate | Base `e6a759de` | Head `72facc6d` |
|---|---|---|
| `./scripts/run_suites.sh` | 33 suites, 1,021,651 checks | 1,021,666; the only differing lines are pp_top's tally (10,444 to 10,459) and the total |
| `make -C tb/pp_top` (six builds) | 10,444 | 10,459 (first build 9,956 to 9,971). Every other graded line is identical; the only extra lines are DN's seven, and one unittest timing line differs |
| `./scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check`, `./syn/yosys/run.sh` | rc 0 | rc 0; all four logs byte-identical to base |

At base, `make check` first failed: the Mermaid lint's browser launch timed out at 30 s under host load. The retry passed and
is the record. The head ran once.

**Campaigns.** These are every campaign that builds a changed file: the eight `tb/pp_top` drivers, plus the pp_top arms of
`tb/adp_engine` and `tb/maap`. Records were compared arm by arm, on every FAIL, `[i]`, tally and verdict line:

| Driver (`--jobs`) | Base | Head | Records |
|---|---|---|---|
| `notify_mutants.py` (3) | 56 of 56 KILLED, 7 goldens PASS | 65 of 65 KILLED, 8 goldens PASS | the 63 base records identical (verdict and every failing check); 9 controls and DN's golden are new |
| `d3_mutants.py` (3) | 110 of 110 KILLED, goldens PASS | the same | 116 of 116 identical |
| `aecp_mutants.py` (2) | 67 of 67 | the same | 67 of 67 identical |
| `aecp_dispatch_mutants.py` (2) | 44 of 44 | the same | 44 of 44 identical, once the integer printed by the unbound `%d` at `d3_phases.hpp:2963` and `:2993` is masked (it prints garbage at base and head alike) |
| `acmp_mutants.py` (2) | 33 of 33 KILLED, goldens PASS | the same | 37 of 37 identical |
| `ctr_mutants.py` (2) | 18 of 18 | the same | 18 of 18 identical |
| `gsi_mutants.py` (1), `name_wr_mutant.py` | 20 detected; decode killed; goldens and restored PASS | the same | 44 and 6 identical |
| `tb/adp_engine/mutants.py` (1), `tb/maap/mutants.py` (1) | 43 and 32 | the same | 43 and 32 identical |

Every existing arm still plants at head: none was refused, and every one gives its base verdict.

**Parent consumer set (17)** at milan-fpga dev `28f9666f` with only the #148 adoption patch (`git apply --check` clean;
sha256 `bbd0301d…ecfea83`, 966 bytes). The scratch parent is uncommitted; its processor worktree and index gitlink were set to
base, then head:

| # | Gate | Result |
|---:|---|---|
| 1-8, 3b, 11 | C++ and Python idiom, RTL source lists and their self-test, `pp_srcs`, port contracts, naming, test evidence, docs, `lint_rtl` | rc 0 at both; logs identical except gate 2's Python line count, 199,989 to 200,035 (`notify_mutants.py` +46) |
| 9 | `scripts/xvlog_gate.py --check`, under the shared lock | PASS, 2 findings == ratchet, at both; identical but for the pinned sha line |
| 10 | `sw/builder/test_builder.py` | "ALL GATES PASS EXCEPT 1 NOT RUN" at both (gate 11: its external build tree is not on this host); identical but for timings and temporary names |
| 12 | `make -C tb/verilator/pp_shadow -j16` | legs of 606, 606, 646 and 311 checks, 0 failures and no `[FAIL]` at both |
| 13, 14 | `nvm_cosim` lint, quick | rc 0 at both; lint identical but for Verilator's timing lines; quick 315 of 315 at both |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | every leg passes at both; all 1,313 pass, fail, check, verdict and result lines identical (sorted; `-j` interleaves them) |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0 at both; identical tallies and graded lines; the image `checksum` lines print only in the base run, where make regenerated the image |

## What remains

- **The LINK_DOWN revert (`KL_srp_domain.sv:157`) is not separately graded at `ev_avb_i`**, for the reason given under item 2.
- **The msrp_mappings words are not graded.** They are the integrator's answer, so this repository grades only the trigger.
- **Not run.** No hardware or bench access; physical behaviour is not tested.
