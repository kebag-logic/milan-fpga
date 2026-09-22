[A174] REVIEW READY

Local unpublished commit: `28e350b99ac240a750326b762c6d029f0653362c` (tree `d17c117db03128e444b7b44742fe82f10746cb28`), clean source on the assigned branch.

Changed: schema 2 binds the exact three generated ROM names/bytes after existing generation/nonempty checks, using one digest for lookup/store, every selected top, both modes and both cache tiers. Cache-contract docs and defect-sensitive controls updated. Inventory remains byte-identical at 54 tops; no product/generator/pin/workflow/ratchet changes.

Validation on this head: `python3 syn/yosys/result_cache.py --selftest`; `python3 syn/yosys/cache_selftest.py --logs <evidence-dir>`; 25/25 focused contract/docs/idiom/evidence commands passed. The live bank preserves all five original arms and adds 54 driver invocations covering all images, modes, selected tops, generation refusals and legacy/invalid records.

Real `KL_pp_shadow`, Yosys 0.66 / sv2v v0.0.13: cold 1141365 cells; identical warm and read-only seed both hit 1141365. The public changed-ROM payload now misses and runs live at 1122602; changed warm hits 1122602; uncached changed input also reports 1122602. All six runs exit 0. Retained staged inputs are byte-identical; only ucode.hex and the ROM digest change. Lookup/store identity equality and raw stat counts were checked. This confirms corrected stale numeric evidence, not a claimed cold failure.

Acceptance: criteria 1-4 have passing focused evidence. Criterion 5's author checks pass; complete parent/PP/gPTP/Yosys/builder banks, trusted act/hosted evidence, R247/R248 reviews and five-lens ledger, candidate validation, authorized merge and containment remain manager-owned and pending. Raw logs, portable probes, command/head/tree/exit/tool/cell receipts, HANDOFF.md and PR-BODY.md are in the assigned local management handoff for publication. Preliminary measurements are explicitly separated. No selfapproval or full-bar completion claim.
