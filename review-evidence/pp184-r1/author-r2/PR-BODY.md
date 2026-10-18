[A648] MSRP Domain re-join: JoinIn only while the declared Domain is registered, JoinMt otherwise (#184)

Closes #184

## What was wrong

`KL_srp_domain` encoded every periodic and LeaveAll re-declaration of the Class A Domain as
JoinIn and never looked at a Domain registration. IEEE 802.1Q-2018 10.7.6.3 (sJ) encodes
JoinIn only while the Registrar of the attribute is IN, and JoinMt in MT or LV. With no
other station declaring a Domain, the re-join must be JoinMt.

## What changes

- `hdl/srp/KL_srp_domain.sv` keeps a one-bit Registrar for its declared value. A received
  New, JoinIn or JoinMt of that value sets IN. Its Lv clears IN at once (Milan v1.2
  4.2.7.2.2, the instantaneous IN to MT). A LeaveAll, received on the Domain lane or the
  own sLA, clears IN to LV. LINK_UP and LINK_DOWN clear it. An adoption carries the adopted
  value's registration. LV is folded into MT, because sJ encodes the two alike and nothing
  else reads the Domain registration (802.1Q-2018 35.2.4: no MAP for the Domain). So no
  leavetimer is added.
- The re-join is JoinIn if the Registrar is IN, JoinMt otherwise. Periodic and
  own-LeaveAll re-joins are made pending at once, as before. A received LeaveAll's re-join
  waits for the next MSRP tx! opportunity, so a bridge that re-declares its Domain after
  its LeaveAll in the same MRPDU is normally answered JoinIn (a received LeaveAll on a tx!
  clock, or a tx! inside the peer's MRPDU, gives JoinMt, as sJ gives for the LV Registrar
  at that tx!). When a pending re-join is serviced, the code is snapshotted from the
  previously registered state into the Domain event queue. That queued event keeps its
  encoding until the encoder accepts it, also if a peer event arrives while it waits, and
  encoder or TX backpressure can extend the drain. The single New at startup and LINK_UP
  is unchanged.
- `hdl/srp/KL_srp_top.sv` drives two new inputs of `KL_srp_domain`: the Domain Lv strobe
  from the decoder, and the tx! opportunity (`join_fsm_w`).
- No register-map change. No top-level port or parameter change: `protocol_processor_top`
  and `KL_srp_top` keep their ports and parameters. `KL_srp_domain` gains two inputs.

## Tests

- `tb/srp_encoder` DR1 to DR11 (12 checks, with DR3a): no peer gives JoinMt; a peer
  declaring gives JoinIn; a peer LeaveAll followed by its Domain before tx! gives JoinIn;
  the own LeaveAll gives JoinMt (LV); LV re-joins JoinMt until the peer re-declares; the
  peer's Lv gives JoinMt on the very next re-join; an Lv of another value changes nothing;
  a received event wins over a LeaveAll in the same clock; adoption carries the
  registration, also when the adoption is withdrawn before it applies; LINK_DOWN and
  LINK_UP clear it. D2, D3, D8 and B1 move to the encoding this rule gives.
- `tb/srp_top` group `domjoin` DJ1 to DJ4, end to end through the decoder, cadence and
  encoder: no peer (JoinMt), peer declaring (JoinIn), a peer LeaveAll MRPDU re-declaring
  the Domain (JoinIn), and the peer's withdrawal (JoinMt on the next re-join). Q2, F1 and
  the F5c negatives follow the same rule.
- 15 planted mutants in `tb/srp_top/mutations/`, run by `tb/srp_top/mutants.py`. Each must
  fail its named check: every new check has at least one. The campaign's assertion coverage
  now also requires DJ1 to DJ4.

## Records

Base is processor main 08ae0013, head is this branch's single commit. Same pinned tools
on both sides (Verilator 5.050, sv2v 0.0.12, Yosys 0.66).

| Gate | Base | Head |
|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,030,000 checks | rc 0, 1,030,016 (+12 srp_encoder, +4 srp_top) |
| `check-req-tags.py` executed half | rc 0, 226 evidence lines | rc 0, 227 (+REQ-SRP-005 on DR6) |
| `scripts/lint_hdl.sh` | rc 0 | rc 0, identical |
| `make check` | rc 0 | rc 0 (links +6, tags +1, ID-scanned files +15) |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0, identical |
| `syn/yosys/run.sh` | rc 0 | rc 0 (only `all.v` line numbers move) |
| `tb/elab_guards/guards.py --frontend yosys` | rc 0, 93/93 | rc 0, 93/93 |

Every campaign that builds a changed file is rc 0 at both: `tb/srp_top/mutants.py` (137 ->
159 checks, assertion coverage 86/86 -> 90/90; the 130 existing receipts have identical
failing sets), `tb/srp_admission`, and in `tb/pp_top` the aecp, aecp-dispatch, ctr, notify
(98/98, including the Domain adoption arms), gsi, name-write, acmp and d3 campaigns, plus
adp_engine, maap, name_state and the elaboration-guard mutants. Each has identical verdicts
and failing sets at base and head.

Consumer gates on a scratch parent at milan-fpga dev e9cbb676 with the gitlink at base and at
head, with the #180 evidence-classification and #176 milan_dp #67 patches applied: the same
verdicts and tallies at both, including BDD (14 features, 406 scenarios), pp_shadow, nvm_cosim,
milan_dp (all legs), milan_dp_render, the builder and xvlog. Expected differences: two more
documented ports, and the unchanged ROM digests recorded for the new pin. `check_submodule_docs`
fails identically at base and head, as it does for any moved pin until an adoption re-records it.

Area: `KL_srp_domain` alone grows by 3 flip-flops and 1 LUT. The parent's whole-design OOC
price of the processor moves from 56,150 to 55,878 LUT and from 26,293 to 26,284 FF, which is
synthesis variation; every other resource column is unchanged.

## Documentation

`docs/architecture/10_srp_engine.md`: F10.2 and the new "Re-join encoding" paragraph in
6.1, the singleton state in 5, and the Domain row of the 6.5 lane table. Suite READMEs of
`tb/srp_encoder` and `tb/srp_top`. `tb/pp_top/README.md` line citations of the Domain
strobe follow the moved lines.

## Round 2

Head 88cb2061: a merge of processor main 5addf297 (no conflicts) and one docs-and-comments
commit. No RTL logic change: `KL_srp_domain.sv` without comments is identical to round 1.
No register map, port, parameter, generator or ROM change.

- **Re-join sampling boundary (review F1).** `docs/architecture/10_srp_engine.md` 6.1 now
  says, in the review's words, that a serviced re-join snapshots the previously registered
  state into the Domain event queue, keeps that encoding until the encoder accepts it (also
  if a peer event arrives while it waits), that a receive on the enqueue edge updates the
  registrar for later re-joins, and that backpressure can extend the drain. The claims
  "chosen at hand-over" and "at most one T-MRP-JOIN" are gone. The `KL_srp_domain.sv` banner
  and this description's second "What changes" bullet say the same.
- **Timing sentence (review RS1).** The received-LeaveAll sentence is the review's exact
  text: a later declaration *normally* registers first. A received LeaveAll on a tx! clock,
  or a tx! inside the peer's MRPDU, gives JoinMt, as sJ gives for the LV Registrar at that
  tx!. The optional `:208` comment wording is applied too.
- Followers: two `tb/pp_top/README.md` line citations move by +2. The 12 `domain-*`
  mutation patches get new hunk offsets, and two of them a new context line; the planted
  defects are unchanged. One `tb/srp_encoder/README.md` sentence no longer says "handed to
  the encoder".
- **Receipt index (review RS2).** The round-2 receipts are published with an index
  generated from the files, including the Domain area receipts that the round-1 index
  named: `KL_srp_domain` alone has 116 -> 119 FF and 130 -> 131 LUT (FDRE 113 -> 116, FDSE 3).
- **Review S1 (optional) is not taken.** It would add tests and campaign arms to a round
  that is scoped as docs only.
- A standalone probe of `KL_srp_domain` checks the corrected text against the RTL:
  12/12 PASS at this head and at round 1's. Three planted mutants each fail their named
  checks: the queued code follows the registrar while waiting, the enqueue uses the next
  state, and the queue pops without acceptance.

| Gate (round 2) | Base main 5addf297 | Head 88cb2061 |
|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,030,013 checks | rc 0, 1,030,029 (+12 srp_encoder, +4 srp_top) |
| `check-req-tags.py` executed half | rc 0, 227 | rc 0, 228 |
| `scripts/lint_hdl.sh` | rc 0 | rc 0, identical |
| `make check` | rc 0 | rc 0 (links +6, tags +1, ID files +15) |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0, identical |
| `syn/yosys/run.sh` | rc 0 | rc 0 (only `all.v` line numbers move) |
| `tb/elab_guards/guards.py --frontend yosys` | rc 0, 93/93 | rc 0, 93/93 |

The same 14 campaigns as round 1 are rc 0 at both: srp_top 137 -> 159 with coverage 86/86 ->
90/90; the head output is identical to round 1's. The others have identical verdicts and
failing sets at base and head: srp_admission; in `tb/pp_top`, aecp, aecp-dispatch, ctr,
notify (now 109/109 with #181's arms), gsi, name-write, acmp and d3; plus adp_engine, maap,
name_state and the elaboration-guard mutants. The parent consumer gates were not rerun in
this round. Round 1's table, at gitlink e11fb36b, still applies to the registrar change, and
the current-dev merge candidate is validated at merge time.
