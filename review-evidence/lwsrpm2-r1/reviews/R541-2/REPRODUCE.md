<!-- SPDX-License-Identifier: Apache-2.0 -->
Run against the exact source head named in the [report](REPORT.md).
Use a new packet directory containing these scripts and an empty scratch directory.
Set SOURCE to the detached clone and PACKET to that directory.
Receipts replace those two location prefixes with portable aliases.
Other process output is preserved.

The [dependency bootstrap](scripts/bootstrap.py) installs the pinned [unit framework](https://github.com/cgreen-devs/cgreen/tree/1.6.3) under scratch.
The [suite driver](scripts/run_checks.py) runs both profiles and documentation checks concurrently.
Its reversal phase runs both published campaigns concurrently and waits for completion.
The [probe driver](scripts/run_probes.py) runs the independent [literal-wire and allocation checks](scripts/probe.c).
The [fault driver](scripts/own_plants.py) adds three independent plants per profile.
Every campaign writes logs and return codes.
No worker outlives its foreground driver.

~~~sh
python3 "$PACKET/scripts/bootstrap.py" --packet "$PACKET"
python3 "$PACKET/scripts/run_checks.py" --source "$SOURCE" --packet "$PACKET" --jobs 4
python3 "$PACKET/scripts/run_checks.py" --source "$SOURCE" --packet "$PACKET" --jobs 2 --phase reversals
python3 "$PACKET/scripts/run_probes.py" --source "$SOURCE" --packet "$PACKET" --jobs 2
python3 "$PACKET/scripts/own_plants.py" --source "$SOURCE" --packet "$PACKET" --profile OFF
python3 "$PACKET/scripts/own_plants.py" --source "$SOURCE" --packet "$PACKET" --profile ON
python3 "$PACKET/scripts/guard_audit.py" --source "$SOURCE" --packet "$PACKET"
python3 "$PACKET/scripts/audit_source.py" --source "$SOURCE" --output "$PACKET/receipts/final-source-audit.json"
~~~

The order and allocation probe modes intentionally return one at this head.
They reproduce the two functional findings.
All other probe modes return zero, including the allocation control.
The [mutation ledger](receipts/mutation-ledger.tsv) distinguishes successful builds from expected failing checks.

The [guard audit](scripts/guard_audit.py) complements manual inspection of the changed guards.
The [integrity audit](scripts/audit_source.py) checks every tracked blob, mode, index entry, and submodule entry.
The published scripts contain no source fixes.
Temporary dependencies, source exports, binaries, and graph images remain under scratch.
