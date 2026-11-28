Status: STOP evidence packet. The completed qualification fails the frozen held-egress ledger; no bound was relaxed. The final local commit and input identities are in [final-head.json](final-head.json).

## Decision and complete qualification

- [DERIVATION.md](DERIVATION.md): every measured cost, all candidate rows, and all seven frozen held-egress rows.
- [final-coverage.json](final-coverage.json): all 159 cases and eight images present in the cost census, exact prior-input hashes, and the unchanged rule-selected row.
- [census/qualification.json](census/qualification.json): full 159-case qualification, per-check verdicts, findings, owner model, longest pass and #969 disposition.
- [census/derived-model.json](census/derived-model.json), [census/merged-census.json](census/merged-census.json), [census/census.json](census/census.json): unchanged-rule derivation and its measured inputs.
- [baseline-row-census.json](baseline-row-census.json), [baseline-row-input.json](baseline-row-input.json): exact dependency maxima supplied to the unchanged merge-and-derive rule.
- [census/egress-100.log](census/egress-100.log): exact-departure replay of every trace, all eight stream phases, gPTP burst, margin, fixed path and separate handshake.
- [census/egress-ledger.log](census/egress-ledger.log), [held-egress-finding.json](held-egress-finding.json): the 62.03635 ms AECP result against the frozen 61.99 ms allowance.
- [census/qualification-commands.json](census/qualification-commands.json), [qualification-run.log](qualification-run.log): exact qualification commands and return codes. Nonzero service results are retained as failures.
- [replay-summary.json](replay-summary.json), [replay.json](replay.json), [replay.log](replay.log): all 159 original cases replayed before the fresh census; changed free-space outcomes refuse evidence carry.

## Full native evidence and reproduction

- [census/ARCHIVE.json](census/ARCHIVE.json): all 159 complete traces, losslessly compressed, with raw and compressed SHA-256 values. These are full traces, not selected extracts. Each image's `results/` also contains its stimulus, native status, grade and journals.
- [census/manifest.json](census/manifest.json), [census/completed.json](census/completed.json), [census/findings.json](census/findings.json): complete case coverage and all findings.
- [census-build-identity.json](census-build-identity.json): all eight native builds checked against the unchanged dependency sources and current pins before relinking the additive queue model.
- [census-join.json](census-join.json), [census-partition.json](census-partition.json): disjoint 37/122-case partitions, 159/159 original stimulus identities, exact trace hashes, and joined findings. Partitioning changes only execution scheduling.
- [join-recovery.json](join-recovery.json): a cross-filesystem receipt rename failed after result moves; all 159 traces and stimuli were reverified before completing the boundary receipt. No trace was altered.
- [egress-cases/](egress-cases/): one replay receipt per trace, bound to raw trace SHA-256, grader source hashes and exact parameters. The final verifier checks every binding and computes the verdict; it does not reuse unbound results.
- [source/prepare-census.py](source/prepare-census.py), [source/run-census.py](source/run-census.py), [source/qualify-census.py](source/qualify-census.py): actual build, execution and qualification recipes. The copied cost/derivation helpers retain the dependency method and #969 disposition.
- [rule-recipe-identity.json](rule-recipe-identity.json): byte identity of all six cost, event, merge, derivation and install helpers to the dependency packet. No cost rule was edited.
- [source/collect-egress.py](source/collect-egress.py), [source/join-census.py](source/join-census.py), [source/archive-census.py](source/archive-census.py), [source/tables.py](source/tables.py): replay collection, coverage verification, lossless archiving and display-only table generation.
- To independently repeat replay, decompress each `census/<image>/results/*.log.gz` to a separate results directory, verify its raw digest against `ARCHIVE.json`, and invoke `tb/verilator/usbnet/egress_grade.py` on all eight image directories at the recorded commit and pins. The repository grader reparses each complete trace and checks exact departures.
- [source/parallel-regrade.py](source/parallel-regrade.py), [pre-parallel-grade-hashes.json](pre-parallel-grade-hashes.json), [parallel-grade-identity.json](parallel-grade-identity.json), [regrade-scheduling.json](regrade-scheduling.json): independent calls to the unchanged per-group grader, with byte identity required against all 159 existing native grades. Later cross-group checks remain in the unchanged command. Serial partial regrades are retained in [sequential-regrade/](sequential-regrade/).
- [census.log](census.log), [census-supplemental.log](census-supplemental.log), [native-slots.jsonl](native-slots.jsonl), [cpu-placement.json](cpu-placement.json): foreground execution and CPU placement. Native models advance explicit simulated clocks; host scheduling does not change stimulus time. Every paused native child was resumed.

## Identity and dependency

- [final-head.json](final-head.json), [round7.patch](round7.patch), [local-history.txt](local-history.txt): final local head, merge ancestry, exact dependency identities and unchanged measured inputs. No push or posting occurred.
- [merge.json](merge.json): initial merge record; its inventory difference was subsequently resolved in favor of exact dependency bytes.
- [dependency-identity.json](dependency-identity.json): final byte identity of all fourteen files changed by the requested dependency commit.
- [firmware-identity.json](firmware-identity.json), [firmware-commands.json](firmware-commands.json), [firmware/](firmware/): six fresh same-pin builds and the actual Arty / ALINX 1x1 / ALINX 8x8 ELF and map-header artifacts.
- [fresh-map-commands.json](fresh-map-commands.json), [fresh-map-identity.json](fresh-map-identity.json), [current-control-map-identity.json](current-control-map-identity.json), [current-maps/](current-maps/): fresh current-head Arty map generation on both sides, matching the firmware build inputs. [fresh-candidate-csr.diff](fresh-candidate-csr.diff) records only a timestamp difference. This is map generation, not route evidence.
- [rulings.json](rulings.json): public decision text used for this round.

## Tests and planted defects

- [usbnet-commands.json](usbnet-commands.json), [usbnet.log](usbnet.log): 92,755 passing USB/LED checks plus four real SET_CLOCK_SOURCE cases; includes the 81-check local RX/mailbox wait proof.
- [plants-commands.json](plants-commands.json), [plants.log](plants.log), [plants/](plants/): all 72 existing named USB/LED planted defects and individual outputs.
- [handshake-controls-named.log](handshake-controls-named.log): 512 shipping MII length/phase cases, maximum 257.5 ns, stated 260 ns; both real RTL plants caught by their named checks.
- [shipping-chain-files.json](shipping-chain-files.json), [shipping-chain/](shipping-chain/): all raw handshake cases, generated production-chain RTL, exact source/pin bindings, build commands and both planted sources/outputs; also the inherited fixed-path run.
- [injection-controls-complete.log](injection-controls-complete.log): final 18 controls, comprising nine clean controls and nine caught plants. Includes missing injection with a forged queue declaration, wrong busy-period behavior, false FIFO occupation, omitted handshake, failed ring-space carry and relaxed exact-departure agreement.
- [base-egress-fixed.log](base-egress-fixed.log), [base-egress-selftest.log](base-egress-selftest.log): inherited shipping fixed path (448 cases; 312.5 ns maximum, stated 320 ns) and 17 grader controls.
- [shaper-commands.json](shaper-commands.json), [shaper-cbs.log](shaper-cbs.log), [shaper-shaper_core.log](shaper-shaper_core.log), [shaper-queues.log](shaper-queues.log): existing CBS, shaper and queue regressions.

## Repository gates and retained failures

- [gates.json](gates.json): eight focused code, naming, hygiene, port-contract and evidence gates pass. [control-style-final.log](control-style-final.log) checks the final control additions.
- [final-documentation-gates.json](final-documentation-gates.json): final documentation, contents, anchor, path, naming, evidence and whitespace checks after the result was documented. Inventory freshness is the expected retained failure.
- [inventory-decision.json](inventory-decision.json), [inventory-exact-dependency.log](inventory-exact-dependency.log), [inventory-before-exact-dependency.md](inventory-before-exact-dependency.md): exact dependency inventory versus the two USB pages it omits. No permission to change dependency bytes was assumed.
- [doc-gates.json](doc-gates.json), [markdown-gates.json](markdown-gates.json): initial environment refusals and subsequent checks in the pinned Markdown environment. Only the successful final checks are counted as passes.
- `initial-*`, `provisional-*`, earlier handshake/control logs, and [injection-controls-nested-plant-refusal.log](injection-controls-nested-plant-refusal.log) preserve setup mistakes and exploratory runs. They are not promoted to final evidence. The provisional replay used an exploratory handshake; the final input is the measured 260 ns term.

## Resource and archive integrity

- [resources-final.json](resources-final.json): final unit weight, CPU affinity, scratch use, free space and absence of live or paused census processes.
- [obsolete-native-cleanup.json](obsolete-native-cleanup.json): obsolete initial native directories archived and logged before deletion; [initial-native-archives/](initial-native-archives/) retains their contents. Every removal used the required prelogged absolute paths.
- [MANIFEST.sha256](MANIFEST.sha256): final receipt file hashes, excluding the manifest itself. The final packet does not claim independent approval, hosted CI success, physical route completion or issue closure.
