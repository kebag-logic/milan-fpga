# Planted-defect and baseline runs at exact head 5e6fef3ee74dcf6766ac3923349ae83524bc0e7b

Driver: `scripts/probe_898.py`. Each plant goes into a disposable copy of `sw/firmware/ctrl`, never into the checkout. It runs on the repository's own arms (`aecp_arms.core_arm(..., 2, "app", <named tests>)` for AECP, `plat_arms.arm_platboot(1|2)` for the platform). It is graded by the repository's own readers (`aecp_mutants.caught`, `ctrl_mutants.caught`). A plant counts as killed only when it compiles, the arm completes with rc 1, and the named test fails with the plant's own diagnostic words.

## Baseline (unmutated copy of the head)

| arm | result | log |
|---|---|---|
| AECP app mode, 1 interface | PASS, 129 tests, the four new Face/AppFace tests OK | `base-aecp/baseline-app-if1.log` |
| AECP app mode, 2 interfaces | PASS, 129 tests, the four new Face/AppFace tests OK | `base-aecp/baseline-app-if2.log` |
| plat | PASS, 2 tests | `base-plat/baseline-plat.log` |
| platboot1 | PASS, 11 tests, `Boot.B11GetAsPathAnswersTheDatapathsSequence` OK | `base-plat/baseline-platboot1.log` |
| platboot2 | PASS, 11 tests, B11 OK | `base-plat/baseline-platboot2.log` |

## The author's plants (nine AECP, one platform), as the tables hold them

| plant | named test | result |
|---|---|---|
| face-as-path-count-read-as-avb-info | Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow | killed (`au-a`) |
| face-as-path-entries-at-one-ordinal | same | killed (`au-a`) |
| face-as-path-through-the-first-interface | same | killed (`au-a`) |
| face-as-path-truncated-at-its-bound | Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt | killed (`au-a`) |
| face-as-path-bound-off-by-one | same | killed (`au-a`) |
| face-as-path-count-unanswered-ignored | Face.AnUnansweredAsPathWordFailsItsPortThere | killed (`au-b`) |
| face-as-path-entry-unanswered-ignored | same | killed (`au-b`) |
| face-as-path-change-notifies-avb-info | AppFace.AnAsPathChangeNotifiesTheDatapathsSequence | killed (`au-b`) |
| face-as-path-change-on-the-first-interface | same | killed (`au-b`) |
| plat-as-path-unavailable | Boot.B11GetAsPathAnswersTheDatapathsSequence, platboot1 and platboot2 | killed at both (`plat`) |

## The reviewer's own plants (not in the author's tables)

| plant | defect | named test, words | result |
|---|---|---|---|
| rv-count-never-reported | `*count = 0u` | T1, "the count, the datapath's" | killed (`rv-a`) |
| rv-caller-capacity-ignored | `n > (capacity \| AECP_PATH_ITEMS)` | T2, "one past the capacity fails the port" | killed (`rv-c`). The first form in `rv-a` (`n > AECP_PATH_ITEMS`) was refused by the compiler (-Werror unused parameter). That is a probe compile error, not an escape. |
| rv-entry-ordinal-plus-one | ordinal `k + 1u` | T1, "in order" | killed (`rv-a`) |
| rv-last-entry-not-read | loop from k = 1 | T1, "the count, then each entry once" | killed (`rv-a`) |
| rv-entry-byte-order-swapped | `out[k] = __builtin_bswap64(out[k])` | T1, "in order" | killed (`rv-a`) |
| rv-entry-index-zero | entry reads at descriptor_index 0 | T1, "of its AVB_INTERFACE" | killed (`rv-b`) |
| rv-count-type-zero | count read at descriptor_type 0 | T1, "of its AVB_INTERFACE" | killed (`rv-b`) |
| rv-entry-through-first-window | entry reads through interface 0's window | T1, "read through its own interface's window" | killed (`rv-b`) |
| rv-as-path-event-dropped | AS_PATH_CHANGED marks nothing | T4, "an AS_PATH change notifies GET_AS_PATH" | killed (`rv-b`) |
| rv-path-not-in-face-ports | `.path` left out of the face's ports | — | refused by the compiler (-Werror unused function), so this defect cannot be built; not an escape |
| rv-plat-entries-dropped | count reported 1 for any non-empty path | B11, "the count the datapath serves", platboot1 and platboot2 | killed at both (`plat`) |

Where T1 = Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow, T2 = Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt, T4 = AppFace.AnAsPathChangeNotifiesTheDatapathsSequence.

`rv-a.rc` and `rv-b.rc` are 1 only because of the two compile-refused probe forms above; every plant that compiled was killed.
