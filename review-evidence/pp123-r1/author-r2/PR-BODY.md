Refuse descriptor bodies that disagree with their directory keys.

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

## Round 2

Every public helper and test in `tb/desc_store/test_gen_desc_image.py` now has
a complete signature and a docstring describing what it builds or proves.
The CLI probe no longer carries a host deadline; the runner bounds hangs.
The generator input sketch now includes `descriptor_index`, and the F07.4
notes state that descriptor bytes 0–3 must equal the index-map type/index key
and that the generator refuses a disagreement.

These changes preserve round-1 behavior. All nine generated image paths and
eight legal probe images are byte-identical at base, round 1 and round 2,
with the same published digests. The six tests / 24 cases pass, and the
round-1 mutant still yields eight legal passes and sixteen refusal failures.

The unchanged review scans pass on archive exports of base and the new head:
zero unannotated public functions, zero undocumented public functions, and
zero added files using a host clock or process deadline.

All listed gates were rerun at `11dd3e903685183250e7cd8ecc391b04fe7fd494` and passed,
including all 33 suites / 1,014,722 checks and the 46-build figure gate.
The parent DUT-source reader disposition and consumer-bank rerun remain in
the parent pin-update patch.
