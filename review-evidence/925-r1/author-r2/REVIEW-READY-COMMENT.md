[A790] REVIEW READY
Commit: `09a948d4`, branch `925-srp-ta-tf`. It is three commits on `16ba667d` (#901's review head), then one `--no-ff` merge of dev-soft-core `70f4056f` (#901's merge). `70f4056f`'s tree is `16ba667d`'s, so the merge changes no file. Not pushed; the manager pushes and opens the PR.

Changed:
- `sw/firmware/ctrl/srp/srp_mbx.c` / `.h`: of a stream's Talker Advertise and Talker Failed, the one registered latest decides each binding's Listener declaration and the kind ACMP sees while it stays registered; the other decides once it leaves (IEEE 802.1Q-2018 35.2.4, 35.2.6).
  - lwSRP replaces the other type only for a JoinIn/JoinMt and registers a New beside it. The adapter now records the order from lwSRP's indications (`latest_kind`, `listener_kind`).
  - The receive filter and the registrar walk were Failed first, which held Asking Failed until the talker's next MRPDU. An Advertise New over a registered Failed is now Ready within a JoinTime.
  - A binding made later takes the StreamID's latest from any binding of it.
  - No SRP timer or bound changes; lwSRP, the mailbox contract and RTL are unchanged.
- Tests: `srp_mbx.cpp` `SrpTalkerKinds` (6) and `srp_feedback.hpp` (2). They cover both replacements, leave of either kind in both orders, coincident registrations in one MRPDU in both orders, a later binding, the fallback, and ACMP's view.
- Plants: `srp_kind_mutants.py` adds ten, one a rule, each caught by name at both interface counts. The `failed-listener-ready` plant moved to its new site.
- `srp/README.md` states the rule. The ledger records `ctrl_plat` at 8x8/2if as 20,416 B (+64), the same 60.5 RAMB36. `coverage.ratchet` holds `srp_mbx.c` as measured.

Validation (clean clones; `1be0a6c4` has the merge's tree, so its results are `09a948d4`'s):
- Firmware self-test (at `a9f0dbc0`): suites PASS; control 716 of 716, AECP 299, SRP 441 caught, 0 escaped. The SRP shard again at `1be0a6c4`: 441, 0 escaped.
- `fw_coverage --check` PASS: `srp_mbx.c` 741/741 lines, 671/671 branches after its standing exclusions.
- Workflow replays, step by step on fresh clones: in every job of rtl-fast, elaborate and docs, each step ran rc 0 or is a hosted-only step not run, with its reason stated. The three mutant jobs ran as their campaign commands above. `docs`, `firmware-unit` and `changes` ran again at `1be0a6c4`.
- `plat_ledger.py` PASS at every point. ROM is +88 B at 1x1 and +32 B at 8x8; 8x8/1if still plans 56.0. The release image is byte-identical: `bios.bin` and the stripped ELF at both configs.
- Service budget at 1x1/1if, rc 0: 96 groups, 0 refusals, 0 of 129,813 passes over the share.
- Rows, re-run on the merge's clone: the flip check at 1x1/1if passes with every row within its bound (`last` 136.65 of 140 ms, `txL` 48.58 of 49); the load gate passes (0.517 / 0.514 against 0.70). Over every point, the flip check exits 1 at 8x8/2if alone, which is reported and not held, as at the base.
- Service budget at 8x8/1if: 95 groups, 0 refusals, 0 of 266,195 passes over the share. Its STATED lines (the polls' base, ACMP's item, ACMP's declined offer) are #914's per-shape statements, as at the base. None is SRP's, and SRP's items are within at both points.
- Both points record the same 7 probe misses, all in `backlog-owed`, pre-existing. No stated cost changes.
- The merge affects no row. Every image the budget legs and routes used relinks byte-identical at `09a948d4` (budget 1x1 `311430e7`, 8x8/1if `6d2a5d0e`, routes `e85cd3a5`, `b648575d`), so round 1's legs at `a9f0dbc0` carry.
- Routes, both shapes: misses at the base, owed to #927, per issuecomment-6908876793. Figures are Slow WNS / Fast WHS in ns, image at `a9f0dbc0` = `09a948d4`'s:

| Shape | ExtraPostPlacementOpt | ExtraTimingOpt | AltSpreadLogic_high |
|---|---|---|---|
| 1x1/1if | +0.024 / +0.036 | +0.008 / +0.023 | +0.177 / +0.023 |
| 8x8/1if | +0.011 / +0.034 | +0.171 / +0.014 | +0.215 / +0.014 |
| 1x1/1if at the base `16ba667d` | +0.208 / +0.014 | +0.260 / +0.014 | not run |

- No seeds or extra directives were run, and no further route is owed: the merge changes no image.
- Verilator-suites sweep at `09a948d4`: 65 suites in 4 shards, every one with a recorded pass: shard 0 15 of 15, shard 2 17 of 17, shard 3 16 of 16, shard 1 14 of 17. Shard 1's other three, one contention failure (`gptp_shadow`'s fixed 12 s lifecycle timeout, its 325 checks passing) and two wall-clock cuts (`milan_dp_gm_steps`, `milan_dp_render`), each passed when re-run uncontended. The shards' tallies total 2,713,029 checks, 0 in-suite failures.

Acceptance criteria: the desk part is met (above). The bench part, Listener Ready within 1 s of the Talker Advertise, is the gating run's.

Open risks/questions:
- A binding that saw neither registration's indication keeps Failed first until the talker's next MRPDU leaves one kind. That needs every binding of the StreamID unbound and one bound again inside the conflict window; it is documented in the README.
- `srp_mbx.cpp` at the 8x8 entity, a shape no gate runs that suite at, fails two startup tests at `16ba667d` too.
- `coverage.ratchet` holds three AECP lines below their measurement at the base; they are not this change's.
- The shards ran one or two at a time (memory and CPU limits) and were completed across host restarts. Every cut run recorded no rc and is not cited. Shard 2 ran with the hosted job's 4-core budget (`VERILATOR_JOBS=4 SIM_JOBS=4`): without it, `capture_coherence` builds with every host core and overran the 10 GB unit cap.
