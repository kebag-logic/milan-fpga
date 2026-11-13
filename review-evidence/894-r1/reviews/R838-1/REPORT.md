[R838] NEGATIVE - exact head 12180198b087d4cfdd531d0de5d3753211b35616

# R838-1: external review of PR #902 for issue #894, the control loop served in tiers

Round R838-1 is the external independent review. It is a full review of the lane's whole diff,
`66f713267f201d1a00d7f711e04b3a996d804dee..12180198b087d4cfdd531d0de5d3753211b35616`. That is round 1's
model commits (`04d3c1cc`, `f9442a10`) and round 2's build (`3f469cef` to `12180198`). The tree is
`120938b3c677bc899acc258fbde163e7cba0688a`. The clone is detached at that head, and the final check
re-verified it (`receipts/restore_verification.txt`).

**Verdict: NEGATIVE.** The build matches the ruling in most places. The two tiers are built as stated.
The owed-notice queue meets conditions (a) to (d). The resumed SRP build sends the same frames. I
reproduced the slice rule's pick of 1,200 us. `flip_grade.py --check --point 1x1/1if` passes, the
load is 0.470 at the pin, and every lane plant I re-ran is caught.

Two MAJOR findings leave the tier bounds not held by every source at 1x1/1if:

- **F1.** Under AECP-first, the binding tier-1 record is now another channel's, ACMP's, and no row
  covers it. By every source it is over 20 ms.
- **F2.** The MRPDU bound loses its by-construction proof and has no every-source bound. The
  requirement row now names an open decision, and nothing at this head rules on it.

There are also five MINOR findings and one RESIDUE.

## Context reconstructed (public state only)

I read these before any judgement:

- `AGENTS.md`, `CONTRIBUTING.md` sections 3 and 6, and `docs/README.md`.
- Issue #894: its body, acceptance and scope, saved as `receipts/public/issue894*.json`.
- The round 1 STOP (issuecomment-6813751879).
- The ruling on it (issuecomment-6813855717): the `aecp_ready` change under (a) to (d), and the slice
  with the largest least relative margin at 1x1/1if.
- The owner's option A (issuecomment-6814835849).
- The round 3 ruling on F1 (issuecomment-6839847820).
- The REVIEW READY (issuecomment-6839788052) and the PR #902 body.
- From #665, the authorities the lane cites:
  - the round 23 ruling, issuecomment-6732443213;
  - decision D, issuecomment-6759183115;
  - the 2026-11-06 maintainer ruling, issuecomment-6681686082.

  All three are saved under `receipts/public/`.

**Executable evidence.** I fetched the author packet `review-evidence/894-r1` at `61a7204d` into a
scratch-only bare repository and read it. I read no private author material and no other reviewer's
report.

**Prior public review findings.** None exist on PR #902 at the time of this pass. The PR has two
comments, both review-start notices, and no reviews or review comments
(`receipts/public/pr902_*.json`). Issue #894 carries no review findings either. Nothing is carried
over to resolve or retain.

## Findings

### F1 MAJOR: under AECP-first, another tier-1 channel's records miss 20 ms by every source, and no row covers them

Lenses: **Conformance, RTL, Tests**.

**Where.**

- `sw/firmware/ctrl/loop/ctrl_loop.c:293-310`: AECP first. The other tier-1 channels are swept only
  once AECP's take left none (`sweep = l->rx_left == 0u`).
- `tb/verilator/ctrl_service_budget/rows_tiers.py:81-82` and `:330-335`: the tier-1 rows are only `R4`
  (AECP's own last record) and `first`.
- `flip_grade.py` holds only those rows.

**Authority.**

- #665 round 23: tier 1 is "the response channels: AECP, ACMP and ADP records", at 20 ms. "No row may
  be held by measurement alone."
- #894 acceptance: "every row by every source within its tier's bound".
- FR_NFR 3.4.1: ACMP's ceiling is T_svc, 20 ms.

**Evidence.**

- Before the tiers every channel was served in turn, so AECP's last record (R4) stood for tier 1. The
  ruling of 2026-11-12 chose AECP-first so that R4 fits. Under that order, ACMP, ADP and MAAP are served
  only after every AECP record that arrives in their window.
- My probe `scripts/tier1_other_rows.py` reuses `rows_tiers.tiered`'s per-pass terms at the built
  design's inputs. It charges all AECP arrivals ahead, the channel's own burst, and the other channels
  in turn. It finds the last record of ACMP's burst at 1x1/1if:
  - **27.26 ms by every source** at the pass count of R4's convention;
  - **22.72 ms** even with the fewest passes (every tier-1 record taken past its cap, no pass lost to a
    centisecond);
  - either way over 20 ms;
  - the terms: AECP's arrivals 4.70, ACMP's own burst 4.48, AECP's owed frames 2.10, and the per-pass
    terms (`receipts/model/tier1_other_rows.txt` and `_lean.txt`).
- ADP's and MAAP's analogues are also over 20 ms, but my "others in turn" charge for them is coarser.
  I state them as indicative.
- The author's own `tx` row, a unit behind every tier-1 arrival, is 29.00 ms at 1x1/1if by the same
  model.
- By measurement ACMP is already the worst tier-1 channel: 6.562 ms in the REVIEW READY, against
  AECP's 4.605. That fits ACMP now being the binding row.

**Impact.** The flip check passes at 1x1/1if while a tier-1 response channel is held by measurement
alone. Under contract-rate AECP input, an ACMP command (the response channel of a stream connect) can
wait past T_svc. That is the failure class the every-source rule exists to catch, and the change this
PR builds creates it.

**Required outcome.** Either of:

- Solve the last record of each tier-1 channel's burst (ACMP, ADP, MAAP) by every source under the
  built design. Hold the rows in `flip_grade.py --design built`, with plants. If one misses, the issue's
  scope item 3 STOP applies.
- Get a recorded maintainer ruling that R4 alone stands for tier 1 under AECP-first.

**Verification.** `rows_tiers.py --terms` lists those rows at 1x1/1if within 20 ms, or the ruling is
linked. `flip_grade.py --check --point 1x1/1if` holds them. `flip_grade.py --selftest` refuses each
row's over and within plants.

### F2 MAJOR: the MRPDU bound loses its by-construction proof and is held by measurement alone

Lenses: **Conformance, Docs**.

**Where.**

- `docs/reference/FR_NFR.md:396`: the SRP/MRP row's service text is rewritten to "which bound holds it
  under the tiers is an open decision on #894".
- `sw/firmware/ctrl/loop/ctrl_loop.c:199-202`: the `_Static_assert(CTRL_LOOP_TX_MS <= CTRL_LOOP_T_SVC_MS)`
  is removed, and so are `CTRL_LOOP_TX_MS` and `CTRL_LOOP_SRP_MS` (`ctrl_loop.h`).
- `rows_tiers.py:461-470`: `tx_row` is "reported" against 20 ms and gated nowhere.

**Authority.**

- The maintainer ruling of 2026-11-06 (#665 issuecomment-6681686082, item 3): every MRPDU a join,
  periodic or LeaveAll timer owes is within 20 ms "by construction ... with a compile-time check".
- Round 23 (item 3): "No row may be held by measurement alone".
- #894 scope: "The bounds ... and the every-source rule are not changed in this lane".
- No later ruling sets the MRPDU's bound under the tiers. Round 23 gives tier 2's 90 ms to R5 and R6,
  the round 1 STOP ruling names five rows, and the round 3 ruling covers F1 only.

**Evidence.** `rows_tiers.py --terms` gives the MRPDU row as **29.00 ms by every source at 1x1/1if,
+9.00 over 20** (`receipts/model/rows_tiers_terms.txt`). The PR's own "Known limitations" calls it an
open decision.

**Impact.** A normative bound in FR_NFR 3.4.1 goes from proved at compile time to "open". Only the
harness's measurement (1.052 ms) holds it. Merging would put in `dev` a requirement row that states no
bound, and a change to the every-source rule that #894's scope forbids.

**Required outcome.** A recorded maintainer or owner decision on the MRPDU's bound under the tiers. For
example, tier 2's 90 ms by every source, held by `flip_grade.py`. FR_NFR 3.4.1 then cites that decision
and the bound is gated with a plant. Otherwise, restore an every-source 20 ms bound.

**Verification.** FR_NFR names the bound and its decision. `flip_grade.py --check --point 1x1/1if`
holds `tx_row` at that bound. A plant over it is refused.

### F3 MINOR: no test fails when the poll stops reporting a longer notice still owed behind a just-drained queue

Lenses: **Tests, Robustness**.

**Where.** `sw/firmware/ctrl/aecp/aecp.c:731`, `return a->owed_count != 0u || a->notify;`.

**Evidence.** My disposable probe rp2 drops `|| a->notify` (`scripts/reviewer_probes.py`). The AECP
arm then reports **0 failing tests** (`receipts/runs/rprobe_aecp.log`).

**Impact.** With that defect, a poll that sends the queue's last notice while a longer notice waits in
the response buffer reports nothing owed:

- `aecp_poll` goes on to `asynchronous()`, whose lock expiry clears `a->notify` (`aecp.c:754`) and
  whose unlock notice and probes rewrite `a->response` (`aecp.c:760-779`);
- the waiting notice can be lost;
- the loop can sleep while it is still owed.

The head is correct today, but the new branch has no check that would catch a regression.

**Required outcome.** A test that fails on that defect. For example, after the queue's last drain the
poll reports a notice still owed, and the longer notice survives a due lock expiry. Add a plant row
naming it.

**Verification.** The plant is caught by its named test's words.

### F4 MINOR: no check fails when an ordinary pass's round keeps `round_one` from a pass given whole

Lenses: **Tests**.

**Where.** `sw/firmware/ctrl/loop/ctrl_loop.c:330`, `l->round_one = false;`.

**Evidence.** Probe rp3 removes that line. The port arm, `Loop.*`, reports **0 checks failed**
(`receipts/runs/rprobe_control.log`). Only the whole-pass assignment is checked
(`test_port_loop.cpp:1388`, `:1684`).

**Impact.** A pass given whole can set `round_one`. If the line is lost, a later round in a pass that
took nothing stays limited to one notice (`aecp_mbx.c:287`). The last queued notice's rounds would then
be shorter than `rows_tiers` counts, and no test would see it.

**Required outcome.** A loop check that this round is told `round_one` false after a pass given whole
set it, with a plant.

**Verification.** The plant is caught by that check's words.

### F5 MINOR: MAILBOX_SPLIT states a 1.05 ms slice at 1x1/1if; the tree's slice is 1,200 us

Lenses: **Docs**.

**Where.** `docs/design/MAILBOX_SPLIT.md:347` says "(1.05 ms at 1x1/1if, 1.3 ms at 8x8/2if)". The
tree says `CTRL_LOOP_SLICE_US (MBX_N_IF == 1u ? 1200u : 1300u)` (`ctrl_loop.h:268`).

**Evidence.** `8cc3e5d3` moved the slice to 1,200 us, and `12180198` restated the other documents but
not this one.

**Impact.** An authoritative design document states a stale figure for the slice that bounds every
tier-2 row.

**Required outcome.** State 1,200 us at 1x1/1if.

**Verification.** A grep of the docs for the 1x1/1if slice finds only 1,200 us.

### F6 MINOR: the order of the other tier-1 channels is misdescribed

Lenses: **Docs**.

**Where.** `docs/design/SPLIT_CONTROL_MEMORY.md:2169` says "then ACMP's, ADP's and MAAP's, each only
once the channel before it left no record it would take". The PR body's Description table says the
same.

**Evidence.**

- The code sweeps the other tier-1 channels in turn, a channel on each pass, gated only on AECP's take
  (`ctrl_loop.c:298-310`).
- `Loop.L25` asserts "one a channel in turn" (`test_port_loop.cpp:1551`).
- `ctrl_loop.h:191-193` states it correctly: "every other tier-1 channel's records only once it holds
  none, each its due, then ... one a channel in turn".

**Impact.** A reader, or a model of the tiers, takes ACMP, ADP and MAAP to be served one after the
other. That understates ADP's and MAAP's exposure and misdescribes the order F1 turns on.

**Required outcome.** Restate both places to match `ctrl_loop.h`.

**Verification.** The text and `Loop.L25` agree.

### F7 MINOR: the SRP build's Domain claim does not hold where a slice makes one MRPDU (8x8/2if)

Lenses: **Docs**.

**Where.**

- `sw/firmware/ctrl/srp/README.md:239`: "A Domain adopted in that call is sent in it, so no poll sees
  the new VID unlicensed between the adoption and its MVRP commit (Milan 4.3.2)".
- `sw/firmware/ctrl/srp/srp_mbx.c:1093-1094`: the same claim in the comment this delta rewrote.

**Evidence.**

- At 8x8/2if `CTRL_LOOP_BUILD_MOST` is 1 (`ctrl_loop.h:313`).
- The MSRP MRPDU is sent in the first slice and the MVRP MRPDU in the next (`srp_mbx.c:1114-1119`).
  Polls run between them.
- The licence still waits on `vlan_sent` (`srp_mbx.c:786`, `:1050`), so Milan v1.2 4.3.2 (MVRP join
  before the stream) is kept.
- The PR body states this as interpretation I3. Only the README and comment claim says otherwise.

**Impact.** The SRP README and its source comment state a behaviour the 8x8/2if image does not have.

**Required outcome.** State that where a slice holds one MRPDU, the MVRP follows in the next slice and
the licence waits for its commit (Milan v1.2 4.3.2).

**Verification.** The README and comment match `transmit`.

### RS1 RESIDUE: new source comments name a review round

Lenses: none (RESIDUE). This is the owner's comment rule of 2026-10-15.

**Where.** 14 new instances of "#665 round 23" or "round 23 ruling" in source comments and docstrings
of the delta (`receipts/residue_round_refs.txt`):

- `aecp_mbx.h:34`;
- `ctrl_loop.h:183`, `:261`;
- `srp_mbx.c:1093`;
- `loop_step_mutants.py:278`;
- `srp_mbx.cpp:1581`;
- `srp_transmit_mutants.py:33`;
- `rows_tiers.py:3`, `:42`, `:52`, `:78`, `:261`;
- `selftest_round.py:85`;
- `slice_grade.py:3`.

**Exact fix.** Cite the decision by issue and date, not by round. For example, "(#894; #665, the
maintainer decision of 2026-11-09, option B)", or "(#665, item 2 of the decision of 2026-11-09)".

### Suggestions (optional)

- **S1. A consequence of the ruled ordering.** Under the queue, controller B's response to its own
  command can precede A's earlier notice. If both commands set the same field (two SET_NAMEs), B
  receives A's notice after its own success, and B never receives its own notice. B's cached value then
  ends at A's, while the entity holds B's. The ruling (issuecomment-6813855717) explicitly allows a
  response ahead of an owed notice. I record the consequence so the owner can confirm it is accepted.
  It could be added to `aecp/README.md` beside conditions (a) to (d).
- **S2. A redundant line.** `aecp.c:724` (`a->counter_event = a->cfg.model->count;`) is redundant.
  Every queued notice's command already ran `header()`, which resets it (`aecp.c:141`), and no scan runs
  while the queue holds one (`round_waits`). Probe rp1 fails no test for that reason. Keep it as a
  stated guard or drop it.
- **S3. The behave layer.** `tests/steps/aecp_owed_notice_steps.py` is a Python model of the queue's
  rules, pinned to the firmware by text. It meets condition (d) literally, and the firmware behaviour
  is proved by `Queued.*`.
- **S4. Datapath sample size.** The datapath sink costs rest on 8 instances of each event at 1x1/1if
  and 16 at 8x8/2if (the author packet's `receipts/measure/datapath-*.json`). A longer group would strengthen the "most measured"
  basis.
- **S5. Decision status at 8x8/2if.** `aecp_mbx.h:33-34`, `aecp/README.md:120`, `FR_NFR.md:373` and
  `SPLIT_CONTROL_MEMORY.md:2046` call the 8x8/2if queued-notice figures "an owner question on #894".
  Citing the owner's option A of 2026-11-12 beside it would show what is already decided: 8x8/2if rows
  by every source are reported, not gated, and owed to #872.

## Checks of the round's focus items

**(1) THE TIERS** (`ctrl_loop.c:247-347`). Clean as to the stated design, but see F1 and F6.

- Tier 1's first channel (AECP) goes past its cap to `CTRL_LOOP_DRAIN_RECORDS` while the clock is at
  most `start + CTRL_LOOP_DRAIN_US` (`:293`). The others are swept only if AECP's take ended on an empty
  ring or a module not ready (`rx_left`, `:172-184`, `:298`).
- Tier 2, SRP, runs only when `rx_left == 0`. It has a zero cap with a clock, and starts each record only
  while the clock is at most `start + CTRL_LOOP_SLICE_US - CTRL_LOOP_SRP_UNIT_US` (`:316-321`).
- A build or a round in a pass given whole follows an ordinary pass that left tier 1 none
  (`tier1_done`), or follows a whole pass after `tier1_holds()` (`:258-261`). The round waits for
  `drained`, so SRP goes first.
- The slice runs from the pass's start, or after an aged step (`slice_end`). A wrap-safe `int32_t`
  difference bounds it at the pass's deadline.
- The ordinary pass adds no mailbox read. `tier1_holds()`, which reads each channel's `RX_HEAD`, runs
  only for a pass given whole after another (`:258-259`).
- The static asserts hold the slice to THE SHARE and one unit of each kind (`:199-202`).

**(2) The owed-notice queue** (`aecp.c:283-284`, `:388-400`, `:509-510`, `:715-743`, `:925`).

- (a) FIFO by `owed_head`, with the head advanced only once a walk completes. Each recipient's
  `sequence` goes up by one for each notice it is sent, and the requester is left out.
- (b) `transmit` = `respond() || notices()`. No queued notice goes out in a record's turn or in a round
  (`drains` false).
- (c) `aecp_ready` is false while the queue is full. Init refuses a depth over 255 or slots without
  storage.
- (d) `Queued.*` (`test_aecp.cpp:714-853`, `:1637`) and the behave feature pass (`behave_owed.log`).
- The fan port's mover is ended by `fan_end`'s commit before `fan_out` returns (`mbx.c:515-534`), so
  reusing `a->response` as the walk's second buffer is safe. It is used only when no notice waits
  there.

Read against the ruling's citations (IEEE 1722.1-2021 9.3.5.4 and 7.5.2; Milan v1.2 5.4.5.1 and
5.4.5.2), the build conforms. S1 records a consequence of the ruled ordering.

**(3) SRP's build split across slices** (`srp_mbx.c:1098-1138`, `:895`).

- At 1x1/1if `CTRL_LOOP_BUILD_MOST` is 2, so the build is whole and its behaviour is unchanged apart
  from tier 2's wait.
- At 8x8/2if the build stops after one MRPDU, reclaims, and resumes at `tx_resume - 1`, skipping the
  declarations it already made.
- `reset_interface` ends a build resuming on that interface. The `uint8_t` promotion makes
  `(0 - 1u) / 2u` unequal to any index, so `tx_resume == 0` is left alone.
- Records taken between two slices are SRP's own, so the later MRPDU reflects the state as received.
  That is normal under IEEE 802.1Q-2018 10.7 (an Applicant's PDU carries its current state). The
  byte-for-byte test compares builds with no record between them.
- Milan v1.2 4.3.2 is kept: the licence follows `vlan_sent`. See F7 for the prose.

**(4) The slice choice (I1/I5), reproduced** (`scripts/slice_sweep.py`, `receipts/model/slice_sweep.txt`).

- On the 50 us grid from 250 us to `CTRL_LOOP_DRAIN_US` at 1x1/1if under BUILT's orders, the argmax is
  **1,200 us, with a least relative margin of 0.26728**, the last queued notice binding.
- 1,050 us gives 0.2610 and 1,300 us gives 0.2650, as stated.
- `rows_tiers.slice_choice` agrees. At 8x8/2if every slice misses, so 1,300 us is the published
  interpretation.

**(5) The rows and the load.**

- `flip_grade.py --check --point 1x1/1if` gives RESULT: PASS, rc 0 (`receipts/model/flip_check_1x1.txt`).
- `--check` at both points is rc 1, from the 8x8/2if rows. That is measured and not gated, by the owner's
  decision.
- `load_grade.py --check` gives **0.470 at the pin and 0.457 with tsn-c-stack #32**, against 0.70, PASS
  (`receipts/runs/load_grade_py___check.log`).
- I checked the costs measured on the image under the tiers against the receipts. Each committed cost is
  the most measured plus 5 %, rounded up to 5 us, or the committed figure if that is larger. For
  example:
  - `record.aecp`: 22,256 cycles gives 235 us;
  - `event.ADP`: 10,614 cycles gives 115 us;
  - `event.TICK`: 4,113 cycles gives 45 us;
  - `base`: 14,956 cycles gives 160 us;
  - the datapath events: 29.66, 26.10 and 20.74 us give 35, 30 and 25 us.

**(6) The planted defects.**

- I re-ran every new or changed plant of the lane's tables through the repository's own drivers, each on
  a copy of the tree (`scripts/plant_subset.py`).
- **Control: 30 of 30 caught.** These are the 17 new tier plants plus 13 changed ones.
- **AECP: 22 of 22 caught.** These are the 19 owed-queue plants plus 3 changed fan-out plants.
- **SRP at two interfaces: 7 of 7 caught**, 4 new plus 3 changed.
- Each was caught by its named test's words (`receipts/runs/plants_*.log`, `receipts/plants_new.txt`).
- Three reviewer probes of branches the tables do not plant escaped. They are F3, F4 and S2.

**(7) The gate pass on `12180198`** (the author packet at `61a7204d`,
`review-evidence/894-r1/author/receipts/gates/`; the measure files cited above are in its `receipts/measure/`).

- `lane-summary.txt` names 12180198 throughout, every lane gate is rc 0, and the expected rc 1s are
  marked as such.
- The workflow table has 139 steps run and 226 not run, each with a reason.
- The one bad step, `elaborate-gates-1` gate_19 (exit 92, wall clock), has its rerun receipt
  `wf-rerun/elaborate__elaborate-gates-1__gate_19.log`: head 12180198, dirty 0, 8 of 8 PASS, rc 0.
- The three sweep suites killed by the wall clock (`milan_dp`, `milan_dp_gm_steps`,
  `milan_dp_render`) each have a rerun `.head` receipt: head 12180198, dirty 0, make rc 0, verdict rc 0.
- The 8x8/2if clean-clone harness build refuses as F1 of the round 3 ruling states: rom 123,544 B,
  58 RAMB36 against the 57.5-RAMB36 ledger. That is 664 B over, and 1,104 B more than before the tiers
  (122,440 B).
- The 1x1/1if image is 108,336 B (`head-build-L1A.txt`), the same bytes at the head.
- These are checks of the stated bytes only. 8x8/2if's ledger is not graded here, per the round 3
  ruling.

**My own runs at the exact head:**

| Command | Result |
|---|---|
| `test_ctrl_firmware.py` (host suites, no RV32 compiler on this host) | 62 suites, 1,599 tests, 0 failures, PASS |
| `run.py --self-test` | `self-test: 0 failures`, 210 plants caught |
| `rows_tiers.py --selftest` | 509 of 509 |
| `flip_grade.py --selftest` | 319 of 319 |
| `load_grade.py --selftest` | 24 of 24 |
| `behave features/aecp_owed_notices.feature` | 3 scenarios passed |
| `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `check_py_idiom.py`, `check_cpp_idiom.py` | rc 0 |
| `git diff --check 66f71326 HEAD` | rc 0 |

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #894 acceptance and rulings; #665 round 23, decision D and the 2026-11-06 ruling; `FR_NFR.md` 3.4.1; `aecp.c` queue against IEEE 1722.1-2021 9.3.5.4 and 7.5.2 and Milan v1.2 5.4.5.1 and 5.4.5.2; `srp_mbx.c` against IEEE 802.1Q-2018 10.7 and Milan v1.2 4.3.2; `rows_tiers.py`, `flip_grade.py` and `load_grade.py` outputs | R838-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |
| RTL | UNCLEAN (F1) | `ctrl_loop.c`/`.h` (tiers, slice, widths, wrap-safe clock arithmetic, static asserts); `aecp.c`/`.h` and `aecp_mbx.c`/`.h` (queue indices, 8-bit counts, buffer reuse against `mbx.c:515-586`); `srp_mbx.c`/`.h` (`tx_resume`); `ctrl_plat.c` and `ctrl_aecp_image.c`; no `hdl/` file is in the diff | R838-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |
| Robustness | UNCLEAN (F3) | the queue full, refused and lost frames, the longer notice behind the queue, the waiting and START/STOP paths, lock expiry beside the queue (`aecp.c:747-780`), interface reset during a resumed build (`srp_mbx.c:895`), no clock bound, a module not ready | R838-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |
| Tests | UNCLEAN (F1, F3, F4) | `test_port_loop.cpp` L16-L27; `test_aecp.cpp` `Queued.*`; `srp_mbx.cpp`'s resumed build; the feature and its steps; the plant tables, re-run (59 of 59 caught) and probed (3 escaped); `rows_tiers`, `flip_grade` and harness self-tests | R838-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |
| Docs | UNCLEAN (F2, F5, F6, F7) | `SPLIT_CONTROL_MEMORY.md` section 13 (THE TIERS), `MAILBOX_SPLIT.md`, `FR_NFR.md` 3.4.1, the AECP, SRP and harness READMEs, `tests/README.md`, the PR body, the REVIEW READY, and source comments under the comment rule (RS1) | R838-1 | 12180198b087d4cfdd531d0de5d3753211b35616 |

## Real limits

- **Hardware.** Physical calibration was NOT RUN and no hardware was used. Field skips are not hardware
  proof.
- **Model accuracy.** F1's figures come from a reviewer probe built on the lane's own model terms, not
  from a gated row. The required outcome asks the lane to solve the rows by its method. ACMP's miss holds
  even with the fewest passes; ADP's and MAAP's are indicative.
- **Harness.** I did not run the CPU budget harness at either point and did not rebuild the images. The
  measured margins and image bytes are the author's receipts, which I checked for head binding and
  arithmetic.
- **Gates not run here.** No RV32 compiler is on this host, so the RV32 arms did not build here. I did
  not run the em-dash check: its renderer is not installed (rc 2, "cannot judge"). The author's docs
  gates report it.
- **Banks.** I ran no full sweep, no parent, processor, gPTP or Yosys bank, and no workflow replica. The
  gate pass is the author's receipts.
- **Spec text.** I could not open the specification texts. Clause readings follow the ruling's
  citations and the repository's own references.

## Pending manager duties

- A manager source bank is not claimed at this head. The current-dev merge candidate (source base
  `66f71326`, live dev `b7d69295`) is to be built and validated at the merge turn, with its receipts
  linked on the PR.
- Hosted and act acceptance stay with the manager.
- Rulings are needed on F1 (the tier-1 rows under AECP-first) and F2 (the MRPDU bound under the tiers).
  F1 of the round 3 ruling (8x8/2if ledger) remains open there and is not graded here.
- RS1 goes to the residue checklist.
- Re-review the corrected head across every lens a fix touches.

R838-1 FINISHED
