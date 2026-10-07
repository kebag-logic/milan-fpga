[A561]

This change documents lwSRP for developers, integrators, managers, and testers.
It provides usage sequences, a code map, a clause matrix, contribution guidance, and 22 graphs.

[Closes #1](https://github.com/kebag-logic/lwSRP/issues/1).

## Round 3

The [status matrix](doc/manager.md#implementation-status) corrects the propagation clause and identifies absent stream service primitives.
The guides disclose the [destination-address deviation](https://github.com/kebag-logic/lwSRP/issues/6) and [cross-type LeaveAll delivery](https://github.com/kebag-logic/lwSRP/issues/7).
Both limitations include source-line evidence and integration guidance.
The [coverage guidance](doc/tester.md#coverage) now explains both repeated-operation assertions and the [wrong-disable coverage defect](https://github.com/kebag-logic/lwSRP/issues/4).
A scratch reproduction confirms that the wrong disable binding passes all three scenarios.

The [ownership graph](doc/developer.md#data-structures) now keeps every edge clear of unrelated nodes.
All 22 graphs were rendered and inspected for crossings and readable labels.
The corrected graph was inspected at native size and page width.
The [architecture test map](doc/architecture.md#test-layout) links the runner and scenario bindings.
The remaining standard, metadata, build-setting, and source-range references are corrected.
The [reference checker](doc/tools/check_references.py) now detects additional standard names and includes a self-test.

| Validation | Result |
| --- | --- |
| [Sentence check](doc/tools/check_sentences.py) | rc 0; 760 prose units; none exceed 25 words. |
| [Reference check](doc/tools/check_references.py) | rc 0; no detected unlinked references. |
| Reference self-test | rc 0; 79 cases pass. |
| [Link check](doc/tools/check_links.py) | rc 1; eight licence-file dependencies and one external access failure. |
| External links | Six repository URLs pass authenticated checks. Eleven other URLs answer anonymously; the required [ISO page](https://www.iso.org/standard/57853.html) returns HTTP 403. |
| [Graph render](doc/tools/render_mermaid.py) | rc 0; 22 graphs, 2–11 nodes; no edge crosses an unrelated node. |
| Host configure and build | rc 0 for both published sequences. |
| Configured and direct unit runs | rc 0; nine tests and 1690 assertions. |
| Isolated codec suite | Compile and execution return rc 0; nine tests and 1690 assertions. |
| [Scenario execution](doc/tester.md#run-the-suites) | rc 0; three scenarios and ten steps pass. |
| Scenario dry run | rc 0; all ten steps match; no behavior executes. |
| Wrong-disable reproduction | Configure, build, and scenario run return rc 0; all three scenarios still pass. |
| Published commands | All 17 occurrences executed; 16 return rc 0. The link check returns rc 1 as detailed above. |
| Scope and whitespace checks | rc 0; source, build, and test files are unchanged. |

The separate licence change must supply [LICENSE](LICENSE) and [NOTICE](NOTICE).
Recheck the required [ISO page](https://www.iso.org/standard/57853.html) when anonymous access is available.
Repeat anonymous repository-link checking after publication.
Hardware, embedded targets, state-machine runtime behavior, and interoperability remain unverified.
The state diagrams show selected normative paths; they do not establish implementation conformance.
