# [A688c] HANDOFF: PR #92 round 3 (R719-2 F1 option (a), R719-2 R1, R720-2 R1/R2)

Status: REVIEW READY at `42f9541e1d80e3d888cee1d16f19e01c0027f1cf`. Every repository gate is rc 0 at this head and at base. With the unchanged parent companion change, every parent consumer gate is rc 0, including both milan_dp gPTP legs, both idiom gates and tsn_fuzz `ptp`. The companion change is not committed upstream from this lane, so the PR body does not use closing keywords.

- Repository: Mister-M-alt/FPGA-gPTP, branch `89-90-91-srto-pdelay` (local only, not pushed)
- Base: `55680bff3b287b9a7b0c759f51471fa617c17335` (main)
- Round-2 head (start of this round): `4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e`
- Round-3 head: `42f9541e1d80e3d888cee1d16f19e01c0027f1cf`
- Round-3 commits (one-line subjects, no body, no trailers):
  - `e81885b` Clear sync-ok on a sync receipt timeout that ages nothing, with the peer still elected (#89)
  - `cfb2f4f` Repair the receipt-timeout controls for the new leg and plant a failing control for each new check
  - `42f9541` Document the sync-ok clear on an unaged timeout, say a master-role expiry marks the port, and rewrap the phase-39 comment
- Issue #90: TAKEN at comment 6449145169; `[A688c] REVIEW READY 42f9541e1d80e3d888cee1d16f19e01c0027f1cf` at comment 6452657074.
- No RTL file change, and no top-level port, parameter or register-map change. ROM usage and the leg map are unchanged: 1,021 words shipping, 1,022 seeded, 1,021 priority1 255, `FUTO@254`, `SRTO@992`.

## Assignment items (round-3 [A10] comment 6449128848)

1. Done. On a slave of an elected peer, a sync receipt timeout that does not age (gmPresent FALSE, a priority1 255 grandmaster) clears `FL_SYNCOK` and commits. The peer stays elected. A master keeps sync-ok.
2. Done. Phase 42 in the priority1 255 pass has two named checks, each failed by its own planted control. The four images were regenerated through the generator. The ROM count is unchanged, so it stays inside the budget.
3. Done. `probe_p255_syncok.py` ran unchanged (sha256 `c751da23…`, matching R719-2's manifest) on a `git archive` extraction of the head. By 1 s after Sync stops it reads `syncok=0` with `gm=0000000000000105`, and still does at 2, 3 and 4 s.
4. Done, with one recorded deviation:
   - R719-2 R1: `receipt_mutants.py:60` and `:155` read exactly as written.
   - R720-2 R2: the phase-39 block (`sim_main.cpp:5524`..`5534`) is rewrapped. No line in it exceeds 80 columns, and `awk 'length>90'` no longer prints it.
   - **R720-2 R1, deviation:** the prescribed sentence "So an expiry found in the master role marks the port aged too." has 13 words. `make docs` (`scripts/check_docs.py`, at most 10 words per sentence) fails it; the review's stated verification was not run. `docs/INTEGRATION.md:618` therefore reads "So a master-role expiry marks the port aged too." (9 words, the prescribed predicate verbatim).
5. See the gate sections below. The parent's expectations did not change, so the companion patch is unchanged: sha256 `b53944d52a51323b267b0a91dbfd6bd1aeaabcacf26d31b246b19318d56a1b7a`.

## The design (IEEE 802.1AS-2011 with Cor1 and Cor2)

- 10.3.11 ages on `currentTime >= syncReceiptTimeoutTime && gmPresent`. gmPresent is FALSE under a priority1 255 grandmaster (10.2.3.13; 10.3.12.1.4 g), so nothing is aged and the peer stays elected. Its Sync has stopped all the same, so the synchronization verdict (flags bit 3, the parent's tu source) falls. This is main's rule, kept for the case that ages nothing. A master keeps sync-ok (#84).
- The ROM had three single free words (two in the seeded images), so the leg had to stay within one word of its 11. It stays at exactly 11 words:
  - `SRTO_PASSED_C` is now `0xFF << 3`. A vector's bits 63:53 (priority1 and the top three clockClass bits) compare below it exactly when priority1 is below 255. The Announce gate shifts by 53 instead of 40 (same word count). Bits 3..10 contain sync-ok and no other flag.
  - `W = (flags & PRESENT) * SRTO_PASSED_C` (MULS): the mark for an elected peer, zero otherwise.
  - `S_BESTPV >> 53 < W` means an elected peer with gmPresent: BECGATE, as in round 2. Nothing compares below zero.
  - Otherwise `MASK RT, R0, W` (`RT & ~W`) clears sync-ok for the elected peer and nothing for a master. Then `BR PUBFLAGS` lands on PDPAIR's existing `WRST flags; COMMIT; END` tail.
- This is the first use of `MASK` (OP_SET_MASKED, `merged_w = (opd & ~opb) | (opa & opb)`, `KL_gptp_ucpu.sv:205`) in the gPTP microcode. With `ra = R0` it is and-not. R0 is the register the existing `ALU ra=R0 SUB` negation already relies on. The engine suite runs the real RTL, and the new controls show that the result is load-bearing.
- A master-role expiry now commits again, as main's leg did on every expiry. That commit republishes the same record: thisClock, its path, and flags with sync-ok.

## Changes (file:line at `42f9541e`)

`hdl/ucode/gen_gptp_ucode.py`
- `:14`..`:20` module note: the priority1 255 expiry clears sync-ok (the v4 rule, kept for the case that ages nothing).
- `:420` `S_SRTO` comment: the mark compares priority1 and the top clockClass bits.
- `:500`..`:507` `SRTO_PASSED_C = 0xFF << 3`, with the threshold and mask reasoning.
- `:680` new `Prog.address(name)`: the absolute address of a local label.
- `:1112` Announce gate: `SHR 53` (was 40).
- `:2131`..`:2139` PDPAIR's `bad` path: `e_flags` written out so the label `pubflags` sits on its flags write. The words are unchanged.
- `:2158`..`:2195` `prog_leg_srto`: the new 11-word leg and its docstring, with an assert that the mark's low nibble is sync-ok alone.
- `:2360`, `:2394` `build()`: `LB["PUBFLAGS"]`, resolved after placement from PDPAIR's base.
- The four tracked images are regenerated with each Makefile's arguments. Each differs from round 2 in 11 words (10 in SRTO, 1 in the Announce gate):
  - engine: `0c896101…`;
  - microCPU and OOC: `b21b244f…`;
  - tsngen: `8d3329bc…`.

`tb/verilator/engine/sim_main.cpp`: 1,805 shipping checks (unchanged) and 59 in the priority1 255 pass (round 2: 57).
- `:201`..`:208` header: phase 42 and the fourth pass's phase list.
- `:311` phase 42 runs after phase 41 in the fourth pass.
- `:3940`..`:3943`, `:3980` phase 19: main's check "#84 takeover: the queued receipt timeout commits after it" (`named >= 2`) replaces round 1's "#89 takeover: the queued receipt timeout ages nothing" (`named == 1`). The master's expiry commits again, so its commit is again what "#84 takeover: a queued receipt timeout keeps sync-ok" grades.
- `:5431` `s39_interval` takes the Sync source (default SRCS, so every existing caller is unchanged).
- `:5524`..`:5534` R720-2 R2 rewrap.
- `:5757`..`:5799` phase 42 `clear_sync_ok_when_sync_stops_without_a_grandmaster_present`.

`tb/verilator/engine/receipt_mutants.py` (290 lines) and `tb/verilator/engine/mutants.py` (833 lines), 100 controls (round 2: 98). Both stay under the parent's 1,000-line module ratchet.
- New: `receipt_mutants.py:104` a sync receipt timeout that ages nothing keeps sync-ok (MASK to NOP, word-neutral); `:110` a consumed pair leaves sync-ok down (SVRATE's sync-ok OR removed, one word shorter).
- Replaced: `receipt_mutants.py:27`, "a queued receipt timeout ages a master", became "an expiry takes a master's own vector for a peer's" (the presence term read as set; word-neutral). The old control sent the expiry straight to BECOME. With the master's expiry committing, a second BECOME on a master publishes the same record and writes nothing else observable: PHC word 3 writes only during a slew. So it was an equivalent mutant.
- Re-planted for the new leg, with their named checks unchanged:
  - `receipt_mutants.py:33` main's leg (seven words);
  - `:62` the rule at d27a1654 (12 words, one longer, which packs);
  - `:96` priority1 read as zero;
  - `:123`, `:139` the Announce gate patterns (shift 53);
  - `mutants.py:267` "a receipt timeout unlocks the servo" (the mark now in RU);
  - `mutants.py:505` "a queued receipt timeout clears a master's sync-ok", now the mask taken as the mark itself (`rb=RU`), word-neutral. This drops round 2's incidental priority1-read defect.
- R719-2 R1 wording at `:60` and `:155`.

Docs:
- `docs/INTEGRATION.md:301`..`:307`: a priority1 255 grandmaster is not aged and its timeout clears the verdict.
- `docs/INTEGRATION.md:402`..`:403`: the verdict table gains a row for the same timeout under priority1 255.
- `docs/INTEGRATION.md:566`..`:570` (#84 section): the unaged timeout clears bit 3 on a slave.
- `docs/INTEGRATION.md:592`..`:594`: the Sync departure needs priority1 below 255.
- `docs/INTEGRATION.md:618`: R720-2 R1 (see the deviation above).
- `docs/INTEGRATION.md:646`..`:648`: the gmPresent paragraph.
- `docs/HDL_DEVELOPER.md:202`..`:218`: the unaged expiry, the mark as a mask, `MASK`, and `PUBFLAGS`.
- `docs/TEST_DEVELOPER.md:129`: "Clears sync-ok when that grandmaster's Sync stops."
- `docs/SOURCE_EVIDENCE.md:31`: the slew anchor `#L998` (the generator grew above it); `:40` new row "Unaged Sync timeout clears sync-ok".

## New checks, their controls and failing words

Both tables come from the head arm's own log, `receipts/repo-gates-head/04b-engine-mutants.log`: `receipts/coverage/coverage-map.md` and `receipts/coverage/mutant-table.md` (all 100 controls). Every control named below was caught through the arm's named verdict.

| Check (new or restored) | Control that fails it | Failing words, as printed |
|---|---|---|
| p1 255 #89 gmPresent: a priority1 255 grandmaster's usable Sync raises sync-ok (new) | a consumed pair leaves sync-ok down | `FAIL p1 255 #89 gmPresent: a priority1 255 grandmaster's usable Sync raises sync-ok got 0000000000000000 exp 0000000000000001` |
| p1 255 #89 gmPresent: when its Sync stops, sync-ok clears within syncReceiptTimeout and the peer stays elected (new) | a sync receipt timeout that ages nothing keeps sync-ok | `FAIL p1 255 #89 gmPresent: when its Sync stops, sync-ok clears within syncReceiptTimeout and the peer stays elected got 0000000000000000 exp 0000000000000001` |
| #84 takeover: the queued receipt timeout commits after it (main's check, restored) | an expiry takes a master's own vector for a peer's | `FAIL #84 takeover: the queued receipt timeout commits after it got 0000000000000000 exp 0000000000000001` |

Re-planted controls (the new leg moved their patterns), each still caught on every check it names:

| Control | Failing words (named checks) |
|---|---|
| a sync receipt timeout only clears sync-ok (main's leg) | #89 Sync stops: the plane takes mastership; #89 never usable: the grandmaster is aged; the three "#89 …: the plane takes mastership within" shapes |
| only an expiry that ages a slave marks the port (the rule at d27a1654) | #89 takeover: the queued receipt timeout leaves the port aged; #89 a lone pair heard as master: a later Announce elects nothing; #89 Announce lapse: a sync receipt timeout after mastership ages the next Announce |
| sync receipt ageing ignores gmPresent | p1 255 #89 gmPresent: a priority1 255 grandmaster without Sync stays elected |
| an aged port takes Announces | the five "#89 …: the aged port stays master" checks; p1 255 #89 gmPresent: a priority1 1 Announce on the aged port elects nothing |
| an aged port refuses a priority1 255 grandmaster | p1 255 #89 gmPresent: the aged port elects a priority1 255 grandmaster |
| a queued receipt timeout clears a master's sync-ok | #84 takeover: a queued receipt timeout keeps sync-ok; #84 every master cycle publishes sync-ok |
| a receipt timeout unlocks the servo | (plain verdict) the servo stays locked across a Sync receipt timeout |

"An aged Announce is dropped rather than aged" kept its pattern (the Announce gate's compare and branch are unchanged) and is caught as before.

## Reviewer probe (R719-2 `probe_p255_syncok.py`, unchanged)

The script's sha256 is `c751da234f20c8208928b76b7ece60c60ce53f9b4e4413b1aee7481c0627ec10`, as in R719-2's `MANIFEST.sha256`. That manifest verified in full. The probe ran on a `git archive` extraction of `42f9541e` with the pinned Verilator (`receipts/probes/`). The reviewer's own logs are under `receipts/probes-before/`.

| Point | base `55680bff` (reviewer) | `d27a1654` (reviewer) | `4d8fb902` (reviewer) | `42f9541e` |
|---|---|---|---|---|
| after 2 s of usable Sync | `flags=d gm=…0105` | `flags=d gm=…0105` | `flags=d gm=…0105` | `flags=d gm=…0105` |
| 1 s after Sync stopped | `flags=5 gm=…0105 syncok=0` | `flags=e` master (`gm` thisClock, the peer aged) | `flags=d gm=…0105 syncok=1` | `flags=5 gm=0000000000000105 syncok=0` |
| 2, 3, 4 s after | the same | the same | the same | the same |
| the pass's own checks | 53/53 | 53/53 | 57/57 | 59/59, rc 0 |

## Base and head repository gate records

Each gate ran unpiped, on its own, through the lane's recorder (`receipts/scripts/gate.py`, `gate-list.py`), with its own log and result row. Every gate ran in its own systemd unit with a memory cap, pinned to this lane's CPUs.
- Head gates 01-11 (except 04b) ran in the lane checkout. 04b and 12 each ran in a fresh clone of the lane at the same commit, so the three could run at once.
- Base gates ran this round, in three fresh clones at `55680bff`, in the same split.
- `head_unchanged` is True in every row. Each row's `.json` is the record. The head fast gates and the head arm shared one output directory, so their `DONE.json` summaries overwrote each other and are not kept; `rows.txt` lists the rows.

### Head `42f9541e`

| Gate | Command | rc | Seconds | HEAD unchanged |
|---|---|---:|---:|---|
| 01-contract | `make contract` | 0 | 0.0 | True |
| 02-ucpu | `make -C tb/verilator/ucpu` | 0 | 0.1 | True |
| 03-parser | `make -C tb/verilator/parser` | 0 | 58.0 | True |
| 04a-engine-run | `make -C tb/verilator/engine run` | 0 | 186.8 | True |
| 04b-engine-mutants | `make -C tb/verilator/engine mutants` | 0 | 7087.9 | True |
| 05-gaskets | `make -C tb/verilator/gaskets` | 0 | 33.9 | True |
| 06-tsngen | `make -C tb/tsngen` | 0 | 34.6 | True |
| 07-bench-test | `make -C bench/arty test` | 0 | 0.1 | True |
| 08-lint | `make lint` | 0 | 0.3 | True |
| 09-docs | `make docs` | 0 | 1.0 | True |
| 10-diagrams-check | `make diagrams-check` | 0 | 0.2 | True |
| 11-ooc-selftest | `python3 syn/ooc/check_ooc_clock.py --selftest` | 0 | 0.1 | True |
| 12-make-all | `make` | 0 | 7169.5 | True |

- Engine suite: 1,805 checks in the shipping pass and in each seeded pass, and 59 in the priority1 255 pass. The arm is 101/101: the control plus 100 controls.
- Other suites: microCPU 768; parser 337 plus 9 mutants; gaskets 81 plus 5; tsngen 288 plus 4.
- `make` (12) repeats all of these with the same tallies.
- Gate 02 took 0.1 s because its Verilator model was already current: the RTL is unchanged, and the model reads the regenerated image at start. Its log shows the 768 checks running.

### Base `55680bff` (rerun this round)

| Gate | Command | rc | Seconds | HEAD unchanged |
|---|---|---:|---:|---|
| 01-contract | `make contract` | 0 | 0.0 | True |
| 02-ucpu | `make -C tb/verilator/ucpu` | 0 | 8.4 | True |
| 03-parser | `make -C tb/verilator/parser` | 0 | 87.3 | True |
| 04a-engine-run | `make -C tb/verilator/engine run` | 0 | 135.4 | True |
| 04b-engine-mutants | `make -C tb/verilator/engine mutants` | 0 | 3812.0 | True |
| 05-gaskets | `make -C tb/verilator/gaskets` | 0 | 48.3 | True |
| 06-tsngen | `make -C tb/tsngen` | 0 | 64.8 | True |
| 07-bench-test | `make -C bench/arty test` | 0 | 9.3 | True |
| 08-lint | `make lint` | 0 | 0.4 | True |
| 09-docs | `make docs` | 0 | 1.1 | True |
| 10-diagrams-check | `make diagrams-check` | 0 | 0.2 | True |
| 11-ooc-selftest | `python3 syn/ooc/check_ooc_clock.py --selftest` | 0 | 0.1 | True |
| 12-make-all | `make` | 0 | 4133.3 | True |

Engine at base: 1,703 per shipping-image pass, 53 in the priority1 255 pass; the arm 73/73.

## Consumer gate table (scratch milan-fpga dev `97aab1d0`)

### Head: snapshot `d94e7bcf89738d124ad1311ac836ef06326a5cbf`

The snapshot is dev `97aab1d0`, freshly cloned from GitHub with its five public submodules. The gptp-processor gitlink is `42f9541e`, and the companion patch (sha256 `b53944d5…`, unchanged from round 2) is applied. It is one local commit, never pushed.
- The manager's template ran with unchanged commands and environment, split over three fresh clones of the snapshot. Each clone ran the manager's recorded-gates runner in its own unit: A = template commands 1-13 and 15; B = command 14; C = tsn_fuzz `ptp` with the CI-pinned field-campaign generator (`deca300c`).
- Specs: `receipts/consumer-head/final-{a,b,c}.json`. Per-command logs, `results.json` and `complete.json` are under `final-{a,b,c}/`.

| Unit | # | Gate | rc | Seconds |
|---|---:|---|---:|---:|
| A | 1 | `python3 scripts/check_cpp_idiom.py` | 0 | 1.817 |
| A | 2 | `python3 scripts/check_py_idiom.py` | 0 | 5.224 |
| A | 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 159.808 |
| A | 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.707 |
| A | 5 | `python3 sw/builder/test_builder.py` | 0 | 1571.504 |
| A | 6 | `make -C tb/verilator/gptp_shadow -j8` | 0 | 258.678 |
| A | 7 | `python3 scripts/check_port_contracts.py` | 0 | 4.598 |
| A | 8 | `python3 scripts/measure_naming.py --check` | 0 | 0.783 |
| A | 9 | `python3 scripts/measure_test_evidence.py --check` | 0 | 11.351 |
| A | 10 | `python3 scripts/docs_check.py` | 0 | 7.929 |
| A | 11 | `python3 scripts/lint_rtl.py --check` | 0 | 18.12 |
| A | 12 | `make -C tb/verilator/milan_dp gptp` | 0 | 149.561 |
| A | 13 | `make -C tb/verilator/milan_dp gptp-lat` | 0 | 151.841 |
| A | 14 | `make -C tb/verilator/milan_dp_gm_steps` | 0 | 645.944 |
| A | | run complete | 0 | |
| B | 1 | `make -C tb/verilator/milan_dp_gptp` | 0 | 5168.418 |
| B | | run complete | 0 | |
| C | 1 | `make -C tb/verilator/tsn_fuzz ptp` | 0 | 51.483 |
| C | | run complete | 0 | |

- milan_dp `gptp` 185/185, `gptp-lat` 185/185.
- milan_dp_gptp: physical scenario 151 checks, 0 failures, `simulated_duration_seconds=17.992742740 cycles=899637137` (the figure the companion patch puts in the parent docs, unchanged); setup abort 6, no-TX 20, no-Pdelay 14, recentre 14, all 0 failures.
- gm_steps: gmstep 196 checks, 0 failures, and its wrapper 6/6.
- tsn_fuzz `ptp`: 677 pass, 0 fail, artifact freshness 1/1.
- After the runs the A and B clones are clean. The C clone holds the campaign's own rewrite of `TEST_RESULTS.md`, whose only change is its timestamp (`receipts/consumer-head/final-c-test-results-rewrite.diff`).
- Extra, not on the list: `make -C tb/verilator/gptp_plane` in the A clone after its run, rc 0 (29/29, phc_step 62 checks with 0 failures, its campaign 8/8; `receipts/parent-explore/`). The companion patch edits that harness, and round 2 had run it only in exploration.

### Base: dev `97aab1d0` with gitlink `55680bff`

These are round 1's records, carried unchanged (`receipts/consumer-base/`; same template, same base commit): all 15 commands rc 0, run complete exit 0. tsn_fuzz `ptp` at base is round 2's record (677/0, rc 0). Neither the parent base nor the template changed since, so neither was rerun this round.

## Residuals and follow-ups

- Parent follow-ups owed by the gitlink bump (none made here):
  - The companion change, sha256 `b53944d5…`, is unchanged and re-verified at this head.
  - The donor deep links that `scripts/check_gptp_docs.py --with-submodule` checks must name the new gitlink.
  - `tb/verilator/milan_dp/README.md:347` "137 checks" was already stale at base.
- A master-role sync receipt timeout commits again (as on main). The commit republishes the same record. Phase 19's check now grades that commit, so "#84 takeover: a queued receipt timeout keeps sync-ok" cannot pass vacuously.
- R720-2 R1 wording deviation (see item 4).
- Suggestions not taken (not in the round-3 assignment):
  - R720-2 S1: a priority1 254 boundary check. The threshold changed encoding this round; it is exact by construction (`255 << 3`), but no control moves it by one.
  - R720-2 S2: record the Sync asCapable gate's reachability note.
  - R720-2 S3 / R719-2 S5: a second responder sending its own Follow_Up.
  - R719-2 S2: a sentence that a new grandmaster on a marked port also waits for its first usable pair.
  - R719-2 S3: own-port Sync filter.
  - R719-2 S4: Figure 11-8 wrong-sequenceId reset.
- Published flags bit 0 keeps its #82 meaning.

## Environment and process notes

- No vendor synthesis tool on this host: `make ooc` ran as its self-test only, and the parent's `xvlog_gate.py --check` takes its documented skip. No RTL changed.
- CPU booking:
  - This unit's own range was 16-31. The parent units A and B ran on a range `cpu_ranges.py pick` returned (112-127).
  - Unit C briefly shared two of this lane's CPUs with the base fast gates as those finished.
  - Units ran with MemoryMax 4-9 GB, `PYTHON_CPU_COUNT=8`, `VERILATOR_JOBS=8` and `MAKEFLAGS=-j8`.
  - Temporary files went to the lane scratch, never to RAM.
- Exploratory runs (`receipts/explore/`):
  - The first work-in-progress engine run failed one check, round 1's "the queued receipt timeout ages nothing". That failure led to restoring main's check.
  - Two parallel runs of 14 and 2 controls through the arm's own `run_mutant` were all caught before the recorded arm.
- A first call of the receipt copier was malformed and left one stray directory under `receipts/`, which was removed before the index was generated.

## Receipts

`receipts/INDEX.md` lists every file present, with size and SHA-256 prefix. Host paths are replaced by placeholders such as `<scratch>`, `<lane>`, `<parent-a>`, `<lane-clone-mutants>` and `<management>`.
- `repo-gates-head/`, `repo-gates-head-make/`: head gate logs and result rows.
- `repo-gates-base/`, `repo-gates-base-mutants/`, `repo-gates-base-make/`: base gate logs and result rows.
- `repo-gates-lists/`: the gate lists.
- `consumer-head/`: specs, the runner's logs, `results.json` and `complete.json`. `consumer-base/`: round 1's base records.
- `probes/` (this head), `probes-before/` (the reviewer's logs).
- `coverage/`: the check-to-control map and the full control table. `rom/packing.txt`: packing for every image, the tracked-image hashes and their byte-identical regeneration, and the decoded SRTO leg and tail.
- `units/`: each unit's command and exit status. `explore/`, `parent-explore/`.
- `parent-companion-test.patch` and its `.sha256`. `scripts/`: the lane's runner and helper scripts.
