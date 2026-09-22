[A182]

## Status

Source ready for independent review at `b5ce20eca8b59709ec5bc6115e5e15bfc312f283`. Manager full banks, hosted checks, current-dev composition and R256/R257 reviews remain pending.

## Description

An interrupted gPTP shadow mutation campaign could leave tracked RTL mutated, and a cancelled sweep could start later suites. Mutations now use verified private source/build copies, including required pinned dependency sources. The sweep latches INT/TERM, stops and reaps owned descendants, preserves attributable partial logs and exits 130/143 without a completed summary.

The nine mutation definitions, six unobservable reasons, named-check/fallback rules, suite populations, deadlines, ordinary failure continuation, masked-verdict refusal, timeout UNKNOWN, locks and shards remain. No product RTL, firmware, processor pin or ordinary pool file changes.

Closes #523

## How to reproduce

The lifecycle and sweep tests execute production drivers at explicit command handshakes. Their unsafe controls reproduce caller-source residue and next-suite continuation in disposable fixtures.

## How to validate

```sh
python3 tb/verilator/gptp_shadow/test_mutant_lifecycle.py
python3 scripts/test_suite_cancellation.py
VERILATOR_JOBS=8 make -C tb/verilator/gptp_shadow
```

Use verified Verilator 5.050. Author result: 309/309 baseline checks, nine mutation detections, six unchanged notes, and all focused idiom/docs/evidence/fail-fast/bare-metal controls passed. Exact receipts belong in the manager's PR evidence comment.

## Definition of done

Author implementation and scoped evidence are complete. Required full local/hosted gates, two independent positive reviews with clean lens coverage, final current-dev candidate validation, maintainer-authorized merge and containment remain mandatory.
