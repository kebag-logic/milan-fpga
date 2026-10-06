[R500] POSITIVE - exact head fa1294279c42f181b6f43c6e6bd812039798705c

Independent composition assessment recorded before reading any prior review report.
The subsequent public-findings reconciliation belongs in REPORT.md.

The candidate is the exact ordered merge of 9e05246c5455b2a1df26038345709437e13c6f18 and d763fce6f3e48fa9c468aaa835653befb8382d06. The first parent's tree equals live dev a1e9839e909c2e44fd47307588fbf9da8c28fd53. From common ancestor 28f9666feab2b2ba287643c63ed3a16b1e0bb863, the sole shared path is docs/README.md. The candidate preserves the exact parent bytes after removing the other parent's one inserted row. Both links resolve. All 29 other F1 paths and 87 other F0 paths retain their owning source's mode, kind and object ID.

F1 contributes no production build registration, workflow edit, RTL, gitlink, mailbox hook or SoC edit. Its flash port and state port remain separate from F0. The F0 SoC addition is default-off and does not change the flash map, NVM derivation or timer ownership. The global documentation, record, workflow and inventory gates all pass on this candidate; see gate-results.json and the individual raw logs. No new blocking composition defect was found.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQUIREMENTS.md:21; frozen F1 scope comment 5993775541; docs/design/SAVED_STATE_FASTCONNECT.md:763; composition.json proves that the composition leaves the F1 contracts unchanged | R500-4 and R501-4 source coverage; R500-5 composition boundary | Source d763fce6f3e48fa9c468aaa835653befb8382d06; candidate fa1294279c42f181b6f43c6e6bd812039798705c |
| RTL | CLEAN | candidate.diff; sw/litex/milan_soc.py:2475; sw/firmware/ctrl/mbx/mbx_hal.h; sw/firmware/ctrl_nvm/nvm_flash.h; no shared production implementation, source-list change or gitlink change from F1 | R500-4 and R501-4 source coverage; R500-5 composition boundary | Source d763fce6f3e48fa9c468aaa835653befb8382d06; candidate fa1294279c42f181b6f43c6e6bd812039798705c |
| Robustness | CLEAN | sw/firmware/ctrl_nvm/nvm_store.c and plat/nvm_flash_litespi.c retain exact reviewed blobs; sw/firmware/ctrl/loop/ctrl_loop.c has no F1 invocation; no new common runtime path | R500-4 and R501-4 source coverage; R500-5 composition boundary | Source d763fce6f3e48fa9c468aaa835653befb8382d06; candidate fa1294279c42f181b6f43c6e6bd812039798705c |
| Tests | CLEAN | scripts/ci_scope.py, scripts/ci_events.py, docs/traceability/gen_module_matrix.py; sw/firmware/ctrl_nvm/test/nvm_bench.py; gate-results.json; unchanged source tests plus passing shared inventory and record checks | R500-5 shared gate composition; R500-4 and R501-4 source tests | Candidate fa1294279c42f181b6f43c6e6bd812039798705c; source d763fce6f3e48fa9c468aaa835653befb8382d06 |
| Docs | CLEAN | docs/README.md:73-77; docs/design/MAILBOX_SPLIT.md; sw/firmware/ctrl_nvm/README.md; docs.log, toc.log, anchors.log, em-dash.log, doc-paths.log | R500-5 composition; R500-4 and R501-4 unchanged source prose | Candidate fa1294279c42f181b6f43c6e6bd812039798705c; source d763fce6f3e48fa9c468aaa835653befb8382d06 |

R500-5-F1, RESIDUE, Docs: sw/firmware/ctrl_nvm/README.md:116 describes F0's HAL as "on its own lane, not merged". Both parents are present in this candidate. Remove the exact substring " on its own\nlane, not merged" from the parenthetical, keeping the path and interface description unchanged. This only corrects a stale merge-status aside; it changes no implementation, measurement, test, conformance or clause claim. Verify the sentence's parenthetical contains the path alone and documentation gates remain clean. The manager carries this exact wording fix to the residue checklist.

Limits: composition acceptance only; source review names and verdicts are supplied by the public assignment and will be reconciled next. Full banks, hosted acceptance and physical calibration are not independently executed here.
