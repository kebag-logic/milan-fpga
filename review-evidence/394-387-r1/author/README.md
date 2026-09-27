[A375] Bench evidence packet

Refs #394 acceptance 2, e1 only. Refs #387 acceptance 4.

HANDOFF.md is the current status and cycle ledger. The assignment, identity, setup, complete cycle results, restore and validation are retained here. The new repository findings page is the public result.

| Artifact | Purpose |
|---|---|
| identity-result.txt, identity-uart.txt, identity-aecp.jsonl | CRC consistency readback and exact descriptor identity |
| expected-crc.txt, image-artifacts.json, csr.csv, port-proof.txt | Assigned build hashes, register map and e1 selection |
| image-to-base-diff.txt | Documentation/evidence-only difference from image source to lane base |
| census-start.jsonl, setup.jsonl | Original state and the two CRF bindings with source selection |
| cycleNN/analysis.json | All decoded cycle observations and timing estimates |
| cycleNN/raw-artifacts.json | Exact raw paths, sizes and hashes; large files remain under /tmp |
| cycleNN/events.jsonl | Clock probes, outlet commands and return codes |
| census-end.jsonl, restore-comparison.txt | Restored bindings, descriptors and clock settings |
| capture-prerequisite.txt, METHOD-NOTES.md | Capture prerequisite repair, two carrier methods, analysis limits |
| redaction.json | Explicit substitutions and original/retained hashes |
| gate-N.txt, gates.json | Nine assigned foreground gate results |
| tools/ | Small source files used for collection, analysis and reporting |

Reproduce analysis with `python3 -B tools/analyze.py cycleNN` while the listed raw artifacts remain available. The analyzer needs no bench access. `tools/ledger.py` refreshes the handoff table. `tools/report.py` requires all ten complete analyses and checks the summary claims before writing the findings page. It does not perform bench actions.

The active acquisition runner takes endpoint names as arguments; none is embedded in its source. A caller must hold the bench lock. Every child command has an explicit timeout; captures end at their requested timeout (status 124), which the action records. Successful actions themselves return 0. No process is detached.

Peer descriptor object names are removed from the retained census. Original bytes remain outside this packet and are identified in redaction.json. Captures remain only under /tmp/a375; no capture, dependency tree, environment, package or large binary belongs in this packet. The build inputs and temporary capture module are represented by sizes and hashes.

The evidence verdict is an operator measurement, not independent review. Publication and independent reviews belong to the coordinator. No push or PR operation is authorized here.
