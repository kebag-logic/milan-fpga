# HANDOFF r4: [A814] second correction round for PR #966 (#884, #665 F6)

Status: corrections, ruled relearn and validation complete; ready for independent re-review (2026-11-22). Base of the round: `8167b70d`
(PR #966's head); head `8267b895`, nine commits: six to the reviews, then the hot list relearned as
[A10]'s ruling on the STOP requires (#884 issuecomment-7084113326) and the documents measured with it; the last commit corrects the measured gPTP pass contribution. Lane
`opt-gptp-sw`, branch `opt-gptp-sw-1`; local commits only, no push. Reviews answered: R884-2 (#966
issuecomment-7079633841) and R883-2 (#966 issuecomment-7079722237).

## Findings and their state

| Finding | Severity | State | Fix commit | Regression test (fails at `8167b70d`) | Plants |
|---|---|---|---|---|---|
| R884-2-F1 multiple responders without Follow_Up keep asCapable | MAJOR | fixed: `pd_multi` clears asCapable (and so the publication) when the second response arrives, in flight or after completion; the cease and its resume rules unchanged | `4e934621` | `Scripted.MultipleResponsesWithoutFollowUpClearAsCapableAtOnce` (the reviewer's probe, from an asCapable port, through the cease and its five-minute end), `ASecondResponseClearsAsCapableBeforeItsExchangeCompletes` (a late Follow_Up restores nothing), `OneClockAnsweringTwiceClearsAsCapableAtOnceAndDoesNotCease`; coverage, passing there too: `ALateSecondResponderClearsTheAsCapableOfACompletedExchange` | `multiple-responses-cleared-at-completion` (four tests) |
| R884-2-F2 a review named in a source comment | RESIDUE | fixed with the reviewer's exact text | `07784595` | | |
| R883-2-F1 a slave step inside the envelope's span drops the far port | MAJOR | fixed: peer delay runs on the LocalClock 11.2.19.3.3 assumes, the PHC less every step the servo applied (`local_off`); the port's own t1, t4 and the t2, t3 it reports are taken on it, so a step of either port, of any size, reaches no rate or turnaround | `4e934621` | `Net.AForwardStepOf300us...`, `...400us...`, `ABackwardStepOf300us...`, `...400us...` at 10 ms, `ABackwardStepOf475usKeepsAsCapableAt5msTurnaround`; coverage: `AForwardStepOf150us...`, `Scripted.AResponderThatStepsItsClockReachesNoRate` (the envelope, for a peer that stamps on a stepped PHC) | `steps-left-on-the-local-clock` (the own-step test and the five mid-step cases), `rate-envelope-dropped` (now the third-party responder's test) |
| R883-2-F2 two builder assertions fail, caused by the PR | MAJOR | fixed at the cause: the software arm's copy of the engine's PHC tie-offs is hoisted into one block for every build without the plane, so `gptp_adj_w`, `gptp_step_we_w`, `gptp_step_w` keep their census counts; the timestamp unit's five reads of the PHC crossing nets and the `--sw-gptp` opt-in are stated in the census and gate 1c with ruling item 6 as the reason | `7d4dc57c` | `test_baremetal_profile_contract`, `test_gptp_product_default_and_legacy_option` | the census's own planted extra reader, still refused (its expected count follows the census) |
| R883-2-R1, R2 heads and reviews named in source comments | RESIDUE | fixed with the reviewer's exact texts; S2's README wording too | `07784595` | | |
| R883-2-S1 the dead ternary in `rx_follow_up` | SUGGESTION | not taken: it keeps the TLV read in bounds should the refusal above it be removed, which the plant `follow-up-without-tlv-used` does | | | |
| R883-2-S3 bind the xvlog receipt to its head | SUGGESTION | taken in this round's receipts | | | |
| R883-2-S4 a wider crossing bench | SUGGESTION | not taken | | | |

Found on the way: the port's state grew 8 B (`local_off`), so the three gPTP memory-ledger points no longer matched
their pinned symbol sizes and the harness and the route prep refused their images. Measured again (`a6323318`):
`image_gptp` 1,104 and 2,152 B, `ctrl_plat` 20,160 B; the tiles stand (59.0, 64.0, 62.0). With the relearned hot list
(`631dc544`) the platform image is 152,072 B of rom and 99,392 B of sram, 1,528 B of rom left.

## The contract, for the second-hart lane

Mailbox contract 2.5 did not change this round: `sw/mailbox/mailbox.yaml`, `docs/reference/MAILBOX_CONTRACT.md` and
`sw/firmware/ctrl/mbx/mbx_contract.h` are byte-identical to `8167b70d`'s, so 2.5 stays additive and a 2.6 based on
it needs nothing re-based. What moved that a composition can meet:

- `hdl/milan/milan_datapath.sv`: the engine's three PHC tie-offs (`gptp_adj_w`, `gptp_step_we_w`, `gptp_step_w`)
  left the `g_gptp_sw` and `g_gptp_off` arms for one block, `g_gptp_engine_off`, after them, for every build without
  the plane. A lane that edits either arm merges against that block.
- `sw/builder/test_builder.py`: the datapath census's five PHC crossing nets now count 5 live references (the
  timestamp unit's read in the exclusive sw arm), gate 1c states the `--sw-gptp` opt-in, gate 1d's EtherType owners
  add `KL_ctrl_split.sv` and `KL_gptp_tsu.sv`.
- `sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py`: the three gPTP ledger points' pinned sizes (`image_gptp` 1,104
  and 2,152 B, `ctrl_plat` 20,160 B). A lane that changes `struct gptp_port` or the platform's `ctrl_plat` re-measures
  them; the tiles did not move.
- `struct gptp_port` (`gptp.h`) gained `uint64_t local_off` after `role`; the HAL and the adapter's calls are unchanged.
- `sw/firmware/ctrl/plat/ctrl_split_hot.txt` and `ctrl_split.ld`: the hot list relearned at `e81cecdb` with the gPTP
  ports in the traced image (286 entries; 15 of `gptp.c` and `gptp_mbx.c`). Every split image's code order moved,
  with gPTP or without. A lane that ships on another head learns the list again there, by the procedure the header
  records; the 2.6 composition's own code changes the traces, so it relearns rather than merging the order.
- `sw/firmware/ctrl/test/ctrl_hot.py` and `ctrl_srp_image.py`: LINKED leaves aside an entry of an object the image
  compiles none of (`GPTP_OBJECTS`, without `--with-gptp`), and refuses that exemption for an object the image links.
  A second hart's objects that only some images compile would take the same exemption by name.

## The STOP, its ruling and the relearn

At `a6323318` `egress_ledger.py --point 8x8-1if` failed on one row, `backlog-owed.service.aecp.last.if0`: 62.18188 ms
against 62.16 (`receipts/harness/aecp-row-phase.md`). The cause was phase, moved by placement: `gptp_mbx.c` was
unchanged, yet its cycles over backlog-owed's passes rose from 149,287 to 214,320 once the port grew ahead of it.
[A10]'s ruling: the figure does not move; relearn the hot list by its standard procedure with the gPTP port's and
adapter's paths measured into it, then measure again.

- **The relearn** (`receipts/hotlist/`): the optimisation line's procedure at `e81cecdb`. The 1x1/1if split image,
  arm A, was built `--with-gptp`, and its three recorded windows were traced. That gave 288 sections. The filter read
  144 link maps (48 builds: 3 points, 8 arms, plain and gPTP) and dropped the same two entries as before. So 286
  entries are listed: the 266 the list held, and 20 more, 15 of them gPTP's.
- **One rule needed scoping.** The 2026-11-18 ruling keeps an entry only if it links in every image the list serves.
  A gPTP entry cannot link in an image built without gPTP, so ctrl_hot.py's LINKED rule now leaves aside an entry of
  an object the image compiles none of. `ctrl_srp_image.py` names gPTP's two objects so without `--with-gptp`. The
  rule refuses that exemption for an object the image does link. Both are planted and caught in the self-test, which
  has two controls and ten plants. This reading of the 2026-11-18 ruling is the one the gPTP ruling needs; it is
  stated in the list's header and is open to the ruling owner.
- **Measured at `631dc544`**: `egress_ledger.py --point 8x8-1if` PASS on the gPTP image, every held row within, the
  AECP row 62.12258 ms and the ACMP row 62.45305 ms. `gptp_mbx.c`'s cycles over backlog-owed's passes are 104,430.
  The plain 8x8/1if image passes too, its AECP row at 61.84002 ms.
- **At 8x8/2if**, which has no ledger, the gPTP image's five owed rows are 63.910 to 64.957 ms. That is 0.05 to
  0.10 ms past the 1if figures; at `a6323318` the five were 0.033 under to 0.014 over. The ACMP row is 62.587 ms.

## Gates after the relearn

The earlier gate table and STOP are superseded by REVIEW-READY.md's measured table. That table names the head of
every run and the source changes since it. In particular:

| Check | Head | Result |
|---|---|---|
| Seven held rows, gPTP and plain 8x8/1if | `631dc544` data, final checker | PASS, every row measured, no new budget miss |
| Both turnaround measurements and CPU/share rows | `631dc544` | 0.309 / 0.292 ms turnaround; 0/5,139 and 0/5,217 passes over 2 ms |
| Five platform-memory points; fixture memory tests | `631dc544` | PASS; allocated tiles unchanged |
| Firmware gate, four shards | `631dc544` | 4/4; 826/826 controls caught; gPTP and UBSan 63 tests each |
| Hot-list checker and self-test | `8267b895` | 286 entries, two passing controls, ten caught plants |
| 73 docs/idiom/light gates, including vendor syntax check | `334ca4b7` | 73/73, none skipped |
| Final documentation correction, paths and audit | `8267b895` | All checks PASS |
| Budget harness self-test; rebuilt split boot at 1x1/1if and 8x8/1if | `631dc544` | PASS |
| Full simulation sweep / synthesis portability / routes | `e81cecdb` / `a6323318` / `a6323318` | Prior complete results retained with unchanged RTL; no post-relearn route claim |
| Fresh closed loop and plants | `334ca4b7` | 48/48 checks; 14/14 plants caught; flood keeps every delivered stamp and lock |
| Full builder suite | `8267b895` | rc=0; both reviewed assertions pass; two declared NOT RUN arms retained |

`receipts/after-relearn/source-equivalence.txt` records the checked input equality and the exact prose-only delta
since the measured firmware head. `measurement-audit.json` derives the CPU maxima from the raw logs and checks
both service conditions. The raw logs are identified by size and full sha256. The budget harness's seven nominal
20 ms misses remain the known held rows, governed by the separate 8x8/1if egress ledger; no 2if ledger pass is claimed.

## Merge surface

This round touches `hdl/milan/milan_datapath.sv` (the tie-off block), `sw/builder/test_builder.py` (census counts,
gates 1c and 1d), `sw/litex/ctrl_memory.py` and `ctrl_memory_ledger.py` (pinned sizes),
`docs/design/SPLIT_CONTROL_MEMORY.md` and `docs/design/GPTP_SOFTWARE.md`, and the port and its tests. A lane that
re-measures the ledger or edits the census's PHC rows meets this round's lines.

## Resume consolidation at the final head

Head: `8267b8951616cfd570baf690835d4b0d38f14596`. The final documentation-only commit corrects gPTP's largest
contribution to one work pass to 37,430 cycles (0.37430 ms), `backlog-owed` at 8x8/2if. It changes no executable
input. All nine commits remain local. The working tree is clean.

Every added-side diff hunk against `8167b70d`, including the hot-list reorder, is listed with file:line and reason
in `receipts/after-relearn/hunks.md`. Main anchors:

- `sw/firmware/ctrl/gptp/gptp.c:314`, `:523`, `:788`; `gptp.h:181`: immediate capability invalidation and
  LocalClock, with regressions at `test_gptp.cpp:500`, `:561`, `:1240` and the neighboring matrix cases.
- `hdl/milan/milan_datapath.sv:9470`: the single engine-off tie-off block; the second-hart lane merges here if it
  changes PHC ownership. Builder assertions remain assertions, with source attribution corrected at their cause.
- `sw/firmware/ctrl/test/ctrl_hot.py:97`, `:146`; `ctrl_srp_image.py:137`, `:261`: absent-object-only LINKED scope,
  and its two plants. Failure words: `named compiled out, yet the image links its sections` and
  `hot-list name ... is no section of the linked image`. All previous ORDER and LINKED plants still fail.
- `sw/firmware/ctrl/plat/ctrl_split_hot.txt:20` and `ctrl_split.ld`: measured section order; a composition relearns
  it from its own image rather than merging the order mechanically.

Contract 2.5 has **no wire, layout, event-routing or reset change in round 4**. The new LocalClock state lives
inside the firmware port. Its HAL and adapter interfaces are unchanged. Contract 2.6 still follows 2.5, with no
new assumption that TIMESTAMP belongs to hart 0.

No public comment was repeated: #884 already has the sole [A814] TAKEN and REPORT from round 1. No push, PR edit,
bench operation, merge or rebase was performed. The manager publishes this packet and requests fresh reviews.

REVIEW READY 8267b8951616cfd570baf690835d4b0d38f14596
