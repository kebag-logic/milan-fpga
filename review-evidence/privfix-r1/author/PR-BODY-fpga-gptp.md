[A869]

## Summary

Remove bench-specific names from documentation and tools.

One historical bench note named the programming cable of the lab board by its own identifier. The load command now shows the `<serial>` placeholder for that argument, so the page still tells a reader which option to pass and what goes in it.

- `docs/history/v1/BENCH_FIRSTLIGHT.md`: one line, `--ftdi-serial <serial>`.

Nothing else changes: no HDL, microcode, testbench, script or diagram is touched.

## Testing

- `make docs` passes before and after the change: the diagram check and its self-test, the docs check (14 current pages, 18 historical) and its self-test (127 arms), and the source-evidence check (20 exact, 0 findings) and its self-test.
- `git diff --stat`: 1 file, 1 line changed.
