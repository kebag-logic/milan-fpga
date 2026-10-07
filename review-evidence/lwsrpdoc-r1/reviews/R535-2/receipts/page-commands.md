# Published command ledger

Exact source head: cd659eb5e93c4da5e97fcbd6282b1efba16e565d.
All 17 occurrences executed, including both repeated configure/build/test/scenario sequences.
Scratch dependency discovery variables were set; the documented optional browser configuration placed the browser profile in scratch.
All command streams preserve exit codes; absolute packet/source prefixes are normalized.

| Page and line | Command | rc | Raw receipt |
| --- | --- | --- | --- |
| [README.md:35](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/README.md#L35) | `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | 0 | [host-configure.log](host-configure.log) |
| [README.md:36](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/README.md#L36) | `cmake --build build --parallel 2` | 0 | [host-build.log](host-build.log) |
| [README.md:37](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/README.md#L37) | `ctest --test-dir build --output-on-failure` | 0 | [ctest.log](ctest.log) |
| [README.md:38](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/README.md#L38) | `behave` | 0 | [scenarios.log](scenarios.log) |
| [doc/tester.md:15](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tester.md#L15) | `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | 0 | [tester-configure.log](tester-configure.log) |
| [doc/tester.md:16](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tester.md#L16) | `cmake --build build --parallel 2` | 0 | [tester-build.log](tester-build.log) |
| [doc/tester.md:17](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tester.md#L17) | `ctest --test-dir build --output-on-failure` | 0 | [tester-ctest.log](tester-ctest.log) |
| [doc/tester.md:18](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tester.md#L18) | `./build/unit_tests` | 0 | [unit-direct.log](unit-direct.log) |
| [doc/tester.md:19](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tester.md#L19) | `behave` | 0 | [tester-scenarios.log](tester-scenarios.log) |
| [doc/tester.md:20](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tester.md#L20) | `behave --dry-run` | 0 | [scenario-dry-run.log](scenario-dry-run.log) |
| [doc/tester.md:45](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tester.md#L45) | `cc command and complete here-document` | 0 | [codec-compile.log](codec-compile.log) |
| [doc/tester.md:53](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tester.md#L53) | `./build/mrp_pdu_tests` | 0 | [codec-run.log](codec-run.log) |
| [doc/tools/README.md:14](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tools/README.md#L14) | `python3 doc/tools/check_sentences.py` | 0 | [sentences.log](sentences.log) |
| [doc/tools/README.md:15](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tools/README.md#L15) | `python3 doc/tools/check_references.py` | 0 | [references.log](references.log) |
| [doc/tools/README.md:16](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tools/README.md#L16) | `python3 doc/tools/check_references.py --self-test` | 0 | [reference-self-test.log](reference-self-test.log) |
| [doc/tools/README.md:17](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tools/README.md#L17) | `python3 doc/tools/check_links.py --github-auth` | 1 | [links.log](links.log) |
| [doc/tools/README.md:18](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tools/README.md#L18) | `python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"` | 0 | [graph-render-final.log](graph-render-final.log) |
