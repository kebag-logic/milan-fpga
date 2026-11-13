[A775] REVIEW READY
Commit: 18300f6e5f0c63b2ebc81d6bbc243496034f638a (branch `895-talker-redeclare`, PR #901, round 2; base `66f71326`, #810 round 29's `7f50ee6a` and `b2d39235` merged; `665-s2b-cycles` read `b2d39235` at the round's start, before each set of legs and at 09:40 CET, before the gate pass started at 09:43. #810's round 30 REVIEW READY (`5bea2597`, on #665) came at 10:10 CET, after it, and the branch is now `32551422`, under review; by the ruling's item 6 (merge only a round 30 REVIEW READY before the gate pass) it is not merged here, and composing this lane with it is the next step after its review; for `dev-soft-core`, after #810)

Changed (round 2: the ruling issuecomment-6840463408 on R835-1 and R836-1, items 1 to 6):
- **R835-1-F5:** `declare_sources` reads `mrp_mad_leave`'s answer. A withdrawal's Leave that lwSRP refuses (its participant holds an MRPDU the ring refused, which the declarations after THE TRANSMIT's build can meet) keeps the source declared (`TALKER_DECL` and `IDLE_SLOPE` too, as lwSRP still declares it) and owed. THE TRANSMIT's next call starts with no frame owed (`transmit_aged`), so its first declarations take the Leave, and the hold-off starts there. No lwSRP change.
- **R835-1-F4:** `srp_bounds.h` states THE TRANSMIT's publications as the code makes them: IDLE_SLOPE and TALKER_DECL at most once a declarations pass, so at most twice on the interface the call builds; SR_DOMAIN once, for an adoption; LICENCE once for each licence a withdrawal closes; at most 5 + MBX_N_PUB_SOURCES writes an interface, within the existing terms. `SRP_MBX_PUB_POLL_MAX` is unchanged.
- **Tests and plants:** `Talker.TransmitPublishesWithinItsTermsAfterARefusedJoin` counts one call's writes with a refused join (TALKER_DECL and IDLE_SLOPE 2 on the built interface and 1 on the other, LICENCE 1, SR_DOMAIN 0). `Talker.RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt` runs R835-1-F5's sequence through the real reclaim, at both points: an adoption refused for storage, the ring refusing the MRPDU built, the adoption made after it, the Leave refused. It then reads the Leave on the wire, `TALKER_DECL` clear at its commit, no Advertise after it, and the hold-off started. Three plants: `talker-transmit-publishes-past-its-terms`, `talker-refused-withdrawal-forgotten` (round 1's code) and `talker-refused-withdrawal-not-owed`. Each is caught at both points.
- **The hot layout:** the F5 fix grew the hot-listed `declare_sources` by one instruction, which moved every later hot function by 4 B. That firmware's legs failed two stated costs at 1x1/1if by their own graders: the registrar walk at 2,015 CPU cycles against `poll_grade.py`'s 2,000, and a pass's polls' base at 16,141 against 15,500. The bounds are unchanged. Instead, `moved`'s stale update is one instruction shorter with the same value (`17ac263f`), so every function after `declare_sources` is at round 1's address again at both points. Every leg then ran again on that firmware.
- **Docs:** `SPLIT_CONTROL_MEMORY.md` section 5 (this head's images, and their growth over `b2d39235`) and section 13 (this head's graders, the 8x8/2if pass at 320 us, the hot layout). The SRP README's Talker paragraph (RS2, and S2's reading of two LeaveAllTime periods). `MAILBOX_SPLIT.md` (TALKER_DECL on a refused Leave, THE TRANSMIT's publications). `ctrl_memory.py`'s reasons carry issue IDs only (RS1). The coverage ratchet is updated.
- **R835-1-F3 / R836-1 F3:** round 1 stated 28 Talker plants, but `d023b77a`'s table held 26. With this round's 3 plants, this head's table holds **29**: `len(srp_talker_mutants.defects())`, and 58 `[ok] talker-` lines in the SRP campaign.

Validation (one clean-clone pass on this head; receipts in the lane's round 2 output directory):
- Every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml`, each job on its own fresh clone: 139 rc 0, 226 not run each with its reason, 0 bad. All 39 job, lane and harness trees were clean after.
- The full Verilator sweep, 65 suites, as four shard units on clones of this head, with 0 in-suite check failures:
  - 62 suites passed as run.
  - `gptp_shadow`, `gptp_tables` and `mbx` failed only in their planted-defect scripts. These read `make`'s output and met its directory messages under the runner's `MAKEFLAGS=-j4`; `rtl.yml` sets `-jN --no-print-directory`.
  - Re-run on the same clone with CI's form, each passed (make rc 0, tally verdict rc 0), with every plant caught.
- `test_ctrl_firmware.py --require-rv32 --self-test`: PASS. Campaigns: control 696 of 696, AECP 227, SRP 398 (the 29 Talker plants at both points among them), 0 escaped.
- `fw_coverage.py --check`: PASS (39 files; `srp_mbx.c` 725/725 lines, 651/651 branches; `ctrl_app_srp.c` 89/89, 72/72). The TSN stack boundary: PASS. The saved-state store gate: 455 tests.
- The CPU budget harness, both points, every arm (arm A, `answering-every-port`, `valid-destinations`, arm B `aecp`):
  - The legs ran on this head's firmware, every group of every arm. 0 refusals. Arm A has 7 of 945 and 7 of 996 misses, the merged head's seven that tsn-c-stack #26 holds; every other arm 0. No work pass over the share (the heaviest is 173,458 cycles), and no `STATED` line.
  - The gate pass built each arm at this head. The image's loadable bytes are identical to the legs' builds, one sample group per arm is byte-identical to its measured log, and every measured group regrades rc 0.
  - The load gate's tables move in neither column.
- `load_grade.py --check` rc 0, `--selftest` 25 of 25; `flip_grade.py --selftest` 131 of 131, `--check` rc 1 at the head as at the base; `test_ctrl_memory.py` PASS; `test_builder.py --require-rv32` rc 0; `behave` 508 scenarios, 2,330 steps; the split boot simulation at 1x1 and 8x8, its native controls and its plants rc 0; `git diff --check` against the base and #810's merged head clean.
- Simulated wire (the `valid-destinations` arm's split SoC, decoded): nothing declared before a probe; each Advertise at MAAP's base + n on its own interface; the 15 s window's end and a range lost to a peer's ANNOUNCE each withdraw; no Talker Failed at any time; both points PASS.
- ROM: fixture / platform RAMB36 1x1/1if 38.5 / 39.5, 1x1/2if 41.5 / 43.0, 8x8/1if 51.5 / 53.0, 8x8/2if 58.0 (ledgered 58.5) / 60.0 (ledgered 60.0, cap 60.5). Over `b2d39235`, each image linked at both commits from the same inputs: +944 to +1,064 B of `rom`, +16 to +64 B of `sram`, `ctrl_plat` +64 B.

Acceptance 4, stated by the ruling (no regression beyond stated deltas; not as met). The 1x1/1if long-window load stays at most 0.70. Every other flip-gate figure was measured at this head and at the base `b2d39235`. The tables did not move this round, so the head's figures equal `d023b77a`'s and the deltas are the ones the ruling accepted:

| Point | Figure | Ceiling or bound | Base | Head | Delta | Owner |
|---|---|---|---:|---:|---:|---|
| 1x1/1if | load at the pin / with tsn-c-stack#32 | 0.70 | 0.486 / 0.483 | **0.488 / 0.486** | +0.002 / +0.003 | this lane, HELD |
| 1x1/1if | R4 / R5 / R6 by every source | 20 / 90 / 90 ms | 66.12 / 35.95 / 28.67 | 66.77 / 36.24 / 28.92 | +0.65 / +0.29 / +0.25 | #894 |
| 1x1/1if | first / last queued notice | 20 / 125 ms | 20.00 / 22.00 | 20.00 / 22.00 | 0 / 0 | #894 |
| 8x8/2if | load at the pin / with tsn-c-stack#32 | 0.75 (#890; `flip_grade.py` 0.70) | 0.816 / 0.767 | 0.817 / 0.768 | +0.001 / +0.001 | #890 |
| 8x8/2if | R4 / R5 / R6 by every source | 20 / 90 / 90 ms | 346.15 / 144.15 / 135.80 | 347.69 / 144.53 / 136.15 | +1.54 / +0.38 / +0.35 | #894 |
| 8x8/2if | first / last queued notice | 20 / 125 ms | 22.00 / 62.00 | 22.00 / 62.00 | 0 / 0 | #894 |
| 8x8/2if | rows by measurement: arm A misses | none over | 7 of 996 (4 of 136) | 7 of 996 (4 of 136) | 0 | tsn-c-stack #26 |
| 8x8/2if | least row margin, arm A / `answering-every-port` | | 8.973 / 6.246 ms | 9.718 / 7.879 ms | +0.745 / +1.633 | |
| 1x1/1if | rows by measurement: arm A misses; least margin arm A / arm | | 7 of 945; 11.006 / 9.080 ms | 7 of 945; 11.233 / 9.036 ms | 0; +0.227 / -0.044 | tsn-c-stack #26 |

(The base's measured rows are #810 round 29's legs, as the base tree's `SPLIT_CONTROL_MEMORY.md` section 13 records them; the head's are this round's legs.)

Acceptance criteria:
- 1: met.
- 2: met, a refused withdrawal included.
- 3: met. 11 unit tests at both points and 3 composition tests; 29 plants, each killed by name at both points; coverage 100 % of the changed files.
- 4: by the ruling, above.
- 5: met (the ruled caps; every other point at or under 56).
- 6: the bench lane's.

Open risks/questions:
- **For a separate issue: the Domain's own leave and join on the same path (`change_domain`).** A probe test of R835-1-F5's sequence (not committed; its source and logs are in the receipts) shows, at both points, the adapter recording VID 3 adopted with nothing owed, while interface 0's MSRP Domain stays VID 2 on the wire for 25 s (28 declaring events, no Leave) and VID 3 is never declared. It is not the same mechanism, so it is not fixed here. The adoption reserves the new VID with `mvrp_declare` before the Leave, then commits `i->domain`, `SR_DOMAIN` and every source's VID; owing it after a refused Leave would leave the reserved VID declared, and leak it if the Domain changes again first. A fix needs an ordering decision (or THE TRANSMIT not re-entering the declarations of an interface whose build left a frame owed).
- Still to be proposed as an issue (R835-1 found none filed): the Domain adoption re-declares in place with a changed vlan_identifier, a FirstValue change that 35.2.2.8 does not allow either.
- The split image's stated costs follow its hot layout. The margins under bounds this lane does not change are a layout's: the polls' base 422 cycles under at both points (15,078 and 27,578 cycles), and the 1x1/1if registrar walk 13 under (1,987 of 2,000).
- Each source is declared on its own interface only (before, every interface declared every source).
- #896: the board's standing Talker Failed that its trigger correlates with is gone; `capture()` and the Listener path are unchanged, so #896's mechanism and fix stay its own.
