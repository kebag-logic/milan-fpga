[A342] Refuse descriptor bodies that disagree with their directory keys.

Closes #123

The packer now compares the assembled body's big-endian type and index with
its normalized directory key. A mismatch raises `ImageError` with the
configuration, key values and body values. The same refusal covers `fields`
and literal `bytes`; image layout and RTL are unchanged.

The existing `desc_store` run target now gates six generator tests covering
24 cases through `build()` and the CLI. Legal controls preserve the packed
bytes; type-only and index-only mismatches fail independently for both input
forms. The CLI returns 1 without writing an image or map. Removing only the
new check makes all 16 refusal cases fail while all eight legal controls pass.

All nine existing generated image paths, plus all eight new legal probe images,
match the base revision byte-for-byte. The worked example and `tb/desc_store`
image retain SHA-256
`20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c`.

Validation passed (all rc 0): `make check`, `scripts/run_suites.sh` (33 suites,
1,014,722 checks), `scripts/lint_hdl.sh`, `syn/yosys/run.sh`, module-matrix and
parameter inventory checks, every CI documentation gate including the 46-build
`nvm_port` figure check, `python3 scripts/check-links.py`, and `git diff --check`.
Detailed change references, test/mutant tables, image digest pairs and gate logs
are recorded in the accompanying `HANDOFF.md`.

The parent shipping-image comparison remains the assigned consumer check at
the new pin; this change makes no parent edits and leaves issue #60's
published acceptance untouched.
