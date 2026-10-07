All 16 shell-command occurrences ran from an exact-head disposable source copy.
Dependency discovery variables point only to the disposable local installation.
The isolated compile entry includes the complete here-document in commands.json.

| Page and line | Command | rc | Receipt |
| --- | --- | --- | --- |
| README.md:35 | `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | 0 | [quick-start-35.log](quick-start-35.log) |
| README.md:36 | `cmake --build build --parallel 2` | 0 | [quick-start-36.log](quick-start-36.log) |
| README.md:37 | `ctest --test-dir build --output-on-failure` | 0 | [quick-start-37.log](quick-start-37.log) |
| README.md:38 | `behave` | 0 | [quick-start-38.log](quick-start-38.log) |
| doc/tester.md:15 | `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | 0 | [published-configure.log](published-configure.log) |
| doc/tester.md:16 | `cmake --build build --parallel 2` | 0 | [published-build.log](published-build.log) |
| doc/tester.md:17 | `ctest --test-dir build --output-on-failure` | 0 | [published-ctest.log](published-ctest.log) |
| doc/tester.md:18 | `./build/unit_tests` | 0 | [published-unit.log](published-unit.log) |
| doc/tester.md:19 | `behave` | 0 | [published-scenarios.log](published-scenarios.log) |
| doc/tester.md:20 | `behave --dry-run` | 0 | [published-scenario-dry.log](published-scenario-dry.log) |
| doc/tester.md:45 | `isolated compile command and complete here-document, as printed on the page` | 0 | [published-isolated-compile.log](published-isolated-compile.log) |
| doc/tester.md:53 | `./build/mrp_pdu_tests` | 0 | [published-isolated-run.log](published-isolated-run.log) |
| doc/tools/README.md:14 | `python3 doc/tools/check_sentences.py` | 0 | [docs-sentences.log](docs-sentences.log) |
| doc/tools/README.md:15 | `python3 doc/tools/check_references.py` | 0 | [docs-references.log](docs-references.log) |
| doc/tools/README.md:16 | `python3 doc/tools/check_links.py --github-auth` | 1 | [docs-links.log](docs-links.log) |
| doc/tools/README.md:17 | `python3 doc/tools/render_mermaid.py --output <packet>/graphs` | 0 | [docs-render-published.log](docs-render-published.log) |

Only the expected eight licence-link failures returned nonzero.
Every command has a matching .rc receipt. Raw process output changes only by path normalization.
