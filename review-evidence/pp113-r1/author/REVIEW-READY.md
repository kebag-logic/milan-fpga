[A280] REVIEW READY

Head: `29840136bb2d21bc0fbe92c7c533368f40837ff6` on `113-latency-notify`, based on `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`.

A committed per-sink latency change now feeds the existing GET_STREAM_INFO notify path. Unchanged refreshes stay quiet; unrelated sinks are not notified. Processor top-level ports are unchanged. Milan v1.2 Section 5.4.5.2 / Table 5.22 was checked directly, and the relevant row is quoted in the prepared PR body. F06.13, the live-event list and compliance row are updated.

Local processor gates all rc 0: full bank 33 suites / 1,009,045 checks / zero failures; processor top 2,074; focused response suite 614; lint, portability, documentation, traceability and NVM figures pass. All 14 retained mutants are detected, including the removed latency trigger failing the named exact-count check. Golden and restored controls pass.

Default-shape complete-processor OOC: 28,649 -> 28,643 LUTs (-6), 31,095 -> 31,123 registers (+28), RAM/DSP unchanged. The changed SRP listener itself adds 73 LUTs / 8 registers; the total includes remapping of unchanged modules. Both builds retain negative OOC slack; no routed timing or hardware claim.

Parent consumer checks used dev `573f0052a0e4412e81f0845438fcec2086ce5d55` with locally committed gitlinks: control `9947af735f2228c7780c44ba98eadb368f5efd04` at processor `a8f8ce81`, candidate `dd8b228b1c1949b10af3b98aab398265477c0775` at this head. All seven commands return rc 0 at both pins, and both consumer runs pass 371 checks with zero failures. The same four front-end ratchet findings are retained. There is no failing command attributable to either the old pin gap or this change. Both builder runs explicitly leave one historical resource-calibration arm unrun because its reference placement report is absent; this shared limitation is recorded, not counted as hardware evidence. The parent remains clean at the local candidate commit; nothing was pushed.

HANDOFF.md, PR-BODY.md, command/return-code receipts, mutant logs and OOC reports are in the assigned evidence packet. Processor and parent commits remain local; no push, PR write, merge or hardware action was performed.
