[A174] Bind generated ROM bytes to Yosys cache evidence

Closes #520

## Status

Local implementation commit: `28e350b99ac240a750326b762c6d029f0653362c`.
Draft for manager publication. Full validation and independent review remain pending.

## Description

A successful ROM regeneration could leave the cached cell count stale because staged sv2v, program and tool identities stayed unchanged. Schema 2 adds the exact generated `ltn_rom.hex`, `ucode.hex` and `gptp_ucode.hex` names and bytes to one deterministic digest after generation and existing nonempty checks. Every top and both modes use that digest for lookup/store in per-head state and read-only seeds. Old-schema evidence runs live.

The synthesis program, stat-json extraction, structural checks, cache trust/scoping and 54-top inventory remain unchanged. Processor code, generators, pins, workflows and ratchets are unchanged.

## How to reproduce

Run the real gate on `KL_pp_shadow` with a fresh per-head cache, then repeat to verify a hit. Change only generated nonempty `ucode.hex` bytes to the public issue's `INVALID_ROM_DATA\n` payload, retaining staged sv2v/program/tool identities. The former hit must run live; compare its cells with an uncached run of the same generated input. The manager handoff includes a portable probe that performs this without editing generator sources and retains the raw tool evidence.

## How to validate

Run `python3 syn/yosys/result_cache.py --selftest` and `python3 syn/yosys/cache_selftest.py --logs <evidence-dir>`. The latter preserves original controls and exercises all image identities, both modes, multiple selected tops, writable state/read-only seed, generation failures and invalid/old records through the real driver. Run the documented full local, trusted act and hosted candidate gates before review completion and merge.

Exact-head author test results belong in the evidence comment. The local handoff contains command/exit/tool/tree/cell receipts and raw logs; it is not independent review.

## DoD

- [x] Conservative generated three-image bundle and schema advance.
- [x] Existing cache/gate contracts preserved; authoritative docs updated.
- [x] Focused unit, real-gate integration, contract/docs/idiom/evidence checks.
- [ ] Complete native banks and required local/act/hosted evidence, owned by manager.
- [ ] R247/R248 independent positives and clean five-lens ledger.
- [ ] Authorized merge, candidate validation, containment and Closed/Done.
