# Round 2i evidence

Head: `7426045c94c317363e5589856e6f3f9fde1a2d21`.
Parent: `8e4b1e53e9b5a8ef5f9854095347436ab84259b6`.

`validation-summary.json` lists 48 passing validation jobs. `jobs/` retains
commands, logs, return codes and elapsed times. The two parent-reader raw
return codes are expected 1; their validation wrapper returns 0.
The builder returns 0 with its historical gate-11 placed-report arm uncovered.

`source-binding.json` binds the five changed files and unchanged scope.
`fresh-trace-tables.json` records full-trace SHA-256 values and sizes.
`fresh-tables/` contains bounded PDU excerpts and tables, while `traces/`
contains complete servo records. `jobs/trace-*.log` contains event records.

`public-round2h-verification.json` verifies the published 277-file manifest
and 45 source bindings. `hosted-timings.json` and the verdict-window log
record actual hosted windows at the parent head. Later acceptance belongs
to the manager after publication.

Run `python3 -B scripts/reproduce.py SOURCE OUTPUT` from this packet,
with OUTPUT outside the source checkout, for the retained diagnostic replay.
The public decimal probe in `scripts/decimal_boundaries.py` is unchanged.

Paths in receipts use `$LANE`, `$BUILD_AREA`, `$TOOLS`, `$RISCV_SDK`,
`$USER_HOME` and `$HOSTED_WORKSPACE` placeholders. Original and retained
hashes, sizes and substitutions are recorded in `retained-files.json`.
`MANIFEST.sha256` covers the retained packet except itself. No file exceeds
200000 bytes. Full generated products remain outside this packet.
