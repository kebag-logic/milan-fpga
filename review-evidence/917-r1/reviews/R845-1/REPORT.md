[R845] NEGATIVE - exact head 3926c271aaf77420fb9093694be0ab9d511b898d

Internal cleared-context review R845-1 of PR #918 / issue #917, the AECP ingress budget. Exact head `3926c271aaf77420fb9093694be0ab9d511b898d`, tree `09b50fe085b129c81e7b033b9611a861af4fb9d4`. Delta `cec88385..3926c271` is three commits (`84d8a214`, `bb001e10`, `3926c271`) touching 17 files (+634/-108).

## Verdict in brief

The shipped RTL and host model are correct for every path examined, and the contract is untouched. I checked them by reading the code clock by clock, with the published campaigns re-run here, and with reviewer probes. A held record is never overwritten, never committed twice, never lost and never held beside a token. The free space and the wrap respect the held record. A reset forgets the held frame. A channel close commits it as documented. A filtered frame or a runt behind a held frame counts nowhere. A frame that finds a token takes the same clocks as before.

The verdict is NEGATIVE because the suite does not prove three of these properties. I planted one defect for each in a scratch copy, and each escaped all 607 checks:

- **The write-head free space.** If the free space is read from `RX_HEAD` alone, a frame behind a held one writes over the oldest unread record (F1).
- **Filtered frames behind a held one.** A frame refused by the filter behind a held one can be counted in `RATE_DROP` (F2).
- **Channel close.** The documented rule "a frame held when its channel closes is still committed" can be broken (F3).

Each one is caught by an 18-check probe extension that passes at the head on the RTL and on the host model. These gaps are test and documentation defects, not RTL defects.

## Findings

### F1 - MINOR - Tests, Robustness, Docs - `tb/verilator/mbx/suite.hpp:1547` (`check_held_not_dropped`), `tb/verilator/mbx/README.md:452`, guarding `hdl/milan/mailbox/KL_mbx_rx.sv:470` - the free space past a held record has no check that can fail
- **Authority/evidence:**
  - The RTL header (`KL_mbx_rx.sv:81-87`, "the one decision that matters": a speculative word never overwrites a record the core has not read) and MAILBOX_SPLIT "The held frame" ("the next frame's words and its free space are based on it, so they never touch the held record") make the write-head free space the safety property of this change.
  - Probe arm `probe-space-from-committed-head` (`used_w = head_r - tail_w`, the space before #917) **escapes**: 607 of 607 checks pass (`receipts/probe_arms.log`).
  - The probe check RP3 fills the AECP ring until only one record fits, holds that record, then offers one more frame. Against the same defect, RP3 shows the frame behind the held one writing over the oldest unread record. U0 reports "no receive ring word is written under the head the core sees" got=10. The frame is also counted in `RATE_DROP` instead of `RX_DROP` (`receipts/probe_tests.log`). At the head, RP3 passes.
  - The README row for `rx-tail-inside-the-held-record-frees-space` says the arm reads "the free space read from RX_HEAD alone". The arm (`mutants.py:674`) actually removes the `RX_HEAD` term (`cused_w`), so the space is read from the write head alone. The table therefore claims coverage of the very defect that escapes.
- **Impact:** a later edit that drops or rebases `wr_head_r` in the space computation would corrupt unread records with no check turning red, even though the change exists to protect exactly this.
- **Required outcome:**
  - A suite check, at least through both adapters, that holds a record in a ring with room for no second record. It must grade that the frame behind it counts in `RX_DROP`, not `RATE_DROP`, and that every unread record and the held record stay byte for byte.
  - A planted arm (space from `RX_HEAD`) caught by that check by name.
  - The README row corrected to say what its arm plants.
- **Verification:** `make -C tb/verilator/mbx mutants` with the new arm caught by its named check, the default `make` green, and the README row matching `mutants.py`.

### F2 - MINOR - Tests, Robustness - `tb/verilator/mbx/suite.hpp:1547` - no frame refused by the filter, and no runt, is offered behind a held one
- **Authority/evidence:**
  - The ruling (#665 issuecomment-6894152131 item 2) and the contract (`docs/reference/MAILBOX_CONTRACT.md:863-866`) say only a passing frame behind a held one is refused into `RATE_DROP`. The reviewer brief names "a runt or filtered frame behind a held one".
  - Probe arm `probe-refused-behind-held-counted` (drops `rule_pass_w` from `vd_rate_r`, `KL_mbx_rx.sv:598`) **escapes** 607 of 607.
  - Probe check RP1 offers a command for a foreign target and a 14-byte runt while a record is held. It catches the arm: `RATE_DROP` got=1 exp=0, ERR set. RP1 passes at the head on the RTL and on the model.
- **Impact:** a regression that counts frames not addressed to this entity as rate drops, and raises `IRQ_STATUS.ERR` for them, would ship unnoticed.
- **Required outcome:** a suite check of a filter-refused frame and a runt behind a held one (no counter, no ERR, the held record then committed whole), and an arm caught by it.
- **Verification:** the arm caught by name in `make mutants`, and the check green on both adapters and the model.

### F3 - MINOR - Tests, Robustness - `docs/design/MAILBOX_SPLIT.md:295-297`, PR #918 "Known limitations", `tb/verilator/mbx/suite.hpp:1547` - the documented close-with-a-frame-held behaviour is not graded
- **Authority/evidence:**
  - MAILBOX_SPLIT says "A frame held when its channel is closed is still committed". The PR states the same, and the brief names "channel disable with a frame held".
  - Probe arm `probe-release-gated-on-open` (`rel_w` gated on `open_i`) **escapes** 607 of 607.
  - Probe check RP2 (close the channel with a frame held, wait one refill) catches it, `RX_PASS` got=16 exp=17. RP2 passes at the head on the RTL and on the model.
- **Impact:** the stated behaviour can change silently, and RTL/model parity on it is unchecked.
- **Required outcome:** a check of a frame held across a `FILTER_EN` close, plus an arm caught by it. Alternatively, a decision to make the behaviour different, with the documentation changed to match.
- **Verification:** the arm caught by name, and the check green on both adapters and the model.

### R1 - RESIDUE - Docs - new source comments carry an issue-comment ID (owner comment rule)
- **Where:** `hdl/milan/mailbox/KL_mbx_rx.sv:39`, `sw/mailbox/mailbox.yaml:1098`, `tb/verilator/mbx/mutants.py:647`, `tb/verilator/mbx/suite.hpp:783`, `tb/verilator/mbx/suite.hpp:1541`. Each contains "#665, comment 6894152131 item 2".
- **Exact fix:** in each, write "#917; #665 ruling item 2" in place of "#917; #665, comment 6894152131 item 2" (and "#665, comment 6894152131 item 2" -> "#665 ruling item 2" where #917 is already named).
- Prose pages (MAILBOX_SPLIT, README) may keep the link.

### R2 - RESIDUE - Docs - `docs/design/MAILBOX_SPLIT.md:298-301`, "What is dropped"
- **Problem:** "every later frame of the channel finds no token and is refused, in `RATE_DROP`" overstates. A later frame the filter refuses is dropped uncounted, and one that does not fit counts in `RX_DROP` (`KL_mbx_rx.sv:597-599`, and the contract's own order).
- **Exact fix:** "every later frame of the channel that passes the filter and fits finds no token and is refused, in `RATE_DROP`".

### S1 - SUGGESTION - Conformance, Docs - #917 acceptance "50 back-to-back AECP reads": state the limit
- **Judgement:** the acceptance is **met under the one-in-flight reading**, which was published at TAKEN (#917 issuecomment-6894290176) and is the only reading consistent with the ruled mechanism.
  - With burst 16 and one held slot, 50 commands sent literally with no wait must lose 33 commands (each counted). The ruling explicitly allows that ("only a command arriving behind a held one may be dropped").
  - B0 is the acceptance as read, and B2 is the hardware finding. Both were re-run here and pass, and `rx-drop-instead-of-hold` is caught by B0 by name.
- **Suggested addition:** a stated limit in MAILBOX_SPLIT "The held frame" and in the #917 record (the owner or manager to confirm the reading). Once the burst is spent and a command is held, any second AECP frame arriving within the refill period is dropped and counted. That covers a second controller, a controller pipelining a second command, and the entity's own CONTROLLER_AVAILABLE response sharing the same bucket.

No prior public review findings exist on PR #918: its comments at review time are the two review-start notices, and it has no review or line comments. So nothing is carried forward or resolved.

## Per-lens results (artifact-specific)

### Conformance (CLEAN; S1 is optional)
- **Ruling and owner decisions (#665 issuecomment-6894152131 item 2 and -6898289590):**
  - The figures stay: `mailbox.yaml` has no non-comment line changed (`receipts/gen_mailbox_identity.txt`).
  - Hold, then commit at the next refill with that refill's token: `KL_mbx_rx.sv:598-610,742-783`.
  - Only a frame behind a held one is dropped, and it is counted (`RATE_DROP` and `IRQ_STATUS.ERR`): B1 and T0/T1 pass, re-run here.
  - Every commit spends one token (`:745`), so the committed rate and the load bound are the table's.
- **No contract change:** `gen_mailbox.py --write` leaves `KL_mbx_pkg.sv` (97a664b1), `KL_mbx.sv` (4a164486) and `mbx_contract.h` (0e441a51) with blob ids equal at base, head and after the write. Only `MAILBOX_CONTRACT.md` moves, through `mailbox_emit.py`. `--check`, `--crosscheck` and `--selftest` rc 0.
- **Counter meanings:** `MAILBOX_CONTRACT.md:738-745` (RX_HEAD, RX_TAIL, RATE_DROP, RX_PASS) still read true. A held record counts in RX_PASS when committed, and a tail inside it is "ahead of RX_HEAD".
- **Acceptance:**
  - Bench: met (S1).
  - Hardware walks: owed to the bench run, not this round.
  - No image change: by construction, because the delta's firmware files are `host/` and `test/` only and `ctrl_build.py:66` marks `HOST` "never measured". The author's hash receipts show 46 fixture images and the split 1x1/8x8 images identical.
  - Timing: met at every corner against the #818 floor in all three directives (author receipts; see RTL).
- **Clause citation:** IEEE 1722.1-2021 9.2.2.4 is cited as in the issue (see limits).

### RTL (CLEAN)
I traced `KL_mbx_rx.sv` clock by clock. The invariant is "held implies bucket empty and `wr_head_r` is `head_r` plus the held record; not held implies `wr_head_r == head_r`". It is preserved because of four facts:
- A frame is stored on a held channel only if a token exists (`:599`), and held excludes a token.
- A refill on a held channel always commits the held record and spends the refill's token (`:742-745`).
- `hold_w` and `rel_w` cannot coincide, because `hold_w` requires no refill in that clock (`:608-610`).
- The double-commit case (`commit_w` and `rel_w` together on one channel) is unreachable, because it needs a stored frame on a held channel.

Further points:
- A refill in the verdict, VRD, HDR0 or HDR1 clock commits the frame then (`tok_now_w`). B5 covers HDR0, HDR1 and the clock after, and B6 watches the invariant over every clock.
- Header and speculative addresses follow `wr_head_r` (`:512,529,535`), and the wrap is modulo the ring through `& (ring_words-1)`. B0 wraps the 512-word ring with held records and checks byte for byte.
- The FSM is unchanged, so a frame with a token takes the same clocks. V1 (6/4 clocks) passes.
- Burst 0 is refused by the contract model (`mailbox_model.py:371`), so the token arithmetic cannot underflow.
- **Evidence I produced:**
  - Six of nine reviewer probe arms were caught, with named failures (`receipts/probe_arms.log`).
  - One escape, `probe-header-at-head`, is an equivalent mutant: `head_r == wr_head_r` whenever a frame reaches HDR, by the invariant above.
  - The full campaign is 238 of 238 caught after four positive controls (`receipts/mbx_mutants_full.log`).
  - RTL lint PASS at the ratchet (`receipts/lint_rtl.log`).
- **Timing and area:** author receipts (`review-evidence/917-r1/author-r1/receipts/route/`, archive ee633e64).
  - AltSpreadLogic_high: WNS +0.203 ns, WHS +0.036 ns at every corner, 0 failing endpoints.
  - ExtraTimingOpt: +0.063/+0.036, meets. Its worst path is now the verdict (`ch_r` -> `vd_acc_r`), consistent with the held flag being read there.
  - ExtraPostPlacementOpt: +0.202/+0.016, meets the #818 floor (0 ns WHS) but not a +0.030 hold floor.
  - Area: LUT +74 to +181, FF +75/+76, BRAM 78.5 tiles and DSP 9 unchanged, `KL_mbx_rx` +124 to +133 LUT and +77 FF. That matches 5 x 17 new state bits plus their multiplexers.
  - Not reproduced here (see limits).

### Robustness (UNCLEAN: F1, F2, F3)
The RTL and the model behave correctly under every probe I ran (`receipts/probe_tests.log`: head 625/625 with 18 added checks; `receipts/probe_model.log`: model 545 = 527 + 18, 0 failures):
- malformed and truncated input (RP1 runt);
- filtered input behind a held frame (RP1);
- ring free space and full ring with a held frame (RP3, and B4 tail inside the held record);
- reset during hold (B3);
- feature-disabled channel (RP2 close);
- refill at every header clock (B5);
- repeated drops counted once and saturating as before (B1).

The lens is unclean because the full-ring, filtered/runt and close paths have no in-tree executable guard. The evidence is the reviewer's out-of-tree probe only (F1-F3).

### Tests (UNCLEAN: F1, F2, F3)
Re-run here at the exact head with the pinned simulator (Verilator 5.050 rev v5.050):
- `make run-wb run-axil run-cosim run-if2` gives 607 / 652 / 32 / 614 / 659 / 532 checks, 0 failures (`receipts/mbx_make.log`). That equals the published counts.
- Full `mutants.py` gives 238 of 238. The seven new arms are each caught by the check they name, six by a B-check and one by T0 (`receipts/mbx_mutants_full.log` lines 236-242).
- `test_ctrl_firmware.py` PASS, with RV32 arms built (`receipts/ctrl_firmware.log`).
- `model-rate-unlimited` and `model-drop-instead-of-hold` are both caught by their named groups (`receipts/model_mutants_two.log`; 28 failing checks for the second, against the author's 27, both caught).

The new checks can fail for their claimed defects: `rx-drop-instead-of-hold` fails B0 by name, which is the acceptance's check.

The host-model change (`mbx_model.c/.h`) and the three `test_acmp_mbx.cpp` loops are **needed for parity**:
- The shared suite (T0/T1/Q10/HeldNotDropped) runs on the model and the co-simulation compares RTL and model.
- The pre-change model is exactly `model-drop-instead-of-hold`, which fails 28 checks.
- The loops' expectations are unchanged, and they now count committed records from RX_PASS.

The gaps are F1-F3.

### Docs (UNCLEAN: F1's README mutant row; residue R1, R2)
- **MAILBOX_SPLIT:** "The held frame" (`:273-317`) and the filter section are accurate apart from R2. The verification table's counts (607/614, 652/659, model 532 of 614, thirteen quick arms) match my runs.
- **Contract and comments:** `MAILBOX_CONTRACT.md:863-866` and the YAML comment are consistent with the RTL.
- **Bench docs:** the README B0-B6 and T0/T1 rows match `suite.hpp`. The README mutant row at `:452` is wrong (F1).
- **Docs gate:** `docs_check` reports 0 findings (`receipts/docs_check.log`).
- **Comment rule:** five new issue-comment IDs in source comments (R1).
- **Evidence for a cold reviewer:** the PR and issue carry enough evidence, and the author's receipts are indexed.

## Specific questions in the brief

1. **Hold, commit, drop.** Verified as above. There is no overwrite, double commit, loss, or hold beside a token, and free space, wrap, reset, close, runt and filtered frames are all correct at the head. The test gaps are F1-F3.
2. **No contract change.** Verified: byte-identical generated outputs, and no register, field, rate figure or version moved.
3. **Tests and mutants.** B0, B1 and B2 pass on both adapters and the model. 238 of 238 are caught, and `rx-drop-instead-of-hold` is caught by B0. I did not re-run the 699-arm firmware campaign; the two model arms this delta adds are caught here.
4. **Host model.** Needed for parity. It is compiled into no image (`ctrl_build.py:66`, and the delta touches no image source). The image hashes are the author's receipts.
5. **"50 back-to-back".** Met under the published one-in-flight reading, with a limit worth stating (S1).
6. **Timing and area.** Author receipts support the claim. All three directives meet the #818 floor, and the best is AltSpreadLogic_high at +0.203/+0.036.
7. **CPU budget harness.** 1x1 base/head byte-identity supports "no 1x1 scenario sends into an empty bucket". The harness reads no RATE_DROP or RX_PASS, so the 8x8 premise is inferred from the base grader's pass, not observed. I judge "8x8 not run" acceptable for this lane because #665 ruling item 1 measures 8x8/1if once at #914's composed head. It is carried as a manager duty.
8. **Gate pass.** Author receipts: 139 steps rc 0, every skip with a reason, sweep 65/65 at `84d8a214` and shard 1/4 17/17 at the head. The `84d8a214..3926c271` delta touches only docs, `ctrl_mutants.py`, the README, `mutants.py` and `suite.hpp`. Re-run here: the mbx bench, all mutants, the firmware gate, lint, the docs check and the generator gates.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #917 body and acceptance; #665 issuecomment-6894152131 item 2, -6898289590; `mailbox.yaml` (no non-comment change); `MAILBOX_CONTRACT.md:738-745,860-866`; `KL_mbx_rx.sv:566-611,728-790`; `receipts/gen_mailbox_identity.txt`; B0/B1/B2 results | R845-1 | 3926c271aaf77420fb9093694be0ab9d511b898d |
| RTL | CLEAN | `KL_mbx_rx.sv:38-55,230-238,457-474,505-556,566-611,727-790`; `tb_mbx_top.sv` probe; `receipts/probe_arms.log`, `mbx_mutants_full.log`, `lint_rtl.log`; author route receipts (ee633e64) | R845-1 | 3926c271aaf77420fb9093694be0ab9d511b898d |
| Robustness | UNCLEAN (F1, F2, F3) | `KL_mbx_rx.sv` space/verdict/buckets; `mbx_model.c:262-275,515-571`; `receipts/probe_tests.log`, `probe_model.log` | R845-1 | 3926c271aaf77420fb9093694be0ab9d511b898d |
| Tests | UNCLEAN (F1, F2, F3) | `suite.hpp:779-853,1497-1680,2420-2470`; `bench.hpp`; `mutants.py:640-690`; `ctrl_mutants.py:305-312`; `test_acmp_mbx.cpp:1406-1580`; `receipts/mbx_make.log`, `mbx_mutants_full.log`, `ctrl_firmware.log`, `model_mutants_two.log`, `probe_*.log` | R845-1 | 3926c271aaf77420fb9093694be0ab9d511b898d |
| Docs | UNCLEAN (F1 README row; R1, R2 residue) | `MAILBOX_SPLIT.md:31,192-317,1754-1774`; `MAILBOX_CONTRACT.md:860-866`; `tb/verilator/mbx/README.md:82-95,159-182,243,433-455`; Makefile header; PR #918 body; `receipts/docs_check.log` | R845-1 | 3926c271aaf77420fb9093694be0ab9d511b898d |

## Real limits of this round
- **Not reproduced here:**
  - Vivado timing and area: author receipts only.
  - The 46 fixture and split image hashes: structural argument plus author receipts, not rebuilt.
  - The CPU budget harness.
  - The full Verilator sweep and the 699-arm firmware mutant campaign: only the two model arms this delta adds were run.
  - The Yosys, rtl-fast and elaborate workflow steps.
- **Clause text:** I did not consult the IEEE 1722.1-2021 text. Clause 9.2.2.4 is taken as cited by the issue and the ruling.
- **Hardware:** none. The three descriptor walks are owed to the bench run, and physical calibration was NOT RUN.
- **Source bank:** no manager source bank ran at this head, and none is claimed.
- **Hosted checks at review time:** 16 success, 1 skipped, the rest queued or in progress, none failed (`receipts/hosted_checks_3926c271.txt`). The manager owns hosted and act acceptance.

## Pending manager duties
- Fix rounds for F1-F3 and the residue checklist R1 and R2. After the fix commit, re-cover Tests, Robustness and Docs at the new head. RTL and Conformance stay covered only if no RTL or contract file changes.
- Merge candidate on live dev (`6b66f66d...`; dev-soft-core now `659d7687` with #902): rebuild and validate the composed candidate at the merge turn, including #902's load gate against the held-frame rule.
- PR #918 says `Closes #917`, but the hardware acceptance (three walks with none unanswered) is still owed. Keep #917 open, or reopen it, until the bench run records the walks.
- Confirm at #914's composed head that the 8x8/1if budget rows are unaffected by the hold.
- Record which directive ships. The integrated default, ExtraPostPlacementOpt, has WHS +0.016 ns: it meets the #818 floor but not a +0.030 hold floor.
- Record the owner's acceptance of the one-in-flight reading of "50 back-to-back" (S1).

R845-1 FINISHED
