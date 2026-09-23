[A189]

## Status

Correction round for the R256-2 and R257-1 findings, both NEGATIVE at `b5ce20ec`. Source `6674c278a8db5f0886d036dceff02d33b7ca6a37`, tree `8d634f12cb83c2ca9ccdb7a4b5e7dde9b19a6245`, descends from live dev `776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d` (conflict-free merge). Author focused gates pass. Re-review by R256 and R257, trusted act, hosted checks and the current-dev candidate remain pending.

## Description

An interrupted gPTP shadow mutation campaign could leave tracked RTL mutated, and a cancelled sweep could start later suites. Mutations now use verified private copies of exactly the files the build reads (`make print-inputs` plus local C++ includes), including the pinned gPTP and axis inputs. The sweep latches INT/TERM, stops and reaps owned descendants, keeps attributable partial logs and exits 130/143 without a completed summary.

Every command the owner launches now dies with its owner. A hard stop (KILL, or HUP to the entry or its group) therefore kills the sweep shell: no later suite, no summary; a suite already running may finish. Git variables that redirect the checkout (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_INDEX_FILE`, object stores, replace refs, configuration injection) are refused by name; every other Git variable is accepted and removed from the identity commands. Only Git's standard output is parsed, an unreadable record is a refusal, and a missing process facility is a `REFUSED:` exit 2 at both entry points. CONTRIBUTING now prescribes initialised pinned submodules instead of a copied `third_party/`.

The nine mutation definitions, six unobservable reasons, named-check/fallback rules, suite populations, deadlines, ordinary failure continuation, masked-verdict refusal, timeout UNKNOWN, locks, shards and the host-process masks remain. No product RTL, firmware, processor pin, ratchet or ordinary pool file changes.

Closes #523

## How to reproduce

The lifecycle and sweep tests execute production drivers at explicit command handshakes. Their unsafe controls reproduce caller-source residue, next-suite continuation and a detached sweep after a hard stop in disposable fixtures.

## How to validate

```sh
python3 tb/verilator/gptp_shadow/test_mutant_lifecycle.py
python3 scripts/test_suite_cancellation.py
VERILATOR_JOBS=8 make -C tb/verilator/gptp_shadow
```

Use verified Verilator 5.050. Author result at this head: 309/309 baseline checks, nine mutation detections, six unchanged notes, in a shell exporting ordinary Git settings; all focused idiom/docs/evidence/fail-fast/bare-metal gates pass. Exact receipts belong in the manager's PR evidence comment.

## Definition of done

Author implementation and scoped evidence are complete. Required trusted act and hosted gates, two independent positive reviews with clean lens coverage, final current-dev candidate validation, maintainer-authorized merge and containment remain mandatory.
