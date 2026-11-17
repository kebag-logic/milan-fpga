[R849] NEGATIVE - exact head 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd

# R849-2: internal review of issue #925 / PR #932, round 3 (delta 09a948d4..5f625090)

Cleared-context internal review. Exact head `5f625090bbd09a67f01080aeaa1f05e9d9a79cdd`, tree
`84cd6032a8efac1563ae09d11a40ba206674373c`. Source base `16ba667d` and the round-2 head `09a948d4` are both
ancestors. Six one-line commits, 12 files, +467/-100. No gitlink, RTL, mailbox-contract or lwSRP change.

All five lenses were applied. The firmware change is correct at this head. Both R850-1 MAJOR findings and all
four R849-1 findings are resolved. The verdict is NEGATIVE for one reason: the authoritative memory design document
still states the platform entry's old cap and its old planted-ledger figures after this delta raised that entry
(F1, MINOR, Docs). Every other lens is clean. There are also two suggestions and one residue item.

Order of reading: AGENTS.md and CONTRIBUTING.md; docs/README; issue #925 (body and acceptance); the ruling
[#925 issuecomment-6930043105](https://github.com/kebag-logic/milan-fpga/issues/925#issuecomment-6930043105); the
owner decision [#665 issuecomment-6892332745](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6892332745);
the delta and its history; the author packet `review-evidence/925-r1/author-r3` at archive `22239840`; REVIEW READY
#925 issuecomment-6939437010. I read the prior review findings (R850-1 issuecomment-6929485868 and R849-1
issuecomment-6930031527) only after my own pass over the diff, and I read no other reviewer's report.

## Findings

### F1 - MINOR - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:145` and `:173-174` still state the platform entry's old cap and old planted ledgers

- **Where:**
  - `docs/design/SPLIT_CONTROL_MEMORY.md:145`: "The caps are 59.0 for the size fixture's point and 60.5 for the
    platform's, which their entries now hold; each image is refused half a tile past its entry, at 59.5 and 61.0."
  - `:173`: the platform's planted ledger "plans 61.0".
  - `:174`: the fixture's planted ledger "plans the platform's 60.5".
- **Authority and evidence:**
  - This delta raises `platform-8x8-two-interfaces` to 61.0, refused at 61.5 (`sw/litex/ctrl_memory.py:267`,
    `sw/litex/ctrl_memory_ledger.py` `OWN`, `HELD` and `REFUSED` "its own image at 61.5 RAMB36, half a tile past its
    61.0"). It also re-plants the ledgers as "the platform's entry at 61.5 RAMB36" and "the size fixture's entry
    at the platform's 61.0" (`ctrl_memory_ledger.py` `planted()`).
  - The same section's new line `:148` and the table row `:138` say 61.0. So `:145` now contradicts them in the
    present tense.
  - `:173-174` describe the test's planted ledgers with figures the test no longer uses.
  - The owner decision of 2026-11-15 also says the caps are no longer stop conditions for the flip lanes.
  - The three lines predate the delta (`git blame`: `8238156d`), but the delta changed what they describe.
  - AGENTS.md section 6, Docs lens: "Changed contracts are reflected in authoritative docs."
- **Why MINOR, not RESIDUE:** the defect is a wrong figure for a ledger contract and for a test's plants in an
  authoritative design document. That is more than wording, and the rule says that when unsure, the item is MINOR.
- **Impact:** a cold reader of section 3 is told the platform image is refused at 61.0 and that the plants sit at
  61.0 and 60.5. Neither is true at this head, and the image now plans 61.0.
- **Required outcome:** `:145` states the entries as they now stand. That means the platform's 61.0, refused at
  61.5, by the owner's decision of 2026-11-15, or `:145` is recast as history before `:148`. `:173-174` name the
  planted ledgers the test holds: 61.5 for the platform's entry and the platform's 61.0 for the fixture's.
- **Verification:** reread the three lines against `ctrl_memory.LEDGERED`, `ctrl_memory_ledger.planted()` and
  `REFUSED` at the fixing head. `python3 -B sw/litex/test_ctrl_memory.py` stays rc 0.

### S1 - SUGGESTION - Tests - two hold details are pinned only by the reference walk, or not at all

- **Where:**
  - `sw/firmware/ctrl/srp/srp_mbx.c:913-920`: `stream_kinds` counted "whatever their destination and VID".
  - `:670`: a binding that takes a held entry claims `stream_kinds = 3u`.
- **Evidence (`receipts/r849-2/`):**
  - Plant `r849-2-stream-kinds-own-destination` counts `stream_kinds` only for the binding's own destination and
    VID. Every `SrpTalkerKinds` and `SrpFeedback` test passes with it in place, at both interface counts. Only the
    reference-walk equivalence check `Srp.OwnDeclarationsThatRewriteARegisteredValueAreCopied` catches it
    (`whole-dest-if1.log`, `whole-dest-if2.log`).
  - My behavioural probe `R8492FinalUnbindingOfAnotherDestinationKeepsTheLatest` shows the plant's effect. The
    StreamID's only binding is moved in place to another destination and then unbound. The StreamID is then not
    held, and the next binding asks Failed where the latest is Advertise. That is R850-1 F2's symptom for that
    variant. The head passes the probe, and the plant fails it at both counts (`probe-head-if*.log`,
    `probe-r849-2-stream-kinds-own-destination-if*.log`).
  - Plant `r849-2-take-without-kinds` drops `replacement.stream_kinds = 3u`, and it survives every selected test
    (`explore-if1.log`). The next walk recomputes the value, so the only exposure is an unbinding made in the same
    pass as the binding that took the hold.
- **Why a suggestion:** the head is correct, and the first plant is caught by the suite, so it cannot merge green.
- **Optional change:** add the probe above, and one bind-then-unbind with no walk between, as behavioural tests,
  each with a planted defect.

### S2 - SUGGESTION - RTL, Robustness - the held table's scan is new work on every Talker leave indication and binding, and no budget group stages it

- **Where:**
  - `sw/firmware/ctrl/srp/srp_mbx.c:246`: `held_stream` on every leave indication.
  - `:667`: `held_stream` on every binding of an identity.
  - `srp_mbx.h:124`: up to `SRP_HELD_STREAMS` entries, 16, 32, 40 and 81 by point. I recomputed these from the
    entity shapes, 2/2 and 9/9 sources and sinks (`receipts/r849-2/entity-shapes.txt`).
- **Evidence:**
  - Each iteration calls the out-of-line `same()` over 8 bytes. From reading the source, I estimate 50 to 100
    cycles an entry. That is about 20 to 40 us a leave with 40 entries at 100 MHz, and twice that with 81. This is
    an estimate, not a measurement.
  - The budget summaries' rows hold as measured. Their own note says costs not directly staged read 0, and no group
    stages a populated held table (`author-r3/receipts/budget/*-summary.md`).
  - A full table needs many StreamIDs unbound while both kinds are registered, inside one LeaveAll period. That is
    far from ordinary operation, but nothing states the worst case.
- **Optional change:** state the worst case beside the SRP record-apply and tick costs, or stage a populated table.

### R1 - RESIDUE - Docs - a lane name added to a source comment

- **Where:** `sw/litex/ctrl_memory.py:250`, a `#:` comment added by `44265574`: "... as debt owed to S14)".
- **Authority:** the owner's comment rule of 2026-10-15 says source comments never show lane names. Existing
  instances are tracked by #746.
- **Exact fix:** "as debt owed to S14" becomes "as debt owed to the hybrid XIP work (#665 decision D3)". The
  string literal at `:280` is data, not a comment, and needs no change under the rule.
- **Status:** wording only. It does not make the verdict negative.

## Prior findings at this head

| Prior finding | Status at 5f625090 | Evidence |
|---|---|---|
| R850-1 F1 MAJOR: a trailing message loses the new kind's transmission work | **Resolved** | `srp_mbx.c:398-402`: `interested_msrp` calls `hold(i)` when its copy moves `desired`. `hold` (`:122-128`) calls no lwSRP function. It sets `tx_due` now, or leaves it to the join timer's end (`:106-107`). THE TRANSMIT still declares from the final state. R850-1's `run_reproduce.py`, with its no-trailing controls, plus `run_probes.py` (200 phase/direction cases, 216 ordered-event traces) and `run_rebind.py` are rc 0 at 1 and 2 interfaces (`receipts/r850-1/`). Regressions at an idle join timer inspect the wire Listener and ACMP GET_RX_STATE (`srp_mbx.cpp:2088`, `srp_feedback.hpp:177`). New and Lv in one MRPDU declare only the final state, with no withdrawal on the wire. The author's two filter plants are caught at both counts (`receipts/r849-2/author-if*.log`). |
| R850-1 F2 MAJOR: final unbind and rebind lose the latest-kind order | **Resolved** | `srp_mbx.c:666-690` (held at the last binding's end, taken by the next binding), `:244-249` (released by either kind's end), `:1102-1108` (released by its interface's reset). The fallback test and plant are replaced by `AFinalUnbindingKeepsTheLatestWhileBothStayRegistered`, `AHeldStreamEndsWithEitherRegistrationOrAReset` and `AStreamIsHeldForItsOwnInterface`. These cover leave, LeaveAll expiry, reset, another identity in the sink's place, and another interface. The full-table guard is tested white-box. The bound holds: lwSRP's `struct mrp_attr_inst` (`third_party/lwSRP/src/core/mrp_mad.c:62-79`, two 48-byte value arrays) is over the 64-byte small class. `run_rebind.py` is rc 0 at both counts. |
| R849-1 F1 MINOR: clause citations and the 35.2.6 NOTE departure | **Resolved** | `srp_mbx.c:194-202`, `srp/README.md:246-275`, `srp_kind_mutants.py:5-8`, `srp_mbx.cpp` section header, `srp_feedback.hpp:138-140` and the PR body's "The rule and its clauses" cite 35.1.2.1, 35.2.6 replacing only on JoinIn/JoinMt, the informative NOTE, Milan v1.2 5.3.8.5 and the ruling. No `35.2.4` citation remains in the touched files. README D3 (`:496`) records the processor's unregister on a leave of either type. I checked that against `protocol-processor/hdl/srp/KL_srp_listener_fsm.sv:472-520`. |
| R849-1 F2 MINOR: latest-decides untested from a two-kind state | **Resolved** | `EachNewInTurnDecidesWhileBothAreRegistered` and the extended `AFailedNewReplacesARegisteredAdvertiseWithinAJoinTime`. Plant `r849-renew-not-recorded` is caught by name at 1 and 2 interfaces (`receipts/r849-2/reviewer-if*.log`), and R849-1's probe P3 catches it as well (`receipts/r849-1/r849-probes-renew-if*.log`, rc 1 as expected). |
| R849-1 F3 SUGGESTION: in-place rebind | **Resolved** | `ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream` is extended in place. Plant `r849-bind-copy-skipped-for-self` is caught at both counts. |
| R849-1 F4 RESIDUE: report-local label | **Resolved** | `srp_mbx.cpp:1891` reads `// #925: the talker replaces ...`. No "Finding 18" remains. |

The legacy R849-1 driver's `r849-unknown-withdraws` targets a test this round removed. I re-selected it against its
replacement, `AFullHeldTableHoldsNothingMore`, with that test's own words, and it is caught at both counts. This
confirms the author's disclosure in the PR's limitations.

## Checks against the brief

1. **R850-1 F1:** met; see the table above. My own probe `R8492WithdrawalBeforeAMessageThatChangesNothingIsSentWithinAJoinTime`
   covers both kinds and both trailers, and the head passes it at both counts. In that scenario the withdrawal
   half is owed with or without the filter's hold: plant `r849-2-filter-holds-no-withdrawal` does not change the
   observed result. That is an equivalent mutant there, not a gap.
2. **R850-1 F2:** met. The order is kept per stream for the lifetime of the retained registrations, ending on
   either kind's leave, on expiry and on reset, and a binding of another identity takes none of it. The fallback
   test and plant are replaced. Plant `r849-2-held-latest-dropped` is caught. Plant `r849-2-reset-walks-forward`
   is masked because a link up resets the interface again (`srp_mbx.c:1125`), so no finding follows from it.
3. **R849-1 F1-F4:** met, as above.
4. **Coverage and budget:**
   - `srp_mbx.c` is at 768/768 lines and 695/695 counted branches, with 3 standing exclusions. I re-ran
     `fw_coverage.py --check --jobs 12` myself: rc 0, 39 files PASS (`receipts/r849-2/cov-check.log`). The ratchet
     line matches.
   - SRP campaign: the author's shard 3 receipt shows 465 caught, 0 escaped. I spot-checked 10 author plants at
     2 interfaces and 8 at 1, and all are caught.
   - CPU budget, from the receipts at 1x1/1if and 8x8/1if: every SRP and THE TRANSMIT path is within its approved
     bound. Record apply is 237.99 and 222.20 us against 280. `mrpdu` is 1.87 and 2.62 ms against 20. There are no
     late, absent or unresolved timer outcomes, and the join intervals fall within 181 to 239 ms.
   - The 8x8/1if `polls.base`, `polls.acmp` and `polls.acmp_declined` statement misses are #914's (known). Moved
     costs are restated only by measurement + 5 %, rounded up to 5 us, and no source cost statement changes in
     the delta.
   - The 8x8/2if ledger entry is raised to 61.0 by the owner rule of 2026-11-15, as `sram` 115,120 B is 432 B past
     56 granules (`author-r3/receipts/ledger/plat_ledger-final.log`).

## Lens results at the head

```text
[R849] PASS Conformance - sw/firmware/ctrl/srp/srp_mbx.c:194-207,:398-402,:228-250,:657-690; #925 body; ruling 6930043105 - latest kind decides while both registered, falls back to the older on a leave, transmission work owed by the filter's copy; R850-1 reproductions and phase/order sweeps rc 0 at 1 and 2 interfaces
[R849] PASS RTL - sw/firmware/ctrl/srp/srp_mbx.h:35,:119-124,:157,:165; srp_mbx.c:26-27,:210-224,:1102-1108; lwSRP mrp_mad.c:62-79 - held table bound (16/32/40/81 from 2/2 and 9/9 shapes), uint8_t count asserted <= 255, swap-release walked backward, hold() re-entrancy-safe in the filter; no RTL, mailbox or gitlink change (receipts/restore-check.txt)
[R849] PASS Robustness - srp_mbx.c bind/leave/reset/filter paths; SrpTalkerKinds.* at srp_mbx.cpp:1893-2112; receipts/r849-2/probe-head-if*.log - leave of either kind, LeaveAll expiry, reset of own and other interface, another identity, full table, in-place rebind, unchanged and ignored trailers, New+Lv in one MRPDU
[R849] PASS Tests - srp_kind_mutants.py (23 plants); receipts/r849-2/{reviewer,author,explore,whole-dest}-if*.log, cov-check.log - prior-reviewer plants and 10/8 author plants caught at 2/1 interfaces; coverage reproduced; residual pinning gaps are S1 (suggestion)
[R849] MINOR Docs - docs/design/SPLIT_CONTROL_MEMORY.md:145,:173-174 - F1; srp/README.md:246-275,:496-503, plat/README.md, ctrl_memory.py docs and PR body otherwise checked against code and receipts
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | srp_mbx.c listener_kind, filter hold, talker_changed, bind; #925 scope; ruling 6930043105; R850-1 reproductions/probes/rebind | R849-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |
| RTL | CLEAN | srp_mbx.h held table and bound; srp_mbx.c held_stream/release_held/reset; lwSRP attribute size; gitlinks unchanged | R849-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |
| Robustness | CLEAN | bind/leave/expiry/reset/other-interface/full-table paths; 3 reviewer probes at 1 and 2 interfaces | R849-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |
| Tests | CLEAN | SrpTalkerKinds and SrpFeedback tests; plant campaigns (prior reviewer and author); exploratory plants; coverage --check reproduced | R849-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |
| Docs | UNCLEAN (F1) | SPLIT_CONTROL_MEMORY.md sections 3 and 5; srp/README.md; plat/README.md; ctrl_memory.py; PR body | R849-2 | 5f625090bbd09a67f01080aeaa1f05e9d9a79cdd |

To clear Docs, F1 must be fixed and Docs re-covered at the fixing head. If the fix touches only that document, the
other four lenses' scope is unchanged, so their coverage at this head carries.

## Real limits

- **No exact-head hosted evidence.** At review time the commit has no check run and no workflow run
  (`receipts/hosted-checks.txt`).
- **Several gates rest on published receipts only.** I verified all 234 `author-r3` files against the archive's
  `MANIFEST.json` (0 bad; `receipts/packet-verify.txt`). I did not re-run them myself: the firmware self-test
  shards (control/AECP/full SRP campaigns), the CPU budget runs, the platform ledger, the workflow replays or the
  release-image identity.
- **Clause texts were not re-read from the standards in this round.** I checked the citations against the ruling's
  quotations and the prior internal round's direct reading.
- **S2's cycle figures are an estimate** from reading the source, not a measurement.
- **Host-model results only.** These are not physical timing. Physical calibration was NOT RUN, and field skips are
  not hardware proof.
- **Known, not findings:** the 8x8/1if STATED lines are #914's; the timing floor is #818's (+0.030 ns setup, 0 ns
  hold); this round ran on the usage fallback.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `16ba667d`, live dev `6b66f66d`). Note that the
  PR's recorded base branch is `dev-soft-core`.
- Accept hosted and act evidence at the exact head.
- Run the bench gate: Listener Ready within 1 s of the Talker Advertise.
- Obtain the external review of this head.
- Carry R1 to the residue checklist.
- Publish this report and its MANIFEST.

## Receipts

Every file is listed in `MANIFEST.sha256`.

- `scripts/r849-2/plants.py`, `probes.cpp` and `probes.py`: this round's plants and probes.
- `scripts/r850-1/*` and `scripts/r849-1/*`: unchanged copies of the prior rounds' drivers from the archive.
- `receipts/r850-1/`, `receipts/r849-1/` and `receipts/r849-2/`: the runs, with their logs and rc files.
- `receipts/packet-verify.txt`, `hosted-checks.txt` and `restore-check.txt`. After the probes the clone was
  restored: tracked blobs, modes, index and the six gitlinks equal HEAD, and the session's ignored bytecode caches
  were removed.

R849-2 FINISHED
