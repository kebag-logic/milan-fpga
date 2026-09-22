[A179] REVIEW READY - completed policy correction only

Local unpublished commit: `5874895eb817ed41c0f8be4eb427ad3315c29844`; tree `45a2a9b2b108a932db49d9ec595ff4b3f18a2b3e`. One one-line correction commit; source clean. Only `scripts/check_baremetal_only.py` changed.

Implemented the [bounded host-tool decision](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5781783857): five file/context-pinned token masks, with literal clean fixtures and wrong-file, unrelated same-file, extra same-line, protected-document and boundary refusals. Existing policy/control AST remains identical outside these additions.

Validation: `rtk proxy python3 scripts/check_baremetal_only.py --check` returns 0 (0 findings / 827 files); `--selftest` returns 0 (601 arms). Ten disposable removed/broadened-mask probes are rejected. Runner 17/17, phase 24/24, tally/ownership, Python idiom, docs, hygiene, evidence, fail-fast, TODO, whitespace and em-dash checks pass. Complete parent/required-submodule bytes, modes and indices match; all 13 ratchets and all five benchmarked artifact bytes are unchanged. Original benchmarks remain attributed to `7ab1c8d0ad073fbc1977c455dea89b7b318d4e52`.

The original exit-1/21-finding log is reproduced byte for byte and preserved. A preliminary boundary probe exposed a draft prefix-mask hole; its exit-2 receipt is preserved and the final regression passes. Factual HANDOFF.md, scripts, raw argv/exits/logs, integrity proofs and manifest are in the designated `517-policy-author` evidence directory.

Pending, explicitly: full fresh manager parent/PP/gPTP/Yosys/builder banks, trusted act, exact-head hosted evidence and timing comparison, independent R245 internal Codex / R246 external Opus reviews, final current-dev candidate and containment. Original manager banks remain partial, not PASS. This handoff claims the bounded correction only, not full #517 acceptance, a review verdict or merge approval. No source push, PR, merge or additional agent; stopping at this local head.
