[R813] POSITIVE - exact head 5fb6904ffe12effc4bde6bf5313faea7a3beebdc

# R813-1: internal cleared-context review of PR #874 (issue #867, Mark II split S7)

- **Head:** `5fb6904ffe12effc4bde6bf5313faea7a3beebdc`, tree `7903e4d6821ca7fbd0e80a5d86220f18daf615f8`.
- **Branch:** ten commits on `dev-soft-core` `1d6bf5556ae28764361d85012b86394eb467d294`.
- **Verdict scope:** items 1 to 4, 6 and 7 and the measurements, which go to review under the ruling on the STOP (#867 issuecomment-6760813135). Item 5 is reviewed only as evidence under its test-only fixture, as that ruling accepts it. Its production-composition run is still owed, and #867 stays open for it. The PR says "Relates to #867".
- **Findings:** no BLOCKER, MAJOR, MINOR or RESIDUE. Four SUGGESTIONs, none blocking.
- **Lenses:** all five are covered clean at this head.
- **Prior review findings:** none. The PR's only earlier comments are the two review-start notices for this round's two reviews.

## How the task was reconstructed

1. **Contract.** `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
2. **Issue.** The #867 body: acceptance 1 to 7, the measurements, and what is out of scope. Then the author's TAKEN and STOP comments, and the manager's ruling issuecomment-6760813135.
3. **#665 rulings.**
   - issuecomment-6495692075: T_svc = 20 ms approved, graded per family by min(T_svc, ceiling). The SRP/MRP row is **18 ms**.
   - issuecomment-6505997821, item 3: the adapter's allocation entry is deferred.
4. **Requirements.** `docs/reference/FR_NFR.md:370`, the MRP timer row: "at most three per 1.5 x JoinTime", Milan Table 4.3 values, and an 18 ms shortest-interval margin. Also `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:222`, which says LV/rLv! is standard Table 10-4 behaviour.
5. **Diff and code.** `git diff 1d6bf555..5fb6904f`, sixteen files, read in full. Also read: the datapath's licence nets, the adapter's timer configuration, and lwSRP's anchors.
6. **Evidence.** The author's public packet at `fe59e758`, `review-evidence/665s7-r1/author/receipts`. Then my own runs, listed under Executed below.

## Item-by-item result against IEEE 802.1Q-2018 and the code

| # | Question | Result | Evidence |
|---|---|---|---|
| 1 | MRPDU form (10.8.1, 10.8.2), at most 1,500 octets, one Message per AttributeType, EndMarks, by a checker that fails on each malformation | **Holds** | See item 1 below |
| 2 | The port MAC as source from the first MRPDU after reset | **Holds** | See item 2 below |
| 3 | JoinTime and LeaveAll spacing at egress within 10.7.4 and Table 10-7, widened by the approved allowance | **Holds** | See item 3 below |
| 4 | TX ring full: no loss, order kept, the refusal reaching the firmware | **Holds** | See item 4 below |
| 6 | LICENCE reaching the policer in the split as in the all-fabric build | **Holds** | See item 6 below |
| 7 | Each plant and mutant refused by its own words, and escaping without its check | **Holds** | See item 7 below |
| (7) | The item-5 fixture cannot reach a production build; the wrappers leave the adapter and lwSRP unedited | **Holds** | See fixture containment below |
| (8) | No change to RTL, firmware, lwSRP, the mailbox contract, rings or shapes | **Holds** | See no production change below |
| 5 | #608: a withdrawal after a LeaveAll stops the talker | **Evidence under the fixture only**, as ruled | See item 5 below |

### Item 1: MRPDU form

- **The checker.** `srptx_grade.py:142-194` (`walk`) reads, for every frame:
  - the ProtocolVersion, AttributeType and AttributeLength;
  - the MSRP AttributeListLength, with its EndMark where that length ends;
  - each vector header, the LeaveAllEvent, ThreePackedEvents (no value of 216 or more, zero padding) and FourPacked;
  - the AttributeList and PDU EndMarks, and zeros only after the PDU EndMark.
- **Further checks.** `srptx_grade.py:262-297` adds:
  - at most 1,500 octets, and also a 1,500-byte frame, which is stricter;
  - one Message per AttributeType;
  - no value twice, with FirstValue + k expanded;
  - a LeaveAll on every AttributeType;
  - the group address;
  - the `srp_wire_compare` decoder on every MSRP frame.
- **Clean run.** No finding in 1,449 + 169 + 69 MRPDUs (`receipts/*-report.json`).
- **My probes beyond the author's plants.** `receipts/probe-grader.log`: 24 of 24 as expected. Each of these is refused under `[WIRE]`:
  - a PDU EndMark of 0x0100;
  - AttributeListLength +2;
  - ProtocolVersion 1;
  - AttributeLength +1;
  - an MVRP AttributeList EndMark that is not zero;
  - an MVRP Message twice;
  - an MVRP VID declared twice;
  - an MVRP MRPDU past 1,500 octets;
  - an MVRP frame sent to the MSRP group;
  - a ThreePackedEvents value of 216;
  - a nonzero byte after the PDU EndMark;
  - an MSRP LeaveAll on types 1 to 3 only;
  - a NumberOfValues past its vector.

### Item 2: source address

- **The check.** `srptx_grade.py:300-308` holds every MRPDU to `port_mac`, the bench's `twin::kEntityMac`.
- **Result.** The first MRPDU leaves at ms 1, and all are from `020000000001`.
- **Plants and mutants.**
  - The zero-source plant is refused.
  - The adapter mutant that leaves the first frame's source unset is refused: "[SA] MSRP frame at ms 1 from 000000000000".
  - My probe changing the last MVRP frame's source is refused.

### Item 3: JoinTime and LeaveAll spacing

- **The allowance is the approved one.** `srptx_grade.py:62-74` sets SVC_MS = min(20, 18) = 18 ms. That is the SRP/MRP row of the owner's per-family rule (#665 issuecomment-6495692075). It is stricter than the issue's bare T_svc of 20.
- **The bounds** in `grade_time`, `srptx_grade.py:313-364`:
  - no four MRPDUs in 1.5 x JoinTime less 18 ms (282 ms);
  - after a New, or a declaration's first message, the next message of that attribute within JoinTime + 18 ms (218 ms);
  - each LeaveAll 9,782 to 15,218 ms after the last one sent, received (the rLA! restart) or after reset, with none missing at the run's end.
- **Measured.** The README table (`tb/verilator/milan_dp/README.md:1570` onward) is reproduced exactly by my reports:
  - egress after a Join or periodic tick: 1.52 to 26.31 us;
  - JoinTime interval error: -1,011.34 to +15.48 us over 104 intervals;
  - LeaveAll error: +/-50 ms (MSRP, 39 intervals) and +/-70 ms (MVRP, 40 intervals);
  - one frame per transmit opportunity, over 727 MSRP and 722 MVRP opportunities.
- **The JoinTime follow-up check is not vacuous.** `receipts/time-coverage.log`: it is evaluated on 6 MSRP and 1 MVRP declarations in each scenario, with a worst gap of 200.000 ms against 218. None is skipped by the "frame received between" exemption.
- **Boundary probes.**
  - A second frame exactly 218.0 ms after the New's egress is accepted.
  - At 218.2 ms it is refused under `[TIME]`.
  - Four MSRP opportunities in 280 ms are refused.
  - A peer LeaveAll 1 s before a sent one is refused for the sent one.

### Item 4: full TX ring

- **Alignment.** `grade_tx`, `srptx_grade.py:424-481`, aligns what the adapter accepted with what left the MAC, by position, byte for byte.
- **Refusals.** Every refusal must have had too little room. The refused MRPDU must be the next one of its protocol accepted. Each hold must show at least one refusal.
- **What the refusal means.** The refusal is the adapter's own return to lwSRP, recorded at the send callback (`srptx.hpp:454-474`). Ring use is computed from TX_HEAD and TX_TAIL as the firmware wrote and read them (`srptx.hpp:254-273`). So the RTL backpressure (`twin_split.cpp:325`, the MAC's `tx_tready` = 0) reaches the firmware.
- **Hold result.**
  - The ring held 507 of 512 words, and a 30-word record was refused from 24,600 ms to 25,000 ms.
  - That MRPDU was retained and sent first.
  - 169 MRPDUs were accepted and 169 sent, with no finding.
- **Wire-scenario probes.** Each of these is refused under `[TX]`:
  - a duplicate frame;
  - a frame lost outside a hold;
  - a frame 2 ms late;
  - a FirstValue bit flipped on the wire;
  - a far reorder.

### Item 6: licence at the policer

- **The wiring.** In the split, `hdl/milan/milan_datapath.sv:9981-9982` drives both `pp_cd_srp_active_w` and `pp_cd_srp_sr_admitted_w` from `i_ctl_pub_licence`. The stream gate, `milan_datapath.sv:8831-8832` (ACTIVE AND admitted), and its consumers sit outside the generate. They are one RTL in both placements: the AAF gate at 2320-2323, the CRF terms at 7150-7151.
- **`[POL]`** (`sim_split.cpp:329-349`) writes each bit alone and checks ACTIVE, admitted, the gate and the CRF top-bit term, then clears the register. `receipts/split.log`:
  - LICENCE 0x0001 gives active, admitted and gate 0x0001, crf 0;
  - LICENCE 0x0002 gives 0x0002, crf 1;
  - 82 checks, 0 failures.
- **`[LIC]`** holds the same at every millisecond of the licence scenario.

### Item 7: plants and mutants

- **Capture plants.** `receipts/srptx.log`: 23 of 23 refused by their own words. No word appears in its unplanted capture.
- **Code mutants.** `receipts/srptx-mutants.log`: 10 of 10, after clean controls for every scenario and length an arm runs.
- **Split-leg arms.** `receipts/split-mutants.log`: 26 of 26, including the two new `[POL]` arms (`split_mutants.py:47-54`).
- **The five the issue names**, each planted both in a capture and in code:
  - a malformed EndMark;
  - a doubled declaration;
  - a LeaveAll on the wrong type;
  - a frame dropped under backpressure (the adapter reports a refused MRPDU as sent);
  - a zero source address.
- **Escaping without its check.** `receipts/knockout.log`: with each plant's own check disabled in a disposable copy of the grader, 23 of 23 plants lose their words.
  - Twelve then escape entirely.
  - The other eleven are still refused by a second, independent section. Six by `[TX]`'s byte-for-byte alignment, three by another `[WIRE]` rule or the decoder, one by `[TIME]` and one by `[LIC]`. That is overlap between checks, not a dependence.

### Fixture containment and the link-time wrappers

- **One translation unit.** `srptx.hpp` is included only by `twin_split.cpp:63`.
- **One link.** `SRPTX_WRAPS` (`Makefile:931`) is used only on `build-twin-sp`'s link (`Makefile:932-936`). `git grep` finds no other `--wrap` or `__wrap_` in any firmware, LiteX or builder path.
- **One scenario.** `__wrap_srp_mbx_init` (`srptx.hpp:567-579`) changes nothing unless `rec().fixture` is set. Only `scenario("licence")` sets it (`srptx.hpp:338-340`), before boot.
- **Pass-through elsewhere.** Every other wrapper passes straight through when the recorder is off.
- **Twin unaffected.** The twin's split capture with the wrappers linked is byte-identical to the base build's: sha256 `ee143865…` (`receipts/twin-split-identity.txt`). The base tree's `milan_dp` files match the base blobs (`receipts/basetree-identity.txt`).
- **Adapter and lwSRP unedited.** Neither `sw/firmware/ctrl/srp/*.c` nor `third_party` changes. The `third_party` tree is `6604713e…` at both base and head.

### No production change

- **Unchanged paths.** `git diff --stat 1d6bf555..5fb6904f` is empty for all of these:
  - `hdl`;
  - `sw/firmware/ctrl`, apart from `test/ctrl_configs.py` and two READMEs;
  - `third_party`, `protocol-processor` and `gptp-processor`;
  - `configs`, `sw/litex` and `sw/builder`.
- **Changed paths.** `tb_split_top.sv` is a bench top that gains probe outputs. `twin_fw.py --replace` is empty by default.
- **Gitlinks.** Every gitlink is unchanged.

### Item 5, under the fixture only, as ruled

- **Stop timing.**
  - The peer's LeaveAll arms the Leave timer at 16,001 ms (500 cs).
  - The withdrawal in LV at 18,000 ms re-arms nothing.
  - The timer expires at 21,000 ms, and LICENCE clears at 21,000.012 ms.
  - The gate closes in that millisecond. The last of 102 stream frames left at 20,946 ms.
- **Mutant.** The lwSRP mutant that restarts LeaveTime on rLv! in LV is refused at 23,000.012 ms.
- **Expected behaviour.** The stop is expected at LeaveAll + LeaveTime, within -10 / +18 ms. That follows the standard Table 10-4 LV/rLv! row, as `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:222` and the README's authority column read it.
- **What this does not prove.** It is evidence of behaviour, not the production composition.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

**[R813] S1 SUGGESTION**
- **Lens:** Docs.
- **Where:** `docs/design/MAILBOX_SPLIT.md:1855-1857`; `sw/firmware/ctrl/srp/README.md:386`.
- **Title:** Say where the licence path holds without the fixture.
- **Authority/evidence:** Both pages say the licence at the policer holds in `make srptx` "only under" the fixture. That is literally true of `make srptx`. But `make split`'s `[POL]` holds the same path per bit with no fixture (`sim_split.cpp:329-349`), and only the `milan_dp` README says so (`tb/verilator/milan_dp/README.md:1567`).
- **Impact:** A reader of these two pages alone may take item 6 as fixture-only.
- **Optional change:** Add "`make split`'s `[POL]` holds it without one".
- **Verification:** Read.

**[R813] S2 SUGGESTION**
- **Lens:** Tests.
- **Where:** `tb/verilator/milan_dp/srptx_grade.py:542`.
- **Title:** The CRF bit is fixed at gate bit 1.
- **Authority/evidence:** `[LIC]` compares `crf_active` with `gate & 2`. That is the twin's single 1x1 shape, two talkers with CRF on top. `[POL]` derives the top bit from `p_n_talkers`.
- **Impact:** None at the shape `srptx` runs. The bit would be wrong if the scenario ever ran at another shape.
- **Optional change:** Record the stream gate's width in the capture and use its top bit.
- **Verification:** A capture with a different width.

**[R813] S3 SUGGESTION**
- **Lens:** Tests.
- **Where:** `tb/verilator/milan_dp/srptx.hpp:403-405` and `:481`.
- **Title:** srptx captures are not byte-reproducible.
- **Authority/evidence:** Each timer event's `id` is the timer's address, so every run's capture differs. My three captures have the same lengths as the author's but different hashes. The graded reports are identical field for field. Two runs of one binary differ only in `id` (`receipts/srptx-repro.txt`).
- **Impact:** A capture cannot be compared by hash across runs or hosts, the way the twin's is.
- **Optional change:** Emit a stable per-timer index instead of the address.
- **Verification:** Two runs, equal hashes.

**[R813] S4 SUGGESTION**
- **Lens:** Tests.
- **Where:** `tb/verilator/milan_dp/srptx_grade.py:246-249`.
- **Title:** The hold exemption is matched by position.
- **Authority/evidence:** `accepted_ms` is matched by `zip` position. After one real loss, every later frame's acceptance time drifts, and the hold exemption no longer applies. With `[TX]`'s alignment knocked out, one dropped frame produced 23 `[TIME]` rate findings (`receipts/knockout.log`).
- **Impact:** Only noise after a genuine `[TX]` finding, which still names the loss first.
- **Optional change:** Reuse `grade_tx`'s alignment for `accepted_ms`.
- **Verification:** The dropped-under-backpressure plant yields its `[TX]` finding alone.

## Clean-lens evidence

**[R813] PASS Conformance**
- **Where:** `tb/verilator/milan_dp/srptx_grade.py:62-74, 142-308, 313-364, 424-481, 501-558`; `hdl/milan/milan_datapath.sv:8831-8832, 9981-9982`; `sw/firmware/ctrl/srp/srp_mbx.c:252-253`.
- **Checked:** Acceptance items 1 to 4, 6 and 7, against IEEE 802.1Q-2018:
  - 10.8.1 and 10.8.2;
  - 10.7.4.1, 10.7.4.3 and 10.7.9;
  - Tables 10-3, 10-4, 10-5 and 10-7.
- **Also against:** `FR_NFR.md:370`, the 18 ms SRP/MRP row of #665 issuecomment-6495692075, and the ruling on the STOP. Item 5 is checked as evidence under the fixture, as ruled.

**[R813] PASS RTL**
- **Where:** `tb/verilator/milan_dp/tb_split_top.sv` (the new probe outputs); `hdl/milan/milan_datapath.sv:2320-2323, 7150-7151, 8831-8832, 9981-9982`.
- **Checked:**
  - No synthesised RTL changes.
  - The probes are read-only.
  - The licence-to-gate path is per bit and shared between placements.
  - The `[POL]` arms (the next source's ACTIVE term, the CRF term on gate 0) are caught.
  - `twin_split.cpp`'s backpressure drives the real MAC `tx_tready`, and its drain is inactive outside `--srptx` (the twin capture is identical).

**[R813] PASS Robustness**
- **Where:** `receipts/probe-grader.log`, `knockout.log`, `srptx.log` (hold and licence scenarios), `srptx-mutants.log`.
- **Checked:**
  - Truncated and malformed MRPDUs.
  - Maximum size.
  - Reorder, duplicate, loss and lateness on the wire.
  - A full ring, with retention and refusal under 160,001 retries.
  - Repeated peer LeaveAll.
  - A withdrawal in LV.
  - Timing boundaries at 218.0 ms (accepted) and 218.2 ms (refused).
  - Fixture-off behaviour, by the twin's identity.

**[R813] PASS Tests**
- **Where:**
  - `tb/verilator/milan_dp/srptx_plants.py`, `srptx_mutants.py`, `split_mutants.py:47-54`, `sim_split.cpp:329-349`;
  - `receipts/srptx.log` (23 of 23), `srptx-mutants.log` (10 of 10), `split-mutants.log` (26 of 26), `split.log` (82 checks, 0 failures), `twin.log` (20 plants, rc 0), `knockout.log` (23 of 23), `test_evidence.log` (ratchet PASS).
- **Checked:**
  - Each new check fails for its own defect.
  - Each plant escapes without its check.
  - Clean controls precede every arm.
  - Build failure is not counted as a catch.

**[R813] PASS Docs**
- **Where:** `tb/verilator/milan_dp/README.md:1488` onward; `docs/design/MAILBOX_SPLIT.md:1849-1858`; `sw/firmware/ctrl/srp/README.md:380-390`; `sw/firmware/ctrl/README.md:255`; the PR body; `receipts/docs_check.log` (0 findings).
- **Checked:**
  - Every README figure against my own reports.
  - The fixture and its limit stated where the check is described.
  - The 183 pin-control count. It is the only difference from `bf1bba25`, and the author's firmware-boundary receipt reads `ctrl_boundary: PASS` at the head.
- **Comment rule.** The added source comments carry no lane label, review round, reviewer ID or comment ID. The README's #665 comment links follow the base pages' existing citation form, and the rule covers source comments.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srptx_grade.py` (form, SA, TIME, TX, 608, LIC); `milan_datapath.sv` licence nets; `srp_mbx.c` timers; the #867 body and ruling; the #665 per-family rule; `FR_NFR.md:370` | R813-1 | `5fb6904ffe12effc4bde6bf5313faea7a3beebdc` |
| RTL | CLEAN | `tb_split_top.sv` probes; `milan_datapath.sv` gate, AAF and CRF terms; `twin_split.cpp` backpressure and drain; the base..head stat (no `hdl` change) | R813-1 | `5fb6904ffe12effc4bde6bf5313faea7a3beebdc` |
| Robustness | CLEAN | 24 reviewer probes; the hold and licence scenarios; 10 code mutants; fixture-off identity | R813-1 | `5fb6904ffe12effc4bde6bf5313faea7a3beebdc` |
| Tests | CLEAN | `srptx_plants.py`, `srptx_mutants.py`, `split_mutants.py`, `sim_split.cpp` `[POL]`; plant, mutant, knockout, split, twin and ratchet receipts | R813-1 | `5fb6904ffe12effc4bde6bf5313faea7a3beebdc` |
| Docs | CLEAN | the `milan_dp` README section, `MAILBOX_SPLIT.md`, the srp and ctrl READMEs, the PR body; `docs_check.py` | R813-1 | `5fb6904ffe12effc4bde6bf5313faea7a3beebdc` |

The SUGGESTIONs S1 to S4 do not affect coverage.

## Executed in this round (foreground or waited on; pinned Verilator 5.050)

All of these ran on this clone at the exact head; see `COMMANDS.md`. Each exited rc 0.

- `make srptx`: three scenarios, 0 findings each.
- `srptx_plants.py`: 23 of 23.
- `srptx_mutants.py`: 10 of 10.
- `make split`: 82 checks, 0 failures.
- `make split-mutants`: 26 of 26.
- `make build-twin`, then the `twin` and `twin-plants` recipes: compare rc 0, 20 plants.
- The base build's twin split capture: identical to the head's.
- `docs_check.py` and `measure_test_evidence.py --check`.
- Three reviewer scripts, on the head's captures: `probe_grader.py` 24 of 24, `knockout.py` 23 of 23, and `time_coverage.py`.
- **Restored afterwards.** Tree `7903e4d6`, clean index and worktree, every required gitlink matching (`receipts/restore-check.txt`). `external` is uninitialised and no gate here needs it.

## Real limits

- **Not run by me:**
  - the full sweep;
  - the per-step replay of the CI workflows;
  - the firmware self-test and boundary self-test, including the 183 pin-control figure;
  - `test_builder.py`;
  - the CPU budget harness;
  - `split-cdc`;
  - `split_parallel.py --selftest`;
  - the docs workflow beyond `docs_check.py` and the ratchet.
  For these I relied on the author's receipts at `fe59e758`. They show `ctrl_boundary: PASS` at the head, and the sweep at 65 suites, 2,192,910 checks, 0 failures.
- **Clause text.** The IEEE 802.1Q-2018 and Milan v1.2 text was read through the repository's requirement rows and findings pages, and through the code, not from the standards themselves.
- **One shape, one interface.** Only AX7101 1x1 with one interface, as the two-placement simulation runs.
- **Simulated time.** The firmware's instructions take no simulated time. The measured egress figures are the RTL path's alone.
- **Hosted checks at this head.** 43 success, 1 skipped, 17 cancelled and 8 failure (`receipts/hosted-check-runs-5fb6904f.tsv`).
  - The Verilator and Yosys shards, `rtl-fast` and `publication-census` were cancelled, all completing between 07:45Z and 07:46Z.
  - The `Union` jobs, and `verilator-suites` and `yosys-portability`, then failed. `Union milan_dp`'s log shows the cause: an assertion that `verilator-shards` was `cancelled`, not a test failure.
  - No exact-head `verilator-suites` or `yosys-portability` pass exists yet.
- **No hardware.** No hardware or physical calibration was run. Field skips are not hardware proof.
- **Not inferred.** No manager source bank is claimed or inferred.

## Pending manager duties

- **Hosted gates.** Re-run, or accept, the exact-head hosted long gates (`verilator-suites`, `yosys-portability`) and `rtl-fast`, all cancelled at this head. Own the hosted and act acceptance.
- **Merge candidate.** Build and validate the current-dev merge candidate (source base `dev-soft-core`, live dev `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`) with the builder and native banks, and link the receipts on the PR.
- **Item 5.** Keep #867 open for item 5 in the production composition. Once #810 merges, the short round re-runs `[608]` without the fixture and removes it (ruling issuecomment-6760813135).
- **New Issues.** File the two items found and not fixed here. Neither has an Issue yet.
  - The split's AAF frames carry stream_id 0, because no firmware writes `SRC_SID`.
  - The twin's split half sends a frame that follows another about 10 to 11 modeled ms late. It is a bench artifact that the `--srptx` drain removes, and the twin itself is unchanged.
- **Second review.** Obtain the second independent review, then the explicit merge authorization.
- **Evidence handling.**
  - `$HOME` replaces the host's home path in four published build logs.
  - Under `scratch/` (not published): the captures, the base tree and probe copies.

R813-1 FINISHED
