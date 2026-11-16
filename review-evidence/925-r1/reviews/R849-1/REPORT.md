[R849] NEGATIVE - exact head 09a948d46413ef3b3ab0fa11bf97c06323f9051f

Round R849-1, internal cleared-context review of PR #932 (issue #925), tree `a7ff40db6afec61b93243ede79af62dd9efd8cb7`.
The lane's change is three commits on `16ba667d` and one `--no-ff` merge of dev-soft-core `70f4056f`. That merge
changes no file: `70f4056f^{tree}` = `16ba667d^{tree}` = `ed63495c`, and `09a948d4^1^{tree}` = `a7ff40db`.

**Verdict.** The fix does what #925 asks. My own runs at the exact head show it:

- An Advertise New over a registered Failed is declared Ready within one JoinTime.
- The latest kind decides in every order I drove, at both interface counts.
- I found no stale kind, no lost Ready, no declaration flapping inside one MRPDU, and no state where ACMP and the
  Listener declaration disagree.
- The gates I re-ran pass.

The verdict is NEGATIVE on two MINOR findings:

- **F1** (Conformance, Docs): the clause and reference record of the new rule is wrong. It does not publish that
  the rule departs from the IEEE 802.1Q-2018 35.2.6 NOTE.
- **F2** (Tests): the rule "the latest decides" is tested only for the first conflict. A planted restriction
  escapes every test at both interface counts.

There is also one SUGGESTION (F3) and one RESIDUE (F4).

## Findings

### F1 - MINOR - Conformance, Docs - the rule's clause citations and its processor comparison are inaccurate, and its departure from the 35.2.6 NOTE is not published

- **Where:**
  - `sw/firmware/ctrl/srp/srp_mbx.c:193-196`
  - `sw/firmware/ctrl/srp/README.md:246-250` and `:482-484`
  - `sw/firmware/ctrl/test/srp_kind_mutants.py:5-7`
  - `sw/firmware/ctrl/test/srp_mbx.cpp:1804-1806` and `:1911`
  - `sw/firmware/ctrl/test/srp_feedback.hpp:113`
  - the PR body's "The rule" paragraph
- **Authority and evidence.** I read IEEE 802.1Q-2018 directly.
  - (a) "A talker declares one of the two for a stream (IEEE 802.1Q-2018 35.2.4)". 35.2.4 is MSRP Attribute
    Propagation, a Bridge MAP clause (p. 1576), and says nothing of the kind. The one-of-two text and the direct
    Advertise-to-Failed transition are 35.1.2.1 (p. 1557). "At most one Talker Declaration" is 35.2.6's NOTE.
  - (b) "A registration of the other kind replaces the one held (35.2.6)". 35.2.6 (p. 1581) replaces only on a
    received JoinIn or JoinMt. Its NOTE then states: "In the unlikely situation where a Talker Advertise and a Talker
    Failed are received for the same Stream on the same port, the Talker Failed declaration takes precedence."
    - That is exactly the state the new `listener_kind` resolves the other way (latest decides, so Advertise can
      win).
    - The README line this PR removes ("conflicting New registrations retain Failed precedence") was the reading
      consistent with that NOTE.
    - The NOTE is informative. Milan v1.2 5.3.8.5 is normative and supports the new behaviour: "If a Talker
      Advertise attribute with matching SRP parameters is being received, the PAAD-AE shall be declaring an MSRP
      Listener Ready attribute". So do the #665 finding-18 decision and the release processor.
    - None of that is cited, and the conflict is not published on #925 or the PR. AGENTS.md section 8: never hide
      a specification conflict in code.
  - (c) `README.md:482-484` says "of conflicting New registrations the latest decides ... as the processor's
    in-place type swap takes every registering event". That reads as parity with the reference implementation, but
    the two differ once something leaves.
    - The processor (`protocol-processor/hdl/srp/KL_srp_listener_fsm.sv:472-491`, `:515-520`) holds one registrar
      per sink. A Lv of either Talker type on IN unregisters it.
    - The split falls back to the older kind when the latest leaves, and treats the older kind's leave as no
      change (`SrpTalkerKinds.LeaveOfEitherKindLeavesTheOtherDeciding`, probe P6).
    - That difference is not in the README's difference table.
- **Impact.** A cold reader is told the standard mandates this precedence and that the release behaves the same. In
  fact the standard's only statement on coexistence says the opposite, and the leave behaviour differs from the
  reference. The behaviour itself is not judged wrong here, because #925's scope decides it. What is wrong is the
  conformance record.
- **Required outcome.**
  - Cite 35.1.2.1 for the talker's one-of-two.
  - State that 35.2.6 replaces only on JoinIn/JoinMt, and that its NOTE gives Failed precedence when both are
    received.
  - Publish the departure and its authority on #925 or the PR, for example the #925 scope decision, Milan v1.2
    5.3.8.5 and the release processor.
  - Record the leave difference from the processor in `srp/README.md`'s comparison.
  - The behaviour is unchanged by all of this. This is not wording-only: it is a clause and conformance claim.
- **Verification.** Reread the touched comments and README against 802.1Q-2018 pp. 1557, 1576 and 1581 and Milan v1.2
  5.3.8.5. Then check that the decision is visible on #925.

### F2 - MINOR - Tests - "the latest registered decides" is tested only from a one-kind state; a restriction of the rule escapes every test

- **Where:** `sw/firmware/ctrl/test/srp_mbx.cpp:1807-1958` (`SrpTalkerKinds`), `sw/firmware/ctrl/test/srp_kind_mutants.py`
- **Evidence.** The reviewer plant `r849-renew-not-recorded` changes `talker_changed` so that it records the latest
  kind only when the binding did not already hold that kind. Under the plant, a talker that flaps Failed, then
  Advertise New, then Failed New keeps the Listener at Ready while the talker's latest declaration is Talker Failed.
  That is finding 18 in reverse.
  - The plant is **ESCAPED** at both interface counts: `receipts/runs/mut1.log` and `receipts/runs/mut2.log`. Every
    `SrpTalkerKinds` and `SrpFeedback` test passes with it in place.
  - The head is correct. Probe `R849Probe.P3EachNewInTurnDecides` passes at both interface counts
    (`receipts/runs/probes1.log`, `probes2.log`) and catches the plant (`receipts/runs/probes2-renew.log`: "P3 Failed
    New again").
- **Impact.** The README and the code comment state the rule in general terms: "while both are registered the one
  registered latest decides". The tests only check the first conflict, so a regression to "the first conflicting New
  decides, later ones do not" would merge green.
- **Required outcome.**
  - A self-checking test where a kind already registered beside the other kind is registered New again, and the
    declaration follows it.
  - A planted defect, caught by name at both interface counts.
- **Verification.** The new plant is caught at 1 and 2 interfaces in the SRP campaign. The head still passes.

### F3 - SUGGESTION - Tests - an in-place rebind that keeps the StreamID is not tested for carrying the latest

- **Where:** `sw/firmware/ctrl/srp/srp_mbx.c:621-625`
- **Evidence.**
  - Plant `r849-bind-copy-skipped-for-self` stops the bind from copying the latest kind from the binding it
    replaces. It is ESCAPED at both interface counts (`mut1.log`, `mut2.log`).
  - The case is a sink rebound to the same StreamID with another destination, then back, while both kinds stay
    registered.
  - The head is correct: probe `P10RebindInPlaceKeepsLatest` passes, and catches the plant (`probes2-selfcopy.log`).
- **Why this is a suggestion:** the window is narrow. Registrations do not match the other destination, so the latest
  matters only on the return.
- **Optional change:** extend `ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream` to an in-place replacement.

### F4 - RESIDUE - Docs - a report-local finding label in a source comment

- **Where:** `sw/firmware/ctrl/test/srp_mbx.cpp:1870`, which reads `// Finding 18: the talker replaces ...`
- **Authority:** the owner's comment rule of 2026-10-15. "Finding 18" is the numbering inside #665 issuecomment
  6904803181's replica report, not an issue or requirement ID. This is a new instance in the reviewed delta.
- **Exact fix:** replace `// Finding 18: the talker` with `// #925: the talker`.
- **Status:** wording only. It does not make the verdict negative.

## The five lenses at this head

| Lens | Result | Examined artifacts (at `09a948d4`) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | see "Conformance" below | R849-1 | `09a948d46413ef3b3ab0fa11bf97c06323f9051f` |
| RTL | CLEAN | see "RTL" below | R849-1 | `09a948d46413ef3b3ab0fa11bf97c06323f9051f` |
| Robustness | CLEAN | see "Robustness" below | R849-1 | `09a948d46413ef3b3ab0fa11bf97c06323f9051f` |
| Tests | UNCLEAN (F2; F3 is a suggestion) | see "Tests" below | R849-1 | `09a948d46413ef3b3ab0fa11bf97c06323f9051f` |
| Docs | UNCLEAN (F1; F4 is residue) | see "Docs" below | R849-1 | `09a948d46413ef3b3ab0fa11bf97c06323f9051f` |

### Conformance

Examined: `srp_mbx.c:192-221`, `:357-369`, `:845-912`, `:586-653`, read against IEEE 802.1Q-2018 35.1.2.1, 35.2.3.1,
35.2.4, 35.2.6 and Milan v1.2 5.3.8.5, 5.3.8.8 and 5.5.3, and lwSRP's `mrp_mad.c:990-1066` and `msrp.c:391-397`.

The behaviour meets #925's scope:

- An Advertise New over a registered Failed is Ready within one JoinTime: `AnAdvertiseNewReplacesARegisteredFailedWithinAJoinTime`.
- ACMP sees the kind change: `AdvertiseNewOverARegisteredFailedUpdatesTheSettledWireView`.

The clause record is wrong (F1). The bench acceptance (Ready within 1 s) is not desk-provable.

### RTL

Firmware only. Examined:

- `git diff --stat 16ba667d..09a948d4 -- hdl protocol-processor gptp-processor tb syn third_party configs sw/firmware/ctrl/loop sw/firmware/ctrl/mbx srp_bounds.h` is empty.
- The gitlinks are identical (`receipts/runs/clone_integrity.txt`).
- The author's export comparison (`author-r1/receipts/images/base-vs-head-route-export.txt`): netlist and integrated
  script identical, ROM contents only.
- `srp_mbx.h:23-41`: one `uint8_t` field. The mailbox contract is unchanged.
- `listener_kind` was tested over all 16 `(registered_kinds, latest_kind)` pairs, compiled from the head's text. It
  returns only 0, 1 or 2 and matches the rule for every reachable pair (`receipts/runs/listener_kind_table.log`).

### Robustness

Reviewer probes at 1 and 2 interfaces (`receipts/runs/probes1.log`, `probes2.log`, 18/18 pass at each):

- P1 and P2: a repeated JoinIn after the New. No Lv and no other subtype on the wire.
- P4: a JoinIn that reverts to the other kind, with no indication.
- P5: JoinMt.
- P6: the older kind's rapid leave is quiet.
- P7: `{Advertise New, Failed JoinIn}` in one MRPDU. Failed decides and no Ready reaches the wire.
- P8: two bindings bound before the registrations.
- P9: the latest leaves, then returns.
- P11: a stream VID that is not the Domain's. Ready at +170 ms, no withdrawal, on both the New and the JoinIn paths.
- P12: a link reset in the middle of a conflict, then a single kind. No stale latest.
- The fallback when no latest is known: Failed (author's test and the truth table).

No robustness defect was found.

### Tests

Re-runs at this head:

- `srp_mbx.cpp` and `srp_feedback.hpp`. SRP shard 3/4 at this head: 441 caught, 0 escaped. That includes the 10
  `feedback-latest-` plants at both interface counts and `failed-listener-ready` (`receipts/runs/fw3.log`).
- A targeted campaign: author plants 11 of 11 caught, reviewer plants 3 of 5 caught, at each interface count
  (`mut1.log`, `mut2.log`).
- Under the old rule (plant `feedback-latest-failed-first`), 5 of the 6 `SrpTalkerKinds` tests and 7 of the 11
  probes fail (`probes2-oldrule.log`).

Gaps: F2 and F3.

### Docs

Examined:

- `srp/README.md:243-259` and `:476-485`
- `docs/design/SPLIT_CONTROL_MEMORY.md:138` and `:147`
- `sw/litex/ctrl_memory.py:263-277` and `ctrl_memory_ledger.py:35`, against the author's `plat_ledger` receipt
  (`author-r1/receipts/ledger/ledger-wt2.log`: 17,536, 19,072, 18,240 and 20,416 B; 8x8/2if at 60.5 RAMB36)
- the PR body and the REVIEW READY comment

`docs_check.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `gen_toc.py --check` and `gen_toc.py --verify-anchors`
all return rc 0 at this head (`receipts/runs/docs_*.log`, `docs_gates.rc`). The defects are F1 and F4.

## Checks against the brief

1. **`srp_mbx.c` rule, every order.**
   - Confirmed from lwSRP's source that a registered Talker of the other type is replaced only for a JoinIn or JoinMt
     (`mrp_mad.c:1030-1052`, `msrp_attr_replaces`). A New registers beside it.
   - Orders driven: both replacements, either leave in both orders, both orders inside one MRPDU, a New plus a
     replacing JoinIn in one MRPDU, a binding made later, a rebind in place, a link reset, and a non-Domain VID.
     These are the author's tests plus probes P1-P12.
   - No stale kind after a leave, no lost Ready, no declaration flap inside one MRPDU (the filter's intermediate
     `desired` only feeds `capture`, never a declaration), and no ACMP or declaration disagreement.
   - One record defect (F1) and one test gap (F2).
2. **lwSRP, tsn-c-stack, SRP timers, bounds, mailbox contract and RTL unchanged.** Verified by diff and gitlinks.
   `CTRL_LOOP_JOIN_CS` and `srp_bounds.h` are untouched.
3. **Tests.**
   - 8 new tests: 6 in `SrpTalkerKinds` and 2 in `SrpFeedback`.
   - 10 plants, each caught by name at both interface counts. The first plant is the old rule.
   - `srp_mbx.c` coverage: 741/741 lines and 671 of 671 counted branches. My `fw_coverage.py --check` at this head
     prints `741/741 671/674 ... branches 100.00 %` and PASS (`receipts/runs/cov.log`), matching `coverage.ratchet`.
   - Ready within a JoinTime is asserted with a wire timestamp at or below start + 190 ms.
4. **CPU budget, ROM and ledger.** From the author's receipts only; I re-ran none of them.
   - 1x1/1if: rc 0, 96 groups, 0 refusals, 0 of 129,813 passes over the share, 7 budget misses (all `backlog-owed`).
   - 8x8/1if: rc 1 on 84 STATED lines. All are polls base, ACMP item or ACMP declined offer, none of them SRP's,
     which matches #914's per-shape statements.
   - Flip grade at 1x1/1if: PASS (`last` 136.65 of 140, `txL` 48.58 of 49). Load: 0.517 / 0.514 against 0.70.
   - ROM: +88 B at 1x1 and +32 B at 8x8 (bank3 722 words against 700). The 8x8/2if `ctrl_plat` record is 20,416 B.
   - Release image byte-identical (`release-image/COMPARE.txt`).
   - Merge-head relink: identical ELF digests (`author-r2/receipts/identity`).
5. **Gates on a clean clone.** Executed here:
   - Firmware suites, shard 0/4 with `--require-rv32` (pinned RV32 SDK verified by `ci_rv32_sdk.py`): 79 arms, rc 0.
   - SRP mutant shard 3/4: rc 0, 441 caught.
   - `fw_coverage --check`: rc 0.
   - The docs gates above.

   I did not run rtl-fast, elaborate, the control and AECP mutant shards (1/4, 2/4), or the 65-suite Verilator
   sweep. For those I read the author's receipts: shards 0, 2 and 3 all passed; shard 1 passed 14 of 17, and the 3
   re-runs passed on an idle host. They are author evidence, not mine.
6. **Timing.** Both shapes' routes are recorded as misses at the base, owed to #927, per #925 issuecomment-6908876793.
   Spot-checked signoff figures match the table. This is not a finding.

KNOWN, not findings: #929; the two `srp_mbx.cpp` startup tests failing at the 8x8 entity at the base; the cut runs of
2026-11-16.

## Real limits

- No manager source bank runs at this head, and none is claimed. Source-head execution here is the reviewer's own runs
  listed above, on this clone with outputs outside the tree. The rest is the author's published receipts.
- The current-dev merge candidate (live dev `6b66f66d`) was not built. That is the manager's duty at the merge turn.
- Physical calibration and the bench acceptance were NOT RUN. Desk results are not hardware proof.
- Hosted exact-head contexts were queued or in progress when I looked. `full-ci-gate` was success and
  `Physical gPTP` was skipped. That is not an executed verdict, and hosted and act acceptance are the manager's.
- `probes2-oldrule`, `probes2-renew` and `probes2-selfcopy` ran with the probe file before P12 was added (17 tests).
- The firmware harness's shard self-check created an untracked `dispatch-build/` in the clone, because it uses a path
  relative to the working directory. This behaviour predates this change. I removed it and re-verified the clone:
  index tree = `a7ff40db`, 1,627 tracked blobs byte-identical, no mode differences, no hidden-index flags, six
  gitlinks at the pinned revisions, and submodule worktrees clean (`receipts/runs/clone_integrity.txt`).
- One other reviewer's report on this PR, posted after this round started, was not read before this verdict and
  ledger were written. No earlier review round with findings exists on this PR, so no prior finding needed to be
  resolved or retained.

## Pending manager duties

- Carry F4 to the residue checklist.
- Validate the current-dev merge candidate with the builder and native banks, and publish its receipts.
- Hosted and act acceptance at the exact head.
- Bench acceptance: Listener Ready within 1 s of the Talker Advertise.
- Decide whether F1's conflict needs an owner ruling on #925.

R849-1 FINISHED
