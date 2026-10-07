# Round 2 published commands

All shell command occurrences execute in a scratch source snapshot. The dependency installation is reused from Round 1.

| Page and line | Command | rc |
| --- | --- | --- |
| README.md:35 | `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | 0 |
| README.md:36 | `cmake --build build --parallel 2` | 0 |
| README.md:37 | `ctest --test-dir build --output-on-failure` | 0 |
| README.md:38 | `behave` | 0 |
| doc/tester.md:15 | `cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | 0 |
| doc/tester.md:16 | `cmake --build build --parallel 2` | 0 |
| doc/tester.md:17 | `ctest --test-dir build --output-on-failure` | 0 |
| doc/tester.md:18 | `./build/unit_tests` | 0 |
| doc/tester.md:19 | `behave` | 0 |
| doc/tester.md:20 | `behave --dry-run` | 0 |
| doc/tester.md:45 | `cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o build/mrp_pdu_tests <<'C'<br>#include <cgreen/cgreen.h><br>TestSuite *mrp_pdu_suite(void);<br>int main(void)<br>{<br>    return run_test_suite(mrp_pdu_suite(), create_text_reporter());<br>}<br>C` | 0 |
| doc/tester.md:53 | `./build/mrp_pdu_tests` | 0 |
| doc/tools/README.md:14 | `python3 doc/tools/check_sentences.py` | 0 |
| doc/tools/README.md:15 | `python3 doc/tools/check_references.py` | 0 |
| doc/tools/README.md:16 | `python3 doc/tools/check_links.py --github-auth` | 1 |
| doc/tools/README.md:17 | `python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"` | 0 |
