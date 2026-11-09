[R802] NEGATIVE - exact head 60094a268c0df46703a3bee08c94118153634fd9

# R802-1: external independent review of processor issue #216 / PR #218

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #218 (closes #216; parent issues kebag-logic/milan-fpga#860 and #857).
- Exact head `60094a268c0df46703a3bee08c94118153634fd9`, tree `4e9a67dac4d0d27d2a3022578e67d13ec1a7510f`, source base `044cb25f4ed2187bd238490650e73d5d189855d1` (ancestor of the head; six commits).
- Reconstructed in this order: README and docs/README (the repository has no AGENTS.md or CONTRIBUTING.md); the issue body (frozen acceptance) and its two comments (TAKEN, REVIEW READY); the PR body; IEEE 802.1Q-2018 10.7.6.3, 10.7.7 Table 10-3, Table 10-4, 10.7.9 Table 10-5 and Milan v1.2 Table 4.3 as cited; `git diff 044cb25f..60094a2` and its history; then the public evidence tree kebag-logic/milan-fpga@8844ce1c `review-evidence/pp216-r1` (author handoff, gate receipts, parent and two-placement receipts).
- Prior public review findings: none had been published when this independent pass was made (the PR then carried only the two review-start notes, zero PR reviews and zero review comments). After this verdict and ledger were written, the internal review's report R801-1 (NEGATIVE, published 12:44Z) appeared on the PR. Its three findings are resolved at this head in the section "Public findings of R801-1, resolved at this head" below.

## Verdict

NEGATIVE. The three issue defects are fixed at this head and every acceptance arm is planted and killed, but the new per-VID Registrar ignores link changes (F1, MAJOR): after a LINK_DOWN / LINK_UP it keeps IN, and VID 2 goes out as JoinIn with nothing registered on the restored link, which is the issue's defect 2 symptom in a path no check or arm holds. One figure in a README row added by this delta is wrong (F2, MINOR).

## Findings

### F1 - MAJOR - the VID Registrar keeps IN across LINK_DOWN / LINK_UP, so VIDs send JoinIn with nothing registered

- Lenses: Conformance, RTL, Robustness, Tests, Docs.
- Where: `hdl/srp/KL_srp_vlan.sv:59-106` (the port list has no link input), `hdl/srp/KL_srp_vlan.sv:252-262` (`reg_nx_w`: rLA!/txLA!, registering events and rLv! only, no Begin!/Flush! term), `hdl/srp/KL_srp_top.sv:463-490` (`u_vlan` receives no `link_up_i`). Contrast `hdl/srp/KL_srp_domain.sv:284-295` (LINK_DOWN: "Flush!: every Registrar to MT"; LINK_UP: Begin!) and `docs/architecture/10_srp_engine.md:420` (Domain: "LINK_UP (Begin!) or LINK_DOWN (Flush!) | MT | JoinMt"), and the engine rule at `10_srp_engine.md:961-965` (issue #212: a link change takes every sink registrar to MT). `10_srp_engine.md:481-501` (section 6.2, the VID Registrar) says nothing about link changes.
- Authority: IEEE 802.1Q-2018 Table 10-4 (Begin! and Flush! take the Registrar to MT) as this engine maps LINK_UP to Begin! and LINK_DOWN to Flush!; 10.7.6.3 (sJ is JoinIn only with the Registrar IN); issue #216 acceptance "sJ follows the Registrar: JoinIn only when IN, else JoinMt". The Domain already has the arm `domain-link-keeps-registrar` (encoder DR11); the VID Registrar, new in this delta, has no counterpart.
- Evidence (reviewer probe, testbench-only, `probes/r802-link-bounce.tb.patch`, log `probes/r802-link-bounce.log`, rc 2): DECLARE_TALKER on VID 2, a peer JoinIn of VID 2 (Registrar IN), then link down at 3750 ms and up at 3780 ms:
  ```
  R802LINK before: New@401 New@601 JoinMt@801 JoinMt@1001 JoinMt@2001 JoinIn@3001
  R802LINK VID 2 after LINK_UP: JoinIn@4001 JoinIn@5001 JoinIn@6001
  R802LINK Domain after LINK_UP: New@3802 New@4002 JoinMt@4203 JoinMt@5203 JoinMt@6203
  FAIL: R802LINK: after LINK_DOWN (Flush!) and LINK_UP (Begin!) VID 2's Registrar is MT, so no JoinIn (3 JoinIn: ...)
  ```
  The Domain restarts as specified; VID 2 claims a registration it has not seen on the new link.
- Impact: after every link bounce each held VID is declared JoinIn until the next own or peer LeaveAll ages the Registrar (up to about 15.5 s) or a peer Lv arrives; a new link partner that does not declare the VID is told it is registered. No row of `tb/srp_top` or `tb/srp_encoder` exercises a VID across a link change, so the campaign cannot see it. (The VID Applicants also take no Begin! at LINK_UP; that matches the talker stream Applicants, which have no link input either, so it is pre-existing scope and not counted here, but the fix should decide it explicitly.)
- Required outcome: the VID Registrar takes LINK_DOWN and LINK_UP to MT, as the Domain's does (a link input to `KL_srp_vlan`, wired in `KL_srp_top`); a check that holds it (for example an `applicant` row: Registrar IN, link bounce, the next VID 2 sJ is JoinMt) and a planted arm that fails that check by name; 10 section 6.2 (and F10.3 if it changes) records the link behaviour. If the maintainer instead accepts the behaviour, 10 section 6.2 records the deviation with its authority, and the issue's acceptance wording is reconciled with it.
- Verification: the probe above (or its in-tree successor) passes at the fixed head; the new arm fails it in `make -C tb/srp_top mutants`; the full campaign stays green with its coverage check.

### F2 - MINOR - a new README row records 7 failing checks where the arm fails 8 (= R801-1-F01, found independently, retained)

- Lenses: Docs, Tests.
- Where: `tb/srp_encoder/README.md:255` (added by `3da1427`): "`vlan-rejoin-of-leaving-allocates` ... | V10 | 7 FAIL - V10, W4, W5 (two), B1 (three)".
- Evidence: this review's delta campaign (`receipts/camp-srp-delta.log`, arm log `receipts/camp-srp-delta-out/vlan-rejoin-of-leaving-allocates.log`) and the author's own head campaign receipt (`head-60094a2/camp-srp/camp-srp.log` in the public evidence) both measure `failures=8`: V10, W4, W5 twice, and B1 four times ("B1 one Domain and one VLAN re-join bridged got 1 0", "B1 VLAN frame captured", "B1-vlan: length got 30 exp 26", "B1-vlan: byte-exact against the independent packer"). `receipts/cmp_counts.txt` compares the count recorded for every row the delta's 54 arms grade, 71 rows. Three differ. This is the only one in a row the delta added or changed; the other two (`leaveall-expiry-lost` 18 against 16, `mvrp-stale-expiry-honoured` 1 against 7) are pre-existing table rows of point 7b, whose re-measured values the README already records.
- Impact: a recorded measurement is wrong (a figure, so not wording-only residue).
- Required outcome: "8 FAIL - V10, W4, W5 (two), B1 (four)".
- Verification: `scripts/cmp_counts.py` over a campaign log at the fixed head reports no differing row that the delta added or changed.

### S1 - SUGGESTION - three Table 10-3 cells of the shared Applicant are not distinguished by any check

- Lens: Tests.
- Where: `hdl/srp/srp_pkg.sv:145` (note 4: rJoinIn! ignored in VP when point-to-point), `:192` (txLA! from VP goes to AA), `:244` (txLA! from VP sends s).
- Evidence: reviewer probes `p09-note4-inverted`, `p12-txla-vp-stays`, `p19-txla-vp-sends-sj` survive every `tb/srp_top` group (applicant, domjoin, join, onevec, then armdelay, phases, edge, peer, congestion, guards, restart, timers, lvleave, lvcoll, share, link) and `tb/srp_encoder` (`probes/*-allgroups.result`). The `tb/srp_top` DJ3 case "with JoinIn, which leaves VP alone (note 4)" passes under the note-4 inversion, because VP and AP both send sJ at the next tx!; only the number of Joins that follow differs. 16 of the 19 probes on the shared rows were killed.
- Not required by the issue's acceptance (every acceptance arm exists and is killed). Suggested: a check that counts the Joins after a peer LeaveAll riding a JoinIn (two from VP with p2p, one from AP), and one for an own LeaveAll tx! that finds the Domain or a VID in VP (s, then AA).

### S2 - SUGGESTION - the MVRP round can stall if `N_VIDS_P` exceeds `ENC_DEPTH_P`

- Lenses: RTL, Robustness.
- Where: `hdl/srp/KL_srp_top.sv:1212-1230` (the MVRP drain waits for the VID walk's `tx_done_o`), `hdl/srp/KL_srp_vlan.sv` W_PUSH (the walk holds each message until the encoder takes it), `hdl/srp/KL_srp_encoder.sv:415-417` (a full MVRP table refuses a new value). There is no MVRP high-water drain.
- With more held VIDs than encoder entries the walk would wait for a drain that waits for the walk. The defaults (4 and 12) are safe and the processor top does not override either, so this is not reachable in the shipped configuration; an elaboration guard (`N_VIDS_P <= ENC_DEPTH_P`) in `KL_srp_top` would keep it so.

### R1 - RESIDUE - section 6.5 copies a timing value outside F08.1 (= R801-1-F02, retained)

- Lens: Docs.
- Where: `docs/architecture/10_srp_engine.md:1116-1117`, new in `3da1427`: "So the MVRP participant sends a LeaveAll every 10 to 15 s from Begin!".
- Authority: `docs/README.md` section 2, single-source rules ("Timing values only in `F08.1`"). The value is the correct one (`08_timing.md` F08.1 row T-MRP-LEAVEALL, "random 10–15 s"), so this is wording only. It changes no figure, test, code or clause claim.
- Exact fix: replace "every 10 to 15 s from Begin!" with "every `T-MRP-LEAVEALL` ([F08.1](08_timing.md#fig-08-constants)) from Begin!". The relative link resolves in the repository; the link in R801-1's fix text points to a copy inside the evidence tree instead.
- It does not make the verdict negative and leaves no lens unclean; it goes to the residue checklist.

### S3 - SUGGESTION - a VID registered by a peer before the first user's join is first answered JoinMt (= R801-1-F03, retained as SUGGESTION)

- Lenses: Conformance, Docs.
- Where: `hdl/srp/KL_srp_vlan.sv:391` (a new entry's Registrar starts MT) and `:410` (a VO/AO/QO entry with no user is discarded with its Registrar); disclosed at `docs/architecture/10_srp_engine.md:494-497`.
- Assessment: confirmed by reading the code. The deviation runs in the conservative direction: JoinMt where a full Table 10-4 Registrar would read IN, never JoinIn without IN. It is corrected at the peer's next declaration, and section 6.2 states it. The acceptance item "JoinIn only when IN" holds. I agree it stays a SUGGESTION, with the clause basis made precise: Table 10-3 note 11 covers discarding Applicant state, not a Registrar that would be IN. Contrast F1, which is the non-conservative direction (JoinIn without IN) and is an open finding.

## Public findings of R801-1, resolved at this head

| R801-1 finding | Severity there | Resolution here |
|---|---|---|
| F01 `tb/srp_encoder/README.md:255` records 7 where the arm fails 8 | MINOR | Retained: independently reproduced as F2 (my delta campaign `failures=8`; `receipts/cmp_counts.txt`) |
| F02 section 6.5 "every 10 to 15 s" outside F08.1 | RESIDUE | Retained as R1, with the in-repo link in the exact fix |
| F03 the VID Registrar exists only from the first user's join | SUGGESTION | Retained as S3, SUGGESTION |

R801-1 records Robustness CLEAN, LINK_DOWN/UP mid-round included. This review's F1 is a finding R801-1 does not carry: the probe shows the VID Registrar surviving a link bounce IN.

## The seven review points

1. New on two transmit opportunities, then Join (Table 10-3). Code: `srp_pkg.sv:115-201` matches the printed Table 10-3 rows for New!, Lv!, rJoinIn! (note 4), rIn! (note 5), rJoinMt!/rMt!, rLv!/rLA!, periodic!, tx! (note 8 at AN) and txLA!, and `srp_app_msg` (`:225-251`) sends New from VN and AN, sJ from VP/AA/AP, sL from LA, s from LO, nothing in the bracketed optional cells. The Domain enters VN at LINK_UP and at adoption (`KL_srp_domain.sv`); each VID enters VN at its first user (`KL_srp_vlan.sv`); Talker Advertise and Listener are unchanged and already follow it. Wire evidence at this head: AP1 (Domain), AP2 (VID 2), AP4 (Talker Advertise, Listener Ready) each New, New, then JoinMt 180-240 ms apart, first within 240 ms; `tb/pp_top` S1 byte-exact. Met.
2. sJ by the Registrar. `srp_app_msg` encodes sJ and s against the Registrar read after the clock's events; VID Registrar per Table 10-4 (MVRP as printed). AP3 (JoinMt with MT, JoinIn after the peer's JoinIn, JoinMt after its Lv), encoder V3 and VR1-VR11. Met in steady state; not met across a link change (F1).
3. LeaveAll with nothing declared. An own MVRP expiry makes the machine Active and the next MVRP tx! is its sLA whether or not a VID is held (`KL_srp_top.sv:1212-1230, 1304-1308`); the encoder starts an MVRP drain for the LeaveAll alone (`KL_srp_encoder.sv:406-410`), the LeaveAll-only MVRPDU. AP5 (from Begin!) and AP6 (every declaration withdrawn) require the first MVRP and MSRP LeaveAll within 15.5 s and each next 9.5-15.5 s, byte-exact for MVRP. My probe `p16-mvrp-leaveall-no-redraw` (no redraw after the first expiry) is killed by them. Met.
4. MRP timers unchanged. The delta touches no timer value: `docs/architecture/08_timing.md`, `hdl/common` and `hdl/top` are untouched, `KL_srp_top`'s ports and parameters are identical, and no timer constant appears in the HDL diff. Met.
5. Planted arms. `domain-one-new`, `vlan-one-new` (one New), `vlan-joinin-registrar-mt` (JoinIn with the Registrar MT) and `mvrp-leaveall-needs-content` (LeaveAll stopped with nothing to send, the base's encoder condition) each fail their named rows; each plants a behavioural change (a state entered, an encoding input, a drain condition), and the rows read the wire, not a constant. This review re-ran every arm whose patch the delta adds or changes, plus `second-queueing`, `join-displaces-new` and `empty-canceled-pdu`: 54 arms, `81 checks: 81 PASS, 0 FAIL`, every row KILLED (`receipts/camp-srp-delta.log`). Met; S1 lists three cells no check distinguishes.
6. 10 section 6.1 and F10.2 match the code: the ladder, the per-event table (`10_srp_engine.md:388-395`) and the Registrar table (`:415-421`) agree with `srp_pkg.sv` and `KL_srp_domain.sv`. Sections 3, 5.1, 6.2 and 6.5 agree with the code as far as they go; 6.2 is silent on link changes (F1).
7. Parent consumer gates and the two-placement simulation (public receipts, not re-run here): `parent-60094a2` holds 40 gates, each rc 0, on dev `ac0a01e3` with the gitlink at `60094a2` (its pin record) and the ROM digests re-recorded; `twin-60094a2` reports exactly the three owed rows `fabric-mvrp-leave-all`, `fabric-domain-one-new` and `fabric-vid2-join-in` as "the defect has gone" (rc 2 by design until the parent deletes the rows; `entity-available-index` still owed to #217). The twin run does not bounce the link, so it cannot see F1.
   The author's two reported gaps: (a) the full sweep ran serially in one unit instead of four shard units. That is a process note, not a defect or residue: it is the same gate command and it completed rc 0, and this review ran `scripts/run_suites.sh` itself (below). (b) The seven `tb/srp_top/README.md` arm counts (`pending-peer-ignored`, `mvrp-supersedes-msrp`, `leaveall-expiry-lost`, `preparation-before-slot`, `mvrp-expiry-only-redraw`, `stale-expiry-honoured`, `mvrp-stale-expiry-honoured`) are in table rows that predate the base (blame `cf4e5c6`). The README's own later paragraphs (lines 410-413 and 443-447, also before the base) already record the re-measured values (26, 8, 16, 21, 17, 7, 7), which this review's campaign confirms for the two that the delta re-planted (`leaveall-expiry-lost` 16, `mvrp-stale-expiry-honoured` 7). So these are not residue of this delta and not a new instance. They are a pre-existing follow-up. The author's comparison did not cover the encoder README, where F2 is.

Comment rule (owner 2026-10-15): the added lines of the delta (HDL, testbench, scripts, patches) carry no bench lane label, lane name, review round, reviewer ID or issue-comment ID; "lane" in the delta means the per-AttributeType LeaveAll lane. No new instance.

## Gates run by this review at the exact head

Each gate ran in its own fresh clone of the head under the packet's scratch area, with the pinned Verilator 5.050 (identity checked: `Verilator 5.050 2026-07-01 rev v5.050`) first on PATH. Receipts are `receipts/<name>.{cmd,log,rc,start,end}`.

| Gate | Command | rc | Result |
|---|---|---|---|
| docs | `make check` | 0 | ids, figures and every docs target OK |
| matrix | `python3 scripts/gen_matrix.py --check` | 0 | `matrix: OK (94 rows, 0 untested)` |
| HDL lint | `bash scripts/lint_hdl.sh` | 0 | 41 modules `LINT OK` |
| whitespace | `git diff --check 044cb25f HEAD` | 0 | empty |
| portability | `bash syn/yosys/run.sh` | 0 | every top `YOSYS OK`, `YOSYS XILINX OK` |
| portability | `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 2` | 0 | `elab guards: 93 checks: 93 PASS, 0 FAIL` |
| suites | `bash scripts/run_suites.sh` (serial, unmodified) | 0 | 36 suites `PASS`, `suites: 1032092 checks total, 0 failing` (srp_top 8703, srp_encoder 1646, srp_stream_fsms 1512, pp_top 11066), 11:38Z to 12:59Z |
| SRP campaign, delta arms | `python3 -B tb/srp_top/mutants.py --only <54 arms> --jobs 6` | 0 | `81 checks: 81 PASS, 0 FAIL`, every row KILLED |
| reviewer probes | `scripts/run_probes.sh 3`, `scripts/run_escalate.sh 3` | - | 19 Applicant-row probes: 16 KILLED, 3 SURVIVED (S1), the three also survive every other group |
| reviewer link probe | `probes/r802-link-bounce.tb.patch`, `make run RUN_ARGS=r802link` | 2 | F1 reproduced |

The delta campaign replaces a full 288-row campaign run, which I stopped early because the shared host was too loaded (load average above 150 on 8 CPUs) for it to finish in reasonable time. Its partial output is not kept. The full campaign at this head is covered by the author's receipt and by R801-1's own full run: `350 checks: 350 PASS, 0 FAIL`, `assertion coverage: 184/184`.

## Hosted evidence at the exact head (inspected, not owned)

The check runs on `60094a2`: `docs-gates` success (two contexts), `portability` success (two contexts), `suites` in progress in both contexts when read (not completed; no conclusion). No commit status. The manager owns hosted/act acceptance.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1; S3) | `srp_pkg.sv` Applicant rows against Table 10-3 and notes 4, 5, 8; sJ/s against 10.7.6.3/10.7.6.5; Domain and VID Registrars against Table 10-4; the LeaveAll machines against 10.7.9 / Table 10-5 and Milan Table 4.3; the link probe | R802-1 | 60094a268c0df46703a3bee08c94118153634fd9 |
| RTL | UNCLEAN (F1; S2) | the full diffs of `KL_srp_domain.sv`, `KL_srp_vlan.sv`, `KL_srp_top.sv`, `KL_srp_encoder.sv`, `srp_pkg.sv`; lint, Yosys and elab guards rc 0 | R802-1 | 60094a268c0df46703a3bee08c94118153634fd9 |
| Robustness | UNCLEAN (F1; S2) | link bounce, owed tx! and queue-full paths, walk/round hand-shakes, the parameter limits of the MVRP round | R802-1 | 60094a268c0df46703a3bee08c94118153634fd9 |
| Tests | UNCLEAN (F1, F2; S1) | AP1-AP7, `tb/pp_top` S1, encoder D/DT/DA/V/VR rows; 54-arm delta campaign; 19 independent probes plus escalation; count comparison; the suite sweep | R802-1 | 60094a268c0df46703a3bee08c94118153634fd9 |
| Docs | UNCLEAN (F2; F1 for section 6.2; R1 residue) | 10 sections 3, 5, 5.1, 6.1 / F10.2, 6.2 / F10.3, 6.5; 09 sections 8.14, 8.15; the three READMEs; MODULE_MATRIX; the comment rule | R802-1 | 60094a268c0df46703a3bee08c94118153634fd9 |

## Real limits

- IEEE 802.1Q-2018 and Milan v1.2 were checked against the clauses as cited, without a copy of the standards at hand during the review. Two cells were read from the cited text and not independently confirmed: rJoinIn! in LO (the code holds LO) and whether note 8 also applies to txLA! from AN (the code goes to QA).
- The parent consumer gates, the two-placement simulation and the area figures were not re-run here; they are judged from the author's public receipts.
- The full 288-row SRP campaign and the AECP campaigns (`aecp-mutants`, `aecp-dispatch-mutants`) were not re-run; the author's receipts cover them.
- The probes ran against `tb/srp_top` and `tb/srp_encoder` only, not `tb/pp_top`.
- Toolchain: host Python 3.14.9 and sv2v v0.0.13 against CI's 3.12.3 and v0.0.12; Yosys 0.66 as in CI.
- For a few minutes the serial sweep shared its clone with a parallel suite run of mine, which I stopped (its partial outputs are discarded, not published). The suites that overlapped (`name_state`, `nvm_port`, `originator`, `pp_top`, `prng`, `release_merge`) all passed the sweep with counts equal to the author's receipt, `pp_top` 11066 among them. A collision could only have made a build or run fail, never pass with a full tally.
- Physical calibration NOT RUN; field skips are not hardware proof. No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- The current-dev merge candidate (source base `044cb25f`, live dev `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`): builder and native banks at the merge turn, with their receipts linked on the PR.
- Hosted/act acceptance (the `suites` contexts were still in progress when read).
- Carry F1 and F2 to the author; carry R1 to the residue checklist; S1, S2 and S3 are optional.
- Open a follow-up for the pre-existing seven `tb/srp_top/README.md` table counts (point 7b); they do not belong to this PR.
- On the parent side, delete the three owed twin rows when this head is adopted.

R802-1 FINISHED
