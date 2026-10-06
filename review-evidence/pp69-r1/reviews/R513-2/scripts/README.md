R513-2 reproduction

Run from any directory, providing a clean repository at the exact reviewed head and an output packet directory. The packet directory must contain these scripts. The supplied pinned simulator defaults to `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`; `REVIEW_VERILATOR` may name an equivalent verified 5.050 executable elsewhere.

```
python3 scripts/run_focused.py SOURCE_REPOSITORY PACKET_DIRECTORY
python3 scripts/run_docs_guards.py SOURCE_REPOSITORY PACKET_DIRECTORY
python3 scripts/run_capacity_probe.py SOURCE_REPOSITORY PACKET_DIRECTORY
python3 scripts/plant_audit.py SOURCE_REPOSITORY PACKET_DIRECTORY
python3 scripts/verify_checkout.py SOURCE_REPOSITORY PACKET_DIRECTORY
```

The first coordinator runs the ADP and notification suites, the twelve round-2 controls, and the documentation gate concurrently. Each campaign has explicit `--jobs 3`; make has `-j16`; the simulator wrapper limits each native build to three workers. Maximum native-build fanout is fifteen. Each child is waited by its foreground coordinator. No shell background job or detached notification waiter is needed. The first invocation used an archive without Git metadata: the doc gate could not enumerate tracked files. The script now supplies local Git metadata; `docs-check-metadata.log` is the successful rerun. The original failed receipt is retained, without treating it as a source failure.

The capacity probe copies unchanged implementation files into scratch, changes only the disposable testbench and its controller-depth fixture, and substitutes `capacity_probe.cpp.inc` for the testbench entry point. It registers sixteen controllers on each port, checks both exhaustion boundaries, and independently exercises monitor response, monitor failure, replacement, and TIME_LIMITED routing for every one of the 32 rows. It is a module-boundary test: the shared services are modeled. The six-check top-level golden in the mutation campaign is the integrated IF test.

`plant_audit.py` checks all 77 notification controls and the three refreshed patch contexts without simulating the old controls. It is not a full processor campaign. `verify_checkout.py` compares each tracked blob and mode, every index entry, HEAD/tree identity, detached state and all gitlinks directly. The reviewed processor tree has no gitlinks.

No implementation changes, commits, remote writes, full banks or hardware runs are performed. All disposable trees, builds, generated images and temporary directories stay under `scratch/`. Only REPORT.md and files listed in MANIFEST.sha256 are designated for publication.
