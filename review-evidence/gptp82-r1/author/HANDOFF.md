# [A649] #82 handoff: grandmaster thisClock and path {thisClock} from reset

Status: REVIEW READY at head 85373de0. The cold-start residual is described under Acceptance.

- Repository: Mister-M-alt/FPGA-gPTP, branch 82-boot-gm-thisclock (local only, not pushed)
- Base: b9ade3a63d1b2292d75eb9b1809647e6439542a0 (main; same tree as the parent's pin e4869fd0)
- Head: 85373de08a5c35487f260087ac8ceaf7a3789cdc
  - dafc34c0 Publish thisClock and {thisClock} from reset until a peer is elected
  - 45f78e38 Grade the boot, winning-peer and departed-peer publication with planted mutants
  - 85373de0 Document the boot grandmaster publication

## Design

- The parent shadow (`hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`, `publication_commit`, at
  e9cbb676) resets its bank to zero. It copies the engine only on `pub_commit_o`. So the
  engine must (1) name thisClock and {thisClock} on its outputs while no grandmaster has been
  elected since reset and (2) commit that state.
- thisClock exists only as a ROM constant. The RTL takes it from the existing S_CID mirror
  (`local_clock_id_r`), written by the cold init leg and kept over a warm reset.
- The ROM is full (1016/1024; the seeded images use 1017, leaving free words 127, 251-255
  and 319). A ROM-side boot leg would not fit without changing unrelated microcode, so the fix
  is RTL-only and the ROM image is unchanged: sha256 a435fba6... at base and head (default args).
- No new port, no parameter, no width change. The engine's parameter and port declarations,
  comments stripped, are byte-identical at pin, base and head (sha256 ccf818c7...).

## Changes (file:line at head)

- `hdl/top/KL_gptp_engine.sv:118-121`: port comment rewritten in the same four lines (keeps
  every ledger anchor above it), adding the boot rule.
- `:624`, `:661`: the µCPU's COMMIT now drives `ucpu_commit_w`.
- `:681-684`: comment: the reset-cleared GM now publishes thisClock and {thisClock}, not zero.
- `:771-776`: `boot_pub_pend_r`, `boot_pub_commit_r` and their rationale.
- `:798-799`: reset sets the pending flag. `:820-828`: one registered engine commit after
  each reset, once `local_clock_valid_r` is set and `dbg_busy_o` is low (no handler between
  its staging and its COMMIT). A µCPU COMMIT first cancels it.
- `:981-993`: while the raw GM is zero (no election since reset): `pub_gm_id_o` = thisClock
  (or zero before a cold start installs it), `pub_path_count_o` = 1 (0 before install), tail zero.
  `pub_commit_o = ucpu_commit_w || boot_pub_commit_r`. The raw bank and µcode reads are unchanged.
- `docs/SOURCE_EVIDENCE.md:31`: two anchors moved (L929->L947, L934->L952).
- `docs/INTEGRATION.md:462-498`: new "Before any peer" subsection. `docs/HDL_DEVELOPER.md:176-186`
  extends the publication invariant. `docs/TEST_DEVELOPER.md:109-110` adds two engine-suite lines.
- `tb/verilator/engine/sim_main.cpp`: PubSnap gains `cyc` and `flags`, plus helpers
  `committed_path_is` (:1000) and `first_commit_since` (:1009) and `cold_boot_mark` (:1114).
  There are two new phases, 1d (:1155) and 35 (:4738), and the header map has new entries
  (:21, :143).
- `tb/verilator/engine/mutants.py:291-333`: six #82 controls. `:459-471`: a #82 control must fail
  every check it names.

Timing as seen by the parent: after a warm reset the commit arrives one cycle after release.
After a cold start the commit follows the first one-second timer beat, about 1.2 s after reset,
because that beat's init leg installs thisClock. Before that, outputs and the shadow stay zero,
as at base. This gap is the only residual against "from reset". Closing it needs either the
identity before the first beat, which would be a parameter or port and therefore a STOP, or
ROM space that does not exist.

## New checks, mutants, failing words

There are ten new checks; each runs in all three images (shipping, request seed, Sync seed). A
#82 mutant must fail every check it names, and the arm enforces this (`mutants.py:459-471`).
Non-vacuity of that rule: a meta-run that adds a name the mutant cannot fail reports
`[FAIL] mutant 'becoming grandmaster keeps the departed GM' missed its named check(s): #82 peer wins: its commit names the peer GM`, rc 1.
Failing words are verbatim from the head mutant run.

| new check | mutant (`mutants.py` line) | failing words |
|---|---|---|
| cold boot: a commit lands with the first beat | no engine commit after reset (:312, RTL) | `FAIL #82 cold boot: a commit lands with the first beat got 0000000000000000 exp 0000000000000001` |
| cold boot: first commit names thisClock | boot publication restored to zero (:293, RTL) | `FAIL #82 cold boot: first commit names thisClock got 0000000000000000 exp 02a1b2fffec3d4e5` |
| cold boot: first commit path is {thisClock} | boot publication restored to zero (:293, RTL) | `FAIL #82 cold boot: first commit path is {thisClock} got 0000000000000000 exp 0000000000000001` |
| warm reset: a commit follows the release at once | no engine commit after reset (:312, RTL) | `FAIL #82 warm reset: a commit follows the release at once got 0000000000000000 exp 0000000000000001` |
| warm reset: first commit names thisClock | boot publication restored to zero (:293, RTL) | `FAIL #82 warm reset: first commit names thisClock got 0000000000000000 exp 02a1b2fffec3d4e5` |
| warm reset: first commit path is {thisClock} | boot publication restored to zero (:293, RTL) | `FAIL #82 warm reset: first commit path is {thisClock} got 0000000000000000 exp 0000000000000001` |
| peer wins: its commit names the peer GM | thisClock hides an elected peer (:317, RTL) | `FAIL #82 peer wins: its commit names the peer GM got 02a1b2fffec3d4e5 exp 0082a0fffe000001` |
| peer wins: its commit carries the peer path | an elected peer keeps the self path (:321, RTL) | `FAIL #82 peer wins: its commit carries the peer path got 0000000000000000 exp 0000000000000001` |
| peer leaves: the mastership commit names thisClock | becoming grandmaster keeps the departed GM (:325, ROM) | `FAIL #82 peer leaves: the mastership commit names thisClock got 0082a0fffe000001 exp 02a1b2fffec3d4e5` |
| peer leaves: the mastership commit path is {thisClock} | becoming grandmaster keeps the departed path (:330, ROM) | `FAIL #82 peer leaves: the mastership commit path is {thisClock} got 0000000000000000 exp 0000000000000001` |

Check names in the harness all start with `#82 ` (prefix dropped in the first column).

The three scenarios:
- Boot, no peer: phase 1d (cold reset, `sim_main.cpp:1155`), plus the first half of phase 35,
  a warm reset (`:4738`).
- Peer wins: phase 35. The peer starts from the boot state (raw GM zero after the warm reset),
  with p1 0 and a three-entry PathTrace {GM82, HOP82, SRC82}.
- Peer leaves: phase 35. The Announces stop, asCapable is held, and after the 3 s receipt
  timeout the mastership commit is graded.
- The existing `announce()` helper always sends a one-entry PathTrace. So the win/leave path
  checks use their own three-entry path: a one-entry peer path is indistinguishable from
  {thisClock} by count.

Control at base RTL (new harness, base engine): `1623 checks: 1617 PASS, 6 FAIL`. Exactly the
six boot checks fail. The win and leave checks pass at base, because that behaviour already
existed and is only now graded at the commit.

Measured (scratch copy of the harness that prints the cycle): the cold-start first commit
lands 2,400,604 cycles after reset release at 2 MHz, which is 1.2003 s.

## Repository gates (pinned Verilator 5.050 first on PATH, TMPDIR in scratch, never piped)

| gate | base b9ade3a6 | head 85373de0 |
|---|---|---|
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make docs` (incl. diagrams-check, both selftests) | rc 0, 20 exact anchors | rc 0, 20 exact anchors |
| `make -C tb/verilator/ucpu` | rc 0, 768 | rc 0, 768 |
| `make -C tb/verilator/parser` | rc 0, 337 + mutants 9/9 | rc 0, 337 + mutants 9/9 |
| `make -C tb/verilator/engine run` | rc 0, 1613 x3 | rc 0, **1623 x3** |
| engine `mutants.py`, foreground shards | 6 shards rc 0: 33/33 caught | 8 shards rc 0: **39/39** caught |
| `make -C tb/verilator/gaskets` | rc 0, 81 + 5/5 | rc 0, 81 + 5/5 |
| `make -C tb/tsngen` | rc 0, 288 + 4/4 | rc 0, 288 + 4/4 |
| `make -C bench/arty test` | rc 0, PASS | rc 0, PASS |

Head runs started from `make clean`. The Makefile's `clean` deletes the tracked
`syn/ooc/work/gptp_ucode.hex` (pre-existing); I restored it with `git checkout` and the tree is clean.
`make ooc` needs Vivado and is not a gate here (no CI workflow in this repository).

Process note: `make -C tb/verilator/engine mutants` as one command runs past the 10-minute
foreground limit. A first unsharded base attempt went to the background, and I removed its work
directory while it was still running. That run is void, with no tally. The arm was then run as
foreground shards. A scratch wrapper loads the suite's own `mutants.py`, sets `MUTATIONS[k::n]`
and calls its own `main()`, so each shard includes the clean control.

## Scratch-parent consumer gates (milan-fpga dev e9cbb676)

Setup. The parent was cloned at dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` with all
submodules. The base column is dev's own gitlink `e4869fd0`, whose tree is identical to this
lane's base `b9ade3a6`. For the head column, a second scratch copy has `gptp-processor` fetched
from the lane, checked out at `85373de0`, and staged with `git add` in the index only. Before
every git command in a submodule, I verified that `rev-parse --show-toplevel` named it. No
parent commit was made and nothing was pushed. Tools: Verilator 5.050 (pinned), Yosys 0.66
(sha 86f2ddeb, the CI pin), sv2v v0.0.12 (CI pin). The tsn-gen field oracle was built from
source at the CI pin `deca300c` in scratch. TMPDIR was in scratch.

STOP check: the engine's parameter and port declarations (comments stripped) are
byte-identical at pin, base and head. The shadow's instance is unchanged. The ROM digest is
unchanged (`a435fba6...`, identical to the ledger row for pin `e4869fd0`). No STOP condition
was met.

| consumer gate | base (gitlink e4869fd0) | head (gitlink 85373de0, index only) |
|---|---|---|
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` (CI yosys-elaboration) | rc 0; cells 74511 / 61944 / 3368 | rc 0; cells 74523 / 61944 / 3380 (+12 in the plane) |
| `python3 scripts/lint_rtl.py --check --self-test` (CI verilator-lint, ratcheted) | rc 0, 90 <= ratchet 90 | rc 0, 90 <= ratchet 90 |
| `scripts/check_port_contracts.py` + `--selftest` | rc 0 / rc 0 | rc 0 / rc 0 |
| `scripts/check_wire_accountability.py --self-test` | rc 0 | rc 0 |
| `scripts/check_gptp_docs.py` + `--selftest` | rc 0 (8 pages) / rc 0 (30 controls) | rc 1 / rc 1 as committed: 35 findings, all "donor reference must use gitlink 85373de0, found e4869fd0" (the parent's pin-bump rule). With the eight parent docs re-pointed to the head SHA in scratch: rc 0 (8 pages) / rc 0 (30 controls). Reverted. |
| `syn/yosys/ooc.sh tcam` (ROM-digest ledger keyed by pin) | rc 0 | rc 2 before the pin is recorded (`no recorded content digest for gptp_ucode.hex at gptp-processor pin 85373de0...`, the normal pin-bump refusal). `--record-rom-digests` (scratch) adds exactly one row, `85373de0... gptp_ucode.hex a435fba6...`, the same digest as the `e4869fd0` row. Then tcam rc 0. Reverted. |
| `make -C tb/verilator/gptp_shadow run` | rc 0, 309/309 | rc 0, 309/309 |
| `make -C tb/verilator/gptp_shadow lifecycle` | rc 0, PASS | rc 0, PASS |
| `make -C tb/verilator/gptp_shadow mutants` | rc 0, controls 9, failures 0 | rc 2, `REFUSED: required dependency gitlinks differ from HEAD` |
| `make -C tb/verilator/gptp_tables` (limits + run + mutants) | rc 0: 36 checks; controls 26, failures 0 | limits + run PASS (36 checks); mutants rc 2, the same REFUSED |
| `make -C tb/verilator/gptp_txts run` | rc 0, 85 checks | rc 0, 85 checks |
| `make -C tb/verilator/gptp_txts mutants` | rc 0, controls 6, failures 0 | rc 0, controls 6, failures 0 |
| `make -C tb/verilator/gptp_plane` (run + phc-step) | rc 0 (585 s): 29; phc_step 62; campaign 8 | run rc 0: 29; phc-step rc 0: 62; campaign 8 |
| `make -C tb/verilator/tsn_fuzz ptp` (TSN_GEN_ROOT = pinned oracle) | rc 0, 677 pass, 0 fail, 0 known gaps; freshness 1/1 | rc 0, 677 pass, 0 fail, 0 known gaps; freshness 1/1 |
| `make -C tb/verilator/milan_dp build-gptp exec-gptp` (plane-on datapath leg, GET_AVB_INFO / GET_AS_PATH) | rc 0, 182/182 | rc 0, 182/182 |
| `make -C tb/verilator/milan_dp gptp-lat` | rc 0, 182/182 | rc 0, 182/182 |
| `make -C tb/verilator/milan_dp gmstep` (the milan_dp_gm_steps leg) | rc 0, 190 checks, 0 failures | rc 0, 190 checks, 0 failures |

Not run, recorded rather than hidden:
- The gptp_shadow and gptp_tables mutant arms at head. `private_inputs.py:186-188` refuses
  unless the dependency gitlink is committed in the parent's HEAD, and I am not allowed to
  commit in the parent. They pass at base. Both suites' own checks pass at head.
- `milan_dp_gm_steps`' `gmstep_mutants.py`. The gmstep leg itself ran (above).
- Suites whose driver deadline is beyond a 10-minute foreground command: the full `milan_dp`
  `run` (4800 s), `milan_dp_gptp` / the physical-gptp job (5400 s), `capture_coherence`
  (2400 s), `milan_dp_mclk` (3600 s) and `milan_dp_render`. Most `milan_dp` cases elaborate
  with `GPTP_PLANE_EN_P=0`, where the engine is absent. The plane-on legs `gptp`, `gptp-lat`
  and `gmstep` ran above.
- `publication_census` follows the protocol processor's class-D values, not the gPTP bank.
- The tsn_fuzz and gptp suites rewrite `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` with a new
  timestamp (same `677 pass`). I reverted it in both scratch copies.

Consequence the parent will see (by reading `KL_gptp_shadow.sv` publication_commit; every
suite above passes with it): the boot commit is a GM edge from 0 to thisClock. So
`pub_disc_o` pulses once and `pub_path_gen_o` advances once after each reset.

## Acceptance

- Assignment 1, from reset: met after a warm reset (commit one cycle after release). On a
  cold start it is met from the first timer beat (1.2003 s measured). Before that, the engine
  does not yet hold thisClock, and outputs and shadow stay zero as before. This is the one
  residual, and it is why the PR body says "Refs #82", not "Closes #82". Closing it needs the
  identity at reset (a parameter or port, which is a STOP) or ROM words that do not exist.
- Assignment 1, a better GM takes over, and the instance returns to thisClock when it leaves:
  met and graded (phase 35). The return still requires asCapable at the receipt timeout, as
  before.
- Assignment 2, interface: width and commit timing are unchanged (a single-cycle pulse over
  stable outputs). Cases and mutants exist for boot (cold and warm), win and leave.
- Assignment 3: repository gates rc 0 at base and head. Consumer gates: the table above. Gaps
  are listed under "Not run".
- Assignment 4: no interface or parameter change, so no STOP.

## Known limits, unchanged here

- If asCapable falls before an elected peer's Announces stop, the receipt timeout cannot become
  master (BECGATE). The departed peer then stays published. 802.1AS-2020 10.3.13.2.4 a) would
  age it out regardless.
- From reading the BTCA code (not tested): after a warm reset the scratch best record
  survives. An Announce worse than that retained record takes `they_win` and re-publishes the
  retained GM.
- At boot, gm_present (flags bit 0) stays 0 and the parent identity stays 0, as before.
  Whether gmPresent should follow 10.3.13.2.4 g) at boot is outside this lane.

## Posting

- TAKEN: issuecomment-6249586531.
- REVIEW READY: issuecomment-6250813690 (head 85373de08a5c35487f260087ac8ceaf7a3789cdc).

Not done, by rule: no push, no PR created or edited, no parent commit, no hardware.
Scratch (not in this directory): `$VALIDATION_STORAGE/gptp82-a649/` (parent copies, tsn-gen,
gate logs `gates/` and `pgates/`, control and measurement copies).
