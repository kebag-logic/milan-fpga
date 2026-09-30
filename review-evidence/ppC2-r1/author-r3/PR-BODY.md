[A439]

Closes #66
Closes #67
Closes #68

Lane C2 (MAAP) of the PP program. It drives the three MAAP behaviours the
compliance-matrix audit found untested (GAP-04: REQ-MAAP-001, -002 and -005), fixes
the one RTL defect a new test exposed, and adds a MAAP mutation campaign with a
ledger. Branch `c2-maap-coverage` from `main` `c951a9ff`. Round 1's head was
`b03d36f`. The current head `921fff5` merges `main` `b2db3a97` (Round 3 section).

Sections 1 to "What remains" are round 1's record. Their line references are
refreshed to the round-3 head `921fff5`, with the round-1 line in parentheses.
Their tallies are round 1's. "What remains" is rewritten to match round 2 and the
ruling (R400-2-F2). The Round 2 and Round 3 sections follow.

## 1. #66: the fit clamp (IEEE 1722-2016 B.1, B.3.6.1, Table B.9; REQ-MAAP-001)

- **Reject arm, deterministic** (`tb/maap` U17). The widest block (`cfg_count_i` =
  255) fits the pool only at offsets up to `0xFE00 - 255 = 0xFD01`. A kind-7 stub
  in `maap_wrap.sv` (harness only; kinds 5 and 6 pass through) hands the engine
  `0xFDFF`, then `0xFD02`, then `0xFD01`. The two overhanging draws are redrawn
  (three draws consumed), and the byte-exact PROBE names `91:E0:F0:00:FD:01`,
  count 255, whose block ends exactly at `91:E0:F0:00:FD:FF`.
- **Seed clamp** (U18). A seeded walk with `cfg_seed_offset_i = 0xFFFF` (above
  `0xFE00 - 8`) probes the clamped offset `0xFDF8` byte-exact without drawing an
  address (footnote a). It claims the block and grants its last source
  `91:E0:F0:00:FD:FF`.
- **RTL fix, found by U17b** (`hdl/maap/KL_pp_maap.sv:613-627`; `:569-577` at
  round 1). An engage fall (Release! or link loss) while a kind-7 draw was in
  flight left the walker's draw mark set. The answer arrived in `W_OFF` unread,
  and the next walk waited forever: a seeded walk in `W_IVAL`, an unseeded one in
  `W_ADDR`'s draw arm (named in round 2, `8382cf6`). From then on no PortOperational! reached
  ReserveAddress!, so there was no PROBE and no claim until reset (Table B.7,
  PortOperational! from INITIAL; B.3.5.9). U17b drops the link at four
  consecutive cycles of the redraw loop and requires every re-engage to probe.
  Before the fix it failed phases 1 to 3 and U18 behind the wedge (6 FAIL of 89).
  The `W_ADDR` exit now clears the mark.
- Mutants `fit-compare-forced-true` (the compare the issue cites at `:587`;
  `:644` at the round-3 head, `:594` at round 1), `fit-compare-off-by-one`,
  `seed-clamp-removed` and `release-keeps-draw-mark` are all KILLED.

## 2. #67: maap_version 0 and 2 through the real RX validator (B.2.3.2, B.2.3.4, Tables B.1/B.10; REQ-MAAP-002)

- `tb/rx_validator` F29 (F28 until the round-3 merge of `main`, whose own F28
  grades the AECP hold): PROBEs with maap_version 2, 0 and 31 (31 sets all five
  bits of the lane) are each accepted, committed, demuxed to `PP_PROTO_MAAP`, and
  deliver the received version in the status lane. The hdr beat is compared field
  by field.
- `tb/pp_top` MP7: a conflicting maap_version-2 PROBE, then a maap_version-0
  PROBE, against the DEFEND-state claim crosses the real validator and dispatch.
  Each is answered by a byte-exact unicast DEFEND carrying our version 1 and the
  B.3.6.6 overlap, and the claim is kept.
- Mutant `validator-maap-version-1-only` (a `maap_version == 1` acceptance rule
  added to the validator) turns both suites red. Round 1: F28, 47 FAIL of 453;
  MP7, 4 FAIL of 33. Round 3: F29, 47 of 497; MP7, 4 of 34.
- No RTL change was needed.

## 3. #68: the Table B.7 conflict walk with a discriminating compare_MAC (B.3.5.5 to B.3.5.7, Table B.7, B.3.6.4; REQ-MAAP-005)

- Every tie-break scenario now uses a peer whose forward and octet-reversed orders
  against our MAC disagree, and checks that premise. `00:11:22:33:44:FF` is
  forward-lower but reversed-higher (we win). `F2:11:22:33:44:01` is
  forward-higher but reversed-lower (we lose).

  | Cell | We win | We lose |
  |---|---|---|
  | PROBE / rProbe! | U9: the walk continues | U19 (new): yield, fresh range |
  | DEFEND / rAnnounce! | U7: the claim stands | U8: yield, fresh 4-probe walk |
  | DEFEND / rDefend! | U20 (new): the claim stands, nothing sent | U21 (new): yield, fresh range |

- U22 (new): PROBE / rAnnounce! from a peer we beat in both orders still yields
  (no tie-break).
- `tb/pp_top` MP4's winner is now `F2:11:22:33:44:01`: reversed-lower, and
  forward-higher than the bench's `0A:0B:0C:0D:0E:0F`.
- Mutant `compare-mac-forward` (`cmp_mac_true_w = own_mac_i < rxm_sa_r`) turns
  `tb/maap` red (9 FAIL) and MP4 red (5 FAIL). One arm per new cell
  (`probe-rprobe-never-yields`, `defend-rdefend-ignored`,
  `defend-rdefend-no-tiebreak`, `probe-rannounce-tiebreak`) and
  `yield-reuses-range` are also KILLED.
- `tb/maap/README.md` now carries the mutation ledger, in the SRP suites' form.
- No RTL change was needed.

## Mutation campaign

`make -C tb/maap mutants` plants each reviewed patch in `tb/maap/mutations/` into a
scratch copy of `hdl/` with `git apply`. Controls run first. Each arm must finish
its simulation red with its own named check, and a build failure or a missing
tally never counts as a kill. The driver reads only simulation logs. pp_top arms
use the new `make -C tb/pp_top maap-internal` (the MP section alone). The HDL
workflow runs the campaign next to the SRP one. At round 1's head: 3 controls
PASS and 13 of 13 arm runs KILLED (29 of 29 at the round-3 head).

## Validation (processor, head `b03d36f`)

- `./scripts/run_suites.sh`: rc 0, 33 suites, 1,015,919 checks, 0 failing (base:
  1,015,815). maap 75 to 114, rx_validator 393 to 453, pp_top 7,751 to 7,756.
- `./scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check`,
  `git diff --check c951a9ff HEAD`: rc 0.
- `make -C tb/maap mutants`: rc 0, 16 of 16.
- `make -C tb/srp_top mutants`: 56 of 56 KILLED, assertion coverage 49/49, run
  in batches.
- `make -C tb/nvm_port figures`: rc 0.
- `syn/yosys/run.sh`: rc 0.
- pp_top `gsi-internal`, `name-writes` and `maap-internal`: rc 0.

The SRP campaign, the NVM figures, Yosys and the pp_top `gsi-internal` and
`name-writes` runs were at `3407c84`. `b03d36f` changes only one rx_validator test
file, which none of them reads. `maap-internal` ran at the head, inside the MAAP
campaign.

## Parent consumer gates

Run in a scratch parent at milan-fpga dev `13eda870`, with the gitlink at
`b03d36f`. It was the 15 identifiable consumer commands, plus both candidates for
the sixteenth (`protocol-processor/scripts/check-integrator-params.py`,
`scripts/lint_rtl.py --check`).

- All rc 0: the nine script gates (C++ and Python idiom, xvlog, RTL source lists,
  `pp_srcs`, port contracts, naming, test evidence, docs), `pp_shadow` (2,120
  checks), `nvm_cosim` lint and quick (315/315), `milan_dp_render` (152/152, 65/65,
  5/5), and both candidates.
- `test_builder --require-elaboration --require-rv32`: rc 0, with its one
  recorded NOT RUN arm (gate 11: the placement report is absent on the host).
- `milan_dp`: rc 0. Every leg passes (gptp, gptp-lat, gmstep, main, notify,
  crflic, nxn, nxndv, nxn8, nxn4c, nolpf, prune, ax1x1, aclk), and the render
  and gmstep mutation campaigns are 6/6 each.

The C++ rule-11 gate first counted one multi-declarator declaration in the new F28
test (F29 since round 3). `b03d36f` fixes it, and the gate is back at 0 <= 0.

## Parent-visible for pin adoption

1. No port, parameter or interface change.
2. The `KL_pp_maap` fix acts only with `cfg_maap_internal_i = 1`. The parent ties
   it to 0 (`hdl/milan/milan_datapath.sv:7769` at dev `ec0cc0c1`; `:7695` at
   round 1's `13eda870`), so the shipping fabric is unchanged.
3. Optional: `scripts/measure_test_evidence.py --check` passes with 74 <= 77
   unarmed suites (75 <= 77 at the base pin), because `tb/maap` is now armed by
   its `mutants` driver. The budget could be lowered to 74. No disposition row is
   needed: 0 unexplained readers, and no host time.
4. New entry points: `make -C tb/maap mutants`, `make -C tb/pp_top maap-internal`.

## What remains (round 1, rewritten in round 3)

Round 1 listed two corners of the Release! arc here as outside its scope. Round 2
resolved both, as its section below states, so neither remains:

- **The footnote-a seed on the `W_ADDR` exit.** Every Release! re-arms the seed,
  including one that lands while generate_address redraws (`8ae76ee`: `W_OFF`
  clears `seed_used_r`, `KL_pp_maap.sv:604`; U27).
- **A frame being drawn or built when the engage falls.** A frame still being
  drawn has no TX slot yet, and is dropped whole with its entry (U17c, U23,
  U28). A frame whose TX slot was requested before the fall belongs to the entry
  that requested it, and may drain as that entry's last act. No PDU is generated
  after the fall (Table B.7 Release! row, B.3.2, B.3.5.2; the ruling, #66 comment
  5890772857). Footnote c says the range becomes free. It does not say that a PDU
  an earlier entry already produced is withdrawn.

What still remains is listed in the Round 3 section.

## Round 2 ([A445]): R400-1 and R401-1

Head `053f979`, nine commits on `b03d36f`. Both round-1 reviews were NEGATIVE:
R400-1 had four MINORs, and R401-1 had one MINOR and three suggestions. This
round resolves them as below.

The round first stopped at `ea79d8b`: a frame whose TX slot was requested before
the fall still left after it, and recalling it would need a processor port
change. The manager ruled that such a frame may drain (option 2: no cancel path,
no port change), and set three points for R400-1 F1. The last three commits
close them. No RTL logic changed after the ruling.

### The Release! rule (IEEE 1722-2016 Table B.7, B.3.1 c) and e), B.3.2, B.3.5.2, B.3.5.9, footnotes a and c)

Table B.7's Release! row stops probe_timer (PROBE) or announce_timer (DEFEND)
and returns to INITIAL. No Release! cell carries sProbe, sAnnounce or sDefend,
and a stopped timer does not expire. B.3.2 executes each state table entry
sequentially. The walker executes an entry over many cycles, so a Release! that
lands mid-entry is ordered by that entry's TX slot request:

- **Before the request.** The Release! comes first and the entry is dropped whole:
  no timer, no frame, no state change. This holds in every walker state that runs
  before the request, and for a fall of a single cycle.
- **From the request on.** The frame belongs to the entry that requested it, and
  it drains as that entry's last act. It is the only frame that can: no new slot
  request follows the fall (a request already pending is retried until granted;
  round 3 wording, R400-2-S1). The top's pool-access arbiter holds the builder as
  owner until it commits, and `KL_pp_tx_slots` frees a committed slot only by
  sending it. The Release! does not wait for the frame:
  - the claim is withdrawn at the fall;
  - the entry's state change is dropped, so no claim is published after the fall;
  - the Release! is latched, so a rise that lands before the lane takes the frame
    still gives INITIAL and a fresh walk.
- **The drain window** runs from the slot request to the lane grant: 63 cycles
  when the pool and the lane grant at once, longer in the top, and unbounded
  while the egress stalls.
- **Begin!/PortOperational!** is the engage level as the released machine sees
  it, so a rise during the teardown or a drain is never lost.
- **Every Release! re-arms the footnote-a seed.** Within an engagement the seed
  is probed once and a conflict is never answered with it again.

`docs/architecture/11_maap_engine.md` §6 and the `KL_pp_maap.sv` banner state
this rule. They cite Table B.7, B.3.2 and B.3.5.2 for the ordering and say "no PDU
generated after the fall". REQ-MAAP-007 and `tb/maap/README.md` say the same.

### Per finding

| Finding | Commit | Change | Clause | Failing arm |
|---|---|---|---|---|
| R400-1 F1 (R401-1 F2 and F3 folded in) | `4de2c60` | `W_IVAL`, `W_RX` and `W_POST` honour a fall; the TX states withdraw the claim and latch the Release!; `W_OFF` starts on the engage level | Table B.7 Release!/PortOperational!, B.3.2, B.3.5.2, B.3.5.9 | U23 to U26 fail 13 checks against the start head's RTL. Arms `ival-sends-after-release`, `post-publishes-after-release`, `tx-path-absorbs-release`, `off-waits-for-an-edge`, `rx-release-returns-to-idle`: all KILLED |
| R400-1 F1, ruling point 1 | `d0acc9b` | U28: 17 falls, landed so the walker first sees each in a chosen state, cover all 12 walker states. For 33 s after each: no new TX slot request, no timer started, no timer expiry, no claim, INITIAL; at most the one frame requested by then drains | Table B.7 Release!, B.3.1 c) and e), B.3.2 | New arms `idle-serves-a-latched-expiry-first` and `teardown-keeps-announce-timer`, both KILLED on U28. U28 fails 4 checks against the start head's RTL |
| R400-1 F1, ruling point 2 | `4f6affc` | U23's drained arm: exactly one slot request (the ANNOUNCE's), byte-exact, on the lane within 63 cycles of the fall at each of 75 offsets (measured maximum 63) | B.3.2, Table B.7 Release! | New arm `drain-waits-for-the-link` KILLED on U23 (drain and window) |
| R400-1 F1, ruling point 3 | `053f979` | `11` §6 and the banner cite Table B.7, B.3.2 and B.3.5.2, and say "no PDU generated after the fall" | Table B.7, B.3.2, B.3.5.2 | (docs) |
| R400-1 F2 + R401-1 F1 | `8ae76ee` | `W_OFF`, which every Release! reaches, re-arms the seed | Table B.7 footnote a | U27 fails the `W_ADDR` arc at the start head. Arm `seed-rearmed-on-idle-release-only` KILLED |
| R400-1 F3 | `fa21c58` | U18b: seed `0xFDF9` clamped to `0xFDF8`; `0xFDF8` and `0xFDF7` taken as given; byte-exact, no draw | B.1, Table B.9, footnote a | Arm `seed-clamp-off-by-one` KILLED; the reviewer's own patch is killed too |
| R400-1 F4 | `2c11d6f` | U17c: Release! during a draw that fits: nothing sent, the draw is never adopted, the next engage probes | Table B.7 Release!, B.3.5.9 | Arm `release-waits-for-draw` KILLED; the reviewer's own patch is killed too |
| R401-1 F4 (suggestion) | `8382cf6` | The comment and README name both stalled states: `W_ADDR` for an unseeded walk, `W_IVAL` for a seeded one | (docs) | none needed |

`ea79d8b` only reorders the scenarios, so U19 to U22 still end the suite, as the
reviewers' probe scripts expect. R400-1 S1 and S2 are retained: they are not in
the round-2 assignment.

**The reviewers' probes at `053f979`.** R400's P1, P1c, P3, P4 and P5 pass, and
P2's claim part passes (0 of 160 offsets). P2's PDU part counts 64 of 160
offsets. Classified in P2's own slot, each of the 64 is the ANNOUNCE whose slot
was requested by the first cycle the fall is seen: no offset has a slot request
after it, and the latest lane request comes 63 cycles after the fall. R401's P1
and P2 pass. Its P3 frame is the first PROBE, which was already being written
when the fall was seen, with no slot request after it. Both are the drain the
ruling accepts; the probes' literal checks still count them.

### Parent-visible for pin adoption (round 2)

1. No port, parameter or interface change. The Release! change acts only with
   `cfg_maap_internal_i = 1`, which the parent ties to 0.
2. The unit wrapper `tb/maap/maap_wrap.sv` reads the walker state through one
   hierarchical reference. The parent's port-contract inventory of test-only
   hierarchical observations goes from 133 to 134; it is not a ratchet, and the
   gate passes.
3. Tallies: `tb/maap` goes from 114 to 191 checks, and `run_suites.sh` from
   1,015,919 to 1,015,996. The MAAP campaign is now 3 controls plus 24 arms
   (27 checks).
4. REQ-MAAP-007's wording changed in `docs/00_MILAN_COMPLIANCE_REVIEW.md`; the
   parent's compliance matrix does not quote it.
5. Unchanged: the test-evidence ratchet can still be lowered to 74, and the entry
   points are the same.

### Validation (round 2, head `053f979`)

- **Processor:**
  - `./scripts/run_suites.sh` rc 0 (33 suites, 1,015,996 checks);
  - `./scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check` and
    `git diff --check` all rc 0;
  - `make -C tb/maap mutants`: 27/27;
  - `make -C tb/srp_top mutants`: 56/56 KILLED, coverage 49/49, in batches;
  - `make -C tb/nvm_port figures`, `syn/yosys/run.sh`, and pp_top
    `maap-internal`, `gsi-internal` and `name-writes`: all rc 0.
- **Reviewers' round-1 scripts** at the new head, on the reviewers' Verilator
  5.050: head suites green, the campaign 27/27, both of R401's own mutants
  KILLED, 4 of 5 of R400's mutants KILLED (S1's survives), and the probes as
  above.
- **Parent consumer gates** in a scratch parent at milan-fpga dev `9e3ccbfb`,
  gitlink at `053f979`: see the table below.

| Parent consumer command (scratch parent, dev `9e3ccbfb`, gitlink `053f979`) | rc | Result |
|---|---|---|
| `scripts/check_cpp_idiom.py`, `check_py_idiom.py`, `docs_check.py` | 0, 0, 0 | within budget; 0 findings |
| `scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, as at round 1 |
| `scripts/check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 | OK |
| `scripts/check_port_contracts.py` | 0 | processor 111 <= 111 undocumented, no port added |
| `scripts/measure_naming.py --check` | 0 | 96 recorded |
| `scripts/measure_test_evidence.py --check` | 0 | 74 <= 77; can be lowered to 74 |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | all gates pass except gate 11 NOT RUN (placement report absent on the host, as at round 1) |
| `make -C tb/verilator/pp_shadow` | 0 | 2,120 checks, no PINMISSING |
| `make -C tb/verilator/nvm_cosim lint` / `quick` | 0 / 0 | 84 non-fatal warnings / 315/315 |
| `make -C tb/verilator/milan_dp` | 0 | every leg PASS (gptp 181 ... aclk 190); render and gmstep controls 6/6 each |
| `make -C tb/verilator/milan_dp_render` | 0 | 152/152, 65/65, 5/5 |
| `protocol-processor/scripts/check-integrator-params.py`, `scripts/lint_rtl.py --check` | 0, 0 | 24/24/24; 90 <= 90 |

## Round 3 ([A452]): the merge of `main`, R400-2 and R401-2

Head `921fff5`, three commits on `053f979`: the merge of processor `main`
`b2db3a97` (PRs #132 and #133), then one commit per finding. R401-2 was POSITIVE.
R400-2 was NEGATIVE on two MINORs: F1 (tests) and F2 (this body). This round
resolves both and takes R400-2's suggestion S1. Apart from what the merge brings,
there is no RTL change and no port change.

### The merge (`c842670`)

A merge commit with parents `053f979` and `b2db3a97`; no rebase. Main brings 31
commits. Three files conflicted, and each keeps both sides' checks:

- **`tb/pp_top/sim_main.cpp`.** Both sides' focused modes are kept: this lane's
  `--maap-internal-only` (the MP section alone), and main's `--d3-only` and
  `--dr3a`. Each focused mode skips every other section. The default run is
  main's: every section, with MP and D3.
- **`tb/rx_validator/sim_main.cpp` and its README.** Both sides added a section
  named F28. Main's F28 (the AECP hold admission) keeps its name, which main's
  `docs/architecture/09_verification.md` and `tb/pp_top/d3_mutants.py` already
  use. This lane's maap_version section becomes **F29** (F29a to F29c), and its
  mutation row becomes M5. The suite has 497 checks.

The same commit carries what the merge moves:

- The MAAP campaign's rx_validator arm now names F29.
- Its patch is re-anchored on the merged validator, because main moved
  `ver_fail_w`. The planted edit is the same.
- Main's MP0 (the D3 restore before AECP) makes the MP section 34 checks. The
  READMEs say so.

At the merge head every suite passes: 33 suites, 1,016,453 checks. That covers
this lane's sections (`tb/maap` 191, rx_validator F29, pp_top MP), #132's (pp_top
D3, rx_validator F28) and C1's (`tb/srp_top` 2,200).

### Per finding

| Finding | Commit | Change | Clause | Failing arm |
|---|---|---|---|---|
| R400-2-F1 (MINOR, tests) | `f7b67ce` | U29: 20 one-cycle falls (the link down for exactly one edge), each first seen in a named state of an entry: `W_IVAL`, `W_ALLOC`, `W_GWAIT`, `W_WRITE`, `W_COMMIT`, `W_LANE` and `W_POST`. They land in a mid-walk PROBE, an sDefend and a DEFEND re-announce (sDefend has no `W_IVAL`). Each must give INITIAL, no claim until the fresh walk claims, at most the entry's own frame drained, and a fresh walk: 4 byte-exact PROBEs of one range, then its ANNOUNCE. `11` §6's "however short" now names U26 and U29 | Table B.7 Release! and PortOperational!, B.3.2, B.3.5.2 | New arms `tx-set-omits-alloc`, `-gwait` and `-commit` (byte-identical to R400-2's patches), plus `-write` and `-lane`: each KILLED on U29, where 3 of 20 falls are absorbed (one per entry). Against the round-1 RTL, U29 absorbs 20 of 20 |
| R400-2-F2 (MINOR, docs) | (this body) | "What remains" rewritten to match round 2 and the ruling. Round-1 line references refreshed, with the round-1 line kept in parentheses; round-1 tallies marked | the ruling (#66 comment 5890772857): Table B.7 Release!, B.3.2, B.3.5.2, footnote c | none (docs) |
| R400-2-S1 (SUGGESTION, taken) | `921fff5` | "no new slot request" (a request already pending is retried until granted) in U28's check and comment, U23's check and comment, `tb/maap/README.md`, and this body's Round 2 section | Table B.7 Release!, B.3.2 | none (wording) |

### Suggestions retained, with the reason

- **R401-2 S1 (a)**, the timers during a drain. It is not in the round-3
  assignment. The normative `11` §6 and the banner already say that the timers
  stop once the lane has the frame, and that an expiry meanwhile meets INITIAL.
  U28's wording is true in the unit bench, where the lane grants at once. Its
  part (b) is R400-2-S1, taken.
- **R401-2 S2**, a stalled-drain expiry arm. It is not in the round-3
  assignment, and R401-2 found no surviving mutant for it.
- **R401-2 S3.** Its first half (mark "What remains") is R400-2-F2, done. The
  comment re-flow at `KL_pp_maap.sv:619-623` is retained: this round changes no
  file under `hdl/`.
- **R400-1 S1 and S2.** Not in the round-3 assignment, as in round 2.

### Parent-visible for pin adoption (round 3, re-read at the merged head)

This lane, rounds 1 to 3 against `c951a9ff`:

1. **No port, parameter or interface change** by this lane. The MAAP engine acts
   only with `cfg_maap_internal_i = 1`, which the parent ties to 0
   (`hdl/milan/milan_datapath.sv:7769` at dev `ec0cc0c1`). Round 3 changes no
   file under `hdl/`.
2. **One test-only hierarchical observation** (`tb/maap/maap_wrap.sv`
   `walker_o`, round 2). The port-contract gate passes at this head, with an
   inventory of 176 test-only hierarchical observations, main's included.
3. **Tallies:**
   - `tb/maap` 196 (U29 adds 5);
   - `tb/rx_validator` 497 (main's 437 plus this lane's F29);
   - `tb/pp_top` 7,893, with MP at 34 (main's MP0);
   - `run_suites.sh` 1,016,458;
   - the MAAP campaign 32 checks (3 controls and 29 arms).

   No parent file pins these counts or cites `tb/maap`, `maap-internal`, or the
   rx_validator section names. The test-evidence ratchet can still be lowered to
   74.
4. **Docs:** REQ-MAAP-007's wording (round 2), and `11` §6's "however short",
   which now names U26 and U29. The parent's `MILAN_COMPLIANCE_MATRIX.md` has
   no MAAP row.

What the merge brings. These are not this lane's changes; they reach this head
through `main` `b2db3a97`:

5. **PR #132's consolidated list** ("Parent-visible for pin adoption: rounds 1-6,
   consolidated", in PR #132's description):
   - the D3 top outputs and parameters, and snapshot word 37;
   - AECP held from reset to the D3 terminal;
   - the firmware's `PP_CTRL[1]` obligations;
   - its parent-harness edits (`milan_dp`, `milan_dp_render` T8, `pp_shadow`,
     `nvm_cosim`);
   - the evidence classifier's `d3_mutants.py` disposition.
6. **C1's section 4** (PR #133's "Parent-visible, for the pin-adoption lane", as
   its Round 2 amends it):
   - the licence's Milan 4.3.2 term, with its VLAN-table overflow and egress
     ordering;
   - fewer own LeaveAlls;
   - the crflic re-base (`sim_crf_licence.cpp:953,956`, `>= 3`);
   - the parent documents to update.

   PR #133's composed-head note says that the adoption lane edits
   `tb/verilator/milan_dp/README.md` once for both lists.
7. **The manager's combined parent adaptation** for 5 and 6 (13 files, sha256
   `2ba66803…ddc420`) applies cleanly at dev `ec0cc0c1`. The consumer bank below
   ran with it. The parent documents in 5 and 6 are not in it.
8. **The merge resolution adds nothing parent-visible:** it changes processor
   tests and their READMEs only.

### Validation (round 3, head `921fff5`)

Verilator 5.052, with every build capped at 8 jobs and run one at a time.

- **Processor, at `921fff5`:**
  - `./scripts/run_suites.sh`: rc 0, 33 suites, 1,016,458 checks;
  - `./scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check`,
    and `git diff --check` against `c951a9ff`, `053f979b` and `b2db3a97`: all
    rc 0;
  - `make -C tb/maap mutants`: 32/32 (3 controls, 29 of 29 arms KILLED);
  - C1's `make -C tb/srp_top mutants`: 90/90 (78 arm runs KILLED, assertion
    coverage 65/65), in one run;
  - #132's `tb/pp_top/d3_mutants.py`: 83 of 83 KILLED, goldens PASS;
  - `tb/pp_top/gsi_mutants.py` (20 detected) and `name_wr_mutant.py`: rc 0;
  - `make -C tb/nvm_port figures` and `syn/yosys/run.sh`: rc 0;
  - pp_top `maap-internal` 34, `gsi-internal` 6,182 and `name-writes` 85: rc 0.
- **At the merge `c842670`:** every suite passes, 33 suites and 1,016,453
  checks. The campaign's two cross-suite arms are KILLED there too.
- **Parent consumer set, the manager's sixteen commands.** It ran in a scratch
  parent at milan-fpga dev `ec0cc0c1` (a `git archive` of the trusted checkout;
  the tree differs from `ec0cc0c1` only in the gitlink). The gitlink is at
  `921fff5`, and the manager's combined #132 + C1 adaptation is applied with
  `git apply`.

| Parent consumer command | rc | Result |
|---|---|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet within budget |
| `python3 scripts/check_py_idiom.py` | 0 | every ratchet within budget |
| `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet (0 in `hdl/`) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 107 files, 4 of 4 lists; processor 36/42 tops, 6 recorded |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| `python3 sw/builder/test_builder.py` | 0 | all gates pass except gate 11 NOT RUN (the placement report is not on the host, as in rounds 1 and 2) |
| `make -C tb/verilator/pp_shadow -j8` | 0 | 595 + 635 + 595 + 295 checks, 0 failures, 0 PINMISSING |
| `python3 scripts/check_port_contracts.py` | 0 | processor 1,747 ports, 111 <= 111 undocumented; 176 test-only hierarchical observations |
| `python3 scripts/measure_naming.py --check` | 0 | 96 recorded |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 74 <= 77; can be lowered to 74 |
| `python3 scripts/docs_check.py` | 0 | 0 findings |
| `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| `make -C tb/verilator/nvm_cosim lint` | 0 | 85 warnings, none fatal, 0 PINMISSING |
| `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| `make -C tb/verilator/milan_dp -j8` | 0 | every leg PASS: gptp 181, gptp-lat 181, gmstep 103, main 234, notify 378, crflic 415 (3 DUT and 3 switch LeaveAll MRPDUs), nxn 1,841, nxndv 1,843, nxn8 3,521, nxn4c 1,841, nolpf 234, prune 33, ax1x1 231, aclk 190; 30 `[AECP-WTMO]` passes; render and gmstep mutation controls 6/6 each |
| `make -C tb/verilator/milan_dp_render -j8` | 0 | 65/65, 152/152, 5/5 |

16 of 16 rc 0.

### What remains (round 3)

- The manager's duties:
  - the hosted checks at `921fff5`;
  - the donor bank;
  - the official parent consumer bank.
- The delta reviews, which judge the merge and the findings together.
- Retained suggestions, as listed above.
- Pin adoption: the parent-visible list above, with PR #132's consolidated list
  and C1's section 4.
