R213 round-four evidence for exact head 02c47cf0dbe7062ff762068875bf70b721dd6b37.

Scripts ran from the assigned temporary root; copies are retained here. Logs normalize home paths to `$HOME` and em dashes to ASCII. The scripts use the reviewed clone and assigned scratch root. `runner.py` runs commands synchronously with CPUs 64-79, MAKEFLAGS=-j8, temporary output and bytecode disabled. Modes `absent` and `elf` use temporary homes and PATH directories, leaving installed compilers untouched.

`runner.py` imports the complete builder for focused gate runs. For `probe.py` and `residual.py`, it exposes unchanged nested functions by returning locals immediately before the gate baseline call in an in-process AST. No tracing hooks, compiler callbacks, or instrumentation of other processes are used. Base probes load only the validation-base test file against unchanged current implementation artifacts. Base traceback displayed source lines can refer to the current file; the exception result is from the base code.

`publication.py` checks the predicate and plants both original later-write variants into the publication source for complete gate 35, restoring its original bytes in finally blocks. Its formatting positives test the AST predicate, not the mutation-site regex. All other source variants are in-memory data. Probe exit 0 means expected observations matched; individual REFUSE and ACCEPT results are retained separately.

`focused-checks.json` contains every static/documentation/host-test command and exit code. `tracked-byte-check.json` hashes every tracked blob in the main tree and all three required submodules. `hosted-checks.json` records exact-head status observations, not local executions.
