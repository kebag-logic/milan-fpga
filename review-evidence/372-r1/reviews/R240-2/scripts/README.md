R240-2 reproducibility
====================

All shell invocations use RTK. Scripts accept a source checkout and, where needed,
the scoped Verilator selector as positional arguments. Their output directory is
the parent of this scripts directory, so copy scripts/ and probes/ into a fresh
output directory to reproduce without overwriting receipts. The checkout must be
the exact source identified in REPORT.md with all three required submodules.

`record.py NAME COMMAND...` records the exact argument vector, working directory,
UTC start/end and exit in raw/NAME.json and complete output in raw/NAME.log.
It prefixes the executed command with `rtk proxy`.

Initial read-only public acquisition commands are in raw/issue.json, pr.json,
assignment.json, old-findings.json, and evidence-tree.json. Run those commands
through record.py, then run fetch_evidence.py. This downloads only the immutable
corrected-source manager packet, verifies each Git blob, and writes the public
hash manifest. It does not query checks or workflow APIs.

Run from the source checkout; placeholders below are arguments, not environment
variable names to overwrite:

```text
rtk proxy mkdir -p <output>/raw
rtk proxy python3 <output>/scripts/record.py tool-identity python3 <output>/scripts/tool_identity.py <verilator-5.050-selector>
rtk proxy python3 <output>/scripts/record.py initial-integrity python3 <output>/scripts/integrity.py <source>
rtk proxy python3 <output>/scripts/record.py source-proof python3 <output>/scripts/source_proof.py <source>
rtk proxy python3 <output>/scripts/record.py focused-mux make --no-print-directory -C <output>/scratch/tb/verilator/ptp_ts mux-sva VERILATOR=<verilator-5.050-selector>
rtk proxy python3 <output>/scripts/record.py focused-campaign python3 -B <output>/scratch/tb/verilator/ptp_ts/sva_campaign.py --verilator <verilator-5.050-selector>
```

Wait for every build to terminate before starting another. Each checker build
uses at most eight jobs. The campaign uses the exact committed executable and
retains each mutant source, build log and run log under scratch/.

The semantics probe's full build vector is raw/semantics-build.json. The command
uses the standalone reviewer SV/CPP, the exact source stream checker, --assert,
-Wall, --top-module semantics_probe and -j 8. Run its resulting binary through
record.py semantics-run. It grades first-history and complete reset-action
timelines itself, including a deliberately incorrect witness flag as a control.

```text
rtk proxy python3 <output>/scripts/record.py focused-controls python3 -B <output>/scripts/focused_controls.py <source> <verilator-5.050-selector>
rtk proxy python3 <output>/scripts/record.py result-audit python3 -B <output>/scripts/audit_results.py <source>
rtk proxy python3 <output>/scripts/record.py tally-verdict python3 -B scripts/suite_tally.py --verdict <output>/raw/focused-suite-composed.log
rtk proxy python3 <output>/scripts/record.py final-inputs python3 -B <output>/scripts/final_inputs.py <source>
rtk proxy python3 <output>/scripts/record.py final-integrity python3 -B <output>/scripts/integrity.py <source>
```

focused_controls.py records all 62 of its commands separately in
raw/focused-controls-results.json. These are distinct from the 62 campaign rows.
It runs the original timestamp leg with only its build parallelism capped at 8,
40 extra seed runs, 12 malformed-input runs (expected exit 2), two default-limit
faults (expected exit 1), six documentation checks, and whitespace validation.
No full parent/native/builder bank runs. The timestamp FIFO is copied from the
verified required gitlink, with its hash printed.

audit_results.py independently derives all 21 property keys from the SV labels,
checks both 15/2/4 witness populations, requires named detections for every key,
and verifies the explicitly composed 495-check focused log using suite_tally.
It also verifies the exact source/base and successful exit population of the
public manager ledgers. It does not relabel a composed log as one invocation.

integrity.py compares exact tracked bytes/kinds/modes, all stage-zero index
records, hidden-index flags, registered submodule HEADs and contents, with Git
replacement objects disabled. final_inputs.py independently rehashes exported
build inputs and records generated-model hashes.

The original two failed mtree receipt-script attempts are retained. The final
tool_identity.py handles mtree inherited defaults and excludes archive-only
metadata, checks 123 installed files, and records the four absent manual pages.
Those corrections affect only reviewer receipt scripts, not reviewed source.

MANIFEST.sha256 covers the report, scripts, public evidence, raw receipts,
probes, generated models and scratch campaign artifacts. No private reasoning
or source edit is included.
