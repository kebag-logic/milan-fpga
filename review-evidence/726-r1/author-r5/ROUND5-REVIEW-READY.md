[A605] REVIEW READY

Round 5 head: `e7d604faa0472d505d6459883b382c2b237ad06d`.
New local commits: `6f8efde7e5fa95be2659c8aafc1806a7e5f4c163` and `e7d604faa0472d505d6459883b382c2b237ad06d`. No push.

R629-4-F01: IV8 no longer includes FRX among interval anomalies. It now states: “FRAMES_RX counts each accepted AVTPDU; its total may be published in a batch.” The six-packet burst still adds six; SM/TU/UF/MR and late/early bursts still add one. Assertions and stimulus are unchanged.

R628-4-R1: the proposed PR body contains the exact hosted-status replacement and removes both specified stale statements, explicitly attributing the success to the Round 4 head. R628-4-R2: the suite README documents the four temporary counters elaborations and links their measurement document. The remote PR was not edited.

Validation, all rc 0: complete receive regression (97 single-sink, 119 NxN, 36 checks at each lockstep shape), its clean control and four named mutant detections, packet-law behavior contract (88 scenarios / 276 steps), C++ idiom, processor/SoC/RTL source-list gates, all five required documentation gates, and whitespace checks. The committed-range em-dash check passes. Build outputs stayed in disk scratch; peak sampled memory was 1,112,285,184 bytes with no OOM events.

No production RTL, firmware implementation, configuration or submodule changed. Ten prior measurement input hashes match; measured image code remains identical. Retained area: 49,427 LUT (+35 against 49,392), 53,378 FF, 87.5 BRAM; constrained WNS/WHS +0.451/+0.036 ns. No image or capture remeasurement was triggered and no STOP condition arose.

HANDOFF.md and PR-BODY.md include Round 5, the emitted IV8 text, exact gate receipts, unchanged-input evidence, retained per-descriptor before/after cadence, mutation/omission provenance and the area table. ROUND5-GATES.tsv and ROUND5-ARTIFACTS.tsv record results, sizes and hashes. Worktree and initialized dependencies are clean. No bench, push, PR action, rebase, amend, merge or existing-comment edit occurred.

Independent re-review, authorized publication and new-head hosted acceptance, current-dev candidate validation and merge-turn physical/reference-peer/controller checks remain required. The proposed PR body retains Relates to #726.
