Every graph was rendered from the exact source into SVG, then rendered into PNG for visual inspection.
All 22 render commands returned zero. All graphs have one identifiable subject and 2–11 named nodes or participants.
Labels contain at most six words. The longest message/note label contains 38 characters.
Dimensions, source, directions and label lengths are preserved in graph-inventory.json.
The review inspected all six contact sheets and the two indicated individual diagrams at native size.

| Source fence | Nodes | Direction | Subject and visual assessment |
| --- | --- | --- | --- |
| CONTRIBUTING.md:47 | 5 | TD | Contribution process; clear linear chain. |
| README.md:14 | 6 | TD | Integration surfaces; separate protocol and switch branches. |
| doc/architecture.md:10 | 11 | TD | Layer boundaries; readable branches and isolated future-driver pair. |
| doc/architecture.md:34 | 7 | TD | Receive processing; readable linear chain. |
| doc/architecture.md:56 | 4 | LR | Missing transmit boundary; clean dashed edges. |
| doc/developer.md:28 | 10 | TD | Ownership; FAIL. Attribute-list edge is hidden behind the port-timer box. |
| doc/developer.md:76 | 6 | TD | Applicant declaration; conditional branches and labels remain distinct. |
| doc/developer.md:114 | 6 | LR | Applicant observation; two clear parallel state chains. |
| doc/developer.md:146 | 7 | TD | Applicant withdrawal; convergence is readable. |
| doc/developer.md:182 | 3 | TD | Registrar; three-state cycle and loop remain distinguishable. |
| doc/developer.md:214 | 2 | LR | LeaveAll; loops and return edge are readable. |
| doc/developer.md:243 | 2 | LR | PeriodicTransmission; enable/disable directions are distinct. |
| doc/developer.md:269 | 6 | TD | Application extension; clear linear process. |
| doc/integrator.md:46 | 4 | Sequence | Creation/declaration; wide at 1390 units, but labels and lifelines are distinct at native size. |
| doc/integrator.md:81 | 4 | Sequence | Receive/observe; callback order and self-message are readable. |
| doc/integrator.md:115 | 3 | Sequence | Global time; one clearly bounded loop. |
| doc/integrator.md:144 | 3 | Sequence | Destruction limitation; notes do not overlap messages. |
| doc/integrator.md:169 | 2 | Sequence | Adapter lifecycle; simple chronological messages. |
| doc/integrator.md:201 | 4 | Sequence | Queue dispatch; producers, consumer and bus remain distinct. |
| doc/manager.md:41 | 6 | TD | Release-readiness process; readable linear chain. |
| doc/tester.md:62 | 6 | TD | Scenario writing; readable linear chain. |
| doc/tester.md:92 | 8 | LR | Coverage and gaps; two clean branches. |

For the failure, inspect diagrams/doc-developer.md-28.png and graphs/doc-developer.md-28.svg.
The timer rectangle spans x=210.3828125–470.3828125, y=320–398.
The list-to-value edge enters that unrelated rectangle before reaching its destination.
For example, its cubic curve contains the interior point approximately (453.56,383.17).
Nodes are painted over edges, making that portion invisible and suggesting an incorrect timer-to-value relationship.
This is a figure defect, not prose residue.
