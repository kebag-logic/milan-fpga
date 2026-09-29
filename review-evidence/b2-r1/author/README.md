# [A440] Bench lane B2 packet (private)

Refs #606, #608, #75. HANDOFF.md gives the state, the step ledger, one row per bind and per cycle, deviations and open questions.

Reproduce an analysis: `python3 -B tools/b2_analyze.py cycles/cycle-022` (reads the raw capture from /tmp/b2-a440/raw).
Summary and page tables: `tools/b2_summary.py`, then `tools/b2_pages.py`, then `tools/b2_assemble.py <lane worktree>`.
The acquisition tools read their endpoints from a private file named by B2_ENDPOINTS, which is not in this packet.
Interface, module and home-path strings were masked after acquisition; raw captures are unmodified and indexed in RAW-ARTIFACTS.json.
Verify the packet: `sha256sum -c MANIFEST.sha256`.
