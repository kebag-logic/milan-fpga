[R528] NEGATIVE - exact head 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70

# R528-1: internal cleared-context review of PR #687 (issue #665, lane F2)

- Head: `1a5d70faba6a9b01aab6bb868c12e4c7023e0c70`, tree `3a359107aafc930166375961fc18a3e93392e7e5`.
- Reviewed delta: `db9aa8c9b135b34ff3d070a979dee70440b37cc6..1a5d70fa` (one commit, 23 files).
  The wider range `021b9c1f..1a5d70fa` also carries the FC round-2 commits `021b9c1f..db9aa8c9`.
  Those belong to PR #685 and its own reviews; they were not re-reviewed here.
- Authorities read: AGENTS.md, CONTRIBUTING.md (sections 3, 5, 6), docs/README.md, issue #665 body,
  assignment 6026720272, resume 6026839422, owner directives 5992455815, 6008744385, 6009661573,
  the F2 STOP 6026825549, REVIEW READY 6028622931, issues #678 and #686, REQUIREMENTS.md section 1
  (MAAP row), FR_NFR.md (FR-MAAP-01, NFR-SCOUT-02/03/08, H-MAAP), REGISTER_MAP.md (0x654-0x65C,
  0x66C, 0x6CC, 0x750-0x760, 0x800 window), and IEEE 1722-2016 Annex B (B.1 to B.4, pages 153-163).
- Prior public findings on PR #687: none existed at this head (no reviews, no review comments;
  the two PR comments are review-start notices). Nothing to resolve or retain.
- Author packet read: `review-evidence/665f2-r1/author/HANDOFF.md` and `PR-BODY.md` at `ee59ec82`
  (sha256 match the published MANIFEST.json).

## Verdict basis

Annex B conformance of the core holds cell by cell, with one exception: the supplied-range rule
of Table B.7 note a (R528-1-F1). The executable bar reproduces at this head, but the tests are
weaker than claimed. Six real defects that I planted escaped every test (F3, F4, F5).
The differential does not state one #686 delta (F2). The CSR output's interaction with the
processor's talker gate is undocumented (F6). Six open MINOR findings make the verdict NEGATIVE.

## Findings

### R528-1-F1 MINOR - Conformance, Robustness, Tests

- Where: `sw/firmware/ctrl/maap/maap.c:182-194`, `maap.c:226-229` (PortOperational! calls
  `restart`, which calls `reserve(m, 0)` at `maap.c:117`), `maap.h:76-78`,
  `maap_mbx.c:145-149`, `app/ctrl_app.c:53`. Untested at `test/test_maap.cpp:263-267`.
- Title: a range supplied with Begin! is silently discarded when the port is not yet operational.
- Authority: IEEE 1722-2016 Table B.7 note a says a range supplied with Begin! is used and
  generate_address is not called. `maap.h:76-77` promises the same: "otherwise a valid pool
  range is used under Table B.7 note a".
- Evidence: `maap_begin` returns true and stores nothing. PortOperational! later draws a random
  range. Reviewer probe `scripts/probes/probe_preferred.cpp` (`receipts/probe_preferred.log`):
  link already up keeps `91e0f0000100`. Begin! while down, then link up, gives `91e0f000f80d`.
  `maap_mbx_start` reads the link level and then calls Begin! (`maap_mbx.c:146-148`), and
  `ctrl_app_start_maap` calls it once at startup. A link that comes up after startup, which is
  the normal case, therefore loses the application's preferred or saved range.
  `MaapCore.ReleaseLossAndRetry` drives exactly this order with `kBase` and never checks the base.
- Impact: note a's reuse of a persisted range (the #70 saved-state use) fails in the normal boot
  order. The API reports acceptance for a range it will not use.
- Required outcome: a valid supplied range accepted while not operational is the range probed
  at the next PortOperational!. Alternatively, Begin! refuses it and the header says so.
  A test pins the chosen behavior.
- Verification: the probe passes, or its refusal variant passes. A planted defect that reverts
  the behavior fails the new named test.

### R528-1-F2 MINOR - Tests, Docs

- Where: `sw/firmware/ctrl/test/test_maap_differential.cpp:102-119`,
  `sw/firmware/ctrl/maap/README.md:146-150`; parent `hdl/ieee1722/maap/KL_maap.sv:100,138`.
- Title: the differential does not state or check the parent's probe-interval delta, and the
  README misattributes another delta to #686.
- Authority: the review brief requires the differential to state each #686 delta explicitly.
  #686 lists "500 to 627 ms probe draws" (`probe_iv_w = 500 + lfsr[6:0]`) against
  B.3.4.2's open interval 500 < T < 600.
- Evidence: `ProbeSequenceWireAndCadence` checks wire bytes, probe count and the parent's
  announcement interval only. The emitted line `DIFF #686: ...` names the retransmission count,
  control_data_length and announcement interval, but not the probe interval. README:148-149
  lists five deltas without the probe interval. It also says #686 records "the parent's
  different retransmission count". The #686 body does not list that deviation
  (`PROBE_N_C = 3` total probes against Table B.7's initial sProbe plus three retransmissions).
  `receipts/issue686.json` holds the issue body as read.
- Impact: one known shipping-fabric deviation is neither stated nor bounded by the differential.
  A reader of the README is told a deviation is tracked when it is not.
- Required outcome: the differential states the probe-interval delta and checks it on shared
  stimulus (parent cadence in 500..627 ms, core strictly inside 500..600 ms). The README lists
  it. The retransmission-count deviation is recorded on #686 (a manager action), or the README
  stops attributing it there.
- Verification: rerun `maap_differential.py --self-test`. A planted change to the parent-side
  expectation fails the named case.

### R528-1-F3 MINOR - Tests

- Where: `sw/firmware/ctrl/test/test_maap.cpp:140-176` (`MaapCell.TableB7`,
  `MaapCore.ReverseOctetPriority`).
- Title: Restart!'s generate_address and most of the B.3.6.4 octet-wise comparison are unpinned.
- Authority: Table B.7 Restart! is generate_address then ReserveAddress!. B.3.6.4 compares all
  six octets in reverse order. AGENTS section 6 (Tests lens) requires that each test can fail
  for the defect it claims to detect.
- Evidence (`receipts/rmut.log`, `receipts/rmut2.log`, driver `scripts/r528_mutants.py`):
  - `r-restart-reuses-range` (`reserve(m, m->base)` on restart) escapes with rc 0. No test
    checks that a conflict selects a new range. The differential masks bytes 26..31 on retry.
  - `r-reverse-five-octets` escapes with rc 0, and so does `r-compare-mac-lsb-only` (compare
    only the least-significant octet). Every fixture pair differs in the final octet, so only
    that octet ever decides.
- Impact: a machine that re-probes the range it just lost, or ranks MAC priority on one octet,
  passes the gate.
- Required outcome: tests fail for each of these three defects. They should check that the
  base moves on Restart! for the fixed seed. They should also include MAC pairs whose last
  octets tie and an earlier octet decides (including the first octet).
- Verification: the three reviewer defects are caught by named tests.

### R528-1-F4 MINOR - Tests, Docs

- Where: `sw/firmware/ctrl/test/test_maap.cpp:319-354` (the `CsrRig` model at line 331 uses
  `regs[0x800/4] & 15` and ignores `A_STRM_SEL[8]`), `sw/firmware/ctrl/maap/maap_csr.c:60-69`,
  `maap_csr.h:34-35`, `maap/README.md:94`.
- Title: the CSR tests do not establish the talker direction or the ordered programming they
  are documented to establish.
- Authority: REGISTER_MAP 0x800: `[8]` dir (0 = listener, 1 = talker). The listener DMAC words
  are RO. README:94 says "The host CSR tests establish ordered programming". The header promises
  "invalidate before programming ... finally restore admission".
- Evidence: `r-csr-select-listener` (`STRM_SEL = k`, listener direction) escapes with rc 0.
  `r-csr-enable-before-programming` (AAF/CRF enables restored before any DMAC write) also escapes
  with rc 0. The tests check only the first two writes and the final register image.
- Impact: streams 1..N-1 could be left unprogrammed on hardware. Admission could open on stale
  destinations of a lost range. The gate would stay green and the documented claim is untrue.
- Required outcome: the register model honours the direction bit. A test pins the write order
  (enables last, after every DMAC write), so both reviewer defects fail named tests.
- Verification: both reviewer defects are caught.

### R528-1-F5 MINOR - Tests

- Where: `sw/firmware/ctrl/maap/maap_mbx.c:119-127`; `test/test_maap_mbx.cpp:79,92,281,298`
  (each stall or timing path releases interface 1 first).
- Title: per-interface poll servicing is untested at two interfaces.
- Authority: the brief asks for output order and expiry under a stalled mailbox at one and two
  interfaces. Owner directive 6009661573 keys state per AVB interface.
- Evidence: `r-poll-first-interface-only` (poll only interface 0) escapes the `maap_if2` arm
  with rc 0.
- Impact: deferred output or an owed expiry on interface 1 could starve indefinitely without a
  failing test.
- Required outcome: a two-interface test stalls interface 1's output and requires the poll to
  drain it within the H-MAAP bound.
- Verification: the reviewer defect is caught in `maap_if2`.

### R528-1-F6 MINOR - RTL, Docs

- Where: `sw/firmware/ctrl/maap/maap_csr.c:46-48`, `maap/README.md:81-95`; fabric
  `hdl/milan/milan_datapath.sv:1999-2002`, `hdl/milan/KL_pp_maap_shim.sv:76-82`,
  `docs/reference/REGISTER_MAP.md:1092` (0x66C), `docs/reference/FR_NFR.md:167`.
- Title: the documented allocation output disables the only DA source of the processor's talker
  gate, and this is not recorded.
- Authority: AGENTS section 6, RTL lens: existing module and interface contracts must remain
  valid and be understood. Assignment item 2 says the range feeds the talker's stream
  destination MACs.
- Evidence: `maap_csr_allocation` clears `MAAP_CTRL[0]`, which disables `KL_maap`.
  `aaf_gate` requires `acmp_talker_active` unless bypass is set. 0x66C says talker_active
  asserts only after a MAAP ALLOC_DA success. `KL_pp_maap_shim` answers ok = 1 only while
  `KL_maap` is in ANNOUNCE. On the current fabric, this output path therefore leaves every AAF
  talker unadmitted, and ACMP answers without a DA, even though the DMAC registers are correct.
  The README lists the platform obligations (bus ordering, window ownership, quiescence,
  boot-policy binding) but not this one.
- Impact: an integrator following the README gets no streams and no stated reason. No shipping
  or default-build effect.
- Required outcome: the README and PR record this dependency and name the integration obligation.
  Either the processor's maap face is fed from the firmware allocation, or ACMP moves to firmware
  (F3) before this output is used.
- Verification: a reviewer reads the corrected text against `KL_pp_maap_shim.sv` and
  `milan_datapath.sv:1999`.

### R528-1-S1 SUGGESTION - Tests

- `maap_mutants.py:171-187` plants each Table B.7 cell defect by injecting code keyed to the
  test's exact peer MAC constants. That proves cell independence but not robustness to stimulus.
  Generic planted defects, like my `r-probe-state-defends` and
  `r-probe-state-compare-mac-on-defend` (both caught), would be stronger evidence.
- A target debug build (assert enabled) would need the C library's assert hook. The RV32 arm
  checks only the `-DNDEBUG` build. Consider stating this.

No RESIDUE findings.

## Lens evidence (clean parts and what was applied)

- Conformance, examined: `maap.c` against Annex B, done by me.
  - B.2.1 / Figure B.1 PDU offsets 14..41, CDL 16, version 0, maap_version 1, zero stream_id,
    unicast DEFEND to the PROBE source: match.
  - B.2.2 reserved types ignored; B.2.3.2-4 version handling: match.
  - B.2.5-8 echo and intersection: match.
  - Table B.7, all 3 states x 11 events: Begin!, Release!, Restart!, ReserveAddress!,
    rProbe!/rDefend!/rAnnounce! with compare_MAC only where note d applies, probeCount!,
    announceTimer!, probeTimer!, PortOperational!. Each cell matches the literal table except
    note a (F1).
  - B.3.3/Table B.8 constants match.
  - B.3.4 strict intervals: draws are 511..589 ms and 30011..31989 ms, inside both open intervals.
  - B.3.6.1: low-32-bit MAC plus clock seed, xorshift32 period 2^32-1, unbiased rejection
    sampling; the bound of at most `size` draws holds.
  - B.3.6.3: only retransmissions decrement.
  - B.3.6.4: reverse octet order; equality returns FALSE.
  - B.4 pool bounds include the last fitting range.
  - H-MAAP checks listed in FR_NFR:409 are all present in `test_maap_mbx.cpp`.
- RTL (architecture and contracts), examined: `maap_csr.c` offsets and packing against
  REGISTER_MAP. 0x654/0x658/0x65C, 0x6CC, 0x750/0x75C/0x760 and 0x800/0x81C/0x820 match. Talker
  index >0 DMAC writes reach TCTX w1/w2 (`hdl/common/csr/milan_csr.sv:1834-1866`). `AAF_CTRL[0]`
  gates every AAF talker (REGISTER_MAP talker t>0 arming). No `hdl/`, register-definition,
  builder or shipping-image file is in the delta. `ctrl_app` is consumed only by host tests and
  co-simulation. Open: F6.
- Robustness, examined: bounded static queue (16 frames, overflow counted), two sends per call,
  owed expiry under stall, reentry guard on all six entries, stale tags, foreign interface
  records and duplicate link levels (adapter), timer wrap, malformed and truncated input.
  `mbx_tx_send` returns BAD only for static arguments. Open: F1.
- Tests, examined: full 180-defect campaign at this head (union audit), 11-defect differential
  self-test, 33 reviewer-planted defects, coverage ratchet with no new exclusion
  (`sw/firmware/gtest/README.md` unchanged in the delta). Open: F2, F3, F4, F5.
- Docs, examined: `maap/README.md`, `ctrl/README.md`, `MAILBOX_SPLIT.md:420-424`, PR body.
  Em-dash, docs_check and TOC gates pass. Claims about counts (66 cases, 180 and 11 defects,
  17 coverage files, 48-access callback, 616/664 pass bounds) match the code and my runs.
  Open: F2, F4, F6.

## Reproduced gates at this head (receipts under `receipts/`)

| Command | Exit | Result |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32` | 0 | every arm PASS, rv32 freestanding, undefined symbols libgcc + memcpy/memset/vsnprintf (`arms.log`) |
| `test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard i 4`, i = 0..3 | 0 x4 | 45+45+45+45 caught, union equals the 180-name catalog (`camp0..3.log`, `campaign_union.txt`) |
| `fw_coverage.py --check --jobs 4` | 0 | 17 files PASS. maap.c 205/205, 138/138; maap_csr.c 39/39, 18/18; maap_mbx.c 98/98, 60/60 (`coverage.log`) |
| `maap_differential.py` and `--self-test` | 0, 0 | 11 checks PASS; 11/11 differential defects caught (`diff.log`, `diffself.log`) |
| `make -C tb/verilator/mbx -j1 VBUILD_JOBS=4` on an exported copy of the head tree | 0 | WB 316, AXI-Lite 361, co-simulation 13, two-interface 316/361/316, controls 5/5 (`mbx.log`, home path redacted) |
| `tally_selftest.py`, `fw_coverage.py --selftest` | 0, 0 | `ft_selftests.log` |
| `check_em_dash.py --base db9aa8c9`, `docs_check.py`, `gen_toc.py --check` | 0 | `docs_gates.log` (the first em-dash and TOC attempts refused without the pinned renderer, then passed in its environment) |
| `scripts/r528_mutants.py` (reviewer defects) | 0 | 29 + 4 planted. Escapes: F3 x3, F4 x2, F5 x1. Three first spellings broke the build and are not counted; their corrected versions are caught (`rmut.log`, `rmut2.log`) |
| `scripts/run_probe_preferred.sh` | 1 | F1 demonstrated (`probe_preferred.log`) |

Simulator identity: `receipts/toolchain.txt` (Verilator 5.050 rev v5.050).
Restore check: `receipts/restore_check.log`. HEAD and tree are exact. Index equals HEAD, the
worktree equals the index, no assume-unchanged or skip-worktree flags, every tracked blob
rehashes equal, nothing is untracked or ignored, and the four gitlinks match HEAD (`external`
uninitialised, as at start).

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `maap.c`, `maap.h` against IEEE 1722-2016 B.2, B.3.2/Table B.7, B.3.3-B.3.6, B.4; FR_NFR:409 | R528-1 | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |
| RTL | UNCLEAN (F6) | `maap_csr.c`, REGISTER_MAP rows, `milan_csr.sv:1834-1866`, `milan_datapath.sv:1999`, `KL_pp_maap_shim.sv`; delta file list | R528-1 | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |
| Robustness | UNCLEAN (F1) | `maap.c` queue, guard, stall and expiry paths; `maap_mbx.c` tags, link, foreign, wrap | R528-1 | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |
| Tests | UNCLEAN (F2, F3, F4, F5) | `test_maap*.cpp`, `maap_mutants.py`, campaign and coverage receipts, reviewer defects | R528-1 | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |
| Docs | UNCLEAN (F2, F4, F6) | `maap/README.md`, `ctrl/README.md`, `MAILBOX_SPLIT.md`, PR body, docs gates | R528-1 | 1a5d70faba6a9b01aab6bb868c12e4c7023e0c70 |

## Real limits

- Host evidence only: no target CPU timing, wire capture, bench or hardware. Physical calibration
  was NOT RUN. The H-MAAP figures rest on the documented 100 ns-per-access model assumption.
- Not rerun by me: `ctrl_nvm` gates (no `ctrl_nvm` file in the delta), the builder bank, Yosys,
  and parent, processor or gPTP banks (excluded by the brief).
- MAAP firmware is co-simulated against the host mailbox model, not against the RTL filter. The
  RTL co-simulation arm runs the ADP composition. This is within the assignment wording.
- `--mutation-shard` partitions were run 4-way, not 8-way. The union audit, not the partition
  count, is the coverage claim.
- Hosted contexts at this head (`receipts/hosted_checks.json`, read once): rtl-fast,
  firmware-unit, full-ci-gate, docs-check-no-git, verilator-lint, yosys-elaboration,
  bdd-conformance, wire-accountability, Verilator shards 0 and 3, and Yosys shards 0-3 completed
  successfully. Verilator shards 1, 2 and 4, elaborate and docs-check were in progress.
  Physical gPTP was skipped, which is not an execution.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, and the candidate merge build against
  live dev `79b086d4` after FC (#685) lands.
- F2: record the parent retransmission-count deviation on #686, or have the README corrected.
- Re-review of the fix commit across every lens that the fix touches.

R528-1 FINISHED
