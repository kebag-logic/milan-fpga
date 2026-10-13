R585-19 focused reproduction

Use an isolated exact-head checkout with the five required submodules initialized. All disposable files belong below this packet's `scratch/` directory. Scripts accept checkout/work paths; no source fix is made. `verify_checkout.py` verifies raw Git blob bytes, modes, index entries and the required submodule revisions rather than trusting status alone.

Recorded environment: CPython 3.12.3, Git 2.56.0, native GCC/G++ 16.2.1, Clang 23.1.1, CMake 4.4.4, GoogleTest/GoogleMock 1.14.0, the pinned Bootlin RV32 SDK (GCC 14.3.0), Verilator 5.050. `receipts/environment.json` and setup receipts give observed identities. The ordinary `clang` executable is used by the stack boundary. An unused, broken `clang-18` shim on PATH was not used by that check. Source-author receipts name their own environment separately.

Create an isolated Python environment under `scratch/`, install `sw/litex/litex_pins.txt` and PyYAML, behave, cmarkgfm and html5lib there, and provide the documented SDK/compiler dependencies. Use `scripts/ci_rv32_sdk.py` with the pinned archive if a private SDK extraction is needed. Set `TMPDIR` to `scratch/`, `PYTHONDONTWRITEBYTECODE=1`, `MILAN_RV32_CC` to that SDK's `bin/riscv32-linux-gcc`, and `VERILATOR` to a verified 5.050 executable. Put the isolated Python on PATH. Set the GoogleTest prefix's include, library and pkg-config paths as needed. Set `VERILATOR_JOBS=4`.

The actual argv and exit code for each execution appear at the beginning/end of its `.log`, with a separate `.rc`. Those absolute paths identify the original run; substitute your isolated checkout and packet paths. All runs were foreground commands. Independent batches ran concurrently with separate logs, no more than 16 build workers and a 12 GiB unit cap. `run_batch.py` runs a bounded batch to completion and does not detach children.

Representative commands, where `ROOT`, `PACKET` and `PY` below stand for the checkout, packet and isolated Python executable (ordinary task variables, not environment home variables):

```sh
"$PY" "$PACKET/scripts/verify_checkout.py" "$ROOT"
"$PY" "$PACKET/scripts/pin_order_probe.py" "$ROOT" "$PACKET/scratch/repro-pin"
"$PY" "$PACKET/scripts/f5_capture_probe.py" "$ROOT" "$PACKET/scratch/repro-capture"
"$PY" "$PACKET/scripts/held_text_probe.py" "$ROOT"
"$PY" "$PACKET/scripts/structure_audit.py" "$ROOT" "$PACKET/receipts/public-author"
```

Run the following from the checkout. Each work path must be fresh. Run independent campaigns concurrently within the worker and memory caps, then collect every exit code in the foreground.

```sh
"$PY" -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
"$PY" -B tb/verilator/milan_dp/stream_counter_f5.py --shape 1 --work "$PACKET/scratch/repro-f5-1"
"$PY" -B tb/verilator/milan_dp/stream_counter_f5.py --shape 8 --work "$PACKET/scratch/repro-f5-8"
"$PY" -B tb/verilator/milan_dp/stream_counter_f5.py --variant late --work "$PACKET/scratch/repro-f5-late"
"$PY" -B tb/verilator/milan_dp/stream_counter_f5.py --variant rate --work "$PACKET/scratch/repro-f5-rate"
"$PY" -B tb/verilator/milan_dp/stream_counter_f5.py --variant fixed-grid --work "$PACKET/scratch/repro-f5-grid"
"$PY" tb/verilator/milan_dp/stream_counters.py --shape 1 --work "$PACKET/scratch/repro-stream-1"
"$PY" tb/verilator/milan_dp/stream_counters.py --shape 8 --work "$PACKET/scratch/repro-stream-8"
"$PY" tb/verilator/milan_dp/stream_counters.py --shape 1 --output-condition frames-only --work "$PACKET/scratch/repro-frames-1"
"$PY" tb/verilator/milan_dp/stream_counters.py --shape 8 --output-condition frames-only --work "$PACKET/scratch/repro-frames-8"
"$PY" tb/verilator/milan_dp/stream_counters.py --variant tx-nodirty --work "$PACKET/scratch/repro-no-dirty"
"$PY" scripts/suite_shards.py --selftest
"$PY" tb/tools/torture_campaign.py --self-test
"$PY" scripts/ci_events.py --check
"$PY" scripts/ci_events.py --selftest
"$PY" scripts/measure_test_evidence.py --check
"$PY" scripts/measure_test_evidence.py --selftest
"$PY" scripts/docs_check.py
"$PY" scripts/check_submodule_docs.py
"$PY" scripts/check_py_idiom.py
"$PY" scripts/check_em_dash.py --base e81ce82f
```

From `tests/`, run `"$PY" -m behave --no-capture -f plain features/counters_contract_milan.feature`.

The firmware boundary's captured campaign commands already supply `--jobs 4`. The focused F5/counter drivers expose no `--jobs` argument; their build setting and `VERILATOR_JOBS` bound their workers. The pin-order probe invokes make with `-j16` and a compiler sentinel, and requires refusal before the sentinel or staging is reached.

`f5_capture_probe.py` clones only into its supplied work directory, captures both clean build-only shapes, checks their attribution and removal refusals, then builds a private-stack-include mutation in that disposable clone. The compilation must succeed while the boundary rejects the forbidden dependency. Its source file is restored in a `finally` block. The reviewed checkout is not mutated. The held-text script is the unchanged public composition-review script; its blob identity and SHA-256 are in `receipts/prior-probe-provenance.json`.

Three failed attempts precede the successful isolated capture: two lacked initialized build dependencies in the disposable clone, and one asserted the wrong log spelling (`BUILT` instead of `built, not run (--build-only)`). Their logs and nonzero return codes are retained. The corrected probe still requires no test execution. An earlier `measure_test_evidence_readers.py --selftest` invocation merely loaded a data module; it is recorded but credited as no test. The real measurement program's `--check` and `--selftest` both subsequently passed.

Do not infer full-bank execution from these focused commands. Author source-head receipts are copied with immutable publication/blob provenance; they are not this reviewer's rebuilt image or manager-bank results. Final current-dev candidate banks and hosted/local-replica acceptance belong to the manager. Re-run `verify_checkout.py` after all experiments and verify this packet with `sha256sum -c MANIFEST.sha256`.
