# [A661] processor #193: one declaring applicant per StreamID

## Round 2 (PR #198, answering R679-1 and R680-1)

**Status: DONE, REVIEW READY at head `7b424cdfe111a426f00517ff471246b4b9650726`** (local
branch; not pushed; started 2026-10-20 21:52 CEST, done 2026-10-21 09:45 CEST). Every gate and
campaign is rc 0 at base and head, except the parent's `check_submodule_docs`, which fails
identically at both (as in round 1b). Assignment: the newest [A10] comment on PR #198 (issuecomment-6300041102), read in full
with R679-1 (issuecomment-6300027310) and R680-1 (issuecomment-6299632354). The reviewers'
probes were taken from their archived packets.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (origin confirmed before
  the first commit of this round; HEAD was then 6ddfcda4).
- Branch `193-shared-listener-leave`, fetched and fast-forwarded to the PR head (`git pull
  --ff-only`: already up to date). New commits on it; no rebase, no amend, no push.
- Base of this round: `6ddfcda4c3170b8f463c8623833f7541ca8c1faf` (the PR head: round 1b's
  788425db with processor main 08023123 merged by the manager).
- Head: `7b424cdfe111a426f00517ff471246b4b9650726`. Five commits, one-line subjects, no
  body, no trailers:
  1. `e38c535` Cite 35.1.2.2 and Table 35-14 for the Listener type sum in the two
     shared-stream test comments and drop their check labels (issue #193)
  2. `acd65be` Keep a parked Listener applicant in the group of the stream_id it holds, so a
     sink declaring that stream takes it over instead of sending New beside its Lv (issue #193)
  3. `c7c8825` Check a parked Listener Leave meeting a sink on its stream, per tick and
     byte-exact on the wire with a peer Registrar, each with a planted control (issue #193)
  4. `57fb7dd` Write the Listener leave copies kept for the settle's compares with one enable
     per sink, not at a variable index of the packed array (issue #193). The first form
     (`lcp_r[ctl_sink_i] <= csid_w`) synthesized as a shifter: +2,251 LUTs for the listener
     alone at 8 sinks, against +322 with one enable per sink (section R2.5). Behaviour is
     unchanged; every record below is at 57fb7dd, the records at c7c8825 were set aside
     (section R2.6).
  5. `7b424cd` Count the new parked-Leave checks in the failing totals of three shared-stream
     controls in the srp_top README (issue #193). Only `tb/srp_top/README.md` changes (the
     counts of `listener-rider-not-quiet`, `-withdraw-ignores-riders` and
     `-teardown-keeps-declaring`, from the head campaign); the records at 57fb7dd stand for
     every gate that does not read it, and the gates that do (`lint_hdl`, `gen_matrix --check`,
     `make check`, and the parent's text gates) were run again at 7b424cd: all identical
     (`receipts/round2/gates/final/`, `consumers/final/`, `compare/final-vs-head-gates/`).
- STOP conditions: none hit. No port, parameter or register-map change: the RTL edit is
  inside `KL_srp_listener_fsm` (internal registers, a generate block and logic; its port
  list and parameters are unchanged).

### R2.1 Item 1 (R679-1-F1 / R680-1-F1): the parked applicant joins its value's group

The defect: a sink alone on a stream re-binds away and parks its owed Leave (#188); another
sink settles on that stream and declares it before the next tx!. The parked applicant was in
no group (`mbr_w` excluded parked sinks, `same_w` compared matcher stream_ids only), so the new
sink created a second applicant for the value, and one MRPDU carried New and Lv for it.

The fix keeps one applicant per value across its live and parked copies (IEEE 802.1Q-2018
10.7.7; the 35.2.6 NOTE; 35.1.2.2). A group is now the sinks whose applicant is for one
stream_id, where a parked sink counts by its leave copy, not by its matcher:

- A sink that settles on a parked stream_id (or whose own park clears while it is settled
  there) is in the parked applicant's group as a rider: VO, quiet.
- The group's first declaration takes the parked applicant over through the existing
  handover (`op_mv_w` with New!): LA (or LO) + New! = VN in the owner's slot, as the #188
  same-stream re-probe rule does for one sink. The parked slot is released (its park ends),
  so the parker's own request for its new stream is granted. No Lv goes out beside the new
  declaration, and a Milan v1.2 4.2.7.2.2 peer registrar stays IN.
- While no sink on the value declares, nothing changes: the owed Lv (or s) goes out once
  from the parked slot (#188 unchanged). When it has gone out in a walk, the sinks on the
  value get the walk mark, so a declaration later in that walk waits for the next tx!.

| File:line (head) | Change | Clause |
|---|---|---|
| `hdl/srp/KL_srp_listener_fsm.sv:103-114` | banner: the parked case, and a handover to a slot already walked waits for the next tx! | 802.1Q-2018 10.7.7, 35.2.6 NOTE, 35.1.2.2; Milan v1.2 4.2.7.2.2 |
| `:417-422` | `lq_r` (leave copy of p equals matcher of t) and `lcp_w` (the leave copies, for compares) | 10.7.7 |
| `:550-563, 565` | `owner_map` comment; `lcset_w` (settle stream_id against each leave copy) | 10.7.7 |
| `:587, 590-609` | `mbr_w` is every recorded sink; `same_w` pairs a parked sink by `lq_r`, others by `eq_r` | 10.7.7 |
| `:821-838` | `g_lcp_flops`: the leave copies in flip-flops (from two sinks), written with the leave copy, one enable per sink | 10.7.7 |
| `:871, 942-954` | reset of `lq_r`; a settle writes its column of `lq_r` from `lcset_w`, a park writes its row from the old `eq_r` pairs | 10.7.7 |
| `:989-996` | a park retired by its tx! gives the walk mark to the sinks on the held value | 10.7.7 (one tx! per applicant per walk) |
| `:1037-1038` | the handover's giver, when parked, owes nothing more (its park ends) | 35.1.2.2 (no Lv for a stream still wanted) |

Docs: `docs/architecture/10_srp_engine.md:214-215` (§5.1 rows), `:249-252` (cost note),
`:644-645` (a handover to a slot already walked), `:648-660` (bullet "A parked Leave"),
`:668-671` (the leave-copy pairs). Tests: section R2.3.

R679-1's `scripts/run_probes.sh`, unchanged but for one anchor of its wire probe (the comment
line it anchors on lost its `SW3: ` prefix under item 3; `receipts/round2/probes/r679/
anchor-adaptation.diff`), on 57fb7dd (`receipts/round2/probes/r679-head/`; its RTL and tests
are those of the final head): rc 0 (`fsm.rc`, `wire.rc` 0), no `FAIL: PR`
or `FAIL: PW` line; every variant (parker 1 or 0, with or without the A8) sends one value per
tick ('0/2', '0/2', '3/2'), no Lv while the joiner declares, and the peer is IN before and after
with 0 deregistrations and 0 Lv. The same probes, unadapted, at the base 6ddfcda4: PR1-PR4 and
PW1-PW2 fail as R679-1 recorded (`receipts/round2/probes/r679-base/`). R680-1's
`run-parked-probe.py` and `run-parked-wire-probe.py`, with only the revision guard set to
57fb7dd and the build parallelism lowered to the lane's limit
(`receipts/round2/probes/r680/revision-guard-adaptation.diff`): 2 of 2 PASS each, count 1,
leaves 0, peer IN.

### R2.2 Items 2-4

- **Item 2 (F2):** PR-BODY.md (Round 2 section and the Behaviour paragraph) now gives the
  area figure with its shape, the module defaults (8 Stream Inputs, 8 Stream Outputs), says no
  1x1 figure was measured here, and that the 4th pin adoption's route-1x1 measures the shipped
  cost. The figures are re-measured at this round's pins (section R2.5).
- **Item 3 (F4, F3):** `tb/srp_stream_fsms/sim_main.cpp:1792-1796` and
  `tb/srp_top/sim_main.cpp:3170-3173` cite 802.1Q-2018 35.1.2.2 and 35.2.4.4.3, Table 35-14 for
  the type sum and keep 35.2.6 for the change in place. `tb/srp_top/sim_main.cpp:3000` is the
  plain heading R680-1-F3 gave, and the `SW3: ` prefix is gone (commit 1).
- **Item 4 (R679-1-S2):** probed (`receipts/round2/probes/s2/`, the probe source
  `probe-s2.cpp` beside its log). (a) Sink 5 holds the applicant (AN, its New due), sink 0 a
  rider; sink 0's registration lands at each clock 1-6 of the walk. When it lands after the
  walk passed sink 0 and before sink 5 (clocks 1-4), the applicant moves to sink 0 and gets no
  tx! in that walk: the next tx! sends its New and the one after its JoinMt ('', '0/2',
  '3/2'). Later (clocks 5-6) sink 5's tx! sends the New first and the applicant moves with its
  walk mark ('0/2', '3/2', ''). Never lost, never two. (b) The parked form (sink 7 parked,
  sink 0 a rider), clocks 1-10: before the walk reaches sink 7, the takeover sends nothing in
  that walk and New at the next ('', '0/2'); after it, the Lv has gone and New follows ('5/2',
  '0/2'). (c) The order SH16 does not take: the walk reaches the stream's parked Lv before the
  re-binding sink's own Leave has gone, so no sink declares the stream yet and the Lv goes out,
  New at the next tx! (#188's rule for the re-binding sink). 17 of 17 as described; no
  misbehaviour, so no change. The one-tick delay is now stated in the banner and in 10 §6.4.

Other probes kept, all on 57fb7dd: R680-1's `handover-pairs.cpp`, 12 of 12 PASS
(`receipts/round2/probes/r680/handover-pairs.log`); a parked-group collision probe
(`receipts/round2/probes/parked-pairs/`, 32 of 32): the joiner's registration in one clock
with periodic!, a received Listener LeaveAll and the join tick, both index orders, the join
tick a clock before, with or after: at most one value per tick in every case (a registration
that lands after the walk evaluated the parked slot gives Lv then New, as one applicant's
would); a parked sink re-binding again hands the LA to the joiner, one Lv; the joiner's A8 as a
rider leaves the parked Lv; a declaration withdrawn before tx! gives one Lv; an LO park taken
over gives one New.

### R2.3 New checks, planted controls and failing words

Assignment item 1 asks for SH/SW cases for both index orders and both re-bind forms, each
grading single-value frames and an uninterrupted peer registrar, each with a named KILLED
control:

| Case | Checks |
|---|---|
| parker 1 / joiner 0, the parker's A15 at once | SH10 (per tick), SW4 (wire, byte-exact) |
| parker 0 / joiner 1, A15 at once | SH11, SW5 |
| parker 1 / joiner 0, A8 (withdrawal) then A15 | SH12, SW6 |
| parker 0 / joiner 1, A8 then A15 | SH13, SW7 |
| no sink on the value declares: #188 unchanged (one Lv), the rider answers no LeaveAll | SH14 |
| a declaration after the walk sent the parked Lv waits for the next tx! | SH15 |
| a sink whose own Leave goes first, then declares the parked value ("declares" trigger) | SH16 |

`tb/srp_stream_fsms/sim_main.cpp` (head): `SIDP`/`DAP` :1595-1596, the peer Registrar model
`PeerReg` :1600 (Milan v1.2 4.2.7.2.2: New/JoinIn/JoinMt register, Lv deregisters at once,
fed the pushes in order), `park_the_stream_alone` :1622, SH10-SH13
`a_new_sink_takes_over_a_parked_leave` :1637, SH14 :1680, SH15 :1706, SH16 :1744, calls in
`run()` :1893-1899; expectations from the suite's Table 10-3 model of one applicant. SH10-SH13
also require the parker to declare its new stream (its slot released) and the peer to stay IN
with 0 deregistrations and 0 Lv over three ticks. `tb/srp_top/sim_main.cpp`: SW4-SW7
`check_a_new_sink_takes_over_a_parked_leave` :3121, calls :631-634; byte-exact against the
independent builder's one-value frame, the next three frames one value each, the existing
`PeerRegistrar` (:3023-3047) fed every MSRP frame since the first Advertise: IN before and
after, 0 deregistrations, 0 Lv; the joiner Ready.

Controls (`tb/srp_top/mutations/*.patch`, generated by `receipts/round2/scripts/
make_patches_r2.py` as exact edits of the head RTL; `tb/srp_top/mutants.py:235-244`,
coverage `:338` now SH1-SH16 and SW1-SW7). The words are from the head campaign's receipts
(`receipts/round2/campaigns/head/work/srp_top/`); for a label graded on two suites the
campaign keeps the later receipt, so the earlier suite was run again alone at the head
(`receipts/round2/head-extra/`, marked †):

| Check | Control (edit) | Failing words at the head |
|---|---|---|
| SH10-SH13 | `listener-merge-keeps-park` (the takeover leaves the giver parked) | `FAIL: SH10: sink 1 parks its Leave of the stream (A15), sink 0 settles on it and declares: it takes the parked applicant over, LA + New! = VN, each tx! sends ONE New or JoinMt for it and no Lv, the parker declares its new stream, a peer Registrar never deregisters (parked 1, took 1, one 0 got tx! 1: '0/2' and '', peer IN 1 deregs 0 Lv 0, decl 2/0)`, and the same for SH11-SH13 |
| SH10-SH16 | `listener-parked-outside-groups` (a parked applicant in no group: the behaviour before this round) † | SH10 `... one 0 got tx! 1: '0/2 5/2' and '', peer IN 1 deregs 1 Lv 1, decl 2/2)`; SH11 `'5/2 0/2'`; SH12 `'0/2 5/2'`; SH13 `'5/2 0/2'`; SH14 `(first '4/0 5/2', rider AN, then '0/2')`; SH15 `(this walk '5/2 0/2', the next '0/2', decl 2)`; SH16 `(stream '5/2' then '0/2', own Leave '5/2', peer IN 1 deregs 1, decl 2)` |
| SH10-SH15 | `listener-settle-skips-leave-copies` (a settle never compares with the leave copies) † | the same words as the row above for SH10-SH15 |
| SH14 | (the two rows above) | `FAIL: SH14: a parked Leave while no sink on the stream declares: the next tx! sends its one Lv, Ready, and nothing from the rider after a received LeaveAll; the joiner's later declaration is one New (first '4/0 5/2', rider AN, then '0/2')` |
| SH15 | `listener-retire-skips-group-mark` (the retired park marks only its own slot) | `FAIL: SH15: sink 7 declares the stream after the walk sent its parked Lv: the New waits for the next tx!, one value per tick (this walk '5/2 0/2', the next '0/2', decl 2)` |
| SH16 | `listener-park-drops-matcher-pairs` (a park does not copy its matcher pairs) | `FAIL: SH16: a sink whose own Leave goes first, then declares the stream parked by another sink: it takes the parked applicant over, no Lv for the stream, its New at the next tx! (stream '5/2' then '0/2', own Leave '5/2', peer IN 1 deregs 1, decl 2)` |
| SW4-SW7 | `listener-parked-outside-groups`, `listener-settle-skips-leave-copies` | `FAIL: SW4: sink 1 alone re-binds away (settled at once) and parks its Leave, sink 0 settles on the stream and registers before the next tx!: ONE Listener value for it, New Ready, byte-exact, then one per frame, and a Milan peer Registrar never deregisters it (47 B, 2 values, most 1, peer 1 -> 1, deregs 1, Lv 1, decl 2/2)`, and the same for SW5 (settled at once), SW6 and SW7 (withdrawn first) |

The failing frame of SW4-SW7 under either control is R679-1's 47-byte frame (New and Lv for
one FirstValue). Against the base RTL, with the head's tests, all 7 new stream-FSM checks and
all 4 new wire checks fail (`receipts/round2/newchecks-at-base/`: 1,410 checks, 7 FAIL; 9
checks, 4 FAIL).

Re-anchored: `listener-settle-compare-dropped` (its context line `mbr_w` changed; the edit is
the same, `git diff` of the patch shows only the hunk header and that context line). Every
other listener patch applies unchanged (`git apply --check` on the head).

### R2.4 Base and head records

Base 6ddfcda4 and head 57fb7dd2, each in a clean clone of the lane (no untracked or ignored
file before the run; `tools.txt` in each record). Tools: Verilator 5.050 (the CI pin, through
the lane's shim that turns a build's `-j 0` into `-j 2`), sv2v 0.0.12, Yosys 0.33 for the
processor gates (the CI portability job's package), Yosys 0.66 for the parent gates (the
parent's pin). Each `.rc` is the command's own exit status, written by the runner, never
through a pipe. Normalized base-vs-head diffs (paths, temporary names, timings) are in
`receipts/round2/compare/`.

#### Processor gates

| Gate | Base 6ddfcda4 | Head 57fb7dd2 | Base vs head |
|---|---|---|---|
| `scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,356 checks, 0 failing | rc 0, 1,030,367, 0 failing | only `srp_stream_fsms` 1,403 -> 1,410 (SH10-SH16), `srp_top` 8,665 -> 8,669 (SW4-SW7) and the total |
| `scripts/check-req-tags.py --suites --evidence` | rc 0, 230 evidence lines | rc 0, 230 | identical |
| `scripts/lint_hdl.sh` | rc 0 | rc 0 | identical |
| `make check` | rc 0 | rc 0 | ids 652 -> 657 files (the five new patches); the rest identical |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 | identical |
| `syn/yosys/run.sh` | rc 0 | rc 0 | identical |
| `tb/elab_guards/guards.py --frontend yosys --jobs 2` | rc 0 | rc 0 | identical |

#### Campaigns that build the listener FSM

Every campaign that builds `KL_srp_listener_fsm.sv`: the srp_top campaign and every campaign
that builds the processor top (the same list as round 1b). Drivers at `--jobs 2`; the head's
campaigns ran in two runners (`receipts/round2/scripts/chain_h1.sh`, `chain_h2.sh`).

| Campaign | Base 6ddfcda4 | Head 57fb7dd2 | Base vs head |
|---|---|---|---|
| `tb/srp_top/mutants.py` | rc 0, 196 of 196, coverage 113/113 | rc 0, 203 of 203, coverage 124/124 | 168 arm runs with the same verdict and failing tags; 9 keep their verdict and tags and gain tags of the new checks (`listener-declaration-not-held`, `-park-never-retires`, `-rebind-abandons-leave`, `-rider-not-quiet`, `-settle-compare-dropped`, `-teardown-keeps-declaring` x2, `-withdraw-ignores-riders` x2); 7 new arm runs (5 new patches); no arm loses a tag (`receipts/round2/compare/campaigns/srp_top-arms.csv`) |
| `tb/pp_top/acmp_mutants.py` | rc 0, 65 of 65 KILLED | rc 0, 65 of 65 | identical (sorted, normalized) |
| `tb/pp_top/notify_mutants.py` | rc 0, 135 of 135 | rc 0, 135 of 135 | identical |
| `tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 | rc 0, 110 of 110 | identical |
| `tb/pp_top/aecp_mutants.py` | rc 0, 67 | rc 0, 67 | identical |
| `tb/pp_top/aecp_dispatch_mutants.py` | rc 0, 73 | rc 0, 73 | identical |
| `tb/pp_top/ctr_mutants.py` | rc 0, 18 | rc 0, 18 | identical |
| `tb/pp_top/gsi_mutants.py` | rc 0, 23 detected, golden and restored PASS | rc 0, 23 detected | identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0, killed | rc 0, killed | identical |
| `make -C tb/name_state mutants` | rc 0, 16 KILLED | rc 0, 16 | identical but for the output path |
| `make -C tb/elab_guards mutants` | rc 0, 160 of 160 | rc 0, 160 of 160 | identical after normalizing `all.v:N` (the listener module is longer), but for the output path |

Not run, because they build no changed file (as in round 1b): `tb/maap`, `tb/adp_engine`,
`tb/srp_admission` mutants, `tb/aecp_cmds` controls, `tb/acmp_talker` retry mutants,
`tb/nvm_port` figures.

### R2.5 Scratch-parent consumer gates and area

Scratch parent: a copy of the round-1b scratch clone of kebag-logic/milan-fpga, its `dev`
fetched (still `78ca9bdf104819265588726bce4322696c38b8c2`) and checked out on a local branch,
every submodule updated, then four local commits in this order (never pushed), each the
`git apply` of one patch:
`pp178-a634/parent-evidence-classification.patch` (sha256 76625170...),
`pp176-a629/parent-adoption-milan_dp-67.patch` (e142e2e7...),
`190-a654/parent-scratch-tspec-every-slot.patch` (37d1b76e...),
`pp192-a660/parent-adoption-milan_dp-gsi-g9.patch` (5ed1656c...). All four applied cleanly.
The protocol-processor gitlink was then committed at processor main 08023123 (out-of-context
gates only, the PR's base), at the base 6ddfcda4 and at the head 57fb7dd2, each fetched from
the lane, the submodule clean (`STATE.txt` in each record). Every git command in the
submodule was preceded by a top-level identity check.

| Parent consumer gate | Base 6ddfcda4 | Head 57fb7dd2 | Base vs head |
|---|---|---|---|
| `check_cpp_idiom.py` | 0 | 0 | identical (every ratchet holds) |
| `check_py_idiom.py` | 0 | 0 | line total 259,549 -> 259,559 |
| `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest`, `check_port_contracts.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `docs_check.py`, `check_sh_idiom.py`, `check_hygiene.py --check`, `check_sv_idiom.py`, `check_baremetal_only.py --check`, `check_soc_sources.py`, `check_todo_ownership.py`, `lint_rtl.py --check --self-test --jobs 4`, `behave --no-capture -f plain` (tests/: 406 scenarios) | 0 each | 0 each | identical |
| `check_submodule_docs.py` | 1 | 1 | identical: "protocol-processor: documented pin differs from Git" and the stale submodule diagram, as for any gitlink the parent's docs do not record (as in round 1b) |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 | 0 | |
| `flock <lock> python3 scripts/xvlog_gate.py --check` | 0 | 0 | only the pin line |
| `make -j8 -C tb/verilator/pp_shadow VERILATOR_JOBS=2` | 0 | 0 | 609 + 609 + 649 + 317 checks, 0 failures at both (four binaries interleave their lines) |
| `make -j8 -C tb/verilator/nvm_cosim lint` / `quick JOBS=2 POOL=2` | 0 / 0 | 0 / 0 | identical |
| `make -j8 -C tb/verilator/milan_dp_render VERILATOR_JOBS=2` | 0 | 0 | identical check lines |
| `make -j4 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2` | 0 | 0 | 10,559 `[ok]`, 1,127 `[PASS]`, 0 `[FAIL]` at both; sorted check lines identical |
| `sw/builder/test_builder.py` | 0 | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" at both (gate 11 needs a build tree not on this host) |
| `syn/yosys/ooc.sh --record-rom-digests tcam` (ledger row in the scratch tree, then restored) | 0 | 0 | ROM rows `ltn_rom.hex` 23cc67ee... and `ucode.hex` a7b1af66... at both pins (and at main) |
| `syn/yosys/ooc_selftest.py` | 0 | 0 | 75 arms at both |
| `syn/yosys/ooc.sh KL_pp_shadow` (module defaults: 8 Stream Inputs, 8 Stream Outputs) | 0: LUT 57,266, LUT_TOT 61,502, FF 26,381 | 0: LUT 58,078, LUT_TOT 62,314, FF 26,949 | +812 LUT, +568 FF; LUTRAM 4,236, RAMB36 15, RAMB18 4, DSP 10, CARRY4 2,392 unchanged |

At processor main 08023123 (the PR's base) `ooc.sh KL_pp_shadow` gives LUT 56,743, LUT_TOT
60,979, FF 26,331, so the whole PR costs 1,335 LUTs (2.4 %) and 618 flip-flops at the module
defaults on this parent; of these, round 1b's election is 523 LUTs and 50 flip-flops here
(1,037 and 50 on dev e26f1816 in round 1b: the flattened netlist's mapping varies by some
hundreds of LUTs between parents). No 1x1 figure of `KL_pp_shadow` was measured; the 4th pin
adoption's route-1x1 measures the shipped cost. Not run: the parent's place-and-route
resource gate.

The listener FSM alone (`receipts/round2/area-listener/`: sv2v, then the same
`synth_xilinx -family xc7 -flatten`, Yosys 0.66, `chparam N_SINKS_P`), base 6ddfcda4 -> head
57fb7dd2: 1 sink 2,729 -> 2,798 LUTs, 456 -> 456 FF; 2 sinks 4,354 -> 4,531, 803 -> 933; 3
sinks 4,420 -> 4,635, 962 -> 1,160; 4 sinks 5,672 -> 5,763, 1,246 -> 1,514; 8 sinks 9,428 ->
9,750, 2,395 -> 2,963. At c7c8825 (commit 3, before commit 4) 8 sinks were 11,679 LUTs; with
`listener-settle-skips-leave-copies` applied (no leave-copy compare) 9,557: the shifter of the
variable-index write was the difference, which commit 4 removes.

### R2.6 Run notes

- 21:52 started; read the assignment and both reviews in full; the reviewers' probes taken
  from their archived packets (R679-1 `scripts/`, R680-1 `run-parked-*.py` and `*.cpp`).
- The fix went through a scratch copy of the working tree first: the reviewers' probes, the
  suites, a targeted campaign of the new and re-anchored arms (`receipts/round2/dev/`), the
  S2 and collision probes. Then commits 1-3 (c7c8825).
- Gates and campaigns ran from detached runners (`receipts/round2/scripts/chain*.sh`) in
  clean clones, base and head side by side, each campaign driver at `--jobs 2`; the consumer
  chain waited for the processor gates. A watcher sampled the unit's memory every 10 s,
  trimmed page cache above 8 GB and logged every minute (`receipts/round2/memwatch.log`).
  Anon peaked at 4.9 GB (01:22). MemoryCurrent went over 9 GB once: one logged sample read
  10.1 GB at 22:27 with anon at 0.4 GB, so page cache, and the next read 6.3 GB.
- At 03:05 the head OOC area showed +2,648 LUTs over the base for this round. The listener
  alone, synthesized by sink count and with the mutation patches as probes, put the cost on
  the variable-index write of the compare copy (section R2.5). Commit 4 fixed it. Every head
  record at c7c8825 (gates, campaigns srp_top/acmp/notify, consumer gates, OOC, the extra
  receipts and the probes) was set aside unused (`<scratch>/r2/rec/void-c7c8825f/`, not
  copied here), and all of it was run again at 57fb7dd: the probes with identical results.
- The head chain was restarted at 57fb7dd, then stopped once more a few minutes into its gates
  to split the head campaigns over two runners (the second waited for the base chain). The
  stop first picked the wrong process group, so the old chain started its srp_top campaign
  beside the new one. It was found within a minute and stopped by its own group, its
  partial records were set aside (`void-57fb-restart/`), and the campaign clone was cleaned
  before the new runner used it. The records here are all from the second start.

### R2.7 Output directory (round 2)

- Indexes generated from the files present (path, bytes, sha256) by
  `receipts/round2/scripts/make_index_split.py`: `receipts/INDEX.md` (HANDOFF.md, PR-BODY.md
  and the round indexes) and one `INDEX.md` per round directory. A single index had grown over
  200 KB, so it is split.
- `receipts/round2/`: `repo-record.txt` (base, head, commits, clean tree, sha256 of every
  changed file, remote refs); `scope-ports.txt` (module headers of the listener, the SRP top
  and the processor top identical at base and head; only the listener changed under `hdl/`;
  docs 02 and 07 unchanged); `probes/` (`r679/` the reviewer's scripts with the one adapted
  anchor, `r679-head/` and `r679-base/` their runs, `r680/` the reviewer's scripts with the
  adapted guard and their runs plus `handover-pairs`, `s2/` and `parked-pairs/` the lane's
  probes with their sources); `newchecks-at-base/`; `dev/` (the targeted campaign of the
  pre-commit tree); `gates/{base,head,final}/`; `campaigns/{base,head}/` (each campaign's log,
  rc and seconds; the per-arm receipts of the srp_top and gsi campaigns under `work/`;
  `head/RUNNER.txt` names the head runner of each); `head-extra/` (the dual-suite controls'
  earlier suite, alone, at 57fb7dd); `consumers/{base,head,final}/` with `STATE.txt` each;
  `ooc/{main,base,head}/`; `area-listener/` (the listener alone by sink count, with the
  scripts); `compare/` (normalized base-vs-head diffs and summaries); `scripts/` (every
  runner used); `memwatch.log`; `EXTERNAL-RECORDS.csv` (sha256 and size of the records over
  200 KB kept in scratch). Host roots are replaced by tokens (`<scratch>`, `<lane>`,
  `<reviews>`, `<toolroot>`, `<tools>`, `<management>`, `<home>`, `<data>`, `<tmp>`).
- `receipts/round1b/`, `receipts/round1/`: unchanged but for their generated `INDEX.md`.
- No toolchain, virtualenv, package, tree export or file over 200 KB is in this directory.

### R2.8 Posts

- On issue #193: `[A661] REVIEW READY` with the head 7b424cdf, issue #193 comment 6310615005
  (text in `receipts/round2/review-ready-comment.md`). TAKEN was not posted again.
- No push, no PR edit, no edit of any existing comment.

---

# Round 1b

**Status: DONE, REVIEW READY at head `788425db609204234282ea655be2452649622cba`** (local branch; not pushed, no PR opened). Every gate listed below is rc 0 at base and head, except `check_submodule_docs`, which fails identically at both.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (origin confirmed before
  the first commit, and HEAD was 21601694 then).
- Branch: `193-shared-listener-leave` (local only, never pushed).
- Base: `21601694880efdfc4be3028afa3525fbc8f29c03` (processor main).
- Head: `788425db609204234282ea655be2452649622cba`. Three commits on the base, one-line
  subjects, no body, no trailers:
  1. `2b382b2adef9ada35ddb1b275d66e0ec43b7fef7` Share one declaring Listener applicant among the
     sinks settled on one stream_id, by owner election in the per-sink plane (issue #193)
  2. `67b90c175f4a8ab48dd98c666a13ffa92489dff8` Check one Listener declaration per stream_id, the
     handover and the declared type sum, each with a planted control (issue #193)
  3. `788425db609204234282ea655be2452649622cba` Plant the FailureInformation re-declaration
     control where the shared applicant's New! is decided (issue #193)
- Assignment: the [A10] ruling on #193, comment 6290012163, read in full; the round-1 assignment
  (comment 6289596705) where the ruling does not override it.
- STOP conditions: none hit. No top-level port, parameter or register-map change: every RTL edit
  is inside `KL_srp_listener_fsm` (internal registers and logic; its ports are unchanged).
- Round 1 (the STOP at the measurement) is kept unchanged under `receipts/round1/`.

## 1. The design (ruling items 1-4)

One declaring applicant per StreamID, kept in the existing per-sink applicant slots. Nothing
is added beside the plane except three small per-sink registers and a pair map.

- **Groups.** Sinks whose applicant is for one stream_id form a group: a record, no parked
  Leave, the same matcher stream_id. The pairs come from one 64-bit compare per sink at each
  settle (`cset_w`), kept in an N(N-1)/2-bit map `eq_r`.
- **Owner and riders (item 1).** Each sink keeps its own declared type `dcl_r` (set by the grant
  of its registrar's declaration request, cleared by its withdrawal, A8 or A15). The owner is
  the lowest-index sink of the group with a type. Exactly one member is *active*: the one
  holding a non-VO applicant, else the owner, else the lowest-index member. Every other member
  is *quiet*: VO, it takes no event (received Listener value, LeaveAll, periodic!, tx!) and
  sends nothing.
- **The group operation.** From registered state, the active member applies one operation:
  - New!, when an owner exists and the applicant is not declaring, or declares another type
    than the sum;
  - a move to the owner, when the active member is not the owner, with New! only if the sum
    changed;
  - Lv!, when no member declares and the applicant still declares.
  A request, a teardown or a handover thus takes effect one clock after it is accepted. The
  operation waits out any clock that accepts a settle or teardown.
- **Handover (item 2).** It carries the state, the parameter, the deferred rLA!/periodic! and the
  walk mark. It applies no Lv! and no New! unless the type sum changed. Besides the deferred
  move, an A15 of the sink holding the applicant hands it to another sink whose record holds
  the stream_id (the next declarer, else the lowest-index), instead of parking it. The last
  declarer's withdrawal is Lv!, and the #188 rules (owed Leave, park, settle arms) apply to it
  unchanged.
- **Declared type (item 3).** The sum over the declaring sinks: Ready with AskingFailed is
  ReadyFailed (802.1Q-2018 35.1.2.2 a-c, Table 35-14 in 35.2.4.4.3; the change in place, 35.2.6;
  Milan v1.2 4.2.7). The codes OR (Asking Failed 1, Ready 2, Ready Failed 3).
- **Registrar side and ACMP (item 4).** Unchanged per sink: matcher, registrar, EVT_TK_*,
  `tk_reg_state`, latency and failure latches. `lstn_decl_state` reports the sink's own type
  while its stream's applicant declares, so each sink's GET_RX_STATE is its own.

## 2. Changes (file:line at the head, with the clause)

`hdl/srp/KL_srp_listener_fsm.sv`:

| Line(s) | Change | Clause |
|---|---|---|
| 84-106 | banner: the shared applicant, owner, riders, type sum, handover, last declarer | 802.1Q-2018 10.7.7, 35.2.6 NOTE, 35.1.2.2, Table 35-14; Milan v1.2 4.2.7 |
| 398-408 | `dcl_r` (own type), `eq_r` (same-stream pairs), `wdone_r` (walk mark) | 10.7.7 |
| 536-613 | `owner_map`: groups, owner, active and quiet members, the type sum `cfp_w`, the group operation | 10.7.7; 35.1.2.2; Table 35-14; 35.2.6 |
| 629-675 | `app_arb`: a request only sets `dcl_r` and still waits while a Leave is parked (638-641); an A8 applies nothing itself (645-647); the group operation (648-653) waits out a settle or teardown; quiet members take no event (654-658); a slot already walked takes no second tx! (667-673) | 10.7.7, 35.1.2.2 |
| 677-719 | `handover`: the deferred move and the A15 hand-over (`hand_w`) | 35.1.2.2 (still wanted: no Lv) |
| 768-787 | settle: a settle that hands its applicant over owes nothing (773-775, 784) | #188 rules kept |
| 817-819, 847-853, 882-889, 894-896, 910, 916-923, 954-981 | registers: reset; `dcl_r` from the grants; the sum declared on New!; the pair map written by the settle; `dcl_r` cleared by A8 and A15; walk marks cleared at the walk's start and set by its tx!; the handover's writes, last in the block | as above |
| 1176-1178 | `lstn_decl_state` is the sink's own type while its stream's applicant declares | ruling item 4 |

`docs/architecture/10_srp_engine.md`: §5.1 table row (214) and cost note (248-249); §6.4 new
part "Sinks on one stream share one declaration" (616-650, anchor `sec-10-shared-stream`).

Tests and campaign: section 3. READMEs: `tb/srp_stream_fsms/README.md:8, 99-127`;
`tb/srp_top/README.md:14, 251, 707-708, 788, 827-871`. Commit 3: `tb/pp_top/gsi_mutants.py:92-97`
and `tb/pp_top/README.md:532-538` (section 4.3).

## 3. New checks, planted mutants and failing words

Ruling item 5, case by case:

| Ruling case | Checks |
|---|---|
| two sinks on one stream: exactly ONE VectorAttribute per value on the wire, frame bytes | SW1 (wire, byte-exact), SH1 (every tick) |
| unbind the owner first, then the rider: no Lv, the declaration continues, then one Lv | SH2, SW2 |
| the reverse order | SH3 |
| three sinks | SH4 |
| a rider rebind to another stream | SH5 (and SH9, the rebind on the clock after the owner's A8) |
| the type combination: Ready with AskingFailed gives ReadyFailed | SH6, SW3 (wire, FourPacked 3) |
| a Milan peer registrar (4.2.7.2.2) never deregisters while a sink wants the stream | SW2 (a peer Registrar model fed every MSRP frame) |
| (the handover mechanics) | SH7 (a handover in the middle of a tx! walk), SH8 (an owner's A8 and A15 on consecutive clocks) |

`tb/srp_stream_fsms/sim_main.cpp` (section SH, expectations from the suite's own Table 10-3 model
of one applicant): helpers `listener_words` :1315, `model_words` :1327,
`shared_stream_goes_quiet` :1334, `tick_sends` :1366, `ticks_follow_the_model` :1581; SH1-SH2
`owner_unbinds_first_then_the_rider` :1375, SH3 :1409, SH4 :1433, SH5 :1454, SH7 :1492,
SH8 :1525, SH9 :1555, SH6 :1594; declarations :437-447, calls in `run()` :1683-1690 (each
function under the parent's 100-line limit). `tb/srp_top/sim_main.cpp` (group `share`):
`listener_values` :3002, the peer Registrar model `PeerRegistrar` :3019, `peer_sees` :3045,
`sinks_settle_and_register` :3052, SW1-SW2 :3064, SW3 :3113; group dispatch :629-632, :3153.

Every control is a checked-in patch of `tb/srp_top/mutations/`, run by `tb/srp_top/mutants.py`
(issue #193 block :211-235, coverage set :327-328), and KILLED at the head by its named check. The
words are from the head campaign's receipts (`receipts/round1b/campaigns/head/work/srp_top/`).
A label graded on two suites keeps one receipt, the later run, so its earlier suite was run
again alone at the head from a fresh export (`receipts/round1b/head-extra/`, marked †):

| Check | Control | Failing words at the head |
|---|---|---|
| SH1 one applicant per tick, owner holds, riders VO | `listener-settle-compare-dropped` (the settle never finds another sink on its stream_id) | `FAIL: SH1: 2 sinks on one stream: every tx! sends what ONE applicant sends, the owner (sink 0) holds it, the riders are VO, each sink reports Ready (one 0 got '3/2 3/2', app0 QA, riders VO 0, decl 1)` |
| SH1 a received LeaveAll draws no Empty from a rider | `listener-rider-not-quiet` | `FAIL: SH1: a received LeaveAll: each tx! sends what ONE applicant sends (want '3/2', got '3/2 4/0', 2 pushes)` |
| SH2 the owner unbinds: no Lv, no New | `listener-teardown-applies-lv` (A8 applies Lv! to its slot, the behaviour before the issue) | `FAIL: SH2: the owner unbinds: the next tx! sends no Lv and no New (want '', got '0/2', 1 pushes)` |
| SH2 the rider holds the applicant in its state | `listener-handover-drops-state` | `FAIL: SH2: the owner unbinds: the rider holds the applicant in its state, still Ready (app VO/VN, decl 0/2)` |
| SH2 (the issue's Lv) | `listener-withdraw-ignores-riders` (a group counts only the sink's own type) † | `FAIL: SH2: the owner unbinds: the next tx! sends no Lv and no New (want '', got '5/2 0/2', 2 pushes)` |
| SH2 the rider last: one Lv | `listener-teardown-keeps-declaring` (A8 leaves the sink's type set) † | `FAIL: SH2: the rider unbinds last: the next tx! sends one Lv, Ready (want '5/2', got '', 0 pushes)` |
| SH3 the reverse order | `listener-teardown-keeps-declaring` † | `FAIL: SH3: the owner unbinds last: the next tx! sends one Lv, Ready (want '5/2', got '', 0 pushes)` |
| SH4 three sinks | `listener-group-order-reversed` (the election runs from the highest index) | `FAIL: SH4: 3 sinks on one stream: every tx! sends what ONE applicant sends, the owner (sink 0) holds it, the riders are VO, each sink reports Ready (one 1 got '', app0 VO, riders VO 0, decl 1)` |
| SH5 a rider rebind | `listener-rider-settle-hands-over` (any member's A15 hands over, a rider's VO too) | `FAIL: SH5: a rider rebinds to another stream: the owner's declaration goes on with no Lv and no New, the rider declares the new stream, New Ready (first stream '0/2', new stream '0/2', decl 2/2)` |
| SH6 the type sum | `listener-type-not-combined` (the last declarer's type) † | `FAIL: SH6: Ready with AskingFailed: New, ReadyFailed (want '0/3', got '0/1', 1 pushes)` |
| SH7 a handover mid-walk | `listener-handover-forgets-walk-mark` | `FAIL: SH7: the owner unbinds while the walk is between it and the rider: the rider takes the walked applicant and the walk sends ONE New (got '0/2 0/2', app VO/AA)` |
| SH8 A8 and A15 on consecutive clocks | `listener-settle-parks-shared-stream` (the settle parks although a rider declares) | `FAIL: SH8: the owner rebinds on the clock after its A8: the rider holds the applicant in its state, the first stream gets no Lv and no New, the new stream New Ready (held 0, first stream '5/2 0/2', new stream '')` |
| SH9 a rider's A15 on the clock after the owner's A8 | `listener-group-op-during-settle` (the group operation does not wait out a settle) | `FAIL: SH9: the rider rebinds on the clock after the owner's A8: the first stream gets one Lv, Ready, the new stream New Ready (first stream '', new stream '0/2')` |
| SW1 one VectorAttribute, byte-exact | `listener-settle-compare-dropped` † | `FAIL: SW1: two sinks declaring one stream: the frame carries ONE Listener VectorAttribute for it, New Ready, byte-exact (47 B, 2 values, decl 2/2)` |
| SW2 the peer Registrar never deregisters | `listener-withdraw-ignores-riders` | `FAIL: SW2: the owner unbinds: a Milan peer Registrar never deregisters, no Lv is sent and the declaration goes on (state 1, deregs 1, Lv 1, re-joins 3, decl 2)` |
| SW2 the rider last: one Lv, one deregistration | `listener-teardown-keeps-declaring` | `FAIL: SW2: the rider unbinds last: one Lv, and the peer Registrar deregisters once (state 1, deregs 0, Lv 0)` |
| SW3 ReadyFailed on the wire | `listener-type-not-combined` | `FAIL: SW3: Ready with AskingFailed on one stream: one New, ReadyFailed, byte-exact; each sink reports its own type (35 B, decl 2/1)` |

The same checks against the base RTL (`receipts/round1b/newchecks-at-base/`): 26 of the 42 new
stream-FSM checks fail (the other 16 are steps a per-sink plane also passes), and all 5
`share` checks fail. SW1 at base shows the round-1 measurement again: 47 B, 2 values.

The nine re-anchored issue #188 controls keep their edits on the moved lines;
`listener-declaration-not-held` now drops the park term of the declaration grant, the one
place that now holds a new stream's request while a Leave is parked. All are KILLED with the
same tags as at base (section 4).

## 4. Base and head records

Base `21601694` and head `67b90c17` (commits 1 and 2: the RTL, the docs and every check). Commit 3
(`788425db`, the final head) changes only `tb/pp_top/gsi_mutants.py` and `tb/pp_top/README.md`
(section 4.3), so the head records at `67b90c17` stand for every gate that reads neither file, and
the gates that read either were run again at `788425db`. Each `.rc` is the command's own exit
status, written by a wrapper, never through a pipe. Base gates ran in a clean clone at the base,
head gates in clean clones at the head (no untracked or ignored files before each run).

Tools: Verilator 5.050 (the CI pin; a wrapper turns a build's `-j 0` into `-j 2`, so two builds
stay inside the memory budget; nothing else changes), sv2v 0.0.12, Yosys 0.33 for the processor
gates (the CI portability job's package), Yosys 0.66 for the parent gates (the parent's pin),
wavedrom 2.0.3.post3, mmdc 11.16.0, behave 1.3.3 (`receipts/round1b/*/tools.txt`,
`*/STATE.txt`). Normalized base-vs-head diffs (paths, temporary names, timings, sv2v's `all.v:N`)
are under `receipts/round1b/compare/`.

### 4.1 Processor gates

| Gate | Base 21601694 | Head 67b90c17 | Final head 788425db | Base vs head |
|---|---|---|---|---|
| `scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,237 checks, 0 failing | rc 0, 1,030,284, 0 failing | (reads neither file) | only `srp_stream_fsms` 1,361 → 1,403 (SH1-SH9), `srp_top` 8,660 → 8,665 (SW1-SW3) and the total |
| `scripts/check-req-tags.py --suites --evidence` | rc 0, 230 evidence lines | rc 0, 230 | | identical |
| `scripts/lint_hdl.sh` | rc 0, 41 LINT OK | rc 0, 41 | rc 0 | identical |
| `make check` | rc 0 | rc 0 | rc 0 | links 1,218 → 1,223 (1,224 at the final head), ids 640 → 652 files (the 12 new patches); the rest identical |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 | rc 0 | identical |
| `syn/yosys/run.sh` | rc 0 | rc 0 | | identical after normalizing `all.v:N` (the listener module is longer) |
| `tb/elab_guards/guards.py --frontend yosys --jobs 2` | rc 0 | rc 0 | | identical after the same normalization |

### 4.2 Campaigns that build a changed file

Every campaign that builds `KL_srp_listener_fsm.sv` (the srp_top campaign and every campaign that
builds the processor top). Not run, because they build no changed file: `tb/maap`,
`tb/adp_engine`, `tb/srp_admission` mutants, `tb/aecp_cmds` controls, `tb/acmp_talker` retry
mutants, `tb/nvm_port` figures. Drivers at `--jobs 2` or `3` (`receipts/round1b/camps/SOURCES.txt`
names the runner of each record):

| Campaign | Base 21601694 | Head 67b90c17 | Base vs head (sorted, normalized) |
|---|---|---|---|
| `tb/srp_top/mutants.py` | rc 0, 179 of 179, coverage 101/101 | rc 0, 196 of 196, coverage 113/113 | the 161 arm runs at both have the same verdict and failing tags, and the same counts but one: `listener-declaration-not-held` 9 → 5 failing checks (its edit is now on the declaration grant); 16 new arm runs (12 new patches) and 1 new control group (`share`) |
| `tb/pp_top/acmp_mutants.py` | rc 0, 65 of 65 KILLED | rc 0, 65 of 65 | identical |
| `tb/pp_top/notify_mutants.py` | rc 0, 135 of 135 | rc 0, 135 of 135 | identical |
| `tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 | rc 0, 110 of 110 | identical |
| `tb/pp_top/aecp_mutants.py` | rc 0, 67 | rc 0, 67 | identical |
| `tb/pp_top/aecp_dispatch_mutants.py` | rc 0, 73 | rc 0, 73 | identical |
| `tb/pp_top/ctr_mutants.py` | rc 0, 18 | rc 0, 18 | identical |
| `tb/pp_top/gsi_mutants.py` | rc 0, 20 detected | rc 1 at 67b90c17: `failure-change-redeclares` survived (section 4.3); rc 0, 20 detected at 788425db | identical at 788425db |
| `tb/pp_top/name_wr_mutant.py` | rc 0, killed | rc 0, killed | identical |
| `make -C tb/name_state mutants` | rc 0, 16 KILLED | rc 0, 16 | identical (tree path only) |
| `make -C tb/elab_guards mutants` | rc 0, 160 of 160 | rc 0, 160 of 160 | identical after normalizing `all.v:N` |

### 4.3 The gsi control that the design made equivalent (commit 3)

`gsi_mutants.py`'s `failure-change-redeclares` planted "a FailureInformation change raises a
declaration request" (`|| ind_fchg_w[s]` in `ind_reg_w`). Before #193 every granted request
applied New!, so the edit put a Listener New on the wire and failed `GI FAILED-REFRESH wire: a
changed FailureInformation sends no Listener New`. In the shared plane a request only sets the
sink's own type, and New! is applied for a first declarer or a changed type sum; a request of an
unchanged type changes nothing on the wire, so the old edit is equivalent (head campaign at
67b90c17: `run_rc 0`, `passed: false`, the driver's `RuntimeError`). Commit 3 plants the same
defect where the New! is decided now, `op_new_w` (`|| ind_fchg_w[s]`), and documents it in
`tb/pp_top/README.md:532-538` and `tb/pp_top/gsi_mutants.py:92-97`. At 788425db the arm fails exactly the named check
(`FAIL: GI FAILED-REFRESH wire: a changed FailureInformation sends no Listener New`) and the gsi
campaign is identical to base. The behaviour change behind it: a single sink's request of the type
it already declares (only reachable when a withdrawal and a re-registration meet before the
request is granted) no longer re-sends New; nothing else on the wire moves.

## 5. Scratch-parent consumer gate table

Scratch parent: a local clone of kebag-logic/milan-fpga dev `e26f1816`, every submodule
initialised, with three local commits in this order (never pushed):
`pp178-a634/parent-evidence-classification.patch` (sha256 76625170…),
`pp176-a629/parent-adoption-milan_dp-67.patch` (e142e2e7…),
`190-a654/parent-scratch-tspec-every-slot.patch` (37d1b76e…). The protocol-processor gitlink was
then committed at the base 21601694 (`d79003a5`), at the head 67b90c17 (`da9e6977`) and at the
final head 788425db (`d669b21c`), each fetched from the lane, the working tree clean
(`STATE.txt`). Every git command in the submodule was preceded by a top-level identity check.

| Parent consumer gate | Base 21601694 | Head 67b90c17 | Final head 788425db | Base vs head |
|---|---|---|---|---|
| `check_cpp_idiom.py` | 0 | 0 | 0 | identical (every ratchet holds) |
| `check_py_idiom.py` | 0 | 0 | 0 | line total 259,319 → 259,344 (259,345 at the final head) |
| `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest`, `check_port_contracts.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `docs_check.py`, `check_sh_idiom.py`, `check_hygiene.py --check`, `check_sv_idiom.py`, `check_baremetal_only.py --check`, `check_soc_sources.py`, `check_todo_ownership.py`, `lint_rtl.py --check --self-test --jobs 4`, `behave --no-capture -f plain` (tests/) | 0 each | 0 each | 0 each | identical |
| `check_submodule_docs.py` | 1 | 1 | 1 | identical: "protocol-processor: documented pin differs from Git" and the stale submodule diagram, which any gitlink the parent's docs do not record fails |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 | 0 | | cells: milan_datapath 75,037 → 75,555, KL_pp_shadow 62,499 → 66,001, KL_gptp_shadow 3,368 both |
| `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` | 0 | 0 | | only the pin line |
| `make -j8 -C tb/verilator/pp_shadow VERILATOR_JOBS=2` | 0 | 0 | | 609 + 609 + 649 + 317 checks, 0 failures at both (four binaries interleave their lines) |
| `make -j8 -C tb/verilator/nvm_cosim lint` / `quick JOBS=2 POOL=2` | 0 / 0 | 0 / 0 | | identical (timings only) |
| `make -j8 -C tb/verilator/milan_dp_render VERILATOR_JOBS=2` | 0 | 0 | | identical check lines |
| `make -j4 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2` | 0 | 0 | | 10,465 `[ok]`, 1,127 `[PASS]`, 0 `[FAIL]` at both; sorted check lines identical |
| `sw/builder/test_builder.py` | 0 | 0 | | "ALL GATES PASS EXCEPT 1 NOT RUN" at both (gate 11 needs a build tree not on this host); self-test finding counts vary run to run |
| `syn/yosys/ooc.sh --record-rom-digests tcam` (ledger row in the scratch tree, then restored) | 0 | 0 | | ROM rows: `ltn_rom.hex` 23cc67ee… and `ucode.hex` a7b1af66… at both pins |
| `syn/yosys/ooc_selftest.py` | 0 | 0 | | identical (75 arms) |
| `syn/yosys/ooc.sh KL_pp_shadow` | 0 | 0 | | LUT 56,501 → 57,538 (+1,037), LUT_TOT 60,737 → 61,774, FF 26,332 → 26,382 (+50); LUTRAM, RAMB36/18, DSP, CARRY4 unchanged |

The final-head column covers the gates that read processor text outside the RTL; the RTL, the
ROM generators and every build input of the other gates are identical at 67b90c17 and 788425db.
Not run: the parent's Vivado resource gate (`syn/ooc/pp_resource_gate.py check`), which needs a
Vivado route; the Yosys OOC figure above is the area record.

## 6. Run notes

- 14:10 resumed after the host reset. The tree held one early partial edit of
  `KL_srp_listener_fsm.sv` (register declarations and a first owner map) and a stale editor
  temp file (removed). No commits.
- About 14:52 a process listing, filtered by the shell wrapper, showed no runners. On that false
  reading duplicate base runs were started, one with a `git clean` of the base tree under the
  live base `run_suites`. All duplicates and the compromised base `run_suites` were stopped by
  process group and their outputs set aside as void (`rec/void/` in scratch, not used). Base
  `run_suites` was rerun from a fresh clone, the base campaigns from the start.
- /tmp is a tmpfs here, so campaign copies count against the unit's memory: campaigns ran with
  TMPDIR on disk. A watchdog trimmed page cache (memory.reclaim) when MemoryCurrent passed
  8 GB; anon peaked at about 4.4 GB (`receipts/round1b/memwatch.log`).
- To shorten the tail, a second runner took a campaign list from the other end, each claiming a
  campaign before starting it, and a watcher stopped the first runner if it started a claimed
  one. Base: the runners met at `ctr`, run once by the second. Head: runner B had just started
  d3 when the split took effect, and the split's cleanup removed its work directory, so that
  d3 run ended rc 1 after 167 s (void, `rec/void/head-d3-runnerB-broken-by-split/`). The helper
  then ran d3 at `--jobs 2`; with the base records done, that run was stopped at 28 of 110 arms
  (void, `rec/void/head-camps-d-jobs2-cut/`) and d3 ran again alone at `--jobs 4`, the record.
- The 67b90c17 gsi rc 1 is a record, not a void run: it is what commit 3 answers (section 4.3).

## 6a. Processor main moved during the lane

At the end of the lane `git ls-remote` showed processor main at
`08023123ae2df5d802d20a9bb22cd063942845cd` (PR #197, #192 started/stopped notifications), no
longer 21601694. The branch stays on 21601694 as assigned (no rebase, no merge). #197 also edits
`tb/pp_top/gsi_mutants.py` and `tb/pp_top/README.md`, which commit 3 touches;
`git merge-tree` of the head with it is clean. For information only, a scratch merge (never
committed to the lane, never pushed; `receipts/round1b/merge-check/`) passes `tb/pp_top`
(10,721 checks, 0 failing) and the gsi campaign (23 detected by named checks, #197's three
new controls included; golden and restored pass).

## 7. Output directory

- `receipts/INDEX.md`: generated from the files present (path, bytes, sha256).
- `receipts/round1b/`: this round. `repo-record.txt` (base, head, commits, clean tree, sha256 of
  every changed file, remote refs); `gates/{base,head,head-final}/`;
  `campaigns/{base,head,head-final}/` (each campaign's log, rc and seconds; the per-arm receipts
  of the srp_top and gsi campaigns under `work/`; `SOURCES.txt` names the runner of each);
  `consumers/{base,head,head-final}/` with `STATE.txt` each; `ooc/{base,head}/`;
  `newchecks-at-base/` (the head's new checks against the base RTL); `head-extra/` (the
  dual-suite arms' earlier suite, alone); `compare/` (normalized base-vs-head diffs and summaries);
  `dev/` (the targeted listener-arm campaign and the pp_top suite run before the first commit);
  `scripts/` (every runner used); `memwatch.log`; `EXTERNAL-RECORDS.csv` (sha256 and size of the
  25 records over 200 KB kept in scratch). Host roots are replaced by tokens (`<scratch>`,
  `<lane>`, `<home>`, `<toolroot>`, `<tmp>`).
- `receipts/round1/`: the round-1 STOP, unchanged.
- No toolchain, virtualenv, package, tree export or file over 200 KB is in this directory.

## 8. Posts on #193

- Round 1: `[A661] TAKEN` (6289893976), `[A661] STOP` (6289991979).
- Round 1b: `[A661] REVIEW READY` with the head 788425db, issue #193 comment 6299186889
  (text in `receipts/round1b/review-ready-comment.md`). TAKEN was not posted again.
- No push, no PR, no edit of any existing comment.
