# HANDOFF r1: [A817] #969 split SRP listener never declares when the Talker was registered before the binding settled

Status: **REVIEW READY** (14:55 CET 2026-11-22) at `f863258d`. Every gate is done and green (gate table below):
the firmware gate's four shards with plants, coverage, the ledger, the twin and its plants, the CPU budget graders,
the docs workflow, and the routes at 1x1/1if and 8x8/1if (the #818 floor met with the first directive). Nothing of
this lane is running. Open: the reviews; the bench re-run after merge (the manager's).

Lane: `/data-2/milan/lanes/fix-969`, branch `pf-969-1` from `dd163e41` (PR #960 reviewed head). Local commits only;
nothing pushed. Scratch: `/data-2/milan/tmp/969-a817`.
TAKEN posted: #969 issuecomment-7077075041 (text: posts/TAKEN-COMMENT.md).
REVIEW READY posted: #969 issuecomment-7080057766 (text: REVIEW-READY.md).

## Cause (proved by the failing-first run)

ACMP initiates the SRP reservation only at PROBE_TX_RESPONSE SUCCESS (Milan v1.2 5.5.3.5.18 step 4;
`third_party/tsn-c-stack/src/acmp.c` probe_response -> p_srp). Until then the sink has no SRP binding, and the MSRP
receive filter (`sw/firmware/ctrl/srp/srp_mbx.c` interested_msrp) refused every Talker attribute of a StreamID no
binding holds, before lwSRP allocates anything (`third_party/lwSRP/src/core/mrp_mad.c:998`). The registrar never held
a Talker declared before the binding, so the walk a binding owes found nothing, and the talker's applicant stays QA
(quiet) until a LeaveAll (IEEE 802.1Q-2018 Table 10-3). UNBIND_RX then BIND_RX works because the old binding's
registration is still held. Neither pointer in the issue (registered_kinds' start, the destination/VID match) is the
cause: the walk would have taken the registration had the registrar held it. The release processor already keeps
N port registrars for this (`KL_srp_listener_fsm.sv`, protocol-processor #212); the split firmware did not.

## Design (as committed)

- The filter keeps a Talker of a StreamID none of the interface's bindings holds: one already kept, or while the
  interface keeps fewer than `SRP_KEPT_TALKERS` (= `CTRL_SRP_SINKS`, the processor's count). Past the bound the old
  behaviour (ignored until the talker's next declaration).
- `kept_count` is counted again before a receive, outside lwSRP's callbacks (`count_kept`), only when a binding
  changed since the last count, or at the bound when a block was returned; the filter adds one per kept. The count
  counts every Talker the participant does not declare (VO/AO/QO/LO) whose StreamID no binding holds, registered or
  left with its block unfreed. The walk reads and writes nothing of it, so #930's walk schedule moves no filter answer
  (the srp_listeners differential holds it; a first design counted in the walk and that differential refused it).
- The pool is unchanged: the fixed 16 medium blocks per interface fund the kept (static assert
  `SRP_KEPT_TALKERS + SRP_POOL_DOMAIN_BLOCKS <= SRP_POOL_FIXED_BLOCKS`). Growing the pool by K blocks would have taken
  the 8x8/1if size fixture (the split SoC's stand-in, no ledger entry) past 56 RAMB36: +2,784 B of sram, 1,376 B slack.
- A StreamID no binding holds is held (#925's `srp_held`) from a registration it is kept for, with the latest kind, so
  a binding made later takes the latest of two kinds. `SRP_HELD_STREAMS` grows by half the kept bound.
- An unbound StreamID's Talker indication owes no walk (`i->stale = i->stale || bound`).
- Placement: no hot-list function moves or changes size (the kept tables sit before `held`, which stays the struct's
  last member: with it not last GCC compiled reset_interface's held loop 12 B shorter, moving the hot code after it).
  The cold code after the changed functions moves (54 symbols: the rest of srp_mbx.o and lwSRP's objects).

## Commits (one-line subjects, no body, no trailers)

| # | Commit | What |
|---|---|---|
| 1 | `6a941bec` | tests: `SrpEarlyTalker.*` (srp_mbx.cpp), `Early.S13`, `Early.S14` (test_plat_sinks.cpp); two old tests restated |
| 2 | `12c5908a` | fix (first form) |
| 3 | `bd08d206` | tests: the JoinIn replacement case; base-compatible restated pool check |
| 4 | `1ed84f6b` | the binding's walk mark restored as the campaigns anchor it |
| 5 | `23a4e7f0` | tests: the bound against a count and a New of the other kind; binding-first at the bound; a kept one that left |
| 6 | `6bcc1c65` | plants: `srp_early_mutants.py`, the platform's `early-talker-ignored`; two plants re-anchored |
| 7 | `e24e6ed4` | docs: srp/README.md, plat/README.md |
| 8 | `c16161c6` | the count before each receive, not in the walk; the pool's fixed blocks fund the kept |
| 9 | `954e5572` | held stays last in `struct srp_mbx` |
| 10 | `67984b77` | ledger: platform 8x8/1if 58.5, 8x8/2if 63.5 (owner's rule of 2026-11-15), ctrl_plat as measured |
| 11 | `f6f83166` | memory test, design doc, READMEs for the ledger |
| 12 | `b56664fe` | the filter's unreachable Talker-type test dropped (an uncovered branch); tests: count past the bound, full held table |
| 13 | `4c5018eb` | the plants' module docstring wrapped (Python idiom gate) |
| 14 | `aca559e3` | the rom figures as the final firmware links them (24 B less, same tiles) |
| 15 | `e4518a0f` | adapter comments wrapped within 120 columns (the images' bytes unchanged) |
| 16 | `c6ef2329` | srp_mbx.c's coverage ratchet line: 854/854 lines, 773/773 branches |
| 17 | `f863258d` | the two kept-Talker comment lines `e4518a0f` left past 120 columns, wrapped with no line moved (the images' bytes unchanged) |

## Changes (file:line at the final head `f863258d`, reason)

| File:line | Reason |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.c:29` | static assertions: the pool's fixed blocks fund the kept beside the Domain's; kept_count fits a byte |
| `srp_mbx.c:260` `talker_changed` | an unbound StreamID's indication owes no walk (`:279`); a StreamID no binding holds is held with its latest kind from a registration it is kept for (`:286`), the #925 ruling for a binding made later |
| `srp_mbx.c:448` `talker_kind`, `:460` `keep_talker` | the filter keeps a Talker no binding holds while under `SRP_KEPT_TALKERS` (or already kept); past it, the old behaviour |
| `srp_mbx.c:518` `interested_msrp` | the Talker branch's last answer is `keep_talker`'s |
| `srp_mbx.c:807` `srp_mbx_bind` | a binding change owes the next receive's count |
| `srp_mbx.c:908-956` `SRP_UNDECLARED_APPL`, `bound_stream`, `kept_visited`, `count_kept` | the count before a receive, outside lwSRP's callbacks, only when a binding changed or at the bound when a block was returned: every undeclared Talker no binding holds, registered or not yet freed |
| `srp_mbx.c:975` `apply_receive` | calls `count_kept` after the snapshot, before `mrp_rx` |
| `srp_mbx.c:1438` `poll` | the retained receive's retry argument: the kept change only with the filter's answers or a count a returned block owes |
| `sw/firmware/ctrl/srp/srp_mbx.h:136-146` | `SRP_KEPT_TALKERS`, `struct srp_kept`, the pool's fixed and Domain blocks named, the pool unchanged |
| `srp_mbx.h:161` | `SRP_HELD_STREAMS` grows by half the kept bound (a held StreamID with one kind has a kept registration) |
| `srp_mbx.h:207` | the kept tables before `held`, which stays last (the hot code compiles as at the base) |
| `sw/firmware/ctrl/srp/README.md` | pool, filter, observation, held, the kept Talkers paragraph, D4 (processor #212) |
| `sw/firmware/ctrl/test/srp_mbx.cpp:603, :2048` | restated for the new contract (an unbound Talker takes a block; a held stream ends by an unanswered LeaveAll) |
| `srp_mbx.cpp:2155-2423` | `SrpEarlyTalker`: 12 tests, every STREAM_INPUT, both orders, rebind, latest, replacement, ended, bound, unbinding, freed, past the bound, a full held table |
| `sw/firmware/ctrl/test/test_plat_sinks.cpp:583, :1075-1323` | `answer_probe`'s stream variant and the probe's own talker id; `Early.S13` (power cut restore), `Early.S14` (bind while bound), GET_STREAM_INFO's flags |
| `sw/firmware/ctrl/test/srp_early_mutants.py` (new), `srp_mutants.py`, `sink_mutants.py` | 11 SRP plants, 1 control plant; `srp_listener_mutants.py`, `srp_kind_mutants.py` two re-anchored |
| `sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py` | 8x8/1if 58.5, 8x8/2if 63.5, ctrl_plat 19,776 / 19,072 / 21,824 B, the test's ELF writer reaching 64.0 |
| `docs/design/SPLIT_CONTROL_MEMORY.md`, `sw/firmware/ctrl/plat/README.md`, `tb/verilator/ctrl_split_boot/README.md` | the plan with the kept Talkers |

## New checks (planted mutant, failing words)

SRP campaign (`srp_early_mutants.py`, planted at 1x1 one and two interfaces and 8x8/1if):

| Plant | Test | Failing words |
|---|---|---|
| feedback-early-talker-ignored | SrpEarlyTalker.ARegistrationMadeBeforeItsBindingIsDeclaredWithinOneTransmitOnEveryInput | an Advertise registered before its binding |
| feedback-early-rebind-ignored | ...ARebindWhileBoundToAStreamDeclaredAllAlongIsDeclaredWithinOneTransmit | a rebind to a stream declared all along |
| feedback-early-bound-first-sink-only | ...ABindingMadeBeforeItsRegistrationIsDeclaredWithinAJoinTimeOnEveryInput | a binding made before its registration |
| feedback-early-unbounded | ...RegistrationsKeptBeforeABindingAreBoundedByTheInputs | a registration past the bound takes no block |
| feedback-early-any-kind-kept | same | the other kind of a kept StreamID, past the bound |
| feedback-early-count-forgets | same | counted again, they are still kept |
| feedback-early-count-adds | ...AKeptRegistrationThatLeftHoldsItsPlaceUntilItsBlockIsFreed | once its block is freed, another is kept |
| feedback-early-left-uncounted | same | a kept registration that left is counted until its block is freed |
| feedback-early-freed-uncounted | same | once its block is freed, another is kept |
| feedback-early-unbinding-uncounted | ...AnUnboundRegistrationIsKeptAndCountedAgainstTheBound | an unbound registration is kept and counted |
| feedback-early-latest-unheld | ...ABindingTakesTheLatestOfTwoKindsRegisteredBeforeIt | the latest of two kinds registered before the binding |

Control campaign (`sink_mutants.py`): `early-talker-ignored`, platsinks8 + platsinks1, S13 and S14:
"... the Listener is declared in THE TRANSMIT's next MRPDU, input 0".

## Gate table

Final head `f863258d`. The firmware gates ran at `4c5018eb`; the final head differs by docs, ledger comment strings,
adapter comments (no line moved) and the coverage ratchet line, the platform images' loadable bytes identical at
1x1/1if and 8x8/1if (receipts/firmware/final-head-image-identity-f863258d.txt), and no hot-list function moved or
resized against the base (receipts/budget/hot-code-identity-platform-f863258d.txt).

| Gate | Head | Result | Receipt |
|---|---|---|---|
| New tests fail first (head tests, base srp_mbx.c/h) | `bd08d206`, then `4c5018eb` + base adapter | FAIL at all 6 arms on every case the fix owns; the control order, an ended registration, UNBIND-then-BIND and the past-the-bound count pass at the base, as they should | receipts/failing-first/, receipts/failing-first-final/ |
| Firmware gate shard 0/4 (suites) | `4c5018eb` | PASS: 88 arms | receipts/firmware/firmware-gate-4c5018eb-shard0.log |
| Firmware gate shard 1/4 (control campaign) | `4c5018eb` | PASS: 827 of 827 caught, `early-talker-ignored` among them | receipts/firmware/firmware-gate-4c5018eb-shard1.log.gz |
| Firmware gate shard 2/4 (AECP campaign) | `4c5018eb` | PASS: 385 caught, 0 escaped | receipts/firmware/firmware-gate-4c5018eb-shard2.log.gz |
| Firmware gate shard 3/4 (SRP campaigns, both interface counts and 8x8/1if) | `4c5018eb` | PASS: 565 caught, 0 escaped; the 11 new plants at each interface count and the 2 re-anchored among them (27 runs) | receipts/firmware/firmware-gate-4c5018eb-shard3.log.gz |
| fw_coverage --check | `4c5018eb`, `c6ef2329`, `f863258d` | PASS (40 files); srp_mbx.c 854/854 lines, 773/773 branches after its 3 exclusions, recorded in the ratchet at `c6ef2329`; at `f6f83166` it found 2 uncovered (fixed in `b56664fe`) | receipts/firmware/fw_coverage-check-*.log |
| plat_ledger + test_ctrl_memory | `4c5018eb` | PASS (0 findings); 1x1/1if 45.5, 1x1/2if 46, 8x8/1if 58.5, 8x8/2if 63.5 | receipts/ledger/ |
| Twin, twin-plants, twin-maps, twin-maps-plants | `4c5018eb` | PASS: 0 findings, every plant refused, the maps leg and its plant caught | receipts/twin/ |
| CPU budget, targeted (srp, acmp-cmd, fixture, backlog, backlog-owed), base vs head | images of `954e5572` (firmware as final) | 5 groups at each point: 0 refusals, 0 passes over the share, the same 7 owed backlog-owed misses as the base; no hot-list function moved; per-probe deltas mostly negative | receipts/budget/ |
| flip_grade --check (1x1/1if, 8x8/1if), load_grade --check, shape_costs --check | `4c5018eb` tree | PASS: last 127.31/130, ACMP 29.06/30, txL 47.88/49; 8x8/1if THE TRANSMIT 76.81 against 77 | receipts/budget/grader-* |
| Release (all-fabric) export | base vs `f6f83166` | bios.bin byte-identical, BIOS disassembly identical, gateware equal outside comments | receipts/release/ |
| Docs workflow, 103 commands | `aca559e3`, `c6ef2329`, `f863258d` | 99 PASS at each; the 4 CI-environment rows refuse as on the base | receipts/docs/ |
| Routes, #818 floor (WNS >= +0.030 ns, WHS >= 0 ns, every signoff corner), S12b recipe | `f6f83166` images (the final head's rom and sram banks, receipts show both) | PASS with the first directive, ExtraPostPlacementOpt; the other two stopped unrun. 1x1/1if worst WNS +0.437 ns, WHS +0.017 ns, 81 of 135 BRAM tiles; 8x8/1if worst WNS +0.058 ns, WHS +0.036 ns, 94.5 of 135; 0 routing errors, image identity PASS at both. Base reference (the flip lane's route of the base's images, same directive): +0.131 and +0.176 ns, so 8x8/1if is 0.118 ns thinner, above the floor | receipts/routes/ |

REVIEW READY f863258d2a455697d85a5ab48813be8f0783e2d4
