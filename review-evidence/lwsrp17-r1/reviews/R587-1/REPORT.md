[R587] POSITIVE - exact head a44eeedf9abb0549b473acfb46eb910e99f397e1

# R587-1 external independent review: kebag-logic/lwSRP PR #18 (issue #17)

- Head `a44eeedf9abb0549b473acfb46eb910e99f397e1`, tree `67b35af9c7a906ea044e04686362d58811f85051`, base main `9197193e47a6bb1c45a56d90a18c1784123aba44`.
- Five commits, 16 files, +1411/-66. Every commit has a one-line subject, no body and no trailer, as CONTRIBUTING.md requires.
- Review start: https://github.com/kebag-logic/lwSRP/pull/18#issuecomment-6094814877.
- I reconstructed scope in this order:
  1. CONTRIBUTING.md and README.md (this repository has no AGENTS.md) and doc/*.md.
  2. The issue #17 body (frozen acceptance 1-5), the assignment comment 6094124382 (scope decisions), TAKEN and REVIEW READY.
  3. The full diff `9197193e..a44eeedf` and its history.
  4. The public evidence at `milan-fpga@f19066eb:review-evidence/lwsrp17-r1`. MANIFEST.json, author/HANDOFF.md and author/PR-BODY.md were fetched, and their sha256 values match the manifest (`receipts/published-evidence-sha256.txt`).
- The only manager comments on the issue and PR are the assignment and the two review-start comments; there are no manager evidence comments.
- No manager source bank ran at this head, and none is claimed or inferred here. The author's published gate receipts are the source-head execution evidence. Everything below is a focused reviewer rerun or probe.

## Verdict

POSITIVE. Every acceptance item of issue #17 is met at this head. I reproduced each one with my own runs, and also with tooling I wrote independently of the reviewed tree. I found no BLOCKER, MAJOR, MINOR or RESIDUE. Four SUGGESTIONs are recorded; none affects the verdict.

## Acceptance, item by item

| # | Acceptance (issue #17) | Reviewer evidence at this head | Result |
| --- | --- | --- | --- |
| 1 | One Message per AttributeType per opportunity; one EndMark each plus the PDU EndMark; ascending types; ascending FirstValue; LeaveAll per type as today; NumberOfValues 1; no "+k" | Code read of `src/core/mrp_mad.c:1288-1493`. My decoder (`scripts/r587_decode.py`, written from 10.8.1.2/10.8.2) graded the PDUs below; it ignores the trace shim's decoded columns. All grouped-form rules hold. | Met |
| 2 | Decoded equivalence per opportunity across every existing scenario, with a test-side decoder | `tests/check_equivalence.py` rc 0 in both profiles: 22 scenarios, 148 opportunities, 138 PDUs; 125 identical, 13 layout-only, 0 different. My decoder independently re-reads the raw bytes of both traces with the same totals (`receipts/decoder/compare-base-suite-{OFF,ON}.txt`). The test decoder includes only `mrpdu_decoder.h` and `<string.h>`; it shares no code with `src/core/mrp_pdu.c`. | Met |
| 3 | Byte-exact goldens for the five named cases | `tests/unit/grouping_test.c:103-250` and `:294-362`. Two Listener values (33 octets); Domain B then A (23); Talker Advertise and Listener in type order (95); empty types under LeaveAll (118); MVRP under LeaveAll (21); exact fit (33, no split); one octet short (two 21-octet PDUs); 1500-octet PDU with 124 Listener vectors (1497); and the 65535-octet bound (65529). All pass in both profiles. | Met |
| 4 | Receive path accepts per-value, grouped and "+k" packed forms, each tested | Three named tests (`:543-556`). The receive parser `src/core/mrp_pdu.c` is not in the diff. My receive plants Q1 (deliver only each Message's first vector) and Q2 (ignore "+k" offsets) are killed by `received_values_grouped_in_one_message_register` and `received_values_packed_in_one_vector_register` respectively. | Met |
| 5 | Existing suites pass; split Message, wrong EndMark count, wrong vector order and dropped vector each caught by a named test | All gates rc 0 (table below). The author's five reversals are killed with their named tests in both profiles: 11, 11, 9, 13 and 1 failing tests. I re-applied all four defect classes in my own forms (P1-P4); each is killed by the unit suite in both profiles. | Met |

The issue's scope comment adds three constraints, also met:
- Only `tx_vector` and its MRPDU assembly change: every `mrp_mad.c` hunk is at line 1285 or later, and lines 1-1284 are byte-identical to base.
- No heap and no new callback: the added source uses only the existing `attr_len`, `attr_has_subtype` and `encode_attr` ops, and no allocation.
- The parent consumer table exists in the public handoff; it is checked below.

## Gates rerun by the reviewer (exact head, both profiles)

`scripts/run_gates.sh` ran all independent gates concurrently. Raw logs and rc files are in `receipts/gates/`. The unit framework was built from its upstream 1.7.0 tag into scratch.

| Check | Default | Milan |
| --- | --- | --- |
| Configure / build (warning lines) | rc 0 / rc 0 (0) | rc 0 / rc 0 (0) |
| CTest | rc 0 | rc 0 |
| Unit runner | rc 0; 102 tests (9 suites), 26658 passes; grouping_suite 6757 | rc 0; 26646 passes; grouping_suite 6757 |
| Scenarios | rc 0; 3 scenarios, 10 steps | rc 0; 3 scenarios, 10 steps |
| Scenario dry run | rc 0 | — |
| Equivalence | rc 0; 22/148/138; 125/13/0; 0 problems | identical |
| Reversals | rc 0; 99 reversals, 0 failures | rc 0; 99, 0 failures |
| Freestanding | rc 0; 7 sources | rc 0; 7 sources |
| Embedded check (both profiles) | rc 0 | — |
| Strict `-Wall -Wextra -Wpedantic -Werror` compile of `mrp_mad.c`, two C compilers | rc 0, rc 0 | — |
| Documentation | Sentences rc 0 (1012, 0 over); references rc 0 (0 unlinked); self-test rc 0 (79 cases); links rc 0 (366 local, 21 external, 0 failures, authenticated read-only); graphs rc 0 (28 rendered, including the new layout graph at `doc/developer.md:114`) | — |

The scenarios run under the transmit trace leave no trace file, so the switch scenarios make no transmit call; this confirms `doc/tester.md`'s claim (`receipts/decoder/behave-under-trace.txt`).

## Independent evidence beyond the author's gates

1. **Reviewer decoder** (`scripts/r587_decode.py`). It is my own code, written from 10.8.1.2, 10.8.2, 35.2.2.6 and 35.2.2.7.2, and it reads only the raw PDU hex, EtherType, send rc and call records.
   - **Base suite**: both traces give 148 opportunities, 138 PDUs, 125 identical, 13 layout-only and 0 different, in both profiles. Every head PDU passes the grouped-form grade and fits its declared capacity.
   - **Order-only changes**: two of the 13 layout-only PDUs change the relative order across types, as the type order requires. In `refused_pdu_survives_timers_without_aging_unsent_leaveall#3`, LeaveAll for types 2-4 now follows a type-1 value. In `retained_ports_replay_propagated_join_and_timer_leave_in_order#7`, the Talker Advertise Message now precedes Domain. See S2.
   - **Head suite**, traced in both profiles: 340 PDUs. 339 PDUs (1077 vectors) pass with no capacity violation. The 65529-octet PDU is truncated by the shim's record buffer (S3), so I graded it directly: `scripts/r587_bound.c` gives 65529 octets, one Message of 2340 ascending vectors and AttributeListLength 65522, grade OK. The base encoder emits 81603 octets for the same input, so the 65535-octet bound is new protection.
2. **Differential fuzz, base library against head library** (`scripts/r587_fuzz.c`, `scripts/r587_fuzz_compare.py` and `scripts/run_fuzz.sh`; receipt `receipts/fuzz/fuzz-head.txt`).
   - The campaign covers three applications × two profiles × roomy and tight capacities × 60 seeds × 400 steps.
   - The inputs are random declarations, withdrawals, received PDUs (including LeaveAll), timer jumps and 1-in-8 send refusals.
   - Results: 720 jobs, 181602 PDUs, 0 failing. Roomy runs match base on every call's result, send count and decoded-event multiset, with 87682 layout-only PDUs.
   - Every head PDU decodes and passes the grouped grade. None exceeds its capacity, and a guard region past the capacity was never written. Every retried PDU is byte-identical to the refused one.
3. **Reviewer plants** (`scripts/r587_plants.py`; per-plant JSON with the exact diff in `receipts/plants/`). These are written independently of `tests/check_reversals.py`, each in its own scratch clone, and run in both profiles.

| Plant | Defect class | Unit tests failing (both profiles) | Equivalence check | Reviewer fuzz |
| --- | --- | --- | --- | --- |
| P1 a third vector opens a second Message | split Message | 9 | rc 1 (9 different) | 48/48 fail |
| P2 MVRP/MMRP Messages lose their EndMark | wrong EndMark count | 2 (`vlan_leaveall_message_carries_the_declared_vectors`, `every_vlan_and_mac_pdu_keeps_one_ordered_message_per_type`) | rc 1 | 32/48 |
| P3 sort compares only the first FirstValue octet | wrong vector order | 7 | rc 1 | 48/48 |
| P4 list-head value committed but not written | dropped vector | 14 | rc 1 (128 different) | 48/48 |
| P5 LeaveAll vector after the values | LeaveAll position | 4 | rc 1 | 48/48 |
| P6 Messages in descending type order | Message order | 4 | rc 1 | 32/48 |
| P7 first-vector cost omits the EndMark | sizing (overrun) | 1 (`one_octet_short_moves_a_vector_to_a_second_pdu`) | **rc 0** | 24/48; 1674 writes past capacity |
| P8 values with no transmit message are also written | event semantics and overrun | **0** | rc 1 (6 different) | 48/48; 1601 writes past capacity |
| Q1 receive delivers only each Message's first vector | receive grouped | 3, including `received_values_grouped_in_one_message_register` | — | — |
| Q2 receive ignores "+k" offsets | receive packed | 4, including `received_values_packed_in_one_vector_register` | — | — |

4. **Event and state-machine semantics are unchanged.**
   - Lines 1-1284 of `src/core/mrp_mad.c` are byte-identical to base. That range holds `appl_table`, `reg_table`, `appl_event`, `reg_event`, `deliver_event` and the whole receive side.
   - From `ps->in_send = true;` to the end of the file (the send, retained-PDU retry and commit loop: tx!, txLA!, txLAF!, local rLA!, periodic, join timer), the code is byte-identical to base.
   - The transmit prologue differs only by an unused local that was removed.
   - The wire event moved from selection into `tx_message` (`:1374`). Its inputs `e->tx` and `a->reg` do not change between selection and assembly.
   - Two Talker Failed / Talker Advertise replacement probes (`scripts/r587_talker_swap.c`, `receipts/decoder/talker-swap-*.txt`):
     - Failed to Advertise: byte-identical to base.
     - Advertise to Failed: the PDU is reordered to Leave(Advertise) before New(Failed). A lwSRP receiver gives identical indications for the base and head orders.
5. **Resources** (`receipts/static-size-stack.txt`; reviewer flags, so absolute figures differ from the author's).
   - Host `-O2`: `mrp_transmit` 176 octets (dynamic, bounded) became 304 (static); text 14661 became 15518.
   - RV32 (`-Os -march=rv32gc`): `mrp_transmit` 96 became 208 static; the 80-octet `tx_vector` frame is gone; text 10183 became 10611.
   - Every frame is static or bounded. There is no recursion and no heap.
   - Ordering is an in-place insertion. On the host, worst case, it costs about 170 ms for 2340 vectors in 64 KiB storage, and a fraction of a millisecond at Ethernet sizes (`receipts/decoder/bound-probe.txt`).

## Parent consumer (milan-fpga dev 554e61d2; gitlink still 9197193e)

I read a sparse, read-only scratch fetch of `sw/firmware/ctrl/` and the cited documents. Nothing was built, run, committed or pushed.
- Every line cited in the public handoff's byte-level table matches `554e61d2` (`receipts/parent/cited-lines-554e61d2.txt`).
  - The `srp_latency.cpp` walker is at `:68-77`.
  - `srp_fixture.hpp:76-128` is the generic vector walker, layout-independent.
  - `srp_mbx.c:521` uses lwSRP's own parser.
  - `srp_mbx.c:800` gives 1500 octets of storage; `MBX_FRAME_BYTES_MAX` is 1514, so 124 Listener values fit (83 before).
  - Also matching: `ctrl_arms.py:362`, `docs/reference/SUBMODULES.md:26` and `docs/diagrams/submodule_boundaries.svg:72`.
- Other SRP transmit consumers (`srp_walk`, `srp_shape`, `srp_app`, `srp_mbx`, `srp_feedback`) use either `capture()` or the EtherType and channel only. I found no other layout-dependent transmit expectation in `sw/firmware/ctrl`.
- I emulated the `srp_latency.cpp:68-77` LeaveAll detector (`scripts/r587_parent_walker.py`, `receipts/parent/walker-emulation.txt`).
  - Base output: 0 wrong verdicts over 15938 MVRP and 16454 MSRP fuzz PDUs.
  - Head output: 9199 wrong MVRP verdicts, plus 4 of 20 base-suite MVRP PDUs. An example is `000102000100086c0001000b6c00000000`.
  - MSRP is unaffected.
  - The handoff's proposed vector walk gives 0 wrong verdicts.
- This confirms the handoff's pin-bump item. It is a parent duty, not a defect in this library.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R587-S1 | SUGGESTION | Tests, Robustness | `tests/unit/grouping_test.c:36-44` (`capture`), `:64-70` (`transmit`), `:364-384` (`sweep`) | Plant P8 (`src/core/mrp_mad.c:1366` without `e->tx == TX_MSG_NONE`) passes all 102 unit tests in both profiles, yet writes past the caller's capacity 1601 times in 24 tight fuzz runs. Plant P7 (cost omits the EndMark) overruns 1674 times and is caught by one golden only. No unit test compares an offered length with the capacity passed, or decoded events with the expected Applicant transmissions. Only the base-pinned `tests/check_equivalence.py` kills P8. | The head is correct (0 overruns in 181602 PDUs). But selection budget and writer filter are now two copies of one rule, a memory-safety invariant that the long-lived suite does not pin. The equivalence check is tied to base `9197193e` and will lose value once intended semantics change. | Optional: in `transmit()` and `sweep()`, assert `frame_len <= capacity`. Optionally run the sweeps with storage exactly at capacity plus a guard. | Re-run P7 and P8 with `scripts/r587_plants.py`; both should then fail named unit tests. |
| R587-S2 | SUGGESTION | Conformance, Docs | `doc/developer.md:109-130` ("MRPDU layout") | In a LeaveAll PDU, the LeaveAll for type n+1 now follows type n's values. This happens in `refused_pdu_survives_timers_without_aging_unsent_leaveall#3` (`receipts/decoder/compare-base-suite-OFF.txt`) and in fuzz output. It is decoded-equivalent because LeaveAll is applied per type (`src/core/mrp_mad.c:1069-1077`, existing `leaveall-scope` reversal), and the issue fixes "flagged per type as today". | A peer that applied a received LeaveAll across every type would see these PDUs differently from the old layout. This is an interoperability note within the frozen scope. | Optional: add one sentence to the layout section. It should say that a type's LeaveAll can follow earlier types' values, and that per-type LeaveAll scope is relied upon. | Documentation checks stay rc 0. |
| R587-S3 | SUGGESTION | Tests | `tests/unit/transmit_trace.c:35` (`record[1u << 16]`) | Tracing the head's own suite truncates the 65529-octet PDU's record to 65463 hex digits (`receipts/decoder/grade-head-suite-*.txt`). | None for the gate: the base suite's largest PDU is 134 octets. It matters if the shim is reused on larger suites. | Optional: size the record from the PDU length, or mark truncated records explicitly. | Trace the head suite; every record parses. |
| R587-S4 | SUGGESTION | Docs | `doc/integrator.md:251-256`, `src/include/shish_lan/mrp.h:260-266` | Ordering is an O(n²) in-place insertion. On the host, worst-case declaration order costs about 170 ms for one 65529-octet MSRP PDU, against well under 1 ms at Ethernet sizes (`receipts/decoder/bound-probe.txt`). | Only integrators passing storage far above a frame are exposed. | Optional: note that storage beyond the largest frame buys nothing but ordering time. | Documentation checks stay rc 0. |

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue acceptance 1-5 and the scope comment, checked against: `src/core/mrp_mad.c:1288-1493`; goldens G1-G8 and the 65535-octet bound; my 10.8 decoder over 138 base-suite, 340 head-suite and 181602 fuzz PDUs; Domain order by wire FirstValue (B=5 before A=6); LeaveAll form and position; NumberOfValues 1 and no "+k"; split only when a value no longer fits; AttributeListLength reach; receive per-type LeaveAll scope; S2 | R587-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |
| RTL (implementation and resources; no HDL in the diff) | CLEAN | Encoder structure; budget equals written length; 64-octet stack bitmaps; no heap and no new callback; host and RV32 frame and text sizes; insertion cost; state tables and receive side byte-identical (lines 1-1284); commit and retry tail byte-identical; brace and enum rules on added C lines | R587-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |
| Robustness | CLEAN | Receive tests for all three forms plus plants Q1 and Q2; parser not in the diff; no capacity overrun and guard intact over 181602 fuzz PDUs; refused-then-retried PDUs byte-identical; refused local declarations during retention; 65535-octet clamp; Talker replacement order probes; parent walker regression (parent duty); S1 | R587-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |
| Tests | CLEAN | Full gate bank in both profiles; equivalence rerun and independently re-decoded; 5 author reversals with named kills and matching counts; 10 reviewer plants (8 encoder, 2 receive); decoder independence (includes); fuzz negative controls (P1-P8 all detected); S1, S3 | R587-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |
| Docs | CLEAN | README, architecture, developer, integrator, manager and tester diffs; `mrp.h:257-267` contract; anchors `#L1351`, `#L1388`, `#L1410` and the unchanged `#L506`, `#L755`, `#L773`; counts (102, 9 suites, 26658/26646, 99, 22/148/138/125/13, 124 values per 1500 octets); documentation checks, links and graphs rc 0; PR body claims; S2, S4 | R587-1 | a44eeedf9abb0549b473acfb46eb910e99f397e1 |

## Prior public review findings

At this head, PR #18 has 0 reviews and 0 review comments. Its issue comments are the two review-start comments and the internal reviewer's R586-1 report (POSITIVE). The issue has no comment after REVIEW READY.
- R586-1 raised no BLOCKER, MAJOR, MINOR or RESIDUE, so no finding needs resolving.
- Its three SUGGESTIONs stay open as suggestions. My own evidence supports each:
  - R586 S1 is consistent with R587-S1 (my P7 and P8, with overrun counts).
  - R586 S2 is consistent with R587-S2.
  - R586 S3 is consistent with R587-S3.
- Disclosure: I fetched the PR comment thread to find manager evidence comments. That thread contained the R586-1 report, which I read before my own pass, contrary to the intended order. All my scripts, plants, probes and measurements were written and run by me, and every figure above comes from my own receipts. Where a probe resembles one in that report, it was re-derived and re-run (P8 is a variant of R586's R9), and the receipts are mine.

## Real limits

- No manager source bank ran at this head. The source-head execution evidence is the author's published receipts plus my focused reruns.
- I ran no parent arms, parent documentation set or parent SRP plant campaign; full parent banks are out of scope. These parent claims are the author's and unverified by me: 59/59 arms, 1191 cases, 237 plants caught, and 14/14 documentation gates after the pin-bump edits. My parent checks were cited-line reads, a grep of `sw/firmware/ctrl` only, and the walker emulation.
- I did not read the IEEE 802.1Q-2018 text. Conformance was judged against the frozen issue scope, the clause references in the source, and the project's existing per-type LeaveAll handling.
- My size and stack figures use reviewer flags, not the parent's RV32 arm flags. I did not reproduce the author's RV32 figures or the CPython 3.12.3 runs.
- No hosted CI exists for this repository: there is no workflow directory, and the head has 0 check runs and 0 statuses (`receipts/hosted-and-pr-state.txt`). Nothing ran and nothing was skipped.
- Physical calibration was NOT RUN, there is no hardware evidence, and field skips are not hardware proof.
- The pinned simulator's identity was verified (5.050), but it was not used: the diff has no HDL.
- After the probes I verified the review clone byte for byte (`receipts/restore-verification.txt`):
  - HEAD `a44eeedf`, tree `67b35af9`, index tree identical;
  - 65 of 65 tracked blobs and modes match;
  - 0 untracked or ignored files;
  - this repository has no gitlinks.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn (source base `9197193e`, live dev `554e61d299ef7ddb5aca6fb9ce0e6a6cd076d8cb`), with builder and native banks, and link the receipts on the PR.
- Own hosted and local workflow acceptance (this repository has none).
- Carry out the parent pin bump, which is outside this PR:
  - `ctrl_arms.py:362` `LWSRP_REV` and `docs/reference/SUBMODULES.md:26`;
  - regenerate `docs/diagrams/submodule_boundaries.*` and the PNG manifest;
  - update the prose pin mentions;
  - apply the vector walk in `sw/firmware/ctrl/test/srp_latency.cpp:68-77`. My emulation shows the current walk gives wrong LeaveAll verdicts on grouped MVRP output.
- Merge still requires the full completion bar. Optionally carry R587-S1 to S4 to the author.

R587-1 FINISHED
