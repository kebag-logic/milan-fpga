# The round-two reviewers' probes, rerun against revision c

Both round-two reviews of PR #503 published their fault-injection probes in
the review archive, commit `7d9da8773c8baec0f705b08cea8b9e04d8c00b27`,
`review-evidence/503-round2/`. This directory reruns them against the
revision-c evidence, in adapted copies, and grades the outcome against the
behaviour each reviewer demanded.

## The adaptations

The archive's README says the scripts carry explicit checkout and scratch
paths, to be adapted in copies. Each copy states its adaptations in its
docstring; in short:

| Copy | Original (sha256) | Adapted |
|---|---|---|
| `r217_probes.py` | `R217/probes.py` (`94de822b...52b`) | paths from `PROBE_OUT` and `EVIDENCE`; the reviewer's bridge seam (the first descriptor request accepted after an application answers 5,000 cycles late) is now the evidence's own knob `desc_delay_after_apply`, with the same trigger |
| `r218_probe_headers.py` | `R218/probe_headers.py` (`d713e83d...ad9`) | paths from `PROBE_OUT` and `EVIDENCE`; V18's anchor carries its comment line, because the line it patched now also occurs in H2 and H2b; the V1a slots come from a seed run of the probe's own build; the two original-trigger results also record their terminal defaults mismatches |

Every stimulus, variant and grading call is otherwise the reviewer's.

## Grading

The reviewers' checkers assert the round-two COUNTEREXAMPLES. The
counterexamples are what revision c removes, so `r217_check.py` and
`r218_check.py` assert what each reviewer demanded instead: a header
transport error in either pass or both ends with a failure verdict and
complete defaults, never blank; a descriptor fault after an application
rolls back to proven defaults, or ends CLOSED while the memory still fails;
an image that cannot be proven at the start ends CLOSED; the original
payload and timeout triggers keep rolling back.

## Rerun

From this directory, with the three submodules initialised and the tools
the evidence README names:

    export PROBE_OUT=/path/to/empty/scratch
    python3 -B r217_probes.py && python3 -B r217_check.py
    python3 -B r218_probe_headers.py && python3 -B r218_check.py

Each checker exits 0 only if every run holds, and prints one line per run.
The command record beside this directory lists the recorded outcome.
