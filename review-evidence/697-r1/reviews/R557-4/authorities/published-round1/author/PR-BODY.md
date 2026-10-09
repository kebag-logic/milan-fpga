[A569]

Relates to kebag-logic/milan-fpga#697 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074245112)).

Import the portable ADP, ACMP and MAAP cores and wire helpers from revision `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. Preserve 26 filtered commits and merge them onto the initial repository history. Rewrite identities and apply MIT identifiers while retaining copyright lines. Production code matches the source after the identifier change.

Split the core cases from mixed tests. Exclude the saved-state adapter because it depends on an external state interface. Keep SRP as the separate Apache-2.0 [lwSRP component](https://github.com/kebag-logic/lwSRP). The consumer submodule and firmware-image checks remain a later step.

Build and test:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j16
ctest --test-dir build --output-on-failure -j16
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
```

The validation kit passes 365 test instances, all 311 core plants and 325 required assertion failures. Every test declaration has a named defect control. Adjusted line and branch coverage is 100%; five inherited exclusion rows identify seven unreachable arcs and two statements. Both supported C11 compiler builds, address and undefined-behavior sanitizers, static analysis with listed suppressions, boundary and licence controls, traceability, privacy and all three diagram renders pass.

The hosted [quality workflow](.github/workflows/quality.yml) runs the same kit. Hosted execution awaits publication of this branch.

Quality documents:

- [Architecture](docs/ARCHITECTURE.md), [porting and example](docs/PORTING.md), and [coding standard](docs/CODING_STANDARD.md).
- [Requirements](docs/REQUIREMENTS.md), generated [traceability](docs/TRACEABILITY.md), and [deviations](docs/DEVIATIONS.md).
- [Verification](docs/VERIFICATION.md), [test defects](docs/TESTS.md), [coverage exclusions](docs/COVERAGE.md), and [static-analysis suppressions](docs/STATIC_ANALYSIS.md).
- [Import record](docs/IMPORT.md), [contribution rules](CONTRIBUTING.md), [security policy](SECURITY.md), and [change log](CHANGELOG.md).

The repository remains private. Two independent reviews and the required licence and documentation merges precede any visibility change.
