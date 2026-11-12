# The new plants on the working tree before the gate pass (aecp_mutants.campaign over the nine, ctrl_mutants.campaign over the one)

| Plant | Caught |
|---|---|
| face-as-path-count-read-as-avb-info (plants-aecp) | True |
| face-as-path-entries-at-one-ordinal (plants-aecp) | True |
| face-as-path-through-the-first-interface (plants-aecp) | False |
| face-as-path-truncated-at-its-bound (plants-aecp) | True |
| face-as-path-bound-off-by-one (plants-aecp) | True |
| face-as-path-count-unanswered-ignored (plants-aecp) | True |
| face-as-path-entry-unanswered-ignored (plants-aecp) | True |
| face-as-path-change-notifies-avb-info (plants-aecp) | True |
| face-as-path-change-on-the-first-interface (plants-aecp) | False |
| face-as-path-through-the-first-interface (plants-aecp2) | True |
| face-as-path-change-on-the-first-interface (plants-aecp2) | True |

The first run's two escapes were caught by the test, but on other words than their own: the count read through
interface 0 failed "the count, then each entry once" before the per-request interface check ran, and the notice for
AVB_INTERFACE 0 left no notice at all. The test was reordered (every request's interface is checked before the
request count) and the second plant names the words it fails on; the second run (plants-aecp2) catches both. The
clean-clone pass's AECP campaign runs all nine again at the final head.
