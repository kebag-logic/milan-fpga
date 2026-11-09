# [A754] HANDOFF: processor issue #216, round 2

Status: REVIEW READY at head `84f6d6a`. Every processor gate (the full sweep as four shard units), every mutation
campaign with every arm killed and the SRP coverage check (185/185), all 40 scratch-parent consumer gates are rc 0;
the two-placement simulation reports the three owed rows of this defect gone; every ruling item and every
acceptance item is met (the tables below).

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked). Branch
  `216-mrp-applicant`, local, not pushed.
- Source base `044cb25f4ed2187bd238490650e73d5d189855d1` (processor main). Round 1 head
  `60094a268c0df46703a3bee08c94118153634fd9` (REVIEW READY, PR #218); HEAD was `60094a2` before the first round 2
  commit. Round 2 head `84f6d6ad77d51d678f8efdf26b45aae011a42001`.
- Round 2 commits on `60094a2` (one-line subjects, no body, no trailers; no rebase, no amend):
  - `b655100` Take every VID Registrar to MT at LINK_DOWN and LINK_UP, restart each VID's Applicant at LINK_UP, and
    grade it and the Table 10-3 VP rows with AP8, DA6, DA7 and VR12 to VR18 and ten arms (issue #216)
  - `b5f9e53` Refuse N_VIDS_P above ENC_DEPTH_P in KL_srp_top at elaboration, graded by its guard-bench case and five
    arms (issue #216)
  - `ceb6a98` Record the VID link change in 10 sections 6.1, 6.2 and F10.3, the pre-join VID registration as GAP-18
    in 00, the T-MRP-LEAVEALL wording in 6.5, the new rows in 09 8.15 and the measured counts in the READMEs
    (issue #216)
  - `84f6d6a` Record the measured srp_top total and the area of the VID link change in 10 section 5.1 (issue #216)
- Authority: the manager's round 2 ruling on issue #216 (issuecomment-6740735425), on R801-1
  (issuecomment-6740368085) and R802-1 (issuecomment-6740725581). TAKEN posted 2026-11-09
  (issuecomment-6740811350).

## Ruling items

| # | Ruling | Done by |
|---|---|---|
| 1 | VID Registrar to MT at LINK_DOWN (Flush!) and LINK_UP (Begin!), link input wired in `KL_srp_top`; VID Applicants Begin! at LINK_UP; a check (Registrar IN, link bounce, the next VID 2 sJ JoinMt and the round restarting with New) and an arm failing it by name; 10 6.2 / F10.3; the stream report | `KL_srp_vlan` `link_up_i`, `KL_srp_top:476`; `tb/srp_top` AP8 with `vlan-link-keeps-registrar`, `vlan-link-no-begin`, `top-vlan-link-unwired` (each fails `AP8:`), and `tb/srp_encoder` VR14 to VR18 with four more arms; 10 6.2 "A link change" and F10.3's link edges; the stream report below |
| 2 | `tb/srp_encoder/README.md` count `8 FAIL — V10, W4, W5 (two), B1 (four)` | `tb/srp_encoder/README.md:277` (the row moved from :255) |
| 3 | 10 6.5: R802-1 R1's exact fix | `10_srp_engine.md:1149-1151`: "every `T-MRP-LEAVEALL` ([F08.1](08_timing.md#fig-08-constants)) from Begin!" |
| 4 | two Table 10-3 checks distinguishing VP from AP, killing `p09-note4-inverted`, `p12-txla-vp-stays`, `p19-txla-vp-sends-sj`; the guard `N_VIDS_P <= ENC_DEPTH_P` in `KL_srp_top` with a plant | DA6/VR12 (note 4) and DA7/VR13 (txLA! from VP), the probes as published each failing them at the head, and their arms `vp-rjoinin-ignores-note4`, `vp-txla-stays-vp`, `vp-txla-sends-sj`; `g_vids_fit` (`KL_srp_top:267-275`) with its `tb/elab_guards` case and five planted arms |
| 5 | the VID registered before the first join as a deviation in 00's gap register, basis: note 11 covers the Applicant only, Table 10-4 would read IN | GAP-18 (`00_MILAN_COMPLIANCE_REVIEW.md:369-382`), its F00.2 row (:598), owned by REQ-SRP-006 (:541); 10 6.2 cites it |

Working notes: round 1's scratch parent and twin copies were moved aside to `$VALIDATION_STORAGE/scratch/pp216-parent-r1`
and `pp216-twin-r1` (nothing deleted); this round's are fresh clones at `$VALIDATION_STORAGE/scratch/pp216-parent` and
`$VALIDATION_STORAGE/scratch/pp216-twin`. The shard clones are `$LANES/pp216-a754b-shard0..3` (scratch, at the
head).

## Changes (file:line at head `84f6d6a`, clause)

| Where | What | Clause |
|---|---|---|
| `hdl/srp/KL_srp_vlan.sv:75` | new input `link_up_i` (internal module port; `KL_srp_top`'s port list is unchanged) | |
| `hdl/srp/KL_srp_vlan.sv:177, 183-188, 339, 345` | the link level of the previous clock; `link_ev_w` (either edge), `link_rise_w` (LINK_UP) | |
| `hdl/srp/KL_srp_vlan.sv:279-280` | LINK_DOWN (Flush!) and LINK_UP (Begin!) take every VID Registrar to MT, after (so winning over) the clock's received events, rLA! and txLA! | 802.1Q-2018 Table 10-4 (Begin!, Flush!), 10.7.5.1, 10.7.5.2; 10.7.6.3 |
| `hdl/srp/KL_srp_vlan.sv:289-290` | LINK_UP is Begin! on every VID Applicant (VO), then New! on each entry with users (VN); the clock's user op or tx! then moves the restarted state; an entry with no user is VO and the next walk discards it | Table 10-3 Begin! and New! rows, note 11 |
| `hdl/srp/KL_srp_vlan.sv:449-455, 474` | a message the walk holds for the encoder on the LINK_UP clock is withdrawn (`vlan_ev_valid_o` low), and the entry takes the walk's tx! in its restarted state (New) | Table 10-3 tx! after Begin!/New! |
| `hdl/srp/KL_srp_vlan.sv:37-47, 234-239` | header and block comments: the link behaviour | |
| `hdl/srp/KL_srp_top.sv:476` | `u_vlan.link_up_i` wired to the engine's `link_up_i` | |
| `hdl/srp/KL_srp_top.sv:267-275` | elaboration guard `g_vids_fit`: `$fatal` when `N_VIDS_P > ENC_DEPTH_P` (the MVRP round would wait on its own walk; no MVRP high-water drain). The defaults (4, 12) and the processor top (no override) pass | R802-1 S2 |

Unchanged on purpose: the talker and listener stream Applicants (no link input; reported below, not changed), the
talker's streaming licence `vid_sent_o` across a link change, every MRP timer (no value, draw range or F08.1 row
moved), `hdl/adp`, `hdl/aecp`, `hdl/acmp` (`git diff --stat 60094a2 HEAD -- hdl/adp hdl/aecp hdl/acmp` is empty), and
no top-level port, parameter or register-map change (`hdl/top` untouched; `KL_srp_top`'s ports and parameters are
identical at `60094a2` and at the head; the new port is on `KL_srp_vlan`, internal).

Docs at the head:
- `docs/architecture/10_srp_engine.md:515-536` (section 6.2, new paragraph "A link change"), `:484-487` (F10.3: the
  LINK_DOWN and LINK_UP edges), `:500-507` (6.2: the pre-join registration now cited as a recorded deviation, GAP-18,
  with its basis), `:456-460` (6.1: DA6 and DA7, the VP rows), `:1149-1151` (6.5: "every `T-MRP-LEAVEALL`
  ([F08.1](08_timing.md#fig-08-constants)) from Begin!", R802-1 R1's exact fix), `:339-347` (5.1: the area).
- `docs/00_MILAN_COMPLIANCE_REVIEW.md:369-382` (GAP-18 [Minor] in the gap register, with its basis: Table 10-3 note 11
  covers the Applicant only; the Registrar per Table 10-4 and 10.7.8 would read IN), `:598` (its F00.2 disposition
  row), `:541` (REQ-SRP-006 owns it, as `scripts/check-matrix.py` requires of every GAP).
- `docs/architecture/09_verification.md:875-877` (8.15: the VP rows, the VID link change, the guard).
- `tb/srp_encoder/README.md:277` now reads `8 FAIL — V10, W4, W5 (two), B1 (four)` (R801-1-F01 = R802-1 F2; the row
  was at :255 before the new rows above it); the suite total 1659; the DA and VR descriptions; 14 re-measured and 9
  new arm rows.
- `tb/srp_top/README.md`: the total 8706, AP8, the coverage line (AP1-AP8), 2 re-measured and 3 new arm rows.
- `tb/elab_guards/README.md`: 32 guards, 96 / 160 checks, 165 arms, the new guard's case.

## New checks and their planted arms (failing words)

Each arm is a checked-in patch under `tb/srp_top/mutations`, graded by `make -C tb/srp_top mutants`, which requires
the named words in a FAIL line (the third column).

| Check | Arm | Failing words the campaign requires | Failures |
|---|---|---|---|
| `tb/srp_top` AP8: Registrar IN (peer JoinIn), link down 30 ms and up; no VID 2 JoinIn after it, and New, New, then JoinMt, the first within 240 ms of LINK_UP | `vlan-link-keeps-registrar` | `AP8:` (srp_top applicant); `VR14 LINK_DOWN` (encoder) | 2; 3 |
| AP8 (the restart) | `vlan-link-no-begin` | `AP8:`; `VR15 LINK_UP` | 1; 5 |
| AP8 (the wiring) | `top-vlan-link-unwired` (`KL_srp_top` ties the VID link input up: the round 1 behaviour, JoinIn after the bounce) | `AP8:` | 2 |
| `tb/srp_encoder` VR14 LINK_DOWN takes IN to MT, Applicant kept; VR15 LINK_UP takes IN to MT and restarts in VN: New, New, JoinMt | `vlan-link-keeps-registrar`, `vlan-link-no-begin` | as above | |
| VR16 a received JoinIn on either link clock registers nothing | `vlan-link-rx-wins` | `VR16` | 1 |
| VR17 a VID with no user (Lv owed) is VO at LINK_UP: nothing sent | `vlan-link-keeps-leaving` | `VR17` | 1 |
| VR18 a LINK_UP while the walk holds a JoinIn withdraws it: New | `vlan-link-push-kept` | `VR18 a LINK_UP while the walk holds` | 2 |
| VR18 a LINK_UP on the clock the walk evaluates the VID comes first: New | `vlan-link-after-tx` | `VR18 a LINK_UP on the clock the walk evaluates` | 1 |
| DA6 (Domain) and VR12 (VID 2): a peer LeaveAll riding its JoinIn leaves VP alone (note 4): JoinIn on two tx!, then nothing | `vp-rjoinin-ignores-note4` (= R802-1 probe `p09-note4-inverted`) | `DA6`; `VR12 a peer LeaveAll` | 2; 2 |
| DA7 (Domain) and VR13 (VID 2): after a peer Lv (VP) the own LeaveAll's tx! sends Mt (s, then AA), then one JoinMt, then nothing | `vp-txla-stays-vp` (= `p12-txla-vp-stays`), `vp-txla-sends-sj` (= `p19-txla-vp-sends-sj`) | `DA7`; `VR13` | 2; 2 each |
| `tb/elab_guards` `KL_srp_top.g_vids_fit`: refused as a `$fatal` at its line by Verilator and Yosys at `N_VIDS_P` 13, elaborates at 12 | the bench's five arms (`error`, `warning`, `initial`, `tightened`, `loosened`) | `FAIL: GUARD ` / `FAIL: ELAB ` naming the guard | |

The three surviving probes of R802-1, applied as published (their patch files unchanged) to the head: each fails the
encoder suite, `1659 checks: 1657 PASS, 2 FAIL` (p09: DA6, VR12; p12 and p19: DA7, VR13). R802-1's link-bounce
probe patch (`patch -p1`, the moved lines of `sim_main.cpp`) passes at the head, `2 checks: 2 PASS, 0 FAIL`:
`R802LINK VID 2 after LINK_UP: New@3801 New@4001 JoinMt@4201 JoinMt@5001 JoinMt@6001` (receipts/r802-probes).

Re-expressed arms (same name, same intent, same rows): `join-sent-at-handover`, `vlan-registrar-never-in`,
`vlan-rlv-ignored`, `vlan-rx-loses-to-leaveall` no longer applied because the lines around their edit moved; each
is regenerated from the same edit (`tools/make_arm_patches.py`) and still killed.

## Stream Applicants across a link bounce (report only, not changed)

Evidence: a disposable `tb/srp_top` group (receipts/stream-link-bounce/streamlink.tb.patch, applied to a scratch copy
only; log probe.log). DECLARE_TALKER source 0 on VID 2 and DECLARE_LISTENER sink 0 on a peer Talker Advertise that
registers; after 3 s the link goes down for 30 ms and comes up.

| Case | Talker Advertise after LINK_UP | Listener Ready after LINK_UP | VID 2 and Domain after LINK_UP |
|---|---|---|---|
| the peer sends nothing after the bounce | `JoinMt@4203 JoinMt@5203 JoinMt@6203` (LINK_UP at 3331): no New; the first message is the JoinMt of the next `periodic!`, 872 ms after LINK_UP | `Lv@3403`, then nothing (the sink registrar was flushed at LINK_DOWN, issue #212, so the declaration is withdrawn) | VID 2 `New@3401 New@3601 JoinMt@3801`; Domain `New@3403 New@3602 JoinMt@3802` |
| the peer declares its Talker Advertise again 100 ms after LINK_UP | the same: JoinMt at each `periodic!`, no New | `Lv@3403 New@3603 New@3803 JoinMt@4003`: declared again, New, New, then JoinMt, once the Talker Advertise registers again | as above |

So the Talker Advertise is not declared again after a link bounce: its Applicant takes no Begin!/New! at LINK_UP
(it has no link input), and the new link partner hears it only at the next `periodic!`, as a JoinMt, never as New,
where the Domain and now each VID restart with New, New, then the Join. Under the engine's mapping of LINK_UP to
Begin! that is a defect of the talker stream Applicant, for its own issue. The Listener Ready is withdrawn with its
sink registration at the link change and declared again, New, New, then the Join, when the peer's Talker Advertise
registers again; its Lv goes out after LINK_UP for a declaration the new partner never saw (harmless, but also a
consequence of the stream Applicants having no Begin!). Not changed in this round, as the ruling says.

## Area (the processor's syn/yosys flow; xc7, flattened; tools/area/area.sh)

| Shape | LUT base `044cb25f` / `60094a2` / head | FF base / `60094a2` / head | RAM cells |
|---|---|---|---|
| `KL_srp_top` 2x2 | 13,536 / 14,109 / 14,108 | 5,407 / 5,447 / 5,447 | 114 / 112 / 112 |
| `KL_srp_top` 8x8 | 28,002 / 28,814 / 28,903 | 11,297 / 11,337 / 11,337 | 179 / 177 / 177 |
| `KL_srp_domain` | 150 / 215 / 215 | 119 / 128 / 128 | 0 |
| `KL_srp_vlan` | 364 / 594 / 643 | 132 / 147 / 148 | 3 / 1 / 1 |
| `KL_srp_encoder` | 2,747 / 2,712 / 2,712 | 1,358 | 52 |

The base column is round 1's receipt (unchanged code); `60094a2` was re-measured this round and equals round 1's
figures; the head was measured on its own clean clone (receipts/area/area-84f6d6a-out). The round 2 change is 49 LUT and 1 FF of `KL_srp_vlan` alone; in `KL_srp_top` -1 LUT at 2x2 and +89 at
8x8, inside this flow's LUT noise (10 section 5.1), with no flip-flop. Recorded in 10 section 5.1.

## Gates at the head `84f6d6a` (processor)

Each gate ran on a clean `--shared` clone of `84f6d6a` (checked: HEAD, empty `git status --porcelain --ignored`), with
CI's pinned Verilator 5.050, Yosys 0.66, sv2v v0.0.12 and a CPython 3.12.3 venv; none was piped; each has its cmd,
log, rc, start, end and interpreter record under receipts/head-84f6d6a.

| Gate (CI job) | Command | rc | Result | Receipt |
|---|---|---|---|---|
| docs-gates | `make check` | 0 | every docs, AECP command, ids and figures gate OK; `lint: 41 mermaid + 18 wavedrom blocks checked, OK` | proc/make_check.* |
| matrix | `python3 scripts/gen_matrix.py --check` | 0 | `matrix: OK (94 rows, 0 untested)` | proc/gen_matrix_check.* |
| HDL lint | `bash scripts/lint_hdl.sh` | 0 | 41 modules `LINT OK` | proc/lint_hdl_5050.* |
| suites (full sweep, 4 shard units) | `tools/proc-shards.py` (below): the repository's `scripts/run_suites.sh` per shard, with `REQ_TAG_LOG` | 0 x 4 | 36 suites PASS, each in one shard; merged `suites: 1032113 checks total, 0 failing` (srp_top 8706, srp_encoder 1659, pp_top 11066, elab_guards 160) | sweep/ |
| requirement tags | `python3 scripts/check-req-tags.py --suites sweep.log --evidence req-tags.txt` (the merged shard records) | 0 | `req-tags executed: 266 evidence lines, 14 suites, OK` | sweep/req_tags_executed.* |
| portability | `bash syn/yosys/run.sh` | 0 | every top `YOSYS OK`, `YOSYS XILINX OK` | proc/yosys_portability.* |
| portability | `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | 0 | `elab guards: 96 checks: 96 PASS, 0 FAIL` (32 guards) | proc/elab_guards.* |
| suites job (figures) | `git fetch --no-tags <repository> refs/pull/13/head`, then `make -C tb/nvm_port figures` | 0, 0 | `all measured figures agree with the tree` | proc/fetch_pr13.*, proc/nvm_port_figures.* |
| whitespace | `git diff --check 044cb25f HEAD` | 0 | empty | proc/diff_check.* |
| SRP campaign | `python3 -B tb/srp_top/mutants.py --jobs 8` (what `make -C tb/srp_top mutants` runs) | 0 | `365 checks: 365 PASS, 0 FAIL`, every arm KILLED, `assertion coverage: 185/185; missing=[]` | camp-srp/ |
| AECP campaign | `make -C tb/pp_top aecp-mutants` | 0 | `67 checks: 67 PASS, 0 FAIL` | camp-pp/camp-aecp.* |
| AECP dispatch campaign | `make -C tb/pp_top aecp-dispatch-mutants` | 0 | `105 checks: 105 PASS, 0 FAIL`, 100 arms KILLED | camp-pp/camp-aecp-dispatch.* |
| MAAP campaign | `make -C tb/maap mutants` | 0 | `32 checks: 32 PASS, 0 FAIL` | camp-more/camp-maap.* |
| ADP campaign | `make -C tb/adp_engine mutants` | 0 | `62 checks: 62 PASS, 0 FAIL` | camp-more/camp-adp.* |
| AECP command decode controls | `make -C tb/aecp_cmds mutants` | 0 | `17 of 17 detected by their named failures; golden and restored PASS` | camp-more/camp-aecp-cmds.* |
| elaboration-guard campaign (not in CI; the bench this change adds a guard to) | `make -C tb/elab_guards mutants` (Verilator and Yosys) | 0 | `elab guard mutants: 165 of 165 killed`, the five `KL_srp_top.g_vids_fit` arms among them | camp-more/camp-elab-guards.* |
| area | `tools/area/area.sh` at `60094a2` and at the head | 0, 0 | the area table above | area/ |

The full sweep as four shard units. MemAvailable was 37 GB at the start, above 30 GB. `native-shards.py` cannot drive
this repository: it reads the submodule list from the head's `.gitmodules` (`git config --blob
<head>:.gitmodules`, rc 1 here, the processor has none) before the first unit, and it re-issues
`scripts/run_all_suites.sh ... --shard k/N`, which the processor does not have (its sweep is `scripts/run_suites.sh`,
with no shard option). `tools/proc-shards.py` keeps the rest of it: a `--shared` clone per shard at
`$LANES/pp216-a754b-shard<k>` at the head, one unit `milan-pp216-a754b-shard<k>` per shard
(`systemd-run --user --collect`, MemoryMax=10G, MAKEFLAGS=-j4, pinned with taskset to a range from
`cpu_ranges.py pick`, picked after the previous shard's unit started: 104-111, 96-103, 72-79, 64-71), and
`2026-09-21/run-recorded-gates.py` running each shard's spec. Each shard runs `tools/proc-shard.sh`: the repository's
own `scripts/run_suites.sh` text with its one suite loop given the shard's suites (suite i of the sorted `tb/*/` with a
Makefile goes to shard i mod 4; sweep/shard-k/assignment.txt), so the uPC map and M9 checks, each suite's `make`, the
verdict lines and the exit status are the repository's. `tools/merge-shards.py` requires every shard rc 0 with its
closing `0 failing` line, every one of the 36 suites PASS in exactly one shard and no FAIL or UNREADABLE line, and
writes the merged record that `check-req-tags.py` reads (sweep/merge.log: `MERGE OK`). Shard 2 (pp_top, srp_top,
srp_admission) ran 1798 s; the others 134 to 409 s. Against round 1's serial sweep the per-suite counts differ only in
elab_guards (155 to 160, the new guard), srp_encoder (1646 to 1659) and srp_top (8703 to 8706).

The SRP campaign's per-arm counts against round 1's campaign at `60094a2` (camp-srp/count-change-vs-60094a2.txt):
only the 12 arms whose README rows were re-measured moved, each because a new row also fails under it; the 10 new
labels are added; none removed. `tools/cmp_counts.py` against every README (camp-srp/cmp-counts.txt): 164 rows equal,
19 differ, all in rows this delta did not add or change and all with the same measured count at `60094a2`: the seven
pre-existing stale counts of `tb/srp_top/README.md` (`pending-peer-ignored`, `mvrp-supersedes-msrp`,
`leaveall-expiry-lost`, `preparation-before-slot`, `mvrp-expiry-only-redraw`, `stale-expiry-honoured`,
`mvrp-stale-expiry-honoured`, as round 1 reported and both reviews confirmed pre-existing) and 12 rows whose tables
record a per-shape or per-group figure the comparator reads as one number (the ten `tf-*` storage arms run at four
shapes, `r-rearm-no-inflight` and `r-rearm-no-deadline` graded on two groups). No row this delta added or changed
differs.

Memory: the unit stayed under 10 GB but for two page-cache peaks (10.2 and 11.4 GB) while the SRP campaign, milan_dp,
firmware and AECP builds overlapped (the governor reclaims page cache above 8 GB and caps campaign builds at -j1 while
anon is above 6.5 GB); to stay under 10 GB the maap/adp/aecp_cmds/elab campaign chain was paused (SIGSTOP) from 17:05
to 17:15 and resumed (SIGCONT). Those drivers have no wall-clock budget (no `timeout` in their sources), so the pause
cannot change a verdict.

## Scratch-parent consumer gate (milan-fpga dev `ac0a01e3`, protocol-processor pinned at `84f6d6a`)

A fresh clone of `$LANES/trusted-dev-20261109-ac0a01e3` (dev `ac0a01e3`, clean) at
`$VALIDATION_STORAGE/scratch/pp216-parent`, branch `pp216-scratch-consumer`, push URL disabled, submodules from the trusted
copy; two local commits, never pushed: `04c5d65246` the gitlink at `84f6d6a`, `a87a71e582` `syn/yosys/rom_digests.tsv`
re-recorded by `syn/yosys/ooc.sh --record-rom-digests` (two rows for the pin, parent-rom-digests-84f6d6a.log;
parent-pin-84f6d6a.txt). The commands are the rtl-fast workflow's run steps, plus milan_dp and the docs workflow's
gates that read the processor tree (`tools/parent-gates.sh`, jobs 3 or 4). All 40 gates return rc 0
(receipts/parent-84f6d6a).

| Job | Gates (each rc 0) | Result |
|---|---|---|
| milan_dp | `make -C tb/verilator/milan_dp SIM_JOBS=2` | 19 `RESULT: PASS`, 12,075 `[ok]`, 0 FAIL (milan_dp-summary.txt) |
| firmware-srp-mutants (the SRP campaigns) | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 3 --shard 3/4` | `test_ctrl_firmware: PASS` |
| firmware-control-mutants | the same, `--shard 1/4` | `mutants: 523 of 523 caught`, `test_ctrl_firmware: PASS` |
| firmware-aecp-mutants | the same, `--shard 2/4` | `test_ctrl_firmware: PASS` |
| firmware-unit | `tally_selftest.py`, `ci_rv32_sdk_selftest.py`, `fw_rv32_selftest.py`, `--shard 0/4`, `test_ctrl_nvm.py`, `fw_coverage.py --selftest`, `fw_coverage.py --check` | PASS; `saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests`; `firmware coverage: PASS (30 files)` |
| firmware-boundary, firmware-verilator | `ctrl_boundary.py --require-rv32 --selftest --without verilator`, `--only verilator` | `ctrl_boundary: PASS` each |
| changes | `ci_scope.py --selftest`; the diff against `ac0a01e3` classified | `selftest: PASS`; `col-processor` |
| verilator-lint | `lint_rtl.py --check --self-test`, `pp_srcs.py --check --selftest` | `LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off)` |
| bdd-conformance | `behave --no-capture -f plain` | 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| yosys-elaboration | `syn/yosys/run.sh --mode elaborate ...`, the OOC read sets and baseline, `ooc_selftest.py`, `guard_selftest.py`, `cache_selftest.py` | `RESULT: PASS`; resource gate `baseline PASS: 3 endpoints`, `all 236 mutants fail`; `75 arm(s) passed`; `36 controls passed`; `cache selftest: OK` |
| publication-census | `publication_census.py --check --selftest --jobs 4` | `RESULT: PASS`; `0 of 120 arm(s) failed`; `mutations: 0 of 31 rule(s) no arm proves` |
| docs ratchets | `docs_check.py`, `check_hygiene.py`, `measure_fail_fast.py`, `measure_test_evidence.py`, `measure_naming.py`, `check_doc_paths.py`, `check_port_contracts.py`, `check_rtl_source_lists.py` | each OK or PASS (`check_port_contracts`: protocol-processor 1788 ports, the new `KL_srp_vlan.link_up_i` documented) |
| idiom | `check_{cpp,py,sv,sh}_idiom.py` and each `--selftest` | each OK; selftests 75, 54, 55, 48 checks PASS |

## Two-placement simulation (milan-fpga #665), with this head pinned

A fresh scratch copy of the #665 lane (`$LANES/665-s6b-cosim`, branch `665-s6b-cosim` at `a88772f1`, read
only: not edited, still clean at `a88772f1` after the run) at `$VALIDATION_STORAGE/scratch/pp216-twin`, push URL disabled,
with protocol-processor at `84f6d6a` and its ROM digests re-recorded through the recorder, committed locally
(`2492225f0d`, `82622f3242`), never pushed. `make -C tb/verilator/milan_dp twin` returns rc 2 (twin_compare.py exits
1) on exactly the three owed rows of this defect, each reporting the defect has gone (receipts/twin-84f6d6a):

```
[DIFF] owed row fabric-mvrp-leave-all: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#857 (a release-image defect)) deletes the row
[DIFF] owed row fabric-domain-one-new: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
[DIFF] owed row fabric-vid2-join-in: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
twin: 3 finding(s); counts {'all-fabric': {'ACMP': 7, 'ADP': 12, 'AECP': 53, 'MAAP': 8, 'MSRP': 88, 'MVRP': 24}, 'split': {'ACMP': 7, 'ADP': 13, 'AECP': 49, 'MAAP': 8, 'MSRP': 91, 'MVRP': 92}}
```

The other owed rows hold (`[OWED]` stream-output-0-notices, split-talker-failed, and entity-available-index for
#217); none is this issue's. The record equals round 1's, frame counts included (the twin does not bounce the link).
The three rows live in the #665 lane and are deleted on the parent side when this head is adopted.

## Acceptance (issue #216)

| Item | Met by |
|---|---|
| Each Applicant (MSRP Domain, Talker Advertise, Listener; MVRP) sends New on two tx! after New!, then the Join | AP1 (Domain), AP2 (VID 2), AP4 (Talker Advertise, Listener Ready); after a link bounce AP8 (VID 2) |
| sJ follows the Registrar: JoinIn only when IN, else JoinMt | AP3, AP8 (no JoinIn across a link change); encoder V3, VR1, VR2, VR10, VR14 to VR16 |
| The LeaveAll state machine runs with nothing declared, within Milan v1.2 Table 4.3, for MVRP and MSRP | AP5 (from Begin!), AP6 (every declaration withdrawn) |
| Tests: the Domain and VID 2 with no peer, New, New, then JoinMt; LeaveAll within 15.5 s and again; the three planted mutants fail | AP1, AP2, AP6; `domain-one-new`, `vlan-one-new`, `vlan-joinin-registrar-mt`, `mvrp-leaveall-needs-content`, each KILLED at the head |
| F10.2 and the section 6.1 text updated; MRP timers unchanged | 10 6.1 and F10.2 (round 1), 6.2 and F10.3 (both rounds); no timer value changed |
| The parent's gates that read SRP and MVRP pass on a scratch parent with this head pinned | the table above, 40 of 40 rc 0 |
