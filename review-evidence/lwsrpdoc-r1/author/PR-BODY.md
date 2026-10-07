[A561]

This change documents lwSRP for developers, integrators, managers, and testers.
It adds usage sequences, a clause matrix, contribution guidance, and 22 readable graphs.
The obsolete diagram source and private instruction page are removed.

[Closes #1](https://github.com/kebag-logic/lwSRP/issues/1).

## Round 2

The [test harness fix](https://github.com/kebag-logic/lwSRP/pull/3) is merged.
The guides now describe the required host test dependency and passing suites.
The [state graphs](doc/developer.md#state-machines) were compared with [IEEE 802.1Q-2018, clauses 10.7.7–10.7.10](https://standards.ieee.org/ieee/802.1Q/6844/).
Their selected transitions match the tables.
Implementation differences have source-line links and appear in the [status matrix](doc/manager.md#implementation-status).
Planned work remains labelled as planned.

| Check | Result |
| --- | --- |
| [Sentence check](doc/tools/check_sentences.py) | rc 0; 708 prose units; none exceed 25 words. |
| [Reference check](doc/tools/check_references.py) | rc 0; no detected unlinked references. |
| [Link check](doc/tools/check_links.py) | rc 1; eight relative links await the separate licence files. |
| External links | Three repository URLs pass with authenticated access. Nine other URLs answer anonymously. |
| [Graph render](doc/tools/render_mermaid.py) | rc 0; all 22 graphs render; 2–11 nodes each; layouts inspected. |
| Host configure and build | rc 0. |
| Configured unit suite | rc 0; nine tests and 1690 assertions. |
| Isolated codec suite | rc 0; nine tests and 1690 assertions. |
| [Scenario execution](doc/tester.md#run-the-suites) | rc 0; three scenarios and ten steps pass. |
| Scenario dry run | rc 0; all ten steps match. |
| Published commands | All 16 occurrences executed; only the documented link dependency returns nonzero. |
| Checker fixtures | Authentication routing and failures checked; invalid source lines and missing targets are rejected. |
| Scope and artifacts | Source, build, and tests match the merged harness fix. No generated assets are included. |

The separate licence change must supply [LICENSE](LICENSE) and [NOTICE](NOTICE).
Repeat anonymous repository-link checking after publication.
The graphs show selected paths; they do not establish implementation conformance.
Hardware, embedded targets, state-machine runtime behavior, and interoperability remain unverified.
