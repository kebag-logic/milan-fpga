# [A445] HANDOFF: PR #135 round 2 (lane C2, MAAP)

Status: **REVIEW READY** at `053f979b9cfc84871ff2e107d43d20bf0e950db4`
(issue #66 comment 5893086634).

- The round first ended on a STOP at `ea79d8b`. The manager ruled **option 2**
  (issue #66 comment 5890772857): a frame whose TX slot was requested before the
  fall may drain; no internal cancel path and no module port change.
- This session closed the ruling's three points on top of `ea79d8b`, with no RTL
  logic change: a new arm (U28), U23's drained arm with its window, and the
  wording and citations in `11` §6 and the banner. Every gate was re-run at the
  new head (section 6).

Details:

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch
  `c2-maap-coverage`.
- Start head `b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745`. STOP head `ea79d8b`.
  New head `053f979b9cfc84871ff2e107d43d20bf0e950db4`, tree
  `33087148b197340778ee033f3f2210ac0f629059`. Not pushed.
- Assignment: issue #66 comment 5887951933 (round 2); round 1: 5884446021.
  Ruling on the STOP: 5890772857.
- Reviews: R400-1 (PR #135 comment 5887946706) and R401-1 (comment 5887948102).
- Issue #66 comments by this role: TAKEN 5887963063; STOP 5890736650 (head
  `ea79d8b`); REVIEW READY 5893086634 (head `053f979`). TAKEN was not posted twice.
- The lane checkout is left clean at `053f979`: no untracked or ignored files.
- The PR body update is `PR-BODY.md` beside this file (its "Round 2" section).

Commits (one-line subjects, no body, no trailers):

| Commit | Finding | Subject |
|---|---|---|
| `4de2c60` | R400-1 F1 (R401-1 F2 and F3 folded in) | Honour a MAAP Release! in every walker state, ordered by the entry's TX slot request, and start walks on the engage level (#66) |
| `8ae76ee` | R400-1 F2 + R401-1 F1 | Re-arm the MAAP footnote-a seed on every Release!, including one that lands while generate_address redraws (#66) |
| `fa21c58` | R400-1 F3 | Grade the MAAP seed clamp at its boundary, 0xFE00 - count + 1 clamped and 0xFE00 - count taken as given (#66) |
| `2c11d6f` | R400-1 F4 | Drop the link during a MAAP draw that fits, so a Release! that waits for the answer and adopts it turns U17c red (#66) |
| `8382cf6` | R401-1 F4 (suggestion) | Name both states a stale MAAP draw mark stalls, W_ADDR for an unseeded walk and W_IVAL for a seeded one (#66) |
| `ea79d8b` | test order only | Run the MAAP Release! scenarios before U19 to U22, so the suite still ends on U22's claim (#66) |
| `d0acc9b` | ruling point 1 (R400-1 F1) | Grade no PDU generated after a MAAP Release! in all 12 walker states, with both timers stopped for 33 s after the fall (#66) |
| `4f6affc` | ruling point 2 (R400-1 F1) | Grade the one frame a MAAP Release! may drain, the ANNOUNCE requested before the fall, on the lane within 63 cycles (#66) |
| `053f979` | ruling point 3 (R400-1 F1) | Cite Table B.7, B.3.2 and B.3.5.2 for the MAAP Release! ordering and say no PDU generated after the fall, in 11 section 6 and the banner (#66) |

Footprint against the start head: 18 files, +1112/-52. The one RTL file changed
is `hdl/maap/KL_pp_maap.sv` (+88/-16, most of it comments). Against the STOP head
`ea79d8b`: 10 files, +368/-67, and the RTL change is the banner comment alone. No
port, parameter or interface change anywhere. The unit wrapper
`tb/maap/maap_wrap.sv` (outside `hdl/`) gained three observation ports.

## 1. Release! design (R400-1 F1/F2, R401-1 F1; R401-1 F2/F3 folded in)

Written before any code in the first session, and completed here with the
ruling. Line numbers are at `053f979`.

### 1.1 What Annex B requires (read from IEEE 1722-2016 itself)

- **Table B.7, Release! row.** PROBE: Stop probe_timer, INITIAL. DEFEND: Stop
  announce_timer, INITIAL. INITIAL: `-x-`. No Release! cell carries sProbe,
  sAnnounce or sDefend.
- **B.3.1 c) and e).** A stop action sets a timer to the stopped state, and a
  stopped timer does not expire. So no probeTimer! or announceTimer! follows the
  Release!.
- **B.3.2.** The functions, events and state changes of each state table entry
  "shall be executed sequentially". A Release! that arrives while an entry is
  executing is ordered before that entry or after it. A frame requested by an
  sProbe or sAnnounce entry that ran before the Release! belongs to that entry.
- **B.3.5.2.** Release! means the range is no longer in use and no longer
  defended, so the claim must not be published or granted after it.
- **Footnote c.** Back in INITIAL after a Release!, the range is free and the
  machine may be destroyed. It does not say that a PDU an earlier entry already
  produced is withdrawn. Both round-1 reviews read "no PDU" through `11` §6 and
  the banner, which cited footnote c for it.
- **Table B.7, PortOperational! row.** INITIAL: generate_address, then
  ReserveAddress!. PROBE and DEFEND: Stop timer, INITIAL/Restart!. So a
  Release!/PortOperational! pair must always end in a fresh walk.
- **Table F.23 (MAAP-1 to MAAP-13)** has no row that asks for a cancel (the
  ruling's reading, checked).

### 1.2 The TX path, and the ruling

The walker executes an entry over many cycles: interval draw, timer arm, TX slot
request, 60 byte writes, commit, lane grant, then the state change. The **TX slot
request** (`W_ALLOC`) is the point of no return. The top's pool-access arbiter
locks ownership to the requester until its commit, only the CA builder has an
abort input, `KL_pp_tx_slots` frees a committed slot only by sending it, and
`KL_pp_maap` has no output that could cancel or release a slot. Recalling a
requested frame would need new module ports, which is why the round first
stopped.

The ruling (option 2) accepts the drain: no cancel path, no port change. R400-1
F1's required outcome is met by three points, closed in section 2.1.

### 1.3 The rule implemented

B.3.2 decides how each Release! is ordered:

1. **A Release! before the entry's slot request** is ordered before the entry.
   The entry is dropped whole: no timer armed, no frame requested, no state
   change. The Release! then runs: teardown (both timers stopped), INITIAL. The
   states covered are `W_IDLE`, `W_RX`, `W_ADDR`, `W_IVAL`, `W_POST`, `W_OFF`,
   `W_TEARDOWN`, and a fall of a single cycle.
2. **A Release! after the slot request** is ordered after the entry. The frame
   belongs to that entry and drains as its last act. It is the only frame that
   can: the walker runs one entry at a time and never requests again after the
   fall (U28). The Release! does not wait for the frame:
   - the claim is withdrawn at the fall (`pstate` INITIAL, `addr_valid_o` low, the
     seam refuses and fans out conflicts);
   - the entry's own state change is dropped: `W_POST` does not advance `pstate`,
     so no claim is published after the fall;
   - the Release! is latched (`rel_pend_r`), so a rise before the lane takes the
     frame is never absorbed;
   - the teardown runs as soon as the lane has the frame. Until then the timers
     are not yet stopped, but an expiry meanwhile finds the machine in INITIAL
     (`-x-`): `W_POST` goes straight to the teardown, which clears it.
   - **The window**, from the slot request to the lane grant: 63 cycles when the
     pool and the lane grant at once (the unit bench), longer in the top where
     both are shared, and unbounded while the egress stalls (U25).
   The states covered are `W_ALLOC`, `W_GWAIT`, `W_WRITE`, `W_COMMIT`, `W_LANE`.
3. **Begin!/PortOperational! is the engage level seen by the released machine.**
   `W_OFF` starts a walk whenever `eng_w` is high, so a rise during the teardown
   or a drain still produces INITIAL and a fresh walk (R401-1 F2).
4. **Every Release! re-arms the footnote-a seed.** `W_OFF`, which every Release!
   reaches, clears `seed_used_r`. Within one engagement the seed is still used
   once, so a conflicted seed is not re-probed until the next Release! (R400-1 F2,
   R401-1 F1 outcome (a); the two reviewers do not conflict).

### 1.4 Checked against `11` §6 and the banner

- `11` §6 (`docs/architecture/11_maap_engine.md:136-168`) now says "no PDU
  generated after the fall" where it said "no PDU", and cites Table B.7, B.3.2 and
  B.3.5.2 for the ordering, plus B.3.1 c) and e) for the stopped timers and
  footnote c for the range being free. It states the one-frame drain and its
  window, and names U23 and U28.
- The banner (`hdl/maap/KL_pp_maap.sv:58-79`) says the same. So does REQ-MAAP-007
  in `docs/00_MILAN_COMPLIANCE_REVIEW.md:453`, whose evidence column is `11` §6.
  `tb/maap/README.md` and U14's citation (Table B.7 Release!, not footnote c) are
  aligned too.
- The in-body comments were left as they are. They describe states where
  nothing is in flight, so "no PDU" there is exact, and the mutation patches
  anchor on them.
- **seed_used_r (Observation A, R400-1 F2, R401-1 F1).** At the start head only
  the `W_IDLE` exit cleared it. The re-arm now sits in `W_OFF` (`:604`, comment
  `:315-322`), so both arcs re-arm it and P1 and P1c both probe the seed.

### 1.5 What each reviewer probe gives at the new head (section 6.3)

| Probe | Result at `053f979` |
|---|---|
| R400 P1 / P1c, R401 P1 / P1c | seed `0x2000` on both arcs: **PASS** |
| R400 P2, claim part | 0 of 160 offsets raise `addr_valid_o` after the fall (70 at the start head): **PASS** |
| R400 P2, PDU part | 64 of 160 offsets put a frame on the lane after the fall. Classified in P2's own slot: all 64 had the ANNOUNCE's slot requested by the first cycle the fall is seen, no offset has a slot request after it, and the latest lane request comes 63 cycles after the fall. This is the drain the ruling accepts. The probe's literal check still fails |
| R400 P3 (bounce inside sDefend) | claim dropped, fresh walk after: **PASS** |
| R400 P4 (Release! during a fitting draw) | 0 PDUs at all 8 offsets: **PASS** |
| R400 P5 (outage, lane stalled) | claim withdrawn, fresh walk after: **PASS** |
| R401 P2 (1-4 cycle fall in `W_IDLE`) | re-probes every time: **PASS** |
| R401 P3 (`cfg_en_i` fall 12 cycles into a walk) | 1 frame. Instrumented: the fall is first seen in `W_WRITE`, the PROBE's slot was requested before it, and there is no slot request after it. The drain the ruling accepts; the probe's literal check still fails |

## 2. Findings: change, clause, failing arm

### 2.1 R400-1 F1 (MINOR): Release! in `W_IVAL`, the TX states and `W_POST`, never absorbed

**RTL change** (`4de2c60`, `hdl/maap/KL_pp_maap.sv`):

- `:581-594` the TX states withdraw the claim at the fall and latch `rel_pend_r`;
- `:597-611` `W_OFF` starts on the engage level;
- `:660-670` `W_IVAL` tears down on a fall;
- `:719-729` `W_POST` drops the entry's state change and tears down when a
  Release! is pending or the level is low;
- `:797-805` `W_RX` tears down on a fall (a one-cycle fall was lost via
  `W_IDLE`);
- `eng_q_r` is removed.

**Clause:** IEEE 1722-2016 Table B.7 (Release! and PortOperational! rows),
B.3.2, B.3.5.2, B.3.5.9.

**Failing arm.** U23 to U26 (`tb/maap/sim_main.cpp:983-1241`, helpers
`:955-981`). They fail 13 checks against the start head's RTL
(`receipts/failing-first/f1-start-head-rtl.log`). Arms `ival-sends-after-release`,
`post-publishes-after-release`, `tx-path-absorbs-release`,
`off-waits-for-an-edge` and `rx-release-returns-to-idle` are all KILLED (6.2).

**The ruling's three points**, closed in this session:

1. **No new PDU is generated after the fall** (`d0acc9b`). New arm **U28**
   (`sim_main.cpp:1296-1462`).
   - It lands 17 falls so that the walker first sees each in a chosen state, and
     together they cover all 12 walker states:
     - `W_ADDR`, and each state of the first PROBE's entry (`W_IVAL`, `W_ALLOC`,
       `W_GWAIT`, `W_WRITE`, `W_COMMIT`, `W_LANE`, `W_POST`);
     - `W_IVAL` for the ANNOUNCE at probeCount!;
     - `W_IDLE` in PROBE and in DEFEND, parked or with a latched probe_timer or
       announce_timer expiry;
     - `W_RX` with an ignored record, and with an rProbe! that sDefend would
       answer;
     - `W_TEARDOWN` and `W_OFF`, after a rise inside the teardown.
   - The link then stays down for 33 s, longer than the longest announce interval
     (B.3.4.1). From the cycle after the first one the fall is seen, it checks:
     no TX slot request; no timer started; no timer expiry (both stopped, B.3.1
     c) and e)); no claim; INITIAL; and at most the one frame requested by then
     drains (4 of the 17 falls owe one, and each drains exactly once).
   - The wrapper exposes `walker_o` (a hierarchical read, used only to land each
     fall), `tmr_start_o` and `tmr_exp_o` (`tb/maap/maap_wrap.sv:97-100,
     177-180`), all wiring.
   - **Clause:** Table B.7 Release!, B.3.1 c) and e), B.3.2.
   - **Mutants**, both KILLED on U28 only:
     - `idle-serves-a-latched-expiry-first`: `W_IDLE` serves a latched timer
       expiry before a fall seen in the same cycle, so the 4th PROBE is sent
       after the fall. U28 x3.
     - `teardown-keeps-announce-timer`: the teardown never stops announce_timer,
       so it expires after the fall in 3 of 17 falls. U28 x1.
   - U28 also kills three older arms a second way: `ival-sends-after-release`
     (U28 x3), `rx-release-returns-to-idle` (U28 x1) and
     `drain-waits-for-the-link` (U28 x2).
   - Against the start head's RTL, U28 fails 4 checks
     (`receipts/final/failing-first/final-suite-start-head-rtl.log`).
2. **At most the one frame requested before the fall drains, within its window**
   (`4f6affc`). U23's drained arm (`sim_main.cpp:991-1069`,
   `kDrainWindowCycles = 63` at `:998`) now also requires:
   - exactly one slot request since the 4th PROBE's grant, so none after the fall
     (`:1031`);
   - the ANNOUNCE on the lane within 63 cycles of the fall (`:1035`, `:1056`).
     Measured: at most 63, at each of the 75 drained offsets. A frame that never
     reaches the lane counts as late.
   - The window is stated in the U23 comment, the README, `11` §6 and the banner:
     63 cycles in the unit bench, longer in the top, and unbounded while the
     egress stalls (U25).
   - **Clause:** B.3.2, Table B.7 Release!.
   - **Mutant** `drain-waits-for-the-link` (the lane request held until the engage
     level returns): KILLED on U23 x2, both the drain check and the window
     check (32 of 43 offsets late), and on U17c and U28 x2 behind it.
3. **`11` §6 and the banner cite Table B.7, B.3.2 and B.3.5.2** (`053f979`), with
   "no PDU generated after the fall" in place of "no PDU" (1.4). This is a docs
   change only; `make check` and `docs_check.py` stay green.

### 2.2 R400-1 F2 (MINOR) + R401-1 F1 (MINOR): seed re-arm on the `W_ADDR` arc

- **Change** (`8ae76ee`): `KL_pp_maap.sv:604`, where `W_OFF` clears
  `seed_used_r`. The `W_IDLE` re-arm is removed. The comment at `:315-322` and
  `11` §6 (`:143-147`) state one rule: every Release! re-arms the seed; within an
  engagement it is probed once, and a conflict is never answered with it.
- **Clause:** Table B.7 footnote a.
- **Failing arm.** U27 (`sim_main.cpp:1243-1294`) grades both arcs. It fails on
  the `W_ADDR` arc against the start head and against `4de2c60` (2 FAIL each;
  `receipts/failing-first/f2-*.log`). The arm `seed-rearmed-on-idle-release-only`
  (the start head's rule) is KILLED on U27 x2.
- **Verification.** R400 P1 and P1c, and R401 P1 and P1c, all probe `0x2000`.

### 2.3 R400-1 F3 (MINOR): the seed clamp's boundary

- **Change** (`fa21c58`): U18b (`sim_main.cpp:813`) seeds `0xFDF9`, which must be
  clamped to `0xFDF8`, and `0xFDF8` and `0xFDF7`, which are taken as given. Each is
  byte-exact, with no draw, in a fresh engagement. No RTL change.
- **Clause:** B.1, Table B.9, footnote a.
- **Mutant.** `seed-clamp-off-by-one` (the same line as R400's patch) is KILLED on
  U18b x2. R400's own `r400-seed-clamp-off-by-one.patch` applies verbatim at the
  new head and is KILLED on U18b.

### 2.4 R400-1 F4 (MINOR): Release! during a draw that fits

- **Change** (`2c11d6f`): U17c (`sim_main.cpp:716`) drops the link at each of the
  first 12 cycles after a rise, with every kind-7 draw fitting. It asserts:
  - nothing is sent after a pre-request Release!;
  - a draw whose answer had not arrived by the fall is abandoned, never adopted;
  - every next PortOperational! probes.

  No RTL change.
- **Clause:** Table B.7 Release! and PortOperational!, B.3.5.9.
- **Mutant.** `release-waits-for-draw` (R400's line) is KILLED on U17c. R400's own
  patch applies verbatim and is KILLED on U17c.

## 3. Suggestions

| Suggestion | Disposition | Reason |
|---|---|---|
| R401-1 F4 (Docs) | **Taken**, `8382cf6` | `KL_pp_maap.sv:613-627` and `tb/maap/README.md` name both states: `W_ADDR`'s draw arm for an unseeded walk, `W_IVAL` for a seeded one |
| R401-1 F2 (short fall in `W_IDLE`) | **Taken** inside the design, `4de2c60` | It is the same invariant F1 requires, and the fix is the same `W_OFF` level start. U26 grades 1 to 4 cycle falls and a one-cycle fall on `W_RX` |
| R401-1 F3 (PDU from `W_IVAL`/TX after the fall) | **Taken** for `W_IVAL` (`4de2c60`); for a frame already requested, closed by the ruling | U28 grades that no PDU is generated after the fall in any walker state, and U23 bounds the one frame that drains. R401-1 F3 itself asked only for a follow-up issue, which this role may not open |
| R400-1 S1 (compare_MAC low-octet pair) | Retained | Not in the round-2 assignment. `r400-compare-mac-last-octet-only` still survives, reproduced (6.3) |
| R400-1 S2 (`MUTANT_OUTPUT` default path) | Retained | Not in the round-2 assignment |

## 4. The STOP and the ruling

The STOP (5890736650) asked whether a frame whose TX slot was requested before
the fall may drain. The ruling (5890772857) chose option 2 on Table B.7's
Release! row, B.3.1 c) and e), B.3.5.2 with footnote c, B.3.2 and Table F.23.
No cancel path was added, no port changed, and no second STOP was raised. The
three points are closed in 2.1.

## 5. Parent-visible list

1. **No port, parameter or interface change.** `protocol_processor_top`,
   `KL_pp_maap` and every other module keep their port lists. Only the unit
   wrapper `tb/maap/maap_wrap.sv` (outside `hdl/`) gained observation ports
   (`slot_req_o` in the first session; `tmr_start_o`, `tmr_exp_o`, `walker_o` in
   this one). The parent's port-contract gate reads processor 1,653 first-party
   ports, 111 <= 111 undocumented, 0 hierarchical bindings.
2. **One more test-only hierarchical observation.** `walker_o` reads
   `u_dut.w_st_r`. The port-contract gate's read-only review inventory goes from
   133 to 134 "test-only hierarchical observation(s)". It is an inventory, not a
   ratchet, and the gate passes.
3. **One RTL behaviour change, dark in the parent.** `KL_pp_maap`'s Release!
   handling acts only with `cfg_maap_internal_i = 1`. The parent at dev
   `9e3ccbfb` ties it to 0, so no parent bench moves (6.4). This session changed
   no RTL logic.
4. **Processor tallies move.** `tb/maap` goes from 114 checks (start head) to 191
   (182 at the STOP head). The `run_suites.sh` total goes from 1,015,919 to
   1,015,996. The MAAP campaign goes from 16 to 27 checks (24 arms). No parent
   pin on these counts was found: the parent's `measure_test_evidence.py
   --check` inventory lists `tb/maap` only as armed by its `mutants` driver.
5. **Docs.** REQ-MAAP-007's wording in `docs/00_MILAN_COMPLIANCE_REVIEW.md`
   changed (section 1.4). The parent's `docs/reference/MILAN_COMPLIANCE_MATRIX.md`
   at `9e3ccbfb` does not quote it.
6. **Optional, unchanged from round 1.** `measure_test_evidence.py --check` still
   says the mutation ratchet can be lowered from 77 to 74.
7. **Entry points:** unchanged (`make -C tb/maap mutants`,
   `make -C tb/pp_top maap-internal`).

## 6. Gates

Tools: Verilator 5.052 (`/usr/bin/verilator`, sha256 `098b09b1…7581`) for the
processor and parent gates. The reviewers' scripts ran on their pinned 5.050
wrapper, whose `verilator_bin` sha256 is `44898b22…bfdd`, the identity R401
recorded.

### 6.1 Processor suites and entry points (head `053f979`, every one in the foreground, never piped)

| Entry point | Result |
|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 suites, **1,015,996 checks**, 0 failing. The only delta from the STOP head is maap, 182 to 191 |
| `./scripts/lint_hdl.sh` | rc 0, 40 modules LINT OK |
| `make check` | rc 0: wavedrom 18; links 925; matrix 115 REQ / 17 GAP; modmatrix 92 rows, 0 untested; params 24/24/24 |
| `python3 scripts/gen_matrix.py --check` | rc 0 (92 rows, 0 untested) |
| `git diff --check` against `c951a9ff`, `b03d36f` and `ea79d8b` | rc 0, rc 0, rc 0 |
| `make -C tb/maap mutants` | rc 0, `27 checks: 27 PASS, 0 FAIL`: 3 controls PASS, 24 of 24 arms KILLED (6.2) |
| `make -C tb/srp_top mutants` | Six `--only` batches (the whole campaign outruns one 10-minute foreground call). Every batch rc 0 with every control PASS: 56 of 56 KILLED, assertion coverage 49/49 computed over the batch logs |
| `make -C tb/nvm_port figures` | rc 0, "all measured figures agree with the tree" |
| `./syn/yosys/run.sh` | rc 0: 35 YOSYS OK, plus `KL_aecp_engine` YOSYS XILINX OK |
| `make -C tb/pp_top maap-internal` / `gsi-internal` / `name-writes` | rc 0: 33 / 6,182 / 85 checks, 0 failures |
| Failing-first: the final suite against the start head's RTL | 20 FAIL of 182: U17c x1, U23 x2, U24 x4, U25 x3, U26 x4, U27 x2, U28 x4 |

### 6.2 Mutant table (`make -C tb/maap mutants`, head `053f979`)

| Arm | Round | Named failures / suite checks |
|---|---|---|
| (controls) maap / pp_top `maap-internal` / rx_validator | | 191/0, 33/0, 453/0 PASS |
| `fit-compare-forced-true` | 1 | U17 x4, U27 x1: 5 of 191 |
| `fit-compare-off-by-one` | 1 | U17 x3, U17b x4: 7 of 190 |
| `seed-clamp-removed` | 1 | U18 x4, U18b x2: 6 of 191 |
| `release-keeps-draw-mark` | 1 | U17b x3, U17c x2, U18 x3, U27 x1: 9 of 189 |
| `validator-maap-version-1-only` | 1 | rx_validator F28 x47: 47 of 453; pp_top MP7 x4: 4 of 33 |
| `compare-mac-forward` | 1 | maap 9 of 189; pp_top MP4 x5: 5 of 33 |
| `probe-rprobe-never-yields` | 1 | U19 x2: 2 of 191 |
| `defend-rdefend-ignored` | 1 | U21 x4, U22 x4: 8 of 189 |
| `defend-rdefend-no-tiebreak` | 1 | U20, U21: 2 of 191 |
| `probe-rannounce-tiebreak` | 1 | U10 x3, U22 x2, U27 x2: 7 of 191 |
| `yield-reuses-range` | 1 | U8, U10, U15, U19, U21, U22, U27 x2: 8 of 191 |
| `ival-sends-after-release` | 2 (F1) | U17c, U23, U28 x3: 5 of 191 |
| `post-publishes-after-release` | 2 (F1) | U24 x2: 2 of 189 |
| `tx-path-absorbs-release` | 2 (F1) | U24 x4, U25 x3: 7 of 185 |
| `off-waits-for-an-edge` | 2 (F1, R401-1 F2) | U24 x2, U25 x3, U26 x3: 8 of 184 |
| `rx-release-returns-to-idle` | 2 (F1) | U26 x2, U28: 3 of 190 |
| `seed-rearmed-on-idle-release-only` | 2 (F2, R401-1 F1) | U27 x2: 2 of 191 |
| `seed-clamp-off-by-one` | 2 (F3) | U18b x2: 2 of 191 |
| `release-waits-for-draw` | 2 (F4) | U17c: 1 of 191 |
| `idle-serves-a-latched-expiry-first` | **2 (ruling point 1)** | U28 x3: 3 of 191 |
| `teardown-keeps-announce-timer` | **2 (ruling point 1)** | U28: 1 of 191 |
| `drain-waits-for-the-link` | **2 (ruling point 2)** | U23 x2, U17c, U28 x2: 5 of 191 |

The same ledger is in `tb/maap/README.md`. Its tallies match this run, R400's
`20_author_campaign.sh` and R401's `02_campaign.sh` (both 27/27 on 5.050).

### 6.3 Reviewers' round-1 scripts at the new head

Both packets were copied to scratch; the packets themselves are untouched.
Adaptations:

- R400: `common.sh` gets `HEAD_SHA`/`HEAD_TREE` for the new head (the only diff,
  `receipts/final/reviewers/r400-common.sh.diff`), with `CLONE` set to this lane.
- R401: its own environment knobs `HEAD_SHA`, `CLONE` and `VLT`.
- No reviewer patch and no probe source was edited. All 7 reviewer patches apply
  verbatim, and both probe inserters find their anchors.
- The P2 and P3 classifications (1.5) are the author's own scratch copies,
  labelled as such in `receipts/final/reviewers/r400-p2-classified.txt` and
  `r401-p3-classified.txt`.
- Not run, as before: the clone-verification scripts (`90_verify_clone.sh`,
  `09_verify_clone.sh`), R401's `05_probes_base_rtl.sh` (informational, base RTL)
  and `06`/`07` (round-1 revision lists; the parent's own idiom gates cover them
  in 6.4).

| Script | Required | Result at `053f979` (5.050) |
|---|---|---|
| R400 `10_head_suites.sh` | head green | maap 191/191, rx_validator 453/453, pp_top `maap-internal` 33/0 |
| R400 `20_author_campaign.sh` | campaign green | rc 0, 27/27, identical tallies |
| R400 `30_probes.sh` | F1: P2, P3, P5 pass; F2: P1 and P1c agree with the rule | P1 `0x2000`, P1c `0x2000`, P3, P4 and P5 PASS; P2's claim part PASS (0). P2's PDU part counts 64 of 160: all the drain the ruling accepts (1.5) |
| R400 `40_reviewer_mutants.sh` | F3 and F4 patches fail on the new named checks | seed-clamp-off-by-one **KILLED** (U18b); release-waits-for-draw **KILLED** (U17c); clears-mark-only-if-prng-idle KILLED (U17b, U17c); compare-mac-word-reversed KILLED (maap 7, MP4 5); compare-mac-last-octet-only survives (S1, retained) |
| R401 `01_head_suites.sh` | head green | maap 191/191, rx_validator 453/453, pp_top 33/0; `verilator_bin` `44898b22…` |
| R401 `02_campaign.sh` | campaign green | rc 0, 27/27 |
| R401 `03_own_mutants.sh` | each KILLED with a named U17b failure | both **KILLED** (U17b phase 1; U17b phase 3) |
| R401 `04_probes.sh` | F1: P1 passes | P1 `0x2000`, P1c `0x2000`; P2: 1 to 4 cycle falls all re-probe; P3: 1 frame, the drain the ruling accepts (1.5) |
| R401 `08_focused_static.sh` | lint and gates | lint `KL_pp_maap` rc 0, 0 warnings; gen_matrix rc 0; diff-check rc 0; 0 gitlinks |

### 6.4 Parent consumer gates (scratch parent at milan-fpga dev `9e3ccbfb`, gitlink `053f979`)

**Scratch parent** (`$VALIDATION_STORAGE/ppC2-a445/parent`):

- A `git archive` of the trusted read-only checkout at `9e3ccbfb`, committed into
  a scratch repository. Its non-gitlink tree is identical to `9e3ccbfb`
  (re-checked at this head).
- `protocol-processor` is a clone of this lane, checked out at `053f979` and
  committed as the gitlink. `gptp-processor` (`5dce647`) and
  `third_party/verilog-axis` (`48ff7a7`) are the public clones from the first
  session; `external` is uninitialised (SSH-only, read by no gate). Every
  checkout's untracked and ignored files were removed first, so nothing was
  reused from the earlier builds.
- The trusted checkout was not modified: HEAD `9e3ccbfb`, and its only non-clean
  entry is the ignored `scripts/__pycache__/` that predates this lane's sessions.

**The command set.** The same 17 commands as before: the 15 identifiable
consumer commands, plus both candidates for the sixteenth. No source this role
may read lists the manager's 16.

**Timing.** Every command ran in the foreground except `milan_dp` and
`test_builder.py`, which outrun one 10-minute foreground call and cannot be
split. Each was started detached with its rc written to a file, then waited on
in consecutive foreground calls until it exited. They ran one after the other,
never at the same time as a build of the other gates. Their rc is their own.

| # | Command (from the scratch parent root) | rc | Result |
|---|---|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet within budget; long function 0 <= 0, multi-declarator 0 <= 0 |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | all ratchets within budget |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | PASS, 4 findings == ratchet (0 in `hdl/`, 4 in pinned processors, as before) |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | OK, 106 files, 4/4 consumer lists; processor 35/41 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 6 | `python3 scripts/check_port_contracts.py` | 0 | OK: processor 1,653 ports, 111 <= 111 undocumented; 0 wildcard/positional/hierarchical binding; inventory 134 test-only hierarchical observations (133 before, +1 `walker_o`) |
| 7 | `python3 scripts/measure_naming.py --check` | 0 | PASS, 96 recorded |
| 8 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS: 74 <= 77 unarmed, 10 <= 10 unseeded, 0 <= 0 unexplained readers, 3 <= 3 wall-clock; "can be lowered to 74" |
| 9 | `python3 scripts/docs_check.py` | 0 | 0 findings |
| 10 | `python3 sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 (placement calibration), whose build report is not on this host, as recorded before. About 16 min, detached and awaited |
| 11 | `make -C tb/verilator/pp_shadow` | 0 | 4 legs PASS: 595 + 595 + 635 + 295 = 2,120 checks, 0 failures, no PINMISSING |
| 12 | `make -C tb/verilator/nvm_cosim lint` | 0 | 84 warnings, none fatal |
| 13 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| 14 | `make -C tb/verilator/milan_dp` | 0 | About 27 min, detached and awaited. Every leg PASS, no FAIL line: gptp 181, gptp-lat 181, gmstep 103, main 234, notify 381, crflic 415, nxn 1,844, nxndv 1,846, nxn8 3,524, nxn4c 1,844, nolpf 234, prune 33, ax1x1 231, aclk 190. Render and gmstep mutation controls 6/6 each. The same counts as at the STOP head |
| 15 | `make -C tb/verilator/milan_dp_render` | 0 | tdm8_render 152/152 and 65/65, `--leg-defects` 5/5 |
| 16a | `python3 protocol-processor/scripts/check-integrator-params.py` | 0 | top 24, guide 24, diagram 24, OK |
| 16b | `python3 scripts/lint_rtl.py --check` | 0 | PASS, 90 <= 90 |

## 7. Receipts

`receipts/final/` beside this file holds this session's receipts at `053f979`.
Every file is at most 200 KB, and `receipts/SHA256SUMS` lists them all:

- `processor/`: the 6.1 logs;
- `maap-mutants/`: the campaign and every arm log;
- `srp-mutants/`: the six batch lists and logs, and the coverage union;
- `failing-first/`: the final suite against the start head's RTL;
- `reviewers/`: both reviewers' receipts regenerated at the new head, the
  `common.sh` diff, and the P2 and P3 classifications;
- `parent-gates/`: logs, `scratch-parent.txt`, and the two detached rc files.

The receipts outside `final/` are the STOP-head (`ea79d8b`) set from the first
session, kept as they were. The scratch tree is `$VALIDATION_STORAGE/ppC2-a445/`. It
holds no toolchain, virtual environment or package. Logs over 200 KB stay there,
listed by size and sha256 in `SHA256SUMS`.
