[R586] POSITIVE - exact head a44eeedf9abb0549b473acfb46eb910e99f397e1

# R586-1 internal independent review: kebag-logic/lwSRP PR #18 (issue #17)

- Head `a44eeedf9abb0549b473acfb46eb910e99f397e1`, tree `67b35af9c7a906ea044e04686362d58811f85051`, base main `9197193e47a6bb1c45a56d90a18c1784123aba44`.
- Five commits, 16 files, +1411/-66. Every commit has a one-line subject with no body or trailer, as CONTRIBUTING requires.
- Scope came from these sources, read in this order:
  - CONTRIBUTING.md and README.md (this repository has no AGENTS.md);
  - doc/*.md;
  - the issue #17 body and the assignment comment 6094124382;
  - the full diff and history;
  - the public evidence `milan-fpga@f19066eb:review-evidence/lwsrp17-r1` (MANIFEST.json, author/HANDOFF.md, author/PR-BODY.md).
- No manager evidence comments exist on the issue or the PR, apart from the review-start comment 6094650072.
- No manager source bank was run at this head, and this report neither claims nor infers one. My reruns are focused reviewer probes. The author's published gate receipts remain the source-head execution evidence.

## Verdict

POSITIVE. Every acceptance item of issue #17 is met at this head. I reproduced each one with my own runs and with tooling I wrote myself. I found no BLOCKER, MAJOR, MINOR or RESIDUE. Three SUGGESTIONs are recorded below; they do not affect the verdict.

## What I verified (reviewer-run, exact head, both profiles unless noted)

All gate commands are in `scripts/run_gates.sh`. Raw logs and rc files are in `receipts/gates/`.

| Check | Result |
| --- | --- |
| Configure and build, default and Milan | rc 0; 0 warning lines in both build logs |
| CTest | rc 0, both profiles |
| Unit runner | rc 0. 102 tests (`receipts/static/test-count.txt`). Default 26658 passes, Milan 26646; `grouping_suite` 6757 passes in each |
| Scenarios and dry run | rc 0. 3 scenarios and 10 steps pass in both builds; dry run rc 0 |
| `tests/check_equivalence.py` | rc 0 in both profiles. 22 scenarios, 148 opportunities, 138 PDUs: 125 byte-identical, 13 layout-only, 0 different, 0 problems. Identical to the published table, row for row |
| `tests/check_reversals.py` | rc 0 in both profiles; 99 reversals, 0 failures |
| Freestanding (both profiles), embedded check | rc 0 |
| Strict `-Wall -Wextra -Wpedantic -Werror` compile of `src/core/mrp_mad.c` | rc 0 with both C compilers |
| Documentation checks | rc 0 for each: sentences (1012, 0 over limit), references (0 unlinked), reference self-test (79 cases), links (366 local and 21 external, 0 failures), graphs (28 rendered, 0 failures) |
| Hosted CI at this head | None exists. The repository has no workflow directory, and the head has 0 check runs and 0 statuses. Nothing was skipped; nothing ran |

## Independent evidence beyond the author's gates

1. **A decoder I wrote, sharing no code with the library or the author's decoder** (`scripts/decode_traces.py`, written from 10.8.1.2 / 10.8.2 and 35.2.2.6 / 35.2.2.7.2).
   - It reads only the raw PDU bytes, EtherType and send result from the equivalence traces; the author's decoded columns are ignored.
   - On the base suite, base sources against head sources, both profiles: 138 PDUs, 125 identical, 13 layout-only, 0 decoded differently. Every head PDU also passes my own grouped-form grader. Receipts: `receipts/decoder/compare-base-suite-{OFF,ON}.txt`.
   - I counted 138 opportunities where the author's table has 148. My tool keys on send records, and 10 opportunities send nothing. Both tools agree on all 138 PDUs.
   - Traced over the head's own suite (339 decodable PDUs, 1077 vectors): 0 grouped-form violations. One 65529-octet PDU exceeds the shim's record buffer and was skipped (S3). Receipts: `receipts/decoder/grade-head-suite-*.txt`.
   - Capacity: 0 of 340 offered PDUs exceed the caller's declared capacity (`receipts/decoder/capacity-head-suite-*.txt`). By code reading, the written length equals the selection budget exactly: per Message, header + optional LeaveAll vector + k vectors + EndMark, plus 3.
2. **Negative controls.** Two of my plants, R9 and R4b, were run through the repository's equivalence check and through my decoder (`receipts/negctl/`).
   - R9: 6 PDUs decoded differently, rc 1, in both tools.
   - R4b: 128 PDUs decoded differently in my decoder; the repository check reports 128 different and 249 problems. rc 1 in both.
3. **I re-planted the defects myself.** 13 plants were written independently of the author's cases (`scripts/probe_plants.py`, `receipts/plants/`). All four defect classes from the acceptance were re-applied in new forms, and each was killed by the unit suite:

| Plant | Defect class | Unit tests failing |
| --- | --- | --- |
| R1, the base encoder dropped into the head | split Message | 10 |
| R2, no AttributeList EndMark | wrong EndMark count | 15 |
| R3, sort key ignores the last octet; R3b, no sort | wrong vector order | 6; 8 |
| R4, values dropped under LeaveAll; R4b, newest declaration dropped | dropped vector | 2; 14 |
| R5, cost misses the EndMark (overrun) | sizing | 1 (`one_octet_short_moves_a_vector_to_a_second_pdu`) |
| R6, old per-value cost | sizing | 3 |
| R7, Messages in descending type order | Message order | 4 |
| R8, AttributeListLength without its EndMark | length field | 13 |
| R10, LeaveAll cost misses its vector | sizing | 1 (`full_leaveall_reports_each_required_transition`) |
| R11, LeaveAll vector with NumberOfValues 1 | LeaveAll form | 5 |
| R9, writer also emits `TX_MSG_NONE` values | event semantics and overrun | **0: survives the unit suite.** Killed by `check_equivalence.py` (see S1) |

   The author's five reversal cases are also killed in my reversal runs, with named tests. Per-case failing-test counts are 11, 11, 9, 13 and 1, matching the published handoff.
4. **Event and state-machine semantics are unchanged.**
   - Every hunk in `src/core/mrp_mad.c` lies at line 1285 or later.
   - `appl_table`, `reg_table`, `appl_event`, `reg_event` and `deliver_event` are untouched. So are the post-send commit loop (`src/core/mrp_mad.c:1495-1541`: tx!, txLA!, txLAF!, local rLA!, periodic, join timer) and the retained-PDU retry path (`:1424`, `:1496-1500`).
   - The wire event is now computed in `tx_message` (`:1374`) rather than during selection. The inputs (`e->tx`, `a->reg`) are the same, with no state change between selection and assembly.
   - The receive parser `src/core/mrp_pdu.c` is not in the diff.
   - The diff adds no heap allocation and no new callback. The only ops it uses are the existing `attr_len`, `attr_has_subtype` and `encode_attr`.
   - Host `-O2` stack: `mrp_transmit` went from 176 octets (dynamic, bounded) to 304 octets (static). `.text` of `mrp_mad.o` grew from 16013 to 16749 octets (`receipts/static/`). These match the published host figures. I did not reproduce the RV32 figures.
5. **Receive path.**
   - Three named tests register the same values from per-value, grouped and "+k" packed encodings (MSRP Listener and Domain, MVRP VID). All pass.
   - LeaveAll is applied per AttributeType at `src/core/mrp_mad.c:1069-1077`. That scope is pinned by the existing `leaveall-scope` reversal, killed in both of my runs. This is what keeps the new cross-type LeaveAll ordering decoded-equivalent (S2).
6. **Parent consumer (milan-fpga dev `554e61d2`, gitlink `9197193e`).** I read it from a read-only scratch clone; nothing in the parent was built or run.
   - The cited lines in the public handoff's byte-level table match `554e61d2` (`receipts/parent/cited-lines.txt`).
   - A grep of the parent's firmware tests found no other layout-dependent transmit expectation. Fixed offsets appear only in receive frames the tests build themselves; transmit checks either use the generic fixture walker or compare EtherType and channel only.
   - I emulated the `srp_latency.cpp:68-77` LeaveAll detector over real PDUs (`scripts/parent_walker_probe.py`, `receipts/parent/`):
     - base-encoder output: 0 false verdicts;
     - head-encoder output: 4 false LeaveAll verdicts on the base suite and 47 on the head suite (example `000102000100026c000100036c00000000`);
     - with the vector walk proposed in the handoff: 0.
   - This confirms the handoff's pin-bump item. It is a parent duty, not a defect in this library.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

| ID | Severity | Lenses | Location | Evidence | Impact | Required outcome | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | SUGGESTION | Tests, Robustness | `tests/unit/grouping_test.c:36-44` (`capture`), `:364-384` (`sweep`) | Plant R9 (drop `e->tx == TX_MSG_NONE` from the `tx_message` filter, `src/core/mrp_mad.c:1366`) passes all 102 unit tests and CTest. Yet 74 of its PDUs exceed the caller's declared capacity, up to 178 octets against 120 (`receipts/negctl/r9-capacity.txt`). Only the base-pinned `check_equivalence.py` catches it (6 different). The sweeps declare capacities of 120-1500 inside a 4096-octet buffer and never compare the PDU length with the capacity. | The head is correct (0 of 340 over capacity). But the split between selection budget and writer is a new memory-safety invariant, and the long-lived unit suite does not pin it. The equivalence check is tied to base `9197193e`, so it may be retired once intended semantics change. | Optional: in `transmit()`/`sweep`, assert that each offered length is at most the capacity passed. Optionally also check decoded events against the expected Applicant transmissions. | Re-run R9 from `scripts/probe_plants.py`; it should then fail the sweep tests. |
| S2 | SUGGESTION | Conformance, Docs | `doc/developer.md:109-130` ("MRPDU layout") | With grouping, LeaveAll for type n+1 now follows type n's values. That happens in 1 base-suite PDU (0 before) and 6 head-suite PDUs (`la_after_value` in `receipts/decoder/`). It is decoded-equivalent only under per-type LeaveAll scope, which the project's receiver applies (`src/core/mrp_mad.c:1069`, `leaveall-scope` reversal). The issue fixes "LeaveAll flagged per type as today", so this is in scope. The author's handoff states it; the repository documentation does not. | A peer that applied a received LeaveAll application-wide would treat these PDUs differently from the old layout. This is an interoperability note, not a defect against the frozen scope. | Optional: add one sentence to the layout section. It should say that per-type LeaveAll scope is relied upon, and that a type's LeaveAll can follow an earlier type's values. | Documentation checks stay rc 0. |
| S3 | SUGGESTION | Tests | `tests/unit/transmit_trace.c:35` | The 64 KiB record buffer holds the hex of PDUs up to about 32 KiB. The head suite's 65529-octet PDU is truncated, and its newline is lost, so its record runs into the next one (`unmatched` in `receipts/decoder/capacity-head-suite-*.txt`). | None for the gate: the base suite's largest PDU is far smaller. It matters only if the shim is reused on larger suites. | Optional: size the buffer from the PDU length, or mark truncated records explicitly. | Trace the head suite and parse every record. |

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue acceptance 1-5 and the scope comment against the following: `src/core/mrp_mad.c:1288-1493`; 9 goldens (G1-G8 and the 65535-octet bound); the grouped-form grader; my own 10.8 decoder over 138 + 339 PDUs; Domain order by wire FirstValue (class B=5 before A=6); LeaveAll form and position; NumberOfValues 1 and no "+k"; MTU split behaviour; the 65535-octet MSRP bound | R586-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |
| RTL (implementation and resources; no HDL in the diff) | CLEAN | Encoder structure; bare-metal constraints (no heap, no new callback, 64-octet stack bitmaps); host stack and size; budget-equals-written-length proof; in-place O(n²) insertion (about 7.6 k swaps at 124 values for a 1500-octet PDU); unchanged state tables, commit loop and retry path; CONTRIBUTING brace and enum rules on new C lines | R586-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |
| Robustness | CLEAN | Receive tests for all three encodings; parser not in the diff; per-type LeaveAll receive scope; capacity never exceeded (0/340); `encode_attr` failure after selection commits nothing; 65535-octet clamp; parent walker regression (a parent duty); S1 | R586-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |
| Tests | CLEAN | Full gate bank in both profiles; equivalence rerun matching the published table; 5 author reversals with named kills and matching counts; 13 reviewer plants (12 killed by the unit suite, R9 by the equivalence gate); negative controls on both the repository and reviewer decoders; decoder independence (it includes only its own header and `<string.h>`); S1 and S3 | R586-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |
| Docs | CLEAN | README, architecture, developer, integrator, manager and tester diffs; `src/include/shish_lan/mrp.h:258-267` contract; anchors (`#L325`, `#L506`, `#L755`, `#L773`, `#L1351`, `#L1388`, `#L1410` resolve to the named functions); counts (102, 26658/26646, 99, nine suites, 22/148/138/125/13); documentation checks, graphs and links rc 0; PR body claims; S2 | R586-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |

## Real limits

- No manager source bank was run at this head. The source-head execution evidence is the author's published receipts plus my focused reruns listed above.
- I ran no parent firmware arms, parent documentation set or parent SRP plant campaign; those are outside the allowed scope. The parent claims (59/59 arms, 1191 cases, 237 plants caught) are the author's and remain unverified by me. I checked only the cited lines, the absence of other layout-dependent expectations (by grep), and the walker defect (by emulation).
- I did not reproduce the RV32 size and stack figures, the CPython 3.12.3 runs, or the trace-based claim that the behave scenarios make no transmit call.
- I did not re-read the IEEE 802.1Q-2018 clause text. Conformance was judged against the frozen issue scope, the clause references in the source and the project's existing per-type LeaveAll interpretation.
- No hosted CI exists for this repository at this head. Physical calibration was NOT RUN, there is no hardware evidence, and field skips are not hardware proof.
- The unit framework was built from its upstream 1.7.0 tag into reviewer scratch. One compile definition was supplied because the shallow source lacks git metadata.
- After the probes, the review clone was verified byte-for-byte against the exact head:
  - HEAD `a44eeedf`, tree `67b35af9`, index tree identical;
  - all 65 tracked blobs and modes match;
  - 0 untracked or ignored files;
  - this repository has no gitlinks (`receipts/restore-verification.txt`).
- The parent gitlink `third_party/lwSRP` at dev `554e61d2` is still `9197193e`; the pin bump is pending.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn: source base `9197193e`, live dev `554e61d299ef7ddb5aca6fb9ce0e6a6cd076d8cb`, builder and native banks. Link the receipts on the PR.
- Own hosted and local workflow acceptance (none exists in this repository).
- The parent pin bump, which is not part of this PR:
  - set `ctrl_arms.py` `LWSRP_REV` and the `docs/reference/SUBMODULES.md:26` row;
  - regenerate `docs/diagrams/submodule_boundaries.*` and its PNG manifest;
  - update the prose pin mentions;
  - apply the vector walk in `sw/firmware/ctrl/test/srp_latency.cpp:68-77`. My emulation shows it is required: 47 false LeaveAll verdicts otherwise.
- Obtain the second independent (external) review required before merge.
- Optionally carry S1-S3 to the author.

## Prior public review findings

None to resolve or retain. I checked after writing the verdict and ledger, at head `a44eeedf`:
- PR #18 has one issue comment, the review-start comment 6094650072;
- it has 0 reviews and 0 review comments;
- issue #17 has no comment after REVIEW READY (6094547884).

R586-1 FINISHED
