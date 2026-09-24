[A280]

Closes #113

Author work complete; ready for independent review. REVIEW READY posted on issue #113: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/113#issuecomment-5821803398

- Branch: `113-latency-notify`
- Base: `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`
- Head: `29840136bb2d21bc0fbe92c7c533368f40837ff6`
- Tree: `03bdccaf528aa94098544cf04f5598292fe855c8`
- Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/113#issuecomment-5821292534
- Prior gap: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/111

The registrar compares the previous per-sink latency latch only on a matching registering attribute write. Its new pulse feeds the existing GET_STREAM_INFO per-descriptor pending path alongside the registration and failure pulses from that same edge. Unchanged refreshes are quiet. No processor top-level port changed; its port declaration is byte-identical to the base. The pulse does not re-drive the applicant or ACMP event router.

Milan v1.2 Section 5.4.5.2 and Table 5.22 were checked directly in the specification, printed pages 62–63. The relevant row is quoted in PR-BODY.md. SPEC.md records the source, and provenance.json carries its digest. F06.13, the Section 06 live-event list, SRP latch contract, interface event catalog and compliance implementation row are updated. The compliance coverage marker describes the original document and remains unchanged.

Acceptance evidence:

| Requirement | Result |
|---|---|
| Changed latency gives exactly one response carrying its new value | GI LATENCY-CHANGE and LATENCY-READ; both Advertise and Failed, byte-exact responses |
| Unchanged refresh gives none | GI LATENCY-SAME, both sinks |
| Other sink stays quiet and retains its latency | GI LATENCY-OTHER plus the empty response queue check |
| Removing the trigger fails the first case | Retained latency-trigger-removed: build rc 0, simulation rc 1; all four exact-count checks fail with zero notifications |
| Controls and regression mutants | Golden/restored: 614 checks, zero failures each; 14/14 mutants detected by named checks |
| All processor workflow gates | rc 0; full bank 33 suites / 1,009,045 checks / zero failures; top suite 2,074; lint, portability with memory mapping, docs, traceability and NVM figures pass |
| Default-shape OOC | Both runs rc 0; -6 LUTs, +28 registers; RAM/DSP unchanged |
| Parent control and candidate | Seven commands rc 0 at each pin; 371 consumer checks / zero failures each |

Area: complete processor 28,649 -> 28,643 LUTs and 31,095 -> 31,123 registers. The changed SRP listener adds 73 LUTs and 8 registers. Whole-processor remapping affects the total; no logic saving is attributed to the trigger. Both OOC builds have negative slack at 10 ns, and no routed timing or hardware claim is made. See AREA.md and area-base/area-head reports.

Parent source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`. Original processor pin: `09f9bf3846511f8388d995126502ed92eaa65213`.
Control local parent commit: `9947af735f2228c7780c44ba98eadb368f5efd04` at processor `a8f8ce81`.
Candidate local parent commit: `dd8b228b1c1949b10af3b98aab398265477c0775` at processor `29840136bb2d21bc0fbe92c7c533368f40837ff6`.
Only the gitlink changes. The parent is left clean at the candidate, with the checkout matching its committed pin. No failing commands were observed at either pin. Both builder runs explicitly skip the same historical resource-calibration arm because its placement report is absent; this limitation is recorded in PARENT-COMPARISON.md.

Evidence map:

- PR-BODY.md: prepared PR body, including the normative quotation and complete results.
- processor-gates.json: exact processor commands, return codes and timings; corresponding logs are alongside it.
- parent-comparison.json and PARENT-COMPARISON.md: all fourteen parent invocations, pins and results.
- mutants/results.json and mutants/*.log: builds, named failures and golden/restored controls.
- AREA.md, area-base/, area-head/, ooc-base.json and ooc-head.json: same-recipe default-shape measurement.
- provenance.json: exact commits, tree and HDL hashes; measured HDL still matches the committed source.
- issue-113.json and pr-111.json: public task sources.

All commands ran in the foreground with generous limits; gate invocations were not piped. Source and parent trees are clean. Commits have one-line subjects without bodies or trailers. No push, PR creation/edit, merge, delegation or hardware action was performed. No private transcripts were read. The output packet contains evidence only; build and source scratch directories are outside it.
