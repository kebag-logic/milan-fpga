# [A452] Round 3 of lane C2 (MAAP), PR #135: handoff

Status: **REVIEW READY** at `921fff59d6e1243284e477f7a368173018420d35`, tree
`dc1d52a75724f6ab29f4831d7498dece23202ca8`. Not pushed: pushing is the
manager's.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch
  `c2-maap-coverage`. `origin` was checked to be
  `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.
- Start head: `053f979b9cfc84871ff2e107d43d20bf0e950db4` (PR #135).
- Main merged: `b2db3a970cedbbff2f8ba813acb96122c442bc58` (`git fetch origin main`).
- Assignment: #66 comment 5903309279 (round 3). Also read: the round-2
  assignment 5887951933, the ruling 5890772857, and both round-2 reviews, R401-2
  (5893508851, POSITIVE) and R400-2 (5893604815, NEGATIVE on F1 and F2).
- Issue #66 comments by this role: TAKEN 5903314753, and REVIEW READY
  5906155816 (this head). No other comment was posted, edited or deleted.
- Every item was done in the assignment's order. No STOP condition was met:
  - no module or top port changed, and nothing under `hdl/` changed;
  - no parent-visible interface changed;
  - the two reviewers' outcomes do not conflict: R401-2's S1(b) is R400-2-S1.
- The lane checkout is left clean at `921fff5`: 0 untracked or ignored entries.
  The build products and the wavedrom venv this session made in it were removed
  (7 paths, each created today).

Commits (one-line subjects, no body, no trailers):

| Commit | Item | Subject |
|---|---|---|
| `c842670` | 1, the merge (parents `053f979b`, `b2db3a97`) | Merge main b2db3a97 (#132, #133) into the MAAP lane, keeping both sides' checks; the maap_version validator section becomes F29 beside main's F28 (#66) |
| `f7b67ce` | 2, R400-2-F1 | Grade a one-cycle MAAP Release! in each state of a mid-walk PROBE, an sDefend and a re-announce entry, and kill each TX state left out of the latch (#66) |
| (PR body) | 3, R400-2-F2 | `PR-BODY.md` beside this file |
| `921fff5` | 4, R400-2-S1 | Say no new TX slot request after a MAAP Release!, since a request already pending is retried until granted, in U28, U23 and the tb/maap README (#66) |
| (PR body, 6) | 5, the parent-visible list | section 6 here; the PR body's Round 3 section |

Footprint:

- **The merge commit** against `053f979b`: 95 files, which is main's content.
  The files this role edited in it are the three conflict files,
  `tb/pp_top/README.md` (MP0 and 34), `tb/maap/README.md` and `mutants.py`
  (F29, the 34 and 497 tallies), and
  `tb/maap/mutations/validator-maap-version-1-only.patch` (re-anchored).
- **After the merge**, `git diff --stat c842670 921fff5`: 9 files, +286/-44.
  They are `tb/maap/sim_main.cpp`, `README.md` and `mutants.py`, five new
  patches, and one sentence of `docs/architecture/11_maap_engine.md`.
  Nothing under `hdl/`.

## 1. Merge resolution (item 1)

Merge commit `c842670d629c46cf4dd991c4ea604a6183d6b4cc` (tree `999435f0`), a
true merge: parents `053f979b` (this branch) and `b2db3a97` (main, PRs #132
and #133). No rebase. Main brings 31 commits over the common base `c951a9ff`,
92 files. Six files changed on both sides. Three merged by themselves
(`docs/00_MILAN_COMPLIANCE_REVIEW.md`, `tb/pp_top/Makefile`,
`tb/pp_top/README.md`), and three conflicted, as the assignment said:

| File | Main's side (#132 D3) | This branch's side (MAAP) | Resolution |
|---|---|---|---|
| `tb/pp_top/sim_main.cpp` `main()` | `--d3-only` runs section D3 alone; `--dr3a` prints the DR3a figures and returns; the default run adds `run_d3` | `--maap-internal-only` runs the MP section alone (`make maap-internal`, the MAAP campaign's pp_top arms) | Both switches kept. Each `if` that skips a section for one focused mode now skips it for every focused mode (`!d3_only && !maap_only`), so `--maap-internal-only` still runs MP alone and `--d3-only` still runs D3 alone. The default run is unchanged from main: Suite (MP included), ISI, name writes, D3 |
| `tb/rx_validator/sim_main.cpp` | new section **F28**, the AECP hold admission (V10), 44 checks | new section **F28** (F28a/b/c), maap_version 2, 0 and 31, 60 checks | Both kept. Two sections cannot share a name, and main's name is already used by main's own docs (`09_verification.md` section 8, "`tb/rx_validator` F28") and by `tb/pp_top/d3_mutants.py` (named checks "F28 held AECP", "F28 rx_aecp_held counts both"). So main keeps **F28**, and this branch's section becomes **F29** (F29a/b/c). It runs after main's F28, and its definition moves after F28. `maap_pdu`'s comment names both users |
| `tb/rx_validator/README.md` | tally 437; V10 bullet; mutation row **M4** (V10 dropped) | tally 453; maap_version bullet; mutation row **M4** (`validator-maap-version-1-only`) | Both bullets kept (this branch's now says F29). Main keeps **M4**; this branch's row becomes **M5**. Tally line **497** (measured: 393 shared + 44 + 60) |

Consequences of the merge, in the same commit:

- `tb/maap/mutants.py`: the rx_validator arm's named check is `F29`, not `F28`.
  With `F28` it would also match main's AECP-hold checks.
- `tb/maap/mutations/validator-maap-version-1-only.patch`: main's V10 moved
  the validator's `ver_fail_w` from line 260 to 274 and changed the trailing
  context, so the patch stopped applying (`git apply --check` failed). It is
  re-anchored with the same planted edit. Every other MAAP patch applies
  unchanged, since main does not touch `hdl/maap`, the PRNG, the timer
  service or `KL_pp_tx_slots`.
- MP section: main adds **MP0** ("both walks over an erased device release
  AECP") to `InternalMaapPhase`, because AECP is held from reset until the D3
  restore ends. `make maap-internal` therefore runs 34 checks, not 33.
  `tb/pp_top/README.md` section MP names MP0 and says 34, and so do the
  pp_top rows of the `tb/maap` ledger.
- Ledger tallies measured at the merge (`tb/maap/mutants.py --only
  validator-maap-version-1-only,compare-mac-forward`, 7/7 with its 3
  controls): F29 47 FAIL of 497, MP7 4 of 34, MP4 5 of 34, maap 9 of 189
  (unchanged).

Graded at the merge head in an export (section 7.1): every suite, including
the MAAP sections (`tb/maap`, rx_validator F29, pp_top MP), #132's (pp_top D3,
acmp_nvm, rx_validator F28) and C1's (`tb/srp_top`, srp_encoder,
srp_stream_fsms). The full campaigns, the MAAP one, #132's
`d3_mutants.py` and C1's `srp_top mutants`, ran at the final head (7.2). Since
the merge, that head changes only `tb/maap` and one sentence of `11`.

## 2. R400-2-F1 (item 2): one-cycle falls in the TX states, commit `f7b67ce`

**Clause.** IEEE 1722-2016 Table B.7: the Release! row goes to INITIAL (Stop
probe_timer in PROBE, Stop announce_timer in DEFEND), and the
PortOperational! row in INITIAL runs generate_address and ReserveAddress!.
So a fall and an immediate rise must end the walk and start a fresh one. By
B.3.2 the frame an entry requested before the fall may drain first (the
ruling, 5890772857). B.3.5.2: no claim after the fall.

**Change** (tests and docs only; no RTL change). Line numbers are at the final
head `921fff5`:

- `tb/maap/sim_main.cpp:1473-1612`, new scenario **U29**
  (`a_one_cycle_release_inside_an_entry_is_never_absorbed`, with the helper
  `start_an_entry` at `:1521`). It lands 20 one-cycle falls (link down for
  exactly one edge, then up), each first seen in a named walker state, in
  three entries (`kEntryFalls`, `:1495`):
  - a **mid-walk PROBE** (the probe_timer expiry that sends the 2nd PROBE):
    `W_IVAL`, `W_ALLOC`, `W_GWAIT`, `W_WRITE`, `W_COMMIT`, `W_LANE`, `W_POST`;
  - **sDefend** (an rProbe! over our block in DEFEND): the same states without
    `W_IVAL`, because sDefend draws no interval;
  - a **DEFEND re-announce** (an announce_timer expiry): all seven.

  The finding asked for `W_ALLOC`, `W_GWAIT` and `W_COMMIT` in one DEFEND
  entry and one mid-walk PROBE entry. U29 covers that and also the other
  states an entry passes through, in both DEFEND entries. Each fall must pass
  five named checks:
  - `:1596` premise: the fall is first seen in its state;
  - `:1599` INITIAL is reached (state_o 0 before the fresh walk's first PROBE);
  - `:1601` no claim is valid from the fall until the fresh walk's 4th PROBE
    is on the wire;
  - `:1604` at most one frame drains first, and it is the entry's own,
    byte-exact (PROBE, DEFEND or ANNOUNCE);
  - `:1607` then a fresh walk: 4 byte-exact PROBEs of one range, then its
    ANNOUNCE, with the claim valid on that range.
  - `:245` declares `enum class Entry` ahead of the suite class, for the
    helper's signature. `run()` calls U29 right after U28, before U19 to U22
    (`:1645`).
- `tb/maap/mutants.py:48-52` adds five arms, each requiring a `U29:` failure.
  `tb/maap/mutations/tx-set-omits-{alloc,gwait,write,commit,lane}.patch` each
  leave one TX state out of the Release! latch at `KL_pp_maap.sv:589-590`. The
  alloc, gwait and commit patches, generated independently here, are
  byte-identical to the reviewer's `receipts/r400-mutants/tx-set-omits-*.patch`
  (`cmp`).
- `tb/maap/README.md`: U0..U29 (`:12`, `:38`), the U29 paragraph (`:166-181`),
  five new ledger rows (`:258-262`), every other row's tally refreshed from
  this campaign run (maap now has 196 checks), and the last-run line: 29 of
  29 arms, 32/32.
- `docs/architecture/11_maap_engine.md:136-138`: "seen in every walker state
  however short" now names the tests that grade it (U26 and U29).

**Head:** `tb/maap` 196/196. U29's 20 falls each give INITIAL and a fresh
walk. The falls in `W_ALLOC` to `W_COMMIT` owe one frame each, which drains.

**The new named check kills each arm** (`make -C tb/maap mutants` at
`f7b67ce`, 32/32):

| Arm | Named failures / checks |
|---|---|
| `tx-set-omits-alloc` | U29 x3 (INITIAL, claim, fresh walk; 3 of 20 falls absorbed, one per entry): 3 of 196 |
| `tx-set-omits-gwait` | U29 x3: 3 of 196 |
| `tx-set-omits-commit` | U29 x3: 3 of 196 |
| `tx-set-omits-write` | U29 x3 and U24 x4: 7 of 192 |
| `tx-set-omits-lane` | U29 x3 and U25 x3: 6 of 194 |

Four older arms now also fail U29: `ival-sends-after-release` (U29 x3, the
`W_IVAL` falls), `post-publishes-after-release` (U29 x2, 10 of 20 falls),
`tx-path-absorbs-release` (U29 x3, 15 of 20) and `off-waits-for-an-edge`
(U29 x1, 20 of 20).

**Failing first.** The new suite against the round-1 RTL (`b03d36f`, whose TX
states did not latch a fall): 23 FAIL of 187, including U29 x3 with all 20
falls absorbed.

## 3. R400-2-F2 (item 3): the PR body, `PR-BODY.md` beside this file

**Clause / authority.** The ruling (#66 comment 5890772857): Table B.7's
Release! row, B.3.2, B.3.5.2, footnote c (the range becomes free, and a PDU an
earlier entry already produced is not withdrawn).

**Change** (no commit; the body is the merge record):

- **"What remains"** is now "What remains (round 1, rewritten in round 3)". It
  says that round 2 resolved both corners:
  - the seed is re-armed by every Release!, including the `W_ADDR` exit
    (`8ae76ee`, `KL_pp_maap.sv:604`, U27);
  - a frame still being drawn is dropped whole with its entry (U17c, U23,
    U28), and a frame whose slot was requested before the fall may drain (Table
    B.7 Release!, B.3.2, B.3.5.2, the ruling), with no PDU generated after the
    fall.

  It no longer contains either false statement R400-2-F2 quotes.
- **Round-1 line references, refreshed** to `921fff5`, with the round-1 line in
  parentheses:
  - the U17b fix `KL_pp_maap.sv:613-627` (`:569-577`);
  - the fit compare `:644` (`:594`);
  - the parent tie `milan_datapath.sv:7769` at dev `ec0cc0c1` (`:7695` at
    `13eda870`).

  Also in round 1's text:
  - the U17b sentence names both stalled states, as round 2's `8382cf6` does;
  - rx_validator F28 is now F29, with round 1's and round 3's tallies each
    labelled;
  - the campaign line says 13 of 13 at round 1 and 29 of 29 now.
- **A header paragraph** says that sections 1 to "What remains" are round 1's
  record: line references refreshed, tallies round 1's.
- **Verification** against the finding: no statement in the body contradicts
  `11` §6 or the ruling. The remaining "no slot request" sentences in Round 2's
  probe paragraph are bench measurements (counts in the unit bench, where the
  pool grants at once), not claims about the top.

The `[A439]` first line and the three `Closes` lines are unchanged. There are
no absolute home paths, tool names or model names, and no attribution footer.

## 4. R400-2-S1 (item 4): "no new slot request", commit `921fff5`

- `tb/maap/sim_main.cpp:1451-1454`, U28's check: "U28: no new TX slot request
  follows the fall (a request already pending is retried until granted), in any
  walker state, for 33 s". The U28 comment (`:1308-1314`) explains the retry:
  at the top, `W_GWAIT` goes back to `W_ALLOC` while the pool is busy, and a
  retry after the fall is the same frame's. This bench's pool grants at once,
  so here any request after the fall would be a new one.
- U23 makes the same statement, so its comment (`:993`) and check (`:1060`) say
  "no new slot request" too.
- `tb/maap/README.md`: U23 (`:114`) and U28 (`:157-165`), with the retry and
  the bench's pool.
- The PR body's Round 2 section: "no new slot request follows the fall" and
  the `d0acc9b` row, each marked as round-3 wording.
- Counts are unchanged: 196/196, and the campaign's `U28:` prefix still
  matches. The new message as it prints on failure is shown by the
  `idle-serves-a-latched-expiry-first` arm (KILLED, "FAIL: U28: no new TX slot
  request follows the fall (a request already pending is retried until
  granted), ... (1 of 17 falls)").

## 5. Suggestions taken or retained

| Suggestion | Disposition | Reason |
|---|---|---|
| R400-2-S1 | **Taken** (`921fff5`, section 4) | Assignment item 4 |
| R401-2 S1 (b), retries at the top | **Taken**: the same text as R400-2-S1 | |
| R401-2 S1 (a), timers during a drain | Retained | Not in the round-3 assignment. `11` §6 and the banner already carry the qualifier ("the timers stop once the lane has the frame, and an expiry meanwhile meets INITIAL"). U28's "no expiry for 33 s" is true in the unit bench, where the lane grants at once |
| R401-2 S2, a stalled-drain expiry arm | Retained | Not in the round-3 assignment. R401-2 found no surviving mutant for it (a documentation-to-test gap, not a behavioural one) |
| R401-2 S3 | First half done (R400-2-F2). The comment re-flow at `KL_pp_maap.sv:619-623` is retained | This round touches no file under `hdl/`, so the RTL stays byte-identical to the reviewed head |
| R400-1 S1 (compare_MAC low-octet pair), R400-1 S2 (`MUTANT_OUTPUT` default) | Retained | Not in the round-3 assignment, as in round 2 |

U29's scope goes a little past F1's required set: it adds `W_IVAL`, `W_WRITE`,
`W_LANE` and `W_POST`, and both DEFEND entries. It is the same scenario shape,
it costs about 5 s of bench time, and it gives each of the five latch states
its own arm.

## 6. Parent-visible list (item 5), re-read at the merged head `921fff5`

Re-read from the diff `c951a9ff..921fff5`, split into what this lane did and
what the merge brings. The processor side was read in PR #132's description
("Parent-visible for pin adoption: rounds 1-6, consolidated") and PR #133's
section 4 with its Round 2 and composed-head notes. The parent side was read
at dev `ec0cc0c1` (trusted checkout, read-only).

**A. This lane (rounds 1 to 3, against `c951a9ff`)**

1. **No port, parameter or interface change.** This lane changes no port or
   parameter of `protocol_processor_top`, `KL_pp_maap`, `KL_pp_rx_validator`
   or any other module (#132's new ports reach the head through the merge,
   B.1). The engine acts only with `cfg_maap_internal_i = 1`, and the parent
   ties it to 0 (`hdl/milan/milan_datapath.sv:7769` at `ec0cc0c1`). The
   shipping fabric does not see rounds 1 to 3. Round 3 changes no file under
   `hdl/`.
2. **One test-only hierarchical observation** (round 2): `tb/maap/maap_wrap.sv`
   `walker_o` reads `u_dut.w_st_r`. See the port-contract gate reading in 7.4.
3. **Tallies**:
   - `tb/maap` 196 (191 at round 2: U29 adds 5);
   - `tb/rx_validator` 497 (main's 437 plus this lane's 60 in F29);
   - `tb/pp_top` 7,893, with MP 34 (main's MP0 included);
   - `run_suites.sh` 1,016,458;
   - the MAAP campaign 32 checks: 3 controls and 29 arms (27 checks and 24 arms
     at round 2).

   No parent file pins any of these counts, and no parent file cites
   `tb/maap`, `maap-internal` or the rx_validator section names (grep of the
   trusted checkout).
4. **A renamed test section:** rx_validator's maap_version section F28 is now
   F29, since main's own F28 grades the AECP hold. No parent file cites either
   name.
5. **Docs:** REQ-MAAP-007's wording (round 2), and `11` §6's "however short"
   now naming U26 and U29 (round 3). The parent's
   `docs/reference/MILAN_COMPLIANCE_MATRIX.md` at `ec0cc0c1` has no MAAP row
   to update.
6. **Entry points**, unchanged in name: `make -C tb/maap mutants` (29 arms) and
   `make -C tb/pp_top maap-internal` (34 checks).

**B. What the merge brings** (it reaches this head through `b2db3a97`, and is
not this lane's change)

1. **PR #132's consolidated list** ("Parent-visible for pin adoption: rounds
   1-6, consolidated", in PR #132's description):
   - top outputs `restore_closed_o`, `restore_rb_o`, `rs_cause_o[2:0]`,
     `restore_cause_o[1:0]`, `d3_unflushed_o`, and the glue
     `pend_i = (|nvm_unflushed_o) | d3_unflushed_o`;
   - parameters `NVM_RETRY_BACKOFF_CYC_P` and `NVM_RS_AGG_CYC_P`, and
     `NVM_RS_TMO_CYC_P`'s ceil derivation;
   - snapshot word 37;
   - AECP held from reset to the D3 terminal (for ever in CLOSED), with the
     hold admission; ADP gated on `restore_done_o`;
   - the firmware obligations: the AEM loaded and CRC-checked before
     `PP_CTRL[1]`; every boot path that enables the entity starts the restore
     walk (the "persistence disabled" path of `nvm_boot()` must run it blind);
     and the bounded terminal wait;
   - the parent-harness edits:
     - the `milan_dp` legs (`sim_aclk`, `sim_ax1x1gptp`, which is outside the
       consumer set, `sim_gmstep`, `sim_gptp`, `sim_main`, `sim_nxn`);
     - `milan_dp_render` T8;
     - `pp_shadow`;
     - `nvm_cosim` `cosim_top.sv` and `cosim_cases.cpp`;
     - the evidence classifier's disposition for `tb/pp_top/d3_mutants.py`.
2. **C1's section 4** (PR #133, "Parent-visible, for the pin-adoption lane",
   as its Round 2 amends it):
   - no interface change;
   - `srp_active_o` gains the Milan 4.3.2 term (the licence waits for the
     stream VID's MVRP join), with the VLAN-table overflow and the egress
     ordering the parent must keep;
   - fewer own LeaveAlls;
   - the one consumer-gate re-base, `sim_crf_licence.cpp:953,956` `>= 4` to
     `>= 3`;
   - the parent documents to update: `docs/traceability/ieee8021q.md` MRP-4
     to MRP-7; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.2.7.1 and
     4.2.7.3/4.4.1; `tb/verilator/milan_dp/README.md`'s `[C]` row and "What
     it cannot show".

   PR #133's composed-head note says the two lists' code edits share no
   parent file, and that the adoption lane edits `milan_dp/README.md` once for
   both (its `[C]` row and sentence, the walk-starter list, the `[AECP]`
   degrade-arm paragraph).
3. **The manager's combined adaptation** `parent-adaptation-132-c1.patch`
   (beside this file; 18,135 bytes, sha256 `2ba66803…ddc420`) is the code half
   of B.1 and B.2. It applies cleanly at dev `ec0cc0c1` (13 files), and the
   consumer bank in 7.4 ran with it. The parent documents in B.1 and B.2 are
   not in it; they are the adoption lane's.
4. **The merge resolution itself adds nothing parent-visible:** it changes
   processor tests and their READMEs only.

## 7. Gates

**Tools.** Verilator 5.052 (`/usr/bin/verilator`, sha256
`098b09b1…7581`, the same binary as round 2). Every build went through a
wrapper outside the tree and the output directory,
`$VALIDATION_STORAGE/ppC2-a452/bin/verilator` (sha256 `58b08717…fbcf`), which
rewrites `-j 0` to `-j 8` and passes everything else through. Heavy builds
ran one at a time. No command was piped; each wrote its log to a file.

**Where.** Suites ran in `git archive` exports under `$VALIDATION_STORAGE/ppC2-a452/`
(`merge-head/tree` at `c842670`, `final/tree` at `921fff5`). The entry points
that read the tree (`make check`, the campaigns, `nvm_port figures`, Yosys, the
pp_top targets) ran in the lane at the final head, with a clean worktree.

**Runs longer than one 10-minute foreground call.** The final `run_suites.sh`
(11 min), the SRP campaign (30 min), the D3 campaign, `test_builder` and
`milan_dp` were each started detached, with their rc written to a file by the
wrapping shell. They were then awaited in consecutive foreground calls and
never overlapped with another build. The first merge-head sweep, also
detached, ended at about 05:26 without writing its rc. Its log stops after 22
passing suites (the last is `scoreboard`), and the cause is unknown: there was
no OOM in this service's cgroup (`memory.events` oom 0), and other lanes run on
the host as the same user. `srp_stream_fsms`'s build directory was left with a
partial, corrupt precompiled header. The remaining 11 suites were then rerun
in the foreground (7.1). `side_port`, `srp_admission`, `srp_decoder` and
`srp_encoder` passed at once. `srp_stream_fsms` failed to compile ("PCH files
were found, but they were invalid"). The build directories of it and of the six
suites after it were cleared, and all seven then passed.

### 7.1 Merge head `c842670` (item 1: every section runs at the merged head)

| Run | Result |
|---|---|
| `run_suites.sh` (export), stopped after 22 suites, then the remaining 11 run one by one with `make` | 33 of 33 suites rc 0, **1,016,453 checks**, 0 failing. MAAP: maap 191, rx_validator 497 (main's F28 and this lane's F29), pp_top 7,893 (MP 34 and D3). #132: pp_top D3, acmp_nvm 360, rx_validator F28. C1: srp_top 2,200, srp_encoder 581, srp_stream_fsms 1,219 |
| `tb/maap/mutants.py --only validator-maap-version-1-only,compare-mac-forward` | 7/7: controls 191/34/497, F29 47 of 497, MP7 4 of 34, maap 9 of 189, MP4 5 of 34 |

### 7.2 Final head `921fff5`: processor suites and entry points

| Entry point | rc | Result |
|---|---|---|
| `./scripts/run_suites.sh` (export) | 0 | 33 suites, **1,016,458 checks**, 0 failing (maap 196) |
| `./scripts/lint_hdl.sh` (export) | 0 | 41 LINT OK |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `make check` (lane) | 0 | mermaid 41, wavedrom 18, links 976, matrix 115 REQ / 17 GAP, modmatrix 94, params 26/26/26 |
| `git diff --check` against `c951a9ff`, `053f979b` and `b2db3a97` | 0, 0, 0 | |
| `make -C tb/maap mutants` | 0 | **32/32**: 3 controls PASS (196, 34, 497), 29 of 29 arms KILLED (table 7.3) |
| `make -C tb/srp_top mutants` (C1's campaign; one full run) | 0 | **90/90**: 11 controls PASS, 78 arm runs KILLED, assertion coverage 65/65 |
| `python3 tb/pp_top/d3_mutants.py --jobs 1` (#132's campaign; one full run, 83 min) | 0 | **83 of 83 KILLED** by their named checks; goldens (acmp_nvm, pp_top, rx_validator) PASS |
| `make -C tb/nvm_port figures` | 0 | "all measured figures agree with the tree" |
| `./syn/yosys/run.sh` | 0 | 36 YOSYS OK, plus `KL_aecp_engine` YOSYS XILINX OK |
| `make -C tb/pp_top maap-internal` / `gsi-internal` / `name-writes` | 0 / 0 / 0 | 34 / 6,182 / 85 checks, 0 failures |
| `python3 tb/pp_top/name_wr_mutant.py` (uses `--name-writes-only`, whose switch the merge touched) | 0 | the decode mutant killed; golden and restored PASS |
| `python3 tb/pp_top/gsi_mutants.py` (uses `--gsi-internal-only`; 13 min) | 0 | 20 mutations detected by named checks; golden and restored PASS |

### 7.3 MAAP mutant table (`make -C tb/maap mutants` at `921fff5`)

| Arm | Named failures / suite checks |
|---|---|
| (controls) maap / pp_top `maap-internal` / rx_validator | 196/0, 34/0, 497/0 PASS |
| `fit-compare-forced-true` | U17 x4, U27: 5 of 196 |
| `fit-compare-off-by-one` | U17 x3, U17b x4: 7 of 195 |
| `seed-clamp-removed` | U18 x4, U18b x2: 6 of 196 |
| `release-keeps-draw-mark` | U17b x3, U17c x2, U18 x3, U27: 9 of 194 |
| `validator-maap-version-1-only` | rx_validator F29 x47: 47 of 497; pp_top MP7 x4: 4 of 34 |
| `compare-mac-forward` | maap U7, U8, U9 x2, U10, U19 x2, U20, U21: 9 of 194; pp_top MP4 x5: 5 of 34 |
| `probe-rprobe-never-yields` | U19 x2: 2 of 196 |
| `defend-rdefend-ignored` | U21 x4, U22 x4: 8 of 194 |
| `defend-rdefend-no-tiebreak` | U20, U21: 2 of 196 |
| `probe-rannounce-tiebreak` | U10 x3, U22 x2, U27 x2: 7 of 196 |
| `yield-reuses-range` | U8, U10, U15, U19, U21, U22, U27 x2: 8 of 196 |
| `ival-sends-after-release` | U17c, U23, U28 x3, U29 x3: 8 of 196 |
| `post-publishes-after-release` | U24 x2, U29 x2: 4 of 194 |
| `tx-path-absorbs-release` | U24 x4, U25 x3, U29 x3: 10 of 190 |
| `off-waits-for-an-edge` | U24 x2, U25 x3, U26 x3, U29: 9 of 189 |
| `rx-release-returns-to-idle` | U26 x2, U28: 3 of 195 |
| `seed-rearmed-on-idle-release-only` | U27 x2: 2 of 196 |
| `seed-clamp-off-by-one` | U18b x2: 2 of 196 |
| `release-waits-for-draw` | U17c: 1 of 196 |
| `idle-serves-a-latched-expiry-first` | U28 x3: 3 of 196 |
| `teardown-keeps-announce-timer` | U28: 1 of 196 |
| `drain-waits-for-the-link` | U17c, U23 x2, U28 x2: 5 of 196 |
| **`tx-set-omits-alloc`** (round 3) | U29 x3: 3 of 196 |
| **`tx-set-omits-gwait`** (round 3) | U29 x3: 3 of 196 |
| **`tx-set-omits-write`** (round 3) | U24 x4, U29 x3: 7 of 192 |
| **`tx-set-omits-commit`** (round 3) | U29 x3: 3 of 196 |
| **`tx-set-omits-lane`** (round 3) | U25 x3, U29 x3: 6 of 194 |

`tb/maap/README.md`'s ledger has the same tallies. The same campaign run at
`f7b67ce` (before the S1 wording) gave identical tallies.

### 7.4 Parent consumer gates (the manager's 16 commands)

**The command set.** The manager's sixteen commands, in the manager's order,
as listed in PR #133's body (Round 2 validation) and confirmed by the manager's
combined bank comment on PR #133 (5890073527).

**Scratch parent** (`$VALIDATION_STORAGE/ppC2-a452/parent`):

- A `git archive` of the trusted read-only checkout at `ec0cc0c1`, committed into
  a scratch repository. Its tree equals `ec0cc0c1`'s except for the
  `protocol-processor` gitlink (`git ls-tree -r` compared: one line differs).
- Submodules:
  - `protocol-processor`: a clone of this lane at `921fff5`;
  - `gptp-processor` (`5dce647`) and `third_party/verilog-axis` (`48ff7a7`):
    fresh public clones at their pins;
  - `external`: left uninitialised (SSH-only, read by no gate).

  They are registered with `git submodule init`, which the parent's
  code-quality gates require.
- `parent-adaptation-132-c1.patch` applied with `git apply` (13 files), and
  committed in the scratch repository only.
- The trusted checkout was not modified.

| # | Command (from the scratch parent root) | rc | Result |
|---|---|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet within budget (multi-declarator 0 <= 0, long function 0 <= 0) |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | all ratchets within budget |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | PASS, 4 findings == ratchet (0 in `hdl/`, 4 in pinned processors, as at round 2) |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | OK: 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 6 | `python3 sw/builder/test_builder.py` (16 min, detached and awaited) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 (placement calibration), whose build report is not on this host, as in rounds 1 and 2. The two `disabled-writer ... FAIL` lines are its mutant being caught ("caught in both states") |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 | 4 legs: 595 + 635 + 595 + 295 checks, 0 failures, 0 PINMISSING |
| 8 | `python3 scripts/check_port_contracts.py` | 0 | OK: 3,780 first-party ports (processor 1,747); undocumented processor 111 <= 111; 0 wildcard, positional or hierarchical binding; inventory 176 test-only hierarchical observations |
| 9 | `python3 scripts/measure_naming.py --check` | 0 | PASS, 96 recorded |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS: 74 <= 77 without a mutation arm, 10 <= 10 unseeded, 0 <= 0 unexplained readers (the patch's `d3_mutants.py` disposition), 3 <= 3 wall-clock; "can be lowered to 74" |
| 11 | `python3 scripts/docs_check.py` | 0 | 0 findings across 179 md files |
| 12 | `python3 scripts/lint_rtl.py --check` | 0 | PASS, 90 <= ratchet 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | 85 warnings, none fatal, 0 PINMISSING (the #132 list's expectation) |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` (25 min, detached and awaited) | 0 | every leg PASS: gptp 181, gptp-lat 181, gmstep 103, main 234, notify 378, crflic 415 (3 DUT and 3 switch LeaveAll MRPDUs), nxn 1,841, nxndv 1,843, nxn8 3,521, nxn4c 1,841, nolpf 234, prune 33, ax1x1 231, aclk 190; 30 `[AECP-WTMO]` passes; render and gmstep mutation controls 6/6 each |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | tdm8_render 65/65 and 152/152; `--leg-defects` 5/5 |

**16 of 16 rc 0.**

The first attempt at commands 1, 2, 8, 9 and 10 returned rc 2, "REFUSED:
project submodules must be initialized". The scratch clones were not yet
registered. After `git submodule init` each was rerun, with the results above.

## 8. Receipts

`receipts/` beside this file (376 files with `SHA256SUMS`, 5.5 MB; no file over 200 KB):

- `tool-identity.txt`: the Verilator binary, the capping wrapper's content and
  sha256, and the other tools;
- `scratch-parent.txt`: how the scratch parent was built, and its tree check;
- `merge/`: the merge-tree builds before the commit, the two re-measured arms,
  and the merge-head sweep (`run_suites.log`, the per-suite logs of the 11
  rerun suites, `totals.txt`);
- `f1/`: U29 at the head, the five new arms, the full campaign at `f7b67ce`,
  and the new suite against the round-1 RTL (`ff-b03d36f.log`);
- `s1/`: the suite after the wording change, and the arm that prints the new
  U28 message;
- `final/`: every processor entry point at `921fff5`, and the campaign
  directories (`maap-mutants/`, `srp-mutants/`, `d3-mutants/` with
  `results.json`, `gsi-mutants/`, `name-wr-mutant/`);
- `parent-gates/`: one log per consumer command, with start, end and rc files
  for the detached ones, the two tree listings, and extracts of the two logs
  over 200 KB;
- `OVERSIZE.txt`: the 8 logs over 200 KB kept only under
  `$VALIDATION_STORAGE/ppC2-a452/`, each with its sha256 and size (six gsi-mutant
  run logs, `milan_dp.log` 1.96 MB, `pp_shadow.log` 288 KB);
- `SHA256SUMS`: every file in `receipts/`.

The scratch area `$VALIDATION_STORAGE/ppC2-a452/` holds the two exports, the
scratch parent, the capping wrapper and the logs. It holds no toolchain,
virtual environment or package.
