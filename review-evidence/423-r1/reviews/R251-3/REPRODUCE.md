R251-3 factual reproduction packet for exact source 4671e582cfa4bba4809b9e3a354ce5b6eb967f99.

Use a detached, populated checkout of that source. Its Git objects must include b911c11671cae329a99f5e413133b4bf6357fa7f and source base 52711029f374650dc93830d5ea28e81cb5c8f410. Python 3, Git with patch-id --verbatim, RTK, and locale/localedef data for en_US ISO-8859-1 are needed. The probes use disposable locale data and do not install locales. No Verilator, hardware, Docker or act is needed.

Run from this packet directory. Replace CHECKOUT and OUT below with absolute paths; OUT must be a new, empty output directory with an existing parent. These are argument placeholders, not environment-variable assignments. Keep commands sequential; each driver uses at most two workers. Every shell invocation starts with RTK. Raw Git byte-argument oracles inside Python deliberately bypass text CLI proxies.

```sh
rtk proxy python3 -B scripts/verify_integrity.py CHECKOUT OUT-initial-integrity.json
rtk proxy python3 -B scripts/prove_identity.py CHECKOUT OUT-object-identity.json
rtk proxy python3 -B scripts/check_parent_locale.py CHECKOUT OUT/parent-locales
rtk proxy python3 -B scripts/transport_probe.py CHECKOUT OUT/transport
rtk proxy python3 -B scripts/run_public_examples.py CHECKOUT OUT/public-examples
rtk proxy python3 -B scripts/run_restorations.py CHECKOUT OUT/restorations
rtk proxy python3 -B scripts/unavailable_locale.py CHECKOUT OUT/unavailable-locale
rtk proxy python3 -B CHECKOUT/scripts/check_py_idiom.py
rtk proxy git -C CHECKOUT diff --check 52711029f374650dc93830d5ea28e81cb5c8f410 4671e582cfa4bba4809b9e3a354ce5b6eb967f99
rtk proxy python3 -B scripts/verify_integrity.py CHECKOUT OUT-final-integrity.json
```

All drivers exit 0 when their expected comparison succeeds. check_parent_locale runs both focused22 and full455 controls under measured UTF-8 and Latin-1 parents, against production and an exact b911 assertion restoration. Only the restored Latin-1 subprocess is expected to exit 1 (21/22 and 454/455); production passes both. Restoration-driver exit 0 means four mutated children were detected, each exiting 1, not that the mutated sources passed. Unavailable-locale exit 0 means the NOT RUN behavior was verified, not that Latin-1 ran in that restricted process.

transport_probe.py and run_restorations.py are byte-identical to the downloaded public R251-2 scripts. run_public_examples.py adapts the same original fixture's source selector and displayed head label, preserving its histories and base. The new parent-locale driver restores the exact b911 blob, captures both full defaults, and records raw tree bytes and all focused comparisons. Script hashes and adaptations are under raw/script-provenance.json and raw/*.adaptation.diff. Original public scripts and the fixture remain under public/.

The receipt wrapper used in this execution captures raw stdout/stderr, argv, cwd, timing and expected/actual exits:

```sh
rtk proxy python3 -B scripts/receipt.py --output OUT/example-run --cwd CHECKOUT -- python3 -B /absolute/packet/scripts/transport_probe.py CHECKOUT OUT/example-transport
```

The current immutable public archive and selection are recorded in raw/evidence-tree.stdout and scripts/download_evidence.py. To verify or re-download selected public blob bytes, use this packet's absolute path:

```sh
rtk proxy python3 -B scripts/download_evidence.py /absolute/packet
rtk proxy python3 -B scripts/assess_evidence.py CHECKOUT /absolute/packet
```

The latter reads existing receipts and stored donor Git objects. It does not rerun the historical 31-case matrix or any full native bank. It verifies the source/base-bound manager result inventories, exact historical commit/raw-patch identity, current original145/all455 assertion preservation, production-output equality across F3 restoration and precise restoration failures. A fresh probe run can be assessed by supplying the same packet layout, with its public/ directory and the newly produced raw/parent-locales, raw/restorations and raw/object-identity.json.

The initial evidence-assessment helper failed on a valid empty whitespace-check log; its source and raw failed receipts are retained. The corrected helper accepts an existing empty log when its recorded command exit is 0. No failing source result was discarded.

The report distinguishes R251-3 execution from accepted R251-2 evidence and inspected manager execution. No command above starts a full native/builder bank, contacts an author, mutates source, publishes, inspects Actions, or invokes candidate orchestration.
