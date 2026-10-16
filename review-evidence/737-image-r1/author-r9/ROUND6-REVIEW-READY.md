[A615] REVIEW READY

PR: #738. Relates to #737.
Local commit (not pushed): `6918d4f9bee7081a71f94d9090d01c557085658a` on `737-ci-image`.

Addresses the round-six assignment (class ruling and items 1-4). The walker now refuses every construct it does not resolve with the real tool's exact semantics, and an observed execution audit backs the static inventory. The 45 tool/pin/workflow-provenance records are unchanged.

Changes:
- Item 3: every in-tree Python import is followed through a modelled per-process module search path. Literal `sys.path` insertions, imported path constants and call-argument parameters resolve exactly; an unresolved entry opens the path to every in-tree portion; literal `runpy`/`spec_from_file_location` loaders are followed and a runtime one is a declared capability. No external-import allowance may name a module the checkout supplies. `tb/verilator/nvm_capture_cpu/run.py` is reached and declared.
- Item 1: Make lines are read as GNU Make 4.3 reads them. Non-canonical assignments, `!=`, double-colon and escaped-end forms refuse; an applicable built-in implicit rule refuses the target unless the makefile sets `MAKEFLAGS += -r`; implicit-rule prerequisites bind with make's directory-keeping stems; a target-specific value a command-line name would override refuses; recipes run in make's exact child environment and the traversal cache keys on the complete incoming state. The built-in rules are recorded from the image's own make. A command substitution yields a directory only as `$(cd <literal> && pwd)`, unredirected and non-symlink; any other output is runtime.
- Item 2: a ptrace `execve` audit records the programs each step runs with the network disabled, refusing an unlisted program or an installer. Its controls catch a planted installer and a planted system program by name; the current-tree receipt shows the reached offline steps running only allowlisted programs. The signed-replay interface is documented for the follow-up.
- Item 4: the guide states the verified RV32 adoption form (`--verify-only --destination /opt/rv32-sdk`, the home link for compiler lookup only) with the switch lane's step and contract change named and a receipt.

Validation at the committed head, inside the authenticated image with the network disabled:
- Full docs-check: all 79 commands rc 0, including the Entity shape gate (228 checks, zero failures), the derived protocol-processor source list, the bare-metal scope gate with the new host-inventory mask, and the full `test_builder.py --require-rv32` bank.
- Full rtl-fast: all 36 commands rc 0 (run as uid 1000 so the custody-oracle self-tests that refuse under root run as intended), including the whole-tree Verilator lint ratchet, the three-top yosys elaboration with its OOC/guard/cache self-tests, the publication census, the firmware unit suites and RV32 builds, the control/AECP/SRP mutation campaigns, the coverage ratchet and the TSN stack boundary.
- Every round-four and round-five fixture and the new planted controls refuse by name; the inventory self-tests, the new exact-semantics self-test, the idiom gate and all source/documentation gates return rc 0.
- Two sequential cold builds produce recipe `54cd38dea89d143d3c4ba40e72971be5de3b16592652658659e670f230ad7a29`, the unchanged image `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c` and byte-identical archives; only the lock's recipe identity changed. One export authenticated at `--record-lock`, the other at `--check-lock --verify-archive`.

Limitations: the full builder command returns zero but reports two NOT RUN arms (the inert `MAKEFLAGS += -e` mutation on this Make version and calibration against the unavailable `mf48` report); neither is claimed as covered. Runtime-assembled behavior remains located residue. This is local evidence, not hosted CI or a review verdict.

HANDOFF.md and PR-BODY.md have Round 6 sections with the change map, evidence, receipts and limitations. The worktree is clean; all seven round-six commits remain local. No push, registry login or push, PR modification, publication, merge, product behavior change or product-test assertion change occurred. Independent re-review and the reviewer-owned coverage ledger are required.
