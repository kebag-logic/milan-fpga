https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009576644
[A10] **Owner decisions, 2026-10-06.** These replace the corresponding lines of the issue body.

1. **Start now.** #664 no longer waits for the end of the protocol-processor program. It is a documentation-only lane and runs in parallel with the processor work and the #665 firmware lanes.
2. **AECP moves to the core with the rest (option a).** ADP, ACMP, MAAP, SRP and AECP, including unsolicited notifications and counters, run on the bare-metal core in the Mark II default. The fabric keeps framing and timestamps, the gPTP plane, the media path and the ingress filter. The "unless the owner rules otherwise" line for AECP is resolved this way.
3. **Default flip.** The documents describe the split as the Mark II default and the all-fabric build as a supported option. The build switch flips to the split only after F2 to F5 (#665) pass the bench: all streams, all counters and the audio soak. Until then the all-fabric build stays the shipping default, and the documents say so explicitly, so the tree holds no contradiction.
4. **VERSION major 3 lands with the default flip, not in this PR.** 0x0003 identifies only images that run the split. #664 states the version-3 rule and the five-simulation landing plan, and leaves VERSION at major 2.

Acceptance items 1, 2 and 4 stand. Item 3 moves to the default-flip PR. The owner approves the requirement text before merge.


https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009584763
[A10] **Lane for #664: Mark II requirements, documents only.** Executor [A548], branch `664-mark2-reqs` from dev `423ac5d9`. Reviewers [R508] (internal) and [R509] (external). The owner decisions in 6009576644 replace the matching lines of the issue body.

**Items:**
1. **Ownership and placement** (`REQUIREMENTS.md` section 1).
   - ADP, ACMP, AECP (including unsolicited notifications and counters), MAAP and SRP become build-selectable placements.
   - The Mark II default is the bare-metal core. The all-fabric build is a supported option, and it is the shipping default until the switch flips after F2 to F5 pass the bench. Say so explicitly.
   - The fabric keeps framing and timestamps, the gPTP plane, the media path and the ingress filter.
2. **FR_NFR** (`docs/reference/FR_NFR.md`).
   - Rewrite NFR-SCOUT-01 (the single control hart and how stream capacity grows) and NFR-SCOUT-02 (who owns protocol control).
   - Rewrite NFR-SCOUT-03. For each moved path, a bounded firmware service latency inside its normative timeout replaces "never on firmware service latency". Derive each bound from the clause that sets the timeout, and cite the clause number. Use `docs/spec-refs.md` and the in-repo extracts first.
   - Define each path's test hook: where the latency is measured, from mailbox RX to TX commit.
   - Audio and gPTP deadlines stay fabric-only.
   - Update every row these trace to.
3. **The split document** (`docs/ARCHITECTURE_HW_SW_SPLIT.md`).
   - Give the ownership rule for each placement.
   - Describe the mailbox interface: several packet mailboxes; block RAM rings, a doorbell and one interrupt; 32-bit accesses, no DMA; a bus adapter per host; portable C behind a small HAL; one YAML contract. Cite `docs/design/MAILBOX_SPLIT.md` and `docs/reference/MAILBOX_CONTRACT.md` (F0), and the saved-state boot read and apply (F1).
   - State the bare-metal-first rule and the unit-test rule (#665 5992455815, 6008744385).
4. **No contradiction in the tree.**
   - Grep every document that cites these rows or states the old ownership: "never on firmware", "fabric-only" for these protocols, the AECP placement. Correct each one.
   - Regenerate the traceability matrix with its generator. Never hand-edit generated files.
5. **Version.** State the version-3 rule (`0x0003` identifies only images that run the split) and the five-simulation landing plan for the default-flip PR, including the `>> 16` major check in `tb/verilator/hostplane`. VERSION stays at major 2 in this PR.
6. **Owner approval.** PR-BODY.md gets a section titled "Requirement text for owner approval". It shows every changed requirement row as old text and new text, side by side.

**STOP conditions:**
- Any change outside documentation, requirement tables, traceability generators' outputs and docs gates' registrations. STOP and name it.
- A normative timeout you cannot cite. STOP with the list.

**Gates:**
- the full docs-check set on the committed head: `docs/traceability/gen_module_matrix.py --check`, `check_wire_accountability`, the requirement/traceability checks, TOC and style;
- the 48-command builder set, because docs-only PRs get the bank too.

All gates rc 0. Output: HANDOFF.md and PR-BODY.md ("Relates to #664" until the owner approves; the manager switches it to Closes at approval). Then post REVIEW READY with the head on #664. Do not push.

Do not edit or delete any existing comment.


https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009675758
[A10] **Ruling on [A548] STOP (6009666033): labelled project service budgets are authorised.**

Some paths have a standard that prescribes immediate action, ordering or cadence, but no numeric maximum. For those, NFR-SCOUT-03 states a **project service budget**, labelled as such and never presented as a normative timeout:

1. **One budget class.** Define a single control-plane service budget, T_svc: the time from mailbox RX (or the triggering event) to TX commit, measured at the test hooks you defined.
2. **Its value.** T_svc must be at most 10 % of the tightest related normative interval of every moved path. Show it in one table, path by path, with the clause numbers. The related intervals include:
   - the AECP command timeout (IEEE 1722.1-2021 9.3.2.6);
   - the GET_COUNTERS one-per-second spacing (Milan v1.2 Table 5.22);
   - the MAAP probe interval and retransmit count (IEEE 1722-2016 Table B.8);
   - the ADP advertisement and valid_time intervals;
   - the ACMP command timeouts;
   - the MRP JoinTime and LeaveTime used by SRP.

   Propose the number from that table. The owner approves it with the requirement text.
3. **Where a numeric normative timeout exists,** the path's bound is that timeout and T_svc must fit inside it. Cite both.
4. **The ordering obligations stay normative, separate from the budget.** They include notification after the response, as in #653 and Milan 5.4.5.2 and IEEE 1722.1-2021 7.5.2; DEFEND on a conflicting PROBE (B.3.x); and DEPARTING on shutdown (Milan 5.6.3.5.8 and 5.6.3.5.11).
5. `docs/spec-refs.md` is absent at this base. Cite from the in-repository transcriptions and the standards directly, as you did.

Then continue the assignment: edits, the full docs-check set on the committed head, the builder bank, HANDOFF.md and PR-BODY.md with the owner-approval section. Post REVIEW READY (or STOP) with the head. Do not push.

Do not edit or delete any existing comment.


https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014311316
[A10] **Owner decision, 2026-10-06: the ingress filter classifies on the full tuple.** This adds to the #664 requirements. PR #674 takes it in a further round before the owner approves the text.

**Rule.** The fabric ingress filter that feeds the mailbox (F0, `sw/mailbox/mailbox.yaml`) classifies each frame by **VLAN tag + destination MAC + EtherType + AVTP subtype**, then by the protocol's identity term:

1. **Tagged frames never reach the mailbox.** A frame with an 802.1Q tag stays on the fabric media path. AAF and CRF stream data use the SR class VLAN; every control protocol below is untagged. AAF/CRF subtypes also have no channel, so a stray untagged media frame is excluded too.
2. **Each channel accepts one exact tuple.** Everything else is dropped.

| Channel | Destination MAC | EtherType | Subtype | Identity term |
|---|---|---|---|---|
| `adp` | `91:E0:F0:01:00:00` | 0x22F0 | 0xFA | ENTITY_DISCOVER for 0 or own entity_id; F3 adds bound talkers' AVAILABLE/DEPARTING |
| `acmp` | `91:E0:F0:01:00:00`; own unicast accepted as a tolerance | 0x22F0 | 0xFC | talker or listener entity_id = own |
| `aecp` | own unicast MAC, per interface | 0x22F0 | 0xFB | (command AND target_entity_id = own) **OR** (response AND controller_entity_id = own) |
| `maap` | `91:E0:F0:00:FF:00` | 0x22F0 | 0xFE | overlaps own range |
| `srp` MSRP | `01:80:C2:00:00:0E` | 0x22EA | n/a | all |
| `srp` MVRP | `01:80:C2:00:00:21` | 0x88F5 | n/a | all |

3. **Own unicast, never any unicast.** "Own unicast" is the entity's MAC per AVB interface. That keeps the redundancy seam (#69) open, because the record carries the interface index. A unicast frame for another MAC is flooded traffic and must not reach the core.
4. **The AECP term is two-sided.** When the core commands a controller, for example the CONTROLLER_AVAILABLE liveness probe (Milan v1.2 5.4.5.3), the reply has controller_entity_id = this entity. F0's command-only term would drop that reply. F5 needs it.
5. **Counted drops.** An untagged frame with a control EtherType that fails its tuple increments a new `FILTER_MISMATCH` counter. The per-channel token buckets stay.

**Open items to confirm by clause before freezing the table:**
- the MVRP group address (IEEE 802.1Q Table 10-1);
- whether any Milan controller sends ACMP unicast (IEEE 1722.1-2021 8.2).

**Requirements change for PR #674.**
- The fabric ingress filter row in REQUIREMENTS.md section 1 and NFR-SCOUT-02 state rules 1 to 5.
- A new requirement row covers the filter, traced to the mailbox contract.
- H-AECP adds the two-sided case: a CONTROLLER_AVAILABLE response must reach the core, and one for another entity must be dropped.
- H-ADP, H-ACMP, H-MAAP and H-SRP add the tagged-frame, wrong-address and wrong-subtype rejections, and the FILTER_MISMATCH count.

**Implementation.** A small contract lane right after FT and before F2-F5 changes `mailbox.yaml`, `KL_mbx_rx` and the mailbox suite. Each rule gets a planted test.


https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014321497
[A10] **Owner approval, 2026-10-06.** The owner concurs with the requirement text in PR #674 at `8fb296e3` ("Requirement text for owner approval"), including the project service budget **T_svc = 10 ms**. The one exception is the ingress filter, which the owner specified in 6014311316.

- **Next round.** A further #674 round adds the filter rules (tagged frames never reach the core; an exact tuple per channel; own unicast MAC per interface; the two-sided AECP term; FILTER_MISMATCH) and their hook checks. It changes nothing else in the approved text.
- **Approval scope.** The manager checks that the added rows match 6014311316. Any other wording change at the new head returns to the owner for approval.
- **Merge.** PR #674 then switches to `Closes #664`, and merges after two POSITIVE reviews at that head, its candidate, act and hosted runs.


https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014341135
[A10] **Round 3 for PR #674: the ingress filter only.** The owner approved the text at `8fb296e3`, including T_svc = 10 ms (6014321497). The only exception is the ingress filter, which the owner decision 6014311316 adds. This round adds that and changes nothing else; any other wording change goes back to the owner.

1. **REQUIREMENTS.md section 1 and NFR-SCOUT-02.** State rules 1 to 5 of 6014311316:
   - tagged frames never reach the mailbox;
   - one exact tuple per channel (VLAN tag, destination MAC, EtherType, AVTP subtype), then the protocol's identity term;
   - own unicast MAC per AVB interface, never any unicast;
   - a two-sided AECP identity term (command AND target_entity_id = own, OR response AND controller_entity_id = own);
   - a FILTER_MISMATCH counter for untagged control frames that fail their tuple. The per-channel token buckets stay.
2. **A new requirement row for the filter,** traced to the mailbox contract (`sw/mailbox/mailbox.yaml`), with its verification method.
3. **Hooks (section 3.4.2).**
   - H-AECP adds the two-sided case: a CONTROLLER_AVAILABLE response (Milan v1.2 5.4.5.3) must reach the core, and one for another entity must be dropped.
   - H-ADP, H-ACMP, H-MAAP and H-SRP add the tagged-frame, wrong-address and wrong-subtype rejections and the FILTER_MISMATCH count.
4. **Confirm by clause before stating the table:**
   - the MVRP group address (IEEE 802.1Q Table 10-1);
   - whether ACMP is ever sent unicast (IEEE 1722.1-2021 8.2), which settles whether own unicast stays a tolerance on `acmp`.
   - If either differs from 6014311316, STOP with the clause text.
5. **The owner-approval section** shows only the added and changed rows from this round, old against new. Everything else is marked "approved at 8fb296e3".

Re-run the docs-check set and the builder bank on the committed head. Post REVIEW READY with the head. Do not push.

Do not edit or delete any existing comment.

